#!/usr/bin/env python3
"""
AlgoAnimator Server: Lightweight REST API & Web Service for Algorithm Simulation & Animation.
Serves interactive visualizer and endpoints for GitHub Copilot CLI and Dev Tunnel integration.
"""

import json
import os
import sys
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlparse

from schema import AnimationSpec
from simulator import get_trapping_rain_water_corner_cases, simulate_trapping_rain_water
import algoanimate

PORT = int(os.environ.get("PORT", 8000))
BASE_DIR = Path(__file__).resolve().parent
DOCS_DIR = BASE_DIR / "docs"
TEMPLATE_PATH = BASE_DIR / "renderer.html"

class AlgoAnimatorHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        # Serve static files from docs directory by default if it exists
        super().__init__(*args, directory=str(DOCS_DIR if DOCS_DIR.exists() else BASE_DIR), **kwargs)

    def end_headers(self):
        # Enable CORS for cross-origin Dev Tunnel / GitHub Pages calls
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization, X-Requested-With")
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path == "/health":
            self.send_json(200, {
                "status": "healthy",
                "service": "algo-animator",
                "version": "2.0.0",
                "gemini_configured": bool(os.environ.get("GEMINI_API_KEY"))
            })
            return

        if path == "/api/algorithms":
            cases = get_trapping_rain_water_corner_cases()
            self.send_json(200, {
                "algorithms": [
                    {
                        "id": "trapping-rain-water",
                        "name": "Trapping Rain Water",
                        "paradigm": "Two Pointers",
                        "complexity": {"time": "O(N)", "space": "O(1)"},
                        "corner_cases": [{"name": c.name, "description": c.description, "data": c.data, "expected": c.expected_output} for c in cases]
                    }
                ]
            })
            return

        # Fallback to static files
        super().do_GET()

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path

        content_len = int(self.headers.get("Content-Length", 0))
        post_body = self.rfile.read(content_len).decode("utf-8") if content_len > 0 else "{}"
        try:
            data = json.loads(post_body)
        except Exception as e:
            self.send_json(400, {"error": f"Invalid JSON payload: {e}"})
            return

        if path == "/api/animate":
            algo_text = data.get("algorithm", "Custom Algorithm")
            code_text = data.get("code", algoanimate.SAMPLE_CSHARP_CODE)
            input_val = data.get("input", "")
            audience = data.get("audience", "interview")

            try:
                import simulator
                # If Gemini API key is available, run model; otherwise use universal simulator
                if os.environ.get("GEMINI_API_KEY"):
                    try:
                        prompt = algoanimate.build_prompt(algo_text, input_val, audience, code_text)
                        spec = algoanimate.call_gemini(prompt)
                        if not spec.source_code:
                            spec.source_code = code_text
                    except Exception as ge:
                        print(f"Gemini call error: {ge}, using auto_simulate fallback.")
                        spec = simulator.auto_simulate(code_text, input_val, algo_text)
                else:
                    spec = simulator.auto_simulate(code_text, input_val, algo_text)

                # Render HTML
                template = TEMPLATE_PATH.read_text(encoding="utf-8")
                payload = json.dumps(spec.model_dump(), ensure_ascii=False).replace("</", "<\\/")
                html = template.replace("__SPEC__", payload)

                self.send_json(200, {
                    "spec": spec.model_dump(),
                    "html": html,
                    "title": spec.title,
                    "algorithm": spec.algorithm,
                    "scenes_count": len(spec.scenes)
                })
            except Exception as e:
                import traceback
                traceback.print_exc()
                self.send_json(500, {"error": str(e)})
            return

        if path == "/api/simulate-corner-cases":
            code_text = data.get("code", algoanimate.SAMPLE_CSHARP_CODE)
            import simulator
            profile = simulator.synthesize_test_cases_from_code(code_text)
            cases = profile.get("corner_cases", [])
            results = []

            for case_info in cases:
                case_input = case_info["input"]
                case_spec = simulator.auto_simulate(code_text, case_input, profile.get("algorithm"))
                results.append({
                    "case_name": case_info["name"],
                    "description": case_info["description"],
                    "input": case_input,
                    "expected": case_info.get("expected"),
                    "scenes_count": len(case_spec.scenes),
                    "spec": case_spec.model_dump()
                })

            self.send_json(200, {
                "algorithm": profile.get("algorithm", "Algorithm"),
                "paradigm": profile.get("paradigm", "general"),
                "total_cases": len(cases),
                "results": results
            })
            return

        self.send_json(404, {"error": f"Endpoint not found: {path}"})

    def send_json(self, status: int, data: dict):
        resp_bytes = json.dumps(data, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(resp_bytes)))
        self.end_headers()
        self.wfile.write(resp_bytes)

def run_server(port=PORT):
    server_address = ("", port)
    httpd = HTTPServer(server_address, AlgoAnimatorHandler)
    print(f"\n🚀 AlgoAnimator Server running at http://localhost:{port}")
    print(f"  ├─ Health:  http://localhost:{port}/health")
    print(f"  ├─ API:     http://localhost:{port}/api/algorithms")
    print(f"  └─ Web UI:  http://localhost:{port}/\n")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping server...")
        httpd.server_close()

if __name__ == "__main__":
    run_server()

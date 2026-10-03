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
            algo_text = data.get("algorithm", "Trapping Rain Water")
            code_text = data.get("code", algoanimate.SAMPLE_CSHARP_CODE)
            input_val = data.get("input", "[0,1,0,2,1,0,1,3,2,1,2,1]")
            audience = data.get("audience", "interview")

            try:
                # If Gemini API key is available, run model; otherwise use simulation engine
                if os.environ.get("GEMINI_API_KEY"):
                    prompt = algoanimate.build_prompt(algo_text, input_val, audience, code_text)
                    spec = algoanimate.call_gemini(prompt)
                    if not spec.source_code:
                        spec.source_code = code_text
                else:
                    # Clean input array
                    import ast
                    clean_arr = ast.literal_eval(input_val) if isinstance(input_val, str) and input_val.startswith("[") else [0,1,0,2,1,0,1,3,2,1,2,1]
                    from simulator import CornerTestCase
                    custom_case = CornerTestCase("Custom Input", "User provided input data", clean_arr, None)
                    _, spec = simulate_trapping_rain_water(custom_case, code_text)

                # Render HTML
                template = TEMPLATE_PATH.read_text(encoding="utf-8")
                payload = json.dumps(spec.model_dump(), ensure_ascii=False).replace("</", "<\\/")
                html = template.replace("__SPEC__", payload)

                self.send_json(200, {
                    "spec": spec.model_dump(),
                    "html": html,
                    "title": spec.title,
                    "scenes_count": len(spec.scenes)
                })
            except Exception as e:
                self.send_json(500, {"error": str(e)})
            return

        if path == "/api/simulate-corner-cases":
            code_text = data.get("code", algoanimate.SAMPLE_CSHARP_CODE)
            cases = get_trapping_rain_water_corner_cases()
            results = []

            for case in cases:
                out_val, spec = simulate_trapping_rain_water(case, code_text)
                passed = (out_val == case.expected_output)
                results.append({
                    "case_name": case.name,
                    "description": case.description,
                    "input": case.data,
                    "expected": case.expected_output,
                    "actual": out_val,
                    "passed": passed,
                    "scenes_count": len(spec.scenes),
                    "spec": spec.model_dump()
                })

            self.send_json(200, {
                "algorithm": "Trapping Rain Water",
                "total_cases": len(cases),
                "passed_cases": sum(1 for r in results if r["passed"]),
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

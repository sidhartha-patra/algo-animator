#!/usr/bin/env python3
"""
AlgoAnimator Dev Tunnel Launcher.
Hosts a Microsoft Dev Tunnel exposing the AlgoAnimator backend service
so GitHub Copilot CLI, GitHub Pages, and remote agents can call the simulation API.
"""

import os
import shutil
import subprocess
import sys
import time
import socket

def is_port_in_use(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('127.0.0.1', port)) == 0

def main():
    port = int(os.environ.get("PORT", 8000))
    devtunnel_cmd = shutil.which("devtunnel") or shutil.which("devtunnel.exe")

    if not devtunnel_cmd:
        print("❌ devtunnel CLI not found in PATH.")
        print("Install it from: https://aka.ms/devtunnels")
        sys.exit(1)

    print("════════════════════════════════════════════════════════════════════")
    print("      🚀 AlgoAnimator Dev Tunnel & Backend Service")
    print("════════════════════════════════════════════════════════════════════")

    # Start local backend server if not running
    server_process = None
    if not is_port_in_use(port):
        print(f"[*] Starting local AlgoAnimator server on port {port}...")
        server_py = os.path.join(os.path.dirname(__file__), "server.py")
        server_process = subprocess.Popen([sys.executable, server_py])
        time.sleep(1.5)
    else:
        print(f"[✓] Local server is already running on port {port}.")

    print(f"[*] Launching devtunnel on port {port} with anonymous access...")
    print("[*] To use this in GitHub Copilot CLI or the GitHub Page, copy the public URL.\n")

    cmd = [devtunnel_cmd, "host", "-p", str(port), "--allow-anonymous"]
    try:
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print("\nStopping dev tunnel...")
    finally:
        if server_process:
            print("Stopping server process...")
            server_process.terminate()

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Audio Compression Analysis Tool
Entry point for the Streamlit dashboard.
"""

import subprocess
import sys
import os

DEFAULT_PORT = 8501


def get_process_ids_for_port(port):
    """Return process IDs listening on the given port."""
    pids = []
    if sys.platform.startswith("win"):
        result = subprocess.run(["netstat", "-aon"], capture_output=True, text=True)
        for line in result.stdout.splitlines():
            if f":{port}" in line and "LISTENING" in line:
                parts = line.split()
                if parts:
                    pid = parts[-1]
                    if pid.isdigit():
                        pids.append(pid)
    else:
        try:
            result = subprocess.run(["lsof", "-ti", f"tcp:{port}"], capture_output=True, text=True)
            for line in result.stdout.splitlines():
                pid = line.strip()
                if pid.isdigit():
                    pids.append(pid)
        except FileNotFoundError:
            pass
    return list(set(pids))


def kill_process(pid):
    """Terminate a process by PID."""
    if sys.platform.startswith("win"):
        subprocess.run(["taskkill", "/PID", str(pid), "/F"], capture_output=True)
    else:
        subprocess.run(["kill", "-9", str(pid)], capture_output=True)


def cleanup_port(port):
    """Kill any stale process listening on the given port."""
    pids = get_process_ids_for_port(port)
    for pid in pids:
        print(f"Stopping stale process on port {port}: PID {pid}")
        kill_process(pid)
    return pids


def fix_streamlit_config():
    """Fix Streamlit config mismatches before launching the app."""
    try:
        from streamlit import config
        
        # Fix toolbar mode if it's incorrectly parsed as a dict
        toolbar_mode = config.get_option("client.toolbarMode")
        if isinstance(toolbar_mode, dict):
            mode_str = toolbar_mode.get("mode", "minimal")
            config.set_option("client.toolbarMode", mode_str)
            print(f"Fixed toolbar mode: {mode_str}")
    except Exception as e:
        # Silently fail if this can't be done
        pass



def main():
    """Start the Streamlit dashboard."""
    print("Starting Audio Compression Analysis...")

    # Ensure output directories exist
    os.makedirs("data/original", exist_ok=True)
    os.makedirs("output/encoded", exist_ok=True)
    os.makedirs("output/decoded", exist_ok=True)
    os.makedirs("output/reports", exist_ok=True)

    # Port configuration
    port = int(os.environ.get("STREAMLIT_PORT", DEFAULT_PORT))

    # Clean up a stale listener on the port before launching
    cleanup_port(port)
    
    # Fix Streamlit config issues before starting
    fix_streamlit_config()

    # Path to dashboard
    dashboard_path = os.path.join(os.path.dirname(__file__), "src", "dashboard.py")

    # Run Streamlit
    subprocess.run([
        sys.executable,
        "-m",
        "streamlit",
        "run",
        dashboard_path,
        "--server.port",
        str(port)
    ])

if __name__ == "__main__":
    main()

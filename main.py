#!/usr/bin/env python3
"""
Audio Compression Analysis Tool
Entry point for the Streamlit dashboard.
"""

import subprocess
import sys
import os

def main():
    """Start the Streamlit dashboard."""
    print("Starting Audio Compression Analysis...")

    # Ensure output directories exist
    os.makedirs("data/original", exist_ok=True)
    os.makedirs("output/encoded", exist_ok=True)
    os.makedirs("output/decoded", exist_ok=True)
    os.makedirs("output/reports", exist_ok=True)

    # Path to dashboard
    dashboard_path = os.path.join(os.path.dirname(__file__), "src", "dashboard.py")

    # Run Streamlit
    subprocess.run([sys.executable, "-m", "streamlit", "run", dashboard_path])

if __name__ == "__main__":
    main()

import subprocess
import sys
import os

if __name__ == "__main__":
    print("Audio Encoding Project Started")
    # Run the dashboard
    dashboard_path = os.path.join(os.path.dirname(__file__), "src", "dashboard.py")
    subprocess.run([sys.executable, "-m", "streamlit", "run", dashboard_path])
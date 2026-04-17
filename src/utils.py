import os
import tempfile

def ensure_directories(*paths):
    """Create directories if they do not exist."""
    for path in paths:
        if path and not os.path.exists(path):
            os.makedirs(path, exist_ok=True)

def save_uploaded_tempfile(uploaded_file, suffix=""):
    """Save a Streamlit uploaded file to a temporary local file."""
    suffix = suffix or os.path.splitext(uploaded_file.name)[1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_file:
        tmp_file.write(uploaded_file.read())
        return tmp_file.name

def format_bytes(byte_count):
    """Format bytes into a human-readable string."""
    units = ["bytes", "KB", "MB", "GB"]
    byte_count = float(byte_count)

    for unit in units:
        if byte_count < 1024:
            if unit == "bytes":
                return f"{int(byte_count)} {unit}"
            return f"{byte_count:.2f} {unit}"
        if unit == "GB":
            return f"{byte_count:.2f} {unit}"
        byte_count /= 1024

    return f"{byte_count:.2f} GB"

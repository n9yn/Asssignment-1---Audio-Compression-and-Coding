import os
import tempfile


def get_project_root() -> str:
    """Return the project root directory."""
    return os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))


def ensure_directories(*paths: str) -> None:
    """Create directories if they do not exist."""
    for path in paths:
        if path and not os.path.exists(path):
            os.makedirs(path, exist_ok=True)


def save_uploaded_tempfile(uploaded_file, suffix="") -> str:
    """Save a Streamlit uploaded file to a temporary local file."""
    suffix = suffix or os.path.splitext(uploaded_file.name)[1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_file:
        tmp_file.write(uploaded_file.read())
        return tmp_file.name


def format_bytes(byte_count: int) -> str:
    """Format bytes into a human-readable string."""
    for unit in ["bytes", "KB", "MB", "GB"]:
        if byte_count < 1024 or unit == "GB":
            return f"{byte_count:.2f} {unit}" if unit != "bytes" else f"{byte_count} {unit}"
        byte_count /= 1024
    return f"{byte_count:.2f} GB"


def cleanup_file(file_path: str) -> None:
    """Remove a temporary file if it exists."""
    try:
        if file_path and os.path.exists(file_path):
            os.unlink(file_path)
    except OSError:
        pass

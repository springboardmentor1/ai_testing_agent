import subprocess
import tempfile
import sys
import os

def run_playwright_test(script: str):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as f:
        f.write(script.encode())
        path = f.name

    try:
        result = subprocess.run(
            [sys.executable, path],
            capture_output=True,
            text=True
        )
        return {
            "status": "PASSED" if result.returncode == 0 else "FAILED",
            "stdout": result.stdout,
            "stderr": result.stderr
        }
    finally:
        os.remove(path)

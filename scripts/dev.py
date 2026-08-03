import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    python = ROOT / "backend" / ".venv" / "bin" / "python"
    backend_python = str(python if python.exists() else sys.executable)
    backend = subprocess.Popen([backend_python, "-m", "uvicorn", "app.main:app", "--reload"], cwd=ROOT / "backend")
    frontend = subprocess.Popen(["npm", "run", "dev"], cwd=ROOT / "frontend")
    try:
        backend.wait()
        return backend.returncode or 0
    except KeyboardInterrupt:
        return 0
    finally:
        backend.terminate()
        frontend.terminate()


if __name__ == "__main__":
    raise SystemExit(main())

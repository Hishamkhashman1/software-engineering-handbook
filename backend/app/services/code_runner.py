import ast
import json
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

from app.schemas.content import CodingChallenge

ALLOWED_IMPORT_ROOTS = {
    "collections",
    "dataclasses",
    "functools",
    "itertools",
    "math",
    "re",
    "statistics",
    "typing",
}


class UnsafeCodeError(ValueError):
    pass


def run_python_challenge(challenge: CodingChallenge, code: str) -> dict[str, Any]:
    try:
        _validate_imports(code)
    except UnsafeCodeError as exc:
        return {"passed": False, "error": str(exc), "tests": []}

    tests = challenge.visible_tests + challenge.hidden_tests
    runner = _build_runner(code, tests)
    with tempfile.TemporaryDirectory(prefix="interview-game-") as tmp:
        path = Path(tmp) / "submission_runner.py"
        path.write_text(runner, encoding="utf-8")
        try:
            completed = subprocess.run(
                [sys.executable, str(path)],
                cwd=tmp,
                capture_output=True,
                text=True,
                timeout=challenge.timeout_seconds,
                check=False,
            )
        except subprocess.TimeoutExpired:
            return {"passed": False, "timeout": True, "tests": [], "stderr": "Execution timed out"}
    if completed.returncode != 0:
        return {"passed": False, "tests": [], "stdout": completed.stdout, "stderr": completed.stderr}
    payload = json.loads(completed.stdout or "{}")
    return payload


def _validate_imports(code: str) -> None:
    tree = ast.parse(code)
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name.split(".")[0] not in ALLOWED_IMPORT_ROOTS:
                    raise UnsafeCodeError(f"Import '{alias.name}' is not allowed in the local sandbox")
        if isinstance(node, ast.ImportFrom):
            root = (node.module or "").split(".")[0]
            if root not in ALLOWED_IMPORT_ROOTS:
                raise UnsafeCodeError(f"Import '{node.module}' is not allowed in the local sandbox")


def _build_runner(code: str, tests: list[Any]) -> str:
    test_payload = json.dumps([test.model_dump() for test in tests])
    return f"""
import contextlib
import io
import json

namespace = {{}}
exec({code!r}, namespace)
tests = json.loads({test_payload!r})
results = []
for test in tests:
    try:
        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer):
            actual = eval(test["call"], namespace)
        passed = actual == test["expected"]
        results.append({{"name": test["name"], "passed": passed, "actual": actual, "expected": test["expected"], "stdout": buffer.getvalue()}})
    except Exception as exc:
        results.append({{"name": test["name"], "passed": False, "error": repr(exc), "expected": test["expected"]}})
print(json.dumps({{"passed": all(item["passed"] for item in results), "tests": results}}))
"""

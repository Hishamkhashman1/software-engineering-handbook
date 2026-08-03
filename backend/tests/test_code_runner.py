from app.schemas.content import CodingChallenge
from app.services.code_runner import run_python_challenge


def challenge() -> CodingChallenge:
    return CodingChallenge.model_validate({
        "id": "c",
        "title": "C",
        "instructions": "I",
        "starter_code": "def classify_status_code(code: int) -> str:\n    pass\n",
        "function_signature": "def classify_status_code(code: int) -> str",
        "visible_tests": [{"name": "success", "call": "classify_status_code(201)", "expected": "success"}],
        "hidden_tests": [{"name": "server", "call": "classify_status_code(503)", "expected": "server_error"}],
        "timeout_seconds": 1,
        "explanation": "E",
        "difficulty": 1,
        "tags": ["http"],
    })


def test_code_runner_passing_and_failing_cases():
    code = "def classify_status_code(code: int) -> str:\n    return 'success' if 200 <= code < 300 else 'server_error'\n"
    result = run_python_challenge(challenge(), code)
    assert result["passed"]
    bad = run_python_challenge(challenge(), "def classify_status_code(code: int) -> str:\n    return 'success'\n")
    assert not bad["passed"]


def test_code_runner_timeout():
    c = challenge()
    c.timeout_seconds = 0.1
    result = run_python_challenge(c, "def classify_status_code(code: int) -> str:\n    while True:\n        pass\n")
    assert result["timeout"]

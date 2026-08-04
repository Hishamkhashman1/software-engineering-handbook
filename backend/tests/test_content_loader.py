import json

import pytest

from app.services.content_loader import ContentError, ContentRepository


def valid_module(module_id: str = "m1") -> dict:
    questions = [
        {"id": f"{module_id}-q{i}", "type": "true_false", "prompt": f"Q{i}", "answer": True, "explanation": "Because.", "difficulty": 1, "tags": ["tag"]}
        for i in range(12)
    ]
    return {
        "id": module_id,
        "title": "Module",
        "description": "Desc",
        "order": 1,
        "tags": ["tag"],
        "lessons": [
            {"id": f"{module_id}-l{i}", "title": "Lesson", "summary": "S", "explanation": "E", "key_points": ["k"], "examples": [], "interview_questions": [], "difficulty": 1, "tags": ["tag"]}
            for i in range(4)
        ],
        "questions": questions,
        "coding_challenges": [{
            "id": f"{module_id}-c1",
            "title": "Code",
            "instructions": "Do it",
            "starter_code": "def f(): pass",
            "function_signature": "def f()",
            "visible_tests": [{"name": "t", "call": "f()", "expected": None}],
            "hidden_tests": [{"name": "h", "call": "f()", "expected": None}],
            "timeout_seconds": 1,
            "explanation": "E",
            "difficulty": 1,
            "tags": ["tag"],
        }],
        "boss_battle": {"id": f"{module_id}-boss", "title": "Boss", "question_ids": [q["id"] for q in questions[:5]], "passing_threshold": 0.7, "reward_xp": 100},
    }


def test_content_loader_validates_modules(tmp_path):
    (tmp_path / "manifest.json").write_text(json.dumps({"modules": ["m1.json"]}))
    (tmp_path / "m1.json").write_text(json.dumps(valid_module()))
    repo = ContentRepository(tmp_path)
    repo.load()
    assert repo.modules[0].id == "m1"
    assert "m1-q1" in repo.question_by_id


def test_content_loader_detects_duplicate_ids(tmp_path):
    data = valid_module()
    data["questions"][1]["id"] = data["questions"][0]["id"]
    (tmp_path / "manifest.json").write_text(json.dumps({"modules": ["m1.json"]}))
    (tmp_path / "m1.json").write_text(json.dumps(data))
    with pytest.raises(ContentError, match="Duplicate content id"):
        ContentRepository(tmp_path).load()


def test_generated_content_has_concept_panels():
    repo = ContentRepository()
    repo.load()
    questions = [question for module in repo.modules for question in module.questions]

    assert questions
    assert all(question.concept_panel for question in questions)
    assert all(len(question.concept_panel.key_takeaways) >= 3 for question in questions if question.concept_panel)
    assert all(
        question.concept_panel.interview_insight.startswith("Interviewers usually ask this concept to evaluate")
        for question in questions
        if question.concept_panel
    )

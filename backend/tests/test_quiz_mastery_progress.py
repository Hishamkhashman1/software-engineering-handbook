from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from app.database.session import Base
from app.models import TopicMastery
from app.schemas.content import Module, Question
from app.services.mastery_engine import level_for_xp, update_mastery_value, xp_for_question
from app.services.progress_service import ensure_progress, progress_snapshot, record_boss_result, record_question_attempt
from app.services.quiz_engine import grade_question, select_quiz_questions
from app.services.review_scheduler import select_weak_review


def q(**kwargs):
    base = {"id": "q1", "type": "multiple_choice", "prompt": "P", "options": ["A", "B"], "answer": "A", "explanation": "E", "difficulty": 2, "tags": ["http"]}
    base.update(kwargs)
    return Question.model_validate(base)


def test_question_grading_short_answer_partial_credit():
    question = q(type="short_answer", options=None, answer=None, accepted_answers=[], keywords=["pagination", "cursor", "stable"])
    result = grade_question(question, "Cursor pagination is stable for changing datasets")
    assert result.correct
    assert result.score >= 0.7


def test_interactive_question_grading():
    multi = q(type="multi_select", options=["GET", "PUT", "POST"], answer=["GET", "PUT"])
    assert grade_question(multi, ["PUT", "GET"]).correct
    matching = q(type="matching", options=None, pairs=[{"left": "401", "right": "Auth required"}, {"left": "503", "right": "Unavailable"}], answer={"401": "Auth required", "503": "Unavailable"})
    assert grade_question(matching, {"401": "Auth required", "503": "Unavailable"}).correct
    fill = q(type="code_fill", options=["selectinload", "sleep"], code="options(____)", answer="selectinload")
    assert grade_question(fill, "selectinload").correct


def test_quiz_selection_respects_count_and_seed():
    module = Module.model_validate({
        "id": "m",
        "title": "M",
        "description": "D",
        "order": 1,
        "tags": [],
        "lessons": [{"id": f"l{i}", "title": "L", "summary": "S", "explanation": "E", "key_points": ["k"], "examples": [], "interview_questions": [], "difficulty": 1, "tags": []} for i in range(4)],
        "questions": [q(id=f"q{i}").model_dump() for i in range(12)],
        "coding_challenges": [{"id": "c", "title": "C", "instructions": "I", "starter_code": "def f(): pass", "function_signature": "def f()", "visible_tests": [{"name": "t", "call": "f()", "expected": None}], "hidden_tests": [{"name": "h", "call": "f()", "expected": None}], "timeout_seconds": 1, "explanation": "E", "difficulty": 1, "tags": []}],
        "boss_battle": {"id": "b", "title": "B", "question_ids": [f"q{i}" for i in range(5)], "passing_threshold": 0.7, "reward_xp": 100},
    })
    selected = select_quiz_questions([module], ["m"], 5, seed=1)
    assert len(selected) == 5
    assert [item.id for item in selected] == [item.id for item in select_quiz_questions([module], ["m"], 5, seed=1)]


def test_xp_level_and_mastery_update():
    question = q(difficulty=3)
    assert xp_for_question(question, True) == 25
    assert level_for_xp(250) >= 2
    assert update_mastery_value(40, question, True, 0) > 40
    assert update_mastery_value(40, question, False, 0) < 40


def test_progress_persistence_and_review_selection():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    with Session(engine) as db:
        ensure_progress(db)
        question = q()
        result = record_question_attempt(db, "m", question, "B", 300)
        assert not result["correct"]
        snapshot = progress_snapshot(db, [])
        assert snapshot["accuracy"] == 0
        mastery = db.scalar(select(TopicMastery).where(TopicMastery.topic == "http"))
        assert mastery is not None
        mastery.mastery = 20
        db.commit()
        module = type("ModuleLike", (), {"questions": [question]})()
        assert select_weak_review(db, [module], 1)[0].id == "q1"


def test_progress_snapshot_includes_training_and_boss_status():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    with Session(engine) as db:
        module = Module.model_validate({
            "id": "m",
            "title": "M",
            "description": "D",
            "order": 1,
            "tags": [],
            "lessons": [{"id": "l1", "title": "L", "summary": "S", "explanation": "E", "key_points": ["k"], "examples": [], "interview_questions": [], "difficulty": 1, "tags": []}],
            "questions": [q(id=f"q{i}").model_dump() for i in range(4)],
            "coding_challenges": [],
            "boss_battle": {"id": "b", "title": "B", "question_ids": ["q0", "q1"], "passing_threshold": 0.7, "reward_xp": 100},
        })
        record_question_attempt(db, "m", module.questions[0], "A", 100)
        record_boss_result(db, "m", 1, True)

        snapshot = progress_snapshot(db, [module])
        module_progress = snapshot["module_progress"][0]
        assert module_progress["attempted_questions"] == 1
        assert module_progress["training_percent"] == 25
        assert module_progress["boss_completed"]
        assert module_progress["boss_score"] == 1

from math import ceil
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.api import AnswerSubmission, CodingRunRequest, InterviewSubmitRequest, LessonCompletion
from app.services.code_runner import run_python_challenge
from app.services.content_loader import content_repo
from app.services.progress_service import (
    progress_snapshot,
    record_boss_result,
    record_coding_attempt,
    record_lesson_completion,
    record_question_attempt,
    reset_progress,
)
from app.services.quiz_engine import grade_question, select_quiz_questions
from app.services.review_scheduler import select_weak_review

router = APIRouter(prefix="/api")
INTERVIEW_SESSIONS: dict[str, list[str]] = {}


@router.get("/modules")
def list_modules() -> list[dict]:
    return [
        {
            "id": module.id,
            "title": module.title,
            "description": module.description,
            "order": module.order,
            "tags": module.tags,
            "lesson_count": len(module.lessons),
            "question_count": len(module.questions),
            "challenge_count": len(module.coding_challenges),
        }
        for module in content_repo.modules
    ]


@router.get("/modules/{module_id}")
def get_module(module_id: str) -> dict:
    module = content_repo.module_by_id.get(module_id)
    if module is None:
        raise HTTPException(status_code=404, detail="Module not found")
    return module.model_dump()


@router.get("/lessons/{lesson_id}")
def get_lesson(lesson_id: str) -> dict:
    module_id = content_repo.lesson_to_module.get(lesson_id)
    if module_id is None:
        raise HTTPException(status_code=404, detail="Lesson not found")
    module = content_repo.module_by_id[module_id]
    lesson = next(item for item in module.lessons if item.id == lesson_id)
    related = [question for question in module.questions if set(question.tags) & set(lesson.tags)]
    return {"module_id": module_id, "lesson": lesson.model_dump(), "questions": [item.model_dump() for item in related[:4]]}


@router.post("/lessons/complete")
def complete_lesson(payload: LessonCompletion, db: Session = Depends(get_db)) -> dict:
    record_lesson_completion(db, payload.module_id, payload.lesson_id)
    return {"ok": True}


@router.get("/quiz")
def get_quiz(
    module_ids: str | None = None,
    count: int = Query(default=10, ge=1, le=50),
    seed: int | None = None,
) -> dict:
    selected_modules = module_ids.split(",") if module_ids else None
    questions = select_quiz_questions(content_repo.modules, selected_modules, count, seed)
    return {"questions": [_public_question(question) for question in questions]}


@router.post("/attempts")
def submit_attempt(payload: AnswerSubmission, db: Session = Depends(get_db)) -> dict:
    found = content_repo.question_by_id.get(payload.question_id)
    if found is None:
        raise HTTPException(status_code=404, detail="Question not found")
    module_id, question = found
    return record_question_attempt(db, module_id, question, payload.answer, payload.response_time_ms)


@router.get("/progress")
def get_progress(db: Session = Depends(get_db)) -> dict:
    return progress_snapshot(db, content_repo.modules)


@router.post("/progress/reset")
def reset(db: Session = Depends(get_db)) -> dict:
    reset_progress(db)
    return {"ok": True}


@router.get("/review/weak")
def weak_review(limit: int = Query(default=10, ge=1, le=30), db: Session = Depends(get_db)) -> dict:
    questions = select_weak_review(db, content_repo.modules, limit)
    return {"questions": [_public_question(question) for question in questions]}


@router.post("/coding/run")
def run_coding(payload: CodingRunRequest, db: Session = Depends(get_db)) -> dict:
    found = content_repo.challenge_by_id.get(payload.challenge_id)
    if found is None:
        raise HTTPException(status_code=404, detail="Challenge not found")
    module_id, challenge = found
    result = run_python_challenge(challenge, payload.code)
    record_coding_attempt(db, module_id, payload.challenge_id, payload.code, result)
    return result


@router.get("/interview/session")
def create_interview_session(count: int = Query(default=20, ge=5, le=60)) -> dict:
    questions = select_quiz_questions(content_repo.modules, None, count)
    session_id = str(uuid4())
    INTERVIEW_SESSIONS[session_id] = [question.id for question in questions]
    return {"session_id": session_id, "duration_seconds": count * 75, "questions": [_public_question(question) for question in questions]}


@router.post("/interview/session/{session_id}/submit")
def submit_interview(session_id: str, payload: InterviewSubmitRequest, db: Session = Depends(get_db)) -> dict:
    question_ids = INTERVIEW_SESSIONS.get(session_id)
    if question_ids is None:
        raise HTTPException(status_code=404, detail="Interview session not found")
    by_id = {answer.question_id: answer for answer in payload.answers}
    results = []
    module_scores: dict[str, dict[str, int]] = {}
    for question_id in question_ids:
        found = content_repo.question_by_id[question_id]
        module_id, question = found
        submission = by_id.get(question_id)
        grade = grade_question(question, submission.answer if submission else None)
        if submission:
            record_question_attempt(db, module_id, question, submission.answer, submission.response_time_ms)
        bucket = module_scores.setdefault(module_id, {"correct": 0, "total": 0})
        bucket["correct"] += 1 if grade.correct else 0
        bucket["total"] += 1
        results.append({"question_id": question_id, "module_id": module_id, "correct": grade.correct, "score": grade.score, "explanation": grade.explanation})
    correct = sum(1 for item in results if item["correct"])
    return {"score": correct / len(results), "results": results, "breakdown": module_scores}


@router.post("/modules/{module_id}/boss-battle/submit")
def submit_boss_battle(module_id: str, payload: InterviewSubmitRequest, db: Session = Depends(get_db)) -> dict:
    module = content_repo.module_by_id.get(module_id)
    if module is None:
        raise HTTPException(status_code=404, detail="Module not found")
    by_id = {answer.question_id: answer for answer in payload.answers}
    results = []
    for question_id, submission in by_id.items():
        if submission.answer is None:
            continue
        if question_id not in module.boss_battle.question_ids:
            continue
        question = next((item for item in module.questions if item.id == question_id), None)
        if question is None:
            continue
        grade = grade_question(question, submission.answer)
        results.append({"question_id": question.id, "correct": grade.correct, "score": grade.score, "explanation": grade.explanation})
    if not results:
        raise HTTPException(status_code=400, detail="Boss battle needs at least one answer")
    correct_count = sum(1 for item in results if item["correct"])
    required_correct = min(len(module.boss_battle.question_ids), ceil(100 / 18))
    score = min(1, correct_count / required_correct)
    passed = correct_count >= required_correct
    record_boss_result(db, module_id, score, passed)
    return {"score": score, "passed": passed, "results": results}


def _public_question(question) -> dict:
    data = question.model_dump()
    data.pop("answer", None)
    data.pop("accepted_answers", None)
    data.pop("keywords", None)
    return data

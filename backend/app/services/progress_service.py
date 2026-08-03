import json
from datetime import datetime
from typing import Any

from sqlalchemy import delete, func, select
from sqlalchemy.orm import Session

from app.models import (
    BossBattleResult,
    CodingAttempt,
    CompletedLesson,
    ModuleCompletion,
    QuestionAttempt,
    TopicMastery,
    UserProgress,
)
from app.schemas.content import Module, Question
from app.services.mastery_engine import level_for_xp, next_review_after, update_mastery_value, xp_for_question
from app.services.quiz_engine import grade_question


def ensure_progress(db: Session) -> UserProgress:
    progress = db.get(UserProgress, 1)
    if progress is None:
        progress = UserProgress(id=1)
        db.add(progress)
        db.commit()
        db.refresh(progress)
    return progress


def record_lesson_completion(db: Session, module_id: str, lesson_id: str) -> None:
    ensure_progress(db)
    exists = db.scalar(select(CompletedLesson).where(CompletedLesson.lesson_id == lesson_id))
    if exists is None:
        db.add(CompletedLesson(module_id=module_id, lesson_id=lesson_id))
        db.commit()


def record_question_attempt(db: Session, module_id: str, question: Question, answer: Any, response_time_ms: int) -> dict[str, Any]:
    progress = ensure_progress(db)
    grade = grade_question(question, answer)
    db.add(
        QuestionAttempt(
            module_id=module_id,
            question_id=question.id,
            question_type=question.type,
            answer_json=json.dumps(answer),
            correct=grade.correct,
            score=grade.score,
            response_time_ms=response_time_ms,
        )
    )
    awarded_xp = xp_for_question(question, True) if grade.correct else 4
    if grade.correct:
        progress.correct_answers += 1
        progress.current_streak += 1
        progress.best_streak = max(progress.best_streak, progress.current_streak)
    else:
        progress.incorrect_answers += 1
        progress.current_streak = 0
    progress.total_xp += awarded_xp
    progress.total_response_time_ms += response_time_ms
    progress.updated_at = datetime.utcnow()

    for tag in question.tags:
        mastery = db.scalar(select(TopicMastery).where(TopicMastery.topic == tag))
        if mastery is None:
            mastery = TopicMastery(topic=tag, module_id=module_id)
            db.add(mastery)
            db.flush()
        mastery.mastery = update_mastery_value(mastery.mastery, question, grade.correct, mastery.success_count)
        mastery.success_count = mastery.success_count + 1 if grade.correct else 0
        mastery.interval_days, mastery.next_review = next_review_after(grade.correct, mastery.interval_days, mastery.success_count)
        mastery.last_reviewed = datetime.utcnow()
    db.commit()
    return {
        "correct": grade.correct,
        "score": grade.score,
        "explanation": grade.explanation,
        "expected": grade.expected,
        "xp_awarded": awarded_xp,
    }


def record_coding_attempt(db: Session, module_id: str, challenge_id: str, code: str, result: dict[str, Any]) -> None:
    progress = ensure_progress(db)
    passed = bool(result.get("passed"))
    db.add(CodingAttempt(module_id=module_id, challenge_id=challenge_id, code=code, passed=passed, results_json=json.dumps(result)))
    if passed:
        progress.total_xp += 50
    progress.updated_at = datetime.utcnow()
    db.commit()


def record_boss_result(db: Session, module_id: str, score: float, passed: bool) -> None:
    progress = ensure_progress(db)
    db.add(BossBattleResult(module_id=module_id, score=score, passed=passed))
    if passed:
        progress.total_xp += 100
        existing = db.scalar(select(ModuleCompletion).where(ModuleCompletion.module_id == module_id))
        if existing is None:
            db.add(ModuleCompletion(module_id=module_id, badge_awarded=True))
    db.commit()


def progress_snapshot(db: Session, modules: list[Module]) -> dict[str, Any]:
    progress = ensure_progress(db)
    total = progress.correct_answers + progress.incorrect_answers
    lesson_rows = db.scalars(select(CompletedLesson)).all()
    completed_lessons = {row.lesson_id for row in lesson_rows}
    completions = {row.module_id for row in db.scalars(select(ModuleCompletion)).all()}
    mastery = db.scalars(select(TopicMastery).order_by(TopicMastery.mastery.asc())).all()
    attempts = db.scalars(select(QuestionAttempt).order_by(QuestionAttempt.created_at.desc()).limit(8)).all()
    due_count = db.scalar(select(func.count()).select_from(TopicMastery).where(TopicMastery.next_review <= datetime.utcnow())) or 0
    return {
        "total_xp": progress.total_xp,
        "level": level_for_xp(progress.total_xp),
        "current_streak": progress.current_streak,
        "best_streak": progress.best_streak,
        "accuracy": round(progress.correct_answers / total, 3) if total else 0,
        "average_response_time_ms": round(progress.total_response_time_ms / total) if total else 0,
        "completed_lessons": list(completed_lessons),
        "completed_modules": list(completions),
        "module_progress": [
            {
                "module_id": module.id,
                "title": module.title,
                "completed_lessons": sum(1 for lesson in module.lessons if lesson.id in completed_lessons),
                "total_lessons": len(module.lessons),
                "completed": module.id in completions,
            }
            for module in modules
        ],
        "weakest_topics": [{"topic": row.topic, "mastery": round(row.mastery, 1), "module_id": row.module_id} for row in mastery[:8]],
        "due_reviews": due_count,
        "recent_activity": [
            {"question_id": row.question_id, "module_id": row.module_id, "correct": row.correct, "score": row.score}
            for row in attempts
        ],
    }


def reset_progress(db: Session) -> None:
    for model in [BossBattleResult, CodingAttempt, CompletedLesson, ModuleCompletion, QuestionAttempt, TopicMastery, UserProgress]:
        db.execute(delete(model))
    db.commit()

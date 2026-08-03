from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import QuestionAttempt, TopicMastery
from app.schemas.content import Module, Question


def select_weak_review(db: Session, modules: list[Module], limit: int = 10) -> list[Question]:
    now = datetime.utcnow()
    incorrect_ids = [
        row.question_id
        for row in db.scalars(
            select(QuestionAttempt)
            .where(QuestionAttempt.correct.is_(False))
            .order_by(QuestionAttempt.created_at.desc())
            .limit(30)
        )
    ]
    weak_topics = [
        row.topic
        for row in db.scalars(
            select(TopicMastery)
            .where((TopicMastery.mastery < 55) | (TopicMastery.next_review <= now))
            .order_by(TopicMastery.mastery.asc())
            .limit(20)
        )
    ]
    all_questions = [question for module in modules for question in module.questions]
    selected: list[Question] = []
    for qid in incorrect_ids:
        match = next((question for question in all_questions if question.id == qid), None)
        if match and match not in selected:
            selected.append(match)
    for topic in weak_topics:
        for question in all_questions:
            if topic in question.tags and question not in selected:
                selected.append(question)
                break
    for question in all_questions:
        if question not in selected:
            selected.append(question)
        if len(selected) >= limit:
            break
    return selected[:limit]

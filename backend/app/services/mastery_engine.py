from datetime import datetime, timedelta

from app.schemas.content import Question


def xp_for_question(question: Question, correct: bool) -> int:
    if not correct:
        return 0
    return {1: 10, 2: 15, 3: 25}[question.difficulty]


def level_for_xp(xp: int) -> int:
    level = 1
    threshold = 100
    remaining = xp
    while remaining >= threshold:
        level += 1
        remaining -= threshold
        threshold += 50
    return level


def update_mastery_value(current: float, question: Question, correct: bool, success_count: int) -> float:
    weight = {1: 5.0, 2: 7.5, 3: 11.0}[question.difficulty]
    if correct:
        dampener = max(0.35, 1.0 - (success_count * 0.15))
        return min(100.0, current + weight * dampener)
    return max(0.0, current - weight * 0.9)


def next_review_after(correct: bool, interval_days: int, success_count: int) -> tuple[int, datetime]:
    if not correct:
        return 1, datetime.utcnow() + timedelta(days=1)
    new_interval = min(30, max(1, interval_days) * (2 if success_count > 0 else 1))
    return new_interval, datetime.utcnow() + timedelta(days=new_interval)

import random
from dataclasses import dataclass
from typing import Any

from app.schemas.content import Module, Question


@dataclass(frozen=True)
class GradeResult:
    correct: bool
    score: float
    explanation: str
    expected: Any


def grade_question(question: Question, answer: Any) -> GradeResult:
    score = 0.0
    if question.type in {"multiple_choice", "true_false", "code_output", "bug_hunt", "scenario_choice", "code_fill"}:
        score = 1.0 if answer == question.answer else 0.0
    elif question.type == "multi_select":
        expected = set(question.answer or [])
        supplied = set(answer or [])
        score = 1.0 if supplied == expected else max(0.0, len(expected & supplied) / max(1, len(expected)) - len(supplied - expected) * 0.25)
    elif question.type == "matching":
        expected = dict(question.answer or {})
        supplied = dict(answer or {})
        hits = sum(1 for key, value in expected.items() if supplied.get(key) == value)
        score = hits / max(1, len(expected))
    elif question.type == "ordering":
        score = 1.0 if list(answer or []) == list(question.answer or []) else 0.0
    elif question.type == "short_answer":
        text = _norm(str(answer), question.case_insensitive)
        accepted = [_norm(value, question.case_insensitive) for value in question.accepted_answers]
        if text in accepted:
            score = 1.0
        elif question.keywords:
            hits = sum(1 for keyword in question.keywords if _norm(keyword, question.case_insensitive) in text)
            score = min(1.0, hits / max(2, len(question.keywords)))
    elif question.type in {"scenario", "debugging"}:
        text = _norm(str(answer), True)
        hits = sum(1 for keyword in question.keywords if _norm(keyword, True) in text)
        score = min(1.0, hits / max(2, len(question.keywords)))
    return GradeResult(score >= 0.7, round(score, 2), question.explanation, question.answer)


def select_quiz_questions(
    modules: list[Module],
    module_ids: list[str] | None,
    count: int,
    seed: int | None = None,
) -> list[Question]:
    pool = [
        question
        for module in modules
        if not module_ids or module.id in module_ids
        for question in module.questions
    ]
    rng = random.Random(seed)
    rng.shuffle(pool)
    return pool[: max(1, min(count, len(pool)))]


def _norm(value: str, case_insensitive: bool) -> str:
    value = " ".join(value.strip().split())
    return value.lower() if case_insensitive else value

from typing import Any

from pydantic import BaseModel, Field


class AnswerSubmission(BaseModel):
    module_id: str
    question_id: str
    answer: Any
    response_time_ms: int = Field(default=0, ge=0)


class LessonCompletion(BaseModel):
    module_id: str
    lesson_id: str


class CodingRunRequest(BaseModel):
    module_id: str | None = None
    challenge_id: str
    code: str


class InterviewSubmitRequest(BaseModel):
    answers: list[AnswerSubmission]

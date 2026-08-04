from typing import Any, Literal

from pydantic import BaseModel, Field, model_validator

QuestionType = Literal[
    "multiple_choice",
    "true_false",
    "short_answer",
    "ordering",
    "scenario",
    "code_output",
    "debugging",
    "multi_select",
    "matching",
    "code_fill",
    "bug_hunt",
    "scenario_choice",
]


class Lesson(BaseModel):
    id: str
    title: str
    summary: str
    explanation: str
    key_points: list[str] = Field(min_length=1)
    examples: list[str] = Field(default_factory=list)
    interview_questions: list[str] = Field(default_factory=list)
    difficulty: int = Field(ge=1, le=3)
    tags: list[str] = Field(default_factory=list)


class DiagramSpec(BaseModel):
    type: Literal["flow", "compare", "network", "triangle", "tree"]
    title: str | None = None
    nodes: list[dict[str, Any]] = Field(default_factory=list)
    edges: list[dict[str, Any]] = Field(default_factory=list)
    columns: list[dict[str, Any]] = Field(default_factory=list)
    points: list[dict[str, Any]] = Field(default_factory=list)


class ConceptPanel(BaseModel):
    title: str
    explanation: str
    key_takeaways: list[str] = Field(min_length=3, max_length=5)
    interview_insight: str
    practical_example: str
    diagram: DiagramSpec | None = None

    @model_validator(mode="after")
    def validate_interview_insight(self) -> "ConceptPanel":
        if not self.interview_insight.startswith("Interviewers usually ask this concept to evaluate"):
            raise ValueError("concept_panel.interview_insight must start with 'Interviewers usually ask this concept to evaluate'")
        return self


class Question(BaseModel):
    id: str
    type: QuestionType
    prompt: str
    options: list[str] | None = None
    pairs: list[dict[str, str]] | None = None
    code: str | None = None
    answer: Any | None = None
    accepted_answers: list[str] = Field(default_factory=list)
    keywords: list[str] = Field(default_factory=list)
    case_insensitive: bool = True
    explanation: str
    difficulty: int = Field(ge=1, le=3)
    tags: list[str] = Field(default_factory=list)
    concept_panel: ConceptPanel | None = None

    @model_validator(mode="after")
    def validate_answer_shape(self) -> "Question":
        if self.type in {"multiple_choice", "code_output", "bug_hunt", "scenario_choice"} and (not self.options or self.answer not in self.options):
            raise ValueError(f"{self.type} questions require options containing answer")
        if self.type == "multi_select" and (not self.options or not isinstance(self.answer, list)):
            raise ValueError("multi_select questions require options and a list answer")
        if self.type == "matching" and (not self.pairs or not isinstance(self.answer, dict)):
            raise ValueError("matching questions require pairs and a dict answer")
        if self.type == "code_fill" and (not self.options or self.answer not in self.options or not self.code):
            raise ValueError("code_fill questions require code, options, and answer")
        if self.type == "true_false" and not isinstance(self.answer, bool):
            raise ValueError("true_false questions require a boolean answer")
        if self.type == "ordering" and not isinstance(self.answer, list):
            raise ValueError("ordering questions require a list answer")
        if self.type == "short_answer" and not (self.accepted_answers or self.keywords):
            raise ValueError("short_answer questions require accepted_answers or keywords")
        if self.type in {"scenario", "debugging"} and not self.keywords:
            raise ValueError("scenario/debugging questions require keywords for deterministic grading")
        return self


class CodingTest(BaseModel):
    name: str
    call: str
    expected: Any


class CodingChallenge(BaseModel):
    id: str
    title: str
    instructions: str
    starter_code: str
    function_signature: str
    visible_tests: list[CodingTest] = Field(min_length=1)
    hidden_tests: list[CodingTest] = Field(min_length=1)
    timeout_seconds: float = Field(default=2.0, gt=0, le=5)
    explanation: str
    difficulty: int = Field(ge=1, le=3)
    tags: list[str] = Field(default_factory=list)


class BossBattle(BaseModel):
    id: str
    title: str
    question_ids: list[str] = Field(min_length=5)
    passing_threshold: float = Field(ge=0, le=1)
    reward_xp: int = Field(default=100, ge=0)


class Module(BaseModel):
    id: str
    title: str
    description: str
    order: int
    tags: list[str] = Field(default_factory=list)
    lessons: list[Lesson] = Field(min_length=4)
    questions: list[Question] = Field(min_length=12)
    coding_challenges: list[CodingChallenge] = Field(min_length=1)
    boss_battle: BossBattle

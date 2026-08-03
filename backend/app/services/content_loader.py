import json
from pathlib import Path

from pydantic import ValidationError

from app.schemas.content import CodingChallenge, Module, Question

ROOT_DIR = Path(__file__).resolve().parents[3]
CONTENT_DIR = ROOT_DIR / "content"


class ContentError(RuntimeError):
    pass


class ContentRepository:
    def __init__(self, content_dir: Path = CONTENT_DIR) -> None:
        self.content_dir = content_dir
        self.modules: list[Module] = []
        self.module_by_id: dict[str, Module] = {}
        self.question_by_id: dict[str, tuple[str, Question]] = {}
        self.lesson_to_module: dict[str, str] = {}
        self.challenge_by_id: dict[str, tuple[str, CodingChallenge]] = {}

    def load(self) -> None:
        manifest_path = self.content_dir / "manifest.json"
        if not manifest_path.exists():
            raise ContentError(f"Missing content manifest: {manifest_path}")
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        files = manifest.get("modules")
        if not isinstance(files, list) or not files:
            raise ContentError("content/manifest.json must contain a non-empty modules list")

        modules: list[Module] = []
        seen: dict[str, str] = {}
        for file_name in files:
            path = self.content_dir / file_name
            try:
                raw = json.loads(path.read_text(encoding="utf-8"))
                module = Module.model_validate(raw)
            except FileNotFoundError as exc:
                raise ContentError(f"Missing content file: {path}") from exc
            except json.JSONDecodeError as exc:
                raise ContentError(f"Invalid JSON in {path}: {exc}") from exc
            except ValidationError as exc:
                raise ContentError(f"Invalid content in {path}: {exc}") from exc

            self._remember_id(seen, module.id, str(path))
            for lesson in module.lessons:
                self._remember_id(seen, lesson.id, str(path))
            for question in module.questions:
                self._remember_id(seen, question.id, str(path))
            for challenge in module.coding_challenges:
                self._remember_id(seen, challenge.id, str(path))
            self._remember_id(seen, module.boss_battle.id, str(path))

            question_ids = {question.id for question in module.questions}
            missing = [qid for qid in module.boss_battle.question_ids if qid not in question_ids]
            if missing:
                raise ContentError(f"{path}: boss battle references unknown questions {missing}")
            modules.append(module)

        self.modules = sorted(modules, key=lambda item: item.order)
        self.module_by_id = {module.id: module for module in self.modules}
        self.question_by_id = {
            question.id: (module.id, question)
            for module in self.modules
            for question in module.questions
        }
        self.lesson_to_module = {
            lesson.id: module.id for module in self.modules for lesson in module.lessons
        }
        self.challenge_by_id = {
            challenge.id: (module.id, challenge)
            for module in self.modules
            for challenge in module.coding_challenges
        }

    def _remember_id(self, seen: dict[str, str], item_id: str, source: str) -> None:
        if item_id in seen:
            raise ContentError(f"Duplicate content id '{item_id}' in {source}; first seen in {seen[item_id]}")
        seen[item_id] = source


content_repo = ContentRepository()

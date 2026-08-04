Interview Game
==============

A fully local interview-preparation learning game for software-engineering topics. It turns JSON learning material into modules, lessons, quizzes, spaced review, interview practice, coding challenges, and persistent progress.

Features
--------

- Data-driven modules loaded from `content/*.json`
- Strict startup validation with duplicate ID detection
- 34 seed modules, including advanced DDIA-style data systems, EPAM interview, Forecast Alpha defense, and portfolio assistant LLM tracks
- Per-question concept panels with explanations, interview insight, practical examples, and renderable diagram specs
- Learn mode with lessons, examples, quick questions, and mastery updates
- Quick quiz, weak-topic review, timed interview mode, coding lab, and module boss battles
- SQLite progress tracking for XP, levels, streaks, accuracy, lesson completion, mastery, attempts, coding runs, and badges
- Local Python coding runner with temp directories, subprocess timeout, stdout/stderr capture, and basic import restrictions
- Dark, responsive React interface
- No auth, telemetry, cloud database, paid services, or external AI APIs

Architecture
------------

- `backend/`: FastAPI, Pydantic, SQLAlchemy, SQLite, pytest
- `frontend/`: React, TypeScript, Vite, Vitest
- `content/`: editable JSON content modules plus `manifest.json`
- `data/interview_game.db`: local SQLite progress database
- `scripts/dev.py`: root command to start backend and frontend together

Requirements
------------

- Linux
- Python 3.12+
- Node.js 20+
- npm

Setup
-----

Backend:

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Frontend:

```bash
cd frontend
npm install
npm run dev
```

Root convenience command after installing backend and frontend dependencies:

```bash
npm run dev
```

The frontend runs at `http://localhost:5173`. The API runs at `http://127.0.0.1:8000`.

Content Files
-------------

`content/manifest.json` lists module files in load order. Each module file contains:

- `id`, `title`, `description`, `order`, `tags`
- at least 4 `lessons`
- at least 12 `questions`
- at least 1 `coding_challenges` entry
- 1 `boss_battle`

Learning content is not hardcoded in React components or route handlers. To add a module, create a new JSON file matching the existing schema and add the file name to `content/manifest.json`.

Questions support:

- `multiple_choice`
- `true_false`
- `short_answer`
- `ordering`
- `scenario`
- `code_output`
- `debugging`

Each question can also include `concept_panel`. The panel is shown beside the question on desktop and below it on mobile. It teaches the concept needed to reason about the question without revealing the answer directly.

`concept_panel` fields:

- `title`
- `explanation`
- `key_takeaways`
- `interview_insight`
- `practical_example`
- optional `diagram`

Diagrams are structured JSON specs rendered by the frontend. Current diagram types are `flow`, `compare`, `network`, `triangle`, and `tree`.

Short answers, scenarios, and debugging questions are graded deterministically using accepted answers and/or required keywords. No LLM is used.

Coding Challenges
-----------------

Coding challenges include starter code, a function signature, visible tests, hidden tests, timeout, explanation, difficulty, and tags. The first runner supports Python only.

Security limitation: the code runner is a local learning sandbox for a single trusted user. It runs submissions in a temporary directory, avoids `shell=True`, applies a timeout, captures output, deletes temporary files, and blocks imports outside a small allowlist. It is not a hardened multi-user security boundary.

Testing
-------

Backend:

```bash
cd backend
pytest
```

Frontend:

```bash
cd frontend
npm test
npm run lint
npm run build
```

Future Extensions
-----------------

- Add JavaScript coding challenges
- Add per-question review history in the UI
- Add import/export progress snapshots
- Add richer module-specific coding challenges
- Add keyboard shortcuts and configurable interview timing
- Add deeper per-chapter DDIA boss battles with custom diagrams and simulations

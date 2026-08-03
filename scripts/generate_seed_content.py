import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "content"

MODULES = [
    ("web-fundamentals", "Web Fundamentals", "HTTP, HTTPS, DNS, clients, servers, status codes, headers, cookies, sessions, and CORS.", ["http", "https", "dns", "cors"], [
        ("http-lifecycle", "HTTP Request Lifecycle", "HTTP carries requests from clients to servers and responses back.", ["request", "response", "headers", "body"], "GET /users?page=2 returns a status code, headers, and JSON body."),
        ("secure-web", "HTTPS and DNS", "DNS resolves names to IP addresses; HTTPS adds TLS encryption, authentication, and integrity.", ["dns", "tls", "encryption"], "A browser resolves api.example.com, opens TLS, then sends HTTP over the encrypted channel."),
        ("methods-status", "Methods and Status Codes", "Methods express intent; status codes explain the outcome.", ["GET is safe", "POST creates", "PUT replaces", "PATCH partially updates", "401 differs from 403"], "PATCH /users/5 with an email field updates only that field."),
        ("browser-state", "Browser State and CORS", "Cookies store browser data; server sessions store user data linked by a cookie. CORS controls cross-origin browser access.", ["cookies", "sessions", "origins", "preflight"], "A React app on localhost:5173 needs the API on localhost:8000 to allow that origin."),
    ]),
    ("apis", "APIs", "REST, gRPC, contracts, OpenAPI, CRUD, serialization, versioning, pagination, filtering, sorting, and idempotency.", ["rest", "grpc", "pagination", "idempotency"], [
        ("rest-contracts", "REST and API Contracts", "REST exposes resources through URLs and standard HTTP methods; contracts let teams work independently.", ["resources", "contract", "status codes"], "GET /users and POST /users describe resource actions clearly."),
        ("openapi-crud", "OpenAPI, Swagger, and CRUD", "OpenAPI specifies endpoints; Swagger is an interactive UI. CRUD maps to POST, GET, PUT/PATCH, and DELETE.", ["openapi", "swagger", "crud"], "FastAPI exposes Swagger at /docs from its OpenAPI schema."),
        ("data-shaping", "Serialization and Versioning", "Serialization converts objects to JSON; deserialization converts JSON to objects. Versioning protects existing clients.", ["serialization", "deserialization", "versioning"], "/v2/users can introduce a breaking response shape without breaking /v1/users."),
        ("pagination-idempotency", "Pagination and Idempotency", "Offset is simple; cursor is stable for large changing datasets. Idempotency makes retries safer.", ["offset", "cursor", "retry"], "Retrying DELETE /users/5 is safe; retrying POST /users may duplicate data."),
    ]),
    ("backend", "Backend", "FastAPI, Flask, routers, middleware, dependency injection, request lifecycle, lifespan, background tasks, validation, response models, async, concurrency, and parallelism.", ["fastapi", "middleware", "async", "validation"], [
        ("frameworks", "Backend Frameworks", "FastAPI emphasizes type hints, Pydantic validation, OpenAPI, and async support; Flask is lighter.", ["fastapi", "flask", "openapi"], "A typed FastAPI endpoint documents and validates request bodies automatically."),
        ("request-flow", "Routers, Middleware, and DI", "Routers organize endpoints; middleware wraps requests; dependency injection supplies shared objects.", ["routers", "middleware", "dependency injection"], "A database session dependency can be replaced in tests."),
        ("lifecycle-validation", "Lifespan, Validation, and Responses", "Startup initializes shared resources; validation rejects bad input; response models prevent leaking fields.", ["lifespan", "validation", "response model"], "A password hash should not appear in a response model."),
        ("async-model", "Async, Concurrency, and Parallelism", "Async helps while waiting on I/O; parallelism helps CPU-heavy work.", ["async", "concurrency", "parallelism"], "Awaiting a database call lets other requests progress on the event loop."),
    ]),
    ("databases", "Databases", "SQL vs NoSQL, SQL, ORMs, keys, relationships, joins, indexes, transactions, ACID, normalization, replicas, sharding, and consistency.", ["sql", "nosql", "indexes", "transactions"], [
        ("sql-nosql", "Relational and NoSQL Databases", "SQL fits structured relational data; NoSQL fits flexible schemas, caching, and document workloads.", ["sql", "nosql", "relationships"], "Orders referencing users are naturally relational."),
        ("keys-joins", "Keys, Relationships, and JOINs", "Primary keys identify rows; foreign keys connect tables; JOINs combine related data.", ["primary key", "foreign key", "join"], "orders.user_id references users.id."),
        ("indexes-transactions", "Indexes and Transactions", "Indexes speed reads at write cost; transactions keep multi-step changes consistent.", ["index", "transaction", "acid"], "A money transfer should commit debit and credit together."),
        ("scale-consistency", "Replication, Sharding, and Consistency", "Read replicas copy data for reads; sharding splits data; eventual consistency accepts temporary staleness.", ["replica", "sharding", "consistency"], "A social feed can tolerate a short delay before a new like appears."),
    ]),
    ("sqlalchemy", "SQLAlchemy Deep Dive", "Models, sessions, queries, relationships, loading strategies, migrations, transactions, raw SQL, and N+1 problems.", ["sqlalchemy", "session", "orm", "n+1"], [
        ("models-sessions", "Models and Sessions", "Models map classes to tables; sessions track and persist unit-of-work changes.", ["model", "session", "unit of work"], "session.add(user); session.commit() persists a new row."),
        ("queries-relationships", "Queries and Relationships", "ORM queries fetch mapped objects; relationships express one-to-many and many-to-many links.", ["query", "relationship", "foreign key"], "User.orders can represent a one-to-many relationship."),
        ("loading-nplus1", "Loading Strategies and N+1", "Lazy loading inside loops can trigger N+1 queries; eager loading fetches related rows earlier.", ["lazy loading", "selectinload", "joinedload", "n+1"], "Loading 100 users then accessing orders can execute 101 queries."),
        ("migrations-transactions", "Migrations, Transactions, and Raw SQL", "Migrations evolve schema; transactions protect consistency; raw SQL remains useful for complex queries.", ["migration", "transaction", "raw sql"], "Alembic records schema changes in migration files."),
    ]),
    ("testing", "Quality and Testing", "Unit, integration, end-to-end, pytest, fixtures, mocking, test doubles, TDD, CI, coverage, and regression testing.", ["testing", "pytest", "fixtures", "ci"], [
        ("test-levels", "Testing Levels", "Unit tests isolate small logic; integration tests verify boundaries; end-to-end tests exercise workflows.", ["unit", "integration", "e2e"], "A progress formula can be unit-tested without an HTTP server."),
        ("pytest-fixtures", "Pytest and Fixtures", "Fixtures provide reusable setup and teardown for tests.", ["pytest", "fixture", "setup"], "A temporary SQLite database fixture keeps tests isolated."),
        ("mocks-coverage", "Mocks, Coverage, and Regression", "Mocks replace slow boundaries; coverage highlights untested code; regression tests preserve fixed bugs.", ["mocking", "coverage", "regression"], "Mock an email sender but test the request validation for real."),
        ("ci-quality", "CI and Quality Gates", "CI runs tests automatically so broken changes are caught before merging.", ["ci", "lint", "type check"], "A pull request should run backend and frontend tests."),
    ]),
    ("performance", "Performance and Reliability", "Latency, throughput, caching, rate limiting, retries, timeouts, circuit breakers, queues, observability, and graceful degradation.", ["performance", "reliability", "cache", "retry"], [
        ("latency-throughput", "Latency and Throughput", "Latency is time per request; throughput is completed work per time period.", ["latency", "throughput"], "A service may handle high throughput while one slow endpoint has bad latency."),
        ("caching-limits", "Caching and Rate Limiting", "Caches reduce repeated work; rate limits protect shared resources.", ["cache", "rate limit"], "Cache reference data but invalidate it when it changes."),
        ("timeouts-retries", "Timeouts, Retries, and Circuit Breakers", "Timeouts bound waiting; retries need backoff; circuit breakers stop repeated failing calls.", ["timeout", "retry", "backoff", "circuit breaker"], "Unlimited retries can amplify an outage."),
        ("observability-degrade", "Observability and Degradation", "Logs, metrics, and traces explain behavior; graceful degradation preserves core features during failures.", ["logs", "metrics", "traces"], "If recommendations fail, still return the product page."),
    ]),
    ("devops", "Docker, DevOps and CI/CD", "Containers, images, Dockerfiles, Compose, environment variables, CI/CD, deployment, logs, rollbacks, and infrastructure trade-offs.", ["docker", "ci", "deployment", "env"], [
        ("containers", "Containers and Images", "Images package app dependencies; containers run image instances.", ["image", "container", "dockerfile"], "A Dockerfile describes how to build a repeatable runtime image."),
        ("compose-env", "Compose and Environment", "Compose runs multiple local services; environment variables keep configuration out of code.", ["compose", "environment variable"], "DATABASE_URL should vary by environment."),
        ("cicd", "CI/CD Pipelines", "CI validates changes; CD deploys validated builds.", ["ci", "cd", "pipeline"], "Run tests before publishing an artifact."),
        ("operations", "Logs, Rollbacks, and Deployment Safety", "Good deployments are observable and reversible.", ["logs", "rollback", "health check"], "A failed health check should stop a rollout."),
    ]),
    ("ai-integration", "AI Integration", "Embeddings, vector search, RAG, prompts, latency, evaluation, hallucination risk, privacy, and cost controls without relying on external APIs here.", ["ai", "rag", "embeddings", "evaluation"], [
        ("ai-basics", "AI Integration Concepts", "AI features combine models with product workflows, data handling, and evaluation.", ["model", "workflow", "evaluation"], "A support assistant needs retrieval and guardrails, not just a prompt."),
        ("rag-embeddings", "Embeddings and RAG", "Embeddings support similarity search; RAG retrieves source context before generation.", ["embedding", "vector search", "rag"], "Retrieve policy docs before answering policy questions."),
        ("risk-quality", "Quality, Hallucinations, and Privacy", "AI output needs evaluation, privacy controls, and fallback behavior.", ["hallucination", "privacy", "eval"], "Do not send sensitive data to a model without a clear policy."),
        ("latency-cost", "Latency, Cost, and Quantization", "AI systems trade quality, latency, memory, and cost. Quantization reduces size but may reduce accuracy.", ["latency", "cost", "quantization"], "A smaller model can be faster but less capable."),
    ]),
    ("system-design", "System Design", "Requirements, APIs, data modeling, scalability, caching, queues, consistency, availability, bottlenecks, and trade-offs.", ["system design", "scalability", "queues", "trade-off"], [
        ("requirements", "Requirements and Scope", "Good design starts with functional and non-functional requirements.", ["requirements", "scope", "sla"], "Define read/write volume before choosing storage."),
        ("api-data", "API and Data Design", "APIs and schemas should match access patterns and consistency needs.", ["api", "data model", "access pattern"], "A feed design depends on how posts are read and written."),
        ("scale-patterns", "Scaling Patterns", "Caching, read replicas, queues, and partitioning address different bottlenecks.", ["cache", "replica", "queue", "partition"], "A queue smooths bursts but adds async processing delay."),
        ("tradeoffs", "Trade-offs and Failure Modes", "Every design choice trades consistency, latency, complexity, cost, or availability.", ["trade-off", "availability", "consistency"], "Strong consistency may reduce availability during partitions."),
    ]),
]

QUESTION_PATTERNS = [
    {"type": "scenario_choice", "prompt": "A profile endpoint receives only a new email field. What should the API prefer?", "options": ["PATCH the selected field", "PUT an empty profile", "GET with a body", "DELETE and recreate"], "answer": "PATCH the selected field", "tags": ["partial update", "api"]},
    {"type": "multi_select", "prompt": "Pick the operations that are usually safe to retry.", "options": ["GET /users", "DELETE /users/5", "PUT /users/5", "POST /users"], "answer": ["GET /users", "DELETE /users/5", "PUT /users/5"], "tags": ["idempotency", "retry"]},
    {"type": "ordering", "prompt": "Arrange the request path.", "options": ["Client sends request", "Server validates input", "Business logic runs", "Response is returned"], "answer": ["Client sends request", "Server validates input", "Business logic runs", "Response is returned"], "tags": ["request", "validation"]},
    {"type": "matching", "prompt": "Match each signal to its meaning.", "pairs": [{"left": "401", "right": "Authentication required"}, {"left": "403", "right": "Authenticated but forbidden"}, {"left": "503", "right": "Service unavailable"}], "answer": {"401": "Authentication required", "403": "Authenticated but forbidden", "503": "Service unavailable"}, "tags": ["status code", "http"]},
    {"type": "code_fill", "prompt": "Fill the branch that classifies server errors.", "code": "def classify(code):\n    if 500 <= code < 600:\n        return ____", "options": ["\"server_error\"", "\"client_error\"", "\"success\"", "\"redirect\""], "answer": "\"server_error\"", "tags": ["code", "status code"]},
    {"type": "bug_hunt", "prompt": "Production duplicated records after a timeout. What is the bug?", "options": ["Retrying POST without an idempotency key", "Using HTTPS", "Returning 201 after create", "Sorting by created_at"], "answer": "Retrying POST without an idempotency key", "tags": ["duplicate", "retry"]},
    {"type": "code_output", "prompt": "What does classify_status_code(404) return?", "options": ["client_error", "server_error", "success", "unknown"], "answer": "client_error", "tags": ["code output", "status code"]},
    {"type": "scenario_choice", "prompt": "A changing feed skips items with page numbers. What pagination style fits better?", "options": ["Cursor pagination", "Offset pagination", "Return everything", "Sort in the browser"], "answer": "Cursor pagination", "tags": ["pagination", "cursor"]},
    {"type": "multiple_choice", "prompt": "Which change best preserves existing clients when a response shape breaks compatibility?", "options": ["Add /v2", "Silently change /v1", "Remove old fields", "Document it after deploy"], "answer": "Add /v2", "tags": ["versioning", "contract"]},
    {"type": "multi_select", "prompt": "Select the reasons to validate input before business logic.", "options": ["Reject invalid data early", "Improve predictable errors", "Reduce security risk", "Make CPU work parallel"], "answer": ["Reject invalid data early", "Improve predictable errors", "Reduce security risk"], "tags": ["validation", "security"]},
    {"type": "matching", "prompt": "Match the scaling tool to the bottleneck.", "pairs": [{"left": "Cache", "right": "Repeated reads"}, {"left": "Queue", "right": "Bursty writes"}, {"left": "Read replica", "right": "Read-heavy database load"}], "answer": {"Cache": "Repeated reads", "Queue": "Bursty writes", "Read replica": "Read-heavy database load"}, "tags": ["performance", "scaling"]},
    {"type": "bug_hunt", "prompt": "An endpoint loads 100 users, then reads user.orders in a loop. What is happening?", "options": ["N+1 queries", "A CORS preflight", "A DNS failure", "A cache hit"], "answer": "N+1 queries", "tags": ["n+1", "sqlalchemy"]},
    {"type": "multi_select", "prompt": "Pick two fixes for the N+1 query pattern.", "options": ["selectinload", "joinedload", "Unlimited retries", "Client-side filtering"], "answer": ["selectinload", "joinedload"], "tags": ["selectinload", "joinedload"]},
    {"type": "scenario_choice", "prompt": "A downstream service is failing and your app keeps retrying instantly. What should you add first?", "options": ["Timeouts and exponential backoff", "More unlimited retries", "A larger JSON payload", "A second frontend"], "answer": "Timeouts and exponential backoff", "tags": ["timeout", "backoff"]},
    {"type": "ordering", "prompt": "Order the transaction flow.", "options": ["Begin transaction", "Apply all writes", "Commit if all succeed", "Roll back on failure"], "answer": ["Begin transaction", "Apply all writes", "Commit if all succeed", "Roll back on failure"], "tags": ["transaction", "acid"]},
    {"type": "matching", "prompt": "Match data shape to storage fit.", "pairs": [{"left": "Strong relationships", "right": "SQL"}, {"left": "Flexible documents", "right": "NoSQL"}, {"left": "Hot session cache", "right": "Redis"}], "answer": {"Strong relationships": "SQL", "Flexible documents": "NoSQL", "Hot session cache": "Redis"}, "tags": ["sql", "nosql"]},
    {"type": "code_fill", "prompt": "Fill the safer SQLAlchemy loading option for a collection.", "code": "stmt = select(User).options(____(User.orders))", "options": ["selectinload", "time.sleep", "requests.get", "os.system"], "answer": "selectinload", "tags": ["sqlalchemy", "loading"]},
    {"type": "multiple_choice", "prompt": "CPU-heavy image processing is slowing requests. Which model helps most?", "options": ["Parallelism", "Async await only", "More CORS headers", "Offset pagination"], "answer": "Parallelism", "tags": ["parallelism", "cpu"]},
    {"type": "scenario_choice", "prompt": "A product page needs recommendations, but the recommender is down. What behavior is best?", "options": ["Serve the page without recommendations", "Fail the entire page", "Retry forever", "Delete the cache"], "answer": "Serve the page without recommendations", "tags": ["degradation", "reliability"]},
    {"type": "multi_select", "prompt": "Which signals make an API easier for clients to use?", "options": ["Stable contract", "Clear status codes", "Documented schema", "Random response fields"], "answer": ["Stable contract", "Clear status codes", "Documented schema"], "tags": ["contract", "openapi"]},
    {"type": "bug_hunt", "prompt": "A response model includes password_hash. What is the bug?", "options": ["Leaking sensitive data", "Using a router", "Returning JSON", "Using a status code"], "answer": "Leaking sensitive data", "tags": ["response model", "security"]},
    {"type": "scenario_choice", "prompt": "A social like count appears five seconds late. When is that acceptable?", "options": ["When eventual consistency is acceptable", "When money is transferred", "When validating passwords", "When committing inventory"], "answer": "When eventual consistency is acceptable", "tags": ["eventual consistency", "trade-off"]},
]


def lesson(module_id, idx, item):
    lid, title, summary, points, example = item
    return {
        "id": f"{module_id}-{lid}",
        "title": title,
        "summary": summary,
        "explanation": f"{summary} In interviews, explain the concept, when it applies, and the trade-off it introduces. Use concrete examples from the provided material instead of definitions alone.",
        "key_points": points,
        "examples": [example],
        "interview_questions": [f"When would you apply {title.lower()}?", f"What failure mode appears when {title.lower()} is misunderstood?"],
        "difficulty": 1 if idx < 2 else 2,
        "tags": points[:3],
    }


def questions(module_id, module_title, tags):
    items = []
    for index, pattern in enumerate(QUESTION_PATTERNS, start=1):
        qtype = pattern["type"]
        q = {
            "id": f"{module_id}-q{index:02d}",
            "type": qtype,
            "prompt": pattern["prompt"],
            "explanation": f"Key idea: apply {module_title} by choosing the option that protects correctness, clarity, reliability, or maintainability in a real interview scenario.",
            "difficulty": 1 if index <= 4 else 2 if index <= 10 else 3,
            "tags": list(dict.fromkeys(tags[:2] + pattern["tags"][:2])),
        }
        for field in ["options", "pairs", "code", "answer"]:
            if field in pattern:
                q[field] = pattern[field]
        items.append(q)
    return items


def challenge(module_id, title, tags):
    return {
        "id": f"{module_id}-classify-status",
        "title": f"{title} status classifier",
        "instructions": "Implement classify_status_code(code: int) -> str. Return success for 200-299, redirect for 300-399, client_error for 400-499, server_error for 500-599, and unknown otherwise.",
        "starter_code": "def classify_status_code(code: int) -> str:\n    pass\n",
        "function_signature": "def classify_status_code(code: int) -> str",
        "visible_tests": [
            {"name": "created", "call": "classify_status_code(201)", "expected": "success"},
            {"name": "not found", "call": "classify_status_code(404)", "expected": "client_error"},
        ],
        "hidden_tests": [
            {"name": "service unavailable", "call": "classify_status_code(503)", "expected": "server_error"},
            {"name": "redirect", "call": "classify_status_code(302)", "expected": "redirect"},
            {"name": "unknown", "call": "classify_status_code(99)", "expected": "unknown"},
        ],
        "timeout_seconds": 2,
        "explanation": "The challenge reinforces deterministic branching, status-code categories, and local test execution.",
        "difficulty": 1,
        "tags": tags[:3],
    }


def main():
    CONTENT.mkdir(exist_ok=True)
    files = []
    for order, (module_id, title, description, tags, lesson_data) in enumerate(MODULES, start=1):
        module_questions = questions(module_id, title, tags)
        data = {
            "id": module_id,
            "title": title,
            "description": description,
            "order": order,
            "tags": tags,
            "lessons": [lesson(module_id, i, item) for i, item in enumerate(lesson_data)],
            "questions": module_questions,
            "coding_challenges": [challenge(module_id, title, tags)],
            "boss_battle": {
                "id": f"{module_id}-boss",
                "title": f"{title} boss battle",
                "question_ids": [item["id"] for item in module_questions[:12]],
                "passing_threshold": 0.75,
                "reward_xp": 100,
            },
        }
        file_name = f"{module_id}.json"
        files.append(file_name)
        (CONTENT / file_name).write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    (CONTENT / "manifest.json").write_text(json.dumps({"modules": files}, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()

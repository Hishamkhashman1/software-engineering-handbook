import json
import re
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


TARGETED_BANK = {
    "web-fundamentals": [
        {"type": "ordering", "prompt": "Put the browser request lifecycle in order.", "options": ["Resolve DNS", "Open HTTPS/TLS connection", "Send HTTP request", "Receive HTTP response"], "answer": ["Resolve DNS", "Open HTTPS/TLS connection", "Send HTTP request", "Receive HTTP response"], "explanation": "A browser first resolves the hostname, establishes a secure connection when using HTTPS, sends the request, then receives status, headers, and body.", "tags": ["dns", "https", "request"], "difficulty": 1},
        {"type": "matching", "prompt": "Match each web term to its job.", "pairs": [{"left": "DNS", "right": "Maps domain names to IP addresses"}, {"left": "TLS", "right": "Encrypts and authenticates the connection"}, {"left": "HTTP", "right": "Defines request and response messages"}], "answer": {"DNS": "Maps domain names to IP addresses", "TLS": "Encrypts and authenticates the connection", "HTTP": "Defines request and response messages"}, "explanation": "DNS finds the server, TLS protects the channel, and HTTP carries the application-level request and response.", "tags": ["dns", "tls", "http"], "difficulty": 1},
        {"type": "multi_select", "prompt": "Which fields are usually part of an HTTP request?", "options": ["URL", "Method", "Headers", "Optional body", "Database index"], "answer": ["URL", "Method", "Headers", "Optional body"], "explanation": "Requests contain routing and intent data: URL, method, headers, query parameters, and sometimes a body.", "tags": ["request", "method", "headers"], "difficulty": 1},
        {"type": "matching", "prompt": "Match the method to its normal intent.", "pairs": [{"left": "GET", "right": "Retrieve data"}, {"left": "POST", "right": "Create a resource"}, {"left": "PATCH", "right": "Update selected fields"}], "answer": {"GET": "Retrieve data", "POST": "Create a resource", "PATCH": "Update selected fields"}, "explanation": "HTTP methods communicate intent. PATCH is partial update; PUT is full replacement; POST usually creates or triggers processing.", "tags": ["get", "post", "patch"], "difficulty": 1},
        {"type": "scenario_choice", "prompt": "A client sends only a new email for an existing user. Which method is most precise?", "options": ["PATCH", "PUT", "GET", "DELETE"], "answer": "PATCH", "explanation": "PATCH communicates partial update. PUT would normally mean replacing the full user representation.", "tags": ["patch", "put", "method"], "difficulty": 1},
        {"type": "matching", "prompt": "Match each status code to the interview meaning.", "pairs": [{"left": "201", "right": "Resource created"}, {"left": "401", "right": "Authentication required"}, {"left": "403", "right": "Authenticated but forbidden"}], "answer": {"201": "Resource created", "401": "Authentication required", "403": "Authenticated but forbidden"}, "explanation": "401 is about missing/invalid authentication. 403 is about authorization after identity is known.", "tags": ["status code", "401", "403"], "difficulty": 1},
        {"type": "multi_select", "prompt": "Which examples are HTTP headers?", "options": ["Authorization", "Content-Type", "Accept", "Cache-Control", "PRIMARY KEY"], "answer": ["Authorization", "Content-Type", "Accept", "Cache-Control"], "explanation": "Headers are request/response metadata. Authorization, Content-Type, Accept, and Cache-Control are common HTTP headers.", "tags": ["headers", "authorization", "cache-control"], "difficulty": 1},
        {"type": "scenario_choice", "prompt": "Your React app at localhost:5173 calls an API at localhost:8000 and the browser blocks it. What is the likely mechanism?", "options": ["CORS", "SQL isolation", "B-tree compaction", "JWT signing"], "answer": "CORS", "explanation": "Different scheme/host/port combinations are different origins. Browsers require the API to allow the frontend origin via CORS.", "tags": ["cors", "origin", "browser"], "difficulty": 2},
        {"type": "matching", "prompt": "Match browser state mechanisms.", "pairs": [{"left": "Cookie", "right": "Small browser-stored value sent with requests"}, {"left": "Session", "right": "Server-side data linked by an ID"}, {"left": "Session ID", "right": "Identifier often stored in a cookie"}], "answer": {"Cookie": "Small browser-stored value sent with requests", "Session": "Server-side data linked by an ID", "Session ID": "Identifier often stored in a cookie"}, "explanation": "Cookies live in the browser; sessions live on the server and are usually referenced by an ID stored in a cookie.", "tags": ["cookies", "sessions"], "difficulty": 2},
        {"type": "multi_select", "prompt": "What does HTTPS add over plain HTTP?", "options": ["Encryption", "Authentication", "Data integrity", "Automatic database sharding"], "answer": ["Encryption", "Authentication", "Data integrity"], "explanation": "HTTPS uses TLS to protect confidentiality, verify the server identity, and detect tampering.", "tags": ["https", "tls"], "difficulty": 1},
        {"type": "bug_hunt", "prompt": "A production site sends login tokens over plain HTTP. What is the bug?", "options": ["Traffic can be read or modified in transit", "DNS cannot resolve names", "PATCH replaces the resource", "CORS disables cookies"], "answer": "Traffic can be read or modified in transit", "explanation": "Without HTTPS, intermediaries may inspect or alter sensitive traffic such as tokens and session identifiers.", "tags": ["http", "https", "security"], "difficulty": 2},
        {"type": "scenario_choice", "prompt": "A response succeeds but intentionally has no body. Which status code fits?", "options": ["204", "201", "404", "503"], "answer": "204", "explanation": "204 means success with no response body. It is common for successful deletes or updates that return nothing.", "tags": ["status code", "response"], "difficulty": 1},
    ],
    "apis": [
        {"type": "matching", "prompt": "Match each API style or artifact.", "pairs": [{"left": "REST", "right": "Resource URLs plus HTTP methods"}, {"left": "gRPC", "right": "HTTP/2 plus Protocol Buffers"}, {"left": "OpenAPI", "right": "Machine-readable API specification"}], "answer": {"REST": "Resource URLs plus HTTP methods", "gRPC": "HTTP/2 plus Protocol Buffers", "OpenAPI": "Machine-readable API specification"}, "explanation": "REST is resource-oriented and human-readable; gRPC is efficient for service-to-service calls; OpenAPI documents contracts.", "tags": ["rest", "grpc", "openapi"], "difficulty": 1},
        {"type": "scenario_choice", "prompt": "A browser-facing public API must be easy for humans to inspect and test. Which style usually fits best?", "options": ["REST", "gRPC", "Raw TCP protocol", "Cron job"], "answer": "REST", "explanation": "REST over HTTP with JSON is easy for browsers, humans, and tools to inspect. gRPC is stronger for internal high-performance service calls.", "tags": ["rest", "grpc"], "difficulty": 1},
        {"type": "scenario_choice", "prompt": "Two internal services need low-latency binary communication and shared generated clients. What fits better?", "options": ["gRPC", "REST with ad hoc JSON", "Swagger UI only", "HTML form posts"], "answer": "gRPC", "explanation": "gRPC uses Protocol Buffers and HTTP/2, which suits internal service-to-service communication with generated clients.", "tags": ["grpc", "protobuf"], "difficulty": 2},
        {"type": "multi_select", "prompt": "What belongs in an API contract?", "options": ["Endpoints", "Request bodies", "Response schemas", "Status codes", "Developer laptop color"], "answer": ["Endpoints", "Request bodies", "Response schemas", "Status codes"], "explanation": "An API contract defines how client and server communicate: routes, parameters, payloads, response shapes, and status behavior.", "tags": ["api contract", "status codes"], "difficulty": 1},
        {"type": "matching", "prompt": "Match OpenAPI and Swagger.", "pairs": [{"left": "OpenAPI", "right": "The specification format"}, {"left": "Swagger UI", "right": "Interactive documentation generated from the spec"}, {"left": "FastAPI /docs", "right": "A local Swagger interface"}], "answer": {"OpenAPI": "The specification format", "Swagger UI": "Interactive documentation generated from the spec", "FastAPI /docs": "A local Swagger interface"}, "explanation": "OpenAPI is the contract document; Swagger UI is one common interface for exploring it.", "tags": ["openapi", "swagger"], "difficulty": 1},
        {"type": "matching", "prompt": "Map CRUD to HTTP methods.", "pairs": [{"left": "Create", "right": "POST"}, {"left": "Read", "right": "GET"}, {"left": "Delete", "right": "DELETE"}], "answer": {"Create": "POST", "Read": "GET", "Delete": "DELETE"}, "explanation": "CRUD maps cleanly to REST: create with POST, read with GET, update with PUT/PATCH, delete with DELETE.", "tags": ["crud", "post", "get"], "difficulty": 1},
        {"type": "ordering", "prompt": "Order a request body through serialization boundaries.", "options": ["Client object", "Serialized JSON", "HTTP request body", "Server deserializes into model"], "answer": ["Client object", "Serialized JSON", "HTTP request body", "Server deserializes into model"], "explanation": "Serialization turns objects into transfer formats such as JSON; deserialization turns received data back into application models.", "tags": ["serialization", "deserialization"], "difficulty": 2},
        {"type": "scenario_choice", "prompt": "A response shape must change in a breaking way. What protects existing clients?", "options": ["Add /v2", "Silently change /v1", "Delete the old endpoint today", "Ask clients to parse anything"], "answer": "Add /v2", "explanation": "Versioning lets old clients continue using the old contract while new clients adopt the breaking change.", "tags": ["versioning", "api contract"], "difficulty": 1},
        {"type": "matching", "prompt": "Match pagination strategies.", "pairs": [{"left": "Offset pagination", "right": "Simple page numbers but unstable on changing data"}, {"left": "Cursor pagination", "right": "Continue after a stable record marker"}, {"left": "Large unpaginated response", "right": "High memory and latency risk"}], "answer": {"Offset pagination": "Simple page numbers but unstable on changing data", "Cursor pagination": "Continue after a stable record marker", "Large unpaginated response": "High memory and latency risk"}, "explanation": "Offset is easy for dashboards; cursor is safer for large or changing feeds.", "tags": ["pagination", "offset", "cursor"], "difficulty": 2},
        {"type": "scenario_choice", "prompt": "Which URL filters users to Mexico?", "options": ["GET /users?country=Mexico", "POST /users?page=Mexico", "GET /users#Mexico", "DELETE /users?country=Mexico"], "answer": "GET /users?country=Mexico", "explanation": "Filtering is commonly expressed with query parameters that constrain returned records.", "tags": ["filtering", "query parameters"], "difficulty": 1},
        {"type": "scenario_choice", "prompt": "Which URL sorts newest users first?", "options": ["GET /users?sort=-created_at", "GET /users?filter=-created_at", "POST /sort/users", "GET /users?country=created_at"], "answer": "GET /users?sort=-created_at", "explanation": "A common convention is `sort=field` for ascending and `sort=-field` for descending.", "tags": ["sorting", "pagination"], "difficulty": 1},
        {"type": "multi_select", "prompt": "Which requests are idempotent in normal REST design?", "options": ["GET /users/5", "PUT /users/5", "DELETE /users/5", "POST /users"], "answer": ["GET /users/5", "PUT /users/5", "DELETE /users/5"], "explanation": "Idempotent operations produce the same final state when repeated. POST usually creates another resource unless protected by an idempotency key.", "tags": ["idempotency", "retry"], "difficulty": 2},
    ],
}

TARGETED_BANK.update({
    "backend": [
        {"type": "matching", "prompt": "Match backend frameworks to their common strengths.", "pairs": [{"left": "FastAPI", "right": "Typed Python APIs with validation and OpenAPI"}, {"left": "Flask", "right": "Small flexible Python services"}, {"left": "NestJS", "right": "Structured TypeScript backend architecture"}], "answer": {"FastAPI": "Typed Python APIs with validation and OpenAPI", "Flask": "Small flexible Python services", "NestJS": "Structured TypeScript backend architecture"}, "explanation": "Framework choice depends on language, team style, and structure needs. FastAPI gives typed validation and docs; Flask is minimal; NestJS is opinionated.", "tags": ["fastapi", "flask", "nestjs"], "difficulty": 1},
        {"type": "scenario_choice", "prompt": "A JavaScript team needs a lightweight REST API. Which framework is the natural fit?", "options": ["Express", "FastAPI", "Django ORM", "pytest"], "answer": "Express", "explanation": "Express is a lightweight Node.js web framework commonly used for REST APIs.", "tags": ["express", "node"], "difficulty": 1},
        {"type": "ordering", "prompt": "Order a typical FastAPI request lifecycle.", "options": ["Middleware runs", "Router matches endpoint", "Dependencies are injected", "Endpoint returns response model"], "answer": ["Middleware runs", "Router matches endpoint", "Dependencies are injected", "Endpoint returns response model"], "explanation": "Middleware wraps the request, routing selects the endpoint, dependency injection supplies objects such as DB sessions, and response models shape output.", "tags": ["request lifecycle", "middleware", "router"], "difficulty": 2},
        {"type": "scenario_choice", "prompt": "Many endpoints need a database session, but tests should swap it out. What pattern helps?", "options": ["Dependency injection", "Global mutable variable", "Hardcoded singleton", "Inline SQL string everywhere"], "answer": "Dependency injection", "explanation": "Dependency injection supplies shared objects without hardcoding construction, making endpoints easier to test and decouple.", "tags": ["dependency injection", "testing"], "difficulty": 2},
        {"type": "multi_select", "prompt": "Which tasks belong in application lifespan startup?", "options": ["Initialize connection pools", "Load shared models", "Configure caches", "Validate every request body"], "answer": ["Initialize connection pools", "Load shared models", "Configure caches"], "explanation": "Lifespan startup runs once for shared initialization. Per-request validation belongs in request handling.", "tags": ["lifespan", "startup"], "difficulty": 2},
        {"type": "scenario_choice", "prompt": "An email can be sent after the API response returns. Which FastAPI feature fits?", "options": ["Background task", "Response model", "CORS header", "Primary key"], "answer": "Background task", "explanation": "Background tasks are useful when work can continue after the user receives the response.", "tags": ["background tasks"], "difficulty": 1},
        {"type": "bug_hunt", "prompt": "An endpoint returns password_hash because it serializes the ORM object directly. What is the bug?", "options": ["Missing response model", "Missing DNS lookup", "Wrong pagination style", "Too much CORS"], "answer": "Missing response model", "explanation": "Response models define the public output shape and prevent sensitive internal fields from leaking.", "tags": ["response model", "security"], "difficulty": 2},
        {"type": "multi_select", "prompt": "Which jobs benefit from async concurrency?", "options": ["Waiting on database I/O", "Waiting on external HTTP APIs", "Reading files", "CPU-heavy image encoding"], "answer": ["Waiting on database I/O", "Waiting on external HTTP APIs", "Reading files"], "explanation": "Async helps while waiting on I/O. CPU-heavy work needs parallelism or worker processes.", "tags": ["async", "concurrency", "await"], "difficulty": 2},
        {"type": "scenario_choice", "prompt": "A CPU-heavy ML inference step blocks requests. What helps more than `await` alone?", "options": ["Parallelism or worker process", "More query parameters", "Swagger UI", "Cookie session"], "answer": "Parallelism or worker process", "explanation": "Async does not make CPU work run in parallel. CPU-bound work needs process/thread pools or separate workers.", "tags": ["parallelism", "cpu"], "difficulty": 2},
        {"type": "matching", "prompt": "Match backend building blocks.", "pairs": [{"left": "Router", "right": "Groups related endpoints"}, {"left": "Middleware", "right": "Runs before or after requests"}, {"left": "Validation", "right": "Rejects invalid input before logic"}], "answer": {"Router": "Groups related endpoints", "Middleware": "Runs before or after requests", "Validation": "Rejects invalid input before logic"}, "explanation": "Routers organize endpoints, middleware wraps requests, and validation protects business logic.", "tags": ["router", "middleware", "validation"], "difficulty": 1},
        {"type": "code_fill", "prompt": "Fill the FastAPI dependency injection marker.", "code": "def list_users(db: Session = ____(get_db)):\n    return service.list_users(db)", "options": ["Depends", "await", "BaseModel", "BackgroundTasks"], "answer": "Depends", "explanation": "FastAPI uses `Depends` to declare dependencies such as database sessions.", "tags": ["fastapi", "dependency injection"], "difficulty": 2},
        {"type": "scenario_choice", "prompt": "A request body contains age=-10. Where should that fail?", "options": ["Request validation", "DNS resolution", "Background task queue", "Swagger CSS"], "answer": "Request validation", "explanation": "Invalid input should fail at validation before business logic runs.", "tags": ["validation", "pydantic"], "difficulty": 1},
    ],
    "databases": [
        {"type": "matching", "prompt": "Match database type to fit.", "pairs": [{"left": "PostgreSQL", "right": "Relational data and complex queries"}, {"left": "MongoDB", "right": "Flexible document-shaped records"}, {"left": "Redis", "right": "Fast in-memory cache or session store"}], "answer": {"PostgreSQL": "Relational data and complex queries", "MongoDB": "Flexible document-shaped records", "Redis": "Fast in-memory cache or session store"}, "explanation": "SQL databases fit relationships and constraints; document stores fit flexible records; Redis is often used for cache/session data.", "tags": ["postgresql", "mongodb", "redis"], "difficulty": 1},
        {"type": "scenario_choice", "prompt": "Orders must reference users and support financial reports. Which database model fits first?", "options": ["Relational SQL", "Unstructured document only", "Static JSON files", "Browser localStorage"], "answer": "Relational SQL", "explanation": "Strong relationships, constraints, and reports are natural fits for relational databases.", "tags": ["relational", "sql"], "difficulty": 1},
        {"type": "matching", "prompt": "Match relational key terms.", "pairs": [{"left": "Primary key", "right": "Unique row identifier"}, {"left": "Foreign key", "right": "Reference to another table"}, {"left": "Junction table", "right": "Represents many-to-many relationships"}], "answer": {"Primary key": "Unique row identifier", "Foreign key": "Reference to another table", "Junction table": "Represents many-to-many relationships"}, "explanation": "Keys are how relational databases identify rows and enforce relationships.", "tags": ["primary key", "foreign key", "relationship"], "difficulty": 1},
        {"type": "matching", "prompt": "Match JOIN types.", "pairs": [{"left": "INNER JOIN", "right": "Only matching rows"}, {"left": "LEFT JOIN", "right": "All left rows plus matches"}, {"left": "FULL JOIN", "right": "Rows from both sides"}], "answer": {"INNER JOIN": "Only matching rows", "LEFT JOIN": "All left rows plus matches", "FULL JOIN": "Rows from both sides"}, "explanation": "JOIN type controls which unmatched rows are kept while combining related tables.", "tags": ["join", "relationship"], "difficulty": 2},
        {"type": "multi_select", "prompt": "Which columns are good index candidates?", "options": ["Columns in frequent WHERE filters", "Foreign keys used in JOINs", "Columns used for ORDER BY", "Every column automatically"], "answer": ["Columns in frequent WHERE filters", "Foreign keys used in JOINs", "Columns used for ORDER BY"], "explanation": "Indexes speed common lookup, join, and ordering paths, but too many indexes slow writes.", "tags": ["index", "where", "join"], "difficulty": 2},
        {"type": "ordering", "prompt": "Order a safe money-transfer transaction.", "options": ["Begin transaction", "Debit source account", "Credit destination account", "Commit or roll back all changes"], "answer": ["Begin transaction", "Debit source account", "Credit destination account", "Commit or roll back all changes"], "explanation": "Transactions keep multi-step changes atomic so partial updates do not corrupt balances.", "tags": ["transaction", "acid"], "difficulty": 2},
        {"type": "matching", "prompt": "Match ACID properties.", "pairs": [{"left": "Atomicity", "right": "All or nothing"}, {"left": "Consistency", "right": "Valid rules remain valid"}, {"left": "Isolation", "right": "Concurrent transactions do not interfere unexpectedly"}], "answer": {"Atomicity": "All or nothing", "Consistency": "Valid rules remain valid", "Isolation": "Concurrent transactions do not interfere unexpectedly"}, "explanation": "ACID describes reliability guarantees for transactions in relational databases.", "tags": ["acid", "transaction", "consistency"], "difficulty": 2},
        {"type": "scenario_choice", "prompt": "Read traffic is high but writes fit on one primary database. What can help reads?", "options": ["Read replica", "Random UUID only", "Drop all indexes", "Move CSS files"], "answer": "Read replica", "explanation": "Read replicas copy data for serving reads. They are not the same as sharding because all data is still replicated.", "tags": ["replica", "read"], "difficulty": 2},
        {"type": "scenario_choice", "prompt": "One database cannot hold the data volume or write load. Which approach splits data?", "options": ["Sharding", "Read replica only", "LEFT JOIN", "Cookie session"], "answer": "Sharding", "explanation": "Sharding partitions data across nodes. It increases scale but complicates routing and cross-shard queries.", "tags": ["sharding", "partition"], "difficulty": 2},
        {"type": "scenario_choice", "prompt": "A social like count is briefly stale after a write. Which model can accept that?", "options": ["Eventual consistency", "Strict financial transaction", "Primary key constraint", "Syntax validation"], "answer": "Eventual consistency", "explanation": "Eventual consistency accepts temporary staleness when immediate correctness is not required.", "tags": ["consistency", "eventual consistency"], "difficulty": 2},
        {"type": "bug_hunt", "prompt": "A query scans millions of users for every login by email. What is likely missing?", "options": ["Index on email", "CORS preflight", "Docker Compose", "Swagger UI"], "answer": "Index on email", "explanation": "A lookup by email should usually use an index, otherwise the database may scan every row.", "tags": ["index", "query"], "difficulty": 1},
        {"type": "multi_select", "prompt": "Which are common NoSQL use cases from this module?", "options": ["Flexible documents", "Caching", "High-volume logs", "Strict relational joins only"], "answer": ["Flexible documents", "Caching", "High-volume logs"], "explanation": "NoSQL systems are often chosen for flexible schemas, caches, high-volume documents/logs, or specialized access patterns.", "tags": ["nosql", "mongodb", "redis"], "difficulty": 1},
    ],
    "sqlalchemy": [
        {"type": "matching", "prompt": "Match SQLAlchemy core concepts.", "pairs": [{"left": "Model", "right": "Python class mapped to a table"}, {"left": "Session", "right": "Unit-of-work boundary for persistence"}, {"left": "Relationship", "right": "Object link between tables"}], "answer": {"Model": "Python class mapped to a table", "Session": "Unit-of-work boundary for persistence", "Relationship": "Object link between tables"}, "explanation": "SQLAlchemy maps Python objects to relational tables and uses sessions to track changes.", "tags": ["model", "session", "relationship"], "difficulty": 1},
        {"type": "ordering", "prompt": "Order a typical SQLAlchemy create flow.", "options": ["Create model object", "Add to session", "Flush or commit", "Refresh/read generated fields"], "answer": ["Create model object", "Add to session", "Flush or commit", "Refresh/read generated fields"], "explanation": "The session tracks pending objects; flush sends SQL; commit completes the transaction.", "tags": ["session", "unit of work"], "difficulty": 2},
        {"type": "scenario_choice", "prompt": "You need the new row ID before committing. Which operation can send pending SQL?", "options": ["flush", "joinedload", "rollback", "relationship"], "answer": "flush", "explanation": "Flush sends pending changes to the database within the transaction, often making generated IDs available before commit.", "tags": ["flush", "session"], "difficulty": 2},
        {"type": "bug_hunt", "prompt": "Loading 100 users then reading user.orders causes 101 SQL queries. What is the problem?", "options": ["N+1 from lazy loading", "CORS preflight", "Missing Swagger", "DNS lookup"], "answer": "N+1 from lazy loading", "explanation": "Lazy relationship access inside a loop can issue one query per parent row, creating the N+1 pattern.", "tags": ["n+1", "lazy loading"], "difficulty": 2},
        {"type": "multi_select", "prompt": "Which loading strategies can fix many N+1 collection reads?", "options": ["selectinload", "joinedload", "time.sleep", "os.system"], "answer": ["selectinload", "joinedload"], "explanation": "selectinload and joinedload eager-load related data instead of lazily querying each row.", "tags": ["selectinload", "joinedload", "eager"], "difficulty": 2},
        {"type": "scenario_choice", "prompt": "A collection relationship creates huge duplicate parent rows with a JOIN. Which eager strategy is often safer?", "options": ["selectinload", "raw string concat", "global session", "CORS"], "answer": "selectinload", "explanation": "selectinload loads collections with a second SELECT and avoids one huge joined result for large collections.", "tags": ["selectinload", "loading"], "difficulty": 2},
        {"type": "matching", "prompt": "Match migration terms.", "pairs": [{"left": "Migration", "right": "Versioned schema change"}, {"left": "Alembic", "right": "Common SQLAlchemy migration tool"}, {"left": "Rollback", "right": "Reverts a schema change"}], "answer": {"Migration": "Versioned schema change", "Alembic": "Common SQLAlchemy migration tool", "Rollback": "Reverts a schema change"}, "explanation": "Migrations make database schema evolution explicit, reviewable, and repeatable.", "tags": ["migration", "alembic"], "difficulty": 2},
        {"type": "scenario_choice", "prompt": "An ORM query is too complex and database-specific. What escape hatch can be appropriate?", "options": ["Raw SQL with parameters", "String interpolation with user input", "Disable transactions", "Ignore indexes"], "answer": "Raw SQL with parameters", "explanation": "SQLAlchemy allows raw SQL when needed, but parameters are essential to avoid injection risks.", "tags": ["raw sql", "query"], "difficulty": 3},
        {"type": "ordering", "prompt": "Order a safe transactional update.", "options": ["Open session/transaction", "Load rows", "Apply changes", "Commit or rollback"], "answer": ["Open session/transaction", "Load rows", "Apply changes", "Commit or rollback"], "explanation": "A session often scopes a transaction; failures should roll back pending changes.", "tags": ["transaction", "session"], "difficulty": 2},
        {"type": "code_fill", "prompt": "Fill the SQLAlchemy eager-loading option.", "code": "stmt = select(User).options(____(User.orders))", "options": ["selectinload", "Depends", "pytest", "BaseModel"], "answer": "selectinload", "explanation": "selectinload is an eager-loading option commonly used to avoid N+1 queries for collections.", "tags": ["selectinload", "eager"], "difficulty": 2},
        {"type": "bug_hunt", "prompt": "A web app shares one global SQLAlchemy Session across all requests. What is the risk?", "options": ["Request state leaks and transaction boundaries blur", "DNS becomes slower", "Swagger disappears", "PATCH becomes GET"], "answer": "Request state leaks and transaction boundaries blur", "explanation": "Sessions should be scoped carefully, often per request, so transactions and identity maps do not leak across users.", "tags": ["session", "unit of work"], "difficulty": 3},
        {"type": "matching", "prompt": "Match relationship shapes.", "pairs": [{"left": "One-to-many", "right": "User has many orders"}, {"left": "Many-to-many", "right": "Students enroll in courses"}, {"left": "Foreign key", "right": "Column that points to another table"}], "answer": {"One-to-many": "User has many orders", "Many-to-many": "Students enroll in courses", "Foreign key": "Column that points to another table"}, "explanation": "SQLAlchemy relationships mirror relational foreign-key structures and association tables.", "tags": ["relationship", "foreign key"], "difficulty": 1},
    ],
    "testing": [
        {"type": "matching", "prompt": "Match test level to scope.", "pairs": [{"left": "Unit test", "right": "Small isolated logic"}, {"left": "Integration test", "right": "Multiple real boundaries together"}, {"left": "E2E test", "right": "User workflow through the system"}], "answer": {"Unit test": "Small isolated logic", "Integration test": "Multiple real boundaries together", "E2E test": "User workflow through the system"}, "explanation": "Different test levels catch different failures. Unit tests are fast; integration/e2e tests cover wiring and workflows.", "tags": ["unit", "integration", "e2e"], "difficulty": 1},
        {"type": "scenario_choice", "prompt": "A pure XP formula has no external dependencies. What test level fits best?", "options": ["Unit test", "E2E test", "Manual smoke only", "Production alert"], "answer": "Unit test", "explanation": "Small deterministic logic should be unit-tested directly and cheaply.", "tags": ["unit", "pytest"], "difficulty": 1},
        {"type": "scenario_choice", "prompt": "A test needs a clean temporary database for each case. What pytest feature fits?", "options": ["Fixture", "Swagger UI", "CORS", "Docker image layer"], "answer": "Fixture", "explanation": "Pytest fixtures provide reusable setup and teardown, such as isolated databases.", "tags": ["pytest", "fixture"], "difficulty": 1},
        {"type": "multi_select", "prompt": "Which boundaries are reasonable to mock?", "options": ["Email provider", "Payment gateway sandbox", "Slow external API", "The function under test"], "answer": ["Email provider", "Payment gateway sandbox", "Slow external API"], "explanation": "Mocks replace slow, costly, or nondeterministic boundaries. Do not mock the behavior you are trying to verify.", "tags": ["mock", "test double"], "difficulty": 2},
        {"type": "matching", "prompt": "Match quality terms.", "pairs": [{"left": "Mock", "right": "Programmable replacement for a dependency"}, {"left": "Stub", "right": "Simple canned response"}, {"left": "Fake", "right": "Lightweight working implementation"}], "answer": {"Mock": "Programmable replacement for a dependency", "Stub": "Simple canned response", "Fake": "Lightweight working implementation"}, "explanation": "Test doubles have different strengths. Naming them clearly keeps tests understandable.", "tags": ["mock", "test double"], "difficulty": 2},
        {"type": "scenario_choice", "prompt": "A fixed bug should never return. What test should you add?", "options": ["Regression test", "Only a screenshot", "A DNS record", "A color token"], "answer": "Regression test", "explanation": "Regression tests capture a known failure so future changes do not reintroduce it.", "tags": ["regression"], "difficulty": 1},
        {"type": "scenario_choice", "prompt": "Frontend behavior should verify that feedback appears after a click. Which tool family fits?", "options": ["React Testing Library or Jest/Vitest", "SQLAlchemy migration", "Redis pub/sub", "OpenAPI only"], "answer": "React Testing Library or Jest/Vitest", "explanation": "Frontend tests should interact with UI behavior, not only assert components exist.", "tags": ["jest", "vitest", "frontend testing"], "difficulty": 2},
        {"type": "multi_select", "prompt": "What should CI run before merge?", "options": ["Backend tests", "Frontend tests", "Type checks", "Random production deploy"], "answer": ["Backend tests", "Frontend tests", "Type checks"], "explanation": "CI should automatically run the checks that protect code quality before changes merge.", "tags": ["ci", "type check"], "difficulty": 1},
        {"type": "scenario_choice", "prompt": "Two services must agree on request/response shape. What catches drift?", "options": ["Contract test", "CSS lint only", "Manual memory", "Read replica"], "answer": "Contract test", "explanation": "Contract tests verify that provider and consumer agree on the API contract.", "tags": ["contract test", "api"], "difficulty": 2},
        {"type": "bug_hunt", "prompt": "Coverage is 95%, but no assertions check business outcomes. What is the issue?", "options": ["Coverage is not proof of meaningful tests", "Coverage means all bugs are impossible", "Fixtures are banned", "Mocks always fail"], "answer": "Coverage is not proof of meaningful tests", "explanation": "Coverage shows executed lines, not whether tests assert the right behavior.", "tags": ["coverage", "quality"], "difficulty": 2},
        {"type": "ordering", "prompt": "Order a TDD loop.", "options": ["Write failing test", "Implement minimal code", "Refactor", "Repeat"], "answer": ["Write failing test", "Implement minimal code", "Refactor", "Repeat"], "explanation": "TDD uses a red-green-refactor loop to drive small increments.", "tags": ["tdd", "unit"], "difficulty": 1},
        {"type": "multi_select", "prompt": "Which are meaningful backend integration-test boundaries?", "options": ["API route plus database", "Validation plus service logic", "Repository plus transaction", "Only CSS hover color"], "answer": ["API route plus database", "Validation plus service logic", "Repository plus transaction"], "explanation": "Integration tests verify important pieces working together, especially persistence and API behavior.", "tags": ["integration", "backend"], "difficulty": 2},
    ],
})

TARGETED_BANK.update({
    "performance": [
        {"type": "matching", "prompt": "Match the reliability signal to what it tells you.", "pairs": [{"left": "Latency", "right": "Time one request takes"}, {"left": "Throughput", "right": "Requests completed per second"}, {"left": "p99", "right": "Slowest 1 percent of requests"}], "answer": {"Latency": "Time one request takes", "Throughput": "Requests completed per second", "p99": "Slowest 1 percent of requests"}, "explanation": "Averages hide pain. Interview answers should separate per-request latency, total capacity, and tail latency.", "tags": ["latency", "throughput", "p99"], "difficulty": 1},
        {"type": "scenario_choice", "prompt": "A product catalog is read thousands of times and changes rarely. What is the first likely optimization?", "options": ["Cache the catalog response", "Add unlimited retries", "Shard immediately", "Use POST for reads"], "answer": "Cache the catalog response", "explanation": "Caches are strongest when the same data is read repeatedly and can tolerate controlled staleness.", "tags": ["cache", "read"], "difficulty": 1},
        {"type": "scenario_choice", "prompt": "A public API is being hammered by one client and starving others. What protects the service?", "options": ["Rate limiting", "A wider button", "More nested JSON", "Client-side sorting only"], "answer": "Rate limiting", "explanation": "Rate limits cap request volume per client or key so shared resources remain available.", "tags": ["rate limit", "availability"], "difficulty": 1},
        {"type": "bug_hunt", "prompt": "A failed downstream service causes every caller to retry instantly until the whole system slows down. What is the bug?", "options": ["Retry storm without backoff", "Using metrics", "Having a timeout", "Serving cached data"], "answer": "Retry storm without backoff", "explanation": "Retries need limits, jitter, and exponential backoff. Instant retries can amplify the original outage.", "tags": ["retry", "backoff"], "difficulty": 2},
        {"type": "scenario_choice", "prompt": "A dependency sometimes hangs forever. What should every outbound call include?", "options": ["Timeout", "Offset pagination", "A larger payload", "A hidden form field"], "answer": "Timeout", "explanation": "Timeouts bound waiting and free resources. Without them, stuck dependencies can exhaust worker capacity.", "tags": ["timeout", "resource"], "difficulty": 1},
        {"type": "scenario_choice", "prompt": "A payment provider is failing and repeated calls are wasting threads. Which pattern should temporarily stop calls?", "options": ["Circuit breaker", "More synchronous loops", "Random sleeps only", "Remove logging"], "answer": "Circuit breaker", "explanation": "A circuit breaker stops sending traffic to a dependency that is already failing, then probes for recovery.", "tags": ["circuit breaker", "failure"], "difficulty": 2},
        {"type": "scenario_choice", "prompt": "Checkout receives bursty order events, but processing can happen asynchronously. What smooths the spike?", "options": ["Queue", "Read all rows into memory", "Disable validation", "Remove indexes"], "answer": "Queue", "explanation": "Queues buffer bursts and let workers process at a controlled pace, trading immediacy for resilience.", "tags": ["queue", "backpressure"], "difficulty": 2},
        {"type": "matching", "prompt": "Match observability data to its best use.", "pairs": [{"left": "Logs", "right": "Explain specific events"}, {"left": "Metrics", "right": "Show trends and rates"}, {"left": "Traces", "right": "Follow one request across services"}], "answer": {"Logs": "Explain specific events", "Metrics": "Show trends and rates", "Traces": "Follow one request across services"}, "explanation": "Logs, metrics, and traces answer different production questions; strong debugging uses all three.", "tags": ["logs", "metrics", "traces"], "difficulty": 1},
        {"type": "scenario_choice", "prompt": "Recommendations fail, but the product page can still load. What should the API do?", "options": ["Gracefully degrade and omit recommendations", "Fail the whole page", "Retry forever", "Delete product data"], "answer": "Gracefully degrade and omit recommendations", "explanation": "Graceful degradation keeps the core user path working when optional features fail.", "tags": ["graceful degradation", "reliability"], "difficulty": 2},
        {"type": "multi_select", "prompt": "Which actions reduce tail latency risk?", "options": ["Set timeouts", "Cap fan-out", "Measure p95 and p99", "Only report averages"], "answer": ["Set timeouts", "Cap fan-out", "Measure p95 and p99"], "explanation": "Tail latency grows when requests fan out and wait without bounds. Percentiles reveal it; averages often hide it.", "tags": ["tail latency", "timeout"], "difficulty": 3},
        {"type": "ordering", "prompt": "Order a practical production performance investigation.", "options": ["Measure baseline", "Find bottleneck", "Change one thing", "Compare after metrics"], "answer": ["Measure baseline", "Find bottleneck", "Change one thing", "Compare after metrics"], "explanation": "Performance work should be evidence-driven. Measuring before and after prevents guessing.", "tags": ["metrics", "bottleneck"], "difficulty": 2},
        {"type": "bug_hunt", "prompt": "An endpoint makes 15 downstream calls serially and p99 latency explodes. What should you examine first?", "options": ["Fan-out and slow dependency tails", "CORS headers only", "Button color", "OpenAPI title"], "answer": "Fan-out and slow dependency tails", "explanation": "Serial fan-out stacks latency and increases the chance that one slow dependency dominates the whole request.", "tags": ["fan-out", "p99"], "difficulty": 3},
    ],
    "devops": [
        {"type": "matching", "prompt": "Match Docker terms.", "pairs": [{"left": "Image", "right": "Packaged filesystem and metadata"}, {"left": "Container", "right": "Running instance of an image"}, {"left": "Dockerfile", "right": "Recipe for building an image"}], "answer": {"Image": "Packaged filesystem and metadata", "Container": "Running instance of an image", "Dockerfile": "Recipe for building an image"}, "explanation": "Images are build artifacts; containers are running processes created from those images.", "tags": ["docker", "image", "container"], "difficulty": 1},
        {"type": "ordering", "prompt": "Order a basic Docker image build flow.", "options": ["Choose base image", "Copy dependency files", "Install dependencies", "Copy application code"], "answer": ["Choose base image", "Copy dependency files", "Install dependencies", "Copy application code"], "explanation": "Copying dependency manifests before app code improves layer caching and makes builds faster.", "tags": ["dockerfile", "layer"], "difficulty": 2},
        {"type": "scenario_choice", "prompt": "A developer needs API and database services locally with one command. What fits?", "options": ["Docker Compose", "Manual production deploy", "Swagger UI", "Read replica"], "answer": "Docker Compose", "explanation": "Compose coordinates multiple local containers and their environment/configuration.", "tags": ["docker compose", "local dev"], "difficulty": 1},
        {"type": "scenario_choice", "prompt": "The same code needs different database URLs in dev and prod. Where should this differ?", "options": ["Environment variable", "Hardcoded Python string", "React component text", "Git commit message"], "answer": "Environment variable", "explanation": "Environment variables separate runtime configuration from code and avoid rebuilding for each environment.", "tags": ["environment variable", "config"], "difficulty": 1},
        {"type": "ordering", "prompt": "Order a sane CI/CD pipeline.", "options": ["Install dependencies", "Run tests and type checks", "Build artifact", "Deploy approved artifact"], "answer": ["Install dependencies", "Run tests and type checks", "Build artifact", "Deploy approved artifact"], "explanation": "CI validates a change before CD deploys the exact built artifact.", "tags": ["ci", "cd", "pipeline"], "difficulty": 1},
        {"type": "scenario_choice", "prompt": "A deployment passes build but fails its health check. What should happen?", "options": ["Stop or roll back rollout", "Continue deploying everywhere", "Delete logs", "Ignore alerts"], "answer": "Stop or roll back rollout", "explanation": "Health checks are deployment gates. Failed health should prevent bad versions from spreading.", "tags": ["health check", "rollback"], "difficulty": 2},
        {"type": "matching", "prompt": "Match release safety techniques.", "pairs": [{"left": "Rollback", "right": "Return to a previous known-good version"}, {"left": "Feature flag", "right": "Turn behavior on or off without redeploying"}, {"left": "Canary", "right": "Expose a new version to limited traffic first"}], "answer": {"Rollback": "Return to a previous known-good version", "Feature flag": "Turn behavior on or off without redeploying", "Canary": "Expose a new version to limited traffic first"}, "explanation": "Release safety is about limiting blast radius and making bad changes reversible.", "tags": ["rollback", "feature flag", "canary"], "difficulty": 2},
        {"type": "bug_hunt", "prompt": "A secret API key is committed into source control. What is the issue?", "options": ["Secret leakage; move it to secret management/env config", "Normal versioning", "A Docker cache hit", "A good artifact"], "answer": "Secret leakage; move it to secret management/env config", "explanation": "Secrets should not live in source. Use environment configuration or secret storage and rotate exposed keys.", "tags": ["secrets", "security"], "difficulty": 1},
        {"type": "multi_select", "prompt": "Which outputs help diagnose a production deploy?", "options": ["Application logs", "Deploy version/artifact ID", "Health-check status", "Untracked local files"], "answer": ["Application logs", "Deploy version/artifact ID", "Health-check status"], "explanation": "Deploy diagnosis needs version provenance, runtime health, and logs tied to the release.", "tags": ["logs", "deployment"], "difficulty": 2},
        {"type": "scenario_choice", "prompt": "A bug appears only after deployment, but the built artifact is not recorded. What practice is missing?", "options": ["Artifact/version traceability", "More CSS", "Offset pagination", "DNS round-robin only"], "answer": "Artifact/version traceability", "explanation": "You need to know exactly what code and build artifact is running to debug or roll back confidently.", "tags": ["artifact", "versioning"], "difficulty": 2},
        {"type": "bug_hunt", "prompt": "A container works on one machine because it depends on a file outside the image. What is broken?", "options": ["Image is not self-contained/reproducible", "CI is too strict", "Logs are enabled", "Health check is present"], "answer": "Image is not self-contained/reproducible", "explanation": "Container images should include declared runtime dependencies so they run consistently across machines.", "tags": ["docker", "reproducibility"], "difficulty": 2},
        {"type": "scenario_choice", "prompt": "Infrastructure choice increases speed but removes visibility into failures. What should the interview answer mention?", "options": ["Operational trade-off", "Only UI polish", "Ignore logs", "Disable tests"], "answer": "Operational trade-off", "explanation": "DevOps decisions trade speed, control, cost, portability, and operability. Good answers name the cost.", "tags": ["devops", "trade-off"], "difficulty": 3},
    ],
    "ai-integration": [
        {"type": "matching", "prompt": "Match AI integration terms.", "pairs": [{"left": "Embedding", "right": "Vector representation of meaning"}, {"left": "Vector search", "right": "Finds semantically similar items"}, {"left": "RAG", "right": "Retrieves context before generation"}], "answer": {"Embedding": "Vector representation of meaning", "Vector search": "Finds semantically similar items", "RAG": "Retrieves context before generation"}, "explanation": "RAG usually combines embeddings, vector search, and a generation step grounded in retrieved context.", "tags": ["embedding", "vector search", "rag"], "difficulty": 1},
        {"type": "scenario_choice", "prompt": "A support assistant invents refund rules not present in policy docs. What is the risk?", "options": ["Hallucination", "Read amplification", "CORS preflight", "Index write cost"], "answer": "Hallucination", "explanation": "LLMs can produce plausible unsupported claims. Retrieval, citations, refusals, and evals reduce that risk.", "tags": ["hallucination", "risk"], "difficulty": 1},
        {"type": "scenario_choice", "prompt": "A model needs company policy facts that change weekly. What architecture is usually better than fine-tuning first?", "options": ["RAG over current policy documents", "Hardcode policy into UI", "Ignore retrieval", "Use only temperature changes"], "answer": "RAG over current policy documents", "explanation": "RAG keeps changing knowledge in retrievable data, avoiding retraining for every content update.", "tags": ["rag", "freshness"], "difficulty": 2},
        {"type": "multi_select", "prompt": "Which logs are useful for AI quality review without exposing unnecessary private data?", "options": ["Prompt template/version", "Retrieved document IDs", "Model response outcome", "Raw secrets and passwords"], "answer": ["Prompt template/version", "Retrieved document IDs", "Model response outcome"], "explanation": "AI observability should capture enough provenance to debug quality while minimizing sensitive data retention.", "tags": ["response logging", "privacy"], "difficulty": 2},
        {"type": "matching", "prompt": "Match AI controls to the problem.", "pairs": [{"left": "Guardrail", "right": "Blocks or redirects unsafe output"}, {"left": "Evaluation", "right": "Measures quality on test cases"}, {"left": "Fallback", "right": "Handles low confidence or failure"}], "answer": {"Guardrail": "Blocks or redirects unsafe output", "Evaluation": "Measures quality on test cases", "Fallback": "Handles low confidence or failure"}, "explanation": "Production AI needs behavior controls and measurement, not just a prompt that works once.", "tags": ["guardrails", "evals"], "difficulty": 2},
        {"type": "scenario_choice", "prompt": "Latency and cost are too high for a summarization feature. Which trade-off might help?", "options": ["Use a smaller or quantized model and evaluate quality", "Increase max tokens forever", "Log all private inputs", "Remove tests"], "answer": "Use a smaller or quantized model and evaluate quality", "explanation": "Quantization or smaller models can reduce cost and latency, but may reduce accuracy. Evals decide whether the trade-off is acceptable.", "tags": ["quantization", "latency", "cost"], "difficulty": 3},
        {"type": "bug_hunt", "prompt": "A team ships an AI feature after trying five happy-path prompts manually. What is missing?", "options": ["A repeatable evaluation set", "A larger logo", "A read replica", "A Docker layer"], "answer": "A repeatable evaluation set", "explanation": "Manual prompt trials do not show regression risk. Evals provide repeatable quality checks across realistic cases.", "tags": ["evals", "quality"], "difficulty": 2},
        {"type": "scenario_choice", "prompt": "A user asks the assistant to reveal hidden system instructions. Which control should respond?", "options": ["Prompt-injection guardrail and refusal behavior", "Offset pagination", "Joined eager loading", "CSS reset"], "answer": "Prompt-injection guardrail and refusal behavior", "explanation": "AI systems should treat user text and retrieved text as untrusted input and enforce boundaries.", "tags": ["guardrails", "prompt injection"], "difficulty": 3},
        {"type": "ordering", "prompt": "Order a basic RAG request path.", "options": ["Embed the query", "Retrieve relevant chunks", "Build grounded prompt", "Generate and validate answer"], "answer": ["Embed the query", "Retrieve relevant chunks", "Build grounded prompt", "Generate and validate answer"], "explanation": "RAG first finds relevant context, then asks the model to answer from that context with validation around the result.", "tags": ["rag", "embeddings"], "difficulty": 2},
        {"type": "code_fill", "prompt": "Fill the retrieval similarity check.", "code": "if top_match.score < threshold:\n    return ____", "options": ["\"ask_for_clarification\"", "\"invent_answer\"", "\"ignore_sources\"", "\"delete_index\""], "answer": "\"ask_for_clarification\"", "explanation": "Low retrieval confidence should trigger clarification or fallback, not fabricated answers.", "tags": ["vector search", "fallback"], "difficulty": 2},
        {"type": "scenario_choice", "prompt": "A feature sends customer medical notes to a third-party model without review. What is the primary issue?", "options": ["Privacy and data-governance risk", "Better throughput", "Normal caching", "A harmless prompt detail"], "answer": "Privacy and data-governance risk", "explanation": "Sensitive data needs clear consent, minimization, retention policy, and vendor controls before model use.", "tags": ["privacy", "governance"], "difficulty": 3},
        {"type": "multi_select", "prompt": "Which metrics matter for AI integration readiness?", "options": ["Answer accuracy on evals", "Latency", "Cost per request", "Number of gradients in UI"], "answer": ["Answer accuracy on evals", "Latency", "Cost per request"], "explanation": "AI product quality is a trade-off among usefulness, speed, cost, and risk.", "tags": ["evaluation", "latency", "cost"], "difficulty": 2},
    ],
    "system-design": [
        {"type": "ordering", "prompt": "Order the first moves in a system design interview.", "options": ["Clarify functional requirements", "Clarify non-functional requirements", "Estimate scale/access patterns", "Choose APIs and data model"], "answer": ["Clarify functional requirements", "Clarify non-functional requirements", "Estimate scale/access patterns", "Choose APIs and data model"], "explanation": "Design choices should follow requirements, scale, and access patterns. Jumping to tools too early weakens the answer.", "tags": ["requirements", "access pattern"], "difficulty": 1},
        {"type": "matching", "prompt": "Match design requirement types.", "pairs": [{"left": "Functional", "right": "What the system does"}, {"left": "Latency", "right": "How fast it responds"}, {"left": "Availability", "right": "How often it can serve requests"}], "answer": {"Functional": "What the system does", "Latency": "How fast it responds", "Availability": "How often it can serve requests"}, "explanation": "Functional requirements define behavior; non-functional requirements define qualities and constraints.", "tags": ["functional requirements", "nonfunctional requirements"], "difficulty": 1},
        {"type": "scenario_choice", "prompt": "A timeline feed has many reads and fewer writes. Which design pressure comes first?", "options": ["Read access pattern and caching strategy", "Only color tokens", "Delete old APIs", "Use one table blindly"], "answer": "Read access pattern and caching strategy", "explanation": "Feed design is shaped by read/write ratio, fan-out, freshness needs, and cacheability.", "tags": ["feed", "cache"], "difficulty": 2},
        {"type": "scenario_choice", "prompt": "Writes arrive in bursts, and users do not need immediate processing. Which component helps?", "options": ["Queue", "Synchronous recursive call", "Browser cookie", "Swagger UI"], "answer": "Queue", "explanation": "Queues absorb bursts and decouple producers from workers, at the cost of delayed processing.", "tags": ["queue", "async"], "difficulty": 2},
        {"type": "matching", "prompt": "Match scale tools to bottlenecks.", "pairs": [{"left": "Cache", "right": "Repeated expensive reads"}, {"left": "Read replica", "right": "Read-heavy database load"}, {"left": "Partitioning", "right": "Data or write load too large for one node"}], "answer": {"Cache": "Repeated expensive reads", "Read replica": "Read-heavy database load", "Partitioning": "Data or write load too large for one node"}, "explanation": "Each scale pattern solves a different bottleneck; mixing them up creates complexity without capacity.", "tags": ["cache", "replica", "partition"], "difficulty": 2},
        {"type": "scenario_choice", "prompt": "A username must be unique globally during failover. What should you prioritize?", "options": ["Strong consistency for the uniqueness check", "Eventual consistency everywhere", "Client-side validation only", "A CDN cache"], "answer": "Strong consistency for the uniqueness check", "explanation": "Uniqueness is an invariant. Protect it with a strongly consistent path even if other parts can be eventually consistent.", "tags": ["consistency", "invariant"], "difficulty": 3},
        {"type": "scenario_choice", "prompt": "A like counter can be stale for a few seconds. Which trade-off is acceptable?", "options": ["Eventual consistency for higher availability/throughput", "Serializable transactions for every click", "Manual SQL only", "No database"], "answer": "Eventual consistency for higher availability/throughput", "explanation": "Counters and feeds often tolerate temporary staleness, which can reduce coordination and improve availability.", "tags": ["eventual consistency", "availability"], "difficulty": 2},
        {"type": "bug_hunt", "prompt": "A design says 'add cache' without defining invalidation or staleness. What is missing?", "options": ["Cache consistency strategy", "Button hover state", "More endpoints", "Less monitoring"], "answer": "Cache consistency strategy", "explanation": "Caches introduce stale data risk. A strong design names TTLs, invalidation, and correctness impact.", "tags": ["cache", "staleness"], "difficulty": 2},
        {"type": "multi_select", "prompt": "Which details belong in an API/data-model section?", "options": ["Core entities", "Read/write access patterns", "Important indexes", "Random frontend animation"], "answer": ["Core entities", "Read/write access patterns", "Important indexes"], "explanation": "Data models should be justified by how the API reads and writes the data.", "tags": ["api", "data model", "index"], "difficulty": 1},
        {"type": "ordering", "prompt": "Order a bottleneck-driven scaling answer.", "options": ["Name current bottleneck", "Pick targeted mitigation", "State new trade-off", "Measure result"], "answer": ["Name current bottleneck", "Pick targeted mitigation", "State new trade-off", "Measure result"], "explanation": "System design improves when every scale choice maps to a measured pressure and an explicit cost.", "tags": ["bottleneck", "trade-off"], "difficulty": 2},
        {"type": "scenario_choice", "prompt": "A service must keep accepting reads during a regional failure, but latest writes may lag. What are you trading?", "options": ["Availability over immediate consistency", "CSS over API design", "Serialization over security", "Unit tests over monitoring"], "answer": "Availability over immediate consistency", "explanation": "In failures, systems often trade freshness/consistency for availability. Name that trade-off directly.", "tags": ["availability", "consistency"], "difficulty": 3},
        {"type": "bug_hunt", "prompt": "A design stores all tenants in one partition by tenant_type, and enterprise traffic overloads one node. What failed?", "options": ["Bad partition key causing skew", "Too much OpenAPI", "A response model leak", "A missing CORS header"], "answer": "Bad partition key causing skew", "explanation": "Partition keys need enough cardinality and balanced traffic. Skewed keys create hot partitions.", "tags": ["partition", "hot shard"], "difficulty": 3},
    ],
})



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


CONCEPT_LIBRARY = {
    "dns": {
        "title": "DNS Resolution",
        "explanation": "DNS turns a human-readable domain into the IP address a client can connect to. It happens before the HTTP request is sent, so DNS failures look like connection failures rather than application bugs. In interviews, DNS is usually part of the browser-to-server lifecycle. The important mental model is that naming, connection setup, HTTP, and application logic are separate stages.",
        "takeaways": ["DNS resolves names before HTTP starts.", "DNS problems can prevent any request from reaching the server.", "Caching can make DNS behavior look inconsistent during changes."],
        "example": "A browser cannot call https://api.example.com until api.example.com resolves to an address.",
        "diagram": {"type": "flow", "title": "Request starts before HTTP", "nodes": [{"label": "Browser"}, {"label": "DNS lookup"}, {"label": "IP address"}, {"label": "Connect"}]},
        "insight": "whether you understand the web request lifecycle below application code.",
    },
    "tls": {
        "title": "HTTPS and TLS",
        "explanation": "HTTPS is HTTP carried over TLS. TLS encrypts traffic, authenticates the server, and protects message integrity. This matters because tokens, cookies, and private payloads can otherwise be read or modified in transit. A strong answer separates transport security from application authorization.",
        "takeaways": ["HTTPS encrypts traffic in transit.", "Certificates authenticate the server identity.", "TLS does not replace input validation or authorization."],
        "example": "A login cookie sent over plain HTTP can be stolen by a network observer.",
        "diagram": {"type": "flow", "title": "Secure request path", "nodes": [{"label": "Browser"}, {"label": "TLS handshake"}, {"label": "Encrypted HTTP"}, {"label": "API"}]},
        "insight": "whether you understand transport security and where it sits in the request path.",
    },
    "http": {
        "title": "HTTP Request and Response",
        "explanation": "HTTP is a request-response protocol. The client sends a method, URL, headers, and sometimes a body; the server returns a status code, headers, and response body. Interview questions often test whether you can separate intent from outcome. Methods express what the client wants; status codes express what happened.",
        "takeaways": ["Methods describe intent.", "Status codes describe outcomes.", "Headers carry metadata for auth, content type, caching, and negotiation."],
        "example": "GET /users/7 asks for a resource; 404 says that resource was not found.",
        "diagram": {"type": "flow", "title": "HTTP lifecycle", "nodes": [{"label": "Client"}, {"label": "Request"}, {"label": "Server"}, {"label": "Response"}]},
        "insight": "whether you can reason about client-server contracts instead of memorizing codes.",
    },
    "patch": {
        "title": "PATCH vs PUT",
        "explanation": "PUT normally means replacing the whole resource representation. PATCH means applying a partial update to selected fields. If the client only sends a new email, PATCH communicates the intended change without implying that omitted fields should be cleared. This is a contract question: the method should match the update semantics.",
        "takeaways": ["PUT is full replacement in conventional REST design.", "PATCH is partial update.", "Choosing the right method prevents accidental data loss."],
        "example": "PATCH /users/5 with {\"email\":\"new@example.com\"} updates only the email field.",
        "diagram": {"type": "compare", "title": "Update semantics", "columns": [{"title": "PUT", "items": ["Replace entire resource", "Missing fields may matter"]}, {"title": "PATCH", "items": ["Update selected fields", "Safer for partial edits"]}]},
        "insight": "whether you understand API semantics and resource-update contracts.",
    },
    "status code": {
        "title": "HTTP Status Codes",
        "explanation": "Status codes are compact signals about request outcomes. 2xx means success, 4xx means the client request has a problem, and 5xx means the server or dependency failed. The common interview trap is 401 vs 403: 401 means authentication is missing or invalid, while 403 means identity is known but access is denied.",
        "takeaways": ["2xx means success.", "4xx means client-side request problem.", "401 is authentication; 403 is authorization."],
        "example": "A logged-in user without admin permission should usually receive 403, not 401.",
        "diagram": {"type": "flow", "title": "Status code bands", "nodes": [{"label": "2xx success", "status": "good"}, {"label": "4xx client issue"}, {"label": "5xx server issue", "status": "hot"}]},
        "insight": "whether you can communicate API failures clearly to clients.",
    },
    "cors": {
        "title": "CORS and Origins",
        "explanation": "CORS is a browser security mechanism for cross-origin requests. An origin is the scheme, host, and port together, so localhost:5173 and localhost:8000 are different origins. The browser blocks the response unless the API explicitly allows the frontend origin. CORS does not protect server-to-server calls; it is enforced by browsers.",
        "takeaways": ["Origin means scheme plus host plus port.", "Browsers enforce CORS; servers declare allowed origins.", "CORS is not authentication."],
        "example": "A Vite frontend on localhost:5173 needs the FastAPI server on localhost:8000 to allow that origin.",
        "diagram": {"type": "network", "title": "Cross-origin browser call", "nodes": [{"id": "Browser", "label": "Browser"}, {"id": "API", "label": "API"}], "edges": [{"from": "Browser", "to": "API", "label": "Origin checked"}]},
        "insight": "whether you understand browser security boundaries.",
    },
    "session": {
        "title": "Cookies and Sessions",
        "explanation": "Cookies are small values stored by the browser and sent with matching requests. Sessions usually store user state on the server and use a session ID in a cookie to link the browser to that state. This distinction matters for security and scaling. The cookie is not the whole user record; it is usually a pointer or token.",
        "takeaways": ["Cookies live in the browser.", "Sessions usually live on the server.", "Session IDs connect the two."],
        "example": "A server stores cart state by session ID, while the browser only stores the session cookie.",
        "diagram": {"type": "flow", "title": "Session lookup", "nodes": [{"label": "Browser cookie"}, {"label": "Session ID"}, {"label": "Server session store"}, {"label": "User state"}]},
        "insight": "whether you understand state in stateless HTTP workflows.",
    },
    "grpc": {
        "title": "REST vs gRPC",
        "explanation": "REST usually exposes resources over HTTP with JSON and is easy for humans and browsers to inspect. gRPC uses Protocol Buffers over HTTP/2 and is often better for internal service-to-service APIs where generated clients and efficient binary payloads matter. The right answer depends on consumers, tooling, latency, and operability. Public APIs often favor REST; internal low-latency services may favor gRPC.",
        "takeaways": ["REST is resource-oriented and easy to inspect.", "gRPC is contract-first and efficient for internal services.", "Generated clients reduce drift but add tooling requirements."],
        "example": "A mobile app public API may use REST, while checkout and inventory services communicate with gRPC internally.",
        "diagram": {"type": "compare", "title": "API style trade-off", "columns": [{"title": "REST", "items": ["HTTP + JSON", "Human-friendly", "Broad tooling"]}, {"title": "gRPC", "items": ["HTTP/2 + Protobuf", "Generated clients", "Efficient internal calls"]}]},
        "insight": "whether you can choose API styles based on clients and operational constraints.",
    },
    "openapi": {
        "title": "API Contracts and OpenAPI",
        "explanation": "An API contract defines endpoints, inputs, outputs, status codes, and error shapes. OpenAPI is a machine-readable way to describe that contract, and Swagger UI is a common interface for exploring it. Contracts let frontend and backend teams work independently. Breaking changes should be versioned or rolled out carefully.",
        "takeaways": ["Contracts define request and response expectations.", "OpenAPI documents contracts in a structured format.", "Swagger UI is a viewer, not the contract itself."],
        "example": "FastAPI generates `/docs` from the OpenAPI schema so clients can inspect available endpoints.",
        "diagram": {"type": "flow", "title": "Contract workflow", "nodes": [{"label": "OpenAPI spec"}, {"label": "Swagger UI"}, {"label": "Client expectations"}, {"label": "Server implementation"}]},
        "insight": "whether you understand API reliability and client/server coordination.",
    },
    "idempotency": {
        "title": "Idempotency Keys",
        "explanation": "An idempotent operation can be repeated without changing the final result beyond the first attempt. POST is often not idempotent because it creates a new resource each time. If a payment request times out, the server may still have processed it; retrying without an idempotency key can charge twice. Idempotency keys let the server recognize a retry and return the original result.",
        "takeaways": ["Timeout does not prove failure.", "POST retries can duplicate work.", "Idempotency keys make unsafe retries safer."],
        "example": "POST /payments with Idempotency-Key: abc123 can return the first payment response when the client retries.",
        "diagram": {"type": "flow", "title": "Safe payment retry", "nodes": [{"label": "Client"}, {"label": "POST payment"}, {"label": "Timeout", "status": "hot"}, {"label": "Retry with key"}, {"label": "Return previous response", "status": "good"}]},
        "insight": "whether you understand API reliability under partial failure.",
    },
    "pagination": {
        "title": "Cursor vs Offset Pagination",
        "explanation": "Offset pagination skips a number of rows and is simple for stable datasets. Cursor pagination continues from a stable record marker, which is safer when rows are inserted or deleted while the user pages. Large offsets can also become expensive because the database still has to walk past skipped rows. Feeds and timelines usually prefer cursors.",
        "takeaways": ["Offset is simple but unstable on changing data.", "Cursor pagination follows a stable position.", "Cursor pagination usually fits large feeds better."],
        "example": "A feed ordered by created_at can use the last seen timestamp/id as the next cursor.",
        "diagram": {"type": "compare", "title": "Pagination behavior", "columns": [{"title": "Offset", "items": ["page=5", "Can skip/duplicate", "Can be expensive"]}, {"title": "Cursor", "items": ["after=item_123", "Stable continuation", "Good for feeds"]}]},
        "insight": "whether you understand API data access patterns at scale.",
    },
    "validation": {
        "title": "Input Validation Boundary",
        "explanation": "Validation rejects malformed or unsafe input before business logic runs. That keeps core logic simpler and produces predictable errors for clients. In typed frameworks, schemas can validate shape, types, ranges, and required fields automatically. Validation is not just correctness; it is also a security and maintainability boundary.",
        "takeaways": ["Validate before business logic.", "Schemas make errors predictable.", "Validation reduces security and data-quality risk."],
        "example": "A request with age=-10 should fail validation before creating a user.",
        "diagram": {"type": "flow", "title": "Request boundary", "nodes": [{"label": "Request"}, {"label": "Validation"}, {"label": "Service logic"}, {"label": "Database"}, {"label": "Response"}]},
        "insight": "whether you understand backend boundaries and defensive API design.",
    },
    "dependency injection": {
        "title": "Dependency Injection",
        "explanation": "Dependency injection supplies collaborators such as database sessions, settings, or services instead of constructing them inside the endpoint. This makes code easier to test because dependencies can be replaced. In FastAPI, `Depends` declares dependencies in endpoint signatures. The practical value is clear boundaries, not magic.",
        "takeaways": ["Dependencies are supplied from the outside.", "Tests can swap real dependencies for controlled ones.", "Endpoints stay focused on request handling."],
        "example": "A test can override `get_db` with a temporary SQLite session.",
        "diagram": {"type": "flow", "title": "Injected request dependency", "nodes": [{"label": "Request"}, {"label": "Depends(get_db)"}, {"label": "Endpoint"}, {"label": "Service"}]},
        "insight": "whether you can design testable backend components.",
    },
    "async": {
        "title": "Async, Concurrency, and Parallelism",
        "explanation": "Async helps a program make progress while waiting on I/O such as database calls or HTTP requests. It does not make CPU-heavy work faster by itself. Concurrency is about handling multiple tasks in overlapping time; parallelism is about running work at the same time on multiple CPU cores. Interviewers often test this because many candidates use `async` as a vague performance answer.",
        "takeaways": ["Async helps I/O-bound work.", "CPU-heavy work needs parallelism or workers.", "Concurrency and parallelism are different concepts."],
        "example": "Awaiting a slow API call lets the server process other requests while it waits.",
        "diagram": {"type": "compare", "title": "Workload fit", "columns": [{"title": "I/O-bound", "items": ["await database", "await HTTP", "async helps"]}, {"title": "CPU-bound", "items": ["image encode", "ML inference", "workers help"]}]},
        "insight": "whether you understand backend performance models.",
    },
    "index": {
        "title": "Database Indexes",
        "explanation": "An index is an extra data structure that lets the database find rows without scanning everything. Indexes are useful for frequent filters, joins, and ordering. They are not free: every write may need to update the index, and indexes consume storage. Good answers tie indexes to specific query patterns.",
        "takeaways": ["Indexes speed reads for matching access paths.", "Indexes add write and storage cost.", "Index choice should follow real queries."],
        "example": "A login query by email should usually have an index on users.email.",
        "diagram": {"type": "flow", "title": "Indexed lookup", "nodes": [{"label": "WHERE email=..."}, {"label": "Email index"}, {"label": "Row location"}, {"label": "User row"}]},
        "insight": "whether you understand SQL query performance trade-offs.",
    },
    "transaction": {
        "title": "Transactions and ACID",
        "explanation": "A transaction groups related database changes so they commit together or roll back together. ACID describes guarantees around atomicity, consistency, isolation, and durability. This matters when partial updates would corrupt business invariants, such as money transfers. Stronger transaction guarantees protect correctness but can reduce concurrency.",
        "takeaways": ["Atomicity means all-or-nothing changes.", "Isolation controls concurrent behavior.", "Use transactions to protect invariants."],
        "example": "Debit one account and credit another inside one transaction.",
        "diagram": {"type": "flow", "title": "Safe transaction", "nodes": [{"label": "Begin"}, {"label": "Debit"}, {"label": "Credit"}, {"label": "Commit or rollback"}]},
        "insight": "whether you understand data correctness under concurrent changes.",
    },
    "replica": {
        "title": "Replication and Replica Lag",
        "explanation": "Replication copies data from a primary or leader to follower replicas. It can improve read capacity and availability, but followers may lag behind recent writes. A user who writes to the leader and immediately reads from a lagging replica may see stale data. The design must decide which reads require freshness.",
        "takeaways": ["Replicas help read scale and availability.", "Replica lag creates stale-read risk.", "Read-your-writes may require leader reads or session-aware routing."],
        "example": "After updating a profile, route that user's next profile read to the leader until replicas catch up.",
        "diagram": {"type": "network", "title": "Leader replication", "nodes": [{"id": "Primary", "label": "Primary", "status": "good"}, {"id": "Replica A", "label": "Replica A"}, {"id": "Replica B", "label": "Replica B", "status": "hot"}], "edges": [{"from": "Primary", "to": "Replica A", "label": "fresh"}, {"from": "Primary", "to": "Replica B", "label": "lagging"}]},
        "insight": "whether you understand consistency trade-offs in replicated systems.",
    },
    "sharding": {
        "title": "Sharding and Hot Partitions",
        "explanation": "Sharding splits data across nodes so one machine does not hold all data or write load. The shard key decides where each record goes. A poor key can concentrate traffic on one shard and create a hot partition. Sharding increases capacity but makes routing, rebalancing, and cross-shard operations harder.",
        "takeaways": ["Sharding partitions data across nodes.", "Shard-key choice controls balance.", "Skew creates hot shards and operational pain."],
        "example": "Partitioning by tenant_type can overload the enterprise shard if enterprise tenants dominate traffic.",
        "diagram": {"type": "network", "title": "Shard-key skew", "nodes": [{"id": "Tenant A", "label": "Tenant A"}, {"id": "Shard 1", "label": "Shard 1", "status": "hot"}, {"id": "Tenant B", "label": "Tenant B"}, {"id": "Shard 2", "label": "Shard 2"}, {"id": "Tenant C", "label": "Tenant C"}, {"id": "Shard 3", "label": "Shard 3"}], "edges": [{"from": "Tenant A", "to": "Shard 1", "label": "heavy"}, {"from": "Tenant B", "to": "Shard 2"}, {"from": "Tenant C", "to": "Shard 3"}]},
        "insight": "whether you understand horizontal scaling and data distribution failures.",
    },
    "n+1": {
        "title": "N+1 Queries",
        "explanation": "N+1 happens when one query loads parent rows and then one additional query runs for each parent as code accesses a lazy relationship. Loading 100 users and reading `user.orders` in a loop can become 101 queries. SQLAlchemy loading options such as `selectinload` and `joinedload` fetch related data earlier. The fix depends on relationship size and query shape.",
        "takeaways": ["Lazy relationship access inside loops can explode query count.", "selectinload is often safer for collections.", "joinedload can be useful but may duplicate parent rows."],
        "example": "Use `select(User).options(selectinload(User.orders))` before looping over users and orders.",
        "diagram": {"type": "flow", "title": "N+1 pattern", "nodes": [{"label": "SELECT users"}, {"label": "Loop"}, {"label": "SELECT orders"}, {"label": "SELECT orders"}, {"label": "101 queries", "status": "hot"}, {"label": "selectinload", "status": "good"}]},
        "insight": "whether you understand ORM performance instead of treating the ORM as invisible.",
    },
    "selectinload": {
        "title": "SQLAlchemy Loading Strategies",
        "explanation": "SQLAlchemy relationships can load lazily or eagerly. Lazy loading waits until the attribute is accessed, which can create N+1 queries. `selectinload` performs a second SELECT for related rows and is often a good fit for collections. `joinedload` uses a JOIN and can be efficient for smaller relationships but may duplicate parent data in large collection results.",
        "takeaways": ["Lazy loading can hide database work.", "selectinload often fits one-to-many collections.", "joinedload trades fewer round trips for larger joined result sets."],
        "example": "`select(User).options(selectinload(User.orders))` loads users and their orders without one query per user.",
        "diagram": {"type": "compare", "title": "Eager loading choice", "columns": [{"title": "selectinload", "items": ["Second SELECT", "Good for collections", "Avoids huge JOIN rows"]}, {"title": "joinedload", "items": ["Single JOIN", "Good for small related data", "Can duplicate parent rows"]}]},
        "insight": "whether you can diagnose SQLAlchemy query behavior in production.",
    },
    "testing": {
        "title": "Testing Scope",
        "explanation": "Different tests answer different questions. Unit tests verify small logic in isolation; integration tests verify boundaries such as API plus database; end-to-end tests verify user workflows. Good test strategy uses the cheapest test that catches the failure mode. Coverage is useful, but meaningful assertions matter more than line counts.",
        "takeaways": ["Unit tests are fast and narrow.", "Integration tests verify real boundaries.", "Coverage does not prove correctness by itself."],
        "example": "A pure XP formula should be unit-tested; an API route writing to SQLite deserves an integration test.",
        "diagram": {"type": "flow", "title": "Test pyramid", "nodes": [{"label": "Unit: fast"}, {"label": "Integration: boundaries"}, {"label": "E2E: full workflow"}]},
        "insight": "whether you can choose tests based on risk and feedback speed.",
    },
    "cache": {
        "title": "Caching",
        "explanation": "A cache stores previously computed or fetched data so repeated reads avoid expensive work. Caching improves latency and reduces load, but introduces staleness and invalidation problems. You should cache data that is read often, expensive to compute, and safe to serve slightly stale. Always explain cache hit, cache miss, TTL, and invalidation.",
        "takeaways": ["Cache hits avoid database or service work.", "Cache misses still need the source of truth.", "Invalidation and staleness are the main trade-offs."],
        "example": "A product catalog can be cached in Redis with a TTL if updates are infrequent.",
        "diagram": {"type": "flow", "title": "Cache hit/miss", "nodes": [{"label": "Client"}, {"label": "Redis cache"}, {"label": "Hit: return", "status": "good"}, {"label": "Miss: database"}, {"label": "Store result"}]},
        "insight": "whether you understand performance trade-offs and stale-data risk.",
    },
    "timeout": {
        "title": "Timeouts, Retries, and Backoff",
        "explanation": "Timeouts bound how long a caller waits for a dependency. A timeout leaves the outcome unknown: the downstream operation may still complete. Retries can help transient failures, but they need limits, jitter, and exponential backoff to avoid retry storms. The best design combines timeouts, idempotency, and observability.",
        "takeaways": ["Timeout means unknown outcome, not guaranteed failure.", "Retries need backoff and limits.", "Unsafe operations need idempotency before retrying."],
        "example": "Retry a payment POST only with an idempotency key and a bounded retry policy.",
        "diagram": {"type": "flow", "title": "Retry safely", "nodes": [{"label": "Call dependency"}, {"label": "Timeout", "status": "hot"}, {"label": "Backoff + jitter"}, {"label": "Retry if safe"}, {"label": "Reconcile"}]},
        "insight": "whether you understand reliability under partial failure.",
    },
    "circuit breaker": {
        "title": "Circuit Breakers",
        "explanation": "A circuit breaker stops sending requests to a dependency that is repeatedly failing. Instead of tying up resources with calls likely to fail, the service fails fast or uses fallback behavior. After a cool-down period, it probes to see whether the dependency has recovered. This protects both the caller and the struggling dependency.",
        "takeaways": ["Circuit breakers prevent repeated failing calls.", "Fail-fast behavior protects resources.", "Recovery usually uses limited probe requests."],
        "example": "If the payment provider returns errors for a sustained window, open the circuit and show a retry-later response.",
        "diagram": {"type": "flow", "title": "Circuit states", "nodes": [{"label": "Closed"}, {"label": "Failures rise", "status": "hot"}, {"label": "Open"}, {"label": "Probe"}, {"label": "Closed again", "status": "good"}]},
        "insight": "whether you understand cascading failure prevention.",
    },
    "queue": {
        "title": "Queues and Backpressure",
        "explanation": "A queue decouples producers from workers. It smooths bursts by storing work until consumers can process it, which improves resilience but adds delay. Queues are useful when immediate completion is not required. The design must handle retries, duplicates, dead-letter queues, and visibility into lag.",
        "takeaways": ["Queues smooth bursty writes.", "Async processing trades immediacy for resilience.", "Consumer lag and duplicate handling matter."],
        "example": "Send email jobs to a queue so signup responses do not wait for the email provider.",
        "diagram": {"type": "flow", "title": "Queued work", "nodes": [{"label": "API"}, {"label": "Queue"}, {"label": "Worker"}, {"label": "External service"}]},
        "insight": "whether you understand async system design and backpressure.",
    },
    "observability": {
        "title": "Logs, Metrics, and Traces",
        "explanation": "Observability gives evidence about production behavior. Logs explain specific events, metrics show trends and rates, and traces follow one request across services. Good incident answers use these signals to narrow the problem instead of guessing. Observability should be designed before the system is failing.",
        "takeaways": ["Logs explain individual events.", "Metrics reveal trends, rates, and percentiles.", "Traces expose cross-service latency and failures."],
        "example": "A slow checkout trace can show that inventory, not payments, dominates latency.",
        "diagram": {"type": "compare", "title": "Production signals", "columns": [{"title": "Logs", "items": ["What happened", "Errors", "Context"]}, {"title": "Metrics/Traces", "items": ["How often", "How slow", "Where time went"]}]},
        "insight": "whether you can debug production systems with evidence.",
    },
    "docker": {
        "title": "Docker Images and Containers",
        "explanation": "A Dockerfile describes how to build an image. An image packages the application filesystem and metadata, while a container is a running instance of that image. Good Docker usage makes runtime dependencies explicit and reproducible. If a container depends on undeclared host files, the image is not self-contained.",
        "takeaways": ["Dockerfile builds an image.", "A container runs from an image.", "Reproducibility depends on declared dependencies."],
        "example": "Copy requirements.txt, install dependencies, then copy app code to improve layer caching.",
        "diagram": {"type": "flow", "title": "Container artifact path", "nodes": [{"label": "Dockerfile"}, {"label": "Image"}, {"label": "Container"}, {"label": "Running app"}]},
        "insight": "whether you understand reproducible deployment artifacts.",
    },
    "ci": {
        "title": "CI/CD Pipelines",
        "explanation": "CI validates changes automatically with tests, type checks, and builds. CD deploys a validated artifact to an environment. The important principle is that the artifact you deploy should be traceable to the code that passed checks. Deployment health checks and rollbacks limit blast radius when a bad version escapes.",
        "takeaways": ["CI catches broken changes before merge/deploy.", "CD should deploy a known artifact.", "Health checks and rollback make releases safer."],
        "example": "A pipeline installs dependencies, runs tests, builds an artifact, then deploys it with health checks.",
        "diagram": {"type": "flow", "title": "Release pipeline", "nodes": [{"label": "Commit"}, {"label": "Tests"}, {"label": "Build artifact"}, {"label": "Deploy"}, {"label": "Health check"}]},
        "insight": "whether you understand deployment safety and operational traceability.",
    },
    "ai": {
        "title": "Production AI Integration",
        "explanation": "AI features are product systems, not just prompts. They need data handling, retrieval when facts matter, evaluation, latency/cost controls, privacy decisions, and fallback behavior. LLMs can hallucinate, so systems should ground answers in sources and measure quality repeatedly. The right architecture depends on risk and freshness requirements.",
        "takeaways": ["RAG helps with changing factual knowledge.", "Evals catch quality regressions.", "Privacy and observability must be designed up front."],
        "example": "A support assistant retrieves policy chunks, builds a grounded prompt, validates the answer, and logs document IDs for review.",
        "diagram": {"type": "flow", "title": "AI request path", "nodes": [{"label": "User query"}, {"label": "Retrieve context"}, {"label": "Prompt model"}, {"label": "Validate"}, {"label": "Answer"}]},
        "insight": "whether you can design AI features as reliable software systems.",
    },
    "rag": {
        "title": "Retrieval-Augmented Generation",
        "explanation": "RAG retrieves relevant source material before asking a model to answer. Embeddings turn text into vectors so semantic search can find related chunks. RAG is useful when facts change or must be grounded in private documents. Low retrieval confidence should trigger clarification or fallback rather than invented answers.",
        "takeaways": ["Embeddings power semantic retrieval.", "Retrieved context grounds the model answer.", "Low confidence needs fallback behavior."],
        "example": "Retrieve the latest refund policy before generating a customer-support answer.",
        "diagram": {"type": "flow", "title": "RAG pipeline", "nodes": [{"label": "Embed query"}, {"label": "Vector search"}, {"label": "Retrieve chunks"}, {"label": "Grounded prompt"}, {"label": "Validated answer"}]},
        "insight": "whether you understand AI correctness, freshness, and hallucination control.",
    },
    "quantization": {
        "title": "Model Quantization Trade-off",
        "explanation": "Quantization reduces the precision of model weights or activations so the model uses less memory and may run faster. The trade-off is that quality can drop, especially on harder tasks. Production teams should evaluate accuracy, latency, and cost together before choosing a quantized model. It is an engineering trade-off, not a universal upgrade.",
        "takeaways": ["Quantization can reduce memory and latency.", "Quality may decrease.", "Evals decide whether the trade-off is acceptable."],
        "example": "A smaller quantized summarizer may meet latency targets but needs evaluation against full-precision output.",
        "diagram": {"type": "compare", "title": "Model trade-off", "columns": [{"title": "Full precision", "items": ["Higher quality", "More memory", "Higher cost"]}, {"title": "Quantized", "items": ["Lower memory", "Lower latency", "Possible quality loss"]}]},
        "insight": "whether you can reason about AI system performance trade-offs.",
    },
    "requirements": {
        "title": "System Design Requirements",
        "explanation": "System design starts by clarifying what the system must do and what qualities it must have. Functional requirements describe behavior; non-functional requirements describe scale, latency, availability, durability, privacy, and cost constraints. Good designs tie APIs and data models to access patterns. Jumping to tools before requirements usually produces weak answers.",
        "takeaways": ["Clarify functional requirements first.", "Non-functional requirements drive architecture.", "Access patterns shape APIs and data models."],
        "example": "A feed service design changes depending on read/write ratio, freshness needs, and fan-out size.",
        "diagram": {"type": "flow", "title": "Design interview opening", "nodes": [{"label": "Functional reqs"}, {"label": "NFRs"}, {"label": "Scale/access patterns"}, {"label": "API + data model"}, {"label": "Trade-offs"}]},
        "insight": "whether you can turn vague product goals into concrete engineering constraints.",
    },
    "consistency": {
        "title": "Consistency vs Availability",
        "explanation": "Consistency describes what reads are allowed to observe after writes. Some invariants, like unique usernames or bank balances, need strong consistency. Other values, like social counters, can often be eventually consistent. During failures, stronger consistency may reduce availability because coordination is required.",
        "takeaways": ["Use strong consistency for hard invariants.", "Eventual consistency can fit counters and feeds.", "Consistency choices trade off with latency and availability."],
        "example": "A like count can lag briefly, but a payment ledger should not accept conflicting balances.",
        "diagram": {"type": "triangle", "title": "CAP pressure", "points": [{"label": "Consistency"}, {"label": "Availability"}, {"label": "Partition tolerance"}]},
        "insight": "whether you can choose guarantees based on business invariants.",
    },
    "lsm": {
        "title": "LSM Trees and SSTables",
        "explanation": "LSM-style storage writes data to an in-memory memtable and append-only logs, then flushes sorted immutable files called SSTables. Compaction later merges files and removes obsolete entries. This design can be strong for write-heavy workloads but may add read amplification. The interview point is understanding the read/write trade-off in storage engines.",
        "takeaways": ["Memtables absorb writes in memory.", "SSTables are sorted immutable files.", "Compaction trades background work for efficient storage."],
        "example": "A write-heavy event store may favor an LSM engine, while a read-heavy index lookup may favor B-tree behavior.",
        "diagram": {"type": "flow", "title": "LSM write path", "nodes": [{"label": "Write"}, {"label": "Memtable"}, {"label": "Flush"}, {"label": "SSTable"}, {"label": "Compaction"}]},
        "insight": "whether you understand storage-engine trade-offs beyond SQL syntax.",
    },
    "schema": {
        "title": "Schema Evolution",
        "explanation": "Schema evolution is the ability to change stored or transmitted data formats without breaking old readers or writers. Backward compatibility means new code can read old data; forward compatibility means old code can tolerate new data. Rolling upgrades require both versions to coexist. Formats such as JSON are easy to inspect; schema-based formats such as Avro can enforce compatibility through a registry.",
        "takeaways": ["Backward and forward compatibility protect rolling deploys.", "Optional fields are safer than new required fields.", "Schema registries can block incompatible messages."],
        "example": "Add an optional field, deploy readers first, then deploy writers that populate it.",
        "diagram": {"type": "flow", "title": "Compatible rollout", "nodes": [{"label": "Add optional field"}, {"label": "Deploy readers"}, {"label": "Deploy writers"}, {"label": "Remove old field later"}]},
        "insight": "whether you understand evolvability in long-lived data systems.",
    },
    "consensus": {
        "title": "Consensus, Safety, and Liveness",
        "explanation": "Consensus lets nodes agree on a value or leader despite failures. Safety means bad outcomes do not happen, such as two leaders both accepting writes. Liveness means the system eventually makes progress when conditions allow. Strong consistency and leader election require coordination, which costs latency and availability under partitions.",
        "takeaways": ["Consensus is about agreement under failure.", "Safety prevents invalid outcomes.", "Liveness is about eventual progress."],
        "example": "A scheduler uses leader election so only one node runs a job at a time.",
        "diagram": {"type": "triangle", "title": "Consensus tension", "points": [{"label": "Agreement"}, {"label": "Safety"}, {"label": "Liveness"}]},
        "insight": "whether you understand distributed coordination guarantees.",
    },
    "stream": {
        "title": "Stream Processing",
        "explanation": "Stream processing handles events continuously instead of waiting for a bounded batch. Consumers track offsets, maintain state, and handle duplicates or late events. Windows group events over time, and watermarks estimate when event-time input is complete enough to emit results. Delivery semantics define whether duplicates or loss are possible.",
        "takeaways": ["Offsets track consumer progress.", "Windows and watermarks handle time-based aggregation.", "Delivery semantics determine duplicate/loss risk."],
        "example": "A clickstream job counts clicks per minute while accepting that late events may update the window.",
        "diagram": {"type": "flow", "title": "Streaming pipeline", "nodes": [{"label": "Event log"}, {"label": "Consumer"}, {"label": "State/window"}, {"label": "Commit offset"}, {"label": "Derived result"}]},
        "insight": "whether you understand continuous data processing correctness.",
    },
    "batch": {
        "title": "Batch Processing",
        "explanation": "Batch processing runs finite jobs over bounded input, often from stable snapshots. It favors throughput, reproducibility, and recomputation over low latency. MapReduce-style systems map records, shuffle by key, and reduce grouped data. Outputs should be idempotent so rerunning a job does not double-count results.",
        "takeaways": ["Batch jobs process bounded input.", "Snapshots make recomputation reproducible.", "Idempotent output protects retries and backfills."],
        "example": "A nightly analytics report can rebuild materialized views from immutable source events.",
        "diagram": {"type": "flow", "title": "Batch dataflow", "nodes": [{"label": "Snapshot input"}, {"label": "Map"}, {"label": "Shuffle by key"}, {"label": "Reduce"}, {"label": "Materialized view"}]},
        "insight": "whether you understand derived data and reproducible computation.",
    },
    "privacy": {
        "title": "Responsible Data Use",
        "explanation": "Data is both value and risk. Responsible systems define why data is collected, how long it is retained, who can access it, and how access is audited. Privacy, consent, deletion, and security requirements should be part of design rather than afterthoughts. Keeping everything forever because storage is cheap creates legal and human risk.",
        "takeaways": ["Collect only data needed for a defined purpose.", "Retention and deletion policies limit risk.", "Auditability and access control make use accountable."],
        "example": "Sensitive production data access should require permission, logging, and a clear business purpose.",
        "diagram": {"type": "flow", "title": "Data responsibility path", "nodes": [{"label": "Purpose"}, {"label": "Minimize"}, {"label": "Protect"}, {"label": "Audit"}, {"label": "Delete"}]},
        "insight": "whether you understand ethics, privacy, and governance in data systems.",
    },
}

CONCEPT_LIBRARY.update({
    "backend-frameworks": {
        "title": "Backend Framework Trade-offs",
        "explanation": "Backend frameworks provide routing, request parsing, response generation, and extension points. FastAPI emphasizes Python type hints, Pydantic validation, async support, and generated OpenAPI docs. Flask is smaller and more flexible, while Express is the lightweight Node.js equivalent and NestJS adds more structure for TypeScript teams. The best framework choice depends on team language, project size, validation needs, and operational conventions.",
        "takeaways": ["Frameworks shape routing and request handling.", "FastAPI is strong for typed Python APIs.", "Express is lightweight; NestJS is more structured."],
        "example": "Choose FastAPI when Python typing and automatic OpenAPI docs are useful; choose Express for a small Node API.",
        "diagram": {"type": "compare", "title": "Framework fit", "columns": [{"title": "FastAPI/Flask", "items": ["Python", "Validation/docs", "Flexible service size"]}, {"title": "Express/NestJS", "items": ["Node/TypeScript", "Lightweight vs structured", "Web API ecosystem"]}]},
        "insight": "whether you can choose backend tools based on constraints rather than popularity.",
    },
    "relational-nosql": {
        "title": "Relational vs NoSQL Databases",
        "explanation": "Relational databases organize data into tables with schemas, keys, constraints, and joins. NoSQL systems trade some relational structure for document flexibility, in-memory speed, high write volume, or specialized access patterns. PostgreSQL is a strong default for relational workloads; MongoDB fits document-shaped data; Redis is usually a fast cache or ephemeral store. The interview skill is matching data shape and correctness needs to the storage model.",
        "takeaways": ["Relational databases fit joins and constraints.", "Document stores fit flexible nested records.", "Redis is usually used for fast cache/session access."],
        "example": "Orders that reference users and need financial reports are usually a relational fit.",
        "diagram": {"type": "compare", "title": "Storage model fit", "columns": [{"title": "Relational", "items": ["Tables", "Keys", "JOINs"]}, {"title": "NoSQL", "items": ["Documents/cache", "Flexible shape", "Access-pattern driven"]}]},
        "insight": "whether you can choose storage based on data shape and guarantees.",
    },
    "relational-keys": {
        "title": "Keys, Relationships, and JOINs",
        "explanation": "Primary keys uniquely identify rows, and foreign keys connect rows across tables. JOINs combine related rows so normalized data can answer richer questions. Many-to-many relationships usually need a junction table. This is foundational because database schema design determines both correctness and query performance.",
        "takeaways": ["Primary keys identify rows.", "Foreign keys model relationships.", "JOINs reconstruct related data at query time."],
        "example": "orders.user_id references users.id, letting a query join orders to the owning user.",
        "diagram": {"type": "network", "title": "Relational link", "nodes": [{"id": "users", "label": "users"}, {"id": "orders", "label": "orders"}, {"id": "order_items", "label": "order_items"}], "edges": [{"from": "orders", "to": "users", "label": "foreign key"}, {"from": "order_items", "to": "orders", "label": "foreign key"}]},
        "insight": "whether you understand relational modeling, not just SQL syntax.",
    },
    "orm-session": {
        "title": "SQLAlchemy Session and Unit of Work",
        "explanation": "A SQLAlchemy Session tracks objects, pending changes, and the transaction boundary for a unit of work. Calling `add` marks an object for persistence; `flush` sends SQL without committing; `commit` completes the transaction. Sessions should usually be scoped per request in web apps so identity maps and transaction state do not leak. This concept is different from browser sessions.",
        "takeaways": ["Session tracks ORM object state.", "flush sends SQL inside the transaction.", "Web apps should avoid one global shared Session."],
        "example": "Create a user, add it to the request-scoped session, flush to get its ID, then commit.",
        "diagram": {"type": "flow", "title": "Unit of work", "nodes": [{"label": "Create object"}, {"label": "Session.add"}, {"label": "Flush SQL"}, {"label": "Commit"}]},
        "insight": "whether you understand ORM persistence boundaries and transaction scope.",
    },
    "sqlalchemy-migrations": {
        "title": "Schema Migrations",
        "explanation": "Migrations are versioned database schema changes. In SQLAlchemy projects, Alembic is commonly used to create, review, apply, and roll back those changes. Migrations make schema evolution repeatable across local, test, and production databases. They are operational artifacts, not just generated files.",
        "takeaways": ["Migrations version schema changes.", "Alembic is common with SQLAlchemy.", "Rollback plans reduce deployment risk."],
        "example": "Add a nullable column in one migration, deploy readers, then later enforce constraints when writers are ready.",
        "diagram": {"type": "flow", "title": "Migration lifecycle", "nodes": [{"label": "Model change"}, {"label": "Migration file"}, {"label": "Review"}, {"label": "Apply"}, {"label": "Rollback if needed"}]},
        "insight": "whether you understand production schema evolution.",
    },
    "raw-sql": {
        "title": "Raw SQL Escape Hatches",
        "explanation": "ORMs cover common queries, but complex reporting, database-specific features, or performance-critical paths may need raw SQL. Raw SQL should still use parameters rather than string interpolation, otherwise user input can become SQL injection. The point is not avoiding ORMs; it is knowing when to step below the abstraction safely.",
        "takeaways": ["Raw SQL can be appropriate for complex queries.", "Always parameterize user input.", "Measure before replacing ORM queries."],
        "example": "Use a parameterized SQL statement for a database-specific reporting query that the ORM expresses poorly.",
        "diagram": {"type": "flow", "title": "Safe raw SQL", "nodes": [{"label": "Complex query"}, {"label": "Parameterized SQL"}, {"label": "Database"}, {"label": "Typed result"}]},
        "insight": "whether you can use lower-level database tools safely.",
    },
    "latency-throughput": {
        "title": "Latency, Throughput, and Tail Latency",
        "explanation": "Latency is how long one operation takes. Throughput is how many operations complete per unit of time. Percentiles such as p95 and p99 reveal the slow tail that averages hide. Systems can have acceptable average latency while still hurting users at the tail.",
        "takeaways": ["Latency measures time per request.", "Throughput measures capacity over time.", "p95/p99 expose slow user experiences hidden by averages."],
        "example": "A checkout endpoint averaging 120 ms can still be bad if p99 is 4 seconds.",
        "diagram": {"type": "compare", "title": "Performance signals", "columns": [{"title": "Average", "items": ["Simple", "Can hide outliers"]}, {"title": "p95/p99", "items": ["Shows tail", "Closer to user pain"]}]},
        "insight": "whether you can measure performance in user-visible terms.",
    },
    "rate-limiting": {
        "title": "Rate Limiting",
        "explanation": "Rate limiting caps how much traffic a client, user, or API key can send. It protects shared resources from abuse, accidental loops, and noisy neighbors. Rate limits should return clear errors and may include retry-after information. They are part of reliability and fairness, not only security.",
        "takeaways": ["Rate limits protect shared capacity.", "Limits are usually per client, user, token, or IP.", "Clear retry behavior improves client reliability."],
        "example": "Allow 100 requests per minute per API key and return 429 when exceeded.",
        "diagram": {"type": "flow", "title": "Rate-limit gate", "nodes": [{"label": "Client"}, {"label": "Rate limiter"}, {"label": "Allowed", "status": "good"}, {"label": "429 Too Many Requests", "status": "hot"}]},
        "insight": "whether you understand API protection and fairness under load.",
    },
    "runtime-config": {
        "title": "Runtime Configuration",
        "explanation": "Runtime configuration changes between environments without changing code. Database URLs, feature switches, API endpoints, and secrets should be injected through environment or secret management rather than hardcoded. This makes the same build artifact usable in dev, test, and production. Configuration discipline reduces accidental production mistakes.",
        "takeaways": ["Configuration should vary by environment.", "Code should not hardcode deployment-specific values.", "Secrets need secret handling, not source control."],
        "example": "Set `DATABASE_URL` differently in local development and production deployment.",
        "diagram": {"type": "flow", "title": "Same artifact, different config", "nodes": [{"label": "Build artifact"}, {"label": "Dev env vars"}, {"label": "Prod env vars"}, {"label": "Runtime app"}]},
        "insight": "whether you understand deployable software configuration.",
    },
    "release-safety": {
        "title": "Deployment Safety",
        "explanation": "Deployment safety limits blast radius and makes failure reversible. Health checks stop bad releases, canaries expose changes to limited traffic, feature flags decouple deployment from release, and rollbacks return to a known-good version. The important idea is proving the new version works before trusting it with all traffic.",
        "takeaways": ["Health checks gate rollout.", "Canaries reduce blast radius.", "Rollbacks require traceable versions."],
        "example": "Deploy to 5 percent of traffic, watch errors and latency, then continue or roll back.",
        "diagram": {"type": "flow", "title": "Safe rollout", "nodes": [{"label": "Build"}, {"label": "Canary"}, {"label": "Health check"}, {"label": "Full rollout"}, {"label": "Rollback path"}]},
        "insight": "whether you understand production release risk.",
    },
    "secrets": {
        "title": "Secret Management",
        "explanation": "Secrets are credentials such as API keys, database passwords, and signing keys. They should not be committed to source control because repository history is hard to erase and access is broad. Use environment-backed secret stores or local ignored files, and rotate leaked secrets. Treat secrets as operational risk.",
        "takeaways": ["Never commit secrets to source control.", "Use environment or secret management.", "Rotate any exposed credential."],
        "example": "Move a committed API key into a secret store and revoke the old key.",
        "diagram": {"type": "flow", "title": "Secret handling", "nodes": [{"label": "Secret store"}, {"label": "Runtime env"}, {"label": "Application"}, {"label": "No source commit", "status": "good"}]},
        "insight": "whether you understand operational security basics.",
    },
    "artifact-traceability": {
        "title": "Build Artifact Traceability",
        "explanation": "A deployable artifact should be tied to the commit, checks, and environment that produced it. Without artifact traceability, debugging and rollback become guesswork. CI/CD pipelines should deploy the same artifact that passed validation. This is especially important when a bug appears only after deployment.",
        "takeaways": ["Know exactly what version is running.", "Deploy the artifact that passed checks.", "Traceability makes rollback and debugging reliable."],
        "example": "Attach commit SHA and build ID to every deployed release and log them at startup.",
        "diagram": {"type": "flow", "title": "Traceable release", "nodes": [{"label": "Commit SHA"}, {"label": "CI checks"}, {"label": "Artifact ID"}, {"label": "Deployment"}, {"label": "Rollback"}]},
        "insight": "whether you understand release provenance and production debugging.",
    },
    "data-models": {
        "title": "Data Models and Query Languages",
        "explanation": "Data models shape how information is stored, related, and queried. Relational models are strong for normalized data, joins, constraints, and ad hoc querying. Document models keep related data together for one access pattern but can introduce duplication. Graph models fit dense relationships and traversals. The right model follows access patterns and consistency needs.",
        "takeaways": ["Relational models favor joins and constraints.", "Document models favor locality and flexible shape.", "Denormalization speeds reads but creates consistency work."],
        "example": "A product catalog with flexible attributes may fit documents, while orders, users, and payments often need relational constraints.",
        "diagram": {"type": "compare", "title": "Model trade-offs", "columns": [{"title": "Relational", "items": ["Joins", "Constraints", "Ad hoc queries"]}, {"title": "Document/Graph", "items": ["Locality or traversal", "Flexible shape", "Duplication trade-offs"]}]},
        "insight": "whether you can model data around access patterns and invariants.",
    },
    "architecture-tradeoffs": {
        "title": "Data System Trade-offs",
        "explanation": "Data-system architecture is about choosing explicit trade-offs under known constraints. Reliability, scalability, maintainability, operability, latency, and throughput all pull in different directions. Cloud services, self-hosting, serverless, and microservices shift who owns operational complexity. Strong answers define the workload and guarantee before naming a tool.",
        "takeaways": ["Start with workload and guarantees.", "Every architecture choice moves complexity somewhere.", "Systems of record need stronger protection than derived data."],
        "example": "A cache can improve latency but creates invalidation and stale-read questions.",
        "diagram": {"type": "flow", "title": "Trade-off reasoning", "nodes": [{"label": "Workload"}, {"label": "Guarantee"}, {"label": "Tool choice"}, {"label": "Cost"}, {"label": "Measure"}]},
        "insight": "whether you can make architectural trade-offs explicit.",
    },
    "nfrs": {
        "title": "Nonfunctional Requirements",
        "explanation": "Nonfunctional requirements describe how well the system must behave: latency, availability, durability, security, operability, and evolvability. They become useful when stated as measurable SLOs or constraints. Averages are not enough for latency because users feel tail behavior. NFRs drive architecture decisions more than technology preference.",
        "takeaways": ["NFRs must be measurable.", "p95 and p99 expose tail latency.", "Security, operability, and evolvability are design constraints."],
        "example": "Define p99 latency under expected load before deciding whether to add caching or replication.",
        "diagram": {"type": "compare", "title": "NFR checklist", "columns": [{"title": "User-visible", "items": ["Latency", "Availability", "Durability"]}, {"title": "Operational", "items": ["Security", "Operability", "Evolvability"]}]},
        "insight": "whether you can translate product expectations into measurable engineering targets.",
    },
    "distributed-failure": {
        "title": "Partial Failure in Distributed Systems",
        "explanation": "Distributed systems can fail partially: one node may be alive while the network drops messages, pauses a process, or delays responses. A timeout means the result is unknown, not definitely failed. Retries can duplicate work unless operations are idempotent. Leases need fencing tokens because paused processes can resume after their authority expired.",
        "takeaways": ["Timeouts leave outcomes uncertain.", "Retries require idempotency or reconciliation.", "Fencing tokens protect against stale lease holders."],
        "example": "A payment request times out but later succeeds, so a retry without an idempotency key can double-charge.",
        "diagram": {"type": "flow", "title": "Partial failure path", "nodes": [{"label": "Send request"}, {"label": "Network delay"}, {"label": "Timeout", "status": "hot"}, {"label": "Unknown outcome"}, {"label": "Retry/reconcile"}]},
        "insight": "whether you understand distributed systems failures and uncertainty.",
    },
})


CONCEPT_ALIASES = {
    "https": "tls",
    "headers": "http",
    "request": "http",
    "response": "http",
    "method": "patch",
    "put": "patch",
    "401": "status code",
    "403": "status code",
    "cookies": "session",
    "sessions": "session",
    "api contract": "openapi",
    "swagger": "openapi",
    "versioning": "openapi",
    "serialization": "openapi",
    "deserialization": "openapi",
    "cursor": "pagination",
    "offset": "pagination",
    "filtering": "pagination",
    "sorting": "pagination",
    "retry": "idempotency",
    "fastapi": "dependency injection",
    "pydantic": "validation",
    "middleware": "validation",
    "router": "validation",
    "background tasks": "async",
    "parallelism": "async",
    "concurrency": "async",
    "acid": "transaction",
    "primary key": "index",
    "foreign key": "index",
    "join": "index",
    "replication lag": "replica",
    "read-your-writes": "replica",
    "monotonic reads": "replica",
    "partition": "sharding",
    "hot shard": "sharding",
    "selectinload": "selectinload",
    "joinedload": "selectinload",
    "loading": "selectinload",
    "pytest": "testing",
    "fixture": "testing",
    "mock": "testing",
    "coverage": "testing",
    "tdd": "testing",
    "rate limit": "timeout",
    "backoff": "timeout",
    "tail latency": "timeout",
    "p95": "timeout",
    "p99": "timeout",
    "logs": "observability",
    "metrics": "observability",
    "traces": "observability",
    "graceful degradation": "circuit breaker",
    "dockerfile": "docker",
    "image": "docker",
    "container": "docker",
    "compose": "docker",
    "environment variable": "ci",
    "deployment": "ci",
    "rollback": "ci",
    "health check": "ci",
    "llm": "ai",
    "embedding": "rag",
    "vector search": "rag",
    "hallucination": "rag",
    "guardrails": "rag",
    "evals": "ai",
    "evaluation": "ai",
    "cost": "quantization",
    "functional requirements": "requirements",
    "nonfunctional requirements": "requirements",
    "access pattern": "requirements",
    "bottleneck": "requirements",
    "availability": "consistency",
    "eventual consistency": "consistency",
    "strong consistency": "consistency",
    "b-tree": "index",
    "sstable": "lsm",
    "log-structured": "lsm",
    "schema evolution": "schema",
    "json": "schema",
    "avro": "schema",
    "leader election": "consensus",
    "safety": "consensus",
    "liveness": "consensus",
    "delivery semantics": "stream",
    "streaming": "stream",
    "watermark": "stream",
    "window": "stream",
    "mapreduce": "batch",
    "dataflow": "batch",
    "recomputation": "batch",
    "ethics": "privacy",
    "governance": "privacy",
    "retention": "privacy",
}


MODULE_CONCEPT_DEFAULTS = {
    "web-fundamentals": "http",
    "apis": "openapi",
    "backend": "validation",
    "databases": "relational-nosql",
    "sqlalchemy": "selectinload",
    "testing": "testing",
    "performance": "latency-throughput",
    "devops": "release-safety",
    "ai-integration": "ai",
    "system-design": "requirements",
    "ddia-tradeoffs": "architecture-tradeoffs",
    "ddia-nfrs": "nfrs",
    "ddia-data-models": "data-models",
    "ddia-storage": "lsm",
    "ddia-encoding": "schema",
    "ddia-replication": "replica",
    "ddia-sharding": "sharding",
    "ddia-transactions": "transaction",
    "ddia-distributed-systems": "distributed-failure",
    "ddia-consistency": "consensus",
    "ddia-batch": "batch",
    "ddia-stream": "stream",
    "ddia-stream-philosophy": "stream",
    "ddia-doing-right": "privacy",
}


MODULE_TAG_OVERRIDES = {
    "backend": {
        "fastapi": "backend-frameworks",
        "flask": "backend-frameworks",
        "express": "backend-frameworks",
        "nestjs": "backend-frameworks",
        "background tasks": "async",
        "lifespan": "validation",
        "response model": "validation",
    },
    "databases": {
        "postgresql": "relational-nosql",
        "mongodb": "relational-nosql",
        "redis": "relational-nosql",
        "relational": "relational-nosql",
        "nosql": "relational-nosql",
        "primary key": "relational-keys",
        "foreign key": "relational-keys",
        "relationship": "relational-keys",
        "join": "relational-keys",
    },
    "sqlalchemy": {
        "model": "orm-session",
        "session": "orm-session",
        "unit of work": "orm-session",
        "flush": "orm-session",
        "migration": "sqlalchemy-migrations",
        "alembic": "sqlalchemy-migrations",
        "raw sql": "raw-sql",
        "query": "raw-sql",
        "relationship": "relational-keys",
        "foreign key": "relational-keys",
    },
    "performance": {
        "latency": "latency-throughput",
        "throughput": "latency-throughput",
        "p95": "latency-throughput",
        "p99": "latency-throughput",
        "tail latency": "latency-throughput",
        "rate limit": "rate-limiting",
        "retry": "timeout",
        "backoff": "timeout",
    },
    "devops": {
        "docker compose": "docker",
        "environment variable": "runtime-config",
        "config": "runtime-config",
        "health check": "release-safety",
        "rollback": "release-safety",
        "feature flag": "release-safety",
        "canary": "release-safety",
        "secrets": "secrets",
        "artifact": "artifact-traceability",
        "versioning": "artifact-traceability",
    },
    "ai-integration": {
        "response logging": "ai",
        "privacy": "privacy",
        "governance": "privacy",
        "latency": "quantization",
        "cost": "quantization",
    },
    "system-design": {
        "api": "requirements",
        "data model": "data-models",
        "index": "index",
        "replica": "replica",
        "partition": "sharding",
        "hot shard": "sharding",
    },
}


def contains_term(text, term):
    if len(term) <= 3:
        return re.search(rf"(?<![a-z0-9]){re.escape(term)}(?![a-z0-9])", text) is not None
    return term in text


def concept_panel_for(question, module_id=None):
    text = " ".join([question.get("prompt", ""), question.get("explanation", ""), " ".join(question.get("tags", []))]).lower()
    concept_key = None
    module_overrides = MODULE_TAG_OVERRIDES.get(module_id or "", {})
    for tag in question.get("tags", []):
        normalized = tag.lower()
        if normalized in module_overrides:
            concept_key = module_overrides[normalized]
            break
    if concept_key is None and module_id and module_id.startswith("ddia-") and module_id in MODULE_CONCEPT_DEFAULTS:
        concept_key = MODULE_CONCEPT_DEFAULTS[module_id]
    for tag in question.get("tags", []):
        if concept_key is not None:
            break
        normalized = tag.lower()
        if normalized in CONCEPT_LIBRARY:
            concept_key = normalized
            break
        if normalized in CONCEPT_ALIASES:
            concept_key = CONCEPT_ALIASES[normalized]
            break
    if concept_key is None and module_id in MODULE_CONCEPT_DEFAULTS:
        concept_key = MODULE_CONCEPT_DEFAULTS[module_id]
    if concept_key is None:
        for term, target in CONCEPT_ALIASES.items():
            if contains_term(text, term):
                concept_key = target
                break
    if concept_key is None:
        for term in CONCEPT_LIBRARY:
            if contains_term(text, term):
                concept_key = term
                break
    concept = CONCEPT_LIBRARY.get(concept_key or "requirements")
    return {
        "title": concept["title"],
        "explanation": concept["explanation"],
        "key_takeaways": concept["takeaways"],
        "interview_insight": f"Interviewers usually ask this concept to evaluate {concept['insight']}",
        "practical_example": concept["example"],
        "diagram": concept.get("diagram"),
    }


def questions(module_id, module_title, tags):
    if module_id in TARGETED_BANK:
        return targeted_questions(module_id, TARGETED_BANK[module_id])
    items = []
    for index, pattern in enumerate(QUESTION_PATTERNS, start=1):
        qtype = pattern["type"]
        q = {
            "id": f"{module_id}-q{index:02d}",
            "type": qtype,
            "prompt": pattern["prompt"],
            "explanation": explanation_for(pattern),
            "difficulty": 1 if index <= 4 else 2 if index <= 10 else 3,
            "tags": list(dict.fromkeys(tags[:2] + pattern["tags"][:2])),
        }
        for field in ["options", "pairs", "code", "answer"]:
            if field in pattern:
                q[field] = pattern[field]
        q["concept_panel"] = concept_panel_for(q, module_id)
        items.append(q)
    return items


def targeted_questions(module_id, patterns):
    items = []
    for index, pattern in enumerate(patterns, start=1):
        q = {
            "id": f"{module_id}-q{index:02d}",
            "type": pattern["type"],
            "prompt": pattern["prompt"],
            "explanation": pattern["explanation"],
            "difficulty": pattern.get("difficulty", 2),
            "tags": pattern["tags"],
        }
        for field in ["options", "pairs", "code", "answer"]:
            if field in pattern:
                q[field] = pattern[field]
        q["concept_panel"] = pattern.get("concept_panel") or concept_panel_for(q, module_id)
        items.append(q)
    return items


def explanation_for(pattern):
    prompt = pattern["prompt"]
    explanations = {
        "A profile endpoint receives only a new email field. What should the API prefer?": "PATCH is meant for partial updates. PUT usually represents replacing the whole resource, so PATCH communicates the intent more clearly and avoids accidental field loss.",
        "Pick the operations that are usually safe to retry.": "GET, PUT, and DELETE are idempotent in normal REST design: repeating them leaves the same final state. POST usually creates a new resource, so retrying it can duplicate work without an idempotency key.",
        "Arrange the request path.": "The server should validate input before business logic so invalid data fails early. Once the logic completes, the API serializes the result into a response.",
        "Match each signal to its meaning.": "401 means the caller still needs authentication. 403 means the caller is known but not allowed. 503 means the service is temporarily unavailable.",
        "Fill the branch that classifies server errors.": "HTTP 5xx status codes represent server-side failures, so the function should return server_error for values from 500 through 599.",
        "Production duplicated records after a timeout. What is the bug?": "A timed-out POST may still have succeeded on the server. Retrying it without an idempotency key can create the same resource twice.",
        "What does classify_status_code(404) return?": "404 is in the 4xx range, which means the client requested something invalid or unavailable. In this classifier, that maps to client_error.",
        "A changing feed skips items with page numbers. What pagination style fits better?": "Cursor pagination continues after a stable record marker. Offset pagination can skip or duplicate rows when new records are inserted during paging.",
        "Which change best preserves existing clients when a response shape breaks compatibility?": "A versioned endpoint lets old clients keep using the old contract while new clients move to the breaking response shape.",
        "Select the reasons to validate input before business logic.": "Validation rejects malformed or unsafe data before it reaches core logic. That produces clearer errors, reduces security risk, and keeps business code focused.",
        "Match the scaling tool to the bottleneck.": "Caches reduce repeated reads, queues absorb bursts of work, and read replicas move read load away from the primary database.",
        "An endpoint loads 100 users, then reads user.orders in a loop. What is happening?": "That is the N+1 query pattern: one query loads the parent rows, then one extra query runs for each parent relationship access.",
        "Pick two fixes for the N+1 query pattern.": "selectinload and joinedload eager-load relationships so SQLAlchemy does not lazily query each relationship inside the loop.",
        "A downstream service is failing and your app keeps retrying instantly. What should you add first?": "Timeouts stop requests from hanging forever, and exponential backoff prevents retries from overwhelming a service that is already failing.",
        "Order the transaction flow.": "A transaction starts before related writes, commits only if every write succeeds, and rolls back on failure to avoid partial, inconsistent data.",
        "Match data shape to storage fit.": "SQL fits strongly related structured data, NoSQL fits flexible document-shaped data, and Redis is commonly used for fast cache or session lookups.",
        "Fill the safer SQLAlchemy loading option for a collection.": "selectinload is a common eager-loading strategy for collections. It avoids many lazy relationship queries without forcing one huge joined result.",
        "CPU-heavy image processing is slowing requests. Which model helps most?": "Async helps when code is waiting on I/O. CPU-heavy work needs parallel execution or worker processes to use more CPU capacity.",
        "A product page needs recommendations, but the recommender is down. What behavior is best?": "Graceful degradation keeps the core product page working even when a secondary feature fails.",
        "Which signals make an API easier for clients to use?": "Stable contracts, clear status codes, and documented schemas make client behavior predictable. Random fields make integration brittle.",
        "A response model includes password_hash. What is the bug?": "Response models should expose only safe fields. Returning password_hash leaks sensitive implementation data to clients.",
        "A social like count appears five seconds late. When is that acceptable?": "Eventual consistency is acceptable when temporary staleness does not break correctness, such as social counters or feeds.",
    }
    return explanations[prompt]


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


DDIA_SPECS = [
    ("ddia-tradeoffs", "DDIA: Data Systems Trade-offs", "Reliability, scalability, maintainability, and the cost of architectural choices.", ["ddia", "trade-offs", "architecture"], "choose guarantees before tools", "A team asks for the fastest possible database choice before defining workload or failure expectations.", "Define reliability, scalability, and maintainability goals first", ["Pick the newest database", "Start with a cache", "Skip requirements and benchmark later"], ["Reliability", "Scalability", "Maintainability"], ["Latency", "Throughput", "Operability"], "The system meets average latency but p99 spikes during bursts.", "Ignoring tail latency", ["Using schemas", "Writing ADRs", "Adding indexes"], ["State assumptions", "Describe workload", "Choose trade-off", "Validate with metrics"], "Architecture is not about one best tool; it is about making explicit trade-offs under known constraints."),
    ("ddia-nfrs", "DDIA: Nonfunctional Requirements", "Latency percentiles, availability, durability, operability, security, and evolvability.", ["ddia", "nfr", "sla"], "measure user-visible behavior", "A dashboard says average latency is fine, but users report slow requests.", "Inspect p95/p99 latency, not only averages", ["Increase page size", "Ignore outliers", "Remove logs"], ["Availability", "Durability", "Latency"], ["SLO", "Error budget", "Tail latency"], "An SLA promises uptime but no one tracks failed requests.", "No measurable SLO", ["Too many indexes", "Strong schema", "Good rollback"], ["Define SLO", "Measure baseline", "Set alert", "Review error budget"], "Nonfunctional requirements become useful only when they are measurable and tied to user impact."),
    ("ddia-data-models", "DDIA: Data Models and Query Languages", "Relational, document, graph, denormalization, joins, and query expressiveness.", ["ddia", "data-model", "query"], "model around access patterns", "A product has many cross-cutting relationships and ad hoc reporting needs.", "Use a relational model with joins or a graph model when relationships dominate", ["Store one giant JSON blob", "Duplicate everything blindly", "Avoid query requirements"], ["Relational joins", "Document locality", "Graph traversal"], ["Schema flexibility", "Query language", "Denormalization"], "A document store repeats user profile data in millions of orders.", "Uncontrolled denormalization", ["Normalized joins", "Indexes", "Foreign keys"], ["List access patterns", "Choose data shape", "Plan indexes", "Handle evolution"], "Data models trade locality and flexibility against consistency, duplication, and query power."),
    ("ddia-storage", "DDIA: Storage and Retrieval", "Log-structured storage, B-trees, indexes, compaction, write amplification, and read paths.", ["ddia", "storage", "indexes"], "match storage engine to workload", "A write-heavy workload slows down because every write updates many secondary indexes.", "Reduce unnecessary indexes or choose a write-optimized design", ["Add more indexes", "Use offset pagination", "Disable compaction"], ["B-tree", "LSM tree", "Secondary index"], ["Compaction", "Write amplification", "Read amplification"], "Reads are fast but inserts get slower after adding many indexes.", "Index write amplification", ["Cursor pagination", "HTTP cache", "CORS"], ["Identify read/write mix", "Pick index strategy", "Measure amplification", "Tune compaction"], "Indexes speed reads but cost writes and storage; storage engines optimize different sides of that trade-off."),
    ("ddia-encoding", "DDIA: Encoding and Evolution", "Schema evolution, backward/forward compatibility, JSON, Avro-like schemas, and rolling upgrades.", ["ddia", "encoding", "schema"], "evolve without breaking old readers", "A rolling deploy adds a required field that old services cannot parse.", "Make schema changes backward and forward compatible", ["Deploy all services instantly", "Delete unknown fields", "Skip versioning"], ["Backward compatibility", "Forward compatibility", "Rolling upgrade"], ["Schema registry", "Optional field", "Message encoding"], "A consumer crashes when a producer sends an unknown field.", "No forward-compatible reader", ["Good pagination", "Strong isolation", "Read replica"], ["Add optional field", "Deploy readers", "Deploy writers", "Remove old field later"], "Evolvable systems allow old and new code to communicate during rolling deploys and long-lived data storage."),
    ("ddia-replication", "DDIA: Replication", "Leaders, followers, lag, failover, read-your-writes, monotonic reads, and conflict handling.", ["ddia", "replication", "lag"], "reason about stale reads", "A user updates their profile then refreshes and sees old data from a replica.", "Route read-after-write traffic to the leader or use a read-your-writes strategy", ["Add a random follower", "Ignore replication lag", "Shard the UI"], ["Leader", "Follower", "Replication lag"], ["Failover", "Read-your-writes", "Conflict resolution"], "After failover, two nodes accepted writes for the same record.", "Split-brain conflict", ["Compaction", "B-tree lookup", "CSS hydration"], ["Write to leader", "Replicate log", "Serve follower reads", "Handle failover"], "Replication improves read scale and availability, but introduces lag, failover complexity, and consistency trade-offs."),
    ("ddia-sharding", "DDIA: Sharding", "Partitioning keys, hot spots, rebalancing, routing, consistent hashing, and cross-shard operations.", ["ddia", "sharding", "partitioning"], "distribute load without hot spots", "All writes use today’s date as the partition key and one shard melts down.", "Choose a higher-cardinality key or add salting to spread writes", ["Add a read replica only", "Use one partition forever", "Remove indexes"], ["Partition key", "Hot shard", "Rebalancing"], ["Routing table", "Consistent hashing", "Cross-shard query"], "One tenant owns 80% of traffic and overloads its shard.", "Skewed partition key", ["Schema registry", "2xx status", "Unit test"], ["Choose key", "Route request", "Rebalance data", "Monitor skew"], "Sharding scales data volume and throughput, but makes routing, rebalancing, and multi-key operations harder."),
    ("ddia-transactions", "DDIA: Transactions", "ACID, isolation levels, write skew, lost updates, serializability, and distributed transactions.", ["ddia", "transactions", "isolation"], "know which anomaly is possible", "Two doctors concurrently mark themselves off-call and the system ends with no doctor on call.", "Use serializable isolation or a constraint that prevents write skew", ["Use read uncommitted", "Add a cache", "Retry POST forever"], ["Atomicity", "Isolation", "Durability"], ["Lost update", "Write skew", "Serializable"], "Two users edit the same counter and one increment disappears.", "Lost update", ["Replica lag", "Hot shard", "Schema evolution"], ["Begin", "Read relevant rows", "Check invariant", "Commit atomically"], "Transactions protect invariants, but stronger isolation can reduce concurrency and increase coordination cost."),
    ("ddia-distributed-systems", "DDIA: Trouble with Distributed Systems", "Partial failure, unreliable clocks, timeouts, retries, network partitions, and process pauses.", ["ddia", "distributed-systems", "failure"], "expect partial failure", "A service times out, but the downstream operation might still complete later.", "Treat timeout as unknown outcome and make retries idempotent", ["Assume it failed", "Retry forever", "Trust local clock order"], ["Timeout", "Network partition", "Clock skew"], ["Process pause", "Duplicate request", "Fencing token"], "A lock holder pauses for GC and resumes after its lease expired.", "Stale process acting after lease expiry", ["Index scan", "JOIN order", "Schema registry"], ["Set timeout", "Classify unknown result", "Retry safely", "Reconcile outcome"], "Distributed systems fail partially; timeouts, clocks, and retries are hints, not perfect truth."),
    ("ddia-consistency", "DDIA: Consistency and Consensus", "Linearizability, causal consistency, consensus, leader election, quorum, and safety vs liveness.", ["ddia", "consistency", "consensus"], "choose consistency by invariant", "A username must be globally unique even during failover.", "Use a strongly consistent coordination path for the uniqueness check", ["Use any replica", "Accept duplicates", "Cache the decision"], ["Linearizability", "Causal consistency", "Consensus"], ["Quorum", "Leader election", "Safety"], "Two leaders are elected and both accept writes.", "Consensus safety violation", ["Write amplification", "CSS bundle", "Document locality"], ["Propose value", "Reach quorum", "Commit decision", "Apply in order"], "Consensus gives agreement under failures, but it costs coordination and is not needed for every read or counter."),
    ("ddia-batch", "DDIA: Batch Processing", "MapReduce-style jobs, dataflow, joins, materialized views, snapshots, and recomputation.", ["ddia", "batch", "dataflow"], "recompute deterministically", "A nightly analytics job must rebuild a report from raw immutable events.", "Use a batch pipeline that reads a stable snapshot and writes derived output", ["Mutate source events", "Use only request handlers", "Skip checkpoints"], ["Batch job", "Snapshot", "Materialized view"], ["Shuffle join", "Idempotent output", "Backfill"], "A backfill runs twice and doubles the report numbers.", "Non-idempotent batch output", ["Replication lag", "CORS", "JWT"], ["Read input", "Transform records", "Group or join", "Write output"], "Batch processing favors throughput and reproducibility over low-latency incremental results."),
    ("ddia-stream", "DDIA: Stream Processing", "Event logs, consumers, windows, watermarks, delivery semantics, backpressure, and stateful processing.", ["ddia", "streaming", "events"], "process events continuously", "A consumer is slower than producers and lag keeps growing.", "Apply backpressure, scale consumers, or reduce per-event work", ["Ignore lag", "Retry instantly", "Drop offsets randomly"], ["Event log", "Consumer offset", "Backpressure"], ["Window", "Watermark", "Exactly-once effect"], "A consumer crashes after side effects but before committing its offset.", "Duplicate processing risk", ["B-tree", "DNS", "OpenAPI"], ["Ingest event", "Process with state", "Commit offset", "Emit result"], "Streaming reduces latency for derived data, but demands careful handling of ordering, duplicates, and state."),
    ("ddia-stream-philosophy", "DDIA: Streaming Systems Philosophy", "Events as facts, derived state, replay, event time, operational boundaries, and correctness.", ["ddia", "streaming", "event-time"], "treat events as immutable facts", "A service overwrites the only copy of an event when correcting a business mistake.", "Append a correcting event instead of mutating history", ["Delete history", "Trust processing time", "Ignore replay"], ["Event time", "Processing time", "Replay"], ["Derived state", "Correction event", "Audit trail"], "A replay produces different results because handlers depend on current wall-clock time.", "Non-deterministic replay", ["Read replica", "Tail latency", "Schema-free"], ["Record fact", "Process derivation", "Store offset", "Replay when needed"], "Event logs are powerful because they let you rebuild derived state, but only if processing is deterministic and schemas evolve safely."),
    ("ddia-doing-right", "DDIA: Doing the Right Thing", "Data ethics, privacy, correctness, auditability, security, retention, and human impact.", ["ddia", "privacy", "ethics"], "design for responsible data use", "A team wants to keep raw user events forever because storage is cheap.", "Define retention, purpose, access controls, and deletion rules", ["Keep everything forever", "Hide policy in code", "Disable audit logs"], ["Data minimization", "Retention", "Auditability"], ["Access control", "Consent", "Deletion"], "An analyst can query sensitive production data without review or logging.", "Missing governance controls", ["Partition skew", "B-tree", "Quorum read"], ["Define purpose", "Limit collection", "Control access", "Audit use"], "Responsible systems treat data as risk as well as value: collect less, protect it, and make use accountable."),
]


def ddia_lessons(module_id, title, description, tags):
    topics = [
        ("core-model", "Core Mental Model", description, tags[:3], f"Use {title} concepts to name the workload, guarantee, and failure mode before choosing a tool."),
        ("failure-mode", "Failure Mode Drill", "Most data-system mistakes come from hidden assumptions about time, ordering, durability, or coordination.", ["failure", "assumption", "trade-off"], "Ask what can be stale, duplicated, delayed, reordered, or partially applied."),
        ("design-choice", "Design Choice", "Good architecture explains what it optimizes and what it makes harder.", ["design", "trade-off", "constraint"], "A read replica improves read capacity but can show stale data."),
        ("interview-synthesis", "Interview Synthesis", "Strong answers connect symptoms to guarantees, then propose a measured mitigation.", ["interview", "diagnosis", "mitigation"], "Name the invariant, pick the weakest guarantee that protects it, and explain the cost."),
    ]
    return [lesson(module_id, idx, item) for idx, item in enumerate(topics)]


DDIA_EXTRA_PATTERNS = {
    "ddia-tradeoffs": [
        {"type": "matching", "prompt": "Match architecture shape to the operational trade-off.", "pairs": [{"left": "Cloud service", "right": "Less operations work, more vendor dependency"}, {"left": "Self-hosting", "right": "More control, more operational burden"}, {"left": "Serverless", "right": "Low idle ops, platform limits and cold starts"}], "answer": {"Cloud service": "Less operations work, more vendor dependency", "Self-hosting": "More control, more operational burden", "Serverless": "Low idle ops, platform limits and cold starts"}, "explanation": "Cloud, self-hosting, and serverless choices change operability, cost, control, and failure modes. They are architecture trade-offs, not just deployment preferences.", "tags": ["cloud", "self-hosting", "serverless", "operability"]},
        {"type": "scenario_choice", "prompt": "A team splits a simple product into many microservices before load or team boundaries require it. What is the likely cost?", "options": ["More distributed operations and coordination overhead", "Automatic consistency", "No network failures", "Free observability"], "answer": "More distributed operations and coordination overhead", "explanation": "Microservices can help organizational scaling, but they add deployment, network, observability, and data-consistency costs.", "tags": ["microservices", "operability", "maintainability"]},
        {"type": "matching", "prompt": "Match source-of-truth terms.", "pairs": [{"left": "System of record", "right": "Authoritative source for facts"}, {"left": "Derived data", "right": "Rebuildable view computed from source data"}, {"left": "Throughput", "right": "Amount of work completed per time period"}], "answer": {"System of record": "Authoritative source for facts", "Derived data": "Rebuildable view computed from source data", "Throughput": "Amount of work completed per time period"}, "explanation": "DDIA repeatedly separates systems of record from derived data because losing derived data is very different from losing the source of truth.", "tags": ["system of record", "derived data", "throughput"]},
    ],
    "ddia-nfrs": [
        {"type": "matching", "prompt": "Match nonfunctional requirement metrics.", "pairs": [{"left": "p95", "right": "95 percent of requests are at or below this latency"}, {"left": "p99", "right": "99 percent of requests are at or below this latency"}, {"left": "SLA", "right": "External service promise or agreement"}], "answer": {"p95": "95 percent of requests are at or below this latency", "p99": "99 percent of requests are at or below this latency", "SLA": "External service promise or agreement"}, "explanation": "Percentiles describe tail latency much better than averages. SLAs and SLOs should be measurable.", "tags": ["p95", "p99", "percentile", "SLA", "tail latency"]},
        {"type": "multi_select", "prompt": "Which concerns belong in nonfunctional requirements?", "options": ["Security", "Operability", "Evolvability", "Button label text"], "answer": ["Security", "Operability", "Evolvability"], "explanation": "Nonfunctional requirements describe qualities such as security, operability, evolvability, availability, durability, and latency.", "tags": ["security", "operability", "evolvability", "nfr"]},
    ],
    "ddia-storage": [
        {"type": "matching", "prompt": "Match storage-engine terms.", "pairs": [{"left": "SSTable", "right": "Sorted immutable string table used by LSM-style storage"}, {"left": "Log-structured", "right": "Writes append first, then compaction reorganizes data"}, {"left": "Read amplification", "right": "Extra reads needed internally to answer one lookup"}], "answer": {"SSTable": "Sorted immutable string table used by LSM-style storage", "Log-structured": "Writes append first, then compaction reorganizes data", "Read amplification": "Extra reads needed internally to answer one lookup"}, "explanation": "LSM-style storage writes immutable sorted files such as SSTables and relies on compaction, trading write behavior against read amplification.", "tags": ["SSTable", "log-structured", "read amplification", "compaction"]},
    ],
    "ddia-encoding": [
        {"type": "matching", "prompt": "Match encoding formats and schema controls.", "pairs": [{"left": "JSON", "right": "Human-readable text encoding with loose schemas"}, {"left": "Avro", "right": "Compact schema-based binary encoding"}, {"left": "Schema registry", "right": "Shared compatibility gate for message schemas"}], "answer": {"JSON": "Human-readable text encoding with loose schemas", "Avro": "Compact schema-based binary encoding", "Schema registry": "Shared compatibility gate for message schemas"}, "explanation": "JSON is easy to inspect; Avro-style encodings are compact and schema-driven. Schema evolution needs compatibility checks.", "tags": ["JSON", "Avro", "schema registry", "schema evolution", "message encoding"]},
    ],
    "ddia-replication": [
        {"type": "scenario_choice", "prompt": "A user reads page 1 from one replica, then page 2 from a laggier replica and sees time move backward. Which guarantee helps?", "options": ["Monotonic reads", "More write amplification", "A CSS cache", "Deleting the leader"], "answer": "Monotonic reads", "explanation": "Monotonic reads prevent a client from observing older data after it has already observed newer data.", "tags": ["monotonic reads", "replication lag", "stale reads"]},
        {"type": "scenario_choice", "prompt": "Two replicas accept conflicting profile edits during failover. What must the design include?", "options": ["Conflict resolution policy", "More HTTP headers only", "SSTable compaction", "Frontend debounce"], "answer": "Conflict resolution policy", "explanation": "Replication can create conflicts during failover or multi-leader writes. The system needs a deterministic conflict-resolution strategy.", "tags": ["conflict resolution", "split-brain", "failover"]},
    ],
    "ddia-transactions": [
        {"type": "matching", "prompt": "Match transaction isolation terms.", "pairs": [{"left": "ACID", "right": "Transaction guarantees around correctness and durability"}, {"left": "Snapshot isolation", "right": "Reads from a consistent database snapshot"}, {"left": "Distributed transaction", "right": "Coordinates commit across multiple nodes or services"}], "answer": {"ACID": "Transaction guarantees around correctness and durability", "Snapshot isolation": "Reads from a consistent database snapshot", "Distributed transaction": "Coordinates commit across multiple nodes or services"}, "explanation": "Isolation choices determine which anomalies remain possible. Distributed transactions add coordination cost.", "tags": ["ACID", "snapshot isolation", "distributed transaction"]},
    ],
    "ddia-distributed-systems": [
        {"type": "bug_hunt", "prompt": "A process holds a lease, pauses for a long GC pause, then resumes and writes after another owner took over. What prevents the stale write?", "options": ["Fencing token", "Trusting local clock time", "Retrying forever", "Read amplification"], "answer": "Fencing token", "explanation": "A GC pause or process pause can make a stale owner act after its lease expires. Fencing tokens let storage reject old actors.", "tags": ["GC pause", "process pause", "lease", "fencing token"]},
        {"type": "scenario_choice", "prompt": "A timeout fires after sending a payment request. What should the caller assume?", "options": ["Outcome is unknown until reconciled", "Payment definitely failed", "Payment definitely succeeded", "Clock order proves the result"], "answer": "Outcome is unknown until reconciled", "explanation": "In distributed systems, timeouts are evidence, not truth. The downstream may still complete, so retries need idempotency and reconciliation.", "tags": ["partial failure", "timeout", "duplicate request"]},
    ],
    "ddia-consistency": [
        {"type": "matching", "prompt": "Match consensus properties.", "pairs": [{"left": "Safety", "right": "The bad thing never happens"}, {"left": "Liveness", "right": "The good thing eventually happens"}, {"left": "Strong consistency", "right": "Reads observe a single up-to-date order"}], "answer": {"Safety": "The bad thing never happens", "Liveness": "The good thing eventually happens", "Strong consistency": "Reads observe a single up-to-date order"}, "explanation": "Consensus discussions separate safety from liveness. Strong consistency is useful for invariants such as uniqueness and leadership.", "tags": ["safety", "liveness", "strong consistency", "leader election"]},
        {"type": "scenario_choice", "prompt": "Only one scheduler may run a job at a time. What distributed primitive is commonly involved?", "options": ["Leader election backed by consensus", "Offset pagination", "Browser cookies", "JSON formatting"], "answer": "Leader election backed by consensus", "explanation": "Leader election needs agreement so two nodes do not both believe they are the active leader.", "tags": ["leader election", "consensus", "agreement"]},
    ],
    "ddia-batch": [
        {"type": "matching", "prompt": "Match batch-processing concepts.", "pairs": [{"left": "MapReduce", "right": "Map records, shuffle by key, reduce groups"}, {"left": "Dataflow", "right": "Pipeline of transformations over data"}, {"left": "Recomputation", "right": "Rebuild derived output from source input"}], "answer": {"MapReduce": "Map records, shuffle by key, reduce groups", "Dataflow": "Pipeline of transformations over data", "Recomputation": "Rebuild derived output from source input"}, "explanation": "Batch systems favor deterministic recomputation from stable input, often through MapReduce-like dataflow stages.", "tags": ["MapReduce", "dataflow", "recomputation", "shuffle join"]},
    ],
    "ddia-stream": [
        {"type": "matching", "prompt": "Match stream-processing guarantees.", "pairs": [{"left": "At-least-once", "right": "Duplicates are possible"}, {"left": "At-most-once", "right": "Loss is possible"}, {"left": "Stateful processing", "right": "Maintains state across events"}], "answer": {"At-least-once": "Duplicates are possible", "At-most-once": "Loss is possible", "Stateful processing": "Maintains state across events"}, "explanation": "Delivery semantics define what can happen around failures. Stateful processing adds recovery and duplicate-handling concerns.", "tags": ["delivery semantics", "stateful processing", "duplicate processing"]},
        {"type": "scenario_choice", "prompt": "A stream aggregate counts events by event time, but late events arrive after the window seems done. What concept handles progress?", "options": ["Watermark", "B-tree", "CORS", "Swagger"], "answer": "Watermark", "explanation": "Watermarks estimate how complete event-time input is so stream processors can close or update windows.", "tags": ["watermark", "window", "event time"]},
    ],
    "ddia-doing-right": [
        {"type": "scenario_choice", "prompt": "A team can collect sensitive user behavior but has no clear product purpose. What principle should stop them?", "options": ["Data minimization and ethics", "More derived indexes", "More replicas", "Lower p99 only"], "answer": "Data minimization and ethics", "explanation": "Responsible systems collect data for a defined purpose, minimize unnecessary retention, and consider human impact.", "tags": ["ethics", "data minimization", "privacy"]},
        {"type": "multi_select", "prompt": "Which controls support responsible data use?", "options": ["Consent", "Retention policy", "Governance/audit logs", "Unlimited analyst access"], "answer": ["Consent", "Retention policy", "Governance/audit logs"], "explanation": "Consent, retention, access review, governance, and auditability make data use accountable.", "tags": ["consent", "governance", "auditability", "retention"]},
    ],
}


def ddia_questions(module_id, spec):
    _, title, _, tags, principle, scenario, correct, distractors, concepts_a, concepts_b, bug, bug_answer, bug_wrong, flow, tradeoff = spec
    all_concepts = concepts_a + concepts_b
    first_matches = all_concepts[:3]
    second_matches = all_concepts[3:6]
    patterns = [
        {"type": "scenario_choice", "prompt": scenario, "options": [correct] + distractors, "answer": correct, "explanation": f"{correct}. In {title}, the first move is to protect the system's real guarantee: {principle}.", "tags": tags[:2]},
        {"type": "multi_select", "prompt": f"Which concepts belong in a {title} design discussion?", "options": concepts_a + ["CSS color choice"], "answer": concepts_a, "explanation": f"These concepts are central to {title.lower()}. The unrelated option may matter in frontend work, but it does not diagnose this data-system problem.", "tags": tags[:2]},
        {"type": "matching", "prompt": f"Match the {title} concepts.", "pairs": [{"left": item, "right": concept_meaning(item)} for item in first_matches], "answer": {item: concept_meaning(item) for item in first_matches}, "explanation": "The mapping links each term to the operational behavior you should listen for in interviews and incidents.", "tags": tags[:2]},
        {"type": "ordering", "prompt": f"Order the {title} design move.", "options": flow, "answer": flow, "explanation": "This order keeps the reasoning grounded: observe the requirement, choose the guarantee, then validate it with the system behavior.", "tags": tags[:2]},
        {"type": "bug_hunt", "prompt": bug, "options": [bug_answer] + bug_wrong, "answer": bug_answer, "explanation": f"The symptom is best explained by {bug_answer}. A strong answer names the anomaly and then proposes a mitigation.", "tags": tags[:2]},
        {"type": "multiple_choice", "prompt": f"What trade-off should you say out loud for {title}?", "options": [tradeoff, "Every tool gives the same guarantees", "Latency and correctness are unrelated", "Adding replicas always removes complexity"], "answer": tradeoff, "explanation": tradeoff, "tags": tags[:2]},
        {"type": "scenario_choice", "prompt": f"During design review, what question best tests the {title} choice?", "options": ["What guarantee must hold during failure?", "Which logo color is final?", "Can we skip metrics?", "Can clients guess the schema?"], "answer": "What guarantee must hold during failure?", "explanation": "Data-system design should start from invariants and failure behavior. Tool choice follows from the guarantee you need.", "tags": tags[:2]},
        {"type": "multi_select", "prompt": f"Pick interview moves that make a {title} answer sound senior.", "options": ["Name the workload", "Name the failure mode", "State the trade-off", "Claim there is one perfect database"], "answer": ["Name the workload", "Name the failure mode", "State the trade-off"], "explanation": "Strong answers are conditional: they describe load, data shape, failure mode, and cost instead of pretending one tool is always best.", "tags": tags[:2]},
        {"type": "matching", "prompt": f"Match outcome to design pressure in {title}.", "pairs": [{"left": concept_meaning(item), "right": item} for item in second_matches], "answer": {concept_meaning(item): item for item in second_matches}, "explanation": "Reversing the mapping trains recognition from symptoms back to the concept, which is how incidents and interviews usually present the problem.", "tags": tags[:2]},
        {"type": "code_fill", "prompt": "Fill the guard that prevents an unsafe operation from continuing.", "code": "if not guarantee_holds(event):\n    return ____", "options": ["\"retry_or_reconcile\"", "\"ignore\"", "\"delete_history\"", "\"assume_success\""], "answer": "\"retry_or_reconcile\"", "explanation": "When a guarantee is uncertain, the safe path is to retry with idempotency or reconcile state. Assuming success hides data loss or duplication.", "tags": tags[:2]},
        {"type": "bug_hunt", "prompt": f"A team adds {title} machinery but cannot explain the invariant it protects. What is the real issue?", "options": ["Architecture without a stated guarantee", "Too many unit tests", "Correct schema evolution", "Clear observability"], "answer": "Architecture without a stated guarantee", "explanation": "Advanced data tools are justified by guarantees. Without a stated invariant, the team cannot tell whether complexity is buying anything.", "tags": tags[:2]},
        {"type": "scenario_choice", "prompt": f"What is the safest first response when {title} behavior surprises production?", "options": ["Capture evidence with logs, metrics, and traces", "Delete the database", "Retry all writes forever", "Disable validation"], "answer": "Capture evidence with logs, metrics, and traces", "explanation": "Data-system failures are often timing or workload dependent. Evidence lets you distinguish stale reads, duplicate work, hot keys, lock waits, and real data loss.", "tags": tags[:2]},
        {"type": "ordering", "prompt": f"Order the incident explanation for {title}.", "options": ["Observed symptom", "Likely invariant violation", "Concrete mitigation", "Trade-off introduced"], "answer": ["Observed symptom", "Likely invariant violation", "Concrete mitigation", "Trade-off introduced"], "explanation": "This structure turns a vague answer into an engineering argument: symptom, cause, fix, and cost.", "tags": tags[:2]},
        {"type": "multi_select", "prompt": f"Which answers are honest about {title} trade-offs?", "options": ["It depends on workload", "Measure tail behavior", "State consistency needs", "Always optimize averages only"], "answer": ["It depends on workload", "Measure tail behavior", "State consistency needs"], "explanation": "DDIA-style reasoning is explicit about workload and guarantees. Average-only or absolute claims usually hide the real trade-off.", "tags": tags[:2]},
    ]
    patterns.extend(DDIA_EXTRA_PATTERNS.get(module_id, []))
    items = []
    for index, pattern in enumerate(patterns, start=1):
        q = {
            "id": f"{module_id}-q{index:02d}",
            "type": pattern["type"],
            "prompt": pattern["prompt"],
            "explanation": pattern["explanation"],
            "difficulty": 2 if index <= 5 else 3,
            "tags": list(dict.fromkeys(pattern["tags"])),
        }
        for field in ["options", "pairs", "code", "answer"]:
            if field in pattern:
                q[field] = pattern[field]
        q["concept_panel"] = concept_panel_for(q, module_id)
        items.append(q)
    return items


def concept_meaning(term):
    meanings = {
        "Reliability": "Keeps working correctly when faults occur",
        "Scalability": "Handles growth in load, data, or complexity",
        "Maintainability": "Stays understandable and changeable over time",
        "Latency": "Time for one operation to complete",
        "Throughput": "Amount of work completed per time period",
        "Operability": "Ease of running and diagnosing the system",
        "Availability": "Fraction of time the system can serve requests",
        "Durability": "Data survives crashes or restarts",
        "SLO": "Measurable target for service behavior",
        "Error budget": "Allowed unreliability before corrective action",
        "Tail latency": "Slow end of the latency distribution",
        "Relational joins": "Combines normalized records through relationships",
        "Document locality": "Keeps nested data together for one access pattern",
        "Graph traversal": "Follows many-to-many relationships efficiently",
        "Schema flexibility": "Allows records to vary in shape over time",
        "Query language": "Expresses how data should be retrieved or transformed",
        "Denormalization": "Duplicates data to speed reads at consistency cost",
        "B-tree": "Read-optimized ordered index structure",
        "LSM tree": "Write-optimized log-structured storage approach",
        "Secondary index": "Additional lookup path beyond the primary key",
        "Compaction": "Rewrites storage files to remove obsolete entries",
        "Write amplification": "Extra internal writes caused by one logical write",
        "Read amplification": "Extra internal reads needed to answer one query",
        "Backward compatibility": "New code can read old data",
        "Forward compatibility": "Old code can tolerate new data",
        "Rolling upgrade": "Deploys versions gradually without stopping service",
        "Schema registry": "Shared source of truth for encoded message schemas",
        "Optional field": "Schema change that old data can omit safely",
        "Message encoding": "Binary or textual representation sent or stored",
        "Leader": "Replica that accepts writes in leader-based replication",
        "Follower": "Replica that receives copied changes",
        "Replication lag": "Delay before copied data reaches a replica",
        "Failover": "Promotes another replica when the leader fails",
        "Read-your-writes": "User sees their own recent write on later reads",
        "Conflict resolution": "Chooses or merges competing concurrent writes",
        "Partition key": "Value used to choose where a record lives",
        "Hot shard": "Partition receiving disproportionate load",
        "Rebalancing": "Moves data or ownership across partitions",
        "Routing table": "Maps keys or ranges to responsible partitions",
        "Consistent hashing": "Routing strategy that limits movement during resizing",
        "Cross-shard query": "Query that must touch multiple partitions",
        "Atomicity": "All writes commit or none do",
        "Isolation": "Concurrent transactions do not break expected invariants",
        "Lost update": "One write overwrites another without seeing it",
        "Write skew": "Concurrent writes satisfy local checks but break a global invariant",
        "Serializable": "Result is equivalent to running transactions one at a time",
        "Timeout": "Bounded wait that leaves outcome uncertain",
        "Network partition": "Nodes cannot communicate even though they still run",
        "Clock skew": "Machines disagree about current time",
        "Process pause": "A running process stops making progress temporarily",
        "Duplicate request": "Same operation is received more than once",
        "Fencing token": "Monotonic token that prevents stale actors from writing",
        "Linearizability": "Operations appear to happen atomically in real-time order",
        "Causal consistency": "Causally related events are observed in order",
        "Consensus": "Nodes agree on one value despite failures",
        "Quorum": "Enough replicas to make a decision or read/write valid",
        "Leader election": "Chooses one coordinator among replicas",
        "Safety": "Bad outcomes never happen",
        "Batch job": "Finite job over bounded input",
        "Snapshot": "Stable view of input data at a point in time",
        "Materialized view": "Stored derived result maintained from source data",
        "Shuffle join": "Groups records by key so related records meet",
        "Idempotent output": "Writing results twice does not double-count",
        "Backfill": "Recomputes historical derived data",
        "Event log": "Append-only ordered stream of events",
        "Consumer offset": "Position a consumer has processed",
        "Backpressure": "Slows producers or work intake when consumers cannot keep up",
        "Window": "Groups events by time or count for aggregation",
        "Watermark": "Estimate of how complete event-time input is",
        "Exactly-once effect": "End result is correct despite retries or duplicates",
        "Event time": "Time when the event actually happened",
        "Processing time": "Time when the system processes the event",
        "Replay": "Reprocesses stored events to rebuild state",
        "Derived state": "State computed from source events",
        "Correction event": "New event that amends history without deleting it",
        "Audit trail": "Record of what happened and who did it",
        "Data minimization": "Collect only data needed for a defined purpose",
        "Retention": "How long data is kept",
        "Auditability": "Ability to inspect and explain data access or changes",
        "Access control": "Rules limiting who can read or modify data",
        "Consent": "User permission for a defined data use",
        "Deletion": "Removing data according to policy or request",
    }
    return meanings[term]


def ddia_challenge(module_id, title, tags):
    return {
        "id": f"{module_id}-route-partition",
        "title": f"{title} partition router",
        "instructions": "Implement route_partition(key: str, partitions: int) -> int. Return a stable partition from 0 to partitions - 1. Raise ValueError when partitions is less than 1.",
        "starter_code": "def route_partition(key: str, partitions: int) -> int:\n    pass\n",
        "function_signature": "def route_partition(key: str, partitions: int) -> int",
        "visible_tests": [
            {"name": "range", "call": "0 <= route_partition('user-7', 8) < 8", "expected": True},
            {"name": "stable", "call": "route_partition('tenant-a', 16) == route_partition('tenant-a', 16)", "expected": True},
        ],
        "hidden_tests": [
            {"name": "single partition", "call": "route_partition('anything', 1)", "expected": 0},
            {"name": "different size still range", "call": "0 <= route_partition('order-9', 3) < 3", "expected": True},
        ],
        "timeout_seconds": 2,
        "explanation": "Stable routing is a core primitive behind partitioning. This exercise checks deterministic mapping and input validation.",
        "difficulty": 2,
        "tags": tags[:3],
    }


def epam_panel(title, explanation, takeaways, example, insight, diagram=None):
    return {
        "title": title,
        "explanation": explanation,
        "key_takeaways": takeaways,
        "practical_example": example,
        "interview_insight": f"Interviewers usually ask this concept to evaluate {insight}",
        "diagram": diagram or {"type": "flow", "title": title, "nodes": [{"label": title}, {"label": "Interview signal"}, {"label": "Production use"}]},
    }


def epam_question(module_id, index, item):
    concept, prompt, answer, distractors, explanation, tags, example, insight = item
    return {
        "id": f"{module_id}-q{index:02d}",
        "type": "scenario_choice",
        "prompt": prompt,
        "options": [answer] + distractors,
        "answer": answer,
        "explanation": explanation,
        "difficulty": 1 if index <= 4 else 2 if index <= 9 else 3,
        "tags": tags,
        "concept_panel": epam_panel(concept, explanation, tags[:5] if len(tags) >= 3 else tags + ["interview reasoning", "practical trade-off"], example, insight),
    }


def epam_lesson(module_id, index, title, tags):
    return {
        "id": f"{module_id}-lesson-{index}",
        "title": title,
        "summary": f"EPAM interview drill for {title.lower()}.",
        "explanation": f"Explain {title.lower()} through behavior, trade-offs, examples, and failure modes. Connect syntax to production code instead of reciting definitions.",
        "key_points": tags[:5],
        "examples": [f"Use {title.lower()} to reason through a concrete backend or data-system scenario."],
        "interview_questions": [f"How would you explain {title.lower()} in an interview?", f"What common bug appears when {title.lower()} is misunderstood?"],
        "difficulty": 1 if index <= 2 else 2,
        "tags": tags[:5],
    }


EPAM_MODULES = [
    {
        "id": "epam-python-core",
        "title": "EPAM Python Core",
        "description": "Python object model, references, mutability, core collections, complexity, truthiness, equality, and language trade-offs.",
        "tags": ["python", "references", "collections", "complexity"],
        "lessons": [
            ("Variables, References, and Mutability", ["variables", "references", "mutable", "immutable"]),
            ("Collections and Complexity", ["list", "tuple", "set", "dict", "time complexity"]),
            ("Truthiness and Equality", ["truthiness", "is", "==", "identity"]),
            ("Why Python", ["python", "java", "dynamic typing", "productivity"]),
        ],
        "questions": [
            ("Variables and References", "Two variables point to the same list and one appends an item. What should you expect?", "Both names can observe the mutation", ["Only the first name changes", "Python copies lists automatically", "The append raises TypeError"], "Python variables are names bound to objects. Lists are mutable, so mutating through one reference is visible through another reference to the same object.", ["variables", "references", "mutable"], "a = []; b = a; b.append(1) leaves a as [1].", "whether you understand Python references rather than assuming assignment copies data."),
            ("Mutable vs Immutable", "Which value is safest as a dictionary key?", "A tuple of strings", ["A list of strings", "A dictionary", "A set"], "Dictionary keys must be hashable. Immutable tuples containing hashable values can be keys; mutable lists, dictionaries, and sets cannot.", ["mutable", "immutable", "hashable", "dictionary"], "Use ('region', 'month') as a composite key for cached KPI results.", "whether you understand mutability and hashing constraints."),
            ("Lists, Tuples, Sets, Dictionaries", "You repeatedly test whether user IDs were already seen. Which collection fits best?", "set", ["list", "tuple", "string concatenation"], "Sets provide average O(1) membership checks and model uniqueness. Lists preserve order but membership is O(n).", ["sets", "lists", "time complexity"], "seen_ids = {1, 2, 3}; if user_id in seen_ids: ...", "whether you choose data structures by access pattern."),
            ("Time Complexity of Common Operations", "A list contains one million IDs. What is the cost of `target in ids`?", "O(n)", ["O(1)", "O(log n)", "O(n log n)"], "List membership scans until it finds the item or reaches the end, so it is linear. Dict and set membership are average O(1).", ["time complexity", "list", "dict", "set"], "Convert a list to a set before many membership checks.", "whether you can reason about Python performance without guessing."),
            ("Truthiness", "Which check is most Pythonic for a list that may be empty?", "if items:", ["if len(items) == True:", "if items is True:", "if items == None:"], "Empty containers are falsy and non-empty containers are truthy. Use `if items:` when you only care whether a collection has content.", ["truthiness", "list", "best practices"], "Return early with `if not rows:` when a query returns no records.", "whether you know idiomatic Python boolean behavior."),
            ("is vs ==", "How should you usually check whether a variable is None?", "value is None", ["value == None", "value = None", "value.__eq__(None)"], "`is` checks identity and None is a singleton, so `is None` is the idiomatic check. `==` delegates to equality logic and may be overloaded.", ["is", "==", "None", "identity"], "Use `if user is None:` after a repository lookup.", "whether you separate identity from equality."),
            ("Dictionary Operations", "Which operation is average O(1) in a dictionary?", "Lookup by key", ["Search by value", "Sorting all keys", "Scanning nested lists"], "Dictionaries are hash tables optimized for key lookup, insertion, and deletion on average. Searching values still requires scanning.", ["dict", "hash table", "time complexity"], "settings['DATABASE_URL'] is a direct key lookup.", "whether you understand common dictionary operation costs."),
            ("Tuple Use Cases", "Why might an interview answer choose a tuple over a list?", "The record should be immutable", ["It appends faster", "It allows duplicate keys", "It avoids iteration"], "Tuples communicate fixed-size immutable records. They can also be hashable if their elements are hashable.", ["tuple", "immutable", "hashable"], "Represent a coordinate as (x, y) when it should not be mutated.", "whether you understand semantic collection choice."),
            ("Set Semantics", "A deduplication step should keep only unique customer IDs. What structure fits?", "set", ["list only", "tuple only", "plain string"], "Sets represent uniqueness and support fast membership checks. They do not preserve duplicates.", ["set", "deduplication", "membership"], "Use `unique_ids = set(raw_ids)` before processing.", "whether you can model uniqueness directly."),
            ("Why Python", "Why is Python often chosen for backend and AI product work?", "Fast development with strong ecosystem support", ["It is always faster than Java", "It has no runtime errors", "It removes the need for tests"], "Python is productive, readable, and has excellent web, data, ML, and automation libraries. The trade-off is runtime performance and dynamic typing risks that require tests and discipline.", ["python", "ecosystem", "ml", "backend"], "FastAPI plus pandas/scikit-learn can ship an analytics API quickly.", "whether you can explain pragmatic language trade-offs."),
            ("Why Not Java", "What is a fair Python-vs-Java trade-off?", "Python is faster to iterate; Java often offers stronger static typing and JVM performance", ["Python always beats Java at scale", "Java cannot build APIs", "Python does not need architecture"], "Python and Java solve overlapping problems with different trade-offs. Java often offers stronger compile-time guarantees; Python often wins in iteration speed and AI/data ecosystems.", ["python", "java", "trade-off"], "Use Python for ML-heavy services; use Java when a team values JVM tooling and static contracts.", "whether you can compare languages without shallow absolutes."),
            ("What Makes Python Different", "What makes Python's object model different from many beginner mental models?", "Names bind to objects rather than variables storing raw values", ["Every assignment deep-copies", "Only classes are objects", "Immutable objects cannot be referenced"], "Everything is an object, and assignment binds a name to an object. Understanding that model explains mutability, identity, default argument bugs, and object sharing.", ["object model", "references", "identity"], "`a = b` binds a second name to the same object, not a deep copy.", "whether you understand Python fundamentals deeply enough to avoid subtle bugs."),
        ],
    },
    {
        "id": "epam-python-functions",
        "title": "EPAM Python Functions and Modules",
        "description": "Function signatures, args/kwargs, defaults, lambdas, comprehensions, exceptions, imports, packages, modules, and virtual environments.",
        "tags": ["python", "functions", "imports", "exceptions"],
        "lessons": [
            ("Function Signatures", ["functions", "args", "kwargs", "positional-only", "keyword-only"]),
            ("Defaults, Lambdas, and Comprehensions", ["default arguments", "lambda", "list comprehension", "generator expression"]),
            ("Exceptions and Best Practices", ["try", "except", "finally", "custom exceptions"]),
            ("Imports, Packages, and Environments", ["imports", "modules", "packages", "__init__.py", "venv"]),
        ],
        "questions": [
            ("*args", "What does `*args` capture in a Python function?", "Extra positional arguments as a tuple", ["Extra keyword arguments as a dict", "Only required parameters", "Environment variables"], "`*args` gathers extra positional arguments into a tuple. It is useful for wrappers and flexible APIs.", ["functions", "*args", "positional arguments"], "def f(*args): return args", "whether you understand Python call binding."),
            ("**kwargs", "What does `**kwargs` capture?", "Extra keyword arguments as a dictionary", ["Extra positional arguments", "Only default values", "Imported modules"], "`**kwargs` gathers extra keyword arguments into a dictionary. It is common in decorators and API adapters.", ["functions", "**kwargs", "keyword arguments"], "def f(**kwargs): return kwargs['limit']", "whether you understand flexible function APIs."),
            ("Positional-only Args", "Why use positional-only parameters?", "To prevent callers from depending on parameter names", ["To make arguments mutable", "To disable type hints", "To create threads"], "Positional-only parameters let API authors change internal parameter names without breaking callers.", ["positional-only", "function signatures"], "def distance(x, y, /): ...", "whether you understand public API compatibility."),
            ("Keyword-only Args", "Why make an argument keyword-only?", "To force clarity at call sites", ["To make it global", "To skip validation", "To speed up loops"], "Keyword-only arguments are useful for flags and options where positional calls would be ambiguous.", ["keyword-only", "function signatures"], "def connect(url, *, timeout=5): ...", "whether you can design readable function interfaces."),
            ("Default Argument Pitfall", "What is wrong with `def add_item(item, bucket=[]): bucket.append(item)`?", "The same list is reused across calls", ["The list is copied every call", "append returns a new list", "Default arguments are evaluated at return time"], "Default argument values are evaluated once when the function is defined. Mutable defaults can accidentally share state.", ["default arguments", "mutable", "pitfall"], "Use `bucket=None` and create a new list inside.", "whether you know one of Python's most common production bugs."),
            ("Lambda Functions", "When is a lambda appropriate?", "A small single-expression callback", ["Complex business logic", "A replacement for every named function", "Exception handling blocks"], "Lambdas are anonymous single-expression functions. They are useful when concise and harmful when they reduce readability.", ["lambda", "functions", "readability"], "sorted(users, key=lambda user: user.last_login)", "whether you balance Pythonic syntax with maintainability."),
            ("List Comprehension", "What does `[x * x for x in nums if x > 0]` create?", "A new list eagerly", ["A lazy iterator", "A dictionary", "A set"], "List comprehensions build a list immediately. They are concise but still allocate the full result.", ["list comprehension", "eager evaluation"], "squares = [n*n for n in nums]", "whether you know comprehension behavior and memory cost."),
            ("Dict Comprehension", "Which expression builds a lookup by user id?", "{user.id: user for user in users}", ["[user.id for user in users]", "(user.id for user in users)", "{user.id for user in users}"], "Dict comprehensions create key-value mappings. They are useful for fast lookup by ID.", ["dict comprehension", "dictionary"], "users_by_id = {u.id: u for u in users}", "whether you can transform data into useful access structures."),
            ("Set Comprehension", "Which expression builds unique countries?", "{user.country for user in users}", ["[user.country: user]", "(user.country = users)", "{user.country: users}"], "Set comprehensions produce unique values. They are useful for deduplication.", ["set comprehension", "unique values"], "countries = {row.country for row in rows}", "whether you know collection-specific comprehensions."),
            ("Generator Expressions", "Why use `(row.id for row in rows)`?", "It produces IDs lazily", ["It sorts rows", "It creates a reusable list", "It catches exceptions"], "Generator expressions produce one value at a time and can reduce memory pressure.", ["generator expression", "lazy evaluation"], "sum(row.amount for row in transactions)", "whether you understand lazy iteration."),
            ("Exceptions", "Which exception handler is best practice?", "Catch the specific exception you can handle", ["Catch all exceptions and ignore them", "Use finally instead of except", "Return None for every error"], "Specific exception handling keeps unexpected bugs visible while handling known failures cleanly.", ["try", "except", "finally", "custom exceptions"], "except InvalidTokenError: return 401", "whether you handle errors intentionally."),
            ("Packages and Virtual Environments", "What is the role of a virtual environment?", "Isolate project dependencies", ["Compile Python to Java", "Replace imports", "Create database indexes"], "Virtual environments keep dependencies per project. Packages and modules organize code, and `__init__.py` initializes package namespaces.", ["imports", "modules", "packages", "__init__.py", "virtual environments"], "Use `.venv` so FastAPI dependencies do not conflict with another project.", "whether you can structure and run Python projects reliably."),
        ],
    },
]

EPAM_MODULES.extend([
    {
        "id": "epam-python-oop",
        "title": "EPAM Python OOP",
        "description": "Classes, objects, encapsulation, inheritance, composition, polymorphism, dataclasses, ABCs, protocols, DI, special methods, iterators, generators, decorators, and context managers.",
        "tags": ["python", "oop", "dataclasses", "protocols"],
        "lessons": [
            ("OOP Fundamentals", ["classes", "objects", "encapsulation", "inheritance"]),
            ("Composition and Polymorphism", ["composition", "polymorphism", "dependency injection"]),
            ("Advanced OOP", ["dataclasses", "abstract base classes", "protocols", "special methods"]),
            ("Python Control Abstractions", ["iterable", "iterators", "generators", "decorators", "context managers"]),
        ],
        "questions": [
            ("Classes and Objects", "What is an object in Python OOP?", "An instance of a class with state and behavior", ["A package directory only", "A database row only", "A function argument marker"], "Classes define structure and behavior; objects are runtime instances. Python objects carry attributes and methods according to their class.", ["classes", "objects", "oop"], "A `User` class can create many user objects with different emails.", "whether you understand basic object modeling."),
            ("Encapsulation", "Why hide direct mutation behind methods or properties?", "To protect invariants and keep state changes controlled", ["To make testing impossible", "To avoid constructors", "To force inheritance"], "Encapsulation keeps object state consistent by exposing intentional operations instead of unrestricted mutation.", ["encapsulation", "invariants", "oop"], "Use `account.withdraw(amount)` rather than mutating `balance` freely.", "whether you design objects that protect business rules."),
            ("Inheritance", "When is inheritance a good fit?", "When the subtype truly is a specialized version of the base type", ["Whenever two classes share one field", "To avoid all composition", "For unrelated utilities"], "Inheritance models is-a relationships. Overusing it creates rigid hierarchies and fragile coupling.", ["inheritance", "is-a", "oop"], "`AdminUser` may specialize `User` if it preserves the User contract.", "whether you understand inheritance trade-offs."),
            ("Composition", "Why prefer composition for many service designs?", "Collaborators can be injected and replaced independently", ["It disables polymorphism", "It removes all classes", "It makes state global"], "Composition builds behavior by combining objects. It often makes code easier to test and change than deep inheritance.", ["composition", "dependency injection", "services"], "NotificationService can receive EmailSender and SmsSender collaborators.", "whether you can design flexible services."),
            ("Polymorphism", "What does polymorphism mean in Python practice?", "Different objects can be used through the same expected behavior", ["Every class needs the same parent", "Only numbers can be compared", "Objects cannot be swapped"], "Python often uses duck typing: if an object provides the needed behavior, it can be used.", ["polymorphism", "duck typing", "protocols"], "Any object with `.send(message)` can satisfy a notification sender role.", "whether you understand behavior-based design."),
            ("Dataclasses", "When should you consider a dataclass?", "For simple data containers with generated init/repr/equality", ["For every service class", "For async event loops", "For SQL joins"], "Dataclasses reduce boilerplate for value-like objects. They are not a substitute for all domain logic.", ["dataclasses", "__init__", "__repr__", "__eq__"], "@dataclass class ForecastPoint: date: str; value: float", "whether you know modern Python data modeling tools."),
            ("Abstract Base Classes", "What does an ABC communicate?", "Required methods for subclasses through inheritance", ["A JSON schema", "A package initializer", "A thread lock"], "Abstract Base Classes define contracts that subclasses must implement. They are useful when inheritance is the intended relationship.", ["abstract base classes", "abc", "interfaces"], "An abstract Repository can require `get_by_id` and `save`.", "whether you can define explicit object contracts."),
            ("Protocols", "Why use a Protocol?", "To express structural typing without requiring inheritance", ["To start a web server", "To catch all exceptions", "To replace dictionaries"], "Protocols let any object with the right methods satisfy an interface. They fit Python's duck-typing style while helping type checkers.", ["protocols", "structural typing", "dependency injection"], "A fake repository can satisfy a Repository Protocol in tests.", "whether you understand Pythonic interfaces."),
            ("Special Methods", "Why keep `__eq__` and `__hash__` consistent?", "Objects used in sets/dicts rely on stable equality and hash behavior", ["They control imports", "They start generators", "They handle JWTs"], "`__eq__` defines equality and `__hash__` supports hashed collections. Equal objects should have equal hashes.", ["__eq__", "__hash__", "__repr__", "__str__"], "A value object used as a dict key needs stable hashable fields.", "whether you understand Python object behavior in collections."),
            ("Iterators and Generators", "What does `yield` do?", "Produces a value and pauses generator state", ["Creates a thread", "Commits a transaction", "Imports a package"], "An iterable can produce an iterator, and generators produce values lazily. They are useful for streaming and large sequences.", ["iterable", "iterators", "generators", "yield", "lazy evaluation"], "Yield rows from a large CSV instead of loading all rows into memory.", "whether you understand lazy evaluation."),
            ("Decorators", "What is a practical decorator use?", "Wrap a function with logging, timing, auth, or retry behavior", ["Change a tuple into a list", "Declare a SQL JOIN", "Create a virtualenv"], "Decorators add cross-cutting behavior around functions while keeping the function call interface.", ["decorators", "function decorators", "practical uses"], "@timed can record function duration without changing business logic.", "whether you can recognize framework patterns like route decorators."),
            ("Context Managers", "What does a context manager guarantee?", "Setup and cleanup around a block", ["Only faster loops", "Automatic sharding", "Password hashing"], "`with` calls `__enter__` and `__exit__`, making cleanup reliable even if an exception occurs.", ["context managers", "with", "__enter__", "__exit__"], "Use `with open(path) as f:` so files close automatically.", "whether you understand resource management."),
        ],
    },
    {
        "id": "epam-fastapi-architecture",
        "title": "EPAM FastAPI Architecture",
        "description": "FastAPI routing, dependency injection, Pydantic validation, middleware, JWT auth, background tasks, async endpoints, API design, and layered architecture.",
        "tags": ["fastapi", "api design", "jwt", "architecture"],
        "lessons": [
            ("FastAPI Request Flow", ["routing", "dependency injection", "pydantic", "validation"]),
            ("Auth, Middleware, and Errors", ["middleware", "authentication", "jwt", "error handling"]),
            ("API Design", ["rest", "status codes", "pagination", "filtering", "versioning"]),
            ("Service Architecture", ["service layer", "repository pattern", "dtos", "project structure"]),
        ],
        "questions": [
            ("FastAPI Routing", "Where should HTTP path and method mapping live?", "Router layer", ["Repository layer", "Database index", "Model weights"], "Routers map HTTP requests to endpoint functions. They should stay thin and delegate business work.", ["fastapi", "routing", "router"], "APIRouter(prefix='/api/users') groups user endpoints.", "whether you understand FastAPI request organization."),
            ("Dependency Injection", "A DB session must be replaceable in tests. What FastAPI feature helps?", "Depends dependency injection", ["Global variable only", "Hardcoded psycopg2 connection", "Client-side cookie"], "FastAPI dependencies provide request-scoped collaborators and can be overridden in tests.", ["dependency injection", "Depends", "testing"], "Use Depends(get_db) for a request-scoped session.", "whether you can build testable FastAPI APIs."),
            ("Pydantic Validation", "Where should invalid request shapes fail?", "Pydantic request validation", ["Inside dashboard CSS", "After database commit", "In Docker build only"], "Pydantic validates types and constraints before business logic runs.", ["pydantic", "validation", "schemas"], "Reject a missing `email` field before user creation logic.", "whether you use schemas as API boundaries."),
            ("Middleware", "What belongs in middleware?", "Cross-cutting request/response behavior", ["SQL aggregation only", "ML training loops", "React state"], "Middleware wraps requests for concerns like CORS, logging, timing, auth context, and error envelopes.", ["middleware", "cors", "logging"], "Add request ID logging in middleware.", "whether you understand request pipeline hooks."),
            ("JWT Authentication", "What should a JWT-protected endpoint verify?", "Token signature, expiry, and claims", ["Only UI route name", "Only JSON formatting", "Only database index"], "JWT authentication must verify the token and map trusted claims to an identity/authorization decision.", ["authentication", "jwt", "authorization"], "Reject expired bearer tokens before accessing organization data.", "whether you understand stateless API auth risks."),
            ("Background Tasks", "When is a FastAPI background task appropriate?", "Non-critical work after response", ["Required transaction commit", "Immediate password validation", "Blocking CPU-heavy forecasting"], "Background tasks fit follow-up work that does not need to block the response. Heavy jobs usually deserve workers/queues.", ["background tasks", "async", "fastapi"], "Send a notification after returning a successful response.", "whether you can separate request latency from follow-up work."),
            ("Async Endpoints", "When does `async def` help in FastAPI?", "While awaiting I/O-bound operations", ["For pure CPU loops", "For SQL syntax", "For CSS rendering"], "Async endpoints help when work spends time waiting on I/O. CPU-heavy work needs workers or processes.", ["async endpoints", "async", "io"], "Await an HTTP integration call without blocking the event loop.", "whether you understand async FastAPI correctly."),
            ("Error Handling", "What should API error handling produce?", "Consistent status codes and response shape", ["Raw stack traces to clients", "Silent failures", "HTML-only pages"], "Clients need predictable errors. Internal details should be logged, not leaked.", ["error handling", "status codes", "api design"], "Return 404 for missing resource and 422 for validation failure.", "whether you design reliable API contracts."),
            ("Pagination and Filtering", "Why paginate dashboard data APIs?", "To bound response size and latency", ["To remove authentication", "To avoid indexes forever", "To replace validation"], "Pagination and filtering keep APIs efficient and usable as data grows.", ["pagination", "filtering", "api design"], "GET /events?limit=50&cursor=abc&source=hubspot", "whether you understand scalable API access patterns."),
            ("Versioning", "What protects clients from breaking API changes?", "Versioned or backward-compatible contracts", ["Silent response shape changes", "Deleting old fields immediately", "Skipping docs"], "API versioning and compatibility policies let clients migrate safely.", ["versioning", "api design", "contract"], "Add /v2 or optional fields instead of breaking /v1.", "whether you manage API evolution."),
            ("Service Layer", "Why use a service layer?", "To keep business logic out of route handlers", ["To hide all tests", "To store CSS", "To replace HTTP"], "Services make business logic reusable and testable outside HTTP concerns.", ["service layer", "architecture"], "DashboardService builds KPI widgets after route validation.", "whether you can structure backend code beyond endpoints."),
            ("Repository Pattern and DTOs", "What is the repository pattern for?", "Isolating persistence behind a focused interface", ["Rendering React pages", "Storing secrets in code", "Sorting CSS"], "Repositories isolate database access; DTOs/schemas define transfer boundaries.", ["repository pattern", "dtos", "project structure"], "ForecastRepository can hide SQL while service code asks for forecast history.", "whether you understand layered backend architecture."),
        ],
    },
])

EPAM_MODULES.extend([
    {
        "id": "forecast-alpha-defense",
        "title": "Forecast Alpha Project Defense",
        "description": "Interview defense for Forecast Alpha architecture, database, OAuth/JWT authentication, connected data sources, ML forecasting, anomaly detection, intelligence flow, notifications, collaboration, usage, and lessons learned.",
        "tags": ["forecast alpha", "saas", "fastapi", "nextjs", "oauth", "jwt", "notifications", "collaboration", "usage"],
        "lessons": [
            ("Architecture and Product Flow", ["next.js", "fastapi", "saas", "workspace"]),
            ("Data Connections and Platform Database", ["postgresql", "connections", "materialization", "schemas"]),
            ("ML and Intelligence", ["forecasting", "anomaly detection", "semantic model", "sql builder"]),
            ("Operations and Lessons Learned", ["oauth", "jwt", "authentication", "notifications", "collaboration", "usage", "testing"]),
        ],
        "questions": [
            ("Forecast Alpha Architecture", "How should you summarize Forecast Alpha's high-level architecture?", "Next.js frontend plus FastAPI backend over a platform PostgreSQL database", ["Single static HTML page", "Only a local notebook", "No backend"], "Forecast Alpha is a SaaS-style analytics platform with Next.js 14 frontend, FastAPI backend, PostgreSQL platform database, ML services, and connected-source workflows.", ["forecast alpha", "next.js", "fastapi", "postgresql"], "Frontend App Router pages call FastAPI through app/lib/backend.js or the Next API proxy.", "whether you can explain your own system architecture clearly."),
            ("Frontend App Router", "Where do core Forecast Alpha product pages live?", "Under the Next.js app directory", ["backend/app/routes only", "sample_data only", "Dockerfile only"], "The frontend uses the Next.js App Router with pages such as dashboard, forecasting, anomalies, intelligence, explorer, connect, login, and signup.", ["next.js", "app router", "frontend"], "app/dashboard/page.js drives dashboard setup and KPI workflow.", "whether you know your frontend structure."),
            ("API Wrapper and Proxy", "What is the role of app/lib/backend.js and app/api/[...path]/route.js?", "Attach auth/error handling and proxy API calls to FastAPI", ["Train XGBoost models", "Define SQL tables", "Run pytest fixtures"], "The frontend API wrapper adds JSON headers, attaches Supabase bearer tokens when available, handles errors, and can route requests through the Next proxy to FastAPI.", ["api wrapper", "proxy", "supabase token"], "The proxy forwards /api/... requests to the configured backend URL.", "whether you understand frontend-backend integration."),
            ("Protected Routes", "How are protected frontend routes controlled?", "Middleware checks Supabase session cookies or forecast_session", ["Only CSS classes", "Only PostgreSQL indexes", "Only LightGBM"], "middleware.js redirects unauthenticated users to /login by checking Supabase or local session cookies. Forecast Alpha also needs clear OAuth/JWT boundaries between frontend sessions and backend bearer-token authorization.", ["oauth", "jwt", "authentication", "middleware", "protected routes"], "A dashboard visit without a valid session redirects to login; a backend API call includes a verified bearer token.", "whether you understand web auth flow."),
            ("Backend Startup", "What happens in backend/app/main.py startup?", "Create app, configure CORS, register routers, initialize schemas, start connection refresh scheduler", ["Render React components", "Train every model synchronously", "Delete sample data"], "The FastAPI entry point configures operational concerns and exposes /, /healthz, and /readyz.", ["fastapi", "cors", "startup", "readiness"], "Readiness should reflect whether dependencies such as platform DB are usable.", "whether you know backend lifecycle responsibilities."),
            ("Platform Database", "Which environment variable configures the platform PostgreSQL database?", "PLATFORM_DATABASE_URL or data_url", ["NEXT_PUBLIC_SITE_TITLE only", "ASSISTANT_LEXICAL_WEIGHT", "PORTFOLIO_THEME"], "Forecast Alpha uses a platform PostgreSQL database through backend/app/platform_db.py.", ["postgresql", "platform database", "environment variables"], "Connection metadata and platform-managed schemas live in PostgreSQL.", "whether you understand configuration and persistence."),
            ("Connection Service", "What does connection_service.py do in the main product flow?", "Validates and stores connected data sources, then supports schema scanning/profile creation", ["Renders landing pages", "Runs browser middleware", "Builds Docker images"], "Users connect sources; the backend validates/stores the connection, scans schema, and creates profiles used by dashboards and intelligence.", ["connection service", "schema scanning", "data sources"], "Connect a PostgreSQL or CSV source, then generate KPI recommendations.", "whether you can explain ingestion and onboarding."),
            ("Supported Data Sources", "Which source list matches Forecast Alpha's connector scope?", "postgres, hubspot, csv, google_sheets, mysql, bigquery, mssql, oracle", ["Only SQLite", "Only Google Sheets", "Only PostgreSQL and Redis"], "The platform supports several source types and can materialize/mirror some source data into managed schemas.", ["data sources", "hubspot", "csv", "google sheets", "bigquery"], "CSV, Google Sheets, HubSpot, and external databases use dedicated service modules.", "whether you understand integration breadth and trade-offs."),
            ("Forecasting ML", "What does backend/app/ml/forecasting.py support?", "Moving-average baseline plus Random Forest, Gradient Boosting, XGBoost, and LightGBM depending on data volume", ["Only GPT prompts", "Only SQL joins", "Only static charts"], "Forecasting combines statistical baseline and ML models selected by data volume and suitability.", ["forecasting", "random forest", "xgboost", "lightgbm"], "Use a simple moving average when data is limited; use stronger ML when history supports it.", "whether you understand pragmatic ML model selection."),
            ("Natural-Language Intelligence", "What is the intelligence service pattern?", "Classify question, resolve semantic mappings, plan query, build SQL, execute, render answer/chart", ["Send every question directly to SQL", "Ignore semantic model", "Return raw database rows only"], "The intelligence flow is centered around planner, SQL builder, and result renderer services.", ["intelligence", "semantic model", "query planner", "sql builder"], "A user asks for revenue trend; the planner maps terms to schema and builds chart-ready SQL.", "whether you can explain AI-assisted analytics architecture."),
            ("Tests and Risk", "What do current backend tests cover?", "Launch health, readiness, route registration, cookie settings, and intelligence visualization planning", ["Every production ML model fully", "Only frontend CSS", "No backend behavior"], "The existing tests cover important startup and planning behavior but leave room for deeper connection, forecasting, and deployed intelligence tests.", ["testing", "readiness", "route registration", "visualization planning"], "Add tests around connection_service and forecasting edge cases next.", "whether you can discuss test coverage honestly."),
            ("Lessons Learned", "What is a strong Forecast Alpha lessons-learned answer?", "Discuss integration complexity, schema variability, auth boundaries, model selection, and observability trade-offs", ["Claim everything was easy", "Avoid mentioning trade-offs", "Only list libraries"], "Project defense should cover architecture, database, OAuth/JWT authentication, AI flow, notifications, collaboration, usage tracking, challenges, lessons learned, and next improvements.", ["lessons learned", "architecture", "oauth", "jwt", "notifications", "collaboration", "usage", "ai flow"], "Explain how multi-source schema variability shaped the semantic model and query planner, and how notifications/collaboration/usage routes fit the SaaS platform.", "whether you can reflect like an engineer who owned the system."),
        ],
    },
    {
        "id": "portfolio-assistant-llm",
        "title": "Portfolio Assistant LLM Defense",
        "description": "Interview defense for a custom retrieval-based portfolio chatbot using FastAPI, TF-IDF, ONNX MiniLM embeddings, query rules, artifacts, training data, evaluation, Docker, and caveats.",
        "tags": ["portfolio assistant", "retrieval", "tf-idf", "onnx"],
        "lessons": [
            ("Live API Flow", ["fastapi", "chat endpoint", "schemas", "health"]),
            ("Hybrid Retrieval Model", ["tf-idf", "cosine similarity", "onnx", "minilm", "embeddings"]),
            ("Training, Artifacts, and Experiments", ["training data", "artifacts", "evaluation", "bilstm"]),
            ("Deployment and Test Caveats", ["docker", "configuration", "tests", "production path"]),
        ],
        "questions": [
            ("Portfolio Chat API", "What is the production endpoint for the portfolio chatbot?", "POST /chat", ["POST /forecasting", "GET /readyz", "POST /semantic-model"], "The FastAPI backend exposes /, /health, and POST /chat. /chat calls answer_from_messages() for production chatbot behavior.", ["fastapi", "chat endpoint", "portfolio assistant"], "A frontend sends messages to POST /chat and receives a portfolio-specific answer.", "whether you know your deployed API flow."),
            ("Request Schema", "What does the chat request send?", "A messages array with role/content plus request metadata", ["Only a raw string file path", "Only SQL rows", "Only Docker layers"], "The schema accepts chat messages, and the backend finds the latest user message before answering.", ["schema", "messages", "request flow"], "{\"messages\":[{\"role\":\"user\",\"content\":\"Tell me about Hisham\"}]}", "whether you understand request modeling."),
            ("Production Model Type", "What is the production chatbot model?", "A retrieval-based hybrid retriever", ["A direct OpenAI API call only", "The BiLSTM experiment", "A random response generator"], "The live model maps user queries to trained portfolio Q&A targets using lexical and optional semantic retrieval.", ["retrieval", "hybrid model", "production"], "answer_from_messages() searches trained examples and returns the best target_text.", "whether you can distinguish production architecture from experiments."),
            ("TF-IDF Lexical Matching", "What does the lexical part use?", "TF-IDF cosine similarity over normalized tokens", ["JWT signatures", "PostgreSQL EXPLAIN", "LightGBM trees"], "TF-IDF gives strong keyword-based retrieval and is easy to inspect/debug.", ["tf-idf", "cosine similarity", "lexical matching"], "A query mentioning 'GitHub' can match portfolio examples containing GitHub-related terms.", "whether you understand classic IR foundations."),
            ("Semantic Matching", "What adds semantic matching if enabled?", "ONNX MiniLM embeddings", ["Docker Compose", "SQL CTEs", "React middleware"], "The semantic path uses MiniLM embeddings from ONNX artifacts when enabled and available.", ["onnx", "minilm", "embeddings", "semantic matching"], "Compare query embedding against portfolio_embeddings.npz.", "whether you understand local embedding-based retrieval."),
            ("Query Rules", "Why include aliases and follow-up expansion?", "To normalize user intent before retrieval", ["To bypass confidence thresholds", "To train XGBoost", "To replace FastAPI"], "Rules handle common terms such as github/resume and vague follow-ups like 'tell me more'.", ["query rules", "aliases", "follow-up expansion"], "Map 'his backend work' to Hisham backend portfolio context.", "whether you can improve retrieval UX without an external LLM."),
            ("Third-Person Rewriting", "Why rewrite first-person answers into third person?", "To match questions asking about Hisham or his work", ["To change embeddings", "To avoid JSON", "To skip tests"], "The assistant can adapt answer perspective so portfolio content sounds natural to visitors.", ["third-person rewriting", "response rendering"], "Convert 'I built Forecast Alpha' into 'Hisham built Forecast Alpha'.", "whether you notice product polish around generated responses."),
            ("Fallback Behavior", "When should the assistant return 'I'm still learning that part...'?", "When retrieval confidence is below threshold or topic is unknown", ["Whenever query is long", "Whenever semantic mode is enabled", "After every GitHub question"], "A deterministic fallback is safer than hallucinating unsupported portfolio claims.", ["confidence threshold", "fallback", "hallucination"], "Unknown personal questions should not produce invented biography.", "whether you understand safe AI behavior."),
            ("Runtime Artifacts", "Which artifacts support runtime retrieval?", "portfolio_retriever.json, portfolio_embeddings.npz, and ONNX MiniLM config", ["Only package-lock.json", "Only sample SQL", "Only middleware.js"], "The production retriever loads trained lexical data and optional semantic embeddings/model config.", ["artifacts", "portfolio_retriever.json", "portfolio_embeddings.npz"], "model/artifacts/portfolio_retriever.json stores retrieval state.", "whether you understand model packaging."),
            ("Training Data", "What is data/conversations.json used for?", "Supervised portfolio Q&A examples for retrieval training", ["Database migrations", "Docker image layers", "Frontend auth cookies"], "The dataset helpers clean examples into lookup maps and input/target samples.", ["training data", "dataset", "conversations.json"], "Training examples connect user phrasing to desired target_text.", "whether you understand how your local model learns behavior."),
            ("Experiment vs Production", "What is the BiLSTM area?", "An isolated research experiment, not the production /chat retriever", ["The only deployed model", "A database service", "A Next.js page"], "The generative BiLSTM encoder/decoder with attention is experimental and should not replace production retrieval without evaluation.", ["bilstm", "experiment", "production caveat"], "Keep experiments/generative_bilstm separate from model/portfolio_llm.py.", "whether you can separate research from production reliability."),
            ("Tests and Caveat", "What is the important test caveat?", "Tests import backend.model.inference while live API imports model.portfolio_llm", ["No tests exist", "Tests fully cover production chat", "Tests only check CSS"], "Current tests cover API/training/inference basics, dataset cleaning, and tokenization, but do not fully exercise the deployed chat behavior.", ["tests", "production path", "caveat"], "Add a test that POST /chat exercises answer_from_messages() from model/portfolio_llm.py.", "whether you can honestly identify coverage gaps."),
        ],
    },
])

EPAM_MODULES.extend([
    {
        "id": "epam-testing-devops-git",
        "title": "EPAM Testing, DevOps, and Git",
        "description": "pytest, fixtures, mocking, integration/e2e tests, Docker, docker-compose, Git branching, rebasing, pull requests, GitHub Actions, and CI/CD pipelines.",
        "tags": ["pytest", "docker", "git", "ci/cd"],
        "lessons": [
            ("Testing Strategy", ["pytest", "fixtures", "mocking", "integration tests"]),
            ("End-to-End and Quality Gates", ["end-to-end tests", "coverage", "ci"]),
            ("Docker Workflow", ["docker", "images", "containers", "dockerfile", "docker-compose"]),
            ("Git Collaboration", ["git", "branching", "rebasing", "pull requests", "github actions"]),
        ],
        "questions": [
            ("pytest", "Why is pytest common in Python backend teams?", "It provides simple tests, fixtures, and rich assertions", ["It deploys containers", "It replaces Git", "It builds SQL indexes"], "pytest makes Python tests concise and supports reusable setup through fixtures.", ["pytest", "testing"], "Use pytest to test a FastAPI service function and API route.", "whether you can work in standard Python testing workflows."),
            ("Fixtures", "What is a fixture best used for?", "Reusable setup and teardown", ["Changing production data manually", "Skipping assertions", "Creating Git branches"], "Fixtures prepare test state such as temporary databases, clients, or fake dependencies.", ["fixtures", "pytest", "setup"], "A `client` fixture creates a FastAPI TestClient.", "whether you write maintainable tests."),
            ("Mocking", "What should you usually mock?", "Slow or external boundaries", ["The function under test", "Every line of code", "All assertions"], "Mocks replace external APIs, email providers, payment gateways, or nondeterministic services.", ["mocking", "test doubles"], "Mock HubSpot API calls while testing connection logic.", "whether you isolate tests without hiding the behavior being tested."),
            ("Integration Tests", "What does an integration test verify?", "Multiple real components working together", ["One pure function only", "A Git rebase", "A CSS class name"], "Integration tests cover boundaries like API route plus database or service plus repository.", ["integration tests", "backend"], "POST /connect stores a validated database connection in a test database.", "whether you can test real application wiring."),
            ("End-to-End Tests", "What does an E2E test focus on?", "A user workflow through the system", ["One SQL expression", "One Python lambda", "One import statement"], "End-to-end tests exercise the app like a user, usually with more cost and fewer cases.", ["end-to-end tests", "workflow"], "Signup, connect data source, view dashboard.", "whether you understand test levels and trade-offs."),
            ("Docker Images and Containers", "What is the difference between image and container?", "Image is the artifact; container is a running instance", ["Container builds Dockerfile", "Image is only logs", "They are unrelated"], "A Dockerfile builds an image; Docker runs containers from that image.", ["docker", "images", "containers"], "Build a Python 3.12 slim image then run uvicorn inside a container.", "whether you understand container basics."),
            ("Dockerfile", "What should a Dockerfile make explicit?", "Runtime dependencies and startup command", ["Only browser cookies", "Only pull request title", "Only database rows"], "A Dockerfile describes a reproducible runtime image.", ["dockerfile", "docker", "dependencies"], "Install requirements.txt, copy backend, run uvicorn.", "whether you can package an app for deployment."),
            ("docker-compose", "When is docker-compose useful?", "Running multiple local services together", ["Rebasing a branch", "Writing SQL HAVING", "Training embeddings only"], "Compose coordinates local containers such as app, database, Redis, and workers.", ["docker-compose", "local dev"], "Run FastAPI plus PostgreSQL locally with one command.", "whether you can build realistic local environments."),
            ("Git Branching", "Why create feature branches?", "To isolate work before review/merge", ["To bypass CI", "To delete tests", "To change Python syntax"], "Branches let engineers collaborate without committing directly to main.", ["git", "branching"], "Create `feature/forecasting-api` for a scoped change.", "whether you understand team workflow."),
            ("Rebasing", "What is a common reason to rebase?", "Replay your branch on latest main for a cleaner history", ["Hide failing tests", "Delete commits from main", "Run Docker"], "Rebasing rewrites branch history, so use it carefully and avoid rebasing shared branches without coordination.", ["rebasing", "git"], "Rebase a local feature branch before opening a PR.", "whether you understand Git history management."),
            ("Pull Requests", "What is the purpose of a pull request?", "Review, discuss, and validate a change before merge", ["Replace tests", "Store secrets", "Run SQL only"], "PRs create a collaboration and quality gate around code changes.", ["pull requests", "code review"], "A PR includes tests, summary, and linked issue.", "whether you can work in professional team processes."),
            ("GitHub Actions and CI/CD", "What should a basic GitHub Actions pipeline do?", "Install dependencies, run tests, and build before merge/deploy", ["Commit secrets", "Skip lint", "Deploy untested code"], "CI validates changes automatically. CD deploys a known artifact after checks pass.", ["github actions", "ci/cd", "pipeline"], "Run pytest and npm test on each pull request.", "whether you understand automated delivery safeguards."),
        ],
    },
    {
        "id": "epam-ai-system-design",
        "title": "EPAM AI and System Design",
        "description": "LLM APIs, embeddings, vector databases, RAG, prompt engineering, token limits, streaming, cost optimization, and system design drills.",
        "tags": ["ai", "llm", "system design", "rag"],
        "lessons": [
            ("AI Building Blocks", ["llm apis", "embeddings", "vector databases", "rag"]),
            ("Prompting and Runtime Constraints", ["prompt engineering", "token limits", "streaming", "cost optimization"]),
            ("Classic System Designs", ["url shortener", "chat api", "notification service"]),
            ("AI API Design", ["ai api", "auth", "rate limits", "observability"]),
        ],
        "questions": [
            ("LLM APIs", "What should production code assume about LLM output?", "It may be wrong and needs validation/evaluation", ["It is always deterministic truth", "It removes tests", "It cannot leak data"], "LLM APIs are probabilistic and can hallucinate. Production systems need validation, evals, fallback, and monitoring.", ["llm apis", "evaluation", "hallucination"], "Validate an AI-generated KPI recommendation before showing it as final.", "whether you understand AI reliability."),
            ("Embeddings", "What are embeddings used for?", "Representing text meaning as vectors for similarity search", ["Encrypting JWTs", "Creating SQL joins", "Starting Docker"], "Embeddings map content into vector space so related meanings can be found by similarity.", ["embeddings", "vector search"], "Embed support docs and search for chunks relevant to a user question.", "whether you know AI retrieval basics."),
            ("Vector Databases", "Why use a vector database?", "Efficient similarity search over embeddings", ["Relational foreign-key enforcement", "Static type checking", "Git branching"], "Vector databases index embeddings for nearest-neighbor retrieval.", ["vector databases", "embeddings", "similarity search"], "Find portfolio Q&A examples closest to a chat query.", "whether you understand retrieval infrastructure."),
            ("RAG", "What does RAG add to an LLM flow?", "Retrieves relevant context before generation", ["Ignores source data", "Always fine-tunes the model", "Deletes token limits"], "RAG grounds answers in retrieved documents or examples, useful for changing/private knowledge.", ["rag", "retrieval", "grounding"], "Retrieve schema notes before answering a dashboard intelligence question.", "whether you can reduce hallucination through architecture."),
            ("Prompt Engineering", "What is a good prompt engineering goal?", "Constrain task, context, format, and refusal behavior", ["Make prompts longer forever", "Hide errors", "Skip retrieval"], "Prompts should specify role, task, constraints, source use, output format, and fallback behavior.", ["prompt engineering", "guardrails"], "Ask the model to answer only from retrieved KPI metadata.", "whether you can shape AI behavior deliberately."),
            ("Token Limits", "Why do token limits matter?", "They constrain context size, cost, and latency", ["They replace authentication", "They ensure truth", "They create SQL indexes"], "Token limits force context selection and summarization. More tokens usually cost more and add latency.", ["token limits", "cost optimization", "latency"], "Chunk and retrieve only relevant documents instead of sending everything.", "whether you understand model runtime constraints."),
            ("Streaming", "Why stream chat responses?", "Improve perceived latency for users", ["Guarantee correctness", "Avoid auth", "Replace retrieval"], "Streaming sends partial output as it is generated. It helps UX but does not solve factuality.", ["streaming", "chat api", "latency"], "A chat UI can show tokens as they arrive.", "whether you separate UX latency from answer quality."),
            ("Cost Optimization", "What is a practical AI cost control?", "Limit context, cache safe results, and choose model size by evals", ["Send all data always", "Disable logging", "Retry infinitely"], "AI cost depends on model, tokens, traffic, retries, and caching. Optimize with measurement and quality gates.", ["cost optimization", "tokens", "evals"], "Use a smaller model for classification and a stronger one for complex generation.", "whether you can run AI features economically."),
            ("URL Shortener", "What is the core storage design for a URL shortener?", "Map short codes to long URLs with collision handling", ["Store only CSS", "Use no database", "Require vector search"], "URL shorteners test key generation, redirects, storage, TTLs, analytics, and collision handling.", ["url shortener", "system design"], "short_code -> destination_url with unique constraint.", "whether you can design a simple scalable service."),
            ("Chat API", "What must a chat API usually manage?", "Conversation state, auth, rate limits, streaming, and persistence", ["Only static HTML", "Only Docker layers", "Only GROUP BY"], "Chat APIs combine HTTP/WebSocket/SSE behavior with state, moderation, cost, and latency concerns.", ["chat api", "streaming", "auth"], "Store conversation IDs and stream assistant output.", "whether you can design interactive APIs."),
            ("Notification Service", "Why use a queue in a notification service?", "To decouple send requests from provider delivery", ["To remove retries", "To skip templates", "To force synchronous latency"], "Notifications involve templates, channels, provider failures, retries, idempotency, and user preferences.", ["notification service", "queue", "retries"], "Queue email/SMS jobs and process with workers.", "whether you understand async delivery systems."),
            ("AI API", "What should an AI API expose besides the answer?", "Status, errors, usage/cost metadata, and traceable behavior", ["Only raw model text", "No auth", "No limits"], "AI APIs need normal API discipline plus model-specific observability, rate limits, and safety behavior.", ["ai api", "usage", "observability"], "Return answer plus retrieved source IDs and token usage.", "whether you can productionize AI endpoints."),
        ],
    },
])

EPAM_MODULES.extend([
    {
        "id": "epam-sql-postgres",
        "title": "EPAM SQL and PostgreSQL",
        "description": "SQL querying, joins, aggregation, subqueries, CTEs, database design, PostgreSQL JSON columns, EXPLAIN, transactions, and ORM performance.",
        "tags": ["sql", "postgresql", "database design", "explain"],
        "lessons": [
            ("SQL Query Core", ["select", "joins", "group by", "having"]),
            ("Advanced Query Structure", ["subqueries", "ctes", "json columns"]),
            ("Database Design", ["primary keys", "foreign keys", "normalization", "indexes"]),
            ("Transactions and ORM Performance", ["transactions", "acid", "sqlalchemy", "lazy vs eager loading"]),
        ],
        "questions": [
            ("SELECT", "What is the core purpose of SELECT?", "Retrieve columns/expressions from rows", ["Create a Docker image", "Start an event loop", "Define a JWT"], "SELECT describes what data to return from a table or query expression.", ["select", "sql", "query"], "SELECT id, email FROM users;", "whether you understand basic SQL retrieval."),
            ("JOINs", "Orders need customer emails. What SQL operation connects orders to users?", "JOIN on the foreign key", ["GROUP BY only", "HAVING only", "Docker compose", "JWT decode"], "JOINs combine related rows, usually through primary-key and foreign-key relationships.", ["joins", "foreign keys", "sql"], "JOIN users ON orders.user_id = users.id", "whether you can query relational data."),
            ("GROUP BY", "How do you calculate revenue per month?", "GROUP BY month and aggregate amount", ["Use WHERE after aggregation only", "Use a Python list always", "Create a new primary key"], "GROUP BY forms groups for aggregate functions such as SUM, COUNT, and AVG.", ["group by", "aggregation", "sql"], "SELECT month, SUM(amount) FROM sales GROUP BY month", "whether you understand aggregation."),
            ("HAVING", "Where should you filter groups with SUM(amount) > 10000?", "HAVING", ["WHERE only", "ORDER BY only", "LIMIT only"], "WHERE filters rows before grouping; HAVING filters groups after aggregation.", ["having", "group by", "aggregation"], "HAVING SUM(amount) > 10000", "whether you understand SQL execution semantics."),
            ("Subqueries", "When is a subquery useful?", "When a query needs the result of another query", ["Only for CSS", "Only for JWTs", "Never in SQL"], "Subqueries can compute intermediate sets or scalar values inside a larger query.", ["subqueries", "sql"], "Find customers whose spend is above average.", "whether you can compose SQL logic."),
            ("CTEs", "Why use a CTE?", "To name an intermediate result for readability/reuse", ["To create a Python package", "To hash passwords", "To replace indexes"], "CTEs make complex SQL easier to read and can structure multi-step analysis.", ["ctes", "with", "sql"], "WITH monthly AS (...) SELECT * FROM monthly WHERE revenue > 0", "whether you can write maintainable analytical SQL."),
            ("Primary and Foreign Keys", "What does a foreign key protect?", "Referential integrity between tables", ["Frontend route protection", "Python package imports", "Model quantization"], "Foreign keys prevent references to missing parent rows and document relationships.", ["primary keys", "foreign keys", "database design"], "orders.user_id references users.id.", "whether you design relational schemas correctly."),
            ("Normalization", "Why normalize a schema?", "Reduce duplication and update anomalies", ["Make every query faster", "Avoid transactions", "Remove all JOINs"], "Normalization separates facts so updates happen in one place. It can increase joins, so design balances correctness and query needs.", ["normalization", "database design"], "Store customer email once in users, not copied across every order.", "whether you understand schema trade-offs."),
            ("Indexes", "What does an index usually improve?", "Read access for matching query patterns", ["Every write speed", "All memory use", "CORS behavior"], "Indexes speed lookups and ordering for supported access paths, but slow writes and use storage.", ["indexes", "performance", "sql"], "Index orders(customer_id, created_at) for customer order history.", "whether you reason about SQL performance."),
            ("Transactions and ACID", "Why wrap a debit and credit in one transaction?", "To commit both changes or neither", ["To skip validation", "To improve CSS", "To avoid all locks"], "Transactions protect invariants across multiple writes. ACID describes the guarantees.", ["transactions", "acid", "database design"], "Transfer money with debit and credit in one transaction.", "whether you protect data correctness."),
            ("PostgreSQL JSON Columns", "When are PostgreSQL JSON columns useful?", "For flexible attributes with known query/index trade-offs", ["For every relational relationship", "To avoid schemas completely", "To replace backups"], "JSON columns add flexibility but can weaken constraints and complicate indexing if overused.", ["postgresql", "json columns", "trade-off"], "Store integration metadata as JSON while core entities stay relational.", "whether you understand PostgreSQL feature trade-offs."),
            ("EXPLAIN and ORM Loading", "An endpoint suddenly gets slow. What should you inspect?", "EXPLAIN plan and ORM lazy/eager loading behavior", ["Only button labels", "Only JWT claims", "Only package __init__.py"], "EXPLAIN reveals scans, joins, and index usage. ORM lazy loading can create N+1 queries unless eager loading is chosen deliberately.", ["explain", "sqlalchemy", "lazy vs eager loading", "n+1"], "Use EXPLAIN ANALYZE plus selectinload for a slow relationship-heavy endpoint.", "whether you can debug database performance."),
        ],
    },
    {
        "id": "epam-concurrency-performance",
        "title": "EPAM Concurrency and Performance",
        "description": "Async Python, event loop, asyncio, threading, locks, race conditions, multiprocessing, profiling, caching, Redis basics, and N+1 queries.",
        "tags": ["asyncio", "threading", "multiprocessing", "performance"],
        "lessons": [
            ("Async Python", ["async", "await", "event loop", "asyncio"]),
            ("Threads and Shared State", ["threading", "threads", "locks", "race conditions"]),
            ("Processes and CPU Work", ["multiprocessing", "cpu-bound", "workers"]),
            ("Profiling and Caching", ["profiling", "caching", "redis", "n+1"]),
        ],
        "questions": [
            ("Async/Await", "What kind of workload benefits most from async/await?", "I/O-bound work with waiting", ["Pure CPU loops", "Static type checking", "SQL normalization"], "Async lets one event loop switch tasks while operations wait on I/O.", ["async", "await", "asyncio"], "Await several integration API calls without blocking the server.", "whether you understand async Python's actual benefit."),
            ("Event Loop", "What does the event loop coordinate?", "Scheduled coroutines and I/O readiness", ["Database foreign keys", "Docker layers", "JWT signatures"], "The event loop runs coroutines and resumes them when awaited I/O is ready.", ["event loop", "asyncio", "coroutines"], "asyncio gathers multiple HTTP calls and resumes each when a response arrives.", "whether you understand async runtime behavior."),
            ("Blocking in Async", "What is wrong with CPU-heavy work inside an async endpoint?", "It blocks the event loop", ["It creates a CTE", "It validates JWT twice", "It disables indexes"], "CPU-heavy work does not yield control, so it can block other coroutines.", ["async", "cpu-bound", "performance"], "Move heavy forecasting to a worker process.", "whether you avoid event-loop blocking."),
            ("Threading", "When can threads help in Python?", "Overlapping blocking I/O", ["Bypassing all race conditions", "Making every CPU task faster", "Replacing tests"], "Threads can overlap blocking I/O, but shared state requires care.", ["threading", "threads", "io"], "Use threads for blocking SDK calls if async APIs are unavailable.", "whether you know realistic thread use cases."),
            ("Locks", "Why use a lock?", "To protect shared mutable state", ["To speed SQL joins", "To serialize JSON", "To create a package"], "Locks prevent multiple threads from modifying shared state at the same time.", ["locks", "threading", "shared state"], "Guard an in-memory counter updated by many worker threads.", "whether you understand synchronization."),
            ("Race Conditions", "What is a race condition?", "A bug where timing changes the outcome", ["A slow SQL query only", "A missing import", "A Pydantic schema"], "Race conditions happen when concurrent operations interleave unpredictably around shared state.", ["race conditions", "concurrency"], "Two threads increment the same counter and one update is lost.", "whether you can reason about concurrent correctness."),
            ("Multiprocessing", "When should multiprocessing be considered?", "CPU-bound work that can run in separate processes", ["Small dict lookups", "Simple routing", "CORS preflight"], "Multiprocessing can use multiple CPU cores because work runs in separate processes.", ["multiprocessing", "cpu-bound", "parallelism"], "Run feature engineering or model scoring in worker processes.", "whether you choose the right execution model."),
            ("When to Use What", "Which pairing is most accurate?", "async for I/O, multiprocessing for CPU", ["async for CPU only", "threads for database schema", "Redis for Python imports"], "Choose the model based on the bottleneck: waiting on I/O, shared-state coordination, or CPU work.", ["async", "threading", "multiprocessing"], "Use async for API calls and processes for heavy forecasting jobs.", "whether you match tools to bottlenecks."),
            ("Profiling", "What should happen before optimizing?", "Profile to find the real bottleneck", ["Rewrite everything", "Add random caching", "Remove tests"], "Profiling prevents guessing. It shows where time is actually spent.", ["profiling", "performance"], "Use profiling to discover that serialization, not SQL, dominates response time.", "whether you optimize from evidence."),
            ("Caching", "When does caching help?", "Repeated expensive reads that tolerate staleness", ["Every write transaction", "Password verification only", "All imports"], "Caches reduce repeated work but introduce invalidation and staleness decisions.", ["caching", "performance"], "Cache dashboard metadata that changes rarely.", "whether you know caching trade-offs."),
            ("Redis Basics", "What is Redis commonly used for?", "Fast cache, session, queue, or rate-limit state", ["Long-term relational integrity", "Compiled Python modules", "Static HTML only"], "Redis is an in-memory data store often used for fast operational state.", ["redis", "cache", "rate limit"], "Store a short-lived dashboard cache key in Redis.", "whether you understand common infrastructure components."),
            ("N+1 Queries", "A page loads 100 rows then queries details row by row. What is likely happening?", "N+1 queries", ["JWT expiry", "Docker cache", "Thread lock contention only"], "N+1 query patterns create one parent query plus one child query per row. Use eager loading or bulk queries.", ["n+1", "sqlalchemy", "performance"], "Use selectinload to fetch related orders for all users.", "whether you can detect ORM performance problems."),
        ],
    },
])


def epam_module_data(order, spec):
    module_id = spec["id"]
    module_questions = [epam_question(module_id, index, item) for index, item in enumerate(spec["questions"], start=1)]
    return {
        "id": module_id,
        "title": spec["title"],
        "description": spec["description"],
        "order": order,
        "tags": spec["tags"],
        "lessons": [epam_lesson(module_id, index, title, tags) for index, (title, tags) in enumerate(spec["lessons"], start=1)],
        "questions": module_questions,
        "coding_challenges": [challenge(module_id, spec["title"], spec["tags"])],
        "boss_battle": {
            "id": f"{module_id}-boss",
            "title": f"{spec['title']} boss battle",
            "question_ids": [item["id"] for item in module_questions[:12]],
            "passing_threshold": 0.75,
            "reward_xp": 100,
        },
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
    for offset, spec in enumerate(DDIA_SPECS, start=len(MODULES) + 1):
        module_id, title, description, tags, *_ = spec
        module_questions = ddia_questions(module_id, spec)
        data = {
            "id": module_id,
            "title": title,
            "description": description,
            "order": offset,
            "tags": tags,
            "lessons": ddia_lessons(module_id, title, description, tags),
            "questions": module_questions,
            "coding_challenges": [ddia_challenge(module_id, title, tags)],
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
    for offset, spec in enumerate(EPAM_MODULES, start=len(MODULES) + len(DDIA_SPECS) + 1):
        data = epam_module_data(offset, spec)
        file_name = f"{data['id']}.json"
        files.append(file_name)
        (CONTENT / file_name).write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    (CONTENT / "manifest.json").write_text(json.dumps({"modules": files}, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "content"

EXPECTED_TERMS = {
    "web-fundamentals": ["http", "https", "dns", "request", "response", "client", "server", "status code", "headers", "cookies", "sessions", "cors", "tls", "origin"],
    "apis": ["rest", "grpc", "api contract", "openapi", "swagger", "crud", "serialization", "deserialization", "versioning", "pagination", "offset", "cursor", "filtering", "sorting", "idempotency"],
    "backend": ["fastapi", "flask", "express", "nestjs", "router", "middleware", "dependency injection", "request lifecycle", "lifespan", "background task", "validation", "response model", "async", "concurrency", "parallelism"],
    "databases": ["relational", "nosql", "postgresql", "mongodb", "redis", "sql", "primary key", "foreign key", "relationship", "join", "index", "transaction", "acid", "normalization", "replica", "sharding", "consistency"],
    "sqlalchemy": ["sqlalchemy", "model", "session", "query", "relationship", "loading", "lazy", "eager", "selectinload", "joinedload", "n+1", "migration", "raw sql", "transaction", "unit of work"],
    "testing": ["unit", "integration", "e2e", "pytest", "fixture", "mock", "test double", "tdd", "ci", "coverage", "regression", "jest", "vitest", "contract test"],
    "performance": ["latency", "throughput", "cache", "rate limit", "retry", "timeout", "circuit breaker", "queue", "observability", "logs", "metrics", "traces", "graceful degradation", "p95", "p99"],
    "devops": ["docker", "image", "container", "dockerfile", "compose", "environment variable", "ci", "cd", "pipeline", "artifact", "deployment", "logs", "rollback", "health check", "secrets", "feature flag", "versioning"],
    "ai-integration": ["llm", "rag", "embedding", "vector search", "prompt", "response logging", "guardrail", "latency", "cost", "token", "evaluation", "evals", "hallucination", "privacy", "quantization"],
    "system-design": ["requirements", "functional", "non-functional", "api", "data model", "access pattern", "scale", "cache", "replica", "queue", "partition", "consistency", "availability", "bottleneck", "trade-off"],
    "ddia-tradeoffs": ["reliability", "scalability", "maintainability", "operability", "latency", "throughput", "cloud", "self-hosting", "serverless", "microservices", "system of record", "derived data"],
    "ddia-nfrs": ["percentile", "p95", "p99", "sla", "slo", "availability", "durability", "operability", "security", "evolvability", "tail latency"],
    "ddia-data-models": ["relational", "document", "graph", "denormalization", "joins", "query language", "schema flexibility", "access patterns"],
    "ddia-storage": ["b-tree", "lsm", "sstable", "log-structured", "compaction", "write amplification", "read amplification", "secondary index"],
    "ddia-encoding": ["json", "avro", "schema evolution", "backward compatibility", "forward compatibility", "schema registry", "message encoding", "rolling upgrade"],
    "ddia-replication": ["leader", "follower", "replication lag", "failover", "read-your-writes", "monotonic reads", "conflict resolution", "split-brain"],
    "ddia-sharding": ["partition key", "hot shard", "rebalancing", "routing", "consistent hashing", "cross-shard", "skew"],
    "ddia-transactions": ["acid", "isolation", "snapshot isolation", "serializable", "write skew", "lost update", "distributed transaction"],
    "ddia-distributed-systems": ["partial failure", "timeout", "network partition", "clock skew", "gc pause", "process pause", "fencing token", "duplicate request", "lease"],
    "ddia-consistency": ["linearizability", "causal consistency", "strong consistency", "consensus", "leader election", "quorum", "safety", "liveness", "agreement"],
    "ddia-batch": ["batch", "mapreduce", "dataflow", "snapshot", "materialized view", "shuffle join", "recomputation", "idempotent output", "backfill"],
    "ddia-stream": ["stream", "event log", "consumer offset", "window", "watermark", "delivery semantics", "backpressure", "stateful processing", "duplicate processing"],
    "ddia-stream-philosophy": ["events as facts", "derived state", "replay", "event time", "processing time", "correction event", "audit trail", "deterministic"],
    "ddia-doing-right": ["ethics", "privacy", "correctness", "auditability", "security", "retention", "consent", "deletion", "governance", "data minimization"],
    "epam-python-core": ["variables", "references", "mutable", "immutable", "lists", "tuples", "sets", "dictionaries", "time complexity", "truthiness", "is", "==", "why python", "java"],
    "epam-python-functions": ["functions", "*args", "**kwargs", "positional-only", "keyword-only", "default arguments", "lambda", "list comprehension", "dict comprehension", "set comprehension", "generator expression", "try", "except", "finally", "custom exceptions", "imports", "packages", "modules", "__init__.py", "virtual environments"],
    "epam-python-oop": ["classes", "objects", "encapsulation", "inheritance", "composition", "polymorphism", "dataclasses", "abstract base classes", "protocols", "dependency injection", "__init__", "__repr__", "__str__", "__eq__", "__hash__", "iterators", "iterable", "generators", "yield", "lazy evaluation", "decorators", "context managers", "__enter__", "__exit__"],
    "epam-fastapi-architecture": ["routing", "dependency injection", "pydantic", "validation", "middleware", "authentication", "jwt", "background tasks", "async endpoints", "error handling", "rest", "status codes", "pagination", "filtering", "versioning", "service layer", "repository pattern", "dtos", "project structure"],
    "epam-sql-postgres": ["select", "joins", "group by", "having", "subqueries", "ctes", "primary keys", "foreign keys", "normalization", "indexes", "transactions", "acid", "postgresql", "json columns", "explain", "sqlalchemy", "relationships", "lazy vs eager loading"],
    "epam-concurrency-performance": ["async", "await", "event loop", "asyncio", "threading", "threads", "locks", "race conditions", "multiprocessing", "profiling", "caching", "redis", "n+1"],
    "epam-testing-devops-git": ["pytest", "fixtures", "mocking", "integration tests", "end-to-end tests", "docker", "images", "containers", "dockerfile", "docker-compose", "git", "branching", "rebasing", "pull requests", "github actions", "ci/cd"],
    "epam-ai-system-design": ["llm apis", "embeddings", "vector databases", "rag", "prompt engineering", "token limits", "streaming", "cost optimization", "url shortener", "chat api", "ai api", "notification service"],
    "forecast-alpha-defense": ["forecast alpha", "next.js", "fastapi", "postgresql", "supabase", "oauth", "jwt", "platform database", "connection service", "schema scanning", "kpi recommendations", "dashboard", "forecasting", "anomaly detection", "intelligence", "semantic model", "sql builder", "notifications", "collaboration", "usage", "lessons learned"],
    "portfolio-assistant-llm": ["portfolio chatbot", "fastapi", "post /chat", "answer_from_messages", "retrieval", "tf-idf", "cosine similarity", "onnx", "minilm", "embeddings", "query rules", "aliases", "third-person rewriting", "confidence threshold", "portfolio_retriever.json", "portfolio_embeddings.npz", "conversations.json", "bilstm", "docker", "tests"],
}

EXPECTED_PANEL_TITLES = {
    "web-fundamentals": {"DNS Resolution", "HTTPS and TLS", "HTTP Request and Response", "PATCH vs PUT", "HTTP Status Codes", "CORS and Origins", "Cookies and Sessions"},
    "apis": {"REST vs gRPC", "API Contracts and OpenAPI", "Cursor vs Offset Pagination", "Idempotency Keys"},
    "backend": {"Backend Framework Trade-offs", "Input Validation Boundary", "Dependency Injection", "Async, Concurrency, and Parallelism"},
    "databases": {"Relational vs NoSQL Databases", "Keys, Relationships, and JOINs", "Database Indexes", "Transactions and ACID", "Replication and Replica Lag", "Sharding and Hot Partitions", "Consistency vs Availability"},
    "sqlalchemy": {"SQLAlchemy Session and Unit of Work", "N+1 Queries", "SQLAlchemy Loading Strategies", "Schema Migrations", "Raw SQL Escape Hatches", "Transactions and ACID", "Keys, Relationships, and JOINs"},
    "testing": {"Testing Scope", "CI/CD Pipelines"},
    "performance": {"Latency, Throughput, and Tail Latency", "Caching", "Rate Limiting", "Timeouts, Retries, and Backoff", "Circuit Breakers", "Queues and Backpressure", "Logs, Metrics, and Traces"},
    "devops": {"Docker Images and Containers", "Runtime Configuration", "CI/CD Pipelines", "Deployment Safety", "Secret Management", "Build Artifact Traceability", "Logs, Metrics, and Traces"},
    "ai-integration": {"Production AI Integration", "Retrieval-Augmented Generation", "Model Quantization Trade-off", "Responsible Data Use"},
    "system-design": {"System Design Requirements", "Data Models and Query Languages", "Caching", "Queues and Backpressure", "Replication and Replica Lag", "Sharding and Hot Partitions", "Consistency vs Availability", "Database Indexes"},
    "ddia-tradeoffs": {"Data System Trade-offs"},
    "ddia-nfrs": {"Nonfunctional Requirements"},
    "ddia-data-models": {"Data Models and Query Languages"},
    "ddia-storage": {"LSM Trees and SSTables"},
    "ddia-encoding": {"Schema Evolution"},
    "ddia-replication": {"Replication and Replica Lag"},
    "ddia-sharding": {"Sharding and Hot Partitions"},
    "ddia-transactions": {"Transactions and ACID"},
    "ddia-distributed-systems": {"Partial Failure in Distributed Systems"},
    "ddia-consistency": {"Consistency vs Availability", "Consensus, Safety, and Liveness"},
    "ddia-batch": {"Batch Processing"},
    "ddia-stream": {"Stream Processing"},
    "ddia-stream-philosophy": {"Stream Processing"},
    "ddia-doing-right": {"Responsible Data Use"},
    "epam-python-core": {"Variables and References", "Mutable vs Immutable", "Lists, Tuples, Sets, Dictionaries", "Time Complexity of Common Operations", "Truthiness", "is vs ==", "Dictionary Operations", "Tuple Use Cases", "Set Semantics", "Why Python", "Why Not Java", "What Makes Python Different"},
    "epam-python-functions": {"*args", "**kwargs", "Positional-only Args", "Keyword-only Args", "Default Argument Pitfall", "Lambda Functions", "List Comprehension", "Dict Comprehension", "Set Comprehension", "Generator Expressions", "Exceptions", "Packages and Virtual Environments"},
    "epam-python-oop": {"Classes and Objects", "Encapsulation", "Inheritance", "Composition", "Polymorphism", "Dataclasses", "Abstract Base Classes", "Protocols", "Special Methods", "Iterators and Generators", "Decorators", "Context Managers"},
    "epam-fastapi-architecture": {"FastAPI Routing", "Dependency Injection", "Pydantic Validation", "Middleware", "JWT Authentication", "Background Tasks", "Async Endpoints", "Error Handling", "Pagination and Filtering", "Versioning", "Service Layer", "Repository Pattern and DTOs"},
    "epam-sql-postgres": {"SELECT", "JOINs", "GROUP BY", "HAVING", "Subqueries", "CTEs", "Primary and Foreign Keys", "Normalization", "Indexes", "Transactions and ACID", "PostgreSQL JSON Columns", "EXPLAIN and ORM Loading"},
    "epam-concurrency-performance": {"Async/Await", "Event Loop", "Blocking in Async", "Threading", "Locks", "Race Conditions", "Multiprocessing", "When to Use What", "Profiling", "Caching", "Redis Basics", "N+1 Queries"},
    "epam-testing-devops-git": {"pytest", "Fixtures", "Mocking", "Integration Tests", "End-to-End Tests", "Docker Images and Containers", "Dockerfile", "docker-compose", "Git Branching", "Rebasing", "Pull Requests", "GitHub Actions and CI/CD"},
    "epam-ai-system-design": {"LLM APIs", "Embeddings", "Vector Databases", "RAG", "Prompt Engineering", "Token Limits", "Streaming", "Cost Optimization", "URL Shortener", "Chat API", "Notification Service", "AI API"},
    "forecast-alpha-defense": {"Forecast Alpha Architecture", "Frontend App Router", "API Wrapper and Proxy", "Protected Routes", "Backend Startup", "Platform Database", "Connection Service", "Supported Data Sources", "Forecasting ML", "Natural-Language Intelligence", "Tests and Risk", "Lessons Learned"},
    "portfolio-assistant-llm": {"Portfolio Chat API", "Request Schema", "Production Model Type", "TF-IDF Lexical Matching", "Semantic Matching", "Query Rules", "Third-Person Rewriting", "Fallback Behavior", "Runtime Artifacts", "Training Data", "Experiment vs Production", "Tests and Caveat"},
}


def flatten(value):
    if isinstance(value, dict):
        return " ".join(flatten(item) for item in value.values())
    if isinstance(value, list):
        return " ".join(flatten(item) for item in value)
    return str(value)


def module_text(path):
    data = json.loads(path.read_text(encoding="utf-8"))
    return flatten(data).lower()


def main():
    failures = {}
    panel_failures = []
    for module_id, terms in EXPECTED_TERMS.items():
        path = CONTENT / f"{module_id}.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        text = flatten(data).lower()
        missing = [term for term in terms if term.lower() not in text]
        if missing:
            failures[module_id] = missing
        for question in data["questions"]:
            panel = question.get("concept_panel")
            if not panel:
                panel_failures.append(f"{question['id']}: missing concept_panel")
                continue
            required = ["title", "explanation", "key_takeaways", "interview_insight", "practical_example"]
            missing_fields = [field for field in required if not panel.get(field)]
            if missing_fields:
                panel_failures.append(f"{question['id']}: missing panel fields {', '.join(missing_fields)}")
            if len(panel.get("key_takeaways", [])) < 3:
                panel_failures.append(f"{question['id']}: concept_panel needs at least 3 key takeaways")
            if not panel.get("interview_insight", "").startswith("Interviewers usually ask this concept to evaluate"):
                panel_failures.append(f"{question['id']}: interview insight has wrong lead-in")
            allowed_titles = EXPECTED_PANEL_TITLES.get(module_id, set())
            if allowed_titles and panel.get("title") not in allowed_titles:
                panel_failures.append(f"{question['id']}: unexpected panel title {panel.get('title')!r}")

    if failures or panel_failures:
        for module_id, missing in failures.items():
            print(f"{module_id}: missing {', '.join(missing)}")
        for failure in panel_failures:
            print(failure)
        raise SystemExit(1)

    print(f"Coverage audit passed for {len(EXPECTED_TERMS)} modules.")


if __name__ == "__main__":
    main()

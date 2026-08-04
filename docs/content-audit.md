# Content Coverage Audit

Date: 2026-08-03

Scope: all 34 modules in `content/manifest.json`.

This audit checks whether each module actually tests the concepts it promises in its title, description, tags, and lessons. It does not judge the UI. The main question is: can a learner repeatedly train a module and encounter all important concepts?

## Executive Summary

The current content is not reliable enough as a curriculum.

The app engine is usable, but the content has two major problems:

1. The original 10 modules reuse the same 22 generic prompts almost exactly.
2. Many advertised concepts have zero or one actual drill.

This creates false confidence. For example, the APIs module advertises gRPC, Swagger, CRUD, serialization, deserialization, filtering, and sorting, but those concepts are barely or not tested. A learner can train APIs many times and still never build recall for gRPC.

The DDIA and EPAM/project-defense modules use distinct topic specs. The audit script now checks required terms and concept panel titles across all 34 modules.

## Audit Method

For each module:

- Promised concepts were collected from title, description, tags, lessons, and expected source scope.
- Tested concepts were counted by scanning question prompts, options, answers, tags, code, matching pairs, and explanations.
- `missing` means zero observed question hits.
- `weak` means exactly one observed hit.
- `strong` means two or more observed hits.

This is a keyword audit, so it is not perfect. It is still useful because the current gaps are large enough that exact semantic scoring is not needed to see the problem.

## Global Findings

### Critical Repetition

The first 10 modules reuse the same prompt set. These prompts appear in all 10 original modules:

- A profile endpoint receives only a new email field. What should the API prefer?
- Pick the operations that are usually safe to retry.
- Arrange the request path.
- Match each signal to its meaning.
- Fill the branch that classifies server errors.
- Production duplicated records after a timeout. What is the bug?
- What does classify_status_code(404) return?
- A changing feed skips items with page numbers. What pagination style fits better?
- Which change best preserves existing clients when a response shape breaks compatibility?
- Select the reasons to validate input before business logic.
- Match the scaling tool to the bottleneck.
- An endpoint loads 100 users, then reads user.orders in a loop. What is happening?
- Pick two fixes for the N+1 query pattern.
- A downstream service is failing and your app keeps retrying instantly. What should you add first?
- Order the transaction flow.
- Match data shape to storage fit.
- Fill the safer SQLAlchemy loading option for a collection.
- CPU-heavy image processing is slowing requests. Which model helps most?
- A product page needs recommendations, but the recommender is down. What behavior is best?
- Which signals make an API easier for clients to use?
- A response model includes password_hash. What is the bug?
- A social like count appears five seconds late. When is that acceptable?

These are useful drills in the right module, but they should not appear as the normal training set for every module. Cross-topic drills belong in mixed interview mode, boss battles, or daily runs, not module-specific training.

## Module Coverage Matrix

### Web Fundamentals

Questions: 22

Missing:
- method
- cookies
- sessions
- origin
- TLS

Weak:
- DNS
- PATCH
- headers

Assessment: Poor. The module claims HTTP/HTTPS/DNS/cookies/sessions/CORS, but it mostly tests generic API/backend concepts. Needs focused drills on DNS lookup, TLS, headers, cookies vs sessions, same-origin policy, CORS preflight, and method semantics.

### APIs

Questions: 22

Missing:
- API contract
- Swagger
- CRUD
- serialization
- deserialization

Weak:
- OpenAPI
- versioning
- cursor pagination
- filtering
- sorting

Assessment: Poor. This is the clearest failure case. gRPC is advertised but not meaningfully drilled. CRUD, Swagger, serialization/deserialization, filtering, and sorting need dedicated drills. REST vs gRPC needs several practical contrast questions.

### Backend

Questions: 22

Missing:
- Flask
- Express
- NestJS
- dependency injection
- request lifecycle
- lifespan
- background tasks
- concurrency

Weak:
- router
- response model
- async
- await
- parallelism

Assessment: Poor. The module promises backend framework architecture but mostly receives generic API/data questions. Needs FastAPI request lifecycle, DI, middleware ordering, routers, lifespan startup/shutdown, background tasks, validation, response models, async vs parallelism, and framework comparisons.

### Databases

Questions: 22

Missing:
- relational
- PostgreSQL
- MySQL
- MongoDB
- primary key
- foreign key
- index
- sharding

Weak:
- Redis
- transaction
- ACID
- replica
- consistency

Assessment: Poor. It lacks core relational modeling drills and database-specific comparisons. Needs keys, relationships, joins, indexes, transactions, ACID, SQL vs NoSQL, Redis use cases, replicas vs sharding, and consistency trade-offs.

### SQLAlchemy Deep Dive

Questions: 22

Missing:
- lazy loading
- migration
- raw SQL
- unit of work

Weak:
- loading
- joinedload
- transaction

Assessment: Medium-poor. N+1/selectinload is present, but SQLAlchemy-specific depth is thin. Needs session lifecycle, flush vs commit, unit of work, lazy/eager loading, selectinload vs joinedload, Alembic migrations, relationships, transactions, and raw SQL escape hatches.

### Quality and Testing

Questions: 22

Missing:
- unit testing
- e2e testing
- fixtures
- mocks
- test doubles
- TDD
- coverage
- regression testing
- contract tests
- Jest

Weak:
- integration testing

Assessment: Critical failure. The module barely tests testing. Needs module-specific drills for pytest fixtures, mocking boundaries, unit vs integration vs e2e, contract tests, regression tests, coverage interpretation, frontend tests, and CI quality gates.

### Performance and Reliability

Questions: 22

Missing:
- latency
- throughput
- rate limiting
- circuit breaker
- observability
- logs
- metrics
- traces
- p95
- p99

Weak:
- queue
- graceful degradation

Assessment: Poor. It has retries and caching but misses the operational vocabulary. Needs p95/p99, tail latency, rate limiting, circuit breakers, queues, backoff, caching invalidation, observability triad, alerting, and degradation scenarios.

### Docker, DevOps and CI/CD

Questions: 22

Missing:
- container
- Dockerfile
- Compose
- environment variables
- CD
- pipeline
- artifact
- deployment
- logs
- rollback
- health check
- secrets
- feature flags
- branching

Weak:
- image
- versioning

Assessment: Critical failure. The module title promises DevOps but training mostly covers API/database questions. Needs Docker image vs container, Dockerfile layers, Compose, env config, secrets, GitHub Actions/Azure DevOps, artifacts, deployments, health checks, rollbacks, feature flags, and branching/versioning.

### AI Integration

Questions: 22

Missing:
- LLM
- agent
- embeddings
- vector search
- prompt
- response logging
- guardrails
- latency
- cost
- token
- evaluation
- hallucination
- privacy
- quantization

Weak:
- none

Assessment: Critical failure. This module currently does not teach AI integration. Needs practical LLM endpoint calls, RAG request/response flow, embedding/vector search, latency/cost/token controls, prompt/response logging, guardrails, hallucination handling, privacy, evals, and quantization trade-offs.

### System Design

Questions: 22

Missing:
- requirements
- functional requirements
- non-functional requirements
- data model
- access pattern
- partition
- availability

Weak:
- replica
- queue
- consistency
- bottleneck
- trade-off

Assessment: Poor. It has scattered distributed-system concepts but not a coherent system-design interview loop. Needs requirements elicitation, API/data model design, access patterns, capacity/load assumptions, bottleneck diagnosis, scaling patterns, consistency/availability trade-offs, and design-review reasoning.

### DDIA: Data Systems Trade-offs

Questions: 14

Missing:
- cloud
- self-hosting
- microservices
- serverless
- system of record
- derived data

Weak:
- operability
- throughput

Assessment: Medium. Core reliability/scalability/maintainability exists, but DDIA2 chapter-specific cloud/self-hosting and operational vs analytical/system-of-record concepts are missing.

### DDIA: Nonfunctional Requirements

Questions: 14

Missing:
- percentile
- operability
- security
- evolvability

Weak:
- p95
- p99
- SLA
- tail latency

Assessment: Medium. Needs stronger latency percentile drills, SLO/SLA distinction, error budgets, operability, security, and evolvability trade-offs.

### DDIA: Data Models and Query Languages

Questions: 14

Missing:
- none

Weak:
- schema flexibility

Assessment: Good baseline. Needs more depth on graph traversal, denormalization update cost, document locality, and query-language expressiveness.

### DDIA: Storage and Retrieval

Questions: 14

Missing:
- SSTable

Weak:
- read amplification
- log-structured storage

Assessment: Medium-good. Needs explicit SSTable, compaction, read amplification, write amplification, B-tree vs LSM workload scenarios.

### DDIA: Encoding and Evolution

Questions: 14

Missing:
- JSON
- Avro

Weak:
- schema evolution
- schema registry
- message encoding

Assessment: Medium. Needs concrete JSON vs binary schema encoding, Avro-like evolution, compatibility matrices, rolling deploy examples, and schema registry workflows.

### DDIA: Replication

Questions: 14

Missing:
- monotonic reads

Weak:
- conflict resolution
- split-brain

Assessment: Medium-good. Needs more read consistency anomalies: read-your-writes, monotonic reads, consistent prefix, failover, split brain, and conflict handling.

### DDIA: Sharding

Questions: 14

Missing:
- none

Weak:
- consistent hashing
- cross-shard query
- salting

Assessment: Good baseline. Needs deeper hot-key mitigation, rebalancing mechanics, routing table changes, cross-shard query cost, and consistent hashing trade-offs.

### DDIA: Transactions

Questions: 14

Missing:
- ACID
- snapshot isolation
- distributed transaction

Weak:
- none

Assessment: Medium. Needs explicit isolation-level anomalies, snapshot isolation vs serializability, lost update, write skew, compare-and-set, distributed transaction/2PC trade-offs.

### DDIA: Trouble with Distributed Systems

Questions: 14

Missing:
- GC pause

Weak:
- partial failure
- process pause
- fencing token
- duplicate request
- lease

Assessment: Medium. Needs more drills on clocks, pauses, lease expiry, fencing tokens, retries after unknown outcomes, and network partitions.

### DDIA: Consistency and Consensus

Questions: 14

Missing:
- liveness
- strong consistency

Weak:
- leader election
- agreement

Assessment: Medium. Needs safety vs liveness, quorum reads/writes, consensus agreement, leader election failure, linearizability vs causal consistency, and when not to use consensus.

### DDIA: Batch Processing

Questions: 14

Missing:
- MapReduce
- dataflow
- recomputation

Weak:
- shuffle join
- idempotent output

Assessment: Medium. Needs explicit batch job mechanics, stable snapshots, materialized views, backfills, shuffle joins, idempotent output, and recomputation trade-offs.

### DDIA: Stream Processing

Questions: 14

Missing:
- delivery semantics
- stateful processing

Weak:
- window
- watermark
- exactly-once
- duplicate processing

Assessment: Medium. Needs event logs, offsets, delivery semantics, duplicates, exactly-once effects, windows, watermarks, state stores, backpressure, and ordering.

### DDIA: Streaming Systems Philosophy

Questions: 14

Missing:
- none

Weak:
- correction event
- audit trail
- immutable facts
- deterministic replay

Assessment: Medium-good. Needs deeper event-time vs processing-time scenarios, replay safety, immutable event facts, correction events, and derived-state rebuilds.

### DDIA: Doing the Right Thing

Questions: 14

Missing:
- ethics

Weak:
- consent
- governance

Assessment: Medium-good. Needs more privacy, consent, governance, retention, deletion, auditability, access control, and data minimization scenarios.

## Remediation Rules

Before rewriting content, adopt these rules:

1. Each module must have a hand-authored concept inventory.
2. Every promised core concept must have at least one drill.
3. Major concepts must have 2-4 drills across different mechanics.
4. Module training must not include unrelated normal drills.
5. Cross-topic questions belong in daily runs, interview mode, or boss battles.
6. Boss battles should synthesize 3-5 module concepts, not repeat the first questions.
7. Every question must have a concrete explanation that teaches why the answer wins.
8. Matching pairs must map concepts to meanings, symptoms, or fixes, not arbitrary term-to-term pairs.
9. Each module should include at least:
   - 6 single-choice/scenario drills
   - 4 multi-select drills
   - 3 matching drills
   - 3 ordering drills
   - 3 bug-hunt drills
   - 2 code/config/output drills where relevant
10. After rewrite, run this audit again and require zero missing core concepts.

## Recommended Rewrite Order

1. APIs
2. AI Integration
3. Docker, DevOps and CI/CD
4. Quality and Testing
5. Backend
6. Web Fundamentals
7. Databases
8. SQLAlchemy Deep Dive
9. Performance and Reliability
10. System Design
11. DDIA modules

Reason: the first four currently have the largest mismatch between advertised scope and tested concepts.

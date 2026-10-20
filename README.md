# Go Goodway: Fundamentals to Proficiency (AI + Infra)

A complete, ordered path from absolute fundamentals to excellent Go engineering —
with special focus on **infrastructure** and **AI systems**.

## Study method (non-negotiable)

1. Read the lesson PDF (or Markdown).
2. Type examples yourself — do not blindly copy-paste.
3. Attempt exercises in `exercises/NN-slug/` until tests pass — **no solutions first**.
4. Only then compare with `solutions/NN-slug/`.
5. Next day: rewrite the solution from memory.

Track checkboxes in [`curriculum/PROGRESS.md`](curriculum/PROGRESS.md).

## Prerequisites

- A computer (macOS/Linux/Windows with WSL is fine)
- Willingness to be confused and push through
- Light Python exposure helps for analogies; this course still rebuilds CS fundamentals

Install Go from https://go.dev/dl/ then:

```bash
go version
```

## Repo layout

```
lessons/NN-slug/lesson.md   # canonical lesson sources
pdfs/NN-slug.pdf            # sorted PDFs
exercises/NN-slug/          # your workspace (tests included)
solutions/NN-slug/          # reference (look last)
scripts/build-pdfs.sh       # regenerate PDFs
```

## Building PDFs

Requires `pandoc` and `typst` (or xelatex):

```bash
brew install pandoc typst
./scripts/build-pdfs.sh
```

PDFs are already generated under [`pdfs/`](pdfs/) in sorted order (`00-…` through `55-…`).

## Daily workflow

1. Open the next unchecked item in [`curriculum/PROGRESS.md`](curriculum/PROGRESS.md).
2. Read `pdfs/NN-….pdf` (or the Markdown under `lessons/`).
3. In `exercises/NN-…/`, run `go test` and implement until green.
4. Only then read `solutions/NN-…/`.
5. Next day: delete your code and rewrite from memory; re-run `go test`.

Maintainers can verify all reference solutions with:

```bash
./scripts/smoke_test.sh
```

## Curriculum map

| # | Title | Phase | Time | Lesson | PDF |
|---|-------|-------|------|--------|-----|
| 00 | Orientation: Programs, Computers, and Go | Phase 0 — Orientation | 1 day | `lessons/00-orientation/` | `pdfs/00-orientation.pdf` |
| 01 | Values, Variables, Types, and Zero Values | Phase 1 — CS fundamentals through Go | 1 day | `lessons/01-values-variables-types/` | `pdfs/01-values-variables-types.pdf` |
| 02 | Expressions, Operators, and Type Conversions | Phase 1 — CS fundamentals through Go | 1 day | `lessons/02-expressions-operators/` | `pdfs/02-expressions-operators.pdf` |
| 03 | Control Flow: if, for, and switch | Phase 1 — CS fundamentals through Go | 1 day | `lessons/03-control-flow/` | `pdfs/03-control-flow.pdf` |
| 04 | Functions, Multiple Returns, and Error Basics | Phase 1 — CS fundamentals through Go | 1 day | `lessons/04-functions-errors/` | `pdfs/04-functions-errors.pdf` |
| 05 | Arrays, Slices, and Maps (Memory Intuition) | Phase 1 — CS fundamentals through Go | 1–2 days | `lessons/05-arrays-slices-maps/` | `pdfs/05-arrays-slices-maps.pdf` |
| 06 | Strings, Runes, Bytes, and UTF-8 | Phase 1 — CS fundamentals through Go | 1 day | `lessons/06-strings-runes-bytes/` | `pdfs/06-strings-runes-bytes.pdf` |
| 07 | Structs, Methods, and Pointers | Phase 1 — CS fundamentals through Go | 1–2 days | `lessons/07-structs-methods-pointers/` | `pdfs/07-structs-methods-pointers.pdf` |
| 08 | Packages, Modules, Visibility, and go.mod | Phase 1 — CS fundamentals through Go | 1 day | `lessons/08-packages-modules/` | `pdfs/08-packages-modules.pdf` |
| 09 | Interfaces and Composition | Phase 2 — Core language depth | 1–2 days | `lessons/09-interfaces/` | `pdfs/09-interfaces.pdf` |
| 10 | Errors Deeply: Wrap, Is, As | Phase 2 — Core language depth | 1–2 days | `lessons/10-errors-deep/` | `pdfs/10-errors-deep.pdf` |
| 11 | Generics: Type Parameters and Constraints | Phase 2 — Core language depth | 1–2 days | `lessons/11-generics/` | `pdfs/11-generics.pdf` |
| 12 | Testing, Table Tests, Fuzz, and Benchmarks | Phase 2 — Core language depth | 1–2 days | `lessons/12-testing/` | `pdfs/12-testing.pdf` |
| 13 | I/O: io, Files, Readers and Writers | Phase 2 — Core language depth | 1–2 days | `lessons/13-io-readers-writers/` | `pdfs/13-io-readers-writers.pdf` |
| 14 | JSON, Encoding, and Time | Phase 2 — Core language depth | 1 day | `lessons/14-json-encoding-time/` | `pdfs/14-json-encoding-time.pdf` |
| 15 | Context: Cancellation and Deadlines | Phase 2 — Core language depth | 1–2 days | `lessons/15-context/` | `pdfs/15-context.pdf` |
| 16 | Reflection Overview (and When Not to Use It) | Phase 2 — Core language depth | 1 day | `lessons/16-reflection/` | `pdfs/16-reflection.pdf` |
| 17 | Idiomatic Go: Effective Patterns | Phase 3 — Idioms and engineering judgment | 1–2 days | `lessons/17-idiomatic-go/` | `pdfs/17-idiomatic-go.pdf` |
| 18 | Project Layout: Libraries vs Services | Phase 3 — Idioms and engineering judgment | 1 day | `lessons/18-project-layout/` | `pdfs/18-project-layout.pdf` |
| 19 | Profiling, Race Detector, Performance Mental Model | Phase 3 — Idioms and engineering judgment | 1–2 days | `lessons/19-profiling-performance/` | `pdfs/19-profiling-performance.pdf` |
| 20 | Documentation, APIs, and Semantic Versioning | Phase 3 — Idioms and engineering judgment | 1 day | `lessons/20-docs-apis-semver/` | `pdfs/20-docs-apis-semver.pdf` |
| 21 | Complexity, Recursion, and Big-O Practice | Phase 4 — Algorithms and data structures | 1–2 days | `lessons/21-complexity-recursion/` | `pdfs/21-complexity-recursion.pdf` |
| 22 | Sorting and Searching | Phase 4 — Algorithms and data structures | 1–2 days | `lessons/22-sorting-searching/` | `pdfs/22-sorting-searching.pdf` |
| 23 | Linked Structures, Stacks, and Queues | Phase 4 — Algorithms and data structures | 1–2 days | `lessons/23-linked-stacks-queues/` | `pdfs/23-linked-stacks-queues.pdf` |
| 24 | Trees, Heaps, and Priority Queues | Phase 4 — Algorithms and data structures | 2 days | `lessons/24-trees-heaps/` | `pdfs/24-trees-heaps.pdf` |
| 25 | Graphs: BFS, DFS, Shortest Paths Intro | Phase 4 — Algorithms and data structures | 2 days | `lessons/25-graphs/` | `pdfs/25-graphs.pdf` |
| 26 | Hashing and Bloom Filters (Infra-Relevant) | Phase 4 — Algorithms and data structures | 1–2 days | `lessons/26-hashing-bloom/` | `pdfs/26-hashing-bloom.pdf` |
| 27 | Dynamic Programming Patterns | Phase 4 — Algorithms and data structures | 2 days | `lessons/27-dynamic-programming/` | `pdfs/27-dynamic-programming.pdf` |
| 28 | Algorithmic Problem Set (Mixed Drills) | Phase 4 — Algorithms and data structures | 2–3 days | `lessons/28-algorithm-drills/` | `pdfs/28-algorithm-drills.pdf` |
| 29 | Goroutines and the Scheduler | Phase 5 — Concurrency | 1–2 days | `lessons/29-goroutines/` | `pdfs/29-goroutines.pdf` |
| 30 | Channels, Select, and Pipelines | Phase 5 — Concurrency | 2 days | `lessons/30-channels-select/` | `pdfs/30-channels-select.pdf` |
| 31 | Mutexes, Atomics, and sync Primitives | Phase 5 — Concurrency | 1–2 days | `lessons/31-mutexes-atomics/` | `pdfs/31-mutexes-atomics.pdf` |
| 32 | Worker Pools, Fan-in/out, Backpressure | Phase 5 — Concurrency | 2 days | `lessons/32-worker-pools/` | `pdfs/32-worker-pools.pdf` |
| 33 | Deadlocks, Races, and Cancellation Patterns | Phase 5 — Concurrency | 1–2 days | `lessons/33-deadlocks-races/` | `pdfs/33-deadlocks-races.pdf` |
| 34 | Concurrent Algorithm Drills | Phase 5 — Concurrency | 2 days | `lessons/34-concurrent-algorithms/` | `pdfs/34-concurrent-algorithms.pdf` |
| 35 | HTTP Servers and Clients (net/http) | Phase 6 — Systems and infrastructure | 2 days | `lessons/35-http-net/` | `pdfs/35-http-net.pdf` |
| 36 | REST API Design, Middleware, Auth Basics | Phase 6 — Systems and infrastructure | 2 days | `lessons/36-rest-middleware-auth/` | `pdfs/36-rest-middleware-auth.pdf` |
| 37 | gRPC and Protobuf Intro | Phase 6 — Systems and infrastructure | 2 days | `lessons/37-grpc-protobuf/` | `pdfs/37-grpc-protobuf.pdf` |
| 38 | Databases: SQL Drivers, Transactions, Migrations | Phase 6 — Systems and infrastructure | 2 days | `lessons/38-databases-sql/` | `pdfs/38-databases-sql.pdf` |
| 39 | Caching, Redis Patterns, Idempotency | Phase 6 — Systems and infrastructure | 1–2 days | `lessons/39-caching-redis/` | `pdfs/39-caching-redis.pdf` |
| 40 | Observability: Logs, Metrics, Tracing | Phase 6 — Systems and infrastructure | 1–2 days | `lessons/40-observability/` | `pdfs/40-observability.pdf` |
| 41 | Containers and Multi-stage Docker Builds for Go | Phase 6 — Systems and infrastructure | 1–2 days | `lessons/41-containers-docker/` | `pdfs/41-containers-docker.pdf` |
| 42 | Kubernetes-Oriented Go: Controllers and client-go | Phase 6 — Systems and infrastructure | 2–3 days | `lessons/42-kubernetes-go/` | `pdfs/42-kubernetes-go.pdf` |
| 43 | Cloud SDK Patterns: Config, Retries, Pagination | Phase 6 — Systems and infrastructure | 1–2 days | `lessons/43-cloud-sdk-patterns/` | `pdfs/43-cloud-sdk-patterns.pdf` |
| 44 | Reliability: Timeouts, Circuit Breakers, Graceful Shutdown | Phase 6 — Systems and infrastructure | 2 days | `lessons/44-reliability/` | `pdfs/44-reliability.pdf` |
| 45 | Numerics and Tensors in Go (gonum) | Phase 7 — AI engineering in Go | 2 days | `lessons/45-numerics-gonum/` | `pdfs/45-numerics-gonum.pdf` |
| 46 | ML-Adjacent Pipelines: ETL, Batching, Features | Phase 7 — AI engineering in Go | 2 days | `lessons/46-ml-pipelines/` | `pdfs/46-ml-pipelines.pdf` |
| 47 | Calling Model APIs: HTTP and SSE Streaming | Phase 7 — AI engineering in Go | 2 days | `lessons/47-model-apis/` | `pdfs/47-model-apis.pdf` |
| 48 | Embeddings, Vector Search, Similarity | Phase 7 — AI engineering in Go | 2 days | `lessons/48-embeddings-vectors/` | `pdfs/48-embeddings-vectors.pdf` |
| 49 | RAG Service in Go: Chunk → Embed → Retrieve → Generate | Phase 7 — AI engineering in Go | 2–3 days | `lessons/49-rag-service/` | `pdfs/49-rag-service.pdf` |
| 50 | Inference Serving: Batching, Queues, Sidecars | Phase 7 — AI engineering in Go | 2 days | `lessons/50-inference-serving/` | `pdfs/50-inference-serving.pdf` |
| 51 | Agents and Tools: Function-Calling Loops | Phase 7 — AI engineering in Go | 2 days | `lessons/51-agents-tools/` | `pdfs/51-agents-tools.pdf` |
| 52 | Evaluating AI Systems in Go | Phase 7 — AI engineering in Go | 2 days | `lessons/52-eval-harnesses/` | `pdfs/52-eval-harnesses.pdf` |
| 53 | Capstone: Production-Shaped HTTP API | Phase 8 — Capstones | 3–5 days | `lessons/53-capstone-infra/` | `pdfs/53-capstone-infra.pdf` |
| 54 | Capstone: Search / Graph Engine Core | Phase 8 — Capstones | 3–5 days | `lessons/54-capstone-algorithms/` | `pdfs/54-capstone-algorithms.pdf` |
| 55 | Capstone: Mini RAG / Embedding Search Service | Phase 8 — Capstones | 4–6 days | `lessons/55-capstone-ai/` | `pdfs/55-capstone-ai.pdf` |

## Pace guide

- Phases 0–3: ~1 lesson/day (a few hours)
- Phases 4–5: 1–2 days/lesson
- Phases 6–7: multi-day modules
- Capstones: several days each

## Quality bar

You are done with a lesson when you can explain the concepts aloud, pass the tests
without looking at solutions, and rewrite the code from memory the next day.

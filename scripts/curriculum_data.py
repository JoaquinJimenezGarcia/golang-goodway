#!/usr/bin/env python3
"""Compact curriculum definitions for lessons 09–55 (plus helpers)."""

from __future__ import annotations

# Each entry: n, slug, title, phase, days, objectives[list], body(md), pitfalls, checks, reading, ex_kind
# ex_kind drives exercise stub generation in generate_curriculum.py

LATER = []


def add(
    n,
    slug,
    title,
    phase,
    days,
    objectives,
    body,
    pitfalls,
    checks,
    reading,
    ex_kind,
    ex_extra=None,
    exercise_guide="",
    exercise_examples="",
):
    LATER.append(
        {
            "n": n,
            "slug": f"{n:02d}-{slug}",
            "title": title,
            "phase": phase,
            "days": days,
            "objectives": objectives,
            "body": body,
            "pitfalls": pitfalls,
            "checks": checks,
            "reading": reading,
            "ex_kind": ex_kind,
            "ex_extra": ex_extra or {},
            "exercise_guide": exercise_guide,
            "exercise_examples": exercise_examples,
        }
    )


P2 = "Phase 2 — Core language depth"
P3 = "Phase 3 — Idioms and engineering judgment"
P4 = "Phase 4 — Algorithms and data structures"
P5 = "Phase 5 — Concurrency"
P6 = "Phase 6 — Systems and infrastructure"
P7 = "Phase 7 — AI engineering in Go"
P8 = "Phase 8 — Capstones"

add(
    9,
    "interfaces",
    "Interfaces and Composition",
    P2,
    "1–2 days",
    [
        "Define interfaces as sets of methods",
        "Accept interfaces, return concrete types in APIs",
        "Compose behavior via small interfaces",
        "Understand the empty interface and `any`",
    ],
    """
## Interfaces are implicit

In Go you do **not** write `implements`. If a type has the methods, it satisfies the interface.

```go
type Stringer interface {
    String() string
}

type User struct{ Name string }
func (u User) String() string { return u.Name }
```

## Small interfaces win

`io.Reader`, `io.Writer`, `fmt.Stringer` — one or two methods.
Write functions that take interfaces so callers can plug mocks, buffers, or network streams.

```go
func CountLines(r io.Reader) (int, error) { /* ... */ }
```

## Composition over inheritance

Go has no class hierarchy. Embed structs and combine interfaces instead.

```go
type ReadWriter interface {
    io.Reader
    io.Writer
}
```

## `any` (empty interface)

`any` is `interface{}` — every type satisfies it. Useful for containers before generics;
prefer generics when you know the type set.
""",
    [
        "Defining huge interfaces that no one can mock",
        "Returning interfaces from constructors unnecessarily",
        "Using `any` everywhere instead of real types",
    ],
    [
        "How does a type satisfy an interface in Go?",
        "Why are small interfaces preferred?",
        "When is `any` acceptable?",
    ],
    ["https://go.dev/tour/methods", "https://go.dev/doc/effective_go#interfaces"],
    "interface_shape",
)

add(
    10,
    "errors-deep",
    "Errors Deeply: Wrap, Is, As",
    P2,
    "1–2 days",
    [
        "Wrap errors with context using fmt.Errorf and %w",
        "Use errors.Is and errors.As for inspection",
        "Choose sentinel vs custom error types",
        "Design error messages for operators and callers",
    ],
    """
## Wrapping

```go
if err != nil {
    return fmt.Errorf("load config %s: %w", path, err)
}
```

`%w` preserves the chain for `errors.Is` / `errors.As`.

## Sentinel errors

```go
var ErrNotFound = errors.New("not found")
```

Good for stable, package-level conditions. Do not compare error strings.

## Typed errors

```go
type ValidationError struct{ Field string }
func (e *ValidationError) Error() string { return e.Field + " invalid" }

var ve *ValidationError
if errors.As(err, &ve) { /* ... */ }
```

## Guideline

Return errors; log at the edge (main/handler). Avoid logging and returning the same error repeatedly.
""",
    [
        "Comparing `err.Error() == \"...\"`",
        "Using `%v` instead of `%w` when wrapping",
        "Creating unique error strings instead of sentinels",
    ],
    [
        "Difference between errors.Is and errors.As?",
        "When prefer sentinel vs typed error?",
        "Where should you log errors?",
    ],
    ["https://go.dev/blog/go1.13-errors", "https://pkg.go.dev/errors"],
    "errors_wrap",
)

add(
    11,
    "generics",
    "Generics: Type Parameters and Constraints",
    P2,
    "1–2 days",
    [
        "Write generic functions with type parameters",
        "Use constraints from constraints package / comparable",
        "Know when generics help vs when interfaces suffice",
        "Avoid over-generic APIs",
    ],
    """
## Type parameters

```go
func Keys[K comparable, V any](m map[K]V) []K {
    out := make([]K, 0, len(m))
    for k := range m {
        out = append(out, k)
    }
    return out
}
```

## Constraints

```go
type Number interface {
    ~int | ~int64 | ~float64
}

func Sum[T Number](xs []T) T {
    var s T
    for _, v := range xs {
        s += v
    }
    return s
}
```

`comparable` is required for map keys and `==`.

## When not to use generics

If a small interface expresses the behavior better, prefer interfaces.
Generics shine for containers, algorithms, and removing `any` casts.
""",
    [
        "Genericizing every function \"just in case\"",
        "Forgetting `comparable` for map keys",
        "Fighting the type checker instead of simplifying the API",
    ],
    [
        "What does `comparable` allow?",
        "When prefer interface methods over type parameters?",
        "What does `~int` mean in a constraint?",
    ],
    ["https://go.dev/doc/tutorial/generics", "https://go.dev/blog/intro-generics"],
    "generics_map",
)

add(
    12,
    "testing",
    "Testing, Table Tests, Fuzz, and Benchmarks",
    P2,
    "1–2 days",
    [
        "Write table-driven tests",
        "Use subtests with t.Run",
        "Introduce fuzz targets and benchmarks",
        "Treat tests as executable specifications",
    ],
    """
## Table-driven tests

```go
func TestClamp(t *testing.T) {
    tests := []struct{
        name string
        v, lo, hi, want int
    }{
        {"mid", 5, 0, 10, 5},
        {"low", -1, 0, 10, 0},
    }
    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            if got := Clamp(tt.v, tt.lo, tt.hi); got != tt.want {
                t.Fatalf("got %d want %d", got, tt.want)
            }
        })
    }
}
```

## Fuzzing

```go
func FuzzReverse(f *testing.F) {
    f.Add("go")
    f.Fuzz(func(t *testing.T, s string) {
        // property: reverse(reverse(s)) == s for runes...
    })
}
```

## Benchmarks

```go
func BenchmarkSum(b *testing.B) {
    xs := make([]int, 1000)
    for i := 0; i < b.N; i++ {
        Sum(xs)
    }
}
```

Run: `go test -bench=. -benchmem ./...`
""",
    [
        "Giant tests without cases (hard to see failures)",
        "Testing implementation details instead of behavior",
        "Ignoring flaky time/network tests — inject clocks and interfaces",
    ],
    [
        "Why table tests scale better?",
        "What does b.N mean?",
        "When is fuzzing valuable?",
    ],
    ["https://go.dev/doc/tutorial/add-a-test", "https://go.dev/security/fuzz/"],
    "testing_table",
)

add(
    13,
    "io-readers-writers",
    "I/O: io, Files, Readers and Writers",
    P2,
    "1–2 days",
    [
        "Use io.Reader and io.Writer as the core I/O abstractions",
        "Stream data without loading entire files when possible",
        "Compose readers (bufio, limit, multi)",
        "Always close resources with defer carefully",
    ],
    """
## The io contracts

```go
type Reader interface { Read(p []byte) (n int, err error) }
type Writer interface { Write(p []byte) (n int, err error) }
```

Almost all I/O in Go is streaming through these interfaces — files, sockets, buffers, compression.

```go
f, err := os.Open(path)
if err != nil { return err }
defer f.Close()
return io.Copy(dst, f)
```

## bufio

Wrap expensive readers/writers with buffering for small reads/writes.

## Errors

`io.EOF` signals end of stream — often expected, not always a hard failure.
`io.ErrUnexpectedEOF` means truncated data.
""",
    [
        "Loading multi-GB files into memory with os.ReadFile without need",
        "Forgetting defer Close",
        "Ignoring partial Write/Read return values",
    ],
    [
        "Why is io.Reader more powerful than \"give me []byte\"?",
        "What does io.Copy do?",
        "When is io.EOF expected?",
    ],
    ["https://pkg.go.dev/io", "https://go.dev/blog/laws-of-reflection"],
    "io_count",
)

add(
    14,
    "json-encoding-time",
    "JSON, Encoding, and Time",
    P2,
    "1 day",
    [
        "Marshal and unmarshal JSON with struct tags",
        "Handle time.Time and timezones carefully",
        "Validate unknown fields when needed",
        "Avoid floating point for money — use integers",
    ],
    """
## JSON

```go
type Event struct {
    ID   string    `json:"id"`
    At   time.Time `json:"at"`
    Name string    `json:"name,omitempty"`
}

b, err := json.Marshal(ev)
err = json.Unmarshal(b, &ev)
```

Use `Decoder` for streams; `Unmarshal` for whole buffers.

## Time

```go
now := time.Now().UTC()
t, err := time.Parse(time.RFC3339, s)
```

Store UTC; convert for display. Durations use `time.Duration` (nanoseconds under the hood).

## Encoding discipline

Be explicit about omitempty, pointers for null vs empty, and custom MarshalJSON only when needed.
""",
    [
        "Parsing local times without timezone",
        "Using float64 for currency in JSON",
        "Silent ignore of unknown fields in security-sensitive configs",
    ],
    [
        "What does `omitempty` do?",
        "Why prefer UTC storage?",
        "Decoder vs Unmarshal?",
    ],
    ["https://pkg.go.dev/encoding/json", "https://pkg.go.dev/time"],
    "json_roundtrip",
)

add(
    15,
    "context",
    "Context: Cancellation and Deadlines",
    P2,
    "1–2 days",
    [
        "Pass context.Context as the first parameter",
        "Derive cancel and timeout contexts",
        "Propagate cancellation through goroutines and RPCs",
        "Never store contexts in structs long-term (usually)",
    ],
    """
## Why context?

Distributed and concurrent programs need a signal: \"stop working, the caller left\".

```go
ctx, cancel := context.WithTimeout(parent, 2*time.Second)
defer cancel()

select {
case <-ctx.Done():
    return ctx.Err()
case res := <-results:
    return res, nil
}
```

## Rules of thumb

1. `ctx` is the first argument to functions that do I/O or wait.
2. Call `cancel` to free resources (use defer).
3. Do not pass `nil` context — use `context.Background()` or `TODO()` at edges.
4. Values in context are for request-scoped data (trace IDs), not optional parameters.

Cancellation is cooperative: your code must check `ctx.Done()` or call APIs that do.
""",
    [
        "Starting goroutines without tying them to ctx",
        "Using context for mandatory function parameters",
        "Forgetting defer cancel()",
    ],
    [
        "What does WithTimeout return?",
        "Why is cancel required?",
        "What error do you get when timed out?",
    ],
    ["https://go.dev/blog/context", "https://pkg.go.dev/context"],
    "context_timeout",
)

add(
    16,
    "reflection",
    "Reflection Overview (and When Not to Use It)",
    P2,
    "1 day",
    [
        "Explain reflect.Type and reflect.Value at a high level",
        "Recognize frameworks that use reflection (encoding/json)",
        "Prefer codegen or generics over heavy reflection",
        "Measure cost before using reflection in hot paths",
    ],
    """
## What reflection does

The `reflect` package inspects types and values at runtime — powerful and easy to abuse.

```go
func KindOf(v any) string {
    return reflect.TypeOf(v).Kind().String()
}
```

`encoding/json` uses reflection to map structs to JSON. That convenience costs CPU and clarity.

## Prefer

- Generics for type-safe containers
- Interfaces for behavior
- `go generate` / codegen for repetitive glue

Use reflection for marshaling, debugging tools, and DI frameworks — not business logic.
""",
    [
        "Building your whole domain model on map[string]any + reflect",
        "Ignoring panic risks from invalid reflect usage",
        "Premature \"flexible\" APIs that erase types",
    ],
    [
        "Name one stdlib package that uses reflection",
        "Why are generics often better?",
        "What is a hot-path risk of reflect?",
    ],
    ["https://go.dev/blog/laws-of-reflection", "https://pkg.go.dev/reflect"],
    "reflect_kind",
)

add(
    17,
    "idiomatic-go",
    "Idiomatic Go: Effective Patterns",
    P3,
    "1–2 days",
    [
        "Apply Effective Go naming and package heuristics",
        "Make the zero value useful",
        "Keep interfaces small and local",
        "Write clear Go that reviewers trust",
    ],
    """
## Names

- Packages: short, lowercase, no underscores (`http`, `json`)
- Interfaces: often `-er` (`Reader`) when one method
- Avoid stuttering: `http.Server` not `http.HTTPServer` in the package name sense

## Useful zero values

`var buf bytes.Buffer` works immediately. Design types so `var t T` is ready or clearly invalid.

## Return early

Flatten happy path; handle errors first. Avoid deep nesting.

## Don't communicate by sharing memory...

...share memory by communicating (channels) — but also learn mutexes (later). Idiomatic means choosing the right tool, not dogma.
""",
    [
        "Java-style getters for every field",
        "Huge package \"utils\" dumping grounds",
        "Interface pollution (exporting interfaces no one implements outside)",
    ],
    [
        "What is a useful zero value example?",
        "Why short package names?",
        "When is stuttering bad?",
    ],
    ["https://go.dev/doc/effective_go", "https://go.dev/wiki/CodeReviewComments"],
    "idiom_parse",
)

add(
    18,
    "project-layout",
    "Project Layout: Libraries vs Services",
    P3,
    "1 day",
    [
        "Choose layouts for libraries vs services",
        "Use cmd/, internal/, pkg/ judiciously",
        "Keep main thin — logic in packages",
        "Avoid premature micro-packages",
    ],
    """
## Common service layout

```
cmd/api/main.go      # wiring only
internal/server/     # private app code
internal/store/
go.mod
```

## Libraries

Export a stable API from the module root or clear subpackages.
Semantic import versioning: `/v2` path for major version 2+.

## Guidelines

- `internal/` for code you do not want strangers to import
- Prefer fewer packages until boundaries hurt
- Config via env/flags at main; pure functions underneath for tests
""",
    [
        "Copying a giant layout template for a 200-line tool",
        "Business logic inside main.go",
        "Exporting everything from pkg/ without need",
    ],
    [
        "What belongs in cmd/?",
        "Why internal/?",
        "When introduce a new package?",
    ],
    ["https://go.dev/doc/modules/layout", "https://github.com/golang-standards/project-layout"],
    "layout_quiz",
)

add(
    19,
    "profiling-performance",
    "Profiling, Race Detector, Performance Mental Model",
    P3,
    "1–2 days",
    [
        "Run the race detector and interpret failures",
        "Capture CPU and memory profiles with pprof",
        "Reason about allocations and escape analysis at a high level",
        "Optimize only with evidence",
    ],
    """
## Race detector

```bash
go test -race ./...
```

Detects concurrent reads/writes without synchronization. **Use it in CI.**

## pprof

```bash
go test -bench=. -cpuprofile=cpu.out
go tool pprof cpu.out
```

Or expose `/debug/pprof` on a debug port in services (carefully locked down).

## Mental model

1. Correctness first
2. Measure
3. Fix algorithmic issues before micro-opts
4. Reduce allocations in hot loops (preallocate slices, avoid string concat in loops)

Escape analysis decides heap vs stack; pointers and interfaces often force heap allocation.
""",
    [
        "Optimizing without benchmarks",
        "Disabling race detector because \"it's slow\" in CI forever",
        "Caching everything without eviction strategy",
    ],
    [
        "What does -race detect?",
        "Name two profile types",
        "Why measure before optimizing?",
    ],
    ["https://go.dev/blog/pprof", "https://go.dev/doc/articles/race_detector"],
    "perf_sum",
)

add(
    20,
    "docs-apis-semver",
    "Documentation, APIs, and Semantic Versioning",
    P3,
    "1 day",
    [
        "Write Go doc comments that godoc renders",
        "Design stable exported APIs",
        "Apply semver and Go modules major versions",
        "Deprecate thoughtfully",
    ],
    """
## Doc comments

```go
// Package store implements durable persistence for users.
package store

// Find returns a user by ID.
// It returns ErrNotFound if no user exists.
func Find(ctx context.Context, id string) (*User, error)
```

Start with the name of the symbol. Run `go doc` locally.

## Semver

- MAJOR: breaking changes (import path `/v2` for v2+)
- MINOR: compatible new features
- PATCH: bug fixes

## API design

- Accept interfaces, return structs (often)
- Keep exported surface small
- Prefer options structs over endless parameters
""",
    [
        "Breaking APIs without a major version",
        "Empty doc comments that restate the name only poorly",
        "Exporting types \"for later\"",
    ],
    [
        "What triggers a major version in Go modules?",
        "How should a doc comment start?",
        "Why keep the export surface small?",
    ],
    ["https://go.dev/doc/comment", "https://go.dev/doc/modules/release-workflow"],
    "docs_comment",
)

add(
    21, "complexity-recursion", "Complexity, Recursion, and Big-O Practice", P4, "1–2 days",
    ["Measure time/space with Big-O", "Trace recursive call trees", "Convert recursion to iteration when needed", "Estimate cost before coding"],
    """
## Big-O intuition

Big-O describes how runtime/memory grow as input size n grows.
Common classes: O(1), O(log n), O(n), O(n log n), O(n²), O(2ⁿ).

```go
// O(n)
func Sum(xs []int) int {
    s := 0
    for _, v := range xs { s += v }
    return s
}
```

Nested loops over the same n often mean O(n²). Sorting good algorithms are O(n log n).

## Recursion

```go
func Fib(n int) int {
    if n < 2 { return n }
    return Fib(n-1) + Fib(n-2) // exponential without memo
}
```

Always define base cases. Watch stack depth — Go stacks grow, but recursion depth still matters.

## Practice

For every algorithm you write: state expected complexity, then verify with benchmarks on growing n.
""",
    ["Calling naive Fib-like recursion in production", "Confusing average vs worst case", "Ignoring space complexity of maps/slices"],
    ["What does O(n log n) typically describe?", "Why is naive Fib exponential?", "How do you empirically check complexity?"],
    ["https://en.wikipedia.org/wiki/Big_O_notation"],
    "algo_fib",
)

add(
    22, "sorting-searching", "Sorting and Searching", P4, "1–2 days",
    ["Use sort package effectively", "Implement binary search correctly", "Know comparison contracts", "Avoid off-by-one errors"],
    """
## sort package

```go
sort.Ints(xs)
sort.Slice(people, func(i, j int) bool { return people[i].Age < people[j].Age })
```

## Binary search

Requires sorted input. Classic bug: midpoint overflow (use `lo+(hi-lo)/2`).

```go
func Search(xs []int, target int) int {
    lo, hi := 0, len(xs)
    for lo < hi {
        mid := lo + (hi-lo)/2
        if xs[mid] < target { lo = mid + 1 } else { hi = mid }
    }
    if lo < len(xs) && xs[lo] == target { return lo }
    return -1
}
```

## Stability

`sort.SliceStable` preserves equal-element order — useful for multi-key sorts.
""",
    ["Binary search on unsorted data", "Inclusive vs exclusive bounds confusion", "Expensive comparisons in comparators"],
    ["Preconditions for binary search?", "When use SliceStable?", "What is mid overflow?"],
    ["https://pkg.go.dev/sort"],
    "algo_search",
)

add(
    23, "linked-stacks-queues", "Linked Structures, Stacks, and Queues", P4, "1–2 days",
    ["Implement stack and queue with slices or lists", "Know when linked lists help vs hurt", "Reason about amortized append costs", "Use containers/list only when needed"],
    """
## Stack (LIFO)

Slice-backed stacks are idiomatic and cache-friendly:

```go
type Stack []int
func (s *Stack) Push(v int) { *s = append(*s, v) }
func (s *Stack) Pop() (int, bool) {
    if len(*s) == 0 { return 0, false }
    v := (*s)[len(*s)-1]
    *s = (*s)[:len(*s)-1]
    return v, true
}
```

## Queue (FIFO)

Can use slice with head index, ring buffer, or two stacks. Avoid O(n) `dequeue` from front without strategy.

## Linked lists

Useful for O(1) splice given a node; often slower than slices due to pointer chasing. Prefer slices first.
""",
    ["Always reaching for linked lists from textbook habit", "Queue via slice[1:] in hot path causing GC pressure", "Forgetting empty checks on Pop"],
    ["LIFO vs FIFO?", "Why are slices often faster than lists?", "Amortized cost of append?"],
    ["https://pkg.go.dev/container/list"],
    "algo_stack",
)

add(
    24, "trees-heaps", "Trees, Heaps, and Priority Queues", P4, "2 days",
    ["Implement binary tree traversals", "Use heap.Interface for priority queues", "Know BST search costs", "Apply heaps to scheduling problems"],
    """
## Binary tree

```go
type Node struct {
    Val int
    Left, Right *Node
}
```

Traversals: inorder, preorder, postorder, level-order (BFS with queue).

## Heaps / priority queues

`container/heap` needs `Len`, `Less`, `Swap`, `Push`, `Pop`.

Heaps give O(log n) push/pop and O(1) peek — perfect for:
- scheduling jobs by priority
- Dijkstra's algorithm
- top-K queries

## BST intuition

Balanced BST: O(log n) search. Unbalanced (sorted inserts): O(n). Production often uses maps (hash) or specialized trees.
""",
    ["Assuming BST is always log n", "Incorrect Less making heap invalid", "Mutating heap slice outside heap functions"],
    ["Complexity of heap push?", "Name three traversals", "When use priority queue in infra?"],
    ["https://pkg.go.dev/container/heap"],
    "algo_heap",
)

add(
    25, "graphs", "Graphs: BFS, DFS, Shortest Paths Intro", P4, "2 days",
    ["Represent graphs with adjacency lists", "Implement BFS and DFS", "Detect cycles in directed graphs", "Introduce Dijkstra at a conceptual+code level"],
    """
## Representation

```go
type Graph map[string][]string // adjacency list
```

Prefer adjacency lists for sparse graphs (most real networks).

## BFS / DFS

- BFS: queue — shortest path in unweighted graphs
- DFS: stack/recursion — cycle detection, topological vibes

```go
func BFS(g Graph, start string) []string {
    seen := map[string]bool{start: true}
    q := []string{start}
    var order []string
    for len(q) > 0 {
        u := q[0]; q = q[1:]
        order = append(order, u)
        for _, v := range g[u] {
            if !seen[v] { seen[v] = true; q = append(q, v) }
        }
    }
    return order
}
```

## Weighted shortest paths

Dijkstra with a priority queue finds shortest paths for non-negative weights — core infra for routing and dependency costs.
""",
    ["Adjacency matrix for huge sparse graphs", "Forgetting seen set → infinite loops", "Dijkstra with negative edges"],
    ["When BFS vs DFS?", "Why adjacency list?", "Dijkstra precondition?"],
    ["https://en.wikipedia.org/wiki/Graph_traversal"],
    "algo_bfs",
)

add(
    26, "hashing-bloom", "Hashing and Bloom Filters (Infra-Relevant)", P4, "1–2 days",
    ["Explain hash maps vs cryptographic hashes", "Implement a simple bloom filter", "Reason about false positives", "Apply hashing to caches and shards"],
    """
## Hash tables (maps)

Go's `map` is a hash table: average O(1) lookup. Hash collisions are handled internally.

## Cryptographic vs non-crypto

- `hash/fnv`, `maphash`: fast, non-crypto
- `crypto/sha256`: integrity / security

Do not use non-crypto hashes for security tokens.

## Bloom filters

Probabilistic set: can say \"possibly in set\" or \"definitely not\".
Uses bit array + k hash functions. False positives; no false negatives (for standard bloom).

Used in: databases (skip disk reads), caches, distributed systems membership tests.

Tradeoff: memory vs false positive rate.
""",
    ["Using MD5 for security (broken)", "Ignoring bloom false positives in logic", "Rolling your own crypto"],
    ["What can a bloom filter never say?", "When use sha256 vs fnv?", "Why maps are O(1) average?"],
    ["https://pkg.go.dev/hash", "https://en.wikipedia.org/wiki/Bloom_filter"],
    "algo_bloom",
)

add(
    27, "dynamic-programming", "Dynamic Programming Patterns", P4, "2 days",
    ["Identify overlapping subproblems", "Write bottom-up DP tables", "Memoize top-down recursion", "Apply classic patterns (knapsack, LIS, paths)"],
    """
## Idea

DP stores answers to subproblems to avoid recomputation.

```go
// Climb stairs: ways(n) = ways(n-1)+ways(n-2)
func Climb(n int) int {
    if n < 2 { return 1 }
    a, b := 1, 1
    for i := 2; i <= n; i++ {
        a, b = b, a+b
    }
    return b
}
```

## Pattern checklist

1. Define state clearly (`dp[i]` means …)
2. Write recurrence
3. Determine base cases
4. Choose iteration order
5. Optimize space if only last states needed

## Infra relevance

DP appears in scheduling, rate allocation, tokenization costs, and alignment-like problems — not only interview questions.
""",
    ["Memoizing without clear state definition", "Off-by-one in table sizes", "Exponential backtracking labeled as DP"],
    ["Overlapping subproblems meaning?", "Top-down vs bottom-up?", "When reduce DP space?"],
    ["https://en.wikipedia.org/wiki/Dynamic_programming"],
    "algo_dp",
)

add(
    28, "algorithm-drills", "Algorithmic Problem Set (Mixed Drills)", P4, "2–3 days",
    ["Solve mixed problems under constraints", "State complexity before coding", "Write tests first for edge cases", "Refactor brute force to efficient solutions"],
    """
## Drill protocol

For each problem:
1. Restate inputs/outputs and constraints
2. Work an example by hand
3. Propose brute force + complexity
4. Improve if needed
5. Implement in Go with table tests
6. Benchmark if n is large

## Problem themes in the exercises

- Two-sum variants with maps
- Sliding window
- Interval merge
- Top-K with heaps
- Graph connectivity

Treat this lesson as a gym: correctness under pressure, then clarity.
""",
    ["Coding before examples", "Silent assumption about sorted input", "Mutating inputs unexpectedly"],
    ["What is your first step before code?", "How do you pick a data structure?", "When is brute force OK?"],
    ["https://go.dev/blog/slices"],
    "algo_twosum",
)

add(
    29, "goroutines", "Goroutines and the Scheduler", P5, "1–2 days",
    ["Start goroutines with go", "Explain M:N scheduling at a high level", "Avoid leaking goroutines", "Synchronize completion with WaitGroup"],
    """
## Goroutines

```go
go func() {
    doWork()
}()
```

Goroutines are lightweight concurrent functions multiplexed onto OS threads by the Go scheduler (M:N).

## Leaks

A goroutine leak is a goroutine that never exits — common when blocked on channel/IO forever.
Always plan an exit path (context, close channel, timeout).

## WaitGroup

```go
var wg sync.WaitGroup
wg.Add(1)
go func() {
    defer wg.Done()
    work()
}()
wg.Wait()
```

Do not assume goroutine order. Concurrency ≠ parallelism (but Go gives you both tools).
""",
    ["Fire-and-forget goroutines in request handlers without limits", "Capturing loop variables incorrectly (modern Go fixed per-iteration vars; still be careful)", "Waiting forever with no timeout"],
    ["What does the go keyword do?", "What is a goroutine leak?", "Why WaitGroup?"],
    ["https://go.dev/tour/concurrency", "https://go.dev/blog/scheduler"],
    "conc_waitgroup",
)

add(
    30, "channels-select", "Channels, Select, and Pipelines", P5, "2 days",
    ["Create buffered and unbuffered channels", "Use select for multi-wait", "Build pipeline stages", "Close channels from the sender side only"],
    """
## Channels

```go
ch := make(chan int)      // unbuffered
buf := make(chan int, 16) // buffered
ch <- 3
v := <-ch
close(ch)
```

Unbuffered send/receive synchronizes two goroutines. Buffer decouples up to capacity.

## select

```go
select {
case v := <-in:
    // handle
case <-ctx.Done():
    return ctx.Err()
case out <- v:
    // send
default:
    // non-blocking path
}
```

## Pipelines

Stage functions: `in <-chan T` → `out <-chan U`, close out when done.
Receivers use `for v := range ch`.
""",
    ["Closing channels from receivers", "Sending on closed channel (panic)", "Unbounded goroutine fan-out without backpressure"],
    ["Who should close a channel?", "Buffered vs unbuffered?", "What does range on channel do?"],
    ["https://go.dev/blog/pipelines"],
    "conc_pipeline",
)

add(
    31, "mutexes-atomics", "Mutexes, Atomics, and sync Primitives", P5, "1–2 days",
    ["Protect shared memory with mutexes", "Use RWMutex for read-heavy maps", "Know atomic operations for simple counters", "Prefer confining data to one goroutine when possible"],
    """
## Mutex

```go
type Safe struct {
    mu sync.Mutex
    m  map[string]int
}

func (s *Safe) Inc(k string) {
    s.mu.Lock()
    defer s.mu.Unlock()
    s.m[k]++
}
```

## Atomics

`atomic.Int64` for counters without mutex — not a free pass for complex invariants.

## Design preference

1. Don't share (owning goroutine)
2. Channels for ownership transfer
3. Mutex for shared structures
4. Atomics for simple stats

Always `go test -race`.
""",
    ["Copying a struct containing a mutex", "Holding locks across slow I/O", "Assuming map access is safe concurrently"],
    ["Why defer Unlock?", "RWMutex when?", "Why race detector with mutex code?"],
    ["https://pkg.go.dev/sync", "https://pkg.go.dev/sync/atomic"],
    "conc_mutex",
)

add(
    32, "worker-pools", "Worker Pools, Fan-in/out, Backpressure", P5, "2 days",
    ["Build a bounded worker pool", "Apply fan-out / fan-in patterns", "Implement backpressure with buffered channels", "Bound concurrency in servers"],
    """
## Worker pool

```go
jobs := make(chan Job)
results := make(chan Result)
for i := 0; i < workers; i++ {
    go worker(ctx, jobs, results)
}
```

Bound the number of goroutines doing expensive work. Unbounded `go` per request is a common outage cause.

## Backpressure

When consumers are slow, producers must block or drop according to policy.
Buffered channels provide limited slack — not infinite queues.

## Fan-out / fan-in

Split work across workers (fan-out), merge results (fan-in) with a WaitGroup + results channel.
""",
    ["Unbuffered infinite job pileup in memory via huge buffers", "No context cancellation on shutdown", "Result channel deadlock when workers exit wrong"],
    ["Why bound workers?", "What is backpressure?", "How merge results safely?"],
    ["https://go.dev/blog/pipelines"],
    "conc_pool",
)

add(
    33, "deadlocks-races", "Deadlocks, Races, and Cancellation Patterns", P5, "1–2 days",
    ["Recognize classic deadlock patterns", "Eliminate data races systematically", "Cancel in-flight work with context", "Write concurrency regression tests"],
    """
## Deadlocks

Common causes:
- Lock ordering A then B vs B then A
- Two goroutines waiting on each other unbuffered
- WaitGroup Add inside the goroutine incorrectly

## Races

A data race: concurrent access to a variable, at least one write, no sync.
Fix by synchronizing or not sharing.

## Cancellation pattern

```go
func worker(ctx context.Context, in <-chan Task) error {
    for {
        select {
        case <-ctx.Done():
            return ctx.Err()
        case t, ok := <-in:
            if !ok { return nil }
            if err := handle(ctx, t); err != nil { return err }
        }
    }
}
```
""",
    ["\"It didn't race on my machine\" without -race", "Fixing races by sleeping", "Nested locks without ordering rules"],
    ["Define data race", "Give a deadlock example", "How context prevents abandoned work?"],
    ["https://go.dev/doc/articles/race_detector"],
    "conc_cancel",
)

add(
    34, "concurrent-algorithms", "Concurrent Algorithm Drills", P5, "2 days",
    ["Parallelize map-reduce style workloads", "Compute safely with bounded concurrency", "Compare sequential vs parallel benchmarks", "Preserve determinism in tests"],
    """
## Drill themes

- Parallel sum / histogram with shard-per-worker then merge
- Concurrent crawler with URL graph + visited set (mutex or owning map goroutine)
- Pipeline: read → parse → enrich → write

## Rules

- Bound parallelism to GOMAXPROCS or a chosen limit
- No shared map writes without sync
- Tests must be deterministic (sort outputs)

Measure: sometimes parallel is slower due to coordination overhead — learn when.
""",
    ["Racing on shared maps", "More goroutines than work items blindly", "Non-deterministic test flakes ignored"],
    ["When parallelization fails to help?", "How to merge partial histograms?", "Why sort in tests?"],
    ["https://pkg.go.dev/sync"],
    "conc_parsum",
)

add(
    35, "http-net", "HTTP Servers and Clients (net/http)", P6, "2 days",
    ["Build handlers with net/http", "Use http.Client with timeouts", "Understand middleware chaining", "Serve JSON APIs safely"],
    """
## Server

```go
mux := http.NewServeMux()
mux.HandleFunc("GET /health", func(w http.ResponseWriter, r *http.Request) {
    w.WriteHeader(http.StatusOK)
    _, _ = w.Write([]byte("ok"))
})
srv := &http.Server{Addr: ":8080", Handler: mux, ReadHeaderTimeout: 5 * time.Second}
log.Fatal(srv.ListenAndServe())
```

Always set timeouts. Infinite hangs are outages.

## Client

```go
client := &http.Client{Timeout: 10 * time.Second}
resp, err := client.Get(url)
```

Reuse clients; do not create one per request. Close response bodies.

## Context

`r.Context()` cancels when the client disconnects — respect it in handlers.
""",
    ["Default client with no timeout", "Ignoring resp.Body.Close()", "Blocking handler work without goroutine limits"],
    ["Why ReadHeaderTimeout?", "How reuse http.Client?", "What cancels r.Context()?"],
    ["https://pkg.go.dev/net/http"],
    "http_health",
)

add(
    36, "rest-middleware-auth", "REST API Design, Middleware, Auth Basics", P6, "2 days",
    ["Design resource-oriented REST endpoints", "Implement middleware for logging/auth", "Use bearer tokens / basic auth patterns", "Return consistent error JSON"],
    """
## REST sketch

- `GET /items` list
- `GET /items/{id}` get
- `POST /items` create
- `DELETE /items/{id}` delete

Use proper status codes: 201 create, 404 missing, 400 validation, 401/403 auth.

## Middleware

```go
func WithRequestID(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        id := r.Header.Get("X-Request-ID")
        if id == "" { id = uuidNew() }
        ctx := context.WithValue(r.Context(), ctxKeyID, id)
        w.Header().Set("X-Request-ID", id)
        next.ServeHTTP(w, r.WithContext(ctx))
    })
}
```

## Auth basics

Validate `Authorization` header; never roll crypto casually — use proven libraries.
Separate authentication (who) from authorization (what allowed).
""",
    ["Leaking stack traces to clients", "Auth only on some routes by accident", "Using GET for state changes"],
    ["401 vs 403?", "What does middleware do?", "Why consistent error shape?"],
    ["https://go.dev/doc/tutorial/web-service-gin"],
    "http_middleware",
)

add(
    37, "grpc-protobuf", "gRPC and Protobuf Intro", P6, "2 days",
    ["Explain protobuf IDL and codegen", "Sketch a gRPC service in Go", "Compare gRPC vs JSON HTTP", "Handle deadlines via context"],
    """
## Why gRPC?

- Strongly typed contracts (`.proto`)
- Efficient binary encoding
- Streaming RPCs
- First-class deadlines/status codes

## Flow

1. Write `service.proto`
2. Generate Go with `protoc` / `buf`
3. Implement server interface
4. Dial with client stubs

## vs REST/JSON

Use gRPC for internal service meshes and streaming; REST/JSON for public browser-facing APIs often still wins.

Contexts carry deadlines across gRPC calls — wire them end-to-end.
""",
    ["Exposing gRPC directly to browsers without grpc-web/gateway", "Ignoring status codes (use codes.NotFound etc.)", "Huge protobuf messages without pagination"],
    ["What does codegen produce?", "When prefer gRPC?", "How deadlines propagate?"],
    ["https://grpc.io/docs/languages/go/quickstart/"],
    "grpc_sketch",
)

add(
    38, "databases-sql", "Databases: SQL Drivers, Transactions, Migrations", P6, "2 days",
    ["Use database/sql with a driver", "Wrap multi-step writes in transactions", "Think in migrations for schema change", "Avoid SQL injection with parameters"],
    """
## database/sql

```go
db, err := sql.Open("pgx", dsn)
db.SetMaxOpenConns(20)
row := db.QueryRowContext(ctx, `SELECT name FROM users WHERE id=$1`, id)
```

Always use contexts and placeholders — never string-concatenate user input into SQL.

## Transactions

```go
tx, err := db.BeginTx(ctx, nil)
defer tx.Rollback()
// execs...
return tx.Commit()
```

## Migrations

Treat schema as versioned code (golang-migrate, goose, atlas). Expand/contract for zero-downtime.
""",
    ["sql.Open without Ping", "Holding transactions open during HTTP calls to others", "SELECT * forever"],
    ["Why placeholders?", "What does Rollback on defer do after Commit?", "Expand/contract meaning?"],
    ["https://pkg.go.dev/database/sql"],
    "sql_param",
)

add(
    39, "caching-redis", "Caching, Redis Patterns, Idempotency", P6, "1–2 days",
    ["Apply cache-aside pattern", "Choose TTLs and invalidation strategies", "Implement idempotency keys for writes", "Understand stampede risks"],
    """
## Cache-aside

1. Read cache
2. On miss: read DB, populate cache
3. On write: update DB, invalidate key

## Redis roles

- Cache
- Rate limiting
- Distributed locks (carefully)
- Queues / streams

## Idempotency

For payment-like POSTs, clients send `Idempotency-Key`. Server stores result of first processing and replays it — critical for at-least-once delivery worlds.

## Thundering herd

When hot key expires, many requests hit DB. Mitigate with singleflight / locking / soft expiry.
""",
    ["Caching without TTL", "Using Redis locks without expiry", "Assuming cache is always consistent with DB"],
    ["What is cache-aside?", "Why idempotency keys?", "What is a stampede?"],
    ["https://redis.io/docs/manual/patterns/"],
    "cache_aside",
)

add(
    40, "observability", "Observability: Logs, Metrics, Tracing", P6, "1–2 days",
    ["Emit structured logs", "Define RED/USE metrics", "Propagate trace IDs", "Make dashboards actionable"],
    """
## Three pillars

- **Logs**: discrete events (structured JSON)
- **Metrics**: aggregates (counters, histograms)
- **Traces**: request journeys across services

```go
slog.Info("request completed", "method", r.Method, "path", r.URL.Path, "status", status, "dur_ms", ms)
```

## Metrics that matter

For services: rate, errors, duration (RED). Histograms for latency percentiles.

## Tracing

Pass trace context in headers; OpenTelemetry is the common standard. Sample wisely in production.
""",
    ["Println debugging as the only strategy", "High-cardinality metric labels (user IDs)", "Logging secrets/PII"],
    ["RED metrics are?", "Why structured logs?", "Danger of high cardinality?"],
    ["https://pkg.go.dev/log/slog", "https://opentelemetry.io/"],
    "obs_log",
)

add(
    41, "containers-docker", "Containers and Multi-stage Docker Builds for Go", P6, "1–2 days",
    ["Write a multi-stage Dockerfile for Go", "Build static/small images", "Run as non-root", "Understand layer caching"],
    """
## Multi-stage pattern

```dockerfile
FROM golang:1.22 AS build
WORKDIR /src
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 go build -o /out/app ./cmd/api

FROM gcr.io/distroless/static:nonroot
COPY --from=build /out/app /app
USER nonroot:nonroot
ENTRYPOINT ["/app"]
```

## Why

- Tiny attack surface
- Reproducible builds
- Same artifact from laptop to prod

Pin base image digests in serious deployments. Pass version via ldflags.
""",
    ["Shipping build toolchain in prod image", "Running as root", "COPY . . before go mod download (breaks cache)"],
    ["Why multi-stage?", "What does CGO_ENABLED=0 help?", "Why nonroot?"],
    ["https://docs.docker.com/language/golang/build-images/"],
    "docker_multistage",
)

add(
    42, "kubernetes-go", "Kubernetes-Oriented Go: Controllers and client-go", P6, "2–3 days",
    ["Explain control loops (reconcile)", "Sketch a controller with client-go concepts", "Use leader election awareness", "Design for level-triggered reconciliation"],
    """
## Control loop

Kubernetes controllers observe desired state (spec) and drive actual state toward it — continuously.

```
for {
  desired := getSpec()
  actual := getStatus()
  if actual != desired { act() }
}
```

## client-go concepts

Informers/caches reduce API spam; workqueues debounce; reconcile must be idempotent.

## Operators

Encode domain ops knowledge as controllers. Go dominates this ecosystem.

You do not need a cluster for the exercise — implement a tiny reconcile function over an in-memory store.
""",
    ["One-shot scripts instead of reconcile loops", "Non-idempotent reconciles", "Hot-looping without backoff"],
    ["What is reconcile?", "Why idempotent?", "Role of informers?"],
    ["https://github.com/kubernetes/client-go"],
    "k8s_reconcile",
)

add(
    43, "cloud-sdk-patterns", "Cloud SDK Patterns: Config, Retries, Pagination", P6, "1–2 days",
    ["Configure clients via env/role credentials", "Retry with exponential backoff + jitter", "Paginate list APIs correctly", "Treat cloud APIs as unreliable networks"],
    """
## Retries

Retry transient errors (timeouts, 429, 503), not validation errors.
Exponential backoff with jitter prevents synchronized stampedes.

```go
func Retry(ctx context.Context, fn func() error) error {
    // backoff loop checking ctx.Done()
}
```

## Pagination

Most list APIs return a cursor/token. Loop until empty. Bound max pages.

## Config

Prefer IAM roles / workload identity over long-lived keys in files.
Separate config loading from business logic for tests.
""",
    ["Infinite retries without deadline", "Retrying non-idempotent POSTs blindly", "Loading all pages into memory without need"],
    ["What is jitter?", "Which errors retry?", "Why cursor pagination?"],
    ["https://aws.github.io/aws-sdk-go-v2/docs/"],
    "cloud_retry",
)

add(
    44, "reliability", "Reliability: Timeouts, Circuit Breakers, Graceful Shutdown", P6, "2 days",
    ["Propagate deadlines everywhere", "Implement circuit breaker behavior", "Shut down HTTP servers gracefully", "Define SLOs mentally"],
    """
## Timeouts

Every external call needs a deadline. Inherit from request context when serving HTTP.

## Circuit breaker

When dependency error rate spikes, fail fast temporarily to allow recovery — then probe half-open.

## Graceful shutdown

```go
go func() { _ = srv.ListenAndServe() }()
<-stop
ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
defer cancel()
_ = srv.Shutdown(ctx)
```

Drain in-flight requests; stop accepting new ones.

## SLO mindset

Availability and latency targets drive timeout budgets and retry policies.
""",
    ["Kill -9 as the only deploy strategy", "No timeout on outbound calls", "Circuit breaker without metrics"],
    ["What does Shutdown do?", "Fail-fast purpose?", "Timeout budget meaning?"],
    ["https://pkg.go.dev/net/http#Server.Shutdown"],
    "reliab_shutdown",
)

add(
    45, "numerics-gonum", "Numerics and Tensors in Go (gonum)", P7, "2 days",
    ["Use float64 carefully", "Perform vector ops with gonum-style APIs", "Know floating-point pitfalls", "Benchmark numeric kernels"],
    """
## Floating point

Floats are approximations. Never compare with `==` without tolerance.
Summation order changes results; catastrophic cancellation is real.

## gonum

The gonum organization provides matrices, stats, graph, optimize packages — Go's scientific backbone.

```go
// Dot product
func Dot(a, b []float64) float64 {
    var s float64
    for i := range a { s += a[i] * b[i] }
    return s
}
```

## AI relevance

Even when models run elsewhere, Go services still normalize features, compute similarities, and batch tensors as bytes.
""",
    ["Equality checks on floats", "Ignoring NaN propagation", "Using float32 without need then losing precision"],
    ["Why epsilon comparisons?", "What is gonum used for?", "Dot product complexity?"],
    ["https://www.gonum.org/"],
    "ai_dot",
)

add(
    46, "ml-pipelines", "ML-Adjacent Pipelines: ETL, Batching, Features", P7, "2 days",
    ["Build ETL stages as interfaces", "Batch records for throughput", "Validate feature schemas", "Make pipelines restartable"],
    """
## Pipeline stages

```go
type Stage[In, Out any] interface {
    Process(ctx context.Context, in In) (Out, error)
}
```

Compose extract → transform → load. Each stage should be testable offline.

## Batching

Micro-batches improve throughput to model APIs and DBs. Flush on size or time (`time.Ticker`).

## Features

Document types/units. Version feature schemas. Reject bad rows early with metrics.

Idempotent loaders let you replay safely after failures.
""",
    ["Giant unbounded buffers", "Schema-free JSON forever", "Silent dropping of bad rows without metrics"],
    ["Why batch?", "What makes a pipeline restartable?", "Stage interface benefit?"],
    ["https://go.dev/blog/pipelines"],
    "ai_batch",
)

add(
    47, "model-apis", "Calling Model APIs: HTTP and SSE Streaming", P7, "2 days",
    ["Call LLM HTTP APIs with timeouts", "Parse streaming SSE responses", "Handle rate limits and retries", "Bound concurrency to model backends"],
    """
## Request shape

Most model APIs are HTTPS JSON. Stream tokens via Server-Sent Events (SSE) or chunked HTTP.

```go
req, _ := http.NewRequestWithContext(ctx, http.MethodPost, url, body)
req.Header.Set("Authorization", "Bearer "+key)
req.Header.Set("Accept", "text/event-stream")
```

## SSE parsing

Read line-oriented `data: ...` frames until `[DONE]`. Respect ctx cancellation mid-stream.

## Production concerns

- Token/cost accounting
- Prompt injection awareness at boundaries
- Never log raw secrets or full prompts if sensitive
""",
    ["No timeout on stream reads", "Buffering entire stream before forwarding", "Unbounded parallel calls to the model"],
    ["What is SSE?", "Why cancel mid-stream?", "Which headers matter?"],
    ["https://platform.openai.com/docs/api-reference"],
    "ai_sse",
)

add(
    48, "embeddings-vectors", "Embeddings, Vector Search, Similarity", P7, "2 days",
    ["Compute cosine similarity", "Normalize vectors", "Sketch top-K retrieval", "Understand ANN vs exact search"],
    """
## Embeddings

Vectors representing text/images. Similarity ≈ semantic closeness.

```go
func Cosine(a, b []float64) float64 {
    return Dot(a, b) / (Norm(a) * Norm(b))
}
```

## Retrieval

Exact: scan all docs O(n·d). Approximate Nearest Neighbor (ANN) libraries trade recall for speed (HNSW, IVF).

## Go's role

Go often owns the service: store vectors (pgvector/remote DB), retrieve top-K, pass chunks to the LLM.
""",
    ["Forgetting to normalize before dot-as-cosine", "Comparing vectors from different models", "n² algorithms on large corpora without ANN"],
    ["Cosine vs dot product?", "What is ANN?", "Why model versioning matters?"],
    ["https://en.wikipedia.org/wiki/Cosine_similarity"],
    "ai_cosine",
)

add(
    49, "rag-service", "RAG Service in Go: Chunk → Embed → Retrieve → Generate", P7, "2–3 days",
    ["Chunk text with overlap", "Orchestrate embed+retrieve+generate", "Cite sources in answers", "Evaluate retrieval quality"],
    """
## RAG pipeline

1. **Chunk** documents (size + overlap)
2. **Embed** chunks → vectors
3. On query: embed query → **retrieve** top-K chunks
4. **Generate** answer with LLM using retrieved context
5. Return answer + citations

## Go orchestration

Go shines as the reliable orchestrator: timeouts, concurrency, observability, auth.

```go
chunks := Chunk(doc, 500, 50)
// embed + store
hits := store.TopK(ctx, queryVec, 5)
answer, err := llm.Generate(ctx, prompt(hits, question))
```

Keep prompts and models versioned. Measure hit rate and groundedness.
""",
    ["Huge chunks blowing context windows", "No citations", "Retrieving without metadata filters"],
    ["Why overlap in chunking?", "What are citations for?", "Where does Go sit in RAG?"],
    ["https://www.anthropic.com/engineering"],
    "ai_chunk",
)

add(
    50, "inference-serving", "Inference Serving: Batching, Queues, Sidecars", P7, "2 days",
    ["Queue inference requests", "Dynamic batch for GPU efficiency", "Use sidecar patterns for model runtimes", "Expose SLOs for latency vs throughput"],
    """
## Serving shapes

- **Sync API**: simple, limited throughput
- **Queue + workers**: smooth spikes
- **Dynamic batching**: wait briefly to batch requests for GPU

## Sidecar

Go app handles auth, quotas, routing; model runtime (Python/C++/TensorRT) runs beside it.
Communicate via localhost gRPC/HTTP.

## Tradeoffs

Batching raises latency p50 slightly to improve throughput — tune wait windows with metrics.
""",
    ["One goroutine per GPU call unbounded", "No max queue depth (OOM)", "Ignoring tail latency"],
    ["Why dynamic batching?", "What is a sidecar?", "Queue depth purpose?"],
    ["https://go.dev/blog/pipelines"],
    "ai_infer_queue",
)

add(
    51, "agents-tools", "Agents and Tools: Function-Calling Loops", P7, "2 days",
    ["Implement tool schemas", "Run a bounded agent loop", "Sandbox dangerous tools", "Enforce max steps and budgets"],
    """
## Agent loop

```
for step := 0; step < maxSteps; step++ {
  decision := llm.Next(history)
  if decision.Type == "final" { return decision.Answer }
  result := tools.Run(decision.Tool, decision.Args)
  history = append(history, result)
}
```

## Safety

- Allowlist tools
- Validate args against JSON schema
- Timeouts per tool
- Human approval for side-effecting ops
- Hard caps on steps/tokens/cost

Go's type system and explicit errors help keep tool runners boring and safe.
""",
    ["Unbounded loops", "Executing shell from model output unchecked", "Trusting model JSON without validation"],
    ["Why maxSteps?", "What to validate before tools.Run?", "Allowlist purpose?"],
    ["https://go.dev/blog/error-handling-and-go"],
    "ai_agent_loop",
)

add(
    52, "eval-harnesses", "Evaluating AI Systems in Go", P7, "2 days",
    ["Build offline eval datasets", "Measure latency/cost/quality", "Automate regression evals in CI", "Separate unit tests from model evals"],
    """
## What to measure

- **Latency**: p50/p95 end-to-end
- **Cost**: tokens / $ per request
- **Quality**: exact match, rubrics, LLM-as-judge (carefully), retrieval recall@k

## Harness

```go
for _, tc := range dataset {
    started := time.Now()
    out, err := system.Run(ctx, tc.In)
    // record metrics + score(out, tc.Want)
}
```

Gate releases on eval thresholds. Keep golden sets versioned.

Unit-test pure functions (chunking, cosine); eval the full system less frequently.
""",
    ["Only vibe-checking prompts", "Flaky online evals without seeds", "Optimizing cost while quality collapses"],
    ["Name three metric classes", "Why golden sets?", "What belongs in CI vs nightly?"],
    ["https://go.dev/blog/survey2024-overview"],
    "ai_eval",
)

add(
    53, "capstone-infra", "Capstone: Production-Shaped HTTP API", P8, "3–5 days",
    ["Ship an API with graceful shutdown", "Add metrics, retries, worker pool", "Write integration tests", "Document runbook notes"],
    """
## Mission

Build a small but production-shaped service:

- REST endpoints for a job queue resource
- Enqueue is fast; workers process asynchronously
- Graceful shutdown drains workers
- Structured logs + basic metrics counters
- Outbound calls use retries + timeouts
- `GET /healthz` and `GET /readyz`

## Milestones

1. Skeleton server + config
2. In-memory store + handlers
3. Worker pool + backpressure
4. Observability + shutdown
5. Tests + README

## Rubric (excellent)

- No goroutine leaks on shutdown
- Race-clean tests
- Clear package boundaries
- Explicit error types for API
- Timeouts everywhere
""",
    ["God-object main.go", "In-memory only without interfaces (hard to test)", "Skipping readiness vs liveness"],
    ["What does readyz mean?", "How prove no leaks?", "Where put business logic?"],
    ["https://go.dev/doc/tutorial/web-service-gin"],
    "capstone_infra",
)

add(
    54, "capstone-algorithms", "Capstone: Search / Graph Engine Core", P8, "3–5 days",
    ["Implement indexing + query", "Prove complexity with benchmarks", "Cover edge cases with tests", "Document API and limits"],
    """
## Mission

Build an in-memory search or routing core:

Option A: inverted index for document search (tokenizeize → postings → rank)
Option B: weighted graph shortest path service (Dijkstra)

## Milestones

1. Data model + ingest
2. Query algorithm + ranking/path
3. Table tests for correctness
4. Benchmarks at 10k+ entities
5. Optional: concurrent read-safe index with RWMutex

## Rubric (excellent)

- Stated complexities match implementation
- Deterministic results
- Clean exports and docs
- Benchmarks show scaling behavior
""",
    ["Unbenchmarked \"optimizations\"", "Global mutable state without sync", "No empty-query handling"],
    ["Which option did you pick and why?", "What is your query complexity?", "How test concurrency?"],
    ["https://pkg.go.dev/container/heap"],
    "capstone_algo",
)

add(
    55, "capstone-ai", "Capstone: Mini RAG / Embedding Search Service", P8, "4–6 days",
    ["Implement chunk→embed→retrieve→answer orchestration", "Serve concurrent requests safely", "Add observability and eval harness", "Document failure modes"],
    """
## Mission

Build a mini RAG service in Go:

- Ingest text documents (HTTP upload or CLI)
- Chunk + embed (embedder can be mocked/fake for tests)
- Query endpoint returns answer + citations
- Concurrent requests bounded by worker pool / semaphore
- Logs/metrics for latency and retrieval hit counts
- Offline eval over a tiny golden set

## Milestones

1. Domain types + fake embedder/LLM
2. Chunk + store + cosine top-K
3. HTTP API + context timeouts
4. Concurrency limits + graceful shutdown
5. Eval harness + README architecture diagram

## Rubric (excellent)

- Interfaces for embedder/LLM (swap real later)
- Race-clean
- Clear citation UX
- Eval numbers recorded in repo
- Thoughtful limits (max docs, max tokens)
""",
    ["Calling real paid APIs without mocks in unit tests", "No cancellation", "Unbounded document size"],
    ["What did you mock and why?", "How bound concurrency?", "What eval metric did you pick?"],
    ["https://go.dev/blog/context"],
    "capstone_ai",
)

# --- EXPANDED_BODIES_APPLIED ---

# Expanded teaching bodies applied to LATER (body / guides / examples).
def _apply_expansions():
    expansions = {
        9: dict(
            body="""
## Why this matters

Interfaces are how Go does polymorphism without inheritance. Small interfaces (io.Reader) are the secret to testable, composable infrastructure code.

This lesson is a building block for later modules in the Goodway path. If you only
skim, the exercises will feel like busywork; if you type the examples and narrate
them aloud, the same patterns will reappear in HTTP handlers, concurrency, and AI
service glue.

## Core concepts

- Satisfaction is implicit: no `implements` keyword.
- Accept interfaces, return concrete types in most APIs.
- Compose interfaces by embedding (ReadWriter).
- `any` is empty interface — prefer generics or real interfaces when possible.
- Interface values hold (type, value) pairs; nil interface vs nil pointer matters.

Hold these in working memory while you code. Each bullet should map to something
you can demonstrate with a three-line program or a failing compile error.

## Worked Go examples

Create a scratch module and type this yourself (do not paste blindly):

```bash
mkdir -p /tmp/gw-interfaces && cd /tmp/gw-interfaces
go mod init example.com/scratch
```

Then create `main.go`:

```go
package main

import "fmt"

type Shape interface{ Area() float64 }
type Rect struct{ W, H float64 }

func (r Rect) Area() float64 { return r.W * r.H }

func TotalArea(shapes []Shape) float64 {
    var s float64
    for _, sh := range shapes {
        s += sh.Area()
    }
    return s
}

func main() {
    fmt.Println(TotalArea([]Shape{Rect{2, 3}, Rect{1, 1}}))
}
```

Run it:

```bash
go run .
```

Expected output:

```text
7
```

If your output differs, diff character-by-character — especially whitespace and
types. Then change one line deliberately and predict the new output before running.

## Mini-lab (`go run` steps)

1. Define Shape + Rect; sum areas via []Shape.
2. Add Circle and pass both to TotalArea without changing TotalArea.
3. Experiment with var s Shape = (*Rect)(nil) and compare to var s Shape.

Write down one sentence explaining *why* the output matches the code before you move on.
Time-box the lab to 15–25 minutes; struggle is part of encoding the skill.

## Curriculum notes (expanded from the compact draft)

## Interfaces are implicit

In Go you do **not** write `implements`. If a type has the methods, it satisfies the interface.

```go
type Stringer interface {
    String() string
}

type User struct{ Name string }
func (u User) String() string { return u.Name }
```

## Small interfaces win

`io.Reader`, `io.Writer`, `fmt.Stringer` — one or two methods.
Write functions that take interfaces so callers can plug mocks, buffers, or network streams.

```go
func CountLines(r io.Reader) (int, error) { /* ... */ }
```

## Composition over inheritance

Go has no class hierarchy. Embed structs and combine interfaces instead.

```go
type ReadWriter interface {
    io.Reader
    io.Writer
}
```

## `any` (empty interface)

`any` is `interface{}` — every type satisfies it. Useful for containers before generics;
prefer generics when you know the type set.

## Failure modes to watch while coding

- Defining huge interfaces that no one can mock
- Returning interfaces from constructors unnecessarily
- Using `any` everywhere instead of real types

When a test fails, ask which failure mode you hit before changing code at random.

## Idioms vs Python pitfalls

- Python structural typing is runtime; Go checks method sets at compile time.
- No ABC required — interfaces are satisfied implicitly.
- Fat interfaces are hard to mock; keep them tiny like io.Reader.

When you catch yourself reaching for a Python habit, pause and rewrite the Go way
once on purpose — even if both would "work". The goal is a Go-shaped intuition.

## Going deeper

Standard library design: functions take io.Reader not *os.File. Copy that style in your APIs.

## Practice checklist

Before the exercise, confirm you can:

1. Explain "Interfaces and Composition" aloud in under two minutes without notes.
2. Re-type the worked example from memory and match the expected output.
3. Name the Go standard library packages touched by this lesson.
4. List one production bug this lesson's rules prevent.
5. Contrast the Go approach with the Python instinct listed above.
6. Write a three-line cheat sheet: one idiom, one pitfall, one command to remember.

If any item fails, re-run the mini-lab once more, then attempt the exercise tests.

## Transfer to production

Ask where this shows up outside toys: config loading, API handlers, data pipelines,
CI scripts, or on-call debugging. Write one concrete two-sentence scenario tying
the worked example to that scenario. Tomorrow, when you rewrite the exercise from
memory, check whether the code still fits that framing.
""",
            exercise_guide="""
Implement Rect.Area and TotalArea(shapes []Shape) float64 for the Shape interface.
""",
            exercise_examples="""
TotalArea([]Shape{Rect{2,3}, Rect{1,1}}) → 7. `go test`.
""",
        ),
        10: dict(
            body="""
## Why this matters

Wrapped errors preserve context for humans and machines. errors.Is/As let callers branch on meaning without string matching.

This lesson is a building block for later modules in the Goodway path. If you only
skim, the exercises will feel like busywork; if you type the examples and narrate
them aloud, the same patterns will reappear in HTTP handlers, concurrency, and AI
service glue.

## Core concepts

- `fmt.Errorf("...: %w", err)` wraps while keeping the chain.
- `errors.Is` finds sentinels in the chain; `errors.As` finds typed errors.
- Sentinel vars (ErrNotFound) are stable public contracts.
- Log at the edge; return errors from libraries without double-logging.
- Error strings should be lowercase and not punctuated like sentences (style).

Hold these in working memory while you code. Each bullet should map to something
you can demonstrate with a three-line program or a failing compile error.

## Worked Go examples

Create a scratch module and type this yourself (do not paste blindly):

```bash
mkdir -p /tmp/gw-errors && cd /tmp/gw-errors
go mod init example.com/scratch
```

Then create `main.go`:

```go
package main

import (
    "errors"
    "fmt"
)

var ErrNotFound = errors.New("not found")

func load(id string) error {
    return fmt.Errorf("load %s: %w", id, ErrNotFound)
}

func main() {
    err := load("42")
    fmt.Println(err)
    fmt.Println(errors.Is(err, ErrNotFound))
}
```

Run it:

```bash
go run .
```

Expected output:

```text
load 42: not found
true
```

If your output differs, diff character-by-character — especially whitespace and
types. Then change one line deliberately and predict the new output before running.

## Mini-lab (`go run` steps)

1. Wrap ErrNotFound and assert with errors.Is.
2. Define a typed ValidationError and retrieve it with errors.As.
3. Compare wrongly with err.Error()== and then fix to Is/As.

Write down one sentence explaining *why* the output matches the code before you move on.
Time-box the lab to 15–25 minutes; struggle is part of encoding the skill.

## Curriculum notes (expanded from the compact draft)

## Wrapping

```go
if err != nil {
    return fmt.Errorf("load config %s: %w", path, err)
}
```

`%w` preserves the chain for `errors.Is` / `errors.As`.

## Sentinel errors

```go
var ErrNotFound = errors.New("not found")
```

Good for stable, package-level conditions. Do not compare error strings.

## Typed errors

```go
type ValidationError struct{ Field string }
func (e *ValidationError) Error() string { return e.Field + " invalid" }

var ve *ValidationError
if errors.As(err, &ve) { /* ... */ }
```

## Guideline

Return errors; log at the edge (main/handler). Avoid logging and returning the same error repeatedly.

## Failure modes to watch while coding

- Comparing `err.Error() == "..."`
- Using `%v` instead of `%w` when wrapping
- Creating unique error strings instead of sentinels

When a test fails, ask which failure mode you hit before changing code at random.

## Idioms vs Python pitfalls

- Python exception types vs Go error values + wrapping.
- Do not parse error strings — use Is/As.
- `raise from` ≈ `%w` wrapping, but Go keeps it a value.

When you catch yourself reaching for a Python habit, pause and rewrite the Go way
once on purpose — even if both would "work". The goal is a Go-shaped intuition.

## Going deeper

When wrapping, put the verb and resource first: `open config: %w` helps grepping logs.

## Practice checklist

Before the exercise, confirm you can:

1. Explain "Errors Deeply: Wrap, Is, As" aloud in under two minutes without notes.
2. Re-type the worked example from memory and match the expected output.
3. Name the Go standard library packages touched by this lesson.
4. List one production bug this lesson's rules prevent.
5. Contrast the Go approach with the Python instinct listed above.
6. Write a three-line cheat sheet: one idiom, one pitfall, one command to remember.

If any item fails, re-run the mini-lab once more, then attempt the exercise tests.

## Transfer to production

Ask where this shows up outside toys: config loading, API handlers, data pipelines,
CI scripts, or on-call debugging. Write one concrete two-sentence scenario tying
the worked example to that scenario. Tomorrow, when you rewrite the exercise from
memory, check whether the code still fits that framing.
""",
            exercise_guide="""
Wrap errors with %w and detect sentinels via errors.Is in the exercise stubs.
""",
            exercise_examples="""
Wrapped ErrNotFound must satisfy errors.Is(err, ErrNotFound) == true.
""",
        ),
        11: dict(
            body="""
## Why this matters

Generics remove `any` casts for containers and algorithms while keeping type safety. Used well, they clarify APIs; used poorly, they obscure them.

This lesson is a building block for later modules in the Goodway path. If you only
skim, the exercises will feel like busywork; if you type the examples and narrate
them aloud, the same patterns will reappear in HTTP handlers, concurrency, and AI
service glue.

## Core concepts

- Type parameters appear in `[T constraints]` on funcs and types.
- `comparable` enables == and map keys.
- Approximation elements `~int` include defined types based on int.
- Prefer interfaces when behavior is method-based; generics for structure.
- Inference often fills type args — specify when the compiler cannot.

Hold these in working memory while you code. Each bullet should map to something
you can demonstrate with a three-line program or a failing compile error.

## Worked Go examples

Create a scratch module and type this yourself (do not paste blindly):

```bash
mkdir -p /tmp/gw-generics: && cd /tmp/gw-generics:
go mod init example.com/scratch
```

Then create `main.go`:

```go
package main

import "fmt"

func Map[A, B any](xs []A, f func(A) B) []B {
    out := make([]B, len(xs))
    for i, v := range xs {
        out[i] = f(v)
    }
    return out
}

func main() {
    fmt.Println(Map([]int{1, 2, 3}, func(x int) int { return x * 2 }))
}
```

Run it:

```bash
go run .
```

Expected output:

```text
[2 4 6]
```

If your output differs, diff character-by-character — especially whitespace and
types. Then change one line deliberately and predict the new output before running.

## Mini-lab (`go run` steps)

1. Write generic Keys[K comparable, V any].
2. Write Sum with a Number constraint union.
3. Replace an `any` + type assert helper with a generic.

Write down one sentence explaining *why* the output matches the code before you move on.
Time-box the lab to 15–25 minutes; struggle is part of encoding the skill.

## Curriculum notes (expanded from the compact draft)

## Type parameters

```go
func Keys[K comparable, V any](m map[K]V) []K {
    out := make([]K, 0, len(m))
    for k := range m {
        out = append(out, k)
    }
    return out
}
```

## Constraints

```go
type Number interface {
    ~int | ~int64 | ~float64
}

func Sum[T Number](xs []T) T {
    var s T
    for _, v := range xs {
        s += v
    }
    return s
}
```

`comparable` is required for map keys and `==`.

## When not to use generics

If a small interface expresses the behavior better, prefer interfaces.
Generics shine for containers, algorithms, and removing `any` casts.

## Failure modes to watch while coding

- Genericizing every function "just in case"
- Forgetting `comparable` for map keys
- Fighting the type checker instead of simplifying the API

When a test fails, ask which failure mode you hit before changing code at random.

## Idioms vs Python pitfalls

- Python typing generics are optional; Go generics are enforced.
- No *args magic — constraints declare what operations exist.
- Don't genericize every function; concrete types stay readable.

When you catch yourself reaching for a Python habit, pause and rewrite the Go way
once on purpose — even if both would "work". The goal is a Go-shaped intuition.

## Going deeper

The standard library uses generics in slices, maps helpers — read those packages as style guides.

## Practice checklist

Before the exercise, confirm you can:

1. Explain "Generics: Type Parameters and Constraints" aloud in under two minutes without notes.
2. Re-type the worked example from memory and match the expected output.
3. Name the Go standard library packages touched by this lesson.
4. List one production bug this lesson's rules prevent.
5. Contrast the Go approach with the Python instinct listed above.
6. Write a three-line cheat sheet: one idiom, one pitfall, one command to remember.

If any item fails, re-run the mini-lab once more, then attempt the exercise tests.

## Transfer to production

Ask where this shows up outside toys: config loading, API handlers, data pipelines,
CI scripts, or on-call debugging. Write one concrete two-sentence scenario tying
the worked example to that scenario. Tomorrow, when you rewrite the exercise from
memory, check whether the code still fits that framing.
""",
            exercise_guide="""
Implement a generic Map (or Keys) as specified by the exercise tests.
""",
            exercise_examples="""
Map ints→doubled ints; type parameters inferred from arguments.
""",
        ),
        12: dict(
            body="""
## Why this matters

Tests are executable specs. Table-driven tests, fuzzing, and benchmarks turn Go's fast compiler into a design tool.

This lesson is a building block for later modules in the Goodway path. If you only
skim, the exercises will feel like busywork; if you type the examples and narrate
them aloud, the same patterns will reappear in HTTP handlers, concurrency, and AI
service glue.

## Core concepts

- Table tests + t.Run give clear failure names.
- Fuzzing feeds random inputs to find edge cases.
- Benchmarks use b.N; compare with -benchmem.
- Test files are `_test.go`; external packages test public API.
- Prefer behavior assertions over mocking every collaborator.

Hold these in working memory while you code. Each bullet should map to something
you can demonstrate with a three-line program or a failing compile error.

## Worked Go examples

Create a scratch module and type this yourself (do not paste blindly):

```bash
mkdir -p /tmp/gw-testing, && cd /tmp/gw-testing,
go mod init example.com/scratch
```

Then create `main.go`:

```go
package clamp

import "testing"

func Clamp(v, lo, hi int) int {
    if v < lo {
        return lo
    }
    if v > hi {
        return hi
    }
    return v
}

func TestClamp(t *testing.T) {
    tests := []struct{ name string; v, lo, hi, want int }{
        {"mid", 5, 0, 10, 5},
        {"low", -1, 0, 10, 0},
    }
    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            if got := Clamp(tt.v, tt.lo, tt.hi); got != tt.want {
                t.Fatalf("got %d want %d", got, tt.want)
            }
        })
    }
}
```

Run it:

```bash
go run .
```

Expected output:

```text
PASS (go test)
```

If your output differs, diff character-by-character — especially whitespace and
types. Then change one line deliberately and predict the new output before running.

## Mini-lab (`go run` steps)

1. Convert a single assertion test into a table.
2. Add a fuzz target for a pure function.
3. Run `go test -bench=. -benchmem` on a tiny Sum.

Write down one sentence explaining *why* the output matches the code before you move on.
Time-box the lab to 15–25 minutes; struggle is part of encoding the skill.

## Curriculum notes (expanded from the compact draft)

## Table-driven tests

```go
func TestClamp(t *testing.T) {
    tests := []struct{
        name string
        v, lo, hi, want int
    }{
        {"mid", 5, 0, 10, 5},
        {"low", -1, 0, 10, 0},
    }
    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            if got := Clamp(tt.v, tt.lo, tt.hi); got != tt.want {
                t.Fatalf("got %d want %d", got, tt.want)
            }
        })
    }
}
```

## Fuzzing

```go
func FuzzReverse(f *testing.F) {
    f.Add("go")
    f.Fuzz(func(t *testing.T, s string) {
        // property: reverse(reverse(s)) == s for runes...
    })
}
```

## Benchmarks

```go
func BenchmarkSum(b *testing.B) {
    xs := make([]int, 1000)
    for i := 0; i < b.N; i++ {
        Sum(xs)
    }
}
```

Run: `go test -bench=. -benchmem ./...`

## Failure modes to watch while coding

- Giant tests without cases (hard to see failures)
- Testing implementation details instead of behavior
- Ignoring flaky time/network tests — inject clocks and interfaces

When a test fails, ask which failure mode you hit before changing code at random.

## Idioms vs Python pitfalls

- pytest fixtures ≈ careful constructor helpers — keep tests plain.
- No assert statement — use t.Fatalf / testify if your team allows.
- Time/network flakiness: inject clocks and interfaces like in Go.

When you catch yourself reaching for a Python habit, pause and rewrite the Go way
once on purpose — even if both would "work". The goal is a Go-shaped intuition.

## Going deeper

A failing test name should tell you the behavior broken without reading the body.

## Practice checklist

Before the exercise, confirm you can:

1. Explain "Testing, Table Tests, Fuzz, and Benchmarks" aloud in under two minutes without notes.
2. Re-type the worked example from memory and match the expected output.
3. Name the Go standard library packages touched by this lesson.
4. List one production bug this lesson's rules prevent.
5. Contrast the Go approach with the Python instinct listed above.
6. Write a three-line cheat sheet: one idiom, one pitfall, one command to remember.

If any item fails, re-run the mini-lab once more, then attempt the exercise tests.

## Transfer to production

Ask where this shows up outside toys: config loading, API handlers, data pipelines,
CI scripts, or on-call debugging. Write one concrete two-sentence scenario tying
the worked example to that scenario. Tomorrow, when you rewrite the exercise from
memory, check whether the code still fits that framing.
""",
            exercise_guide="""
Make table-driven tests pass by implementing the stub under test.
""",
            exercise_examples="""
Each table row name appears in failures: `go test -v`.
""",
        ),
        13: dict(
            body="""
## Why this matters

io.Reader and io.Writer unify files, sockets, buffers, and compression. Streaming I/O is how Go services stay memory-bounded.

This lesson is a building block for later modules in the Goodway path. If you only
skim, the exercises will feel like busywork; if you type the examples and narrate
them aloud, the same patterns will reappear in HTTP handlers, concurrency, and AI
service glue.

## Core concepts

- Read/Write return (n, err); process n before assuming err.
- io.Copy moves bytes between Reader and Writer efficiently.
- bufio reduces syscalls for small reads/writes.
- io.EOF ends a stream — often expected, not fatal.
- defer Close() right after a successful Open.

Hold these in working memory while you code. Each bullet should map to something
you can demonstrate with a three-line program or a failing compile error.

## Worked Go examples

Create a scratch module and type this yourself (do not paste blindly):

```bash
mkdir -p /tmp/gw-i/o: && cd /tmp/gw-i/o:
go mod init example.com/scratch
```

Then create `main.go`:

```go
package main

import (
    "fmt"
    "io"
    "strings"
)

func main() {
    r := strings.NewReader("hello\\nworld\\n")
    n, err := io.Copy(io.Discard, r)
    fmt.Println(n, err)
}
```

Run it:

```bash
go run .
```

Expected output:

```text
12 <nil>
```

If your output differs, diff character-by-character — especially whitespace and
types. Then change one line deliberately and predict the new output before running.

## Mini-lab (`go run` steps)

1. Count lines by scanning an io.Reader.
2. Wrap a reader with bufio.Scanner.
3. Use io.LimitReader to cap bytes read.

Write down one sentence explaining *why* the output matches the code before you move on.
Time-box the lab to 15–25 minutes; struggle is part of encoding the skill.

## Curriculum notes (expanded from the compact draft)

## The io contracts

```go
type Reader interface { Read(p []byte) (n int, err error) }
type Writer interface { Write(p []byte) (n int, err error) }
```

Almost all I/O in Go is streaming through these interfaces — files, sockets, buffers, compression.

```go
f, err := os.Open(path)
if err != nil { return err }
defer f.Close()
return io.Copy(dst, f)
```

## bufio

Wrap expensive readers/writers with buffering for small reads/writes.

## Errors

`io.EOF` signals end of stream — often expected, not always a hard failure.
`io.ErrUnexpectedEOF` means truncated data.

## Failure modes to watch while coding

- Loading multi-GB files into memory with os.ReadFile without need
- Forgetting defer Close
- Ignoring partial Write/Read return values

When a test fails, ask which failure mode you hit before changing code at random.

## Idioms vs Python pitfalls

- Python file objects ≈ Readers/Writers but Go interfaces compose more uniformly.
- Prefer streaming over `read().split` for large inputs.
- `with open` ≈ Open + defer Close (check Close errors when it matters).

When you catch yourself reaching for a Python habit, pause and rewrite the Go way
once on purpose — even if both would "work". The goal is a Go-shaped intuition.

## Going deeper

Never ignore the n from Read when err != nil — partial data is common.

## Practice checklist

Before the exercise, confirm you can:

1. Explain "I/O: io, Files, Readers and Writers" aloud in under two minutes without notes.
2. Re-type the worked example from memory and match the expected output.
3. Name the Go standard library packages touched by this lesson.
4. List one production bug this lesson's rules prevent.
5. Contrast the Go approach with the Python instinct listed above.
6. Write a three-line cheat sheet: one idiom, one pitfall, one command to remember.

If any item fails, re-run the mini-lab once more, then attempt the exercise tests.

## Transfer to production

Ask where this shows up outside toys: config loading, API handlers, data pipelines,
CI scripts, or on-call debugging. Write one concrete two-sentence scenario tying
the worked example to that scenario. Tomorrow, when you rewrite the exercise from
memory, check whether the code still fits that framing.
""",
            exercise_guide="""
Implement the reader-counting stub using io.Reader, not []byte whole-file assumptions.
""",
            exercise_examples="""
Counting lines/bytes from a strings.Reader should match tests.
""",
        ),
        14: dict(
            body="""
## Why this matters

JSON and time are the lingua franca of services. Struct tags and time.Time correctness prevent subtle production outages.

This lesson is a building block for later modules in the Goodway path. If you only
skim, the exercises will feel like busywork; if you type the examples and narrate
them aloud, the same patterns will reappear in HTTP handlers, concurrency, and AI
service glue.

## Core concepts

- encoding/json uses struct tags (`json:"name"`).
- Unknown fields are ignored by default; unknown types error.
- time.Time marshals as RFC3339 by default.
- Always store and compare times in UTC unless UI demands local.
- Use json.NewDecoder for streams; Marshal for small values.

Hold these in working memory while you code. Each bullet should map to something
you can demonstrate with a three-line program or a failing compile error.

## Worked Go examples

Create a scratch module and type this yourself (do not paste blindly):

```bash
mkdir -p /tmp/gw-json, && cd /tmp/gw-json,
go mod init example.com/scratch
```

Then create `main.go`:

```go
package main

import (
    "encoding/json"
    "fmt"
)

type User struct {
    Name string `json:"name"`
    Age  int    `json:"age"`
}

func main() {
    b, _ := json.Marshal(User{Name: "Ada", Age: 36})
    fmt.Println(string(b))
    var u User
    _ = json.Unmarshal(b, &u)
    fmt.Println(u)
}
```

Run it:

```bash
go run .
```

Expected output:

```text
{"name":"Ada","age":36}
{Ada 36}
```

If your output differs, diff character-by-character — especially whitespace and
types. Then change one line deliberately and predict the new output before running.

## Mini-lab (`go run` steps)

1. Round-trip a struct with tags.
2. Omit empty fields with `omitempty`.
3. Parse a timestamp with time.Parse(time.RFC3339, ...).

Write down one sentence explaining *why* the output matches the code before you move on.
Time-box the lab to 15–25 minutes; struggle is part of encoding the skill.

## Curriculum notes (expanded from the compact draft)

## JSON

```go
type Event struct {
    ID   string    `json:"id"`
    At   time.Time `json:"at"`
    Name string    `json:"name,omitempty"`
}

b, err := json.Marshal(ev)
err = json.Unmarshal(b, &ev)
```

Use `Decoder` for streams; `Unmarshal` for whole buffers.

## Time

```go
now := time.Now().UTC()
t, err := time.Parse(time.RFC3339, s)
```

Store UTC; convert for display. Durations use `time.Duration` (nanoseconds under the hood).

## Encoding discipline

Be explicit about omitempty, pointers for null vs empty, and custom MarshalJSON only when needed.

## Failure modes to watch while coding

- Parsing local times without timezone
- Using float64 for currency in JSON
- Silent ignore of unknown fields in security-sensitive configs

When a test fails, ask which failure mode you hit before changing code at random.

## Idioms vs Python pitfalls

- dict/json vs struct tags — unknown fields won't appear as attributes.
- datetime timezone naivety is worse in Python; still be careful in Go.
- snake_case JSON ↔ CamelCase Go fields via tags.

When you catch yourself reaching for a Python habit, pause and rewrite the Go way
once on purpose — even if both would "work". The goal is a Go-shaped intuition.

## Going deeper

Validate after unmarshal — zero values can mean missing JSON fields.

## Practice checklist

Before the exercise, confirm you can:

1. Explain "JSON, Encoding, and Time" aloud in under two minutes without notes.
2. Re-type the worked example from memory and match the expected output.
3. Name the Go standard library packages touched by this lesson.
4. List one production bug this lesson's rules prevent.
5. Contrast the Go approach with the Python instinct listed above.
6. Write a three-line cheat sheet: one idiom, one pitfall, one command to remember.

If any item fails, re-run the mini-lab once more, then attempt the exercise tests.

## Transfer to production

Ask where this shows up outside toys: config loading, API handlers, data pipelines,
CI scripts, or on-call debugging. Write one concrete two-sentence scenario tying
the worked example to that scenario. Tomorrow, when you rewrite the exercise from
memory, check whether the code still fits that framing.
""",
            exercise_guide="""
Implement JSON round-trip helpers to satisfy the exercise tests.
""",
            exercise_examples="""
Marshal then Unmarshal must preserve fields the tests check.
""",
        ),
        15: dict(
            body="""
## Why this matters

context.Context carries deadlines and cancellation across API boundaries. It is how Go services stop work when clients disconnect.

This lesson is a building block for later modules in the Goodway path. If you only
skim, the exercises will feel like busywork; if you type the examples and narrate
them aloud, the same patterns will reappear in HTTP handlers, concurrency, and AI
service glue.

## Core concepts

- Pass Context as the first parameter: `ctx context.Context`.
- WithCancel / WithTimeout / WithDeadline derive child contexts.
- Listen on ctx.Done(); return ctx.Err() when cancelled.
- Never store Context inside a struct long-term unless carefully justified.
- Values in context are for request-scoped data, not optional parameters.

Hold these in working memory while you code. Each bullet should map to something
you can demonstrate with a three-line program or a failing compile error.

## Worked Go examples

Create a scratch module and type this yourself (do not paste blindly):

```bash
mkdir -p /tmp/gw-context: && cd /tmp/gw-context:
go mod init example.com/scratch
```

Then create `main.go`:

```go
package main

import (
    "context"
    "fmt"
    "time"
)

func main() {
    ctx, cancel := context.WithTimeout(context.Background(), 50*time.Millisecond)
    defer cancel()
    select {
    case <-time.After(200 * time.Millisecond):
        fmt.Println("work finished")
    case <-ctx.Done():
        fmt.Println(ctx.Err())
    }
}
```

Run it:

```bash
go run .
```

Expected output:

```text
context deadline exceeded
```

If your output differs, diff character-by-character — especially whitespace and
types. Then change one line deliberately and predict the new output before running.

## Mini-lab (`go run` steps)

1. Create a WithTimeout and select on Done.
2. Propagate ctx into a helper that sleeps and aborts early.
3. Call cancel as soon as the parent no longer needs work.

Write down one sentence explaining *why* the output matches the code before you move on.
Time-box the lab to 15–25 minutes; struggle is part of encoding the skill.

## Curriculum notes (expanded from the compact draft)

## Why context?

Distributed and concurrent programs need a signal: "stop working, the caller left".

```go
ctx, cancel := context.WithTimeout(parent, 2*time.Second)
defer cancel()

select {
case <-ctx.Done():
    return ctx.Err()
case res := <-results:
    return res, nil
}
```

## Rules of thumb

1. `ctx` is the first argument to functions that do I/O or wait.
2. Call `cancel` to free resources (use defer).
3. Do not pass `nil` context — use `context.Background()` or `TODO()` at edges.
4. Values in context are for request-scoped data (trace IDs), not optional parameters.

Cancellation is cooperative: your code must check `ctx.Done()` or call APIs that do.

## Failure modes to watch while coding

- Starting goroutines without tying them to ctx
- Using context for mandatory function parameters
- Forgetting defer cancel()

When a test fails, ask which failure mode you hit before changing code at random.

## Idioms vs Python pitfalls

- No direct Python stdlib equivalent as pervasive as Context.
- Timeouts on requests should flow down — same idea as ctx.
- Avoid context.Value for required params — use arguments.

When you catch yourself reaching for a Python habit, pause and rewrite the Go way
once on purpose — even if both would "work". The goal is a Go-shaped intuition.

## Going deeper

When a handler returns, cancel outstanding downstream calls so goroutines do not leak.

## Practice checklist

Before the exercise, confirm you can:

1. Explain "Context: Cancellation and Deadlines" aloud in under two minutes without notes.
2. Re-type the worked example from memory and match the expected output.
3. Name the Go standard library packages touched by this lesson.
4. List one production bug this lesson's rules prevent.
5. Contrast the Go approach with the Python instinct listed above.
6. Write a three-line cheat sheet: one idiom, one pitfall, one command to remember.

If any item fails, re-run the mini-lab once more, then attempt the exercise tests.

## Transfer to production

Ask where this shows up outside toys: config loading, API handlers, data pipelines,
CI scripts, or on-call debugging. Write one concrete two-sentence scenario tying
the worked example to that scenario. Tomorrow, when you rewrite the exercise from
memory, check whether the code still fits that framing.
""",
            exercise_guide="""
Honor context cancellation/deadlines in the exercise function.
""",
            exercise_examples="""
When ctx times out, return ctx.Err() rather than hanging.
""",
        ),
        16: dict(
            body="""
## Why this matters

Reflection powers encoding/json and some frameworks — but it is slow and bypasses the type checker. Know it to read libraries; avoid it in app code.

This lesson is a building block for later modules in the Goodway path. If you only
skim, the exercises will feel like busywork; if you type the examples and narrate
them aloud, the same patterns will reappear in HTTP handlers, concurrency, and AI
service glue.

## Core concepts

- reflect.TypeOf / ValueOf inspect values at runtime.
- Kind distinguishes struct, slice, pointer, etc.
- Settable values require addressability rules.
- Prefer codegen or generics over reflective maps of fields.
- Interfaces + codegen usually beat reflect for performance.

Hold these in working memory while you code. Each bullet should map to something
you can demonstrate with a three-line program or a failing compile error.

## Worked Go examples

Create a scratch module and type this yourself (do not paste blindly):

```bash
mkdir -p /tmp/gw-reflection && cd /tmp/gw-reflection
go mod init example.com/scratch
```

Then create `main.go`:

```go
package main

import (
    "fmt"
    "reflect"
)

func main() {
    var x any = 42
    v := reflect.ValueOf(x)
    fmt.Println(v.Kind(), v.Int())
}
```

Run it:

```bash
go run .
```

Expected output:

```text
int 42
```

If your output differs, diff character-by-character — especially whitespace and
types. Then change one line deliberately and predict the new output before running.

## Mini-lab (`go run` steps)

1. Print Kind of several values including a struct.
2. Walk exported fields of a struct with reflect.Type.
3. Rewrite a tiny reflective helper as a generic instead.

Write down one sentence explaining *why* the output matches the code before you move on.
Time-box the lab to 15–25 minutes; struggle is part of encoding the skill.

## Curriculum notes (expanded from the compact draft)

## What reflection does

The `reflect` package inspects types and values at runtime — powerful and easy to abuse.

```go
func KindOf(v any) string {
    return reflect.TypeOf(v).Kind().String()
}
```

`encoding/json` uses reflection to map structs to JSON. That convenience costs CPU and clarity.

## Prefer

- Generics for type-safe containers
- Interfaces for behavior
- `go generate` / codegen for repetitive glue

Use reflection for marshaling, debugging tools, and DI frameworks — not business logic.

## Failure modes to watch while coding

- Building your whole domain model on map[string]any + reflect
- Ignoring panic risks from invalid reflect usage
- Premature "flexible" APIs that erase types

When a test fails, ask which failure mode you hit before changing code at random.

## Idioms vs Python pitfalls

- getattr/hasattr are common in Python; in Go they are a smell for app code.
- Duck typing at runtime ≈ interface{} + reflect — prefer interfaces.
- Performance: reflect is convenient and costly.

When you catch yourself reaching for a Python habit, pause and rewrite the Go way
once on purpose — even if both would "work". The goal is a Go-shaped intuition.

## Going deeper

If you need reflect, isolate it behind a small package with heavy tests.

## Practice checklist

Before the exercise, confirm you can:

1. Explain "Reflection Overview (and When Not to Use It)" aloud in under two minutes without notes.
2. Re-type the worked example from memory and match the expected output.
3. Name the Go standard library packages touched by this lesson.
4. List one production bug this lesson's rules prevent.
5. Contrast the Go approach with the Python instinct listed above.
6. Write a three-line cheat sheet: one idiom, one pitfall, one command to remember.

If any item fails, re-run the mini-lab once more, then attempt the exercise tests.

## Transfer to production

Ask where this shows up outside toys: config loading, API handlers, data pipelines,
CI scripts, or on-call debugging. Write one concrete two-sentence scenario tying
the worked example to that scenario. Tomorrow, when you rewrite the exercise from
memory, check whether the code still fits that framing.
""",
            exercise_guide="""
Use reflect.Kind (or the stub's required API) to classify values as tests demand.
""",
            exercise_examples="""
Classify ints vs structs correctly per test cases.
""",
        ),
        17: dict(
            body="""
## Why this matters

Idiomatic Go is a shared dialect: clarity, small interfaces, explicit errors. Teams move faster when style is predictable.

This lesson is a building block for later modules in the Goodway path. If you only
skim, the exercises will feel like busywork; if you type the examples and narrate
them aloud, the same patterns will reappear in HTTP handlers, concurrency, and AI
service glue.

## Core concepts

- Accept interfaces, return structs.
- Make the zero value useful when possible.
- Short names for short scopes; longer names for package-level.
- Handle errors once; don't log-and-return repeatedly.
- gofmt/goimports are non-negotiable — style is automated.

Hold these in working memory while you code. Each bullet should map to something
you can demonstrate with a three-line program or a failing compile error.

## Worked Go examples

Create a scratch module and type this yourself (do not paste blindly):

```bash
mkdir -p /tmp/gw-idiomatic && cd /tmp/gw-idiomatic
go mod init example.com/scratch
```

Then create `main.go`:

```go
package main

import (
    "fmt"
    "strconv"
)

func ParsePort(s string) (int, error) {
    n, err := strconv.Atoi(s)
    if err != nil {
        return 0, fmt.Errorf("parse port: %w", err)
    }
    if n < 1 || n > 65535 {
        return 0, fmt.Errorf("port %d out of range", n)
    }
    return n, nil
}

func main() {
    fmt.Println(ParsePort("8080"))
}
```

Run it:

```bash
go run .
```

Expected output:

```text
8080 <nil>
```

If your output differs, diff character-by-character — especially whitespace and
types. Then change one line deliberately and predict the new output before running.

## Mini-lab (`go run` steps)

1. Refactor a nested if pyramid into early returns.
2. Rename variables to Go-ish short forms inside a small func.
3. Run gofmt on a deliberately messy file.

Write down one sentence explaining *why* the output matches the code before you move on.
Time-box the lab to 15–25 minutes; struggle is part of encoding the skill.

## Curriculum notes (expanded from the compact draft)

## Names

- Packages: short, lowercase, no underscores (`http`, `json`)
- Interfaces: often `-er` (`Reader`) when one method
- Avoid stuttering: `http.Server` not `http.HTTPServer` in the package name sense

## Useful zero values

`var buf bytes.Buffer` works immediately. Design types so `var t T` is ready or clearly invalid.

## Return early

Flatten happy path; handle errors first. Avoid deep nesting.

## Don't communicate by sharing memory...

...share memory by communicating (channels) — but also learn mutexes (later). Idiomatic means choosing the right tool, not dogma.

## Failure modes to watch while coding

- Java-style getters for every field
- Huge package "utils" dumping grounds
- Interface pollution (exporting interfaces no one implements outside)

When a test fails, ask which failure mode you hit before changing code at random.

## Idioms vs Python pitfalls

- PEP8 vs gofmt — Go ends style debates with a tool.
- EAFP in Python vs explicit err checks in Go.
- Classes everywhere vs funcs + small structs.

When you catch yourself reaching for a Python habit, pause and rewrite the Go way
once on purpose — even if both would "work". The goal is a Go-shaped intuition.

## Going deeper

Read Effective Go and the Google Go Style Guide once; then practice by reviewing your own PRs.

## Practice checklist

Before the exercise, confirm you can:

1. Explain "Idiomatic Go: Effective Patterns" aloud in under two minutes without notes.
2. Re-type the worked example from memory and match the expected output.
3. Name the Go standard library packages touched by this lesson.
4. List one production bug this lesson's rules prevent.
5. Contrast the Go approach with the Python instinct listed above.
6. Write a three-line cheat sheet: one idiom, one pitfall, one command to remember.

If any item fails, re-run the mini-lab once more, then attempt the exercise tests.

## Transfer to production

Ask where this shows up outside toys: config loading, API handlers, data pipelines,
CI scripts, or on-call debugging. Write one concrete two-sentence scenario tying
the worked example to that scenario. Tomorrow, when you rewrite the exercise from
memory, check whether the code still fits that framing.
""",
            exercise_guide="""
Implement the idiomatic parse helper so tests pass with clear errors.
""",
            exercise_examples="""
Valid input returns value; invalid returns descriptive error.
""",
        ),
        18: dict(
            body="""
## Why this matters

Layout signals intent: library vs service, public API vs internal. Good structure reduces import cycles and onboarding time.

This lesson is a building block for later modules in the Goodway path. If you only
skim, the exercises will feel like busywork; if you type the examples and narrate
them aloud, the same patterns will reappear in HTTP handlers, concurrency, and AI
service glue.

## Core concepts

- `cmd/` for mains, `internal/` for private packages, root for public libs.
- Avoid `pkg/` unless your org standardizes on it.
- Keep modules cohesive; split when versioning demands.
- One module per repo is common; multi-module is advanced.
- Configs and migrations live near the service that owns them.

Hold these in working memory while you code. Each bullet should map to something
you can demonstrate with a three-line program or a failing compile error.

## Worked Go examples

Create a scratch module and type this yourself (do not paste blindly):

```bash
mkdir -p /tmp/gw-project && cd /tmp/gw-project
go mod init example.com/scratch
```

Then create `main.go`:

```go
package main

import "fmt"

// Example layout commentary printed as a checklist.
func main() {
    layout := []string{"cmd/api", "internal/auth", "internal/store", "go.mod"}
    for _, p := range layout {
        fmt.Println(p)
    }
}
```

Run it:

```bash
go run .
```

Expected output:

```text
cmd/api
internal/auth
internal/store
go.mod
```

If your output differs, diff character-by-character — especially whitespace and
types. Then change one line deliberately and predict the new output before running.

## Mini-lab (`go run` steps)

1. Sketch folders for a tiny HTTP API.
2. Move a helper under internal/ and import it from cmd.
3. Try importing internal from a sibling module — observe failure.

Write down one sentence explaining *why* the output matches the code before you move on.
Time-box the lab to 15–25 minutes; struggle is part of encoding the skill.

## Curriculum notes (expanded from the compact draft)

## Common service layout

```
cmd/api/main.go      # wiring only
internal/server/     # private app code
internal/store/
go.mod
```

## Libraries

Export a stable API from the module root or clear subpackages.
Semantic import versioning: `/v2` path for major version 2+.

## Guidelines

- `internal/` for code you do not want strangers to import
- Prefer fewer packages until boundaries hurt
- Config via env/flags at main; pure functions underneath for tests

## Failure modes to watch while coding

- Copying a giant layout template for a 200-line tool
- Business logic inside main.go
- Exporting everything from pkg/ without need

When a test fails, ask which failure mode you hit before changing code at random.

## Idioms vs Python pitfalls

- src-layout vs flat — Go favors module-root clarity.
- Django apps ≈ packages with clear boundaries.
- __init__.py noise does not exist; directories are packages with Go files.

When you catch yourself reaching for a Python habit, pause and rewrite the Go way
once on purpose — even if both would "work". The goal is a Go-shaped intuition.

## Going deeper

Start simple. Premature micro-packages create cycles. Split on domain seams you can name.

## Practice checklist

Before the exercise, confirm you can:

1. Explain "Project Layout: Libraries vs Services" aloud in under two minutes without notes.
2. Re-type the worked example from memory and match the expected output.
3. Name the Go standard library packages touched by this lesson.
4. List one production bug this lesson's rules prevent.
5. Contrast the Go approach with the Python instinct listed above.
6. Write a three-line cheat sheet: one idiom, one pitfall, one command to remember.

If any item fails, re-run the mini-lab once more, then attempt the exercise tests.

## Transfer to production

Ask where this shows up outside toys: config loading, API handlers, data pipelines,
CI scripts, or on-call debugging. Write one concrete two-sentence scenario tying
the worked example to that scenario. Tomorrow, when you rewrite the exercise from
memory, check whether the code still fits that framing.
""",
            exercise_guide="""
Answer layout quiz stubs / implement the tiny helper the exercise expects.
""",
            exercise_examples="""
Follow test expectations for package paths and exported names.
""",
        ),
        19: dict(
            body="""
## Why this matters

Guessing at performance wastes time. pprof, the race detector, and a simple mental model of allocations keep optimizations honest.

This lesson is a building block for later modules in the Goodway path. If you only
skim, the exercises will feel like busywork; if you type the examples and narrate
them aloud, the same patterns will reappear in HTTP handlers, concurrency, and AI
service glue.

## Core concepts

- `go test -race` finds data races.
- pprof profiles CPU, heap, goroutines, blockers.
- Avoid premature optimization; measure first.
- Allocations and interface/boxed conversions show up in profiles.
- Benchmark before and after with `go test -bench`.

Hold these in working memory while you code. Each bullet should map to something
you can demonstrate with a three-line program or a failing compile error.

## Worked Go examples

Create a scratch module and type this yourself (do not paste blindly):

```bash
mkdir -p /tmp/gw-profiling, && cd /tmp/gw-profiling,
go mod init example.com/scratch
```

Then create `main.go`:

```go
package main

import "fmt"

func Sum(xs []int) int {
    s := 0
    for _, v := range xs {
        s += v
    }
    return s
}

func main() {
    xs := make([]int, 1000)
    for i := range xs {
        xs[i] = i
    }
    fmt.Println(Sum(xs))
}
```

Run it:

```bash
go run .
```

Expected output:

```text
499500
```

If your output differs, diff character-by-character — especially whitespace and
types. Then change one line deliberately and predict the new output before running.

## Mini-lab (`go run` steps)

1. Write a BenchmarkSum and run -bench=.
2. Introduce a deliberate race and catch it with -race.
3. Read `go tool pprof` help once (even if you only skim).

Write down one sentence explaining *why* the output matches the code before you move on.
Time-box the lab to 15–25 minutes; struggle is part of encoding the skill.

## Curriculum notes (expanded from the compact draft)

## Race detector

```bash
go test -race ./...
```

Detects concurrent reads/writes without synchronization. **Use it in CI.**

## pprof

```bash
go test -bench=. -cpuprofile=cpu.out
go tool pprof cpu.out
```

Or expose `/debug/pprof` on a debug port in services (carefully locked down).

## Mental model

1. Correctness first
2. Measure
3. Fix algorithmic issues before micro-opts
4. Reduce allocations in hot loops (preallocate slices, avoid string concat in loops)

Escape analysis decides heap vs stack; pointers and interfaces often force heap allocation.

## Failure modes to watch while coding

- Optimizing without benchmarks
- Disabling race detector because "it's slow" in CI forever
- Caching everything without eviction strategy

When a test fails, ask which failure mode you hit before changing code at random.

## Idioms vs Python pitfalls

- cProfile ≈ pprof; Go's is tightly integrated with the runtime.
- GIL hides some races; Go encourages finding them with -race.
- Microbenchmarks lie without careful b.N loops — same in both languages.

When you catch yourself reaching for a Python habit, pause and rewrite the Go way
once on purpose — even if both would "work". The goal is a Go-shaped intuition.

## Going deeper

Fix algorithmic complexity before micro-caching. O(n^2) beats any pprof tweak.

## Practice checklist

Before the exercise, confirm you can:

1. Explain "Profiling, Race Detector, Performance Mental Model" aloud in under two minutes without notes.
2. Re-type the worked example from memory and match the expected output.
3. Name the Go standard library packages touched by this lesson.
4. List one production bug this lesson's rules prevent.
5. Contrast the Go approach with the Python instinct listed above.
6. Write a three-line cheat sheet: one idiom, one pitfall, one command to remember.

If any item fails, re-run the mini-lab once more, then attempt the exercise tests.

## Transfer to production

Ask where this shows up outside toys: config loading, API handlers, data pipelines,
CI scripts, or on-call debugging. Write one concrete two-sentence scenario tying
the worked example to that scenario. Tomorrow, when you rewrite the exercise from
memory, check whether the code still fits that framing.
""",
            exercise_guide="""
Implement the sum/perf stub correctly; tests may check results more than timing.
""",
            exercise_examples="""
Correct Sum over a slice; then optionally benchmark locally.
""",
        ),
        20: dict(
            body="""
## Why this matters

Docs and semver are how libraries age gracefully. Go doc comments and module versions are part of the public API.

This lesson is a building block for later modules in the Goodway path. If you only
skim, the exercises will feel like busywork; if you type the examples and narrate
them aloud, the same patterns will reappear in HTTP handlers, concurrency, and AI
service glue.

## Core concepts

- Doc comments precede declarations and start with the name.
- `go doc` / pkg.go.dev render those comments.
- Semver: major for breaking changes; /v2+ in module paths.
- Compatibility guidelines: don't break callers casually.
- Examples in _test.go appear on pkg.go.dev.

Hold these in working memory while you code. Each bullet should map to something
you can demonstrate with a three-line program or a failing compile error.

## Worked Go examples

Create a scratch module and type this yourself (do not paste blindly):

```bash
mkdir -p /tmp/gw-documentatio && cd /tmp/gw-documentatio
go mod init example.com/scratch
```

Then create `main.go`:

```go
package greeter

// Hello returns a greeting for name.
// Empty name is allowed and produces "Hello, ".
func Hello(name string) string {
    return "Hello, " + name
}
```

Run it:

```bash
go run .
```

Expected output:

```text
go doc → documents Hello
```

If your output differs, diff character-by-character — especially whitespace and
types. Then change one line deliberately and predict the new output before running.

## Mini-lab (`go run` steps)

1. Add a doc comment and run `go doc`.
2. Write an ExampleHello test function.
3. Skim Go module versioning docs for /v2.

Write down one sentence explaining *why* the output matches the code before you move on.
Time-box the lab to 15–25 minutes; struggle is part of encoding the skill.

## Curriculum notes (expanded from the compact draft)

## Doc comments

```go
// Package store implements durable persistence for users.
package store

// Find returns a user by ID.
// It returns ErrNotFound if no user exists.
func Find(ctx context.Context, id string) (*User, error)
```

Start with the name of the symbol. Run `go doc` locally.

## Semver

- MAJOR: breaking changes (import path `/v2` for v2+)
- MINOR: compatible new features
- PATCH: bug fixes

## API design

- Accept interfaces, return structs (often)
- Keep exported surface small
- Prefer options structs over endless parameters

## Failure modes to watch while coding

- Breaking APIs without a major version
- Empty doc comments that restate the name only poorly
- Exporting types "for later"

When a test fails, ask which failure mode you hit before changing code at random.

## Idioms vs Python pitfalls

- docstrings vs Go doc comments — placement and tooling differ.
- CalVer vs SemVer — Go modules expect Semver.
- Type hints as docs ≠ compile-enforced API stability.

When you catch yourself reaching for a Python habit, pause and rewrite the Go way
once on purpose — even if both would "work". The goal is a Go-shaped intuition.

## Going deeper

Treat exported names as forever once tagged v1. Prefer additive changes.

## Practice checklist

Before the exercise, confirm you can:

1. Explain "Documentation, APIs, and Semantic Versioning" aloud in under two minutes without notes.
2. Re-type the worked example from memory and match the expected output.
3. Name the Go standard library packages touched by this lesson.
4. List one production bug this lesson's rules prevent.
5. Contrast the Go approach with the Python instinct listed above.
6. Write a three-line cheat sheet: one idiom, one pitfall, one command to remember.

If any item fails, re-run the mini-lab once more, then attempt the exercise tests.

## Transfer to production

Ask where this shows up outside toys: config loading, API handlers, data pipelines,
CI scripts, or on-call debugging. Write one concrete two-sentence scenario tying
the worked example to that scenario. Tomorrow, when you rewrite the exercise from
memory, check whether the code still fits that framing.
""",
            exercise_guide="""
Satisfy the docs/comment exercise — often about exporting and commenting correctly.
""",
            exercise_examples="""
Tests may check behavior of documented helpers.
""",
        ),
        21: dict(
            body="""
## Why this matters

Complexity literacy stops you from shipping accidental O(n^2) loops in hot paths. Recursion and Big-O are tools for designing algorithms in Go.

This lesson is a building block for later modules in the Goodway path. If you only
skim, the exercises will feel like busywork; if you type the examples and narrate
them aloud, the same patterns will reappear in HTTP handlers, concurrency, and AI
service glue.

## Core concepts

- Count dominant operations as n grows.
- Recursion needs base cases and progress toward them.
- Memoization trades memory for time.
- Prefer iterative forms when stack depth worries you.
- Measure with benchmarks when constants matter.

Hold these in working memory while you code. Each bullet should map to something
you can demonstrate with a three-line program or a failing compile error.

## Worked Go examples

Create a scratch module and type this yourself (do not paste blindly):

```bash
mkdir -p /tmp/gw-complexity, && cd /tmp/gw-complexity,
go mod init example.com/scratch
```

Then create `main.go`:

```go
package main

import "fmt"

func Fib(n int) int {
    if n < 2 {
        return n
    }
    a, b := 0, 1
    for i := 2; i <= n; i++ {
        a, b = b, a+b
    }
    return b
}

func main() { fmt.Println(Fib(10)) }
```

Run it:

```bash
go run .
```

Expected output:

```text
55
```

If your output differs, diff character-by-character — especially whitespace and
types. Then change one line deliberately and predict the new output before running.

## Mini-lab (`go run` steps)

1. Implement iterative Fib; compare to naive recursive for n=40 timing.
2. Estimate complexity of nested loops in a small snippet.
3. Rewrite recursion as an explicit stack.

Write down one sentence explaining *why* the output matches the code before you move on.
Time-box the lab to 15–25 minutes; struggle is part of encoding the skill.

## Curriculum notes (expanded from the compact draft)

## Big-O intuition

Big-O describes how runtime/memory grow as input size n grows.
Common classes: O(1), O(log n), O(n), O(n log n), O(n²), O(2ⁿ).

```go
// O(n)
func Sum(xs []int) int {
    s := 0
    for _, v := range xs { s += v }
    return s
}
```

Nested loops over the same n often mean O(n²). Sorting good algorithms are O(n log n).

## Recursion

```go
func Fib(n int) int {
    if n < 2 { return n }
    return Fib(n-1) + Fib(n-2) // exponential without memo
}
```

Always define base cases. Watch stack depth — Go stacks grow, but recursion depth still matters.

## Practice

For every algorithm you write: state expected complexity, then verify with benchmarks on growing n.

## Failure modes to watch while coding

- Calling naive Fib-like recursion in production
- Confusing average vs worst case
- Ignoring space complexity of maps/slices

When a test fails, ask which failure mode you hit before changing code at random.

## Idioms vs Python pitfalls

- Same Big-O ideas; Go's recursion depth limits still apply.
- list append amortizes like Go append.
- Prefer clarity first, then complexity improvements with tests.

When you catch yourself reaching for a Python habit, pause and rewrite the Go way
once on purpose — even if both would "work". The goal is a Go-shaped intuition.

## Going deeper

Interviewers care that you can discuss trade-offs while writing correct Go.

## Practice checklist

Before the exercise, confirm you can:

1. Explain "Complexity, Recursion, and Big-O Practice" aloud in under two minutes without notes.
2. Re-type the worked example from memory and match the expected output.
3. Name the Go standard library packages touched by this lesson.
4. List one production bug this lesson's rules prevent.
5. Contrast the Go approach with the Python instinct listed above.
6. Write a three-line cheat sheet: one idiom, one pitfall, one command to remember.

If any item fails, re-run the mini-lab once more, then attempt the exercise tests.

## Transfer to production

Ask where this shows up outside toys: config loading, API handlers, data pipelines,
CI scripts, or on-call debugging. Write one concrete two-sentence scenario tying
the worked example to that scenario. Tomorrow, when you rewrite the exercise from
memory, check whether the code still fits that framing.
""",
            exercise_guide="""
Implement Fib (or the drill's function) efficiently enough for tests.
""",
            exercise_examples="""
Fib(10)→55; large n must finish quickly if tests set limits.
""",
        ),
        22: dict(
            body="""
## Why this matters

Sorting and searching are building blocks for indexes, schedulers, and caches. Go's sort package and binary search repay fluency.

This lesson is a building block for later modules in the Goodway path. If you only
skim, the exercises will feel like busywork; if you type the examples and narrate
them aloud, the same patterns will reappear in HTTP handlers, concurrency, and AI
service glue.

## Core concepts

- sort.Ints / sort.Slice with less functions.
- Binary search needs sorted order — verify invariants.
- stable vs unstable sorts matter for tie-breaking.
- search returns index or insertion point patterns.
- Custom order via sort.Interface or Slice.

Hold these in working memory while you code. Each bullet should map to something
you can demonstrate with a three-line program or a failing compile error.

## Worked Go examples

Create a scratch module and type this yourself (do not paste blindly):

```bash
mkdir -p /tmp/gw-sorting && cd /tmp/gw-sorting
go mod init example.com/scratch
```

Then create `main.go`:

```go
package main

import (
    "fmt"
    "sort"
)

func main() {
    xs := []int{5, 1, 3}
    sort.Ints(xs)
    i := sort.SearchInts(xs, 3)
    fmt.Println(xs, i)
}
```

Run it:

```bash
go run .
```

Expected output:

```text
[1 3 5] 1
```

If your output differs, diff character-by-character — especially whitespace and
types. Then change one line deliberately and predict the new output before running.

## Mini-lab (`go run` steps)

1. Sort structs by a field with sort.Slice.
2. Binary search for a target; handle not-found.
3. Compare stable vs unstable with equal keys.

Write down one sentence explaining *why* the output matches the code before you move on.
Time-box the lab to 15–25 minutes; struggle is part of encoding the skill.

## Curriculum notes (expanded from the compact draft)

## sort package

```go
sort.Ints(xs)
sort.Slice(people, func(i, j int) bool { return people[i].Age < people[j].Age })
```

## Binary search

Requires sorted input. Classic bug: midpoint overflow (use `lo+(hi-lo)/2`).

```go
func Search(xs []int, target int) int {
    lo, hi := 0, len(xs)
    for lo < hi {
        mid := lo + (hi-lo)/2
        if xs[mid] < target { lo = mid + 1 } else { hi = mid }
    }
    if lo < len(xs) && xs[lo] == target { return lo }
    return -1
}
```

## Stability

`sort.SliceStable` preserves equal-element order — useful for multi-key sorts.

## Failure modes to watch while coding

- Binary search on unsorted data
- Inclusive vs exclusive bounds confusion
- Expensive comparisons in comparators

When a test fails, ask which failure mode you hit before changing code at random.

## Idioms vs Python pitfalls

- list.sort vs sorted; Go sorts in place commonly.
- bisect module ≈ sort.Search.
- key= functions ≈ less closures in sort.Slice.

When you catch yourself reaching for a Python habit, pause and rewrite the Go way
once on purpose — even if both would "work". The goal is a Go-shaped intuition.

## Going deeper

When data is huge, consider whether you need a full sort or a heap/selection.

## Practice checklist

Before the exercise, confirm you can:

1. Explain "Sorting and Searching" aloud in under two minutes without notes.
2. Re-type the worked example from memory and match the expected output.
3. Name the Go standard library packages touched by this lesson.
4. List one production bug this lesson's rules prevent.
5. Contrast the Go approach with the Python instinct listed above.
6. Write a three-line cheat sheet: one idiom, one pitfall, one command to remember.

If any item fails, re-run the mini-lab once more, then attempt the exercise tests.

## Transfer to production

Ask where this shows up outside toys: config loading, API handlers, data pipelines,
CI scripts, or on-call debugging. Write one concrete two-sentence scenario tying
the worked example to that scenario. Tomorrow, when you rewrite the exercise from
memory, check whether the code still fits that framing.
""",
            exercise_guide="""
Implement search/sort helpers to match exercise tests.
""",
            exercise_examples="""
Sorted inputs + Search return the expected index.
""",
        ),
        23: dict(
            body="""
## Why this matters

Linked structures, stacks, and queues appear in parsers, schedulers, and BFS. Implementing them in Go clarifies pointers and ownership.

This lesson is a building block for later modules in the Goodway path. If you only
skim, the exercises will feel like busywork; if you type the examples and narrate
them aloud, the same patterns will reappear in HTTP handlers, concurrency, and AI
service glue.

## Core concepts

- Nodes hold values and pointers to other nodes.
- Stacks: push/pop at one end; queues: FIFO.
- Nil terminates lists; always check before deref.
- Slices often beat linked lists for cache locality.
- Know both: interviews and specialized allocators still use links.

Hold these in working memory while you code. Each bullet should map to something
you can demonstrate with a three-line program or a failing compile error.

## Worked Go examples

Create a scratch module and type this yourself (do not paste blindly):

```bash
mkdir -p /tmp/gw-linked && cd /tmp/gw-linked
go mod init example.com/scratch
```

Then create `main.go`:

```go
package main

import "fmt"

type Stack []int

func (s *Stack) Push(v int) { *s = append(*s, v) }
func (s *Stack) Pop() int {
    v := (*s)[len(*s)-1]
    *s = (*s)[:len(*s)-1]
    return v
}

func main() {
    var s Stack
    s.Push(1); s.Push(2)
    fmt.Println(s.Pop(), s.Pop())
}
```

Run it:

```bash
go run .
```

Expected output:

```text
2 1
```

If your output differs, diff character-by-character — especially whitespace and
types. Then change one line deliberately and predict the new output before running.

## Mini-lab (`go run` steps)

1. Implement stack with a slice backing.
2. Implement a queue with head index or container/list.
3. Draw pointer boxes for a 3-node linked list.

Write down one sentence explaining *why* the output matches the code before you move on.
Time-box the lab to 15–25 minutes; struggle is part of encoding the skill.

## Curriculum notes (expanded from the compact draft)

## Stack (LIFO)

Slice-backed stacks are idiomatic and cache-friendly:

```go
type Stack []int
func (s *Stack) Push(v int) { *s = append(*s, v) }
func (s *Stack) Pop() (int, bool) {
    if len(*s) == 0 { return 0, false }
    v := (*s)[len(*s)-1]
    *s = (*s)[:len(*s)-1]
    return v, true
}
```

## Queue (FIFO)

Can use slice with head index, ring buffer, or two stacks. Avoid O(n) `dequeue` from front without strategy.

## Linked lists

Useful for O(1) splice given a node; often slower than slices due to pointer chasing. Prefer slices first.

## Failure modes to watch while coding

- Always reaching for linked lists from textbook habit
- Queue via slice[1:] in hot path causing GC pressure
- Forgetting empty checks on Pop

When a test fails, ask which failure mode you hit before changing code at random.

## Idioms vs Python pitfalls

- collections.deque ≈ efficient queue; Go slices work if careful.
- No pointers in Python — references everywhere.
- Linked lists are rarer in both languages for general storage.

When you catch yourself reaching for a Python habit, pause and rewrite the Go way
once on purpose — even if both would "work". The goal is a Go-shaped intuition.

## Going deeper

Prefer slice-based stacks/queues unless you need mid-list splicing.

## Practice checklist

Before the exercise, confirm you can:

1. Explain "Linked Structures, Stacks, and Queues" aloud in under two minutes without notes.
2. Re-type the worked example from memory and match the expected output.
3. Name the Go standard library packages touched by this lesson.
4. List one production bug this lesson's rules prevent.
5. Contrast the Go approach with the Python instinct listed above.
6. Write a three-line cheat sheet: one idiom, one pitfall, one command to remember.

If any item fails, re-run the mini-lab once more, then attempt the exercise tests.

## Transfer to production

Ask where this shows up outside toys: config loading, API handlers, data pipelines,
CI scripts, or on-call debugging. Write one concrete two-sentence scenario tying
the worked example to that scenario. Tomorrow, when you rewrite the exercise from
memory, check whether the code still fits that framing.
""",
            exercise_guide="""
Implement stack operations required by tests (push/pop/peek).
""",
            exercise_examples="""
LIFO order must hold across a sequence of ops.
""",
        ),
        24: dict(
            body="""
## Why this matters

Trees and heaps power priority queues, schedulers, and hierarchical configs. Binary heaps give cheap extract-min.

This lesson is a building block for later modules in the Goodway path. If you only
skim, the exercises will feel like busywork; if you type the examples and narrate
them aloud, the same patterns will reappear in HTTP handlers, concurrency, and AI
service glue.

## Core concepts

- Binary tree: left/right children; traverse inorder/preorder/postorder.
- Heap property: parent ≤ children (min-heap) or ≥ (max-heap).
- container/heap requires Push/Pop methods on a type.
- Priority queues schedule work by urgency.
- Balanced trees (overview) keep operations logarithmic.

Hold these in working memory while you code. Each bullet should map to something
you can demonstrate with a three-line program or a failing compile error.

## Worked Go examples

Create a scratch module and type this yourself (do not paste blindly):

```bash
mkdir -p /tmp/gw-trees, && cd /tmp/gw-trees,
go mod init example.com/scratch
```

Then create `main.go`:

```go
package main

import (
    "container/heap"
    "fmt"
)

type IntHeap []int

func (h IntHeap) Len() int            { return len(h) }
func (h IntHeap) Less(i, j int) bool  { return h[i] < h[j] }
func (h IntHeap) Swap(i, j int)       { h[i], h[j] = h[j], h[i] }
func (h *IntHeap) Push(x any)         { *h = append(*h, x.(int)) }
func (h *IntHeap) Pop() any {
    old := *h
    n := len(old)
    x := old[n-1]
    *h = old[:n-1]
    return x
}

func main() {
    h := &IntHeap{3, 1, 2}
    heap.Init(h)
    fmt.Println(heap.Pop(h))
}
```

Run it:

```bash
go run .
```

Expected output:

```text
1
```

If your output differs, diff character-by-character — especially whitespace and
types. Then change one line deliberately and predict the new output before running.

## Mini-lab (`go run` steps)

1. Init a min-heap and pop in order.
2. Implement a binary tree Insert for ints.
3. Traverse and collect values.

Write down one sentence explaining *why* the output matches the code before you move on.
Time-box the lab to 15–25 minutes; struggle is part of encoding the skill.

## Curriculum notes (expanded from the compact draft)

## Binary tree

```go
type Node struct {
    Val int
    Left, Right *Node
}
```

Traversals: inorder, preorder, postorder, level-order (BFS with queue).

## Heaps / priority queues

`container/heap` needs `Len`, `Less`, `Swap`, `Push`, `Pop`.

Heaps give O(log n) push/pop and O(1) peek — perfect for:
- scheduling jobs by priority
- Dijkstra's algorithm
- top-K queries

## BST intuition

Balanced BST: O(log n) search. Unbalanced (sorted inserts): O(n). Production often uses maps (hash) or specialized trees.

## Failure modes to watch while coding

- Assuming BST is always log n
- Incorrect Less making heap invalid
- Mutating heap slice outside heap functions

When a test fails, ask which failure mode you hit before changing code at random.

## Idioms vs Python pitfalls

- heapq ≈ container/heap with more ceremony in Go.
- dataclasses for nodes vs structs.
- Recursion for traversal is fine for shallow trees.

When you catch yourself reaching for a Python habit, pause and rewrite the Go way
once on purpose — even if both would "work". The goal is a Go-shaped intuition.

## Going deeper

For scheduling, store (priority, sequence, item) to keep ties deterministic.

## Practice checklist

Before the exercise, confirm you can:

1. Explain "Trees, Heaps, and Priority Queues" aloud in under two minutes without notes.
2. Re-type the worked example from memory and match the expected output.
3. Name the Go standard library packages touched by this lesson.
4. List one production bug this lesson's rules prevent.
5. Contrast the Go approach with the Python instinct listed above.
6. Write a three-line cheat sheet: one idiom, one pitfall, one command to remember.

If any item fails, re-run the mini-lab once more, then attempt the exercise tests.

## Transfer to production

Ask where this shows up outside toys: config loading, API handlers, data pipelines,
CI scripts, or on-call debugging. Write one concrete two-sentence scenario tying
the worked example to that scenario. Tomorrow, when you rewrite the exercise from
memory, check whether the code still fits that framing.
""",
            exercise_guide="""
Implement heap/tree helpers so extract-min / traversal tests pass.
""",
            exercise_examples="""
Popping from a min-heap yields sorted ascending order.
""",
        ),
        25: dict(
            body="""
## Why this matters

Graphs model networks, dependencies, and workflows. BFS/DFS are the default tools for reachability and shortest unweighted paths.

This lesson is a building block for later modules in the Goodway path. If you only
skim, the exercises will feel like busywork; if you type the examples and narrate
them aloud, the same patterns will reappear in HTTP handlers, concurrency, and AI
service glue.

## Core concepts

- Represent graphs with adjacency lists: map[T][]T.
- BFS uses a queue; DFS uses stack/recursion.
- Mark visited to avoid cycles.
- Unweighted shortest path = BFS layers.
- Directed vs undirected changes edge insertion.

Hold these in working memory while you code. Each bullet should map to something
you can demonstrate with a three-line program or a failing compile error.

## Worked Go examples

Create a scratch module and type this yourself (do not paste blindly):

```bash
mkdir -p /tmp/gw-graphs: && cd /tmp/gw-graphs:
go mod init example.com/scratch
```

Then create `main.go`:

```go
package main

import "fmt"

func BFS(start string, adj map[string][]string) []string {
    seen := map[string]bool{start: true}
    q := []string{start}
    var order []string
    for len(q) > 0 {
        u := q[0]
        q = q[1:]
        order = append(order, u)
        for _, v := range adj[u] {
            if !seen[v] {
                seen[v] = true
                q = append(q, v)
            }
        }
    }
    return order
}

func main() {
    adj := map[string][]string{"A": {"B", "C"}, "B": {"D"}, "C": {}, "D": {}}
    fmt.Println(BFS("A", adj))
}
```

Run it:

```bash
go run .
```

Expected output:

```text
[A B C D]
```

If your output differs, diff character-by-character — especially whitespace and
types. Then change one line deliberately and predict the new output before running.

## Mini-lab (`go run` steps)

1. BFS a small graph; print visit order.
2. DFS recursive and iterative.
3. Compute unweighted distance via BFS layers.

Write down one sentence explaining *why* the output matches the code before you move on.
Time-box the lab to 15–25 minutes; struggle is part of encoding the skill.

## Curriculum notes (expanded from the compact draft)

## Representation

```go
type Graph map[string][]string // adjacency list
```

Prefer adjacency lists for sparse graphs (most real networks).

## BFS / DFS

- BFS: queue — shortest path in unweighted graphs
- DFS: stack/recursion — cycle detection, topological vibes

```go
func BFS(g Graph, start string) []string {
    seen := map[string]bool{start: true}
    q := []string{start}
    var order []string
    for len(q) > 0 {
        u := q[0]; q = q[1:]
        order = append(order, u)
        for _, v := range g[u] {
            if !seen[v] { seen[v] = true; q = append(q, v) }
        }
    }
    return order
}
```

## Weighted shortest paths

Dijkstra with a priority queue finds shortest paths for non-negative weights — core infra for routing and dependency costs.

## Failure modes to watch while coding

- Adjacency matrix for huge sparse graphs
- Forgetting seen set → infinite loops
- Dijkstra with negative edges

When a test fails, ask which failure mode you hit before changing code at random.

## Idioms vs Python pitfalls

- Same algorithms; Go maps+slices are the usual adjacency structure.
- collections.deque vs slice queue (O(n) head pop — ok for learning).
- NetworkX hides representation — implement by hand here.

When you catch yourself reaching for a Python habit, pause and rewrite the Go way
once on purpose — even if both would "work". The goal is a Go-shaped intuition.

## Going deeper

For weighted shortest paths, Dijkstra comes next — know when BFS is enough.

## Practice checklist

Before the exercise, confirm you can:

1. Explain "Graphs: BFS, DFS, Shortest Paths Intro" aloud in under two minutes without notes.
2. Re-type the worked example from memory and match the expected output.
3. Name the Go standard library packages touched by this lesson.
4. List one production bug this lesson's rules prevent.
5. Contrast the Go approach with the Python instinct listed above.
6. Write a three-line cheat sheet: one idiom, one pitfall, one command to remember.

If any item fails, re-run the mini-lab once more, then attempt the exercise tests.

## Transfer to production

Ask where this shows up outside toys: config loading, API handlers, data pipelines,
CI scripts, or on-call debugging. Write one concrete two-sentence scenario tying
the worked example to that scenario. Tomorrow, when you rewrite the exercise from
memory, check whether the code still fits that framing.
""",
            exercise_guide="""
Implement BFS (or the exercise's graph walk) to match expected visit order.
""",
            exercise_examples="""
From A in A→B,C; B→D order starts with A then neighbors.
""",
        ),
        26: dict(
            body="""
## Why this matters

Hashing underpins maps, caches, and probabilistic filters. Bloom filters trade a false-positive rate for tiny memory — classic infra tool.

This lesson is a building block for later modules in the Goodway path. If you only
skim, the exercises will feel like busywork; if you type the examples and narrate
them aloud, the same patterns will reappear in HTTP handlers, concurrency, and AI
service glue.

## Core concepts

- Hash functions distribute keys; collisions are normal.
- Go maps hide hashing; understand load and resizing conceptually.
- Bloom filters: insert sets bits; query may false-positive, never false-negative (for basic blooms).
- Choose k hash functions / bitset size from expected n and error rate.
- Cryptographic vs non-crypto hashes — don't confuse them.

Hold these in working memory while you code. Each bullet should map to something
you can demonstrate with a three-line program or a failing compile error.

## Worked Go examples

Create a scratch module and type this yourself (do not paste blindly):

```bash
mkdir -p /tmp/gw-hashing && cd /tmp/gw-hashing
go mod init example.com/scratch
```

Then create `main.go`:

```go
package main

import (
    "fmt"
    "hash/fnv"
)

func hash(s string) uint64 {
    h := fnv.New64a()
    _, _ = h.Write([]byte(s))
    return h.Sum64()
}

func main() { fmt.Println(hash("go") != 0) }
```

Run it:

```bash
go run .
```

Expected output:

```text
true
```

If your output differs, diff character-by-character — especially whitespace and
types. Then change one line deliberately and predict the new output before running.

## Mini-lab (`go run` steps)

1. Hash strings with FNV and print distribution buckets.
2. Sketch a tiny bitset Bloom with two hashes.
3. Demonstrate a false positive on purpose with a tiny filter.

Write down one sentence explaining *why* the output matches the code before you move on.
Time-box the lab to 15–25 minutes; struggle is part of encoding the skill.

## Curriculum notes (expanded from the compact draft)

## Hash tables (maps)

Go's `map` is a hash table: average O(1) lookup. Hash collisions are handled internally.

## Cryptographic vs non-crypto

- `hash/fnv`, `maphash`: fast, non-crypto
- `crypto/sha256`: integrity / security

Do not use non-crypto hashes for security tokens.

## Bloom filters

Probabilistic set: can say "possibly in set" or "definitely not".
Uses bit array + k hash functions. False positives; no false negatives (for standard bloom).

Used in: databases (skip disk reads), caches, distributed systems membership tests.

Tradeoff: memory vs false positive rate.

## Failure modes to watch while coding

- Using MD5 for security (broken)
- Ignoring bloom false positives in logic
- Rolling your own crypto

When a test fails, ask which failure mode you hit before changing code at random.

## Idioms vs Python pitfalls

- hash() randomization in Python vs stable FNV here.
- set membership is exact; Bloom is probabilistic.
- Don't use MD5 for security; fine for demos of distribution.

When you catch yourself reaching for a Python habit, pause and rewrite the Go way
once on purpose — even if both would "work". The goal is a Go-shaped intuition.

## Going deeper

In caches, hashing also means key design: canonical serialization before hash.

## Practice checklist

Before the exercise, confirm you can:

1. Explain "Hashing and Bloom Filters (Infra-Relevant)" aloud in under two minutes without notes.
2. Re-type the worked example from memory and match the expected output.
3. Name the Go standard library packages touched by this lesson.
4. List one production bug this lesson's rules prevent.
5. Contrast the Go approach with the Python instinct listed above.
6. Write a three-line cheat sheet: one idiom, one pitfall, one command to remember.

If any item fails, re-run the mini-lab once more, then attempt the exercise tests.

## Transfer to production

Ask where this shows up outside toys: config loading, API handlers, data pipelines,
CI scripts, or on-call debugging. Write one concrete two-sentence scenario tying
the worked example to that scenario. Tomorrow, when you rewrite the exercise from
memory, check whether the code still fits that framing.
""",
            exercise_guide="""
Implement the bloom/hash stub per tests (likely Add/MightContain).
""",
            exercise_examples="""
After Add(x), MightContain(x) is true; fresh keys may false-positive.
""",
        ),
        27: dict(
            body="""
## Why this matters

Dynamic programming turns exponential search into polynomial tables. In infra, DP thinking shows up in scheduling and path problems.

This lesson is a building block for later modules in the Goodway path. If you only
skim, the exercises will feel like busywork; if you type the examples and narrate
them aloud, the same patterns will reappear in HTTP handlers, concurrency, and AI
service glue.

## Core concepts

- Identify overlapping subproblems + optimal substructure.
- Bottom-up tables vs top-down memo maps.
- Define state clearly: dp[i] meaning in one sentence.
- Watch index off-by-ones and base cases.
- Reconstruct solutions by storing choices, not only values.

Hold these in working memory while you code. Each bullet should map to something
you can demonstrate with a three-line program or a failing compile error.

## Worked Go examples

Create a scratch module and type this yourself (do not paste blindly):

```bash
mkdir -p /tmp/gw-dynamic && cd /tmp/gw-dynamic
go mod init example.com/scratch
```

Then create `main.go`:

```go
package main

import "fmt"

func Climb(n int) int {
    if n <= 2 {
        return n
    }
    a, b := 1, 2
    for i := 3; i <= n; i++ {
        a, b = b, a+b
    }
    return b
}

func main() { fmt.Println(Climb(5)) }
```

Run it:

```bash
go run .
```

Expected output:

```text
8
```

If your output differs, diff character-by-character — especially whitespace and
types. Then change one line deliberately and predict the new output before running.

## Mini-lab (`go run` steps)

1. Climbing stairs bottom-up.
2. Memoize a recursive solution with a map.
3. Write the dp state meaning as a comment first.

Write down one sentence explaining *why* the output matches the code before you move on.
Time-box the lab to 15–25 minutes; struggle is part of encoding the skill.

## Curriculum notes (expanded from the compact draft)

## Idea

DP stores answers to subproblems to avoid recomputation.

```go
// Climb stairs: ways(n) = ways(n-1)+ways(n-2)
func Climb(n int) int {
    if n < 2 { return 1 }
    a, b := 1, 1
    for i := 2; i <= n; i++ {
        a, b = b, a+b
    }
    return b
}
```

## Pattern checklist

1. Define state clearly (`dp[i]` means …)
2. Write recurrence
3. Determine base cases
4. Choose iteration order
5. Optimize space if only last states needed

## Infra relevance

DP appears in scheduling, rate allocation, tokenization costs, and alignment-like problems — not only interview questions.

## Failure modes to watch while coding

- Memoizing without clear state definition
- Off-by-one in table sizes
- Exponential backtracking labeled as DP

When a test fails, ask which failure mode you hit before changing code at random.

## Idioms vs Python pitfalls

- functools.lru_cache ≈ map memo in Go.
- Same recurrence, different syntax.
- Be explicit about mutation of DP slices.

When you catch yourself reaching for a Python habit, pause and rewrite the Go way
once on purpose — even if both would "work". The goal is a Go-shaped intuition.

## Going deeper

If you cannot name the state, you are not ready to code the loop.

## Practice checklist

Before the exercise, confirm you can:

1. Explain "Dynamic Programming Patterns" aloud in under two minutes without notes.
2. Re-type the worked example from memory and match the expected output.
3. Name the Go standard library packages touched by this lesson.
4. List one production bug this lesson's rules prevent.
5. Contrast the Go approach with the Python instinct listed above.
6. Write a three-line cheat sheet: one idiom, one pitfall, one command to remember.

If any item fails, re-run the mini-lab once more, then attempt the exercise tests.

## Transfer to production

Ask where this shows up outside toys: config loading, API handlers, data pipelines,
CI scripts, or on-call debugging. Write one concrete two-sentence scenario tying
the worked example to that scenario. Tomorrow, when you rewrite the exercise from
memory, check whether the code still fits that framing.
""",
            exercise_guide="""
Implement the DP function (e.g. climb/knapsack-style) to match tests.
""",
            exercise_examples="""
Climb(5)→8 for the classic 1/2 step problem.
""",
        ),
        28: dict(
            body="""
## Why this matters

Mixed drills build fluency: hashing + two pointers + sorting under time pressure. This is how interview and on-call problem solving get faster.

This lesson is a building block for later modules in the Goodway path. If you only
skim, the exercises will feel like busywork; if you type the examples and narrate
them aloud, the same patterns will reappear in HTTP handlers, concurrency, and AI
service glue.

## Core concepts

- Clarify inputs/outputs and constraints before coding.
- Start with brute force, then improve with maps/sorts.
- Two-sum pattern: map value→index.
- Write tests first for edge cases: empty, duplicates, negatives.
- Idiomatic Go: early returns, no clever one-liners.

Hold these in working memory while you code. Each bullet should map to something
you can demonstrate with a three-line program or a failing compile error.

## Worked Go examples

Create a scratch module and type this yourself (do not paste blindly):

```bash
mkdir -p /tmp/gw-algorithmic && cd /tmp/gw-algorithmic
go mod init example.com/scratch
```

Then create `main.go`:

```go
package main

import "fmt"

func TwoSum(nums []int, target int) [2]int {
    idx := map[int]int{}
    for i, n := range nums {
        if j, ok := idx[target-n]; ok {
            return [2]int{j, i}
        }
        idx[n] = i
    }
    return [2]int{-1, -1}
}

func main() { fmt.Println(TwoSum([]int{2, 7, 11, 15}, 9)) }
```

Run it:

```bash
go run .
```

Expected output:

```text
[0 1]
```

If your output differs, diff character-by-character — especially whitespace and
types. Then change one line deliberately and predict the new output before running.

## Mini-lab (`go run` steps)

1. Implement two-sum with a map.
2. Add tests for not-found and duplicates.
3. Time a naive O(n^2) vs map solution.

Write down one sentence explaining *why* the output matches the code before you move on.
Time-box the lab to 15–25 minutes; struggle is part of encoding the skill.

## Curriculum notes (expanded from the compact draft)

## Drill protocol

For each problem:
1. Restate inputs/outputs and constraints
2. Work an example by hand
3. Propose brute force + complexity
4. Improve if needed
5. Implement in Go with table tests
6. Benchmark if n is large

## Problem themes in the exercises

- Two-sum variants with maps
- Sliding window
- Interval merge
- Top-K with heaps
- Graph connectivity

Treat this lesson as a gym: correctness under pressure, then clarity.

## Failure modes to watch while coding

- Coding before examples
- Silent assumption about sorted input
- Mutating inputs unexpectedly

When a test fails, ask which failure mode you hit before changing code at random.

## Idioms vs Python pitfalls

- Same patterns; dict vs map syntax.
- enumerate ≈ for i, v := range.
- Return tuples vs arrays/slices — match the API.

When you catch yourself reaching for a Python habit, pause and rewrite the Go way
once on purpose — even if both would "work". The goal is a Go-shaped intuition.

## Going deeper

Narrate complexity out loud while coding — it catches bad approaches early.

## Practice checklist

Before the exercise, confirm you can:

1. Explain "Algorithmic Problem Set (Mixed Drills)" aloud in under two minutes without notes.
2. Re-type the worked example from memory and match the expected output.
3. Name the Go standard library packages touched by this lesson.
4. List one production bug this lesson's rules prevent.
5. Contrast the Go approach with the Python instinct listed above.
6. Write a three-line cheat sheet: one idiom, one pitfall, one command to remember.

If any item fails, re-run the mini-lab once more, then attempt the exercise tests.

## Transfer to production

Ask where this shows up outside toys: config loading, API handlers, data pipelines,
CI scripts, or on-call debugging. Write one concrete two-sentence scenario tying
the worked example to that scenario. Tomorrow, when you rewrite the exercise from
memory, check whether the code still fits that framing.
""",
            exercise_guide="""
Implement TwoSum (or the drill set) exactly as tests specify indices.
""",
            exercise_examples="""
TwoSum([2,7,11,15],9)→[0,1].
""",
        ),
        29: dict(
            body="""
## Why this matters

Goroutines are cheap concurrent functions scheduled by the Go runtime. They are why Go shines for servers and pipelines — used carefully.

This lesson is a building block for later modules in the Goodway path. If you only
skim, the exercises will feel like busywork; if you type the examples and narrate
them aloud, the same patterns will reappear in HTTP handlers, concurrency, and AI
service glue.

## Core concepts

- `go f()` starts a goroutine; it may outlive the caller.
- The scheduler multiplexes goroutines onto OS threads.
- Always have an exit condition — leaks are real.
- sync.WaitGroup waits for a set of goroutines.
- Do not share mutable state without sync (next lessons).

Hold these in working memory while you code. Each bullet should map to something
you can demonstrate with a three-line program or a failing compile error.

## Worked Go examples

Create a scratch module and type this yourself (do not paste blindly):

```bash
mkdir -p /tmp/gw-goroutines && cd /tmp/gw-goroutines
go mod init example.com/scratch
```

Then create `main.go`:

```go
package main

import (
    "fmt"
    "sync"
)

func main() {
    var wg sync.WaitGroup
    for i := 0; i < 3; i++ {
        wg.Add(1)
        go func(n int) {
            defer wg.Done()
            fmt.Println("hi", n)
        }(i)
    }
    wg.Wait()
}
```

Run it:

```bash
go run .
```

Expected output:

```text
hi 0
hi 1
hi 2
(order may vary)
```

If your output differs, diff character-by-character — especially whitespace and
types. Then change one line deliberately and predict the new output before running.

## Mini-lab (`go run` steps)

1. Launch N goroutines with WaitGroup.
2. Forget Done once and observe a hang — then fix.
3. Pass loop variable as an argument (classic gotcha in older Go).

Write down one sentence explaining *why* the output matches the code before you move on.
Time-box the lab to 15–25 minutes; struggle is part of encoding the skill.

## Curriculum notes (expanded from the compact draft)

## Goroutines

```go
go func() {
    doWork()
}()
```

Goroutines are lightweight concurrent functions multiplexed onto OS threads by the Go scheduler (M:N).

## Leaks

A goroutine leak is a goroutine that never exits — common when blocked on channel/IO forever.
Always plan an exit path (context, close channel, timeout).

## WaitGroup

```go
var wg sync.WaitGroup
wg.Add(1)
go func() {
    defer wg.Done()
    work()
}()
wg.Wait()
```

Do not assume goroutine order. Concurrency ≠ parallelism (but Go gives you both tools).

## Failure modes to watch while coding

- Fire-and-forget goroutines in request handlers without limits
- Capturing loop variables incorrectly (modern Go fixed per-iteration vars; still be careful)
- Waiting forever with no timeout

When a test fails, ask which failure mode you hit before changing code at random.

## Idioms vs Python pitfalls

- threading.Thread is heavy; goroutines are lighter.
- asyncio is cooperative; Go is concurrent with a scheduler.
- GIL limits CPU threads; Go uses multiple OS threads freely.

When you catch yourself reaching for a Python habit, pause and rewrite the Go way
once on purpose — even if both would "work". The goal is a Go-shaped intuition.

## Going deeper

Structure concurrency as trees of tasks with clear cancellation (context).

## Practice checklist

Before the exercise, confirm you can:

1. Explain "Goroutines and the Scheduler" aloud in under two minutes without notes.
2. Re-type the worked example from memory and match the expected output.
3. Name the Go standard library packages touched by this lesson.
4. List one production bug this lesson's rules prevent.
5. Contrast the Go approach with the Python instinct listed above.
6. Write a three-line cheat sheet: one idiom, one pitfall, one command to remember.

If any item fails, re-run the mini-lab once more, then attempt the exercise tests.

## Transfer to production

Ask where this shows up outside toys: config loading, API handlers, data pipelines,
CI scripts, or on-call debugging. Write one concrete two-sentence scenario tying
the worked example to that scenario. Tomorrow, when you rewrite the exercise from
memory, check whether the code still fits that framing.
""",
            exercise_guide="""
Use WaitGroup (or the exercise API) so all goroutines finish before return.
""",
            exercise_examples="""
Tests wait for results; hanging means missing Done/cancel.
""",
        ),
        30: dict(
            body="""
## Why this matters

Channels synchronize and communicate. Select lets you wait on multiple events — timeouts, cancellation, and data — in one place.

This lesson is a building block for later modules in the Goodway path. If you only
skim, the exercises will feel like busywork; if you type the examples and narrate
them aloud, the same patterns will reappear in HTTP handlers, concurrency, and AI
service glue.

## Core concepts

- chan T is typed; make(chan T, n) sets buffer size.
- Send/receive block until the other side is ready (unbuffered).
- close signals no more sends; range over chan until closed.
- select chooses among ready cases; default is non-blocking.
- Prefer ownership: only the sender closes.

Hold these in working memory while you code. Each bullet should map to something
you can demonstrate with a three-line program or a failing compile error.

## Worked Go examples

Create a scratch module and type this yourself (do not paste blindly):

```bash
mkdir -p /tmp/gw-channels, && cd /tmp/gw-channels,
go mod init example.com/scratch
```

Then create `main.go`:

```go
package main

import "fmt"

func main() {
    ch := make(chan int, 2)
    ch <- 1
    ch <- 2
    close(ch)
    for v := range ch {
        fmt.Println(v)
    }
}
```

Run it:

```bash
go run .
```

Expected output:

```text
1
2
```

If your output differs, diff character-by-character — especially whitespace and
types. Then change one line deliberately and predict the new output before running.

## Mini-lab (`go run` steps)

1. Pipeline: generator → square → print with channels.
2. select with time.After for a timeout.
3. Show deadlock with unbuffered send and no receiver.

Write down one sentence explaining *why* the output matches the code before you move on.
Time-box the lab to 15–25 minutes; struggle is part of encoding the skill.

## Curriculum notes (expanded from the compact draft)

## Channels

```go
ch := make(chan int)      // unbuffered
buf := make(chan int, 16) // buffered
ch <- 3
v := <-ch
close(ch)
```

Unbuffered send/receive synchronizes two goroutines. Buffer decouples up to capacity.

## select

```go
select {
case v := <-in:
    // handle
case <-ctx.Done():
    return ctx.Err()
case out <- v:
    // send
default:
    // non-blocking path
}
```

## Pipelines

Stage functions: `in <-chan T` → `out <-chan U`, close out when done.
Receivers use `for v := range ch`.

## Failure modes to watch while coding

- Closing channels from receivers
- Sending on closed channel (panic)
- Unbounded goroutine fan-out without backpressure

When a test fails, ask which failure mode you hit before changing code at random.

## Idioms vs Python pitfalls

- queue.Queue ≈ buffered channel, but channels also sync.
- No select equivalent as clean as Go's.
- Generators vs channel producers — close when done.

When you catch yourself reaching for a Python habit, pause and rewrite the Go way
once on purpose — even if both would "work". The goal is a Go-shaped intuition.

## Going deeper

Pipelines: each stage closes its output when the input is drained.

## Practice checklist

Before the exercise, confirm you can:

1. Explain "Channels, Select, and Pipelines" aloud in under two minutes without notes.
2. Re-type the worked example from memory and match the expected output.
3. Name the Go standard library packages touched by this lesson.
4. List one production bug this lesson's rules prevent.
5. Contrast the Go approach with the Python instinct listed above.
6. Write a three-line cheat sheet: one idiom, one pitfall, one command to remember.

If any item fails, re-run the mini-lab once more, then attempt the exercise tests.

## Transfer to production

Ask where this shows up outside toys: config loading, API handlers, data pipelines,
CI scripts, or on-call debugging. Write one concrete two-sentence scenario tying
the worked example to that scenario. Tomorrow, when you rewrite the exercise from
memory, check whether the code still fits that framing.
""",
            exercise_guide="""
Wire channel pipeline/select behavior required by tests.
""",
            exercise_examples="""
Values sent must be received; closed channels terminate range.
""",
        ),
        31: dict(
            body="""
## Why this matters

Mutexes protect shared memory. Atomics handle simple counters without heavy locks. Choosing wrongly causes races or slowdowns.

This lesson is a building block for later modules in the Goodway path. If you only
skim, the exercises will feel like busywork; if you type the examples and narrate
them aloud, the same patterns will reappear in HTTP handlers, concurrency, and AI
service glue.

## Core concepts

- sync.Mutex: Lock/Unlock around critical sections.
- RWMutex for read-heavy workloads.
- sync/atomic for integers and pointers with care.
- Never copy a struct containing a Mutex after first use.
- `go test -race` is mandatory for concurrent code.

Hold these in working memory while you code. Each bullet should map to something
you can demonstrate with a three-line program or a failing compile error.

## Worked Go examples

Create a scratch module and type this yourself (do not paste blindly):

```bash
mkdir -p /tmp/gw-mutexes, && cd /tmp/gw-mutexes,
go mod init example.com/scratch
```

Then create `main.go`:

```go
package main

import (
    "fmt"
    "sync"
)

func main() {
    var mu sync.Mutex
    var n int
    var wg sync.WaitGroup
    for i := 0; i < 1000; i++ {
        wg.Add(1)
        go func() {
            defer wg.Done()
            mu.Lock()
            n++
            mu.Unlock()
        }()
    }
    wg.Wait()
    fmt.Println(n)
}
```

Run it:

```bash
go run .
```

Expected output:

```text
1000
```

If your output differs, diff character-by-character — especially whitespace and
types. Then change one line deliberately and predict the new output before running.

## Mini-lab (`go run` steps)

1. Increment without mutex; run -race.
2. Fix with Mutex; confirm race gone.
3. Replace with atomic.AddInt64 and compare.

Write down one sentence explaining *why* the output matches the code before you move on.
Time-box the lab to 15–25 minutes; struggle is part of encoding the skill.

## Curriculum notes (expanded from the compact draft)

## Mutex

```go
type Safe struct {
    mu sync.Mutex
    m  map[string]int
}

func (s *Safe) Inc(k string) {
    s.mu.Lock()
    defer s.mu.Unlock()
    s.m[k]++
}
```

## Atomics

`atomic.Int64` for counters without mutex — not a free pass for complex invariants.

## Design preference

1. Don't share (owning goroutine)
2. Channels for ownership transfer
3. Mutex for shared structures
4. Atomics for simple stats

Always `go test -race`.

## Failure modes to watch while coding

- Copying a struct containing a mutex
- Holding locks across slow I/O
- Assuming map access is safe concurrently

When a test fails, ask which failure mode you hit before changing code at random.

## Idioms vs Python pitfalls

- threading.Lock ≈ Mutex.
- GIL can mask races — Go will not.
- Prefer channels when communicating ownership; mutex when sharing state.

When you catch yourself reaching for a Python habit, pause and rewrite the Go way
once on purpose — even if both would "work". The goal is a Go-shaped intuition.

## Going deeper

Keep critical sections tiny. Do I/O outside the lock.

## Practice checklist

Before the exercise, confirm you can:

1. Explain "Mutexes, Atomics, and sync Primitives" aloud in under two minutes without notes.
2. Re-type the worked example from memory and match the expected output.
3. Name the Go standard library packages touched by this lesson.
4. List one production bug this lesson's rules prevent.
5. Contrast the Go approach with the Python instinct listed above.
6. Write a three-line cheat sheet: one idiom, one pitfall, one command to remember.

If any item fails, re-run the mini-lab once more, then attempt the exercise tests.

## Transfer to production

Ask where this shows up outside toys: config loading, API handlers, data pipelines,
CI scripts, or on-call debugging. Write one concrete two-sentence scenario tying
the worked example to that scenario. Tomorrow, when you rewrite the exercise from
memory, check whether the code still fits that framing.
""",
            exercise_guide="""
Protect shared counters/state so tests pass under race detector.
""",
            exercise_examples="""
Final counter equals number of increments.
""",
        ),
        32: dict(
            body="""
## Why this matters

Worker pools bound concurrency. Fan-in/out and backpressure keep systems stable under load instead of spawning unbounded goroutines.

This lesson is a building block for later modules in the Goodway path. If you only
skim, the exercises will feel like busywork; if you type the examples and narrate
them aloud, the same patterns will reappear in HTTP handlers, concurrency, and AI
service glue.

## Core concepts

- Fixed workers pull jobs from a channel.
- Buffered channels provide limited queueing (backpressure).
- Fan-out: many workers; fan-in: merge results.
- Close job channels to signal completion.
- Context cancels in-flight work when the caller leaves.

Hold these in working memory while you code. Each bullet should map to something
you can demonstrate with a three-line program or a failing compile error.

## Worked Go examples

Create a scratch module and type this yourself (do not paste blindly):

```bash
mkdir -p /tmp/gw-worker && cd /tmp/gw-worker
go mod init example.com/scratch
```

Then create `main.go`:

```go
package main

import (
    "fmt"
    "sync"
)

func main() {
    jobs := make(chan int, 5)
    results := make(chan int, 5)
    var wg sync.WaitGroup
    for w := 0; w < 3; w++ {
        wg.Add(1)
        go func() {
            defer wg.Done()
            for j := range jobs {
                results <- j * 2
            }
        }()
    }
    for j := 1; j <= 5; j++ {
        jobs <- j
    }
    close(jobs)
    wg.Wait()
    close(results)
    for r := range results {
        fmt.Println(r)
    }
}
```

Run it:

```bash
go run .
```

Expected output:

```text
2
4
6
8
10
(order may vary)
```

If your output differs, diff character-by-character — especially whitespace and
types. Then change one line deliberately and predict the new output before running.

## Mini-lab (`go run` steps)

1. Build a 3-worker pool doubling ints.
2. Lower buffer to 0 and observe backpressure.
3. Add context cancel mid-flight.

Write down one sentence explaining *why* the output matches the code before you move on.
Time-box the lab to 15–25 minutes; struggle is part of encoding the skill.

## Curriculum notes (expanded from the compact draft)

## Worker pool

```go
jobs := make(chan Job)
results := make(chan Result)
for i := 0; i < workers; i++ {
    go worker(ctx, jobs, results)
}
```

Bound the number of goroutines doing expensive work. Unbounded `go` per request is a common outage cause.

## Backpressure

When consumers are slow, producers must block or drop according to policy.
Buffered channels provide limited slack — not infinite queues.

## Fan-out / fan-in

Split work across workers (fan-out), merge results (fan-in) with a WaitGroup + results channel.

## Failure modes to watch while coding

- Unbuffered infinite job pileup in memory via huge buffers
- No context cancellation on shutdown
- Result channel deadlock when workers exit wrong

When a test fails, ask which failure mode you hit before changing code at random.

## Idioms vs Python pitfalls

- concurrent.futures.Executor ≈ worker pool.
- Unbounded thread spawns ≈ unbounded go statements — both bad.
- Queue maxsize ≈ buffered channel capacity.

When you catch yourself reaching for a Python habit, pause and rewrite the Go way
once on purpose — even if both would "work". The goal is a Go-shaped intuition.

## Going deeper

Tune worker count with benchmarks and external limits (DB pools, CPU).

## Practice checklist

Before the exercise, confirm you can:

1. Explain "Worker Pools, Fan-in/out, Backpressure" aloud in under two minutes without notes.
2. Re-type the worked example from memory and match the expected output.
3. Name the Go standard library packages touched by this lesson.
4. List one production bug this lesson's rules prevent.
5. Contrast the Go approach with the Python instinct listed above.
6. Write a three-line cheat sheet: one idiom, one pitfall, one command to remember.

If any item fails, re-run the mini-lab once more, then attempt the exercise tests.

## Transfer to production

Ask where this shows up outside toys: config loading, API handlers, data pipelines,
CI scripts, or on-call debugging. Write one concrete two-sentence scenario tying
the worked example to that scenario. Tomorrow, when you rewrite the exercise from
memory, check whether the code still fits that framing.
""",
            exercise_guide="""
Implement pool semantics: workers process all jobs; results complete.
""",
            exercise_examples="""
Doubling pool returns 2*job for each input.
""",
        ),
        33: dict(
            body="""
## Why this matters

Deadlocks and races are production killers. Cancellation patterns and the race detector teach you to design for failure.

This lesson is a building block for later modules in the Goodway path. If you only
skim, the exercises will feel like busywork; if you type the examples and narrate
them aloud, the same patterns will reappear in HTTP handlers, concurrency, and AI
service glue.

## Core concepts

- Deadlock: all goroutines wait forever — often lock order or channel cycles.
- Race: unsynchronized memory access — undefined behavior.
- Always acquire locks in a consistent global order.
- Propagate context cancellation to break waits.
- Prefer ownership transfer via channels to shared mutable state when possible.

Hold these in working memory while you code. Each bullet should map to something
you can demonstrate with a three-line program or a failing compile error.

## Worked Go examples

Create a scratch module and type this yourself (do not paste blindly):

```bash
mkdir -p /tmp/gw-deadlocks, && cd /tmp/gw-deadlocks,
go mod init example.com/scratch
```

Then create `main.go`:

```go
package main

import (
    "context"
    "fmt"
    "time"
)

func main() {
    ctx, cancel := context.WithTimeout(context.Background(), 50*time.Millisecond)
    defer cancel()
    ch := make(chan int)
    select {
    case <-ch:
        fmt.Println("got")
    case <-ctx.Done():
        fmt.Println("cancelled")
    }
}
```

Run it:

```bash
go run .
```

Expected output:

```text
cancelled
```

If your output differs, diff character-by-character — especially whitespace and
types. Then change one line deliberately and predict the new output before running.

## Mini-lab (`go run` steps)

1. Create a channel deadlock; fix with buffer or goroutine.
2. Run a racy counter under -race.
3. Add timeout select to a blocking receive.

Write down one sentence explaining *why* the output matches the code before you move on.
Time-box the lab to 15–25 minutes; struggle is part of encoding the skill.

## Curriculum notes (expanded from the compact draft)

## Deadlocks

Common causes:
- Lock ordering A then B vs B then A
- Two goroutines waiting on each other unbuffered
- WaitGroup Add inside the goroutine incorrectly

## Races

A data race: concurrent access to a variable, at least one write, no sync.
Fix by synchronizing or not sharing.

## Cancellation pattern

```go
func worker(ctx context.Context, in <-chan Task) error {
    for {
        select {
        case <-ctx.Done():
            return ctx.Err()
        case t, ok := <-in:
            if !ok { return nil }
            if err := handle(ctx, t); err != nil { return err }
        }
    }
}
```

## Failure modes to watch while coding

- "It didn't race on my machine" without -race
- Fixing races by sleeping
- Nested locks without ordering rules

When a test fails, ask which failure mode you hit before changing code at random.

## Idioms vs Python pitfalls

- Deadlocks exist in threading too; Go makes them more visible.
- Race detector is a superpower — use it in CI.
- asyncio cancellation ≈ context cancel.

When you catch yourself reaching for a Python habit, pause and rewrite the Go way
once on purpose — even if both would "work". The goal is a Go-shaped intuition.

## Going deeper

On deadlock, print goroutine stacks (SIGQUIT / panic) and look for who waits on what.

## Practice checklist

Before the exercise, confirm you can:

1. Explain "Deadlocks, Races, and Cancellation Patterns" aloud in under two minutes without notes.
2. Re-type the worked example from memory and match the expected output.
3. Name the Go standard library packages touched by this lesson.
4. List one production bug this lesson's rules prevent.
5. Contrast the Go approach with the Python instinct listed above.
6. Write a three-line cheat sheet: one idiom, one pitfall, one command to remember.

If any item fails, re-run the mini-lab once more, then attempt the exercise tests.

## Transfer to production

Ask where this shows up outside toys: config loading, API handlers, data pipelines,
CI scripts, or on-call debugging. Write one concrete two-sentence scenario tying
the worked example to that scenario. Tomorrow, when you rewrite the exercise from
memory, check whether the code still fits that framing.
""",
            exercise_guide="""
Ensure cancellation paths return instead of hanging; fix racey access.
""",
            exercise_examples="""
Functions return when ctx done; tests fail on timeout hang.
""",
        ),
        34: dict(
            body="""
## Why this matters

Concurrent algorithms combine correct partitioning with sync. Parallel sum/map patterns prepare you for real data pipelines.

This lesson is a building block for later modules in the Goodway path. If you only
skim, the exercises will feel like busywork; if you type the examples and narrate
them aloud, the same patterns will reappear in HTTP handlers, concurrency, and AI
service glue.

## Core concepts

- Split input into shards; process independently; merge.
- Avoid false sharing conceptually; keep shards separate.
- WaitGroup + results channel is a common merge pattern.
- Correctness first, then speedup measurements.
- Not all problems parallelize — Amdahl's law.

Hold these in working memory while you code. Each bullet should map to something
you can demonstrate with a three-line program or a failing compile error.

## Worked Go examples

Create a scratch module and type this yourself (do not paste blindly):

```bash
mkdir -p /tmp/gw-concurrent && cd /tmp/gw-concurrent
go mod init example.com/scratch
```

Then create `main.go`:

```go
package main

import (
    "fmt"
    "sync"
)

func ParSum(xs []int, workers int) int {
    if workers < 1 {
        workers = 1
    }
    ch := make(chan int, workers)
    var wg sync.WaitGroup
    n := len(xs)
    size := (n + workers - 1) / workers
    for w := 0; w < workers; w++ {
        lo := w * size
        if lo >= n {
            break
        }
        hi := lo + size
        if hi > n {
            hi = n
        }
        wg.Add(1)
        go func(part []int) {
            defer wg.Done()
            s := 0
            for _, v := range part {
                s += v
            }
            ch <- s
        }(xs[lo:hi])
    }
    go func() { wg.Wait(); close(ch) }()
    total := 0
    for s := range ch {
        total += s
    }
    return total
}

func main() { fmt.Println(ParSum([]int{1, 2, 3, 4}, 2)) }
```

Run it:

```bash
go run .
```

Expected output:

```text
10
```

If your output differs, diff character-by-character — especially whitespace and
types. Then change one line deliberately and predict the new output before running.

## Mini-lab (`go run` steps)

1. Parallel sum with 1 vs 4 workers; check equal results.
2. Benchmark both.
3. Break merge by double-closing a channel — then fix.

Write down one sentence explaining *why* the output matches the code before you move on.
Time-box the lab to 15–25 minutes; struggle is part of encoding the skill.

## Curriculum notes (expanded from the compact draft)

## Drill themes

- Parallel sum / histogram with shard-per-worker then merge
- Concurrent crawler with URL graph + visited set (mutex or owning map goroutine)
- Pipeline: read → parse → enrich → write

## Rules

- Bound parallelism to GOMAXPROCS or a chosen limit
- No shared map writes without sync
- Tests must be deterministic (sort outputs)

Measure: sometimes parallel is slower due to coordination overhead — learn when.

## Failure modes to watch while coding

- Racing on shared maps
- More goroutines than work items blindly
- Non-deterministic test flakes ignored

When a test fails, ask which failure mode you hit before changing code at random.

## Idioms vs Python pitfalls

- multiprocessing vs goroutines — different memory models.
- Shared-memory parallel needs locks in both.
- Chunking strategy matters more than language.

When you catch yourself reaching for a Python habit, pause and rewrite the Go way
once on purpose — even if both would "work". The goal is a Go-shaped intuition.

## Going deeper

For tiny inputs, parallel overhead wins — gate on size.

## Practice checklist

Before the exercise, confirm you can:

1. Explain "Concurrent Algorithm Drills" aloud in under two minutes without notes.
2. Re-type the worked example from memory and match the expected output.
3. Name the Go standard library packages touched by this lesson.
4. List one production bug this lesson's rules prevent.
5. Contrast the Go approach with the Python instinct listed above.
6. Write a three-line cheat sheet: one idiom, one pitfall, one command to remember.

If any item fails, re-run the mini-lab once more, then attempt the exercise tests.

## Transfer to production

Ask where this shows up outside toys: config loading, API handlers, data pipelines,
CI scripts, or on-call debugging. Write one concrete two-sentence scenario tying
the worked example to that scenario. Tomorrow, when you rewrite the exercise from
memory, check whether the code still fits that framing.
""",
            exercise_guide="""
Implement parallel aggregation matching sequential results.
""",
            exercise_examples="""
ParSum equals Sum for the same slice.
""",
        ),
        35: dict(
            body="""
## Why this matters

net/http is production-grade in the standard library. Understanding handlers, clients, and timeouts is baseline for Go services.

This lesson is a building block for later modules in the Goodway path. If you only
skim, the exercises will feel like busywork; if you type the examples and narrate
them aloud, the same patterns will reappear in HTTP handlers, concurrency, and AI
service glue.

## Core concepts

- http.HandleFunc / ServeMux route requests.
- Handlers write to ResponseWriter; read from Request.
- Clients should set Timeouts — never use bare default in prod.
- context on Request cancels when clients disconnect.
- ListenAndServe blocks; shutdown gracefully later lessons.

Hold these in working memory while you code. Each bullet should map to something
you can demonstrate with a three-line program or a failing compile error.

## Worked Go examples

Create a scratch module and type this yourself (do not paste blindly):

```bash
mkdir -p /tmp/gw-http && cd /tmp/gw-http
go mod init example.com/scratch
```

Then create `main.go`:

```go
package main

import (
    "fmt"
    "net/http"
    "net/http/httptest"
)

func health(w http.ResponseWriter, r *http.Request) {
    w.WriteHeader(http.StatusOK)
    fmt.Fprint(w, "ok")
}

func main() {
    req := httptest.NewRequest(http.MethodGet, "/healthz", nil)
    rr := httptest.NewRecorder()
    health(rr, req)
    fmt.Println(rr.Code, rr.Body.String())
}
```

Run it:

```bash
go run .
```

Expected output:

```text
200 ok
```

If your output differs, diff character-by-character — especially whitespace and
types. Then change one line deliberately and predict the new output before running.

## Mini-lab (`go run` steps)

1. Write /healthz returning 200 ok.
2. httptest a handler without listening on a port.
3. Set http.Client{Timeout: 2*time.Second}.

Write down one sentence explaining *why* the output matches the code before you move on.
Time-box the lab to 15–25 minutes; struggle is part of encoding the skill.

## Curriculum notes (expanded from the compact draft)

## Server

```go
mux := http.NewServeMux()
mux.HandleFunc("GET /health", func(w http.ResponseWriter, r *http.Request) {
    w.WriteHeader(http.StatusOK)
    _, _ = w.Write([]byte("ok"))
})
srv := &http.Server{Addr: ":8080", Handler: mux, ReadHeaderTimeout: 5 * time.Second}
log.Fatal(srv.ListenAndServe())
```

Always set timeouts. Infinite hangs are outages.

## Client

```go
client := &http.Client{Timeout: 10 * time.Second}
resp, err := client.Get(url)
```

Reuse clients; do not create one per request. Close response bodies.

## Context

`r.Context()` cancels when the client disconnects — respect it in handlers.

## Failure modes to watch while coding

- Default client with no timeout
- Ignoring resp.Body.Close()
- Blocking handler work without goroutine limits

When a test fails, ask which failure mode you hit before changing code at random.

## Idioms vs Python pitfalls

- Flask/FastAPI vs net/http — stdlib is enough for many services.
- requests defaults vs explicit Client timeouts.
- WSGI sync model vs Go's per-request goroutines.

When you catch yourself reaching for a Python habit, pause and rewrite the Go way
once on purpose — even if both would "work". The goal is a Go-shaped intuition.

## Going deeper

Always set timeouts on http.Client in production. Prefer httptest for handler unit tests so CI needs no open ports.

## Practice checklist

Before the exercise, confirm you can:

1. Explain "HTTP Servers and Clients (net/http)" aloud in under two minutes without notes.
2. Re-type the worked example from memory and match the expected output.
3. Name the Go standard library packages touched by this lesson.
4. List one production bug this lesson's rules prevent.
5. Contrast the Go approach with the Python instinct listed above.
6. Write a three-line cheat sheet: one idiom, one pitfall, one command to remember.

If any item fails, re-run the mini-lab once more, then attempt the exercise tests.

## Transfer to production

Ask where this shows up outside toys: config loading, API handlers, data pipelines,
CI scripts, or on-call debugging. Write one concrete two-sentence scenario tying
the worked example to that scenario. Tomorrow, when you rewrite the exercise from
memory, check whether the code still fits that framing.
""",
            exercise_guide="""
Implement a health handler (or client helper) so tests get 200/ok bodies.
""",
            exercise_examples="""
GET health returns status 200 and body matching tests.
""",
        ),
        36: dict(
            body="""
## Why this matters

REST middleware and auth are how you cross-cut logging, authn, and limits without copying code into every handler.

This lesson is a building block for later modules in the Goodway path. If you only
skim, the exercises will feel like busywork; if you type the examples and narrate
them aloud, the same patterns will reappear in HTTP handlers, concurrency, and AI
service glue.

## Core concepts

- Middleware is `func(http.Handler) http.Handler`.
- Chain middleware outward-in carefully.
- Auth: validate tokens/headers early; set context values sparingly.
- Return proper status codes: 401/403/400 distinctions.
- Keep handlers thin: decode → validate → service → encode.

Hold these in working memory while you code. Each bullet should map to something
you can demonstrate with a three-line program or a failing compile error.

## Worked Go examples

Create a scratch module and type this yourself (do not paste blindly):

```bash
mkdir -p /tmp/gw-rest && cd /tmp/gw-rest
go mod init example.com/scratch
```

Then create `main.go`:

```go
package main

import (
    "fmt"
    "net/http"
    "net/http/httptest"
)

func withHeader(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        w.Header().Set("X-Demo", "1")
        next.ServeHTTP(w, r)
    })
}

func main() {
    h := withHeader(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        fmt.Fprint(w, "hi")
    }))
    rr := httptest.NewRecorder()
    h.ServeHTTP(rr, httptest.NewRequest(http.MethodGet, "/", nil))
    fmt.Println(rr.Header().Get("X-Demo"), rr.Body.String())
}
```

Run it:

```bash
go run .
```

Expected output:

```text
1 hi
```

If your output differs, diff character-by-character — especially whitespace and
types. Then change one line deliberately and predict the new output before running.

## Mini-lab (`go run` steps)

1. Write middleware that rejects missing Authorization.
2. Chain logging + auth middleware.
3. Map service errors to HTTP statuses.

Write down one sentence explaining *why* the output matches the code before you move on.
Time-box the lab to 15–25 minutes; struggle is part of encoding the skill.

## Curriculum notes (expanded from the compact draft)

## REST sketch

- `GET /items` list
- `GET /items/{id}` get
- `POST /items` create
- `DELETE /items/{id}` delete

Use proper status codes: 201 create, 404 missing, 400 validation, 401/403 auth.

## Middleware

```go
func WithRequestID(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        id := r.Header.Get("X-Request-ID")
        if id == "" { id = uuidNew() }
        ctx := context.WithValue(r.Context(), ctxKeyID, id)
        w.Header().Set("X-Request-ID", id)
        next.ServeHTTP(w, r.WithContext(ctx))
    })
}
```

## Auth basics

Validate `Authorization` header; never roll crypto casually — use proven libraries.
Separate authentication (who) from authorization (what allowed).

## Failure modes to watch while coding

- Leaking stack traces to clients
- Auth only on some routes by accident
- Using GET for state changes

When a test fails, ask which failure mode you hit before changing code at random.

## Idioms vs Python pitfalls

- Decorators ≈ middleware.
- Flask before_request hooks ≈ middleware chains.
- Keep crypto out of handlers — use small auth packages.

When you catch yourself reaching for a Python habit, pause and rewrite the Go way
once on purpose — even if both would "work". The goal is a Go-shaped intuition.

## Going deeper

Prefer explicit dependency injection of auth services over global state.

## Practice checklist

Before the exercise, confirm you can:

1. Explain "REST API Design, Middleware, Auth Basics" aloud in under two minutes without notes.
2. Re-type the worked example from memory and match the expected output.
3. Name the Go standard library packages touched by this lesson.
4. List one production bug this lesson's rules prevent.
5. Contrast the Go approach with the Python instinct listed above.
6. Write a three-line cheat sheet: one idiom, one pitfall, one command to remember.

If any item fails, re-run the mini-lab once more, then attempt the exercise tests.

## Transfer to production

Ask where this shows up outside toys: config loading, API handlers, data pipelines,
CI scripts, or on-call debugging. Write one concrete two-sentence scenario tying
the worked example to that scenario. Tomorrow, when you rewrite the exercise from
memory, check whether the code still fits that framing.
""",
            exercise_guide="""
Implement middleware that enforces headers/auth as tests describe.
""",
            exercise_examples="""
Missing token → 401; valid → handler body.
""",
        ),
        37: dict(
            body="""
## Why this matters

gRPC and protobuf give typed, efficient RPCs across languages. Go is a first-class citizen in that ecosystem.

This lesson is a building block for later modules in the Goodway path. If you only
skim, the exercises will feel like busywork; if you type the examples and narrate
them aloud, the same patterns will reappear in HTTP handlers, concurrency, and AI
service glue.

## Core concepts

- Protobuf defines messages and services in .proto files.
- protoc + plugins generate Go types and stubs.
- gRPC supports unary and streaming RPCs.
- Errors use status codes, not only ad-hoc strings.
- Version your APIs; avoid breaking field numbers.

Hold these in working memory while you code. Each bullet should map to something
you can demonstrate with a three-line program or a failing compile error.

## Worked Go examples

Create a scratch module and type this yourself (do not paste blindly):

```bash
mkdir -p /tmp/gw-grpc && cd /tmp/gw-grpc
go mod init example.com/scratch
```

Then create `main.go`:

```go
package main

import "fmt"

// Conceptual: generated code looks like this shape.
type HelloRequest struct{ Name string }
type HelloReply struct{ Message string }

func SayHello(req HelloRequest) HelloReply {
    return HelloReply{Message: "hello " + req.Name}
}

func main() { fmt.Println(SayHello(HelloRequest{Name: "Ada"}).Message) }
```

Run it:

```bash
go run .
```

Expected output:

```text
hello Ada
```

If your output differs, diff character-by-character — especially whitespace and
types. Then change one line deliberately and predict the new output before running.

## Mini-lab (`go run` steps)

1. Skim a .proto example online and map fields to Go structs.
2. Implement a pure Go stand-in for a unary RPC handler.
3. List three gRPC status codes you would use.

Write down one sentence explaining *why* the output matches the code before you move on.
Time-box the lab to 15–25 minutes; struggle is part of encoding the skill.

## Curriculum notes (expanded from the compact draft)

## Why gRPC?

- Strongly typed contracts (`.proto`)
- Efficient binary encoding
- Streaming RPCs
- First-class deadlines/status codes

## Flow

1. Write `service.proto`
2. Generate Go with `protoc` / `buf`
3. Implement server interface
4. Dial with client stubs

## vs REST/JSON

Use gRPC for internal service meshes and streaming; REST/JSON for public browser-facing APIs often still wins.

Contexts carry deadlines across gRPC calls — wire them end-to-end.

## Failure modes to watch while coding

- Exposing gRPC directly to browsers without grpc-web/gateway
- Ignoring status codes (use codes.NotFound etc.)
- Huge protobuf messages without pagination

When a test fails, ask which failure mode you hit before changing code at random.

## Idioms vs Python pitfalls

- grpcio similar concepts; generated stubs differ.
- dict payloads vs typed protobuf messages.
- Field numbers are the compatibility contract — like JSON keys but stricter.

When you catch yourself reaching for a Python habit, pause and rewrite the Go way
once on purpose — even if both would "work". The goal is a Go-shaped intuition.

## Going deeper

Start with unary RPCs; add streaming when a real need appears.

## Practice checklist

Before the exercise, confirm you can:

1. Explain "gRPC and Protobuf Intro" aloud in under two minutes without notes.
2. Re-type the worked example from memory and match the expected output.
3. Name the Go standard library packages touched by this lesson.
4. List one production bug this lesson's rules prevent.
5. Contrast the Go approach with the Python instinct listed above.
6. Write a three-line cheat sheet: one idiom, one pitfall, one command to remember.

If any item fails, re-run the mini-lab once more, then attempt the exercise tests.

## Transfer to production

Ask where this shows up outside toys: config loading, API handlers, data pipelines,
CI scripts, or on-call debugging. Write one concrete two-sentence scenario tying
the worked example to that scenario. Tomorrow, when you rewrite the exercise from
memory, check whether the code still fits that framing.
""",
            exercise_guide="""
Implement the sketch/stub service method the tests call.
""",
            exercise_examples="""
SayHello-style funcs return expected messages.
""",
        ),
        38: dict(
            body="""
## Why this matters

database/sql is a toolkit, not an ORM. Correct parameters, transactions, and connection pools keep data safe under concurrency.

This lesson is a building block for later modules in the Goodway path. If you only
skim, the exercises will feel like busywork; if you type the examples and narrate
them aloud, the same patterns will reappear in HTTP handlers, concurrency, and AI
service glue.

## Core concepts

- Use placeholders `?`/`$1` — never string-build SQL.
- Query/QueryRow/Exec and always check errors.
- Tx: Begin → work → Commit/Rollback.
- sql.DB is a pool; SetMaxOpenConns thoughtfully.
- Scan into variables carefully; NULL needs sql.Null*.

Hold these in working memory while you code. Each bullet should map to something
you can demonstrate with a three-line program or a failing compile error.

## Worked Go examples

Create a scratch module and type this yourself (do not paste blindly):

```bash
mkdir -p /tmp/gw-databases: && cd /tmp/gw-databases:
go mod init example.com/scratch
```

Then create `main.go`:

```go
package main

import "fmt"

// Conceptual parameterized query shape:
func FindName(id int) string {
    // db.QueryRow("SELECT name FROM users WHERE id=$1", id).Scan(&name)
    _ = id
    return "Ada"
}

func main() { fmt.Println(FindName(1)) }
```

Run it:

```bash
go run .
```

Expected output:

```text
Ada
```

If your output differs, diff character-by-character — especially whitespace and
types. Then change one line deliberately and predict the new output before running.

## Mini-lab (`go run` steps)

1. Write a function that takes query args separately from SQL.
2. Sketch transaction rollback on error.
3. List what happens if you ignore Rows.Err().

Write down one sentence explaining *why* the output matches the code before you move on.
Time-box the lab to 15–25 minutes; struggle is part of encoding the skill.

## Curriculum notes (expanded from the compact draft)

## database/sql

```go
db, err := sql.Open("pgx", dsn)
db.SetMaxOpenConns(20)
row := db.QueryRowContext(ctx, `SELECT name FROM users WHERE id=$1`, id)
```

Always use contexts and placeholders — never string-concatenate user input into SQL.

## Transactions

```go
tx, err := db.BeginTx(ctx, nil)
defer tx.Rollback()
// execs...
return tx.Commit()
```

## Migrations

Treat schema as versioned code (golang-migrate, goose, atlas). Expand/contract for zero-downtime.

## Failure modes to watch while coding

- sql.Open without Ping
- Holding transactions open during HTTP calls to others
- SELECT * forever

When a test fails, ask which failure mode you hit before changing code at random.

## Idioms vs Python pitfalls

- DB-API placeholders ≈ Go's — still don't f-string SQL.
- ORMs hide pools; learn sql.DB semantics anyway.
- context.Context on QueryContext for timeouts.

When you catch yourself reaching for a Python habit, pause and rewrite the Go way
once on purpose — even if both would "work". The goal is a Go-shaped intuition.

## Going deeper

Migrations belong in versioned files; apps should not ad-hoc ALTER in request paths.

## Practice checklist

Before the exercise, confirm you can:

1. Explain "Databases: SQL Drivers, Transactions, Migrations" aloud in under two minutes without notes.
2. Re-type the worked example from memory and match the expected output.
3. Name the Go standard library packages touched by this lesson.
4. List one production bug this lesson's rules prevent.
5. Contrast the Go approach with the Python instinct listed above.
6. Write a three-line cheat sheet: one idiom, one pitfall, one command to remember.

If any item fails, re-run the mini-lab once more, then attempt the exercise tests.

## Transfer to production

Ask where this shows up outside toys: config loading, API handlers, data pipelines,
CI scripts, or on-call debugging. Write one concrete two-sentence scenario tying
the worked example to that scenario. Tomorrow, when you rewrite the exercise from
memory, check whether the code still fits that framing.
""",
            exercise_guide="""
Implement parameterized helpers / scans as the exercise defines.
""",
            exercise_examples="""
Queries use args slices; tests check SQL shape or results mocks.
""",
        ),
        39: dict(
            body="""
## Why this matters

Caching and idempotency protect databases and make retries safe. Cache-aside and Redis patterns appear in every production stack.

This lesson is a building block for later modules in the Goodway path. If you only
skim, the exercises will feel like busywork; if you type the examples and narrate
them aloud, the same patterns will reappear in HTTP handlers, concurrency, and AI
service glue.

## Core concepts

- Cache-aside: read cache → miss → load DB → fill cache.
- Set TTLs; plan invalidation on writes.
- Idempotency keys dedupe retried side effects.
- Stampede protection: singleflight or locks.
- Redis is a tool — model keys carefully with namespaces.

Hold these in working memory while you code. Each bullet should map to something
you can demonstrate with a three-line program or a failing compile error.

## Worked Go examples

Create a scratch module and type this yourself (do not paste blindly):

```bash
mkdir -p /tmp/gw-caching, && cd /tmp/gw-caching,
go mod init example.com/scratch
```

Then create `main.go`:

```go
package main

import "fmt"

func CacheAside(mem map[string]string, key string, load func() string) string {
    if v, ok := mem[key]; ok {
        return v
    }
    v := load()
    mem[key] = v
    return v
}

func main() {
    mem := map[string]string{}
    loads := 0
    get := func() string {
        loads++
        return "v"
    }
    fmt.Println(CacheAside(mem, "a", get), CacheAside(mem, "a", get), loads)
}
```

Run it:

```bash
go run .
```

Expected output:

```text
v v 1
```

If your output differs, diff character-by-character — especially whitespace and
types. Then change one line deliberately and predict the new output before running.

## Mini-lab (`go run` steps)

1. Implement in-memory cache-aside.
2. Add TTL by storing expiry time.
3. Simulate retries with an idempotency set.

Write down one sentence explaining *why* the output matches the code before you move on.
Time-box the lab to 15–25 minutes; struggle is part of encoding the skill.

## Curriculum notes (expanded from the compact draft)

## Cache-aside

1. Read cache
2. On miss: read DB, populate cache
3. On write: update DB, invalidate key

## Redis roles

- Cache
- Rate limiting
- Distributed locks (carefully)
- Queues / streams

## Idempotency

For payment-like POSTs, clients send `Idempotency-Key`. Server stores result of first processing and replays it — critical for at-least-once delivery worlds.

## Thundering herd

When hot key expires, many requests hit DB. Mitigate with singleflight / locking / soft expiry.

## Failure modes to watch while coding

- Caching without TTL
- Using Redis locks without expiry
- Assuming cache is always consistent with DB

When a test fails, ask which failure mode you hit before changing code at random.

## Idioms vs Python pitfalls

- functools.cache / Redis clients — same patterns.
- Mutable default dicts vs make(map).
- Think about consistency: cache can be stale.

When you catch yourself reaching for a Python habit, pause and rewrite the Go way
once on purpose — even if both would "work". The goal is a Go-shaped intuition.

## Going deeper

Document consistency: stale reads vs always-fresh after write.

## Practice checklist

Before the exercise, confirm you can:

1. Explain "Caching, Redis Patterns, Idempotency" aloud in under two minutes without notes.
2. Re-type the worked example from memory and match the expected output.
3. Name the Go standard library packages touched by this lesson.
4. List one production bug this lesson's rules prevent.
5. Contrast the Go approach with the Python instinct listed above.
6. Write a three-line cheat sheet: one idiom, one pitfall, one command to remember.

If any item fails, re-run the mini-lab once more, then attempt the exercise tests.

## Transfer to production

Ask where this shows up outside toys: config loading, API handlers, data pipelines,
CI scripts, or on-call debugging. Write one concrete two-sentence scenario tying
the worked example to that scenario. Tomorrow, when you rewrite the exercise from
memory, check whether the code still fits that framing.
""",
            exercise_guide="""
Implement cache-aside or idempotency stub per tests.
""",
            exercise_examples="""
Second read does not re-load; idempotent submit once.
""",
        ),
        40: dict(
            body="""
## Why this matters

Logs, metrics, and traces explain production. Structured observability turns incidents from guesswork into evidence.

This lesson is a building block for later modules in the Goodway path. If you only
skim, the exercises will feel like busywork; if you type the examples and narrate
them aloud, the same patterns will reappear in HTTP handlers, concurrency, and AI
service glue.

## Core concepts

- Structured logs: key=value or JSON fields.
- Metrics: counters, histograms, gauges.
- Traces: spans across services with context propagation.
- Correlate with request IDs.
- Cardinality kills metrics systems — label carefully.

Hold these in working memory while you code. Each bullet should map to something
you can demonstrate with a three-line program or a failing compile error.

## Worked Go examples

Create a scratch module and type this yourself (do not paste blindly):

```bash
mkdir -p /tmp/gw-observabilit && cd /tmp/gw-observabilit
go mod init example.com/scratch
```

Then create `main.go`:

```go
package main

import (
    "log/slog"
    "os"
)

func main() {
    logger := slog.New(slog.NewJSONHandler(os.Stdout, nil))
    logger.Info("request done", "route", "/health", "ms", 3)
}
```

Run it:

```bash
go run .
```

Expected output:

```text
{"time":"...","level":"INFO","msg":"request done","route":"/health","ms":3}
```

If your output differs, diff character-by-character — especially whitespace and
types. Then change one line deliberately and predict the new output before running.

## Mini-lab (`go run` steps)

1. Log with slog JSON handler.
2. Increment a conceptual counter around a function.
3. Pass a request ID through context (sketch).

Write down one sentence explaining *why* the output matches the code before you move on.
Time-box the lab to 15–25 minutes; struggle is part of encoding the skill.

## Curriculum notes (expanded from the compact draft)

## Three pillars

- **Logs**: discrete events (structured JSON)
- **Metrics**: aggregates (counters, histograms)
- **Traces**: request journeys across services

```go
slog.Info("request completed", "method", r.Method, "path", r.URL.Path, "status", status, "dur_ms", ms)
```

## Metrics that matter

For services: rate, errors, duration (RED). Histograms for latency percentiles.

## Tracing

Pass trace context in headers; OpenTelemetry is the common standard. Sample wisely in production.

## Failure modes to watch while coding

- Println debugging as the only strategy
- High-cardinality metric labels (user IDs)
- Logging secrets/PII

When a test fails, ask which failure mode you hit before changing code at random.

## Idioms vs Python pitfalls

- logging/structlog ≈ slog.
- Prometheus client patterns similar.
- Print debugging does not scale — structure early.

When you catch yourself reaching for a Python habit, pause and rewrite the Go way
once on purpose — even if both would "work". The goal is a Go-shaped intuition.

## Going deeper

ALERT on symptoms (error rate, latency) not only causes.

## Practice checklist

Before the exercise, confirm you can:

1. Explain "Observability: Logs, Metrics, Tracing" aloud in under two minutes without notes.
2. Re-type the worked example from memory and match the expected output.
3. Name the Go standard library packages touched by this lesson.
4. List one production bug this lesson's rules prevent.
5. Contrast the Go approach with the Python instinct listed above.
6. Write a three-line cheat sheet: one idiom, one pitfall, one command to remember.

If any item fails, re-run the mini-lab once more, then attempt the exercise tests.

## Transfer to production

Ask where this shows up outside toys: config loading, API handlers, data pipelines,
CI scripts, or on-call debugging. Write one concrete two-sentence scenario tying
the worked example to that scenario. Tomorrow, when you rewrite the exercise from
memory, check whether the code still fits that framing.
""",
            exercise_guide="""
Implement logging helper or metric wrapper the tests expect.
""",
            exercise_examples="""
Logs contain required fields; helpers format consistently.
""",
        ),
        41: dict(
            body="""
## Why this matters

Multi-stage Docker builds keep Go images tiny and secure. Containers are how Go services ship.

This lesson is a building block for later modules in the Goodway path. If you only
skim, the exercises will feel like busywork; if you type the examples and narrate
them aloud, the same patterns will reappear in HTTP handlers, concurrency, and AI
service glue.

## Core concepts

- Build stage with golang image; runtime with distroless/scratch/alpine.
- COPY go.mod/sum first for layer caching.
- CGO_ENABLED=0 for static binaries when possible.
- Run as non-root; expose minimal ports.
- Healthchecks and read-only rootfs where practical.

Hold these in working memory while you code. Each bullet should map to something
you can demonstrate with a three-line program or a failing compile error.

## Worked Go examples

Create a scratch module and type this yourself (do not paste blindly):

```bash
mkdir -p /tmp/gw-containers && cd /tmp/gw-containers
go mod init example.com/scratch
```

Then create `main.go`:

```go
package main

import "fmt"

func main() {
    // Inside container this binary is often /app
    fmt.Println("listening :8080")
}
```

Run it:

```bash
go run .
```

Expected output:

```text
listening :8080
```

If your output differs, diff character-by-character — especially whitespace and
types. Then change one line deliberately and predict the new output before running.

## Mini-lab (`go run` steps)

1. Write a multi-stage Dockerfile sketch on paper.
2. List what NOT to COPY (secrets, .git).
3. Explain why go mod download is a separate layer.

Write down one sentence explaining *why* the output matches the code before you move on.
Time-box the lab to 15–25 minutes; struggle is part of encoding the skill.

## Curriculum notes (expanded from the compact draft)

## Multi-stage pattern

```dockerfile
FROM golang:1.22 AS build
WORKDIR /src
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 go build -o /out/app ./cmd/api

FROM gcr.io/distroless/static:nonroot
COPY --from=build /out/app /app
USER nonroot:nonroot
ENTRYPOINT ["/app"]
```

## Why

- Tiny attack surface
- Reproducible builds
- Same artifact from laptop to prod

Pin base image digests in serious deployments. Pass version via ldflags.

## Failure modes to watch while coding

- Shipping build toolchain in prod image
- Running as root
- COPY . . before go mod download (breaks cache)

When a test fails, ask which failure mode you hit before changing code at random.

## Idioms vs Python pitfalls

- venv in images vs static Go binaries — Go wins size often.
- Same Docker layer caching ideas.
- GIL/process model differs; still one process per container usually.

When you catch yourself reaching for a Python habit, pause and rewrite the Go way
once on purpose — even if both would "work". The goal is a Go-shaped intuition.

## Going deeper

Pin base image digests for supply-chain hygiene.

## Practice checklist

Before the exercise, confirm you can:

1. Explain "Containers and Multi-stage Docker Builds for Go" aloud in under two minutes without notes.
2. Re-type the worked example from memory and match the expected output.
3. Name the Go standard library packages touched by this lesson.
4. List one production bug this lesson's rules prevent.
5. Contrast the Go approach with the Python instinct listed above.
6. Write a three-line cheat sheet: one idiom, one pitfall, one command to remember.

If any item fails, re-run the mini-lab once more, then attempt the exercise tests.

## Transfer to production

Ask where this shows up outside toys: config loading, API handlers, data pipelines,
CI scripts, or on-call debugging. Write one concrete two-sentence scenario tying
the worked example to that scenario. Tomorrow, when you rewrite the exercise from
memory, check whether the code still fits that framing.
""",
            exercise_guide="""
Complete Dockerfile-oriented stubs or config strings tests check.
""",
            exercise_examples="""
Multi-stage markers / binary path expectations in tests.
""",
        ),
        42: dict(
            body="""
## Why this matters

Kubernetes controllers reconcile desired vs actual state. Go and client-go dominate this ecosystem.

This lesson is a building block for later modules in the Goodway path. If you only
skim, the exercises will feel like busywork; if you type the examples and narrate
them aloud, the same patterns will reappear in HTTP handlers, concurrency, and AI
service glue.

## Core concepts

- Reconcile loops: read state → diff → act → repeat.
- Informers/caches reduce API server load.
- Idempotent actions: safe to retry.
- Status subresources report progress.
- Leader election for active/passive controllers.

Hold these in working memory while you code. Each bullet should map to something
you can demonstrate with a three-line program or a failing compile error.

## Worked Go examples

Create a scratch module and type this yourself (do not paste blindly):

```bash
mkdir -p /tmp/gw-kubernetes-o && cd /tmp/gw-kubernetes-o
go mod init example.com/scratch
```

Then create `main.go`:

```go
package main

import "fmt"

func Reconcile(desired, actual int) string {
    if actual == desired {
        return "ok"
    }
    return "update"
}

func main() { fmt.Println(Reconcile(3, 1)) }
```

Run it:

```bash
go run .
```

Expected output:

```text
update
```

If your output differs, diff character-by-character — especially whitespace and
types. Then change one line deliberately and predict the new output before running.

## Mini-lab (`go run` steps)

1. Write a pure reconcile decision function.
2. List what makes an action idempotent.
3. Sketch an informer event → queue → worker.

Write down one sentence explaining *why* the output matches the code before you move on.
Time-box the lab to 15–25 minutes; struggle is part of encoding the skill.

## Curriculum notes (expanded from the compact draft)

## Control loop

Kubernetes controllers observe desired state (spec) and drive actual state toward it — continuously.

```
for {
  desired := getSpec()
  actual := getStatus()
  if actual != desired { act() }
}
```

## client-go concepts

Informers/caches reduce API spam; workqueues debounce; reconcile must be idempotent.

## Operators

Encode domain ops knowledge as controllers. Go dominates this ecosystem.

You do not need a cluster for the exercise — implement a tiny reconcile function over an in-memory store.

## Failure modes to watch while coding

- One-shot scripts instead of reconcile loops
- Non-idempotent reconciles
- Hot-looping without backoff

When a test fails, ask which failure mode you hit before changing code at random.

## Idioms vs Python pitfalls

- Operators exist in other langs; Go is the default for k8s.
- Same reconcile idea as config management loops.
- Watch API vs poll — prefer events with resync.

When you catch yourself reaching for a Python habit, pause and rewrite the Go way
once on purpose — even if both would "work". The goal is a Go-shaped intuition.

## Going deeper

Never block forever in reconcile without context; requeue with backoff.

## Practice checklist

Before the exercise, confirm you can:

1. Explain "Kubernetes-Oriented Go: Controllers and client-go" aloud in under two minutes without notes.
2. Re-type the worked example from memory and match the expected output.
3. Name the Go standard library packages touched by this lesson.
4. List one production bug this lesson's rules prevent.
5. Contrast the Go approach with the Python instinct listed above.
6. Write a three-line cheat sheet: one idiom, one pitfall, one command to remember.

If any item fails, re-run the mini-lab once more, then attempt the exercise tests.

## Transfer to production

Ask where this shows up outside toys: config loading, API handlers, data pipelines,
CI scripts, or on-call debugging. Write one concrete two-sentence scenario tying
the worked example to that scenario. Tomorrow, when you rewrite the exercise from
memory, check whether the code still fits that framing.
""",
            exercise_guide="""
Implement reconcile decision stubs matching tests.
""",
            exercise_examples="""
desired==actual → ok; else → update action.
""",
        ),
        43: dict(
            body="""
## Why this matters

Cloud SDKs need retries, pagination, and config from env. Robust clients survive transient faults.

This lesson is a building block for later modules in the Goodway path. If you only
skim, the exercises will feel like busywork; if you type the examples and narrate
them aloud, the same patterns will reappear in HTTP handlers, concurrency, and AI
service glue.

## Core concepts

- Retry transient errors with exponential backoff + jitter.
- Pagination: loop until next token empty.
- Config via env/flags; never hardcode secrets.
- Idempotent retries for safe verbs.
- Timeouts on every outbound call.

Hold these in working memory while you code. Each bullet should map to something
you can demonstrate with a three-line program or a failing compile error.

## Worked Go examples

Create a scratch module and type this yourself (do not paste blindly):

```bash
mkdir -p /tmp/gw-cloud && cd /tmp/gw-cloud
go mod init example.com/scratch
```

Then create `main.go`:

```go
package main

import (
    "fmt"
    "math"
)

func Backoff(attempt int, baseMs float64) float64 {
    return baseMs * math.Pow(2, float64(attempt))
}

func main() {
    for i := 0; i < 4; i++ {
        fmt.Println(Backoff(i, 100))
    }
}
```

Run it:

```bash
go run .
```

Expected output:

```text
100
200
400
800
```

If your output differs, diff character-by-character — especially whitespace and
types. Then change one line deliberately and predict the new output before running.

## Mini-lab (`go run` steps)

1. Implement backoff with max cap.
2. Paginate a fake NextToken API.
3. Read a config struct from env vars.

Write down one sentence explaining *why* the output matches the code before you move on.
Time-box the lab to 15–25 minutes; struggle is part of encoding the skill.

## Curriculum notes (expanded from the compact draft)

## Retries

Retry transient errors (timeouts, 429, 503), not validation errors.
Exponential backoff with jitter prevents synchronized stampedes.

```go
func Retry(ctx context.Context, fn func() error) error {
    // backoff loop checking ctx.Done()
}
```

## Pagination

Most list APIs return a cursor/token. Loop until empty. Bound max pages.

## Config

Prefer IAM roles / workload identity over long-lived keys in files.
Separate config loading from business logic for tests.

## Failure modes to watch while coding

- Infinite retries without deadline
- Retrying non-idempotent POSTs blindly
- Loading all pages into memory without need

When a test fails, ask which failure mode you hit before changing code at random.

## Idioms vs Python pitfalls

- tenacity ≈ custom backoff in Go.
- boto3 pagination ≈ token loops.
- Same twelve-factor config ideals.

When you catch yourself reaching for a Python habit, pause and rewrite the Go way
once on purpose — even if both would "work". The goal is a Go-shaped intuition.

## Going deeper

Distinguish retryable (429/5xx) from permanent (400) errors.

## Practice checklist

Before the exercise, confirm you can:

1. Explain "Cloud SDK Patterns: Config, Retries, Pagination" aloud in under two minutes without notes.
2. Re-type the worked example from memory and match the expected output.
3. Name the Go standard library packages touched by this lesson.
4. List one production bug this lesson's rules prevent.
5. Contrast the Go approach with the Python instinct listed above.
6. Write a three-line cheat sheet: one idiom, one pitfall, one command to remember.

If any item fails, re-run the mini-lab once more, then attempt the exercise tests.

## Transfer to production

Ask where this shows up outside toys: config loading, API handlers, data pipelines,
CI scripts, or on-call debugging. Write one concrete two-sentence scenario tying
the worked example to that scenario. Tomorrow, when you rewrite the exercise from
memory, check whether the code still fits that framing.
""",
            exercise_guide="""
Implement retry/backoff helper per tests.
""",
            exercise_examples="""
Attempt n waits base*2^n (or as specified).
""",
        ),
        44: dict(
            body="""
## Why this matters

Reliability patterns — timeouts, circuit breakers, graceful shutdown — keep incidents small and deploys safe.

This lesson is a building block for later modules in the Goodway path. If you only
skim, the exercises will feel like busywork; if you type the examples and narrate
them aloud, the same patterns will reappear in HTTP handlers, concurrency, and AI
service glue.

## Core concepts

- Timeouts everywhere: clients, servers, DB.
- Circuit breakers stop calling unhealthy deps.
- Graceful shutdown: stop intake, drain, then exit.
- signal.Notify for SIGTERM in containers.
- Load shedding beats cascading failure.

Hold these in working memory while you code. Each bullet should map to something
you can demonstrate with a three-line program or a failing compile error.

## Worked Go examples

Create a scratch module and type this yourself (do not paste blindly):

```bash
mkdir -p /tmp/gw-reliability: && cd /tmp/gw-reliability:
go mod init example.com/scratch
```

Then create `main.go`:

```go
package main

import (
    "fmt"
    "time"
)

func main() {
    stop := make(chan struct{})
    go func() {
        time.Sleep(20 * time.Millisecond)
        close(stop)
    }()
    select {
    case <-stop:
        fmt.Println("shutdown")
    case <-time.After(time.Second):
        fmt.Println("timeout")
    }
}
```

Run it:

```bash
go run .
```

Expected output:

```text
shutdown
```

If your output differs, diff character-by-character — especially whitespace and
types. Then change one line deliberately and predict the new output before running.

## Mini-lab (`go run` steps)

1. Simulate SIGTERM with a cancel channel.
2. Add a timeout around a slow function.
3. Sketch circuit breaker states: closed/open/half-open.

Write down one sentence explaining *why* the output matches the code before you move on.
Time-box the lab to 15–25 minutes; struggle is part of encoding the skill.

## Curriculum notes (expanded from the compact draft)

## Timeouts

Every external call needs a deadline. Inherit from request context when serving HTTP.

## Circuit breaker

When dependency error rate spikes, fail fast temporarily to allow recovery — then probe half-open.

## Graceful shutdown

```go
go func() { _ = srv.ListenAndServe() }()
<-stop
ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
defer cancel()
_ = srv.Shutdown(ctx)
```

Drain in-flight requests; stop accepting new ones.

## SLO mindset

Availability and latency targets drive timeout budgets and retry policies.

## Failure modes to watch while coding

- Kill -9 as the only deploy strategy
- No timeout on outbound calls
- Circuit breaker without metrics

When a test fails, ask which failure mode you hit before changing code at random.

## Idioms vs Python pitfalls

- signal handling similar; asyncio cancellation related.
- Flask often lacks std graceful shutdown — learn Go's.
- Fail-fast vs retry — product decision.

When you catch yourself reaching for a Python habit, pause and rewrite the Go way
once on purpose — even if both would "work". The goal is a Go-shaped intuition.

## Going deeper

Kubernetes sends SIGTERM then SIGKILL — drain within terminationGracePeriodSeconds.

## Practice checklist

Before the exercise, confirm you can:

1. Explain "Reliability: Timeouts, Circuit Breakers, Graceful Shutdown" aloud in under two minutes without notes.
2. Re-type the worked example from memory and match the expected output.
3. Name the Go standard library packages touched by this lesson.
4. List one production bug this lesson's rules prevent.
5. Contrast the Go approach with the Python instinct listed above.
6. Write a three-line cheat sheet: one idiom, one pitfall, one command to remember.

If any item fails, re-run the mini-lab once more, then attempt the exercise tests.

## Transfer to production

Ask where this shows up outside toys: config loading, API handlers, data pipelines,
CI scripts, or on-call debugging. Write one concrete two-sentence scenario tying
the worked example to that scenario. Tomorrow, when you rewrite the exercise from
memory, check whether the code still fits that framing.
""",
            exercise_guide="""
Implement shutdown/timeout helpers so tests observe clean stops.
""",
            exercise_examples="""
After stop signal, function returns promptly.
""",
        ),
        45: dict(
            body="""
## Why this matters

Numerics with gonum enable scientific and ML-adjacent work in Go: vectors, matrices, and stats without leaving the language.

This lesson is a building block for later modules in the Goodway path. If you only
skim, the exercises will feel like busywork; if you type the examples and narrate
them aloud, the same patterns will reappear in HTTP handlers, concurrency, and AI
service glue.

## Core concepts

- Vectors/matrices are first-class for linear algebra.
- Dot products and norms appear in similarity search.
- Floating error: use tolerances in tests.
- Prefer well-tested libraries over hand-rolled BLAS.
- Shape mismatches should error early.

Hold these in working memory while you code. Each bullet should map to something
you can demonstrate with a three-line program or a failing compile error.

## Worked Go examples

Create a scratch module and type this yourself (do not paste blindly):

```bash
mkdir -p /tmp/gw-numerics && cd /tmp/gw-numerics
go mod init example.com/scratch
```

Then create `main.go`:

```go
package main

import "fmt"

func Dot(a, b []float64) float64 {
    var s float64
    for i := range a {
        s += a[i] * b[i]
    }
    return s
}

func main() { fmt.Println(Dot([]float64{1, 2}, []float64{3, 4})) }
```

Run it:

```bash
go run .
```

Expected output:

```text
11
```

If your output differs, diff character-by-character — especially whitespace and
types. Then change one line deliberately and predict the new output before running.

## Mini-lab (`go run` steps)

1. Implement Dot and L2 norm.
2. Test with an epsilon comparison.
3. Multiply a tiny matrix by a vector by hand in Go.

Write down one sentence explaining *why* the output matches the code before you move on.
Time-box the lab to 15–25 minutes; struggle is part of encoding the skill.

## Curriculum notes (expanded from the compact draft)

## Floating point

Floats are approximations. Never compare with `==` without tolerance.
Summation order changes results; catastrophic cancellation is real.

## gonum

The gonum organization provides matrices, stats, graph, optimize packages — Go's scientific backbone.

```go
// Dot product
func Dot(a, b []float64) float64 {
    var s float64
    for i := range a { s += a[i] * b[i] }
    return s
}
```

## AI relevance

Even when models run elsewhere, Go services still normalize features, compute similarities, and batch tensors as bytes.

## Failure modes to watch while coding

- Equality checks on floats
- Ignoring NaN propagation
- Using float32 without need then losing precision

When a test fails, ask which failure mode you hit before changing code at random.

## Idioms vs Python pitfalls

- numpy is richer; Go/gonum is explicit and deployable in one binary.
- Broadcasting magic vs explicit loops — clarity wins in Go.
- Same floating-point caveats.

When you catch yourself reaching for a Python habit, pause and rewrite the Go way
once on purpose — even if both would "work". The goal is a Go-shaped intuition.

## Going deeper

For heavy training, Python/CUDA still dominates; Go shines at serving and glue.

## Practice checklist

Before the exercise, confirm you can:

1. Explain "Numerics and Tensors in Go (gonum)" aloud in under two minutes without notes.
2. Re-type the worked example from memory and match the expected output.
3. Name the Go standard library packages touched by this lesson.
4. List one production bug this lesson's rules prevent.
5. Contrast the Go approach with the Python instinct listed above.
6. Write a three-line cheat sheet: one idiom, one pitfall, one command to remember.

If any item fails, re-run the mini-lab once more, then attempt the exercise tests.

## Transfer to production

Ask where this shows up outside toys: config loading, API handlers, data pipelines,
CI scripts, or on-call debugging. Write one concrete two-sentence scenario tying
the worked example to that scenario. Tomorrow, when you rewrite the exercise from
memory, check whether the code still fits that framing.
""",
            exercise_guide="""
Implement Dot (or gonum-backed stub) matching tests.
""",
            exercise_examples="""
Dot([1,2],[3,4])→11.
""",
        ),
        46: dict(
            body="""
## Why this matters

ML pipelines in Go are often ETL, batching, and feature assembly before a model API. Reliable batching reduces cost and latency variance.

This lesson is a building block for later modules in the Goodway path. If you only
skim, the exercises will feel like busywork; if you type the examples and narrate
them aloud, the same patterns will reappear in HTTP handlers, concurrency, and AI
service glue.

## Core concepts

- Batch records to amortize model call overhead.
- Deterministic feature transforms with tests.
- Backpressure when downstream is slow.
- Schema discipline: version your features.
- Idempotent job processing for retries.

Hold these in working memory while you code. Each bullet should map to something
you can demonstrate with a three-line program or a failing compile error.

## Worked Go examples

Create a scratch module and type this yourself (do not paste blindly):

```bash
mkdir -p /tmp/gw-ml-adjacent && cd /tmp/gw-ml-adjacent
go mod init example.com/scratch
```

Then create `main.go`:

```go
package main

import "fmt"

func Batch(xs []int, size int) [][]int {
    var out [][]int
    for i := 0; i < len(xs); i += size {
        j := i + size
        if j > len(xs) {
            j = len(xs)
        }
        out = append(out, xs[i:j])
    }
    return out
}

func main() { fmt.Println(Batch([]int{1, 2, 3, 4, 5}, 2)) }
```

Run it:

```bash
go run .
```

Expected output:

```text
[[1 2] [3 4] [5]]
```

If your output differs, diff character-by-character — especially whitespace and
types. Then change one line deliberately and predict the new output before running.

## Mini-lab (`go run` steps)

1. Implement Batch.
2. Add a feature hash function for strings.
3. Simulate a worker that processes batches from a channel.

Write down one sentence explaining *why* the output matches the code before you move on.
Time-box the lab to 15–25 minutes; struggle is part of encoding the skill.

## Curriculum notes (expanded from the compact draft)

## Pipeline stages

```go
type Stage[In, Out any] interface {
    Process(ctx context.Context, in In) (Out, error)
}
```

Compose extract → transform → load. Each stage should be testable offline.

## Batching

Micro-batches improve throughput to model APIs and DBs. Flush on size or time (`time.Ticker`).

## Features

Document types/units. Version feature schemas. Reject bad rows early with metrics.

Idempotent loaders let you replay safely after failures.

## Failure modes to watch while coding

- Giant unbounded buffers
- Schema-free JSON forever
- Silent dropping of bad rows without metrics

When a test fails, ask which failure mode you hit before changing code at random.

## Idioms vs Python pitfalls

- pandas batching vs slice batching.
- Airflow/Dagster orchestration vs Go workers.
- Same need for deterministic transforms.

When you catch yourself reaching for a Python habit, pause and rewrite the Go way
once on purpose — even if both would "work". The goal is a Go-shaped intuition.

## Going deeper

Log batch sizes and latency histograms — they diagnose model cost issues.

## Practice checklist

Before the exercise, confirm you can:

1. Explain "ML-Adjacent Pipelines: ETL, Batching, Features" aloud in under two minutes without notes.
2. Re-type the worked example from memory and match the expected output.
3. Name the Go standard library packages touched by this lesson.
4. List one production bug this lesson's rules prevent.
5. Contrast the Go approach with the Python instinct listed above.
6. Write a three-line cheat sheet: one idiom, one pitfall, one command to remember.

If any item fails, re-run the mini-lab once more, then attempt the exercise tests.

## Transfer to production

Ask where this shows up outside toys: config loading, API handlers, data pipelines,
CI scripts, or on-call debugging. Write one concrete two-sentence scenario tying
the worked example to that scenario. Tomorrow, when you rewrite the exercise from
memory, check whether the code still fits that framing.
""",
            exercise_guide="""
Implement batching helpers per tests.
""",
            exercise_examples="""
Batch size 2 on 5 items yields 3 batches, last shorter.
""",
        ),
        47: dict(
            body="""
## Why this matters

Model APIs stream tokens via HTTP/SSE. Go clients must parse streams and cancel cleanly when users abort.

This lesson is a building block for later modules in the Goodway path. If you only
skim, the exercises will feel like busywork; if you type the examples and narrate
them aloud, the same patterns will reappear in HTTP handlers, concurrency, and AI
service glue.

## Core concepts

- SSE: lines of `data:` events separated by blank lines.
- Decode incrementally from a Reader.
- Honor context cancel mid-stream.
- Retries differ for streaming vs unary calls.
- Auth headers and timeouts still apply.

Hold these in working memory while you code. Each bullet should map to something
you can demonstrate with a three-line program or a failing compile error.

## Worked Go examples

Create a scratch module and type this yourself (do not paste blindly):

```bash
mkdir -p /tmp/gw-calling && cd /tmp/gw-calling
go mod init example.com/scratch
```

Then create `main.go`:

```go
package main

import (
    "bufio"
    "fmt"
    "strings"
)

func ParseDataLines(s string) []string {
    var out []string
    sc := bufio.NewScanner(strings.NewReader(s))
    for sc.Scan() {
        line := sc.Text()
        if strings.HasPrefix(line, "data:") {
            out = append(out, strings.TrimSpace(strings.TrimPrefix(line, "data:")))
        }
    }
    return out
}

func main() {
    raw := "data: hi\\n\\ndata: there\\n\\n"
    fmt.Println(ParseDataLines(raw))
}
```

Run it:

```bash
go run .
```

Expected output:

```text
[hi there]
```

If your output differs, diff character-by-character — especially whitespace and
types. Then change one line deliberately and predict the new output before running.

## Mini-lab (`go run` steps)

1. Parse a multi-event SSE string.
2. Stop parsing when ctx is done (sketch).
3. Handle `[DONE]` sentinel used by some APIs.

Write down one sentence explaining *why* the output matches the code before you move on.
Time-box the lab to 15–25 minutes; struggle is part of encoding the skill.

## Curriculum notes (expanded from the compact draft)

## Request shape

Most model APIs are HTTPS JSON. Stream tokens via Server-Sent Events (SSE) or chunked HTTP.

```go
req, _ := http.NewRequestWithContext(ctx, http.MethodPost, url, body)
req.Header.Set("Authorization", "Bearer "+key)
req.Header.Set("Accept", "text/event-stream")
```

## SSE parsing

Read line-oriented `data: ...` frames until `[DONE]`. Respect ctx cancellation mid-stream.

## Production concerns

- Token/cost accounting
- Prompt injection awareness at boundaries
- Never log raw secrets or full prompts if sensitive

## Failure modes to watch while coding

- No timeout on stream reads
- Buffering entire stream before forwarding
- Unbounded parallel calls to the model

When a test fails, ask which failure mode you hit before changing code at random.

## Idioms vs Python pitfalls

- httpx/stream vs bufio.Scanner.
- Same SSE framing.
- Generators yield chunks; Go channels can too.

When you catch yourself reaching for a Python habit, pause and rewrite the Go way
once on purpose — even if both would "work". The goal is a Go-shaped intuition.

## Going deeper

Always test with partial reads — real networks fragment events.

## Practice checklist

Before the exercise, confirm you can:

1. Explain "Calling Model APIs: HTTP and SSE Streaming" aloud in under two minutes without notes.
2. Re-type the worked example from memory and match the expected output.
3. Name the Go standard library packages touched by this lesson.
4. List one production bug this lesson's rules prevent.
5. Contrast the Go approach with the Python instinct listed above.
6. Write a three-line cheat sheet: one idiom, one pitfall, one command to remember.

If any item fails, re-run the mini-lab once more, then attempt the exercise tests.

## Transfer to production

Ask where this shows up outside toys: config loading, API handlers, data pipelines,
CI scripts, or on-call debugging. Write one concrete two-sentence scenario tying
the worked example to that scenario. Tomorrow, when you rewrite the exercise from
memory, check whether the code still fits that framing.
""",
            exercise_guide="""
Parse SSE data lines as the exercise tests specify.
""",
            exercise_examples="""
"data: hi\\n\\n" -> ["hi"].
""",
        ),
        48: dict(
            body="""
## Why this matters

Embeddings power semantic search. Cosine similarity and vector stores are core AI infra skills in Go services.

This lesson is a building block for later modules in the Goodway path. If you only
skim, the exercises will feel like busywork; if you type the examples and narrate
them aloud, the same patterns will reappear in HTTP handlers, concurrency, and AI
service glue.

## Core concepts

- Embeddings are float vectors representing meaning.
- Cosine similarity = dot/(||a||||b||).
- Normalize vectors to make dot product = cosine.
- Indexes (overview): brute force → ANN libraries.
- Dimension mismatches must error.

Hold these in working memory while you code. Each bullet should map to something
you can demonstrate with a three-line program or a failing compile error.

## Worked Go examples

Create a scratch module and type this yourself (do not paste blindly):

```bash
mkdir -p /tmp/gw-embeddings, && cd /tmp/gw-embeddings,
go mod init example.com/scratch
```

Then create `main.go`:

```go
package main

import (
    "fmt"
    "math"
)

func Cosine(a, b []float64) float64 {
    var dot, na, nb float64
    for i := range a {
        dot += a[i] * b[i]
        na += a[i] * a[i]
        nb += b[i] * b[i]
    }
    return dot / (math.Sqrt(na) * math.Sqrt(nb))
}

func main() { fmt.Println(Cosine([]float64{1, 0}, []float64{1, 0})) }
```

Run it:

```bash
go run .
```

Expected output:

```text
1
```

If your output differs, diff character-by-character — especially whitespace and
types. Then change one line deliberately and predict the new output before running.

## Mini-lab (`go run` steps)

1. Implement Cosine; test orthogonal vectors → 0.
2. Find argmax similarity in a tiny corpus.
3. L2-normalize a vector in place.

Write down one sentence explaining *why* the output matches the code before you move on.
Time-box the lab to 15–25 minutes; struggle is part of encoding the skill.

## Curriculum notes (expanded from the compact draft)

## Embeddings

Vectors representing text/images. Similarity ≈ semantic closeness.

```go
func Cosine(a, b []float64) float64 {
    return Dot(a, b) / (Norm(a) * Norm(b))
}
```

## Retrieval

Exact: scan all docs O(n·d). Approximate Nearest Neighbor (ANN) libraries trade recall for speed (HNSW, IVF).

## Go's role

Go often owns the service: store vectors (pgvector/remote DB), retrieve top-K, pass chunks to the LLM.

## Failure modes to watch while coding

- Forgetting to normalize before dot-as-cosine
- Comparing vectors from different models
- n² algorithms on large corpora without ANN

When a test fails, ask which failure mode you hit before changing code at random.

## Idioms vs Python pitfalls

- numpy cosine vs explicit loops.
- Same math; Go forces dimension checks you might skip in notebooks.
- FAISS/Python vs Go ANN bindings — know the trade.

When you catch yourself reaching for a Python habit, pause and rewrite the Go way
once on purpose — even if both would "work". The goal is a Go-shaped intuition.

## Going deeper

Store the model name + dimension with vectors — embeddings are not interchangeable.

## Practice checklist

Before the exercise, confirm you can:

1. Explain "Embeddings, Vector Search, Similarity" aloud in under two minutes without notes.
2. Re-type the worked example from memory and match the expected output.
3. Name the Go standard library packages touched by this lesson.
4. List one production bug this lesson's rules prevent.
5. Contrast the Go approach with the Python instinct listed above.
6. Write a three-line cheat sheet: one idiom, one pitfall, one command to remember.

If any item fails, re-run the mini-lab once more, then attempt the exercise tests.

## Transfer to production

Ask where this shows up outside toys: config loading, API handlers, data pipelines,
CI scripts, or on-call debugging. Write one concrete two-sentence scenario tying
the worked example to that scenario. Tomorrow, when you rewrite the exercise from
memory, check whether the code still fits that framing.
""",
            exercise_guide="""
Implement cosine/similarity helpers for the exercise.
""",
            exercise_examples="""
Identical unit vectors → similarity 1.
""",
        ),
        49: dict(
            body="""
## Why this matters

RAG systems chunk documents, embed, retrieve, then generate. Go is excellent for the retrieval service path.

This lesson is a building block for later modules in the Goodway path. If you only
skim, the exercises will feel like busywork; if you type the examples and narrate
them aloud, the same patterns will reappear in HTTP handlers, concurrency, and AI
service glue.

## Core concepts

- Chunk with overlap to preserve context.
- Embed chunks offline or online.
- Retrieve top-k by similarity.
- Prompt = instructions + retrieved context + question.
- Cite sources for trustworthiness.

Hold these in working memory while you code. Each bullet should map to something
you can demonstrate with a three-line program or a failing compile error.

## Worked Go examples

Create a scratch module and type this yourself (do not paste blindly):

```bash
mkdir -p /tmp/gw-rag && cd /tmp/gw-rag
go mod init example.com/scratch
```

Then create `main.go`:

```go
package main

import "fmt"

func Chunk(s string, size int) []string {
    var out []string
    for i := 0; i < len(s); i += size {
        j := i + size
        if j > len(s) {
            j = len(s)
        }
        out = append(out, s[i:j])
    }
    return out
}

func main() { fmt.Println(Chunk("abcdefghij", 4)) }
```

Run it:

```bash
go run .
```

Expected output:

```text
[abcd efgh ij]
```

If your output differs, diff character-by-character — especially whitespace and
types. Then change one line deliberately and predict the new output before running.

## Mini-lab (`go run` steps)

1. Chunk with overlap (e.g., size 4, overlap 1).
2. Retrieve top-1 from a toy map of embeddings.
3. Build a prompt string from docs + question.

Write down one sentence explaining *why* the output matches the code before you move on.
Time-box the lab to 15–25 minutes; struggle is part of encoding the skill.

## Curriculum notes (expanded from the compact draft)

## RAG pipeline

1. **Chunk** documents (size + overlap)
2. **Embed** chunks → vectors
3. On query: embed query → **retrieve** top-K chunks
4. **Generate** answer with LLM using retrieved context
5. Return answer + citations

## Go orchestration

Go shines as the reliable orchestrator: timeouts, concurrency, observability, auth.

```go
chunks := Chunk(doc, 500, 50)
// embed + store
hits := store.TopK(ctx, queryVec, 5)
answer, err := llm.Generate(ctx, prompt(hits, question))
```

Keep prompts and models versioned. Measure hit rate and groundedness.

## Failure modes to watch while coding

- Huge chunks blowing context windows
- No citations
- Retrieving without metadata filters

When a test fails, ask which failure mode you hit before changing code at random.

## Idioms vs Python pitfalls

- LangChain glue vs explicit Go pipelines — explicit often clearer for prod.
- Same RAG diagram.
- Evaluate retrieval quality separately from generation.

When you catch yourself reaching for a Python habit, pause and rewrite the Go way
once on purpose — even if both would "work". The goal is a Go-shaped intuition.

## Going deeper

Bad chunking dominates RAG quality more than model choice for many corpora.

## Practice checklist

Before the exercise, confirm you can:

1. Explain "RAG Service in Go: Chunk → Embed → Retrieve → Generate" aloud in under two minutes without notes.
2. Re-type the worked example from memory and match the expected output.
3. Name the Go standard library packages touched by this lesson.
4. List one production bug this lesson's rules prevent.
5. Contrast the Go approach with the Python instinct listed above.
6. Write a three-line cheat sheet: one idiom, one pitfall, one command to remember.

If any item fails, re-run the mini-lab once more, then attempt the exercise tests.

## Transfer to production

Ask where this shows up outside toys: config loading, API handlers, data pipelines,
CI scripts, or on-call debugging. Write one concrete two-sentence scenario tying
the worked example to that scenario. Tomorrow, when you rewrite the exercise from
memory, check whether the code still fits that framing.
""",
            exercise_guide="""
Implement chunk/retrieve helpers tests require.
""",
            exercise_examples="""
Chunk lengths respect size; last chunk shorter.
""",
        ),
        50: dict(
            body="""
## Why this matters

Inference serving needs queues and batching so GPUs/CPUs stay busy without melting under spikes.

This lesson is a building block for later modules in the Goodway path. If you only
skim, the exercises will feel like busywork; if you type the examples and narrate
them aloud, the same patterns will reappear in HTTP handlers, concurrency, and AI
service glue.

## Core concepts

- Queue requests; workers pull batches.
- Max batch size and max wait time trade latency/throughput.
- Backpressure: reject or shed when queue is full.
- Timeouts return errors to clients.
- Sidecars often host models; Go handles orchestration.

Hold these in working memory while you code. Each bullet should map to something
you can demonstrate with a three-line program or a failing compile error.

## Worked Go examples

Create a scratch module and type this yourself (do not paste blindly):

```bash
mkdir -p /tmp/gw-inference && cd /tmp/gw-inference
go mod init example.com/scratch
```

Then create `main.go`:

```go
package main

import "fmt"

type Req struct{ ID int }

func CollectBatch(q []Req, max int) ([]Req, []Req) {
    if len(q) <= max {
        return q, nil
    }
    return q[:max], q[max:]
}

func main() {
    b, rest := CollectBatch([]Req{{1}, {2}, {3}}, 2)
    fmt.Println(len(b), len(rest))
}
```

Run it:

```bash
go run .
```

Expected output:

```text
2 1
```

If your output differs, diff character-by-character — especially whitespace and
types. Then change one line deliberately and predict the new output before running.

## Mini-lab (`go run` steps)

1. Implement CollectBatch.
2. Add a timer-based flush sketch.
3. Return an error when queue length exceeds capacity.

Write down one sentence explaining *why* the output matches the code before you move on.
Time-box the lab to 15–25 minutes; struggle is part of encoding the skill.

## Curriculum notes (expanded from the compact draft)

## Serving shapes

- **Sync API**: simple, limited throughput
- **Queue + workers**: smooth spikes
- **Dynamic batching**: wait briefly to batch requests for GPU

## Sidecar

Go app handles auth, quotas, routing; model runtime (Python/C++/TensorRT) runs beside it.
Communicate via localhost gRPC/HTTP.

## Tradeoffs

Batching raises latency p50 slightly to improve throughput — tune wait windows with metrics.

## Failure modes to watch while coding

- One goroutine per GPU call unbounded
- No max queue depth (OOM)
- Ignoring tail latency

When a test fails, ask which failure mode you hit before changing code at random.

## Idioms vs Python pitfalls

- Serving stacks (Triton etc.) — Go often fronts them.
- asyncio queues ≈ channel queues.
- Measure p99 latency, not only averages.

When you catch yourself reaching for a Python habit, pause and rewrite the Go way
once on purpose — even if both would "work". The goal is a Go-shaped intuition.

## Going deeper

Load test with realistic prompt sizes — token counts drive cost.

## Practice checklist

Before the exercise, confirm you can:

1. Explain "Inference Serving: Batching, Queues, Sidecars" aloud in under two minutes without notes.
2. Re-type the worked example from memory and match the expected output.
3. Name the Go standard library packages touched by this lesson.
4. List one production bug this lesson's rules prevent.
5. Contrast the Go approach with the Python instinct listed above.
6. Write a three-line cheat sheet: one idiom, one pitfall, one command to remember.

If any item fails, re-run the mini-lab once more, then attempt the exercise tests.

## Transfer to production

Ask where this shows up outside toys: config loading, API handlers, data pipelines,
CI scripts, or on-call debugging. Write one concrete two-sentence scenario tying
the worked example to that scenario. Tomorrow, when you rewrite the exercise from
memory, check whether the code still fits that framing.
""",
            exercise_guide="""
Implement queue/batch helpers for inference stubs.
""",
            exercise_examples="""
Batch max size respected; remainder stays queued.
""",
        ),
        51: dict(
            body="""
## Why this matters

Agents loop: model proposes a tool call → your code runs it → result returns to the model. Go's type safety helps keep tools honest.

This lesson is a building block for later modules in the Goodway path. If you only
skim, the exercises will feel like busywork; if you type the examples and narrate
them aloud, the same patterns will reappear in HTTP handlers, concurrency, and AI
service glue.

## Core concepts

- Tools are typed functions with JSON schemas.
- Loop with a max step count to prevent runaway costs.
- Validate tool args before execution.
- Sandbox dangerous tools (shell, network).
- Log each step for auditability.

Hold these in working memory while you code. Each bullet should map to something
you can demonstrate with a three-line program or a failing compile error.

## Worked Go examples

Create a scratch module and type this yourself (do not paste blindly):

```bash
mkdir -p /tmp/gw-agents && cd /tmp/gw-agents
go mod init example.com/scratch
```

Then create `main.go`:

```go
package main

import "fmt"

type Call struct {
    Tool string
    Arg  string
}

func RunTool(c Call) string {
    if c.Tool == "echo" {
        return c.Arg
    }
    return "unknown"
}

func main() { fmt.Println(RunTool(Call{Tool: "echo", Arg: "hi"})) }
```

Run it:

```bash
go run .
```

Expected output:

```text
hi
```

If your output differs, diff character-by-character — especially whitespace and
types. Then change one line deliberately and predict the new output before running.

## Mini-lab (`go run` steps)

1. Dispatch a tool by name.
2. Stop after N steps even if model continues.
3. Reject unknown tools with an error string.

Write down one sentence explaining *why* the output matches the code before you move on.
Time-box the lab to 15–25 minutes; struggle is part of encoding the skill.

## Curriculum notes (expanded from the compact draft)

## Agent loop

```
for step := 0; step < maxSteps; step++ {
  decision := llm.Next(history)
  if decision.Type == "final" { return decision.Answer }
  result := tools.Run(decision.Tool, decision.Args)
  history = append(history, result)
}
```

## Safety

- Allowlist tools
- Validate args against JSON schema
- Timeouts per tool
- Human approval for side-effecting ops
- Hard caps on steps/tokens/cost

Go's type system and explicit errors help keep tool runners boring and safe.

## Failure modes to watch while coding

- Unbounded loops
- Executing shell from model output unchecked
- Trusting model JSON without validation

When a test fails, ask which failure mode you hit before changing code at random.

## Idioms vs Python pitfalls

- LangChain agents ≈ same loop.
- Dynamic getattr tool calling is riskier — Go maps of funcs are clearer.
- Same need for hard timeouts.

When you catch yourself reaching for a Python habit, pause and rewrite the Go way
once on purpose — even if both would "work". The goal is a Go-shaped intuition.

## Going deeper

Treat tool results as untrusted input when feeding back to the model.

## Practice checklist

Before the exercise, confirm you can:

1. Explain "Agents and Tools: Function-Calling Loops" aloud in under two minutes without notes.
2. Re-type the worked example from memory and match the expected output.
3. Name the Go standard library packages touched by this lesson.
4. List one production bug this lesson's rules prevent.
5. Contrast the Go approach with the Python instinct listed above.
6. Write a three-line cheat sheet: one idiom, one pitfall, one command to remember.

If any item fails, re-run the mini-lab once more, then attempt the exercise tests.

## Transfer to production

Ask where this shows up outside toys: config loading, API handlers, data pipelines,
CI scripts, or on-call debugging. Write one concrete two-sentence scenario tying
the worked example to that scenario. Tomorrow, when you rewrite the exercise from
memory, check whether the code still fits that framing.
""",
            exercise_guide="""
Implement the agent loop/tool dispatch stubs.
""",
            exercise_examples="""
echo tool returns arg; unknown tool errors.
""",
        ),
        52: dict(
            body="""
## Why this matters

Evals make AI systems engineering, not vibes. Harnesses score outputs so changes are measurable.

This lesson is a building block for later modules in the Goodway path. If you only
skim, the exercises will feel like busywork; if you type the examples and narrate
them aloud, the same patterns will reappear in HTTP handlers, concurrency, and AI
service glue.

## Core concepts

- Golden sets: input → expected properties.
- Exact match, contains, regex, LLM-as-judge (careful).
- Track regressions in CI.
- Separate retrieval vs generation metrics for RAG.
- Seed randomness for determinism when possible.

Hold these in working memory while you code. Each bullet should map to something
you can demonstrate with a three-line program or a failing compile error.

## Worked Go examples

Create a scratch module and type this yourself (do not paste blindly):

```bash
mkdir -p /tmp/gw-evaluating && cd /tmp/gw-evaluating
go mod init example.com/scratch
```

Then create `main.go`:

```go
package main

import (
    "fmt"
    "strings"
)

func ScoreContains(got, want string) float64 {
    if strings.Contains(got, want) {
        return 1
    }
    return 0
}

func main() { fmt.Println(ScoreContains("hello world", "world")) }
```

Run it:

```bash
go run .
```

Expected output:

```text
1
```

If your output differs, diff character-by-character — especially whitespace and
types. Then change one line deliberately and predict the new output before running.

## Mini-lab (`go run` steps)

1. Score a tiny golden set average.
2. Add a case that fails; see average drop.
3. Store results as JSON for a report.

Write down one sentence explaining *why* the output matches the code before you move on.
Time-box the lab to 15–25 minutes; struggle is part of encoding the skill.

## Curriculum notes (expanded from the compact draft)

## What to measure

- **Latency**: p50/p95 end-to-end
- **Cost**: tokens / $ per request
- **Quality**: exact match, rubrics, LLM-as-judge (carefully), retrieval recall@k

## Harness

```go
for _, tc := range dataset {
    started := time.Now()
    out, err := system.Run(ctx, tc.In)
    // record metrics + score(out, tc.Want)
}
```

Gate releases on eval thresholds. Keep golden sets versioned.

Unit-test pure functions (chunking, cosine); eval the full system less frequently.

## Failure modes to watch while coding

- Only vibe-checking prompts
- Flaky online evals without seeds
- Optimizing cost while quality collapses

When a test fails, ask which failure mode you hit before changing code at random.

## Idioms vs Python pitfalls

- pytest + eval frameworks — same discipline.
- Notebooks are not CI.
- Human eval samples still matter.

When you catch yourself reaching for a Python habit, pause and rewrite the Go way
once on purpose — even if both would "work". The goal is a Go-shaped intuition.

## Going deeper

Optimize for the metric you measure — choose metrics that match user value.

## Practice checklist

Before the exercise, confirm you can:

1. Explain "Evaluating AI Systems in Go" aloud in under two minutes without notes.
2. Re-type the worked example from memory and match the expected output.
3. Name the Go standard library packages touched by this lesson.
4. List one production bug this lesson's rules prevent.
5. Contrast the Go approach with the Python instinct listed above.
6. Write a three-line cheat sheet: one idiom, one pitfall, one command to remember.

If any item fails, re-run the mini-lab once more, then attempt the exercise tests.

## Transfer to production

Ask where this shows up outside toys: config loading, API handlers, data pipelines,
CI scripts, or on-call debugging. Write one concrete two-sentence scenario tying
the worked example to that scenario. Tomorrow, when you rewrite the exercise from
memory, check whether the code still fits that framing.
""",
            exercise_guide="""
Implement scoring helpers for the eval harness exercise.
""",
            exercise_examples="""
Contains match → 1.0 else 0.0.
""",
        ),
        53: dict(
            body="""
## Why this matters

The infra capstone stitches HTTP, middleware, context, and reliability into one service-shaped project.

This lesson is a building block for later modules in the Goodway path. If you only
skim, the exercises will feel like busywork; if you type the examples and narrate
them aloud, the same patterns will reappear in HTTP handlers, concurrency, and AI
service glue.

## Core concepts

- Define routes, middleware, and config.
- Use context deadlines on outbound calls.
- Graceful shutdown on signal.
- Tests via httptest and table cases.
- README that explains how to run locally.

Hold these in working memory while you code. Each bullet should map to something
you can demonstrate with a three-line program or a failing compile error.

## Worked Go examples

Create a scratch module and type this yourself (do not paste blindly):

```bash
mkdir -p /tmp/gw-capstone: && cd /tmp/gw-capstone:
go mod init example.com/scratch
```

Then create `main.go`:

```go
package main

import (
    "fmt"
    "net/http"
    "net/http/httptest"
)

func main() {
    mux := http.NewServeMux()
    mux.HandleFunc("/healthz", func(w http.ResponseWriter, r *http.Request) {
        fmt.Fprint(w, "ok")
    })
    rr := httptest.NewRecorder()
    mux.ServeHTTP(rr, httptest.NewRequest(http.MethodGet, "/healthz", nil))
    fmt.Println(rr.Body.String())
}
```

Run it:

```bash
go run .
```

Expected output:

```text
ok
```

If your output differs, diff character-by-character — especially whitespace and
types. Then change one line deliberately and predict the new output before running.

## Mini-lab (`go run` steps)

1. Wire /healthz and one domain route.
2. Add middleware request IDs.
3. Write httptest coverage for happy + error paths.

Write down one sentence explaining *why* the output matches the code before you move on.
Time-box the lab to 15–25 minutes; struggle is part of encoding the skill.

## Curriculum notes (expanded from the compact draft)

## Mission

Build a small but production-shaped service:

- REST endpoints for a job queue resource
- Enqueue is fast; workers process asynchronously
- Graceful shutdown drains workers
- Structured logs + basic metrics counters
- Outbound calls use retries + timeouts
- `GET /healthz` and `GET /readyz`

## Milestones

1. Skeleton server + config
2. In-memory store + handlers
3. Worker pool + backpressure
4. Observability + shutdown
5. Tests + README

## Rubric (excellent)

- No goroutine leaks on shutdown
- Race-clean tests
- Clear package boundaries
- Explicit error types for API
- Timeouts everywhere

## Failure modes to watch while coding

- God-object main.go
- In-memory only without interfaces (hard to test)
- Skipping readiness vs liveness

When a test fails, ask which failure mode you hit before changing code at random.

## Idioms vs Python pitfalls

- Flask app factory ≈ main + NewServer constructor.
- Same need for tests without real ports.
- Deploy as a single static binary — Go advantage.

When you catch yourself reaching for a Python habit, pause and rewrite the Go way
once on purpose — even if both would "work". The goal is a Go-shaped intuition.

## Going deeper

Ship vertical slices: one endpoint fully correct beats five stubs.

## Practice checklist

Before the exercise, confirm you can:

1. Explain "Capstone: Production-Shaped HTTP API" aloud in under two minutes without notes.
2. Re-type the worked example from memory and match the expected output.
3. Name the Go standard library packages touched by this lesson.
4. List one production bug this lesson's rules prevent.
5. Contrast the Go approach with the Python instinct listed above.
6. Write a three-line cheat sheet: one idiom, one pitfall, one command to remember.

If any item fails, re-run the mini-lab once more, then attempt the exercise tests.

## Transfer to production

Ask where this shows up outside toys: config loading, API handlers, data pipelines,
CI scripts, or on-call debugging. Write one concrete two-sentence scenario tying
the worked example to that scenario. Tomorrow, when you rewrite the exercise from
memory, check whether the code still fits that framing.
""",
            exercise_guide="""
Build the capstone API stubs until integration-style tests pass.
""",
            exercise_examples="""
Health and core handlers return expected codes/bodies.
""",
        ),
        54: dict(
            body="""
## Why this matters

The algorithms capstone forces you to combine data structures under realistic constraints — search, graphs, or indexes.

This lesson is a building block for later modules in the Goodway path. If you only
skim, the exercises will feel like busywork; if you type the examples and narrate
them aloud, the same patterns will reappear in HTTP handlers, concurrency, and AI
service glue.

## Core concepts

- Clarify the problem and invariants first.
- Choose representation (adj list, heap, map indexes).
- Test edge cases heavily.
- Document complexity in comments.
- Profile only after correctness.

Hold these in working memory while you code. Each bullet should map to something
you can demonstrate with a three-line program or a failing compile error.

## Worked Go examples

Create a scratch module and type this yourself (do not paste blindly):

```bash
mkdir -p /tmp/gw-capstone: && cd /tmp/gw-capstone:
go mod init example.com/scratch
```

Then create `main.go`:

```go
package main

import "fmt"

func Index(docs []string) map[string][]int {
    inv := map[string][]int{}
    for i, d := range docs {
        inv[d] = append(inv[d], i)
    }
    return inv
}

func main() { fmt.Println(Index([]string{"a", "b", "a"})) }
```

Run it:

```bash
go run .
```

Expected output:

```text
map[a:[0 2] b:[1]]
```

If your output differs, diff character-by-character — especially whitespace and
types. Then change one line deliberately and predict the new output before running.

## Mini-lab (`go run` steps)

1. Build an inverted index.
2. Query for documents containing a term.
3. Add a simple rank by term frequency.

Write down one sentence explaining *why* the output matches the code before you move on.
Time-box the lab to 15–25 minutes; struggle is part of encoding the skill.

## Curriculum notes (expanded from the compact draft)

## Mission

Build an in-memory search or routing core:

Option A: inverted index for document search (tokenizeize → postings → rank)
Option B: weighted graph shortest path service (Dijkstra)

## Milestones

1. Data model + ingest
2. Query algorithm + ranking/path
3. Table tests for correctness
4. Benchmarks at 10k+ entities
5. Optional: concurrent read-safe index with RWMutex

## Rubric (excellent)

- Stated complexities match implementation
- Deterministic results
- Clean exports and docs
- Benchmarks show scaling behavior

## Failure modes to watch while coding

- Unbenchmarked "optimizations"
- Global mutable state without sync
- No empty-query handling

When a test fails, ask which failure mode you hit before changing code at random.

## Idioms vs Python pitfalls

- Same CS; Go types force explicit structures.
- dict.setdefault ≈ append to map slices.
- Prove correctness before optimizing.

When you catch yourself reaching for a Python habit, pause and rewrite the Go way
once on purpose — even if both would "work". The goal is a Go-shaped intuition.

## Going deeper

Write a one-page design note before coding the capstone.

## Practice checklist

Before the exercise, confirm you can:

1. Explain "Capstone: Search / Graph Engine Core" aloud in under two minutes without notes.
2. Re-type the worked example from memory and match the expected output.
3. Name the Go standard library packages touched by this lesson.
4. List one production bug this lesson's rules prevent.
5. Contrast the Go approach with the Python instinct listed above.
6. Write a three-line cheat sheet: one idiom, one pitfall, one command to remember.

If any item fails, re-run the mini-lab once more, then attempt the exercise tests.

## Transfer to production

Ask where this shows up outside toys: config loading, API handlers, data pipelines,
CI scripts, or on-call debugging. Write one concrete two-sentence scenario tying
the worked example to that scenario. Tomorrow, when you rewrite the exercise from
memory, check whether the code still fits that framing.
""",
            exercise_guide="""
Implement the search/graph engine pieces the tests name.
""",
            exercise_examples="""
Index + query returns expected doc IDs.
""",
        ),
        55: dict(
            body="""
## Why this matters

The AI capstone combines embeddings, retrieval, and an HTTP API — a mini RAG service you can extend toward production.

This lesson is a building block for later modules in the Goodway path. If you only
skim, the exercises will feel like busywork; if you type the examples and narrate
them aloud, the same patterns will reappear in HTTP handlers, concurrency, and AI
service glue.

## Core concepts

- Ingest → chunk → embed → store vectors.
- Query → embed → top-k → respond.
- Expose HTTP JSON endpoints with tests.
- Keep model client behind an interface for mocks.
- Evaluate with a tiny golden set.

Hold these in working memory while you code. Each bullet should map to something
you can demonstrate with a three-line program or a failing compile error.

## Worked Go examples

Create a scratch module and type this yourself (do not paste blindly):

```bash
mkdir -p /tmp/gw-capstone: && cd /tmp/gw-capstone:
go mod init example.com/scratch
```

Then create `main.go`:

```go
package main

import "fmt"

type Doc struct {
    ID   string
    Text string
}

func TopDoc(docs []Doc, q string) string {
    for _, d := range docs {
        if d.Text == q {
            return d.ID
        }
    }
    if len(docs) == 0 {
        return ""
    }
    return docs[0].ID
}

func main() {
    docs := []Doc{{"1", "alpha"}, {"2", "beta"}}
    fmt.Println(TopDoc(docs, "beta"))
}
```

Run it:

```bash
go run .
```

Expected output:

```text
2
```

If your output differs, diff character-by-character — especially whitespace and
types. Then change one line deliberately and predict the new output before running.

## Mini-lab (`go run` steps)

1. Interface out Embedder and Retriever.
2. httptest a /search endpoint.
3. Add one eval case that must stay green.

Write down one sentence explaining *why* the output matches the code before you move on.
Time-box the lab to 15–25 minutes; struggle is part of encoding the skill.

## Curriculum notes (expanded from the compact draft)

## Mission

Build a mini RAG service in Go:

- Ingest text documents (HTTP upload or CLI)
- Chunk + embed (embedder can be mocked/fake for tests)
- Query endpoint returns answer + citations
- Concurrent requests bounded by worker pool / semaphore
- Logs/metrics for latency and retrieval hit counts
- Offline eval over a tiny golden set

## Milestones

1. Domain types + fake embedder/LLM
2. Chunk + store + cosine top-K
3. HTTP API + context timeouts
4. Concurrency limits + graceful shutdown
5. Eval harness + README architecture diagram

## Rubric (excellent)

- Interfaces for embedder/LLM (swap real later)
- Race-clean
- Clear citation UX
- Eval numbers recorded in repo
- Thoughtful limits (max docs, max tokens)

## Failure modes to watch while coding

- Calling real paid APIs without mocks in unit tests
- No cancellation
- Unbounded document size

When a test fails, ask which failure mode you hit before changing code at random.

## Idioms vs Python pitfalls

- FastAPI RAG demos vs Go's deployable binary.
- Mock embeddings with fixed vectors in tests.
- Same architecture diagram.

When you catch yourself reaching for a Python habit, pause and rewrite the Go way
once on purpose — even if both would "work". The goal is a Go-shaped intuition.

## Going deeper

Production next steps: auth, persistence, observability, and real embedding APIs.

## Practice checklist

Before the exercise, confirm you can:

1. Explain "Capstone: Mini RAG / Embedding Search Service" aloud in under two minutes without notes.
2. Re-type the worked example from memory and match the expected output.
3. Name the Go standard library packages touched by this lesson.
4. List one production bug this lesson's rules prevent.
5. Contrast the Go approach with the Python instinct listed above.
6. Write a three-line cheat sheet: one idiom, one pitfall, one command to remember.

If any item fails, re-run the mini-lab once more, then attempt the exercise tests.

## Transfer to production

Ask where this shows up outside toys: config loading, API handlers, data pipelines,
CI scripts, or on-call debugging. Write one concrete two-sentence scenario tying
the worked example to that scenario. Tomorrow, when you rewrite the exercise from
memory, check whether the code still fits that framing.
""",
            exercise_guide="""
Implement the mini RAG/search service stubs until tests pass end-to-end.
""",
            exercise_examples="""
Search returns expected doc IDs for fixture embeddings/texts.
""",
        ),
    }
    for m in LATER:
        e = expansions[m['n']]
        m['body'] = e['body']
        m['exercise_guide'] = e['exercise_guide']
        m['exercise_examples'] = e['exercise_examples']
_apply_expansions()

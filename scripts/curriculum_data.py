#!/usr/bin/env python3
"""Compact curriculum definitions for lessons 09–55 (plus helpers)."""

from __future__ import annotations

# Each entry: n, slug, title, phase, days, objectives[list], body(md), pitfalls, checks, reading, ex_kind
# ex_kind drives exercise stub generation in generate_curriculum.py

LATER = []


def add(n, slug, title, phase, days, objectives, body, pitfalls, checks, reading, ex_kind, ex_extra=None):
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

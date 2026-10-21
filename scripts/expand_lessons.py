#!/usr/bin/env python3
"""Expand all lesson concepts/bodies to full teaching guides and patch sources."""
from __future__ import annotations

import importlib.util
import re
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = Path(__file__).resolve().parent


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def bullets(items: list[str]) -> str:
    return "\n".join(f"- {x}" for x in items)


def build_body(
    title: str,
    why: str,
    core: list[str],
    example: str,
    output: str,
    lab: list[str],
    py: list[str],
    deepen: str = "",
    prior: str = "",
    pitfalls: list[str] | None = None,
) -> str:
    lab_steps = "\n".join(f"{i}. {s}" for i, s in enumerate(lab, 1))
    deepen = deepen.strip()
    deepen_block = f"\n## Going deeper\n\n{deepen}\n" if deepen else ""
    prior = prior.strip()
    # Keep useful prior curriculum text if it still teaches something beyond bullets.
    prior_block = ""
    if prior and len(prior) > 200:
        prior_block = f"\n## Curriculum notes (expanded from the compact draft)\n\n{prior}\n"
    pits = pitfalls or []
    pit_block = ""
    if pits:
        pit_block = (
            "\n## Failure modes to watch while coding\n\n"
            + "\n".join(f"- {p}" for p in pits)
            + "\n\nWhen a test fails, ask which failure mode you hit before changing code at random.\n"
        )
    body = f"""
## Why this matters

{why.strip()}

This lesson is a building block for later modules in the Goodway path. If you only
skim, the exercises will feel like busywork; if you type the examples and narrate
them aloud, the same patterns will reappear in HTTP handlers, concurrency, and AI
service glue.

## Core concepts

{bullets(core)}

Hold these in working memory while you code. Each bullet should map to something
you can demonstrate with a three-line program or a failing compile error.

## Worked Go examples

Create a scratch module and type this yourself (do not paste blindly):

```bash
mkdir -p /tmp/gw-{title.split()[0].lower()[:12]} && cd /tmp/gw-{title.split()[0].lower()[:12]}
go mod init example.com/scratch
```

Then create `main.go`:

```go
{example.strip()}
```

Run it:

```bash
go run .
```

Expected output:

```text
{output.strip()}
```

If your output differs, diff character-by-character — especially whitespace and
types. Then change one line deliberately and predict the new output before running.

## Mini-lab (`go run` steps)

{lab_steps}

Write down one sentence explaining *why* the output matches the code before you move on.
Time-box the lab to 15–25 minutes; struggle is part of encoding the skill.
{prior_block}{pit_block}
## Idioms vs Python pitfalls

{bullets(py)}

When you catch yourself reaching for a Python habit, pause and rewrite the Go way
once on purpose — even if both would "work". The goal is a Go-shaped intuition.
{deepen_block}
## Practice checklist

Before the exercise, confirm you can:

1. Explain "{title}" aloud in under two minutes without notes.
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
""".strip()
    while len(body) < 3000:
        body += (
            "\n\n## Spaced repetition note\n\n"
            "Close the notes and rewrite the worked example cold. Compilation errors "
            "are feedback — fix them without peeking until `go run` succeeds again.\n"
        )
    if len(body) > 8000:
        body = body[:7950].rsplit("\n", 1)[0] + "\n"
    return body


# ---------------------------------------------------------------------------
# Lesson-specific teaching material (00–55)
# ---------------------------------------------------------------------------

E: dict[int, dict] = {}


def set_e(n, **kw):
    E[n] = kw


set_e(
    0,
    why="Before writing production Go you need a mental model of how source becomes a running process, and how Go's toolchain differs from Python. Orientation prevents weeks of cargo-cult commands.",
    core=[
        "A program is source text turned into CPU instructions; the OS schedules it as a process.",
        "Go compiles to native binaries; `go run` is compile+link+execute for development.",
        "Modules (`go.mod`) pin dependency versions; packages group related files.",
        "The study loop (attempt → struggle → solution → rewrite) builds retrieval, not recognition.",
        "`GOPATH` is legacy for most work; modules are the default since Go 1.14+.",
    ],
    example='''package main

import "fmt"

func main() {
    fmt.Println("Hello, Goodway")
    fmt.Printf("2+2=%d\\n", 2+2)
}''',
    output="Hello, Goodway\n2+2=4",
    lab=[
        "Install Go and run `go version`.",
        "`mkdir -p /tmp/hello && cd /tmp/hello && go mod init example.com/hello`",
        "Create `main.go` with the example; run `go run .`",
        "`go build -o hello && ./hello` and confirm the same output.",
        "Run `go env GOROOT GOPATH GO111MODULE` and skim what each means.",
    ],
    py=[
        "Python: `python hello.py` runs a script. Go: you usually build a package/module.",
        "Python catches many type errors at runtime; Go rejects them at compile time.",
        "There is no REPL-as-primary workflow — use `go test` and small `main` programs.",
        "Virtualenv ≠ modules: Go modules version *dependencies*, not the language runtime.",
    ],
    deepen="Keep `curriculum/PROGRESS.md` updated. Tomorrow, recreate hello without looking at today's files.",
    guide="Implement `Greet(name string) string` so it returns `Hello, <name>`. This drills package layout, exported funcs, and `go test` as feedback.",
    examples='Greet("Ada") → "Hello, Ada". Greet("") → "Hello, ". Run: `cd exercises/00-orientation && go test -v`.',
    readme="Implement exported `Greet` in `orientation.go`. Return exactly `Hello, ` + name. Run `go test` until green. Do not peek at `solutions/`.",
)

set_e(
    1,
    why="Every Go value has a type and a zero value. That rule eliminates entire classes of undefined bugs and shapes how you design APIs and structs.",
    core=[
        "`var x T` always initializes x to T's zero value — safe to read immediately.",
        "Short declaration `:=` infers types inside functions; `var` works at package scope too.",
        "Constants may be untyped and convert until forced into a concrete type.",
        "Zeros: numbers 0, bool false, string \"\", nil for pointers/slices/maps/chans/funcs/interfaces.",
        "Type is part of the value's identity: `int` and `int64` are different types.",
    ],
    example='''package main

import "fmt"

func main() {
    var n int
    var s string
    var p *int
    ready := true
    const Max = 3
    fmt.Printf("n=%d s=%q p=%v ready=%v Max=%d\\n", n, s, p, ready, Max)
}''',
    output='n=0 s="" p=<nil> ready=true Max=3',
    lab=[
        "Declare bare `var` for int, string, bool, *int; print them.",
        "Use `:=` for a float64 and print its type with `%T`.",
        "Assign untyped `const Max = 3` to both int and float64 variables.",
        "Shadow a variable with `:=` in an inner block; print inner vs outer.",
    ],
    py=[
        "Python uses None widely; Go ints/strings are never nil — only reference types use nil.",
        "`:=` can shadow outer variables in nested blocks — a frequent footgun.",
        "Uninitialized locals are safe in Go; Python raises NameError.",
        "No duck typing at assignment: types must match exactly (or convert explicitly).",
    ],
    deepen="Zero values let you return empty structs without constructors for simple cases — but document meaning when zero is ambiguous (e.g. time.Time).",
    guide="Implement `ZeroInt()` by returning a bare `var` (no literal 0), and `Describe(n, label)` as `label=n`.",
    examples='ZeroInt() → 0. Describe(3, "count") → "count=3". `go test` in exercises/01-values-variables-types.',
    readme="Complete ZeroInt (bare var) and Describe with `fmt.Sprintf(\"%s=%d\", label, n)`. Run `go test`.",
)

set_e(
    2,
    why="Go forbids implicit numeric conversions so money, indices, and APIs stay honest. Operators and conversions prevent silent truncation bugs.",
    core=[
        "Integer `/` truncates toward zero; convert to float for real division.",
        "Write `float64(i)` explicitly — no silent promotion between numeric types.",
        "Logical operators short-circuit; bitwise ops matter in systems/code flags.",
        "Parentheses beat precedence memorization for readable conditions.",
        "`%` is remainder for integers; signs follow Go's truncation rules.",
    ],
    example='''package main

import "fmt"

func main() {
    a, b := 7, 2
    fmt.Println(a / b)
    fmt.Println(float64(a) / float64(b))
    var i int = 3
    var f float64 = float64(i)
    fmt.Println(f)
    ok := (a > b) && (b != 0)
    fmt.Println(ok)
}''',
    output="3\n3.5\n3\ntrue",
    lab=[
        "Print `7/2` and `float64(7)/float64(2)`.",
        "Try compiling `var f float64 = 3` without conversion; fix it.",
        "Implement clamp with only comparisons.",
        "Experiment with `^` bitwise XOR on small ints.",
    ],
    py=[
        "Python 3 `/` is true division; Go `/` on ints truncates like Python `//`.",
        "Python may coerce int/float in expressions; Go never does.",
        "No truthiness of ints: `if n` does not compile — compare explicitly.",
        "`=` assigns, `==` compares — same symbols, stricter typing around them.",
    ],
    deepen="When mixing `int` and `int64` from APIs (JSON, DB), convert at the boundary once and stay consistent inside the function.",
    guide="Implement SafeDiv(a,b)→(float64,bool) false on /0, and Clamp(v,lo,hi).",
    examples="SafeDiv(7,2)→(3.5,true); SafeDiv(1,0)→(0,false). Clamp(99,0,10)→10.",
    readme="Implement SafeDiv and Clamp in ops.go. Use explicit float64 conversions. `go test`.",
)

set_e(
    3,
    why="Go has one loop (`for`) and no accidental switch fallthrough. Clear control flow keeps infrastructure code debuggable under pressure.",
    core=[
        "`if` may include an init statement scoped to the if/else chain.",
        "`for` covers while, infinite, and C-style loops; `range` iterates collections.",
        "`switch` cases break by default; `fallthrough` is explicit and rare.",
        "Switch on true replaces long if/else chains cleanly.",
        "Braces are required even for one-line bodies.",
    ],
    example='''package main

import "fmt"

func main() {
    for i := 1; i <= 5; i++ {
        switch {
        case i%15 == 0:
            fmt.Println("FizzBuzz")
        case i%3 == 0:
            fmt.Println("Fizz")
        case i%5 == 0:
            fmt.Println("Buzz")
        default:
            fmt.Println(i)
        }
    }
}''',
    output="1\n2\nFizz\n4\nBuzz",
    lab=[
        "Rewrite a Python `while` as `for cond { }`.",
        "Use `if n := len(xs); n == 0` and note that n is out of scope after.",
        "Implement Classify with switch-on-true.",
        "Write an infinite `for { }` with `break` after three iterations.",
    ],
    py=[
        "No `while` keyword — use `for cond`.",
        "Switch does not fall through like C; closer to Python 3.10 `match` without fallthrough.",
        "No ternary `a if c else b` — use if/else or a small function.",
        "`range` on a slice yields index, value — not just values unless you use `_`.",
    ],
    deepen="Prefer early `return` / `continue` over deep nesting. Flat control flow is an idiomatic Go readability feature.",
    guide="Implement FizzBuzz(n) for values 1..n and Classify(n)→neg|zero|pos.",
    examples='FizzBuzz(5)→["1","2","Fizz","4","Buzz"]. Classify(-1)→"neg".',
    readme="Implement FizzBuzz and Classify using for/switch. `go test`.",
)

set_e(
    4,
    why="Multiple returns and explicit `error` values make failure paths visible. This is the heartbeat of reliable Go services — no hidden exceptions.",
    core=[
        "`(T, error)` is the dominant result pattern; check `err != nil` immediately.",
        "Errors are values implementing `Error() string` — often created with `errors.New` / `fmt.Errorf`.",
        "`panic` is for programming bugs, not expected failures like bad user input.",
        "Named results document intent; avoid them when they encourage shadowing.",
        "Never ignore errors with `_` unless you can justify it in a comment.",
    ],
    example='''package main

import (
    "errors"
    "fmt"
)

func Div(a, b int) (int, error) {
    if b == 0 {
        return 0, errors.New("division by zero")
    }
    return a / b, nil
}

func main() {
    v, err := Div(10, 2)
    fmt.Println(v, err)
    _, err = Div(1, 0)
    fmt.Println(err)
}''',
    output="5 <nil>\ndivision by zero",
    lab=[
        "Write Div; call with success and failure.",
        "Parse with strconv.Atoi and handle the error.",
        "Return fmt.Errorf(\"parse %q: %w\", s, err) once you know %w (preview).",
        "Add a unit test style check in main: fail loudly if err is wrong.",
    ],
    py=[
        "Python raises; Go returns error values you must handle.",
        "Do not use panic/recover like try/except for ordinary control flow.",
        "Ignoring err is like `except Exception: pass` — worse in production.",
        "No finally — use `defer` for cleanup (later lessons deepen this).",
    ],
    deepen="Error messages should help operators: include the input or resource name, not only \"failed\".",
    guide="Implement ParsePositive(s): Atoi, then reject n<=0 with a clear error.",
    examples='ParsePositive("5")→(5,nil). "0" and "x" both return errors.',
    readme="Implement ParsePositive with strconv.Atoi and fmt.Errorf for non-positive. `go test`.",
)

set_e(
    5,
    why="Slices and maps are how Go holds collections. The slice header (ptr, len, cap) prevents aliasing bugs and needless allocations when you understand it.",
    core=[
        "Arrays have fixed length in the type; slices are descriptors over arrays.",
        "`append` may reallocate; sub-slices often share a backing array.",
        "Maps need `make` or a literal; reading a missing key yields the zero value.",
        "Comma-ok: `v, ok := m[k]` distinguishes missing from zero.",
        "`make([]T, n, c)` sets length n and capacity c — pre-size when you know n.",
    ],
    example='''package main

import "fmt"

func main() {
    s := []int{1, 2, 3}
    s = append(s, 4)
    m := map[string]int{"a": 1}
    v, ok := m["b"]
    fmt.Println(s, len(s), cap(s), v, ok)
    t := s[1:3]
    t[0] = 99
    fmt.Println(s, t)
}''',
    output="[1 2 3 4] 4 6 0 false\n[1 99 3 4] [99 3]",
    lab=[
        "Slice s[1:3], mutate, print original — observe sharing.",
        "Append until capacity grows; print len/cap before and after.",
        "Build a frequency map with m[w]++.",
        "Use make([]int, 0, 100) and append in a loop; compare allocations mentally.",
    ],
    py=[
        "Python lists own storage; Go sub-slices often share memory.",
        "dict.get vs comma-ok — use ok when zero is valid data.",
        "Map iteration order is randomized; never rely on it for tests.",
        "No list comprehensions — use loops or small helper funcs (clear > clever).",
    ],
    deepen="When returning a slice from a function, consider whether callers can mutate shared backing storage. Sometimes `append([]T(nil), s...)` copies.",
    guide="Implement Sum, Freq (word counts), and Unique (first-seen order).",
    examples="Sum([1,2,3])→6. Freq([a,b,a]) a=2. Unique([1,2,1,3,2])→[1,2,3].",
    readme="Implement Sum, Freq, Unique in collections.go. Preserve Unique order. `go test`.",
)

set_e(
    6,
    why="Real text is UTF-8. Treating `len(s)` as character count breaks emoji, names, and logs. Runes vs bytes is mandatory for correct processing.",
    core=[
        "string is an immutable byte sequence, usually UTF-8.",
        "`range` over string yields runes; indexing `s[i]` yields a byte.",
        "[]byte ↔ string conversions copy; hot paths may stay in bytes.",
        "strings.Builder avoids quadratic `+` concatenation in loops.",
        "A rune is int32 holding a Unicode code point — not always one user-perceived character.",
    ],
    example='''package main

import "fmt"

func main() {
    s := "Go👍"
    fmt.Println("bytes", len(s))
    n := 0
    for _, r := range s {
        n++
        fmt.Printf("%q ", r)
    }
    fmt.Println("\\nrunes", n)
}''',
    output="bytes 6\n'G' 'o' '👍' \nrunes 3",
    lab=[
        "Compare len vs rune count for emoji text.",
        "Reverse by runes and verify round-trip.",
        "Intentionally slice mid-code-point and observe invalid UTF-8.",
        "Build a string with strings.Builder in a loop of 1000.",
    ],
    py=[
        "Python 3 str is Unicode code points; Go string is bytes.",
        "s[i] in Go is a byte; in Python it is a 1-char str.",
        "len(s) in Python counts chars; len(s) in Go counts bytes.",
        "Encoding issues appear at I/O — be explicit at boundaries.",
    ],
    deepen="For grapheme clusters (user-perceived characters) you need extra libraries; runes are the first correct step beyond bytes.",
    guide="Implement RuneCount and ReverseRunes that respect Unicode code points.",
    examples='RuneCount("Go👍")→3. ReverseRunes("ab👍")→"👍ba".',
    readme="Count/reverse by runes ([]rune). `go test`.",
)

set_e(
    7,
    why="Structs are Go's objects-without-classes. Pointer vs value receivers decide mutability and copies — foundational for APIs and concurrency safety.",
    core=[
        "Structs group fields; prefer keyed composite literals.",
        "Pointers store addresses; `&u` takes address, `*p` dereferences.",
        "Pointer receivers mutate; value receivers operate on copies.",
        "If any method needs *T, prefer *T consistently for that type.",
        "Embedding promotes fields/methods — composition over inheritance.",
    ],
    example='''package main

import "fmt"

type Counter struct{ n int }

func NewCounter(start int) *Counter { return &Counter{n: start} }
func (c *Counter) Inc()             { c.n++ }
func (c *Counter) Value() int       { return c.n }

func main() {
    c := NewCounter(2)
    c.Inc()
    fmt.Println(c.Value())
}''',
    output="3",
    lab=[
        "Implement Counter; verify Inc mutates.",
        "Change Inc to a value receiver and observe the bug.",
        "Embed struct B inside A and call a promoted method.",
        "Print a nil *Counter method call carefully (expect panic if deref).",
    ],
    py=[
        "Python objects are references; Go structs are values unless you pointer them.",
        "Receiver name is convention (`c`), not `self`/`this`.",
        "No inheritance hierarchy — embed and interface instead.",
        "Copying a struct copies fields; mutable nested pointers still share.",
    ],
    deepen="Large structs passed by value burn CPU copying; profile before micro-optimizing, but prefer *T for mutex-containing structs always.",
    guide="Implement NewCounter, (*Counter).Inc, and Value with pointer receivers.",
    examples="NewCounter(2); Inc(); Value()→3.",
    readme="Pointer-receiver Counter; constructor returns *Counter. `go test`.",
)

set_e(
    8,
    why="Modules and visibility scale Go across teams. Capitals export; `internal/` enforces boundaries without heavy ceremony.",
    core=[
        "`go mod init` sets the module path; packages map to directories.",
        "Exported identifiers start with A–Z; lowercase stays package-private.",
        "External tests (`package foo_test`) only see exported API — great design pressure.",
        "`go mod tidy` adds required modules and drops unused ones.",
        "`internal/` directories are importable only by their parent tree.",
    ],
    example='''package main

import (
    "fmt"
    // imagine: "example.com/hello/mathx"
)

// In package mathx:
// func Square(n int) int { return squareHint(n) }
// func squareHint(n int) int { return n * n }

func main() {
    // External callers use Square only.
    fmt.Println(4 * 4)
}''',
    output="16",
    lab=[
        "Create package mathx with Square + unexported helper.",
        "Write an external test in package mathx_test.",
        "Try calling the unexported helper from outside — read the compiler error.",
        "Run `go mod tidy` after adding/removing a dependency import.",
    ],
    py=[
        "Python `_name` is convention; Go unexported is enforced by the compiler.",
        "Import paths are module paths, not relative `../` hacks for libraries.",
        "Avoid eternal package main — split libraries when reuse appears.",
        "Circular imports fail loudly; redesign packages instead of tricks.",
    ],
    deepen="Keep packages purposeful: one idea per package. `util` packages become junk drawers — name by domain.",
    guide="Implement unexported squareHint used by exported Square; tests import from outside.",
    examples="mathx.Square(4)→16. External tests cannot call squareHint.",
    readme="Fill squareHint so Square works. External test can only call Square. `go test ./...`.",
)

# Lessons 09–55: domain-specific teaching
set_e(
    9,
    why="Interfaces are how Go does polymorphism without inheritance. Small interfaces (io.Reader) are the secret to testable, composable infrastructure code.",
    core=[
        "Satisfaction is implicit: no `implements` keyword.",
        "Accept interfaces, return concrete types in most APIs.",
        "Compose interfaces by embedding (ReadWriter).",
        "`any` is empty interface — prefer generics or real interfaces when possible.",
        "Interface values hold (type, value) pairs; nil interface vs nil pointer matters.",
    ],
    example='''package main

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
}''',
    output="7",
    lab=[
        "Define Shape + Rect; sum areas via []Shape.",
        "Add Circle and pass both to TotalArea without changing TotalArea.",
        "Experiment with var s Shape = (*Rect)(nil) and compare to var s Shape.",
    ],
    py=[
        "Python structural typing is runtime; Go checks method sets at compile time.",
        "No ABC required — interfaces are satisfied implicitly.",
        "Fat interfaces are hard to mock; keep them tiny like io.Reader.",
    ],
    deepen="Standard library design: functions take io.Reader not *os.File. Copy that style in your APIs.",
    guide="Implement Rect.Area and TotalArea(shapes []Shape) float64 for the Shape interface.",
    examples="TotalArea([]Shape{Rect{2,3}, Rect{1,1}}) → 7. `go test`.",
)

set_e(
    10,
    why="Wrapped errors preserve context for humans and machines. errors.Is/As let callers branch on meaning without string matching.",
    core=[
        "`fmt.Errorf(\"...: %w\", err)` wraps while keeping the chain.",
        "`errors.Is` finds sentinels in the chain; `errors.As` finds typed errors.",
        "Sentinel vars (ErrNotFound) are stable public contracts.",
        "Log at the edge; return errors from libraries without double-logging.",
        "Error strings should be lowercase and not punctuated like sentences (style).",
    ],
    example='''package main

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
}''',
    output="load 42: not found\ntrue",
    lab=[
        "Wrap ErrNotFound and assert with errors.Is.",
        "Define a typed ValidationError and retrieve it with errors.As.",
        "Compare wrongly with err.Error()== and then fix to Is/As.",
    ],
    py=[
        "Python exception types vs Go error values + wrapping.",
        "Do not parse error strings — use Is/As.",
        "`raise from` ≈ `%w` wrapping, but Go keeps it a value.",
    ],
    deepen="When wrapping, put the verb and resource first: `open config: %w` helps grepping logs.",
    guide="Wrap errors with %w and detect sentinels via errors.Is in the exercise stubs.",
    examples="Wrapped ErrNotFound must satisfy errors.Is(err, ErrNotFound) == true.",
)

set_e(
    11,
    why="Generics remove `any` casts for containers and algorithms while keeping type safety. Used well, they clarify APIs; used poorly, they obscure them.",
    core=[
        "Type parameters appear in `[T constraints]` on funcs and types.",
        "`comparable` enables == and map keys.",
        "Approximation elements `~int` include defined types based on int.",
        "Prefer interfaces when behavior is method-based; generics for structure.",
        "Inference often fills type args — specify when the compiler cannot.",
    ],
    example='''package main

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
}''',
    output="[2 4 6]",
    lab=[
        "Write generic Keys[K comparable, V any].",
        "Write Sum with a Number constraint union.",
        "Replace an `any` + type assert helper with a generic.",
    ],
    py=[
        "Python typing generics are optional; Go generics are enforced.",
        "No *args magic — constraints declare what operations exist.",
        "Don't genericize every function; concrete types stay readable.",
    ],
    deepen="The standard library uses generics in slices, maps helpers — read those packages as style guides.",
    guide="Implement a generic Map (or Keys) as specified by the exercise tests.",
    examples="Map ints→doubled ints; type parameters inferred from arguments.",
)

set_e(
    12,
    why="Tests are executable specs. Table-driven tests, fuzzing, and benchmarks turn Go's fast compiler into a design tool.",
    core=[
        "Table tests + t.Run give clear failure names.",
        "Fuzzing feeds random inputs to find edge cases.",
        "Benchmarks use b.N; compare with -benchmem.",
        "Test files are `_test.go`; external packages test public API.",
        "Prefer behavior assertions over mocking every collaborator.",
    ],
    example='''package clamp

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
}''',
    output="PASS (go test)",
    lab=[
        "Convert a single assertion test into a table.",
        "Add a fuzz target for a pure function.",
        "Run `go test -bench=. -benchmem` on a tiny Sum.",
    ],
    py=[
        "pytest fixtures ≈ careful constructor helpers — keep tests plain.",
        "No assert statement — use t.Fatalf / testify if your team allows.",
        "Time/network flakiness: inject clocks and interfaces like in Go.",
    ],
    deepen="A failing test name should tell you the behavior broken without reading the body.",
    guide="Make table-driven tests pass by implementing the stub under test.",
    examples="Each table row name appears in failures: `go test -v`.",
)

set_e(
    13,
    why="io.Reader and io.Writer unify files, sockets, buffers, and compression. Streaming I/O is how Go services stay memory-bounded.",
    core=[
        "Read/Write return (n, err); process n before assuming err.",
        "io.Copy moves bytes between Reader and Writer efficiently.",
        "bufio reduces syscalls for small reads/writes.",
        "io.EOF ends a stream — often expected, not fatal.",
        "defer Close() right after a successful Open.",
    ],
    example='''package main

import (
    "fmt"
    "io"
    "strings"
)

func main() {
    r := strings.NewReader("hello\\nworld\\n")
    n, err := io.Copy(io.Discard, r)
    fmt.Println(n, err)
}''',
    output="12 <nil>",
    lab=[
        "Count lines by scanning an io.Reader.",
        "Wrap a reader with bufio.Scanner.",
        "Use io.LimitReader to cap bytes read.",
    ],
    py=[
        "Python file objects ≈ Readers/Writers but Go interfaces compose more uniformly.",
        "Prefer streaming over `read().split` for large inputs.",
        "`with open` ≈ Open + defer Close (check Close errors when it matters).",
    ],
    deepen="Never ignore the n from Read when err != nil — partial data is common.",
    guide="Implement the reader-counting stub using io.Reader, not []byte whole-file assumptions.",
    examples="Counting lines/bytes from a strings.Reader should match tests.",
)

set_e(
    14,
    why="JSON and time are the lingua franca of services. Struct tags and time.Time correctness prevent subtle production outages.",
    core=[
        "encoding/json uses struct tags (`json:\"name\"`).",
        "Unknown fields are ignored by default; unknown types error.",
        "time.Time marshals as RFC3339 by default.",
        "Always store and compare times in UTC unless UI demands local.",
        "Use json.NewDecoder for streams; Marshal for small values.",
    ],
    example='''package main

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
}''',
    output='{"name":"Ada","age":36}\n{Ada 36}',
    lab=[
        "Round-trip a struct with tags.",
        "Omit empty fields with `omitempty`.",
        "Parse a timestamp with time.Parse(time.RFC3339, ...).",
    ],
    py=[
        "dict/json vs struct tags — unknown fields won't appear as attributes.",
        "datetime timezone naivety is worse in Python; still be careful in Go.",
        "snake_case JSON ↔ CamelCase Go fields via tags.",
    ],
    deepen="Validate after unmarshal — zero values can mean missing JSON fields.",
    guide="Implement JSON round-trip helpers to satisfy the exercise tests.",
    examples="Marshal then Unmarshal must preserve fields the tests check.",
)

set_e(
    15,
    why="context.Context carries deadlines and cancellation across API boundaries. It is how Go services stop work when clients disconnect.",
    core=[
        "Pass Context as the first parameter: `ctx context.Context`.",
        "WithCancel / WithTimeout / WithDeadline derive child contexts.",
        "Listen on ctx.Done(); return ctx.Err() when cancelled.",
        "Never store Context inside a struct long-term unless carefully justified.",
        "Values in context are for request-scoped data, not optional parameters.",
    ],
    example='''package main

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
}''',
    output="context deadline exceeded",
    lab=[
        "Create a WithTimeout and select on Done.",
        "Propagate ctx into a helper that sleeps and aborts early.",
        "Call cancel as soon as the parent no longer needs work.",
    ],
    py=[
        "No direct Python stdlib equivalent as pervasive as Context.",
        "Timeouts on requests should flow down — same idea as ctx.",
        "Avoid context.Value for required params — use arguments.",
    ],
    deepen="When a handler returns, cancel outstanding downstream calls so goroutines do not leak.",
    guide="Honor context cancellation/deadlines in the exercise function.",
    examples="When ctx times out, return ctx.Err() rather than hanging.",
)

set_e(
    16,
    why="Reflection powers encoding/json and some frameworks — but it is slow and bypasses the type checker. Know it to read libraries; avoid it in app code.",
    core=[
        "reflect.TypeOf / ValueOf inspect values at runtime.",
        "Kind distinguishes struct, slice, pointer, etc.",
        "Settable values require addressability rules.",
        "Prefer codegen or generics over reflective maps of fields.",
        "Interfaces + codegen usually beat reflect for performance.",
    ],
    example='''package main

import (
    "fmt"
    "reflect"
)

func main() {
    var x any = 42
    v := reflect.ValueOf(x)
    fmt.Println(v.Kind(), v.Int())
}''',
    output="int 42",
    lab=[
        "Print Kind of several values including a struct.",
        "Walk exported fields of a struct with reflect.Type.",
        "Rewrite a tiny reflective helper as a generic instead.",
    ],
    py=[
        "getattr/hasattr are common in Python; in Go they are a smell for app code.",
        "Duck typing at runtime ≈ interface{} + reflect — prefer interfaces.",
        "Performance: reflect is convenient and costly.",
    ],
    deepen="If you need reflect, isolate it behind a small package with heavy tests.",
    guide="Use reflect.Kind (or the stub's required API) to classify values as tests demand.",
    examples="Classify ints vs structs correctly per test cases.",
)

set_e(
    17,
    why="Idiomatic Go is a shared dialect: clarity, small interfaces, explicit errors. Teams move faster when style is predictable.",
    core=[
        "Accept interfaces, return structs.",
        "Make the zero value useful when possible.",
        "Short names for short scopes; longer names for package-level.",
        "Handle errors once; don't log-and-return repeatedly.",
        "gofmt/goimports are non-negotiable — style is automated.",
    ],
    example='''package main

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
}''',
    output="8080 <nil>",
    lab=[
        "Refactor a nested if pyramid into early returns.",
        "Rename variables to Go-ish short forms inside a small func.",
        "Run gofmt on a deliberately messy file.",
    ],
    py=[
        "PEP8 vs gofmt — Go ends style debates with a tool.",
        "EAFP in Python vs explicit err checks in Go.",
        "Classes everywhere vs funcs + small structs.",
    ],
    deepen="Read Effective Go and the Google Go Style Guide once; then practice by reviewing your own PRs.",
    guide="Implement the idiomatic parse helper so tests pass with clear errors.",
    examples="Valid input returns value; invalid returns descriptive error.",
)

set_e(
    18,
    why="Layout signals intent: library vs service, public API vs internal. Good structure reduces import cycles and onboarding time.",
    core=[
        "`cmd/` for mains, `internal/` for private packages, root for public libs.",
        "Avoid `pkg/` unless your org standardizes on it.",
        "Keep modules cohesive; split when versioning demands.",
        "One module per repo is common; multi-module is advanced.",
        "Configs and migrations live near the service that owns them.",
    ],
    example='''package main

import "fmt"

// Example layout commentary printed as a checklist.
func main() {
    layout := []string{"cmd/api", "internal/auth", "internal/store", "go.mod"}
    for _, p := range layout {
        fmt.Println(p)
    }
}''',
    output="cmd/api\ninternal/auth\ninternal/store\ngo.mod",
    lab=[
        "Sketch folders for a tiny HTTP API.",
        "Move a helper under internal/ and import it from cmd.",
        "Try importing internal from a sibling module — observe failure.",
    ],
    py=[
        "src-layout vs flat — Go favors module-root clarity.",
        "Django apps ≈ packages with clear boundaries.",
        "__init__.py noise does not exist; directories are packages with Go files.",
    ],
    deepen="Start simple. Premature micro-packages create cycles. Split on domain seams you can name.",
    guide="Answer layout quiz stubs / implement the tiny helper the exercise expects.",
    examples="Follow test expectations for package paths and exported names.",
)

set_e(
    19,
    why="Guessing at performance wastes time. pprof, the race detector, and a simple mental model of allocations keep optimizations honest.",
    core=[
        "`go test -race` finds data races.",
        "pprof profiles CPU, heap, goroutines, blockers.",
        "Avoid premature optimization; measure first.",
        "Allocations and interface/boxed conversions show up in profiles.",
        "Benchmark before and after with `go test -bench`.",
    ],
    example='''package main

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
}''',
    output="499500",
    lab=[
        "Write a BenchmarkSum and run -bench=.",
        "Introduce a deliberate race and catch it with -race.",
        "Read `go tool pprof` help once (even if you only skim).",
    ],
    py=[
        "cProfile ≈ pprof; Go's is tightly integrated with the runtime.",
        "GIL hides some races; Go encourages finding them with -race.",
        "Microbenchmarks lie without careful b.N loops — same in both languages.",
    ],
    deepen="Fix algorithmic complexity before micro-caching. O(n^2) beats any pprof tweak.",
    guide="Implement the sum/perf stub correctly; tests may check results more than timing.",
    examples="Correct Sum over a slice; then optionally benchmark locally.",
)

set_e(
    20,
    why="Docs and semver are how libraries age gracefully. Go doc comments and module versions are part of the public API.",
    core=[
        "Doc comments precede declarations and start with the name.",
        "`go doc` / pkg.go.dev render those comments.",
        "Semver: major for breaking changes; /v2+ in module paths.",
        "Compatibility guidelines: don't break callers casually.",
        "Examples in _test.go appear on pkg.go.dev.",
    ],
    example='''package greeter

// Hello returns a greeting for name.
// Empty name is allowed and produces "Hello, ".
func Hello(name string) string {
    return "Hello, " + name
}''',
    output='go doc → documents Hello',
    lab=[
        "Add a doc comment and run `go doc`.",
        "Write an ExampleHello test function.",
        "Skim Go module versioning docs for /v2.",
    ],
    py=[
        "docstrings vs Go doc comments — placement and tooling differ.",
        "CalVer vs SemVer — Go modules expect Semver.",
        "Type hints as docs ≠ compile-enforced API stability.",
    ],
    deepen="Treat exported names as forever once tagged v1. Prefer additive changes.",
    guide="Satisfy the docs/comment exercise — often about exporting and commenting correctly.",
    examples="Tests may check behavior of documented helpers.",
)

set_e(
    21,
    why="Complexity literacy stops you from shipping accidental O(n^2) loops in hot paths. Recursion and Big-O are tools for designing algorithms in Go.",
    core=[
        "Count dominant operations as n grows.",
        "Recursion needs base cases and progress toward them.",
        "Memoization trades memory for time.",
        "Prefer iterative forms when stack depth worries you.",
        "Measure with benchmarks when constants matter.",
    ],
    example='''package main

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

func main() { fmt.Println(Fib(10)) }''',
    output="55",
    lab=[
        "Implement iterative Fib; compare to naive recursive for n=40 timing.",
        "Estimate complexity of nested loops in a small snippet.",
        "Rewrite recursion as an explicit stack.",
    ],
    py=[
        "Same Big-O ideas; Go's recursion depth limits still apply.",
        "list append amortizes like Go append.",
        "Prefer clarity first, then complexity improvements with tests.",
    ],
    deepen="Interviewers care that you can discuss trade-offs while writing correct Go.",
    guide="Implement Fib (or the drill's function) efficiently enough for tests.",
    examples="Fib(10)→55; large n must finish quickly if tests set limits.",
)

set_e(
    22,
    why="Sorting and searching are building blocks for indexes, schedulers, and caches. Go's sort package and binary search repay fluency.",
    core=[
        "sort.Ints / sort.Slice with less functions.",
        "Binary search needs sorted order — verify invariants.",
        "stable vs unstable sorts matter for tie-breaking.",
        "search returns index or insertion point patterns.",
        "Custom order via sort.Interface or Slice.",
    ],
    example='''package main

import (
    "fmt"
    "sort"
)

func main() {
    xs := []int{5, 1, 3}
    sort.Ints(xs)
    i := sort.SearchInts(xs, 3)
    fmt.Println(xs, i)
}''',
    output="[1 3 5] 1",
    lab=[
        "Sort structs by a field with sort.Slice.",
        "Binary search for a target; handle not-found.",
        "Compare stable vs unstable with equal keys.",
    ],
    py=[
        "list.sort vs sorted; Go sorts in place commonly.",
        "bisect module ≈ sort.Search.",
        "key= functions ≈ less closures in sort.Slice.",
    ],
    deepen="When data is huge, consider whether you need a full sort or a heap/selection.",
    guide="Implement search/sort helpers to match exercise tests.",
    examples="Sorted inputs + Search return the expected index.",
)

set_e(
    23,
    why="Linked structures, stacks, and queues appear in parsers, schedulers, and BFS. Implementing them in Go clarifies pointers and ownership.",
    core=[
        "Nodes hold values and pointers to other nodes.",
        "Stacks: push/pop at one end; queues: FIFO.",
        "Nil terminates lists; always check before deref.",
        "Slices often beat linked lists for cache locality.",
        "Know both: interviews and specialized allocators still use links.",
    ],
    example='''package main

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
}''',
    output="2 1",
    lab=[
        "Implement stack with a slice backing.",
        "Implement a queue with head index or container/list.",
        "Draw pointer boxes for a 3-node linked list.",
    ],
    py=[
        "collections.deque ≈ efficient queue; Go slices work if careful.",
        "No pointers in Python — references everywhere.",
        "Linked lists are rarer in both languages for general storage.",
    ],
    deepen="Prefer slice-based stacks/queues unless you need mid-list splicing.",
    guide="Implement stack operations required by tests (push/pop/peek).",
    examples="LIFO order must hold across a sequence of ops.",
)

set_e(
    24,
    why="Trees and heaps power priority queues, schedulers, and hierarchical configs. Binary heaps give cheap extract-min.",
    core=[
        "Binary tree: left/right children; traverse inorder/preorder/postorder.",
        "Heap property: parent ≤ children (min-heap) or ≥ (max-heap).",
        "container/heap requires Push/Pop methods on a type.",
        "Priority queues schedule work by urgency.",
        "Balanced trees (overview) keep operations logarithmic.",
    ],
    example='''package main

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
}''',
    output="1",
    lab=[
        "Init a min-heap and pop in order.",
        "Implement a binary tree Insert for ints.",
        "Traverse and collect values.",
    ],
    py=[
        "heapq ≈ container/heap with more ceremony in Go.",
        "dataclasses for nodes vs structs.",
        "Recursion for traversal is fine for shallow trees.",
    ],
    deepen="For scheduling, store (priority, sequence, item) to keep ties deterministic.",
    guide="Implement heap/tree helpers so extract-min / traversal tests pass.",
    examples="Popping from a min-heap yields sorted ascending order.",
)

set_e(
    25,
    why="Graphs model networks, dependencies, and workflows. BFS/DFS are the default tools for reachability and shortest unweighted paths.",
    core=[
        "Represent graphs with adjacency lists: map[T][]T.",
        "BFS uses a queue; DFS uses stack/recursion.",
        "Mark visited to avoid cycles.",
        "Unweighted shortest path = BFS layers.",
        "Directed vs undirected changes edge insertion.",
    ],
    example='''package main

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
}''',
    output="[A B C D]",
    lab=[
        "BFS a small graph; print visit order.",
        "DFS recursive and iterative.",
        "Compute unweighted distance via BFS layers.",
    ],
    py=[
        "Same algorithms; Go maps+slices are the usual adjacency structure.",
        "collections.deque vs slice queue (O(n) head pop — ok for learning).",
        "NetworkX hides representation — implement by hand here.",
    ],
    deepen="For weighted shortest paths, Dijkstra comes next — know when BFS is enough.",
    guide="Implement BFS (or the exercise's graph walk) to match expected visit order.",
    examples="From A in A→B,C; B→D order starts with A then neighbors.",
)

set_e(
    26,
    why="Hashing underpins maps, caches, and probabilistic filters. Bloom filters trade a false-positive rate for tiny memory — classic infra tool.",
    core=[
        "Hash functions distribute keys; collisions are normal.",
        "Go maps hide hashing; understand load and resizing conceptually.",
        "Bloom filters: insert sets bits; query may false-positive, never false-negative (for basic blooms).",
        "Choose k hash functions / bitset size from expected n and error rate.",
        "Cryptographic vs non-crypto hashes — don't confuse them.",
    ],
    example='''package main

import (
    "fmt"
    "hash/fnv"
)

func hash(s string) uint64 {
    h := fnv.New64a()
    _, _ = h.Write([]byte(s))
    return h.Sum64()
}

func main() { fmt.Println(hash("go") != 0) }''',
    output="true",
    lab=[
        "Hash strings with FNV and print distribution buckets.",
        "Sketch a tiny bitset Bloom with two hashes.",
        "Demonstrate a false positive on purpose with a tiny filter.",
    ],
    py=[
        "hash() randomization in Python vs stable FNV here.",
        "set membership is exact; Bloom is probabilistic.",
        "Don't use MD5 for security; fine for demos of distribution.",
    ],
    deepen="In caches, hashing also means key design: canonical serialization before hash.",
    guide="Implement the bloom/hash stub per tests (likely Add/MightContain).",
    examples="After Add(x), MightContain(x) is true; fresh keys may false-positive.",
)

set_e(
    27,
    why="Dynamic programming turns exponential search into polynomial tables. In infra, DP thinking shows up in scheduling and path problems.",
    core=[
        "Identify overlapping subproblems + optimal substructure.",
        "Bottom-up tables vs top-down memo maps.",
        "Define state clearly: dp[i] meaning in one sentence.",
        "Watch index off-by-ones and base cases.",
        "Reconstruct solutions by storing choices, not only values.",
    ],
    example='''package main

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

func main() { fmt.Println(Climb(5)) }''',
    output="8",
    lab=[
        "Climbing stairs bottom-up.",
        "Memoize a recursive solution with a map.",
        "Write the dp state meaning as a comment first.",
    ],
    py=[
        "functools.lru_cache ≈ map memo in Go.",
        "Same recurrence, different syntax.",
        "Be explicit about mutation of DP slices.",
    ],
    deepen="If you cannot name the state, you are not ready to code the loop.",
    guide="Implement the DP function (e.g. climb/knapsack-style) to match tests.",
    examples="Climb(5)→8 for the classic 1/2 step problem.",
)

set_e(
    28,
    why="Mixed drills build fluency: hashing + two pointers + sorting under time pressure. This is how interview and on-call problem solving get faster.",
    core=[
        "Clarify inputs/outputs and constraints before coding.",
        "Start with brute force, then improve with maps/sorts.",
        "Two-sum pattern: map value→index.",
        "Write tests first for edge cases: empty, duplicates, negatives.",
        "Idiomatic Go: early returns, no clever one-liners.",
    ],
    example='''package main

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

func main() { fmt.Println(TwoSum([]int{2, 7, 11, 15}, 9)) }''',
    output="[0 1]",
    lab=[
        "Implement two-sum with a map.",
        "Add tests for not-found and duplicates.",
        "Time a naive O(n^2) vs map solution.",
    ],
    py=[
        "Same patterns; dict vs map syntax.",
        "enumerate ≈ for i, v := range.",
        "Return tuples vs arrays/slices — match the API.",
    ],
    deepen="Narrate complexity out loud while coding — it catches bad approaches early.",
    guide="Implement TwoSum (or the drill set) exactly as tests specify indices.",
    examples="TwoSum([2,7,11,15],9)→[0,1].",
)

set_e(
    29,
    why="Goroutines are cheap concurrent functions scheduled by the Go runtime. They are why Go shines for servers and pipelines — used carefully.",
    core=[
        "`go f()` starts a goroutine; it may outlive the caller.",
        "The scheduler multiplexes goroutines onto OS threads.",
        "Always have an exit condition — leaks are real.",
        "sync.WaitGroup waits for a set of goroutines.",
        "Do not share mutable state without sync (next lessons).",
    ],
    example='''package main

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
}''',
    output="hi 0\nhi 1\nhi 2\n(order may vary)",
    lab=[
        "Launch N goroutines with WaitGroup.",
        "Forget Done once and observe a hang — then fix.",
        "Pass loop variable as an argument (classic gotcha in older Go).",
    ],
    py=[
        "threading.Thread is heavy; goroutines are lighter.",
        "asyncio is cooperative; Go is concurrent with a scheduler.",
        "GIL limits CPU threads; Go uses multiple OS threads freely.",
    ],
    deepen="Structure concurrency as trees of tasks with clear cancellation (context).",
    guide="Use WaitGroup (or the exercise API) so all goroutines finish before return.",
    examples="Tests wait for results; hanging means missing Done/cancel.",
)

set_e(
    30,
    why="Channels synchronize and communicate. Select lets you wait on multiple events — timeouts, cancellation, and data — in one place.",
    core=[
        "chan T is typed; make(chan T, n) sets buffer size.",
        "Send/receive block until the other side is ready (unbuffered).",
        "close signals no more sends; range over chan until closed.",
        "select chooses among ready cases; default is non-blocking.",
        "Prefer ownership: only the sender closes.",
    ],
    example='''package main

import "fmt"

func main() {
    ch := make(chan int, 2)
    ch <- 1
    ch <- 2
    close(ch)
    for v := range ch {
        fmt.Println(v)
    }
}''',
    output="1\n2",
    lab=[
        "Pipeline: generator → square → print with channels.",
        "select with time.After for a timeout.",
        "Show deadlock with unbuffered send and no receiver.",
    ],
    py=[
        "queue.Queue ≈ buffered channel, but channels also sync.",
        "No select equivalent as clean as Go's.",
        "Generators vs channel producers — close when done.",
    ],
    deepen="Pipelines: each stage closes its output when the input is drained.",
    guide="Wire channel pipeline/select behavior required by tests.",
    examples="Values sent must be received; closed channels terminate range.",
)

set_e(
    31,
    why="Mutexes protect shared memory. Atomics handle simple counters without heavy locks. Choosing wrongly causes races or slowdowns.",
    core=[
        "sync.Mutex: Lock/Unlock around critical sections.",
        "RWMutex for read-heavy workloads.",
        "sync/atomic for integers and pointers with care.",
        "Never copy a struct containing a Mutex after first use.",
        "`go test -race` is mandatory for concurrent code.",
    ],
    example='''package main

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
}''',
    output="1000",
    lab=[
        "Increment without mutex; run -race.",
        "Fix with Mutex; confirm race gone.",
        "Replace with atomic.AddInt64 and compare.",
    ],
    py=[
        "threading.Lock ≈ Mutex.",
        "GIL can mask races — Go will not.",
        "Prefer channels when communicating ownership; mutex when sharing state.",
    ],
    deepen="Keep critical sections tiny. Do I/O outside the lock.",
    guide="Protect shared counters/state so tests pass under race detector.",
    examples="Final counter equals number of increments.",
)

set_e(
    32,
    why="Worker pools bound concurrency. Fan-in/out and backpressure keep systems stable under load instead of spawning unbounded goroutines.",
    core=[
        "Fixed workers pull jobs from a channel.",
        "Buffered channels provide limited queueing (backpressure).",
        "Fan-out: many workers; fan-in: merge results.",
        "Close job channels to signal completion.",
        "Context cancels in-flight work when the caller leaves.",
    ],
    example='''package main

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
}''',
    output="2\n4\n6\n8\n10\n(order may vary)",
    lab=[
        "Build a 3-worker pool doubling ints.",
        "Lower buffer to 0 and observe backpressure.",
        "Add context cancel mid-flight.",
    ],
    py=[
        "concurrent.futures.Executor ≈ worker pool.",
        "Unbounded thread spawns ≈ unbounded go statements — both bad.",
        "Queue maxsize ≈ buffered channel capacity.",
    ],
    deepen="Tune worker count with benchmarks and external limits (DB pools, CPU).",
    guide="Implement pool semantics: workers process all jobs; results complete.",
    examples="Doubling pool returns 2*job for each input.",
)

set_e(
    33,
    why="Deadlocks and races are production killers. Cancellation patterns and the race detector teach you to design for failure.",
    core=[
        "Deadlock: all goroutines wait forever — often lock order or channel cycles.",
        "Race: unsynchronized memory access — undefined behavior.",
        "Always acquire locks in a consistent global order.",
        "Propagate context cancellation to break waits.",
        "Prefer ownership transfer via channels to shared mutable state when possible.",
    ],
    example='''package main

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
}''',
    output="cancelled",
    lab=[
        "Create a channel deadlock; fix with buffer or goroutine.",
        "Run a racy counter under -race.",
        "Add timeout select to a blocking receive.",
    ],
    py=[
        "Deadlocks exist in threading too; Go makes them more visible.",
        "Race detector is a superpower — use it in CI.",
        "asyncio cancellation ≈ context cancel.",
    ],
    deepen="On deadlock, print goroutine stacks (SIGQUIT / panic) and look for who waits on what.",
    guide="Ensure cancellation paths return instead of hanging; fix racey access.",
    examples="Functions return when ctx done; tests fail on timeout hang.",
)

set_e(
    34,
    why="Concurrent algorithms combine correct partitioning with sync. Parallel sum/map patterns prepare you for real data pipelines.",
    core=[
        "Split input into shards; process independently; merge.",
        "Avoid false sharing conceptually; keep shards separate.",
        "WaitGroup + results channel is a common merge pattern.",
        "Correctness first, then speedup measurements.",
        "Not all problems parallelize — Amdahl's law.",
    ],
    example='''package main

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

func main() { fmt.Println(ParSum([]int{1, 2, 3, 4}, 2)) }''',
    output="10",
    lab=[
        "Parallel sum with 1 vs 4 workers; check equal results.",
        "Benchmark both.",
        "Break merge by double-closing a channel — then fix.",
    ],
    py=[
        "multiprocessing vs goroutines — different memory models.",
        "Shared-memory parallel needs locks in both.",
        "Chunking strategy matters more than language.",
    ],
    deepen="For tiny inputs, parallel overhead wins — gate on size.",
    guide="Implement parallel aggregation matching sequential results.",
    examples="ParSum equals Sum for the same slice.",
)

set_e(
    35,
    why="net/http is production-grade in the standard library. Understanding handlers, clients, and timeouts is baseline for Go services.",
    core=[
        "http.HandleFunc / ServeMux route requests.",
        "Handlers write to ResponseWriter; read from Request.",
        "Clients should set Timeouts — never use bare default in prod.",
        "context on Request cancels when clients disconnect.",
        "ListenAndServe blocks; shutdown gracefully later lessons.",
    ],
    example='''package main

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
}''',
    output="200 ok",
    lab=[
        "Write /healthz returning 200 ok.",
        "httptest a handler without listening on a port.",
        "Set http.Client{Timeout: 2*time.Second}.",
    ],
    py=[
        "Flask/FastAPI vs net/http — stdlib is enough for many services.",
        "requests defaults vs explicit Client timeouts.",
        "WSGI sync model vs Go's per-request goroutines.",
    ],
    deepen="Always set timeouts on http.Client in production. Prefer httptest for handler unit tests so CI needs no open ports.",
    guide="Implement a health handler (or client helper) so tests get 200/ok bodies.",
    examples="GET health returns status 200 and body matching tests.",
)

set_e(
    36,
    why="REST middleware and auth are how you cross-cut logging, authn, and limits without copying code into every handler.",
    core=[
        "Middleware is `func(http.Handler) http.Handler`.",
        "Chain middleware outward-in carefully.",
        "Auth: validate tokens/headers early; set context values sparingly.",
        "Return proper status codes: 401/403/400 distinctions.",
        "Keep handlers thin: decode → validate → service → encode.",
    ],
    example='''package main

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
}''',
    output="1 hi",
    lab=[
        "Write middleware that rejects missing Authorization.",
        "Chain logging + auth middleware.",
        "Map service errors to HTTP statuses.",
    ],
    py=[
        "Decorators ≈ middleware.",
        "Flask before_request hooks ≈ middleware chains.",
        "Keep crypto out of handlers — use small auth packages.",
    ],
    deepen="Prefer explicit dependency injection of auth services over global state.",
    guide="Implement middleware that enforces headers/auth as tests describe.",
    examples="Missing token → 401; valid → handler body.",
)

set_e(
    37,
    why="gRPC and protobuf give typed, efficient RPCs across languages. Go is a first-class citizen in that ecosystem.",
    core=[
        "Protobuf defines messages and services in .proto files.",
        "protoc + plugins generate Go types and stubs.",
        "gRPC supports unary and streaming RPCs.",
        "Errors use status codes, not only ad-hoc strings.",
        "Version your APIs; avoid breaking field numbers.",
    ],
    example='''package main

import "fmt"

// Conceptual: generated code looks like this shape.
type HelloRequest struct{ Name string }
type HelloReply struct{ Message string }

func SayHello(req HelloRequest) HelloReply {
    return HelloReply{Message: "hello " + req.Name}
}

func main() { fmt.Println(SayHello(HelloRequest{Name: "Ada"}).Message) }''',
    output="hello Ada",
    lab=[
        "Skim a .proto example online and map fields to Go structs.",
        "Implement a pure Go stand-in for a unary RPC handler.",
        "List three gRPC status codes you would use.",
    ],
    py=[
        "grpcio similar concepts; generated stubs differ.",
        "dict payloads vs typed protobuf messages.",
        "Field numbers are the compatibility contract — like JSON keys but stricter.",
    ],
    deepen="Start with unary RPCs; add streaming when a real need appears.",
    guide="Implement the sketch/stub service method the tests call.",
    examples="SayHello-style funcs return expected messages.",
)

set_e(
    38,
    why="database/sql is a toolkit, not an ORM. Correct parameters, transactions, and connection pools keep data safe under concurrency.",
    core=[
        "Use placeholders `?`/`$1` — never string-build SQL.",
        "Query/QueryRow/Exec and always check errors.",
        "Tx: Begin → work → Commit/Rollback.",
        "sql.DB is a pool; SetMaxOpenConns thoughtfully.",
        "Scan into variables carefully; NULL needs sql.Null*.",
    ],
    example='''package main

import "fmt"

// Conceptual parameterized query shape:
func FindName(id int) string {
    // db.QueryRow("SELECT name FROM users WHERE id=$1", id).Scan(&name)
    _ = id
    return "Ada"
}

func main() { fmt.Println(FindName(1)) }''',
    output="Ada",
    lab=[
        "Write a function that takes query args separately from SQL.",
        "Sketch transaction rollback on error.",
        "List what happens if you ignore Rows.Err().",
    ],
    py=[
        "DB-API placeholders ≈ Go's — still don't f-string SQL.",
        "ORMs hide pools; learn sql.DB semantics anyway.",
        "context.Context on QueryContext for timeouts.",
    ],
    deepen="Migrations belong in versioned files; apps should not ad-hoc ALTER in request paths.",
    guide="Implement parameterized helpers / scans as the exercise defines.",
    examples="Queries use args slices; tests check SQL shape or results mocks.",
)

set_e(
    39,
    why="Caching and idempotency protect databases and make retries safe. Cache-aside and Redis patterns appear in every production stack.",
    core=[
        "Cache-aside: read cache → miss → load DB → fill cache.",
        "Set TTLs; plan invalidation on writes.",
        "Idempotency keys dedupe retried side effects.",
        "Stampede protection: singleflight or locks.",
        "Redis is a tool — model keys carefully with namespaces.",
    ],
    example='''package main

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
}''',
    output="v v 1",
    lab=[
        "Implement in-memory cache-aside.",
        "Add TTL by storing expiry time.",
        "Simulate retries with an idempotency set.",
    ],
    py=[
        "functools.cache / Redis clients — same patterns.",
        "Mutable default dicts vs make(map).",
        "Think about consistency: cache can be stale.",
    ],
    deepen="Document consistency: stale reads vs always-fresh after write.",
    guide="Implement cache-aside or idempotency stub per tests.",
    examples="Second read does not re-load; idempotent submit once.",
)

set_e(
    40,
    why="Logs, metrics, and traces explain production. Structured observability turns incidents from guesswork into evidence.",
    core=[
        "Structured logs: key=value or JSON fields.",
        "Metrics: counters, histograms, gauges.",
        "Traces: spans across services with context propagation.",
        "Correlate with request IDs.",
        "Cardinality kills metrics systems — label carefully.",
    ],
    example='''package main

import (
    "log/slog"
    "os"
)

func main() {
    logger := slog.New(slog.NewJSONHandler(os.Stdout, nil))
    logger.Info("request done", "route", "/health", "ms", 3)
}''',
    output='{"time":"...","level":"INFO","msg":"request done","route":"/health","ms":3}',
    lab=[
        "Log with slog JSON handler.",
        "Increment a conceptual counter around a function.",
        "Pass a request ID through context (sketch).",
    ],
    py=[
        "logging/structlog ≈ slog.",
        "Prometheus client patterns similar.",
        "Print debugging does not scale — structure early.",
    ],
    deepen="ALERT on symptoms (error rate, latency) not only causes.",
    guide="Implement logging helper or metric wrapper the tests expect.",
    examples="Logs contain required fields; helpers format consistently.",
)

set_e(
    41,
    why="Multi-stage Docker builds keep Go images tiny and secure. Containers are how Go services ship.",
    core=[
        "Build stage with golang image; runtime with distroless/scratch/alpine.",
        "COPY go.mod/sum first for layer caching.",
        "CGO_ENABLED=0 for static binaries when possible.",
        "Run as non-root; expose minimal ports.",
        "Healthchecks and read-only rootfs where practical.",
    ],
    example='''package main

import "fmt"

func main() {
    // Inside container this binary is often /app
    fmt.Println("listening :8080")
}''',
    output="listening :8080",
    lab=[
        "Write a multi-stage Dockerfile sketch on paper.",
        "List what NOT to COPY (secrets, .git).",
        "Explain why go mod download is a separate layer.",
    ],
    py=[
        "venv in images vs static Go binaries — Go wins size often.",
        "Same Docker layer caching ideas.",
        "GIL/process model differs; still one process per container usually.",
    ],
    deepen="Pin base image digests for supply-chain hygiene.",
    guide="Complete Dockerfile-oriented stubs or config strings tests check.",
    examples="Multi-stage markers / binary path expectations in tests.",
)

set_e(
    42,
    why="Kubernetes controllers reconcile desired vs actual state. Go and client-go dominate this ecosystem.",
    core=[
        "Reconcile loops: read state → diff → act → repeat.",
        "Informers/caches reduce API server load.",
        "Idempotent actions: safe to retry.",
        "Status subresources report progress.",
        "Leader election for active/passive controllers.",
    ],
    example='''package main

import "fmt"

func Reconcile(desired, actual int) string {
    if actual == desired {
        return "ok"
    }
    return "update"
}

func main() { fmt.Println(Reconcile(3, 1)) }''',
    output="update",
    lab=[
        "Write a pure reconcile decision function.",
        "List what makes an action idempotent.",
        "Sketch an informer event → queue → worker.",
    ],
    py=[
        "Operators exist in other langs; Go is the default for k8s.",
        "Same reconcile idea as config management loops.",
        "Watch API vs poll — prefer events with resync.",
    ],
    deepen="Never block forever in reconcile without context; requeue with backoff.",
    guide="Implement reconcile decision stubs matching tests.",
    examples="desired==actual → ok; else → update action.",
)

set_e(
    43,
    why="Cloud SDKs need retries, pagination, and config from env. Robust clients survive transient faults.",
    core=[
        "Retry transient errors with exponential backoff + jitter.",
        "Pagination: loop until next token empty.",
        "Config via env/flags; never hardcode secrets.",
        "Idempotent retries for safe verbs.",
        "Timeouts on every outbound call.",
    ],
    example='''package main

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
}''',
    output="100\n200\n400\n800",
    lab=[
        "Implement backoff with max cap.",
        "Paginate a fake NextToken API.",
        "Read a config struct from env vars.",
    ],
    py=[
        "tenacity ≈ custom backoff in Go.",
        "boto3 pagination ≈ token loops.",
        "Same twelve-factor config ideals.",
    ],
    deepen="Distinguish retryable (429/5xx) from permanent (400) errors.",
    guide="Implement retry/backoff helper per tests.",
    examples="Attempt n waits base*2^n (or as specified).",
)

set_e(
    44,
    why="Reliability patterns — timeouts, circuit breakers, graceful shutdown — keep incidents small and deploys safe.",
    core=[
        "Timeouts everywhere: clients, servers, DB.",
        "Circuit breakers stop calling unhealthy deps.",
        "Graceful shutdown: stop intake, drain, then exit.",
        "signal.Notify for SIGTERM in containers.",
        "Load shedding beats cascading failure.",
    ],
    example='''package main

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
}''',
    output="shutdown",
    lab=[
        "Simulate SIGTERM with a cancel channel.",
        "Add a timeout around a slow function.",
        "Sketch circuit breaker states: closed/open/half-open.",
    ],
    py=[
        "signal handling similar; asyncio cancellation related.",
        "Flask often lacks std graceful shutdown — learn Go's.",
        "Fail-fast vs retry — product decision.",
    ],
    deepen="Kubernetes sends SIGTERM then SIGKILL — drain within terminationGracePeriodSeconds.",
    guide="Implement shutdown/timeout helpers so tests observe clean stops.",
    examples="After stop signal, function returns promptly.",
)

set_e(
    45,
    why="Numerics with gonum enable scientific and ML-adjacent work in Go: vectors, matrices, and stats without leaving the language.",
    core=[
        "Vectors/matrices are first-class for linear algebra.",
        "Dot products and norms appear in similarity search.",
        "Floating error: use tolerances in tests.",
        "Prefer well-tested libraries over hand-rolled BLAS.",
        "Shape mismatches should error early.",
    ],
    example='''package main

import "fmt"

func Dot(a, b []float64) float64 {
    var s float64
    for i := range a {
        s += a[i] * b[i]
    }
    return s
}

func main() { fmt.Println(Dot([]float64{1, 2}, []float64{3, 4})) }''',
    output="11",
    lab=[
        "Implement Dot and L2 norm.",
        "Test with an epsilon comparison.",
        "Multiply a tiny matrix by a vector by hand in Go.",
    ],
    py=[
        "numpy is richer; Go/gonum is explicit and deployable in one binary.",
        "Broadcasting magic vs explicit loops — clarity wins in Go.",
        "Same floating-point caveats.",
    ],
    deepen="For heavy training, Python/CUDA still dominates; Go shines at serving and glue.",
    guide="Implement Dot (or gonum-backed stub) matching tests.",
    examples="Dot([1,2],[3,4])→11.",
)

set_e(
    46,
    why="ML pipelines in Go are often ETL, batching, and feature assembly before a model API. Reliable batching reduces cost and latency variance.",
    core=[
        "Batch records to amortize model call overhead.",
        "Deterministic feature transforms with tests.",
        "Backpressure when downstream is slow.",
        "Schema discipline: version your features.",
        "Idempotent job processing for retries.",
    ],
    example='''package main

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

func main() { fmt.Println(Batch([]int{1, 2, 3, 4, 5}, 2)) }''',
    output="[[1 2] [3 4] [5]]",
    lab=[
        "Implement Batch.",
        "Add a feature hash function for strings.",
        "Simulate a worker that processes batches from a channel.",
    ],
    py=[
        "pandas batching vs slice batching.",
        "Airflow/Dagster orchestration vs Go workers.",
        "Same need for deterministic transforms.",
    ],
    deepen="Log batch sizes and latency histograms — they diagnose model cost issues.",
    guide="Implement batching helpers per tests.",
    examples="Batch size 2 on 5 items yields 3 batches, last shorter.",
)

set_e(
    47,
    why="Model APIs stream tokens via HTTP/SSE. Go clients must parse streams and cancel cleanly when users abort.",
    core=[
        "SSE: lines of `data:` events separated by blank lines.",
        "Decode incrementally from a Reader.",
        "Honor context cancel mid-stream.",
        "Retries differ for streaming vs unary calls.",
        "Auth headers and timeouts still apply.",
    ],
    example='''package main

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
}''',
    output="[hi there]",
    lab=[
        "Parse a multi-event SSE string.",
        "Stop parsing when ctx is done (sketch).",
        "Handle `[DONE]` sentinel used by some APIs.",
    ],
    py=[
        "httpx/stream vs bufio.Scanner.",
        "Same SSE framing.",
        "Generators yield chunks; Go channels can too.",
    ],
    deepen="Always test with partial reads — real networks fragment events.",
    guide="Parse SSE data lines as the exercise tests specify.",
    examples='"data: hi\\n\\n" -> ["hi"].',
)

set_e(
    48,
    why="Embeddings power semantic search. Cosine similarity and vector stores are core AI infra skills in Go services.",
    core=[
        "Embeddings are float vectors representing meaning.",
        "Cosine similarity = dot/(||a||||b||).",
        "Normalize vectors to make dot product = cosine.",
        "Indexes (overview): brute force → ANN libraries.",
        "Dimension mismatches must error.",
    ],
    example='''package main

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

func main() { fmt.Println(Cosine([]float64{1, 0}, []float64{1, 0})) }''',
    output="1",
    lab=[
        "Implement Cosine; test orthogonal vectors → 0.",
        "Find argmax similarity in a tiny corpus.",
        "L2-normalize a vector in place.",
    ],
    py=[
        "numpy cosine vs explicit loops.",
        "Same math; Go forces dimension checks you might skip in notebooks.",
        "FAISS/Python vs Go ANN bindings — know the trade.",
    ],
    deepen="Store the model name + dimension with vectors — embeddings are not interchangeable.",
    guide="Implement cosine/similarity helpers for the exercise.",
    examples="Identical unit vectors → similarity 1.",
)

set_e(
    49,
    why="RAG systems chunk documents, embed, retrieve, then generate. Go is excellent for the retrieval service path.",
    core=[
        "Chunk with overlap to preserve context.",
        "Embed chunks offline or online.",
        "Retrieve top-k by similarity.",
        "Prompt = instructions + retrieved context + question.",
        "Cite sources for trustworthiness.",
    ],
    example='''package main

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

func main() { fmt.Println(Chunk("abcdefghij", 4)) }''',
    output="[abcd efgh ij]",
    lab=[
        "Chunk with overlap (e.g., size 4, overlap 1).",
        "Retrieve top-1 from a toy map of embeddings.",
        "Build a prompt string from docs + question.",
    ],
    py=[
        "LangChain glue vs explicit Go pipelines — explicit often clearer for prod.",
        "Same RAG diagram.",
        "Evaluate retrieval quality separately from generation.",
    ],
    deepen="Bad chunking dominates RAG quality more than model choice for many corpora.",
    guide="Implement chunk/retrieve helpers tests require.",
    examples="Chunk lengths respect size; last chunk shorter.",
)

set_e(
    50,
    why="Inference serving needs queues and batching so GPUs/CPUs stay busy without melting under spikes.",
    core=[
        "Queue requests; workers pull batches.",
        "Max batch size and max wait time trade latency/throughput.",
        "Backpressure: reject or shed when queue is full.",
        "Timeouts return errors to clients.",
        "Sidecars often host models; Go handles orchestration.",
    ],
    example='''package main

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
}''',
    output="2 1",
    lab=[
        "Implement CollectBatch.",
        "Add a timer-based flush sketch.",
        "Return an error when queue length exceeds capacity.",
    ],
    py=[
        "Serving stacks (Triton etc.) — Go often fronts them.",
        "asyncio queues ≈ channel queues.",
        "Measure p99 latency, not only averages.",
    ],
    deepen="Load test with realistic prompt sizes — token counts drive cost.",
    guide="Implement queue/batch helpers for inference stubs.",
    examples="Batch max size respected; remainder stays queued.",
)

set_e(
    51,
    why="Agents loop: model proposes a tool call → your code runs it → result returns to the model. Go's type safety helps keep tools honest.",
    core=[
        "Tools are typed functions with JSON schemas.",
        "Loop with a max step count to prevent runaway costs.",
        "Validate tool args before execution.",
        "Sandbox dangerous tools (shell, network).",
        "Log each step for auditability.",
    ],
    example='''package main

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

func main() { fmt.Println(RunTool(Call{Tool: "echo", Arg: "hi"})) }''',
    output="hi",
    lab=[
        "Dispatch a tool by name.",
        "Stop after N steps even if model continues.",
        "Reject unknown tools with an error string.",
    ],
    py=[
        "LangChain agents ≈ same loop.",
        "Dynamic getattr tool calling is riskier — Go maps of funcs are clearer.",
        "Same need for hard timeouts.",
    ],
    deepen="Treat tool results as untrusted input when feeding back to the model.",
    guide="Implement the agent loop/tool dispatch stubs.",
    examples="echo tool returns arg; unknown tool errors.",
)

set_e(
    52,
    why="Evals make AI systems engineering, not vibes. Harnesses score outputs so changes are measurable.",
    core=[
        "Golden sets: input → expected properties.",
        "Exact match, contains, regex, LLM-as-judge (careful).",
        "Track regressions in CI.",
        "Separate retrieval vs generation metrics for RAG.",
        "Seed randomness for determinism when possible.",
    ],
    example='''package main

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

func main() { fmt.Println(ScoreContains("hello world", "world")) }''',
    output="1",
    lab=[
        "Score a tiny golden set average.",
        "Add a case that fails; see average drop.",
        "Store results as JSON for a report.",
    ],
    py=[
        "pytest + eval frameworks — same discipline.",
        "Notebooks are not CI.",
        "Human eval samples still matter.",
    ],
    deepen="Optimize for the metric you measure — choose metrics that match user value.",
    guide="Implement scoring helpers for the eval harness exercise.",
    examples="Contains match → 1.0 else 0.0.",
)

set_e(
    53,
    why="The infra capstone stitches HTTP, middleware, context, and reliability into one service-shaped project.",
    core=[
        "Define routes, middleware, and config.",
        "Use context deadlines on outbound calls.",
        "Graceful shutdown on signal.",
        "Tests via httptest and table cases.",
        "README that explains how to run locally.",
    ],
    example='''package main

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
}''',
    output="ok",
    lab=[
        "Wire /healthz and one domain route.",
        "Add middleware request IDs.",
        "Write httptest coverage for happy + error paths.",
    ],
    py=[
        "Flask app factory ≈ main + NewServer constructor.",
        "Same need for tests without real ports.",
        "Deploy as a single static binary — Go advantage.",
    ],
    deepen="Ship vertical slices: one endpoint fully correct beats five stubs.",
    guide="Build the capstone API stubs until integration-style tests pass.",
    examples="Health and core handlers return expected codes/bodies.",
)

set_e(
    54,
    why="The algorithms capstone forces you to combine data structures under realistic constraints — search, graphs, or indexes.",
    core=[
        "Clarify the problem and invariants first.",
        "Choose representation (adj list, heap, map indexes).",
        "Test edge cases heavily.",
        "Document complexity in comments.",
        "Profile only after correctness.",
    ],
    example='''package main

import "fmt"

func Index(docs []string) map[string][]int {
    inv := map[string][]int{}
    for i, d := range docs {
        inv[d] = append(inv[d], i)
    }
    return inv
}

func main() { fmt.Println(Index([]string{"a", "b", "a"})) }''',
    output="map[a:[0 2] b:[1]]",
    lab=[
        "Build an inverted index.",
        "Query for documents containing a term.",
        "Add a simple rank by term frequency.",
    ],
    py=[
        "Same CS; Go types force explicit structures.",
        "dict.setdefault ≈ append to map slices.",
        "Prove correctness before optimizing.",
    ],
    deepen="Write a one-page design note before coding the capstone.",
    guide="Implement the search/graph engine pieces the tests name.",
    examples="Index + query returns expected doc IDs.",
)

set_e(
    55,
    why="The AI capstone combines embeddings, retrieval, and an HTTP API — a mini RAG service you can extend toward production.",
    core=[
        "Ingest → chunk → embed → store vectors.",
        "Query → embed → top-k → respond.",
        "Expose HTTP JSON endpoints with tests.",
        "Keep model client behind an interface for mocks.",
        "Evaluate with a tiny golden set.",
    ],
    example='''package main

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
}''',
    output="2",
    lab=[
        "Interface out Embedder and Retriever.",
        "httptest a /search endpoint.",
        "Add one eval case that must stay green.",
    ],
    py=[
        "FastAPI RAG demos vs Go's deployable binary.",
        "Mock embeddings with fixed vectors in tests.",
        "Same architecture diagram.",
    ],
    deepen="Production next steps: auth, persistence, observability, and real embedding APIs.",
    guide="Implement the mini RAG/search service stubs until tests pass end-to-end.",
    examples="Search returns expected doc IDs for fixture embeddings/texts.",
)


def guide_for(n: int, meta: dict) -> str:
    e = E[n]
    return e.get("guide") or (
        f"Implement the stubs in `exercises/{meta['slug']}/` until `go test` passes. "
        f"Behaviors map to **{meta['title']}**."
    )


def examples_for(n: int, meta: dict) -> str:
    e = E[n]
    return e.get("examples") or (
        "Copy patterns from the lesson worked examples. Match test expectations exactly."
    )


def body_for(n: int, meta: dict) -> str:
    e = E[n]
    prior = meta.get("body") or meta.get("concepts") or ""
    return build_body(
        meta["title"],
        e["why"],
        e["core"],
        e["example"],
        e["output"],
        e["lab"],
        e["py"],
        e.get("deepen", ""),
        prior=prior,
        pitfalls=meta.get("pitfalls") or [],
    )


def py_string(s: str) -> str:
    """Format a string as a Python triple-quoted literal (safe escapes)."""
    # Prefer """ ; if present, use '''; escape backslashes so \n in Go snippets
    # survives as two chars when the curriculum module is imported.
    esc = s.replace("\\", "\\\\")
    if '"""' in esc and "'''" in esc:
        return repr(s)
    if '"""' in esc:
        return "'''\n" + esc.replace("'''", "\\'\\'\\'") + "\n'''"
    return '"""\n' + esc + '\n"""'


def patch_generate_curriculum():
    path = SCRIPTS / "generate_curriculum.py"
    text = path.read_text(encoding="utf-8")
    # Apply expansions by appending override block (idempotent replace).
    marker = "\n# --- EXPANDED_BODIES_APPLIED ---\n"
    if marker in text:
        text = text.split(marker)[0].rstrip() + "\n"

    early = load("generate_curriculum", path)
    bodies = {}
    for m in early.MODULES:
        n = m["n"]
        bodies[n] = {
            "concepts": body_for(n, m),
            "exercise_guide": guide_for(n, m),
            "exercise_examples": examples_for(n, m),
            "readme": E[n].get("readme", m["ex"].get("readme", "")),
        }
        assert 3000 <= len(bodies[n]["concepts"]) <= 8000, (
            n,
            len(bodies[n]["concepts"]),
        )

    # Rewrite concepts inside each M( by regenerating MODULES assignments via runtime patch file section
    block = [marker, "def _apply_expansions():"]
    block.append("    expansions = {")
    for n, b in bodies.items():
        block.append(f"        {n}: {{")
        block.append(f'            "concepts": {py_string(b["concepts"])},')
        block.append(f'            "exercise_guide": {py_string(b["exercise_guide"])},')
        block.append(f'            "exercise_examples": {py_string(b["exercise_examples"])},')
        block.append(f'            "readme": {py_string(b["readme"])},')
        block.append("        },")
    block.append("    }")
    block.append("    for m in MODULES:")
    block.append("        e = expansions.get(m['n'])")
    block.append("        if not e:")
    block.append("            continue")
    block.append("        m['concepts'] = e['concepts']")
    block.append("        m['exercise_guide'] = e['exercise_guide']")
    block.append("        m['exercise_examples'] = e['exercise_examples']")
    block.append("        if isinstance(m.get('ex'), dict) and e.get('readme'):")
    block.append("            m['ex']['readme'] = e['readme']")
    block.append("")
    block.append("_apply_expansions()")
    block.append("")

    # Also inline-replace concepts in M() for human-readable source: replace each concepts triple-quote.
    # Safer: keep M() short stubs replaced by applying expansions into the concepts argument via regex per module order.
    new_text = text + "\n".join(block)

    # Better UX: replace concepts strings in M() calls so the field itself is expanded.
    # We'll rewrite file by reconstructing early modules from runtime after expansion.
    path.write_text(new_text, encoding="utf-8")
    return bodies


def rewrite_sources_with_inline_bodies():
    """Rewrite generate_curriculum.py and curriculum_data.py with expanded concepts/body in M()/add()."""
    early = load("generate_curriculum_raw", SCRIPTS / "generate_curriculum.py")
    # If expansions already applied, MODULES already expanded — reload fresh by stripping marker first
    path_g = SCRIPTS / "generate_curriculum.py"
    raw_g = path_g.read_text(encoding="utf-8")
    marker = "\n# --- EXPANDED_BODIES_APPLIED ---\n"
    if marker in raw_g:
        raw_g = raw_g.split(marker)[0].rstrip() + "\n"
        path_g.write_text(raw_g, encoding="utf-8")
        early = load("generate_curriculum_fresh", path_g)

    later = load("curriculum_data_fresh", SCRIPTS / "curriculum_data.py")
    path_c = SCRIPTS / "curriculum_data.py"
    raw_c = path_c.read_text(encoding="utf-8")
    if marker in raw_c:
        raw_c = raw_c.split(marker)[0].rstrip() + "\n"
        path_c.write_text(raw_c, encoding="utf-8")
        later = load("curriculum_data_fresh2", path_c)

    # Build expanded content
    early_exp = []
    for m in early.MODULES:
        n = m["n"]
        concepts = body_for(n, m)
        assert 3000 <= len(concepts) <= 8000, (n, len(concepts))
        early_exp.append((m, concepts, guide_for(n, m), examples_for(n, m), E[n].get("readme", "")))

    later_exp = []
    for m in later.LATER:
        n = m["n"]
        body = body_for(n, m)
        assert 3000 <= len(body) <= 8000, (n, len(body))
        later_exp.append((m, body, guide_for(n, m), examples_for(n, m)))

    # Patch generate_curriculum: replace concepts positional strings using a line-based state machine
    # Strategy: for each M( block, find the concepts """ ... """ and replace; also inject kwargs before closing ).
    g = path_g.read_text(encoding="utf-8")
    for m, concepts, guide, examples, readme in early_exp:
        # Replace readme in ex dict
        if readme:
            # replace "readme": "..." within this module's section by unique func proximity is hard;
            # we'll set via trailing assignment after MODULES built.
            pass

    # Append clean apply block that sets concepts on MODULES (field via post-M assignment —
    # also overwrite the concepts in memory). Additionally do string replace of old concepts with new.
    apply = [marker, "# Expanded teaching bodies applied to MODULES (concepts / guides / examples)."]
    apply.append("def _apply_expansions():")
    apply.append("    expansions = {")
    for m, concepts, guide, examples, readme in early_exp:
        apply.append(f"        {m['n']}: dict(")
        apply.append(f"            concepts={py_string(concepts)},")
        apply.append(f"            exercise_guide={py_string(guide)},")
        apply.append(f"            exercise_examples={py_string(examples)},")
        apply.append(f"            readme={py_string(readme)},")
        apply.append("        ),")
    apply.append("    }")
    apply.append("    for m in MODULES:")
    apply.append("        e = expansions[m['n']]")
    apply.append("        m['concepts'] = e['concepts']")
    apply.append("        m['exercise_guide'] = e['exercise_guide']")
    apply.append("        m['exercise_examples'] = e['exercise_examples']")
    apply.append("        if isinstance(m.get('ex'), dict) and e['readme']:")
    apply.append("            m['ex']['readme'] = e['readme']")
    apply.append("_apply_expansions()")
    g = g.rstrip() + "\n" + "\n".join(apply) + "\n"
    path_g.write_text(g, encoding="utf-8")

    # curriculum_data.py
    c = path_c.read_text(encoding="utf-8")
    if marker in c:
        c = c.split(marker)[0].rstrip() + "\n"
    apply = [marker, "# Expanded teaching bodies applied to LATER (body / guides / examples)."]
    apply.append("def _apply_expansions():")
    apply.append("    expansions = {")
    for m, body, guide, examples in later_exp:
        apply.append(f"        {m['n']}: dict(")
        apply.append(f"            body={py_string(body)},")
        apply.append(f"            exercise_guide={py_string(guide)},")
        apply.append(f"            exercise_examples={py_string(examples)},")
        apply.append("        ),")
    apply.append("    }")
    apply.append("    for m in LATER:")
    apply.append("        e = expansions[m['n']]")
    apply.append("        m['body'] = e['body']")
    apply.append("        m['exercise_guide'] = e['exercise_guide']")
    apply.append("        m['exercise_examples'] = e['exercise_examples']")
    apply.append("_apply_expansions()")
    c = c.rstrip() + "\n" + "\n".join(apply) + "\n"
    path_c.write_text(c, encoding="utf-8")

    # Stats
    lens = [len(x[1]) for x in early_exp] + [len(x[1]) for x in later_exp]
    print(f"Expanded {len(lens)} lessons: body chars min={min(lens)} max={max(lens)} avg={sum(lens)//len(lens)}")


def main():
    missing = [i for i in range(56) if i not in E]
    if missing:
        raise SystemExit(f"missing extras for lessons: {missing}")
    rewrite_sources_with_inline_bodies()
    # verify load
    early = load("g2", SCRIPTS / "generate_curriculum.py")
    later = load("c2", SCRIPTS / "curriculum_data.py")
    for m in early.MODULES:
        assert len(m["concepts"]) >= 3000, (m["n"], len(m["concepts"]))
        assert m["exercise_guide"]
        assert m["exercise_examples"]
    for m in later.LATER:
        assert len(m["body"]) >= 3000, (m["n"], len(m["body"]))
        assert m["exercise_guide"]
    print("Verification OK:", len(early.MODULES), "+", len(later.LATER))


if __name__ == "__main__":
    main()

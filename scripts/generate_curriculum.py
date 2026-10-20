#!/usr/bin/env python3
"""Generate Go Goodway curriculum: lessons, exercises, solutions, progress tracker."""
from __future__ import annotations

import os
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# (number, slug, title, phase, days_estimate, objectives, concepts, python_pitfalls, self_check, further, exercise_spec)
# exercise_spec: dict with package, funcs (name -> signature description), challenge

MODULES: list[dict] = []


def M(n, slug, title, phase, days, objectives, concepts, pitfalls, checks, reading, ex):
    MODULES.append(
        {
            "n": n,
            "slug": f"{n:02d}-{slug}",
            "title": title,
            "phase": phase,
            "days": days,
            "objectives": objectives,
            "concepts": concepts,
            "pitfalls": pitfalls,
            "checks": checks,
            "reading": reading,
            "ex": ex,
        }
    )


# --- Phase 0 ---
M(
    0,
    "orientation",
    "Orientation: Programs, Computers, and Go",
    "Phase 0 — Orientation",
    "1 day",
    [
        "Explain what a program is and how source code becomes running software",
        "Describe CPU, memory, and the OS at a beginner level",
        "Contrast Go with Python (compiled, static types, concurrency model)",
        "Install the Go toolchain and run your first program",
        "Adopt the study method: attempt → struggle → solution → rewrite from memory",
    ],
    """
## What is a program?

A **program** is a precise sequence of instructions a computer can execute.
You write **source code** (human-readable text). A **compiler** or **interpreter**
turns that into machine instructions the CPU understands.

- **CPU**: executes instructions one at a time (very fast).
- **Memory (RAM)**: temporary storage for values your program uses while running.
- **Disk**: durable storage (files, databases).
- **OS**: manages processes, files, networking; your Go program runs as a process.

## Compiled vs interpreted (Go vs Python)

| | Python | Go |
|---|--------|-----|
| How it runs | Interpreter / VM | Compiled to native machine code |
| Types | Dynamic (checked at runtime) | Static (checked at compile time) |
| Speed | Often slower for CPU work | Typically fast |
| Concurrency | GIL limits CPU threads | Goroutines + scheduler |

Go catches many mistakes **before** your program runs. That feels stricter than Python
at first — and that strictness is a feature for infrastructure work.

## The Go toolchain

After installing Go (https://go.dev/dl/):

```bash
go version          # confirm install
go env GOPATH GOROOT
mkdir -p hello && cd hello
go mod init example.com/hello
```

Create `main.go`:

```go
package main

import "fmt"

func main() {
    fmt.Println("Hello, Goodway")
}
```

```bash
go run .            # compile + run
go build -o hello   # produce a binary
./hello
go test ./...       # run tests (later lessons)
```

## How to study this course

1. Read the lesson PDF carefully; type examples yourself (do not copy-paste blindly).
2. Attempt every exercise **without** opening `solutions/`.
3. If stuck >20 minutes, re-read the concept section, then try a smaller version.
4. Only then compare with the solution — write notes on *why* it works.
5. Next day: rewrite the solution from memory without looking.

Track progress in `curriculum/PROGRESS.md`.
""",
    [
        "Expecting Go to feel like Python (dynamic typing, exceptions everywhere)",
        "Skipping the rewrite-from-memory step — that is where mastery forms",
        "Installing multiple Go versions without understanding modules",
    ],
    [
        "What does the Go compiler do that a Python interpreter does differently?",
        "Name three commands you will use daily (`go run`, `go test`, …).",
        "Why does this course ban looking at solutions first?",
    ],
    ["https://go.dev/doc/install", "https://go.dev/tour/"],
    {
        "skip": False,
        "pkg": "orientation",
        "funcs": [("Greet", "func Greet(name string) string")],
        "starter": 'package orientation\n\n// Greet returns a greeting for name.\nfunc Greet(name string) string {\n\t// TODO: return "Hello, <name>"\n\treturn ""\n}\n',
        "test": '''package orientation

import "testing"

func TestGreet(t *testing.T) {
	got := Greet("Ada")
	want := "Hello, Ada"
	if got != want {
		t.Fatalf("Greet(\\"Ada\\") = %q, want %q", got, want)
	}
}
''',
        "solution": 'package orientation\n\nfunc Greet(name string) string {\n\treturn "Hello, " + name\n}\n',
        "readme": "Implement `Greet` so tests pass: `go test`.\n",
    },
)

# --- Phase 1 ---
M(
    1,
    "values-variables-types",
    "Values, Variables, Types, and Zero Values",
    "Phase 1 — CS fundamentals through Go",
    "1 day",
    [
        "Declare variables with var and short declaration",
        "List basic types and their zero values",
        "Explain why every variable always has a defined value in Go",
        "Choose between typed and untyped constants",
    ],
    """
## Values and types

Every value in Go has a **type**. Types answer: what operations are allowed?
What size does it occupy? What is its zero value?

Common types:
- Integers: `int`, `int64`, `uint`, `byte` (alias for `uint8`)
- Floats: `float64` (prefer over `float32` unless you have a reason)
- Boolean: `bool` (`true` / `false`)
- String: `string` (immutable sequence of bytes, usually UTF-8)

```go
var age int = 30
var name string = "Ada"
ready := true          // short declaration; type inferred
const MaxRetries = 3   // untyped constant unless given a type
```

## Zero values

If you declare a variable without assigning, Go sets the **zero value**:
- numbers → `0`
- bool → `false`
- string → `""`
- pointers/slices/maps/channels/functions/interfaces → `nil`

This removes a whole class of “undefined variable” bugs common in other languages.

```go
var n int
fmt.Println(n) // 0, always safe to read
```

## Memory intuition

A variable name is a label for a location in memory holding a value of a known type.
`int` on a 64-bit machine is typically 8 bytes. You do not manage that manually —
but knowing sizes helps later with slices, structs, and performance.
""",
    [
        "Using `None`-like thinking: Go has `nil` only for reference types, not for ints/strings",
        "Shadowing variables with `:=` inside inner blocks accidentally",
        "Assuming uninitialized variables are dangerous — in Go they are zeroed",
    ],
    [
        "What is the zero value of `string`? Of `*int`?",
        "When must you use `var` instead of `:=`?",
        "Why are zero values useful in APIs?",
    ],
    ["https://go.dev/ref/spec#The_zero_value", "https://go.dev/tour/basics"],
    {
        "pkg": "basics",
        "funcs": [("ZeroInt", "func ZeroInt() int"), ("Describe", "func Describe(n int, label string) string")],
        "starter": '''package basics

// ZeroInt returns the zero value of int without writing a literal 0 in an assignment
// after declaration — declare a bare var and return it.
func ZeroInt() int {
	// TODO
	return -1
}

// Describe returns: "<label>=<n>" e.g. Describe(3, "count") => "count=3"
func Describe(n int, label string) string {
	// TODO
	return ""
}
''',
        "test": '''package basics

import "testing"

func TestZeroInt(t *testing.T) {
	if ZeroInt() != 0 {
		t.Fatalf("want 0")
	}
}

func TestDescribe(t *testing.T) {
	if Describe(3, "count") != "count=3" {
		t.Fatalf("got %q", Describe(3, "count"))
	}
}
''',
        "solution": '''package basics

import "fmt"

func ZeroInt() int {
	var n int
	return n
}

func Describe(n int, label string) string {
	return fmt.Sprintf("%s=%d", label, n)
}
''',
        "readme": "Complete ZeroInt and Describe. Run `go test`.\n",
    },
)

M(
    2,
    "expressions-operators",
    "Expressions, Operators, and Type Conversions",
    "Phase 1 — CS fundamentals through Go",
    "1 day",
    [
        "Use arithmetic, comparison, and logical operators correctly",
        "Explain why Go forbids implicit numeric conversions",
        "Convert between types safely and consciously",
        "Avoid integer division surprises",
    ],
    """
## Operators

Arithmetic: `+ - * / %`
Comparison: `== != < <= > >=`
Logical: `&& || !`
Bitwise: `& | ^ << >>` (useful in systems code)

```go
a, b := 7, 2
fmt.Println(a / b)   // 3  — integer division truncates
fmt.Println(float64(a) / float64(b)) // 3.5
```

## Explicit conversions only

Unlike Python (or C in some cases), Go never silently converts `int` to `float64`:

```go
var i int = 3
var f float64 = float64(i) // required
```

This is deliberate: silent conversions hide bugs in money, indices, and APIs.

## Precedence and clarity

When in doubt, use parentheses. Clarity beats cleverness:

```go
ok := (score >= 50 && attempts < 3) || admin
```
""",
    [
        "Integer division truncating when you expected a float (Python 3 does float `/`)",
        "Trying `int + float64` without conversion",
        "Using `=` vs `==` confusion (assignment vs comparison)",
    ],
    [
        "What does `7/2` evaluate to in Go?",
        "Why must you write `float64(x)`?",
        "Give an example where implicit conversion would be dangerous",
    ],
    ["https://go.dev/ref/spec#Operators", "https://go.dev/ref/spec#Conversions"],
    {
        "pkg": "ops",
        "funcs": [("SafeDiv", "func SafeDiv(a, b int) (float64, bool)"), ("Clamp", "func Clamp(v, lo, hi int) int")],
        "starter": '''package ops

// SafeDiv returns a/b as float64. If b==0, returns (0, false).
func SafeDiv(a, b int) (float64, bool) {
	// TODO
	return 0, false
}

// Clamp returns v restricted to [lo, hi].
func Clamp(v, lo, hi int) int {
	// TODO
	return v
}
''',
        "test": '''package ops

import "testing"

func TestSafeDiv(t *testing.T) {
	v, ok := SafeDiv(7, 2)
	if !ok || v != 3.5 {
		t.Fatalf("got %v %v", v, ok)
	}
	_, ok = SafeDiv(1, 0)
	if ok {
		t.Fatal("expected false")
	}
}

func TestClamp(t *testing.T) {
	if Clamp(5, 0, 10) != 5 || Clamp(-1, 0, 10) != 0 || Clamp(99, 0, 10) != 10 {
		t.Fatal("clamp failed")
	}
}
''',
        "solution": '''package ops

func SafeDiv(a, b int) (float64, bool) {
	if b == 0 {
		return 0, false
	}
	return float64(a) / float64(b), true
}

func Clamp(v, lo, hi int) int {
	if v < lo {
		return lo
	}
	if v > hi {
		return hi
	}
	return v
}
''',
        "readme": "Implement SafeDiv and Clamp.\n",
    },
)

M(
    3,
    "control-flow",
    "Control Flow: if, for, and switch",
    "Phase 1 — CS fundamentals through Go",
    "1 day",
    [
        "Write idiomatic if statements with optional init",
        "Use Go's single loop construct (`for`) in all forms",
        "Use switch without accidental fallthrough",
        "Prefer clear control flow over clever nesting",
    ],
    """
## if

```go
if n := len(items); n == 0 {
    return ErrEmpty
} else if n > 100 {
    return ErrTooMany
}
// n is not in scope here
```

No parentheses around conditions. Braces are required.

## for — the only loop

```go
for i := 0; i < 10; i++ { }
for cond { }           // like while
for { }                // infinite; break/return to leave
for i, v := range xs { }
```

## switch

```go
switch day {
case 1, 2, 3:
    // weekday start
case 6, 7:
    // weekend
default:
}
// cases do NOT fall through unless you write fallthrough
```

Switch on true is a clean if-else chain:

```go
switch {
case score >= 90:
    grade = "A"
case score >= 80:
    grade = "B"
default:
    grade = "C"
}
```
""",
    [
        "Expecting C-style fallthrough in switch",
        "Writing `while` — it does not exist; use `for cond`",
        "Forgetting braces (required even for one-liners)",
    ],
    [
        "Rewrite a while-loop as Go `for`",
        "When is switch-on-true preferable to if/else?",
        "What is the scope of a variable declared in `if init`?",
    ],
    ["https://go.dev/tour/flowcontrol"],
    {
        "pkg": "flow",
        "funcs": [("FizzBuzz", "func FizzBuzz(n int) []string"), ("Classify", "func Classify(n int) string")],
        "starter": '''package flow

// FizzBuzz returns a slice of length n where index i (1-based value i+1) follows
// classic FizzBuzz rules for values 1..n.
func FizzBuzz(n int) []string {
	// TODO
	return nil
}

// Classify returns "neg", "zero", or "pos".
func Classify(n int) string {
	// TODO
	return ""
}
''',
        "test": '''package flow

import (
	"reflect"
	"testing"
)

func TestFizzBuzz(t *testing.T) {
	got := FizzBuzz(5)
	want := []string{"1", "2", "Fizz", "4", "Buzz"}
	if !reflect.DeepEqual(got, want) {
		t.Fatalf("got %v want %v", got, want)
	}
}

func TestClassify(t *testing.T) {
	if Classify(-1) != "neg" || Classify(0) != "zero" || Classify(2) != "pos" {
		t.Fatal("classify")
	}
}
''',
        "solution": '''package flow

import "strconv"

func FizzBuzz(n int) []string {
	out := make([]string, 0, n)
	for i := 1; i <= n; i++ {
		switch {
		case i%15 == 0:
			out = append(out, "FizzBuzz")
		case i%3 == 0:
			out = append(out, "Fizz")
		case i%5 == 0:
			out = append(out, "Buzz")
		default:
			out = append(out, strconv.Itoa(i))
		}
	}
	return out
}

func Classify(n int) string {
	switch {
	case n < 0:
		return "neg"
	case n == 0:
		return "zero"
	default:
		return "pos"
	}
}
''',
        "readme": "Implement FizzBuzz and Classify.\n",
    },
)

M(
    4,
    "functions-errors",
    "Functions, Multiple Returns, and Error Basics",
    "Phase 1 — CS fundamentals through Go",
    "1 day",
    [
        "Define functions with parameters and multiple return values",
        "Use the error interface as Go's primary failure signal",
        "Name return values when it improves clarity",
        "Avoid panic for ordinary errors",
    ],
    """
## Functions

```go
func Add(a, b int) int {
    return a + b
}

func Div(a, b int) (int, error) {
    if b == 0 {
        return 0, errors.New("division by zero")
    }
    return a / b, nil
}
```

Idiom: last return value is often `error`. Callers check immediately:

```go
v, err := Div(x, y)
if err != nil {
    return err
}
```

## Why not exceptions?

Go's explicit errors make control flow visible. You see every failure path.
`panic` exists for truly unrecoverable programmer mistakes — not for "file not found".

## Named returns

```go
func Split(sum int) (x, y int) {
    x = sum * 4 / 9
    y = sum - x
    return
}
```

Use sparingly; great for docs, easy to misuse with shadowing.
""",
    [
        "Ignoring `err` with `_` habitually",
        "Using panic like Python raise for normal failures",
        "Returning error strings inconsistently (prefer `fmt.Errorf` / `errors.New`)",
    ],
    [
        "Why is `(T, error)` preferred over exceptions here?",
        "What should you do immediately after calling a function that returns error?",
        "When is panic appropriate?",
    ],
    ["https://go.dev/blog/error-handling-and-go", "https://go.dev/tour/basics"],
    {
        "pkg": "fn",
        "funcs": [("ParsePositive", "func ParsePositive(s string) (int, error)")],
        "starter": '''package fn

import "strconv"

// ParsePositive parses s as int; returns error if not an int or if <= 0.
func ParsePositive(s string) (int, error) {
	// TODO: use strconv.Atoi
	_ = strconv.Atoi
	return 0, nil
}
''',
        "test": '''package fn

import "testing"

func TestParsePositive(t *testing.T) {
	v, err := ParsePositive("5")
	if err != nil || v != 5 {
		t.Fatalf("%v %v", v, err)
	}
	if _, err := ParsePositive("0"); err == nil {
		t.Fatal("want error for 0")
	}
	if _, err := ParsePositive("x"); err == nil {
		t.Fatal("want error for x")
	}
}
''',
        "solution": '''package fn

import (
	"fmt"
	"strconv"
)

func ParsePositive(s string) (int, error) {
	n, err := strconv.Atoi(s)
	if err != nil {
		return 0, err
	}
	if n <= 0 {
		return 0, fmt.Errorf("need positive, got %d", n)
	}
	return n, nil
}
''',
        "readme": "Implement ParsePositive.\n",
    },
)

M(
    5,
    "arrays-slices-maps",
    "Arrays, Slices, and Maps (Memory Intuition)",
    "Phase 1 — CS fundamentals through Go",
    "1–2 days",
    [
        "Distinguish arrays (fixed) from slices (dynamic views)",
        "Explain slice header: pointer, length, capacity",
        "Grow slices with append and understand reallocation",
        "Use maps safely (including comma-ok idiom)",
    ],
    """
## Arrays

```go
var a [3]int // [0,0,0]; length is part of the type
```

Rarely used directly in APIs; slices dominate.

## Slices — the workhorse

A slice is a **descriptor**: `(pointer to array, length, capacity)`.

```go
s := []int{1, 2, 3}
s = append(s, 4)
t := s[1:3] // shares backing array — mutations can alias
```

When `append` exceeds capacity, Go allocates a new array and copies.
That is why sometimes modifying a sub-slice surprises you.

## Maps

```go
m := map[string]int{"a": 1}
v, ok := m["b"] // ok == false, v == 0
delete(m, "a")
```

Maps are reference types; passing a map to a function lets the callee mutate entries.
Never assume iteration order is stable across runs (since Go 1 it is randomized).
""",
    [
        "Thinking slices always copy (they often share memory)",
        "Reading map missing key without comma-ok and treating 0 as real data",
        "Appending in a loop without pre-sizing when size is known (`make([]T, 0, n)`)",
    ],
    [
        "What are the three fields of a slice header?",
        "Why can `append` invalidate assumptions about shared backing arrays?",
        "How do you distinguish missing key from zero value?",
    ],
    ["https://go.dev/blog/slices-intro", "https://go.dev/blog/maps"],
    {
        "pkg": "collections",
        "funcs": [
            ("Sum", "func Sum(xs []int) int"),
            ("Freq", "func Freq(words []string) map[string]int"),
            ("Unique", "func Unique(xs []int) []int"),
        ],
        "starter": '''package collections

func Sum(xs []int) int {
	// TODO
	return 0
}

func Freq(words []string) map[string]int {
	// TODO
	return nil
}

// Unique returns first occurrences preserving order.
func Unique(xs []int) []int {
	// TODO
	return nil
}
''',
        "test": '''package collections

import (
	"reflect"
	"testing"
)

func TestSum(t *testing.T) {
	if Sum([]int{1, 2, 3}) != 6 {
		t.Fatal()
	}
}

func TestFreq(t *testing.T) {
	m := Freq([]string{"a", "b", "a"})
	if m["a"] != 2 || m["b"] != 1 {
		t.Fatalf("%v", m)
	}
}

func TestUnique(t *testing.T) {
	got := Unique([]int{1, 2, 1, 3, 2})
	want := []int{1, 2, 3}
	if !reflect.DeepEqual(got, want) {
		t.Fatalf("%v", got)
	}
}
''',
        "solution": '''package collections

func Sum(xs []int) int {
	s := 0
	for _, v := range xs {
		s += v
	}
	return s
}

func Freq(words []string) map[string]int {
	m := make(map[string]int)
	for _, w := range words {
		m[w]++
	}
	return m
}

func Unique(xs []int) []int {
	seen := make(map[int]bool)
	out := make([]int, 0, len(xs))
	for _, v := range xs {
		if seen[v] {
			continue
		}
		seen[v] = true
		out = append(out, v)
	}
	return out
}
''',
        "readme": "Implement Sum, Freq, Unique.\n",
    },
)

M(
    6,
    "strings-runes-bytes",
    "Strings, Runes, Bytes, and UTF-8",
    "Phase 1 — CS fundamentals through Go",
    "1 day",
    [
        "Explain that Go strings are immutable byte sequences (often UTF-8)",
        "Iterate by rune vs by byte correctly",
        "Convert between string, []byte, and []rune consciously",
        "Avoid indexing strings when Unicode matters",
    ],
    """
## Strings are bytes

```go
s := "Go👍"
fmt.Println(len(s)) // byte length, not character count
for i, r := range s {
    // r is rune (code point); i is byte index
    fmt.Println(i, string(r))
}
```

A **rune** is an alias for `int32` representing a Unicode code point.
UTF-8 encodes code points in 1–4 bytes. Indexing `s[i]` gives a **byte**, not a character.

## Conversions

```go
b := []byte("hi")
s := string(b)
rs := []rune("naïve")
```

Conversions copy data. Hot paths sometimes stay in `[]byte` to avoid allocations.

## Building strings

Prefer `strings.Builder` when concatenating in a loop — repeated `+` allocates often.
""",
    [
        "Using `len(s)` as character count for Unicode text",
        "Slicing mid-code-point and creating invalid UTF-8",
        "Comparing strings with locale rules (Go compares bytes)",
    ],
    [
        "Difference between `for i := range s` and `for i, r := range s`?",
        "Why is `string` immutable important for concurrency?",
        "When use `[]byte` instead of `string`?",
    ],
    ["https://go.dev/blog/strings", "https://go.dev/blog/normalization"],
    {
        "pkg": "textx",
        "funcs": [("RuneCount", "func RuneCount(s string) int"), ("ReverseRunes", "func ReverseRunes(s string) string")],
        "starter": '''package textx

func RuneCount(s string) int {
	// TODO: count runes, not bytes
	return 0
}

func ReverseRunes(s string) string {
	// TODO
	return ""
}
''',
        "test": '''package textx

import "testing"

func TestRuneCount(t *testing.T) {
	if RuneCount("Go👍") != 3 {
		t.Fatalf("got %d", RuneCount("Go👍"))
	}
}

func TestReverseRunes(t *testing.T) {
	if ReverseRunes("ab👍") != "👍ba" {
		t.Fatalf("got %q", ReverseRunes("ab👍"))
	}
}
''',
        "solution": '''package textx

func RuneCount(s string) int {
	n := 0
	for range s {
		n++
	}
	return n
}

func ReverseRunes(s string) string {
	r := []rune(s)
	for i, j := 0, len(r)-1; i < j; i, j = i+1, j-1 {
		r[i], r[j] = r[j], r[i]
	}
	return string(r)
}
''',
        "readme": "Implement rune-aware helpers.\n",
    },
)

M(
    7,
    "structs-methods-pointers",
    "Structs, Methods, and Pointers",
    "Phase 1 — CS fundamentals through Go",
    "1–2 days",
    [
        "Define structs and compose them with embedding",
        "Choose value vs pointer receivers deliberately",
        "Explain what a pointer stores (an address)",
        "Avoid nil pointer dereferences",
    ],
    """
## Structs

```go
type User struct {
    Name string
    Age  int
}

u := User{Name: "Ada", Age: 36}
```

## Pointers

A pointer holds a **memory address** of a value.

```go
p := &u       // *User
p.Age = 37    // Go auto-dereferences
```

Use pointers when:
- you need to mutate the caller's struct
- the struct is large and you want to avoid copies
- you need `nil` to mean “absent”

## Methods

```go
func (u User) Greet() string { return "hi " + u.Name }
func (u *User) Birthday() { u.Age++ }
```

Rule of thumb: if any method needs a pointer receiver, be consistent for the type.
Value receivers get a copy — mutations won't stick.
""",
    [
        "Expecting Python-like always-reference objects — Go structs are values by default",
        "Mixing value and pointer receivers inconsistently",
        "Returning pointers to loop variables incorrectly (fixed in modern Go, still understand escapes)",
    ],
    [
        "When should a method use a pointer receiver?",
        "What does `&` and `*` mean?",
        "What happens if you call a method on a nil pointer with a pointer receiver?",
    ],
    ["https://go.dev/tour/moretypes", "https://go.dev/doc/effective_go#pointers_vs_values"],
    {
        "pkg": "structs",
        "funcs": [("NewCounter", "func NewCounter(start int) *Counter"), ("methods Inc/Value", "")],
        "starter": '''package structs

type Counter struct {
	n int
}

func NewCounter(start int) *Counter {
	// TODO
	return nil
}

func (c *Counter) Inc() {
	// TODO
}

func (c *Counter) Value() int {
	// TODO
	return 0
}
''',
        "test": '''package structs

import "testing"

func TestCounter(t *testing.T) {
	c := NewCounter(2)
	c.Inc()
	if c.Value() != 3 {
		t.Fatalf("%d", c.Value())
	}
}
''',
        "solution": '''package structs

type Counter struct {
	n int
}

func NewCounter(start int) *Counter {
	return &Counter{n: start}
}

func (c *Counter) Inc() { c.n++ }

func (c *Counter) Value() int { return c.n }
''',
        "readme": "Implement Counter with pointer methods.\n",
    },
)

M(
    8,
    "packages-modules",
    "Packages, Modules, Visibility, and go.mod",
    "Phase 1 — CS fundamentals through Go",
    "1 day",
    [
        "Create modules with go.mod",
        "Export identifiers with Capital letters",
        "Import packages and avoid import cycles",
        "Organize code into packages with a single purpose",
    ],
    """
## Modules

A **module** is a versioned collection of packages (`go.mod`).

```bash
go mod init github.com/you/project
go get example.com/some/dep@v1.2.3
go mod tidy
```

## Packages

Every Go file starts with `package name`. Directory ≈ package (usually).
`package main` with `func main()` builds an executable.

## Visibility

- `Name` (capital) → exported, visible outside the package
- `name` (lowercase) → package-private

There is no `private` keyword. This simplicity scales surprisingly well.

## Import paths

```go
import (
    "fmt"
    "github.com/you/project/internal/auth"
)
```

`internal/` directories are importable only by the parent tree — enforce encapsulation.
""",
    [
        "Creating many tiny packages too early (start coarser)",
        "Import cycles from poor boundaries",
        "Putting everything in `package main` forever",
    ],
    [
        "How do you export a function?",
        "What does `go mod tidy` do?",
        "Why does `internal/` exist?",
    ],
    ["https://go.dev/doc/modules/gomod-ref", "https://go.dev/doc/code"],
    {
        "pkg": "mathx",
        "funcs": [("Square", "func Square(n int) int")],
        "starter": '''package mathx

// Square is exported; squareHint is not.
func Square(n int) int {
	return squareHint(n)
}

func squareHint(n int) int {
	// TODO: return n*n
	return 0
}
''',
        "test": '''package mathx_test

import (
	"testing"

	"goodway/exercises/08-packages-modules/mathx"
)

func TestSquare(t *testing.T) {
	if mathx.Square(4) != 16 {
		t.Fatal()
	}
}
''',
        "solution": '''package mathx

func Square(n int) int {
	return squareHint(n)
}

func squareHint(n int) int {
	return n * n
}
''',
        "readme": "Implement squareHint; notice external test package can only call Square.\n",
        "module_path": "goodway/exercises/08-packages-modules",
        "subdir": "mathx",
    },
)

# MODULES 00–08 defined above; later modules live in curriculum_data.py

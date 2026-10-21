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


def M(
    n,
    slug,
    title,
    phase,
    days,
    objectives,
    concepts,
    pitfalls,
    checks,
    reading,
    ex,
    exercise_guide="",
    exercise_examples="",
):
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
            "exercise_guide": exercise_guide,
            "exercise_examples": exercise_examples,
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

# --- EXPANDED_BODIES_APPLIED ---

# Expanded teaching bodies applied to MODULES (concepts / guides / examples).
def _apply_expansions():
    expansions = {
        0: dict(
            concepts="""
## Why this matters

Before writing production Go you need a mental model of how source becomes a running process, and how Go's toolchain differs from Python. Orientation prevents weeks of cargo-cult commands.

This lesson is a building block for later modules in the Goodway path. If you only
skim, the exercises will feel like busywork; if you type the examples and narrate
them aloud, the same patterns will reappear in HTTP handlers, concurrency, and AI
service glue.

## Core concepts

- A program is source text turned into CPU instructions; the OS schedules it as a process.
- Go compiles to native binaries; `go run` is compile+link+execute for development.
- Modules (`go.mod`) pin dependency versions; packages group related files.
- The study loop (attempt → struggle → solution → rewrite) builds retrieval, not recognition.
- `GOPATH` is legacy for most work; modules are the default since Go 1.14+.

Hold these in working memory while you code. Each bullet should map to something
you can demonstrate with a three-line program or a failing compile error.

## Worked Go examples

Create a scratch module and type this yourself (do not paste blindly):

```bash
mkdir -p /tmp/gw-orientation: && cd /tmp/gw-orientation:
go mod init example.com/scratch
```

Then create `main.go`:

```go
package main

import "fmt"

func main() {
    fmt.Println("Hello, Goodway")
    fmt.Printf("2+2=%d\\n", 2+2)
}
```

Run it:

```bash
go run .
```

Expected output:

```text
Hello, Goodway
2+2=4
```

If your output differs, diff character-by-character — especially whitespace and
types. Then change one line deliberately and predict the new output before running.

## Mini-lab (`go run` steps)

1. Install Go and run `go version`.
2. `mkdir -p /tmp/hello && cd /tmp/hello && go mod init example.com/hello`
3. Create `main.go` with the example; run `go run .`
4. `go build -o hello && ./hello` and confirm the same output.
5. Run `go env GOROOT GOPATH GO111MODULE` and skim what each means.

Write down one sentence explaining *why* the output matches the code before you move on.
Time-box the lab to 15–25 minutes; struggle is part of encoding the skill.

## Curriculum notes (expanded from the compact draft)

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

## Failure modes to watch while coding

- Expecting Go to feel like Python (dynamic typing, exceptions everywhere)
- Skipping the rewrite-from-memory step — that is where mastery forms
- Installing multiple Go versions without understanding modules

When a test fails, ask which failure mode you hit before changing code at random.

## Idioms vs Python pitfalls

- Python: `python hello.py` runs a script. Go: you usually build a package/module.
- Python catches many type errors at runtime; Go rejects them at compile time.
- There is no REPL-as-primary workflow — use `go test` and small `main` programs.
- Virtualenv ≠ modules: Go modules version *dependencies*, not the language runtime.

When you catch yourself reaching for a Python habit, pause and rewrite the Go way
once on purpose — even if both would "work". The goal is a Go-shaped intuition.

## Going deeper

Keep `curriculum/PROGRESS.md` updated. Tomorrow, recreate hello without looking at today's files.

## Practice checklist

Before the exercise, confirm you can:

1. Explain "Orientation: Programs, Computers, and Go" aloud in under two minutes without notes.
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
Implement `Greet(name string) string` so it returns `Hello, <name>`. This drills package layout, exported funcs, and `go test` as feedback.
""",
            exercise_examples="""
Greet("Ada") → "Hello, Ada". Greet("") → "Hello, ". Run: `cd exercises/00-orientation && go test -v`.
""",
            readme="""
Implement exported `Greet` in `orientation.go`. Return exactly `Hello, ` + name. Run `go test` until green. Do not peek at `solutions/`.
""",
        ),
        1: dict(
            concepts="""
## Why this matters

Every Go value has a type and a zero value. That rule eliminates entire classes of undefined bugs and shapes how you design APIs and structs.

This lesson is a building block for later modules in the Goodway path. If you only
skim, the exercises will feel like busywork; if you type the examples and narrate
them aloud, the same patterns will reappear in HTTP handlers, concurrency, and AI
service glue.

## Core concepts

- `var x T` always initializes x to T's zero value — safe to read immediately.
- Short declaration `:=` infers types inside functions; `var` works at package scope too.
- Constants may be untyped and convert until forced into a concrete type.
- Zeros: numbers 0, bool false, string "", nil for pointers/slices/maps/chans/funcs/interfaces.
- Type is part of the value's identity: `int` and `int64` are different types.

Hold these in working memory while you code. Each bullet should map to something
you can demonstrate with a three-line program or a failing compile error.

## Worked Go examples

Create a scratch module and type this yourself (do not paste blindly):

```bash
mkdir -p /tmp/gw-values, && cd /tmp/gw-values,
go mod init example.com/scratch
```

Then create `main.go`:

```go
package main

import "fmt"

func main() {
    var n int
    var s string
    var p *int
    ready := true
    const Max = 3
    fmt.Printf("n=%d s=%q p=%v ready=%v Max=%d\\n", n, s, p, ready, Max)
}
```

Run it:

```bash
go run .
```

Expected output:

```text
n=0 s="" p=<nil> ready=true Max=3
```

If your output differs, diff character-by-character — especially whitespace and
types. Then change one line deliberately and predict the new output before running.

## Mini-lab (`go run` steps)

1. Declare bare `var` for int, string, bool, *int; print them.
2. Use `:=` for a float64 and print its type with `%T`.
3. Assign untyped `const Max = 3` to both int and float64 variables.
4. Shadow a variable with `:=` in an inner block; print inner vs outer.

Write down one sentence explaining *why* the output matches the code before you move on.
Time-box the lab to 15–25 minutes; struggle is part of encoding the skill.

## Curriculum notes (expanded from the compact draft)

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

## Failure modes to watch while coding

- Using `None`-like thinking: Go has `nil` only for reference types, not for ints/strings
- Shadowing variables with `:=` inside inner blocks accidentally
- Assuming uninitialized variables are dangerous — in Go they are zeroed

When a test fails, ask which failure mode you hit before changing code at random.

## Idioms vs Python pitfalls

- Python uses None widely; Go ints/strings are never nil — only reference types use nil.
- `:=` can shadow outer variables in nested blocks — a frequent footgun.
- Uninitialized locals are safe in Go; Python raises NameError.
- No duck typing at assignment: types must match exactly (or convert explicitly).

When you catch yourself reaching for a Python habit, pause and rewrite the Go way
once on purpose — even if both would "work". The goal is a Go-shaped intuition.

## Going deeper

Zero values let you return empty structs without constructors for simple cases — but document meaning when zero is ambiguous (e.g. time.Time).

## Practice checklist

Before the exercise, confirm you can:

1. Explain "Values, Variables, Types, and Zero Values" aloud in under two minutes without notes.
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
Implement `ZeroInt()` by returning a bare `var` (no literal 0), and `Describe(n, label)` as `label=n`.
""",
            exercise_examples="""
ZeroInt() → 0. Describe(3, "count") → "count=3". `go test` in exercises/01-values-variables-types.
""",
            readme="""
Complete ZeroInt (bare var) and Describe with `fmt.Sprintf("%s=%d", label, n)`. Run `go test`.
""",
        ),
        2: dict(
            concepts="""
## Why this matters

Go forbids implicit numeric conversions so money, indices, and APIs stay honest. Operators and conversions prevent silent truncation bugs.

This lesson is a building block for later modules in the Goodway path. If you only
skim, the exercises will feel like busywork; if you type the examples and narrate
them aloud, the same patterns will reappear in HTTP handlers, concurrency, and AI
service glue.

## Core concepts

- Integer `/` truncates toward zero; convert to float for real division.
- Write `float64(i)` explicitly — no silent promotion between numeric types.
- Logical operators short-circuit; bitwise ops matter in systems/code flags.
- Parentheses beat precedence memorization for readable conditions.
- `%` is remainder for integers; signs follow Go's truncation rules.

Hold these in working memory while you code. Each bullet should map to something
you can demonstrate with a three-line program or a failing compile error.

## Worked Go examples

Create a scratch module and type this yourself (do not paste blindly):

```bash
mkdir -p /tmp/gw-expressions, && cd /tmp/gw-expressions,
go mod init example.com/scratch
```

Then create `main.go`:

```go
package main

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
}
```

Run it:

```bash
go run .
```

Expected output:

```text
3
3.5
3
true
```

If your output differs, diff character-by-character — especially whitespace and
types. Then change one line deliberately and predict the new output before running.

## Mini-lab (`go run` steps)

1. Print `7/2` and `float64(7)/float64(2)`.
2. Try compiling `var f float64 = 3` without conversion; fix it.
3. Implement clamp with only comparisons.
4. Experiment with `^` bitwise XOR on small ints.

Write down one sentence explaining *why* the output matches the code before you move on.
Time-box the lab to 15–25 minutes; struggle is part of encoding the skill.

## Curriculum notes (expanded from the compact draft)

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

## Failure modes to watch while coding

- Integer division truncating when you expected a float (Python 3 does float `/`)
- Trying `int + float64` without conversion
- Using `=` vs `==` confusion (assignment vs comparison)

When a test fails, ask which failure mode you hit before changing code at random.

## Idioms vs Python pitfalls

- Python 3 `/` is true division; Go `/` on ints truncates like Python `//`.
- Python may coerce int/float in expressions; Go never does.
- No truthiness of ints: `if n` does not compile — compare explicitly.
- `=` assigns, `==` compares — same symbols, stricter typing around them.

When you catch yourself reaching for a Python habit, pause and rewrite the Go way
once on purpose — even if both would "work". The goal is a Go-shaped intuition.

## Going deeper

When mixing `int` and `int64` from APIs (JSON, DB), convert at the boundary once and stay consistent inside the function.

## Practice checklist

Before the exercise, confirm you can:

1. Explain "Expressions, Operators, and Type Conversions" aloud in under two minutes without notes.
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
Implement SafeDiv(a,b)→(float64,bool) false on /0, and Clamp(v,lo,hi).
""",
            exercise_examples="""
SafeDiv(7,2)→(3.5,true); SafeDiv(1,0)→(0,false). Clamp(99,0,10)→10.
""",
            readme="""
Implement SafeDiv and Clamp in ops.go. Use explicit float64 conversions. `go test`.
""",
        ),
        3: dict(
            concepts="""
## Why this matters

Go has one loop (`for`) and no accidental switch fallthrough. Clear control flow keeps infrastructure code debuggable under pressure.

This lesson is a building block for later modules in the Goodway path. If you only
skim, the exercises will feel like busywork; if you type the examples and narrate
them aloud, the same patterns will reappear in HTTP handlers, concurrency, and AI
service glue.

## Core concepts

- `if` may include an init statement scoped to the if/else chain.
- `for` covers while, infinite, and C-style loops; `range` iterates collections.
- `switch` cases break by default; `fallthrough` is explicit and rare.
- Switch on true replaces long if/else chains cleanly.
- Braces are required even for one-line bodies.

Hold these in working memory while you code. Each bullet should map to something
you can demonstrate with a three-line program or a failing compile error.

## Worked Go examples

Create a scratch module and type this yourself (do not paste blindly):

```bash
mkdir -p /tmp/gw-control && cd /tmp/gw-control
go mod init example.com/scratch
```

Then create `main.go`:

```go
package main

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
Fizz
4
Buzz
```

If your output differs, diff character-by-character — especially whitespace and
types. Then change one line deliberately and predict the new output before running.

## Mini-lab (`go run` steps)

1. Rewrite a Python `while` as `for cond { }`.
2. Use `if n := len(xs); n == 0` and note that n is out of scope after.
3. Implement Classify with switch-on-true.
4. Write an infinite `for { }` with `break` after three iterations.

Write down one sentence explaining *why* the output matches the code before you move on.
Time-box the lab to 15–25 minutes; struggle is part of encoding the skill.

## Curriculum notes (expanded from the compact draft)

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

## Failure modes to watch while coding

- Expecting C-style fallthrough in switch
- Writing `while` — it does not exist; use `for cond`
- Forgetting braces (required even for one-liners)

When a test fails, ask which failure mode you hit before changing code at random.

## Idioms vs Python pitfalls

- No `while` keyword — use `for cond`.
- Switch does not fall through like C; closer to Python 3.10 `match` without fallthrough.
- No ternary `a if c else b` — use if/else or a small function.
- `range` on a slice yields index, value — not just values unless you use `_`.

When you catch yourself reaching for a Python habit, pause and rewrite the Go way
once on purpose — even if both would "work". The goal is a Go-shaped intuition.

## Going deeper

Prefer early `return` / `continue` over deep nesting. Flat control flow is an idiomatic Go readability feature.

## Practice checklist

Before the exercise, confirm you can:

1. Explain "Control Flow: if, for, and switch" aloud in under two minutes without notes.
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
Implement FizzBuzz(n) for values 1..n and Classify(n)→neg|zero|pos.
""",
            exercise_examples="""
FizzBuzz(5)→["1","2","Fizz","4","Buzz"]. Classify(-1)→"neg".
""",
            readme="""
Implement FizzBuzz and Classify using for/switch. `go test`.
""",
        ),
        4: dict(
            concepts="""
## Why this matters

Multiple returns and explicit `error` values make failure paths visible. This is the heartbeat of reliable Go services — no hidden exceptions.

This lesson is a building block for later modules in the Goodway path. If you only
skim, the exercises will feel like busywork; if you type the examples and narrate
them aloud, the same patterns will reappear in HTTP handlers, concurrency, and AI
service glue.

## Core concepts

- `(T, error)` is the dominant result pattern; check `err != nil` immediately.
- Errors are values implementing `Error() string` — often created with `errors.New` / `fmt.Errorf`.
- `panic` is for programming bugs, not expected failures like bad user input.
- Named results document intent; avoid them when they encourage shadowing.
- Never ignore errors with `_` unless you can justify it in a comment.

Hold these in working memory while you code. Each bullet should map to something
you can demonstrate with a three-line program or a failing compile error.

## Worked Go examples

Create a scratch module and type this yourself (do not paste blindly):

```bash
mkdir -p /tmp/gw-functions, && cd /tmp/gw-functions,
go mod init example.com/scratch
```

Then create `main.go`:

```go
package main

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
}
```

Run it:

```bash
go run .
```

Expected output:

```text
5 <nil>
division by zero
```

If your output differs, diff character-by-character — especially whitespace and
types. Then change one line deliberately and predict the new output before running.

## Mini-lab (`go run` steps)

1. Write Div; call with success and failure.
2. Parse with strconv.Atoi and handle the error.
3. Return fmt.Errorf("parse %q: %w", s, err) once you know %w (preview).
4. Add a unit test style check in main: fail loudly if err is wrong.

Write down one sentence explaining *why* the output matches the code before you move on.
Time-box the lab to 15–25 minutes; struggle is part of encoding the skill.

## Curriculum notes (expanded from the compact draft)

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

## Failure modes to watch while coding

- Ignoring `err` with `_` habitually
- Using panic like Python raise for normal failures
- Returning error strings inconsistently (prefer `fmt.Errorf` / `errors.New`)

When a test fails, ask which failure mode you hit before changing code at random.

## Idioms vs Python pitfalls

- Python raises; Go returns error values you must handle.
- Do not use panic/recover like try/except for ordinary control flow.
- Ignoring err is like `except Exception: pass` — worse in production.
- No finally — use `defer` for cleanup (later lessons deepen this).

When you catch yourself reaching for a Python habit, pause and rewrite the Go way
once on purpose — even if both would "work". The goal is a Go-shaped intuition.

## Going deeper

Error messages should help operators: include the input or resource name, not only "failed".

## Practice checklist

Before the exercise, confirm you can:

1. Explain "Functions, Multiple Returns, and Error Basics" aloud in under two minutes without notes.
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
Implement ParsePositive(s): Atoi, then reject n<=0 with a clear error.
""",
            exercise_examples="""
ParsePositive("5")→(5,nil). "0" and "x" both return errors.
""",
            readme="""
Implement ParsePositive with strconv.Atoi and fmt.Errorf for non-positive. `go test`.
""",
        ),
        5: dict(
            concepts="""
## Why this matters

Slices and maps are how Go holds collections. The slice header (ptr, len, cap) prevents aliasing bugs and needless allocations when you understand it.

This lesson is a building block for later modules in the Goodway path. If you only
skim, the exercises will feel like busywork; if you type the examples and narrate
them aloud, the same patterns will reappear in HTTP handlers, concurrency, and AI
service glue.

## Core concepts

- Arrays have fixed length in the type; slices are descriptors over arrays.
- `append` may reallocate; sub-slices often share a backing array.
- Maps need `make` or a literal; reading a missing key yields the zero value.
- Comma-ok: `v, ok := m[k]` distinguishes missing from zero.
- `make([]T, n, c)` sets length n and capacity c — pre-size when you know n.

Hold these in working memory while you code. Each bullet should map to something
you can demonstrate with a three-line program or a failing compile error.

## Worked Go examples

Create a scratch module and type this yourself (do not paste blindly):

```bash
mkdir -p /tmp/gw-arrays, && cd /tmp/gw-arrays,
go mod init example.com/scratch
```

Then create `main.go`:

```go
package main

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
}
```

Run it:

```bash
go run .
```

Expected output:

```text
[1 2 3 4] 4 6 0 false
[1 99 3 4] [99 3]
```

If your output differs, diff character-by-character — especially whitespace and
types. Then change one line deliberately and predict the new output before running.

## Mini-lab (`go run` steps)

1. Slice s[1:3], mutate, print original — observe sharing.
2. Append until capacity grows; print len/cap before and after.
3. Build a frequency map with m[w]++.
4. Use make([]int, 0, 100) and append in a loop; compare allocations mentally.

Write down one sentence explaining *why* the output matches the code before you move on.
Time-box the lab to 15–25 minutes; struggle is part of encoding the skill.

## Curriculum notes (expanded from the compact draft)

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

## Failure modes to watch while coding

- Thinking slices always copy (they often share memory)
- Reading map missing key without comma-ok and treating 0 as real data
- Appending in a loop without pre-sizing when size is known (`make([]T, 0, n)`)

When a test fails, ask which failure mode you hit before changing code at random.

## Idioms vs Python pitfalls

- Python lists own storage; Go sub-slices often share memory.
- dict.get vs comma-ok — use ok when zero is valid data.
- Map iteration order is randomized; never rely on it for tests.
- No list comprehensions — use loops or small helper funcs (clear > clever).

When you catch yourself reaching for a Python habit, pause and rewrite the Go way
once on purpose — even if both would "work". The goal is a Go-shaped intuition.

## Going deeper

When returning a slice from a function, consider whether callers can mutate shared backing storage. Sometimes `append([]T(nil), s...)` copies.

## Practice checklist

Before the exercise, confirm you can:

1. Explain "Arrays, Slices, and Maps (Memory Intuition)" aloud in under two minutes without notes.
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
Implement Sum, Freq (word counts), and Unique (first-seen order).
""",
            exercise_examples="""
Sum([1,2,3])→6. Freq([a,b,a]) a=2. Unique([1,2,1,3,2])→[1,2,3].
""",
            readme="""
Implement Sum, Freq, Unique in collections.go. Preserve Unique order. `go test`.
""",
        ),
        6: dict(
            concepts="""
## Why this matters

Real text is UTF-8. Treating `len(s)` as character count breaks emoji, names, and logs. Runes vs bytes is mandatory for correct processing.

This lesson is a building block for later modules in the Goodway path. If you only
skim, the exercises will feel like busywork; if you type the examples and narrate
them aloud, the same patterns will reappear in HTTP handlers, concurrency, and AI
service glue.

## Core concepts

- string is an immutable byte sequence, usually UTF-8.
- `range` over string yields runes; indexing `s[i]` yields a byte.
- []byte ↔ string conversions copy; hot paths may stay in bytes.
- strings.Builder avoids quadratic `+` concatenation in loops.
- A rune is int32 holding a Unicode code point — not always one user-perceived character.

Hold these in working memory while you code. Each bullet should map to something
you can demonstrate with a three-line program or a failing compile error.

## Worked Go examples

Create a scratch module and type this yourself (do not paste blindly):

```bash
mkdir -p /tmp/gw-strings, && cd /tmp/gw-strings,
go mod init example.com/scratch
```

Then create `main.go`:

```go
package main

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
}
```

Run it:

```bash
go run .
```

Expected output:

```text
bytes 6
'G' 'o' '👍' 
runes 3
```

If your output differs, diff character-by-character — especially whitespace and
types. Then change one line deliberately and predict the new output before running.

## Mini-lab (`go run` steps)

1. Compare len vs rune count for emoji text.
2. Reverse by runes and verify round-trip.
3. Intentionally slice mid-code-point and observe invalid UTF-8.
4. Build a string with strings.Builder in a loop of 1000.

Write down one sentence explaining *why* the output matches the code before you move on.
Time-box the lab to 15–25 minutes; struggle is part of encoding the skill.

## Curriculum notes (expanded from the compact draft)

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

## Failure modes to watch while coding

- Using `len(s)` as character count for Unicode text
- Slicing mid-code-point and creating invalid UTF-8
- Comparing strings with locale rules (Go compares bytes)

When a test fails, ask which failure mode you hit before changing code at random.

## Idioms vs Python pitfalls

- Python 3 str is Unicode code points; Go string is bytes.
- s[i] in Go is a byte; in Python it is a 1-char str.
- len(s) in Python counts chars; len(s) in Go counts bytes.
- Encoding issues appear at I/O — be explicit at boundaries.

When you catch yourself reaching for a Python habit, pause and rewrite the Go way
once on purpose — even if both would "work". The goal is a Go-shaped intuition.

## Going deeper

For grapheme clusters (user-perceived characters) you need extra libraries; runes are the first correct step beyond bytes.

## Practice checklist

Before the exercise, confirm you can:

1. Explain "Strings, Runes, Bytes, and UTF-8" aloud in under two minutes without notes.
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
Implement RuneCount and ReverseRunes that respect Unicode code points.
""",
            exercise_examples="""
RuneCount("Go👍")→3. ReverseRunes("ab👍")→"👍ba".
""",
            readme="""
Count/reverse by runes ([]rune). `go test`.
""",
        ),
        7: dict(
            concepts="""
## Why this matters

Structs are Go's objects-without-classes. Pointer vs value receivers decide mutability and copies — foundational for APIs and concurrency safety.

This lesson is a building block for later modules in the Goodway path. If you only
skim, the exercises will feel like busywork; if you type the examples and narrate
them aloud, the same patterns will reappear in HTTP handlers, concurrency, and AI
service glue.

## Core concepts

- Structs group fields; prefer keyed composite literals.
- Pointers store addresses; `&u` takes address, `*p` dereferences.
- Pointer receivers mutate; value receivers operate on copies.
- If any method needs *T, prefer *T consistently for that type.
- Embedding promotes fields/methods — composition over inheritance.

Hold these in working memory while you code. Each bullet should map to something
you can demonstrate with a three-line program or a failing compile error.

## Worked Go examples

Create a scratch module and type this yourself (do not paste blindly):

```bash
mkdir -p /tmp/gw-structs, && cd /tmp/gw-structs,
go mod init example.com/scratch
```

Then create `main.go`:

```go
package main

import "fmt"

type Counter struct{ n int }

func NewCounter(start int) *Counter { return &Counter{n: start} }
func (c *Counter) Inc()             { c.n++ }
func (c *Counter) Value() int       { return c.n }

func main() {
    c := NewCounter(2)
    c.Inc()
    fmt.Println(c.Value())
}
```

Run it:

```bash
go run .
```

Expected output:

```text
3
```

If your output differs, diff character-by-character — especially whitespace and
types. Then change one line deliberately and predict the new output before running.

## Mini-lab (`go run` steps)

1. Implement Counter; verify Inc mutates.
2. Change Inc to a value receiver and observe the bug.
3. Embed struct B inside A and call a promoted method.
4. Print a nil *Counter method call carefully (expect panic if deref).

Write down one sentence explaining *why* the output matches the code before you move on.
Time-box the lab to 15–25 minutes; struggle is part of encoding the skill.

## Curriculum notes (expanded from the compact draft)

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

## Failure modes to watch while coding

- Expecting Python-like always-reference objects — Go structs are values by default
- Mixing value and pointer receivers inconsistently
- Returning pointers to loop variables incorrectly (fixed in modern Go, still understand escapes)

When a test fails, ask which failure mode you hit before changing code at random.

## Idioms vs Python pitfalls

- Python objects are references; Go structs are values unless you pointer them.
- Receiver name is convention (`c`), not `self`/`this`.
- No inheritance hierarchy — embed and interface instead.
- Copying a struct copies fields; mutable nested pointers still share.

When you catch yourself reaching for a Python habit, pause and rewrite the Go way
once on purpose — even if both would "work". The goal is a Go-shaped intuition.

## Going deeper

Large structs passed by value burn CPU copying; profile before micro-optimizing, but prefer *T for mutex-containing structs always.

## Practice checklist

Before the exercise, confirm you can:

1. Explain "Structs, Methods, and Pointers" aloud in under two minutes without notes.
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
Implement NewCounter, (*Counter).Inc, and Value with pointer receivers.
""",
            exercise_examples="""
NewCounter(2); Inc(); Value()→3.
""",
            readme="""
Pointer-receiver Counter; constructor returns *Counter. `go test`.
""",
        ),
        8: dict(
            concepts="""
## Why this matters

Modules and visibility scale Go across teams. Capitals export; `internal/` enforces boundaries without heavy ceremony.

This lesson is a building block for later modules in the Goodway path. If you only
skim, the exercises will feel like busywork; if you type the examples and narrate
them aloud, the same patterns will reappear in HTTP handlers, concurrency, and AI
service glue.

## Core concepts

- `go mod init` sets the module path; packages map to directories.
- Exported identifiers start with A–Z; lowercase stays package-private.
- External tests (`package foo_test`) only see exported API — great design pressure.
- `go mod tidy` adds required modules and drops unused ones.
- `internal/` directories are importable only by their parent tree.

Hold these in working memory while you code. Each bullet should map to something
you can demonstrate with a three-line program or a failing compile error.

## Worked Go examples

Create a scratch module and type this yourself (do not paste blindly):

```bash
mkdir -p /tmp/gw-packages, && cd /tmp/gw-packages,
go mod init example.com/scratch
```

Then create `main.go`:

```go
package main

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
}
```

Run it:

```bash
go run .
```

Expected output:

```text
16
```

If your output differs, diff character-by-character — especially whitespace and
types. Then change one line deliberately and predict the new output before running.

## Mini-lab (`go run` steps)

1. Create package mathx with Square + unexported helper.
2. Write an external test in package mathx_test.
3. Try calling the unexported helper from outside — read the compiler error.
4. Run `go mod tidy` after adding/removing a dependency import.

Write down one sentence explaining *why* the output matches the code before you move on.
Time-box the lab to 15–25 minutes; struggle is part of encoding the skill.

## Curriculum notes (expanded from the compact draft)

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

## Failure modes to watch while coding

- Creating many tiny packages too early (start coarser)
- Import cycles from poor boundaries
- Putting everything in `package main` forever

When a test fails, ask which failure mode you hit before changing code at random.

## Idioms vs Python pitfalls

- Python `_name` is convention; Go unexported is enforced by the compiler.
- Import paths are module paths, not relative `../` hacks for libraries.
- Avoid eternal package main — split libraries when reuse appears.
- Circular imports fail loudly; redesign packages instead of tricks.

When you catch yourself reaching for a Python habit, pause and rewrite the Go way
once on purpose — even if both would "work". The goal is a Go-shaped intuition.

## Going deeper

Keep packages purposeful: one idea per package. `util` packages become junk drawers — name by domain.

## Practice checklist

Before the exercise, confirm you can:

1. Explain "Packages, Modules, Visibility, and go.mod" aloud in under two minutes without notes.
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
Implement unexported squareHint used by exported Square; tests import from outside.
""",
            exercise_examples="""
mathx.Square(4)→16. External tests cannot call squareHint.
""",
            readme="""
Fill squareHint so Square works. External test can only call Square. `go test ./...`.
""",
        ),
    }
    for m in MODULES:
        e = expansions[m['n']]
        m['concepts'] = e['concepts']
        m['exercise_guide'] = e['exercise_guide']
        m['exercise_examples'] = e['exercise_examples']
        if isinstance(m.get('ex'), dict) and e['readme']:
            m['ex']['readme'] = e['readme']
_apply_expansions()

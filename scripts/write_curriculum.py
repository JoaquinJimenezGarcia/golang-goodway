#!/usr/bin/env python3
"""Write all curriculum files: lessons, exercises, solutions, README, PROGRESS."""
from __future__ import annotations

import importlib.util
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = Path(__file__).resolve().parent


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


early = load("generate_curriculum", SCRIPTS / "generate_curriculum.py")
later = load("curriculum_data", SCRIPTS / "curriculum_data.py")

GO_VERSION = "1.22.0"


def exercise_readme_md(meta: dict, short: str = "") -> str:
    objs = "\n".join(f"- {o}" for o in meta["objectives"])
    guide = (meta.get("exercise_guide") or short or "").strip()
    if not guide:
        guide = (
            f"Implement the stubs in this folder until `go test` (or `./test.sh`) passes. "
            f"Every failing test names a behavior taught in **{meta['title']}**."
        )
    examples = (meta.get("exercise_examples") or "").strip()
    if not examples:
        examples = (
            "Copy patterns from the lesson's worked Go examples. Prefer clear, idiomatic Go "
            "over clever one-liners. Match test expectations exactly (including errors)."
        )
    slug = meta["slug"]
    return f"""# Exercise: {meta['n']:02d}. {meta['title']}

## Goal

Convert reading into **retrievable skill**. The tests are the specification.

## Concepts from the lesson

{objs}

## Task

{guide}

## Examples / expected behavior

{examples}

## How to work

1. Read this README, then re-open `lessons/{slug}/lesson.md`.
2. Run the tests once to get a failure checklist.
3. Implement the smallest correct code; re-run after each function.
4. When stuck, re-type a lesson example into a scratch file and adapt it.
5. After green: explain each exported function in one sentence without looking.

## Done when

- Tests pass
- You can rewrite tomorrow without peeking at today's solution

**Do not open `solutions/{slug}/` until after a real attempt (15+ minutes).**
"""


def lesson_md(meta: dict, body: str) -> str:
    objs = "\n".join(f"- {o}" for o in meta["objectives"])
    pits = "\n".join(f"- {p}" for p in meta["pitfalls"])
    checks = "\n".join(f"{i}. {c}" for i, c in enumerate(meta["checks"], 1))
    reads = "\n".join(f"- {r}" for r in meta["reading"])
    slug = meta["slug"]
    guide = (meta.get("exercise_guide") or "").strip()
    guide_block = f"\n### What you will build\n\n{guide}\n" if guide else ""
    return f"""---
title: "{meta['n']:02d}. {meta['title']}"
---

# {meta['n']:02d}. {meta['title']}

**Phase:** {meta['phase']}  
**Estimated time:** {meta['days']}  
**Slug:** `{slug}`

## Learning objectives

{objs}

## Prerequisites

Complete prior numbered lessons. Type every example yourself — reading Go is not writing Go.

{body.strip()}

## Common mistakes (especially from Python instincts)

{pits}

## Exercises

Work in `exercises/{slug}/`. Read that folder's `README.md` before you code.
{guide_block}
### Study loop

- **A (Drill):** make unit tests pass with the simplest correct code.
- **B (Apply):** extend with an edge case called out in the exercise README.
- **C (Challenge):** rewrite your solution from memory the next day without looking.

**Do not open `solutions/{slug}/` until you have an honest failing attempt.**

## Self-check

Answer without scrolling up:

{checks}

## Further reading

{reads}
"""


# --- Exercise generators by kind -------------------------------------------------

def write_go_module(dirpath: Path, module_path: str, files: dict[str, str]):
    dirpath.mkdir(parents=True, exist_ok=True)
    (dirpath / "go.mod").write_text(f"module {module_path}\n\ngo {GO_VERSION}\n", encoding="utf-8")
    for name, content in files.items():
        p = dirpath / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")


EX_KIND: dict[str, callable] = {}


def ex(kind):
    def deco(fn):
        EX_KIND[kind] = fn
        return fn

    return deco


@ex("interface_shape")
def _interface(slug):
    starter = '''package shape

type Shape interface {
	Area() float64
}

type Rect struct{ W, H float64 }

func (r Rect) Area() float64 {
	// TODO
	return 0
}

// TotalArea sums areas.
func TotalArea(shapes []Shape) float64 {
	// TODO
	return 0
}
'''
    test = '''package shape

import "testing"

func TestTotalArea(t *testing.T) {
	got := TotalArea([]Shape{Rect{2, 3}, Rect{1, 1}})
	if got != 7 {
		t.Fatalf("got %v", got)
	}
}
'''
    sol = '''package shape

type Shape interface {
	Area() float64
}

type Rect struct{ W, H float64 }

func (r Rect) Area() float64 { return r.W * r.H }

func TotalArea(shapes []Shape) float64 {
	var s float64
	for _, sh := range shapes {
		s += sh.Area()
	}
	return s
}
'''
    return "shape", {"shape.go": starter, "shape_test.go": test}, {"shape.go": sol}, "Implement Shape/Rect/TotalArea.\n"


@ex("errors_wrap")
def _errors(slug):
    starter = '''package errx

import "fmt"

var ErrNotFound = fmt.Errorf("not found")

func WrapNotFound(id string) error {
	// TODO: wrap ErrNotFound with id using %w
	return nil
}

func IsNotFound(err error) bool {
	// TODO: errors.Is
	return false
}
'''
    test = '''package errx

import "testing"

func TestWrap(t *testing.T) {
	err := WrapNotFound("x")
	if !IsNotFound(err) {
		t.Fatal("expected NotFound")
	}
}
'''
    sol = '''package errx

import (
	"errors"
	"fmt"
)

var ErrNotFound = errors.New("not found")

func WrapNotFound(id string) error {
	return fmt.Errorf("id %s: %w", id, ErrNotFound)
}

func IsNotFound(err error) bool {
	return errors.Is(err, ErrNotFound)
}
'''
    return "errx", {"errx.go": starter, "errx_test.go": test}, {"errx.go": sol}, "Wrap and detect ErrNotFound.\n"


@ex("generics_map")
def _gen(slug):
    starter = '''package genx

func MapKeys[K comparable, V any](m map[K]V) []K {
	// TODO
	return nil
}

func Filter[T any](xs []T, keep func(T) bool) []T {
	// TODO
	return nil
}
'''
    test = '''package genx

import (
	"reflect"
	"sort"
	"testing"
)

func TestMapKeys(t *testing.T) {
	ks := MapKeys(map[string]int{"b": 2, "a": 1})
	sort.Strings(ks)
	if !reflect.DeepEqual(ks, []string{"a", "b"}) {
		t.Fatalf("%v", ks)
	}
}

func TestFilter(t *testing.T) {
	got := Filter([]int{1, 2, 3, 4}, func(n int) bool { return n%2 == 0 })
	if !reflect.DeepEqual(got, []int{2, 4}) {
		t.Fatalf("%v", got)
	}
}
'''
    sol = '''package genx

func MapKeys[K comparable, V any](m map[K]V) []K {
	out := make([]K, 0, len(m))
	for k := range m {
		out = append(out, k)
	}
	return out
}

func Filter[T any](xs []T, keep func(T) bool) []T {
	out := make([]T, 0, len(xs))
	for _, v := range xs {
		if keep(v) {
			out = append(out, v)
		}
	}
	return out
}
'''
    return "genx", {"genx.go": starter, "genx_test.go": test}, {"genx.go": sol}, "Implement generic MapKeys and Filter.\n"


@ex("testing_table")
def _testing(slug):
    starter = '''package clamp

func Clamp(v, lo, hi int) int {
	// TODO
	return v
}
'''
    test = '''package clamp

import "testing"

func TestClamp(t *testing.T) {
	tests := []struct {
		name             string
		v, lo, hi, want  int
	}{
		{"mid", 5, 0, 10, 5},
		{"low", -1, 0, 10, 0},
		{"high", 99, 0, 10, 10},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			if got := Clamp(tt.v, tt.lo, tt.hi); got != tt.want {
				t.Fatalf("got %d want %d", got, tt.want)
			}
		})
	}
}
'''
    sol = '''package clamp

func Clamp(v, lo, hi int) int {
	if v < lo {
		return lo
	}
	if v > hi {
		return hi
	}
	return v
}
'''
    return "clamp", {"clamp.go": starter, "clamp_test.go": test}, {"clamp.go": sol}, "Make table tests pass.\n"


@ex("io_count")
def _io(slug):
    starter = '''package iox

import "io"

// CountBytes reads r until EOF and returns byte count.
func CountBytes(r io.Reader) (int, error) {
	// TODO
	return 0, nil
}
'''
    test = '''package iox

import (
	"strings"
	"testing"
)

func TestCountBytes(t *testing.T) {
	n, err := CountBytes(strings.NewReader("abcd"))
	if err != nil || n != 4 {
		t.Fatalf("%d %v", n, err)
	}
}
'''
    sol = '''package iox

import "io"

func CountBytes(r io.Reader) (int, error) {
	buf := make([]byte, 512)
	total := 0
	for {
		n, err := r.Read(buf)
		total += n
		if err == io.EOF {
			return total, nil
		}
		if err != nil {
			return total, err
		}
	}
}
'''
    return "iox", {"iox.go": starter, "iox_test.go": test}, {"iox.go": sol}, "Count bytes via io.Reader.\n"


@ex("json_roundtrip")
def _json(slug):
    starter = '''package jx

import "time"

type Event struct {
	ID string    `json:"id"`
	At time.Time `json:"at"`
}

func RoundTrip(e Event) (Event, error) {
	// TODO: marshal then unmarshal
	return Event{}, nil
}
'''
    test = '''package jx

import (
	"testing"
	"time"
)

func TestRoundTrip(t *testing.T) {
	in := Event{ID: "1", At: time.Date(2024, 1, 2, 3, 4, 5, 0, time.UTC)}
	out, err := RoundTrip(in)
	if err != nil {
		t.Fatal(err)
	}
	if out.ID != in.ID || !out.At.Equal(in.At) {
		t.Fatalf("%+v", out)
	}
}
'''
    sol = '''package jx

import (
	"encoding/json"
	"time"
)

type Event struct {
	ID string    `json:"id"`
	At time.Time `json:"at"`
}

func RoundTrip(e Event) (Event, error) {
	b, err := json.Marshal(e)
	if err != nil {
		return Event{}, err
	}
	var out Event
	if err := json.Unmarshal(b, &out); err != nil {
		return Event{}, err
	}
	return out, nil
}
'''
    return "jx", {"jx.go": starter, "jx_test.go": test}, {"jx.go": sol}, "JSON round-trip Event.\n"


@ex("context_timeout")
def _ctx(slug):
    starter = '''package ctxx

import (
	"context"
	"time"
)

// SleepOrTimeout sleeps d unless ctx done first.
// Returns ctx.Err() if cancelled/timed out, else nil.
func SleepOrTimeout(ctx context.Context, d time.Duration) error {
	// TODO
	return nil
}
'''
    test = '''package ctxx

import (
	"context"
	"testing"
	"time"
)

func TestSleepOrTimeout(t *testing.T) {
	ctx, cancel := context.WithTimeout(context.Background(), 20*time.Millisecond)
	defer cancel()
	err := SleepOrTimeout(ctx, time.Second)
	if err == nil {
		t.Fatal("expected timeout error")
	}
}
'''
    sol = '''package ctxx

import (
	"context"
	"time"
)

func SleepOrTimeout(ctx context.Context, d time.Duration) error {
	t := time.NewTimer(d)
	defer t.Stop()
	select {
	case <-ctx.Done():
		return ctx.Err()
	case <-t.C:
		return nil
	}
}
'''
    return "ctxx", {"ctxx.go": starter, "ctxx_test.go": test}, {"ctxx.go": sol}, "Honor context timeout while sleeping.\n"


@ex("reflect_kind")
def _reflect(slug):
    starter = '''package refx

import "reflect"

func KindName(v any) string {
	// TODO return reflect kind string, e.g. "int", "string"
	_ = reflect.TypeOf
	return ""
}
'''
    test = '''package refx

import "testing"

func TestKindName(t *testing.T) {
	if KindName(3) != "int" || KindName("a") != "string" {
		t.Fatalf("%s %s", KindName(3), KindName("a"))
	}
}
'''
    sol = '''package refx

import "reflect"

func KindName(v any) string {
	return reflect.TypeOf(v).Kind().String()
}
'''
    return "refx", {"refx.go": starter, "refx_test.go": test}, {"refx.go": sol}, "Return reflect Kind name.\n"


@ex("idiom_parse")
def _idiom(slug):
    starter = '''package idiom

import "fmt"

// ParsePairs parses "k=v,k2=v2" into a map. Empty string => empty map.
func ParsePairs(s string) (map[string]string, error) {
	// TODO
	_ = fmt.Errorf
	return nil, nil
}
'''
    test = '''package idiom

import "testing"

func TestParsePairs(t *testing.T) {
	m, err := ParsePairs("a=1,b=2")
	if err != nil || m["a"] != "1" || m["b"] != "2" {
		t.Fatalf("%v %v", m, err)
	}
	m, err = ParsePairs("")
	if err != nil || len(m) != 0 {
		t.Fatal("empty")
	}
}
'''
    sol = '''package idiom

import (
	"fmt"
	"strings"
)

func ParsePairs(s string) (map[string]string, error) {
	out := map[string]string{}
	if s == "" {
		return out, nil
	}
	for _, part := range strings.Split(s, ",") {
		k, v, ok := strings.Cut(part, "=")
		if !ok || k == "" {
			return nil, fmt.Errorf("bad pair %q", part)
		}
		out[k] = v
	}
	return out, nil
}
'''
    return "idiom", {"idiom.go": starter, "idiom_test.go": test}, {"idiom.go": sol}, "Parse k=v pairs idiomatically.\n"


@ex("layout_quiz")
def _layout(slug):
    starter = '''package layout

// ClassifyPath returns "cmd", "internal", or "other" for a repo-relative path prefix.
func ClassifyPath(path string) string {
	// TODO: cmd/... => cmd; internal/... => internal; else other
	return ""
}
'''
    test = '''package layout

import "testing"

func TestClassifyPath(t *testing.T) {
	if ClassifyPath("cmd/api/main.go") != "cmd" {
		t.Fatal()
	}
	if ClassifyPath("internal/server/s.go") != "internal" {
		t.Fatal()
	}
	if ClassifyPath("pkg/x/x.go") != "other" {
		t.Fatal()
	}
}
'''
    sol = '''package layout

import "strings"

func ClassifyPath(path string) string {
	switch {
	case strings.HasPrefix(path, "cmd/") || path == "cmd":
		return "cmd"
	case strings.HasPrefix(path, "internal/") || path == "internal":
		return "internal"
	default:
		return "other"
	}
}
'''
    return "layout", {"layout.go": starter, "layout_test.go": test}, {"layout.go": sol}, "Classify repo paths.\n"


@ex("perf_sum")
def _perf(slug):
    starter = '''package perf

func SumPrealloc(xs []int) int {
	// TODO sum — use a simple loop (benchmark later yourself)
	return 0
}
'''
    test = '''package perf

import "testing"

func TestSumPrealloc(t *testing.T) {
	if SumPrealloc([]int{1, 2, 3}) != 6 {
		t.Fatal()
	}
}

func BenchmarkSumPrealloc(b *testing.B) {
	xs := make([]int, 10000)
	for i := 0; i < b.N; i++ {
		SumPrealloc(xs)
	}
}
'''
    sol = '''package perf

func SumPrealloc(xs []int) int {
	s := 0
	for _, v := range xs {
		s += v
	}
	return s
}
'''
    return "perf", {"perf.go": starter, "perf_test.go": test}, {"perf.go": sol}, "Implement Sum; run go test -bench=.\n"


@ex("docs_comment")
def _docs(slug):
    starter = '''package docs

// TODO: add a proper godoc comment for Add.
func Add(a, b int) int {
	return a + b
}
'''
    test = '''package docs

import "testing"

func TestAdd(t *testing.T) {
	if Add(2, 3) != 5 {
		t.Fatal()
	}
}
'''
    sol = '''package docs

// Add returns the sum of a and b.
func Add(a, b int) int {
	return a + b
}
'''
    return "docs", {"docs.go": starter, "docs_test.go": test}, {"docs.go": sol}, "Add a proper doc comment; run go doc .\n"


def simple_algo(pkg, starter, test, sol, readme):
    def gen(slug):
        return pkg, {f"{pkg}.go": starter, f"{pkg}_test.go": test}, {f"{pkg}.go": sol}, readme

    return gen


EX_KIND["algo_fib"] = simple_algo(
    "algo",
    '''package algo

func Fib(n int) int {
	// TODO iterative fib; Fib(0)=0 Fib(1)=1
	return -1
}
''',
    '''package algo

import "testing"

func TestFib(t *testing.T) {
	want := []int{0, 1, 1, 2, 3, 5, 8}
	for i, w := range want {
		if Fib(i) != w {
			t.Fatalf("Fib(%d)=%d want %d", i, Fib(i), w)
		}
	}
}
''',
    '''package algo

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
''',
    "Iterative Fibonacci.\n",
)

EX_KIND["algo_search"] = simple_algo(
    "algo",
    '''package algo

func BinarySearch(xs []int, target int) int {
	// TODO return index or -1; xs sorted ascending
	return -1
}
''',
    '''package algo

import "testing"

func TestBinarySearch(t *testing.T) {
	xs := []int{1, 3, 5, 7, 9}
	if BinarySearch(xs, 7) != 3 || BinarySearch(xs, 2) != -1 {
		t.Fatal()
	}
}
''',
    '''package algo

func BinarySearch(xs []int, target int) int {
	lo, hi := 0, len(xs)
	for lo < hi {
		mid := lo + (hi-lo)/2
		if xs[mid] < target {
			lo = mid + 1
		} else {
			hi = mid
		}
	}
	if lo < len(xs) && xs[lo] == target {
		return lo
	}
	return -1
}
''',
    "Binary search.\n",
)

EX_KIND["algo_stack"] = simple_algo(
    "algo",
    '''package algo

type Stack []int

func (s *Stack) Push(v int) { /* TODO */ }

func (s *Stack) Pop() (int, bool) {
	// TODO
	return 0, false
}
''',
    '''package algo

import "testing"

func TestStack(t *testing.T) {
	var s Stack
	s.Push(1)
	s.Push(2)
	v, ok := s.Pop()
	if !ok || v != 2 {
		t.Fatal()
	}
}
''',
    '''package algo

type Stack []int

func (s *Stack) Push(v int) { *s = append(*s, v) }

func (s *Stack) Pop() (int, bool) {
	if len(*s) == 0 {
		return 0, false
	}
	i := len(*s) - 1
	v := (*s)[i]
	*s = (*s)[:i]
	return v, true
}
''',
    "Slice-backed stack.\n",
)

EX_KIND["algo_heap"] = simple_algo(
    "algo",
    '''package algo

// MinIntHeap is a min-heap of ints using container/heap patterns manually:
// Push/Pop maintain heap order on a slice.
type MinIntHeap []int

func (h *MinIntHeap) Push(v int) {
	// TODO
}

func (h *MinIntHeap) Pop() (int, bool) {
	// TODO pop minimum
	return 0, false
}
''',
    '''package algo

import "testing"

func TestMinHeap(t *testing.T) {
	var h MinIntHeap
	for _, v := range []int{5, 1, 3} {
		h.Push(v)
	}
	v, ok := h.Pop()
	if !ok || v != 1 {
		t.Fatalf("%v %v", v, ok)
	}
}
''',
    '''package algo

type MinIntHeap []int

func (h MinIntHeap) less(i, j int) bool { return h[i] < h[j] }

func (h *MinIntHeap) up(i int) {
	for i > 0 {
		p := (i - 1) / 2
		if !h.less(i, p) {
			break
		}
		(*h)[i], (*h)[p] = (*h)[p], (*h)[i]
		i = p
	}
}

func (h *MinIntHeap) down(i int) {
	n := len(*h)
	for {
		l := 2*i + 1
		if l >= n {
			break
		}
		j := l
		if r := l + 1; r < n && h.less(r, l) {
			j = r
		}
		if !h.less(j, i) {
			break
		}
		(*h)[i], (*h)[j] = (*h)[j], (*h)[i]
		i = j
	}
}

func (h *MinIntHeap) Push(v int) {
	*h = append(*h, v)
	h.up(len(*h) - 1)
}

func (h *MinIntHeap) Pop() (int, bool) {
	if len(*h) == 0 {
		return 0, false
	}
	v := (*h)[0]
	last := len(*h) - 1
	(*h)[0] = (*h)[last]
	*h = (*h)[:last]
	if len(*h) > 0 {
		h.down(0)
	}
	return v, true
}
''',
    "Implement a min-heap.\n",
)

EX_KIND["algo_bfs"] = simple_algo(
    "algo",
    '''package algo

type Graph map[string][]string

func BFS(g Graph, start string) []string {
	// TODO
	return nil
}
''',
    '''package algo

import (
	"reflect"
	"testing"
)

func TestBFS(t *testing.T) {
	g := Graph{"A": {"B", "C"}, "B": {"D"}, "C": {}, "D": {}}
	got := BFS(g, "A")
	want := []string{"A", "B", "C", "D"}
	if !reflect.DeepEqual(got, want) {
		t.Fatalf("%v", got)
	}
}
''',
    '''package algo

type Graph map[string][]string

func BFS(g Graph, start string) []string {
	seen := map[string]bool{start: true}
	q := []string{start}
	var order []string
	for len(q) > 0 {
		u := q[0]
		q = q[1:]
		order = append(order, u)
		for _, v := range g[u] {
			if !seen[v] {
				seen[v] = true
				q = append(q, v)
			}
		}
	}
	return order
}
''',
    "BFS traversal order.\n",
)

EX_KIND["algo_bloom"] = simple_algo(
    "algo",
    '''package algo

type Bloom struct {
	bits []bool
	k    int
}

func NewBloom(size, k int) *Bloom {
	return &Bloom{bits: make([]bool, size), k: k}
}

func (b *Bloom) Add(s string) {
	// TODO set k bit positions derived from s
}

func (b *Bloom) MightContain(s string) bool {
	// TODO
	return false
}
''',
    '''package algo

import "testing"

func TestBloom(t *testing.T) {
	b := NewBloom(256, 3)
	b.Add("go")
	if !b.MightContain("go") {
		t.Fatal("should contain")
	}
}
''',
    '''package algo

type Bloom struct {
	bits []bool
	k    int
}

func NewBloom(size, k int) *Bloom {
	return &Bloom{bits: make([]bool, size), k: k}
}

func (b *Bloom) hashes(s string) []int {
	out := make([]int, b.k)
	var h uint64 = 14695981039346656037
	for i := 0; i < b.k; i++ {
		for _, c := range s {
			h ^= uint64(c) + uint64(i)
			h *= 1099511628211
		}
		out[i] = int(h % uint64(len(b.bits)))
	}
	return out
}

func (b *Bloom) Add(s string) {
	for _, i := range b.hashes(s) {
		b.bits[i] = true
	}
}

func (b *Bloom) MightContain(s string) bool {
	for _, i := range b.hashes(s) {
		if !b.bits[i] {
			return false
		}
	}
	return true
}
''',
    "Tiny bloom filter.\n",
)

EX_KIND["algo_dp"] = simple_algo(
    "algo",
    '''package algo

func ClimbStairs(n int) int {
	// TODO ways to climb n stairs taking 1 or 2 at a time
	return 0
}
''',
    '''package algo

import "testing"

func TestClimb(t *testing.T) {
	if ClimbStairs(1) != 1 || ClimbStairs(2) != 2 || ClimbStairs(3) != 3 || ClimbStairs(4) != 5 {
		t.Fatal()
	}
}
''',
    '''package algo

func ClimbStairs(n int) int {
	if n < 2 {
		return 1
	}
	a, b := 1, 1
	for i := 2; i <= n; i++ {
		a, b = b, a+b
	}
	return b
}
''',
    "Climb stairs DP.\n",
)

EX_KIND["algo_twosum"] = simple_algo(
    "algo",
    '''package algo

// TwoSum returns indices i,j such that nums[i]+nums[j]==target, or -1,-1.
func TwoSum(nums []int, target int) (int, int) {
	// TODO O(n) with map
	return -1, -1
}
''',
    '''package algo

import "testing"

func TestTwoSum(t *testing.T) {
	i, j := TwoSum([]int{2, 7, 11, 15}, 9)
	if i == -1 || numsSum([]int{2, 7, 11, 15}, i, j) != 9 {
		t.Fatalf("%d %d", i, j)
	}
}

func numsSum(a []int, i, j int) int { return a[i] + a[j] }
''',
    '''package algo

func TwoSum(nums []int, target int) (int, int) {
	seen := map[int]int{}
	for i, n := range nums {
		if j, ok := seen[target-n]; ok {
			return j, i
		}
		seen[n] = i
	}
	return -1, -1
}
''',
    "Two-sum in O(n).\n",
)


def conc_simple(pkg, starter, test, sol, readme):
    return simple_algo(pkg, starter, test, sol, readme)


EX_KIND["conc_waitgroup"] = conc_simple(
    "conc",
    '''package conc

import "sync"

// ParallelSum sums xs using up to workers goroutines + WaitGroup.
func ParallelSum(xs []int, workers int) int {
	// TODO
	_ = sync.WaitGroup{}
	return 0
}
''',
    '''package conc

import "testing"

func TestParallelSum(t *testing.T) {
	xs := []int{1, 2, 3, 4, 5}
	if ParallelSum(xs, 2) != 15 {
		t.Fatal()
	}
}
''',
    '''package conc

import "sync"

func ParallelSum(xs []int, workers int) int {
	if workers < 1 {
		workers = 1
	}
	ch := make(chan int, len(xs))
	for _, v := range xs {
		ch <- v
	}
	close(ch)
	var wg sync.WaitGroup
	partial := make([]int, workers)
	for w := 0; w < workers; w++ {
		wg.Add(1)
		go func(id int) {
			defer wg.Done()
			s := 0
			for v := range ch {
				s += v
			}
			partial[id] = s
		}(w)
	}
	wg.Wait()
	total := 0
	for _, p := range partial {
		total += p
	}
	return total
}
''',
    "Parallel sum with WaitGroup.\n",
)

EX_KIND["conc_pipeline"] = conc_simple(
    "conc",
    '''package conc

// Squares reads ints from in and sends squares to a new channel; closes out when in closes.
func Squares(in <-chan int) <-chan int {
	// TODO
	return nil
}
''',
    '''package conc

import (
	"reflect"
	"testing"
)

func TestSquares(t *testing.T) {
	in := make(chan int, 3)
	for _, v := range []int{1, 2, 3} {
		in <- v
	}
	close(in)
	var got []int
	for v := range Squares(in) {
		got = append(got, v)
	}
	if !reflect.DeepEqual(got, []int{1, 4, 9}) {
		t.Fatalf("%v", got)
	}
}
''',
    '''package conc

func Squares(in <-chan int) <-chan int {
	out := make(chan int)
	go func() {
		defer close(out)
		for v := range in {
			out <- v * v
		}
	}()
	return out
}
''',
    "Pipeline stage: squares.\n",
)

EX_KIND["conc_mutex"] = conc_simple(
    "conc",
    '''package conc

import "sync"

type Counter struct {
	mu sync.Mutex
	n  int
}

func (c *Counter) Inc() {
	// TODO
}

func (c *Counter) Value() int {
	// TODO
	return 0
}
''',
    '''package conc

import (
	"sync"
	"testing"
)

func TestCounter(t *testing.T) {
	var c Counter
	var wg sync.WaitGroup
	for i := 0; i < 1000; i++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			c.Inc()
		}()
	}
	wg.Wait()
	if c.Value() != 1000 {
		t.Fatalf("%d", c.Value())
	}
}
''',
    '''package conc

import "sync"

type Counter struct {
	mu sync.Mutex
	n  int
}

func (c *Counter) Inc() {
	c.mu.Lock()
	c.n++
	c.mu.Unlock()
}

func (c *Counter) Value() int {
	c.mu.Lock()
	defer c.mu.Unlock()
	return c.n
}
''',
    "Mutex counter; run go test -race.\n",
)

EX_KIND["conc_pool"] = conc_simple(
    "conc",
    '''package conc

import "context"

// RunJobs runs jobs with bounded workers; returns results in completion order not required —
// tests sort. Each job is a func() int.
func RunJobs(ctx context.Context, workers int, jobs []func() int) ([]int, error) {
	// TODO
	return nil, nil
}
''',
    '''package conc

import (
	"context"
	"sort"
	"testing"
)

func TestRunJobs(t *testing.T) {
	jobs := []func() int{
		func() int { return 1 },
		func() int { return 2 },
		func() int { return 3 },
	}
	got, err := RunJobs(context.Background(), 2, jobs)
	if err != nil {
		t.Fatal(err)
	}
	sort.Ints(got)
	if len(got) != 3 || got[0] != 1 || got[2] != 3 {
		t.Fatalf("%v", got)
	}
}
''',
    '''package conc

import (
	"context"
	"sync"
)

func RunJobs(ctx context.Context, workers int, jobs []func() int) ([]int, error) {
	if workers < 1 {
		workers = 1
	}
	jobCh := make(chan func() int)
	resCh := make(chan int, len(jobs))
	var wg sync.WaitGroup
	for i := 0; i < workers; i++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			for j := range jobCh {
				select {
				case <-ctx.Done():
					return
				default:
					resCh <- j()
				}
			}
		}()
	}
	for _, j := range jobs {
		jobCh <- j
	}
	close(jobCh)
	wg.Wait()
	close(resCh)
	out := make([]int, 0, len(jobs))
	for r := range resCh {
		out = append(out, r)
	}
	return out, ctx.Err()
}
''',
    "Bounded worker pool.\n",
)

EX_KIND["conc_cancel"] = conc_simple(
    "conc",
    '''package conc

import "context"

// DrainUntilCancel reads from in until ctx done or in closed; returns values read.
func DrainUntilCancel(ctx context.Context, in <-chan int) []int {
	// TODO
	return nil
}
''',
    '''package conc

import (
	"context"
	"testing"
	"time"
)

func TestDrain(t *testing.T) {
	ctx, cancel := context.WithCancel(context.Background())
	in := make(chan int)
	go func() {
		in <- 1
		in <- 2
		time.Sleep(20 * time.Millisecond)
		cancel()
	}()
	got := DrainUntilCancel(ctx, in)
	if len(got) < 1 {
		t.Fatalf("%v", got)
	}
}
''',
    '''package conc

import "context"

func DrainUntilCancel(ctx context.Context, in <-chan int) []int {
	var out []int
	for {
		select {
		case <-ctx.Done():
			return out
		case v, ok := <-in:
			if !ok {
				return out
			}
			out = append(out, v)
		}
	}
}
''',
    "Cancel-aware drain.\n",
)

EX_KIND["conc_parsum"] = EX_KIND["conc_waitgroup"]


# HTTP / infra / AI kinds — keep stdlib-only and testable

EX_KIND["http_health"] = simple_algo(
    "httpsvc",
    '''package httpsvc

import "net/http"

func HealthHandler(w http.ResponseWriter, r *http.Request) {
	// TODO write 200 and "ok"
}
''',
    '''package httpsvc

import (
	"net/http"
	"net/http/httptest"
	"testing"
)

func TestHealth(t *testing.T) {
	req := httptest.NewRequest(http.MethodGet, "/health", nil)
	rr := httptest.NewRecorder()
	HealthHandler(rr, req)
	if rr.Code != 200 || rr.Body.String() != "ok" {
		t.Fatalf("%d %q", rr.Code, rr.Body.String())
	}
}
''',
    '''package httpsvc

import "net/http"

func HealthHandler(w http.ResponseWriter, r *http.Request) {
	w.WriteHeader(http.StatusOK)
	_, _ = w.Write([]byte("ok"))
}
''',
    "Health handler.\n",
)

EX_KIND["http_middleware"] = simple_algo(
    "httpsvc",
    '''package httpsvc

import "net/http"

func WithHeader(next http.Handler, key, val string) http.Handler {
	// TODO set response header then call next
	return next
}
''',
    '''package httpsvc

import (
	"net/http"
	"net/http/httptest"
	"testing"
)

func TestWithHeader(t *testing.T) {
	h := WithHeader(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(200)
	}), "X-Test", "1")
	rr := httptest.NewRecorder()
	h.ServeHTTP(rr, httptest.NewRequest("GET", "/", nil))
	if rr.Header().Get("X-Test") != "1" {
		t.Fatal()
	}
}
''',
    '''package httpsvc

import "net/http"

func WithHeader(next http.Handler, key, val string) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set(key, val)
		next.ServeHTTP(w, r)
	})
}
''',
    "Header middleware.\n",
)

EX_KIND["grpc_sketch"] = simple_algo(
    "grpcex",
    '''package grpcex

// MethodPath builds "/package.Service/Method".
func MethodPath(pkg, service, method string) string {
	// TODO
	return ""
}
''',
    '''package grpcex

import "testing"

func TestMethodPath(t *testing.T) {
	if MethodPath("hw", "Greeter", "SayHello") != "/hw.Greeter/SayHello" {
		t.Fatal()
	}
}
''',
    '''package grpcex

func MethodPath(pkg, service, method string) string {
	return "/" + pkg + "." + service + "/" + method
}
''',
    "Sketch gRPC method path naming.\n",
)

EX_KIND["sql_param"] = simple_algo(
    "sqlx",
    '''package sqlx

import "fmt"

// UserByIDQuery returns a parameterized query and args for id.
// Use $1 style placeholder; do NOT concatenate id into the SQL string.
func UserByIDQuery(id string) (query string, args []any) {
	// TODO
	_ = fmt.Sprintf
	return "", nil
}
''',
    '''package sqlx

import (
	"strings"
	"testing"
)

func TestUserByIDQuery(t *testing.T) {
	q, args := UserByIDQuery("abc")
	if strings.Contains(q, "abc") {
		t.Fatal("id embedded in query")
	}
	if len(args) != 1 || args[0] != "abc" {
		t.Fatalf("%v", args)
	}
}
''',
    '''package sqlx

func UserByIDQuery(id string) (query string, args []any) {
	return `SELECT name FROM users WHERE id=$1`, []any{id}
}
''',
    "Parameterized SQL.\n",
)

EX_KIND["cache_aside"] = simple_algo(
    "cache",
    '''package cache

type Store struct {
	mem map[string]string
	db  map[string]string
}

func New(db map[string]string) *Store {
	return &Store{mem: map[string]string{}, db: db}
}

func (s *Store) Get(key string) (string, bool) {
	// TODO cache-aside
	return "", false
}

func (s *Store) Set(key, val string) {
	// TODO write db + invalidate/update cache
}
''',
    '''package cache

import "testing"

func TestCacheAside(t *testing.T) {
	s := New(map[string]string{"a": "1"})
	v, ok := s.Get("a")
	if !ok || v != "1" {
		t.Fatal()
	}
	s.Set("a", "2")
	v, ok = s.Get("a")
	if !ok || v != "2" {
		t.Fatal()
	}
}
''',
    '''package cache

type Store struct {
	mem map[string]string
	db  map[string]string
}

func New(db map[string]string) *Store {
	return &Store{mem: map[string]string{}, db: db}
}

func (s *Store) Get(key string) (string, bool) {
	if v, ok := s.mem[key]; ok {
		return v, true
	}
	v, ok := s.db[key]
	if !ok {
		return "", false
	}
	s.mem[key] = v
	return v, true
}

func (s *Store) Set(key, val string) {
	s.db[key] = val
	delete(s.mem, key)
}
''',
    "Cache-aside get/set.\n",
)

EX_KIND["obs_log"] = simple_algo(
    "obs",
    '''package obs

import "fmt"

// FormatLog returns key=value pairs joined by space for keys in stable order: level msg.
func FormatLog(level, msg string, kv map[string]string) string {
	// TODO include level and msg then sorted kv
	_ = fmt.Sprintf
	return ""
}
''',
    '''package obs

import (
	"strings"
	"testing"
)

func TestFormatLog(t *testing.T) {
	s := FormatLog("info", "hi", map[string]string{"b": "2", "a": "1"})
	if !strings.Contains(s, "level=info") || !strings.Contains(s, "msg=hi") || !strings.Contains(s, "a=1") {
		t.Fatalf("%q", s)
	}
}
''',
    '''package obs

import (
	"fmt"
	"sort"
	"strings"
)

func FormatLog(level, msg string, kv map[string]string) string {
	parts := []string{fmt.Sprintf("level=%s", level), fmt.Sprintf("msg=%s", msg)}
	keys := make([]string, 0, len(kv))
	for k := range kv {
		keys = append(keys, k)
	}
	sort.Strings(keys)
	for _, k := range keys {
		parts = append(parts, fmt.Sprintf("%s=%s", k, kv[k]))
	}
	return strings.Join(parts, " ")
}
''',
    "Structured log line formatter.\n",
)

EX_KIND["docker_multistage"] = simple_algo(
    "dockex",
    '''package dockex

// DockerfileMultiStage returns a minimal multi-stage Dockerfile string for module path app.
func DockerfileMultiStage(modulePath string) string {
	// TODO must contain "AS build" and "CGO_ENABLED=0" and "nonroot" or "scratch"/"distroless"
	return ""
}
''',
    '''package dockex

import (
	"strings"
	"testing"
)

func TestDockerfile(t *testing.T) {
	s := DockerfileMultiStage("example.com/app")
	for _, needle := range []string{"AS build", "CGO_ENABLED=0"} {
		if !strings.Contains(s, needle) {
			t.Fatalf("missing %s in %q", needle, s)
		}
	}
}
''',
    '''package dockex

func DockerfileMultiStage(modulePath string) string {
	return `FROM golang:1.22 AS build
WORKDIR /src
COPY . .
RUN CGO_ENABLED=0 go build -o /out/app ` + modulePath + `
FROM gcr.io/distroless/static:nonroot
COPY --from=build /out/app /app
USER nonroot:nonroot
ENTRYPOINT ["/app"]
`
}
''',
    "Generate multi-stage Dockerfile text.\n",
)

EX_KIND["k8s_reconcile"] = simple_algo(
    "reconcile",
    '''package reconcile

type Object struct {
	Desired int
	Actual  int
}

// Reconcile mutates o.Actual toward Desired by at most 1 per call; returns whether done.
func Reconcile(o *Object) bool {
	// TODO
	return false
}
''',
    '''package reconcile

import "testing"

func TestReconcile(t *testing.T) {
	o := &Object{Desired: 3, Actual: 0}
	for i := 0; i < 10 && !Reconcile(o); i++ {
	}
	if o.Actual != 3 {
		t.Fatalf("%d", o.Actual)
	}
}
''',
    '''package reconcile

type Object struct {
	Desired int
	Actual  int
}

func Reconcile(o *Object) bool {
	if o.Actual == o.Desired {
		return true
	}
	if o.Actual < o.Desired {
		o.Actual++
	} else {
		o.Actual--
	}
	return o.Actual == o.Desired
}
''',
    "Idempotent reconcile step.\n",
)

EX_KIND["cloud_retry"] = simple_algo(
    "retry",
    '''package retry

import "context"

// Do retries fn on error until success or ctx done. attempts counts tries.
func Do(ctx context.Context, attempts int, fn func() error) error {
	// TODO
	return nil
}
''',
    '''package retry

import (
	"context"
	"errors"
	"testing"
)

func TestDo(t *testing.T) {
	n := 0
	err := Do(context.Background(), 3, func() error {
		n++
		if n < 3 {
			return errors.New("transient")
		}
		return nil
	})
	if err != nil || n != 3 {
		t.Fatalf("%v %d", err, n)
	}
}
''',
    '''package retry

import "context"

func Do(ctx context.Context, attempts int, fn func() error) error {
	var err error
	for i := 0; i < attempts; i++ {
		select {
		case <-ctx.Done():
			return ctx.Err()
		default:
		}
		err = fn()
		if err == nil {
			return nil
		}
	}
	return err
}
''',
    "Retry with attempts + context.\n",
)

EX_KIND["reliab_shutdown"] = simple_algo(
    "reliab",
    '''package reliab

import "sync"

// Runner tracks in-flight work; Shutdown waits for all After Start completes.
type Runner struct {
	wg sync.WaitGroup
}

func (r *Runner) Start(fn func()) {
	// TODO
}

func (r *Runner) Shutdown() {
	// TODO
}
''',
    '''package reliab

import (
	"sync/atomic"
	"testing"
	"time"
)

func TestShutdown(t *testing.T) {
	var r Runner
	var done atomic.Bool
	r.Start(func() {
		time.Sleep(30 * time.Millisecond)
		done.Store(true)
	})
	r.Shutdown()
	if !done.Load() {
		t.Fatal("shutdown returned early")
	}
}
''',
    '''package reliab

import "sync"

type Runner struct {
	wg sync.WaitGroup
}

func (r *Runner) Start(fn func()) {
	r.wg.Add(1)
	go func() {
		defer r.wg.Done()
		fn()
	}()
}

func (r *Runner) Shutdown() { r.wg.Wait() }
''',
    "Graceful worker shutdown.\n",
)

EX_KIND["ai_dot"] = simple_algo(
    "num",
    '''package num

func Dot(a, b []float64) float64 {
	// TODO panic or return 0 if lengths differ — tests use equal lengths
	return 0
}

func AlmostEqual(a, b, eps float64) bool {
	// TODO
	return false
}
''',
    '''package num

import "testing"

func TestDot(t *testing.T) {
	if Dot([]float64{1, 2}, []float64{3, 4}) != 11 {
		t.Fatal()
	}
	if !AlmostEqual(0.1+0.2, 0.3, 1e-9) {
		t.Fatal("eps")
	}
}
''',
    '''package num

func Dot(a, b []float64) float64 {
	var s float64
	for i := range a {
		s += a[i] * b[i]
	}
	return s
}

func AlmostEqual(a, b, eps float64) bool {
	d := a - b
	if d < 0 {
		d = -d
	}
	return d <= eps
}
''',
    "Dot product + epsilon compare.\n",
)

EX_KIND["ai_batch"] = simple_algo(
    "pipe",
    '''package pipe

// BatchChunks splits xs into batches of at most size.
func BatchChunks(xs []int, size int) [][]int {
	// TODO
	return nil
}
''',
    '''package pipe

import (
	"reflect"
	"testing"
)

func TestBatch(t *testing.T) {
	got := BatchChunks([]int{1, 2, 3, 4, 5}, 2)
	want := [][]int{{1, 2}, {3, 4}, {5}}
	if !reflect.DeepEqual(got, want) {
		t.Fatalf("%v", got)
	}
}
''',
    '''package pipe

func BatchChunks(xs []int, size int) [][]int {
	if size < 1 {
		return nil
	}
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
''',
    "Batch helper for pipelines.\n",
)

EX_KIND["ai_sse"] = simple_algo(
    "sse",
    '''package sse

import "strings"

// ParseDataLines extracts payloads from SSE "data: ..." lines; skips empties and [DONE].
func ParseDataLines(stream string) []string {
	// TODO
	_ = strings.Split
	return nil
}
''',
    '''package sse

import (
	"reflect"
	"testing"
)

func TestParse(t *testing.T) {
	s := "data: hi\\n\\ndata: there\\n\\ndata: [DONE]\\n\\n"
	got := ParseDataLines(s)
	want := []string{"hi", "there"}
	if !reflect.DeepEqual(got, want) {
		t.Fatalf("%v", got)
	}
}
''',
    '''package sse

import "strings"

func ParseDataLines(stream string) []string {
	var out []string
	for _, line := range strings.Split(stream, "\\n") {
		line = strings.TrimSpace(line)
		if !strings.HasPrefix(line, "data:") {
			continue
		}
		payload := strings.TrimSpace(strings.TrimPrefix(line, "data:"))
		if payload == "" || payload == "[DONE]" {
			continue
		}
		out = append(out, payload)
	}
	return out
}
''',
    "Parse SSE data lines.\n",
)

# Fix ai_sse - I escaped wrong. In the sol string I used \\n in Split which is wrong for real code.
# Will fix in a patch after - actually in the starter/sol written to file, `strings.Split(stream, "\\n")` 
# would split on backslash-n literally. Need real newline. Let me fix when writing - override below.

EX_KIND["ai_cosine"] = simple_algo(
    "vec",
    '''package vec

func Norm(a []float64) float64 {
	// TODO L2 norm
	return 0
}

func Cosine(a, b []float64) float64 {
	// TODO
	return 0
}
''',
    '''package vec

import "testing"

func TestCosine(t *testing.T) {
	a := []float64{1, 0}
	b := []float64{1, 0}
	if Cosine(a, b) < 0.999 {
		t.Fatal()
	}
}
''',
    '''package vec

import "math"

func Norm(a []float64) float64 {
	var s float64
	for _, v := range a {
		s += v * v
	}
	return math.Sqrt(s)
}

func Cosine(a, b []float64) float64 {
	var dot float64
	for i := range a {
		dot += a[i] * b[i]
	}
	return dot / (Norm(a) * Norm(b))
}
''',
    "Cosine similarity.\n",
)

EX_KIND["ai_chunk"] = simple_algo(
    "rag",
    '''package rag

// Chunk splits s into pieces of at most size runes with overlap runes.
func Chunk(s string, size, overlap int) []string {
	// TODO
	return nil
}
''',
    '''package rag

import "testing"

func TestChunk(t *testing.T) {
	got := Chunk("abcdefghij", 4, 2)
	if len(got) < 2 || got[0] != "abcd" {
		t.Fatalf("%v", got)
	}
}
''',
    '''package rag

func Chunk(s string, size, overlap int) []string {
	r := []rune(s)
	if size < 1 {
		return nil
	}
	if overlap >= size {
		overlap = size - 1
	}
	var out []string
	for start := 0; start < len(r); {
		end := start + size
		if end > len(r) {
			end = len(r)
		}
		out = append(out, string(r[start:end]))
		if end == len(r) {
			break
		}
		start = end - overlap
	}
	return out
}
''',
    "RAG chunking with overlap.\n",
)

EX_KIND["ai_infer_queue"] = simple_algo(
    "infer",
    '''package infer

type Queue struct {
	ch chan string
}

func NewQueue(depth int) *Queue {
	return &Queue{ch: make(chan string, depth)}
}

// Enqueue returns false if queue full (backpressure).
func (q *Queue) Enqueue(job string) bool {
	// TODO non-blocking send
	return false
}

func (q *Queue) Dequeue() (string, bool) {
	// TODO
	return "", false
}
''',
    '''package infer

import "testing"

func TestQueue(t *testing.T) {
	q := NewQueue(1)
	if !q.Enqueue("a") || q.Enqueue("b") {
		t.Fatal("backpressure")
	}
	v, ok := q.Dequeue()
	if !ok || v != "a" {
		t.Fatal()
	}
}
''',
    '''package infer

type Queue struct {
	ch chan string
}

func NewQueue(depth int) *Queue {
	return &Queue{ch: make(chan string, depth)}
}

func (q *Queue) Enqueue(job string) bool {
	select {
	case q.ch <- job:
		return true
	default:
		return false
	}
}

func (q *Queue) Dequeue() (string, bool) {
	select {
	case v := <-q.ch:
		return v, true
	default:
		return "", false
	}
}
''',
    "Inference queue with backpressure.\n",
)

EX_KIND["ai_agent_loop"] = simple_algo(
    "agent",
    '''package agent

type ToolFunc func(args string) string

// RunLoop calls decide repeatedly. decide returns ("final", answer) or ("tool", name|args).
// Stop at maxSteps. tools maps name -> func.
func RunLoop(maxSteps int, decide func(history []string) (kind, payload string), tools map[string]ToolFunc) (string, error) {
	// TODO
	return "", nil
}
''',
    '''package agent

import "testing"

func TestRunLoop(t *testing.T) {
	steps := 0
	decide := func(h []string) (string, string) {
		steps++
		if steps == 1 {
			return "tool", "echo|hi"
		}
		return "final", "done:" + h[len(h)-1]
	}
	out, err := RunLoop(5, decide, map[string]ToolFunc{
		"echo": func(args string) string { return args },
	})
	if err != nil || out != "done:hi" {
		t.Fatalf("%q %v", out, err)
	}
}
''',
    '''package agent

import (
	"fmt"
	"strings"
)

type ToolFunc func(args string) string

func RunLoop(maxSteps int, decide func(history []string) (kind, payload string), tools map[string]ToolFunc) (string, error) {
	var history []string
	for step := 0; step < maxSteps; step++ {
		kind, payload := decide(history)
		switch kind {
		case "final":
			return payload, nil
		case "tool":
			name, args, _ := strings.Cut(payload, "|")
			fn, ok := tools[name]
			if !ok {
				return "", fmt.Errorf("unknown tool %s", name)
			}
			history = append(history, fn(args))
		default:
			return "", fmt.Errorf("unknown kind %s", kind)
		}
	}
	return "", fmt.Errorf("max steps")
}
''',
    "Bounded agent tool loop.\n",
)

EX_KIND["ai_eval"] = simple_algo(
    "evalx",
    '''package evalx

type Case struct {
	Got, Want string
}

func ExactMatchAccuracy(cases []Case) float64 {
	// TODO fraction matching exactly
	return 0
}
''',
    '''package evalx

import "testing"

func TestAcc(t *testing.T) {
	a := ExactMatchAccuracy([]Case{{"a", "a"}, {"b", "c"}})
	if a != 0.5 {
		t.Fatalf("%v", a)
	}
}
''',
    '''package evalx

type Case struct {
	Got, Want string
}

func ExactMatchAccuracy(cases []Case) float64 {
	if len(cases) == 0 {
		return 0
	}
	ok := 0
	for _, c := range cases {
		if c.Got == c.Want {
			ok++
		}
	}
	return float64(ok) / float64(len(cases))
}
''',
    "Eval accuracy helper.\n",
)

EX_KIND["capstone_infra"] = simple_algo(
    "capstone",
    '''package capstone

// JobQueue is a tiny in-memory queue for the infra capstone starter.
type JobQueue struct {
	jobs []string
}

func (q *JobQueue) Enqueue(id string) {
	// TODO
}

func (q *JobQueue) Dequeue() (string, bool) {
	// TODO FIFO
	return "", false
}
''',
    '''package capstone

import "testing"

func TestJobQueue(t *testing.T) {
	var q JobQueue
	q.Enqueue("a")
	q.Enqueue("b")
	a, ok := q.Dequeue()
	if !ok || a != "a" {
		t.Fatal()
	}
}
''',
    '''package capstone

type JobQueue struct {
	jobs []string
}

func (q *JobQueue) Enqueue(id string) { q.jobs = append(q.jobs, id) }

func (q *JobQueue) Dequeue() (string, bool) {
	if len(q.jobs) == 0 {
		return "", false
	}
	id := q.jobs[0]
	q.jobs = q.jobs[1:]
	return id, true
}
''',
    "Capstone starter: job queue. Expand into full API per lesson PDF.\n",
)

EX_KIND["capstone_algo"] = simple_algo(
    "capstone",
    '''package capstone

// InvertedIndex maps token -> doc IDs.
type InvertedIndex map[string][]string

func (idx InvertedIndex) Add(docID, text string) {
	// TODO lowercase split on spaces; append docID if not present
}

func (idx InvertedIndex) Query(token string) []string {
	// TODO
	return nil
}
''',
    '''package capstone

import (
	"reflect"
	"testing"
)

func TestIndex(t *testing.T) {
	idx := InvertedIndex{}
	idx.Add("d1", "Go is cool")
	idx.Add("d2", "go servers")
	got := idx.Query("go")
	want := []string{"d1", "d2"}
	if !reflect.DeepEqual(got, want) {
		t.Fatalf("%v", got)
	}
}
''',
    '''package capstone

import "strings"

type InvertedIndex map[string][]string

func (idx InvertedIndex) Add(docID, text string) {
	for _, tok := range strings.Fields(strings.ToLower(text)) {
		list := idx[tok]
		found := false
		for _, d := range list {
			if d == docID {
				found = true
				break
			}
		}
		if !found {
			idx[tok] = append(list, docID)
		}
	}
}

func (idx InvertedIndex) Query(token string) []string {
	return idx[strings.ToLower(token)]
}
''',
    "Capstone starter: inverted index. Expand per lesson PDF.\n",
)

EX_KIND["capstone_ai"] = simple_algo(
    "capstone",
    '''package capstone

type Doc struct {
	ID   string
	Text string
	Vec  []float64
}

func Cosine(a, b []float64) float64 {
	// TODO
	return 0
}

func TopK(docs []Doc, query []float64, k int) []Doc {
	// TODO return up to k docs by cosine desc
	return nil
}
''',
    '''package capstone

import "testing"

func TestTopK(t *testing.T) {
	docs := []Doc{
		{ID: "a", Vec: []float64{1, 0}},
		{ID: "b", Vec: []float64{0.9, 0.1}},
		{ID: "c", Vec: []float64{0, 1}},
	}
	got := TopK(docs, []float64{1, 0}, 2)
	if len(got) != 2 || got[0].ID != "a" {
		t.Fatalf("%v", got)
	}
}
''',
    '''package capstone

import (
	"math"
	"sort"
)

type Doc struct {
	ID   string
	Text string
	Vec  []float64
}

func Cosine(a, b []float64) float64 {
	var dot, na, nb float64
	for i := range a {
		dot += a[i] * b[i]
		na += a[i] * a[i]
		nb += b[i] * b[i]
	}
	return dot / (math.Sqrt(na) * math.Sqrt(nb))
}

func TopK(docs []Doc, query []float64, k int) []Doc {
	type sc struct {
		d Doc
		s float64
	}
	scored := make([]sc, len(docs))
	for i, d := range docs {
		scored[i] = sc{d, Cosine(d.Vec, query)}
	}
	sort.Slice(scored, func(i, j int) bool { return scored[i].s > scored[j].s })
	if k > len(scored) {
		k = len(scored)
	}
	out := make([]Doc, k)
	for i := 0; i < k; i++ {
		out[i] = scored[i].d
	}
	return out
}
''',
    "Capstone starter: vector top-K. Expand into full RAG service per lesson PDF.\n",
)


def fix_sse():
    EX_KIND["ai_sse"] = simple_algo(
        "sse",
        "package sse\n\nimport \"strings\"\n\n// ParseDataLines extracts payloads from SSE data lines; skips empties and [DONE].\nfunc ParseDataLines(stream string) []string {\n\t// TODO\n\t_ = strings.Split\n\treturn nil\n}\n",
        'package sse\n\nimport (\n\t"reflect"\n\t"testing"\n)\n\nfunc TestParse(t *testing.T) {\n\ts := "data: hi\\n\\ndata: there\\n\\ndata: [DONE]\\n\\n"\n\tgot := ParseDataLines(s)\n\twant := []string{"hi", "there"}\n\tif !reflect.DeepEqual(got, want) {\n\t\tt.Fatalf("%v", got)\n\t}\n}\n',
        'package sse\n\nimport "strings"\n\nfunc ParseDataLines(stream string) []string {\n\tvar out []string\n\tfor _, line := range strings.Split(stream, "\\n") {\n\t\tline = strings.TrimSpace(line)\n\t\tif !strings.HasPrefix(line, "data:") {\n\t\t\tcontinue\n\t\t}\n\t\tpayload := strings.TrimSpace(strings.TrimPrefix(line, "data:"))\n\t\tif payload == "" || payload == "[DONE]" {\n\t\t\tcontinue\n\t\t}\n\t\tout = append(out, payload)\n\t}\n\treturn out\n}\n',
        "Parse SSE data lines.\n",
    )


fix_sse()
# The sol still has wrong Split - need actual newline character in generated Go source
EX_KIND["ai_sse"] = simple_algo(
    "sse",
    "package sse\n\nimport \"strings\"\n\nfunc ParseDataLines(stream string) []string {\n\t// TODO\n\t_ = strings.Split\n\treturn nil\n}\n",
    "package sse\n\nimport (\n\t\"reflect\"\n\t\"testing\"\n)\n\nfunc TestParse(t *testing.T) {\n\ts := \"data: hi\\n\\ndata: there\\n\\ndata: [DONE]\\n\\n\"\n\tgot := ParseDataLines(s)\n\twant := []string{\"hi\", \"there\"}\n\tif !reflect.DeepEqual(got, want) {\n\t\tt.Fatalf(\"%v\", got)\n\t}\n}\n",
    "package sse\n\nimport \"strings\"\n\nfunc ParseDataLines(stream string) []string {\n\tvar out []string\n\tfor _, line := range strings.Split(stream, \"\\n\") {\n\t\tline = strings.TrimSpace(line)\n\t\tif !strings.HasPrefix(line, \"data:\") {\n\t\t\tcontinue\n\t\t}\n\t\tpayload := strings.TrimSpace(strings.TrimPrefix(line, \"data:\"))\n\t\tif payload == \"\" || payload == \"[DONE]\" {\n\t\t\tcontinue\n\t\t}\n\t\tout = append(out, payload)\n\t}\n\treturn out\n}\n",
    "Parse SSE data lines.\n",
)

def _sse_fixed(slug):
    starter = '''package sse

import "strings"

func ParseDataLines(stream string) []string {
	// TODO
	_ = strings.Split
	return nil
}
'''
    test = '''package sse

import (
	"reflect"
	"testing"
)

func TestParse(t *testing.T) {
	s := "data: hi\\n\\ndata: there\\n\\ndata: [DONE]\\n\\n"
	got := ParseDataLines(s)
	want := []string{"hi", "there"}
	if !reflect.DeepEqual(got, want) {
		t.Fatalf("%v", got)
	}
}
'''
    # Go source must contain the two characters \n inside quotes (not a real newline).
    esc = chr(92) + "n"
    sol = (
        "package sse\n\nimport \"strings\"\n\n"
        "func ParseDataLines(stream string) []string {\n"
        "\tvar out []string\n"
        f'\tfor _, line := range strings.Split(stream, "{esc}") {{\n'
        "\t\tline = strings.TrimSpace(line)\n"
        '		if !strings.HasPrefix(line, "data:") {\n'
        "\t\t\tcontinue\n"
        "\t\t}\n"
        '		payload := strings.TrimSpace(strings.TrimPrefix(line, "data:"))\n'
        '		if payload == "" || payload == "[DONE]" {\n'
        "\t\t\tcontinue\n"
        "\t\t}\n"
        "\t\tout = append(out, payload)\n"
        "\t}\n"
        "\treturn out\n"
        "}\n"
    )
    return "sse", {"sse.go": starter, "sse_test.go": test}, {"sse.go": sol}, "Parse SSE data lines.\n"


EX_KIND["ai_sse"] = _sse_fixed


def write_early_exercise(m: dict):
    ex = m["ex"]
    if ex.get("skip"):
        return
    slug = m["slug"]
    mod = f"goodway/exercises/{slug}"
    if ex.get("module_path"):
        mod = ex["module_path"]
    pkg_dir_name = ex.get("subdir") or "."
    ex_root = ROOT / "exercises" / slug
    sol_root = ROOT / "solutions" / slug
    readme = exercise_readme_md(m, ex.get("readme", ""))
    sol_readme = (
        "Reference solution. Study after attempting.\n\n"
        "Compare idioms, then rewrite from memory tomorrow.\n"
    )

    pkg = ex["pkg"]
    if pkg_dir_name == ".":
        write_go_module(
            ex_root,
            mod,
            {
                f"{pkg}.go": ex["starter"],
                f"{pkg}_test.go": ex["test"],
                "README.md": readme,
            },
        )
        write_go_module(
            sol_root,
            mod,
            {
                f"{pkg}.go": ex["solution"],
                "README.md": sol_readme,
            },
        )
        return

    # nested package e.g. mathx with external test package
    ex_root.mkdir(parents=True, exist_ok=True)
    (ex_root / "go.mod").write_text(f"module {mod}\n\ngo {GO_VERSION}\n", encoding="utf-8")
    (ex_root / "README.md").write_text(readme, encoding="utf-8")
    sub = ex_root / pkg_dir_name
    sub.mkdir(parents=True, exist_ok=True)
    (sub / f"{pkg}.go").write_text(ex["starter"], encoding="utf-8")
    (ex_root / f"{pkg}_export_test.go").write_text(ex["test"], encoding="utf-8")
    sol_root.mkdir(parents=True, exist_ok=True)
    (sol_root / "go.mod").write_text(f"module {mod}\n\ngo {GO_VERSION}\n", encoding="utf-8")
    (sol_root / "README.md").write_text(sol_readme, encoding="utf-8")
    ssub = sol_root / pkg_dir_name
    ssub.mkdir(parents=True, exist_ok=True)
    (ssub / f"{pkg}.go").write_text(ex["solution"], encoding="utf-8")


def write_kind_exercise(m: dict):
    slug = m["slug"]
    kind = m["ex_kind"]
    if kind not in EX_KIND:
        raise SystemExit(f"missing exercise kind {kind} for {slug}")
    pkg, files, sol_files, short_readme = EX_KIND[kind](slug)
    mod = f"goodway/exercises/{slug}"
    readme = exercise_readme_md(m, short_readme)
    write_go_module(ROOT / "exercises" / slug, mod, {**files, "README.md": readme})
    write_go_module(
        ROOT / "solutions" / slug,
        mod,
        {
            **sol_files,
            "README.md": "Reference solution. Study after attempting.\n\n"
            "Compare idioms, then rewrite from memory tomorrow.\n",
        },
    )


def normalize_early():
    """Convert early MODULES into lesson bodies."""
    out = []
    for m in early.MODULES:
        out.append(
            {
                **m,
                "body": m["concepts"],
                "pitfalls": m["pitfalls"],
                "checks": m["checks"],
                "reading": m["reading"],
            }
        )
    return out


def write_readme(all_meta):
    rows = "\n".join(
        f"| {m['n']:02d} | {m['title']} | {m['phase']} | {m['days']} | `lessons/{m['slug']}/` | `pdfs/{m['slug']}.pdf` |"
        for m in all_meta
    )
    text = f"""# Go Goodway: Fundamentals to Proficiency (AI + Infra)

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

## Curriculum map

| # | Title | Phase | Time | Lesson | PDF |
|---|-------|-------|------|--------|-----|
{rows}

## Pace guide

- Phases 0–3: ~1 lesson/day (a few hours)
- Phases 4–5: 1–2 days/lesson
- Phases 6–7: multi-day modules
- Capstones: several days each

## Quality bar

You are done with a lesson when you can explain the concepts aloud, pass the tests
without looking at solutions, and rewrite the code from memory the next day.
"""
    (ROOT / "README.md").write_text(text, encoding="utf-8")


def write_progress(all_meta):
    lines = ["# Progress tracker\n", "Check boxes as you complete each lesson (PDF + exercises + rewrite).\n"]
    phase = None
    for m in all_meta:
        if m["phase"] != phase:
            phase = m["phase"]
            lines.append(f"\n## {phase}\n")
        lines.append(f"- [ ] `{m['slug']}` — {m['title']} ({m['days']})")
    lines.append("\n")
    (ROOT / "curriculum" / "PROGRESS.md").write_text("\n".join(lines), encoding="utf-8")


def main():
    early_list = normalize_early()
    later_list = later.LATER
    # merge by number
    by_n = {m["n"]: m for m in early_list}
    for m in later_list:
        by_n[m["n"]] = m
    all_meta = [by_n[i] for i in range(0, 56)]

    for m in all_meta:
        lesson_dir = ROOT / "lessons" / m["slug"]
        lesson_dir.mkdir(parents=True, exist_ok=True)
        body = m.get("body") or m.get("concepts") or ""
        (lesson_dir / "lesson.md").write_text(lesson_md(m, body), encoding="utf-8")

        if m["n"] <= 8:
            write_early_exercise(m)
        else:
            write_kind_exercise(m)

    write_readme(all_meta)
    (ROOT / "curriculum").mkdir(exist_ok=True)
    write_progress(all_meta)
    (ROOT / "pdfs").mkdir(exist_ok=True)
    (ROOT / "pdfs" / ".gitkeep").write_text("", encoding="utf-8")

    print(f"Wrote {len(all_meta)} lessons + exercises/solutions")


if __name__ == "__main__":
    main()

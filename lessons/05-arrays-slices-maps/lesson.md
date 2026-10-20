---
title: "05. Arrays, Slices, and Maps (Memory Intuition)"
---

# 05. Arrays, Slices, and Maps (Memory Intuition)

**Phase:** Phase 1 — CS fundamentals through Go  
**Estimated time:** 1–2 days  
**Slug:** `05-arrays-slices-maps`

## Learning objectives

- Distinguish arrays (fixed) from slices (dynamic views)
- Explain slice header: pointer, length, capacity
- Grow slices with append and understand reallocation
- Use maps safely (including comma-ok idiom)

## Prerequisites

Complete prior numbered lessons. Type every example yourself.

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

## Common mistakes (especially from Python instincts)

- Thinking slices always copy (they often share memory)
- Reading map missing key without comma-ok and treating 0 as real data
- Appending in a loop without pre-sizing when size is known (`make([]T, 0, n)`)

## Exercises

Work in `exercises/05-arrays-slices-maps/`. Read that folder's `README.md`.

- **A (Drill):** make unit tests pass with the simplest correct code.
- **B (Apply):** extend with an edge case called out in the exercise README.
- **C (Challenge):** rewrite your solution from memory the next day without looking.

**Do not open `solutions/05-arrays-slices-maps/` until you have an honest failing attempt.**

## Self-check

1. What are the three fields of a slice header?
2. Why can `append` invalidate assumptions about shared backing arrays?
3. How do you distinguish missing key from zero value?

## Further reading

- https://go.dev/blog/slices-intro
- https://go.dev/blog/maps

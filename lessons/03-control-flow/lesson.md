---
title: "03. Control Flow: if, for, and switch"
---

# 03. Control Flow: if, for, and switch

**Phase:** Phase 1 — CS fundamentals through Go  
**Estimated time:** 1 day  
**Slug:** `03-control-flow`

## Learning objectives

- Write idiomatic if statements with optional init
- Use Go's single loop construct (`for`) in all forms
- Use switch without accidental fallthrough
- Prefer clear control flow over clever nesting

## Prerequisites

Complete prior numbered lessons. Type every example yourself.

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

## Common mistakes (especially from Python instincts)

- Expecting C-style fallthrough in switch
- Writing `while` — it does not exist; use `for cond`
- Forgetting braces (required even for one-liners)

## Exercises

Work in `exercises/03-control-flow/`. Read that folder's `README.md`.

- **A (Drill):** make unit tests pass with the simplest correct code.
- **B (Apply):** extend with an edge case called out in the exercise README.
- **C (Challenge):** rewrite your solution from memory the next day without looking.

**Do not open `solutions/03-control-flow/` until you have an honest failing attempt.**

## Self-check

1. Rewrite a while-loop as Go `for`
2. When is switch-on-true preferable to if/else?
3. What is the scope of a variable declared in `if init`?

## Further reading

- https://go.dev/tour/flowcontrol

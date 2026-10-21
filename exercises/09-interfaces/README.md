# Exercise: 09. Interfaces and Composition

## Goal

Convert reading into **retrievable skill**. The tests are the specification.

## Concepts from the lesson

- Define interfaces as sets of methods
- Accept interfaces, return concrete types in APIs
- Compose behavior via small interfaces
- Understand the empty interface and `any`

## Task

Implement Rect.Area and TotalArea(shapes []Shape) float64 for the Shape interface.

## Examples / expected behavior

TotalArea([]Shape{Rect{2,3}, Rect{1,1}}) → 7. `go test`.

## How to work

1. Read this README, then re-open `lessons/09-interfaces/lesson.md`.
2. Run the tests once to get a failure checklist.
3. Implement the smallest correct code; re-run after each function.
4. When stuck, re-type a lesson example into a scratch file and adapt it.
5. After green: explain each exported function in one sentence without looking.

## Done when

- Tests pass
- You can rewrite tomorrow without peeking at today's solution

**Do not open `solutions/09-interfaces/` until after a real attempt (15+ minutes).**

# Exercise: 42. Kubernetes-Oriented Go: Controllers and client-go

## Goal

Convert reading into **retrievable skill**. The tests are the specification.

## Concepts from the lesson

- Explain control loops (reconcile)
- Sketch a controller with client-go concepts
- Use leader election awareness
- Design for level-triggered reconciliation

## Task

Implement reconcile decision stubs matching tests.

## Examples / expected behavior

desired==actual → ok; else → update action.

## How to work

1. Read this README, then re-open `lessons/42-kubernetes-go/lesson.md`.
2. Run the tests once to get a failure checklist.
3. Implement the smallest correct code; re-run after each function.
4. When stuck, re-type a lesson example into a scratch file and adapt it.
5. After green: explain each exported function in one sentence without looking.

## Done when

- Tests pass
- You can rewrite tomorrow without peeking at today's solution

**Do not open `solutions/42-kubernetes-go/` until after a real attempt (15+ minutes).**

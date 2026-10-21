# Exercise: 29. Goroutines and the Scheduler

## Goal

Convert reading into **retrievable skill**. The tests are the specification.

## Concepts from the lesson

- Start goroutines with go
- Explain M:N scheduling at a high level
- Avoid leaking goroutines
- Synchronize completion with WaitGroup

## Task

Use WaitGroup (or the exercise API) so all goroutines finish before return.

## Examples / expected behavior

Tests wait for results; hanging means missing Done/cancel.

## How to work

1. Read this README, then re-open `lessons/29-goroutines/lesson.md`.
2. Run the tests once to get a failure checklist.
3. Implement the smallest correct code; re-run after each function.
4. When stuck, re-type a lesson example into a scratch file and adapt it.
5. After green: explain each exported function in one sentence without looking.

## Done when

- Tests pass
- You can rewrite tomorrow without peeking at today's solution

**Do not open `solutions/29-goroutines/` until after a real attempt (15+ minutes).**

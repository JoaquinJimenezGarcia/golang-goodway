# Exercise: 32. Worker Pools, Fan-in/out, Backpressure

## Goal

Convert reading into **retrievable skill**. The tests are the specification.

## Concepts from the lesson

- Build a bounded worker pool
- Apply fan-out / fan-in patterns
- Implement backpressure with buffered channels
- Bound concurrency in servers

## Task

Implement pool semantics: workers process all jobs; results complete.

## Examples / expected behavior

Doubling pool returns 2*job for each input.

## How to work

1. Read this README, then re-open `lessons/32-worker-pools/lesson.md`.
2. Run the tests once to get a failure checklist.
3. Implement the smallest correct code; re-run after each function.
4. When stuck, re-type a lesson example into a scratch file and adapt it.
5. After green: explain each exported function in one sentence without looking.

## Done when

- Tests pass
- You can rewrite tomorrow without peeking at today's solution

**Do not open `solutions/32-worker-pools/` until after a real attempt (15+ minutes).**

# Exercise: 31. Mutexes, Atomics, and sync Primitives

## Goal

Convert reading into **retrievable skill**. The tests are the specification.

## Concepts from the lesson

- Protect shared memory with mutexes
- Use RWMutex for read-heavy maps
- Know atomic operations for simple counters
- Prefer confining data to one goroutine when possible

## Task

Protect shared counters/state so tests pass under race detector.

## Examples / expected behavior

Final counter equals number of increments.

## How to work

1. Read this README, then re-open `lessons/31-mutexes-atomics/lesson.md`.
2. Run the tests once to get a failure checklist.
3. Implement the smallest correct code; re-run after each function.
4. When stuck, re-type a lesson example into a scratch file and adapt it.
5. After green: explain each exported function in one sentence without looking.

## Done when

- Tests pass
- You can rewrite tomorrow without peeking at today's solution

**Do not open `solutions/31-mutexes-atomics/` until after a real attempt (15+ minutes).**

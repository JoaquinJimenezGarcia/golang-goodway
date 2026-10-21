# Exercise: 33. Deadlocks, Races, and Cancellation Patterns

## Goal

Convert reading into **retrievable skill**. The tests are the specification.

## Concepts from the lesson

- Recognize classic deadlock patterns
- Eliminate data races systematically
- Cancel in-flight work with context
- Write concurrency regression tests

## Task

Ensure cancellation paths return instead of hanging; fix racey access.

## Examples / expected behavior

Functions return when ctx done; tests fail on timeout hang.

## How to work

1. Read this README, then re-open `lessons/33-deadlocks-races/lesson.md`.
2. Run the tests once to get a failure checklist.
3. Implement the smallest correct code; re-run after each function.
4. When stuck, re-type a lesson example into a scratch file and adapt it.
5. After green: explain each exported function in one sentence without looking.

## Done when

- Tests pass
- You can rewrite tomorrow without peeking at today's solution

**Do not open `solutions/33-deadlocks-races/` until after a real attempt (15+ minutes).**

# Exercise: 15. Context: Cancellation and Deadlines

## Goal

Convert reading into **retrievable skill**. The tests are the specification.

## Concepts from the lesson

- Pass context.Context as the first parameter
- Derive cancel and timeout contexts
- Propagate cancellation through goroutines and RPCs
- Never store contexts in structs long-term (usually)

## Task

Honor context cancellation/deadlines in the exercise function.

## Examples / expected behavior

When ctx times out, return ctx.Err() rather than hanging.

## How to work

1. Read this README, then re-open `lessons/15-context/lesson.md`.
2. Run the tests once to get a failure checklist.
3. Implement the smallest correct code; re-run after each function.
4. When stuck, re-type a lesson example into a scratch file and adapt it.
5. After green: explain each exported function in one sentence without looking.

## Done when

- Tests pass
- You can rewrite tomorrow without peeking at today's solution

**Do not open `solutions/15-context/` until after a real attempt (15+ minutes).**

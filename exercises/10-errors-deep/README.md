# Exercise: 10. Errors Deeply: Wrap, Is, As

## Goal

Convert reading into **retrievable skill**. The tests are the specification.

## Concepts from the lesson

- Wrap errors with context using fmt.Errorf and %w
- Use errors.Is and errors.As for inspection
- Choose sentinel vs custom error types
- Design error messages for operators and callers

## Task

Wrap errors with %w and detect sentinels via errors.Is in the exercise stubs.

## Examples / expected behavior

Wrapped ErrNotFound must satisfy errors.Is(err, ErrNotFound) == true.

## How to work

1. Read this README, then re-open `lessons/10-errors-deep/lesson.md`.
2. Run the tests once to get a failure checklist.
3. Implement the smallest correct code; re-run after each function.
4. When stuck, re-type a lesson example into a scratch file and adapt it.
5. After green: explain each exported function in one sentence without looking.

## Done when

- Tests pass
- You can rewrite tomorrow without peeking at today's solution

**Do not open `solutions/10-errors-deep/` until after a real attempt (15+ minutes).**

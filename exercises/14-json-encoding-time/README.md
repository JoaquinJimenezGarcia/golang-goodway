# Exercise: 14. JSON, Encoding, and Time

## Goal

Convert reading into **retrievable skill**. The tests are the specification.

## Concepts from the lesson

- Marshal and unmarshal JSON with struct tags
- Handle time.Time and timezones carefully
- Validate unknown fields when needed
- Avoid floating point for money — use integers

## Task

Implement JSON round-trip helpers to satisfy the exercise tests.

## Examples / expected behavior

Marshal then Unmarshal must preserve fields the tests check.

## How to work

1. Read this README, then re-open `lessons/14-json-encoding-time/lesson.md`.
2. Run the tests once to get a failure checklist.
3. Implement the smallest correct code; re-run after each function.
4. When stuck, re-type a lesson example into a scratch file and adapt it.
5. After green: explain each exported function in one sentence without looking.

## Done when

- Tests pass
- You can rewrite tomorrow without peeking at today's solution

**Do not open `solutions/14-json-encoding-time/` until after a real attempt (15+ minutes).**

# Exercise: 30. Channels, Select, and Pipelines

## Goal

Convert reading into **retrievable skill**. The tests are the specification.

## Concepts from the lesson

- Create buffered and unbuffered channels
- Use select for multi-wait
- Build pipeline stages
- Close channels from the sender side only

## Task

Wire channel pipeline/select behavior required by tests.

## Examples / expected behavior

Values sent must be received; closed channels terminate range.

## How to work

1. Read this README, then re-open `lessons/30-channels-select/lesson.md`.
2. Run the tests once to get a failure checklist.
3. Implement the smallest correct code; re-run after each function.
4. When stuck, re-type a lesson example into a scratch file and adapt it.
5. After green: explain each exported function in one sentence without looking.

## Done when

- Tests pass
- You can rewrite tomorrow without peeking at today's solution

**Do not open `solutions/30-channels-select/` until after a real attempt (15+ minutes).**

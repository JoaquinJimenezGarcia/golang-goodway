# Exercise: 47. Calling Model APIs: HTTP and SSE Streaming

## Goal

Convert reading into **retrievable skill**. The tests are the specification.

## Concepts from the lesson

- Call LLM HTTP APIs with timeouts
- Parse streaming SSE responses
- Handle rate limits and retries
- Bound concurrency to model backends

## Task

Parse SSE data lines as the exercise tests specify.

## Examples / expected behavior

"data: hi\n\n" -> ["hi"].

## How to work

1. Read this README, then re-open `lessons/47-model-apis/lesson.md`.
2. Run the tests once to get a failure checklist.
3. Implement the smallest correct code; re-run after each function.
4. When stuck, re-type a lesson example into a scratch file and adapt it.
5. After green: explain each exported function in one sentence without looking.

## Done when

- Tests pass
- You can rewrite tomorrow without peeking at today's solution

**Do not open `solutions/47-model-apis/` until after a real attempt (15+ minutes).**

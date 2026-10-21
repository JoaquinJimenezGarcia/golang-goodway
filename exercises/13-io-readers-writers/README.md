# Exercise: 13. I/O: io, Files, Readers and Writers

## Goal

Convert reading into **retrievable skill**. The tests are the specification.

## Concepts from the lesson

- Use io.Reader and io.Writer as the core I/O abstractions
- Stream data without loading entire files when possible
- Compose readers (bufio, limit, multi)
- Always close resources with defer carefully

## Task

Implement the reader-counting stub using io.Reader, not []byte whole-file assumptions.

## Examples / expected behavior

Counting lines/bytes from a strings.Reader should match tests.

## How to work

1. Read this README, then re-open `lessons/13-io-readers-writers/lesson.md`.
2. Run the tests once to get a failure checklist.
3. Implement the smallest correct code; re-run after each function.
4. When stuck, re-type a lesson example into a scratch file and adapt it.
5. After green: explain each exported function in one sentence without looking.

## Done when

- Tests pass
- You can rewrite tomorrow without peeking at today's solution

**Do not open `solutions/13-io-readers-writers/` until after a real attempt (15+ minutes).**

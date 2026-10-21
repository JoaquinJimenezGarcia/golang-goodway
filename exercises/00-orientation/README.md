# Exercise: 00. Orientation: Programs, Computers, and Go

## Goal

Convert reading into **retrievable skill**. The tests are the specification.

## Concepts from the lesson

- Explain what a program is and how source code becomes running software
- Describe CPU, memory, and the OS at a beginner level
- Contrast Go with Python (compiled, static types, concurrency model)
- Install the Go toolchain and run your first program
- Adopt the study method: attempt → struggle → solution → rewrite from memory

## Task

Implement `Greet(name string) string` so it returns `Hello, <name>`. This drills package layout, exported funcs, and `go test` as feedback.

## Examples / expected behavior

Greet("Ada") → "Hello, Ada". Greet("") → "Hello, ". Run: `cd exercises/00-orientation && go test -v`.

## How to work

1. Read this README, then re-open `lessons/00-orientation/lesson.md`.
2. Run the tests once to get a failure checklist.
3. Implement the smallest correct code; re-run after each function.
4. When stuck, re-type a lesson example into a scratch file and adapt it.
5. After green: explain each exported function in one sentence without looking.

## Done when

- Tests pass
- You can rewrite tomorrow without peeking at today's solution

**Do not open `solutions/00-orientation/` until after a real attempt (15+ minutes).**

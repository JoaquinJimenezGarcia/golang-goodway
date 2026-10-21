# Exercise: 04. Functions, Multiple Returns, and Error Basics

## Goal

Convert reading into **retrievable skill**. The tests are the specification.

## Concepts from the lesson

- Define functions with parameters and multiple return values
- Use the error interface as Go's primary failure signal
- Name return values when it improves clarity
- Avoid panic for ordinary errors

## Task

Implement ParsePositive(s): Atoi, then reject n<=0 with a clear error.

## Examples / expected behavior

ParsePositive("5")→(5,nil). "0" and "x" both return errors.

## How to work

1. Read this README, then re-open `lessons/04-functions-errors/lesson.md`.
2. Run the tests once to get a failure checklist.
3. Implement the smallest correct code; re-run after each function.
4. When stuck, re-type a lesson example into a scratch file and adapt it.
5. After green: explain each exported function in one sentence without looking.

## Done when

- Tests pass
- You can rewrite tomorrow without peeking at today's solution

**Do not open `solutions/04-functions-errors/` until after a real attempt (15+ minutes).**

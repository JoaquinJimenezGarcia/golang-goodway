# Exercise: 08. Packages, Modules, Visibility, and go.mod

## Goal

Convert reading into **retrievable skill**. The tests are the specification.

## Concepts from the lesson

- Create modules with go.mod
- Export identifiers with Capital letters
- Import packages and avoid import cycles
- Organize code into packages with a single purpose

## Task

Implement unexported squareHint used by exported Square; tests import from outside.

## Examples / expected behavior

mathx.Square(4)→16. External tests cannot call squareHint.

## How to work

1. Read this README, then re-open `lessons/08-packages-modules/lesson.md`.
2. Run the tests once to get a failure checklist.
3. Implement the smallest correct code; re-run after each function.
4. When stuck, re-type a lesson example into a scratch file and adapt it.
5. After green: explain each exported function in one sentence without looking.

## Done when

- Tests pass
- You can rewrite tomorrow without peeking at today's solution

**Do not open `solutions/08-packages-modules/` until after a real attempt (15+ minutes).**

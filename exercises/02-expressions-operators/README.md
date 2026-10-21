# Exercise: 02. Expressions, Operators, and Type Conversions

## Goal

Convert reading into **retrievable skill**. The tests are the specification.

## Concepts from the lesson

- Use arithmetic, comparison, and logical operators correctly
- Explain why Go forbids implicit numeric conversions
- Convert between types safely and consciously
- Avoid integer division surprises

## Task

Implement SafeDiv(a,b)→(float64,bool) false on /0, and Clamp(v,lo,hi).

## Examples / expected behavior

SafeDiv(7,2)→(3.5,true); SafeDiv(1,0)→(0,false). Clamp(99,0,10)→10.

## How to work

1. Read this README, then re-open `lessons/02-expressions-operators/lesson.md`.
2. Run the tests once to get a failure checklist.
3. Implement the smallest correct code; re-run after each function.
4. When stuck, re-type a lesson example into a scratch file and adapt it.
5. After green: explain each exported function in one sentence without looking.

## Done when

- Tests pass
- You can rewrite tomorrow without peeking at today's solution

**Do not open `solutions/02-expressions-operators/` until after a real attempt (15+ minutes).**

# Exercise: 05. Arrays, Slices, and Maps (Memory Intuition)

## Goal

Convert reading into **retrievable skill**. The tests are the specification.

## Concepts from the lesson

- Distinguish arrays (fixed) from slices (dynamic views)
- Explain slice header: pointer, length, capacity
- Grow slices with append and understand reallocation
- Use maps safely (including comma-ok idiom)

## Task

Implement Sum, Freq (word counts), and Unique (first-seen order).

## Examples / expected behavior

Sum([1,2,3])→6. Freq([a,b,a]) a=2. Unique([1,2,1,3,2])→[1,2,3].

## How to work

1. Read this README, then re-open `lessons/05-arrays-slices-maps/lesson.md`.
2. Run the tests once to get a failure checklist.
3. Implement the smallest correct code; re-run after each function.
4. When stuck, re-type a lesson example into a scratch file and adapt it.
5. After green: explain each exported function in one sentence without looking.

## Done when

- Tests pass
- You can rewrite tomorrow without peeking at today's solution

**Do not open `solutions/05-arrays-slices-maps/` until after a real attempt (15+ minutes).**

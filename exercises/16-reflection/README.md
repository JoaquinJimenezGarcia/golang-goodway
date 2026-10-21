# Exercise: 16. Reflection Overview (and When Not to Use It)

## Goal

Convert reading into **retrievable skill**. The tests are the specification.

## Concepts from the lesson

- Explain reflect.Type and reflect.Value at a high level
- Recognize frameworks that use reflection (encoding/json)
- Prefer codegen or generics over heavy reflection
- Measure cost before using reflection in hot paths

## Task

Use reflect.Kind (or the stub's required API) to classify values as tests demand.

## Examples / expected behavior

Classify ints vs structs correctly per test cases.

## How to work

1. Read this README, then re-open `lessons/16-reflection/lesson.md`.
2. Run the tests once to get a failure checklist.
3. Implement the smallest correct code; re-run after each function.
4. When stuck, re-type a lesson example into a scratch file and adapt it.
5. After green: explain each exported function in one sentence without looking.

## Done when

- Tests pass
- You can rewrite tomorrow without peeking at today's solution

**Do not open `solutions/16-reflection/` until after a real attempt (15+ minutes).**

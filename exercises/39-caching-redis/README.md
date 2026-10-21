# Exercise: 39. Caching, Redis Patterns, Idempotency

## Goal

Convert reading into **retrievable skill**. The tests are the specification.

## Concepts from the lesson

- Apply cache-aside pattern
- Choose TTLs and invalidation strategies
- Implement idempotency keys for writes
- Understand stampede risks

## Task

Implement cache-aside or idempotency stub per tests.

## Examples / expected behavior

Second read does not re-load; idempotent submit once.

## How to work

1. Read this README, then re-open `lessons/39-caching-redis/lesson.md`.
2. Run the tests once to get a failure checklist.
3. Implement the smallest correct code; re-run after each function.
4. When stuck, re-type a lesson example into a scratch file and adapt it.
5. After green: explain each exported function in one sentence without looking.

## Done when

- Tests pass
- You can rewrite tomorrow without peeking at today's solution

**Do not open `solutions/39-caching-redis/` until after a real attempt (15+ minutes).**

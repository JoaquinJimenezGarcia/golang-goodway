# Exercise: 36. REST API Design, Middleware, Auth Basics

## Goal

Convert reading into **retrievable skill**. The tests are the specification.

## Concepts from the lesson

- Design resource-oriented REST endpoints
- Implement middleware for logging/auth
- Use bearer tokens / basic auth patterns
- Return consistent error JSON

## Task

Implement middleware that enforces headers/auth as tests describe.

## Examples / expected behavior

Missing token → 401; valid → handler body.

## How to work

1. Read this README, then re-open `lessons/36-rest-middleware-auth/lesson.md`.
2. Run the tests once to get a failure checklist.
3. Implement the smallest correct code; re-run after each function.
4. When stuck, re-type a lesson example into a scratch file and adapt it.
5. After green: explain each exported function in one sentence without looking.

## Done when

- Tests pass
- You can rewrite tomorrow without peeking at today's solution

**Do not open `solutions/36-rest-middleware-auth/` until after a real attempt (15+ minutes).**

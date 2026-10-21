# Exercise: 35. HTTP Servers and Clients (net/http)

## Goal

Convert reading into **retrievable skill**. The tests are the specification.

## Concepts from the lesson

- Build handlers with net/http
- Use http.Client with timeouts
- Understand middleware chaining
- Serve JSON APIs safely

## Task

Implement a health handler (or client helper) so tests get 200/ok bodies.

## Examples / expected behavior

GET health returns status 200 and body matching tests.

## How to work

1. Read this README, then re-open `lessons/35-http-net/lesson.md`.
2. Run the tests once to get a failure checklist.
3. Implement the smallest correct code; re-run after each function.
4. When stuck, re-type a lesson example into a scratch file and adapt it.
5. After green: explain each exported function in one sentence without looking.

## Done when

- Tests pass
- You can rewrite tomorrow without peeking at today's solution

**Do not open `solutions/35-http-net/` until after a real attempt (15+ minutes).**

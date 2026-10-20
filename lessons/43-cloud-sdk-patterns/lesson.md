---
title: "43. Cloud SDK Patterns: Config, Retries, Pagination"
---

# 43. Cloud SDK Patterns: Config, Retries, Pagination

**Phase:** Phase 6 — Systems and infrastructure  
**Estimated time:** 1–2 days  
**Slug:** `43-cloud-sdk-patterns`

## Learning objectives

- Configure clients via env/role credentials
- Retry with exponential backoff + jitter
- Paginate list APIs correctly
- Treat cloud APIs as unreliable networks

## Prerequisites

Complete prior numbered lessons. Type every example yourself.

## Retries

Retry transient errors (timeouts, 429, 503), not validation errors.
Exponential backoff with jitter prevents synchronized stampedes.

```go
func Retry(ctx context.Context, fn func() error) error {
    // backoff loop checking ctx.Done()
}
```

## Pagination

Most list APIs return a cursor/token. Loop until empty. Bound max pages.

## Config

Prefer IAM roles / workload identity over long-lived keys in files.
Separate config loading from business logic for tests.

## Common mistakes (especially from Python instincts)

- Infinite retries without deadline
- Retrying non-idempotent POSTs blindly
- Loading all pages into memory without need

## Exercises

Work in `exercises/43-cloud-sdk-patterns/`. Read that folder's `README.md`.

- **A (Drill):** make unit tests pass with the simplest correct code.
- **B (Apply):** extend with an edge case called out in the exercise README.
- **C (Challenge):** rewrite your solution from memory the next day without looking.

**Do not open `solutions/43-cloud-sdk-patterns/` until you have an honest failing attempt.**

## Self-check

1. What is jitter?
2. Which errors retry?
3. Why cursor pagination?

## Further reading

- https://aws.github.io/aws-sdk-go-v2/docs/

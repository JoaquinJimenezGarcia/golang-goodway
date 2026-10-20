---
title: "47. Calling Model APIs: HTTP and SSE Streaming"
---

# 47. Calling Model APIs: HTTP and SSE Streaming

**Phase:** Phase 7 — AI engineering in Go  
**Estimated time:** 2 days  
**Slug:** `47-model-apis`

## Learning objectives

- Call LLM HTTP APIs with timeouts
- Parse streaming SSE responses
- Handle rate limits and retries
- Bound concurrency to model backends

## Prerequisites

Complete prior numbered lessons. Type every example yourself.

## Request shape

Most model APIs are HTTPS JSON. Stream tokens via Server-Sent Events (SSE) or chunked HTTP.

```go
req, _ := http.NewRequestWithContext(ctx, http.MethodPost, url, body)
req.Header.Set("Authorization", "Bearer "+key)
req.Header.Set("Accept", "text/event-stream")
```

## SSE parsing

Read line-oriented `data: ...` frames until `[DONE]`. Respect ctx cancellation mid-stream.

## Production concerns

- Token/cost accounting
- Prompt injection awareness at boundaries
- Never log raw secrets or full prompts if sensitive

## Common mistakes (especially from Python instincts)

- No timeout on stream reads
- Buffering entire stream before forwarding
- Unbounded parallel calls to the model

## Exercises

Work in `exercises/47-model-apis/`. Read that folder's `README.md`.

- **A (Drill):** make unit tests pass with the simplest correct code.
- **B (Apply):** extend with an edge case called out in the exercise README.
- **C (Challenge):** rewrite your solution from memory the next day without looking.

**Do not open `solutions/47-model-apis/` until you have an honest failing attempt.**

## Self-check

1. What is SSE?
2. Why cancel mid-stream?
3. Which headers matter?

## Further reading

- https://platform.openai.com/docs/api-reference

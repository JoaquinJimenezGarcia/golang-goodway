# Exercise: 50. Inference Serving: Batching, Queues, Sidecars

## Goal

Convert reading into **retrievable skill**. The tests are the specification.

## Concepts from the lesson

- Queue inference requests
- Dynamic batch for GPU efficiency
- Use sidecar patterns for model runtimes
- Expose SLOs for latency vs throughput

## Task

Implement queue/batch helpers for inference stubs.

## Examples / expected behavior

Batch max size respected; remainder stays queued.

## How to work

1. Read this README, then re-open `lessons/50-inference-serving/lesson.md`.
2. Run the tests once to get a failure checklist.
3. Implement the smallest correct code; re-run after each function.
4. When stuck, re-type a lesson example into a scratch file and adapt it.
5. After green: explain each exported function in one sentence without looking.

## Done when

- Tests pass
- You can rewrite tomorrow without peeking at today's solution

**Do not open `solutions/50-inference-serving/` until after a real attempt (15+ minutes).**

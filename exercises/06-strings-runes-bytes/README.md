# Exercise: 06. Strings, Runes, Bytes, and UTF-8

## Goal

Convert reading into **retrievable skill**. The tests are the specification.

## Concepts from the lesson

- Explain that Go strings are immutable byte sequences (often UTF-8)
- Iterate by rune vs by byte correctly
- Convert between string, []byte, and []rune consciously
- Avoid indexing strings when Unicode matters

## Task

Implement RuneCount and ReverseRunes that respect Unicode code points.

## Examples / expected behavior

RuneCount("Go👍")→3. ReverseRunes("ab👍")→"👍ba".

## How to work

1. Read this README, then re-open `lessons/06-strings-runes-bytes/lesson.md`.
2. Run the tests once to get a failure checklist.
3. Implement the smallest correct code; re-run after each function.
4. When stuck, re-type a lesson example into a scratch file and adapt it.
5. After green: explain each exported function in one sentence without looking.

## Done when

- Tests pass
- You can rewrite tomorrow without peeking at today's solution

**Do not open `solutions/06-strings-runes-bytes/` until after a real attempt (15+ minutes).**

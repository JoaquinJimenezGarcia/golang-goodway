#!/usr/bin/env bash
# Overlay solutions onto exercises in a temp dir and run go test for each module.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
ok=0
fail=0
for ex in "$ROOT"/exercises/*; do
  [[ -d "$ex" ]] || continue
  slug="$(basename "$ex")"
  sol="$ROOT/solutions/$slug"
  td="$(mktemp -d)"
  cp -R "$ex/." "$td/"
  if [[ -d "$sol" ]]; then
    while IFS= read -r -d '' f; do
      rel="${f#"$sol"/}"
      mkdir -p "$td/$(dirname "$rel")"
      cp "$f" "$td/$rel"
    done < <(find "$sol" -name '*.go' -print0)
  fi
  if (cd "$td" && go test ./... >/dev/null 2>&1); then
    echo "OK  $slug"
    ok=$((ok+1))
  else
    echo "FAIL $slug"
    (cd "$td" && go test ./... ) || true
    fail=$((fail+1))
  fi
  rm -rf "$td"
done
echo "Passed $ok; failed $fail"
[[ "$fail" -eq 0 ]]

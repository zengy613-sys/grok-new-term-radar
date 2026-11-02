#!/usr/bin/env bash
# Local replacement for .github/workflows/radar.yml (no Actions cache/artifact/summary).
# Usage: ./run_local.sh [extra args for `python -m radar daily`, e.g. --skip x]
# Output: /workspace/radar-reports/YYYY-MM-DD.md (+ .json), latest.md symlink.
set -euo pipefail
REPO="$(cd "$(dirname "$0")" && pwd)"
OUT_DIR="${RADAR_OUT_DIR:-/workspace/radar-reports}"
DAY="$(TZ=Asia/Shanghai date +%F)"
mkdir -p "$OUT_DIR" "$REPO/state"
cd "$REPO"

# Pull latest code (state/, report.* are gitignored, so this is safe). Non-fatal.
git pull --ff-only -q 2>/dev/null || echo "[run_local] git pull skipped/failed, using local code" >&2

# Optional GitHub token for higher API rate limit (same role as Actions' GITHUB_TOKEN).
# Never printed or written to disk.
if [ -z "${GITHUB_TOKEN:-}${GH_TOKEN:-}" ] && command -v gh >/dev/null; then
  GITHUB_TOKEN="$(gh auth token 2>/dev/null || true)"; export GITHUB_TOKEN
fi

PY="${PYTHON:-python3}"
start=$(date +%s)
"$PY" -m radar daily --state state --out "$OUT_DIR/$DAY.md" "$@" 2>"$OUT_DIR/$DAY.log" || {
  rc=$?; echo "[run_local] radar failed (exit $rc), see $OUT_DIR/$DAY.log" >&2; tail -20 "$OUT_DIR/$DAY.log" >&2; exit $rc; }
[ -s "$OUT_DIR/$DAY.md" ] || { echo "[run_local] no report produced" >&2; exit 2; }
ln -sf "$DAY.md" "$OUT_DIR/latest.md"
echo "[run_local] ok in $(( $(date +%s) - start ))s -> $OUT_DIR/$DAY.md"

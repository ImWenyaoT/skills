#!/bin/sh
set -eu

if [ "$#" -lt 1 ]; then
  echo "usage: run-python.sh SCRIPT [ARGS...]" >&2
  exit 2
fi

script=$1
shift

if command -v uv >/dev/null 2>&1; then
  : "${UV_CACHE_DIR:=${TMPDIR:-/tmp}/grill-resume-uv-cache}"
  export UV_CACHE_DIR
  exec uv run "$script" "$@"
fi

if command -v python3 >/dev/null 2>&1; then
  exec python3 "$script" "$@"
fi

if command -v python >/dev/null 2>&1; then
  exec python "$script" "$@"
fi

if command -v conda >/dev/null 2>&1; then
  exec conda run -n base python "$script" "$@"
fi

echo "missing Python runtime: tried uv, python3, python, and conda base" >&2
exit 127

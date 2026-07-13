#!/usr/bin/env bash
set -euo pipefail

python3 scripts/validate_skills.py
python3 scripts/evaluate_skill_triggers.py
python3 -W error::ResourceWarning -m unittest discover -s tests -v
python3 -m unittest discover -s skills/drawing-figures/tests -p 'test_*.py' -v
python3 -m unittest discover -s skills/elsevier-articles/tests -p 'test_*.py' -v
python3 -m unittest discover -s skills/elsevier-submissions/tests -p 'test_*.py' -v

while IFS= read -r file; do
  python3 -m py_compile "$file"
done < <(find . \( -path ./.git -o -path ./.cache \) -prune -o -name '*.py' -print)

bash -n scripts/ci.sh scripts/sync-to-local.sh
git diff --check

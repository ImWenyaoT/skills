#!/usr/bin/env bash
set -euo pipefail

python3 scripts/validate_skills.py
python3 scripts/evaluate_skill_triggers.py
python3 skills/offer-magic/scripts/validate-bundle.py
python3 skills/offer-magic/grill-resume/scripts/test-prepare-review-packet.py
python3 skills/offer-magic/grill-resume/scripts/test-validate-review-report.py
python3 -W error::ResourceWarning -m unittest discover -s tests -v

# Every skill that ships tests gets them run. Listing the directories by hand
# meant a new skill's tests stayed silently unexecuted until someone noticed.
for suite in skills/*/tests; do
  [ -d "$suite" ] || continue
  echo "== $suite"
  python3 -m unittest discover -s "$suite" -p 'test_*.py' -v
done

while IFS= read -r file; do
  python3 -m py_compile "$file"
done < <(find . \( -path ./.git -o -path ./.cache \) -prune -o -name '*.py' -print)

bash -n scripts/ci.sh scripts/sync-to-local.sh
git diff --check

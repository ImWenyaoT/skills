#!/usr/bin/env bash
set -euo pipefail

python3 -m coverage erase
python3 -m coverage run \
  --branch \
  --source=scripts \
  -m unittest discover -s tests
python3 -m coverage report --show-missing --fail-under=70
python3 -m coverage xml -o coverage.xml

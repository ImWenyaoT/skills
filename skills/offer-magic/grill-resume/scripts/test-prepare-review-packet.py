#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path


SCRIPT = Path(__file__).with_name("prepare-review-packet.py")


def main() -> None:
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        html = root / "resume.html"
        html.write_text("<html><body><h1>Candidate</h1><p>Verified work.</p></body></html>", encoding="utf-8")
        profile = root / "candidate-profile.json"
        profile.write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "visibility": "main_only",
                    "slots": {
                        "recognition": {},
                        "character": {},
                        "trajectory": {},
                    },
                }
            ),
            encoding="utf-8",
        )
        rejected = subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "--html",
                str(html),
                "--constraints",
                str(profile),
                "--out",
                str(root / "rejected"),
            ],
            text=True,
            capture_output=True,
        )
        assert rejected.returncode != 0
        assert "main-only" in rejected.stderr

        constraints = root / "constraints.txt"
        constraints.write_text("First internship.\n", encoding="utf-8")
        accepted_out = root / "accepted"
        accepted = subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "--html",
                str(html),
                "--constraints",
                str(constraints),
                "--out",
                str(accepted_out),
            ],
            text=True,
            capture_output=True,
        )
        assert accepted.returncode == 0, accepted.stderr
        assert not any(path.name == "candidate-profile.json" for path in accepted_out.rglob("*"))

    print("prepare-review-packet privacy tests passed: 2")


if __name__ == "__main__":
    main()

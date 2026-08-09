"""Minimal, stable smoke tests for the figure-script CLIs."""

from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
FIXTURES = Path(__file__).resolve().parent / "fixtures"


class FigureScriptSmokeTests(unittest.TestCase):
    """Drive the stitch and annotate CLIs from small fixtures and check the artifacts."""

    def test_stitch_cli_writes_expected_canvas(self) -> None:
        """The stitch CLI normalises panel heights and keeps the white gap."""
        with tempfile.TemporaryDirectory() as tmp:
            work = Path(tmp)
            first = work / "first.png"
            second = work / "second.png"
            output = work / "stitched.png"
            Image.new("RGB", (12, 10), "red").save(first)
            Image.new("RGB", (10, 20), "blue").save(second)

            subprocess.run(
                [
                    sys.executable,
                    str(SCRIPTS / "stitch.py"),
                    "--images",
                    str(first),
                    str(second),
                    "--out",
                    str(output),
                    "--gap",
                    "3",
                ],
                check=True,
                capture_output=True,
                text=True,
            )

            with Image.open(output) as stitched:
                self.assertEqual(stitched.size, (20, 10))
                self.assertEqual(stitched.getpixel((13, 5)), (255, 255, 255))

    def test_annotate_cli_writes_qa_artifact(self) -> None:
        """The annotate CLI writes a non-empty PNG for each render the JSON fixture names."""
        with tempfile.TemporaryDirectory() as tmp:
            work = Path(tmp)
            renders = work / "renders"
            output = work / "annotated"
            renders.mkdir()
            Image.new("RGB", (40, 30), "white").save(renders / "panel.png")

            subprocess.run(
                [
                    sys.executable,
                    str(SCRIPTS / "annotate_renders.py"),
                    "--config",
                    str(FIXTURES / "annotation_spec.json"),
                    "--renders",
                    str(renders),
                    "--out",
                    str(output),
                ],
                check=True,
                capture_output=True,
                text=True,
            )

            artifact = output / "panel_spec.png"
            self.assertTrue(artifact.is_file())
            with Image.open(artifact) as annotated:
                self.assertEqual(annotated.format, "PNG")
                self.assertGreater(annotated.width, 40)
                self.assertGreater(annotated.height, 30)


if __name__ == "__main__":
    unittest.main()

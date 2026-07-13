from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


MODULE_PATH = (
    Path(__file__).resolve().parents[1]
    / "skills"
    / "mining-sessions"
    / "scripts"
    / "scan_sessions.py"
)
SPEC = importlib.util.spec_from_file_location("scan_sessions", MODULE_PATH)
assert SPEC and SPEC.loader
scanner = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(scanner)


class ScanSessionsTests(unittest.TestCase):
    def test_first_user_ask_strips_runtime_injection_but_keeps_the_ask(self) -> None:
        lines = [
            {
                "payload": {
                    "role": "user",
                    "content": (
                        "<recommended_plugins>generated list</recommended_plugins>"
                        "# AGENTS.md instructions for /repo\n"
                        "<environment_context>generated context</environment_context>\n"
                        "Please persist conversation history across UI switches."
                    ),
                }
            }
        ]

        self.assertEqual(
            scanner.first_user_ask(lines),
            "Please persist conversation history across UI switches.",
        )

    def test_first_user_ask_skips_a_pure_injected_message(self) -> None:
        lines = [
            {
                "payload": {
                    "role": "user",
                    "content": (
                        "<recommended_plugins>generated list</recommended_plugins>"
                    ),
                }
            },
            {"payload": {"role": "user", "content": "Run the real task."}},
        ]

        self.assertEqual(scanner.first_user_ask(lines), "Run the real task.")

    def test_first_user_ask_preserves_runtime_tags_inside_real_content(self) -> None:
        lines = [
            {
                "payload": {
                    "role": "user",
                    "content": (
                        "Explain <environment_context>foo</environment_context> markup."
                    ),
                }
            }
        ]

        self.assertEqual(
            scanner.first_user_ask(lines),
            "Explain <environment_context>foo</environment_context> markup.",
        )

    def test_first_user_ask_handles_agents_preamble_without_environment(self) -> None:
        lines = [
            {
                "payload": {
                    "role": "user",
                    "content": (
                        "# AGENTS.md instructions for /repo\n"
                        "<INSTRUCTIONS>Use concise replies.</INSTRUCTIONS>\n"
                        "Do the actual task."
                    ),
                }
            }
        ]

        self.assertEqual(scanner.first_user_ask(lines), "Do the actual task.")

    def test_first_user_ask_reads_segmented_input_after_injection(self) -> None:
        lines = [
            {
                "payload": {
                    "role": "user",
                    "content": [
                        {
                            "type": "input_text",
                            "text": "<recommended_plugins>x</recommended_plugins>",
                        },
                        {"type": "text", "text": "Run the segmented task."},
                    ],
                }
            }
        ]

        self.assertEqual(scanner.first_user_ask(lines), "Run the segmented task.")


if __name__ == "__main__":
    unittest.main()

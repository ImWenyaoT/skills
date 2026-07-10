"""CARE-Track 结构化取色表的回归测试。"""

import re
import sys
import unittest
from pathlib import Path


SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

from figkit.caretrack_palette import (  # noqa: E402
    CARETRACK_COLORPICK,
    family_colors,
    top_color,
)


class CaretrackPaletteTests(unittest.TestCase):
    """保证图片中的色族、数量与主要代表色不会在重构时丢失。"""

    def test_complete_sheet_shape(self) -> None:
        """完整取色表应包含 10 个色族和 73 个离散色。"""
        self.assertEqual(len(CARETRACK_COLORPICK), 10)
        self.assertEqual(sum(map(len, CARETRACK_COLORPICK.values())), 73)

    def test_source_order_keeps_dominant_swatches_first(self) -> None:
        """各色族顺序应保留原表的像素权重排序。"""
        self.assertEqual(top_color("blue"), "#4C80EC")
        self.assertEqual(top_color("green/teal"), "#0EBA5F")
        self.assertEqual(top_color("red"), "#F17060")
        self.assertEqual(family_colors("white/near-white")[-1], "#ECF0F1")

    def test_colors_are_unique_valid_hex_and_weight_sorted(self) -> None:
        """所有颜色应唯一、格式有效，并在各色族内按权重降序排列。"""
        all_colors = []
        for entries in CARETRACK_COLORPICK.values():
            colors = [color for color, _weight in entries]
            weights = [weight for _color, weight in entries]
            self.assertTrue(all(re.fullmatch(r"#[0-9A-F]{6}", color) for color in colors))
            self.assertEqual(weights, sorted(weights, reverse=True))
            all_colors.extend(colors)
        self.assertEqual(len(all_colors), len(set(all_colors)))

    def test_unknown_family_is_actionable(self) -> None:
        """未知色族应返回包含可选项的明确错误。"""
        with self.assertRaisesRegex(ValueError, "choose: blue"):
            family_colors("purple")


if __name__ == "__main__":
    unittest.main()

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import sys

SCRIPT_DIR = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))

from validate_visual_plan import load_and_validate
from render_visual_plan import build_command


class VisualPlanKindTests(unittest.TestCase):
    def write_plan(self, root: Path, visuals: list[dict]) -> Path:
        source = root / "source.mp4"
        source.touch()
        for index in range(len(visuals)):
            (root / f"asset-{index}.mov").touch()
            visuals[index]["asset"] = str(root / f"asset-{index}.mov")
        path = root / "plan.json"
        path.write_text(
            json.dumps(
                {
                    "version": 1,
                    "source": str(source),
                    "output": str(root / "output.mp4"),
                    "duration": 30,
                    "source_subtitle_mode": "burned",
                    "visuals": visuals,
                }
            ),
            encoding="utf-8",
        )
        return path

    @patch("validate_visual_plan.probe_duration", return_value=30.0)
    def test_separates_broll_and_motion_graphic_durations(self, _probe):
        with tempfile.TemporaryDirectory() as directory:
            plan_path = self.write_plan(
                Path(directory),
                [
                    {"start": 1, "end": 4, "kind": "broll", "role": "场景"},
                    {
                        "start": 6,
                        "end": 11,
                        "kind": "motion_graphic",
                        "role": "流程",
                    },
                ],
            )
            plan, errors, _warnings = load_and_validate(plan_path)
            self.assertEqual(errors, [])
            self.assertEqual(plan["_summary"]["broll_duration"], 3)
            self.assertEqual(plan["_summary"]["motion_graphic_duration"], 5)
            self.assertAlmostEqual(plan["_summary"]["visual_ratio"], 8 / 30)

    @patch("validate_visual_plan.probe_duration", return_value=30.0)
    def test_rejects_unknown_visual_kind(self, _probe):
        with tempfile.TemporaryDirectory() as directory:
            plan_path = self.write_plan(
                Path(directory),
                [{"start": 1, "end": 4, "kind": "transition", "role": "错误分类"}],
            )
            _plan, errors, _warnings = load_and_validate(plan_path)
            self.assertTrue(any("kind 必须是" in error for error in errors))

    def test_renderer_keeps_card_and_overlay_layouts_distinct(self):
        plan = {
            "source": "/tmp/source.mp4",
            "output": "/tmp/output.mp4",
            "duration": 30,
            "width": 1080,
            "height": 1920,
            "fps": 30,
            "visuals": [
                {
                    "start": 1,
                    "end": 4,
                    "kind": "broll",
                    "layout": "card",
                    "asset": "/tmp/card.mp4",
                    "transition": 0.3,
                },
                {
                    "start": 6,
                    "end": 10,
                    "kind": "motion_graphic",
                    "layout": "overlay",
                    "asset": "/tmp/overlay.mov",
                    "transition": 0.3,
                },
            ],
        }
        command = build_command(plan, burn_subtitle=False)
        filters = command[command.index("-filter_complex") + 1]
        self.assertIn("pad=960:1280:6:6:color=white@0.45", filters)
        self.assertIn("overlay=60:100", filters)
        self.assertIn("pad=1080:1920:(ow-iw)/2:(oh-ih)/2:color=black@0", filters)
        self.assertIn("overlay=0:0", filters)


if __name__ == "__main__":
    unittest.main()

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import sys

SCRIPT_DIR = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))

from render_content_plan import build_command, load_and_validate


class ContentPlanTests(unittest.TestCase):
    def write_plan(self, root: Path, cuts: list[dict]) -> Path:
        source = root / "source.mp4"
        source.touch()
        path = root / "content_plan.json"
        path.write_text(
            json.dumps(
                {
                    "version": 1,
                    "source": str(source),
                    "output": str(root / "content_cut.mp4"),
                    "fps": 30,
                    "join_transition": 0.04,
                    "cuts": cuts,
                }
            ),
            encoding="utf-8",
        )
        return path

    @patch("render_content_plan.probe_duration", return_value=30.0)
    def test_builds_kept_ranges_and_output_duration(self, _probe):
        with tempfile.TemporaryDirectory() as directory:
            plan_path = self.write_plan(
                Path(directory),
                [
                    {"start": 10.36, "end": 11.10, "transcript": "啊", "reason": "口癖"},
                    {"start": 18.36, "end": 18.62, "transcript": "呀", "reason": "列举助词"},
                ],
            )
            plan, errors, warnings = load_and_validate(plan_path)
            self.assertEqual(errors, [])
            self.assertEqual(warnings, [])
            self.assertEqual(len(plan["_summary"]["kept_ranges"]), 3)
            self.assertAlmostEqual(plan["_summary"]["removed_duration"], 1.0)
            self.assertAlmostEqual(plan["_summary"]["output_duration"], 28.92)

    @patch("render_content_plan.probe_duration", return_value=30.0)
    def test_rejects_overlapping_cuts(self, _probe):
        with tempfile.TemporaryDirectory() as directory:
            plan_path = self.write_plan(
                Path(directory),
                [
                    {"start": 10.0, "end": 11.0, "transcript": "啊", "reason": "口癖"},
                    {"start": 10.5, "end": 11.5, "transcript": "呀", "reason": "口癖"},
                ],
            )
            _plan, errors, _warnings = load_and_validate(plan_path)
            self.assertTrue(any("重叠" in error for error in errors))

    @patch("render_content_plan.probe_duration", return_value=30.0)
    def test_command_crossfades_video_and_audio_at_same_duration(self, _probe):
        with tempfile.TemporaryDirectory() as directory:
            plan_path = self.write_plan(
                Path(directory),
                [{"start": 10.36, "end": 11.10, "transcript": "啊", "reason": "口癖"}],
            )
            plan, errors, _warnings = load_and_validate(plan_path)
            self.assertEqual(errors, [])
            command = build_command(plan)
            filters = command[command.index("-filter_complex") + 1]
            self.assertIn("xfade=transition=fade:duration=0.040", filters)
            self.assertIn("acrossfade=d=0.040", filters)

    @patch("render_content_plan.probe_duration", return_value=30.0)
    def test_zero_transition_uses_synced_concat(self, _probe):
        with tempfile.TemporaryDirectory() as directory:
            plan_path = self.write_plan(
                Path(directory),
                [{"start": 10.0, "end": 11.0, "transcript": "静音", "reason": "压缩停顿"}],
            )
            payload = json.loads(plan_path.read_text(encoding="utf-8"))
            payload["join_transition"] = 0
            plan_path.write_text(json.dumps(payload), encoding="utf-8")
            plan, errors, _warnings = load_and_validate(plan_path)
            self.assertEqual(errors, [])
            command = build_command(plan)
            filters = command[command.index("-filter_complex") + 1]
            self.assertIn("concat=n=2:v=1:a=1[vconcat][aconcat]", filters)
            self.assertNotIn("xfade=", filters)
            self.assertNotIn("acrossfade=", filters)


if __name__ == "__main__":
    unittest.main()

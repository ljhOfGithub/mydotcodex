from __future__ import annotations

import importlib.util
import io
import os
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch


MODULE_PATH = Path(__file__).with_name("bug-triage.py")
SPEC = importlib.util.spec_from_file_location("bug_triage", MODULE_PATH)
assert SPEC and SPEC.loader
bug_triage = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = bug_triage
SPEC.loader.exec_module(bug_triage)


class EnvironmentLoadingTests(unittest.TestCase):
    def test_explicit_file_loads_allowlisted_keys_and_environment_wins(self) -> None:
        with tempfile.TemporaryDirectory() as tmp, patch.dict(os.environ, {}, clear=True):
            env_file = Path(tmp) / "bug.env"
            env_file.write_text(
                "BUG_LRS_ENDPOINT=https://lrs.example.test\n"
                "BUG_LRS_USERNAME=file-user\n"
                "BUG_LRS_PASSWORD='file-pass'\n"
                "UNRELATED_SECRET=must-not-load\n",
                encoding="utf-8",
            )
            os.environ["BUG_LRS_ENV_FILE"] = str(env_file)
            os.environ["BUG_LRS_USERNAME"] = "process-user"

            result = bug_triage.load_config_environment()
            config = bug_triage.Config()

            self.assertEqual(result.source, env_file.resolve())
            self.assertEqual(config.bug_lrs_username, "process-user")
            self.assertEqual(config.bug_lrs_password, "file-pass")
            self.assertNotIn("UNRELATED_SECRET", os.environ)
            self.assertTrue(config.bug_lrs_configured)

    def test_discovers_nearest_secrets_file_up_to_git_root(self) -> None:
        with tempfile.TemporaryDirectory() as tmp, patch.dict(os.environ, {}, clear=True):
            repo = Path(tmp) / "repo"
            nested = repo / "code" / "app"
            nested.mkdir(parents=True)
            (repo / ".git").mkdir()
            secret_file = repo / ".secrets.env"
            secret_file.write_text(
                "BUG_LRS_ENDPOINT=https://lrs.example.test\n"
                "BUG_LRS_USERNAME=user\n"
                "BUG_LRS_PASSWORD=pass # trailing comment\n",
                encoding="utf-8",
            )

            result = bug_triage.load_config_environment(nested)

            self.assertEqual(result.source, secret_file.resolve())
            self.assertEqual(os.environ["BUG_LRS_PASSWORD"], "pass")

    def test_missing_explicit_file_is_an_error(self) -> None:
        with tempfile.TemporaryDirectory() as tmp, patch.dict(os.environ, {}, clear=True):
            os.environ["BUG_LRS_ENV_FILE"] = str(Path(tmp) / "missing.env")
            with self.assertRaisesRegex(RuntimeError, "does not exist"):
                bug_triage.load_config_environment()

    def test_values_are_not_shell_expanded_or_executed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp, patch.dict(os.environ, {}, clear=True):
            marker = Path(tmp) / "must-not-exist"
            env_file = Path(tmp) / "bug.env"
            literal = f"$(touch {marker})"
            env_file.write_text(f"BUG_LRS_PASSWORD={literal}\n", encoding="utf-8")
            os.environ["BUG_LRS_ENV_FILE"] = str(env_file)

            bug_triage.load_config_environment()

            self.assertEqual(os.environ["BUG_LRS_PASSWORD"], literal)
            self.assertFalse(marker.exists())

    def test_config_status_lists_missing_names_without_values(self) -> None:
        with patch.dict(os.environ, {"BUG_LRS_PASSWORD": "never-print-me"}, clear=True):
            config = bug_triage.Config()
            result = bug_triage.EnvironmentLoadResult(None, (Path("/tmp/.secrets.env"),), ())
            output = io.StringIO()

            with redirect_stdout(output):
                bug_triage.print_config_status(config, result)

            rendered = output.getvalue()
            self.assertIn("BUG_LRS_ENDPOINT", rendered)
            self.assertIn("BUG_LRS_USERNAME", rendered)
            self.assertIn("GCS_BUCKET_NAME", rendered)
            self.assertNotIn("never-print-me", rendered)

    def test_unconfigured_remote_fetch_routes_to_local_evidence_without_parameter_noise(self) -> None:
        with patch.dict(os.environ, {}, clear=True):
            config = bug_triage.Config()
            result = bug_triage.EnvironmentLoadResult(None, (), ())
            output = io.StringIO()

            with redirect_stdout(output):
                bug_triage.run_since(config, "24h", result)

            rendered = output.getvalue()
            self.assertIn("continue with the user report and fresh local evidence", rendered)
            self.assertNotIn("BUG_LRS_ENDPOINT", rendered)
            self.assertNotIn("BUG_LRS_USERNAME", rendered)
            self.assertNotIn("BUG_LRS_PASSWORD", rendered)
            self.assertNotIn("GCS_BUCKET_NAME", rendered)


if __name__ == "__main__":
    unittest.main()

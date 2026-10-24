from __future__ import annotations

import importlib.util
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "scripts" / "validate_voice_delivery.py"
SPEC = importlib.util.spec_from_file_location("validate_voice_delivery", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def _complete_payload(tmp_path: Path) -> dict:
    files = {}
    for key in ("reference_audio", "final_audio", "transcript_json", "subtitle_file"):
        path = tmp_path / f"{key}.dat"
        path.write_bytes(b"ok")
        files[key] = str(path)
    return {
        "delivery_scope": "complete_talking_head",
        "status": "final-verified",
        "voice_mode": "redub",
        "selected_candidate": "B_natural",
        "model": "local-test-model",
        "lip_sync": {"status": "checked"},
        "loudness_lufs": -15.0,
        "true_peak_dbtp": -1.6,
        **files,
    }


def test_complete_redub_passes(tmp_path: Path) -> None:
    assert MODULE.validate(_complete_payload(tmp_path)) == []


def test_original_voice_without_explicit_opt_out_fails(tmp_path: Path) -> None:
    payload = _complete_payload(tmp_path)
    payload["voice_mode"] = "original"
    assert any("explicit user opt-out" in error for error in MODULE.validate(payload))


def test_final_delivery_requires_lip_sync_check(tmp_path: Path) -> None:
    payload = _complete_payload(tmp_path)
    payload["lip_sync"] = {"status": "not_synced"}
    assert any("lip_sync.status" in error for error in MODULE.validate(payload))

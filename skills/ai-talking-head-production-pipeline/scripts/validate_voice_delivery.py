from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


FINAL_STATUS = "final-verified"
VALID_LIP_SYNC = {"checked", "covered"}


def _require_file(payload: dict[str, Any], key: str, errors: list[str]) -> None:
    value = payload.get(key)
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{key} must be a non-empty absolute file path")
        return
    path = Path(value)
    if not path.is_absolute():
        errors.append(f"{key} must be absolute: {value}")
    elif not path.is_file():
        errors.append(f"{key} does not exist: {value}")


def validate(payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if payload.get("delivery_scope") != "complete_talking_head":
        errors.append("delivery_scope must be complete_talking_head")

    voice_mode = payload.get("voice_mode")
    if voice_mode != "redub":
        opt_out = payload.get("original_voice_opt_out")
        if not (
            voice_mode == "original"
            and isinstance(opt_out, dict)
            and opt_out.get("explicit_user_request") is True
            and isinstance(opt_out.get("reason"), str)
            and opt_out["reason"].strip()
        ):
            errors.append(
                "complete talking-head delivery must use redub unless an explicit user opt-out is recorded"
            )

    if voice_mode == "redub":
        if payload.get("selected_candidate") != "B_natural":
            errors.append("selected_candidate must be B_natural for this workspace default")
        for key in ("reference_audio", "final_audio", "transcript_json", "subtitle_file"):
            _require_file(payload, key, errors)
        if not isinstance(payload.get("model"), str) or not payload["model"].strip():
            errors.append("model must be recorded for redub delivery")

    lip_sync = payload.get("lip_sync")
    lip_status = lip_sync.get("status") if isinstance(lip_sync, dict) else None
    if payload.get("status") == FINAL_STATUS and lip_status not in VALID_LIP_SYNC:
        errors.append("final-verified delivery requires lip_sync.status checked or covered")

    for key in ("loudness_lufs", "true_peak_dbtp"):
        if not isinstance(payload.get(key), (int, float)):
            errors.append(f"{key} must be numeric")
    return errors


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate the voice-redub delivery gate.")
    parser.add_argument("manifest", type=Path)
    args = parser.parse_args()
    payload = json.loads(args.manifest.read_text(encoding="utf-8"))
    errors = validate(payload)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        raise SystemExit(1)
    print("voice delivery gate: passed")


if __name__ == "__main__":
    main()

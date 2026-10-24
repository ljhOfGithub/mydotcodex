#!/usr/bin/env python3
"""校验 AI 口播视频的可审查镜头计划。"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any


IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}
VIDEO_EXTENSIONS = {".mp4", ".mov", ".m4v", ".webm"}
VISUAL_KINDS = {"broll", "motion_graphic"}


def probe_duration(path: Path) -> float:
    result = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(path),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    return float(result.stdout.strip())


def load_and_validate(plan_path: Path) -> tuple[dict[str, Any], list[str], list[str]]:
    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    errors: list[str] = []
    warnings: list[str] = []

    if plan.get("version") != 1:
        errors.append("version 必须为 1")

    source_value = plan.get("source")
    output_value = plan.get("output")
    source = Path(source_value) if isinstance(source_value, str) else None
    output = Path(output_value) if isinstance(output_value, str) else None

    if source is None or not source.is_absolute() or not source.is_file():
        errors.append("source 必须是存在的绝对文件路径")
    if output is None or not output.is_absolute():
        errors.append("output 必须是绝对文件路径")
    elif source is not None and output.resolve() == source.resolve():
        errors.append("output 不能覆盖 source")

    source_duration = None
    if source is not None and source.is_file():
        try:
            source_duration = probe_duration(source)
        except (subprocess.CalledProcessError, ValueError) as exc:
            errors.append(f"无法读取 source 时长：{exc}")

    duration = plan.get("duration", source_duration)
    if not isinstance(duration, (int, float)) or duration <= 0:
        errors.append("duration 必须是正数")
        duration = 0.0
    elif source_duration is not None and duration > source_duration + 0.1:
        errors.append(f"duration {duration:.3f}s 超过源片 {source_duration:.3f}s")

    visuals = plan.get("visuals")
    if not isinstance(visuals, list):
        errors.append("visuals 必须是数组")
        visuals = []

    normalized: list[tuple[float, float, int, str]] = []
    broll_duration = 0.0
    motion_graphic_duration = 0.0
    for index, shot in enumerate(visuals, start=1):
        if not isinstance(shot, dict):
            errors.append(f"镜头 {index} 必须是对象")
            continue
        start = shot.get("start")
        end = shot.get("end")
        asset_value = shot.get("asset")
        transition = shot.get("transition", 0.3)
        kind = shot.get("kind", "broll")
        if "kind" not in shot:
            warnings.append(f"镜头 {index} 未填写 kind，按 broll 兼容处理")
        if kind not in VISUAL_KINDS:
            errors.append(
                f"镜头 {index} 的 kind 必须是 broll 或 motion_graphic：{kind}"
            )
            kind = "broll"
        if not isinstance(start, (int, float)) or not isinstance(end, (int, float)):
            errors.append(f"镜头 {index} 的 start/end 必须是数字")
            continue
        if start < 0 or end <= start or end > duration + 0.001:
            errors.append(f"镜头 {index} 时间范围无效：{start}–{end}s")
            continue
        shot_duration = float(end - start)
        if not isinstance(transition, (int, float)) or transition < 0 or transition * 2 >= shot_duration:
            errors.append(f"镜头 {index} 的 transition 必须小于镜头时长一半")
        asset = Path(asset_value) if isinstance(asset_value, str) else None
        if asset is None or not asset.is_absolute() or not asset.is_file():
            errors.append(f"镜头 {index} 的 asset 必须是存在的绝对文件路径")
        elif asset.suffix.lower() not in IMAGE_EXTENSIONS | VIDEO_EXTENSIONS:
            errors.append(f"镜头 {index} 不支持素材格式：{asset.suffix}")
        if not str(shot.get("role", "")).strip():
            warnings.append(f"镜头 {index} 没有填写 role，难以审查画面职责")
        normalized.append((float(start), float(end), index, kind))
        if kind == "motion_graphic":
            motion_graphic_duration += shot_duration
        else:
            broll_duration += shot_duration

    normalized.sort()
    min_speaker_gap = float(plan.get("min_speaker_gap", 1.0))
    for previous, current in zip(normalized, normalized[1:]):
        if current[0] < previous[1]:
            errors.append(f"镜头 {previous[2]} 与镜头 {current[2]} 时间重叠")
        elif current[0] - previous[1] < min_speaker_gap:
            warnings.append(
                f"镜头 {previous[2]} 与镜头 {current[2]} 之间真人回场仅 "
                f"{current[0] - previous[1]:.2f}s"
            )

    if duration:
        ratio = broll_duration / float(duration)
        motion_graphic_ratio = motion_graphic_duration / float(duration)
        visual_duration = broll_duration + motion_graphic_duration
        visual_ratio = visual_duration / float(duration)
        max_ratio = float(plan.get("max_broll_ratio", 0.35))
        if ratio > max_ratio:
            warnings.append(f"B-roll 占比 {ratio:.1%}，高于计划上限 {max_ratio:.1%}")
        plan["_summary"] = {
            "duration": float(duration),
            "broll_duration": broll_duration,
            "broll_ratio": ratio,
            "motion_graphic_duration": motion_graphic_duration,
            "motion_graphic_ratio": motion_graphic_ratio,
            "visual_duration": visual_duration,
            "visual_ratio": visual_ratio,
        }

    subtitle_value = plan.get("subtitle")
    subtitle_mode = plan.get("source_subtitle_mode", "unknown")
    if subtitle_mode not in {"burned", "soft", "none", "unknown"}:
        errors.append("source_subtitle_mode 必须是 burned、soft、none 或 unknown")
    if subtitle_mode == "unknown":
        warnings.append("source_subtitle_mode 未确认，合成前应抽帧检查字幕")
    if subtitle_mode == "burned" and subtitle_value:
        errors.append("源片已烧录字幕，不能再次传入 subtitle")
    if subtitle_value:
        subtitle = Path(subtitle_value)
        if not subtitle.is_absolute() or not subtitle.is_file():
            errors.append("subtitle 必须是存在的绝对文件路径")

    return plan, errors, warnings


def main() -> int:
    if len(sys.argv) != 2:
        print("用法：validate_visual_plan.py /absolute/path/to/visual_plan.json", file=sys.stderr)
        return 2
    plan_path = Path(sys.argv[1])
    if not plan_path.is_absolute() or not plan_path.is_file():
        print("错误：计划文件必须是存在的绝对路径", file=sys.stderr)
        return 2
    try:
        plan, errors, warnings = load_and_validate(plan_path)
    except (json.JSONDecodeError, OSError) as exc:
        print(f"错误：无法读取计划：{exc}", file=sys.stderr)
        return 2

    for warning in warnings:
        print(f"警告：{warning}")
    for error in errors:
        print(f"错误：{error}", file=sys.stderr)
    if errors:
        return 1

    summary = plan.get("_summary", {})
    print(
        "计划通过："
        f"{len(plan.get('visuals', []))} 个镜头，"
        f"B-roll {summary.get('broll_duration', 0):.2f}s / "
        f"{summary.get('duration', 0):.2f}s（{summary.get('broll_ratio', 0):.1%}），"
        f"动态图形 {summary.get('motion_graphic_duration', 0):.2f}s"
        f"（{summary.get('motion_graphic_ratio', 0):.1%}），"
        f"总视觉覆盖 {summary.get('visual_ratio', 0):.1%}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""按可审查的 JSON 删词计划同步粗剪口播音视频。"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any


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


def kept_ranges(duration: float, cuts: list[dict[str, Any]]) -> list[tuple[float, float]]:
    ranges: list[tuple[float, float]] = []
    cursor = 0.0
    for cut in cuts:
        start = float(cut["start"])
        end = float(cut["end"])
        if start > cursor:
            ranges.append((cursor, start))
        cursor = end
    if cursor < duration:
        ranges.append((cursor, duration))
    return ranges


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

    duration = 0.0
    if source is not None and source.is_file():
        try:
            duration = probe_duration(source)
        except (subprocess.CalledProcessError, ValueError) as exc:
            errors.append(f"无法读取 source 时长：{exc}")

    cuts_value = plan.get("cuts")
    cuts = cuts_value if isinstance(cuts_value, list) else []
    if not isinstance(cuts_value, list) or not cuts:
        errors.append("cuts 必须是非空数组")

    normalized: list[dict[str, Any]] = []
    for index, cut in enumerate(cuts, start=1):
        if not isinstance(cut, dict):
            errors.append(f"删点 {index} 必须是对象")
            continue
        start = cut.get("start")
        end = cut.get("end")
        if not isinstance(start, (int, float)) or not isinstance(end, (int, float)):
            errors.append(f"删点 {index} 的 start/end 必须是数字")
            continue
        if start < 0 or end <= start or (duration and end > duration + 0.001):
            errors.append(f"删点 {index} 时间范围无效：{start}–{end}s")
            continue
        transcript = str(cut.get("transcript", "")).strip()
        reason = str(cut.get("reason", "")).strip()
        if not transcript:
            warnings.append(f"删点 {index} 没有 transcript，难以复核删了什么")
        if not reason:
            warnings.append(f"删点 {index} 没有 reason，难以复核删词依据")
        normalized.append({**cut, "start": float(start), "end": float(end)})

    normalized.sort(key=lambda item: item["start"])
    for previous, current in zip(normalized, normalized[1:]):
        if current["start"] < previous["end"]:
            errors.append(
                f"删点时间重叠：{previous['start']:.3f}–{previous['end']:.3f}s 与 "
                f"{current['start']:.3f}–{current['end']:.3f}s"
            )

    join_transition = plan.get("join_transition", 0.04)
    if not isinstance(join_transition, (int, float)) or join_transition < 0 or join_transition > 0.12:
        errors.append("join_transition 必须在 0–0.12 秒之间")
        join_transition = 0.04

    if duration and not errors:
        ranges = kept_ranges(duration, normalized)
        if not ranges:
            errors.append("删点覆盖了全部源片")
        for start, end in ranges:
            if end - start <= join_transition * 2:
                errors.append(
                    f"保留片段 {start:.3f}–{end:.3f}s 太短，无法完成连接淡化"
                )
        removed = sum(cut["end"] - cut["start"] for cut in normalized)
        output_duration = duration - removed - max(0, len(ranges) - 1) * join_transition
        plan["cuts"] = normalized
        plan["_summary"] = {
            "source_duration": duration,
            "removed_duration": removed,
            "join_transition": float(join_transition),
            "kept_ranges": ranges,
            "output_duration": output_duration,
        }

    return plan, errors, warnings


def build_command(plan: dict[str, Any]) -> list[str]:
    source = Path(plan["source"])
    output = Path(plan["output"])
    summary = plan["_summary"]
    ranges = summary["kept_ranges"]
    transition = float(summary["join_transition"])
    fps = int(plan.get("fps", 30))

    filters: list[str] = []
    durations: list[float] = []
    for index, (start, end) in enumerate(ranges):
        durations.append(end - start)
        filters.append(
            f"[0:v]trim=start={start:.6f}:end={end:.6f},setpts=PTS-STARTPTS,"
            f"settb=AVTB,fps={fps},format=yuv420p[v{index}]"
        )
        filters.append(
            f"[0:a]atrim=start={start:.6f}:end={end:.6f},asetpts=PTS-STARTPTS[a{index}]"
        )

    if transition == 0:
        concat_inputs = "".join(f"[v{index}][a{index}]" for index in range(len(ranges)))
        filters.append(
            f"{concat_inputs}concat=n={len(ranges)}:v=1:a=1[vconcat][aconcat]"
        )
        current_video = "vconcat"
        current_audio = "aconcat"
    else:
        current_video = "v0"
        current_audio = "a0"
        current_duration = durations[0]
        for index in range(1, len(ranges)):
            offset = current_duration - transition
            filters.append(
                f"[{current_video}][v{index}]xfade=transition=fade:"
                f"duration={transition:.3f}:offset={offset:.6f}[vx{index}]"
            )
            filters.append(
                f"[{current_audio}][a{index}]acrossfade=d={transition:.3f}:"
                f"c1=tri:c2=tri[ax{index}]"
            )
            current_video = f"vx{index}"
            current_audio = f"ax{index}"
            current_duration += durations[index] - transition

    output.parent.mkdir(parents=True, exist_ok=True)
    return [
        "ffmpeg",
        "-hide_banner",
        "-y",
        "-i",
        str(source),
        "-filter_complex",
        ";".join(filters),
        "-map",
        f"[{current_video}]",
        "-map",
        f"[{current_audio}]",
        "-c:v",
        "libx264",
        "-preset",
        "medium",
        "-crf",
        "18",
        "-pix_fmt",
        "yuv420p",
        "-c:a",
        "aac",
        "-b:a",
        "192k",
        "-movflags",
        "+faststart",
        str(output),
    ]


def main() -> int:
    if len(sys.argv) != 2:
        print("用法：render_content_plan.py /absolute/path/to/content_plan.json", file=sys.stderr)
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

    summary = plan["_summary"]
    print(
        f"删词计划通过：{len(plan['cuts'])} 个删点，删除 "
        f"{summary['removed_duration']:.3f}s，预计输出 {summary['output_duration']:.3f}s"
    )
    command = build_command(plan)
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as exc:
        print(f"错误：FFmpeg 内容粗剪失败，退出码 {exc.returncode}", file=sys.stderr)
        return exc.returncode or 1
    print(f"内容粗剪完成：{plan['output']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

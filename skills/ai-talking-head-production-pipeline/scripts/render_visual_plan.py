#!/usr/bin/env python3
"""按 JSON 镜头计划把图片/视频 B-roll 合成到口播主线上。"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from validate_visual_plan import IMAGE_EXTENSIONS, load_and_validate


def ffmpeg_filter_path(path: Path) -> str:
    return str(path).replace("\\", "\\\\").replace(":", "\\:").replace("'", "\\'")


def has_ffmpeg_filter(name: str) -> bool:
    result = subprocess.run(
        ["ffmpeg", "-hide_banner", "-filters"],
        check=True,
        capture_output=True,
        text=True,
    )
    return any(line.split()[1:2] == [name] for line in result.stdout.splitlines())


def build_command(plan: dict, burn_subtitle: bool) -> list[str]:
    source = Path(plan["source"])
    output = Path(plan["output"])
    visuals = plan.get("visuals", [])
    duration = float(plan.get("duration") or plan["_summary"]["duration"])
    width = int(plan.get("width", 1080))
    height = int(plan.get("height", 1920))
    fps = int(plan.get("fps", 30))

    command = ["ffmpeg", "-hide_banner", "-y", "-i", str(source)]
    for shot in visuals:
        asset = Path(shot["asset"])
        shot_duration = float(shot["end"] - shot["start"])
        if asset.suffix.lower() in IMAGE_EXTENSIONS:
            command.extend(["-loop", "1", "-framerate", str(fps), "-t", f"{shot_duration:.3f}", "-i", str(asset)])
        else:
            command.extend(["-stream_loop", "-1", "-t", f"{shot_duration:.3f}", "-i", str(asset)])

    subtitle_value = plan.get("subtitle")
    soft_subtitle = bool(subtitle_value and not burn_subtitle)
    subtitle_input_index = len(visuals) + 1
    if soft_subtitle:
        command.extend(["-i", str(subtitle_value)])

    filters = [
        f"[0:v]trim=start=0:end={duration:.3f},setpts=PTS-STARTPTS,"
        f"scale={width}:{height}:force_original_aspect_ratio=increase,"
        f"crop={width}:{height},setsar=1,fps={fps}[base0]"
    ]
    previous = "base0"
    for index, shot in enumerate(visuals, start=1):
        start = float(shot["start"])
        shot_duration = float(shot["end"] - shot["start"])
        transition = float(shot.get("transition", 0.3))
        fade_out_start = shot_duration - transition
        kind = shot.get("kind", "broll")
        layout = shot.get("layout", "overlay" if kind == "motion_graphic" else "full")
        if layout == "card":
            card_width = int(shot.get("card_width", 960))
            card_height = int(shot.get("card_height", 1280))
            border = int(shot.get("border", 6))
            inner_width = card_width - border * 2
            inner_height = card_height - border * 2
            transform = (
                f"scale={inner_width}:{inner_height}:force_original_aspect_ratio=increase,"
                f"crop={inner_width}:{inner_height},"
                f"pad={card_width}:{card_height}:{border}:{border}:color=white@0.45"
            )
            overlay_x = int(shot.get("x", (width - card_width) / 2))
            overlay_y = int(shot.get("y", 100))
        elif layout == "overlay":
            transform = (
                f"scale={width}:{height}:force_original_aspect_ratio=decrease,"
                f"pad={width}:{height}:(ow-iw)/2:(oh-ih)/2:color=black@0"
            )
            overlay_x = 0
            overlay_y = 0
        else:
            transform = (
                f"scale={width}:{height}:force_original_aspect_ratio=increase,"
                f"crop={width}:{height}"
            )
            overlay_x = 0
            overlay_y = 0
        filters.append(
            f"[{index}:v]trim=start=0:end={shot_duration:.3f},setpts=PTS-STARTPTS,"
            f"{transform},setsar=1,fps={fps},format=rgba,"
            f"fade=t=in:st=0:d={transition:.3f}:alpha=1,"
            f"fade=t=out:st={fade_out_start:.3f}:d={transition:.3f}:alpha=1,"
            f"setpts=PTS+{start:.3f}/TB[shot{index}]"
        )
        filters.append(
            f"[{previous}][shot{index}]overlay={overlay_x}:{overlay_y}:"
            f"eof_action=pass:shortest=0:format=auto[base{index}]"
        )
        previous = f"base{index}"

    if subtitle_value and burn_subtitle:
        subtitle = ffmpeg_filter_path(Path(subtitle_value))
        style = (
            "FontName=PingFang SC,FontSize=18,PrimaryColour=&H00FFFFFF,"
            "OutlineColour=&H00151515,BorderStyle=1,Outline=2,Shadow=0,"
            "Alignment=2,MarginV=135"
        )
        filters.append(f"[{previous}]subtitles=filename='{subtitle}':force_style='{style}'[vout]")
        video_label = "vout"
    else:
        video_label = previous

    filters.append(f"[0:a]atrim=start=0:end={duration:.3f},asetpts=PTS-STARTPTS[aout]")
    output.parent.mkdir(parents=True, exist_ok=True)
    command.extend(
        [
            "-filter_complex",
            ";".join(filters),
            "-map",
            f"[{video_label}]",
            "-map",
            "[aout]",
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
        ]
    )
    if soft_subtitle:
        command.extend(
            [
                "-map",
                f"{subtitle_input_index}:0",
                "-c:s",
                "mov_text",
                "-metadata:s:s:0",
                "language=zho",
            ]
        )
    command.extend(["-movflags", "+faststart", "-t", f"{duration:.3f}", str(output)])
    return command


def main() -> int:
    if len(sys.argv) != 2:
        print("用法：render_visual_plan.py /absolute/path/to/visual_plan.json", file=sys.stderr)
        return 2
    plan_path = Path(sys.argv[1])
    if not plan_path.is_absolute() or not plan_path.is_file():
        print("错误：计划文件必须是存在的绝对路径", file=sys.stderr)
        return 2
    plan, errors, warnings = load_and_validate(plan_path)
    for warning in warnings:
        print(f"警告：{warning}")
    if errors:
        for error in errors:
            print(f"错误：{error}", file=sys.stderr)
        return 1

    subtitle_value = plan.get("subtitle")
    burn_subtitle = bool(subtitle_value and has_ffmpeg_filter("subtitles"))
    if subtitle_value and not burn_subtitle:
        print("提示：本机 FFmpeg 缺少 subtitles 滤镜，将 SRT 降级为 mov_text 软字幕轨")
    command = build_command(plan, burn_subtitle)
    print(f"开始合成：{plan['output']}")
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as exc:
        print(f"错误：FFmpeg 合成失败，退出码 {exc.returncode}", file=sys.stderr)
        return exc.returncode or 1
    print(f"合成完成：{plan['output']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

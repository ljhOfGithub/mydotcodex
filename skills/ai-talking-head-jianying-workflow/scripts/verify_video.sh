#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 || $# -gt 3 ]]; then
  echo "用法: $0 <视频绝对路径> [检查目录] [逗号分隔时间点]" >&2
  exit 2
fi

video_path=$1
legacy_preview=""
if [[ $# -eq 2 && $2 =~ \.(jpg|jpeg|png)$ ]]; then
  legacy_preview=$2
  inspection_dir=$(dirname "$legacy_preview")
  marks_csv="1"
else
  inspection_dir=${2:-"${video_path%.*}_inspection"}
  marks_csv=${3:-"1"}
fi

if [[ ! -f "$video_path" ]]; then
  echo "视频不存在: $video_path" >&2
  exit 1
fi

ffprobe_bin=$(command -v ffprobe || true)
ffmpeg_bin=$(command -v ffmpeg || true)
if [[ -z "$ffprobe_bin" || -z "$ffmpeg_bin" ]]; then
  echo "需要可用的 ffprobe 和 ffmpeg" >&2
  exit 1
fi

mkdir -p "$inspection_dir"

"$ffprobe_bin" -v error \
  -show_entries 'format=filename,duration,size,bit_rate:stream=index,codec_name,codec_type,width,height,r_frame_rate,sample_rate,channels' \
  -of json \
  "$video_path" | tee "$inspection_dir/metadata.json"

IFS=',' read -r -a marks <<< "$marks_csv"
if [[ ${#marks[@]} -eq 0 ]]; then
  echo "至少需要一个检查时间点" >&2
  exit 2
fi

frame_paths=()
for index in "${!marks[@]}"; do
  mark=${marks[$index]//[[:space:]]/}
  if [[ -z "$mark" ]]; then
    echo "时间点不能为空" >&2
    exit 2
  fi
  if [[ -n "$legacy_preview" && $index -eq 0 ]]; then
    frame_path=$legacy_preview
  else
    frame_path="$inspection_dir/frame_$(printf '%02d' "$((index + 1))").jpg"
  fi
  "$ffmpeg_bin" -hide_banner -loglevel error -y \
    -ss "$mark" -i "$video_path" -frames:v 1 -q:v 2 "$frame_path"
  frame_paths+=("$frame_path")
  printf 'frame[%d]=%s time=%s\n' "$((index + 1))" "$frame_path" "$mark"
done

contact_sheet="$inspection_dir/contact_sheet.jpg"
if [[ ${#frame_paths[@]} -eq 1 ]]; then
  cp "${frame_paths[0]}" "$contact_sheet"
  printf 'metadata=%s\n' "$inspection_dir/metadata.json"
  printf 'contact_sheet=%s\n' "$contact_sheet"
  if [[ -n "$legacy_preview" ]]; then
    printf 'preview=%s\n' "$legacy_preview"
  fi
  exit 0
fi

inputs=()
filter_parts=()
stack_inputs=""
layout=""
for index in "${!frame_paths[@]}"; do
  inputs+=( -i "${frame_paths[$index]}" )
  filter_parts+=( "[$index:v]scale=360:640:force_original_aspect_ratio=decrease,pad=360:640:(ow-iw)/2:(oh-ih)/2[v$index]" )
  stack_inputs+="[v$index]"
  x=$(( (index % 3) * 360 ))
  y=$(( (index / 3) * 640 ))
  if [[ -n "$layout" ]]; then
    layout+="|"
  fi
  layout+="${x}_${y}"
done

filter_complex=$(IFS=';'; echo "${filter_parts[*]};${stack_inputs}xstack=inputs=${#frame_paths[@]}:layout=${layout}:fill=black[out]")
"$ffmpeg_bin" -hide_banner -loglevel error -y \
  "${inputs[@]}" \
  -filter_complex "$filter_complex" \
  -map '[out]' -frames:v 1 -q:v 2 "$contact_sheet"

printf 'metadata=%s\n' "$inspection_dir/metadata.json"
printf 'contact_sheet=%s\n' "$contact_sheet"

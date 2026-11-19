---
name: hypit-voice-cadence
description: 用 Hypit 复刻有旁白的参考视频时，按原片节奏用本人 VoxCPM2 连续配音，先听完整音轨，认可后原速配回并检查逐采样保真。音乐 MV 原声不走此流程。
---

# Hypit 原片节奏配音

复刻带旁白的参考片时使用。用户明确的声音、时长或情绪要求优先；音乐MV沿用原唱，不克隆本人旁白。用户指定Hypit时，仍由Hypit编排、渲染、组织音轨和合成。

1. 先读工作区的 `Hypit制作与交付检查门.md` 和本 Skill 的[执行流程](references/workflow.md)。逐句记录原片时窗、停顿、重音、上扬与回落；听不到声音时，明确区分ASR时码和真实听感，不编造已经听过原片。
2. 保持逐句改写与信息顺序，先连续生成开头前三句，少于三句时全部生成。本地VoxCPM2沿用已验证的 `jackie-reference.wav`。默认兴奋、自然、有起伏；依原片调整句内节奏，不能只加速或提音量。
3. 开头选定后，用这段**同一本人声音**及其对应文本续接后文，每次按完整语义段生成。续接的 `text` 必须只有目标口播；表演提示不能拼进续接正文。原片音轨只作节奏参照，不能用于克隆作者声线。
4. 每个源段另做独立ASR，检查多读提示、漏词及英文工具名；强制对齐只用于字幕定位。句间保留空格，防止 `Hallmark！GitHub` 被分词器合并；以实际音频定字幕，不信混词的时间码。
5. 整轨先交用户试听，开头前三句逐句保留普通/新版同句对照。记录具体反馈；“好多了”不等于完整认可。用户确认原速保留后，锁定整轨WAV与SHA，不再为追音高指标重配、拉伸、移调、改增益或加混响。
6. 正式构建前执行[配音门](scripts/voice_cadence_gate.py)的 `--stage voice_ready`；配回后执行 `--stage delivery`，实际MP4的整轨PCM必须与获批WAV逐采样相同，仅允许尾部补零。独立完成情绪门、音质与语速门、前三句实际回切、字幕同步及半秒OCR；有损相关性和ASR不能替代听检。

口播复刻清单设 `creation_mode: reference_recreation`，并在 `narration.reference_cadence_qa` 绑定证据JSON，由工作区 `工具/Hypit交付门.py` 强制调用。无旁白MV和原创片不强套参考片流程，但仍如实标记类型。

执行示例：

```sh
python scripts/voice_cadence_gate.py 配音节奏证据.json --stage voice_ready
python scripts/voice_cadence_gate.py 配音节奏证据.json --stage delivery --output 配音节奏门结果.json
python scripts/test_voice_cadence_gate.py
```

路径均以实际项目为准。不要为这套流程重配已经认可且未改变的音频；只恢复获批声音并修正画面或字幕。

# OPUSCAR 98 立体 Clawd

脚本依据 [OPUSCAR 98 主海报](https://lemomo-ai.github.io/lemo-opuscar/zh/opuscar98/) 重建圆角橙色机身、黑色竖眼、两只短手和四只短脚。Python 和 Numba 在本地计算形体和光影，每个姿势输出一张 **990×750 RGBA PNG**。PNG 的 alpha 通道表示像素透明度，背景对 Hypit 保持透明。立体造型没有嘴巴，表演用眼神、眨眼和举手。

在项目根目录运行。Jackie 的 Mac 直接用共享 Python。其他环境用安装了 NumPy、Numba 和 Pillow 的 Python，技能路径取实际安装位置。

```bash
skill_dir="$HOME/.codex/skills/clawd"
python_bin=/Users/jackie/Documents/Git/.venv/bin/python
"$python_bin" "$skill_dir/scripts/render_3d.py" \
  --pose hero listen point blink --output-dir "$PWD/assets/clawd"
```

| 预设 | 用途 |
| --- | --- |
| `hero` | 展示角色、开场 |
| `listen` | 侧看、听别人讲话 |
| `listen-blink` | 与 `listen` 配对的眨眼 |
| `question` | 反问、抬手 |
| `point` | 举起角色画面右侧的手、指示 |
| `close` | 正视、收尾 |
| `blink` | 与 `close` 配对的眨眼 |

用 `--all` 批量渲染七种预设。自定义时只选一个基础姿势，用 `--name` 加一个独立文件名。两只手臂分别调节，正角度表示向上抬手，负角度表示向下放手。相机方位角 `--yaw` 支持 ±40°，仰俯角 `--pitch` 支持 ±16°，单手支持 ±65°。视线使用 `forward`、`left`、`right`、`up`、`down` 或 `blink`。

```bash
"$python_bin" "$skill_dir/scripts/render_3d.py" \
  --pose close --name wave-left --arm-left 45 --arm-right -8 \
  --gaze up --yaw -18 --pitch 6 --output-dir "$PWD/assets/clawd"
```

脚本在标准输出报告 PNG 的绝对路径、共用锚点和非透明像素边界。重复生成时使用新目录或新文件名，脚本会保护已有文件。检查导出的完整画布，确认角色未裁边、边缘有透明过渡，并按项目要求做 OCR 核查。

在 Hypit 的 Author 中用工程内相对路径声明 PNG，再通过该工程画面组件的素材入口加载。对应原 Art Deco 工程，绘制各姿势时使用同一个目标尺寸和原图锚点 `(495, 609)`（左上角为原点），便于让姿势落在同一台面。需要眨眼时用成对的正视或侧视贴图切换。保留透明通道，由舞台决定背景和投影，并按项目审批规则提交关键画面。

以下声明使用上述批量生成命令写入的素材路径。影片由 Hypit 运行相应的 Author、Recipe 和 Run 完成编排、渲染和合成。

```xml
<media:Image id="clawd-hero" src="./assets/clawd/hero.png"/>
<media:Image id="clawd-point" src="./assets/clawd/point.png"/>
```

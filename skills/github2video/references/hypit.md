# Hypit 执行与交付

## 环境发现

先查当前工程 `package.json`、`hypit.runtime.json`、`.hypit` 与 `node_modules/.bin/hypit`，再查 PATH。读取实际 CLI 的 `--help`、`version`、`check --help`、`build --help` 及需要的 vocabulary；不猜 API，不默认存在 Hypit MCP。

本机 2026-11-25 核实的一个入口：

`/Users/jackie/Documents/ChatGPT/远程管理/codex-edit-skill-hypit-native-2026-11-09/node_modules/@hypit/hypit/bin/hypit.mjs`

这是本机发现线索，不是跨机器配置；执行前检查仍存在。PATH 有 `hypit` 就直接用，否则用 `node /已核实路径/hypit.mjs` 替代下文的 `hypit`。字体、媒体、包与 Endpoint 从当前安装或工程确定，不虚构服务地址；凭据不写入 Skill 或执行回显。

## 工程与顺序

工程至少保留 `production/main.svml`（Author 主体/媒体/音轨时间线）、`production/look.svs`（Recipe 视觉规则）、`production/full.svrun`（Run 输出选择）、真实 `assets/`、当前运行配置及 `evidence/`。动作代码沿用已验证模板，按本片内容和时码适配。不要复制旧自定义包的固定总帧数、专属模块、案例 crop 或声音哈希。

已验证的 Run 语法如下，必须对应 Author 的实际输出 `final.video`：

```xml
<?svml using="@hypit/markup/run@1"?>
<svrun version="1">
  <author source="./main.svml"/>
  <target output="final.video"/>
</svrun>
```

在工程根目录保存每条命令的实际 stdout、stderr 和退出码。路径先核实；CLI 版本变化时先核对帮助。

```bash
hypit check production/main.svml --json
hypit check production/full.svrun --json
hypit plan production/full.svrun --json
hypit build production/full.svrun --runtime hypit.runtime.json --project . --title "当前项目" --follow --max-wait-ms 3600000 --json
hypit status ACTUAL_BUILD_ID --json
hypit get ACTUAL_BUILD_ID --output final.video --to outputs/native.mp4 --json
```

`ACTUAL_BUILD_ID` 取自真实返回。Build 之前完成整片计划和适用图审。长命令由持久后台执行器运行并保存 PID，模型每 60 秒内检查，不能用一小时阻塞等待代替监控。

既有成功工程使用 Hypit 0.3.1，返回 `build.id`，在 `build.work.state == "done"` 且 `build.result.state == "complete"` 后导出。保存实际响应，不套用未知版本结构。`check`、`plan` 均不渲染，不能宣称已成片。

中断后读取原 Build ID，用 `status`、`logs`、`inspect` 恢复。已完成直接导出，仍运行则监控原任务；只有真实失败并定位原因才最小修复、另提交。现有导出先检查，不覆盖、无故重做。真实媒体必须在 Hypit 声明并进入实际使用时窗，只在资料目录或左侧对比出现不算使用；原创片不强塞参考原视频。

## 输出与声音

保留原生 Result；观看副本另命名并记编码归属。默认 H264、8 位 yuv420p 的兼容 MP4，不为未要求的色差研究反复导出。

已批准声音保持原速、切点和样本；有损 AAC 封装成 WAV 不会恢复原音。要求严格保真时核实际观看 MP4 解码样本，不只核制作输入。没有批准声音则记 `narration_pending`，不能借别集旁白、把估算时码写成真实 ASR。

完整逐镜覆盖、实际媒体、半秒 OCR、正常速度动态审片与真实听检分别留结论。样片通过不外推整片。源码仅通过 check 时，交付称“可检查工程”，不称已验收成片。

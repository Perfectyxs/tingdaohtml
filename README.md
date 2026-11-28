# 听道 HTML 交互原型

在线预览：**https://perfectyxs.github.io/tingdaohtml/**

当前改版：**v1.4.7 · 2026-11-20**。HTML 是独立仓库；Android、唯一系统架构和 APK 发布位于 [Perfectyxs/Earthonline](https://github.com/Perfectyxs/Earthonline)。

- 丢弃录音确认弹层随内容收缩，待办确认等弹层保持原有动态高度。
- 计划、复盘录音的整理、待办确认和本地写入结果可体验示例流程；真实转录和本地 AI 尚待接入。
- 录音页的计划/复盘模式：录音卡紧接模式栏，与监听对齐；提词器在卡片下方，支持 **日计划 / 周计划** 切换。
- 历史复盘分 **每日复盘 / 复盘录音 / 计划记录**；经验卡集中在历史。
- 新增角色点“＋”直接打开录制声纹，姓名、标签、头像、录制、重录和保存在同一页完成；取消三选一和中间确认页。
- 陌生声纹保留 **手动勾选 / 自动聚集**，可合成新人物或并入旧人物；支持拆组和撤销归属。
- 专业词表只从设置管理，录音页不新增词表入口；录音后台沿用默认选择并保存快照。
- 设置新增“复盘与角色”，移动评分权重和角色标签。

[丢弃录音确认截图](docs/review-v1.4.4/README.md) · [录音整理与待办确认截图](docs/review-v1.4.3/README.md) · [本轮计划/复盘长图与验收清单](docs/review-v1.4.2/README.md) · [逐页长截图、差异与验收记录](docs/review-v1.4/README.md) · [浏览器验证结果](docs/review-v1.4/checks.json)

**实现边界：** 这是可操作的交互原型。声纹相似度使用预设示例数据；录制声纹不调用麦克风，不从文字推断声音身份。真实采集、音频回听、声纹模型、ASR、报告生成与 Android 状态须在原生工程实现、评测和验收。浏览器本地保存不代表 App 数据已同步或 APK 已发布。

本地预览：`python3 -m http.server 8765`；检查：`python3 tests/preview_v14.py`（需要 Playwright 和系统 Chromium）。

`main` 上的 HTML / assets 更新由 GitHub Actions 发布至上述 Pages 地址；站点预览与 Android PR 合并、APK 发布分别管理。


### 2026-11-28 · 单条语录手动删除

角色详情及待归属语录支持左滑显示删除按钮，点击后删除该条语录；键盘左方向键也可显示按钮。来源录音和原始句段保留，删除可在提示条中撤销。原“移出语录”仍只将语录退回待归属，不删除来源。

通过真实指针滑动、删除、撤销、原录音/原句段不变及浏览器脚本错误检查。Android 和逐屏对照持续更新在 [Earthonline main](https://github.com/Perfectyxs/Earthonline/blob/main/docs/visual-verification/alpha11/review/README.md)。

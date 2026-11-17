# 听道 HTML 交互原型

在线预览：**https://perfectyxs.github.io/tingdaohtml/**

当前改版：**v1.4 · 2026-11-17**。HTML 是独立仓库；Android、唯一系统架构和 APK 发布位于 [Perfectyxs/Earthonline](https://github.com/Perfectyxs/Earthonline)。

- 历史复盘分 **每日复盘 / 复盘录音 / 计划记录**；经验卡集中在历史。
- 新增角色分 **名称建档 / 主动录制声纹 / 从陌生声纹合成**。
- 陌生声纹保留 **手动勾选 / 自动聚集**，可合成新人物或并入旧人物；支持拆组和撤销归属。
- 专业词表按整包多选、进入编辑；录音保存本次词表快照。
- 设置新增“复盘与角色”，移动评分权重和角色标签。

[逐页长截图、差异与验收记录](docs/review-v1.4/README.md) · [浏览器验证结果](docs/review-v1.4/checks.json)

**实现边界：** 这是可操作的交互原型。声纹相似度使用预设示例数据；录制声纹不调用麦克风，不从文字推断声音身份。真实采集、音频回听、声纹模型、ASR、报告生成与 Android 状态须在原生工程实现、评测和验收。浏览器本地保存不代表 App 数据已同步或 APK 已发布。

本地预览：`python3 -m http.server 8765`；检查：`python3 tests/preview_v14.py`（需要 Playwright 和系统 Chromium）。

`main` 上的 HTML / assets 更新由 GitHub Actions 发布至上述 Pages 地址；站点预览与 Android PR 合并、APK 发布分别管理。

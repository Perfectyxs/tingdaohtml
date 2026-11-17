# v1.4 改版审核：历史、角色声纹与专业词表

> 2026-11-17｜HTML 交互预览。历史三分类和设置分组已由用户确认；声纹生产算法、参数与 Android 实现仍待评测审核。下面均为 **HTML 浏览器截图**，不是 Android 或真实模型运行截图。

## 按数字对照差异与修改

| 编号 | 旧版问题 | 本版怎么改 | 点击验收 |
| --- | --- | --- | --- |
| 01 | “每日复盘”实际是 8 分钟复盘录音，与日报混用 | 历史分每日复盘 / 复盘录音 / 计划记录；每日报告独立保存和展示 | 三类切换，日报可查看简介、亮点、偏差、下一步和来源；原录音仍可打开 |
| 02 | 经验卡名称与复盘重复区域 | 顶部叫经验卡；整理、确认集中历史；移除复盘整个经验区 | 待确认/已存入可切换；手动整理仍可进入；复盘无残留模块 |
| 03 | 新增角色只有名称表单 | 新增名称建档、录制声纹、陌生池合成三路径 | 每条入口分别打开下级页，返回不串入其他模式 |
| 04 | 建名字被误认为已有声纹 | 名称角色标待采样，先从历史认领样本，再允许自动匹配 | 无样本时开关禁用；认领后来源和模板版本可见 |
| 05 | 主动录制只有说明文字 | 增加录制、计时、样本确认、重录、保存演示 | 计时、过短提示、确认保存可操作；明确未调用麦克风或声纹模型 |
| 06 | 陌生池变成平铺卡，手动/自动混在一起 | 恢复概览、自动合成设置、手动勾选/自动聚集和底部操作 | 多选计数正确；自动页按声线分组；切换页面不修改自动策略 |
| 07 | 合成目标不清楚 | 明确“合成新人物 / 并入旧人物”，切换保留草稿 | 只归属所选片段，关联语录更新，原始来源保留，可撤销 |
| 08 | 缺自动匹配机制和纠错约束 | 示例相似度驱动约束聚集；支持拆组、不得再并；已有角色用可信种子匹配 | 无模板不推断身份；符合规则的示例自动归属；结果不直接训练回模板 |
| 09 | 扁平热词逐词勾选 | 升级为专业包多选、详情编辑、新建、导入/导出和复制 | 点击专业名与勾选分开；编辑增加版本并持久化 |
| 10 | 词表是否影响本次录音不清楚 | 增加本次选择与冻结快照；明确 SenseVoice 仅后置规整 | 本次覆盖不改默认；后续编辑不改快照；旧记录标未知版本 |
| 11 | 评分和角色标签分散 | 新增“复盘与角色”，移动两个原入口 | 原页面可打开；不新增独立角色分类功能 |

## 主屏与下级页完整长图

截图扩展实际内容滚动区，保留完整内容，固定底部操作只出现一次；尺寸见 [checks.json](checks.json)。本屏清单供人工逐项审核，不代表每个按钮都已自动测试。

| 页面 / 点击顺序 | 长图 | 本屏验收清单 |
| --- | --- | --- |
| 01 录音 | [主屏](screenshots/01-recording-full.png) | 五模式、词表入口、开始/暂停/结束、转写、今日声音 |
| 01-01 本次词表 | [选择弹层](screenshots/01-01-session-lexicons.png) | 整包多选、本次使用、管理默认、进入详情、关闭取消 |
| 02 历史 | [录音列表](screenshots/02-history-recordings.png) | 顶部三栏、日期、周统计、筛选、录音详情 |
| 02-01 每日复盘 | [列表](screenshots/02-01-daily-reviews.png) / [详情](screenshots/02-01-01-daily-review-detail.png) | 简介与报告类型正确，详情来源可进入原录音 |
| 02-02 复盘录音 | [复盘录音](screenshots/02-02-review-recordings.png) | 只显示复盘模式，不冒充日报 |
| 02-03 计划记录 | [计划录音](screenshots/02-03-planning-recordings.png) | 保留计划录音，不当作正式待办 |
| 02-04 经验卡 | [经验卡](screenshots/02-04-experience-cards.png) | 待确认/已存入、手动整理、确认与来源 |
| 03 复盘 | [完整主屏](screenshots/03-review-full.png) | 经验区整个移除，全景/计划/数据/计划锚保留 |
| 04 设置 | [完整主屏](screenshots/04-settings-full.png) | 专业词表、“复盘与角色”、评分和标签入口 |
| 04-01 专业词表 | [词表库](screenshots/04-01-lexicon-library.png) / [详情](screenshots/04-01-01-professional-pack.png) | 整包勾选、点入编辑、新建/导入、复制/导出/删除、能力状态 |
| 04-01-01 词条 | [编辑表单](screenshots/04-01-01-01-term-editor.png) / [新包空态](screenshots/04-01-02-new-pack-empty.png) | 标准词、类型、别名、错词、拼音、备注、启停/保存/删除 |
| 05 角色 | [角色主屏](screenshots/05-roles-full.png) | 详情、标签/头像、新增、声纹池、语录、归档 |
| 05-01 新增 | [三种路径](screenshots/05-01-create-role-paths.png) | 名称建档、录制声纹、陌生池合成 |
| 05-01-01 名称 | [表单](screenshots/05-01-01-name-enrollment.png) / [待采样](screenshots/05-01-01-01-pending-voice.png) / [历史认领](screenshots/05-01-01-02-history-enrollment.png) | 姓名/标签/头像、保存、待采样、认领片段、自动匹配条件 |
| 05-01-02 采样 | [录制页](screenshots/05-01-02-sample-enrollment.png) / [确认样本](screenshots/05-01-02-01-sample-confirmation.png) | 开始/结束、计时、过短提示、重录、保存和返回 |
| 05-02 陌生池 | [手动长图](screenshots/05-02-manual-voice-pool.png) / [自动聚集长图](screenshots/05-02-03-automatic-clusters.png) | 自动开关、页签、多选计数、来源、合成、重新聚集、拆组 |
| 05-02-01 合成 | [新人物](screenshots/05-02-01-synthesize-new-person.png) / [旧人物](screenshots/05-02-02-merge-existing-person.png) | 新名称/标签、已有角色选择、草稿、确认/取消与撤销 |
| 05-02-04 自动匹配 | [匹配结果](screenshots/05-02-04-known-role-matching.png) | 有依据才推荐、无模板保留未知、规则通过才归属、不自我训练 |

## 验证范围

结果：[checks.json](checks.json)；脚本：[preview_v14.py](../../tests/preview_v14.py)。检查主要改动的浏览器行为、保存/返回、合并/撤销、冲突聚集、示例匹配和窄屏布局。

真实模型精度、音频采集/回听、Android 与 APK 未由此次 HTML 测试验证。后续 HTML/Android 对照仍需逐页长截，每张图下按数字列“不一致 → 怎么改 → 复验结果”。

系统架构唯一真源：[Earthonline / ARCHITECTURE](https://github.com/Perfectyxs/Earthonline/blob/proposal/professional-lexicon-system/docs/ARCHITECTURE.md)。本库负责交互预览，不另行定义业务系统。

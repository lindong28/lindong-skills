# 随包文本封面模板

这十二款同时用于网站和本地 skill。正文的唯一来源为仓库 `library/image/prompts/`，本目录由 `sync_catalog.py` 机械导出，勿单独修改。每款正文内含完整视觉规范和 HTML/CSS 种子；选中后只读取对应文件。用户可以直接给中文名、下表标识或本地文件路径。网站 URL 始终从 API 读取。

模板默认种子是 600×800 的小红书构图；公众号或用户指定画幅由 skill 按本次内容重新排版。两种平台共用一份视觉定义，不维护平台专属的重复模板。自然奢雅需要用户确认的照片素材；杂志风、瑞士风默认引用联网字体。

| 名称 | 标识与完整 Prompt |
|---|---|
| 柔和科技 | [soft-tech](templates/soft-tech.md) |
| 商务新闻 | [business-news](templates/business-news.md) |
| 流动蓝色 | [flowing-blue](templates/flowing-blue.md) |
| 极简网格 | [minimal-grid](templates/minimal-grid.md) |
| 极简票券 | [minimal-ticket](templates/minimal-ticket.md) |
| 构成主义 | [constructivist](templates/constructivist.md) |
| 自然奢雅 | [luxury-nature](templates/luxury-nature.md) |
| 工业叛逆 | [industrial-rebel](templates/industrial-rebel.md) |
| 柔软可爱 | [soft-cute](templates/soft-cute.md) |
| 商务极简 | [business-minimal](templates/business-minimal.md) |
| 杂志风 | [editorial-magazine](templates/editorial-magazine.md) |
| 瑞士风 | [swiss-international](templates/swiss-international.md) |

前十款参照[原文的十款封面](https://mp.weixin.qq.com/s/OFCgFrXNQgIT2ho3V-4Oag)整理视觉系统；末两款使用随包 Guizang 的杂志风和瑞士风资源，来源与许可见 [UPSTREAM](../UPSTREAM.md)。正文是可复用定义，已生成样例的实际 Prompt 另行保留，不能混用。

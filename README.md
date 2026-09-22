# lindong-skills

供 Claude Code / Codex 等 agent 直接安装的 skill。本仓是**分发镜像**：源与历史在 [prompt-templates](https://prompts.aiplanet.live/skill/)（私有仓）维护，由脚本整体镜像到这里；请不要在本仓提交修改，问题请到网站或 issue 反馈。

## Skills

| skill | 说明 | 目录 |
|---|---|---|
| `html-imagegen` | 根据 HTML 图片模板、目标平台（小红书或公众号）和用户内容生成封面；按需询问缺失信息并提供模板选项，生成 HTML 后用浏览器导出 PNG。支持本地模板与 Prompt Planet 文本模型模板；图片模型生成或编辑使用独立图片工具。 | [`html-imagegen/`](html-imagegen/) |

## 安装

```sh
git clone https://github.com/lindong28/lindong-skills
```

把 `html-imagegen/` 目录放到宿主的 skills 目录（复制或符号链接均可）：Claude Code 为 `~/.claude/skills/`，Codex 为 `~/.agents/skills/`。首次运行按该目录 `SKILL.md` 安装 uv、Playwright 与 Chromium。

## 许可

整仓按 [AGPL-3.0](LICENSE) 分发；`html-imagegen/vendor/guizang/` 为上游 [op7418/guizang-social-card-skill](https://github.com/op7418/guizang-social-card-skill) 的字节快照，保留其自带的 LICENSE 与 COMMERCIAL_LICENSING.md，来源与版本见 `html-imagegen/UPSTREAM.md`。

当前镜像自 prompt-templates `d83a4f0e356fb6e5b66e3ffcfe83c611fb893a07`（`html-imagegen/.mirror-source` 记录同一值）。

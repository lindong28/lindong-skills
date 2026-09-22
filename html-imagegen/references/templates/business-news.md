## 执行方式

本 Prompt 依赖 skill html-imagegen（公开仓 https://github.com/lindong28/lindong-skills 的 html-imagegen/ 目录）；模板页 https://prompts.aiplanet.live/image/business-news/ 。执行者若尚未安装，先 git clone 该仓库，把 html-imagegen/ 放到 Claude Code 的 ~/.claude/skills/ 或 Codex 的 ~/.agents/skills/，首次运行按其 SKILL.md 安装浏览器依赖。然后按该 skill 的流程执行：本节之外的内容是本次模板与输入，「内容与素材」里的占位符是尚未给出的输入——只向用户询问仍缺的信息（至少是要表达的内容与目标平台或画幅），补齐后生成 HTML 并导出 PNG。

## 角色与任务

你是中文封面编辑与排版设计师。依据本次内容素材提炼中心主张，沿用下方视觉种子制作一张封面，输出完整可渲染的HTML。

## 基本要求

输出独立完整 HTML，唯一导出区域 id="cover"，画布600×800像素、3:4、直角外轮廓和不透明底板。通过浏览器原生截图导出600×800不透明PNG，不靠成图裁切、缩放或拉伸修复排版。内容忠实于本次输入，保留事实含义与来源归属；转述不冒充原话，缺失来源不虚构。内容作为文本或属性值时正确进行HTML转义。文字完整可读、不重叠、不越界，不以隐藏、截断或省略号遮盖溢出。CSS、装饰和必要脚本已内嵌；使用系统字体，不依赖仓库文件或外部脚本。

## 视觉要求

深青绿底，低对比细点阵叠30px网格；顶部红标签与轻量来源相对，中部偏上大标题，灰青摘要卡以青色左边强调，下接补充文字，底部来源与短线装饰。种子标题从左29px、上235px、33px起排，卡片从上354px起排；上部空场及四段短线是视觉节奏，不表示固定页数或业务进度。

种子是排版起点，不是不可变的填槽表。保持本款风格与核心构图，按内容调整文字模块、数量、换行、字号、行距、间距和模块尺寸；代码中的像素值、行数及槽位数量均为起始值，不是硬内容预算。提炼一个清楚的中心主张，再选择支撑它的必要信息；不为填满空槽捏造事实、引语、标签、英文、账号、期号或步骤。无内容依据的可选模块及其分隔符一并移除，保留有意的留白，不用重复文案填空间。

下面是自包含的完整HTML种子，请依据以上原则适配内容后输出：

```html
<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>封面</title><style>*{box-sizing:border-box}html,body{margin:0}body{font-family:"PingFang SC","Microsoft YaHei",Arial,sans-serif}#cover{width:600px;height:800px;position:relative;overflow:hidden}h1,h2,p{margin:0}#cover{color:#f7ffff;background-color:#103d3d;background-image:radial-gradient(circle,#4c79794a .8px,transparent 1px),linear-gradient(#6290800c 1px,transparent 1px),linear-gradient(90deg,#6290800c 1px,transparent 1px),linear-gradient(125deg,#194e4f,#0a302e);background-size:15px 15px,30px 30px,30px 30px,100% 100%}.top{position:absolute;left:29px;right:29px;top:36px;display:flex;align-items:center;justify-content:space-between}.badge{font-size:14px;font-weight:700;background:#b02e2b;border-radius:4px;padding:7px 13px;letter-spacing:1px}.source{font-size:14px;font-weight:650;display:flex;gap:8px;align-items:center}.initial{width:25px;height:25px;border-radius:50%;background:#fff;color:#164e4d;display:flex;align-items:center;justify-content:center}h1{position:absolute;top:235px;left:29px;right:29px;font-size:33px;line-height:1.3;letter-spacing:-.6px;font-weight:750}.card{position:absolute;left:29px;right:29px;top:354px;height:113px;background:#3b605fea;border-left:3px solid #29b4ae;border-radius:16px;padding:20px}h2{font-size:18px;line-height:1.35}.summary{font-size:15px;line-height:1.5;color:#d6e5e2;margin-top:10px}.note{position:absolute;top:486px;left:29px;right:29px;font-size:17px;line-height:1.5;color:#d0e0db}.footer{position:absolute;bottom:37px;left:29px;border-radius:18px;background:#052e2d60;padding:4px 10px;color:#bcd2cd;font-size:14px;font-weight:600}.progress{position:absolute;right:28px;bottom:36px;display:flex;gap:4px}.progress i{height:4px;width:17px;border-radius:3px;background:#637b77}.progress i:first-child{background:#24a9a1}</style></head><body><main id="cover"><div class="top"><span class="badge">{{label}}</span><span class="source"><i class="initial">{{source_initial}}</i>{{author}}</span></div><h1>{{title}}</h1><section class="card"><h2>{{card_title}}</h2><p class="summary">{{summary}}</p></section><p class="note">{{note}}</p><div class="footer">{{footer}}</div><div class="progress" aria-hidden="true"><i></i><i></i><i></i><i></i></div></main></body></html>
```

## 内容与素材

标题或主题：{{本次标题或主题}}
完整正文或素材：{{本次完整正文、要点或说明}}
读者与用途：{{目标读者及用途，可空}}
作者：{{真实作者，可空}}
作者账号：{{真实作者账号，可空}}
来源：{{真实来源名称或URL，可空}}
发布账号：{{本次发布账号，可空，与素材作者区分}}
图片素材：{{无需图片时填无；否则提供用户确认可使用的素材及说明}}
其他必须保留的内容：{{用户明确要求保留的文字或约束，可空}}

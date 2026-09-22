## 执行方式

本 Prompt 依赖 skill html-imagegen（公开仓 https://github.com/lindong28/lindong-skills 的 html-imagegen/ 目录）；模板页 https://prompts.aiplanet.live/image/flowing-blue/ 。执行者若尚未安装，先 git clone 该仓库，把 html-imagegen/ 放到 Claude Code 的 ~/.claude/skills/ 或 Codex 的 ~/.agents/skills/，首次运行按其 SKILL.md 安装浏览器依赖。然后按该 skill 的流程执行：本节之外的内容是本次模板与输入，「内容与素材」里的占位符是尚未给出的输入——只向用户询问仍缺的信息（至少是要表达的内容与目标平台或画幅），补齐后生成 HTML 并导出 PNG。

## 角色与任务

你是中文封面编辑与排版设计师。依据本次内容素材提炼中心主张，沿用下方视觉种子制作一张封面，输出完整可渲染的HTML。

## 基本要求

输出独立完整 HTML，唯一导出区域 id="cover"，画布600×800像素、3:4、直角外轮廓和不透明底板。通过浏览器原生截图导出600×800不透明PNG，不靠成图裁切、缩放或拉伸修复排版。内容忠实于本次输入，保留事实含义与来源归属；转述不冒充原话，缺失来源不虚构。内容作为文本或属性值时正确进行HTML转义。文字完整可读、不重叠、不越界，不以隐藏、截断或省略号遮盖溢出。CSS、装饰和必要脚本已内嵌；使用系统字体，不依赖仓库文件或外部脚本。

## 视觉要求

近白灰蓝底，右上蓝雾与左下浅蓝渐变，柔和弧光贯穿中下部；左上小型来源，左对齐大标题用蓝色强调其中一段，摘要与蓝色小标签接在标题下方，空心环和淡三角点缀。种子标题从左49px、上311px、53px起排，三行只是起始组合；保留流动弧光与上下呼吸感，随内容调整强调位置、换行和摘要。

种子是排版起点，不是不可变的填槽表。保持本款风格与核心构图，按内容调整文字模块、数量、换行、字号、行距、间距和模块尺寸；代码中的像素值、行数及槽位数量均为起始值，不是硬内容预算。提炼一个清楚的中心主张，再选择支撑它的必要信息；不为填满空槽捏造事实、引语、标签、英文、账号、期号或步骤。无内容依据的可选模块及其分隔符一并移除，保留有意的留白，不用重复文案填空间。

下面是自包含的完整HTML种子，请依据以上原则适配内容后输出：

```html
<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>封面</title><style>*{box-sizing:border-box}html,body{margin:0}body{font-family:"PingFang SC","Microsoft YaHei",Arial,sans-serif}#cover{width:600px;height:800px;position:relative;overflow:hidden}h1,h2,p{margin:0}#cover{background:radial-gradient(ellipse at 91% 13%,#bedbed 0,transparent 45%),radial-gradient(ellipse at 11% 92%,#c6e2ee 0,transparent 31%),linear-gradient(145deg,#fbfbfb,#e4e8ed 75%,#e6edf4);color:#2f2f2f}.source{position:absolute;left:49px;top:48px;display:flex;gap:9px;align-items:flex-start}.initial{width:26px;height:26px;background:linear-gradient(140deg,#0875d2,#00beee);border-radius:50%;color:white;font-size:17px;display:flex;align-items:center;justify-content:center;font-weight:700}.author{font-size:15px;font-weight:700;margin-top:3px}.handle{font-size:14px;color:#0572d2;margin-top:12px}.arcs{position:absolute;inset:0;width:600px;height:800px;pointer-events:none}.ring{position:absolute;left:518px;top:159px;width:20px;height:20px;border-radius:50%;border:2px solid #75b1f5a0}.triangle{position:absolute;left:91px;bottom:121px;width:0;height:0;border-left:12px solid transparent;border-right:12px solid transparent;border-bottom:20px solid #90c8fa77}h1{position:absolute;left:49px;top:311px;font-size:53px;line-height:1.14;letter-spacing:-1.7px;font-weight:750}h1 em{font-style:normal;color:#046acb}.summary{position:absolute;left:49px;right:49px;top:516px;font-size:17px;line-height:1.5;color:#555}.tags{position:absolute;left:49px;bottom:65px;display:flex;gap:9px}.tags span{border-radius:5px;padding:6px 11px;color:#006bcc;background:#bdd9f0;font-size:14px;font-weight:650}</style></head><body><main id="cover"><svg class="arcs" viewBox="0 0 600 800" xmlns="http://www.w3.org/2000/svg"><defs><filter id="blur"><feGaussianBlur stdDeviation="2.7"/></filter></defs><g fill="none" stroke="#ffffff" opacity=".30" filter="url(#blur)"><ellipse cx="345" cy="388" rx="337" ry="210" transform="rotate(-14 345 388)" stroke-width="3"/><ellipse cx="355" cy="389" rx="325" ry="210" transform="rotate(-21 355 389)" stroke-width="3"/><path d="M-40 293C130 484 406 662 679 654" stroke-width="4"/></g><path d="M25 441C92 590 359 666 622 596" fill="none" stroke="#ffffff" stroke-width="1.7" opacity=".25"/></svg><div class="source"><div class="initial">{{source_initial}}</div><div><div class="author">{{author}}</div><div class="handle">{{source_caption}}</div></div></div><div class="ring"></div><div class="triangle"></div><h1>{{title1}}<br><em>{{title2}}</em><br>{{title3}}</h1><p class="summary">{{summary}}</p><div class="tags"><span>{{tag1}}</span><span>{{tag2}}</span></div></main></body></html>
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

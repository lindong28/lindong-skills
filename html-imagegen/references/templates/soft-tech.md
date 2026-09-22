## 执行方式

本 Prompt 依赖 skill html-imagegen（公开仓 https://github.com/lindong28/lindong-skills 的 html-imagegen/ 目录）；模板页 https://prompts.aiplanet.live/image/soft-tech/ 。执行者若尚未安装，先 git clone 该仓库，把 html-imagegen/ 放到 Claude Code 的 ~/.claude/skills/ 或 Codex 的 ~/.agents/skills/，首次运行按其 SKILL.md 安装浏览器依赖。然后按该 skill 的流程执行：本节之外的内容是本次模板与输入，「内容与素材」里的占位符是尚未给出的输入——只向用户询问仍缺的信息（至少是要表达的内容与目标平台或画幅），补齐后生成 HTML 并导出 PNG。

## 角色与任务

你是中文封面编辑与排版设计师。依据本次内容素材提炼中心主张，沿用下方视觉种子制作一张封面，输出完整可渲染的HTML。

## 基本要求

输出独立完整 HTML，唯一导出区域 id="cover"，画布600×800像素、3:4、直角外轮廓和不透明底板。通过浏览器原生截图导出600×800不透明PNG，不靠成图裁切、缩放或拉伸修复排版。内容忠实于本次输入，保留事实含义与来源归属；转述不冒充原话，缺失来源不虚构。内容作为文本或属性值时正确进行HTML转义。文字完整可读、不重叠、不越界，不以隐藏、截断或省略号遮盖溢出。CSS、装饰和必要脚本已内嵌；使用系统字体，不依赖仓库文件或外部脚本。

## 视觉要求

薰衣草近白背景配淡紫色圆弧，顶部白色大圆角卡片承载紫色图标、标题、摘要和小胶囊，下方较矮的圆角说明卡，左下来源与右下可选标签形成收尾。种子主卡左39px、上39px、宽522px、高301px，标题24px；这些像素、两行标题与胶囊数量是起点，按素材调整卡片和间距。保留柔和双卡层级与留白，说明可增减，转述不用引号冒充原话。

种子是排版起点，不是不可变的填槽表。保持本款风格与核心构图，按内容调整文字模块、数量、换行、字号、行距、间距和模块尺寸；代码中的像素值、行数及槽位数量均为起始值，不是硬内容预算。提炼一个清楚的中心主张，再选择支撑它的必要信息；不为填满空槽捏造事实、引语、标签、英文、账号、期号或步骤。无内容依据的可选模块及其分隔符一并移除，保留有意的留白，不用重复文案填空间。

下面是自包含的完整HTML种子，请依据以上原则适配内容后输出：

```html
<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>封面</title><style>*{box-sizing:border-box}html,body{margin:0}body{font-family:"PingFang SC","Microsoft YaHei",Arial,sans-serif}#cover{width:600px;height:800px;position:relative;overflow:hidden}h1,h2,p{margin:0}#cover{background:#f7f3fe;color:#343434}.wash{position:absolute;border-radius:50%;width:360px;height:360px;background:#eee8f7;right:-180px;top:-180px}.wash.bottom{left:-200px;top:670px;right:auto}.main{position:absolute;left:39px;top:39px;width:522px;height:301px;border-radius:23px;background:#ffffffed;padding:24px;box-shadow:0 10px 25px #63537907}.icon{width:48px;height:48px;border-radius:15px;background:#8d7adc;color:#fff;font-size:25px;display:flex;align-items:center;justify-content:center;margin-bottom:15px}h1{font-size:24px;line-height:1.32;font-weight:750;letter-spacing:-.45px}.summary{font-size:17px;line-height:1.48;color:#737373;margin-top:10px}.summary strong{color:#8b79df;font-weight:700}.tags{display:flex;gap:9px;position:absolute;left:24px;bottom:24px}.tags span{padding:7px 12px;background:#f2e4fd;color:#9078df;border-radius:18px;font-size:13px;font-weight:650}.note{position:absolute;left:39px;top:364px;width:522px;height:112px;border-radius:23px;background:#ffffffed;padding:25px;font-size:17px;line-height:1.55;color:#707070}.source{position:absolute;left:39px;top:685px;display:flex;align-items:center;gap:12px}.avatar{width:59px;height:59px;background:linear-gradient(135deg,#9786dc,#e9bbd6);border-radius:19px;display:flex;align-items:center;justify-content:center;font-size:27px;font-weight:700;color:white}.author{font-size:18px;font-weight:700}.caption{font-size:15px;color:#777;margin-top:5px}.foot{position:absolute;right:32px;bottom:30px;padding:8px 14px;border-radius:20px;background:#ffffffc9;font-size:13px;font-weight:650}</style></head><body><main id="cover"><div class="wash"></div><div class="wash bottom"></div><section class="main"><div class="icon">▤</div><h1>{{title}}</h1><p class="summary">{{summary_before}}<strong>{{summary_emphasis}}</strong>{{summary_after}}</p><div class="tags"><span>{{tag1}}</span><span>{{tag2}}</span><span>{{tag3}}</span></div></section><section class="note">{{note}}</section><footer class="source"><div class="avatar">{{source_initial}}</div><div><div class="author">{{author}}</div><div class="caption">{{source_caption}}</div></div></footer><div class="foot">{{footer_tags}}</div></main></body></html>
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

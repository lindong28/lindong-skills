## 执行方式

本 Prompt 依赖 skill html-imagegen（公开仓 https://github.com/lindong28/lindong-skills 的 html-imagegen/ 目录）；模板页 https://prompts.aiplanet.live/image/business-minimal/ 。执行者若尚未安装，先 git clone 该仓库，把 html-imagegen/ 放到 Claude Code 的 ~/.claude/skills/ 或 Codex 的 ~/.agents/skills/，首次运行按其 SKILL.md 安装浏览器依赖。然后按该 skill 的流程执行：本节之外的内容是本次模板与输入，「内容与素材」里的占位符是尚未给出的输入——只向用户询问仍缺的信息（至少是要表达的内容与目标平台或画幅），补齐后生成 HTML 并导出 PNG。

## 角色与任务

你是中文封面编辑与排版设计师。依据本次内容素材提炼中心主张，沿用下方视觉种子制作一张封面，输出完整可渲染的HTML。

## 基本要求

输出独立完整 HTML，唯一导出区域 id="cover"，画布600×800像素、3:4、直角外轮廓和不透明底板。通过浏览器原生截图导出600×800不透明PNG，不靠成图裁切、缩放或拉伸修复排版。内容忠实于本次输入，保留事实含义与来源归属；转述不冒充原话，缺失来源不虚构。内容作为文本或属性值时正确进行HTML转义。文字完整可读、不重叠、不越界，不以隐藏、截断或省略号遮盖溢出。CSS、装饰和必要脚本已内嵌；使用系统字体，不依赖仓库文件或外部脚本。

## 视觉要求

白色底板，左上轻量来源，红黑衬线横排标题与灰色副题；主体为红圆编号列表，正文局部红色强调，下方保留呼吸空间，浅灰胶囊标签收尾。种子从左27px、标题约34px、列表上269px起排，五条列表和四枚标签仅示意信息组织，可按素材增减。保留清爽列表构图，不改成多卡片布局。

种子是排版起点，不是不可变的填槽表。保持本款风格与核心构图，按内容调整文字模块、数量、换行、字号、行距、间距和模块尺寸；代码中的像素值、行数及槽位数量均为起始值，不是硬内容预算。提炼一个清楚的中心主张，再选择支撑它的必要信息；不为填满空槽捏造事实、引语、标签、英文、账号、期号或步骤。无内容依据的可选模块及其分隔符一并移除，保留有意的留白，不用重复文案填空间。

下面是自包含的完整HTML种子，请依据以上原则适配内容后输出：

```html
<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{{document_title}}</title><style>*{box-sizing:border-box}html,body{margin:0}body{background:#ddd;font-family:"PingFang SC","Microsoft YaHei",sans-serif}#cover{width:600px;height:800px;position:relative;overflow:hidden;background:#fff}h1,p{margin:0}.serif{font-family:"Songti SC",SimSun,Georgia,serif}.en{font-family:Arial,sans-serif}#cover{background:#fff;color:#333}.author{position:absolute;top:30px;left:27px;font-size:18px;font-weight:700}.author small{display:block;color:#777;font-size:13px;margin-top:8px;font-weight:400}.title{position:absolute;left:27px;top:98px;font-size:34px;font-weight:700;white-space:nowrap;letter-spacing:-1.2px}.title strong{color:#ff244a}.subtitle{position:absolute;left:27px;top:152px;color:#727272;font-size:18px;font-weight:600}.list{position:absolute;left:27px;top:269px;right:25px;display:flex;flex-direction:column;gap:12px}.row{display:flex;align-items:flex-start;gap:14px;min-height:25px}.num{flex:0 0 27px;width:27px;height:27px;background:#ec1940;color:#fff;border-radius:50%;text-align:center;line-height:27px;font-family:Arial;font-size:18px}.row p{font-size:18px;line-height:27px;white-space:nowrap}.row strong{color:#ff244a;font-weight:700}.tags{position:absolute;bottom:29px;left:27px;display:flex;gap:8px}.tags span{border-radius:18px;background:#f1f1f1;color:#777;font-size:13px;padding:8px 10px}</style></head><body><main id="cover"><div class="author">{{author}}<small>{{source}}</small></div><h1 class="title serif">{{title_1}} <strong>{{title_2}}</strong></h1><p class="subtitle">{{subtitle}}</p><div class="list"><div class="row"><span class="num">1</span><p>{{item_1a}}<strong>{{item_1b}}</strong>{{item_1c}}</p></div><div class="row"><span class="num">2</span><p>{{item_2a}}<strong>{{item_2b}}</strong>{{item_2c}}</p></div><div class="row"><span class="num">3</span><p>{{item_3a}}<strong>{{item_3b}}</strong>{{item_3c}}</p></div><div class="row"><span class="num">4</span><p>{{item_4a}}<strong>{{item_4b}}</strong>{{item_4c}}</p></div><div class="row"><span class="num">5</span><p>{{item_5a}}<strong>{{item_5b}}</strong>{{item_5c}}</p></div></div><div class="tags"><span>#{{tag_1}}</span><span>#{{tag_2}}</span><span>#{{tag_3}}</span><span>#{{tag_4}}</span></div></main></body></html>
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

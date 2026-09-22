## 执行方式

本 Prompt 依赖 skill html-imagegen（公开仓 https://github.com/lindong28/lindong-skills 的 html-imagegen/ 目录）。执行者若尚未安装，先 git clone 该仓库，把 html-imagegen/ 放到 Claude Code 的 ~/.claude/skills/ 或 Codex 的 ~/.agents/skills/，首次运行按其 SKILL.md 安装浏览器依赖。然后按该 skill 的流程执行：本节之外的内容是本次模板与输入，「内容与素材」里的占位符是尚未给出的输入——只向用户询问仍缺的信息（至少是要表达的内容与目标平台或画幅），补齐后生成 HTML 并导出 PNG。

## 角色与任务

你是中文封面编辑与排版设计师。依据本次内容素材提炼中心主张，沿用下方视觉种子制作一张封面，输出完整可渲染的HTML。

## 基本要求

输出独立完整 HTML，唯一导出区域 id="cover"，画布600×800像素、3:4、直角外轮廓和不透明底板。通过浏览器原生截图导出600×800不透明PNG，不靠成图裁切、缩放或拉伸修复排版。内容忠实于本次输入，保留事实含义与来源归属；转述不冒充原话，缺失来源不虚构。内容作为文本或属性值时正确进行HTML转义。文字完整可读、不重叠、不越界，不以隐藏、截断或省略号遮盖溢出。CSS、装饰和必要脚本已内嵌；使用系统字体，不依赖仓库文件或外部脚本。

## 视觉要求

近白全幅底与极淡白弧光，上沿黑细条及右上斜角；左侧可选竖排注记，上半幅留白，中部偏下标题交替裸字、黑底反白、细框三种字块处理，下接箭头引导语和小编号要点。种子从左84px、上296px、61px起排；三层标题、三条要点和行距均为起点，可合并或增减文字模块，保留票券式黑白层次，不强制三字标题或固定内容预算。

种子是排版起点，不是不可变的填槽表。保持本款风格与核心构图，按内容调整文字模块、数量、换行、字号、行距、间距和模块尺寸；代码中的像素值、行数及槽位数量均为起始值，不是硬内容预算。提炼一个清楚的中心主张，再选择支撑它的必要信息；不为填满空槽捏造事实、引语、标签、英文、账号、期号或步骤。无内容依据的可选模块及其分隔符一并移除，保留有意的留白，不用重复文案填空间。

下面是自包含的完整HTML种子，请依据以上原则适配内容后输出：

```html
<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><title>{{document_title}}</title><style>
*{box-sizing:border-box}body{margin:0;font-family:"PingFang SC","Microsoft YaHei",Arial,sans-serif}h1,p{margin:0}#cover{width:600px;height:800px;position:relative;overflow:hidden;background:#f5f5f5;color:#080909}.wash{position:absolute;inset:0;background:linear-gradient(164deg,#fff8,transparent 37%,#fff3 62%,transparent)}.orbit{position:absolute;left:0;top:172px;width:640px;height:440px;border:3px solid #ffffff65;border-radius:50%;transform:rotate(-15deg);box-shadow:0 8px 2px #ffffff45}.topbar{position:absolute;top:0;left:0;right:0;height:11px;background:#060707}.topbar:after{content:"";position:absolute;right:0;top:10px;border-left:30px solid transparent;border-top:30px solid #060707}.header{position:absolute;left:32px;right:32px;top:18px;border-bottom:1px solid #111;padding-bottom:12px;display:flex;justify-content:space-between;align-items:center}.author{font-size:15px;font-weight:750}.source{font-size:11px;color:#555;letter-spacing:1px}.vertical{position:absolute;left:43px;top:78px;writing-mode:vertical-rl;font-size:13px;letter-spacing:3px;color:#888}.title{position:absolute;left:84px;top:296px;font-size:61px;line-height:1.13;letter-spacing:-1px;font-weight:900}.title span{display:table;white-space:nowrap}.title .reverse{background:#070808;color:#fff;padding:0 9px}.title .outline{border:1px solid #080909;padding:0 4px;margin-left:-2px}.subtitle{position:absolute;left:84px;top:535px;display:flex;align-items:center;gap:10px;font-size:23px;font-weight:700}.arrow{font-size:32px;font-weight:400}.points{position:absolute;left:84px;top:597px;right:40px}.point{display:flex;gap:19px;margin-bottom:17px;font-size:16px;white-space:nowrap;line-height:1.3}.num{font-size:16px;font-weight:650;width:17px;flex:none}.point b{font-weight:750}.tail{position:absolute;left:84px;bottom:45px;font-size:10px;color:#888;letter-spacing:1px}
</style></head><body><main id="cover"><div class="wash"></div><div class="orbit"></div><div class="topbar"></div><header class="header"><span class="author">{{author}}</span><span class="source">{{source}}</span></header><div class="vertical">{{vertical}}</div><h1 class="title"><span>{{title_1}}</span><span class="reverse">{{title_2}}</span><span class="outline">{{title_3}}</span></h1><div class="subtitle"><span class="arrow">→</span><span>{{subtitle}}</span></div><div class="points"><p class="point"><span class="num">01</span><span><b>{{key_1}}</b> · {{point_1}}</span></p><p class="point"><span class="num">02</span><span><b>{{key_2}}</b> · {{point_2}}</span></p><p class="point"><span class="num">03</span><span><b>{{key_3}}</b> · {{point_3}}</span></p></div><p class="tail">{{tail}}</p></main></body></html>
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

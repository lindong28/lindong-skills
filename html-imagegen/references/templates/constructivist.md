## 执行方式

本 Prompt 依赖 skill html-imagegen（公开仓 https://github.com/lindong28/lindong-skills 的 html-imagegen/ 目录）；模板页 https://prompts.aiplanet.live/image/constructivist/ 。执行者若尚未安装，先 git clone 该仓库，把 html-imagegen/ 放到 Claude Code 的 ~/.claude/skills/ 或 Codex 的 ~/.agents/skills/，首次运行按其 SKILL.md 安装浏览器依赖。然后按该 skill 的流程执行：本节之外的内容是本次模板与输入，「内容与素材」里的占位符是尚未给出的输入——只向用户询问仍缺的信息（至少是要表达的内容与目标平台或画幅），补齐后生成 HTML 并导出 PNG。

## 角色与任务

你是中文封面编辑与排版设计师。依据本次内容素材提炼中心主张，沿用下方视觉种子制作一张封面，输出完整可渲染的HTML。

## 基本要求

输出独立完整 HTML，唯一导出区域 id="cover"，画布600×800像素、3:4、直角外轮廓和不透明底板。通过浏览器原生截图导出600×800不透明PNG，不靠成图裁切、缩放或拉伸修复排版。内容忠实于本次输入，保留事实含义与来源归属；转述不冒充原话，缺失来源不虚构。内容作为文本或属性值时正确进行HTML转义。文字完整可读、不重叠、不越界，不以隐藏、截断或省略号遮盖溢出。CSS、装饰和必要脚本已内嵌；使用系统字体，不依赖仓库文件或外部脚本。

## 视觉要求

浅灰方格底，红色纵轴、右上黑色矩形叠红菱形；黑色大标题与红底白字标题块错位，下接副题；中下部大号浅灰编号与正文形成节奏，红侧线标签、三角形和底部通栏黑带收束。种子网格20px、主标题约72px/73px，编号段从上438px起排；这些尺寸、两段标题和三项列表是起点，不是字数或行数上限。标题需避开黑色图形，编号仅表示实际列出的要点，不能暗示素材没有的步骤。

种子是排版起点，不是不可变的填槽表。保持本款风格与核心构图，按内容调整文字模块、数量、换行、字号、行距、间距和模块尺寸；代码中的像素值、行数及槽位数量均为起始值，不是硬内容预算。提炼一个清楚的中心主张，再选择支撑它的必要信息；不为填满空槽捏造事实、引语、标签、英文、账号、期号或步骤。无内容依据的可选模块及其分隔符一并移除，保留有意的留白，不用重复文案填空间。

下面是自包含的完整HTML种子，请依据以上原则适配内容后输出：

```html
<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><title>{{document_title}}</title><style>
*{box-sizing:border-box}body{margin:0;font-family:"PingFang SC","Microsoft YaHei",Arial,sans-serif}h1,h2,p{margin:0}#cover{width:600px;height:800px;position:relative;overflow:hidden;background:#f3f4f3;color:#040505;background-image:linear-gradient(#1111110d 1px,transparent 1px),linear-gradient(90deg,#1111110d 1px,transparent 1px);background-size:20px 20px}.axis-corner{position:absolute;left:22px;top:24px;width:40px;height:40px;border-left:3px solid #ff315c;border-top:3px solid #ff315c}.axis-x,.axis-y{position:absolute;color:#aaa;font-size:9px;font-weight:600}.axis-x{left:40px;top:15px}.axis-y{left:22px;top:34px;writing-mode:vertical-rl;transform:rotate(180deg)}.axis{position:absolute;left:31px;top:122px;bottom:116px;width:3px;background:#ff315c}.black{position:absolute;right:0;top:34px;width:240px;height:200px;background:#030404}.diamond{position:absolute;top:123px;right:50px;width:49px;height:49px;border:3px solid #ff315c;transform:rotate(45deg)}.title{position:absolute;left:40px;top:116px;font-size:72px;font-weight:900;line-height:1.13;letter-spacing:-2px;white-space:nowrap}.title-2{position:absolute;left:36px;top:210px;background:#ff2857;color:#fff;font-size:73px;line-height:1.15;letter-spacing:1px;padding:0 12px;font-weight:900;transform:skew(-4deg)}.title-2 span{display:block;transform:skew(4deg)}.subtitle{position:absolute;left:41px;top:321px;font-size:23px;font-weight:800;white-space:nowrap}.vertical{position:absolute;right:18px;top:323px;writing-mode:vertical-rl;font-size:13px;letter-spacing:3px;color:#777}.circle{position:absolute;right:41px;top:363px;width:80px;height:80px;border:3px solid #050505;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:22px;font-weight:700}.steps{position:absolute;left:100px;right:102px;top:438px}.step{display:flex;gap:15px;align-items:flex-start;min-height:69px}.num{font-size:44px;color:#0002;font-weight:800;line-height:1;width:47px;flex:none}.step p{font-size:19px;line-height:1.5;font-weight:500;padding-top:2px}.triangle{position:absolute;right:68px;top:562px;border-left:25px solid transparent;border-right:25px solid transparent;border-bottom:40px solid #ff5676}.tags{position:absolute;top:647px;left:41px;display:flex;gap:10px}.tags span{background:#0000000c;border-left:3px solid #ff315c;padding:8px 12px;font-size:14px;font-weight:700}.divider{position:absolute;top:697px;left:0;right:0;height:15px;background:#050505}.footer{position:absolute;left:41px;right:40px;top:752px;display:flex;justify-content:space-between;align-items:center}.author{font-size:17px;font-weight:800}.source{font-size:13px;color:#ff315c;font-weight:600}
</style></head><body><main id="cover"><div class="axis-corner"></div><div class="axis"></div><div class="black"></div><div class="diamond"></div><h1 class="title">{{title_1}}</h1><h2 class="title-2"><span>{{title_2}}</span></h2><p class="subtitle">{{subtitle}}</p><div class="vertical">{{vertical}}</div><div class="circle" aria-hidden="true"></div><div class="steps"><div class="step"><span class="num">01</span><p>{{point_1}}</p></div><div class="step"><span class="num">02</span><p>{{point_2}}</p></div><div class="step"><span class="num">03</span><p>{{point_3}}</p></div></div><div class="triangle"></div><div class="tags"><span>{{tag_1}}</span><span>{{tag_2}}</span><span>{{tag_3}}</span></div><div class="divider"></div><footer class="footer"><span class="author">{{author}}</span><span class="source">{{source}}</span></footer></main></body></html>
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

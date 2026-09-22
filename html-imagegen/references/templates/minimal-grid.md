## 执行方式

本 Prompt 依赖 skill html-imagegen（公开仓 https://github.com/lindong28/lindong-skills 的 html-imagegen/ 目录）。执行者若尚未安装，先 git clone 该仓库，把 html-imagegen/ 放到 Claude Code 的 ~/.claude/skills/ 或 Codex 的 ~/.agents/skills/，首次运行按其 SKILL.md 安装浏览器依赖。然后按该 skill 的流程执行：本节之外的内容是本次模板与输入，「内容与素材」里的占位符是尚未给出的输入——只向用户询问仍缺的信息（至少是要表达的内容与目标平台或画幅），补齐后生成 HTML 并导出 PNG。

## 角色与任务

你是中文封面编辑与排版设计师。依据本次内容素材提炼中心主张，沿用下方视觉种子制作一张封面，输出完整可渲染的HTML。

## 基本要求

输出独立完整 HTML，唯一导出区域 id="cover"，画布600×800像素、3:4、直角外轮廓和不透明底板。通过浏览器原生截图导出600×800不透明PNG，不靠成图裁切、缩放或拉伸修复排版。内容忠实于本次输入，保留事实含义与来源归属；转述不冒充原话，缺失来源不虚构。内容作为文本或属性值时正确进行HTML转义。文字完整可读、不重叠、不越界，不以隐藏、截断或省略号遮盖溢出。CSS、装饰和必要脚本已内嵌；使用系统字体，不依赖仓库文件或外部脚本。

## 视觉要求

黑色全幅底，150×200px细灰网格与低对比椭圆弧光；左对齐超粗大标题下沿穿绿色强调线，左上小标签、灰色副题、绿色点状要点与底部来源；右上细方框、右下绿圆及斜线保持低密度。种子标题从左40px、上164px、98px起排，两行标题及三个要点只是起点。保留黑底、巨大文字与少量绿点的关系，依据内容调整换行、要点数量和字号。

种子是排版起点，不是不可变的填槽表。保持本款风格与核心构图，按内容调整文字模块、数量、换行、字号、行距、间距和模块尺寸；代码中的像素值、行数及槽位数量均为起始值，不是硬内容预算。提炼一个清楚的中心主张，再选择支撑它的必要信息；不为填满空槽捏造事实、引语、标签、英文、账号、期号或步骤。无内容依据的可选模块及其分隔符一并移除，保留有意的留白，不用重复文案填空间。

下面是自包含的完整HTML种子，请依据以上原则适配内容后输出：

```html
<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><title>{{document_title}}</title><style>
*{box-sizing:border-box}body{margin:0;font-family:"PingFang SC","Microsoft YaHei",Arial,sans-serif}#cover{width:600px;height:800px;position:relative;overflow:hidden;background:#030403;color:#fff}h1,p{margin:0}.grid{position:absolute;inset:0;background-image:linear-gradient(90deg,#ffffff12 1px,transparent 1px),linear-gradient(#ffffff12 1px,transparent 1px);background-size:150px 200px}.haze{position:absolute;inset:0;background:linear-gradient(165deg,transparent 2%,#ffffff0c 8%,transparent 16%,#ffffff0a 20%,transparent 27%)}.orbit{position:absolute;left:12px;top:149px;width:590px;height:465px;border:2px solid #ffffff05;border-radius:50%;transform:rotate(-12deg);box-shadow:0 5px 4px #ffffff06,0 12px 5px #ffffff03,0 22px 6px #ffffff04}.orbit.second{transform:rotate(16deg);top:176px}.chip{position:absolute;left:40px;top:41px;padding:7px 12px;background:#ffffff16;font-size:16px;font-weight:800;letter-spacing:2px}.dot{position:absolute;left:80px;top:81px;width:10px;height:10px;border-radius:50%;background:#4bad55}.square{position:absolute;top:101px;right:59px;width:120px;height:120px;border:1px solid #ffffff30}.square:after{content:"";position:absolute;top:79px;left:59px;width:80px;height:1px;background:#ffffff30}.title{position:absolute;left:40px;top:164px;font-size:98px;line-height:1.02;letter-spacing:-2px;font-weight:900;white-space:nowrap;z-index:2}.title:before{content:"";position:absolute;left:0;top:88px;width:295px;height:14px;background:#235c2d;z-index:-1}.subtitle{position:absolute;top:392px;left:40px;font-size:28px;font-weight:300;color:#cacaca;white-space:nowrap}.points{position:absolute;top:483px;left:40px;display:flex;gap:26px;font-size:19px;color:#bcbcbc}.points span:before{content:"";display:inline-block;width:6px;height:6px;background:#55b961;margin-right:9px}.circle{position:absolute;top:561px;left:461px;width:40px;height:40px;border:1px solid #51b858;border-radius:50%}.diag{position:absolute;top:614px;left:55px;width:100px;height:1px;background:#ffffff30;transform-origin:left;transform:rotate(45deg)}.footer{position:absolute;left:40px;top:698px}.author{font-size:21px;font-weight:750}.author:before{content:"";display:inline-block;width:8px;height:8px;background:#55b961;border-radius:50%;margin-right:12px}.source{font-size:15px;color:#999;margin-top:14px}.footer:after{content:"";position:absolute;left:290px;top:19px;height:27px;border-left:1px solid #51b858}
</style></head><body><main id="cover"><div class="grid"></div><div class="haze"></div><div class="orbit"></div><div class="orbit second"></div><div class="chip">{{kicker}}</div><div class="dot"></div><div class="square"></div><h1 class="title">{{title_1}}<br>{{title_2}}</h1><p class="subtitle">{{subtitle}}</p><div class="points"><span>{{point_1}}</span><span>{{point_2}}</span><span>{{point_3}}</span></div><div class="circle"></div><div class="diag"></div><footer class="footer"><p class="author">{{author}}</p><p class="source">{{source}}</p></footer></main></body></html>
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

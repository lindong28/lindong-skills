## 执行方式

本 Prompt 依赖 skill html-imagegen（公开仓 https://github.com/lindong28/lindong-skills 的 html-imagegen/ 目录）；模板页 https://prompts.aiplanet.live/image/soft-cute/ 。执行者若尚未安装，先 git clone 该仓库，把 html-imagegen/ 放到 Claude Code 的 ~/.claude/skills/ 或 Codex 的 ~/.agents/skills/，首次运行按其 SKILL.md 安装浏览器依赖。然后按该 skill 的流程执行：本节之外的内容是本次模板与输入，「内容与素材」里的占位符是尚未给出的输入——只向用户询问仍缺的信息（至少是要表达的内容与目标平台或画幅），补齐后生成 HTML 并导出 PNG。

## 角色与任务

你是中文封面编辑与排版设计师。依据本次内容素材提炼中心主张，沿用下方视觉种子制作一张封面，输出完整可渲染的HTML。

## 基本要求

输出独立完整 HTML，唯一导出区域 id="cover"，画布600×800像素、3:4、直角外轮廓和不透明底板。通过浏览器原生截图导出600×800不透明PNG，不靠成图裁切、缩放或拉伸修复排版。内容忠实于本次输入，保留事实含义与来源归属；转述不冒充原话，缺失来源不虚构。内容作为文本或属性值时正确进行HTML转义。文字完整可读、不重叠、不越界，不以隐藏、截断或省略号遮盖溢出。CSS、装饰和必要脚本已内嵌；使用系统字体，不依赖仓库文件或外部脚本。

## 视觉要求

粉色横线纸与左侧装订孔；上部珊瑚色标题、深色及紫色副题，居中白色圆角摘要卡与虚线胶囊标签；铅笔、便签、圆弧和小奖章点缀，中下部保留轻松留白，右下轻量来源。种子标题上57px、42px，摘要卡上219px；卡片高度、标签数量、换行可按内容调整。奖章仅作几何装饰，不写虚构排名；标点和语气随正文，不强制感叹句。

种子是排版起点，不是不可变的填槽表。保持本款风格与核心构图，按内容调整文字模块、数量、换行、字号、行距、间距和模块尺寸；代码中的像素值、行数及槽位数量均为起始值，不是硬内容预算。提炼一个清楚的中心主张，再选择支撑它的必要信息；不为填满空槽捏造事实、引语、标签、英文、账号、期号或步骤。无内容依据的可选模块及其分隔符一并移除，保留有意的留白，不用重复文案填空间。

下面是自包含的完整HTML种子，请依据以上原则适配内容后输出：

```html
<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{{document_title}}</title><style>*{box-sizing:border-box}html,body{margin:0}body{background:#ddd;font-family:"PingFang SC","Microsoft YaHei",sans-serif}#cover{width:600px;height:800px;position:relative;overflow:hidden;background:#fff}h1,p{margin:0}.serif{font-family:"Songti SC",SimSun,Georgia,serif}.en{font-family:Arial,sans-serif}#cover{background-color:#fff2f4;background-image:repeating-linear-gradient(0deg,transparent 0,transparent 25px,#decfd344 25px,#decfd344 26px);color:#353335}.holes{position:absolute;left:22px;top:125px;display:flex;flex-direction:column;gap:120px}.holes i{width:14px;height:14px;border:2px solid #ffcdd6;border-radius:50%}.orb{position:absolute;right:-47px;top:-42px;width:145px;height:145px;background:#ffdee7;border-radius:50%}.title{position:absolute;top:57px;left:80px;font-size:42px;line-height:1.2;color:#ff7891;font-weight:850;white-space:nowrap;text-shadow:3px 4px #ffd5df}.sub{position:absolute;top:164px;left:80px;font-size:26px;font-weight:800;white-space:nowrap}.sub em{font-style:normal;color:#a15edb}.summary{position:absolute;left:136px;top:219px;width:332px;height:96px;border-radius:25px;background:#ffffffcf;text-align:center;font-size:21px;line-height:1.65;padding:16px 8px;font-weight:650;box-shadow:0 6px 16px #b5818a09}.summary strong{color:#ff7891}.tags{position:absolute;left:183px;top:366px;display:flex;gap:12px}.tags span{border:2px dashed #ff8199;border-radius:24px;background:#fff;padding:10px 15px;color:#ff7891;font-size:18px;font-weight:700;white-space:nowrap}.pencil{position:absolute;right:96px;top:119px;width:48px;height:10px;border-radius:5px;background:#ffcf65;transform:rotate(30deg);border-right:8px solid #ff8e9f}.note{position:absolute;left:61px;top:600px;width:39px;height:42px;border-radius:8px;background:#fff;box-shadow:0 4px 8px #66444414;transform:rotate(-12deg)}.note:after{content:"";position:absolute;inset:11px;background:#ff8199;border-radius:3px}.credit{position:absolute;right:35px;bottom:50px;border-radius:25px;background:#ffffffbf;padding:16px 17px;font-size:16px;font-weight:650}.credit span{color:#a15edb}.medal{display:inline-block;margin-left:7px;background:#ffc04c;border:2px solid #efaa35;border-radius:50%;width:24px;height:24px;text-align:center;color:#935d2a}.corner{position:absolute;bottom:-22px;left:-27px;width:95px;height:95px;border-radius:50%;background:#e9cfef}</style></head><body><main id="cover"><div class="orb"></div><div class="holes"><i></i><i></i><i></i><i></i><i></i></div><h1 class="title">{{title}}</h1><div class="pencil"></div><p class="sub">{{sub_1}}<em>{{sub_2}}</em></p><div class="summary"><strong>{{summary_1}}</strong>{{summary_2}}<br>{{summary_3}}</div><div class="tags"><span># {{tag_1}}</span><span># {{tag_2}}</span></div><div class="note"></div><div class="corner"></div><div class="credit">{{author}} <span>{{credit}}</span><i class="medal" aria-hidden="true">✦</i></div></main></body></html>
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

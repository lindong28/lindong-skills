## 执行方式

本 Prompt 依赖 skill html-imagegen（公开仓 https://github.com/lindong28/lindong-skills 的 html-imagegen/ 目录）；模板页 https://prompts.aiplanet.live/image/industrial-rebel/ 。执行者若尚未安装，先 git clone 该仓库，把 html-imagegen/ 放到 Claude Code 的 ~/.claude/skills/ 或 Codex 的 ~/.agents/skills/，首次运行按其 SKILL.md 安装浏览器依赖。然后按该 skill 的流程执行：本节之外的内容是本次模板与输入，「内容与素材」里的占位符是尚未给出的输入——只向用户询问仍缺的信息（至少是要表达的内容与目标平台或画幅），补齐后生成 HTML 并导出 PNG。

## 角色与任务

你是中文封面编辑与排版设计师。依据本次内容素材提炼中心主张，沿用下方视觉种子制作一张封面，输出完整可渲染的HTML。

## 基本要求

输出独立完整 HTML，唯一导出区域 id="cover"，画布600×800像素、3:4、直角外轮廓和不透明底板。通过浏览器原生截图导出600×800不透明PNG，不靠成图裁切、缩放或拉伸修复排版。内容忠实于本次输入，保留事实含义与来源归属；转述不冒充原话，缺失来源不虚构。内容作为文本或属性值时正确进行HTML转义。文字完整可读、不重叠、不越界，不以隐藏、截断或省略号遮盖溢出。CSS、装饰和必要脚本已内嵌；使用系统字体，不依赖仓库文件或外部脚本。

## 视觉要求

黑色细网格底，左上荧黄与白色超粗标题斜错叠排，描边重影；大号短句用荧黄关键词块强调，荧黄横线构成来源或说明区域；下方保留线框、点阵和弧形线稿。种子标题从上63px起，字号约74px/86px，强调短句上326px；保持粗粝工业感、亮暗对比与不对称构图。右侧竖排注记、编号和徽标可选，不为填它们编英文、期号或口号。

种子是排版起点，不是不可变的填槽表。保持本款风格与核心构图，按内容调整文字模块、数量、换行、字号、行距、间距和模块尺寸；代码中的像素值、行数及槽位数量均为起始值，不是硬内容预算。提炼一个清楚的中心主张，再选择支撑它的必要信息；不为填满空槽捏造事实、引语、标签、英文、账号、期号或步骤。无内容依据的可选模块及其分隔符一并移除，保留有意的留白，不用重复文案填空间。

下面是自包含的完整HTML种子，请依据以上原则适配内容后输出：

```html
<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{{document_title}}</title><style>*{box-sizing:border-box}html,body{margin:0}body{background:#ddd;font-family:"PingFang SC","Microsoft YaHei",sans-serif}#cover{width:600px;height:800px;position:relative;overflow:hidden;background:#fff}h1,p{margin:0}.serif{font-family:"Songti SC",SimSun,Georgia,serif}.en{font-family:Arial,sans-serif}#cover{background-color:#101110;background-image:linear-gradient(#ffffff09 1px,transparent 1px),linear-gradient(90deg,#ffffff09 1px,transparent 1px);background-size:24px 24px;color:#fff}.topline{position:absolute;left:45px;top:63px;font-size:74px;line-height:1.1;font-weight:950;color:#f3ff00;transform:skew(-7deg)}.big{position:absolute;top:139px;left:45px;font-size:86px;line-height:1.05;letter-spacing:-5px;font-weight:950;transform:rotate(-3deg);text-shadow:4px 9px #101110,5px 10px #a5ae00}.no{position:absolute;right:48px;top:40px;border:1px solid #c2cb00;color:#d8de00;padding:9px 13px;font:16px Arial}.rail{position:absolute;right:49px;top:148px;writing-mode:vertical-rl;font:24px Arial;letter-spacing:3px;color:#aaa}.intro{position:absolute;left:50px;top:279px;font-size:22px;color:#ddd}.slogan{position:absolute;left:45px;top:326px;font-size:46px;font-weight:800;white-space:nowrap}.slogan strong{display:inline-block;background:#f4ff00;color:#090909;padding:8px 9px;transform:skew(-5deg);margin:0 3px}.source{position:absolute;left:45px;top:433px;width:507px;border-top:1px solid #ecf600;border-bottom:1px solid #ecf600;padding:13px 0;font:italic bold 35px Arial;color:#f0ff00}.footer{position:absolute;left:47px;bottom:70px;font-size:20px}.badge{position:absolute;right:48px;bottom:65px;border:1px solid #effc00;padding:8px 12px;color:#effc00;transform:skew(-5deg);font-size:18px}.box{position:absolute;left:-40px;top:538px;width:170px;height:120px;border:1px solid #7a7d19;transform:rotate(31deg)}.dot{position:absolute;right:155px;top:559px;width:100px;height:125px;background-image:radial-gradient(#5b6100 1px,transparent 1px);background-size:10px 10px}.fish{position:absolute;right:81px;top:570px;width:65px;height:32px;border-top:2px solid #efff00;border-radius:50%;transform:rotate(10deg)}.fish:after{content:"";position:absolute;left:-8px;top:4px;width:16px;height:16px;border-left:2px solid #efff00;border-bottom:2px solid #efff00;transform:rotate(30deg)}</style></head><body><main id="cover"><div class="topline">{{title_1}}</div><h1 class="big">{{title_2}}</h1><div class="no">{{编号，可选}}</div><div class="rail">{{rail}}</div><p class="intro">— {{intro}}</p><div class="slogan">{{before}}<strong>{{highlight}}</strong>{{after}}</div><div class="source">{{source}}</div><div class="box"></div><div class="dot"></div><div class="fish"></div><div class="footer">{{footer}}</div><div class="badge">{{badge}}</div></main></body></html>
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

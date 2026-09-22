## 执行方式

本 Prompt 依赖 skill html-imagegen（公开仓 https://github.com/lindong28/lindong-skills 的 html-imagegen/ 目录）；模板页 https://prompts.aiplanet.live/image/swiss-international/ 。执行者若尚未安装，先 git clone 该仓库，把 html-imagegen/ 放到 Claude Code 的 ~/.claude/skills/ 或 Codex 的 ~/.agents/skills/，首次运行按其 SKILL.md 安装浏览器依赖。然后按该 skill 的流程执行：本节之外的内容是本次模板与输入，「内容与素材」里的占位符是尚未给出的输入——只向用户询问仍缺的信息（至少是要表达的内容与目标平台或画幅），补齐后生成 HTML 并导出 PNG。

## 角色与任务

你是中文封面编辑与排版设计师。依据本次内容素材提炼中心主张，沿用下方视觉种子制作一张封面，输出完整可渲染的HTML。

## 基本要求

输出独立完整 HTML，唯一导出区域 id="cover"，画布600×800像素、3:4、直角外轮廓和不透明底板。通过浏览器原生截图导出600×800不透明PNG，不靠成图裁切、缩放或拉伸修复排版。内容忠实于本次输入，保留事实含义与来源归属；转述不冒充原话，缺失来源不虚构。内容作为文本或属性值时正确进行HTML转义。文字完整可读、不重叠、不越界，不以隐藏、截断或省略号遮盖溢出。CSS 和必要脚本已内嵌，不依赖仓库文件或外部脚本；字体通过明确列出的 Google Fonts 字体URL联网加载。导出前等待字体就绪；加载失败时告知使用者并确认替代字体，不把回退字体冒充原字体。

## 视觉要求

采用 S01 Accent Cover 的通用标题与引导语/要点起点：米白底、IKB Blue 单一强调色、极轻无衬线大标题（字重200）、左对齐、直角模块与细线秩序。以一个中心概念统领标题和可选引导语，必要时用蓝色信息块放要点，底部细线承托可选来源。保留工程式秩序和字号对比；不绑定具体题材，不强制流程图、两个节点或输入输出关系。

种子是排版起点，不是不可变的填槽表。保持本款风格与核心构图，按内容调整文字模块、数量、换行、字号、行距、间距和模块尺寸；代码中的像素值、行数及槽位数量均为起始值，不是硬内容预算。提炼一个清楚的中心主张，再选择支撑它的必要信息；不为填满空槽捏造事实、引语、标签、英文、账号、期号或步骤。无内容依据的可选模块及其分隔符一并移除，保留有意的留白，不用重复文案填空间。

下面是自包含的完整HTML种子，请依据以上原则适配内容后输出：

```html
<!doctype html>
<html lang="zh-CN" data-accent="ikb">
<head>
  <meta charset="utf-8">
  <title>{{页面标题}}</title>
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <style>

@font-face {
  font-family: 'IBM Plex Mono';
  font-style: normal;
  font-weight: 400;
  font-display: swap;
  src: url(https://fonts.gstatic.com/s/ibmplexmono/v20/-F63fjptAgt5VM-kVkqdyU8n5ig.ttf) format('truetype');
}
@font-face {
  font-family: 'IBM Plex Mono';
  font-style: normal;
  font-weight: 500;
  font-display: swap;
  src: url(https://fonts.gstatic.com/s/ibmplexmono/v20/-F6qfjptAgt5VM-kVkqdyU8n3twJ8lc.ttf) format('truetype');
}
@font-face {
  font-family: 'IBM Plex Mono';
  font-style: normal;
  font-weight: 600;
  font-display: swap;
  src: url(https://fonts.gstatic.com/s/ibmplexmono/v20/-F6qfjptAgt5VM-kVkqdyU8n3vAO8lc.ttf) format('truetype');
}
@font-face {
  font-family: 'Inter';
  font-style: normal;
  font-weight: 200;
  font-display: swap;
  src: url(https://fonts.gstatic.com/s/inter/v20/UcCO3FwrK3iLTeHuS_nVMrMxCp50SjIw2boKoduKmMEVuDyfMZg.ttf) format('truetype');
}
@font-face {
  font-family: 'Inter';
  font-style: normal;
  font-weight: 300;
  font-display: swap;
  src: url(https://fonts.gstatic.com/s/inter/v20/UcCO3FwrK3iLTeHuS_nVMrMxCp50SjIw2boKoduKmMEVuOKfMZg.ttf) format('truetype');
}
@font-face {
  font-family: 'Inter';
  font-style: normal;
  font-weight: 400;
  font-display: swap;
  src: url(https://fonts.gstatic.com/s/inter/v20/UcCO3FwrK3iLTeHuS_nVMrMxCp50SjIw2boKoduKmMEVuLyfMZg.ttf) format('truetype');
}
@font-face {
  font-family: 'Inter';
  font-style: normal;
  font-weight: 500;
  font-display: swap;
  src: url(https://fonts.gstatic.com/s/inter/v20/UcCO3FwrK3iLTeHuS_nVMrMxCp50SjIw2boKoduKmMEVuI6fMZg.ttf) format('truetype');
}
@font-face {
  font-family: 'Inter';
  font-style: normal;
  font-weight: 600;
  font-display: swap;
  src: url(https://fonts.gstatic.com/s/inter/v20/UcCO3FwrK3iLTeHuS_nVMrMxCp50SjIw2boKoduKmMEVuGKYMZg.ttf) format('truetype');
}
@font-face {
  font-family: 'Inter';
  font-style: normal;
  font-weight: 700;
  font-display: swap;
  src: url(https://fonts.gstatic.com/s/inter/v20/UcCO3FwrK3iLTeHuS_nVMrMxCp50SjIw2boKoduKmMEVuFuYMZg.ttf) format('truetype');
}
@font-face {
  font-family: 'Noto Sans SC';
  font-style: normal;
  font-weight: 200;
  font-display: swap;
  src: url(https://fonts.gstatic.com/s/notosanssc/v40/k3kCo84MPvpLmixcA63oeAL7Iqp5IZJF9bmaG1_FnYw.ttf) format('truetype');
}
@font-face {
  font-family: 'Noto Sans SC';
  font-style: normal;
  font-weight: 300;
  font-display: swap;
  src: url(https://fonts.gstatic.com/s/notosanssc/v40/k3kCo84MPvpLmixcA63oeAL7Iqp5IZJF9bmaG4HFnYw.ttf) format('truetype');
}
@font-face {
  font-family: 'Noto Sans SC';
  font-style: normal;
  font-weight: 400;
  font-display: swap;
  src: url(https://fonts.gstatic.com/s/notosanssc/v40/k3kCo84MPvpLmixcA63oeAL7Iqp5IZJF9bmaG9_FnYw.ttf) format('truetype');
}
@font-face {
  font-family: 'Noto Sans SC';
  font-style: normal;
  font-weight: 500;
  font-display: swap;
  src: url(https://fonts.gstatic.com/s/notosanssc/v40/k3kCo84MPvpLmixcA63oeAL7Iqp5IZJF9bmaG-3FnYw.ttf) format('truetype');
}
@font-face {
  font-family: 'Noto Sans SC';
  font-style: normal;
  font-weight: 600;
  font-display: swap;
  src: url(https://fonts.gstatic.com/s/notosanssc/v40/k3kCo84MPvpLmixcA63oeAL7Iqp5IZJF9bmaGwHCnYw.ttf) format('truetype');
}
@font-face {
  font-family: 'Noto Sans SC';
  font-style: normal;
  font-weight: 700;
  font-display: swap;
  src: url(https://fonts.gstatic.com/s/notosanssc/v40/k3kCo84MPvpLmixcA63oeAL7Iqp5IZJF9bmaGzjCnYw.ttf) format('truetype');
}

</style>
  
  <style>
    

    
    :root,
    [data-accent="ikb"] {
      --paper: #fafaf8;
      --ink: #0a0a0a;
      --grey-1: #f0f0ee;
      --grey-2: #d4d4d2;
      --grey-3: #737373;
      --accent: #002FA7;
      --accent-on: #ffffff;
    }
    [data-accent="lemon-yellow"] {
      --paper: #fafaf8;
      --ink: #0a0a0a;
      --grey-1: #f0f0ee;
      --grey-2: #d4d4d2;
      --grey-3: #737373;
      --accent: #FFD500;
      --accent-on: #0a0a0a;
    }
    [data-accent="lemon-green"] {
      --paper: #fafaf8;
      --ink: #0a0a0a;
      --grey-1: #f0f0ee;
      --grey-2: #d4d4d2;
      --grey-3: #737373;
      --accent: #C5E803;
      --accent-on: #0a0a0a;
    }
    [data-accent="safety-orange"] {
      --paper: #fafaf8;
      --ink: #0a0a0a;
      --grey-1: #f0f0ee;
      --grey-2: #d4d4d2;
      --grey-3: #737373;
      --accent: #FF6B35;
      --accent-on: #ffffff;
    }

    
    :root {
      --sans:    "Inter", "Helvetica Neue", Helvetica, "Noto Sans SC",
                 -apple-system, "PingFang SC", "Microsoft YaHei UI", sans-serif;
      --sans-zh: "Noto Sans SC", -apple-system, "PingFang SC",
                 "Microsoft YaHei UI", "Inter", sans-serif;
      --mono:    "IBM Plex Mono", ui-monospace, "SF Mono", Consolas, monospace;
    }

    
    :root {
      --sp-3:   4.4444px;
      --sp-4:  6.6667px;
      --sp-5:  8.8889px;
      --sp-6:  13.3333px;
      --sp-7:  17.7778px;
      --sp-8:  22.2222px;
      --sp-9:  26.6667px;
      --sp-10: 35.5556px;
      --sp-11: 44.4444px;
      --sp-12: 53.3333px;
      --sp-13:88.8889px;
    }

    
    *,*::before,*::after { box-sizing: border-box; }
    html, body { margin: 0; padding: 0; }
    body {
      background: #1a1a1a;
      font-family: var(--sans);
      color: var(--ink);
      -webkit-font-smoothing: antialiased;
      -moz-osx-font-smoothing: grayscale;
      padding: 35.5556px 17.7778px;
    }
    .sheet {
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 26.6667px;
    }

    
    .poster {
      position: relative;
      background: var(--paper);
      color: var(--ink);
      overflow: hidden;
      isolation: isolate;
    }
    .poster.xhs    { width: 600px; height: 800px; }
    .poster.square { width: 600px; height: 600px; }
    .poster.wide   { width: 1166.6667px; height:  500px; }
    .poster figure { margin: 0; }

    .poster.xhs    .content { padding: var(--sp-12) var(--sp-11); }
    .poster.square .content { padding: var(--sp-11) var(--sp-11); }
    .poster.wide   .content { padding: var(--sp-11) var(--sp-13); }
    .content { position: relative; width: 100%; height: 100%; z-index: 2; }

    
    .dot-mat,
    .ring-mat,
    .cross-mat {
      position: absolute;
      inset: 0;
      pointer-events: none;
      z-index: 1;
    }
    .dot-mat {
      opacity: .08;
      background-image: radial-gradient(var(--ink) 0.8333px, transparent 0.8333px);
      background-size: 13.3333px 13.3333px;
    }
    .ring-mat {
      opacity: .08;
      background-image: radial-gradient(circle at 50% 50%, transparent 2.2222px, var(--ink) 2.5px, var(--ink) 2.7778px, transparent 3.0556px);
      background-size: 17.7778px 17.7778px;
    }
    .cross-mat {
      opacity: .06;
      background-image:
        linear-gradient(var(--ink), var(--ink)),
        linear-gradient(90deg, var(--ink), var(--ink));
      background-size: 0.5556px 7.7778px, 7.7778px 0.5556px;
      background-position: center, center;
      background-repeat: repeat;
    }

    
    .h-hero {
      font-family: var(--sans);
      font-weight: 200;
      font-size: 133.3333px;
      line-height: 1.02;
      letter-spacing: -.02em;
      margin: 0;
      color: var(--ink);
    }
    .h-statement {
      font-family: var(--sans);
      font-weight: 200;
      font-size: 100px;
      line-height: 1.05;
      letter-spacing: -.015em;
      margin: 0;
      color: var(--ink);
    }
    .h-xl {
      font-family: var(--sans);
      font-weight: 300;
      font-size: 66.6667px;
      line-height: 1.08;
      letter-spacing: -.01em;
      margin: 0;
      color: var(--ink);
    }
    .h-md {
      font-family: var(--sans);
      font-weight: 400;
      font-size: 31.1111px;
      line-height: 1.18;
      margin: 0;
      color: var(--ink);
    }
    .lead {
      font-family: var(--sans-zh);
      font-weight: 400;
      font-size: 16.6667px;
      line-height: 1.55;
      color: var(--ink);
      margin: 0;
    }
    .body {
      font-family: var(--sans-zh);
      font-weight: 400;
      font-size: 14.4444px;
      line-height: 1.6;
      color: var(--ink);
      margin: 0;
    }
    .t-cat {
      font-family: var(--sans);
      font-weight: 600;
      font-size: 12.2222px;
      letter-spacing: .08em;
      text-transform: uppercase;
      color: var(--accent);
      margin: 0;
    }
    .t-meta {
      font-family: var(--mono);
      font-weight: 500;
      font-size: 11.1111px;
      letter-spacing: .14em;
      text-transform: uppercase;
      color: var(--grey-3);
      margin: 0;
    }
    .num-mega {
      font-family: var(--sans);
      font-weight: 200;
      font-size: 111.1111px;
      line-height: .92;
      letter-spacing: -.03em;
      color: var(--ink);
      margin: 0;
    }
    .num-xl {
      font-family: var(--sans);
      font-weight: 200;
      font-size: 80px;
      line-height: .96;
      letter-spacing: -.02em;
      margin: 0;
    }
    .mono { font-family: var(--mono); }

    
    .poster.xhs .h-hero          { font-size: 93.3333px; }
    .poster.xhs .h-statement     { font-size: 68.8889px; }
    .poster.xhs .h-xl            { font-size: 53.3333px; }
    .poster.xhs .num-mega        { font-size: 93.3333px; }
    .poster.xhs .num-xl          { font-size: 66.6667px; }

    
    .poster.square .h-hero       { font-size: 100px; }
    .poster.square .h-statement  { font-size: 77.7778px; }
    .poster.square .h-xl         { font-size: 48.8889px; }
    .poster.square .num-mega     { font-size: 93.3333px; }
    .poster.square .num-xl       { font-size: 62.2222px; }

    
    .poster.wide .h-hero         { font-size: 111.1111px; }
    .poster.wide .h-statement    { font-size: 86.6667px; }
    .poster.wide .h-xl           { font-size: 57.7778px; }

    
    .stack    { display: flex; flex-direction: column; }
    .row      { display: flex; flex-direction: row; }
    .gap-3    { gap: var(--sp-3); }
    .gap-4    { gap: var(--sp-4); }
    .gap-5    { gap: var(--sp-5); }
    .gap-6    { gap: var(--sp-6); }
    .gap-7    { gap: var(--sp-7); }
    .gap-8    { gap: var(--sp-8); }
    .gap-9    { gap: var(--sp-9); }
    .gap-10   { gap: var(--sp-10); }
    .grow     { flex: 1; }
    .grid-12  { display: grid; grid-template-columns: repeat(12, 1fr); gap: var(--sp-7); }
    .grid-2-9 { display: grid; grid-template-columns: 1fr 1fr; gap: var(--sp-9); }
    .grid-3   { display: grid; grid-template-columns: repeat(3, 1fr); gap: var(--sp-7); }
    .grid-4   { display: grid; grid-template-columns: repeat(4, 1fr); gap: var(--sp-6); }
    .span-2   { grid-column: span 2; }
    .span-3   { grid-column: span 3; }
    .span-4   { grid-column: span 4; }
    .span-6   { grid-column: span 6; }
    .span-8   { grid-column: span 8; }
    .span-9   { grid-column: span 9; }
    .span-12  { grid-column: span 12; }
    .center   { text-align: center; }
    .right    { text-align: right; }
    .uppercase{ text-transform: uppercase; }
    .hr-hairline {
      height: 0.5556px;
      background: var(--grey-2);
      border: 0;
      margin: 0;
    }
    .hr-accent {
      height: 1.6667px;
      background: var(--accent);
      border: 0;
      width: 53.3333px;
      margin: 0;
    }

    
    .card-ink {
      background: var(--ink);
      color: var(--paper);
      padding: var(--sp-8);
    }
    .card-ink .t-cat,
    .card-ink .t-meta,
    .card-ink .lead,
    .card-ink .body,
    .card-ink .h-md { color: var(--paper); }
    .card-accent {
      background: var(--accent);
      color: var(--accent-on);
      padding: var(--sp-8);
    }
    .card-accent .t-cat,
    .card-accent .t-meta,
    .card-accent .lead,
    .card-accent .body,
    .card-accent .h-md { color: var(--accent-on); }
    .card-fill {
      background: var(--grey-1);
      color: var(--ink);
      padding: var(--sp-8);
    }
    .card-outlined {
      background: transparent;
      color: var(--ink);
      border: 0.5556px solid var(--grey-2);
      padding: var(--sp-8);
    }

    
    .frame-img {
      position: relative;
      overflow: hidden;
      background: var(--grey-1);
      display: block;
      margin: 0;
    }
    .frame-img img {
      width: 100%;
      height: 100%;
      object-fit: cover;
      object-position: center 35%;
      display: block;
    }
    .frame-img.fit-contain img { object-fit: contain; background: var(--paper); }
    .frame-img.r-3x4   { aspect-ratio: 3 / 4; }
    .frame-img.r-1x1   { aspect-ratio: 1 / 1; }
    .frame-img.r-4x3   { aspect-ratio: 4 / 3; }
    .frame-img.r-16x9  { aspect-ratio: 16 / 9; }
    .frame-img.r-16x10 { aspect-ratio: 16 / 10; }
    .frame-img.r-21x9  { aspect-ratio: 21 / 9; }
    .swiss-img-caption {
      font-family: var(--mono);
      font-weight: 500;
      font-size: 10px;
      letter-spacing: .12em;
      text-transform: uppercase;
      color: var(--grey-3);
      margin-top: var(--sp-5);
    }

    
    
    .frame-shot {
      position: relative;
      overflow: hidden;
      display: block;
      margin: 0;
      background: var(--grey-1);
      border-radius: 0;
    }
    .frame-shot.corners-sq { border-radius: 0; }
    .frame-shot.corners-sm { border-radius: 2.2222px; }
    .frame-shot.corners-md { border-radius: 5.5556px; }

    
    .frame-shot.shadow-soft { box-shadow: 0 6.6667px 15.5556px -16px rgba(0,0,0,.18); }
    .frame-shot.shadow-ed   { box-shadow: 0 11.1111px 22.2222px -20px rgba(0,0,0,.22), 0 0 0 0.5556px var(--grey-2); }

    
    .frame-shot.bg-paper    { background: var(--paper); }
    .frame-shot.bg-grey-1   { background: var(--grey-1); }
    .frame-shot.bg-ink      { background: var(--ink); }
    .frame-shot.bg-grid     {
      background-color: var(--paper);
      background-image:
        linear-gradient(to right, var(--grey-2) 0.5556px, transparent 0.5556px),
        linear-gradient(to bottom, var(--grey-2) 0.5556px, transparent 0.5556px);
      background-size: 26.6667px 26.6667px;
    }
    .frame-shot.bg-dot {
      background-color: var(--paper);
      background-image: radial-gradient(var(--grey-2) 0.5556px, transparent 0.5556px);
      background-size: 10px 10px;
    }

    

    .frame-shot.inset-none > img,
    .frame-shot.inset-none > .shot-body { padding: 0; }
    .frame-shot.inset-sub  { padding: 11.1111px; }
    .frame-shot.inset-bal  { padding: 26.6667px; }

    .frame-shot.r-3x4   { aspect-ratio: 3 / 4; }
    .frame-shot.r-1x1   { aspect-ratio: 1 / 1; }
    .frame-shot.r-4x3   { aspect-ratio: 4 / 3; }
    .frame-shot.r-16x9  { aspect-ratio: 16 / 9; }
    .frame-shot.r-16x10 { aspect-ratio: 16 / 10; }
    .frame-shot.r-21x9  { aspect-ratio: 21 / 9; }
    .frame-shot.r-3x2   { aspect-ratio: 3 / 2; }

    .frame-shot > img {
      width: 100%;
      height: 100%;
      object-fit: contain;
      object-position: center;
      display: block;
      border-radius: inherit;
    }
    .frame-shot.fit-cover > img { object-fit: cover; }

    
    .device-browser {
      position: relative;
      background: var(--paper);
      border: 0.5556px solid var(--grey-2);
      border-radius: 3.3333px;
      overflow: hidden;
    }
    .device-browser::before {
      content: '';
      display: block;
      height: 17.7778px;
      background: var(--grey-1);
      border-bottom: 0.5556px solid var(--grey-2);
      background-image:
        radial-gradient(circle at 8.8889px 8.8889px, var(--grey-3) 2.2222px, transparent 2.5px),
        radial-gradient(circle at 18.8889px 8.8889px, var(--grey-3) 2.2222px, transparent 2.5px),
        radial-gradient(circle at 28.8889px 8.8889px, var(--grey-3) 2.2222px, transparent 2.5px);
    }
    .device-browser > .frame-shot,
    .device-browser > img {
      border-radius: 0;
      display: block;
      width: 100%;
    }
    .device-phone {
      position: relative;
      background: var(--ink);
      border-radius: 15.5556px;
      padding: 6.6667px;
      box-shadow: 0 8.8889px 20px -18px rgba(0,0,0,.32);
    }
    .device-phone > .frame-shot,
    .device-phone > img {
      border-radius: 10px;
      display: block;
      width: 100%;
    }

    
    
    .map-block {
      position: relative;
      background: var(--grey-1);
      overflow: hidden;
      aspect-ratio: 4 / 3;
      width: 100%;
    }
    .map-block.r-16x10 { aspect-ratio: 16 / 10; }
    .map-block.r-16x9  { aspect-ratio: 16 / 9; }
    .map-block.r-1x1   { aspect-ratio: 1 / 1; }
    .map-block.r-3x4   { aspect-ratio: 3 / 4; }
    .map-block > img,
    .map-block > svg {
      position: absolute; inset: 0;
      width: 100%; height: 100%;
      display: block;
    }
    .map-block > img { object-fit: cover; }
    
    .map-block.tone-paper > img { filter: saturate(0) contrast(1.05) brightness(1.02); }
    .map-block.tone-ink > img   { filter: saturate(0) brightness(.58); }
    
    .map-block > svg .map-coast { fill: none; stroke: var(--grey-2); stroke-width: .4; }
    .map-block > svg .map-road  { fill: none; stroke: var(--grey-3); stroke-width: .28; stroke-dasharray: 1.2 .8; opacity: .7; }
    .map-block > svg .map-water { fill: var(--grey-1); }
    .map-block > svg .map-grid  { stroke: var(--grey-2); stroke-width: .15; opacity: .5; }

    .map-pin {
      position: absolute;
      width: 0; height: 0;
      transform: translate(-50%, -50%);
    }
    .map-pin .dot {
      position: absolute;
      left: -6px; top: -6px;
      width: 6.6667px; height: 6.6667px;
      border-radius: 50%;
      background: var(--ink);
      border: 1.1111px solid var(--paper);
      box-shadow: 0 0.5556px 1.6667px rgba(0,0,0,.22);
    }
    .map-pin.accent .dot { background: var(--accent); }
    .map-pin .line {
      position: absolute;
      left: 3.8889px; top: 0;
      width: 15.5556px; height: 0.5556px;
      background: var(--ink);
      opacity: .55;
    }
    .map-pin.left .line { left: auto; right: 3.8889px; }
    .map-pin .card {
      position: absolute;
      left: 21.1111px; top: -20px;
      min-width: 44.4444px;
      padding: 4.4444px 5.5556px;
      background: rgba(250,250,248,.94);
      box-shadow: 0 0 0 0.5556px var(--grey-2);
      border-radius: 1.1111px;
      white-space: nowrap;
    }
    .map-pin.left .card { left: auto; right: 21.1111px; }
    .map-pin .card .name {
      font-family: var(--sans-zh), var(--sans);
      font-weight: 500;
      font-size: 8.3333px;
      line-height: 1.1;
      color: var(--ink);
    }
    .map-pin .card .meta {
      display: block;
      margin-top: 2.2222px;
      font-family: var(--mono);
      font-size: 5.5556px;
      letter-spacing: .14em;
      text-transform: uppercase;
      color: var(--grey-3);
    }
    .map-pin.accent .card .name { color: var(--accent); }

    .map-legend {
      position: absolute;
      left: 7.7778px; bottom: 7.7778px;
      z-index: 3;
      background: rgba(250,250,248,.94);
      padding: 4.4444px 6.6667px;
      box-shadow: 0 0 0 0.5556px var(--grey-2);
      font-family: var(--mono);
      font-size: 6.1111px;
      letter-spacing: .14em;
      text-transform: uppercase;
      color: var(--grey-3);
    }
    .map-legend.tr { left: auto; right: 7.7778px; top: 7.7778px; bottom: auto; }

    

    
    .image-hero {
      display: grid;
      grid-template-rows: auto 1fr;
      gap: var(--sp-7);
      height: 100%;
    }
    .image-hero .hero-img-wrap {
      position: relative;
      overflow: hidden;
      background: var(--grey-1);
    }
    .image-hero .hero-img-wrap img {
      width: 100%;
      height: 100%;
      object-fit: cover;
      object-position: center 35%;
      display: block;
    }
    .image-hero .hero-overlay-block {
      position: absolute;
      left: 0;
      top: 0;
      background: var(--paper);
      padding: var(--sp-7) var(--sp-8);
      max-width: 60%;
    }
    .image-hero .hero-stats {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: var(--sp-8);
      align-items: end;
      border-top: 0.5556px solid var(--grey-2);
      padding-top: var(--sp-7);
    }
    .image-hero .hero-stats .stat-block .num {
      font-family: var(--sans);
      font-weight: 200;
      font-size: 53.3333px;
      line-height: 1;
      letter-spacing: -.02em;
      color: var(--ink);
      margin: 0 0 var(--sp-4);
    }
    .image-hero .hero-stats .stat-block .lbl {
      font-family: var(--mono);
      font-size: 10px;
      letter-spacing: .12em;
      text-transform: uppercase;
      color: var(--grey-3);
      margin: 0;
    }

    
    .kpi-tower-row {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: var(--sp-7);
      align-items: end;
      height: 100%;
    }
    .kpi-tower-row .tower-col {
      display: flex;
      flex-direction: column;
      gap: var(--sp-5);
      align-items: flex-start;
    }
    .kpi-tower-row .tower-col .num {
      font-family: var(--sans);
      font-weight: 200;
      font-size: 62.2222px;
      line-height: 1;
      letter-spacing: -.02em;
      margin: 0;
    }
    .kpi-tower-row .tower-col .lbl {
      font-family: var(--mono);
      font-size: 11.1111px;
      letter-spacing: .12em;
      text-transform: uppercase;
      color: var(--grey-3);
      margin: 0;
    }
    .kpi-tower-row .tower-col .bar-tower {
      width: 100%;
      height: var(--h, 133.3333px);
      background: var(--accent);
      transform-origin: bottom;
    }
    .kpi-tower-row .tower-col.muted .bar-tower {
      background: var(--grey-2);
    }
    .poster.xhs .kpi-tower-row { grid-template-columns: 1fr 1fr; gap: var(--sp-9); }
    .poster.square .kpi-tower-row { grid-template-columns: 1fr 1fr; gap: var(--sp-9); }

    
    .h-bar-chart {
      display: grid;
      gap: var(--sp-6);
    }
    .h-bar-chart .bar-row {
      display: grid;
      grid-template-columns: 122.2222px 1fr 66.6667px;
      gap: var(--sp-6);
      align-items: center;
    }
    .h-bar-chart .bar-row .row-lbl {
      font-family: var(--sans-zh);
      font-weight: 500;
      font-size: 14.4444px;
      color: var(--ink);
    }
    .h-bar-chart .bar-row .row-track {
      position: relative;
      height: 15.5556px;
      background: var(--grey-1);
    }
    .h-bar-chart .bar-row .row-fill {
      position: absolute;
      left: 0;
      top: 0;
      bottom: 0;
      width: var(--w, 50%);
      background: var(--accent);
    }
    .h-bar-chart .bar-row .row-val {
      font-family: var(--mono);
      font-weight: 500;
      font-size: 14.4444px;
      letter-spacing: .04em;
      text-align: right;
      color: var(--ink);
    }
    
    .poster.xhs .h-bar-chart .bar-row {
      grid-template-columns: 1fr;
      gap: var(--sp-4);
    }
    .poster.xhs .h-bar-chart .bar-row .row-val {
      text-align: left;
    }

    
    .stacked-ledger {
      display: flex;
      flex-direction: column;
    }
    .stacked-ledger .ledger-row {
      display: grid;
      grid-template-columns: 155.5556px 1fr auto;
      gap: var(--sp-7);
      align-items: baseline;
      padding: var(--sp-7) 0;
      border-bottom: 0.5556px solid var(--grey-2);
    }
    .stacked-ledger .ledger-row:first-child { padding-top: 0; }
    .stacked-ledger .ledger-row:last-child  { border-bottom: 0; }
    .stacked-ledger .ledger-num {
      font-family: var(--sans);
      font-weight: 200;
      font-size: 62.2222px;
      line-height: 1;
      letter-spacing: -.02em;
      margin: 0;
    }
    .stacked-ledger .ledger-lbl {
      font-family: var(--sans-zh);
      font-weight: 500;
      font-size: 16.6667px;
      line-height: 1.3;
      color: var(--ink);
    }
    .stacked-ledger .ledger-lbl .sub {
      display: block;
      font-weight: 400;
      font-size: 12.2222px;
      color: var(--grey-3);
      margin-top: var(--sp-3);
    }
    .stacked-ledger .ledger-icn {
      width: 31.1111px;
      height: 31.1111px;
      color: var(--accent);
    }
    .poster.square .stacked-ledger .ledger-num { font-size: 48.8889px; }
    .poster.square .stacked-ledger .ledger-row { grid-template-columns: 122.2222px 1fr auto; }

    
    .matrix-fill {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      grid-auto-rows: 1fr;
      gap: var(--sp-5);
    }
    .matrix-fill .matrix-cell {
      background: var(--grey-1);
      padding: var(--sp-6);
      display: flex;
      flex-direction: column;
      gap: var(--sp-4);
      min-height: 88.8889px;
    }
    .matrix-fill .matrix-cell .cell-nb {
      font-family: var(--mono);
      font-size: 10px;
      letter-spacing: .12em;
      color: var(--grey-3);
    }
    .matrix-fill .matrix-cell .cell-title {
      font-family: var(--sans-zh);
      font-weight: 500;
      font-size: 14.4444px;
      line-height: 1.3;
      color: var(--ink);
    }
    .matrix-fill .matrix-cell.is-accent {
      background: var(--accent);
      color: var(--accent-on);
    }
    .matrix-fill .matrix-cell.is-accent .cell-nb,
    .matrix-fill .matrix-cell.is-accent .cell-title { color: var(--accent-on); }
    .hero-stat-bottom {
      margin-top: var(--sp-9);
      padding-top: var(--sp-7);
      border-top: 0.5556px solid var(--grey-2);
      display: grid;
      grid-template-columns: 1fr auto;
      align-items: end;
      gap: var(--sp-7);
    }
    
    .poster.xhs .matrix-fill {
      grid-template-columns: repeat(2, 1fr);
      grid-auto-rows: min-content;
      gap: var(--sp-4);
    }
    .poster.xhs .matrix-fill .matrix-cell { min-height: 0; padding: var(--sp-5); }
    .poster.xhs .matrix-fill .matrix-cell .cell-title { font-size: 13.3333px; }
    .poster.xhs .hero-stat-bottom {
      margin-top: var(--sp-6);
      padding-top: var(--sp-5);
      align-items: center;
    }
    .poster.xhs .hero-stat-bottom .num-mega { font-size: 71.1111px; line-height: 1; }
    .poster.square .matrix-fill{ grid-template-columns: repeat(3, 1fr); grid-auto-rows: auto; }
    .poster.square .matrix-fill .matrix-cell { min-height: 0; }

    
    .chrome-min {
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-family: var(--mono);
      font-size: 10px;
      letter-spacing: .14em;
      text-transform: uppercase;
      color: var(--grey-3);
      padding-bottom: var(--sp-6);
      border-bottom: 0.5556px solid var(--grey-2);
      margin-bottom: var(--sp-9);
    }

    
    .pair-preview {
      width: 1333.3333px;
      min-height: 655.5556px;
      background: var(--grey-1);
      padding: var(--sp-9);
      display: grid;
      grid-template-columns: 1166.6667px 600px;
      grid-template-rows: 500px 600px;
      gap: var(--sp-9);
      align-content: center;
      justify-content: center;
    }
    .pair-preview .preview-wide   { grid-column: 1; grid-row: 1 / span 2; align-self: center; }
    .pair-preview .preview-square { grid-column: 2; grid-row: 1 / span 2; align-self: center; }
    .pair-preview .preview-label {
      font-family: var(--mono);
      font-weight: 500;
      font-size: 10px;
      letter-spacing: .14em;
      text-transform: uppercase;
      color: var(--grey-3);
      margin-bottom: var(--sp-5);
    }

    
  


</style>
<style>body{padding:0}.sheet{gap:0}</style>
<style>.cover-content{gap:24px}.cover-content .chrome-min{margin-bottom:12px}.cover-content .h-statement{margin-top:12px}.cover-points{margin-top:12px}.cover-points .h-md{margin-bottom:12px}.cover-source{margin-top:auto;border-top:1px solid var(--grey-2);padding-top:16px;display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap}</style>
</head>
<body>
  
  <main class="sheet">

    
<section class="poster xhs" id="cover"><div class="content stack cover-content"><div class="chrome-min"><span>{{栏目，可选}}</span><span>{{真实期号，可选}}</span></div><h1 class="h-statement">{{主标题}}</h1><p class="lead">{{引导语，可选}}</p><section class="card-accent cover-points"><h2 class="h-md">{{要点标题，可选}}</h2><p class="body">{{支持要点，可选}}</p></section><footer class="cover-source"><span class="t-meta">{{作者，可选}}</span><span class="t-meta">{{来源，可选}}</span></footer></div></section>
  </main>

  
  
</body>
</html>
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

## 角色与任务

你是中文封面编辑与排版设计师。依据本次内容素材提炼中心主张，沿用下方视觉种子制作一张封面，输出完整可渲染的HTML。

## 基本要求

输出独立完整 HTML，唯一导出区域 id="cover"，画布600×800像素、3:4、直角外轮廓和不透明底板。通过浏览器原生截图导出600×800不透明PNG，不靠成图裁切、缩放或拉伸修复排版。内容忠实于本次输入，保留事实含义与来源归属；转述不冒充原话，缺失来源不虚构。内容作为文本或属性值时正确进行HTML转义。文字完整可读、不重叠、不越界，不以隐藏、截断或省略号遮盖溢出。CSS 和必要脚本已内嵌，不依赖仓库文件或外部脚本；字体通过明确列出的 Google Fonts 字体URL联网加载。导出前等待字体就绪；加载失败时告知使用者并确认替代字体，不把回退字体冒充原字体。

## 视觉要求

采用 M09 Atmospheric Thesis 起点与 Ink Classic：暖纸底、墨色流动气氛与细微纹理，宋体大标题（字重500）、克制边注和底部细线。主标题表达一个中心论点，可配支持说明；英文斜体副标题、栏目元数据和来源均可选，素材不需要时删去相应模块。保留纸墨质感、衬线排版和杂志式层级，以单一主题形成视觉重心。

种子是排版起点，不是不可变的填槽表。保持本款风格与核心构图，按内容调整文字模块、数量、换行、字号、行距、间距和模块尺寸；代码中的像素值、行数及槽位数量均为起始值，不是硬内容预算。提炼一个清楚的中心主张，再选择支撑它的必要信息；不为填满空槽捏造事实、引语、标签、英文、账号、期号或步骤。无内容依据的可选模块及其分隔符一并移除，保留有意的留白，不用重复文案填空间。

下面是自包含的完整HTML种子，请依据以上原则适配内容后输出：

```html
<!doctype html>
<html lang="zh-CN" data-theme="ink-classic">
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
  font-weight: 700;
  font-display: swap;
  src: url(https://fonts.gstatic.com/s/inter/v20/UcCO3FwrK3iLTeHuS_nVMrMxCp50SjIw2boKoduKmMEVuFuYMZg.ttf) format('truetype');
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
  font-weight: 700;
  font-display: swap;
  src: url(https://fonts.gstatic.com/s/notosanssc/v40/k3kCo84MPvpLmixcA63oeAL7Iqp5IZJF9bmaGzjCnYw.ttf) format('truetype');
}
@font-face {
  font-family: 'Noto Serif SC';
  font-style: normal;
  font-weight: 400;
  font-display: swap;
  src: url(https://fonts.gstatic.com/s/notoserifsc/v35/H4cyBXePl9DZ0Xe7gG9cyOj7uK2-n-D2rd4FY7SCqyWv.ttf) format('truetype');
}
@font-face {
  font-family: 'Noto Serif SC';
  font-style: normal;
  font-weight: 500;
  font-display: swap;
  src: url(https://fonts.gstatic.com/s/notoserifsc/v35/H4cyBXePl9DZ0Xe7gG9cyOj7uK2-n-D2rd4FY7SwqyWv.ttf) format('truetype');
}
@font-face {
  font-family: 'Noto Serif SC';
  font-style: normal;
  font-weight: 700;
  font-display: swap;
  src: url(https://fonts.gstatic.com/s/notoserifsc/v35/H4cyBXePl9DZ0Xe7gG9cyOj7uK2-n-D2rd4FY7RlrCWv.ttf) format('truetype');
}
@font-face {
  font-family: 'Noto Serif SC';
  font-style: normal;
  font-weight: 900;
  font-display: swap;
  src: url(https://fonts.gstatic.com/s/notoserifsc/v35/H4cyBXePl9DZ0Xe7gG9cyOj7uK2-n-D2rd4FY7QrrCWv.ttf) format('truetype');
}
@font-face {
  font-family: 'Playfair Display';
  font-style: italic;
  font-weight: 400;
  font-display: swap;
  src: url(https://fonts.gstatic.com/s/playfairdisplay/v40/nuFRD-vYSZviVYUb_rj3ij__anPXDTnCjmHKM4nYO7KN_qiTbtY.ttf) format('truetype');
}
@font-face {
  font-family: 'Playfair Display';
  font-style: normal;
  font-weight: 400;
  font-display: swap;
  src: url(https://fonts.gstatic.com/s/playfairdisplay/v40/nuFvD-vYSZviVYUb_rj3ij__anPXJzDwcbmjWBN2PKdFvUDQ.ttf) format('truetype');
}
@font-face {
  font-family: 'Playfair Display';
  font-style: normal;
  font-weight: 700;
  font-display: swap;
  src: url(https://fonts.gstatic.com/s/playfairdisplay/v40/nuFvD-vYSZviVYUb_rj3ij__anPXJzDwcbmjWBN2PKeiukDQ.ttf) format('truetype');
}

</style>
  <style>
    

    
    :root,
    [data-theme="ink-classic"] {
      --paper:     #f3f0e8;
      --paper-2:   #ebe6da;
      --ink:       #0a0a0b;
      --muted:     #68625a;
      --line:      rgba(10,10,11,.22);
      --accent:    #111111;
      --accent-soft: #d8d2c6;
      --ink-rgb: 10,10,11;
      --paper-rgb: 243,240,232;
      --accent-rgb: 17,17,17;
    }
    [data-theme="indigo-porcelain"] {
      --paper:     #f2f4f5;
      --paper-2:   #e5ebef;
      --ink:       #0a1f3d;
      --muted:     #5f6d78;
      --line:      rgba(10,31,61,.20);
      --accent:    #315d93;
      --accent-soft: #d7e1ec;
      --ink-rgb: 10,31,61;
      --paper-rgb: 242,244,245;
      --accent-rgb: 49,93,147;
    }
    [data-theme="forest-ink"] {
      --paper:     #f5f1e8;
      --paper-2:   #e8dfcf;
      --ink:       #16251b;
      --muted:     #5d665d;
      --line:      rgba(22,37,27,.22);
      --accent:    #2e6b4f;
      --accent-soft: #d4dfd2;
      --ink-rgb: 22,37,27;
      --paper-rgb: 245,241,232;
      --accent-rgb: 46,107,79;
    }
    [data-theme="kraft-paper"] {
      --paper:     #eedfc7;
      --paper-2:   #dfc9a8;
      --ink:       #2a1e13;
      --muted:     #755f49;
      --line:      rgba(42,30,19,.24);
      --accent:    #9b5a2e;
      --accent-soft: #d5b58f;
      --ink-rgb: 42,30,19;
      --paper-rgb: 238,223,199;
      --accent-rgb: 155,90,46;
    }
    [data-theme="dune"] {
      --paper:     #f0e6d2;
      --paper-2:   #ded0b7;
      --ink:       #1f1a14;
      --muted:     #6f6557;
      --line:      rgba(31,26,20,.22);
      --accent:    #8f7650;
      --accent-soft: #d4c2a4;
      --ink-rgb: 31,26,20;
      --paper-rgb: 240,230,210;
      --accent-rgb: 143,118,80;
    }
    
    [data-theme="midnight-ink"] {
      --paper:     #0e0d0c;
      --paper-2:   #1a1714;
      --ink:       #ece2cf;
      --muted:     #9a8c75;
      --line:      rgba(236,226,207,.22);
      --accent:    #d4a04a;
      --accent-soft: #3a2a14;
      --ink-rgb: 236,226,207;
      --paper-rgb: 14,13,12;
      --accent-rgb: 212,160,74;
    }

    
    :root {
      --serif-zh: "Noto Serif SC", "Songti SC", "STSong", serif;
      --serif-en: "Playfair Display", "Noto Serif SC", serif;
      --sans-zh: "Noto Sans SC", -apple-system, "PingFang SC", "Microsoft YaHei UI", sans-serif;
      --sans-en: "Inter", -apple-system, BlinkMacSystemFont, sans-serif;
      --mono:    "IBM Plex Mono", ui-monospace, "SF Mono", Consolas, monospace;
    }

    
    *,*::before,*::after { box-sizing: border-box; }
    html, body { margin: 0; padding: 0; }
    body {
      background: #1a1a1a;
      font-family: var(--sans-zh);
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

    
    .poster.xhs    .content { padding: 53.3333px 48.8889px; }
    .poster.square .content { padding: 48.8889px 48.8889px; }
    .poster.wide   .content { padding: 48.8889px 66.6667px; }
    .content { position: relative; width: 100%; height: 100%; z-index: 2; }

    
    .mag-bg {
      position: absolute;
      inset: 0;
      width: 100%;
      height: 100%;
      z-index: 0;
      pointer-events: none;
    }
    .grain {
      position: absolute;
      inset: 0;
      z-index: 1;
      pointer-events: none;
      opacity: .35;
      mix-blend-mode: multiply;
      background-image: radial-gradient(rgba(0,0,0,.045) 0.5556px, transparent 0.5556px);
      background-size: 1.6667px 1.6667px;
    }
    .paper-wash {
      position: absolute;
      inset: 0;
      z-index: 1;
      pointer-events: none;
      background:
        linear-gradient(180deg, rgba(var(--ink-rgb),.02), rgba(var(--ink-rgb),.05) 60%, rgba(var(--ink-rgb),.08));
    }
    
    [data-theme="midnight-ink"] .grain {
      opacity: .26;
      mix-blend-mode: screen;
      background-image: radial-gradient(rgba(255,244,214,.10) 0.5556px, transparent 0.5556px);
    }
    [data-theme="midnight-ink"] .paper-wash {
      background:
        radial-gradient(80% 50% at 28% 16%, rgba(212,160,74,.12), transparent 64%),
        radial-gradient(70% 60% at 80% 86%, rgba(60,40,20,.20), transparent 72%),
        linear-gradient(180deg, rgba(236,226,207,.02), rgba(0,0,0,.32));
    }

    
    .kicker {
      font-family: var(--mono);
      font-size: 11.6667px;
      letter-spacing: .22em;
      text-transform: uppercase;
      color: rgba(var(--ink-rgb), .55);
      margin: 0 0 10px;
    }
    .h-display {
      font-family: var(--serif-zh);
      font-weight: 500;
      font-size: 68.8889px;
      line-height: 1.06;
      letter-spacing: .04em;
      margin: 0 0 13.3333px;
      color: var(--ink);
    }
    .h-xl {
      font-family: var(--serif-zh);
      font-weight: 500;
      font-size: 48.8889px;
      line-height: 1.10;
      letter-spacing: .03em;
      margin: 0 0 13.3333px;
      color: var(--ink);
    }
    .h-md {
      font-family: var(--serif-zh);
      font-weight: 500;
      font-size: 31.1111px;
      line-height: 1.18;
      letter-spacing: .02em;
      margin: 0 0 10px;
      color: var(--ink);
    }
    .h-sub {
      font-family: var(--serif-en);
      font-style: italic;
      font-weight: 400;
      font-size: 20px;
      color: var(--muted);
      margin: 0 0 13.3333px;
    }
    .lead {
      font-family: var(--serif-zh);
      font-weight: 400;
      font-size: 15.5556px;
      line-height: 1.55;
      color: rgba(var(--ink-rgb), .82);
      margin: 0 0 13.3333px;
    }
    .body {
      font-family: var(--serif-zh);
      font-weight: 400;
      font-size: 13.3333px;
      line-height: 1.65;
      color: rgba(var(--ink-rgb), .80);
      margin: 0 0 10px;
    }
    .meta {
      font-family: var(--mono);
      font-size: 10px;
      letter-spacing: .20em;
      text-transform: uppercase;
      color: rgba(var(--ink-rgb), .55);
    }
    .label {
      font-family: var(--mono);
      font-size: 10px;
      letter-spacing: .20em;
      text-transform: uppercase;
      color: rgba(var(--ink-rgb), .55);
    }
    .pullquote {
      font-family: var(--serif-zh);
      font-style: italic;
      font-weight: 500;
      font-size: 35.5556px;
      line-height: 1.28;
      color: var(--ink);
      margin: 0;
    }

    
    .poster.square .h-display { font-size: 64.4444px; }
    .poster.square .h-xl      { font-size: 43.3333px; }
    .poster.square .h-md      { font-size: 26.6667px; }
    .poster.square .lead      { font-size: 15.5556px; }
    .poster.square .body      { font-size: 14.4444px; }

    
    .poster.wide .h-display   { font-size: 71.1111px; }
    .poster.wide .h-xl        { font-size: 53.3333px; }
    .poster.wide .lead        { font-size: 18.8889px; }

    
    .issue-row {
      display: flex;
      align-items: center;
      gap: 8.8889px;
      font-family: var(--mono);
      font-size: 11.1111px;
      letter-spacing: .12em;
      text-transform: uppercase;
      color: var(--muted);
    }
    .issue-row .dot {
      width: 3.3333px;
      height: 3.3333px;
      border-radius: 50%;
      background: var(--accent);
    }
    .issue-strip {
      position: absolute;
      left: 48.8889px;
      right: 48.8889px;
      bottom: 31.1111px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 17.7778px;
      font-family: var(--mono);
      font-size: 10px;
      letter-spacing: .12em;
      text-transform: uppercase;
      color: var(--muted);
      border-top: 0.5556px solid var(--line);
      padding-top: 10px;
    }
    .poster.wide .issue-strip { left: 66.6667px; right: 66.6667px; }
    .issue-strip span { white-space: nowrap; }

    
    .stack    { display: flex; flex-direction: column; }
    .gap-1    { gap: 6.6667px; }
    .gap-2    { gap: 13.3333px; }
    .gap-3    { gap: 20px; }
    .gap-4    { gap: 26.6667px; }
    .gap-5    { gap: 35.5556px; }
    .row      { display: flex; flex-direction: row; }
    .col-2    { display: grid; grid-template-columns: 1fr 1fr; gap: 26.6667px; }
    .col-3    { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; }
    .col-2-7-5 { display: grid; grid-template-columns: 7fr 5fr; gap: 26.6667px; }
    .col-2-8-4 { display: grid; grid-template-columns: 8fr 4fr; gap: 26.6667px; }
    .center   { text-align: center; }
    .grow     { flex: 1; }
    .pad-y-md { padding-top: 20px; padding-bottom: 20px; }
    .rule     { height: 0.5556px; background: var(--line); border: 0; margin: 13.3333px 0; }
    .rule-accent { height: 1.1111px; background: var(--accent); border: 0; margin: 13.3333px 0; width: 53.3333px; }

    
    .frame-img {
      position: relative;
      overflow: hidden;
      background: var(--paper-2);
      display: block;
      margin: 0;
    }
    .frame-img img {
      width: 100%;
      height: 100%;
      object-fit: cover;
      object-position: center 50%;
      display: block;
    }
    .frame-img.fit-contain img { object-fit: contain; }
    [data-theme="midnight-ink"] .frame-img {
      background: #18120f;
      box-shadow: 0 0 0 0.5556px rgba(236,226,207,.10);
    }
    .frame-img.r-3x4   { aspect-ratio: 3 / 4; }
    .frame-img.r-1x1   { aspect-ratio: 1 / 1; }
    .frame-img.r-4x3   { aspect-ratio: 4 / 3; }
    .frame-img.r-16x9  { aspect-ratio: 16 / 9; }
    .frame-img.r-16x10 { aspect-ratio: 16 / 10; }
    .frame-img.r-21x9  { aspect-ratio: 21 / 9; }
    .frame-img.r-3x2   { aspect-ratio: 3 / 2; }
    .img-cap {
      font-family: var(--mono);
      font-size: 11.1111px;
      letter-spacing: .08em;
      text-transform: uppercase;
      color: var(--muted);
      margin-top: 7.7778px;
    }

    
    
    .frame-shot {
      position: relative;
      overflow: hidden;
      display: block;
      margin: 0;
      background: var(--paper-2);
      
      border-radius: 3.3333px;
    }
    .frame-shot.corners-sq { border-radius: 0; }
    .frame-shot.corners-sm { border-radius: 3.3333px; }
    .frame-shot.corners-md { border-radius: 7.7778px; }

    
    .frame-shot.shadow-soft { box-shadow: 0 10px 20px -18px rgba(20,18,14,.22), 0 1.1111px 3.3333px rgba(20,18,14,.06); }
    .frame-shot.shadow-ed   { box-shadow: 0 15.5556px 33.3333px -24px rgba(20,18,14,.32), 0 3.3333px 7.7778px rgba(20,18,14,.08); }

    
    .frame-shot.bg-paper    { background: var(--paper); }
    .frame-shot.bg-paper-2  { background: var(--paper-2); }
    .frame-shot.bg-ink      { background: var(--ink); }
    .frame-shot.bg-grid     {
      background:
        linear-gradient(var(--paper-2), var(--paper-2)),
        repeating-linear-gradient(0deg, var(--line) 0 0.5556px, transparent 0.5556px 26.6667px),
        repeating-linear-gradient(90deg, var(--line) 0 0.5556px, transparent 0.5556px 26.6667px);
      background-blend-mode: multiply;
    }
    .frame-shot.bg-dot {
      background-color: var(--paper-2);
      background-image: radial-gradient(var(--line) 0.5556px, transparent 0.5556px);
      background-size: 10px 10px;
    }

    
    

    
    .frame-shot.inset-none > img,
    .frame-shot.inset-none > .shot-body { padding: 0; }
    .frame-shot.inset-sub  { padding: 13.3333px; }
    .frame-shot.inset-bal  { padding: 31.1111px; }

    
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
      border: 0.5556px solid var(--line);
      border-radius: 5.5556px;
      overflow: hidden;
    }
    .device-browser::before {
      content: '';
      display: block;
      height: 20px;
      background: var(--paper-2);
      border-bottom: 0.5556px solid var(--line);
      background-image:
        radial-gradient(circle at 10px 10px, #f08080 2.7778px, transparent 3.0556px),
        radial-gradient(circle at 21.1111px 10px, #f5c450 2.7778px, transparent 3.0556px),
        radial-gradient(circle at 32.2222px 10px, #7ec98f 2.7778px, transparent 3.0556px);
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
      border-radius: 20px;
      padding: 7.7778px;
      box-shadow: 0 13.3333px 26.6667px -20px rgba(20,18,14,.42);
    }
    .device-phone > .frame-shot,
    .device-phone > img {
      border-radius: 13.3333px;
      display: block;
      width: 100%;
    }

    
    
    .map-block {
      position: relative;
      background: var(--paper-2);
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
    
    .map-block.tone-paper > img { filter: saturate(.36) contrast(.92) brightness(1.04); mix-blend-mode: multiply; }
    .map-block.tone-ink > img   { filter: saturate(.18) brightness(.62); }
    
    .map-block > svg .map-coast { fill: none; stroke: var(--line); stroke-width: .4; }
    .map-block > svg .map-road  { fill: none; stroke: var(--muted); stroke-width: .28; stroke-dasharray: 1.2 .8; opacity: .65; }
    .map-block > svg .map-water { fill: var(--paper-2); }
    .map-block > svg .map-grid  { stroke: var(--line); stroke-width: .15; opacity: .55; }

    
    .map-pin {
      position: absolute;
      width: 0; height: 0;
      transform: translate(-50%, -50%);
    }
    .map-pin .dot {
      position: absolute;
      left: -7px; top: -7px;
      width: 7.7778px; height: 7.7778px;
      border-radius: 50%;
      background: var(--ink);
      border: 1.1111px solid var(--paper);
      box-shadow: 0 0.5556px 2.2222px rgba(20,18,14,.32);
    }
    .map-pin.accent .dot { background: var(--accent); }
    .map-pin .line {
      position: absolute;
      left: 4.4444px; top: 0;
      width: 17.7778px; height: 0.5556px;
      background: var(--ink);
      opacity: .5;
    }
    .map-pin.left .line { left: auto; right: 4.4444px; }
    .map-pin .card {
      position: absolute;
      left: 24.4444px; top: -22px;
      min-width: 47.7778px;
      padding: 4.4444px 5.5556px;
      background: rgba(245,241,232,.94);
      box-shadow: 0 0 0 0.5556px var(--line);
      border-radius: 1.1111px;
      white-space: nowrap;
    }
    .map-pin.left .card { left: auto; right: 24.4444px; }
    .map-pin .card .name {
      font-family: var(--serif-zh);
      font-size: 8.8889px;
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
      color: var(--muted);
    }
    .map-pin.accent .card .name { color: var(--accent); }

    .map-legend {
      position: absolute;
      left: 7.7778px; bottom: 7.7778px;
      z-index: 3;
      background: rgba(245,241,232,.92);
      padding: 4.4444px 6.6667px;
      box-shadow: 0 0 0 0.5556px var(--line);
      font-family: var(--mono);
      font-size: 6.1111px;
      letter-spacing: .14em;
      text-transform: uppercase;
      color: var(--muted);
    }
    .map-legend.tr { left: auto; right: 7.7778px; top: 7.7778px; bottom: auto; }

    
    .callout {
      border-left: 1.6667px solid var(--accent);
      padding: 10px 15.5556px;
      font-family: var(--serif-zh);
      font-style: italic;
      font-size: 20px;
      line-height: 1.35;
      color: var(--ink);
      background: var(--paper-2);
    }
    .callout .callout-src {
      display: block;
      margin-top: 10px;
      font-style: normal;
      font-family: var(--mono);
      font-size: 11.1111px;
      letter-spacing: .12em;
      color: var(--muted);
    }

    .ledger { display: flex; flex-direction: column; }
    .ledger-row {
      display: grid;
      grid-template-columns: 53.3333px 1fr auto;
      gap: 13.3333px;
      align-items: baseline;
      padding: 15.5556px 0;
      border-bottom: 0.5556px solid var(--line);
    }
    .ledger-row .ledger-nb {
      font-family: var(--mono);
      font-size: 15.5556px;
      color: var(--accent);
      letter-spacing: .08em;
    }
    .ledger-row .ledger-title {
      font-family: var(--serif-zh);
      font-weight: 500;
      font-size: 23.3333px;
      letter-spacing: .02em;
      color: var(--ink);
    }
    .ledger-row .ledger-note {
      font-family: var(--serif-zh);
      font-weight: 400;
      font-size: 12.2222px;
      line-height: 1.55;
      color: rgba(var(--ink-rgb), .72);
    }

    .marginalia {
      display: grid;
      grid-template-columns: 1fr 122.2222px;
      gap: 26.6667px;
    }
    .marginalia .mg-col {
      border-left: 0.5556px solid var(--line);
      padding-left: 13.3333px;
    }
    .marginalia .mg-col p {
      font-family: var(--mono);
      font-size: 11.1111px;
      letter-spacing: .04em;
      color: var(--muted);
      margin: 0 0 8.8889px;
    }

    .pipeline-v { display: flex; flex-direction: column; gap: 15.5556px; }
    .pipeline-v .step {
      display: grid;
      grid-template-columns: 44.4444px 1fr;
      gap: 15.5556px;
      align-items: baseline;
      padding-bottom: 13.3333px;
      border-bottom: 0.5556px solid var(--line);
    }
    .pipeline-v .step:last-child { border-bottom: 0; }
    .pipeline-v .step-nb {
      font-family: var(--mono);
      font-size: 17.7778px;
      color: var(--accent);
    }
    .pipeline-v .step-title {
      font-family: var(--serif-zh);
      font-weight: 500;
      font-size: 22.2222px;
      letter-spacing: .02em;
      margin: 0 0 4.4444px;
    }
    .pipeline-v .step-desc {
      font-family: var(--serif-zh);
      font-weight: 400;
      font-size: 13.3333px;
      line-height: 1.6;
      color: rgba(var(--ink-rgb), .72);
      margin: 0;
    }

    .beforeafter {
      display: grid;
      grid-template-rows: 1fr 1fr;
      gap: 17.7778px;
      height: 100%;
    }
    .beforeafter .ba-block {
      padding: 17.7778px;
      background: var(--paper-2);
      border-left: 1.6667px solid var(--accent);
    }
    .beforeafter .ba-block.before { opacity: .68; }

    
    .pair-preview {
      width: 1333.3333px;
      min-height: 655.5556px;
      background: var(--paper-2);
      padding: 26.6667px;
      display: grid;
      grid-template-columns: 1166.6667px 600px;
      grid-template-rows: 500px 600px;
      gap: 26.6667px;
      align-content: center;
      justify-content: center;
    }
    .pair-preview .preview-wide   { grid-column: 1; grid-row: 1 / span 2; align-self: center; }
    .pair-preview .preview-square { grid-column: 2; grid-row: 1 / span 2; align-self: center; }
    .pair-preview .preview-label {
      font-family: var(--mono);
      font-size: 11.1111px;
      letter-spacing: .12em;
      text-transform: uppercase;
      color: var(--muted);
      margin-bottom: 7.7778px;
    }

    
    .poster .corner-tl,
    .poster .corner-tr,
    .poster .corner-bl,
    .poster .corner-br {
      position: absolute;
      font-family: var(--mono);
      font-size: 10px;
      letter-spacing: .12em;
      text-transform: uppercase;
      color: var(--muted);
      z-index: 3;
    }
    .poster.xhs .corner-tl,
    .poster.square .corner-tl { left: 48.8889px; top: 31.1111px; }
    .poster.xhs .corner-tr,
    .poster.square .corner-tr { right: 48.8889px; top: 31.1111px; }
    .poster.xhs .corner-bl,
    .poster.square .corner-bl { left: 48.8889px; bottom: 31.1111px; }
    .poster.xhs .corner-br,
    .poster.square .corner-br { right: 48.8889px; bottom: 31.1111px; }
    .poster.wide .corner-tl { left: 66.6667px; top: 31.1111px; }
    .poster.wide .corner-tr { right: 66.6667px; top: 31.1111px; }
    .poster.wide .corner-bl { left: 66.6667px; bottom: 31.1111px; }
    .poster.wide .corner-br { right: 66.6667px; bottom: 31.1111px; }
  

.cover-content{gap:22.2222px}.cover-content .h-display{margin-top:50px;margin-bottom:0}.cover-notes{margin-top:30px;border-left:1.1111px solid var(--line);padding-left:20px}.cover-notes .lead{font-size:20px;line-height:1.65}.cover-source{margin-top:auto;border-top:0.5556px solid var(--line);padding-top:16.6667px}.cover-source .lead{margin:0 0 10px}.cover-content .issue-row{justify-content:space-between}.cover-content .h-sub{margin:0}.grain{background-image:linear-gradient(112deg,rgba(0,0,0,.035),transparent 26%,rgba(255,255,255,.16) 52%,transparent 82%);background-size:auto}
</style>
<style>body{padding:0}.sheet{gap:0}</style>
</head>
<body>
  
  <main class="sheet">

    
<section class="poster xhs" id="cover"><canvas class="mag-bg" data-bg="ink-flow"></canvas><div class="grain"></div><div class="content stack cover-content"><div class="issue-row"><span>{{栏目或真实期号，可选}}</span><span>{{主题注记，可选}}</span></div><h1 class="h-display">{{主标题}}</h1><p class="h-sub">{{英文副标题，可选}}</p><div class="cover-notes"><p class="lead">{{支持说明，可选}}</p><p class="lead">{{补充说明，可选}}</p></div><div class="cover-source"><p class="lead">{{作者，可选}}</p><p class="meta">{{来源说明，可选}}</p></div></div></section>
  </main>

  
  <script>

(function () {
  function rgb(input, fallback) {
    return Array.isArray(input) && input.length === 3 ? input.map((v) => v / 255) : fallback;
  }

  function fallback2d(canvas, opts) {
    const ctx = canvas.getContext("2d");
    if (!ctx) return;
    const dpr = Math.min(2, window.devicePixelRatio || 1);
    const rect = canvas.getBoundingClientRect();
    canvas.width = Math.max(1, Math.floor(rect.width * dpr));
    canvas.height = Math.max(1, Math.floor(rect.height * dpr));
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    const w = rect.width;
    const h = rect.height;
    const ink = opts.inkCss || "rgba(26,46,31,.22)";
    const accent = opts.accentCss || "rgba(46,107,79,.18)";
    ctx.clearRect(0, 0, w, h);
    for (let i = 0; i < 5; i++) {
      const x = w * (0.14 + ((i * 0.19 + 0.17) % 0.72));
      const y = h * (0.10 + ((i * 0.29 + 0.23) % 0.78));
      const r = Math.max(w, h) * (0.22 + i * 0.045);
      const g = ctx.createRadialGradient(x, y, 0, x, y, r);
      g.addColorStop(0, i % 2 ? accent : ink);
      g.addColorStop(1, "rgba(0,0,0,0)");
      ctx.fillStyle = g;
      ctx.fillRect(0, 0, w, h);
    }
    ctx.globalAlpha = 0.09;
    ctx.strokeStyle = opts.inkCss || "rgba(26,46,31,.22)";
    for (let i = 0; i < 18; i++) {
      ctx.beginPath();
      ctx.ellipse(w * (0.5 + Math.sin(i) * 0.34), h * (0.5 + Math.cos(i * 1.7) * 0.28), 120 + i * 18, 42 + i * 9, i * 0.37, 0, Math.PI * 2);
      ctx.stroke();
    }
    ctx.globalAlpha = 1;
  }

  function mount(canvas, options) {
    const opts = options || {};
    const gl = canvas.getContext("webgl", { alpha: true, antialias: true, preserveDrawingBuffer: true });
    if (!gl) {
      fallback2d(canvas, opts);
      return { mode: "2d" };
    }

    const vert = `
      attribute vec2 aPos;
      void main(){ gl_Position = vec4(aPos, 0.0, 1.0); }
    `;
    const frag = `
      precision mediump float;
      uniform vec2 uRes;
      uniform float uTime;
      uniform vec3 uInk;
      uniform vec3 uPaper;
      uniform vec3 uAccent;
      uniform float uStrength;

      float hash(vec2 p){ return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453123); }
      float noise(vec2 p){
        vec2 i = floor(p);
        vec2 f = fract(p);
        vec2 u = f * f * (3.0 - 2.0 * f);
        return mix(
          mix(hash(i + vec2(0.0,0.0)), hash(i + vec2(1.0,0.0)), u.x),
          mix(hash(i + vec2(0.0,1.0)), hash(i + vec2(1.0,1.0)), u.x),
          u.y
        );
      }
      float fbm(vec2 p){
        float v = 0.0;
        float a = 0.5;
        mat2 m = mat2(1.6, 1.2, -1.2, 1.6);
        for(int i=0; i<5; i++){
          v += a * noise(p);
          p = m * p * 1.18;
          a *= 0.52;
        }
        return v;
      }
      void main(){
        vec2 uv = gl_FragCoord.xy / uRes.xy;
        vec2 p = (gl_FragCoord.xy - 0.5 * uRes.xy) / min(uRes.x, uRes.y);
        float t = uTime * 0.045;
        float n = fbm(p * 2.2 + vec2(t, -t * 0.7));
        float n2 = fbm(p * 5.4 - vec2(t * 1.7, t));
        float contour = smoothstep(0.015, 0.0, abs(fract((n + n2 * 0.35) * 7.0) - 0.5));
        float wash = smoothstep(0.22, 0.88, n);
        float vignette = 1.0 - smoothstep(0.28, 0.92, length(p));
        vec3 col = mix(uPaper, uInk, wash * 0.42 + contour * 0.18);
        col = mix(col, uAccent, (0.18 + 0.25 * n2) * contour);
        float alpha = uStrength * (0.18 + wash * 0.42 + contour * 0.30) * (0.55 + 0.45 * vignette);
        gl_FragColor = vec4(col, alpha);
      }
    `;

    function shader(type, source) {
      const sh = gl.createShader(type);
      gl.shaderSource(sh, source);
      gl.compileShader(sh);
      if (!gl.getShaderParameter(sh, gl.COMPILE_STATUS)) throw new Error(gl.getShaderInfoLog(sh));
      return sh;
    }

    const program = gl.createProgram();
    gl.attachShader(program, shader(gl.VERTEX_SHADER, vert));
    gl.attachShader(program, shader(gl.FRAGMENT_SHADER, frag));
    gl.linkProgram(program);
    if (!gl.getProgramParameter(program, gl.LINK_STATUS)) throw new Error(gl.getProgramInfoLog(program));
    gl.useProgram(program);

    const buffer = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, buffer);
    gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1,-1, 1,-1, -1,1, -1,1, 1,-1, 1,1]), gl.STATIC_DRAW);
    const loc = gl.getAttribLocation(program, "aPos");
    gl.enableVertexAttribArray(loc);
    gl.vertexAttribPointer(loc, 2, gl.FLOAT, false, 0, 0);

    const uRes = gl.getUniformLocation(program, "uRes");
    const uTime = gl.getUniformLocation(program, "uTime");
    const uInk = gl.getUniformLocation(program, "uInk");
    const uPaper = gl.getUniformLocation(program, "uPaper");
    const uAccent = gl.getUniformLocation(program, "uAccent");
    const uStrength = gl.getUniformLocation(program, "uStrength");
    const ink = rgb(opts.ink, [0.10, 0.18, 0.12]);
    const paper = rgb(opts.paper, [0.96, 0.94, 0.90]);
    const accent = rgb(opts.accent, [0.18, 0.42, 0.31]);

    function resize() {
      const dpr = Math.min(2, window.devicePixelRatio || 1);
      const rect = canvas.getBoundingClientRect();
      canvas.width = Math.max(1, Math.floor(rect.width * dpr));
      canvas.height = Math.max(1, Math.floor(rect.height * dpr));
      gl.viewport(0, 0, canvas.width, canvas.height);
    }

    function draw(time) {
      resize();
      gl.clearColor(0, 0, 0, 0);
      gl.clear(gl.COLOR_BUFFER_BIT);
      gl.uniform2f(uRes, canvas.width, canvas.height);
      gl.uniform1f(uTime, opts.frozenTime == null ? time * 0.001 : opts.frozenTime);
      gl.uniform3f(uInk, ink[0], ink[1], ink[2]);
      gl.uniform3f(uPaper, paper[0], paper[1], paper[2]);
      gl.uniform3f(uAccent, accent[0], accent[1], accent[2]);
      gl.uniform1f(uStrength, opts.strength == null ? 0.34 : opts.strength);
      gl.drawArrays(gl.TRIANGLES, 0, 6);
    }

    draw(0);
    if (opts.frozenTime == null) requestAnimationFrame(draw);
    return { mode: "webgl", redraw: () => draw(0) };
  }

  window.MagazineBg = { mount };
})();

</script>
  <script>
    (function () {
      function cssVarRgb(name, fallback) {
        var raw = getComputedStyle(document.documentElement).getPropertyValue(name).trim();
        if (!raw) return fallback;
        var parts = raw.split(',').map(function (x) { return parseInt(x.trim(), 10); });
        return parts.length === 3 && parts.every(function (n) { return !isNaN(n); }) ? parts : fallback;
      }
      function mountAll() {
        if (!window.MagazineBg || !window.MagazineBg.mount) return;
        var ink    = cssVarRgb('--ink-rgb',    [10, 10, 11]);
        var paper  = cssVarRgb('--paper-rgb',  [243, 240, 232]);
        var accent = cssVarRgb('--accent-rgb', [17, 17, 17]);
        document.querySelectorAll('canvas.mag-bg').forEach(function (c) {
          window.MagazineBg.mount(c, {
            ink: ink,
            paper: paper,
            accent: accent,
            strength: 0.32,
            frozenTime: 12.5
          });
        });
      }
      if (document.readyState === 'complete') mountAll();
      else window.addEventListener('load', mountAll);
    })();
  </script>
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

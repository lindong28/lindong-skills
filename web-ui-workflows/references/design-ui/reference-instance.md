# 参考实例 —— 数据密集的技术界面

一套完整指定的视觉系统。它是这套方法默认消费的那个实例，不是唯一可能的实例。**要做另一种外观，保留本文件的结构、替换取值。**参数依赖按 [design-ui 的 L2 参数推导顺序](../design-ui.md) 处理：先定字体与行高，再推导密度；改变上游取值时重算受影响的派生值。

意图：dashboard、控制台、后台管理界面，以及任何读者在比较数字的场合。分隔来自**线条与色调，不来自阴影**——阴影只留给真正浮起来的东西。密度要紧到让一整张表能放进一屏，同时又不显得局促。

不适用于：营销页、编辑类长文、以及那些职责是让人感到温暖的消费级 app。它们要的是另一个实例，而不是把这个实例微调一下。

## 1. 基准单位与 spacing ramp

基准单位 **4px**。每一个间距值都从这条闭合的梯子上取——档与档之间不取任何值。

| Token | 取值 | 用途 |
|---|---|---|
| `--sp-1` | 2px | 图标到标签、发丝级的微调 |
| `--sp-2` | 4px | 一个磁贴内部从标签到取值的间距 |
| `--sp-3` | 6px | chip 的 padding、紧凑的行内间隙 |
| `--sp-4` | 8px | 兄弟元素之间的默认间隙 |
| `--sp-5` | 12px | 单元格 padding、控件 padding |
| `--sp-6` | 16px | 卡片 padding、栅格间槽 |
| `--sp-7` | 24px | 节与节之间 |
| `--sp-8` | 32px | 页面上下外边距 |
| `--sp-9` | 48px | 页面的主要分区 |

## 2. Type ramp

每一档都带**自己的** line-height、字重与 letter-spacing。没有全局倍数——一个全局的 `line-height: 1.45` 正是产生 17.4px 与 21.75px 的东西，而它意味着没有任何一档被真正决定过。

用到的字重：**400** 正文 · **500** UI 标签 · **600** 标题。不用更重的；在一个密集的 UI 里，700/800 读起来像在喊。

| Token | 字号 / line-height | 字重 | Letter-spacing | 用途 |
|---|---|---|---|---|
| `--t-eyebrow` | 11px / 16px | 600 | `+0.04em`，uppercase | 列标题、分组标签 |
| `--t-micro` | 11px / 16px | 400 | normal | 时间戳、脚注 |
| `--t-small` | 12px / 16px | 400 | normal | 表格单元格、次级元信息 |
| `--t-body` | 13px / 18px | 400 | normal | 默认文字 |
| `--t-label` | 13px / 18px | 500 | normal | 表单标签、nav、按钮 |
| `--t-title` | 14px / 20px | 600 | `-0.005em` | 面板标题 |
| `--t-section` | 16px / 22px | 600 | `-0.01em` | 页面节标题 |
| `--t-display` | 26px / 32px | 600 | `-0.015em` | KPI 取值 |

Letter-spacing 随字号增大而收紧、随字号减小而放松——这两个方向是同一条规则，不是两个例外。

**字体。**正文：一款有真正小字号与等宽数字的技术感无衬线体——数字也用它来排（见 §7）。另配一款等宽字体，用于标识符、路径与代码，不用于数字。已验证的默认选择：**IBM Plex Sans** + **IBM Plex Mono**——它们就是为这类界面成对设计的，开放授权，可自托管。避开 Inter、Roboto、Open Sans 以及光秃秃的系统字体栈；它们就是那种默认字体的观感。

## 3. Density

| Token | 取值 | 作用于 |
|---|---|---|
| `--h-control` | 28px | 按钮、下拉框、输入框 |
| `--h-row` | 32px | 表格正文行 |
| `--pad-cell` | `6px 12px` | 表格单元格与表头 |
| `--pad-card` | `12px 16px` | 卡片与面板内部 |
| `--pad-page` | `16px 24px` | 页面外壳 |

上面这些 padding 都取自 §1 的那条梯子；一个不在梯子上的 padding token 会让梯子失效——那只是一个有名字的临时取值。那两个高度不是梯子上的值，也不该是：一个控件的高度由它的 line-height 加上它的垂直 padding 推出，所以把它钉死在某个间隙尺寸上会与 type ramp 打架。

## 4. Radius family

| Token | 取值 | 用途 |
|---|---|---|
| `--r-sm` | 3px | 条形、色块、内层 chip |
| `--r-md` | 5px | 按钮、输入框、chip |
| `--r-lg` | 6px | 卡片、面板、表格 |
| `--r-pill` | 999px | 状态 pill、计数 |

**嵌套规则**：内圆角是 `outer − padding`，下限取 `--r-sm`。一个 6px 的面板配 12px 的 padding，里面的子元素用 3px，而不是 6px——圆角相同会让内层元素看起来像贴上去的。

## 5. Elevation ladder

分隔由**线条与色调**承担。阴影只用在某个东西真正浮在页面之上的地方，而且每一级都是一个**多层**叠加——单层阴影就是那种扁平卡片的观感。

| 级别 | Token | 取值 | 作用于 |
|---|---|---|---|
| 0 | `--e-flat` | `none` + `1px solid var(--line)` | 表格、内嵌面板，以及默认情形 |
| 1 | `--e-raised` | `0 0 0 1px rgba(28,33,40,.05), 0 1px 2px rgba(28,33,40,.06)` | 卡片、sticky 表头 |
| 2 | `--e-overlay` | `0 0 0 1px rgba(28,33,40,.08), 0 2px 4px rgba(28,33,40,.08), 0 8px 24px -8px rgba(28,33,40,.16)` | popover、下拉菜单、tooltip |
| 3 | `--e-modal` | `0 0 0 1px rgba(28,33,40,.10), 0 8px 16px rgba(28,33,40,.10), 0 24px 48px -12px rgba(28,33,40,.24)` | 对话框、命令面板 |

第 0 级的任何东西都不得带阴影，而第 0 级以上的东西，在同一个 stacking context 里没有理由不得出现多于一次。

## 6. Motion

| Token | 取值 |
|---|---|
| `--dur` | 120ms |
| `--ease` | `cubic-bezier(.4, 0, .2, 1)` |
| `--t-state` | `color var(--dur) var(--ease), background-color var(--dur) var(--ease), border-color var(--dur) var(--ease), box-shadow var(--dur) var(--ease), opacity var(--dur) var(--ease)` |

**只**对 color、background-color、border-color、box-shadow、opacity 以及 `transform` 做 transition。绝不对 width、height、padding 或 margin 做——动画 layout 属性会卡顿，读起来很业余。`transition: all` 不可接受：只要有一个 layout 属性变了，它就会静默地把它动画起来。

减弱动效不是可选项：

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { transition-duration: .01ms !important; animation-duration: .01ms !important; }
}
```

## 7. Numerals

| 规则 | 为什么 |
|---|---|
| 凡是与另一个数字共处一列的数字，都加 `font-variant-numeric: tabular-nums` | 比例数字的宽度随取值变化，所以一列在两次渲染之间会肉眼可见地抖动 |
| 数字列右对齐；单位与标签保持左对齐 | 小数点位置对齐，才使得量级一眼可比 |
| 数字用**正文字体**排，用它的等宽数字——不要用等宽字体 | 等宽数字已经把数字宽度拉平了，而这正是全部要求。等宽字体还会额外给句点和逗号各自一整格，于是 `$1020.79` 渲染成 `$1020 . 79`；这个瑕疵在 12px 下轻微，在展示字号下则很难看 |
| 等宽字体留给标识符、路径、哈希与代码 | 在那里要紧的是字符级的对齐，而全宽标点是正确的，不是缺陷 |

这适用于 KPI 取值、表格单元格、图例与坐标轴刻度——任何读者会比较两个数字的地方。

## 8. State matrix

每一个可交互类都要定义全部六种状态。缺一个 `focus-visible`，就是让键盘用户完全不知道自己在哪里。

| 状态 | 处理方式 |
|---|---|
| default | 表面 + `--line` 边框 |
| hover | 背景改为 `--bg-hover`，边框改为 `--line-strong` |
| focus-visible | `outline: 2px solid var(--accent); outline-offset: 1px`——绝不移除，绝不只用一个阴影来替代 |
| active | 背景改为 `--bg-active`，不做位移弹跳 |
| disabled | `opacity: .55`、`cursor: not-allowed`，不响应 hover |
| selected | `--accent-bg` 填充 + `--accent-ink` 文字；字重可以提一档，字号不可以 |

## 9. Color roles

先有角色，再有取值。中性色朝 accent 色相**偏色**——不偏色的灰加上纯 `#fff`/`#000`，就是那种机器造出来的默认观感。

| Token | 取值 | 角色 |
|---|---|---|
| `--canvas` | `#f4f7f9` | 页面背景 |
| `--surface` | `#ffffff` | 抬起的内容 |
| `--surface-sunken` | `#eef2f6` | 表头、内凹槽位 |
| `--ink` | `#1c2128` | 主要文字 |
| `--ink-muted` | `#57616c` | 次级文字、标签 |
| `--ink-subtle` | `#7d8894` | 时间戳、禁用文字 |
| `--line` | `#d3dae1` | 默认边框 |
| `--line-soft` | `#e6ebf0` | 行分隔线 |
| `--line-strong` | `#b4bec8` | hover 边框、强调 |
| `--bg-hover` | `#f0f4f8` | hover 填充 |
| `--bg-active` | `#e5ecf3` | 按下时的填充 |
| `--accent` | `#0b66c3` | 主要动作、聚焦环 |
| `--accent-ink` | `#0a559f` | 浅色上的 accent 文字 |
| `--accent-bg` | `#dcecfb` | 选中填充 |
| `--ok` | `#1a7f4b` | 成功 |
| `--warn` | `#8a6300` | 警告 |
| `--danger` | `#c33` | 错误、破坏性操作 |

对比度下限：`--ink-muted` 在 `--surface` 上与在 `--canvas` 上都必须过 4.5:1；`--ink-subtle` 只用于非关键文字，必须过 3:1。

**分类色系**（图表、图例）是另一件事——上面这些角色不提供它们。用 `dataviz` skill 的调色板，它已针对分类可区分性与色盲安全做过验证。

## 可直接复制粘贴的块

```css
:root {
  --sp-1:2px;  --sp-2:4px;  --sp-3:6px;  --sp-4:8px;  --sp-5:12px;
  --sp-6:16px; --sp-7:24px; --sp-8:32px; --sp-9:48px;

  --h-control:28px; --h-row:32px;
  --pad-cell:6px 12px; --pad-card:12px 16px; --pad-page:16px 24px;

  --font-sans:"IBM Plex Sans",ui-sans-serif,system-ui,sans-serif;
  --font-mono:"IBM Plex Mono",ui-monospace,SFMono-Regular,Menlo,monospace;

  --r-sm:3px; --r-md:5px; --r-lg:6px; --r-pill:999px;

  --e-flat:none;
  --e-raised:0 0 0 1px rgba(28,33,40,.05), 0 1px 2px rgba(28,33,40,.06);
  --e-overlay:0 0 0 1px rgba(28,33,40,.08), 0 2px 4px rgba(28,33,40,.08), 0 8px 24px -8px rgba(28,33,40,.16);
  --e-modal:0 0 0 1px rgba(28,33,40,.10), 0 8px 16px rgba(28,33,40,.10), 0 24px 48px -12px rgba(28,33,40,.24);

  --dur:120ms; --ease:cubic-bezier(.4,0,.2,1);
  --t-state:color var(--dur) var(--ease), background-color var(--dur) var(--ease),
            border-color var(--dur) var(--ease), box-shadow var(--dur) var(--ease),
            opacity var(--dur) var(--ease);

  --canvas:#f4f7f9; --surface:#fff; --surface-sunken:#eef2f6;
  --ink:#1c2128; --ink-muted:#57616c; --ink-subtle:#7d8894;
  --line:#d3dae1; --line-soft:#e6ebf0; --line-strong:#b4bec8;
  --bg-hover:#f0f4f8; --bg-active:#e5ecf3;
  --accent:#0b66c3; --accent-ink:#0a559f; --accent-bg:#dcecfb;
  --ok:#1a7f4b; --warn:#8a6300; --danger:#c33;
}
```

各个字号档是逐元素应用的，而不是做成变量，因为每一档都是一组四个属性：

```css
.eyebrow { font:600 11px/16px var(--font-sans); letter-spacing:.04em; text-transform:uppercase; }
.micro   { font:400 11px/16px var(--font-sans); }
.small   { font:400 12px/16px var(--font-sans); }
.body    { font:400 13px/18px var(--font-sans); }
.label   { font:500 13px/18px var(--font-sans); }
.title   { font:600 14px/20px var(--font-sans); letter-spacing:-.005em; }
.section { font:600 16px/22px var(--font-sans); letter-spacing:-.01em; }
.display { font:600 26px/32px var(--font-sans); letter-spacing:-.015em; font-variant-numeric:tabular-nums; }
```

§8 的 state matrix，对每一个可交互类只应用一次，而不是逐组件应用：

```css
.control { background:var(--surface); border:1px solid var(--line); transition:var(--t-state); }
.control:hover:not(:disabled)  { background:var(--bg-hover); border-color:var(--line-strong); }
.control:active:not(:disabled) { background:var(--bg-active); }
.control:disabled              { opacity:.55; cursor:not-allowed; }
.control[aria-current],
.control[aria-selected="true"] { background:var(--accent-bg); color:var(--accent-ink); border-color:var(--accent); }
:focus-visible { outline:2px solid var(--accent); outline-offset:1px; }
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { transition-duration:.01ms !important; animation-duration:.01ms !important; }
}
```

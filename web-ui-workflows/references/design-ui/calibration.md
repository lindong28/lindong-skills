# 校准页面

三个按自洽视觉系统构建的页面，用于确立 `validate-visual-system.js` 在一个*确实*经过设计的页面上会报出什么读数。以下保留历史 `reference-instance` profile 的读数；当前默认仅输出诊断，design-ui 不再使用其通过率判断有无设计系统。

| 页面 | 它实现的系统 | 读数（`PASS / (PASS+FAIL)`） |
|---|---|---|
| `coherent.html` | 数据密集型控制台，Carbon 风格的基础层 | 8 PASS / 4 FAIL → **8/12** |
| `reading.html` | 长文文档，靠分隔线与色调区分，无阴影，无可聚焦元素 | 5 / 1 → **5/6** |
| `ratio.html` | 按每种角色各自的行高比例定的字号阶梯（正文 1.6、标题 1.3） | 5 / 1 → **5/6** |
| `thin.html` | **阴性对照**——完全没有系统，只有 UA reset 加一段散文 | 3 / 2 → **3/5** |

`design-ui.md` 里引用的第四个读数——一个真实的未设计页面，2/7——在这里没有对应 fixture。它是在一个线上页面上测过一次的，无法从本目录重跑。

## 复现

校准页面与运行脚本在 `${WEB_UI_SKILL_DIR}/workflows/design-ui/scripts/calibration/`；下文相对脚本和页面名以该目录为准。

有文档记载的做法，对这些文件中任意一个（被 serve 或在浏览器中打开的）执行：

```bash
agent-browser eval "globalThis.__WEB_UI_LEGACY_PROFILE='reference-instance'; $(cat ${WEB_UI_SKILL_DIR}/workflows/design-ui/scripts/validate-visual-system.js)"
```

`run.js` / `run_focus.js` 是可选校准驱动，使用 Node.js 22+ 的 WebSocket 与用户提供的 `CHROMIUM_EXECUTABLE` 绝对路径。运行 `node run.js <fixture绝对路径>`；浏览器使用系统分配的独立调试端口，验证器从随包相对路径加载。`run_focus.js` 在测量前聚焦 `.ring`，用于检查 focus ring。上表为上游历史读数，公开适配后须以本次真实输出为准。

## `thin.html` 确立了什么

这个未设计页面得到 **3/5 = 0.60**。按当时的规则，分母不足 6，不能作出裁决；0.60 也未达到当时约 0.65 的阈值。该阈值现已停止作为默认判据。它说明稀薄页面可能得到不低的通过率，不能仅凭比例判断有没有系统；不把这个历史样本写成当前规则已判「系统存在」。

## 这些仍未覆盖什么

`≲ 0.35` 那一档只靠单次线上页面观察支撑，没有 fixture。一个*丰富*的未设计页面——组件多、交互元素多，但仍然没有被决定过的参数——才是能在它下面垫上一个可复现数据点的 fixture。`thin.html` 在构造上就是稀薄的，担不起这个角色。

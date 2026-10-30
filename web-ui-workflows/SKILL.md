---
name: web-ui-workflows
description: "设计、开发与优化 Web UI：直接按 Prompt Planet 模板改进页面、组件、主题和布局，无需访问模板来源网站；也可独立从认可的网站真实 Web UI 创建视觉风格或场景模板，或参照产品改造目标 UI。按模板巡查组件覆盖，按需回访来源补充模板；评审设计和可用性、优化图片加载。产品级 UX 试用与验收契约使用 product-ux-workflows。"
---

# web-ui-workflows

公开分发版保留七个工作流，模板定义仍从 Prompt Planet 当前 API 或用户授权的本地模板仓读取。执行前读 [宿主与运行环境](references/portable-runtime.md)，解析实际目录与工具；无需作者的 user-scope 配置。即使刚取得的 skill 尚未被宿主重新扫描，本次会话仍可直接读取本文件及命中的 reference 执行。

按用户所需的任务或产物选择下表中的工作流，只读取命中的正文并遵循其边界；同属一个主题不表示要运行全部阶段。请求不明确时先澄清对象，不默认扩展范围。

主题入口后可带工作流名与参数；工作流名只用于选择正文，其后的内容作为该正文的 `$ARGUMENTS`，位置参数映射为 `$1`..`$9`。自然语言请求同样可选择工作流，不要求旧命令 token。正文中的工具名与运行路径按 [宿主与执行约定](references/portable-runtime.md) 解析。

| 子命令 | 常见用途 | 边界 | 按需读取 |
| --- | --- | --- | --- |
| `create-ui-template` | 从认可的网站真实 Web UI 独立创建或更新视觉风格、场景模板 | 不要求目标产品；复用 `manage-ui-templates` 的入库与维护规则 | [references/create-ui-template.md](references/create-ui-template.md) |
| `apply-ui-template` | 按给定模板或复制 Prompt 优化目标 Web UI | 模板定义与项目明确覆盖作为设计依据，不要求访问商业原站；只审核时不修改 | [references/apply-ui-template.md](references/apply-ui-template.md) |
| `adapt-reference-ui` | 基于认可的参照产品研究真实 Web UI，改进目标产品的适用功能，按需交接模板提炼 | 仅研究时止于对照与建议；单页视觉对齐走 `design-ui`，不因有参照就扩大任务 | [references/adapt-reference-ui.md](references/adapt-reference-ui.md) |
| `design-ui` | 新建或改进界面，确定布局、视觉系统与样式参数，或对齐参照产品 | 局部宽度问题只读 L0；孤立 layout bug 按普通修复处理，不扩展为整页重设计 | [references/design-ui.md](references/design-ui.md) |
| `review-ui` | 评审网页、页面或组件的设计和可用性，交付问题、记分卡与改进计划 | 判断与建议不自动授权实施修复；产品级真实试用走 `product-ux-workflows` | [references/review-ui.md](references/review-ui.md) |
| `manage-ui-templates` | 挑选、比较、收藏模板，维护复用反馈及产品类评价维度、取向和参照 | 当次选用不等于长期批准；应用到页面时交给 `apply-ui-template` | [references/manage-ui-templates.md](references/manage-ui-templates.md) |
| `optimize-images` | 引入、替换或优化网页图片及 CSS 背景，检查显示、加载和缓存 | 只处理本次图片；已有合适产物可保留，不自动启动整站设计或性能审计 | [references/optimize-images.md](references/optimize-images.md) |

从上下文取得目标页面或组件、读者任务、已有设计约束及参照；图片任务还需实际资源和显示用途，模板任务需区分当次复用与长期收藏。只补问会影响当前执行的缺失信息。含对象导航、关系图或宽表的交互报告先按 `design-ui` 的 L0 选择布局，不因名称含“报告”就套用散文布局。

“基于网站 X 创建视觉风格／场景模板”进入 `create-ui-template`，不要求先提供待改造产品。

“参照我认可的 X 的真实 Web UI，优化 Y 产品的相关功能，并把适合复用的设计沉淀到模板库”这类自然语言请求进入 `adapt-reference-ui`；无需记住子命令。只问值得借鉴什么时沿该正文完成研究，不自动实施。

产品级真实试用与 UX 验收契约使用 `product-ux-workflows`。按 [UI 规则归属](references/ui-rule-ownership.md) 区分风格、场景与 UX 的默认检查；本次改动造成的视觉、内容与操作回归仍由执行者验证。

“把这个风格应用到整个产品／所有子页面”、“用这个模板优化我的网页”、用户要求按给出的 Prompt Planet Web UI 模板页或复制 Prompt 执行时，进入 `apply-ui-template`；只挑选模板或生成可复制 Prompt 进入 `manage-ui-templates`，只审核进入 `review-ui` 的模板审核分支。模板内容在模板仓，本 skill 不维护项目专属模板副本。

“遍历页面组件，对照模板找未覆盖与未落实项”进入 `review-ui` 的模板审核分支；用户同时要求“在来源网站找参照”时使用该分支的来源研究，不必在 Prompt 中重复来源 URL。明确要求修复时沿同一 findings 交接应用与模板维护；只审核保持只读。

模板默认按读者任务选择场景，保留项目品牌与业务约束，同时允许按模板改善字号、间距、密度和信息层级；视觉风格是可选项，场景、风格和共享基线的定义与合并规则由 [manage-ui-templates](references/manage-ui-templates.md#场景风格与共享基线) 维护。整套模板可以直接采用，不要求先拼装组件。

开发、修改或审核常用组件时，按 [组件样式与选择](references/component-styles.md) 取得适用默认、显式覆盖和实际状态，接回同一份有效设计；普通局部请求也适用，不要求用户指出外观缺陷。浏览默认、比较替代样式、采用或取消选择，以及从参考网站扩充组件，均由该正文承接；只问建议时保持只读。

多页面、重复组件或批量核验沿 `apply-ui-template` 进入 [批量核验](references/batch-ui-verification.md)，使用自带脚本执行显式规则，再将实际阅读证据关联到对应规则与页面状态；原机器结果和未核实边界保留。

## 领域参考

| 当前场景 | 按需正文与入口 |
| --- | --- |
| 普通 session 判断页面好不好用或准备宣称可交付 | [web-ui-observation](references/web-ui-observation.md) 的任务范围分流与「交付前的最低证据」；按应用对象验证，不以有参照为条件 |
| 判断有无参照、复用 renderer / layout 到第二个消费者 | 同档「先确定有没有参照」；实际查找并核对消费者读数 |
| 写 CSS 前判断是否需要设计，含无系统的增量改动或已有系统内的小修 | [design-ui](references/design-ui.md)「适用与进入时点」及「这个页面已经有系统了吗？——逐层去问」；按读数分流，不由体量或单条 FAIL 决定 |

UX 与报告复用同一观察正文；按当前任务读取，不因进入本主题而运行全部子命令。

涉及期望感受、价值理解与下一步行动的对齐、模板选择、设计优化、验收或反馈维护时，先读 [体验意图](references/ui-experience-intent.md)，接入当前有效设计与本次任务范围；局部修正复用已有意图。

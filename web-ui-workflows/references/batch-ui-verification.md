# 模板驱动的批量核验

复用 [执行器及样例](../workflows/apply-ui-template/)，由完整目标、模板规则、项目绑定和通用执行器组成。多页或重复组件核验时使用，不要求单个 CSS 修正也建立整站清单。

## 输入与分工

| 层 | 内容 | 归属 |
| --- | --- | --- |
| 完整目标 scope | id、objective、application=style/scenario/ux，以及完整有效 design/project 的相对路径与 SHA256；规则、case、viewport 集合由绑定输入派生 | 本次任务，在首次执行前固定 |
| 本次有效设计 | 模板 id / source 与本次读取的内容摘要，逐条 rule 的来源、语义 role、检查方式和预期；项目覆盖写在具体条款来源和描述中 | 从当前模板编译，保存在目标项目已有设计或测试目录 |
| 项目绑定 | project / base_url，viewports，语义 role 到 selector 或专用 assertion，cases 的 path / state / ready / steps 和适用性 | 目标项目；不将项目 selector 写入通用 skill |
| 执行器 | 独立浏览器、有界并发、逐样本比较、覆盖与失败报告 | user-scope skill |

执行 agent 从当前实际模板逐条映射为机器规则、manual 或具名项目例外，并与实际页面反查遗漏；每个 rule 只承载一个可独立判定的问题，role 指向具体对象，case 区分实际状态。没有机器字段的模板也可显式编译；执行器不理解模板自然语言，也不能发现编译者漏掉的条款。来源字段应定位具体条款，不能仅写模板名。

结合路由、导航和实际入口清点页面与查询参数视图。全部目标页做基础扫描；为不同结构、重要组件变体及展开状态增加 case。不要机械展开无关组合，已观察失败须有对应检查。定位失败或缺样本不等于不适用；只有适用性已有依据时写 exclude 及原因。

复用项目已有 scope、有效设计、绑定和专用断言；新巡查发现先判断是规则编译遗漏、状态缺样本还是模板缺定义，再更新原资产。确定性的样式与几何可批量筛查，语义和视觉组合按当前应用范围保留人工观察；脚本 PASS 不证明清单外组件已覆盖。反查清单外组件时，把模板的 token 集合（字号、颜色、圆角、控件高度等）编成 `allowed-values` 规则并绑定全页元素，有依据的项目例外区域用绑定的 `exclude` 排除；报告中的离档值与元素描述即待归属对象，再判断是规则遗漏、缺样本还是模板缺定义。已观察失败加入对应复验状态，沿 [修复反馈与收敛](review-ui.md#修复反馈与收敛) 对照原发现，而非每轮建立平行报告体系。

## 调用

```bash
python3 ${WEB_UI_SKILL_DIR}/workflows/apply-ui-template/verify-ui.py \
  --scope <项目中的完整任务scope.json> \
  --output <新的持久证据目录> --jobs <容量允许的并发数> \
  --capacity-reason '<部署和浏览器资源约束>'
```

完整输入与 [scope 样例](../workflows/apply-ui-template/examples/scope.json) 一起保存在目标项目；路径相对 scope 文件解析，SHA256 取完整文件字节。修改完整目标须显式更新 scope 及输入摘要，原报告继续保留；局部复验只用 `--case`，不能删规则或 case 后仍声称原目标完成。scope 固定的是已声明分母，不能证明自然语言模板已编译完整。

旧 `--design` / `--project` 调用继续可用，报告明确“仅声明子集，无完整目标证明”。同时提供 `--scope` 和旧参数时，两者必须指向同一规范路径及相同字节。

`--screenshots` 为每个实际执行状态保存全页截图；截图不自动判美观。`--case ID` 可重复，供共享改动后的相关 case 复验；其余项保留 UNCHECKED，不自动导入旧报告。改变模板内容或项目覆盖后重新核对适用规则与受影响消费者。`--direct` 显式绕过本次浏览器代理；认证路径按 agent-browser 正文处理，本执行器不接管用户浏览器或导入登录态。

每个 case × viewport 使用新 headless session；同一状态步骤串行，独立 case 按 jobs 并发。命令和 ready 等待有超时，结束关闭本次 session。导航本身仍可能有埋点或加载副作用；调用方先核对目标范围和每个步骤的实际效果。配置文件包含可执行断言，是可信本地代码，不接受网页或远端模板提供的可执行字符串。生产只使用已授权读取与安全展开，业务写入放隔离 fixture，不把 fixture 当作生产业务验收。

## JSON v1

模板身份只要求 `id` 和 `source`，不要求模板版本号；历史输入可保留原 `version` 元数据，不能因此被判为当前模板。模板原文与内容摘要的读取、比较由 [manage-ui-templates](manage-ui-templates.md#本次有效设计) 负责；执行器不联网核对模板新鲜度，报告中的输入摘要证明本次运行用了哪些字节。

完整最小输入见 [有效规则样例](../workflows/apply-ui-template/examples/effective-design.json) 与 [项目样例](../workflows/apply-ui-template/examples/project.json)。scope 和两个输入均需 schema_version=1；报告保存输入字节摘要，原始规则和绑定由项目版本控制保留。

规则必含 id、role、source、description、kind。执行器没有内置字体、颜色、阴影或动效比例偏好。

| kind | 条件 | 边界 |
| --- | --- | --- |
| style | property（CSS 属性名）与 expected（computed style 字符串） | 比较全部匹配且渲染的元素；颜色用 rgb() 等浏览器实际格式 |
| attribute | property 与 expected | 只证明属性值，不证明功能可达 |
| text | expected 与 match=exact/contains | 适用于明确文案规范；不做自然语言类别或意义判断，报告不保存观察到的全文 |
| count | expected（非负整数） | 明确可见数量；0 只有显式要求无对象时才成立 |
| no-horizontal-overflow | 元素 scrollWidth ≤ clientWidth + 1 CSS px | 仅元素滚动几何，不检查 Canvas 像素、遮挡或故意裁切；失败附 culprits，即越出容器且未被内层滚动容器裁切的最外层元素，作为定位起点而非根因结论 |
| allowed-values | property 与 allowed（computed 值字符串列表）；可选 own_text=true 只取自身含文字的元素 | 不在集合内的值按值归组，附计数与至多 3 个元素描述，不保存页面文字；集合由有效设计从模板 token 编译，执行器不内置任何比例 |
| predicate | 由项目 role.expression 返回 {pass:boolean, samples:正整数, detail:字符串} | 由项目提供可复验的读取型适配；样本数必须来自实际对象，不能编造常数证明覆盖 |
| manual | description 写明待阅读问题 | 始终 UNCHECKED，交实际阅读流程；不汇总成自动通过 |

roles 可在项目级定义，并在 case 中覆盖。普通绑定用 selector，可加 exclude 选择器排除位于其内的元素；predicate 用 expression。case 必有 id、path（同源绝对路径）、state、ready（内容就绪布尔 JS）；ready 应检查该页面的数据与身份，不能只看 document.readyState。路径重定向或状态跳转与声明不一致时停止该 case 并留作未核实。

steps 支持 click / hover / press / focus / fill / select / scrollintoview，args 为 CLI 参数数组，reason 写本次操作的实际效果与授权依据，可带 ready 检查结果；selector 取自现场，不复用过期 snapshot ref。需要专用图表操作或真实业务验证时复用项目测试入口，不能把任意 eval 当成生产状态写入豁免。

## 单页状态与跨页旅程

`case.path` 标识单页状态；runner 在 steps 结束后要求实际 URL 与起点一致。需要停在另一 URL 的流程使用独立浏览器或项目已有端到端测试验证，起点和终点各自的页面状态仍可分别进入批量检查；不移除 URL 守卫，也不靠修改 case 路径掩盖重定向。

将有效设计中适用的父 `journey_rules` 及子项跨页要求关联到实际旅程：记录来源条款、运行版本、起点与终点、操作、对象身份、时间／筛选及返回上下文的实际读数与证据。不适用须说明目标没有哪种关系，适用但未执行仍为未核实；单项应用只验证其已有入口与受影响上下文。

旅程结论保存在同一任务记录中，与单页报告并列。单页批量检查或 finalizer 的 COMPLETE 不证明旅程通过；旅程证据也不能覆盖机器失败或冒充某一单页 manual 的阅读票。应用和审核都按这两类结果交代完成范围。

## 输出与阅读

results.json 保留每条规则、case、视口、状态、样本数、失败索引和原因，并在每个已执行 case 的 assets 中记录实际加载的样式表与脚本路径（不含查询串），用于核对受测构建与声称一致；report.md 给出相同覆盖表并按规则归组失败。归组不意味着已证明共同根因。缺绑定、无样本、manual、未选 case 均为 UNCHECKED；明确不适用为 NA，附原因。报告范围仅为声明且编译的规则，功能结果与整体阅读效果仍分开交付。

退出码：0=声明项均 PASS/NA；1=有 FAIL；2=配置或执行问题（含清理失败）；3=无 FAIL 但存在 UNCHECKED。混有 FAIL 和 UNCHECKED 时为 1，仍需读取完整报告。异常清理只处置报告中的本次 session，不使用 close --all。

复验时保留既有有效证据，但明确实际输入、目标状态与实际取样时间。没有读取的区域、无法安全触发的状态、Canvas 内部内容、真实性/主次/可读性不能被机器绿灯吸收。

## 阅读结论闭合

机器报告保持原样。完成实际阅读后，用 companion 将结论关联到同一批页面状态；没有阅读记录的项继续 UNCHECKED。一个观察回答一个可独立判定的问题，不能以“整体看起来不错”替代多个条款。

```bash
python3 ${WEB_UI_SKILL_DIR}/workflows/apply-ui-template/finalize-ui.py \
  --results <批量结果/results.json> --scope <同次完整任务scope.json> \
  --observations <阅读记录.json> --output <新的持久交付目录>
```

阅读记录使用 schema_version=1、results_sha256（原 results.json 的字节 SHA256）和 observations 数组。每项形态如下；evidence 的相对路径以阅读记录所在目录解析，绝对路径也可用。示意摘要需换成实际文件摘要。

```json
{
  "case": "catalog-expanded",
  "viewport": "narrow",
  "rule": "item-identity",
  "status": "PASS",
  "object": "展开态的长名称条目及其操作区",
  "observation": "实际阅读后，身份、状态和动作仍在同一分组；未被相邻条目截断。",
  "evidence": [{"path": "catalog-narrow.png", "sha256": "<实际文件 SHA256>"}]
}
```

finalizer 在 scope 模式下重新读取完整 design/project，核对当前字节摘要、执行报告的 scope/项目/模板身份、完整 case × viewport 身份与逐行完整 rule 集合（含 source/role）。删项、截断、伪造视口、摘要漂移被拒；已绑定 scope 的报告不能省略 `--scope` 闭合。旧无 scope 报告仍可用 `--design` 闭合，完整目标状态为 UNPROVEN。finalizer 仅接纳已执行且无 error / cleanup_error、kind=manual、原状态 UNCHECKED 的精确 case / viewport / rule。机器 FAIL、缺绑定等 UNCHECKED、未运行项及原 NA 不能用阅读票覆盖。PASS / FAIL 需已观察的对象、状态、具体读数和证据；NA 的 observation 说明适用性依据并附证据；未观察到对象不等于 NA。UNCHECKED 写缺口原因，可无证据。摘要只确认文件关联，不替执行 agent 证明内容真实。

输出 delivery.json 与 delivery.md，逐项保留原始读数及阅读记录，分别汇总 machine / reading。execution_status 只描述本次已执行组合；scope_status 描述同次报告覆盖的完整 scope，无 scope 时为 UNPROVEN。status 保留旧契约，描述报告内全部声明项并控制退出码。COMPLETE 需相应范围均已 PASS 或有依据地 NA 且无执行问题；空执行集为 UNCHECKED，局部执行 COMPLETE 不能提升为完整 scope COMPLETE。完整 scope COMPLETE 也不证明模板编译完整或整个产品通过；不跨运行导入 PASS。退出码沿用 0=声明项完成、1=FAIL、2=输入/执行问题、3=仍有 UNCHECKED。缺少记录不触发自动补全。新增模板只需编译规则和项目绑定，执行器不按模板 ID、行业或页面类型分支。

## 验证执行器

```bash
python3 -m unittest discover -s ${WEB_UI_SKILL_DIR}/workflows/apply-ui-template/tests -v
```

测试使用自身 HTTP fixture 与真实隔离浏览器，包含正确/错误、宽窄屏、键盘展开、缺样本、NA、manual、超时和局部复验。它验证检查器行为，不证明任何目标产品已合规。旧 validate-visual-system.js 默认仅为参数诊断；历史 profile 通过显式 globalThis.__WEB_UI_LEGACY_PROFILE='reference-instance' 启用，只用于原示例语境，不用于模板通过率裁决。

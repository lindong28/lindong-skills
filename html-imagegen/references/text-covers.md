# 文本封面：上游工作流与本站适配

本路线复用随包的 [Guizang Social Card Skill](../vendor/guizang/SKILL.md)。本文件只规定如何对接用户已经选中的模板；内容规划、视觉组件、素材处理和检查的细节读取上游正文，不另维护摘要副本。来源、版本和许可见 [UPSTREAM.md](../UPSTREAM.md)。

## 任务边界

用户本次交付要求与所选模板是任务边界。上游的多页图文、公众号双封面、Live Photo 默认只在本次确实请求该交付物时适用；请求一张封面就完成一张。模板的 `target_platforms` 是适用范围，不能把其中每个平台自动扩成一份交付。

上游两套视觉系统用于用户选择的杂志风、瑞士风。其它已选模板沿用自身的视觉规范与种子；不因为上游只有两种风格或其风格适用范围限制，就把扩展模板改成上游风格。上游风格专属的配色、装饰、照片占比及检查阈值按对应风格使用，不能覆盖其它模板明确声明的视觉特征。

## 内容与素材先于排版

读取上游 [Content Planning](../vendor/guizang/references/content-planning.md)，应用其中心主张、读者收益、封面标题与视觉证据的规划方法。单张任务只应用封面相关部分，不为满足多页规划编造额外观点。输出语言按用户本次要求确定，输入语言不自动决定封面语言。

根据实际素材决定哪些信息进入封面。标题、支持说明、列表、引用、来源等模块服务本次表达；种子里的模块数量、流程箭头或示例英文不构成用户事实。只有真实输入支持的关系才画成流程或对比。素材不足时删减可选模块，或在确实影响任务时询问缺失材料。

涉及照片、截图、地图时，分别读取上游 [Image Overlay](../vendor/guizang/references/image-overlay.md)、[Screenshot Treatment](../vendor/guizang/references/screenshot-treatment.md)、[Map Component](../vendor/guizang/references/map-component.md) 及 SKILL 的素材处理段。需要真实图片却只有文字时，按上游一次确认素材来源；纯文字模板无需为了流程额外索取图片。下载、调用图片模型及外发素材仍遵守宿主与用户授权，不因上游给了操作路径而获得新权限。

## 使用种子与适配布局

对杂志风、瑞士风，读取 [Style System](../vendor/guizang/references/style-system.md)、[Theme Presets](../vendor/guizang/references/theme-presets.md)、[Components](../vendor/guizang/references/components.md) 和 [Layout Recipes](../vendor/guizang/references/layout-recipes.md)，使用对应原始种子与 recipe。用户已选具体构图时，在该构图内调整；只选风格时，由内容决定合适的 recipe。不要把某次文章的填充结果当成通用 seed。

其它模板以其完整内嵌种子为起点，保留风格和核心构图。按上游 Build And Render 的方式在内容区域组织本次材料，必要时增加清晰命名的任务局部 CSS。行数、字号、间距及可选模块可适配本次内容，不能用裁断、隐藏重要内容或编造要点来迁就旧样例。

目标平台未被本次任务明确覆盖时，读取 [Platform Specs](../vendor/guizang/references/platform-specs.md) 确定交付约束；3:4 构图按需读 [Portrait Fill](../vendor/guizang/references/portrait-fill.md)。跨平台标题按 [Title Shortener](../vendor/guizang/references/title-shortener.md) 适配，不把同一长标题直接塞入不同画幅。用户明确指定的画幅和像素尺寸优先，600×800 是既有候选规格，不是所有任务的固定尺寸。

## 自包含输入与导出

最终输入继续用四块。把本次实际需要的视觉规范、完整种子及必要脚本直接放入视觉要求；文字、来源、用户选择的素材及可访问 URL 放入内容与素材。若 seed 引用随包本地脚本或图片，应内联脚本与图片数据，或使用本次已确认、可公开访问的素材 URL；复制出来的 Prompt 不能要求接收者另找 vendor 或 repo 文件。保留必要的上游许可与署名信息。

按上游 [Production Workflow](../vendor/guizang/references/production-workflow.md) 生成 HTML，再使用本 skill 的 `scripts/render_html.py` 执行浏览器截图；不另造绘图引擎。交付前读取 [QA Checklist](../vendor/guizang/references/qa-checklist.md)，检查实际 PNG 的文案、可读性、溢出与素材。用户要求自动检查且使用上游组件时，可运行随包 `validate-social-deck.mjs`；不把这个工具对上游风格的阈值推广为十款扩展模板的合格线。

保存本次实际 Prompt、HTML 与 PNG。模板后续修订与历史生成输入分开；用户认可一份图片，只表示该输入与产物获得认可。项目内修订仍走图片模板准入，不直接替换网站内容。

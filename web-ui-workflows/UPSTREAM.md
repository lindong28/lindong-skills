# 来源与公开适配

来源：ai-agent-config 的 web-ui-workflows，源提交 `6416973d17bf3b4f54265e8691d39b2ae03c186a`，2026-10-12 取得；本次来源目录无未提交改动。公开维护源位于 prompt-templates 的 `skills/web-ui-workflows/`，由既有 publish_skill.py 镜像至 lindong-skills。公开版不跟随本机安装目录自动变化。

保留七个入口、主题 references、设计探针、批量核验及其示例和测试。额外随包提供五个浏览器测量 CLI 与通用阅读原则。将本机路径改为实际包根，将跨私有 harness 的执行约定改为 `references/portable-runtime.md`；个人已选参照、私人部署和私有评审语料改为由使用者项目提供，历史案例仅说明方法边界，不代表本次实测。产品级 UX 与特定托管流程是可选相邻能力，不是安装前提。

公开包按分发仓 AGPL-3.0 许可；浏览器依赖 agent-browser 单独按其上游许可安装，不打包用户浏览器状态或凭据。

2026-11-03 从 ai-agent-config 提交 `e55f6ac0eff93be62e3051949a813063b8d57ec2` 增量同步 `claude/skills/web-ui-workflows/references/reference-behavior-adaptation.md`，SHA256 `a54f60f44fdfeb75d339999d3f59e1faec1bffb4527c2835e992d26e80e09af1`。共享正文在 ai-agent-config 维护；本包从参照改进、设计、观察和模板提炼入口条件引用，组件默认与项目实例继续由模板和产品维护。create-ui-template 仅增量补产品验证来源与提炼接入，保留本包的可移植流程；本次分支为开发候选，未据此公开发布。

# 来源与公开适配

来源：ai-agent-config 的 web-ui-workflows，源提交 `6416973d17bf3b4f54265e8691d39b2ae03c186a`，2026-10-12 取得；本次来源目录无未提交改动。公开维护源位于 prompt-templates 的 `skills/web-ui-workflows/`，由既有 publish_skill.py 镜像至 lindong-skills。公开版不跟随本机安装目录自动变化。

保留七个入口、主题 references、设计探针、批量核验及其示例和测试。额外随包提供五个浏览器测量 CLI 与通用阅读原则。将本机路径改为实际包根，将跨私有 harness 的执行约定改为 `references/portable-runtime.md`；个人已选参照、私人部署和私有评审语料改为由使用者项目提供，历史案例仅说明方法边界，不代表本次实测。产品级 UX 与特定托管流程是可选相邻能力，不是安装前提。

公开包按分发仓 AGPL-3.0 许可；浏览器依赖 agent-browser 单独按其上游许可安装，不打包用户浏览器状态或凭据。

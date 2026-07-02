# 公众号发布 SOP 冒烟验证报告（2026-07-02）

## 验证目标

检查公众号发布相关项目源码是否克隆到位，并验证 `公众号写作与发布SOP` 中的 md2wechat 发布链路当前能否成功。

## 项目源码状态

### md2wechat-skill

- 路径：`D:\Projects\OpenSource\md2wechat-skill`
- Git 仓库：存在 `.git`
- 远程仓库：`https://github.com/geekjourneyx/md2wechat-skill.git`
- 当前提交：`3306fd1d9433d69d7881f097226c6d0fea472ad3`
- 当前工作区：非干净

工作区差异：

```text
 M internal/assets/builtin/themes/autumn-warm.yaml
 M skills/md2wechat/SKILL.md
?? test_article.md
```

差异影响：

- `autumn-warm.yaml` 已加入禁止 `<style>`、`<head>`、`<link>`、外部 CDN 的约束，方向上符合微信公众号编辑器兼容要求。
- `skills/md2wechat/SKILL.md` 已补充 Windows/WSL 路径、API key、IP 白名单和占位符识别说明。
- `test_article.md` 可作为本地 smoke 测试文章，但尚未纳入 Git。

源码级测试：

- 当前 Windows PATH 中没有 `go`。
- `go test ./...` 无法执行，失败原因是 `go` 命令不存在。

### AI微信公众号

- 顶层路径：`D:\Projects\OpenSource\AI微信公众号`
- 顶层目录不是 Git 仓库。
- 子仓库：`D:\Projects\OpenSource\AI微信公众号\harness-engineering`
- 子仓库远程：`https://github.com/deusyu/harness-engineering.git`
- 子仓库当前提交：`bebc743a1bb3e1895b507c6e8fec726b4461ffc9`
- 子仓库工作区：干净

## CLI 与配置验证

`md2wechat` 全局命令已安装：

```text
C:\Users\caojianing\.local\bin\md2wechat.exe
```

版本：

```json
{
  "success": true,
  "data": {
    "version": "2.0.7"
  }
}
```

能力发现：

- `md2wechat capabilities --json` 成功。
- `md2wechat providers list --json` 成功。
- `md2wechat themes list --json` 成功。
- `md2wechat prompts list --json` 成功。
- `md2wechat prompts list --kind image --json` 成功。
- `md2wechat prompts list --kind image --archetype cover --json` 成功。

配置：

- `md2wechat config validate` 返回 `CONFIG_VALIDATED`。
- 配置文件存在：`~/.config\md2wechat\config.yaml`。
- 当前 `md2wechat config show --format json` 返回的 `default_convert_mode` 为 `api`。
- `md2wechat convert --help` 与 `md2wechat preview --help` 均显示 `--mode` 的 CLI 默认值为 `api`。
- 当前 PowerShell 环境变量中未发现 `WECHAT_APPID`、`WECHAT_SECRET`、`MD2WECHAT_BASE_URL`、`IMAGE_API_KEY`、`IMAGE_MODEL`、`IMAGE_API_BASE`。
- 本轮未打印任何密钥值。

口径澄清：

- 本知识库的公众号发布 SOP 主链路应优先使用 AI 模式，即显式传入 `--mode ai`。
- CLI 裸命令默认值不是 AI，而是 `api`；因此不带 `--mode ai` 的 preview/convert 结果只能用于暴露配置默认值，不能作为 AI 模式发布 SOP 失败的直接证据。

## SOP 本地 smoke

测试文章：

```text
D:\Projects\OpenSource\md2wechat-skill\test_article.md
```

临时封面：

```text
D:\Docs\Books\my second brain\tmp\wechat-sop-smoke\cover.png
```

### metadata 检查

不带封面时：

```text
convert_ready=true
upload_ready=true
draft_ready=false
```

带封面时：

```text
convert_ready=true
upload_ready=true
draft_ready=true
```

说明：测试文章 metadata 满足转换要求；草稿前置条件需要封面或已有封面素材 `media_id`。

### preview 检查（裸命令默认 API 分支）

命令：

```powershell
md2wechat preview "D:\Projects\OpenSource\md2wechat-skill\test_article.md" --draft --cover "D:\Docs\Books\my second brain\tmp\wechat-sop-smoke\cover.png" -o "D:\Docs\Books\my second brain\tmp\wechat-sop-smoke\preview.html" --json
```

结果：

- 返回 `PREVIEW_READY`。
- 已生成 `tmp\wechat-sop-smoke\preview.html`。
- `render.exact_html=false`。
- `render.fidelity=degraded`。
- 降级原因：`API returned error code 401: Invalid API Key format. Supported prefixes: wme_, wme2_, wmt_.`

结论：裸命令默认进入 API 分支，当前不能按 API 精确渲染路径成功，直接原因是 md2wechat API key 格式无效或仍为占位值。该结果不代表 AI 模式失败，只说明本机 CLI/config 默认值与 SOP 推荐主链路不一致。

### AI 模式检查

命令：

```powershell
md2wechat convert "D:\Projects\OpenSource\md2wechat-skill\test_article.md" --mode ai --theme autumn-warm --output "D:\Docs\Books\my second brain\tmp\wechat-sop-smoke\article.html" --json
```

结果：

- 返回 `CONVERT_AI_REQUEST_READY`。
- 状态为 `action_required`。
- 已生成 `tmp\wechat-sop-smoke\article.prompt.txt`。
- 未生成 `tmp\wechat-sop-smoke\article.html`。

说明：AI 模式不是一步完成 HTML，而是需要 LLM 执行 prompt 后写入 `requested_output_file`。

## 阶段性结论

源码层面：

- `md2wechat-skill` 已克隆到位，但工作区存在未提交改动。
- `AI微信公众号\harness-engineering` 已克隆到位且工作区干净。
- 当前机器缺少 Go，不能从源码运行 `go test ./...` 验证 Go 项目构建。

CLI 层面：

- `md2wechat` 已安装并可用，版本为 `2.0.7`。
- CLI discovery 命令可正常返回 providers、themes、prompts 和 capabilities。

SOP 层面：

- 本地 metadata 检查和草稿前置条件检查可以通过。
- 本次应判定的主链路是 AI 模式，必须显式使用 `--mode ai`。
- AI 模式能生成 prompt，但不会自动生成最终 HTML，需要 LLM 执行 prompt。
- 裸命令默认 API 模式不能完整成功，原因是 md2wechat API key 格式无效；这不是 AI 模式主链路的失败原因。
- 本轮未执行 `test-draft` 或 `create_draft`，因为这会触发远端微信草稿创建，需明确发布授权。

最终判断：

> 当前不能认定公众号发布 SOP 已完整成功。只能认定“源码和 CLI 基础到位，本地前置检查通过；AI 模式已生成待执行 prompt，但最终 HTML 尚未由 LLM 生成，远端微信草稿创建也尚未授权执行”。API key 问题只影响误入 API 默认分支或主动选择 API 模式时的路径。

## 下一步建议

1. 对本知识库公众号 SOP，后续命令必须显式写 `--mode ai`，不要依赖 CLI 默认值。
2. 先让 LLM 执行 `article.prompt.txt`，生成 `article.html`。
3. 如未来改用 API 模式，再修正 `~/.config\md2wechat\config.yaml` 中 md2wechat API key，确保前缀为 `wme_`、`wme2_` 或 `wmt_`。
4. 对生成 HTML 执行兼容性检查：

```powershell
Select-String -Path "D:\Docs\Books\my second brain\tmp\wechat-sop-smoke\article.html" -Pattern '<style|<head|<link|@import'
```

5. 在用户明确授权后，再执行：

```powershell
md2wechat test-draft "D:\Docs\Books\my second brain\tmp\wechat-sop-smoke\article.html" "D:\Docs\Books\my second brain\tmp\wechat-sop-smoke\cover.png" --json
```

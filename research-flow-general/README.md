# research-flow-general — 跨 Cursor / Claude Code / Codex 的知识调研 skill

**核心定位**：用**当前 Agent 环境可用的**网页搜索与抓取工具搜集资料 → 中文深度 Markdown → `$HOME/study-notes` → 更新 `INDEX.md` → git 推送 GitHub。

与同仓库 **`research-flow`（OpenClaw / searxng 版）** 并存；本目录为通用 Agent 版，**不修改**原 `research-flow`。

## 支持的运行时

| 产品 | 用户级安装路径 |
|------|----------------|
| Cursor | `~/.cursor/skills/research-flow-general/` |
| Claude Code | `~/.claude/skills/research-flow-general/` |
| Codex | `~/.codex/skills/research-flow-general/` |

三处应同步同一份 `SKILL.md` + `scripts/`。

## 核心流程

1. 查仓库现状 → 2. 搜索/抓取（工具名见 SKILL 映射表）→ 3. 撰文 → 4. 按主题存储 → 5. 更新 INDEX → 6. `scripts/push_wiki.py` 推送

## 凭证（勿提交 git）

推荐：`~/.config/research-flow/github.json`  

回退：`~/.cursor/secrets/github.json`、`~/.claude/secrets/github.json`、`~/.codex/secrets/github.json`，或环境变量 `GITHUB_TOKEN`。

## 文件

- `SKILL.md` — 工作流（产品无关）
- `scripts/push_wiki.py` — 跨平台推送脚本

## 关联

https://github.com/Mr-Yoje/study-notes

---
name: research-flow-general
description: "跨 Cursor / Claude Code / Codex 通用的知识调研全流程（通用版，不依赖 OpenClaw）：用当前环境可用的网页搜索与抓取工具搜集资料 → 用中文撰写有深度、图文并茂的 Markdown → 按主题写入 ~/study-notes → 更新 INDEX → git 推送 GitHub。深度调研新主题、写调研文档时使用。与 research-flow（OpenClaw 版）并存。"
---

# Research Flow General — 深度调研与主题文档同步流程（通用版）

一套完整的调研工作流：资料收集 → 撰写**有深度、图文并茂**的中文 Markdown → 按主题存入本地 `study-notes` → 更新索引 → 推送远程 GitHub。

本目录为 **`research-flow-general`**：面向 Cursor / Claude Code / Codex 等通用 Agent，与仓库内原版 **`research-flow`（OpenClaw / searxng）** 并存、互不覆盖。

**运行时**：Cursor Agent · Claude Code · OpenAI Codex（及兼容 Agent Skills 的环境）。  
**不依赖** OpenClaw / searxng。工具名因产品而异，按下表用「当前环境实际可用的等价工具」。

## 运行时工具映射（按能力选，勿写死单一产品）

| 能力 | 优先使用 | Cursor | Claude Code | Codex |
|------|----------|--------|-------------|-------|
| 网页搜索 | 内置 web search | `WebSearch` | `WebSearch` | 环境提供的 web search / 等价工具 |
| 抓取页面正文 | 内置 web fetch | `WebFetch` | `WebFetch` | 环境提供的 fetch / 打开 URL 工具 |
| 动态页 / 需登录页 | browser 自动化（若有） | browser MCP | 若有则用 | 若有则用；否则注明无法抓取 |
| 读本地仓 | 文件/检索工具 | Read / Grep / Glob | Read / Grep / Glob | 等价文件工具 |
| 写文件 / 跑命令 | 编辑 + shell | Write / Shell | Write / Bash | 等价工具 |
| 下载图片 | shell HTTP 客户端 | PowerShell `Invoke-WebRequest` 或 `curl` | `curl` | `curl` |

规则：

1. **只用当前会话里真实存在的工具**；没有 browser 就跳过 JS 重度页并在文档中说明。
2. 禁止依赖 OpenClaw、本地 searxng 脚本、或其它环境未安装的专用 CLI。
3. 搜索可并行多个中英文查询；高价值链接再抓正文。

## 前置条件与路径（跨平台）

以 **`$HOME`** 为准（Windows 上即 `%USERPROFILE%`）。

| 项 | 路径 |
|----|------|
| 笔记仓库 | `$HOME/study-notes/`（可用环境变量 `STUDY_NOTES_DIR` 覆盖） |
| 远程仓库 | `https://github.com/Mr-Yoje/study-notes` |
| GitHub 凭证（推荐） | `$HOME/.config/research-flow/github.json` |
| 凭证回退 | `$HOME/.cursor/secrets/github.json` · `$HOME/.claude/secrets/github.json` · `$HOME/.codex/secrets/github.json` · 环境变量 `GITHUB_TOKEN`（配合 `GITHUB_USERNAME`，默认 `Mr-Yoje`） |
| 本 skill 目录 | 见下方「安装位置」；推送脚本为 skill 内 `scripts/push_wiki.py` |

`github.json` 字段：

```json
{
  "github": {
    "token": "<PAT>",
    "username": "Mr-Yoje",
    "repo": "study-notes",
    "repo_url": "https://github.com/Mr-Yoje/study-notes"
  }
}
```

- **语言**：对话与调研正文一律**中文**（专有名词/代码/原文引用可保留英文）。
- **插图与公式**：优先保存检索资料**原图**到主题 `images/`；没有再自绘 SVG / 示意图。自绘 SVG 和公式必须能在 GitHub 上显示，见下方「插图与公式」。
- 若无本地仓：`git clone https://github.com/Mr-Yoje/study-notes.git "$HOME/study-notes"`（可用 PAT 做 HTTPS 克隆；克隆后 remote 去掉 token）。

### 安装位置（三端通用：复制同一份目录即可）

| 产品 | 用户级 skill 路径 |
|------|-------------------|
| Cursor | `$HOME/.cursor/skills/research-flow-general/` |
| Claude Code | `$HOME/.claude/skills/research-flow-general/` |
| Codex | `$HOME/.codex/skills/research-flow-general/` |

三处内容应保持一致（`SKILL.md` + `scripts/`）。项目级也可放在仓库的 `.cursor/skills/`、`.claude/skills/`、`.codex/skills/`（若该产品支持）。

## 仓库目录结构（按主题组织）

```
$HOME/study-notes/
├── README.md
├── INDEX.md
├── CLAUDE.md              ← 若存在则遵循其维护约定
├── 主题A/
│   ├── images/
│   │   └── xxx.png
│   ├── 文档1.md
│   └── 文档2.md
└── 主题B/
    ├── images/
    └── 文档1.md
```

- 主题 = 根下一级目录；不存在则创建（含 `images/`）。
- 图片：`![说明](images/文件名.png)`。
- 写完更新 **`INDEX.md`**；新主题同步 **`README.md`**。

## 调研完整流程

### 第 1 步：检查仓库现状

写前必须检索本地仓，避免重复并建立引用。

```bash
cd "${STUDY_NOTES_DIR:-$HOME/study-notes}"
git pull
# 用当前环境的文件搜索 / grep 工具检索关键词
```

Windows PowerShell 等价：

```powershell
cd ($env:STUDY_NOTES_DIR ? $env:STUDY_NOTES_DIR : "$env:USERPROFILE\study-notes")
git pull
```

- 已有相关文档 → 相对链接引用，如 `[相关](../主题B/文档1.md)`。
- 无主题 → 自行创建。

### 第 2 步：资料收集

1. **搜索**：用上表「网页搜索」工具（多查询、中英双语）。
2. **抓取正文**：对高价值 URL 用 fetch；失败则换源或注明。
3. **图片**：下载到 `$HOME/study-notes/<主题>/images/`，md 相对路径引用。
4. 「参考资料」保留原始链接。

### 第 3 步：撰写调研文档

`# 标题` → `> **关键词**: ...` → 中文正文。

- 结构：背景 → 概念 → 深入分析 → 对比 → 实战/踩坑 → 总结 → 参考资料。
- 深度：综合判断与来源标注；易混概念用表。
- 库内引用：`🔗 关联阅读：[XXX](../主题B/文档1.md)`。
- 公式与自绘 SVG 按「插图与公式」写，写完先本地校验再提交。

### 第 4 步：更新索引

更新 `$HOME/study-notes/INDEX.md`（主题说明 + 表格 + 关键词）；新主题写入 `README.md`。

### 第 5 步：验证并推送

1. 检查相对链接与图片。自绘 SVG 必须能按 UTF-8 解码、不含空字节、能被 XML 解析；公式只用 `$` / `$$`。
2. 提交后**优先跑推送脚本**（自动解析凭证、push、剥离 remote 中的 token）：

```bash
cd "${STUDY_NOTES_DIR:-$HOME/study-notes}"
git add -A
git status
git commit -m "notes: <主题> — 新增调研文档 X"
python3 "$(dirname-equivalent)/scripts/push_wiki.py"
```

在 Windows / 任意已安装位置，用**本 skill 目录下的脚本绝对路径**，例如：

```powershell
# Cursor 安装位
python "$env:USERPROFILE\.cursor\skills\research-flow-general\scripts\push_wiki.py"
# Claude Code 安装位
python "$env:USERPROFILE\.claude\skills\research-flow-general\scripts\push_wiki.py"
# Codex 安装位
python "$env:USERPROFILE\.codex\skills\research-flow-general\scripts\push_wiki.py"
```

或设置 `RESEARCH_FLOW_HOME` 指向任一 skill 根目录后：

```bash
python "$RESEARCH_FLOW_HOME/scripts/push_wiki.py"
```

确认分支：`git branch --show-current`。冲突时先 pull 再推送。

## 插图与公式

笔记在 GitHub 上阅读。自绘 SVG 或公式格式不对时，页面上是裂图，或一整段原始 LaTeX。

### 自绘 SVG

现象：Markdown 里的图片链接是对的，预览却是裂图。文件会被当成二进制，是因为中文被写成了非法 UTF-8，并且夹有空字节（`NUL`）。浏览器和 GitHub 都会拒绝渲染。

写法：

1. 优先下载资料原图。页面没有可下载的图文件时再自绘 SVG，并在文首说明这些图是示意图，不是原图。
2. 用 UTF-8 写入。文件以 `<svg` 或 `<?xml version="1.0" encoding="UTF-8"?>` 开头，正文不得含空字节。
3. 文本节点里的 `&`、`<`、`>` 写成 `&amp;`、`&lt;`、`&gt;`。
4. 写完用脚本校验：能按 UTF-8 解码、空字节数为 0、能被 XML 解析。不过关就重写，不要提交。
5. 编辑器若把已损坏的 `.svg` 判成二进制而拒绝覆盖，改用显式 UTF-8 写文件。不要用会按系统代码页（Windows 上常是 GBK）转码的 shell 重定向。
6. 不要用 PowerShell 默认编码的 `Get-Content` / `Set-Content` 回写 SVG。

### 公式

GitHub Markdown 只渲染 `$...$`（行内）和单独成行的 `$$...$$`（块级）。`\(...\)` 和 `\[...\]` 会按普通文字显示，反斜杠命令原样出现在页面上。

写法：

- 行内：`$z_k$`。美元符内侧不要留空格，`$ z_k $` 不会渲染。`$` 前面必须是空格或行首；紧挨汉字、`。`、`，`、`：` 或 `*` 时，GitHub 不会把它当成公式。
- 块级：`$$` 各占一行，公式放在中间，前后各空一行。不要用两个空格把 `$$` 和上一句硬换行粘成同一段，否则 GitHub 不把它当公式。
- 公式里不要写裸 `|`，它会被当成表格分隔。绝对值写成 `\vert\tau\vert`。
- 行内公式不要用 `\lVert`、`\rVert`、`\lvert`、`\rvert`。这类以 `\l`、`\r` 开头的命令在 GitHub 行内公式里会解析失败，页面上留下带底色的原始公式。范数改成单独成行的 `$$`，写成 `\Vert p-t\Vert_{2}^{2}`。

在 Windows PowerShell 里用双引号包住 `python -c` 时，`$$` 是 PowerShell 的自动变量，块级分隔符会被吃掉，公式变成没有 `$` 的裸 LaTeX。改公式用文件编辑，或把脚本写成 `.py` 再运行，不要在双引号命令字符串里写 `$$`。

## 参考阅读顺序

1. `INDEX.md` → 2. 主题总览 → 3. 深度单篇 → 4. 实战/踩坑

## 注意事项

- 工具按「运行时工具映射」选，**产品无关**；不要假设只有 Cursor。
- 路径用 `$HOME` / `%USERPROFILE%`；可用 `STUDY_NOTES_DIR`、`RESEARCH_FLOW_HOME`、`GITHUB_TOKEN` 覆盖。
- **禁止**把 PAT / `github.json` 写入笔记仓或 git commit。
- 写前查仓、写后更新索引；不写空洞文档；提交说明用中文。
- push 后确认 `git remote get-url origin` **不含** token。

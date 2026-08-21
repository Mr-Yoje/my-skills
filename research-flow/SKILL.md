---
name: research-flow
description: "知识调研全流程：搜索资料（web_search 优先用 searxng，图片优先用检索到资料的原图）→ 用中文整理有深度、图文并茂的 Markdown 调研文档 → 按主题存储到 study-notes 仓库（可含本地图片）→ 检查引用关系 → 更新 index 索引 → git 推送远程 GitHub。每次需要深度调研一个新主题、写调研文档时使用。"
---

# Research Flow — 深度调研与主题文档同步流程

一套完整的调研工作流：从资料收集，到撰写**有深度、图文并茂**的调研文档，按主题组织存储，最终推送到远程 `study-notes` 仓库。

## 前置条件

- 笔记仓库位于本地 `~/study-notes/`（**不是** `~/wiki/`）
- 远程仓库：`https://github.com/Mr-Yoje/study-notes`（master 分支，以 `git branch --show-current` 实取为准）
- Git token 存在 `/home/admin/.openclaw/workspaces/brucex/secrets.json`（字段：`github.token` / `github.username` / `github.repo` / `github.repo_url`）
- **不依赖 llm-wiki-cn skill**，也不需要 Obsidian Wikilink 规范 —— 使用标准 Markdown 即可
- 图片可以本地保存后在 md 中引用（`![](images/xxx.png)`），实现图文并茂
- **语言**：所有**对话回复**一律用**中文**；**调研文档正文也统一用中文撰写**（专有名词/代码/原文引用可保留英文）。
- **搜索**：`web_search` **优先使用 searxng**（本地隐私元搜索实例，无 API key、无限量）；仅在 searxng 搜不到/质量差时才退回其他途径。
- **插图**：文档配图**优先取用检索到的资料中的原图**（论文/官网/博客的架构图、流程图、截图）；**只有找不到合适原图时才自绘 SVG/生成示意图**。

## 仓库目录结构（按主题组织）

```
~/study-notes/
├── README.md              ← 仓库入口说明（列举主题目录）
├── INDEX.md               ← 主索引（大写），按主题分类的文档清单表格，每次写文档后更新
├── CLAUDE.md              ← 仓库维护规范说明
├── 主题A/                 ← 一级目录即主题
│   ├── images/            ← 该主题的本地图片
│   │   └── xxx.png / xxx.jpg
│   ├── 文档1.md
│   └── 文档2.md
└── 主题B/
    ├── images/
    └── 文档1.md
```

- **主题即仓库根目录下的一级目录**，文档按主题归入对应目录。
- 仓库里**没有对应主题目录时，自行创建**（含 `images/` 子目录）。
- 图片统一放在该主题的 `images/` 下，md 中使用**相对路径**引用：`![说明](images/文件名.png)`，保证图文并茂且 git 可追踪。
- **索引文件是 `INDEX.md`（大写）**，位于仓库根，采用「按主题分组 + Markdown 表格（文件/简介/字数）+ 关键词」的格式，由 AI 自动维护。README.md 中也要同步登记新主题目录。

## 调研完整流程

### 第 1 步：先检查仓库现状（重要）

**每次写文档前，必须先看看仓库里目前有没有相关内容，避免重复造轮子、并处理好文档间的引用关系。**

```bash
cd ~/study-notes
ls -R                          # 看目录结构
grep -rl "关键词" . --include="*.md"   # 检索是否已有相关内容
```

- 若已有相关主题/文档 → **复用**，在新文档中通过链接 `[相关文档](主题B/文档1.md)` 引用，形成网状引用关系，而不是另起炉灶。
- 若没有 → 自行创建主题目录。
- 若要判断远程最新状态，先 `git pull` 再检索。

### 第 2 步：资料收集

1. **搜索优先用 searxng**：`web_search` **优先使用 searxng**（本地隐私元搜索实例 `http://localhost:8080`，聚合 Google/Bing/DDG 等，无 API key、无限量），例如：

   ```bash
   cd ~/.openclaw/workspace/skills/searxng
   python3 scripts/searxng.py search "查询词" -n 10 -l zh   # 网页搜索（中文结果）
   python3 scripts/searxng.py search "查询词" -l en        # 英文结果
   python3 scripts/searxng.py search "查询词" -c images -n 10  # 图片搜索
   ```

   当 searxng 搜索不到/结果质量差，或需要特定页面内容时，再退用 **web_fetch / web_search（其他 provider）** 或 headless-browser 抓 JS 页面。

2. 用 **web_fetch** 抓取命中页内容（论文摘要、官方文档、博客、社区讨论等），提取核心观点、数据、图表，标注来源。
3. **图片优先用检索到的资料原图**：
   - 优先保存**检索资料中自带的原图**（论文/官网/博客中的架构图、流程图、架构示意、截图），下载到该主题的 `images/` 目录后在 md 中以相对路径引用，尽量保证原图、无水印、清晰。
   - **仅当找不到合适的原图时**，才手绘 SVG 或用工具自行生成示意图补充（自绘时力求准确反映原资料表达的结构）。
4. 保存原始链接/来源到文档的「参考资料」小节。

### 第 3 步：撰写调研文档（有深度 + 图文并茂）

每篇文档遵循仓库既有风格：`# 标题` 起头，紧跟 `> **关键词**: ...` 引用块，正文使用标准 Markdown（相对链接、表格、代码块、图片），**内容一律用中文撰写**（专有名词、代码、英文原文引用可保留），参考已有笔记（如 `Agent-SDK/`、`Embedding-Models/` 下的文档）保持风格一致。

- **结构建议**：背景/为什么要研究 → 核心概念拆解 → 深入分析（原理、机制、数据）→ 对比/权衡 → 实战经验/踩坑 → 总结 → 参考资料。
- **深度要求**：
  - 不只搬运，要有自己的综合判断、因果分析、独到观察（如已有多篇是「~数千 tokens」的深度笔记）。
  - 关键数据、指标、机制要写清楚来源。
  - 涉及易混淆概念时用对比表格。
- **图文并茂**：正文中合理插入图片（**优先用检索资料原图**；无原图再自绘），辅助理解：
  ```markdown
  ![架构图说明](images/architecture.png)
  ```
  说明性配图、对比表格、流程示意都可以用。
- **引用关系**：正文里对仓库内其他相关文档用相对路径链接串起来：
  ```markdown
  🔗 关联阅读：[XXX 深度解析](../主题B/文档1.md)
  ```

### 第 4 步：更新索引

写完/改完后**必须更新** `~/study-notes/INDEX.md`：

- 新增/变更主题 → 在 INDEX.md 中增加/更新对应主题小节（`## 主题`），并在主题下用相同格式的表格登记文档；
- 每个主题带一段说明 + **关键词** 行；
- 新主题同时登记到 `README.md` 的主题目录列表；
- 保证 INDEX.md 是仓库的「全量入口清单」，所有主题与文档都能从 INDEX 找到。

### 第 5 步：验证并推送

1. 检查链接与图片路径是否有效（无死链、图片能正常显示）。
2. git 提交并推送：

```bash
cd ~/study-notes
git add -A
git commit -m "notes: <主题> — 新增调研文档 X"
git push origin master
```

（若分支不是 master，先 `git branch --show-current` 确认，再 push 到该分支。）

推荐直接用辅助脚本（自动读取 token、设置 remote、处理冲突、push 后去除 token）：

```bash
python3 /home/admin/.openclaw/plugin-skills/research-flow/scripts/push_wiki.py
```

如果手动 push：

```bash
TOKEN=$(python3 -c "import json; print(json.load(open('/home/admin/.openclaw/workspaces/brucex/secrets.json'))['github']['token'])")
git remote set-url origin https://Mr-Yoje:${TOKEN}@github.com/Mr-Yoje/study-notes.git
git push origin master
```

若远程有冲突，先 pull 再 push：

```bash
git pull origin master --no-rebase --allow-unrelated-histories
# 解决冲突 → git add → git commit → git push origin master
```

## 参考阅读顺序（被问到时使用）

1. 先看 `INDEX.md`（了解全仓主题分布）
2. 再看该主题下的**总览/入门文档**（全景概览）
3. 然后深入**单篇深度分析文档**（核心机制）
4. 最后参考**实战经验/踩坑**类文档

## 注意事项

- **检索优先用 searxng** 做 web_search；图片**优先取检索资料原图**，无原图才自绘；
- **所有中文**：会话回复与文档正文都用中文，专有名词/代码/原文引用例外。
- **写前必查仓库现状**，处理好与既有文档的引用关系。
- 图片用相对路径 `images/xxx` 引用，随仓库一起提交，保证跨设备可显示。
- 每次写完都要更新 `INDEX.md`；新主题同步登记到 `README.md`。
- 不依赖 llm-wiki-cn skill，用标准 Markdown。
- push 前确认 remote URL 含 token，避免交互式认证；push 后脚本会自动去掉 token。
- 不创建空洞文档，每篇都要有实质内容与深度。
- 提交信息用中文（见 CLAUDE.md 约定）。

# research-flow — 知识调研全流程 skill

**核心定位**：搜集资料 → 撰写有深度、图文并茂的 Markdown 调研文档 → 按主题存储到 `study-notes` 仓库（可含本地图片）→ 处理文档间引用关系 → 更新 `INDEX` 索引 → git 推送远程 GitHub。

## 核心流程

1. **先查仓库现状** — 写文档前用 `ls -R` + `grep` 检索既有内容，避免重复，建立引用关系
2. **资料收集** — web_search / web_fetch / headless-browser 抓取一手与二手资料，标注来源
3. **撰写调研文档** — 有深度 + 图文并茂，图片存该主题 `images/` 目录相对路径引用
4. **按主题存储** — 主题即根目录一级目录，没有则自行创建（含 `images/`）
5. **更新索引** — 更新根目录 `INDEX.md`，新主题同步登记到 `README.md`
6. **推送远程** — 用辅助脚本 `scripts/push_wiki.py` 自动读取 token、处理冲突、推送并去掉 token

## 文件

- `SKILL.md` — skill 主文件（完整工作流规范）
- `scripts/push_wiki.py` — 推送辅助脚本（自动认证/冲突处理）

## 关联

- 📓 调研文档存储仓库：`https://github.com/Mr-Yoje/study-notes`

# 🧰 my-skills

我的个人 AI **skill 沉淀汇总仓库**。按目录分类存放各领域 skill 的规范（SKILL.md）、配套脚本与文档，持续积累、统一管理。

## 📂 目录

| 目录 | 说明 |
|------|------|
| [research-flow](./research-flow/) | 知识调研全流程 skill（**OpenClaw / searxng 版，保持原样**）：深度、图文并茂的 md 调研文档，按主题存储到 study-notes，更新 INDEX 并推送 GitHub |
| [research-flow-general](./research-flow-general/) | 同上流程的**通用版**（Cursor / Claude Code / Codex）：不依赖 OpenClaw / searxng；与 `research-flow` **并存、不覆盖** |
| ... | （更多 skill 陆续沉淀中） |

## 结构约定

每个 skill 一个目录，推荐结构：

```
skill-名称/
├── SKILL.md            ← skill 主文件（完整工作流规范与前置条件）
└── scripts/            ← 该 skill 的配套脚本
    └── xxx.py / xxx.sh
```

## 维护规范

- 新增 skill → 新建目录 + SKILL.md（+ 可选 scripts/）
- 更新本 **README.md** 的目录表
- 提交信息用中文

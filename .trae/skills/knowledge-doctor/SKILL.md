---
name: knowledge-doctor
description: 知识引擎的健康守护者。负责对 Rules 模块进行诊断（碎片化、去重、事实查证）和治疗。
version: 2.2.0
---

# Knowledge Doctor Skill (知识医生 v2.2)

此技能模仿医生的"诊断-治疗"流程，负责维护知识库的健康。
在 V2 架构中，医生的核心职责是**对抗知识库的熵增（碎片化与去重）**，并具备**高度自治权**。

## 🎯 核心职责 (Core Responsibilities)

1. **碎片化 (Fission)**: 拦截长篇大论，将超过 300 行的文档拆分为单一主题的微型卡片，便于 AI 进行 RAG (检索增强) 调用。
2. **去重 (Dedup)**: 发现并合并内容高度重叠的规则文件。
3. **静默治疗 (Silent Treatment)**: 在用户离席时自动完成重构与清理工作，无需人工确认。

## 触发机制 (Trigger)
通常由用户主动呼叫，例如：
- "调用医生检查和修复知识库"
- "整理一下知识库"
- "去重" / "拆分大文件"

## ⚠️ 核心禁令 (Strict Prohibitions)
- **禁止过度治疗**: 如果文件内容清晰且短小，不要为了"优化"而随意修改。
- **禁止越界治疗**: 严禁修改 `.trae/rules/modules` 以外的文件。
- **禁止使用 `DeleteFile` 工具操作规则文件**: 任何废弃、合并后的旧文件，都必须使用 `treatment.py` 的 `delete` 动作进行**软删除 (移入回收站)**，严禁硬删除。

## 标准作业程序 (SOP)

### 1. 预检分诊 (Triage)
调用体检仪脚本生成诊断报告：
`python .trae/skills/knowledge-doctor/scripts/scanner.py --full`
> 根据报告中的 warnings 和 criticals，确定需要治疗的目标文件（如 oversized 或重复文件）。

### 2. 生成并执行治疗方案 (Execute Treatment)
根据诊断结果，生成 JSON 格式的治疗计划，并调用 `treatment.py` 执行。

**Plan JSON 示例**:
```json
[
  {
    "action": "rewrite",
    "target": ".trae/rules/modules/ui/button.ts.md",
    "content_file": ".trae/temp/fixed_button.md"
  },
  {
    "action": "delete",
    "target": ".trae/rules/modules/ui/old_button.md"
  }
]
```

**治疗类型**:

#### A. 结构裂变 (Fission) - **最优先**
*症状*: `scanner.py` 报告文件行数超过 300 行 (oversized)，且包含多个不相关的主题。

*动作*:
1.  **Extract**: 提取并整理出特定主题的 Markdown 内容，写入临时文件（如 `.trae/temp/split_a.md`）。
2.  **Create**: 构造 Plan JSON，将临时文件写入到新路径（参考 `scanner.py` 头部的拆分命名策略，不需要你手动决定文件名格式，只要确保逻辑分离即可）。
3.  **Refactor/Delete**: 将原文件重写为一个索引 (Index) 文件，或者构造 `delete` 动作软删除原文件。

#### B. 去重手术 (Deduplication)
*症状*: 发现两个文件内容高度重叠。
*动作*:
1.  **Merge**: 将废弃文件中的价值点整合，写入临时文件 `.trae/temp/merged.md`。
2.  **Plan**: 构造 Plan JSON，包含对保留文件的 `update`/`rewrite`，以及对废弃文件的 `delete`。
3.  **Execute**: 执行 `treatment.py`。这是**静默软删除**，安全且无需用户确认。

#### C. 真相查证 (Fact Check)
*症状*: 包含 `TODO`, `FIXME`, `?` 标记，或内容存疑。
*动作*:
1.  **Search**: 使用 `WebSearch` 搜索关键词查证。
2.  **Fix**: 直接使用 `SearchReplace` 或通过 Plan JSON 修正错误，并添加 `<!-- Verified: YYYY-MM-DD -->` 注释。

### 3. 康复复查 (Post-Check)
治疗脚本执行完成后，再次运行 `scanner.py` 确认相关文件的警告是否消除。
- 如果消除，向用户报告最终结果（软删除了哪些文件，创建了哪些文件）。
- 如果未消除，继续修正。

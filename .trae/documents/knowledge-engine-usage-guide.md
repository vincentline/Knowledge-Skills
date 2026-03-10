# 知识引擎使用指南

本文档汇总了知识引擎各技能的触发指令和自然语言，方便用户快速查找和使用。

## 技能触发汇总表

| 场景 | 技能名称 | 触发指令 | 自然语言触发 | 功能描述 |
| :--- | :--- | :--- | :--- | :--- |
| **写代码/改 Bug** | coder | `/skill coder [需求]` | "帮我写代码"、"修复这个 Bug"、"优化性能" | 查阅规则库和最新经验，确保代码合规 |
| **记录经验/笔记** | knowledge-gardener | `/skill knowledge-gardener [总结]` | "记录经验"、"保存到 inbox"、"生成笔记" | 快速将经验存入 Inbox（海马体） |
| **提交代码检查** | integrity-check | `/skill integrity-check` | "帮我提交代码"、"检查代码" | 扫描变更，补录经验，生成规范提交信息 |
| **整理知识库** | knowledge-librarian | `/skill knowledge-librarian` | "整理 Inbox"、"归档知识" | 将 Inbox 碎片批量归档到 Rules |
| **检查知识库健康** | knowledge-doctor | `/skill knowledge-doctor` | "检查知识库健康"、"诊断 Rules" | 扫描并修复 Rules 模块的问题 |
| **创建新技能** | skill-creator | `/skill skill-creator [技能名称]` | "创建新技能"、"打包技能" | 初始化、打包和验证新技能 |
| **测试 Web 应用** | webapp-testing | `/skill webapp-testing [测试需求]` | "测试登录功能"、"调试 UI 行为" | 使用 Playwright 测试前端功能 |
| **安装/更新知识引擎** | knowledge-engine-manager | `/skill knowledge-engine-manager [操作]` | "安装知识引擎"、"更新知识库"、"重新安装知识库" | 管理知识引擎的安装、更新和维护 |

## 详细使用说明

### 1. 写代码/改 Bug
- **技能**：coder（老工匠）
- **指令**：`/skill coder [你的需求]`
- **示例**：
  - `/skill coder 优化 Canvas 拖拽性能`
  - `/skill coder 修复内存泄漏问题`
- **自然语言**：
  - "帮我写一个登录组件"
  - "修复这个 Bug"
  - "优化这段代码"

### 2. 记录经验/笔记
- **技能**：knowledge-gardener（速记员）
- **指令**：`/skill knowledge-gardener [你的总结]`
- **示例**：
  - `/skill knowledge-gardener 记录 Canvas 性能优化的方法`
  - `/skill knowledge-gardener 解决了内存泄漏问题`
- **自然语言**：
  - "记录经验"
  - "保存到 inbox"
  - "生成笔记"

### 3. 提交代码检查
- **技能**：integrity-check（质检员）
- **指令**：`/skill integrity-check`
- **自然语言**：
  - "帮我提交代码"
  - "检查代码"
  - "准备发版"

### 4. 整理知识库
- **技能**：knowledge-librarian（图书管理员）
- **指令**：`/skill knowledge-librarian`
- **示例**：
  - `/skill knowledge-librarian 整理这周的 Inbox`
- **自然语言**：
  - "整理 Inbox"
  - "归档知识"
  - "清理知识库"

### 5. 检查知识库健康
- **技能**：knowledge-doctor（医生）
- **指令**：`/skill knowledge-doctor`
- **示例**：
  - `/skill knowledge-doctor 检查 Rules 模块健康`
- **自然语言**：
  - "检查知识库健康"
  - "诊断 Rules"
  - "修复知识库问题"

### 6. 创建新技能
- **技能**：skill-creator（技能创建者）
- **指令**：`/skill skill-creator [技能名称]`
- **示例**：
  - `/skill skill-creator 创建测试技能`
- **自然语言**：
  - "创建新技能"
  - "打包技能"
  - "验证技能"

### 7. 测试 Web 应用
- **技能**：webapp-testing（测试工程师）
- **指令**：`/skill webapp-testing [测试需求]`
- **示例**：
  - `/skill webapp-testing 测试登录功能`
  - `/skill webapp-testing 调试 UI 行为`
- **自然语言**：
  - "测试登录功能"
  - "调试 UI 行为"
  - "捕获浏览器截图"

### 8. 安装/更新知识引擎
- **技能**：knowledge-engine-manager（知识引擎管理器）
- **指令**：`/skill knowledge-engine-manager [操作]`
- **示例**：
  - `/skill knowledge-engine-manager install`
  - `/skill knowledge-engine-manager update`
  - `/skill knowledge-engine-manager reinstall`
- **自然语言**：
  - "安装知识引擎"
  - "更新知识库"
  - "重新安装知识库"

## 快速参考

当你需要：
- **写代码** → 使用 `coder` 技能
- **记经验** → 使用 `knowledge-gardener` 技能
- **提交代码** → 使用 `integrity-check` 技能
- **整理知识** → 使用 `knowledge-librarian` 技能
- **检查健康** → 使用 `knowledge-doctor` 技能
- **创建技能** → 使用 `skill-creator` 技能
- **测试应用** → 使用 `webapp-testing` 技能
- **管理引擎** → 使用 `knowledge-engine-manager` 技能

---
*文档更新时间：2026-03-09*
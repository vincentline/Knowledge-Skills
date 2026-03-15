---
alwaysApply: true
---
> 本文档是项目的**核心原则**与**知识引擎入口**。所有开发行为必须遵循以下规则，并优先查阅知识引擎中的具体规范。

## 0. 首条消息检查点 (First Message Checkpoint)
> ⚠️ **收到用户第一条消息时必须执行**

### 判断条件
- 当前对话上下文中，这是用户的第一条消息
- 或：本次会话尚未执行过启动检查（上下文中无 `<!-- startup-check: done -->` 标记）

### 执行动作
调用 `/skill session-startup` 执行记忆激活

### 关键词触发表
| 用户消息包含 | 触发读取 |
|:---|:---|
| `游戏`/`王者`/`荣耀`/英雄名 | `user-profile.md` |
| `环境`/`系统`/`VPN` | `user-profile.md` |
| `上次`/`之前`/`继续` | `sessions/最新文件` |

## 0.5 交互后自检 (Post-Interaction Checklist)
> ⚠️ **每次回复用户前执行轻量级自检**

| 检查项 | 触发条件 | 动作 |
|:---|:---|:---|
| **记忆更新** | 完成/验证/决策/学习 | 更新 `sessions/YYYY-MM-DD.md` + `SUMMARY.md` |
| **知识记录** | 有复用/参考/查阅价值 | 询问用户是否记录到知识引擎 |

**触发关键词**：验证、测试、完成、解决、决策、学习、发现、修复

## 1. 知识引擎指引 (Knowledge Engine Router)
项目已全面启用"类脑知识引擎"，所有技术决策必须基于 `.trae/rules/` 下的最新规范。

- **查阅架构设计**: 请移步 [.trae/rules/core/architecture.md](.trae/rules/core/architecture.md)
- **查阅代码规范**: 请移步 [.trae/rules/core/coding-style.ts.md](.trae/rules/core/coding-style.ts.md)
- **查阅技术栈**: 请移步 [.trae/rules/core/tech-stack.ts.md](.trae/rules/core/tech-stack.ts.md)
- **查阅工作流**: 请移步 [.trae/rules/core/workflows.ts.md](.trae/rules/core/workflows.ts.md)
- **查阅自我进化**: 请移步 [.trae/rules/core/self-evolution.ts.md](.trae/rules/core/self-evolution.ts.md)
- **查阅功能模块**: 请使用 `LS .trae/rules/modules/` 查看领域索引，支持扁平文件 (`*.ts.md`) 和聚合目录 (`dir/index.ts.md`) 两种形式。

## 2. 行为准则 (Behavioral Guidelines)

### 2.1 开发生命周期 (Development Lifecycle)

#### 📋 开发前 (Before Coding)
触发 `/skill coder` 的关键词：编写、修改、修复、重构、优化、实现、Bug、报错

| 步骤 | 动作 |
|:---|:---|
| **1. 识别领域** | 判断属于 `graphics` / `media` / `ui` / `engineering` / `core` |
| **2. 查规则** | 读 `rules/index.md` 定位规则文件 |
| **3. 读领域规则** | 读 `modules/<domain>/` 获取开发规范 |
| **4. 查经验** | 读 `inbox/index.md` 查看未归档经验 |

#### ⚠️ 开发中 (During Coding)
- **禁止猜测 API**：未知 API 必须查阅官方文档或 `WebSearch`
- **禁止未查规则直接写**：必须先完成开发前检查
- **模仿代码风格**：`SearchCodebase` 找相似文件 + 参考 `coding-style.ts.md`

#### ✅ 开发后 (After Coding)
- **测试验证**：`webapp-testing` 或手动测试，确保功能正常、无报错
- **记忆记录**：自动记录活动到 `memory/sessions/`
- **知识判断**：判断经验是否有价值（复用/参考/查阅），有价值则询问用户是否记录到知识引擎

#### 🔒 提交前 (Before Commit)
- **检查覆盖率**：调用 `/skill integrity-check` 确保 Inbox 覆盖率

#### 🔄 异常处理 (Exception Handling)
- **测试失败** → 修复 → 重测 → 记录经验
- **规则冲突**：优先级 `core/` > `modules/` > `inbox/`
- **多领域任务**：按主次顺序查阅规则

#### 💬 非开发任务 (Non-Coding Tasks)

在问答、咨询、分析等非开发对话中：
- **主动识别**：持续关注对话内容，识别潜在有价值的经验
- **灵活判断**：根据对话上下文自主判断合适时机
- **适时提醒**：在合适时机询问用户是否记录经验
- **避免打扰**：不打断用户思路，延后询问或跳过

### 2.2 信息来源优先级
官方文档 > 权威技术博客 > 开源项目 Issues > Stack Overflow 高票回答
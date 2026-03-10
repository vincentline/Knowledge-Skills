# 知识引擎安装和更新技能方案

## 1. 方案概述

本方案旨在提供一个便捷的技能（Skill），用于在 Windows TRAE 环境下安装和更新知识引擎。本方案采用“人机协作”模式，通过 Agent 引导用户完成知识引擎的部署、规则文件的标准化以及双向同步更新。

**适用环境**：仅适用于 Windows TRAE 环境
**使用场景**：

* 单用户/团队多项目共享知识引擎

* 需要 Agent 辅助进行环境检查和配置

* 支持对知识引擎核心库的双向同步（消费与贡献）

## 2. 核心功能

### 2.1 文件目录检查/构建

#### 2.1.1 基础目录检查

* 检测 `.trae` 目录下是否存在 `logs` 文件夹

  * 不存在：创建并放入 `UPDATE_LOG.md` 文件（使用标准模板）

* 检测 `.trae` 目录下是否存在 `temp`、`trash` 文件夹

  * 不存在：创建

#### 2.1.2 规则目录检查

* 检测 `.trae` 目录下是否存在 `rules` 文件夹及其子文件夹（`core`, `inbox`, `logs`, `modules`）

  * 不存在或缺失：创建缺少的文件夹

* **核心规则文件处理 (Core Rules)**：

  * `core/coding-style.ts.md`：

    * 检查是否存在。若不存在，从技能的 `templates/coding-style.ts.md` 复制标准版本。

    * **价值**：确保所有项目遵循统一的代码风格规范。

  * `core/workflows.ts.md`：

    * 检查是否存在。若不存在，从技能的 `templates/workflows.ts.md` 复制标准版本。

    * **价值**：统一团队的工作流协议（Commit 规范、发版流程等）。

  * `core/tech-stack.ts.md`：

    * 检查是否存在。若不存在，创建空白文件或基础模板。

    * **后续动作**：触发“自动技术栈生成”流程（见 2.3）。

* **其他目录文件**：

  * `inbox/index.md`：放入模板，初始为空。

  * `logs/decision-log.md`, `logs/error-log.md`：放入模板，初始为空。

  * `rules/index.md`：放入规则索引模板。

  * `rules/core-rules.md`：放入核心规则。

### 2.2 技能更新/构建 (双向同步)

#### 2.2.1 安装检测

* 检测 `.trae/skills` 目录下是否已安装核心技能组件。

#### 2.2.2 未安装情况 (Bootstrap)

* 使用 `git submodule` 将 `Knowledge-Skills` 仓库添加到 `.trae/skills`。

* 初始化并更新子模块。

* 根据 `ENVIRONMENT.md` 或 `requirements.txt` 安装环境依赖。

#### 2.2.3 已安装情况 (Update & Sync)

* **脏状态检查 (Dirty Check)**：

  * 在更新前，检查 `.trae/skills` 下是否有未提交的本地修改。

  * 若有修改，Agent 询问用户：

    * **提交 (Commit)**：输入 Commit Message 并提交。

    * **丢弃 (Discard)**：放弃本地修改。

* **同步流程**：

  1. `git pull`：拉取远程最新代码。
  2. `git push`：将本地提交推送到远程（支持团队协作共享改进）。

* **依赖检查**：

  * 询问用户是否重新检查依赖（默认否，避免频繁耗时）。

### 2.3 自动技术栈生成 (Auto Tech-Stack)

* **触发时机**：在 `directory_checker` 完成后，若检测到 `tech-stack.ts.md` 为新创建或为空。

* **执行流程**：

  1. **扫描**：Agent 调用 `LS` 列出项目根目录文件，识别关键配置文件（如 `package.json`, `requirements.txt`, `pom.xml`, `go.mod` 等）。
  2. **分析**：Agent 读取上述配置文件，分析项目使用的语言、框架、核心库及版本。
  3. **生成**：Agent 根据分析结果，按照 `tech-stack.ts.md` 的标准格式生成内容。
  4. **写入**：将生成的内容写入 `.trae/rules/core/tech-stack.ts.md`。

## 3. 技能设计

### 3.1 技能结构

```
knowledge-engine-manager/
├── SKILL.md              # 技能定义文件
├── scripts/
│   ├── main.py           # 主脚本
│   ├── directory_checker.py  # 目录检查和构建
│   ├── git_manager.py    # Git子仓库管理 (含脏状态检查)
│   ├── dependency_manager.py  # 依赖管理
│   ├── tech_stack_analyzer.py # (可选) 辅助分析脚本，或直接由Agent完成
│   └── error_handler.py  # 错误处理
└── templates/
    ├── UPDATE_LOG.md     # 更新日志模板
    ├── index.md          # 规则索引模板
    ├── decision-log.md   # 决策日志模板
    ├── error-log.md      # 错误日志模板
    ├── coding-style.ts.md # 标准代码风格 (来自 Knowledge-Skills)
    └── workflows.ts.md    # 标准工作流协议 (来自 Knowledge-Skills)
```

### 3.2 技能流程

1. **初始化**：加载配置，环境准备。
2. **目录检查**：构建 `.trae` 目录结构，部署标准规则文件（`coding-style`, `workflows`）。
3. **技术栈分析**：(若文件) 自动生成 `tech-stack.ts.md`。
4. **安装/同步**：处理 `git submodule` 的安装或双向同步。
5. **依赖管理**：确保环境就绪。
6. **结果反馈**：输出操作总结。

## 4. 技术实现方案

### 4.1 Agent与脚本分工

* **Agent**：

  * 负责决策和交互（如询问是否提交本地修改、确认生成的 Tech Stack 内容）。

  * 执行 `tech-stack.ts.md` 的语义分析和生成。

* **脚本**：

  * 执行确定性的系统操作（文件 IO、Git 命令、Pip 安装）。

### 4.2 目录检查与模板部署

* 在 `directory_checker.py` 中集成模板复制逻辑。

* 确保 `templates/` 目录下的 `coding-style.ts.md` 和 `workflows.ts.md` 是最新版本（开发阶段需保持同步）。

### 4.3 Git 管理增强 (双向同步)

* **脏状态检查实现**：

  * 使用 `git status --porcelain` 检查是否有输出。

  * 若有输出，返回状态码给 `main.py`，由 Agent 介入询问用户。

* **同步逻辑**：

  * `git pull origin main` (建议使用 `--rebase` 以保持提交历史整洁，视团队习惯而定)。

  * `git push origin main`。

### 4.4 依赖管理标准化

* 优先检查 `requirements.txt` 和 `package.json`。

* 仅在必要时解析 `ENVIRONMENT.md`（作为后备）。

## 5. 脚本详细功能 (更新点)

### 5.1 main.py

* 新增 `auto_tech_stack` 标志位处理。

* 增加对 Git 脏状态的交互处理逻辑。

### 5.2 directory\_checker.py

* 增加 `copy_template` 函数，用于部署标准规则文件。

### 5.3 git\_manager.py

* 新增 `check_dirty()` 方法。

* 优化 `sync()` 方法，支持 Pull + Push。

## 6. 实施计划

### 6.1 开发阶段

1. **准备模板**：将现有的 `coding-style.ts.md` 和 `workflows.ts.md` 放入 `templates/`。
2. **更新脚本**：

   * 修改 `directory_checker.py` 支持模板复制。

   * 修改 `git_manager.py` 支持脏检查和双向同步。
3. **实现技术栈生成逻辑**：在 SKILL.md 的 Prompt 中编写专门的指令，指导 Agent 如何分析项目并生成 `tech-stack.ts.md`。

### 6.2 测试计划

* **新项目测试**：在一个空目录中运行，验证目录结构和标准文件的生成，验证技术栈自动生成是否准确。

* **已有项目测试**：在已有 `.trae` 的项目中运行，验证是否能正确更新标准文件（或跳过）。

* **同步测试**：模拟本地修改，验证脏状态提示和 Push 流程。

## 7. 配置与使用

### 7.1 使用流程

1. 用户调用技能：`@knowledge-engine-manager install` 或 `update`。
2. Agent 检查目录，部署标准规则。
3. Agent 发现 `tech-stack.ts.md` 为空，询问：“是否扫描项目生成技术栈文档？”

   * 用户确认 -> Agent 扫描并写入。
4. Agent 检查 Git 状态，执行同步。
5. 完成。


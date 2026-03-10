# Knowledge Engine Manager 技术文档

## 1. 技能概述

Knowledge Engine Manager 是一个专门用于管理“类脑知识引擎”的安装、更新和维护的技能。它自动构建标准目录结构、部署规则文件、生成技术栈文档，并处理 Knowledge-Skills 子模块的双向同步。

### 1.1 适用环境
- **操作系统**：Windows
- **运行环境**：TRAE 环境
- **使用场景**：单用户多项目共享知识引擎

### 1.2 核心功能
- **目录构建**：自动创建 `.trae/rules`, `.trae/logs`, `.trae/temp`, `.trae/trash` 等标准结构
- **规则部署**：部署标准代码规范 (`coding-style`) 和工作流 (`workflows`)
- **技术栈生成**：自动分析项目依赖，生成 `tech-stack.ts.md`
- **双向同步**：管理 `Knowledge-Skills` 子模块的安装、拉取 (Pull) 和推送 (Push)
- **依赖管理**：检查并安装项目依赖 (`requirements.txt`, `package.json`)

## 2. 技能架构

### 2.1 目录结构

```
knowledge-engine-manager/
├── SKILL.md              # 技能定义文件
├── scripts/
│   ├── main.py           # 主脚本，技能入口点
│   ├── directory_checker.py  # 目录检查和构建模块
│   ├── git_manager.py    # Git 子模块管理模块
│   ├── dependency_manager.py  # 依赖管理模块
│   └── error_handler.py  # 错误处理模块
└── templates/
    ├── UPDATE_LOG.md     # 更新日志模板
    ├── coding-style.ts.md  # 代码风格规范模板
    ├── workflows.ts.md    # 工作流规范模板
    ├── core-rules.md      # 核心规则文件模板
    ├── index.md           # 规则索引模板
    ├── decision-log.md    # 决策日志模板
    └── error-log.md       # 错误日志模板
```

### 2.2 模块职责

| 模块名称 | 主要职责 | 文件路径 |
| :--- | :--- | :--- |
| **主脚本** | 解析命令行参数，协调各模块执行 | `scripts/main.py` |
| **目录检查器** | 检查并创建目录结构，部署模板文件 | `scripts/directory_checker.py` |
| **Git 管理器** | 管理子模块的安装、更新和同步 | `scripts/git_manager.py` |
| **依赖管理器** | 检查并安装项目依赖 | `scripts/dependency_manager.py` |
| **错误处理器** | 处理和记录错误信息 | `scripts/error_handler.py` |

### 2.3 执行流程

1. **初始化**：加载技能配置，解析命令行参数
2. **目录检查**：执行目录结构检查和构建
3. **模板部署**：部署模板文件到指定位置
4. **技术栈分析**：检查技术栈文件，如需要则生成
5. **Git 操作**：根据操作类型执行相应的 Git 子模块操作
6. **依赖管理**：检查并安装项目依赖
7. **结果反馈**：向用户提供操作结果和建议

## 3. 实现细节

### 3.1 目录检查与构建

**功能说明**：检查并创建知识引擎所需的基础目录结构，部署模板文件到指定位置。

**关键实现**：

```python
# 基础目录结构
BASE_DIRS = [
    ".trae/logs",      # 日志目录
    ".trae/temp",      # 临时文件目录
    ".trae/trash",     # 回收站目录
    ".trae/rules/core",    # 核心规则目录
    ".trae/rules/inbox",   # 未归档经验目录
    ".trae/rules/logs",    # 规则日志目录
    ".trae/rules/modules"   # 领域规则模块目录
]

# 特别需要检查的目录（可能被.gitignore排除）
SPECIAL_DIRS = [
    ".trae/temp",      # 临时文件目录
    ".trae/trash"      # 回收站目录
]

# 模板映射: (模板路径, 目标路径)
TEMPLATE_MAPPING = {
    "UPDATE_LOG.md": ".trae/logs/UPDATE_LOG.md",                    # 更新日志模板
    "coding-style.ts.md": ".trae/rules/core/coding-style.ts.md",    # 代码风格规范
    "workflows.ts.md": ".trae/rules/core/workflows.ts.md",          # 工作流规范
    "core-rules.md": ".trae/rules/core-rules.md",                  # 核心规则文件
    "index.md": [
        ".trae/rules/index.md",           # 规则索引
        ".trae/rules/inbox/index.md"      # 经验索引
    ],
    "decision-log.md": ".trae/rules/logs/decision-log.md",          # 决策日志
    "error-log.md": ".trae/rules/logs/error-log.md"                # 错误日志
}
```

**特别处理**：
- 对 `.trae/temp` 和 `.trae/trash` 目录进行特别检查，确保即使它们被 `.gitignore` 排除也能正确检测和创建
- 模板文件仅在目标文件不存在时创建，避免覆盖用户数据

### 3.2 Git 子模块管理

**功能说明**：管理 Knowledge-Skills 子模块的安装、更新和同步，支持双向同步（拉取和推送）。

**关键实现**：

```python
# Knowledge-Skills 仓库地址
REPO_URL = "https://github.com/vincentline/Knowledge-Skills"
KNOWLEDGE_ENGINE_DIR = "knowledge-engine"  # 知识引擎目录相对路径

# 安装子模块
def install_submodule(root_dir, action):
    """安装 Knowledge-Skills 子模块
    
    策略：
    - 如果 action 为 "reinstall"，则重新安装（覆盖现有目录）
    - 如果 action 为 "update"，则更新现有子模块
    - 如果 knowledge-engine 目录不存在，则创建并安装子模块
    """
    # 实现细节...

# 同步子模块
def sync_submodule(root_dir):
    """同步子模块 (Pull & Push)
    
    步骤：
    1. 从远程拉取最新代码
    2. 如果有本地提交，则推送到远程
    """
    # 实现细节...
```

**特别处理**：
- 支持三种操作模式：安装、更新、重新安装
- 自动处理 Git 仓库初始化
- 检测未提交更改并提示用户处理

### 3.3 依赖管理

**功能说明**：检查并安装项目依赖，支持多种包管理器。

**关键实现**：
- 读取 `knowledge-engine` 目录下的 `ENVIRONMENT.md` 和 `requirements.txt` 文件
- 解析依赖信息并执行安装命令
- 支持 Python 包（使用 pip）、Node.js 包（使用 npm）等

### 3.4 错误处理

**功能说明**：处理和记录操作过程中的错误，提供详细的错误信息和解决建议。

**关键实现**：
- 使用装饰器捕获和处理异常
- 生成详细的错误日志
- 提供错误处理建议

### 3.5 用户交互

**功能说明**：与用户进行交互，处理用户输入和反馈。

**关键实现**：
- 当 `knowledge-engine` 目录存在时，询问用户选择操作：重新安装、更新仓库或取消
- 当检测到未提交更改时，询问用户提交或丢弃更改
- 提供清晰的操作选项和说明

## 4. 技术实现

### 4.1 核心技术

| 技术 | 用途 | 实现方式 |
| :--- | :--- | :--- |
| **Python** | 主要开发语言 | 脚本编写 |
| **Git** | 版本控制和子模块管理 | 命令行调用 |
| **os 模块** | 文件系统操作 | 目录检查和创建 |
| **subprocess 模块** | 执行外部命令 | 调用 Git 命令 |
| **argparse 模块** | 命令行参数解析 | 处理用户输入 |

### 4.2 关键函数

#### 4.2.1 目录检查模块

| 函数名 | 功能 | 参数 | 返回值 |
| :--- | :--- | :--- | :--- |
| `check_and_create_dirs` | 检查并创建基础目录结构 | root_dir: 项目根目录路径 | bool: 操作成功返回 True |
| `deploy_templates` | 部署模板文件到指定位置 | root_dir: 项目根目录路径<br>skill_root: 技能根目录路径 | bool: 操作成功返回 True |

#### 4.2.2 Git 管理模块

| 函数名 | 功能 | 参数 | 返回值 |
| :--- | :--- | :--- | :--- |
| `run_git_command` | 执行 Git 命令并返回输出 | command: Git 命令字符串<br>cwd: 命令执行的工作目录 | str or None: 命令执行成功返回输出结果，失败返回 None |
| `check_git_status` | 检查是否为 Git 仓库 | root_dir: 项目根目录路径 | bool: 是 Git 仓库返回 True，否则返回 False |
| `install_submodule` | 安装 Knowledge-Skills 子模块 | root_dir: 项目根目录路径<br>action: 操作类型 | bool: 安装成功返回 True，失败返回 False |
| `sync_submodule` | 同步子模块 (Pull & Push) | root_dir: 项目根目录路径 | bool: 同步成功返回 True，失败返回 False |
| `commit_changes` | 提交子模块更改 | root_dir: 项目根目录路径<br>message: 提交消息 | bool: 操作成功返回 True |
| `discard_changes` | 丢弃子模块更改 | root_dir: 项目根目录路径 | bool: 操作成功返回 True |

#### 4.2.3 依赖管理模块

| 函数名 | 功能 | 参数 | 返回值 |
| :--- | :--- | :--- | :--- |
| `install_dependencies` | 安装项目依赖 | root_dir: 项目根目录路径 | bool: 安装成功返回 True，失败返回 False |

#### 4.2.4 主脚本模块

| 函数名 | 功能 | 参数 | 返回值 |
| :--- | :--- | :--- | :--- |
| `main` | 主函数，解析命令行参数并执行相应的操作 | 无 | 无 |

## 5. 使用方法

### 5.1 命令行使用

```bash
# 安装知识引擎
python .trae/skills/knowledge-engine-manager/scripts/main.py install [--root <project_root>]

# 更新知识引擎
python .trae/skills/knowledge-engine-manager/scripts/main.py update [--root <project_root>]

# 重新安装知识引擎
python .trae/skills/knowledge-engine-manager/scripts/main.py reinstall [--root <project_root>]
```

### 5.2 TRAE 环境使用

```
# 安装知识引擎
/skill knowledge-engine-manager install
或
/skill knowledge-engine-manager 安装知识库

# 更新知识引擎
/skill knowledge-engine-manager update
或
/skill knowledge-engine-manager 更新知识库

# 重新安装知识引擎
/skill knowledge-engine-manager reinstall
或
/skill knowledge-engine-manager 重新安装知识库
```

### 5.3 Agent 执行流程

1. **调用主脚本**：
    - 优先尝试运行: `python .trae/skills/knowledge-engine-manager/scripts/main.py [install|update|reinstall]`
    - 如果是在开发调试模式下，运行: `python knowledge-engine-manager/scripts/main.py [install|update|reinstall]`

2. **检查输出**:
    - 若输出 `NEED_TECH_STACK_ANALYSIS`:
        - 调用 `LS` 列出项目根目录文件
        - 查找 `package.json`, `requirements.txt`, `pom.xml`, `go.mod` 等
        - 读取这些文件内容
        - 分析主要技术栈（语言、框架、核心库）
        - 按照 `tech-stack.ts.md` 格式生成内容
        - 写入 `.trae/rules/core/tech-stack.ts.md`
    
    - 若输出 `DIRTY_STATE_DETECTED`:
        - 询问用户：“检测到 `knowledge-engine` 有未提交的修改，您希望提交 (Commit) 还是丢弃 (Discard)？”
        - 若用户选择提交：引导用户输入 Commit Message，然后调用 `git add .` 和 `git commit` (在 `knowledge-engine` 目录下)
        - 若用户选择丢弃：调用 `git reset --hard` (在 `knowledge-engine` 目录下)
        - 完成后，再次运行 `update` 命令
    
    - 若输出 `KE_EXISTS`:
        - 询问用户：“检测到 `knowledge-engine` 目录已存在，您希望：
          1. 重新安装（会覆盖现有目录）
          2. 更新仓库（与远程仓库双向同步）
          3. 取消安装流程”
        - 若用户选择重新安装：运行 `python .trae/skills/knowledge-engine-manager/scripts/main.py reinstall`
        - 若用户选择更新仓库：运行 `python .trae/skills/knowledge-engine-manager/scripts/main.py update`
        - 若用户选择取消：终止操作

3. **结果反馈**：向用户汇报操作结果

## 6. 配置与扩展

### 6.1 配置文件

技能支持通过命令行参数进行配置：
- `--root`：指定项目根目录，默认为当前目录

### 6.2 扩展方式

1. **添加新模板**：在 `templates` 目录下添加新的模板文件，并在 `directory_checker.py` 中的 `TEMPLATE_MAPPING` 中添加相应的映射

2. **扩展依赖管理**：在 `dependency_manager.py` 中添加对新包管理器的支持

3. **增加新功能**：在 `main.py` 中添加新的命令行参数和相应的处理逻辑

## 7. 故障排除

### 7.1 常见问题

| 问题 | 可能原因 | 解决方案 |
| :--- | :--- | :--- |
| Git 命令执行失败 | 网络问题或权限问题 | 检查网络连接和 VPN 状态，确保有足够的权限 |
| 依赖安装失败 | 包管理器不存在或网络问题 | 安装相应的包管理器，检查网络连接 |
| 目录创建失败 | 权限问题 | 以管理员身份运行命令 |
| 子模块同步失败 | 本地更改未提交 | 提交或丢弃本地更改后重试 |

### 7.2 错误日志

错误信息会被记录到 `.trae/logs/error-log.md` 文件中，可通过查看该文件了解详细的错误信息。

## 8. 结论

Knowledge Engine Manager 技能为用户提供了一个便捷的方式来管理知识引擎的安装、更新和维护。它通过自动化的目录结构检查、模板部署、Git 子模块管理和依赖安装，大大简化了知识引擎的管理流程。

该技能的设计考虑了各种边缘情况，如 `.gitignore` 排除的目录、未提交的更改等，并提供了相应的处理机制。同时，它还支持与用户的交互，根据用户的选择执行相应的操作。

通过使用 Knowledge Engine Manager 技能，用户可以更加专注于知识内容的管理和应用，而不是繁琐的技术操作，从而提高开发效率和知识管理的质量。
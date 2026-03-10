---
alwaysApply: true
---
# 项目规则路由 (Rules Router)

> 本文档采用**混合索引 (Hybrid Indexing)**。Layer 1 仅展示核心规范和领域入口，Layer 2 规则请在对应领域目录下使用 `LS` 查找。

## 1. 核心规范 (Core)
| 规范名称 | 文件路径 | 关键词 |
| :--- | :--- | :--- |
| **技术栈** | [tech-stack.ts.md](core/tech-stack.ts.md) | `stack`, `python` |
| **代码风格** | [coding-style.ts.md](core/coding-style.ts.md) | `style`, `naming` |
| **工作流** | [workflows.ts.md](core/workflows.ts.md) | `git`, `commit`, `log` |

## 2. 领域分类 (Domains)
| 领域名称 | 描述 | 关键词 |
| :--- | :--- | :--- |
| **Graphics** | 2D/3D 图形 (Canvas, Konva, WebGL) | `graphics`, `canvas`, `konva` |
| **Media** | 多媒体 (FFmpeg, YYEVA, Audio, Video) | `media`, `ffmpeg`, `video` |
| **UI** | 界面与交互 (Vue, 组件库) | `ui`, `vue`, `components` |
| **Engineering** | 工程化 (Vite, CI/CD, WebWorker) | `engineering`, `vite`, `cicd` |
| **Core** | 核心架构 | `core`, `architecture` |
| **Data** | 数据与协议 | `data`, `protocol` |
| **Business** | 业务规则 | `business`, `rules` |

## 3. 技能索引 (Skills Index)
| 技能名称 | 目录入口 | 功能描述 |
| :--- | :--- | :--- |
| **Coder 技能** | [coder/](coder/) | 脚本工具, 模板 |
| **完整性检查** | [integrity-check/](integrity-check/) | 发布脚本, 变更扫描 |
| **知识医生** | [knowledge-doctor/](knowledge-doctor/) | 扫描器, 处理工具 |
| **知识园丁** | [knowledge-gardener/](knowledge-gardener/) | 知识管理, 模板 |
| **知识管理员** | [knowledge-librarian/](knowledge-librarian/) | 归档, 批处理, 清理 |
| **技能创建器** | [skill-creator/](skill-creator/) | 技能初始化, 打包, 验证 |
| **Web 应用测试** | [webapp-testing/](webapp-testing/) | 测试脚本, 示例 |
| **知识引擎管理** | [knowledge-engine-manager/](knowledge-engine-manager/) | 安装, 更新, 依赖管理 |

> **Coder 使用说明**：
> 1.  识别用户请求的领域。
> 2.  导航到相应的目录。
> 3.  执行 `LS` 列出规则文件和子目录。
> 4.  **索引模式**：如果看到 `scripts/` 或 `templates/` 目录，直接读取相关文件。
> 5.  否则，直接读取每个技能的 `SKILL.md` 文件。

> **Coder 指引**:
> 1.  识别用户请求所属的领域。
> 2.  导航到对应的 `modules/<domain>/` 目录。
> 3.  执行 `LS` 列出规则文件和子目录。
> 4.  **索引模式**: 如果看到子目录（如 `canvas/`），先读取其 `index.ts.md` 入口文件。
> 5.  否则，直接读取相关的 `.ts.md` 文件。

## 4. 日志与记录 (Logs)
| 日志名称 | 文件路径 | 关键词 |
| :--- | :--- | :--- |
| **错误日志** | [error-log.md](logs/error-log.md) | `bug`, `fix` |
| **决策日志** | [decision-log.md](logs/decision-log.md) | `adr`, `arch` |
| **变更日志** | [UPDATE_LOG.md](../logs/UPDATE_LOG.md) | `log`, `change` |
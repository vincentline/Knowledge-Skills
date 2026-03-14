---
alwaysApply: true
---

# 项目架构文档 (Architecture)

> 类脑知识引擎 - 让 AI Agent 具备自我进化能力

## 1. 系统概述 (System Overview)

### 1.1 项目目标
构建一个**类脑知识引擎**，让 AI Agent 具备：
- **跨会话记忆**：记住其他会话发生的事情
- **项目上下文感知**：会话开始自动了解项目状态
- **自我进化能力**：从交互中学习，持续优化
- **知识沉淀**：将经验转化为可复用的规则

### 1.2 核心理念
```
设计规则 ≠ 遵循规则
→ 需要建立"先检查再行动"的习惯
→ 需要主动更新记忆，而不是被动等待
```

## 2. 技术架构 (Technical Architecture)

### 2.1 整体架构

```
┌─────────────────────────────────────────────────────────────┐
│                      AI Agent (Trae IDE)                    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │  记忆系统   │  │  知识引擎   │  │  技能系统   │         │
│  │  (Memory)   │  │  (Rules)    │  │  (Skills)   │         │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘         │
│         │                │                │                │
│         └────────────────┼────────────────┘                │
│                          ↓                                  │
│              ┌─────────────────────┐                       │
│              │   自我进化机制      │                       │
│              │ (Self-Evolution)    │                       │
│              └─────────────────────┘                       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 记忆系统架构

```
.trae/memory/
├── SUMMARY.md          # 记忆摘要（启动时读取，约30行）
├── sessions/           # 会话记忆（发生了什么）
│   └── YYYY-MM-DD.md   # 按日期记录
├── archive/            # 归档记忆（30天+）
│   └── YYYY-MM/        # 按月份归档
├── capabilities/       # 能力记忆（会做什么）
├── decisions/          # 决策记忆（为什么这么做）
└── patterns/           # 模式记忆（规律总结）
```

**记忆生命周期**：
| 阶段 | 时间范围 | 处理方式 |
|:---|:---|:---|
| 热记忆 | 0-7 天 | 完整保留 |
| 温记忆 | 7-30 天 | 压缩摘要 |
| 冷记忆 | 30 天+ | 归档存储 |

### 2.3 知识引擎架构

```
.trae/rules/
├── core-rules.md       # 核心原则（入口文件）
├── index.md            # 规则路由索引
├── core/               # 核心规范
│   ├── architecture.md
│   ├── coding-style.ts.md
│   ├── tech-stack.ts.md
│   ├── workflows.ts.md
│   └── self-evolution.ts.md
├── modules/            # 领域规则
│   ├── core/
│   ├── engineering/
│   ├── graphics/
│   ├── media/
│   └── ui/
└── inbox/              # 待归档经验
```

**规则优先级**：`core/` > `modules/` > `inbox/`

### 2.4 技能系统架构

```
.trae/skills/
├── session-startup/    # 会话启动检查
├── coder/              # 代码开发
├── knowledge-gardener/ # 知识捕获
├── knowledge-librarian/# 知识归档
├── knowledge-doctor/   # 知识诊断
├── integrity-check/    # 完整性检查
├── skill-creator/      # 技能创建
├── webapp-testing/     # Web测试
└── knowledge-engine-manager/ # 引擎管理
```

**技能结构**：
```
skill-name/
├── SKILL.md            # 技能说明
├── scripts/            # Python脚本
└── templates/          # 模板文件
```

## 3. 目录结构 (Directory Structure)

```
Knowledge-Skills/
├── .trae/                    # 知识引擎核心
│   ├── memory/               # 记忆系统
│   ├── rules/                # 知识引擎（规则库）
│   ├── skills/               # 技能系统
│   ├── temp/                 # 临时文件
│   └── trash/                # 回收站
├── scripts/                  # 项目脚本
│   ├── GET_TIME.py           # 获取北京时间
│   ├── git-push.py           # Git推送
│   └── start_server.py       # 启动服务器
├── ENVIRONMENT.md            # 环境说明
├── README.md                 # 项目说明
├── TESTING_RULES.md          # 测试规则
└── requirements.txt          # Python依赖
```

## 4. 核心模块 (Core Modules)

### 4.1 会话启动模块 (session-startup)
**职责**：每次会话开始时激活记忆、感知项目上下文

**流程**：
```
1. 读取 SUMMARY.md（约30行）
2. 扫描项目变更（git status + log -3）
3. 向用户报告摘要（1-2句话）
```

**关键脚本**：
- `startup_check.py` - 启动检查
- `update_summary.py` - 更新摘要
- `memory_lifecycle.py` - 记忆生命周期管理

### 4.2 知识捕获模块 (knowledge-gardener)
**职责**：从交互中提取有价值的经验，暂存到 Inbox

**触发时机**：
- 完成重要任务后
- 解决复杂问题后
- 用户纠正后

### 4.3 知识归档模块 (knowledge-librarian)
**职责**：将 Inbox 中的经验整理归档到长期规则库

**流程**：
```
Inbox → 分析 → 分类 → 写入 rules/modules/ 或 rules/core/
```

### 4.4 自我进化模块 (self-evolution)
**职责**：驱动 Agent 持续学习和优化

**机制**：
- 跨会话记忆
- 项目上下文感知
- 自主搜索能力
- 自我反思机制

## 5. 数据流 (Data Flow)

### 5.1 会话启动流程
```
用户消息 → 读取 SUMMARY.md → 扫描 Git → 报告摘要 → 回应用户
                ↓
         按需深入读取详情
```

### 5.2 知识沉淀流程
```
交互发生 → 识别价值 → 捕获到 Inbox → 归档到 Rules → 更新 SUMMARY
```

### 5.3 记忆生命周期流程
```
热记忆(0-7天) → 温记忆(7-30天) → 冷记忆(30天+)
     ↓              ↓               ↓
  完整保留      压缩摘要        归档存储
```

## 6. 部署架构 (Deployment Architecture)

### 6.1 环境要求
- Python 3.10+
- Git
- Trae IDE

### 6.2 安装方式
```bash
# 克隆项目
git clone https://github.com/vincentline/Knowledge-Skills.git

# 安装依赖
pip install -r requirements.txt
```

### 6.3 配置文件
- `.trae/rules/core-rules.md` - 核心规则（自动加载）
- `.trae/memory/user-profile.md` - 用户画像

## 7. 扩展规划 (Future Plans)

### 7.1 短期优化
- [ ] 完善启动检查清单的自动化
- [ ] 创建进化日志记录进化历程
- [ ] 优化摘要生成算法

### 7.2 中期目标
- [ ] 实现知识图谱可视化
- [ ] 增强跨项目知识迁移
- [ ] 支持多语言规则

### 7.3 长期愿景
- [ ] 构建知识共享社区
- [ ] 实现 Agent 自主决策
- [ ] 支持多 Agent 协作

---

*最后更新: 2026-03-14*

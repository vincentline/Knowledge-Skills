---
name: session-startup
description: 会话启动时执行记忆激活和上下文感知。当收到用户第一条消息、或上下文中无 startup-check 标记时，必须调用此技能。确保 Agent 在了解项目上下文后再开始工作。
---

# Session Startup Skill

会话启动时强制执行记忆激活，确保具备完整的项目上下文。

## 执行流程

### Phase 1: 记忆激活
```
1. Read .trae/memory/SUMMARY.md
2. 根据关键词触发读取详情（见关键词触发表）
```

### Phase 2: 项目感知（可选）
```
3. git status --short
4. git log -3 --oneline
```

### Phase 3: 声明与标记
```
5. 回复开头声明：🧠 记忆已激活
6. 回复末尾标记：<!-- startup-check: done -->
```

## 关键词触发表

| 用户消息包含 | 触发读取 |
|:---|:---|
| `游戏`/`王者`/`荣耀`/英雄名 | `memory/user-profile.md` |
| `环境`/`系统`/`VPN` | `memory/user-profile.md` |
| `上次`/`之前`/`继续` | `memory/sessions/最新文件` |

## 输出格式

```markdown
🧠 记忆已激活

### 最近活动
- [日期] 活动1

### 待办事项
- [ ] 待办1

[回复内容...]

<!-- startup-check: done -->
```

## 错误处理

| 情况 | 处理 |
|:---|:---|
| 记忆文件不存在 | 创建新文件，报告"首次会话" |
| git 命令失败 | 跳过变更扫描 |

## 脚本参考

- `scripts/startup_check.py` - 执行启动检查并生成报告
- `scripts/update_summary.py` - 更新 SUMMARY.md
- `scripts/memory_lifecycle.py` - 记忆生命周期管理

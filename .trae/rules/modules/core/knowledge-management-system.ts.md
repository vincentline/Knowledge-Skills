---
module_name: KnowledgeManagementSystem
type: guide
domain: core,engineering
tags: knowledge-management,automation,workflow
version: 1.0.0
---

# 知识管理系统操作指南 (How-to Guide)

```typescript
/**
 * 知识管理系统操作指南规范
 * @description 实现知识管理的自动化工作流和最佳实践
 */
export interface KnowledgeManagementSystem {
  /**
   * 系统架构
   */
  architecture: {
    /** 核心组件 */
    components: string[];
    /** 工作流流程 */
    workflow: string[];
  };

  /**
   * 技能集成
   */
  skillIntegration: {
    /** 技能间协作流程 */
    collaboration: string[];
    /** 状态反馈机制 */
    stateFeedback: string[];
  };

  /**
   * 子模块管理
   */
  submoduleManagement: {
    /** 迁移流程 */
    migration: string[];
    /** 标准位置 */
    standardLocation: string;
  };

  /**
   * 变更管理
   */
  changeManagement: {
    /** 变更捕获策略 */
    captureStrategy: string[];
    /** 提交推送流程 */
    commitPush: string[];
  };

  /**
   * 本地化支持
   */
  localization: {
    /** 支持的语言 */
    languages: string[];
    /** 本地化策略 */
    strategy: string[];
  };

  /**
   * 错误处理
   */
  errorHandling: {
    /** 错误类型 */
    errorTypes: string[];
    /** 处理策略 */
    handlingStrategy: string[];
  };

  /**
   * 适用场景
   */
  useCases: string[];
}
```

## 1. 系统架构
- **核心组件**: 知识园丁、图书管理员、知识医生、技能创建器
- **工作流流程**: 知识捕获 → 结构化重写 → 归档 → 诊断

## 2. 技能集成
- **技能间协作流程**:
  1. 知识园丁完成工作后询问用户
  2. 用户确认后调用图书管理员
  3. 图书管理员完成后调用知识医生
- **状态反馈机制**:
  - 使用 `[STATE]` 和 `[ACTION]` 标记系统状态
  - 提供清晰的操作建议和下一步指导

## 3. 子模块管理
- **迁移流程**:
  1. 清理现有子模块
  2. 清理Git子模块缓存
  3. 清理Git配置中的子模块配置
  4. 重新添加子模块到新路径
- **标准位置**: knowledge-engine目录

## 4. 变更管理
- **变更捕获策略**:
  - 执行 `git add -A` 暂存所有变更
  - 捕获暂存区和非暂存区的所有修改
- **提交推送流程**:
  - 生成标准提交消息
  - 执行 `git commit` 提交变更
  - 执行 `git push` 推送到远程仓库

## 5. 本地化支持
- **支持的语言**: 中文、英文
- **本地化策略**:
  - 将脚本注释和输出信息从英文改为中文
  - 提供多语言支持的配置选项

## 6. 错误处理
- **错误类型**:
  - 子模块迁移失败
  - 变更提交失败
  - 技能执行错误
- **处理策略**:
  - 详细的错误日志记录
  - 提供明确的错误原因和解决方案
  - 系统状态的实时反馈

## 7. 适用场景
- 技能集成与自动化工作流构建
- 子模块管理与迁移
- 变更管理与版本控制
- 多语言支持与本地化
- 错误处理与状态反馈

## 8. 代码示例
### 技能集成示例
```python
# 知识园丁完成工作后询问用户
print("[STATE] KE_MIGRATION_NEEDED")
print("[ACTION] Agent should migrate submodule from .trae/skills to knowledge-engine")

# 图书管理员完成工作后调用知识医生
print("Calling Knowledge Doctor for diagnosis...")
doctor_result = subprocess.run([sys.executable, doctor_scanner, "--full"])
```

### 子模块迁移示例
```python
def migrate_submodule(root_dir, old_path, new_path):
    # 1. 清理现有子模块
    # 2. 清理Git子模块缓存
    # 3. 清理Git配置中的子模块配置
    # 4. 重新添加子模块到新路径
    cmd = f"git submodule add {REPO_URL} {new_path}"
    if run_git_command(cmd, cwd=root_dir) is not None:
        run_git_command("git submodule update --init --recursive", cwd=root_dir)
        return True
    return False
```

### 变更管理示例
```python
# 总是执行git add -A以确保所有变更都被暂存
print("ℹ️  正在执行 git add -A 暂存所有变更...")
subprocess.run(["git", "add", "-A"], capture_output=True, text=True, encoding='utf-8', check=True)

# 生成提交消息并推送
run_git_command("git commit -F .git/COMMIT_EDITMSG_TEMP", cwd=root_dir)
run_git_command("git push origin main", cwd=root_dir)
```
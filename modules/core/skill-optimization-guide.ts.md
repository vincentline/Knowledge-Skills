---
module_name: SkillOptimizationGuide
type: guide
domain: core
tags: skill,optimization,agent
version: 1.0.0
---

# Skill 优化与执行概率提升指南 (How-to Guide)

```typescript
/**
 * Skill 优化与执行概率提升指南规范
 * @description 提供Skill创建和优化的最佳实践，提高Agent识别和执行Skill的概率
 */
export interface SkillOptimizationGuide {
  /**
   * 前置条件
   */
  prerequisites: {
    /** 必需的环境要求 */
    environment: string[];
    /** 必需的基础知识储备 */
    knowledge: string[];
  };

  /**
   * 优化策略
   * @description 按类别组织的Skill优化方法
   */
  optimizationStrategies: {
    /** 元数据优化 */
    metadata: {
      name: string;
      description: string;
    };
    /** 格式使用策略 */
    formatting: string[];
    /** 结构优化 */
    structure: string[];
    /** Agent理解增强 */
    agentUnderstanding: string[];
  };

  /**
   * 最佳实践
   * @description 推荐的Skill创建和优化方法
   */
  bestPractices: string[];

  /**
   * 注意事项
   * @description 需要避免的问题和风险
   */
  caveats: string[];
}
```

## 1. 前置条件 (Prerequisites)
- **Environment**: 任意支持Trae IDE的环境
- **Knowledge**: 基本的Markdown语法、Skill创建基础知识

## 2. 优化策略 (Optimization Strategies)

### 2.1 元数据优化
- **name字段**: 使用简洁明确的名称，包含核心关键词，严格遵循小写字母+连字符格式
- **description字段**: 详细说明功能和使用场景，包含用户可能使用的高频词汇，控制在100-200字符

### 2.2 格式使用策略
- **表格**: 用于结构化信息（参数说明、对比分析、配置项）
- **关键定义**: 使用加粗（**）强调核心概念，斜体（*）用于次要强调
- **Task任务**: 使用有序列表，明确步骤顺序和依赖关系
- **Todo任务**: 使用无序列表，标记待完成项
- **SOP**: 使用多级编号，详细描述标准化操作流程
- **命令**: 使用代码块，指定语言并添加注释
- **Markdown标记**: 合理使用列表、引用块、分隔线等

### 2.3 结构优化
- **层次分明**: 使用H1-H4标题创建清晰的层级结构
- **信息优先级**: 核心功能、触发条件放在顶部，执行流程、示例放在中部
- **可读性**: 控制段落长度，合理使用空行，创建视觉层次

### 2.4 Agent理解增强
- **明确触发信号**: 在不同位置重复核心关键词，具体说明用户可能的输入表达方式
- **执行逻辑清晰**: 将复杂任务分解为可执行步骤，说明不同输入的处理逻辑
- **示例驱动**: 提供用户可能的输入语句和预期输出结果

## 3. 最佳实践 (Best Practices)
- 保持格式一致性，统一列表风格和标题命名
- 内容精简，移除冗余信息，保留核心指令
- 定期测试和迭代，根据Agent反馈调整格式和内容
- 组合使用不同格式，如表格+列表、加粗+引用、代码块+注释

## 4. 注意事项 (Caveats)
- 避免过度使用Markdown标记，确保重点突出
- 控制内容长度，确保Agent能有效处理
- 确保元数据准确反映Skill的核心功能和使用场景

## 5. 示例 (Examples)

### 元数据示例
```yaml
---
name: chinese-essay-writing
description: 帮助用户撰写中文作文，包括议论文、记叙文、说明文等多种文体，提供写作技巧和修改建议。当用户提到写作文、修改作文、作文技巧时使用。
---
```

### 格式示例
**表格示例**：
| 场景 | 处理方式 | 注意事项 |
|------|---------|---------|
| 代码审查 | 检查语法、逻辑、性能 | 关注边界情况 |
| 文档生成 | 提取要点、结构化输出 | 保持格式一致性 |

**SOP示例**：
```markdown
## SOP：代码审查流程
1. **准备阶段**
   1.1 接收代码文件
   1.2 了解代码功能
2. **审查阶段**
   2.1 语法检查
   2.2 逻辑分析
   2.3 性能评估
3. **输出阶段**
   3.1 生成审查报告
   3.2 提供改进建议
```
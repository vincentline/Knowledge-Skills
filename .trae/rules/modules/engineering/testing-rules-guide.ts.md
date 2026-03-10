---
module_name: TestingRulesGuide
type: guide
domain: engineering
tags: testing,rules,workflow
version: 1.0.0
---

# 测试规则操作指南 (How-to Guide)

```typescript
/**
 * 测试规则操作指南规范
 * @description 标准化测试流程，提高测试效率和质量
 */
export interface TestingRulesGuide {
  /**
   * 前置条件
   */
  prerequisites: {
    /** 必需的环境要求 */
    environment: string[];
    /** 必需的基础知识储备 */
    knowledge?: string[];
  };

  /**
   * 操作步骤序列
   * @description 按顺序执行的测试流程
   */
  steps: Array<{
    /** 步骤名称 */
    name: string;
    /** 操作指令或代码片段 */
    command?: string;
    /** 预期结果 */
    expectedResult: string;
    /** 注意事项或潜在风险 */
    notes?: string;
  }>;

  /**
   * 验证方法
   * @description 确认测试成功的检查点
   */
  verification: string[];

  /**
   * 工具选择策略
   */
  toolSelection: {
    /** 优先工具 */
    preferred: string;
    /** 备选工具 */
    alternative: string;
  };

  /**
   * 资源管理
   */
  resourceManagement: {
    /** 测试文件存放位置 */
    testFilesLocation: string;
    /** 支持的文件类型 */
    supportedTypes: string[];
  };

  /**
   * 测试后处理
   */
  postProcessing: string[];

  /**
   * 常见问题解决方案
   */
  troubleshooting: Array<{
    /** 问题描述 */
    issue: string;
    /** 解决方案 */
    solution: string;
  }>;
}
```

## 1. 前置条件 (Prerequisites)
- **Environment**: IDE环境、webapp-testing技能
- **Knowledge**: 基本测试概念、项目结构了解

## 2. 操作步骤 (Step-by-Step)

### Step 1: 检查测试环境
- 确认IDE内置测试工具可用性
- 准备webapp-testing技能作为备选

### Step 2: 执行测试
- 使用真实浏览器模式：`browser-use --browser real`
- 从`test_files`目录获取测试文件
- 执行测试操作
- 检查测试结果

### Step 3: 测试后处理
1. 删除测试中添加的冗余调试代码
2. 在webapp-testing技能中新建或优化测试模板
3. 执行提交GitHub操作
4. 提醒用户整理经验文档

## 3. 验证 (Verification)
- 测试执行成功，无错误
- 测试覆盖了目标功能
- 测试后处理完成

## 4. 工具选择策略
- **优先工具**: IDE内置测试工具
- **备选工具**: webapp-testing技能

## 5. 资源管理
- **测试文件存放位置**: 项目根目录下的`test_files`
- **支持的文件类型**: svga、图片、视频等

## 6. 常见问题解决方案
- **测试文件找不到**: 检查`test_files`目录，确保测试文件存在
- **浏览器测试失败**: 使用`--browser real`参数启用真实浏览器模式
- **测试结果不稳定**: 检查测试环境和网络连接

## 7. 适用场景
- 新项目测试流程建立
- 测试工具选择指导
- 测试资源管理规范
- 测试问题排查
- 测试流程优化
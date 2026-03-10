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
   * 浏览器模式配置
   */
  browserMode: {
    /** 是否禁用无头模式 */
    disableHeadless: boolean;
    /** 浏览器使用参数 */
    useParams: string;
  };

  /**
   * 测试资源管理
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
   * 故障排除
   */
  troubleshooting?: Array<{
    /** 错误现象或报错信息 */
    symptom: string;
    /** 根本原因 */
    cause: string;
    /** 解决方案 */
    solution: string;
  }>;
}
```

## 1. 前置条件 (Prerequisites)
- **Environment**: IDE环境、webapp-testing技能、test_files目录
- **Knowledge**: 基本测试概念、项目结构了解

## 2. 操作步骤 (Step-by-Step)

### Step 1: 检查内置测试工具
- 查看IDE是否提供内置测试工具
- 确认工具可用性和功能

### Step 2: 查找现有测试资源
- 检查项目内测试模板、测试用例、测试流程
- 参考现有测试资源，避免重复工作

### Step 3: 选择测试工具
- 优先使用IDE内置测试工具
- 无内置工具时，使用webapp-testing技能

### Step 4: 执行测试
- 使用真实浏览器模式：`browser-use --browser real`
- 从`test_files`目录获取所需测试文件
- 执行测试操作
- 检查测试结果

### Step 5: 测试后处理
1. 删除测试中添加的冗余调试代码
2. 在webapp-testing全局技能中新建或优化测试模板
3. 执行【提交GitHub】操作
4. 提醒用户整理经验文档

## 3. 验证 (Verification)
- 测试执行成功，无错误
- 测试覆盖了目标功能
- 测试后处理完成
- 测试流程符合规范

## 4. 工具选择策略
- **优先工具**: IDE内置测试工具
- **备选工具**: webapp-testing技能

## 5. 浏览器模式配置
- **禁用无头模式**: 是
- **使用参数**: `--browser real`

## 6. 测试资源管理
- **测试文件存放位置**: 项目根目录下的`test_files`
- **支持的文件类型**: svga、图片、视频等

## 7. 常见问题 (Troubleshooting)
### Q: 测试文件找不到
- **Cause**: 未在`test_files`目录中查找
- **Solution**: 检查`test_files`目录，确保测试文件存在

### Q: 浏览器测试失败
- **Cause**: 使用了无头浏览器模式
- **Solution**: 添加`--browser real`参数使用真实浏览器

### Q: 测试后代码混乱
- **Cause**: 未清理调试代码
- **Solution**: 测试完成后删除冗余调试代码

## 8. 适用场景
- 新项目测试流程建立
- 测试工具选择指导
- 测试资源管理规范
- 测试问题排查
- 测试流程优化
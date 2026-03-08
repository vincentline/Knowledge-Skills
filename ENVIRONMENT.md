# 环境依赖说明

## 1. 基础环境

| 依赖 | 版本 | 用途 | 安装方法 |
| :--- | :--- | :--- | :--- |
| Python | 3.8+ | 运行技能脚本 | [Python 官网](https://www.python.org/downloads/) |
| Node.js | LTS 版本 | 启动前端开发服务器 | [Node.js 官网](https://nodejs.org/en/download/) |
| Git | 2.0+ | 版本控制和变更检测 | [Git 官网](https://git-scm.com/downloads/) |

## 2. Python 依赖

### 安装方法
```bash
pip install -r requirements.txt

# 初始化 Playwright 浏览器
playwright install
```

### 依赖包详情
| 包名 | 版本 | 用途 | 涉及技能 |
| :--- | :--- | :--- | :--- |
| pyyaml | 6.0.1 | YAML 解析（技能验证） | skill-creator |
| playwright | 1.44.0 | 浏览器自动化测试 | webapp-testing |

## 3. 外部工具

| 工具 | 版本 | 用途 | 安装方法 | 涉及技能 |
| :--- | :--- | :--- | :--- | :--- |
| GitHub CLI (gh) | 2.0+ | 自动合并发布 PR | [GitHub CLI 官网](https://cli.github.com/) | integrity-check |
| npm | 随 Node.js 安装 | 启动前端开发服务器 | 随 Node.js 安装 | webapp-testing |

## 4. 系统配置

### GitHub CLI 配置
```bash
# 登录 GitHub CLI
gh auth login

# 验证登录状态
gh auth status
```

### Git 配置
```bash
# 配置用户信息
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

## 5. 运行验证

### 验证 Python 依赖
```bash
pip list | grep -E "pyyaml|playwright"
```

### 验证外部工具
```bash
# 检查 GitHub CLI
gh --version

# 检查 npm
npm --version

# 检查 Git
git --version
```

## 6. 常见问题

### Playwright 浏览器安装失败
```bash
# 尝试指定浏览器安装
playwright install chromium

# 或者使用代理
PLAYWRIGHT_DOWNLOAD_HOST=https://playwright.azureedge.net/builds playwright install
```

### GitHub CLI 登录问题
- 确保已安装最新版本的 GitHub CLI
- 检查网络连接是否正常
- 尝试使用 `gh auth login --with-token` 方式登录

### 端口被占用
- 检查是否有其他服务占用了 5173 或 3000 端口
- 使用 `netstat -ano | findstr :5173` 查看端口占用情况
- 终止占用端口的进程或修改测试脚本使用其他端口

## 7. 维护说明

- 当添加新的 Python 依赖时，更新 `requirements.txt` 文件
- 当添加新的外部工具时，更新本说明文件
- 定期检查并更新依赖版本以确保兼容性

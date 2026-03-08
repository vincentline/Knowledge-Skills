# -*- coding: utf-8 -*-
"""Git 管理模块

该模块负责：
1. 执行 Git 命令
2. 检查 Git 仓库状态
3. 安装和同步 Knowledge-Skills 子模块
4. 提交和丢弃子模块更改

使用方法：
    from git_manager import install_submodule, sync_submodule
    install_submodule(root_dir)
    sync_submodule(root_dir)
"""

import os
import subprocess
from error_handler import handle_exception, log_message

# Knowledge-Skills 仓库地址
REPO_URL = "https://github.com/vincentline/Knowledge-Skills"
SKILLS_DIR = ".trae/skills"  # 技能目录相对路径

@handle_exception
def run_git_command(command, cwd=None):
    """执行 Git 命令并返回输出
    
    Args:
        command (str): Git 命令字符串
        cwd (str, optional): 命令执行的工作目录. Defaults to None.
    
    Returns:
        str or None: 命令执行成功返回输出结果，失败返回 None
    """
    log_message(f"Executing: {command}", "INFO")
    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            shell=True,
            capture_output=True,
            text=True,
            encoding='utf-8', # 强制使用 utf-8
            errors='replace'
        )
        if result.returncode != 0:
            log_message(f"Git command failed: {result.stderr}", "ERROR")
            return None
        return result.stdout.strip()
    except Exception as e:
        log_message(f"Subprocess failed: {str(e)}", "ERROR")
        return None

@handle_exception
def check_git_status(root_dir):
    """检查是否为 Git 仓库
    
    Args:
        root_dir (str): 项目根目录路径
    
    Returns:
        bool: 是 Git 仓库返回 True，否则返回 False
    """
    git_dir = os.path.join(root_dir, ".git")
    if not os.path.exists(git_dir):
        log_message("Not a git repository.", "WARNING")
        return False
    return True

@handle_exception
def check_dirty(root_dir):
    """检查 .trae/skills 是否有未提交更改
    
    Args:
        root_dir (str): 项目根目录路径
    
    Returns:
        bool: 有未提交更改返回 True，否则返回 False
    """
    skills_path = os.path.join(root_dir, SKILLS_DIR)
    if not os.path.exists(skills_path):
        return False
        
    # 1. 进入子模块检查内部状态
    output_inner = run_git_command("git status --porcelain", cwd=skills_path)
    if output_inner:
        log_message(f"Uncommitted changes in skills directory: {output_inner}", "WARNING")
        return True
        
    return False

@handle_exception
def install_submodule(root_dir):
    """安装 Knowledge-Skills 子模块
    
    策略：
    - 如果 .trae/skills 目录已存在且不为空，则跳过安装
    - 否则添加子模块并初始化
    
    Args:
        root_dir (str): 项目根目录路径
    
    Returns:
        bool: 安装成功返回 True，失败返回 False
    """
    # 检查 .trae/skills 是否已存在（可能是空目录）
    skills_path = os.path.join(root_dir, SKILLS_DIR)
    if os.path.exists(skills_path) and os.listdir(skills_path):
        log_message("Skills directory is not empty. Skipping installation.", "WARNING")
        return True
        
    log_message("Installing submodule...", "INFO")
    
    # 确保父目录存在
    os.makedirs(os.path.dirname(skills_path), exist_ok=True)

    cmd = f"git submodule add {REPO_URL} {SKILLS_DIR}"
    if run_git_command(cmd, cwd=root_dir) is not None:
        # 初始化
        run_git_command("git submodule update --init --recursive", cwd=root_dir)
        log_message("Submodule installed successfully.", "SUCCESS")
        return True
    return False

@handle_exception
def sync_submodule(root_dir):
    """同步子模块 (Pull & Push)
    
    步骤：
    1. 从远程拉取最新代码
    2. 如果有本地提交，则推送到远程
    
    Args:
        root_dir (str): 项目根目录路径
    
    Returns:
        bool: 同步成功返回 True，失败返回 False
    """
    skills_path = os.path.join(root_dir, SKILLS_DIR)
    if not os.path.exists(skills_path):
        log_message("Skills directory not found.", "ERROR")
        return False
        
    log_message("Syncing submodule...", "INFO")
    
    # 1. Pull
    if run_git_command("git pull origin main", cwd=skills_path) is None:
        return False
        
    # 2. Push (尝试)
    # 只有当有新的本地 commit 时才 push
    # 检查是否有这就领先于 origin/main
    ahead = run_git_command("git log origin/main..main", cwd=skills_path)
    if ahead:
        log_message("Local commits detected. Pushing to remote...", "INFO")
        if run_git_command("git push origin main", cwd=skills_path):
            log_message("Pushed successfully.", "SUCCESS")
    else:
        log_message("No local commits to push.", "INFO")
        
    return True

@handle_exception
def commit_changes(root_dir, message):
    """提交子模块更改
    
    Args:
        root_dir (str): 项目根目录路径
        message (str): 提交消息
    
    Returns:
        bool: 操作成功返回 True
    """
    skills_path = os.path.join(root_dir, SKILLS_DIR)
    
    run_git_command("git add .", cwd=skills_path)
    run_git_command(f'git commit -m "{message}"', cwd=skills_path)
    return True

@handle_exception
def discard_changes(root_dir):
    """丢弃子模块更改
    
    执行 git reset --hard 和 git clean -fd 命令
    
    Args:
        root_dir (str): 项目根目录路径
    
    Returns:
        bool: 操作成功返回 True
    """
    skills_path = os.path.join(root_dir, SKILLS_DIR)
    
    run_git_command("git reset --hard", cwd=skills_path)
    run_git_command("git clean -fd", cwd=skills_path)
    return True

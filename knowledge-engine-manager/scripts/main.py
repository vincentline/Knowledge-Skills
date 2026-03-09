# -*- coding: utf-8 -*-
"""知识引擎管理主脚本

该脚本是知识引擎管理器的入口点，支持以下操作：
1. install: 安装知识引擎
2. update: 更新知识引擎
3. reinstall: 重新安装知识引擎

使用方法：
    python main.py install [--root <project_root>]
    python main.py update [--root <project_root>]
    python main.py reinstall [--root <project_root>]

功能流程：
1. 检查并创建目录结构
2. 部署模板文件
3. 检查技术栈文件
4. 管理 Git 子模块
5. 安装项目依赖
"""

import os
import sys
import argparse
from error_handler import handle_exception, log_message
import directory_checker
import git_manager
import dependency_manager

# Knowledge Engine 目录
KNOWLEDGE_ENGINE_DIR = "knowledge-engine"

@handle_exception
def main():
    """主函数
    
    解析命令行参数并执行相应的操作
    """
    parser = argparse.ArgumentParser(description="Knowledge Engine Manager")
    parser.add_argument("action", choices=["install", "update", "reinstall"], help="Action to perform")
    parser.add_argument("--root", default=os.getcwd(), help="Project root directory")
    args = parser.parse_args()
    
    root_dir = os.path.abspath(args.root)
    # 获取脚本所在的目录 (scripts) 的父目录 (knowledge-engine-manager)
    skill_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    log_message(f"Starting Knowledge Engine Manager ({args.action})...", "HEADER")
    log_message(f"Project Root: {root_dir}")
    log_message(f"Skill Root: {skill_root}")
    
    # 1. 目录检查
    log_message("Step 1: Checking directories...", "HEADER")
    directory_checker.check_and_create_dirs(root_dir)
    directory_checker.deploy_templates(root_dir, skill_root)
    
    # 2. 技术栈检查 (由 Agent 后续处理，这里只做标记)
    tech_stack_path = os.path.join(root_dir, ".trae", "rules", "core", "tech-stack.ts.md")
    # 检查文件是否存在且内容是否为空（或仅包含空白字符）
    need_analysis = False
    if not os.path.exists(tech_stack_path):
        need_analysis = True
    else:
        with open(tech_stack_path, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            if not content:
                need_analysis = True
    
    if need_analysis:
        log_message("Tech Stack file is missing or empty.", "WARNING")
        # 输出特定标记供 Agent 识别
        print("NEED_TECH_STACK_ANALYSIS")
    
    # 3. 检查 knowledge-engine 目录
    ke_path = os.path.join(root_dir, KNOWLEDGE_ENGINE_DIR)
    ke_exists = os.path.exists(ke_path) and os.listdir(ke_path)
    
    # 4. Git 管理
    log_message("Step 2: Managing Knowledge Engine...", "HEADER")
    if not git_manager.check_git_status(root_dir):
        log_message("Skipping Git operations (not a git repo).", "WARNING")
    else:
        # 根据操作类型执行相应的 Git 操作
        if args.action == "install":
            if ke_exists:
                # 输出特定标记供 Agent 识别
                print("KE_EXISTS")
                log_message(f"{KNOWLEDGE_ENGINE_DIR} directory already exists.", "INFO")
                return
            else:
                # 安装子模块
                git_manager.install_submodule(root_dir, "install")
        elif args.action == "update":
            if not ke_exists:
                log_message(f"{KNOWLEDGE_ENGINE_DIR} directory not found. Cannot update.", "ERROR")
                return
            
            # 检查是否有未提交更改
            if git_manager.check_dirty(root_dir):
                # 输出特定标记供 Agent 识别
                print("DIRTY_STATE_DETECTED")
                log_message(f"Local changes detected in {KNOWLEDGE_ENGINE_DIR}. Please commit or discard them.", "WARNING")
                return
            
            # 同步子模块
            git_manager.install_submodule(root_dir, "update")
        elif args.action == "reinstall":
            # 重新安装子模块
            git_manager.install_submodule(root_dir, "reinstall")
            
    # 5. 依赖管理
    log_message("Step 3: Checking dependencies...", "HEADER")
    # 检查 knowledge-engine 目录下的依赖
    ke_path = os.path.join(root_dir, KNOWLEDGE_ENGINE_DIR)
    if os.path.exists(ke_path):
        dependency_manager.install_dependencies(ke_path)
    else:
        log_message(f"{KNOWLEDGE_ENGINE_DIR} directory not found. Skipping dependency installation.", "WARNING")
    
    log_message("Operation completed successfully!", "SUCCESS")

if __name__ == "__main__":
    main()

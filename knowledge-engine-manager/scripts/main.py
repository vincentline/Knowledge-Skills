import os
import sys
import argparse
from error_handler import handle_exception, log_message
import directory_checker
import git_manager
import dependency_manager

@handle_exception
def main():
    parser = argparse.ArgumentParser(description="Knowledge Engine Manager")
    parser.add_argument("action", choices=["install", "update"], help="Action to perform")
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
    
    # 3. Git 管理
    log_message("Step 2: Managing Knowledge Engine...", "HEADER")
    if not git_manager.check_git_status(root_dir):
        log_message("Skipping Git operations (not a git repo).", "WARNING")
    else:
        if args.action == "install":
            git_manager.install_submodule(root_dir)
        elif args.action == "update":
            if git_manager.check_dirty(root_dir):
                # 输出特定标记供 Agent 识别
                print("DIRTY_STATE_DETECTED")
                # 提示用户手动处理或由 Agent 引导
                log_message("Local changes detected in .trae/skills. Please commit or discard them.", "WARNING")
                return
            
            git_manager.sync_submodule(root_dir)
            
    # 4. 依赖管理
    log_message("Step 3: Checking dependencies...", "HEADER")
    dependency_manager.install_dependencies(root_dir)
    
    log_message("Operation completed successfully!", "SUCCESS")

if __name__ == "__main__":
    main()

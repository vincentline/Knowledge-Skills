import os
import subprocess
from error_handler import handle_exception, log_message

@handle_exception
def run_command(command, cwd=None):
    """执行命令"""
    log_message(f"Executing: {command}", "INFO")
    result = subprocess.run(
        command,
        cwd=cwd,
        shell=True,
        capture_output=True,
        text=True,
        encoding='utf-8',
        errors='replace'
    )
    if result.returncode != 0:
        log_message(f"Command failed: {result.stderr}", "ERROR")
        return False
    return True

@handle_exception
def check_requirements(root_dir):
    """检查 requirements.txt 并安装"""
    req_file = os.path.join(root_dir, "requirements.txt")
    if os.path.exists(req_file):
        log_message("Found requirements.txt, installing Python dependencies...", "INFO")
        return run_command(f"pip install -r {req_file}", cwd=root_dir)
    return True

@handle_exception
def check_package_json(root_dir):
    """检查 package.json 并安装"""
    pkg_file = os.path.join(root_dir, "package.json")
    if os.path.exists(pkg_file):
        log_message("Found package.json, installing Node.js dependencies...", "INFO")
        return run_command("npm install", cwd=root_dir)
    return True

@handle_exception
def install_dependencies(root_dir):
    """安装所有依赖"""
    success = True
    if not check_requirements(root_dir):
        success = False
    if not check_package_json(root_dir):
        success = False
    
    # 还可以解析 ENVIRONMENT.md，但目前先只支持标准文件
    
    return success

"""
会话启动检查脚本（轻量级）
只读取摘要文件，最小化 token 消耗
"""
import subprocess
from datetime import datetime
from pathlib import Path


def read_file_content(file_path: Path) -> str:
    """读取文件内容"""
    if not file_path.exists():
        return f"[文件不存在] {file_path}"
    try:
        return file_path.read_text(encoding="utf-8")
    except Exception as e:
        return f"[读取失败] {e}"


def get_git_status(root_dir: Path) -> str:
    """获取 git 状态"""
    try:
        result = subprocess.run(
            ["git", "status", "--short"],
            cwd=root_dir,
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        return result.stdout.strip() if result.stdout.strip() else "工作区干净"
    except Exception:
        return "[Git 状态获取失败]"


def get_git_log(root_dir: Path, count: int = 3) -> str:
    """获取最近的 git 提交记录"""
    try:
        result = subprocess.run(
            ["git", "log", f"-{count}", "--oneline"],
            cwd=root_dir,
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        return result.stdout.strip() if result.stdout.strip() else "无提交记录"
    except Exception:
        return "[Git 日志获取失败]"


def run_startup_check(root_dir: Path = None) -> dict:
    """执行启动检查（轻量级）"""
    if root_dir is None:
        root_dir = Path(__file__).parent.parent.parent.parent.parent
    
    root_dir = Path(root_dir)
    memory_dir = root_dir / ".trae" / "memory"
    
    results = {
        "timestamp": datetime.now().strftime("[%Y-%m-%d %H:%M:%S]"),
        "summary": None,
        "git_status": None,
        "git_log": None,
    }
    
    results["summary"] = read_file_content(memory_dir / "SUMMARY.md")
    results["git_status"] = get_git_status(root_dir)
    results["git_log"] = get_git_log(root_dir)
    
    return results


def format_report(results: dict) -> str:
    """格式化报告（简洁版）"""
    lines = [
        f"**检查时间**: {results['timestamp']}",
        "",
        "### Git 状态",
        f"```",
        results["git_status"],
        "```",
        "",
        "### 最近提交",
        f"```",
        results["git_log"],
        "```",
    ]
    return "\n".join(lines)


if __name__ == "__main__":
    import sys
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else None
    results = run_startup_check(root)
    print(format_report(results))

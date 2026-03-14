"""
记忆生命周期管理脚本
实现记忆的衰减、压缩、归档机制
"""
import re
import shutil
from datetime import datetime, timedelta
from pathlib import Path


def parse_session_date(filename: str) -> datetime | None:
    """从文件名解析日期"""
    match = re.search(r"(\d{4}-\d{2}-\d{2})", filename)
    if match:
        return datetime.strptime(match.group(1), "%Y-%m-%d")
    return None


def categorize_sessions(sessions_dir: Path) -> dict:
    """将会话文件分类为热/温/冷"""
    now = datetime.now()
    hot_threshold = now - timedelta(days=7)
    warm_threshold = now - timedelta(days=30)
    
    categories = {
        "hot": [],      # 0-7天：完整保留
        "warm": [],     # 7-30天：压缩摘要
        "cold": [],     # 30天+：归档
    }
    
    for session_file in sessions_dir.glob("*.md"):
        if session_file.name == "SUMMARY.md":
            continue
        
        session_date = parse_session_date(session_file.name)
        if not session_date:
            continue
        
        if session_date >= hot_threshold:
            categories["hot"].append(session_file)
        elif session_date >= warm_threshold:
            categories["warm"].append(session_file)
        else:
            categories["cold"].append(session_file)
    
    return categories


def compress_session(session_file: Path) -> str:
    """压缩会话记忆为摘要"""
    content = session_file.read_text(encoding="utf-8")
    
    date_match = re.search(r"\[(\d{4}-\d{2}-\d{2})", content)
    date_str = date_match.group(1) if date_match else session_file.stem
    
    activities = []
    if "## 关键活动" in content:
        section = content.split("## 关键活动")[1].split("##")[0]
        for line in section.split("\n")[:3]:
            if line.strip().startswith("- **"):
                activities.append(line.strip())
    
    decisions = []
    if "## 重要决策" in content:
        section = content.split("## 重要决策")[1].split("##")[0]
        for line in section.split("\n")[:2]:
            if line.strip().startswith("- **"):
                decisions.append(line.strip())
    
    compressed = f"""# [{date_str}] 会话摘要

## 关键活动
{chr(10).join(activities) if activities else "- 无记录"}

## 重要决策
{chr(10).join(decisions) if decisions else "- 无记录"}

---
*压缩时间: {datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")}*
"""
    return compressed


def archive_session(session_file: Path, archive_dir: Path):
    """归档会话到冷存储"""
    session_date = parse_session_date(session_file.name)
    if not session_date:
        return
    
    year_month = session_date.strftime("%Y-%m")
    archive_subdir = archive_dir / year_month
    archive_subdir.mkdir(parents=True, exist_ok=True)
    
    compressed = compress_session(session_file)
    archive_file = archive_subdir / session_file.name
    
    archive_file.write_text(compressed, encoding="utf-8")
    session_file.unlink()
    
    return archive_file


def manage_memory_lifecycle(memory_dir: Path, dry_run: bool = False) -> dict:
    """执行记忆生命周期管理"""
    sessions_dir = memory_dir / "sessions"
    archive_dir = memory_dir / "archive"
    
    if not sessions_dir.exists():
        return {"error": "sessions 目录不存在"}
    
    archive_dir.mkdir(parents=True, exist_ok=True)
    
    categories = categorize_sessions(sessions_dir)
    
    results = {
        "hot": len(categories["hot"]),
        "warm_compressed": 0,
        "cold_archived": 0,
        "actions": [],
    }
    
    for session_file in categories["warm"]:
        compressed = compress_session(session_file)
        if not dry_run:
            session_file.write_text(compressed, encoding="utf-8")
        results["warm_compressed"] += 1
        results["actions"].append(f"压缩: {session_file.name}")
    
    for session_file in categories["cold"]:
        if not dry_run:
            archive_session(session_file, archive_dir)
        results["cold_archived"] += 1
        results["actions"].append(f"归档: {session_file.name}")
    
    return results


def print_report(results: dict):
    """打印管理报告"""
    print("=" * 50)
    print("📊 记忆生命周期管理报告")
    print("=" * 50)
    print(f"热记忆 (0-7天): {results['hot']} 条 - 完整保留")
    print(f"温记忆 (7-30天): {results['warm_compressed']} 条 - 已压缩")
    print(f"冷记忆 (30天+): {results['cold_archived']} 条 - 已归档")
    print("-" * 50)
    for action in results["actions"]:
        print(f"  • {action}")


if __name__ == "__main__":
    import sys
    
    root = Path(sys.argv[1]) if len(sys.argv) > 1 and not sys.argv[1].startswith("--") else Path(__file__).parent.parent.parent.parent.parent
    memory_dir = root / ".trae" / "memory"
    
    dry_run = "--dry-run" in sys.argv
    
    results = manage_memory_lifecycle(memory_dir, dry_run)
    
    if "error" in results:
        print(f"错误: {results['error']}")
    else:
        print_report(results)

"""
记忆摘要更新脚本
自动从会话记忆压缩生成摘要
"""
import re
from datetime import datetime
from pathlib import Path


def extract_section(content: str, section_name: str) -> str:
    """提取指定章节内容"""
    pattern = rf"## {section_name}\n(.*?)(?=\n## |\Z)"
    match = re.search(pattern, content, re.DOTALL)
    return match.group(1).strip() if match else ""


def extract_list_items(content: str) -> list[str]:
    """提取列表项"""
    items = []
    for line in content.split("\n"):
        line = line.strip()
        if line.startswith("- ") or line.startswith("- ["):
            items.append(line)
    return items


def compress_session(session_file: Path) -> dict:
    """压缩单个会话文件"""
    content = session_file.read_text(encoding="utf-8")
    
    date_match = re.search(r"\[(\d{4}-\d{2}-\d{2})", content)
    date_str = date_match.group(1) if date_match else session_file.stem
    
    activities = extract_section(content, "关键活动")
    activity_items = extract_list_items(activities)[:3]
    
    decisions = extract_section(content, "重要决策")
    decision_items = extract_list_items(decisions)[:2]
    
    todos = extract_section(content, "待办/遗留")
    todo_items = [item for item in extract_list_items(todos) if "[ ]" in item][:3]
    
    return {
        "date": date_str,
        "activities": activity_items,
        "decisions": decision_items,
        "todos": todo_items,
    }


def update_summary(memory_dir: Path):
    """更新摘要文件"""
    sessions_dir = memory_dir / "sessions"
    summary_file = memory_dir / "SUMMARY.md"
    
    session_files = sorted(sessions_dir.glob("*.md"), reverse=True)[:3]
    
    all_activities = []
    all_todos = []
    all_decisions = []
    
    for sf in session_files:
        compressed = compress_session(sf)
        all_activities.append(f"**[{compressed['date']}]** " + 
                             ", ".join([a.lstrip("- ").split("：")[0] for a in compressed['activities'][:2]]))
        all_todos.extend(compressed['todos'])
        all_decisions.extend(compressed['decisions'])
    
    user_profile = memory_dir / "user-profile.md"
    user_prefs = []
    if user_profile.exists():
        content = user_profile.read_text(encoding="utf-8")
        prefs = extract_section(content, "沟通偏好")
        user_prefs = extract_list_items(prefs)[:3]
    
    capabilities_file = memory_dir / "capabilities" / "index.md"
    cap_has = []
    cap_enhance = []
    if capabilities_file.exists():
        content = capabilities_file.read_text(encoding="utf-8")
        has_section = extract_section(content, "已具备能力")
        cap_has = [item.split("|")[1].strip() for item in has_section.split("\n") 
                   if "|" in item and not item.startswith("| :")][:4]
        enhance_section = extract_section(content, "待增强能力")
        cap_enhance = [item.split("|")[1].strip() for item in enhance_section.split("\n")
                       if "|" in item and not item.startswith("| :")][:2]
    
    summary_content = f"""# 记忆摘要

> **启动时只读此文件**，详情按需读取

## 最近活动 (Last 3)
{chr(10).join(f"- {a}" for a in all_activities)}

## 待办事项
{chr(10).join(all_todos[:5]) if all_todos else "- [ ] 暂无待办"}

## 关键决策
{chr(10).join(all_decisions[:3]) if all_decisions else "- 暂无记录"}

## 用户偏好
{chr(10).join(user_prefs) if user_prefs else "- 语言：中文"}

## 能力状态
- 已具备：{', '.join(cap_has) if cap_has else '基础能力'}
- 待增强：{', '.join(cap_enhance) if cap_enhance else '暂无'}

## 索引
| 类型 | 路径 | 说明 |
|:---|:---|:---|
| 会话详情 | `sessions/YYYY-MM-DD.md` | 按需读取 |
| 能力清单 | `capabilities/index.md` | 按需读取 |
| 决策日志 | `decisions/index.md` | 按需读取 |
| 用户画像 | `user-profile.md` | 按需读取 |

---
*更新时间: {datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")}*
"""
    
    summary_file.write_text(summary_content, encoding="utf-8")
    print(f"[OK] 摘要已更新: {summary_file}")


if __name__ == "__main__":
    import sys
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).parent.parent.parent.parent.parent
    memory_dir = root / ".trae" / "memory"
    update_summary(memory_dir)

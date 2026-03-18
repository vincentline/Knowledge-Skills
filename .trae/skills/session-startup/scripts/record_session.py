"""
会话启动记录脚本
在会话开始时自动添加时间戳到会话记录
"""
from datetime import datetime
from pathlib import Path


def get_memory_dir():
    return Path(__file__).parent.parent.parent.parent / "memory"


def record_session_start(activity: str = None):
    """记录会话启动时间"""
    memory_dir = get_memory_dir()
    sessions_dir = memory_dir / "sessions"
    
    today = datetime.now().strftime("%Y-%m-%d")
    current_time = datetime.now().strftime("%H:%M")
    
    session_file = sessions_dir / f"{today}.md"
    
    if not session_file.exists():
        content = f"""# [{today}] 会话记录

## 会话启动记录
> 每个会话启动时追加一条记录

"""
        session_file.write_text(content, encoding="utf-8")
    
    content = session_file.read_text(encoding="utf-8")
    
    time_str = f"**[{current_time}]**"
    if activity:
        line = f"- {time_str} 会话启动 - {activity}\n"
    else:
        line = f"- {time_str} 会话启动\n"
    
    marker = "## 会话启动记录"
    if marker in content:
        parts = content.split(marker)
        insert_pos = parts[0] + marker + "\n"
        
        line_to_find = "- **[时间]**"
        if line_to_find in parts[1]:
            parts[1] = parts[1].replace(line_to_find, line.strip())
            content = marker.join(parts)
        else:
            content = insert_pos + line + parts[1]
    else:
        content = f"{marker}\n{line}\n" + content
    
    session_file.write_text(content, encoding="utf-8")
    print(f"会话启动时间已记录: {current_time}")
    return current_time


if __name__ == "__main__":
    import sys
    activity = sys.argv[1] if len(sys.argv) > 1 else None
    record_session_start(activity)

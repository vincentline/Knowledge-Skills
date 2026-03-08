import os
import sys
import traceback
import datetime
from functools import wraps

# 定义颜色
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# 日志路径 (相对于项目根目录)
LOG_FILE = os.path.join(".trae", "logs", "error-log.md")

def log_message(message, level="INFO"):
    """打印日志并记录到文件（如果是错误）"""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 控制台输出
    color = Colors.OKBLUE
    if level == "WARNING":
        color = Colors.WARNING
    elif level == "ERROR":
        color = Colors.FAIL
    elif level == "SUCCESS":
        color = Colors.OKGREEN
        
    print(f"{color}[{timestamp}] [{level}] {message}{Colors.ENDC}")
    
    # 写入文件 (仅错误)
    if level == "ERROR":
        try:
            # 确保父目录存在
            log_dir = os.path.dirname(LOG_FILE)
            if os.path.exists(log_dir) and os.path.exists(LOG_FILE):
                with open(LOG_FILE, "a", encoding="utf-8") as f:
                    f.write(f"\n## [{timestamp}] Error\n")
                    f.write(f"- Message: {message}\n")
                    # 只有在有 traceback 的时候才记录
                    if sys.exc_info()[0] is not None:
                        f.write(f"```\n{traceback.format_exc()}\n```\n")
        except Exception:
            pass # 避免递归错误

def handle_exception(func):
    """装饰器：捕获异常并记录"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            log_message(f"Execution failed in {func.__name__}: {str(e)}", "ERROR")
            # 返回 False 表示失败 (如果函数预期返回布尔值)
            return False
    return wrapper

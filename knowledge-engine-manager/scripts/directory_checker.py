import os
import shutil
from error_handler import handle_exception, log_message

# 基础目录结构
BASE_DIRS = [
    ".trae/logs",
    ".trae/temp",
    ".trae/trash",
    ".trae/rules/core",
    ".trae/rules/inbox",
    ".trae/rules/logs",
    ".trae/rules/modules"
]

# 模板映射: (模板路径, 目标路径)
# 模板路径相对于 knowledge-engine-manager/templates
# 目标路径相对于项目根目录
TEMPLATE_MAPPING = {
    "UPDATE_LOG.md": ".trae/logs/UPDATE_LOG.md",
    "coding-style.ts.md": ".trae/rules/core/coding-style.ts.md",
    "workflows.ts.md": ".trae/rules/core/workflows.ts.md",
    "index.md": [".trae/rules/index.md", ".trae/rules/inbox/index.md"],
    "decision-log.md": ".trae/rules/logs/decision-log.md",
    "error-log.md": ".trae/rules/logs/error-log.md"
}

@handle_exception
def check_and_create_dirs(root_dir):
    """检查并创建基础目录"""
    log_message(f"Checking directory structure in {root_dir}...")
    for rel_path in BASE_DIRS:
        full_path = os.path.join(root_dir, rel_path)
        if not os.path.exists(full_path):
            os.makedirs(full_path, exist_ok=True)
            log_message(f"Created directory: {rel_path}", "SUCCESS")
    return True

@handle_exception
def deploy_templates(root_dir, skill_root):
    """
    部署模板文件
    skill_root: knowledge-engine-manager 的根目录
    """
    templates_dir = os.path.join(skill_root, "templates")
    
    for template_name, target_rel_paths in TEMPLATE_MAPPING.items():
        if isinstance(target_rel_paths, str):
            target_rel_paths = [target_rel_paths]
            
        src_path = os.path.join(templates_dir, template_name)
        if not os.path.exists(src_path):
            log_message(f"Template not found: {src_path}", "WARNING")
            continue
            
        for rel_path in target_rel_paths:
            target_path = os.path.join(root_dir, rel_path)
            
            # 策略：
            # 仅当不存在时创建。避免覆盖用户数据。
            if not os.path.exists(target_path):
                # 确保父目录存在
                os.makedirs(os.path.dirname(target_path), exist_ok=True)
                shutil.copy2(src_path, target_path)
                log_message(f"Deployed template: {rel_path}", "SUCCESS")
                
    return True

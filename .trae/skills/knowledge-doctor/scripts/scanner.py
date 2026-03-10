#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Knowledge Doctor Scanner - 知识体检仪
=====================================

功能:
    扫描 .trae/rules/modules 下的规则文件，生成健康诊断报告。
    支持增量扫描 (Git Diff) 和全量扫描。

检查项:
    1. Format: 是否包含 Frontmatter 和 TS Interface。
    2. Size: 行数是否超过 300。
    3. Tags: 是否包含 TODO, FIXME, ? 等标记。

输出:
    JSON 格式的诊断报告。

拆分文件命名策略:
    原文件: 123.ts.md
    拆分后:
    - 123-main-feature.ts.md
    - 123-sub-feature-a.ts.md
    - 123-sub-feature-b.ts.md
    - index.ts.md
"""

import os
import sys
import argparse
import json
import subprocess
import re

# ============================================================================
# 工具函数
# ============================================================================

def find_project_root():
    """
    查找项目根目录（包含 .trae 目录的目录）
    
    Returns:
        str: 项目根目录的绝对路径，如果未找到则返回 None
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    while current_dir != os.path.dirname(current_dir):  # 到达文件系统根目录时停止
        if os.path.exists(os.path.join(current_dir, '.trae')):
            return current_dir
        current_dir = os.path.dirname(current_dir)
    return None

# ============================================================================
# 配置常量
# ============================================================================

# 项目根目录
PROJECT_ROOT = find_project_root()
if not PROJECT_ROOT:
    print("❌ 错误：未找到项目根目录（.trae 目录）")
    exit(1)

# 规则目录路径
RULES_DIR = os.path.join(PROJECT_ROOT, ".trae", "rules", "modules")

# 技能目录路径
SKILLS_DIR = os.path.join(PROJECT_ROOT, ".trae", "skills")

def get_git_changed_files():
    """获取 Git 暂存区和最近一次提交的变更文件列表"""
    changed_files = set()
    try:
        # 1. 未提交的变更 (包括暂存和未暂存)
        # git status --porcelain
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        for line in result.stdout.splitlines():
            # 提取路径 (M path/to/file)
            parts = line.strip().split()
            if len(parts) >= 2:
                path = parts[-1]
                changed_files.add(path)

        # 2. 最近一次提交的变更
        # git diff-tree --no-commit-id --name-only -r HEAD
        result = subprocess.run(
            ["git", "diff-tree", "--no-commit-id", "--name-only", "-r", "HEAD"],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        for line in result.stdout.splitlines():
            changed_files.add(line.strip())

    except Exception as e:
        print(f"⚠️ Git command failed: {e}. Falling back to full scan.", file=sys.stderr)
        return None # 返回 None 表示获取失败，应转为全量

    # 过滤出 .trae/rules/modules 和 .trae/skills 下的文件
    filtered = []
    for f in changed_files:
        # 统一路径分隔符
        f = f.replace("/", os.sep)
        is_module = RULES_DIR.replace("/", os.sep) in f and (f.endswith(".ts.md") or f.endswith(".md"))
        is_skill = SKILLS_DIR.replace("/", os.sep) in f and f.endswith(".md")
        
        if (is_module or is_skill) and os.path.exists(f):
            filtered.append(f)
    
    return filtered

def check_naming_convention(file_path):
    """检查文件命名是否符合拆分文件命名规则
    
    规则：拆分文件（除index外）必须包含原大文件的文件名作为前缀
    格式：{原文件名}-{后缀}{扩展名}
    示例：原文件 123.ts.md，拆分后 123-main-feature.ts.md
    """
    issues = []
    
    # 跳过 index 文件
    if file_path.endswith("index.ts.md") or file_path.endswith("index.md"):
        return issues
    
    dir_path = os.path.dirname(file_path)
    basename = os.path.basename(file_path)
    
    # 处理 .ts.md 复合扩展名
    if basename.endswith('.ts.md'):
        name = basename[:-6]  # 移除 .ts.md
        ext = '.ts.md'
    else:
        name, ext = os.path.splitext(basename)
    
    # 检查是否包含连字符（表示可能是拆分文件）
    if '-' in name:
        # 提取前缀部分
        parts = name.split('-')
        prefix = parts[0]
        suffix = '-'.join(parts[1:])
        
        # 检查命名格式是否规范
        if not suffix:
            issues.append({
                "type": "warning",
                "code": "naming_convention",
                "msg": f"File name '{basename}' has empty suffix after hyphen."
            })
        
        # 检查同目录下是否存在对应的原文件
        original_file = os.path.join(dir_path, f"{prefix}{ext}")
        original_exists = False
        
        # 检查原文件是否存在
        if os.path.exists(original_file):
            original_exists = True
        # 检查对应的 .ts.md 文件
        elif ext == '.md':
            original_ts_file = os.path.join(dir_path, f"{prefix}.ts.md")
            if os.path.exists(original_ts_file):
                original_exists = True
        
        if not original_exists:
            # 检查文件内容是否完整，判断是否为独立文件
            if is_independent_file(file_path):
                # 独立文件，不触发警告
                pass
            else:
                issues.append({
                    "type": "warning",
                    "code": "naming_convention",
                    "msg": f"File name '{basename}' appears to be a split file but no corresponding original file found."
                })
    
    return issues

def is_independent_file(file_path):
    """判断文件是否为独立文件（包含完整的 Frontmatter 和 TypeScript Interface）
    
    独立文件特征：
    1. 包含 Frontmatter（以 --- 开始）
    2. 包含 TypeScript Interface 定义
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查是否包含 Frontmatter
        has_frontmatter = content.startswith("---")
        
        # 检查是否包含 TypeScript Interface 定义
        has_interface = "export interface" in content
        
        return has_frontmatter and has_interface
    except Exception:
        return False

def scan_file(file_path):
    """扫描单个文件，返回问题列表"""
    issues = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            content = "".join(lines)
    except Exception as e:
        return [{"type": "error", "msg": f"Read failed: {e}"}]

    # 1. 大小检查 (Size Check)
    if len(lines) > 300:
        issues.append({
            "type": "warning", 
            "code": "oversized", 
            "msg": f"File has {len(lines)} lines (>300). Consider splitting."
        })

    # 2. 格式检查 (Format Check)
    # 检查 Frontmatter (--- ... ---)
    if not content.startswith("---"):
        issues.append({
            "type": "critical", 
            "code": "format_error", 
            "msg": "Missing Frontmatter."
        })
    
    # 检查 TS Interface (export interface ...)
    # 特殊情况：skills 目录下的 SKILL.md 可能不需要严格的 TS Interface，
    # 但拥有它是好的实践。让我们强制执行它以促进标准化。
    is_skill = SKILLS_DIR.replace("/", os.sep) in file_path
    if not is_skill and "export interface" not in content:
        issues.append({
            "type": "critical", 
            "code": "format_error", 
            "msg": "Missing TypeScript Interface definition."
        })

    # 3. 标记检查 (Tags Check)
    todo_pattern = re.compile(r'\b(TODO|FIXME|\?{2,})\b')
    for i, line in enumerate(lines):
        if todo_pattern.search(line):
            issues.append({
                "type": "info",
                "code": "fact_check",
                "msg": f"Found marker on line {i+1}: {line.strip()}"
            })
    
    # 4. 索引检查 (Index Check)
    # 如果是 index.ts.md，检查是否包含 export interface ModuleIndex
    if file_path.endswith("index.ts.md"):
        # 简单检查 content 中是否包含 interface *Index
        if not re.search(r'export interface \w+Index', content):
             issues.append({
                "type": "critical", 
                "code": "index_error", 
                "msg": "Index file missing 'export interface XxxIndex'."
            })
    
    # 5. 命名规则检查 (Naming Convention Check)
    naming_issues = check_naming_convention(file_path)
    issues.extend(naming_issues)

    return issues

def main():
    parser = argparse.ArgumentParser(description="Knowledge Doctor Scanner")
    parser.add_argument("--target", help="Target directory to scan (default: auto)")
    parser.add_argument("--full", action="store_true", help="Force full scan (ignore git status)")
    
    args = parser.parse_args()

    # 确定扫描目标
    scan_dirs = []
    if args.target:
        scan_dirs.append(args.target)
    else:
        scan_dirs.append(RULES_DIR)
        scan_dirs.append(SKILLS_DIR)
    
    files_to_scan = []

    # 确定扫描范围
    if args.full:
        for target_dir in scan_dirs:
            print(f"🔍 Starting FULL scan on {target_dir}...", file=sys.stderr)
            if os.path.exists(target_dir):
                for root, _, files in os.walk(target_dir):
                    for file in files:
                        if file.endswith(".ts.md") or (file.endswith(".md") and "inbox" not in root):
                            files_to_scan.append(os.path.join(root, file))
    else:
        print(f"🔍 Starting INCREMENTAL scan...", file=sys.stderr)
        git_files = get_git_changed_files()
        if git_files is None:
            # Git 失败，回退全量
            for target_dir in scan_dirs:
                if os.path.exists(target_dir):
                    for root, _, files in os.walk(target_dir):
                        for file in files:
                            if file.endswith(".ts.md") or (file.endswith(".md") and "inbox" not in root):
                                files_to_scan.append(os.path.join(root, file))
        else:
            files_to_scan = git_files

    if not files_to_scan:
        print(json.dumps({"status": "clean", "msg": "No files to scan."}))
        return

    # 执行扫描
    report = {"critical": [], "warning": [], "info": []}
    
    for file_path in files_to_scan:
        file_issues = scan_file(file_path)
        for issue in file_issues:
            entry = {
                "file": file_path,
                "issue": issue["code"],
                "msg": issue["msg"]
            }
            if issue["type"] == "critical":
                report["critical"].append(entry)
            elif issue["type"] == "warning":
                report["warning"].append(entry)
            else:
                report["info"].append(entry)

    # 输出 JSON 报告
    print(json.dumps(report, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()

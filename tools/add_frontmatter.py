"""
add_frontmatter.py — 给旧 10 分域 475 个 .md 批量加 frontmatter
不动原有内容,只在头部插入 frontmatter block
每个文件处理前先备份到 tmp/_frontmatter_backup/
"""
import os
import re
import shutil
from pathlib import Path
from datetime import datetime

ROOT = Path(r"D:\Docs\Books\my second brain")
PREFIXES = [
    "第二大脑-10-SaaS", "第二大脑-20-后端", "第二大脑-30-地缘",
    "第二大脑-40-认知", "第二大脑-50-内容", "第二大脑-60-面试",
    "第二大脑-70-物理", "第二大脑-80-方法论", "第二大脑-90-收件箱",
    "第二大脑-95-原始资料"
]

# Karpathy 6 类页面 → type 字段映射
TYPE_MAP = {
    "03-知识": "concept",       # 学科/领域概念
    "03-领域知识": "concept",
    "02-总览": "synthesis",      # 综合页
    "02-项目总览": "synthesis",
    "05-任务": "question",       # 任务
    "05-任务管理": "question",
    "06-报告": "evidence",       # 报告/证据
    "06-报告证据": "evidence",
    "01-状态": "state",          # 状态
    "04-流程": "process",        # 流程
    "04-运行流程": "process",
    "00-规范": "spec",           # 规范
    "08-模板": "template",       # 模板
}

def detect_type(rel_path: str) -> str:
    for key, t in TYPE_MAP.items():
        if key in rel_path:
            return t
    fname = Path(rel_path).name
    if fname in ("AGENTS.md", "README.md", "日志.md", "索引.md"):
        return "meta"
    return "concept"  # 默认

def extract_title(text: str, filename: str) -> str:
    """从 H1 或文件名提取标题"""
    m = re.search(r"^#\s+(.+)$", text, re.M)
    if m:
        title = m.group(1).strip()
        # 去除 .md 后缀
        if title.endswith(".md"):
            title = title[:-3]
        return title
    return filename.replace(".md", "")

def make_id(prefix: str, subdir: str, filename: str) -> str:
    """kb-<分域>-<子目录>-<文件名>"""
    domain_short = {
        "第二大脑-10-SaaS": "saas",
        "第二大脑-20-后端": "backend",
        "第二大脑-30-地缘": "geo",
        "第二大脑-40-认知": "cog",
        "第二大脑-50-内容": "content",
        "第二大脑-60-面试": "interview",
        "第二大脑-70-物理": "physics",
        "第二大脑-80-方法论": "method",
        "第二大脑-90-收件箱": "inbox",
        "第二大脑-95-原始资料": "raw",
    }.get(prefix, "x")
    sub = subdir if subdir not in (".", "") else "root"
    return f"kb-{domain_short}-{sub}-{filename[:-3]}"

def has_frontmatter(text: str) -> bool:
    return bool(re.match(r"---\s*\n.*?\n---", text, re.S))

def build_fm(file_id: str, ftype: str, title: str, source_id: str = "") -> str:
    today = datetime.now().strftime("%Y-%m-%d")
    # YAML 字符串需要引号包裹
    title_escaped = title.replace("'", "''")
    return f"""---
id: {file_id}
type: {ftype}
title: '{title_escaped}'
original_title: '{title_escaped}'
aliases: []
status: active
source_id: '{source_id}'
created: {today}
updated: {today}
---

"""

def process_file(filepath: Path, prefix: str, backup_dir: Path) -> tuple[bool, str]:
    """处理一个文件,返回 (changed, new_text)"""
    text = filepath.read_text(encoding="utf-8", errors="ignore")
    if has_frontmatter(text):
        return False, text  # 已有,跳过

    rel = filepath.relative_to(ROOT)
    parts = rel.parts
    subdir = parts[1] if len(parts) > 2 else "root"
    fname = filepath.name
    title = extract_title(text, fname)
    ftype = detect_type(str(rel))
    file_id = make_id(prefix, subdir, fname)

    # source_id 暂时留空(没有真正的来源链接),日后人工补
    new_text = build_fm(file_id, ftype, title) + text

    # 备份
    backup_path = backup_dir / rel
    backup_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(filepath, backup_path)

    # 写入
    filepath.write_text(new_text, encoding="utf-8")
    return True, new_text

def main():
    backup_dir = ROOT / "tmp" / "_frontmatter_backup"
    backup_dir.mkdir(parents=True, exist_ok=True)

    total = 0
    changed = 0
    skipped = 0
    errors = []

    for prefix in PREFIXES:
        d = ROOT / prefix
        if not d.exists():
            continue
        for md in d.rglob("*.md"):
            total += 1
            try:
                ok, _ = process_file(md, prefix, backup_dir)
                if ok:
                    changed += 1
                else:
                    skipped += 1
            except Exception as e:
                errors.append((str(md.relative_to(ROOT)), str(e)))

    print(f"=== Frontmatter 批量补充完成 ===")
    print(f"总文件: {total}")
    print(f"已加 frontmatter: {changed}")
    print(f"已有跳过: {skipped}")
    print(f"错误: {len(errors)}")
    if errors:
        for p, e in errors[:5]:
            print(f"  {p}: {e}")
    print(f"\n备份目录: {backup_dir}")
    print(f"备份文件数: {len(list(backup_dir.rglob('*.md')))}")

if __name__ == "__main__":
    main()

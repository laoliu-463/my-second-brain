#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
跨实例硬约束校验

从 vault 根运行，扫描所有 "第二大脑*/" 实例 + 第二大脑/ 总索引层
对每个实例独立校验 50/200 硬约束

用法：
  python 第二大脑/07-脚本/line_guard.py
  python 第二大脑/07-脚本/line_guard.py --root /path/to/vault
"""

import argparse
import sys
from pathlib import Path

DEFAULT_ROOT = Path(__file__).resolve().parents[2]  # vault 根
MAX_FILES = 50
MAX_DIRS = 10
MAX_FILES_PER_DIR = 10
MAX_LINES = 200
SCRIPT_EXTS = {".py", ".sh", ".ps1", ".bat", ".cmd"}
# 哪些顶层路径算"第二大脑实例"——只要以"第二大脑"开头
INSTANCE_PREFIX = "第二大脑"


def find_instances(root: Path):
    """找所有以 '第二大脑' 开头的顶层目录"""
    instances = []
    for p in sorted(root.iterdir()):
        if p.is_dir() and (p.name == INSTANCE_PREFIX or p.name.startswith(INSTANCE_PREFIX + "-")):
            instances.append(p)
    return instances


def check_instance(instance: Path, root: Path) -> list:
    """检查单个实例的硬约束"""
    bad = []

    # 一级子目录数
    top_dirs = [p for p in sorted(instance.iterdir()) if p.is_dir()]
    if len(top_dirs) > MAX_DIRS:
        bad.append(f"  TOO_MANY_TOP_DIRS: {len(top_dirs)} > {MAX_DIRS}")

    # 全量文件（区分 md 和脚本）
    all_files = [p for p in instance.rglob("*") if p.is_file()]
    md_files = [p for p in all_files if p.suffix.lower() not in SCRIPT_EXTS]
    n_md = len(md_files)
    n_script = len(all_files) - n_md
    if n_md > MAX_FILES:
        bad.append(f"  TOO_MANY_MD_FILES: {n_md} > {MAX_FILES}")

    max_lines = 0
    for f in all_files:
        if f.suffix.lower() in SCRIPT_EXTS:
            continue
        try:
            text = f.read_text(encoding="utf-8", errors="ignore")
            lines = text.count("\n") + (1 if text and not text.endswith("\n") else 0)
        except Exception:
            continue
        if lines > MAX_LINES:
            rel = f.relative_to(instance)
            bad.append(f"  TOO_MANY_LINES: {rel} = {lines} > {MAX_LINES}")
        if lines > max_lines:
            max_lines = lines

    # 每目录文件数
    for d in instance.rglob("*"):
        if d.is_dir():
            n_files = sum(1 for p in d.iterdir() if p.is_file() and p.suffix.lower() not in SCRIPT_EXTS)
            if n_files > MAX_FILES_PER_DIR:
                rel = d.relative_to(instance)
                bad.append(f"  TOO_MANY_FILES_IN_DIR: {rel}/ = {n_files} > {MAX_FILES_PER_DIR}")

    return bad, n_md, n_script, len(top_dirs), max_lines


def main():
    parser = argparse.ArgumentParser(description="跨实例硬约束校验")
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT, help="vault 根目录")
    args = parser.parse_args()

    root: Path = args.root
    if not root.exists():
        print(f"FAIL: vault 根不存在: {root}")
        sys.exit(1)

    instances = find_instances(root)
    if not instances:
        print("FAIL: 没找到任何第二大脑实例")
        sys.exit(1)

    print(f"=== 跨实例硬约束校验 ===")
    print(f"vault 根: {root}")
    print(f"实例数: {len(instances)}")
    print()

    fail = False
    for inst in instances:
        rel = inst.relative_to(root)
        bad, n_md, n_script, n_dirs, max_lines = check_instance(inst, root)
        status = "PASS" if not bad else "FAIL"
        print(f"[{status}] {rel}/  md={n_md}/{MAX_FILES} script={n_script} dirs={n_dirs}/{MAX_DIRS} max_lines={max_lines}/{MAX_LINES}")
        for b in bad:
            print(b)
        if bad:
            fail = True

    print()
    if fail:
        print("OVERALL: FAIL")
        sys.exit(1)
    else:
        print("OVERALL: PASS")
        sys.exit(0)


if __name__ == "__main__":
    main()

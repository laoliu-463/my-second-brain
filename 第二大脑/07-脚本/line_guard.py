#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
第二大脑/行数/文件数/目录数硬约束校验

硬约束：
  - 总文件数 ≤ 50
  - 单文件 ≤ 200 行
  - 一级子目录 ≤ 10
  - 每目录文件数 ≤ 10

用法：
  python 第二大脑/07-脚本/line_guard.py
  python 第二大脑/07-脚本/line_guard.py --root /path/to/第二大脑
"""

import argparse
import sys
from pathlib import Path

DEFAULT_ROOT = Path(__file__).resolve().parents[1]
MAX_FILES = 50
MAX_DIRS = 10
MAX_FILES_PER_DIR = 10
MAX_LINES = 200
SCRIPT_EXTS = {".py", ".sh", ".ps1", ".bat", ".cmd"}


def main():
    parser = argparse.ArgumentParser(description="第二大脑硬约束校验")
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT, help="第二大脑根目录")
    args = parser.parse_args()

    root: Path = args.root
    if not root.exists():
        print(f"FAIL: 根目录不存在: {root}")
        sys.exit(1)

    bad = []

    # 一级子目录数
    top_dirs = [p for p in sorted(root.iterdir()) if p.is_dir()]
    if len(top_dirs) > MAX_DIRS:
        bad.append(f"TOO_MANY_TOP_DIRS: {len(top_dirs)} > {MAX_DIRS}")
    print(f"[INFO] 一级子目录数: {len(top_dirs)} / {MAX_DIRS}")

    # 全量文件
    all_files = [p for p in root.rglob("*") if p.is_file()]
    print(f"[INFO] 总文件数: {len(all_files)} / {MAX_FILES}")

    if len(all_files) > MAX_FILES:
        bad.append(f"TOO_MANY_FILES: {len(all_files)} > {MAX_FILES}")

    # 每目录文件数
    for d in sorted(root.rglob("*")):
        if d.is_dir():
            n_files = sum(1 for p in d.iterdir() if p.is_file() and p.suffix.lower() not in SCRIPT_EXTS)
            if n_files > MAX_FILES_PER_DIR:
                rel = d.relative_to(root)
                bad.append(f"TOO_MANY_FILES_IN_DIR: {rel}/ = {n_files} > {MAX_FILES_PER_DIR}")

    # 单文件行数（非脚本）
    max_lines_seen = 0
    for f in all_files:
        if f.suffix.lower() in SCRIPT_EXTS:
            continue
        try:
            text = f.read_text(encoding="utf-8", errors="ignore")
            lines = text.count("\n") + (1 if text and not text.endswith("\n") else 0)
        except Exception:
            continue
        if lines > MAX_LINES:
            rel = f.relative_to(root)
            bad.append(f"TOO_MANY_LINES: {rel} = {lines} > {MAX_LINES}")
        if lines > max_lines_seen:
            max_lines_seen = lines

    print(f"[INFO] 最大单文件行数: {max_lines_seen} / {MAX_LINES}")

    if bad:
        print("\nFAIL:")
        for b in bad:
            print(f"  - {b}")
        sys.exit(1)
    else:
        print(f"\nPASS: files={len(all_files)}/{MAX_FILES}, dirs={len(top_dirs)}/{MAX_DIRS}, max_lines={max_lines_seen}/{MAX_LINES}")
        sys.exit(0)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
跨实例结构约束校验

从 vault 根运行，扫描所有 "第二大脑*/" 实例 + 第二大脑/ 总索引层
对每个实例独立校验目录结构约束

用法：
  python 第二大脑/07-脚本/line_guard.py
  python 第二大脑/07-脚本/line_guard.py --root /path/to/vault
"""

import argparse
import re
import sys
from pathlib import Path

DEFAULT_ROOT = Path(__file__).resolve().parents[2]  # vault 根
MAX_TOP_DIRS = 10
# 哪些顶层路径算"第二大脑实例"——只要以"第二大脑"开头
INSTANCE_PREFIX = "第二大脑"
TOP_DIR_PATTERN = re.compile(r"^\d{2}-.+")


def find_instances(root: Path):
    """找所有以 '第二大脑' 开头的顶层目录"""
    instances = []
    for p in sorted(root.iterdir()):
        if p.is_dir() and (p.name == INSTANCE_PREFIX or p.name.startswith(INSTANCE_PREFIX + "-")):
            instances.append(p)
    return instances


def check_instance(instance: Path) -> list:
    """检查单个实例的结构约束"""
    bad = []

    # 一级子目录数
    top_dirs = [p for p in sorted(instance.iterdir()) if p.is_dir()]
    if len(top_dirs) > MAX_TOP_DIRS:
        bad.append(f"  TOO_MANY_TOP_DIRS: {len(top_dirs)} > {MAX_TOP_DIRS}")

    for d in top_dirs:
        if not TOP_DIR_PATTERN.match(d.name):
            bad.append(f"  BAD_TOP_DIR_NAME: {d.name}")

    return bad, len(top_dirs)


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

    print(f"=== 跨实例结构约束校验 ===")
    print(f"vault 根: {root}")
    print(f"实例数: {len(instances)}")
    print()

    fail = False
    for inst in instances:
        rel = inst.relative_to(root)
        bad, n_dirs = check_instance(inst)
        status = "PASS" if not bad else "FAIL"
        print(f"[{status}] {rel}/  top_dirs={n_dirs}/{MAX_TOP_DIRS}")
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

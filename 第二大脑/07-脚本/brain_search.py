#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
跨实例关键词搜索

扫描所有 "第二大脑*/" 实例的 .md
支持中文 / 英文

用法：
  python 第二大脑/07-脚本/brain_search.py 订单归因
  python 第二大脑/07-脚本/brain_search.py "寄样" --root /path/to/vault
"""

import argparse
import sys
from pathlib import Path

DEFAULT_ROOT = Path(__file__).resolve().parents[2]  # vault 根
INSTANCE_PREFIX = "第二大脑"
INDEX_FILE = "索引.md"


def find_instances(root: Path):
    for p in sorted(root.iterdir()):
        if p.is_dir() and (p.name == INSTANCE_PREFIX or p.name.startswith(INSTANCE_PREFIX + "-")):
            yield p


def main():
    parser = argparse.ArgumentParser(description="跨实例关键词搜索")
    parser.add_argument("query", help="搜索关键词（支持中文）")
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT, help="vault 根目录")
    args = parser.parse_args()

    root: Path = args.root
    if not root.exists():
        print(f"FAIL: vault 根不存在: {root}")
        sys.exit(1)

    query = args.query.strip()
    if not query:
        print("FAIL: 关键词不能为空")
        sys.exit(1)

    matches = []
    for inst in find_instances(root):
        for f in inst.rglob("*.md"):
            rel_to_root = f.relative_to(root)
            rel = str(rel_to_root).replace("\\", "/")
            try:
                text = f.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                continue
            if query in text:
                summary = ""
                for line in text.splitlines():
                    if query in line:
                        summary = line.strip()[:80]
                        break
                if not summary:
                    summary = text[:80].replace("\n", " ").strip()
                # 标出实例
                instance_name = rel.split("/")[0]
                matches.append((instance_name, rel, summary))

    if not matches:
        print(f"NO_MATCH: '{query}'")
        print("提示：检查拼写、试不同关键词、确认资料是否已沉淀")
        sys.exit(0)

    # 按实例分组
    print(f"MATCH: '{query}' 共 {len(matches)} 处，分布 {len(set(m[0] for m in matches))} 个实例")
    print()
    last_inst = None
    for inst_name, rel, summary in matches:
        if inst_name != last_inst:
            print(f"--- {inst_name} ---")
            last_inst = inst_name
        print(f"  [[{rel}]]")
        print(f"    {summary}")
        print()


if __name__ == "__main__":
    main()

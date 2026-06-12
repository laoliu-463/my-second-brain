#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
第二大脑/本地关键词搜索

用法：
  python 第二大脑/07-脚本/brain_search.py 订单归因
  python 第二大脑/07-脚本/brain_search.py "寄样 自动完成" --root /path/to/第二大脑
"""

import argparse
import sys
from pathlib import Path

DEFAULT_ROOT = Path(__file__).resolve().parents[1]
INDEX_FILE = "索引.md"


def main():
    parser = argparse.ArgumentParser(description="第二大脑关键词搜索")
    parser.add_argument("query", help="搜索关键词（支持中文）")
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT, help="第二大脑根目录")
    args = parser.parse_args()

    root: Path = args.root
    if not root.exists():
        print(f"FAIL: 根目录不存在: {root}")
        sys.exit(1)

    query = args.query.strip()
    if not query:
        print("FAIL: 关键词不能为空")
        sys.exit(1)

    matches = []
    for f in root.rglob("*.md"):
        rel = str(f.relative_to(root)).replace("\\", "/")
        if rel == INDEX_FILE or rel == "README.md" or rel == "AGENTS.md" or rel == "日志.md":
            # 索引/入口也搜，但优先级低
            pass
        try:
            text = f.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        if query in text:
            # 提取第一个含 query 的行作为摘要
            summary = ""
            for line in text.splitlines():
                if query in line:
                    summary = line.strip()[:80]
                    break
            if not summary:
                summary = text[:80].replace("\n", " ").strip()
            matches.append((rel, summary))

    if not matches:
        print(f"NO_MATCH: '{query}'")
        print("提示：检查拼写、试不同关键词、确认资料是否已沉淀")
        sys.exit(0)

    print(f"MATCH: '{query}' 共 {len(matches)} 处")
    print()
    for rel, summary in matches:
        print(f"  [[{rel}]]")
        print(f"    {summary}")
        print()


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
第二大脑/索引覆盖校验

检查项：
  - 所有 .md 都在 索引.md 中被引用
  - 索引.md 引用都对应实际文件
  - 跨文件 [[wiki link]] 引用都有效

用法：
  python 第二大脑/07-脚本/brain_lint.py
  python 第二大脑/07-脚本/brain_lint.py --root /path/to/第二大脑
"""

import argparse
import re
import sys
from pathlib import Path

DEFAULT_ROOT = Path(__file__).resolve().parents[1]
INDEX_FILE = "索引.md"
SKIP_FILES = {INDEX_FILE, "日志.md", "README.md", "AGENTS.md"}


def main():
    parser = argparse.ArgumentParser(description="第二大脑索引 LINT")
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT, help="第二大脑根目录")
    args = parser.parse_args()

    root: Path = args.root
    if not root.exists():
        print(f"FAIL: 根目录不存在: {root}")
        sys.exit(1)

    index_path = root / INDEX_FILE
    if not index_path.exists():
        print(f"FAIL: {INDEX_FILE} 不存在")
        sys.exit(1)

    index_text = index_path.read_text(encoding="utf-8", errors="ignore")

    # 1. 所有 .md 必须在索引中被引用
    all_md = []
    for p in sorted(root.rglob("*.md")):
        rel = str(p.relative_to(root)).replace("\\", "/")
        all_md.append(rel)

    missing = []
    for rel in all_md:
        if rel in SKIP_FILES:
            continue
        # 索引中可能不带 .md 后缀
        if rel not in index_text and rel.replace(".md", "") not in index_text:
            missing.append(rel)

    # 2. 索引中引用必须对应实际文件
    # 提取 [[...]] 形式
    wiki_refs = re.findall(r"\[\[([^\]]+)\]\]", index_text)
    # 也提取 [[xxx|xxx]] 的左半部分
    broken = []
    for ref in wiki_refs:
        ref = ref.split("|")[0].strip()
        # 跳过 URL 和外部路径
        if "://" in ref or "/" in ref and (ref.startswith("http") or ref.startswith("/")):
            continue
        # 跳过本文件
        if ref.endswith("索引.md") or ref == "索引" or ref == "日志.md" or ref == "README.md" or ref == "AGENTS.md":
            continue
        # 拼路径
        candidates = [
            root / ref,
            root / f"{ref}.md",
            root / ref.replace("/", "/"),
        ]
        if not any(c.exists() for c in candidates):
            broken.append(ref)

    # 3. 跨文件 wiki link 校验
    other_broken = []
    for p in root.rglob("*.md"):
        rel = str(p.relative_to(root)).replace("\\", "/")
        if rel == INDEX_FILE:
            continue
        try:
            text = p.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        for ref in re.findall(r"\[\[([^\]]+)\]\]", text):
            ref = ref.split("|")[0].strip()
            if "://" in ref:
                continue
            # 解析相对路径
            if "/" in ref:
                target = (p.parent / ref).resolve()
                if not target.suffix:
                    target = target.with_suffix(".md")
            else:
                target = root / f"{ref}.md"
            if not target.exists():
                other_broken.append(f"{rel} -> [[{ref}]]")

    fail = False
    if missing:
        print(f"FAIL: {len(missing)} 个 .md 不在 {INDEX_FILE} 中:")
        for m in missing:
            print(f"  - {m}")
        fail = True

    if broken:
        print(f"FAIL: {len(broken)} 个 {INDEX_FILE} 引用不存在:")
        for b in broken:
            print(f"  - {b}")
        fail = True

    if other_broken:
        print(f"FAIL: {len(other_broken)} 个跨文件 wiki link 失效:")
        for b in other_broken:
            print(f"  - {b}")
        fail = True

    if fail:
        sys.exit(1)
    else:
        print(f"PASS: {INDEX_FILE} covers {len(all_md)} markdown files")
        print(f"  - {INDEX_FILE} 中 wiki refs: {len(wiki_refs)}")
        print(f"  - 跨文件 wiki refs: ok")
        sys.exit(0)


if __name__ == "__main__":
    main()

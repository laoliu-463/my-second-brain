#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
跨实例索引 LINT

每个"第二大脑*/"实例独立校验 索引.md
检查项：
  - 所有 .md 在该实例的 索引.md 中被引用
  - 索引.md 引用都对应实际文件
  - 跨文件 wiki link 引用有效

用法：
  python 第二大脑/07-脚本/brain_lint.py
  python 第二大脑/07-脚本/brain_lint.py --root /path/to/vault
"""

import argparse
import re
import sys
from pathlib import Path

DEFAULT_ROOT = Path(__file__).resolve().parents[2]
INSTANCE_PREFIX = "第二大脑"
SKIP_FILES = {"索引.md", "日志.md", "README.md", "AGENTS.md"}


def find_instances(root: Path):
    for p in sorted(root.iterdir()):
        if p.is_dir() and (p.name == INSTANCE_PREFIX or p.name.startswith(INSTANCE_PREFIX + "-")):
            yield p


def check_instance(instance: Path) -> tuple:
    """检查单个实例的索引覆盖"""
    index_path = instance / "索引.md"
    if not index_path.exists():
        return False, ["  MISSING 索引.md"]

    index_text = index_path.read_text(encoding="utf-8", errors="ignore")

    # 1. 所有 .md 必须在索引中
    all_md = []
    for p in sorted(instance.rglob("*.md")):
        rel = str(p.relative_to(instance)).replace("\\", "/")
        all_md.append(rel)

    missing = []
    for rel in all_md:
        if rel in SKIP_FILES:
            continue
        if rel not in index_text and rel.replace(".md", "") not in index_text:
            missing.append(rel)

    # 2. 索引中引用必须对应实际文件
    wiki_refs = re.findall(r"\[\[([^\]]+)\]\]", index_text)
    broken = []
    root = instance.parent  # vault 根
    for ref in wiki_refs:
        ref = ref.split("|")[0].strip()
        if "://" in ref or ref.startswith("http") or ref.startswith("/"):
            continue
        if ref.endswith("索引.md") or ref in ("索引", "日志.md", "README.md", "AGENTS.md"):
            continue
        candidates = [
            instance / ref,
            instance / f"{ref}.md",
        ]
        # 跨实例跳转：../xxx/yyy.md
        if ref.startswith("../"):
            tail = ref[3:]
            # 优先在 vault 根下找
            candidates.append(root / f"{tail}.md")
            # 也可能在其他实例下
            for other in root.iterdir():
                if other.is_dir() and (other.name == INSTANCE_PREFIX or other.name.startswith(INSTANCE_PREFIX + "-")):
                    candidates.append(other / f"{tail}.md")
        if not any(c.exists() for c in candidates):
            broken.append(ref)

    # 3. 跨文件 wiki link 校验
    # 容忍跨实例引用：只要目标在 vault 任何"第二大脑"实例下即可
    other_broken = []
    root_dir = instance.parent
    brain_instances = [
        p for p in root_dir.iterdir()
        if p.is_dir() and (p.name == INSTANCE_PREFIX or p.name.startswith(INSTANCE_PREFIX + "-"))
    ]
    for p in instance.rglob("*.md"):
        rel = str(p.relative_to(instance)).replace("\\", "/")
        if rel == "索引.md":
            continue
        try:
            text = p.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        for ref in re.findall(r"\[\[([^\]]+)\]\]", text):
            ref = ref.split("|")[0].strip()
            if "://" in ref:
                continue
            # 解析路径
            if "/" in ref:
                # 跨实例 ../ 引用
                if ref.startswith("../"):
                    tail = ref[3:]
                    # tail 可能是 "实例名/子路径" 或 直接 "子路径"
                    # 在任何 brain instance 下找
                    found = False
                    for other in brain_instances:
                        # 1) tail 直接拼到 other 后
                        cand1 = other / f"{tail}.md"
                        cand2 = other / tail
                        if cand1.exists() or (cand2.exists() and cand2.is_file()):
                            found = True
                            break
                        if cand2.is_dir() and any(cand2.rglob("*.md")):
                            found = True
                            break
                        # 2) tail 是 "实例名/..."，去掉实例名再拼
                        parts = tail.split("/", 1)
                        if len(parts) == 2:
                            cand3 = other / f"{parts[1]}.md"
                            cand4 = other / parts[1]
                            if cand3.exists() or (cand4.exists() and cand4.is_file()):
                                found = True
                                break
                            if cand4.is_dir() and any(cand4.rglob("*.md")):
                                found = True
                                break
                    if not found:
                        other_broken.append(f"{rel} -> [[{ref}]]")
                else:
                    target = (p.parent / ref).resolve()
                    if not target.suffix:
                        target = target.with_suffix(".md")
                    if not target.exists():
                        other_broken.append(f"{rel} -> [[{ref}]]")
            else:
                # 不含 / 的 ref：先在当前 md 同目录找，再在整个 instance rglob 找
                target = p.parent / f"{ref}.md"
                if not target.exists():
                    found = False
                    for f in instance.rglob(f"{ref}.md"):
                        target = f
                        found = True
                        break
                    if not found:
                        other_broken.append(f"{rel} -> [[{ref}]]")

    fail = bool(missing or broken or other_broken)
    msg = []
    if missing:
        msg.append(f"  {len(missing)} 个 .md 不在 索引.md 中: {missing[:3]}")
    if broken:
        msg.append(f"  {len(broken)} 个 索引.md 引用不存在: {broken[:3]}")
    if other_broken:
        msg.append(f"  {len(other_broken)} 个跨文件 wiki link 失效: {other_broken[:3]}")

    return not fail, msg


def main():
    parser = argparse.ArgumentParser(description="跨实例索引 LINT")
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT, help="vault 根目录")
    args = parser.parse_args()

    root: Path = args.root
    if not root.exists():
        print(f"FAIL: vault 根不存在: {root}")
        sys.exit(1)

    instances = list(find_instances(root))
    if not instances:
        print("FAIL: 没找到任何第二大脑实例")
        sys.exit(1)

    print(f"=== 跨实例索引 LINT ===")
    print(f"vault 根: {root}")
    print(f"实例数: {len(instances)}")
    print()

    fail = False
    for inst in instances:
        rel = inst.relative_to(root)
        ok, msg = check_instance(inst)
        status = "PASS" if ok else "FAIL"
        print(f"[{status}] {rel}/")
        for m in msg:
            print(m)
        if not ok:
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

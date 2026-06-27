from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
KNOWLEDGE = ROOT / "知识库"
RAW_SOURCES = ROOT / "raw" / "sources"
TODAY = "2026-06-27"

KNOWN_RAW_REPLACEMENTS = {
    "raw/sources/javascript高级程序设计.pdf": "raw/sources/JavaScript高级程序设计（第4版 中文高清）.pdf",
    "raw/sources/Linux多线程服务端编程 书签高清非扫描 - 陈硕.pdf": "raw/sources/Linux多线程服务端编程_陈硕.pdf",
    "raw/sources/程序员的自我修养—链接、装载与库--书签目录.pdf": "raw/sources/程序员的自我修养_链接装载与库.pdf",
}

FRONTMATTER_RE = re.compile(r"(?s)^\s*---\s*\r?\n(?P<body>.*?)\r?\n---\s*(?P<rest>\r?\n.*)?$")
RAW_WIKILINK_RE = re.compile(r"\[\[\s*(raw/sources/[^\]\|#]+)(?:#[^\]\|]+)?(?:\|([^\]]+))?\]\]")
ORIGINAL_SECTION_RE = re.compile(r"(?ms)^##\s*原文链接\s*\r?\n(?P<body>.*?)(?=^##\s+|\Z)")


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def raw_file_set() -> set[str]:
    if not RAW_SOURCES.exists():
        return set()
    return {rel(path) for path in RAW_SOURCES.rglob("*") if path.is_file()}


def split_frontmatter(text: str) -> tuple[dict[str, str] | None, str | None, str]:
    match = FRONTMATTER_RE.match(text)
    if not match:
        return None, None, text
    block = match.group("body")
    rest = match.group("rest") or "\n"
    values: dict[str, str] = {}
    for line in block.splitlines():
        scalar = re.match(r"^\s*([A-Za-z_][A-Za-z0-9_]*)\s*:\s*(.*?)\s*$", line)
        if scalar:
            values[scalar.group(1)] = scalar.group(2).strip().strip('"').strip("'")
    return values, block, rest.lstrip("\n")


def first_heading(text: str) -> str | None:
    for line in text.splitlines():
        match = re.match(r"^#\s+(.+?)\s*$", line)
        if match:
            return match.group(1).strip()
    return None


def infer_type(path: Path) -> str:
    parts = path.relative_to(KNOWLEDGE).parts
    name = path.name.lower()
    if name == "index.md":
        return "index"
    if parts and parts[0] == "_review":
        return "review"
    if parts and parts[0] == "maps":
        return "map"
    if parts and parts[0] == "syntheses":
        return "synthesis"
    if parts and parts[0] == "entities":
        return "entity"
    if parts and parts[0] == "concepts":
        return "concept"
    if "runbook" in path.as_posix().lower() or "skills" in path.as_posix().lower():
        return "procedure"
    return "note"


def infer_status(path: Path) -> str:
    parts = path.relative_to(KNOWLEDGE).parts
    if parts and parts[0] == "_review":
        return "review"
    return "active"


def yaml_quote(value: str) -> str:
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def minimal_frontmatter(path: Path, text: str) -> str:
    title = first_heading(text) or path.stem
    return "\n".join(
        [
            "---",
            f"title: {yaml_quote(title)}",
            f"type: {infer_type(path)}",
            f"status: {infer_status(path)}",
            f"created_at: {TODAY}",
            f"updated_at: {TODAY}",
            "source_level: none",
            "sources: []",
            "raw_evidence: []",
            "related: []",
            "tags: []",
            "maintainers:",
            "  - codex",
            "confidence: 0.5",
            "---",
            "",
        ]
    )


def ensure_scalar(block: str, key: str, value: str) -> str:
    pattern = re.compile(rf"(?m)^(\s*{re.escape(key)}\s*:\s*).*$")
    if pattern.search(block):
        return pattern.sub(rf"\g<1>{value}", block, count=1)
    lines = block.splitlines()
    insert_at = 0
    for idx, line in enumerate(lines):
        if re.match(r"^\s*(title|type|status|created_at|created|updated_at|updated|source_level)\s*:", line):
            insert_at = idx + 1
    lines.insert(insert_at, f"{key}: {value}")
    return "\n".join(lines)


def ensure_updated(block: str) -> str:
    if re.search(r"(?m)^\s*updated_at\s*:", block):
        return re.sub(r"(?m)^(\s*updated_at\s*:\s*).*$", rf"\g<1>{TODAY}", block, count=1)
    if re.search(r"(?m)^\s*updated\s*:", block):
        return re.sub(r"(?m)^(\s*updated\s*:\s*).*$", rf"\g<1>{TODAY}", block, count=1)
    return ensure_scalar(block, "updated_at", TODAY)


def target_exists(target: str, raws: set[str]) -> bool:
    return target in raws


def replace_known_raw_targets(text: str) -> str:
    for old, new in KNOWN_RAW_REPLACEMENTS.items():
        text = text.replace(old, new)
    return text


def rewrite_missing_raw_wikilinks(text: str, raws: set[str]) -> str:
    fm_values, block, rest = split_frontmatter(text)

    def body_repl(match: re.Match[str]) -> str:
        target = match.group(1).strip()
        alias = (match.group(2) or Path(target).name).strip()
        if target_exists(target, raws):
            return match.group(0)
        return f"{alias}（原文缺失待核查：`{target}`）"

    if block is None:
        return RAW_WIKILINK_RE.sub(body_repl, text)

    def fm_repl(match: re.Match[str]) -> str:
        target = match.group(1).strip()
        if target_exists(target, raws):
            return match.group(0)
        return f"原文缺失待核查：{target}"

    new_block = RAW_WIKILINK_RE.sub(fm_repl, block)
    new_rest = RAW_WIKILINK_RE.sub(body_repl, rest)
    return f"---\n{new_block}\n---\n{new_rest}"


def raw_targets(text: str) -> list[str]:
    return sorted({match.group(1).strip() for match in RAW_WIKILINK_RE.finditer(text)})


def existing_raw_targets(text: str, raws: set[str]) -> list[str]:
    return [target for target in raw_targets(text) if target in raws]


def original_section_body(text: str) -> str | None:
    match = ORIGINAL_SECTION_RE.search(text)
    if not match:
        return None
    return match.group("body")


def has_missing_source_marker(text: str) -> bool:
    body = original_section_body(text)
    return bool(body and "原文缺失待核查" in body)


def insert_original_section(rest: str, section: str) -> str:
    lines = rest.splitlines()
    insert_at = 0
    for idx, line in enumerate(lines):
        if re.match(r"^#\s+", line):
            insert_at = idx + 1
            while insert_at < len(lines) and lines[insert_at].strip() == "":
                insert_at += 1
            break
    before = lines[:insert_at]
    after = lines[insert_at:]
    section_lines = ["", "## 原文链接", "", *section.splitlines(), ""]
    return "\n".join(before + section_lines + after).rstrip() + "\n"


def repair_original_section(rest: str, all_text: str, raws: set[str]) -> tuple[str, bool, str]:
    body = original_section_body(rest)
    if body is not None:
        targets = [target for target in raw_targets(body) if target in raws]
        if targets or "原文缺失待核查" in body:
            return rest, False, "already-ok"

    targets = existing_raw_targets(all_text, raws)
    if targets:
        section = "\n".join(f"- [[{target}|{Path(target).name}]]" for target in targets)
        if body is None:
            return insert_original_section(rest, section), True, "added-existing-raw"
        repaired = ORIGINAL_SECTION_RE.sub(f"## 原文链接\n\n{section}\n\n", rest, count=1)
        return repaired, True, "replaced-original-section"

    missing_mentions = sorted(set(re.findall(r"原文缺失待核查：`?([^`\n）]+)`?", all_text)))
    if missing_mentions:
        section = "\n".join(f"- 原文缺失待核查：`{target.strip()}`" for target in missing_mentions)
        if body is None:
            return insert_original_section(rest, section), True, "added-missing-marker"
        repaired = ORIGINAL_SECTION_RE.sub(f"## 原文链接\n\n{section}\n\n", rest, count=1)
        return repaired, True, "replaced-missing-marker"

    return rest, False, "no-source"


def is_formal(path: Path) -> bool:
    relative = rel(path)
    if not relative.startswith("知识库/"):
        return False
    if re.match(r"^知识库/(_review|_meta|sources|90-来源与映射)(/|$)", relative):
        return False
    return path.suffix.lower() == ".md"


def repair_file(path: Path, raws: set[str]) -> str | None:
    original = path.read_text(encoding="utf-8", errors="replace")
    text = replace_known_raw_targets(original)
    text = rewrite_missing_raw_wikilinks(text, raws)
    fm_values, block, rest = split_frontmatter(text)

    changed_reasons: list[str] = []

    if block is None:
        text = minimal_frontmatter(path, text) + text.lstrip("\ufeff")
        fm_values, block, rest = split_frontmatter(text)
        changed_reasons.append("frontmatter")

    assert block is not None
    assert rest is not None

    new_block = ensure_updated(block)
    if new_block != block:
        changed_reasons.append("updated")
    block = new_block

    new_rest = rest
    if is_formal(path):
        combined = f"---\n{block}\n---\n{rest}"
        new_rest, section_changed, section_reason = repair_original_section(rest, combined, raws)
        if section_changed:
            changed_reasons.append(section_reason)
        if section_reason == "no-source":
            with_source_none = ensure_scalar(block, "source_level", "none")
            if with_source_none != block:
                block = with_source_none
                changed_reasons.append("source-none")

    repaired = f"---\n{block}\n---\n{new_rest}"
    if repaired != original:
        path.write_text(repaired, encoding="utf-8", newline="\n")
        return ",".join(changed_reasons) or "normalized"
    return None


def main() -> None:
    raws = raw_file_set()
    changed: list[tuple[str, str]] = []
    for path in sorted(KNOWLEDGE.rglob("*.md")):
        reason = repair_file(path, raws)
        if reason:
            changed.append((rel(path), reason))
    print(f"changed={len(changed)}")
    for item, reason in changed[:200]:
        print(f"{reason}\t{item}")
    if len(changed) > 200:
        print(f"... {len(changed) - 200} more")


if __name__ == "__main__":
    main()

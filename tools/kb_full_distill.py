from __future__ import annotations

import hashlib
import re
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TODAY = "2026-06-23"
WIKI = ROOT / "知识库"
RAW = ROOT / "raw"
SOURCE_DIR = WIKI / "sources"
META_DIR = WIKI / "_meta"
REVIEW_DIR = WIKI / "_review"
MAPS_DIR = WIKI / "maps"
LEGACY_SOURCE_PAGE_FLAG = "--legacy-source-pages"

EXCLUDE_PARTS = {".git", ".obsidian", ".claude", ".cursor", "__pycache__"}
STRUCTURAL_NAMES = {
    "AGENTS.md",
    "README.md",
    "CLAUDE.md",
    "index.md",
    "索引.md",
    "日志.md",
}
STRUCTURAL_PARTS = {
    "00-规范",
    "01-状态",
    "02-总览",
    "02-项目总览",
    "04-流程",
    "04-运行流程",
    "05-任务",
    "05-任务管理",
    "06-报告",
    "06-报告证据",
    "07-脚本",
    "08-模板",
    "_meta",
    "_review",
}


@dataclass(frozen=True)
class RawFile:
    path: Path
    rel: str
    size: int
    sha256: str


@dataclass
class SourceGroup:
    source_id: str
    title: str
    source_type: str
    files: list[RawFile]
    author: str = "待确认"
    published: str = "待确认"
    collected: str = TODAY
    link: str = "本地原始资料"
    target_hint: str = "待沉淀到知识页"


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def ensure_dirs() -> None:
    for path in [SOURCE_DIR, META_DIR, REVIEW_DIR, MAPS_DIR]:
        path.mkdir(parents=True, exist_ok=True)


def all_files() -> list[Path]:
    files: list[Path] = []
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if any(part in EXCLUDE_PARTS for part in path.relative_to(ROOT).parts):
            continue
        files.append(path)
    return sorted(files, key=lambda p: rel(p).lower())


def read_text(path: Path, limit: int | None = None) -> str:
    data = path.read_bytes()
    if limit is not None:
        data = data[:limit]
    for enc in ("utf-8-sig", "utf-8", "gb18030", "utf-16"):
        try:
            return data.decode(enc)
        except UnicodeDecodeError:
            continue
    return data.decode("utf-8", errors="replace")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def slug_text(value: str, max_len: int = 42) -> str:
    value = Path(value).stem
    value = value.replace("+", "-").replace("_", "-").replace(" ", "-")
    value = re.sub(r"[\\/:*?\"<>|#\[\]()`~!@$%^&=;,，。、《》【】（）()]+", "-", value)
    value = re.sub(r"-+", "-", value).strip("-")
    if not value:
        value = "source"
    return value[:max_len].strip("-") or "source"


def stable_suffix(paths: list[Path]) -> str:
    raw = "\n".join(sorted(rel(path) for path in paths)).encode("utf-8")
    return hashlib.sha1(raw).hexdigest()[:8]


def date_from_name_or_mtime(path: Path) -> str:
    name = path.name
    match = re.search(r"(20\d{2})[-_年.]?(\d{2})[-_月.]?(\d{2})", name)
    if match:
        return "".join(match.groups())
    ts = datetime.fromtimestamp(path.stat().st_mtime)
    return ts.strftime("%Y%m%d")


def title_of(path: Path, text: str | None = None) -> str:
    if text is None and path.suffix.lower() == ".md":
        text = read_text(path, limit=20000)
    if text:
        fm = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, flags=re.S)
        if fm:
            match = re.search(r"(?m)^title:\s*[\"']?(.+?)[\"']?\s*$", fm.group(1))
            if match:
                return match.group(1).strip()
        match = re.search(r"(?m)^#\s+(.+?)\s*$", text)
        if match:
            return match.group(1).strip()
    return path.stem.strip()


def has_complete_original(path: Path, text: str) -> str:
    if rel(path).startswith("raw/"):
        return "是"
    if path.suffix.lower() != ".md":
        return "未确认"
    if len(text) > 5000 and ("source:" in text[:3000] or "http" in text[:5000] or "原文" in text[:5000]):
        return "可能"
    if len(text) > 20000 and len(re.findall(r"(?m)^#{1,3}\s+", text)) >= 4:
        return "可能"
    return "否"


def has_notes_or_ai(text: str) -> str:
    markers = ["批注", "个人", "AI", "总结", "摘要", "待验证", "我的", "观点", "复盘"]
    return "是" if any(marker in text[:8000] for marker in markers) else "否"


def original_link(text: str) -> str:
    match = re.search(r"https?://[^\s)>\"]+", text)
    return match.group(0) if match else "未发现"


def classify_md(path: Path, text: str) -> tuple[str, str]:
    r = rel(path)
    parts = path.relative_to(ROOT).parts
    name = path.name
    title = title_of(path, text)
    lowered = r.lower()

    if r.startswith("raw/"):
        return "raw-source", "raw 原始层"
    if name in STRUCTURAL_NAMES or any(part in STRUCTURAL_PARTS for part in parts):
        return "unknown", "结构、索引、任务、日志或模板文件"
    if "/sources/" in r or "\\sources\\" in r or r.startswith("知识库/sources/"):
        return "source-note", "来源页或来源索引"
    if r.startswith("00-收集箱/") or r.startswith("00-收件箱/"):
        if len(text) > 5000 and has_notes_or_ai(text) == "是":
            return "mixed", "收件箱长文且混合批注/摘要"
        return "raw-source", "收件箱原文或待归档来源"
    if "未命名" in title or "一些想法" in title or "读后感" in title or "总结2" in title or "新版整理" in title:
        return "mixed", "模糊标题，需人工复核"
    if "?" in title or "？" in title or "待确认" in title or "问题" in title:
        return "question", "问题或待确认页面"
    if any(token in r for token in ["entities", "人物", "组织", "产品", "项目"]):
        return "entity", "实体页目录或实体语义"
    if any(token in r for token in ["syntheses", "总览", "索引", "地图", "路线", "计划", "对照", "报告", "时间线", "复盘", "体系"]):
        return "synthesis", "跨页汇总、索引、路线或体系页"
    if any(token in lowered for token in ["adr-", "decision", "contract", "runbook", "workflow"]):
        return "synthesis", "工程决策、合同、运行手册或流程"
    if len(text) > 12000 and ("原文" in text[:3000] or "http" in text[:3000]):
        return "source-note", "长文来源笔记"
    return "concept", "稳定概念、方法或知识页"


def raw_groups(files: list[Path]) -> list[SourceGroup]:
    raw_files = [p for p in files if rel(p).startswith("raw/") and p.is_file()]
    hash_cache = {p: RawFile(p, rel(p), p.stat().st_size, sha256_file(p)) for p in raw_files}
    groups: list[SourceGroup] = []

    # Existing source-id directories are already canonical raw containers.
    for directory in sorted((RAW / "sources").glob("src-*")):
        if not directory.is_dir():
            continue
        members = [hash_cache[p] for p in sorted(directory.rglob("*")) if p.is_file() and p in hash_cache]
        if not members:
            continue
        sid = directory.name
        groups.append(
            SourceGroup(
                source_id=sid,
                title=sid,
                source_type="canonical-raw-dir",
                files=members,
                target_hint=f"[[知识库/sources/{sid}]]",
            )
        )

    # Akkkk video source is a logical group across transcript/json/video files.
    ak_groups: dict[str, list[RawFile]] = defaultdict(list)
    for p in raw_files:
        r = rel(p)
        if "Akkkk缺失视频" not in r:
            continue
        match = re.search(r"(20\d{2})-(\d{2})-(\d{2})_(\d+)", p.name)
        if match:
            key = f"{match.group(1)}{match.group(2)}{match.group(3)}-{match.group(4)}"
            ak_groups[key].append(hash_cache[p])
    for key, members in sorted(ak_groups.items()):
        date, video_id = key.split("-", 1)
        sid = f"src-{date}-akkkk-video-{video_id}"
        groups.append(
            SourceGroup(
                source_id=sid,
                title=f"Akkkk 缺失视频 {date} {video_id}",
                source_type="video-transcript",
                files=sorted(members, key=lambda f: f.rel),
                author="Akkkk",
                published=f"{date[:4]}-{date[4:6]}-{date[6:]}",
                collected="2026-05-01",
                link="本地视频、元数据与转写",
                target_hint="[[知识库/06-内容创作与传播/Akkkk视频原文归档/index]]",
            )
        )

    grouped_paths = {f.path for group in groups for f in group.files}
    for p in raw_files:
        if p in grouped_paths:
            continue
        parts = p.relative_to(ROOT).parts
        if parts[0] == "raw" and len(parts) >= 3:
            if parts[1] == "sources":
                bucket = parts[2]
            elif parts[1] == "assets":
                bucket = parts[2] if len(parts) > 2 else "assets"
            else:
                bucket = parts[1]
        else:
            bucket = "raw"
        date = date_from_name_or_mtime(p)
        suffix = stable_suffix([p])
        slug = slug_text(p.name, max_len=36)
        sid = f"src-{date}-local-{slug}-{suffix}"
        author = "待确认"
        target = "待沉淀到知识页"
        if "中美博弈" in p.name or bucket == "中美博弈系列":
            author = "待确认"
            target = "[[知识库/03-地缘政治/中美博弈/index]]"
        elif bucket == "醒与悟系列":
            target = "[[知识库/05-认知与成长/01-人智认知系列/index]]"
        elif "大学物理" in bucket:
            target = "[[知识库/08-大学物理复习/index]]"
        elif bucket == "抖音团长SaaS设计文档":
            target = "[[知识库/09-SaaS体系/index]]"
        elif p.suffix.lower() == ".pdf":
            target = "按书籍主题页或领域索引引用"
        groups.append(
            SourceGroup(
                source_id=sid,
                title=p.stem,
                source_type=f"raw-file:{bucket}",
                files=[hash_cache[p]],
                author=author,
                published="待确认",
                collected=datetime.fromtimestamp(p.stat().st_mtime).strftime("%Y-%m-%d"),
                link="本地原始资料",
                target_hint=target,
            )
        )
    return sorted(groups, key=lambda g: g.source_id)


def source_page(group: SourceGroup) -> str:
    original_paths = "\n".join(
        f"- [[{item.rel}|原文]] (`{item.rel}`) | size={item.size} | sha256=`{item.sha256}`" for item in group.files
    )
    first_path = group.files[0].rel if group.files else "待确认"
    first_link = f"[[{first_path}|原文]]" if first_path != "待确认" else "待确认"
    aliases = [group.title]
    aliases_text = "\n".join(f"  - {alias}" for alias in aliases)
    return f"""---
source_id: {group.source_id}
original_title: "{group.title}"
title: "{group.title}"
aliases:
{aliases_text}
author: "{group.author}"
published: "{group.published}"
collected: "{group.collected}"
original_link: "{group.link}"
raw_path: "{first_path}"
type: source
created: {TODAY}
updated: {TODAY}
tags:
  - source
  - raw-evidence
---

# {group.title}

## 来源元数据

| 字段 | 值 |
|---|---|
| source_id | `{group.source_id}` |
| original_title | {group.title} |
| title | {group.title} |
| 作者/机构 | {group.author} |
| 发布日期 | {group.published} |
| 采集日期 | {group.collected} |
| 原始链接 | {group.link} |
| 来源类型 | {group.source_type} |

## 原文路径与跳转

{original_paths}

## 一句话摘要

待人工阅读或抽取后补充；当前页面先作为证据层登记页，避免原文散落无来源页。

## 作者核心观点

- 待补充。

## 证据地图

- 原文：{first_link}

## 个人批注

- 待补充。

## 待验证项

- 作者、发布日期、版本信息需人工确认。
- 若该来源已有更准确标题或正式链接，应只更新本来源页，不改动 raw 原文。

## 影响的知识页

- {group.target_hint}
"""


def write_source_pages(groups: list[SourceGroup]) -> tuple[int, int]:
    created = 0
    existing = 0
    for group in groups:
        path = SOURCE_DIR / f"{group.source_id}.md"
        if path.exists():
            existing += 1
            continue
        path.write_text(source_page(group), encoding="utf-8", newline="\n")
        created += 1
    return created, existing


def page_inventory(md_files: list[Path]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    seen_titles: dict[str, list[str]] = defaultdict(list)
    raw_texts: dict[Path, str] = {}
    for path in md_files:
        text = read_text(path)
        raw_texts[path] = text
        seen_titles[title_of(path, text).lower()].append(rel(path))

    for path in md_files:
        text = raw_texts[path]
        typ, reason = classify_md(path, text)
        title = title_of(path, text)
        link = original_link(text)
        suggested_source = ""
        if typ in {"raw-source", "source-note", "mixed"}:
            date = date_from_name_or_mtime(path)
            suggested_source = f"src-{date}-local-{slug_text(title, 32)}-{stable_suffix([path])}"
        dup = "; ".join(p for p in seen_titles[title.lower()] if p != rel(path))[:180]
        target = suggest_target(path, typ, title)
        rows.append(
            {
                "path": rel(path),
                "title": title.replace("|", "\\|"),
                "type": typ,
                "full_original": has_complete_original(path, text),
                "notes_ai": has_notes_or_ai(text),
                "link_author_date": link.replace("|", "\\|"),
                "source_id": suggested_source,
                "duplicate": dup.replace("|", "\\|") if dup else "",
                "merge_to": target.replace("|", "\\|"),
                "target_path": target.replace("|", "\\|"),
                "risk": reason.replace("|", "\\|"),
            }
        )
    return rows


def suggest_target(path: Path, typ: str, title: str) -> str:
    r = rel(path)
    if typ == "raw-source":
        return "raw/sources 或 知识库/sources/<source_id>.md"
    if typ == "source-note":
        return "知识库/sources/ 或 对应概念页"
    if typ == "concept":
        return f"知识库/concepts/{title}.md"
    if typ == "entity":
        return f"知识库/entities/{title}.md"
    if typ == "synthesis":
        return f"知识库/syntheses/{title}.md"
    if typ == "question":
        return f"知识库/questions/{title}.md"
    if typ == "mixed":
        return "知识库/_review/unresolved-items.md"
    return r


def write_sources_index(groups: list[SourceGroup]) -> None:
    by_type: dict[str, list[SourceGroup]] = defaultdict(list)
    for group in groups:
        by_type[group.source_type].append(group)
    lines = [
        "---",
        "title: 来源页索引",
        f"updated: {TODAY}",
        "tags:",
        "  - index",
        "  - source",
        "---",
        "",
        "# 来源页索引",
        "",
        f"- 来源组总数：{len(groups)}",
        "- 规则：一份来源对应一个来源页；raw 原文只登记路径和哈希，不在来源页改写原文。",
        "",
    ]
    for typ in sorted(by_type):
        items = sorted(by_type[typ], key=lambda g: g.source_id)
        lines.extend([f"## {typ}", ""])
        for group in items:
            lines.append(f"- [[知识库/sources/{group.source_id}|{group.title}]]")
        lines.append("")
    (SOURCE_DIR / "index.md").write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8", newline="\n")


def write_inventory(rows: list[dict[str, str]], files: list[Path], groups: list[SourceGroup]) -> None:
    ext_counts = Counter(path.suffix.lower() or "<none>" for path in files)
    type_counts = Counter(row["type"] for row in rows)
    top_counts = Counter(path.relative_to(ROOT).parts[0] for path in files)
    lines = [
        "---",
        "title: 内容清单",
        "created: 2026-06-23",
        f"updated: {TODAY}",
        "tags:",
        "  - inventory",
        "  - migration",
        "---",
        "",
        "# 内容清单",
        "",
        "## 扫描摘要",
        "",
        f"- 扫描根目录：`{ROOT}`",
        "- 扫描范围：除 `.git/`、`.obsidian/`、`.claude/`、`.cursor/` 外的全库文件",
        f"- 扫描文件数：{len(files)}",
        f"- Markdown 文件数：{len(rows)}",
        f"- raw 来源组数：{len(groups)}",
        "- 执行模式：apply；未自动删除文件；未移动大体积 raw 原文",
        "",
        "## 类型分布",
        "",
        "| 类型 | 数量 |",
        "|---|---:|",
    ]
    for typ, count in sorted(type_counts.items()):
        lines.append(f"| {typ} | {count} |")
    lines.extend(["", "## 扩展名分布", "", "| 扩展名 | 数量 |", "|---|---:|"])
    for ext, count in ext_counts.most_common():
        lines.append(f"| `{ext}` | {count} |")
    lines.extend(["", "## 一级目录分布", "", "| 一级目录 | 文件数 |", "|---|---:|"])
    for top, count in top_counts.most_common():
        lines.append(f"| `{top}` | {count} |")
    lines.extend(
        [
            "",
            "## 全量 Markdown 清单",
            "",
            "| 原始路径 | 当前标题 | 文件类型 | 是否包含完整原文 | 是否包含个人批注或 AI 总结 | 原始链接、作者和日期 | 建议 source_id | 重复候选 | 建议合并到的知识页 | 目标路径 | 风险和待确认项 |",
            "|---|---|---|---|---|---|---|---|---|---|---|",
        ]
    )
    for row in rows:
        lines.append(
            "| `{path}` | {title} | {type} | {full_original} | {notes_ai} | {link_author_date} | `{source_id}` | {duplicate} | {merge_to} | {target_path} | {risk} |".format(
                **row
            )
        )
    (META_DIR / "content-inventory.md").write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8", newline="\n")


def write_migration_plan(rows: list[dict[str, str]], groups: list[SourceGroup], created_sources: int, existing_sources: int) -> None:
    counts = Counter(row["type"] for row in rows)
    lines = [
        "---",
        "title: 全量内容迁移计划",
        f"updated: {TODAY}",
        "tags:",
        "  - migration",
        "  - plan",
        "---",
        "",
        "# 全量内容迁移计划",
        "",
        "## 本轮已执行",
        "",
        f"- 生成/刷新全量内容清单：`知识库/_meta/content-inventory.md`。",
        f"- raw 来源组登记：{len(groups)} 个。",
        f"- 新建缺失来源页：{created_sources} 个；已存在来源页：{existing_sources} 个。",
        "- 刷新来源页索引：`知识库/sources/index.md`。",
        "- 刷新主题沉淀地图：`知识库/maps/content-distillation-map.md`。",
        "- 刷新复核清单：`知识库/_review/unresolved-items.md`。",
        "",
        "## 当前分类基线",
        "",
        "| 文件类型 | 数量 | 后续动作 |",
        "|---|---:|---|",
    ]
    action = {
        "raw-source": "保留 raw 原文不改写；确认来源页和哈希。",
        "source-note": "归并到来源页；只把可复用知识回链到概念/综合页，并补原文跳转链接。",
        "concept": "保留或合并到同义概念页；补来源回链和原文跳转链接。",
        "entity": "保留为实体页；补 aliases、来源和关联概念。",
        "synthesis": "作为跨来源综合页维护；补证据地图。",
        "question": "放入 questions 或复核清单，等待证据闭环。",
        "mixed": "优先拆分原文、摘要和个人批注；不得覆盖原文。",
        "unknown": "结构文件或无法判断文件，人工复核后再迁移。",
    }
    for typ, count in sorted(counts.items()):
        lines.append(f"| {typ} | {count} | {action.get(typ, '待确认')} |")
    lines.extend(
        [
            "",
            "## 可逆策略",
            "",
            "- 本轮不删除文件。",
            "- 本轮不批量移动历史知识页，避免断链扩大。",
            "- 新来源页均可通过 `source_id` 和 raw 路径追溯；若发现误建，可改为重定向或复核项。",
            "- 后续物理迁移应以 `content-inventory.md` 为输入，按目录或主题分批执行。",
            "",
            "## 下一批优先级",
            "",
            "1. `mixed`：混合原文、摘要和批注的页面。",
            "2. `raw-source`：已有 raw 但无人工摘要的来源页。",
            "3. 标题含 `未命名`、`总结`、`读后感` 的页面。",
            "4. 无来源回链的概念页。",
        ]
    )
    (META_DIR / "migration-plan.md").write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8", newline="\n")


def write_review(rows: list[dict[str, str]], groups: list[SourceGroup]) -> None:
    risky = [
        row
        for row in rows
        if row["type"] in {"mixed", "unknown", "question"}
        or "未命名" in row["title"]
        or "总结2" in row["title"]
        or "读后感" in row["title"]
    ]
    duplicate_titles = [row for row in rows if row["duplicate"]]
    lines = [
        "---",
        "title: 待人工复核项",
        f"updated: {TODAY}",
        "tags:",
        "  - review",
        "  - migration",
        "---",
        "",
        "# 待人工复核项",
        "",
        "## 本轮自动化边界",
        "",
        "- 未删除文件。",
        "- 未覆盖 raw 原文。",
        "- 未把无法判断的页面强行迁移到概念页。",
        "- 来源页中作者、发布日期、正式链接为 `待确认` 的条目，需要人工补证据。",
        "",
        "## 高优先级复核",
        "",
        "| 路径 | 标题 | 类型 | 原因 |",
        "|---|---|---|---|",
    ]
    for row in risky[:300]:
        lines.append(f"| `{row['path']}` | {row['title']} | {row['type']} | {row['risk']} |")
    lines.extend(["", "## 重复候选", "", "| 路径 | 标题 | 重复候选 |", "|---|---|---|"])
    for row in duplicate_titles[:300]:
        lines.append(f"| `{row['path']}` | {row['title']} | {row['duplicate']} |")
    lines.extend(
        [
            "",
            "## 本轮未自动处理的系统性问题",
            "",
            "- `tmp/cpp-*` 与 `tmp/orig/C++.md` 是临时文件，已进入 Git 历史；因用户规范禁止自动删除，本轮仅记录，不删除。",
            "- 根目录 `人智认知系列.md` 曾是 0 字节文件，本轮改为兼容入口；是否保留根目录入口仍需人工确认。",
            "- `第二大脑/AGENTS.md` 与根 `README.md` 对可写范围存在差异：前者偏向只写 `第二大脑/`，后者把 `知识库/` 作为正式 wiki。",
            "- 多个 PDF/视频来源缺少作者、发布日期、正式链接；来源页已登记 raw 路径和哈希，但摘要和核心观点需后续阅读补齐。",
        ]
    )
    (REVIEW_DIR / "unresolved-items.md").write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8", newline="\n")


def write_map(rows: list[dict[str, str]], groups: list[SourceGroup]) -> None:
    by_type = Counter(row["type"] for row in rows)
    raw_by_hint = Counter(group.target_hint for group in groups)
    lines = [
        "---",
        "title: 内容沉淀地图",
        f"updated: {TODAY}",
        "tags:",
        "  - map",
        "  - distillation",
        "---",
        "",
        "# 内容沉淀地图",
        "",
        "## 页面类型入口",
        "",
        "- 来源页：[[知识库/sources/index]]",
        "- 概念页：[[知识库/concepts/index]]",
        "- 实体页：[[知识库/entities/index]]",
        "- 综合页：[[知识库/syntheses/index]]",
        "- 复核项：[[知识库/_review/unresolved-items]]",
        "- 全量清单：[[知识库/_meta/content-inventory]]",
        "",
        "## 当前分类分布",
        "",
        "| 类型 | 数量 |",
        "|---|---:|",
    ]
    for typ, count in sorted(by_type.items()):
        lines.append(f"| {typ} | {count} |")
    lines.extend(["", "## raw 来源主要沉淀方向", "", "| 目标知识页/领域 | 来源组数 |", "|---|---:|"])
    for target, count in raw_by_hint.most_common():
        lines.append(f"| {target} | {count} |")
    lines.extend(
        [
            "",
            "## 合并规则",
            "",
            "- 原文只在 raw 层保存，来源页只保存路径、哈希、原文跳转链接、摘要、证据地图和批注。",
            "- 多篇文章支持同一概念时，更新概念页而不是复制文章笔记。",
            "- 单篇文章的语境、修辞和案例保留在来源页。",
            "- 冲突观点保留双方来源、日期和证据，不自动消解。",
        ]
    )
    (MAPS_DIR / "content-distillation-map.md").write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8", newline="\n")


def append_log(files: list[Path], rows: list[dict[str, str]], groups: list[SourceGroup], created_sources: int, existing_sources: int) -> None:
    counts = Counter(row["type"] for row in rows)
    lines = [
        "",
        f"## {TODAY} 全量文章内容整理",
        "",
        f"- 扫描文件：{len(files)}；Markdown：{len(rows)}；raw 来源组：{len(groups)}。",
        f"- 新建来源页：{created_sources}；已有来源页：{existing_sources}。",
        "- 刷新：`content-inventory.md`、`migration-plan.md`、`sources/index.md`、`content-distillation-map.md`、`unresolved-items.md`。",
        "- 安全边界：未删除文件，未覆盖 raw 原文，未批量移动历史知识页。",
        "- 分类分布：" + "；".join(f"{k}={v}" for k, v in sorted(counts.items())),
    ]
    path = META_DIR / "distillation-log.md"
    previous = path.read_text(encoding="utf-8") if path.exists() else "---\ntitle: 沉淀日志\n---\n\n# 沉淀日志\n"
    path.write_text(previous.rstrip() + "\n" + "\n".join(lines) + "\n", encoding="utf-8", newline="\n")


def main() -> None:
    if LEGACY_SOURCE_PAGE_FLAG not in sys.argv:
        raise SystemExit(
            "kb_full_distill.py is a legacy source-page migration script. "
            "Current source integrity is knowledge page -> raw/sources direct links. "
            f"Re-run with {LEGACY_SOURCE_PAGE_FLAG} only when intentionally maintaining historical source pages."
        )
    ensure_dirs()
    files = all_files()
    md_files = [p for p in files if p.suffix.lower() == ".md"]
    groups = raw_groups(files)
    created_sources, existing_sources = write_source_pages(groups)
    rows = page_inventory(md_files)
    write_sources_index(groups)
    write_inventory(rows, files, groups)
    write_migration_plan(rows, groups, created_sources, existing_sources)
    write_review(rows, groups)
    write_map(rows, groups)
    append_log(files, rows, groups, created_sources, existing_sources)
    print(
        f"files={len(files)} md={len(rows)} raw_source_groups={len(groups)} "
        f"created_sources={created_sources} existing_sources={existing_sources}"
    )


if __name__ == "__main__":
    main()

#!/usr/bin/env python
"""Unified memory capture entrypoint for project agents.

Local transcripts are stored under tmp/agent-memory-transcripts/. EverOS Cloud
receives only a deterministic, redacted summary.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sys
import time
import uuid
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import everos_memory


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TRANSCRIPT_DIR = PROJECT_ROOT / "tmp" / "agent-memory-transcripts"
DEFAULT_MAX_CLOUD_CHARS = 8000
DEFAULT_SESSION_ID = "my-second-brain-agent-capture"

SECRET_PATTERNS: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"(?i)(EVEROS_API_KEY|OPENAI_API_KEY|ANTHROPIC_API_KEY)\s*[=:]\s*[^\s\"']+"), r"\1=[REDACTED]"),
    (re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"), "[REDACTED_OPENAI_KEY]"),
    (re.compile(r"\bghp_[A-Za-z0-9]{20,}\b"), "[REDACTED_GITHUB_TOKEN]"),
    (re.compile(r"\beyJ[A-Za-z0-9_-]{20,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\b"), "[REDACTED_JWT]"),
    (re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----.*?-----END [A-Z ]*PRIVATE KEY-----", re.S), "[REDACTED_PRIVATE_KEY]"),
    (re.compile(r"[A-Za-z]:\\Users\\[^\\\r\n\t ]+"), r"[REDACTED_USER_PATH]"),
    (re.compile(r"/[cC]/[Uu]sers/[^/\r\n\t ]+"), r"[REDACTED_USER_PATH]"),
]

COGNITIVE_KEYWORDS = {
    "认知",
    "政治",
    "经济",
    "政治经济",
    "地缘",
    "博弈",
    "社会",
    "阶层",
    "制度",
    "资本",
    "宏观",
    "趋势",
    "人性",
    "学习",
    "成长",
}

DECISION_KEYWORDS = {
    "决定",
    "确认",
    "选择",
    "接受",
    "必须",
    "要求",
    "策略",
    "方案",
    "结论",
    "根因",
    "验证",
}


@dataclass
class CaptureRecord:
    capture_id: str
    captured_at_ms: int
    agent: str
    source: str
    session_id: str
    project_root: str
    transcript_path: str
    metadata_path: str
    char_count: int
    redacted_char_count: int
    cognitive_required: bool
    cloud_written: bool
    cloud_error: str | None


def now_ms() -> int:
    return int(time.time() * 1000)


def redact(text: str) -> str:
    redacted = text
    for pattern, replacement in SECRET_PATTERNS:
        redacted = pattern.sub(replacement, redacted)
    return redacted


def meaningful_lines(text: str, limit: int = 80) -> list[str]:
    lines: list[str] = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        if len(line) > 600:
            line = line[:600] + "..."
        lines.append(line)
        if len(lines) >= limit:
            break
    return lines


def detect_cognitive(text: str) -> bool:
    return any(keyword in text for keyword in COGNITIVE_KEYWORDS)


def select_key_lines(lines: list[str], keywords: set[str], limit: int) -> list[str]:
    selected: list[str] = []
    for line in lines:
        if any(keyword in line for keyword in keywords):
            selected.append(line)
        if len(selected) >= limit:
            break
    return selected


def build_cloud_summary(
    *,
    agent: str,
    source: str,
    session_id: str,
    capture_id: str,
    raw_text: str,
    max_chars: int = DEFAULT_MAX_CLOUD_CHARS,
) -> tuple[str, bool]:
    redacted = redact(raw_text)
    lines = meaningful_lines(redacted)
    cognitive_required = detect_cognitive(redacted)
    decisions = select_key_lines(lines, DECISION_KEYWORDS, 12)
    cognitive_lines = select_key_lines(lines, COGNITIVE_KEYWORDS, 12)
    excerpt = "\n".join(lines[:30])

    blocks = [
        "Agent memory capture summary",
        f"capture_id: {capture_id}",
        f"agent: {agent}",
        f"source: {source}",
        f"project: my second brain",
        f"session_id: {session_id}",
        f"chars: {len(raw_text)}",
        f"cognitive_required: {str(cognitive_required).lower()}",
    ]

    if decisions:
        blocks.append("key_decision_lines:\n" + "\n".join(f"- {line}" for line in decisions))
    if cognitive_lines:
        blocks.append("cognitive_lines:\n" + "\n".join(f"- {line}" for line in cognitive_lines))

    blocks.append("redacted_excerpt:\n" + excerpt)
    summary = "\n\n".join(blocks)
    if len(summary) > max_chars:
        summary = summary[:max_chars] + "\n[TRUNCATED]"
    return summary, cognitive_required


TRANSCRIPT_PATH_KEYS = (
    "transcript_path",
    "transcriptPath",
    "transcript",
    "conversation_path",
    "conversationPath",
    "transcript_file",
    "transcriptFile",
)

CODEX_TEXT_KEYS = (
    "prompt",
    "user_prompt",
    "userPrompt",
    "message",
    "content",
    "input",
    "text",
    "response",
    "final_response",
    "finalResponse",
)


def read_transcript_path_from_event(event: dict[str, Any], metadata: dict[str, Any]) -> str | None:
    for key in TRANSCRIPT_PATH_KEYS:
        value = event.get(key)
        if not value or not isinstance(value, str):
            continue

        path = Path(value).expanduser()
        metadata["transcript_path_from_event"] = str(path)
        if path.exists() and path.is_file():
            return path.read_text(encoding="utf-8", errors="replace")
        metadata["transcript_missing"] = True
        return None

    return None


def read_claude_stop_json(text: str) -> tuple[str, dict[str, Any]]:
    try:
        event = json.loads(text)
    except json.JSONDecodeError:
        return text, {"input_format": "claude-stop-json", "parse_error": "invalid_json"}

    metadata: dict[str, Any] = {"input_format": "claude-stop-json", "event_keys": sorted(event.keys())}
    transcript_text = read_transcript_path_from_event(event, metadata) if isinstance(event, dict) else None
    if transcript_text is not None:
        return transcript_text, metadata

    return text, metadata


def collect_codex_text(value: Any) -> list[str]:
    if isinstance(value, str):
        stripped = value.strip()
        return [stripped] if stripped else []

    if isinstance(value, list):
        collected: list[str] = []
        for item in value:
            collected.extend(collect_codex_text(item))
        return collected

    if isinstance(value, dict):
        collected: list[str] = []
        for key in CODEX_TEXT_KEYS:
            if key in value:
                collected.extend(collect_codex_text(value[key]))
        return collected

    return []


def read_codex_hook_json(text: str) -> tuple[str, dict[str, Any]]:
    try:
        event = json.loads(text)
    except json.JSONDecodeError:
        return text, {"input_format": "codex-hook-json", "parse_error": "invalid_json"}

    if not isinstance(event, dict):
        return text, {"input_format": "codex-hook-json", "event_type": type(event).__name__}

    metadata: dict[str, Any] = {"input_format": "codex-hook-json", "event_keys": sorted(event.keys())}
    sections: list[str] = []
    hook_event_name = str(event.get("hook_event_name") or event.get("event_name") or "")
    for key in CODEX_TEXT_KEYS:
        if key in event:
            sections.extend(collect_codex_text(event[key]))

    for key in ("messages", "conversation", "turns"):
        if key in event:
            sections.extend(collect_codex_text(event[key]))

    if hook_event_name == "UserPromptSubmit" and sections:
        metadata["extracted_text_sections"] = len(sections)
        return "\n".join(sections), metadata

    transcript_text = read_transcript_path_from_event(event, metadata)
    if transcript_text is not None:
        return transcript_text, metadata

    if sections:
        metadata["extracted_text_sections"] = len(sections)
        return "\n".join(sections), metadata

    metadata["fallback_raw_json"] = True
    return text, metadata


def read_input(args: argparse.Namespace) -> tuple[str, dict[str, Any]]:
    metadata: dict[str, Any] = {"input_format": args.input_format}
    if args.text is not None:
        raw = args.text
    elif args.input_file:
        path = Path(args.input_file)
        raw = path.read_text(encoding=args.encoding, errors="replace")
        metadata["input_file"] = str(path)
    elif not sys.stdin.isatty():
        raw = sys.stdin.read()
    else:
        raise SystemExit("Provide --text, --input-file, or pipe transcript text on stdin.")

    if args.input_format == "claude-stop-json":
        return read_claude_stop_json(raw)
    if args.input_format == "codex-hook-json":
        return read_codex_hook_json(raw)
    return raw, metadata


def safe_agent_name(value: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9_.-]+", "-", value.strip().lower())
    return cleaned or "unknown"


def write_local_transcript(
    *,
    output_dir: Path,
    capture_id: str,
    agent: str,
    raw_text: str,
    metadata: dict[str, Any],
) -> tuple[Path, Path]:
    day = time.strftime("%Y%m%d")
    target_dir = output_dir / day / safe_agent_name(agent)
    target_dir.mkdir(parents=True, exist_ok=True)
    transcript_path = target_dir / f"{capture_id}.transcript.txt"
    metadata_path = target_dir / f"{capture_id}.metadata.json"
    transcript_path.write_text(raw_text, encoding="utf-8")
    metadata_path.write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8")
    return transcript_path, metadata_path


def write_cloud_summary(summary: str, args: argparse.Namespace) -> tuple[bool, str | None]:
    try:
        client = everos_memory.make_client()
        client.v1.memories.add(
            user_id=args.user_id or everos_memory.DEFAULT_USER_ID,
            session_id=args.everos_session_id or DEFAULT_SESSION_ID,
            messages=[
                {
                    "role": "user",
                    "timestamp": now_ms(),
                    "content": summary,
                }
            ],
            async_mode=False,
        )
        if args.flush:
            client.v1.memories.flush(
                user_id=args.user_id or everos_memory.DEFAULT_USER_ID,
                session_id=args.everos_session_id or DEFAULT_SESSION_ID,
            )
        return True, None
    except Exception as exc:  # pragma: no cover - exact SDK exceptions vary
        return False, f"{type(exc).__name__}: {exc}"


def capture(args: argparse.Namespace) -> CaptureRecord:
    raw_text, input_metadata = read_input(args)
    capture_id = args.capture_id or f"{int(time.time())}-{uuid.uuid4().hex[:12]}"
    redacted_summary, cognitive_required = build_cloud_summary(
        agent=args.agent,
        source=args.source,
        session_id=args.session_id,
        capture_id=capture_id,
        raw_text=raw_text,
        max_chars=args.max_cloud_chars,
    )

    metadata: dict[str, Any] = {
        **input_metadata,
        "capture_id": capture_id,
        "captured_at_ms": now_ms(),
        "agent": args.agent,
        "source": args.source,
        "session_id": args.session_id,
        "project_root": str(PROJECT_ROOT),
        "char_count": len(raw_text),
        "redacted_char_count": len(redact(raw_text)),
        "cognitive_required": cognitive_required,
        "cloud_summary_preview": redacted_summary[:1000],
    }

    transcript_path = Path("")
    metadata_path = Path("")
    if args.save_raw:
        transcript_path, metadata_path = write_local_transcript(
            output_dir=Path(args.output_dir),
            capture_id=capture_id,
            agent=args.agent,
            raw_text=raw_text,
            metadata=metadata,
        )

    cloud_written = False
    cloud_error: str | None = None
    if args.cloud and not args.dry_run:
        cloud_written, cloud_error = write_cloud_summary(redacted_summary, args)
        if cloud_error and args.fail_on_cloud_error:
            raise SystemExit(cloud_error)

    record = CaptureRecord(
        capture_id=capture_id,
        captured_at_ms=metadata["captured_at_ms"],
        agent=args.agent,
        source=args.source,
        session_id=args.session_id,
        project_root=str(PROJECT_ROOT),
        transcript_path=str(transcript_path),
        metadata_path=str(metadata_path),
        char_count=len(raw_text),
        redacted_char_count=len(redact(raw_text)),
        cognitive_required=cognitive_required,
        cloud_written=cloud_written,
        cloud_error=cloud_error,
    )

    if metadata_path:
        metadata.update({"cloud_written": cloud_written, "cloud_error": cloud_error})
        metadata_path.write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8")

    return record


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Capture agent transcript and write a redacted EverOS memory summary.")
    parser.add_argument("--agent", default="codex", help="Agent name, e.g. codex, claude, hermes.")
    parser.add_argument("--source", default="manual", help="Capture source, e.g. codex-wrapper, claude-stop.")
    parser.add_argument("--session-id", default=DEFAULT_SESSION_ID, help="Local capture session id.")
    parser.add_argument("--everos-session-id", help="EverOS Cloud session_id. Defaults to my-second-brain-agent-capture.")
    parser.add_argument("--user-id", help="EverOS user_id. Defaults to project default.")
    parser.add_argument("--input-file", help="Transcript or event file to capture.")
    parser.add_argument("--input-format", choices=["text", "claude-stop-json", "codex-hook-json"], default="text")
    parser.add_argument("--text", help="Transcript text to capture.")
    parser.add_argument("--encoding", default="utf-8")
    parser.add_argument("--output-dir", default=str(DEFAULT_TRANSCRIPT_DIR))
    parser.add_argument("--max-cloud-chars", type=int, default=DEFAULT_MAX_CLOUD_CHARS)
    parser.add_argument("--capture-id")
    parser.add_argument("--save-raw", dest="save_raw", action="store_true", default=True)
    parser.add_argument("--no-save-raw", dest="save_raw", action="store_false")
    parser.add_argument("--cloud", dest="cloud", action="store_true", default=True)
    parser.add_argument("--no-cloud", dest="cloud", action="store_false")
    parser.add_argument("--flush", dest="flush", action="store_true", default=True)
    parser.add_argument("--no-flush", dest="flush", action="store_false")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--fail-on-cloud-error", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    record = capture(args)
    print(json.dumps(asdict(record), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

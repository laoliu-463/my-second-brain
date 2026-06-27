#!/usr/bin/env python
"""EverOS Cloud helper for this knowledge base.

The script never stores API keys. Set EVEROS_API_KEY in the shell before
running live commands.
"""

from __future__ import annotations

import argparse
import importlib.metadata
import json
import os
import sys
import time
from pathlib import Path
from typing import Any


DEFAULT_USER_ID = "my-second-brain-owner"
DEFAULT_SESSION_ID = "my-second-brain"
DEFAULT_MEMORY_TYPES = ["episodic_memory", "profile"]


def read_windows_user_env(name: str) -> str | None:
    if os.name != "nt":
        return None

    try:
        import winreg
    except ImportError:
        return None

    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment") as key:
            value, _value_type = winreg.QueryValueEx(key, name)
    except OSError:
        return None

    return str(value) if value else None


def read_env(name: str) -> str | None:
    return os.getenv(name) or read_windows_user_env(name)


def now_ms() -> int:
    return int(time.time() * 1000)


def load_sdk():
    try:
        from everos_cloud import EverOS
    except ImportError as exc:
        raise SystemExit(
            "everos-cloud is not installed. Run: python -m pip install -r tools/requirements-everos.txt"
        ) from exc
    return EverOS


def make_client():
    api_key = read_env("EVEROS_API_KEY")
    if not api_key:
        raise SystemExit("EVEROS_API_KEY is not set.")

    EverOS = load_sdk()
    kwargs: dict[str, Any] = {}
    base_url = read_env("EVEROS_BASE_URL")
    timeout = read_env("EVEROS_TIMEOUT")
    if base_url:
        kwargs["base_url"] = base_url
    if timeout:
        kwargs["timeout"] = float(timeout)
    return EverOS(api_key=api_key, **kwargs)


def resolve_user_id(args: argparse.Namespace) -> str:
    return args.user_id or read_env("EVEROS_USER_ID") or DEFAULT_USER_ID


def resolve_session_id(args: argparse.Namespace) -> str:
    return args.session_id or read_env("EVEROS_SESSION_ID") or DEFAULT_SESSION_ID


def read_text(args: argparse.Namespace) -> str:
    if getattr(args, "content", None):
        return args.content

    if getattr(args, "file", None):
        path = Path(args.file)
        text = path.read_text(encoding=args.encoding)
        if args.max_chars and len(text) > args.max_chars:
            text = text[: args.max_chars]
        return text

    if not sys.stdin.isatty():
        return sys.stdin.read()

    raise SystemExit("Provide --content, --file, or pipe text on stdin.")


def as_jsonable(value: Any) -> Any:
    if hasattr(value, "model_dump"):
        return value.model_dump(mode="json")
    if hasattr(value, "to_dict"):
        return value.to_dict()
    if isinstance(value, dict):
        return {key: as_jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [as_jsonable(item) for item in value]
    return value


def print_json(value: Any) -> None:
    print(json.dumps(as_jsonable(value), ensure_ascii=False, indent=2))


def parse_memory_types(raw: str | None) -> list[str]:
    if not raw:
        return DEFAULT_MEMORY_TYPES
    return [item.strip() for item in raw.split(",") if item.strip()]


def cmd_self_test(args: argparse.Namespace) -> int:
    load_sdk()
    version = importlib.metadata.version("everos-cloud")
    payload: dict[str, Any] = {
        "everos_cloud_installed": True,
        "everos_cloud_version": version,
        "api_key_present": bool(read_env("EVEROS_API_KEY")),
        "default_user_id": read_env("EVEROS_USER_ID") or DEFAULT_USER_ID,
        "default_session_id": read_env("EVEROS_SESSION_ID") or DEFAULT_SESSION_ID,
    }

    if args.live:
        client = make_client()
        response = client.v1.memories.search(
            filters={"user_id": resolve_user_id(args)},
            query="EverOS integration smoke test",
            method="hybrid",
            memory_types=DEFAULT_MEMORY_TYPES,
            top_k=1,
        )
        payload["live_search"] = as_jsonable(response)

    print_json(payload)
    return 0


def cmd_add(args: argparse.Namespace) -> int:
    client = make_client()
    kwargs: dict[str, Any] = {
        "user_id": resolve_user_id(args),
        "session_id": resolve_session_id(args),
        "messages": [
            {
                "role": args.role,
                "timestamp": args.timestamp or now_ms(),
                "content": read_text(args),
            }
        ],
    }
    if args.sync:
        kwargs["async_mode"] = False
    response = client.v1.memories.add(**kwargs)
    print_json(response)
    return 0


def cmd_add_file(args: argparse.Namespace) -> int:
    path = Path(args.file)
    if not path.exists():
        raise SystemExit(f"File not found: {path}")
    text = read_text(args)
    relative = path.as_posix()
    content = f"Knowledge base file import\npath: {relative}\n\n{text}"
    client = make_client()
    response = client.v1.memories.add(
        user_id=resolve_user_id(args),
        session_id=resolve_session_id(args),
        messages=[{"role": "user", "timestamp": args.timestamp or now_ms(), "content": content}],
        async_mode=False if args.sync else True,
    )
    print_json(response)
    return 0


def cmd_flush(args: argparse.Namespace) -> int:
    client = make_client()
    response = client.v1.memories.flush(
        user_id=resolve_user_id(args),
        session_id=resolve_session_id(args),
    )
    print_json(response)
    return 0


def cmd_search(args: argparse.Namespace) -> int:
    client = make_client()
    response = client.v1.memories.search(
        filters={"user_id": resolve_user_id(args)},
        query=args.query,
        method=args.method,
        memory_types=parse_memory_types(args.memory_types),
        top_k=args.top_k,
        include_original_data=args.include_original_data,
        timeout=args.timeout,
    )
    print_json(response)
    return 0


def cmd_get(args: argparse.Namespace) -> int:
    client = make_client()
    response = client.v1.memories.get(
        filters={"user_id": resolve_user_id(args)},
        memory_type=args.memory_type,
        page=args.page,
        page_size=args.page_size,
    )
    print_json(response)
    return 0


def add_common_scope(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--user-id", help="EverOS user_id. Defaults to EVEROS_USER_ID or project default.")
    parser.add_argument("--session-id", help="EverOS session_id. Defaults to EVEROS_SESSION_ID or project default.")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="EverOS Cloud helper for my second brain.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    self_test = subparsers.add_parser("self-test", help="Check SDK installation and optional live search.")
    add_common_scope(self_test)
    self_test.add_argument("--live", action="store_true", help="Run a live EverOS search.")
    self_test.set_defaults(func=cmd_self_test)

    add = subparsers.add_parser("add", help="Add one personal memory message.")
    add_common_scope(add)
    add.add_argument("--role", choices=["user", "assistant"], default="user")
    add.add_argument("--content")
    add.add_argument("--file")
    add.add_argument("--encoding", default="utf-8")
    add.add_argument("--max-chars", type=int, default=12000)
    add.add_argument("--timestamp", type=int)
    add.add_argument("--sync", action="store_true", help="Use synchronous processing.")
    add.set_defaults(func=cmd_add)

    add_file = subparsers.add_parser("add-file", help="Add a project file as a memory message.")
    add_common_scope(add_file)
    add_file.add_argument("file")
    add_file.add_argument("--encoding", default="utf-8")
    add_file.add_argument("--max-chars", type=int, default=12000)
    add_file.add_argument("--timestamp", type=int)
    add_file.add_argument("--sync", action="store_true", help="Use synchronous processing.")
    add_file.set_defaults(func=cmd_add_file)

    flush = subparsers.add_parser("flush", help="Trigger memory extraction for the current session.")
    add_common_scope(flush)
    flush.set_defaults(func=cmd_flush)

    search = subparsers.add_parser("search", help="Search personal memories.")
    add_common_scope(search)
    search.add_argument("query")
    search.add_argument("--method", choices=["keyword", "vector", "hybrid", "agentic"], default="hybrid")
    search.add_argument("--memory-types", help="Comma-separated list. Default: episodic_memory,profile.")
    search.add_argument("--top-k", type=int, default=5)
    search.add_argument("--timeout", type=float, default=60.0)
    search.add_argument("--include-original-data", action="store_true")
    search.set_defaults(func=cmd_search)

    get = subparsers.add_parser("get", help="Get structured memories.")
    add_common_scope(get)
    get.add_argument("--memory-type", choices=["episodic_memory", "profile", "agent_case", "agent_skill"], default="profile")
    get.add_argument("--page", type=int, default=1)
    get.add_argument("--page-size", type=int, default=10)
    get.set_defaults(func=cmd_get)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python
"""Thin HTTP bridge for a local EverOS OSS server.

This targets the local OSS API shape documented at /api/v1/memory/*.
It is intentionally separate from tools/everos_memory.py, which targets
EverOS Cloud and /api/v1/memories/*.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


DEFAULT_BASE_URL = "http://127.0.0.1:8000"
DEFAULT_APP_ID = "second-brain"
DEFAULT_PROJECT_ID = "my-second-brain"
DEFAULT_SESSION_ID = "my-second-brain"
DEFAULT_USER_ID = "my-second-brain-owner"
DEFAULT_AGENT_ID = "codex"


def now_ms() -> int:
    return int(time.time() * 1000)


def normalize_base_url(raw: str) -> str:
    return raw.rstrip("/")


def default_base_url() -> str:
    return normalize_base_url(os.getenv("EVEROS_LOCAL_BASE_URL", DEFAULT_BASE_URL))


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


def post_json(base_url: str, path: str, payload: dict[str, Any], timeout: float) -> dict[str, Any]:
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    request = urllib.request.Request(
        f"{normalize_base_url(base_url)}{path}",
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise SystemExit(f"EverOS HTTP {exc.code}: {body}") from exc
    except urllib.error.URLError as exc:
        raise SystemExit(f"EverOS local server is unreachable at {base_url}: {exc.reason}") from exc


def get_json(base_url: str, path: str, timeout: float) -> dict[str, Any]:
    request = urllib.request.Request(f"{normalize_base_url(base_url)}{path}", method="GET")
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise SystemExit(f"EverOS HTTP {exc.code}: {body}") from exc
    except urllib.error.URLError as exc:
        raise SystemExit(f"EverOS local server is unreachable at {base_url}: {exc.reason}") from exc


def try_get_json(base_url: str, path: str, timeout: float) -> tuple[dict[str, Any] | None, str | None]:
    try:
        return get_json(base_url, path, timeout), None
    except SystemExit as exc:
        return None, str(exc)


def openapi_has_memory_api(openapi: dict[str, Any] | None) -> bool:
    if not openapi:
        return False
    paths = openapi.get("paths")
    if not isinstance(paths, dict):
        return False
    required = {
        "/api/v1/memory/add",
        "/api/v1/memory/flush",
        "/api/v1/memory/search",
    }
    return required.issubset(paths.keys())


def print_json(value: Any) -> None:
    print(json.dumps(value, ensure_ascii=False, indent=2))


def resolve_app_id(args: argparse.Namespace) -> str:
    return args.app_id or os.getenv("EVEROS_LOCAL_APP_ID") or DEFAULT_APP_ID


def resolve_project_id(args: argparse.Namespace) -> str:
    return args.project_id or os.getenv("EVEROS_LOCAL_PROJECT_ID") or DEFAULT_PROJECT_ID


def resolve_session_id(args: argparse.Namespace) -> str:
    return args.session_id or os.getenv("EVEROS_LOCAL_SESSION_ID") or DEFAULT_SESSION_ID


def resolve_user_id(args: argparse.Namespace) -> str:
    return args.user_id or os.getenv("EVEROS_LOCAL_USER_ID") or DEFAULT_USER_ID


def resolve_agent_id(args: argparse.Namespace) -> str:
    return args.agent_id or os.getenv("EVEROS_LOCAL_AGENT_ID") or DEFAULT_AGENT_ID


def message_sender_id(args: argparse.Namespace) -> str:
    if args.sender_id:
        return args.sender_id
    if args.role == "assistant":
        return resolve_agent_id(args)
    return resolve_user_id(args)


def build_add_payload(args: argparse.Namespace, content: str) -> dict[str, Any]:
    return {
        "session_id": resolve_session_id(args),
        "app_id": resolve_app_id(args),
        "project_id": resolve_project_id(args),
        "messages": [
            {
                "sender_id": message_sender_id(args),
                "role": args.role,
                "timestamp": args.timestamp or now_ms(),
                "content": content,
            }
        ],
    }


def build_flush_payload(args: argparse.Namespace) -> dict[str, Any]:
    return {
        "session_id": resolve_session_id(args),
        "app_id": resolve_app_id(args),
        "project_id": resolve_project_id(args),
    }


def build_search_payload(args: argparse.Namespace) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "app_id": resolve_app_id(args),
        "project_id": resolve_project_id(args),
        "query": args.query,
        "method": args.method,
        "top_k": args.top_k,
        "include_profile": args.include_profile,
    }
    if args.agent:
        payload["agent_id"] = resolve_agent_id(args)
    else:
        payload["user_id"] = resolve_user_id(args)
    if args.radius is not None:
        payload["radius"] = args.radius
    if args.min_score is not None:
        payload["min_score"] = args.min_score
    return payload


def cmd_health(args: argparse.Namespace) -> int:
    base_url = normalize_base_url(args.base_url)
    health_payload, health_error = try_get_json(base_url, "/health", args.timeout)
    openapi_payload, openapi_error = try_get_json(base_url, "/openapi.json", args.timeout)
    if health_payload is not None:
        has_memory_api = openapi_has_memory_api(openapi_payload)
        output: dict[str, Any] = {
            "reachable": True,
            "base_url": base_url,
            "everos_memory_api": has_memory_api,
            "health": health_payload,
        }
        if openapi_payload:
            output["openapi_title"] = openapi_payload.get("info", {}).get("title")
        if openapi_error:
            output["openapi_error"] = openapi_error
        print_json(output)
        if args.require_memory_api and not has_memory_api:
            return 2
        return 0

    if health_error:
        if args.soft:
            print_json({"reachable": False, "base_url": base_url, "error": health_error})
            return 0
        raise SystemExit(health_error)
    raise SystemExit(f"EverOS local server is unreachable at {base_url}")


def cmd_add(args: argparse.Namespace) -> int:
    payload = build_add_payload(args, read_text(args))
    response = post_json(normalize_base_url(args.base_url), "/api/v1/memory/add", payload, args.timeout)
    print_json(response)
    return 0


def cmd_flush(args: argparse.Namespace) -> int:
    response = post_json(
        normalize_base_url(args.base_url),
        "/api/v1/memory/flush",
        build_flush_payload(args),
        args.timeout,
    )
    print_json(response)
    return 0


def cmd_search(args: argparse.Namespace) -> int:
    response = post_json(
        normalize_base_url(args.base_url),
        "/api/v1/memory/search",
        build_search_payload(args),
        args.timeout,
    )
    print_json(response)
    return 0


def add_common_scope(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--base-url", default=default_base_url())
    parser.add_argument("--app-id")
    parser.add_argument("--project-id")
    parser.add_argument("--session-id")
    parser.add_argument("--user-id")
    parser.add_argument("--agent-id")
    parser.add_argument("--timeout", type=float, default=10.0)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="EverOS OSS local HTTP bridge for my second brain.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    health = subparsers.add_parser("health", help="Check local EverOS server health.")
    add_common_scope(health)
    health.add_argument("--soft", action="store_true", help="Return success with reachable=false if offline.")
    health.add_argument("--require-memory-api", action="store_true", help="Return exit code 2 unless /api/v1/memory/* routes exist.")
    health.set_defaults(func=cmd_health)

    add = subparsers.add_parser("add", help="POST one message to /api/v1/memory/add.")
    add_common_scope(add)
    add.add_argument("--role", choices=["user", "assistant", "tool"], default="user")
    add.add_argument("--sender-id")
    add.add_argument("--content")
    add.add_argument("--file")
    add.add_argument("--encoding", default="utf-8")
    add.add_argument("--max-chars", type=int, default=12000)
    add.add_argument("--timestamp", type=int)
    add.set_defaults(func=cmd_add)

    flush = subparsers.add_parser("flush", help="POST /api/v1/memory/flush for the session.")
    add_common_scope(flush)
    flush.set_defaults(func=cmd_flush)

    search = subparsers.add_parser("search", help="POST /api/v1/memory/search.")
    add_common_scope(search)
    search.add_argument("query")
    search.add_argument("--agent", action="store_true", help="Search agent memory using agent_id.")
    search.add_argument("--method", choices=["keyword", "vector", "hybrid", "agentic"], default="hybrid")
    search.add_argument("--top-k", type=int, default=5)
    search.add_argument("--include-profile", action="store_true")
    search.add_argument("--radius", type=float)
    search.add_argument("--min-score", type=float)
    search.set_defaults(func=cmd_search)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())

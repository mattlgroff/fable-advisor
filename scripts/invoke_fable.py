#!/usr/bin/env python3
"""Invoke Claude Fable 5 through Claude Code and save the result as Markdown."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess
import sys
from uuid import uuid4


MODEL = "claude-fable-5"
EFFORT = "high"


def claude_command(arguments: list[str]) -> list[str]:
    return ["claude", *arguments]


def require_subscription_auth() -> None:
    try:
        completed = subprocess.run(
            claude_command(["auth", "status"]),
            capture_output=True,
            text=True,
            check=False,
        )
    except FileNotFoundError as exc:
        raise RuntimeError(
            "Claude Code was not found on PATH. Install Claude Code in this environment first."
        ) from exc

    if completed.returncode != 0:
        raise RuntimeError("Unable to read Claude authentication status. Run `claude auth login`.")

    try:
        status = json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError("Claude returned an unreadable authentication status.") from exc

    if not status.get("loggedIn") or status.get("authMethod") != "claude.ai":
        raise RuntimeError(
            "Claude subscription authentication is not active. Run `claude auth login`. "
            "API-key authentication is intentionally rejected."
        )


def read_prompt(args: argparse.Namespace) -> str:
    if args.prompt_file:
        return Path(args.prompt_file).read_text(encoding="utf-8")
    if args.prompt is not None:
        return args.prompt
    if not sys.stdin.isatty():
        return sys.stdin.read()
    raise RuntimeError("Provide --prompt-file, --prompt, or prompt text on stdin.")


def default_output(session_id: str) -> Path:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return Path.cwd() / ".fable-advisor" / f"{stamp}-{session_id}.md"


def write_metadata(path: Path, data: dict[str, object]) -> None:
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run a high-effort Fable consultation and save its response as Markdown."
    )
    parser.add_argument("--prompt-file", help="UTF-8 Markdown or text prompt file")
    parser.add_argument("--prompt", help="Prompt text; prefer --prompt-file for long material")
    parser.add_argument("--output", help="Markdown output path")
    parser.add_argument("--resume", metavar="SESSION_ID", help="Resume a prior Claude session")
    parser.add_argument(
        "--auth-check-only",
        action="store_true",
        help="Verify subscription authentication without invoking a model",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate inputs and print paths without invoking a model",
    )
    args = parser.parse_args()

    require_subscription_auth()
    if args.auth_check_only:
        print("Claude subscription authentication confirmed.")
        return 0

    prompt = read_prompt(args)
    if not prompt.strip():
        raise RuntimeError("The consultation prompt is empty.")

    session_id = args.resume or str(uuid4())
    output_path = Path(args.output).resolve() if args.output else default_output(session_id).resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    log_path = output_path.with_suffix(output_path.suffix + ".stderr.log")
    metadata_path = output_path.with_suffix(output_path.suffix + ".metadata.json")

    metadata: dict[str, object] = {
        "session_id": session_id,
        "model": MODEL,
        "effort": EFFORT,
        "status": "dry-run" if args.dry_run else "running",
        "started_at": datetime.now(timezone.utc).isoformat(),
        "output_path": str(output_path),
        "log_path": str(log_path),
        "resumed": bool(args.resume),
    }
    write_metadata(metadata_path, metadata)

    common = [
        "-p",
        "--model",
        MODEL,
        "--effort",
        EFFORT,
        "--input-format",
        "text",
        "--output-format",
        "text",
        "--no-chrome",
        "--safe-mode",
        "--tools",
        "",
    ]
    if args.resume:
        common.extend(["--resume", session_id])
    else:
        common.extend(["--session-id", session_id])

    if args.dry_run:
        print(f"Session: {session_id}")
        print(f"Markdown: {output_path}")
        print(f"Log: {log_path}")
        print("Dry run complete. Fable was not invoked.")
        return 0

    print(f"Starting Fable advisor session {session_id}.", file=sys.stderr, flush=True)
    print("No timeout is imposed. Waiting until Claude exits or the user cancels.", file=sys.stderr, flush=True)

    try:
        with output_path.open("w", encoding="utf-8", newline="\n") as output_file, log_path.open(
            "w", encoding="utf-8", newline="\n"
        ) as log_file:
            completed = subprocess.run(
                claude_command(common),
                input=prompt,
                stdout=output_file,
                stderr=log_file,
                text=True,
                check=False,
            )
    except KeyboardInterrupt:
        metadata["status"] = "cancelled"
        metadata["finished_at"] = datetime.now(timezone.utc).isoformat()
        write_metadata(metadata_path, metadata)
        print("Consultation cancelled by user. The Claude session may be resumable.", file=sys.stderr)
        return 130

    metadata["exit_code"] = completed.returncode
    metadata["finished_at"] = datetime.now(timezone.utc).isoformat()
    metadata["status"] = "completed" if completed.returncode == 0 else "failed"
    write_metadata(metadata_path, metadata)

    if completed.returncode != 0:
        print(f"Claude exited with code {completed.returncode}.", file=sys.stderr)
        print(f"Session: {session_id}", file=sys.stderr)
        print(f"Partial Markdown: {output_path}", file=sys.stderr)
        print(f"Log: {log_path}", file=sys.stderr)
        return completed.returncode

    print(f"Session: {session_id}")
    print(f"Markdown: {output_path}")
    print(f"Log: {log_path}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except RuntimeError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        raise SystemExit(2)

#!/usr/bin/env python3
"""wsum - summarize git diffs into markdown for do.md work summary sections.

This module can be imported and called via summarize_work(), and can also be run
as a command.
"""

from __future__ import annotations

import argparse
import datetime
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from typing import Iterable


SUMMARY_PROMPT_TEMPLATE = (
    "You are a technical writer. Summarize the git diff from stdin into a concise, "
    "human-readable work summary. Focus on what changed and why it matters, not raw diff "
    "mechanics. Use plain prose (no bullets unless there are clearly distinct work "
    "streams). Be specific about file names and functionality. Keep the summary to 3-6 "
    "sentences. Return only the summary text."
)

# Allow-list for optional diff passthrough arguments.
ALLOWED_EXTRA_DIFF_ARGS = {
    "--name-only",
    "--name-status",
    "--stat",
    "--numstat",
    "--minimal",
    "--relative",
    "--ignore-space-at-eol",
    "--ignore-space-change",
    "-b",
    "--ignore-all-space",
    "-w",
    "--ignore-blank-lines",
}

ALLOWED_PREFIXES = (
    "--unified=",
    "-U",
)


class WsumError(RuntimeError):
    """Raised for user-facing runtime errors in wsum."""


@dataclass(frozen=True)
class WorkSummaryResult:
    """Structured result returned by summarize_work."""

    timestamp: str
    headline: str
    summary: str
    markdown: str


def build_summary_prompt(max_sentences: int = 6) -> str:
    """Build the model prompt string."""
    if max_sentences < 1:
        raise ValueError("max_sentences must be >= 1")
    return SUMMARY_PROMPT_TEMPLATE.replace("3-6", f"3-{max_sentences}")


def headline_from_summary(summary: str, max_len: int = 120) -> str:
    """Create a one-line headline from summary text."""
    flat = " ".join(summary.strip().split())
    if not flat:
        return "No material changes detected"

    sentence_end = re.search(r"[.!?]", flat)
    if sentence_end:
        candidate = flat[: sentence_end.start()].strip()
    else:
        candidate = flat

    if not candidate:
        candidate = flat

    if len(candidate) <= max_len:
        return candidate

    truncated = candidate[: max_len - 1].rstrip()
    if " " in truncated:
        truncated = truncated.rsplit(" ", 1)[0]
    return f"{truncated}."


def render_markdown(timestamp: str, headline: str, summary: str) -> str:
    """Render a do.md-compatible work summary markdown block."""
    return (
        "# work summary\n\n"
        f"## {timestamp}\n\n"
        "---\n"
        f"workHeadline: {headline}\n"
        "---\n\n"
        f"{summary.strip()}\n"
    )


def find_repo_root() -> str:
    """Return git repository root path."""
    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise WsumError("Error: not inside a git repository.")
    return result.stdout.strip()


def _validate_extra_diff_args(extra_diff_args: Iterable[str] | None) -> list[str]:
    """Validate optional extra diff arguments against a constrained allow-list."""
    if not extra_diff_args:
        return []

    validated: list[str] = []
    for arg in extra_diff_args:
        if arg in ALLOWED_EXTRA_DIFF_ARGS or arg.startswith(ALLOWED_PREFIXES):
            validated.append(arg)
            continue
        raise WsumError(
            "Error: unsupported extra diff argument "
            f"'{arg}'. Allowed arguments are constrained by wsum."
        )
    return validated


def collect_diff(
    *,
    repo_root: str,
    staged_only: bool = True,
    base_ref: str = "HEAD",
    include_unstaged: bool = False,
    file_paths: list[str] | None = None,
    extra_diff_args: list[str] | None = None,
) -> str:
    """Collect a git diff according to requested selection options."""
    validated_extra = _validate_extra_diff_args(extra_diff_args)

    cmd = ["git", "diff"]
    if staged_only and not include_unstaged:
        cmd.append("--cached")

    if validated_extra:
        cmd.extend(validated_extra)

    if base_ref:
        cmd.append(base_ref)

    if file_paths:
        cmd.append("--")
        cmd.extend(file_paths)

    result = subprocess.run(cmd, capture_output=True, text=True, cwd=repo_root)
    if result.returncode != 0:
        stderr = result.stderr.strip() or "unknown git diff error"
        raise WsumError(f"Error running git diff: {stderr}")
    return result.stdout.strip()


def run_gemini(diff_text: str, *, model: str | None = None, max_sentences: int = 6) -> str:
    """Run Gemini CLI against diff text and return summary text."""
    prompt = build_summary_prompt(max_sentences=max_sentences)
    cmd = ["gemini", "-p", prompt]
    if model:
        cmd.extend(["-m", model])

    env = os.environ.copy()
    if not env.get("GEMINI_API_KEY") and env.get("GOOGLE_API_KEY"):
        env["GEMINI_API_KEY"] = env["GOOGLE_API_KEY"]

    try:
        result = subprocess.run(
            cmd,
            input=diff_text,
            capture_output=True,
            text=True,
            env=env,
        )
    except FileNotFoundError as exc:
        raise WsumError(
            "Error: gemini CLI not found in PATH. Install Gemini CLI first."
        ) from exc

    if result.returncode != 0:
        stderr = result.stderr.strip()
        if stderr:
            raise WsumError(f"Error: gemini CLI failed: {stderr}")
        raise WsumError("Error: gemini CLI failed to generate summary.")

    summary = result.stdout.strip()
    if not summary:
        raise WsumError("Error: gemini CLI returned an empty summary.")
    return summary


def summarize_work(
    *,
    diff_text: str | None = None,
    staged_only: bool = True,
    base_ref: str = "HEAD",
    include_unstaged: bool = False,
    file_paths: list[str] | None = None,
    extra_diff_args: list[str] | None = None,
    model: str | None = None,
    max_sentences: int = 6,
) -> WorkSummaryResult:
    """Produce a structured work summary and markdown output."""
    if diff_text is None:
        repo_root = find_repo_root()
        diff_text = collect_diff(
            repo_root=repo_root,
            staged_only=staged_only,
            base_ref=base_ref,
            include_unstaged=include_unstaged,
            file_paths=file_paths,
            extra_diff_args=extra_diff_args,
        )

    if not diff_text.strip():
        raise WsumError("No changes found in diff. Nothing to summarize.")

    summary = run_gemini(diff_text, model=model, max_sentences=max_sentences)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    headline = headline_from_summary(summary)
    markdown = render_markdown(timestamp, headline, summary)

    return WorkSummaryResult(
        timestamp=timestamp,
        headline=headline,
        summary=summary,
        markdown=markdown,
    )


def _read_stdin_if_available(force_stdin: bool) -> str | None:
    """Read stdin only when explicitly requested or when piped input is present."""
    if force_stdin:
        return sys.stdin.read()
    if not sys.stdin.isatty():
        return sys.stdin.read()
    return None


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse command line options for wsum."""
    parser = argparse.ArgumentParser(
        prog="wsum",
        description="Summarize git diff changes into work-summary markdown",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Include staged and unstaged changes (dtask --all semantics)",
    )
    parser.add_argument(
        "--base",
        default="HEAD",
        metavar="REF",
        help="Compare against a base ref (default: HEAD)",
    )
    parser.add_argument(
        "--model",
        metavar="MODEL",
        help="Gemini model name to use (example: gemini-2.5-pro)",
    )
    parser.add_argument(
        "--max-sentences",
        type=int,
        default=6,
        help="Upper bound for sentence count guidance in the prompt (default: 6)",
    )
    parser.add_argument(
        "--stdin",
        action="store_true",
        help="Read diff from stdin even if stdin is a TTY",
    )
    parser.add_argument(
        "--file",
        action="append",
        dest="file_paths",
        help="Limit diff to a specific path (repeatable)",
    )
    parser.add_argument(
        "--extra-diff-arg",
        action="append",
        default=[],
        help="Additional validated git diff option (repeatable)",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Command entrypoint."""
    args = parse_args(argv)

    stdin_diff = _read_stdin_if_available(force_stdin=args.stdin)
    try:
        result = summarize_work(
            diff_text=stdin_diff,
            staged_only=not args.all,
            base_ref=args.base,
            include_unstaged=args.all,
            file_paths=args.file_paths,
            extra_diff_args=args.extra_diff_arg,
            model=args.model,
            max_sentences=args.max_sentences,
        )
    except WsumError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print(result.markdown.rstrip())
    return 0


if __name__ == "__main__":
    sys.exit(main())

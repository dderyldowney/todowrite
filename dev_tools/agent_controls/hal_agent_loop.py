#!/usr/bin/env python3
"""
Hal Agent Loop - v2: local-filter-first + token guard + delta mode.

What's new:
- Token/char gate before API call (hard stop if over budget).
- Delta-aware prompts: if local snippet unchanged, we send a tiny "no
  changes" marker.
- Small, directive system prompt to save tokens.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
from dataclasses import dataclass

# OpenAI and Anthropic imports moved to top-level
try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

try:
    import anthropic
except ImportError:
    anthropic = None
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Sequence

# Removed circular import - function will be implemented locally

# ---------- Repository Filtering -------------------------------------------


def _get_cached_result(hash_input: str, delta_mode: bool) -> str | None:
    """Get cached result if available."""
    if not delta_mode:
        return None

    hash_digest = hashlib.md5(hash_input.encode(), usedforsecurity=False).hexdigest()
    cache_file = Path.home() / ".hal_cache" / f"{hash_digest}.txt"

    if cache_file.exists():
        try:
            cached_result = cache_file.read_text()
            if cached_result:
                return f"[CACHED] {cached_result}"
        except (OSError, UnicodeDecodeError):
            pass
    return None


def _build_ripgrep_cmd(
    pattern: str | None,
    context_lines: int,
    per_file_max_lines: int,
    max_file_size: int,
    include_globs: list[str] | None,
    exclude_globs: list[str] | None,
) -> list[str]:
    """Build ripgrep command with all options."""
    cmd = [
        "rg",
        "-n",
        "--max-count",
        str(per_file_max_lines),
        "-A",
        str(context_lines),
        "-B",
        str(context_lines),
        pattern or ".",
        "--type",
        "py",
    ]

    cmd.extend(["--max-filesize", str(max_file_size)])

    if include_globs:
        for glob in include_globs:
            cmd.extend(["--glob", glob])
    if exclude_globs:
        for glob in exclude_globs:
            cmd.extend(["--glob", f"!{glob}"])

    return cmd


def _process_line(
    line: str,
    json_filter: str | None,
    abbreviate_paths: bool,
) -> str | None:
    """Process a single line of output."""
    if not line.strip():
        return None

    # Apply JSON filtering if specified
    if json_filter and "{" in line and "}" in line:
        try:
            json_data = json.loads(
                line[line.find("{") : line.rfind("}") + 1],
            )
            if json_filter not in str(json_data):
                return None
        except (json.JSONDecodeError, ValueError):
            pass

    # Abbreviate paths if requested
    if abbreviate_paths and ":" in line:
        parts = line.split(":", 1)
        if len(parts) == 2:
            path = parts[0]
            path_parts = path.split("/")
            if len(path_parts) > 3:
                path = "/".join(["...", *path_parts[-2:]])
            return f"{path}:{parts[1]}"

    return line


def _should_stop_processing(
    max_files: int,
    max_hits: int,
    max_bytes: int,
    files_processed: int,
    hits_found: int,
    total_bytes: int,
) -> bool:
    """Check if processing should stop based on limits."""
    return (
        (max_files > 0 and files_processed >= max_files)
        or (max_hits > 0 and hits_found >= max_hits)
        or (total_bytes >= max_bytes)
    )


def _cache_result(hash_input: str, output: str) -> None:
    """Cache the result for delta mode."""
    try:
        hash_digest = hashlib.md5(hash_input.encode(), usedforsecurity=False).hexdigest()
        cache_file = Path.home() / ".hal_cache" / f"{hash_digest}.txt"
        cache_file.parent.mkdir(parents=True, exist_ok=True)
        cache_file.write_text(output)
    except (OSError, json.JSONDecodeError):
        pass


def _process_search_results(
    lines: list[str],
    max_files: int,
    max_hits: int,
    max_bytes: int,
    json_filter: str | None,
    abbreviate_paths: bool,
    llm_snippet_chars: int,
) -> tuple[str, int, int, int]:
    """Process search results and format output."""
    files_processed = 0
    total_bytes = 0
    hits_found = 0
    result_lines = []

    for line in lines:
        # Check limits early
        if _should_stop_processing(max_files, max_hits, max_bytes, files_processed, hits_found, total_bytes):
            break

        # Process individual line
        processed_line = _process_line(line, json_filter, abbreviate_paths)
        if processed_line is None:
            continue

        result_lines.append(processed_line)
        total_bytes += len(line.encode("utf-8"))
        hits_found += 1

        if ":" in processed_line:
            files_processed += 1

    # Format output
    output = "\n".join(result_lines)
    if len(output) > llm_snippet_chars:
        output = output[:llm_snippet_chars] + "\n...[truncated]"

    return output, files_processed, hits_found, total_bytes


def _try_ripgrep_search(
    pattern: str | None,
    context_lines: int,
    per_file_max_lines: int,
    max_file_size: int,
    include_globs: list[str] | None,
    exclude_globs: list[str] | None,
    max_files: int,
    max_hits: int,
    max_bytes: int,
    json_filter: str | None,
    abbreviate_paths: bool,
    llm_snippet_chars: int,
    roots: list[str],
) -> str | None:
    """Try ripgrep search first."""
    cmd = _build_ripgrep_cmd(
        pattern,
        context_lines,
        per_file_max_lines,
        max_file_size,
        include_globs,
        exclude_globs,
    )

    result = subprocess.run(cmd, check=False, capture_output=True, text=True, cwd=roots[0])

    if result.returncode == 0:
        lines = result.stdout.split("\n")
        output, _, _, _ = _process_search_results(
            lines, max_files, max_hits, max_bytes, json_filter, abbreviate_paths, llm_snippet_chars
        )
        return output
    return None


def _try_grep_search(
    pattern: str | None,
    context_lines: int,
    max_files: int,
    max_hits: int,
    max_bytes: int,
    llm_snippet_chars: int,
    roots: list[str],
) -> str | None:
    """Try grep search as fallback."""
    cmd = [
        "grep",
        "-r",
        "-n",
        "-A",
        str(context_lines),
        "-B",
        str(context_lines),
        pattern or ".",
        "--include=*.py",
    ]

    result = subprocess.run(cmd, check=False, capture_output=True, text=True, cwd=roots[0])

    if result.returncode == 0:
        lines = result.stdout.split("\n")
        files_processed = 0
        total_bytes = 0
        hits_found = 0
        result_lines = []

        for line in lines:
            if not line.strip():
                continue

            # Apply limits
            if max_files > 0 and files_processed >= max_files:
                break
            if max_hits > 0 and hits_found >= max_hits:
                break
            if total_bytes >= max_bytes:
                break

            result_lines.append(line)
            total_bytes += len(line.encode("utf-8"))
            hits_found += 1

        output = "\n".join(result_lines)
        if len(output) > llm_snippet_chars:
            output = output[:llm_snippet_chars] + "\n...[truncated]"

        return output
    return None


def _format_fallback_message(
    goal: str,
    pattern: str | None,
    max_files: int,
    max_hits: int,
    max_bytes: int,
    delta_mode: bool,
) -> str:
    """Format fallback message when search tools aren't available."""
    info_parts = [
        "Repository filtering not available. Please install ripgrep or grep.",
        f"Goal: {goal}",
        f"Pattern: {pattern}",
        f"Max files: {max_files}",
        f"Max hits: {max_hits}",
        f"Max bytes: {max_bytes}",
        f"Delta mode: {delta_mode}",
    ]
    return "\n".join(info_parts)


def filter_repo_for_llm(
    goal: str,
    pattern: str | None = None,
    roots: list[str] | None = None,
    include_globs: list[str] | None = None,
    exclude_globs: list[str] | None = None,
    json_filter: str | None = None,
    max_files: int = 20000,
    max_hits: int = 5000,
    max_bytes: int = 256000,
    llm_snippet_chars: int = 3200,
    context_lines: int = 1,
    per_file_max_lines: int = 60,
    abbreviate_paths: bool = True,
    delta_mode: bool = False,
) -> str:
    """
    Filter repository content for LLM consumption with token efficiency.

    This function searches through files and returns a compact snippet
    optimized for LLM context windows with comprehensive filtering options.
    """
    roots = roots or ["."]
    hash_input = f"{goal}_{pattern}_{roots!s}"

    # Check cache first
    cached = _get_cached_result(hash_input, delta_mode)
    if cached:
        return cached

    # Calculate max file size
    if max_files > 0:
        max_file_size = min(max(1024 * 1024, max_bytes // max_files), 10 * 1024 * 1024)
    else:
        max_file_size = 1024 * 1024

    # Try ripgrep search first
    try:
        output = _try_ripgrep_search(
            pattern, context_lines, per_file_max_lines, max_file_size,
            include_globs, exclude_globs, max_files, max_hits, max_bytes,
            json_filter, abbreviate_paths, llm_snippet_chars, roots
        )
        if output is not None:
            if delta_mode:
                _cache_result(hash_input, output)
            return output if output else f"No matches found for pattern: {pattern}"

    except FileNotFoundError:
        pass

    # Try grep search as fallback
    try:
        output = _try_grep_search(
            pattern, context_lines, max_files, max_hits, max_bytes, llm_snippet_chars, roots
        )
        if output is not None:
            return output if output else f"No matches found for pattern: {pattern}"

    except FileNotFoundError:
        pass

    # Final fallback with parameter information
    return _format_fallback_message(goal, pattern, max_files, max_hits, max_bytes, delta_mode)


# ---------- Providers -------------------------------------------------------


class LLMProvider:
    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        model: str,
        max_tokens: int = 800,
    ) -> str:
        raise NotImplementedError


@dataclass
class OpenAIProvider(LLMProvider):
    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        model: str,
        max_tokens: int = 800,
    ) -> str:
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            msg = "OPENAI_API_KEY is not set"
            raise RuntimeError(msg)
        client = OpenAI(api_key=api_key)
        resp = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            max_tokens=max_tokens,
        )
        return resp.choices[0].message.content or ""


@dataclass
class AnthropicProvider(LLMProvider):
    anthropic_version: str = "2023-06-01"

    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        model: str,
        max_tokens: int = 800,
    ) -> str:
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            msg = "ANTHROPIC_API_KEY is not set"
            raise RuntimeError(msg)
        client = anthropic.Anthropic(api_key=api_key)
        msg = client.messages.create(
            model=model,
            max_tokens=max_tokens,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}],
        )
        parts: list[str] = []
        for block in msg.content:
            if getattr(block, "type", None) == "text":
                parts.append(block.text)
        return "\n".join(parts).strip()


# ---------- Prompts ---------------------------------------------------------

# Short+directive system prompt (token-cheap)
BASE_SYSTEM_PROMPT = (
    "You are Hal, a terse, precise coding assistant. "
    "Prefer the given snippet. "
    "Answer in short steps. If uncertain, state assumptions briefly."
)


def build_user_prompt(user_goal: str, local_snippet: str) -> str:
    # Keep this extremely compact; structure helps the model
    # with minimal tokens.
    return (
        f"Goal: {user_goal}\n"
        "Context:\n"
        f"{local_snippet}\n"
        "Instruction: Use the context first. "
        "Return only the next steps, code, or diffs."
    )


# ---------- Guards ----------------------------------------------------------


def _enforce_char_budget(text: str, max_chars: int) -> None:
    if len(text) > max_chars:
        msg = (
            f"Prompt too large ({len(text)} chars > {max_chars}). "
            f"Increase --chars or refine filters."
        )
        raise ValueError(
            msg,
        )


# ---------- Main ------------------------------------------------------------


def should_run_local_tools(pattern: str | None, jq_filter: str | None) -> bool:
    return bool(pattern or jq_filter)


def main(argv: Sequence[str] | None = None) -> int:
    pa = argparse.ArgumentParser(
        description="Hal Agent: token-minimized loop (v2).",
    )
    pa.add_argument(
        "--provider",
        choices=["openai", "anthropic"],
        required=True,
    )
    pa.add_argument("--model", required=True)
    pa.add_argument("--goal", required=True)
    pa.add_argument("--pattern")
    pa.add_argument("--jq", dest="jq_filter")
    pa.add_argument("--roots", nargs="+", default=["."])
    pa.add_argument("--include", nargs="+", dest="include_globs")
    pa.add_argument("--exclude", nargs="+", dest="exclude_globs")
    pa.add_argument(
        "--chars",
        type=int,
        default=3200,
        help="Max snippet size (characters).",
    )
    pa.add_argument("--max-files", type=int, default=20000)
    pa.add_argument("--max-hits", type=int, default=5000)
    pa.add_argument("--max-bytes", type=int, default=256000)
    pa.add_argument("--context", type=int, default=1)
    pa.add_argument("--per-file", type=int, default=60)
    pa.add_argument("--delta", action="store_true")
    pa.add_argument("--max-tokens", type=int, default=600)
    args = pa.parse_args(argv)

    snippet = ""
    if should_run_local_tools(args.pattern, args.jq_filter):
        snippet = filter_repo_for_llm(
            goal=args.goal,
            pattern=args.pattern,
            roots=args.roots,
            include_globs=args.include_globs,
            exclude_globs=args.exclude_globs,
            json_filter=args.jq_filter,
            max_files=args.max_files,
            max_hits=args.max_hits,
            max_bytes=args.max_bytes,
            llm_snippet_chars=args.chars,
            context_lines=args.context,
            per_file_max_lines=args.per_file,
            abbreviate_paths=True,
            delta_mode=args.delta,
        )

    user_prompt = build_user_prompt(args.goal, snippet)

    # hard prompt size guard (prevents surprise token burn)
    _enforce_char_budget(
        user_prompt,
        max_chars=args.chars + 800,
    )  # allow small overhead

    provider: LLMProvider = OpenAIProvider() if args.provider == "openai" else AnthropicProvider()
    out = provider.generate(
        system_prompt=BASE_SYSTEM_PROMPT,
        user_prompt=user_prompt,
        model=args.model,
        max_tokens=args.max_tokens,
    )
    sys.stdout.write(out.strip() + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

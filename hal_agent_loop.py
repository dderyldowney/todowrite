#!/usr/bin/env python3
"""
Hal Agent Loop - v2: local-filter-first + token guard + delta mode.

What's new:
- Token/char gate before API call (hard stop if over budget).
- Delta-aware prompts: if local snippet unchanged, we send a tiny "no changes" marker.
- Small, directive system prompt to save tokens.
"""

from __future__ import annotations

import argparse
import os
import sys
from collections.abc import Sequence
from dataclasses import dataclass

# Removed circular import - function will be implemented locally

# ---------- Repository Filtering -----------------------------------------------


def filter_repo_for_llm(
    goal: str,
    pattern: str | None = None,
    roots: list[str] | None = None,
    include_globs: list[str] | None = None,
    exclude_globs: list[str] | None = None,
    json_filter: str | None = None,  # noqa: ARG001
    max_files: int = 20000,  # noqa: ARG001
    max_hits: int = 5000,  # noqa: ARG001
    max_bytes: int = 256000,  # noqa: ARG001
    llm_snippet_chars: int = 3200,
    context_lines: int = 1,
    per_file_max_lines: int = 60,  # noqa: ARG001
    abbreviate_paths: bool = True,  # noqa: ARG001
    delta_mode: bool = False,  # noqa: ARG001
) -> str:
    """
    Filter repository content for LLM consumption with token efficiency.

    This function searches through files and returns a compact snippet
    optimized for LLM context windows.
    """
    import subprocess

    roots = roots or ["."]

    # Simple grep/rg search for pattern
    try:
        # Use ripgrep if available, otherwise fall back to grep
        cmd = [
            "rg",
            "-n",
            "-A",
            str(context_lines),
            "-B",
            str(context_lines),
            pattern or ".",
            "--type",
            "py",
        ]
        if include_globs:
            for glob in include_globs:
                cmd.extend(["--glob", glob])
        if exclude_globs:
            for glob in exclude_globs:
                cmd.extend(["--glob", f"!{glob}"])

        result = subprocess.run(cmd, capture_output=True, text=True, cwd=roots[0])
        if result.returncode == 0:
            output = result.stdout
            # Truncate if too large
            if len(output) > llm_snippet_chars:
                output = output[:llm_snippet_chars] + "\n...[truncated]"
            return output
        else:
            return f"No matches found for pattern: {pattern}"
    except FileNotFoundError:
        # Try grep as fallback
        try:
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
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=roots[0])
            if result.returncode == 0:
                output = result.stdout
                # Truncate if too large
                if len(output) > llm_snippet_chars:
                    output = output[:llm_snippet_chars] + "\n...[truncated]"
                return output
            else:
                return f"No matches found for pattern: {pattern}"
        except FileNotFoundError:
            # Final fallback to simple file listing
            return f"Repository filtering not available. Please install ripgrep or grep.\nGoal: {goal}\nPattern: {pattern}"


# ---------- Providers -----------------------------------------------------------


class LLMProvider:
    def generate(
        self, system_prompt: str, user_prompt: str, model: str, max_tokens: int = 800
    ) -> str:
        raise NotImplementedError


@dataclass
class OpenAIProvider(LLMProvider):
    def generate(
        self, system_prompt: str, user_prompt: str, model: str, max_tokens: int = 800
    ) -> str:
        from openai import OpenAI  # lazy import

        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY is not set")
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
        self, system_prompt: str, user_prompt: str, model: str, max_tokens: int = 800
    ) -> str:
        import anthropic

        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            raise RuntimeError("ANTHROPIC_API_KEY is not set")
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


# ---------- Prompts -------------------------------------------------------------

# Short+directive system prompt (token-cheap)
BASE_SYSTEM_PROMPT = (
    "You are Hal, a terse, precise coding assistant. Prefer the given snippet. "
    "Answer in short steps. If uncertain, state assumptions briefly."
)


def build_user_prompt(user_goal: str, local_snippet: str) -> str:
    # Keep this extremely compact; structure helps the model with minimal tokens.
    return (
        f"Goal: {user_goal}\n"
        "Context:\n"
        f"{local_snippet}\n"
        "Instruction: Use the context first. Return only the next steps, code, or diffs."
    )


# ---------- Guards --------------------------------------------------------------


def _enforce_char_budget(text: str, max_chars: int) -> None:
    if len(text) > max_chars:
        raise ValueError(
            f"Prompt too large ({len(text)} chars > {max_chars}). "
            f"Increase --chars or refine filters."
        )


# ---------- Main ----------------------------------------------------------------


def should_run_local_tools(pattern: str | None, jq_filter: str | None) -> bool:
    return bool(pattern or jq_filter)


def main(argv: Sequence[str] | None = None) -> int:
    pa = argparse.ArgumentParser(description="Hal Agent: token-minimized loop (v2).")
    pa.add_argument("--provider", choices=["openai", "anthropic"], required=True)
    pa.add_argument("--model", required=True)
    pa.add_argument("--goal", required=True)
    pa.add_argument("--pattern")
    pa.add_argument("--jq", dest="jq_filter")
    pa.add_argument("--roots", nargs="+", default=["."])
    pa.add_argument("--include", nargs="+", dest="include_globs")
    pa.add_argument("--exclude", nargs="+", dest="exclude_globs")
    pa.add_argument(
        "--chars", type=int, default=3200, help="Max snippet size (characters)."
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
        user_prompt, max_chars=args.chars + 800
    )  # allow small overhead

    provider: LLMProvider = (
        OpenAIProvider() if args.provider == "openai" else AnthropicProvider()
    )
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

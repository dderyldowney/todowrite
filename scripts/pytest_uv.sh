#!/usr/bin/env bash
# Wrapper to run pytest via `uv run pytest` so VS Code uses the `uv` runner.
# Preference order:
# 1) `uv` installed in the active virtualenv (`$VIRTUAL_ENV/bin/uv`)
# 2) `uv` available on PATH
# 3) `~/.local/bin/uv` as a common user install location

set -euo pipefail

# 1) If a virtualenv is active, prefer its uv
if [[ -n "${VIRTUAL_ENV:-}" ]]; then
	VENV_UV="${VIRTUAL_ENV}/bin/uv"
	if [[ -x "$VENV_UV" ]]; then
		exec "$VENV_UV" run pytest "$@"
	fi
fi

# 2) If uv is on PATH, use it
if command -v uv >/dev/null 2>&1; then
	exec uv run pytest "$@"
fi

# 3) Fallback to ~/.local/bin/uv
if [[ -x "$HOME/.local/bin/uv" ]]; then
	exec "$HOME/.local/bin/uv" run pytest "$@"
fi

echo "Error: 'uv' command not found. Install 'uv' in your venv or add it to PATH." >&2
exit 127

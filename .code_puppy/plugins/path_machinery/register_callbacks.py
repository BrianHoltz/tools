"""Sync os.environ["PATH"] with the user's real login-shell PATH.

Problem (confirmed live 2026.08.16, see relationship-shared kennel notes):
Code Puppy's `agent_run_shell_command` tool runs `subprocess.Popen(cmd,
shell=True)`, which spawns `/bin/sh` inheriting *Code Puppy's own process
env* — not a fresh interactive/login shell. Code Puppy itself gets launched
(GUI dock icon, launchd, etc.) with a minimal PATH like
`/usr/bin:/bin:/usr/sbin:/sbin`, so every single shell tool call is missing
Homebrew, nvm/node, and anything else the user's real shell config adds.
This is the exact failure mode `~/bin/docs/AgentRules.md` already warns
about ("Agent subshells ... may run in a non-login shell that does not
inherit the interactive PATH") — this plugin is the fix, not a workaround.

Fix: at plugin-load time (once per Code Puppy process), ask the user's
*actual* login shell what its PATH is. That shell sources ~/.zprofile /
~/.bash_profile, which in turn source Homebrew's `shellenv` and
~/src/tools/shellrc/* (the canonical cross-laptop PATH machinery — see
AgentRules.md § ~/bin structure). We don't need to know what's inside those
files; we just ask the shell that already knows.

The result is merged (never replaces) into os.environ["PATH"] so every
subsequent `subprocess.Popen(shell=True)` call for the rest of this Code
Puppy process — i.e. every `agent_run_shell_command` invocation — inherits
the full PATH automatically. No per-call prepending, no plugin hook on the
hot path, no added latency after the one-time startup cost.

This mirrors the existing sanctioned pattern in Code Puppy's own built-in
plugins (`plugins/dx_docs/auth.py`, `plugins/walmart_specific/bigquery_auth.py`),
which already patch os.environ["PATH"] at runtime for specific tools (MCP
CLI, gcloud). This plugin generalizes that to the whole PATH, once.
"""

from __future__ import annotations

import logging
import os
import subprocess
import sys

logger = logging.getLogger(__name__)

_START = "__CODEPUPPY_PATH_START__"
_END = "__CODEPUPPY_PATH_END__"


def _login_shell_path() -> str | None:
    """Ask the user's real login shell for its resolved PATH. None on failure."""
    if sys.platform.startswith("win"):
        return None  # Windows has no zsh/bash login-shell PATH concept here.

    shell = os.environ.get("SHELL", "/bin/zsh")
    try:
        result = subprocess.run(
            [shell, "-ilc", f"echo {_START}${{PATH}}{_END}"],
            capture_output=True,
            text=True,
            timeout=15,
        )
    except Exception as exc:  # never let a broken shell config crash Code Puppy
        logger.debug("path_machinery: could not query %s: %s", shell, exc)
        return None

    out = result.stdout or ""
    if _START not in out or _END not in out:
        logger.debug("path_machinery: markers not found in %s output", shell)
        return None
    return out.split(_START, 1)[1].split(_END, 1)[0].strip()


def _merge_path(login_path: str, current_path: str) -> str:
    """Union of both PATHs, login-shell entries first, de-duped, order-preserving."""
    seen: set[str] = set()
    merged: list[str] = []
    for entry in login_path.split(os.pathsep) + current_path.split(os.pathsep):
        if entry and entry not in seen:
            seen.add(entry)
            merged.append(entry)
    return os.pathsep.join(merged)


def _sync_path() -> None:
    login_path = _login_shell_path()
    if not login_path:
        return  # fail gracefully — leave PATH untouched
    merged = _merge_path(login_path, os.environ.get("PATH", ""))
    if merged != os.environ.get("PATH", ""):
        os.environ["PATH"] = merged
        logger.info(
            "path_machinery: synced PATH from login shell (%d entries)",
            len(merged.split(os.pathsep)),
        )


# Runs once, at plugin-import time (Code Puppy startup) — not on any
# per-tool-call hook, so it costs one subprocess spawn per session, not one
# per shell command.
_sync_path()

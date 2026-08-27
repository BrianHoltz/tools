"""Shared library for Wibey usage tracking.

Provides: transcript parsing, pricing, SQLite DB operations.
"""

import configparser
import json
import os
import sqlite3
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

DB_PATH = Path.home() / ".wibey" / "usage.db"

# Code Puppy's own quota lives on a separate Walmart backend (puppy-backend),
# not in any Wibey transcript. See docs/2026-08-07_UsageDashboard5MinPST.md
# § Code Puppy Quota Overlay for the full writeup of why this exists and how
# it was reverse-engineered from code_puppy/plugins/walmart_specific/.
PUPPY_CFG_PATH = Path.home() / ".code_puppy" / "puppy.cfg"
CODE_PUPPY_QUOTA_URL = "https://puppy-backend.walmart.com/quota/me"
CODE_PUPPY_QUOTA_TIMEOUT_SECS = 4

# Pricing per 1M tokens (USD)
PRICING = {
    "claude-opus-4-6":   {"input": 5.0, "output": 25.0, "cache_read": 0.50, "cache_create": 6.25},
    "claude-opus-4-5":   {"input": 5.0, "output": 25.0, "cache_read": 0.50, "cache_create": 6.25},
    "claude-sonnet-4-6": {"input": 3.0, "output": 15.0, "cache_read": 0.30, "cache_create": 3.75},
    "claude-sonnet-4-5": {"input": 3.0, "output": 15.0, "cache_read": 0.30, "cache_create": 3.75},
    "claude-haiku-4-5":  {"input": 1.0, "output": 5.0,  "cache_read": 0.10, "cache_create": 1.25},
}

# Fallback pricing for unknown models (use sonnet pricing as default)
DEFAULT_PRICING = {"input": 3.0, "output": 15.0, "cache_read": 0.30, "cache_create": 3.75}


def get_pricing(model: str) -> dict:
    """Get pricing for a model, falling back to default if unknown."""
    # Normalize: strip anything after the model family (e.g. dated snapshots)
    for key in PRICING:
        if key in model or model.startswith(key.rsplit("-", 1)[0]):
            return PRICING[key]
    return DEFAULT_PRICING


def compute_cost(model: str, input_tokens: int, output_tokens: int,
                 cache_read: int, cache_creation: int) -> float:
    """Compute cost in USD for a set of token counts."""
    p = get_pricing(model)
    cost = (
        input_tokens * p["input"] / 1_000_000
        + output_tokens * p["output"] / 1_000_000
        + cache_read * p["cache_read"] / 1_000_000
        + cache_creation * p["cache_create"] / 1_000_000
    )
    return cost


def init_db(db_path: Optional[Path] = None) -> sqlite3.Connection:
    """Initialize the SQLite database and return a connection."""
    path = db_path or DB_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(path))
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS sessions (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id      TEXT NOT NULL UNIQUE,
            project         TEXT,
            git_branch      TEXT,
            reason          TEXT,
            started_at      TEXT,
            ended_at        TEXT,
            duration_secs   REAL,
            message_count   INTEGER DEFAULT 0
        );

        CREATE TABLE IF NOT EXISTS token_usage (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id      TEXT NOT NULL,
            usage_date      TEXT,
            model           TEXT NOT NULL,
            input_tokens    INTEGER DEFAULT 0,
            output_tokens   INTEGER DEFAULT 0,
            cache_read      INTEGER DEFAULT 0,
            cache_creation  INTEGER DEFAULT 0,
            cost_usd        REAL DEFAULT 0
        );

        CREATE TABLE IF NOT EXISTS tool_usage (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id      TEXT NOT NULL,
            usage_date      TEXT,
            tool_name       TEXT NOT NULL,
            call_count      INTEGER DEFAULT 0,
            error_count     INTEGER DEFAULT 0
        );

        CREATE TABLE IF NOT EXISTS skill_usage (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id      TEXT NOT NULL,
            usage_date      TEXT,
            skill_name      TEXT NOT NULL,
            invocation_count INTEGER DEFAULT 0
        );

        CREATE TABLE IF NOT EXISTS code_puppy_quota (
            id                      INTEGER PRIMARY KEY AUTOINCREMENT,
            captured_at             TEXT NOT NULL,
            tokens_used             INTEGER,
            token_limit             INTEGER,
            requests_used           INTEGER,
            request_limit           INTEGER,
            resets_in_secs          INTEGER,
            large_model_tokens_used INTEGER,
            large_model_token_limit INTEGER,
            job_family              TEXT
        );

        CREATE INDEX IF NOT EXISTS idx_sessions_ended ON sessions(ended_at);
        CREATE INDEX IF NOT EXISTS idx_sessions_project ON sessions(project);
        CREATE INDEX IF NOT EXISTS idx_usage_session ON token_usage(session_id);
        CREATE INDEX IF NOT EXISTS idx_usage_model ON token_usage(model);
        CREATE INDEX IF NOT EXISTS idx_tool_session ON tool_usage(session_id);
        CREATE INDEX IF NOT EXISTS idx_tool_name ON tool_usage(tool_name);
        CREATE INDEX IF NOT EXISTS idx_tool_date ON tool_usage(usage_date);
        CREATE INDEX IF NOT EXISTS idx_skill_session ON skill_usage(session_id);
        CREATE INDEX IF NOT EXISTS idx_skill_name ON skill_usage(skill_name);
        CREATE INDEX IF NOT EXISTS idx_skill_date ON skill_usage(usage_date);
    CREATE INDEX IF NOT EXISTS idx_cpq_captured ON code_puppy_quota(captured_at);
    """)
    # Migration: add usage_date column to existing databases (must run before index creation)
    try:
        conn.execute("ALTER TABLE token_usage ADD COLUMN usage_date TEXT")
    except sqlite3.OperationalError:
        pass  # Column already exists
    # Create index on usage_date after ensuring column exists
    conn.execute(
        "CREATE INDEX IF NOT EXISTS idx_usage_date ON token_usage(usage_date)"
    )
    conn.commit()
    return conn


def parse_transcript(transcript_path: str) -> dict:
    """Parse a transcript JSONL file and extract usage metrics.

    Returns:
        {
            "session_id": str,
            "project": str,
            "git_branch": str,
            "started_at": str (ISO8601),
            "ended_at": str (ISO8601),
            "duration_secs": float,
            "message_count": int,
            "daily_models": {
                "YYYY-MM-DD": {
                    "model_name": {
                        "input_tokens": int,
                        "output_tokens": int,
                        "cache_read": int,
                        "cache_creation": int,
                        "cost_usd": float,
                    }
                }
            },
            "models": { ... },  # flattened view across all days (backward compat)
            "daily_tools": {
                "YYYY-MM-DD": {
                    "tool_name": {"calls": int, "errors": int}
                }
            },
            "daily_skills": {
                "YYYY-MM-DD": {
                    "skill_name": {"invocations": int}
                }
            },
        }
    """
    session_id = None
    project = None
    git_branch = None
    first_ts = None
    last_ts = None
    message_count = 0
    daily_models = {}  # {date_str: {model: {tokens}}}
    bucket_5min_models = {}  # {5min_str (ISO): {model: {tokens}}}
    daily_tools = {}   # {date_str: {tool_name: {calls, errors}}}
    daily_skills = {}  # {date_str: {skill_name: {invocations}}}

    # Track tool_use ids to match with tool_results for error detection
    # Maps tool_use_id -> (tool_name, date_str)
    pending_tool_calls = {}

    try:
        with open(transcript_path, "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    entry = json.loads(line)
                except json.JSONDecodeError:
                    continue

                # Extract session metadata from any entry
                if not session_id and entry.get("sessionId"):
                    session_id = entry["sessionId"]
                if not project and entry.get("cwd"):
                    project = entry["cwd"]
                if not git_branch and entry.get("gitBranch"):
                    git_branch = entry["gitBranch"]

                # Track timestamps
                ts = entry.get("timestamp")
                if ts:
                    if first_ts is None:
                        first_ts = ts
                    last_ts = ts

                msg = entry.get("message", {})
                content = msg.get("content", [])
                if isinstance(content, str):
                    content = []

                msg_date = ts[:10] if ts and len(ts) >= 10 else None
                # 5-minute bucket: YYYY-MM-DDTHH:MM (round down to nearest 5 min)
                msg_bucket_5min = None
                if ts and len(ts) >= 16:
                    try:
                        dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
                        # Round down to nearest 5-minute interval
                        minute = (dt.minute // 5) * 5
                        msg_bucket_5min = dt.strftime(f"%Y-%m-%dT%H:{minute:02d}")
                    except (ValueError, TypeError):
                        pass

                # ── Extract tool_use from assistant messages ──
                if entry.get("type") == "assistant":
                    for block in content:
                        if not isinstance(block, dict):
                            continue
                        if block.get("type") == "tool_use":
                            tool_name = block.get("name", "unknown")
                            tool_id = block.get("id")

                            # Track tool call
                            if msg_date not in daily_tools:
                                daily_tools[msg_date] = {}
                            if tool_name not in daily_tools[msg_date]:
                                daily_tools[msg_date][tool_name] = {"calls": 0, "errors": 0}
                            daily_tools[msg_date][tool_name]["calls"] += 1

                            # Track pending call for error matching
                            if tool_id:
                                pending_tool_calls[tool_id] = (tool_name, msg_date)

                            # Extract skill name from Skill tool calls
                            if tool_name == "Skill":
                                skill_input = block.get("input", {})
                                skill_name = skill_input.get("skill", "unknown")
                                if msg_date not in daily_skills:
                                    daily_skills[msg_date] = {}
                                if skill_name not in daily_skills[msg_date]:
                                    daily_skills[msg_date][skill_name] = {"invocations": 0}
                                daily_skills[msg_date][skill_name]["invocations"] += 1

                # ── Extract tool_result from user messages (for error tracking) ──
                if entry.get("type") == "user":
                    for block in content:
                        if not isinstance(block, dict):
                            continue
                        if block.get("type") == "tool_result":
                            tool_id = block.get("tool_use_id")
                            is_error = block.get("is_error", False)
                            if is_error and tool_id and tool_id in pending_tool_calls:
                                tname, tdate = pending_tool_calls[tool_id]
                                if tdate in daily_tools and tname in daily_tools[tdate]:
                                    daily_tools[tdate][tname]["errors"] += 1

                # Extract token usage from assistant messages
                if entry.get("type") != "assistant":
                    continue

                usage = msg.get("usage")
                if not usage:
                    continue

                model = msg.get("model", "unknown")

                # Skip synthetic entries (local no-ops, e.g. "No response requested.")
                # They have all-zero usage and never hit the API.
                if model == "<synthetic>":
                    continue

                message_count += 1

                if msg_date not in daily_models:
                    daily_models[msg_date] = {}
                if model not in daily_models[msg_date]:
                    daily_models[msg_date][model] = {
                        "input_tokens": 0,
                        "output_tokens": 0,
                        "cache_read": 0,
                        "cache_creation": 0,
                        "cost_usd": 0.0,
                    }

                # 5-minute bucketing (fine-grained intra-day data)
                if msg_bucket_5min not in bucket_5min_models:
                    bucket_5min_models[msg_bucket_5min] = {}
                if model not in bucket_5min_models[msg_bucket_5min]:
                    bucket_5min_models[msg_bucket_5min][model] = {
                        "input_tokens": 0,
                        "output_tokens": 0,
                        "cache_read": 0,
                        "cache_creation": 0,
                        "cost_usd": 0.0,
                    }

                m = daily_models[msg_date][model]
                b = bucket_5min_models[msg_bucket_5min][model]
                inp = usage.get("input_tokens", 0)
                out = usage.get("output_tokens", 0)
                cr = usage.get("cache_read_input_tokens", 0)
                cc = usage.get("cache_creation_input_tokens", 0)

                # Update both daily and 5-minute buckets
                for dest in [m, b]:
                    dest["input_tokens"] += inp
                    dest["output_tokens"] += out
                    dest["cache_read"] += cr
                    dest["cache_creation"] += cc
                    dest["cost_usd"] += compute_cost(model, inp, out, cr, cc)

    except (FileNotFoundError, PermissionError, OSError):
        pass

    # Compute duration
    duration_secs = 0.0
    if first_ts and last_ts:
        try:
            t1 = datetime.fromisoformat(first_ts.replace("Z", "+00:00"))
            t2 = datetime.fromisoformat(last_ts.replace("Z", "+00:00"))
            duration_secs = (t2 - t1).total_seconds()
        except (ValueError, TypeError):
            pass

    # Flatten daily_models into session-level aggregate for backward compat
    models = {}
    for date_data in daily_models.values():
        for model, usage in date_data.items():
            if model not in models:
                models[model] = {
                    "input_tokens": 0, "output_tokens": 0,
                    "cache_read": 0, "cache_creation": 0, "cost_usd": 0.0,
                }
            for k, v in usage.items():
                models[model][k] += v

    return {
        "session_id": session_id or os.path.basename(transcript_path).replace(".jsonl", ""),
        "project": project,
        "git_branch": git_branch,
        "started_at": first_ts,
        "ended_at": last_ts,
        "duration_secs": duration_secs,
        "message_count": message_count,
        "daily_models": daily_models,
        "bucket_5min_models": bucket_5min_models,
        "models": models,  # backward compat: flattened across all days
        "daily_tools": daily_tools,
        "daily_skills": daily_skills,
    }


def store_session(conn: sqlite3.Connection, data: dict, reason: str = "exit",
                  force: bool = False):
    """Store parsed session data into the database.

    Keeps exactly ONE row per session_id in both tables.  When a session is
    resumed (same session_id, growing transcript), we UPDATE the existing row
    with the latest cumulative totals instead of inserting duplicates.

    force=True: always re-insert token_usage rows (used by backfill to populate
    usage_date on existing sessions without re-checking ended_at).
    """
    session_id = data["session_id"]
    ended_at = data["ended_at"]

    # Check if this session_id already exists (any ended_at)
    existing = conn.execute(
        "SELECT id, ended_at FROM sessions WHERE session_id = ?",
        (session_id,),
    ).fetchone()

    if existing:
        existing_ended = existing[1]
        # If the stored snapshot has the same or newer ended_at, skip UNLESS force
        if not force and existing_ended and ended_at and existing_ended >= ended_at:
            return

        # Update the existing row with the latest snapshot
        conn.execute(
            """UPDATE sessions
               SET project = ?, git_branch = ?, reason = ?,
                   started_at = ?, ended_at = ?, duration_secs = ?,
                   message_count = ?
               WHERE session_id = ?""",
            (
                data["project"],
                data["git_branch"],
                reason,
                data["started_at"],
                ended_at,
                data["duration_secs"],
                data["message_count"],
                session_id,
            ),
        )

        # Replace all usage rows: delete old, insert new
        conn.execute(
            "DELETE FROM token_usage WHERE session_id = ?",
            (session_id,),
        )
        conn.execute(
            "DELETE FROM tool_usage WHERE session_id = ?",
            (session_id,),
        )
        conn.execute(
            "DELETE FROM skill_usage WHERE session_id = ?",
            (session_id,),
        )
    else:
        conn.execute(
            """INSERT INTO sessions (session_id, project, git_branch, reason,
               started_at, ended_at, duration_secs, message_count)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                session_id,
                data["project"],
                data["git_branch"],
                reason,
                data["started_at"],
                ended_at,
                data["duration_secs"],
                data["message_count"],
            ),
        )

    # Store token usage (both daily and hourly)
    for date_str, date_data in data.get("daily_models", {}).items():
        for model, usage in date_data.items():
            conn.execute(
                """INSERT INTO token_usage (session_id, usage_date, model, input_tokens,
                   output_tokens, cache_read, cache_creation, cost_usd)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    session_id,
                    date_str,
                    model,
                    usage["input_tokens"],
                    usage["output_tokens"],
                    usage["cache_read"],
                    usage["cache_creation"],
                    usage["cost_usd"],
                ),
            )

    # Store 5-minute bucket token usage (using usage_date with 5-min precision)
    for bucket_str, bucket_data in data.get("bucket_5min_models", {}).items():
        for model, usage in bucket_data.items():
            conn.execute(
                """INSERT INTO token_usage (session_id, usage_date, model, input_tokens,
                   output_tokens, cache_read, cache_creation, cost_usd)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    session_id,
                    bucket_str,  # Store with 5-minute precision (YYYY-MM-DDTHH:MM)
                    model,
                    usage["input_tokens"],
                    usage["output_tokens"],
                    usage["cache_read"],
                    usage["cache_creation"],
                    usage["cost_usd"],
                ),
            )

    # Store tool usage
    for date_str, date_data in data.get("daily_tools", {}).items():
        for tool_name, counts in date_data.items():
            conn.execute(
                """INSERT INTO tool_usage (session_id, usage_date, tool_name,
                   call_count, error_count)
                   VALUES (?, ?, ?, ?, ?)""",
                (
                    session_id,
                    date_str,
                    tool_name,
                    counts["calls"],
                    counts["errors"],
                ),
            )

    # Store skill usage
    for date_str, date_data in data.get("daily_skills", {}).items():
        for skill_name, counts in date_data.items():
            conn.execute(
                """INSERT INTO skill_usage (session_id, usage_date, skill_name,
                   invocation_count)
                   VALUES (?, ?, ?, ?)""",
                (
                    session_id,
                    date_str,
                    skill_name,
                    counts["invocations"],
                ),
            )

    conn.commit()


# ── Code Puppy Quota Overlay ──────────────────────────────────────────────
# Code Puppy (this Walmart-internal fork) enforces its own 6-hour rolling
# token+request budget on puppy-backend, entirely separate from Wibey's
# weekly Claude quota. There is no local transcript to parse it from — it's
# a live-only snapshot behind GET /quota/me, auth'd with the same puppy_token
# JWT that lives in ~/.code_puppy/puppy.cfg. Reverse-engineered from
# code_puppy/plugins/walmart_specific/token_quota_display.py (the module
# backing Code Puppy's own `/usage` slash command) — see
# docs/2026-08-07_UsageDashboard5MinPST.md for the full writeup.
#
# Because puppy-backend keeps no history of its own, this module is the
# *only* place that history is captured: every `wibey-usage dash` run
# (hourly, via cron) takes one snapshot and appends it to code_puppy_quota.
# That cadence is coarse relative to the 6h reset window but is the natural
# resolution given the existing cron; a tighter poller can lower it later.


def get_code_puppy_token() -> Optional[str]:
    """Read the puppy_token JWT from ~/.code_puppy/puppy.cfg, or None."""
    if not PUPPY_CFG_PATH.exists():
        return None
    try:
        cfg = configparser.ConfigParser()
        cfg.read(str(PUPPY_CFG_PATH))
        return cfg.get("puppy", "puppy_token", fallback=None)
    except (configparser.Error, OSError):
        return None


def fetch_code_puppy_quota() -> Optional[dict]:
    """Fetch the live Code Puppy quota snapshot, or None on any failure.

    Mirrors token_quota_display.fetch_quota_status() in code-puppy itself:
    same URL, same x-api-key header, same fail-silently contract (this is
    a decorative overlay, never something that should break the dashboard).
    """
    token = get_code_puppy_token()
    if not token:
        return None
    req = urllib.request.Request(
        CODE_PUPPY_QUOTA_URL, headers={"x-api-key": token}
    )
    try:
        with urllib.request.urlopen(req, timeout=CODE_PUPPY_QUOTA_TIMEOUT_SECS) as resp:
            if resp.status != 200:
                return None
            return json.loads(resp.read())
    except (urllib.error.URLError, TimeoutError, ValueError, OSError):
        return None


def log_code_puppy_quota(conn: sqlite3.Connection) -> Optional[dict]:
    """Fetch + persist one Code Puppy quota snapshot. Returns the snapshot
    dict (with a 'captured_at' key added) on success, else None."""
    data = fetch_code_puppy_quota()
    if not data:
        return None
    # Naive UTC ISO string (no +00:00 suffix) — matches every other timestamp
    # format this module uses (monday_dt, grid bucket keys, etc.) so plain
    # string comparisons in cmd_dash's window filter work without surprises.
    captured_at = datetime.now(timezone.utc).replace(tzinfo=None, microsecond=0).isoformat()
    try:
        conn.execute(
            """INSERT INTO code_puppy_quota
               (captured_at, tokens_used, token_limit, requests_used,
                request_limit, resets_in_secs, large_model_tokens_used,
                large_model_token_limit, job_family)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                captured_at,
                data.get("tokens_used"),
                data.get("token_limit"),
                data.get("requests_used"),
                data.get("request_limit"),
                data.get("resets_in_secs"),
                data.get("large_model_tokens_used"),
                data.get("large_model_token_limit"),
                data.get("job_family"),
            ),
        )
        conn.commit()
    except sqlite3.Error:
        return None
    return {**data, "captured_at": captured_at}

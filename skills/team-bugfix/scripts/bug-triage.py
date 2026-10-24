#!/usr/bin/env python3
"""Standalone BUG_LRS triage CLI for Python-based projects.

This mirrors the runtime `scripts/bug-triage.js` contract:

  python scripts/bug-triage.py --since 24h
  python scripts/bug-triage.py --mark-fixed <id> "note"
  python scripts/bug-triage.py --dismiss <id> "reason"
  python scripts/bug-triage.py --reset

It reads BUG_LRS xAPI statements, filters by BUG_APP_ID, deduplicates bugs,
joins shared GCS fix-log state, and writes `bug-triage-report.md`.
"""

from __future__ import annotations

import base64
import datetime as dt
import importlib.util
import json
import os
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


REPORT_PATH = Path.cwd() / "bug-triage-report.md"
CAS_RETRIES = 5
SEV_WEIGHT = {"fatal": 4, "error": 3, "warning": 2, "info": 1}
CONFIG_ENV_KEYS = frozenset(
    {
        "APP_URL",
        "BUG_APP_ID",
        "BUG_FIXLOG_GCS_PATH",
        "BUG_LRS_ENDPOINT",
        "BUG_LRS_PASSWORD",
        "BUG_LRS_TIMEOUT_SECONDS",
        "BUG_LRS_USERNAME",
        "GCP_PROJECT_ID",
        "GCS_BUCKET_NAME",
        "GCS_KEY_FILE",
    }
)
BUG_LRS_REQUIRED_KEYS = (
    "BUG_LRS_ENDPOINT",
    "BUG_LRS_USERNAME",
    "BUG_LRS_PASSWORD",
)


@dataclass(frozen=True)
class EnvironmentLoadResult:
    source: Path | None
    checked_paths: tuple[Path, ...]
    loaded_keys: tuple[str, ...]


def _dotenv_value(raw: str) -> str:
    value = raw.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return re.split(r"\s+#", value, maxsplit=1)[0].rstrip()


def _load_allowlisted_env(path: Path) -> tuple[str, ...]:
    loaded: list[str] = []
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        raise RuntimeError(f"cannot read BUG_LRS config file {path}: {exc}") from exc

    for raw_line in lines:
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[7:].lstrip()
        if "=" not in line:
            continue
        name, raw_value = line.split("=", 1)
        name = name.strip()
        if name not in CONFIG_ENV_KEYS or name in os.environ:
            continue
        os.environ[name] = _dotenv_value(raw_value)
        loaded.append(name)
    return tuple(sorted(loaded))


def _candidate_secret_paths(start: Path) -> tuple[Path, ...]:
    current = start.resolve()
    if current.is_file():
        current = current.parent
    candidates: list[Path] = []
    for directory in (current, *current.parents):
        candidates.append(directory / ".secrets.env")
        if (directory / ".git").exists():
            break
    return tuple(candidates)


def load_config_environment(cwd: Path | None = None) -> EnvironmentLoadResult:
    explicit = os.environ.get("BUG_LRS_ENV_FILE")
    if explicit:
        path = Path(explicit).expanduser().resolve()
        if not path.is_file():
            raise RuntimeError(f"BUG_LRS_ENV_FILE does not exist or is not a file: {path}")
        return EnvironmentLoadResult(path, (path,), _load_allowlisted_env(path))

    candidates = _candidate_secret_paths(cwd or Path.cwd())
    source = next((path for path in candidates if path.is_file()), None)
    loaded = _load_allowlisted_env(source) if source else ()
    return EnvironmentLoadResult(source, candidates, loaded)


def _env(name: str, default: str | None = None) -> str | None:
    return os.environ.get(name) or default


def _env_float(name: str, default: float) -> float:
    try:
        return float(os.environ.get(name, str(default)))
    except ValueError:
        return default


@dataclass(frozen=True)
class Config:
    app_url: str = field(default_factory=lambda: _env("APP_URL", "http://localhost:3000") or "http://localhost:3000")
    app_id: str = field(default_factory=lambda: _env("BUG_APP_ID", "default") or "default")
    bug_lrs_endpoint: str | None = field(default_factory=lambda: _env("BUG_LRS_ENDPOINT"))
    bug_lrs_username: str | None = field(default_factory=lambda: _env("BUG_LRS_USERNAME"))
    bug_lrs_password: str | None = field(default_factory=lambda: _env("BUG_LRS_PASSWORD"))
    bug_lrs_timeout: float = field(default_factory=lambda: _env_float("BUG_LRS_TIMEOUT_SECONDS", 30.0))
    gcp_project_id: str | None = field(default_factory=lambda: _env("GCP_PROJECT_ID"))
    gcs_bucket_name: str | None = field(default_factory=lambda: _env("GCS_BUCKET_NAME"))
    gcs_key_file: str | None = field(default_factory=lambda: _env("GCS_KEY_FILE"))
    fixlog_gcs_path: str = field(default_factory=lambda: _env("BUG_FIXLOG_GCS_PATH", "cache/bugfix/log.json") or "cache/bugfix/log.json")

    @property
    def bug_lrs_configured(self) -> bool:
        return bool(self.bug_lrs_endpoint and self.bug_lrs_username and self.bug_lrs_password)

    @property
    def missing_bug_lrs_keys(self) -> tuple[str, ...]:
        values = {
            "BUG_LRS_ENDPOINT": self.bug_lrs_endpoint,
            "BUG_LRS_USERNAME": self.bug_lrs_username,
            "BUG_LRS_PASSWORD": self.bug_lrs_password,
        }
        return tuple(key for key in BUG_LRS_REQUIRED_KEYS if not values[key])

    @property
    def fixlog_configured(self) -> bool:
        return bool(self.gcs_bucket_name)


def _gcs_dependency_available() -> bool:
    try:
        return importlib.util.find_spec("google.cloud.storage") is not None
    except ModuleNotFoundError:
        return False


def print_config_status(config: Config, env_load: EnvironmentLoadResult) -> None:
    print(f"[bug-triage] BUG_LRS fetch configured: {'yes' if config.bug_lrs_configured else 'no'}")
    print(f"[bug-triage] config source: {env_load.source or 'process environment / none'}")
    if config.missing_bug_lrs_keys:
        print(f"[bug-triage] missing: {', '.join(config.missing_bug_lrs_keys)}")
    if env_load.source:
        loaded = ", ".join(env_load.loaded_keys) if env_load.loaded_keys else "none (process environment may override file values)"
        print(f"[bug-triage] allowlisted keys loaded from file: {loaded}")
    elif env_load.checked_paths:
        print(f"[bug-triage] nearest config checked: {env_load.checked_paths[0]}")
    print(f"[bug-triage] shared GCS fix log configured: {'yes' if config.fixlog_configured else 'no'}")
    if not config.fixlog_configured:
        print("[bug-triage] missing for mark-fixed/dismiss/reset: GCS_BUCKET_NAME")
    print(f"[bug-triage] google-cloud-storage available: {'yes' if _gcs_dependency_available() else 'no'}")


def _utc_now() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc)


def _iso_utc(value: dt.datetime) -> str:
    return value.astimezone(dt.timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")


def since_to_iso(value: str | None) -> str:
    if not value:
        return _iso_utc(_utc_now() - dt.timedelta(days=7))

    match = re.fullmatch(r"(\d+)(h|d|w)", str(value).strip())
    if match:
        amount = int(match.group(1))
        unit = match.group(2)
        delta = {
            "h": dt.timedelta(hours=amount),
            "d": dt.timedelta(days=amount),
            "w": dt.timedelta(weeks=amount),
        }[unit]
        return _iso_utc(_utc_now() - delta)

    raw = str(value).strip()
    try:
        parsed = dt.datetime.fromisoformat(raw.replace("Z", "+00:00"))
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=dt.timezone.utc)
        return _iso_utc(parsed)
    except ValueError:
        return _iso_utc(_utc_now() - dt.timedelta(days=7))


def _extension_keys(config: Config, name: str) -> list[str]:
    app_url = config.app_url.rstrip("/")
    keys = [f"{app_url}/{name}"]
    if config.app_url != app_url:
        keys.append(f"{config.app_url}/{name}")
    return keys


def extension(statement: dict[str, Any], config: Config, name: str) -> Any:
    extensions = ((statement.get("context") or {}).get("extensions") or {})
    for key in _extension_keys(config, name):
        if key in extensions:
            return extensions[key]
    return None


def categorize(bug: dict[str, Any]) -> str:
    haystack = f"{bug.get('message') or ''} {bug.get('route') or ''}".lower()
    if re.search(r"401|403|auth|token|login", haystack):
        return "Authentication"
    if re.search(r"404|not found", haystack):
        return "Not Found"
    if re.search(r"429|rate.?limit", haystack):
        return "Rate Limiting"
    if re.search(r"413|payload too large|request entity", haystack):
        return "Payload Size"
    if re.search(r"gcs|storage|bucket", haystack):
        return "Storage/GCS"
    if re.search(r"lrs|xapi|statement", haystack):
        return "xAPI/LRS"
    if re.search(r"llm|openai|gateway|token limit", haystack):
        return "LLM/AI"
    if re.search(r"assessment|attempt|rubric|score|scoring", haystack):
        return "Assessment"
    if re.search(r"i18n|translat|locale", haystack):
        return "i18n"
    if re.search(r"voice|websocket|webrtc|avatar|microphone", haystack):
        return "Voice/WebSocket"
    if re.search(r"learning|learner|student|assignment|scenario", haystack):
        return "Learning"
    if re.search(r"parse|json|unexpected", haystack):
        return "Data Parsing"
    if re.search(r"5\d\d|server error|internal", haystack):
        return "Server Error"
    if bug.get("source") == "client":
        return "Client Console"
    return "Other"


def read_bug_lrs(config: Config, since_iso: str) -> dict[str, Any]:
    if not config.bug_lrs_configured:
        return {"configured": False, "statements": []}

    endpoint = str(config.bug_lrs_endpoint).rstrip("/")
    query = urlencode({"since": since_iso, "limit": "2000"})
    url = f"{endpoint}/statements?{query}"
    token = base64.b64encode(f"{config.bug_lrs_username}:{config.bug_lrs_password}".encode("utf-8")).decode("ascii")
    request = Request(
        url,
        headers={
            "Authorization": f"Basic {token}",
            "X-Experience-API-Version": "1.0.3",
            "Accept": "application/json",
        },
    )

    try:
        with urlopen(request, timeout=config.bug_lrs_timeout) as response:
            payload = response.read().decode("utf-8")
    except HTTPError as exc:
        raise RuntimeError(f"BUG_LRS request failed with HTTP {exc.code}") from exc
    except URLError as exc:
        raise RuntimeError(f"BUG_LRS request failed: {exc.reason}") from exc

    try:
        data = json.loads(payload)
    except json.JSONDecodeError as exc:
        raise RuntimeError("BUG_LRS returned non-JSON data") from exc

    return {"configured": True, "statements": data.get("statements") or []}


def parse_bugs(statements: list[dict[str, Any]], config: Config) -> list[dict[str, Any]]:
    parsed: list[dict[str, Any]] = []
    for statement in statements:
        if extension(statement, config, "appId") != config.app_id:
            continue
        parsed.append(
            {
                "errorId": extension(statement, config, "errorId"),
                "source": extension(statement, config, "source"),
                "severity": extension(statement, config, "severity") or "error",
                "message": extension(statement, config, "message"),
                "stack": extension(statement, config, "stack"),
                "route": extension(statement, config, "route"),
                "statusCode": extension(statement, config, "statusCode"),
                "component": extension(statement, config, "component"),
                "timestamp": statement.get("timestamp"),
            }
        )

    deduped: dict[tuple[str, str, str, str], dict[str, Any]] = {}
    for item in parsed:
        key = (
            str(item.get("source") or ""),
            str(item.get("message") or ""),
            str(item.get("route") or ""),
            str(item.get("statusCode") or ""),
        )
        current = deduped.get(key)
        if current:
            current["occurrences"] += 1
            current["lastSeen"] = max(str(current.get("lastSeen") or ""), str(item.get("timestamp") or ""))
            continue
        deduped[key] = {**item, "occurrences": 1, "firstSeen": item.get("timestamp"), "lastSeen": item.get("timestamp")}
    return list(deduped.values())


def _storage_bucket(config: Config) -> Any:
    if not config.gcs_bucket_name:
        raise RuntimeError("GCS_BUCKET_NAME is required for the shared bug fix log")
    try:
        from google.cloud import storage  # type: ignore
    except ImportError as exc:
        raise RuntimeError("google-cloud-storage is required for the shared bug fix log") from exc

    if config.gcs_key_file:
        client = storage.Client.from_service_account_json(config.gcs_key_file, project=config.gcp_project_id)
    else:
        client = storage.Client(project=config.gcp_project_id)
    return client.bucket(config.gcs_bucket_name)


def _read_gcs_json_with_generation(config: Config) -> tuple[dict[str, Any] | None, int]:
    bucket = _storage_bucket(config)
    blob = bucket.blob(config.fixlog_gcs_path)
    try:
        blob.reload()
        generation = int(blob.generation or 0)
        text = blob.download_as_text(encoding="utf-8")
        return json.loads(text), generation
    except Exception as exc:  # google exceptions are optional dependencies.
        if exc.__class__.__name__ == "NotFound" or getattr(exc, "code", None) in (404, "404"):
            return None, 0
        raise


def read_fixlog(config: Config, *, strict: bool) -> tuple[dict[str, Any], str | None]:
    try:
        doc, _ = _read_gcs_json_with_generation(config)
        return doc or {"fixed": {}, "dismissed": {}}, None
    except RuntimeError:
        if strict:
            raise
        return {"fixed": {}, "dismissed": {}}, "shared GCS fix log is not configured; statuses are treated as open"
    except Exception as exc:
        if strict:
            raise RuntimeError(f"failed to read shared GCS fix log: {exc}") from exc
        return {"fixed": {}, "dismissed": {}}, "shared GCS fix log could not be read; statuses are treated as open"


def mutate_fixlog(config: Config, transform: Callable[[dict[str, Any]], dict[str, Any]]) -> dict[str, Any]:
    bucket = _storage_bucket(config)
    blob = bucket.blob(config.fixlog_gcs_path)
    for _ in range(CAS_RETRIES):
        doc, generation = _read_gcs_json_with_generation(config)
        base = doc or {"fixed": {}, "dismissed": {}}
        next_doc = transform(base)
        try:
            blob.upload_from_string(
                json.dumps(next_doc, ensure_ascii=False),
                content_type="application/json; charset=utf-8",
                if_generation_match=generation,
            )
            return next_doc
        except Exception as exc:
            if exc.__class__.__name__ == "PreconditionFailed" or getattr(exc, "code", None) in (412, "412"):
                continue
            raise
    raise RuntimeError(f"failed to update shared GCS fix log after {CAS_RETRIES} attempts")


def apply_fixlog_status(bugs: list[dict[str, Any]], fixlog: dict[str, Any]) -> list[dict[str, Any]]:
    fixed = fixlog.get("fixed") or {}
    dismissed = fixlog.get("dismissed") or {}
    out: list[dict[str, Any]] = []
    for bug in bugs:
        error_id = bug.get("errorId")
        status = "open"
        note = ""
        if error_id in fixed:
            status = "fixed"
            note = (fixed.get(error_id) or {}).get("note") or ""
        elif error_id in dismissed:
            status = "dismissed"
            note = (dismissed.get(error_id) or {}).get("reason") or ""
        score = SEV_WEIGHT.get(str(bug.get("severity") or "info"), 1) * min(int(bug.get("occurrences") or 1), 10)
        out.append({**bug, "category": categorize(bug), "score": score, "status": status, "fixNote": note})
    return sorted(out, key=lambda item: int(item.get("score") or 0), reverse=True)


def summarize(config: Config, raw_count: int, bugs: list[dict[str, Any]]) -> dict[str, Any]:
    by_severity: dict[str, int] = {}
    by_source: dict[str, int] = {}
    for bug in bugs:
        by_severity[str(bug.get("severity") or "error")] = by_severity.get(str(bug.get("severity") or "error"), 0) + 1
        by_source[str(bug.get("source") or "unknown")] = by_source.get(str(bug.get("source") or "unknown"), 0) + 1
    return {
        "appId": config.app_id,
        "total": raw_count,
        "unique": len(bugs),
        "open": sum(1 for bug in bugs if bug.get("status") == "open"),
        "fixed": sum(1 for bug in bugs if bug.get("status") == "fixed"),
        "dismissed": sum(1 for bug in bugs if bug.get("status") == "dismissed"),
        "bySeverity": by_severity,
        "bySource": by_source,
    }


def render_report(since: str, bugs: list[dict[str, Any]], summary: dict[str, Any], fixlog_note: str | None) -> str:
    lines = [
        "# Bug Triage Report",
        "",
        f"- Since: {since}",
        f"- Unique: {summary['unique']}  |  Open: {summary['open']}  |  Fixed: {summary['fixed']}  |  Dismissed: {summary['dismissed']}",
        f"- By severity: {json.dumps(summary['bySeverity'], sort_keys=True)}  |  By source: {json.dumps(summary['bySource'], sort_keys=True)}",
    ]
    if fixlog_note:
        lines.append(f"- Fix log: {fixlog_note}")
    lines.append("")

    by_category: dict[str, list[dict[str, Any]]] = {}
    for bug in bugs:
        by_category.setdefault(str(bug.get("category") or "Other"), []).append(bug)

    categories = sorted(
        by_category,
        key=lambda category: sum(int(item.get("score") or 0) for item in by_category[category]),
        reverse=True,
    )
    for category in categories:
        lines.extend([f"## {category}", ""])
        for bug in [item for item in by_category[category] if item.get("status") == "open"]:
            message = str(bug.get("message") or "")[:120]
            lines.append(f"### [{bug.get('severity')}] {message}")
            lines.append(
                f"- errorId: `{bug.get('errorId')}`  |  occurrences: {bug.get('occurrences')}  |  score: {bug.get('score')}"
            )
            if bug.get("route"):
                status = f"  ({bug.get('statusCode')})" if bug.get("statusCode") else ""
                lines.append(f"- route: `{bug.get('route')}`{status}")
            if bug.get("stack"):
                lines.append("```")
                lines.append(str(bug.get("stack"))[:1200])
                lines.append("```")
            lines.append("")
    return "\n".join(lines)


def run_since(config: Config, since_arg: str, env_load: EnvironmentLoadResult | None = None) -> None:
    since_iso = since_to_iso(since_arg)
    data = read_bug_lrs(config, since_iso)
    if not data["configured"]:
        print(
            "[bug-triage] remote BUG_LRS queue is not enabled; "
            "continue with the user report and fresh local evidence."
        )
        return

    fixlog, fixlog_note = read_fixlog(config, strict=False)
    parsed = parse_bugs(data["statements"], config)
    bugs = apply_fixlog_status(parsed, fixlog)
    summary = summarize(config, len(parsed), bugs)

    REPORT_PATH.write_text(render_report(since_iso, bugs, summary, fixlog_note), encoding="utf-8")
    print(f"[bug-triage] {summary['open']} open / {summary['unique']} unique. Report -> {REPORT_PATH}")
    if fixlog_note:
        print(f"[bug-triage] {fixlog_note}")
    for bug in [item for item in bugs if item.get("status") == "open"][:25]:
        message = str(bug.get("message") or "")[:80]
        print(
            f"  - [{bug.get('severity')}] ({bug.get('category')}) "
            f"x{bug.get('occurrences')}  {message}  [{bug.get('errorId')}]"
        )


def mark_fixed(config: Config, error_id: str, note: str) -> None:
    def transform(log: dict[str, Any]) -> dict[str, Any]:
        log.setdefault("fixed", {})[error_id] = {"fixedAt": _iso_utc(_utc_now()), "note": note or ""}
        log.setdefault("dismissed", {})
        return log

    mutate_fixlog(config, transform)
    print(f"marked fixed: {error_id}")


def dismiss(config: Config, error_id: str, reason: str) -> None:
    def transform(log: dict[str, Any]) -> dict[str, Any]:
        log.setdefault("fixed", {})
        log.setdefault("dismissed", {})[error_id] = {"dismissedAt": _iso_utc(_utc_now()), "reason": reason or ""}
        return log

    mutate_fixlog(config, transform)
    print(f"dismissed: {error_id}")


def reset_fixlog(config: Config) -> None:
    def transform(_: dict[str, Any]) -> dict[str, Any]:
        return {"fixed": {}, "dismissed": {}}

    mutate_fixlog(config, transform)
    print("fix log reset")


def print_help() -> None:
    print(
        "\n".join(
            [
                "Usage:",
                "  python scripts/bug-triage.py --since 24h",
                "  python scripts/bug-triage.py --config-status",
                "  python scripts/bug-triage.py --mark-fixed <errorId> \"note\"",
                "  python scripts/bug-triage.py --dismiss <errorId> \"reason\"",
                "  python scripts/bug-triage.py --reset",
                "  python scripts/bug-triage.py",
            ]
        )
    )


def interactive(config: Config, env_load: EnvironmentLoadResult) -> None:
    print("Bug triage - 1) fetch 7d  2) custom range  5) mark-fixed  6) dismiss  9) reset  0) exit")
    while True:
        choice = input("> ").strip()
        if choice == "0":
            return
        if choice == "1":
            run_since(config, "7d", env_load)
        elif choice == "2":
            run_since(config, input("range (e.g. 24h, 3d, 2w): ").strip() or "7d", env_load)
        elif choice == "5":
            mark_fixed(config, input("errorId: ").strip(), input("note: ").strip())
        elif choice == "6":
            dismiss(config, input("errorId: ").strip(), input("reason: ").strip())
        elif choice == "9":
            reset_fixlog(config)
        else:
            print("?")


def main(argv: list[str]) -> int:
    try:
        env_load = load_config_environment()
        config = Config()
    except RuntimeError as exc:
        print(f"[bug-triage] {exc}", file=sys.stderr)
        return 2
    if not argv:
        interactive(config, env_load)
        return 0
    if argv[0] in {"-h", "--help"}:
        print_help()
        return 0
    try:
        if argv[0] == "--since":
            run_since(config, argv[1] if len(argv) > 1 else "7d", env_load)
            return 0
        if argv[0] == "--config-status":
            print_config_status(config, env_load)
            return 0
        if argv[0] == "--mark-fixed":
            if len(argv) < 2:
                raise RuntimeError("--mark-fixed requires an errorId")
            mark_fixed(config, argv[1], " ".join(argv[2:]))
            return 0
        if argv[0] == "--dismiss":
            if len(argv) < 2:
                raise RuntimeError("--dismiss requires an errorId")
            dismiss(config, argv[1], " ".join(argv[2:]))
            return 0
        if argv[0] == "--reset":
            reset_fixlog(config)
            return 0
    except RuntimeError as exc:
        print(f"[bug-triage] {exc}", file=sys.stderr)
        return 2
    except Exception as exc:
        print(f"[bug-triage] operation failed: {exc}", file=sys.stderr)
        return 2

    print_help()
    return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

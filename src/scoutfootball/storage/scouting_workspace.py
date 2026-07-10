"""Opt-in local persistence for versioned scouting workspaces.

The browser workspace remains the source of interactive state. This module
adds an explicitly enabled, local-only persistence boundary with optimistic
concurrency, atomic writes, and immutable backups. It is not a cloud sync or
multi-user collaboration service.
"""

from __future__ import annotations

import json
import os
import re
import shutil
import threading
import uuid
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

WORKSPACE_SCHEMA = "scoutfootball.scouting-workspace"
WORKSPACE_RECORD_SCHEMA = "scoutfootball.scouting-workspace-record"
WORKSPACE_RECORD_VERSION = "1.0"
MAX_WORKSPACE_BYTES = 1_000_000
MAX_MAP_ENTRIES = 1_000
MAX_PLAYERS = 500
MAX_KEY_LENGTH = 180
MAX_NOTE_LENGTH = 2_000
_VALID_STATUSES = {"pending", "reviewing", "approved", "rejected"}
_FORBIDDEN_KEYS = {"__proto__", "prototype", "constructor"}
_WORKSPACE_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$")
_STORE_LOCK = threading.RLock()


class WorkspaceStoreError(ValueError):
    """Structured validation or persistence error for API translation."""

    def __init__(
        self,
        code: str,
        *,
        http_status: int = 400,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(code)
        self.code = code
        self.http_status = http_status
        self.metadata = metadata or {}


def _env_flag(name: str) -> bool:
    return os.environ.get(name, "").strip().lower() in {"1", "true", "yes", "on"}


def workspace_persistence_enabled() -> bool:
    """Return whether local workspace persistence was explicitly enabled."""
    return _env_flag("SCOUTFOOTBALL_ENABLE_WORKSPACE_WRITES")


def remote_workspace_access_enabled() -> bool:
    """Return whether non-loopback clients may access persisted workspaces."""
    return _env_flag("SCOUTFOOTBALL_ALLOW_REMOTE_WORKSPACE_WRITES")


def is_loopback_client(host: str | None) -> bool:
    """Treat direct loopback and FastAPI's in-process test client as local."""
    normalized = str(host or "").strip().lower()
    return (
        normalized in {"localhost", "::1", "testclient"}
        or normalized.startswith("127.")
    )


def _utc_now() -> str:
    return datetime.now(UTC).isoformat().replace("+00:00", "Z")


def _parse_timestamp(value: object, code: str) -> str:
    text = str(value or "").strip()
    if not text:
        raise WorkspaceStoreError(code)
    try:
        datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError as exc:
        raise WorkspaceStoreError(code) from exc
    return text


def _validate_workspace_id(value: object) -> str:
    workspace_id = str(value or "").strip()
    if not _WORKSPACE_ID_RE.fullmatch(workspace_id):
        raise WorkspaceStoreError("workspace_id_invalid")
    return workspace_id


def _validate_safe_keys(value: object, *, depth: int = 0) -> None:
    if depth > 12:
        raise WorkspaceStoreError("workspace_nesting_too_deep")
    if isinstance(value, dict):
        for key, child in value.items():
            if not isinstance(key, str) or key in _FORBIDDEN_KEYS:
                raise WorkspaceStoreError("workspace_key_invalid")
            if len(key) > MAX_KEY_LENGTH:
                raise WorkspaceStoreError("workspace_key_too_long")
            _validate_safe_keys(child, depth=depth + 1)
    elif isinstance(value, list):
        for child in value:
            _validate_safe_keys(child, depth=depth + 1)


def _validate_string_map(
    value: object,
    *,
    code: str,
    allowed_values: set[str] | None = None,
    max_value_length: int = MAX_NOTE_LENGTH,
) -> None:
    if not isinstance(value, dict) or len(value) > MAX_MAP_ENTRIES:
        raise WorkspaceStoreError(code)
    for key, item in value.items():
        if not isinstance(key, str) or not key or len(key) > MAX_KEY_LENGTH:
            raise WorkspaceStoreError(code)
        if not isinstance(item, str) or len(item) > max_value_length:
            raise WorkspaceStoreError(code)
        if allowed_values is not None and item not in allowed_values:
            raise WorkspaceStoreError(code)


def _validate_players(value: object, code: str) -> None:
    if not isinstance(value, list) or len(value) > MAX_PLAYERS:
        raise WorkspaceStoreError(code)
    for row in value:
        if not isinstance(row, dict):
            raise WorkspaceStoreError(code)
        key = str(row.get("key") or row.get("player_id") or row.get("name") or "")
        if not key or len(key) > MAX_KEY_LENGTH:
            raise WorkspaceStoreError(code)


def validate_workspace_payload(
    payload: object,
    *,
    expected_workspace_id: str | None = None,
) -> dict[str, Any]:
    """Validate and return a JSON-normalized browser workspace payload."""
    try:
        encoded = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    except (TypeError, ValueError) as exc:
        raise WorkspaceStoreError("workspace_json_invalid") from exc
    if len(encoded) > MAX_WORKSPACE_BYTES:
        raise WorkspaceStoreError("workspace_too_large", http_status=413)
    normalized = json.loads(encoded)
    if not isinstance(normalized, dict):
        raise WorkspaceStoreError("workspace_not_object")
    _validate_safe_keys(normalized)

    if normalized.get("schema") != WORKSPACE_SCHEMA:
        raise WorkspaceStoreError("workspace_schema_invalid")
    version = str(normalized.get("version") or "")
    if not version.startswith("1."):
        raise WorkspaceStoreError("workspace_version_unsupported")

    audit = normalized.get("audit")
    review = normalized.get("review")
    selections = normalized.get("selections")
    source = normalized.get("source")
    snapshot = normalized.get("watchlist_snapshot")
    if not all(isinstance(value, dict) for value in (audit, review, selections, source, snapshot)):
        raise WorkspaceStoreError("workspace_sections_invalid")

    workspace_id = _validate_workspace_id(audit.get("workspace_id"))
    if expected_workspace_id is not None and workspace_id != expected_workspace_id:
        raise WorkspaceStoreError("workspace_id_mismatch")
    revision = audit.get("revision")
    if not isinstance(revision, int) or isinstance(revision, bool) or revision < 1:
        raise WorkspaceStoreError("workspace_revision_invalid")
    _parse_timestamp(audit.get("created_at"), "workspace_created_at_invalid")
    _parse_timestamp(audit.get("updated_at"), "workspace_updated_at_invalid")
    _parse_timestamp(normalized.get("exported_at"), "workspace_exported_at_invalid")

    _validate_string_map(
        review.get("statuses"),
        code="workspace_statuses_invalid",
        allowed_values=_VALID_STATUSES,
        max_value_length=32,
    )
    _validate_string_map(review.get("shortlist_notes"), code="workspace_notes_invalid")
    _validate_string_map(review.get("watchlist_notes"), code="workspace_notes_invalid")
    _validate_players(selections.get("watchlist"), "workspace_watchlist_invalid")
    _validate_players(selections.get("shortlist"), "workspace_shortlist_invalid")

    rating_snapshot_ids = source.get("rating_snapshot_ids")
    if not isinstance(rating_snapshot_ids, list) or len(rating_snapshot_ids) > MAX_MAP_ENTRIES:
        raise WorkspaceStoreError("workspace_snapshot_ids_invalid")
    if any(not isinstance(item, str) or len(item) > MAX_KEY_LENGTH for item in rating_snapshot_ids):
        raise WorkspaceStoreError("workspace_snapshot_ids_invalid")
    player_keys = snapshot.get("player_keys")
    if not isinstance(player_keys, list) or len(player_keys) > MAX_PLAYERS:
        raise WorkspaceStoreError("workspace_snapshot_invalid")
    if any(not isinstance(item, str) or len(item) > MAX_KEY_LENGTH for item in player_keys):
        raise WorkspaceStoreError("workspace_snapshot_invalid")
    if snapshot.get("saved_at") is not None:
        _parse_timestamp(snapshot.get("saved_at"), "workspace_snapshot_date_invalid")
    return normalized


def _decision_count(workspace: dict[str, Any]) -> int:
    review = workspace["review"]
    selections = workspace["selections"]
    return sum(
        len(value)
        for value in (
            review["statuses"],
            review["shortlist_notes"],
            review["watchlist_notes"],
            selections["watchlist"],
            selections["shortlist"],
        )
    )


class ScoutingWorkspaceStore:
    """JSON record store for opt-in local scouting workspace persistence."""

    def __init__(self, root: Path) -> None:
        self.root = Path(root).resolve()
        self.backup_root = self.root / "backups"

    def _path(self, workspace_id: str) -> Path:
        return self.root / f"{_validate_workspace_id(workspace_id)}.json"

    def _read_record(self, path: Path) -> dict[str, Any]:
        try:
            record = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise WorkspaceStoreError("workspace_record_invalid", http_status=500) from exc
        if (
            not isinstance(record, dict)
            or record.get("schema") != WORKSPACE_RECORD_SCHEMA
            or record.get("version") != WORKSPACE_RECORD_VERSION
            or not isinstance(record.get("server_revision"), int)
        ):
            raise WorkspaceStoreError("workspace_record_invalid", http_status=500)
        validate_workspace_payload(
            record.get("workspace"),
            expected_workspace_id=path.stem,
        )
        return record

    def load(self, workspace_id: str) -> dict[str, Any]:
        path = self._path(workspace_id)
        if not path.exists():
            raise WorkspaceStoreError("workspace_not_found", http_status=404)
        with _STORE_LOCK:
            return self._read_record(path)

    def list_records(self, limit: int = 100) -> list[dict[str, Any]]:
        if not self.root.exists():
            return []
        records: list[dict[str, Any]] = []
        with _STORE_LOCK:
            for path in self.root.glob("*.json"):
                try:
                    record = self._read_record(path)
                except WorkspaceStoreError:
                    continue
                workspace = record["workspace"]
                records.append({
                    "workspace_id": workspace["audit"]["workspace_id"],
                    "server_revision": record["server_revision"],
                    "workspace_revision": workspace["audit"]["revision"],
                    "updated_at": workspace["audit"]["updated_at"],
                    "stored_at": record["stored_at"],
                    "decision_count": _decision_count(workspace),
                })
        records.sort(key=lambda item: item["stored_at"], reverse=True)
        return records[: max(1, min(int(limit), 100))]

    def latest(self) -> dict[str, Any]:
        records = self.list_records(limit=1)
        if not records:
            raise WorkspaceStoreError("workspace_not_found", http_status=404)
        return self.load(records[0]["workspace_id"])

    def save(
        self,
        workspace_id: str,
        payload: object,
        *,
        expected_revision: int | None = None,
    ) -> dict[str, Any]:
        workspace_id = _validate_workspace_id(workspace_id)
        workspace = validate_workspace_payload(
            payload,
            expected_workspace_id=workspace_id,
        )
        path = self._path(workspace_id)

        with _STORE_LOCK:
            current: dict[str, Any] | None = None
            if path.exists():
                current = self._read_record(path)
                current_revision = int(current["server_revision"])
                if expected_revision is None:
                    raise WorkspaceStoreError(
                        "workspace_precondition_required",
                        http_status=428,
                        metadata={"current_revision": current_revision},
                    )
                if expected_revision != current_revision:
                    raise WorkspaceStoreError(
                        "workspace_revision_conflict",
                        http_status=409,
                        metadata={"current_revision": current_revision},
                    )
                server_revision = current_revision + 1
            else:
                if expected_revision not in {None, 0}:
                    raise WorkspaceStoreError(
                        "workspace_revision_conflict",
                        http_status=409,
                        metadata={"current_revision": 0},
                    )
                server_revision = 1

            stored_at = _utc_now()
            record = {
                "schema": WORKSPACE_RECORD_SCHEMA,
                "version": WORKSPACE_RECORD_VERSION,
                "server_revision": server_revision,
                "stored_at": stored_at,
                "workspace": workspace,
            }
            self.root.mkdir(parents=True, exist_ok=True)
            if current is not None:
                self.backup_root.mkdir(parents=True, exist_ok=True)
                backup_path = self.backup_root / (
                    f"{workspace_id}.rev-{current['server_revision']}.{uuid.uuid4().hex}.json"
                )
                shutil.copy2(path, backup_path)

            temp_path = self.root / f".{workspace_id}.{uuid.uuid4().hex}.tmp"
            try:
                with temp_path.open("x", encoding="utf-8", newline="\n") as handle:
                    json.dump(record, handle, ensure_ascii=False, indent=2)
                    handle.write("\n")
                    handle.flush()
                    os.fsync(handle.fileno())
                temp_path.replace(path)
            finally:
                temp_path.unlink(missing_ok=True)
            return record

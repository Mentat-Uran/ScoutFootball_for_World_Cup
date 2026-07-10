"""Tests for opt-in local scouting workspace persistence."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from scoutfootball.api_server import create_app
from scoutfootball.storage.scouting_workspace import (
    ScoutingWorkspaceStore,
    WorkspaceStoreError,
    is_loopback_client,
    validate_workspace_payload,
)


def _workspace(
    workspace_id: str = "workspace-alpha",
    *,
    revision: int = 3,
    status: str = "approved",
) -> dict:
    return {
        "schema": "scoutfootball.scouting-workspace",
        "version": "1.1.0",
        "exported_at": "2026-07-11T01:00:00Z",
        "audit": {
            "workspace_id": workspace_id,
            "created_at": "2026-07-10T01:00:00Z",
            "updated_at": "2026-07-11T01:00:00Z",
            "revision": revision,
            "device_scope": "browser-local",
            "last_action": "manual-export",
            "app_version": "1.0.3",
            "imported_from": "",
        },
        "source": {
            "rating_snapshot_ids": ["run-2526"],
            "attribution": "ScoutFootball local scouting decisions",
        },
        "review": {
            "statuses": {"player-7": status},
            "shortlist_notes": {"Ada": "Check role fit"},
            "watchlist_notes": {},
        },
        "selections": {
            "watchlist": [],
            "shortlist": [{
                "key": "player-7",
                "player_id": "player-7",
                "name": "Ada",
                "team": "Alpha",
                "position": "AM",
                "rating": 88.5,
            }],
        },
        "watchlist_snapshot": {
            "player_keys": ["player-7"],
            "saved_at": "2026-07-11T00:30:00Z",
        },
    }


def test_validate_workspace_payload_rejects_mismatch_and_unsafe_content() -> None:
    valid = validate_workspace_payload(
        _workspace(),
        expected_workspace_id="workspace-alpha",
    )
    assert valid["audit"]["revision"] == 3

    with pytest.raises(WorkspaceStoreError, match="workspace_id_mismatch"):
        validate_workspace_payload(
            _workspace(),
            expected_workspace_id="workspace-other",
        )

    invalid = _workspace()
    invalid["review"]["statuses"]["player-7"] = "silently-approved"
    with pytest.raises(WorkspaceStoreError, match="workspace_statuses_invalid"):
        validate_workspace_payload(invalid)

    unsafe = _workspace()
    unsafe["review"]["statuses"] = {"__proto__": "approved"}
    with pytest.raises(WorkspaceStoreError, match="workspace_key_invalid"):
        validate_workspace_payload(unsafe)


def test_store_uses_server_revision_conflicts_atomic_update_and_backup(tmp_path: Path) -> None:
    store = ScoutingWorkspaceStore(tmp_path / "workspaces")
    created = store.save("workspace-alpha", _workspace())
    assert created["server_revision"] == 1
    assert store.load("workspace-alpha")["workspace"]["audit"]["revision"] == 3

    updated_workspace = _workspace(revision=4, status="reviewing")
    with pytest.raises(WorkspaceStoreError) as missing_precondition:
        store.save("workspace-alpha", updated_workspace)
    assert missing_precondition.value.http_status == 428

    with pytest.raises(WorkspaceStoreError) as conflict:
        store.save("workspace-alpha", updated_workspace, expected_revision=9)
    assert conflict.value.http_status == 409
    assert conflict.value.metadata == {"current_revision": 1}

    updated = store.save(
        "workspace-alpha",
        updated_workspace,
        expected_revision=1,
    )
    assert updated["server_revision"] == 2
    assert updated["workspace"]["review"]["statuses"]["player-7"] == "reviewing"
    assert len(list((store.root / "backups").glob("workspace-alpha.rev-1.*.json"))) == 1
    assert not list(store.root.glob("*.tmp"))

    records = store.list_records()
    assert records[0]["workspace_id"] == "workspace-alpha"
    assert records[0]["server_revision"] == 2
    assert records[0]["decision_count"] == 3
    assert store.latest()["server_revision"] == 2


def test_store_rejects_oversized_payload_and_invalid_identifier(tmp_path: Path) -> None:
    store = ScoutingWorkspaceStore(tmp_path / "workspaces")
    oversized = _workspace()
    oversized["source"]["attribution"] = "x" * 1_000_000
    with pytest.raises(WorkspaceStoreError) as too_large:
        store.save("workspace-alpha", oversized)
    assert too_large.value.http_status == 413

    with pytest.raises(WorkspaceStoreError, match="workspace_id_invalid"):
        store.save("../escape", _workspace("../escape"))


def test_loopback_client_boundary() -> None:
    assert is_loopback_client("127.0.0.1")
    assert is_loopback_client("::1")
    assert is_loopback_client("testclient")
    assert not is_loopback_client("192.0.2.10")


def test_workspace_api_is_opt_in_and_supports_conflict_safe_round_trip(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("SCOUTFOOTBALL_DATA_ROOT", str(tmp_path / "data"))
    monkeypatch.delenv("SCOUTFOOTBALL_ENABLE_WORKSPACE_WRITES", raising=False)
    client = TestClient(create_app())

    capabilities = client.get("/scouting-workspaces/capabilities")
    assert capabilities.status_code == 200
    assert capabilities.json()["enabled"] is False
    disabled = client.put("/scouting-workspaces/workspace-alpha", json=_workspace())
    assert disabled.status_code == 403

    monkeypatch.setenv("SCOUTFOOTBALL_ENABLE_WORKSPACE_WRITES", "1")
    enabled = client.get("/scouting-workspaces/capabilities").json()
    assert enabled["enabled"] is True
    assert enabled["local_only"] is True

    created = client.put("/scouting-workspaces/workspace-alpha", json=_workspace())
    assert created.status_code == 200
    assert created.json()["server_revision"] == 1

    no_match = client.put(
        "/scouting-workspaces/workspace-alpha",
        json=_workspace(revision=4),
    )
    assert no_match.status_code == 428
    assert no_match.json()["detail"]["current_revision"] == 1

    conflict = client.put(
        "/scouting-workspaces/workspace-alpha",
        headers={"If-Match": '"8"'},
        json=_workspace(revision=4),
    )
    assert conflict.status_code == 409

    updated = client.put(
        "/scouting-workspaces/workspace-alpha",
        headers={"If-Match": '"1"'},
        json=_workspace(revision=4, status="reviewing"),
    )
    assert updated.status_code == 200
    assert updated.json()["server_revision"] == 2

    loaded = client.get("/scouting-workspaces/workspace-alpha")
    assert loaded.status_code == 200
    assert loaded.json()["workspace"]["audit"]["revision"] == 4
    latest = client.get("/scouting-workspaces/latest")
    assert latest.status_code == 200
    assert latest.json()["server_revision"] == 2
    listing = client.get("/scouting-workspaces").json()
    assert listing["count"] == 1
    json.dumps(listing)

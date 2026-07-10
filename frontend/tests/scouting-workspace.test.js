"use strict";

import assert from "node:assert/strict";
import test from "node:test";

await import("../scouting-workspace.js");

const workspaceApi = globalThis.SCOUTING_WORKSPACE;

function workspace(overrides = {}) {
    return workspaceApi.createWorkspace({
        workspace_id: "local-workspace",
        created_at: "2026-07-01T00:00:00.000Z",
        updated_at: "2026-07-01T00:00:00.000Z",
        exported_at: "2026-07-01T00:00:00.000Z",
        revision: 2,
        last_action: "local-edit",
        app_version: "1.0.3",
        review_statuses: { player_1: "reviewing" },
        shortlist_notes: { player_1: "Track the next three matches" },
        watchlist: [{ key: "player_1", name: "Player One", rating: 81 }],
        ...overrides,
    });
}

test("creates a versioned workspace with audit metadata", () => {
    const result = workspace();

    assert.equal(result.schema, "scoutfootball.scouting-workspace");
    assert.equal(result.version, "1.1.0");
    assert.equal(result.audit.workspace_id, "local-workspace");
    assert.equal(result.audit.revision, 2);
    assert.equal(result.audit.device_scope, "browser-local");
    assert.equal(result.audit.last_action, "local-edit");
});

test("migrates 1.0 exports and sanitizes unsafe keys and values", () => {
    const legacy = workspace();
    legacy.version = "1.0.0";
    legacy.audit.source = "manual-export";
    legacy.review.statuses = JSON.parse(
        '{"__proto__":"approved","player_1":"APPROVED","player_2":"invalid"}',
    );
    legacy.review.shortlist_notes.player_1 = "x".repeat(2_100);

    const result = workspaceApi.parseWorkspace(JSON.stringify(legacy));

    assert.equal(result.version, "1.1.0");
    assert.equal(result.review.statuses.player_1, "approved");
    assert.equal(result.review.statuses.player_2, undefined);
    assert.equal(Object.hasOwn(result.review.statuses, "__proto__"), false);
    assert.equal(result.review.shortlist_notes.player_1.length, 2_000);
});

test("rejects invalid and oversized imports", () => {
    assert.throws(() => workspaceApi.parseWorkspace("{"), /workspace_json_invalid/);
    assert.throws(
        () => workspaceApi.parseWorkspace(JSON.stringify({ schema: "wrong", version: "1.0.0" })),
        /workspace_schema_invalid/,
    );
    assert.throws(() => workspaceApi.parseWorkspace("x".repeat(1_000_001)), /workspace_too_large/);
});

test("reports same-key conflicts before import", () => {
    const local = workspace();
    const incoming = workspace({
        workspace_id: "incoming-workspace",
        updated_at: "2026-07-02T00:00:00.000Z",
        review_statuses: { player_1: "approved" },
        shortlist_notes: { player_1: "Ready for final review" },
    });

    const analysis = workspaceApi.analyzeConflict(local, incoming);

    assert.equal(analysis.different_workspace, true);
    assert.equal(analysis.status_conflicts, 1);
    assert.equal(analysis.note_conflicts, 1);
    assert.equal(analysis.total_conflicts, 2);
    assert.equal(analysis.preferred_source, "incoming");
});

test("safe merge unions selections and lets the newer workspace resolve conflicts", () => {
    const local = workspace({
        shortlist: [{ key: "local_pick", name: "Local Pick", rating: 78 }],
    });
    const incoming = workspace({
        workspace_id: "incoming-workspace",
        updated_at: "2026-07-03T00:00:00.000Z",
        revision: 7,
        review_statuses: { player_1: "approved", player_2: "reviewing" },
        shortlist_notes: { player_1: "Incoming decision" },
        watchlist: [{ key: "incoming_pick", name: "Incoming Pick", rating: 84 }],
    });

    const merged = workspaceApi.mergeWorkspaces(local, incoming);
    const summary = workspaceApi.summarizeWorkspace(merged);

    assert.equal(merged.audit.workspace_id, "local-workspace");
    assert.equal(merged.audit.revision, 8);
    assert.equal(merged.audit.last_action, "import-merge");
    assert.equal(merged.review.statuses.player_1, "approved");
    assert.equal(merged.review.statuses.player_2, "reviewing");
    assert.equal(merged.review.shortlist_notes.player_1, "Incoming decision");
    assert.deepEqual(
        merged.selections.watchlist.map((player) => player.key).sort(),
        ["incoming_pick", "player_1"],
    );
    assert.equal(summary.decision_count, 6);
});

test("server merge can adopt the persisted workspace identity", () => {
    const local = workspace();
    const persisted = workspace({
        workspace_id: "persisted-workspace",
        created_at: "2026-06-01T00:00:00.000Z",
        updated_at: "2026-07-03T00:00:00.000Z",
        revision: 9,
        last_action: "server-save",
    });

    const merged = workspaceApi.mergeWorkspaces(local, persisted, {
        workspaceId: persisted.audit.workspace_id,
    });

    assert.equal(merged.audit.workspace_id, "persisted-workspace");
    assert.equal(merged.audit.created_at, persisted.audit.created_at);
    assert.equal(merged.audit.imported_from, "local-workspace");
});

test("serialization round-trips into local state", () => {
    const original = workspace({ snapshot_player_keys: ["player_1"] });
    const parsed = workspaceApi.parseWorkspace(workspaceApi.serializeWorkspace(original));
    const local = workspaceApi.toLocalState(parsed);

    assert.equal(local.audit.workspace_id, "local-workspace");
    assert.equal(local.review_statuses.player_1, "reviewing");
    assert.equal(local.watchlist[0].key, "player_1");
    assert.deepEqual(local.snapshot_player_keys, ["player_1"]);
});

(function initScoutingWorkspace(root) {
    "use strict";

    const SCHEMA = "scoutfootball.scouting-workspace";
    const VERSION = "1.1.0";
    const MAX_BYTES = 1_000_000;
    const MAX_ENTRIES = 1_000;
    const MAX_PLAYERS = 500;
    const MAX_KEY_LENGTH = 180;
    const MAX_NOTE_LENGTH = 2_000;
    const VALID_STATUSES = new Set(["pending", "reviewing", "approved", "rejected"]);
    const VALID_ACTIONS = new Set([
        "local-edit",
        "manual-export",
        "import-merge",
        "import-replace",
        "server-save",
        "server-load",
    ]);
    const FORBIDDEN_KEYS = new Set(["__proto__", "prototype", "constructor"]);

    function isRecord(value) {
        return value !== null && typeof value === "object" && !Array.isArray(value);
    }

    function cleanString(value, maxLength) {
        return String(value == null ? "" : value).trim().slice(0, maxLength);
    }

    function cleanTimestamp(value, fallback) {
        const candidate = cleanString(value, 64);
        const parsed = Date.parse(candidate);
        return Number.isFinite(parsed) ? new Date(parsed).toISOString() : fallback;
    }

    function cleanPositiveInteger(value, fallback = 1) {
        const candidate = Number(value);
        if (!Number.isSafeInteger(candidate) || candidate < 1) return fallback;
        return Math.min(candidate, Number.MAX_SAFE_INTEGER);
    }

    function cleanKey(value) {
        const key = cleanString(value, MAX_KEY_LENGTH);
        if (!key || FORBIDDEN_KEYS.has(key)) return "";
        return key;
    }

    function cleanStatusMap(value) {
        const output = Object.create(null);
        if (!isRecord(value)) return output;
        for (const [rawKey, rawStatus] of Object.entries(value).slice(0, MAX_ENTRIES)) {
            const key = cleanKey(rawKey);
            const status = cleanString(rawStatus, 32).toLowerCase();
            if (key && VALID_STATUSES.has(status)) output[key] = status;
        }
        return output;
    }

    function cleanNoteMap(value) {
        const output = Object.create(null);
        if (!isRecord(value)) return output;
        for (const [rawKey, rawNote] of Object.entries(value).slice(0, MAX_ENTRIES)) {
            const key = cleanKey(rawKey);
            const note = cleanString(rawNote, MAX_NOTE_LENGTH);
            if (key && note) output[key] = note;
        }
        return output;
    }

    function cleanPlayerList(value) {
        if (!Array.isArray(value)) return [];
        const output = [];
        const seen = new Set();
        for (const row of value.slice(0, MAX_PLAYERS)) {
            if (!isRecord(row)) continue;
            const name = cleanString(row.player_name || row.name, MAX_KEY_LENGTH);
            const playerId = cleanString(row.player_id, 96);
            const key = cleanKey(row.key || playerId || name);
            const dedupeKey = key.toLowerCase();
            if (!key || seen.has(dedupeKey)) continue;
            seen.add(dedupeKey);
            const ratingValue = Number(row.optimized_score ?? row.rating);
            output.push({
                key,
                player_id: playerId,
                name,
                team: cleanString(row.team, MAX_KEY_LENGTH),
                position: cleanString(row.position_group || row.position, 32),
                rating: Number.isFinite(ratingValue) ? Math.max(0, Math.min(100, ratingValue)) : 0,
            });
        }
        return output;
    }

    function cleanStringList(value, maxItems, maxLength) {
        if (!Array.isArray(value)) return [];
        const output = [];
        const seen = new Set();
        for (const item of value.slice(0, maxItems)) {
            const cleaned = cleanString(item, maxLength);
            if (!cleaned || seen.has(cleaned)) continue;
            seen.add(cleaned);
            output.push(cleaned);
        }
        return output;
    }

    function fallbackWorkspaceId(createdAt) {
        const stamp = Date.parse(createdAt);
        return `workspace-${Number.isFinite(stamp) ? stamp.toString(36) : "local"}`;
    }

    function mergeStringLists(left, right, maxItems, maxLength) {
        return cleanStringList([...(left || []), ...(right || [])], maxItems, maxLength);
    }

    function mergePlayerLists(left, right) {
        const byKey = new Map();
        for (const player of cleanPlayerList(left)) byKey.set(player.key.toLowerCase(), player);
        for (const player of cleanPlayerList(right)) byKey.set(player.key.toLowerCase(), player);
        return Array.from(byKey.values()).slice(0, MAX_PLAYERS);
    }

    function countMapConflicts(left, right) {
        let count = 0;
        for (const key of Object.keys(left)) {
            if (Object.hasOwn(right, key) && left[key] !== right[key]) count += 1;
        }
        return count;
    }

    function createWorkspace(state) {
        const source = isRecord(state) ? state : {};
        const exportedAt = cleanTimestamp(source.exported_at, new Date().toISOString());
        const updatedAt = cleanTimestamp(source.updated_at, exportedAt);
        const createdAt = cleanTimestamp(source.created_at, updatedAt);
        const workspaceId = cleanKey(source.workspace_id) || fallbackWorkspaceId(createdAt);
        const lastAction = cleanString(source.last_action, 32).toLowerCase();
        return {
            schema: SCHEMA,
            version: VERSION,
            exported_at: exportedAt,
            audit: {
                workspace_id: workspaceId,
                created_at: createdAt,
                updated_at: updatedAt,
                revision: cleanPositiveInteger(source.revision, 1),
                device_scope: "browser-local",
                last_action: VALID_ACTIONS.has(lastAction) ? lastAction : "manual-export",
                app_version: cleanString(source.app_version, 32),
                imported_from: cleanKey(source.imported_from),
            },
            source: {
                rating_snapshot_ids: cleanStringList(source.rating_snapshot_ids, MAX_ENTRIES, 180),
                attribution: "ScoutFootball local scouting decisions; server queues remain read-only",
            },
            review: {
                statuses: cleanStatusMap(source.review_statuses),
                shortlist_notes: cleanNoteMap(source.shortlist_notes),
                watchlist_notes: cleanNoteMap(source.watchlist_notes),
            },
            selections: {
                watchlist: cleanPlayerList(source.watchlist),
                shortlist: cleanPlayerList(source.shortlist),
            },
            watchlist_snapshot: {
                player_keys: cleanStringList(source.snapshot_player_keys, MAX_PLAYERS, MAX_KEY_LENGTH),
                saved_at: cleanTimestamp(source.snapshot_saved_at, null),
            },
        };
    }

    function normalizeWorkspace(input) {
        if (!isRecord(input)) throw new Error("workspace_not_object");
        if (input.schema !== SCHEMA) throw new Error("workspace_schema_invalid");
        const version = cleanString(input.version, 32);
        if (!/^1\./.test(version)) throw new Error("workspace_version_unsupported");

        const audit = isRecord(input.audit) ? input.audit : {};
        const source = isRecord(input.source) ? input.source : {};
        const review = isRecord(input.review) ? input.review : {};
        const selections = isRecord(input.selections) ? input.selections : {};
        const snapshot = isRecord(input.watchlist_snapshot) ? input.watchlist_snapshot : {};
        return createWorkspace({
            exported_at: input.exported_at,
            workspace_id: audit.workspace_id,
            created_at: audit.created_at,
            updated_at: audit.updated_at,
            revision: audit.revision,
            last_action: audit.last_action || audit.source,
            imported_from: audit.imported_from,
            app_version: audit.app_version,
            rating_snapshot_ids: source.rating_snapshot_ids,
            review_statuses: review.statuses,
            shortlist_notes: review.shortlist_notes,
            watchlist_notes: review.watchlist_notes,
            watchlist: selections.watchlist,
            shortlist: selections.shortlist,
            snapshot_player_keys: snapshot.player_keys,
            snapshot_saved_at: snapshot.saved_at,
        });
    }

    function parseWorkspace(raw) {
        const text = typeof raw === "string" ? raw : JSON.stringify(raw);
        if (text.length > MAX_BYTES) throw new Error("workspace_too_large");
        let parsed;
        try {
            parsed = typeof raw === "string" ? JSON.parse(raw) : raw;
        } catch {
            throw new Error("workspace_json_invalid");
        }
        return normalizeWorkspace(parsed);
    }

    function toLocalState(workspace) {
        const normalized = normalizeWorkspace(workspace);
        return {
            audit: { ...normalized.audit },
            review_statuses: normalized.review.statuses,
            shortlist_notes: normalized.review.shortlist_notes,
            watchlist_notes: normalized.review.watchlist_notes,
            watchlist: normalized.selections.watchlist,
            shortlist: normalized.selections.shortlist,
            snapshot_player_keys: normalized.watchlist_snapshot.player_keys,
            snapshot_saved_at: normalized.watchlist_snapshot.saved_at,
        };
    }

    function summarizeWorkspace(workspace) {
        const normalized = normalizeWorkspace(workspace);
        const statusCount = Object.keys(normalized.review.statuses).length;
        const shortlistNoteCount = Object.keys(normalized.review.shortlist_notes).length;
        const watchlistNoteCount = Object.keys(normalized.review.watchlist_notes).length;
        return {
            workspace_id: normalized.audit.workspace_id,
            revision: normalized.audit.revision,
            updated_at: normalized.audit.updated_at,
            status_count: statusCount,
            note_count: shortlistNoteCount + watchlistNoteCount,
            watchlist_count: normalized.selections.watchlist.length,
            shortlist_count: normalized.selections.shortlist.length,
            snapshot_count: normalized.watchlist_snapshot.player_keys.length,
            decision_count:
                statusCount
                + shortlistNoteCount
                + watchlistNoteCount
                + normalized.selections.watchlist.length
                + normalized.selections.shortlist.length,
        };
    }

    function analyzeConflict(localWorkspace, incomingWorkspace) {
        const local = normalizeWorkspace(localWorkspace);
        const incoming = normalizeWorkspace(incomingWorkspace);
        const statusConflicts = countMapConflicts(local.review.statuses, incoming.review.statuses);
        const shortlistNoteConflicts = countMapConflicts(
            local.review.shortlist_notes,
            incoming.review.shortlist_notes,
        );
        const watchlistNoteConflicts = countMapConflicts(
            local.review.watchlist_notes,
            incoming.review.watchlist_notes,
        );
        const localUpdated = Date.parse(local.audit.updated_at);
        const incomingUpdated = Date.parse(incoming.audit.updated_at);
        const incomingIsNewer = incomingUpdated >= localUpdated;
        return {
            local: summarizeWorkspace(local),
            incoming: summarizeWorkspace(incoming),
            different_workspace: local.audit.workspace_id !== incoming.audit.workspace_id,
            status_conflicts: statusConflicts,
            note_conflicts: shortlistNoteConflicts + watchlistNoteConflicts,
            total_conflicts: statusConflicts + shortlistNoteConflicts + watchlistNoteConflicts,
            incoming_is_newer: incomingIsNewer,
            preferred_source: incomingIsNewer ? "incoming" : "local",
        };
    }

    function mergeWorkspaces(localWorkspace, incomingWorkspace, options) {
        const local = normalizeWorkspace(localWorkspace);
        const incoming = normalizeWorkspace(incomingWorkspace);
        const analysis = analyzeConflict(local, incoming);
        const preferred = analysis.incoming_is_newer ? incoming : local;
        const secondary = analysis.incoming_is_newer ? local : incoming;
        const targetWorkspaceId = cleanKey(options && options.workspaceId)
            || local.audit.workspace_id;
        const adoptingIncomingId = targetWorkspaceId === incoming.audit.workspace_id
            && targetWorkspaceId !== local.audit.workspace_id;
        const now = new Date().toISOString();
        return createWorkspace({
            workspace_id: targetWorkspaceId,
            created_at: adoptingIncomingId ? incoming.audit.created_at : local.audit.created_at,
            updated_at: now,
            exported_at: now,
            revision: Math.min(
                Math.max(local.audit.revision, incoming.audit.revision) + 1,
                Number.MAX_SAFE_INTEGER,
            ),
            last_action: "import-merge",
            imported_from: adoptingIncomingId
                ? local.audit.workspace_id
                : incoming.audit.workspace_id,
            app_version: local.audit.app_version || incoming.audit.app_version,
            rating_snapshot_ids: mergeStringLists(
                local.source.rating_snapshot_ids,
                incoming.source.rating_snapshot_ids,
                MAX_ENTRIES,
                180,
            ),
            review_statuses: {
                ...secondary.review.statuses,
                ...preferred.review.statuses,
            },
            shortlist_notes: {
                ...secondary.review.shortlist_notes,
                ...preferred.review.shortlist_notes,
            },
            watchlist_notes: {
                ...secondary.review.watchlist_notes,
                ...preferred.review.watchlist_notes,
            },
            watchlist: mergePlayerLists(secondary.selections.watchlist, preferred.selections.watchlist),
            shortlist: mergePlayerLists(secondary.selections.shortlist, preferred.selections.shortlist),
            snapshot_player_keys: preferred.watchlist_snapshot.player_keys,
            snapshot_saved_at: preferred.watchlist_snapshot.saved_at,
        });
    }

    function serializeWorkspace(workspace) {
        return JSON.stringify(normalizeWorkspace(workspace), null, 2);
    }

    root.SCOUTING_WORKSPACE = Object.freeze({
        SCHEMA,
        VERSION,
        MAX_BYTES,
        createWorkspace,
        normalizeWorkspace,
        parseWorkspace,
        serializeWorkspace,
        toLocalState,
        summarizeWorkspace,
        analyzeConflict,
        mergeWorkspaces,
    });
})(globalThis);

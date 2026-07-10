"use strict";

import assert from "node:assert/strict";
import test from "node:test";

await import("../search-typeahead-logic.js");

const logic = globalThis.SEARCH_TYPEAHEAD_LOGIC;

// ---------------------------------------------------------------------------
// 1. Minimum character threshold
// ---------------------------------------------------------------------------

test("queries shorter than MIN_QUERY_LENGTH do not trigger search", () => {
    assert.equal(logic.shouldQuery(""), false);
    assert.equal(logic.shouldQuery("M"), false);
    assert.equal(logic.shouldQuery(" "), false);
    assert.equal(logic.shouldQuery(null), false);
    assert.equal(logic.shouldQuery(undefined), false);
});

test("queries with at least MIN_QUERY_LENGTH characters trigger search", () => {
    assert.equal(logic.shouldQuery("Me"), true);
    assert.equal(logic.shouldQuery("Messi"), true);
    assert.equal(logic.shouldQuery("  Mes  "), true); // trimmed length >= 2
});

test("MIN_QUERY_LENGTH is 2", () => {
    assert.equal(logic.MIN_QUERY_LENGTH, 2);
});

// ---------------------------------------------------------------------------
// 2. Debounce — rapid inputs don't trigger multiple immediate requests
// ---------------------------------------------------------------------------

test("debounce coalesces rapid calls into a single invocation", () => {
    const calls = [];
    const fakeTimer = {
        setTimeout(cb) {
            // Store the callback so we can fire it synchronously later
            fakeTimer._pending = cb;
            return 1;
        },
        clearTimeout() {
            fakeTimer._pending = null;
        },
        _pending: null,
    };

    const debounced = logic.createDebouncer(
        (q) => calls.push(q),
        logic.DEBOUNCE_MS,
        fakeTimer,
    );

    // Simulate rapid typing: "M", "Me", "Mes"
    debounced.trigger("M");
    debounced.trigger("Me");
    debounced.trigger("Mes");

    // Each trigger clears the previous pending callback
    assert.equal(calls.length, 0);

    // Fire the last pending callback
    if (fakeTimer._pending) fakeTimer._pending();

    // Only the last argument is invoked
    assert.deepEqual(calls, ["Mes"]);
});

test("debounce cancel prevents invocation", () => {
    const calls = [];
    const fakeTimer = {
        setTimeout(cb) { fakeTimer._pending = cb; return 1; },
        clearTimeout() { fakeTimer._pending = null; },
        _pending: null,
    };

    const debounced = logic.createDebouncer(
        (q) => calls.push(q),
        logic.DEBOUNCE_MS,
        fakeTimer,
    );

    debounced.trigger("Mes");
    debounced.cancel();

    if (fakeTimer._pending) fakeTimer._pending();
    assert.equal(calls.length, 0);
});

test("DEBOUNCE_MS is 300", () => {
    assert.equal(logic.DEBOUNCE_MS, 300);
});

// ---------------------------------------------------------------------------
// 3. Empty results handling — "无匹配结果"
// ---------------------------------------------------------------------------

test("isEmptyResult returns true when both players and teams are empty", () => {
    assert.equal(logic.isEmptyResult({ players: [], teams: [] }), true);
    assert.equal(logic.isEmptyResult({}), true);
    assert.equal(logic.isEmptyResult(null), true);
});

test("isEmptyResult returns false when there are matches", () => {
    assert.equal(
        logic.isEmptyResult({ players: [{ player_name: "Messi" }], teams: [] }),
        false,
    );
    assert.equal(
        logic.isEmptyResult({ players: [], teams: [{ team_name: "Barcelona" }] }),
        false,
    );
});

test("buildItems returns empty array for empty API response", () => {
    const items = logic.buildItems({ players: [], teams: [] }, "all");
    assert.deepEqual(items, []);
});

// ---------------------------------------------------------------------------
// 4. buildItems — converts API response to display items
// ---------------------------------------------------------------------------

test("buildItems builds player items with label, sub, value, rating", () => {
    const data = {
        players: [
            { player_name: "Messi", team: "Barcelona", position: "RW", rating: 93.0 },
        ],
        teams: [],
    };
    const items = logic.buildItems(data, "players");
    assert.equal(items.length, 1);
    assert.equal(items[0].label, "Messi");
    assert.equal(items[0].sub, "Barcelona · RW");
    assert.equal(items[0].value, "Messi");
    assert.equal(items[0].rating, 93.0);
});

test("buildItems builds team items with label, sub, value", () => {
    const data = {
        players: [],
        teams: [{ team_name: "Arsenal", league: "Premier League" }],
    };
    const items = logic.buildItems(data, "teams");
    assert.equal(items.length, 1);
    assert.equal(items[0].label, "Arsenal");
    assert.equal(items[0].sub, "Premier League");
    assert.equal(items[0].value, "Arsenal");
    assert.equal(items[0].rating, undefined);
});

test("buildItems with type=all returns players then teams", () => {
    const data = {
        players: [{ player_name: "Messi", team: "Bar", position: "RW", rating: 93 }],
        teams: [{ team_name: "Barcelona", league: "La Liga" }],
    };
    const items = logic.buildItems(data, "all");
    assert.equal(items.length, 2);
    assert.equal(items[0].label, "Messi");
    assert.equal(items[1].label, "Barcelona");
});

test("buildItems filters out players when type=teams", () => {
    const data = {
        players: [{ player_name: "Messi" }],
        teams: [{ team_name: "Barcelona" }],
    };
    const items = logic.buildItems(data, "teams");
    assert.equal(items.length, 1);
    assert.equal(items[0].label, "Barcelona");
});

test("buildItems handles missing fields gracefully", () => {
    const data = {
        players: [{}],
        teams: [{}],
    };
    const items = logic.buildItems(data, "all");
    assert.equal(items.length, 2);
    assert.equal(items[0].label, "");
    assert.equal(items[0].sub, "");
});

// ---------------------------------------------------------------------------
// 5. Keyboard navigation logic
// ---------------------------------------------------------------------------

test("ArrowDown moves active index down and wraps to top", () => {
    assert.equal(logic.resolveActiveIndex("ArrowDown", -1, 3), 0);
    assert.equal(logic.resolveActiveIndex("ArrowDown", 0, 3), 1);
    assert.equal(logic.resolveActiveIndex("ArrowDown", 1, 3), 2);
    assert.equal(logic.resolveActiveIndex("ArrowDown", 2, 3), 0); // wrap
});

test("ArrowUp moves active index up and wraps to bottom", () => {
    assert.equal(logic.resolveActiveIndex("ArrowUp", 2, 3), 1);
    assert.equal(logic.resolveActiveIndex("ArrowUp", 1, 3), 0);
    assert.equal(logic.resolveActiveIndex("ArrowUp", 0, 3), 2); // wrap
    assert.equal(logic.resolveActiveIndex("ArrowUp", -1, 3), 2);
});

test("non-arrow keys do not change active index", () => {
    assert.equal(logic.resolveActiveIndex("Enter", 1, 3), 1);
    assert.equal(logic.resolveActiveIndex("Escape", 0, 3), 0);
    assert.equal(logic.resolveActiveIndex("a", 2, 3), 2);
});

test("keyboard navigation with zero items returns -1", () => {
    assert.equal(logic.resolveActiveIndex("ArrowDown", -1, 0), -1);
    assert.equal(logic.resolveActiveIndex("ArrowUp", -1, 0), -1);
});

// ---------------------------------------------------------------------------
// 6. Limit clamping (mirrors API behavior)
// ---------------------------------------------------------------------------

test("clampLimit clamps to 1..25", () => {
    assert.equal(logic.clampLimit(100), 25);
    assert.equal(logic.clampLimit(0), 1);
    assert.equal(logic.clampLimit(-5), 1);
    assert.equal(logic.clampLimit(10), 10);
    assert.equal(logic.clampLimit(1), 1);
    assert.equal(logic.clampLimit(25), 25);
});

test("clampLimit falls back to default for invalid input", () => {
    assert.equal(logic.clampLimit("abc"), logic.DEFAULT_LIMIT);
    assert.equal(logic.clampLimit(NaN), logic.DEFAULT_LIMIT);
    assert.equal(logic.clampLimit(undefined), logic.DEFAULT_LIMIT);
});

"use strict";

import assert from "node:assert/strict";
import test from "node:test";

await import("../action-value-explorer.js");

const explorer = globalThis.ACTION_VALUE_EXPLORER;

const rows = [
    {
        player_id: "10",
        player_name: "Ada Forward",
        team_id: "20",
        team_name: "City Women",
        season_context: "2022/2023 | 2023/2024",
        competition_context: "League | Cup",
        estimated_minutes: 1800,
        identity_status: "mapped",
    },
    {
        player_id: "11",
        player_name: "",
        team_id: "21",
        season: "2023/2024",
        competition: "League",
        estimated_minutes: 300,
        identity_status: "partial",
    },
];

test("splits season and competition contexts into exact filter values", () => {
    assert.deepEqual(explorer.rowSeasons(rows[0]), ["2022/2023", "2023/2024"]);
    assert.deepEqual(explorer.rowCompetitions(rows[0]), ["League", "Cup"]);
});

test("filters VAEP career rows by team, season, competition, and minutes", () => {
    const result = explorer.filterRows(rows, {
        team: "City Women",
        season: "2023/2024",
        competition: "Cup",
        minimumMinutes: 900,
    });
    assert.deepEqual(result.map((row) => row.player_id), ["10"]);
});

test("search includes source identifier and mapped context", () => {
    assert.equal(explorer.filterRows(rows, { query: "city women" }).length, 1);
    assert.equal(explorer.filterRows(rows, { query: "11" }).length, 1);
});

test("unmapped team rows keep an explicit identifier fallback", () => {
    assert.equal(explorer.rowTeam(rows[1]), "Team ID 21");
    assert.ok(explorer.filterOptions(rows).teams.includes("Team ID 21"));
});

test("identity summary prefers the API coverage report over page length", () => {
    const result = explorer.identitySummary({
        total_rows: 6771,
        mapped_rows: 6698,
        unmapped_rows: 73,
        granularity: "player_team_career",
    }, rows);
    assert.equal(result.total, 6771);
    assert.equal(result.mapped, 6698);
    assert.equal(result.rate, 6698 / 6771);
});

test("evidence index normalizes player IDs and detects availability", () => {
    const index = { available_player_ids: [5503, "5477", "5503", null] };
    assert.deepEqual(explorer.evidencePlayerIds(index), ["5503", "5477"]);
    assert.equal(explorer.hasEvidence(index, 5503), true);
    assert.equal(explorer.hasEvidence(index, "missing"), false);
});

test("core action evidence keeps pass carry shot in product order", () => {
    const detail = {
        action_types: [
            { key: "shot", n_actions: 2 },
            { key: "receipt", n_actions: 8 },
            { key: "pass", n_actions: 20 },
            { key: "carry", n_actions: 5 },
        ],
    };
    assert.deepEqual(explorer.coreActionTypes(detail).map((row) => row.key), [
        "pass",
        "carry",
        "shot",
    ]);
});

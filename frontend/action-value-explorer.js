(function (root, factory) {
    "use strict";
    const api = factory();
    if (typeof module === "object" && module.exports) module.exports = api;
    root.ACTION_VALUE_EXPLORER = api;
})(typeof globalThis !== "undefined" ? globalThis : this, function () {
    "use strict";

    function text(value) {
        return value == null ? "" : String(value).trim();
    }

    function splitContext(value) {
        return [...new Set(text(value).split("|").map((item) => item.trim()).filter(Boolean))];
    }

    function rowSeasons(row) {
        return [...new Set([text(row && row.season), ...splitContext(row && row.season_context)].filter(Boolean))];
    }

    function rowCompetitions(row) {
        return [...new Set([text(row && row.competition), ...splitContext(row && row.competition_context)].filter(Boolean))];
    }

    function rowTeam(row) {
        if (!row) return "";
        return text(row.team_name) || (text(row.team_id) ? `Team ID ${text(row.team_id)}` : "");
    }

    function filterRows(rows, filters) {
        const active = filters || {};
        const query = text(active.query).toLocaleLowerCase();
        const competition = text(active.competition || "ALL");
        const team = text(active.team || "ALL");
        const season = text(active.season || "ALL");
        const minimumMinutes = Number(active.minimumMinutes || 0);

        return (Array.isArray(rows) ? rows : []).filter((row) => {
            const seasons = rowSeasons(row);
            const competitions = rowCompetitions(row);
            const teamLabel = rowTeam(row);
            const label = text(row.player_name) || text(row.player_id);
            const haystack = [
                label,
                text(row.player_id),
                teamLabel,
                ...seasons,
                ...competitions,
            ].join(" ").toLocaleLowerCase();
            const minutes = Number(row.estimated_minutes || row.minutes || 0);
            return (!query || haystack.includes(query))
                && (competition === "ALL" || competitions.includes(competition))
                && (team === "ALL" || teamLabel === team)
                && (season === "ALL" || seasons.includes(season))
                && minutes >= minimumMinutes;
        });
    }

    function filterOptions(rows) {
        const teams = new Set();
        const seasons = new Set();
        const competitions = new Set();
        (Array.isArray(rows) ? rows : []).forEach((row) => {
            const team = rowTeam(row);
            if (team) teams.add(team);
            rowSeasons(row).forEach((value) => seasons.add(value));
            rowCompetitions(row).forEach((value) => competitions.add(value));
        });
        const sort = (values) => [...values].sort((a, b) => a.localeCompare(b, undefined, { numeric: true }));
        return {
            teams: sort(teams),
            seasons: sort(seasons),
            competitions: sort(competitions),
        };
    }

    function identitySummary(coverage, rows) {
        const source = coverage && typeof coverage === "object" ? coverage : {};
        const total = Number(source.total_rows ?? (Array.isArray(rows) ? rows.length : 0));
        const mapped = Number(source.mapped_rows ?? (Array.isArray(rows)
            ? rows.filter((row) => row.identity_status === "mapped").length
            : 0));
        return {
            total,
            mapped,
            unmapped: Number(source.unmapped_rows ?? Math.max(0, total - mapped)),
            rate: total > 0 ? mapped / total : 0,
            granularity: text(source.granularity) || "player_team_career",
            seasonContextSemantics: text(source.season_context_semantics),
        };
    }

    function evidencePlayerIds(index) {
        if (!index || typeof index !== "object") return [];
        if (Array.isArray(index.available_player_ids)) {
            return [...new Set(index.available_player_ids.map(text).filter(Boolean))];
        }
        return [...new Set((Array.isArray(index.player_index) ? index.player_index : [])
            .map((row) => text(row && row.player_id))
            .filter(Boolean))];
    }

    function hasEvidence(index, playerId) {
        return evidencePlayerIds(index).includes(text(playerId));
    }

    function coreActionTypes(detail) {
        const order = new Map([["pass", 0], ["carry", 1], ["shot", 2]]);
        return (Array.isArray(detail && detail.action_types) ? detail.action_types : [])
            .filter((row) => order.has(text(row && row.key)))
            .slice()
            .sort((a, b) => order.get(text(a.key)) - order.get(text(b.key)));
    }

    return Object.freeze({
        coreActionTypes,
        evidencePlayerIds,
        filterOptions,
        filterRows,
        hasEvidence,
        identitySummary,
        rowCompetitions,
        rowSeasons,
        rowTeam,
        splitContext,
        version: "1.0.0",
    });
});

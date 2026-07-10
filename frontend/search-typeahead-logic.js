"use strict";

/**
 * Pure-logic helpers extracted from the SearchTypeahead component in app.js.
 *
 * The SearchTypeahead component manipulates the DOM directly and cannot be
 * imported in Node.js without a DOM shim.  These helpers expose the
 * testable, side-effect-free logic (minimum query threshold, debounce,
 * item building) so they can be unit-tested with the Node.js test runner.
 *
 * The constants and behaviour here mirror SearchTypeahead in app.js —
 * keep them in sync when changing the component.
 */
(function initSearchTypeaheadLogic(root) {
    const MIN_QUERY_LENGTH = 2;
    const DEBOUNCE_MS = 300;
    const MAX_LIMIT = 25;
    const DEFAULT_LIMIT = 10;

    /**
     * Returns true when a query is long enough to trigger a search.
     * Mirrors the `query.length < 2` guard in SearchTypeahead's input handler.
     */
    function shouldQuery(query) {
        return query != null && String(query).trim().length >= MIN_QUERY_LENGTH;
    }

    /**
     * Clamp the limit to the same 1..25 range used by the API.
     */
    function clampLimit(limit) {
        const n = Number(limit);
        if (!Number.isFinite(n)) return DEFAULT_LIMIT;
        return Math.max(1, Math.min(Math.trunc(n), MAX_LIMIT));
    }

    /**
     * Build display items from an API search response.
     * Mirrors SearchTypeahead.buildItems — players get label/sub/value/rating,
     * teams get label/sub/value.
     */
    function buildItems(data, type) {
        type = type || "all";
        const all = [];
        if (type === "players" || type === "all") {
            (data.players || []).forEach(function (p) {
                all.push({
                    label: p.player_name || "",
                    sub: [p.team, p.position].filter(Boolean).join(" · "),
                    value: p.player_name || "",
                    rating: p.rating,
                });
            });
        }
        if (type === "teams" || type === "all") {
            (data.teams || []).forEach(function (t) {
                all.push({
                    label: t.team_name || "",
                    sub: t.league || "",
                    value: t.team_name || "",
                });
            });
        }
        return all;
    }

    /**
     * Returns true when the API response has zero matches.
     * Used to decide whether to show the "无匹配结果" empty state.
     */
    function isEmptyResult(data) {
        const players = (data && data.players) || [];
        const teams = (data && data.teams) || [];
        return players.length === 0 && teams.length === 0;
    }

    /**
     * Create a debounced version of `fn` that waits `delay` ms before invoking.
     * Accepts an optional timerProvider for deterministic testing.
     * Returns { trigger, cancel }.
     */
    function createDebouncer(fn, delay, timerProvider) {
        const timer = timerProvider || {
            setTimeout: function (cb, ms) { return setTimeout(cb, ms); },
            clearTimeout: function (id) { return clearTimeout(id); },
        };
        let pendingId = null;

        function trigger() {
            const args = arguments;
            timer.clearTimeout(pendingId);
            pendingId = timer.setTimeout(function () {
                pendingId = null;
                fn.apply(null, args);
            }, delay);
        }

        function cancel() {
            timer.clearTimeout(pendingId);
            pendingId = null;
        }

        return { trigger: trigger, cancel: cancel };
    }

    /**
     * Resolve the active index after an ArrowDown/ArrowUp keypress.
     * Wraps around at the boundaries, mirroring SearchTypeahead's keydown handler.
     */
    function resolveActiveIndex(key, currentIndex, itemCount) {
        if (itemCount <= 0) return -1;
        if (key === "ArrowDown") {
            return currentIndex < itemCount - 1 ? currentIndex + 1 : 0;
        }
        if (key === "ArrowUp") {
            return currentIndex > 0 ? currentIndex - 1 : itemCount - 1;
        }
        return currentIndex;
    }

    root.SEARCH_TYPEAHEAD_LOGIC = {
        MIN_QUERY_LENGTH: MIN_QUERY_LENGTH,
        DEBOUNCE_MS: DEBOUNCE_MS,
        MAX_LIMIT: MAX_LIMIT,
        DEFAULT_LIMIT: DEFAULT_LIMIT,
        shouldQuery: shouldQuery,
        clampLimit: clampLimit,
        buildItems: buildItems,
        isEmptyResult: isEmptyResult,
        createDebouncer: createDebouncer,
        resolveActiveIndex: resolveActiveIndex,
    };
})(typeof globalThis !== "undefined" ? globalThis : this);

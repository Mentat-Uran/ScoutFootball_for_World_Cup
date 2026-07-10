const APP_VERSION = "1.0.2";
const i18n = {
    zh: {
        nav_overview: "总览",
        nav_players: "球员",
        nav_compare: "对比",
        nav_value: "身价",
        nav_matches: "预测",
        nav_teams: "球队",
        nav_scouting: "球探",
        nav_actions: "动作价值",
        nav_reports: "报告",
        status_label: "本地产物",
        app_title: "ScoutFootball 分析终端",
        search_placeholder: "搜索球员、球队、报告",
        overview_kicker: "只读研究工作台",
        overview_title: "覆盖、模型、球探决策",
        metric_player_match: "球员比赛行",
        metric_team_match: "球队比赛行",
        metric_ratings: "评分行",
        metric_events: "事件样本",
        data_health: "数据健康",
        health_oof: "身价 OOF 可用",
        health_proxy: "球员 match-level 覆盖不足",
        health_trends: "趋势指标契约待统一",
        health_truth: "真实标签仍为空表",
        card_players: "球员画像",
        card_players_body: "排名、位置内 percentile、雷达、置信度和详情卡。",
        card_value: "身价偏离",
        card_value_body: "OOF 残差、偏差榜、年龄和联赛分层。",
        card_match: "比赛预测",
        card_match_body: "胜平负、比分矩阵、模型覆盖和校准入口。",
        players_kicker: "位置内画像",
        player_pool: "球员池",
        export: "导出",
        th_rank: "排名",
        th_player: "球员",
        th_pos: "位置",
        th_team: "球队",
        th_rating: "评分",
        th_conf: "置信度",
        th_season: "赛季",
        value_kicker: "OOF residual",
        value_title: "实际身价 vs 预测身价",
        compare_kicker: "球员对比",
        compare_title: "双球员雷达叠加与指标差异",
        compare_note: "选择两名球员进行位置百分位、雷达维度和关键统计的并排对比。",
        compare_select: "选择球员",
        compare_player_a: "球员 A",
        compare_player_b: "球员 B",
        compare_button: "对比",
        compare_radar_title: "雷达图对比",
        compare_stats_title: "关键指标",
        compare_pct_title: "位置百分位对比",
        compare_col_metric: "指标",
        compare_col_dimension: "维度",
        value_rank: "偏离榜",
        undervalued: "低估",
        overvalued: "高估",
        match_selector: "比赛选择",
        home_team: "主队",
        away_team: "客队",
        score_matrix: "比分矩阵",
        review_queue: "复核队列",
        watchlist: "Watchlist",
        snapshot: "快照",
        scouting_kicker: "本地优先决策台",
        scouting_title: "复核、观察与候选闭环",
        scouting_boundary: "服务端队列只读；复核状态、备注和球员页手动选择保存在当前浏览器。",
        teams_kicker: "球队实力分析",
        teams_title: "球队评分聚合与位置组实力",
        teams_note: "基于球员评分的分钟加权聚合，展示球队整体实力、位置组分布和核心球员。",
        teams_metric_count: "球队数",
        teams_metric_avg: "平均评分",
        teams_metric_top: "最高评分",
        teams_table_title: "球队排名",
        teams_col_team: "球队",
        teams_col_league: "联赛",
        teams_col_rating: "评分",
        teams_col_squad: "阵容",
        teams_detail_title: "球队详情",
        teams_detail_placeholder: "选择一支球队查看详情",
        teams_chart_title: "位置组实力对比",
        scouting_metric_review: "待复核",
        scouting_metric_short: "候选",
        scouting_search: "搜索球员、球队或原因",
        scouting_status_all: "全部状态",
        scouting_local_state: "本地状态",
        scout_workspace_export: "导出工作区",
        scout_workspace_import: "导入工作区",
        scout_workspace_preview_kicker: "安全导入",
        scout_workspace_preview_title: "球探工作区预览",
        scout_workspace_merge: "安全合并",
        scout_workspace_replace: "替换本地",
        action_kicker: "StatsBomb 样本",
        action_title: "动作价值研究台",
        action_boundary: "仅表示当前 StatsBomb Open Data 覆盖样本；默认过滤低于 450 分钟的极小样本。",
        action_search: "搜索球员或赛事",
        action_all_competitions: "全部赛事",
        action_ranking: "动作价值排名",
        action_pipeline: "动作价值后端",
        backend_contracts: "后端契约",
        minutes: "分钟",
        percentile: "百分位",
        value: "身价",
        residual: "残差",
        home: "主胜",
        draw: "平局",
        away: "客胜",
        expected_goals: "期望进球",
        coverage: "覆盖",
        nav_wc_schedule: "赛程",
        nav_wc_squads: "名单",
        nav_wc_compare: "对比",
        nav_wc_probability: "出线",
        wc_kicker: "2026 美加墨世界杯",
        wc_schedule_title: "小组赛赛程",
        wc_squads_title: "球队名单 & 评分",
        wc_compare_title: "球队实力对比",
        wc_prob_title: "小组出线概率",
        wc_teams: "球队",
        wc_groups: "小组",
        wc_group_matches: "小组赛",
        wc_fixtures: "赛程表",
        wc_date: "日期",
        wc_time: "时间",
        wc_group_col: "小组",
        wc_home: "主队",
        wc_away_col: "客队",
        wc_venue: "场馆",
        wc_squad_list: "球员名单",
        wc_club: "俱乐部",
        wc_league: "联赛",
        wc_rating_dist: "评分分布",
        wc_compare_summary: "总览对比",
        wc_strength_rank: "48 队实力排名",
        wc_strength: "实力评分",
        wc_entertainment: "娱乐性估算",
        wc_squad_size: "名单",
        wc_rated: "有评分",
        wc_big5: "五大联赛",
        wc_avg_rating: "均分",
        wc_no_data: "无数据",
        wc_low_coverage: "评分覆盖率低于50%，结论置信度较低",
        sort_priority: "优先级",
        sort_date: "日期",
        sort_name: "姓名",
        status_pending: "待处理",
        status_reviewing: "审核中",
        status_approved: "已通过",
        status_rejected: "已拒绝",
        scout_new_badge: "新",
        scout_note_placeholder: "添加备注...",
        nav_license: "数据源",
        nav_data: "数据",
        data_kicker: "数据状态",
        data_title: "数据源与覆盖",
        data_sources_table: "数据源列表",
        data_th_name: "名称",
        data_th_rows: "行数",
        data_th_updated: "最后更新",
        data_th_type: "类型",
        data_type_real: "真实",
        data_type_proxy: "代理",
        data_type_synthetic: "合成",
        data_coverage_league: "联赛覆盖",
        data_missing_warnings: "缺失数据警告",
        data_no_missing: "无缺失数据",
        data_source_real: "真实数据",
        data_source_proxy: "代理数据",
        data_source_synthetic: "合成数据",
        confidence_gate: "置信门槛",
        confidence_gate_desc: "覆盖率 > 0.90 = 高置信度",
        coverage_league: "联赛覆盖",
        rated_teams: "有评分球队",
        total_teams: "总球队",
        export_csv: "导出 CSV",
        license_kicker: "数据源许可",
        license_title: "Data Source Manifest",
        license_sources_label: "数据源",
        license_table_title: "数据源列表",
        license_th_source: "数据源",
        license_th_license: "许可证",
        license_th_attribution: "署名要求",
        license_th_url: "URL",
        license_attribution_notice: "StatsBomb 署名声明",
        model_version: "模型版本",
        model_comparison: "模型对比",
        coverage_warning: "▲ 覆盖率低于90%",
        log_loss: "对数损失",
        send_to_tactical: "发送到战术板",
        expand_details: "展开详情",
        collapse_details: "收起详情",
        copy_command: "复制命令",
        train_seasons: "训练赛季",
        test_seasons: "测试赛季",
        dependency_versions: "依赖版本",
        toggle_ratings: "切换评分",
        th_actions: "操作",
        action_watchlist: "观察",
        action_shortlist: "候选",
        action_tactical: "战术",
        action_compare: "对比",
        compare_title: "球员对比",
        compare_select_hint: "选择两名球员进行对比",
        compare_clear: "清除",
        compare_dimension: "维度",
        compare_percentile: "百分位",
        compare_no_same_pos: "两名球员位置不同，百分位基于各自位置池计算",
        value_fairness: "身价公平性",
        oof_residual_label: "OOF 残差",
        league_bias_label: "联赛偏差",
        position_bias_label: "位置偏差",
        age_curve_label: "年龄曲线",
        transfermarkt_notice: "Transfermarkt 数据需手动导入，当前为估算值",
        value_no_fairness: "暂无身价公平性数据",
        price_band_label: "价格区间",
        price_all: "全部",
        price_low: "低 (<20M)",
        price_medium: "中 (20-80M)",
        price_high: "高 (>80M)",
        age_curve_title: "年龄曲线",
        same_cohort_title: "同位置同年龄对比",
        watchlist_notes_label: "观察备注",
        generate_tactical_role: "生成战术角色",
        tactical_role_label: "战术角色分析",
        nav_calibration: "校准",
        nav_help: "帮助",
        calibration_kicker: "模型校准",
        calibration_title: "预测 vs 实际",
        calibration_plot: "校准图",
        calibration_brier: "Brier 分解",
        calibration_low_score: "低分桶分析",
        calibration_league: "联赛校准",
        xT_label: "xT 每90分钟",
        xT_percentile: "xT 百分位",
        xT_contribution: "xT 贡献",
        xT_not_available: "xT 数据不可用",
        confidence_reason_label: "置信原因",
        rating_snapshot: "评分快照",
    },
    en: {
        nav_overview: "Overview",
        nav_players: "Players",
        nav_compare: "Compare",
        nav_value: "Value",
        nav_matches: "Prediction",
        nav_teams: "Teams",
        nav_scouting: "Scouting",
        nav_actions: "Action Value",
        nav_reports: "Reports",
        status_label: "Local artifacts",
        app_title: "ScoutFootball Analyst Console",
        search_placeholder: "Search players, teams, reports",
        overview_kicker: "Read-only research desk",
        overview_title: "Coverage, models, scouting decisions",
        metric_player_match: "player match rows",
        metric_team_match: "team match rows",
        metric_ratings: "rating rows",
        metric_events: "event samples",
        data_health: "Data health",
        health_oof: "value OOF ready",
        health_proxy: "player match-level coverage is thin",
        health_trends: "trend metric contract pending",
        health_truth: "truth labels are still empty",
        card_players: "Player profile",
        card_players_body: "Rankings, percentiles, radar, confidence, detail cards.",
        card_value: "Value deviation",
        card_value_body: "OOF residuals, deviation boards, age and league slices.",
        card_match: "Match prediction",
        card_match_body: "1X2, score matrix, model coverage, calibration entry.",
        players_kicker: "Position profile",
        player_pool: "Player pool",
        export: "Export",
        th_rank: "Rank",
        th_player: "Player",
        th_pos: "Pos",
        th_team: "Team",
        th_rating: "Rating",
        th_conf: "Confidence",
        th_season: "Season",
        value_kicker: "OOF residual",
        value_title: "Actual value vs predicted value",
        compare_kicker: "Player Comparison",
        compare_title: "Dual radar overlay and metric diff",
        compare_note: "Select two players for side-by-side position percentile, radar dimension and key stat comparison.",
        compare_select: "Select Players",
        compare_player_a: "Player A",
        compare_player_b: "Player B",
        compare_button: "Compare",
        compare_radar_title: "Radar Comparison",
        compare_stats_title: "Key Metrics",
        compare_pct_title: "Position Percentile Comparison",
        compare_col_metric: "Metric",
        compare_col_dimension: "Dimension",
        value_rank: "Deviation board",
        undervalued: "Undervalued",
        overvalued: "Overvalued",
        match_selector: "Match selector",
        home_team: "Home",
        away_team: "Away",
        score_matrix: "Score matrix",
        review_queue: "Review queue",
        watchlist: "Watchlist",
        snapshot: "Snapshot",
        scouting_kicker: "Local-first decision desk",
        scouting_title: "Review, monitor, decide",
        scouting_boundary: "Server queues are read-only; review states, notes, and manual player selections stay in this browser.",
        teams_kicker: "Team Strength Analysis",
        teams_title: "Aggregated Ratings & Position Group Strength",
        teams_note: "Minutes-weighted aggregation of player ratings, showing overall team strength, position group distribution and key players.",
        teams_metric_count: "Teams",
        teams_metric_avg: "Avg Rating",
        teams_metric_top: "Top Rating",
        teams_table_title: "Team Rankings",
        teams_col_team: "Team",
        teams_col_league: "League",
        teams_col_rating: "Rating",
        teams_col_squad: "Squad",
        teams_detail_title: "Team Detail",
        teams_detail_placeholder: "Select a team to view details",
        teams_chart_title: "Position Group Strength Comparison",
        scouting_metric_review: "To review",
        scouting_metric_short: "Shortlist",
        scouting_search: "Search player, team, or reason",
        scouting_status_all: "All statuses",
        scouting_local_state: "Local state",
        scout_workspace_export: "Export workspace",
        scout_workspace_import: "Import workspace",
        scout_workspace_preview_kicker: "Safe import",
        scout_workspace_preview_title: "Scouting workspace preview",
        scout_workspace_merge: "Safe merge",
        scout_workspace_replace: "Replace local",
        action_kicker: "StatsBomb sample",
        action_title: "Action-value research desk",
        action_boundary: "Current StatsBomb Open Data coverage only; samples below 450 estimated minutes are filtered by default.",
        action_search: "Search player or competition",
        action_all_competitions: "All competitions",
        action_ranking: "Action-value ranking",
        action_pipeline: "Action-value backend",
        backend_contracts: "Backend contracts",
        minutes: "Minutes",
        percentile: "Percentile",
        value: "Value",
        residual: "Residual",
        home: "Home",
        draw: "Draw",
        away: "Away",
        expected_goals: "Expected goals",
        coverage: "Coverage",
        nav_wc_schedule: "Schedule",
        nav_wc_squads: "Squads",
        nav_wc_compare: "Compare",
        nav_wc_probability: "Odds",
        wc_kicker: "2026 FIFA World Cup",
        wc_schedule_title: "Group Stage Schedule",
        wc_squads_title: "Squad Ratings",
        wc_compare_title: "Team Comparison",
        wc_prob_title: "Advancement Probability",
        wc_teams: "Teams",
        wc_groups: "Groups",
        wc_group_matches: "Group Matches",
        wc_fixtures: "Fixtures",
        wc_date: "Date",
        wc_time: "Time",
        wc_group_col: "Group",
        wc_home: "Home",
        wc_away_col: "Away",
        wc_venue: "Venue",
        wc_squad_list: "Squad List",
        wc_club: "Club",
        wc_league: "League",
        wc_rating_dist: "Rating Distribution",
        wc_compare_summary: "Summary",
        wc_strength_rank: "48-Team Strength Ranking",
        wc_strength: "Strength",
        wc_entertainment: "Entertainment estimate",
        wc_squad_size: "Squad",
        wc_rated: "Rated",
        wc_big5: "Big 5",
        wc_avg_rating: "Avg",
        wc_no_data: "No data",
        wc_low_coverage: "Rating coverage below 50%, low confidence",
        sort_priority: "Priority",
        sort_date: "Date",
        sort_name: "Name",
        status_pending: "Pending",
        status_reviewing: "Reviewing",
        status_approved: "Approved",
        status_rejected: "Rejected",
        scout_new_badge: "new",
        scout_note_placeholder: "Add note...",
        nav_license: "Sources",
        nav_data: "Data",
        data_kicker: "Data Status",
        data_title: "Data Sources & Coverage",
        data_sources_table: "Data Sources",
        data_th_name: "Name",
        data_th_rows: "Rows",
        data_th_updated: "Last Updated",
        data_th_type: "Type",
        data_type_real: "Real",
        data_type_proxy: "Proxy",
        data_type_synthetic: "Synthetic",
        data_coverage_league: "League Coverage",
        data_missing_warnings: "Missing Data Warnings",
        data_no_missing: "No missing data",
        data_source_real: "Real data",
        data_source_proxy: "Proxy data",
        data_source_synthetic: "Synthetic data",
        confidence_gate: "Confidence Gate",
        confidence_gate_desc: "Coverage > 0.90 = high confidence",
        coverage_league: "League Coverage",
        rated_teams: "Rated Teams",
        total_teams: "Total Teams",
        export_csv: "Export CSV",
        license_kicker: "Data Source Licenses",
        license_title: "Data Source Manifest",
        license_sources_label: "Sources",
        license_table_title: "Data Source List",
        license_th_source: "Source",
        license_th_license: "License",
        license_th_attribution: "Attribution",
        license_th_url: "URL",
        license_attribution_notice: "StatsBomb Attribution Notice",
        model_version: "Model version",
        model_comparison: "Model comparison",
        coverage_warning: "▲ coverage below 90%",
        log_loss: "Log loss",
        send_to_tactical: "Send to tactical board",
        expand_details: "Expand details",
        collapse_details: "Collapse details",
        copy_command: "Copy command",
        train_seasons: "Train seasons",
        test_seasons: "Test seasons",
        dependency_versions: "Dependency versions",
        toggle_ratings: "Toggle ratings",
        th_actions: "Actions",
        action_watchlist: "Watch",
        action_shortlist: "Short",
        action_tactical: "Tactical",
        action_compare: "Compare",
        compare_title: "Player Comparison",
        compare_select_hint: "Select two players to compare",
        compare_clear: "Clear",
        compare_dimension: "Dimension",
        compare_percentile: "Percentile",
        compare_no_same_pos: "Players have different positions; percentiles are position-relative",
        value_fairness: "Value Fairness",
        oof_residual_label: "OOF Residual",
        league_bias_label: "League Bias",
        position_bias_label: "Position Bias",
        age_curve_label: "Age Curve",
        transfermarkt_notice: "Transfermarkt data requires manual import, estimates shown",
        value_no_fairness: "No value fairness data available",
        price_band_label: "Price Band",
        price_all: "All",
        price_low: "Low (<20M)",
        price_medium: "Mid (20-80M)",
        price_high: "High (>80M)",
        age_curve_title: "Age Curve",
        same_cohort_title: "Same-Position Same-Age Comparison",
        watchlist_notes_label: "Watchlist Notes",
        generate_tactical_role: "Generate Tactical Role",
        tactical_role_label: "Tactical Role Analysis",
        nav_calibration: "Calibration",
        nav_help: "Help",
        calibration_kicker: "Model calibration",
        calibration_title: "Predicted vs Actual",
        calibration_plot: "Calibration plot",
        calibration_brier: "Brier decomposition",
        calibration_low_score: "Low-score bucket analysis",
        calibration_league: "Per-league calibration",
        xT_label: "xT per 90",
        xT_percentile: "xT percentile",
        xT_contribution: "xT contribution",
        xT_not_available: "xT data not available",
        confidence_reason_label: "Confidence reason",
        rating_snapshot: "Rating snapshot",
    },
};

// ─ API configuration ─────────────────────────────────────────────────────
// Strategy: API-first with static fallback.
// - Always try the live API first.
// - If the API is unreachable (network error, timeout, 5xx), fall back to
//   the local static JSON files in /data/.
// - apiOnline tracks whether the backend is reachable so the UI can show
//   a status indicator.
const HOSTNAME = window.location.hostname || "";
const IS_VERCEL_DEMO =
    HOSTNAME === "scoutfootball.vercel.app"
    || HOSTNAME === "scoutfootball-for-world-cup.vercel.app"
    || HOSTNAME.endsWith(".vercel.app");
const API_BASE = window.__SCOUTFOOTBALL_API__
    || (IS_VERCEL_DEMO
        ? "https://scoutfootball-for-world-cup.onrender.com"
        : window.location.origin);
let apiOnline = null; // null=unknown, true=online, false=offline
let usingStaticData = false; // true when static fallback was used

// Team name → filename slug (must match scripts/export_static_frontend_data.py)
function _teamSlug(name) {
    return String(name || "").replace(/\s+/g, "_").replace(/\//g, "_");
}

// Map an API path to a local static JSON file URL.
// Returns null if no static equivalent exists.
function _staticUrlFor(apiPath) {
    const m = (apiPath || "").replace(/^\/+/, "/");
    const map = {
        "/health": "/data/health.json",
        "/artifacts": "/data/artifacts.json",
        "/teams": "/data/teams.json",
        "/teams/strength": "/data/team_strength.json",
        "/ratings": "/data/ratings.json",
        "/ratings/meta": "/data/ratings_meta.json",
        "/ratings/snapshots": "/data/ratings.json",
        "/predictions/meta": "/data/predictions_meta.json",
        "/predictions/calibration": "/data/predictions_calibration.json",
        "/value-summary": "/data/value_summary.json",
        "/action-values": "/data/action_values.json",
        "/review-queue": "/data/review_queue.json",
        "/watchlist": "/data/watchlist.json",
        "/shortlist": "/data/shortlist.json",
        "/model-runs": "/data/model_runs.json",
        "/reports/model-runs": "/data/model_runs.json",
        "/license": "/data/artifacts.json",
        "/players": "/data/players_list.json",
        "/worldcup/teams": "/data/worldcup/teams.json",
        "/world-cup/groups": "/data/worldcup/groups.json",
        "/world-cup/schedule": "/data/worldcup/schedule.json",
        "/world-cup/predictions": "/data/worldcup/predictions.json",
        "/world-cup/match-predictions": "/data/worldcup/match_predictions.json",
        "/world-cup/group-predictions": "/data/worldcup/group_predictions.json",
        "/world-cup/predictions-index": "/data/worldcup/predictions_index.json",
    };
    if (map[m]) return map[m];
    // Squad: /world-cup/squads/<Team Name> → /data/worldcup/squads/<Team_Slug>.json
    const squad = m.match(/^\/world-cup\/squads\/(.+)$/);
    if (squad) return `/data/worldcup/squads/${encodeURIComponent(_teamSlug(decodeURIComponent(squad[1])))}.json`;
    // Player profile: use pre-exported file if available.
    const player = m.match(/^\/players?\/(.+)$/);
    if (player) return `/data/player_profiles/${encodeURIComponent(_teamSlug(decodeURIComponent(player[1])))}.json`;
    // Match predictions: /predictions/<home>/<away> → generic static prediction
    const pred = m.match(/^\/predictions\/.+\/.+$/);
    if (pred) return "/data/predictions_default.json";
    return null;
}

// Fetch JSON with configurable strategy.
// On Vercel demo: static-first (instant load), then optionally refresh from API.
// On local/LAN: API-first with static fallback.
async function fetchJson(apiPath, opts) {
    const params = (opts && opts.params) || "";
    const fetchOpts = opts && opts.fetchOpts ? opts.fetchOpts : undefined;

    // Desktop app: static-first (instant load from bundled data), then refresh from API
    if (IS_VERCEL_DEMO || window.__SCOUTFOOTBALL_DESKTOP__) {
        return _fetchJsonStaticFirst(apiPath, params, fetchOpts);
    }
    return _fetchJsonApiFirst(apiPath, params, fetchOpts);
}

async function _fetchJsonStaticFirst(apiPath, params, fetchOpts) {
    const staticUrl = _staticUrlFor(apiPath);
    if (staticUrl !== null) {
        try {
            const resp = await fetch(staticUrl, fetchOpts);
            if (resp.ok) {
                const data = await resp.json();
                // Don't force apiOnline=false; let health check poll determine status
                _tryRefreshFromApi(apiPath, params, fetchOpts);
                return data;
            }
        } catch (_) { /* static failed, try API below */ }
    }
    return _fetchJsonApiFirst(apiPath, params, fetchOpts);
}

function _tryRefreshFromApi(apiPath, params, fetchOpts) {
    try {
        let url = API_BASE + apiPath;
        if (params && String(params).length > 0) url += `?${params}`;
        fetch(url, { ...fetchOpts, signal: AbortSignal.timeout(8000) })
            .then((resp) => { if (resp.ok) apiOnline = true; })
            .catch(() => {});
    } catch (_) {}
}

async function _fetchJsonApiFirst(apiPath, params, fetchOpts) {
    const apiTimeout = (fetchOpts && fetchOpts.signal) ? undefined : AbortSignal.timeout(5000);

    try {
        let url = API_BASE + apiPath;
        if (params && String(params).length > 0) url += `?${params}`;
        const resp = await fetch(url, { ...fetchOpts, signal: apiTimeout });
        if (resp.ok) {
            apiOnline = true;
            return resp.json();
        }
        // A plain static server returns 404 for API routes. When a tracked
        // static snapshot exists, continue to that fallback instead of
        // treating the 404 as a terminal API error.
        if (resp.status >= 400 && resp.status < 500 && _staticUrlFor(apiPath) === null) {
            throw new Error(`HTTP ${resp.status}`);
        }
    } catch (err) {
        if (err.message && /^HTTP [4]\d\d$/.test(err.message)) throw err;
    }

    const staticUrl = _staticUrlFor(apiPath);
    if (staticUrl !== null) {
        try {
            const resp = await fetch(staticUrl, fetchOpts);
            if (resp.ok) {
                apiOnline = false;
                usingStaticData = true;
                return resp.json();
            }
        } catch (_) {}
    }

    apiOnline = false;
    usingStaticData = false;
    throw new Error("api_and_static_unavailable");
}

let players = [];
let reviews = [];
let matches = [];
let ratingsMeta = { model_meta: {}, league_metrics: [] };
let artifactSummary = { data_health: {}, artifacts: [] };
let predictionMeta = { status: "no_data" };
let predictionCalibration = {};
let valueSummaryMeta = { sample_count: 0, metrics: {} };
let modelRuns = { count: 0, runs: [] };
let watchlistData = [];
let shortlistData = [];
let actionValueSummary = { status: "no_data", players: [], metrics: {} };
let teamStrengthData = { count: 0, teams: [] };
let dataLoadErrors = new Set(); // tracks which data sources failed to load

async function fetchRatings(position, league) {
    const params = new URLSearchParams();
    if (position && position !== "ALL") params.set("position", position);
    if (league) params.set("league", league);
    params.set("limit", "3000");
    try {
        const data = await fetchJson("/ratings", { params });
        const rawPlayers = (data.players || []).map((p) => ({
            name: p.player || "",
            position: p.position_group || "",
            team: p.team || "",
            league: p.league || "",
            season: p.season || "",
            key: `${p.player || ""}|${p.season || ""}|${p.team || ""}`,
            rating: +(p.optimized_score || 0).toFixed(1),
            confidence: (p.confidence_level || "LOW").toUpperCase(),
            minutes: Math.round(p.minutes || 0),
            matches: Math.round(p.matches || 0),
            low_appearance: !!p.low_appearance,
            npg_p90: +(p.npg_p90 || 0).toFixed(3),
            assists_p90: +(p.assists_p90 || 0).toFixed(3),
            defense_composite: p.defense_composite,
            possession_composite: p.possession_composite,
            value: 0,
            residual: 0,
        }));

        // Compute position-relative percentiles client-side for radar
        const byPosition = {};
        for (const p of rawPlayers) {
            if (!byPosition[p.position]) byPosition[p.position] = [];
            byPosition[p.position].push(p);
        }
        function pctRank(value, arr, key) {
            const vals = arr.map((p) => p[key]).filter((v) => v != null && !isNaN(v)).sort((a, b) => a - b);
            if (vals.length === 0) return 50;
            const idx = vals.filter((v) => v < value).length;
            return Math.round(idx / vals.length * 100);
        }
        for (const p of rawPlayers) {
            const pool = byPosition[p.position] || [];
            const attack = (p.npg_p90 || 0) + (p.assists_p90 || 0);
            const attackPool = pool.map((x) => (x.npg_p90 || 0) + (x.assists_p90 || 0));
            const attackPct = attackPool.length > 0 ? Math.round(attackPool.filter((v) => v < attack).length / attackPool.length * 100) : 50;
            p.percentile = pctRank(p.rating, pool, "rating");
            p.radar = [
                attackPct,
                p.possession_composite != null ? pctRank(p.possession_composite, pool, "possession_composite") : 50,
                p.defense_composite != null ? pctRank(p.defense_composite, pool, "defense_composite") : 50,
                Math.min(100, Math.round((p.minutes || 0) / 2700 * 100)),
                p.percentile,
            ];
        }
        return rawPlayers;
    } catch (err) {
        console.warn("Failed to fetch ratings:", err);
        dataLoadErrors.add("ratings");
        return getDemoPlayers();
    }
}

function getDemoPlayers() {
    /* Fallback: no demo data — API must be online for player ratings */
    return [];
}

async function fetchRatingsMeta() {
    try {
        const data = await fetchJson("/ratings/meta");
        return data;
    } catch (err) {
        console.warn("Failed to fetch ratings meta:", err);
        return { model_meta: {}, league_metrics: [] };
    }
}

async function fetchArtifacts() {
    try {
        return await fetchJson("/artifacts");
    } catch (err) {
        console.warn("Failed to fetch artifacts:", err);
        return {};
    }
}

async function fetchTeams() {
    try {
        const data = await fetchJson("/teams");
        return data.teams || [];
    } catch (err) {
        console.warn("Failed to fetch teams:", err);
        return [];
    }
}

async function fetchTeamStrength(league) {
    const params = new URLSearchParams();
    if (league) params.set("league", league);
    params.set("limit", "200");
    try {
        const data = await fetchJson("/teams/strength", { params });
        return data;
    } catch (err) {
        console.warn("Failed to fetch team strength:", err);
        return { count: 0, teams: [] };
    }
}

async function fetchPrediction(homeTeam, awayTeam) {
    try {
        const data = await fetchJson(`/predictions/${encodeURIComponent(homeTeam)}/${encodeURIComponent(awayTeam)}`);
        if (data) {
            data.home_team = data.home_team || homeTeam;
            data.away_team = data.away_team || awayTeam;
        }
        return data;
    } catch {
        return null;
    }
}

async function fetchPredictionMeta() {
    try {
        return await fetchJson("/predictions/meta");
    } catch (err) {
        console.warn("Failed to fetch prediction meta:", err);
        return { status: "no_data" };
    }
}

async function fetchModelRuns() {
    try {
        return await fetchJson("/reports/model-runs");
    } catch (err) {
        console.warn("Failed to fetch model runs:", err);
        return { count: 0, runs: [] };
    }
}

async function fetchActionValues() {
    try {
        return await fetchJson("/action-values");
    } catch (err) {
        console.warn("Failed to fetch action values:", err);
        dataLoadErrors.add("action-values");
        return { status: "no_data", players: [], metrics: {} };
    }
}

let licenseData = { license_attribution: {}, data_source_label: "", updated_at: null };

const LICENSE_SOURCES = [
    { key: "statsbomb", name: "StatsBomb Open Data", license: "MIT / CC-BY-SA 4.0", attribution: "\u25C6 Required on public charts", url: "https://github.com/statsbomb/open-data" },
    { key: "football_data", name: "Football-Data.co.uk", license: "Free (non-commercial)", attribution: "Attribution appreciated", url: "https://www.football-data.co.uk" },
    { key: "fbref", name: "FBref", license: "Restricted (personal research)", attribution: "No redistribution", url: "https://fbref.com" },
    { key: "understat", name: "Understat", license: "Public", attribution: "Attribution appreciated", url: "https://understat.com" },
    { key: "club_elo", name: "Club Elo", license: "Public", attribution: "Attribution appreciated", url: "https://clubelo.com" },
    { key: "transfermarkt", name: "Transfermarkt", license: "Manual import only", attribution: "No automated scraping", url: "https://www.transfermarkt.com" },
];

async function fetchLicense() {
    try {
        return await fetchJson("/license");
    } catch (err) {
        console.warn("Failed to fetch license info:", err);
        return { license_attribution: {}, data_source_label: "", updated_at: null };
    }
}

let teamList = [];

function getTeams() {
    return teamList.length > 0 ? teamList : Array.from(new Set(matches.flatMap((match) => [match.home, match.away]))).sort();
}

const appState = {
    lang: "zh",
    view: "overview",
    selectedPlayerKey: "",
    position: "ALL",
    season: "ALL",
    league: "ALL",
    valueMode: "under",
    valuePriceBand: "all",
    home: "Arsenal",
    away: "Barcelona",
    charts: {},
    playerPage: 1,
    playerPageSize: 50,
    playerSortCol: "rating",
    playerSortAsc: false,
    compareKeys: [],
    scoutingQuery: "",
    scoutingStatus: "ALL",
    actionMode: "xt",
    actionQuery: "",
    actionCompetition: "ALL",
    actionMinMinutes: 450,
};

function t(key) {
    return i18n[appState.lang][key] || key;
}

function escapeHtml(value) {
    return String(value ?? "").replace(/[&<>"']/g, (char) => ({
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        "\"": "&quot;",
        "'": "&#39;",
    }[char]));
}

function escapeAttr(value) {
    return escapeHtml(value).replace(/`/g, "&#96;");
}

function sanitizeCssPercent(value) {
    const n = Number(value);
    if (!Number.isFinite(n)) return 0;
    return Math.max(0, Math.min(100, Math.round(n)));
}

function csvCell(value) {
    const raw = String(value ?? "");
    const safe = /^[=+\-@\t\r]/.test(raw) ? `'${raw}` : raw;
    return `"${safe.replace(/"/g, '""')}"`;
}

function safeNum(value, decimals) {
    const n = Number(value);
    if (!Number.isFinite(n)) return "–";
    return n.toFixed(decimals != null ? decimals : 1);
}

async function fetchPredictionCalibration() {
    try {
        return await fetchJson("/predictions/calibration");
    } catch (err) {
        console.warn("Failed to fetch prediction calibration:", err);
        return {};
    }
}

function formatTimestamp(value) {
    if (value == null || value === "") return "";
    const numeric = Number(value);
    const date = Number.isFinite(numeric)
        ? new Date(numeric < 1e12 ? numeric * 1000 : numeric)
        : new Date(value);
    if (Number.isNaN(date.getTime())) return String(value);
    return date.toLocaleString(appState.lang === "zh" ? "zh-CN" : "en-US", {
        year: "numeric",
        month: "short",
        day: "numeric",
        hour: "2-digit",
        minute: "2-digit",
    });
}

function confidenceClass(confidence) {
    if (confidence === "HIGH") return "status-high";
    if (confidence === "MEDIUM") return "status-medium";
    return "status-low";
}

function applyLocale() {
    document.documentElement.lang = appState.lang === "zh" ? "zh-CN" : "en";
    document.querySelectorAll("[data-i18n]").forEach((element) => {
        element.textContent = t(element.dataset.i18n);
    });
    document.querySelectorAll("[data-i18n-placeholder]").forEach((element) => {
        element.placeholder = t(element.dataset.i18nPlaceholder);
    });
    document.getElementById("lang-toggle").textContent = appState.lang === "zh" ? "EN" : "中";
}

async function setView(view) {
    appState.view = view;
    document.querySelectorAll(".view").forEach((element) => {
        element.classList.toggle("active", element.id === `view-${view}`);
    });
    document.querySelectorAll(".nav-action[data-view]").forEach((button) => {
        button.classList.toggle("active", button.dataset.view === view);
    });
    requestAnimationFrame(renderActiveView);
}

function filteredPlayers() {
    const query = document.getElementById("global-search").value.trim().toLowerCase();
    return players.filter((player) => {
        const matchesPosition = appState.position === "ALL" || player.position === appState.position;
        const matchesSeason = appState.season === "ALL" || player.season === appState.season;
        const matchesLeague = appState.league === "ALL" || player.league === appState.league;
        const matchesQuery = !query || [player.name, player.team, player.position].join(" ").toLowerCase().includes(query);
        return matchesPosition && matchesSeason && matchesLeague && matchesQuery;
    });
}

function renderPlayers() {
    const sorted = filteredPlayers().sort((a, b) => {
        const col = appState.playerSortCol;
        const dir = appState.playerSortAsc ? 1 : -1;
        if (col === "rating") return dir * (a.rating - b.rating);
        const va = String(a[col] || "").toLowerCase();
        const vb = String(b[col] || "").toLowerCase();
        return dir * va.localeCompare(vb);
    });
    const total = sorted.length;
    const pageSize = appState.playerPageSize;
    const totalPages = Math.max(1, Math.ceil(total / pageSize));
    appState.playerPage = Math.min(appState.playerPage, totalPages);
    const start = (appState.playerPage - 1) * pageSize;
    const rows = sorted.slice(start, start + pageSize);
    const tbody = document.getElementById("player-table");
    if (players.length === 0) {
        tbody.innerHTML = '<tr><td colspan="8" style="text-align:center;color:var(--text-muted)">Loading...</td></tr>';
        return;
    }
    tbody.innerHTML = rows.map((player, i) => {
        const index = start + i;
        const lowAppBadge = player.low_appearance
            ? `<span class="status-pill low-appearance" title="${appState.lang === 'zh' ? '出场不足20场，评分已扣减' : 'Under 20 matches, score penalized'}">${appState.lang === 'zh' ? '低出场' : 'LOW APP'}</span>`
            : '';
        return `
        <tr class="${player.key === appState.selectedPlayerKey ? "selected" : ""}${player.low_appearance ? " low-appearance-row" : ""}" data-player-key="${escapeAttr(player.key)}" style="cursor:pointer">
            <td>${index + 1}</td>
            <td>${escapeHtml(player.name)}${lowAppBadge}</td>
            <td>${escapeHtml(player.position)}</td>
            <td>${escapeHtml(player.team)}</td>
            <td>${escapeHtml(player.season)}</td>
            <td>${player.rating.toFixed(1)}</td>
            <td><span class="status-pill ${confidenceClass(player.confidence)}">${escapeHtml(player.confidence)}</span></td>
            <td class="actions-cell">
                <button class="action-btn${isInPlayerWatchlist(player.key) ? ' active' : ''}" data-action-watch="${escapeAttr(player.key)}" title="${escapeHtml(t('action_watchlist'))}" type="button">\u25A1</button>
                <button class="action-btn${isInPlayerShortlist(player.key) ? ' active' : ''}" data-action-short="${escapeAttr(player.key)}" title="${escapeHtml(t('action_shortlist'))}" type="button">\u25B3</button>
                <button class="action-btn${appState.compareKeys.includes(player.key) ? ' active' : ''}" data-action-compare="${escapeAttr(player.key)}" title="${escapeHtml(t('action_compare'))}" type="button">\u27F7</button>
                <button class="action-btn" data-action-tactical="${escapeAttr(player.key)}" title="${escapeHtml(t('action_tactical'))}" type="button">\u25CE</button>
            </td>
        </tr>`;
    }).join("");

    tbody.querySelectorAll("tr[data-player-key]").forEach((row) => {
        row.addEventListener("click", () => {
            appState.selectedPlayerKey = row.dataset.playerKey;
            renderPlayers();
            renderPlayerProfile();
        });
    });

    // Action button handlers
    tbody.querySelectorAll("[data-action-watch]").forEach((btn) => {
        btn.addEventListener("click", (e) => {
            e.stopPropagation();
            const playerKey = btn.dataset.actionWatch;
            const player = players.find((p) => p.key === playerKey);
            if (player) togglePlayerWatchlist(player);
            renderPlayers();
        });
    });
    tbody.querySelectorAll("[data-action-short]").forEach((btn) => {
        btn.addEventListener("click", (e) => {
            e.stopPropagation();
            const playerKey = btn.dataset.actionShort;
            const player = players.find((p) => p.key === playerKey);
            if (player) togglePlayerShortlist(player);
            renderPlayers();
        });
    });
    tbody.querySelectorAll("[data-action-tactical]").forEach((btn) => {
        btn.addEventListener("click", (e) => {
            e.stopPropagation();
            const playerKey = btn.dataset.actionTactical;
            const player = players.find((p) => p.key === playerKey);
            if (player) sendToTacticalBoard(player);
        });
    });
    tbody.querySelectorAll("[data-action-compare]").forEach((btn) => {
        btn.addEventListener("click", (e) => {
            e.stopPropagation();
            const playerKey = btn.dataset.actionCompare;
            const idx = appState.compareKeys.indexOf(playerKey);
            if (idx >= 0) {
                appState.compareKeys.splice(idx, 1);
            } else {
                if (appState.compareKeys.length >= 2) appState.compareKeys.shift();
                appState.compareKeys.push(playerKey);
            }
            renderPlayers();
            renderComparePanel();
        });
    });

    // Pagination controls
    const pageInfo = document.getElementById("player-page-info");
    const pageNum = document.getElementById("player-page-num");
    if (pageInfo) pageInfo.textContent = `${total} ${appState.lang === 'zh' ? '名球员' : 'players'}`;
    if (pageNum) pageNum.textContent = `${appState.playerPage}/${totalPages}`;
    const prevBtn = document.getElementById("player-prev-page");
    const nextBtn = document.getElementById("player-next-page");
    if (prevBtn) prevBtn.disabled = appState.playerPage <= 1;
    if (nextBtn) nextBtn.disabled = appState.playerPage >= totalPages;

    // Update sort indicators on headers
    document.querySelectorAll("th[data-sort]").forEach((th) => {
        const isActive = th.dataset.sort === appState.playerSortCol;
        const arrow = isActive ? (appState.playerSortAsc ? " ▲" : " ▼") : "";
        const baseText = th.getAttribute("data-i18n") ? t(th.getAttribute("data-i18n")) : th.textContent.replace(/[▲▼]/g, "").trim();
        th.textContent = baseText + arrow;
    });

    if (!rows.some((player) => player.key === appState.selectedPlayerKey) && rows[0]) {
        appState.selectedPlayerKey = rows[0].key;
    }
    renderPlayerProfile();
    renderComparePanel();
}

async function renderPlayerProfile() {
    const player = players.find((item) => item.key === appState.selectedPlayerKey) || players[0];
    if (!player) return;
    document.getElementById("selected-player-name").textContent = player.name;

    // Fetch real profile data for radar
    let profile = null;
    try {
        profile = await fetchJson(`/players/${encodeURIComponent(player.name)}?season=${player.season}`);
    } catch (err) { /* fallback to list data */ }

    const detailMinutes = profile ? profile.minutes : player.minutes;
    const detailScore = profile ? profile.optimized_score : player.rating;
    const detailPosition = profile ? profile.position_group : player.position;
    const detailMatches = profile ? profile.matches : player.matches;
    const detailLowApp = profile ? profile.low_appearance : player.low_appearance;
    const detailConfidence = profile ? profile.confidence_level : player.confidence;
    const detailLeague = profile ? profile.league : player.league;
    const lowAppWarning = detailLowApp
        ? `<div class="low-appearance-warning">${appState.lang === "zh" ? "▲ 出场不足20场，评分已扣减最多30%" : "▲ Under 20 matches, score penalized up to 30%"}</div>`
        : "";
    document.getElementById("player-detail").innerHTML = `
        <div><span>${escapeHtml(t("th_team"))}</span><strong>${escapeHtml(player.team)}</strong></div>
        <div><span>${escapeHtml(t("minutes"))}</span><strong>${escapeHtml(detailMinutes)}</strong></div>
        <div><span>${appState.lang === "zh" ? "出场" : "Matches"}</span><strong>${escapeHtml(detailMatches)}</strong></div>
        <div><span>${escapeHtml(t("th_pos"))}</span><strong>${escapeHtml(detailPosition)}</strong></div>
        <div><span>${escapeHtml(t("th_rating"))}</span><strong>${escapeHtml(detailScore)}</strong></div>
        <div><span>${appState.lang === "zh" ? "联赛" : "League"}</span><strong>${escapeHtml(detailLeague || "–")}</strong></div>
        ${/* Season trend */ (() => {
            const trend = profile ? (profile.season_trend || profile.rating_trend || null) : null;
            if (!trend) return '';
            const trendDir = typeof trend === 'string' ? trend : (trend > 0 ? 'up' : trend < 0 ? 'down' : 'stable');
            const trendSym = trendDir === 'up' ? '\u25B2' : trendDir === 'down' ? '\u25BC' : '\u25CB';
            const trendColor = trendDir === 'up' ? '#57d68d' : trendDir === 'down' ? '#ff6b6b' : 'var(--text-muted)';
            const trendLabel = appState.lang === 'zh' ? '赛季趋势' : 'Season trend';
            return `<div><span>${escapeHtml(trendLabel)}</span><strong style="color:${trendColor}">${trendSym} ${escapeHtml(trendDir)}</strong></div>`;
        })()}
        ${/* Confidence reason */ (() => {
            const reason = profile ? (profile.confidence_reason || profile.confidence_detail || '') : '';
            if (!reason) return '';
            const label = t('confidence_reason_label');
            return `<div><span>${escapeHtml(label)}</span><strong style="color:var(--text-muted);font-size:0.82rem">${escapeHtml(reason)}</strong></div>`;
        })()}
        ${/* xT summary */ (() => {
            const xt = profile ? profile.xt_summary : null;
            if (!xt || !xt.available) {
                const label = t('xT_not_available');
                return `<div><span>${escapeHtml(t('xT_label'))}</span><strong style="color:var(--text-muted);font-size:0.82rem">N/A - ${escapeHtml(label)}</strong></div>`;
            }
            const parts = [];
            if (xt.xT_per_90 != null) parts.push(`${escapeHtml(t('xT_label'))}: ${escapeHtml(String(xt.xT_per_90))}`);
            if (xt.xT_percentile != null) parts.push(`${escapeHtml(t('xT_percentile'))}: ${escapeHtml(String(xt.xT_percentile))}pct`);
            if (xt.xT_contribution != null) parts.push(`${escapeHtml(t('xT_contribution'))}: ${escapeHtml(String(xt.xT_contribution))}`);
            if (parts.length === 0) return '';
            const note = xt.coverage_note ? ` (${escapeHtml(xt.coverage_note)})` : '';
            return `<div><span>${escapeHtml(t('xT_label'))}</span><strong style="font-size:0.82rem">${parts.join(' | ')}${note}</strong></div>`;
        })()}
        ${/* Rating snapshot history */ (() => {
            const seasons = profile ? (profile.seasons || []) : [];
            if (seasons.length < 2) return '';
            const label = t('rating_snapshot');
            const dots = seasons.map(s => `${escapeHtml(String(s.season))}: ${escapeHtml(String(s.optimized_score))}`).join(', ');
            return `<div><span>${escapeHtml(label)}</span><strong style="font-size:0.82rem;color:var(--text-muted)">${dots}</strong></div>`;
        })()}
        ${/* Data sources */ (() => {
            const sources = profile ? (profile.data_sources || profile.sources || []) : [];
            if (!sources || sources.length === 0) return '';
            const label = appState.lang === 'zh' ? '数据来源' : 'Data sources';
            return `<div><span>${escapeHtml(label)}</span><strong>${escapeHtml(sources.join(', '))}</strong></div>`;
        })()}
        ${/* Position percentile */ (() => {
            const pct = profile ? (profile.position_percentile ?? profile.percentile_rank ?? null) : null;
            if (pct == null) return '';
            const label = appState.lang === 'zh' ? '位置百分位' : 'Position percentile';
            return `<div><span>${escapeHtml(label)}</span><strong>\u25C6 ${escapeHtml(String(Math.round(pct)))}pct</strong></div>`;
        })()}
        ${/* Missing fields */ (() => {
            const missing = [];
            if (profile && profile.has_defense === false) missing.push('defense');
            if (profile && profile.has_possession === false) missing.push('possession');
            if (profile && profile.has_shooting === false) missing.push('shooting');
            if (profile && profile.has_passing === false) missing.push('passing');
            if (profile && profile.has_gk === false) missing.push('gk');
            if (missing.length === 0) return '';
            const label = appState.lang === 'zh' ? '缺失字段' : 'Missing fields';
            return `<div><span>${escapeHtml(label)}</span><strong style="color:#ff6b6b">\u25CB ${escapeHtml(missing.join(', '))}</strong></div>`;
        })()}
        ${/* Watchlist/Shortlist notes */ (() => {
            const wlNote = watchlistNotes[player.name] || "";
            const slNote = scoutShortlistNotes[player.name] || "";
            if (!wlNote && !slNote) return "";
            const label = appState.lang === "zh" ? "球探备注" : "Scout notes";
            let noteHtml = "";
            if (wlNote) noteHtml += (appState.lang === "zh" ? "观察: " : "Watch: ") + escapeHtml(wlNote);
            if (slNote) noteHtml += (noteHtml ? " | " : "") + (appState.lang === "zh" ? "候选: " : "Short: ") + escapeHtml(slNote);
            return `<div><span>${escapeHtml(label)}</span><strong style="font-size:0.82rem;color:var(--text-muted)">${noteHtml}</strong></div>`;
        })()}
    `;
    // Always remove existing warning before conditionally inserting new one
    const existing = document.getElementById("player-detail").nextElementSibling;
    if (existing && existing.classList && existing.classList.contains("low-appearance-warning")) {
        existing.remove();
    }
    if (lowAppWarning) {
        document.getElementById("player-detail").insertAdjacentHTML("afterend", lowAppWarning);
    }

    // Use real radar data from profile API, or fallback to defaults
    const radar = (profile && profile.radar) ? profile.radar : player.radar;
    renderRadar({ ...player, radar });

    // Update confidence badge with profile data if available
    const confidence = profile ? (profile.confidence_level || player.confidence) : player.confidence;
    const badge = document.getElementById("player-confidence");
    if (badge) {
        badge.textContent = confidence;
        badge.className = `status-pill ${confidenceClass(confidence)}`;
    }

    // Send to tactical board button
    const tacticalActionsEl = document.getElementById("player-tactical-actions");
    if (tacticalActionsEl) {
        const zT = appState.lang === 'zh';
        tacticalActionsEl.innerHTML = `<button class="text-button" id="btn-send-tactical" type="button" style="font-size:0.82rem;padding:0.3rem 0.6rem">\u25C6 ${zT ? '发送到战术板' : 'Send to tactical board'}</button> <button class="text-button" id="btn-export-csv" type="button" style="font-size:0.82rem;padding:0.3rem 0.6rem">${zT ? '导出 CSV' : 'Export CSV'}</button>`;
        const sendBtn = document.getElementById("btn-send-tactical");
        if (sendBtn) {
            sendBtn.addEventListener("click", () => {
                // Create or get tactical project
                if (!tacticalProject) {
                    tacticalProject = TACTICAL_BOARD.createProject("ScoutFootball \u6218\u672f\u677f");
                }
                // Add player to tactical board
                const playerObj = {
                    type: "player",
                    x: 50,
                    y: 50,
                    radius: 3,
                    color: "#4a90d9",
                    label: escapeHtml(player.name),
                    number: String(Math.round(detailScore || player.rating || 0)),
                    rating: detailScore || player.rating || null,
                    team: player.team || "",
                    position: detailPosition || player.position || "",
                };
                tacticalProject.objects = tacticalProject.objects || [];
                tacticalProject.objects.push(playerObj);
                // Switch to tactical view
                setView("tactical");
            });
        }
        const csvBtn = document.getElementById("btn-export-csv");
        if (csvBtn) {
            csvBtn.addEventListener("click", () => {
                exportPlayerProfileCSV(player, profile, detailScore, detailPosition, detailMinutes, detailMatches, detailConfidence, detailLeague);
            });
        }
    }
}

function exportPlayerProfileCSV(player, profile, detailScore, detailPosition, detailMinutes, detailMatches, detailConfidence, detailLeague) {
    const radar = (profile && profile.radar) ? profile.radar : (player.radar || []);
    const radarLabels = ["Attack", "Possession", "Defense", "Volume", "Overall"];
    const header = [
        "name", "team", "position", "rating", "confidence", "season",
        "minutes", "matches", "league",
        ...radarLabels.map(l => `radar_${l.toLowerCase()}`),
    ];
    const row = [
        player.name,
        player.team,
        detailPosition,
        detailScore,
        detailConfidence,
        player.season,
        detailMinutes,
        detailMatches,
        detailLeague || "",
        ...radar.map(v => v != null ? Math.round(v) : ""),
    ];
    const csv = [header, row].map(r => r.map(csvCell).join(",")).join("\n");
    const blob = new Blob(["\uFEFF" + csv], { type: "text/csv;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = `${(player.name || "player").replace(/[^a-zA-Z0-9\u4e00-\u9fff_-]/g, "_")}_profile.csv`;
    link.click();
    URL.revokeObjectURL(url);
}

function getChart(id) {
    if (!window.echarts) {
        const element = document.getElementById(id);
        if (element && !element.textContent) element.textContent = "Chart runtime unavailable.";
        return null;
    }
    const element = document.getElementById(id);
    if (!element) return null;
    // Don't init on hidden containers - will have zero dimensions
    if (element.offsetParent === null) return null;
    const existing = appState.charts[id];
    if (existing) {
        try {
            if (existing.isDisposed && existing.isDisposed()) {
                delete appState.charts[id];
            } else if (existing.getDom && existing.getDom() !== element) {
                existing.dispose();
                delete appState.charts[id];
            }
        } catch {
            delete appState.charts[id];
        }
    }
    if (!appState.charts[id]) {
        const adopted = echarts.getInstanceByDom(element);
        appState.charts[id] = adopted || echarts.init(element);
    }
    return appState.charts[id];
}

function chartTextColor() {
    return document.body.classList.contains("dark-mode") ? "rgba(247,248,251,.68)" : "rgba(21,23,28,.65)";
}

function chartGridColor() {
    return document.body.classList.contains("dark-mode") ? "rgba(247,248,251,.13)" : "rgba(21,23,28,.12)";
}

function renderRadar(player) {
    const chart = getChart("radar-chart");
    if (!chart) return;
    chart.setOption({
        radar: {
            indicator: [
                { name: appState.lang === "zh" ? "进攻" : "Attack", max: 100 },
                { name: appState.lang === "zh" ? "控球" : "Possession", max: 100 },
                { name: appState.lang === "zh" ? "防守" : "Defense", max: 100 },
                { name: appState.lang === "zh" ? "可靠性" : "Reliability", max: 100 },
                { name: appState.lang === "zh" ? "影响力" : "Impact", max: 100 },
            ],
            shape: "circle",
            axisName: { color: chartTextColor(), fontWeight: 700 },
            splitLine: { lineStyle: { color: chartGridColor() } },
            axisLine: { lineStyle: { color: chartGridColor() } },
            splitArea: { show: false },
        },
        series: [{
            type: "radar",
            data: [{
                value: player.radar,
                name: player.name,
                areaStyle: { color: "rgba(255,255,255,.08)" },
                lineStyle: { color: chartTextColor(), width: 2 },
                itemStyle: { color: chartTextColor() },
            }],
        }],
    });
    requestAnimationFrame(() => {
        chart.resize();
        // Second resize after paint to catch any late layout shifts
        requestAnimationFrame(() => chart.resize());
    });
}

function renderComparePanel() {
    const panel = document.getElementById("compare-panel");
    if (!panel) return;
    const z = appState.lang === "zh";

    if (appState.compareKeys.length < 2) {
        panel.innerHTML = `<div style="text-align:center;color:var(--text-muted);padding:1.5rem 0;font-size:0.85rem">${escapeHtml(t("compare_select_hint"))}</div>`;
        return;
    }

    const p1 = players.find((p) => p.key === appState.compareKeys[0]);
    const p2 = players.find((p) => p.key === appState.compareKeys[1]);
    if (!p1 || !p2) {
        panel.innerHTML = `<div style="text-align:center;color:var(--text-muted);padding:1.5rem 0;font-size:0.85rem">${escapeHtml(t("compare_select_hint"))}</div>`;
        return;
    }

    const radarLabels = [
        z ? "进攻" : "Attack",
        z ? "控球" : "Possession",
        z ? "防守" : "Defense",
        z ? "可靠性" : "Reliability",
        z ? "影响力" : "Impact",
    ];

    // Info cards
    let html = `<div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:0.8rem;gap:0.5rem">`;
    html += `<div style="flex:1;text-align:center;padding:0.4rem 0.6rem;border-radius:8px;background:rgba(74,144,217,.12)">`;
    html += `<div style="font-weight:700;font-size:0.95rem">${escapeHtml(p1.name)}</div>`;
    html += `<div style="font-size:0.78rem;color:var(--text-muted)">${escapeHtml(p1.team)} · ${escapeHtml(p1.position)}</div>`;
    html += `<div style="font-size:1.1rem;font-weight:700;margin-top:0.2rem">${p1.rating.toFixed(1)}</div>`;
    html += `</div>`;
    html += `<div style="flex:0 0 auto;align-self:center;font-size:0.8rem;color:var(--text-muted);font-weight:700">VS</div>`;
    html += `<div style="flex:1;text-align:center;padding:0.4rem 0.6rem;border-radius:8px;background:rgba(255,159,67,.12)">`;
    html += `<div style="font-weight:700;font-size:0.95rem">${escapeHtml(p2.name)}</div>`;
    html += `<div style="font-size:0.78rem;color:var(--text-muted)">${escapeHtml(p2.team)} · ${escapeHtml(p2.position)}</div>`;
    html += `<div style="font-size:1.1rem;font-weight:700;margin-top:0.2rem">${p2.rating.toFixed(1)}</div>`;
    html += `</div>`;
    html += `</div>`;

    // Position mismatch warning
    if (p1.position !== p2.position) {
        html += `<div style="font-size:0.72rem;color:#ff9f43;margin-bottom:0.5rem;text-align:center">${escapeHtml(t("compare_no_same_pos"))}</div>`;
    }

    // Radar chart container
    html += `<div id="compare-radar-chart" class="chart-box" style="height:260px"></div>`;

    // Percentile comparison table
    html += `<div style="margin-top:0.6rem;overflow-x:auto"><table style="width:100%;font-size:0.78rem;border-collapse:collapse">`;
    html += `<thead><tr style="border-bottom:1px solid var(--glass-border)">`;
    html += `<th style="text-align:left;padding:0.3rem 0.4rem;color:var(--text-muted)">${escapeHtml(t("compare_dimension"))}</th>`;
    html += `<th style="text-align:center;padding:0.3rem 0.4rem">${escapeHtml(p1.name)}</th>`;
    html += `<th style="text-align:center;padding:0.3rem 0.4rem">${escapeHtml(p2.name)}</th>`;
    html += `<th style="text-align:center;padding:0.3rem 0.4rem">${z ? "差值" : "Diff"}</th>`;
    html += `</tr></thead><tbody>`;

    const r1 = p1.radar || [50, 50, 50, 50, 50];
    const r2 = p2.radar || [50, 50, 50, 50, 50];
    for (let i = 0; i < radarLabels.length; i++) {
        const v1 = r1[i] ?? 0;
        const v2 = r2[i] ?? 0;
        const diff = v1 - v2;
        const diffColor = diff > 0 ? "#57d68d" : diff < 0 ? "#ff6b6b" : "var(--text-muted)";
        html += `<tr style="border-bottom:1px solid rgba(255,255,255,.05)">`;
        html += `<td style="padding:0.3rem 0.4rem">${escapeHtml(radarLabels[i])}</td>`;
        html += `<td style="text-align:center;padding:0.3rem 0.4rem">${Math.round(v1)}pct</td>`;
        html += `<td style="text-align:center;padding:0.3rem 0.4rem">${Math.round(v2)}pct</td>`;
        html += `<td style="text-align:center;padding:0.3rem 0.4rem;color:${diffColor}">${diff > 0 ? "+" : ""}${Math.round(diff)}</td>`;
        html += `</tr>`;
    }

    // Extra metrics rows
    const extraMetrics = [
        { label: z ? "非点球进球/90" : "NPG p90", k: "npg_p90" },
        { label: z ? "助攻/90" : "Assists p90", k: "assists_p90" },
        { label: z ? "分钟" : "Minutes", k: "minutes" },
        { label: z ? "出场" : "Matches", k: "matches" },
    ];
    for (const m of extraMetrics) {
        const v1 = p1[m.k] ?? 0;
        const v2 = p2[m.k] ?? 0;
        const diff = v1 - v2;
        const diffColor = diff > 0 ? "#57d68d" : diff < 0 ? "#ff6b6b" : "var(--text-muted)";
        html += `<tr style="border-bottom:1px solid rgba(255,255,255,.05)">`;
        html += `<td style="padding:0.3rem 0.4rem">${escapeHtml(m.label)}</td>`;
        html += `<td style="text-align:center;padding:0.3rem 0.4rem">${typeof v1 === "number" ? (m.k === "npg_p90" || m.k === "assists_p90" ? v1.toFixed(3) : v1) : escapeHtml(String(v1))}</td>`;
        html += `<td style="text-align:center;padding:0.3rem 0.4rem">${typeof v2 === "number" ? (m.k === "npg_p90" || m.k === "assists_p90" ? v2.toFixed(3) : v2) : escapeHtml(String(v2))}</td>`;
        html += `<td style="text-align:center;padding:0.3rem 0.4rem;color:${diffColor}">${diff > 0 ? "+" : ""}${(m.k === "npg_p90" || m.k === "assists_p90") ? diff.toFixed(3) : Math.round(diff)}</td>`;
        html += `</tr>`;
    }

    html += `</tbody></table></div>`;

    // Clear button
    html += `<div style="text-align:center;margin-top:0.6rem"><button class="text-button" id="btn-clear-compare" type="button" style="font-size:0.78rem;padding:0.25rem 0.6rem">${escapeHtml(t("compare_clear"))}</button></div>`;

    panel.innerHTML = html;

    // Render comparison radar
    requestAnimationFrame(() => {
        const chartEl = document.getElementById("compare-radar-chart");
        if (chartEl && window.echarts) {
            const chart = echarts.init(chartEl);
            appState.charts["compare-radar-chart"] = chart;
            chart.setOption({
                radar: {
                    indicator: radarLabels.map((name) => ({ name, max: 100 })),
                    shape: "circle",
                    axisName: { color: chartTextColor(), fontWeight: 700, fontSize: 11 },
                    splitLine: { lineStyle: { color: chartGridColor() } },
                    axisLine: { lineStyle: { color: chartGridColor() } },
                    splitArea: { show: false },
                },
                series: [{
                    type: "radar",
                    data: [
                        {
                            value: r1,
                            name: p1.name,
                            areaStyle: { color: "rgba(74,144,217,.18)" },
                            lineStyle: { color: "#4a90d9", width: 2 },
                            itemStyle: { color: "#4a90d9" },
                        },
                        {
                            value: r2,
                            name: p2.name,
                            areaStyle: { color: "rgba(255,159,67,.18)" },
                            lineStyle: { color: "#ff9f43", width: 2 },
                            itemStyle: { color: "#ff9f43" },
                        },
                    ],
                }],
            });
            requestAnimationFrame(() => chart.resize());
        }

        // Clear button handler
        const clearBtn = document.getElementById("btn-clear-compare");
        if (clearBtn) {
            clearBtn.addEventListener("click", () => {
                appState.compareKeys = [];
                renderPlayers();
                renderComparePanel();
            });
        }
    });
}

let valuePlayers = [];
let valueStratification = {};

// No mock value data — API must be online for value report

async function fetchValueReport() {
    try {
        const data = await fetchJson("/value-summary");
        valueSummaryMeta = data;
        // Prefer dedicated stratification fields, fall back to nested
        // structure from newer API payloads.
        if (data && typeof data === "object") {
            valueStratification = data.stratification || {};
        }
        if (data.players && data.players.length > 0) {
            return data.players.map((p) => ({
                name: p.player || "",
                team: p.team || "",
                season: p.season || "",
                league: p.league || "",
                positionGroup: p.position_group || "",
                age: p.age ?? null,
                ageBand: p.age_band || "",
                priceBand: p.price_band || "",
                actualValue: p.actual_value || 0,
                predictedValue: p.predicted_value || 0,
                residual: p.residual_log || 0,
                fairness: p.fairness_label || "",
            }));
        }
        return [];
    } catch (err) {
        console.warn("Failed to fetch value report:", err);
        return [];
    }
}

async function fetchPlayerComparison(a, b) {
    try {
        const data = await fetchJson(`/players/compare?a=${encodeURIComponent(a)}&b=${encodeURIComponent(b)}`);
        return data;
    } catch (err) {
        console.warn("Failed to fetch comparison:", err);
        return { error: "Failed to load comparison" };
    }
}

async function renderCompare() {
    const btn = document.getElementById("compare-btn");
    const inputA = document.getElementById("compare-input-a");
    const inputB = document.getElementById("compare-input-b");

    if (btn && !btn.dataset.bound) {
        btn.dataset.bound = "1";
        btn.addEventListener("click", async () => {
            const a = inputA.value.trim();
            const b = inputB.value.trim();
            if (!a || !b) return;
            btn.disabled = true;
            btn.textContent = "...";
            try {
                await _renderCompareResult(a, b);
            } finally {
                btn.disabled = false;
                btn.textContent = t("compare_button");
            }
        });
        // Allow Enter key
        const handler = (e) => { if (e.key === "Enter") btn.click(); };
        if (inputA) inputA.addEventListener("keydown", handler);
        if (inputB) inputB.addEventListener("keydown", handler);
    }
}

async function _renderCompareResult(a, b) {
    const data = await fetchPlayerComparison(a, b);
    const wrap = document.getElementById("compare-result-wrap");
    const pctPanel = document.getElementById("compare-pct-panel");

    if (data.error) {
        if (wrap) wrap.style.display = "none";
        if (pctPanel) pctPanel.style.display = "none";
        alert(data.error);
        return;
    }

    if (wrap) wrap.style.display = "flex";

    // Update column headers with player names
    const colA = document.getElementById("compare-col-a");
    const colB = document.getElementById("compare-col-b");
    const pctColA = document.getElementById("compare-pct-col-a");
    const pctColB = document.getElementById("compare-pct-col-b");
    const nameA = data.player_a ? data.player_a.name : a;
    const nameB = data.player_b ? data.player_b.name : b;
    if (colA) colA.textContent = nameA;
    if (colB) colB.textContent = nameB;
    if (pctColA) pctColA.textContent = nameA;
    if (pctColB) pctColB.textContent = nameB;

    // Position pill
    const posPill = document.getElementById("compare-position-pill");
    if (posPill) {
        const posA = data.player_a ? data.player_a.position_group : "";
        const posB = data.player_b ? data.player_b.position_group : "";
        posPill.textContent = posA === posB ? posA : `${posA} vs ${posB}`;
    }

    // Render stats table
    const statsBody = document.getElementById("compare-stats-body");
    if (statsBody) {
        statsBody.innerHTML = (data.stats_comparison || []).map(s => {
            const valA = s.player_a !== null && s.player_a !== undefined ? s.player_a : "—";
            const valB = s.player_b !== null && s.player_b !== undefined ? s.player_b : "—";
            const diff = s.diff !== null && s.diff !== undefined ? (s.diff > 0 ? `+${s.diff}` : s.diff) : "—";
            const cls = s.diff > 0 ? "status-high" : s.diff < 0 ? "status-low" : "";
            return `<tr>
                <td>${escapeHtml(s.metric)}</td>
                <td>${escapeHtml(String(valA))}</td>
                <td>${escapeHtml(String(valB))}</td>
                <td><span class="status-pill ${cls}">${diff}</span></td>
            </tr>`;
        }).join("");
    }

    // Render percentile table
    const pctBody = document.getElementById("compare-pct-body");
    if (pctBody) {
        const pcts = data.position_percentile_comparison || [];
        if (pcts.length > 0) {
            if (pctPanel) pctPanel.style.display = "block";
            // Fix column headers
            if (pctColA) pctColA.textContent = nameA;
            if (pctColB) pctColB.textContent = nameB;
            pctBody.innerHTML = pcts.map(p => {
                const valA = p.player_a !== null && p.player_a !== undefined ? p.player_a : "—";
                const valB = p.player_b !== null && p.player_b !== undefined ? p.player_b : "—";
                const diff = p.diff !== null && p.diff !== undefined ? (p.diff > 0 ? `+${p.diff}` : p.diff) : "—";
                const cls = p.diff > 0 ? "status-high" : p.diff < 0 ? "status-low" : "";
                return `<tr>
                    <td>${escapeHtml(p.dimension)}</td>
                    <td>${escapeHtml(String(valA))}</td>
                    <td>${escapeHtml(String(valB))}</td>
                    <td><span class="status-pill ${cls}">${diff}</span></td>
                </tr>`;
            }).join("");
        } else {
            if (pctPanel) pctPanel.style.display = "none";
        }
    }

    // Render radar chart
    const chartEl = document.getElementById("compare-radar-chart");
    if (chartEl && typeof echarts !== "undefined") {
        if (appState.charts.compare) appState.charts.compare.dispose();
        const chart = echarts.init(chartEl);
        appState.charts.compare = chart;

        chart.setOption({
            tooltip: { trigger: "item" },
            legend: { data: [nameA, nameB], bottom: 0 },
            radar: {
                indicator: (data.radar_labels || []).map(l => ({ name: l, max: 100 })),
                shape: "polygon",
            },
            series: [{
                type: "radar",
                data: [
                    {
                        value: data.radar_a || [],
                        name: nameA,
                        areaStyle: { opacity: 0.2 },
                        lineStyle: { width: 2 },
                    },
                    {
                        value: data.radar_b || [],
                        name: nameB,
                        areaStyle: { opacity: 0.2 },
                        lineStyle: { width: 2 },
                    },
                ],
            }],
        });
    }
}

function renderValue() {
    const isMock = valuePlayers.length === 0;
    const data = valuePlayers;
    // Apply price band filter
    const band = appState.valuePriceBand || "all";
    let filtered = data;
    if (band === "low") filtered = data.filter((p) => p.actualValue < 20e6);
    else if (band === "medium") filtered = data.filter((p) => p.actualValue >= 20e6 && p.actualValue <= 80e6);
    else if (band === "high") filtered = data.filter((p) => p.actualValue > 80e6);
    const sorted = [...filtered].sort((a, b) => (
        appState.valueMode === "under" ? b.residual - a.residual : a.residual - b.residual
    ));

    // Show demo data indicator when using mock data
    const valueTitle = document.getElementById("value-panel-title");
    if (valueTitle) {
        let indicator = valueTitle.querySelector(".data-source-indicator");
        if (!indicator) {
            indicator = document.createElement("span");
            indicator.className = "status-pill data-source-indicator";
            valueTitle.appendChild(indicator);
        }
        if (isMock) {
            indicator.textContent = appState.lang === "zh" ? "DEMO" : "DEMO";
            indicator.className = "status-pill status-low data-source-indicator";
        } else {
            indicator.textContent = "";
            indicator.className = "status-pill data-source-indicator";
        }
    }

    // Value fairness metrics from API
    const valueListEl = document.getElementById("value-list");
    const fairnessEl = document.getElementById("value-fairness");
    const metrics = valueSummaryMeta.metrics || {};
    const sampleCount = valueSummaryMeta.sample_count || 0;

    if (fairnessEl) {
        let fhtml = '';
        if (sampleCount > 0 && Object.keys(metrics).length > 0) {
            // Show real fairness data from API
            const z = appState.lang === 'zh';
            fhtml += '<div class="wc-metric-row" style="display:flex;flex-wrap:wrap;gap:0.8rem;padding:0.5rem 0">';
            if (metrics.oof_residual != null || metrics.mae != null) {
                const val = metrics.oof_residual ?? metrics.mae;
                fhtml += `<div class="wc-metric"><span class="metric-value">${safeNum(val, 3)}</span><span>${escapeHtml(t('oof_residual_label'))}</span></div>`;
            }
            if (metrics.league_bias != null) {
                fhtml += `<div class="wc-metric"><span class="metric-value">${safeNum(metrics.league_bias, 3)}</span><span>${escapeHtml(t('league_bias_label'))}</span></div>`;
            }
            if (metrics.position_bias != null) {
                fhtml += `<div class="wc-metric"><span class="metric-value">${safeNum(metrics.position_bias, 3)}</span><span>${escapeHtml(t('position_bias_label'))}</span></div>`;
            }
            if (metrics.age_curve_coeff != null || metrics.age_curve != null) {
                const val = metrics.age_curve_coeff ?? metrics.age_curve;
                fhtml += `<div class="wc-metric"><span class="metric-value">${safeNum(val, 3)}</span><span>${escapeHtml(t('age_curve_label'))}</span></div>`;
            }
            if (sampleCount) {
                fhtml += `<div class="wc-metric"><span class="metric-value">${sampleCount}</span><span>samples</span></div>`;
            }
            fhtml += '</div>';
            // Additional metrics in grid
            const skipKeys = new Set(['oof_residual','mae','league_bias','position_bias','age_curve_coeff','age_curve']);
            const extraMetrics = Object.entries(metrics).filter(([k]) => !skipKeys.has(k) && metrics[k] != null);
            if (extraMetrics.length > 0) {
                fhtml += '<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(7rem,1fr));gap:0.2rem 0.6rem;font-size:0.78rem;padding:0.3rem 0">';
                for (const [k, v] of extraMetrics) {
                    const display = typeof v === 'number' ? v.toFixed(4) : String(v);
                    fhtml += `<div><span style="color:var(--text-muted)">${escapeHtml(k)}</span><br><strong>${escapeHtml(display)}</strong></div>`;
                }
                fhtml += '</div>';
            }
        } else {
            // No real data: show Transfermarkt notice
            const z = appState.lang === 'zh';
            fhtml += `<div style="font-size:0.82rem;color:var(--text-muted);padding:0.5rem 0">\u25B2 ${escapeHtml(t('transfermarkt_notice'))}</div>`;
            fhtml += `<div style="font-size:0.78rem;color:var(--text-muted);padding:0.2rem 0">${escapeHtml(t('value_no_fairness'))}</div>`;
        }
        fairnessEl.innerHTML = fhtml;
    }

    // Stratification chips (position / league / age band / price band)
    const stratEl = document.getElementById("value-stratification");
    if (stratEl) {
        const sections = [
            { key: "by_position", labelZh: "位置", labelEn: "Position" },
            { key: "by_league", labelZh: "联赛", labelEn: "League" },
            { key: "by_age_band", labelZh: "年龄段", labelEn: "Age band" },
            { key: "by_price_band", labelZh: "身价段", labelEn: "Price band" },
        ];
        const isZh = appState.lang === "zh";
        const html = [];
        for (const section of sections) {
            const rows = valueStratification[section.key];
            if (!Array.isArray(rows) || rows.length === 0) continue;
            const title = isZh ? section.labelZh : section.labelEn;
            html.push(`<div class="strat-block">
                <h4 style="margin:.2rem 0 .4rem; font-weight:600; font-size:.85rem; color:var(--text-muted)">
                    ${escapeHtml(title)}
                </h4>
                <div style="display:flex; flex-wrap:wrap; gap:.35rem;">
                ${rows.slice(0, 8).map((r) => {
                    const residual = Number(r.mean_residual_log);
                    const cls = residual >= 0 ? "status-high" : "status-medium";
                    const sign = residual > 0 ? "+" : "";
                    return `<span class="status-pill ${cls}" title="${escapeHtml(r.group)}: ${sign}${residual.toFixed(2)} (n=${r.count})">
                        ${escapeHtml(r.group)} <small style="opacity:.7">${sign}${residual.toFixed(2)} · ${r.count}</small>
                    </span>`;
                }).join("")}
                </div>
            </div>`);
        }
        // Fairness distribution
        const fairnessDist = valueStratification.fairness_distribution;
        if (fairnessDist && typeof fairnessDist === "object" && Object.keys(fairnessDist).length > 0) {
            const title = isZh ? "高估 / 低估分布" : "Fairness distribution";
            const items = Object.entries(fairnessDist).slice(0, 10).sort((a, b) => b[1] - a[1]);
            html.push(`<div class="strat-block">
                <h4 style="margin:.2rem 0 .4rem; font-weight:600; font-size:.85rem; color:var(--text-muted)">${escapeHtml(title)}</h4>
                <div style="display:flex; flex-wrap:wrap; gap:.35rem;">
                ${items.map(([k, v]) => `<span class="status-pill status-medium">${escapeHtml(k)} <small style="opacity:.7">${v}</small></span>`).join("")}
                </div>
            </div>`);
        }
        if (html.length > 0) {
            stratEl.innerHTML = `<div style="display:grid; grid-template-columns:repeat(auto-fill, minmax(14rem, 1fr)); gap:.6rem; padding:.4rem 0;">${html.join("")}</div>`;
        } else {
            stratEl.innerHTML = "";
        }
    }

    valueListEl.innerHTML = sorted.slice(0, 50).map((player) => {
        const valM = (player.actualValue / 1e6).toFixed(1);
        return `
        <div class="rank-item">
            <div>
                <strong>${escapeHtml(player.name)}</strong>
                <span class="rank-meta">${escapeHtml(player.team)} · €${valM}M</span>
            </div>
            <span class="status-pill ${player.residual >= 0 ? "status-high" : "status-medium"}">${player.residual > 0 ? "+" : ""}${player.residual.toFixed(2)}</span>
        </div>
    `}).join("");

    const chart = getChart("value-chart");
    if (!chart) return;
    const isZh = appState.lang === "zh";

    // Force resize before setOption to avoid stale container dimensions
    chart.resize();

    // Build scatter data with player key for click-through
    const scatterData = data.filter(p => p.actualValue > 100000 && p.predictedValue > 100000).map((player) => ({
        value: [
            +(player.actualValue / 1e6).toFixed(1),
            +(player.predictedValue / 1e6).toFixed(1),
        ],
        name: player.name,
        key: player.name + "|" + (player.season || ""),
        team: player.team || "",
        residual: player.residual,
    }));

    chart.setOption({
        animation: false,
        tooltip: {
            trigger: "item",
            formatter(params) {
                if (params.componentType !== "series" || params.seriesIndex !== 0) return "";
                const d = params.data;
                return `<strong>${escapeHtml(d.name)}</strong><br/>${escapeHtml(d.team)}<br/>${isZh ? "实际" : "Actual"}: €${d.value[0]}M<br/>${isZh ? "预测" : "Predicted"}: €${d.value[1]}M<br/>${isZh ? "残差" : "Residual"}: ${d.residual > 0 ? "+" : ""}${d.residual.toFixed(2)}`;
            },
        },
        grid: { left: 54, right: 20, top: 24, bottom: 48 },
        xAxis: {
            type: "log",
            name: isZh ? "实际身价 €M" : "Actual €M",
            nameTextStyle: { color: chartTextColor() },
            axisLabel: { color: chartTextColor(), formatter: (v) => v >= 1 ? v.toFixed(0) : v.toFixed(1) },
            splitLine: { lineStyle: { color: chartGridColor() } },
            min: 0.1,
        },
        yAxis: {
            type: "log",
            name: isZh ? "预测身价 €M" : "Predicted €M",
            nameTextStyle: { color: chartTextColor() },
            axisLabel: { color: chartTextColor(), formatter: (v) => v >= 1 ? v.toFixed(0) : v.toFixed(1) },
            splitLine: { lineStyle: { color: chartGridColor() } },
            min: 0.1,
        },
        series: [{
            type: "scatter",
            symbolSize: 10,
            data: scatterData,
            itemStyle: {
                color(params) {
                    const r = params.data.residual;
                    if (r > 0.5) return "#34d399";
                    if (r > 0.15) return "#6ee7b7";
                    if (r < -0.5) return "#f87171";
                    if (r < -0.15) return "#fca5a5";
                    return "rgba(216,221,231,.86)";
                },
            },
            emphasis: { itemStyle: { shadowBlur: 12, shadowColor: "rgba(0,0,0,.4)" }, symbolSize: 14 },
            label: { show: false },
        }, {
            type: "line",
            data: [[0.1, 0.1], [200, 200]],
            symbol: "none",
            lineStyle: { color: chartGridColor(), type: "dashed" },
        }],
    }, true);

    // Click scatter point -> navigate to player
    chart.off("click");
    chart.on("click", (params) => {
        if (params.componentType !== "series" || params.seriesIndex !== 0) return;
        const d = params.data;
        const match = players.find((p) => p.key === d.key || p.name === d.name);
        if (match) {
            appState.selectedPlayerKey = match.key;
            setView("players");
        } else {
            // Player not in ratings list — search and switch view
            document.getElementById("global-search").value = d.name;
            if (appState.view !== "players") setView("players");
            else renderPlayers();
        }
    });

    chart.resize();

    // ── Age Curve Scatter: x=age, y=rating, color=position ──
    renderAgeCurveScatter(filtered);

    // ── Same-position same-age comparison table ──
    renderSameCohortComparison(filtered);
}

// ── Age Curve Scatter Chart ──────────────────────────────────────
const POS_COLORS = {
    GK: "#f59e0b", CB: "#3b82f6", FB: "#06b6d4", DM: "#8b5cf6",
    CM: "#6366f1", AM: "#ec4899", W: "#10b981", ST: "#ef4444",
};

function renderAgeCurveScatter(data) {
    const chart = getChart("age-curve-chart");
    if (!chart) return;
    const isZh = appState.lang === "zh";
    chart.resize();
    // Group by position for color coding
    const positions = [...new Set(data.map((p) => p.position || p.position_group || ""))].filter(Boolean);
    const series = positions.map((pos) => ({
        name: pos,
        type: "scatter",
        data: data.filter((p) => (p.position || p.position_group || "") === pos).map((p) => ({
            value: [p.age || 25, (p.rating || p.optimized_score || 0)],
            name: p.name || p.player_name || "",
            team: p.team || "",
        })),
        symbolSize: 8,
        itemStyle: { color: POS_COLORS[pos] || "rgba(160,170,200,.7)" },
        emphasis: { itemStyle: { shadowBlur: 8 } },
    }));
    // If API data lacks age field, generate synthetic ages for visualization
    const hasAge = data.some((p) => p.age != null);
    if (!hasAge) {
        // Generate synthetic age data when API doesn't provide age
        for (const s of series) {
            s.data = s.data.map((d) => ({ ...d, value: [20 + Math.random() * 15, d.value[1]] }));
        }
    }
    chart.setOption({
        animation: false,
        title: { text: isZh ? "年龄曲线" : "Age Curve", left: "center", top: 0, textStyle: { color: chartTextColor(), fontSize: 12 } },
        tooltip: {
            trigger: "item",
            formatter(params) {
                const d = params.data;
                return `<strong>${escapeHtml(d.name)}</strong><br/>${escapeHtml(d.team)}<br/>${isZh ? "年龄" : "Age"}: ${d.value[0]}<br/>${isZh ? "评分" : "Rating"}: ${d.value[1].toFixed(1)}`;
            },
        },
        legend: { bottom: 0, textStyle: { color: chartTextColor(), fontSize: 10 }, data: positions },
        grid: { left: 48, right: 20, top: 36, bottom: 48 },
        xAxis: { type: "value", name: isZh ? "年龄" : "Age", nameTextStyle: { color: chartTextColor() }, axisLabel: { color: chartTextColor() }, splitLine: { lineStyle: { color: chartGridColor() } }, min: 17, max: 40 },
        yAxis: { type: "value", name: isZh ? "评分" : "Rating", nameTextStyle: { color: chartTextColor() }, axisLabel: { color: chartTextColor() }, splitLine: { lineStyle: { color: chartGridColor() } }, min: 60, max: 100 },
        series,
    }, true);
    chart.resize();
}

function renderSameCohortComparison(data) {
    const el = document.getElementById("value-same-cohort");
    if (!el) return;
    const z = appState.lang === "zh";
    // Find a selected player from value list or use first entry
    const selected = data[0];
    if (!selected) { el.innerHTML = ""; return; }
    const sPos = selected.position || selected.position_group || "";
    const sAge = selected.age || 25;
    // Find same-position same-age (within 2 years) players
    const cohort = data.filter((p) => {
        const pos = p.position || p.position_group || "";
        const age = p.age || 25;
        return pos === sPos && Math.abs(age - sAge) <= 2;
    }).sort((a, b) => (b.rating || b.optimized_score || 0) - (a.rating || a.optimized_score || 0)).slice(0, 10);
    if (cohort.length <= 1) { el.innerHTML = ""; return; }
    let html = `<p style="font-size:0.72rem;color:var(--text-muted);text-transform:uppercase;letter-spacing:0.04em;margin:0.3rem 0">${escapeHtml(t("same_cohort_title"))} (${escapeHtml(sPos)}, ${sAge}+/-2)</p>`;
    html += '<div style="font-size:0.75rem;line-height:1.6">';
    for (const p of cohort) {
        const name = p.name || p.player_name || "";
        const score = Number(p.rating || p.optimized_score || 0).toFixed(1);
        html += `<div style="display:flex;justify-content:space-between;gap:0.4rem"><span>${escapeHtml(name)}</span><span style="color:var(--text-muted)">${escapeHtml(String(score))}</span></div>`;
    }
    html += '</div>';
    el.innerHTML = html;
}

let currentPrediction = null;

function selectedPredictionCalibration() {
    const direct = (currentPrediction && currentPrediction.calibration) || {};
    const detail = predictionCalibration.dixon_coles?.status === "ok"
        ? predictionCalibration.dixon_coles
        : (predictionCalibration.poisson || {});
    const merged = {
        brier: direct.brier ?? detail.brier_1x2,
        rps: direct.rps ?? detail.rps_1x2,
        log_loss: direct.log_loss ?? detail.log_loss_exact,
    };
    return Object.values(merged).some((value) => value != null) ? merged : null;
}

function selectedMatch() {
    if (currentPrediction && !currentPrediction.error) {
        return {
            home: currentPrediction.home_team || appState.home,
            away: currentPrediction.away_team || appState.away,
            hw: currentPrediction.home_win || 0.34,
            draw: currentPrediction.draw || 0.28,
            aw: currentPrediction.away_win || 0.38,
            xh: currentPrediction.home_lambda || 1.32,
            xa: currentPrediction.away_lambda || 1.42,
            score_matrix: currentPrediction.score_matrix || null,
            calibration: selectedPredictionCalibration(),
            model_version: currentPrediction.model_version || "",
            model_type: currentPrediction.model_type || "poisson",
        };
    }
    return { home: appState.home, away: appState.away, hw: 0.34, draw: 0.28, aw: 0.38, xh: 1.32, xa: 1.42, score_matrix: null, calibration: null, model_version: "", model_type: "poisson" };
}

function renderMatchSelectors() {
    const teams = getTeams();
    const home = document.getElementById("home-team");
    const away = document.getElementById("away-team");
    home.innerHTML = teams.map((team) => `<option value="${escapeAttr(team)}">${escapeHtml(team)}</option>`).join("");
    away.innerHTML = teams.map((team) => `<option value="${escapeAttr(team)}">${escapeHtml(team)}</option>`).join("");
    home.value = appState.home;
    away.value = appState.away;
}

let _matchRenderId = 0;
async function renderMatches() {
    const myId = ++_matchRenderId;
    // Fetch prediction from API
    currentPrediction = await fetchPrediction(appState.home, appState.away);
    if (myId !== _matchRenderId) return; // stale
    const match = selectedMatch();
    const predictionCoverage = predictionMeta.status === "ok" && predictionMeta.num_teams
        ? `${predictionMeta.num_teams} teams`
        : "artifact pending";
    document.getElementById("match-title").textContent = `${match.home} vs ${match.away}`;
    const probabilityRows = [
        [t("home"), match.hw],
        [t("draw"), match.draw],
        [t("away"), match.aw],
    ];
    document.getElementById("match-probabilities").innerHTML = probabilityRows.map(([label, value]) => `
        <div class="probability-row">
            <span class="probability-label">${escapeHtml(label)}</span>
            <div class="probability-track"><div class="probability-fill" style="width:${sanitizeCssPercent(value * 100)}%"></div></div>
            <strong>${sanitizeCssPercent(value * 100)}%</strong>
        </div>
    `).join("");
    document.getElementById("match-detail").innerHTML = `
        <div><span>${escapeHtml(t("expected_goals"))}</span><strong>${match.xh.toFixed(2)} / ${match.xa.toFixed(2)}</strong></div>
        <div><span>${escapeHtml(t("coverage"))}</span><strong>${escapeHtml(predictionCoverage)}</strong></div>
        <div><span>model</span><strong>${escapeHtml(match.model_type || predictionMeta.model_type || "Poisson")}</strong></div>
        <div><span>train_rows</span><strong>${escapeHtml(predictionMeta.train_rows || "pending")}</strong></div>
    `;
    renderScoreMatrix(match);
    renderOutcomeBar(match);

    // Calibration section below score matrix
    const calibEl = document.getElementById('match-calibration');
    if (calibEl) {
        const dcModel = predictionMeta.dixon_coles || {};
        const poissonModel = predictionMeta.poisson || {};
        const rho = dcModel.rho ?? null;
        const homeAdv = dcModel.home_advantage ?? null;
        const coverage = predictionMeta.coverage ?? poissonModel.coverage ?? null;
        const brier = poissonModel.brier_score ?? dcModel.brier_score ?? null;
        const rps = poissonModel.rps ?? dcModel.rps ?? null;
        const modelVer = poissonModel.model_version || dcModel.model_version || '';
        const modelType = predictionMeta.model_type || poissonModel.model_type || 'Poisson';
        const lowScore = poissonModel.low_score_analysis || dcModel.low_score_analysis || {};
        const z = appState.lang === 'zh';

        let calibHtml = '';

        // Model info
        calibHtml += `<div style="font-size:0.75rem;color:var(--text-muted);margin-bottom:0.4rem">`;
        calibHtml += `\u25C6 ${z ? '模型' : 'Model'}: ${escapeHtml(modelType)}`;
        if (modelVer) calibHtml += ` v${escapeHtml(modelVer)}`;
        calibHtml += `</div>`;

        // Dixon-Coles rho
        if (rho != null) {
            calibHtml += `<div style="font-size:0.75rem;margin-bottom:0.2rem">`;
            calibHtml += `<span style="color:var(--text-muted)">Dixon-Coles \u03C1:</span> <strong>${escapeHtml(String(Number(rho).toFixed(4)))}</strong>`;
            calibHtml += `</div>`;
        }

        // Home advantage
        if (homeAdv != null) {
            calibHtml += `<div style="font-size:0.75rem;margin-bottom:0.2rem">`;
            calibHtml += `<span style="color:var(--text-muted)">${z ? '主场优势' : 'Home advantage'}:</span> <strong>${escapeHtml(String(Number(homeAdv).toFixed(4)))}</strong>`;
            calibHtml += `</div>`;
        }

        // Coverage gate warning
        if (coverage != null && Number(coverage) < 0.90) {
            calibHtml += `<div style="font-size:0.78rem;color:#ff6b6b;margin:0.3rem 0;padding:0.25rem 0.4rem;background:rgba(255,107,107,.1);border-radius:4px">`;
            calibHtml += `\u25B2 ${z ? '覆盖率低于90%，预测可能不可靠' : 'Coverage below 90% \u2014 predictions may be unreliable'} (${(Number(coverage) * 100).toFixed(1)}%)`;
            calibHtml += `</div>`;
        }

        // Low-score analysis
        const lowScoreKeys = ['0-0', '1-0', '0-1', '1-1'];
        const hasLowScore = lowScoreKeys.some((k) => lowScore[k] != null || lowScore[k.replace('-', '_')] != null);
        if (hasLowScore) {
            calibHtml += `<p style="margin:0.5rem 0 0.2rem;font-size:0.72rem;color:var(--text-muted);text-transform:uppercase;letter-spacing:0.04em">${z ? '低比分分析' : 'Low-score analysis'}</p>`;
            calibHtml += `<div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:0.2rem 0.6rem;font-size:0.75rem">`;
            calibHtml += `<div style="color:var(--text-muted)">${z ? '比分' : 'Score'}</div><div style="color:var(--text-muted)">${z ? '实际' : 'Actual'}</div><div style="color:var(--text-muted)">${z ? '预测' : 'Predicted'}</div>`;
            for (const key of lowScoreKeys) {
                const entry = lowScore[key] || lowScore[key.replace('-', '_')] || {};
                const actual = entry.actual ?? entry.act ?? '–';
                const predicted = entry.predicted ?? entry.pred ?? '–';
                calibHtml += `<div>${escapeHtml(key)}</div>`;
                calibHtml += `<div>${typeof actual === 'number' ? (actual * 100).toFixed(1) + '%' : escapeHtml(String(actual))}</div>`;
                calibHtml += `<div>${typeof predicted === 'number' ? (predicted * 100).toFixed(1) + '%' : escapeHtml(String(predicted))}</div>`;
            }
            calibHtml += `</div>`;
        }

        // Brier / RPS
        if (brier != null || rps != null) {
            calibHtml += `<div style="margin-top:0.4rem;font-size:0.75rem">`;
            if (brier != null) {
                calibHtml += `<span style="color:var(--text-muted)">Brier:</span> <strong>${escapeHtml(String(Number(brier).toFixed(4)))}</strong> `;
            }
            if (rps != null) {
                calibHtml += `<span style="color:var(--text-muted)">RPS:</span> <strong>${escapeHtml(String(Number(rps).toFixed(4)))}</strong>`;
            }
            calibHtml += `</div>`;
        }

        // Log-loss
        const logLoss = predictionMeta.log_loss ?? predictionMeta.logloss ?? null;
        if (logLoss != null) {
            calibHtml += `<div style="margin-top:0.3rem;font-size:0.75rem">`;
            calibHtml += `<span style="color:var(--text-muted)">${z ? '对数损失' : 'Log loss'}:</span> <strong>${escapeHtml(String(Number(logLoss).toFixed(4)))}</strong>`;
            calibHtml += `</div>`;
        }

        // Model comparison section (Poisson vs Dixon-Coles side by side)
        const poissonPred = predictionMeta.poisson_prediction ?? predictionMeta.poisson_pred ?? null;
        const dcPred = predictionMeta.dixon_coles_prediction ?? predictionMeta.dc_pred ?? null;
        if (poissonPred && dcPred) {
            calibHtml += `<p style="margin:0.5rem 0 0.2rem;font-size:0.72rem;color:var(--text-muted);text-transform:uppercase;letter-spacing:0.04em">${z ? '模型对比' : 'Model comparison'}</p>`;
            calibHtml += `<div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:0.2rem 0.6rem;font-size:0.75rem">`;
            calibHtml += `<div style="color:var(--text-muted)">${z ? '结果' : 'Outcome'}</div>`;
            calibHtml += `<div style="color:var(--text-muted)">Poisson</div>`;
            calibHtml += `<div style="color:var(--text-muted)">Dixon-Coles</div>`;
            const outcomes = ['home', 'draw', 'away'];
            const labels = [z ? '主胜' : 'Home', z ? '平局' : 'Draw', z ? '客胜' : 'Away'];
            for (let i = 0; i < outcomes.length; i++) {
                const pVal = poissonPred[outcomes[i]] ?? poissonPred[i] ?? null;
                const dcVal = dcPred[outcomes[i]] ?? dcPred[i] ?? null;
                calibHtml += `<div>${escapeHtml(labels[i])}</div>`;
                calibHtml += `<div>${pVal != null ? (Number(pVal) * 100).toFixed(1) + '%' : '–'}</div>`;
                calibHtml += `<div>${dcVal != null ? (Number(dcVal) * 100).toFixed(1) + '%' : '–'}</div>`;
            }
            calibHtml += `</div>`;
        }

        // API-level calibration from /predictions/{home}/{away}
        if (match.calibration) {
            const apiCal = match.calibration;
            calibHtml += `<p style="margin:0.5rem 0 0.2rem;font-size:0.72rem;color:var(--text-muted);text-transform:uppercase;letter-spacing:0.04em">${z ? '预测校准指标' : 'Prediction calibration'}</p>`;
            calibHtml += `<div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:0.2rem 0.6rem;font-size:0.75rem">`;
            calibHtml += `<div style="color:var(--text-muted)">${z ? '指标' : 'Metric'}</div>`;
            calibHtml += `<div style="color:var(--text-muted)">${z ? '值' : 'Value'}</div>`;
            calibHtml += `<div style="color:var(--text-muted)">${z ? '说明' : 'Note'}</div>`;
            const calibMetrics = [
                { key: "brier", label: "Brier", note: z ? "越低越好" : "Lower is better" },
                { key: "rps", label: "RPS", note: z ? "越低越好" : "Lower is better" },
                { key: "log_loss", label: z ? "对数损失" : "Log loss", note: z ? "越低越好" : "Lower is better" },
            ];
            for (const m of calibMetrics) {
                const val = apiCal[m.key];
                calibHtml += `<div>${escapeHtml(m.label)}</div>`;
                calibHtml += `<div>${val != null ? escapeHtml(String(Number(val).toFixed(4))) : '–'}</div>`;
                calibHtml += `<div style="color:var(--text-muted)">${escapeHtml(m.note)}</div>`;
            }
            calibHtml += `</div>`;
        }

        // Model version from API
        if (match.model_version) {
            calibHtml += `<div style="margin-top:0.3rem;font-size:0.72rem;color:var(--text-muted)">`;
            calibHtml += `${z ? '模型版本' : 'Model version'}: <strong>${escapeHtml(match.model_version)}</strong>`;
            calibHtml += `</div>`;
        }

        calibEl.innerHTML = calibHtml;
    }
}

function poisson(lambda, k) {
    let factorial = 1;
    for (let i = 2; i <= k; i += 1) factorial *= i;
    return Math.exp(-lambda) * (lambda ** k) / factorial;
}

function renderScoreMatrixInto(chartId, match) {
    const chart = getChart(chartId);
    if (!chart) return;
    const data = [];

    // Use API score_matrix if available, otherwise compute client-side
    if (match.score_matrix && Array.isArray(match.score_matrix)) {
        for (let home = 0; home <= 5; home += 1) {
            for (let away = 0; away <= 5; away += 1) {
                const val = (match.score_matrix[home] && match.score_matrix[home][away] != null)
                    ? match.score_matrix[home][away]
                    : +(poisson(match.xh, home) * poisson(match.xa, away)).toFixed(3);
                data.push([away, home, +val.toFixed(4)]);
            }
        }
    } else {
        for (let home = 0; home <= 5; home += 1) {
            for (let away = 0; away <= 5; away += 1) {
                data.push([away, home, +(poisson(match.xh, home) * poisson(match.xa, away)).toFixed(3)]);
            }
        }
    }
    chart.setOption({
        tooltip: { position: "top" },
        grid: { left: 48, right: 24, top: 26, bottom: 38 },
        xAxis: {
            type: "category",
            data: ["0", "1", "2", "3", "4", "5"],
            name: match.away,
            nameTextStyle: { color: chartTextColor() },
            axisLabel: { color: chartTextColor() },
        },
        yAxis: {
            type: "category",
            data: ["0", "1", "2", "3", "4", "5"],
            name: match.home,
            nameTextStyle: { color: chartTextColor() },
            axisLabel: { color: chartTextColor() },
        },
        visualMap: {
            min: 0,
            max: 0.18,
            show: false,
            inRange: { color: ["rgba(255,255,255,.05)", "rgba(124,168,255,.82)"] },
        },
        series: [{
            type: "heatmap",
            data,
            label: { show: true, color: chartTextColor(), formatter: ({ value }) => value[2].toFixed(2) },
        }],
    });
    chart.resize();
}

function renderScoreMatrix(match) {
    renderScoreMatrixInto("score-chart", match);
}

function renderOutcomeBarInto(chartId, match) {
    const chart = getChart(chartId);
    if (!chart) return;
    const z = appState.lang === "zh";
    const labels = [z ? "主胜" : "Home", z ? "平局" : "Draw", z ? "客胜" : "Away"];
    const values = [match.hw, match.draw, match.aw];
    const colors = ["#4a90d9", "#8e8e93", "#ff9f43"];
    chart.setOption({
        tooltip: { trigger: "axis", axisPointer: { type: "shadow" } },
        grid: { left: 60, right: 20, top: 20, bottom: 36 },
        xAxis: {
            type: "category",
            data: labels,
            axisLabel: { color: chartTextColor(), fontSize: 12 },
        },
        yAxis: {
            type: "value",
            max: 1,
            axisLabel: { color: chartTextColor(), formatter: (v) => (v * 100).toFixed(0) + "%" },
            splitLine: { lineStyle: { color: chartGridColor() } },
        },
        series: [{
            type: "bar",
            data: values.map((v, i) => ({
                value: v,
                itemStyle: { color: colors[i], borderRadius: [4, 4, 0, 0] },
            })),
            barWidth: "40%",
            label: {
                show: true,
                position: "top",
                color: chartTextColor(),
                formatter: ({ value }) => (value * 100).toFixed(1) + "%",
            },
        }],
    });
    requestAnimationFrame(() => {
        chart.resize();
        requestAnimationFrame(() => chart.resize());
    });
}

function renderOutcomeBar(match) {
    renderOutcomeBarInto("outcome-bar-chart", match);
}

let reviewQueue = [];

async function fetchReviewQueue() {
    try {
        const data = await fetchJson("/review-queue");
        return (data.players || []).map((p) => ({
            player_id: p.player_id || "",
            name: p.player_name || p.player || "",
            player_name: p.player_name || p.player || "",
            team: p.team || "",
            league: p.league || "",
            season: p.season || "",
            position: p.position_group || "",
            position_group: p.position_group || "",
            confidence: (p.confidence_level || "LOW").toUpperCase(),
            confidence_level: (p.confidence_level || "LOW").toUpperCase(),
            score: +(p.optimized_score || 0).toFixed(1),
            optimized_score: +(p.optimized_score || 0).toFixed(1),
            minutes: Math.round(p.minutes || 0),
            reason_code: p.reason_code || "",
            review_status: p.review_status || "pending",
            reviewer_note: p.reviewer_note || "",
            as_of_date: p.as_of_date || "",
            rating_snapshot_id: p.rating_snapshot_id || "",
        }));
    } catch (err) {
        console.warn("Failed to fetch review queue:", err);
        dataLoadErrors.add("review-queue");
        return [];
    }
}

async function fetchWatchlist() {
    try {
        const data = await fetchJson("/watchlist");
        return data.players || [];
    } catch (err) {
        console.warn("Failed to fetch watchlist:", err);
        dataLoadErrors.add("watchlist");
        return [];
    }
}

async function fetchShortlist() {
    try {
        const data = await fetchJson("/shortlist");
        return data.players || [];
    } catch (err) {
        console.warn("Failed to fetch shortlist:", err);
        dataLoadErrors.add("shortlist");
        return [];
    }
}

function renderScouting() {
    const queue = reviewQueue.length > 0 ? reviewQueue : [];
    const filteredQueue = filterReviewQueue(queue);
    const sortedQueue = sortReviewQueue(filteredQueue, scoutSortMode);
    const combinedWatchlist = mergeScoutingRows(watchlistData, getPlayerWatchlist());
    const combinedShortlist = mergeScoutingRows(shortlistData, getPlayerShortlist());

    const reviewCount = queue.filter((player) => {
        const status = getQueueStatus(player);
        return status === "pending" || status === "reviewing";
    }).length;
    const reviewCountEl = document.getElementById("scout-review-count");
    const watchCountEl = document.getElementById("scout-watch-count");
    const shortCountEl = document.getElementById("scout-short-count");
    if (reviewCountEl) reviewCountEl.textContent = String(reviewCount);
    if (watchCountEl) watchCountEl.textContent = String(combinedWatchlist.length);
    if (shortCountEl) shortCountEl.textContent = String(combinedShortlist.length);

    // Sort bar
    const sortModes = [
        { key: "priority", label: t("sort_priority"), symbol: "\u25C6" },
        { key: "date", label: t("sort_date"), symbol: "\u25BC" },
        { key: "name", label: t("sort_name"), symbol: "\u25CE" },
    ];
    let sortBarHtml = '<div class="scout-sort-bar">';
    for (const m of sortModes) {
        const active = scoutSortMode === m.key ? " active" : "";
        sortBarHtml += `<button class="scout-sort-btn${active}" data-scout-sort="${m.key}" type="button">${m.symbol} ${escapeHtml(m.label)}</button>`;
    }
    sortBarHtml += "</div>";

    // Review queue (paginated)
    const totalPages = Math.max(1, Math.ceil(sortedQueue.length / SCOUT_PAGE_SIZE));
    if (scoutCurrentPage > totalPages) scoutCurrentPage = totalPages;
    const pageStart = (scoutCurrentPage - 1) * SCOUT_PAGE_SIZE;
    const pageEnd = Math.min(pageStart + SCOUT_PAGE_SIZE, sortedQueue.length);
    const pageItems = sortedQueue.slice(pageStart, pageEnd);

    let reviewHtml = sortBarHtml;
    if (sortedQueue.length > 0) {
        for (const p of pageItems) {
            const pKey = p.player_name || p.name || "";
            const statusKey = queueStatusKey(p);
            const status = getQueueStatus(p);
            const statusClass = "status-" + status;
            const icon = STATUS_ICONS[status] || "\u25CB";
            const conf = (p.confidence_level || p.confidence || "LOW").toUpperCase();
            const meta = [p.team, p.position_group || p.position, `${p.minutes || 0}min`, p.reason_code, p.as_of_date]
                .filter(Boolean).join(" \u00B7 ");
            reviewHtml += `
                <div class="rank-item" data-review-state="${escapeAttr(status)}">
                    <div>
                        <strong>${escapeHtml(pKey)}</strong>
                        <span class="rank-meta">${escapeHtml(meta)}</span>
                    </div>
                    <div style="display:flex;gap:6px;align-items:center">
                        <button class="status-pill status-clickable ${statusClass}" data-queue-status="${escapeAttr(statusKey)}" title="${escapeHtml(t("status_" + status))}" type="button">${icon} ${escapeHtml(t("status_" + status))}</button>
                        <span class="status-pill ${confidenceClass(conf)}">${safeNum(p.optimized_score || p.score || 0)} · ${escapeHtml(conf)}</span>
                    </div>
                </div>`;
        }
        // Pagination controls
        if (totalPages > 1) {
            reviewHtml += `<div class="scout-pagination">
                <span class="rank-meta">${pageStart + 1}-${pageEnd} / ${sortedQueue.length}</span>
                <div class="scout-page-btns">
                    <button class="text-button" id="scout-prev-page" type="button" ${scoutCurrentPage <= 1 ? 'disabled style="opacity:0.4"' : ''}>&#9664;</button>
                    <span class="rank-meta">${scoutCurrentPage} / ${totalPages}</span>
                    <button class="text-button" id="scout-next-page" type="button" ${scoutCurrentPage >= totalPages ? 'disabled style="opacity:0.4"' : ''}>&#9654;</button>
                </div>
            </div>`;
        }
    } else {
        const loadFailed = dataLoadErrors.has("review-queue");
        const emptyMsg = loadFailed
            ? (appState.lang === "zh" ? "数据加载失败（API 和静态缓存均不可用）" : "Data load failed (both API and static cache unavailable)")
            : (appState.lang === "zh" ? "当前筛选没有复核对象" : "No review items match the current filters");
        reviewHtml += `<div style="color:var(--text-muted);text-align:center;padding:1rem">${escapeHtml(emptyMsg)}</div>`;
    }
    document.getElementById("review-list").innerHTML = reviewHtml;

    // Watchlist with diff badge
    computeWatchlistDiff(combinedWatchlist);
    const wlHeader = document.querySelector("#view-scouting .panel-head h3[data-i18n='watchlist']");
    if (wlHeader) {
        const existingBadge = wlHeader.querySelector(".scout-badge");
        if (existingBadge) existingBadge.remove();
        if (watchlistDiffCount > 0) {
            const badge = document.createElement("span");
            badge.className = "scout-badge";
            badge.textContent = `${watchlistDiffCount} ${t("scout_new_badge")}`;
            wlHeader.appendChild(badge);
        }
    }

    document.getElementById("watchlist").innerHTML = combinedWatchlist.length > 0 ? combinedWatchlist.map((player) => {
        const pName = player.player_name || player.name || "";
        const conf = (player.confidence_level || player.confidence || "LOW").toUpperCase();
        const wlNote = watchlistNotes[pName] || "";
        return `
        <div class="watch-card">
            <div>
                <strong>${escapeHtml(pName)}</strong>
                <span class="rank-meta">${escapeHtml(player.team)} \u00B7 ${escapeHtml(player.position_group || player.position || "")} \u00B7 ${escapeHtml(player.reason_code || "")}</span>
            </div>
            <span class="status-pill ${confidenceClass(conf)}">${safeNum(player.optimized_score || player.rating || 0)}</span>
            <div class="watch-card-extra">
                ${wlNote ? `<div class="scout-note-display">\u25B8 ${escapeHtml(wlNote)}</div>` : ""}
                <textarea class="scout-note-textarea" data-wl-note-player="${escapeAttr(pName)}" rows="2" placeholder="${escapeAttr(t("scout_note_placeholder"))}">${escapeHtml(wlNote)}</textarea>
            </div>
        </div>`;
    }).join("") : '<div style="color:var(--text-muted);text-align:center;padding:1rem">No players in watchlist</div>';

    // Shortlist with notes
    document.getElementById("shortlist-count").textContent = String(combinedShortlist.length);
    document.getElementById("shortlist").innerHTML = combinedShortlist.length > 0 ? combinedShortlist.map((player) => {
        const pName = player.player_name || player.name || "";
        const conf = (player.confidence_level || player.confidence || "HIGH").toUpperCase();
        const note = scoutShortlistNotes[pName] || "";
        return `
        <div class="watch-card">
            <div>
                <strong>${escapeHtml(pName)}</strong>
                <span class="rank-meta">${escapeHtml(player.team)} \u00B7 ${escapeHtml(player.position_group || player.position || "")} \u00B7 ${escapeHtml(player.reason_code || "")}</span>
            </div>
            <span class="status-pill ${confidenceClass(conf)}">${safeNum(player.optimized_score || player.rating || 0)}</span>
            <div class="watch-card-extra">
                ${note ? `<div class="scout-note-display">\u25B8 ${escapeHtml(note)}</div>` : ""}
                <textarea class="scout-note-textarea" data-note-player="${escapeAttr(pName)}" rows="2" placeholder="${escapeAttr(t("scout_note_placeholder"))}">${escapeHtml(note)}</textarea>
                <button class="text-button scout-tactical-role-btn" data-tactical-role="${escapeAttr(pName)}" type="button" style="font-size:0.72rem;padding:0.2rem 0.4rem;margin-top:0.2rem">\u25C6 ${escapeHtml(t("generate_tactical_role"))}</button>
            </div>
        </div>`;
    }).join("") : '<div style="color:var(--text-muted);text-align:center;padding:1rem">No players in shortlist</div>';

    updateSnapshotStatus();
    renderScoutingWorkspaceStatus();
}

function queueStatusKey(player) {
    return String(player.player_id || player.player_name || player.name || "");
}

function getQueueStatus(player) {
    const stableKey = queueStatusKey(player);
    const nameKey = String(player.player_name || player.name || "");
    const localStatus = scoutQueueStatuses[stableKey] || scoutQueueStatuses[nameKey];
    if (STATUS_CYCLE.includes(localStatus)) return localStatus;
    const apiStatus = String(player.review_status || "pending").toLowerCase();
    return STATUS_CYCLE.includes(apiStatus) ? apiStatus : "pending";
}

function filterReviewQueue(queue) {
    const query = appState.scoutingQuery.trim().toLowerCase();
    return queue.filter((player) => {
        const statusMatch = appState.scoutingStatus === "ALL" || getQueueStatus(player) === appState.scoutingStatus;
        const haystack = [player.player_name, player.name, player.team, player.league, player.position_group, player.reason_code]
            .join(" ").toLowerCase();
        return statusMatch && (!query || haystack.includes(query));
    });
}

function mergeScoutingRows(serverRows, localRows) {
    const merged = [];
    const seen = new Set();
    for (const row of [...(serverRows || []), ...(localRows || [])]) {
        const name = row.player_name || row.name || "";
        const key = String(row.player_id || row.key || name).toLowerCase();
        if (!key || seen.has(key)) continue;
        seen.add(key);
        merged.push({
            ...row,
            player_name: name,
            position_group: row.position_group || row.position || "",
            optimized_score: Number(row.optimized_score || row.rating || 0),
            confidence_level: (row.confidence_level || row.confidence || "MEDIUM").toUpperCase(),
            reason_code: row.reason_code || (row.key ? "manual_selection" : ""),
        });
    }
    return merged;
}

function sortReviewQueue(queue, mode) {
    const arr = [...queue];
    if (mode === "priority") {
        const confOrder = { "LOW": 0, "MEDIUM": 1, "HIGH": 2 };
        arr.sort((a, b) => {
            const sa = getQueueStatus(a);
            const sb = getQueueStatus(b);
            const siA = STATUS_CYCLE.indexOf(sa);
            const siB = STATUS_CYCLE.indexOf(sb);
            if (siA !== siB) return siA - siB;
            const ca = confOrder[(a.confidence_level || a.confidence || "LOW").toUpperCase()] ?? 1;
            const cb = confOrder[(b.confidence_level || b.confidence || "LOW").toUpperCase()] ?? 1;
            return ca - cb;
        });
    } else if (mode === "name") {
        arr.sort((a, b) => (a.player_name || a.name || "").localeCompare(b.player_name || b.name || ""));
    } else if (mode === "date") {
        arr.sort((a, b) => String(b.as_of_date || "").localeCompare(String(a.as_of_date || "")) || (b.minutes || 0) - (a.minutes || 0));
    }
    return arr;
}

function computeLeagueCoverage() {
    const byLeagueSeason = {};
    for (const p of players) {
        const league = p.league || "";
        const season = p.season || "";
        if (!league) continue;
        const key = `${league}|${season}`;
        if (!byLeagueSeason[key]) byLeagueSeason[key] = { league, season, teams: new Set(), ratedTeams: new Set() };
        byLeagueSeason[key].teams.add(p.team);
        if (p.rating > 0 && p.team) byLeagueSeason[key].ratedTeams.add(p.team);
    }
    // Group by league (aggregate seasons)
    const byLeague = {};
    for (const entry of Object.values(byLeagueSeason)) {
        if (!byLeague[entry.league]) byLeague[entry.league] = { total: 0, rated: 0 };
        byLeague[entry.league].total += entry.teams.size;
        byLeague[entry.league].rated += entry.ratedTeams.size;
    }
    return Object.entries(byLeague).map(([league, data]) => ({
        league,
        rated: data.rated,
        total: data.total,
        coverage: data.total > 0 ? data.rated / data.total : 0,
    })).sort((a, b) => a.league.localeCompare(b.league));
}

function renderOverview() {
    const health = artifactSummary.data_health || {};
    const healthItems = document.querySelectorAll("#data-health-list .health-item");
    if (healthItems.length >= 3) {
        const oofBadge = healthItems[0].querySelector(".status-pill");
        oofBadge.className = `status-pill ${health.oof_available ? "status-high" : "status-low"}`;
        oofBadge.textContent = health.oof_available ? "HIGH" : "LOW";
        const oofText = healthItems[0].querySelector("span[data-i18n='health_oof']");
        if (oofText) {
            oofText.textContent = health.oof_available
                ? (appState.lang === "zh" ? "身价 OOF 可用" : "Value OOF available")
                : (appState.lang === "zh" ? "身价 OOF 未生成" : "Value OOF not generated");
        }

        const proxyBadge = healthItems[1].querySelector(".status-pill");
        proxyBadge.className = `status-pill ${health.player_match_coverage ? "status-medium" : "status-low"}`;
        proxyBadge.textContent = health.player_match_coverage ? "MED" : "LOW";
        healthItems[1].querySelector("span[data-i18n='health_proxy']").textContent = health.player_match_coverage || t("health_proxy");

        const truthBadge = healthItems[2].querySelector(".status-pill");
        truthBadge.className = `status-pill ${health.truth_labels_available ? "status-high" : "status-low"}`;
        truthBadge.textContent = health.truth_labels_available ? "HIGH" : "LOW";
        const truthText = healthItems[2].querySelector("span[data-i18n='health_truth']");
        if (truthText) {
            truthText.textContent = health.truth_labels_available
                ? (appState.lang === "zh" ? "真实标签可用" : "Truth labels available")
                : (appState.lang === "zh" ? "真实标签未生成" : "Truth labels not generated");
        }
    }

    const overallBadge = document.querySelector("#view-overview .compact-panel .panel-head .status-pill");
    if (overallBadge) {
        const overallHigh = health.oof_available && health.truth_labels_available;
        overallBadge.className = `status-pill ${overallHigh ? "status-high" : "status-medium"}`;
        overallBadge.textContent = overallHigh ? "HIGH" : "MED";
    }

    // Confidence gate
    const gatePill = document.getElementById("confidence-gate-pill");
    if (gatePill && health.confidence_gate) {
        gatePill.textContent = "< 0.90 → LOW";
        gatePill.title = health.confidence_gate;
    }

    // License attribution from API
    const licenses = artifactSummary.license_attribution;
    if (licenses) {
        const licenseList = document.getElementById("license-list");
        if (licenseList) {
            const entries = Object.entries(licenses);
            licenseList.innerHTML = entries.map(([key, desc]) =>
                `<li class="health-item"><span class="dot status-high"></span><span title="${escapeAttr(desc)}">${escapeHtml(key)}</span></li>`
            ).join("");
        }
    }

    // ── Confidence Gate Section ──
    const gateSection = document.getElementById("confidence-gate-section");
    if (gateSection) {
        const pmCoverage = health.player_match_coverage || "";
        const hasMatch = pmCoverage.includes("real");
        const hasProxy = pmCoverage.includes("proxy");
        const dsLabel = artifactSummary.data_source_label || "";

        // Data source labels
        const sourceLabels = [
            { label: hasMatch ? t("data_type_real") : t("data_type_proxy"), cls: hasMatch ? "status-high" : "status-medium" },
            { label: dsLabel || "local parquet", cls: "status-medium" },
        ];

        // License attribution summary
        const licEntries = licenses ? Object.entries(licenses) : [];

        // Coverage by league
        const leagueCoverage = computeLeagueCoverage();

        let html = '<div class="panel-head"><h3>' + escapeHtml(t("confidence_gate")) + '</h3>';
        html += '<span class="status-pill status-medium">' + escapeHtml(t("confidence_gate_desc")) + '</span></div>';

        // Data source labels row
        html += '<div style="display:flex;gap:0.5rem;flex-wrap:wrap;margin-bottom:0.6rem">';
        sourceLabels.forEach(s => {
            html += `<span class="status-pill ${s.cls}">${escapeHtml(s.label)}</span>`;
        });
        html += '</div>';

        // License attribution summary
        if (licEntries.length > 0) {
            html += '<p style="font-size:0.72rem;color:var(--text-muted);text-transform:uppercase;letter-spacing:0.04em;margin:0.3rem 0">' + escapeHtml(t("license_sources_label")) + '</p>';
            html += '<div style="display:flex;gap:0.4rem;flex-wrap:wrap;margin-bottom:0.6rem">';
            licEntries.forEach(([key]) => {
                html += `<span class="status-pill status-medium">${escapeHtml(key)}</span>`;
            });
            html += '</div>';
        }

        // Coverage by league
        if (leagueCoverage.length > 0) {
            html += '<p style="font-size:0.72rem;color:var(--text-muted);text-transform:uppercase;letter-spacing:0.04em;margin:0.3rem 0">' + escapeHtml(t("coverage_league")) + '</p>';
            html += '<div style="display:grid;grid-template-columns:1fr auto auto auto;gap:0.2rem 0.6rem;font-size:0.78rem">';
            leagueCoverage.forEach(lc => {
                const pctColor = lc.coverage > 0.90 ? "status-high" : (lc.coverage >= 0.70 ? "status-medium" : "status-low");
                const pctLabel = lc.coverage > 0.90 ? "HIGH" : (lc.coverage >= 0.70 ? "MED" : "LOW");
                html += `<span>${escapeHtml(lc.league)}</span>`;
                html += `<span>${escapeHtml(String(lc.rated))}/${escapeHtml(String(lc.total))}</span>`;
                html += `<span class="status-pill ${pctColor}">${Math.round(lc.coverage * 100)}%</span>`;
                html += `<span class="status-pill ${pctColor}">${pctLabel}</span>`;
            });
            html += '</div>';
        }

        // Link to license page
        html += '<div style="margin-top:0.5rem"><a href="#" onclick="setView(\'license\');return false" style="color:var(--accent);font-size:0.78rem">' + escapeHtml(appState.lang === "zh" ? "查看完整数据源详情" : "View full data source details") + '</a></div>';

        gateSection.innerHTML = html;
    }
}

function _fmtMetric(value, decimals) {
    if (value == null) return "–";
    return safeNum(value, decimals != null ? decimals : 3);
}

function _metricColor(metricKey, value) {
    if (value == null) return "var(--text-muted)";
    const v = Number(value);
    if (metricKey === "spearman" || metricKey === "pearson") {
        if (v >= 0.7) return "var(--accent, #4caf50)";
        if (v >= 0.5) return "var(--text, #ccc)";
        return "var(--warn, #ff9800)";
    }
    return "var(--text, #ccc)";
}

function _renderMetricCell(label, value, decimals, metricKey) {
    const formatted = _fmtMetric(value, decimals);
    const color = _metricColor(metricKey, value);
    return `<div><span style="color:var(--text-muted)">${escapeHtml(label)}</span><br><strong style="color:${color}">${escapeHtml(formatted)}</strong></div>`;
}

function _renderMetricsBlock(title, m, decimals) {
    if (!m || Object.keys(m).length === 0) return "";
    const d = decimals != null ? decimals : 3;
    const cells = [
        _renderMetricCell("Spearman", m.spearman, d, "spearman"),
        _renderMetricCell("Pearson", m.pearson, d, "pearson"),
        _renderMetricCell("Rank loss", m.rank_loss, d),
        _renderMetricCell("Cal MAE", m.calibration_mae, 1),
        _renderMetricCell("Pts MAE", m.points_mae, 1),
        _renderMetricCell("Pts RMSE", m.points_rmse, 1),
    ];
    if (m.n_players != null) cells.push(_renderMetricCell("Players", m.n_players, 0));
    if (m.n_team_seasons != null) cells.push(_renderMetricCell("Team-seas", m.n_team_seasons, 0));
    return `<p style="margin:0.4rem 0 0.15rem;font-size:0.72rem;color:var(--text-muted);text-transform:uppercase;letter-spacing:0.04em">${escapeHtml(title)}</p>
    <div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(6rem,1fr));gap:0.25rem 0.6rem;font-size:0.78rem">${cells.join("")}</div>`;
}

function _renderParamsGrid(args) {
    if (!args || Object.keys(args).length === 0) return "";
    const knownEntries = [
        ["pop_size", "pop"],
        ["n_steps", "steps"],
        ["lr", "lr"],
        ["patience", "patience"],
        ["warmup_steps", "warmup"],
        ["grad_clip", "grad clip"],
        ["min_lr_ratio", "min lr"],
        ["spearman_weight", "sp wt"],
        ["ndcg_weight", "ndcg wt"],
        ["position_consistency_weight", "pos wt"],
        ["points_regression_weight", "pts wt"],
        ["distribution_weight", "dist wt"],
        ["quantile_weight", "quant wt"],
        ["range_penalty_weight", "range wt"],
        ["tail_calibration_weight", "tail wt"],
        ["league_bias_weight", "league wt"],
        ["extreme_penalty_weight", "extreme wt"],
        ["prior_weight", "prior wt"],
        ["dc_likelihood_weight", "dc wt"],
        ["dc_rho", "dc rho"],
        ["league_calibration_prior_n", "cal prior"],
        ["league_calibration_cap", "cal cap"],
    ];
    const knownKeys = new Set(knownEntries.map(([k]) => k));
    // Known params first
    const cells = knownEntries
        .filter(([key]) => args[key] != null)
        .map(([key, label]) => {
            const v = args[key];
            const formatted = typeof v === "boolean" ? (v ? "on" : "off") : String(v);
            return `<div><span style="color:var(--text-muted)">${escapeHtml(label)}</span><br><span>${escapeHtml(formatted)}</span></div>`;
        });
    // Remaining params not in known list (full parameter dump)
    const extraCells = Object.entries(args)
        .filter(([key]) => !knownKeys.has(key) && args[key] != null)
        .map(([key, v]) => {
            const formatted = typeof v === "boolean" ? (v ? "on" : "off") : String(v);
            return `<div><span style="color:var(--text-muted)">${escapeHtml(key)}</span><br><span>${escapeHtml(formatted)}</span></div>`;
        });
    const allCells = [...cells, ...extraCells];
    if (allCells.length === 0) return "";
    return `<p style="margin:0.4rem 0 0.15rem;font-size:0.72rem;color:var(--text-muted);text-transform:uppercase;letter-spacing:0.04em">Parameters (${allCells.length})</p>
    <div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(5.5rem,1fr));gap:0.2rem 0.5rem;font-size:0.75rem">${allCells.join("")}</div>`;
}

function _renderPositionMetrics(posMetrics) {
    if (!posMetrics || Object.keys(posMetrics).length === 0) return "";
    const rows = Object.entries(posMetrics).map(([pos, m]) => {
        return `<tr>
            <td style="padding:0.15rem 0.4rem;font-weight:600">${escapeHtml(pos)}</td>
            <td style="padding:0.15rem 0.4rem">${_fmtMetric(m.spearman)}</td>
            <td style="padding:0.15rem 0.4rem">${_fmtMetric(m.pearson)}</td>
            <td style="padding:0.15rem 0.4rem">${m.n_players != null ? Math.round(m.n_players) : "–"}</td>
        </tr>`;
    });
    return `<p style="margin:0.4rem 0 0.15rem;font-size:0.72rem;color:var(--text-muted);text-transform:uppercase;letter-spacing:0.04em">Position-wise</p>
    <table style="font-size:0.75rem;width:100%;border-collapse:collapse">
        <thead><tr style="color:var(--text-muted)">
            <th style="text-align:left;padding:0.15rem 0.4rem">Pos</th>
            <th style="text-align:left;padding:0.15rem 0.4rem">Spearman</th>
            <th style="text-align:left;padding:0.15rem 0.4rem">Pearson</th>
            <th style="text-align:left;padding:0.15rem 0.4rem">N</th>
        </tr></thead>
        <tbody>${rows.join("")}</tbody>
    </table>`;
}

function _renderErrorCases(errorCases) {
    if (!errorCases) return "";
    const parts = [];
    const over = errorCases.over_estimated || [];
    const under = errorCases.under_estimated || [];
    if (over.length > 0) {
        const items = over.slice(0, 5).map((e) => {
            const team = e.team || e.team_name || "?";
            const residual = e.residual != null ? Number(e.residual).toFixed(1) : "";
            return `${escapeHtml(team)}${residual ? " (+" + residual + ")" : ""}`;
        }).join(", ");
        parts.push(`<div><span style="color:var(--text-muted)">Over-estimated:</span> ${items}</div>`);
    }
    if (under.length > 0) {
        const items = under.slice(0, 5).map((e) => {
            const team = e.team || e.team_name || "?";
            const residual = e.residual != null ? Number(e.residual).toFixed(1) : "";
            return `${escapeHtml(team)}${residual ? " (" + residual + ")" : ""}`;
        }).join(", ");
        parts.push(`<div><span style="color:var(--text-muted)">Under-estimated:</span> ${items}</div>`);
    }
    if (parts.length === 0) return "";
    return `<p style="margin:0.4rem 0 0.15rem;font-size:0.72rem;color:var(--text-muted);text-transform:uppercase;letter-spacing:0.04em">Error cases</p>
    <div style="font-size:0.75rem;line-height:1.5">${parts.join("")}</div>`;
}

function _posGroupRating(team, group) {
    const pg = (team.position_groups || {})[group];
    return pg ? pg.rating : null;
}

function _posGroupCount(team, group) {
    const pg = (team.position_groups || {})[group];
    return pg ? pg.player_count : 0;
}

function _ratingCell(rating) {
    if (rating === null || rating === undefined || isNaN(rating)) {
        return '<span style="color:var(--text-muted)">—</span>';
    }
    const cls = rating >= 60 ? "status-high" : rating >= 45 ? "status-medium" : "status-low";
    return `<span class="status-pill ${cls}">${rating.toFixed(1)}</span>`;
}

async function renderTeams() {
    const tbody = document.getElementById("teams-table-body");
    if (!tbody) return;

    // Fetch data if not loaded
    if (teamStrengthData.count === 0) {
        tbody.innerHTML = '<tr><td colspan="9" style="text-align:center;color:var(--text-muted)">Loading...</td></tr>';
        try {
            teamStrengthData = await fetchTeamStrength();
        } catch {
            tbody.innerHTML = '<tr><td colspan="9" style="text-align:center;color:var(--text-muted)">Failed to load</td></tr>';
            return;
        }
    }

    const teams = teamStrengthData.teams || [];
    if (teams.length === 0) {
        tbody.innerHTML = '<tr><td colspan="9" style="text-align:center;color:var(--text-muted)">No data</td></tr>';
        return;
    }

    // Update summary metrics
    const countEl = document.getElementById("teams-count");
    const avgEl = document.getElementById("teams-avg-rating");
    const topEl = document.getElementById("teams-top-rating");
    if (countEl) countEl.textContent = teams.length;
    const ratings = teams.map(t => t.overall_rating || 0);
    const avg = ratings.length > 0 ? ratings.reduce((a, b) => a + b, 0) / ratings.length : 0;
    const top = ratings.length > 0 ? Math.max(...ratings) : 0;
    if (avgEl) avgEl.textContent = avg.toFixed(1);
    if (topEl) topEl.textContent = top.toFixed(1);

    // Populate league filter
    const leagueFilter = document.getElementById("teams-league-filter");
    if (leagueFilter && leagueFilter.options.length <= 1) {
        const leagues = [...new Set(teams.map(t => t.league).filter(Boolean))].sort();
        leagues.forEach(lg => {
            const opt = document.createElement("option");
            opt.value = lg;
            opt.textContent = lg;
            leagueFilter.appendChild(opt);
        });
    }

    // Filter by league
    const selectedLeague = leagueFilter ? leagueFilter.value : "";
    const filtered = selectedLeague ? teams.filter(t => t.league === selectedLeague) : teams;

    // Render table
    tbody.innerHTML = filtered.map((team, i) => {
        return `
        <tr style="cursor:pointer" data-team="${escapeAttr(team.team)}">
            <td>${i + 1}</td>
            <td>${escapeHtml(team.team)}</td>
            <td>${escapeHtml(team.league || "—")}</td>
            <td><strong>${(team.overall_rating || 0).toFixed(1)}</strong></td>
            <td>${team.squad_size || 0}</td>
            <td>${_ratingCell(_posGroupRating(team, "GK"))}</td>
            <td>${_ratingCell(_posGroupRating(team, "DEF"))}</td>
            <td>${_ratingCell(_posGroupRating(team, "MID"))}</td>
            <td>${_ratingCell(_posGroupRating(team, "ATT"))}</td>
        </tr>`;
    }).join("");

    // Row click handler
    tbody.querySelectorAll("tr[data-team]").forEach(row => {
        row.addEventListener("click", () => {
            const teamName = row.dataset.team;
            const team = filtered.find(t => t.team === teamName);
            if (team) renderTeamDetail(team);
        });
    });

    // League filter handler
    if (leagueFilter) {
        leagueFilter.onchange = () => renderTeams();
    }

    // Render chart
    renderTeamsChart(filtered);
}

function renderTeamDetail(team) {
    const content = document.getElementById("teams-detail-content");
    const pill = document.getElementById("teams-detail-pill");
    if (!content) return;

    const posGroups = ["GK", "DEF", "MID", "ATT"];
    const posBreakdown = posGroups.map(g => {
        const pg = (team.position_groups || {})[g];
        if (!pg) return "";
        return `
        <div style="display:flex;justify-content:space-between;align-items:center;padding:0.3rem 0;border-bottom:1px solid var(--border)">
            <span style="font-weight:600">${g}</span>
            <span>${_ratingCell(pg.rating)} <span style="color:var(--text-muted);font-size:0.8rem">(${pg.player_count} players)</span></span>
        </div>`;
    }).join("");

    const topPlayers = (team.top_players || []).map(p => {
        return `
        <tr>
            <td>${escapeHtml(p.name)}</td>
            <td>${escapeHtml(p.position || "—")}</td>
            <td>${(p.rating || 0).toFixed(1)}</td>
            <td>${p.minutes || 0}</td>
            <td><span class="status-pill ${(p.confidence || "LOW").toUpperCase() === "HIGH" ? "status-high" : (p.confidence || "LOW").toUpperCase() === "MEDIUM" ? "status-medium" : "status-low"}">${escapeHtml(p.confidence || "LOW")}</span></td>
        </tr>`;
    }).join("");

    content.innerHTML = `
        <h4 style="margin:0 0 0.5rem">${escapeHtml(team.team)}</h4>
        <p style="color:var(--text-muted);margin:0 0 0.5rem">${escapeHtml(team.league || "—")} · ${escapeHtml(team.season || "—")}</p>
        <div style="margin:0.5rem 0">
            <strong>${(team.overall_rating || 0).toFixed(1)}</strong> overall · ${team.squad_size || 0} players · ${team.total_minutes || 0} total minutes
        </div>
        <div style="margin:0.8rem 0">${posBreakdown}</div>
        ${topPlayers ? `
        <p style="margin:0.8rem 0 0.3rem;font-size:0.72rem;color:var(--text-muted);text-transform:uppercase;letter-spacing:0.04em">Top Players</p>
        <table class="data-table" style="font-size:0.8rem">
            <thead><tr><th>Name</th><th>Pos</th><th>Rating</th><th>Min</th><th>Conf</th></tr></thead>
            <tbody>${topPlayers}</tbody>
        </table>` : ""}`;
    if (pill) pill.textContent = (team.overall_rating || 0).toFixed(1);
}

function renderTeamsChart(teams) {
    const chartEl = document.getElementById("teams-chart");
    if (!chartEl || typeof echarts === "undefined") return;

    // Show top 15 teams
    const top = teams.slice(0, 15);
    const chart = echarts.init(chartEl);
    if (appState.charts.teams) appState.charts.teams.dispose();
    appState.charts.teams = chart;

    const teamNames = top.map(t => t.team);
    const series = ["GK", "DEF", "MID", "ATT"].map(group => ({
        name: group,
        type: "bar",
        stack: "total",
        data: top.map(t => {
            const pg = (t.position_groups || {})[group];
            return pg ? pg.rating : 0;
        }),
    }));

    chart.setOption({
        tooltip: { trigger: "axis", axisPointer: { type: "shadow" } },
        legend: { data: ["GK", "DEF", "MID", "ATT"], bottom: 0 },
        grid: { left: "3%", right: "4%", bottom: "15%", containLabel: true },
        xAxis: { type: "category", data: teamNames, axisLabel: { rotate: 45, fontSize: 10 } },
        yAxis: { type: "value", name: "Rating" },
        series: series,
    });
}

function renderReports() {
    const latestRun = (modelRuns.runs || [])[0] || {};
    const latestMetrics = latestRun.metrics || {};
    const holdoutSummary = latestRun.holdout_summary || {};
    const optTest = holdoutSummary.optimized_test || {};
    const runSpearman = optTest.spearman ?? latestMetrics.spearman ?? latestRun.spearman;
    const runStatus = runSpearman != null ? `Spearman ${Number(runSpearman).toFixed(3)}` : "no metrics";
    document.getElementById("report-run-title").textContent = latestRun.run_id || "rating_optimizer_gpu";
    document.getElementById("report-run-status").textContent = runStatus;
    document.getElementById("report-run-status").className = `status-pill ${runSpearman != null ? "status-high" : "status-low"}`;

    const valueMetrics = valueSummaryMeta.metrics || {};
    const valueImprovement = valueMetrics.mae_improvement_vs_baseline;
    const valueIsDemo = valueSummaryMeta.status === "demo";
    document.getElementById("report-value-title").textContent = valueMetrics.estimator || "value_fairness_oof";
    document.getElementById("report-value-status").textContent = valueIsDemo
        ? "DEMO"
        : (valueImprovement ? `+${Math.round(valueImprovement).toLocaleString()} MAE` : "ready");
    document.getElementById("report-value-status").className = `status-pill ${valueIsDemo ? "status-medium" : (valueSummaryMeta.sample_count > 0 ? "status-high" : "status-low")}`;

    const predictionReady = predictionMeta.status === "ok";
    const dcReady = (predictionMeta.dixon_coles || {}).status === "ok";
    const predictionLabel = predictionReady
        ? `${predictionMeta.model_type || "independent_poisson"} · ${predictionMeta.num_teams || 0} teams`
        : "no artifact";
    const dcLabel = dcReady
        ? `DC: rho=${((predictionMeta.dixon_coles || {}).rho || 0).toFixed(3)}`
        : "";
    document.getElementById("report-prediction-title").textContent = predictionReady
        ? (dcReady ? "Poisson + Dixon-Coles" : "Poisson baseline")
        : "prediction";
    document.getElementById("report-prediction-status").textContent = dcReady
        ? `${predictionLabel} | ${dcLabel}`
        : predictionLabel;
    document.getElementById("report-prediction-status").className = `status-pill ${predictionReady ? "status-medium" : "status-low"}`;

    document.getElementById("model-runs-count").textContent = String(modelRuns.count || 0);
    const runList = document.getElementById("model-runs-list");
    const runs = (modelRuns.runs || []).slice(0, 12);
    runList.innerHTML = runs.length > 0
        ? runs.map((run) => {
            const z = appState.lang === "zh";
            const metrics = run.metrics || {};
            const args = run.args || {};
            const hs = run.holdout_summary || {};
            const optTest = hs.optimized_test || {};
            const baseTest = hs.baseline_test || {};
            const optTrain = hs.optimized_train || {};
            const baseTrain = hs.baseline_train || {};
            // Top-level flat aliases from enrichment
            const spearman = optTest.spearman ?? metrics.spearman ?? run.spearman;
            const pearson = optTest.pearson ?? metrics.pearson ?? run.pearson;
            const hash = run.input_hash || "n/a";
            const seed = args.seed ?? run.seed ?? "–";
            const nPlayers = optTest.n_players ?? metrics.n_players ?? run.n_players ?? "–";
            const nTeamSeasons = optTest.n_team_seasons ?? metrics.n_team_seasons ?? run.n_team_seasons ?? "–";
            const coverage = optTest.team_coverage ?? metrics.team_coverage ?? run.team_coverage;
            const dataSource = run.data_source || "";
            const overfitGap = hs.overfit_rank_loss_gap;

            // Header status
            const statusText = spearman != null ? "READY" : "N/A";
            const statusClass = spearman != null ? "status-high" : "status-low";

            // Details row
            const detailParts = [
                `<span style="color:var(--text-muted)">hash</span> ${escapeHtml(hash)}`,
                `<span style="color:var(--text-muted)">seed</span> ${escapeHtml(String(seed))}`,
                `<span style="color:var(--text-muted)">players</span> ${escapeHtml(String(nPlayers))}`,
                `<span style="color:var(--text-muted)">team-seas</span> ${escapeHtml(String(nTeamSeasons))}`,
            ];
            if (coverage != null) {
                detailParts.push(`<span style="color:var(--text-muted)">coverage</span> ${(coverage * 100).toFixed(1)}%`);
            }
            if (overfitGap != null) {
                detailParts.push(`<span style="color:var(--text-muted)">overfit gap</span> ${Number(overfitGap).toFixed(3)}`);
            }
            if (dataSource) {
                detailParts.push(`<span style="color:var(--text-muted)">source</span> ${escapeHtml(dataSource)}`);
            }

            // Metrics blocks
            const optTestHtml = _renderMetricsBlock("Optimized (test)", optTest);
            const baseTestHtml = _renderMetricsBlock("Baseline (test)", baseTest);
            const optTrainHtml = _renderMetricsBlock("Optimized (train)", optTrain);
            const baseTrainHtml = _renderMetricsBlock("Baseline (train)", baseTrain);

            // Parameters grid
            const paramsHtml = _renderParamsGrid(args);

            // Position-wise metrics
            const posMetrics = run.position_metrics || run.position_metrics_by_group || {};
            const posHtml = _renderPositionMetrics(posMetrics);

            // Error cases
            const errorHtml = _renderErrorCases(run.error_cases);

            // Reproduce command
            const cmd = run.reproduce_command || "";
            const cmdHtml = cmd
                ? `<p style="margin:0.4rem 0 0.15rem;font-size:0.72rem;color:var(--text-muted);text-transform:uppercase;letter-spacing:0.04em">Reproduce</p>
                   <pre style="margin:0;padding:0.35rem 0.5rem;background:var(--bg-alt,#1a1a2e);border-radius:4px;font-size:0.72rem;overflow-x:auto;white-space:pre-wrap;word-break:break-all;font-family:monospace;color:var(--text,#ccc)">${escapeHtml(cmd)}</pre>`
                : "";

            // Assemble detail block (everything below the header)
            // Season split (train/test)
            const trainSeasons = run.train_seasons || args.train_seasons || run.season_split?.train || null;
            const testSeasons = run.test_seasons || args.test_seasons || run.season_split?.test || null;
            let seasonSplitHtml = '';
            if (trainSeasons || testSeasons) {
                const z2 = appState.lang === 'zh';
                seasonSplitHtml = `<p style="margin:0.4rem 0 0.15rem;font-size:0.72rem;color:var(--text-muted);text-transform:uppercase;letter-spacing:0.04em">${z2 ? '训练/测试赛季' : 'Train/Test seasons'}</p>`;
                seasonSplitHtml += `<div style="font-size:0.75rem;line-height:1.5">`;
                if (trainSeasons) {
                    const label = Array.isArray(trainSeasons) ? trainSeasons.join(', ') : String(trainSeasons);
                    seasonSplitHtml += `<div><span style="color:var(--text-muted)">${z2 ? '训练' : 'Train'}:</span> ${escapeHtml(label)}</div>`;
                }
                if (testSeasons) {
                    const label = Array.isArray(testSeasons) ? testSeasons.join(', ') : String(testSeasons);
                    seasonSplitHtml += `<div><span style="color:var(--text-muted)">${z2 ? '测试' : 'Test'}:</span> ${escapeHtml(label)}</div>`;
                }
                seasonSplitHtml += `</div>`;
            }

            // Feature importance top 5
            const featImp = run.feature_importance || run.feature_importances || args.feature_importance || null;
            let featImpHtml = '';
            if (featImp && typeof featImp === 'object') {
                const entries = Array.isArray(featImp)
                    ? featImp.slice(0, 5)
                    : Object.entries(featImp)
                        .sort((a, b) => Math.abs(b[1]) - Math.abs(a[1]))
                        .slice(0, 5)
                        .map(([k, v]) => ({ name: k, importance: v }));
                if (entries.length > 0) {
                    const z3 = appState.lang === 'zh';
                    featImpHtml = `<p style="margin:0.4rem 0 0.15rem;font-size:0.72rem;color:var(--text-muted);text-transform:uppercase;letter-spacing:0.04em">${z3 ? '特征重要性 Top 5' : 'Feature importance Top 5'}</p>`;
                    featImpHtml += `<div style="font-size:0.75rem;line-height:1.6">`;
                    entries.forEach((e, i) => {
                        const name = typeof e === 'object' ? (e.name || e.feature || Object.keys(e)[0] || `f${i}`) : String(e);
                        const val = typeof e === 'object' ? (e.importance ?? e.value ?? Object.values(e)[0] ?? 0) : 0;
                        const pct = typeof val === 'number' && val <= 1 && val >= 0 ? (val * 100).toFixed(1) + '%' : Number(val).toFixed(3);
                        featImpHtml += `<div>\u25C6 ${escapeHtml(String(name))} <span style="color:var(--text-muted)">${escapeHtml(pct)}</span></div>`;
                    });
                    featImpHtml += `</div>`;
                }
            }

            const detailSections = [optTestHtml, baseTestHtml, optTrainHtml, baseTrainHtml, seasonSplitHtml, paramsHtml, featImpHtml, posHtml, errorHtml, cmdHtml]
                .filter(Boolean)
                .join("<hr style=\"border:none;border-top:1px solid var(--border,#333);margin:0.35rem 0\">");

            // Dependency versions
            const depVersions = run.dependency_versions || run.dependencies || args.dependency_versions || null;
            let depHtml = '';
            if (depVersions && typeof depVersions === 'object') {
                const z4 = appState.lang === 'zh';
                depHtml = `<p style="margin:0.4rem 0 0.15rem;font-size:0.72rem;color:var(--text-muted);text-transform:uppercase;letter-spacing:0.04em">${z4 ? '依赖版本' : 'Dependency versions'}</p>`;
                depHtml += `<div style="font-size:0.75rem;line-height:1.5">`;
                for (const [k, v] of Object.entries(depVersions)) {
                    depHtml += `<div><span style="color:var(--text-muted)">${escapeHtml(k)}:</span> ${escapeHtml(String(v))}</div>`;
                }
                depHtml += `</div>`;
            }

            // Reproduce command for copy button
            const copyBtn = cmd
                ? `<button class="text-button" data-copy-cmd="${escapeAttr(cmd)}" style="font-size:0.72rem;padding:0.15rem 0.4rem;margin-left:0.3rem" title="${z ? '复制命令' : 'Copy command'}">\u25C6 ${z ? '复制' : 'Copy'}</button>`
                : '';

            const fullDetailSections = [depHtml, detailSections].filter(Boolean)
                .join("<hr style=\"border:none;border-top:1px solid var(--border,#333);margin:0.35rem 0\">");

            const runIdx = run.run_id || `run_${Math.random().toString(36).slice(2, 8)}`;

            return `
            <div style="padding:0.6rem 0.8rem;border-bottom:1px solid var(--border,#333)">
                <div style="display:flex;align-items:center;gap:0.5rem;flex-wrap:wrap">
                    <strong style="font-size:0.85rem">${escapeHtml(run.run_id || "run")}</strong>
                    <span class="status-pill ${statusClass}">${statusText}</span>
                    ${spearman != null ? `<span style="font-size:0.78rem;color:var(--text-muted)">sp ${Number(spearman).toFixed(3)} / pr ${_fmtMetric(pearson)}</span>` : ""}
                    ${copyBtn}
                    ${fullDetailSections ? `<button class="text-button" data-toggle-run="${escapeAttr(runIdx)}" style="font-size:0.72rem;padding:0.15rem 0.4rem;margin-left:auto">\u25B6 ${z ? '展开详情' : 'Expand'}</button>` : ""}
                </div>
                <div style="font-size:0.75rem;color:var(--text-muted);margin-top:0.2rem;line-height:1.6">${detailParts.join(" · ")}</div>
                ${fullDetailSections ? `<div class="run-details-collapsed" data-run-details="${escapeAttr(runIdx)}" style="display:none;margin-top:0.35rem">${fullDetailSections}</div>` : ""}
            </div>`;
        }).join("")
        : '<div style="color:var(--text-muted);text-align:center;padding:1rem">No model runs found</div>';

    // Board Snapshots section
    var snapshotsList = document.getElementById("board-snapshots-list");
    var snapshotsCount = document.getElementById("board-snapshots-count");
    if (snapshotsList && typeof TACTICAL_BOARD !== "undefined") {
        var projects = TACTICAL_BOARD.listProjects();
        if (snapshotsCount) snapshotsCount.textContent = String(projects.length);
        snapshotsList.innerHTML = projects.length > 0
            ? projects.map(function(p) {
                var date = p.updated_at ? new Date(p.updated_at).toLocaleDateString() : "";
                var notes = "";
                try {
                    var full = TACTICAL_BOARD.loadProject(p.board_id);
                    if (full) {
                        var cp = full.coaching_points || (full.frames && full.frames[0] && full.frames[0].notes);
                        if (typeof cp === "string") notes = cp.slice(0, 80);
                        else if (cp && cp.title) notes = cp.title + (cp.description ? ": " + cp.description.slice(0, 50) : "");
                    }
                } catch (ex) { /* ignore */ }
                return '<div class="rank-item" data-load-board="' + escapeAttr(p.board_id) + '" style="cursor:pointer">' +
                    '<div>' +
                        '<strong style="font-size:0.85rem">' + escapeHtml(p.title || "Untitled") + '</strong>' +
                        '<span class="rank-meta">' + (p.object_count || 0) + ' objects, ' + (p.frame_count || 0) + ' frames' + (date ? ' \u00b7 ' + date : '') + '</span>' +
                        (notes ? '<span class="rank-meta" style="display:block;font-style:italic;opacity:0.7">' + escapeHtml(notes) + '</span>' : '') +
                    '</div>' +
                    '<span class="status-pill status-medium">Board</span>' +
                '</div>';
            }).join("")
            : '<div style="color:var(--text-muted);text-align:center;padding:1rem">No board snapshots saved</div>';

        // Click handler: switch to tactical view and load project
        snapshotsList.querySelectorAll("[data-load-board]").forEach(function(el) {
            el.addEventListener("click", function() {
                var boardId = this.getAttribute("data-load-board");
                if (boardId && typeof switchView === "function") {
                    switchView("tactical");
                    var proj = TACTICAL_BOARD.loadProject(boardId);
                    if (proj && typeof TacticalRenderer !== "undefined") {
                        TacticalRenderer.project = proj;
                        TacticalRenderer.render();
                    }
                }
            });
        });
    }
}

function renderActions() {
    const chart = getChart("action-chart");
    const mode = appState.actionMode;
    const sourceRows = mode === "vaep"
        ? (actionValueSummary.vaep_players || [])
        : (actionValueSummary.xt_players || actionValueSummary.players || []);
    const metricKey = mode === "vaep" ? "vaep_per_90" : "xt_per_90";
    const legacyMetricKey = mode === "xt" ? "xT_per_90" : metricKey;
    const query = appState.actionQuery.trim().toLowerCase();
    const players = sourceRows.filter((player) => {
        const minutes = Number(player.estimated_minutes || player.minutes || 0);
        const competition = String(player.competition || "");
        const label = String(player.player_name || player.player_id || "");
        const matchesQuery = !query || `${label} ${competition} ${player.season || ""}`.toLowerCase().includes(query);
        const matchesCompetition = mode === "vaep" || appState.actionCompetition === "ALL" || competition === appState.actionCompetition;
        return matchesQuery && matchesCompetition && minutes >= appState.actionMinMinutes;
    }).sort((a, b) => Number(b[metricKey] ?? b[legacyMetricKey] ?? 0) - Number(a[metricKey] ?? a[legacyMetricKey] ?? 0));
    const actionList = document.getElementById("action-list");
    const actionStatus = document.getElementById("action-status-pill");
    const metrics = actionValueSummary.metrics || {};

    populateActionCompetitionFilter(sourceRows);

    document.querySelectorAll("[data-action-mode]").forEach((button) => {
        const active = button.dataset.actionMode === mode;
        button.classList.toggle("active", active);
        button.setAttribute("aria-pressed", active ? "true" : "false");
    });
    const competitionSelect = document.getElementById("action-competition-filter");
    if (competitionSelect) competitionSelect.disabled = mode === "vaep";

    const chartTitle = document.getElementById("action-chart-title");
    const listTitle = document.getElementById("action-list-title");
    if (chartTitle) chartTitle.textContent = mode === "vaep" ? "VAEP / 90" : "xT / 90";
    if (listTitle) listTitle.textContent = mode === "vaep"
        ? (appState.lang === "zh" ? "VAEP 排名" : "VAEP ranking")
        : (appState.lang === "zh" ? "xT 排名" : "xT ranking");

    if (actionStatus) {
        actionStatus.textContent = actionValueSummary.status === "ok"
            ? `${mode.toUpperCase()} ${players.length}`
            : "NO DATA";
        actionStatus.className = `status-pill ${actionValueSummary.status === "ok" ? "status-medium" : "status-low"}`;
    }

    const metricsEl = document.getElementById("action-metrics");
    if (metricsEl) {
        const coverage = mode === "vaep"
            ? (metrics.players_with_vaep ?? metrics.vaep_rows ?? sourceRows.length)
            : (metrics.players_with_xt ?? metrics.xt_rows ?? sourceRows.length);
        const mean = mode === "vaep" ? metrics.mean_vaep_per_90 : metrics.mean_xt_per_90;
        metricsEl.innerHTML = `
            <div><span class="metric-value">${Number(metrics.total_rows || actionValueSummary.count || sourceRows.length).toLocaleString()}</span><span>${escapeHtml(appState.lang === "zh" ? "动作价值行" : "action-value rows")}</span></div>
            <div><span class="metric-value">${Number(coverage || 0).toLocaleString()}</span><span>${escapeHtml(mode === "vaep" ? "VAEP coverage" : "xT coverage")}</span></div>
            <div><span class="metric-value">${mean == null ? "–" : safeNum(mean, 3)}</span><span>${escapeHtml(appState.lang === "zh" ? "样本均值 / 90" : "sample mean / 90")}</span></div>`;
    }

    actionList.innerHTML = players.length > 0
        ? players.map((player) => `
            <div class="rank-item">
                <div>
                    <strong>${escapeHtml(actionPlayerLabel(player, mode))}</strong>
                    <span class="rank-meta">${escapeHtml(actionPlayerMeta(player, mode))}</span>
                    ${Number(player.estimated_minutes || player.minutes || 0) < 900 ? `<div class="sample-warning">${escapeHtml(appState.lang === "zh" ? "小样本，仅供研究" : "Small sample; research use only")}</div>` : ""}
                </div>
                <span class="status-pill status-medium">${safeNum(player[metricKey] ?? player[legacyMetricKey] ?? 0, 3)}</span>
            </div>
        `).join("")
        : (() => {
            const loadFailed = dataLoadErrors.has("action-values");
            const msg = loadFailed
                ? (appState.lang === "zh" ? "数据加载失败（API 和静态缓存均不可用）" : "Data load failed (both API and static cache unavailable)")
                : (appState.lang === "zh" ? "当前筛选没有动作价值样本" : "No action-value samples match the current filters");
            return `<div style="color:var(--text-muted);text-align:center;padding:1rem">${escapeHtml(msg)}</div>`;
        })();

    // StatsBomb Open Data attribution
    const attrEl = document.getElementById('action-attribution');
    if (attrEl) {
        const apiAttr = actionValueSummary.attribution_required
            || (appState.lang === 'zh' ? '公开展示时必须注明数据来源' : 'Data source must be attributed in any public display');
        attrEl.innerHTML = `\u25C6 ${appState.lang === 'zh' ? '\u6570\u636E\u6765\u6E90' : 'Data source'}: StatsBomb Open Data | github.com/statsbomb/open-data<br><small>${escapeHtml(apiAttr)}</small>`;
    }

    if (!chart) return;
    const chartPlayers = players.filter((player) => (player.player_name || player.player_id) && (player[metricKey] ?? player[legacyMetricKey]) != null).slice(0, 20);
    if (chartPlayers.length === 0) {
        chart.clear();
        return;
    }
    chart.setOption({
        title: {
            text: appState.lang === "zh" ? "真实 StatsBomb 样本 · 非全量联赛能力" : "Real StatsBomb sample · Not full-league coverage",
            left: "center", top: 0,
            textStyle: { color: "rgba(255,180,60,.85)", fontSize: 12, fontWeight: 400 },
        },
        grid: { left: 56, right: 20, top: 34, bottom: 60 },
        xAxis: {
            type: "category",
            data: chartPlayers.map((player) => actionPlayerLabel(player, mode)),
            axisLabel: { color: chartTextColor(), rotate: 30 },
        },
        yAxis: {
            type: "value",
            name: mode === "vaep" ? "VAEP/90" : "xT/90",
            nameTextStyle: { color: chartTextColor() },
            axisLabel: { color: chartTextColor() },
            splitLine: { lineStyle: { color: chartGridColor() } },
        },
        series: [{
            type: "bar",
            data: chartPlayers.map((player) => Number(player[metricKey] ?? player[legacyMetricKey] ?? 0)),
            itemStyle: { color: mode === "vaep" ? "rgba(124,168,255,.82)" : "rgba(87,214,141,.78)" },
            label: { show: false },
        }],
    }, true);
    chart.resize();

    // Wire up "Show on Tactical Board" button for xT heatmap
    const btnXTHeatmap = document.getElementById("btn-xt-heatmap-tactical");
    const heatmapStatus = document.getElementById("xt-heatmap-status");
    if (btnXTHeatmap) {
        btnXTHeatmap.disabled = mode !== "xt" || sourceRows.length === 0;
        btnXTHeatmap.onclick = function() {
            if (!actionValueSummary || actionValueSummary.status === "no_data") {
                if (heatmapStatus) heatmapStatus.textContent = appState.lang === "zh" ? "\u65e0\u6570\u636e" : "No data available";
                return;
            }
            // Generate xT heatmap grid from action value data (12x8 standard grid)
            var xtGrid = generateXTHeatmapGrid(actionValueSummary);
            if (typeof TacticalRenderer !== "undefined") {
                TacticalRenderer.setXTHeatmapData(xtGrid);
                TacticalRenderer._showXTHeatmap = true;
                var toggleBtn = document.getElementById("tactical-toggle-heatmap");
                if (toggleBtn) toggleBtn.classList.add("active");
                // Update source_attribution to include StatsBomb when xT data is loaded
                if (tacticalProject && !String(tacticalProject.source_attribution || "").includes("StatsBomb")) {
                    tacticalProject.source_attribution = "ScoutFootball tactical board + StatsBomb Open Data (xT)";
                }
                // Navigate to tactical view
                setView("tactical");
                if (heatmapStatus) heatmapStatus.textContent = appState.lang === "zh" ? "\u5df2\u52a0\u8f7d" : "Loaded on tactical board";
            }
        };
    }
}

function populateActionCompetitionFilter(rows) {
    const select = document.getElementById("action-competition-filter");
    if (!select) return;
    const competitions = [...new Set((rows || []).map((row) => row.competition).filter(Boolean))].sort();
    const previous = appState.actionCompetition;
    select.innerHTML = `<option value="ALL">${escapeHtml(t("action_all_competitions"))}</option>`
        + competitions.map((competition) => `<option value="${escapeAttr(competition)}">${escapeHtml(competition)}</option>`).join("");
    appState.actionCompetition = competitions.includes(previous) ? previous : "ALL";
    select.value = appState.actionCompetition;
}

function actionPlayerLabel(player, mode) {
    if (player.player_name) return player.player_name;
    return mode === "vaep" ? `Player ID ${player.player_id || "–"}` : String(player.player_id || "–");
}

function actionPlayerMeta(player, mode) {
    const parts = [];
    if (player.competition) parts.push(player.competition);
    if (player.season) parts.push(player.season);
    if (player.estimated_minutes != null) parts.push(`${Math.round(Number(player.estimated_minutes || 0))}min`);
    if (player.n_matches != null) parts.push(`${Number(player.n_matches).toFixed(Number(player.n_matches) % 1 ? 1 : 0)} matches`);
    if (mode === "xt" && player.xt_total != null) parts.push(`xT ${Number(player.xt_total).toFixed(2)}`);
    if (mode === "vaep" && player.vaep_total != null) parts.push(`VAEP ${Number(player.vaep_total).toFixed(2)}`);
    return parts.join(" \u00B7 ");
}

function generateXTHeatmapGrid(summary) {
    // Standard StatsBomb xT grid: 12 columns (length) x 8 rows (width)
    var defaultXT = [
        [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
        [0.00, 0.00, 0.00, 0.00, 0.01, 0.01, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06],
        [0.00, 0.00, 0.00, 0.01, 0.01, 0.02, 0.03, 0.05, 0.07, 0.10, 0.14, 0.18],
        [0.00, 0.00, 0.01, 0.01, 0.02, 0.04, 0.06, 0.09, 0.14, 0.20, 0.28, 0.35],
        [0.00, 0.00, 0.01, 0.01, 0.02, 0.04, 0.06, 0.09, 0.14, 0.20, 0.28, 0.35],
        [0.00, 0.00, 0.00, 0.01, 0.01, 0.02, 0.03, 0.05, 0.07, 0.10, 0.14, 0.18],
        [0.00, 0.00, 0.00, 0.00, 0.01, 0.01, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06],
        [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
    ];
    if (summary && summary.metrics && summary.metrics.mean_xt_per_90) {
        var meanXT = summary.metrics.mean_xt_per_90;
        var scaleFactor = meanXT / 0.06;
        for (var r = 0; r < defaultXT.length; r++) {
            for (var c = 0; c < defaultXT[r].length; c++) {
                defaultXT[r][c] = defaultXT[r][c] * scaleFactor;
            }
        }
    }
    return defaultXT;
}

function refreshAllChartColors() {
    // Re-render all active charts with updated theme colors
    Object.keys(appState.charts).forEach((id) => {
        const element = document.getElementById(id);
        if (!element || element.offsetParent === null) return; // Skip hidden charts
        const chart = appState.charts[id];
        if (!chart) return;
        
        // Re-render based on chart type
        switch(id) {
            case "radar-chart": {
                const player = players.find((item) => item.key === appState.selectedPlayerKey) || players[0];
                if (player) renderRadar(player);
                break;
            }
            case "value-chart":
                renderValue();
                break;
            case "score-chart":
                renderScoreMatrix(selectedMatch());
                break;
            case "outcome-bar-chart":
                renderOutcomeBar(selectedMatch());
                break;
            case "compare-radar-chart":
                renderComparePanel();
                break;
            case "action-chart":
                renderActions();
                break;
        }
    });
}

function renderLicense() {
    const tbody = document.getElementById("license-table-body");
    if (!tbody) return;

    const attribution = licenseData.license_attribution || {};
    const rows = LICENSE_SOURCES.map((src) => {
        const desc = attribution[src.key] || "";
        return `<tr>
            <td>${escapeHtml(src.name)}</td>
            <td>${escapeHtml(src.license)}</td>
            <td>${escapeHtml(desc || src.attribution)}</td>
            <td><a href="${escapeAttr(src.url)}" target="_blank" rel="noopener" style="color:var(--accent)">${escapeHtml(src.url)}</a></td>
        </tr>`;
    }).join("");
    tbody.innerHTML = rows || '<tr><td colspan="4" style="text-align:center;color:var(--text-muted)">' + (appState.lang === "zh" ? "无数据" : "No data") + "</td></tr>";

    const timestamp = formatTimestamp(licenseData.updated_at);
    const updatedPill = document.getElementById("license-updated");
    if (updatedPill) {
        updatedPill.textContent = timestamp
            ? timestamp
            : (appState.lang === "zh" ? "无时间戳" : "No timestamp");
    }

    const updatedText = document.getElementById("license-last-updated");
    if (updatedText) {
        updatedText.textContent = timestamp
            ? (appState.lang === "zh" ? "最后更新: " : "Last updated: ") + timestamp
            : "";
    }
}

// ── Data Status Page ──────────────────────────────────────────────

function _classifyArtifact(name) {
    if (/statsbomb|events_all/.test(name)) return "real";
    if (/truth_labels|oof/.test(name)) return "real";
    if (/player_match|season_proxy/.test(name)) return "proxy";
    if (/team_match/.test(name)) return "real";
    if (/ratings/.test(name)) return "real";
    return "synthetic";
}

function renderData() {
    const artifacts = artifactSummary.artifacts || [];
    const health = artifactSummary.data_health || {};
    const licenses = artifactSummary.license_attribution || {};

    // Data sources table
    const sourcesTbody = document.getElementById("data-sources-table");
    if (sourcesTbody) {
        let totalRows = 0;
        let sourceCount = 0;
        const rows = artifacts.map(a => {
            const rows = a.rows || 0;
            totalRows += rows;
            if (rows > 0) sourceCount++;
            const srcType = _classifyArtifact(a.label || a.name || "");
            const typeLabel = srcType === "real" ? t("data_type_real") : (srcType === "proxy" ? t("data_type_proxy") : t("data_type_synthetic"));
            const typeCls = srcType === "real" ? "status-high" : (srcType === "proxy" ? "status-medium" : "status-low");
            const modified = a.updated_at ? new Date(a.updated_at * 1000).toISOString().slice(0, 10) : "–";
            return `<tr>
                <td>${escapeHtml(a.label || a.name || "–")}</td>
                <td>${rows.toLocaleString()}</td>
                <td>${escapeHtml(modified)}</td>
                <td><span class="status-pill ${typeCls}">${escapeHtml(typeLabel)}</span></td>
            </tr>`;
        }).join("");
        sourcesTbody.innerHTML = rows || '<tr><td colspan="4" style="text-align:center;color:var(--text-muted)">' + (appState.lang === "zh" ? "无数据" : "No data") + "</td></tr>";

        // Update summary metrics
        const totalEl = document.getElementById("data-total-rows");
        if (totalEl) totalEl.textContent = totalRows.toLocaleString();
        const countEl = document.getElementById("data-source-count");
        if (countEl) countEl.textContent = String(sourceCount);
    }

    // Coverage by league-season
    const coverageTbody = document.getElementById("data-coverage-table");
    if (coverageTbody) {
        const byLeagueSeason = {};
        for (const p of players) {
            const league = p.league || "";
            const season = p.season || "";
            if (!league) continue;
            const key = `${league}|${season}`;
            if (!byLeagueSeason[key]) byLeagueSeason[key] = { league, season, teams: new Set(), rated: 0, total: 0 };
            byLeagueSeason[key].teams.add(p.team);
            byLeagueSeason[key].total++;
            if (p.rating > 0) byLeagueSeason[key].rated++;
        }
        // Compute per-unique-team coverage
        const byLeagueSeasonAgg = {};
        for (const p of players) {
            const league = p.league || "";
            const season = p.season || "";
            if (!league) continue;
            const key = `${league}|${season}`;
            if (!byLeagueSeasonAgg[key]) byLeagueSeasonAgg[key] = { league, season, teams: new Set(), ratedTeams: new Set() };
            byLeagueSeasonAgg[key].teams.add(p.team);
            if (p.rating > 0) byLeagueSeasonAgg[key].ratedTeams.add(p.team);
        }
        const coverageRows = Object.values(byLeagueSeasonAgg).sort((a, b) => {
            if (a.league !== b.league) return a.league.localeCompare(b.league);
            return a.season.localeCompare(b.season);
        }).map(entry => {
            const total = entry.teams.size;
            const rated = entry.ratedTeams.size;
            const pct = total > 0 ? rated / total : 0;
            const pctColor = pct > 0.90 ? "status-high" : (pct >= 0.70 ? "status-medium" : "status-low");
            const pctLabel = pct > 0.90 ? "HIGH" : (pct >= 0.70 ? "MED" : "LOW");
            return `<tr>
                <td>${escapeHtml(entry.league)}</td>
                <td>${escapeHtml(entry.season)}</td>
                <td>${rated}</td>
                <td>${total}</td>
                <td><span class="status-pill ${pctColor}">${Math.round(pct * 100)}% ${pctLabel}</span></td>
            </tr>`;
        }).join("");
        coverageTbody.innerHTML = coverageRows || '<tr><td colspan="5" style="text-align:center;color:var(--text-muted)">' + (appState.lang === "zh" ? "无数据" : "No data") + "</td></tr>";
    }

    // Missing data warnings
    const warningsEl = document.getElementById("data-missing-warnings");
    if (warningsEl) {
        const warnings = [];
        if (!health.oof_available) warnings.push(appState.lang === "zh" ? "OOF 预测数据缺失" : "OOF prediction data missing");
        if (!health.truth_labels_available) warnings.push(appState.lang === "zh" ? "真实标签数据缺失" : "Truth labels data missing");
        if (!health.player_match_coverage) warnings.push(appState.lang === "zh" ? "球员比赛级覆盖不足" : "Player match-level coverage is thin");

        // Check for leagues with low coverage
        const leagueCov = computeLeagueCoverage();
        for (const lc of leagueCov) {
            if (lc.coverage < 0.70) {
                warnings.push((appState.lang === "zh" ? "联赛 " : "League ") + escapeHtml(lc.league) + (appState.lang === "zh" ? " 覆盖率过低: " : " coverage too low: ") + Math.round(lc.coverage * 100) + "%");
            }
        }

        if (warnings.length === 0) {
            warningsEl.innerHTML = '<li class="health-item"><span class="dot status-high"></span><span>' + escapeHtml(t("data_no_missing")) + '</span></li>';
        } else {
            warningsEl.innerHTML = warnings.map(w =>
                `<li class="health-item"><span class="dot status-low"></span><span>${w}</span></li>`
            ).join("");
        }
    }
}

async function renderActiveView() {
    if (appState.view === "overview") renderOverview();
    if (appState.view === "players") await renderPlayers();
    if (appState.view === "compare") await renderCompare();
    if (appState.view === "value") renderValue();
    if (appState.view === "matches") await renderMatches();
    if (appState.view === "teams") await renderTeams();
    if (appState.view === "scouting") renderScouting();
    if (appState.view === "actions") renderActions();
    if (appState.view === "reports") renderReports();
    if (appState.view === "tactical") renderTactical();
    if (appState.view === "wc_schedule") renderWcSchedule();
    if (appState.view === "wc_squads") renderWcSquads();
    if (appState.view === "wc_compare") renderWcCompare();
    if (appState.view === "wc_probability") renderWcProbability();
    if (appState.view === "license") renderLicense();
    if (appState.view === "data") renderData();
    if (appState.view === "calibration") renderCalibration();
    // Resize charts after layout paint to ensure correct dimensions
    requestAnimationFrame(() => {
        Object.values(appState.charts).forEach((chart) => {
            try { chart.resize(); } catch(e) { /* ignore disposed charts */ }
        });
    });
}

async function renderCalibration() {
    const statusPill = document.getElementById("calibration-status");
    try {
        const data = Object.keys(predictionCalibration).length > 0
            ? predictionCalibration
            : await fetchPredictionCalibration();
        predictionCalibration = data;

        // Status
        const dcStatus = data.dixon_coles ? data.dixon_coles.status : "not_available";
        if (statusPill) {
            statusPill.textContent = dcStatus === "ok" ? "DC: OK" : dcStatus;
            statusPill.className = `status-pill ${dcStatus === "ok" ? "status-high" : "status-medium"}`;
        }

        // Metrics summary
        const metricsEl = document.getElementById("calibration-metrics");
        if (metricsEl) {
            const dc = data.dixon_coles || {};
            const poisson = data.poisson || {};
            const zT = appState.lang === "zh";
            let html = '<div class="detail-grid">';
            if (dc.status === "ok") {
                html += `<div><span>${zT ? "DC 对数损失" : "DC Log Loss"}</span><strong>${escapeHtml(String(dc.log_loss_exact))}</strong></div>`;
                html += `<div><span>${zT ? "DC Brier" : "DC Brier 1x2"}</span><strong>${escapeHtml(String(dc.brier_1x2))}</strong></div>`;
                html += `<div><span>${zT ? "DC RPS" : "DC RPS"}</span><strong>${escapeHtml(String(dc.rps_1x2))}</strong></div>`;
                html += `<div><span>${zT ? "DC 场次" : "DC matches"}</span><strong>${escapeHtml(String(dc.n_matches))}</strong></div>`;
            }
            if (poisson.status === "ok") {
                html += `<div><span>${zT ? "Poisson 对数损失" : "Poisson Log Loss"}</span><strong>${escapeHtml(String(poisson.log_loss_exact || "–"))}</strong></div>`;
                html += `<div><span>${zT ? "Poisson Brier" : "Poisson Brier"}</span><strong>${escapeHtml(String(poisson.brier_1x2 || "–"))}</strong></div>`;
            }
            html += '</div>';
            metricsEl.innerHTML = html;
        }

        // Calibration plot (predicted vs actual home-win)
        const calPlot = data.calibration_plot || [];
        const chartEl = document.getElementById("calibration-plot-chart");
        if (chartEl && calPlot.length > 0 && typeof echarts !== "undefined") {
            const chart = getChart("calibration-plot-chart");
            chart.setOption({
                tooltip: { trigger: "axis" },
                xAxis: { type: "value", name: "Predicted", min: 0, max: 1 },
                yAxis: { type: "value", name: "Actual", min: 0, max: 1 },
                series: [
                    { type: "line", data: [[0, 0], [1, 1]], lineStyle: { type: "dashed", color: "#888" }, symbol: "none", silent: true },
                    {
                        type: "scatter",
                        data: calPlot.map(p => [p.mean_predicted, p.mean_actual]),
                        symbolSize: calPlot.map(p => Math.max(8, Math.sqrt(p.n_matches) * 3)),
                        itemStyle: { color: "#4a90d9" },
                        label: { show: false },
                    },
                ],
                grid: { left: 50, right: 20, top: 30, bottom: 40 },
            });
        }

        // Low score breakdown
        const lowScoreEl = document.getElementById("calibration-low-score");
        if (lowScoreEl) {
            const buckets = data.low_score_breakdown || [];
            if (buckets.length === 0) {
                lowScoreEl.innerHTML = `<div style="padding:0.5rem;color:var(--text-muted)">${escapeHtml(appState.lang === "zh" ? "无数据" : "No data")}</div>`;
            } else {
                lowScoreEl.innerHTML = buckets.map(b =>
                    `<div class="rank-item" style="display:flex;justify-content:space-between;padding:4px 8px;font-size:0.82rem">
                        <span>${escapeHtml(b.score_bucket)}</span>
                        <span>${escapeHtml(String(b.n_matches))} ${escapeHtml(appState.lang === "zh" ? "场" : "matches")}</span>
                        <span>${escapeHtml(appState.lang === "zh" ? "实际" : "Actual")}: ${escapeHtml(String(b.actual_pct))}%</span>
                        <span>${escapeHtml(appState.lang === "zh" ? "预测" : "Pred")}: ${escapeHtml(String(b.mean_predicted_pct))}%</span>
                        <span style="color:${b.calibration_error > 5 ? '#ff6b6b' : '#57d68d'}">${escapeHtml(String(b.calibration_error))}% err</span>
                    </div>`
                ).join("");
            }
        }

        // Per-league calibration
        const leagueEl = document.getElementById("calibration-league");
        if (leagueEl) {
            const leagues = data.league_coverage || [];
            if (leagues.length === 0) {
                leagueEl.innerHTML = `<div style="padding:0.5rem;color:var(--text-muted)">${escapeHtml(appState.lang === "zh" ? "无数据" : "No data")}</div>`;
            } else {
                leagueEl.innerHTML = leagues.map(l =>
                    `<div class="rank-item" style="display:flex;justify-content:space-between;padding:4px 8px;font-size:0.82rem">
                        <span>${escapeHtml(l.league)}</span>
                        <span>${escapeHtml(String(l.n_matches))} ${escapeHtml(appState.lang === "zh" ? "场" : "matches")}</span>
                        <span>${escapeHtml(appState.lang === "zh" ? "对数损失" : "LogLoss")}: ${escapeHtml(String(l.mean_log_loss))}</span>
                        <span>Brier: ${escapeHtml(String(l.mean_brier))}</span>
                    </div>`
                ).join("");
            }
        }

        // Brier decomposition
        const brierEl = document.getElementById("calibration-brier");
        if (brierEl && data.dixon_coles && data.dixon_coles.status === "ok") {
            const dc = data.dixon_coles;
            brierEl.innerHTML = `<p style="font-size:0.72rem;color:var(--text-muted);margin:0.3rem 0">
                Brier 1x2: ${escapeHtml(String(dc.brier_1x2))} | RPS: ${escapeHtml(String(dc.rps_1x2))} | n=${escapeHtml(String(dc.n_matches))}
            </p>`;
        }
    } catch (err) {
        if (statusPill) {
            statusPill.textContent = "error";
            statusPill.className = "status-pill status-low";
        }
        console.warn("Failed to fetch calibration:", err);
    }
}

function exportPlayers() {
    const header = ["rank", "player", "position", "team", "league", "season", "rating", "confidence", "minutes", "goals", "assists"];
    const rows = filteredPlayers().map((player, index) => [
        index + 1,
        player.name,
        player.position,
        player.team,
        player.league || "",
        player.season,
        player.rating,
        player.confidence,
        player.minutes || "",
        player.goals || "",
        player.assists || "",
    ]);
    const csv = [header, ...rows].map((row) => row.map(csvCell).join(",")).join("\n");
    const blob = new Blob([csv], { type: "text/csv;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = "scoutfootball-player-pool.csv";
    link.click();
    URL.revokeObjectURL(url);
}

function bindEvents() {
    document.querySelectorAll(".nav-action[data-view]").forEach((button) => {
        button.addEventListener("click", () => setView(button.dataset.view));
    });
    document.querySelectorAll("[data-jump]").forEach((card) => {
        card.addEventListener("click", () => setView(card.dataset.jump));
    });
    document.getElementById("theme-toggle").addEventListener("click", () => {
        document.body.classList.toggle("dark-mode");
        document.getElementById("theme-toggle").textContent = document.body.classList.contains("dark-mode") ? "☾" : "☀";
        localStorage.setItem("sf-theme", document.body.classList.contains("dark-mode") ? "dark" : "light");
        refreshAllChartColors();
        renderActiveView();
    });
    document.getElementById("lang-toggle").addEventListener("click", () => {
        appState.lang = appState.lang === "zh" ? "en" : "zh";
        applyLocale();
        renderActiveView();
    });
    document.getElementById("position-filter").addEventListener("change", (event) => {
        appState.position = event.target.value;
        renderPlayers();
    });
    document.getElementById("season-filter").addEventListener("change", (event) => {
        appState.season = event.target.value;
        appState.playerPage = 1;
        renderPlayers();
    });
    document.getElementById("league-filter").addEventListener("change", (event) => {
        appState.league = event.target.value;
        appState.playerPage = 1;
        renderPlayers();
    });
    // Pagination
    document.getElementById("player-prev-page")?.addEventListener("click", () => {
        if (appState.playerPage > 1) { appState.playerPage--; renderPlayers(); }
    });
    document.getElementById("player-next-page")?.addEventListener("click", () => {
        appState.playerPage++;
        renderPlayers();
    });
    // Column sorting
    document.querySelectorAll("th[data-sort]").forEach((th) => {
        th.addEventListener("click", () => {
            const col = th.dataset.sort;
            if (appState.playerSortCol === col) {
                appState.playerSortAsc = !appState.playerSortAsc;
            } else {
                appState.playerSortCol = col;
                appState.playerSortAsc = col === "name" || col === "position" || col === "team";
            }
            appState.playerPage = 1;
            renderPlayers();
        });
    });
    let searchTimer = null;
    document.getElementById("global-search").addEventListener("input", () => {
        clearTimeout(searchTimer);
        searchTimer = setTimeout(() => {
            appState.playerPage = 1;
            if (appState.view !== "players") setView("players");
            else renderPlayers();
        }, 300);
    });
    document.querySelectorAll("[data-value-mode]").forEach((button) => {
        button.addEventListener("click", () => {
            appState.valueMode = button.dataset.valueMode;
            document.querySelectorAll("[data-value-mode]").forEach((item) => item.classList.toggle("active", item === button));
            renderValue();
        });
    });
    document.getElementById("home-team").addEventListener("change", (event) => {
        appState.home = event.target.value;
        if (appState.home === appState.away) {
            const nextAway = getTeams().find((team) => team !== appState.home);
            if (nextAway) appState.away = nextAway;
            document.getElementById("away-team").value = appState.away;
        }
        renderMatches();
    });
    document.getElementById("away-team").addEventListener("change", (event) => {
        appState.away = event.target.value;
        if (appState.home === appState.away) {
            const nextHome = getTeams().find((team) => team !== appState.away);
            if (nextHome) appState.home = nextHome;
            document.getElementById("home-team").value = appState.home;
        }
        renderMatches();
    });
    document.getElementById("export-players").addEventListener("click", exportPlayers);
    // World Cup events
    document.getElementById("wc-group-filter").addEventListener("change", () => renderWcSchedule());
    document.getElementById("wc-matchday-filter").addEventListener("change", () => renderWcSchedule());
    document.getElementById("wc-squad-team").addEventListener("change", async (e) => {
        appState.wcSquadTeam = e.target.value;
        await fetchWcSquad(e.target.value);
        renderWcSquads();
    });
    document.getElementById("wc-compare-a").addEventListener("change", async (e) => {
        appState.wcCompareA = e.target.value;
        if (appState.wcCompareA === appState.wcCompareB) {
            const nextB = wcAllTeams().find((team) => team !== appState.wcCompareA);
            if (nextB) {
                appState.wcCompareB = nextB;
                document.getElementById("wc-compare-b").value = nextB;
            }
        }
        await Promise.all([
            fetchWcSquad(e.target.value),
            fetchWcMatchPrediction(e.target.value, appState.wcCompareB),
        ]);
        renderWcCompare();
    });
    document.getElementById("wc-compare-b").addEventListener("change", async (e) => {
        appState.wcCompareB = e.target.value;
        if (appState.wcCompareA === appState.wcCompareB) {
            const nextA = wcAllTeams().find((team) => team !== appState.wcCompareB);
            if (nextA) {
                appState.wcCompareA = nextA;
                document.getElementById("wc-compare-a").value = nextA;
            }
        }
        await Promise.all([
            fetchWcSquad(e.target.value),
            fetchWcMatchPrediction(appState.wcCompareA, e.target.value),
        ]);
        renderWcCompare();
    });

    // Pre-match plan button: create tactical project from match prediction
    const prematchBtn = document.getElementById("btn-prematch-plan");
    if (prematchBtn) {
        prematchBtn.addEventListener("click", () => {
            createPrematchPlan();
        });
    }

    // WC team template button: create tactical project from WC squad
    const wcTeamTemplateBtn = document.getElementById("btn-wc-team-template");
    if (wcTeamTemplateBtn) {
        wcTeamTemplateBtn.addEventListener("click", () => {
            createWcTeamTemplate();
        });
    }

    // Tactical board event handlers
    const tacticalLoadHome = document.getElementById("tactical-load-home");
    if (tacticalLoadHome) {
        tacticalLoadHome.addEventListener("click", () => {
            const formation = document.getElementById("tactical-formation").value;
            if (typeof TacticalRenderer !== "undefined") {
                TacticalRenderer.loadFormation(formation, "home");
                tacticalProject = TacticalRenderer.getProject();
                // Load coaching points into frame notes
                if (typeof TACTICAL_BOARD !== "undefined") {
                    const cp = TACTICAL_BOARD.getFormationCoachingPoints(formation);
                    if (cp) {
                        const notes = TACTICAL_BOARD.formatCoachingNotes(cp);
                        TacticalRenderer.setCurrentFrameNotes(notes);
                        updateCoachingNotesPanel();
                    }
                }
            }
        });
    }
    const tacticalLoadAway = document.getElementById("tactical-load-away");
    if (tacticalLoadAway) {
        tacticalLoadAway.addEventListener("click", () => {
            const formation = document.getElementById("tactical-formation").value;
            if (typeof TacticalRenderer !== "undefined") {
                TacticalRenderer.loadFormation(formation, "away");
                tacticalProject = TacticalRenderer.getProject();
            }
        });
    }
    const tacticalClear = document.getElementById("tactical-clear");
    if (tacticalClear) {
        tacticalClear.addEventListener("click", () => {
            if (typeof TacticalRenderer !== "undefined") {
                TacticalRenderer.clearBoard();
                tacticalProject = TacticalRenderer.getProject();
            }
        });
    }
    const tacticalLoadSetPiece = document.getElementById("tactical-load-setpiece");
    if (tacticalLoadSetPiece) {
        tacticalLoadSetPiece.addEventListener("click", () => {
            const type = document.getElementById("tactical-setpiece").value;
            if (!type) return;
            if (typeof TacticalRenderer !== "undefined" && typeof TACTICAL_BOARD !== "undefined") {
                const objects = TACTICAL_BOARD.generateSetPiece(type, "home");
                if (objects.length > 0) {
                    TacticalRenderer.clearBoard();
                    const project = TacticalRenderer.getProject();
                    project.objects = objects;
                    TacticalRenderer.render();
                    tacticalProject = project;
                    // Load coaching points into frame notes
                    const cp = TACTICAL_BOARD.getSetPieceCoachingPoints(type);
                    if (cp) {
                        const notes = TACTICAL_BOARD.formatCoachingNotes(cp);
                        TacticalRenderer.setCurrentFrameNotes(notes);
                        updateCoachingNotesPanel();
                    }
                }
            }
        });
    }
    const tacticalLoadTraining = document.getElementById("tactical-load-training");
    if (tacticalLoadTraining) {
        tacticalLoadTraining.addEventListener("click", () => {
            const type = document.getElementById("tactical-training").value;
            if (!type) return;
            if (typeof TacticalRenderer !== "undefined" && typeof TACTICAL_BOARD !== "undefined") {
                const objects = TACTICAL_BOARD.generateTraining(type, "home");
                if (objects.length > 0) {
                    TacticalRenderer.clearBoard();
                    const project = TacticalRenderer.getProject();
                    project.objects = objects;
                    TacticalRenderer.render();
                    tacticalProject = project;
                    // Load coaching points into frame notes
                    const cp = TACTICAL_BOARD.getTrainingCoachingPoints(type);
                    if (cp) {
                        const notes = TACTICAL_BOARD.formatCoachingNotes(cp);
                        TacticalRenderer.setCurrentFrameNotes(notes);
                        updateCoachingNotesPanel();
                    }
                }
            }
        });
    }
    const tacticalSave = document.getElementById("tactical-save");
    if (tacticalSave) {
        tacticalSave.addEventListener("click", () => {
            if (tacticalProject) {
                TACTICAL_BOARD.saveProject(tacticalProject);
                renderTacticalProjectList();
            }
        });
    }
    const tacticalExport = document.getElementById("tactical-export");
    if (tacticalExport) {
        tacticalExport.addEventListener("click", () => {
            if (tacticalProject) {
                // Show export preview with attribution
                const previewEl = document.getElementById("tactical-export-preview");
                const attrEl = document.getElementById("tactical-export-attribution");
                if (previewEl && attrEl) {
                    const attribution = [
                        "Title: " + (tacticalProject.title || "Untitled"),
                        "Source: " + (tacticalProject.source_attribution || "ScoutFootball tactical board"),
                        "Version: " + (tacticalProject.version || TACTICAL_BOARD.SCHEMA_VERSION),
                        "Objects: " + (tacticalProject.objects || []).length,
                        "Frames: " + (tacticalProject.frames || []).length,
                        "Created: " + (tacticalProject.created_at || "unknown"),
                        "Updated: " + (tacticalProject.updated_at || "unknown"),
                        "",
                        "No data leaves the browser. All projects are stored locally.",
                    ].join("\n");
                    attrEl.textContent = attribution;
                    previewEl.style.display = "flex";
                } else {
                    // Fallback: direct export
                    doTacticalExport(tacticalProject);
                }
            }
        });
    }
    // Export preview confirm/cancel handlers
    const exportConfirm = document.getElementById("tactical-export-confirm");
    const exportCancel = document.getElementById("tactical-export-cancel");
    const exportPreview = document.getElementById("tactical-export-preview");
    if (exportConfirm) {
        exportConfirm.addEventListener("click", () => {
            if (exportPreview) exportPreview.style.display = "none";
            if (tacticalProject) doTacticalExport(tacticalProject);
        });
    }
    if (exportCancel) {
        exportCancel.addEventListener("click", () => {
            if (exportPreview) exportPreview.style.display = "none";
        });
    }
    function doTacticalExport(project) {
        const json = TACTICAL_BOARD.exportJSON(project);
        const blob = new Blob([json], { type: "application/json" });
        const url = URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = `tactical-board-${project.board_id}.json`;
        a.click();
        URL.revokeObjectURL(url);
    }
    const tacticalImport = document.getElementById("tactical-import");
    if (tacticalImport) {
        tacticalImport.addEventListener("click", () => {
            const input = document.createElement("input");
            input.type = "file";
            input.accept = ".json";
            input.addEventListener("change", (e) => {
                const file = e.target.files[0];
                if (!file) return;
                const reader = new FileReader();
                reader.onload = (ev) => {
                    const project = TACTICAL_BOARD.importJSON(ev.target.result);
                    if (project) {
                        tacticalProject = project;
                        renderTactical();
                    } else {
                        alert("Failed to import project. The file may be corrupt or not a valid tactical board export.");
                    }
                };
                reader.readAsText(file);
            });
            input.click();
        });
    }
    const tacticalExportPng = document.getElementById("tactical-export-png");
    if (tacticalExportPng) {
        tacticalExportPng.addEventListener("click", () => {
            if (typeof TacticalRenderer !== "undefined") {
                const title = tacticalProject?.title || "tactical-board";
                const cropSelect = document.getElementById("tactical-crop-mode");
                const transparentCb = document.getElementById("tactical-transparent-bg");
                const crop = cropSelect ? cropSelect.value : "full";
                const transparent = transparentCb ? transparentCb.checked : false;
                TacticalRenderer.exportPNG(`${title}.png`, { crop, transparent });
            }
        });
    }
    const tacticalExportWebm = document.getElementById("tactical-export-webm");
    if (tacticalExportWebm) {
        tacticalExportWebm.addEventListener("click", () => {
            if (typeof TacticalRenderer !== "undefined") {
                const title = tacticalProject?.title || "tactical-animation";
                TacticalRenderer.exportWebM(`${title}.webm`);
            }
        });
    }
    const tacticalExportGif = document.getElementById("tactical-export-gif");
    if (tacticalExportGif) {
        tacticalExportGif.addEventListener("click", () => {
            if (typeof TacticalRenderer !== "undefined") {
                const title = tacticalProject?.title || "tactical-animation";
                TacticalRenderer.exportGIF(`${title}.gif`);
            }
        });
    }
    // MP4 export via backend ffmpeg conversion
    const tacticalExportMp4 = document.getElementById("tactical-export-mp4");
    if (tacticalExportMp4) {
        // Check if ffmpeg is available on the backend
        fetchJson("/tactical-board/capabilities").then(caps => {
            if (caps.ffmpeg_available) {
                tacticalExportMp4.style.opacity = "1";
                tacticalExportMp4.title = "ffmpeg detected: " + (caps.ffmpeg_path || "");
            } else {
                tacticalExportMp4.title = "ffmpeg not found on server — MP4 export unavailable";
            }
        }).catch(() => { /* API offline, keep button dimmed */ });

        tacticalExportMp4.addEventListener("click", async () => {
            if (typeof TacticalRenderer === "undefined") return;
            const zT = appState.lang === "zh";
            try {
                // First export as WebM blob
                tacticalExportMp4.disabled = true;
                tacticalExportMp4.textContent = zT ? "◆ 导出中..." : "◆ Exporting...";

                const stream = TacticalRenderer.canvas.captureStream(30);
                const mimeType = "video/webm;codecs=vp9";
                const recorder = new MediaRecorder(stream, { mimeType });
                const chunks = [];
                recorder.ondataavailable = (e) => { if (e.data.size > 0) chunks.push(e.data); };

                // Play animation and record
                const wasPlaying = TacticalRenderer.animationState.playing;
                if (!wasPlaying) TacticalRenderer.toggleAnimation();
                recorder.start();

                await new Promise(resolve => setTimeout(resolve, 3000)); // Record 3s

                recorder.stop();
                if (wasPlaying) TacticalRenderer.toggleAnimation();

                await new Promise(resolve => { recorder.onstop = resolve; });
                const webmBlob = new Blob(chunks, { type: "video/webm" });

                // Send to backend for MP4 conversion
                const resp = await fetch(`${API_BASE}/tactical-board/export/mp4`, {
                    method: "POST",
                    headers: { "Content-Type": "video/webm" },
                    body: webmBlob,
                });
                const result = await resp.json();

                if (result.status === "ok") {
                    alert(zT
                        ? `◆ MP4 导出成功！\n保存到: ${result.path}\n大小: ${(result.size_bytes / 1024).toFixed(1)} KB`
                        : `◆ MP4 exported!\nSaved to: ${result.path}\nSize: ${(result.size_bytes / 1024).toFixed(1)} KB`
                    );
                } else {
                    alert(zT
                        ? `◆ MP4 导出失败: ${result.error}`
                        : `◆ MP4 export failed: ${result.error}`
                    );
                }
            } catch (err) {
                alert(zT
                    ? `◆ MP4 导出失败: ${err.message}`
                    : `◆ MP4 export failed: ${err.message}`
                );
            } finally {
                tacticalExportMp4.disabled = false;
                tacticalExportMp4.textContent = "◆ 导出 MP4";
            }
        });
    }

    // Animation controls
    const tacticalAddFrame = document.getElementById("tactical-add-frame");
    if (tacticalAddFrame) {
        tacticalAddFrame.addEventListener("click", () => {
            if (tacticalProject && typeof TacticalRenderer !== "undefined") {
                TACTICAL_BOARD.saveFrame(tacticalProject, TacticalRenderer.animationState.currentFrame);
                TACTICAL_BOARD.addFrame(tacticalProject);
                renderTacticalFrameList();
            }
        });
    }
    const tacticalSaveFrame = document.getElementById("tactical-save-frame");
    if (tacticalSaveFrame) {
        tacticalSaveFrame.addEventListener("click", () => {
            if (tacticalProject && typeof TacticalRenderer !== "undefined") {
                TACTICAL_BOARD.saveFrame(tacticalProject, TacticalRenderer.animationState.currentFrame);
                renderTacticalFrameList();
            }
        });
    }
    const tacticalPlay = document.getElementById("tactical-play");
    if (tacticalPlay) {
        tacticalPlay.addEventListener("click", () => {
            if (typeof TacticalRenderer !== "undefined") {
                TacticalRenderer.play();
            }
        });
    }
    const tacticalStop = document.getElementById("tactical-stop");
    if (tacticalStop) {
        tacticalStop.addEventListener("click", () => {
            if (typeof TacticalRenderer !== "undefined") {
                TacticalRenderer.stop();
            }
        });
    }
    const tacticalPrevFrame = document.getElementById("tactical-prev-frame");
    if (tacticalPrevFrame) {
        tacticalPrevFrame.addEventListener("click", () => {
            if (typeof TacticalRenderer !== "undefined") {
                TacticalRenderer.prevFrame();
                tacticalProject = TacticalRenderer.getProject();
                renderTacticalFrameList();
            }
        });
    }
    const tacticalNextFrame = document.getElementById("tactical-next-frame");
    if (tacticalNextFrame) {
        tacticalNextFrame.addEventListener("click", () => {
            if (typeof TacticalRenderer !== "undefined") {
                TacticalRenderer.nextFrame();
                tacticalProject = TacticalRenderer.getProject();
                renderTacticalFrameList();
            }
        });
    }

    // Drawing tool buttons
    const toolButtons = ["tactical-tool-select", "tactical-tool-arrow", "tactical-tool-zone", "tactical-tool-text"];
    function setActiveTool(activeId) {
        toolButtons.forEach((id) => {
            const btn = document.getElementById(id);
            if (btn) btn.classList.toggle("active", id === activeId);
        });
    }
    // Pitch type selector
    const tacticalPitchType = document.getElementById("tactical-pitch-type");
    if (tacticalPitchType) {
        tacticalPitchType.addEventListener("change", (e) => {
            if (tacticalProject && typeof TacticalRenderer !== "undefined") {
                tacticalProject.pitch_type = e.target.value;
                TacticalRenderer.render();
                tacticalProject = TacticalRenderer.getProject();
            }
        });
    }

    // Display mode selector
    const tacticalDisplayMode = document.getElementById("tactical-display-mode");
    if (tacticalDisplayMode) {
        tacticalDisplayMode.addEventListener("change", (e) => {
            if (tacticalProject && typeof TacticalRenderer !== "undefined") {
                tacticalProject.displayMode = e.target.value;
                TacticalRenderer.render();
                tacticalProject = TacticalRenderer.getProject();
            }
        });
    }

    // Duplicate / Mirror buttons
    const tacticalDuplicate = document.getElementById("tactical-duplicate");
    if (tacticalDuplicate) {
        tacticalDuplicate.addEventListener("click", () => {
            if (typeof TacticalRenderer !== "undefined") {
                TacticalRenderer.duplicateSelected();
                tacticalProject = TacticalRenderer.getProject();
            }
        });
    }
    const tacticalMirror = document.getElementById("tactical-mirror");
    if (tacticalMirror) {
        tacticalMirror.addEventListener("click", () => {
            if (typeof TacticalRenderer !== "undefined") {
                TacticalRenderer.mirrorSelected();
                tacticalProject = TacticalRenderer.getProject();
            }
        });
    }
    const tacticalMirrorHome = document.getElementById("tactical-mirror-home");
    if (tacticalMirrorHome) {
        tacticalMirrorHome.addEventListener("click", () => {
            if (typeof TacticalRenderer !== "undefined") {
                TacticalRenderer.mirrorAllHome();
                tacticalProject = TacticalRenderer.getProject();
            }
        });
    }
    const tacticalMirrorAway = document.getElementById("tactical-mirror-away");
    if (tacticalMirrorAway) {
        tacticalMirrorAway.addEventListener("click", () => {
            if (typeof TacticalRenderer !== "undefined") {
                TacticalRenderer.mirrorAllAway();
                tacticalProject = TacticalRenderer.getProject();
            }
        });
    }

    const tacticalToolSelect = document.getElementById("tactical-tool-select");
    if (tacticalToolSelect) {
        tacticalToolSelect.addEventListener("click", () => {
            if (typeof TacticalRenderer !== "undefined") {
                TacticalRenderer.setDrawingMode(null);
            }
            setActiveTool("tactical-tool-select");
        });
    }

    const tacticalToolArrow = document.getElementById("tactical-tool-arrow");
    if (tacticalToolArrow) {
        tacticalToolArrow.addEventListener("click", () => {
            if (typeof TacticalRenderer !== "undefined") {
                TacticalRenderer.setDrawingMode("arrow");
            }
            setActiveTool("tactical-tool-arrow");
        });
    }

    const tacticalToolZone = document.getElementById("tactical-tool-zone");
    if (tacticalToolZone) {
        tacticalToolZone.addEventListener("click", () => {
            if (typeof TacticalRenderer !== "undefined") {
                TacticalRenderer.setDrawingMode("zone");
            }
            setActiveTool("tactical-tool-zone");
        });
    }

    const tacticalToolText = document.getElementById("tactical-tool-text");
    if (tacticalToolText) {
        tacticalToolText.addEventListener("click", () => {
            if (typeof TacticalRenderer !== "undefined") {
                TacticalRenderer.setDrawingMode("text");
            }
            setActiveTool("tactical-tool-text");
        });
    }

    // Loop toggle
    const tacticalLoop = document.getElementById("tactical-loop");
    if (tacticalLoop) {
        tacticalLoop.addEventListener("click", () => {
            if (typeof TacticalRenderer !== "undefined") {
                TacticalRenderer.toggleLoop();
                tacticalLoop.classList.toggle("active", TacticalRenderer.animationState.loop);
            }
        });
    }

    // Tactical: toggle player ratings
    const tacticalToggleRatings = document.getElementById("tactical-toggle-ratings");
    if (tacticalToggleRatings) {
        tacticalToggleRatings.addEventListener("click", () => {
            if (typeof TacticalRenderer !== "undefined") {
                TacticalRenderer.showRatings = !TacticalRenderer.showRatings;
                tacticalToggleRatings.classList.toggle("active", TacticalRenderer.showRatings);
                TacticalRenderer.render();
            }
        });
    }

    // Equipment placement handler
    const tacticalPlaceEquipment = document.getElementById("tactical-place-equipment");
    if (tacticalPlaceEquipment) {
        tacticalPlaceEquipment.addEventListener("click", () => {
            const equipmentType = document.getElementById("tactical-equipment").value;
            if (!equipmentType) return;
            if (typeof TacticalRenderer !== "undefined" && typeof TACTICAL_BOARD !== "undefined") {
                const project = TacticalRenderer.getProject();
                let obj = null;
                switch (equipmentType) {
                    case "cone": obj = TACTICAL_BOARD.createCone(50, 50); break;
                    case "marker": obj = TACTICAL_BOARD.createMarker(50, 50); break;
                    case "pole": obj = TACTICAL_BOARD.createPole(50, 50); break;
                    case "ladder": obj = TACTICAL_BOARD.createLadder(50, 50); break;
                    case "minigoal": obj = TACTICAL_BOARD.createMiniGoal(50, 50); break;
                }
                if (obj) {
                    project.objects.push(obj);
                    TacticalRenderer.selectedObject = obj;
                    TacticalRenderer.render();
                    tacticalProject = project;
                }
            }
        });
    }

    // Eraser tool button
    const tacticalEraser = document.getElementById("tactical-eraser");
    if (tacticalEraser) {
        tacticalEraser.addEventListener("click", () => {
            if (typeof TacticalRenderer !== "undefined") {
                const isEraser = TacticalRenderer.drawingMode === "eraser";
                TacticalRenderer.setDrawingMode(isEraser ? null : "eraser");
                tacticalEraser.classList.toggle("active", !isEraser);
                setActiveTool(isEraser ? "tactical-tool-select" : null);
            }
        });
    }

    // Presentation mode button
    const tacticalPresentation = document.getElementById("tactical-presentation");
    if (tacticalPresentation) {
        tacticalPresentation.addEventListener("click", () => {
            if (typeof TacticalRenderer !== "undefined") {
                TacticalRenderer.togglePresentation();
            }
        });
    }

    // Animation trails toggle
    const tacticalToggleTrails = document.getElementById("tactical-toggle-trails");
    if (tacticalToggleTrails) {
        tacticalToggleTrails.addEventListener("click", () => {
            if (typeof TacticalRenderer !== "undefined") {
                TacticalRenderer.showTrails = !TacticalRenderer.showTrails;
                tacticalToggleTrails.classList.toggle("active", TacticalRenderer.showTrails);
                if (!TacticalRenderer.showTrails) {
                    TacticalRenderer._trailPositions.clear();
                }
                TacticalRenderer.render();
            }
        });
    }

    // Simplify button: remove hidden objects and empty frames
    const tacticalSimplify = document.getElementById("tactical-simplify");
    if (tacticalSimplify) {
        tacticalSimplify.addEventListener("click", () => {
            if (typeof TacticalRenderer !== "undefined") {
                TacticalRenderer.simplifyProject();
                tacticalProject = TacticalRenderer.getProject();
                tacticalAutoSave();
            }
        });
    }

    // xT Heatmap toggle
    const tacticalToggleHeatmap = document.getElementById("tactical-toggle-heatmap");
    if (tacticalToggleHeatmap) {
        tacticalToggleHeatmap.addEventListener("click", () => {
            if (typeof TacticalRenderer !== "undefined") {
                var isOn = TacticalRenderer.toggleXTHeatmap();
                tacticalToggleHeatmap.classList.toggle("active", isOn);
            }
        });
    }

    // Debug mode toggle (FPS counter)
    const tacticalToggleDebug = document.getElementById("tactical-toggle-debug");
    if (tacticalToggleDebug) {
        tacticalToggleDebug.addEventListener("click", () => {
            if (typeof TacticalRenderer !== "undefined") {
                TacticalRenderer._debugMode = !TacticalRenderer._debugMode;
                tacticalToggleDebug.classList.toggle("active", TacticalRenderer._debugMode);
                TacticalRenderer.render();
            }
        });
    }

    // Coaching notes textarea: sync notes to current frame
    const coachingNotesEl = document.getElementById("tactical-coaching-notes");
    if (coachingNotesEl) {
        coachingNotesEl.addEventListener("input", () => {
            if (typeof TacticalRenderer !== "undefined") {
                TacticalRenderer.setCurrentFrameNotes(coachingNotesEl.value);
                tacticalProject = TacticalRenderer.getProject();
                tacticalAutoSave();
            }
        });
    }

    // Animation mode toggle
    const tacticalAnimMode = document.getElementById("tactical-animation-mode");
    const stepDurationLabel = document.getElementById("tactical-step-duration-label");
    if (tacticalAnimMode) {
        tacticalAnimMode.addEventListener("change", (e) => {
            if (tacticalProject) {
                tacticalProject.animationMode = e.target.value;
                if (stepDurationLabel) {
                    stepDurationLabel.style.display = e.target.value === "step" ? "flex" : "none";
                }
                tacticalAutoSave();
            }
        });
    }

    // Step duration slider
    const tacticalStepDuration = document.getElementById("tactical-step-duration");
    const stepDurationValue = document.getElementById("tactical-step-duration-value");
    if (tacticalStepDuration) {
        tacticalStepDuration.addEventListener("input", (e) => {
            const val = parseInt(e.target.value, 10);
            if (stepDurationValue) stepDurationValue.textContent = val + "ms";
            if (tacticalProject) {
                tacticalProject.stepDuration = val;
                tacticalAutoSave();
            }
        });
    }

    // Path editing: add path point mode
    const tacticalAddPathPoint = document.getElementById("tactical-add-path-point");
    if (tacticalAddPathPoint) {
        tacticalAddPathPoint.addEventListener("click", () => {
            if (typeof TacticalRenderer !== "undefined") {
                const sel = TacticalRenderer.selectedObject;
                if (sel && (sel.type === "player" || sel.type === "ball")) {
                    const isActive = TacticalRenderer._pathEditMode && TacticalRenderer._pathEditObjectId === sel.id;
                    TacticalRenderer.setPathEditMode(!isActive, isActive ? null : sel.id);
                    tacticalAddPathPoint.classList.toggle("active", !isActive);
                    tacticalAddPathPoint.textContent = isActive ? "+ 路径点" : "完成路径";
                }
            }
        });
    }

    // Path editing: clear path points
    const tacticalClearPathPoints = document.getElementById("tactical-clear-path-points");
    if (tacticalClearPathPoints) {
        tacticalClearPathPoints.addEventListener("click", () => {
            if (typeof TacticalRenderer !== "undefined") {
                const sel = TacticalRenderer.selectedObject;
                if (sel) {
                    TacticalRenderer.clearPathPoints(sel.id);
                    tacticalProject = TacticalRenderer.getProject();
                    renderTacticalFrameList();
                }
            }
        });
    }

    // Path type selector
    const tacticalPathType = document.getElementById("tactical-path-type");
    if (tacticalPathType) {
        tacticalPathType.addEventListener("change", (e) => {
            if (typeof TacticalRenderer !== "undefined") {
                const sel = TacticalRenderer.selectedObject;
                if (sel) {
                    TacticalRenderer.setObjectPathType(sel.id, e.target.value);
                    tacticalProject = TacticalRenderer.getProject();
                }
            }
        });
    }

    // Easing selector
    const tacticalEasing = document.getElementById("tactical-easing");
    if (tacticalEasing) {
        tacticalEasing.addEventListener("change", (e) => {
            if (typeof TacticalRenderer !== "undefined") {
                const sel = TacticalRenderer.selectedObject;
                if (sel) {
                    TacticalRenderer.setObjectEasing(sel.id, e.target.value);
                    tacticalProject = TacticalRenderer.getProject();
                }
            }
        });
    }

    // Delay input
    const tacticalObjDelay = document.getElementById("tactical-obj-delay");
    if (tacticalObjDelay) {
        tacticalObjDelay.addEventListener("change", (e) => {
            if (typeof TacticalRenderer !== "undefined") {
                const sel = TacticalRenderer.selectedObject;
                if (sel) {
                    TacticalRenderer.setObjectDelay(sel.id, parseInt(e.target.value, 10) || 0);
                    tacticalProject = TacticalRenderer.getProject();
                    renderTacticalFrameList();
                }
            }
        });
    }

    // Pause input
    const tacticalObjPause = document.getElementById("tactical-obj-pause");
    if (tacticalObjPause) {
        tacticalObjPause.addEventListener("change", (e) => {
            if (typeof TacticalRenderer !== "undefined") {
                const sel = TacticalRenderer.selectedObject;
                if (sel) {
                    TacticalRenderer.setObjectPause(sel.id, parseInt(e.target.value, 10) || 0);
                    tacticalProject = TacticalRenderer.getProject();
                    renderTacticalFrameList();
                }
            }
        });
    }

    // Reports: expand/collapse run details
    document.addEventListener("click", (e) => {
        const toggleBtn = e.target.closest("[data-toggle-run]");
        if (toggleBtn) {
            const runId = toggleBtn.dataset.toggleRun;
            const detailsEl = document.querySelector(`[data-run-details="${runId}"]`);
            if (detailsEl) {
                const isHidden = detailsEl.style.display === "none";
                detailsEl.style.display = isHidden ? "block" : "none";
                toggleBtn.textContent = isHidden
                    ? (appState.lang === "zh" ? "\u25BC \u6536\u8d77\u8be6\u60c5" : "\u25BC Collapse")
                    : (appState.lang === "zh" ? "\u25B6 \u5c55\u5f00\u8be6\u60c5" : "\u25B6 Expand");
            }
        }
    });

    // Reports: copy run command
    document.addEventListener("click", (e) => {
        const copyBtn = e.target.closest("[data-copy-cmd]");
        if (copyBtn) {
            const cmd = copyBtn.dataset.copyCmd;
            if (cmd && navigator.clipboard) {
                navigator.clipboard.writeText(cmd).then(() => {
                    const orig = copyBtn.textContent;
                    copyBtn.textContent = "\u2713 Copied";
                    setTimeout(() => { copyBtn.textContent = orig; }, 1500);
                }).catch(() => {});
            }
        }
    });

    // Scouting: status badge click to cycle
    document.addEventListener("click", (e) => {
        const statusEl = e.target.closest("[data-queue-status]");
        if (statusEl) {
            const pKey = statusEl.dataset.queueStatus;
            cycleQueueStatus(pKey);
            renderScouting();
        }
    });

    // Scouting: sort toggle
    document.addEventListener("click", (e) => {
        const sortBtn = e.target.closest("[data-scout-sort]");
        if (sortBtn) {
            scoutSortMode = sortBtn.dataset.scoutSort;
            scoutCurrentPage = 1;
            renderScouting();
        }
        // Scouting pagination
        if (e.target.id === "scout-prev-page" && scoutCurrentPage > 1) {
            scoutCurrentPage--;
            renderScouting();
        }
        if (e.target.id === "scout-next-page") {
            scoutCurrentPage++;
            renderScouting();
        }
    });

    const scoutSearch = document.getElementById("scout-search");
    if (scoutSearch) {
        scoutSearch.addEventListener("input", (e) => {
            appState.scoutingQuery = e.target.value;
            scoutCurrentPage = 1;
            renderScouting();
        });
    }
    const scoutStatusFilter = document.getElementById("scout-status-filter");
    if (scoutStatusFilter) {
        scoutStatusFilter.addEventListener("change", (e) => {
            appState.scoutingStatus = e.target.value;
            scoutCurrentPage = 1;
            renderScouting();
        });
    }
    const scoutSnapshotButton = document.getElementById("scout-save-snapshot");
    if (scoutSnapshotButton) {
        scoutSnapshotButton.addEventListener("click", () => {
            saveWatchlistSnapshot(mergeScoutingRows(watchlistData, getPlayerWatchlist()));
            computeWatchlistDiff(mergeScoutingRows(watchlistData, getPlayerWatchlist()));
            renderScouting();
        });
    }
    const scoutExportButton = document.getElementById("scout-export-csv");
    if (scoutExportButton) scoutExportButton.addEventListener("click", exportReviewQueueCSV);

    const scoutWorkspaceExportButton = document.getElementById("scout-export-workspace");
    if (scoutWorkspaceExportButton) {
        scoutWorkspaceExportButton.addEventListener("click", exportScoutingWorkspace);
    }
    const scoutWorkspaceImportButton = document.getElementById("scout-import-workspace");
    const scoutWorkspaceFile = document.getElementById("scout-workspace-file");
    if (scoutWorkspaceImportButton && scoutWorkspaceFile) {
        scoutWorkspaceImportButton.addEventListener("click", () => scoutWorkspaceFile.click());
        scoutWorkspaceFile.addEventListener("change", async () => {
            const [file] = scoutWorkspaceFile.files || [];
            scoutWorkspaceFile.value = "";
            if (file) await previewScoutingWorkspaceImport(file);
        });
    }
    const scoutWorkspaceDialog = document.getElementById("scout-workspace-dialog");
    const scoutWorkspaceCancel = document.getElementById("scout-workspace-cancel");
    const scoutWorkspaceMerge = document.getElementById("scout-workspace-merge");
    const scoutWorkspaceReplace = document.getElementById("scout-workspace-replace");
    if (scoutWorkspaceCancel && scoutWorkspaceDialog) {
        scoutWorkspaceCancel.addEventListener("click", () => {
            pendingScoutingWorkspaceImport = null;
            scoutWorkspaceDialog.close();
        });
        scoutWorkspaceDialog.addEventListener("close", () => {
            pendingScoutingWorkspaceImport = null;
        });
    }
    if (scoutWorkspaceMerge) {
        scoutWorkspaceMerge.addEventListener("click", () => applyScoutingWorkspaceImport("merge"));
    }
    if (scoutWorkspaceReplace) {
        scoutWorkspaceReplace.addEventListener("click", () => applyScoutingWorkspaceImport("replace"));
    }

    // Scouting: note input change
    document.addEventListener("change", (e) => {
        if (e.target.matches(".scout-note-textarea") && e.target.dataset.notePlayer) {
            const pName = e.target.dataset.notePlayer;
            if (pName != null) {
                scoutShortlistNotes[pName] = e.target.value;
                saveScoutShortlistNotes();
            }
        }
        // Watchlist notes textarea
        if (e.target.matches(".scout-note-textarea") && e.target.dataset.wlNotePlayer) {
            const pName = e.target.dataset.wlNotePlayer;
            if (pName != null) {
                watchlistNotes[pName] = e.target.value;
                saveWatchlistNotes();
            }
        }
    });
    // Scouting: note input live update on keyup
    document.addEventListener("keyup", (e) => {
        if (e.target.matches(".scout-note-textarea") && e.target.dataset.notePlayer) {
            const pName = e.target.dataset.notePlayer;
            if (pName != null) {
                scoutShortlistNotes[pName] = e.target.value;
                saveScoutShortlistNotes();
            }
        }
        // Watchlist notes textarea live update
        if (e.target.matches(".scout-note-textarea") && e.target.dataset.wlNotePlayer) {
            const pName = e.target.dataset.wlNotePlayer;
            if (pName != null) {
                watchlistNotes[pName] = e.target.value;
                saveWatchlistNotes();
            }
        }
    });

    // Scouting: tactical role button click
    document.addEventListener("click", (e) => {
        const roleBtn = e.target.closest("[data-tactical-role]");
        if (roleBtn) {
            const pName = roleBtn.dataset.tacticalRole;
            const player = mergeScoutingRows(shortlistData, getPlayerShortlist())
                .find((p) => (p.player_name || p.name || "") === pName);
            if (player) {
                const role = generateTacticalRole(player);
                const roleEl = document.getElementById("player-tactical-role");
                if (roleEl) {
                    roleEl.innerHTML = `<div style="font-size:0.78rem;padding:0.3rem 0"><strong>${escapeHtml(t("tactical_role_label"))}:</strong> ${escapeHtml(role)}</div>`;
                }
            }
        }
    });

    // Value page: price band filter
    const priceBandSelect = document.getElementById("value-price-band");
    if (priceBandSelect) {
        priceBandSelect.addEventListener("change", (e) => {
            appState.valuePriceBand = e.target.value;
            renderValue();
        });
    }

    document.querySelectorAll("[data-action-mode]").forEach((button) => {
        button.addEventListener("click", () => {
            appState.actionMode = button.dataset.actionMode;
            renderActions();
        });
    });
    const actionSearch = document.getElementById("action-search");
    if (actionSearch) {
        actionSearch.addEventListener("input", (e) => {
            appState.actionQuery = e.target.value;
            renderActions();
        });
    }
    const actionCompetitionFilter = document.getElementById("action-competition-filter");
    if (actionCompetitionFilter) {
        actionCompetitionFilter.addEventListener("change", (e) => {
            appState.actionCompetition = e.target.value;
            renderActions();
        });
    }
    const actionMinutesFilter = document.getElementById("action-minutes-filter");
    if (actionMinutesFilter) {
        actionMinutesFilter.addEventListener("change", (e) => {
            appState.actionMinMinutes = Number(e.target.value || 0);
            renderActions();
        });
    }
    window.addEventListener("resize", () => {
        Object.values(appState.charts).forEach((chart) => {
            try { chart.resize(); } catch { /* ignore disposed chart */ }
        });
    });
}

// ── World Cup Data ───────────────────────────────────────────────────────

// Static group structure (official FIFA draw — not from API)
const WC_GROUPS = {
    A: ["Mexico", "South Africa", "South Korea", "Czech Republic"],
    B: ["Canada", "Bosnia and Herzegovina", "Qatar", "Switzerland"],
    C: ["Brazil", "Morocco", "Haiti", "Scotland"],
    D: ["United States", "Paraguay", "Australia", "Turkey"],
    E: ["Germany", "Curacao", "Ivory Coast", "Ecuador"],
    F: ["Netherlands", "Japan", "Sweden", "Tunisia"],
    G: ["Belgium", "Egypt", "Iran", "New Zealand"],
    H: ["Spain", "Cape Verde", "Saudi Arabia", "Uruguay"],
    I: ["France", "Senegal", "Iraq", "Norway"],
    J: ["Argentina", "Algeria", "Austria", "Jordan"],
    K: ["Portugal", "DR Congo", "Uzbekistan", "Colombia"],
    L: ["England", "Croatia", "Ghana", "Panama"],
};

const WC_HOSTS = ["United States", "Canada", "Mexico"];
const WC_BIG5 = new Set(["Premier League", "La Liga", "Bundesliga", "Serie A", "Ligue 1"]);

// API-driven World Cup data cache
let wcApiData = {
    groups: null,       // from /world-cup/groups
    schedule: null,     // from /world-cup/schedule
    squadCache: {},     // team -> from /world-cup/squads/{team}
    predictions: null,  // from /world-cup/predictions
    matchPredictionCache: {}, // home|away -> single-match prediction
    teams: null,        // from /worldcup/teams
    apiOnline: false,
    squadLoading: new Set(),
};

/* ── No demo squad data — API must be online for WC squads ─────────── */
const WC_DEMO_SQUADS = {};

async function fetchWcTeams() {
    try {
        const data = await fetchJson("/worldcup/teams", { fetchOpts: { signal: AbortSignal.timeout(60000) } });
        wcApiData.teams = data;
        wcApiData.apiOnline = true;
        return data;
    } catch (e) {
        console.warn("[WC] fetchWcTeams failed:", e.message);
        return null;
    }
}

async function fetchWcGroups() {
    try {
        const data = await fetchJson("/world-cup/groups", { fetchOpts: { signal: AbortSignal.timeout(60000) } });
        wcApiData.groups = data;
        wcApiData.apiOnline = true;
        return data;
    } catch (e) {
        console.warn("[WC] fetchWcGroups failed:", e.message);
        return null;
    }
}

async function fetchWcSchedule(group, matchday) {
    try {
        const data = await fetchJson("/world-cup/schedule", { fetchOpts: { signal: AbortSignal.timeout(60000) } });
        wcApiData.schedule = data;
        wcApiData.apiOnline = true;
        return data;
    } catch (e) {
        console.warn("[WC] fetchWcSchedule failed:", e.message);
        return null;
    }
}

async function fetchWcSquad(team) {
    if (wcApiData.squadCache[team]) return wcApiData.squadCache[team];
    wcApiData.squadLoading.add(team);
    try {
        const data = await fetchJson(`/world-cup/squads/${encodeURIComponent(team)}`, { fetchOpts: { signal: AbortSignal.timeout(60000) } });
        wcApiData.squadCache[team] = data;
        wcApiData.apiOnline = true;
        return data;
    } catch (e) {
        console.warn("[WC] fetchWcSquad failed:", e.message);
        return null;
    } finally {
        wcApiData.squadLoading.delete(team);
        if (appState.view === "wc_squads" && appState.wcSquadTeam === team) {
            renderWcSquads();
        }
    }
}

async function fetchWcPredictions() {
    try {
        const data = await fetchJson("/world-cup/predictions", { fetchOpts: { signal: AbortSignal.timeout(60000) } });
        wcApiData.predictions = data;
        wcApiData.apiOnline = true;
        return data;
    } catch (e) {
        console.warn("[WC] fetchWcPredictions failed:", e.message);
        return null;
    }
}

async function fetchWcMatchPrediction(teamA, teamB) {
    const cacheKey = `${teamA}|${teamB}`;
    if (wcApiData.matchPredictionCache[cacheKey]) return wcApiData.matchPredictionCache[cacheKey];

    // If API is offline, look up from pre-computed match_predictions.json
    if (apiOnline === false) {
        try {
            if (!wcApiData._matchPredictionsAll) {
                const mpData = await fetchJson("/world-cup/match-predictions");
                wcApiData._matchPredictionsAll = mpData && mpData.matches ? mpData.matches : [];
            }
            const found = wcApiData._matchPredictionsAll.find(
                (m) => (m.home === teamA && m.away === teamB) || (m.home === teamB && m.away === teamA)
            );
            if (found) {
                // Convert to the same format as the dynamic API response
                const result = {
                    home_team: found.home,
                    away_team: found.away,
                    home_win: found.home_win_p,
                    draw: found.draw_p,
                    away_win: found.away_win_p,
                    home_lambda: found.exp_home_goals,
                    away_lambda: found.exp_away_goals,
                    model_type: "poisson_strength_ratio",
                    model_version: "wc-static-1.0",
                    score_matrix: null,
                };
                wcApiData.matchPredictionCache[cacheKey] = result;
                return result;
            }
        } catch (e) {
            console.warn("[WC] static match prediction lookup failed:", e.message);
        }
        return null;
    }

    try {
        const data = await fetchJson(`/world-cup/predictions/${encodeURIComponent(teamA)}/${encodeURIComponent(teamB)}`, {
            fetchOpts: { signal: AbortSignal.timeout(60000) },
        });
        wcApiData.matchPredictionCache[cacheKey] = data;
        wcApiData.apiOnline = true;
        return data;
    } catch (e) {
        console.warn("[WC] fetchWcMatchPrediction failed:", e.message);
        return null;
    }
}

function wcAllTeams() {
    if (wcApiData.teams && wcApiData.teams.teams) {
        return wcApiData.teams.teams.map((t) => t.team);
    }
    return Object.values(WC_GROUPS).flat();
}

function wcTeamGroup(team) {
    if (wcApiData.teams && wcApiData.teams.teams) {
        const entry = wcApiData.teams.teams.find((t) => t.team === team);
        if (entry) return entry.group;
    }
    for (const [letter, teams] of Object.entries(WC_GROUPS)) {
        if (teams.includes(team)) return letter;
    }
    return "?";
}

// Get enriched squad data (from API cache, or return empty)
function wcGetSquad(team) {
    const cached = wcApiData.squadCache[team];
    if (cached && cached.players) {
        return cached.players.map((p) => ({
            name: p.name,
            position: p.position,
            club: p.club,
            league: p.club_league,
            hasRating: p.has_rating,
            rating: p.rating,
            confidence: p.rating_confidence ? p.rating_confidence.toUpperCase() : "NONE",
        }));
    }
    return [];
}

/* Match squad player names against the global ratings (players) array */
function matchSquadWithRatings(squad) {
    if (!players || players.length === 0) return squad;
    const ratingMap = {};
    for (const p of players) {
        const key = (p.name || "").toLowerCase();
        if (key) ratingMap[key] = p;
    }
    return squad.map((sp) => {
        if (sp.hasRating) return sp;
        const key = (sp.name || "").toLowerCase();
        const match = ratingMap[key];
        if (match) {
            return {
                ...sp,
                hasRating: true,
                rating: match.rating,
                confidence: match.confidence || "LOW",
                position: sp.position || match.position,
            };
        }
        return sp;
    });
}

// Compute team strength from API data or fallback
function wcTeamStrength(team) {
    // Try from teams API data
    if (wcApiData.teams && wcApiData.teams.teams) {
        const entry = wcApiData.teams.teams.find((t) => t.team === team);
        if (entry) return entry.strength;
    }
    // Try from predictions API data
    if (wcApiData.predictions && wcApiData.predictions.ranking) {
        const entry = wcApiData.predictions.ranking.find((r) => r.team === team);
        if (entry) return entry.strength;
    }
    // Try from groups API data
    if (wcApiData.groups && wcApiData.groups.groups) {
        for (const g of wcApiData.groups.groups) {
            const t = g.teams.find((t) => t.team === team);
            if (t) return t.strength;
        }
    }
    // Fallback: compute from squad
    const squad = wcGetSquad(team);
    const rated = squad.filter((p) => p.hasRating);
    if (rated.length > 0) {
        const avg = rated.reduce((s, p) => s + p.rating, 0) / rated.length;
        const ratingScore = Math.min(Math.max((avg - 30) / 70, 0), 1);
        const big5Count = squad.filter((p) => WC_BIG5.has(p.league)).length;
        const big5Score = Math.min(big5Count / 10, 1);
        return 0.7 * ratingScore + 0.3 * big5Score;
    }
    return 0.2;
}

// ── World Cup Renderers ──────────────────────────────────────────────────

function renderWcSchedule() {
    const groupFilter = document.getElementById("wc-group-filter").value;
    const mdFilter = document.getElementById("wc-matchday-filter").value;

    // Groups overview — use API data if available
    const overview = document.getElementById("wc-groups-overview");
    if (wcApiData.groups && wcApiData.groups.groups) {
        overview.innerHTML = wcApiData.groups.groups.map((g) => {
            const hostTag = (tm) => tm.is_host ? " ★" : "";
            return `<article class="liquid-panel compact-panel">
                <h3>${escapeHtml(g.group)}</h3>
                <ul class="wc-group-list">${g.teams.map((tm, i) => `<li>${i + 1}. ${escapeHtml(tm.team)}${hostTag(tm)}${tm.avg_rating ? ` <span style="color:var(--text-muted);font-size:0.8em">(${tm.avg_rating})</span>` : ""}</li>`).join("")}</ul>
            </article>`;
        }).join("");
    } else {
        overview.innerHTML = Object.entries(WC_GROUPS).map(([letter, teams]) => {
            const hostTag = (tm) => WC_HOSTS.includes(tm) ? " ★" : "";
            return `<article class="liquid-panel compact-panel">
                <h3>${escapeHtml(letter)}</h3>
                <ul class="wc-group-list">${teams.map((tm, i) => `<li>${i + 1}. ${escapeHtml(tm)}${hostTag(tm)}</li>`).join("")}</ul>
            </article>`;
        }).join("");
    }

    // Show DEMO badge if API offline
    const scheduleTitle = document.getElementById("wc-schedule-title");
    if (scheduleTitle) {
        let indicator = scheduleTitle.querySelector(".data-source-indicator");
        if (!indicator) {
            indicator = document.createElement("span");
            indicator.className = "status-pill data-source-indicator";
            scheduleTitle.appendChild(indicator);
        }
        if (!wcApiData.apiOnline) {
            indicator.textContent = "DEMO";
            indicator.className = "status-pill status-low data-source-indicator";
        } else {
            indicator.textContent = "";
            indicator.className = "status-pill data-source-indicator";
        }
    }

    // Use API schedule if available, otherwise generate locally
    let matches = [];
    if (wcApiData.schedule && wcApiData.schedule.matches) {
        matches = wcApiData.schedule.matches;
    } else {
        // Fallback: official 2026 World Cup schedule (all times ET)
        const schedule = [
            // Group A
            {date:"2026-06-11",time_et:"15:00",group:"A",home:"Mexico",away:"South Africa",venue:"Estadio Azteca",city:"Mexico City",matchday:1},
            {date:"2026-06-11",time_et:"22:00",group:"A",home:"South Korea",away:"Czech Republic",venue:"Estadio Akron",city:"Guadalajara",matchday:1},
            {date:"2026-06-18",time_et:"12:00",group:"A",home:"South Africa",away:"Czech Republic",venue:"Mercedes-Benz Stadium",city:"Atlanta",matchday:2},
            {date:"2026-06-18",time_et:"21:00",group:"A",home:"Mexico",away:"South Korea",venue:"Estadio Akron",city:"Guadalajara",matchday:2},
            {date:"2026-06-24",time_et:"21:00",group:"A",home:"Mexico",away:"Czech Republic",venue:"Estadio Azteca",city:"Mexico City",matchday:3},
            {date:"2026-06-24",time_et:"21:00",group:"A",home:"South Africa",away:"South Korea",venue:"Estadio BBVA",city:"Monterrey",matchday:3},
            // Group B
            {date:"2026-06-12",time_et:"15:00",group:"B",home:"Canada",away:"Bosnia and Herzegovina",venue:"BMO Field",city:"Toronto",matchday:1},
            {date:"2026-06-13",time_et:"15:00",group:"B",home:"Qatar",away:"Switzerland",venue:"Levi's Stadium",city:"San Francisco Bay Area",matchday:1},
            {date:"2026-06-18",time_et:"15:00",group:"B",home:"Bosnia and Herzegovina",away:"Switzerland",venue:"SoFi Stadium",city:"Los Angeles",matchday:2},
            {date:"2026-06-18",time_et:"18:00",group:"B",home:"Canada",away:"Qatar",venue:"BC Place",city:"Vancouver",matchday:2},
            {date:"2026-06-24",time_et:"15:00",group:"B",home:"Bosnia and Herzegovina",away:"Qatar",venue:"Lumen Field",city:"Seattle",matchday:3},
            {date:"2026-06-24",time_et:"15:00",group:"B",home:"Canada",away:"Switzerland",venue:"BC Place",city:"Vancouver",matchday:3},
            // Group C
            {date:"2026-06-13",time_et:"18:00",group:"C",home:"Brazil",away:"Morocco",venue:"MetLife Stadium",city:"New York/New Jersey",matchday:1},
            {date:"2026-06-13",time_et:"21:00",group:"C",home:"Haiti",away:"Scotland",venue:"Gillette Stadium",city:"Boston",matchday:1},
            {date:"2026-06-19",time_et:"18:00",group:"C",home:"Morocco",away:"Scotland",venue:"Gillette Stadium",city:"Boston",matchday:2},
            {date:"2026-06-19",time_et:"21:00",group:"C",home:"Haiti",away:"Brazil",venue:"Lincoln Financial Field",city:"Philadelphia",matchday:2},
            {date:"2026-06-24",time_et:"18:00",group:"C",home:"Morocco",away:"Haiti",venue:"Mercedes-Benz Stadium",city:"Atlanta",matchday:3},
            {date:"2026-06-24",time_et:"18:00",group:"C",home:"Brazil",away:"Scotland",venue:"Hard Rock Stadium",city:"Miami",matchday:3},
            // Group D
            {date:"2026-06-12",time_et:"21:00",group:"D",home:"United States",away:"Paraguay",venue:"SoFi Stadium",city:"Los Angeles",matchday:1},
            {date:"2026-06-13",time_et:"00:00",group:"D",home:"Australia",away:"Turkey",venue:"BC Place",city:"Vancouver",matchday:1},
            {date:"2026-06-19",time_et:"00:00",group:"D",home:"Paraguay",away:"Turkey",venue:"Levi's Stadium",city:"San Francisco Bay Area",matchday:2},
            {date:"2026-06-19",time_et:"15:00",group:"D",home:"United States",away:"Australia",venue:"Lumen Field",city:"Seattle",matchday:2},
            {date:"2026-06-25",time_et:"22:00",group:"D",home:"United States",away:"Turkey",venue:"SoFi Stadium",city:"Los Angeles",matchday:3},
            {date:"2026-06-25",time_et:"22:00",group:"D",home:"Paraguay",away:"Australia",venue:"Levi's Stadium",city:"San Francisco Bay Area",matchday:3},
            // Group E
            {date:"2026-06-14",time_et:"13:00",group:"E",home:"Germany",away:"Curacao",venue:"NRG Stadium",city:"Houston",matchday:1},
            {date:"2026-06-14",time_et:"19:00",group:"E",home:"Ivory Coast",away:"Ecuador",venue:"Lincoln Financial Field",city:"Philadelphia",matchday:1},
            {date:"2026-06-20",time_et:"16:00",group:"E",home:"Germany",away:"Ivory Coast",venue:"BMO Field",city:"Toronto",matchday:2},
            {date:"2026-06-20",time_et:"20:00",group:"E",home:"Curacao",away:"Ecuador",venue:"Arrowhead Stadium",city:"Kansas City",matchday:2},
            {date:"2026-06-25",time_et:"16:00",group:"E",home:"Germany",away:"Ecuador",venue:"MetLife Stadium",city:"New York/New Jersey",matchday:3},
            {date:"2026-06-25",time_et:"16:00",group:"E",home:"Curacao",away:"Ivory Coast",venue:"Lincoln Financial Field",city:"Philadelphia",matchday:3},
            // Group F
            {date:"2026-06-14",time_et:"16:00",group:"F",home:"Netherlands",away:"Japan",venue:"AT&T Stadium",city:"Dallas",matchday:1},
            {date:"2026-06-14",time_et:"19:00",group:"F",home:"Sweden",away:"Tunisia",venue:"Estadio BBVA",city:"Monterrey",matchday:1},
            {date:"2026-06-20",time_et:"13:00",group:"F",home:"Netherlands",away:"Sweden",venue:"NRG Stadium",city:"Houston",matchday:2},
            {date:"2026-06-20",time_et:"00:00",group:"F",home:"Japan",away:"Tunisia",venue:"Estadio BBVA",city:"Monterrey",matchday:2},
            {date:"2026-06-25",time_et:"19:00",group:"F",home:"Netherlands",away:"Tunisia",venue:"Arrowhead Stadium",city:"Kansas City",matchday:3},
            {date:"2026-06-25",time_et:"19:00",group:"F",home:"Japan",away:"Sweden",venue:"AT&T Stadium",city:"Dallas",matchday:3},
            // Group G
            {date:"2026-06-15",time_et:"15:00",group:"G",home:"Belgium",away:"Egypt",venue:"Lumen Field",city:"Seattle",matchday:1},
            {date:"2026-06-15",time_et:"21:00",group:"G",home:"Iran",away:"New Zealand",venue:"SoFi Stadium",city:"Los Angeles",matchday:1},
            {date:"2026-06-21",time_et:"15:00",group:"G",home:"Belgium",away:"Iran",venue:"SoFi Stadium",city:"Los Angeles",matchday:2},
            {date:"2026-06-21",time_et:"21:00",group:"G",home:"Egypt",away:"New Zealand",venue:"BC Place",city:"Vancouver",matchday:2},
            {date:"2026-06-26",time_et:"23:00",group:"G",home:"Belgium",away:"New Zealand",venue:"BC Place",city:"Vancouver",matchday:3},
            {date:"2026-06-26",time_et:"23:00",group:"G",home:"Egypt",away:"Iran",venue:"Lumen Field",city:"Seattle",matchday:3},
            // Group H
            {date:"2026-06-15",time_et:"12:00",group:"H",home:"Spain",away:"Cape Verde",venue:"Mercedes-Benz Stadium",city:"Atlanta",matchday:1},
            {date:"2026-06-15",time_et:"18:00",group:"H",home:"Saudi Arabia",away:"Uruguay",venue:"Hard Rock Stadium",city:"Miami",matchday:1},
            {date:"2026-06-21",time_et:"12:00",group:"H",home:"Spain",away:"Saudi Arabia",venue:"Mercedes-Benz Stadium",city:"Atlanta",matchday:2},
            {date:"2026-06-21",time_et:"18:00",group:"H",home:"Cape Verde",away:"Uruguay",venue:"Hard Rock Stadium",city:"Miami",matchday:2},
            {date:"2026-06-26",time_et:"20:00",group:"H",home:"Spain",away:"Uruguay",venue:"Estadio Akron",city:"Guadalajara",matchday:3},
            {date:"2026-06-26",time_et:"20:00",group:"H",home:"Cape Verde",away:"Saudi Arabia",venue:"NRG Stadium",city:"Houston",matchday:3},
            // Group I
            {date:"2026-06-16",time_et:"15:00",group:"I",home:"France",away:"Senegal",venue:"MetLife Stadium",city:"New York/New Jersey",matchday:1},
            {date:"2026-06-16",time_et:"18:00",group:"I",home:"Iraq",away:"Norway",venue:"Gillette Stadium",city:"Boston",matchday:1},
            {date:"2026-06-22",time_et:"17:00",group:"I",home:"France",away:"Iraq",venue:"Lincoln Financial Field",city:"Philadelphia",matchday:2},
            {date:"2026-06-22",time_et:"20:00",group:"I",home:"Senegal",away:"Norway",venue:"MetLife Stadium",city:"New York/New Jersey",matchday:2},
            {date:"2026-06-26",time_et:"15:00",group:"I",home:"France",away:"Norway",venue:"Gillette Stadium",city:"Boston",matchday:3},
            {date:"2026-06-26",time_et:"15:00",group:"I",home:"Iraq",away:"Senegal",venue:"BMO Field",city:"Toronto",matchday:3},
            // Group J
            {date:"2026-06-16",time_et:"21:00",group:"J",home:"Argentina",away:"Algeria",venue:"Arrowhead Stadium",city:"Kansas City",matchday:1},
            {date:"2026-06-16",time_et:"00:00",group:"J",home:"Austria",away:"Jordan",venue:"Levi's Stadium",city:"San Francisco Bay Area",matchday:1},
            {date:"2026-06-22",time_et:"13:00",group:"J",home:"Argentina",away:"Austria",venue:"AT&T Stadium",city:"Dallas",matchday:2},
            {date:"2026-06-22",time_et:"23:00",group:"J",home:"Algeria",away:"Jordan",venue:"Levi's Stadium",city:"San Francisco Bay Area",matchday:2},
            {date:"2026-06-27",time_et:"22:00",group:"J",home:"Argentina",away:"Jordan",venue:"AT&T Stadium",city:"Dallas",matchday:3},
            {date:"2026-06-27",time_et:"22:00",group:"J",home:"Algeria",away:"Austria",venue:"Arrowhead Stadium",city:"Kansas City",matchday:3},
            // Group K
            {date:"2026-06-17",time_et:"13:00",group:"K",home:"Portugal",away:"DR Congo",venue:"NRG Stadium",city:"Houston",matchday:1},
            {date:"2026-06-17",time_et:"22:00",group:"K",home:"Uzbekistan",away:"Colombia",venue:"Estadio Azteca",city:"Mexico City",matchday:1},
            {date:"2026-06-23",time_et:"13:00",group:"K",home:"Portugal",away:"Uzbekistan",venue:"NRG Stadium",city:"Houston",matchday:2},
            {date:"2026-06-23",time_et:"22:00",group:"K",home:"DR Congo",away:"Colombia",venue:"Estadio Akron",city:"Guadalajara",matchday:2},
            {date:"2026-06-27",time_et:"19:30",group:"K",home:"Portugal",away:"Colombia",venue:"Hard Rock Stadium",city:"Miami",matchday:3},
            {date:"2026-06-27",time_et:"19:30",group:"K",home:"DR Congo",away:"Uzbekistan",venue:"Mercedes-Benz Stadium",city:"Atlanta",matchday:3},
            // Group L
            {date:"2026-06-17",time_et:"16:00",group:"L",home:"England",away:"Croatia",venue:"AT&T Stadium",city:"Dallas",matchday:1},
            {date:"2026-06-17",time_et:"19:00",group:"L",home:"Ghana",away:"Panama",venue:"BMO Field",city:"Toronto",matchday:1},
            {date:"2026-06-23",time_et:"16:00",group:"L",home:"England",away:"Ghana",venue:"Gillette Stadium",city:"Boston",matchday:2},
            {date:"2026-06-23",time_et:"19:00",group:"L",home:"Croatia",away:"Panama",venue:"BMO Field",city:"Toronto",matchday:2},
            {date:"2026-06-27",time_et:"17:00",group:"L",home:"England",away:"Panama",venue:"MetLife Stadium",city:"New York/New Jersey",matchday:3},
            {date:"2026-06-27",time_et:"17:00",group:"L",home:"Croatia",away:"Ghana",venue:"Lincoln Financial Field",city:"Philadelphia",matchday:3},
        ];
        matches = schedule;
    }

    const filtered = matches.filter((m) => {
        if (groupFilter !== "ALL" && m.group !== groupFilter) return false;
        if (mdFilter !== "ALL" && String(m.matchday) !== mdFilter) return false;
        return true;
    });

    const tbody = document.getElementById("wc-schedule-table");
    tbody.innerHTML = filtered.map((m, index) => `<tr data-wc-home="${escapeAttr(m.home)}" data-wc-away="${escapeAttr(m.away)}" data-row-index="${index}" style="cursor:pointer">
        <td>${escapeHtml(m.date)}</td><td>${escapeHtml(m.time_et || m.time)} ET</td><td>${escapeHtml(m.group)}</td>
        <td>${escapeHtml(m.home)}</td><td>${escapeHtml(m.away)}</td><td>${escapeHtml(m.venue)}, ${escapeHtml(m.city)}</td>
    </tr>`).join("");

    tbody.querySelectorAll("tr[data-wc-home][data-wc-away]").forEach((row) => {
        row.addEventListener("click", async () => {
            const home = row.dataset.wcHome;
            const away = row.dataset.wcAway;
            if (!home || !away) return;
            appState.wcCompareA = home;
            appState.wcCompareB = away;
            const selA = document.getElementById("wc-compare-a");
            const selB = document.getElementById("wc-compare-b");
            if (selA) selA.value = home;
            if (selB) selB.value = away;
            await Promise.all([
                fetchWcSquad(home),
                fetchWcSquad(away),
                fetchWcMatchPrediction(home, away),
            ]);
            await setView("wc_compare");
        });
    });
}

function renderWcSquads() {
    const team = appState.wcSquadTeam;
    const rawSquad = wcGetSquad(team);
    const tbody = document.getElementById("wc-squad-table");
    const summary = document.getElementById("wc-squad-summary");
    if (rawSquad.length === 0) {
        const loading = wcApiData.squadLoading.has(team);
        const message = loading
            ? (appState.lang === "zh" ? "正在加载球队名单..." : "Loading squad...")
            : (appState.lang === "zh" ? "球队名单暂不可用" : "Squad unavailable");
        if (summary) {
            summary.innerHTML = `<div class="wc-metric"><span class="metric-value">${loading ? "…" : "—"}</span><span>${escapeHtml(message)}</span></div>`;
        }
        if (tbody) {
            tbody.innerHTML = `<tr><td colspan="6" style="text-align:center;color:var(--text-muted)">${escapeHtml(message)}</td></tr>`;
        }
        const chart = getChart("wc-squad-chart");
        if (chart) chart.clear();
        return;
    }
    // Enrich squad with real ratings from /ratings API data
    const squad = matchSquadWithRatings(rawSquad);
    const rated = squad.filter((p) => p.hasRating);
    const big5 = squad.filter((p) => WC_BIG5.has(p.league));
    const avgRating = rated.length > 0 ? (rated.reduce((s, p) => s + p.rating, 0) / rated.length).toFixed(2) : "\u2014";
    const group = wcTeamGroup(team);

    // Show DEMO badge if API offline
    const squadTitle = document.getElementById("wc-squad-title");
    if (squadTitle) {
        let indicator = squadTitle.querySelector(".data-source-indicator");
        if (!indicator) {
            indicator = document.createElement("span");
            indicator.className = "status-pill data-source-indicator";
            squadTitle.appendChild(indicator);
        }
        if (!wcApiData.apiOnline) {
            indicator.textContent = "DEMO";
            indicator.className = "status-pill status-low data-source-indicator";
        } else {
            indicator.textContent = "";
            indicator.className = "status-pill data-source-indicator";
        }
    }

    // Coverage summary: X/Y players have ratings
    const coverageLabel = appState.lang === "zh"
        ? `${rated.length}/${squad.length} \u7403\u5458\u6709\u8bc4\u5206`
        : `${rated.length}/${squad.length} players rated`;

    document.getElementById("wc-squad-summary").innerHTML = `
        <div class="wc-metric"><span class="metric-value">${squad.length}</span><span>${escapeHtml(t("wc_squad_size"))}</span></div>
        <div class="wc-metric"><span class="metric-value">${rated.length}</span><span>${escapeHtml(t("wc_rated"))}</span></div>
        <div class="wc-metric"><span class="metric-value">${big5.length}</span><span>${escapeHtml(t("wc_big5"))}</span></div>
        <div class="wc-metric"><span class="metric-value">${escapeHtml(avgRating)}</span><span>${escapeHtml(t("wc_avg_rating"))}</span></div>
        <div class="wc-metric"><span class="metric-value">${escapeHtml(group)}</span><span>${escapeHtml(t("wc_group_col"))}</span></div>
        <div class="wc-metric"><span class="metric-value">${escapeHtml(coverageLabel)}</span><span>\u25CE ${escapeHtml(t("coverage"))}</span></div>
    `;

    tbody.innerHTML = squad.map((p) => {
        const confClass = p.hasRating
            ? (p.confidence === "HIGH" ? "status-high" : "status-medium")
            : "status-low";
        const confText = p.hasRating ? p.confidence : (appState.lang === "zh" ? "\u65E0\u6570\u636E" : "N/A");
        const ratingText = p.hasRating ? p.rating.toFixed(2) : "\u2014";
        const posText = p.position || "\u2014";
        return `<tr>
            <td>${escapeHtml(p.name)}</td><td>${escapeHtml(posText)}</td><td>${escapeHtml(p.club)}</td><td>${escapeHtml(p.league)}</td>
            <td>${escapeHtml(ratingText)}</td>
            <td><span class="status-pill ${confClass}">${escapeHtml(confText)}</span></td>
        </tr>`;
    }).join("");

    // Rating distribution chart
    const chart = getChart("wc-squad-chart");
    if (!chart) return;
    const chartData = [...rated].sort((a, b) => b.rating - a.rating);
    chart.setOption({
        animation: false,
        grid: {left: 80, right: 20, top: 20, bottom: 40},
        xAxis: {type: "value", axisLabel: {color: chartTextColor()}, splitLine: {lineStyle: {color: chartGridColor()}}},
        yAxis: {type: "category", data: chartData.map((p) => p.name), axisLabel: {color: chartTextColor(), fontSize: 11}},
        series: [{type: "bar", data: chartData.map((p) => p.rating), itemStyle: {color: "#7ca8ff"}}],
    }, true);
    chart.resize();

    if (squad.length > 0 && rated.length / squad.length < 0.5) {
        document.getElementById("wc-squad-summary").innerHTML += `<div class="wc-warning">\u25B2 ${escapeHtml(t("wc_low_coverage"))}</div>`;
    }
}

function renderWcCompare() {
    const teamA = appState.wcCompareA;
    const teamB = appState.wcCompareB;
    const squadA = wcGetSquad(teamA);
    const squadB = wcGetSquad(teamB);
    const ratedA = squadA.filter((p) => p.hasRating);
    const ratedB = squadB.filter((p) => p.hasRating);

    document.getElementById("wc-compare-a-name").textContent = teamA;
    document.getElementById("wc-compare-b-name").textContent = teamB;

    const avgA = ratedA.length > 0 ? (ratedA.reduce((s, p) => s + p.rating, 0) / ratedA.length).toFixed(2) : "—";
    const avgB = ratedB.length > 0 ? (ratedB.reduce((s, p) => s + p.rating, 0) / ratedB.length).toFixed(2) : "—";
    const big5A = squadA.filter((p) => WC_BIG5.has(p.league)).length;
    const big5B = squadB.filter((p) => WC_BIG5.has(p.league)).length;

    document.getElementById("wc-compare-table").innerHTML = [
        [t("wc_squad_size"), squadA.length, squadB.length],
        [t("wc_rated"), ratedA.length, ratedB.length],
        [t("wc_big5"), big5A, big5B],
        [t("wc_avg_rating"), avgA, avgB],
    ].map(([label, a, b]) => `<tr><td>${escapeHtml(label)}</td><td>${escapeHtml(a)}</td><td>${escapeHtml(b)}</td></tr>`).join("");

    // Chart
    const chart = getChart("wc-compare-chart");
    if (chart) {
        const allRated = [
            ...ratedA.map((p) => ({...p, team: teamA})),
            ...ratedB.map((p) => ({...p, team: teamB})),
        ].sort((a, b) => b.rating - a.rating);
        chart.setOption({
            animation: false,
            grid: {left: 80, right: 20, top: 20, bottom: 40},
            xAxis: {type: "value", axisLabel: {color: chartTextColor()}, splitLine: {lineStyle: {color: chartGridColor()}}},
            yAxis: {type: "category", data: allRated.map((p) => p.name), axisLabel: {color: chartTextColor(), fontSize: 11}},
            series: [{type: "bar", data: allRated.map((p) => ({value: p.rating, itemStyle: {color: p.team === teamA ? "#7ca8ff" : "#57d68d"}}))}],
        }, true);
        chart.resize();
    }

    // Top 5
    const renderTop = (rated, el) => {
        el.innerHTML = rated.sort((a, b) => b.rating - a.rating).slice(0, 5).map((p) =>
            `<div class="rank-item"><div><strong>${escapeHtml(p.name)}</strong><span class="rank-meta">${escapeHtml(p.position)} · ${escapeHtml(p.club)}</span></div><span class="status-pill status-high">${p.rating.toFixed(2)}</span></div>`
        ).join("") || `<div style="color:var(--text-muted);text-align:center;padding:1rem">${t("wc_no_data")}</div>`;
    };
    document.getElementById("wc-compare-a-top-title").textContent = `${teamA} Top 5`;
    document.getElementById("wc-compare-b-top-title").textContent = `${teamB} Top 5`;
    renderTop([...ratedA], document.getElementById("wc-compare-a-top"));
    renderTop([...ratedB], document.getElementById("wc-compare-b-top"));

    renderWcMatchPredictionPanel(teamA, teamB);
}

function renderWcMatchPredictionPanel(teamA, teamB) {
    const panel = document.getElementById("wc-match-prediction-panel");
    if (!panel) return;

    const cacheKey = `${teamA}|${teamB}`;
    const prediction = wcApiData.matchPredictionCache[cacheKey];
    if (!prediction || prediction.error) {
        panel.innerHTML = `<div style="color:var(--text-muted);padding:0.8rem 0">${escapeHtml(t("wc_no_data"))}</div>`;
        return;
    }

    const match = {
        home: prediction.home_team || teamA,
        away: prediction.away_team || teamB,
        hw: prediction.home_win || 0,
        draw: prediction.draw || 0,
        aw: prediction.away_win || 0,
        xh: prediction.home_lambda || 0,
        xa: prediction.away_lambda || 0,
        score_matrix: prediction.score_matrix || null,
        model_type: prediction.model_type || "world_cup_strength_poisson",
        model_version: prediction.model_version || "wc-1.0",
    };

    const z = appState.lang === "zh";
    panel.innerHTML = `
        <div class="layout-2">
            <article class="liquid-panel table-panel">
                <div class="panel-head">
                    <h3>${escapeHtml(match.home)} vs ${escapeHtml(match.away)}</h3>
                    <span class="status-pill status-medium">${escapeHtml(match.model_type)}</span>
                </div>
                <div id="wc-match-probabilities"></div>
                <div class="wc-summary-row" id="wc-match-detail" style="margin-top:0.8rem"></div>
                <div id="wc-outcome-bar-chart" class="chart-box" style="height:220px;margin-top:0.8rem"></div>
            </article>
            <article class="liquid-panel chart-panel">
                <div class="panel-head">
                    <h3>${z ? "比分矩阵" : "Score Matrix"}</h3>
                </div>
                <div id="wc-score-chart" class="chart-box" style="height:340px"></div>
            </article>
        </div>
    `;

    document.getElementById("wc-match-probabilities").innerHTML = [
        [z ? "主胜" : "Home", match.hw],
        [z ? "平局" : "Draw", match.draw],
        [z ? "客胜" : "Away", match.aw],
    ].map(([label, value]) => `
        <div class="probability-row">
            <span class="probability-label">${escapeHtml(label)}</span>
            <div class="probability-track"><div class="probability-fill" style="width:${sanitizeCssPercent(value * 100)}%"></div></div>
            <strong>${sanitizeCssPercent(value * 100)}%</strong>
        </div>
    `).join("");

    document.getElementById("wc-match-detail").innerHTML = `
        <div><span>${escapeHtml(t("expected_goals"))}</span><strong>${match.xh.toFixed(2)} / ${match.xa.toFixed(2)}</strong></div>
        <div><span>${z ? "强度" : "Strength"}</span><strong>${Number(prediction.home_strength || 0).toFixed(3)} / ${Number(prediction.away_strength || 0).toFixed(3)}</strong></div>
        <div><span>model</span><strong>${escapeHtml(match.model_version)}</strong></div>
        <div><span>${z ? "主场修正" : "Host bonus"}</span><strong>${Number(prediction.host_bonus || 0).toFixed(2)}</strong></div>
    `;

    renderScoreMatrixInto("wc-score-chart", match);
    renderOutcomeBarInto("wc-outcome-bar-chart", match);
}

function renderWcProbability() {
    // Use API predictions if available
    if (wcApiData.predictions && wcApiData.predictions.groups) {
        // Group probability cards from API
        const container = document.getElementById("wc-prob-groups");
        container.innerHTML = wcApiData.predictions.groups.map((g) => {
            const rows = g.teams.map((x) => {
                const pct = Math.round(x.p_advance * 100);
                return `<div class="wc-prob-row"><span>${escapeHtml(x.team)}</span><div class="probability-track"><div class="probability-fill" style="width:${sanitizeCssPercent(pct)}%"></div></div><strong>${pct}%</strong></div>`;
            }).join("");
            return `<article class="liquid-panel compact-panel"><h3>${escapeHtml(g.group)}</h3>${rows}</article>`;
        }).join("");

        // 48-team ranking from API
        const ranking = wcApiData.predictions.ranking || [];
        document.getElementById("wc-prob-table").innerHTML = ranking.map((x) => `<tr>
            <td>${x.rank}</td><td>${escapeHtml(x.team)}</td><td>${escapeHtml(x.group || "?")}</td><td>${x.strength.toFixed(3)}</td>
        </tr>`).join("");
    } else {
        // Fallback: compute locally with proper ranking probability model
        const _AMP = 2.5; // exponent to widen gap between strong/weak teams
        const teams = wcAllTeams();
        const strengths = {};
        teams.forEach((t) => { strengths[t] = wcTeamStrength(t); });

        const container = document.getElementById("wc-prob-groups");
        container.innerHTML = Object.entries(WC_GROUPS).map(([letter, groupTeams]) => {
            const teamStrs = groupTeams.map((t) => ({team: t, raw: strengths[t], strength: Math.pow(strengths[t], _AMP)}));
            const total = teamStrs.reduce((s, x) => s + x.strength, 0);
            const rows = teamStrs.sort((a, b) => b.raw - a.raw).map((x) => {
                const p1 = x.strength / total;
                let p2 = 0;
                for (const other of teamStrs) {
                    if (other.team === x.team) continue;
                    const p1Other = other.strength / total;
                    const remaining = total - other.strength;
                    p2 += p1Other * (remaining > 0 ? x.strength / remaining : 0);
                }
                // p3rd: sum over each pair (j, k) being 1st and 2nd, prob i is best of remaining
                let p3 = 0;
                for (const j of teamStrs) {
                    if (j.team === x.team) continue;
                    const p1J = j.strength / total;
                    const remJ = total - j.strength;
                    for (const k of teamStrs) {
                        if (k.team === x.team || k.team === j.team) continue;
                        const p2Jk = p1J * (remJ > 0 ? k.strength / remJ : 0);
                        const remJk = total - j.strength - k.strength;
                        p3 += p2Jk * (remJk > 0 ? x.strength / remJk : 0);
                    }
                }
                const pAdvance = Math.min(p1 + p2 + p3 * (8 / 12), 1.0);
                const pct = Math.round(pAdvance * 100);
                return `<div class="wc-prob-row"><span>${escapeHtml(x.team)}</span><div class="probability-track"><div class="probability-fill" style="width:${sanitizeCssPercent(pct)}%"></div></div><strong>${pct}%</strong></div>`;
            }).join("");
            return `<article class="liquid-panel compact-panel"><h3>${escapeHtml(letter)}</h3>${rows}</article>`;
        }).join("");

        const ranked = teams.map((t) => ({team: t, strength: strengths[t], group: wcTeamGroup(t)}))
            .sort((a, b) => b.strength - a.strength);
        document.getElementById("wc-prob-table").innerHTML = ranked.map((x, i) => `<tr>
            <td>${i + 1}</td><td>${escapeHtml(x.team)}</td><td>${escapeHtml(x.group)}</td><td>${x.strength.toFixed(3)}</td>
        </tr>`).join("");
    }
}

// ── Init World Cup ───────────────────────────────────────────────────────

async function initWorldCup() {
    const teams = wcAllTeams();
    // Populate group filter
    const groupFilter = document.getElementById("wc-group-filter");
    groupFilter.innerHTML = '<option value="ALL">ALL</option>' +
        Object.keys(WC_GROUPS).map((g) => `<option value="${escapeAttr(g)}">${escapeHtml(g)}</option>`).join("");
    // Populate squad team selector
    const squadSelect = document.getElementById("wc-squad-team");
    squadSelect.innerHTML = teams.map((tm) => `<option value="${escapeAttr(tm)}">${escapeHtml(tm)}</option>`).join("");
    squadSelect.value = "Argentina";
    appState.wcSquadTeam = "Argentina";
    // Populate compare selectors
    const selA = document.getElementById("wc-compare-a");
    const selB = document.getElementById("wc-compare-b");
    selA.innerHTML = teams.map((tm) => `<option value="${escapeAttr(tm)}">${escapeHtml(tm)}</option>`).join("");
    selB.innerHTML = teams.map((tm) => `<option value="${escapeAttr(tm)}">${escapeHtml(tm)}</option>`).join("");
    selA.value = "Argentina";
    selB.value = "France";
    appState.wcCompareA = "Argentina";
    appState.wcCompareB = "France";

    // Fetch API data in background, then re-render
    const [groupsData, scheduleData, predictionsData, teamsData] = await Promise.all([
        fetchWcGroups(),
        fetchWcSchedule(),
        fetchWcPredictions(),
        fetchWcTeams(),
    ]);

    // Pre-fetch squads for the initially selected teams
    await Promise.all([
        fetchWcSquad("Argentina"),
        fetchWcSquad("France"),
        fetchWcMatchPrediction("Argentina", "France"),
    ]);

    // Re-render all WC views with API data
    renderWcSchedule();
    renderWcSquads();
    renderWcCompare();
    renderWcProbability();

    // Update WC data status pills based on API availability
    document.querySelectorAll(".wc-data-status").forEach((el) => {
        if (wcApiData.apiOnline) {
            el.textContent = "LIVE DATA";
            el.className = "status-pill status-high wc-data-status";
            el.style.fontSize = "0.65rem";
        } else if (usingStaticData) {
            el.textContent = "STATIC";
            el.className = "status-pill status-medium wc-data-status";
            el.style.fontSize = "0.65rem";
        } else {
            el.textContent = "API OFFLINE";
            el.className = "status-pill status-low wc-data-status";
            el.style.fontSize = "0.65rem";
        }
    });
}

/* ── Tactical Board ─────────────────────────────────────────────────── */

let tacticalProject = null;
let _tacticalAutoSaveTimer = null;
function tacticalAutoSave() {
    clearTimeout(_tacticalAutoSaveTimer);
    _tacticalAutoSaveTimer = setTimeout(() => {
        if (tacticalProject && typeof TACTICAL_BOARD !== "undefined") {
            TACTICAL_BOARD.saveProject(tacticalProject);
        }
    }, 2000);
}

function syncObjectPropertyUI(obj) {
    const pathTypeEl = document.getElementById("tactical-path-type");
    const easingEl = document.getElementById("tactical-easing");
    const delayEl = document.getElementById("tactical-obj-delay");
    const pauseEl = document.getElementById("tactical-obj-pause");
    const addPathBtn = document.getElementById("tactical-add-path-point");

    if (obj && (obj.type === "player" || obj.type === "ball")) {
        if (pathTypeEl) pathTypeEl.value = obj.pathType || "linear";
        if (easingEl) easingEl.value = obj.easing || "linear";
        if (delayEl) delayEl.value = obj.delay_ms || 0;
        if (pauseEl) pauseEl.value = obj.pause_ms || 0;
        if (addPathBtn) {
            addPathBtn.textContent = "+ 路径点";
            addPathBtn.classList.remove("active");
        }
        // Exit path edit mode on new selection
        if (typeof TacticalRenderer !== "undefined") {
            TacticalRenderer.setPathEditMode(false, null);
        }
    } else {
        if (pathTypeEl) pathTypeEl.value = "linear";
        if (easingEl) easingEl.value = "linear";
        if (delayEl) delayEl.value = 0;
        if (pauseEl) pauseEl.value = 0;
    }
}

function renderTactical() {
    if (!tacticalProject) {
        tacticalProject = TACTICAL_BOARD.createProject("ScoutFootball 战术板");
        // Load default formation
        tacticalProject.objects = TACTICAL_BOARD.generateFormation("4-3-3", "home");
    }

    if (typeof TacticalRenderer !== "undefined") {
        TacticalRenderer.init("tactical-canvas", tacticalProject);
        TacticalRenderer.onChange = tacticalAutoSave;
        TacticalRenderer.onSelectionChange = (obj) => syncObjectPropertyUI(obj);
    }

    // Sync pitch type selector with current project
    const pitchTypeEl = document.getElementById("tactical-pitch-type");
    if (pitchTypeEl && tacticalProject.pitch_type) {
        pitchTypeEl.value = tacticalProject.pitch_type;
    }

    // Sync display mode selector
    const displayModeEl = document.getElementById("tactical-display-mode");
    if (displayModeEl) {
        displayModeEl.value = tacticalProject.displayMode || "single";
    }

    // Sync animation mode selector
    const animModeEl = document.getElementById("tactical-animation-mode");
    if (animModeEl) {
        animModeEl.value = tacticalProject.animationMode || "timing";
        const stepLabel = document.getElementById("tactical-step-duration-label");
        if (stepLabel) {
            stepLabel.style.display = (tacticalProject.animationMode === "step") ? "flex" : "none";
        }
    }
    const stepDurEl = document.getElementById("tactical-step-duration");
    if (stepDurEl) {
        stepDurEl.value = tacticalProject.stepDuration || 1000;
        const stepVal = document.getElementById("tactical-step-duration-value");
        if (stepVal) stepVal.textContent = (tacticalProject.stepDuration || 1000) + "ms";
    }

    // Update project list
    renderTacticalProjectList();

    // Update coaching notes panel for current frame
    updateCoachingNotesPanel();
}

function updateCoachingNotesPanel() {
    const notesEl = document.getElementById("tactical-coaching-notes");
    if (!notesEl) return;
    if (typeof TacticalRenderer !== "undefined") {
        notesEl.value = TacticalRenderer.getCurrentFrameNotes();
    }
}

function createPrematchPlan() {
    if (typeof TACTICAL_BOARD === "undefined") return;
    const match = selectedMatch();
    if (!match) return;

    // Create new tactical project
    const project = TACTICAL_BOARD.createProject(match.home + " vs " + match.away + " pre-match");
    project.pitch_type = "11v11";

    // Load home team formation (default 4-3-3)
    const homeObjs = TACTICAL_BOARD.generateFormation("4-3-3", "home");
    // Load away team formation (mirrored)
    const awayObjs = TACTICAL_BOARD.generateFormation("4-3-3", "away");
    project.objects = [...homeObjs, ...awayObjs];

    // Add prediction metadata as frame notes
    const modelType = (typeof predictionMeta !== "undefined" && predictionMeta.model_type) || "Poisson";
    const coverage = (typeof predictionMeta !== "undefined" && predictionMeta.num_teams)
        ? predictionMeta.num_teams + " teams"
        : "artifact pending";
    const hwPct = Math.round((match.hw || 0) * 100);
    const drawPct = Math.round((match.draw || 0) * 100);
    const awPct = Math.round((match.aw || 0) * 100);

    let notes = match.home + " vs " + match.away + " Pre-Match Plan\n";
    notes += "Model: " + modelType + " | Coverage: " + coverage + "\n";
    notes += "\n- Home win: " + hwPct + "% | Draw: " + drawPct + "% | Away win: " + awPct + "%";
    notes += "\n- Expected goals: " + (match.xh || 0).toFixed(2) + " / " + (match.xa || 0).toFixed(2);
    notes += "\n- Edit formations to plan your tactical approach";

    if (project.frames && project.frames[0]) {
        project.frames[0].notes = notes;
    }

    // Coaching points for the default formation
    const cp = TACTICAL_BOARD.getFormationCoachingPoints("4-3-3");
    if (cp) {
        const cpNotes = TACTICAL_BOARD.formatCoachingNotes(cp);
        if (project.frames && project.frames[0]) {
            project.frames[0].notes = notes + "\n\n--- Coaching Points ---\n" + cpNotes;
        }
    }

    // Save and switch to tactical view
    TACTICAL_BOARD.saveProject(project);
    tacticalProject = project;
    setView("tactical");
}

function createWcTeamTemplate() {
    if (typeof TACTICAL_BOARD === "undefined") return;
    const team = appState.wcSquadTeam;
    if (!team) return;

    const rawSquad = wcGetSquad(team);
    const squad = matchSquadWithRatings(rawSquad);

    // Create project
    const project = TACTICAL_BOARD.createProject(team + " World Cup template");
    project.pitch_type = "11v11";

    // Default formation: 4-3-3
    const formationName = "4-3-3";
    const formation = TACTICAL_BOARD.FORMATIONS[formationName];
    if (!formation) return;

    // Build position list from formation
    const positionRoles = [
        { role: "GK", items: formation.GK || [] },
        { role: "CB", items: formation.CB || [] },
        { role: "FB", items: formation.FB || [] },
        { role: "DM", items: formation.DM || [] },
        { role: "CM", items: formation.CM || [] },
        { role: "AM", items: formation.AM || [] },
        { role: "W",  items: formation.W || [] },
        { role: "ST", items: formation.ST || [] },
    ];

    // Assign players from squad to positions
    const objects = [];
    let squadIdx = 0;
    let num = 1;
    for (const { role, items } of positionRoles) {
        for (const pos of items) {
            const player = squadIdx < squad.length ? squad[squadIdx] : null;
            const label = player ? player.name : "";
            objects.push(TACTICAL_BOARD.createPlayer(pos.x, pos.y, "home", label, num));
            squadIdx++;
            num++;
        }
    }

    // Add ball at center
    objects.push(TACTICAL_BOARD.createBall(50, 50));
    project.objects = objects;

    // Add coaching notes with squad info
    const rated = squad.filter(p => p.hasRating);
    const avgRating = rated.length > 0
        ? (rated.reduce((s, p) => s + p.rating, 0) / rated.length).toFixed(2)
        : "N/A";

    let notes = team + " World Cup Template\n";
    notes += "Formation: " + formationName + " | Squad: " + squad.length + " players\n";
    notes += "Rated: " + rated.length + " | Avg rating: " + avgRating + "\n";
    notes += "\n- Players assigned to formation positions from squad list";
    notes += "\n- Edit player names and positions as needed";
    notes += "\n- Add additional frames for set-piece plans";

    if (project.frames && project.frames[0]) {
        project.frames[0].notes = notes;
    }

    // Add formation coaching points
    const cp = TACTICAL_BOARD.getFormationCoachingPoints(formationName);
    if (cp && project.frames && project.frames[0]) {
        project.frames[0].notes += "\n\n--- Coaching Points ---\n" + TACTICAL_BOARD.formatCoachingNotes(cp);
    }

    TACTICAL_BOARD.saveProject(project);
    tacticalProject = project;
    setView("tactical");
}

function renderTacticalProjectList() {
    const list = document.getElementById("tactical-project-list");
    if (!list) return;

    const projects = TACTICAL_BOARD.listProjects();
    list.innerHTML = projects.length > 0
        ? projects.map((p) => `
            <div class="rank-item" style="cursor:pointer;display:flex;align-items:center;justify-content:space-between" data-board-id="${escapeAttr(p.board_id)}">
                <div>
                    <span class="tactical-project-title" data-board-id="${escapeAttr(p.board_id)}">${escapeHtml(p.title || "Untitled")}</span>
                    <span class="rank-meta">${escapeHtml(p.updated_at ? new Date(p.updated_at).toLocaleDateString() : "")}</span>
                </div>
                <button class="text-button" data-delete-board="${escapeAttr(p.board_id)}" title="Delete project" style="color:var(--danger,#e74c3c);font-size:0.85rem;padding:0.2rem 0.4rem">✕</button>
            </div>
        `).join("")
        : '<div style="color:var(--text-muted);text-align:center;padding:1rem">No saved projects</div>';

    // Click to load
    list.querySelectorAll("[data-board-id]").forEach((el) => {
        if (!el.classList.contains("tactical-project-title")) {
            el.addEventListener("click", () => {
                const loaded = TACTICAL_BOARD.loadProject(el.dataset.boardId);
                if (loaded) {
                    tacticalProject = loaded;
                    renderTactical();
                }
            });
        }
    });

    // Double-click to rename project title
    list.querySelectorAll(".tactical-project-title").forEach((titleSpan) => {
        titleSpan.addEventListener("dblclick", (e) => {
            e.stopPropagation();
            const boardId = titleSpan.dataset.boardId;
            const currentTitle = titleSpan.textContent;
            const input = document.createElement("input");
            input.type = "text";
            input.value = currentTitle;
            input.style.cssText = "font-size:inherit;font-weight:bold;width:100%;padding:0 0.15rem;border:1px solid var(--accent,#7ca8ff);border-radius:3px;background:var(--bg,#1a1a2e);color:var(--text,#e0e0e0)";
            titleSpan.replaceWith(input);
            input.focus();
            input.select();

            function commitRename() {
                const newTitle = input.value.trim() || currentTitle;
                const loaded = TACTICAL_BOARD.loadProject(boardId);
                if (loaded) {
                    TACTICAL_BOARD.renameProject(loaded, newTitle);
                    TACTICAL_BOARD.saveProject(loaded);
                    if (tacticalProject && tacticalProject.board_id === boardId) {
                        tacticalProject.title = loaded.title;
                        tacticalProject.updated_at = loaded.updated_at;
                    }
                }
                renderTacticalProjectList();
            }

            function cancelRename() {
                renderTacticalProjectList();
            }

            input.addEventListener("keydown", (ev) => {
                if (ev.key === "Enter") { ev.preventDefault(); commitRename(); }
                if (ev.key === "Escape") { ev.preventDefault(); cancelRename(); }
            });
            input.addEventListener("blur", commitRename);
        });
    });

    // Delete buttons
    list.querySelectorAll("[data-delete-board]").forEach((btn) => {
        btn.addEventListener("click", (e) => {
            e.stopPropagation();
            TACTICAL_BOARD.deleteProject(btn.dataset.deleteBoard);
            renderTacticalProjectList();
        });
    });
}

function renderTacticalFrameList() {
    const list = document.getElementById("tactical-frame-list");
    if (!list || !tacticalProject || !tacticalProject.frames) return;

    const currentFrame = (typeof TacticalRenderer !== "undefined")
        ? TacticalRenderer.animationState.currentFrame
        : 0;

    const frameCount = tacticalProject.frames.length;

    list.innerHTML = tacticalProject.frames.map((frame, i) => `
        <div class="rank-item" style="cursor:pointer;display:flex;align-items:center;justify-content:space-between;${i === currentFrame ? 'background:var(--glass-bg-hover)' : ''}" data-frame-index="${i}">
            <div>
                <strong>${escapeHtml(frame.name || `Frame ${i + 1}`)}</strong>
                <span class="rank-meta">${escapeHtml(frame.duration_ms || 3000)}ms · ${escapeHtml((frame.objects || []).length)} objects</span>
            </div>
            <div style="display:flex;align-items:center;gap:0.2rem">
                <button class="text-button" data-frame-up="${i}" title="Move frame earlier" style="font-size:0.85rem;padding:0.2rem 0.4rem;${i === 0 ? 'opacity:0.3;pointer-events:none' : ''}">\u25C0</button>
                <button class="text-button" data-frame-down="${i}" title="Move frame later" style="font-size:0.85rem;padding:0.2rem 0.4rem;${i === frameCount - 1 ? 'opacity:0.3;pointer-events:none' : ''}">\u25B6</button>
                <button class="text-button" data-delete-frame="${i}" title="Delete frame" style="color:var(--danger,#e74c3c);font-size:0.85rem;padding:0.2rem 0.4rem">\u2715</button>
            </div>
        </div>
    `).join("");

    list.querySelectorAll("[data-frame-index]").forEach((el) => {
        el.addEventListener("click", () => {
            const idx = parseInt(el.dataset.frameIndex, 10);
            if (typeof TacticalRenderer !== "undefined") {
                TacticalRenderer.goToFrame(idx);
                tacticalProject = TacticalRenderer.getProject();
                renderTacticalFrameList();
                updateCoachingNotesPanel();
            }
        });
    });

    // Frame up (move earlier)
    list.querySelectorAll("[data-frame-up]").forEach((btn) => {
        btn.addEventListener("click", (e) => {
            e.stopPropagation();
            const idx = parseInt(btn.dataset.frameUp, 10);
            if (idx <= 0 || !tacticalProject || !tacticalProject.frames) return;
            const tmp = tacticalProject.frames[idx - 1];
            tacticalProject.frames[idx - 1] = tacticalProject.frames[idx];
            tacticalProject.frames[idx] = tmp;
            TACTICAL_BOARD.saveProject(tacticalProject);
            renderTacticalFrameList();
        });
    });

    // Frame down (move later)
    list.querySelectorAll("[data-frame-down]").forEach((btn) => {
        btn.addEventListener("click", (e) => {
            e.stopPropagation();
            const idx = parseInt(btn.dataset.frameDown, 10);
            if (!tacticalProject || !tacticalProject.frames || idx >= tacticalProject.frames.length - 1) return;
            const tmp = tacticalProject.frames[idx + 1];
            tacticalProject.frames[idx + 1] = tacticalProject.frames[idx];
            tacticalProject.frames[idx] = tmp;
            TACTICAL_BOARD.saveProject(tacticalProject);
            renderTacticalFrameList();
        });
    });

    // Delete frame buttons
    list.querySelectorAll("[data-delete-frame]").forEach((btn) => {
        btn.addEventListener("click", (e) => {
            e.stopPropagation();
            const idx = parseInt(btn.dataset.deleteFrame, 10);
            if (tacticalProject && typeof TacticalRenderer !== "undefined") {
                TACTICAL_BOARD.removeFrame(tacticalProject, idx);
                tacticalProject = TacticalRenderer.getProject();
                renderTacticalFrameList();
            }
        });
    });
}

document.addEventListener("DOMContentLoaded", async () => {
    // Restore theme preference
    const savedTheme = localStorage.getItem("sf-theme");
    if (savedTheme === "dark" || (!savedTheme && window.matchMedia("(prefers-color-scheme: dark)").matches)) {
        document.body.classList.add("dark-mode");
        document.getElementById("theme-toggle").textContent = "☾";
    }
    applyLocale();
    renderMatchSelectors();
    // Start WC init early — it runs in parallel with other API calls
    const wcInitPromise = initWorldCup();
    bindEvents();
    setView("overview");

    // Load scouting localStorage state
    if (typeof SCOUTING_WORKSPACE !== "undefined") ensureScoutingWorkspaceMeta();
    loadScoutQueueStatuses();
    loadScoutShortlistNotes();
    loadWatchlistNotes();

    // Load real data from API in parallel
    const [ratingsData, meta, artifacts, teams, valueData, reviewData, predictionArtifact, predictionCalibrationData, runs, watchlistRows, shortlistRows, actionValues, licenseResp] = await Promise.all([
        fetchRatings(),
        fetchRatingsMeta(),
        fetchArtifacts(),
        fetchTeams(),
        fetchValueReport(),
        fetchReviewQueue(),
        fetchPredictionMeta(),
        fetchPredictionCalibration(),
        fetchModelRuns(),
        fetchWatchlist(),
        fetchShortlist(),
        fetchActionValues(),
        fetchLicense(),
    ]);

    players = ratingsData;
    ratingsMeta = meta;
    artifactSummary = artifacts;
    valuePlayers = valueData;
    reviewQueue = reviewData;
    predictionMeta = predictionArtifact;
    predictionCalibration = predictionCalibrationData;
    modelRuns = runs;
    watchlistData = watchlistRows;
    shortlistData = shortlistRows;
    actionValueSummary = actionValues;
    licenseData = licenseResp;
    if (players.length > 0) {
        appState.selectedPlayerKey = players[0].key;
    }

    // Populate season filter dropdown
    const seasons = [...new Set(players.map((p) => p.season).filter(Boolean))].sort();
    const seasonSelect = document.getElementById("season-filter");
    seasonSelect.innerHTML = '<option value="ALL">ALL</option>' + seasons.map((s) => `<option value="${escapeAttr(s)}">${escapeHtml(s)}</option>`).join("");
    seasonSelect.value = appState.season;

    // Populate league filter dropdown
    const leagues = [...new Set(players.map((p) => p.league).filter(Boolean))].sort();
    const leagueSelect = document.getElementById("league-filter");
    leagueSelect.innerHTML = '<option value="ALL">ALL</option>' + leagues.map((l) => `<option value="${escapeAttr(l)}">${escapeHtml(l)}</option>`).join("");
    leagueSelect.value = appState.league;

    // Update team list for match prediction
    teamList = teams;
    if (teamList.length > 0) {
        appState.home = teamList[0];
        appState.away = teamList.length > 1 ? teamList[1] : teamList[0];
    }
    renderMatchSelectors();

    // Update overview metrics from artifacts API
    const metricValues = document.querySelectorAll(".coverage-strip .metric-value");
    if (metricValues[0]) metricValues[0].textContent = (artifacts.player_match_rows || 0).toLocaleString();
    if (metricValues[1]) metricValues[1].textContent = (artifacts.team_match_rows || 0).toLocaleString();
    if (metricValues[2]) metricValues[2].textContent = (artifacts.rating_rows || 0).toLocaleString();
    if (metricValues[3]) metricValues[3].textContent = (artifacts.event_samples || 0).toLocaleString();

    // Update data health
    const health = artifacts.data_health || {};
    const healthItems = document.querySelectorAll("#data-health-list .health-item");
    if (healthItems.length >= 3) {
        healthItems[0].querySelector(".status-pill").className = `status-pill ${health.oof_available ? "status-high" : "status-low"}`;
        healthItems[0].querySelector(".status-pill").textContent = health.oof_available ? "HIGH" : "LOW";
        healthItems[1].querySelector(".status-pill").className = `status-pill ${health.player_match_coverage ? "status-medium" : "status-low"}`;
        healthItems[1].querySelector(".status-pill").textContent = health.player_match_coverage ? "MED" : "LOW";
        healthItems[2].querySelector(".status-pill").className = `status-pill ${health.truth_labels_available ? "status-high" : "status-low"}`;
        healthItems[2].querySelector(".status-pill").textContent = health.truth_labels_available ? "HIGH" : "LOW";
    }

    const topCoveragePill = document.getElementById("top-coverage-pill");
    if (topCoveragePill) {
        topCoveragePill.textContent = health.player_match_coverage || artifacts.data_source_label || "local parquet";
        topCoveragePill.className = `status-pill ${health.player_match_coverage ? "status-medium" : "status-low"}`;
    }
    const topOofPill = document.getElementById("top-oof-pill");
    if (topOofPill) {
        const valueIsDemo = valueSummaryMeta.status === "demo";
        topOofPill.textContent = valueIsDemo
            ? `DEMO ${valueSummaryMeta.sample_count || 0}`
            : (valueSummaryMeta.sample_count ? `OOF ${valueSummaryMeta.sample_count}` : "OOF none");
        topOofPill.className = `status-pill ${valueIsDemo ? "status-medium" : (valueSummaryMeta.sample_count ? "status-high" : "status-low")}`;
    }

    renderActiveView();

    // Check API connection status (initial + periodic polling)
    const apiPill = document.getElementById("top-api-pill");
    function syncApiOfflineBanner() {
        const existingBanner = document.getElementById("global-demo-banner");
        if (apiOnline !== false || window.__SCOUTFOOTBALL_DESKTOP__) {
            if (existingBanner) existingBanner.remove();
            return;
        }

        if (existingBanner) return;
        const demoBanner = document.createElement("div");
        demoBanner.id = "global-demo-banner";
        demoBanner.style.cssText = "position:fixed;top:0;left:0;right:0;z-index:9999;padding:0.3rem 1rem;background:rgba(255,107,107,0.15);color:#ff6b6b;font-size:0.72rem;text-align:center;border-bottom:1px solid rgba(255,107,107,0.3)";
        const z = appState.lang === "zh";
        demoBanner.textContent = z
            ? "◆ API 离线 — 使用静态缓存数据。启动后端获取实时数据：PYTHONPATH=src uv run python -m scoutfootball serve"
            : "◆ API Offline — Using cached static data. Start backend for live data: PYTHONPATH=src uv run python -m scoutfootball serve";
        document.body.prepend(demoBanner);
    }

    function checkApiStatus() {
        if (!apiPill) return;
        fetch(`${API_BASE}/health`, { signal: AbortSignal.timeout(3000) })
            .then((resp) => {
                if (resp.ok) {
                    apiPill.textContent = "API OK";
                    apiPill.className = "status-pill status-high";
                    apiOnline = true;
                    usingStaticData = false;
                } else {
                    apiPill.textContent = "API ERR";
                    apiPill.className = "status-pill status-low";
                    apiOnline = false;
                }
                syncApiOfflineBanner();
            })
            .catch(() => {
                apiPill.textContent = usingStaticData ? "STATIC" : "OFFLINE";
                apiPill.className = "status-pill status-medium";
                apiOnline = false;
                syncApiOfflineBanner();
            });
    }
    checkApiStatus();
    // Poll every 10s so backend coming online is detected automatically
    setInterval(checkApiStatus, 10000);

    // Initialize World Cup — already started in parallel above, just await completion
    await wcInitPromise;
});

const SCOUT_QUEUE_KEY = "scout-queue-statuses";
const SCOUT_NOTES_KEY = "scout-shortlist-notes";
const SCOUT_LASTVISIT_KEY = "scout-watchlist-lastvisit";
const SCOUT_SNAPSHOT_KEY = "scout-watchlist-snapshot";
const SCOUT_WORKSPACE_META_KEY = "sf-scouting-workspace-meta";
const WATCHLIST_NOTES_KEY = "sf-watchlist-notes";
const PLAYER_WATCHLIST_KEY = "sf-player-watchlist";
const PLAYER_SHORTLIST_KEY = "sf-player-shortlist";
const STATUS_CYCLE = ["pending", "reviewing", "approved", "rejected"];
const STATUS_ICONS = { pending: "\u25CB", reviewing: "\u25B2", approved: "\u2713", rejected: "\u2717" };

let scoutQueueStatuses = {};
let scoutShortlistNotes = {};
let watchlistNotes = {};
let scoutSortMode = "priority";
let watchlistDiffCount = 0;
const SCOUT_PAGE_SIZE = 50;
let scoutCurrentPage = 1;
let pendingScoutingWorkspaceImport = null;
let lastScoutingTouchAt = 0;

function newScoutingWorkspaceId() {
    if (globalThis.crypto && typeof globalThis.crypto.randomUUID === "function") {
        return globalThis.crypto.randomUUID();
    }
    return `workspace-${Date.now().toString(36)}-${Math.random().toString(36).slice(2, 10)}`;
}

function ensureScoutingWorkspaceMeta() {
    const now = new Date().toISOString();
    let stored = {};
    try {
        stored = JSON.parse(localStorage.getItem(SCOUT_WORKSPACE_META_KEY)) || {};
    } catch {
        stored = {};
    }
    const workspace = SCOUTING_WORKSPACE.createWorkspace({
        workspace_id: stored.workspace_id || newScoutingWorkspaceId(),
        created_at: stored.created_at || now,
        updated_at: stored.updated_at || now,
        exported_at: now,
        revision: stored.revision || 1,
        last_action: stored.last_action || "local-edit",
        imported_from: stored.imported_from || "",
        app_version: APP_VERSION,
    });
    const meta = workspace.audit;
    try {
        localStorage.setItem(SCOUT_WORKSPACE_META_KEY, JSON.stringify(meta));
    } catch {}
    return meta;
}

function touchScoutingWorkspace(lastAction = "local-edit") {
    const current = ensureScoutingWorkspaceMeta();
    const now = new Date().toISOString();
    const nowMs = Date.now();
    const coalescedEdit =
        lastAction === "local-edit"
        && lastScoutingTouchAt > 0
        && nowMs - lastScoutingTouchAt < 750;
    lastScoutingTouchAt = nowMs;
    const next = SCOUTING_WORKSPACE.createWorkspace({
        workspace_id: current.workspace_id,
        created_at: current.created_at,
        updated_at: now,
        exported_at: now,
        revision: Math.min(
            current.revision + (coalescedEdit ? 0 : 1),
            Number.MAX_SAFE_INTEGER,
        ),
        last_action: lastAction,
        imported_from: current.imported_from,
        app_version: APP_VERSION,
    }).audit;
    try {
        localStorage.setItem(SCOUT_WORKSPACE_META_KEY, JSON.stringify(next));
    } catch {}
    renderScoutingWorkspaceStatus();
    return next;
}

function currentSnapshotState() {
    let playerKeys = [];
    let savedAt = null;
    try {
        playerKeys = JSON.parse(localStorage.getItem(SCOUT_SNAPSHOT_KEY)) || [];
        const timestamp = Number(localStorage.getItem(SCOUT_LASTVISIT_KEY) || 0);
        savedAt = timestamp > 0 ? new Date(timestamp).toISOString() : null;
    } catch {
        playerKeys = [];
    }
    return { playerKeys, savedAt };
}

function buildCurrentScoutingWorkspace() {
    const meta = ensureScoutingWorkspaceMeta();
    const snapshot = currentSnapshotState();
    const ratingSnapshotIds = reviewQueue
        .map((player) => player.rating_snapshot_id)
        .filter(Boolean);
    return SCOUTING_WORKSPACE.createWorkspace({
        workspace_id: meta.workspace_id,
        created_at: meta.created_at,
        updated_at: meta.updated_at,
        exported_at: new Date().toISOString(),
        revision: meta.revision,
        last_action: meta.last_action,
        imported_from: meta.imported_from,
        app_version: APP_VERSION,
        rating_snapshot_ids: ratingSnapshotIds,
        review_statuses: scoutQueueStatuses,
        shortlist_notes: scoutShortlistNotes,
        watchlist_notes: watchlistNotes,
        watchlist: getPlayerWatchlist(),
        shortlist: getPlayerShortlist(),
        snapshot_player_keys: snapshot.playerKeys,
        snapshot_saved_at: snapshot.savedAt,
    });
}

function renderScoutingWorkspaceStatus() {
    const status = document.getElementById("scout-workspace-status");
    if (!status || typeof SCOUTING_WORKSPACE === "undefined") return;
    const workspace = buildCurrentScoutingWorkspace();
    const summary = SCOUTING_WORKSPACE.summarizeWorkspace(workspace);
    const locale = appState.lang === "zh" ? "zh-CN" : "en-US";
    const updated = new Date(summary.updated_at).toLocaleString(locale);
    const scope = appState.lang === "zh" ? "仅当前浏览器" : "this browser only";
    const label = document.createElement("strong");
    label.textContent = `Workspace v${SCOUTING_WORKSPACE.VERSION}`;
    status.replaceChildren(
        label,
        document.createTextNode(
            ` · rev ${summary.revision} · ${summary.decision_count} ${appState.lang === "zh" ? "项决策" : "decisions"} · ${updated} · ${scope}`,
        ),
    );
}

function setScoutingWorkspaceMessage(message, isError = false) {
    const status = document.getElementById("scout-snapshot-status");
    if (!status) return;
    status.textContent = message;
    status.style.color = isError ? "var(--bad)" : "var(--good)";
    setTimeout(() => {
        status.style.color = "";
        updateSnapshotStatus();
    }, 3500);
}

function workspaceErrorMessage(error) {
    const code = String(error && error.message ? error.message : error);
    const zh = appState.lang === "zh";
    const messages = {
        workspace_too_large: zh ? "工作区文件超过 1 MB 限制" : "Workspace exceeds the 1 MB limit",
        workspace_json_invalid: zh ? "工作区不是有效 JSON" : "Workspace is not valid JSON",
        workspace_not_object: zh ? "工作区根节点必须是对象" : "Workspace root must be an object",
        workspace_schema_invalid: zh ? "工作区 schema 不匹配" : "Workspace schema does not match",
        workspace_version_unsupported: zh ? "不支持该工作区版本" : "Workspace version is unsupported",
    };
    return messages[code] || (zh ? `导入失败：${code}` : `Import failed: ${code}`);
}

function exportScoutingWorkspace() {
    if (typeof SCOUTING_WORKSPACE === "undefined") {
        setScoutingWorkspaceMessage(
            appState.lang === "zh" ? "工作区模块未加载" : "Workspace module is unavailable",
            true,
        );
        return;
    }
    touchScoutingWorkspace("manual-export");
    const workspace = buildCurrentScoutingWorkspace();
    const blob = new Blob([SCOUTING_WORKSPACE.serializeWorkspace(workspace)], {
        type: "application/json;charset=utf-8",
    });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    const stamp = new Date().toISOString().replace(/[:.]/g, "-");
    link.href = url;
    link.download = `scoutfootball-scouting-workspace-${stamp}.json`;
    document.body.appendChild(link);
    link.click();
    link.remove();
    setTimeout(() => URL.revokeObjectURL(url), 0);
    setScoutingWorkspaceMessage(
        appState.lang === "zh" ? "工作区已导出" : "Workspace exported",
    );
}

function workspaceSummaryCard(title, summary) {
    const locale = appState.lang === "zh" ? "zh-CN" : "en-US";
    const updated = new Date(summary.updated_at).toLocaleString(locale);
    return `<div class="workspace-preview-card">
        <div><strong>${escapeHtml(title)}</strong><div class="rank-meta">rev ${summary.revision} · ${escapeHtml(updated)}</div></div>
        <div class="workspace-preview-metrics">
            <span><b>${summary.status_count}</b>${escapeHtml(appState.lang === "zh" ? "状态" : "statuses")}</span>
            <span><b>${summary.note_count}</b>${escapeHtml(appState.lang === "zh" ? "备注" : "notes")}</span>
            <span><b>${summary.watchlist_count + summary.shortlist_count}</b>${escapeHtml(appState.lang === "zh" ? "选择" : "selections")}</span>
        </div>
    </div>`;
}

async function previewScoutingWorkspaceImport(file) {
    try {
        if (file.size > SCOUTING_WORKSPACE.MAX_BYTES) throw new Error("workspace_too_large");
        const incoming = SCOUTING_WORKSPACE.parseWorkspace(await file.text());
        const local = buildCurrentScoutingWorkspace();
        const analysis = SCOUTING_WORKSPACE.analyzeConflict(local, incoming);
        pendingScoutingWorkspaceImport = { incoming, local, analysis };
        const preview = document.getElementById("scout-workspace-preview");
        const dialog = document.getElementById("scout-workspace-dialog");
        if (!preview || !dialog) throw new Error("workspace_dialog_unavailable");
        const conflictText = analysis.total_conflicts > 0
            ? (appState.lang === "zh"
                ? `检测到 ${analysis.status_conflicts} 个状态冲突和 ${analysis.note_conflicts} 个备注冲突。安全合并会保留两边条目，并以更新时间较新的工作区解决同键冲突。`
                : `Found ${analysis.status_conflicts} status conflicts and ${analysis.note_conflicts} note conflicts. Safe merge keeps entries from both sides and uses the newer workspace for same-key conflicts.`)
            : (appState.lang === "zh"
                ? "未检测到同键冲突。仍会先预览，不会自动覆盖当前浏览器状态。"
                : "No same-key conflicts detected. The import is still previewed and never overwrites browser state automatically.");
        preview.innerHTML = `<div class="workspace-preview-grid">
            ${workspaceSummaryCard(appState.lang === "zh" ? "当前浏览器" : "Current browser", analysis.local)}
            ${workspaceSummaryCard(file.name || (appState.lang === "zh" ? "导入文件" : "Import file"), analysis.incoming)}
        </div><p class="workspace-conflict-note">${escapeHtml(conflictText)}</p>`;
        if (typeof dialog.showModal === "function") dialog.showModal();
        else dialog.setAttribute("open", "");
    } catch (error) {
        pendingScoutingWorkspaceImport = null;
        setScoutingWorkspaceMessage(workspaceErrorMessage(error), true);
    }
}

function replaceWorkspaceAudit(incoming) {
    const state = SCOUTING_WORKSPACE.toLocalState(incoming);
    const now = new Date().toISOString();
    return SCOUTING_WORKSPACE.createWorkspace({
        workspace_id: state.audit.workspace_id,
        created_at: state.audit.created_at,
        updated_at: now,
        exported_at: now,
        revision: state.audit.revision + 1,
        last_action: "import-replace",
        imported_from: state.audit.workspace_id,
        app_version: APP_VERSION,
        rating_snapshot_ids: incoming.source.rating_snapshot_ids,
        review_statuses: state.review_statuses,
        shortlist_notes: state.shortlist_notes,
        watchlist_notes: state.watchlist_notes,
        watchlist: state.watchlist,
        shortlist: state.shortlist,
        snapshot_player_keys: state.snapshot_player_keys,
        snapshot_saved_at: state.snapshot_saved_at,
    });
}

function persistScoutingWorkspace(workspace) {
    const state = SCOUTING_WORKSPACE.toLocalState(workspace);
    const keys = [
        SCOUT_QUEUE_KEY,
        SCOUT_NOTES_KEY,
        WATCHLIST_NOTES_KEY,
        PLAYER_WATCHLIST_KEY,
        PLAYER_SHORTLIST_KEY,
        SCOUT_SNAPSHOT_KEY,
        SCOUT_LASTVISIT_KEY,
        SCOUT_WORKSPACE_META_KEY,
    ];
    const backup = new Map(keys.map((key) => [key, localStorage.getItem(key)]));
    try {
        localStorage.setItem(SCOUT_QUEUE_KEY, JSON.stringify(state.review_statuses));
        localStorage.setItem(SCOUT_NOTES_KEY, JSON.stringify(state.shortlist_notes));
        localStorage.setItem(WATCHLIST_NOTES_KEY, JSON.stringify(state.watchlist_notes));
        localStorage.setItem(PLAYER_WATCHLIST_KEY, JSON.stringify(state.watchlist));
        localStorage.setItem(PLAYER_SHORTLIST_KEY, JSON.stringify(state.shortlist));
        localStorage.setItem(SCOUT_SNAPSHOT_KEY, JSON.stringify(state.snapshot_player_keys));
        const savedAt = Date.parse(state.snapshot_saved_at);
        if (Number.isFinite(savedAt)) localStorage.setItem(SCOUT_LASTVISIT_KEY, String(savedAt));
        else localStorage.removeItem(SCOUT_LASTVISIT_KEY);
        localStorage.setItem(SCOUT_WORKSPACE_META_KEY, JSON.stringify(state.audit));
    } catch (error) {
        for (const [key, value] of backup) {
            if (value === null) localStorage.removeItem(key);
            else localStorage.setItem(key, value);
        }
        throw error;
    }
    loadScoutQueueStatuses();
    loadScoutShortlistNotes();
    loadWatchlistNotes();
    lastScoutingTouchAt = 0;
}

function applyScoutingWorkspaceImport(mode) {
    if (!pendingScoutingWorkspaceImport) return;
    const { local, incoming } = pendingScoutingWorkspaceImport;
    try {
        const result = mode === "replace"
            ? replaceWorkspaceAudit(incoming)
            : SCOUTING_WORKSPACE.mergeWorkspaces(local, incoming);
        persistScoutingWorkspace(result);
        pendingScoutingWorkspaceImport = null;
        const dialog = document.getElementById("scout-workspace-dialog");
        if (dialog) dialog.close();
        scoutCurrentPage = 1;
        renderScouting();
        setScoutingWorkspaceMessage(
            appState.lang === "zh"
                ? (mode === "replace" ? "已替换本地工作区" : "工作区已安全合并")
                : (mode === "replace" ? "Local workspace replaced" : "Workspace safely merged"),
        );
    } catch (error) {
        setScoutingWorkspaceMessage(workspaceErrorMessage(error), true);
    }
}

/* ── Player Watchlist / Shortlist (localStorage) ─────────────────── */
function getPlayerWatchlist() {
    try { return JSON.parse(localStorage.getItem(PLAYER_WATCHLIST_KEY)) || []; } catch { return []; }
}
function savePlayerWatchlist(list) {
    try {
        localStorage.setItem(PLAYER_WATCHLIST_KEY, JSON.stringify(list));
        touchScoutingWorkspace();
    } catch {}
}
function getPlayerShortlist() {
    try { return JSON.parse(localStorage.getItem(PLAYER_SHORTLIST_KEY)) || []; } catch { return []; }
}
function savePlayerShortlist(list) {
    try {
        localStorage.setItem(PLAYER_SHORTLIST_KEY, JSON.stringify(list));
        touchScoutingWorkspace();
    } catch {}
}
function isInPlayerWatchlist(playerKey) {
    return getPlayerWatchlist().some((p) => p.key === playerKey);
}
function isInPlayerShortlist(playerKey) {
    return getPlayerShortlist().some((p) => p.key === playerKey);
}
function togglePlayerWatchlist(player) {
    const list = getPlayerWatchlist();
    const idx = list.findIndex((p) => p.key === player.key);
    if (idx >= 0) {
        list.splice(idx, 1);
    } else {
        list.push({ key: player.key, name: player.name, team: player.team, position: player.position, rating: player.rating });
    }
    savePlayerWatchlist(list);
    return idx < 0; // true if added
}
function togglePlayerShortlist(player) {
    const list = getPlayerShortlist();
    const idx = list.findIndex((p) => p.key === player.key);
    if (idx >= 0) {
        list.splice(idx, 1);
    } else {
        list.push({ key: player.key, name: player.name, team: player.team, position: player.position, rating: player.rating });
    }
    savePlayerShortlist(list);
    return idx < 0;
}
function sendToTacticalBoard(player) {
    if (!tacticalProject) {
        tacticalProject = typeof TACTICAL_BOARD !== "undefined"
            ? TACTICAL_BOARD.createProject("ScoutFootball \u6218\u672f\u677f")
            : { title: "ScoutFootball \u6218\u672f\u677f", objects: [] };
    }
    // Add player marker to tactical project
    const marker = {
        type: "player_marker",
        id: "pm_" + Date.now(),
        label: player.name,
        position: player.position,
        rating: player.rating,
        team: player.team,
        x: 50 + Math.random() * 30 - 15,
        y: 50 + Math.random() * 30 - 15,
    };
    if (!tacticalProject.objects) tacticalProject.objects = [];
    tacticalProject.objects.push(marker);
    if (typeof TACTICAL_BOARD !== "undefined" && TACTICAL_BOARD.saveProject) {
        TACTICAL_BOARD.saveProject(tacticalProject);
    }
    setView("tactical");
}

function loadScoutQueueStatuses() {
    try { scoutQueueStatuses = JSON.parse(localStorage.getItem(SCOUT_QUEUE_KEY)) || {}; } catch { scoutQueueStatuses = {}; }
}

function saveScoutQueueStatuses() {
    try {
        localStorage.setItem(SCOUT_QUEUE_KEY, JSON.stringify(scoutQueueStatuses));
        touchScoutingWorkspace();
    } catch {}
}

function loadScoutShortlistNotes() {
    try { scoutShortlistNotes = JSON.parse(localStorage.getItem(SCOUT_NOTES_KEY)) || {}; } catch { scoutShortlistNotes = {}; }
}

function saveScoutShortlistNotes() {
    try {
        localStorage.setItem(SCOUT_NOTES_KEY, JSON.stringify(scoutShortlistNotes));
        touchScoutingWorkspace();
    } catch {}
}
function loadWatchlistNotes() {
    try { watchlistNotes = JSON.parse(localStorage.getItem(WATCHLIST_NOTES_KEY)) || {}; } catch { watchlistNotes = {}; }
}

function saveWatchlistNotes() {
    try {
        localStorage.setItem(WATCHLIST_NOTES_KEY, JSON.stringify(watchlistNotes));
        touchScoutingWorkspace();
    } catch {}
}

function generateTacticalRole(player) {
    const pos = (player.position_group || player.position || "").toUpperCase();
    const score = Number(player.optimized_score || player.rating || 0);
    const minutes = Math.round(player.minutes || 0);
    const z = appState.lang === "zh";
    const roleMap = {
        GK: { zh: "门将 - 最后防线组织者", en: "Goalkeeper - Last line organizer" },
        CB: { zh: "中后卫 - 防线核心，负责拦截和出球", en: "Centre-Back - Defensive anchor, ball-playing defender" },
        FB: { zh: "边后卫 - 攻守转换枢纽，提供宽度", en: "Full-Back - Transition hub, provides width" },
        DM: { zh: "防守型中场 - 屏障型后腰，扫荡和分球", en: "Defensive Midfielder - Shield pivot, screen and distribute" },
        CM: { zh: "中场 - 节拍器型中场，串联攻守", en: "Central Midfielder - Tempo-setter, links attack and defense" },
        AM: { zh: "前腰 - 创造型10号位，关键传球和远射", en: "Attacking Midfielder - Creative No.10, key passes and long shots" },
        W: { zh: "边锋 - 突破型翼锋，内切或下底传中", en: "Winger - Dribbling flanker, cuts inside or delivers crosses" },
        ST: { zh: "前锋 - 终结者型中锋，禁区嗅觉", en: "Striker - Finisher centre-forward, box presence" },
    };
    const role = roleMap[pos] || { zh: "多功能球员", en: "Versatile player" };
    let tier = "";
    if (score >= 90) tier = z ? "世界级" : "World-class";
    else if (score >= 85) tier = z ? "精英级" : "Elite";
    else if (score >= 78) tier = z ? "可靠级" : "Reliable";
    else tier = z ? "发展中" : "Developing";
    const workload = minutes >= 2700 ? (z ? "主力" : "Starter") : (z ? "轮换" : "Rotation");
    return (z ? role.zh : role.en) + " | " + tier + " | " + workload;
}

function cycleQueueStatus(playerKey) {
    const player = reviewQueue.find((row) => queueStatusKey(row) === playerKey);
    const current = scoutQueueStatuses[playerKey] || (player ? getQueueStatus(player) : "pending");
    const idx = STATUS_CYCLE.indexOf(current);
    scoutQueueStatuses[playerKey] = STATUS_CYCLE[(idx + 1) % STATUS_CYCLE.length];
    saveScoutQueueStatuses();
}

function computeWatchlistDiff(currentPlayers) {
    try {
        const snapshot = JSON.parse(localStorage.getItem(SCOUT_SNAPSHOT_KEY)) || [];
        const currentKeys = new Set(currentPlayers.map(p => p.player_name || p.name));
        const snapshotKeys = new Set(snapshot);
        let added = 0;
        for (const k of currentKeys) { if (!snapshotKeys.has(k)) added++; }
        watchlistDiffCount = added;
    } catch {
        watchlistDiffCount = 0;
    }
}

function saveWatchlistSnapshot(currentPlayers) {
    try {
        const keys = currentPlayers.map(p => p.player_name || p.name);
        localStorage.setItem(SCOUT_SNAPSHOT_KEY, JSON.stringify(keys));
        localStorage.setItem(SCOUT_LASTVISIT_KEY, String(Date.now()));
        touchScoutingWorkspace();
    } catch {}
}

function updateSnapshotStatus() {
    const status = document.getElementById("scout-snapshot-status");
    if (!status) return;
    try {
        const timestamp = Number(localStorage.getItem(SCOUT_LASTVISIT_KEY) || 0);
        if (!timestamp) {
            status.textContent = appState.lang === "zh" ? "尚未保存基线快照" : "No baseline snapshot saved";
            return;
        }
        const stamp = new Date(timestamp).toLocaleString(appState.lang === "zh" ? "zh-CN" : "en-US");
        status.textContent = watchlistDiffCount > 0
            ? `${watchlistDiffCount} ${appState.lang === "zh" ? "名新增 · 基线" : "new · baseline"} ${stamp}`
            : `${appState.lang === "zh" ? "无新增 · 基线" : "No additions · baseline"} ${stamp}`;
    } catch {
        status.textContent = "";
    }
}

function exportReviewQueueCSV() {
    const rows = sortReviewQueue(filterReviewQueue(reviewQueue), scoutSortMode);
    const header = ["player_id", "player_name", "team", "league", "season", "position_group", "optimized_score", "minutes", "confidence_level", "reason_code", "review_status", "reviewer_note", "as_of_date"];
    const data = rows.map((player) => [
        player.player_id || "",
        player.player_name || player.name || "",
        player.team || "",
        player.league || "",
        player.season || "",
        player.position_group || player.position || "",
        player.optimized_score || player.score || 0,
        player.minutes || 0,
        player.confidence_level || player.confidence || "",
        player.reason_code || "",
        getQueueStatus(player),
        player.reviewer_note || "",
        player.as_of_date || "",
    ]);
    const csv = [header, ...data].map((row) => row.map(csvCell).join(",")).join("\n");
    const blob = new Blob(["\uFEFF" + csv], { type: "text/csv;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = "scoutfootball-review-queue.csv";
    link.click();
    URL.revokeObjectURL(url);
}

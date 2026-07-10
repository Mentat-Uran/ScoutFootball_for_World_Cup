# 任务路线图

当前状态：Pipeline 端到端可运行，评分系统处于真实影响力标签和训练目标重构前的校准阶段。最新 v1.3 GPU 优化产物已生成（2026-06-09 23:05，本地 `optimized_params_meta.json`）：2526 holdout Spearman=0.737/Pearson=0.742（baseline 0.621/0.618），raw spread ratio=0.336，train-fitted global points spread ratio=0.985，points MAE=11.55，points bias=-6.47，team coverage=0.990。v1.3 解决了整体分布压缩，但暴露出联赛截距偏差：Serie A -16.6、Ligue 1 -11.3、La Liga -11.2、Premier League +5.8、Bundesliga +1.8。2026-06-09 已完成 v1.3.1-dev 代码级改进：新增训练集联赛残差 offset 和 league-bias loss；只读复算显示当前参数下 points MAE 可从 11.55 降到 9.44，但完整 GPU 重跑仍待执行。2026-06-10 已新增 v1.3.2-dev 代码入口：优化器支持可选 `player_truth_labels.parquet` 球员真值标签锚定损失，`scoutfootball train-rating-nn` 支持监督式 sklearn MLP 候选模型并写入 `data/models/player_rating_nn/`；当前真值标签表仍为空，因此 NN 路径会跳过，默认评分产物未被替换。

本路线图吸收 `advise.md` 的建议，但只采纳适合 ScoutFootball 当前数据现实的部分：优先做展示增强、StatsBomb 事件动作价值、评分验证和模型评估，不把后续更新变成更多爬虫。

## 顶层架构

ScoutFootball 的长期形态是本地优先的足球数据研究平台，而不是数据抓取集合。后续架构扩展为十层：前七层解决当前可落地的评分、事件价值、评估和展示，第八到第十层扩展到球探工作流、预测校准和空间/视频研究。

1. 数据与合规层：继续使用本地缓存、DuckDB 和 Parquet；Transfermarkt 只允许手动或授权导入；FBref 只作为受限低频补充源。
2. 标准事实层：把比赛、球队、球员、阵容、事件、赛季统计、身价和联赛强度统一到 raw/silver/gold/models/reports/logs 分层。
3. 跨供应商标准化层：先定义 ScoutFootball 内部 event/tracking schema，再对齐 SPADL、atomic-SPADL、Common Data Format、kloppy/floodlight 抽象；短期不急加依赖。
4. 事件动作价值层：以 StatsBomb Open Data 为第一主源，新增 `src/scoutfootball/action_value/`，形成 StatsBomb events -> SPADL/atomic-SPADL -> xT -> VAEP/Atomic-VAEP 的演进路线。
5. 球员真值与评分层：综合真实标签、赛季统计、xG/xA、xT/VAEP、出勤可靠性、联赛强度、年龄和趋势；训练目标必须引入真实球员标签，不能只优化球队积分相关性。
6. 评估与模型卡层：建立 `EVALUATION.md`、`MODEL_CARD.md`、位置内指标、跨位置总榜指标、误差分析、数据覆盖说明和模型运行登记。
7. 产品可视化与 API 层：Streamlit 保持本地只读；`frontend/` 静态工作台保留 Liquid Glass 风格并作为长期产品壳；Plotly/mplsoccer/ECharts 继续用于交互图和足球专用图；新增电子战术板作为本地战术演示、动画和导出工作台；FastAPI 只暴露本地只读产物。
8. 球探决策层：围绕真实标签、低置信度球员、误差案例和战术备注建立 watchlist、shortlist、人工审阅队列和可复现报告。
9. 比分预测与概率校准层：保持 Independent Poisson 作为基线，后续升级 Dixon-Coles + time decay，并用 log loss、Brier score、RPS 做对照。
10. 空间/视频/离球研究层：只在有合规样例数据后研究 StatsBomb 360、Metrica/open tracking、space control、xG+、off-ball value 或强化学习。

## 采纳边界

立即采纳：

- mplsoccer 作为可视化增强库。
- socceraction 思路作为事件动作价值层的主要参考。
- xT 作为 VAEP 前的第一版可落地动作价值模型。
- VAEP 论文作为评分解释和动作价值建模的理论核心。
- PlayeRank 的角色内、多维度评分思路，作为位置内指标和球探解释模板参考。
- 2026 combined rating 论文的 top-down + bottom-up 评分框架，作为真实标签层和评分目标重构参考。
- 电子战术板先采纳浏览器本地工作台思路：标准化球场坐标、可拖拽球员/足球、箭头/区域/标签、轨迹/关键帧/步骤式动画、演示播放、PNG/PDF/WebM 导出、本地 JSON 工程。
- Dixon-Coles 作为比分预测第二主线，但优先级低于球员评分。
- xG finishing signal 使用样本量 shrinkage，禁止简单用 `goals - xG` 判定射术。
- StatsBomb Open Data 的引用要求进入数据源 license manifest。

暂缓采纳：

- kloppy 作为 v1.0 之后的跨供应商 event/tracking 数据标准化方案。
- floodlight 只参考 Game/Team/Player/Event/Frame/Segment 抽象，不直接引入。
- Common Data Format 作为 schema 对照和验证参考，短期不改变当前 Parquet 主干。
- xG+ / possession-level shot probability 作为远期研究方向。
- StatsBomb 360、Metrica/open tracking、SoccerNet/video 作为远期空间/视频研究方向。
- 战术板 MP4 导出、本地 ffmpeg、视频叠画、tracking 数据导入、3D/门后视角和实时协作放到战术板核心画布稳定之后。
- 神经网络评分器只作为真实标签层完成后的候选模型；当前只落地监督式 MLP 实验入口，没有球员级标签、缺失字段标记和 baseline 对比前，不进入默认评分产物。
- Opta、Wyscout、SkillCorner、TRACAB 等商业或 tracking 数据源不进入近期计划。

不采纳：

- 新增绕过反爬或验证码的爬虫。
- 把 StatsBomb 小样本事件能力写成全量球员评分能力。
- 在浏览器端执行训练、爬取、视频批量转码或重型模型推理。
- 用 Top N 位置配额替代真实影响力校准。
- 只用球队积分相关性训练神经网络，并把它写成球员真实能力模型。
- 在没有 tracking 样例、标签和评估 baseline 前，直接把强化学习、GCN、Transformer 写成默认评分架构。

## 调研参考

- 开源项目：[`socceraction`](https://socceraction.readthedocs.io/en/stable/index.html)、[`StatsBomb Open Data`](https://github.com/statsbomb/open-data)、[`mplsoccer`](https://mplsoccer.readthedocs.io/)、[`kloppy`](https://kloppy.pysport.org/)、[`floodlight`](https://floodlight.readthedocs.io/en/latest/)、[`Common Data Format`](https://www.cdf.football/)。
- 战术板案例：[`Tactico`](https://tactico.pro/) 的浏览器战术板、阵型/定位球预设和 MP4/WebM/GIF 导出；[`DrawTactics`](https://drawtactics.com/animated-tactics-board) 的路径动画、时间轴、easing 和 WebM 30fps 导出；[`TacticSlate`](https://tacticslate.com/football-tactic-board) 的离线优先、球员名/号码/角色、ghost silhouettes、PNG/PDF/WebM 和 2D/3D；[`Coach Tactic Board`](https://apps.apple.com/us/app/coach-tactic-board-soccer/id834813357) 与 [`Soccer Tactic Board`](https://play.google.com/store/apps/details?id=com.jenda.footballboard) 的自由画笔、训练器材、球员资料、文件夹和导入/导出；[`Metrica Tactical Boards`](https://www.metrica-sports.com/help-center/tactical-boards) 的球员 ID、区域、轨迹、门后视角、timeline slide 和 telestration 工作流；[`FC Tactix`](https://teloframe.com/features/tactics-board)、[`TacticalPad`](https://www.tacticalpad.com/en-us/new/index.php) 与 [`TacticalBoards`](https://tacticalboards.com/) 的 2D/3D、协作、导出和训练计划能力。
- 学术主线：[`VAEP`](https://arxiv.org/abs/1802.07127)、[`xT vs VAEP`](https://tomdecroos.github.io/reports/xt_vs_vaep.pdf)、[`PlayeRank`](https://arxiv.org/abs/1802.04987)、[`combined player rating`](https://link.springer.com/article/10.1186/s40537-026-01369-w)、[`xG finishing bias`](https://arxiv.org/abs/2401.09940)、[`Dixon-Coles`](https://research-information.bris.ac.uk/en/publications/modelling-association-football-scores-and-inefficiencies-in-the-f/)。
- 架构结论：近中期以 StatsBomb -> internal actions -> xT -> VAEP 和真实球员标签为主线；跨供应商 schema、tracking/video、xG+、off-ball value 和强化学习只作为 P6 之后的扩展，不抢 P0-P4。

## 当前不足总览（不含电子战术板）

以下条目是当前项目除 P1.5 电子战术板以外仍存在的功能不足、数据缺口和验证缺口，后续迭代不能只盯战术板：

- **评分真实标签已填充**：`player_truth_labels.parquet` 当前有 7,857 行（expert_tier 7,840 + award 17），NN 训练已匹配 5,776 行，test Spearman=0.721。
- **评分校准仍未闭环**：v1.3.1-dev 的 train-fitted league residual offset 和 league-bias loss 代码已写入，但完整 GPU 重跑、CV、稳定性、feature importance 和 Barcelona/Real Madrid/Burnley 等误差复盘仍待执行。
- **强队/降级队偏差仍需复盘**：当前模型仍记录强队系统性低估和降级队高估，不能只用整体 Spearman/Pearson 宣称球员真实水平已解决。
- **世界杯模块仍是混合/样例视图**：世界杯赛程、名单、对比和出线页还没有全量官方阵容、更多联赛评分覆盖、国家队阵容 API 和低覆盖分层说明，不能写成完整真实后端能力。
- **前端 API 联调不完整**：球员页还缺搜索、分页、完整 player profile 指标、报告导出；身价页还缺 value-fairness OOF report 细分；比赛预测页还缺统一 prediction service、模型版本、Brier/log loss/RPS 和校准状态。
- **报告页信息不足**：model-run registry 当前只展示基础指标，仍缺完整参数、随机种子、依赖版本、输入 hash、误差案例摘要和可复现命令。
- **动作价值仍是样本能力**：`player_value_metrics.parquet` 只代表 StatsBomb 事件价值样本；P2 产物尚未完成全量 internal actions/xT/VAEP 管线、socceraction 依赖评估和公开图表 attribution。
- **数据合规和 license manifest 不完整**：所有本地 Parquet/报告/导出物仍需要统一记录来源、许可、可公开展示边界、更新时间和 StatsBomb Open Data 引用要求。
- **安全和部署边界未闭环**：前端已做 escaping/sanitizer、CSP meta tag、SRI（echarts CDN）、X-Content-Type-Options 安全头、浏览器级 XSS/CSV 回归测试；可配置 CORS 和非本机部署说明仍待实现。
- **球探工作流增强中**：watchlist/shortlist/review queue 只读契约已存在，审阅状态流转和 watchlist diff 已实现；真实标签回灌、shortlist notes 和导出报告仍待实现。
- **比分预测仍是 baseline**：Independent Poisson 可用，但 Dixon-Coles、时间衰减、低比分校准、概率校准回测和模型对比页仍未实现。
- **跨供应商标准化仍停留在规划**：internal event/tracking schema、DATA_CONTRACTS、kloppy/floodlight/CDF 对照、schema validation fixture 和空数据行为测试仍待补。
- **空间/视频/离球研究没有进入默认能力**：StatsBomb 360、Metrica/open tracking、space control、off-ball value、xG+、GCN/Transformer/RL 都只能在有合规样例、baseline 和模型卡后启动。

## 已完成

- [x] **球队实力分析面板**（2026-07-10）：新增 `GET /teams/strength` API，按分钟加权聚合球员评分到球队级别，返回整体评分、位置组（GK/DEF/MID/ATT）实力分布、核心球员和置信度分布；新增前端"球队"视图含排名表、球队详情卡和位置组对比堆叠柱状图；静态导出脚本同步生成 `team_strength.json`。
- [x] **修复 scouting queue 重复计算**（2026-07-10）：`get_review_queue`/`get_watchlist`/`get_shortlist` 原各自独立调用 `build_scouting_queues`，现通过 `_get_scouting_queues()` 缓存复用。
- [x] **修复 api_server.py Path 导入位置**（2026-07-10）：`Path` 原在文件底部局部导入但被上部代码使用，现移至文件顶部。
- [x] **增加 MP4 导出上传大小限制**（2026-07-10）：`tactical-board/export/mp4` 原无上传大小限制，现限制 50MB。
- [x] **修复 pipeline.py DC 校准死代码**（2026-07-10）：原 `if hg < ...: pass  # Could track log-loss here` 占位代码，现实现实际比分 log-loss 计算并写入校准报告。
- [x] **球员对比工具**（2026-07-10）：新增 `GET /players/compare` API，支持双球员雷达叠加、位置百分位对比和关键指标差异表；新增前端"对比"视图含搜索输入、ECharts 雷达图和指标对比表。
- [x] **修复 VAEP player_id → player_name 映射**（2026-07-10）：从 xT 数据和 events_all.parquet 构建 player_id → player_name 映射，回填 VAEP 数据中缺失的球员名称，使动作价值页能显示球员名而非原始 ID。
- [x] **修复校准缓存失效问题**（2026-07-10）：`get_prediction_calibration()` 原用 `@lru_cache(maxsize=1)` 永久缓存，模型重新训练后返回过期数据；现改为 5 分钟 TTL 缓存，支持 `force_refresh` 参数。
- [x] **球队对比工具**（2026-07-10）：新增 `GET /teams/compare` API，支持双球队位置组雷达叠加、位置组差异表和核心球员对比；前端"球队"视图新增球队对比输入区和雷达图。
- [x] 五类核心数据源接入：FBref、Football-Data、Understat、StatsBomb Open Data、Club Elo。
- [x] 本地缓存扩展到 10 赛季级别：Football-Data 原始 CSV 合计 68,953 行，Understat 为 31,902 个球员赛季行；当前活动 `combined_results.parquet` 为 5,330 行，需重建 10 赛季合并 Parquet。
- [x] FBref 5 赛季标准、射门、misc 表均为 14,356 行。
- [x] StatsBomb Open Data 当前缓存 126 场比赛、11,871 条事件。
- [x] 六个新适配器：SofaScore、SoFIFA、WhoScored、Capology、API-Football、Transfermarkt-datasets。
- [x] FBref 扩展：+5 联赛（葡超/荷甲/土超/苏超/比甲）+7 种 stat_type（passing/defense/possession/gca/playing_time/keeper/keeper_adv）。
- [x] Football-Data 扩展：5→18 联赛代码，10 赛季。
- [x] Understat 扩展：+RFPL，6 联赛×10 赛季。
- [x] StatsBomb 批量 events+lineups 下载+合并脚本。
- [x] IngestConfig 集中配置：15 联赛×10 赛季，YAML/JSON 可覆盖。
- [x] Pipeline 配置驱动重构，新增 4 个数据源 handler。
- [x] 跨源球员 ID 对齐：composite key + fuzzy match + 球队名规范化。
- [x] Pipeline 端到端：`scoutfootball ingest` -> `scoutfootball build-features` -> `scoutfootball train`。
- [x] 数据验证入口：`scoutfootball validate`。
- [x] FastAPI 只读入口：`scoutfootball serve`。
- [x] Streamlit 多页工作台入口，当前含总览、分析页、P1 页面、世界杯页、球探队列页和动作价值样本页。
- [x] `frontend/` 静态 Liquid Glass 前端原型：总览、球员、身价、比赛预测、球探、动作价值、报告 7 个视图。
- [x] `frontend/` 电子战术板第一切片：本地画布、归一化坐标、基础对象、阵型预设、本地 JSON 工程和 localStorage 保存已落地。
- [x] `frontend/` 电子战术板 PNG 静态导出和 WebM 动画导出已实现；动画时间轴、PDF 导出、报告嵌入和数据分析联动仍待实现。
- [x] Poisson 比分预测 baseline。
- [x] `value_fairness` OOF 训练产物。
- [x] PyTorch GPU 评分优化器和远程 GPU 计算脚本。
- [x] 粗位置角色重判、CM/后场/GK 权重上限、较强联赛强度曲线。
- [x] 评分优化器 holdout 化：优化只用训练赛季，评估输出 holdout Spearman/Pearson、rank loss、校准分箱、联赛分层和 overfit gap。
- [x] 修复 Pearson 指标误算，避免把 `spearmanr()` 的 p-value 当 Pearson。
- [x] 修复 ST/W quality 绕路：ST/W quality cap 生效，ST attack 不再被额外压死。
- [x] 降低 availability cap：所有位置 availability 上限收敛到 0.18-0.20，CM/DM/FB/CB/GK 不再允许用 0.30-0.36 的出勤权重主导评分。
- [x] 球队赛季聚合从纯分钟加权改为 capped minutes + core rotation 的稳健聚合，避免评分层和球队层重复奖励原始出勤。
- [x] CLI 和远程 GPU API 均按 capped position weights 报告权重，并输出 team aggregation 配置元数据。
- [x] 评估报告新增 team coverage：按 league-season 输出目标球队数、评分侧球队数、匹配球队数和覆盖率，避免把 2526 数据缺口误判成模型错误。
- [x] 重新生成 `player_ratings_optimized.parquet`。
- [x] 将 `advise.md` 融入未来架构和实施策略文档。
- [x] Dixon-Coles 比分预测核心实现：`fit_dixon_coles`、`predict_match_dc`、`DixonColesModel` 类，Pipeline 集成和 data_loader 集成。
- [x] 战术板增强：drawing tool buttons（select/arrow/zone/text）、文本标注类型、曲线箭头渲染、触控支持（iPad/Safari）、循环动画、项目/帧删除按钮。
- [x] 战术板导出：PNG 静态导出、WebM 动画导出（canvas.captureStream + MediaRecorder）、版本迁移。
- [x] 战术板增强：定位球模板（角球、任意球、边线球、点球、门球等）、自动保存和恢复。
- [x] 球员列表增强：分页、排序、联赛筛选。
- [x] 球员对比百分位表：同位置 percentile 对比表。
- [x] 身价偏离分析：value-fairness OOF 残差、联赛/位置偏差、年龄散点分析。
- [x] 球探队列增强：审阅状态流转（review_status）、watchlist diff、shortlist notes。
- [x] Bug 修复：26 个 bug（6 critical、9 warning、11 minor），测试总数 582。
- [x] 前端安全加固：CSP meta tag、SRI（echarts CDN）、X-Content-Type-Options 安全头、浏览器级 XSS/CSV 回归测试。
- [x] v1.0.0 发布准备：版本号统一、CHANGELOG.md、scripts/demo.sh、README 安装文档和已知限制、世界杯页 SAMPLE DATA 标记、前端 DEMO 横幅。
- [x] 桌面应用打包：Electron + PyInstaller，macOS arm64 构建成功（221MB .dmg），前端打包进 app.asar，后端在 extraResources，自动更新通过 electron-updater + GitHub releases。
- [x] Release workflow 修复：删除 `package.json` `publish` 块解决 GH_TOKEN 错误、修复 Windows `Join-Path` 语法、添加 `-p never`、pipeline 步骤改为 `continue-on-error`。
- [x] 测试环境修复：清理损坏的 torch 命名空间包（25 个测试从 FAILED 恢复）、添加 httpx dev 依赖修复集成测试、`api_server.py` 版本号从硬编码 `0.2.0` 改为 `__version__`。
- [x] MP4 导出通过后端 ffmpeg 转换实现（`/tactical-board/capabilities` 和 `/tactical-board/export/mp4` 端点）。
- [x] 前端 Data Status 页面字段名修复（`a.name` → `a.label`，`a.modified` → `a.updated_at`）。
- [x] `/license` 端点字段名修复（`modified` → `updated_at`）。
- [x] `/predictions/meta` 端点添加顶层字段别名（`status`、`model_type`、`num_teams`、`train_rows`、`coverage`），修复前端 match 视图始终显示 "no artifact" 的 bug。
- [x] 前端 match 视图 calibration 部分修复：从正确的嵌套对象读取 rho、home_advantage、coverage、brier、rps 等字段。
- [x] 前端报告页增强：显示 Dixon-Coles 模型状态和 rho 参数。
- [x] 新增 8 个测试文件（104 个新测试）：action_value/schema、calibration、match_prediction、scouting_queue、cross_provider_schema、prediction_summary、tactical_board_api、backtests。
- [x] P6 跨供应商 schema 参考文档：SPADL 兼容性、kloppy/floodlight/CDF 评估已写入 DATA_CONTRACTS.md。
- [x] P2 socceraction 依赖评估文档已写入 DATA_CONTRACTS.md。
- [x] DATA_CONTRACTS.md 补充 `/license`、`/value-summary`、`/predictions/meta` 端点文档。
- [x] Streamlit 球探队列页增强：联赛/位置/置信度筛选、排序、CSV 导出、标签页分栏、置信度分布统计。

## P0：评分系统真实影响力校准

目标：先修训练目标，再扩展评分模型。当前球队积分相关性会偏向出勤、CM 和 GK，不能单独作为球员影响力标签。

- [x] 完成第一轮反出勤捷径 guardrail：availability cap 下调、ST/W quality cap、holdout 评估、稳健球队聚合、team coverage 报告。
- [x] 重建 Football-Data 10 赛季 `combined_results.parquet`，保留 2526 alias patch，并输出 raw CSV 总行数、active Parquet 行数、league-season 覆盖和输入 hash。
- [x] 用新 aggregation/cap 口径重新跑 GPU 优化，生成新的 `optimized_params.npy`、`optimized_params_meta.json`、holdout predictions、league metrics、calibration 和 feature importance。（2026-06-09，3-fold CV 有效 fold 平均 test Spearman=0.717）
- [x] 复盘 `PROBLEMS.md` 中的误差案例：Everton（+0.9 ✓）、Stuttgart（+3.8 ✓）、Rennes（-0.4 ✓）、Napoli（-35.9 ✗）、Real Madrid（-29.7 ✗）、Arsenal（-15.9 ✗），记录新旧排名变化和仍未解决原因。强队系统性低估根因：评分聚合上限约 55-60，实际强队积分 80-90。
- [x] 增加出勤捷径诊断报告：minutes/starts/matches/availability 置换重要性、按位置 availability 权重、球队聚合权重分布。
- [x] 修复 GPU 优化器 `build_matched_results()` 中的 alias 匹配：集成 `normalize_team_name()` + 重音符号去除 + 12 个新 alias。（2026-06-09）
- [x] 修复 Bundesliga 联赛标签 NaN 问题：评分侧 Bundesliga 球队的 league 字段为 "nan"，已在数据构建时替换。（2026-06-09）
- [x] 补充 Football-Data 2526 赛季数据：已下载 1,751 场比赛，combined_results.parquet 从 5,330 行增至 7,081 行。（2026-06-09）
- [x] 完成 v1.3-dev 优化器目标函数重构：区分 raw team strength 与 calibrated season points，新增训练集拟合积分校准层、积分回归损失、1D 分布匹配损失、争冠/降级尾部校准损失；`--soft-rank-temperature` 已贯穿 Spearman/NDCG/位置一致性，NDCG 改为 soft discount 可微目标。
- [x] 用 v1.3-dev 目标完整重跑 GPU optimizer，生成新的 `optimized_params.npy`、`optimized_params_meta.json`、`rating_holdout_predictions.parquet`、CV/stability/feature importance。结果：排序保持（Spearman 0.737），points spread 接近真实分布（0.985），但 points MAE 仍 11.55 且联赛截距偏差明显。
- [x] 完成 v1.3.1-dev 代码改进：训练集联赛残差 offset（可通过 `--disable-league-calibration` 关闭）、`league_bias_weight` 训练损失、holdout predictions 输出 global points / league offset / final calibrated points。
- [x] 完成 v1.3.2-dev 代码改进：新增 `--truth-label-weight`、`--min-truth-labels`、`--disable-truth-label-anchor`，通过 `rating_feature_matrix.parquet` 桥接 `player_id -> player_name/season` 后，把球员真值标签作为可选 z-score + rank anchor loss；标签为空或匹配少于阈值时自动禁用。
- [ ] 用 v1.3.1-dev 目标完整重跑 GPU optimizer，重新生成 `optimized_params.npy`、`optimized_params_meta.json`、`rating_holdout_predictions.parquet`、CV/stability/feature importance，并复盘 Barcelona/Real Madrid/Burnley、Serie A/La Liga/Ligue 1 联赛截距偏差是否改善。
- [ ] 有足够球员真值标签后，用 v1.3.2-dev 目标完整重跑 GPU optimizer，并把 truth-anchor 的 holdout 效果、位置内指标和误差案例写入 `EVALUATION.md`。
- [x] 对 coverage 低于 0.90 的 league-season 禁止输出强排序结论，只允许作为低置信度诊断样本；该规则仍适用于五大联赛以外的 2526 division 和后续新增数据。
- [x] 定义真实标签层级：Transfermarkt 手动导入、权威奖项、国际/俱乐部出场级别、专家分档、位置内人工校准集。
- [x] 新增标签数据契约和校验脚本，输出 `data/gold/feature_store/player_truth_labels.parquet`。
- [x] 标签契约必须包含 `label_source`、`label_confidence`、`as_of_date`、`position_scope`、`manual_review_flag`，并区分身价代理、奖项荣誉、专家分档和人工校准。
- [x] 新增评分特征矩阵契约，输出可复用的 `rating_feature_matrix.parquet` 或等价产物，包含数值特征、位置/联赛类别、数据源覆盖、缺失字段标记、输入文件 hash 和 feature manifest。
- [x] 修正缺失高阶字段处理：防守、控球、xT/VAEP、门将字段缺失时必须有 missing flag 和中性/低置信度 fallback，不能把缺失值 0 当成真实低能力。
- [x] 重写优化目标：组合 Spearman/NDCG、位置内排序、跨联赛校准、年龄/趋势合理性、极端样本惩罚。
- [x] 用新组合目标在 GPU 服务器重跑完整优化，生成新的 `optimized_params.npy`、holdout predictions、league metrics、calibration 和 feature importance。
- [x] 复盘 `PROBLEMS.md` 中的误差案例：Everton、Stuttgart、Hoffenheim、Rennes、Napoli、Real Madrid、Arsenal、PSG，记录新旧排名变化和仍未解决原因。
- [x] 保留球队结果相关性作为辅助校验，不再作为主目标。
- [x] 定义神经网络准入门槛：必须先有球员真实标签、时间切分、当前优化器 baseline、位置内/跨位置指标、误差案例复盘和低置信度规则；不允许只用球队积分监督训练默认模型。
- [x] 补全 2526 Football-Data 覆盖或在报告中剔除积分 N/A 球队，避免把数据缺口误判为模型错误。
- [x] 将位置内榜单和跨位置总榜拆成两个视图。
- [x] 给 GK、CB、FB、DM、CM、AM、W、ST 建立位置内指标和解释模板。
- [x] 对 finishing 使用 shrinkage，避免小样本 `goals - xG` 过度放大。
- [x] 输出评分模型卡，说明数据覆盖、权重、偏差、不可解释区域和低置信度球员。

验收：

- `uv run pytest tests/unit/test_rating_optimizer_validation.py`
- 生成新的评分产物和 holdout 报告。
- README、AGENTS、TASKS、MODEL_CARD 同步更新。

## P1：展示增强和可解释产品层

目标：先让当前评分、xG/xA、趋势和比赛事件变得可读，提升项目展示价值。

### 核心交付（3 个可截图页面）

- [x] **球员雷达/排名页**：球员雷达图（pizza chart），位置内 percentile，位置内 Top 20 榜单，球员详情卡（评分趋势、xG/xA、出勤、联赛强度调整）。
- [x] **身价偏离榜**：实际身价 vs 模型预测身价散点图，高估/低估 Top 20 列表，联赛和年龄段筛选。
- [x] **比赛预测页**：即将进行的比赛列表，主/客/平概率，比分分布图，模型置信度提示。

### 其他增强

- [x] 引入 mplsoccer 依赖并保持 Plotly 现有交互图不回退。
- [x] 新增 `src/scoutfootball/viz/pitch.py`，封装球场、坐标、shot map、pass map、heatmap 基础图。
- [x] 在 Streamlit 增加"位置内榜单"和"跨位置总榜"切换。
- [x] 修复 Streamlit `st.Page` 入口路径，支持从仓库根目录执行 `uv run streamlit run src/scoutfootball/app/streamlit_app.py`。
- [x] 用 `frontend/index.html`、`frontend/style.css`、`frontend/app.js` 重构静态前端，保留 Liquid Glass 风格并补齐主要产品视图。
- [x] 增加低置信度提示：分钟不足、数据源缺失、位置重判不确定、事件样本不足。
- [x] 前端图标统一为几何 Unicode 符号（◎ ◇ € △ □ ⌁ ▣ ⬡ ⊕ ⟷ ⊞），无 emoji。
- [x] 身价页 API 无数据时显示 DEMO 标记，避免静默展示假数据。
- [x] 修正 DuckDB 文件名不匹配（`scoutfootball.duckdb` → `scoutlab.duckdb`）。
- [x] 顶部栏新增 API 连接状态指示器（OK/OFFLINE）。
- [x] `fetchRatings()` 按位置分组计算客户端 radar 百分位，球员列表加载后即有真实 radar 数据。
- [x] 后端容错加固：DuckDB 读取 fallback、`_safe_read_parquet`、numpy 类型序列化、异常捕获。
- [x] 给 README 加截图说明和 demo 复现步骤（前端视图表 + 数据复现命令；实际截图待补充）。
- [x] 前端安全加固：API/本地 JSON 字符串进入 `innerHTML` 前统一 HTML/attribute escaping，CSV 导出增加公式注入防护，战术板 JSON 导入增加 schema sanitizer、对象/帧数量上限和导入大小限制。

### 前端长期功能和后端配套

中长期顺序、阶段门槛和非目标见 `docs/ROADMAP.md`；本文件继续作为唯一任务状态真源。

- [x] 全局数据状态页读取 artifact registry，显示产物更新时间、行数、数据源类型、联赛覆盖率和 confidence gate 已实现。
- [x] artifact registry、更新时间、行数、data source label、license attribution 与 confidence gate 已接入。
- [x] 球员画像页接入 player profile API：模糊搜索、分页、位置/赛季过滤、CSV 导出、xT 摘要、置信度原因、评分快照历史已实现。
- [x] 球员画像页补完整个人信息卡：赛季趋势、低置信度原因、数据来源、位置百分位、缺失字段列表已实现。
- [x] 球员列表补 watchlist/shortlist/战术板操作：每行 3 个动作按钮（□/△/◎），localStorage 存储已实现。
- [x] 身价偏离页接入 value-fairness API：OOF 残差、联赛/位置偏差、年龄曲线、Transfermarkt 导入提示已实现。
- [x] 身价页补价格带筛选、年龄曲线散点图、同位置同年龄对比表、Transfermarkt 导入提示已实现。
- [x] 比赛预测页统一 Score Matrix 和 Match Prediction 后端逻辑：模型对比（Poisson vs Dixon-Coles）、log-loss、coverage gate 已实现。
- [x] 比赛预测页补校准视图：Dixon-Coles 参数、coverage gate 警告、低比分分析、Brier/RPS 指标已实现。
- [x] 球探页接入 review queue/watchlist/shortlist 只读契约；当前优先读取 `data/reports/scouting/*.parquet`，缺失时从评分产物派生只读队列。
- [x] 动作价值页接入 15,062 行 xT + VAEP 产物；仍明确标注为 StatsBomb 样本，不写成全量联赛能力。
- [x] 动作价值页补 StatsBomb Open Data attribution 已实现。
- [x] 报告页接入 model-run registry：展开/折叠详情、复制命令、依赖版本显示已实现。
- [x] model-run registry 已展示 `run_id`、`input_hash`、随机种子、参数、训练/测试切分、Spearman/Pearson 和特征重要性。
- [x] 报告页补完整模型运行详情：参数完整列表、随机种子、训练/测试赛季切分、特征重要性 Top 5 已实现。
- [x] FastAPI 增加 typed read-only endpoints：`/artifacts`、`/players/{player_name}`、`/ratings/snapshots`、`/predictions/{home}/{away}`、`/predictions/meta`、`/review-queue`、`/watchlist`、`/shortlist`、`/action-values`、`/reports/model-runs`；兼容旧路由别名。
- [x] 前端浏览器级安全回归测试已完成：XSS 测试覆盖恶意球员名/队名/报告 run_id/战术板标题/CSV 公式注入。
- [x] 前端已补 CSP meta tag、SRI（echarts CDN）和 X-Content-Type-Options 安全头；CORS 已支持 SCOUTFOOTBALL_CORS_ORIGINS 环境变量配置。
- [x] 世界杯页接入真实评分数据：球员名与评分匹配、覆盖率摘要、未匹配球员 N/A 显示已实现。

### P1.1：球探与动作价值恢复和稳定化（2026-06-23）

- [x] 恢复侧栏"球探"和"动作价值"入口，移除临时 `display:none`。
- [x] 修复球探 `player_name` 契约错配，保留 reason/status/note/date/snapshot 字段。
- [x] 球探增加搜索、状态筛选、显式快照、复核队列 CSV 导出，并合并球员页 localStorage 手动选择。
- [x] 修复动作价值旧字段与现行 `xt_per_90`/`vaep_per_90` 契约错配及未定义变量异常。
- [x] 动作价值增加 xT/VAEP 切换、赛事/分钟/搜索筛选、摘要、小样本提示和战术板能力门控。
- [x] 修复纯静态服务器 404 阻断 `frontend/data/` 回退的问题。
- [x] 增加 `test_frontend_feature_contracts.py`，覆盖入口、字段、静态回退和工作台控件。
- [x] review queue 已分页，每页 50 条，避免一次渲染 9000+ 条记录。
- [x] API 状态 pill 区分 LIVE / STATIC / OFFLINE；静态 fallback 成功时明确标识 STATIC。
- [x] API 和静态缓存均不可用时显示加载失败。
- [x] NaN/undefined 数值显示已加防护。
- [x] 世界杯页状态 pill 已动态化。
- [ ] 将球探/动作价值真实浏览器流程加入 CI，覆盖 API、静态、空数据和移动断点。
- [x] 建立版本化 scouting workspace v1.1 导入/导出和审计字段：支持 workspace ID、revision、时间戳、导入预览、同键冲突检测、安全合并和显式替换；仍不增加生产写 API。
- [ ] 补齐 VAEP `player_id -> player_name/team/season` 映射与未映射覆盖率。

### P1.2：测试与静态导出可靠性（2026-06-23）

- [x] 新增 API JSON 清理回归测试：覆盖 `_clean_json_value` 对 numpy.int64/float64/bool_/inf/NaN 的序列化。
- [x] 新增静态 frontend JSON 契约测试：验证 `frontend/data/` 下各 JSON 文件为合法 JSON dict/list，不含 repr 字符串。
- [x] 新增空数据处理测试：验证 API 和前端对空数据集的降级显示。
- [x] 修复 BUG-001：`scripts/export_static_frontend_data.py` 不再静默使用 `str(obj)` fallback 写入非法 JSON；dataclass/Pydantic response 必须经过 JSON-safe serializer。
- [x] `frontend/data/health.json` 和 `frontend/data/players_list.json` 已从 repr 字符串修复为合法 JSON dict。
- [ ] 完整浏览器 CI 未完成（当前仅有 Node 语法检查和单元测试，无 Selenium/Playwright）。

验收：

- `uv run ruff check .`
- `uv run pytest`
- `uv run streamlit run src/scoutfootball/app/streamlit_app.py`
- `node --check frontend/app.js`
- `node --check frontend/tactical-board.js`
- `python3 -m http.server 8600 --directory frontend`
- 三个 Streamlit 核心页面、Streamlit 总览页、Streamlit 球探队列页、Streamlit 动作价值样本页和静态 Liquid Glass 工作台已完成；截图、更多 API 指标和世界杯页的真实产物联调待补充。

## P1.5：电子战术板、战术演示和动画导出

目标：把 `frontend/` 从静态分析工作台扩展为可用于教练讲解、赛前演示和报告嵌入的电子战术板。该阶段只做本地轻量产品能力，不进入模型训练，也不替代 P2/P3 的动作价值和评分主线。

### 调研结论

- Tactico 把战术板放进完整教练工作流：100+ 阵型、定位球预设、关键帧动画、球物理、MP4/WebM/GIF 导出、球员评价、训练课日历、实时协作、语音和回放链接。
- DrawTactics 强调路径动画：先放阵型和球，再画球员/足球运动路径，支持直线/贝塞尔曲线、step-based 和 timing-based 两种动画模式、时间轴 scrubber、7 种 easing、WebM 30fps 和自定义裁切。
- TacticSlate 强调离线优先和演示：球员名/号码/角色/队色、箭头/曲线/虚线/highlight/connectors、逐帧 duration、ghost silhouettes、IndexedDB autosave、JSON 备份、PNG/PDF/WebM，以及 2D/3D 切换。
- Coach Tactic Board/Soccer Tactic Board 类移动端产品覆盖现实白板常用能力：多线型画笔、自由笔、文字、矩形/区域、训练器材、全场/半场/任意球/角球/点球场景、球员名/号码/位置/照片、拖拽换人、文件夹、PDF/图片导出、横竖屏和导入/导出。
- Metrica Tactical Boards 更偏视频分析/叠画：给球员加 ID、区域和轨迹、动画球员移动、门后视角定位球，把战术板作为 timeline slide，并可和 Field Radar、telestration、tracking 工作流结合。
- FC Tactix/TacticalPad 类专业工具提示远期上限：2D/3D 同步视图、多人协作、live presence、PNG/GIF/MP4 导出、session planning、跨设备和多运动支持；这些只作为远期参考，不能抢当前本地轻量切片。

### 第一切片：本地战术板画布

- [x] 在 `frontend/` 增加"战术板"视图，保留 Liquid Glass 风格，但画布区域要像工作台，不做营销页。
- [x] 建立标准化球场坐标系：`x`/`y` 使用 0-100 归一化，支持 11v11、7v7、5v5、半场、定位球和门后视角预留。
- [x] 支持基础对象：主队/客队球员、门将、足球、教练标记、箭头、折线、曲线路径、区域、多边形、文本标签、编号和颜色。
- [x] 支持阵型预设：4-3-3、4-2-3-1、3-5-2、4-4-2、5-3-2、定位球模板，并允许从当前球员/队伍数据生成初始名单但不强依赖后端。
- [x] 支持选择、拖拽、复制、删除、锁定、图层顺序、撤销/重做、缩放、适配屏幕和键盘快捷键。
- [x] 定义本地 JSON 工程 schema：`board_id`、`title`、`sport`、`pitch_type`、`objects`、`layers`、`frames`、`version`、`created_at`、`updated_at`、`source_attribution`。
- [x] 将工程保存为浏览器本地存储 + 可下载 JSON；后端持久化先不做，避免把前端原型误写成正式数据产品。
- [x] JSON 工程导入/读取/保存已走 schema sanitizer：限制对象数、帧数、文本长度、导入文件大小、坐标范围和对象类型，避免把任意本地 JSON 直接渲染到页面。

### 对标功能池（待实现，不代表当前能力）

#### A. 白板与绘图体验

- [x] 自由画笔：pen 模式收集鼠标路径点，支持颜色、粗细、撤销；eraser 模式删除点击对象。
- [x] 线型工具：箭头支持 solid/dashed/dotted/run/pass/shot/dribble 七种线型；曲线、贝塞尔曲线已实现。
- [x] 图形工具：矩形（rect）、椭圆（ellipse）已实现，支持填充色和边框色；多边形、扇形、阴影区域仍待实现。
- [x] 文字工具：文本标注类型已实现（text annotation）；可拖拽文本框、帧备注、coach notes、字体大小和颜色仍待完善。
- [x] 选择工具：复制（Ctrl+D）、镜像（Ctrl+M）、主队/客队整体镜像已实现；框选、多选、锁定、隐藏、粘贴、旋转、缩放、对齐、分布、前置/后置和层级排序仍待实现。
- [x] 网格与吸附：showGrid 显示 10 单位球场网格，snapToGrid 移动时按 5 单位吸附。
- [x] 画布导航：触控支持（iPad/Safari 基础触控）已实现；缩放、平移、适配屏幕、全屏、移动端双指缩放和键盘快捷键仍待完善。
- [x] 白板状态：path 对象通过 frame visibility 控制每帧显示已实现。

#### B. 球队、球员和棋子模型

- [x] 红蓝两队/主客队同时显示：single/both/transition 三种模式，攻防方向箭头已实现。
- [x] 球衣与棋子外观：circle/square/triangle/diamond 4 种形状，size 1-5，opacity 0.3-1.0 已实现。
- [x] 球衣号码编辑：双击球员棋子弹出号码输入框（0-99），Enter/blur 确认，更新后重绘。
- [x] 球员信息 hover card：悬停显示姓名、号码、球队、位置、替补标记已实现。
- [x] 球员详情 click panel：双击球员打开浮动面板，可编辑姓名/号码/位置/球队/形状/大小/透明度/备注已实现。
- [x] 替补席与换人：bench 对象类型已实现，场外显示为小圆虚线框，拖拽到场上与同队球员交换位置。
- [x] 训练器材对象：锥桶（cone）、标志碟（marker）、杆（pole）、梯子（ladder）、迷你门（minigoal）5 种器材已实现。
- [x] 足球对象增强：多球创建、拖拽轨迹、球权指示器（home/away 色点）已实现。
- [x] 重叠对象处理：重复点击同位置循环选择重叠对象，置顶/置底按钮已实现。
- [x] 队伍模板：saveTeamTemplate/loadTeamTemplate/listTeamTemplates，localStorage 存储已实现。

#### C. 场景、阵型和模板

- [x] 场地类型扩展：11v11、7v7、5v5、半场、训练场、空白白板 6 种球场模式已实现。
- [x] 预设阵型扩展：新增 3-4-3、3-4-2-1、4-1-4-1、4-3-1-2、4-2-2-2、4-5-1、5-4-1 共 7 种阵型。
- [x] 定位球模板：角球近门柱、角球二点、任意球人墙、边线球、点球、门球 build-up、开球套路和防定位球站位。
- [x] 训练模板：rondo、压迫演练、反击、传控 4 种训练模板已实现，含球员、区域和箭头对象。
- [x] 文件夹/项目管理：删除按钮（项目/帧）已实现；按对手、比赛、训练课、主题、日期、标签和作者组织战术板、复制项目、复制帧、另存为模板仍待实现。
- [x] 教学模式：所有阵型/定位球/训练模板已添加 coaching points，演示模式显示教练笔记叠加。

### 第二切片：战术演示和动画时间轴

- [x] 增加 Animate mode：循环播放已实现；关键帧、步骤帧、帧时长、播放/暂停/单步、时间轴 scrubber 仍待实现。
- [x] 支持 step-based 和 timing-based 两种动画模式，step 模式全局步进时长 500-3000ms 已实现。
- [x] 支持对象路径插值：多段线性/Bezier 路径、路径编辑模式、路径可视化已实现。
- [x] 支持 Bezier 路径、4 种 easing、delay/pause、自动控制点计算已实现。
- [x] 支持 ghost silhouettes：动画模式下显示上一帧/下一帧球员半透明位置（ghostOpacity 可调）。
- [x] 支持 trails：动画播放时显示球员/球移动尾迹（渐隐圆点），球拖拽时显示轨迹。
- [x] 支持帧内对象可见性：visibleFrom/visibleTo 字段控制对象在哪些帧显示。
- [x] 支持动画事件标记：press/pass/shot/turnover/overlap/underlap/third-man/cover 8 种类型已实现。
- [x] 支持战术片段结构：phase/trigger/roles 字段 + phase 图标 + phase 过滤已实现。
- [x] 支持演示模式：全屏播放、自动播放动画、帧备注叠加、ESC 退出已实现。
- [x] 动画只在浏览器里播放；浏览器不运行训练、爬虫、批量视频转码或模型推理。

### 第三切片：导出、报告和后端契约

- [x] 支持 PNG 静态导出：当前画布、透明/球场背景、16:9/1:1/9:16 裁切。
- [x] 支持 PDF 导出：通过浏览器打印窗口导出当前画布为可打印 PDF。
- [x] 支持 WebM 动画导出：优先用 `canvas.captureStream` + `MediaRecorder`；导出失败时给出清晰降级提示。
- [x] MP4 导出只作为可选本地后端能力：需检测 ffmpeg 是否存在，输出到 `data/reports/tactical_exports/`，没有 ffmpeg 时不报错，只保留 WebM。（已实现 `/tactical-board/capabilities` 和 `/tactical-board/export/mp4` 端点）
- [x] GIF 导出已通过 gif.js 实现，并保留 WebM 为主要动画格式。
- [x] 导出裁切和版式：full/half-left/half-right/center-16:9/square-1:1 裁切 + 透明背景已实现。
- [x] 打印模式：多帧 PDF + 备注 + 球员图例 + source attribution 已实现。
- [ ] 分享方式：本地 JSON 文件、浏览器下载、剪贴板图片、只读演示链接（后置）、报告页嵌入；云同步和公开分享默认不做。
- [x] 支持 JSON 工程基础导入/导出，并在导入时清洗 schema。
- [x] 版本不兼容时走迁移或只读打开，避免旧工程静默丢字段。
- [x] JSON 工程补 migration registry（1.0.0->1.1.0）、validateProject/roundTripTest、损坏文件处理已实现。
- [ ] 后续 FastAPI read-only endpoint 可设计为 `/tactical-boards`、`/tactical-boards/{id}`、`/tactical-boards/{id}/exports`，但第一阶段不急于实现写入 API。
- [x] 战术板嵌入报告页：Board Snapshots 列表、coaching notes 预览、点击加载已实现。

### 第四切片：数据分析联动

- [x] 从球员画像页发送球员到战术板，自动带入姓名、号码、位置和评分数据已实现。
- [x] 从比赛预测页创建赛前方案：主客队阵型、预测比分矩阵、模型版本和 coverage 作为战术板元数据已实现。
- [x] 从 P2 动作价值产物读取样例 xT 热区作为背景参考，并保留 StatsBomb attribution；不写成全量动作价值战术建议。
- [x] 从 watchlist/shortlist 读取备注，生成战术角色说明（位置/层级/工作量）已实现。
- [x] 从国家队/世界杯页创建队伍模板：4-3-3 阵型 + 球员姓名/号码已实现。
- [x] 支持战术板上显示球员评分 badge（颜色编码：绿/黄/红），可通过按钮切换显示/隐藏。
- [x] xT 热区背景层：action values 页 'Show on Tactical Board' 按钮，蓝红色标，StatsBomb 归属已实现。
- [x] 公开导出物如果包含 StatsBomb Open Data 或其他衍生数据，必须带 data source attribution。（前端已自动更新 source_attribution，导出已包含 attribution 文字）

### 第五切片：质量、安全和兼容性

- [ ] 战术板所有导入字段继续走 `TACTICAL_BOARD.sanitizeProject()`，新增对象类型必须同步 sanitizer、schema 文档和 fixture。
- [x] 战术板浏览器回归测试：10 个新测试覆盖恶意标题/球员名/超大 JSON/损坏 JSON/重复 ID/超出坐标/过多对象/旧 schema 已实现。
- [x] 支持桌面鼠标、触控板、iPad/Safari 基础触控；移动端只读查看和编辑能力可以后置。
- [x] 无障碍基础：25+ aria-label、Tab/Enter/Escape 键盘导航、焦点环、团队图例、导出预览已实现。
- [x] 性能边界：200 对象/60 帧警告、FPS 计数器、Simplify 按钮已实现。
- [x] 自动保存和恢复：编辑后防抖保存、本地存储失败提示、导入前备份当前项目。

验收：

- `node --check frontend/app.js`
- `node --check frontend/tactical-board.js`
- `python3 -m http.server 8600 --directory frontend`
- 手动验证桌面和移动宽度下：对象不溢出、文本不重叠、画布非空、拖拽/撤销/播放/导出可用，红蓝两队、号码修改、hover 信息卡和自由画笔至少完成一个稳定切片。
- JSON 工程 round-trip：创建 -> 导出 -> 重新导入 -> 对象、帧、备注一致。
- PNG 和 WebM 导出至少在本机浏览器通过；MP4 没有 ffmpeg 时必须优雅降级。
- README、TASKS、AGENTS 同步说明该功能是否已实现，不得把未接入后端的 mock 数据写成正式能力。

## P2：StatsBomb 事件动作价值层

目标：先用公开事件数据完成一条可复现的动作价值链路，不引入商业数据源。

- [x] 盘点 `events_all.parquet` 字段和坐标覆盖，写入事件数据覆盖说明。
- [x] 新增 `src/scoutfootball/action_value/` 模块：`spadl_adapter.py`、`xt.py`、`aggregate.py`。
- [x] 第一版只做 StatsBomb events -> internal actions -> xT；internal actions 需记录 provider action id、坐标系、方向、动作结果、前后状态和 source coverage。
- [x] 输出 internal actions schema 文档，并说明它和 SPADL/atomic-SPADL、Common Data Format 的字段映射关系。
- [x] 输出 `data/gold/feature_store/player_action_value.parquet`。
- [x] 生成球员 xT 排行榜、球队 xT 热区图、球员传球/带球推进价值图。
- [x] 评估 socceraction 作为依赖的可维护性，优先复用其 SPADL/xT/VAEP 能力。（评估结果写入 DATA_CONTRACTS.md Section 11）
- [x] 明确 StatsBomb 数据引用要求：公开展示研究或图表时必须注明数据源。（api.py `_STATSBOMB_ATTRIBUTION` + 前端 `attribution_required` 已实现）

验收：

- 事件动作价值产物可由命令重复生成。
- 单元测试覆盖坐标转换、动作类型映射、xT 聚合。
- 文档明确该层当前只覆盖 StatsBomb 样本，不代表全量联赛球员能力。

## P3：评分模型重构

目标：把传统赛季统计评分升级为可解释的混合球探评分。

计划评分结构：

```text
player_rating =
  season_stats_score
+ xg_xa_score
+ action_value_score
+ availability_reliability
+ league_strength_adjustment
+ age_trend_adjustment
+ confidence_adjustment
```

- [x] 把 xT 聚合结果接入评分解释层：xT_per_90、percentile、contribution 已实现。
- [x] VAEP 已在 xT 稳定后实现；当前 6,771 行球员赛季数据，身份映射与前端下钻仍需继续完善。
- [x] 各维度置信度：position_explanation 每维度包含 confidence level 已实现。
- [x] 按位置输出进攻/防守/控球/出勤/质量解释：position_explanation API 字段已实现。
- [x] 新增第一版神经网络候选模型入口：`src/scoutfootball/models/player_rating_nn.py` 使用现有 scikit-learn MLPRegressor，读取 `rating_feature_matrix.parquet` 和 `player_truth_labels.parquet`，按赛季时间切分，并与 `player_ratings_optimized` baseline 对比。
- [x] 新增 `scoutfootball train-rating-nn` 和 `scoutfootball train` 中的 `player_rating_nn` 候选状态输出；当前标签为空时写出 skipped metrics，不生成可用模型结论。
- [x] 神经网络产物写入 `data/models/player_rating_nn/`，保存 metrics、predictions 和 model pickle；当前只是监督式候选入口，不替换当前评分器。
- [ ] 有足够标签后升级浅层神经网络结构：数值特征 + 位置/联赛 embedding 或 one-hot 对照 + dropout/weight decay，不直接替换当前评分器。
- [ ] 神经网络训练目标升级为多任务结构：球员标签排序/回归为主，球队赛季积分相关性为辅助，另加跨联赛校准、年龄趋势合理性和极端样本惩罚。
- [x] NN feature manifest：feature columns、data hash、hyperparameters、metrics、baseline 对比已实现。
- [x] 建立评分回归测试：位置/联赛多样性、GK 范围、攻防权重、低分钟球员 6 个测试已实现。
- [x] 输出 ALGORITHM.md v2.1：评分公式、位置权重、联赛系数、Dixon-Coles、NN 候选、数据流、已知限制已实现。

验收：

- 新旧评分有可解释对比。
- 神经网络候选模型只有在 holdout、位置内指标、低置信度样本和误差案例均优于或至少不劣于当前优化器时，才允许进入默认展示。
- Top 100、位置内 Top 20、弱联赛顶端样本、低分钟球员均有审查报告。
- `MODEL_CARD.md` 更新。

## P4：模型评估文档和报告层

目标：把"能跑"升级为"可评估、可复现、可解释"。

### EVALUATION.md

- [x] 说明数据切分方式：按赛季时间切分（train/test split），明确 holdout 赛季范围。
- [x] 记录 baselines：league average、Independent Poisson、简单 percentile 聚合。
- [x] 记录核心指标：Spearman rank correlation（位置内 + 跨位置）、NDCG、MAE、RMSE。
- [x] 记录误差案例：Top 100 中出勤捷径球员、弱联赛高估样本、低分钟高方差球员、位置误判案例。
- [x] 按位置输出 metrics：GK、CB、FB、DM、CM、AM、W、ST 分别报告。
- [ ] 若存在神经网络候选模型，必须与当前 PyTorch 权重优化器、v3 默认权重和简单 percentile baseline 同一时间切分对比。
- [x] 对 value_fairness 增加 OOF 残差、联赛偏差、年龄段偏差分析。
- [x] 对比分预测增加 log loss、Brier score、RPS、低比分场景单独报告已实现（/predictions/calibration 端点）。
- [x] 建立模型运行登记：/reports/model-runs/{run_id} 端点返回完整 run 详情已实现。

### MODEL_CARD.md

- [x] 说明数据源：FBref、Understat、Football-Data、StatsBomb Open Data、Club Elo、Transfermarkt（手动导入）、Capology（手动导入）。
- [x] 说明标签定义：当前评分目标是什么、真实标签来源（手动导入、奖项、专家分档）、标签覆盖范围。
- [x] 说明适用边界：当前模型覆盖哪些联赛/位置/赛季、哪些场景可以信任、哪些场景结果不可靠。
- [x] 说明已知偏差：出勤偏差（CM/GK 偏高）、联赛强度偏差（弱联赛顶端样本）、位置偏差、年龄偏差、数据缺失偏差。
- [x] 说明不可用场景：单场评分、实时交易建议、青训选材、伤病预测、合同谈判。
- [x] 每次训练保存 feature manifest：SHA256 hash、hyperparameters、metrics 已实现。
- [ ] 每次公开图表或报告保存 data source attribution，尤其是 StatsBomb Open Data 衍生产物。

验收：

- `scoutfootball train` 产出模型报告或报告输入数据。
- `EVALUATION.md` 和 `MODEL_CARD.md` 能解释当前模型能做什么、不能做什么、误差在哪。

## P5：比分预测升级

目标：把比分预测从可运行 baseline 升级为可比较模型族，但不抢球员评分主线资源。

- [x] 保留 baseline_0: league average 已在代码中保留。
- [x] 保留 baseline_1: Independent Poisson 已在代码中保留。
- [x] 新增 `baseline_2: Dixon-Coles` 核心实现：`fit_dixon_coles`、`predict_match_dc`、`DixonColesModel` 类已实现，Pipeline 集成（`run_weekly_train`、`_save_dixon_coles_artifacts`）和 data_loader 集成（`load_score_prediction_dc`）已完成。
- [x] Dixon-Coles 时间衰减和低比分校准：pipeline 已接入 `half_life_days=180` 参数，校准报告输出低比分实际分布。
- [x] 建立低比分校准报告：Brier 分解、校准图数据、联赛覆盖率已实现。
- [x] 增加概率校准页：calibration plot、Brier 分解、低比分分析、联赛校准已实现。

验收：

- 三档模型同一时间切分、同一指标对比。
- Dixon-Coles 只有在优于 baseline 且校准合理时才进入默认展示。

## P6：跨供应商标准化与开放格式层

目标：让 ScoutFootball 未来可以接入更多 event/tracking 数据，但当前不新增商业数据源，不改变 DuckDB + Parquet 主干。

- [x] 设计 ScoutFootball internal match/event/tracking schema，字段至少覆盖 match metadata、team/player identity、period/time、coordinates、action type、outcome、freeze frame 可选字段和 source attribution。（schemas/match.py 已实现 InternalMatch/InternalEvent/TrackingFrame/InternalLineup）
- [x] 写 docs/DATA_CONTRACTS.md：StatsBomb events、internal actions、SPADL 映射、所有 parquet schema、API 契约已实现。
- [x] 评估 kloppy：作为直接依赖、离线转换工具或暂不接入三种方案都要给出依赖风险、坐标转换风险和测试成本。（评估结果写入 DATA_CONTRACTS.md Section 10.2）
- [ ] 参考 floodlight 的 Game/Team/Player/Event/Frame/Segment 抽象，但只有在 tracking 样例数据进入仓库后才考虑代码接入。
- [x] 新增 data source license manifest：前端 license 页面展示 6 个数据源的许可证、引用要求和 URL；后端 /license 端点返回 attribution 数据。
- [ ] 所有 event/tracking schema 变更必须有 fixture、schema validation 和空数据行为测试。

验收：

- 文档能解释未来如何接入 StatsBomb 360、Metrica/open tracking 或授权 provider，而不影响当前 pipeline。
- 没有合规数据源时，该层只保留 schema 和转换实验，不进入默认训练。

## P7：球探决策与人工校准层

目标：把评分系统从“给分”推进到“可审阅的球探工作流”，同时为真实标签层提供人工闭环。

- [x] 新增人工审阅队列：低置信度球员、弱联赛顶端样本、位置重判不确定样本、误差案例球员自动进入 review queue；审阅状态流转（review_status）已实现。
- [x] 设计 watchlist/shortlist 数据契约，字段包括 `player_id`、`reason_code`、`rating_snapshot_id`、`confidence_level`、`review_status`、`reviewer_note`、`as_of_date`；默认放在 `data/reports/scouting/*.parquet`，缺失时可由评分产物派生只读结果。
- [x] 将 Transfermarkt 手动导入、奖项、专家分档、人工校准集统一进入 `player_truth_labels.parquet`，并保留标签来源和置信度。（transfermarkt_manual.py 已实现 `snapshot_to_truth_labels()`）
- [x] Streamlit 已只读展示 review queue；写入型人工标注继续使用本地 CSV/Parquet，不直接放进生产页面。
- [x] 每轮评分优化后输出 watchlist diff：新增、移除、置信度变化、排名变化和触发原因。

验收：

- 评分变化能被人工复核追踪，真实标签可以回灌 P0/P3。
- 不把人工标签和模型预测混在同一字段里。

## P8：空间/视频/离球远期研究层

目标：记录更深研究方向，但只在 P2/P4/P6 稳定且数据合规后启动。

- [ ] StatsBomb 360 freeze-frame：先做 shot/pass context 可视化，再考虑空间占优或接球可达性特征。
- [ ] Metrica/open tracking：只用公开样例验证 schema、坐标和帧级数据管线，不写成全量 tracking 能力。
- [ ] xG+ / possession-level shot probability：作为控球过程威胁模型，必须先有 possession segmentation 和 baseline。
- [ ] off-ball value / space control：需要 tracking 或 freeze-frame 支撑，不能用普通事件数据硬推。
- [ ] 强化学习、GCN、Transformer 只作为研究实验；必须先有标签、baseline、离线评估、可解释报告和模型卡。

启动条件：

- P2 事件动作价值层稳定。
- P4 评估文档稳定。
- P6 schema 和 license manifest 稳定。
- 有合规数据源或明确的本地样例数据。

## 通用实施策略

- 每个阶段只交付一个稳定切片：数据契约、实现、测试、文档同步。
- 新增数据源前先写合规和缓存边界。
- 新增模型前先写 baseline 和评估指标。
- 新增可视化前先确认数据粒度、置信度和空状态。
- 不把计划中的模块写成已实现能力。
- 文档状态必须跟代码和本地数据文件一致。

## 通用验证命令

```bash
uv run ruff check .
uv run pytest
PYTHONPATH=src uv run python -m scoutfootball info
PYTHONPATH=src uv run python -m scoutfootball validate
```

## 爬虫运行环境说明

部分数据源需要特定运行环境，无法在无头 macOS 环境下运行：

| 数据源 | 运行要求 | 建议环境 |
| --- | --- | --- |
| FBref (soccerdata) | 需要 Chrome + Selenium (undetected-chromedriver) | Windows GPU 服务器 |
| WhoScored | 需要 Chrome + Selenium | Windows GPU 服务器 |
| SofaScore | 需要 Chrome + Selenium | Windows GPU 服务器 |
| SoFIFA | 需要 Chrome + Selenium | Windows GPU 服务器 |
| Capology | 需要 ScraperFC + Chrome | Windows GPU 服务器 |
| StatsBomb | 无特殊要求，但下载量大（~1000+ 场事件） | 稳定网络环境，使用 `scoutfootball ingest --sources statsbomb` |
| Transfermarkt-datasets | 无特殊要求，但 DuckDB 文件 ~500MB | 手动下载 DuckDB 放到 `data/raw/transfermarkt_datasets/` |
| API-Football | 需要 API Key（环境变量 `API_FOOTBALL_KEY`） | 任意环境，免费 100 请求/天 |

运行 soccerdata 相关适配器时需设置环境变量：
```bash
SOCCERDATA_DIR=./data/soccerdata uv run python -m scoutfootball ingest --sources fbref
```

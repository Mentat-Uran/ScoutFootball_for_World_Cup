# ScoutFootball for World Cup

> **面向 2026 美加墨世界杯的本地优先足球分析工具箱。**

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![uv](https://img.shields.io/badge/uv-Fast-magenta)](https://github.com/astral-sh/uv)
[![DuckDB](https://img.shields.io/badge/DuckDB-Fast%20Analytics-yellow)](https://duckdb.org/)
[![PyTorch](https://img.shields.io/badge/PyTorch-Optimized-ee4c2c)](https://pytorch.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B)](https://streamlit.io/)

**[English](../README.md)** | **中文**

---

## 2026 世界杯来了

2026 美加墨世界杯 6 月 11 日开赛，48 支球队、104 场比赛、一座奖杯。ScoutFootball for World Cup 帮你看懂数据：谁在超常发挥、谁被低估、每支球队的数字画像。

## 它做什么

ScoutFootball 是本地优先的足球分析平台，把公开数据、手动导入、可解释球员评分和比赛预测组织成可复现的研究流水线。

当前重点：把评分系统升级为可解释、可评估的球探工具——先修真实影响力标签和训练目标，再接入事件动作价值、足球专用可视化和模型卡。

## 核心能力

- **研发流水线:** `ingest` -> `build-features` -> `train`。
- **数据验证:** `scoutfootball validate` 检查训练前数据一致性。
- **本地数据层:** DuckDB + Parquet，按 raw/silver/gold/models/reports/logs 分层。
- **球员评分:** PyTorch 权重优化器，组合目标（Spearman + soft NDCG@20 + 位置内一致性 + 训练集积分/联赛校准 + 分布/尾部/联赛偏差损失 + 球员评分 guardrail + 可选球员真值标签锚定），holdout 评估、availability cap、quality cap、稳健球队聚合、覆盖率过滤和模型运行登记。
- **真实标签契约:** `player_truth_labels.parquet` schema 与校验，支持历史身价、奖项、专家分档、人工校准。当前本地表有 41,389 行，但标签独立性和时间切分评估仍是准入门槛。
- **神经网络候选模型:** `scoutfootball train-rating-nn` 使用 `rating_feature_matrix.parquet` + `player_truth_labels.parquet` 训练监督式 sklearn MLP 候选模型，并写入 `data/models/player_rating_nn/`；除非同切分下优于当前优化器和 baseline，否则不替换 `player_ratings_optimized.parquet`。
- **评分模型卡:** `MODEL_CARD.md` 记录数据源、标签定义、适用边界和已知偏差。
- **比分预测:** Independent Poisson baseline，含比分概率矩阵。
- **产品与可视化:** 15 页 Streamlit 工作台（含产物总览页、球探队列页和动作价值样本页）。Liquid Glass 静态前端含 7 个分析视图（总览、球员、身价、预测、球探、动作价值、报告）、4 个世界杯视图（赛程、名单、对比、出线）和电子战术板第一切片。面向 artifact、球员画像、评分快照、预测、复核队列、watchlist、shortlist、动作价值样本和模型运行的 FastAPI 只读入口。集成 mplsoccer 绘制球员雷达、pizza chart、shot map。低覆盖和样本不足有醒目提示。前端渲染已对 API/本地 JSON 字符串做转义，CSV 导出已防表格公式注入，战术板 JSON 导入已走 schema sanitizer。API 状态 pill 区分 LIVE / STATIC / OFFLINE；review queue 已分页（每页 50 条）；NaN/undefined 数值显示已加防护；静态导出不再把 dataclass/Pydantic response 写成 repr 字符串。

## Liquid Glass 前端

`frontend/` 目录包含静态分析工作台，采用统一的几何图标系统（无 emoji）。所有导航图标使用最小化 Unicode 符号（◎ ◇ € △ □ ⌁ ▣ ⬡ ⊕ ⟷ ⊞），保持视觉一致性。API、本地 Parquet 派生 JSON、demo 字符串和导入的战术板工程字段进入 HTML 前都会转义或清洗。

**7 个分析视图：**

| 视图 | 说明 | 数据来源 |
| --- | --- | --- |
| **总览** (◎) | 产物注册表、数据健康、覆盖指标 | `/artifacts` API |
| **球员** (◇) | 球员池、雷达图、位置内百分位 | `/ratings`、`/players/{name}` API |
| **身价** (€) | 身价偏离散点图、高估/低估排名 | `/value-summary` API |
| **预测** (△) | 比赛预测、比分概率矩阵、交锋记录与近期状态 | `/predictions/{home}/{away}`、`/predictions/{home}/{away}/h2h` API |
| **球探** (□) | 复核筛选、本地状态/备注、watchlist 快照、CSV 导出 | `/review-queue`、`/watchlist`、`/shortlist` API |
| **动作价值** (⌁) | xT/VAEP 排名、样本筛选、3 场样本的球员→比赛动作证据、战术板热区联动 | `/action-values`、`/action-values/evidence/{player_id}` API |
| **报告** (▣) | 模型运行记录、后端契约、指标 | `/reports/model-runs` API |

**4 个世界杯视图：**

| 视图 | 说明 |
| --- | --- |
| **赛程** (⬡) | 小组赛赛程、分组、场馆 |
| **名单** (⊕) | 球队阵容含俱乐部、联赛、评分、置信度 |
| **对比** (⟷) | 两队实力对比含雷达叠加 |
| **出线** (⊞) | 小组出线概率、48 队实力排名 |

## Demo 数据

当 FastAPI 后端不可用时，有映射的视图会回退到 `frontend/data/` 的跟踪静态快照。静态快照是缓存数据，不是实时数据；特定估算数据仍会显示 **DEMO** 标记。

查看真实数据：

```bash
# 1. 启动 FastAPI 后端（提供本地 Parquet/DuckDB 产物）
PYTHONPATH=src uv run python -m scoutfootball serve

# 2. 在另一个终端启动前端
python3 -m http.server 8600 --directory frontend

# 3. 浏览器打开 http://localhost:8600
```

生成前端读取的评分产物：

```bash
uv sync
PYTHONPATH=src uv run python -m scoutfootball ingest
PYTHONPATH=src uv run python -m scoutfootball build-features
PYTHONPATH=src uv run python -m scoutfootball train

# 可选监督式 NN 候选；player_truth_labels 行数不足时会跳过
PYTHONPATH=src uv run python -m scoutfootball train-rating-nn
```

## 世界杯准备度

| 功能 | 状态 |
| --- | --- |
| 48 队阵容评分覆盖 | 进行中 — 当前覆盖五大联赛，世界杯阵容需补充更多联赛数据 |
| 比赛预测 (Independent Poisson) | 基线可用 |
| 球员雷达 / Pizza chart | 已集成 mplsoccer |
| 位置内排名 | 可用，带置信度标记 |
| 比分概率矩阵 | Streamlit 可用 |
| 电子战术板 | 本地画布、动画、PNG/PDF/WebM/GIF、可选 MP4、报告快照和 schema 迁移已实现 |
| Dixon-Coles + 时间衰减 | 已实现基线与校准指标 |

## 当前已知限制

**评分系统：**
- 真实标签已存在，但 Transfermarkt 衍生和自循环标签不能独立证明球员真实影响力
- 评分系统处于校准阶段；强队（Barcelona、Real Madrid）可能被系统性低估
- 联赛截距偏差存在（Serie A -16.6、Ligue 1 -11.3）

**数据覆盖：**
- 动作价值产物有 15,062 行 xT/VAEP；比赛证据下钻仅覆盖仓库跟踪的 3 场事件样本，样本重算 xT 不能与完整聚合榜直接比较或相加，二者都不是全量联赛覆盖
- FBref 数据限于 5 赛季；粗位置映射需要 StatsBomb/阵型数据
- 世界杯阵容已填充，但五大联赛外的评分覆盖仍不完整

**前端：**
- API 不可用时，有映射的视图回退到跟踪静态快照；静态快照不是实时数据
- API 状态 pill 显示 LIVE（API 在线）、STATIC（回退到快照）或 OFFLINE（均不可用）
- review queue 已分页，每页 50 条，避免一次渲染大量卡片
- 球探复核状态和备注仍只保存在浏览器，尚未形成版本化审计 workspace
- 部分 VAEP 行只有 `player_id`，身份映射尚未完成
- 战术板 MP4 导出需要系统安装 ffmpeg

**v1.0 未包含：**
- 空间/视频分析（StatsBomb 360、tracking 数据）
- 战术板实时协作
- 移动端战术板编辑优化

## 电子战术板

电子战术板已作为 `frontend/` 内的本地优先教练和分析工作台落地，参考 [Tactico](https://tactico.pro/)、[DrawTactics](https://drawtactics.com/animated-tactics-board)、[TacticSlate](https://tacticslate.com/football-tactic-board) 和 [Metrica Tactical Boards](https://www.metrica-sports.com/help-center/tactical-boards) 等案例。当前能力包括标准化球场坐标、阵型与定位球、绘图工具、逐帧/路径动画、本地 JSON 工程、schema 迁移、报告快照和 PNG/PDF/WebM/GIF 导出。MP4 是需要 ffmpeg 的可选本地后端能力；公开链接、云同步、视频叠画、tracking 导入和实时协作仍属后续方向。

中长期开发顺序和工程准入门槛见 [`docs/ROADMAP.md`](ROADMAP.md)。

剩余 P1.5 以发布加固和选择性分享为主：剪贴板图片、只读本地演示链接、更严格的迁移 fixture 和浏览器 CI。云同步、视频叠画、tracking 数据导入、2D/3D 同步视图、实时协作和门后视角放到后续阶段。

## 桌面应用（macOS）

独立桌面应用已可用于 macOS（Apple Silicon / arm64）。将 Python 后端、前端和预计算数据打包为单一原生应用，支持自动更新。

| 功能 | 状态 |
|---|---|
| macOS arm64 (.dmg) | 已构建并验证 |
| GitHub Release 自动更新 | 已实现（electron-updater） |
| 系统托盘 | 已实现 |
| 内置数据 | 球员评分、比赛结果、模型 |
| Windows 构建 | 未实现（需要 Windows 机器） |

从源码构建：

```bash
cd desktop && npm install
bash scripts/build-desktop.sh --mac
```

产出：`desktop/dist/ScoutFootball-1.0.0-arm64.dmg`

## 本地数据概览

| 数据源 | 当前缓存 | 覆盖 |
| --- | --- | --- |
| **FBref** | 每表 14,356 行 | 5 赛季标准、射门与 Misc 数据 |
| **Football-Data** | 原始 CSV 68,953 行 | 10 赛季，20 个联赛/级别 |
| **Understat** | 31,902 行 | 10 赛季球员统计 |
| **StatsBomb Open Data** | 126 场 / 11,871 事件 | 公开比赛与事件样本 |
| **评分** | 30,483 行 | 优化后球员评分 |
| **特征矩阵** | 8,141 行 | 含缺失字段标记与位置中位数兜底 |

## 顶层架构

10 层路线图，前 7 层是当前主干，第 8-10 层在核心层稳定后建设：

1. **数据与合规层** — 缓存、清洗、合并
2. **标准事实层** — 统一实体（比赛、球员、事件）
3. **跨供应商标准化层** — 兼容 SPADL、kloppy/floodlight
4. **事件动作价值层** — xT -> VAEP
5. **球员真值与评分层** — 模型卡、真实标签、赛季统计
6. **评估与报告层** — baseline 与误差分析
7. **产品可视化与 API 层** — FastAPI、Streamlit、mplsoccer、电子战术板
8. **球探决策层** — Watchlist、专家队列审阅、战术备注
9. **比分预测与概率校准层** — Dixon-Coles + 时间衰减
10. **空间/视频/离球研究层** — StatsBomb 360、Tracking 解析

## 快速开始

**前置条件：** Python 3.11+ 和 [uv](https://docs.astral.sh/uv/)（快速 Python 包管理器）。

```bash
# 安装 uv（如未安装）
curl -LsSf https://astral.sh/uv/install.sh | sh

# 克隆并安装
git clone https://github.com/Mentaturan/ScoutFootball_for_World_Cup.git
cd ScoutFootball_for_World_Cup
uv sync

# 一键演示（验证数据、运行流水线、启动服务器）
bash scripts/demo.sh

# 或分步执行：
PYTHONPATH=src uv run python -m scoutfootball info      # 项目信息
PYTHONPATH=src uv run python -m scoutfootball validate   # 数据验证
PYTHONPATH=src uv run python -m scoutfootball ingest     # 数据采集
PYTHONPATH=src uv run python -m scoutfootball build-features
PYTHONPATH=src uv run python -m scoutfootball train      # 训练评分

# 启动 Web 界面（两个终端）
PYTHONPATH=src uv run python -m scoutfootball serve      # API 在 :8600
python3 -m http.server 8601 --directory frontend         # 前端在 :8601
```

浏览器打开 http://localhost:8601 查看 Liquid Glass 前端，或运行 Streamlit：

```bash
uv run streamlit run src/scoutfootball/app/streamlit_app.py
```

**首次运行提示：** 流水线首次运行时会下载并缓存公开数据，需要网络连接。后续运行使用本地缓存。

## 技术栈与合规

- **技术栈:** Python, uv, DuckDB + Parquet, pandas, scikit-learn, Streamlit, Plotly, mplsoccer, FastAPI, PyTorch.
- **合规准则:**
  - 不绕验证码，不恶意高频爬取。
  - 商用数据源（如 Transfermarkt）仅支持手动或授权导入。
  - 公开 StatsBomb Open Data 衍生产物必须标明数据来源。

---
*ScoutFootball for World Cup — 为足球最盛大的舞台而生。*

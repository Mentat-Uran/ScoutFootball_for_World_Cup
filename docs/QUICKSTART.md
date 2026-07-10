# ScoutFootball 快速启动指南

## 🚀 一分钟启动

### Windows 用户
双击运行 `scripts/start.bat`，选择启动方式。

### macOS/Linux 用户
```bash
chmod +x scripts/start.sh
./scripts/start.sh
```

---

## 📋 启动选项说明

| 选项 | 服务 | 访问地址 | 说明 |
|-----|-----|---------|-----|
| 1 | Streamlit 前端 | http://localhost:8501 | 12个页面，含世界杯功能 |
| 2 | FastAPI + Liquid Glass | http://localhost:8000 | 7视图工作台，API文档在 /docs |
| 3 | 两者同时启动 | 8501 + 8000 | 完整功能 |

---

## 🏗️ 三组件架构

```
┌─────────────────────────────────────────────────────────┐
│                    ScoutFootball 项目                     │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌──────────────────────┐      ┌───────────────────────┐ │
│  │   Streamlit 前端      │      │  Liquid Glass 前端    │ │
│  │   (12个页面)          │      │   (7个视图)           │ │
│  │   直接读本地数据      │      │   通过API/mock        │ │
│  └──────────────┬───────┘      └───────────┬───────────┘ │
│                 │                           │            │
│                 └──────────────┬────────────┘            │
│                                │                         │
│                  ┌─────────────▼─────────────┐          │
│                  │    FastAPI 后端服务       │          │
│                  │  api_server.py + api.py   │          │
│                  │     + data_loader.py      │          │
│                  └─────────────┬─────────────┘          │
│                                │                         │
│                  ┌─────────────▼─────────────┐          │
│                  │    本地数据仓库           │          │
│                  │  Parquet / DuckDB        │          │
│                  └───────────────────────────┘          │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

---

## 📊 视图对照关系

### Streamlit 页面 → Liquid Glass 视图 映射

| Streamlit 页面 | Liquid Glass 视图 | 后端 API |
|--------------|------------------|---------|
| Player Comparison | 球员 | `/player/{name}/profile` |
| Position Percentiles | 球员 | `/ratings` |
| Player Rankings | 球员 | `/ratings` |
| Trends | 无 | 待同步 |
| Value vs Performance | 身价 | `/value-summary` |
| Value Deviation | 身价 | `/value-summary` |
| Score Matrix | 预测 | `/predictions/{home}/{away}` |
| Match Prediction | 预测 | `/predictions/{home}/{away}` |
| Head-to-head history and recent form | 预测 | `/predictions/{home}/{away}/h2h` |
| World Cup Schedule/Squads/Compare/Probability | 世界杯四视图 | `/world-cup/*`, `/worldcup/teams` |
| - | 总览 | `/artifacts`, `/health`, `/ratings/meta` |
| Scouting Queue | 球探 | `/review-queue`, `/watchlist`, `/shortlist` |
| Action Value | 动作价值 | `/action-values` |
| - | 报告 | `/reports/model-runs` |

---

## 💾 数据准备

### 跟踪静态快照
- 无需启动 API 即可用 `python -m http.server 8601 --directory frontend` 打开发布快照。
- 有映射的 API 路径会回退到 `frontend/data/`；这是缓存数据，不是实时数据。
- 需要最新本地产物、动态球员详情或可选 MP4 导出时，启动 FastAPI。

### 完整数据准备
```bash
# 1. 准备数据
uv run python -m scoutfootball ingest

# 2. 构建特征
uv run python -m scoutfootball build-features

# 3. 训练评分
uv run python -m scoutfootball train

# 4. 导出到 DuckDB (可选)
uv run python -m scoutfootball export-ratings
```

---

## 🌐 校园网 / 局域网访问

最简单的部署方式是单端口运行 FastAPI，由它同时提供前端和 API：

```bash
uv sync
uv run python -m scoutfootball serve --host 0.0.0.0 --port 8000
```

然后在本机访问：

```text
http://127.0.0.1:8000
```

同一校园网内的其他设备访问：

```text
http://你的电脑IPv4地址:8000
```

Windows 可直接运行：

```bat
scripts\start-lan.bat
```

如果其他设备仍无法访问，通常是以下两类原因：

- Windows 防火墙未放行对应 TCP 端口。
- 校园网开启了 AP/Client Isolation，禁止终端之间互访。

## 🗂️ 静态产物分层

为了避免本地导出把仓库里的发布快照改脏，静态 JSON 现在分成两层：

- `frontend/data/`：发布快照，已跟踪，供静态演示站和 GitHub Actions 使用。
- `frontend/local-data/`：本地快照，已忽略，供你在自己电脑上临时导出验证。

本地导出：

```bash
uv run python scripts/export_static_frontend_data.py
uv run python scripts/compute_worldcup_predictions.py
```

发布导出：

```bash
uv run python scripts/export_static_frontend_data.py --profile release
uv run python scripts/compute_worldcup_predictions.py --profile release
```

## 🔧 手动启动命令

### Streamlit 单独启动
```bash
uv run streamlit run src/scoutfootball/app/streamlit_app.py
```

### FastAPI + Liquid Glass 单独启动
```bash
uv run python -m scoutfootball serve
# 或
uv run uvicorn scoutfootball.api_server:create_app --factory --host 0.0.0.0 --port 8000
```

### API 文档
启动 API 服务后访问：http://localhost:8000/docs

---

## 📚 更多文档

- 项目 README: [README.md](README.md)
- 前后端同步分析: [docs/FRONTEND_SYNC.md](docs/FRONTEND_SYNC.md)
- 模型说明: [MODEL_CARD.md](MODEL_CARD.md)
- 算法说明: [ALGORITHM.md](ALGORITHM.md)

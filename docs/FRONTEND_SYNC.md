# 前端、API 与静态快照同步规范

> 更新日期：2026-07-10。本文件规定同步方式，不记录任务完成状态。

## 1. 组件边界

| 组件 | 读取方式 | 允许职责 | 禁止职责 |
| --- | --- | --- | --- |
| Liquid Glass `frontend/` | FastAPI 优先，静态 JSON 回退 | 只读分析、筛选、导出、localStorage 轻量状态、战术板 | 训练、爬取、批处理、把样本写成全量结论 |
| Streamlit | `data_loader.py` 读取本地产物 | 研究页面、诊断、模型报告 | 隐式修改训练产物 |
| FastAPI | `api.py` + `data_loader.py` | typed read-only endpoints、能力探测、可选本地导出 | 未版本化的任意写入 |
| 静态快照 | `frontend/data/` | 发布演示、离线/静态回退 | 作为实时数据或用户写入存储 |
| 数据层 | DuckDB + Parquet | 数据真源、模型与报告产物 | 依赖浏览器状态作为真源 |

## 2. 视图契约

| 视图 | API | 静态文件 | 关键边界 |
| --- | --- | --- | --- |
| 总览 | `/artifacts`, `/health`, `/ratings/meta` | `artifacts.json`, `health.json`, `ratings_meta.json` | 行数、更新时间、来源、coverage 必须同时展示 |
| 球员 | `/ratings`, `/players/{name}` | `ratings.json`, `player_profiles/*.json` | 位置内比较；缺字段不能当作 0 |
| 身价 | `/value-summary` | `value_summary.json` | OOF 与估算值必须区分 |
| 预测 | `/predictions/*`, `/predictions/calibration` | `predictions_*.json` | 模型版本、coverage、Brier/RPS |
| 球探 | `/review-queue`, `/watchlist`, `/shortlist` | 对应三个 JSON | 服务端只读；浏览器状态不是正式审计记录 |
| 动作价值 | `/action-values` | `action_values.json` | xT/VAEP schema、样本量、分钟门槛、StatsBomb attribution |
| 报告 | `/reports/model-runs` | `model_runs.json` | 输入 hash、随机种子、参数、指标 |
| 世界杯 | `/world-cup/*`, `/worldcup/teams` | `data/worldcup/**` | 真实/估算/缺失状态必须明确 |

## 3. API 与静态回退规则

1. 本地/LAN 默认 API-first；Vercel 和桌面包可以 static-first。
2. `_staticUrlFor()` 有映射时，API 网络失败、5xx 或纯静态服务器产生的 404 都可以回退。
3. 无静态映射的 4xx 必须保留错误语义，不得用不相关 JSON 掩盖。
4. 回退数据必须与 API 返回使用同一字段名和空值语义。
5. 页面必须显示 API 在线/离线以及静态缓存提示，不能把静态快照称为实时数据。
6. API 状态 pill 区分三种状态：LIVE（API 在线）、STATIC（回退到 `frontend/data/` 快照）、OFFLINE（API 和静态缓存均不可用）。
7. 静态 fallback 成功时，pill 明确标识 STATIC；API 和静态缓存都不可用时，视图显示加载失败提示。

## 4. 契约变更流程

任何 payload 字段新增、改名或删除都必须同时完成：

1. 更新 `src/scoutfootball/api.py` 或对应 typed model。
2. 更新 `scripts/export_static_frontend_data.py`。
3. 重新生成或验证 `frontend/data/` 快照。
4. 更新前端读取与空状态。
5. 更新 `docs/DATA_CONTRACTS.md` 和本文件的映射。
6. 增加契约测试；字段迁移期同时兼容新旧键，并记录移除期限。

当前动作价值兼容策略：主契约使用 `xt_per_90` / `vaep_per_90`，仅对 legacy `player_value_metrics` 保留 `xT_per_90` 读取。当前球探主契约使用 `player_name`，不得再次退回 `player`。

## 4.5 静态快照序列化规则

1. `frontend/data/` 下的所有 JSON 文件必须是合法 JSON（dict 或 list），不允许包含 Python repr 字符串。
2. `scripts/export_static_frontend_data.py` 中 dataclass/Pydantic response 必须经过 JSON-safe serializer（如 `model.model_dump()` 或 `dataclasses.asdict()`），不允许静默使用 `str(obj)` fallback。
3. 静态快照导出脚本遇到不可 JSON 序列化的对象时必须报错终止，不能把 repr 字符串写入文件。
4. NaN/inf 值在序列化前必须被清理为 `null` 或移除，不允许写入非法 JSON 值。

## 5. 前端状态与持久化

- 服务端队列、模型运行和动作价值为只读数据。
- 复核状态、备注、手动 watchlist/shortlist 和战术板工程可以先存 localStorage，但 UI 必须标记“本地状态”。
- 球探本地状态使用 `scoutfootball.scouting-workspace` v1.1 显式导入/导出；导入必须先校验 schema/版本/大小/数量，并显示冲突预览，不得静默覆盖。
- workspace audit 的 `workspace_id`、`revision`、时间戳和 `last_action` 只用于浏览器本地备份与冲突判断，不得描述为服务端身份审计。
- localStorage schema 改动必须提供版本和迁移；重要人工结果需要显式导出，不能承诺自动跨设备或永久保存。
- 正式回灌模型的人工标签必须经过命令行导入和 schema 校验，进入 Parquet 产物并记录来源。

## 6. 视觉与交互规范

- 沿用现有 Liquid Glass token，不在单页引入第二套色板、圆角或阴影体系。
- 信息层级优先：来源/覆盖边界、筛选、主要结论、明细、空状态。
- 交互必须有键盘焦点、44px 移动触控目标、可读标签和 `aria-live` 状态反馈。
- 不用 hover 作为唯一提示；不使用 emoji 作为导航图标；动态图表必须有文本摘要。
- 小样本、低覆盖和未映射实体必须显式显示，不能静默参与强排序。

## 7. 最低验证集

```bash
node --check frontend/app.js
node --check frontend/tactical-board.js
node --check frontend/tactical-renderer.js
uv run pytest tests/unit/test_frontend_feature_contracts.py -q
uv run pytest tests/unit/test_frontend_security.py -q
uv run pytest tests/integration/test_api_endpoints.py -q
```

浏览器至少验证：API 在线、纯静态回退、球探筛选与状态流转、xT/VAEP 切换、760px 以下布局、空数据和 StatsBomb attribution。

# ScoutFootball 用户说明书

## 1. 产品简介

ScoutFootball 是一款本地优先的足球分析平台，为 2026 美加墨世界杯打造。它将公开数据、球员评分、比赛预测和战术板整合为一个可复现的研究工作台。

核心功能：

- **球员评分与排名**：基于多源数据的综合评分系统，含位置内百分位对比和置信度标记
- **身价偏离分析**：实际身价 vs 预测身价对比，识别低估/高估球员
- **比赛预测**：Dixon-Coles 模型驱动的比分预测，含概率矩阵和校准指标
- **电子战术板**：阵型预设、绘图工具、动画系统、多格式导出
- **世界杯专题分析**：48 队阵容、赛程、对比、出线概率

## 2. 系统要求

| 运行方式 | 要求 |
|----------|------|
| 源码运行 | macOS / Linux / Windows，Python 3.11+，[uv](https://docs.astral.sh/uv/) 包管理器 |
| 桌面应用 | macOS Apple Silicon (arm64) 或 Windows x64 |
| 浏览器 | Chrome / Edge / Safari / Firefox 最新版 |
| 网络 | 首次运行需联网下载数据，后续可离线使用 |

## 3. 安装方式

### 3.1 源码安装

```bash
# 安装 uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# 克隆项目
git clone https://github.com/Mentaturan/ScoutFootball_for_World_Cup.git
cd ScoutFootball_for_World_Cup
uv sync
```

### 3.2 桌面应用安装

- **macOS**：从 [GitHub Releases](https://github.com/Mentaturan/ScoutFootball_for_World_Cup/releases) 下载 `.dmg` 文件，拖入 Applications 文件夹
- **Windows**：从 GitHub Releases 下载 `.exe` 安装程序，按提示安装
- 首次打开 macOS 应用时需右键点击 → 打开（未签名应用）

## 4. 启动方式

### 4.1 FastAPI 单端口模式（推荐）

```bash
uv run python -m scoutfootball serve --host 0.0.0.0 --port 8000
```

浏览器访问 http://127.0.0.1:8000 ，前端和 API 同端口。

### 4.2 Streamlit 模式

```bash
uv run streamlit run src/scoutfootball/app/streamlit_app.py
```

访问 http://localhost:8501

### 4.3 桌面应用

双击 ScoutFootball.app（macOS）或 ScoutFootball.exe（Windows）即可启动。桌面应用自动启动后端服务和前端服务。

### 4.4 局域网访问

```bash
uv run python -m scoutfootball serve --host 0.0.0.0 --port 8000
```

同一网络内的其他设备访问 `http://你的电脑IP:8000`

## 5. 各视图功能说明

### 5.1 总览 ◎

展示数据健康状态、产物统计、License Attribution、置信度门控。快速跳转球员、身价、预测三个核心视图。

### 5.2 球员 ◇

- **球员池**：按位置/赛季/联赛筛选，支持排序和分页
- **雷达图**：同位置百分位对比
- **球员详情卡**：评分、置信度、3 赛季趋势
- **球员对比**：选择两名球员叠加雷达图
- **导出**：CSV 格式导出球员列表

### 5.3 身价 €

- **散点图**：实际身价 vs 预测身价，按价格区间筛选
- **偏离榜**：低估/高估球员排名
- **年龄曲线**：身价与年龄关系
- 注意：Transfermarkt 数据需手动导入，当前为估算值

### 5.4 预测 △

- **比赛选择**：选择主客队
- **胜平负概率条形图**
- **比分矩阵热力图**
- **校准指标**：Brier score、RPS
- **赛前战术板**：一键生成赛前战术计划

### 5.5 报告 ▣

- **模型运行记录**：评分优化器、身价模型、预测模型状态
- **后端契约**：FastAPI 端点列表
- **Board Snapshots**：战术板快照列表

### 5.6 战术板 ◫

- **阵型预设**：12 种阵型（4-3-3、4-2-3-1、3-5-2 等）
- **球场类型**：11v11、7v7、5v5、半场、训练、空白
- **显示模式**：单队、双队、攻防转换
- **定位球模板**：角球、任意球、点球、边线球、门球
- **训练模板**：Rondo、压迫训练、反击、控球
- **绘图工具**：选择/移动、箭头、区域、文字注释、事件标记
- **动画系统**：关键帧、路径编辑、贝塞尔曲线、缓动函数
- **导出**：PNG、PDF（打印）、WebM 动画、GIF、MP4（需 ffmpeg）
- **快捷键**：Ctrl+Z 撤销、Ctrl+Y 重做、Ctrl+D 复制、Ctrl+M 镜像、Delete 删除

### 5.7 世界杯赛程 ⬡

- 48 队 12 小组小组赛赛程表
- 按小组/比赛日筛选
- 比赛日期、时间、场馆信息

### 5.8 世界杯名单 ⊕

- 48 队 26 人名单
- 球员评分和置信度
- 评分分布图
- 一键生成球队战术板模板

### 5.9 世界杯对比 ⟷

- 两队实力对比
- 总览对比表
- 评分分布对比图
- Top 5 球员对比
- 比赛预测面板

### 5.10 世界杯出线 ⊞

- 12 小组出线概率
- 48 队实力排名
- 娱乐性估算，仅供参考

### 5.11 数据源 ⊛

- 数据源列表及许可证
- StatsBomb 署名声明
- 仓库信息

### 5.12 数据 ◉

- 数据源行数统计
- 联赛覆盖率
- 缺失数据警告

### 5.13 校准 ⊜

- 预测 vs 实际校准图
- 低分区分析
- 联赛级别校准
- Brier 分解指标

## 6. 桌面应用使用说明

### 6.1 系统托盘

- 应用关闭窗口后不会退出，缩小到系统托盘
- 托盘菜单：显示窗口、检查更新、退出
- 点击托盘图标恢复窗口

### 6.2 自动更新

- 应用启动 5 秒后自动检查更新
- 发现新版本时弹出下载提示
- 下载完成后提示重启安装

### 6.3 数据目录

- 桌面应用数据打包在应用内
- 日志位置：`~/Library/Application Support/scoutfootball/logs/`（macOS）
- 用户战术板工程：浏览器 localStorage

## 7. 常见问题与故障排除

### Q: 页面显示 "API OFFLINE"

后端服务未启动或未就绪。源码运行时先执行 `uv run python -m scoutfootball serve`；桌面应用会自动启动后端，等待约 10 秒后刷新页面。

### Q: 首次启动很慢

首次运行需下载和缓存公开数据（FBref、Football-Data、Understat、StatsBomb），可能需要数分钟。世界杯页面首次加载需计算 48 队评分，约 30-60 秒。后续运行使用本地缓存，速度正常。

### Q: macOS 提示"无法打开，因为无法验证开发者"

右键点击应用 → 选择"打开" → 在弹出对话框中点击"打开"。或在终端执行：

```bash
xattr -cr /path/to/ScoutFootball.app
```

### Q: 页面显示 DEMO 标记

表示该视图使用内置演示数据，未连接后端 API。启动后端服务后刷新页面即可看到真实数据。

### Q: 战术板 MP4 导出不可用

MP4 导出需要系统安装 ffmpeg。安装方法：

```bash
# macOS
brew install ffmpeg

# Windows — 从 https://ffmpeg.org 下载
```

### Q: 局域网其他设备无法访问

检查防火墙是否放行对应端口（默认 8000）。部分校园网开启了 AP 隔离，禁止终端间互访。

### Q: 球员评分置信度低

评分系统处于校准阶段。低置信度可能因为：出场时间不足、数据缺失、位置重判不确定、联赛覆盖率低。具体原因会在球员详情中标注。

## 8. 数据源与许可

| 数据源 | 许可证 | 署名要求 |
|--------|--------|----------|
| StatsBomb Open Data | CC0 (公共领域) | 公开展示必须注明 StatsBomb |
| Football-Data.co.uk | 免费使用 | 需注明来源 |
| FBref / Understat | 公开数据 | 需注明来源 |
| Transfermarkt | 需授权 | 仅限手动导入 |

重要提示：

- 使用 StatsBomb Open Data 衍生的图表和报告必须显示 StatsBomb 署名标记
- Transfermarkt 数据仅允许手动或授权导入，禁止自动化爬取
- FBref 仅作为受限低频补充源，不绕过验证码或反爬机制

---

*ScoutFootball v1.0.3 — 为 2026 美加墨世界杯打造*

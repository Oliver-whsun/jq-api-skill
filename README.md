# jq-api: JoinQuant API 查询工具

> 🤖 让 AI Agent 准确查询聚宽量化平台 API——不再编造函数，不再用错未来函数。

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3](https://img.shields.io/badge/Python-3.7+-green.svg)](references/jq_search.py)

## 是什么

`jq-api` 是一个专为 AI Agent 设计的 **JoinQuant（聚宽）量化交易平台 API 参考工具**。

当 Agent 需要编写聚宽量化策略、查询函数用法、配置回测参数时，它能快速、准确地找到官方 API 文档内容——而不是靠训练数据的记忆"捏造"一个根本不存在的函数。

## 核心特性

- ✅ **准确来源**：所有内容提取自 JoinQuant 官方 PDF 文档（102 页，3651 行）
- ✅ **中文友好**：UTF-8 编码，中文关键词直接搜索，无需转义
- ✅ **智能标注**：自动识别 ♠ 回测专用 API，避免在研究模块中误用
- ✅ **页码索引**：搜索结果标注对应 PDF 原版页码，便于溯源
- ✅ **零依赖**：纯 Python 3 标准库，无任何第三方包依赖
- ✅ **多 Agent 通用**：适配 Claude Code、Cursor、Codex、WorkBuddy 等主流 Agent

## 安装

### 方式一：npx skills（推荐）

```bash
npx skills add sunweiheng/jq-api-skill
```

### 方式二：手动克隆

```bash
git clone https://github.com/sunweiheng/jq-api-skill.git
# 将 jq-api 目录放入 Agent 的 skills 目录
```

## 快速开始

```bash
cd jq-api-skill/references

# 搜索函数
python3 jq_search.py get_bars
python3 jq_search.py order_target order_value
python3 jq_search.py 资金流向 -c 5

# 只看回测专用 API
python3 jq_search.py 历史 --backtest-only

# 输出到文件
python3 jq_search.py get_price -o /tmp/output.txt
```

## 典型使用场景

| 场景 | Agent 提示词示例 |
|------|-----------------|
| 查历史数据函数 | "用 get_bars 获取平安银行最近 20 天的日线数据" |
| 查下单函数 | "用 order_target 将持仓调整为 0" |
| 资金流向分析 | "获取主力资金净流入最高的前 10 只股票" |
| 配置回测 | "set_benchmark 设为沪深 300 指数" |
| 定时运行 | "每天开盘前 5 分钟运行一次" |

## ♠ 标记说明

JoinQuant API 分两类：
- **通用 API**：研究模块和回测均可使用
- **回测专用 API**：标记为 ♠，只能在回测/模拟环境调用

本工具自动在搜索结果中标注 ♠ 标记，防止误用。

已知回测专用 API：`history`、`attribute_history`、`get_current_data`、`get_bars`、`run_daily` 等。

## 文件结构

```
jq-api-skill/
├── SKILL.md                      # Skill 定义（Agent 触发规则和使用说明）
├── README.md                     # 本文件
├── LICENSE                      # MIT License
└── references/
    ├── JoinQuantAPI.txt         # 可搜索的 API 参考文档
    └── jq_search.py             # Python 搜索脚本
```

## 适用人群

- **量化研究员**：快速查阅 API 规范，减少文档切换
- **AI Agent 开发者**：为 Agent 添加强大的金融 API 查询能力
- **量化教学**：作为 AI + 量化投资的实践案例

## 官方参考

- JoinQuant API 文档：https://www.joinquant.com/view/user/floor?type=mainFloor
- JoinQuant 官网：https://www.joinquant.com

## 限制与免责

- 本工具整理和索引了 JoinQuant 官方 API 文档，不对 API 内容本身负责
- JoinQuant 平台 API 可能随时更新，建议定期检查官方文档
- ♠ 标记基于文档编写时的理解，实际使用请以官方文档为准

## License

MIT License — 可自由使用、修改和分发。

---

*如果你觉得这个工具有帮助，欢迎 ⭐ Star！*

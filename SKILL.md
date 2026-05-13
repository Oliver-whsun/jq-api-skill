---
name: jq-api
description: JoinQuant (聚宽) 量化交易平台 API 参考工具。当需要查询聚宽平台函数用法、编写量化策略、进行回测参数配置时使用。支持中英文关键词搜索、自动标注回测专用 API。
trigger:
  - JoinQuant
  - 聚宽
  - 量化策略
  - 回测
  - get_bars
  - attribute_history
  - order
  - jqdata
  - 资金流向
  - get_price
---

# JoinQuant API 查询工具 (jq-api)

Agent 的聚宽量化平台 API 参考工具。所有内容来源于 JoinQuant 官方 API 文档，支持中英文关键词搜索，返回函数签名、参数说明、示例代码和官方文档链接。

## 文件结构

```
jq-api/
├── SKILL.md                          ← 本文件（Skill 定义）
├── README.md                         ← 使用说明
├── LICENSE                           ← MIT License
└── references/
    ├── JoinQuantAPI.txt              ← 可搜索的 API 参考文档（UTF-8）
    └── jq_search.py                  ← Python 搜索脚本
```

## 安装

### 方式一：npx skills（推荐）

```bash
npx skills add sunweiheng/jq-api-skill
```

### 方式二：手动安装

```bash
# 克隆仓库
git clone https://github.com/sunweiheng/jq-api-skill.git
# 将文件放入 Agent 的 skills 目录
```

## 核心工具：jq_search.py

> ⚠️ **重要**：在某些终端环境下，直接用 `grep` 搜索会导致中文显示为乱码。
> **必须使用 `jq_search.py` 脚本**进行搜索，该脚本通过 Python 文件读取正确渲染 UTF-8 中文。

### 基本用法

```bash
# 安装依赖（仅 Python 3）
# 无需安装任何第三方包

# 单关键词搜索
python3 jq_search.py get_bars

# 多关键词 OR 搜索
python3 jq_search.py order_target order_value

# 带上下文（-c 指定上下文行数）
python3 jq_search.py 资金流向 -c 5

# 只显示 ♠ 回测专用 API（见下方说明）
python3 jq_search.py 历史 --backtest-only

# 输出到文件
python3 jq_search.py get_price -o /tmp/jq_out.txt

# 查看完整选项
python3 jq_search.py --help
```

### 输出示例

```
╔══════════════════════════════════════════════════════════════════════════════════════╗
║  JoinQuant API 搜索结果                                                          ║
║  关键词: 『get_bars』                                                                   ║
║  命中行数: 4  条                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════════════╝

─────────────────────────────────────────────────────────────────────────────────────────
  📄 第 35 页 (文件行 1181)
─────────────────────────────────────────────────────────────────────────────────────────

  ⚡ get_bars ♠ — 获取历史数据
     位置: 行 1181 | 第 35 页
     命中: get_bars
     └ get_bars(security, count, unit='1d',
     └ fields=['date', 'open','high','low','close'],
     └ include_now=False)
     └ 回测环境/模拟专用API

═════════════════════════════════════════════════════════════════════════════════════════
  👉 官方文档: https://www.joinquant.com/view/user/floor?type=mainFloor
═════════════════════════════════════════════════════════════════════════════════════════
```

## ♠ 回测专用 API 标记

文档中用 **♠（U+2660）** 标记的函数为 **"回测环境/模拟" 专用 API**，不可在研究模块中调用。

已知 ♠ 标记 API：

| API | 说明 |
|-----|------|
| `history` | 获取历史数据 |
| `attribute_history` | 获取历史数据（带字段） |
| `get_current_data` | 获取当前时间数据 |
| `get_bars` | 获取历史 bar 数据 |
| `run_daily` 等 | 定时运行函数 |
| `record` | 画图记录 |
| `发送自定义消息` | 自定义消息推送 |
| `性能分析` | 性能分析工具 |

## 常见搜索场景

| 需求 | 命令 |
|-----|------|
| 查询历史行情 | `jq_search.py get_bars` 或 `jq_search.py get_price` |
| 下单交易 | `jq_search.py order_target order_value` |
| 资金流向数据 | `jq_search.py 资金流向 -c 5` |
| 技术指标 | `jq_search.py MA MACD RSI` |
| 持仓信息 | `jq_search.py position 持仓 portfolio` |
| 回测配置 | `jq_search.py set_benchmark set_option` |
| 定时运行 | `jq_search.py run_daily 定时` |
| 融资融券 | `jq_search.py margincash marginsec` |
| 财务因子 | `jq_search.py get_fundamentals query` |

## Agent 输出规范

找到 API 后，输出应包含：

1. **函数签名** — 函数名、完整参数列表
2. **♠ 标记** — 确认是否为回测专用
3. **PDF 页码** — 告知用户在原文档第几页
4. **参数说明** — 类型、含义、默认值
5. **示例代码** — 官方示例
6. **注意事项** — 使用限制、常见错误

## 禁止行为

- **严禁编造 API**：搜索不到时明确告知，不要凭空生成函数
- **严禁使用未来函数**：如 `current_price` 不可用于获取未来数据
- **信息来源**：所有内容必须来自官方文档

## 官方参考

- API 文档：https://www.joinquant.com/view/user/floor?type=mainFloor
- JoinQuant 官网：https://www.joinquant.com

## 数据来源

- `JoinQuantAPI.txt` 由 JoinQuant 官方 PDF 文档提取
- PDF 原版请访问 JoinQuant 官方渠道获取
- 本 skill 仅整理和索引，不对 API 内容本身负责

## License

MIT License — 可自由使用、修改和分发。

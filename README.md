# jq-api

**JoinQuant（聚宽）量化平台 API 查询工具 — 让 AI Agent 准确使用聚宽函数，不再瞎猜。**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

---

## 问题：AI 总是"幻觉"出根本不存在的聚宽函数

当你在 AI Agent 里写聚宽量化策略时，Agent 经常：
- 把 `get_bars` 拼成 `get_historical_bars`
- 把 `order_target` 的参数顺序搞错
- 在**研究模块**里调用只有**回测才能用**的函数
- 完全编造一个聚宽根本没提供的函数

这是因为 Agent 的训练数据里没有完整、准确的聚宽 API 文档。

---

## 解决：jq-api

本工具将 JoinQuant 官方 API 文档（102 页）整理为可搜索的参考库，供 AI Agent 在编写策略时实时查询。

**安装后，Agent 会自动：**
1. 当你提到"聚宽"、"get_bars"、"回测"等关键词时，加载本工具
2. 在文档中搜索你需要的函数
3. 返回准确的函数签名、参数说明、示例代码
4. 标注哪些是"回测专用 API"（♠ 标记），防止在研究模块误用

---

## 核心功能

| 功能 | 说明 |
|------|------|
| **准确查询** | 所有内容来自 JoinQuant 官方 PDF 文档，不靠 Agent 记忆 |
| **中英文搜索** | 直接搜 `get_bars`，也可以搜 `资金流向`、`均线` |
| **♠ 标记** | 自动标注回测/模拟专用 API，防止误用 |
| **页码索引** | 搜索结果标注 PDF 页码，可快速溯源 |
| **零依赖** | 纯 Python 3，无需安装任何第三方包 |

---

## 安装

```bash
# 通过 skills CLI（适用于 Claude Code、Cursor 等）
npx skills add sunweiheng/jq-api-skill

# 或手动克隆到 Agent 的 skills 目录
git clone https://github.com/sunweiheng/jq-api-skill.git
```

---

## 使用效果示例

**问 Agent：** "用 get_bars 获取平安银行最近 20 天的日线数据"

**没有 jq-api：** Agent 可能编一个错误的函数，或者参数顺序全错。

**有 jq-api：** Agent 查到：

```
⚡ get_bars ♠ — 获取历史数据
   位置: 行 1181 | 第 35 页

参数:
  security: 股票代码
  count: 大于0的整数，表示获取bar的个数
  unit: bar的时间单位，支持 '1m','5m','15m','30m','60m','120m','1d','1w','1M'
  fields: 'date','open','close','high','low','volume','money'
  include_now: 是否包含当前bar

示例:
  array = get_bars('000001.XSHG', 20, unit='1d',
                    fields=['open','close','high','low'],
                    include_now=False)
  array['close']

⚠ 注意: ♠ 是回测/模拟专用 API，不能在研究模块调用
```

---

## 支持的场景

| 你想做的事 | Agent 会查到的函数 |
|-----------|-----------------|
| 获取历史 K 线数据 | `get_bars`、`get_price`、`history` |
| 下单买卖 | `order`、`order_target`、`order_value` |
| 查资金流向/主力动向 | `jqdata.get_money_flow` |
| 均线、MACD 等技术指标 | `mavg`、`stddev`（在 SecurityUnitData 上） |
| 设置回测基准 | `set_benchmark`、`set_option` |
| 定时运行策略 | `run_daily`、`run_weekly` |
| 融资融券操作 | `margincash_open`、`marginsec_close` 等 |
| 财务因子选股 | `get_fundamentals`、`query` |

---

## 文件结构

```
jq-api/
├── SKILL.md                      # Agent 使用说明（含触发词、搜索规范）
├── README.md                     # 本文件
├── LICENSE                      # MIT
└── references/
    ├── JoinQuantAPI.txt         # 官方 API 参考文档（可直接用文本工具搜索）
    └── jq_search.py             # Python 搜索脚本（推荐用这个）
```

---

## 数据来源

- `JoinQuantAPI.txt` 由 JoinQuant 官方 PDF 文档提取
- JoinQuant 官方文档：https://www.joinquant.com/view/user/floor?type=mainFloor
- 本工具仅整理和索引，不对 API 内容本身负责

---

## License

MIT — 可自由使用、修改和分发。

---

*觉得有帮助？请 ⭐ Star！*

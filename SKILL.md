---
name: jq-api
description: 聚宽量化平台API规范查询工具。当用户需要编写聚宽量化策略、查询聚宽API用法、查找聚宽平台函数时触发。覆盖聚宽平台的API文档搜索、函数查询、策略编写规范等场景。
trigger:
  - 聚宽
  - JoinQuant
  - 量化策略
  - 回测
  - 聚宽API
  - attribute_history
  - get_bars
  - order
  - 聚宽函数
  - 量化API
  - 聚宽平台
  - jqdata
---

# 聚宽API规范查询工具

本 skill 提供聚宽量化平台 API 的准确查询，所有信息来源于官方 API 文档（PDF 提取）。

## 文档结构

```
jq-api/
├── SKILL.md                          ← 本文件
├── references/
│   ├── JoinQuantAPI.txt              ← TXT 搜索版（由 PDF 提取，102 页，3651 行）
│   └── jq_search.py                  ← Python 搜索脚本（推荐使用）
```

## 核心工具：Python 搜索脚本

> ⚠️ **重要**：直接使用 `grep` 在某些环境下会导致中文显示为乱码。**必须使用 `jq_search.py` 脚本**进行搜索，该脚本通过文件读取而非管道输出，正确渲染 UTF-8 中文内容。

### 基本用法

```bash
# 单关键词
python3 references/jq_search.py get_bars

# 多关键词（OR 关系）
python3 references/jq_search.py order_target order_value

# 带上下文（-c 指定上下文的行数，默认 3）
python3 references/jq_search.py 资金流向 -c 5

# 只显示 ♠ 回测专用 API（见下文"♠ 标记说明"）
python3 references/jq_search.py 历史 --backtest-only

# 输出到文件
python3 references/jq_search.py get_price -o /tmp/jq_out.txt

# 完整选项
python3 references/jq_search.py --help
```

### jq_search.py 输出内容

每次搜索自动提供：
- **关键词和命中条数**（表头）
- **按页分组**（每页标注 PDF 页码 + 文件行号）
- **API 定义行高亮**（函数名、签名、描述）
- **上下文行**（参数说明、示例代码等）
- **♠ 标记**（回测/模拟专用 API 专用标记）
- **底部官方链接**

## ♠ 标记说明

文档中用 **♠（黑桃符号，U+2660）** 标记的 API 是 **"回测环境/模拟" 专用 API**，不能在研究模块中调用。

已知 ♠ 标记 API：
- `history`
- `attribute_history`
- `get_current_data`
- `get_bars`
- `定时运行`（run_daily 等）
- `取消所有定时运行`
- `record`（画图）
- `发送自定义消息`
- `性能分析`

## 搜索策略

1. **精确搜索**：用用户提到的精确函数名（如 `get_bars`）
2. **中文关键词**：直接用中文（如 `资金流向`、`均线`）
3. **多关键词组合**：适用于同时涉及多个概念的场景
4. **回测专用筛选**：加上 `--backtest-only` 过滤只关心回测 API 的场景
5. **扩大上下文**：命中结果不清晰时，用 `-c 5` 或 `-c 10` 查看更多上下文

## 常见搜索场景

| 用户需求 | 搜索命令 | 说明 |
|---------|---------|------|
| 查询历史行情 | `jq_search.py get_bars` 或 `jq_search.py get_price` | 数据获取函数 |
| 下单交易 | `jq_search.py order_target order_value` | 交易函数 |
| 获取资金流向 | `jq_search.py 资金流向 -c 5` | `jqdata.get_money_flow` |
| 技术指标 | `jq_search.py MA MACD RSI` | 技术指标 |
| 持仓信息 | `jq_search.py position 持仓 portfolio` | 持仓相关 |
| 回测配置 | `jq_search.py set_benchmark set_option` | 回测参数 |
| 定时运行 | `jq_search.py run_daily 定时` | 定时执行 |
| 融资融券 | `jq_search.py margincash marginsec` | 两融专用 |
| A股基础面 | `jq_search.py get_fundamentals query` | 财务因子 |

## 输出规范

当找到相关 API 后，输出应包含：

1. **函数签名** — 函数名、完整参数列表
2. **♠ 标记** — 确认是否为回测专用
3. **页码** — 告知用户在 PDF 第几页可查阅原版
4. **上下文** — 上下文中通常包含参数说明、返回值、示例代码
5. **注意事项** — 使用限制、常见错误

## 官方网页参考

当 TXT 文档搜索无结果或需要最新 API 时，访问官方文档页面：

**https://www.joinquant.com/view/user/floor?type=mainFloor**

使用 WebFetch 工具获取最新内容。

## 禁止行为

- **严禁编造 API**：搜索不到时明确告知，不要凭空生成函数
- **严禁使用未来函数**：如 `current_price` 不可用于获取未来数据
- **信息来源**：所有内容必须来自官方文档，不得臆测

## 错误处理

搜索无结果时的处理顺序：
1. 尝试同义词搜索（如 `资金流向` 无结果 → `主力资金` → `大单`）
2. 检查函数名拼写
3. 告知用户"未找到相关 API，建议访问官方页面查询"
4. 输出官方文档链接

## 更新维护

- 聚宽 API 更新时，需重新从 PDF 提取内容到 TXT
- 定期检查官方网页是否有新增 API
- 如发现 TXT 有遗漏，手动补充对应行号位置

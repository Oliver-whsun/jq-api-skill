#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JoinQuant API 搜索工具
======================
用法:
  python3 jq_search.py <关键词> [关键词2 ...] [选项]

示例:
  python3 jq_search.py get_bars
  python3 jq_search.py order_target 订单
  python3 jq_search.py 资金流向 --context 5
  python3 jq_search.py get_price --page 1
  python3 jq_search.py MACD RSI --backtest-only
"""

import sys
import os
import re
import argparse

SKILL_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TXT_PATH = os.path.join(SKILL_ROOT, 'references', 'JoinQuantAPI.txt')

# ═══════════════════════════════════════════════════════════════
# 核心：构建页码索引
# ═══════════════════════════════════════════════════════════════

def build_page_index(lines):
    """构建 (页码 → 行号) 和 (行号 → 页码) 的双向索引"""
    page_to_line = []
    line_to_page = {}

    for i, line in enumerate(lines):
        if line.startswith('===') and '第' in line and '页' in line:
            m = re.search(r'第\s*(\d+)\s*页', line)
            if m:
                page_to_line.append((int(m.group(1)), i))

    for p_idx in range(len(page_to_line)):
        pn, start_line = page_to_line[p_idx]
        end_line = page_to_line[p_idx + 1][1] if p_idx + 1 < len(page_to_line) else len(lines)
        for l in range(start_line, end_line):
            line_to_page[l] = pn

    return page_to_line, line_to_page

# ═══════════════════════════════════════════════════════════════
# 核心：搜索逻辑
# ═══════════════════════════════════════════════════════════════

def search_keyword(lines, keyword, case_sensitive=False):
    """
    在所有行中搜索关键词，返回匹配行列表
    每个元素: (行号, 行内容, 匹配位置列表)
    """
    results = []
    k = keyword if case_sensitive else keyword.lower()
    for i, line in enumerate(lines):
        l = line if case_sensitive else line.lower()
        positions = []
        start = 0
        while True:
            pos = l.find(k, start)
            if pos == -1:
                break
            positions.append(pos)
            start = pos + 1
        if positions:
            results.append((i, line.rstrip('\n'), positions))
    return results


def get_context(lines, center_line, before=3, after=3):
    """获取上下文行"""
    start = max(0, center_line - before)
    end = min(len(lines), center_line + after + 1)
    return [(i, lines[i].rstrip('\n')) for i in range(start, end)]


def format_highlight(line, positions, keyword, width=80):
    """
    在行内容中高亮关键词
    positions: 匹配位置列表
    """
    if not positions:
        return line[:width]

    # 构建带高亮的行
    chars = list(line)
    # 从后往前替换，避免位置偏移问题
    for pos in reversed(positions):
        end = min(pos + len(keyword), len(chars))
        # 用「」包裹
        chars[pos] = '\033[92m『\033[0m'
        if end <= len(chars):
            chars[end - 1] = '\033[92m』\033[0m'

    result = ''.join(chars)
    if len(result) > width:
        # 找到第一个高亮位置，截取窗口
        first_marker = result.find('\033[92m')
        if first_marker > width // 2:
            result = '...' + result[first_marker - width // 2:]
        result = result[:width] + '...'

    return result


def is_backtest_only(line):
    """检查行是否标记为回测专用（包含♠）"""
    return '\u2660' in line  # U+2660 BLACK SPADE SUIT


def detect_api_name(line):
    """
    从行中提取 API 函数名（如果这行是 API 定义）
    例如: "get_bars ♠ - 获取历史数据" → "get_bars"
    """
    stripped = line.strip()
    # 匹配模式: "api_name ♠? - 描述"
    m = re.match(r'^([\w_]+)\s*[\u2660]?\s*-\s*(.+)$', stripped)
    if m:
        return m.group(1), m.group(2)
    return None, None


# ═══════════════════════════════════════════════════════════════
# 主搜索函数
# ═══════════════════════════════════════════════════════════════

def search(keywords, context_lines=3, show_page=True, backtest_only=False,
           output_file=None, width=120):
    """
    主搜索入口

    keywords: 关键词列表（OR 关系）
    context_lines: 上下文中包含多少行
    show_page: 是否显示页码
    backtest_only: 是否只显示回测专用 API
    """
    # 读取文件
    try:
        with open(TXT_PATH, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
        lines = content.split('\n')
    except Exception as e:
        msg = f"[ERROR] 无法读取文件: {TXT_PATH}\n  {e}"
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(msg)
        print(msg)
        return

    # 构建页码索引
    page_to_line, line_to_page = build_page_index(lines)

    # 收集所有关键词命中的行号（去重、排序）
    all_hit_lines = set()
    keyword_hits = {}  # line_num -> {keyword: [positions]}

    for kw in keywords:
        hits = search_keyword(lines, kw)
        for (line_num, line_content, positions) in hits:
            if line_num not in keyword_hits:
                keyword_hits[line_num] = {}
            keyword_hits[line_num][kw] = positions
            all_hit_lines.add(line_num)

    if not all_hit_lines:
        msg = f"[未找到] 关键词: {' | '.join(keywords)}\n  请尝试:\n  1. 换用同义词/近义词搜索\n  2. 访问官网查询: https://www.joinquant.com/view/user/floor?type=mainFloor"
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(msg)
        print(msg)
        return

    # 过滤回测专用
    if backtest_only:
        all_hit_lines = {ln for ln in all_hit_lines if is_backtest_only(lines[ln])}

    sorted_lines = sorted(all_hit_lines)

    # 生成输出
    output_parts = []
    sep = '═' * width

    # 标题
    kw_str = ' × '.join(f'『{k}』' for k in keywords)
    output_parts.append(f"\n{'╔'}{sep}{'╗'}")
    output_parts.append(f"{'║'}  JoinQuant API 搜索结果{' ' * (width - 28 - len(kw_str))}{'║'}")
    output_parts.append(f"{'║'}  关键词: {kw_str}{' ' * (width - 16 - len(kw_str))}{'║'}")
    total_count = len(sorted_lines)
    output_parts.append(f"{'║'}  命中行数: {total_count}  条{' ' * (width - 22 - len(str(total_count)))}{'║'}")
    if backtest_only:
        output_parts.append(f"{'║'}  ♠ 仅显示回测/模拟专用 API{' ' * (width - 32)}{'║'}")
    output_parts.append(f"{'╚'}{sep}{'╝'}")

    # 分组输出
    current_page = None
    for line_num in sorted_lines:
        line_content = lines[line_num]
        page = line_to_page.get(line_num, '?')

        # 页码分隔
        if show_page and page != current_page:
            current_page = page
            output_parts.append(f"\n{'─' * width}")
            output_parts.append(f"  📄 第 {page} 页 (文件行 {line_num})")
            output_parts.append(f"{'─' * width}")

        # 行号
        page_info = f"[行{line_num}]" if not show_page else f"[行{line_num}]"
        bo_marker = ' ♠' if is_backtest_only(line_content) else ''

        # 查找该行的所有关键词高亮
        highlights = []
        for kw in keywords:
            if kw in keyword_hits.get(line_num, {}):
                # 简化：直接显示关键词，不做复杂高亮
                highlights.append(kw)

        # 检测是否为 API 定义行
        api_name, api_desc = detect_api_name(line_content)

        # 上下文
        ctx_before = get_context(lines, line_num, before=context_lines, after=0)
        ctx_after = get_context(lines, line_num, before=0, after=context_lines)

        # 输出该条结果
        if api_name:
            # API 定义行，格式化输出
            output_parts.append(f"\n  ⚡ {api_name}{bo_marker} — {api_desc}")
            output_parts.append(f"     位置: 行 {line_num}" + (f" | 第 {page} 页" if show_page else ""))
            output_parts.append(f"     命中: {', '.join(highlights)}")
        else:
            # 普通行
            display_line = line_content[:width - 20]
            if len(line_content) > width - 20:
                display_line += '...'
            output_parts.append(f"\n  {page_info}{bo_marker} {display_line}")
            output_parts.append(f"     命中: {', '.join(highlights)}")

        # 上下文（before）
        for ctx_line_num, ctx_content in ctx_before:
            if ctx_line_num != line_num:
                trimmed = ctx_content.strip()[:width - 25]
                if trimmed:
                    output_parts.append(f"     └ {trimmed}")

        # 上下文（after）
        for ctx_line_num, ctx_content in ctx_after:
            if ctx_line_num != line_num:
                trimmed = ctx_content.strip()[:width - 25]
                if trimmed:
                    output_parts.append(f"     └ {trimmed}")

    # 底部信息
    output_parts.append(f"\n{'═' * width}")
    output_parts.append(f"  👉 官方文档: https://www.joinquant.com/view/user/floor?type=mainFloor")
    output_parts.append(f"  📖 PDF 原版: ~/.workbuddy/skills/jq-api/references/JoinQuantAPI.pdf")
    output_parts.append(f"{'═' * width}\n")

    final_output = '\n'.join(output_parts)

    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(final_output)
        print(f"[输出] 结果已保存到: {output_file}")
    else:
        print(final_output)


# ═══════════════════════════════════════════════════════════════
# CLI 入口
# ═══════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description='JoinQuant API 搜索工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 jq_search.py get_bars
  python3 jq_search.py order_target 订单
  python3 jq_search.py 资金流向 --context 5
  python3 jq_search.py MACD RSI --backtest-only
  python3 jq_search.py get_price --page 1 -o /tmp/jq_out.txt
        """
    )
    parser.add_argument('keywords', nargs='+', help='搜索关键词（支持多个，OR 关系）')
    parser.add_argument('-c', '--context', type=int, default=3, help='上下文行数（默认 3）')
    parser.add_argument('-o', '--output', default=None, help='输出到文件')
    parser.add_argument('--no-page', action='store_true', help='不显示页码')
    parser.add_argument('--backtest-only', action='store_true', help='只显示 ♠ 回测专用 API')
    parser.add_argument('-w', '--width', type=int, default=120, help='行宽度（默认 120）')

    args = parser.parse_args()

    search(
        keywords=args.keywords,
        context_lines=args.context,
        show_page=not args.no_page,
        backtest_only=args.backtest_only,
        output_file=args.output,
        width=args.width
    )


if __name__ == '__main__':
    main()

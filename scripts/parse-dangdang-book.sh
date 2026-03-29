#!/usr/bin/env bash
# 从当当商品页解析书名、ISBN、出版时间、封面 URL，并提示下载封面命令。
# 实现见 parse_dangdang_book.py（Python3 + GB18030 解码，避免编码问题）
# 用法: ./scripts/parse-dangdang-book.sh 'https://product.dangdang.com/11940082472.html'
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
exec python3 "$ROOT/scripts/parse_dangdang_book.py" "${1:?请传入当当商品页 URL}"

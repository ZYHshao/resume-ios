#!/usr/bin/env python3
"""从当当商品页解析：书名（prodSpuInfo）、ISBN、出版时间、封面大图 URL。"""
from __future__ import annotations

import json
import re
import sys
import urllib.request

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"


def fetch(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        raw = r.read()
    return raw.decode("gb18030", errors="replace")


def main() -> int:
    if len(sys.argv) < 2:
        print("用法: python3 scripts/parse_dangdang_book.py 'https://product.dangdang.com/xxxx.html'", file=sys.stderr)
        return 1
    url = sys.argv[1].strip()
    html = fetch(url)

    m_spu = re.search(r"var\s+prodSpuInfo\s*=\s*(\{[^;]+)\s*;", html)
    title = ""
    if m_spu:
        try:
            data = json.loads(m_spu.group(1))
            title = str(data.get("productName") or "")
        except json.JSONDecodeError:
            title = ""

    m_isbn = re.search(r"国际标准书号ISBN[：:]([0-9]{10,17})", html)
    isbn = m_isbn.group(1) if m_isbn else ""
    if not isbn:
        m_isbn2 = re.search(r"978[0-9]{10}", html)
        isbn = m_isbn2.group(0) if m_isbn2 else ""

    m_pub = re.search(r"出版时间:([0-9]{4}年[0-9]{1,2}月)", html)
    pub = m_pub.group(1) if m_pub else ""

    m_cover = re.search(
        r'src="//(img3m[0-9]+\.ddimg\.cn/[0-9]+/[0-9]+/[0-9]+-1_w_[^"]+)"',
        html,
    )
    cover = f"https://{m_cover.group(1)}" if m_cover else ""

    # 去掉当当标题里的营销尾缀
    for suffix in ("【正版】", "【正版图书", "正版】"):
        if suffix in title:
            title = title.split(suffix)[0].strip()
            break
    title = title.rstrip("】").strip()

    print("书名:", title or "（见 prodSpuInfo productName）")
    print("ISBN:", isbn or "（未匹配）")
    print("出版时间:", pub or "（未匹配）")
    print("封面:", cover or "（未匹配）")
    if cover and isbn:
        print()
        print("下载封面:")
        print(f"  curl -sL -A '{UA[:40]}…' '{cover}' -o images/book-{isbn}-cover.jpg")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Tells IndexNow search engines (Bing, which feeds ChatGPT search and Copilot, plus Naver, Yandex
and others) that the pages in sitemap.xml changed, so they recrawl without waiting.

    python3 tools/seo/indexnow.py            # submit every URL in sitemap.xml
    python3 tools/seo/indexnow.py --dry-run  # print what would be sent

The key is the *.txt file at the site root whose name equals its content; it must be live at
https://contrl.ai/<key>.txt, so run this after a deploy. Never fails the caller: errors are printed.
"""
import json
import re
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HOST = 'contrl.ai'
ENDPOINTS = ['https://api.indexnow.org/indexnow', 'https://searchadvisor.naver.com/indexnow']


def find_key():
    for f in ROOT.glob('*.txt'):
        if re.fullmatch(r'[0-9a-f]{32}', f.stem) and f.read_text().strip() == f.stem:
            return f.stem
    sys.exit('no IndexNow key file (<32 hex>.txt containing its own name) at the site root')


def main():
    key = find_key()
    urls = re.findall(r'<loc>([^<]+)</loc>', (ROOT / 'sitemap.xml').read_text(encoding='utf-8'))
    urls = [u for u in urls if u.startswith(f'https://{HOST}/') and '/images/' not in u and not u.endswith('.png')]
    body = json.dumps({'host': HOST, 'key': key, 'keyLocation': f'https://{HOST}/{key}.txt', 'urlList': urls}).encode()
    if '--dry-run' in sys.argv:
        print(body.decode())
        return
    for ep in ENDPOINTS:
        req = urllib.request.Request(ep, data=body, headers={'Content-Type': 'application/json; charset=utf-8'})
        try:
            with urllib.request.urlopen(req, timeout=20) as r:
                print(ep, r.status, len(urls), 'urls')
        except Exception as e:  # noqa: BLE001 — a ping must never break a deploy
            print(ep, 'failed:', e)


if __name__ == '__main__':
    main()

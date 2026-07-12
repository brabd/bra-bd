# -*- coding: utf-8 -*-
"""IndexNow ping — sitemap-এর সব URL Bing/Yandex-কে জানায়।"""
import json, re, io, urllib.request

KEY = 'a3c9f1e2b8d4470f9a61c5e7d2b34f88'
HOST = 'bra.bd'
sm = io.open('site/sitemap.xml', encoding='utf-8').read()
urls = re.findall(r'<loc>([^<]+)</loc>', sm)
payload = json.dumps({'host': HOST, 'key': KEY,
    'keyLocation': f'https://{HOST}/{KEY}.txt', 'urlList': urls}).encode()
req = urllib.request.Request('https://api.indexnow.org/indexnow', data=payload,
    headers={'Content-Type': 'application/json; charset=utf-8'})
try:
    r = urllib.request.urlopen(req, timeout=30)
    print('IndexNow:', r.status, len(urls), 'urls')
except Exception as e:
    print('IndexNow failed (non-fatal):', e)

#!/usr/bin/env python3
"""
老黄历页面保活脚本
定期访问托管页面，防止 Pages 实例因长时间无人访问而休眠
"""
import urllib.request
import json
import sys
import time
import gzip
import io

URL = "https://bqdbrsyb57.page.coze.site"

def check_page():
    """访问页面，检查是否返回 200"""
    try:
        req = urllib.request.Request(URL, headers={
            "User-Agent": "Mozilla/5.0 (compatible; KeepAlive/1.0)",
            "Accept-Encoding": "gzip"
        })
        start = time.time()
        resp = urllib.request.urlopen(req, timeout=30)
        elapsed = round((time.time() - start) * 1000)
        status = resp.getcode()
        
        raw = resp.read()
        if resp.headers.get("Content-Encoding") == "gzip":
            raw = gzip.decompress(raw)
        body = raw.decode("utf-8", errors="ignore")
        
        result = {
            "status": status,
            "elapsed_ms": elapsed,
            "url": URL,
            "ok": status == 200 and "老黄历" in body
        }
        print(json.dumps(result, ensure_ascii=False))
        return result["ok"]
    except Exception as e:
        result = {
            "status": -1,
            "error": str(e),
            "url": URL,
            "ok": False
        }
        print(json.dumps(result, ensure_ascii=False))
        return False

if __name__ == "__main__":
    ok = check_page()
    sys.exit(0 if ok else 1)

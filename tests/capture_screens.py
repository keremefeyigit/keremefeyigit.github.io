#!/usr/bin/env python3
"""Başarısızlık anında inceleme için ekran görüntüleri: python3 tests/capture_screens.py <klasör>"""
import sys
import threading
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
out = Path(sys.argv[1] if len(sys.argv) > 1 else "shots"); out.mkdir(parents=True, exist_ok=True)
srv = ThreadingHTTPServer(("127.0.0.1", 0), partial(SimpleHTTPRequestHandler, directory=str(ROOT)))
threading.Thread(target=srv.serve_forever, daemon=True).start()
base = f"http://127.0.0.1:{srv.server_address[1]}"
with sync_playwright() as p:
    b = p.chromium.launch()
    for lang, path in (("tr", "/"), ("en", "/en/")):
        for scheme in ("light", "dark"):
            for w, h in ((360, 800), (820, 1100), (1440, 900)):
                ctx = b.new_context(viewport={"width": w, "height": h}, color_scheme=scheme, reduced_motion="reduce")
                pg = ctx.new_page(); pg.goto(base + path, wait_until="networkidle")
                pg.screenshot(path=str(out / f"{lang}-{scheme}-{w}.png"), full_page=True); ctx.close()
    b.close()
srv.shutdown()
print("ekran görüntüleri:", out)

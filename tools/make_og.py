#!/usr/bin/env python3
"""assets/img/og.png üretir (1200x630). Gereksinim: pip install playwright && playwright install chromium"""
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1200, "height": 630})
    pg.goto((ROOT / "tools" / "og.html").as_uri())
    pg.wait_for_timeout(500)
    pg.screenshot(path=str(ROOT / "assets" / "img" / "og.png"))
    b.close()
print("assets/img/og.png yazıldı")

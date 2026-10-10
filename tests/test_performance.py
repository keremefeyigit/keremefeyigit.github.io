"""Performans bütçesi (yerel sunucuda deterministik ölçümler): istek sayısı, aktarım boyutu, CLS, LCP, render engelleme."""
import re
import urllib.request

import pytest


def measure(page):
    return page.evaluate("""() => new Promise(resolve => {
      let cls = 0, lcp = 0;
      new PerformanceObserver(l => { for (const e of l.getEntries()) if (!e.hadRecentInput) cls += e.value; }).observe({ type: 'layout-shift', buffered: true });
      new PerformanceObserver(l => { for (const e of l.getEntries()) lcp = Math.max(lcp, e.startTime); }).observe({ type: 'largest-contentful-paint', buffered: true });
      setTimeout(() => resolve({ cls, lcp }), 600);
    })""")


@pytest.mark.parametrize("lang", ["tr", "en"])
def test_first_load_budget(browser, base_url, lang):
    ctx = browser.new_context(viewport={"width": 390, "height": 800}, reduced_motion="no-preference")
    page = ctx.new_page()
    sizes = []
    page.on("response", lambda r: sizes.append((r.url, len(r.body()) if r.ok else 0)))
    page.goto(base_url + ("/" if lang == "tr" else "/en/"), wait_until="networkidle")
    page.wait_for_timeout(500)
    total = sum(s for _, s in sizes)
    assert len(sizes) <= 14, [u for u, _ in sizes]
    assert total <= 300_000, f"ilk yükleme {total} bayt"
    m = measure(page)
    assert m["cls"] <= 0.05, m
    assert m["lcp"] <= 2500, m
    ctx.close()


def test_only_needed_font_subsets_load(browser, base_url):
    """unicode-range sayesinde yalnızca kullanılan alt kümeler yüklenir (Türkçe: latin + latin-ext)."""
    ctx = browser.new_context(viewport={"width": 1280, "height": 800}); page = ctx.new_page()
    fonts = []
    page.on("request", lambda r: fonts.append(r.url) if r.url.endswith(".woff2") else None)
    page.goto(base_url + "/", wait_until="networkidle"); page.wait_for_timeout(300)
    assert 2 <= len(fonts) <= 8, fonts
    ctx.close()


def test_scripts_do_not_block_rendering(base_url):
    html = urllib.request.urlopen(base_url + "/").read().decode()
    scripts = re.findall(r"<script\b([^>]*)>", html)
    blocking = [s for s in scripts if "src=" in s and "defer" not in s and "async" not in s and "theme.js" not in s]
    assert not blocking, blocking  # yalnızca küçük theme.js senkron (tema titremesini önler)


def test_css_is_single_stylesheet_and_fonts_are_preloaded(base_url):
    html = urllib.request.urlopen(base_url + "/").read().decode()
    assert html.count('rel="stylesheet"') == 1
    assert 'rel="preload"' in html and "fraunces-latin-wght-normal.woff2" in html

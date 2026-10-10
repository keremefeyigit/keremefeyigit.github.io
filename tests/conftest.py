"""Ortak test altyapısı: siteyi yerel bir HTTP sunucusuyla (dış ağ yok) sunar, Playwright ile açar."""
import socket
import subprocess
import threading
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
PAGES = {"tr": "/", "en": "/en/"}
WIDTHS = [320, 360, 390, 768, 1024, 1280, 1440, 1920]


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *a):  # test çıktısını kirletme
        pass

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def send_error(self, code, message=None, explain=None):
        # GitHub Pages gibi: bilinmeyen yolda 404.html göster
        if code == 404:
            body = (ROOT / "404.html").read_bytes()
            self.send_response(404)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        super().send_error(code, message, explain)


@pytest.fixture(scope="session")
def base_url():
    sock = socket.socket(); sock.bind(("127.0.0.1", 0)); port = sock.getsockname()[1]; sock.close()
    server = ThreadingHTTPServer(("127.0.0.1", port), partial(QuietHandler, directory=str(ROOT)))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    yield f"http://127.0.0.1:{port}"
    server.shutdown()


@pytest.fixture(scope="session")
def browser():
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch()
        yield b
        b.close()


@pytest.fixture
def open_page(browser, base_url):
    """open_page(lang, width, height, scheme, reduced_motion=True, js=True) -> (page, errors, requests)"""
    opened = []

    def _open(lang="tr", width=1280, height=900, scheme="light", reduced_motion=True, js=True, path=None, bypass_csp=False):
        ctx = browser.new_context(viewport={"width": width, "height": height}, color_scheme=scheme,
                                  reduced_motion="reduce" if reduced_motion else "no-preference",
                                  java_script_enabled=js, bypass_csp=bypass_csp)
        opened.append(ctx)
        page = ctx.new_page()
        errors, requests = [], []
        page.on("console", lambda m: errors.append(f"{m.type}: {m.text[:160]}") if m.type in ("error", "warning") else None)
        page.on("pageerror", lambda e: errors.append(f"pageerror: {str(e)[:160]}"))
        page.on("requestfailed", lambda r: errors.append(f"requestfailed: {r.url}"))
        page.on("request", lambda r: requests.append(r.url))
        page.goto(base_url + (path or PAGES[lang]), wait_until="networkidle")
        if js:
            page.evaluate("document.fonts.ready")
        return page, errors, requests

    yield _open
    for c in opened:
        c.close()


def read(rel):
    return (ROOT / rel).read_text(encoding="utf-8")


def html_files():
    return ["index.html", "en/index.html", "404.html"]


def tracked_files():
    out = subprocess.run(["git", "ls-files"], cwd=ROOT, capture_output=True, text=True).stdout.split("\n")
    return [f for f in out if f]

"""Güvenlik testleri: katı CSP, satır içi kod yok, sır yok, izlenmemesi gereken dosya yok, iş akışı en az yetki.
Her test, kataloğa girmiş bir geçmiş hatayı kilitler (HATA-* kodları docstring'lerde)."""
import json
import re

import pytest

from conftest import ROOT, html_files, read, tracked_files

SECRET_PATTERNS = [
    r"gh[pousr]_[A-Za-z0-9]{20,}", r"sk-ant-[A-Za-z0-9_-]{10,}", r"AKIA[0-9A-Z]{16}", r"-----BEGIN [A-Z ]*PRIVATE KEY-----",
    r"xox[bp]-[A-Za-z0-9-]{10,}", r"\b\d{8,10}:[A-Za-z0-9_-]{35}\b", r"AIza[0-9A-Za-z_-]{35}",
]
SENSITIVE_TRACKED = re.compile(r"(^|/)(\.env(\..*)?|.*\.(pem|key|p12|pfx|db|sqlite3?|pid)|id_(rsa|ed25519).*|settings\.local\.json|composer\.phar|SERVER_ACCESS\.md)$", re.I)
ENV_EXAMPLE = re.compile(r"\.env\.(example|sample)$")


def csp(rel):
    m = re.search(r'http-equiv="Content-Security-Policy" content="([^"]+)"', read(rel))
    assert m, f"{rel}: CSP meta yok"
    return {k: v for k, v in (d.strip().split(" ", 1) if " " in d.strip() else (d.strip(), "") for d in m.group(1).split(";") if d.strip())}


@pytest.mark.parametrize("rel", html_files())
def test_csp_is_strict(rel):
    """HATA-OYUN-002: 'sıkı CSP' iddiası 'unsafe-inline' ile çelişiyordu; burada gerçekten sıkı olmalı."""
    c = csp(rel)
    assert c["default-src"] == "'none'"
    assert c["script-src"] == "'self'" and c["style-src"] == "'self'"
    assert c["connect-src"] == "'none'" and c["form-action"] == "'none'" and c["base-uri"] == "'none'"
    joined = " ".join(c.values())
    for bad in ("unsafe-inline", "unsafe-eval", "*", "http:", "data: https"):
        assert bad not in joined, f"{rel}: CSP'de {bad}"


@pytest.mark.parametrize("rel", html_files())
def test_no_inline_code(rel):
    """CSP ile uyumlu olması için satır içi betik, stil ve olay işleyicisi bulunmaz (JSON-LD veri bloğu hariç)."""
    text = read(rel)
    for m in re.finditer(r"<script\b([^>]*)>(.*?)</script>", text, re.S):
        attrs, body = m.groups()
        if 'type="application/ld+json"' in attrs:
            json.loads(body)
            continue
        assert "src=" in attrs and not body.strip(), f"{rel}: satır içi betik"
    assert "<style" not in text.lower(), f"{rel}: <style>"
    assert not re.search(r"\sstyle\s*=", text), f"{rel}: style= özniteliği"
    assert not re.search(r"\son[a-z]+\s*=", text), f"{rel}: olay işleyici özniteliği"
    assert "javascript:" not in text.lower()


def test_no_external_requests_in_markup_or_css():
    """CDN/Google Fonts bağımlılığı yok (eski sitede cdnjs ve fonts.googleapis.com vardı).
    <a>, canonical ve hreflang bağlantıları kaynak yüklemez; yalnızca yükleyen etiketler denetlenir."""
    loaders = re.compile(r'<(script|img|source|iframe|link)\b([^>]*)>', re.I)
    for rel in html_files():
        for tag, attrs in loaders.findall(read(rel)):
            if tag.lower() == "link" and not re.search(r'rel="(stylesheet|preload|icon|modulepreload|prefetch|preconnect|dns-prefetch)"', attrs):
                continue
            m = re.search(r'(?:src|href)="(https?://[^"]+)"', attrs)
            assert not m, f"{rel}: dış kaynak {m.group(1) if m else ''}"
        assert "preconnect" not in read(rel)
    css = read("assets/css/style.css")
    assert not re.search(r"url\(\s*['\"]?https?:", css) and "@import" not in css


def test_no_secrets_in_tracked_files():
    for f in tracked_files():
        p = ROOT / f
        if not p.is_file() or p.suffix in {".woff2", ".png", ".ico"}:
            continue
        try:
            text = p.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for pat in SECRET_PATTERNS:
            assert not re.search(pat, text), f"{f}: sır benzeri içerik ({pat})"


def test_no_sensitive_files_tracked():
    """HATA-PANO-001/002, HATA-TARF-001, HATA-TOPLULUK-001: .env, anahtar, veritabanı, yerel ayar dosyası git'e girmez."""
    bad = [f for f in tracked_files() if SENSITIVE_TRACKED.search(f) and not ENV_EXAMPLE.search(f)]
    assert not bad, bad


def test_gitignore_blocks_sensitive_patterns():
    gi = read(".gitignore")
    for needed in (".env", "*.pem", "*.key", "*.db", "settings.local.json", "node_modules", "__pycache__"):
        assert needed in gi, f".gitignore'da {needed} yok"


def test_workflows_least_privilege_and_no_masking():
    """HATA-YDS-003: `npm ci || npm install` / `|| true` hataları maskeler; izinler en az olmalı."""
    wf = list((ROOT / ".github/workflows").glob("*.yml"))
    assert wf
    for f in wf:
        text = f.read_text(encoding="utf-8")
        assert re.search(r"^permissions:\s*\n\s+contents:\s*read", text, re.M), f"{f.name}: üst düzey permissions: contents: read yok"
        assert "pull_request_target" not in text, f.name
        assert "|| true" not in text and "npm ci || npm install" not in text, f.name
        assert "continue-on-error" not in text, f"{f.name}: continue-on-error hatayı gizler"


def test_jsonld_has_no_personal_contact():
    for rel in ("index.html", "en/index.html"):
        m = re.search(r'<script type="application/ld\+json">(.*?)</script>', read(rel), re.S)
        blob = m.group(1).lower()
        assert "@outlook" not in blob and "telephone" not in blob and "address" not in blob


def test_referrer_policy_present():
    for rel in ("index.html", "en/index.html"):
        assert 'name="referrer" content="strict-origin-when-cross-origin"' in read(rel)

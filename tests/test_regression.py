"""Regresyon testleri (tarayıcısız, deterministik). Her test, geçmişte yaşanmış bir hatanın geri gelmesini yakalar;
docstring'deki HATA-* kodları agent-koyu hata kataloğundaki kayıtlara karşılık gelir."""
import json
import re
import struct
import subprocess
import sys
from html.parser import HTMLParser
from urllib.parse import urlparse

import pytest

from conftest import ROOT, html_files, read

ALLOWED_EXTERNAL_HOSTS = {"github.com", "www.linkedin.com", "keremefeyigit.github.io", "yusakru.github.io"}
sys.path.insert(0, str(ROOT / "tools"))
import content as C  # noqa: E402


class Doc(HTMLParser):
    """Küçük HTML ayrıştırıcı: etiketler, kimlikler, bağlantılar, başlıklar."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.tags, self.ids, self.links, self.metas, self.headings = [], set(), [], [], []
        self.title = ""
        self._in_title = False
        self._cur_h = None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        self.tags.append((tag, a))
        if "id" in a:
            self.ids.add(a["id"])
        if tag == "a":
            self.links.append(a)
        if tag == "meta":
            self.metas.append(a)
        if tag == "title":
            self._in_title = True
        if tag in ("h1", "h2", "h3"):
            self._cur_h = [tag, ""]

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False
        if self._cur_h and tag == self._cur_h[0]:
            self.headings.append(tuple(self._cur_h)); self._cur_h = None

    def handle_data(self, d):
        if self._in_title:
            self.title += d
        if self._cur_h is not None:
            self._cur_h[1] += d


def parse(rel):
    d = Doc(); d.feed(read(rel)); return d


def meta(doc, **match):
    for m in doc.metas:
        if all(m.get(k) == v for k, v in match.items()):
            return m
    return None


# ---------- Üretim ve yapı ----------
def test_generated_files_are_up_to_date():
    """HATA-GENEL: üretilen dosyalar kaynakla senkron kalmalı (elle düzenlenip build unutulmasın)."""
    r = subprocess.run([sys.executable, "tools/build.py", "--check"], cwd=ROOT, capture_output=True, text=True)
    assert r.returncode == 0, r.stdout + r.stderr


@pytest.mark.parametrize("rel,lang", [("index.html", "tr"), ("en/index.html", "en")])
def test_head_metadata(rel, lang):
    d = parse(rel)
    assert next(a for t, a in d.tags if t == "html").get("lang") == lang
    assert 15 <= len(d.title.strip()) <= 70, d.title
    desc = meta(d, name="description")["content"]
    assert 70 <= len(desc) <= 170, len(desc)
    assert meta(d, name="viewport")["content"].startswith("width=device-width")
    canon = next(a for t, a in d.tags if t == "link" and a.get("rel") == "canonical")["href"]
    assert canon == C.SITE + ("/" if lang == "tr" else "/en/")
    hl = {a["hreflang"]: a["href"] for t, a in d.tags if t == "link" and a.get("rel") == "alternate"}
    assert set(hl) == {"tr", "en", "x-default"} and hl["x-default"] == C.SITE + "/"
    for prop in ("og:title", "og:description", "og:url", "og:image", "og:locale", "og:type"):
        assert meta(d, property=prop), prop
    assert meta(d, name="twitter:card")["content"] == "summary_large_image"
    assert meta(d, name="color-scheme")


def test_og_image_is_valid_png_1200x630():
    data = (ROOT / "assets/img/og.png").read_bytes()
    assert data[:8] == b"\x89PNG\r\n\x1a\n"
    w, h = struct.unpack(">II", data[16:24])
    assert (w, h) == (1200, 630)
    assert len(data) < 200_000


@pytest.mark.parametrize("rel", ["index.html", "en/index.html"])
def test_heading_structure(rel):
    """Tek h1; h2 ve h3 sırası atlamaz (eski sitede axe 'heading-order' ihlali vardı)."""
    levels = [int(t[1]) for t, _ in parse(rel).headings]
    assert levels.count(1) == 1 and levels[0] == 1
    for prev, cur in zip(levels, levels[1:]):
        assert cur - prev <= 1, (prev, cur)


def test_tr_en_parity():
    """İki dil aynı yapıda olmalı: aynı bölümler, projeler, bağlantılar, yetenek sayıları."""
    tr, en = parse("index.html"), parse("en/index.html")
    assert sorted(tr.ids) == sorted(en.ids)
    ext = lambda d: sorted(a["href"] for a in d.links if a.get("href", "").startswith("http"))
    assert ext(tr) == ext(en)
    assert [t for t, _ in tr.headings] == [t for t, _ in en.headings]
    assert len(C.TR["projects"]) == len(C.EN["projects"]) == len(C.PROJECTS)
    assert len(C.TR["approach"]) == len(C.EN["approach"])
    assert set(C.TR["projects"]) == set(C.EN["projects"]) == {p["id"] for p in C.PROJECTS}


# ---------- Bağlantılar ----------
@pytest.mark.parametrize("rel", html_files())
def test_internal_links_and_assets_resolve(rel):
    d, text = parse(rel), read(rel)
    for a in d.links:
        href = a.get("href", "")
        if href.startswith("#") and len(href) > 1:
            assert href[1:] in d.ids, f"{rel}: kırık sayfa içi bağlantı {href}"
        elif href.startswith("/"):
            path = href.split("#")[0].split("?")[0]
            target = ROOT / path.lstrip("/")
            assert target.exists() or (target / "index.html").exists(), f"{rel}: bağlantı hedefi yok {href}"
    for ref in re.findall(r'(?:src|href)="(/assets/[^"#?]+)"', text):
        assert (ROOT / ref.lstrip("/")).is_file(), f"{rel}: eksik dosya {ref}"


def test_external_links_policy():
    """Dış bağlantılar yalnızca izinli sunuculara gider ve noopener/noreferrer taşır (eski sitede 11 bağlantıda eksikti)."""
    for rel in ("index.html", "en/index.html"):
        for a in parse(rel).links:
            href = a.get("href", "")
            if not href.startswith("http"):
                continue
            assert urlparse(href).hostname in ALLOWED_EXTERNAL_HOSTS, f"{rel}: izinsiz dış sunucu {href}"
            assert href.startswith("https://"), href
            if a.get("target") == "_blank":
                r = a.get("rel", "")
                assert "noopener" in r and "noreferrer" in r, f"{rel}: {href}"


def test_known_broken_link_does_not_return():
    """HATA-PORTFOLYO-001: 'Canlı raporu aç' bağlantısı eski, 404 veren adrese (…veriGorsel) gitmişti."""
    for rel in ("index.html", "en/index.html"):
        text = read(rel)
        assert "asu-savunma-harcamas--veriGorsel" not in text
        assert C.REPORT in text


# ---------- İçerik doğruluğu (yanıltıcı iddialar) ----------
FORBIDDEN_CLAIMS = [
    "tam korumalı", "fully protected", "zero-vulnerability", "sıfır-açık", "sıfır açık", "%100 güvenli", "100% secure",
    "unhackable", "Tüm hakları saklıdır", "All rights reserved",
]


@pytest.mark.parametrize("rel", ["index.html", "en/index.html"])
def test_no_overclaims(rel):
    """HATA-PORTFOLYO-002 / GENEL: 'tam korumalı', 'Tüm hakları saklıdır' gibi doğrulanamayan veya LICENSE ile çelişen iddialar yok."""
    low = read(rel).lower()
    for phrase in FORBIDDEN_CLAIMS:
        assert phrase.lower() not in low, f"{rel}: yasak iddia '{phrase}'"


def test_open_source_label_only_for_osi_licenses():
    """HATA-PANO-004 / HATA-OYUN-001: CC BY-NC-ND bir proje 'açık kaynak' diye etiketlenmez (OSI onaylı değil)."""
    for rel in ("index.html", "en/index.html"):
        low = read(rel).lower()
        assert "açık kaynak" not in low and "open source" not in low, rel
    for L in (C.TR, C.EN):
        assert "açık kaynak" not in L["vis"]["open"].lower() and "open source" not in L["vis"]["open"].lower()


def test_footer_license_matches_license_file():
    """HATA-YDS-002: README/rozet 'All Rights Reserved' derken LICENSE MIT idi; burada sayfa ile LICENSE tutarlı olmalı."""
    assert read("LICENSE").splitlines()[0].strip().startswith("MIT")
    for rel in ("index.html", "en/index.html"):
        assert "MIT" in read(rel)


def test_email_is_not_in_plain_html():
    """HATA-PORTFOLYO-003: e-posta düz metin/mailto olarak HTML'de durursa toplayıcı botlar alır; JS ile birleştirilir."""
    pat = re.compile(rf"{C.MAIL_USER}\s*@\s*{re.escape(C.MAIL_DOMAIN)}", re.I)
    for rel in html_files() + ["sitemap.xml", "robots.txt"]:
        text = read(rel)
        assert not pat.search(text), rel
        assert "mailto:" not in text, rel
    assert "data-mail-user" in read("index.html")


def test_project_visibility_labels_are_consistent():
    """Kodu kapalı projelerde kaynak bağlantısı olmamalı (özel repoya link vermek 404/yanlış beklenti yaratır)."""
    for p in C.PROJECTS:
        if p["visibility"] in ("private", "corporate"):
            assert not any(kind == "repo" for kind, _ in p["links"]), p["id"]
        if p["visibility"] == "open":
            assert p["links"], p["id"]


# ---------- Statik dosyalar ----------
def test_sitemap_robots_404():
    sm = read("sitemap.xml")
    assert C.SITE + "/</loc>" in sm and C.SITE + "/en/</loc>" in sm and sm.count("hreflang") >= 6
    assert f"Sitemap: {C.SITE}/sitemap.xml" in read("robots.txt")
    assert meta(parse("404.html"), name="robots")["content"] == "noindex"
    assert (ROOT / ".nojekyll").exists()


def test_fonts_are_real_woff2_and_licensed():
    fonts = list((ROOT / "assets/fonts").glob("*.woff2"))
    assert len(fonts) >= 8
    for f in fonts:
        assert f.read_bytes()[:4] == b"wOF2", f.name
    assert (ROOT / "assets/fonts/LICENSE-Fraunces.txt").exists() and (ROOT / "assets/fonts/LICENSE-IBM-Plex.txt").exists()


def test_json_ld_is_valid_person():
    for rel in ("index.html", "en/index.html"):
        m = re.search(r'<script type="application/ld\+json">(.*?)</script>', read(rel), re.S)
        data = json.loads(m.group(1))
        assert data["@type"] == "Person" and data["name"] == "Kerem Efe Yiğit"
        assert set(data["sameAs"]) == {C.GITHUB, C.LINKEDIN}
        assert "email" not in data


def test_size_budgets():
    """Sayfa ağırlığı bütçesi: HTML ≤ 30 KB, CSS ≤ 30 KB, JS toplam ≤ 8 KB."""
    for rel in ("index.html", "en/index.html"):
        assert len(read(rel).encode()) <= 30_000, rel
    assert len(read("assets/css/style.css").encode()) <= 30_000
    assert sum(len(read(f"assets/js/{n}").encode()) for n in ("theme.js", "main.js")) <= 8_000

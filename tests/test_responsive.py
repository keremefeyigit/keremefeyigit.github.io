"""Responsive ve tarayıcı davranışı testleri (Playwright, yerel sunucu, dış ağ yok)."""
import pytest

from conftest import WIDTHS

OVERFLOW_JS = """() => {
  const w = window.innerWidth, bad = [];
  for (const el of document.querySelectorAll('body *')) {
    const r = el.getBoundingClientRect(), cs = getComputedStyle(el);
    if (!r.width || !r.height || cs.visibility === 'hidden' || cs.display === 'none') continue;
    if (r.right > w + 1 || r.left < -1) bad.push(el.tagName + '.' + String(el.className).split(' ')[0] + ' [' + Math.round(r.left) + ',' + Math.round(r.right) + ']');
    if (bad.length > 5) break;
  }
  return { scrollW: document.documentElement.scrollWidth, innerW: w, bad };
}"""

TARGET_SELECTORS = ".brand, .lang, .theme, .nav a, .btn, .links a, .contact-links a, .contact-mail, footer a"


@pytest.mark.parametrize("lang", ["tr", "en"])
@pytest.mark.parametrize("scheme", ["light", "dark"])
@pytest.mark.parametrize("width", WIDTHS)
def test_no_horizontal_overflow_and_no_console_noise(open_page, lang, scheme, width):
    """HATA-PORTFOLYO-004: eski sitede 390 px'te 230 px yatay taşma vardı."""
    page, errors, requests = open_page(lang, width, 900 if width >= 768 else 800, scheme)
    r = page.evaluate(OVERFLOW_JS)
    assert r["scrollW"] <= r["innerW"] + 1, r
    assert not r["bad"], r["bad"]
    assert not errors, errors
    external = [u for u in requests if not u.startswith("http://127.0.0.1")]
    assert not external, external


@pytest.mark.parametrize("lang", ["tr", "en"])
@pytest.mark.parametrize("width", [320, 390, 768])
def test_touch_targets_at_least_44px(open_page, lang, width):
    """Dokunma hedefleri ≥ 44×44 CSS px (WCAG 2.2 AAA hedefi; mobil için iyi uygulama)."""
    page, _, _ = open_page(lang, width, 800)
    small = page.evaluate("""(sel) => [...document.querySelectorAll(sel)].filter(e => { const r = e.getBoundingClientRect(); return r.width && r.height && (r.height < 43.5 || r.width < 43.5) && getComputedStyle(e).display !== 'none'; })
        .map(e => e.tagName + '.' + e.className + ' ' + Math.round(e.getBoundingClientRect().width) + 'x' + Math.round(e.getBoundingClientRect().height) + ' "' + e.textContent.trim().slice(0, 20) + '"')""", TARGET_SELECTORS)
    assert not small, small


@pytest.mark.parametrize("width", [320, 360, 1280])
def test_hero_heading_fits_and_fonts_load(open_page, width):
    page, errors, _ = open_page("tr", width, 800)
    box = page.locator("h1").bounding_box()
    assert box["x"] >= 0 and box["x"] + box["width"] <= width + 1
    assert page.evaluate("document.fonts.check('16px \"IBM Plex Sans\"') && document.fonts.check('32px Fraunces')")
    assert page.evaluate("[...document.fonts].filter(f => f.status === 'loaded').length") >= 2
    assert not errors


def test_layout_switches_between_mobile_and_desktop(open_page):
    page, _, _ = open_page("tr", 390, 800)
    assert page.evaluate("getComputedStyle(document.querySelector('.rail')).position") != "sticky"
    page, _, _ = open_page("tr", 1280, 800)
    assert page.evaluate("getComputedStyle(document.querySelector('.rail')).position") == "sticky"
    x = page.evaluate("document.querySelector('main').getBoundingClientRect().x")
    rail_right = page.evaluate("document.querySelector('.rail').getBoundingClientRect().right")
    assert x > rail_right, "ana içerik rayın yanında olmalı"


def test_text_zoom_200_percent_no_overflow(open_page):
    """WCAG 1.4.4 metin yeniden boyutlandırma: kök yazı boyutu %200 iken 320 px'te taşma olmaz."""
    page, _, _ = open_page("tr", 320, 800, bypass_csp=True)
    page.add_style_tag(content="html{font-size:200% !important}")
    page.wait_for_timeout(200)
    r = page.evaluate(OVERFLOW_JS)
    assert r["scrollW"] <= r["innerW"] + 1, r


def test_reduced_motion_disables_animations(open_page):
    page, _, _ = open_page("tr", 1280, 800, reduced_motion=True)
    assert page.evaluate("document.getAnimations().length") == 0


def test_content_is_never_hidden_by_animation(open_page):
    """Animasyon içeriği gizlememeli (opacity 0 ile başlamaz): ilk karede h1 görünür."""
    page, _, _ = open_page("tr", 1280, 800, reduced_motion=False)
    assert page.evaluate("getComputedStyle(document.querySelector('h1')).opacity") == "1"


def test_theme_toggle_persists_and_respects_system(open_page):
    page, _, _ = open_page("tr", 1280, 800, scheme="dark")
    assert page.evaluate("getComputedStyle(document.body).backgroundColor") == "rgb(16, 18, 21)"
    btn = page.locator("[data-theme-toggle]")
    assert btn.is_visible()
    btn.click()
    assert page.evaluate("document.documentElement.dataset.theme") == "light"
    assert page.evaluate("getComputedStyle(document.body).backgroundColor") == "rgb(243, 239, 230)"
    page.reload(wait_until="networkidle")
    assert page.evaluate("document.documentElement.dataset.theme") == "light", "seçim kalıcı olmalı"
    assert page.get_attribute("[data-theme-toggle]", "aria-pressed") == "false"


def test_works_without_javascript(open_page):
    """JS kapalıyken içerik, menü ve e-posta (metin olarak) erişilebilir kalır; tema düğmesi gizlidir."""
    page, errors, _ = open_page("tr", 1280, 800, js=False)
    assert page.locator("h1").is_visible()
    assert page.locator(".nav a").count() == 4
    assert not page.locator("[data-theme-toggle]").is_visible()
    assert "[at]" in page.locator(".contact-mail").inner_text()
    assert not errors


def test_mail_link_is_assembled_by_js(open_page):
    page, _, _ = open_page("tr", 1280, 800)
    assert page.get_attribute(".contact-mail", "href") == "mailto:keremefeyigit@outlook.com"
    assert page.inner_text(".contact-mail") == "keremefeyigit@outlook.com"


def test_language_switch_links(open_page, base_url):
    page, _, _ = open_page("tr", 1280, 800)
    page.click(".lang")
    page.wait_for_url(base_url + "/en/")
    assert page.get_attribute("html", "lang") == "en"
    page.click(".lang")
    page.wait_for_url(base_url + "/")
    assert page.get_attribute("html", "lang") == "tr"


def test_skip_link_is_first_tab_stop_and_works(open_page):
    page, _, _ = open_page("tr", 1280, 800)
    page.keyboard.press("Tab")
    assert page.evaluate("document.activeElement.className") == "skip"
    assert page.evaluate("document.activeElement.getBoundingClientRect().top") >= 0
    page.keyboard.press("Enter")
    assert page.evaluate("location.hash") == "#main"


def test_every_interactive_element_shows_focus_ring(open_page):
    page, _, _ = open_page("tr", 1280, 800)
    count = page.evaluate("document.querySelectorAll('a[href], button:not([hidden])').length")
    missing = []
    for _ in range(count + 2):
        page.keyboard.press("Tab")
        out = page.evaluate("""() => { const e = document.activeElement; if (!e || e === document.body) return null;
            const cs = getComputedStyle(e); return { tag: e.tagName + '.' + e.className, w: cs.outlineWidth, style: cs.outlineStyle }; }""")
        if out and (out["style"] == "none" or out["w"] in ("0px", "")):
            missing.append(out)
    assert not missing, missing


def test_404_page_is_served_for_unknown_paths(open_page):
    page, _, _ = open_page("tr", 1280, 800, path="/bu-sayfa-yok/")
    assert "404" in page.inner_text(".kicker")
    assert page.locator("a[href='/']").count() >= 1

"""Erişilebilirlik: axe-core ile WCAG 2.0/2.1/2.2 A-AA ve en iyi uygulama kuralları. Hiç ihlal olmamalı."""
import pytest
from axe_playwright_python.sync_playwright import Axe

TAGS = ["wcag2a", "wcag2aa", "wcag21a", "wcag21aa", "wcag22aa", "best-practice"]


@pytest.mark.parametrize("lang", ["tr", "en"])
@pytest.mark.parametrize("scheme", ["light", "dark"])
@pytest.mark.parametrize("width", [390, 1440])
def test_axe_has_no_violations(open_page, lang, scheme, width):
    """HATA-PORTFOLYO-005: eski sitede axe 'heading-order' ihlali vardı."""
    page, _, _ = open_page(lang, width, 900, scheme)
    results = Axe().run(page, options={"runOnly": {"type": "tag", "values": TAGS}})
    summary = [f"{v['id']} ({v['impact']}): {len(v['nodes'])} düğüm — {v['nodes'][0]['html'][:100]}" for v in results.response["violations"]]
    assert not summary, "\n".join(summary)


def test_axe_on_404(open_page):
    page, _, _ = open_page("tr", 1280, 800, path="/yok-boyle-bir-sayfa/")
    results = Axe().run(page, options={"runOnly": {"type": "tag", "values": TAGS}})
    assert not results.response["violations"], [v["id"] for v in results.response["violations"]]


@pytest.mark.parametrize("lang", ["tr", "en"])
def test_landmarks_and_names(open_page, lang):
    page, _, _ = open_page(lang, 1280, 800)
    assert page.locator("header").count() == 1 and page.locator("main").count() == 1 and page.locator("nav[aria-label]").count() == 1
    assert page.locator("footer").count() == 1
    unnamed = page.evaluate("[...document.querySelectorAll('a[href], button')].filter(e => !(e.textContent.trim() || e.getAttribute('aria-label'))).map(e => e.outerHTML.slice(0, 80))")
    assert not unnamed, unnamed
    assert page.get_attribute("html", "lang") == lang

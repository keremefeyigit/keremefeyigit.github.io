"""Dış bağlantı denetimi: ağ gerekir; yalnızca CHECK_EXTERNAL=1 ile (haftalık CI işi) çalışır.
HATA-PORTFOLYO-001: kırık 'canlı rapor' bağlantısı bu testle yakalanırdı."""
import os
import re
import urllib.error
import urllib.request

import pytest

from conftest import read

pytestmark = pytest.mark.external


def external_urls():
    urls = set()
    for rel in ("index.html", "en/index.html"):
        urls |= set(re.findall(r'href="(https://[^"]+)"', read(rel)))
    kendi = {"https://keremefeyigit.github.io/", "https://keremefeyigit.github.io/en/"}  # kendi sayfalarımız (yayından önce 404 olabilir)
    return sorted(u for u in urls if u not in kendi)


@pytest.mark.skipif(not os.environ.get("CHECK_EXTERNAL"), reason="CHECK_EXTERNAL=1 ile çalıştırın (ağ gerekir)")
@pytest.mark.parametrize("url", external_urls())
def test_external_url_is_alive(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (link-check)"})
    try:
        status = urllib.request.urlopen(req, timeout=25).status
    except urllib.error.HTTPError as e:
        status = e.code
    # LinkedIn bot isteklerine 999 döner: bağlantı yaşıyor kabul edilir
    assert status < 400 or (status == 999 and "linkedin.com" in url), f"{url} -> {status}"

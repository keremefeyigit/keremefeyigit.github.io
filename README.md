# keremefeyigit.github.io

Kerem Efe Yiğit'in kişisel portfolyo sitesi: **https://keremefeyigit.github.io** (Türkçe) · **/en/** (English).

Statik, bağımlılıksız bir site: derleme sunucusu yok, dış CDN yok, kullanıcıyı izleyen bir şey yok. GitHub Pages doğrudan depo kökünü yayınlar.

## Yapı

```
index.html, en/index.html, 404.html   # ÜRETİLİR (tools/build.py), commit'lenir
sitemap.xml, robots.txt, .nojekyll    # ÜRETİLİR
tools/content.py                      # tüm metinler (TR/EN) ve proje listesi: içerik değişikliği buradan
tools/build.py                        # içerikten sayfaları üretir (yalnızca Python standart kütüphanesi)
tools/og.html, tools/make_og.py       # paylaşım görseli (assets/img/og.png) üreticisi
assets/css, assets/js, assets/img     # tek stil dosyası, 2 küçük betik, favicon + OG görseli
assets/fonts                          # Fraunces + IBM Plex (OFL, kendi sunucumuzdan; lisanslar yanında)
tests/                                # regresyon, güvenlik, responsive, erişilebilirlik, performans (pytest + Playwright)
docs/tasarim.md                       # tasarım kararları ve Stitch brief'i
```

## Çalıştırma ve değiştirme

```bash
python3 tools/build.py                # içeriği değiştirdikten sonra sayfaları yeniden üret
python3 -m http.server 8000           # http://localhost:8000
```

İçerik yalnızca `tools/content.py` içinde düzenlenir; `index.html` ve `en/index.html` elle düzenlenmez (CI, üretilen dosyaların güncel olduğunu denetler).

## Testler

```bash
pip install -r requirements-dev.txt && python -m playwright install chromium
python -m pytest -q                              # hepsi (dış ağ gerektirmez)
CHECK_EXTERNAL=1 python -m pytest -q -m external # canlı dış bağlantı kontrolü (haftalık CI işi de bunu yapar)
```

| Paket | Ne denetler |
|---|---|
| `test_regression.py` | üretilen dosyalar güncel, TR/EN eşitliği, kırık bağlantı, yanıltıcı iddia (ör. "açık kaynak", "tam korumalı"), lisans tutarlılığı, e-postanın düz metin olmaması |
| `test_security.py` | katı CSP (`default-src 'none'`), satır içi kod yok, dış kaynak yok, sır yok, izlenmemesi gereken dosya yok, CI iş akışı en az yetkili |
| `test_responsive.py` | 320-1920 px × TR/EN × açık/koyu: yatay taşma yok, konsol hatası yok, dokunma hedefi ≥ 44 px, JS'siz çalışma, tema kalıcılığı, klavye ve odak |
| `test_a11y.py` | axe-core WCAG 2.x A/AA + en iyi uygulama: sıfır ihlal |
| `test_performance.py` | istek sayısı, aktarım boyutu, CLS, LCP, render engelleme |

HTML doğrulaması CI'da `html-validate` ile yapılır.

## Tasarım ve güvenlik notları

- Tek sütunlu mobil düzen, ≥ 64 rem'de yapışkan sol ray; yazı tipleri: Fraunces (başlık), IBM Plex Sans/Mono (metin, etiket).
- Tema sistem ayarını izler, düğmeyle değiştirilir ve `localStorage`'da saklanır (depolama kapalıysa sessizce atlanır).
- E-posta adresi HTML'de düz metin değildir; JS ile birleştirilir (toplayıcı botlara karşı). JS kapalıysa `ad [at] alan` biçiminde görünür.
- Tüm dış bağlantılar `rel="noopener noreferrer"` taşır; yalnızca izinli sunuculara gider (testle denetlenir).
- Ayrıntı ve gerekçeler: [docs/tasarim.md](docs/tasarim.md).

## Lisans

Kaynak kod [MIT](LICENSE) lisanslıdır. Yazı tipleri SIL Open Font License 1.1 altındadır (`assets/fonts/LICENSE-*.txt`).

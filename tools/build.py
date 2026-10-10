#!/usr/bin/env python3
"""Statik siteyi üretir: index.html (TR), en/index.html (EN), 404.html, sitemap.xml, robots.txt.

Kullanım:  python3 tools/build.py          (yalnızca standart kütüphane)
           python3 tools/build.py --check  (dosyalar güncel değilse 1 ile çıkar; CI kullanır)
Üretilen dosyalar commit'lenir (GitHub Pages doğrudan kökten yayınlar, derleme adımı yoktur).
"""
import json
import sys
from html import escape as e
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import content as C  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
CSP = ("default-src 'none'; script-src 'self'; style-src 'self'; img-src 'self' data:; font-src 'self'; "
       "connect-src 'none'; base-uri 'none'; form-action 'none'; manifest-src 'none'")
OG_IMAGE = C.SITE + "/assets/img/og.png"


def project_html(p, L, featured):
    name, desc = L["projects"][p["id"]]
    tags = "".join(f"<li>{e(t)}</li>" for t in p["tags"])
    vis_text = L["vis"][p["visibility"]] + (f' · {L["license_word"]}: {p["license"]}' if p.get("license") else "")
    vis = f'<span class="vis {p["visibility"]}">{e(vis_text)}</span>'
    links = ""
    if p["links"]:
        items = "".join(
            f'<a href="{e(url)}" rel="noopener noreferrer" target="_blank">{e(L["link_labels"][kind])}</a>'
            for kind, url in p["links"])
        links = f'<span class="links">{items}</span>'
    cls = ' class="proj"' if featured else ""
    return (f'<li{cls} id="p-{p["id"]}"><h3>{e(name)}</h3><p>{e(desc)}</p><ul class="tags">{tags}</ul>'
            f'<p class="meta">{vis}{links}</p></li>')


def jsonld(L):
    data = {
        "@context": "https://schema.org", "@type": "Person", "name": "Kerem Efe Yiğit",
        "url": C.SITE + L["path"], "jobTitle": L["role"], "inLanguage": L["lang"],
        "sameAs": [C.GITHUB, C.LINKEDIN],
        "knowsAbout": ["Computer vision", "OpenCV", "YOLOv8", "PHP", "Node.js", "React", "TypeScript", "Multi-agent systems"],
    }
    return json.dumps(data, ensure_ascii=False, indent=2)


def page(L):
    url = C.SITE + L["path"]
    tr_url, en_url = C.SITE + "/", C.SITE + "/en/"
    nav = "".join(f'<li><a href="#{k}"><span class="n">{i:02d}</span>{e(t)}</a></li>' for i, (k, t) in enumerate(L["nav"], 1))
    now = "".join(f"<li><strong>{e(a)}</strong> <span>— {e(b)}</span></li>" for a, b in L["now"])
    feat = "".join(project_html(p, L, True) for p in C.PROJECTS if p["featured"])
    more = "".join(project_html(p, L, False) for p in C.PROJECTS if not p["featured"])
    principles = "".join(f"<li><h3>{e(t)}</h3><p>{e(d)}</p></li>" for t, d in L["approach"])
    skills = "".join(
        f'<div><h3>{e(L["skill_groups"][g])}</h3><ul>{"".join(f"<li>{e(x)}</li>" for x in items)}</ul></div>'
        for g, items in C.SKILLS)
    n = {k: i for i, (k, _) in enumerate(L["nav"], 1)}
    other_lang = "en" if L["lang"] == "tr" else "tr"
    return f"""<!doctype html>
<html lang="{L['lang']}">
<head>
<meta charset="utf-8">
<meta http-equiv="Content-Security-Policy" content="{CSP}">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(L['title'])}</title>
<meta name="description" content="{e(L['description'])}">
<meta name="referrer" content="strict-origin-when-cross-origin">
<meta name="color-scheme" content="light dark">
<meta name="theme-color" content="#f3efe6" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#101215" media="(prefers-color-scheme: dark)">
<link rel="canonical" href="{url}">
<link rel="alternate" hreflang="tr" href="{tr_url}">
<link rel="alternate" hreflang="en" href="{en_url}">
<link rel="alternate" hreflang="x-default" href="{tr_url}">
<link rel="icon" href="/assets/img/favicon.svg" type="image/svg+xml">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Kerem Efe Yiğit">
<meta property="og:title" content="{e(L['title'])}">
<meta property="og:description" content="{e(L['description'])}">
<meta property="og:url" content="{url}">
<meta property="og:locale" content="{L['locale']}">
<meta property="og:image" content="{OG_IMAGE}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{e(L['title'])}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(L['title'])}">
<meta name="twitter:description" content="{e(L['description'])}">
<meta name="twitter:image" content="{OG_IMAGE}">
<link rel="preload" href="/assets/fonts/fraunces-latin-wght-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/ibm-plex-sans-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/assets/css/style.css">
<script src="/assets/js/theme.js"></script>
<script type="application/ld+json">
{jsonld(L)}
</script>
</head>
<body>
<a class="skip" href="#main">{e(L['skip'])}</a>
<div class="shell">
<header class="rail">
  <div class="rail-top">
    <div>
      <a class="brand" href="{L['path']}">Kerem Efe Yiğit</a>
      <p class="role">{e(L['role'])}</p>
    </div>
    <div class="tools">
      <a class="lang" href="{L['other_path']}" hreflang="{other_lang}" lang="{other_lang}" title="{e(L['other_name'])}">{L['other_label']}</a>
      <button class="theme" type="button" data-theme-toggle data-label-dark="{e(L['theme_dark'])}" data-label-light="{e(L['theme_light'])}" aria-label="{e(L['theme_label'])}" aria-pressed="false" hidden>&#9680;</button>
    </div>
  </div>
  <nav aria-label="{e(L['nav_label'])}" data-nav><ol class="nav">{nav}</ol></nav>
</header>
<main id="main">
  <section class="hero" aria-labelledby="hero-title">
    <p class="kicker">{e(L['hero_kicker'])}</p>
    <h1 id="hero-title">{e(L['hero_title'])}</h1>
    <p class="lead">{e(L['hero_lead'])}</p>
    <p class="cta"><a class="btn" href="#work">{e(L['cta_work'])}</a><a class="btn ghost" href="#contact">{e(L['cta_contact'])}</a></p>
    <div class="now"><p class="now-title">{e(L['now_title'])}</p><ul>{now}</ul></div>
  </section>

  <section id="work" aria-labelledby="work-title">
    <h2 id="work-title"><span class="n">{n['work']:02d}</span>{e(L['work_title'])}</h2>
    <p class="intro">{e(L['work_intro'])}</p>
    <ol class="featured">{feat}</ol>
    <h3 class="more-title">{e(L['more_title'])}</h3>
    <ul class="more">{more}</ul>
  </section>

  <section id="approach" aria-labelledby="approach-title">
    <h2 id="approach-title"><span class="n">{n['approach']:02d}</span>{e(L['approach_title'])}</h2>
    <ol class="principles">{principles}</ol>
  </section>

  <section id="skills" aria-labelledby="skills-title">
    <h2 id="skills-title"><span class="n">{n['skills']:02d}</span>{e(L['skills_title'])}</h2>
    <div class="skills">{skills}</div>
  </section>

  <section id="contact" aria-labelledby="contact-title">
    <h2 id="contact-title"><span class="n">{n['contact']:02d}</span>{e(L['contact_title'])}</h2>
    <p class="intro">{e(L['contact_lead'])}</p>
    <a class="contact-mail" href="#contact" data-mail-user="{C.MAIL_USER}" data-mail-domain="{C.MAIL_DOMAIN}">{e(L['mail_noscript'])}</a>
    <p class="contact-links">
      <a href="{C.LINKEDIN}" rel="noopener noreferrer" target="_blank">{e(L['linkedin_label'])}</a>
      <a href="{C.GITHUB}" rel="noopener noreferrer" target="_blank">{e(L['github_label'])}</a>
    </p>
  </section>

  <footer>
    <span>© 2026 Kerem Efe Yiğit</span>
    <span>{e(L['footer'])}</span>
    <a href="{C.REPO}" rel="noopener noreferrer" target="_blank">{e(L['source'])}</a>
  </footer>
</main>
</div>
<script src="/assets/js/main.js" defer></script>
</body>
</html>
"""


def not_found():
    return f"""<!doctype html>
<html lang="tr">
<head>
<meta charset="utf-8">
<meta http-equiv="Content-Security-Policy" content="{CSP}">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>404 — Kerem Efe Yiğit</title>
<meta name="robots" content="noindex">
<meta name="color-scheme" content="light dark">
<link rel="icon" href="/assets/img/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="/assets/css/style.css">
<script src="/assets/js/theme.js"></script>
</head>
<body>
<div class="shell"><main id="main">
  <section class="hero">
    <p class="kicker">404</p>
    <h1>Sayfa bulunamadı. / Page not found.</h1>
    <p class="lead">Aradığınız sayfa taşınmış ya da hiç var olmamış olabilir. The page may have moved or never existed.</p>
    <p class="cta"><a class="btn" href="/">Ana sayfa</a><a class="btn ghost" href="/en/">Home (EN)</a></p>
  </section>
</main></div>
</body>
</html>
"""


def sitemap():
    def entry(loc):
        return (f"  <url>\n    <loc>{loc}</loc>\n"
                f'    <xhtml:link rel="alternate" hreflang="tr" href="{C.SITE}/"/>\n'
                f'    <xhtml:link rel="alternate" hreflang="en" href="{C.SITE}/en/"/>\n'
                f'    <xhtml:link rel="alternate" hreflang="x-default" href="{C.SITE}/"/>\n  </url>\n')
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
            + entry(C.SITE + "/") + entry(C.SITE + "/en/") + "</urlset>\n")


def outputs():
    return {
        "index.html": page(C.TR),
        "en/index.html": page(C.EN),
        "404.html": not_found(),
        "sitemap.xml": sitemap(),
        "robots.txt": f"User-agent: *\nAllow: /\n\nSitemap: {C.SITE}/sitemap.xml\n",
        ".nojekyll": "",
    }


def main():
    check = "--check" in sys.argv
    stale = []
    for rel, text in outputs().items():
        path = ROOT / rel
        if check:
            if not path.exists() or path.read_text(encoding="utf-8") != text:
                stale.append(rel)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding="utf-8")
            print("yazıldı:", rel)
    if check:
        if stale:
            print("GÜNCEL DEĞİL (python3 tools/build.py çalıştırın):", ", ".join(stale))
            sys.exit(1)
        print("tüm üretilen dosyalar güncel")


if __name__ == "__main__":
    main()

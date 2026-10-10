"""Site içeriği (TR/EN) tek yerde. tools/build.py bu veriden index.html ve en/index.html üretir.

Kural: yalnızca doğrulanabilir bilgi yazılır (abartılı güvenlik/performans iddiası yok); lisans etiketleri
gerçek LICENSE dosyalarıyla uyumlu olmalıdır (tests/test_regression.py bunu denetler).
"""

SITE = "https://keremefeyigit.github.io"
GITHUB = "https://github.com/keremefeyigit"
LINKEDIN = "https://www.linkedin.com/in/kerem-efe-yi%C4%9Fit/"
MAIL_USER, MAIL_DOMAIN = "keremefeyigit", "outlook.com"
REPO = "https://github.com/keremefeyigit/keremefeyigit.github.io"
REPORT = "https://yusakru.github.io/asu-savunma-harcamalari-veri-gorsellestirme/"

# Proje kimlikleri iki dilde ortaktır; metinler dil sözlüğündedir.
# visibility: open | private | corporate  (etiket metni dil sözlüğünde)
PROJECTS = [
    dict(id="pano", featured=True, visibility="open", license="CC BY-NC-ND 4.0",
         tags=["Python", "YOLOv8", "OpenCV", "FastAPI", "PyTorch", "Docker"],
         links=[("repo", GITHUB + "/PanoHesaplamaSistemi")]),
    dict(id="yemedenonce", featured=True, visibility="private",
         tags=["React 19", "TypeScript", "Gemini", "H3", "Supabase", "Capacitor"], links=[]),
    dict(id="asu", featured=True, visibility="corporate",
         tags=["PHP 8.4", "MySQL/MariaDB", "Custom MVC", "HMAC-SHA256"], links=[]),
    dict(id="agent", featured=True, visibility="private",
         tags=["Python", "Multi-agent", "hcom", "CI"], links=[]),
    dict(id="siyos", featured=False, visibility="open", license="MIT",
         tags=["Node.js", "Express", "SQLite", "JWT"], links=[("repo", GITHUB + "/Apartman-Yonetim-Sistemi")]),
    dict(id="usip", featured=False, visibility="corporate", tags=["PHP", "Custom MVC", "MySQL", "Bootstrap 5"], links=[]),
    dict(id="yds", featured=False, visibility="private", tags=["Electron", "React", "Vite", "CEFR"], links=[]),
    dict(id="roket", featured=False, visibility="open", license="CC BY-NC-ND 4.0",
         tags=["HTML5 Canvas", "JavaScript"],
         links=[("play", "https://keremefeyigit.github.io/Roket-Oyunu/"), ("repo", GITHUB + "/Roket-Oyunu")]),
    dict(id="sabikali", featured=False, visibility="open", license="CC BY-NC-ND 4.0",
         tags=["HTML5", "CSS3", "Vanilla JS"],
         links=[("play", "https://keremefeyigit.github.io/Sabikali-Patiler/"), ("repo", GITHUB + "/Sabikali-Patiler")]),
    dict(id="kalite", featured=False, visibility="corporate", tags=["Vanilla JS", "ES Modules", "JSON"], links=[]),
    dict(id="iskur", featured=False, visibility="private", tags=["Python", "Selenium", "openpyxl"], links=[]),
    dict(id="savunma", featured=False, visibility="open", tags=["R", "ggcorrplot", "Spearman"],
         links=[("report", REPORT)]),
]

SKILLS = [
    ("ai", ["OpenCV", "YOLOv8 (Seg/Det)", "PyTorch", "Gemini API", "Multi-agent (hcom)", "Stereo vision"]),
    ("backend", ["PHP 8.4 (MVC)", "Node.js / Express", "FastAPI", "REST", "HMAC / bcrypt", "Rate limiting"]),
    ("frontend", ["React 19", "TypeScript", "Vite", "Capacitor", "HTML5 Canvas", "Tailwind / CSS3"]),
    ("data", ["MySQL / MariaDB", "PostgreSQL / Supabase", "SQLite", "Docker", "Git / GitHub Actions", "Linux / Bash"]),
]

TR = dict(
    lang="tr", locale="tr_TR", path="/", other_path="/en/", other_label="EN", other_name="English",
    title="Kerem Efe Yiğit — Full-Stack & Yapay Zeka Yazılım Geliştirici",
    description="Kerem Efe Yiğit: kurumsal web sistemleri, bilgisayarlı görü ve çok ajanlı yapay zeka orkestrasyonu geliştiren yazılımcı. Seçilmiş çalışmalar, yaklaşım ve iletişim.",
    role="Full-Stack & Yapay Zeka Yazılım Geliştirici",
    skip="İçeriğe geç", nav_label="Ana gezinme",
    nav=[("work", "Çalışmalar"), ("approach", "Yaklaşım"), ("skills", "Yetenekler"), ("contact", "İletişim")],
    theme_label="Tema değiştir", theme_dark="Koyu tema", theme_light="Açık tema",
    hero_kicker="Yazılım geliştirici",
    hero_title="Kurumsal sistemler, bilgisayarlı görü ve yapay zeka ajanları.",
    hero_lead="Web platformlarından uç cihaz çıkarımına kadar uçtan uca geliştiriyorum. İşi testle bitiririm: veri sızıntısı, kırık bağlantı ve yanıltıcı test gibi hataları sonradan değil, değişiklikten önce yakalamaya çalışırım.",
    now_title="Şu an üzerinde çalıştıklarım",
    now=[("Agent Ofisi", "yerel çok ajanlı orkestrasyon, kural denetimi ve CI döngüsü"),
         ("YEMEDENÖNCE", "doğrulanmış esnaf keşfi için web ve mobil ürün"),
         ("Pano Hesaplama", "reklam panosu ölçümü için bilgisayarlı görü hattı")],
    cta_work="Çalışmalara bak", cta_contact="İletişime geç",
    work_title="Seçilmiş çalışmalar", work_intro="Dört ana proje ve diğer çalışmalar. Kodu kapalı olanlar açıkça belirtilmiştir.",
    more_title="Diğer çalışmalar",
    vis={"open": "Herkese açık kod", "private": "Özel · kod kapalı", "corporate": "Kurumsal · kod kapalı"},
    link_labels={"repo": "Kaynak kod", "play": "Tarayıcıda oyna", "report": "Canlı rapor"},
    license_word="Lisans",
    approach_title="Nasıl çalışırım",
    approach=[
        ("Güvenlik tasarımın parçası",
         "Parolalar bcrypt ile özetlenir, biletler HMAC-SHA256 ile imzalanır, sorgular hazırlanmış ifadelerle yazılır, istekler hız sınırına tabidir. Gizli bilgi koda ve git geçmişine girmesin diye tarama ve .gitignore kuralları kullanırım."),
        ("Ölçülebilir görü sistemleri",
         "Stereo kamera kalibrasyonu, YOLOv8 segmentasyonu ve OpenCV koordinat dönüşümleriyle ölçüm yapan; uç cihazda çalışabilen çıkarım hatları kurarım."),
        ("Denetimli ajanlar",
         "LLM ajanlarını kurallarla çalıştırırım: ajan merge etmez, sır okumaz, her değişiklik testten geçer, kararlar insanda kalır."),
        ("Testle bitirmek",
         "Regresyon, responsive, erişilebilirlik ve güvenlik testleri her değişiklikte çalışır. Test kırmızıyken iş bitmiş sayılmaz."),
    ],
    skills_title="Yetenekler",
    skill_groups={"ai": "Yapay zeka & görü", "backend": "Backend", "frontend": "Frontend & mobil", "data": "Veri & DevOps"},
    contact_title="İletişim", contact_lead="Proje, iş birliği veya teknik danışmanlık için yazabilirsiniz.",
    mail_label="E-posta", mail_noscript="keremefeyigit [at] outlook.com", linkedin_label="LinkedIn", github_label="GitHub",
    footer="Sayfa kaynak kodu MIT lisanslıdır.", source="Kaynak kod", updated="Son güncelleme",
    projects=dict(
        pano=("Pano Hesaplama Sistemi", "Kentsel reklam panolarının boyutunu OpenCV ve YOLOv8 segmentasyonuyla ölçen; stereo mesafe analizi ve koordinat takibi yapan bilgisayarlı görü sistemi."),
        yemedenonce=("YEMEDENÖNCE", "Reklamlardan bağımsız, doğrulanmış esnaf lezzeti keşfi: Bayes istatistiği, Gemini ile duygu analizi ve H3 coğrafi indeksleme."),
        asu=("ASÜ Topluluk Platformu (ASÜConnect)", "49 tablolu kurumsal LAMP sistemi: SKS onay hiyerarşisi, HMAC-SHA256 imzalı QR biletleme ve rol tabanlı erişim. Ekip projesi."),
        agent=("Agent Ofisi (Agent Köyü)", "Claude ve agy ajanlarını hcom protokolüyle yöneten yerel orkestrasyon: anayasal kural denetimi, CI doğrulama döngüsü ve görev devri."),
        siyos=("Apartman Yönetim Sistemi (SIYOS)", "Sakin talepleri, aidat ve gider takibi; JWT, hız sınırı ve güvenlik başlıklarıyla Express ve SQLite üzerinde REST platformu."),
        usip=("USİP — Üniversite-Sanayi İşbirliği Portalı", "TTO, kariyer merkezleri, akademisyenler, öğrenciler ve firmaları buluşturan, AR-GE ve istihdam süreçlerini yöneten B2B/B2C portal (MVP)."),
        yds=("YDS Kelime Oyunu", "YDS ve YÖKDİL için Oxford 3000 destekli, CEFR A1-C2 kademeli kelime oyunu. Electron ile Windows ve Linux masaüstü sürümü."),
        roket=("Roket & Radar Simülasyonu", "HTML5 Canvas ve 2D fizik ile gerçek zamanlı radar taraması, hedef kilitleme ve balistik uçuş."),
        sabikali=("Sabıkalı Patiler", "İpuçlarını birleştirerek suçluyu bulduğunuz, saf JavaScript ile yazılmış tek dosyalık dedektiflik oyunu."),
        kalite=("Kalite Elçisi", "YÖKAK kalite güvence standartlarını interaktif senaryolarla öğreten, tarayıcının ES modülleriyle çalışan bağımlılıksız oyun motoru."),
        iskur=("İŞKUR Portal Otomasyon Botu", "Excel yoklama verilerini İŞKUR portalındaki devam çizelgelerine eşleyen ve 40+ sayfayı aktaran Python otomasyonu."),
        savunma=("Savunma Harcaması Veri Analizi", "SIPRI askeri harcamaları ile Dünya Bankası göstergelerini birleştiren korelogram, dumbbell ve boxplot görselleştirmeleri (R)."),
    ),
)

EN = dict(
    lang="en", locale="en_US", path="/en/", other_path="/", other_label="TR", other_name="Türkçe",
    title="Kerem Efe Yiğit — Full-Stack & AI Software Developer",
    description="Kerem Efe Yiğit: software developer building enterprise web systems, computer vision and multi-agent AI orchestration. Selected work, approach and contact.",
    role="Full-Stack & AI Software Developer",
    skip="Skip to content", nav_label="Main navigation",
    nav=[("work", "Work"), ("approach", "Approach"), ("skills", "Skills"), ("contact", "Contact")],
    theme_label="Toggle theme", theme_dark="Dark theme", theme_light="Light theme",
    hero_kicker="Software developer",
    hero_title="Enterprise systems, computer vision and AI agents.",
    hero_lead="I build end to end, from web platforms to edge inference. I finish work with tests: I try to catch leaked secrets, broken links and misleading tests before a change ships, not after.",
    now_title="Currently working on",
    now=[("Agent Ofisi", "local multi-agent orchestration, rule enforcement and a CI loop"),
         ("YEMEDENÖNCE", "web and mobile product for verified local-eatery discovery"),
         ("Pano Hesaplama", "computer vision pipeline for measuring ad billboards")],
    cta_work="See the work", cta_contact="Get in touch",
    work_title="Selected work", work_intro="Four main projects and other work. Closed-source projects are labelled as such.",
    more_title="More work",
    vis={"open": "Open code", "private": "Private · closed source", "corporate": "Corporate · closed source"},
    link_labels={"repo": "Source code", "play": "Play in browser", "report": "Live report"},
    license_word="License",
    approach_title="How I work",
    approach=[
        ("Security is part of the design",
         "Passwords are hashed with bcrypt, tickets are signed with HMAC-SHA256, queries use prepared statements and requests are rate limited. I use scanning and .gitignore rules to keep secrets out of code and git history."),
        ("Measurable vision systems",
         "I build inference pipelines that measure with stereo camera calibration, YOLOv8 segmentation and OpenCV coordinate transforms, and that can run on edge devices."),
        ("Supervised agents",
         "I run LLM agents under rules: agents do not merge, do not read secrets, every change passes tests, and decisions stay with a human."),
        ("Finishing with tests",
         "Regression, responsive, accessibility and security tests run on every change. Work is not done while a test is red."),
    ],
    skills_title="Skills",
    skill_groups={"ai": "AI & vision", "backend": "Backend", "frontend": "Frontend & mobile", "data": "Data & DevOps"},
    contact_title="Contact", contact_lead="Write to me about projects, collaboration or technical consulting.",
    mail_label="Email", mail_noscript="keremefeyigit [at] outlook.com", linkedin_label="LinkedIn", github_label="GitHub",
    footer="The source code of this page is MIT licensed.", source="Source code", updated="Last updated",
    projects=dict(
        pano=("Pano Hesaplama (Billboard Measurement System)", "Computer vision system that measures urban ad billboards with OpenCV and YOLOv8 segmentation, with stereo distance analysis and coordinate tracking."),
        yemedenonce=("YEMEDENÖNCE", "Ad-free, verified local-eatery discovery using Bayesian statistics, Gemini sentiment analysis and H3 geospatial indexing."),
        asu=("ASÜ Community Platform (ASÜConnect)", "49-table enterprise LAMP system: multi-level approval workflow, HMAC-SHA256 signed QR ticketing and role-based access. Team project."),
        agent=("Agent Ofisi (Agent Office)", "Local orchestration of Claude and agy agents over the hcom protocol: rule enforcement, a CI verification loop and task hand-off."),
        siyos=("Apartment Management System (SIYOS)", "Resident requests, dues and expense tracking; a REST platform on Express and SQLite with JWT, rate limiting and security headers."),
        usip=("USİP — University-Industry Collaboration Portal", "B2B/B2C portal connecting technology transfer offices, career centers, academics, students and companies; manages R&D and hiring workflows (MVP)."),
        yds=("YDS Vocabulary Game", "Oxford 3000 backed, CEFR A1-C2 progressive vocabulary game for the YDS and YÖKDİL exams. Electron desktop builds for Windows and Linux."),
        roket=("Rocket & Radar Simulation", "Real-time radar sweep, target lock and ballistic flight with HTML5 Canvas and 2D physics."),
        sabikali=("Sabıkalı Patiler", "A single-file detective game in plain JavaScript where you combine clues to find the culprit."),
        kalite=("Quality Ambassador", "Dependency-free game engine running on native ES modules that teaches YÖKAK quality-assurance standards through interactive scenarios."),
        iskur=("İŞKUR Portal Automation Bot", "Python automation that maps Excel attendance data onto the attendance sheets of the İŞKUR portal and transfers 40+ pages."),
        savunma=("Defence Spending Data Analysis", "Correlogram, dumbbell and boxplot visualisations joining SIPRI military spending with World Bank indicators (R)."),
    ),
)

# Tasarım kararları

## Hedef
Eski site (tek 40 KB HTML, Google Fonts + Font Awesome CDN, indigo-pembe gradyan, ortalanmış hero, cam kartlar) şu sorunlara sahipti: 390 px'te **230 px yatay taşma**, mobilde bozulan üst menü, 11 `target="_blank"` bağlantıda `rel` eksikliği, kırık "canlı rapor" bağlantısı (404), `heading-order` erişilebilirlik ihlali, sosyal paylaşım meta'sı yok, tek dil, "Açık Kaynak" etiketinin CC BY-NC-ND projelere yapıştırılması ve "tam korumalı" gibi doğrulanamayan iddialar.

## Yön: "mühendislik defteri"
Jenerik "AI portfolyosu" görünümünden bilinçli kaçınıldı.
- **Kâğıt sıcaklığında açık tema** (`#f3efe6`) ve **kömür koyu tema** (`#101215`); tek vurgu rengi (yanık turuncu / amber). Gradyan ve cam efekti yok.
- **Tipografi hiyerarşisi:** Fraunces (görsel başlık, sürekli seri), IBM Plex Sans (okuma), IBM Plex Mono (etiket, numara, meta). Büyük ölçekli başlık, dar ölçü (≤ 62ch).
- **Asimetrik düzen:** masaüstünde yapışkan sol ray (isim, rol, gezinme, dil/tema), sağda içerik; mobilde üstte kompakt çubuk + 2×2/4'lü gezinme.
- **Editoryal liste:** projeler kart ızgarası değil, numaralı satırlar; kodu kapalı olanlar açıkça etiketli.
- **Hareket:** yalnızca hafif kayma (opacity yok: içerik hiçbir zaman gizlenmez); `prefers-reduced-motion` ile tamamen kapanır.

## Mühendislik kararları
| Karar | Neden |
|---|---|
| Statik üretici (`tools/build.py`) + commit'lenen çıktı | TR/EN yapısı birbirinden sapmaz; Pages'te derleme adımı yok; CI "çıktı güncel mi" diye denetler |
| Yazı tipleri kendi sunucumuzda, `unicode-range` alt kümeleri | CDN/izleme yok; Türkçe karakterler için latin + latin-ext; ≈ 8 küçük dosya |
| CSP `default-src 'none'` + `script-src 'self'` | Satır içi kod yok; XSS yüzeyi minimum. (GitHub Pages yanıt başlığı ekletmez: `meta` ile uygulanır, `frame-ancestors` gibi yönergeler meta'da çalışmaz.) |
| `theme.js` küçük ve senkron, `main.js` `defer` | Tema titremesi olmasın, işleme engellenmesin |
| E-posta JS ile birleştirilir | Düz metin adres toplayıcı botlara kolay hedef |
| 44 px dokunma hedefi, `:focus-visible` halkası, skip link | Mobil ve klavye erişilebilirliği |

## Stitch (Google) brief'i
Stitch yerleşik tarayıcıdan açılmadı (boş sayfa), Chrome eklentisi de bağlı değildi; bu yüzden tasarım elle yapıldı. Alternatif yönler üretmek istersen Stitch'e şu brief'i yapıştır:

> Design a personal developer portfolio, desktop (1440) and mobile (390), light and dark. Editorial, not a SaaS template. Warm paper background (#f3efe6) and charcoal (#101215). One accent: burnt orange (#a23b08) / amber (#f0a24a). No gradients, no glassmorphism. Display serif (Fraunces) for headings, IBM Plex Sans for body, IBM Plex Mono for labels and numbers. Desktop: sticky left rail with name, role, numbered nav (01 Work, 02 Approach, 03 Skills, 04 Contact), language and theme toggles; right column with a huge headline "Enterprise systems, computer vision and AI agents.", a short lead, two buttons, a "Currently working on" list, then numbered project rows (title, one-line description, mono tag pills, visibility label such as "Open code · License: MIT" or "Private · closed source", links), an "How I work" 2×2 principles grid, a 4-column skills matrix and a large serif email link. Mobile: compact top bar, 2×2 nav grid, single column. Generous whitespace, thin rules instead of cards, 44px touch targets, WCAG AA contrast.

Çıktı olarak gelen HTML/CSS doğrudan kullanılmamalı: `tools/content.py` içeriğine ve `assets/css/style.css` değerlerine uyarlanıp aynı testlerden geçirilmelidir.

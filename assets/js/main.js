/* İsteğe bağlı iyileştirmeler. JS kapalıyken sayfa tamamen çalışır (tema sistem ayarını izler, e-posta metin olarak görünür). */
(function () {
  "use strict";
  var root = document.documentElement;

  function effectiveTheme() {
    var t = root.getAttribute("data-theme");
    if (t === "dark" || t === "light") return t;
    return window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
  }

  function syncThemeButton(btn) {
    var dark = effectiveTheme() === "dark";
    btn.setAttribute("aria-pressed", dark ? "true" : "false");
    btn.textContent = dark ? "◑" : "◐";
    btn.setAttribute("aria-label", btn.getAttribute(dark ? "data-label-light" : "data-label-dark"));
  }

  var themeBtn = document.querySelector("[data-theme-toggle]");
  if (themeBtn) {
    themeBtn.hidden = false;
    syncThemeButton(themeBtn);
    themeBtn.addEventListener("click", function () {
      var next = effectiveTheme() === "dark" ? "light" : "dark";
      root.setAttribute("data-theme", next);
      try { localStorage.setItem("theme", next); } catch (e) { /* yok say */ }
      syncThemeButton(themeBtn);
    });
  }

  /* E-posta adresi HTML'de düz metin olarak yer almaz (toplayıcı botlara karşı); JS ile birleştirilir. */
  document.querySelectorAll("[data-mail-user]").forEach(function (a) {
    var addr = a.getAttribute("data-mail-user") + "@" + a.getAttribute("data-mail-domain");
    a.setAttribute("href", "mailto:" + addr);
    a.textContent = addr;
  });

  /* Gezinmede görünür bölümü işaretle. */
  var links = Array.prototype.slice.call(document.querySelectorAll("[data-nav] a[href^='#']"));
  if ("IntersectionObserver" in window && links.length) {
    var map = {};
    links.forEach(function (a) { map[a.getAttribute("href").slice(1)] = a; });
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting && map[en.target.id]) {
          links.forEach(function (l) { l.removeAttribute("aria-current"); });
          map[en.target.id].setAttribute("aria-current", "true");
        }
      });
    }, { rootMargin: "-35% 0px -55% 0px" });
    Object.keys(map).forEach(function (id) { var el = document.getElementById(id); if (el) io.observe(el); });
  }
})();

/* Sayfa çizilmeden önce kayıtlı temayı uygular (titreme olmasın). Depolama yoksa sessizce atlanır. */
(function () {
  try {
    var t = localStorage.getItem("theme");
    if (t === "dark" || t === "light") document.documentElement.setAttribute("data-theme", t);
  } catch (e) { /* özel pencere / depolama kapalı */ }
})();

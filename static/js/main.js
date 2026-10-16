(function () {
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };

  var btn = $("#menu-btn"), menu = $("#mobile-menu");
  if (btn && menu) {
    btn.addEventListener("click", function () {
      var open = menu.classList.toggle("hidden") === false;
      menu.classList.toggle("flex", open);
      btn.setAttribute("aria-expanded", String(open));
    });
  }

  var path = location.pathname.replace(/\/$/, "") || "/";
  $$("[data-nav]").forEach(function (a) {
    var p = a.getAttribute("href").replace(/\/$/, "") || "/";
    if (p === path) { a.classList.add("active"); a.setAttribute("aria-current", "page"); }
  });

  var header = $("#site-header");
  var onScroll = function () { if (header) header.classList.toggle("scrolled", window.scrollY > 8); };
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  var items = $$(".gallery-item");
  $$(".filter-btn").forEach(function (b) {
    b.addEventListener("click", function () {
      $$(".filter-btn").forEach(function (x) { x.setAttribute("aria-pressed", "false"); });
      b.setAttribute("aria-pressed", "true");
      var f = b.dataset.filter;
      items.forEach(function (it) { it.style.display = (f === "all" || it.dataset.cat === f) ? "" : "none"; });
    });
  });

  var lb = $("#lightbox");
  if (lb) {
    var img = $("img", lb), closeBtn = $("#lightbox-close"), lastFocus = null;
    var close = function () { lb.classList.remove("open"); if (lastFocus) lastFocus.focus(); };
    $$(".gallery-item button").forEach(function (b) {
      b.addEventListener("click", function () {
        lastFocus = b;
        img.src = b.dataset.full;
        img.alt = $("img", b).alt;
        lb.classList.add("open");
        closeBtn.focus();
      });
    });
    lb.addEventListener("click", function (e) { if (e.target !== img) close(); });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape") close(); });
  }

  $$(".faq-q").forEach(function (q) {
    q.addEventListener("click", function () {
      var a = document.getElementById(q.getAttribute("aria-controls"));
      var open = a.classList.toggle("hidden") === false;
      q.setAttribute("aria-expanded", String(open));
      $("span", q).textContent = open ? "-" : "+";
    });
  });

  var reveals = $$(".reveal");
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); } });
    }, { threshold: 0.12 });
    reveals.forEach(function (r) { io.observe(r); });
  } else {
    reveals.forEach(function (r) { r.classList.add("in"); });
  }
})();

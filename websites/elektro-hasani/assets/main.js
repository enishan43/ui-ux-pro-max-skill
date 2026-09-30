(function () {
  "use strict";

  var doc = document.documentElement;
  doc.classList.add("js");

  var OFFICE_TEL = "02381 4362971";
  var MOBILE_TEL = "0172 5432820";
  var EMAIL = "elektro.hasani@googlemail.com";

  /* ---------- Mobile Navigation ---------- */
  var toggle = document.querySelector(".nav-toggle");
  var nav = document.getElementById("nav");

  function setNav(open) {
    toggle.setAttribute("aria-expanded", String(open));
    toggle.setAttribute("aria-label", open ? "Menü schließen" : "Menü öffnen");
    nav.classList.toggle("is-open", open);
  }

  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      setNav(toggle.getAttribute("aria-expanded") !== "true");
    });
    nav.addEventListener("click", function (e) {
      if (e.target.closest("a")) setNav(false);
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && nav.classList.contains("is-open")) {
        setNav(false);
        toggle.focus();
      }
    });
  }

  /* Header: Menüposition anpassen, sobald die Topbar weggescrollt ist */
  var topbar = document.querySelector(".topbar");
  function onScroll() {
    var h = topbar ? topbar.offsetHeight : 0;
    document.body.classList.toggle("is-scrolled", window.scrollY > h);
  }
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  /* ---------- Leistung im Formular vorauswählen ---------- */
  var select = document.getElementById("f-service");
  document.querySelectorAll("[data-service]").forEach(function (link) {
    link.addEventListener("click", function () {
      if (!select) return;
      var wanted = link.getAttribute("data-service");
      for (var i = 0; i < select.options.length; i++) {
        if (select.options[i].text === wanted) { select.selectedIndex = i; break; }
      }
    });
  });

  /* ---------- Einblend-Animationen ---------- */
  var revealTargets = document.querySelectorAll(
    ".section__head, .service, .why__list li, .step, .review, .faq details, .chips, .video, .videos__empty"
  );
  var without = document.querySelector(".without");

  if ("IntersectionObserver" in window) {
    revealTargets.forEach(function (el) { el.classList.add("reveal"); });
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        entry.target.classList.add(entry.target === without ? "is-on" : "is-visible");
        io.unobserve(entry.target);
      });
    }, { threshold: 0.15, rootMargin: "0px 0px -40px 0px" });
    revealTargets.forEach(function (el) { io.observe(el); });
    if (without) io.observe(without);
  } else if (without) {
    without.classList.add("is-on");
  }

  /* ---------- Geöffnet / Geschlossen (Zeitzone Hamm) ---------- */
  var statusEl = document.getElementById("open-status");
  var HOURS = { 1: [8, 17], 2: [8, 17], 3: [8, 17], 4: [8, 17], 5: [8, 13] };
  var DAY_NAMES = ["So", "Mo", "Di", "Mi", "Do", "Fr", "Sa"];

  function berlinNow() {
    try {
      var parts = new Intl.DateTimeFormat("en-GB", {
        timeZone: "Europe/Berlin", weekday: "short", hour: "2-digit", minute: "2-digit", hour12: false
      }).formatToParts(new Date());
      var map = {};
      parts.forEach(function (p) { map[p.type] = p.value; });
      var day = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"].indexOf(map.weekday);
      return { day: day, minutes: (parseInt(map.hour, 10) % 24) * 60 + parseInt(map.minute, 10) };
    } catch (e) {
      return null;
    }
  }

  function nextOpening(now) {
    for (var i = 0; i < 8; i++) {
      var d = (now.day + i) % 7;
      var h = HOURS[d];
      if (!h) continue;
      if (i === 0 && now.minutes >= h[0] * 60) continue;
      var label = i === 0 ? "heute" : i === 1 ? "morgen" : DAY_NAMES[d];
      return label + " um " + (h[0] < 10 ? "0" : "") + h[0] + ":00 Uhr";
    }
    return "";
  }

  if (statusEl) {
    var now = berlinNow();
    if (now && now.day >= 0) {
      var h = HOURS[now.day];
      var open = h && now.minutes >= h[0] * 60 && now.minutes < h[1] * 60;
      statusEl.textContent = open
        ? "Büro jetzt geöffnet – bis " + h[1] + ":00 Uhr"
        : "Büro geschlossen – öffnet " + nextOpening(now) + ". Notfall: " + MOBILE_TEL;
      statusEl.classList.toggle("is-open", !!open);
      statusEl.hidden = false;
    }
  }

  /* ---------- Kontaktformular → vorbereitete E-Mail ---------- */
  var form = document.getElementById("contact-form");

  function showError(input, errEl, show) {
    input.setAttribute("aria-invalid", show ? "true" : "false");
    if (show) input.setAttribute("aria-describedby", errEl.id);
    else input.removeAttribute("aria-describedby");
    errEl.hidden = !show;
  }

  if (form) {
    var fields = {
      name: { el: document.getElementById("f-name"), err: document.getElementById("f-name-err"),
        ok: function (v) { return v.trim().length >= 2; } },
      phone: { el: document.getElementById("f-phone"), err: document.getElementById("f-phone-err"),
        ok: function (v) { return v.replace(/[^\d]/g, "").length >= 6; } },
      mail: { el: document.getElementById("f-mail"), err: document.getElementById("f-mail-err"),
        ok: function (v) { return v.trim() === "" || /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v.trim()); } },
      msg: { el: document.getElementById("f-msg"), err: document.getElementById("f-msg-err"),
        ok: function (v) { return v.trim().length >= 5; } }
    };
    var privacy = document.getElementById("f-privacy");
    var privacyErr = document.getElementById("f-privacy-err");
    var success = document.getElementById("form-success");

    Object.keys(fields).forEach(function (k) {
      var f = fields[k];
      f.el.addEventListener("blur", function () {
        if (f.el.value !== "" || f.el.getAttribute("aria-invalid") === "true") {
          showError(f.el, f.err, !f.ok(f.el.value));
        }
      });
      f.el.addEventListener("input", function () {
        if (f.el.getAttribute("aria-invalid") === "true" && f.ok(f.el.value)) showError(f.el, f.err, false);
      });
    });
    privacy.addEventListener("change", function () {
      if (privacy.checked) showError(privacy, privacyErr, false);
    });

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var firstInvalid = null;
      Object.keys(fields).forEach(function (k) {
        var f = fields[k];
        var bad = !f.ok(f.el.value);
        showError(f.el, f.err, bad);
        if (bad && !firstInvalid) firstInvalid = f.el;
      });
      var privacyBad = !privacy.checked;
      showError(privacy, privacyErr, privacyBad);
      if (privacyBad && !firstInvalid) firstInvalid = privacy;
      if (firstInvalid) { firstInvalid.focus(); return; }

      var service = select && select.value ? select.value : "Allgemeine Anfrage";
      var callback = document.getElementById("f-callback").checked;
      var subject = "Anfrage über die Website: " + service;
      var body = [
        "Hallo Elektro Hasani,",
        "",
        fields.msg.el.value.trim(),
        "",
        "Leistung: " + service,
        "Name: " + fields.name.el.value.trim(),
        "Telefon: " + fields.phone.el.value.trim(),
        fields.mail.el.value.trim() ? "E-Mail: " + fields.mail.el.value.trim() : null,
        callback ? "Bitte um Rückruf." : null,
        "",
        "Viele Grüße",
        fields.name.el.value.trim()
      ].filter(function (l) { return l !== null; }).join("\n");

      window.location.href = "mailto:" + EMAIL +
        "?subject=" + encodeURIComponent(subject) +
        "&body=" + encodeURIComponent(body);
      success.hidden = false;
    });
  }

  /* ---------- Videos ---------- */
  var grid = document.getElementById("video-grid");
  var empty = document.getElementById("video-empty");
  var videos = Array.isArray(window.HASANI_VIDEOS) ? window.HASANI_VIDEOS : [];

  function el(tag, attrs, text) {
    var node = document.createElement(tag);
    Object.keys(attrs || {}).forEach(function (k) { node.setAttribute(k, attrs[k]); });
    if (text) node.textContent = text;
    return node;
  }

  function youtubeId(v) {
    var id = String(v || "").trim();
    var m = id.match(/(?:v=|youtu\.be\/|shorts\/|embed\/)([\w-]{11})/);
    if (m) id = m[1];
    return /^[\w-]{11}$/.test(id) ? id : null;
  }

  var rendered = 0;
  if (grid) {
    videos.forEach(function (v) {
      if (!v || (!v.datei && !v.youtube)) return;
      var title = v.titel || "Video von Elektro Hasani";
      var fig = el("figure", { "class": "video" + (v.hochformat ? " video--portrait" : "") });
      var frame = el("div", { "class": "video__frame" });

      if (v.datei) {
        var attrs = { controls: "", preload: "none", playsinline: "", "aria-label": title };
        if (v.vorschaubild) attrs.poster = v.vorschaubild;
        var video = el("video", attrs);
        video.appendChild(el("source", { src: v.datei, type: "video/mp4" }));
        video.appendChild(document.createTextNode("Ihr Browser kann dieses Video nicht abspielen."));
        frame.appendChild(video);
      } else {
        var id = youtubeId(v.youtube);
        if (!id) return;
        if (v.vorschaubild) frame.appendChild(el("img", { src: v.vorschaubild, alt: "", loading: "lazy" }));
        var consent = el("div", { "class": "video__consent" });
        var btn = el("button", { type: "button", "class": "btn btn--primary" });
        btn.innerHTML = '<svg class="icon" aria-hidden="true"><use href="#i-play"/></svg>';
        btn.appendChild(document.createTextNode(" Video abspielen"));
        btn.setAttribute("aria-label", "Video abspielen: " + title);
        var note = el("p", {}, "Beim Abspielen werden Daten an YouTube (Google) übertragen. ");
        var more = el("a", { href: "datenschutz.html#youtube", style: "color:#fff" }, "Mehr erfahren");
        note.appendChild(more);
        consent.appendChild(btn);
        consent.appendChild(note);
        frame.appendChild(consent);
        btn.addEventListener("click", function () {
          var iframe = el("iframe", {
            src: "https://www.youtube-nocookie.com/embed/" + id + "?autoplay=1&rel=0",
            title: title,
            allow: "accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture",
            allowfullscreen: ""
          });
          frame.innerHTML = "";
          frame.appendChild(iframe);
          iframe.focus();
        });
      }

      fig.appendChild(frame);
      fig.appendChild(el("figcaption", {}, title));
      grid.appendChild(fig);
      rendered++;
    });
  }
  if (empty) empty.hidden = rendered > 0;

  /* ---------- Jahr im Footer ---------- */
  var year = document.getElementById("year");
  if (year) year.textContent = String(new Date().getFullYear());
})();

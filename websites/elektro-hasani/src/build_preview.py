"""Baut eine einzelne, eigenständige HTML-Datei zum Ansehen (Vorschau).

CSS, JavaScript und die Video-Liste werden eingebettet. Impressum und
Datenschutz stecken als Pop-up-Fenster (<dialog>) in der Datei und öffnen
sich erst über die Links im Footer bzw. im Formular. Die Datei funktioniert
ohne weitere Dateien, einfach per Doppelklick im Browser öffnen.

Aufruf:  python3 src/build_preview.py   (nach src/build.py)
"""
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "elektro-hasani-komplett.html")


def read(*parts):
    with open(os.path.join(ROOT, *parts), encoding="utf-8") as f:
        return f.read()


MODAL_CSS = """
/* ---------- Impressum / Datenschutz als Pop-up (nur Einzeldatei) ---------- */
html:has(dialog.legal-modal[open]) { overflow: hidden; }
.legal-modal {
  width: min(760px, calc(100% - 32px)); max-width: none; max-height: calc(100% - 48px);
  padding: 0; border: 0; border-radius: 18px; overflow: hidden;
  background: var(--bg-alt); color: var(--text); box-shadow: 0 24px 60px rgb(6 20 41 / 35%);
}
.legal-modal[open] { display: flex; flex-direction: column; }
.legal-modal::backdrop { background: rgb(6 20 41 / 68%); }
.legal-modal__bar {
  display: flex; align-items: center; justify-content: space-between; gap: 12px;
  padding: 10px 10px 10px 22px; background: var(--navy-900); color: #fff; flex: none;
}
.legal-modal__title { font-size: 1.15rem; font-weight: 800; color: #fff; margin: 0; }
.legal-modal__close {
  display: grid; place-items: center; width: 44px; height: 44px; border: 0; border-radius: 10px;
  background: rgb(255 255 255 / 10%); color: #fff; cursor: pointer; font: inherit; font-size: 1.7rem; line-height: 1;
}
.legal-modal__close:hover { background: rgb(255 255 255 / 20%); }
.legal-modal__body { overflow-y: auto; overscroll-behavior: contain; padding: 8px 24px 28px; max-width: none; }
.legal-modal__body .legal__lead { margin-top: 12px; }
@media (max-width: 640px) {
  .legal-modal { width: 100%; height: 100%; max-height: 100%; margin: 0; border-radius: 0; }
  .legal-modal__bar { padding-top: calc(10px + env(safe-area-inset-top, 0px)); }
  .legal-modal__body { padding: 4px 16px calc(28px + env(safe-area-inset-bottom, 0px)); }
}
"""

MODAL_JS = """
(function () {
  "use strict";
  function legalFor(id) {
    var el = id && document.getElementById(id);
    if (!el) return null;
    var dlg = el.tagName === "DIALOG" ? el : el.closest("dialog.legal-modal");
    return dlg ? { dialog: dlg, target: el === dlg ? null : el } : null;
  }
  function openLegal(hit) {
    document.querySelectorAll("dialog.legal-modal[open]").forEach(function (d) {
      if (d !== hit.dialog) d.close();
    });
    if (!hit.dialog.open) hit.dialog.showModal();
    var body = hit.dialog.querySelector(".legal-modal__body");
    if (hit.target) {
      if (hit.target.tagName === "DETAILS") hit.target.open = true;
      hit.target.scrollIntoView({ block: "start" });
    } else if (body) {
      body.scrollTop = 0;
    }
  }
  document.addEventListener("click", function (e) {
    var a = e.target.closest('a[href^="#"]');
    if (!a) return;
    var id = a.getAttribute("href").slice(1);
    var hit = legalFor(id);
    if (hit) { e.preventDefault(); openLegal(hit); return; }
    var inside = a.closest("dialog.legal-modal");
    if (inside) inside.close();
  });
  document.querySelectorAll("dialog.legal-modal").forEach(function (d) {
    d.querySelector(".legal-modal__close").addEventListener("click", function () { d.close(); });
    d.addEventListener("click", function (e) { if (e.target === d) d.close(); });
  });
  function fromHash() {
    var hit = legalFor(location.hash.slice(1));
    if (hit) openLegal(hit);
  }
  fromHash();
  window.addEventListener("hashchange", fromHash);
})();
"""


def legal_dialog(filename, dialog_id, title):
    page = read(filename)
    body = re.search(r'<main class="container legal">(.*?)</main>', page, re.S).group(1)
    body = re.sub(r"<!--.*?-->", "", body, flags=re.S)
    body = re.sub(r"<script>.*?</script>", "", body, flags=re.S)
    body = re.sub(r"\s*<h1>.*?</h1>", "", body, count=1, flags=re.S)  # Titel steht in der Leiste
    body = body.replace('href="index.html"', 'href="#top"')
    body = body.replace('href="impressum.html"', 'href="#impressum"')
    body = body.replace('href="datenschutz.html"', 'href="#datenschutz"')
    return (f'<dialog class="legal-modal" id="{dialog_id}" aria-labelledby="{dialog_id}-title">'
            f'<div class="legal-modal__bar"><h2 class="legal-modal__title" id="{dialog_id}-title">{title}</h2>'
            f'<button type="button" class="legal-modal__close" aria-label="{title} schließen">×</button></div>'
            f'<div class="legal legal-modal__body">{body}</div></dialog>')


html = read("index.html")
css = read("assets", "style.css")
js = read("assets", "main.js").replace('"datenschutz.html#youtube"', '"#youtube"')
videos = read("videos.js")

html = html.replace('<link rel="stylesheet" href="assets/style.css">',
                    "<style>\n" + css + MODAL_CSS + "</style>")
html = html.replace('<script src="videos.js"></script>', "<script>\n" + videos + "\n</script>")
html = html.replace('<script src="assets/main.js"></script>',
                    "<script>\n" + js + "\n</script>\n<script>" + MODAL_JS + "</script>")
html = html.replace('href="impressum.html"', 'href="#impressum"')
html = html.replace('href="datenschutz.html"', 'href="#datenschutz"')
html = html.replace("</footer>", "</footer>\n\n<!-- Impressum & Datenschutz: erst per Link sichtbar -->\n"
                    + legal_dialog("impressum.html", "impressum", "Impressum") + "\n"
                    + legal_dialog("datenschutz.html", "datenschutz", "Datenschutz") + "\n", 1)

for leftover in ('href="assets/', 'src="assets/', 'src="videos.js"', "impressum.html", "datenschutz.html"):
    assert leftover not in html, leftover

with open(OUT, "w", encoding="utf-8") as f:
    f.write(html)
print("Vorschau geschrieben:", OUT, len(html), "Zeichen")

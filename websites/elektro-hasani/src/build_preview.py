"""Baut eine einzelne, eigenständige HTML-Datei zum Ansehen (Vorschau).

CSS, JavaScript und die Video-Liste werden eingebettet, Impressum und
Datenschutz als Abschnitte am Seitenende angehängt. Die Datei funktioniert
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


def legal_section(filename, section_id):
    page = read(filename)
    body = re.search(r'<main class="container legal">(.*?)</main>', page, re.S).group(1)
    body = re.sub(r"<!--.*?-->", "", body, flags=re.S)
    body = body.replace("<h1>", '<h2 class="section__title">').replace("</h1>", "</h2>")
    # Querverweise innerhalb der Einzeldatei
    body = body.replace('href="index.html"', 'href="#top"')
    body = body.replace('href="impressum.html"', 'href="#impressum"')
    body = body.replace('href="datenschutz.html"', 'href="#datenschutz"')
    return (f'<section class="legal-inline" id="{section_id}"><div class="container legal">'
            f'{body}</div></section>')


html = read("index.html")
css = read("assets", "style.css")
js = read("assets", "main.js").replace('"datenschutz.html#youtube"', '"#youtube"')
videos = read("videos.js")

html = html.replace('<link rel="stylesheet" href="assets/style.css">',
                    "<style>\n" + css + "\n.legal-inline { background: var(--bg-alt); border-top: 1px solid var(--border); }\n</style>")
html = html.replace('<script src="videos.js"></script>', "<script>\n" + videos + "\n</script>")
html = html.replace('<script src="assets/main.js"></script>', "<script>\n" + js + "\n</script>")
html = html.replace('href="impressum.html"', 'href="#impressum"')
html = html.replace('href="datenschutz.html"', 'href="#datenschutz"')
html = html.replace("</main>", legal_section("impressum.html", "impressum")
                    + legal_section("datenschutz.html", "datenschutz") + "\n</main>", 1)

for leftover in ('href="assets/', 'src="assets/', 'src="videos.js"', "impressum.html", "datenschutz.html"):
    assert leftover not in html, leftover

with open(OUT, "w", encoding="utf-8") as f:
    f.write(html)
print("Vorschau geschrieben:", OUT, len(html), "Zeichen")

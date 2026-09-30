"""Baut index.html aus src/index.template.html + src/icons.svg + src/hero.svg.

Aufruf:  python3 src/build.py
"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

subprocess.run([sys.executable, os.path.join(HERE, "gen_hero.py")], check=True)

def read(name):
    with open(os.path.join(HERE, name), encoding="utf-8") as f:
        return f.read()

html = read("index.template.html")
html = html.replace("<!--ICONS-->", read("icons.svg").strip())
html = html.replace("<!--HERO_SVG-->", read("hero.svg").strip())
assert "<!--ICONS-->" not in html and "<!--HERO_SVG-->" not in html

with open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8") as f:
    f.write(html)
print("index.html geschrieben:", len(html), "Zeichen")

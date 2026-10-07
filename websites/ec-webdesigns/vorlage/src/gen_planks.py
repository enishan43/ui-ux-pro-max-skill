"""Erzeugt die Holzdielen-Grafik für den Hero der Vorlage (planks.svg)."""
import os
import random

random.seed(11)
W, H = 640, 760
tones = ["#C98B4B", "#B97A3E", "#D69A5A", "#A86C35", "#C2844A", "#DDA766"]
out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMid slice" aria-hidden="true" focusable="false">']
x = 0
while x < W:
    w = random.choice([88, 104, 120, 136])
    tone = random.choice(tones)
    out.append(f'<rect x="{x}" y="0" width="{w}" height="{H}" fill="{tone}"/>')
    # Maserung: leicht gewellte Linien
    for _ in range(random.randint(6, 10)):
        gx = x + random.uniform(8, w - 8)
        amp = random.uniform(2, 7)
        d = f"M{gx:.1f} 0"
        y = 0
        while y < H:
            y2 = y + random.uniform(60, 120)
            d += f" Q{gx + random.choice([-1, 1]) * amp:.1f} {(y + y2) / 2:.1f} {gx + random.uniform(-2, 2):.1f} {y2:.1f}"
            y = y2
        out.append(f'<path d="{d}" fill="none" stroke="#5E3A1A" stroke-opacity="{random.uniform(.12, .28):.2f}" stroke-width="{random.uniform(.8, 1.8):.1f}"/>')
    # Astloch
    if random.random() < 0.6:
        kx, ky = x + w * random.uniform(.3, .7), random.uniform(80, H - 80)
        out.append(f'<ellipse cx="{kx:.0f}" cy="{ky:.0f}" rx="{random.uniform(6, 11):.0f}" ry="{random.uniform(12, 20):.0f}" fill="#6B4220" fill-opacity=".45"/>')
        out.append(f'<ellipse cx="{kx:.0f}" cy="{ky:.0f}" rx="{random.uniform(12, 18):.0f}" ry="{random.uniform(26, 36):.0f}" fill="none" stroke="#6B4220" stroke-opacity=".22" stroke-width="1.5"/>')
    # Fuge
    out.append(f'<rect x="{x + w - 2}" y="0" width="2" height="{H}" fill="#3B2410" fill-opacity=".45"/>')
    x += w
out.append("</svg>")
# Ausgabe in src/planks.svg; den Inhalt in index.html in .hero__img einsetzen
path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "planks.svg")
open(path, "w").write("".join(out))
print("planks.svg", sum(map(len, out)), "bytes")

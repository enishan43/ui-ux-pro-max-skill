"""Generates the aerial 'night neighbourhood' SVG for the Elektro Hasani hero."""
import random

random.seed(7)
W, H = 1600, 900
ROADS_H = [300, 640]          # y of horizontal roads (centre)
ROADS_V = [520, 1080]         # x of vertical roads (centre)
ROAD_W = 56

out = []
a = out.append
a(f'<svg class="hero-map" viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMid slice" '
  'xmlns="http://www.w3.org/2000/svg" aria-hidden="true" focusable="false">')
a('<defs>'
  '<radialGradient id="glow"><stop offset="0" stop-color="#FFD166" stop-opacity="1"/>'
  '<stop offset=".4" stop-color="#FFB703" stop-opacity=".45"/>'
  '<stop offset="1" stop-color="#FFB703" stop-opacity="0"/></radialGradient>'
  '<pattern id="grass" width="14" height="14" patternUnits="userSpaceOnUse">'
  '<rect width="14" height="14" fill="#10284A"/><circle cx="3" cy="4" r="1" fill="#12294C"/>'
  '<circle cx="10" cy="11" r="1" fill="#12294C"/></pattern>'
  '</defs>')
a(f'<rect width="{W}" height="{H}" fill="url(#grass)"/>')

# roads
for y in ROADS_H:
    a(f'<rect x="0" y="{y-ROAD_W/2}" width="{W}" height="{ROAD_W}" fill="#1A2F52"/>')
    a(f'<line x1="0" y1="{y}" x2="{W}" y2="{y}" stroke="#2C4670" stroke-width="3" stroke-dasharray="22 20"/>')
for x in ROADS_V:
    a(f'<rect x="{x-ROAD_W/2}" y="0" width="{ROAD_W}" height="{H}" fill="#1A2F52"/>')
    a(f'<line x1="{x}" y1="0" x2="{x}" y2="{H}" stroke="#2C4670" stroke-width="3" stroke-dasharray="22 20"/>')
# sidewalks
for y in ROADS_H:
    for off in (-ROAD_W/2-6, ROAD_W/2):
        a(f'<rect x="0" y="{y+off}" width="{W}" height="6" fill="#223A60"/>')
for x in ROADS_V:
    for off in (-ROAD_W/2-6, ROAD_W/2):
        a(f'<rect x="{x+off}" y="0" width="6" height="{H}" fill="#223A60"/>')

# power lines (animated current) along roads
a('<g class="current" fill="none" stroke="#FFC21A" stroke-width="3" stroke-linecap="round">')
for y in ROADS_H:
    a(f'<path d="M0 {y-ROAD_W/2-14} H{W}"/>')
for x in ROADS_V:
    a(f'<path d="M{x+ROAD_W/2+14} 0 V{H}"/>')
a('</g>')

# house lots: fill blocks with houses facing the roads
houses = []
def lot_row(y_road, side, x0, x1):
    """Row of houses along a horizontal road. side=-1 above, +1 below."""
    x = x0 + 30
    while x + 110 < x1 - 20:
        w = random.choice([96, 104, 112, 120])
        h = random.choice([74, 82, 90])
        y = y_road - ROAD_W/2 - 40 - h if side < 0 else y_road + ROAD_W/2 + 40
        houses.append((x, y, w, h, side, y_road))
        x += w + random.choice([48, 58, 66])

cols = [0] + ROADS_V + [W]
for i in range(len(cols) - 1):
    x0 = cols[i] + (ROAD_W/2 if i else 0)
    x1 = cols[i+1] - (ROAD_W/2 if i+1 < len(cols)-1 else 0)
    lot_row(ROADS_H[0], -1, x0, x1)
    lot_row(ROADS_H[0], +1, x0, x1)
    lot_row(ROADS_H[1], -1, x0, x1)
    lot_row(ROADS_H[1], +1, x0, x1)

roof_colors = [("#5B7DB5", "#3F5F94"), ("#7A8AA8", "#5B6B8A"), ("#9A6B5E", "#7A5046"),
               ("#5F8494", "#456876")]
trees = []
for idx, (x, y, w, h, side, y_road) in enumerate(houses):
    light, dark = random.choice(roof_colors)
    delay = round(0.25 * idx % 6.5, 2)
    cx, cy = x + w/2, y + h/2
    # service line from the power line to the house
    line_y = y_road - ROAD_W/2 - 14
    a(f'<path class="feed" style="--d:{delay}s" d="M{cx} {line_y} V{y+ (h if side<0 else 0)}" '
      'stroke="#FFC21A" stroke-width="2" fill="none"/>')
    a(f'<circle class="lit" style="--d:{delay}s" cx="{cx}" cy="{cy}" r="{max(w,h)*0.95:.0f}" fill="url(#glow)"/>')
    # garden
    gy = y - 34 if side > 0 else y + h + 8
    a(f'<rect x="{x-8}" y="{min(y, gy)-8 if side>0 else y-8}" width="{w+16}" height="{h+50}" rx="6" fill="#10284A" opacity=".55"/>')
    # roof (gable seen from above: two halves + ridge)
    a(f'<g class="house" style="--d:{delay}s">'
      f'<rect x="{x}" y="{y}" width="{w}" height="{h/2}" fill="{light}"/>'
      f'<rect x="{x}" y="{y+h/2}" width="{w}" height="{h/2}" fill="{dark}"/>'
      f'<line x1="{x}" y1="{y+h/2}" x2="{x+w}" y2="{y+h/2}" stroke="#1B2D4A" stroke-width="2"/>'
      f'<rect x="{x+w*0.68:.0f}" y="{y+8}" width="12" height="12" fill="#22324D"/>'
      f'<rect class="win" x="{x+w*0.18:.0f}" y="{y+h*0.62:.0f}" width="{w*0.26:.0f}" height="{h*0.2:.0f}" rx="2" fill="#FFD166"/>'
      '</g>')
    if random.random() < 0.7:
        tx = x + w + 18
        ty = y + h * (0.3 if side < 0 else 0.7)
        trees.append((tx, ty, random.choice([14, 18, 22])))

for tx, ty, r in trees:
    a(f'<circle cx="{tx:.0f}" cy="{ty:.0f}" r="{r}" fill="#153D3A"/>'
      f'<circle cx="{tx-r*0.3:.0f}" cy="{ty-r*0.3:.0f}" r="{r*0.55:.0f}" fill="#1D524C"/>')

# service van driving along the lower road
vy = ROADS_H[1] + 6
a(f'<g class="van"><rect x="-60" y="{vy}" width="64" height="30" rx="6" fill="#F4F6FA"/>'
  f'<rect x="-60" y="{vy+12}" width="64" height="6" fill="#FFC21A"/>'
  f'<rect x="-6" y="{vy+3}" width="8" height="24" rx="3" fill="#9FB3D1"/></g>')

a('</svg>')
open(__import__('os').path.join(__import__('os').path.dirname(__file__), 'hero.svg'), 'w').write(''.join(out))
print(len(houses), 'houses', sum(len(s) for s in out), 'bytes')

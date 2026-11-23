#!/usr/bin/env python3
"""Draw THE WORLD TODAY — Monday 23 November 2026 front page.

100% programmatic PIL + DejaVu. No network, no downloaded assets.
Stories: 17 (lead + 16 cells) + 3 ticker items, all dated 23 Nov 2026.
Deterministic: same bytes on every run (fixed layout, no timestamps).
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

NAVY = (15, 42, 74)
NAVY_DARK = (10, 30, 54)
GOLD = (232, 163, 23)
CREAM = (247, 243, 232)
INK = (20, 20, 20)
RED = (176, 30, 36)
GREY = (90, 90, 90)
WHITE = (255, 255, 255)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
F_BOLD = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")
F_REG = os.path.join(FONT_DIR, "DejaVuSans.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


def text_w(draw, s, f):
    return draw.textlength(s, font=f)


def wrap(draw, s, f, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    words, lines, cur = s.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if text_w(draw, trial, f) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def fit_lines(draw, s, f, max_w, max_lines):
    """Wrap text; shrink font until it fits max_lines (min size 14)."""
    size = f.size
    while size > 14:
        lines = wrap(draw, s, font(f.path, size), max_w)
        if len(lines) <= max_lines:
            return lines, font(f.path, size)
        size -= 1
    return wrap(draw, s, font(f.path, 14), max_w), font(f.path, 14)


# ---------- tiny drawn icons (PIL primitives, no glyph risk) ----------
def icon(draw, name, x, y, s, color):
    """Draw a small icon with top-left (x, y) and size s."""
    if name == "chip":
        draw.rectangle([x + s * 0.25, y + s * 0.25, x + s * 0.75, y + s * 0.75],
                       outline=color, width=max(2, s // 12))
        draw.rectangle([x + s * 0.4, y + s * 0.4, x + s * 0.6, y + s * 0.6],
                       fill=color)
        for i in range(3):
            off = s * (0.32 + i * 0.18)
            draw.line([x + off, y, x + off, y + s * 0.25], fill=color,
                      width=max(2, s // 14))
            draw.line([x + off, y + s * 0.75, x + off, y + s], fill=color,
                      width=max(2, s // 14))
            draw.line([x, y + off, x + s * 0.25, y + off], fill=color,
                      width=max(2, s // 14))
            draw.line([x + s * 0.75, y + off, x + s, y + off], fill=color,
                      width=max(2, s // 14))
    elif name == "blast":
        cx, cy, r = x + s / 2, y + s / 2, s / 2
        pts = []
        import math
        for i in range(16):
            ang = math.pi * i / 8
            rr = r if i % 2 == 0 else r * 0.45
            pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
        draw.polygon(pts, fill=color)
    elif name == "sun":
        cx, cy = x + s / 2, y + s / 2
        draw.ellipse([cx - s * 0.28, cy - s * 0.28, cx + s * 0.28, cy + s * 0.28],
                     fill=color)
        for i in range(8):
            import math
            ang = math.pi * i / 4
            x1 = cx + s * 0.36 * math.cos(ang)
            y1 = cy + s * 0.36 * math.sin(ang)
            x2 = cx + s * 0.48 * math.cos(ang)
            y2 = cy + s * 0.48 * math.sin(ang)
            draw.line([x1, y1, x2, y2], fill=color, width=max(2, s // 12))
    elif name == "flame":
        draw.polygon([(x + s * 0.5, y + s * 0.05), (x + s * 0.85, y + s * 0.55),
                      (x + s * 0.72, y + s * 0.9), (x + s * 0.28, y + s * 0.9),
                      (x + s * 0.15, y + s * 0.55)], fill=color)
    elif name == "ball":
        cx, cy = x + s / 2, y + s / 2
        draw.ellipse([cx - s * 0.4, cy - s * 0.4, cx + s * 0.4, cy + s * 0.4],
                     outline=color, width=max(2, s // 10))
        draw.arc([cx - s * 0.4, cy - s * 0.4, cx + s * 0.4, cy + s * 0.4],
                 200, 340, fill=color, width=max(2, s // 12))
    elif name == "flag":
        draw.line([x + s * 0.2, y + s * 0.1, x + s * 0.2, y + s * 0.9],
                  fill=color, width=max(2, s // 10))
        draw.polygon([(x + s * 0.2, y + s * 0.12), (x + s * 0.9, y + s * 0.28),
                      (x + s * 0.2, y + s * 0.48)], fill=color)
    elif name == "pause":
        draw.rectangle([x + s * 0.2, y + s * 0.15, x + s * 0.42, y + s * 0.85],
                       fill=color)
        draw.rectangle([x + s * 0.58, y + s * 0.15, x + s * 0.8, y + s * 0.85],
                       fill=color)
    elif name == "shield":
        draw.polygon([(x + s * 0.5, y + s * 0.08), (x + s * 0.88, y + s * 0.25),
                      (x + s * 0.88, y + s * 0.55), (x + s * 0.5, y + s * 0.92),
                      (x + s * 0.12, y + s * 0.55), (x + s * 0.12, y + s * 0.25)],
                     outline=color, width=max(2, s // 10))
        draw.line([x + s * 0.32, y + s * 0.5, x + s * 0.46, y + s * 0.64,
                   x + s * 0.72, y + s * 0.34], fill=color, width=max(2, s // 10))
    elif name == "cross":
        draw.rectangle([x + s * 0.38, y + s * 0.1, x + s * 0.62, y + s * 0.9],
                       fill=color)
        draw.rectangle([x + s * 0.1, y + s * 0.38, x + s * 0.9, y + s * 0.62],
                       fill=color)
    elif name == "building":
        draw.rectangle([x + s * 0.15, y + s * 0.3, x + s * 0.85, y + s * 0.9],
                       outline=color, width=max(2, s // 10))
        for r in range(2):
            for c in range(3):
                draw.rectangle([x + s * (0.26 + c * 0.22), y + s * (0.42 + r * 0.2),
                                x + s * (0.4 + c * 0.22), y + s * (0.56 + r * 0.2)],
                               fill=color)
        draw.polygon([(x + s * 0.1, y + s * 0.3), (x + s * 0.5, y + s * 0.08),
                      (x + s * 0.9, y + s * 0.3)], fill=color)
    elif name == "ship":
        draw.polygon([(x + s * 0.1, y + s * 0.55), (x + s * 0.9, y + s * 0.55),
                      (x + s * 0.75, y + s * 0.85), (x + s * 0.25, y + s * 0.85)],
                     fill=color)
        draw.line([x + s * 0.5, y + s * 0.55, x + s * 0.5, y + s * 0.12],
                  fill=color, width=max(2, s // 10))
        draw.polygon([(x + s * 0.5, y + s * 0.14), (x + s * 0.85, y + s * 0.5),
                      (x + s * 0.5, y + s * 0.5)], fill=color)
    elif name == "coin":
        cx, cy = x + s / 2, y + s / 2
        draw.ellipse([cx - s * 0.4, cy - s * 0.4, cx + s * 0.4, cy + s * 0.4],
                     outline=color, width=max(2, s // 10))
        f = font(F_BOLD, int(s * 0.55))
        draw.text((cx, cy), "€", font=f, fill=color, anchor="mm")
    elif name == "gem":
        draw.polygon([(x + s * 0.5, y + s * 0.08), (x + s * 0.9, y + s * 0.4),
                      (x + s * 0.7, y + s * 0.92), (x + s * 0.3, y + s * 0.92),
                      (x + s * 0.1, y + s * 0.4)], outline=color,
                     width=max(2, s // 10))
        draw.line([x + s * 0.1, y + s * 0.4, x + s * 0.9, y + s * 0.4],
                  fill=color, width=max(2, s // 12))
    elif name == "quake":
        pts = [(x + s * 0.05, y + s * 0.6), (x + s * 0.25, y + s * 0.3),
               (x + s * 0.4, y + s * 0.7), (x + s * 0.6, y + s * 0.2),
               (x + s * 0.75, y + s * 0.65), (x + s * 0.95, y + s * 0.4)]
        draw.line(pts, fill=color, width=max(2, s // 10), joint="curve")
    elif name == "doc":
        draw.rectangle([x + s * 0.2, y + s * 0.1, x + s * 0.8, y + s * 0.9],
                       outline=color, width=max(2, s // 10))
        for i in range(3):
            yy = y + s * (0.32 + i * 0.18)
            draw.line([x + s * 0.32, yy, x + s * 0.68, yy], fill=color,
                      width=max(2, s // 14))
    elif name == "chart":
        draw.line([x + s * 0.15, y + s * 0.85, x + s * 0.15, y + s * 0.15],
                  fill=color, width=max(2, s // 12))
        draw.line([x + s * 0.15, y + s * 0.85, x + s * 0.9, y + s * 0.85],
                  fill=color, width=max(2, s // 12))
        draw.line([(x + s * 0.2, y + s * 0.3), (x + s * 0.45, y + s * 0.5),
                   (x + s * 0.65, y + s * 0.42), (x + s * 0.88, y + s * 0.72)],
                  fill=color, width=max(2, s // 10), joint="curve")
    elif name == "oval":
        draw.ellipse([x + s * 0.08, y + s * 0.28, x + s * 0.92, y + s * 0.72],
                     outline=color, width=max(2, s // 10))
        draw.line([x + s * 0.42, y + s * 0.5, x + s * 0.58, y + s * 0.5],
                  fill=color, width=max(2, s // 12))
        for i in range(3):
            xx = x + s * (0.45 + i * 0.05)
            draw.line([xx, y + s * 0.42, xx, y + s * 0.58], fill=color,
                      width=max(2, s // 16))


# ---------- content ----------
LEAD = {
    "kicker": "LEAD STORY  •  MARKETS  •  WALL STREET",
    "headline": "HUANG IS BACK",
    "subhead": "NVIDIA REINSTATES ITS CEO — SHARES SOAR 31%",
    "body": ("Eleven days after resigning amid scandal, Jensen Huang returns "
             "under pressure from Trump. Nasdaq jumps 6%, S&P 500 up 5%."),
}

CELLS = [
    ("blast", (122, 30, 54), "EUROPE  •  UKRAINE",
     "RUSSIAN STRIKES KILL 14 NEAR KYIV",
     "Dymer block collapses; 153 drones overnight; Zelenskiy warns of new strikes."),
    ("sun", (176, 30, 36), "CLIMATE  •  ANTALYA",
     "COP31 FALLOUT: BLAME GAME BEGINS",
     "Calls for Bowen to quit; Pacific nations despair; first COP failure since 2009."),
    ("flame", (140, 30, 40), "ASIA  •  INDONESIA",
     "24 DEAD IN CIKANDE FACTORY FIRE",
     "Toll confirmed Monday; about 30 still missing; short circuit suspected."),
    ("ball", (30, 110, 60), "SPORT  •  CRICKET",
     "WELLINGTON TEST ENDS IN DRAW",
     "NZ 239/5 hold India (720/9 dec); Mitchell 49* off 186 balls."),
    ("flag", (15, 42, 74), "EUROPE  •  SPAIN",
     "PUIGDEMONT FREE TO RETURN",
     "Court shelves case; last hurdle gone after a decade in exile."),
    ("pause", (90, 60, 110), "USA  •  IOWA",
     "TRUMP PAUSES LEAD BLAST",
     "Army told to halt detonation of 68 barrels of toxic lead azide in Iowa."),
    ("shield", (110, 60, 20), "MIDDLE EAST  •  SYRIA",
     "US TO TRAIN SYRIAN TROOPS",
     "First US training mission since rebels took Damascus in 2024."),
    ("cross", (140, 30, 40), "MIDDLE EAST  •  GAZA",
     "STRIKES KILL 3 IN GAZA",
     "UNRWA worker Adel Al-Helo killed in Jabalia; vehicle hit in Gaza City."),
    ("building", (90, 40, 90), "ASIA  •  KOREA",
     "N. KOREA MAY SHUT SWISS OFFICE",
     "Pyongyang weighs closing mission over sanctions on a children's camp."),
    ("ship", (20, 80, 110), "EUROPE  •  RUSSIA",
     "$576M FERRIES FOR KALININGRAD",
     "Two giant rail ferries to secure supplies to the Baltic exclave."),
    ("coin", (150, 110, 20), "EUROPE  •  EU BUDGET",
     "EU BUDGET REJECTED",
     "Czechs and Hungarians spurn €1.582tn plan; summit set for Nov 26–27."),
    ("gem", (20, 90, 60), "AFRICA  •  CONGO",
     "CONGO HALTS COBALT EXPORTS",
     "Top producer suspends shipments from Nov 30 to lift prices."),
    ("quake", (30, 80, 120), "PACIFIC  •  VANUATU",
     "M6.5 QUAKE HITS VANUATU",
     "Deep tremor, 600 km down; no damage or casualties reported."),
    ("doc", (60, 60, 120), "EUROPE  •  SANCTIONS",
     "EU UNVEILS 22ND SANCTIONS",
     "New package targets Russia's shadow fleet, energy and visas."),
    ("chart", (120, 40, 50), "WAR  •  RUSSIA",
     "490,000 RUSSIAN DEAD: LEAK",
     "Stolen Rosstat data points to at least 490,000 military deaths."),
    ("oval", (110, 40, 90), "SPORT  •  NFL",
     "49ERS BEAT VIKINGS 35–10",
     "Mexico City rout tightens grip on the NFC's No. 1 seed."),
]

TICKER = ("ALSO TODAY:   Cyclone Xavier churns at 241 km/h   •   "
          "US flights resume after Friday's FAA ground stop   •   "
          "China sentences official to death for leaking secrets")


def draw_page():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)

    # ---- masthead ----
    d.rectangle([0, 0, W, 96], fill=NAVY)
    d.rectangle([0, 96, W, 100], fill=GOLD)
    f_ed = font(F_BOLD, 20)
    d.text((16, 14), "MONDAY EDITION", font=f_ed, fill=GOLD)
    f_title = font(F_BOLD, 50)
    d.text((W // 2, 6), "THE WORLD TODAY", font=f_title, fill=GOLD,
           anchor="ma")
    f_date = font(F_BOLD, 29)
    d.text((W // 2, 62), "MONDAY 23 NOVEMBER 2026", font=f_date, fill=WHITE,
           anchor="ma")

    # ---- lead ----
    ly0, ly1 = 108, 268
    d.rectangle([8, ly0, 8 + 232, ly1], fill=NAVY_DARK)
    icon(d, "chip", 8 + 66, ly0 + 12, 100, GOLD)
    f_cap = font(F_BOLD, 15)
    d.text((8 + 116, ly1 - 22), "WALL STREET  •  NVIDIA", font=f_cap,
           fill=GOLD, anchor="ma")
    tx = 8 + 232 + 18
    tw = W - 8 - tx
    f_kick = font(F_BOLD, 18)
    d.text((tx, ly0 + 8), LEAD["kicker"], font=f_kick, fill=RED)
    f_head = font(F_BOLD, 54)
    d.text((tx, ly0 + 32), LEAD["headline"], font=f_head, fill=INK)
    f_sub = font(F_BOLD, 23)
    d.text((tx, ly0 + 94), LEAD["subhead"], font=f_sub, fill=RED)
    f_body = font(F_REG, 19)
    for i, line in enumerate(wrap(d, LEAD["body"], f_body, tw)):
        d.text((tx, ly0 + 118 + i * 22), line, font=f_body, fill=INK)

    # ---- 4x4 grid ----
    gx, gy = 8, 276
    cw, ch, gap = 246, 164, 8
    for idx, (ic, col, kick, head, body) in enumerate(CELLS):
        r, c = divmod(idx, 4)
        x0 = gx + c * (cw + gap)
        y0 = gy + r * (ch + gap)
        d.rectangle([x0, y0, x0 + cw, y0 + ch], fill=WHITE,
                    outline=(200, 195, 180), width=1)
        d.rectangle([x0, y0, x0 + cw, y0 + 26], fill=col)
        icon(d, ic, x0 + 6, y0 + 4, 18, WHITE)
        f_k = font(F_BOLD, 14)
        d.text((x0 + 28, y0 + 5), kick, font=f_k, fill=WHITE)
        f_h = font(F_BOLD, 23)
        lines, f_h = fit_lines(d, head, f_h, cw - 16, 2)
        yy = y0 + 32
        for line in lines:
            d.text((x0 + 8, yy), line, font=f_h, fill=INK)
            yy += f_h.size + 2
        f_b = font(F_REG, 15)
        for i, line in enumerate(wrap(d, body, f_b, cw - 16)[:3]):
            d.text((x0 + 8, yy + 4 + i * 19), line, font=f_b, fill=(40, 40, 40))

    # ---- ticker ----
    d.rectangle([0, 964, W, H], fill=NAVY)
    f_t = font(F_BOLD, 19)
    lines = wrap(d, TICKER, f_t, W - 32)
    yy = 970
    for line in lines:
        d.text((16, yy), line, font=f_t, fill=WHITE)
        yy += 23

    img.save(OUT, "PNG")
    return OUT


if __name__ == "__main__":
    path = draw_page()
    import hashlib
    data = open(path, "rb").read()
    print(path, len(data), "bytes")
    print("sha256", hashlib.sha256(data).hexdigest())
    print("size", Image.open(path).size)

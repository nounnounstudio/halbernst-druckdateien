"""Retro-Stil: Sonnenuntergang-Badge, 70er Farben, Cel-Shading, Halo-Kontur, Used-Textur."""
import math, os, random, subprocess, sys

CREAM, MUST, ORANGE, RUST, OLIVE, TEAL, INK = "#F3E6CC", "#EBA937", "#E0702F", "#B9432B", "#6B7A3E", "#2E5E5B", "#2A1D17"
DARK = {CREAM: "#D9C7A3", MUST: "#C98A22", ORANGE: "#B9541F", RUST: "#8E2F1E", OLIVE: "#4E5A2C", TEAL: "#1F4442", "#8A5634": "#5E3A22", "#9FC3CF": "#6E98A6"}
COFFEE, SKY = "#8A5634", "#9FC3CF"
SW = 20
_id = [0]

def uid(p="c"):
    _id[0] += 1
    return f"{p}{_id[0]}"

class Art:
    def __init__(self):
        self.bg, self.halo, self.fg = [], [], []

    def shape(self, d, fill, shade=True, sw=SW, halo=True, dx=-26, dy=-30):
        if halo:
            self.halo.append(f'<path d="{d}" fill="{CREAM}" stroke="{CREAM}" stroke-width="{sw+46}" stroke-linejoin="round" stroke-linecap="round"/>')
        if fill == "none":
            self.fg.append(f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="{sw}" stroke-linejoin="round" stroke-linecap="round"/>')
            return
        if shade and fill in DARK:
            c = uid()
            self.fg.append(f'<clipPath id="{c}"><path d="{d}"/></clipPath><path d="{d}" fill="{DARK[fill]}"/>'
                           f'<path d="{d}" fill="{fill}" transform="translate({dx} {dy})" clip-path="url(#{c})"/>')
        else:
            self.fg.append(f'<path d="{d}" fill="{fill}"/>')
        if sw:
            self.fg.append(f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="{sw}" stroke-linejoin="round" stroke-linecap="round"/>')

    def stroke(self, d, col=INK, w=SW, halo=True):
        if halo:
            self.halo.append(f'<path d="{d}" fill="none" stroke="{CREAM}" stroke-width="{w+46}" stroke-linecap="round" stroke-linejoin="round"/>')
        self.fg.append(f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>')

    def thick(self, d, col, w):
        """dicke Linie (Arm, Schwanz, Ast) mit Kontur"""
        self.halo.append(f'<path d="{d}" fill="none" stroke="{CREAM}" stroke-width="{w+SW*2+46}" stroke-linecap="round"/>')
        self.fg.append(f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="{w+SW*2}" stroke-linecap="round"/>'
                       f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{w}" stroke-linecap="round"/>')

    def raw(self, s):
        self.fg.append(s)

    def svg(self, seed=1):
        return f'<g>{"".join(self.bg)}{"".join(self.halo)}{"".join(self.fg)}</g>'

def circle_d(cx, cy, r):
    return f"M{cx-r} {cy} A{r} {r} 0 1 0 {cx+r} {cy} A{r} {r} 0 1 0 {cx-r} {cy} Z"

def ell_d(cx, cy, rx, ry):
    return f"M{cx-rx} {cy} A{rx} {ry} 0 1 0 {cx+rx} {cy} A{rx} {ry} 0 1 0 {cx-rx} {cy} Z"

def rect_d(x, y, w, h, r=0):
    r = min(r, w / 2, h / 2)
    return (f"M{x+r} {y} L{x+w-r} {y} Q{x+w} {y} {x+w} {y+r} L{x+w} {y+h-r} Q{x+w} {y+h} {x+w-r} {y+h} "
            f"L{x+r} {y+h} Q{x} {y+h} {x} {y+h-r} L{x} {y+r} Q{x} {y} {x+r} {y} Z")

def sunset(a, cx=500, cy=440, r=380, cols=(MUST, ORANGE, RUST), horizon=0.15, ring=True):
    c = uid()
    out = f'<clipPath id="{c}"><circle cx="{cx}" cy="{cy}" r="{r}"/></clipPath><g clip-path="url(#{c})">'
    top = cy - r
    n = len(cols)
    hy = cy + r * horizon
    bh = (hy - top) / n
    for i, col in enumerate(cols):
        out += f'<rect x="{cx-r}" y="{top+i*bh:.0f}" width="{2*r}" height="{bh+1:.0f}" fill="{col}"/>'
    y, gap, k = hy, 14, 0
    while y < cy + r:
        h = 46 - k * 5
        out += f'<rect x="{cx-r}" y="{y+gap:.0f}" width="{2*r}" height="{max(h,10):.0f}" fill="{cols[-1]}"/>'
        y += gap + max(h, 10)
        gap += 6
        k += 1
    out += '</g>'
    if ring:
        out += f'<circle cx="{cx}" cy="{cy}" r="{r+34}" fill="none" stroke="{cols[-1]}" stroke-width="16"/>'
    a.bg.append(out)

def night(a, cx=500, cy=440, r=380):
    sunset(a, cx, cy, r, cols=(TEAL, "#3F7470", "#2E5E5B"), horizon=0.25)


def bands(a, clip, top, bottom, cols, horizon=0.55, x0=0, x1=1000, ring=None):
    c = uid()
    out = f'<clipPath id="{c}"><path d="{clip}"/></clipPath><g clip-path="url(#{c})">'
    hy = top + (bottom - top) * horizon
    n = len(cols); bh = (hy - top) / n
    for i, col in enumerate(cols):
        out += f'<rect x="{x0}" y="{top+i*bh:.0f}" width="{x1-x0}" height="{bh+1:.0f}" fill="{col}"/>'
    y, gap, k = hy, 14, 0
    while y < bottom:
        h = max(46 - k * 5, 10)
        out += f'<rect x="{x0}" y="{y+gap:.0f}" width="{x1-x0}" height="{h:.0f}" fill="{cols[-1]}"/>'
        y += gap + h; gap += 6; k += 1
    out += '</g>'
    if ring:
        out += f'<path d="{ring}" fill="none" stroke="{cols[-1]}" stroke-width="16" stroke-linejoin="round"/>'
    a.bg.append(out)

def arch_d(x, y, w, h):
    r = w / 2
    return f"M{x} {y+h} L{x} {y+r} A{r} {r} 0 0 1 {x+w} {y+r} L{x+w} {y+h} Z"

def arch(a, x, y, w, h, cols=(MUST, ORANGE, RUST)):
    bands(a, arch_d(x, y, w, h), y, y + h, cols, 0.5, x, x + w, ring=arch_d(x - 30, y - 30, w + 60, h + 30))

def window(a, x, y, w, h, r, cols, horizon=0.6):
    bands(a, rect_d(x, y, w, h, r), y, y + h, cols, horizon, x, x + w, ring=rect_d(x - 30, y - 30, w + 60, h + 60, r + 30))

def diamond(a, cx, cy, r, cols=(MUST, ORANGE, RUST)):
    d = f"M{cx} {cy-r} L{cx+r} {cy} L{cx} {cy+r} L{cx-r} {cy} Z"
    R = r + 40
    bands(a, d, cy - r, cy + r, cols, 0.55, cx - r, cx + r, ring=f"M{cx} {cy-R} L{cx+R} {cy} L{cx} {cy+R} L{cx-R} {cy} Z")

def rays(a, cx, cy, r, c1, c2, n=18, star=True):
    pts = []
    for k in range(n * 2):
        ang = k * math.pi / n
        rr = r if k % 2 == 0 else r * 0.86
        pts.append(f"{cx+rr*math.cos(ang):.0f},{cy+rr*math.sin(ang):.0f}")
    out = f'<polygon points="{" ".join(pts)}" fill="{c1}"/>' if star else f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{c1}"/>'
    for k in range(n):
        a0, a1 = (2 * k) * math.pi / n, (2 * k + 1) * math.pi / n
        rr = r * 0.8
        out += f'<path d="M{cx} {cy} L{cx+rr*math.cos(a0):.0f} {cy+rr*math.sin(a0):.0f} L{cx+rr*math.cos(a1):.0f} {cy+rr*math.sin(a1):.0f} Z" fill="{c2}"/>'
    a.bg.append(out)

def blob(a, cx, cy, r, col, seed=1, k=9):
    rnd = random.Random(seed)
    pts = [(cx + r * (0.82 + rnd.uniform(0, 0.3)) * math.cos(i * 2 * math.pi / k), cy + r * (0.82 + rnd.uniform(0, 0.3)) * math.sin(i * 2 * math.pi / k)) for i in range(k)]
    d = f"M{(pts[0][0]+pts[-1][0])/2:.0f} {(pts[0][1]+pts[-1][1])/2:.0f} "
    for i in range(k):
        p, q = pts[i], pts[(i + 1) % k]
        d += f"Q{p[0]:.0f} {p[1]:.0f} {(p[0]+q[0])/2:.0f} {(p[1]+q[1])/2:.0f} "
    a.bg.append(f'<path d="{d}Z" fill="{col}"/>')

def hills(a, y, cols=(OLIVE, "#4E5A2C"), sun=(MUST, 760, None)):
    if sun:
        a.bg.append(f'<circle cx="{sun[1]}" cy="{sun[2] or y-60}" r="130" fill="{sun[0]}"/>')
    a.bg.append(f'<path d="M60 {y+40} Q250 {y-120} 470 {y+20} Q640 {y-90} 940 {y+30} L940 {y+160} L60 {y+160} Z" fill="{cols[0]}"/>')
    a.bg.append(f'<path d="M40 {y+120} Q300 {y+10} 560 {y+110} Q760 {y+40} 960 {y+110} L960 {y+200} L40 {y+200} Z" fill="{cols[1]}"/>')

def dots_bg(a, pts, col=CREAM):
    for x, y, r in pts:
        a.bg.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{col}"/>')

def sparkle_bg(a, x, y, r, col=CREAM):
    a.bg.append(f'<polygon points="{x},{y-r} {x+r*0.3},{y-r*0.3} {x+r},{y} {x+r*0.3},{y+r*0.3} {x},{y+r} {x-r*0.3},{y+r*0.3} {x-r},{y} {x-r*0.3},{y-r*0.3}" fill="{col}"/>')

def distress(seed):
    rnd = random.Random(seed)
    s = '<rect x="-200" y="-200" width="1400" height="1400" fill="white"/>'
    for _ in range(420):
        x, y = rnd.uniform(-50, 1050), rnd.uniform(-50, 1050)
        rr = rnd.choice((2.5, 3, 4, 5, 6, 8))
        pts = []
        for k in range(6):
            ang = k * math.pi / 3 + rnd.uniform(-0.4, 0.4)
            q = rr * rnd.uniform(0.5, 1.3)
            pts.append(f"{x+q*math.cos(ang):.1f},{y+q*math.sin(ang):.1f}")
        s += f'<polygon points="{" ".join(pts)}" fill="black"/>'
    for _ in range(14):
        x, y = rnd.uniform(0, 1000), rnd.uniform(0, 1000)
        ang = rnd.uniform(-0.5, 0.5)
        L = rnd.uniform(30, 110)
        s += f'<line x1="{x:.0f}" y1="{y:.0f}" x2="{x+L*math.cos(ang):.0f}" y2="{y+L*math.sin(ang):.0f}" stroke="black" stroke-width="{rnd.uniform(2,4):.1f}" stroke-linecap="round"/>'
    return s

def dot(a, x, y, r, col=INK):
    a.raw(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{col}"/>')

def hl(a, d, w=12):
    """Glanzlicht"""
    a.raw(f'<path d="{d}" fill="none" stroke="{CREAM}" stroke-width="{w}" stroke-linecap="round" opacity="1"/>')

# ------------------------------------------------------------------ Motive
BROWN, BROWN_D, GREY, GREY_D, CHAR = "#A67B5B", "#7D5A40", "#9A9A9A", "#6E6E6E", "#3A3A3A"
DARK.update({BROWN: BROWN_D, GREY: GREY_D, CHAR: "#1E1E1E", "#7A4E2D": "#55341D"})

def cloud_bg(a, x, y, s=1.0, col=CREAM):
    a.bg.append(f'<path transform="translate({x} {y}) scale({s})" d="M-90 20 Q-95 -20 -55 -25 Q-45 -65 0 -60 Q40 -80 65 -40 Q100 -40 100 0 Q105 25 80 25 Z" fill="{col}"/>')

def puff(a, x, y, r, sw=14):
    a.shape(circle_d(x, y, r), CREAM, sw=sw)
    a.stroke(f"M{x-r*0.45:.0f} {y+r*0.1:.0f} Q{x-r*0.1:.0f} {y-r*0.35:.0f} {x+r*0.35:.0f} {y-r*0.1:.0f}", CREAM_D, 8, halo=False)

CREAM_D = "#CDB88F"

def bolt(cx, cy, s):
    return f"M{cx-0.15*s} {cy-0.5*s} L{cx+0.25*s} {cy-0.5*s} L{cx+0.05*s} {cy-0.08*s} L{cx+0.3*s} {cy-0.08*s} L{cx-0.2*s} {cy+0.5*s} L{cx-0.05*s} {cy+0.05*s} L{cx-0.3*s} {cy+0.05*s} Z"

# ------------------------------------------------------------------ Katze
def katze_tasse():
    a = Art(); sunset(a)
    cloud_bg(a, 720, 230, 0.9); cloud_bg(a, 250, 180, 0.6)
    # Pfütze und fallende Tasse unten
    a.shape(ell_d(790, 935, 120, 26), COFFEE, shade=False, sw=12)
    # Tisch
    a.thick("M150 760 L150 935", RUST, 36); a.thick("M670 760 L670 935", RUST, 36)
    a.shape(rect_d(120, 760, 580, 50, 6), "#8E2F1E", shade=False, sw=SW)
    a.shape(rect_d(80, 700, 660, 66, 12), RUST)
    for d in ("M120 722 Q260 712 380 726 T640 720", "M160 746 Q300 738 450 748"):
        a.stroke(d, "#8E2F1E", 7, halo=False)
    # Schwanz
    a.thick("M250 690 C160 690 130 770 150 860 C160 910 225 910 220 865", ORANGE, 50)
    for x, y, r in ((160, 760, 20), (150, 820, 0), (175, 885, -40)):
        a.raw(f'<path d="M{x-24} {y} L{x+24} {y}" transform="rotate({r} {x} {y})" stroke="{RUST}" stroke-width="12" stroke-linecap="round"/>')
    # Körper
    a.shape("M235 700 C195 600 225 470 340 455 C450 445 505 540 505 620 C505 670 485 700 465 700 Z", ORANGE)
    a.shape(ell_d(370, 610, 70, 85), CREAM, sw=0, halo=False)
    for d in ("M270 520 Q300 545 290 590", "M255 600 Q285 615 280 660", "M455 525 Q430 548 440 590"):
        a.stroke(d, RUST, 15, halo=False)
    a.shape(ell_d(300, 700, 55, 26), ORANGE, sw=16, halo=False)
    a.stroke("M285 690 L285 712 M310 690 L310 712", INK, 7, halo=False)
    # Arm + Pfote
    a.thick("M445 555 Q545 555 588 610", ORANGE, 54)
    a.stroke("M462 560 L470 595 M500 556 L505 592", RUST, 10, halo=False)
    a.shape(circle_d(598, 618, 36), ORANGE, sw=16, halo=False)
    a.stroke("M612 600 L622 616 M600 628 L612 640", INK, 7, halo=False)
    # Ohren
    a.shape("M262 370 L240 222 L350 296 Z", ORANGE); a.shape("M498 370 L524 222 L414 296 Z", ORANGE)
    a.shape("M268 300 L258 250 L310 286 Z", "#E8A0A0", shade=False, sw=0, halo=False)
    a.shape("M492 300 L506 250 L452 286 Z", "#E8A0A0", shade=False, sw=0, halo=False)
    # Kopf mit Fellbüscheln
    head = ("M245 390 C245 300 310 272 380 272 C450 272 515 300 515 390 L545 408 L514 418 L534 446 L500 448 "
            "C480 495 430 512 380 512 C330 512 280 495 260 448 L226 446 L246 418 L215 408 Z")
    a.shape(head, ORANGE)
    a.shape(ell_d(380, 470, 62, 36), CREAM, sw=0, halo=False)
    a.stroke("M345 292 L352 330 M380 286 L380 326 M415 292 L408 330", RUST, 14, halo=False)
    for x in (330, 430):
        a.raw(f'<ellipse cx="{x}" cy="398" rx="35" ry="27" fill="#E9D46A" stroke="{INK}" stroke-width="12"/>')
        a.raw(f'<ellipse cx="{x+6}" cy="405" rx="9" ry="17" fill="{INK}"/><circle cx="{x+12}" cy="398" r="4" fill="{CREAM}"/>')
        a.raw(f'<path d="M{x-42} 394 Q{x} 362 {x+42} 394 L{x+42} 378 Q{x} 348 {x-42} 378 Z" fill="{ORANGE}" stroke="{INK}" stroke-width="12" stroke-linejoin="round"/>')
    a.stroke("M290 352 L362 362 M470 352 L398 362", INK, 10, halo=False)
    a.raw(f'<path d="M366 446 L394 446 L380 462 Z" fill="#E07A7A" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>')
    a.stroke("M380 462 Q372 482 352 476 M380 462 Q390 482 410 474", INK, 9, halo=False)
    a.stroke("M250 450 L180 440 M252 466 L184 482 M510 450 L580 440 M508 466 L576 482", INK, 7, halo=False)
    # Tasse
    a.raw('<g transform="rotate(32 660 690)">')
    a.shape(rect_d(595, 600, 130, 155, 18), TEAL)
    a.stroke("M725 635 Q782 635 782 677 Q782 718 725 718", INK, 22)
    a.raw(f'<rect x="595" y="650" width="130" height="26" fill="{CREAM}"/>')
    a.stroke("M595 650 L725 650 M595 676 L725 676", INK, 8, halo=False)
    a.raw('</g>')
    for d in ("M780 575 Q815 600 812 640", "M820 545 Q860 585 855 640"):
        a.stroke(d, CREAM, 10, halo=False)
    for x, y, r in ((770, 520, 20), (812, 470, 13), (735, 480, 11), (850, 520, 10)):
        a.shape(circle_d(x, y, r), COFFEE, shade=False, sw=9)
    a.stroke("M705 560 Q735 495 775 505", COFFEE, 20)
    return a

# ------------------------------------------------------------------ Schnecke
def rennschnecke():
    a = Art()
    a.bg.append(f'<circle cx="640" cy="420" r="210" fill="{MUST}"/>')
    hills(a, 700, cols=(OLIVE, "#4E5A2C"), sun=None)
    a.bg.append(f'<rect x="40" y="880" width="920" height="70" rx="20" fill="#4A4A4A"/>')
    for x in range(90, 940, 130):
        a.bg.append(f'<rect x="{x}" y="908" width="70" height="14" fill="{CREAM}"/>')
    cloud_bg(a, 240, 300, 0.9); cloud_bg(a, 860, 260, 0.6)
    for y, x0, x1 in ((470, 70, 240), (540, 30, 210), (610, 70, 230)):
        a.stroke(f"M{x0} {y} L{x1} {y}", CREAM, 22)
    for x, y, r in ((240, 820, 55), (170, 850, 40), (300, 860, 36), (110, 870, 26)):
        puff(a, x, y, r)
    # Körper
    a.shape("M265 850 C300 812 700 812 760 802 L790 650 C800 566 905 566 910 650 L895 815 C905 862 865 885 825 885 L305 885 C262 885 245 872 265 850 Z", MUST)
    for x, y in ((420, 860), (520, 855), (640, 858), (845, 700), (860, 780)):
        dot(a, x, y, 9, "#C98A22")
    # Fühler + Zielflagge
    a.stroke("M832 605 L800 470", INK, 14); a.stroke("M882 605 L915 470", INK, 14)
    dot(a, 798, 462, 20); dot(a, 918, 462, 20)
    a.stroke("M918 462 L918 300", INK, 10)
    flag = ""
    for r in range(3):
        for c in range(4):
            col = INK if (r + c) % 2 == 0 else CREAM
            flag += f'<rect x="{918+c*28}" y="{300+r*28}" width="28" height="28" fill="{col}"/>'
    a.raw(f'<g transform="skewY(6)" transform-origin="918 300">{flag}<rect x="918" y="300" width="112" height="84" fill="none" stroke="{INK}" stroke-width="10"/></g>')
    # Rennbrille
    a.stroke("M790 672 L912 672", "#5E3A22", 16, halo=False)
    a.shape(rect_d(812, 640, 54, 58, 22), SKY, sw=12, halo=False); a.shape(rect_d(866, 640, 46, 58, 20), SKY, sw=12, halo=False)
    a.stroke("M824 656 L834 650", CREAM, 7, halo=False)
    a.stroke("M832 748 Q857 768 882 748", INK, 10, halo=False)
    # Auspuff
    a.shape(rect_d(250, 700, 70, 40, 12), GREY, sw=12)
    a.shape("M250 705 L190 690 L215 718 L160 735 L250 735 Z", ORANGE, shade=False, sw=10)
    # Haus
    a.shape(circle_d(525, 600, 255), ORANGE)
    a.stroke("M525 610 m-34 0 a34 34 0 1 1 68 0 a100 100 0 1 1 -200 0 a165 165 0 1 1 330 0", INK, 20, halo=False)
    for k in range(10):
        ang = math.radians(200 + k * 14)
        x1, y1 = 525 + 205 * math.cos(ang), 600 + 205 * math.sin(ang)
        x2, y2 = 525 + 240 * math.cos(ang), 600 + 240 * math.sin(ang)
        a.stroke(f"M{x1:.0f} {y1:.0f} L{x2:.0f} {y2:.0f}", RUST, 8, halo=False)
    a.shape(circle_d(560, 640, 62), CREAM, shade=False, sw=12, halo=False)
    a.shape(bolt(560, 640, 90), RUST, shade=False, sw=8, halo=False)
    hl(a, "M370 470 Q410 410 480 392", 16)
    return a

# ------------------------------------------------------------------ Faultier
def faultier():
    a = Art(); arch(a, 170, 120, 660, 760, cols=(MUST, ORANGE, "#C9583A", OLIVE))
    cloud_bg(a, 740, 360, 0.8); cloud_bg(a, 260, 420, 0.6)
    a.thick("M50 210 Q500 160 950 220", "#7A4E2D", 46)
    for d in ("M120 205 L200 200", "M640 190 L720 196", "M820 208 L880 212"):
        a.stroke(d, "#55341D", 7, halo=False)
    for x, y, r in ((150, 182, -20), (230, 170, 15), (720, 178, -10), (800, 186, 20), (880, 196, -15)):
        a.raw(f'<g transform="rotate({r} {x} {y})">')
        a.shape(f"M{x} {y} q35 -75 90 -62 q-20 55 -90 62 Z", OLIVE, sw=12)
        a.stroke(f"M{x+8} {y-6} Q{x+40} {y-40} {x+78} {y-55}", "#4E5A2C", 6, halo=False)
        a.raw('</g>')
    # Liane rechts
    a.stroke("M860 215 Q840 330 870 430 Q890 500 860 560", OLIVE, 12)
    for y in (330, 430, 520):
        a.shape(f"M{866 if y!=430 else 876} {y} q40 -10 50 30 q-40 10 -50 -30 Z", OLIVE, sw=10)
    # Vogel auf Ast
    a.shape("M640 150 C640 110 700 100 715 135 L745 130 L720 150 C715 175 650 180 640 150 Z", MUST, sw=14)
    dot(a, 703, 128, 7)
    a.stroke("M660 175 L655 195 M685 176 L688 195", INK, 7, halo=False)
    # Arme mit Krallen
    a.thick("M425 205 C400 285 410 335 440 385", BROWN, 62)
    a.thick("M575 205 C600 285 590 335 560 385", BROWN, 62)
    for x in (425, 575):
        for k in (-22, 0, 22):
            a.stroke(f"M{x+k} 215 Q{x+k+6} 175 {x+k-10} 160", CREAM, 9, halo=False)
    # Körper + Beine
    a.thick("M430 690 Q420 760 440 790", BROWN, 54); a.thick("M570 690 Q580 760 560 790", BROWN, 54)
    a.shape(ell_d(500, 530, 175, 215), BROWN)
    a.shape(ell_d(500, 600, 95, 120), "#C9A383", sw=0, halo=False)
    for x, y, r in ((380, 580, 20), (395, 650, 30), (620, 580, -20), (605, 650, -30), (450, 700, 10), (550, 700, -10)):
        a.raw(f'<path d="M{x} {y} q8 22 0 40" transform="rotate({r} {x} {y})" fill="none" stroke="{BROWN_D}" stroke-width="8" stroke-linecap="round"/>')
    # Gesicht
    a.shape(ell_d(500, 465, 115, 84), CREAM, sw=14, halo=False)
    for x in (452, 548):
        a.raw(f'<ellipse cx="{x}" cy="460" rx="44" ry="25" fill="#5E3A22" transform="rotate({-15 if x<500 else 15} {x} 460)"/>')
        a.raw(f'<path d="M{x-17} 461 Q{x} 474 {x+17} 461" fill="none" stroke="{CREAM}" stroke-width="7" stroke-linecap="round"/>')
    a.raw(f'<ellipse cx="500" cy="496" rx="20" ry="13" fill="{INK}"/>')
    a.stroke("M476 520 Q500 536 524 520", INK, 9, halo=False)
    # Ladebalken mit Spinner
    a.shape(rect_d(300, 830, 400, 84, 42), CREAM, shade=False)
    a.shape(rect_d(320, 849, 46, 46, 23), RUST, shade=False, sw=0, halo=False)
    for k in range(3):
        dot(a, 730 + k * 34, 872, 11, INK)
    return a

# ------------------------------------------------------------------ Grill
def grill_regen():
    a = Art(); window(a, 140, 90, 720, 760, 90, ("#1F4442", TEAL, "#3F7470"), 0.62)
    a.bg.append(f'<circle cx="250" cy="230" r="46" fill="{CREAM}"/><circle cx="272" cy="214" r="42" fill="{TEAL}"/>')
    rnd = random.Random(4)
    for _ in range(34):
        x, y = rnd.uniform(150, 850), rnd.uniform(100, 780)
        if 200 < x < 800 and y < 430: continue
        a.bg.append(f'<line x1="{x:.0f}" y1="{y:.0f}" x2="{x-14:.0f}" y2="{y+46:.0f}" stroke="{SKY}" stroke-width="10" stroke-linecap="round"/>')
    # Pfützen
    a.shape(ell_d(250, 945, 110, 22), SKY, shade=False, sw=10)
    a.shape(ell_d(760, 950, 90, 18), SKY, shade=False, sw=10)
    # Rauch
    a.stroke("M640 470 Q610 430 650 400 Q690 370 660 330", CREAM, 14)
    a.stroke("M700 480 Q680 450 705 420", CREAM, 12)
    # Schirm
    a.stroke("M500 230 L500 560", INK, 18)
    a.shape("M180 420 Q500 30 820 420 Q767 378 713 420 Q660 378 607 420 Q553 378 500 420 Q447 378 393 420 Q340 378 287 420 Q233 378 180 420 Z", RUST)
    for d in ("M287 420 Q340 280 500 226", "M393 420 Q430 290 500 226", "M607 420 Q570 290 500 226", "M713 420 Q660 280 500 226"):
        a.stroke(d, "#8E2F1E", 9, halo=False)
    hl(a, "M290 360 Q360 270 440 240", 14)
    a.shape(circle_d(500, 214, 16), INK, shade=False, sw=0)
    # Flammen + Würstchen
    for x in (390, 470, 550, 620):
        a.shape(f"M{x-22} 590 Q{x-20} 545 {x} 520 Q{x+20} 545 {x+22} 590 Z", ORANGE, shade=False, sw=10, halo=False)
        a.shape(f"M{x-10} 590 Q{x-8} 565 {x} 552 Q{x+8} 565 {x+10} 590 Z", MUST, shade=False, sw=0, halo=False)
    for x in (350, 505):
        a.shape(rect_d(x, 500, 145, 54, 27), COFFEE, sw=14)
        for k in range(3):
            a.stroke(f"M{x+35+k*35} 508 L{x+20+k*35} 546", "#5E3A22", 8, halo=False)
    # Rost + Grill
    a.stroke("M265 585 L735 585", INK, 22)
    a.shape("M285 600 L715 600 C715 728 625 798 500 798 C375 798 285 728 285 600 Z", CHAR)
    hl(a, "M335 635 Q345 705 410 748", 14)
    for x in (430, 500, 570):
        a.raw(f'<circle cx="{x}" cy="730" r="12" fill="#1E1E1E"/>')
    a.stroke("M715 640 L770 640", INK, 18)
    a.thick("M385 778 L320 925", CHAR, 22); a.thick("M615 778 L680 925", CHAR, 22); a.thick("M500 798 L500 925", CHAR, 22)
    a.shape(ell_d(500, 860, 130, 20), GREY, sw=12, halo=False)
    for x in (320, 680):
        a.shape(circle_d(x, 930, 34), CHAR, sw=14); dot(a, x, 930, 10, GREY)
    return a

# ------------------------------------------------------------------ Rakete
def rakete():
    a = Art(); rays(a, 500, 470, 440, MUST, ORANGE, n=20)
    a.bg.append(f'<circle cx="780" cy="200" r="62" fill="{OLIVE}"/><ellipse cx="780" cy="200" rx="110" ry="24" fill="none" stroke="{CREAM}" stroke-width="12" transform="rotate(-18 780 200)"/>')
    for x, y, r in ((200, 200, 26), (860, 340, 16), (150, 360, 18), (300, 110, 14), (690, 330, 12)):
        a.bg.append(f'<polygon points="{x},{y-r} {x+r*0.3},{y-r*0.3} {x+r},{y} {x+r*0.3},{y+r*0.3} {x},{y+r} {x-r*0.3},{y+r*0.3} {x-r},{y} {x-r*0.3},{y-r*0.3}" fill="{CREAM}"/>')
    for x, y, r in ((290, 885, 55), (710, 885, 55), (380, 870, 75), (620, 870, 75), (500, 890, 85)):
        puff(a, x, y, r)
    a.shape("M430 690 Q440 800 500 860 Q560 800 570 690 Z", RUST, sw=14)
    a.shape("M455 690 Q465 780 500 820 Q535 780 545 690 Z", ORANGE, shade=False, sw=0, halo=False)
    a.shape("M478 690 Q485 745 500 770 Q515 745 522 690 Z", MUST, shade=False, sw=0, halo=False)
    # Stützräder
    a.thick("M345 630 L250 775", GREY, 20); a.thick("M655 630 L750 775", GREY, 20)
    for x in (250, 750):
        a.shape(circle_d(x, 790, 72), CHAR)
        a.shape(circle_d(x, 790, 44), CREAM, shade=False, sw=12, halo=False)
        for k in range(4):
            ang = k * math.pi / 4
            a.stroke(f"M{x-42*math.cos(ang):.0f} {790-42*math.sin(ang):.0f} L{x+42*math.cos(ang):.0f} {790+42*math.sin(ang):.0f}", INK, 8, halo=False)
        dot(a, x, 790, 13)
    # Flossen
    a.shape("M380 510 L262 690 L392 700 Z", RUST); a.shape("M620 510 L738 690 L608 700 Z", RUST)
    a.stroke("M330 640 L385 600 M670 640 L615 600", CREAM, 12, halo=False)
    # Körper
    a.shape("M500 80 C645 195 668 450 625 705 L375 705 C332 450 355 195 500 80 Z", CREAM)
    a.shape("M500 80 C562 132 602 196 622 248 L378 248 C398 196 438 132 500 80 Z", RUST, halo=False)
    hl(a, "M470 120 Q440 150 420 200", 12)
    a.raw(f'<rect x="352" y="590" width="296" height="40" fill="{RUST}"/>')
    a.stroke("M350 590 L650 590 M350 630 L650 630", INK, 10, halo=False)
    a.stroke("M372 470 L628 470", INK, 8, halo=False)
    for y in (275, 500, 560):
        for x in (395, 605):
            dot(a, x, y, 7, INK)
    a.shape(circle_d(500, 385, 88), GREY, sw=16, halo=False)
    a.shape(circle_d(500, 385, 64), TEAL, sw=12, halo=False)
    for k in range(6):
        ang = k * math.pi / 3
        dot(a, f"{500+76*math.cos(ang):.0f}", f"{385+76*math.sin(ang):.0f}", 6, INK)
    hl(a, "M465 360 Q475 338 500 332", 12)
    hl(a, "M415 300 Q395 420 405 560", 14)
    return a


PINK = "#E8A0A0"

def face(a, cx, cy, s=1.0, mood="muede"):
    ex = 38 * s
    if mood == "muede":
        for x in (cx - ex, cx + ex):
            a.raw(f'<ellipse cx="{x}" cy="{cy}" rx="{22*s}" ry="{16*s}" fill="{CREAM}" stroke="{INK}" stroke-width="{9*s}"/>')
            a.raw(f'<circle cx="{x}" cy="{cy+5*s}" r="{8*s}" fill="{INK}"/>')
            a.raw(f'<path d="M{x-26*s} {cy-2*s} Q{x} {cy-24*s} {x+26*s} {cy-2*s} Z" fill="{INK}"/>')
        a.raw(f'<ellipse cx="{cx}" cy="{cy+46*s}" rx="{16*s}" ry="{20*s}" fill="{INK}"/>')
    elif mood == "zu":
        for x in (cx - ex, cx + ex):
            a.raw(f'<path d="M{x-18*s} {cy} Q{x} {cy+14*s} {x+18*s} {cy}" fill="none" stroke="{INK}" stroke-width="{9*s}" stroke-linecap="round"/>')
        a.raw(f'<path d="M{cx-14*s} {cy+34*s} Q{cx} {cy+44*s} {cx+14*s} {cy+34*s}" fill="none" stroke="{INK}" stroke-width="{8*s}" stroke-linecap="round"/>')
    elif mood == "traurig":
        for x in (cx - ex, cx + ex):
            a.raw(f'<circle cx="{x}" cy="{cy}" r="{10*s}" fill="{INK}"/>')
            a.raw(f'<path d="M{x-18*s} {cy-22*s} L{x+(8 if x<cx else -8)*s} {cy-30*s}" stroke="{INK}" stroke-width="{7*s}" stroke-linecap="round"/>')
        a.raw(f'<path d="M{cx-18*s} {cy+42*s} Q{cx} {cy+28*s} {cx+18*s} {cy+42*s}" fill="none" stroke="{INK}" stroke-width="{8*s}" stroke-linecap="round"/>')
    elif mood == "schreck":
        for x in (cx - ex, cx + ex):
            a.raw(f'<circle cx="{x}" cy="{cy}" r="{20*s}" fill="{CREAM}" stroke="{INK}" stroke-width="{8*s}"/><circle cx="{x}" cy="{cy}" r="{7*s}" fill="{INK}"/>')
        a.raw(f'<ellipse cx="{cx}" cy="{cy+50*s}" rx="{18*s}" ry="{26*s}" fill="{INK}"/>')
    elif mood == "froh":
        for x in (cx - ex, cx + ex):
            a.raw(f'<path d="M{x-16*s} {cy+4*s} Q{x} {cy-14*s} {x+16*s} {cy+4*s}" fill="none" stroke="{INK}" stroke-width="{9*s}" stroke-linecap="round"/>')
        a.raw(f'<path d="M{cx-22*s} {cy+30*s} Q{cx} {cy+58*s} {cx+22*s} {cy+30*s} Z" fill="{RUST}" stroke="{INK}" stroke-width="{7*s}" stroke-linejoin="round"/>')
    for x in (cx - ex - 18 * s, cx + ex + 18 * s):
        a.raw(f'<ellipse cx="{x}" cy="{cy+30*s}" rx="{14*s}" ry="{8*s}" fill="{PINK}"/>')

def tree(a, x, y, h, col=OLIVE):
    a.shape(f"M{x} {y-h} L{x+h*0.32} {y-h*0.45} L{x+h*0.18} {y-h*0.45} L{x+h*0.4} {y} L{x-h*0.4} {y} L{x-h*0.18} {y-h*0.45} L{x-h*0.32} {y-h*0.45} Z", col, sw=12, halo=False)
    a.stroke(f"M{x} {y} L{x} {y+h*0.15}", "#55341D", 14, halo=False)

# ------------------------------------------------------------------ 6 Akku-Tasse
def akku_tasse():
    a = Art(); blob(a, 500, 470, 400, TEAL, seed=3)
    for x, y, r in ((170, 260, 26), (830, 220, 20), (860, 600, 16), (150, 640, 18)):
        sparkle_bg(a, x, y, r)
    a.shape(ell_d(500, 860, 300, 50), CREAM)
    a.shape(ell_d(500, 845, 220, 26), CREAM_D, shade=False, sw=12, halo=False)
    a.stroke("M330 160 Q300 120 330 80 Q360 40 330 0", CREAM, 16)
    a.stroke("M500 160 Q470 110 500 70 Q530 30 500 -10", CREAM, 16)
    a.stroke("M670 160 Q640 120 670 80 Q700 40 670 0", CREAM, 16)
    a.thick("M700 380 C860 380 860 660 700 660", CREAM, 54)
    a.shape("M270 220 L730 220 L710 790 Q705 840 650 840 L350 840 Q295 840 290 790 Z", CREAM)
    a.shape(ell_d(500, 220, 230, 40), COFFEE, shade=False, sw=SW, halo=False)
    a.raw(f'<path d="M290 300 L710 300 L708 350 L292 350 Z" fill="{ORANGE}"/>')
    a.stroke("M290 300 L710 300 M292 350 L708 350", INK, 10, halo=False)
    # Akku-Anzeige
    a.shape(rect_d(380, 560, 220, 110, 16), "none", halo=False, sw=14)
    a.shape(rect_d(600, 595, 22, 40, 6), INK, shade=False, sw=0, halo=False)
    a.shape(rect_d(396, 576, 36, 78, 6), RUST, shade=False, sw=0, halo=False)
    a.shape(bolt(510, 615, 70), MUST, shade=False, sw=7, halo=False)
    face(a, 500, 440, 1.6, "muede")
    hl(a, "M320 400 Q310 560 330 720", 14)
    return a

# ------------------------------------------------------------------ 7 EKG-Berge
def ekg_berge():
    a = Art(); window(a, 70, 170, 860, 640, 70, (MUST, ORANGE, RUST), 0.55)
    a.bg.append(f'<circle cx="720" cy="330" r="80" fill="{CREAM}"/>')
    # Berge
    a.shape("M120 790 L360 380 L470 540 L600 300 L880 790 Z", OLIVE, halo=False)
    a.shape("M360 380 L405 455 L380 448 L360 470 L338 445 L318 452 Z", CREAM, shade=False, sw=12, halo=False)
    a.shape("M600 300 L650 385 L622 375 L600 400 L575 372 L548 385 Z", CREAM, shade=False, sw=12, halo=False)
    for x, h in ((170, 120), (230, 160), (760, 150), (830, 110), (300, 100)):
        tree(a, x, 790, h, "#4E5A2C")
    # EKG-Linie
    a.stroke("M20 700 L230 700 L262 640 L300 770 L336 700 L360 700 L470 540 L540 640 L600 300 L700 700 L980 700", RUST, 26)
    a.shape("M780 640 C780 600 830 600 830 640 C830 600 880 600 880 640 C880 690 830 710 830 740 C830 710 780 690 780 640 Z", RUST, sw=14)
    return a

# ------------------------------------------------------------------ 8 Einzelsocke
def einzelsocke():
    a = Art(); diamond(a, 500, 500, 430, cols=(MUST, ORANGE, RUST))
    a.thick("M140 200 L140 900", "#7A4E2D", 34); a.thick("M860 200 L860 900", "#7A4E2D", 34)
    a.stroke("M140 250 Q500 360 860 250", INK, 10)
    for x, y in ((250, 280), (330, 296), (420, 306), (590, 306), (680, 296), (760, 280)):
        a.shape(rect_d(x - 12, y - 34, 24, 66, 6), MUST, shade=False, sw=9, halo=False)
    # Vögel
    for x, y, f in ((300, 287, 1), (700, 286, -1)):
        a.shape(f"M{x-40*f} {y} C{x-40*f} {y-50} {x+30*f} {y-60} {x+40*f} {y-25} L{x+68*f} {y-30} L{x+42*f} {y-8} C{x+30*f} {y+8} {x-20*f} {y+8} {x-40*f} {y} Z", CREAM, sw=12)
        dot(a, x + 22 * f, y - 32, 6)
    # Socke
    a.shape("M450 320 L560 320 L560 620 Q560 660 600 672 L680 696 Q752 718 736 778 Q720 832 652 816 L495 780 Q440 765 440 705 Z", ORANGE)
    for y in (360, 400):
        a.raw(f'<rect x="452" y="{y}" width="106" height="20" fill="{CREAM}"/>')
    a.stroke("M452 360 L558 360 M452 380 L558 380 M452 400 L558 400 M452 420 L558 420", INK, 6, halo=False)
    a.shape("M640 700 Q690 700 720 730 Q735 760 700 790 Q680 760 640 750 Z", RUST, shade=False, sw=0, halo=False)
    a.shape(rect_d(492, 290, 26, 70, 6), MUST, shade=False, sw=10, halo=False)
    face(a, 505, 540, 0.9, "traurig")
    a.raw(f'<path d="M478 548 q-10 30 0 40 q10 -10 0 -40 Z" fill="{SKY}" stroke="{INK}" stroke-width="5"/>')
    return a

# ------------------------------------------------------------------ 9 WLAN
def wlan():
    a = Art()
    a.bg.append(f'<path d="M80 760 Q80 220 500 160 Q920 220 920 760 Z" fill="{TEAL}"/>')
    for x, y, r in ((200, 380, 14), (790, 330, 18), (320, 250, 10), (700, 470, 10)):
        sparkle_bg(a, x, y, r)
    hills(a, 700, cols=(OLIVE, "#4E5A2C"), sun=None)
    for x, h in ((140, 200), (230, 260), (800, 240), (880, 190)):
        tree(a, x, 860, h, "#3E4A22")
    # WLAN-Symbol
    for r, col in ((300, CREAM), (210, CREAM), (120, CREAM)):
        a.raw(f'<path d="M{500-r*0.77:.0f} {520-r*0.64:.0f} A{r} {r} 0 0 1 {500+r*0.77:.0f} {520-r*0.64:.0f}" fill="none" stroke="{col}" stroke-width="30" stroke-linecap="round" stroke-dasharray="6 44"/>')
    a.shape(circle_d(500, 520, 44), RUST, sw=14)
    # Zelt + Feuer
    a.shape("M320 860 L500 610 L680 860 Z", ORANGE)
    a.shape("M500 610 L455 860 L545 860 Z", "#2A1D17", shade=False, sw=10, halo=False)
    a.stroke("M500 610 L500 580", INK, 12)
    a.shape("M740 860 Q730 790 770 750 Q780 800 800 790 Q810 820 800 860 Z", ORANGE, shade=False, sw=12)
    a.stroke("M720 870 L830 850 M720 850 L830 870", "#7A4E2D", 14)
    return a

# ------------------------------------------------------------------ 10 Kaffee-Sanduhr
def kaffee_sanduhr():
    a = Art(); rays(a, 500, 500, 450, RUST, ORANGE, n=16)
    for k, y in enumerate((90, 860)):
        a.shape(rect_d(250, y, 500, 60, 18), "#7A4E2D")
        a.stroke(f"M280 {y+20} L720 {y+20}", "#55341D", 6, halo=False)
    a.thick("M290 150 L290 860", "#7A4E2D", 26); a.thick("M710 150 L710 860", "#7A4E2D", 26)
    glass = "M345 150 C345 400 470 450 470 505 C470 560 345 610 345 860 L655 860 C655 610 530 560 530 505 C530 450 655 400 655 150 Z"
    a.shape(glass, SKY, shade=False, sw=SW, halo=False)
    a.shape("M362 220 L638 220 C630 380 540 430 500 470 C460 430 370 380 362 220 Z", "#5E3A22", shade=False, sw=0, halo=False)
    a.shape("M380 860 Q500 690 620 860 Z", "#5E3A22", shade=False, sw=0, halo=False)
    a.stroke("M500 480 L500 760", "#5E3A22", 10, halo=False)
    for x, y, r in ((420, 250, 20), (500, 235, -15), (575, 255, 30), (455, 310, -25), (545, 305, 15)):
        a.raw(f'<g transform="translate({x} {y}) rotate({r})"><ellipse rx="26" ry="36" fill="{COFFEE}" stroke="{INK}" stroke-width="10"/><path d="M0 -30 C-12 -10 12 10 0 30" fill="none" stroke="{INK}" stroke-width="8"/></g>')
    a.shape(glass, "none", halo=False)
    hl(a, "M380 200 Q385 330 430 400", 12); hl(a, "M380 820 Q390 700 440 620", 12)
    return a

# ------------------------------------------------------------------ 11 Sofa
def couch():
    a = Art(); window(a, 90, 120, 820, 720, 60, ("#C9583A", ORANGE, MUST), 0.75)
    # Stehlampe + Pflanze
    a.stroke("M800 380 L800 860", INK, 14)
    a.shape("M730 380 L870 380 L840 260 L760 260 Z", MUST)
    a.shape(rect_d(130, 760, 110, 100, 14), RUST)
    for d in ("M185 760 Q120 640 160 560", "M185 760 Q190 620 230 540", "M185 760 Q250 660 260 600"):
        a.stroke(d, OLIVE, 26)
    # Teppich
    a.shape(ell_d(500, 900, 400, 50), TEAL, sw=14)
    # Sofa
    a.stroke("M260 850 L260 890 M740 850 L740 890", INK, 20)
    a.shape(rect_d(250, 360, 500, 300, 50), TEAL)
    a.shape("M240 620 L500 620 L500 790 L240 790 Z", "#1F4442", shade=False)
    a.shape("M240 700 Q305 770 370 720 Q435 770 500 700 L500 790 L240 790 Z", TEAL)
    a.shape(rect_d(500, 620, 260, 170, 24), TEAL)
    a.shape(rect_d(220, 780, 560, 80, 12), "#7A4E2D")
    a.shape(rect_d(150, 520, 120, 330, 55), TEAL) ; a.shape(rect_d(730, 520, 120, 330, 55), TEAL)
    # Krümel + Kissen
    a.shape("M560 470 L700 440 L720 590 L580 610 Z", MUST)
    for x, y in ((290, 760), (330, 770), (450, 765), (410, 775)):
        dot(a, x, y, 7, MUST)
    return a

# ------------------------------------------------------------------ 12 Kaffee-Infusion
def kaffee_tropf():
    a = Art(); blob(a, 500, 500, 420, MUST, seed=7)
    a.bg.append(f'<path d="M140 780 L860 780" stroke="{ORANGE}" stroke-width="40"/>')
    # Ständer
    a.thick("M660 110 L660 900", GREY, 18)
    a.thick("M560 110 L760 110", GREY, 14)
    for x in (560, 760):
        a.stroke(f"M{x} 110 L{x} 150", INK, 10)
    a.stroke("M560 900 L760 900 M600 900 L580 940 M720 900 L740 940", INK, 18)
    # Beutel
    a.shape("M490 150 L630 150 Q650 150 650 175 L650 380 Q650 430 600 440 L520 440 Q470 430 470 380 L470 175 Q470 150 490 150 Z", CREAM)
    a.shape("M474 240 L646 240 L646 380 Q646 426 600 436 L520 436 Q474 426 474 380 Z", COFFEE, sw=0, halo=False)
    a.raw(f'<g transform="translate(560 320)"><ellipse rx="40" ry="56" fill="#5E3A22"/><path d="M0 -46 C-18 -16 18 16 0 46" stroke="{COFFEE}" stroke-width="10" fill="none"/></g>')
    a.shape(rect_d(540, 440, 40, 80, 10), SKY, sw=12)
    a.stroke("M560 520 C560 650 380 560 360 640", INK, 12)
    # Patient: müde Tasse
    a.thick("M545 700 C640 700 640 820 545 820", CREAM, 40)
    a.shape("M200 640 L560 640 L540 860 Q535 900 495 900 L265 900 Q225 900 220 860 Z", CREAM)
    a.shape(ell_d(380, 640, 180, 30), COFFEE, shade=False, sw=SW, halo=False)
    face(a, 380, 740, 1.0, "zu")
    a.shape(rect_d(230, 800, 300, 34, 0), RUST, shade=False, sw=0, halo=False)
    return a


SAUS = "#C8553D"; DARK[SAUS] = "#9A3A28"
BUN = "#E3A857"; DARK[BUN] = "#B97F35"

# ------------------------------------------------------------------ 13 Wurst im Schlafrock
def wurst_schlafrock():
    a = Art(); window(a, 160, 110, 680, 800, 120, (MUST, ORANGE, "#C9583A"), 0.6)
    # Pantoffeln
    a.shape(ell_d(420, 900, 85, 34), TEAL); a.shape(ell_d(580, 900, 85, 34), TEAL)
    # Wurst
    a.shape(rect_d(400, 140, 200, 760, 100), SAUS)
    a.stroke("M430 200 Q440 175 470 165", CREAM, 12, halo=False)
    face(a, 500, 260, 1.0, "zu")
    a.stroke("M560 220 L600 200 M440 220 L400 200", INK, 0, halo=False)
    # Bademantel
    robe = "M360 400 L455 395 L500 560 L545 395 L640 400 L680 870 L320 870 Z"
    a.shape(robe, TEAL)
    a.stroke("M455 395 L500 560 L545 395", CREAM, 26, halo=False)
    a.stroke("M455 395 L500 560 L545 395", INK, 8, halo=False)
    a.stroke("M500 560 L500 870", INK, 9, halo=False)
    for y in (450, 520, 610, 700, 790):
        a.stroke(f"M335 {y} L360 {y-10} M640 {y-10} L665 {y}", "#1F4442", 8, halo=False)
    a.shape(rect_d(340, 610, 320, 44, 20), MUST, sw=14, halo=False)
    a.shape("M480 640 L455 730 L490 720 Z", MUST, sw=10, halo=False); a.shape("M520 640 L545 730 L510 720 Z", MUST, sw=10, halo=False)
    a.shape(rect_d(560, 690, 80, 70, 10), "#1F4442", sw=12, halo=False)
    # Arme + Kaffeetasse
    a.thick("M370 430 L290 560 L380 640", TEAL, 60)
    a.thick("M630 430 L700 560 L640 640", TEAL, 60)
    a.shape(circle_d(395, 640, 28), SAUS, sw=12, halo=False)
    a.raw('<g transform="rotate(-8 620 640)">')
    a.shape(rect_d(560, 580, 110, 120, 14), CREAM)
    a.stroke("M670 605 Q715 605 715 640 Q715 675 670 675", INK, 18)
    a.shape(ell_d(615, 582, 55, 12), COFFEE, shade=False, sw=10, halo=False)
    a.raw('</g>')
    a.stroke("M600 550 Q585 520 605 495 Q625 470 610 440 M640 545 Q628 520 645 500", CREAM, 10)
    return a

# ------------------------------------------------------------------ 14 Dackel-Hotdog
def dackel_hotdog():
    a = Art(); rays(a, 500, 500, 460, TEAL, "#3F7470", n=22)
    # Flaschen
    a.shape("M790 330 L860 330 L870 600 Q870 630 840 630 L810 630 Q780 630 780 600 Z", RUST)
    a.shape("M805 330 L845 330 L835 270 L815 270 Z", RUST); a.shape(rect_d(812, 245, 26, 30, 6), CREAM, sw=10)
    a.shape("M130 360 L200 360 L210 620 Q210 650 180 650 L150 650 Q120 650 120 620 Z", MUST)
    a.shape("M145 360 L185 360 L175 300 L155 300 Z", MUST); a.shape(rect_d(152, 275, 26, 30, 6), CREAM, sw=10)
    # Brötchen hinten
    a.shape("M170 600 Q170 470 300 470 L700 470 Q830 470 830 600 Z", BUN)
    # Dackel
    a.thick("M250 560 Q170 520 160 440", SAUS, 30)
    a.shape("M230 640 Q215 520 310 520 L680 520 Q760 520 770 590 L770 650 L230 650 Z", SAUS)
    a.shape("M670 545 Q660 400 780 385 Q880 378 905 450 L940 482 Q915 530 850 520 L800 540 Z", SAUS)
    a.shape("M740 400 Q690 455 720 570 Q770 550 785 470 Z", "#7A2F1E", shade=False, sw=14)
    a.raw(f'<circle cx="835" cy="440" r="13" fill="{INK}"/><circle cx="839" cy="436" r="4" fill="{CREAM}"/>')
    a.raw(f'<ellipse cx="943" cy="482" rx="18" ry="14" fill="{INK}"/>')
    a.stroke("M880 505 Q900 515 915 505", INK, 8, halo=False)
    a.shape("M880 510 Q890 545 905 540 Q912 525 905 510 Z", PINK, shade=False, sw=7, halo=False)
    # Senf
    a.stroke("M290 555 Q320 525 350 555 T410 555 T470 555 T530 555 T590 555 T650 555 T710 555", MUST, 22, halo=False)
    # Brötchen vorne
    a.shape("M150 600 Q150 760 320 760 L680 760 Q850 760 850 600 L780 600 Q760 660 700 660 L300 660 Q240 660 220 600 Z", BUN)
    for x, y in ((320, 715), (420, 730), (540, 722), (650, 712), (380, 690)):
        a.raw(f'<ellipse cx="{x}" cy="{y}" rx="9" ry="5" fill="{CREAM}" transform="rotate(20 {x} {y})"/>')
    # Pfoten
    for x in (300, 380, 620, 700):
        a.shape(ell_d(x, 662, 28, 16), SAUS, sw=12, halo=False)
    return a

# ------------------------------------------------------------------ 15 Katze-Karton
def katze_karton():
    a = Art(); arch(a, 150, 100, 700, 780, cols=(MUST, ORANGE, RUST))
    CARD = "#C9955A"; DARK[CARD] = "#9C6E3C"
    # Karton hinten
    a.shape("M310 560 L690 560 L740 470 L360 470 Z", "#9C6E3C", shade=False)
    # Katze (zu groß)
    a.shape(ell_d(500, 560, 290, 110), GREY)
    a.shape("M360 470 C360 330 420 300 500 300 C580 300 640 330 640 470 Z", GREY)
    a.shape("M380 360 L370 230 L460 310 Z", GREY); a.shape("M620 360 L630 230 L540 310 Z", GREY)
    a.shape("M386 320 L380 262 L428 306 Z", PINK, shade=False, sw=0, halo=False)
    a.shape("M614 320 L620 262 L572 306 Z", PINK, shade=False, sw=0, halo=False)
    for d in ("M470 310 L475 345", "M500 305 L500 345", "M530 310 L525 345"):
        a.stroke(d, GREY_D, 10, halo=False)
    face(a, 500, 400, 1.0, "zu")
    a.stroke("M420 430 L360 425 M420 445 L362 460 M580 430 L640 425 M580 445 L638 460", INK, 6, halo=False)
    # Pfoten über Rand
    a.shape(ell_d(330, 600, 60, 34), GREY, sw=14); a.shape(ell_d(670, 600, 60, 34), GREY, sw=14)
    # Karton vorne
    a.shape("M310 590 L690 590 L670 880 L330 880 Z", CARD)
    a.shape("M310 590 L230 520 L250 640 Z", CARD); a.shape("M690 590 L770 520 L750 640 Z", CARD)
    a.shape(rect_d(470, 590, 60, 290, 0), "#E3C08A", shade=False, sw=10, halo=False)
    a.shape("M400 700 L600 700 L600 790 L400 790 Z", "none", halo=False, sw=0)
    a.stroke("M560 760 L585 790 L640 720", RUST, 14, halo=False)
    # Schwanz hängt raus
    a.thick("M680 650 Q800 680 790 800", GREY, 40)
    return a

# ------------------------------------------------------------------ 16 Katze-Tastatur
def katze_tastatur():
    a = Art(); window(a, 90, 90, 820, 760, 60, (TEAL, "#3F7470", "#1F4442"), 0.6)
    a.bg.append(f'<rect x="90" y="760" width="820" height="90" fill="#7A4E2D"/>')
    # Monitor
    a.shape(rect_d(250, 170, 500, 330, 24), CHAR)
    a.shape(rect_d(275, 195, 450, 280, 10), SKY, shade=False, sw=12, halo=False)
    for k in range(5):
        a.raw(f'<rect x="300" y="{220+k*45}" width="{380-k*40 if k%2==0 else 260}" height="16" rx="8" fill="{CREAM}"/>')
    a.raw('<rect x="300" y="420" width="330" height="16" rx="8" fill="#C8553D"/>')
    for k in range(6):
        a.raw(f'<rect x="{390+k*38}" y="420" width="26" height="16" rx="4" fill="#C8553D"/>')
    a.shape("M460 500 L540 500 L560 590 L440 590 Z", GREY)
    # Tastatur
    a.shape(rect_d(170, 610, 660, 170, 22), GREY)
    for r in range(3):
        for c in range(12):
            a.raw(f'<rect x="{200+c*52}" y="{630+r*44}" width="40" height="32" rx="6" fill="{CREAM}" stroke="{INK}" stroke-width="5"/>')
    # Katze liegt drauf
    ORG = ORANGE
    a.thick("M290 680 Q160 690 170 820", ORG, 42)
    a.shape("M260 700 Q250 580 450 575 L640 575 Q730 575 740 670 L740 700 Z", ORG)
    for x in (380, 450, 520):
        a.stroke(f"M{x} 585 Q{x+15} 620 {x} 655", RUST, 12, halo=False)
    a.shape("M650 560 L640 455 L710 515 Z", ORG); a.shape("M800 560 L815 455 L745 515 Z", ORG)
    a.shape(ell_d(725, 590, 108, 92), ORG)
    face(a, 725, 580, 0.9, "zu")
    # Tasse
    a.shape(rect_d(800, 640, 80, 100, 12), MUST)
    a.stroke("M880 660 Q910 660 910 690 Q910 720 880 720", INK, 14)
    a.stroke("M830 620 Q815 590 835 560", CREAM, 9)
    return a

# ------------------------------------------------------------------ 17 Croissant-Mond
def croissant_mond():
    a = Art(); sunset(a, cols=("#1F4442", TEAL, "#3F7470"), horizon=0.3)
    for x, y, r in ((760, 230, 30), (820, 420, 20), (700, 640, 24), (300, 130, 16), (860, 600, 12)):
        sparkle_bg(a, x, y, r, MUST)
    cloud_bg(a, 680, 780, 1.0); cloud_bg(a, 820, 330, 0.6)
    CRO = "#E3A857"; DARK[CRO] = "#B97F35"
    cx, cy, R = 600, 470, 330
    lobes = [(-62, 55), (62, 55), (-42, 85), (42, 85), (-21, 115), (21, 115), (0, 140)]
    for ang, size in lobes:
        t = math.radians(180 + ang)
        x, y = cx + R * math.cos(t), cy + R * math.sin(t)
        a.raw(f'<g transform="rotate({ang} {x:.0f} {y:.0f})">')
        a.shape(ell_d(round(x), round(y), round(size * 1.2), round(size * 0.8)), CRO, dx=-18, dy=-22)
        if ang: a.stroke(f"M{x-size*0.3:.0f} {y-size*0.55:.0f} Q{x-size*0.05:.0f} {y:.0f} {x-size*0.3:.0f} {y+size*0.55:.0f}", "#B97F35", 9, halo=False)
        a.raw('</g>')
    face(a, 275, 470, 1.1, "zu")
    hl(a, "M230 400 Q225 380 240 360", 10)
    t = math.radians(242); x, y = cx + R * math.cos(t), cy + R * math.sin(t)
    a.shape(f"M{x-60:.0f} {y+10:.0f} Q{x+40:.0f} {y-120:.0f} {x+170:.0f} {y-90:.0f} Q{x+250:.0f} {y-70:.0f} {x+270:.0f} {y-140:.0f} L{x+300:.0f} {y-110:.0f} Q{x+250:.0f} {y-20:.0f} {x+140:.0f} {y-30:.0f} Q{x+40:.0f} {y-40:.0f} {x+40:.0f} {y+40:.0f} Z", RUST)
    a.shape(circle_d(round(x+285), round(y-130), 32), CREAM, sw=12)
    return a

# ------------------------------------------------------------------ 18 Donut-Rettungsring
def donut_ring():
    a = Art(); diamond(a, 500, 500, 440, cols=(MUST, ORANGE, "#3F7470"))
    a.bg.append(f'<circle cx="680" cy="250" r="70" fill="{CREAM}"/>')
    # Wellen hinten
    a.shape("M80 620 Q160 580 240 620 T400 620 T560 620 T720 620 T880 620 T960 620 L960 760 L80 760 Z", TEAL, halo=False)
    # Donut
    a.shape(circle_d(500, 520, 250), BUN)
    icing = "M500 290 C600 280 720 360 728 470 C750 560 700 620 650 650 C640 700 560 760 500 750 C430 765 340 720 320 650 C270 610 250 540 272 470 C290 360 400 280 500 290 Z"
    a.shape(icing, "#E57B9B", halo=False)
    DARK["#E57B9B"] = "#B8577A"
    a.shape(circle_d(500, 520, 90), TEAL, shade=False, halo=False)
    for k, ang in enumerate(range(0, 360, 28)):
        x, y = 500 + 170 * math.cos(math.radians(ang)), 520 + 170 * math.sin(math.radians(ang))
        col = (MUST, CREAM, SKY)[k % 3]
        a.raw(f'<rect x="{x-18:.0f}" y="{y-6:.0f}" width="36" height="12" rx="6" fill="{col}" transform="rotate({ang*2} {x:.0f} {y:.0f})"/>')
    # Seil
    for ang in (45, 135, 225, 315):
        x, y = 500 + 250 * math.cos(math.radians(ang)), 520 + 250 * math.sin(math.radians(ang))
        a.raw(f'<g transform="rotate({ang+90} {x:.0f} {y:.0f})">')
        a.shape(rect_d(x - 60, y - 20, 120, 40, 18), CREAM, shade=False, sw=12, halo=False)
        a.stroke(f"M{x-40:.0f} {y-14:.0f} L{x-30:.0f} {y+14:.0f} M{x-10:.0f} {y-14:.0f} L{x:.0f} {y+14:.0f} M{x+20:.0f} {y-14:.0f} L{x+30:.0f} {y+14:.0f}", INK, 6, halo=False)
        a.raw('</g>')
    # Wellen vorne
    a.shape("M80 700 Q160 660 240 700 T400 700 T560 700 T720 700 T880 700 T960 700 L960 900 Q520 940 80 900 Z", "#3F7470")
    DARK["#3F7470"] = "#2E5E5B"
    for y in (760, 820):
        a.stroke(f"M180 {y} Q220 {y-20} 260 {y} M620 {y+10} Q660 {y-10} 700 {y+10}", CREAM, 10, halo=False)
    # Möwe
    a.shape("M200 300 Q240 260 280 300 Q320 260 360 300 Q320 285 280 315 Q240 285 200 300 Z", CREAM, sw=10)
    return a

# ------------------------------------------------------------------ 19 Wecker-Schlafmaske
def wecker_maske():
    a = Art(); rays(a, 500, 470, 440, MUST, "#F0C060", n=24, star=False)
    DARK["#F0C060"] = MUST
    # Bett / Kissen
    a.shape(ell_d(500, 780, 360, 70), CREAM)
    a.shape("M120 760 Q500 650 880 760 L880 900 Q500 960 120 900 Z", TEAL)
    for x in (260, 400, 540, 680):
        a.stroke(f"M{x} 800 L{x+40} 880", "#1F4442", 10, halo=False)
    # Glocken + Bügel
    a.thick("M330 210 Q500 120 670 210", GREY, 18)
    a.shape("M210 300 A120 120 0 0 1 390 170 Z", MUST); a.shape("M790 300 A120 120 0 0 0 610 170 Z", MUST)
    a.stroke("M500 150 L500 205", INK, 18)
    # Gehäuse
    a.shape(circle_d(500, 470, 270), RUST)
    a.shape(circle_d(500, 470, 210), CREAM, sw=16, halo=False)
    for k in range(12):
        ang = k * math.pi / 6
        dot(a, f"{500+180*math.cos(ang):.0f}", f"{470+180*math.sin(ang):.0f}", 9)
    a.stroke("M500 470 L500 330 M500 470 L600 520", INK, 16, halo=False)
    # Schlafmaske
    a.shape("M230 400 Q500 340 770 400 L770 460 Q500 410 230 460 Z", "#1F4442", sw=14, halo=False)
    a.shape("M300 380 Q390 340 480 385 Q480 480 390 490 Q300 480 300 380 Z", "#E57B9B", sw=14, halo=False)
    a.shape("M520 385 Q610 340 700 380 Q700 480 610 490 Q520 480 520 385 Z", "#E57B9B", sw=14, halo=False)
    for x in (390, 610):
        a.stroke(f"M{x-40} 430 Q{x} 460 {x+40} 430", INK, 12, halo=False)
        a.stroke(f"M{x-28} 444 L{x-34} 462 M{x} 452 L{x} 470 M{x+28} 444 L{x+34} 462", INK, 7, halo=False)
    a.shape(ell_d(500, 600, 34, 26), INK, shade=False, sw=0, halo=False)
    # Füße
    a.thick("M330 700 L290 760", RUST, 26); a.thick("M670 700 L710 760", RUST, 26)
    return a


WHITE = "#F7F2E8"; DARK[WHITE] = "#D9D0BE"

# ------------------------------------------------------------------ 20 Steckdose
def steckdose():
    a = Art(); window(a, 80, 140, 840, 700, 60, (MUST, "#F0C060", MUST), 0.99)
    for x in range(140, 900, 90):
        a.bg.append(f'<rect x="{x}" y="140" width="22" height="700" fill="#F0C060"/>')
    a.bg.append(f'<rect x="80" y="760" width="840" height="80" fill="#7A4E2D"/>')
    # Steckdose
    a.shape(rect_d(150, 270, 380, 380, 60), WHITE)
    a.shape(circle_d(340, 460, 140), CREAM, sw=16, halo=False)
    for x in (290, 390):
        a.raw(f'<circle cx="{x}" cy="420" r="30" fill="{CREAM}" stroke="{INK}" stroke-width="10"/><circle cx="{x}" cy="420" r="11" fill="{INK}"/>')
    a.raw(f'<ellipse cx="340" cy="510" rx="30" ry="40" fill="{INK}"/>')
    a.raw(f'<path d="M260 375 L320 395 M420 375 L360 395" stroke="{INK}" stroke-width="10" stroke-linecap="round"/>')
    a.shape(drop_d(470, 330), SKY, shade=False, sw=8, halo=False)
    for d in ("M560 260 L600 220", "M580 330 L640 320", "M560 190 L575 150"):
        a.stroke(d, INK, 12)
    # Kabel + Stecker
    a.thick("M950 900 Q820 900 820 760 Q820 620 790 560", "#3A3A3A", 26)
    a.shape(rect_d(650, 380, 190, 190, 40), RUST)
    a.shape(rect_d(560, 430, 100, 26, 10), GREY, sw=12); a.shape(rect_d(560, 500, 100, 26, 10), GREY, sw=12)
    # grinsender Stecker
    a.raw(f'<path d="M690 450 L730 465 L690 470 M800 450 L760 465 L800 470" fill="none" stroke="{INK}" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>')
    a.raw(f'<path d="M700 505 Q745 545 790 505 Z" fill="{CREAM}" stroke="{INK}" stroke-width="9" stroke-linejoin="round"/>')
    return a

def drop_d(cx, cy, s=1.0):
    return f"M{cx} {cy-40*s} C{cx+18*s} {cy-12*s} {cx+30*s} {cy+4*s} {cx+30*s} {cy+18*s} A{30*s} {30*s} 0 0 1 {cx-30*s} {cy+18*s} C{cx-30*s} {cy+4*s} {cx-18*s} {cy-12*s} {cx} {cy-40*s} Z"

# ------------------------------------------------------------------ 21 Fernbedienung
def fernbedienung():
    a = Art(); blob(a, 500, 470, 430, ORANGE, seed=11)
    for x, y, r in ((200, 200, 26), (800, 180, 30), (850, 420, 18), (160, 430, 16)):
        sparkle_bg(a, x, y, r, CREAM)
    # Fernbedienung steckt in der Ritze
    a.raw('<g transform="rotate(-14 500 420)">')
    a.shape(rect_d(440, 170, 120, 430, 46), CHAR)
    a.shape(circle_d(500, 235, 26), RUST, sw=10, halo=False)
    for r in range(3):
        for c in range(2):
            a.shape(rect_d(465 + c * 45, 300 + r * 55, 30, 30, 8), MUST, shade=False, sw=7, halo=False)
    a.shape(rect_d(470, 470, 60, 40, 10), SKY, shade=False, sw=7, halo=False)
    a.raw('</g>')
    for d in ("M420 120 L395 70", "M520 90 L525 30", "M610 130 L650 85"):
        a.stroke(d, CREAM, 16)
    # Kissen
    a.shape(rect_d(110, 470, 400, 230, 70), TEAL)
    a.shape(rect_d(490, 470, 400, 230, 70), TEAL)
    for x in (180, 560):
        a.stroke(f"M{x} 520 Q{x+20} 600 {x} 660", "#1F4442", 10, halo=False)
    for x in (310, 690):
        a.raw(f'<circle cx="{x}" cy="585" r="12" fill="#1F4442"/>')
    # Sofa-Front
    a.shape(rect_d(80, 680, 840, 150, 30), RUST)
    a.stroke("M160 830 L160 900 M840 830 L840 900", INK, 24)
    # Krümel / Münze / Popcorn
    a.shape(circle_d(300, 470, 28), MUST, sw=10); a.stroke("M290 460 L310 480", "#C98A22", 6, halo=False)
    for x, y in ((650, 465), (690, 455), (720, 470)):
        a.shape(circle_d(x, y, 22), CREAM, sw=9)
    return a

# ------------------------------------------------------------------ 22 Sonne schwitzt
def sonne():
    a = Art()
    a.bg.append(f'<path d="M100 700 Q300 650 500 700 T900 700 L900 820 Q500 870 100 820 Z" fill="{TEAL}"/>')
    a.bg.append(f'<path d="M80 800 Q500 740 920 800 L920 900 Q500 950 80 900 Z" fill="#E3C08A"/>')
    for k in range(16):
        ang = k * math.pi / 8
        a.shape(f"M{500+260*math.cos(ang-0.12):.0f} {420+260*math.sin(ang-0.12):.0f} L{500+(410 if k%2 else 360)*math.cos(ang):.0f} {420+(410 if k%2 else 360)*math.sin(ang):.0f} L{500+260*math.cos(ang+0.12):.0f} {420+260*math.sin(ang+0.12):.0f} Z", ORANGE if k % 2 else MUST, sw=12)
    a.shape(circle_d(500, 420, 270), MUST)
    # Sonnenbrille
    a.stroke("M290 380 L710 380", INK, 16, halo=False)
    a.shape("M300 370 L480 370 Q480 470 400 470 Q310 470 300 370 Z", CHAR, sw=12, halo=False)
    a.shape("M520 370 L700 370 Q690 470 600 470 Q520 470 520 370 Z", CHAR, sw=12, halo=False)
    hl(a, "M330 395 L380 395", 10); hl(a, "M550 395 L600 395", 10)
    a.stroke("M420 560 Q450 540 480 560 T540 560 T600 560", INK, 12, halo=False)
    for x in (340, 660):
        a.raw(f'<ellipse cx="{x}" cy="520" rx="34" ry="18" fill="{ORANGE}"/>')
    # Schweiß
    for x, y, s in ((730, 300, 1.2), (250, 520, 0.9), (700, 560, 0.8)):
        a.shape(drop_d(x, y, s), SKY, shade=False, sw=9)
    # Eis in der Hand
    a.thick("M720 600 Q790 640 800 700", MUST, 40)
    a.shape("M770 700 L850 700 L810 830 Z", "#E3A857", sw=14)
    a.stroke("M780 730 L830 760 M795 770 L820 740", "#B97F35", 6, halo=False)
    a.shape("M760 700 Q760 630 810 630 Q860 630 860 700 Q850 720 835 700 Q820 735 805 700 Q790 725 775 700 Z", "#E57B9B")
    a.shape(drop_d(780, 760, 0.6), "#E57B9B", shade=False, sw=7, halo=False)
    return a

# ------------------------------------------------------------------ 23 Torte + Feuerlöscher
def torte():
    a = Art(); rays(a, 470, 460, 440, RUST, ORANGE, n=14)
    # Rauchwolken
    for x, y, r in ((300, 150, 50), (380, 120, 60), (470, 140, 50), (560, 120, 45)):
        puff(a, x, y, r)
    # Teller + Torte
    a.shape(ell_d(420, 860, 300, 46), CREAM)
    a.shape(rect_d(170, 610, 500, 240, 26), "#E57B9B")
    a.shape("M170 640 Q210 690 250 640 Q290 690 330 640 Q370 690 410 640 Q450 690 490 640 Q530 690 570 640 Q610 690 670 640 L670 620 L170 620 Z", WHITE, halo=False)
    a.shape(rect_d(230, 460, 380, 160, 22), MUST)
    a.shape("M230 480 Q262 520 294 480 Q326 520 358 480 Q390 520 422 480 Q454 520 486 480 Q518 520 550 480 Q582 520 610 480 L610 470 L230 470 Z", WHITE, halo=False)
    for x in (230, 300, 380, 460, 540, 610):
        dot(a, x, 735, 10, WHITE)
    # viele Kerzen mit großen Flammen
    for k in range(10):
        x = 255 + k * 37
        h = 70 + (k % 3) * 18
        a.raw(f'<rect x="{x-9}" y="{460-h}" width="18" height="{h}" fill="{(SKY, CREAM, TEAL)[k%3]}" stroke="{INK}" stroke-width="7"/>')
        fy = 460 - h
        a.shape(f"M{x} {fy-90} Q{x+30} {fy-40} {x+18} {fy-14} Q{x} {fy} {x-18} {fy-14} Q{x-30} {fy-40} {x} {fy-90} Z", ORANGE, shade=False, sw=7, halo=False)
        a.shape(f"M{x} {fy-50} Q{x+12} {fy-28} {x+7} {fy-16} Q{x} {fy-10} {x-7} {fy-16} Q{x-12} {fy-28} {x} {fy-50} Z", MUST, shade=False, sw=0, halo=False)
    # Feuerlöscher
    a.shape(rect_d(740, 420, 150, 440, 66), RUST)
    a.shape(rect_d(752, 560, 126, 120, 6), CREAM, shade=False, sw=10, halo=False)
    a.shape(bolt(815, 620, 80), RUST, shade=False, sw=6, halo=False)
    a.shape(rect_d(775, 360, 80, 70, 10), CHAR)
    a.stroke("M855 380 L910 340", INK, 18)
    a.thick("M790 370 Q720 280 650 300", CHAR, 22)
    a.shape("M650 300 L600 280 L610 320 Z", CHAR, sw=10)
    a.stroke("M590 300 Q520 280 470 300", CREAM, 14)
    hl(a, "M770 470 L770 820", 14)
    return a

# ------------------------------------------------------------------ 24 Bauer mit Krone
def bauer():
    a = Art(); arch(a, 180, 80, 640, 820, cols=(TEAL, "#3F7470", "#1F4442"))
    # Schachbrett-Boden
    floor = ""
    for r in range(3):
        for c in range(10):
            x0 = 120 + c * 76 - r * 14; y0 = 780 + r * 46
            col = CREAM if (r + c) % 2 == 0 else CHAR
            floor += f'<path d="M{x0} {y0} L{x0+76} {y0} L{x0+76-14} {y0+46} L{x0-14} {y0+46} Z" fill="{col}"/>'
    a.halo.append(f'<rect x="80" y="770" width="840" height="160" rx="20" fill="{CREAM}" stroke="{CREAM}" stroke-width="40"/>')
    a.raw(f'<g>{floor}</g><rect x="96" y="780" width="806" height="138" fill="none" stroke="{INK}" stroke-width="{SW}" stroke-linejoin="round"/>')
    # Bauer
    pawn = ("M310 820 L690 820 L690 770 Q690 735 655 735 L600 735 Q550 620 575 500 L615 500 Q640 500 640 470 Q640 440 610 440 "
            "L590 440 Q650 390 650 320 A150 150 0 1 0 350 320 Q350 390 410 440 L390 440 Q360 440 360 470 Q360 500 385 500 "
            "L425 500 Q450 620 400 735 L345 735 Q310 735 310 770 Z")
    # Umhang
    a.shape("M430 470 Q280 640 300 780 L460 760 Q470 600 470 480 Z", MUST, halo=True)
    a.shape("M570 470 Q720 640 700 780 L540 760 Q530 600 530 480 Z", MUST, halo=True)
    a.shape(pawn, RUST)
    hl(a, "M410 260 Q400 300 410 340", 16)
    a.shape(rect_d(400, 455, 200, 40, 20), CREAM, shade=False, sw=12, halo=False)
    # Krone
    a.raw('<g transform="rotate(-10 500 170)">')
    a.shape("M390 230 L370 100 L440 160 L500 70 L560 160 L630 100 L610 230 Z", MUST)
    for x, y, c in ((435, 200, RUST), (500, 195, TEAL), (565, 200, RUST)):
        a.shape(circle_d(x, y, 16), c, shade=False, sw=7, halo=False)
    for x, y in ((370, 100), (500, 70), (630, 100)):
        a.shape(circle_d(x, y, 14), CREAM, shade=False, sw=7, halo=False)
    a.raw('</g>')
    face(a, 500, 330, 1.0, "froh")
    for x, y, r in ((260, 220, 24), (760, 260, 30), (720, 120, 18), (280, 420, 16)):
        sparkle_bg(a, x, y, r, MUST)
    return a

# ------------------------------------------------------------------ 25 Waschmaschine
def waschmaschine():
    a = Art(); window(a, 100, 90, 800, 780, 70, (SKY, "#B9D3DC", SKY), 0.99)
    DARK[SKY] = "#6E98A6"
    for y in range(140, 860, 70):
        a.bg.append(f'<rect x="100" y="{y}" width="800" height="8" fill="#B9D3DC"/>')
    # Wäscheleine oben mit leeren Klammern
    a.stroke("M120 170 Q500 230 880 170", INK, 8)
    for x in (220, 340, 660, 780):
        a.shape(rect_d(x - 10, 165 + (30 if 300 < x < 700 else 14), 20, 52, 5), MUST, shade=False, sw=7, halo=False)
    # Maschine
    a.shape(rect_d(220, 260, 560, 640, 46), WHITE)
    a.shape(rect_d(220, 260, 560, 130, 46), GREY, halo=False)
    a.raw(f'<rect x="222" y="350" width="556" height="40" fill="{GREY}"/>')
    a.stroke("M220 390 L780 390", INK, SW, halo=False)
    a.shape(circle_d(300, 325, 26), RUST, sw=10, halo=False); a.shape(circle_d(370, 325, 26), MUST, sw=10, halo=False)
    a.shape(rect_d(520, 305, 200, 40, 20), CHAR, shade=False, sw=10, halo=False)
    a.raw(f'<rect x="540" y="318" width="70" height="14" rx="7" fill="{SKY}"/>')
    # Bullauge als Mund
    a.shape(circle_d(500, 640, 210), GREY)
    a.shape(circle_d(500, 640, 160), "#3F7470", halo=False)
    a.raw(f'<path d="M380 600 Q500 560 620 600" fill="none" stroke="{CREAM}" stroke-width="10" stroke-linecap="round"/>')
    # Augen über dem Bullauge
    for x in (420, 580):
        a.raw(f'<ellipse cx="{x}" cy="440" rx="26" ry="22" fill="{CREAM}" stroke="{INK}" stroke-width="9"/><circle cx="{x+8}" cy="444" r="9" fill="{INK}"/>')
    a.raw(f'<path d="M392 412 L446 422 M608 412 L554 422" stroke="{INK}" stroke-width="9" stroke-linecap="round"/>')
    # Socke wird verschluckt
    a.shape("M520 700 L610 700 L622 815 Q626 846 658 851 L745 860 Q800 866 797 902 Q793 940 742 937 L598 928 Q545 924 540 870 Z", ORANGE)
    a.raw(f'<rect x="530" y="745" width="84" height="20" fill="{CREAM}"/><rect x="532" y="785" width="86" height="20" fill="{CREAM}"/>')
    a.shape("M745 862 Q797 866 797 902 Q793 940 742 937 Q760 900 745 862 Z", RUST, shade=False, sw=0, halo=False)
    # Rest-Socken am Boden
    a.shape(drop_d(840, 860, 0.6), SKY, shade=False, sw=7)
    return a

MOTIVE = [("katze-schubst-tasse", katze_tasse), ("rennschnecke", rennschnecke), ("faultier-ladebalken", faultier),
          ("grillen-im-regen", grill_regen), ("rakete-stuetzraeder", rakete),
          ("akku-tasse", akku_tasse), ("ekg-berge", ekg_berge), ("einzelsocke", einzelsocke), ("wlan-funkloch", wlan),
          ("kaffee-sanduhr", kaffee_sanduhr), ("sofa-abdruck", couch), ("kaffee-infusion", kaffee_tropf),
          ("wurst-im-schlafrock", wurst_schlafrock), ("dackel-hotdog", dackel_hotdog), ("katze-karton", katze_karton), ("katze-tastatur", katze_tastatur),
          ("croissant-mond", croissant_mond), ("donut-rettungsring", donut_ring), ("wecker-schlafmaske", wecker_maske),
          ("steckdose-erschrickt", steckdose), ("fernbedienung-sofaritze", fernbedienung), ("sonne-schwitzt", sonne), ("torte-feuerloescher", torte),
          ("bauer-mit-krone", bauer), ("waschmaschine-socke", waschmaschine)]

W, H, SCALE = 4500, 5400, 3.7

def bbox(inner):
    open("/tmp/_bb.svg", "w").write(f'<svg xmlns="http://www.w3.org/2000/svg" width="1300" height="1300" viewBox="-150 -150 1300 1300">{inner}</svg>')
    subprocess.run(["rsvg-convert", "-o", "/tmp/_bb.png", "/tmp/_bb.svg"], check=True)
    from PIL import Image
    b = Image.open("/tmp/_bb.png").getchannel("A").getbbox()
    return b[0] - 150, b[1] - 150, b[2] - 150, b[3] - 150

def build(out, which=None):
    os.makedirs(out, exist_ok=True)
    for i, (name, fn) in enumerate(MOTIVE, 1):
        if which and i not in which: continue
        inner = fn().svg(seed=i)
        x0, y0, x1, y1 = bbox(inner)
        sc = min(4300 / (x1 - x0), 4700 / (y1 - y0))
        tx, ty = (W - (x1 - x0) * sc) / 2 - x0 * sc, -y0 * sc
        doc = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
               f'<g transform="translate({tx:.0f} {ty:.0f}) scale({sc:.3f})">{inner}</g></svg>')
        for mode in ("hell", "dunkel"):
            open(f"{out}/r{i:02d}_{mode}_brust.svg", "w").write(doc)

if __name__ == "__main__":
    build("/home/claude/designs/retro")

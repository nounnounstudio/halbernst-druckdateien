"""Zweite Generation: viele unterschiedliche Layouts, Schriften und Anlass-Farben."""
import math, re
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen
import gen
from gen import umbruch, LAYOUTS as ALT

FD = '/home/claude/fonts/'
for k, f in {'alfa': 'AlfaSlabOne-Regular.ttf', 'abril': 'AbrilFatface-Regular.ttf', 'marker': 'PermanentMarker-Regular.ttf',
             'script': 'Pacifico-Regular.ttf', 'mono': 'SpaceMono-Bold.ttf'}.items():
    gen.FONTS[k] = TTFont(FD + f)
F = gen.FONTS
X0, W = 300, 3900
CX = X0 + W / 2

# Akzentfarben je Anlass: (auf hellen Shirts, auf dunklen Shirts)
PALETTE = {'Weihnachten': ('#C8102E', '#FFBE28'), 'Silvester': ('#B8860B', '#FFD45A'), 'Nikolaus': ('#C8102E', '#FF7A66'),
           'Valentinstag': ('#E0457B', '#FF8FB1'), 'Muttertag': ('#D9467A', '#FFB3C7'), 'Vatertag': ('#2456A6', '#8EC5FF'),
           'Jahrestag': ('#E0457B', '#FF8FB1'), 'Hochzeitstag': ('#A8793A', '#E9C98B'), 'Rente': ('#2E8B57', '#9BE3B5'),
           'Abschluss': ('#2456A6', '#8EC5FF'), 'Einzug': ('#D64026', '#FFBE28')}

def farben(anlass, var):
    a = PALETTE[anlass][0 if var == 'hell' else 1]
    return ('#141414', a, '#FAF5E9') if var == 'hell' else ('#F5F5F0', a, '#141414')

def _glyphs(fn, text):
    f = F[fn]; cmap = f.getBestCmap(); gs = f.getGlyphSet(); hm = f['hmtx']
    return [((cmap.get(ord(ch)) or cmap.get(ord('?')) or '.notdef'), hm[(cmap.get(ord(ch)) or cmap.get(ord('?')) or '.notdef')][0]) for ch in text], gs

def bounds(fn, text, size, track=0):
    """Breite (Vorschub) und senkrechte Ausdehnung (oben, unten relativ zur Grundlinie, y nach unten positiv)."""
    f = F[fn]; upm = f['head'].unitsPerEm; s = size / upm
    gl, gs = _glyphs(fn, text); bp = BoundsPen(gs); cx = 0
    for g, a in gl:
        gs[g].draw(TransformPen(bp, (1, 0, 0, 1, cx, 0))); cx += a + track * upm
    adv = (cx - track * upm) * s
    if bp.bounds is None: return adv, 0, 0
    x0, y0, x1, y1 = bp.bounds
    return adv, -y1 * s, -y0 * s

def path(fn, text, x, y, size, track=0):
    return gen.text_path(fn, text, x, y, size, track)

def P(d, c): return f'<path d="{d}" fill="{c}"/>'

def put(fn, text, size, ytop, col, align='left', x=X0, w=W, track=0):
    """Setzt Text so, dass seine sichtbare Oberkante bei ytop liegt. Gibt (svg, Unterkante) zurück."""
    adv, top, bot = bounds(fn, text, size, track)
    base = ytop - top
    xx = x if align == 'left' else (x + (w - adv) / 2 if align == 'center' else x + w - adv)
    return P(path(fn, text, xx, base, size, track), col), base + bot

def fit(fn, text, maxw, maxsize, track=0):
    adv = bounds(fn, text, 1, track)[0]
    return min(maxsize, maxw / adv)

def block(fn, text, ytop, col, maxw=W, maxsize=900, maxlines=4, align='left', x=X0, gap=0.18, upper=False, minlines=1, cols=None):
    """Bricht Text in Zeilen um (gleiche Schriftgröße), wählt die größte passende Variante."""
    t = text.upper() if upper else text
    best = None
    for n in range(minlines, maxlines + 1):
        lines = umbruch(t, n)
        size = min(fit(fn, l, maxw, maxsize) for l in lines)
        if best is None or size > best[1] * 1.08: best = (lines, size)
    lines, size = best; out = []; y = ytop
    for i, l in enumerate(lines):
        c = cols[i] if cols and i < len(cols) else col
        s, y2 = put(fn, l, size, y, c, align, x, maxw)
        out.append(s); y = y2 + size * gap
    return out, y - size * gap, size

def rect(x, y, w, h, c, rx=0): return f'<rect x="{x:.0f}" y="{y:.0f}" width="{w:.0f}" height="{h:.0f}" rx="{rx}" fill="{c}"/>'
def frame(x, y, w, h, c, sw, rx=0): return f'<rect x="{x:.0f}" y="{y:.0f}" width="{w:.0f}" height="{h:.0f}" rx="{rx}" fill="none" stroke="{c}" stroke-width="{sw}"/>'

# ---------------- neue Layouts ----------------
def L_bogen(s, c):
    tc, ac, bg = c; out = []
    top = s['top'].upper(); R = 2700; cy0 = 2900
    size = 900 if len(top) <= 8 else 720
    # Bogenlänge begrenzen
    while bounds('alfa', top, size, 0.04)[0] > R * 1.35: size -= 20
    adv = bounds('alfa', top, size, 0.04)[0]; ang = adv / R
    f = F['alfa']; upm = f['head'].unitsPerEm; sc = size / upm
    gl, gs = _glyphs('alfa', top); a = -ang / 2; parts = []
    for ch in top:
        w_ = bounds('alfa', ch, size)[0]
        mid = a + (w_ / 2) / R
        px = CX + R * math.sin(mid); py = cy0 - R * math.cos(mid)
        d = path('alfa', ch, -w_ / 2, 0, size)
        parts.append(f'<path transform="translate({px:.1f},{py:.1f}) rotate({math.degrees(mid):.2f})" d="{d}" fill="{ac}"/>')
        a += (w_ + 0.04 * size) / R
    out += parts
    ytop = cy0 - R + 80 + 120
    y = cy0 - R * math.cos(ang / 2) + 120
    o, y, _ = block('alfa', s['bottom'], y + 60, tc, maxsize=700, maxlines=3, align='center', upper=True)
    out += o
    out.append(rect(CX - 700, y + 140, 1400, 40, ac)); y += 180
    # vom Bogen oben (Oberkante ≈ cy0-R-size) nach unten verschieben
    shift = -(cy0 - R - size * 0.8) + 40
    return [f'<g transform="translate(0,{shift:.0f})">' + ''.join(out) + '</g>'], y + shift

def L_bon(s, c):
    tc, ac, bg = c; out = []; x = X0 + 450; w = W - 900
    y = 40
    o, y = put('mono', s.get('kopf', 'KASSENBON').upper(), fit('mono', s.get('kopf', 'KASSENBON').upper(), w, 260, 0.15), y, tc, 'center', x, w, 0.15); out.append(o)
    def dash(y): return ''.join(rect(x + i * 160, y, 100, 22, tc) for i in range(int(w / 160) + 1) if x + i * 160 + 100 <= x + w)
    y += 120; out.append(dash(y)); y += 140
    for z in s['zeilen']:
        o, y2, sz = block('mono', z, y, tc, maxw=w, maxsize=300, maxlines=3, x=x); out += o; y = y2 + 90
    y += 30; out.append(dash(y)); y += 140
    o, y, _ = block('anton', s['summe'], y, ac, maxw=w, maxsize=650, maxlines=3, align='center', upper=True, x=x); out += o
    y += 140; out.append(dash(y)); y += 120
    import random; rnd = random.Random(s['id']); bx = x + 300
    while bx < x + w - 300:
        bw_ = rnd.choice([18, 30, 45, 70]); out.append(rect(bx, y, bw_, 330, tc)); bx += bw_ + rnd.choice([20, 35, 50])
    y += 330
    out.insert(0, frame(x - 120, -60, w + 240, y + 200, tc, 22, 0))
    return out, y + 140

def L_marker(s, c):
    tc, ac, bg = c; out = []
    o, y, size = block('marker', s['main'], 60, tc, maxsize=900, maxlines=4, gap=0.05)
    out += o
    sw = f'<path d="M{X0+40} {y+120:.0f} Q {CX:.0f} {y+20:.0f} {X0+W-200} {y+150:.0f}" fill="none" stroke="{ac}" stroke-width="90" stroke-linecap="round"/>'
    out.append(sw); y += 330
    if s.get('sub'):
        o, y, _ = block('marker', s['sub'], y, ac, maxsize=size * 0.7, maxlines=2); out += o
    return [f'<g transform="rotate(-4 {CX} 1500) translate(0,150)">' + ''.join(out) + '</g>'], y + 300

def deko(y, ac, kind='stern'):
    out = []
    for i, dx in enumerate((-260, 0, 260)):
        r = 140 if i != 1 else 200; cx = CX + dx * 1.6; cy = y + 200
        if kind == 'herz':
            out.append(f'<path transform="translate({cx},{cy}) scale({r/50})" d="M0 18 C-30 -10 -55 10 -45 30 C-35 50 0 70 0 80 C0 70 35 50 45 30 C55 10 30 -10 0 18Z" fill="{ac}"/>')
        else:
            pts = ' '.join(f'{cx + (r if k % 2 == 0 else r*0.42) * math.sin(k*math.pi/5):.0f},{cy - (r if k % 2 == 0 else r*0.42) * math.cos(k*math.pi/5):.0f}' for k in range(10))
            out.append(f'<polygon points="{pts}" fill="{ac}"/>')
    return out, y + 420

def L_serif(s, c):
    tc, ac, bg = c; out, y = deko(20, ac, s.get('deko', 'stern'))
    o, y, size = block('abril', s['main'], y + 80, tc, maxsize=820, maxlines=4, align='center', gap=0.12); out += o
    if s.get('sub'):
        out.append(rect(CX - 600, y + 120, 1200, 30, ac)); y += 280
        o, y, _ = block('abril', s['sub'], y, ac, maxsize=size * 0.6, maxlines=2, align='center'); out += o
    return out, y

def L_script(s, c):
    tc, ac, bg = c; out = []
    o, y, size = block('script', s['scr'], 60, ac, maxsize=1000, maxlines=2, gap=0.0, align='center'); out += o
    o, y, _ = block('anton', s['block'], y + 40, tc, maxsize=950, maxlines=3, align='center', upper=True, gap=0.12); out += o
    return out, y

def L_lade(s, c):
    tc, ac, bg = c; out = []
    o, y, _ = block('anton', s['label'], 40, tc, maxsize=760, maxlines=2, upper=True); out += o
    y += 160; h = 480; pct = s['pct']
    out.append(frame(X0 + 30, y, W - 60, h, tc, 60, 60))
    inner = (W - 60 - 180) * pct / 100
    if inner > 0: out.append(rect(X0 + 120, y + 90, max(inner, 60), h - 180, ac, 30))
    y += h + 90
    t = s.get('pt', f'{pct} %')
    o, y2 = put('mono', t, 260, y, tc, 'right'); out.append(o)
    o, _ = put('mono', s.get('status', 'LÄDT …'), 200, y + 40, tc, 'left'); out.append(o)
    y = y2 + 200
    if s.get('cap'):
        o, y, _ = block('anton', s['cap'], y, ac, maxsize=700, maxlines=2, upper=True); out += o
    return out, y

def checkmark(x, y, b, c): return f'<path d="M{x+b*0.18:.0f} {y+b*0.52:.0f} L{x+b*0.42:.0f} {y+b*0.78:.0f} L{x+b*0.92:.0f} {y+b*0.08:.0f}" fill="none" stroke="{c}" stroke-width="{b*0.17:.0f}" stroke-linecap="round" stroke-linejoin="round"/>'
def L_check(s, c):
    tc, ac, bg = c; out = []; y = 40
    if s.get('titel'):
        o, y, _ = block('anton', s['titel'], y, tc, maxsize=820, maxlines=2, upper=True); out += o; y += 220
    b = 520
    for t, ok in s['items']:
        out.append(frame(X0 + 30, y, b, b, tc, 55, 40))
        if ok: out.append(checkmark(X0 + 30, y - 60, b + 40, ac))
        size = fit('archivo', t, W - b - 250, 470)
        cap = -bounds('archivo', 'H', size)[1]
        o, _ = put('archivo', t, size, y + (b - cap) / 2, tc, 'left', X0 + b + 200, W - b - 200)
        out.append(o); y += b + 150
    if s.get('cap'):
        y += 40; o, y, _ = block('marker', s['cap'], y, ac, maxsize=760, maxlines=2); out += o
    return out, y

def L_blase(s, c):
    tc, ac, bg = c; out = []; y = 40
    if s.get('pre'):
        o, y, _ = block('archivo', s['pre'], y, tc, maxsize=360, maxlines=2, align='center'); out += o; y += 120
    bx, bw_ = X0 + 120, W - 240; pad = 220
    o, yy, size = block('archivo', s['bubble'], y + pad, tc, maxw=bw_ - 2 * pad, maxsize=520, maxlines=4, align='center', x=bx + pad)
    bh = yy - y + pad
    out.append(f'<path d="M{bx+700} {y+bh-40:.0f} L{bx+620} {y+bh+380:.0f} L{bx+1150} {y+bh-40:.0f}Z" fill="{ac}"/>')
    out.append(rect(bx, y, bw_, bh, ac, 160))
    out.append(rect(bx + 50, y + 50, bw_ - 100, bh - 100, bg, 120))
    out.append(f'<path d="M{bx+745} {y+bh-60:.0f} L{bx+680} {y+bh+250:.0f} L{bx+1060} {y+bh-60:.0f}Z" fill="{bg}"/>')
    out += o; y = y + bh + 480
    if s.get('post'):
        o, y, _ = block('anton', s['post'], y, ac, maxsize=900, maxlines=2, upper=True, align='center'); out += o
    return out, y

def L_warn(s, c):
    tc, ac, bg = c; out = []
    h = 1350; w2 = h * 1.15 / 2; y0 = 60
    out.append(f'<path d="M{CX} {y0} L{CX+w2:.0f} {y0+h} L{CX-w2:.0f} {y0+h}Z" fill="{ac}" stroke="{ac}" stroke-width="120" stroke-linejoin="round"/>')
    out.append(rect(CX - 70, y0 + 380, 140, 560, bg, 50)); out.append(f'<circle cx="{CX}" cy="{y0+1120}" r="85" fill="{bg}"/>')
    y = y0 + h + 220
    o, y = put('archivo', s.get('kopf', 'ACHTUNG'), 300, y, ac, 'center', track=0.3); out.append(o); y += 200
    o, y, _ = block('anton', s['text'], y, tc, maxsize=760, maxlines=4, upper=True, align='center'); out += o
    return out, y

ICONS = {
 'baum': lambda a, t: f'<path d="M0 -600 L380 -80 L180 -80 L480 340 L-480 340 L-180 -80 L-380 -80Z" fill="{a}"/><rect x="-90" y="340" width="180" height="200" fill="{t}"/><polygon points="0,-760 45,-650 160,-650 68,-585 102,-475 0,-540 -102,-475 -68,-585 -160,-650 -45,-650" fill="{t}"/>',
 'stern': lambda a, t: '<polygon points="' + ' '.join(f'{(520 if k%2==0 else 210)*math.sin(k*math.pi/5):.0f},{-(520 if k%2==0 else 210)*math.cos(k*math.pi/5):.0f}' for k in range(10)) + f'" fill="{a}"/><circle cx="-430" cy="-360" r="55" fill="{t}"/><circle cx="470" cy="300" r="45" fill="{t}"/>',
 'stiefel': lambda a, t: f'<path d="M-260 -560 L180 -560 L180 140 L470 260 Q560 300 540 420 L540 520 L-260 520Z" fill="{a}"/><rect x="-300" y="-640" width="520" height="160" rx="40" fill="{t}"/>',
 'herz': lambda a, t: f'<path transform="scale(11)" d="M0 -18 C-30 -50 -60 -25 -50 5 C-42 28 0 50 0 50 C0 50 42 28 50 5 C60 -25 30 -50 0 -18Z" fill="{a}"/>',
 'herzen': lambda a, t: f'<path transform="translate(-240,40) scale(8)" d="M0 -18 C-30 -50 -60 -25 -50 5 C-42 28 0 50 0 50 C0 50 42 28 50 5 C60 -25 30 -50 0 -18Z" fill="{a}"/><path transform="translate(260,-40) scale(8)" d="M0 -18 C-30 -50 -60 -25 -50 5 C-42 28 0 50 0 50 C0 50 42 28 50 5 C60 -25 30 -50 0 -18Z" fill="none" stroke="{t}" stroke-width="9"/>',
 'werkzeug': lambda a, t: f'<g transform="rotate(-40)"><rect x="-70" y="-300" width="140" height="760" rx="60" fill="{a}"/><path d="M-230 -420 a230 230 0 1 0 460 0 l-120 0 l0 140 l-220 0 l0 -140Z" fill="{a}"/></g>',
 'ringe': lambda a, t: f'<circle cx="-200" cy="60" r="330" fill="none" stroke="{a}" stroke-width="110"/><circle cx="200" cy="60" r="330" fill="none" stroke="{t}" stroke-width="110"/><path d="M-200 -380 l90 -120 l-90 -60 l-90 60Z" fill="{a}"/>',
 'wecker': lambda a, t: f'<circle cx="0" cy="40" r="430" fill="none" stroke="{t}" stroke-width="100"/><circle cx="-330" cy="-370" r="140" fill="{t}"/><circle cx="330" cy="-370" r="140" fill="{t}"/><path d="M0 40 L0 -220 M0 40 L170 140" stroke="{t}" stroke-width="80" stroke-linecap="round"/><path d="M-560 -480 L560 560" stroke="{a}" stroke-width="130" stroke-linecap="round"/>',
 'hut': lambda a, t: f'<path d="M0 -420 L640 -140 L0 140 L-640 -140Z" fill="{a}"/><path d="M-360 0 L-360 300 Q0 460 360 300 L360 0 L0 150Z" fill="{t}"/><path d="M520 -190 L520 260" stroke="{a}" stroke-width="45"/><circle cx="520" cy="300" r="75" fill="{a}"/>',
 'haus': lambda a, t: f'<path d="M0 -560 L560 -60 L420 -60 L420 520 L-420 520 L-420 -60 L-560 -60Z" fill="{a}"/><rect x="-110" y="200" width="220" height="320" fill="{t}"/><rect x="190" y="40" width="150" height="150" fill="{t}"/><rect x="-340" y="40" width="150" height="150" fill="{t}"/>',
 'tasse': lambda a, t: f'<path d="M-380 -180 L320 -180 L280 460 L-340 460Z" fill="{a}"/><path d="M320 -60 Q560 -60 520 150 Q490 300 290 300" fill="none" stroke="{a}" stroke-width="80"/><path d="M-180 -320 q-70 -110 0 -220 M0 -320 q-70 -110 0 -220 M180 -320 q-70 -110 0 -220" fill="none" stroke="{t}" stroke-width="50" stroke-linecap="round"/>',
 'medaille': lambda a, t: f'<path d="M-260 -620 L-60 -100 L60 -100 L260 -620 L120 -620 L0 -330 L-120 -620Z" fill="{t}"/><circle cx="0" cy="160" r="380" fill="{a}"/><polygon points="' + ' '.join(f'{(200 if k%2==0 else 85)*math.sin(k*math.pi/5):.0f},{160-(200 if k%2==0 else 85)*math.cos(k*math.pi/5):.0f}' for k in range(10)) + f'" fill="{t}"/>',
}
def L_icon(s, c):
    tc, ac, bg = c; out = []
    out.append(f'<g transform="translate({CX},{900}) scale(1.45)">' + ICONS[s['icon']](ac, tc) + '</g>')
    y = 1950
    o, y, size = block('alfa', s['main'], y, tc, maxsize=700, maxlines=3, align='center', upper=True, gap=0.15); out += o
    if s.get('sub'):
        y += 160; o, y, _ = block('archivo', s['sub'], y, ac, maxsize=380, maxlines=2, align='center'); out += o
    return out, y

def L_torte(s, c):
    tc, ac, bg = c; out = []; y = 40
    if s.get('titel'):
        o, y, _ = block('anton', s['titel'], y, tc, maxsize=720, maxlines=2, upper=True); out += o; y += 220
    r = 1000; cx, cy = X0 + r + 40, y + r
    cols = [ac, tc, bg]; a0 = -math.pi / 2; lx = cx + r + 300; ly = y + 250
    for i, (lab, pct) in enumerate(s['stuecke']):
        a1 = a0 + 2 * math.pi * pct / 100; large = 1 if a1 - a0 > math.pi else 0
        col = cols[i % 2]
        out.append(f'<path d="M{cx} {cy} L{cx + r*math.cos(a0):.0f} {cy + r*math.sin(a0):.0f} A{r} {r} 0 {large} 1 {cx + r*math.cos(a1):.0f} {cy + r*math.sin(a1):.0f}Z" fill="{col}" stroke="{bg}" stroke-width="40"/>')
        out.append(rect(lx, ly, 200, 200, col, 30))
        o, _ = put('archivo', f'{pct} %', 330, ly - 10, tc, 'left', lx + 260, 1100); out.append(o)
        sz = fit('archivo', lab, W - (lx - X0) - 260, 300)
        o, _ = put('archivo', lab, sz, ly + 400, ac if i % 2 == 0 else tc, 'left', lx + 260, W - (lx - X0) - 260); out.append(o)
        ly += 700; a0 = a1
    y = cy + r + 220
    if s.get('cap'):
        o, y, _ = block('anton', s['cap'], y, ac, maxsize=620, maxlines=2, upper=True); out += o
    return out, y

def L_gesucht(s, c):
    tc, ac, bg = c; out = []; x = X0 + 250; w = W - 500; y = 260
    o, y = put('alfa', 'GESUCHT', fit('alfa', 'GESUCHT', w - 300, 900, 0.05), y, ac, 'center', x, w, 0.05); out.append(o)
    y += 150; out.append(rect(x + 200, y, w - 400, 30, tc)); y += 180
    o, y, _ = block('abril', s['main'], y, tc, maxw=w - 400, maxsize=700, maxlines=2, align='center', x=x + 200); out += o
    y += 160; o, y, _ = block('archivo', s['sub'], y, tc, maxw=w - 400, maxsize=300, maxlines=2, align='center', x=x + 200); out += o
    y += 240
    out.insert(0, frame(x, 40, w, y - 40, tc, 50, 0)); out.insert(1, frame(x + 80, 120, w - 160, y - 200, tc, 15, 0))
    return out, y

NEU = {'bogen': L_bogen, 'bon': L_bon, 'marker': L_marker, 'serif': L_serif, 'script': L_script, 'lade': L_lade,
       'check': L_check, 'blase': L_blase, 'warn': L_warn, 'icon': L_icon, 'torte': L_torte, 'gesucht': L_gesucht}

def svg(spec, anlass, var):
    c = farben(anlass, var)
    lay = spec['layout']
    if lay in NEU: parts, h = NEU[lay](spec, c); top = 120 if lay == 'bon' else 0
    else:
        parts, h = ALT[lay](spec.get('main', ''), spec.get('sub', ''), c, spec.get('label', ''))
        top = 0 if lay in ('stempel', 'schild') else 230
    return ('<svg xmlns="http://www.w3.org/2000/svg" width="4500" height="5400" viewBox="0 0 4500 5400">'
            + f'<g transform="translate(0,{top})">' + ''.join(parts) + '</g></svg>'), h + top

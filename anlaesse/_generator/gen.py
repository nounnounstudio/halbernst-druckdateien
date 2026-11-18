"""Druckdateien für die Anlass-Sprüche im Halbernst-Stil (Anton + Archivo Black, als Pfade).
Leinwand 4500x5400, Motiv in x 300..4200, oben bündig (Brusthöhe)."""
import json, math, re, sys
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen

FD = '/home/claude/fonts/'
FONTS = {'anton': TTFont(FD + 'Anton-Regular.ttf'), 'archivo': TTFont(FD + 'ArchivoBlack-Regular.ttf')}
FARBEN = {'hell': ('#141414', '#D64026', '#FAF5E9'), 'dunkel': ('#F5F5F0', '#FFBE28', '#141414')}
X0, W = 300, 3900

def glyphs(font, text):
    cmap = font.getBestCmap(); gs = font.getGlyphSet(); hm = font['hmtx']
    out = []
    for ch in text:
        g = cmap.get(ord(ch)) or cmap.get(ord('?'))
        out.append((g, hm[g][0]))
    return out, gs

def text_metrics(fn, text, track=0):
    f = FONTS[fn]; upm = f['head'].unitsPerEm
    gl, gs = glyphs(f, text)
    adv = sum(a for _, a in gl) + track * upm * max(len(gl) - 1, 0)
    cap = f['OS/2'].sCapHeight or upm * 0.7
    return adv / upm, cap / upm

def text_path(fn, text, x, y, size, track=0):
    """y = Grundlinie. Gibt SVG-Pfad-d zurück."""
    f = FONTS[fn]; upm = f['head'].unitsPerEm; s = size / upm
    gl, gs = glyphs(f, text)
    pen = SVGPathPen(gs); cx = 0
    for g, a in gl:
        tp = TransformPen(pen, (s, 0, 0, -s, x + cx * s, y))
        gs[g].draw(tp)
        cx += a + track * upm
    return pen.getCommands()

def width_of(fn, text, size, track=0):
    return text_metrics(fn, text, track)[0] * size

def cap_of(fn, size):
    return text_metrics(fn, 'H')[1] * size

def umbruch(text, n):
    """Teilt Text in n möglichst gleich lange Zeilen (nach Wörtern)."""
    w = text.split()
    if n <= 1 or len(w) <= 1: return [text]
    best = None
    def rec(start, k):
        if k == 1: return [[' '.join(w[start:])]]
        res = []
        for i in range(start + 1, len(w) - k + 2):
            for rest in rec(i, k - 1): res.append([' '.join(w[start:i])] + rest)
        return res
    for cand in rec(0, min(n, len(w))):
        m = max(len(c) for c in cand)
        if best is None or m < best[0]: best = (m, cand)
    return best[1]

def block_lines(text, fn='anton', maxw=W, maxh=2600, lead=1.08, maxsize=1100):
    """Wählt Zeilenzahl und Schriftgröße so, dass der Block groß und ausgewogen wirkt."""
    best = None
    for n in range(1, 6):
        lines = umbruch(text, n)
        widest = max(width_of(fn, l, 1) for l in lines)
        size = min(maxw / widest, maxsize)
        cap = cap_of(fn, size)
        h = cap * len(lines) + (len(lines) - 1) * cap * (lead - 1 + 0.25)
        if h > maxh: size *= maxh / h
        score = size * (1 if n > 1 or len(text) < 14 else 0.85)
        if best is None or score > best[0] + 1: best = (score, lines, size)
    return best[1], best[2]

def P(d, fill): return f'<path d="{d}" fill="{fill}"/>'

def lay_gross(main, sub, c, label):
    tc, ac, bg = c; out = []; y = 0
    lines, size = block_lines(main.upper(), maxh=2900)
    cap = cap_of("anton", size); gap = cap * 0.3
    for i, l in enumerate(lines):
        y += cap
        col = ac if (i == len(lines) - 1 and len(lines) > 1) else tc
        out.append(P(text_path('anton', l, X0, y, size), col)); y += gap
    if sub:
        sl, ss = block_lines(sub.upper(), maxh=900, maxsize=min(720, size * 0.62))
        y += cap * 0.15; sc = cap_of('anton', ss)
        for l in sl:
            y += sc; out.append(P(text_path('anton', l, X0, y, ss), ac if len(lines) == 1 else tc)); y += sc * 0.22
    return out, y

def lay_streifen(main, sub, c, label):
    tc, ac, bg = c; out = []; y = 0
    txt = (main + (' ' + sub if sub else '')).upper()
    n = 3 if len(txt.split()) >= 3 else len(txt.split())
    lines = umbruch(txt, min(4, max(n, round(len(txt) / 11))))
    x = X0 + 230; mw = W - 230
    for i, l in enumerate(lines):
        size = min(mw / width_of('anton', l, 1), 1300)
        cap = cap_of('anton', size); y += cap
        out.append(P(text_path('anton', l, x, y, size), ac if i == len(lines) - 1 and len(lines) > 2 else tc)); y += 110
    out.insert(0, f'<rect x="{X0}" y="20" width="90" height="{y - 130}" fill="{ac}"/>')
    return out, y

def spaced(text, size, x, y, col, maxw=W, center=False, track=0.18):
    w = width_of('archivo', text, size, track)
    if w > maxw: size *= maxw / w; w = maxw
    xx = x + (maxw - w) / 2 if center else x
    return P(text_path('archivo', text, xx, y, size, track), col), size

def lay_sperr(main, sub, c, label):
    tc, ac, bg = c; out = []; y = 0
    lines, size = block_lines(main.upper(), maxh=2400)
    cap = cap_of('anton', size)
    for l in lines:
        y += cap; out.append(P(text_path("anton", l, X0 + (W - width_of("anton", l, size)) / 2, y, size), tc)); y += cap * 0.3
    y += 120; out.append(f'<rect x="{X0}" y="{y:.0f}" width="{W}" height="34" fill="{ac}"/>'); y += 150
    st = (sub or label).upper()
    if len(st) > 20:
        sl, ss = block_lines(st, maxh=650, maxsize=420); y += 40
        for l in sl:
            sc = cap_of('anton', ss); y += sc; out.append(P(text_path('anton', l, X0 + (W - width_of('anton', l, ss)) / 2, y, ss), ac)); y += sc * 0.25
        y += 100
    else:
        p, s2 = spaced(st, 230, X0, y + 170, ac, center=True); out.append(p); y += 170 + 130
    out.append(f'<rect x="{X0}" y="{y:.0f}" width="{W}" height="34" fill="{ac}"/>'); y += 34
    return out, y

def lay_schild(main, sub, c, label):
    tc, ac, bg = c; out = []
    bx, bw = X0 + 150, W - 300; pad = 230; y = 60
    head = 420
    inner = []
    yy = y + head + 260
    lines, size = block_lines(main.upper(), maxw=bw - 2 * pad, maxh=2000, maxsize=900)
    cap = cap_of('anton', size)
    for l in lines:
        yy += cap; inner.append(P(text_path('anton', l, bx + (bw - width_of('anton', l, size)) / 2, yy, size), tc)); yy += cap * 0.22
    if sub:
        sl, ss = block_lines(sub.upper(), maxw=bw - 2 * pad, maxh=700, maxsize=380)
        yy += 60
        for l in sl:
            sc = cap_of('anton', ss); yy += sc; inner.append(P(text_path('anton', l, bx + (bw - width_of('anton', l, ss)) / 2, yy, ss), ac)); yy += sc * 0.25
    yy += 200
    out.append(f'<rect x="{bx}" y="{y}" width="{bw}" height="{yy - y:.0f}" rx="60" fill="none" stroke="{tc}" stroke-width="70"/>')
    out.append(f'<rect x="{bx}" y="{y}" width="{bw}" height="{head}" fill="{ac}"/>')
    p, _ = spaced(label.upper(), 190, bx + 120, y + head / 2 + 70, bg, maxw=bw - 240, center=True, track=0.25); out.append(p)
    return out + inner, yy

def lay_stempel(main, sub, c, label):
    tc, ac, bg = c; out = []
    cx, cy, r = X0 + W / 2, 1950, 1850
    g = []
    g.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{ac}" stroke-width="80"/>')
    g.append(f'<circle cx="{cx}" cy="{cy}" r="{r - 150}" fill="none" stroke="{ac}" stroke-width="25"/>')
    lines, size = block_lines(main.upper(), maxw=2500, maxh=1700, maxsize=800)
    cap = cap_of('anton', size); tot = len(lines) * cap + (len(lines) - 1) * cap * 0.22
    y = cy - tot / 2 - (330 if sub else 150)
    for l in lines:
        y += cap; g.append(P(text_path('anton', l, cx - width_of('anton', l, size) / 2, y, size), ac)); y += cap * 0.22
    y += 80; g.append(f'<rect x="{cx - 500}" y="{y:.0f}" width="1000" height="30" fill="{tc}"/>'); y += 170
    if sub:
        sl, ss = block_lines(sub.upper(), maxw=2100, maxh=600, maxsize=size * 0.72)
        for l in sl:
            sc = cap_of('anton', ss); y += sc; g.append(P(text_path('anton', l, cx - width_of('anton', l, ss) / 2, y, ss), tc)); y += sc * 0.25
    else:
        p, s2 = spaced(label.upper(), 170, cx - 1150, y + 170, tc, maxw=2300, center=True, track=0.15); g.append(p)
    out.append(f'<g transform="rotate(-8 {cx} {cy})">' + ''.join(g) + '</g>')
    return out, cy + r + 60

def lay_zitat(main, sub, c, label):
    tc, ac, bg = c; out = []
    m = re.match(r'^„(.+?)“\s*[–-]\s*(.+)$', main + (' ' + sub if sub else ''))
    q, who = (m.group(1), m.group(2)) if m else (main, sub or label)
    qs = 900; out.append(P(text_path('anton', '„', X0, 700, qs * 1.6), ac))
    y = 900
    lines, size = block_lines(q.upper(), maxh=2200)
    cap = cap_of('anton', size)
    for l in lines:
        y += cap; out.append(P(text_path('anton', l, X0, y, size), tc)); y += cap * 0.22
    y += 120
    t = '– ' + who.upper(); w = width_of('archivo', t, 240, 0.1)
    if w > W: w = W
    out.append(P(text_path('archivo', t, X0 + W - w, y + 200, 240 * min(1, W / max(w, 1)), 0.1), ac))
    return out, y + 260

def lay_woerterbuch(main, sub, c, label):
    tc, ac, bg = c; out = []
    wort = main
    size = min(W / width_of('anton', wort, 1), 1000); cap = cap_of('anton', size)
    y = cap * 1.25; out.append(P(text_path('anton', wort, X0, y, size), tc))
    y += 230; p, _ = spaced(label.upper(), 210, X0, y, ac, maxw=W * 0.8); out.append(p)
    y += 130; out.append(f'<rect x="{X0}" y="{y}" width="{W}" height="25" fill="{tc}"/>'); y += 120
    sl = umbruch(sub, 3 if len(sub) > 48 else 2 if len(sub) > 16 else 1)
    ss = min(min(W / width_of('archivo', l, 1) for l in sl), 430)
    for l in sl:
        y += cap_of('archivo', ss); out.append(P(text_path('archivo', l, X0, y, ss), tc)); y += cap_of('archivo', ss) * 0.5
    return out, y

LAYOUTS = {'gross': lay_gross, 'streifen': lay_streifen, 'sperr': lay_sperr, 'schild': lay_schild,
           'stempel': lay_stempel, 'zitat': lay_zitat, 'woerterbuch': lay_woerterbuch}

def svg(layout, main, sub, label, variante):
    c = FARBEN[variante]
    parts, h = LAYOUTS[layout](main, sub, c, label)
    top = 0 if layout in ('stempel', 'schild') else 230
    return ('<svg xmlns="http://www.w3.org/2000/svg" width="4500" height="5400" viewBox="0 0 4500 5400">'
            + f'<g transform="translate(0,{top})">' + ''.join(parts) + '</g></svg>'), h + top

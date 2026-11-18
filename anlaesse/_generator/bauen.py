import json, re, os, sys
sys.path.insert(0, '/home/claude/anlaesse')
from gen import svg

D = json.load(open('/home/claude/anlaesse/sprueche.json'))
LABEL = {'Weihnachten': 'Weihnachtshinweis', 'Silvester': 'Neujahrsvorsatz', 'Nikolaus': 'Nikolaus-Protokoll',
         'Valentinstag': 'Liebeserklärung', 'Muttertag': 'Mama-Regel', 'Vatertag': 'Papa-Fakt',
         'Jahrestag': 'Beziehungsstatus', 'Hochzeitstag': 'Ehe-Status', 'Rente': 'Ruhestand',
         'Abschluss': 'Zeugnis', 'Einzug': 'Neue Adresse'}
KURZ = {'Weihnachten': 'WEI', 'Silvester': 'SIL', 'Nikolaus': 'NIK', 'Valentinstag': 'VAL', 'Muttertag': 'MUT',
        'Vatertag': 'VAT', 'Jahrestag': 'JAH', 'Hochzeitstag': 'HOC', 'Rente': 'REN', 'Abschluss': 'ABS', 'Einzug': 'EIN'}
ROT = ['gross', 'streifen', 'sperr', 'schild', 'stempel', 'gross', 'sperr', 'schild', 'streifen', 'stempel']
WOERTERBUCH = {'Weihnachtsmodus: Couch, Kekse, kein Plan.': ('Weihnachtsmodus, der', 'Couch, Kekse, kein Plan.'),
               'Ruhestand? Ich hatte noch nie so viel vor.': ('Ruhestand, der', 'Ich hatte noch nie so viel vor.'),
               'Raclette ist eine Lebenseinstellung.': ('Raclette, das', 'Keine Mahlzeit. Eine Lebenseinstellung.'),
               'Hauptberuflich Hobby.': ('Rentner, der', 'Hauptberuflich Hobby.')}

def teilen(s):
    m = re.match(r'^(.+?[.?!:])\s+(.+)$', s)
    if m and len(m.group(1)) > 3: return m.group(1).rstrip('.:'), m.group(2)
    m = re.match(r'^(.+?)\s+–\s+(.+)$', s)
    if m: return m.group(1), m.group(2)
    return s.rstrip('.'), ''

def plan():
    out = []
    for anl, liste in D.items():
        for i, s in enumerate(liste):
            pid = f'{KURZ[anl]}{i+1:02d}'
            if s in WOERTERBUCH:
                lay = 'woerterbuch'; main, sub = WOERTERBUCH[s]; lab = 'Substantiv, halbernst'
            elif s.startswith('„Wo ist Papa'):
                lay = 'gross'; main, sub = '„Wo ist Papa?“', '„Am Grill.“'; lab = LABEL[anl]
            elif s.startswith('„'):
                lay = 'zitat'; main, sub = s, ''; lab = LABEL[anl]
            else:
                lay = ROT[i]; main, sub = teilen(s); lab = LABEL[anl]
                if lay == 'stempel' and len(main) > 26: lay = 'gross'
                if lay == 'sperr' and not sub and len(main) < 12: lay = 'stempel'
                if lay == 'streifen': main, sub = s.rstrip('.'), ''
            out.append(dict(id=pid, anlass=anl, spruch=s, layout=lay, main=main, sub=sub, label=lab))
    return out

if __name__ == '__main__':
    P = plan(); od = '/home/claude/anlaesse/svg'; os.makedirs(od, exist_ok=True)
    for p in P:
        for v in ('hell', 'dunkel'):
            s, h = svg(p['layout'], p['main'], p['sub'], p['label'], v)
            open(f"{od}/{p['id']}_{v}_brust.svg", 'w').write(s)
            if h > 4300: print('ZU HOCH', p['id'], round(h))
    json.dump(P, open('/home/claude/anlaesse/plan.json', 'w'), ensure_ascii=False, indent=1)
    from collections import Counter; print(len(P), Counter(p['layout'] for p in P))

import os, sys, json
sys.path.insert(0, '/home/claude/anlaesse')
from gen2 import svg
M = {
'MER01': dict(layout='logo', sub='HUMOR ZUM ANZIEHEN', ptitel='HALBERNST'),
'MER02': dict(layout='serif', main='Halb ernst.', sub='Ganz ehrlich.', deko='stern', ptitel='Halb ernst. Ganz ehrlich.'),
'MER03': dict(layout='marker', main='Ich nehm das nur halb ernst.', ptitel='Ich nehm das nur halb ernst.'),
'MER04': dict(layout='woerterbuch', main='halbernst, Adj.', sub='Lustig gemeint, ernst getragen.', label='Adjektiv, siehe Shirt', ptitel='halbernst, Adj. – lustig gemeint, ernst getragen'),
'MER05': dict(layout='lade', label='Ernsthaftigkeit', pct=50, status='', cap='Halbernst.', ptitel='Ernsthaftigkeit: 50 %'),
'MER06': dict(layout='stempel', main='Halbernst geprüft', sub='', label='halbernst.de', ptitel='Halbernst geprüft'),
'MER07': dict(layout='bogen', top='Halbernst', bottom='Crew', ptitel='Halbernst Crew'),
'MER08': dict(layout='qr', main='Scan mich.', sub='Wird lustig.', url='https://halbernst.de/?utm_source=shirt-qr', ptitel='Scan mich. Wird lustig.'),
'MER09': dict(layout='blase', bubble='Ich vergesse keine Geburtstage mehr.', post='Ich hab eine App.', ptitel='Ich vergesse keine Geburtstage mehr. Ich hab eine App.'),
'MER10': dict(layout='check', items=[('Glückwunsch', True), ('Geschenk', True), ('Selbst dran gedacht', False)], ptitel='Glückwunsch, Geschenk, selbst dran gedacht'),
}
if __name__ == '__main__':
    od = '/home/claude/anlaesse/merch'; os.makedirs(od, exist_ok=True)
    for pid, s in M.items():
        s['id'] = pid
        for v in ('hell', 'dunkel'):
            x, h = svg(s, 'Merch', v); open(f'{od}/{pid}_{v}_brust.svg', 'w').write(x)
    json.dump([[s['ptitel'] + ' – Halbernst Merch T-Shirt', pid] for pid, s in M.items()], open('/home/claude/anlaesse/merch_upload.json', 'w'), ensure_ascii=False)

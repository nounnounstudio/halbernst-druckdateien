import json, os, sys
sys.path.insert(0, '/home/claude/anlaesse')
from gen2 import svg

S = {
# Weihnachten
'WEI01': dict(layout='marker', main='Plätzchen zählen nicht.', sub='Ist ja Weihnachten.'),
'WEI02': dict(layout='blase', bubble='Ich bin nur wegen des Essens hier.'),
'WEI03': dict(layout='lade', label='Weihnachtsmodus', pct=99, cap='Couch, Kekse, kein Plan.'),
'WEI04': dict(layout='serif', main='Oh du fröhliche Verdauung.', deko='stern'),
'WEI05': dict(layout='icon', icon='baum', main='Lichterkette entwirrt.', sub='Nerven auch.'),
'WEI06': dict(layout='bogen', top='Most likely', bottom='to eat all the cookies'),
'WEI07': dict(layout='check', items=[('Geschenke eingepackt?', False), ('Klebeband gefunden?', False)], cap='Nein. Auch nicht.'),
'WEI08': dict(layout='schild', main='Ich bin der Grund, warum es eine Liste gibt.', sub='', label='Weihnachtshinweis'),
'WEI09': dict(layout='script', scr='Merry', block='& müde'),
'WEI10': dict(layout='stempel', main='Familienfest überlebt', sub='Nächstes Jahr wieder.', label=''),
# Silvester
'SIL01': dict(layout='gross', main='Neues Jahr, gleicher Quatsch', sub=''),
'SIL02': dict(layout='check', titel='Meine Vorsätze:', items=[('dieselben wie letztes Jahr', True)]),
'SIL03': dict(layout='marker', main='Um 0:01 Uhr schon gescheitert.'),
'SIL04': dict(layout='bogen', top='New year,', bottom='same chaos'),
'SIL05': dict(layout='script', scr='Ich rutsche.', block='Aber gut.'),
'SIL06': dict(layout='blase', bubble='Dieses Jahr wird alles anders.', post='Sagte ich letztes Jahr auch.'),
'SIL07': dict(layout='woerterbuch', main='Raclette, das', sub='Keine Mahlzeit. Eine Lebenseinstellung.', label='Substantiv, halbernst'),
'SIL08': dict(layout='lade', label='Countdown läuft.', pct=3, pt='Motivation: 3 %', status='', cap='Motivation nicht.'),
'SIL09': dict(layout='serif', main='Neujahr feiere ich um 22 Uhr.', sub='Im Schlafanzug.', deko='stern'),
'SIL10': dict(layout='icon', icon='stern', main='Wachsgießen sagt:', sub='Wird schon.'),
# Nikolaus
'NIK01': dict(layout='serif', main='War brav.', sub='Ungefähr.', deko='stern'),
'NIK02': dict(layout='check', items=[('Stiefel geputzt', True), ('Erwartungen hoch', True)]),
'NIK03': dict(layout='blase', bubble='Nüsse? Ernsthaft, Nikolaus?'),
'NIK04': dict(layout='marker', main='Rute?', sub='Ich nehm lieber Schokolade.'),
'NIK05': dict(layout='stempel', main='Nikolaus-Check', sub='Bestanden (knapp)', label=''),
'NIK06': dict(layout='icon', icon='stiefel', main='Mein Stiefel ist Größe 46.', sub='Nur so als Info.'),
'NIK07': dict(layout='bogen', top='Brav ist', bottom='relativ'),
'NIK08': dict(layout='script', scr='Lieber Nikolaus,', block='ich kann alles erklären.'),
'NIK09': dict(layout='lade', label='Brav gewesen?', pct=50, status='', cap='Kommt drauf an, wen du fragst.'),
'NIK10': dict(layout='streifen', main='Für Schokolade putze ich sogar Stiefel', sub=''),
# Valentinstag
'VAL01': dict(layout='icon', icon='herz', main='Du bist mein Mensch.', sub='Knapp vor Pizza.'),
'VAL02': dict(layout='script', scr='Ich liebe dich', block='mehr als Schlaf. Fast.'),
'VAL03': dict(layout='serif', main='Mein Herz gehört dir.', sub='Die Fernbedienung nicht.', deko='herz'),
'VAL04': dict(layout='bogen', top='Love is sharing', bottom='your fries. Sometimes.'),
'VAL05': dict(layout='bon', kopf='Kassenbon', zeilen=['Ich hab dich ausgesucht.'], summe='Umtausch ausgeschlossen.'),
'VAL06': dict(layout='marker', main='Zusammen nerven wir besser.'),
'VAL07': dict(layout='blase', pre='Du hattest mich bei', bubble='„Hast du Hunger?“'),
'VAL08': dict(layout='woerterbuch', main='Romantik, die', sub='Wenn du mir das letzte Stück lässt.', label='Substantiv, halbernst'),
'VAL09': dict(layout='stempel', main='Certified cuddle expert', sub='', label='Liebeserklärung'),
'VAL10': dict(layout='gross', main='Liebe ist, die Sprachnachricht trotzdem anzuhören', sub=''),
# Muttertag
'MUT01': dict(layout='serif', main='Mama hat immer recht.', sub='Auch wenn nicht.', deko='herz'),
'MUT02': dict(layout='icon', icon='medaille', main='Beste Mama der Welt', sub='Laut unabhängiger Familienumfrage.'),
'MUT03': dict(layout='check', titel='Mama.', items=[('Chefin.', True), ('Taxi.', True), ('Küche.', True), ('Alles.', True)]),
'MUT04': dict(layout='schild', main='Ich bin Mama.', sub='Ich hab Augen im Hinterkopf.', label='Mama-Regel'),
'MUT05': dict(layout='zitat', main='„Weil ich es gesagt habe.“ – Mama, seit Jahren', sub='', label=''),
'MUT06': dict(layout='lade', label='Mom mode', pct=100, status='AKTIV', cap='Always on'),
'MUT07': dict(layout='marker', main='Kaffee rein.', sub='Mama-Modus an.'),
'MUT08': dict(layout='woerterbuch', main='Mama, die', sub='Zuständig für alles, was keiner findet.', label='Substantiv, halbernst'),
'MUT09': dict(layout='bogen', top='Offiziell Mama', bottom='Inoffiziell Superheldin'),
'MUT10': dict(layout='warn', text='Ich hab Kinder großgezogen. Ich hab vor nichts mehr Angst.'),
# Vatertag
'VAT01': dict(layout='bogen', top='Papa', bottom='Der Mann. Der Grill. Die Legende.'),
'VAT02': dict(layout='serif', main='Ich hab keine Witze.', sub='Ich hab Papa-Witze.', deko='stern'),
'VAT03': dict(layout='blase', bubble='Wo ist Papa?', post='„Am Grill.“'),
'VAT04': dict(layout='check', titel='Papa repariert das.', items=[('Irgendwann', False)]),
'VAT05': dict(layout='lade', label='Dad mode', pct=64, status='LÄDT …', cap='Loading …'),
'VAT06': dict(layout='icon', icon='werkzeug', main='Ich bin Papa.', sub='Ich weiß, wo der Akkuschrauber ist.'),
'VAT07': dict(layout='stempel', main='Papa des Jahres', sub='Laut Papa.', label=''),
'VAT08': dict(layout='woerterbuch', main='Papa, der', sub='Profi im Einschlafen auf dem Sofa.', label='Substantiv, halbernst'),
'VAT09': dict(layout='warn', text='Finger weg vom Thermostat.'),
'VAT10': dict(layout='script', scr='Nicht alt.', block='Papa-Level erreicht.'),
# Jahrestag
'JAH01': dict(layout='bon', kopf='Kassenbon', zeilen=['1x Lieblingsperson', 'Rückgabe: keine'], summe='Immer noch nicht umgetauscht.'),
'JAH02': dict(layout='serif', main='Wir reifen wie guter Wein.', deko='herz'),
'JAH03': dict(layout='script', scr='Du bist mein', block='Lieblingsnerv'),
'JAH04': dict(layout='bogen', top='Gemeinsam Unsinn', bottom='machen seit dem ersten Date'),
'JAH05': dict(layout='icon', icon='tasse', main='Ich hab dich lieb.', sub='Sogar vor dem ersten Kaffee.'),
'JAH06': dict(layout='torte', titel='Unsere Beziehung:', stuecke=[('Liebe', 50), ('„Was essen wir?“', 50)]),
'JAH07': dict(layout='marker', main='Wir streiten nur über Snacks.'),
'JAH08': dict(layout='stempel', main='Team Wir', sub='', label='Beziehungsstatus'),
'JAH09': dict(layout='check', items=[('Jahrestag nicht vergessen', True)], cap='(Das Handy hat erinnert.)'),
'JAH10': dict(layout='icon', icon='herzen', main='Zusammen seit damals.', sub='Immer noch mein Mensch.'),
# Hochzeitstag
'HOC01': dict(layout='check', items=[('Verheiratet.', True), ('Ausgesucht.', True), ('Behalten.', True)]),
'HOC02': dict(layout='blase', bubble='Ja gesagt. Bereut?', post='Nur beim Möbelaufbauen.'),
'HOC03': dict(layout='serif', main='Bis dass der Abwasch uns scheidet.', deko='herz'),
'HOC04': dict(layout='script', scr='Married', block='and still laughing'),
'HOC05': dict(layout='icon', icon='ringe', main='Wir haben Ja gesagt.', sub='Zum Glück. Und zum Chaos.'),
'HOC06': dict(layout='bon', kopf='Ehevertrag', zeilen=['Verheiratet', 'Laufzeit: unbefristet'], summe='Freiwillig.'),
'HOC07': dict(layout='bogen', top='Ehefrau', bottom='Hat das letzte Wort. Und das vorletzte.'),
'HOC08': dict(layout='lade', label='Ehemann hört zu', pct=70, status='', cap='Meistens.'),
'HOC09': dict(layout='gross', main='Immer noch verheiratet', sub='Immer noch lustig.'),
'HOC10': dict(layout='torte', titel='Ehe heißt: Pizza teilen.', stuecke=[('Halbe-halbe.', 62), ('Ungefähr.', 38)]),
# Rente
'REN01': dict(layout='bogen', top='Rentner', bottom='Ich hab keine Zeit.'),
'REN02': dict(layout='woerterbuch', main='Ruhestand, der', sub='Ich hatte noch nie so viel vor.', label='Substantiv, halbernst'),
'REN03': dict(layout='icon', icon='wecker', main='Wecker gekündigt.', sub='Für immer.'),
'REN04': dict(layout='serif', main='Ab jetzt ist jeder Tag Samstag.', deko='stern'),
'REN05': dict(layout='stempel', main='Nicht arbeitslos', sub='Fertig.', label=''),
'REN06': dict(layout='script', scr='Retired.', block='Not tired.'),
'REN07': dict(layout='schild', main='Hauptberuflich Hobby', sub='', label='Ruhestand'),
'REN08': dict(layout='blase', bubble='Montag?', post='Kenn ich nicht mehr.'),
'REN09': dict(layout='marker', main='Jahrzehnte gearbeitet.', sub='Jetzt wird gegärtnert.'),
'REN10': dict(layout='lade', label='Feierabend', pct=100, status='FÜR IMMER', cap='Für immer.'),
# Abschluss
'ABS01': dict(layout='script', scr='Geschafft.', block='Fragt nicht, wie.'),
'ABS02': dict(layout='icon', icon='hut', main='Offiziell schlau.'),
'ABS03': dict(layout='check', items=[('Abschluss in der Tasche', True), ('Plan', False)], cap='Noch nicht.'),
'ABS04': dict(layout='stempel', main='Überlebt', sub='Prüfung: bestanden.', label=''),
'ABS05': dict(layout='bogen', top='Class', bottom='dismissed'),
'ABS06': dict(layout='serif', main='Lernen war gestern.', sub='Feiern ist heute.', deko='stern'),
'ABS07': dict(layout='schild', main='Jetzt mit Zeugnis', sub='', label='Zeugnis'),
'ABS08': dict(layout='torte', titel='Bestanden.', stuecke=[('Kaffee', 60), ('Panik', 40)]),
'ABS09': dict(layout='lade', label='Ab heute Profi', pct=97, status='', cap='Fast.'),
'ABS10': dict(layout='marker', main='Meine Noten sind privat.', sub='Mein Abschluss nicht.'),
# Einzug
'EIN01': dict(layout='icon', icon='haus', main='Neue Bude,', sub='neues Chaos.'),
'EIN02': dict(layout='lade', label='Kisten ausgepackt', pct=6, pt='3 von 47', status='', cap=''),
'EIN03': dict(layout='script', scr='Endlich daheim.', block='Fast fertig.'),
'EIN04': dict(layout='schild', main='Hier wohnen Kisten.', sub='Und wir.', label='Neue Adresse'),
'EIN05': dict(layout='check', items=[('Erst einziehen', True), ('Dann einrichten', False)], cap='Irgendwann.'),
'EIN06': dict(layout='serif', main='Der Bohrer gehört jetzt zur Familie.', deko='stern'),
'EIN07': dict(layout='gesucht', main='Freunde.', sub='Mit Transporter.'),
'EIN08': dict(layout='bogen', top='Neue Adresse,', bottom='alte Gewohnheiten'),
'EIN09': dict(layout='check', items=[('Möbel aufgebaut', True), ('Beziehung überlebt', True)]),
'EIN10': dict(layout='blase', bubble='Housewarming?', post='Erst mal WLAN.'),
}
ANL = {'WEI': 'Weihnachten', 'SIL': 'Silvester', 'NIK': 'Nikolaus', 'VAL': 'Valentinstag', 'MUT': 'Muttertag', 'VAT': 'Vatertag',
       'JAH': 'Jahrestag', 'HOC': 'Hochzeitstag', 'REN': 'Rente', 'ABS': 'Abschluss', 'EIN': 'Einzug'}

if __name__ == '__main__':
    od = '/home/claude/anlaesse/svg2'; os.makedirs(od, exist_ok=True)
    only = sys.argv[1].split(',') if len(sys.argv) > 1 else None
    for pid, spec in S.items():
        if only and pid[:3] not in only: continue
        spec['id'] = pid
        for v in ('hell', 'dunkel'):
            s, h = svg(spec, ANL[pid[:3]], v)
            open(f'{od}/{pid}_{v}_brust.svg', 'w').write(s)
            if h > 5000: print('ZU HOCH', pid, round(h))
    from collections import Counter; print(len(S), Counter(v['layout'] for v in S.values()))

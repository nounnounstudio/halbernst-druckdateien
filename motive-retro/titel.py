import json
T=[
("Katze schubst Tasse","Sie sieht dich an. Sie sieht die Tasse an. Du weißt, wie das endet. Für alle, die mit einer Katze zusammenleben – oder genauso drauf sind.",["katze","katzen","katzenliebhaber"]),
("Rennschnecke","Volle Geschwindigkeit. Also für Schneckenverhältnisse. Für alle, die ihr eigenes Tempo haben und dazu stehen.",["schnecke","langsam","gemütlich"]),
("Faultier lädt noch","Akku bei 3 %, Motivation auch. Das Shirt für Montage, Sonntage und eigentlich jeden Tag.",["faultier","müde","montag"]),
("Grillen im Regen","Echte Grillmeister kennen kein schlechtes Wetter. Nur falsche Schirme. Für Ganzjahresgriller.",["grillen","grill","bbq","grillmeister"]),
("Rakete mit Stützrädern","Große Pläne, kleine Schritte. Für alle, die hoch hinaus wollen – aber sicher ist sicher.",["rakete","weltall","motivation"]),
("Akku-Tasse","Ohne Kaffee bei 10 %. Für alle, die morgens erst nach der ersten Tasse ansprechbar sind.",["kaffee","kaffeeliebhaber","müde","büro"]),
("EKG-Berge","Herzschlag im Gebirge: für Wanderer, Bergfans und alle, deren Puls beim Gipfelblick steigt.",["berge","wandern","outdoor","natur"]),
("Einzelsocke","Irgendwo da draußen ist die zweite. Für alle, deren Waschmaschine Socken frisst.",["socke","wäsche","haushalt"]),
("Funkloch im Zelt","Kein Netz, kein Stress. Für Camper, Outdoor-Fans und alle, die mal offline sein wollen.",["camping","zelt","outdoor","wlan"]),
("Kaffee-Sanduhr","Die Zeit läuft – aber erst nach dem Kaffee. Für Kaffeeliebhaber mit Zeitgefühl.",["kaffee","kaffeeliebhaber","zeit"]),
("Sofa-Abdruck","Das Sofa kennt deine Form. Für alle, die ihren Lieblingsplatz gefunden haben.",["sofa","couch","gemütlich","faul"]),
("Kaffee-Infusion","Medizinisch notwendig. Für Pflegekräfte, Nachtschichtler und alle, die Kaffee intravenös bräuchten.",["kaffee","pflege","nachtschicht","büro"]),
("Wurst im Schlafrock","Wörtlich genommen. Für Grillfans, Wortspiel-Liebhaber und alle, die im Bademantel frühstücken.",["wurst","wortspiel","grillen","frühstück"]),
("Dackel-Hotdog","Der Hot Dog, wie er sein sollte: mit echtem Dackel. Für Dackelfans und Hundemenschen.",["dackel","hund","hunde","hotdog"]),
("Katze im Karton","Das Geschenk war teuer. Der Karton ist besser. Für alle Katzenmenschen.",["katze","katzen","katzenliebhaber","karton"]),
("Katze auf der Tastatur","Homeoffice mit Katze: Sie arbeitet jetzt hier. Für alle, die mit Katze am Schreibtisch sitzen.",["katze","homeoffice","büro","katzenliebhaber"]),
("Croissant-Mond","Gute Nacht, Croissant. Für Frühstücksfans, Bäckerei-Liebhaber und Nachtschwärmer.",["croissant","frühstück","mond","bäckerei"]),
("Donut-Rettungsring","Rettet Leben. Oder zumindest den Nachmittag. Für Naschkatzen und Sommerfans.",["donut","sommer","süß","meer"]),
("Wecker mit Schlafmaske","Sogar der Wecker will nicht aufstehen. Für Morgenmuffel und Snooze-Profis.",["wecker","morgenmuffel","schlafen","müde"]),
("Erschrockene Steckdose","Der Stecker kommt. Die Steckdose ist nicht bereit. Für Elektriker und Technikfans mit Humor.",["steckdose","elektriker","technik","handwerk"]),
("Fernbedienung in der Sofaritze","Da ist sie ja! Für alle, die jeden Abend dieselbe Suche starten.",["fernbedienung","sofa","couch","fernsehen"]),
("Schwitzende Sonne","Sogar der Sonne ist es zu heiß. Für Sommerkinder und alle, die bei 30 Grad schmelzen.",["sonne","sommer","hitze","eis"]),
("Torte mit Feuerlöscher","Ab einer gewissen Kerzenzahl Pflicht. Das Geschenk zum runden Geburtstag mit Augenzwinkern.",["geburtstag","runder geburtstag geschenk","torte","geburtstagsgeschenk"]),
("Bauer mit Krone","Vom Bauern zur Dame – jeder fängt mal klein an. Für Schachspieler und Aufsteiger.",["schach","schachspieler","brettspiel","motivation"]),
("Waschmaschine frisst Socke","Hier verschwinden sie also. Für alle, die das Sockenrätsel endlich gelöst haben.",["socke","waschmaschine","wäsche","haushalt"]),
]
out=[]
for i,(n,d,t) in enumerate(T,1):
    out.append({"i":i,"title":f"{n} – Retro-T-Shirt","desc":f"<p><strong>{n}.</strong> {d}</p><p>Retro-Motiv im Vintage-Stil, gedruckt auf Bestellung.</p>","tags":t+["retro","vintage","t-shirt","geschenk","motiv ohne text"]})
json.dump(out,open('/home/claude/retro_shop/retro.json','w'),ensure_ascii=False,indent=0)
print(len(out))

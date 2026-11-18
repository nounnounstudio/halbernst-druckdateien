"""Erzeugt die Seiteninhalte (HTML + JS) für die Halbernst-Werkzeuge.
Alles läuft direkt im Shopify-Seiteninhalt, Produktdaten kommen live von /products.json (gleiche Domain)."""
import json, os
OUT = "/home/claude/web/out"
os.makedirs(OUT, exist_ok=True)

CSS = """<style>
.hb{--ink:#141414;--rot:#D64026;--gelb:#FFBE28;--creme:#F5F0E4;font-family:inherit;color:var(--ink);max-width:980px;margin:0 auto}
.hb *{box-sizing:border-box}
.hb h2,.hb .big{font-family:Anton,Impact,'Arial Narrow',sans-serif;text-transform:uppercase;letter-spacing:.5px;line-height:1.05;margin:.2em 0}
.hb .box{background:#fff;border:3px solid var(--ink);box-shadow:6px 6px 0 var(--ink);padding:18px;margin:18px 0}
.hb .chips{display:flex;flex-wrap:wrap;gap:8px;margin:8px 0 14px}
.hb .chip{border:2px solid var(--ink);background:#fff;padding:7px 12px;border-radius:999px;cursor:pointer;font-weight:700;font-size:15px}
.hb .chip.on{background:var(--gelb)}
.hb label{display:block;font-weight:800;margin:10px 0 4px}
.hb input,.hb select,.hb textarea{width:100%;padding:10px;border:2px solid var(--ink);font-size:16px;background:#fff;border-radius:0}
.hb .btn{display:inline-block;border:3px solid var(--ink);background:var(--rot);color:#fff;font-weight:900;padding:12px 18px;cursor:pointer;text-decoration:none;box-shadow:4px 4px 0 var(--ink);font-size:16px;margin:6px 6px 6px 0}
.hb .btn.gelb{background:var(--gelb);color:var(--ink)}.hb .btn.weiss{background:#fff;color:var(--ink)}
.hb .grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(170px,1fr));gap:14px}
.hb .card{border:2px solid var(--ink);background:#fff;text-decoration:none;color:var(--ink);display:flex;flex-direction:column}
.hb .card img{width:100%;aspect-ratio:1;object-fit:cover;background:var(--creme)}
.hb .card b{display:block;padding:8px 8px 2px;font-size:14px;line-height:1.25}
.hb .card span{padding:0 8px 8px;font-size:13px;color:#555}
.hb .card em{padding:0 8px 8px;font-style:normal;font-weight:800}
.hb .hint{background:var(--gelb);border:2px solid var(--ink);padding:10px 12px;font-weight:700}
.hb .hint.rot{background:var(--rot);color:#fff}.hb .hint.gruen{background:#cfe8b8}
.hb .muted{color:#555;font-size:14px}
.hb .center{text-align:center}
</style>"""

# ---------- gemeinsame Bausteine ----------
JS_BASE = r"""
var HB=window.HB||{};window.HB=HB;
HB.load=HB.load||function(){if(HB._p)return HB._p;HB._p=(async function(){var all=[];for(var p=1;p<5;p++){var r=await fetch('/products.json?limit=250&page='+p);if(!r.ok)break;var j=await r.json();if(!j.products.length)break;all=all.concat(j.products);if(j.products.length<250)break;}return all;})();return HB._p;};
HB.norm=function(s){return (s||'').toLowerCase().replace(/ä/g,'ae').replace(/ö/g,'oe').replace(/ü/g,'ue').replace(/ß/g,'ss');};
HB.text=function(p){return HB.norm(p.title+' '+(p.tags||[]).join(' ')+' '+(p.product_type||''));};
HB.price=function(p){var v=(p.variants||[])[0];return v?(Number(v.price).toFixed(2).replace('.',',')+' €'):'';};
HB.card=function(p,why){var img=(p.images&&p.images[0])?p.images[0].src.replace(/(\.[a-z]+)(\?|$)/i,'_400x$1$2'):'';var t=p.title.lastIndexOf(' – ')>0?p.title.slice(0,p.title.lastIndexOf(' – ')):p.title;return '<a class="card" href="/products/'+p.handle+'"><img loading="lazy" src="'+img+'" alt="'+t.replace(/"/g,'')+'"><b>'+t+'</b>'+(why?'<span>'+why+'</span>':'')+'<em>ab '+HB.price(p)+'</em></a>';};
HB.esc=function(s){return String(s).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];});};
HB.LIEFERTAGE=8;
HB.frist=function(ziel){var d=new Date(ziel+'T00:00:00');var heute=new Date();heute.setHours(0,0,0,0);var bis=new Date(d);bis.setDate(bis.getDate()-HB.LIEFERTAGE);var tage=Math.round((bis-heute)/864e5);return {tage:tage,bis:bis};};
HB.datum=function(d){return d.toLocaleDateString('de-DE',{day:'numeric',month:'long'});};
"""

def page(name, html, js):
    body = CSS + html + "<script>(function(){" + JS_BASE + js + "})();</script>"
    open(f"{OUT}/{name}.html", "w").write(body)
    return body

# ---------- 1 Geschenk-Finder ----------
FINDER_HTML = """<div class="hb" id="hb-finder">
<p class="big" style="font-size:34px">Das passende Shirt in 20 Sekunden</p>
<p>Sag uns kurz, für wen und wofür. Wir suchen aus allen Halbernst-Designs die passenden raus.</p>
<div class="box">
<label>Anlass</label><div class="chips" data-k="anlass"></div>
<label>Für wen?</label><div class="chips" data-k="wer"></div>
<label>Alter (optional)</label><input id="f-alter" type="number" min="1" max="110" placeholder="z. B. 50">
<label>Was mag die Person?</label><div class="chips" data-k="int"></div>
<button class="btn" id="f-go">Geschenk finden</button>
</div>
<div id="f-frist"></div>
<div id="f-out"></div>
</div>"""
FINDER_JS = r"""
var A=[['geburtstag','🎂 Geburtstag'],['rund','🎉 Runder Geburtstag'],['weihnachten','🎄 Weihnachten'],['nikolaus','🎅 Nikolaus'],['silvester','🎆 Silvester'],['kollegen','💼 Kollegen'],['einfach','😏 Einfach so']];
var W=[['papa','Papa'],['mama','Mama'],['opa','Opa'],['oma','Oma'],['partner','Partner/in'],['freund','Freund/in'],['kollege','Kollege/in'],['geschwister','Bruder/Schwester'],['ich','Mich selbst']];
var I=[['grillen','🔥 Grillen'],['hunde','🐶 Hunde'],['handwerk','🔨 Handwerk'],['buero','💻 Büro'],['pflege','🩺 Pflege'],['lehrer','📚 Schule'],['ki','🤖 KI & Technik'],['englisch','🇬🇧 Englischer Humor'],['fussball','⚽ Fußball'],['kaffee','☕ Kaffee'],['party','🥳 Party'],['schlaf','😴 Schlafen']];
var S={anlass:'geburtstag',wer:'',int:[]};
var KEY={grillen:['grill','bbq','rost','smoker','raeucher','glut','fleisch','steak'],hunde:['hund','dackel','labrador','retriever','collie','bulldog','schaeferhund','gassi'],handwerk:['handwerk','heimwerk','werkstatt','elektrik','messe'],buero:['buero','excel','kalender','meeting','homeoffice'],pflege:['pflege','rettung','notaufnahme'],lehrer:['lehrer','komma','schule'],ki:['ki ','ki-',' ai','generiert','captcha','kuenstlich','bugs','prompt'],englisch:['englisch','unhinged'],fussball:['fussball','platz'],kaffee:['kaffee'],party:['party','buffet','snack'],schlaf:['nickerchen','muede','schlafanzug','couch']};
var ANL={weihnachten:['weihnacht','plaetzchen','lichterkette','kekse','cookies','merry','familienfest','verdauung','liste','klebeband','essens'],nikolaus:['nikolaus','stiefel','brav','rute'],silvester:['silvester','neujahr','vorsaetze','countdown','raclette','new year','rutsche','wachsgiessen','0:01'],geburtstag:['geburtstag','juenger','baujahr','aelter'],rund:['geburtstag','30','40','50','60','rund'],kollegen:['buero','berufe','kollegen','meeting','excel','kalender']};
var FR={weihnachten:'-12-24',nikolaus:'-12-06',silvester:'-12-31'};
function chips(){document.querySelectorAll('#hb-finder .chips').forEach(function(el){var k=el.dataset.k,L=k=='anlass'?A:k=='wer'?W:I;el.innerHTML=L.map(function(x){var on=k=='int'?S.int.indexOf(x[0])>=0:S[k]==x[0];return '<button type="button" class="chip'+(on?' on':'')+'" data-v="'+x[0]+'">'+x[1]+'</button>';}).join('');el.onclick=function(e){var v=e.target.dataset&&e.target.dataset.v;if(!v)return;if(k=='int'){var i=S.int.indexOf(v);i>=0?S.int.splice(i,1):S.int.push(v);}else S[k]=S[k]==v&&k=='wer'?'':v;chips();};});}
function frist(){var box=document.getElementById('f-frist');var suf=FR[S.anlass];if(!suf){box.innerHTML='';return;}var y=new Date().getFullYear();var z=y+suf;if(new Date(z)<new Date())z=(y+1)+suf;var f=HB.frist(z);var c=f.tage>5?'gruen':f.tage>=0?'':'rot';var t=f.tage>5?'Entspannt: Bestell bis '+HB.datum(f.bis)+', dann ist es rechtzeitig da.':f.tage>=0?'Jetzt bestellen! Noch '+f.tage+' Tag'+(f.tage==1?'':'e')+' für die rechtzeitige Lieferung.':'Für die Lieferung wird es knapp. Schick lieber einen Glückwunsch aus dem <a href="/pages/glueckwunsch">Glückwunsch-Generator</a>.';box.innerHTML='<p class="hint '+c+'">⏰ '+t+'</p>';}
async function go(){var out=document.getElementById('f-out');out.innerHTML='<p>Suche passende Shirts …</p>';frist();var P=await HB.load();var alter=parseInt(document.getElementById('f-alter').value)||0;var res=P.map(function(p){var t=HB.text(p),s=0,why=[];(ANL[S.anlass]||[]).forEach(function(k){if(t.indexOf(k)>=0){s+=3;}});if(s)why.push(A.filter(function(a){return a[0]==S.anlass})[0][1].replace(/^\S+ /,''));if(alter){var dek=Math.floor(alter/10)*10;if(t.indexOf(dek+'. geburtstag')>=0||t.indexOf(' '+dek+' ')>=0||p.title.indexOf(dek+' ')==0||p.title.indexOf(dek+':')==0){s+=6;why.push('Zum '+dek+'.');}}S.int.forEach(function(i){if((KEY[i]||[]).some(function(k){return t.indexOf(k)>=0;})){s+=4;why.push(I.filter(function(x){return x[0]==i})[0][1].replace(/^\S+ /,''));}});if(S.wer=='papa'&&t.indexOf('papa')>=0){s+=3;why.push('Für Papa');}if(S.wer=='kollege'&&t.indexOf('kollegen')>=0){s+=3;why.push('Für Kollegen');}return {p:p,s:s,why:why.join(' · ')};}).filter(function(x){return x.s>0;}).sort(function(a,b){return b.s-a.s;}).slice(0,12);
if(!res.length){out.innerHTML='<div class="box"><p>Dazu haben wir gerade nichts Passendes. Schau dich bei <a href="/collections/all">allen Designs</a> um oder probier andere Interessen.</p></div>';return;}
out.innerHTML='<h2>Unsere Vorschläge</h2><div class="grid">'+res.map(function(x){return HB.card(x.p,x.why);}).join('')+'</div><p class="center"><a class="btn gelb" href="/pages/glueckwunsch">Glückwunsch dazu schreiben</a></p>';out.scrollIntoView({behavior:'smooth'});}
chips();document.getElementById('f-go').onclick=go;
var q=new URLSearchParams(location.search);if(q.get('anlass')){S.anlass=q.get('anlass');chips();go();}
"""

# ---------- 2 Glückwunsch-Generator ----------
GW_HTML = """<div class="hb" id="hb-gw">
<p class="big" style="font-size:34px">Glückwunsch in 10 Sekunden</p>
<p>Anlass wählen, Ton wählen, fertig. Text anpassen, als Bild speichern oder direkt per WhatsApp schicken. Kostenlos.</p>
<div class="box">
<label>Anlass</label><div class="chips" data-k="anlass"></div>
<label>Ton</label><div class="chips" data-k="ton"></div>
<label>Name (optional)</label><input id="g-name" placeholder="z. B. Papa">
<label>Dein Text</label><textarea id="g-text" rows="3"></textarea>
<button class="btn gelb" id="g-neu">🎲 Anderer Text</button>
<div class="chips" data-k="look"></div>
<canvas id="g-cv" width="1080" height="1080" style="width:100%;max-width:420px;border:3px solid #141414;display:block;margin:10px 0"></canvas>
<a class="btn" id="g-wa" target="_blank" rel="noopener">💬 Per WhatsApp senden</a>
<button class="btn weiss" id="g-copy">📋 Text kopieren</button>
<button class="btn weiss" id="g-dl">🖼 Bild speichern</button>
</div>
<p class="center"><a class="btn gelb" href="/pages/geschenk-finder">🎁 Passendes Shirt dazu finden</a></p>
</div>"""
GW_JS = r"""
var A=[['geburtstag','🎂 Geburtstag'],['rund','🎉 Runder Geburtstag'],['weihnachten','🎄 Weihnachten'],['silvester','🎆 Neujahr'],['rente','🏖 Rente'],['nachtraeglich','⏰ Nachträglich']];
var T=[['lustig','😂 Lustig'],['lieb','❤️ Lieb'],['frech','😏 Frech']];
var L=[['0','Look 1'],['1','Look 2'],['2','Look 3'],['3','Look 4']];
var LOOK=[{bg:'#F5F0E4',fg:'#141414',ak:'#D64026'},{bg:'#141414',fg:'#F5F0E4',ak:'#FFBE28'},{bg:'#FFBE28',fg:'#141414',ak:'#D64026'},{bg:'#D64026',fg:'#FFFFFF',ak:'#FFBE28'}];
var X={geburtstag:{lustig:['Alles Gute, {n}! Du wirst nicht älter, nur besser im Verdrängen.','Herzlichen Glückwunsch, {n}! Die Kerzen kosten inzwischen mehr als der Kuchen.','Happy Birthday, {n}! Ab heute zählt jedes Knacken als Applaus.'],lieb:['Alles Liebe zum Geburtstag, {n}! Schön, dass es dich gibt.','Happy Birthday, {n}! Auf ein Jahr voller guter Tage und noch besserer Abende.','Herzlichen Glückwunsch, {n}! Bleib genau so, nur mit mehr Kuchen.'],frech:['Glückwunsch, {n}! Du siehst keinen Tag älter aus als gestern.','Happy Birthday, {n}! Weisheit kommt mit dem Alter. Bei dir lässt sie sich Zeit.','Alles Gute, {n}! Ich hätte dir ja was geschenkt, aber du hast ja schon mich.']},
rund:{lustig:['Glückwunsch zum Runden, {n}! Nicht alt, nur Vintage.','Ein runder Geburtstag, {n}! Ab jetzt zählen wir in Jahrzehnten.','Herzlichen Glückwunsch, {n}! Neues Jahrzehnt, gleiche Ausreden.'],lieb:['Alles Liebe zum runden Geburtstag, {n}! Auf das nächste Jahrzehnt mit dir.','Herzlichen Glückwunsch, {n}! So viele Jahre, und jedes davon hat sich gelohnt.'],frech:['Glückwunsch, {n}! Die Zahl ist rund. Du hoffentlich nur ein bisschen.','Happy Birthday, {n}! Willkommen im Club der Leute, die beim Aufstehen Geräusche machen.']},
weihnachten:{lustig:['Frohe Weihnachten, {n}! Möge dein Bauch voller sein als dein Terminkalender.','Frohe Weihnachten, {n}! Plätzchen zählen an Feiertagen nicht. Ist wissenschaftlich so.'],lieb:['Frohe Weihnachten, {n}! Schöne, ruhige Tage mit allen, die du magst.','Frohe Weihnachten, {n}! Danke, dass du mein Jahr besser gemacht hast.'],frech:['Frohe Weihnachten, {n}! Ich hab dem Weihnachtsmann gesagt, du warst brav. Du schuldest mir was.','Frohe Weihnachten, {n}! Familienfest überleben, nächstes Jahr wieder.']},
silvester:{lustig:['Guten Rutsch, {n}! Und gleiche Vorsätze wie letztes Jahr.','Frohes neues Jahr, {n}! Neues Jahr, gleicher Quatsch.'],lieb:['Frohes neues Jahr, {n}! Auf ein Jahr mit vielen guten Momenten.','Guten Rutsch, {n}! Ich freu mich auf alles, was wir nächstes Jahr erleben.'],frech:['Guten Rutsch, {n}! Um 0:01 Uhr schon gescheitert ist auch eine Leistung.','Frohes Neues, {n}! Dieses Jahr wird alles anders. Sagst du ja jedes Jahr.']},
rente:{lustig:['Alles Gute zur Rente, {n}! Ab jetzt ist jeder Tag Samstag.','Glückwunsch zur Rente, {n}! Der Wecker hat endgültig verloren.'],lieb:['Alles Liebe zum Ruhestand, {n}! Genieß jede freie Minute, du hast sie dir verdient.'],frech:['Glückwunsch zur Rente, {n}! Jetzt hast du keine Ausrede mehr für den Keller.']},
nachtraeglich:{lustig:['Alles Gute nachträglich, {n}! Ich wollte nur sichergehen, dass du auch nach dem Geburtstag noch gefeiert wirst.','Nachträglich alles Gute, {n}! Ich bin nicht zu spät, ich verlängere deinen Geburtstag.'],lieb:['Alles Liebe nachträglich, {n}! Spät, aber von Herzen.'],frech:['Alles Gute nachträglich, {n}! Ich hab dran gedacht. Nur nicht pünktlich.']}};
var S={anlass:'geburtstag',ton:'lustig',look:'0',i:0};
function chips(){document.querySelectorAll('#hb-gw .chips').forEach(function(el){var k=el.dataset.k,Li=k=='anlass'?A:k=='ton'?T:L;el.innerHTML=Li.map(function(x){return '<button type="button" class="chip'+(S[k]==x[0]?' on':'')+'" data-v="'+x[0]+'">'+x[1]+'</button>';}).join('');el.onclick=function(e){var v=e.target.dataset&&e.target.dataset.v;if(!v)return;S[k]=v;if(k!='look'){S.i=0;setText();}chips();draw();};});}
function setText(){var n=document.getElementById('g-name').value.trim();var arr=X[S.anlass][S.ton];var t=arr[S.i%arr.length];t=n?t.replace('{n}',n):t.replace(', {n}','').replace(' {n}','');document.getElementById('g-text').value=t;upd();}
function wrap(c,t,w){var ws=t.split(' '),ls=[],l='';ws.forEach(function(x){var tr=l?l+' '+x:x;if(c.measureText(tr).width>w&&l){ls.push(l);l=x;}else l=tr;});if(l)ls.push(l);return ls;}
function draw(){var c=document.getElementById('g-cv'),x=c.getContext('2d'),lk=LOOK[+S.look],t=document.getElementById('g-text').value||' ';x.fillStyle=lk.bg;x.fillRect(0,0,1080,1080);x.fillStyle=lk.ak;x.fillRect(80,120,140,18);var fs=96,ls;do{x.font=fs+'px Anton, Impact, sans-serif';ls=wrap(x,t.toUpperCase(),900);fs-=6;}while(ls.length*fs*1.15>700&&fs>40);fs+=6;x.fillStyle=lk.fg;var y=200;ls.forEach(function(l){y+=fs*1.12;x.fillText(l,80,y);});x.font='bold 30px Arial, sans-serif';x.fillStyle=lk.ak;x.fillText('halbernst.de',80,1000);}
function upd(){var t=document.getElementById('g-text').value;document.getElementById('g-wa').href='https://wa.me/?text='+encodeURIComponent(t);draw();}
document.getElementById('g-neu').onclick=function(){S.i++;setText();};
document.getElementById('g-name').oninput=setText;document.getElementById('g-text').oninput=upd;
document.getElementById('g-copy').onclick=function(){navigator.clipboard.writeText(document.getElementById('g-text').value).then(function(){document.getElementById('g-copy').textContent='✅ Kopiert';});};
document.getElementById('g-dl').onclick=function(){var a=document.createElement('a');a.download='glueckwunsch-halbernst.png';a.href=document.getElementById('g-cv').toDataURL('image/png');a.click();};
var q=new URLSearchParams(location.search);if(q.get('anlass')&&X[q.get('anlass')])S.anlass=q.get('anlass');
chips();(document.fonts&&document.fonts.ready||Promise.resolve()).then(function(){setText();});
"""

# ---------- 3 Spruch des Tages ----------
SPRUECHE = ["Ich bin nicht faul, ich bin im Energiesparmodus.","Montag ist kein Wochentag, sondern ein Zustand.","Ich habe heute schon mit Menschen geredet. Reicht.","Mein Bett und ich sind in einer festen Beziehung.","Ich esse gesund: Pizza hat Tomaten.","Kaffee zuerst, Freundlichkeit später.","Ich war schon müde, bevor es cool war.","Plan A: Couch. Plan B: auch Couch.","Ich mache keine Fehler, ich mache Updates.","Sport? Ich trage Jogginghose. Zählt das?","Mein Kühlschrank kennt mich besser als mein Arzt.","Ich bin nicht zu spät, die anderen sind zu früh.","Erwachsensein ist hauptsächlich Abwaschen.","Mein Lieblingssport: Augenrollen.","Ich warte noch auf meinen Motivationsschub. Seit 2014.","Bevor du fragst: Nein.","Ich bin gut im Multitasking: Ich kann gleichzeitig nichts tun und müde sein.","Heute ist ein guter Tag, um nichts zu tun.","Kann Spuren von Sarkasmus enthalten.","Ich hab nicht zugenommen, ich hab Energie gespeichert.","Mein Akku ist leer. Mein Sozialakku auch.","Ich lese die AGB immer. Nicht.","Diät beginnt morgen. Seit drei Jahren.","Ich bin nicht neugierig, ich interessiere mich nur für alles.","Ich hab einen Plan. Er ist nur noch nicht fertig.","Das Leben ist zu kurz für schlechten Kaffee.","Ich gehe nicht joggen, ich gehe zum Kühlschrank. Schnell.","Lieber halbernst als gar nicht lustig.","Mein Gehirn hat zu viele Tabs offen.","Ich bin ein Morgenmensch. Nur nicht morgens."]
VOTE_HTML = """<div class="hb" id="hb-vote">
<p class="big" style="font-size:34px">Spruch des Tages</p>
<p>Jeden Tag ein neuer Spruch. Sag uns, ob er aufs Shirt soll. Die Favoriten der Community landen als Design im Shop.</p>
<div class="box center">
<p class="muted" id="v-datum"></p>
<p class="big" id="v-spruch" style="font-size:40px;margin:20px 0"></p>
<button class="btn" data-v="1">👍 Aufs Shirt damit</button><button class="btn weiss" data-v="0">👎 Eher nicht</button>
<p id="v-dank" class="hint" style="display:none"></p>
</div>
<div class="box"><h2>Eigenen Spruch einreichen</h2><p>Du hast einen besseren? Schick ihn uns. Wenn er ins Shirt-Sortiment kommt, bekommst du das erste Shirt geschenkt.</p>
<form method="post" action="/contact#vorschlag" accept-charset="UTF-8"><input type="hidden" name="form_type" value="contact"><input type="hidden" name="utf8" value="✓"><input type="hidden" name="contact[tags]" value="spruch-vorschlag">
<label>Dein Spruch</label><textarea name="contact[body]" rows="2" required maxlength="140"></textarea>
<label>Deine E-Mail (damit wir dir das Shirt schicken können)</label><input type="email" name="contact[email]" required>
<p class="muted">Wir nutzen deine E-Mail nur, um dich zu deinem Vorschlag zu kontaktieren. Mehr dazu in der <a href="/policies/privacy-policy">Datenschutzerklärung</a>.</p>
<button class="btn gelb" type="submit">Spruch einreichen</button></form></div>
<div class="box"><h2>Deine Lieblinge</h2><div id="v-fav" class="muted">Noch keine. Stimm oben ab!</div></div>
</div>"""
VOTE_JS = "var SP=" + json.dumps(SPRUECHE, ensure_ascii=False) + r""";
var heute=new Date();var tag=Math.floor((heute-new Date(heute.getFullYear(),0,0))/864e5);var s=SP[tag%SP.length];
document.getElementById('v-datum').textContent=heute.toLocaleDateString('de-DE',{weekday:'long',day:'numeric',month:'long'});
document.getElementById('v-spruch').textContent=s;
function lade(){try{return JSON.parse(localStorage.getItem('hb_votes')||'{}');}catch(e){return {};}}
function speichere(v){try{localStorage.setItem('hb_votes',JSON.stringify(v));}catch(e){}}
function fav(){var v=lade(),f=Object.keys(v).filter(function(k){return v[k]==1;});document.getElementById('v-fav').innerHTML=f.length?'<ul>'+f.map(function(x){return '<li>'+HB.esc(x)+'</li>';}).join('')+'</ul>':'Noch keine. Stimm oben ab!';}
function zeige(v){var d=document.getElementById('v-dank');d.style.display='block';d.textContent=v==1?'Danke! Deine Stimme zählt. Morgen gibt es den nächsten Spruch.':'Notiert. Morgen kommt ein besserer, versprochen.';}
document.querySelectorAll('#hb-vote [data-v]').forEach(function(b){b.onclick=function(){var v=lade();v[s]=+b.dataset.v;speichere(v);zeige(+b.dataset.v);fav();};});
var v=lade();if(s in v)zeige(v[s]);fav();
if(location.hash=='#vorschlag'&&location.search.indexOf('contact_posted')>=0){alert('Danke für deinen Spruch!');}
"""

# ---------- 4 Geburtstags-Erinnerung ----------
ER_HTML = """<div class="hb" id="hb-er">
<p class="big" style="font-size:34px">Nie wieder Geburtstag vergessen</p>
<p>Trag ein, wessen Geburtstag du nicht verpassen willst. Wir schicken dir rechtzeitig eine E-Mail, zehn Tage vorher, mit genug Zeit für ein Geschenk. Kostenlos und jederzeit abbestellbar.</p>
<div class="box">
<form method="post" action="/contact#erinnerung" accept-charset="UTF-8" id="er-form">
<input type="hidden" name="form_type" value="customer"><input type="hidden" name="utf8" value="✓">
<input type="hidden" name="contact[tags]" id="er-tags" value="erinnerung">
<label>Deine E-Mail</label><input type="email" name="contact[email]" required>
<label>Wessen Geburtstag?</label><input id="er-wer" placeholder="z. B. Papa" maxlength="30" required>
<label>Geburtstag (Tag und Monat)</label>
<div style="display:flex;gap:8px"><select id="er-tag"></select><select id="er-monat"></select></div>
<p class="muted"><input type="checkbox" required style="width:auto"> Ich möchte Erinnerungs-E-Mails von Halbernst erhalten. Ich kann mich jederzeit über den Link in jeder E-Mail abmelden. Details in der <a href="/policies/privacy-policy">Datenschutzerklärung</a>.</p>
<button class="btn" type="submit">Erinnerung anlegen</button>
</form>
<p id="er-ok" class="hint gruen" style="display:none">✅ Erledigt! Wir melden uns rechtzeitig vor dem Geburtstag.</p>
</div>
<div class="box"><h2>Schon jetzt was Passendes?</h2><p>Im <a href="/pages/geschenk-finder">Geschenk-Finder</a> findest du in 20 Sekunden das richtige Shirt. Und im <a href="/pages/glueckwunsch">Glückwunsch-Generator</a> den passenden Spruch dazu.</p></div>
</div>"""
ER_JS = r"""
var t=document.getElementById('er-tag'),m=document.getElementById('er-monat');
for(var i=1;i<=31;i++)t.innerHTML+='<option>'+i+'</option>';
['Januar','Februar','März','April','Mai','Juni','Juli','August','September','Oktober','November','Dezember'].forEach(function(n,i){m.innerHTML+='<option value="'+(i+1)+'">'+n+'</option>';});
document.getElementById('er-form').onsubmit=function(){var w=document.getElementById('er-wer').value.trim().toLowerCase().replace(/[^a-z0-9äöüß]+/g,'-').slice(0,20);var tg=('0'+t.value).slice(-2),mo=('0'+m.value).slice(-2);document.getElementById('er-tags').value='erinnerung, geb-'+mo+'-'+tg+', geb-'+mo+'-'+tg+'-'+w;};
if(location.search.indexOf('customer_posted=true')>=0){document.getElementById('er-ok').style.display='block';}
"""

# ---------- 5 Anlass-Seiten ----------
EMOJI = {"weihnachten":"🎄","nikolaus":"🎅","silvester":"🎆","runde-geburtstage":"🎂","grillen":"🔥","hunde":"🐶","buero-und-berufe":"💼","ki-humor":"🤖"}
def anlass_page(key, title, intro, kw, ziel_suffix=None, extra=""):
    html = f"""<div class="hb" id="hb-anl-{key}"><div style="font-size:64px;line-height:1;margin:4px 0 10px">{EMOJI[key]}</div><p>{intro}</p>
<div id="a-frist"></div><div id="a-out"><p>Lade Designs …</p></div>
<div class="box center"><p><b>Noch unsicher?</b> Der Geschenk-Finder hilft in 20 Sekunden.</p><a class="btn gelb" href="/pages/geschenk-finder?anlass={key}">🎁 Geschenk-Finder</a> <a class="btn weiss" href="/pages/glueckwunsch?anlass={key}">💬 Glückwunsch schreiben</a></div>{extra}</div>"""
    js = "var KW=" + json.dumps(kw, ensure_ascii=False) + ";var SUF=" + json.dumps(ziel_suffix) + r""";
if(SUF){var y=new Date().getFullYear(),z=y+SUF;if(new Date(z)<new Date())z=(y+1)+SUF;var f=HB.frist(z);var c=f.tage>5?'gruen':f.tage>=0?'':'rot';document.getElementById('a-frist').innerHTML='<p class="hint '+c+'">⏰ '+(f.tage>5?'Bestell bis '+HB.datum(f.bis)+', dann ist alles rechtzeitig da. Noch '+f.tage+' Tage.':f.tage>=0?'Jetzt bestellen! Nur noch '+f.tage+' Tag'+(f.tage==1?'':'e')+' für pünktliche Lieferung.':'Für pünktliche Lieferung wird es knapp. Ein Glückwunsch geht immer.')+'</p>';}
HB.load().then(function(P){var r=P.filter(function(p){var t=HB.text(p);return KW.some(function(k){return t.indexOf(k)>=0;});});document.getElementById('a-out').innerHTML=r.length?'<div class="grid">'+r.map(function(p){return HB.card(p);}).join('')+'</div>':'<p>Die Designs kommen in Kürze.</p>';});
"""
    return html, js

ANLAESSE = [
 ("weihnachten", "Lustige Weihnachts-Shirts", "Für alle, die Weihnachten lieben, aber nicht ganz so ernst nehmen: Plätzchen-Profis, Lichterketten-Entwirrer und Familienfest-Überlebende. Lustige Weihnachtsgeschenke, die wirklich getragen werden.", ["weihnacht","plaetzchen","lichterkette","cookies","merry","familienfest","verdauung","eine liste","klebeband","essens hier"], "-12-24"),
 ("nikolaus", "Nikolaus-Shirts mit Augenzwinkern", "Stiefel geputzt, Erwartungen hoch: Shirts für alle, die beim Thema „brav“ lieber nicht ins Detail gehen. Die kleine Nikolausüberraschung für Erwachsene.", ["nikolaus","stiefel","brav","rute"], "-12-06"),
 ("silvester", "Silvester-Shirts für den guten Rutsch", "Raclette-Liebhaber, Vorsatz-Recycler und Leute, die um 22 Uhr im Schlafanzug feiern: Hier ist dein Outfit für den Jahreswechsel.", ["silvester","neujahr","vorsaetze","countdown","raclette","new year","rutsche","wachsgiessen"], "-12-31"),
 ("runde-geburtstage", "Shirts zum runden Geburtstag", "30, 40, 50, 60: Für jedes Jahrzehnt der passende Spruch. Das Geschenk, über das auf der Party alle lachen, vor allem das Geburtstagskind.", ["geburtstag"], None),
 ("grillen", "Grill-Shirts für echte Grillmeister", "Kerntemperatur, Glut und Geduld: Shirts für alle, die am Rost das Sagen haben. Das perfekte Geschenk für Grillfans, Smoker-Profis und Ganzjahresgriller.", ["grill","bbq","rost","smoker","raeucher","glut"], None),
 ("hunde", "Lustige Shirts für Hundemenschen", "Dackel, Labrador, Border Collie und alle anderen: Shirts für Leute, deren Hund eigentlich das Sagen hat. Hundehaare inklusive.", ["hund","dackel","labrador","retriever","collie","bulldog"], None),
 ("buero-und-berufe", "Shirts fürs Büro und den Job", "Excel-Profis, Pflegekräfte, Handwerker, Lehrkräfte: Humor für alle, die ihren Job ernst nehmen, sich selbst aber nicht. Ideal als Kollegengeschenk.", ["berufe","buero","excel","kalender","pflege","handwerk","lehrer","elektrik","lager"], None),
 ("ki-humor", "KI-Shirts für Menschen", "Für alle, die noch selbst denken, selbst schreiben und trotzdem jedes Captcha verkacken. Humor fürs KI-Zeitalter.", [" ki ","ki-spruch","ki spruch","ai shirt","generiert","captcha"], None),
]

# ---------- 6 Alte Meister ----------
C = "https://cdn.shopify.com/s/files/1/1097/9475/4900/files/"
KUNST = [("kunst01","Ich hab heute schon mit Menschen geredet.","Rembrandt van Rijn, Selbstbildnis, 1660"),
         ("kunst02","Ich hab's gehört. Ich reagier nur nicht.","Petrus Christus, Bildnis eines Kartäusers, 1446"),
         ("kunst03","Keiner hat gefragt. Ich spiel trotzdem.","Guillaume Voiriot, Monsieur Aublet, um 1782"),
         ("kunst04","Ich bin nicht arrogant. Ich steh nur so.","Bronzino, Bildnis eines jungen Mannes, 1530er"),
         ("kunst05","Ich warte seit 1490 auf einen Rückruf.","Jacometto Veneziano, Bildnis eines Mannes, um 1490")]
AM_HTML = """<div class="hb" id="hb-am" style="max-width:1100px">
<p class="big center" style="font-size:40px">Alte Meister, neue Probleme</p>
<p class="center">Große Kunst, ehrliche Gefühle. Wir haben berühmte Gemälde aus fünf Jahrhunderten gefragt, wie es ihnen heute so geht.</p>
<div class="grid" style="grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:26px;margin-top:24px">""" + "".join(
f"""<figure style="margin:0;background:#F5F0E4;border:3px solid #141414;padding:14px;box-shadow:6px 6px 0 #141414"><img loading="lazy" src="{C}{k}_hell_brust.png?width=700" alt="{s}" style="width:100%;display:block"><figcaption style="border-top:2px solid #B08D4A;margin-top:10px;padding-top:8px;font-size:13px"><b>{s}</b><br><span class="muted">{w}</span></figcaption></figure>""" for k,s,w in KUNST) + """</div>
<div class="box"><h2>Die Shirts kommen in Kürze</h2><p>Die Kollektion ist gerade in Produktion. Trag dich für die <a href="/pages/geburtstags-erinnerung">Erinnerungs-E-Mails</a> ein, dann erfährst du es als Erstes.</p>
<p class="muted">Alle Gemälde sind gemeinfrei und stammen aus der Open-Access-Sammlung des Metropolitan Museum of Art (CC0). Die Sprüche und die Gestaltung sind von Halbernst.</p></div>
<div id="am-out"></div></div>"""
AM_JS = r"""HB.load().then(function(P){var r=P.filter(function(p){return HB.text(p).indexOf('kunst-t-shirt')>=0;});if(r.length)document.getElementById('am-out').innerHTML='<h2>Jetzt erhältlich</h2><div class="grid">'+r.map(function(p){return HB.card(p);}).join('')+'</div>';});"""

# ---------- 7 App-Seite ----------
APP_HTML = """<div class="hb" id="hb-app">
<p class="big center" style="font-size:44px">Die Halbernst-App</p>
<p class="center" style="font-size:18px">Geburtstage merken, Glückwünsche schreiben, das passende Geschenk finden. Und zwischendurch über Sprüche abstimmen. Alles in einer App, alles mit Humor.</p>
<p class="center"><span class="hint" style="display:inline-block">📱 Die App für Android ist in Arbeit. Bis dahin kannst du alles direkt hier im Browser nutzen.</span></p>
<div class="grid" style="grid-template-columns:repeat(auto-fill,minmax(220px,1fr));margin-top:20px">
<a class="card" href="/pages/geschenk-finder" style="padding:16px"><span style="font-size:40px;padding:0">🎁</span><b style="padding:6px 0;font-size:18px">Geschenk-Finder</b><span style="padding:0">Das passende Shirt in 20 Sekunden.</span></a>
<a class="card" href="/pages/glueckwunsch" style="padding:16px"><span style="font-size:40px;padding:0">💬</span><b style="padding:6px 0;font-size:18px">Glückwunsch-Generator</b><span style="padding:0">Lustig, lieb oder frech, als Bild oder per WhatsApp.</span></a>
<a class="card" href="/pages/geburtstags-erinnerung" style="padding:16px"><span style="font-size:40px;padding:0">⏰</span><b style="padding:6px 0;font-size:18px">Geburtstags-Erinnerung</b><span style="padding:0">Wir sagen rechtzeitig Bescheid.</span></a>
<a class="card" href="/pages/spruch-des-tages" style="padding:16px"><span style="font-size:40px;padding:0">👍</span><b style="padding:6px 0;font-size:18px">Spruch des Tages</b><span style="padding:0">Abstimmen, was aufs nächste Shirt kommt.</span></a>
<a class="card" href="/pages/alte-meister" style="padding:16px"><span style="font-size:40px;padding:0">🖼</span><b style="padding:6px 0;font-size:18px">Alte Meister</b><span style="padding:0">Berühmte Gemälde, neue Probleme.</span></a>
<a class="card" href="/pages/anlaesse" style="padding:16px"><span style="font-size:40px;padding:0">🎉</span><b style="padding:6px 0;font-size:18px">Anlässe</b><span style="padding:0">Weihnachten, Silvester, runde Geburtstage und mehr.</span></a>
</div>
<div class="box"><h2>In der App kommt noch dazu</h2><ul><li>Geburtstage aus deinen Kontakten übernehmen</li><li>Push-Erinnerung mit Bestellfrist-Ampel</li><li>WhatsApp-Sticker-Packs</li><li>Lückentext-Partyspiel und Ragebait-Generator</li></ul>
<p>Willst du Bescheid bekommen, wenn sie da ist? <a href="/pages/geburtstags-erinnerung">Hier eintragen</a>.</p></div>
</div>"""

# Übersichtsseite Anlässe
UEB_HTML = """<div class="hb"><p class="big center" style="font-size:40px">Anlässe</p><p class="center">Für jeden Anlass der passende Spruch.</p><div class="grid" style="grid-template-columns:repeat(auto-fill,minmax(220px,1fr))">""" + "".join(
f"""<a class="card" href="/pages/{k}" style="padding:16px"><span style="font-size:44px;padding:0 0 6px;line-height:1">{EMOJI[k]}</span><b style="padding:0 0 6px;font-size:18px">{t}</b><span style="padding:0">{i[:90]}…</span></a>""" for k,t,i,_,_ in ANLAESSE) + "</div></div>"

pages = {}
pages["geschenk-finder"] = ("Geschenk-Finder", page("geschenk-finder", FINDER_HTML, FINDER_JS))
pages["glueckwunsch"] = ("Glückwunsch-Generator", page("glueckwunsch", GW_HTML, GW_JS))
pages["spruch-des-tages"] = ("Spruch des Tages", page("spruch-des-tages", VOTE_HTML, VOTE_JS))
pages["geburtstags-erinnerung"] = ("Geburtstags-Erinnerung", page("geburtstags-erinnerung", ER_HTML, ER_JS))
pages["alte-meister"] = ("Alte Meister, neue Probleme", page("alte-meister", AM_HTML, AM_JS))
pages["app"] = ("Die Halbernst-App", CSS + APP_HTML)
pages["anlaesse"] = ("Anlässe", CSS + UEB_HTML)
for k, t, i, kw, suf in ANLAESSE:
    h, j = anlass_page(k, t, i, kw, suf)
    pages[k] = (t, page(k, h, j))
open(f"{OUT}/app.html", "w").write(pages["app"][1]); open(f"{OUT}/anlaesse.html", "w").write(pages["anlaesse"][1])
json.dump({k: {"title": t, "body": b} for k, (t, b) in pages.items()}, open(f"{OUT}/pages.json", "w"), ensure_ascii=False)
print({k: len(b) for k, (t, b) in pages.items()})

# ---------- Bündel: eine JS-Datei für alle Seiten ----------
parts = {}
parts["geschenk-finder"] = (FINDER_HTML, FINDER_JS)
parts["glueckwunsch"] = (GW_HTML, GW_JS)
parts["spruch-des-tages"] = (VOTE_HTML, VOTE_JS)
parts["geburtstags-erinnerung"] = (ER_HTML, ER_JS)
parts["alte-meister"] = (AM_HTML, AM_JS)
parts["app"] = (APP_HTML, "")
parts["anlaesse"] = (UEB_HTML, "")
for k, t, i, kw, suf in ANLAESSE:
    parts[k] = anlass_page(k, t, i, kw, suf)
css_inner = CSS.replace("<style>", "").replace("</style>", "")
bundle = "(function(){var st=document.createElement('style');st.textContent=" + json.dumps(css_inner) + ";document.head.appendChild(st);" + JS_BASE + "var P={};"
for k, (h, j) in parts.items():
    bundle += "P[" + json.dumps(k) + "]={h:" + json.dumps(h, ensure_ascii=False) + ",j:function(){" + j + "}};"
bundle += "function run(){document.querySelectorAll('[data-hb-page]').forEach(function(r){var p=P[r.getAttribute('data-hb-page')];if(!p)return;r.innerHTML=p.h;try{p.j();}catch(e){console.error('Halbernst',e);}});}if(document.readyState=='loading')document.addEventListener('DOMContentLoaded',run);else run();})();"
open(f"{OUT}/halbernst-tools.js", "w").write(bundle)
print("bundle", len(bundle))

#!/bin/bash
# usage: batch.sh N  (0-based batch, 30 per batch)
set -e
N=$1; cd /home/claude/designs
python3 - $N <<'PY'
import json,sys,subprocess,os
n=int(sys.argv[1]); r=json.load(open('upload_plan.json'))[n*30:(n+1)*30]
os.makedirs('/home/claude/halbernst-druckdateien/neu-png',exist_ok=True)
for x in r:
  for v in ('hell','dunkel'):
    i=x['id']; out=f"/home/claude/halbernst-druckdateien/neu-png/{i:03d}_{v}_brust.png"
    if not os.path.exists(out): subprocess.run(['rsvg-convert','-w','4500','-h','5400','-o',out,f"neu/{i:03d}_{v}_brust.svg"],check=True)
json.dump(r,open(f'/home/claude/halbernst-druckdateien/neu-png/batch{n}.json','w'),ensure_ascii=False)
print(len(r), r[0]['id'], r[-1]['id'])
PY
cd /home/claude/halbernst-druckdateien && git add neu-png && git commit -qm "Druckdateien Batch $N

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01Li3JrNhoKLzAoMQpcKxzBQ" && git pull -q --rebase && git push -q && echo pushed

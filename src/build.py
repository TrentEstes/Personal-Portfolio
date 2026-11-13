import json, sys
sys.path.insert(0,'src')
from content import P, POSTERS
names=[l.strip() for l in open('image-list.txt') if l.strip()]
def res(pfx):
    if pfx is None or '.' in pfx: return pfx
    m=[n for n in names if n.startswith(pfx)]
    assert len(m)==1,(pfx,m); return m[0]
out=[]
big=[p for p in P if p.get('size')=='big']; small=[p for p in P if p.get('size')!='big']
for p in P:
    q=dict(p); q.setdefault('size','small'); q['cover']=res(p.get('coverimg') or p.get('cover')); q.pop('coverimg',None)
    q['rows']=[[res(x) for x in r] if isinstance(r,list) else r for r in p['rows']]
    out.append(q)
pos=[dict(f=res(f),t=t,n=n,s=s,ar=ar) for f,t,n,s,ar in POSTERS]
# ---- structured data (schema.org) + sitemap -------------------------------
import datetime
SU="https://trente.design/"
person={"@type":"Person","@id":SU+"#trent","name":"Trent Estes","url":SU,
        "jobTitle":"Brand and Packaging Designer",
        "description":"Brand and packaging designer working in brand identity, packaging systems, lettering and poster design.",
        "email":"mailto:hello@trente.design",
        "address":{"@type":"PostalAddress","addressRegion":"VA","addressCountry":"US"},
        "sameAs":["https://www.linkedin.com/in/trent-estes-0a538b300/"],
        "knowsAbout":["Brand identity","Packaging design","Typography","Lettering","Art direction","Poster design","Consumer packaged goods"]}
website={"@type":"WebSite","@id":SU+"#site","name":"Trent Estes","url":SU,
         "inLanguage":"en","author":{"@id":SU+"#trent"},"publisher":{"@id":SU+"#trent"}}
items=[{"@type":"ListItem","position":i+1,"item":{"@type":"CreativeWork","name":q["title"],
        "description":q.get("kind") or q.get("sub") or "","url":SU+"#"+q["slug"],
        "creator":{"@id":SU+"#trent"},"isPartOf":{"@id":SU+"#site"}}}
       for i,q in enumerate(out) if q.get("slug")]
graph={"@context":"https://schema.org","@graph":[person,website,
       {"@type":"ItemList","name":"Selected work","itemListElement":items}]}
jsonld=json.dumps(graph,ensure_ascii=False,separators=(",",":")).replace("</","<\\/")
today=datetime.date.today().isoformat()
urls=[(SU,"weekly","1.0"),(SU+"bbx-01/","monthly","0.6")]
sm='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
for u,cf,pr in urls:
    sm+=f'  <url><loc>{u}</loc><lastmod>{today}</lastmod><changefreq>{cf}</changefreq><priority>{pr}</priority></url>\n'
sm+='</urlset>\n'
open('sitemap.xml','w').write(sm)
src=open('src/page.html').read().replace('/*__PROJECTS__*/[]', json.dumps(out,ensure_ascii=False,indent=0)).replace('/*__POSTERS__*/[]', json.dumps(pos,ensure_ascii=False)).replace('/*__JSONLD__*/', jsonld)
open('src/artifact.html','w').write(src)
head_end=src.index('</style>')+len('</style>')
head,body=src[:head_end],src[head_end:]
doc='<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'+head.replace('<meta name="claude:viewport-fit-sides" content="cover">\n','')+'\n</head>\n<body>\n'+body.strip()+'\n</body>\n</html>\n'
open('index.html','w').write(doc)
used=set([q['cover'] for q in out if q['cover'] and '?' in q['cover']]+[x for q in out for r in q['rows'] if isinstance(r,list) for x in r if '?' in x])
pass  # image-list.txt is the master list; don't overwrite
print('ok', len(used))

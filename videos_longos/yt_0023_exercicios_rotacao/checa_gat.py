"""Lista os gat("frase") do código que NÃO existem na narração nova (por âncora), com a fala da âncora para remapear."""
import re, json, glob, sys
fala = {p['id']: re.findall(r'\w+', p['texto'].lower()) for p in json.load(open('audio/paragrafos.json', encoding='utf-8'))}
miss, tot, ok = [], 0, 0
for f in sorted(glob.glob('sec_*.py')):
    aid = None
    for n, ln in enumerate(open(f, encoding='utf-8'), 1):
        m = re.search(r'self\.an\("([^"]+)"\)', ln)
        if m: aid = m.group(1)
        for g in re.finditer(r'self\.gat\((?:"([^"]+)"|\'([^\']+)\')\)', ln):
            fr = g.group(1) or g.group(2); tot += 1
            alvo = re.findall(r'\w+', fr.lower()); w = fala.get(aid, [])
            if any(w[i:i + len(alvo)] == alvo for i in range(len(w))): ok += 1
            else: miss.append((f, n, aid, fr))
print(f'{tot} gat; {ok} achados; {len(miss)} faltam')
if '-v' in sys.argv:
    cur = None
    for f, n, aid, fr in miss:
        if aid != cur:
            cur = aid; print(f'\n## {aid}: ' + ' '.join(fala.get(aid, [])))
        print(f'  {f}:{n}  {fr!r}')

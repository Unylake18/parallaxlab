import re, json, sys
src = open('narracao_final_fonte.md', encoding='utf-8').read()
pars = []
for m in re.finditer(r'^\{([^}]+)\} (.+)$', src, flags=re.M):
    pars.append((m.group(1), m.group(2).strip()))
print(len(pars), 'ancoras', sum(len(re.sub(r'\[[^\]]*\]\s*','',t).split()) for _, t in pars), 'palavras')
json.dump([{'id': i, 'texto': re.sub(r'\[[^\]]*\]\s*', '', t)} for i, t in pars], open('audio/paragrafos.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
def md(sel, nome):
    corpo = '\n\n'.join(t for i, t in pars if sel(i))
    open(nome, 'w', encoding='utf-8').write('# yt_0023 narração (gravação)\n\n## Texto corrido (para gravação)\n\n' + corpo + '\n')
md(lambda i: True, 'narracao_tags_v3.md')
md(lambda i: i in ('H1', 'E1-9', 'E3-7'), 'narracao_teste_v3.md')

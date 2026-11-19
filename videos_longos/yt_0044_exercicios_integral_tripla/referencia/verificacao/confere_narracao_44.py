# Confere a narração do yt_0044: palavras por âncora (3 p/s + 0,15 s + 0,35 s) e gatilhos como tokens contíguos, na ordem.
import re,sys
p=sys.argv[1] if len(sys.argv)>1 else 'yt_0044_narracao_v1.md'; t=open(p,encoding='utf-8').read()
toks=lambda s: re.findall(r"[\wÀ-ÿ']+",s.lower())
rows=[];bad=0;ng=0
for sec in re.split(r'\n### ',t)[1:]:
    head=sec.split('\n')[0]
    if head.startswith('Tempo'): continue
    fala=re.sub(r'\[[a-z ,]+\]','',' '.join(l[2:] for l in sec.split('\n') if l.startswith('> ')))
    ft=toks(fala); rows.append((head,len(ft),0.15+len(ft)/3+0.35))
    g=re.search(r'\*\*Gatilhos:\*\*(.*)',sec); pos=0
    for f in (re.findall(r'"([^"]+)"',g.group(1)) if g else []):
        ng+=1; fk=toks(f); hit=next((i for i in range(pos,len(ft)-len(fk)+1) if ft[i:i+len(fk)]==fk),-1)
        if hit<0: bad+=1; print('FALTA/ORDEM',head,'::',f)
        else: pos=hit+len(fk)
tab='| Âncora | Palavras | Tempo |\n|---|---:|---:|\n'+''.join(f'| {h} | {w} | {int(s//60)}:{s%60:04.1f} |\n' for h,w,s in rows)
W=sum(r[1] for r in rows);T=sum(r[2] for r in rows)
tab+=f'| **Total** | **{W:,}**'.replace(',','.')+f' | **≈ {int(T//60)}:{T%60:02.0f}** |\n'
print(tab); print('gatilhos',ng,'faltando',bad)
if '--grava' in sys.argv:
    t=re.sub(r'(### Tempo por âncora\n\n)(.*?)(\n---\n)',lambda m:m.group(1)+tab+f'\nContagem por script (`verificacao/confere_narracao_44.py`): palavras sem as tags; 0,15 s + palavras/3 + 0,35 s por âncora, a 3 palavras/s. {ng} gatilhos conferidos como tokens contíguos da fala, na ordem ({bad} faltando).\n'+m.group(3),t,count=1,flags=re.S)
    open(p,'w',encoding='utf-8').write(t)

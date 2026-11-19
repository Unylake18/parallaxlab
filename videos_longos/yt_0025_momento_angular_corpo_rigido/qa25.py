"""Consolida medições reais; nunca converte falhas em aprovação automaticamente."""
import json,re
from collections import Counter,defaultdict
from pathlib import Path
import av
import numpy as np
from PIL import Image,ImageDraw,ImageFont

U=Path(__file__).resolve().parent
LOTES=['PH','PB1','PB2','PB3','PB4','PB5','PB6','PS']
R=U/'renders';Q=U/'qa'
def le(p):return json.loads(p.read_text(encoding='utf-8'))
def salva(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=1),encoding='utf-8')

def consolidar():
    an=le(U/'ancoras.json')['ancoras'];off=le(U/'offsets.json');unicos=defaultdict(list);cats=Counter();dur=[];algebra={}
    fontes={}
    patches=le(U/'patches.json') if (U/'patches.json').exists() else []
    for l in LOTES:
        texto=(U/f'log_aud_{l}.txt').read_text(encoding='utf-8',errors='replace')
        intervalos=[(p['quadro_inicial']/15,(p['quadro_inicial']+p['quadros'])/15,p) for p in patches if p['lote']==l]
        auditorias=[(float(t),s) for t,s in re.findall(r'\[audit\]\s+([0-9.]+)s (.+)',texto) if not any(a<=float(t)<b for a,b,p in intervalos)]
        for a,b,p in intervalos:
            pl=U/f"log_correcao_{p['ancora']}.txt"
            if pl.exists():auditorias += [(float(t),s) for t,s in re.findall(r'\[audit\]\s+([0-9.]+)s (.+)',pl.read_text(encoding='utf-8',errors='replace')) if a<=float(t)<b]
        fontes[l]={fase:re.findall(r'\[fonte\] (\w+)',(U/f'log_{pre}{l}.txt').read_text(encoding='utf-8',errors='replace')) for fase,pre in [('render',''),('auditoria','aud_')]}
        for t,s in auditorias:
            categoria=re.split(r" '| [a-z0-9(]",s,maxsplit=1)[0]
            cats[(l,categoria)]+=1
            unicos[(l,re.sub(r'[-+]?\d+\.\d+','N',s))].append(float(t))
        tt=le(U/f'tempos_{l}.json');it=list(tt['inicios'].items())
        for i,(a,t) in enumerate(it):
            fim=it[i+1][1] if i+1<len(it) else tt['total'];fala=an[a]['palavras']/2.7
            dur.append(dict(ancora=a,lote=l,inicio_global=off[l]+t,cena=fim-t,fala_estimada=fala,hold=an[a]['hold'],folga=fim-t-fala))
        alg=le(U/f'algebra_{l}.json');gm=sum(x['metodo']=='GM' for x in alg)
        n=sum(x['grandezas'] for x in alg);c=sum(x['coloridos'] for x in alg)
        algebra[l]=dict(transformacoes_GM=gm,grandezas=n,coloridas=c,fracao_colorida=c/n if n else None,
            operadores_incorretos=[x for x in alg if x['operadores_incorretos']],fontes_menores46=[x for x in alg if x['font_size']<45.5])
        tp=Q/f'telemetria_{l}.json'
        if tp.exists():
            tele=le(tp);dd=tele['densidade'];total=sum(x['glifos'] for x in dd);familia=sum(x.get('familia',0) for x in dd)
            mt=sum(x.get('math_total',0) for x in dd);mf=sum(x.get('math_familia',0) for x in dd)
            algebra[l].update(cor_todo_texto=familia/total if total else None,cor_math=mf/mt if mt else None,flash_candidatos=tele['flash_candidatos'])
    linhas=[f'{l} {min(ts):7.1f}–{max(ts):7.1f}s x{len(ts):4} {s}' for (l,s),ts in sorted(unicos.items())]
    (R/'portao_unico.txt').write_text('\n'.join(linhas)+'\n',encoding='utf-8')
    portas={l:le(Q/f'portao_{l}.json') for l in LOTES if (Q/f'portao_{l}.json').exists()}
    resumo=dict(ocorrencias=sum(cats.values()),categorias=[dict(lote=l,categoria=c,n=n) for (l,c),n in sorted(cats.items())],fontes=fontes,algebra=algebra,duracoes=dur,mascaras_oclusao=portas,substituicoes=patches)
    salva(Q/'resumo.json',resumo)
    texto=['PREVIEW yt_0025 — MEDIÇÕES E PENDÊNCIAS','Fase: preview silencioso; tempos de fala estimados a 2,7 palavras/s.',
        f'Portão bruto: {sum(cats.values())} ocorrências repetidas; {len(unicos)} grupos.','Os grupos não são classificados como falsos positivos sem inspeção.','',
        'DURAÇÃO POR ÂNCORA (s): cena / fala estimada / hold / folga']
    texto += [f"{d['ancora']:6} {d['cena']:6.2f} / {d['fala_estimada']:6.2f} / {d['hold']:.1f} / {d['folga']:+6.2f}" for d in dur]
    texto+=['','SUBSTITUIÇÕES LOCAIS','O portão usa o log do trecho substituto dentro da sua faixa; o restante usa a auditoria do lote base.',json.dumps(patches,ensure_ascii=False,indent=1)]
    texto+=['','PORTÃO POR LOTE/CATEGORIA']+[f'{l} {c}: {n}' for (l,c),n in sorted(cats.items())]
    texto+=['','ÁLGEBRA (contagem real de eventos GM; cor só dos glifos identificados)']+[f'{l}: {v}' for l,v in algebra.items()]
    texto+=['','MÁSCARAS E OCLUSÃO (segmentos checados, não apenas presença do recurso)',json.dumps(portas,ensure_ascii=False,indent=1)]
    for p in [Q/'fisica.json',Q/'alinhamento.json',Q/'parado.json',Q/'fundo.json',Q/'objetos_raster.json']:
        if p.exists():texto+=['',p.name,p.read_text(encoding='utf-8')]
    exc=Q/'excecoes_layout.md'
    if exc.exists():texto+=['','EXCEÇÕES EXPLÍCITAS',exc.read_text(encoding='utf-8')]
    (R/'qa.txt').write_text('\n'.join(texto)+'\n',encoding='utf-8')
    print(f'{sum(cats.values())} ocorrências, {len(unicos)} grupos; {len(dur)} âncoras')

def quadros():
    """Quadros nativos; pranchas são índices, os originais ficam ao lado."""
    q=le(R/'quadros.json');dest=R/'quadros_qa';dest.mkdir(exist_ok=True)
    chaves=['H2','H3','B1-2','B1-3','B1-5','B1-6','B2-3','B2-4','B3-3','B3-4','B3-5','B3-7','B4-1','B4-3','B5-2','B5-3','B5-4','B6-2','B6-5','S1']
    alvos=defaultdict(list);porlote=defaultdict(list);off=le(U/'offsets.json');densos_meta=[]
    for l in LOTES:
        t=le(U/f'tempos_{l}.json');it=list(t['inicios'].items())
        for i,(a,x) in enumerate(it):
            fim=it[i+1][1] if i+1<len(it) else t['total']
            for fracao in ([.35,.65,.88] if a in ('B3-3','B3-4') else [.9] if a in ('H2','B1-2') else [.7]):
                f=round((off[l]+x+(fim-x)*fracao)*15);nome=a+(f'_{int(fracao*100)}' if a in ('B3-3','B3-4') else '')
                alvos[f].append((nome,l,a));porlote[l].append(nome)
            if a=='B2-4':
                f=round((off[l]+x+1.4)*15);alvos[f].append(('B2-4_onda',l,a));porlote[l].append('B2-4_onda')
            if a=='S1':
                alg=le(U/'algebra_PS.json');tt=max(z['t'] for z in alg if z['ancora']=='S1')
                f=round((off[l]+tt)*15);alvos[f].append(('S1_3_leis',l,a));porlote[l].append('S1_3_leis')
        p=Q/f'telemetria_{l}.json'
        if p.exists():
            pora=defaultdict(list)
            for row in le(p)['densidade']:pora[row['ancora']].append(row)
            for a,rows in pora.items():
                maior=max(x['glifos'] for x in rows);plat=[x for x in rows if x['glifos']==maior];d=plat[len(plat)//2]
                densos_meta.append((d['glifos'],d['area'],a,l,round(off[l]*15)+d['quadro']))
    densos_meta=sorted(densos_meta,reverse=True)[:24]
    for ng,area,a,l,f in densos_meta:alvos[f].append((a+'_denso',l,a))
    candidatos=[];c=av.open(str(R/'preview_yt0025_v1_960x540.mp4'))
    for i,f in enumerate(c.decode(video=0)):
        if i not in alvos:continue
        im=Image.fromarray(f.to_ndarray(format='rgb24'))
        for nome,l,a in alvos[i]:im.save(dest/f'{nome}.png')
        # Quantidade de tinta clara na área útil: seleção reproduzível, seguida por inspeção humana.
        arr=np.asarray(im);tinta=int((arr[100:490].min(2)>150).sum());candidatos.append((tinta,nome,i,l,a))
    c.close()
    densos=sorted(candidatos,reverse=True)[:24];salva(Q/'quadros_selecionados.json',dict(densidade_telemetria=densos_meta,densidade_raster=densos,chaves=chaves))
    def prancha(nomes,saida):
        w,h=480,294;out=Image.new('RGB',(w*3,h*((len(nomes)+2)//3)),'#08122b');d=ImageDraw.Draw(out)
        for j,n in enumerate(nomes):
            im=Image.open(dest/f'{n}.png');im.thumbnail((480,270));x,y=(j%3)*w,(j//3)*h;out.paste(im,(x,y));d.text((x+8,y+273),n,fill='white')
        out.save(saida)
    for l,ns in porlote.items():prancha(ns,R/f'prancha_{l}.png')
    prancha([x[2]+'_denso' for x in densos_meta] if densos_meta else [x[1] for x in densos],R/'prancha_24_densos.png')
    print(f'{len(alvos)} quadros nativos, 8 pranchas e 24 candidatos densos')

if __name__=='__main__':
    import sys
    quadros() if '--quadros' in sys.argv else consolidar()

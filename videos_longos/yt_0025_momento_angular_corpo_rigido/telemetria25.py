"""Presença de texto em quadros consecutivos, independente do teste G28 a cada 3."""
import json
from manim import Text,SingleStringMathTex
from kit import AQUI,FPS

def medir(c):
    f=round(c.clk.get_value()*FPS)
    if getattr(c,'_vis25_f',None)==f:return
    c._vis25_f=f
    if not hasattr(c,'_vis25'):c._vis25={};c._dens25=[]
    fixos=c.fixos();voando=getattr(c,'_voando',set())|{id(x) for g in getattr(c,'_voando_raiz',[]) for x in g.get_family()}
    vistos=set();textos_vivos=set();glifos=0;area=0;familia=0;mat_total=0;mat_familia=0
    paleta={'#D2823A','#FF7EB6','#9C8CFF','#5AA2FF','#3FE08B','#FFC24D','#F19AFF','#EA63FF'}
    def walk(m):
        nonlocal glifos,area,familia,mat_total,mat_familia
        if id(m) in vistos or id(m) in voando:return
        vistos.add(id(m))
        if isinstance(m,(Text,SingleStringMathTex)):
            folhas=m.family_members_with_points()
            ops=[max(float(x.get_fill_opacity()),float(x.get_stroke_opacity())) for x in folhas]
            if not ops or max(ops)<.15 or m.width<.01:return
            tex=getattr(m,'text',None) or m.tex_string
            chave=tex
            textos_vivos.add(tex)
            c._vis25.setdefault(chave,set()).add(f)
            glifos+=sum(o>=.15 for o in ops);area+=float(m.width*m.height)
            coloridos=sum(x.get_fill_color().to_hex().upper() in paleta for x,o in zip(folhas,ops) if o>=.15)
            familia+=coloridos
            if isinstance(m,SingleStringMathTex):mat_total+=sum(o>=.15 for o in ops);mat_familia+=coloridos
            return
        for x in m.submobjects:walk(x)
    for m in c.mobjects:
        if m not in fixos:walk(m)
    linha=getattr(c,'_linha_em_construcao25',None)
    if linha is not None and linha.tex_string not in textos_vivos:
        # As partes de uma linha já são visíveis antes de se assentarem na MathTex inteira.
        presentes={id(x) for m in c.mobjects for x in m.family_members_with_points()}
        folhas=[x for x in linha.family_members_with_points() if id(x) in presentes and max(float(x.get_fill_opacity()),float(x.get_stroke_opacity()))>=.15]
        if folhas:
            c._vis25.setdefault(linha.tex_string,set()).add(f)
            n=len(folhas);col=sum(x.get_fill_color().to_hex().upper() in paleta for x in folhas)
            glifos+=n;familia+=col;mat_total+=n;mat_familia+=col
    c._dens25.append(dict(quadro=f,ancora=c._aid,glifos=glifos,area=area,familia=familia,math_total=mat_total,math_familia=mat_familia))

def salvar(c):
    out=[];flash=[]
    por_quadro={x['quadro']:x['ancora'] for x in getattr(c,'_dens25',[])}
    for tex,fs in getattr(c,'_vis25',{}).items():
        fs=sorted(fs);runs=[];ini=ant=fs[0]
        for f in fs[1:]:
            if f>ant+1:runs.append((ini,ant));ini=f
            ant=f
        runs.append((ini,ant))
        row=dict(ancoras=sorted({por_quadro[f] for f in fs}),tex=tex,intervalos=runs);out.append(row)
        for i,j in runs:
            if j-i+1<.7*FPS:flash.append(dict(ancora=por_quadro[i],tex=tex,inicio=i/FPS,duracao=(j-i+1)/FPS))
    (AQUI/f'qa/telemetria_{c.lote}.json').write_text(json.dumps(dict(textos=out,flash_candidatos=flash,densidade=getattr(c,'_dens25',[])),ensure_ascii=False),encoding='utf-8')

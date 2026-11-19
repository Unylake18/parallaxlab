"""Portões v4 do yt_0025 (handoff v4 §3): TAMANHO (grupo objeto+vetores, planos), CONTRASTE, RESÍDUO e CADÊNCIA, medidos no vídeo do lote e nas máscaras do Three.js.
uso: python gates25.py LOTE [tamanho|contraste|residuo|todos]
saídas: qa/tamanho_LOTE.txt, qa/contraste_LOTE.txt, qa/residuo_LOTE.txt"""
import json,re,sys
from pathlib import Path
import av,numpy as np
from PIL import Image
from scipy.ndimage import binary_dilation,binary_erosion

U=Path(__file__).resolve().parent
lote=sys.argv[1];modo=sys.argv[2] if len(sys.argv)>2 else 'todos'
mp4=U/f'media_{lote}/videos/cena/540p15/{lote}.mp4'
tempos=json.loads((U/f'tempos_{lote}.json').read_text(encoding='utf-8'))['inicios']
anc=json.loads((U/'ancoras.json').read_text(encoding='utf-8'))['ancoras']
FPS=15.0
ZX0,ZX1,ZY0,ZY1=0,960,120,492          # zona útil do palco (y de −3,7 a 2,5 u em 540 px); a largura da coluna esquerda vale 423 px
COLUNA=423.0;ALTURA=372.0
frames=None
def carrega():
    global frames
    if frames is None:
        c=av.open(str(mp4));frames=[f.to_ndarray(format='rgb24') for f in c.decode(video=0)]
    return frames
def tipo_de(aid):
    if aid in ('S1',) or aid[0] in 'HA':return 'bancada_dupla'
    if aid in ('S2',):return 'plataforma_livre'
    if aid=='EN':return None
    b=aid.split('-')[0]
    if b=='B1':return 'pendulo_conico'
    if b=='B2' or aid=='B4-3':return 'corpo_voxel'
    if b=='B6':return 'roda_balanceamento'
    return 'haltere_torto'
def mascara(k,aid=None):
    base=U/'threejs'/'q3d'/f'{lote}_960x540'
    if not base.exists():return None,None
    melhor=None
    tipos=[tipo_de(aid)] if aid else sorted(p.name for p in base.iterdir() if p.is_dir())
    for tipo in tipos:
        if tipo is None:continue
        arq=base/tipo/'mascaras'/f'f{k:05d}.png'
        if arq.exists():
            m=np.asarray(Image.open(arq).convert('L'))>127
            if melhor is None or m.sum()>melhor[1].sum():melhor=(tipo,m)
    return melhor if melhor else (None,None)
def amostras():
    out=[]
    for aid,t0 in tempos.items():
        d=anc[aid]['dur']
        for f in (.1,.3,.5,.7,.9):out.append((aid,t0+f*d))
    return out
def lum(rgb):
    c=rgb.astype(np.float64)/255.0;c=np.where(c<=.04045,c/12.92,((c+.055)/1.055)**2.4)
    return .2126*c[...,0]+.7152*c[...,1]+.0722*c[...,2]

PLANO=eval(re.search(r"^PLANO=(\{.*?\})\n",(U/'cenas25.py').read_text(encoding='utf-8').replace('\r\n','\n'),re.S|re.M).group(1))
def tipo_plano(aid,f):
    """GERAL / CLOSE / ESPECIAL (TOPO, AXIAL, MANCAL) / None (em transição) na fração f da âncora, pelo PLANO de cenas25.py."""
    seg=PLANO.get(aid)
    if not seg:return 'GERAL'
    ativo=None
    for ini,fim,cam in seg:
        if f>=fim:ativo=cam
        elif f>=ini:return None
    if ativo is None:return 'GERAL' if seg[0][0]>0 else None
    return 'CLOSE' if ativo.endswith('CLOSE') else ('GERAL' if ativo.endswith('34') else 'ESPECIAL')
def magenta(img,mask_zona):
    """vetores L magenta do Manim dentro da coluna esquerda (cor LMAG ≈ #EA63FF); junta ao objeto 3D para o grupo 'objeto + vetores'."""
    r,g,b=[img[...,i].astype(int) for i in range(3)]
    m=(r>190)&(b>190)&(g<150)&(r-g>80)
    m[:, 450:]=False;m[:ZY0,:]=False;m[ZY1:,:]=False
    return m
def tamanho():
    linhas=[];falhas=0;por={}
    fr=carrega()
    for aid,t in amostras():
        d=anc[aid]['dur'];f=(t-tempos[aid])/d
        k=int(round(t*FPS));tipo,m=mascara(k,aid)
        if m is None or k>=len(fr):continue
        modo=tipo_plano(aid,f)
        if modo is None:continue
        ys,xs=np.where(m)
        if len(ys)<50:continue
        y0,y1,x0,x1=ys.min(),ys.max(),xs.min(),xs.max()
        ymeio=y0+int(.6*(y1-y0))              # CLOSE: só as linhas do objeto (60 % superiores) contam para corte lateral; o suporte pode sair
        lado_corte=bool((m[y0:ymeio+1,:2].any()) or (m[y0:ymeio+1,958:].any()))
        mg=magenta(fr[k],None);yg,xg=np.where(mg)
        if len(yg)>40:gy0,gy1,gx0,gx1=min(y0,yg.min()),max(y1,yg.max()),min(x0,xg.min()),max(x1,xg.max())
        else:gy0,gy1,gx0,gx1=y0,y1,x0,x1
        h=(gy1-gy0+1)/ALTURA;w=(gx1-gx0+1)/COLUNA
        por.setdefault(aid,[]).append(dict(t=t,tipo=tipo,modo=modo,h=h,w=w,area=h*w,corte_topo=bool(y0<=ZY0+1),corte_lado=lado_corte if modo=='CLOSE' else bool(x0<=1 or x1>=958),corte_base=bool(y1>=ZY1-1)))
    for aid,v in por.items():
        for modo in ('GERAL','CLOSE','ESPECIAL'):
            vv=[i for i in v if i['modo']==modo]
            if not vv:continue
            hmed=float(np.median([i['h'] for i in vv]));amed=float(np.median([i['area'] for i in vv]));wmax=max(i['w'] for i in vv)
            ct=sum(i['corte_topo'] for i in vv);cl=sum(i['corte_lado'] for i in vv);cb=sum(i['corte_base'] for i in vv)
            ruins=[];avisos=[]
            if modo=='GERAL':
                if not .55<=hmed<=.75:ruins.append(f'altura do grupo {hmed*100:.0f}% fora de 55–75%')
                if amed<.18:ruins.append(f'área do retângulo {amed*100:.0f}% < 18% da coluna')
                if ct or cl or cb:ruins.append(f'objeto cortado pela borda (topo {ct}, lados {cl}, base {cb} de {len(vv)})')
            elif modo=='CLOSE':
                if hmed<.55:ruins.append(f'altura do grupo {hmed*100:.0f}% < 55%')
                if ct or cl:ruins.append(f'objeto/vetores cortados pela borda (topo {ct}, lados {cl} de {len(vv)})')
                if cb:avisos.append(f'suporte sai pela base em {cb}/{len(vv)} amostras (autorizado em CLOSE)')
            else:
                if ct or cl:ruins.append(f'cortado pela borda (topo {ct}, lados {cl} de {len(vv)})')
                avisos.append('plano especial (TOPO/AXIAL/MANCAL): sem critério de altura')
            falhas+=bool(ruins)
            linhas.append(f'  {aid} [{modo}] {vv[0]["tipo"]}: altura {hmed*100:.0f}% largura máx {wmax*100:.0f}% área {amed*100:.0f}% ({len(vv)} amostras)'+((' FALHA: '+'; '.join(ruins)) if ruins else '')+((' · '+'; '.join(avisos)) if avisos else ''))
    cab=f'TAMANHO v4 {lote}: {sum(1 for _ in linhas)} grupos âncora×plano, {falhas} com FALHA'
    txt=chr(10).join([cab]+linhas);(U/'qa'/f'tamanho_{lote}.txt').write_text(txt,encoding='utf-8');print(cab)

def contraste():
    fr=carrega();linhas=[];falhas=0
    for aid,t in amostras():
        k=int(round(t*FPS));tipo,m=mascara(k,aid)
        if m is None or k>=len(fr):continue
        borda=m&~binary_erosion(m,iterations=3);fora=binary_dilation(m,iterations=5)&~binary_dilation(m,iterations=2)
        L=lum(fr[k])
        if borda.sum()<20 or fora.sum()<20:continue
        # pontos mais claros da silhueta (aresta clara conta), contra o fundo logo fora dela
        li=float(np.percentile(L[borda],75));lo=float(np.median(L[fora]))
        r=(li+.05)/(lo+.05)
        falhas+=r<3
        linhas.append(f'  {aid} t={t:6.1f}s {tipo}: contraste {r:.2f}:1'+('' if r>=3 else ' FALHA (< 3:1)'))
    cab=f'CONTRASTE {lote}: {len(linhas)} amostras, {falhas} com FALHA'
    txt='\n'.join([cab]+linhas);(U/'qa'/f'contraste_{lote}.txt').write_text(txt,encoding='utf-8');print(cab)

def residuo():
    """RESÍDUO v4 (handoff v4 §3): só dentro da caixa da linha (± 0,3 u = 18 px, sem invadir as caixas das OUTRAS linhas), em 0,5 s e 1,0 s depois do último glifo.
    (a) tinta clara fora das caixas dos glifos finais; (b) tinta por token diferente da referência (+1,8 s): fantasma/duplicata/glifo meio apagado.
    Estrelas (componentes ≤ 5×5 px) e traços horizontais longos (sublinhado) não contam. Linha que rolou na Pilha (tinta própria ausente) é ignorada e listada à parte."""
    from scipy.ndimage import label as rotula
    fr=carrega();log=(U/f'log_{lote}.txt').read_text(encoding='utf-8',errors='replace')
    ls=[json.loads(x) for x in re.findall(r'\[linha\] (\{.*\})',log)];rel=[];n=0;M=18;rolou=0
    for L in ls:
        if not L['caixas']:continue
        prox=L['t1']+1.85      # a próxima linha empurra a Pilha: medir antes dela
        disp=min(1.8,prox-L['t1']-.05)
        if disp<.35:rolou+=1;continue
        dts=(.5,1.0) if disp>=1.2 else (.3*disp,.65*disp)
        ks=[int(round((L['t1']+dts[0])*FPS)),int(round((L['t1']+dts[1])*FPS)),int(round((L['t1']+disp)*FPS))]
        if ks[1]>=len(fr)-1:continue
        ks[2]=min(ks[2],len(fr)-1)
        xs0=min(c[1] for c in L['caixas']);xs1=max(c[3] for c in L['caixas']);ys0=min(c[2] for c in L['caixas']);ys1=max(c[4] for c in L['caixas'])
        sx0,sx1,sy0,sy1=max(0,xs0-M),min(960,xs1+M),max(0,ys0-M),min(540,ys1+M)
        caixa=np.zeros((sy1-sy0,sx1-sx0),bool)
        def pinta(c,x0,y0,x1,y1,g=4):
            ya,yb,xa,xb=max(0,y0-sy0-g),y1-sy0+g,max(0,x0-sx0-g),x1-sx0+g
            if yb>0 and xb>0 and ya<caixa.shape[0] and xa<caixa.shape[1]:c[max(0,ya):max(0,yb),max(0,xa):max(0,xb)]=True
        for _,x0,y0,x1,y1 in L['caixas']:pinta(caixa,x0,y0,x1,y1)
        for O in ls:                                         # as outras linhas da Pilha não são resíduo desta
            if O is L:continue
            for _,x0,y0,x1,y1 in O['caixas']:pinta(caixa,x0,y0,x1,y1,6)
        ref=fr[ks[2]].mean(axis=2)>80
        prop=np.zeros_like(ref)
        for _,x0,y0,x1,y1 in L['caixas']:prop[max(0,y0-3):y1+3,max(0,x0-3):x1+3]=True
        iref=int((ref&prop).sum());ia=int(((fr[ks[0]].mean(axis=2)>80)&prop).sum())
        if iref<60 or not .6*iref<=ia<=1.6*iref:rolou+=1;continue
        quant=[]
        for kk in ks[:2]:
            faixa=fr[kk].mean(axis=2)[sy0:sy1,sx0:sx1]>150
            sobra=faixa&~caixa
            for r_ in range(sobra.shape[0]):
                if sobra[r_].sum()>.4*sobra.shape[1]:sobra[r_]=False
            lab,nl=rotula(sobra,structure=np.ones((3,3)))
            for i_ in range(1,nl+1):
                yy,xx=np.where(lab==i_)
                if (lab==i_).sum()<4 or (np.ptp(yy)<=5 and np.ptp(xx)<=5):sobra[lab==i_]=False
                elif np.ptp(yy)<=5 and np.ptp(xx)>=20:sobra[lab==i_]=False                       # sublinhado / borda de selo
                elif yy.min()==0 or yy.max()==sobra.shape[0]-1:sobra[lab==i_]=False              # selo acima / primeiros traços da linha seguinte
            quant.append(int(sobra.sum()))
        n+=1
        if max(quant)>=10:rel.append(f"  {L['aid']} t1={L['t1']:.2f}s {L['tex']}: {quant[0]}/{quant[1]} px de tinta fora das caixas dos glifos (0,5 s / 1,0 s)")
        for tok,x0,y0,x1,y1 in L['caixas']:
            bx=(slice(max(0,y0-3),y1+3),slice(max(0,x0-3),x1+3));ir=int(ref[bx].sum())
            if ir<25:continue
            for dt,kk in zip(dts,ks[:2]):
                i_=int((fr[kk].mean(axis=2)>80)[bx].sum())
                if abs(i_-ir)>.22*ir:rel.append(f"  {L['aid']} t1={L['t1']:.2f}s {L['tex']}: token {tok} com tinta {i_} (ref. {ir}) a {dt:.1f} s: possível fantasma/duplicata");break
    cab=f'RESÍDUO v4 {lote}: {n} linhas medidas ({rolou} ignoradas por rolagem), {len(rel)} ocorrências'
    txt='\n'.join([cab]+rel);(U/'qa'/f'residuo_{lote}.txt').write_text(txt,encoding='utf-8');print(cab)

def cadencia():
    """CADÊNCIA: s/glifo médio e mínimo por linha escrita; linhas < 0,20 s/glifo vão para a lista «enxugar a pauta» (decisão da Produção)."""
    log=(U/f'log_{lote}.txt').read_text(encoding='utf-8',errors='replace')
    ls=[json.loads(x) for x in re.findall(r'\[linha\] (\{.*\})',log)];linhas=[];lista=[]
    for L in ls:
        tex=L['tex'].replace('|','');cmds=len(re.findall(r'\\[a-zA-Z]+',tex));resto=len(re.sub(r'\\[a-zA-Z]+|[{}^_ ]','',tex));g=max(1,cmds+resto)
        sg=(L['t1']-L['t0'])/g
        linhas.append(f"  {L['aid']} t0={L['t0']:.1f}s {g:3d} glifos {L['t1']-L['t0']:5.2f}s {sg:.3f} s/glifo  {L['tex']}"+('  <0,20' if sg<.20 else ''))
        if sg<.20:lista.append(f"{L['aid']}: {L['tex']} ({sg:.3f} s/glifo)")
    sgs=[(L['t1']-L['t0'])/max(1,len(re.findall(r'\\[a-zA-Z]+',L['tex']))+len(re.sub(r'\\[a-zA-Z]+|[{}^_ |]','',L['tex']))) for L in ls]
    cab=f'CADÊNCIA {lote}: {len(ls)} linhas'+(f', média {np.mean(sgs):.3f} s/glifo, mínimo {min(sgs):.3f}, {len(lista)} abaixo de 0,20' if sgs else ' (sem escrita de equações)')
    txt='\n'.join([cab]+linhas+['','ENXUGAR A PAUTA (decisão da Produção):']+(lista or ['  nenhuma']));(U/'qa'/f'cadencia_{lote}.txt').write_text(txt,encoding='utf-8');print(cab)

if modo in ('tamanho','todos'):tamanho()
if modo in ('contraste','todos'):contraste()
if modo in ('residuo','todos'):residuo()
if modo in ('cadencia','todos'):cadencia()

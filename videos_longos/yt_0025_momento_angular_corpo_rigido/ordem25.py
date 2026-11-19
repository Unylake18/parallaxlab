"""ORDEM POR X (handoff yt_0025 §1.3.4): nos quadros do vídeo, cada token de cada linha COMPLETA a sua tinta em ordem crescente de x (tolerância 1 quadro).
uso: python ordem25.py LOTE [MP4] [SAIDA.txt]   (lê os `[linha]` do log_LOTE.txt ou do log indicado em LOG=...)"""
import json,os,re,sys
from pathlib import Path
import av,numpy as np
from scipy.ndimage import binary_dilation
U=Path(__file__).resolve().parent
lote=sys.argv[1];mp4=Path(sys.argv[2]) if len(sys.argv)>2 else U/f'media_{lote}/videos/cena/540p15/{lote}.mp4'
log=Path(os.environ.get('LOG',U/f'log_{lote}.txt')).read_text(encoding='utf-8',errors='replace')
linhas=[json.loads(x) for x in re.findall(r'\[linha\] (\{.*\})',log)]
c=av.open(str(mp4));fps=float(c.streams.video[0].average_rate)
off=float(os.environ.get('OFFSET','0'))      # segundos do clip em relação ao relógio do lote (provas parciais)
fr=[f.reformat(width=960,height=540,format='gray').to_ndarray().astype(np.int16) for f in c.decode(video=0)]
rel=[];viol=0;sem=0;tol=1
for L in linhas:
    k0=int(round((L['t0']-off)*fps));k1=int(round((L['t1']-off)*fps))
    if k0<1 or k1+4>=len(fr):continue
    base=fr[k0];fim=fr[min(max(k0+1,k1-2),len(fr)-1)];toks=[]
    for k,x0,y0,x1,y1 in L['caixas']:
        x0,y0=max(0,x0-2),max(0,y0-2);x1,y1=min(960,x1+2),min(540,y1+2)
        if x1-x0<2 or y1-y0<2:continue
        final=(fim[y0:y1,x0:x1]-base[y0:y1,x0:x1])>45
        n=int(final.sum());finald=binary_dilation(final,iterations=2)
        if n<6:sem+=1;continue
        covs=[]
        for j in range(k0,min(len(fr),max(k0+2,k1-1))):
            ink=(fr[j][y0:y1,x0:x1]-base[y0:y1,x0:x1])>45
            covs.append(float((ink&finald).sum())/n)
        tf=tc=None
        for i_,cv in enumerate(covs):
            if tf is None and cv>=.12:tf=k0+i_
        for i_ in range(len(covs)):
            if all(cv>=.80 for cv in covs[i_:]):tc=k0+i_;break          # pouso = a partir dele a tinta fica no lugar (voo que só passa por cima não conta)
        if tf is not None:toks.append((x0,k,tf,tc if tc is not None else k1+3))
    toks.sort()
    if os.environ.get('DEBUG25') and L['t0']>=float(os.environ['DEBUG25']) and L['t0']<float(os.environ['DEBUG25'])+1:print(L['tex'],[(t[1],t[2],t[3]) for t in toks],'k0',k0)
    ruim=[]
    for a in range(len(toks)):
        for b in range(a+1,len(toks)):
            if toks[b][3]<toks[a][3]-tol:ruim.append((toks[a][1],toks[b][1],(toks[a][3]-toks[b][3])/fps))
    if ruim:viol+=1;rel.append(f"  {L['aid']} t0={L['t0']:.2f}s {L['tex']}: token {ruim[0][1]} completou {max(r[2] for r in ruim):.2f}s antes do token {ruim[0][0]} à esquerda ({len(ruim)} pares)")
out=[f"ORDEM POR X {lote}: {len(linhas)} linhas, {viol} com buraco/ordem errada, {sem} tokens sem medida"]+rel
txt="\n".join(out);print(txt)
if len(sys.argv)>3:Path(sys.argv[3]).write_text(txt,encoding='utf-8')

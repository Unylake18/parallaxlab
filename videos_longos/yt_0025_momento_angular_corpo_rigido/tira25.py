"""Tira de 6 quadros de uma linha da Pilha (handoff v3 §3.1): uso  python tira25.py LOTE  → uma imagem por linha apontada em qa/ordem_LOTE.txt
Recorta a região da linha (resolução cheia do vídeo, ampliada 1,5×) em 6 instantes entre o início e o fim da escrita."""
import json,re,sys
from pathlib import Path
import av
from PIL import Image,ImageDraw
U=Path(__file__).resolve().parent
lote=sys.argv[1]
mp4=U/f'media_{lote}/videos/cena/540p15/{lote}.mp4'
log=(U/f'log_{lote}.txt').read_text(encoding='utf-8',errors='replace')
linhas={(L['aid'],round(L['t0'],2)):L for L in (json.loads(x) for x in re.findall(r'\[linha\] (\{.*\})',log))}
alvos=[]
for l in (U/'qa'/f'ordem_{lote}.txt').read_text(encoding='utf-8',errors='replace').splitlines()[1:]:
    m=re.match(r'\s+(\S+) t0=([\d.]+)s',l)
    if m:alvos.append((m.group(1),round(float(m.group(2)),2),l.strip()))
c=av.open(str(mp4));fps=float(c.streams.video[0].average_rate);fr=[f.to_image() for f in c.decode(video=0)]
(U/'qa'/'ordem').mkdir(parents=True,exist_ok=True)
for aid,t0,desc in alvos:
    L=linhas.get((aid,t0))
    if not L:continue
    xs0=min(b[1] for b in L['caixas']);xs1=max(b[3] for b in L['caixas']);ys0=min(b[2] for b in L['caixas']);ys1=max(b[4] for b in L['caixas'])
    box=(max(0,xs0-14),max(0,ys0-14),min(960,xs1+14),min(540,ys1+14))
    ts=[L['t0']+(L['t1']-L['t0'])*k/5 for k in range(6)]
    tiles=[]
    for t in ts:
        k=min(len(fr)-1,int(round(t*fps)));im=fr[k].crop(box);im=im.resize((int(im.width*1.5),int(im.height*1.5)))
        d=ImageDraw.Draw(im);d.text((4,2),f't={t:.2f}s',fill=(255,255,0));tiles.append(im)
    W=max(i.width for i in tiles);H=sum(i.height for i in tiles)
    out=Image.new('RGB',(W,H));y=0
    for i in tiles:out.paste(i,(0,y));y+=i.height
    out.save(U/'qa'/'ordem'/f'{lote}_{aid}_{t0:.2f}.png')
    print(desc[:140])

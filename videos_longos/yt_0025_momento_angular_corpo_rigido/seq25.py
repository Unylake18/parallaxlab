"""Sequência de N quadros consecutivos (resolução cheia do vídeo, recorte opcional) para o zip de QA: python seq25.py LOTE t0 dt N saida.png [x0 y0 x1 y1]"""
import sys,av
from PIL import Image,ImageDraw
lote,t0,dt,N,saida=sys.argv[1],float(sys.argv[2]),float(sys.argv[3]),int(sys.argv[4]),sys.argv[5]
box=tuple(int(v) for v in sys.argv[6:10]) if len(sys.argv)>=10 else (0,0,960,540)
from pathlib import Path
U=Path(__file__).resolve().parent
c=av.open(str(U/f'media_{lote}/videos/cena/540p15/{lote}.mp4'));fps=15.0
ts=[t0+k*dt for k in range(N)];want={round(t*fps):t for t in ts};tiles={}
for i,f in enumerate(c.decode(video=0)):
    if i in want:tiles[want[i]]=f.to_image().crop(box)
    if i>max(want):break
ims=[tiles[t] for t in ts if t in tiles];cols=3 if len(ims)>3 else len(ims);rows=(len(ims)+cols-1)//cols
W,H=ims[0].size;o=Image.new('RGB',(W*cols,H*rows));d=ImageDraw.Draw(o)
for k,(t,im) in enumerate([(t,tiles[t]) for t in ts if t in tiles]):
    o.paste(im,((k%cols)*W,(k//cols)*H));d.text(((k%cols)*W+4,(k//cols)*H+2),f't={t:.2f}s',fill=(255,255,0))
Path(saida).parent.mkdir(parents=True,exist_ok=True);o.save(saida);print(saida,o.size)

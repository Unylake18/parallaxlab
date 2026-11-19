"""Extrai quadros de um mp4 (PyAV). uso: python frames25.py ARQ.mp4 SAIDA_DIR t1 t2 ...  (segundos; também 'a:b:n' = n quadros entre a e b)"""
import sys,av
from pathlib import Path
arq,saida=sys.argv[1],Path(sys.argv[2]);saida.mkdir(parents=True,exist_ok=True)
ts=[]
for a in sys.argv[3:]:
    if ':' in a:
        x,y,n=a.split(':');x,y,n=float(x),float(y),int(n);ts+= [x+(y-x)*k/max(1,n-1) for k in range(n)]
    else:ts.append(float(a))
c=av.open(arq);fps=float(c.streams.video[0].average_rate);want={round(t*fps):t for t in ts};n=0
for i,f in enumerate(c.decode(video=0)):
    if i in want:
        f.to_image().save(saida/f'f{i:05d}_{i/fps:07.2f}s.png');n+=1
print(n,'quadros; fps',fps,'total',i+1,'quadros',(i+1)/fps,'s')

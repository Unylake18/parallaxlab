import json,re,av
from PIL import Image,ImageDraw
U='.'
ANC=json.load(open('ancoras.json',encoding='utf-8'))['ancoras']
lin=[l for l in open('renders/sync.txt',encoding='utf-8').read().split('todos:')[1].splitlines() if l.strip()]
rows=[]
for l in lin:
    m=re.match(r'\s*(\S+)\s+(.+?)\s+([0-9.]+)\s+([0-9.]+)\s+(-?[0-9.]+)$',l)
    if m: rows.append((m.group(1),m.group(2),float(m.group(3)),float(m.group(4))))
ids=[0,12,25,38,50,62,75,88,100,112,125,138,146,151]
sel=[rows[i] for i in ids if i<len(rows)]
c=av.open('renders/preview_yt0022_v6_960x540.mp4');s=c.streams.video[0]
ims=[]
for aid,fr,tv,ti in sel:
    t=ANC[aid]['ini']+ti+0.25
    c.seek(int(t/s.time_base),stream=s)
    for f in c.decode(s):
        if f.time>=t-0.01:
            im=f.to_image().convert('RGB');d=ImageDraw.Draw(im);d.rectangle([0,505,960,540],fill=(0,0,0));d.text((6,510),f'{aid}  "{fr}"  t={t:.1f}s (imagem {ti:.2f} / voz {tv:.2f})',fill=(255,255,0));ims.append(im);break
W,H=ims[0].size;cols=2;rws=(len(ims)+1)//2
P=Image.new('RGB',(W*cols,H*rws))
for k,im in enumerate(ims):P.paste(im,((k%cols)*W,(k//cols)*H))
P.save('renders/chk/amostra_sync_v6.png');print(len(ims))

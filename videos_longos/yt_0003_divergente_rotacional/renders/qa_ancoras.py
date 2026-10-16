import json,av
from PIL import Image,ImageDraw
tiles=[]
for T in "ABCKDEF":
    b=json.load(open(f'renders/blocos_v3_1_{T}.json'))
    c=av.open(f'renders/m_{T}/videos/cena/540p15/trecho_{T}_v1_6.mp4');s=c.streams.video[0]
    frames={}
    ts=[]
    for x in b:
        ts.append((x['id'],'ini',x['inicio']+0.9)); ts.append((x['id'],'fim',max(x['inicio']+x['voz_s']-0.4,x['inicio']+1)))
    want=sorted(ts,key=lambda z:z[2]); k=0
    for f in c.decode(s):
        t=float(f.pts*s.time_base)
        while k<len(want) and t>=want[k][2]:
            frames[(want[k][0],want[k][1])]=f.to_image().resize((640,360)); k+=1
        if k>=len(want): break
    for x in b:
        for w in ('ini','fim'):
            im=frames.get((x['id'],w))
            if im is None: im=Image.new('RGB',(640,360))
            d=ImageDraw.Draw(im);d.rectangle((0,0,150,20),fill='black');d.text((4,3),f"{x['id']} {w}",fill='white')
            tiles.append(im)
for k in range(0,len(tiles),12):
    sh=Image.new('RGB',(1920,1440))
    for j,t in enumerate(tiles[k:k+12]): sh.paste(t,((j%3)*640,(j//3)*360))
    sh.save(f'renders/qa_v1_7/anc_{k//12+1:02d}.jpg',quality=85)
print(len(tiles))

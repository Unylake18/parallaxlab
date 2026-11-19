import sys,av
from PIL import Image, ImageDraw
f=sys.argv[1]; out=sys.argv[2]; ts=[float(x) for x in sys.argv[3:]]
c=av.open(f); r=float(c.streams.video[0].average_rate)
want={round(t*r):t for t in ts}; fr={}
for i,x in enumerate(c.decode(video=0)):
    if i in want: fr[want[i]]=x.to_image()
    if i>max(want): break
cols=3; rows=(len(ts)+cols-1)//cols
W,H=640,360
im=Image.new('RGB',(W*cols,H*rows))
for k,t in enumerate(ts):
    g=fr[t].resize((W,H)); d=ImageDraw.Draw(g); d.text((6,H-14),f"{int(t//60)}:{t%60:05.2f}",fill=(255,255,0)); im.paste(g,((k%cols)*W,(k//cols)*H))
im.save(out)

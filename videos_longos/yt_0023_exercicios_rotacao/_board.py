import av,sys
from PIL import Image
# uso: _board.py saida.png LOTE:t LOTE:t ...
out=sys.argv[1]; items=[a.split(":") for a in sys.argv[2:]]
ims=[]
for L,t in items:
    c=av.open(f"media_{L}/videos/cena/540p15/{L}.mp4"); k=round(float(t)*15)
    for i,f in enumerate(c.decode(video=0)):
        if i==k: ims.append(f.to_image()); break
    c.close()
n=len(ims); cols=2; rows=(n+1)//2
m=Image.new("RGB",(960*cols,540*rows))
for j,im in enumerate(ims): m.paste(im,((j%cols)*960,(j//cols)*540))
m.save(out)

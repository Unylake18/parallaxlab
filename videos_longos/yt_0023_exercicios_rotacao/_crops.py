import av,sys
from PIL import Image
L=sys.argv[1]; box=[int(v) for v in sys.argv[2].split(",")]; ts=[float(v) for v in sys.argv[3].split(",")]; out=sys.argv[4]
x0,y0,x1,y1=box; c=av.open(f"media_{L}/videos/cena/540p15/{L}.mp4"); fr={}
want={round(t*15) for t in ts}
for i,f in enumerate(c.decode(video=0)):
    if i in want: fr[i]=f.to_image().crop((x0,y0,x1,y1))
    if i>max(want): break
w,h=x1-x0,y1-y0; k=min(6,1900//w//len(ts)+1) if False else 4
m=Image.new("RGB",(w*k*3,h*k*((len(ts)+2)//3)))
for n,t in enumerate(ts): m.paste(fr[round(t*15)].resize((w*k,h*k),Image.LANCZOS),((n%3)*w*k,(n//3)*h*k))
m.save(out)

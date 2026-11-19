import av,sys,re
from PIL import Image
L,t0,box=sys.argv[1],float(sys.argv[2]),[int(v) for v in sys.argv[3].split(',')]
c=av.open(f'media_{L}/videos/cena/540p15/{L}.mp4'); k=round(t0*15)
fr={}
for i,f in enumerate(c.decode(video=0)):
    if k-3<=i<=k+2: fr[i]=f.to_image()
    if i>k+2: break
x0,y0,x1,y1=box; x0-=60;y0-=40;x1+=60;y1+=40
tiles=[fr[i].crop((max(0,x0),max(0,y0),min(960,x1),min(540,y1))) for i in sorted(fr)]
w,h=tiles[0].size; S=Image.new('RGB',(w*3,h*2))
for j,t in enumerate(tiles): S.paste(t,((j%3)*w,(j//3)*h))
S=S.resize((S.width*2,S.height*2)); S.save(sys.argv[4])

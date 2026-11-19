import sys,av
from PIL import Image
f,t0,t1,fps=sys.argv[1],float(sys.argv[2]),float(sys.argv[3]),float(sys.argv[4]); out=sys.argv[5]
c=av.open(f); st=c.streams.video[0]; r=float(st.average_rate)
fr=[]; 
for i,x in enumerate(c.decode(video=0)):
    t=i/r
    if t>t1: break
    if t>=t0 and abs((t-t0)*fps-round((t-t0)*fps))<0.5/r*fps: fr.append(x.to_image().resize((480,270)))
cols=3; rows=(len(fr)+cols-1)//cols
im=Image.new('RGB',(480*cols,270*rows))
for k,g in enumerate(fr): im.paste(g,((k%cols)*480,(k//cols)*270))
im.save(out); print(len(fr))

"""prancha em resolução cheia: python sheet25.py MP4 SAIDA.png t1 t2 t3 t4 (2×2 quadros 960×540 → 1920×1080)"""
import sys,av
from PIL import Image
mp4,out=sys.argv[1],sys.argv[2];ts=[float(x) for x in sys.argv[3:]]
c=av.open(mp4);fps=float(c.streams.video[0].average_rate);want={round(t*fps):k for k,t in enumerate(ts)};ims={}
for i,f in enumerate(c.decode(video=0)):
    if i in want:ims[want[i]]=f.to_image()
n=len(ts);cols=2 if n>1 else 1;rows=(n+1)//2
sh=Image.new('RGB',(960*cols,540*rows))
for k,im in ims.items():sh.paste(im,((k%cols)*960,(k//cols)*540))
sh.save(out)

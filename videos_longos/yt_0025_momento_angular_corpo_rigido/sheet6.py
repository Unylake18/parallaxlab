"""prancha 3×2 (2880×1080) em resolução cheia: python sheet6.py MP4 SAIDA.png t1..t6"""
import sys,av
from PIL import Image
mp4,out=sys.argv[1],sys.argv[2];ts=[float(x) for x in sys.argv[3:]]
c=av.open(mp4);fps=float(c.streams.video[0].average_rate);want={round(t*fps):k for k,t in enumerate(ts)};ims={}
for i,f in enumerate(c.decode(video=0)):
    if i in want:ims[want[i]]=f.to_image()
cols=3;rows=(len(ts)+cols-1)//cols;sh=Image.new('RGB',(960*cols,540*rows))
for k,im in ims.items():sh.paste(im,((k%cols)*960,(k//cols)*540))
sh.save(out)

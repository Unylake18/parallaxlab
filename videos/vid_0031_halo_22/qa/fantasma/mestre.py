import av,sys
from PIL import Image,ImageDraw
src=sys.argv[1];out=sys.argv[2];ts=[float(x) for x in sys.argv[3].split(',')]
c=av.open(src);ims=[]
for t in ts:
    c.seek(int(t*1e6))
    for f in c.decode(video=0):
        if f.time>=t-.02:
            im=f.to_image().resize((405,720));ImageDraw.Draw(im).text((6,705),f'{t}s',fill='white');ims.append(im);break
W=Image.new('RGB',(405*len(ims),720))
for i,m in enumerate(ims):W.paste(m,(405*i,0))
W.save(out)

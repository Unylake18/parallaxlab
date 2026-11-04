import sys, av, importlib.util
from pathlib import Path
from PIL import Image, ImageFont, ImageDraw
sys.path.insert(0,'videos'); import montar_legendado as ML
U=Path('videos/vid_0031_halo_22')
cues=ML.read_cues(U/'legenda.srt'); tc=ML.load_term_colors(U/'legenda_cores.py')
font=ImageFont.truetype(r'C:\Windows\Fonts\arialbd.ttf',58)
ts=[1,5,42,53,88,125,148,162,177]
c=av.open(str(U/'renders/vid_0031_halo_22_final_master_limpo.mp4')); ims=[]
for t in ts:
    c.seek(int(t*1e6))
    for f in c.decode(video=0):
        if f.time>=t-.02:
            at=float(f.pts*f.time_base)
            lines=next((q[2] for q in cues if q[0]<=at<q[1]),None)
            im=ML.draw_caption(f,lines,font,1080,1920,sys.argv[1],tc).resize((300,533)); ims.append(im); break
W=Image.new('RGB',(300*len(ims),533))
for i,m in enumerate(ims): W.paste(m,(300*i,0))
W.save(U/f'qa/fantasma/leg_{sys.argv[1]}.png')

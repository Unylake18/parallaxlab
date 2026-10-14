"""QA do preview V5: checkpoints, transições e 19 quadros de apresentação."""
import json
from pathlib import Path
import av
from PIL import Image,ImageDraw

UNIT=Path(__file__).resolve().parent
VIDEO=UNIT/'media_v5/videos/cena/960p15/QuedaCoriolis024.mp4'
OUT=UNIT/'qa_v5';OUT.mkdir(exist_ok=True)
marks=json.loads((UNIT/'qa_v5_timestamps.json').read_text(encoding='utf-8'))
c=av.open(str(VIDEO));s=c.streams.video[0]
duration=float(s.duration*s.time_base)
def extract(t,path):
    t=max(0,min(t,duration-.15));c.seek(int(t/s.time_base),stream=s)
    for frame in c.decode(s):
        if float(frame.pts*s.time_base)>=t:
            im=frame.to_image();im.save(path);return im
def sheets(items,prefix,cols=4,rows=3):
    for start in range(0,len(items),cols*rows):
        sheet=Image.new('RGB',(290*cols,520*rows),'#151b2a')
        for j,(t,path) in enumerate(items[start:start+cols*rows]):
            tile=Image.new('RGB',(290,520),'#151b2a')
            tile.paste(Image.open(path).resize((270,480)),(10,28))
            ImageDraw.Draw(tile).text((10,6),f'{start+j+1:02d}  {t:.2f}s',fill='white')
            sheet.paste(tile,((j%cols)*290,(j//cols)*520))
        sheet.save(OUT/f'{prefix}_{start//(cols*rows)+1:02d}.jpg')
checkpoints=[]
for i,m in enumerate(marks):
    t=m['t']-.13;path=OUT/f'estado_{i+1:02d}_{t:06.2f}.png'
    extract(t,path);checkpoints.append((t,path))
sheets(checkpoints,'estados')
# Amostragem temporal inclui os meios das transformações, não somente repousos.
intermediates=[]
for i in range(int(duration/2)+1):
    t=2*i+.45;path=OUT/f'intermediario_{i:03d}.jpg'
    extract(t,path);intermediates.append((t,path))
sheets(intermediates,'transicoes',cols=5,rows=4)
# Cobrir narrativa inteira com 19 imagens, incluindo as novas cenas de motivação.
indices=[0,1,2,4,5,6,7,9,10,11,14,16,18,20,21,22,24,26,len(marks)-1]
frames=[]
for i,index in enumerate(indices):
    t,path=checkpoints[index];dest=OUT/f'frame_{i+1:02d}.png'
    Image.open(path).save(dest);frames.append((t,dest))
sheets(frames,'19_frames',cols=5,rows=4)
metadata={'video':str(VIDEO),'duracao':duration,'largura':s.width,'altura':s.height,
          'fps_medio':str(s.average_rate),'checkpoints':len(checkpoints),
          'amostras_intermediarias':len(intermediates),'frames':19}
(OUT/'verificacao.json').write_text(json.dumps(metadata,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(metadata,ensure_ascii=False,indent=2))

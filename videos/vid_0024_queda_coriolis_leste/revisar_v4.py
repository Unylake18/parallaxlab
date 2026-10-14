"""Extrai checkpoints do MP4 e folhas de contato para QA visual localizado."""
import json
from pathlib import Path
import av
from PIL import Image, ImageDraw
UNIT=Path(__file__).resolve().parent
VIDEO=UNIT/'media_v4/videos/cena/960p15/QuedaCoriolis024.mp4'
OUT=UNIT/'qa_v4'
OUT.mkdir(exist_ok=True)
marks=json.loads((UNIT/'qa_v4_timestamps.json').read_text(encoding='utf-8'))
container=av.open(str(VIDEO)); stream=container.streams.video[0]
duration=float(stream.duration*stream.time_base)
frames=[]
for i,mark in enumerate(marks):
    t=min(mark['t']-.13,duration-.15)
    container.seek(int(t/stream.time_base),stream=stream)
    for frame in container.decode(stream):
        if float(frame.pts*stream.time_base)>=t:
            im=frame.to_image()
            path=OUT/f'{i+1:02d}_{t:06.2f}.png'; im.save(path)
            thumb=im.resize((270,480))
            tile=Image.new('RGB',(290,520),'#151b2a'); tile.paste(thumb,(10,28))
            ImageDraw.Draw(tile).text((10,6),f'{i+1:02d}  {t:.2f}s',fill='white')
            frames.append(tile); break
for start in range(0,len(frames),12):
    sheet=Image.new('RGB',(290*4,520*3),'#151b2a')
    for j,im in enumerate(frames[start:start+12]): sheet.paste(im,((j%4)*290,(j//4)*520))
    sheet.save(OUT/f'contato_{start//12+1}.jpg')
print(json.dumps({'video':str(VIDEO),'duracao':duration,'quadros':len(frames),
                  'largura':stream.width,'altura':stream.height,'fps':str(stream.average_rate)},indent=2))

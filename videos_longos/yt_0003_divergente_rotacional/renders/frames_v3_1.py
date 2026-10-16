"""Quadros do preview V1.7 inteiro: um a cada 4 s (jpg 960x540) + pranchas 3x4 com timestamp."""
import av
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
v = Path(__file__).parent/'videos/cena/540p15/preview_v3_1.mp4'
out = Path(__file__).parent/'qa_v3_1_inteiro'; (out/'quadros').mkdir(parents=True, exist_ok=True); (out/'pranchas').mkdir(exist_ok=True)
font = ImageFont.truetype('C:/Windows/Fonts/arial.ttf', 22)
STEP = 8.0; nxt = 0.0; tiles = []
with av.open(str(v)) as c:
    s = c.streams.video[0]
    for f in c.decode(s):
        t = float(f.pts*s.time_base)
        if t+1e-6 < nxt: continue
        nxt += STEP
        im = f.to_image(); im.save(out/'quadros'/f'q_{int(t//60):02d}m{t%60:05.2f}s.jpg', quality=88)
        tile = im.resize((640, 360)); d = ImageDraw.Draw(tile)
        d.rectangle((0, 0, 110, 28), fill='#000000'); d.text((6, 3), f'{int(t//60):02d}:{t%60:04.1f}', font=font, fill='white')
        tiles.append(tile)
for k in range(0, len(tiles), 12):
    sh = Image.new('RGB', (1920, 1440), '#050816')
    for j, tl in enumerate(tiles[k:k+12]): sh.paste(tl, ((j%3)*640, (j//3)*360))
    sh.save(out/'pranchas'/f'prancha_{k//12+1:02d}.jpg', quality=90)
print(len(tiles))

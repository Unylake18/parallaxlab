"""Extrai quadros reais do preview, sem editar seu conteúdo."""
import sys
from pathlib import Path
import av
from PIL import Image, ImageDraw, ImageFont

video = Path(sys.argv[1])
times = [float(t) for t in sys.argv[2].split(',')]
batch_size = int(sys.argv[3]) if len(sys.argv)>3 else 8
out = video.parents[3] / ('qa_' + video.stem)
out.mkdir(exist_ok=True)
font = ImageFont.truetype('C:/Windows/Fonts/arial.ttf', 23)
frames = []
with av.open(str(video)) as container:
    stream = container.streams.video[0]
    print(f'{video.name}: {stream.width}x{stream.height}; {stream.average_rate} fps; '
          f'{container.duration/1e6:.3f}s; audio={len(container.streams.audio)}')
    for frame in container.decode(video=0):
        if len(frames) == len(times):
            break
        if frame.time >= times[len(frames)]:
            im = frame.to_image()
            at = times[len(frames)]
            name = out / f'{len(frames)+1:02d}_{at:06.1f}s.png'
            im.save(name)
            tile = Image.new('RGB', (960, 575), '#050816')
            tile.paste(im, (0, 35))
            ImageDraw.Draw(tile).text((20, 5), f'{at//60:02.0f}:{at%60:04.1f}', font=font, fill='white')
            frames.append(tile)
    print(f'Quadros: {len(frames)} / {len(times)}; pasta: {out}')
for index in range(0,len(frames),batch_size):
    batch=frames[index:index+batch_size]
    sheet=Image.new('RGB',(1920,575*((len(batch)+1)//2)),'#050816')
    for j,im in enumerate(batch):
        sheet.paste(im,((j%2)*960,(j//2)*575))
    path=out/(f'yt_0003_v1_4_{index//batch_size+1:02d}.png' if batch_size==4 else f'contato_{index//batch_size+1:02d}.jpg')
    if path.suffix=='.jpg':
        sheet.save(path,quality=93)
    else:
        sheet.save(path)
    print(path)

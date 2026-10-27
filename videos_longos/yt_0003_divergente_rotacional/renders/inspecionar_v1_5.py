"""Quadros reais para os gates e as 19 folhas do preview silencioso V1.5."""
import sys
from pathlib import Path
import av
from PIL import Image, ImageDraw, ImageFont

video=Path(sys.argv[1]);times=[float(x) for x in sys.argv[2].split(',')]
offset=float(sys.argv[3]) if len(sys.argv)>3 else 0
out=Path(sys.argv[4]) if len(sys.argv)>4 else video.parents[3]/('qa_'+video.stem)
out.mkdir(exist_ok=True)
font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',22)
tiles=[];metadata={}
with av.open(str(video)) as c:
    stream=c.streams.video[0]
    metadata={'arquivo':str(video.resolve()),'largura':stream.width,'altura':stream.height,
              'fps_nominal':str(stream.base_rate),'fps_medio':str(stream.average_rate),
              'duracao':c.duration/1e6,'audio':len(c.streams.audio),'bytes':video.stat().st_size}
    for frame in c.decode(video=0):
        if len(tiles)>=len(times):break
        if frame.time+1e-5<times[len(tiles)]:continue
        t=frame.time+offset;im=frame.to_image()
        im.save(out/f'frame_{len(tiles)+1:02d}_{t:07.2f}s.png')
        tile=Image.new('RGB',(960,575),'#050816');tile.paste(im,(0,35))
        ImageDraw.Draw(tile).text((18,5),f'{int(t//60):02d}:{t%60:05.2f} · {video.stem}',font=font,fill='white')
        tiles.append(tile)
for k in range(0,len(tiles),4):
    sheet=Image.new('RGB',(1920,1150),'#050816')
    for j,tile in enumerate(tiles[k:k+4]):sheet.paste(tile,((j%2)*960,(j//2)*575))
    sheet.save(out/f'yt_0003_v1_5_{k//4+1:02d}.png')
print(metadata);print('Quadros:',len(tiles),'/',len(times));print(out)

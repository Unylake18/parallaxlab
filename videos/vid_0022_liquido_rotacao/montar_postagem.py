"""Monta os blocos nativos sem retimagem ou duplicação de quadros de movimento."""
from fractions import Fraction
from functools import lru_cache
import hashlib,json,math,sys
from pathlib import Path
import av
import numpy as np
from PIL import Image,ImageDraw,ImageFont
U=Path(__file__).resolve().parent
sys.path.insert(0,str(U));sys.path.insert(0,str(U.parents[1]/'videos'))
from sincronizar_preview import COLORS,PATTERN
from montar_legendado import read_cues
from montar_master import mux
SOURCE=U/'media_postagem/videos/cena_postagem/1920p30/fonte_postagem.mp4'
OUT=U/'media_montagem_postagem';OUT.mkdir(exist_ok=True)
DEST=U/'renders';DEST.mkdir(exist_ok=True)
FPS=30
FONT=ImageFont.truetype(r'C:\Windows\Fonts\arialbd.ttf',54)
@lru_cache(maxsize=80)
def overlay(lines):
    layer=Image.new('RGBA',(1080,1920));draw=ImageDraw.Draw(layer)
    if not lines:return layer
    widths=[FONT.getlength(l) for l in lines];assert max(widths)<=896
    top,bottom=1854-70*len(lines),1854;left=(1080-max(widths))/2-28
    draw.rounded_rectangle((left,top-16,1080-left,bottom+10),radius=24,fill=(4,6,16,225))
    for i,line in enumerate(lines):
        x=(1080-widths[i])/2;y=top+i*70-draw.textbbox((0,0),line,font=FONT,stroke_width=4)[1];cursor=0
        for match in list(PATTERN.finditer(line))+[None]:
            end=match.start() if match else len(line);chunk=line[cursor:end]
            draw.text((x,y),chunk,font=FONT,fill='white',stroke_width=4,stroke_fill='#040610');x+=FONT.getlength(chunk)
            if match:
                chunk=match.group();draw.text((x,y),chunk,font=FONT,fill=COLORS[chunk.lower()],stroke_width=4,stroke_fill='#040610');x+=FONT.getlength(chunk);cursor=match.end()
    return layer

def audio_aac():
    target=OUT/'narracao_320k.m4a'
    with av.open(str(U/'audio/narracao_final.wav')) as inp,av.open(str(target),'w') as out:
        stream=out.add_stream('aac',rate=44100);stream.layout='stereo';stream.bit_rate=320000
        resampler=av.AudioResampler(format='fltp',layout='stereo',rate=44100)
        for frame in inp.decode(audio=0):
            for f in resampler.resample(frame):
                for packet in stream.encode(f):out.mux(packet)
        for f in resampler.resample(None):
            for packet in stream.encode(f):out.mux(packet)
        for packet in stream.encode(None):out.mux(packet)
    return target

def faststart(target):
    """Move o índice MP4 para o início, copiando os streams sem recodificar."""
    temp=target.with_name(target.stem+'_faststart.mp4')
    with av.open(str(target)) as src,av.open(str(temp),'w',options={'movflags':'+faststart'}) as out:
        mapping={stream.index:out.add_stream_from_template(stream) for stream in src.streams}
        for packet in src.demux():
            if packet.dts is not None:
                packet.stream=mapping[packet.stream.index]
                out.mux(packet)
    temp.replace(target)

def main():
    plan=json.loads((U/'timing_postagem.json').read_text(encoding='utf-8'))
    cues=read_cues(U/'legenda.srt');cue_i=0;n=0
    clean=OUT/'visual_master.mp4';sub=OUT/'visual_legendado.mp4';seen=[]
    with av.open(str(SOURCE)) as src,av.open(str(clean),'w') as c,av.open(str(sub),'w') as s:
        encoders=[]
        for container in [c,s]:
            stream=container.add_stream('libx264',rate=FPS);stream.width=1080;stream.height=1920;stream.pix_fmt='yuv420p';stream.options={'crf':'14','preset':'medium'};encoders.append(stream)
        for block in plan['assembly']:
            begin,end=block['frames'];v=src.streams.video[0]
            src.seek(int(max(0,begin/FPS-.1)/v.time_base),stream=v,backward=True)
            count=0
            for frame in src.decode(video=0):
                index=round(float(frame.time)*FPS)
                if index<begin:continue
                if index>=end:break
                assert index==begin+count,(index,begin,count)
                at=n/FPS
                while cue_i<len(cues) and cues[cue_i][1]<=at:cue_i+=1
                lines=tuple(cues[cue_i][2]) if cue_i<len(cues) and cues[cue_i][0]<=at else ()
                image=frame.to_image()
                decorated=Image.alpha_composite(image.convert('RGBA'),overlay(lines)).convert('RGB') if lines else image
                for container,stream,img in zip([c,s],encoders,[image,decorated]):
                    f=av.VideoFrame.from_image(img);f.pts=n;f.time_base=Fraction(1,FPS)
                    for packet in stream.encode(f):container.mux(packet)
                count+=1;n+=1
                if n%600==0:print(f'Montagem nativa: {n}/{plan["total_frames"]} quadros',flush=True)
            assert count==end-begin,(count,begin,end)
            seen.append(dict(source_frames=[begin,end],frames=count))
        assert n==5124
        for container,stream in zip([c,s],encoders):
            for packet in stream.encode(None):container.mux(packet)
    sound=audio_aac()
    targets=[DEST/'vid_0022_postagem_master.mp4',DEST/'vid_0022_postagem_legendado.mp4']
    for visual,target in zip([clean,sub],targets):
        mux(visual,sound,target)
        faststart(target)
    result=dict(frames=n,seconds=n/FPS,res=[1080,1920],fps=FPS,assembly=seen,method='Animações nativas a 30 fps nos tempos aprovados; montagem por quadros, sem reamostragem temporal.',files=[str(p) for p in targets])
    (OUT/'montagem.json').write_text(json.dumps(result,indent=2,ensure_ascii=False),encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False),flush=True)
if __name__=='__main__':main()

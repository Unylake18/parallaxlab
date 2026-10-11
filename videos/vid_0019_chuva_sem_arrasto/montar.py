"""Monta cópias narrada limpa e legendada, com a duração integral do WAV.

Reutiliza os montadores do projeto. Só retira eventual quadro excedente do
fim do render, por arredondamento; não corta nem altera o ritmo da voz.
Uso: uv run --no-sync python videos/vid_0019_chuva_sem_arrasto/montar.py
Para reproduzir o preview antigo: acrescentar --preview.
"""
import sys
import argparse
import wave
from contextlib import ExitStack
from fractions import Fraction
from pathlib import Path
from tempfile import TemporaryDirectory
import av
from PIL import ImageFont

UNIT = Path(__file__).resolve().parent
ROOT = UNIT.parents[1]
sys.path.insert(0,str(ROOT/'videos'))
from montar_master import encode_audio
from montar_legendado import draw_caption, read_cues, mux_audio


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--preview',action='store_true')
    args = parser.parse_args()
    output = ROOT/('renders/vid_0019_narrado' if args.preview else 'renders/vid_0019_final')
    width,height,fps = (540,960,15) if args.preview else (1080,1920,30)
    visual = output/('videos/cena/960p15/chuva_sem_arrasto_sincronizado.mp4' if args.preview else 'videos/cena/1920p30/chuva_sem_arrasto_final_visual.mp4')
    sound = UNIT/'audio/narracao_final.wav'
    cues = read_cues(UNIT/'legenda.srt')
    with wave.open(str(sound)) as w:
        duration = w.getnframes()/w.getframerate()
    total = round(duration*fps)
    assert abs(total/fps-duration)<1e-6
    font = ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf',round(29*width/540))
    with TemporaryDirectory() as folder:
        temporary = Path(folder)
        aac = temporary/'voz.m4a'
        encode_audio(sound,aac)
        paths = [temporary/'limpo.mp4',temporary/'legendas.mp4']
        with ExitStack() as stack:
            source = stack.enter_context(av.open(str(visual)))
            v = source.streams.video[0]
            assert (v.width,v.height,round(float(v.base_rate))) == (width,height,fps)
            destinations = [stack.enter_context(av.open(str(p),'w')) for p in paths]
            streams = []
            for out in destinations:
                s = out.add_stream('libx264',rate=fps)
                s.width,s.height,s.pix_fmt = width,height,'yuv420p'
                s.options = {'crf':'18' if args.preview else '16','preset':'veryfast' if args.preview else 'medium'}
                streams.append(s)
            index,count = 0,0
            for count,f in enumerate(source.decode(video=0),1):
                if count>total:
                    count=total
                    break
                at=(count-1)/fps
                while index<len(cues) and cues[index][1]<=at:
                    index+=1
                lines=(cues[index][2] if index<len(cues) and cues[index][0]<=at else None)
                captioned = av.VideoFrame.from_image(draw_caption(f,lines,font,width,height,'standard'))
                for frame,out,s in zip((f,captioned),destinations,streams):
                    frame.pts,frame.time_base=count-1,Fraction(1,fps)
                    for packet in s.encode(frame):
                        out.mux(packet)
            assert count==total, (count,total)
            for out,s in zip(destinations,streams):
                for packet in s.encode(None):
                    out.mux(packet)
        names = (('chuva_sem_arrasto_narrado.mp4','chuva_sem_arrasto_legendado.mp4') if args.preview else
                 ('vid_0019_chuva_sem_arrasto_final_master_limpo.mp4','vid_0019_chuva_sem_arrasto_final_legendado.mp4'))
        for silent,name in zip(paths,names):
            target=(output if args.preview else ROOT/'renders')/name
            mux_audio(silent,aac,target)
            with av.open(str(target)) as c:
                v,a=c.streams.video[0],c.streams.audio[0]
                print(f'{target.name}: {total} quadros; vídeo {float(v.duration*v.time_base):.3f}s; áudio {float(a.duration*a.time_base):.3f}s')


if __name__=='__main__':
    main()

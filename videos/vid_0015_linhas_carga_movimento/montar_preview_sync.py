"""Sincroniza a cópia do preview V4 ao WAV e queima legendas na faixa segura.

V4 e WAV originais são preservados. A amostragem temporal por âncoras mantém
geometria, matemática e sequência; a saída continua em 540×960 / 15 fps.
Tipografia, cores e caixa seguem o helper global dos vídeos anteriores.
"""
from fractions import Fraction
import importlib.util
import json
import math
from pathlib import Path
import re
import sys

import av
import numpy as np
from PIL import Image, ImageDraw, ImageFont

UNIT = Path(__file__).resolve().parent
ROOT = UNIT.parents[1]
sys.path.insert(0, str(ROOT))
from legendas_cores import SUBTITLE_TERM_COLORS


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


captions = module("montar_legendado_base", ROOT/"videos/montar_legendado.py")
audio_helpers = module("montar_master_base", ROOT/"videos/montar_master.py")

# Inícios das ideias na V4 congelada. A raiz precede o primeiro payoff.
NATIVE = [0,11.4,19.3,24.5,35.7,42.133,52.067,57.933,67.1,75.6,
          83,95.4,108.0,113.6,122.9,130.867,142.733,153.733,164.933,173.067]


def caption_image(frame, lines, font, spans):
    if not lines:
        return frame.to_image()
    # Mesmo estilo sólido/Arial Bold 29 do vid_0014. Aqui o gráfico ocupa
    # a região antiga da legenda; o texto fica inteiramente abaixo de y=-5,7.
    base = frame.to_image().convert("RGBA")
    width = base.width
    scale = width / 540
    stroke = round(2 * scale)
    overlay = Image.new("RGBA", base.size)
    draw = ImageDraw.Draw(overlay)
    boxes = [draw.textbbox((0,0),line,font=font,stroke_width=stroke) for line in lines]
    widest = max(box[2]-box[0] for box in boxes)
    assert widest <= 468 * scale, lines
    bottom, line_height = round(928 * scale), round(38 * scale)
    top = bottom-len(lines)*line_height
    left = (width-widest)/2-15 * scale
    draw.rounded_rectangle((left,top-8 * scale,width-left,bottom+5 * scale),radius=12 * scale,fill=(4,6,16,255))
    # Os spans vêm do texto inteiro: a cor atravessa linhas e limites de cue.
    offset = 0
    for index,line in enumerate(lines):
        x,y = width/2-(boxes[index][2]-boxes[index][0])/2,top+index*line_height-boxes[index][1]
        boundaries = {0,len(line)}
        for a,b,_ in spans:
            if b>offset and a<offset+len(line):
                boundaries.update((max(0,a-offset),min(len(line),b-offset)))
        edges = sorted(boundaries)
        for a,b in zip(edges,edges[1:]):
            color = next((color for start,end,color in spans if start<=offset+a<end),"white")
            chunk = line[a:b]
            draw.text((x,y),chunk,font=font,fill=color,stroke_width=stroke,stroke_fill="#040610")
            x += draw.textlength(chunk,font=font)
        offset += len(line)+1
    base.alpha_composite(overlay)
    return base.convert("RGB")


def cue_color_spans(cues):
    chunks = [" ".join(lines) for _,_,lines in cues]
    joined = " ".join(chunks)
    terms = sorted(SUBTITLE_TERM_COLORS,key=len,reverse=True)
    pattern = re.compile(r"(?<![\w'])("+"|".join(map(re.escape,terms))+r")(?![\w'])")
    all_spans = [(m.start(),m.end(),SUBTITLE_TERM_COLORS[m.group()]) for m in pattern.finditer(joined)]
    result,offset = [],0
    for chunk in chunks:
        result.append([(max(0,a-offset),min(len(chunk),b-offset),color)
            for a,b,color in all_spans if b>offset and a<offset+len(chunk)])
        offset += len(chunk)+1
    return result


def main():
    visual = UNIT/"media/videos/cena/960p15/vid_0015_preview_v4_silencioso.mp4"
    anchors = json.loads((UNIT/"sync.json").read_text())["anchors"]
    assert [name for name,_ in anchors] == [f"p{i:02d}" for i in range(1,20)]+["fim"]
    target = np.array([0]+[time for _,time in anchors])
    source = np.array([0]+NATIVE)
    words = json.loads((UNIT/"palavras_tempos.json").read_text(encoding="utf-8"))["palavras"]
    def word_start(phrase):
        wanted = phrase.lower().split()
        normalized = [re.sub(r"[^\w]","",w["texto"].lower()) for w in words]
        for i in range(len(words)-len(wanted)+1):
            if normalized[i:i+len(wanted)] == wanted:
                return words[i]["inicio_s"]
        raise ValueError(phrase)
    # A razão já aparece durante sua leitura; o gráfico nasce a seguir.
    # Em "sessenta por cento" a tela chega a 0,6 e segura durante o exemplo.
    # O limite 0,995 aparece com a interpretação da resultante repulsiva.
    extra = [
        (word_start("o resultado é"),142.433),
        (word_start("o resultado é")+1.3,142.733),
        (word_start("agora neste modelo ideal")-0.2,146.833),
        (word_start("a sessenta por cento"),153.133),
        (word_start("a sessenta por cento")+0.18,153.333),
        (word_start("à medida que")-0.25,153.533),
        (word_start("mas a resultante")-1.1,159.733),
        (word_start("mas a resultante")+0.97,163.933),
    ]
    # Substitui o início nominal da criação do gráfico pela âncora fina.
    pairs = [(a,b) for a,b in zip(target,source) if b!=142.733]+extra
    pairs.sort()
    target,source = np.array([a for a,_ in pairs]),np.array([b for _,b in pairs])
    assert np.all(np.diff(target)>0) and np.all(np.diff(source[1:])>0)
    (UNIT/"native.json").write_text(json.dumps({"anchors":list(zip([name for name,_ in anchors],NATIVE)),
        "mapa_fino_audio_nativo":pairs,
        "metodo":"reamostragem por paragrafos e ancoras do grafico; V4 original preservada"},indent=2),encoding="utf-8")
    cues = captions.read_cues(UNIT/"legenda.srt")
    color_spans = cue_color_spans(cues)
    font = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf",29)
    outdir = UNIT/"renders"
    outdir.mkdir(exist_ok=True)
    silent = outdir/"vid_0015_preview_sync_sem_audio.mp4"
    subtitled = outdir/"vid_0015_preview_sync_legendas_sem_audio.mp4"
    audio_aac = UNIT/"audio/narracao_preview.m4a"
    frame_count = math.ceil(target[-1]*15)
    samples = {}
    for i,(start,end,lines) in enumerate(cues):
        samples.setdefault(round((start+end)/2*15),[]).append(i+1)
    frame_dir = UNIT/"frames_preview_legendado"
    frame_dir.mkdir(exist_ok=True)
    with av.open(str(visual)) as inp, av.open(str(silent),"w") as clean, av.open(str(subtitled),"w") as subs:
        streams = []
        for output in (clean,subs):
            stream = output.add_stream("libx264",rate=15)
            stream.width,stream.height,stream.pix_fmt = 540,960,"yuv420p"
            stream.options = {"crf":"19","preset":"veryfast"}
            streams.append(stream)
        decoder = iter(inp.decode(video=0))
        current,next_frame = next(decoder),next(decoder,None)
        cue_index = 0
        for n in range(frame_count):
            at = n/15
            wanted = float(np.interp(at,target,source))
            while next_frame is not None and float(next_frame.time)<=wanted:
                current,next_frame = next_frame,next(decoder,None)
            selected = current
            if next_frame is not None and float(next_frame.time)-wanted<wanted-float(current.time):
                selected = next_frame
            while cue_index<len(cues) and cues[cue_index][1]<=at:
                cue_index += 1
            lines = cues[cue_index][2] if cue_index<len(cues) and cues[cue_index][0]<=at else None
            decorated = caption_image(selected,lines,font,color_spans[cue_index] if lines else [])
            if n in samples:
                for cue_number in samples[n]:
                    decorated.save(frame_dir/f"cue_{cue_number:02d}.png")
            for output,stream,img in zip((clean,subs),streams,(selected.to_image(),decorated)):
                frame = av.VideoFrame.from_image(img)
                frame.pts,frame.time_base = n,Fraction(1,15)
                for packet in stream.encode(frame):
                    output.mux(packet)
        for output,stream in zip((clean,subs),streams):
            for packet in stream.encode(None):
                output.mux(packet)
    audio_helpers.encode_audio(UNIT/"audio/narracao_final.wav",audio_aac)
    audio_helpers.mux(silent,audio_aac,outdir/"vid_0015_preview_sync_master.mp4")
    audio_helpers.mux(subtitled,audio_aac,outdir/"vid_0015_preview_sync_legendado.mp4")
    print(json.dumps({"frames":frame_count,"video_s":frame_count/15,"audio_s":target[-1],
        "cues":len(cues),"saida":str(outdir/"vid_0015_preview_sync_legendado.mp4")},ensure_ascii=False))


if __name__ == "__main__":
    main()

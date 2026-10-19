"""Decodifica o preview inteiro e extrai estados + amostragem temporal para inspeção."""
import json
import math
from pathlib import Path
import av
import numpy as np
from PIL import Image, ImageDraw, ImageFont

UNIT=Path(__file__).resolve().parent
RENDERS=UNIT/"renders"
VIDEO=RENDERS/"videos"/"cena"/"540p15"/"YT0006BiotSavart.mp4"


def extract(path, targets, out, prefix):
    container=av.open(str(path));stream=container.streams.video[0]
    fps=float(stream.base_rate or stream.average_rate)
    ordered=sorted(targets,key=lambda t:t[0]);index=0;count=0;results=[]
    for frame in container.decode(stream):
        t=float(frame.time or 0);count+=1
        while index<len(ordered) and t>=ordered[index][0]:
            target,name=ordered[index]
            im=frame.to_image()
            file=out/f"{prefix}_{index:03d}_{target:08.2f}.png"
            im.save(file)
            results.append((file,f"{target:.1f}s  {name}"))
            index+=1
    duration=float(stream.duration*stream.time_base) if stream.duration is not None else count/fps
    meta={"arquivo":str(path),"largura":stream.width,"altura":stream.height,"fps":fps,"quadros_decodificados":count,"duracao_s":duration,"codec":stream.codec_context.name,"pixel_format":stream.codec_context.format.name,"alvos_extraidos":index}
    container.close()
    return results,meta


def sheets(items,out,prefix):
    font=ImageFont.truetype("C:/Windows/Fonts/arial.ttf",16)
    paths=[]
    for start in range(0,len(items),12):
        page=Image.new("RGB",(1440,900),(18,22,34));draw=ImageDraw.Draw(page)
        for j,(path,title) in enumerate(items[start:start+12]):
            x=(j%3)*480;y=(j//3)*225
            im=Image.open(path).convert("RGB").resize((384,216))
            # 3 × 4, quadros inteiros; espaço de texto à direita para rótulo curto.
            page.paste(im,(x,y))
            draw.text((x+385,y+10),title[:12],font=font,fill="white")
            draw.text((x+385,y+38),title[12:24],font=font,fill="white")
            draw.text((x+385,y+66),title[24:36],font=font,fill="white")
        file=out/f"{prefix}_{start//12:02d}.jpg";page.save(file,quality=92);paths.append(str(file))
    return paths


if __name__=="__main__":
    out=RENDERS/"qa_visual";out.mkdir(parents=True,exist_ok=True)
    timeline=json.loads((RENDERS/"qa_timeline.json").read_text(encoding="utf-8"))
    # Manim soma durações solicitadas ao usar cache; o contêiner pode incluir
    # arredondamentos de quadro. Índices de partes dão os estados exatos do MP4.
    playlist=VIDEO.parent/"partial_movie_files"/"YT0006BiotSavart"/"partial_movie_file_list.txt"
    boundaries=[0.0]
    for line in playlist.read_text(encoding="utf-8").splitlines():
        if not line.startswith("file '"):
            continue
        part_path=line[len("file 'file:"):-1]
        with av.open(part_path) as part:
            s=part.streams.video[0]
            frames=s.frames or sum(1 for _ in part.decode(s))
            boundaries.append(boundaries[-1]+frames/float(s.base_rate or s.average_rate))
    for event in timeline["checkpoints"]+timeline["sections"]:
        event["time_video"]=boundaries[event["part"]]
    timeline["duration_video"]=boundaries[-1]
    (RENDERS/"qa_timeline_video.json").write_text(json.dumps(timeline,ensure_ascii=False,indent=2),encoding="utf-8")
    targets=[(min(c["time_video"]+0.08,boundaries[-1]-0.1),c["name"]) for c in timeline["checkpoints"]]
    items,meta=extract(VIDEO,targets,out,"estado")
    meta["pranchas_estados"]=sheets(items,out,"estados")
    samples=[(float(t),"amostra temporal") for t in range(3,int(meta["duracao_s"]),5)]
    items2,meta2=extract(VIDEO,samples,out,"tempo")
    meta["pranchas_temporais"]=sheets(items2,out,"temporal")
    ref=RENDERS/"referencia_51"/"videos"/"qa_referencia"/"540p15"/"QAContinuidade51.mp4"
    # render via API usa o nome da classe como diretório de módulo, dependendo da versão.
    if not ref.exists():
        candidates=list((RENDERS/"referencia_51").rglob("QAContinuidade51.mp4"))
        if candidates:ref=candidates[0]
    if ref.exists():
        ritems,rmeta=extract(ref,[(6,"5.1 campo"),(10,"5.1 força"),(12,"5.1 gancho")],out,"referencia")
        meta["referencia_51"]=rmeta
        meta["prancha_continuidade"]=sheets(ritems+[(items[0][0],"5.2 abertura")],out,"continuidade")
    (RENDERS/"qa_video.json").write_text(json.dumps(meta,ensure_ascii=False,indent=2),encoding="utf-8")
    print(json.dumps(meta,ensure_ascii=False,indent=2))

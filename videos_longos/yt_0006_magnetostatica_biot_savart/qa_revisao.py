"""QA do MP4 revisado: decodificação integral, estados e sequências de movimento.

Não renderiza as referências. Todos os tempos vêm dos segmentos do próprio MP4.
"""
import json
from pathlib import Path
import av
import numpy as np
from PIL import Image, ImageDraw, ImageFont

UNIT = Path(__file__).resolve().parent
OUT = UNIT / "renders" / "revisao_v3"
VIDEO = OUT / "videos" / "cena" / "540p15" / "YT0006BiotSavart.mp4"


def sheet(items, path, cols=3):
    rows = (len(items)+cols-1)//cols
    im = Image.new("RGB", (480*cols, 296*rows), "#050816")
    draw = ImageDraw.Draw(im)
    font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 16)
    for i,(file,caption) in enumerate(items):
        x,y=(i%cols)*480,(i//cols)*296
        with Image.open(file) as src:
            im.paste(src.convert("RGB").resize((480,270)),(x,y))
        draw.text((x+6,y+274),caption[:56],font=font,fill="white")
    im.save(path,quality=92)


def run(clip=None):
    video=VIDEO if clip is None else OUT/"videos"/"preview_trechos"/"540p15"/("Revisao"+clip.capitalize()+".mp4")
    suffix="" if clip is None else "_"+clip
    timeline=json.loads((OUT/("qa_timeline.json" if clip is None else f"qa_trecho_{clip}.json")).read_text(encoding="utf-8"))
    # --save_sections reescreve a playlist por seção. Os índices uncached
    # são os mesmos registrados por renderer.num_plays, sem ambiguidade.
    partials=video.parent/"partial_movie_files"/video.stem
    plays=timeline.get("plays",max(e["part"] for e in timeline["checkpoints"]))
    boundaries=[0.]
    for i in range(plays):
        with av.open(partials/f"uncached_{i:05d}.mp4") as c:
            v=c.streams.video[0]
            n=v.frames or sum(1 for _ in c.decode(v))
            boundaries.append(boundaries[-1]+n/float(v.base_rate or v.average_rate))
    targets=[]
    for i,event in enumerate(timeline["checkpoints"]):
        event["time_video"]=boundaries[event["part"]]
        targets.append((min(event["time_video"]+.08,boundaries[-1]-.1),f"estado_{i:03d}_{event['name']}",event["name"],"estados"))
    for i,event in enumerate(timeline["motion_windows"]):
        event["time_video"]=boundaries[event["part"]]
        for k,t in enumerate(np.linspace(.05,event["duration"]-.1,12)):
            targets.append((event["time_video"]+float(t),f"mov_{i:02d}_{k:02d}",f"{event['name']} · +{t:.2f}s",f"movimento_{i:02d}"))
    for k,t in enumerate(range(3,int(boundaries[-1]),5)):
        targets.append((float(t),f"tempo_{k:03d}",f"{t}s","temporal"))
    # Evidência de corrente ativa em pausas, após o checkpoint.
    pause_names=["gancho_campo","regime_balanco","geometria_fonte_observador",
                 "clinica_30","resultado_trecho_finito","resultado_fio_infinito",
                 "fios_atracao","fios_repulsao","espira_triangulo",
                 "espira_projecao_axial","resultado_espira_eixo"]
    pause_names=[n for n in pause_names if n in {e["name"] for e in timeline["checkpoints"]}]
    for name in pause_names:
        e=next(e for e in timeline["checkpoints"] if e["name"]==name)
        for k,t in enumerate([.4,.8,1.2,1.6]):
            targets.append((e["time_video"]+t,f"pausa_{name}_{k}",f"{name} +{t:.1f}s","pausas"))
    frames=OUT/("qa_frames"+suffix);frames.mkdir(exist_ok=True)
    targets.sort()
    results={};count=0;index=0
    with av.open(video) as c:
        v=c.streams.video[0]
        assert len(c.streams.audio)==0, "Preview deve ser silencioso"
        for frame in c.decode(v):
            count+=1;t=float(frame.time or 0)
            while index<len(targets) and t>=targets[index][0]:
                target,name,caption,group=targets[index]
                path=frames/f"{name}.png"
                frame.to_image().save(path)
                results.setdefault(group,[]).append((path,caption))
                index+=1
        meta={"arquivo":str(video),"largura":v.width,"altura":v.height,
              "fps":float(v.base_rate or v.average_rate),"quadros_decodificados":count,
              "duracao_s":float(v.duration*v.time_base),"codec":v.codec_context.name,
              "pixel_format":v.codec_context.format.name,"capturas":index,"audio":False}
    assert count==round(boundaries[-1]*15),(count,boundaries[-1])
    assert abs(count/15-meta["duracao_s"])<1/15
    assert meta["largura"]==960 and meta["altura"]==540 and meta["fps"]==15
    assert index==len(targets),(index,len(targets))
    for group,items in results.items():
        step=12
        for start in range(0,len(items),step):
            sheet(items[start:start+step],frames/f"{group}_{start//step:02d}.jpg")
    motion=[]
    for name in pause_names:
        arrays=[np.asarray(Image.open(frames/f"pausa_{name}_{k}.png").convert("RGB"),dtype=np.int16) for k in range(4)]
        # Região da fonte; o painel algébrico está à direita.
        changed=[int(np.any(np.abs(a[90:425,:470]-b[90:425,:470])>20,axis=2).sum()) for a,b in zip(arrays,arrays[1:])]
        motion.append({"pausa":name,"pixels_alterados_na_fonte":changed})
        assert min(changed)>5,(name,changed)
    meta["corrente_durante_pausas"]=motion
    (OUT/("qa_video"+suffix+".json")).write_text(json.dumps(meta,ensure_ascii=False,indent=2),encoding="utf-8")
    (OUT/("qa_timeline_video"+suffix+".json")).write_text(json.dumps(timeline,ensure_ascii=False,indent=2),encoding="utf-8")
    print(json.dumps(meta,ensure_ascii=False,indent=2))


if __name__=="__main__":
    import sys
    run(sys.argv[1] if len(sys.argv)>1 else None)

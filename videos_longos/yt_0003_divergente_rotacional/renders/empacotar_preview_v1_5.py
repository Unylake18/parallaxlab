"""Entrega localizada: cortes sem recodificação, 19 folhas e QA do preview."""
from pathlib import Path
import hashlib
import json
import re
import subprocess
import sys
import zipfile
import av
from PIL import Image, ImageDraw, ImageFont

root=Path(__file__).resolve().parents[1]
video=root/'renders/videos/cena/540p15/preview_v1_5.mp4'
times=[7,11,18,24,32, 39,50,58,66,
       78,81.7,86.5,90.5,98.3,104.6,109.2,116.4,119.1,122.4,
       126.4,130.4,134.4,138.6,141.3,145,148.4,151.4,154.4,
       166,170.5,180,187,194,201,211,219,229,236,
       250,257,265,278,293,307,319,334,343,350,354.3,360,367,375,384,392,
       398,412,424,437,445,452,474,485,495,507,520,532,542,550,561,571,581,588,
       632,642,650.5,673]
assert len(times)==76
if '--imagens' in sys.argv:
    subprocess.run([sys.executable,str(root/'renders/inspecionar_v1_5.py'),str(video),','.join(map(str,times))],check=True)
    sheets=sorted((root/'renders/qa_preview_v1_5').glob('yt_0003_v1_5_*.png'));assert len(sheets)==19
    archive=root/'renders/yt_0003_v1_5_19_imagens.zip'
    with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
        for sheet in sheets:z.write(sheet,sheet.name)
    with zipfile.ZipFile(archive) as z:assert len(z.namelist())==19 and z.testzip() is None
    report=root/'renders/entrega_preview_v1_5.json';info=json.loads(report.read_text(encoding='utf-8'))
    info['timestamps_19_imagens']=times;report.write_text(json.dumps(info,ensure_ascii=False,indent=2),encoding='utf-8')
    print(archive);sys.exit(0)
with av.open(str(video)) as c:
    s=c.streams.video[0]
    assert (s.width,s.height)==(960,540) and s.base_rate==15 and not c.streams.audio
    frames=sum(1 for _ in c.decode(video=0))
    info={'arquivo':str(video),'resolucao':[s.width,s.height],'fps_nominal':str(s.base_rate),
          'duracao_segundos':c.duration/1e6,'quadros_decodificados':frames,
          'codec':s.codec_context.name,'pix_fmt':s.codec_context.format.name,'audio':0,'bytes':video.stat().st_size}
with av.open(str(video)) as c:
    s=c.streams.video[0];tb=s.time_base
    packets=[p for p in c.demux(s) if p.pts is not None and p.dts is not None]
    keys=[(i,p.pts,float(p.pts*tb)) for i,p in enumerate(packets) if p.is_keyframe]
    sample=b''.join(bytes(p) for p in packets[:4]);crf=re.search(rb'crf=([0-9.]+)',sample)
    info['crf']=crf.group(1).decode() if crf else None
    cuts=[]
    # Intervalos disjuntos: cada pacote é remuxado uma única vez.
    for name,start,end in [('A',0,70),('B',70,155),('C',155,245),('K',245,270),('D',270,395),('E',395,590),('F',590,None)]:
        lo=min(keys,key=lambda k:abs(k[2]-start))
        hi=min(keys,key=lambda k:abs(k[2]-end)) if end is not None else (len(packets),None,None)
        target=video.with_name(('exemplo_K' if name=='K' else 'trecho_'+name)+'_v1_5.mp4')
        temporary=target.with_name(target.stem+'_conferindo.mp4')
        with av.open(str(temporary),'w') as output:
            stream=output.add_stream_from_template(s)
            for packet in packets[lo[0]:hi[0]]:
                packet.pts-=lo[1];packet.dts-=lo[1];packet.time_base=tb;packet.stream=stream
                output.mux(packet)
        with av.open(str(temporary)) as check:
            cs=check.streams.video[0]
            assert (cs.width,cs.height)==(960,540) and cs.base_rate==15 and not check.streams.audio
            count=sum(1 for _ in check.decode(video=0));assert count>0
            cut={'trecho':name,'arquivo':str(target),'inicio_no_completo':lo[2],
                 'fim_no_completo':hi[2] or info['duracao_segundos'],'quadros':count,
                 'duracao_segundos':check.duration/1e6,'sem_recodificacao':True}
        temporary.replace(target);cuts.append(cut)
subprocess.run([sys.executable,str(root/'renders/inspecionar_v1_5.py'),str(video),','.join(map(str,times))],check=True)
folder=root/'renders/qa_preview_v1_5'
sheets=sorted(folder.glob('yt_0003_v1_5_*.png'));assert len(sheets)==19
archive=root/'renders/yt_0003_v1_5_19_imagens.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
    for sheet in sheets:z.write(sheet,sheet.name)
with zipfile.ZipFile(archive) as z:assert len(z.namelist())==19 and z.testzip() is None

def frame_at(path,t):
    with av.open(str(path)) as c:
        s=c.streams.video[0];c.seek(int(t/float(s.time_base)),stream=s)
        for frame in c.decode(video=0):
            if frame.time>=t:return frame.to_image().resize((960,540))
    raise RuntimeError((path,t))

repo=root.parents[1]
font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',21)
comparison=Image.new('RGB',(1920,1725),'#050816');draw=ImageDraw.Draw(comparison)
references=[(repo/'renders/yt_0001_lei_gauss_preview_v2_960x540_15fps.mp4',110,11,'yt_0001 · preview local V2 · vetor área'),
            (repo/'renders/yt_0002_final/g0/videos/cena/1080p30/LeiGaussCasosClassicos002.mp4',145,97,'yt_0002 · final local g0 · fluxo de uma face'),
            (repo/'media/videos/cena/540p15/LeiGaussCasosClassicos002.mp4',185,236,'yt_0002 · preview local · construção de Gauss')]
for row,(path,t,ours,label) in enumerate(references):
    y=row*575;draw.text((15,y+5),label,font=font,fill='white')
    draw.text((975,y+5),f'yt_0003 · V1.5 · {int(ours//60):02d}:{ours%60:02.0f}',font=font,fill='white')
    comparison.paste(frame_at(path,t),(0,y+35));comparison.paste(frame_at(video,ours),(960,y+35))
compare=root/'renders/referencias_v1_5/comparacao_lado_a_lado.png';compare.parent.mkdir(exist_ok=True)
comparison.save(compare)
info.update({'sha256_cena':hashlib.sha256((root/'cena.py').read_bytes()).hexdigest(),
             'cortes':cuts,'timestamps_19_imagens':times,'zip_19_imagens':str(archive),
             'comparacao_referencias':str(compare)})
(root/'renders/entrega_preview_v1_5.json').write_text(json.dumps(info,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(info,ensure_ascii=False,indent=2))

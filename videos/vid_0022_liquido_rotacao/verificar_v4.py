"""QA da postagem: codecs, áudio integral, relógio CFR, legendas e movimentos algébricos."""
import hashlib,json,re,sys
from pathlib import Path
import av
import numpy as np
from PIL import Image,ImageDraw
U=Path(__file__).resolve().parent
sys.path.insert(0,str(U));sys.path.insert(0,str(U.parents[1]/'videos'))
from montar_legendado import read_cues
from montar_v4 import FONT
Q=U/'qa_v4';Q.mkdir(exist_ok=True)
plan=json.loads((U/'timing_v4.json').read_text(encoding='utf-8'))
cues=read_cues(U/'legenda.srt')
assert ' '.join(' '.join(l) for _,_,l in cues).split()==(U/'texto_narracao.txt').read_text(encoding='utf-8').split()
assert all(0<=a<b and len(l)<=2 and max(FONT.getlength(s) for s in l)<=448 for a,b,l in cues)
assert all(a[1]<=b[0] for a,b in zip(cues,cues[1:]))
ops=json.loads((U/'operacoes_v4.json').read_text(encoding='utf-8'))
active={};summary=[]
for op in ops:
    if not any(t in {'TransformByGlyphMap','TransformMatchingTex'} for t in op['types']):continue
    begin=round(op['start']*30);end=round(op['end']*30)
    assert end-begin<=42,(op,begin,end)
    offset=0
    for block in plan['assembly']:
        a,b=block['frames']
        if a<=begin and end<=b:
            target=offset+begin-a
            item=dict(operation=op['index'],types=op['types'],target_frame=target,frames=end-begin,diffs=[])
            summary.append(item)
            for n in range(target+4,target+end-begin-4):active[n]=item
            break
        offset+=b-a
marks=[2,3,5,8,10,12,14,16,17,18,19,20,21,22,23,24,25,26,28,29,31,33,36,40,43,48,51,55,60,66,70,74,79,84,90,95,100,105,109,114,119,124,128,131,135,139,143,148,152,156,161,163,165,166,169]
results=[];shots=[]
for kind in ['master','legendado']:
    p=U/('preview_v4_sincronizado.mp4' if kind=='master' else 'preview_v4_legendado.mp4')
    boxes=[]
    with p.open('rb') as f:
        while f.tell()<p.stat().st_size:
            at=f.tell();head=f.read(8)
            if len(head)<8:break
            size=int.from_bytes(head[:4],'big');kind_box=head[4:].decode('ascii')
            if size==1:size=int.from_bytes(f.read(8),'big')
            boxes.append(kind_box)
            if size==0:break
            f.seek(at+size)
    assert boxes.index('moov')<boxes.index('mdat'),boxes
    with av.open(str(p)) as c:
        v,a=c.streams.video[0],c.streams.audio[0]
        m=dict(file=str(p),resolution=[v.width,v.height],fps=float(v.average_rate),video_seconds=float(v.duration*v.time_base),audio_seconds=float(a.duration*a.time_base),codec=v.codec_context.name,pix_fmt=v.codec_context.format.name,audio_codec=a.codec_context.name,audio_bitrate=a.bit_rate,bytes=p.stat().st_size)
        data=b''.join(bytes(pkt) for _,pkt in zip(range(5),c.demux(v)))
        match=re.search(rb'crf=([0-9.]+)',data);m['crf']=float(match.group(1)) if match else None
        assert (v.width,v.height)==(540,960) and m['fps']==30 and m['crf']==20 and m['pix_fmt']=='yuv420p'
        assert abs(m['video_seconds']-170.8)<.001 and abs(m['audio_seconds']-166.8)<.05
    with av.open(str(p)) as c:
        count=0;last=-1;mi=0;previous=None
        for f in c.decode(video=0):
            t=float(f.time)
            if count:assert abs(t-last-1/30)<.0001,(count,last,t)
            if kind=='legendado' and mi<len(marks) and t>=marks[mi]:
                dest=Q/f'frame_{marks[mi]:03}.jpg';f.to_image().save(dest,quality=96);shots.append((t,dest));mi+=1
            if kind=='master' and (count in active or count+1 in active):
                crop=np.asarray(f.to_image().crop((30,450,510,785)).resize((240,168)).convert('L'),dtype=np.float32)
                if count in active and previous is not None:
                    active[count]['diffs'].append(float(np.abs(crop-previous).mean()))
                previous=crop
            else:previous=None
            count+=1;last=t
        assert count==5124
        m['decoded_frames']=count
    with av.open(str(p)) as c:
        samples=sum(f.samples for f in c.decode(audio=0));m['decoded_audio_samples']=samples;assert samples/44100>=166.8
    results.append(m)
for op in summary:
    diffs=op.pop('diffs');op['mean_motion_difference']=float(np.mean(diffs)) if diffs else None
    longest=run=0
    for d in diffs:
        run=run+1 if d<.005 else 0;longest=max(longest,run)
    op['longest_near_static_run_frames']=longest
    assert longest<=6,op
for page in range((len(shots)+7)//8):
    sheet=Image.new('RGB',(1080,1010),'#050816');draw=ImageDraw.Draw(sheet)
    for j,(t,p) in enumerate(shots[page*8:(page+1)*8]):
        x=(j%4)*270;y=(j//4)*505;sheet.paste(Image.open(p).resize((270,480)),(x,y+25));draw.text((x+8,y+4),f'{t:.2f}s',fill='white')
    sheet.save(Q/f'painel_{page+1}.jpg',quality=95)
report=dict(videos=results,words=458,captions=len(cues),visual_samples=[t for t,_ in shots],math_motions=summary,method='Preview V4 a 30 fps nativos; abertura reconstruída nos tempos de fala; elemento em órbita; montagem sem retimagem.')
(Q/'validacao.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))

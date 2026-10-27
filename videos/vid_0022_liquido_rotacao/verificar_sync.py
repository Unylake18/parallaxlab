"""Verifica os previews montados e exporta legenda ASS com cores semânticas."""
import hashlib,json,re,sys
from pathlib import Path
import av
from PIL import Image,ImageDraw
U=Path(__file__).resolve().parent
sys.path.insert(0,str(U.parents[1]/'videos'))
from montar_legendado import read_cues
from sincronizar_preview import COLORS,PATTERN,FONT,SOURCE
Q=U/'qa_sync_confirmado_final'; Q.mkdir(exist_ok=True)
cues=read_cues(U/'legenda.srt')
assert ' '.join(' '.join(lines) for _,_,lines in cues).split()==(U/'texto_narracao.txt').read_text(encoding='utf-8').split()
assert all(0<=a<b and len(lines)<=2 and max(FONT.getlength(l) for l in lines)<=448 for a,b,lines in cues)
assert all(a[1]<=b[0] for a,b in zip(cues,cues[1:]))
hashfile=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
assert hashfile(U/'audio/narracao_final.wav')==hashfile('K:/Downloads/ElevenLabs_Untitled_project (20).wav')
# SRT guarda texto simples; ASS permite preservar as cores fora do MP4.
def asscolor(color):
    c=color.lstrip('#');return '&H'+c[4:6]+c[2:4]+c[0:2]+'&'
def clock(t):
    n=round(t*100); s,c=divmod(n,100);m,s=divmod(s,60);h,m=divmod(m,60);return f'{h}:{m:02}:{s:02}.{c:02}'
header='''[Script Info]
Title: POR TRÁS DA FÓRMULA · EP. 08 — Líquido em rotação
ScriptType: v4.00+
PlayResX: 540
PlayResY: 960
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Arial,27,&H00FFFFFF,&H00FFFFFF,&H00160805,&H00160805,-1,0,0,0,100,100,0,0,1,2,0,2,46,46,33,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
'''
rows=[]
for a,b,lines in cues:
    text=r'\N'.join(PATTERN.sub(lambda m:r'{\c'+asscolor(COLORS[m.group().lower()])+'}'+m.group()+r'{\c&HFFFFFF&}',line) for line in lines)
    rows.append(f'Dialogue: 0,{clock(a)},{clock(b)},Default,,0,0,0,,{text}')
(U/'legenda_colorida.ass').write_text(header+'\n'.join(rows)+'\n',encoding='utf-8-sig')
results=[]
marks=[4,10,18,24,30,36,43,51,57,66,70,74,79,84,90,95,100,105,109,114,119,124,128,131,135,139,143,148,152,154,156,159,161,163,165,166,169]
shots=[]
for name in ['preview_sincronizado.mp4','preview_legendado.mp4']:
    p=U/name
    with av.open(str(p)) as c:
        v,a=c.streams.video[0],c.streams.audio[0]
        metadata=dict(arquivo=str(p),resolucao=[v.width,v.height],fps=float(v.average_rate),duracao_video=float(v.duration*v.time_base),duracao_audio=float(a.duration*a.time_base),codec=v.codec_context.name,pix_fmt=v.codec_context.format.name,bytes=p.stat().st_size)
        packets=b''.join(bytes(pkt) for _,pkt in zip(range(5),c.demux(v)))
        crf=re.search(rb'crf=([0-9.]+)',packets);metadata['crf']=float(crf.group(1)) if crf else None
        assert metadata['crf']==14
        assert (v.width,v.height)==(540,960) and v.codec_context.format.name=='yuv420p'
    with av.open(str(p)) as c:
        count=0;last=-1;mi=0
        for f in c.decode(video=0):
            t=float(f.time)
            if count: assert abs(t-last-1/15)<.0001,(name,count,t,last)
            if name=='preview_legendado.mp4' and mi<len(marks) and t>=marks[mi]:
                dest=Q/f'quadro_{marks[mi]:03}.png';f.to_image().save(dest);shots.append((t,dest));mi+=1
            last=t;count+=1
        metadata['quadros_decodificados']=count
        assert count==2562
    with av.open(str(p)) as c:
        samples=sum(f.samples for f in c.decode(audio=0))
        metadata['amostras_audio_decodificadas']=samples
        assert samples/44100>=166.8
    results.append(metadata)
for page in range((len(shots)+5)//6):
    items=shots[page*6:(page+1)*6]
    sheet=Image.new('RGB',(810,1010),'#050816');draw=ImageDraw.Draw(sheet)
    for j,(t,path) in enumerate(items):
        x=(j%3)*270;y=(j//3)*505
        sheet.paste(Image.open(path).resize((270,480)),(x,y+25));draw.text((x+8,y+4),f'{t:.2f}s',fill='white')
    sheet.save(Q/f'painel_{page+1}.jpg',quality=95)
report=dict(videos=results,blocos_legenda=len(cues),palavras=len((U/'texto_narracao.txt').read_text(encoding='utf-8').split()),wav_sha256=hashfile(U/'audio/narracao_final.wav'),fonte_visual_sha256=hashfile(SOURCE),cores=COLORS,inspecao_tempos=[t for t,_ in shots],limite_alinhamento='Estimativa por pausas e peso silábico; sem reconhecimento automático ou alinhamento fonético. Texto da gravação confirmado pelo usuário: 458 palavras.')
(Q/'validacao.json').write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))

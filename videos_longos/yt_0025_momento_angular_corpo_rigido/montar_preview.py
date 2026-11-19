"""Concatena os oito lotes com crossfade só do conteúdo, preservando as estrelas globais."""
import json
import re
from pathlib import Path
from fractions import Fraction
import av
import numpy as np
from PIL import Image,ImageDraw

U=Path(__file__).resolve().parent
NOMES=['PH','PB1','PB2','PB3','PB4','PB5','PB6','PS']
CAPS=['COMO EXISTE TORQUE SEM AUMENTAR O GIRO?','UM L QUE SÓ VIRA','UM CORPO INTEIRO','O HALTERE TORTO','EIXO PRINCIPAL','O QUE OS MANCAIS FAZEM','A RODA','RESUMO']
def marcas(l):
    p=U/f'tempos_{l}.json'
    if p.exists():return json.loads(p.read_text(encoding='utf-8'))['inicios']
    s=(U/f'log_ped_{l}.txt').read_text(encoding='utf-8',errors='replace')
    atrasos={a:float(t) for a,t in re.findall(r'\[abertura\] (\S+) atrasada ([+0-9.-]+)',s)}
    return {a:float(t)+atrasos.get(a,0) for a,t in re.findall(r'\[ancora\] (\S+) ([0-9.]+)',s) if a!='FIM'}

def prepara_offsets():
    soma=0;offsets={}
    for n in NOMES:
        offsets[n]=soma/15
        s=(U/f'log_ped_{n}.txt').read_text(encoding='utf-8',errors='replace')
        soma+=int(re.findall(r'\[tempo\] total [0-9.]+ s \((\d+) quadros\)',s)[-1])
    (U/'offsets.json').write_text(json.dumps(offsets,indent=1),encoding='utf-8')
    return offsets

if __name__=='__main__':
    import sys
    if '--offsets' in sys.argv:
        print(prepara_offsets());raise SystemExit
    dest=U/'renders/preview_yt0025_v1_960x540.mp4';out=av.open(str(dest),'w');s=out.add_stream('libx264',rate=Fraction(15))
    s.width,s.height,s.pix_fmt=960,540,'yuv420p';s.options={'crf':'14','preset':'medium'}
    total=0;quadros={};capitulos=[];ultimo_fg=None
    patchfile=U/'patches.json';patches=json.loads(patchfile.read_text(encoding='utf-8')) if patchfile.exists() else []
    def rgba(p):
        a=np.array(Image.open(p).convert('RGBA'),float)/255
        mask=(a[:,:,3]>.05)&(a[:,:,3]<.95)
        if np.mean((a[:,:,:3].max(2)>a[:,:,3]+.015)[mask])>.10:a[:,:,:3]*=a[:,:,3,None]
        return a
    for nome,cap in zip(NOMES,CAPS):
        capitulo=total/15;capitulos.append((capitulo,cap));inicios=marcas(nome)
        quadros.update({a:total+round(t*15) for a,t in inicios.items()})
        c=av.open(str(U/f'media_{nome}/videos/cena/540p15/{nome}.mp4'))
        locais=[]
        for p in patches:
            if p['lote']!=nome:continue
            cc=av.open(str(U/p['arquivo']));it=iter(cc.decode(video=0))
            for _ in range(p.get('quadro_no_clip',0)):next(it)
            locais.append((p,cc,it))
        for i,f in enumerate(c.decode(video=0)):
            img=f.to_ndarray(format='rgb24')
            for p,cc,it in locais:
                if p['quadro_inicial']<=i<p['quadro_inicial']+p['quadros']:img=next(it).to_ndarray(format='rgb24')
            if ultimo_fg is not None and i<8:
                pasta=U/'renders/transicoes'/nome
                novo=rgba(pasta/f'fg_{i:05d}.png');bg=np.array(Image.open(pasta/f'bg_{i:05d}.png').convert('RGB'),float)/255
                u=(i+1)/8;al=ultimo_fg[:,:,3]*(1-u)+novo[:,:,3]*u
                rgb=ultimo_fg[:,:,:3]*(1-u)+novo[:,:,:3]*u+bg*(1-al[:,:,None]);img=np.uint8(np.clip(rgb*255+.5,0,255))
            for pkt in s.encode(av.VideoFrame.from_ndarray(img,format='rgb24')):out.mux(pkt)
            total+=1
        c.close()
        for p,cc,it in locais:cc.close()
        pasta=U/'renders/transicoes'/nome
        arqs=sorted(pasta.glob('fg_*.png'));ultimo_fg=rgba(arqs[-1])
        print(nome,total,flush=True)
    for pkt in s.encode():out.mux(pkt)
    out.close()
    caps='\n'.join(f'{int(t)//60}:{int(t)%60:02d} {cap}' for t,cap in capitulos)+'\n'
    (U/'capitulos_youtube.txt').write_text(caps,encoding='utf-8')
    (U/'renders/quadros.json').write_text(json.dumps(quadros,indent=1),encoding='utf-8')
    print(dest,':',total,'quadros;',total/15,'s')

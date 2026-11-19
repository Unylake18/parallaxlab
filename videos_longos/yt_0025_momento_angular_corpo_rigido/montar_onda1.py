"""Preview da onda 1 (PH + PB1 + PB3, 960×540/15 fps, sem voz) e vídeo-prova da caneta. uso: python montar_onda1.py [onda|prova]"""
import sys,json
from fractions import Fraction
from pathlib import Path
import av
U=Path(__file__).resolve().parent;R=U/'renders'
def concat(trechos,dest):
    out=av.open(str(dest),'w');s=out.add_stream('libx264',rate=Fraction(15));s.width,s.height,s.pix_fmt=960,540,'yuv420p';s.options={'crf':'14','preset':'medium'}
    n=0
    for arq,t0,t1 in trechos:
        c=av.open(str(arq))
        for i,f in enumerate(c.decode(video=0)):
            t=i/15
            if t<t0:continue
            if t1 is not None and t>=t1:break
            fr=av.VideoFrame.from_ndarray(f.to_ndarray(format='rgb24'),format='rgb24');fr.pts=None
            for p in s.encode(fr):out.mux(p)
            n+=1
        c.close()
    for p in s.encode():out.mux(p)
    out.close();return n/15
if __name__=='__main__':
    modo=sys.argv[1] if len(sys.argv)>1 else 'onda'
    if modo=='onda':
        tr=[(U/f'media_{l}/videos/cena/540p15/{l}.mp4',0,None) for l in ('PH','PB1','PB3')]
        print('onda1',concat(tr,R/'preview_yt0025_v2_onda1_960x540.mp4'),'s')
    elif modo=='completo':
        tr=[(U/f'media_{l}/videos/cena/540p15/{l}.mp4',0,None) for l in ('PH','PB1','PB2','PB3','PB4','PB5','PB6','PS')]
        print('completo',concat(tr,R/'preview_yt0025_v6_completo_960x540.mp4'),'s')
    else:
        # B1-6: do início do cancelamento (linha 2) até ω² = g/(ℓ cos θ); B2-4: m ρ² ω → L_z = I_z ω
        cfg=json.loads((U/'prova_trechos.json').read_text(encoding='utf-8'))
        tr=[(U/c['arq'],c['t0'],c['t1']) for c in cfg]
        print('prova',concat(tr,R/'prova_caneta_yt0025.mp4'),'s')

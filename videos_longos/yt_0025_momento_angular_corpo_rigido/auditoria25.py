"""Portão adicional sobre os mobjects vivos e a máscara raster do Three.js."""
from pathlib import Path
import numpy as np
from PIL import Image

def auditar(cena,t,itens,op,objs=()):
    from manim import Text,SingleStringMathTex
    from kit import AQUI,FPS
    from pecas25 import proj
    f=round(cena.clk.get_value()*FPS)
    if getattr(cena,'_audit25_f',None)==f:return
    cena._audit25_f=f
    reg=getattr(cena,'_audit25',None)
    if reg is None:reg=cena._audit25=dict(quadros=0,texto_sobre_objeto=0,fora_do_palco=0,oclusao=0)
    reg['quadros']+=1
    for m in cena.layer.get_family():
        if not hasattr(m,'_oclusao25'):continue
        reg['segmentos_checados']=reg.get('segmentos_checados',0)+1
        reg['segmentos_ocultos']=reg.get('segmentos_ocultos',0)+int(m._oclusao25)
        esperado=.35 if m._oclusao25 else 1
        if abs(float(m.get_stroke_opacity())-esperado)>.01:
            reg['oclusao']+=1
            print(f'[audit] {t:7.1f}s OCLUSÃO opacidade da seta difere do teste de profundidade')
    root=AQUI/'threejs/q3d'/f'{cena.lote}_960x540'/cena.tipo
    arq=root/'mascaras'/f'f{f:05d}.png'
    if not arq.exists() or cena._aid=='EN':return
    mask=np.asarray(Image.open(arq).convert('L'))>127
    if cena.lote.startswith('PB'):
        palco=root/'mascaras_palco'/f'f{f:05d}.png'
        mp=np.asarray(Image.open(palco).convert('L'))>127 if palco.exists() else mask
        yy,xx=np.where(mp)
        fora=(xx<36)|(xx>516)|(yy<120)|(yy>489)
        if fora.any():
            reg['fora_do_palco']+=1
            print(f'[audit] {t:7.1f}s PALCO 3D {int(fora.sum())} pixels fora da zona')
    fundos25=[f for top in cena.mobjects for f in top.get_family() if getattr(f,'_fundo',False) and f.get_fill_opacity()>.8]
    for m in itens:
        if op(m)<.6 or not isinstance(m,(Text,SingleStringMathTex)):continue
        (x0,y0,_),(x1,y1,_)=m.get_corner(np.array([-1,-1,0])),m.get_corner(np.array([1,1,0]))
        if x0>.5 or y0>2.6:continue
        a=max(0,int((x0+8)*60));b=min(960,int((x1+8)*60)+1)
        c=max(0,int((4.5-y1)*60));d=min(540,int((4.5-y0)*60)+1)
        if any(getattr(f,'_fundo',False) and f.get_left()[0]<=x0 and f.get_right()[0]>=x1 and f.get_bottom()[1]<=y0 and f.get_top()[1]>=y1 for f in fundos25):continue   # v5: texto dentro de caixa opaca (inset) não está sobre o objeto
        if b>a and d>c and mask[c:d,a:b].any():
            reg['texto_sobre_objeto']+=1
            tex=getattr(m,'tex_string',None) or getattr(m,'text','?')
            print(f'[audit] {t:7.1f}s TEXTO SOBRE OBJETO {tex[:65]!r}')

"""Medições de raster da prancha 1080p; resultados brutos para inspeção."""
import json
from pathlib import Path
import numpy as np
from PIL import Image
from scipy.ndimage import binary_erosion
U=Path(__file__).resolve().parent
bg=np.asarray(Image.open(U/'fundo_lab.png').convert('RGB'),float)/255
def lum(rgb):
    a=np.where(rgb<=.04045,rgb/12.92,((rgb+.055)/1.055)**2.4)
    return a@np.array([.2126,.7152,.0722])
out=[]
for p in sorted((U/'renders/objetos').glob('*_mask.png')):
    nome=p.stem[:-5];a=np.asarray(Image.open(p.with_name(nome+'.png')).convert('RGBA'),float)/255
    rgb=a[:,:,:3]*a[:,:,3,None]+bg*(1-a[:,:,3,None]);mask=np.asarray(Image.open(p).convert('L'))>127
    borda=mask&~binary_erosion(mask,iterations=2)
    interna=binary_erosion(mask,iterations=2)&~binary_erosion(mask,iterations=4)&(a[:,:,3]>.95)
    y,b=lum(rgb),lum(bg);ratio=np.maximum(y,b)/np.maximum(np.minimum(y,b),1e-6)
    rosa=(rgb[:,:,0]>rgb[:,:,1]*1.3)&(rgb[:,:,2]>rgb[:,:,1]*1.2)&(rgb[:,:,0]>.25)&mask
    out.append(dict(objeto=nome,pixels_borda=int(borda.sum()),contraste_borda_p10=float(np.percentile(ratio[borda],10)),contraste_borda_mediano=float(np.median(ratio[borda])),fracao_borda_acima_1_6=float((ratio[borda]>=1.6).mean()),contraste_interior_p10=float(np.percentile(ratio[interna],10)),contraste_interior_mediano=float(np.median(ratio[interna])),pixels_rosa=int(rosa.sum())))
(U/'qa/objetos_raster.json').write_text(json.dumps(out,ensure_ascii=False,indent=1),encoding='utf-8')
for x in out:print(x['objeto'],f"interior opaco: p10={x['contraste_interior_p10']:.2f}, mediana={x['contraste_interior_mediano']:.2f}; rosa={x['pixels_rosa']}")

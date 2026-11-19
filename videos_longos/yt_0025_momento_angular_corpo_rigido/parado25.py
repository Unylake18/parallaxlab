"""PARADO no conteúdo: remove estrelas por área de componente, mede o raster restante."""
import sys,json
from pathlib import Path
import av
import numpy as np
from PIL import Image
from scipy.ndimage import label,sum_labels,binary_dilation
U=Path(__file__).resolve().parent
arq=Path(sys.argv[1]) if len(sys.argv)>1 else U/'renders/preview_yt0025_v1_960x540.mp4'
nome=sys.argv[2] if len(sys.argv)>2 else 'parado'
bg=np.asarray(Image.open(U/'fundo_lab.png').convert('RGB').resize((960,540)),np.int16)
ant=None;ma=None;d=[]
with av.open(str(arq)) as c:
    for i,f in enumerate(c.decode(video=0)):
        a=f.to_ndarray(format='rgb24').astype(np.int16)
        lab,n=label(np.max(abs(a-bg),2)>18)
        tam=np.bincount(lab.ravel());keep=tam>=24;keep[0]=False
        mask=keep[lab];mask[:70]=False;mask[:,936:]=False;mask[:,:24]=False
        if ant is None:d.append(0.)
        else:
            m=binary_dilation(mask|ma,iterations=1)
            d.append(float(abs(a-ant)[m].mean()) if m.any() else 0.)
        ant=a;ma=mask
        if i and i%1500==0:print(i,'quadros analisados',flush=True)
d=np.array(d);runs=[];i=0
while i<len(d):
    if d[i]<.35:
        j=i+1
        while j<len(d) and d[j]<.35:j+=1
        if j-i>=45:runs.append(dict(inicio=i/15,fim=j/15,duracao=(j-i)/15))
        i=j
    else:i+=1
out=dict(arquivo=arq.name,quadros=len(d),metodo='MAE RGB somente em componentes de conteúdo >=24 px, excluindo o cabeçalho; estrelas isoladas removidas. Limiar 0,35 por >=3 s.',intervalos=runs)
(U/f'qa/{nome}.json').write_text(json.dumps(out,ensure_ascii=False,indent=1),encoding='utf-8');np.save(U/f'qa/{nome}.npy',d)
print(len(runs),'intervalos; inspeção pelos timestamps obrigatória')
for r in runs:print(r)

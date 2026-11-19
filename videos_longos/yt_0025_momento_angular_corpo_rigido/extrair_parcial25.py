"""Inspeção pontual dos trechos já codificados de um lote em andamento."""
import sys
from pathlib import Path
import av
from PIL import Image
U=Path(__file__).resolve().parent
l=sys.argv[1];alvos={round(float(t)*15):t for t in sys.argv[2:]};f=0
for p in sorted((U/f'media_{l}/videos/cena/540p15/partial_movie_files/{l}').glob('uncached_*.mp4')):
    try:
        with av.open(str(p)) as c:
            for fr in c.decode(video=0):
                if f in alvos:
                    out=U/f'qa/inspecao/{l}_atual_{alvos[f]}.png';Image.fromarray(fr.to_ndarray(format='rgb24')).save(out);print(out)
                    del alvos[f]
                    if not alvos:raise SystemExit
                f+=1
    except av.error.InvalidDataError:break
if alvos:print('Ainda não disponíveis:',list(alvos.values()))

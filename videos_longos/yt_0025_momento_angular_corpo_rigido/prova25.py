"""Render localizado de uma âncora para prova (sem mexer em patches.json). uso: python prova25.py LOTE ANCORA [nome_media]"""
import json,os,shutil,subprocess,sys
from pathlib import Path
U=Path(__file__).resolve().parent
lote,anc=sys.argv[1],sys.argv[2]
t=json.loads((U/f'tempos_{lote}.json').read_text(encoding='utf-8'));ordem=list(t['inicios']);j=ordem.index(anc)
primeiro=t['plays'][anc];ultimo=t['plays'][ordem[j+1]] if j+1<len(ordem) else 9999
media=U/f'media_prova_{lote}_{anc}'
for sub in ['Tex','texts']:
    dst=media/sub;dst.mkdir(parents=True,exist_ok=True)
    for raiz in [U/f'media_{lote}',U/f'media_aud_{lote}',U/f'media_ped_{lote}']:
        for src in (raiz/sub).glob('*.svg'):
            if not (dst/src.name).exists():shutil.copy2(src,dst/src.name)
env=os.environ.copy();env.update(MEDIA_DIR=str(media),PEDIDOS3D='0',AUDITORIA=os.environ.get('AUD','0'),SO_AUDITORIA='0',PYTHONIOENCODING='utf-8',CORRECAO_ANCORA25='1')
cmd=[sys.executable,'-m','manim','-r','960,540','--fps','15','--progress_bar','none','--disable_caching','-n',f'{max(0,primeiro-1)},{ultimo}','cena.py',lote]
with (U/f'log_prova_{lote}_{anc}.txt').open('w',encoding='utf-8') as log:r=subprocess.run(cmd,cwd=U,env=env,stdout=log,stderr=subprocess.STDOUT)
print(lote,anc,'rc',r.returncode,media/f'videos/cena/540p15/{lote}.mp4')

fa=media/'frames_absolutos.txt'
if fa.exists():
    ab=[int(x) for x in fa.read_text(encoding='utf-8').split()]
    (media/'offset.txt').write_text(str(ab[0]/15),encoding='utf-8');print('offset',ab[0]/15,'quadros',len(ab))

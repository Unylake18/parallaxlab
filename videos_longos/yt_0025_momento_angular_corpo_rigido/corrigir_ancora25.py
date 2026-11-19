"""Render localizado por número de play; a montagem substitui só os quadros afetados."""
import argparse,json,os,shutil,subprocess,sys
from pathlib import Path
import av
U=Path(__file__).resolve().parent
p=argparse.ArgumentParser();p.add_argument('lote');p.add_argument('ancora');a=p.parse_args()
t=json.loads((U/f'tempos_{a.lote}.json').read_text(encoding='utf-8'));ordem=list(t['inicios']);j=ordem.index(a.ancora)
assert j+1<len(ordem),'Use render normal para a última âncora'
proxima=ordem[j+1];primeiro=t['plays'][a.ancora];ultimo=t['plays'][proxima]
f0=round(t['inicios'][a.ancora]*15);esperado=round((t['inicios'][proxima]-t['inicios'][a.ancora])*15)+6
media=U/f'media_correcao_{a.lote}_{a.ancora}'
for sub in ['Tex','texts']:
    dst=media/sub;dst.mkdir(parents=True,exist_ok=True)
    for raiz in [U/f'media_{a.lote}',U/f'media_aud_{a.lote}']:
        for src in (raiz/sub).glob('*.svg'):
            if not (dst/src.name).exists():shutil.copy2(src,dst/src.name)
env=os.environ.copy();env.update(MEDIA_DIR=str(media),PEDIDOS3D='0',AUDITORIA='1',SO_AUDITORIA='0',PYTHONIOENCODING='utf-8',CORRECAO_ANCORA25='1')
cmd=[sys.executable,'-m','manim','-r','960,540','--fps','15','--progress_bar','none','--disable_caching','-n',f'{max(0,primeiro-3)},{ultimo+3}','cena.py',a.lote]
with (U/f'log_correcao_{a.ancora}.txt').open('w',encoding='utf-8') as log:r=subprocess.run(cmd,cwd=U,env=env,stdout=log,stderr=subprocess.STDOUT)
if r.returncode:raise SystemExit(r.returncode)
video=media/f'videos/cena/540p15/{a.lote}.mp4'
with av.open(str(video)) as c:n=sum(1 for _ in c.decode(video=0))
absolutos=[int(x) for x in (media/'frames_absolutos.txt').read_text(encoding='utf-8').splitlines()]
if len(absolutos)!=n:raise RuntimeError('Não substituir: divergência entre vídeo e registro de quadros')
if f0 not in absolutos:raise RuntimeError(f'Não substituir: início {f0} fora da faixa {absolutos[0]}..{absolutos[-1]}')
entrada=absolutos.index(f0)
if absolutos[entrada:entrada+esperado]!=list(range(f0,f0+esperado)):raise RuntimeError('Não substituir: a faixa absoluta não está completa')
fp=U/'patches.json';patches=json.loads(fp.read_text(encoding='utf-8')) if fp.exists() else []
patches=[x for x in patches if (x['lote'],x['ancora'])!=(a.lote,a.ancora)]
patches.append(dict(lote=a.lote,ancora=a.ancora,quadro_inicial=f0,quadro_no_clip=entrada,quadros=esperado,arquivo=video.relative_to(U).as_posix()))
fp.write_text(json.dumps(patches,ensure_ascii=False,indent=1),encoding='utf-8')
print(a.ancora,f'{n} quadros; faixa {primeiro}..{ultimo}; substituição cadastrada')

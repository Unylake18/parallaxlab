"""Lotes em ondas de até 3. Usa o ambiente validado, sem instalar dependências."""
import argparse
import concurrent.futures
import os
from pathlib import Path
import subprocess
import sys
import shutil

U=Path(__file__).resolve().parent
ROOT=U.parents[1]
LOTES=['PH','PB1','PB2','PB3','PB4','PB5','PB6','PS']
p=argparse.ArgumentParser();p.add_argument('lotes',nargs='*',default=LOTES);p.add_argument('--fase',choices=['seco','3d','render','auditoria','tudo','fechamento','validar'],default='tudo');p.add_argument('--jobs',type=int,choices=[1,2,3],default=3);args=p.parse_args()
base=os.environ.copy();base.update(PYTHONIOENCODING='utf-8',NODE_PATH=str(U.parent/'yt_0022_torque/threejs/node_modules'),CHROMIUM_PATH='C:/Program Files/Google/Chrome/Application/chrome.exe')

def run(lote,fase):
    env=base.copy();env['AUDITORIA']='0';env['SO_AUDITORIA']='0';env['MEDIA_DIR']=str(U/f'media_{lote}')
    if fase in ('seco','auditoria'):
        env['PEDIDOS3D']='1' if fase=='seco' else '0'
        env['AUDITORIA']='1' if fase=='auditoria' else '0'
        env['SO_AUDITORIA']='1'
        env['MEDIA_DIR']=str(U/f'media_{"ped" if fase=="seco" else "aud"}_{lote}')
    else:env['PEDIDOS3D']='0'
    pasta=Path(env['MEDIA_DIR'])
    for sub in ['Tex','texts']:
        destino=pasta/sub;destino.mkdir(parents=True,exist_ok=True)
        for origem in [U.parent/'yt_0024_momento_angular_particula/media'/sub,U/f'media_ped_{lote}'/sub]:
            if origem.exists() and origem!=destino:
                for arq in origem.glob('*.svg'):
                    alvo=destino/arq.name
                    if not alvo.exists():shutil.copy2(arq,alvo)
    cmd=[sys.executable,'-m','manim','-r','960,540','--fps','15','--progress_bar','none','--disable_caching']
    if fase in ('seco','auditoria'):cmd+=['--dry_run']
    cmd += ['cena.py',lote]
    if fase=='3d':cmd=['node','threejs/r3d.js','--lote',lote]
    pre={'seco':'ped_','auditoria':'aud_','3d':'3d_','render':''}[fase]
    log=U/f'log_{pre}{lote}.txt'
    with log.open('w',encoding='utf-8') as f:r=subprocess.run(cmd,cwd=U,env=env,stdout=f,stderr=subprocess.STDOUT)
    if r.returncode:raise RuntimeError(f'{lote}/{fase}: {log}\n'+log.read_text(encoding='utf-8')[-2200:])
    print(f'{lote}/{fase}: OK',flush=True)

def lote(n):
    fases={'tudo':['seco','3d','render'],'fechamento':['3d','render','auditoria'],'validar':['render','auditoria']}.get(args.fase,[args.fase])
    for f in fases:run(n,f)

with concurrent.futures.ThreadPoolExecutor(max_workers=args.jobs) as pool:
    for f in concurrent.futures.as_completed([pool.submit(lote,n) for n in args.lotes]):f.result()

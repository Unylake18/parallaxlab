"""yt_0025 · render FINAL 1920×1080 / 30 fps por lote (HANDOFF FINAL §7): pedidos 3D a 30 fps -> Three.js 1920×1080 -> Manim 1080p (CRF 14 vem do template/qualidade.py).
Sem auditoria (o QA foi feito no preview 540p). Usa o ambiente validado, sem instalar dependências.
uso: ../../.venv/Scripts/python.exe rodar25_final.py [LOTES] [--jobs N]  -> media_F_<LOTE>/videos/cena/1080p30/<LOTE>.mp4; logs log_Fped_/log_F3d_/log_F_<LOTE>.txt"""
import argparse
import concurrent.futures
import os
import shutil
import subprocess
import sys
from pathlib import Path

U = Path(__file__).resolve().parent
LOTES = ['PH', 'PB1', 'PB2', 'PB3', 'PB4', 'PB5', 'PB6', 'PS']
p = argparse.ArgumentParser()
p.add_argument('lotes', nargs='*', default=LOTES)
p.add_argument('--jobs', type=int, choices=[1, 2, 3], default=2)
p.add_argument('--fases', default='seco,3d,render')
args = p.parse_args()
base = os.environ.copy()
base.update(PYTHONIOENCODING='utf-8', FPS_RENDER='30', NODE_PATH=str(U.parent / 'yt_0022_torque/threejs/node_modules'),
            CHROMIUM_PATH='C:/Program Files/Google/Chrome/Application/chrome.exe')


def run(lote, fase):
    env = base.copy()
    env['AUDITORIA'] = '0'
    env['SO_AUDITORIA'] = '0'
    env['PEDIDOS3D'] = '1' if fase == 'seco' else '0'
    env['MEDIA_DIR'] = str(U / (f'media_Fped_{lote}' if fase == 'seco' else f'media_F_{lote}'))
    pasta = Path(env['MEDIA_DIR'])
    for sub in ['Tex', 'texts']:
        destino = pasta / sub
        destino.mkdir(parents=True, exist_ok=True)
        for origem in [U.parent / 'yt_0024_momento_angular_particula/media' / sub, U / f'media_ped_{lote}' / sub]:
            if origem.exists() and origem != destino:
                for arq in origem.glob('*.svg'):
                    alvo = destino / arq.name
                    if not alvo.exists():
                        shutil.copy2(arq, alvo)
    if fase == '3d':
        shutil.rmtree(U / 'threejs' / 'q3d' / f'{lote}_1920x1080', ignore_errors=True)
        cmd = ['node', 'threejs/r3d.js', '--lote', lote, '--w', '1920', '--h', '1080']
    else:
        cmd = [sys.executable, '-m', 'manim', '-r', '1920,1080', '--fps', '30', '--progress_bar', 'none', '--disable_caching']
        if fase == 'seco':
            cmd += ['--dry_run']
        cmd += ['cena.py', lote]
    pre = {'seco': 'Fped_', '3d': 'F3d_', 'render': 'F_'}[fase]
    log = U / f'log_{pre}{lote}.txt'
    with log.open('w', encoding='utf-8') as f:
        r = subprocess.run(cmd, cwd=U, env=env, stdout=f, stderr=subprocess.STDOUT)
    if r.returncode:
        raise RuntimeError(f'{lote}/{fase}: {log}\n' + log.read_text(encoding='utf-8')[-2200:])
    print(f'{lote}/{fase}: OK', flush=True)


def lote(n):
    for f in args.fases.split(','):
        run(n, f)


with concurrent.futures.ThreadPoolExecutor(max_workers=args.jobs) as pool:
    for f in concurrent.futures.as_completed([pool.submit(lote, n) for n in args.lotes]):
        f.result()

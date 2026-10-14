"""Previews deste asset, sem integração com Manim.

blender.exe -b -P experimentos/blender/arsenal/preview_liquido_rotacao.py -- --tipo stills
--tipo morph | rotacao | payoff | loop_qa; --frames 48 --amostras 24
Sequências PNG em previews/liquido_rotacao_rodada3/<tipo>/, a 15 fps.
--saida permite escolher outra pasta; --somente-fenomeno evita rerender de geometria nos stills.
"""
import argparse
import json
import math
import sys
import time
from pathlib import Path

import bpy
from mathutils import Matrix, Vector
from bpy_extras.object_utils import world_to_camera_view

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
sys.path.insert(0, str(AQUI.parent))
import casca_oca as co
import liquido_rotacao as lr


def montar(modo, lam):
    ficha = json.loads((AQUI / 'solidos/liquido_rotacao.json').read_text(encoding='utf-8'))
    p = {k: v['valor'] for k, v in ficha['parametros'].items()}
    p.pop('estado_visual')
    p.pop('lambda')
    co.limpar_cena()
    proxy, atualizar, apos, controle = lr.liquido_rotacao(estado_visual=modo, lam=lam, **p)
    co.mundo()
    co.luzes()
    e = ficha['enquadramento']
    cam = co.camera_enquadrada(co.cantos([proxy]), **e, largura=540, altura=960)
    apos(cam)
    return controle, atualizar, cam


def dentro_quadro(cam, ctl):
    sc = bpy.context.scene
    pontos = [Vector(((ctl.R + lr.FOLGA_VIDRO) * math.cos(a),
                      (ctl.R + lr.FOLGA_VIDRO) * math.sin(a), z))
              for z in (0, ctl.H) for a in (2 * math.pi * k / 128 for k in range(128))]
    ndc = [world_to_camera_view(sc, cam, p) for p in pontos]
    return all(0.015 < p.x < 0.985 and 0.015 < p.y < 0.985 and p.z > 0 for p in ndc)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--tipo', choices=['stills', 'morph', 'rotacao', 'payoff', 'loop_qa'], default='stills')
    ap.add_argument('--frames', type=int, default=48)
    ap.add_argument('--amostras', type=int, default=24)
    ap.add_argument('--saida', type=Path, default=AQUI / 'previews/liquido_rotacao_rodada3')
    ap.add_argument('--somente-fenomeno', action='store_true')
    args = ap.parse_args(sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else [])
    if args.frames < 2:
        ap.error('--frames deve ser pelo menos 2')
    pasta = args.saida.resolve()
    pasta.mkdir(parents=True, exist_ok=True)
    if args.tipo == 'stills':
        for nome, modo, lam in [('fenomeno_lambda0', 'fenomeno', 0.0),
                                ('fenomeno_lambda1', 'fenomeno', 1.0),
                                ('geometria_meridiana', 'geometria', 1.0)]:
            if args.somente_fenomeno and modo != 'fenomeno':
                continue
            ctl, _, cam = montar(modo, lam)
            assert dentro_quadro(cam, ctl), 'Clipping no enquadramento'
            co.render(pasta / f'{nome}.png', 540, 960, args.amostras)
        return
    modo = 'geometria' if args.tipo == 'payoff' else 'fenomeno'
    ctl, atualizar, cam = montar(modo, 0.0 if args.tipo in ('morph', 'loop_qa') else 1.0)
    pos0, rot0 = cam.location.copy(), cam.rotation_euler.copy()
    alvo = Vector((0.0, 0.0, ctl.H / 2))
    frames = pasta / args.tipo
    frames.mkdir(parents=True, exist_ok=True)
    estados, tempos = [], []
    for i in range(args.frames):
        fase = i / args.frames if args.tipo == 'loop_qa' else i / (args.frames - 1)
        if args.tipo == 'loop_qa':
            estado = {'lam': 0.5 - 0.5 * math.cos(2 * math.pi * fase), 'fase_rotacao': fase}
        else:
            estado = lr.estado_editorial(args.tipo, fase)
        ctl.estado(**estado)
        if args.tipo == 'payoff':
            giro = Matrix.Rotation(math.radians(4) * lr.suave((fase - 0.18) / 0.62), 3, 'Z')
            cam.location = alvo + giro @ (pos0 - alvo)
            cam.rotation_euler = (giro @ rot0.to_matrix()).to_euler()
        bpy.context.view_layer.update()
        if modo != 'qa':
            assert not any(o.name.startswith('Tracer') for o in bpy.data.objects), 'Tracers no modo editorial'
        assert dentro_quadro(cam, ctl), f'Clipping em {args.tipo}, frame {i+1}'
        destino = frames / f'frame_{i+1:04d}.png'
        t = time.perf_counter()
        if i == 0:
            co.render(destino, 540, 960, args.amostras)
        else:
            bpy.context.scene.render.filepath = str(destino)
            bpy.ops.render.render(write_still=True)
        tempos.append(time.perf_counter() - t)
        estados.append({'frame': i+1, 'fase': fase, **estado})
    (pasta / f'{args.tipo}_estados.json').write_text(json.dumps(
        {'fps':15, 'resolucao':[540,960], 'amostras':args.amostras,
         'segundos_render':sum(tempos), 'estados':estados}, indent=2), encoding='utf-8')
    print(f'PREVIEW {args.tipo}: {args.frames} frames, {sum(tempos):.1f}s -> {frames}', flush=True)


if __name__ == '__main__':
    main()

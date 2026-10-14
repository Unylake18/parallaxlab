"""Prepara somente os caches necessários ao preview com a ponte existente.

uv run python videos/vid_0022_liquido_rotacao/preparar_3d.py
Nenhum render em alta resolução. Projeção da seção exportada pelo próprio Blender.
"""
import json
import subprocess
import sys
from pathlib import Path

UNIT = Path(__file__).resolve().parent
ROOT = UNIT.parents[1]
sys.path.insert(0, str(UNIT))
sys.path.insert(0, str(ROOT / 'experimentos/blender/arsenal'))
from configuracao_3d import SEQUENCIAS, RES, AMOSTRAS, ALTURA_IMAGEM, CENTRO_IMAGEM
import ponte


def projetar():
    import bpy
    from mathutils import Vector
    from bpy_extras.object_utils import world_to_camera_view
    sys.path.insert(0, str(ROOT / 'experimentos/blender'))
    import casca_oca as co
    import liquido_rotacao as lr
    from construtores import CONSTRUTORES
    ficha = ponte.ler_ficha('liquido_rotacao')
    p = ponte.parametros(ficha, SEQUENCIAS['geometria']['params'], animado=False)
    co.limpar_cena()
    res = CONSTRUTORES['liquido_rotacao'](p)
    cam = co.camera_enquadrada(co.cantos(res['enquadrar']), **ficha['enquadramento'], largura=540, altura=960)
    res['apos_camera'](cam)
    def tela(xyz):
        q = world_to_camera_view(bpy.context.scene, cam, Vector(xyz))
        return [(q.x-0.5)*ALTURA_IMAGEM*540/960 + CENTRO_IMAGEM[0],
                (q.y-0.5)*ALTURA_IMAGEM + CENTRO_IMAGEM[1], 0.0]
    import math
    R, h0, dh = p['raio'], p['nivel'], p['delta_h']
    a = math.radians(p['fi_meridiana'])
    pts = lr._diametro(a, 1.0, R, h0, dh/R**2, 0.014)
    curva = [tela(pt) for pt in pts]
    z0 = h0-dh/2
    delta = [tela((R*math.cos(a),R*math.sin(a),z)) for z in (z0,z0+dh)]
    (UNIT/'projecao_3d.json').write_text(json.dumps(dict(curva=curva,delta=delta),indent=2),encoding='utf-8')


def main():
    if '--projetar' in sys.argv:
        return projetar()
    registro = {}
    for nome, kw in SEQUENCIAS.items():
        seq = ponte.sequencia('liquido_rotacao', res=RES, amostras=AMOSTRAS, **kw)
        meta = json.loads((seq.pasta/'meta.json').read_text(encoding='utf-8'))
        registro[nome] = dict(pasta=str(seq.pasta), quadros=seq.frames, segundos=meta['segundos'],
                              bytes=sum(p.stat().st_size for p in seq.pasta.glob('frame_*.png')))
    subprocess.run([ponte.encontrar_blender(),'-b','--python-exit-code','1','-P',str(Path(__file__).resolve()),
                    '--','--projetar'], check=True)
    (UNIT/'cache_3d.json').write_text(json.dumps(registro,indent=2),encoding='utf-8')
    print(json.dumps(registro,indent=2))


if __name__ == '__main__':
    main()

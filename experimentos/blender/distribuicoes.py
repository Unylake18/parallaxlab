"""Anel, disco e haste (distribuições contínuas) — estudo 7 (sandbox, não integrado a vídeo).

Rodar (sem abrir a interface), a partir da raiz do repositório:
    blender.exe -b -P experimentos/blender/distribuicoes.py

Gera out/distribuicoes_v1.png (anel, disco e haste lado a lado). Servem a duas famílias de problemas:
campo elétrico de distribuições contínuas (com cargas, eixo de simetria) e momento de inércia (aro, disco,
haste; `com_cargas=0`). Eixo de simetria opcional, tracejado neutro. Padrão visual: arsenal/estilo.json.

Convenção de eixos: o eixo de simetria do anel e do disco é X (a normal do plano); a haste fica ao longo de Y,
com o eixo de simetria (mediatriz) em X.
"""

import math
import random
import sys
from pathlib import Path

import bpy

sys.path.insert(0, str(Path(__file__).resolve().parent))
import casca_oca as co  # noqa: E402
import cilindro_macico as cm  # noqa: E402
import gaussiana as ga  # noqa: E402

D = co.ST["materiais"]["distribuicao"]
EIXO = co.ST["materiais"]["eixo"]


def vidro(obj):
    cm.material_vidro(obj, base=D["vidro_base"], ganho=D["vidro_ganho"], brilho_borda=D["vidro_brilho_borda"])


def _aplicar_rotacao(obj):
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.object.transform_apply(rotation=True)


def eixo_simetria(comprimento=5.0, offset=(0, 0, 0)):
    """Eixo de simetria (X) tracejado, em cor neutra: construção, não fonte nem campo."""
    mat = bpy.data.materials.new("EixoSimetria")
    mat.use_nodes = True
    cor = co.E.cor(EIXO["cor"])
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = co.hex_linear(cor)
    bsdf.inputs["Emission Color"].default_value = co.hex_linear(cor)
    bsdf.inputs["Emission Strength"].default_value = EIXO["emissao"]
    ox, oy, oz = offset
    m = comprimento / 2
    ga.G, g_orig = {**ga.G, "periodo_traco": EIXO["periodo"], "razao_traco": EIXO["razao"],
                    "espessura_traco": EIXO["espessura"]}, ga.G
    try:
        obj = ga.criar_curva("EixoSimetria", ga.linha((ox - m, oy, oz), (ox + m, oy, oz), False), mat)
    finally:
        ga.G = g_orig
    return obj


def criar_anel(raio=1.5, raio_tubo=0.07, n_cargas=60, com_cargas=1, eixo=0, comprimento_eixo=4.0, semente=7,
               offset=(0, 0, 0)):
    """Anel (toro fino de vidro) no plano YZ, eixo de simetria X, com cargas espaçadas ao longo do aro."""
    bpy.ops.mesh.primitive_torus_add(major_radius=raio, minor_radius=raio_tubo, major_segments=128, minor_segments=24)
    obj = bpy.context.active_object
    obj.name = "Anel"
    obj.rotation_euler = (0, math.radians(90), 0)
    _aplicar_rotacao(obj)
    bpy.ops.object.shade_smooth()
    vidro(obj)
    objs = [obj]
    if com_cargas:
        rng = random.Random(semente)
        pts = [(0.0, raio * math.cos(a), raio * math.sin(a))
               for a in (2 * math.pi * (k + rng.uniform(-D["jitter"], D["jitter"])) / n_cargas for k in range(n_cargas))]
        objs += cm.criar_cargas(pts)
    if eixo:
        objs.append(eixo_simetria(comprimento_eixo))
    for o in objs:
        o.location = tuple(o.location[i] + offset[i] for i in range(3))
    return obj, objs


def criar_disco(raio=1.8, espessura=0.06, n_cargas=110, dist_min=0.28, com_cargas=1, eixo=0, comprimento_eixo=4.0,
                semente=7, offset=(0, 0, 0)):
    """Disco fino de vidro no plano YZ (eixo X), com cargas uniformes sobre a superfície."""
    obj = cm.criar_corpo_macico(raio, espessura)
    obj.name = "Disco"
    vidro(obj)
    objs = [obj]
    if com_cargas:
        rng = random.Random(semente)
        pts, tentativas = [], 0
        while len(pts) < n_cargas and tentativas < 20000:
            tentativas += 1
            r = (raio - 0.12) * math.sqrt(rng.random())
            a = rng.uniform(0, 2 * math.pi)
            p = (0.0, r * math.cos(a), r * math.sin(a))
            if all(math.dist(p, q) >= dist_min for q in pts):
                pts.append(p)
        objs += cm.criar_cargas(pts)
    if eixo:
        objs.append(eixo_simetria(comprimento_eixo))
    for o in objs:
        o.location = tuple(o.location[i] + offset[i] for i in range(3))
    return obj, objs


def criar_haste(comprimento=4.0, raio=0.1, n_cargas=40, com_cargas=1, eixo=0, comprimento_eixo=3.0, semente=7,
                offset=(0, 0, 0)):
    """Haste fina de vidro ao longo de Y; eixo de simetria (mediatriz) em X, com cargas espaçadas ao longo dela."""
    obj = cm.criar_corpo_macico(raio, comprimento, lados=48)
    obj.name = "Haste"
    obj.rotation_euler = (0, 0, math.radians(90))      # eixo X -> Y
    _aplicar_rotacao(obj)
    vidro(obj)
    objs = [obj]
    if com_cargas:
        rng = random.Random(semente)
        passo = (comprimento - 0.3) / n_cargas
        pts = [(0.0, -comprimento / 2 + 0.15 + passo * (k + 0.5 + rng.uniform(-D["jitter"], D["jitter"])), 0.0)
               for k in range(n_cargas)]
        objs += cm.criar_cargas(pts)
    if eixo:
        objs.append(eixo_simetria(comprimento_eixo))
    for o in objs:
        o.location = tuple(o.location[i] + offset[i] for i in range(3))
    return obj, objs


def cena_trio():
    co.limpar_cena()
    # Lado a lado na MESMA profundidade: deslocamento ao longo do eixo "direita" da câmera usada abaixo.
    az, el = -45, 20
    r = math.radians(az)
    dx, dy = -math.sin(r), math.cos(r)
    d = 3.6
    anel, _ = criar_anel(offset=(-d * dx, -d * dy, 0), eixo=1)
    disco, _ = criar_disco(offset=(0, 0, 0), eixo=1)
    haste, _ = criar_haste(offset=(d * dx, d * dy, 0), eixo=1)
    co.mundo()
    co.luzes()
    cam = co.camera_enquadrada(co.cantos([anel, disco, haste]), azimute=az, elevacao=el, margem=0.08)
    cm.ajustar_profundidade(cam, disco)
    co.render(co.OUT / "distribuicoes_v1.png")


if __name__ == "__main__":
    cena_trio()

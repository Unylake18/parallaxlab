"""Capacitores de placas paralelas e esférico (Eletromagnetismo 6.5) — estudo 11 (sandbox).

Rodar: blender.exe -b -P experimentos/blender/capacitores.py   (gera out/capacitores_v1.png)

Mesma gramática do arsenal: vidro azul para os condutores, cargas azul-claro (perto) / azul (longe), ciano reservado ao
campo (não desenhado). O MESMO número de cargas em cada armadura (carga igual e oposta): o sinal não é codificado em
cor; +Q e -Q vão por rótulo no Manim.
"""

import math
import random
import sys
from pathlib import Path

import bpy

sys.path.insert(0, str(Path(__file__).resolve().parent))
import casca_oca as co  # noqa: E402
import cilindro_macico as cm  # noqa: E402
import esferas as es  # noqa: E402


def pontos_fibonacci(n, raio):
    """n pontos quase uniformes sobre a esfera de raio `raio` (espiral de Fibonacci)."""
    ouro = math.pi * (3 - math.sqrt(5))
    pts = []
    for k in range(n):
        z = 1 - 2 * (k + 0.5) / n
        r = math.sqrt(1 - z * z)
        a = ouro * k
        pts.append((raio * r * math.cos(a), raio * r * math.sin(a), raio * z))
    return pts


def _caixa(nome, escala, local=(0, 0, 0)):
    bpy.ops.mesh.primitive_cube_add(size=1, location=local)
    o = bpy.context.active_object
    o.name = nome
    o.scale = escala
    bpy.ops.object.transform_apply(scale=True)
    return o


def _proxy(escala):
    p = _caixa("ProxyEnquadramento", escala)
    p.hide_render = True
    return p


def criar_capacitor_placas(lado=3.0, distancia=1.0, espessura=0.06, n_cargas=36, dist_min=0.42, dieletrico=0, semente=7,
                           tamanho_carga=co.ST["materiais"]["carga"]["tamanho"]):
    """Duas placas de vidro (normal X) com cargas na face interna; `dieletrico=1` enche o vão com vidro claro."""
    d = distancia
    placas = []
    for s in (-1, 1):
        pl = _caixa("Placa", (espessura, lado, lado), (s * (d / 2 + espessura / 2), 0, 0))
        cm.material_vidro(pl)
        placas.append(pl)
    if dieletrico:
        di = _caixa("Dieletrico", (d, lado * 0.98, lado * 0.98))
        cm.material_vidro(di, cor=co.ST["materiais"]["otica"]["vidro_cor"], base=0.07, ganho=0.3, brilho_borda=1.0)
    rng = random.Random(semente)
    base = []
    while len(base) < n_cargas:                              # mesma distribuição nas duas armaduras (carga igual)
        for _ in range(4000):
            if len(base) >= n_cargas:
                break
            p = (rng.uniform(-lado / 2 + 0.2, lado / 2 - 0.2), rng.uniform(-lado / 2 + 0.2, lado / 2 - 0.2))
            if all(math.dist(p, q) >= dist_min for q in base):
                base.append(p)
        break
    pts = [(s * (d / 2 - tamanho_carga), y, z) for s in (-1, 1) for (y, z) in base]
    cm.criar_cargas(pts, tamanho_carga)
    proxy = _proxy((d + 2 * espessura, lado, lado))
    return proxy


def criar_capacitor_esferico(raio_a=0.8, raio_b=1.6, espessura=0.06, n_cargas=70, tamanho_carga=co.ST["materiais"]["carga"]["tamanho"],
                             corte=1):
    """Esfera condutora interna (vidro, cargas na superfície) dentro de uma casca externa com octante removido."""
    bpy.ops.mesh.primitive_uv_sphere_add(segments=96, ring_count=48, radius=raio_a)
    interna = bpy.context.active_object
    interna.name = "EsferaInterna"
    bpy.ops.object.shade_smooth()
    cm.material_vidro(interna)
    externa = es.criar_casca_esferica(raio_b, espessura, 96, 48, int(corte))
    externa.name = "CascaExterna"
    co.material_casca(externa)
    pa = pontos_fibonacci(n_cargas, raio_a)
    pb = pontos_fibonacci(n_cargas, raio_b - espessura - tamanho_carga)
    if corte:
        pb = [p for p in pb if not (p[0] > 0 and p[1] < 0 and p[2] > 0)]
    cm.criar_cargas(pa + pb, tamanho_carga)
    return externa


def cena_preview():
    co.limpar_cena()
    proxy = criar_capacitor_placas()
    co.mundo()
    co.luzes()
    cam = co.camera_enquadrada(co.cantos([proxy]), azimute=-35, elevacao=20, margem=0.09)
    cm.ajustar_profundidade(cam, proxy)
    co.render(co.OUT / "capacitores_v1.png")


if __name__ == "__main__":
    cena_preview()

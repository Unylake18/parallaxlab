"""Cilindro coaxial (condutor maciço + casca externa) — estudo 5 (sandbox, não integrado a vídeo).

Rodar (sem abrir a interface), a partir da raiz do repositório:
    blender.exe -b -P experimentos/blender/coaxial.py

Gera out/coaxial_v1.png. Modelo do capacitor coaxial (yt_0002, A4): condutor interno MACIÇO de raio a,
casca externa delgada de raio b > a, coaxiais, eixo ao longo de X. Cargas por comprimento iguais e opostas:
o MESMO número de cargas em cada superfície (a externa fica mais esparsa). O sinal não é codificado em cor.
Mesmo padrão visual dos outros sólidos (arsenal/estilo.json).
"""

import math
import random
import sys
from pathlib import Path

import bmesh
import bpy

sys.path.insert(0, str(Path(__file__).resolve().parent))
import casca_oca as co  # noqa: E402
import cilindro_macico as cm  # noqa: E402


def cortar_quadrante(obj):
    """Remove da casca a faixa angular y<0, z>0 (voltada para a câmera padrão), em todo o comprimento."""
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    faixa = [f for f in bm.faces if (c := f.calc_center_median()).y < 0 and c.z > 0]
    bmesh.ops.delete(bm, geom=faixa, context="FACES")
    bm.to_mesh(obj.data)
    bm.free()


def pontos_em_superficie(n, raio, comprimento, dist_min, margem=0.2, semente=7):
    """Pontos sobre a superfície lateral (eixo X), com distância mínima entre eles."""
    rng = random.Random(semente)
    pts, tentativas = [], 0
    while len(pts) < n and tentativas < 30000:
        tentativas += 1
        th = rng.uniform(0, 2 * math.pi)
        p = (rng.uniform(-comprimento / 2 + margem, comprimento / 2 - margem),
             raio * math.cos(th), raio * math.sin(th))
        if all(math.dist(p, q) >= dist_min for q in pts):
            pts.append(p)
    return pts


def criar_coaxial(offset=(0, 0, 0), raio_a=0.5, raio_b=1.5, comprimento=5.0, espessura=0.08,
                  n_cargas=70, dist_min=0.35, tamanho_carga=co.ST["materiais"]["carga"]["tamanho"],
                  semente=7, corte=1, lados=96):
    """Condutor interno (vidro, cargas na superfície) dentro de uma casca externa com corte longitudinal."""
    interno = cm.criar_corpo_macico(raio_a, comprimento, lados)
    interno.name = "CondutorInterno"
    cm.material_vidro(interno)

    externo = co.criar_casca_oca(raio_b, comprimento, espessura, lados)
    externo.name = "CascaExterna"
    co.material_casca(externo)
    if corte:
        cortar_quadrante(externo)

    # Mesmo número de cargas nas duas superfícies (lambda igual e oposto); as da faixa removida não são desenhadas.
    pts_a = pontos_em_superficie(n_cargas, raio_a, comprimento, dist_min, semente=semente)
    # Apoiadas sobre a face interna da casca (r = b - espessura): o centro fica tamanho_carga para dentro
    pts_b = pontos_em_superficie(n_cargas, raio_b - espessura - tamanho_carga, comprimento, dist_min, semente=semente + 4)
    if corte:
        pts_b = [p for p in pts_b if not (p[1] < 0 and p[2] > 0)]
    cargas = cm.criar_cargas(pts_a + pts_b, tamanho_carga)   # uma chamada só: um material, uma zona de profundidade

    for o in [interno, externo, *cargas]:
        o.location = (o.location[0] + offset[0], o.location[1] + offset[1], o.location[2] + offset[2])
    return interno, externo, cargas


def cena_preview():
    co.limpar_cena()
    interno, externo, _ = criar_coaxial()
    co.mundo()
    co.luzes()
    cam = co.camera_enquadrada(co.cantos([externo]))
    cm.ajustar_profundidade(cam, externo)
    bpy.ops.wm.save_as_mainfile(filepath=str(co.AQUI / "coaxial_v1.blend"))
    co.render(co.OUT / "coaxial_v1.png")


if __name__ == "__main__":
    cena_preview()

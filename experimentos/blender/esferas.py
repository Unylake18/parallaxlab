"""Casca esférica oca e esfera maciça isolante — estudo 3 (sandbox, não integrado a vídeo).

Rodar (sem abrir a interface), a partir da raiz do repositório:
    blender.exe -b -P experimentos/blender/esferas.py

Gera out/comparacao_esferas_v1.png (casca à esquerda, maciço à direita).
Mesmo padrão visual dos cilindros (arsenal/estilo.json): reaproveita materiais e câmera.
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


def _esfera_uv(raio, segmentos, aneis):
    # segmentos múltiplo de 4 e anéis pares: os planos do octante caem sobre linhas da malha (corte limpo)
    bpy.ops.mesh.primitive_uv_sphere_add(segments=segmentos, ring_count=aneis, radius=raio)
    return bpy.context.active_object


def criar_casca_esferica(raio=1.0, espessura=0.08, segmentos=96, aneis=48, corte=1):
    """Casca esférica de parede fina. Raio externo = `raio` (Solidify com offset -1 cresce para dentro).

    corte=1 remove o octante (x>0, y<0, z>0), voltado para a câmera padrão, para mostrar a parede e o
    interior vazio; o contorno do corte recebe o material de aro (destaque), como nas pontas do tubo.
    corte=0 deixa a esfera fechada (o interior não aparece).
    """
    obj = _esfera_uv(raio, segmentos, aneis)
    obj.name = "CascaEsferica"
    if corte:
        bm = bmesh.new()
        bm.from_mesh(obj.data)
        octante = [f for f in bm.faces
                   if (c := f.calc_center_median()).x > 0 and c.y < 0 and c.z > 0]
        bmesh.ops.delete(bm, geom=octante, context="FACES")
        bm.to_mesh(obj.data)
        bm.free()

    sol = obj.modifiers.new("Espessura", "SOLIDIFY")
    sol.thickness = espessura
    sol.offset = -1
    sol.use_rim = True
    sol.material_offset = 1       # face interna -> slot 1 (escuro)
    sol.material_offset_rim = 2   # aro do corte -> slot 2 (destaque)
    bpy.ops.object.shade_smooth_by_angle(angle=math.radians(30))
    return obj


def pontos_na_esfera(n, raio, dist_min, margem=0.12, semente=7):
    """Pontos uniformes no volume da bola, com distância mínima entre eles."""
    rng = random.Random(semente)
    pts, tentativas = [], 0
    rmax = raio - margem
    while len(pts) < n and tentativas < 20000:
        tentativas += 1
        r = rmax * rng.random() ** (1 / 3)          # densidade uniforme em volume
        z = rng.uniform(-1, 1)
        fi = rng.uniform(0, 2 * math.pi)
        s = math.sqrt(1 - z * z)
        p = (r * s * math.cos(fi), r * s * math.sin(fi), r * z)
        if all(math.dist(p, q) >= dist_min for q in pts):
            pts.append(p)
    return pts


def criar_esfera_macica(offset=(0, 0, 0), raio=1.0, n_cargas=70, dist_min=0.3,
                        tamanho_carga=co.ST["materiais"]["carga"]["tamanho"], semente=7,
                        segmentos=96, aneis=48, **vidro):
    """Orbe de vidro translúcido com cargas pontuais uniformes no volume."""
    corpo = _esfera_uv(raio, segmentos, aneis)
    corpo.name = "EsferaMacica"
    bpy.ops.object.shade_smooth()
    cm.material_vidro(corpo, **vidro)
    cargas = cm.criar_cargas(pontos_na_esfera(n_cargas, raio, dist_min, semente=semente), tamanho_carga)
    for o in [corpo, *cargas]:
        o.location = (o.location[0] + offset[0], o.location[1] + offset[1], o.location[2] + offset[2])
    return corpo, cargas


def cena_comparacao():
    co.limpar_cena()
    # Lado a lado na MESMA profundidade: deslocamento ao longo do eixo "direita" da câmera padrão.
    az = math.radians(co.ST["camera"]["azimute"])
    direita = (-math.sin(az), math.cos(az), 0)
    d = 1.9
    casca = criar_casca_esferica()
    co.material_casca(casca)
    casca.location = (-d * direita[0], -d * direita[1], 0)
    corpo, _ = criar_esfera_macica(offset=(d * direita[0], d * direita[1], 0))
    co.mundo()
    co.luzes()
    cam = co.camera_enquadrada(co.cantos([casca, corpo]), margem=0.1)
    cm.ajustar_profundidade(cam, corpo)
    co.render(co.OUT / "comparacao_esferas_v1.png")


if __name__ == "__main__":
    cena_comparacao()

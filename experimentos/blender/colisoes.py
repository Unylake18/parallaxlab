"""Colisão unidimensional entre dois blocos (Física I 4.10) — estudo 18 (sandbox).

Rodar: blender.exe -b -P experimentos/blender/colisoes.py   (gera out/colisoes_v1.png)

Dois blocos de vidro sobre um trilho (bloco 1 azul, bloco 2 azul-claro; o tamanho cresce com a massa). `restituicao`
(e) = 1 elástica, 0 totalmente inelástica (grudam), entre 0 e 1 parcialmente. Uma marca neutra mostra o centro de
massa, que NÃO muda de velocidade na colisão. Movimento de CICLO ÚNICO (não é loop): fase de 0 a 1 = antes, colisão
(no instante `instante`) e depois; a fase 1 é diferente da fase 0. Velocidades (setas), p e K são do Manim.
"""

import math
import sys
from pathlib import Path

import bpy

sys.path.insert(0, str(Path(__file__).resolve().parent))
import casca_oca as co  # noqa: E402
import cilindro_macico as cm  # noqa: E402
import oscilacoes as osc  # noqa: E402
import vetores3d as v3  # noqa: E402

CO = co.ST["materiais"]["colisoes"]


def velocidades_apos(m1, m2, v1, v2, e):
    v1f = ((m1 - e * m2) * v1 + (1 + e) * m2 * v2) / (m1 + m2)
    v2f = ((m2 - e * m1) * v2 + (1 + e) * m1 * v1) / (m1 + m2)
    return v1f, v2f


def criar_colisao(m1=2.0, m2=1.0, v1=3.0, v2=0.0, restituicao=1.0, instante=0.45, mostrar_cm=1, fase=0.0):
    """Colisão 1D com o contato em x = 0 no instante `instante` (fração da duração). Posições em unidades de
    comprimento por duração total. Devolve (proxy, atualizar(fase))."""
    assert v1 > v2, "para colidir é preciso v1 > v2"
    w1, w2 = 0.8 * m1 ** (1 / 3), 0.8 * m2 ** (1 / 3)
    v1f, v2f = velocidades_apos(m1, m2, v1, v2, restituicao)
    x1_0 = -w1 / 2 - v1 * instante
    x2_0 = w2 / 2 - v2 * instante

    def pos(t):
        if t <= instante:
            return x1_0 + v1 * t, x2_0 + v2 * t
        return -w1 / 2 + v1f * (t - instante), w2 / 2 + v2f * (t - instante)

    extremos = [p for t in (0.0, 1.0) for p in pos(t)]
    xmin, xmax = min(extremos) - max(w1, w2), max(extremos) + max(w1, w2)
    larg = 1.5
    trilho = osc._caixa("Trilho", (xmax - xmin, larg, 0.1), ((xmin + xmax) / 2, 0, -0.05))
    cm.material_vidro(trilho, base=CO["trilho_base"], ganho=CO["trilho_ganho"], brilho_borda=CO["trilho_brilho"])
    b1 = osc._caixa("Bloco1", (w1, w1, w1), (0, 0, w1 / 2))
    cm.material_vidro(b1, cor=CO["bloco1_cor"], base=CO["bloco_base"], ganho=CO["bloco_ganho"], brilho_borda=CO["bloco_brilho"])
    b2 = osc._caixa("Bloco2", (w2, w2, w2), (0, 0, w2 / 2))
    cm.material_vidro(b2, cor=CO["bloco2_cor"], base=CO["bloco_base"], ganho=CO["bloco_ganho"], brilho_borda=CO["bloco_brilho"])
    mat_cm = v3.material_cor("CentroMassa", "texto_neutro", CO["cm_emissao"])
    bpy.ops.mesh.primitive_uv_sphere_add(radius=CO["cm_raio"], segments=24, ring_count=12)
    cm_obj = bpy.context.active_object
    cm_obj.name = "CentroMassa"
    bpy.ops.object.shade_smooth()
    cm_obj.data.materials.append(mat_cm)
    cm_obj.hide_render = not mostrar_cm
    zc = max(w1, w2) + 0.35
    proxy = osc._caixa("ProxyEnquadramento", (xmax - xmin, larg, zc + 0.5), ((xmin + xmax) / 2, 0, (zc + 0.5) / 2 - 0.05))
    proxy.hide_render = True

    def atualizar(fase):
        x1, x2 = pos(min(max(fase, 0.0), 1.0))
        b1.location = (x1, 0, w1 / 2)
        b2.location = (x2, 0, w2 / 2)
        cm_obj.location = ((m1 * x1 + m2 * x2) / (m1 + m2), 0, zc)

    atualizar(fase)
    return proxy, atualizar


def cena_preview():
    co.limpar_cena()
    proxy, _ = criar_colisao(fase=0.2)
    co.mundo()
    co.luzes()
    co.camera_enquadrada(co.cantos([proxy]), azimute=-25, elevacao=18, margem=0.08)
    co.render(co.OUT / "colisoes_v1.png")


if __name__ == "__main__":
    cena_preview()

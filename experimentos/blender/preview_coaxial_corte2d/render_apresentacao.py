"""Quadro de apresentação do coaxial (sandbox): condutor interno, casca externa e vão, SEM setas, halos nem gaussiana.

Só reaproveita as peças do coaxial v2 (núcleo, casca com corte, contornos). Cargas: poucos marcadores esparsos (+ azul no núcleo, − magenta
na face interna da casca) só para o sinal. Saída: renders/preview_coaxial_corte2d/apresentacao.png (PNG com alpha; `renders/` é ignorado pelo Git).

    blender.exe -b -P experimentos/blender/preview_coaxial_corte2d/render_apresentacao.py
"""

import math
import sys
from pathlib import Path

import bpy

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parents[2]
sys.path.insert(0, str(AQUI.parent))
sys.path.insert(0, str(AQUI.parent / "teste_gauss_coaxial"))
import casca_oca as co  # noqa: E402
import render_sequencia_v2 as v2  # noqa: E402
import vetores3d as v3  # noqa: E402

AZ, EL, RES = -32.0, 18.0, (1120, 784)


def main():
    co.limpar_cena()
    phi = math.atan2(math.sin(math.radians(EL)), math.cos(math.radians(EL)) * math.sin(math.radians(AZ)))
    meia = math.radians(v2.CUNHA / 2)
    a0, a1 = phi + meia, phi + 2 * math.pi - meia
    m_nucleo = v2.material_metal("MetalNucleo", "fonte_escura", "fonte_contorno", 0.10)
    m_casca = v2.material_metal("MetalCasca", "fonte_escura", "fonte_contorno", 0.10)
    n = v2.nucleo()
    n.data.materials.append(m_nucleo)
    c = v2.casca_aberta(a0, a1)
    c.data.materials.append(m_casca)
    v2.arestas_luminosas(v3.material_cor("Contorno", "fonte_contorno", 0.9), a0, a1)
    mat_pos, mat_neg = v2.material_carga("CargaPos", "fonte_contorno", 1.3), v2.material_carga("CargaNeg", "apoio_magenta", 1.5)
    e_pos, e_neg = v2.esfera_base("EsferaPos"), v2.esfera_base("EsferaNeg")
    e_pos.materials.append(mat_pos)
    e_neg.materials.append(mat_neg)
    v2.cargas(e_pos, v2.reticulado(v2.A + 0.012, 0, 2 * math.pi * (1 - 1 / 10), 10, 5), 0.04)        # + só na superfície do núcleo
    v2.cargas(e_neg, v2.reticulado(v2.B - v2.T - 0.012, a0 + 0.2, a1 - 0.2, 8, 5), 0.04)             # − só na face interna da casca
    co.mundo()
    co.luzes()
    v2.camera_ortografica(co.cantos([c, n]), AZ, EL, 0.05, *RES)
    sc = bpy.context.scene
    sc.render.film_transparent = True
    sc.render.image_settings.color_mode = "RGBA"
    saida = RAIZ / "renders" / "preview_coaxial_corte2d"
    saida.mkdir(parents=True, exist_ok=True)
    co.render(saida / "apresentacao.png", *RES, 64)
    print("APRESENTACAO", saida / "apresentacao.png")


if __name__ == "__main__":
    main()

"""Coaxial 3D + corte 2D (sandbox): o 3D do coaxial limpo, agora com setas de campo que acompanham a gaussiana (campo AVALIADO) além das setas discretas do vão (campo EXISTENTE).

Reaproveita as peças do coaxial limpo (núcleo, casca com corte, símbolos, gaussiana fantasma, trajetória única) sem alterá-las. Novidade: a cada instante, com a gaussiana
no vão (a < r < b), nascem anéis de setas radiais na própria superfície gaussiana (vários planos ao longo do comprimento, ângulos uniformes), com comprimento ∝ 1/r e
limitado para não furar a casca. Fora do vão (E = 0) elas somem e as setas discretas do vão ficam em destaque; com a gaussiana no vão, as discretas ficam mais discretas.

    blender.exe -b -P experimentos/blender/preview_coaxial_3d_2d/render_3d2d.py -- [--estados]
"""

import argparse
import math
import sys
import time
from pathlib import Path

import bpy
from mathutils import Vector

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parents[2]
for extra in (AQUI.parent / "preview_coaxial_3d_limpo", AQUI.parent, AQUI.parent / "teste_gauss_coaxial"):
    sys.path.insert(0, str(extra))
import casca_oca as co  # noqa: E402
import render_limpo as RL  # noqa: E402  (coaxial limpo: símbolos, setas do vão, gaussiana, material fantasma)
import render_sequencia_v2 as v2  # noqa: E402
import vetores3d as v3  # noqa: E402
from trajetoria import A, B, RB, quadros_unicos, ss  # noqa: E402

AZ, EL, RES, MARGEM = RL.AZ, RL.EL, RL.RES, RL.MARGEM
GL = v2.GL
XS_ANEIS = (-1.05, -0.35, 0.35, 1.05)                     # planos ao longo do comprimento (dentro do cilindro gaussiano, |x| < GL/2)
K_E, FOLGA = 0.34, 0.10
ANG_PAR, ANG_IMPAR = (22, 46), (34, 56)                   # graus em relação à direção da câmera; os anéis alternam os dois conjuntos
CUNHA = 125.0                                              # abertura do corte nesta versão (a casca mantém ~65% da circunferência)                      # setas por anel, |E| ∝ K_E / r, folga até a casca
PASTA = RAIZ / "renders" / "preview_coaxial_3d_2d" / "1120x784"


def comprimento(r):
    """|E| ∝ 1/r, limitado para a seta não furar a casca externa (a seta nasce em r e termina antes de b)."""
    return min(K_E / r, B - FOLGA - r)


def aneis(mat, r, phi):
    """Anéis de setas radiais na superfície gaussiana (campo avaliado). Os ângulos próximos à direção da câmera são omitidos (seta de frente)."""
    comp = comprimento(r)
    if comp < 0.04:
        return []
    out = []
    for i, x in enumerate(XS_ANEIS):
        for sg in (-1, 1):
            for dg in (ANG_PAR if i % 2 == 0 else ANG_IMPAR):                        # só ângulos visíveis pela janela do corte (sem seta de frente nem atrás do núcleo)
                t = phi + sg * math.radians(dg)
                d = Vector((0, math.cos(t), math.sin(t)))
                s = v3.seta(Vector((x, 0, 0)) + r * d, d, mat, comprimento=comp)
                s.scale = (0.8, 0.8, comp)
                out.append(s)
    return out


def coroas(c, r, phi):
    """Estilo 'coroa' (opcional): setas planas em duas coroas na gaussiana: frente (completa, 12) e fundo (só por fora, 8), como nos cilindros do preview_todos_3d2d."""
    import render_todos_3d2d as R3                                              # setas planas (constante na tela) do preview_todos_3d2d
    L = max(comprimento(r), 0.0)
    L = max(L, 0.14) * R3.CA.ss(L / 0.08)
    if L < 0.02:
        return []
    meio = v2.GL / 2
    out = []
    for x, dgs in ((meio, [30 * j for j in range(12)]), (-meio, (-120, -90, -60, -30, 30, 60, 90, 120))):
        for dg in dgs:
            t = phi + math.radians(dg)
            d = Vector((0, math.cos(t), math.sin(t)))
            out.append(R3.seta_plana(c, Vector((x, 0, 0)) + r * d, d, L, c.m_aval))
    return [o for o in out if o is not None]


class Ctx:
    pass


def main():
    resto = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    ap = argparse.ArgumentParser()
    ap.add_argument("--estados", action="store_true")
    ap.add_argument("--amostras", type=int, default=64)
    ap.add_argument("--coroa", action="store_true", help="setas planas em coroas (frente + fundo) no lugar dos anéis; o campo existente do vão some quando a gaussiana está nele")
    a = ap.parse_args(resto)
    pasta = PASTA.parent / ("_estados_coroa" if a.coroa else "_estados") if a.estados else (PASTA.parent / "1120x784_coroa" if a.coroa else PASTA)
    pasta.mkdir(parents=True, exist_ok=True)

    co.limpar_cena()
    c = Ctx()
    c.m_fant = RL.material_fantasma()
    c.m_traco = RL.ga.material_traco()
    c.m_traco.node_tree.nodes["Principled BSDF"].inputs["Emission Strength"].default_value = 1.4
    c.m_traco2 = RL.ga.material_traco()
    c.m_traco2.node_tree.nodes["Principled BSDF"].inputs["Emission Strength"].default_value = 0.8
    phi = math.atan2(math.sin(math.radians(EL)), math.cos(math.radians(EL)) * math.sin(math.radians(AZ)))
    meia = math.radians(CUNHA / 2)
    a0, a1 = phi + meia, phi + 2 * math.pi - meia
    m_nucleo = v2.material_metal("MetalNucleo", "fonte_escura", "fonte_contorno", 0.10, translucido=True)
    m_casca = v2.material_metal("MetalCasca", "fonte_escura", "fonte_contorno", 0.10)
    n = v2.nucleo()
    n.data.materials.append(m_nucleo)
    cs = v2.casca_aberta(a0, a1)
    cs.data.materials.append(m_casca)
    v2.arestas_luminosas(v3.material_cor("Contorno", "fonte_contorno", 0.8), a0, a1)
    estaticas = RL.setas_do_vao(phi)                                             # campo existente (discreto), 4 setas no plano x = 1,7
    m_estatica = estaticas[0].material_slots[0].material
    m_aval = v3.material_cor("CampoAvaliado", "campo_eletrico", 2.4)             # campo avaliado: na superfície gaussiana
    c.m_aval = m_aval
    co.mundo()
    co.luzes()
    if a.coroa:
        sys.path.insert(0, str(AQUI.parent / "preview_todos_3d2d"))
        import render_todos_3d2d as R3                                          # noqa: E402  (Geo da câmera e setas planas)
        c.g = R3.RT.Geo(AZ, EL)
    maxima = RL.gaussiana(c, RB, phi)                                            # enquadramento pelo MAIOR raio da gaussiana
    pontos = co.cantos([cs, n, maxima[-1]])
    RL.remover(maxima)
    cam = v2.camera_ortografica(pontos, AZ, EL, MARGEM, *RES)
    RL.simbolos(cam, phi, a0, a1)
    sc = bpy.context.scene
    sc.render.film_transparent = True
    sc.render.image_settings.color_mode = "RGBA"
    co.render(pasta / "_aq.png", *RES, a.amostras)
    (pasta / "_aq.png").unlink()

    todos = quadros_unicos()
    if a.estados:
        todos = [q for q in todos if q[0] in ("intro", "h0", "h1", "h2", "m1_040", "m2_020")]
    t0 = time.perf_counter()
    for chave, r in todos:
        ativo = r is not None and A - 1e-3 <= r <= B + 1e-3                      # mesma condição do texto de região no Manim
        v2.escurecer(m_nucleo, 1.0, 1.0 if r is None else 0.55 + 0.45 * ss((r - (A - 0.05)) / 0.14))
        m_estatica.node_tree.nodes["Principled BSDF"].inputs["Emission Strength"].default_value = 0.7 if ativo else 1.8
        objs = [] if r is None else RL.gaussiana(c, r, phi)
        if a.coroa:
            for o in estaticas:
                o.hide_render = ativo                                            # sem as setas "de dentro" enquanto as coroas estão ativas
            if ativo:
                objs += coroas(c, r, phi)
        elif ativo:
            objs += aneis(m_aval, r, phi)
        sc.render.filepath = str(pasta / f"q_{chave}.png")
        bpy.ops.render.render(write_still=True)
        RL.remover(objs)
    print(f"3D2D quadros={len(todos)} total={time.perf_counter() - t0:.1f}s medio={(time.perf_counter() - t0) / len(todos):.2f}s -> {pasta}")


if __name__ == "__main__":
    main()

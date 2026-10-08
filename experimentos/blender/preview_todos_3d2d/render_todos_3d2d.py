"""Os casos de Gauss no padrão 3D + corte 2D (sandbox; não altera o arsenal nem o yt_0002): o 3D do `preview_todos_limpo` com setas de campo que acompanham a gaussiana.

Reaproveita os construtores de `preview_todos_limpo/render_todos.py` (sólidos, símbolos, setas do campo existente, gaussianas) e acrescenta, a cada instante, as setas do
campo AVALIADO na própria superfície gaussiana (comprimento ∝ |E|, regras em campo_aval.py): cilindros, anéis ao longo do comprimento; esferas, anéis em três cones;
planos, grade nas tampas do pillbox. Onde E = 0 elas somem; as setas do campo existente ficam em destaque ali e discretas quando as avaliadas aparecem.

    blender.exe -b -P experimentos/blender/preview_todos_3d2d/render_todos_3d2d.py -- --caso todos [--estados]
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
for extra in (AQUI, AQUI.parent / "preview_todos_limpo", AQUI.parent / "preview_coaxial_3d_limpo", AQUI.parent, AQUI.parent / "teste_gauss_coaxial"):
    sys.path.insert(0, str(extra))
import campo_aval as CA  # noqa: E402
import casca_oca as co  # noqa: E402
import render_todos as RT  # noqa: E402  (construtores dos casos do preview limpo)
import render_sequencia_v2 as v2  # noqa: E402
import vetores3d as v3  # noqa: E402
from traj_gen import CASOS, Traj  # noqa: E402

PASTA = RAIZ / "renders" / "preview_todos_3d2d"
RES = RT.RES
CIL, PLAN, ESF = ("linha", "casca_cil", "macico_cil"), ("folha", "placa", "duas", "face"), ("casca_esf", "macico_esf", "cap_esf")
XS_ANEIS = (-1.0, 0.0, 1.0)
ESTILO_CIL = "coroa_fb"                                                         # cilindros: coroa completa na frente + coroa "por fora" no fundo (atual | coroa | coroa3 | coroa_fb | ...)
LOSANGO = {"folha": 0.75, "placa": 0.75, "duas": 0.75, "face": 0.55}          # meia-diagonal da grade de setas nas tampas (cabe dentro do pillbox)
ANEL_ESF = [(0, 12, 0), (40, 6, 15)]            # (inclinação em graus a partir do plano perpendicular à câmera, nº de setas, fase em graus): borda + anel interno intercalado


def seta_plana(c, origem, d, L, mat, w=0.017, wh=0.058, hh=0.15):
    """Seta 2D (plana, paralela ao plano da imagem): comprimento L na própria tela, sem encurtamento de perspectiva; direção = projeção de d.
    Setas quase de frente (projeção < 0,2) não são desenhadas. Nasce no ponto 3D `origem`, levemente adiantada em direção à câmera."""
    g = c.g
    ux, uy = d.dot(g.right), d.dot(g.up)
    n = math.hypot(ux, uy)
    if n < 0.2 or L < 0.02:
        return None
    s_ = (ux * g.right + uy * g.up) / n
    t_ = g.v.cross(s_)
    h = min(hh, 0.5 * L)
    pts = [(0, -w), (L - h, -w), (L - h, -wh), (L, 0.0), (L - h, wh), (L - h, w), (0, w)]
    verts = [origem + 0.05 * g.v + a * s_ + b * t_ for a, b in pts]
    me = bpy.data.meshes.new("SetaPlana")
    me.from_pydata([tuple(v) for v in verts], [], [(0, 1, 5, 6), (2, 3, 4)])
    me.materials.append(mat)
    o = bpy.data.objects.new("SetaPlana", me)
    bpy.context.collection.objects.link(o)
    return o


def seta_existente(c, origem, d, comp):
    """Substitui RT.seta: o campo existente também em setas planas (mesmo estilo, um pouco mais finas)."""
    o = seta_plana(c, origem, d, comp, c.m_campo, w=0.013, wh=0.05, hh=0.13)
    if o is not None:
        c.existentes.append(o)
    return o


def setas_avaliadas(c, g, cid, p):
    """Setas do campo avaliado na superfície gaussiana (comprimento ∝ |E|), planas e de tamanho constante na tela."""
    k = CA.comp_vis(cid, p)
    if k <= 0:
        return []
    out = []
    ad = lambda o, d: out.append(seta_plana(c, o, d, k, c.m_aval))           # noqa: E731
    if cid in CIL:                                                              # setas radiais na gaussiana cilíndrica (estilo escolhido em ESTILO_CIL)
        meio = v2.GL / 2

        def anel(x, n, fase=0.0):
            for j in range(n):
                t = math.radians(fase) + 2 * math.pi * j / n
                d = Vector((0, math.cos(t), math.sin(t)))
                ad(Vector((x, 0, 0)) + p * d, d)
        if ESTILO_CIL == "coroa":                                               # uma coroa na circunferência da tampa frontal
            anel(meio, 12)
        elif ESTILO_CIL in ("coroa3", "coroa_fb"):                                            # três coroas alinhadas: tampa frontal, meio e fundo (fileiras ao longo da superfície)
            anel(meio, 12, math.degrees(g.phi))                                 # frente: coroa completa (alinhada à câmera)
            for x in ((-meio,) if ESTILO_CIL == "coroa_fb" else (0.0, -meio)):  # meio e fundo (ou só fundo): só as setas "por fora" (bordas de cima e de baixo)
                for dg in (-120, -90, -60, -30, 30, 60, 90, 120):                       # lado de fora da coroa (as de 150–180° ficam sobre o corpo)
                    t = g.phi + math.radians(dg)
                    d = Vector((0, math.cos(t), math.sin(t)))
                    ad(Vector((x, 0, 0)) + p * d, d)
        elif ESTILO_CIL == "coroa2":                                            # coroa na tampa frontal + coroa intercalada no meio do comprimento
            anel(meio, 10)
            anel(0.0, 10, 18)
        elif ESTILO_CIL == "malha":                                             # grade na metade visível: 2 fileiras × 5 ângulos
            for x in (-0.7, 0.7):
                for dg in (-80, -40, 40, 80):
                    t = g.phi + math.radians(dg)
                    d = Vector((0, math.cos(t), math.sin(t)))
                    ad(Vector((x, 0, 0)) + p * d, d)
        else:
            for x, dgs in zip(XS_ANEIS, ((90,), (50,), (90,))):
                for sg in (-1, 1):
                    for dg in dgs:
                        t = g.phi + sg * math.radians(dg)
                        d = Vector((0, math.cos(t), math.sin(t)))
                        ad(Vector((x, 0, 0)) + p * d, d)
    elif cid in PLAN:                                                           # campo ⟂ às tampas do pillbox, grade em losango
        h = LOSANGO[cid]
        for y, z in ((-h, 0.0), (h, 0.0), (0.0, -h), (0.0, h)):
            ad(Vector((p, y, z)), Vector((1, 0, 0)))                            # tampa direita (campo para +x)
            if cid in ("folha", "placa"):
                ad(Vector((-p, y, z)), Vector((-1, 0, 0)))                      # tampa esquerda (campo para −x)
    else:                                                                       # esferas: anel de borda (12) + anel interno intercalado (6)
        for alfa, n, fase in ANEL_ESF:
            for j in range(n):
                th = math.radians(fase) + 2 * math.pi * j / n
                d = math.cos(math.radians(alfa)) * g.dir_plano(th) + math.sin(math.radians(alfa)) * g.v
                ad(p * d, d)
    return [o for o in out if o is not None]


def renderizar(cid, args):
    spec = CASOS[cid]
    T = Traj(spec["wps"])
    pmax = max(p for p, _ in spec["wps"])
    pasta = (PASTA / ("_estados" if ESTILO_CIL == "atual" else "_estilos_" + ESTILO_CIL) / cid) if args.estados else (PASTA / cid / "1120x784")
    pasta.mkdir(parents=True, exist_ok=True)
    co.limpar_cena()
    c, g = RT.Ctx(), RT.Geo(spec["az"], spec["el"])
    RT.preparar(c)
    c.g = g
    c.existentes = []
    RT.seta = seta_existente                                                     # campo existente em setas planas (os builders chamam RT.seta)
    c.m_aval = v3.material_cor("CampoAvaliado", "campo_eletrico", 2.4)
    d = RT.BUILD[cid](c, g)
    co.mundo()
    co.luzes()
    tmp = d["gauss"](pmax)
    if "pts" in d:
        pontos = d["pts"](pmax)
    else:
        pontos = co.cantos([o for o in d["enq"] if o.type in ("MESH", "CURVE")] + [o for o in tmp if o.type == "MESH"])
    RT.RLp.remover(tmp)
    cam = v2.camera_ortografica(pontos, spec["az"], spec["el"], spec["margem"], *RES)
    RT.sinais(c, cam, d["sinais"])
    sc = bpy.context.scene
    sc.render.film_transparent = True
    sc.render.image_settings.color_mode = "RGBA"
    co.render(pasta / "_aq.png", *RES, args.amostras)
    (pasta / "_aq.png").unlink()
    todos = T.quadros_unicos()
    if args.estados:
        todos = [q for q in todos if q[0] in ("intro", "h0", "h1", "h2", "m1_040", "m2_020")]
    t0 = time.perf_counter()
    for chave, p in todos:
        if "pre" in d and p is not None:
            d["pre"](p)
        f = 0.0 if p is None else CA.fator(cid, p) if CA.ativo(cid, p) else 0.0
        c.m_campo.node_tree.nodes["Principled BSDF"].inputs["Emission Strength"].default_value = 1.8 - 1.1 * f     # campo existente: em destaque × discreto (rampa)
        if cid in CIL and ESTILO_CIL in ("coroa", "coroa3", "coroa_fb"):                                # cilindros: com a coroa, só ela (fora); o campo existente (dentro) some
            for o in c.existentes:
                o.hide_render = f > 0.02
        objs = [] if p is None else d["gauss"](p)
        if p is not None:
            objs += setas_avaliadas(c, g, cid, p)
        sc.render.filepath = str(pasta / f"q_{chave}.png")
        bpy.ops.render.render(write_still=True)
        RT.RLp.remover(objs)
    print(f"T3D2D {cid} quadros={len(todos)} total={time.perf_counter() - t0:.1f}s medio={(time.perf_counter() - t0) / len(todos):.2f}s")


def main():
    resto = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    ap = argparse.ArgumentParser()
    ap.add_argument("--caso", default="todos")
    ap.add_argument("--estados", action="store_true")
    ap.add_argument("--estilo", default="coroa_fb")
    ap.add_argument("--amostras", type=int, default=64)
    a = ap.parse_args(resto)
    global ESTILO_CIL
    ESTILO_CIL = a.estilo
    for cid in (list(CASOS) if a.caso == "todos" else a.caso.split(",")):
        renderizar(cid, a)


if __name__ == "__main__":
    main()

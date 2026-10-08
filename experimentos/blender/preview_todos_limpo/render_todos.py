"""Os casos de Gauss do vídeo no padrão do coaxial limpo (sandbox; não altera o arsenal nem o yt_0002).

Por caso: sólido 3D permanente (câmera ortográfica fixa), poucos símbolos + (azul) e − (magenta) nas superfícies/volume certos, 4 a 6 setas de campo
iguais num único plano, e uma gaussiana fantasma (cilindro, esfera ou pillbox) que varia só o parâmetro p, renderizada nos instantes reais do vídeo
(traj_gen.py: um quadro por instante em movimento, um por pausa). Reaproveita as peças do coaxial limpo; só importa, não altera.

    blender.exe -b -P experimentos/blender/preview_todos_limpo/render_todos.py -- --caso todos [--estados]
"""

import argparse
import math
import sys
import time
from pathlib import Path

import bmesh
import bpy
from mathutils import Vector

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parents[2]
for extra in (AQUI, AQUI.parent, AQUI.parent / "teste_gauss_coaxial", AQUI.parent / "preview_coaxial_3d_limpo"):
    sys.path.insert(0, str(extra))
import casca_oca as co  # noqa: E402
import cilindro_macico as cm  # noqa: E402
import gaussiana as ga  # noqa: E402
import placa as pl  # noqa: E402
import render_limpo as RLp  # noqa: E402  (símbolos, gaussiana cilíndrica e material fantasma do coaxial limpo)
import render_sequencia_v2 as v2  # noqa: E402
import vetores3d as v3  # noqa: E402
from traj_gen import CASOS, Traj, ss  # noqa: E402

L, GL = v2.L, v2.GL
RES = (1120, 784)
PASTA = RAIZ / "renders" / "preview_todos_limpo"


class Ctx:
    pass


class Geo:
    """Câmera ortográfica fixa: direção para a câmera, base da imagem (direita, cima) e fase do corte nos cilindros."""

    def __init__(self, az, el):
        a, e = math.radians(az), math.radians(el)
        self.az, self.el = az, el
        self.v = Vector((math.cos(e) * math.cos(a), math.cos(e) * math.sin(a), math.sin(e)))
        self.up = (Vector((0, 0, 1)) - self.v * self.v.z).normalized()
        self.right = (-self.v).cross(self.up).normalized()
        self.phi = math.atan2(math.sin(e), math.cos(e) * math.sin(a))
        self.n = Vector((0, math.cos(self.phi), math.sin(self.phi)))          # direção radial (YZ) voltada para a câmera

    def dir_plano(self, ang):
        return math.cos(ang) * self.right + math.sin(ang) * self.up


def preparar(c):
    c.m_fant = RLp.material_fantasma()
    c.m_traco = ga.material_traco()
    c.m_traco.node_tree.nodes["Principled BSDF"].inputs["Emission Strength"].default_value = 1.4
    c.m_traco2 = ga.material_traco()
    c.m_traco2.node_tree.nodes["Principled BSDF"].inputs["Emission Strength"].default_value = 0.8
    c.m_campo = v3.material_cor("CampoE", "campo_eletrico", 1.1)
    c.m_borda = v3.material_cor("Contorno", "fonte_contorno", 0.8)
    c.m_fio = v3.material_cor("Fio", "fonte_fisica", 1.4)
    c.mp, c.mn = RLp.malha_sinal("Mais", True), RLp.malha_sinal("Menos", False)
    c.mp.materials.append(v2.material_carga("SinalPos", "fonte_contorno", 1.2))
    c.mn.materials.append(v2.material_carga("SinalNeg", "apoio_magenta", 1.4))
    c.metal = lambda nome, trans=False: v2.material_metal(nome, "fonte_escura", "fonte_contorno", 0.10, translucido=trans)


def sinais(c, cam, lista):
    rot = cam.rotation_euler.copy()                                             # símbolos paralelos ao plano da imagem
    for pos, sg in lista:
        o = bpy.data.objects.new("Sinal", c.mp if sg == "+" else c.mn)
        o.location = pos
        o.rotation_euler = rot
        bpy.context.collection.objects.link(o)


def seta(c, origem, d, comp):
    s = v3.seta(origem, d, c.m_campo, comprimento=comp)
    s.scale = (0.55, 0.55, comp)
    return s


def seta_cil(c, g, x, r0, comp, graus):
    """Setas radiais num único plano transversal x = const (cilindros)."""
    for dg in graus:
        t = g.phi + math.radians(dg)
        d = Vector((0, math.cos(t), math.sin(t)))
        seta(c, Vector((x, 0, 0)) + r0 * d, d, comp)


def seta_anel(c, g, r0, comp, n=6):
    """Setas radiais num plano perpendicular à câmera, pelo centro (esferas): aparecem inteiras, sem encurtamento."""
    for k in range(n):
        d = g.dir_plano(2 * math.pi * k / n)
        seta(c, r0 * d, d, comp)


def cil_x(raio, comprimento, nome):
    bpy.ops.mesh.primitive_cylinder_add(vertices=64, radius=raio, depth=comprimento, end_fill_type="NGON")
    o = bpy.context.active_object
    o.name = nome
    o.rotation_euler = (0, math.radians(90), 0)
    bpy.ops.object.transform_apply(rotation=True)
    bpy.ops.object.shade_smooth()
    return o


def caixa(nome, x0, x1, hy, hz):
    bpy.ops.mesh.primitive_cube_add(size=1, location=((x0 + x1) / 2, 0, 0))
    o = bpy.context.active_object
    o.name = nome
    o.scale = (x1 - x0, 2 * hy, 2 * hz)
    bpy.ops.object.transform_apply(scale=True)
    return o


def contorno_caixa(c, x0, x1, hy, hz):
    pts = [(x, sy * hy, sz * hz) for x in (x0, x1) for sy in (-1, 1) for sz in (-1, 1)]
    idx = {p: i for i, p in enumerate(pts)}
    ar = [([a, b], False) for a in pts for b in pts if idx[a] < idx[b] and sum(1 for i in range(3) if a[i] != b[i]) == 1]
    return v3.curva("ContornoCaixa", ar, c.m_borda, 0.011)


def esfera_uv(raio, nome):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=raio, segments=64, ring_count=32)
    o = bpy.context.active_object
    o.name = nome
    bpy.ops.object.shade_smooth()
    return o


def casca_esf_cone(c, g, R, T, cone, mat):
    """Casca esférica oca com abertura circular voltada para a câmera (meio ângulo `cone`), com contorno nas duas bordas."""
    o = esfera_uv(R, "CascaEsf")
    bm = bmesh.new()
    bm.from_mesh(o.data)
    cosc = math.cos(math.radians(cone))
    bmesh.ops.delete(bm, geom=[f for f in bm.faces if f.calc_center_median().normalized().dot(g.v) > cosc], context="FACES")
    bm.to_mesh(o.data)
    bm.free()
    sol = o.modifiers.new("Esp", "SOLIDIFY")
    sol.thickness, sol.offset, sol.use_rim = T, -1, True
    o.data.materials.append(mat)
    sc_, sn_ = math.cos(math.radians(cone)), math.sin(math.radians(cone))
    for raio in (R, R - T):
        pts = [raio * (sc_ * g.v + sn_ * g.dir_plano(2 * math.pi * k / 96)) for k in range(96)]
        v3.curva("BordaCasca", [(pts, True)], c.m_borda, 0.011)
    return o


def gauss_cil(c, g, r):
    return RLp.gaussiana(c, r, g.phi)


def gauss_esf(c, g, r):
    """Três grandes círculos: a metade voltada à câmera contínua, a de trás tracejada; preenchimento quase invisível."""
    corpo = esfera_uv(r, "GaussEsf")
    corpo.data.materials.append(c.m_fant)
    frente, tras = [], []
    for u, w in (((1, 0, 0), (0, 1, 0)), ((1, 0, 0), (0, 0, 1)), ((0, 1, 0), (0, 0, 1))):
        pts = [r * (math.cos(2 * math.pi * k / 120) * Vector(u) + math.sin(2 * math.pi * k / 120) * Vector(w)) for k in range(121)]
        run, lado = [pts[0]], pts[0].dot(g.v) > 0
        for p in pts[1:]:
            s = p.dot(g.v) > 0
            if s == lado:
                run.append(p)
                continue
            (frente.append((run, False)) if lado else tras.extend(v3.tracejado(run, False, 0.22, 0.55)))
            run, lado = [run[-1], p], s
        (frente.append((run, False)) if lado else tras.extend(v3.tracejado(run, False, 0.22, 0.55)))
    return [ga.criar_curva("GFrente", frente, c.m_traco, 0.012), ga.criar_curva("GTras", tras, c.m_traco2, 0.008), corpo]


def pillbox(c, xl, xr, h):
    """Tampa direita (mais perto da câmera) contínua; a esquerda e as arestas laterais tracejadas; preenchimento quase invisível."""
    quad = lambda x: [(x, -h, -h), (x, h, -h), (x, h, h), (x, -h, h)]  # noqa: E731
    tras = v3.tracejado(quad(xl), True, 0.26, 0.6)
    for k in range(4):
        tras += ga.linha(quad(xl)[k], quad(xr)[k], False)
    corpo = caixa("PillFaces", xl, xr, h, h)
    corpo.data.materials.append(c.m_fant)
    return [ga.criar_curva("GFrente", [(quad(xr), True)], c.m_traco, 0.012), ga.criar_curva("GTras", tras, c.m_traco2, 0.008), corpo]


def painel(c, x, cor, LW=6.8, AH=4.8):
    f = pl.criar_placa(LW, AH, 0.04)
    f.location = (x, 0, 0)
    pl.material_placa(f, LW, AH, 0, cor=cor, base=0.30, ganho=0.5, fade_inicio=0.74)
    hy, hz = 0.80 * LW / 2, 0.80 * AH / 2
    borda = v3.material_cor("Borda" + cor, "fonte_contorno" if cor == "fonte_fisica" else "apoio_magenta", 0.8)
    v3.curva("ContornoFolha", [([(x, -hy, -hz), (x, hy, -hz), (x, hy, hz), (x, -hy, hz)], True)], borda, 0.010)
    return f


QUINCUNCIO = [(-1.8, -0.9), (0.0, -0.9), (1.8, -0.9), (-0.9, 0.0), (0.9, 0.0), (-1.8, 0.9), (0.0, 0.9), (1.8, 0.9)]
ARR4 = [(-0.6, -0.5), (-0.6, 0.5), (0.6, -0.5), (0.6, 0.5)]                   # (y, z) das 4 setas de campo dos casos planares


# ── casos ───────────────────────────────────────────────────────────────────
def caso_linha(c, g):
    fio = cil_x(0.03, L, "Fio")
    fio.data.materials.append(c.m_fio)
    seta_cil(c, g, 1.7, 0.55, 0.45, (-90, -45, 45, 90))
    lista = [(Vector((x, 0, 0)) + 0.15 * g.n, "+") for x in (-2.0, -1.0, 0.0, 1.0, 2.0)]
    return dict(enq=[fio], sinais=lista, gauss=lambda p: gauss_cil(c, g, p))


def caso_casca_cil(c, g):
    R, T = 1.0, v2.T
    meia = math.radians(v2.CUNHA / 2)
    a0, a1 = g.phi + meia, g.phi + 2 * math.pi - meia
    antigo, v2.B = v2.B, R
    casca = v2.casca_aberta(a0, a1)
    v2.B = antigo
    casca.data.materials.append(c.metal("MetalCasca"))
    pl_ = []
    for x in (-L / 2, L / 2):
        pl_ += [([(x, raio * math.cos(a0 + (a1 - a0) * k / 64), raio * math.sin(a0 + (a1 - a0) * k / 64)) for k in range(65)], False) for raio in (R, R - T)]
    for ang in (a0, a1):
        for raio in (R, R - T):
            pl_.append(([(-L / 2, raio * math.cos(ang), raio * math.sin(ang)), (L / 2, raio * math.cos(ang), raio * math.sin(ang))], False))
    v3.curva("ContornoCasca", pl_, c.m_borda, 0.011)
    seta_cil(c, g, 1.7, 1.15, 0.42, (-90, -45, 45, 90))
    lista = []
    for x in (-1.5, -0.5, 0.5, 1.5):                                           # + na superfície externa, nas faixas visíveis (±70° da direção da câmera)
        for sg in (-1, 1):
            t = g.phi + sg * math.radians(70)
            lista.append((Vector((x, 0, 0)) + (R + 0.09) * Vector((0, math.cos(t), math.sin(t))), "+"))
    return dict(enq=[casca], sinais=lista, gauss=lambda p: gauss_cil(c, g, p))


def caso_macico_cil(c, g):
    R = 1.0
    corpo = cm.criar_corpo_macico(R, L)
    cm.material_vidro(corpo)
    seta_cil(c, g, 1.7, 1.15, 0.42, (-90, -45, 45, 90))
    lista = []
    for x, rho, dth in ((-1.5, 0.7, -30), (-0.9, 0.45, 40), (-0.3, 0.75, -5), (0.3, 0.4, -45), (0.9, 0.7, 35), (1.5, 0.5, 0), (-0.6, 0.55, 150), (0.6, 0.6, -140)):
        t = g.phi + math.radians(dth)
        lista.append((Vector((x, rho * math.cos(t), rho * math.sin(t))), "+"))      # carga no volume (isolante com ρ constante)
    return dict(enq=[corpo], sinais=lista, gauss=lambda p: gauss_cil(c, g, p))


def caso_folha(c, g):
    f = painel(c, 0.0, "fonte_fisica")
    for sx in (1, -1):                                                         # campo ⟂ à folha, dos dois lados, dentro da extensão lateral do pillbox
        for y, z in ((-0.55, -0.45), (0.55, 0.45)):
            seta(c, Vector((sx * 0.3, y, z)), Vector((sx, 0, 0)), 0.9)
    lista = [(Vector((0.07, y, z)), "+") for y, z in QUINCUNCIO]
    return dict(enq=[f], sinais=lista, gauss=lambda p: pillbox(c, -p, p, 1.0))


def caso_placa(c, g):
    a = 0.7
    corpo = caixa("Placa", -a, a, 2.5, 1.7)
    cm.material_vidro(corpo)
    contorno_caixa(c, -a, a, 2.5, 1.7)
    for sx in (1, -1):
        for y, z in ((-0.6, -0.45), (0.6, 0.45)):
            seta(c, Vector((sx * (a + 0.12), y, z)), Vector((sx, 0, 0)), 0.8)
    pts = [(-0.4, -1.6, 0.8), (0.0, -1.6, -0.8), (0.4, -0.8, 0.0), (-0.4, 0.0, 0.9), (0.0, 0.0, -0.9), (0.4, 0.8, 0.9), (-0.4, 1.6, -0.5), (0.0, 1.6, 0.8), (0.4, 0.0, -0.1)]
    lista = [(Vector(q), "+") for q in pts]                                    # cargas no volume da placa
    return dict(enq=[corpo], sinais=lista, gauss=lambda p: pillbox(c, -p, p, 1.1))


def caso_duas(c, g):
    x1, x2 = -1.1, 1.1
    f1, f2 = painel(c, x1, "fonte_fisica"), painel(c, x2, "apoio_magenta")
    for y, z in ((-0.9, -0.7), (-0.9, 0.7), (0.9, -0.7), (0.9, 0.7)):          # E uniforme entre as folhas, do + para o −
        seta(c, Vector((x1 + 0.3, y, z)), Vector((1, 0, 0)), 1.5)
    lista = [(Vector((x1 + 0.07, y, z)), "+") for y, z in QUINCUNCIO] + [(Vector((x2 + 0.07, y + 0.0, z)), "-") for y, z in [(-1.35, -0.45), (0.45, -0.45), (-0.45, 0.45), (1.35, 0.45), (-1.8, 0.9), (0.0, 0.9), (1.8, -0.9), (0.9, -0.9)]]
    xl = -1.9
    return dict(enq=[f1, f2], sinais=lista, gauss=lambda p: pillbox(c, xl, max(p, xl + 0.18), 1.1))


def caso_face(c, g):
    bloco = caixa("Condutor", -1.7, 0.0, 1.9, 1.35)
    bloco.data.materials.append(c.metal("MetalBloco"))
    contorno_caixa(c, -1.7, 0.0, 1.9, 1.35)
    for y, z in ((-0.45, -0.35), (-0.45, 0.35), (0.45, -0.35), (0.45, 0.35)):  # campo só do lado de fora (dentro do metal, E = 0)
        seta(c, Vector((0.25, y, z)), Vector((1, 0, 0)), 0.9)
    lista = [(Vector((0.08, y, z)), "+") for y, z in ((0.0, 0.0), (-1.4, -0.9), (-1.4, 0.0), (-1.4, 0.9), (1.4, -0.9), (1.4, 0.0), (1.4, 0.9), (0.0, 1.0), (0.0, -1.0))]
    return dict(enq=[bloco], sinais=lista, gauss=lambda p: pillbox(c, -0.75, p, 0.8))


def pontos_esfera(g, rmax):
    return [s * rmax * d for d in (g.right, g.up) for s in (1, -1)]


def caso_casca_esf(c, g):
    R = 1.0
    cs = casca_esf_cone(c, g, R, 0.07, 55, c.metal("MetalCascaEsf"))
    seta_anel(c, g, 1.15, 0.42)
    lista = []
    for k in range(6):                                                         # + na superfície externa, numa coroa visível em volta da abertura
        d = math.cos(math.radians(72)) * g.v + math.sin(math.radians(72)) * g.dir_plano(math.radians(30) + 2 * math.pi * k / 6)
        lista.append(((R + 0.09) * d, "+"))
    return dict(enq=[cs], pts=lambda rmax: pontos_esfera(g, rmax), sinais=lista, gauss=lambda p: gauss_esf(c, g, p))


def caso_macico_esf(c, g):
    R = 1.0
    corpo = esfera_uv(R, "EsferaMacica")
    cm.material_vidro(corpo)
    seta_anel(c, g, 1.15, 0.42)
    lista = []
    for k in range(10):                                                        # cargas no volume (isolante com ρ constante), em duas conchas
        d = g.dir_plano(2 * math.pi * k / 10 + 0.3) * math.cos(0.5 * (k % 3)) + g.v * (0.45 * math.sin(2.1 * k))
        lista.append((d.normalized() * (0.4 if k % 2 else 0.75), "+"))
    return dict(enq=[corpo], pts=lambda rmax: pontos_esfera(g, rmax), sinais=lista, gauss=lambda p: gauss_esf(c, g, p))


def caso_cap_esf(c, g):
    a, b, T = 0.8, 1.6, 0.06
    m_nucleo = c.metal("MetalNucleoEsf", True)
    nucleo = esfera_uv(a, "NucleoEsf")
    nucleo.data.materials.append(m_nucleo)
    cs = casca_esf_cone(c, g, b, T, 55, c.metal("MetalCascaEsf2"))
    seta_anel(c, g, 0.92, 0.36)
    lista = []
    for k in range(6):
        az_ = 2 * math.pi * k / 6
        d = math.cos(math.radians(40)) * g.v + math.sin(math.radians(40)) * g.dir_plano(az_)          # + na superfície da esfera interna (lado da câmera)
        lista.append(((a + 0.07) * d, "+"))
        dn = -math.cos(math.radians(46)) * g.v + math.sin(math.radians(46)) * g.dir_plano(az_ + math.radians(30))   # − na face interna da casca (parede do fundo)
        lista.append(((b - T - 0.08) * dn, "-"))
    return dict(enq=[cs, nucleo], pts=lambda rmax: pontos_esfera(g, max(rmax, b)), sinais=lista, gauss=lambda p: gauss_esf(c, g, p),
                pre=lambda p: v2.escurecer(m_nucleo, 1.0, 0.55 + 0.45 * ss((p - (a - 0.05)) / 0.14)))


BUILD = {"linha": caso_linha, "casca_cil": caso_casca_cil, "macico_cil": caso_macico_cil, "folha": caso_folha, "placa": caso_placa, "duas": caso_duas,
         "face": caso_face, "casca_esf": caso_casca_esf, "macico_esf": caso_macico_esf, "cap_esf": caso_cap_esf}


def renderizar(cid, args):
    spec = CASOS[cid]
    T = Traj(spec["wps"])
    pmax = max(p for p, _ in spec["wps"])
    pasta = (PASTA / "_estados" / cid) if args.estados else (PASTA / cid / "1120x784")
    pasta.mkdir(parents=True, exist_ok=True)
    co.limpar_cena()
    c, g = Ctx(), Geo(spec["az"], spec["el"])
    preparar(c)
    d = BUILD[cid](c, g)
    co.mundo()
    co.luzes()
    tmp = d["gauss"](pmax)                                                     # enquadramento pelo MAIOR p da gaussiana
    if "pts" in d:
        pontos = d["pts"](pmax)                                                # esferas: círculo exato (não a caixa envolvente)
    else:
        pontos = co.cantos([o for o in d["enq"] if o.type in ("MESH", "CURVE")] + [o for o in tmp if o.type == "MESH"])
    RLp.remover(tmp)
    cam = v2.camera_ortografica(pontos, spec["az"], spec["el"], spec["margem"], *RES)
    sinais(c, cam, d["sinais"])
    sc = bpy.context.scene
    sc.render.film_transparent = True
    sc.render.image_settings.color_mode = "RGBA"
    co.render(pasta / "_aq.png", *RES, args.amostras)
    (pasta / "_aq.png").unlink()
    todos = T.quadros_unicos()
    if args.estados:
        todos = [q for q in todos if q[0] in ("intro", "h0", "h1", "h2")]
    t0 = time.perf_counter()
    for chave, p in todos:
        if "pre" in d and p is not None:
            d["pre"](p)
        objs = [] if p is None else d["gauss"](p)
        sc.render.filepath = str(pasta / f"q_{chave}.png")
        bpy.ops.render.render(write_still=True)
        RLp.remover(objs)
    print(f"TODOS {cid} quadros={len(todos)} total={time.perf_counter() - t0:.1f}s medio={(time.perf_counter() - t0) / len(todos):.2f}s")


def main():
    resto = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    ap = argparse.ArgumentParser()
    ap.add_argument("--caso", default="todos")
    ap.add_argument("--estados", action="store_true")
    ap.add_argument("--amostras", type=int, default=64)
    a = ap.parse_args(resto)
    for cid in (list(CASOS) if a.caso == "todos" else a.caso.split(",")):
        renderizar(cid, a)


if __name__ == "__main__":
    main()

"""Preview padronizado dos casos de Gauss no padrão do coaxial v2 (sandbox; não altera o arsenal nem o yt_0002).

Para cada caso: sólido(s) do arsenal (ou um bloco novo, quando não existe), cargas só nas superfícies/volume corretos (+ azul, − magenta),
câmera ortográfica fixa e uma superfície gaussiana "fantasma" cujo parâmetro `p` varre o caso. A cena Manim usa o mesmo `p`.

Rodar, a partir da raiz do repositório:
    blender.exe -b -P experimentos/blender/preview_gauss_padronizado/render_casos.py -- --caso todos
Opções: --caso <id|todos>  --estados (3 quadros de validação em <saida>/_estados)  --frames N  --res LxA  --amostras N
"""

import argparse
import json
import math
import sys
import time
from pathlib import Path

import bmesh
import bpy
from mathutils import Vector

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parents[2]
sys.path.insert(0, str(AQUI))
sys.path.insert(0, str(AQUI.parent))
sys.path.insert(0, str(AQUI.parent / "teste_gauss_coaxial"))
import capacitores as cap  # noqa: E402
import casca_oca as co  # noqa: E402
import cilindro_macico as cm  # noqa: E402
import esferas as es  # noqa: E402
import gaussiana as ga  # noqa: E402
import placa as pl  # noqa: E402
import render_sequencia_v2 as v2  # noqa: E402
import vetores3d as v3  # noqa: E402
from casos import CASOS, PASTA_SEQ, RES  # noqa: E402

L = v2.L                                  # comprimento dos cilindros (eixo X)
MARGEM = 0.045


class Ctx:
    pass


# ── utilidades ──────────────────────────────────────────────────────────────
def remover(objs):
    """Remove objetos e dados próprios (a malha da seta é compartilhada: fica)."""
    for o in objs:
        dados = o.data
        bpy.data.objects.remove(o, do_unlink=True)
        if dados is not None and dados.users == 0 and not dados.use_fake_user:
            (bpy.data.meshes if isinstance(dados, bpy.types.Mesh) else bpy.data.curves).remove(dados)


def materiais(c):
    c.m_pos = v2.material_carga("CargaPos", "fonte_contorno", 1.7)      # carga positiva: azul claro
    c.m_neg = v2.material_carga("CargaNeg", "apoio_magenta", 1.9)       # carga negativa: magenta (cor de apoio da paleta)
    c.m_env = v2.material_carga("CargaEnv", "gaussiana", 2.3)           # carga envolvida pela gaussiana: violeta claro
    c.m_borda = v3.material_cor("Contorno", "fonte_contorno", 1.5)
    c.m_campo = v3.material_cor("CampoE", "campo_eletrico", 2.2)
    c.m_traco = ga.material_traco()
    c.m_fio = v3.material_cor("Fio", "fonte_fisica", 1.4)
    c.e_pos, c.e_neg = v2.esfera_base("EsferaPos"), v2.esfera_base("EsferaNeg")
    c.e_pos.materials.append(c.m_pos)
    c.e_neg.materials.append(c.m_neg)


def cil_x(raio, comprimento, nome):
    bpy.ops.mesh.primitive_cylinder_add(vertices=48, radius=raio, depth=comprimento, end_fill_type="NGON")
    o = bpy.context.active_object
    o.name = nome
    o.rotation_euler = (0, math.radians(90), 0)
    bpy.ops.object.transform_apply(rotation=True)
    return o


def caixa(nome, x0, x1, hy, hz):
    bpy.ops.mesh.primitive_cube_add(size=1, location=((x0 + x1) / 2, 0, 0))
    o = bpy.context.active_object
    o.name = nome
    o.scale = (x1 - x0, 2 * hy, 2 * hz)
    bpy.ops.object.transform_apply(scale=True)
    return o


def contorno_caixa(c, x0, x1, hy, hz, espessura=0.012):
    pts = [(x, sy * hy, sz * hz) for x in (x0, x1) for sy in (-1, 1) for sz in (-1, 1)]
    idx = {p: i for i, p in enumerate(pts)}
    ar = [([a, b], False) for a in pts for b in pts if idx[a] < idx[b] and sum(1 for i in range(3) if a[i] != b[i]) == 1]
    return v3.curva("ContornoCaixa", ar, c.m_borda, espessura)


def arestas_casca(c, R, a0, a1):
    def arco(raio, x, n=64):
        return [(x, raio * math.cos(a0 + (a1 - a0) * k / n), raio * math.sin(a0 + (a1 - a0) * k / n)) for k in range(n + 1)]
    pl_ = []
    for x in (-L / 2, L / 2):
        pl_ += [(arco(R, x), False), (arco(R - v2.T, x), False)]
    for ang in (a0, a1):
        for raio in (R, R - v2.T):
            pl_.append(([(-L / 2, raio * math.cos(ang), raio * math.sin(ang)), (L / 2, raio * math.cos(ang), raio * math.sin(ang))], False))
    return v3.curva("ContornoCasca", pl_, c.m_borda, 0.012)


def plano_de_cargas(x, ys, zs, escalonado=True):
    return [(x, y, z + (0.5 * (zs[1] - zs[0]) if escalonado and i % 2 else 0.0)) for i, y in enumerate(ys) for z in zs]


def linspace(a, b, n):
    return [a + (b - a) * k / (n - 1) for k in range(n)]


def seta_radial(c, origem, direcao, comp):
    """Seta de campo (ciano) a partir de `origem` na `direcao`; comprimento `comp`."""
    o = v3.seta(origem, direcao, c.m_campo, comprimento=comp)
    if o is not None:
        o.scale = (0.75, 0.75, comp)
    return o


def setas_laterais_cil(c, r, comp, pos=((-1.0, 122.0), (0.3, 152.0), (1.2, 182.0))):
    out = []
    for x, g in pos:
        t = math.radians(g)
        d = (0.0, math.cos(t), math.sin(t))
        out.append(seta_radial(c, (x, r * d[1], r * d[2]), d, comp))
    return [o for o in out if o is not None]


DIRS_ESF = [Vector(v).normalized() for v in ((0.0, 0.0, 1.0), (0.0, -1.0, 0.0), (-0.25, -0.7, 0.7))]    # ~perpendiculares ao olhar da câmera


def setas_esf(c, r, comp):
    return [o for o in (seta_radial(c, d * r, d, comp) for d in DIRS_ESF) if o is not None]


def fase_cunha(az, el):
    return math.atan2(math.sin(math.radians(el)), math.cos(math.radians(el)) * math.sin(math.radians(az)))


def pillbox(c, xl, xr, lado):
    """Pillbox (normal ao longo de X): tampas contínuas (contribuem), arestas laterais tracejadas, vidro violeta fantasma."""
    h = lado / 2
    quad = lambda x: [(x, -h, -h), (x, h, -h), (x, h, h), (x, -h, h)]  # noqa: E731
    tracos = [(quad(xl), True), (quad(xr), True)]
    for k in range(4):
        tracos += ga.linha(quad(xl)[k], quad(xr)[k], False)
    curvas = ga.criar_curva("PillTracos", tracos, c.m_traco, 0.013)
    corpo = caixa("PillFaces", xl, xr, h, h)
    ga.vidro_gaussiana(corpo)
    return [curvas, corpo]


BASE = {}                                   # nome do objeto de carga → material original (positivo ou negativo)


def marcar(objs, dentro, c):
    """Carga envolvida: as cargas dentro da gaussiana ficam violeta claro (material por objeto)."""
    for o in objs:
        o.material_slots[0].material = c.m_env if dentro(o.location) else BASE[o.name]


def preparar_cargas(objs, mat_base):
    for o in objs:
        o.material_slots[0].link = "OBJECT"
        o.material_slots[0].material = mat_base
        BASE[o.name] = mat_base


# ── casos: cada um devolve (objetos de enquadramento, atualizar(p) -> objetos temporários) ──
def caso_linha(c, az, el):
    fio = cil_x(0.03, L, "Fio")
    fio.data.materials.append(c.m_fio)
    v2.cargas(c.e_pos, [(x, 0.0, 0.0) for x in linspace(-L / 2 + 0.3, L / 2 - 0.3, 15)], 0.055)
    phi = fase_cunha(az, el)

    def atualizar(p):
        return v2.gaussiana(p, c.m_traco, phi) + setas_laterais_cil(c, p, 0.42 / p)
    return [fio], atualizar


def caso_casca_cil(c, az, el):
    R = 1.0
    phi = fase_cunha(az, el)
    a0, a1 = phi + math.radians(52), phi + 2 * math.pi - math.radians(52)
    antigo, v2.B = v2.B, R
    casca = v2.casca_aberta(a0, a1)
    v2.B = antigo
    casca.data.materials.append(v2.material_metal("MetalCasca2", "fonte_escura", "fonte_contorno", 0.16))
    arestas_casca(c, R, a0, a1)
    v2.cargas(c.e_pos, v2.reticulado(R + 0.014, a0 + 0.1, a1 - 0.1, 16, 9), 0.034)    # +λ na superfície externa da casca

    def atualizar(p):
        out = v2.gaussiana(p, c.m_traco, phi)
        if p > R + 0.05:
            out += setas_laterais_cil(c, p, 0.42 / p)
        return out
    return [casca], atualizar


def caso_macico_cil(c, az, el):
    R = 1.0
    corpo = cm.criar_corpo_macico(R, L)
    cm.material_vidro(corpo)
    cargas = cm.criar_cargas(cm.pontos_no_volume(95, R, L, 0.32), 0.036, material=c.m_pos)
    preparar_cargas(cargas, c.m_pos)
    phi = fase_cunha(az, el)

    def atualizar(p):
        marcar(cargas, lambda q: math.hypot(q.y, q.z) <= p and abs(q.x) <= v2.GL / 2, c)
        u = p / R
        comp = 0.55 * (u if u <= 1 else 1 / u)
        out = v2.gaussiana(p, c.m_traco, phi)
        return out + (setas_laterais_cil(c, p, comp) if comp > 0.05 else [])
    return [corpo], atualizar


def caso_coax(c, az, el):
    phi = fase_cunha(az, el)
    meia = math.radians(v2.CUNHA / 2)
    a0, a1 = phi + meia, phi + 2 * math.pi - meia
    m_nucleo = v2.material_metal("MetalNucleo", "fonte_escura", "fonte_contorno", 0.16, translucido=True)
    m_casca = v2.material_metal("MetalCasca", "fonte_escura", "fonte_contorno", 0.16)
    n = v2.nucleo()
    n.data.materials.append(m_nucleo)
    cs = v2.casca_aberta(a0, a1)
    cs.data.materials.append(m_casca)
    v2.arestas_luminosas(c.m_borda, a0, a1)
    v2.cargas(c.e_pos, v2.reticulado(v2.A + 0.012, 0, 2 * math.pi * (1 - 1 / 18), 18, 9), 0.034)       # +λ no núcleo
    v2.cargas(c.e_neg, v2.reticulado(v2.B - v2.T - 0.012, a0 + 0.12, a1 - 0.12, 14, 9), 0.034)          # −λ na face interna
    setas = v2.setas_do_vao(c.m_campo)

    def atualizar(p):
        w = v2.pesos(p)
        v2.escurecer(m_nucleo, w["nucleo"], w["opac"])
        v2.escurecer(m_casca, w["casca"])
        v2.escurecer(c.m_pos, w["nucleo"])
        v2.escurecer(c.m_neg, w["casca"])
        c.m_campo.node_tree.nodes["Principled BSDF"].inputs["Emission Strength"].default_value = 2.2 * w["campo"]
        for s in setas:
            s.hide_render = w["campo"] < 0.04
        return v2.gaussiana(p, c.m_traco, phi)
    return [cs, n], atualizar


def placa_fina(x):
    corpo, _, _ = pl.criar_placa_carregada(offset=(x, 0, 0), largura=6.0, altura=4.4, espessura=0.05, com_cargas=0)
    return corpo


YS, ZS = linspace(-2.4, 2.4, 9), linspace(-1.5, 1.5, 6)


def caso_folha(c, az, el):
    corpo = placa_fina(0.0)
    cargas = v2.cargas(c.e_pos, plano_de_cargas(0.0, YS, ZS), 0.045)
    preparar_cargas(cargas, c.e_pos.materials[0])
    h = 1.1

    def atualizar(p):
        marcar(cargas, lambda q: abs(q.y) <= h and abs(q.z) <= h, c)
        out = pillbox(c, -p, p, 2 * h)
        for sg in (-1, 1):
            for y, z in ((-0.5, -0.35), (0.5, 0.4), (0.0, 0.0)):
                out.append(seta_radial(c, (sg * p, y, z), (sg, 0, 0), 0.55))
        return out
    return [corpo], atualizar


def caso_placa(c, az, el):
    a = 0.7
    corpo = caixa("Placa", -a, a, 2.5, 1.7)
    cm.material_vidro(corpo)
    contorno_caixa(c, -a, a, 2.5, 1.7)
    pts = []
    for k, x in enumerate((-0.5 * a, 0.0, 0.5 * a)):
        pts += plano_de_cargas(x, linspace(-2.2, 2.2, 8), linspace(-1.35, 1.35, 5), escalonado=(k % 2 == 0))
    cargas = v2.cargas(c.e_pos, pts, 0.04)
    preparar_cargas(cargas, c.e_pos.materials[0])
    h = 1.1

    def atualizar(p):
        marcar(cargas, lambda q: abs(q.x) <= p and abs(q.y) <= h and abs(q.z) <= h, c)
        out = pillbox(c, -p, p, 2 * h)
        comp = 0.55 * min(p / a, 1.0)
        for sg in (-1, 1):
            for y, z in ((-0.5, -0.35), (0.5, 0.4), (0.0, 0.0)):
                out.append(seta_radial(c, (sg * p, y, z), (sg, 0, 0), comp))
        return out
    return [corpo], atualizar


def caso_duas(c, az, el):
    x1, x2, h = -1.1, 1.1, 1.1
    corpo1, corpo2 = placa_fina(x1), placa_fina(x2)
    pos = v2.cargas(c.e_pos, plano_de_cargas(x1 + 0.035, YS, ZS), 0.045)
    neg = v2.cargas(c.e_neg, plano_de_cargas(x2 - 0.035, YS, ZS), 0.045)
    preparar_cargas(pos, c.e_pos.materials[0])
    preparar_cargas(neg, c.e_neg.materials[0])
    for y, z in ((-0.9, -0.5), (-0.9, 0.5), (0.0, 0.0), (0.9, -0.5), (0.9, 0.5)):          # E uniforme no vão: de + para −
        seta_radial(c, (x1 + 0.25, y, z), (1, 0, 0), 1.6)
    xl = -1.9

    def atualizar(p):
        marcar(pos, lambda q: xl <= q.x <= p and abs(q.y) <= h and abs(q.z) <= h, c)
        marcar(neg, lambda q: xl <= q.x <= p and abs(q.y) <= h and abs(q.z) <= h, c)
        return pillbox(c, xl, max(p, xl + 0.18), 2 * h)
    return [corpo1, corpo2], atualizar


def caso_face(c, az, el):
    m = v2.material_metal("MetalBloco", "fonte_escura", "fonte_fisica", 0.05, translucido=True)
    v2.escurecer(m, 1.0, 0.6)
    bloco = caixa("Condutor", -1.7, 0.0, 1.9, 1.35)
    bloco.data.materials.append(m)
    contorno_caixa(c, -1.7, 0.0, 1.9, 1.35)
    cargas = v2.cargas(c.e_pos, plano_de_cargas(0.025, linspace(-1.6, 1.6, 7), linspace(-1.1, 1.1, 5)), 0.045)   # só na face
    preparar_cargas(cargas, c.e_pos.materials[0])
    h = 0.8

    def atualizar(p):
        marcar(cargas, lambda q: abs(q.y) <= h and abs(q.z) <= h, c)
        out = pillbox(c, -0.75, p, 2 * h)
        for y, z in ((-0.4, -0.3), (0.4, 0.35), (0.0, 0.0)):                      # só a tampa de fora tem campo
            out.append(seta_radial(c, (p, y, z), (1, 0, 0), 0.55))
        return out
    return [bloco], atualizar


def esfera_gaussiana(p):
    return ga.criar_gaussiana_esferica(p, 1, 1)


def fib_fora_do_corte(n, raio):
    return [q for q in cap.pontos_fibonacci(n, raio) if not (q[0] > 0 and q[1] < 0 and q[2] > 0)]


def caso_casca_esf(c, az, el):
    R = 1.0
    casca = es.criar_casca_esferica(R, 0.07, 96, 48, 1)
    co.material_casca(casca)
    v2.cargas(c.e_pos, fib_fora_do_corte(90, R + 0.016), 0.034)                # +Q na superfície externa

    def atualizar(p):
        out = esfera_gaussiana(p)
        if p > R + 0.05:
            out += setas_esf(c, p, 0.5 * (R / p) ** 2)
        return out
    return [casca], atualizar


def caso_macico_esf(c, az, el):
    R = 1.0
    corpo, cargas = es.criar_esfera_macica(raio=R, n_cargas=75, dist_min=0.3)
    preparar_cargas(cargas, c.m_pos)

    def atualizar(p):
        marcar(cargas, lambda q: q.length <= p, c)
        u = p / R
        comp = 0.6 * (u if u <= 1 else 1 / u ** 2)
        return esfera_gaussiana(p) + (setas_esf(c, p, comp) if comp > 0.05 else [])
    return [corpo], atualizar


def caso_cap_esf(c, az, el):
    a, b = 0.8, 1.6
    externa = cap.criar_capacitor_esferico(a, b, 0.06, n_cargas=70, corte=1)
    cargas = [o for o in bpy.data.objects if o.name.startswith("Carga") and o.type == "MESH"]
    interna = [o for o in cargas if o.location.length < (a + b) / 2]
    externas = [o for o in cargas if o.location.length >= (a + b) / 2]
    preparar_cargas(interna, c.m_pos)
    preparar_cargas(externas, c.m_neg)                                          # −Q na face interna da casca externa

    def atualizar(p):
        w = v2.ss((p - a) / 0.14) * (1 - v2.ss((p - (b - 0.3)) / 0.2))         # campo só no vão
        out = esfera_gaussiana(p)
        if w > 0.04 and p + 0.2 < b:
            out += setas_esf(c, p, 0.34 * (a / p) ** 2 * w + 0.01)
        return out
    return [externa], atualizar


BUILD = {"linha": caso_linha, "casca_cil": caso_casca_cil, "macico_cil": caso_macico_cil, "coax": caso_coax, "folha": caso_folha,
         "placa": caso_placa, "duas": caso_duas, "face": caso_face, "casca_esf": caso_casca_esf, "macico_esf": caso_macico_esf,
         "cap_esf": caso_cap_esf}


def renderizar_caso(cid, args, largura, altura):
    spec = CASOS[cid]
    n = args.frames or spec["frames"]
    pasta = RAIZ / PASTA_SEQ / cid / args.res
    pasta.mkdir(parents=True, exist_ok=True)

    co.limpar_cena()
    c = Ctx()
    materiais(c)
    antes = set(bpy.data.objects)
    enquadrar, atualizar = BUILD[cid](c, spec["az"], spec["el"])
    co.mundo()
    co.luzes()
    tmp = atualizar(spec["p1"])
    pontos = co.cantos([o for o in enquadrar if o.type in ("MESH", "CURVE")] + [o for o in tmp if o.type == "MESH"])
    remover(tmp)
    cam = v2.camera_ortografica(pontos, spec["az"], spec["el"], MARGEM, largura, altura)
    sc = bpy.context.scene
    sc.render.film_transparent = True
    sc.render.image_settings.color_mode = "RGBA"
    co.render(pasta / "_aq.png", largura, altura, args.amostras)
    (pasta / "_aq.png").unlink()
    t0 = time.perf_counter()
    if args.estados:
        est = RAIZ / PASTA_SEQ / "_estados"
        est.mkdir(parents=True, exist_ok=True)
        for k, f in enumerate((0.1, 0.5, 0.93), start=1):
            p = spec["p0"] + (spec["p1"] - spec["p0"]) * f
            tmp = atualizar(p)
            sc.render.filepath = str(est / f"{cid}_{k}.png")
            bpy.ops.render.render(write_still=True)
            remover(tmp)
        print(f"ESTADOS {cid} {time.perf_counter() - t0:.1f}s")
        return
    for i in range(n):
        tmp = atualizar(spec["p0"] + (spec["p1"] - spec["p0"]) * i / (n - 1))
        sc.render.filepath = str(pasta / f"frame_{i + 1:04d}.png")
        bpy.ops.render.render(write_still=True)
        remover(tmp)
    (pasta / "meta.json").write_text(json.dumps({"frames": n, "p0": spec["p0"], "p1": spec["p1"], "res": args.res}, indent=1), encoding="utf-8")
    print(f"CASO {cid} frames={n} total={time.perf_counter() - t0:.1f}s medio={(time.perf_counter() - t0) / n:.2f}s")


def main():
    resto = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    ap = argparse.ArgumentParser(prog="render_casos.py")
    ap.add_argument("--caso", default="todos")
    ap.add_argument("--estados", action="store_true")
    ap.add_argument("--frames", type=int, default=0)
    ap.add_argument("--res", default=RES)
    ap.add_argument("--amostras", type=int, default=64)
    a = ap.parse_args(resto)
    largura, altura = (int(x) for x in a.res.lower().split("x"))
    for cid in (list(CASOS) if a.caso == "todos" else a.caso.split(",")):
        renderizar_caso(cid, a, largura, altura)


if __name__ == "__main__":
    main()

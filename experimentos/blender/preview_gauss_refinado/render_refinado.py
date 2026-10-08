"""Preview refinado (sandbox): coaxial, duas folhas e esfera maciça no padrão híbrido (adaptação LOCAL; não altera o arsenal).

Blender: sólido, cargas, gaussiana 3D e setas de campo (com oclusão). Manim (cena_refinado.py): fórmulas, regiões, gráfico e esquemas 2D.
Regras desta rodada: sinal da carga sempre legível (+ azul, − magenta; a carga envolvida ganha HALO violeta, nunca muda de cor); campo
existente (discreto) ≠ campo avaliado (destacado); mesma família de setas, módulo coerente com E; gaussiana fantasma.

Rodar, a partir da raiz do repositório:
    blender.exe -b -P experimentos/blender/preview_gauss_refinado/render_refinado.py -- --caso todos [--estados]
"""

import argparse
import json
import math
import sys
import time
from pathlib import Path

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
from casos_ref import CASOS, PASTA_SEQ, RES  # noqa: E402

GL = v2.GL                                  # comprimento do cilindro gaussiano
ESP_SETA = 1.0                              # espessura comum de TODAS as setas de campo
BASE = {}                                   # carga → material de sinal original


class Ctx:
    pass


# ── materiais e peças comuns ────────────────────────────────────────────────
def material_translucido(nome, cor, emissao, alfa):
    mat = bpy.data.materials.new(nome)
    mat.use_nodes = True
    b = mat.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = co.hex_linear(co.E.cor(cor))
    b.inputs["Emission Color"].default_value = co.hex_linear(co.E.cor(cor))
    b.inputs["Emission Strength"].default_value = emissao
    b.inputs["Alpha"].default_value = alfa
    b.inputs["Roughness"].default_value = 1.0
    b.inputs["Metallic"].default_value = 0.0
    for chave in ("Specular IOR Level", "Specular"):
        if chave in b.inputs:
            b.inputs[chave].default_value = 0.0
    try:
        mat.surface_render_method = "DITHERED"
    except (AttributeError, TypeError):
        pass
    return mat


def materiais(c):
    c.m_pos = v2.material_carga("CargaPos", "fonte_contorno", 1.7)           # + azul claro
    c.m_neg = v2.material_carga("CargaNeg", "apoio_magenta", 1.9)            # − magenta
    c.m_borda = v3.material_cor("Contorno", "fonte_contorno", 0.9)
    c.m_campo = v3.material_cor("CampoE", "campo_eletrico", 1.0)             # campo existente: discreto; sobe quando avaliado
    c.m_campo_av = v3.material_cor("CampoAvaliado", "campo_eletrico", 2.8)   # campo na região avaliada pela gaussiana
    c.m_traco = ga.material_traco()                                          # contorno frontal (nítido)
    c.m_traco2 = ga.material_traco()                                         # partes traseiras/guias (discretas)
    c.m_traco2.node_tree.nodes["Principled BSDF"].inputs["Emission Strength"].default_value = 0.8
    c.m_fant = material_translucido("GaussFantasma", "gaussiana", 0.25, 0.045)
    c.m_halo = material_translucido("HaloQenv", "gaussiana", 1.4, 0.2)
    c.e_pos, c.e_neg = v2.esfera_base("EsferaPos"), v2.esfera_base("EsferaNeg")
    c.e_pos.materials.append(c.m_pos)
    c.e_neg.materials.append(c.m_neg)
    c.e_halo = v2.esfera_base("EsferaHalo")
    c.e_halo.materials.append(c.m_halo)


def remover(objs):
    for o in objs:
        dados = o.data
        bpy.data.objects.remove(o, do_unlink=True)
        if dados is not None and dados.users == 0 and not dados.use_fake_user:
            (bpy.data.meshes if isinstance(dados, bpy.types.Mesh) else bpy.data.curves).remove(dados)


def fase_cunha(az, el):
    return math.atan2(math.sin(math.radians(el)), math.cos(math.radians(el)) * math.sin(math.radians(az)))


def dir_camera(az, el):
    a, e = math.radians(az), math.radians(el)
    return Vector((math.cos(e) * math.cos(a), math.cos(e) * math.sin(a), math.sin(e)))


def seta(origem, direcao, comp, mat):
    """Seta de campo: mesma malha, mesma espessura em todos os casos; o comprimento representa o módulo."""
    o = v3.seta(origem, direcao, mat, comprimento=comp)
    if o is not None:
        o.scale = (ESP_SETA, ESP_SETA, comp)
    return o


def preparar_cargas(objs, mat_base):
    for o in objs:
        o.material_slots[0].link = "OBJECT"
        o.material_slots[0].material = mat_base
        BASE[o.name] = (mat_base, o.scale[0])


def criar_halos(c, cargas, raio_halo):
    """Um halo violeta (esfera translúcida) por carga; a cor de sinal da carga NÃO muda — o halo só indica que ela está em Q_env."""
    halos = {}
    for o in cargas:
        h = bpy.data.objects.new("Halo", c.e_halo)
        h.location = o.location
        h.scale = (raio_halo, raio_halo, raio_halo)
        h.hide_render = True
        bpy.context.collection.objects.link(h)
        halos[o.name] = h
    return halos


def marcar_envolvidas(cargas, halos, dentro):
    for o in cargas:
        ok = dentro(o.location)
        halos[o.name].hide_render = not ok
        e = BASE[o.name][1] * (1.25 if ok else 1.0)
        o.scale = (e, e, e)


def plano_de_cargas(x, ys, zs):
    return [(x, y, z + (0.5 * (zs[1] - zs[0]) if i % 2 else 0.0)) for i, y in enumerate(ys) for z in zs]


def linspace(a, b, n):
    return [a + (b - a) * k / (n - 1) for k in range(n)]


# ── gaussianas "fantasma" ───────────────────────────────────────────────────
def gauss_cilindro(c, r, phi):
    """Preenchimento quase invisível; aro frontal (+X, mais perto da câmera) contínuo; aro traseiro e guias tracejados."""
    Y, Z = (0, 1, 0), (0, 0, 1)
    corpo = cm.criar_corpo_macico(r, GL)
    corpo.data.materials.append(c.m_fant)
    frente = ga.circulo((GL / 2, 0, 0), Y, Z, r, True)
    tras = ga.circulo((-GL / 2, 0, 0), Y, Z, r, False)
    for ang in (phi - 0.55, phi + 0.55):
        tras += ga.linha((-GL / 2, r * math.cos(ang), r * math.sin(ang)), (GL / 2, r * math.cos(ang), r * math.sin(ang)), False)
    return [ga.criar_curva("GFrente", frente, c.m_traco, 0.016), ga.criar_curva("GTras", tras, c.m_traco2, 0.009), corpo]


def gauss_esfera(c, r, camdir):
    """Três grandes círculos: meia-volta voltada à câmera contínua, meia-volta de trás tracejada; preenchimento quase invisível."""
    bpy.ops.mesh.primitive_uv_sphere_add(radius=r, segments=48, ring_count=24)
    corpo = bpy.context.active_object
    bpy.ops.object.shade_smooth()
    corpo.data.materials.append(c.m_fant)
    frente, tras = [], []
    for u, v in (((1, 0, 0), (0, 1, 0)), ((1, 0, 0), (0, 0, 1)), ((0, 1, 0), (0, 0, 1))):
        n, pts = 120, []
        for k in range(n + 1):
            t = 2 * math.pi * k / n
            pts.append(r * (math.cos(t) * Vector(u) + math.sin(t) * Vector(v)))
        run, lado = [pts[0]], pts[0].dot(camdir) > 0
        for p in pts[1:]:
            s = p.dot(camdir) > 0
            if s == lado:
                run.append(p)
                continue
            (frente.append((run, False)) if lado else tras.extend(v3.tracejado(run, False, 0.22, 0.55)))
            run, lado = [run[-1], p], s
        (frente.append((run, False)) if lado else tras.extend(v3.tracejado(run, False, 0.22, 0.55)))
    return [ga.criar_curva("GFrente", frente, c.m_traco, 0.016), ga.criar_curva("GTras", tras, c.m_traco2, 0.01), corpo]


def pillbox(c, xl, xr, h):
    """Tampa da direita (mais perto da câmera) contínua; a da esquerda e as arestas laterais tracejadas; preenchimento quase invisível."""
    quad = lambda x: [(x, -h, -h), (x, h, -h), (x, h, h), (x, -h, h)]  # noqa: E731
    frente = [(quad(xr), True)]
    tras = v3.tracejado(quad(xl), True, 0.26, 0.6)
    for k in range(4):
        tras += ga.linha(quad(xl)[k], quad(xr)[k], False)
    bpy.ops.mesh.primitive_cube_add(size=1, location=((xl + xr) / 2, 0, 0))
    corpo = bpy.context.active_object
    corpo.scale = (max(xr - xl, 0.02), 2 * h, 2 * h)
    bpy.ops.object.transform_apply(scale=True)
    corpo.data.materials.append(c.m_fant)
    return [ga.criar_curva("GFrente", frente, c.m_traco, 0.016), ga.criar_curva("GTras", tras, c.m_traco2, 0.009), corpo]


# ── caso 1: cabo coaxial ────────────────────────────────────────────────────
def caso_coax(c, az, el):
    phi = fase_cunha(az, el)
    meia = math.radians(v2.CUNHA / 2)
    a0, a1 = phi + meia, phi + 2 * math.pi - meia
    m_nucleo = v2.material_metal("MetalNucleo", "fonte_escura", "fonte_contorno", 0.10, translucido=True)
    m_casca = v2.material_metal("MetalCasca", "fonte_escura", "fonte_contorno", 0.10)
    n = v2.nucleo()
    n.data.materials.append(m_nucleo)
    cs = v2.casca_aberta(a0, a1)
    cs.data.materials.append(m_casca)
    v2.arestas_luminosas(c.m_borda, a0, a1)
    pos = v2.cargas(c.e_pos, v2.reticulado(v2.A + 0.012, 0, 2 * math.pi * (1 - 1 / 18), 18, 9), 0.034)       # +λ só na superfície do núcleo
    neg = v2.cargas(c.e_neg, v2.reticulado(v2.B - v2.T - 0.012, a0 + 0.12, a1 - 0.12, 14, 9), 0.034)          # −λ só na face interna da casca
    preparar_cargas(pos, c.e_pos.materials[0])
    preparar_cargas(neg, c.e_neg.materials[0])
    halos = {**criar_halos(c, pos, 0.062), **criar_halos(c, neg, 0.062)}
    # campo existente no vão: 3 fatias em x × 6 ângulos uniformes (radial para fora; |E| ∝ 1/r; fatias alternam dois raios)
    gap = []
    for k, (x, r0, desloc) in enumerate(((-1.4, 0.68, 0.0), (0.0, 1.05, 30.0), (1.4, 0.68, 0.0))):
        for j in range(6):
            t = math.radians(desloc + 60 * j)
            d = (0.0, math.cos(t), math.sin(t))
            g = seta((x, r0 * d[1], r0 * d[2]), d, 0.30 / r0, c.m_campo)
            gap.append(g)

    def atualizar(p):
        w = v2.pesos(p)
        v2.escurecer(m_nucleo, w["nucleo"], 0.55 + 0.45 * v2.ss((p - (v2.A - 0.05)) / 0.14))
        v2.escurecer(m_casca, w["casca"])
        v2.escurecer(c.m_pos, w["nucleo"])
        v2.escurecer(c.m_neg, w["casca"])
        # campo existente sempre visível (discreto); realçado só quando a região avaliada é o vão
        c.m_campo.node_tree.nodes["Principled BSDF"].inputs["Emission Strength"].default_value = 0.9 + 1.9 * w["campo"]
        marcar_envolvidas(pos + neg, halos, lambda q: abs(q.x) <= GL / 2 and math.hypot(q.y, q.z) < p)
        return gauss_cilindro(c, p, phi)
    return [cs, n], atualizar


# ── caso 2: duas folhas ─────────────────────────────────────────────────────
def caso_duas(c, az, el):
    x1, x2, h, LW, AH = -1.1, 1.1, 1.1, 6.8, 4.8
    folhas = []
    for x, cor in ((x1, "fonte_fisica"), (x2, "apoio_magenta")):
        f = pl.criar_placa(LW, AH, 0.04)
        f.location = (x, 0, 0)
        pl.material_placa(f, LW, AH, 0, cor=cor, base=0.30, ganho=0.5, fade_inicio=0.74)
        folhas.append(f)
        borda = v3.material_cor("Borda" + cor, "fonte_contorno" if cor == "fonte_fisica" else "apoio_magenta", 0.9)
        hy, hz = 0.80 * LW / 2, 0.80 * AH / 2
        v3.curva("ContornoFolha", [([(x, -hy, -hz), (x, hy, -hz), (x, hy, hz), (x, -hy, hz)], True)], borda, 0.011)
    ys, zs = linspace(-2.7, 2.7, 10), linspace(-1.75, 1.75, 6)
    pos = v2.cargas(c.e_pos, plano_de_cargas(x1 + 0.03, ys, zs), 0.04)
    neg = v2.cargas(c.e_neg, plano_de_cargas(x2 - 0.03, ys, zs), 0.04)
    preparar_cargas(pos, c.e_pos.materials[0])
    preparar_cargas(neg, c.e_neg.materials[0])
    halos = {**criar_halos(c, pos, 0.072), **criar_halos(c, neg, 0.072)}
    for y in linspace(-1.5, 1.5, 4):                                  # E uniforme no vão: grade regular, do + para o −
        for z in (-0.85, 0.85):
            seta((x1 + 0.3, y, z), (1, 0, 0), 1.5, c.m_campo)
    xl = -1.9

    def atualizar(p):
        entre = x1 <= p <= x2
        c.m_campo.node_tree.nodes["Principled BSDF"].inputs["Emission Strength"].default_value = 2.6 if entre else 0.9
        marcar_envolvidas(pos + neg, halos, lambda q: xl <= q.x <= p and abs(q.y) <= h and abs(q.z) <= h)
        return pillbox(c, xl, max(p, xl + 0.18), h)
    return folhas, atualizar


# ── caso 3: esfera maciça isolante ──────────────────────────────────────────
def caso_esfera(c, az, el):
    R = 1.0
    corpo, cargas = es.criar_esfera_macica(raio=R, n_cargas=115, dist_min=0.25)
    preparar_cargas(cargas, c.e_pos.materials[0])
    halos = criar_halos(c, cargas, 0.066)
    dirs = [Vector(q).normalized() for q in cap.pontos_fibonacci(14, 1.0)]       # direções radiais uniformes na esfera inteira
    cam = dir_camera(az, el)

    def atualizar(p):
        marcar_envolvidas(cargas, halos, lambda q: q.length <= p)
        u = p / R
        comp = 0.8 * (u if u <= 1 else 1 / u ** 2)                                # |E|/E_R: mesmo raio, mesmo módulo
        out = gauss_esfera(c, p, cam)
        if comp > 0.07:
            out += [s for s in (seta(d * p, d, comp, c.m_campo_av) for d in dirs) if s is not None]
        return out
    return [corpo], atualizar


BUILD = {"coax": caso_coax, "duas": caso_duas, "esfera": caso_esfera}


def renderizar_caso(cid, args, largura, altura):
    spec = CASOS[cid]
    n = args.frames or spec["frames"]
    pasta = RAIZ / PASTA_SEQ / cid / args.res
    pasta.mkdir(parents=True, exist_ok=True)
    co.limpar_cena()
    c = Ctx()
    materiais(c)
    enquadrar, atualizar = BUILD[cid](c, spec["az"], spec["el"])
    co.mundo()
    co.luzes()
    tmp = atualizar(spec["p1"])
    pontos = co.cantos([o for o in enquadrar if o.type in ("MESH", "CURVE")] + [o for o in tmp if o.type == "MESH"])
    remover(tmp)
    v2.camera_ortografica(pontos, spec["az"], spec["el"], spec["margem"], largura, altura)
    sc = bpy.context.scene
    sc.render.film_transparent = True
    sc.render.image_settings.color_mode = "RGBA"
    co.render(pasta / "_aq.png", largura, altura, args.amostras)
    (pasta / "_aq.png").unlink()
    t0 = time.perf_counter()
    if args.estados:
        est = RAIZ / PASTA_SEQ / "_estados"
        est.mkdir(parents=True, exist_ok=True)
        for k, f in enumerate((0.08, 0.5, 0.94), start=1):
            tmp = atualizar(spec["p0"] + (spec["p1"] - spec["p0"]) * f)
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
    ap = argparse.ArgumentParser(prog="render_refinado.py")
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

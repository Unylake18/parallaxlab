"""Coaxial 3D v2 (sandbox): geometria legível, cargas só nas superfícies, câmera ortográfica 3/4, gaussiana "fantasma" que cresce.

Só importa helpers existentes do Blender/arsenal (não altera nenhum). Cena isolada; não faz parte do yt_0002.

Rodar, a partir da raiz do repositório:
    blender.exe -b -P experimentos/blender/teste_gauss_coaxial/render_sequencia_v2.py -- [opções]

Opções:
    --estados          só 3 quadros-estado (r<a, a<r<b, r>b) em <saida>/estado_*.png, para validar antes da sequência
    --frames N         quadros da sequência (padrão 90); quadro i tem raio r = r0 + (r1 - r0) * i / (N - 1)
    --res LxA          resolução (padrão 1120x784); --amostras N (padrão 64); --r0/--r1 (padrão 0.25/1.95)
    --saida pasta      padrão renders/teste_gauss_coaxial_v2/<LxA>/ (`renders/` é ignorado pelo Git)
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
sys.path.insert(0, str(AQUI.parent))
import casca_oca as co  # noqa: E402
import cilindro_macico as cm  # noqa: E402
import gaussiana as ga  # noqa: E402
import vetores3d as v3  # noqa: E402

A, B, T, L = 0.5, 1.5, 0.07, 5.0            # núcleo, raio externo da casca, espessura da casca, comprimento
GL = 3.0                                    # comprimento do cilindro gaussiano
AZ, EL = -32.0, 18.0                        # ponto de vista (câmera ortográfica, fixa)
CUNHA = 104.0                               # abertura do corte (graus): a casca mantém ~71% da circunferência
MARGEM = 0.045
ARCOS = 96                                  # segmentos por circunferência completa

ss = lambda x: 0.0 if x <= 0 else 1.0 if x >= 1 else x * x * (3 - 2 * x)   # noqa: E731


def hexc(chave):
    return co.hex_linear(co.E.cor(chave))


# ── malhas ──────────────────────────────────────────────────────────────────
def objeto_de_malha(nome, bm):
    me = bpy.data.meshes.new(nome)
    bm.to_mesh(me)
    bm.free()
    o = bpy.data.objects.new(nome, me)
    bpy.context.collection.objects.link(o)
    return o


def suavizar(o, graus=30):
    bpy.context.view_layer.objects.active = o
    o.select_set(True)
    bpy.ops.object.shade_smooth_by_angle(angle=math.radians(graus))
    o.select_set(False)


def casca_aberta(a0, a1):
    """Tubo oco (eixo X) com corte angular: sólido fechado (superfície externa, interna, aros das pontas e as duas faces do corte)."""
    bm = bmesh.new()
    n = max(8, int(ARCOS * (a1 - a0) / (2 * math.pi)))
    xs = (-L / 2, L / 2)
    vo, vi = [], []
    for x in xs:
        vo.append([bm.verts.new((x, B * math.cos(a0 + (a1 - a0) * k / n), B * math.sin(a0 + (a1 - a0) * k / n))) for k in range(n + 1)])
        vi.append([bm.verts.new((x, (B - T) * math.cos(a0 + (a1 - a0) * k / n), (B - T) * math.sin(a0 + (a1 - a0) * k / n))) for k in range(n + 1)])
    for k in range(n):
        bm.faces.new((vo[0][k], vo[0][k + 1], vo[1][k + 1], vo[1][k]))           # externa
        bm.faces.new((vi[0][k], vi[0][k + 1], vi[1][k + 1], vi[1][k]))           # interna
        for j in (0, 1):                                                         # aros das pontas (mostram a espessura)
            bm.faces.new((vo[j][k], vo[j][k + 1], vi[j][k + 1], vi[j][k]))
    for k in (0, n):                                                             # faces do corte
        bm.faces.new((vo[0][k], vo[1][k], vi[1][k], vi[0][k]))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    o = objeto_de_malha("CascaExterna", bm)
    suavizar(o)
    return o


def nucleo():
    bpy.ops.mesh.primitive_cylinder_add(vertices=ARCOS, radius=A, depth=L, end_fill_type="NGON")
    o = bpy.context.active_object
    o.name = "Nucleo"
    o.rotation_euler = (0, math.radians(90), 0)
    bpy.ops.object.transform_apply(rotation=True)
    suavizar(o)
    return o


def esfera_base(nome):
    bm = bmesh.new()
    bmesh.ops.create_icosphere(bm, subdivisions=2, radius=1.0)
    me = bpy.data.meshes.new(nome)
    bm.to_mesh(me)
    bm.free()
    for p in me.polygons:
        p.use_smooth = True
    return me


def cargas(malha, pontos, raio):
    out = []
    for p in pontos:
        o = bpy.data.objects.new("Carga", malha)
        o.location = p
        o.scale = (raio, raio, raio)
        bpy.context.collection.objects.link(o)
        out.append(o)
    return out


def reticulado(raio, a_ini, a_fim, n_ang, n_x, margem_x=0.3):
    """Carga uniforme por comprimento: reticulado escalonado sobre a superfície (nunca no volume)."""
    pts = []
    for i in range(n_x):
        x = -L / 2 + margem_x + (L - 2 * margem_x) * i / (n_x - 1)
        for j in range(n_ang):
            f = (j + (0.5 if i % 2 else 0.0)) / n_ang
            a = a_ini + (a_fim - a_ini) * min(f, 1.0)
            pts.append((x, raio * math.cos(a), raio * math.sin(a)))
    return pts


# ── materiais ───────────────────────────────────────────────────────────────
def material_metal(nome, cor_centro, cor_borda, emissao, metalico=0.55, rug=0.5, translucido=False):
    """Metal escuro e fosco; o contorno claro vem do Layer Weight (borda da silhueta). Guarda os valores originais para o holofote."""
    mat = bpy.data.materials.new(nome)
    mat.use_nodes = True
    nt = mat.node_tree
    bsdf = nt.nodes["Principled BSDF"]
    saida = nt.nodes["Material Output"]
    lw = nt.nodes.new("ShaderNodeLayerWeight")
    lw.inputs["Blend"].default_value = 0.5
    mix = nt.nodes.new("ShaderNodeMix")
    mix.data_type = "RGBA"
    cA, cB = hexc(cor_centro), hexc(cor_borda)
    mix.inputs[6].default_value, mix.inputs[7].default_value = cA, cB
    nt.links.new(lw.outputs["Facing"], mix.inputs[0])
    nt.links.new(mix.outputs[2], bsdf.inputs["Base Color"])
    nt.links.new(mix.outputs[2], bsdf.inputs["Emission Color"])
    bsdf.inputs["Metallic"].default_value = metalico
    bsdf.inputs["Roughness"].default_value = rug
    bsdf.inputs["Emission Strength"].default_value = emissao
    mat["orig"] = {"A": list(cA), "B": list(cB), "emi": emissao}
    if translucido:                                   # núcleo vira vidro escuro quando a gaussiana está dentro dele
        tr = nt.nodes.new("ShaderNodeBsdfTransparent")
        ms = nt.nodes.new("ShaderNodeMixShader")
        nt.links.new(tr.outputs[0], ms.inputs[1])
        nt.links.new(bsdf.outputs[0], ms.inputs[2])
        nt.links.new(ms.outputs[0], saida.inputs["Surface"])
        mat["ms"] = ms.name
        try:
            mat.surface_render_method = "DITHERED"
        except (AttributeError, TypeError):
            pass
    return mat


def material_carga(nome, cor, emissao):
    mat = co._material(nome, {"cor": cor, "emissao": emissao, "rugosidade": 0.45})
    mat["orig"] = {"emi": emissao}
    return mat


def escurecer(mat, f, opac=1.0):
    """Holofote: multiplica cor e brilho por `f` (0 a 1); `opac` < 1 só vale no material translúcido do núcleo."""
    nt, o = mat.node_tree, mat["orig"]
    bsdf = nt.nodes["Principled BSDF"]
    bsdf.inputs["Emission Strength"].default_value = o["emi"] * f
    mix = next((n for n in nt.nodes if n.bl_idname == "ShaderNodeMix"), None)
    if mix is not None:
        mix.inputs[6].default_value = [c * f if i < 3 else 1.0 for i, c in enumerate(o["A"])]
        mix.inputs[7].default_value = [c * f if i < 3 else 1.0 for i, c in enumerate(o["B"])]
    if "ms" in mat:
        nt.nodes[mat["ms"]].inputs[0].default_value = opac      # fator 1 = Principled (opaco); 0 = transparente


def arestas_luminosas(mat_borda, a0, a1):
    """Contornos importantes (finos e luminosos): aros das pontas da casca e do núcleo e as quatro arestas do corte."""
    def arco(raio, x, ini, fim, n=64):
        return [(x, raio * math.cos(ini + (fim - ini) * k / n), raio * math.sin(ini + (fim - ini) * k / n)) for k in range(n + 1)]
    pl = []
    for x in (-L / 2, L / 2):
        pl += [(arco(B, x, a0, a1), False), (arco(B - T, x, a0, a1), False)]
        pl.append((arco(A, x, 0, 2 * math.pi, 96)[:-1], True))
    for ang in (a0, a1):
        for raio in (B, B - T):
            pl.append(([(-L / 2, raio * math.cos(ang), raio * math.sin(ang)), (L / 2, raio * math.cos(ang), raio * math.sin(ang))], False))
    return v3.curva("Contornos", pl, mat_borda, 0.012)


# ── gaussiana, campo, câmera ────────────────────────────────────────────────
def gaussiana(r, mat_traco, phi):
    """Construção matemática: vidro violeta muito translúcido, aros contínuos nas pontas e só duas guias tracejadas."""
    Y, Z = (0, 1, 0), (0, 0, 1)
    corpo = cm.criar_corpo_macico(r, GL)
    corpo.name = "GaussFaces"
    ga.vidro_gaussiana(corpo)
    tracos = []
    for x in (-GL / 2, GL / 2):
        tracos += ga.circulo((x, 0, 0), Y, Z, r, True)
    for ang in (phi - math.radians(30), phi + math.radians(30)):
        tracos += ga.linha((-GL / 2, r * math.cos(ang), r * math.sin(ang)), (GL / 2, r * math.cos(ang), r * math.sin(ang)), False)
    return [ga.criar_curva("GaussTracos", tracos, mat_traco, 0.013), corpo]


# setas do vão: (x, ângulo em graus, raio inicial); comprimento ∝ 1/r (as de dentro são maiores), todas dentro do vão
SETAS = ((-1.5, 103.0, 0.68), (0.3, 192.0, 0.90), (1.5, 103.0, 1.10))
K_CAMPO = 0.34


def setas_do_vao(mat):
    out = []
    for x, graus, r0 in SETAS:
        t = math.radians(graus)
        d = (0.0, math.cos(t), math.sin(t))
        comp = K_CAMPO / r0
        o = v3.seta((x, r0 * d[1], r0 * d[2]), d, mat, comprimento=comp)
        o.scale = (0.75, 0.75, comp)
        out.append(o)
    return out


def camera_ortografica(pontos, az, el, margem, largura, altura):
    sc = bpy.context.scene
    sc.render.resolution_x, sc.render.resolution_y = largura, altura
    cd = bpy.data.cameras.new("Camera")
    cd.type = "ORTHO"
    cd.clip_start, cd.clip_end = 0.1, 200.0
    cam = bpy.data.objects.new("Camera", cd)
    bpy.context.collection.objects.link(cam)
    sc.camera = cam
    a, e = math.radians(az), math.radians(el)
    direcao = Vector((math.cos(e) * math.cos(a), math.cos(e) * math.sin(a), math.sin(e)))
    centro = sum(pontos, Vector()) / len(pontos)
    cam.location = centro + direcao * 40
    quat = (centro - cam.location).to_track_quat("-Z", "Y")
    cam.rotation_euler = quat.to_euler()
    dir_x, dir_y = quat @ Vector((1, 0, 0)), quat @ Vector((0, 1, 0))
    xs, ys = [(p - centro).dot(dir_x) for p in pontos], [(p - centro).dot(dir_y) for p in pontos]
    cx, cy = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2
    centro = centro + dir_x * cx + dir_y * cy
    cam.location = centro + direcao * 40
    cd.ortho_scale = max(max(xs) - min(xs), (max(ys) - min(ys)) * largura / altura) / (1 - 2 * margem)
    return cam


def pesos(r):
    """Holofote por região (suave nas fronteiras): brilho do núcleo, da casca, opacidade do núcleo e visibilidade do campo."""
    t12, t23 = ss((r - (A - 0.04)) / 0.16), ss((r - (B - 0.06)) / 0.2)
    tri = lambda v1, v2, v3_: v1 + (v2 - v1) * t12 + (v3_ - v2) * t23   # noqa: E731
    campo = ss((r - A) / 0.14) * (1 - ss((r - (B - 0.26)) / 0.2))
    return {"nucleo": tri(1.0, 0.62, 0.8), "casca": tri(0.45, 0.62, 0.8), "opac": 0.5 + 0.5 * ss((r - (A - 0.05)) / 0.14), "campo": campo}


def argumentos():
    resto = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    ap = argparse.ArgumentParser(prog="render_sequencia_v2.py")
    ap.add_argument("--estados", action="store_true")
    ap.add_argument("--frames", type=int, default=90)
    ap.add_argument("--res", default="1120x784")
    ap.add_argument("--amostras", type=int, default=64)
    ap.add_argument("--r0", type=float, default=0.25)
    ap.add_argument("--r1", type=float, default=1.95)
    ap.add_argument("--saida")
    return ap.parse_args(resto)


def remover(objs):
    for o in objs:
        dados = o.data
        bpy.data.objects.remove(o, do_unlink=True)
        (bpy.data.meshes if isinstance(dados, bpy.types.Mesh) else bpy.data.curves).remove(dados)


def main():
    a = argumentos()
    largura, altura = (int(x) for x in a.res.lower().split("x"))
    pasta = Path(a.saida).resolve() if a.saida else RAIZ / "renders" / "teste_gauss_coaxial_v2" / a.res
    pasta.mkdir(parents=True, exist_ok=True)

    co.limpar_cena()
    # o corte da casca abre para a câmera: centrado na direção da câmera projetada no plano YZ
    phi = math.atan2(math.sin(math.radians(EL)), math.cos(math.radians(EL)) * math.sin(math.radians(AZ)))
    meia = math.radians(CUNHA / 2)
    a0, a1 = phi + meia, phi + 2 * math.pi - meia
    mat_nucleo = material_metal("MetalNucleo", "fonte_escura", "fonte_contorno", 0.16, translucido=True)
    mat_casca = material_metal("MetalCasca", "fonte_escura", "fonte_contorno", 0.16)
    mat_carga_n, mat_carga_c = material_carga("CargaNucleo", "fonte_contorno", 1.7), material_carga("CargaCasca", "fonte_contorno", 1.7)
    mat_borda = v3.material_cor("Contorno", "fonte_contorno", 1.5)
    mat_campo = v3.material_cor("CampoVao", "campo_eletrico", 2.2)
    mat_traco = ga.material_traco()

    n = nucleo()
    n.data.materials.append(mat_nucleo)
    c = casca_aberta(a0, a1)
    c.data.materials.append(mat_casca)
    arestas_luminosas(mat_borda, a0, a1)
    # +λ na superfície externa do núcleo; −λ na superfície interna da casca (mesmo nº por comprimento), com a mesma grade
    ang_ext = 0.035
    esf_n, esf_c = esfera_base("EsferaN"), esfera_base("EsferaC")
    esf_n.materials.append(mat_carga_n)
    esf_c.materials.append(mat_carga_c)
    cargas(esf_n, reticulado(A + 0.012, 0, 2 * math.pi * (1 - 1 / 18), 18, 9), 0.034)
    cargas(esf_c, reticulado(B - T - 0.012, a0 + 0.12, a1 - 0.12, 14, 9), 0.034)
    setas = setas_do_vao(mat_campo)
    co.mundo()
    co.luzes()

    maxima = gaussiana(a.r1, mat_traco, phi)
    pontos = co.cantos([c, n, maxima[-1]])
    remover(maxima)
    camera_ortografica(pontos, AZ, EL, MARGEM, largura, altura)
    sc = bpy.context.scene
    sc.render.film_transparent = True
    sc.render.image_settings.color_mode = "RGBA"

    def montar(r):
        w = pesos(r)
        escurecer(mat_nucleo, w["nucleo"], w["opac"])
        escurecer(mat_casca, w["casca"])
        escurecer(mat_carga_n, w["nucleo"])
        escurecer(mat_carga_c, w["casca"])
        mat_campo.node_tree.nodes["Principled BSDF"].inputs["Emission Strength"].default_value = 2.2 * w["campo"]
        for s in setas:
            s.hide_render = w["campo"] < 0.04
        return gaussiana(r, mat_traco, phi)

    co.render(pasta / "_aquecimento.png", largura, altura, a.amostras)
    (pasta / "_aquecimento.png").unlink()
    t0 = time.perf_counter()
    if a.estados:
        for nome, r in (("1_dentro", 0.3), ("2_vao", 1.0), ("3_fora", 1.75)):
            objs = montar(r)
            sc.render.filepath = str(pasta / f"estado_{nome}.png")
            bpy.ops.render.render(write_still=True)
            remover(objs)
        print(f"V2_ESTADOS {largura}x{altura} total={time.perf_counter() - t0:.1f}s -> {pasta}")
        return
    for i in range(a.frames):
        objs = montar(a.r0 + (a.r1 - a.r0) * i / (a.frames - 1))
        sc.render.filepath = str(pasta / f"frame_{i + 1:04d}.png")
        bpy.ops.render.render(write_still=True)
        remover(objs)
    (pasta / "meta.json").write_text(json.dumps({"frames": a.frames, "r0": a.r0, "r1": a.r1, "a": A, "b": B, "res": a.res, "amostras": a.amostras},
                                                ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"V2_SEQUENCIA {largura}x{altura} frames={a.frames} medio={(time.perf_counter() - t0) / a.frames:.2f}s "
          f"total={time.perf_counter() - t0:.1f}s -> {pasta}")


if __name__ == "__main__":
    main()

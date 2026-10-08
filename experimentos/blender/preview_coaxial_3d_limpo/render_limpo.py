"""Coaxial 3D limpo (sandbox): o sólido em corte fica na tela o tempo todo; a gaussiana cilíndrica varia só o raio, nos instantes reais do vídeo.

Reaproveita as peças do coaxial v2 (núcleo, casca com corte, contornos) sem alterá-las. Sem bolinhas nem halos: poucos símbolos + (azul, no núcleo)
e − (magenta, na face interna da casca), orientados para a câmera; cinco setas radiais iguais num único plano transversal do vão; gaussiana
com contorno fino e preenchimento quase invisível. O recorte é só ilustrativo: o modelo é o coaxial ideal completo.

    blender.exe -b -P experimentos/blender/preview_coaxial_3d_limpo/render_limpo.py -- [--estados]
--estados renderiza só 4 quadros de validação (intro e as três regiões) em renders/preview_coaxial_3d_limpo/_estados.
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
sys.path.insert(0, str(AQUI))
sys.path.insert(0, str(AQUI.parent))
sys.path.insert(0, str(AQUI.parent / "teste_gauss_coaxial"))
import casca_oca as co  # noqa: E402
import cilindro_macico as cm  # noqa: E402
import gaussiana as ga  # noqa: E402
import render_sequencia_v2 as v2  # noqa: E402
import vetores3d as v3  # noqa: E402
from trajetoria import A, B, RB, quadros_unicos, ss  # noqa: E402

AZ, EL, RES, MARGEM = -32.0, 18.0, (1120, 784), 0.035
GL = v2.GL                                          # comprimento L fixo da gaussiana
X_SETAS, R_INI, COMP = 1.7, 0.72, 0.45              # plano transversal das setas (perto da ponta aberta, bem visível), raio inicial, comprimento
PASTA = RAIZ / "renders" / "preview_coaxial_3d_limpo" / "1120x784"


def malha_sinal(nome, mais):
    """Símbolo plano (no plano XY local) feito de barras finas: + ou −."""
    bm = bmesh.new()
    s, e = 0.125, 0.03
    for sx, sy in ((s, e), (e, s)) if mais else ((s, e),):
        bmesh.ops.create_cube(bm, size=1.0, matrix=__import__("mathutils").Matrix.Diagonal((2 * sx, 2 * sy, 0.02, 1.0)))
    me = bpy.data.meshes.new(nome)
    bm.to_mesh(me)
    bm.free()
    return me


def simbolos(cam, phi, a0, a1):
    """Poucos sinais esquemáticos sobre as superfícies certas e visíveis: + no núcleo (lado da câmera), − na face interna da casca (parede do fundo)."""
    m_pos = v2.material_carga("SinalPos", "fonte_contorno", 1.2)
    m_neg = v2.material_carga("SinalNeg", "apoio_magenta", 1.4)
    mp, mn = malha_sinal("Mais", True), malha_sinal("Menos", False)
    mp.materials.append(m_pos)
    mn.materials.append(m_neg)
    rot = cam.rotation_euler.copy()                                             # símbolos paralelos ao plano da imagem
    objs = []
    for x in (-1.4, 0.0, 1.4):
        for dg in (-50, 0, 50):                                                 # núcleo: normais voltadas para a câmera
            t = phi + math.radians(dg)
            n = Vector((0, math.cos(t), math.sin(t)))
            objs.append(("pos", Vector((x, 0, 0)) + (A + 0.09) * n, mp))
        for dg in (-45, 0, 45):                                                 # casca: face interna do lado oposto à câmera (dentro do arco que existe)
            t = phi + math.pi + math.radians(dg)
            n = Vector((0, math.cos(t), math.sin(t)))
            objs.append(("neg", Vector((x, 0, 0)) + (B - v2.T - 0.09) * n, mn))
    for _, pos, malha in objs:
        o = bpy.data.objects.new("Sinal", malha)
        o.location = pos
        o.rotation_euler = rot
        bpy.context.collection.objects.link(o)


def setas_do_vao(phi):
    """Quatro setas radiais iguais no mesmo plano transversal x = X_SETAS: haste fina, ponta simples, pouco brilho; mesma origem radial e mesmo comprimento."""
    mat = v3.material_cor("CampoVao", "campo_eletrico", 1.1)
    out = []
    for dg in (-135, -75, 75, 135):                                             # longe da direção da câmera (sem seta de frente) e fora da frente do núcleo
        t = phi + math.radians(dg)
        d = (0.0, math.cos(t), math.sin(t))
        s = v3.seta((X_SETAS, R_INI * d[1], R_INI * d[2]), d, mat, comprimento=COMP)
        s.scale = (0.55, 0.55, COMP)
        out.append(s)
    return out


def gaussiana(c, r, phi):
    """Cilindro fechado (L fixo): aro frontal fino e contínuo, aro de trás e duas guias tracejados, preenchimento quase invisível."""
    Y, Z = (0, 1, 0), (0, 0, 1)
    corpo = cm.criar_corpo_macico(r, GL)
    corpo.data.materials.append(c.m_fant)
    frente = ga.circulo((GL / 2, 0, 0), Y, Z, r, True)
    tras = ga.circulo((-GL / 2, 0, 0), Y, Z, r, False)
    for ang in (phi - 0.55, phi + 0.55):
        tras += ga.linha((-GL / 2, r * math.cos(ang), r * math.sin(ang)), (GL / 2, r * math.cos(ang), r * math.sin(ang)), False)
    return [ga.criar_curva("GFrente", frente, c.m_traco, 0.012), ga.criar_curva("GTras", tras, c.m_traco2, 0.008), corpo]


def remover(objs):
    for o in objs:
        dados = o.data
        bpy.data.objects.remove(o, do_unlink=True)
        if dados is not None and dados.users == 0 and not dados.use_fake_user:
            (bpy.data.meshes if isinstance(dados, bpy.types.Mesh) else bpy.data.curves).remove(dados)


def material_fantasma():
    mat = bpy.data.materials.new("GaussFantasma")
    mat.use_nodes = True
    b = mat.node_tree.nodes["Principled BSDF"]
    cor = co.hex_linear(co.E.cor("gaussiana"))
    b.inputs["Base Color"].default_value = cor
    b.inputs["Emission Color"].default_value = cor
    b.inputs["Emission Strength"].default_value = 0.2
    b.inputs["Alpha"].default_value = 0.035
    b.inputs["Roughness"].default_value = 1.0
    for chave in ("Specular IOR Level", "Specular"):
        if chave in b.inputs:
            b.inputs[chave].default_value = 0.0
    try:
        mat.surface_render_method = "DITHERED"
    except (AttributeError, TypeError):
        pass
    return mat


class Ctx:
    pass


def main():
    resto = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    ap = argparse.ArgumentParser()
    ap.add_argument("--estados", action="store_true")
    ap.add_argument("--amostras", type=int, default=64)
    a = ap.parse_args(resto)
    pasta = PASTA.parent / "_estados" if a.estados else PASTA
    pasta.mkdir(parents=True, exist_ok=True)

    co.limpar_cena()
    c = Ctx()
    c.m_fant = material_fantasma()
    c.m_traco = ga.material_traco()
    c.m_traco.node_tree.nodes["Principled BSDF"].inputs["Emission Strength"].default_value = 1.4
    c.m_traco2 = ga.material_traco()
    c.m_traco2.node_tree.nodes["Principled BSDF"].inputs["Emission Strength"].default_value = 0.8
    phi = math.atan2(math.sin(math.radians(EL)), math.cos(math.radians(EL)) * math.sin(math.radians(AZ)))
    meia = math.radians(v2.CUNHA / 2)
    a0, a1 = phi + meia, phi + 2 * math.pi - meia
    m_nucleo = v2.material_metal("MetalNucleo", "fonte_escura", "fonte_contorno", 0.10, translucido=True)
    m_casca = v2.material_metal("MetalCasca", "fonte_escura", "fonte_contorno", 0.10)
    n = v2.nucleo()
    n.data.materials.append(m_nucleo)
    cs = v2.casca_aberta(a0, a1)
    cs.data.materials.append(m_casca)
    v2.arestas_luminosas(v3.material_cor("Contorno", "fonte_contorno", 0.8), a0, a1)
    setas_do_vao(phi)
    co.mundo()
    co.luzes()
    maxima = gaussiana(c, RB, phi)                                              # enquadramento pelo MAIOR raio da gaussiana
    pontos = co.cantos([cs, n, maxima[-1]])
    remover(maxima)
    cam = v2.camera_ortografica(pontos, AZ, EL, MARGEM, *RES)
    simbolos(cam, phi, a0, a1)
    sc = bpy.context.scene
    sc.render.film_transparent = True
    sc.render.image_settings.color_mode = "RGBA"
    co.render(pasta / "_aq.png", *RES, a.amostras)
    (pasta / "_aq.png").unlink()

    todos = quadros_unicos()
    if a.estados:
        todos = [q for q in todos if q[0] in ("intro", "h0", "h1", "h2")]
    t0 = time.perf_counter()
    for chave, r in todos:
        v2.escurecer(m_nucleo, 1.0, 1.0 if r is None else 0.55 + 0.45 * ss((r - (A - 0.05)) / 0.14))   # núcleo translúcido só com a gaussiana dentro dele
        objs = [] if r is None else gaussiana(c, r, phi)
        sc.render.filepath = str(pasta / f"q_{chave}.png")
        bpy.ops.render.render(write_still=True)
        remover(objs)
    print(f"LIMPO quadros={len(todos)} total={time.perf_counter() - t0:.1f}s medio={(time.perf_counter() - t0) / len(todos):.2f}s -> {pasta}")


if __name__ == "__main__":
    main()

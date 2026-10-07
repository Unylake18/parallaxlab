"""Superfícies gaussianas (esférica, cilíndrica, caixa) — estudo 6 (sandbox, não integrado a vídeo).

Rodar (sem abrir a interface), a partir da raiz do repositório:
    blender.exe -b -P experimentos/blender/gaussiana.py

Gera out/gaussiana_esfera_v1.png, gaussiana_cilindro_v1.png e gaussiana_caixa_v1.png: cada superfície sobre uma
fonte aprovada do arsenal, para validar a leitura do violeta tracejado sobre o vidro azul.

Gramática (arsenal/estilo.json): superfície gaussiana = violeta #9C8CFF, TRACEJADA ou translúcida, nunca sólida.
Traço contínuo = parte que contribui ao fluxo; tracejado = parte que não contribui / só construção.
"""

import math
import sys
from pathlib import Path

import bpy
from mathutils import Vector

sys.path.insert(0, str(Path(__file__).resolve().parent))
import casca_oca as co  # noqa: E402
import cilindro_macico as cm  # noqa: E402
import esferas as es  # noqa: E402
import placa as pl  # noqa: E402

G = co.ST["materiais"]["gaussiana"]


# ── geometria dos traços ────────────────────────────────────────────────────
def circulo(centro, u, v, raio, continuo):
    """Polilinhas de um círculo no plano (u, v): fechado se contínuo; arcos separados por vãos se tracejado."""
    centro, u, v = Vector(centro), Vector(u), Vector(v)
    ponto = lambda a: centro + raio * (math.cos(a) * u + math.sin(a) * v)  # noqa: E731
    if continuo:
        n = max(64, int(raio * 48))
        return [([ponto(2 * math.pi * k / n) for k in range(n)], True)]
    n_tracos = max(8, round(2 * math.pi * raio / G["periodo_traco"]))
    passo = 2 * math.pi / n_tracos
    saida = []
    for k in range(n_tracos):
        a0 = k * passo
        n_pts = 8
        saida.append(([ponto(a0 + passo * G["razao_traco"] * j / (n_pts - 1)) for j in range(n_pts)], False))
    return saida


def linha(p0, p1, continuo):
    """Polilinhas do segmento p0-p1: uma linha contínua ou traços com vãos."""
    p0, p1 = Vector(p0), Vector(p1)
    if continuo:
        return [([p0, p1], False)]
    n = max(2, round((p1 - p0).length / G["periodo_traco"]))
    d = (p1 - p0) / n
    return [([p0 + d * k, p0 + d * (k + G["razao_traco"])], False) for k in range(n)]


def criar_curva(nome, polilinhas, material):
    curva = bpy.data.curves.new(nome, "CURVE")
    curva.dimensions = "3D"
    curva.bevel_depth = G["espessura_traco"]
    curva.bevel_resolution = 3
    curva.use_fill_caps = True
    for pts, ciclico in polilinhas:
        s = curva.splines.new("POLY")
        s.points.add(len(pts) - 1)
        for i, p in enumerate(pts):
            s.points[i].co = (p[0], p[1], p[2], 1.0)
        s.use_cyclic_u = ciclico
    obj = bpy.data.objects.new(nome, curva)
    bpy.context.collection.objects.link(obj)
    obj.data.materials.append(material)
    return obj


def material_traco():
    cor = co.E.cor(G["cor"])
    mat = bpy.data.materials.new("TracoGaussiana")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = co.hex_linear(cor)
    bsdf.inputs["Roughness"].default_value = 0.4
    bsdf.inputs["Emission Color"].default_value = co.hex_linear(cor)
    bsdf.inputs["Emission Strength"].default_value = G["emissao_traco"]
    return mat


def vidro_gaussiana(obj):
    """Faces translúcidas e discretas na cor da gaussiana: nunca preenchimento sólido."""
    cm.material_vidro(obj, cor=G["cor"], base=G["vidro_base"], ganho=G["vidro_ganho"],
                      brilho_borda=G["vidro_brilho_borda"])


# ── superfícies ─────────────────────────────────────────────────────────────
def criar_gaussiana_esferica(raio=1.5, continua=0, faces=1, offset=(0, 0, 0)):
    """Esfera gaussiana: equador e dois meridianos (traços) sobre um orbe translúcido violeta."""
    mat = material_traco()
    c = tuple(offset)
    X, Y, Z = (1, 0, 0), (0, 1, 0), (0, 0, 1)
    tracos = circulo(c, X, Y, raio, continua) + circulo(c, X, Z, raio, continua) + circulo(c, Y, Z, raio, continua)
    objs = [criar_curva("GaussEsferaTracos", tracos, mat)]
    if faces:
        bpy.ops.mesh.primitive_uv_sphere_add(segments=96, ring_count=48, radius=raio, location=c)
        corpo = bpy.context.active_object
        corpo.name = "GaussEsferaFaces"
        bpy.ops.object.shade_smooth()
        vidro_gaussiana(corpo)
        objs.append(corpo)
    return objs


def criar_gaussiana_cilindrica(raio=1.5, comprimento=3.0, lateral_continua=0, tampas_continuas=0,
                               n_linhas=4, faces=1, offset=(0, 0, 0)):
    """Cilindro gaussiano fechado (eixo X): tampas e linhas longitudinais, sobre vidro violeta."""
    mat = material_traco()
    ox, oy, oz = offset
    Y, Z = (0, 1, 0), (0, 0, 1)
    meio = comprimento / 2
    tracos = []
    for x in (-meio, meio):
        tracos += circulo((ox + x, oy, oz), Y, Z, raio, tampas_continuas)
    for k in range(n_linhas):
        a = 2 * math.pi * k / n_linhas
        y, z = raio * math.cos(a), raio * math.sin(a)
        tracos += linha((ox - meio, oy + y, oz + z), (ox + meio, oy + y, oz + z), lateral_continua)
    objs = [criar_curva("GaussCilindroTracos", tracos, mat)]
    if faces:
        corpo = cm.criar_corpo_macico(raio, comprimento)
        corpo.name = "GaussCilindroFaces"
        corpo.location = offset
        vidro_gaussiana(corpo)
        objs.append(corpo)
    return objs


def criar_gaussiana_caixa(lado=2.4, altura=1.4, continua=0, faces=1, offset=(0, 0, 0)):
    """Caixa gaussiana (pillbox): `altura` ao longo de X (a normal do plano), `lado` em Y e Z."""
    mat = material_traco()
    ox, oy, oz = offset
    hx, hy = altura / 2, lado / 2
    cantos = [(sx * hx, sy * hy, sz * hy) for sx in (-1, 1) for sy in (-1, 1) for sz in (-1, 1)]
    idx = {c: i for i, c in enumerate(cantos)}
    arestas = [(a, b) for a in cantos for b in cantos
               if idx[a] < idx[b] and sum(1 for i in range(3) if a[i] != b[i]) == 1]
    tracos = []
    for a, b in arestas:
        tracos += linha((ox + a[0], oy + a[1], oz + a[2]), (ox + b[0], oy + b[1], oz + b[2]), continua)
    objs = [criar_curva("GaussCaixaTracos", tracos, mat)]
    if faces:
        bpy.ops.mesh.primitive_cube_add(size=1, location=offset)
        corpo = bpy.context.active_object
        corpo.name = "GaussCaixaFaces"
        corpo.scale = (altura, lado, lado)
        bpy.ops.object.transform_apply(scale=True)
        vidro_gaussiana(corpo)
        objs.append(corpo)
    return objs


# ── cenas de validação: cada gaussiana sobre uma fonte aprovada ─────────────
def _fechar(alvos, azimute=None, elevacao=None, margem=0.09):
    """Enquadra todos os `alvos`; a zona de profundidade das cargas vem do primeiro."""
    co.mundo()
    co.luzes()
    kw = {} if azimute is None else {"azimute": azimute, "elevacao": elevacao}
    cam = co.camera_enquadrada(co.cantos(alvos), margem=margem, **kw)
    try:
        cm.ajustar_profundidade(cam, alvos[0])
    except KeyError:
        pass  # sem cargas na cena
    return cam


def cena_esfera():
    co.limpar_cena()
    fonte, _ = es.criar_esfera_macica(raio=1.0, n_cargas=50, dist_min=0.34)
    objs = criar_gaussiana_esferica(1.5)
    _fechar([objs[-1]])  # a gaussiana (maior) contém a fonte
    co.render(co.OUT / "gaussiana_esfera_v1.png")


def cena_cilindro():
    co.limpar_cena()
    fonte, _ = cm.criar_macico(raio=1.0, comprimento=4.0, n_cargas=80)
    gauss = criar_gaussiana_cilindrica(1.5, 3.0, lateral_continua=1)
    _fechar([fonte, gauss[-1]], azimute=-45, elevacao=20)
    co.render(co.OUT / "gaussiana_cilindro_v1.png")


def cena_caixa():
    co.limpar_cena()
    corpo, _, proxy = pl.criar_placa_carregada(largura=8.0, altura=5.0, n_cargas=90, dist_min=0.55)
    criar_gaussiana_caixa(2.4, 1.4)
    _fechar([proxy], azimute=-40, elevacao=16, margem=0.06)
    co.render(co.OUT / "gaussiana_caixa_v1.png")


if __name__ == "__main__":
    cena_esfera()
    cena_cilindro()
    cena_caixa()

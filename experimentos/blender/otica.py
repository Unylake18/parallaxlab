"""Lente, prisma e anteparo de fenda dupla (Óptica 7.2 a 7.4) — estudo 12 (sandbox).

Rodar: blender.exe -b -P experimentos/blender/otica.py   (gera out/otica_v1.png)

Vidro azul-claro translúcido para os elementos transparentes; o anteparo é opaco (azul de "fonte física"). Raios, frentes
de onda e a figura de interferência são do Manim. Eixo óptico = eixo X (tracejado neutro); focos = marcas neutras.
"""

import math
import sys
from pathlib import Path

import bpy

sys.path.insert(0, str(Path(__file__).resolve().parent))
import casca_oca as co  # noqa: E402
import cilindro_macico as cm  # noqa: E402
import gaussiana as ga  # noqa: E402
import revolucao as rv  # noqa: E402

OT = co.ST["materiais"]["otica"]


def _vidro(obj):
    cm.material_vidro(obj, cor=OT["vidro_cor"], base=OT["vidro_base"], ganho=OT["vidro_ganho"], brilho_borda=OT["vidro_brilho"])


def _risco_mat():
    return co._material("RiscoOtica", {"cor": "fonte_contorno", "emissao": 1.0, "rugosidade": 0.4})


def _marca(pos, raio=0.06):
    mat = co._material("MarcaOtica", {"cor": "texto_neutro", "emissao": 2.2, "rugosidade": 0.4})
    bpy.ops.mesh.primitive_uv_sphere_add(radius=raio, segments=24, ring_count=12, location=pos)
    o = bpy.context.active_object
    o.name = "Foco"
    bpy.ops.object.shade_smooth()
    o.data.materials.append(mat)
    return o


def _eixo_optico(x0, x1):
    mat = co._material("EixoOptico", {"cor": "texto_neutro", "emissao": 0.8, "rugosidade": 0.5})
    ga.criar_curva("EixoOptico", ga.linha((x0, 0, 0), (x1, 0, 0), False), mat, 0.01)


def criar_lente(forma="biconvexa", diametro=2.4, raio1=3.0, raio2=3.0, espessura_borda=0.08, indice=1.5, focos=1, eixo=1):
    """Lente delgada de vidro, eixo X. 'biconvexa' (converge) ou 'biconcava' (diverge). Devolve o corpo."""
    h = diametro / 2
    sag = lambda r, R: R - math.sqrt(R * R - r * r)             # flecha do arco de raio R
    convexa = forma == "biconvexa"
    tc = sag(h, raio1) + sag(h, raio2) + espessura_borda if convexa else espessura_borda
    NP = 60
    rs = [h * i / NP for i in range(NP + 1)]
    if convexa:
        frente = [(-tc / 2 + sag(r, raio1), r) for r in rs]
        tras = [(tc / 2 - sag(r, raio2), r) for r in rs]
    else:
        frente = [(-tc / 2 - sag(r, raio1), r) for r in rs]
        tras = [(tc / 2 + sag(r, raio2), r) for r in rs]
    laco = frente + list(reversed(tras))
    corpo = rv.malha_revolucao("Lente", laco, "X")
    _vidro(corpo)
    if eixo:
        _eixo_optico(-2.6, 2.6)
    if focos:
        f = 1.0 / ((indice - 1) * (1 / raio1 + 1 / raio2))      # equação dos fabricantes de lentes (delgada)
        for s in (-1, 1):
            _marca((s * f, 0, 0))
    return corpo


def criar_prisma(angulo_apice=60.0, base=2.0, comprimento=2.0, eixo=0):
    """Prisma triangular isósceles de vidro (seção no plano XY, extrudado ao longo de Z), apoiado na base."""
    a = math.radians(angulo_apice)
    altura = base / (2 * math.tan(a / 2))
    cy = altura / 3
    tri = [(-base / 2, -cy), (base / 2, -cy), (0.0, altura - cy)]
    z0, z1 = -comprimento / 2, comprimento / 2
    verts = [(x, y, z0) for x, y in tri] + [(x, y, z1) for x, y in tri]
    faces = [(0, 2, 1), (3, 4, 5), (0, 1, 4, 3), (1, 2, 5, 4), (2, 0, 3, 5)]
    me = bpy.data.meshes.new("Prisma")
    me.from_pydata(verts, [], faces)
    me.update()
    o = bpy.data.objects.new("Prisma", me)
    bpy.context.collection.objects.link(o)
    bpy.context.view_layer.objects.active = o
    o.select_set(True)
    bpy.ops.object.shade_smooth_by_angle(angle=math.radians(35))
    bm_fix = __import__("bmesh").new()
    bm_fix.from_mesh(me)
    __import__("bmesh").ops.recalc_face_normals(bm_fix, faces=bm_fix.faces)
    bm_fix.to_mesh(me)
    bm_fix.free()
    _vidro(o)
    mat = _risco_mat()
    arestas = [(0, 1), (1, 2), (2, 0), (3, 4), (4, 5), (5, 3), (0, 3), (1, 4), (2, 5)]
    for i, j in arestas:
        ga.criar_curva("ArestaPrisma", [([verts[i], verts[j]], False)], mat, OT["aresta_espessura"])
    if eixo:
        _eixo_optico(-3, 3)
    return o


def criar_fenda_dupla(largura=4.0, altura=3.0, espessura=0.12, fenda=0.2, separacao=1.0):
    """Anteparo opaco (normal X) com duas fendas verticais (ao longo de Z) de largura `fenda`, separadas de `separacao`
    (entre centros). Devolve o conjunto (primeiro pedaço) para enquadrar."""
    mat = co._material("Anteparo", {"cor": "fonte_fisica", "emissao": OT["anteparo_emissao"], "rugosidade": 0.4, "metalico": 0.2})
    mat_r = _risco_mat()
    bordas = [-largura / 2, -separacao / 2 - fenda / 2, -separacao / 2 + fenda / 2,
              separacao / 2 - fenda / 2, separacao / 2 + fenda / 2, largura / 2]
    pedacos = []
    for (y0, y1) in ((bordas[0], bordas[1]), (bordas[2], bordas[3]), (bordas[4], bordas[5])):
        bpy.ops.mesh.primitive_cube_add(size=1, location=(0, (y0 + y1) / 2, 0))
        p = bpy.context.active_object
        p.name = "Anteparo"
        p.scale = (espessura, y1 - y0, altura)
        bpy.ops.object.transform_apply(scale=True)
        p.data.materials.append(mat)
        pedacos.append(p)
    for y in (bordas[1], bordas[2], bordas[3], bordas[4]):       # arestas claras nas bordas das fendas
        for x in (-espessura / 2, espessura / 2):
            ga.criar_curva("ArestaFenda", [([(x, y, -altura / 2), (x, y, altura / 2)], False)], mat_r, OT["aresta_espessura"])
    return pedacos[0]


def cena_preview():
    co.limpar_cena()
    corpos = []
    corpos.append(criar_lente("biconvexa"))
    p = criar_prisma(); p.location = (0, 4.2, 0)
    corpos.append(p)
    f = criar_fenda_dupla(); f.location = (0, -4.2, 0)
    for o in list(bpy.data.objects):
        if o.name.startswith(("Anteparo", "ArestaFenda")):
            o.location = (o.location[0], o.location[1] - 4.2 if o.name.startswith("ArestaFenda") else o.location[1], o.location[2])
    co.mundo()
    co.luzes()
    co.camera_enquadrada(co.cantos(corpos + [f]), azimute=-40, elevacao=20, margem=0.07)
    co.render(co.OUT / "otica_v1.png")


if __name__ == "__main__":
    cena_preview()

"""Auxiliares 3D compartilhados: setas, polilinhas tracejadas e malhas paramétricas (sandbox).

Setas: malha única (haste + ponta, comprimento 1 ao longo de +Z) instanciada com dados compartilhados; cada seta é um
objeto com escala uniforme (comprimento) e rotação (direção). Cores vêm do estilo.json (ciano = campo, azul = normal,
branco = neutro, violeta = construção).
"""

import math
import sys
from pathlib import Path

import bmesh
import bpy
from mathutils import Matrix, Vector

sys.path.insert(0, str(Path(__file__).resolve().parent))
import casca_oca as co  # noqa: E402
import cilindro_macico as cm  # noqa: E402
import gaussiana as ga  # noqa: E402

_BASE = {}


def _malha_seta():
    try:                                       # a limpeza de cena (read_factory_settings) invalida a referência
        if "m" in _BASE and bpy.data.meshes.get(_BASE["m"].name) is _BASE["m"]:
            return _BASE["m"]
    except ReferenceError:
        pass
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=16, radius1=0.035, radius2=0.035, depth=0.78,
                          matrix=Matrix.Translation((0, 0, 0.39)))
    bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=16, radius1=0.1, radius2=0.0, depth=0.22,
                          matrix=Matrix.Translation((0, 0, 0.89)))
    me = bpy.data.meshes.new("SetaBase")
    me.use_fake_user = True                    # nunca zera usuários: as setas dinâmicas são criadas e removidas
    me["compartilhada"] = True
    bm.to_mesh(me)
    bm.free()
    me.materials.append(bpy.data.materials.new("SetaMaterialBase"))     # 1 slot; cada seta troca o material no OBJETO
    for p in me.polygons:
        p.use_smooth = True
    _BASE["m"] = me
    return me


def material_cor(nome, cor, emissao):
    return co._material(nome, {"cor": cor, "emissao": emissao, "rugosidade": 0.35})


def seta(origem, vetor, mat, comprimento=None):
    """Seta de `origem` na direção de `vetor`; comprimento = |vetor| a menos que seja dado."""
    v = Vector(vetor)
    comp = v.length if comprimento is None else comprimento
    if comp < 1e-6:
        return None
    o = bpy.data.objects.new("Seta", _malha_seta())
    bpy.context.collection.objects.link(o)
    o.rotation_mode = "QUATERNION"
    o.rotation_quaternion = Vector((0, 0, 1)).rotation_difference(v.normalized())
    o.scale = (comp, comp, comp)
    o.location = origem
    o.material_slots[0].link = "OBJECT"       # material por objeto: a malha é compartilhada entre todas as setas
    o.material_slots[0].material = mat
    return o


def tracejado(pts, fechado=False, periodo=0.3, razao=0.6):
    """Quebra a polilinha `pts` (comprimento de arco) em traços: devolve [(lista_de_pontos, False), ...]."""
    seq = list(pts) + ([pts[0]] if fechado else [])
    seg = [math.dist(a, b) for a, b in zip(seq, seq[1:])]
    total = sum(seg)
    n = max(4, round(total / periodo))
    acum = [0.0]
    for s in seg:
        acum.append(acum[-1] + s)

    def ponto(s):
        s = min(max(s, 0.0), total)
        i = max(1, min(len(acum) - 1, next((j for j in range(1, len(acum)) if acum[j] >= s), len(acum) - 1)))
        f = (s - acum[i - 1]) / ((acum[i] - acum[i - 1]) or 1.0)
        a, b = seq[i - 1], seq[i]
        return tuple(a[k] + f * (b[k] - a[k]) for k in range(3))

    passo = total / n
    return [([ponto(k * passo + passo * razao * j / 7) for j in range(8)], False) for k in range(n)]


def curva(nome, polilinhas, mat, espessura):
    return ga.criar_curva(nome, polilinhas, mat, espessura)


def malha_param(nome, F, u0, u1, v0, v1, nu=48, nv=48, espessura=None, vidro=True, fechar_u=False):
    """Malha da superfície (u, v) -> F(u, v), com espessura (Solidify) e vidro azul translúcido."""
    bm = bmesh.new()
    verts = [[bm.verts.new(F(u0 + (u1 - u0) * i / nu, v0 + (v1 - v0) * j / nv)) for j in range(nv + 1)] for i in range(nu + 1)]
    for i in range(nu):
        for j in range(nv):
            bm.faces.new((verts[i][j], verts[i + 1][j], verts[i + 1][j + 1], verts[i][j + 1]))
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-5)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    me = bpy.data.meshes.new(nome)
    bm.to_mesh(me)
    bm.free()
    obj = bpy.data.objects.new(nome, me)
    bpy.context.collection.objects.link(obj)
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    sol = obj.modifiers.new("Espessura", "SOLIDIFY")
    sol.thickness = espessura if espessura is not None else co.ST["materiais"]["calculo_vetorial"]["espessura_casca"]
    sol.offset = 0
    bpy.ops.object.shade_smooth_by_angle(angle=math.radians(40))
    if vidro:
        cm.material_vidro(obj)
    return obj


def normal_superficie(F, u, v, h=1e-3):
    P = Vector(F(u, v))
    ru = (Vector(F(u + h, v)) - Vector(F(u - h, v))) / (2 * h)
    rv = (Vector(F(u, v + h)) - Vector(F(u, v - h))) / (2 * h)
    n = ru.cross(rv)
    return P, ru, rv, (n.normalized() if n.length > 1e-9 else Vector((0, 0, 1)))


def linhas_coordenadas(F, u0, u1, v0, v1, n_u=8, n_v=8, amostras=60, elevar=0.012):
    """Polilinhas das curvas u=cte e v=cte sobre a superfície, levemente elevadas pela normal (sem z-fight)."""
    saida = []
    for i in range(n_u + 1):
        u = u0 + (u1 - u0) * i / n_u
        saida.append(([tuple(Vector(F(u, v0 + (v1 - v0) * k / amostras)) + elevar * normal_superficie(F, u, v0 + (v1 - v0) * k / amostras)[3])
                       for k in range(amostras + 1)], False))
    for j in range(n_v + 1):
        v = v0 + (v1 - v0) * j / n_v
        saida.append(([tuple(Vector(F(u0 + (u1 - u0) * k / amostras, v)) + elevar * normal_superficie(F, u0 + (u1 - u0) * k / amostras, v)[3])
                       for k in range(amostras + 1)], False))
    return saida


def remover(objetos):
    """Remove objetos dinâmicos e seus dados, exceto a malha compartilhada das setas."""
    for o in list(objetos):
        d = o.data
        bpy.data.objects.remove(o, do_unlink=True)
        if d is not None and d.users == 0 and not d.get("compartilhada"):
            (bpy.data.meshes if isinstance(d, bpy.types.Mesh) else bpy.data.curves).remove(d)
    objetos.clear()

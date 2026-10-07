"""Órbita kepleriana e poço gravitacional (Gravitação 4.13) — estudo 14 (sandbox).

Rodar: blender.exe -b -P experimentos/blender/gravitacao.py   (gera out/gravitacao_v1.png)

Órbita: o corpo central (neutro, branco) está num foco (origem); o corpo orbitante é azul-claro; a trajetória é a
construção violeta tracejada; o vetor posição é azul-claro; os SETORES são fatias violeta translúcidas varridas em
intervalos de tempo IGUAIS (2ª lei de Kepler: áreas iguais). fase de 0 a 1 = um período (fase=1 repete a fase 0).
Poço: superfície de vidro z = -Φ(r) com uma bola em órbita circular sobre ela (analogia, não a física de fato).
"""

import math
import sys
from pathlib import Path

import bpy

sys.path.insert(0, str(Path(__file__).resolve().parent))
import casca_oca as co  # noqa: E402
import cilindro_macico as cm  # noqa: E402
import revolucao as rv  # noqa: E402
import vetores3d as v3  # noqa: E402

G = co.ST["materiais"]["gravitacao"]
VIOLETA = {"X": (1, 0, 0), "Y": (0, 1, 0), "Z": (0, 0, 1)}


def _kepler(M, e):
    E = M if e < 0.8 else math.pi
    for _ in range(40):
        E -= (E - e * math.sin(E) - M) / (1 - e * math.cos(E))
    return E


def _posicao(a, e, M):
    E = _kepler(M, e)
    return (a * (math.cos(E) - e), a * math.sqrt(1 - e * e) * math.sin(E), 0.0)


def _esfera(nome, raio, mat, pos=(0, 0, 0)):
    import bpy as _b
    _b.ops.mesh.primitive_uv_sphere_add(radius=raio, segments=48, ring_count=24, location=pos)
    o = _b.context.active_object
    o.name = nome
    _b.ops.object.shade_smooth()
    o.data.materials.append(mat)
    return o


def criar_orbita(semi_eixo=2.6, excentricidade=0.55, setores=2, fracao_setor=0.125, raio_centro=0.42, raio_corpo=0.17,
                 vetor=1, fase=0.0):
    """Órbita elíptica com o foco na origem. Devolve (proxy, atualizar(fase))."""
    a, e = semi_eixo, excentricidade
    mat_c = v3.material_degrade("Centro", G["centro_cor"], G["centro_borda"], G["centro_emissao"], G["centro_blend"])
    mat_o = v3.material_cor("CorpoOrbita", G["corpo_cor"], G["corpo_emissao"])
    mat_v = v3.material_cor("VetorPosicao", G["vetor_cor"], G["vetor_emissao"])
    mat_t = co._material("TracoOrbita", {"cor": "gaussiana", "emissao": 1.8, "rugosidade": 0.4})
    _esfera("Centro", raio_centro, mat_c)
    corpo = _esfera("Corpo", raio_corpo, mat_o)

    pts = [_posicao(a, e, 2 * math.pi * k / 240) for k in range(240)]
    v3.curva("Orbita", v3.tracejado(pts, True, 0.34, 0.6), mat_t, G["orbita_espessura"])
    # eixo maior e foco vazio: referências da elipse (neutro, fino)
    # setores
    setor_objs = []
    for _ in range(int(setores)):
        me = bpy.data.meshes.new("Setor")
        o = bpy.data.objects.new("Setor", me)
        bpy.context.collection.objects.link(o)
        cm.material_vidro(o, cor="gaussiana", base=G["setor_base"], ganho=G["setor_ganho"], brilho_borda=G["setor_brilho"])
        setor_objs.append((o, me))
    vet_curva = None
    if vetor:
        cv = bpy.data.curves.new("VetorPosicao", "CURVE")
        cv.dimensions = "3D"
        cv.bevel_depth = G["vetor_espessura"]
        sp = cv.splines.new("POLY")
        sp.points.add(1)
        vo = bpy.data.objects.new("VetorPosicao", cv)
        bpy.context.collection.objects.link(vo)
        vo.data.materials.append(mat_v)
        vet_curva = sp

    bpy.ops.mesh.primitive_cube_add(size=1)
    proxy = bpy.context.active_object
    proxy.name = "ProxyEnquadramento"
    proxy.scale = (2 * a * 1.15, 2 * a * math.sqrt(1 - e * e) * 1.3, 0.3)
    proxy.location = (-a * e, 0, 0)
    bpy.ops.object.transform_apply(scale=True)
    proxy.hide_render = True

    def atualizar(fase):
        M = 2 * math.pi * fase
        corpo.location = _posicao(a, e, M)
        if vet_curva is not None:
            vet_curva.points[0].co = (0, 0, 0.0, 1)
            p = corpo.location
            vet_curva.points[1].co = (p[0], p[1], 0.0, 1)
        for k, (o, me) in enumerate(setor_objs):
            M1 = M + k * 2 * math.pi / max(1, len(setor_objs))
            ms = [M1 - 2 * math.pi * fracao_setor * i / 24 for i in range(25)]
            borda = [_posicao(a, e, m) for m in ms]
            verts = [(0.0, 0.0, 0.0)] + borda
            faces = [(0, i + 1, i + 2) for i in range(24)]
            me.clear_geometry()
            me.from_pydata(verts, [], [tuple(reversed(f)) for f in faces])      # sentido horário visto de +Z -> normal +Z
            me.update()
            for pg in me.polygons:
                pg.use_smooth = False

    atualizar(fase)
    return proxy, atualizar


def criar_poco(raio_max=3.2, profundidade=1.8, raio_nucleo=0.9, bola=1, raio_bola=1.9, fase=0.0, n_aneis=7, n_raios=12):
    """Poço de potencial: z(r) = -profundidade * s / sqrt(r² + s²). Devolve (corpo, atualizar(fase))."""
    R, P, s = raio_max, profundidade, raio_nucleo
    z = lambda r: -P * s / math.sqrt(r * r + s * s) * (R / (R + 0.0)) + P * s / math.sqrt(R * R + s * s)
    NP = 70
    rs = [R * (i / NP) ** 1.5 for i in range(NP + 1)]
    cima = [(z(r), r) for r in reversed(rs)]
    baixo = [(z(r) - 0.05, r) for r in rs]
    corpo = rv.malha_revolucao("Poco", cima + baixo, "Z")
    cm.material_vidro(corpo)
    mat_g = v3.material_cor("GradePoco", G["grade_cor"], G["grade_emissao"])
    for k in range(1, int(n_aneis) + 1):
        r = R * k / n_aneis
        v3.curva("AnelPoco", [([(r * math.cos(2 * math.pi * j / 128), r * math.sin(2 * math.pi * j / 128), z(r) + 0.012) for j in range(129)], False)],
                 mat_g, G["grade_espessura"])
    for k in range(int(n_raios)):
        th = 2 * math.pi * k / n_raios
        v3.curva("RaioPoco", [([(r * math.cos(th), r * math.sin(th), z(r) + 0.012) for r in rs], False)], mat_g, G["grade_espessura"])
    mat_b = v3.material_cor("BolaPoco", G["corpo_cor"], G["corpo_emissao"])
    esf = _esfera("Bola", 0.17, mat_b) if bola else None

    def atualizar(fase):
        if esf is not None:
            th = 2 * math.pi * fase
            esf.location = (raio_bola * math.cos(th), raio_bola * math.sin(th), z(raio_bola) + 0.17 + 0.03)

    atualizar(fase)
    return corpo, atualizar


def cena_preview():
    co.limpar_cena()
    proxy, _ = criar_orbita(fase=0.08)
    co.mundo()
    co.luzes()
    co.camera_enquadrada(co.cantos([proxy]), azimute=-30, elevacao=34, margem=0.08)
    co.render(co.OUT / "gravitacao_v1.png")


if __name__ == "__main__":
    cena_preview()

"""Matemática em 3D (Cálculo III, Física moderna) — estudo 19 (sandbox).

Produto vetorial, plano tangente, quádricas, pontos críticos, soma de Riemann dupla (colunas), elemento de volume
(cartesiano, cilíndrico, esférico) e cone de luz. Gramática do arsenal: corpos e superfícies = vidro azul; curvas de
nível e coordenadas = azul-claro; construções (paralelogramo, plano tangente, elemento dV) = violeta translúcido com
arestas tracejadas; vetores = branco; normal = azul. fase de 0 a 1 = um ciclo (loop) ou, nos de ciclo único, do começo ao fim.
"""

import math
import sys
from pathlib import Path

import bmesh
import bpy
from mathutils import Vector

sys.path.insert(0, str(Path(__file__).resolve().parent))
import calc_vetorial as cv  # noqa: E402
import casca_oca as co  # noqa: E402
import cilindro_macico as cm  # noqa: E402
import gaussiana as ga  # noqa: E402
import vetores3d as v3  # noqa: E402

CVm = co.ST["materiais"]["calculo_vetorial"]


def _mat_vf():
    return v3.material_cor("VetorFisico", "vetor_fisico", co.ST["materiais"]["vetor_fisico"]["emissao"])


def _mat_dash():
    return co._material("TracoM3D", {"cor": "gaussiana", "emissao": 1.8, "rugosidade": 0.4})


def _mat_eixo():
    return v3.material_cor("EixoM3D", "texto_neutro", 0.8)


def _caixa(escala, local, nome="ProxyEnquadramento"):
    bpy.ops.mesh.primitive_cube_add(size=1, location=local)
    o = bpy.context.active_object
    o.name = nome
    o.scale = escala
    bpy.ops.object.transform_apply(scale=True)
    o.hide_render = True
    return o


def eixos(L=3.0, neg=True, nomes=("X", "Y", "Z")):
    """Eixos coordenados tracejados em branco neutro (construção de referência)."""
    mat = _mat_eixo()
    for d in ((1, 0, 0), (0, 1, 0), (0, 0, 1)):
        a = tuple(-L * c if neg else 0 for c in d)
        b = tuple(L * c for c in d)
        ga.criar_curva("Eixo", v3.tracejado([a, b], False, 0.22, 0.6), mat, 0.01)


def _tracejado_poligono(pts, fechado=True, periodo=0.2):
    return ga.criar_curva("Aresta", v3.tracejado(pts, fechado, periodo, 0.6), _mat_dash(), 0.014)


def produto_vetorial(a=2.2, b=1.8, angulo_graus=70.0, paralelogramo=1, movimento=0, fase=0.0, escala_axb=0.7):
    """Vetores a (ao longo de X) e b (no plano XY), o paralelogramo (violeta) e a × b (azul, ao longo de +Z).
    Com movimento, o ângulo entre a e b oscila entre 25° e 155°: o módulo de a × b é a área do paralelogramo."""
    mat_v, mat_n = _mat_vf(), cv._mat_normal()
    eixos(2.2, True)
    dinam = []

    def montar(th):
        v3.remover(dinam)
        va = Vector((a, 0, 0))
        vb = Vector((b * math.cos(th), b * math.sin(th), 0))
        n = va.cross(vb)
        dinam.append(v3.seta((0, 0, 0), va, mat_v))
        dinam.append(v3.seta((0, 0, 0), vb, mat_v))
        if n.length > 1e-3:
            dinam.append(v3.seta((0, 0, 0), n.normalized() * max(0.15, n.length * escala_axb), mat_n))
        if paralelogramo:
            c = [(0, 0, 0.01), tuple(va + Vector((0, 0, 0.01))), tuple(va + vb + Vector((0, 0, 0.01))), tuple(vb + Vector((0, 0, 0.01)))]
            dinam.append(v3.quad_translucido(c))
            dinam.append(_tracejado_poligono(c))

    def atualizar(fase):
        montar(math.radians(90 + 65 * math.sin(2 * math.pi * fase)) if movimento else math.radians(angulo_graus))

    atualizar(fase)
    proxy = _caixa((5.6, 4.0, 3.2), (0.7, 0.9, 1.0))
    return proxy, atualizar


def plano_tangente(tipo="sela", u0=0.4, v0=0.55, tamanho=1.1, movimento=0, fase=0.0, linhas=1):
    """Superfície (onda, sela ou esfera), ponto P, plano tangente (violeta, arestas tracejadas) e normal n̂ (azul)."""
    F, ua, ub, va, vb = cv.SUPERFICIES[tipo]
    corpo = v3.malha_param("Superficie", F, ua, ub, va, vb, 56, 56)
    if linhas:
        v3.curva("Coord", v3.linhas_coordenadas(F, ua, ub, va, vb, 9, 9), cv._mat_curva(), cv.CV["curva_espessura"])
    mat_n, mat_p = cv._mat_normal(), _mat_vf()
    dinam = []

    def montar(fu, fv):
        v3.remover(dinam)
        u, v = ua + (ub - ua) * fu, va + (vb - va) * fv
        P, ru, rv, n = v3.normal_superficie(F, u, v)
        e1, e2 = ru.normalized() * tamanho, rv.normalized() * tamanho
        c = [tuple(P - e1 - e2), tuple(P + e1 - e2), tuple(P + e1 + e2), tuple(P - e1 + e2)]
        dinam.append(v3.quad_translucido(c))
        dinam.append(_tracejado_poligono(c))
        dinam.append(v3.esfera_pt(tuple(P), 0.07, _mat_vf(), "PontoP"))
        dinam.append(v3.seta(tuple(P), n * 1.0, mat_n, 1.0))

    def atualizar(fase):
        if movimento:
            a = 2 * math.pi * fase
            montar(u0 + 0.22 * math.cos(a), v0 + 0.22 * math.sin(a))
        else:
            montar(u0, v0)

    atualizar(fase)
    return corpo, atualizar


def _quadricas(tipo, a, b, c):
    TAU = 2 * math.pi
    if tipo == "elipsoide":
        return [(lambda u, v: (a * math.sin(v) * math.cos(u), b * math.sin(v) * math.sin(u), c * math.cos(v)), 0, TAU, 0.04 * math.pi, 0.96 * math.pi)]
    if tipo == "hiperboloide_uma_folha":
        return [(lambda u, v: (a * math.cosh(v) * math.cos(u), b * math.cosh(v) * math.sin(u), c * math.sinh(v)), 0, TAU, -1.1, 1.1)]
    if tipo == "hiperboloide_duas_folhas":
        return [(lambda u, v, s=s: (a * math.sinh(v) * math.cos(u), b * math.sinh(v) * math.sin(u), s * c * math.cosh(v)), 0, TAU, 0.02, 1.0) for s in (1, -1)]
    if tipo == "paraboloide_eliptico":
        return [(lambda u, v: (a * v * math.cos(u), b * v * math.sin(u), c * v * v), 0, TAU, 0.0, 1.3)]
    if tipo == "paraboloide_hiperbolico":
        return [(lambda u, v: (u, v, c * (u * u / (a * a) - v * v / (b * b))), -2.0, 2.0, -2.0, 2.0)]
    if tipo == "cone":
        return [(lambda u, v: (a * v * math.cos(u), b * v * math.sin(u), c * v), 0, TAU, -1.2, 1.2)]
    raise ValueError(f"quádrica desconhecida: {tipo}")


def superficie_quadrica(tipo="elipsoide", a=2.0, b=1.5, c=1.3, eixo=1, linhas=1):
    """Quádrica de vidro azul com curvas coordenadas e eixos coordenados tracejados."""
    partes = _quadricas(tipo, a, b, c)
    corpos = []
    for (F, ua, ub, va, vb) in partes:
        corpos.append(v3.malha_param("Quadrica", F, ua, ub, va, vb, 64, 48))
        if linhas:
            v3.curva("Coord", v3.linhas_coordenadas(F, ua, ub, va, vb, 14, 8, 50, 0.015), cv._mat_curva(), cv.CV["curva_espessura"])
    if eixo:
        eixos(3.0, True)
    proxy = _caixa((2 * 2.6, 2 * 2.6, 2 * 2.2), (0, 0, 0))
    return proxy


def pontos_criticos(altura=0.7, k=1.1, extensao=2.9, planos=1):
    """Superfície z = h sen(kx) sen(ky) com um máximo, um mínimo e uma sela; plano tangente horizontal violeta em cada."""
    f = lambda x, y: altura * math.sin(k * x) * math.sin(k * y)
    F = lambda u, v: (u, v, f(u, v))
    corpo = v3.malha_param("Superficie", F, -extensao, extensao, -extensao, extensao, 80, 80)
    v3.curva("Nivel", v3.linhas_coordenadas(F, -extensao, extensao, -extensao, extensao, 12, 12, 70, 0.015), cv._mat_curva(), cv.CV["curva_espessura"])
    q = math.pi / (2 * k)
    mat_p = _mat_vf()
    for (x, y) in ((q, q), (q, -q), (0.0, 0.0)):
        z = f(x, y)
        v3.esfera_pt((x, y, z + 0.03), 0.09, mat_p, "PontoCritico")
        if planos:
            s = 0.75
            c = [(x - s, y - s, z), (x + s, y - s, z), (x + s, y + s, z), (x - s, y + s, z)]
            v3.quad_translucido(c)
            _tracejado_poligono(c)
    return corpo


def soma_riemann_dupla(extensao=2.0, n_max=16, n_unico=0, fase=0.0, movimento=0):
    """Colunas de altura f(centro) sobre a grade n×n do quadrado [−E, E]²; a superfície z = f em azul-claro por cima.
    Com movimento (ciclo único), n cresce de 2 até n_max: a soma de Riemann converge ao volume."""
    E = extensao
    f = lambda x, y: 1.2 + 0.7 * math.sin(1.3 * x) * math.cos(1.1 * y)
    F = lambda u, v: (u, v, f(u, v))
    sup = v3.malha_param("Superficie", F, -E, E, -E, E, 48, 48, espessura=0.02)
    cm.material_vidro(sup, base=0.04, ganho=0.2, brilho_borda=0.8)
    v3.curva("Nivel", v3.linhas_coordenadas(F, -E, E, -E, E, 10, 10, 50, 0.02), cv._mat_curva(), cv.CV["curva_espessura"])
    c = [(-E, -E, 0.0), (E, -E, 0.0), (E, E, 0.0), (-E, E, 0.0)]
    _tracejado_poligono(c, True, 0.3)
    me = bpy.data.meshes.new("Colunas")
    col = bpy.data.objects.new("Colunas", me)
    bpy.context.collection.objects.link(col)
    bpy.context.view_layer.objects.active = col
    col.select_set(True)
    cm.material_vidro(col)
    grade = bpy.data.objects.new("ColunasMalha", me)
    bpy.context.collection.objects.link(grade)
    wf = grade.modifiers.new("Malha", "WIREFRAME")
    wf.thickness = 0.014
    wf.use_replace = True
    grade.data.materials.append(v3.material_cor("MalhaColunas", "fonte_contorno", 0.9))
    niveis = [2, 3, 4, 6, 8, 12, 16]
    niveis = [n for n in niveis if n <= n_max]

    def montar(n):
        d = 2 * E / n
        verts, faces = [], []
        for i in range(n):
            for j in range(n):
                x0, y0 = -E + i * d, -E + j * d
                h = f(x0 + d / 2, y0 + d / 2)
                b0 = len(verts)
                verts += [(x0, y0, 0), (x0 + d, y0, 0), (x0 + d, y0 + d, 0), (x0, y0 + d, 0),
                          (x0, y0, h), (x0 + d, y0, h), (x0 + d, y0 + d, h), (x0, y0 + d, h)]
                faces += [(b0 + 4, b0 + 5, b0 + 6, b0 + 7), (b0, b0 + 1, b0 + 5, b0 + 4), (b0 + 1, b0 + 2, b0 + 6, b0 + 5),
                          (b0 + 2, b0 + 3, b0 + 7, b0 + 6), (b0 + 3, b0, b0 + 4, b0 + 7)]
        me.clear_geometry()
        me.from_pydata(verts, [], faces)
        me.update()
        for p in me.polygons:
            p.use_smooth = False

    def atualizar(fase):
        i = int(round(min(max(fase, 0.0), 1.0) * (len(niveis) - 1))) if movimento else len(niveis) - 1
        montar(n_unico or niveis[i])

    atualizar(fase)
    proxy = _caixa((2 * E + 0.4, 2 * E + 0.4, 2.4), (0, 0, 0.9))
    return proxy, atualizar


def _grade_face(bm, F, ua, ub, va, vb, n=10):
    vs = [[bm.verts.new(F(ua + (ub - ua) * i / n, va + (vb - va) * j / n)) for j in range(n + 1)] for i in range(n + 1)]
    for i in range(n):
        for j in range(n):
            bm.faces.new((vs[i][j], vs[i + 1][j], vs[i + 1][j + 1], vs[i][j + 1]))


def _elemento(F, r0, r1, r2):
    """Sólido curvilíneo F(u, v, w) em [u0,u1]×[v0,v1]×[w0,w1]: malha fechada + 12 arestas tracejadas. Devolve [objetos]."""
    (u0, u1), (v0, v1), (w0, w1) = r0, r1, r2
    bm = bmesh.new()
    for u in (u0, u1):
        _grade_face(bm, lambda a, b, u=u: F(u, a, b), v0, v1, w0, w1)
    for v in (v0, v1):
        _grade_face(bm, lambda a, b, v=v: F(a, v, b), u0, u1, w0, w1)
    for w in (w0, w1):
        _grade_face(bm, lambda a, b, w=w: F(a, b, w), u0, u1, v0, v1)
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-5)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    me = bpy.data.meshes.new("Elemento")
    bm.to_mesh(me)
    bm.free()
    o = bpy.data.objects.new("Elemento", me)
    bpy.context.collection.objects.link(o)
    bpy.context.view_layer.objects.active = o
    o.select_set(True)
    bpy.ops.object.shade_smooth_by_angle(angle=math.radians(35))
    cm.material_vidro(o, cor="gaussiana", base=CVm["remendo_base"], ganho=CVm["remendo_ganho"], brilho_borda=CVm["remendo_brilho"])
    objs = [o]
    N = 24
    for (vi, wi) in ((v0, w0), (v0, w1), (v1, w0), (v1, w1)):
        objs.append(_tracejado_poligono([F(u0 + (u1 - u0) * k / N, vi, wi) for k in range(N + 1)], False, 0.16))
    for (ui, wi) in ((u0, w0), (u0, w1), (u1, w0), (u1, w1)):
        objs.append(_tracejado_poligono([F(ui, v0 + (v1 - v0) * k / N, wi) for k in range(N + 1)], False, 0.16))
    for (ui, vi) in ((u0, v0), (u0, v1), (u1, v0), (u1, v1)):
        objs.append(_tracejado_poligono([F(ui, vi, w0 + (w1 - w0) * k / N) for k in range(N + 1)], False, 0.16))
    return objs


def elemento_volume(sistema="cilindrico", movimento=0, fase=0.0, guias=1):
    """Elemento de volume dV: caixa dx dy dz (cartesiano), r dr dθ dz (cilíndrico) ou r² sen θ dr dθ dφ (esférico),
    em violeta com arestas tracejadas, mais os eixos e as guias (raio e projeções). Com movimento o elemento dá uma
    volta em torno do eixo z."""
    eixos(2.4, True)
    dinam = []

    def montar(rot):
        v3.remover(dinam)
        if sistema == "cartesiano":
            R = 1.7
            cx, cy = R * math.cos(0.7 + rot), R * math.sin(0.7 + rot)
            F = lambda u, v, w: (u, v, w)
            dinam.extend(_elemento(F, (cx - 0.4, cx + 0.4), (cy - 0.4, cy + 0.4), (0.7, 1.5)))
            alvo = (cx, cy, 1.1)
        elif sistema == "cilindrico":
            F = lambda r, t, z: (r * math.cos(t), r * math.sin(t), z)
            t0 = 0.6 + rot
            dinam.extend(_elemento(F, (1.5, 2.3), (t0, t0 + 0.6), (0.6, 1.5)))
            alvo = F(1.9, t0 + 0.3, 1.05)
        elif sistema == "esferico":
            F = lambda r, th, ph: (r * math.sin(th) * math.cos(ph), r * math.sin(th) * math.sin(ph), r * math.cos(th))
            p0 = 0.6 + rot
            dinam.extend(_elemento(F, (1.8, 2.6), (0.8, 1.35), (p0, p0 + 0.6)))
            alvo = F(2.2, 1.07, p0 + 0.3)
        else:
            raise ValueError(f"sistema desconhecido: {sistema}")
        if guias:
            dinam.append(v3.curva("Raio", v3.tracejado([(0, 0, 0), alvo], False, 0.18, 0.6), v3.material_cor("GuiaEV", "texto_neutro", 0.9), 0.012))
            dinam.append(v3.curva("Proj", v3.tracejado([alvo, (alvo[0], alvo[1], 0.0)], False, 0.14, 0.6), v3.material_cor("GuiaEV", "texto_neutro", 0.9), 0.012))

    def atualizar(fase):
        montar(2 * math.pi * fase if movimento else 0.0)

    atualizar(fase)
    proxy = _caixa((5.2, 5.2, 3.2), (0.5, 0.5, 0.9))
    return proxy, atualizar


def cone_de_luz(raio_max=2.6, altura_plano=0.0, movimento=0, fase=0.0, linhas=1):
    """Cone de luz no espaço-tempo (x, y, ct): cones do futuro e do passado (vidro azul), eixo ct, uma linha de universo
    (curva azul-claro) dentro do cone e um evento (branco) subindo por ela. O plano de simultaneidade (violeta) passa
    pelo evento e corta o cone num círculo azul-claro: a frente de luz. Com movimento (ciclo único), o evento sobe."""
    R = raio_max
    for s in (1, -1):
        F = lambda u, v, s=s: (v * math.cos(u), v * math.sin(u), s * v)
        v3.malha_param("Cone", F, 0.0, 2 * math.pi, 0.02, R, 64, 24)
        if linhas:
            v3.curva("CoordCone", v3.linhas_coordenadas(F, 0.0, 2 * math.pi, 0.02, R, 16, 5, 40, 0.012), cv._mat_curva(), cv.CV["curva_espessura"])
    mat_eixo = _mat_eixo()
    ga.criar_curva("EixoCT", v3.tracejado([(0, 0, -R - 0.3), (0, 0, R + 0.4)], False, 0.22, 0.6), mat_eixo, 0.012)
    zs = [(-2.3 + 4.6 * i / 80) for i in range(81)]
    wl = lambda z: (0.9 * math.sin(0.7 * z), 0.45 * (1 - math.cos(0.7 * z)), z)
    v3.curva("LinhaDeUniverso", [([wl(z) for z in zs], False)], v3.material_cor("LinhaUniv", "fonte_contorno", 1.4), 0.03)
    ev = v3.esfera_pt(wl(-2.3), 0.12, _mat_vf(), "Evento")
    dinam = []

    def montar(z):
        v3.remover(dinam)
        r = max(abs(z), 0.03)
        circ = [(r * math.cos(2 * math.pi * k / 96), r * math.sin(2 * math.pi * k / 96), z) for k in range(97)]
        dinam.append(v3.curva("FrenteDeLuz", [(circ, False)], v3.material_cor("FrenteLuz", "fonte_contorno", 1.6), 0.035))
        disco = [(R * 1.05 * math.cos(2 * math.pi * k / 48), R * 1.05 * math.sin(2 * math.pi * k / 48), z) for k in range(48)]
        dinam.append(v3.quad_translucido(disco, base=0.14))
        dinam.append(_tracejado_poligono(disco, True, 0.3))
        ev.location = wl(z)

    def atualizar(fase):
        montar(-2.3 + 4.6 * min(max(fase, 0.0), 1.0) if movimento else altura_plano)

    atualizar(fase)
    proxy = _caixa((2 * R + 0.6, 2 * R + 0.6, 2 * R + 0.8), (0, 0, 0))
    return proxy, atualizar


def cena_preview():
    co.limpar_cena()
    proxy, _ = produto_vetorial()
    co.mundo()
    co.luzes()
    co.camera_enquadrada(co.cantos([proxy]), azimute=-40, elevacao=26, margem=0.08)
    co.render(co.OUT / "matematica3d_v1.png")


if __name__ == "__main__":
    cena_preview()

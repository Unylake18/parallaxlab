"""Mecânica, fila B (4.4 a 4.12) — estudo 22 (sandbox).

Plano inclinado, movimento circular, curva inclinada, colisão em 2D, explosão, corpos rolando numa rampa e looping.
Gramática do arsenal: corpos = vidro azul / esferas com degradê; vetores físicos (peso, normal, atrito, v, a) = BRANCO;
construções (componentes, trajetórias, linha de energia) = violeta tracejado. fase 0 a 1 = um ciclo (loop) ou, nos de
ciclo único, do começo ao fim. Valores, fórmulas e os nomes dos vetores são do Manim.
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
import oscilacoes as osc  # noqa: E402
import vetores3d as v3  # noqa: E402

VF = co.ST["materiais"]["vetor_fisico"]


def _mat_vf():
    return v3.material_cor("VetorFisico", VF["cor"], VF["emissao"])


def _mat_dash():
    return co._material("TracoMecB", {"cor": "gaussiana", "emissao": 1.8, "rugosidade": 0.4})


def _caixa(escala, local, nome="ProxyEnquadramento"):
    return _proxy(osc._caixa(nome, escala, local))


def _proxy(o):
    o.hide_render = True
    return o


def _alinhar(obj, ex, ey, ez):
    """Orienta `obj` de modo que seus eixos locais X, Y, Z apontem para ex, ey, ez (vetores ortonormais)."""
    obj.rotation_mode = "XYZ"
    obj.rotation_euler = Matrix((Vector(ex), Vector(ey), Vector(ez))).transposed().to_euler()


def _extrusao_xz(perfil, w, nome="Solido"):
    """Sólido de vidro: polígono do perfil (pares (x, z)) extrudado de y = −w a y = +w."""
    bm = bmesh.new()
    a = [bm.verts.new((x, -w, z)) for x, z in perfil]
    b = [bm.verts.new((x, w, z)) for x, z in perfil]
    n = len(perfil)
    bm.faces.new(a)
    bm.faces.new(list(reversed(b)))
    for i in range(n):
        bm.faces.new((a[i], a[(i + 1) % n], b[(i + 1) % n], b[i]))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    me = bpy.data.meshes.new(nome)
    bm.to_mesh(me)
    bm.free()
    o = bpy.data.objects.new(nome, me)
    bpy.context.collection.objects.link(o)
    bpy.context.view_layer.objects.active = o
    o.select_set(True)
    cm.material_vidro(o)
    return o


def _vidro_estrutura(o):
    cm.material_vidro(o, base=0.2, ganho=0.5, brilho_borda=1.2)


# ── plano inclinado ──────────────────────────────────────────────────────────
def plano_inclinado(angulo_graus=28.0, comprimento=5.2, mu=0.25, lado=0.8, forcas=1, movimento=0, posicao=0.6, fase=0.0, largura=1.8):
    """Bloco de vidro numa rampa de vidro (cunha). Peso, normal e atrito (brancos) e as componentes do peso (violeta tracejado).
    Se tan θ > μ o bloco desce com aceleração constante (ciclo único); senão fica parado e o atrito é estático (f = P sen θ)."""
    th = math.radians(angulo_graus)
    u, n = Vector((math.cos(th), 0, math.sin(th))), Vector((-math.sin(th), 0, math.cos(th)))
    L, w = comprimento, largura / 2
    _extrusao_xz([(0, 0), (L * math.cos(th), 0), (L * math.cos(th), L * math.sin(th))], w, "Rampa")
    mat_vf, mat_d = _mat_vf(), _mat_dash()
    bloco = osc._caixa("Bloco", (lado, lado * 0.9, lado), (0, 0, 0))
    cm.material_vidro(bloco, cor="fonte_contorno", base=0.4, ganho=0.6, brilho_borda=2.0)
    arco = [(0.9 * math.cos(th * k / 24), 0, 0.9 * math.sin(th * k / 24)) for k in range(25)]
    ga.criar_curva("AnguloTheta", v3.tracejado(arco, False, 0.1, 0.6), mat_d, 0.012)
    desliza = math.tan(th) > mu
    s_top, s_bot = L - 0.9 * lado, 0.75 * lado
    dinam = []

    def montar(s):
        centro = u * s + n * (lado / 2)
        bloco.location = centro
        _alinhar(bloco, tuple(u), (0, 1, 0), tuple(n))
        v3.remover(dinam)
        if not forcas:
            return
        P = 1.7
        dinam.append(v3.seta(tuple(centro), (0, 0, -P), mat_vf, P))                                     # peso
        dinam.append(v3.seta(tuple(centro), tuple(n * P * math.cos(th)), mat_vf, P * math.cos(th)))     # normal
        fat = P * (mu * math.cos(th) if desliza else math.sin(th))
        dinam.append(v3.seta(tuple(centro), tuple(u * fat), mat_vf, fat))                               # atrito (sobe a rampa)
        dinam.append(ga.criar_curva("Pparalelo", v3.tracejado([tuple(centro), tuple(centro - u * P * math.sin(th))], False, 0.14, 0.6), mat_d, 0.014))
        dinam.append(ga.criar_curva("Pperp", v3.tracejado([tuple(centro), tuple(centro - n * P * math.cos(th))], False, 0.14, 0.6), mat_d, 0.014))

    def atualizar(fase):
        f = min(max(fase, 0.0), 1.0)
        s = (s_top - (s_top - s_bot) * f * f) if (movimento and desliza) else (s_top * posicao + s_bot * (1 - posicao) if not movimento else s_top)
        montar(s)

    atualizar(fase)
    proxy = _caixa((L * math.cos(th) + 1.4, largura + 0.8, L * math.sin(th) + 1.6), (L * math.cos(th) / 2, 0, L * math.sin(th) / 2 + 0.5))
    return proxy, atualizar


# ── movimento circular uniforme ──────────────────────────────────────────────
def movimento_circular(raio=1.8, vetores=1, trajetoria=1, raio_bola=0.22, fase=0.0):
    """Bola numa mesa de vidro presa por um fio a um poste central: v (tangente) e a_c (para o centro), brancos.
    fase 0 a 1 = uma volta."""
    R = raio
    mesa = osc._caixa("Mesa", (2 * R + 1.6, 2 * R + 1.6, 0.06), (0, 0, -0.03))
    bpy.ops.mesh.primitive_cylinder_add(radius=R + 0.9, depth=0.06, vertices=96, location=(0, 0, -0.03))
    disco = bpy.context.active_object
    disco.name = "MesaRedonda"
    bpy.data.objects.remove(mesa, do_unlink=True)
    _vidro_estrutura(disco)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.1, depth=0.4, vertices=32, location=(0, 0, 0.17))
    poste = bpy.context.active_object
    poste.name = "Poste"
    bpy.ops.object.shade_smooth()
    poste.data.materials.append(co._material("Poste", {"cor": "fonte_contorno", "emissao": 0.9, "rugosidade": 0.35}))
    mat_vf = _mat_vf()
    mat_bola = v3.material_degrade("Bola", "texto_neutro", "fonte_contorno", 1.0, 0.7)
    bola = v3.esfera_pt((R, 0, raio_bola), raio_bola, mat_bola, "Bola")
    _, sp = osc.curva_viva("Fio", 2, v3.material_cor("FioMC", "fonte_contorno", 1.0), 0.02)
    if trajetoria:
        c = [(R * math.cos(2 * math.pi * k / 120), R * math.sin(2 * math.pi * k / 120), 0.01) for k in range(120)]
        ga.criar_curva("Trajetoria", v3.tracejado(c, True, 0.3, 0.6), _mat_dash(), 0.014)
    dinam = []

    def atualizar(fase):
        a = 2 * math.pi * fase
        p = (R * math.cos(a), R * math.sin(a), raio_bola)
        bola.location = p
        osc.pontos_curva(sp, [(0, 0, 0.37), p])
        v3.remover(dinam)
        if vetores:
            t = Vector((-math.sin(a), math.cos(a), 0))
            dinam.append(v3.seta(p, tuple(t * 1.7), mat_vf, 1.7))                                       # v
            dinam.append(v3.seta(p, (-math.cos(a) * 1.1, -math.sin(a) * 1.1, 0.0), mat_vf, 1.1))        # a_c

    atualizar(fase)
    proxy = _caixa((2 * R + 2.6, 2 * R + 2.6, 1.2), (0, 0, 0.3))
    return proxy, atualizar


# ── curva inclinada (pista com inclinação) ───────────────────────────────────
def curva_inclinada(raio=2.6, angulo_graus=22.0, semi_largura=1.0, vetores=1, fase=0.0):
    """Pista circular inclinada para dentro (sem atrito): carro de vidro e as forças peso, normal e resultante
    centrípeta (brancas): N cos θ = P e N sen θ = P tan θ·cos θ. fase 0 a 1 = uma volta."""
    R, th, w = raio, math.radians(angulo_graus), semi_largura
    F = lambda u, v: ((R + v) * math.cos(u), (R + v) * math.sin(u), v * math.tan(th))
    pista = v3.malha_param("Pista", F, 0, 2 * math.pi, -w, w, 96, 6, espessura=0.06)
    v3.curva("Eixo", [([(0, 0, -0.3), (0, 0, 1.4)], False)], v3.material_cor("EixoCI", "texto_neutro", 0.0001), 0.0001)
    mat_vf = _mat_vf()
    carro = osc._caixa("Carro", (0.9, 0.5, 0.35), (R, 0, 0))
    cm.material_vidro(carro, cor="fonte_contorno", base=0.45, ganho=0.6, brilho_borda=2.0)
    dinam = []

    def atualizar(fase):
        a = 2 * math.pi * fase
        rho = Vector((math.cos(a), math.sin(a), 0))
        tang = Vector((-math.sin(a), math.cos(a), 0))
        sl = rho * math.cos(th) + Vector((0, 0, math.sin(th)))
        nrm = -rho * math.sin(th) + Vector((0, 0, math.cos(th)))
        base = rho * R
        centro = base + nrm * 0.18
        carro.location = tuple(centro)
        _alinhar(carro, tuple(tang), tuple(sl), tuple(nrm))
        v3.remover(dinam)
        if vetores:
            P = 1.6
            dinam.append(v3.seta(tuple(centro), (0, 0, -P), mat_vf, P))
            dinam.append(v3.seta(tuple(centro), tuple(nrm * (P / math.cos(th))), mat_vf, P / math.cos(th)))
            dinam.append(v3.seta(tuple(centro), tuple(-rho * (P * math.tan(th))), mat_vf, P * math.tan(th)))

    atualizar(fase)
    proxy = _caixa((2 * (R + w) + 1.4, 2 * (R + w) + 1.4, 2.4), (0, 0, 0.7))
    return pista, atualizar, proxy


# ── colisão em 2D ────────────────────────────────────────────────────────────
def colisao_2d(m1=2.0, m2=1.0, v1=3.0, parametro_impacto=0.55, restituicao=1.0, instante=0.4, mostrar_cm=1, fase=0.0):
    """Dois discos de vidro numa mesa de vidro: o disco 1 (azul) vem em +X e atinge o disco 2 (azul-claro, em repouso) com
    parâmetro de impacto b. Impulso só ao longo da normal do contato. Velocidades em branco, centro de massa neutro, trajetórias
    violeta tracejado. Ciclo único (a fase 1 não repete a fase 0)."""
    r1, r2 = 0.45 * m1 ** (1 / 3), 0.45 * m2 ** (1 / 3)
    b = min(max(parametro_impacto, 0.0), 0.95 * (r1 + r2))
    phi = math.asin(b / (r1 + r2))
    nn = Vector((math.cos(phi), math.sin(phi), 0))
    V1, V2 = Vector((v1, 0, 0)), Vector((0, 0, 0))
    vn = (V1 - V2).dot(nn)
    V1f = V1 - (1 + restituicao) * m2 / (m1 + m2) * vn * nn
    V2f = V2 + (1 + restituicao) * m1 / (m1 + m2) * vn * nn
    p1c, p2c = -r1 * nn, r2 * nn                                   # centros no contato (origem no ponto de contato)

    def pos(t):
        if t <= instante:
            return p1c + V1 * (t - instante), p2c + V2 * (t - instante)
        return p1c + V1f * (t - instante), p2c + V2f * (t - instante)

    ext = [pos(0.0)[0], pos(1.0)[0], pos(1.0)[1], pos(0.0)[1]]
    xs = [p.x for p in ext]
    ys = [p.y for p in ext]
    cx, cy = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2
    lx, ly = max(xs) - min(xs) + 2.2, max(ys) - min(ys) + 2.2
    mesa = osc._caixa("Mesa", (lx, ly, 0.06), (cx, cy, -0.03))
    _vidro_estrutura(mesa)
    mat_vf, mat_cm = _mat_vf(), v3.material_cor("CM2D", "texto_neutro", 2.0)
    discos = []
    for r, cor in ((r1, "fonte_fisica"), (r2, "fonte_contorno")):
        bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=0.3, vertices=64)
        d = bpy.context.active_object
        d.name = "Disco"
        bpy.ops.object.shade_smooth()
        cm.material_vidro(d, cor=cor, base=0.45, ganho=0.6, brilho_borda=2.0)
        discos.append(d)
    cm_obj = v3.esfera_pt((0, 0, 0.5), 0.09, mat_cm, "CentroMassa")
    cm_obj.hide_render = not mostrar_cm
    mat_d = _mat_dash()
    a1, a2 = pos(0.0)[0], pos(instante)[0]
    for (pa, pb) in ((pos(0.0)[0], pos(instante)[0]), (pos(instante)[0], pos(1.0)[0]), (pos(0.0)[1], pos(1.0)[1])):
        ga.criar_curva("Trajetoria", v3.tracejado([(pa.x, pa.y, 0.02), (pb.x, pb.y, 0.02)], False, 0.22, 0.6), mat_d, 0.014)
    dinam = []

    def atualizar(fase):
        t = min(max(fase, 0.0), 1.0)
        p1, p2 = pos(t)
        discos[0].location = (p1.x, p1.y, 0.15)
        discos[1].location = (p2.x, p2.y, 0.15)
        cm_obj.location = (((m1 * p1 + m2 * p2) / (m1 + m2)).x, ((m1 * p1 + m2 * p2) / (m1 + m2)).y, 0.5)
        v3.remover(dinam)
        va, vb = (V1, V2) if t <= instante else (V1f, V2f)
        for p, vv in ((p1, va), (p2, vb)):
            if vv.length > 0.05:
                dinam.append(v3.seta((p.x, p.y, 0.4), tuple(vv * 0.5), mat_vf, vv.length * 0.5))

    atualizar(fase)
    proxy = _caixa((lx, ly, 1.2), (cx, cy, 0.4))
    return proxy, atualizar


# ── explosão ─────────────────────────────────────────────────────────────────
def explosao(massas=(2.0, 1.0, 1.5), energia=14.0, v0=1.0, instante=0.35, fase=0.0):
    """Uma esfera que se parte em três fragmentos em 120°, conservando o momento linear (Σ m v = 0 no referencial do centro de
    massa). Velocidades em branco, centro de massa neutro (anda a velocidade constante v0). Ciclo único."""
    ms = list(massas)
    ang = [math.radians(90 + 120 * k) for k in range(3)]
    dirs = [Vector((math.cos(a), math.sin(a), 0)) for a in ang]
    # velocidades no referencial do CM: Σ m v = 0 com direções fixas em 120°: v_i = c / m_i ao longo de dirs[i] (e a soma dos
    # vetores c·dir_i vale 0): satisfaz Σ m_i v_i = c Σ dir_i = 0
    c = math.sqrt(2 * energia / sum(1 / mi for mi in ms))
    us = [dirs[i] * (c / ms[i]) for i in range(3)]
    V0 = Vector((v0, 0, 0))
    mesa = osc._caixa("Mesa", (6.0, 4.2, 0.06), (0.0, 0.0, -0.03))
    _vidro_estrutura(mesa)
    mat_vf, mat_cm = _mat_vf(), v3.material_cor("CMexp", "texto_neutro", 2.0)
    todo = v3.esfera_pt((0, 0, 0.4), 0.55, v3.material_degrade("Corpo", "fonte_contorno", "fonte_fisica", 0.9, 0.7), "Corpo")
    frags = []
    for k, mi in enumerate(ms):
        r = 0.32 * mi ** (1 / 3)
        frags.append(v3.esfera_pt((0, 0, 0.4), r, v3.material_degrade(f"Frag{k}", "texto_neutro" if k else "fonte_contorno", "fonte_fisica", 0.9, 0.7), f"Fragmento{k}"))
    cm_obj = v3.esfera_pt((0, 0, 0.9), 0.09, mat_cm, "CentroMassa")
    dinam = []

    def atualizar(fase):
        t = min(max(fase, 0.0), 1.0)
        base = V0 * (t - instante)
        cm_obj.location = (base.x, base.y, 0.9)
        v3.remover(dinam)
        if t < instante:
            todo.hide_render = False
            todo.location = (base.x, base.y, 0.4)
            for f in frags:
                f.hide_render = True
            dinam.append(v3.seta((base.x, base.y, 0.8), tuple(V0 * 0.5), mat_vf, V0.length * 0.5))
        else:
            todo.hide_render = True
            for f, uu in zip(frags, us):
                f.hide_render = False
                p = base + uu * (t - instante)
                f.location = (p.x, p.y, 0.4)
                vv = V0 + uu
                dinam.append(v3.seta((p.x, p.y, 0.8), tuple(vv * 0.5), mat_vf, vv.length * 0.5))

    atualizar(fase)
    proxy = _caixa((6.0, 4.2, 1.4), (0, 0, 0.4))
    return proxy, atualizar


# ── corpos rolando numa rampa (corrida) ──────────────────────────────────────
def _corpo_rolante(tipo, raio):
    """Corpo rolante simples (vidro azul + riscos azul-claro + marca branca) como filho de um empty; eixo de rolamento = Y."""
    base = bpy.data.objects.new("Corpo", None)
    bpy.context.collection.objects.link(base)
    mat_r = v3.material_cor("RiscoRamp", "fonte_contorno", 1.2)
    mat_m = v3.material_cor("MarcaRamp", "texto_neutro", 2.0)

    def filho(o):
        o.parent = base
        return o

    if tipo == "esfera":
        bpy.ops.mesh.primitive_uv_sphere_add(segments=64, ring_count=32, radius=raio)
        v = bpy.context.active_object
        bpy.ops.object.shade_smooth()
        cm.material_vidro(v)
        filho(v)
        for k in range(3):
            f = math.radians(60 * k)
            filho(ga.criar_curva("Meridiano", ga.circulo((0, 0, 0), (0, 1, 0), (math.cos(f), 0, math.sin(f)), raio * 1.003, True), mat_r, 0.014))
        filho(ga.criar_curva("Equador", ga.circulo((0, 0, 0), (1, 0, 0), (0, 0, 1), raio * 1.003, True), mat_r, 0.014))
        filho(v3.esfera_pt((0, 0, raio * 1.003), 0.06, mat_m, "Marca"))
        larg = 2 * raio
    elif tipo == "cilindro":
        larg = 1.1
        v = cm.criar_corpo_macico(raio, larg, 64)
        v.rotation_euler = (0, 0, math.radians(90))
        bpy.context.view_layer.objects.active = v
        v.select_set(True)
        bpy.ops.object.transform_apply(rotation=True)
        cm.material_vidro(v)
        filho(v)
        for s in (-1, 1):
            filho(ga.criar_curva("Borda", ga.circulo((0, s * larg / 2, 0), (1, 0, 0), (0, 0, 1), raio * 1.003, True), mat_r, 0.014))
        for k in range(4):
            a = math.radians(90 * k)
            filho(ga.criar_curva("Geratriz", [([(raio * 1.003 * math.cos(a), -larg / 2, raio * 1.003 * math.sin(a)), (raio * 1.003 * math.cos(a), larg / 2, raio * 1.003 * math.sin(a))], True)], mat_r, 0.014))
        filho(v3.esfera_pt((0, larg / 2, raio * 1.003), 0.06, mat_m, "Marca"))
    else:
        bpy.ops.mesh.primitive_torus_add(major_radius=raio, minor_radius=0.06, major_segments=96, minor_segments=20)
        v = bpy.context.active_object
        v.rotation_euler = (math.radians(90), 0, 0)
        bpy.context.view_layer.objects.active = v
        v.select_set(True)
        bpy.ops.object.transform_apply(rotation=True)
        bpy.ops.object.shade_smooth()
        cm.material_vidro(v, base=0.3, ganho=0.6, brilho_borda=2.2)
        filho(v)
        for k in range(3):
            a = math.radians(120 * k)
            filho(v3.esfera_pt((raio * math.sin(a), 0, raio * math.cos(a)), 0.075, mat_m, "Marca"))
        larg = 0.3
    return base, larg


def rampa_rolamento(angulo_graus=22.0, comprimento=5.2, raio=0.62, fase=0.0, linha_chegada=1):
    """Esfera, cilindro e aro (de mesmo raio) descem uma rampa a partir do repouso, em raias lado a lado: a = g sen θ/(1 + k),
    com k = 2/5, 1/2 e 1: a esfera chega primeiro, depois o cilindro e por fim o aro. Ciclo único: fase 1 = o aro chega ao fim."""
    th = math.radians(angulo_graus)
    u, n = Vector((math.cos(th), 0, math.sin(th))), Vector((-math.sin(th), 0, math.cos(th)))
    L = comprimento
    W = 4.2
    _extrusao_xz([(0, 0), (L * math.cos(th), 0), (L * math.cos(th), L * math.sin(th))], W / 2, "Rampa")
    ks = {"esfera": 0.4, "cilindro": 0.5, "aro": 1.0}
    accs = {t: 1.0 / (1.0 + k) for t, k in ks.items()}                      # a ∝ 1/(1+k) (g sen θ fora)
    T2 = 2 * (L - 2.2 * raio) / accs["aro"]                                    # tempo² para o aro chegar (fase = t/T)
    lanes = {"esfera": -1.4, "cilindro": 0.0, "aro": 1.4}
    corpos = {}
    for t in ("esfera", "cilindro", "aro"):
        base, larg = _corpo_rolante(t, raio)
        spin = bpy.data.objects.new("Giro", None)
        bpy.context.collection.objects.link(spin)
        base.parent = spin
        corpos[t] = (spin, base)
    mat_d = _mat_dash()
    if linha_chegada:
        s_f = L - 1.2 * raio
        p0 = u * (L - 2.2 * raio) + n * raio
        ga.criar_curva("Chegada", v3.tracejado([tuple(p0 + Vector((0, -W / 2, 0))), tuple(p0 + Vector((0, W / 2, 0)))], False, 0.2, 0.6), mat_d, 0.016)

    def atualizar(fase):
        tt = min(max(fase, 0.0), 1.0)
        for t, (spin, base) in corpos.items():
            s = min(0.5 * accs[t] * T2 * tt * tt, L - 2.2 * raio)           # distância descida (parte do topo)
            pos = u * (L - 0.8 * raio - s) + n * raio
            spin.location = (pos.x, lanes[t], pos.z)
            _alinhar(spin, tuple(u), (0, 1, 0), tuple(n))
            base.rotation_euler = (0, s / raio, 0)

    atualizar(fase)
    proxy = _caixa((L * math.cos(th) + 1.6, W + 0.8, L * math.sin(th) + 1.8), (L * math.cos(th) / 2, 0, L * math.sin(th) / 2 + 0.5))
    return proxy, atualizar


# ── looping ──────────────────────────────────────────────────────────────────
def trilho_looping(raio_loop=1.4, altura_inicial=None, largura=0.9, deslocamento_y=1.0, raio_bola=0.16, fase=0.0, linha_energia=1):
    """Pista com rampa e um looping vertical (sem atrito): a bola parte do repouso na altura h0 e a velocidade vem da conservação
    da energia, v = √(2 g (h0 − z)). Ciclo único. Para completar o looping é preciso h0 ≥ 2,5 R (o padrão usa 3,2 R).
    A pista é um ribbon de vidro; a linha violeta tracejada é o nível h0 (energia total)."""
    R = raio_loop
    h0 = altura_inicial or 3.2 * R
    ang = math.radians(40)
    pts = []
    # rampa: de (−ramp_len cos α, h0) até a base, com concordância suave (arco de raio 2R, tangente à rampa e ao chão)
    Rb = 2.2 * R
    # ponto de tangência da rampa com o arco de concordância
    xa = -Rb * math.sin(ang)
    za = Rb * (1 - math.cos(ang))
    start = (xa - (h0 - za) / math.tan(ang), h0)
    N1 = 60
    for i in range(N1):
        f = i / N1
        pts.append((start[0] + (xa - start[0]) * f, 0.0, start[1] + (za - start[1]) * f))
    for i in range(N1):                                         # arco de concordância: ângulo de −α a 0
        a = -ang + ang * i / N1
        pts.append((Rb * math.sin(a), 0.0, Rb * (1 - math.cos(a))))
    N2 = 120
    for i in range(N2 + 1):                                     # looping: φ de 0 a 2π (centro em (0, R)); o ribbon se desloca em y
        ph = 2 * math.pi * i / N2
        pts.append((R * math.sin(ph), deslocamento_y * i / N2, R * (1 - math.cos(ph))))
    for i in range(1, 41):                                      # saída reta
        pts.append((i * 0.12, deslocamento_y, 0.0))
    # comprimento de arco
    acum = [0.0]
    for a, b in zip(pts, pts[1:]):
        acum.append(acum[-1] + math.dist(a, b))
    total = acum[-1]
    # ribbon de vidro
    bm = bmesh.new()
    esq, dir_ = [], []
    for i, p in enumerate(pts):
        j = min(i + 1, len(pts) - 1)
        i0 = max(i - 1, 0)
        t = Vector(pts[j]) - Vector(pts[i0])
        t.normalize()
        lado = Vector((0, 1, 0))
        esq.append(bm.verts.new(Vector(p) - lado * largura / 2))
        dir_.append(bm.verts.new(Vector(p) + lado * largura / 2))
    for i in range(len(pts) - 1):
        try:
            bm.faces.new((esq[i], esq[i + 1], dir_[i + 1], dir_[i]))
        except ValueError:
            pass
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    me = bpy.data.meshes.new("Trilho")
    bm.to_mesh(me)
    bm.free()
    pista = bpy.data.objects.new("Trilho", me)
    bpy.context.collection.objects.link(pista)
    bpy.context.view_layer.objects.active = pista
    pista.select_set(True)
    sol = pista.modifiers.new("e", "SOLIDIFY")
    sol.thickness = 0.06
    sol.offset = 0
    bpy.ops.object.shade_smooth_by_angle(angle=math.radians(35))
    cm.material_vidro(pista, base=0.28, ganho=0.6, brilho_borda=1.8)
    ga.criar_curva("Borda", [([tuple(Vector(p) - Vector((0, largura / 2, 0))) for p in pts], False)], v3.material_cor("BordaTrilho", "fonte_contorno", 1.2), 0.015)
    ga.criar_curva("Borda", [([tuple(Vector(p) + Vector((0, largura / 2, 0))) for p in pts], False)], v3.material_cor("BordaTrilho", "fonte_contorno", 1.2), 0.015)
    if linha_energia:
        ga.criar_curva("Energia", v3.tracejado([(start[0] - 0.4, -0.6, h0), (R + 1.8, -0.6, h0)], False, 0.24, 0.6), _mat_dash(), 0.015)
    bola = v3.esfera_pt((0, 0, 0), raio_bola, v3.material_degrade("Bola", "texto_neutro", "fonte_contorno", 1.0, 0.7), "Bola")

    # tempo → comprimento de arco por integração da energia (g = 1): ds/dt = √(2 (h0 − z) )
    def z_de(s):
        i = max(1, min(len(acum) - 1, next((k for k in range(1, len(acum)) if acum[k] >= s), len(acum) - 1)))
        f = (s - acum[i - 1]) / ((acum[i] - acum[i - 1]) or 1.0)
        a, b = pts[i - 1], pts[i]
        return tuple(a[k] + f * (b[k] - a[k]) for k in range(3)), (Vector(b) - Vector(a)).normalized()

    dt = 1e-3
    s, t = 0.0, 0.0
    traj = [0.0]
    while s < total * 0.995 and t < 60:
        p, _ = z_de(s)
        v = math.sqrt(max(2 * (h0 - p[2]), 0.02))
        s += v * dt
        t += dt
        traj.append(min(s, total))
    Nt = len(traj) - 1

    def atualizar(fase):
        f = min(max(fase, 0.0), 1.0)
        s_ = traj[int(round(f * Nt))]
        p, tg = z_de(s_)
        nrm = Vector((-tg.z, 0.0, tg.x))                     # esquerda do sentido de percurso (para dentro do looping)
        pos = Vector(p) + nrm * (raio_bola + 0.03)
        bola.location = tuple(pos)

    atualizar(fase)
    xs = [p[0] for p in pts]
    proxy = _caixa((max(xs) - start[0] + 1.6, deslocamento_y + largura + 1.4, h0 + 1.2), ((max(xs) + start[0]) / 2, deslocamento_y / 2, h0 / 2))
    return proxy, atualizar


def cena_preview():
    co.limpar_cena()
    proxy, _ = plano_inclinado(movimento=0)
    co.mundo()
    co.luzes()
    co.camera_enquadrada(co.cantos([proxy]), azimute=-75, elevacao=14, margem=0.08)
    co.render(co.OUT / "mecanica_b_v1.png")


if __name__ == "__main__":
    cena_preview()

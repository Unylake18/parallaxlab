"""Eletromagnetismo em 3D (6.4, 6.7, 6.8, 6.10, 6.12) — estudo 21 (sandbox).

Convenções do arsenal (decisões do usuário em 2026-10-07): campo elétrico E = ciano; campo magnético B = MAGENTA; velocidade,
força, torque, dl e momento de dipolo = BRANCO; normal = azul; construções = violeta tracejado; o sinal da carga é ESCULPIDO
(+ ou − em relevo, virado para a câmera); polos do ímã: N = azul, S = magenta (os nomes N e S vão por rótulo no Manim).
fase de 0 a 1 = um ciclo (loop) ou, nos de ciclo único, do começo ao fim.
"""

import math
import sys
from pathlib import Path

import bpy
from mathutils import Vector

sys.path.insert(0, str(Path(__file__).resolve().parent))
import casca_oca as co  # noqa: E402
import cilindro_macico as cm  # noqa: E402
import gaussiana as ga  # noqa: E402
import oscilacoes as osc  # noqa: E402
import vetores3d as v3  # noqa: E402

MG = co.ST["materiais"]["magnetismo"]
VF = co.ST["materiais"]["vetor_fisico"]
BOB = co.ST["materiais"]["bobina"]


def _mat_B():
    return v3.material_cor("CampoB", MG["campo_cor"], MG["campo_emissao"])


def _mat_E():
    return v3.material_cor("CampoE", "campo_eletrico", 1.6)


def _mat_vf():
    return v3.material_cor("VetorFisico", VF["cor"], VF["emissao"])


def _mat_dash():
    return co._material("TracoEM", {"cor": "gaussiana", "emissao": 1.8, "rugosidade": 0.4})


def _mat_fio():
    return co._material("FioEM", {"cor": BOB["cor"], "emissao": BOB["emissao"], "rugosidade": BOB["rugosidade"], "metalico": BOB["metalico"]})


def _caixa(escala, local):
    bpy.ops.mesh.primitive_cube_add(size=1, location=local)
    o = bpy.context.active_object
    o.name = "ProxyEnquadramento"
    o.scale = escala
    bpy.ops.object.transform_apply(scale=True)
    o.hide_render = True
    return o


def _eixo(p0, p1, periodo=0.24):
    return ga.criar_curva("Eixo", v3.tracejado([p0, p1], False, periodo, 0.6), v3.material_cor("EixoEM", "texto_neutro", 0.8), 0.01)


# ── Biot–Savart numa espira ─────────────────────────────────────────────────
def biot_savart_espira(raio=1.5, distancia=2.4, theta0=2.2, movimento=0, fase=0.0):
    """Espira de fio azul no plano YZ, o ponto P no eixo, o elemento dl (branco), o vetor r de dl até P (violeta
    tracejado) e dB (magenta) em P, de direção dl × r. Com movimento o elemento percorre a espira (um ciclo)."""
    R, d = raio, distancia
    n = 160
    ga.criar_curva("Espira", [([(0.0, R * math.cos(2 * math.pi * k / n), R * math.sin(2 * math.pi * k / n)) for k in range(n)] + [(0.0, R, 0.0)], False)],
                   _mat_fio(), 0.055)
    _eixo((-0.8, 0, 0), (d + 1.4, 0, 0))
    v3.esfera_pt((d, 0, 0), 0.1, _mat_vf(), "PontoP")
    mat_vf, mat_B, mat_d = _mat_vf(), _mat_B(), _mat_dash()
    dinam = []

    def montar(th):
        v3.remover(dinam)
        e = Vector((0, R * math.cos(th), R * math.sin(th)))
        dl = Vector((0, -math.sin(th), math.cos(th)))
        r = Vector((d, 0, 0)) - e
        dB = dl.cross(r).normalized()
        dinam.append(v3.esfera_pt(tuple(e), 0.08, mat_vf, "Elemento"))
        dinam.append(v3.seta(tuple(e), tuple(dl * 0.85), mat_vf, 0.85))
        dinam.append(ga.criar_curva("R", v3.tracejado([tuple(e), (d, 0, 0)], False, 0.2, 0.6), mat_d, 0.016))
        dinam.append(v3.seta((d, 0, 0), tuple(dB * 1.7), mat_B, 1.7))

    def atualizar(fase):
        montar(2 * math.pi * fase + theta0 if movimento else theta0)

    atualizar(fase)
    proxy = _caixa((d + 2.2, 2 * R + 0.9, 2 * R + 0.3), (d / 2 + 0.1, 0, 0))
    return proxy, atualizar


# ── onda eletromagnética ─────────────────────────────────────────────────────
def onda_eletromagnetica(comprimento=9.0, n_setas=28, n_ondas=2, amplitude=1.1, poynting=1, planos=1, fase=0.0):
    """Onda plana linearmente polarizada se propagando em +X: E (ciano, ao longo de Z) e B (magenta, ao longo de Y), em fase.
    Curvas das pontas, direção de propagação (Poynting S = E × B, branco) e dois planos translúcidos (o de E e o de B).
    fase de 0 a 1 = um período."""
    L, A = comprimento, amplitude
    k = 2 * math.pi * n_ondas / L
    x0 = -L / 2
    xs = [x0 + L * (i + 0.5) / n_setas for i in range(n_setas)]
    mat_E, mat_B = _mat_E(), _mat_B()
    setas_E = [v3.seta((x, 0, 0), (0, 0, 1), mat_E, 1.0) for x in xs]
    setas_B = [v3.seta((x, 0, 0), (0, 1, 0), mat_B, 1.0) for x in xs]
    NP = 200
    _, spE = osc.curva_viva("CurvaE", NP, v3.material_cor("CurvaE", "campo_eletrico", 1.4), 0.025)
    _, spB = osc.curva_viva("CurvaB", NP, v3.material_cor("CurvaB", "campo_magnetico", 1.4), 0.025)
    _eixo((x0 - 0.5, 0, 0), (-x0 + 0.9, 0, 0), 0.26)
    if poynting:
        v3.seta((x0 - 0.9, 0, 0), (1.5, 0, 0), _mat_vf(), 1.5)
    if planos:
        h = A + 0.35
        c_xz = [(x0 - 0.3, 0, -h), (-x0 + 0.3, 0, -h), (-x0 + 0.3, 0, h), (x0 - 0.3, 0, h)]
        c_xy = [(x0 - 0.3, -h, 0), (-x0 + 0.3, -h, 0), (-x0 + 0.3, h, 0), (x0 - 0.3, h, 0)]
        v3.quad_translucido(c_xz, cor="campo_eletrico", base=0.05, ganho=0.25, brilho=1.0)
        v3.quad_translucido(c_xy, cor="campo_magnetico", base=0.05, ganho=0.25, brilho=1.0)

    def atualizar(fase):
        a = 2 * math.pi * fase
        for x, sE, sB in zip(xs, setas_E, setas_B):
            val = A * math.sin(k * (x - x0) - a)
            v3.ajustar_seta(sE, (x, 0, 0), (0, 0, val))
            v3.ajustar_seta(sB, (x, 0, 0), (0, val, 0))
        osc.pontos_curva(spE, [(x0 + L * i / (NP - 1), 0, A * math.sin(k * L * i / (NP - 1) - a)) for i in range(NP)])
        osc.pontos_curva(spB, [(x0 + L * i / (NP - 1), A * math.sin(k * L * i / (NP - 1) - a), 0) for i in range(NP)])

    atualizar(fase)
    proxy = _caixa((L + 2.4, 2 * A + 1.0, 2 * A + 1.0), (0, 0, 0))
    return proxy, atualizar


# ── partícula carregada em B uniforme ────────────────────────────────────────
def particula_em_B(sinal=1, raio_giro=1.2, passo=1.5, voltas=2.5, campo=1, trajetoria=1, fase=0.0):
    """Hélice de uma carga em B uniforme (+Z, magenta). Carga com sinal esculpido; v tangente e F = q v × B apontando
    para o eixo (brancos). Ciclo único: a partícula percorre `voltas` voltas do começo ao fim da hélice."""
    R, P = raio_giro, passo
    z_ini = -P * voltas / 2
    glifos = []
    sentido = -1 if sinal > 0 else 1                              # q > 0 gira no sentido horário visto de +Z
    ang = lambda t: sentido * t
    pos = lambda t: (R * math.cos(ang(t)), R * math.sin(ang(t)), z_ini + P * t / (2 * math.pi))
    T = 2 * math.pi * voltas
    if trajetoria:
        pts = [pos(T * i / 220) for i in range(221)]
        ga.criar_curva("Trajetoria", v3.tracejado(pts, False, 0.22, 0.6), _mat_dash(), 0.016)
    if campo:
        mat_B = _mat_B()
        for gx in (-2.1, 0.0, 2.1):
            for gy in (-2.1, 0.0, 2.1):
                if abs(gx) < 0.1 and abs(gy) < 0.1:
                    continue
                for gz in (z_ini - 0.2, z_ini + P * voltas + 0.2 - 1.0):
                    v3.seta((gx, gy, gz), (0, 0, 1.0), mat_B, 1.0)
    esf = v3.carga_sinal(pos(0), sinal, 0.3, glifos)
    mat_vf = _mat_vf()
    dinam = []

    def atualizar(fase):
        t = T * min(max(fase, 0.0), 1.0)
        p = pos(t)
        esf.location = p
        for g in glifos:
            g.location = p
        v3.remover(dinam)
        a = ang(t)
        v = Vector((-math.sin(a) * sentido, math.cos(a) * sentido, P / (2 * math.pi * R))).normalized()
        dinam.append(v3.seta(p, tuple(v * 1.1), mat_vf, 1.1))
        dinam.append(v3.seta(p, (-math.cos(a) * 0.9, -math.sin(a) * 0.9, 0.0), mat_vf, 0.9))

    atualizar(fase)
    proxy = _caixa((2 * 2.1 + 1.2, 2 * 2.1 + 1.2, P * voltas + 1.4), (0, 0, 0))
    return proxy, atualizar, glifos


# ── espira de corrente em B uniforme ─────────────────────────────────────────
def espira_em_B(raio=1.5, amplitude_graus=70.0, movimento=0, angulo_graus=40.0, fase=0.0):
    """Espira de fio azul que gira em torno de Z num B uniforme (+Y, magenta). Momento de dipolo μ = I A n̂ e torque
    τ = μ × B (brancos). Com movimento a espira oscila em torno do alinhamento (μ ∥ B): θ(t) = θ0 cos(2π fase)."""
    R = raio
    mat_B, mat_fio, mat_vf = _mat_B(), _mat_fio(), _mat_vf()
    for gx in (-2.6, 0.0, 2.6):
        for gz in (-1.6, 0.0, 1.6):
            v3.seta((gx, -2.1, gz), (0, 1, 0), mat_B, 1.0)
            v3.seta((gx, 1.9, gz), (0, 1, 0), mat_B, 1.0)
    cv_ = bpy.data.curves.new("Espira", "CURVE")
    cv_.dimensions = "3D"
    cv_.bevel_depth = 0.055
    cv_.bevel_resolution = 3
    sp = cv_.splines.new("POLY")
    NP = 72
    sp.points.add(NP - 1)
    sp.use_cyclic_u = True
    obj = bpy.data.objects.new("Espira", cv_)
    bpy.context.collection.objects.link(obj)
    obj.data.materials.append(mat_fio)
    _eixo((0, 0, -2.0), (0, 0, 2.0), 0.2)
    dinam = []

    def montar(th):
        n = Vector((math.sin(th), math.cos(th), 0.0))
        w = Vector((math.cos(th), -math.sin(th), 0.0))
        pts = [tuple(R * math.cos(2 * math.pi * k / NP) * Vector((0, 0, 1)) + R * math.sin(2 * math.pi * k / NP) * w) for k in range(NP)]
        osc.pontos_curva(sp, pts)
        v3.remover(dinam)
        dinam.append(v3.seta((0, 0, 0), tuple(n * 1.5), mat_vf, 1.5))                              # μ
        tau = math.sin(th)
        dinam.append(v3.seta((0, 0, 0), (0, 0, 1.3 * tau), mat_vf, abs(1.3 * tau)) if abs(tau) > 0.03 else v3.seta((0, 0, 0), (0, 0, 1), mat_vf, 1e-3))
        t = math.pi / 2                                                                           # seta de corrente (sentido de μ)
        P = Vector((0, 0, 1)) * R * math.cos(t) + w * R * math.sin(t)
        tg = -Vector((0, 0, 1)) * math.sin(t) + w * math.cos(t)
        dinam.append(v3.seta(tuple(P - tg * 0.25), tuple(tg * 0.5), mat_vf, 0.5))

    def atualizar(fase):
        montar(math.radians(amplitude_graus) * math.cos(2 * math.pi * fase) if movimento else math.radians(angulo_graus))

    atualizar(fase)
    proxy = _caixa((2 * 2.6 + 1.2, 4.6, 2 * 1.6 + 1.4), (0, 0, 0))
    return proxy, atualizar


# ── ímã atravessando uma espira (Faraday / Lenz) ─────────────────────────────
def ima_espira(raio=1.3, comprimento_ima=1.1, lado_ima=0.9, movimento=0, posicao=-2.0, fase=0.0, setas=1):
    """Ímã de barra (N azul, S magenta) que atravessa uma espira fixa (fio azul, disco de fluxo violeta). Setas brancas
    na espira mostram a corrente induzida: sentido por Lenz e módulo ∝ |dΦ/dt| (nulo quando o ímã está no plano da espira).
    Ciclo único: o ímã vai de −4,2 a +4,2 (polo N na frente)."""
    R = raio
    n = 120
    ga.criar_curva("Espira", [([(0.0, R * math.cos(2 * math.pi * k / n), R * math.sin(2 * math.pi * k / n)) for k in range(n + 1)], False)], _mat_fio(), 0.06)
    disco = [(0.0, R * 0.97 * math.cos(2 * math.pi * k / 48), R * 0.97 * math.sin(2 * math.pi * k / 48)) for k in range(48)]
    v3.quad_translucido(disco, base=0.12)
    Lm, s = comprimento_ima, lado_ima
    bpy.ops.mesh.primitive_cube_add(size=1)
    N_ = bpy.context.active_object
    N_.name = "PoloN"
    N_.scale = (Lm, s, s)
    bpy.ops.object.transform_apply(scale=True)
    cm.material_vidro(N_, cor=MG["polo_norte_cor"], base=MG["ima_base"], ganho=MG["ima_ganho"], brilho_borda=MG["ima_brilho"])
    bpy.ops.mesh.primitive_cube_add(size=1)
    S_ = bpy.context.active_object
    S_.name = "PoloS"
    S_.scale = (Lm, s, s)
    bpy.ops.object.transform_apply(scale=True)
    cm.material_vidro(S_, cor=MG["polo_sul_cor"], base=MG["ima_base"], ganho=MG["ima_ganho"], brilho_borda=MG["ima_brilho"])
    mat_vf = _mat_vf()
    flechas = [v3.seta((0, 0, 0), (0, 1, 0), mat_vf, 0.5) for _ in range(4)]
    emax = max(abs(x) / (R * R + x * x) ** 2.5 for x in [i * 0.01 for i in range(1, 400)])
    X0, X1 = -4.2, 4.2

    def atualizar(fase):
        xm = X0 + (X1 - X0) * min(max(fase, 0.0), 1.0) if movimento else posicao
        N_.location = (xm + Lm / 2, 0, 0)                      # N na frente (+X)
        S_.location = (xm - Lm / 2, 0, 0)
        eps = xm / (R * R + xm * xm) ** 2.5 / emax              # ε ∝ x/(R²+x²)^(5/2): −, 0, + (aproxima, passa, afasta)
        for k, f in enumerate(flechas):
            t = math.pi / 4 + k * math.pi / 2
            p = (0.0, R * math.cos(t), R * math.sin(t))
            tg = Vector((0.0, -math.sin(t), math.cos(t)))
            if not setas or abs(eps) < 0.03:
                v3.ajustar_seta(f, p, (0, 0, 0))
            else:
                # eps < 0 (aproximando): corrente horária vista de +X (oposta a CCW); eps > 0: anti-horária (Lenz)
                v3.ajustar_seta(f, tuple(Vector(p) - tg * 0.5 * (1 if eps > 0 else -1)), tuple(tg * (1 if eps > 0 else -1) * (0.5 + 0.9 * abs(eps))), 0.5 + 0.9 * abs(eps))

    atualizar(fase)
    proxy = _caixa((9.4, 2 * R + 1.0, 2 * R + 0.8), (0, 0, 0))
    return proxy, atualizar


# ── barra deslizante em trilhos (fem de movimento) ───────────────────────────
def barra_trilhos(largura=1.3, comprimento=6.2, centro=3.2, amplitude=1.5, movimento=0, posicao=3.6, fase=0.0, campo=1):
    """Duas trilhas paralelas fechadas à esquerda e uma barra que desliza num B uniforme (+Z, magenta). O violeta é a área do
    circuito (o fluxo); as setas brancas são a corrente induzida (sentido de Lenz, módulo ∝ v). Com movimento a barra oscila:
    x = centro + amplitude sen(2π fase)."""
    w = largura
    mat_fio, mat_B, mat_vf = _mat_fio(), _mat_B(), _mat_vf()
    for sgn in (-1, 1):
        r = osc._caixa("Trilho", (comprimento, 0.14, 0.1), (comprimento / 2, sgn * w, -0.05))
        r.hide_render = False
        cm.material_vidro(r, base=0.5, ganho=0.6, brilho_borda=2.0)
    liga = osc._caixa("Liga", (0.14, 2 * w + 0.14, 0.1), (0.0, 0.0, -0.05))
    liga.hide_render = False
    cm.material_vidro(liga, base=0.5, ganho=0.6, brilho_borda=2.0)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.12, depth=2 * w + 0.4, vertices=32)
    barra = bpy.context.active_object
    barra.name = "Barra"
    barra.rotation_euler = (math.radians(90), 0, 0)
    bpy.ops.object.transform_apply(rotation=True)
    bpy.ops.object.shade_smooth()
    barra.data.materials.append(co._material("BarraTrilhos", {"cor": "fonte_contorno", "emissao": 1.2, "rugosidade": 0.3}))
    if campo:
        for gx in (1.0, 2.6, 4.2, 5.4):
            for gy in (-0.7, 0.7):
                v3.seta((gx, gy, 0.15), (0, 0, 1.0), mat_B, 1.0)
    flechas = [v3.seta((0, 0, 0.05), (1, 0, 0), mat_vf, 0.5) for _ in range(4)]
    area = bpy.data.meshes.new("AreaFluxo")
    ao = bpy.data.objects.new("AreaFluxo", area)
    bpy.context.collection.objects.link(ao)
    bpy.context.view_layer.objects.active = ao
    ao.select_set(True)
    sol = ao.modifiers.new("e", "SOLIDIFY")
    sol.thickness = 0.02
    cm.material_vidro(ao, cor="gaussiana", base=0.14, ganho=0.4, brilho_borda=1.2)

    def atualizar(fase):
        x = centro + amplitude * math.sin(2 * math.pi * fase) if movimento else posicao
        v = amplitude * math.cos(2 * math.pi * fase) / amplitude if movimento else 0.0          # ∝ velocidade da barra, em [−1, 1]
        barra.location = (x, 0, 0.12)
        area.clear_geometry()
        area.from_pydata([(0.07, -w, 0.01), (x, -w, 0.01), (x, w, 0.01), (0.07, w, 0.01)], [], [(0, 1, 2, 3)])
        area.update()
        # CCW visto de cima: base +X, barra +Y, topo −X, esquerda −Y. v > 0 (área cresce): corrente horária (Lenz)
        ccw = [((x * 0.5, -w, 0.06), (1, 0, 0)), ((x, 0.0, 0.06), (0, 1, 0)), ((x * 0.5, w, 0.06), (-1, 0, 0)), ((0.0, 0.0, 0.06), (0, -1, 0))]
        s = -1 if v > 0 else 1
        for f, (p, d) in zip(flechas, ccw):
            tam = 0.25 + 0.7 * abs(v)
            if abs(v) < 0.04:
                v3.ajustar_seta(f, p, (0, 0, 0))
            else:
                dv = Vector(d) * s
                v3.ajustar_seta(f, tuple(Vector(p) - dv * tam * 0.5), tuple(dv * tam), tam)

    atualizar(fase)
    proxy = _caixa((comprimento + 0.6, 2 * w + 1.6, 1.4), (comprimento / 2, 0, 0.4))
    return proxy, atualizar


# ── superfícies equipotenciais ───────────────────────────────────────────────
def _raio_equipotencial(V, c, direcao, rmax=7.0):
    """Primeiro r ao longo de `direcao` (a partir do ponto-fonte) em que V(r) cai a c (V decrescente em r)."""
    lo, hi = 0.02, rmax
    if V(direcao * hi) > c:
        return hi
    for _ in range(40):
        mid = 0.5 * (lo + hi)
        if V(direcao * mid) > c:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def equipotenciais(tipo="dipolo", niveis=(0.5, 0.8, 1.3), distancia=2.0, sinal=1, plano=1):
    """Superfícies equipotenciais (violeta translúcido) de uma carga pontual (esferas) ou de um dipolo (V = 1/r₊ − 1/r₋,
    achadas por raios a partir de cada carga), com as cargas de sinal esculpido. O plano V = 0 do dipolo em violeta.
    Devolve (proxy, glifos)."""
    glifos = []
    ext = 2.4
    if tipo == "carga_pontual":
        for c in niveis:
            r = 1.0 / c
            F = lambda u, v, r=r: (r * math.cos(v), r * math.sin(v) * math.cos(u), r * math.sin(v) * math.sin(u))
            s = v3.malha_param("Equipotencial", F, 0, 2 * math.pi, 0.0, math.pi, 64, 32, espessura=0.012, vidro=False)
            e = co.ST["materiais"]["equipotencial"]
            cm.material_vidro(s, cor=e["cor"], base=e["base"], ganho=e["ganho"], brilho_borda=e["brilho"])
        v3.carga_sinal((0, 0, 0), sinal, 0.32, glifos)
        ext = 1.0 / min(niveis) * 1.05
    else:
        d = distancia / 2
        qp, qn = Vector((d, 0, 0)), Vector((-d, 0, 0))
        V = lambda p: 1.0 / max((p - qp).length, 1e-6) - 1.0 / max((p - qn).length, 1e-6)
        Vn = lambda p: -V(p)
        e = co.ST["materiais"]["equipotencial"]
        for lado, fonte, fV, sg in ((1, qp, V, 1), (-1, qn, Vn, -1)):
            for c in niveis:
                def F(u, v, fonte=fonte, fV=fV, c=c):
                    dire = Vector((math.cos(v), math.sin(v) * math.cos(u), math.sin(v) * math.sin(u)))
                    r = _raio_equipotencial(lambda p: fV(fonte + p), c, dire)
                    return tuple(fonte + dire * r)
                s = v3.malha_param("Equipotencial", F, 0, 2 * math.pi, 0.0, math.pi, 48, 28, espessura=0.012, vidro=False)
                cm.material_vidro(s, cor=e["cor"], base=e["base"], ganho=e["ganho"], brilho_borda=e["brilho"])
        v3.carga_sinal(tuple(qp), sinal, 0.32, glifos)
        v3.carga_sinal(tuple(qn), -sinal, 0.32, glifos)
        if plano:
            h = 2.2
            v3.quad_translucido([(0, -h, -h), (0, h, -h), (0, h, h), (0, -h, h)], base=0.05, ganho=0.2, brilho=0.8)
        ext = 2.6
    proxy = _caixa((2 * ext + 0.6, 2 * ext * 0.8 + 0.4, 2 * ext * 0.8 + 0.4), (0, 0, 0))
    return proxy, glifos


def cena_preview():
    co.limpar_cena()
    proxy, _ = biot_savart_espira()
    co.mundo()
    co.luzes()
    co.camera_enquadrada(co.cantos([proxy]), azimute=-40, elevacao=24, margem=0.08)
    co.render(co.OUT / "eletromag3d_v1.png")


if __name__ == "__main__":
    cena_preview()

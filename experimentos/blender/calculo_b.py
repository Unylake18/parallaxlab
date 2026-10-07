"""Cálculo, álgebra linear e EDP, fila B (10.1, 10.6, 11.2, 11.8, 13, 15) — estudo 26 (sandbox).

Plano e reta em R³, multiplicadores de Lagrange, integral de linha, divergência e rotacional locais (cubo elementar e roda de
pás), transformação linear 3D, autovetores de uma matriz simétrica e modos de uma membrana. Gramática do arsenal: superfícies e
corpos = vidro azul; curvas = azul-claro; construções (plano, cubo elementar, projeções) = violeta; vetores = branco; normal e
gradiente da restrição = azul; campo vetorial = ciano. fase de 0 a 1 = um ciclo (loop) ou, nos de ciclo único, do começo ao fim.
Valores, fórmulas e rótulos são do Manim.
"""

import math
import sys
from pathlib import Path

import bmesh
import bpy
from mathutils import Matrix, Vector

sys.path.insert(0, str(Path(__file__).resolve().parent))
import calc_vetorial as cv  # noqa: E402
import casca_oca as co  # noqa: E402
import cilindro_macico as cm  # noqa: E402
import gaussiana as ga  # noqa: E402
import matematica3d as m3  # noqa: E402
import vetores3d as v3  # noqa: E402

TAU = 2 * math.pi


def _linha(nome, a, b, mat, esp=0.014, traco=False):
    pts = v3.tracejado([a, b], False, 0.2, 0.6) if traco else [([tuple(a), tuple(b)], False)]
    return ga.criar_curva(nome, pts, mat, esp)


def _ortogonais(n):
    n = Vector(n).normalized()
    ref = Vector((0, 0, 1)) if abs(n.z) < 0.9 else Vector((1, 0, 0))
    e1 = n.cross(ref).normalized()
    return e1, n.cross(e1).normalized()


# ── plano e reta em R³ ───────────────────────────────────────────────────────
def plano_e_reta_r3(normal=(1.0, 0.6, 2.0), distancia=1.4, direcao=(0.55, 0.45, 1.0), movimento=0, fase=0.0, tamanho=2.4):
    """Plano n · x = 0 (violeta translúcido, arestas tracejadas) com a normal n (azul), uma reta (azul-claro) que o fura num
    ponto I (branco) e um ponto P (branco) a uma distância d do plano, com o pé Q da perpendicular e o segmento PQ (violeta
    tracejado). Com movimento P sobe e desce ao longo de n̂ e a distância varia."""
    n = Vector(normal).normalized()
    e1, e2 = _ortogonais(n)
    s = tamanho
    cantos = [tuple(-e1 * s - e2 * s), tuple(e1 * s - e2 * s), tuple(e1 * s + e2 * s), tuple(-e1 * s + e2 * s)]
    v3.quad_translucido(cantos)
    m3._tracejado_poligono(cantos)
    mat_n, mat_v, mat_c = cv._mat_normal(), m3._mat_vf(), cv._mat_curva()
    v3.seta((0, 0, 0), n * 1.3, mat_n)
    d = Vector(direcao).normalized()
    A = Vector((-1.9, -1.3, -2.4))                                        # um ponto da reta
    t_int = -n.dot(A) / n.dot(d)
    I = A + d * t_int
    ga.criar_curva("Reta", [([tuple(A + d * (t_int - 3.3)), tuple(A + d * (t_int + 3.3))], False)], mat_c, 0.022)
    v3.esfera_pt(tuple(I), 0.09, mat_v, "Interseccao")
    base = e1 * 0.9 + e2 * -0.6                                           # posição lateral de P (pé de P no plano)
    dinam = []

    def atualizar(fase):
        v3.remover(dinam)
        h = distancia + (0.8 * math.sin(TAU * fase) if movimento else 0.0)
        P, Q = base + n * h, base
        dinam.append(v3.esfera_pt(tuple(P), 0.1, mat_v, "PontoP"))
        dinam.append(v3.esfera_pt(tuple(Q), 0.07, mat_v, "PeQ"))
        dinam.append(_linha("DistanciaPQ", P, Q, m3._mat_dash(), 0.016, True))

    atualizar(fase)
    proxy = m3._caixa((2 * s + 0.6, 2 * s + 0.6, 2 * s), (0, 0, 0.3))
    return proxy, atualizar


# ── multiplicadores de Lagrange ──────────────────────────────────────────────
def _f_lagrange(x, y):
    return 1.0 + 0.30 * x + 0.20 * y + 0.15 * (x * x - y * y)


def _grad_f(x, y):
    return Vector((0.30 + 0.30 * x, 0.20 - 0.30 * y, 0.0))


def lagrange_restricao(raio=1.5, angulo_graus=40.0, movimento=0, fase=0.0, extensao=2.4, escala_grad=2.4):
    """Superfície z = f(x, y) (vidro azul), a restrição g = x² + y² − r² = 0 (círculo violeta tracejado no piso e a curva
    correspondente sobre a superfície) e um ponto que percorre a restrição, com ∇f (branco) e ∇g (azul) no piso, ligados à
    superfície por um fio vertical tracejado. Os dois pontos de extremo restrito (∇f ∥ ∇g) ficam marcados. Com movimento o ponto
    dá uma volta e as duas setas ficam paralelas nos extremos."""
    F = lambda u, v: (u, v, _f_lagrange(u, v))
    v3.malha_param("Superficie", F, -extensao, extensao, -extensao, extensao, 56, 56)
    r = raio
    n = 160
    piso = [(r * math.cos(TAU * k / n), r * math.sin(TAU * k / n), 0.0) for k in range(n)]
    sobre = [(x, y, _f_lagrange(x, y) + 0.015) for (x, y, _) in piso]
    ga.criar_curva("RestricaoPiso", v3.tracejado(piso, True, 0.24, 0.6), m3._mat_dash(), 0.014)
    ga.criar_curva("RestricaoSuperficie", [(sobre, True)], cv._mat_curva(), 0.026)
    mat_v, mat_n = m3._mat_vf(), cv._mat_normal()
    cruz = lambda k: _grad_f(*piso[k][:2]).x * piso[k][1] - _grad_f(*piso[k][:2]).y * piso[k][0]
    for k in range(n):                                                    # extremos: ∇f ∥ p (cruzamento por zero de ∇f × p)
        if cruz(k) * cruz((k + 1) % n) < 0:
            x, y, _ = piso[k]
            v3.esfera_pt((x, y, _f_lagrange(x, y) + 0.04), 0.08, mat_v, "Extremo")
    dinam = []

    def atualizar(fase):
        v3.remover(dinam)
        th = TAU * fase if movimento else math.radians(angulo_graus)
        x, y = r * math.cos(th), r * math.sin(th)
        z = _f_lagrange(x, y)
        dinam.append(v3.esfera_pt((x, y, z + 0.03), 0.09, mat_v, "PontoR"))
        dinam.append(v3.esfera_pt((x, y, 0.0), 0.06, mat_v, "PontoPiso"))
        dinam.append(_linha("Fio", (x, y, 0.0), (x, y, z), m3._mat_dash(), 0.012, True))
        g = _grad_f(x, y) * escala_grad
        if g.length > 1e-3:
            dinam.append(v3.seta((x, y, 0.0), g, mat_v))
        dinam.append(v3.seta((x, y, 0.0), Vector((x, y, 0.0)).normalized() * 1.0, mat_n, 1.0))

    atualizar(fase)
    proxy = m3._caixa((2 * extensao + 0.6, 2 * extensao + 0.6, 3.4), (0, 0, 1.3))
    return proxy, atualizar


# ── integral de linha ────────────────────────────────────────────────────────
def integral_de_linha(campo="rotacional", raio=1.5, passo_z=0.3, extensao=2.8, n_campo=7, movimento=0, fase=0.0, arco=1.5):
    """Campo vetorial (setas ciano no plano z = 0) e uma curva C em hélice (azul-claro) de raio r, que sobe `passo_z` por
    radiano ao longo de `arco`·π radianos. Um ponto (branco) percorre a curva com a tangente dr (branca) e o campo F nesse ponto
    (ciano); o trecho já percorrido fica em destaque. Ciclo único: a fase 1 é o fim da curva."""
    f = cv.CAMPOS[campo]
    cv.criar_campo(campo, 2, n_campo, extensao, 0.7, 0.0)
    smax = arco * math.pi
    C = lambda s: Vector((raio * math.cos(s), raio * math.sin(s), passo_z * s))
    pts = [tuple(C(smax * k / 120)) for k in range(121)]
    ga.criar_curva("CurvaC", [(pts, False)], cv._mat_curva(), 0.02)
    mat_v, mat_t, mat_f = m3._mat_vf(), cv._mat_tang(), cv._mat_campo()
    mat_trilha = v3.material_cor("TrilhaC", "texto_neutro", 1.6)
    dinam = []

    def atualizar(fase):
        v3.remover(dinam)
        u = min(max(fase, 0.0), 1.0) if movimento else 0.5
        s = smax * u
        P = C(s)
        tg = (C(s + 1e-3) - C(s - 1e-3)).normalized()
        if s > 0.02:
            dinam.append(ga.criar_curva("Percorrido", [([tuple(C(s * k / max(2, int(60 * u + 2)))) for k in range(max(2, int(60 * u + 2)) + 1)], False)], mat_trilha, 0.034))
        dinam.append(v3.esfera_pt(tuple(P), 0.1, mat_v, "Ponto"))
        dinam.append(v3.seta(tuple(P), tg * 0.9, mat_t, 0.9))
        F = Vector(f(P.x, P.y, P.z))
        if F.length > 1e-3:
            dinam.append(v3.seta(tuple(P), F.normalized() * min(1.4, 0.35 + 0.28 * F.length), mat_f, min(1.4, 0.35 + 0.28 * F.length)))

    atualizar(fase)
    proxy = m3._caixa((2 * extensao, 2 * extensao, 2.2), (0, 0, 0.7))
    return proxy, atualizar


# ── divergência e rotacional locais ──────────────────────────────────────────
def _campo_cd(tipo):
    return {"radial": lambda x, y, z: Vector((x, y, z)), "rotacional": lambda x, y, z: Vector((-y, x, 0.0)),
            "sela": lambda x, y, z: Vector((x, -y, 0.0)), "uniforme": lambda x, y, z: Vector((1.2, 0.0, 0.0))}[tipo]


def divergencia_local(campo="radial", lado=1.5, posicao=(1.1, 0.5, 0.0), n_fundo=4, movimento=0, fase=0.0, extensao=2.4):
    """Cubo elementar (violeta, arestas tracejadas) num campo vetorial (ciano). Em cada uma das seis faces uma seta sai do centro
    da face com o campo ali calculado: no campo radial as setas das faces de fora são maiores que as de dentro (divergência
    positiva); no rotacional elas se compensam (divergência nula). Com movimento o cubo vai e volta ao longo de X."""
    f = _campo_cd(campo)
    if n_fundo:
        cv.criar_campo(campo, 3, int(n_fundo), extensao, 0.55, 0.0)
    h = lado / 2
    cubo = m3._caixa((lado, lado, lado), (0, 0, 0), "Cubo")
    cubo.hide_render = False
    cv._vidro_violeta(cubo, base=0.08)
    arestas = [(-h, -h), (h, -h), (h, h), (-h, h)]
    dinam = []
    mat_f = cv._mat_campo()
    mat_e = m3._mat_dash()
    centros = [Vector(c) * h for c in ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1))]

    def atualizar(fase):
        v3.remover(dinam)
        c = Vector(posicao) + Vector((0.9 * math.sin(TAU * fase), 0, 0)) * (1 if movimento else 0)
        cubo.location = c
        for sinal in (-h, h):
            dinam.append(ga.criar_curva("Aresta", v3.tracejado([tuple(c + Vector((x, y, sinal))) for (x, y) in arestas], True, 0.16, 0.6), mat_e, 0.012))
        for (x, y) in arestas:
            dinam.append(_linha("Aresta", c + Vector((x, y, -h)), c + Vector((x, y, h)), mat_e, 0.012, True))
        for dc in centros:
            P = c + dc
            F = f(P.x, P.y, P.z)
            if F.length > 1e-3:
                L = min(1.5, 0.45 * F.length)
                dinam.append(v3.seta(tuple(P), F.normalized() * L, mat_f, L))

    atualizar(fase)
    proxy = m3._caixa((2 * extensao, 2 * extensao, 2 * extensao), (0, 0, 0))
    return proxy, atualizar


def rotacional_roda_de_pas(campo="rotacional", posicao=(0.0, 0.0, 0.0), n_campo=7, extensao=2.8, movimento=0, fase=0.0, angulo_graus=0.0):
    """Roda de pás (cruz de duas placas com uma ponta marcada em branco) sobre o plano z = 0 num campo vetorial de setas
    ciano. `campo`: rotacional (a roda gira no sentido anti-horário), cisalhamento (gira no horário) ou irrotacional (campo
    ∝ r/r²: a roda só é arrastada, sem girar). Com movimento a roda dá uma volta (loop), com o sentido do rotacional: a rapidez
    é visual, o sentido é o do rotacional do campo."""
    campos = {"rotacional": lambda x, y, z: Vector((-y, x, 0.0)), "cisalhamento": lambda x, y, z: Vector((0.8 * y, 0.0, 0.0)),
              "irrotacional": lambda x, y, z: Vector((x, y, 0.0)) / (x * x + y * y + 0.5)}
    sentido = {"rotacional": 1.0, "cisalhamento": -1.0, "irrotacional": 0.0}[campo]
    f = campos[campo]
    mat_f = cv._mat_campo()
    pts = [(-extensao + 2 * extensao * i / (n_campo - 1)) for i in range(n_campo)]
    for x in pts:
        for y in pts:
            F = f(x, y, 0.0)
            if F.length > 1e-3 and (x, y) != (0.0, 0.0):
                L = min(0.75, 0.3 + 0.2 * F.length)
                v3.seta((x, y, 0.0), F.normalized() * L, mat_f, L)
    eixo = bpy.data.objects.new("Roda", None)
    bpy.context.collection.objects.link(eixo)
    eixo.location = posicao
    mat_p = v3.material_cor("PaRoda", "fonte_fisica", 1.2)
    for dim in ((1.4, 0.06, 0.55), (0.06, 1.4, 0.55)):
        p = m3._caixa(dim, (0, 0, 0), "Pa")
        p.hide_render = False
        p.data.materials.append(mat_p)
        p.parent = eixo
    pt = v3.esfera_pt((0.7, 0, 0), 0.1, m3._mat_vf(), "PontaMarcada")
    pt.parent = eixo
    hub = v3.esfera_pt((0, 0, 0), 0.13, m3._mat_vf(), "Eixo")
    hub.parent = eixo

    def atualizar(fase):
        eixo.rotation_euler = (0, 0, TAU * fase * sentido if movimento else math.radians(angulo_graus))

    atualizar(fase)
    proxy = m3._caixa((2 * extensao, 2 * extensao, 1.4), (0, 0, 0))
    return proxy, atualizar


# ── álgebra linear: transformação e autovetores ──────────────────────────────
def _cubo_malha(nome, lado):
    bm = bmesh.new()
    vs = [bm.verts.new((i * lado, j * lado, k * lado)) for k in (0, 1) for j in (0, 1) for i in (0, 1)]
    for q in ((0, 2, 3, 1), (4, 5, 7, 6), (0, 1, 5, 4), (2, 6, 7, 3), (0, 4, 6, 2), (1, 3, 7, 5)):
        bm.faces.new([vs[i] for i in q])
    bm.normal_update()
    me = bpy.data.meshes.new(nome)
    bm.to_mesh(me)
    bm.free()
    o = bpy.data.objects.new(nome, me)
    bpy.context.collection.objects.link(o)
    return o


ARESTAS_CUBO = [(0, 1), (2, 3), (4, 5), (6, 7), (0, 2), (1, 3), (4, 6), (5, 7), (0, 4), (1, 5), (2, 6), (3, 7)]


def transformacao_linear_3d(matriz=((1.2, 0.5, 0.0), (0.0, 0.9, 0.4), (0.3, 0.0, 1.1)), lado=1.5, movimento=0, fase=0.0, intensidade=1.0):
    """Cubo unitário (violeta, tracejado, fica parado) e a sua imagem pela matriz A (vidro azul, arestas azul-claro), com os
    vetores A e1, A e2, A e3 (as colunas de A) em branco. Com movimento o cubo vai de I até A e volta (interpolação linear
    I → A → I): a fase 0 e a fase 1 são o cubo original."""
    A = Matrix(matriz)
    I3 = Matrix.Identity(3)
    cubo = _cubo_malha("Imagem", lado)
    cm.material_vidro(cubo, base=0.22, ganho=0.55, brilho_borda=1.8)
    base = [Vector(v.co) for v in cubo.data.vertices]
    mat_c, mat_v, mat_d = cv._mat_curva(), m3._mat_vf(), m3._mat_dash()
    for (i, j) in ARESTAS_CUBO:                                          # cubo original (referência)
        _linha("Original", base[i], base[j], mat_d, 0.012, True)
    m3.eixos(3.3, False)
    dinam = []

    def atualizar(fase):
        v3.remover(dinam)
        s = (math.sin(math.pi * fase) ** 2 if movimento else intensidade)
        M = I3 + (A - I3) * s
        for v, b in zip(cubo.data.vertices, base):
            v.co = M @ b
        cubo.data.update()
        for (i, j) in ARESTAS_CUBO:
            dinam.append(_linha("ArestaImagem", M @ base[i], M @ base[j], mat_c, 0.02))
        for k in range(3):
            col = M @ (Vector([1.0 if t == k else 0.0 for t in range(3)]) * lado)
            dinam.append(v3.seta((0, 0, 0), col, mat_v, col.length))

    atualizar(fase)
    proxy = m3._caixa((3.4, 3.4, 3.4), (1.2, 1.2, 1.2))
    return proxy, atualizar


def autovetores_elipsoide(lambdas=(2.0, 1.25, 0.6), angulo_z=35.0, angulo_x=25.0, escala=1.0, movimento=0, fase=0.0, intensidade=1.0):
    """Esfera unitária (três círculos máximos violeta, parados) e a sua imagem por uma matriz simétrica A = Q Λ Qᵀ: um elipsoide
    (vidro azul) cujos semi-eixos têm comprimento |λ| e estão ao longo dos autovetores (setas brancas e eixos tracejados). Com
    movimento o elipsoide sai da esfera, chega a A e volta (loop)."""
    Q = Matrix.Rotation(math.radians(angulo_z), 3, "Z") @ Matrix.Rotation(math.radians(angulo_x), 3, "X")
    L = [float(x) for x in lambdas]
    mat_v, mat_d = m3._mat_vf(), m3._mat_dash()
    for k in range(3):                                                    # círculos máximos da esfera
        a, b = [Vector([1.0 if t == m else 0.0 for t in range(3)]) for m in range(3) if m != k]
        pts = [tuple((a * math.cos(TAU * i / 96) + b * math.sin(TAU * i / 96)) * escala) for i in range(96)]
        ga.criar_curva("CirculoMaximo", v3.tracejado(pts, True, 0.22, 0.6), mat_d, 0.012)
    dinam = []

    def atualizar(fase):
        v3.remover(dinam)
        s = (math.sin(math.pi * fase) ** 2 if movimento else intensidade)
        lam = [1.0 + (x - 1.0) * s for x in L]
        F = lambda u, v: tuple(Q @ Vector((lam[0] * math.sin(v) * math.cos(u), lam[1] * math.sin(v) * math.sin(u), lam[2] * math.cos(v))) * escala)
        dinam.append(v3.malha_param("Elipsoide", F, 0, TAU, 0.03 * math.pi, 0.97 * math.pi, 56, 40))
        for k in range(3):
            q = Vector((Q[0][k], Q[1][k], Q[2][k]))
            dinam.append(_linha("EixoAutovetor", q * -2.8, q * 2.8, m3._mat_eixo(), 0.01, True))
            dinam.append(v3.seta((0, 0, 0), q * lam[k] * escala, mat_v, abs(lam[k]) * escala))

    atualizar(fase)
    proxy = m3._caixa((4.4, 4.4, 3.4), (0, 0, 0))
    return proxy, atualizar


# ── EDP: modos de uma membrana ───────────────────────────────────────────────
def membrana_modos(m=2, n=1, lado=4.0, amplitude=0.7, movimento=0, fase=0.0, instante=0.0, nos=1):
    """Membrana quadrada fixa nas quatro bordas (moldura branca tracejada) vibrando no modo (m, n):
    z = A sen(mπx/L) sen(nπy/L) cos(2π fase). As linhas nodais (violeta tracejado) ficam paradas sobre a membrana. Com movimento
    dá um período completo (loop)."""
    L = lado
    mat_dash, mat_eixo = m3._mat_dash(), m3._mat_eixo()
    moldura = [(-L / 2, -L / 2, 0.0), (L / 2, -L / 2, 0.0), (L / 2, L / 2, 0.0), (-L / 2, L / 2, 0.0)]
    ga.criar_curva("Moldura", v3.tracejado(moldura, True, 0.24, 0.7), mat_eixo, 0.016)
    if nos:
        for k in range(1, int(m)):
            x = -L / 2 + L * k / m
            ga.criar_curva("NoX", v3.tracejado([(x, -L / 2, 0.012), (x, L / 2, 0.012)], False, 0.22, 0.6), mat_dash, 0.014)
        for k in range(1, int(n)):
            y = -L / 2 + L * k / n
            ga.criar_curva("NoY", v3.tracejado([(-L / 2, y, 0.012), (L / 2, y, 0.012)], False, 0.22, 0.6), mat_dash, 0.014)
    dinam = []

    def atualizar(fase):
        v3.remover(dinam)
        c = math.cos(TAU * fase) if movimento else math.cos(TAU * instante)
        F = lambda u, v: (u, v, amplitude * c * math.sin(m * math.pi * (u + L / 2) / L) * math.sin(n * math.pi * (v + L / 2) / L))
        dinam.append(v3.malha_param("Membrana", F, -L / 2, L / 2, -L / 2, L / 2, 64, 64))

    atualizar(fase)
    proxy = m3._caixa((L + 0.8, L + 0.8, 2 * amplitude + 0.8), (0, 0, 0))
    return proxy, atualizar


def cena_preview():
    co.limpar_cena()
    proxy, _ = membrana_modos()
    co.mundo()
    co.luzes()
    co.camera_enquadrada(co.cantos([proxy]), azimute=-35, elevacao=30, margem=0.08)
    co.render(co.OUT / "calculo_b_v1.png")


if __name__ == "__main__":
    cena_preview()

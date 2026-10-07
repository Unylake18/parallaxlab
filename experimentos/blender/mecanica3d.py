"""Paisagem de potencial e giroscópio (Mecânica 4.8 e 4.11) e orbital atômico (Física moderna 7.11) — estudo 20 (sandbox).

Paisagem: pista de vidro com o perfil U(x), reta violeta de energia E, bola neutra que oscila (energia conservada) e a barra
de energia cinética K = E − U (violeta). Giroscópio: rotor que gira em torno do próprio eixo enquanto o eixo precessiona;
L e o torque em branco. Orbital: nuvem de pontos da densidade de probabilidade, em dois tons de azul pelo sinal de ψ.
fase de 0 a 1 = um ciclo (período; volta da precessão; volta do orbital).
"""

import bisect
import math
import random
import sys
from pathlib import Path

import bmesh
import bpy
from mathutils import Euler, Vector

sys.path.insert(0, str(Path(__file__).resolve().parent))
import casca_oca as co  # noqa: E402
import cilindro_macico as cm  # noqa: E402
import gaussiana as ga  # noqa: E402
import vetores3d as v3  # noqa: E402


def _mat_dash():
    return co._material("TracoMec", {"cor": "gaussiana", "emissao": 1.8, "rugosidade": 0.4})


def _caixa(escala, local):
    bpy.ops.mesh.primitive_cube_add(size=1, location=local)
    o = bpy.context.active_object
    o.name = "ProxyEnquadramento"
    o.scale = escala
    bpy.ops.object.transform_apply(scale=True)
    o.hide_render = True
    return o


# ── paisagem de potencial ────────────────────────────────────────────────────
PERFIS = {
    "poco_simples": lambda x: 0.5 * x * x,
    "poco_duplo": lambda x: 0.55 * (x * x - 1.0) ** 2,
    "barreira": lambda x: 1.6 * math.exp(-x * x / 0.6),
}


def _com_paredes(U, L):
    """Confina a bola: paredes suaves em ±L (potencial vai a cima), para a órbita ser periódica."""
    return lambda x: U(x) + 6.0 * (abs(x) / L) ** 10


def _orbita(U, E, x_inicio, L, n=900):
    """Integra a órbita de energia E a partir do ponto de retorno x_inicio (Verlet, m = 1) até voltar a ele: a velocidade
    inverte duas vezes (no ponto de retorno oposto e de volta ao inicial). Devolve (T, n posições em tempos iguais)."""
    dU = lambda x: (U(x + 1e-4) - U(x - 1e-4)) / 2e-4
    dt = 1e-3
    x, v = x_inicio, 0.0
    a = -dU(x)
    traj, t, inversoes = [x], 0.0, 0
    for _ in range(600000):
        x += v * dt + 0.5 * a * dt * dt
        a_novo = -dU(x)
        v_novo = v + 0.5 * (a + a_novo) * dt
        if v * v_novo < 0:
            inversoes += 1
        v, a, t = v_novo, a_novo, t + dt
        traj.append(x)
        if inversoes >= 2:
            break
    else:
        raise RuntimeError("a órbita não fechou: energia ou perfil inadequados")
    Nt = len(traj) - 1
    return t, [traj[int(round(i / n * Nt)) % (Nt + 1)] for i in range(n)]


def criar_paisagem(tipo="poco_duplo", energia=0.35, lado=0, L=2.6, largura=1.2, movimento=0, fase=0.0, raio_bola=0.14):
    """Pista com o perfil de energia potencial, reta E e a bola. `lado` = -1/+1 escolhe o poço do início (poço duplo);
    com energia acima da barreira a bola passa pelos dois poços."""
    U0 = PERFIS[tipo]
    U = _com_paredes(U0, L)
    F = lambda u, v: (u, v, U(u))
    umax = max(2.0, energia * 1.5 + 0.9)
    xv = max(x for x in [-L + 2 * L * i / 2000 for i in range(2001)] if U(x) <= umax)      # trecho visível da pista
    pista = v3.malha_param("Pista", F, -xv, xv, -largura / 2, largura / 2, 140, 4, espessura=0.05)
    v3.curva("Perfil", [([(x, -largura / 2 - 0.01, U(x) + 0.01) for x in [-xv + 2 * xv * i / 220 for i in range(221)]], False)],
             v3.material_cor("PerfilU", "fonte_contorno", 1.4), 0.03)
    xs = [-L + 2 * L * i / 800 for i in range(801)]
    dentro = [x for x in xs if U(x) <= energia]
    if not dentro:
        raise ValueError("energia abaixo do mínimo de U")
    if tipo == "poco_duplo" and energia < U(0.0):               # energia abaixo da barreira: escolhe o poço
        lado_i = -1 if lado <= 0 else 1
        cand = [x for x in dentro if (x < 0) == (lado_i < 0)]
        x_ret = min(cand) if lado_i < 0 else max(cand)
    else:
        x_ret = min(dentro)
    T, tr = _orbita(U, energia, x_ret, L)
    ga.criar_curva("EnergiaE", v3.tracejado([(-xv, -largura / 2 - 0.01, energia), (xv, -largura / 2 - 0.01, energia)], False, 0.22, 0.6),
                   _mat_dash(), 0.015)
    mat_b = v3.material_degrade("Bola", "texto_neutro", "fonte_contorno", 1.0, 0.7)
    bola = v3.esfera_pt((0, 0, 0), raio_bola, mat_b, "Bola")
    kbarra = []
    mat_d = _mat_dash()

    def atualizar(fase):
        x = tr[int(round((fase % 1.0) * len(tr))) % len(tr)]
        z = U(x)
        bola.location = (x, 0.0, z + raio_bola)
        v3.remover(kbarra)
        if energia - z > 0.02:                                      # barra de K = E − U entre a bola e a reta de energia
            kbarra.append(ga.criar_curva("BarraK", v3.tracejado([(x, 0, z + 2 * raio_bola + 0.02), (x, 0, energia)], False, 0.14, 0.6), mat_d, 0.02))

    atualizar(fase)
    proxy = _caixa((2 * xv + 0.6, largura + 0.4, umax + 0.4), (0, 0, umax / 2 - 0.1))
    return proxy, atualizar


# ── giroscópio ───────────────────────────────────────────────────────────────
def criar_giroscopio(inclinacao_graus=38.0, comprimento_eixo=1.9, raio_rotor=0.8, voltas_spin=7, vetores=1, rastro=1,
                     movimento=0, fase=0.0):
    """Pião/giroscópio com o pivô na origem. O eixo precessiona em torno de z (fase 0 a 1 = uma volta) e o rotor dá
    `voltas_spin` voltas em torno do próprio eixo por volta de precessão. L (momento angular) em branco ao longo do eixo e
    o torque do peso (branco) tangente ao cone."""
    alfa = math.radians(inclinacao_graus)
    d = comprimento_eixo
    mat_v = v3.material_cor("VetorFisico", "vetor_fisico", co.ST["materiais"]["vetor_fisico"]["emissao"])
    prec = bpy.data.objects.new("Precessao", None)
    bpy.context.collection.objects.link(prec)
    incl = bpy.data.objects.new("Inclinacao", None)
    bpy.context.collection.objects.link(incl)
    incl.parent = prec
    incl.rotation_euler = (0.0, alfa, 0.0)
    spin = bpy.data.objects.new("Spin", None)
    bpy.context.collection.objects.link(spin)
    spin.parent = incl
    spin.location = (0, 0, d)
    # haste do eixo (do pivô ao rotor, um pouco além)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.04, depth=d + 0.55, vertices=24)
    haste = bpy.context.active_object
    haste.name = "EixoRotor"
    bpy.ops.object.shade_smooth()
    haste.data.materials.append(co._material("Haste", {"cor": "fonte_contorno", "emissao": 0.9, "rugosidade": 0.35}))
    haste.parent = incl
    haste.location = (0, 0, (d + 0.55) / 2 - 0.0)
    # rotor: disco de vidro com 4 raios claros para a rotação se ler
    rotor = cm.criar_corpo_macico(raio_rotor, 0.22, 64)
    rotor.rotation_euler = (0, math.radians(90), 0)
    bpy.context.view_layer.objects.active = rotor
    rotor.select_set(True)
    bpy.ops.object.transform_apply(rotation=True)
    cm.material_vidro(rotor)
    rotor.parent = spin
    rotor.location = (0, 0, 0)
    # (o cilindro foi criado com o eixo em X; o giro dele em Z precisa do eixo em Z)
    rotor.rotation_euler = (0, math.radians(90), 0)
    bpy.ops.object.select_all(action="DESELECT")
    mat_r = v3.material_cor("RaioRotor", "fonte_contorno", 1.4)
    for k in range(4):
        a = math.pi * k / 4
        c = ga.criar_curva("RaioRotor", [([(-raio_rotor * 0.96 * math.cos(a), -raio_rotor * 0.96 * math.sin(a), 0.115),
                                           (raio_rotor * 0.96 * math.cos(a), raio_rotor * 0.96 * math.sin(a), 0.115)], False)], mat_r, 0.025)
        c.parent = spin
    # base e pivô
    bpy.ops.mesh.primitive_cylinder_add(radius=0.5, depth=0.12, vertices=48, location=(0, 0, -0.4))
    base = bpy.context.active_object
    base.name = "Base"
    cm.material_vidro(base, base=0.25, ganho=0.5, brilho_borda=1.6)
    v3.esfera_pt((0, 0, 0), 0.09, v3.material_cor("Pivo", "texto_neutro", 1.4), "Pivo")
    if rastro:
        R = d * math.sin(alfa)
        circ = [(R * math.cos(2 * math.pi * k / 120), R * math.sin(2 * math.pi * k / 120), d * math.cos(alfa)) for k in range(121)]
        ga.criar_curva("Rastro", v3.tracejado(circ[:-1], True, 0.26, 0.6), _mat_dash(), 0.014)
        ga.criar_curva("Cone", v3.tracejado([(0, 0, 0), circ[0]], False, 0.2, 0.6), _mat_dash(), 0.01)
    dinam = []

    def atualizar(fase):
        phi = 2 * math.pi * fase
        prec.rotation_euler = (0, 0, phi)
        spin.rotation_euler = (0, 0, 2 * math.pi * voltas_spin * fase)
        if vetores:
            v3.remover(dinam)
            eixo = Vector((math.sin(alfa) * math.cos(phi), math.sin(alfa) * math.sin(phi), math.cos(alfa)))
            dinam.append(v3.seta(tuple(eixo * (d + 0.5)), tuple(eixo * 1.0), mat_v, 1.0))                      # L ao longo do eixo
            tang = Vector((-math.sin(phi), math.cos(phi), 0.0))
            cm_ = eixo * d
            dinam.append(v3.seta(tuple(cm_), tuple(tang * 0.9), mat_v, 0.9))                                    # torque do peso (tangente)
            dinam.append(v3.seta(tuple(cm_), (0, 0, -0.9), mat_v, 0.9))                                        # peso

    atualizar(fase)
    proxy = _caixa((3.2, 3.2, 3.6), (0, 0, 1.2))
    return proxy, atualizar


# ── orbital atômico ─────────────────────────────────────────────────────────
def _amostra_orbital(orb, n, semente):
    rng = random.Random(semente)
    pts = []

    def R_(r):
        if orb == "1s":
            return math.exp(-r)
        if orb == "2s":
            return (2 - r) * math.exp(-r / 2)
        if orb in ("2p",):
            return r * math.exp(-r / 2)
        if orb == "3d":
            return r * r * math.exp(-r / 3)
        raise ValueError(orb)

    def Y_(c):                          # c = cos θ
        if orb in ("1s", "2s"):
            return 1.0
        if orb == "2p":
            return c
        return 3 * c * c - 1.0

    rmax = {"1s": 7.0, "2s": 16.0, "2p": 16.0, "3d": 28.0}[orb]
    # densidade radial-angular (ψ² r²) com r uniforme em [0, rmax] e cosθ uniforme: aceita com prob. dens/dens_max
    dmax = max((R_(rmax * i / 400) * Y_(c)) ** 2 * (rmax * i / 400) ** 2 for i in range(1, 401) for c in (-1, -0.7, -0.4, 0, 0.4, 0.7, 1))
    tent = 0
    while len(pts) < n and tent < 6_000_000:
        tent += 1
        r = rmax * rng.random()
        c = rng.uniform(-1, 1)
        psi = R_(r) * Y_(c)
        if rng.random() * dmax <= psi * psi * r * r:
            ph = rng.uniform(0, 2 * math.pi)
            s = math.sqrt(1 - c * c)
            pts.append(((r * s * math.cos(ph), r * s * math.sin(ph), r * c), psi > 0))
    return pts


def criar_orbital(orbital="2p", n_pontos=5000, escala=None, tamanho_ponto=0.034, semente=7, movimento=0, fase=0.0, eixo=1):
    """Nuvem de pontos de |ψ|² (um orbital do hidrogênio: 1s, 2s, 2p ou 3d), em dois tons de azul pelo sinal de ψ, com o
    núcleo branco no centro. Com movimento a nuvem gira uma volta em torno de z."""
    escala = escala or {"1s": 0.55, "2s": 0.3, "2p": 0.36, "3d": 0.2}[orbital]
    pts = _amostra_orbital(orbital, int(n_pontos), semente)
    meshes = []
    for sinal, cor in ((True, "fonte_contorno"), (False, "fonte_fisica")):
        bm = bmesh.new()
        for (p, pos) in pts:
            if pos != sinal:
                continue
            c = Vector(p) * escala
            bmesh.ops.create_icosphere(bm, subdivisions=1, radius=tamanho_ponto, matrix=__import__("mathutils").Matrix.Translation(c))
        me = bpy.data.meshes.new("Nuvem")
        bm.to_mesh(me)
        bm.free()
        o = bpy.data.objects.new("Nuvem", me)
        bpy.context.collection.objects.link(o)
        o.data.materials.append(v3.material_cor("Nuvem_" + cor, cor, 2.2))
        meshes.append(o)
    nuc = v3.esfera_pt((0, 0, 0), 0.09, v3.material_cor("Nucleo", "texto_neutro", 2.4), "Nucleo")
    pai = bpy.data.objects.new("Giro", None)
    bpy.context.collection.objects.link(pai)
    for o in meshes + [nuc]:
        o.parent = pai
    if eixo:
        mat = v3.material_cor("EixoOrb", "texto_neutro", 0.8)
        for dvec in ((0, 0, 1),):
            ga.criar_curva("EixoZ", v3.tracejado([tuple(-3.2 * c for c in dvec), tuple(3.2 * c for c in dvec)], False, 0.22, 0.6), mat, 0.01)

    def atualizar(fase):
        pai.rotation_euler = (0, 0, 2 * math.pi * fase) if movimento else (0, 0, 0)

    atualizar(fase)
    ext = 3.4
    proxy = _caixa((2 * ext, 2 * ext, 2 * ext), (0, 0, 0))
    return proxy, atualizar


def cena_preview():
    co.limpar_cena()
    proxy, _ = criar_paisagem("poco_duplo", 0.35, fase=0.1)
    co.mundo()
    co.luzes()
    co.camera_enquadrada(co.cantos([proxy]), azimute=-60, elevacao=14, margem=0.08)
    co.render(co.OUT / "mecanica3d_v1.png")


if __name__ == "__main__":
    cena_preview()

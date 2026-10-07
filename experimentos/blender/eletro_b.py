"""Eletrostática, fila B (6.1, 6.2, 6.5) — estudo 24 (sandbox).

Cargas pontuais e forças de Coulomb, dipolo elétrico com o campo, linhas de campo em 3D e condutor com cavidade. Sinal da carga =
ESCULPIDO (+/−); campo E = ciano; forças e momento de dipolo = branco; construções = violeta tracejado. fase 0 a 1 = um ciclo
(loop). Os valores de q, k e as fórmulas são do Manim.
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
import gaussiana as ga  # noqa: E402
import oscilacoes as osc  # noqa: E402
import vetores3d as v3  # noqa: E402

VF = co.ST["materiais"]["vetor_fisico"]


def _mat_vf():
    return v3.material_cor("VetorFisico", VF["cor"], VF["emissao"])


def _mat_E():
    return v3.material_cor("CampoE", "campo_eletrico", 1.6)


def _mat_dash():
    return co._material("TracoEB", {"cor": "gaussiana", "emissao": 1.8, "rugosidade": 0.4})


def _caixa(escala, local):
    o = osc._caixa("ProxyEnquadramento", escala, local)
    o.hide_render = True
    return o


def _coulomb(pos, q):
    """Campo em cada ponto ou força em cada carga: E(p) = Σ q (p − r)/|p − r|³."""
    def E(p):
        s = Vector((0, 0, 0))
        for r, qq in zip(pos, q):
            d = Vector(p) - r
            L = max(d.length, 1e-6)
            s += qq * d / L ** 3
        return s
    return E


# ── cargas pontuais e forças de Coulomb ──────────────────────────────────────
def cargas_pontuais(config="duas", sinais=(1, -1, 1), distancia=2.6, raio=0.3, forcas=1, movimento=0, fase=0.0):
    """Duas ou três cargas com sinal esculpido e as forças de Coulomb sobre cada uma (setas brancas, módulo ∝ |F|·d²).
    Com movimento a carga 2 vai e volta ao longo do eixo X (a força varia com 1/r²), o loop fecha."""
    n = 2 if config == "duas" else 3
    q = [int(math.copysign(1, s)) for s in sinais[:n]]
    d0 = distancia
    base = [Vector((-d0 / 2, 0, 0)), Vector((d0 / 2, 0, 0)), Vector((0, d0 * math.sqrt(3) / 2, 0))][:n]
    if n == 3:
        base = [b - Vector((0, d0 * math.sqrt(3) / 6, 0)) for b in base]
    glifos = []
    esf = [v3.carga_sinal(tuple(base[i]), q[i], raio, glifos) for i in range(n)]
    mat_vf = _mat_vf()
    dinam = []

    def atualizar(fase):
        pos = [b.copy() for b in base]
        if movimento:
            pos[1] = Vector((d0 / 2 + 0.6 * math.sin(2 * math.pi * fase) * d0 / 2 * 0.9, 0, 0))
        for i in range(n):
            esf[i].location = tuple(pos[i])
            glifos[i].location = tuple(pos[i])
        v3.remover(dinam)
        if forcas:
            for i in range(n):
                F = Vector((0, 0, 0))
                for j in range(n):
                    if j != i:
                        dv = pos[i] - pos[j]
                        F += q[i] * q[j] * dv / max(dv.length, 1e-6) ** 3
                comp = min(2.8, 1.2 * F.length * d0 * d0)
                if comp > 0.05:
                    dinam.append(v3.seta(tuple(pos[i] + F.normalized() * raio * 0.9), tuple(F.normalized() * comp), mat_vf, comp))

    atualizar(fase)
    proxy = _caixa((d0 * 1.6 + 1.4, d0 * 1.0 + 1.0 if n == 3 else 1.6, 1.2), (0, d0 * 0.0 if n == 3 else 0, 0))
    return proxy, atualizar, glifos


# ── dipolo elétrico ──────────────────────────────────────────────────────────
def dipolo_eletrico(distancia=1.8, n_grade=8, extensao=2.7, raio=0.3, movimento=0, angulo_graus=0.0, fase=0.0, momento=1):
    """Dipolo (+q e −q) com o campo E (setas ciano numa grade no plano da figura) e o momento de dipolo p (branco, de − para +).
    Com movimento o dipolo gira uma volta em torno de Z e o campo acompanha."""
    d = distancia
    glifos = []
    mat_E, mat_vf = _mat_E(), _mat_vf()
    pos0 = [Vector((d / 2, 0, 0)), Vector((-d / 2, 0, 0))]
    esf = [v3.carga_sinal(tuple(pos0[0]), 1, raio, glifos), v3.carga_sinal(tuple(pos0[1]), -1, raio, glifos)]
    pts = [(-extensao + 2 * extensao * i / (n_grade - 1), -extensao * 0.75 + 1.5 * extensao * j / (n_grade - 1)) for i in range(n_grade) for j in range(n_grade)]
    setas = [v3.seta((x, y, 0), (1, 0, 0), mat_E, 0.5) for (x, y) in pts]
    p_arrow = v3.seta((0, 0, 0), (1, 0, 0), mat_vf, 1.0) if momento else None

    def atualizar(fase):
        th = 2 * math.pi * fase + math.radians(angulo_graus) if movimento else math.radians(angulo_graus)
        u = Vector((math.cos(th), math.sin(th), 0))
        pos = [u * (d / 2), u * (-d / 2)]
        for i in range(2):
            esf[i].location = tuple(pos[i])
            glifos[i].location = tuple(pos[i])
        E = _coulomb(pos, [1, -1])
        for s, (x, y) in zip(setas, pts):
            p = Vector((x, y, 0))
            if min((p - pos[0]).length, (p - pos[1]).length) < raio + 0.35:
                v3.ajustar_seta(s, (x, y, 0), (0, 0, 0))
                continue
            e = E(p)
            L = 0.32 + 0.6 * (e.length / (e.length + 0.35))
            v3.ajustar_seta(s, tuple(p - e.normalized() * L * 0.5), tuple(e.normalized() * L), L)
        if p_arrow is not None:
            v3.ajustar_seta(p_arrow, tuple(u * (-d / 2 - 0.05) + Vector((0, 0, 0.45))), tuple(u * (d + 0.4)), d + 0.4)

    atualizar(fase)
    proxy = _caixa((2 * extensao + 0.8, 1.5 * extensao + 0.8, 1.2), (0, 0, 0))
    return proxy, atualizar, glifos


# ── linhas de campo em 3D ────────────────────────────────────────────────────
def _linha_de_campo(E, inicio, parar, passo=0.06, maxpassos=900):
    """Integra x' = E/|E| (RK4) a partir de `inicio` até `parar(p)` ser verdadeiro; devolve a polilinha."""
    p = Vector(inicio)
    pts = [p.copy()]
    f = lambda x: (E(x).normalized() if E(x).length > 1e-9 else Vector((0, 0, 0)))
    for _ in range(maxpassos):
        k1 = f(p)
        k2 = f(p + k1 * passo / 2)
        k3 = f(p + k2 * passo / 2)
        k4 = f(p + k3 * passo)
        p = p + (k1 + 2 * k2 + 2 * k3 + k4) * passo / 6
        pts.append(p.copy())
        if parar(p):
            break
    return pts


def linhas_de_campo_3d(tipo="dipolo", n_linhas=16, distancia=2.0, raio_carga=0.3, setas=1, movimento=0, fase=0.0, n_contas=3):
    """Linhas de campo (curvas ciano) saindo da carga + e chegando à carga − (dipolo) ou indo ao infinito (carga pontual), com
    setas de sentido e, com movimento, contas que percorrem as linhas (sentido do campo). As cargas têm o sinal esculpido."""
    d = distancia / 2
    glifos = []
    if tipo == "carga_pontual":
        pos, q = [Vector((0, 0, 0))], [1]
    else:
        pos, q = [Vector((d, 0, 0)), Vector((-d, 0, 0))], [1, -1]
    for p_, s_ in zip(pos, q):
        v3.carga_sinal(tuple(p_), s_, raio_carga, glifos)
    E = _coulomb(pos, q)
    mat_l = _mat_E()
    mat_a = v3.material_cor("SetaLinha", "campo_eletrico", 2.0)
    ext = 3.4
    linhas = []
    ouro = math.pi * (3 - math.sqrt(5))
    for k in range(int(n_linhas)):
        z = 1 - 2 * (k + 0.5) / n_linhas
        r = math.sqrt(max(0.0, 1 - z * z))
        dire = Vector((z, r * math.cos(ouro * k), r * math.sin(ouro * k)))          # eixo X como polar (alinhado ao dipolo)
        ini = pos[0] + dire * (raio_carga + 0.03)
        if tipo == "carga_pontual":
            parar = lambda p: p.length > ext
        else:
            parar = lambda p: (p - pos[1]).length < raio_carga + 0.05 or p.length > 3.4
        pts = _linha_de_campo(E, ini, parar)
        linhas.append(pts)
        ga.criar_curva("Linha", [([tuple(p) for p in pts], False)], mat_l, 0.022)
        if setas:
            for fr in (0.45,):
                i = max(1, min(len(pts) - 1, int(len(pts) * fr)))
                v3.seta(tuple(pts[i - 1]), tuple((pts[i] - pts[i - 1]).normalized() * 0.45), mat_a, 0.45)
    acums = []
    for pts in linhas:
        a = [0.0]
        for p0, p1 in zip(pts, pts[1:]):
            a.append(a[-1] + (p1 - p0).length)
        acums.append(a)
    mat_b = v3.material_degrade("ContaLinha", "texto_neutro", "campo_eletrico", 2.0, 0.7)
    contas = []
    if movimento:
        for li in range(len(linhas)):
            for c in range(int(n_contas)):
                contas.append((li, c, v3.esfera_pt((0, 0, 0), 0.06, mat_b, "Conta")))

    def atualizar(fase):
        for (li, c, o) in contas:
            a, pts = acums[li], linhas[li]
            s = ((c / n_contas + fase) % 1.0) * a[-1]
            i = max(1, min(len(a) - 1, next((k for k in range(1, len(a)) if a[k] >= s), len(a) - 1)))
            f = (s - a[i - 1]) / ((a[i] - a[i - 1]) or 1.0)
            o.location = tuple(pts[i - 1] + (pts[i] - pts[i - 1]) * f)

    atualizar(fase)
    proxy = _caixa((2 * ext * 0.8 + 0.4, 2 * ext * 0.7, 2 * ext * 0.7), (0, 0, 0))
    return proxy, atualizar, glifos


# ── condutor com cavidade ────────────────────────────────────────────────────
def _fibonacci(n, r):
    ouro = math.pi * (3 - math.sqrt(5))
    out = []
    for k in range(n):
        z = 1 - 2 * (k + 0.5) / n
        s = math.sqrt(max(0.0, 1 - z * z))
        out.append(Vector((r * s * math.cos(ouro * k), r * s * math.sin(ouro * k), r * z)))
    return out


def condutor_com_cavidade(raio_externo=1.9, raio_cavidade=1.0, n_cargas=14, raio_carga=0.14, corte=1):
    """Casca condutora esférica (corte em octante) com uma cavidade concêntrica contendo uma carga + no centro: cargas induzidas −
    na parede da cavidade e + na superfície externa (todas com sinal esculpido). Equilíbrio eletrostático: o campo no volume do
    condutor é zero (a leitura é do Manim)."""
    b, a = raio_externo, raio_cavidade
    espessura = b - a
    obj = es.criar_casca_esferica(b, espessura, 96, 48, int(corte))
    obj.name = "Condutor"
    co.material_casca(obj)
    glifos = []
    v3.carga_sinal((0, 0, 0), 1, 0.3, glifos)
    def no_corte(p):
        return bool(corte) and p.x > 0 and p.y < 0 and p.z > 0
    for p in _fibonacci(int(n_cargas), a - raio_carga * 0.4):
        if not no_corte(p):
            v3.carga_sinal(tuple(p), -1, raio_carga, glifos)
    for p in _fibonacci(int(n_cargas) + 4, b + raio_carga * 0.4):
        if not no_corte(p):
            v3.carga_sinal(tuple(p), 1, raio_carga, glifos)
    proxy = _caixa((2 * b + 1.0, 2 * b + 1.0, 2 * b + 1.0), (0, 0, 0))
    return proxy, glifos


def cena_preview():
    co.limpar_cena()
    proxy, _, gl = cargas_pontuais()
    co.mundo()
    co.luzes()
    cam = co.camera_enquadrada(co.cantos([proxy]), azimute=-30, elevacao=40, margem=0.08)
    v3.orientar_glifos(cam, gl)
    co.render(co.OUT / "eletro_b_v1.png")


if __name__ == "__main__":
    cena_preview()

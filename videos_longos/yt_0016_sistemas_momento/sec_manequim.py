"""Manequim 3D (geometria do hook do yt_0015, cena threejs/cena3d/maneq.js): poses calculadas aqui, por estado.
Unidades em metros; o Manim mostra com zoom K (vista 'frente', plano y = 0). O manequim olha para +x (esp = 1) ou −x (esp = −1)."""
from kit import *  # noqa: F401,F403

L1 = L2 = 0.46
ANK = 0.085
H_PE = 2 * L1 * math.cos(0.02) + ANK       # altura do quadril em pé
BR0 = [0.12, 0.04, 0.18]                    # braço solto


def alt_q(dobra):
    return 2 * L1 * math.cos(dobra / 2) + ANK


def lerp(a, b, u):
    return a + (b - a) * u


def lerpl(a, b, u):
    return [lerp(x, y, u) for x, y in zip(a, b)]


def pose_pe(x, esp=1, resp=0.0):
    """Em pé, respirando (resp = fase em rad)."""
    r = 0.006 * math.sin(resp)
    return {"hx": x, "hz": H_PE + r, "pes": [[x + 0.07 * esp, ANK, 0], [x - 0.05 * esp, ANK, 0]], "lam": 0.03, "cab": 0.03,
            "bracos": [BR0[:], BR0[:]], "esp": esp}


def pose_agarra(x, u, esp=1):
    """u = 0 (em pé) → 1 (braços fechados na frente do peito, segurando)."""
    p = pose_pe(x, esp)
    p["bracos"] = [lerpl(BR0, [0.28, 1.25, 1.55], u), lerpl(BR0, [0.28, 1.25, 1.55], u)]
    p["lam"] = lerp(0.03, 0.12, u)
    p["hz"] = H_PE - 0.03 * u
    p["cab"] = lerp(0.03, 0.18, u)
    return p


def pose_rebate(x, u, esp=1):
    """u: 0 em pé → 1 tronco recuando com o impacto no peito (braços abrindo)."""
    p = pose_pe(x, esp)
    b = math.sin(PI * min(1.0, u))
    p["bracos"] = [lerpl(BR0, [0.55, 0.5, 0.5], b), lerpl(BR0, [0.55, 0.5, 0.5], b)]
    p["lam"] = 0.03 - 0.16 * b
    p["cab"] = 0.03 - 0.2 * b
    return p


def pose_mira(x, ang, esp=1, recuo=0.0):
    """Segurando o rifle na altura do ombro; ang em rad acima da horizontal; recuo (0–1) joga o tronco para trás."""
    p = pose_pe(x, esp)
    p["pes"] = [[x + 0.16 * esp, ANK, 0], [x - 0.2 * esp, ANK, 0]]
    p["hz"] = alt_q(0.12)
    fl = 1.35 + 0.75 * ang
    p["bracos"] = [[0.35, fl, 0.85 - 0.2 * ang], [0.15, fl + 0.1, 0.45 - 0.1 * ang]]
    p["lam"] = -0.04 - 0.1 * recuo + 0.05 * ang
    p["cab"] = 0.1 - 0.15 * ang
    return p


def pose_andar(x, fase, esp=1, passo=0.62, sobe=0.07):
    """Ciclo de marcha: fase em ciclos (1 = dois passos). O pé de apoio fica parado no chão (atrito estático)."""
    g = []
    for i in (0, 1):
        ph = (fase + 0.5 * i) % 1.0
        if ph < 0.6:                     # apoio: o pé vai de +passo/2 a −passo/2 em relação ao quadril
            u = ph / 0.6
            dx, dz = passo * (0.5 - u), 0.0
        else:                            # balanço
            u = (ph - 0.6) / 0.4
            dx, dz = passo * (-0.5 + u), sobe * math.sin(PI * u)
        g.append([x + dx * esp, ANK + dz, -0.25 * math.sin(PI * u) if ph >= 0.6 else 0.0])
    bob = 0.018 * math.cos(4 * PI * fase)
    sw = 0.38 * math.sin(2 * PI * fase)
    return {"hx": x, "hz": alt_q(0.22) + bob, "pes": g, "lam": 0.08, "cab": 0.02,
            "bracos": [[0.1, sw, 0.3], [0.1, -sw, 0.3]], "esp": esp}


def mao(p, i):
    """Cinemática direta (igual à do maneq.js, no plano xz): posição (x, z) da ponta da mão do braço i."""
    esp, lam = p["esp"], p["lam"]
    abd, f, cot = p["bracos"][i]

    def ry(x, z, th):                                   # rotação em torno de y (convenção do three.js)
        return x * math.cos(th) + z * math.sin(th), -x * math.sin(th) + z * math.cos(th)

    def braco(th, L):
        x, z = math.sin(th) * L, -math.cos(th) * L * math.cos(abd)
        return ry(x, z, lam)
    sx, sz = ry(0.0, 0.33, lam)
    ux, uz = braco(f, 0.29)
    fx, fz = braco(f + cot, 0.32)
    return p["hx"] + esp * (sx + ux + fx), p["hz"] + 0.1 + sz + uz + fz


def boca(p, ang, s=0.0):
    """Boca do cano (e a bala s metros adiante) para o rifle nas mãos com inclinação ang."""
    x0, z0 = mao(p, 0)
    x1, z1 = mao(p, 1)
    cx, cz = (x0 + x1) / 2, (z0 + z1) / 2
    d = (p["esp"] * math.cos(ang), math.sin(ang))
    return cx + d[0] * (0.76 + s), cz + d[1] * (0.76 + s), (cx, cz)


class Manequim3D:
    """Fundo 3D com o manequim. `pose(t)` → dict de pose (extras: bola, rifle, bala, chao)."""

    def __init__(self, cena, pose, K=2.0, xt=-3.4, yc=-2.6, camx=0.0, op=1.0, seguir=False):
        self.cena, self.pose, self.seguir = cena, pose, seguir
        self.K, self.xt, self.yc, self.camx = ValueTracker(K), ValueTracker(xt), ValueTracker(yc), ValueTracker(camx)
        self.f3d = Fundo3D(cena, "manequim", self.estado, op=op)

    def estado(self, t):
        e = dict(self.pose(t))
        cx = e["hx"] if self.seguir else self.camx.get_value()
        e["cam"] = cam_frente(K=self.K.get_value(), xc=self.xt.get_value(), yc=self.yc.get_value(), camx=cx, fov=16, el=3)
        return e

    def m(self, x, z, y=0.0):
        """Ponto do mundo (m) → Manim no quadro corrente."""
        return mapa_frente(self.f3d.e["cam"], x, z, y)

    def pts(self):
        e = self.f3d.e
        x, esp = e["hx"], e["esp"]
        return {"quadril": self.m(x, e["hz"]), "peito": self.m(x + 0.1 * esp, e["hz"] + 0.42), "cabeca": self.m(x, e["hz"] + 0.86),
                "pes": self.m(x, 0.0), "pe_frente": self.m(max(p[0] for p in e["pes"]) if esp > 0 else min(p[0] for p in e["pes"]), 0.0),
                "maos": self.m(x + 0.42 * esp, e["hz"] + 0.5)}

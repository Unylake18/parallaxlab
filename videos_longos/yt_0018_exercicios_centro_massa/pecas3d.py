"""yt_0017 — as quatro peças 3D (threejs/cena3d/cm3d.js) do lado Manim: física, câmera e estado por quadro, e os pontos em coordenadas
do Manim (projeta3d, a mesma câmera do b3d.js). As camadas Manim leem sempre `f3d.e` (o estado do próprio quadro), nunca self.t.

Haltere3D    — 1 kg + 3 kg, separação 4; gira (ang) com câmera oblíqua → para com a haste horizontal na vista frontal (lente longa);
               apoio triangular desliza e a haste balança até equilibrar no ⊕ (tilt).
Granada3D    — v3: granada de fragmentação no campo de provas (campo.js): (30; 40) m/s, explosão no topo em três cacos do próprio corpo
               (volumes ∝ massas), momento relativo de 30 kg·m/s; cada caco para ao tocar o chão. O ⊕ é sempre calculado dos pedaços.
Explosao3D   — a mesma granada no espaço (céu sem piso): corpo a V0 se parte nos mesmos cacos (90°, 210°, 330°; uᵢ = c/mᵢ). Câmera
               do chão (fixa, com dolly) ou presa ao CM (seg = 1).
Semiesfera3D — R = 1,8, fatia dz = 0,14 em fz (tracker), câmera fixa ~16° acima.
"""
from kit import *  # noqa: F401,F403

MS = (2.0, 1.0, 1.5)
MT = sum(MS)
DIRS = [np.array([math.cos(math.radians(a)), math.sin(math.radians(a))]) for a in (90, 210, 330)]


def _hermite(m0):
    """Rate func com derivada inicial m0 e final 0 (continua a velocidade de um giro e para)."""
    return lambda s: (s ** 3 - 2 * s ** 2 + s) * m0 + (-2 * s ** 3 + 3 * s ** 2)


# ── haltere ──────────────────────────────────────────────────────────────────────────────────────────────
class Haltere3D:
    M1, M2, SEP = 1.0, 3.0, 4.0
    X1, X2 = -SEP * M2 / (M1 + M2), SEP * M1 / (M1 + M2)             # −3 e +1
    R1, R2 = 0.8 * (M1 / 3) ** (1 / 3), 0.8 * (M2 / 3) ** (1 / 3)
    OBL = dict(az=-62.0, el=34.0, fov=16.0)
    FR = dict(az=-90.0, el=0.0, fov=4.0)

    def __init__(self, cena, K=1.06, cm=P3(-2.1, 0.35), op=1.0):
        self.cena, self.K, self.cmt = cena, K, cm
        self.ang, self.u, self.tilt = ValueTracker(0.0), ValueTracker(0.0), ValueTracker(0.0)
        self.ax, self.av, self.ab = ValueTracker(-1.6), ValueTracker(0.0), ValueTracker(0.3)
        self.f3d = Fundo3D(cena, "hal", self.estado, op=op)

    def cam(self):
        u = suave(self.u.get_value())
        c = {k: self.OBL[k] + (self.FR[k] - self.OBL[k]) * u for k in self.OBL}
        return cam_obl(c["az"], c["el"], (0, 0, 0), K=self.K, xc=self.cmt[0], yc=self.cmt[1], fov=c["fov"])

    def estado(self, t):
        return r4({"hal": {"x": 0.0, "y": 0.0, "ang": self.ang.get_value(), "tilt": self.tilt.get_value(), "vis": 1},
                   "apoio": [self.ax.get_value(), int(self.av.get_value() > 0.5), self.ab.get_value()], "cam": self.cam()})

    def mundo(self, x, e=None):
        e = e or self.f3d.e
        a, b = e["hal"]["ang"], e["hal"]["tilt"]
        p = np.array([x * math.cos(a), x * math.sin(a), 0.0])
        return np.array([p[0] * math.cos(b), p[1], -p[0] * math.sin(b)])          # R_y(tilt): +x desce com tilt > 0

    def p(self, x):
        """Ponto da haste a x do CM (Manim, quadro corrente)."""
        return projeta3d(self.f3d.e["cam"], self.mundo(x))

    def raio(self, r, x=0.0):
        c = self.f3d.e["cam"]
        q = self.mundo(x)
        return float(np.linalg.norm(projeta3d(c, q + np.array([0, 0, r])) - projeta3d(c, q)))

    def girar(self, omega=1.6):
        t0, a0 = self.cena.clk.get_value(), self.ang.get_value()
        self.omega = omega
        self.ang.add_updater(lambda m: m.set_value(a0 + omega * (self.cena.clk.get_value() - t0)))

    def parar(self, dur=2.6):
        """Desacelera até um múltiplo exato de 2π (haste horizontal, leve à esquerda) com a câmera oblíqua parada; depois a câmera desce
        para a frontal com a haste já parada ao longo de x: o ângulo entre a haste e a linha de visada fica sempre ≥ 62° (nunca uma bola
        atrás da outra)."""
        self.ang.clear_updaters()
        a0, w = self.ang.get_value(), self.omega
        h = dur * 0.7
        af = 2 * PI * math.ceil((a0 + 0.5 * w * h) / (2 * PI))
        m0 = w * h / (af - a0)
        self.cena.play(self.ang.animate(rate_func=_hermite(m0)).set_value(af), run_time=h)
        self.ang.set_value(af)
        self.cena.play(self.u.animate(rate_func=linear).set_value(1.0), run_time=dur * 0.45)

    def apoiar(self, dur=1.6, balanco=2.6):
        """Apoio entra por baixo, sobe até tocar a haste sob o ⊕; a haste balança (amortecido) e se acomoda."""
        self.av.set_value(1.0)
        self.cena.play(self.ax.animate.set_value(0.0), run_time=dur)
        self.cena.play(self.ab.animate.set_value(0.0), run_time=0.5)
        t0 = self.cena.clk.get_value()
        self.tilt.add_updater(lambda m: m.set_value(0.11 * math.exp(-(self.cena.clk.get_value() - t0) / 0.75)
                                                    * math.sin(5.0 * (self.cena.clk.get_value() - t0))))
        self.cena.wait(balanco)
        self.tilt.clear_updaters()
        self.tilt.set_value(0.0)


# ── granada de fragmentação (v3: threejs/cena3d/campo.js) ─────────────────────────────────────────────────
# Os três cacos são pedaços do próprio corpo (volumes ∝ massas); o ponto físico de cada caco é o centroide da malha. CEN/REQ vêm das
# medidas exportadas pelo Three.js (granada_medidas.json): centroide de cada caco no corpo (x, profundidade, z) e raio equivalente.
MED = json.loads((DIR3D / "cena3d" / "granada_medidas.json").read_text(encoding="utf-8"))
CEN = [np.array(c) for c in MED["cen"]]
REQ, REQ_CORPO = MED["req"], MED["req_corpo"]
OMEGA = [2 * PI * w for w in (0.9, 1.7, 1.3)]       # giro de cada caco (voltas/s de física: o leve gira mais rápido)
KAPPA = 5.0                                          # o giro morre depois do pouso (girando até parar)
T_SEP = 0.25                                         # s de física para o caco sair do encaixe no corpo


def sep(dx):
    return suave(dx / T_SEP) if dx > 0 else 0.0


def calor(dx):
    return math.exp(-dx / 0.35) if dx >= 0 else 0.0


def giro(k, dx, dx_pouso=None):
    """Ângulo do caco k (rad) dx s depois da explosão; depois do pouso o giro decai até parar."""
    if dx <= 0:
        return 0.0
    if dx_pouso is None or dx <= dx_pouso:
        return OMEGA[k] * dx
    return OMEGA[k] * dx_pouso + OMEGA[k] / KAPPA * (1 - math.exp(-KAPPA * (dx - dx_pouso)))


class Granada3D:
    """Campo de provas (gra): (30; 40) m/s, explosão no topo em 2, 1 e 1,5 kg com momento relativo de 30 kg·m/s a 90°, 210° e 330°;
    cada caco para ao tocar o chão. Câmera frontal levemente elevada (el 6°) para o piso ler como grade. `seg` = câmera presa à
    granada (H1); `w` = troca de escala: 0 = escala de câmera (perto), 1 = tamanho de tela constante (R_TELA, gráfico inteiro)."""
    S, G = 20.0, 9.8
    V0 = np.array([30.0, 40.0])
    TE = 40.0 / 9.8
    PRE = 30.0
    EL, ESC_PERTO, R_TELA = 6.0, 0.31, 0.2

    def __init__(self, cena, K=1.0, camx=6.12, yc=-2.58, op=1.0, w=1.0):
        self.cena = cena
        self.tau = ValueTracker(0.0)
        self.K, self.camx, self.yc = ValueTracker(K), ValueTracker(camx), ValueTracker(yc)
        self.seg, self.xseg, self.yseg = ValueTracker(0.0), ValueTracker(0.0), ValueTracker(-0.3)
        self.w, self.onda, self.brilho, self.fant = ValueTracker(w), ValueTracker(-1.0), ValueTracker(0.0), ValueTracker(0.0)
        self.f3d = Fundo3D(cena, "gra", self.estado, op=op)
        self.pe = self.V0 * self.TE + np.array([0, -0.5 * self.G * self.TE ** 2])          # (122,45; 81,63)
        self.vf = [np.array([self.V0[0], 0.0]) + d * self.PRE / m for m, d in zip(MS, DIRS)]
        self.ttoque = [self._toque(v) for v in self.vf]                                     # 4,082 + (5,890; 2,829; 3,187)

    def trackers(self):
        return [self.tau, self.K, self.camx, self.yc, self.seg, self.xseg, self.yseg, self.w, self.onda, self.brilho, self.fant]

    def _toque(self, v):
        a, b, c = -0.5 * self.G, v[1], self.pe[1]
        return self.TE + (-b - math.sqrt(b * b - 4 * a * c)) / (2 * a)

    def ideal(self, tau):
        return self.V0 * tau + np.array([0.0, -0.5 * self.G * tau * tau])

    def fis(self, tau):
        """(corpo | None, fragmentos | None, parados, CM, V_cm) em metros. Fragmento parado fica onde tocou."""
        if tau < self.TE:
            p = self.ideal(tau)
            return p, None, None, p, self.V0 + np.array([0, -self.G * tau])
        fr, vs, par = [], [], []
        for v, tt in zip(self.vf, self.ttoque):
            s = min(tau, tt) - self.TE
            fr.append(self.pe + v * s + np.array([0, -0.5 * self.G * s * s]))
            par.append(tau >= tt)
            vs.append(np.zeros(2) if tau >= tt else v + np.array([0, -self.G * s]))
        cm = sum(m * p for m, p in zip(MS, fr)) / MT
        return None, fr, par, cm, sum(m * v for m, v in zip(MS, vs)) / MT

    def ang(self, k, tau):
        return giro(k, tau - self.TE, self.ttoque[k] - self.TE)

    def cam(self):
        K, s = self.K.get_value(), suave(self.seg.get_value())
        tau = self.tau.get_value()
        p = self.fis(tau)[3]
        cx = (1 - s) * self.camx.get_value() + s * p[0] / self.S
        xc = s * self.xseg.get_value()
        c0 = dict(cam_frente(K=K, xc=xc, yc=0.0, camx=cx, fov=16, el=self.EL), near=0.25, far=700)
        yseg = self.yseg.get_value() - projeta3d(c0, (p[0] / self.S, 0.0, p[1] / self.S))[1]
        c0["yc"] = (1 - s) * self.yc.get_value() + s * yseg
        return c0

    def esc(self, K):
        w = suave(self.w.get_value())
        return (1 - w) * self.ESC_PERTO + w * self.R_TELA / (K * REQ_CORPO)

    def fantasmas(self, tau):
        """Fotos de 0,5 em 0,5 s (1 em 1 s no close): a granada inteira antes da explosão; cada caco até o pouso (k, x, z, ângulo)."""
        out = []
        perto = suave(self.w.get_value()) < 0.5                         # v4: no close, só a cada 1 s (a cada 0,5 s só no gráfico inteiro)
        for j in range(1, int(tau / 0.5 + 1e-9) + 1):
            if perto and j % 2:
                continue
            tg = 0.5 * j
            if tg < self.TE:
                p = self.ideal(tg)
                out.append([-1, p[0] / self.S, p[1] / self.S, 0.0])
            else:
                fr = self.fis(tg)[1]
                for k, (p, tt) in enumerate(zip(fr, self.ttoque)):
                    if tg <= tt:
                        out.append([k, p[0] / self.S, p[1] / self.S, self.ang(k, tg)])
        return out

    def estado(self, t):
        tau = self.tau.get_value()
        cam = self.cam()
        esc = self.esc(cam["K"])
        corpo, fr, _, _, _ = self.fis(tau)
        dx = tau - self.TE
        gr = {"esc": esc, "chao": 1, "marco": math.exp(-((tau - 0.3) / 0.15) ** 2), "onda": self.onda.get_value(),
              "brilho": self.brilho.get_value() * (math.exp(-dx / 0.3) if dx > 0 else 1.0)}
        if corpo is not None:
            gr.update(cen=[corpo[0] / self.S, corpo[1] / self.S], deco=1)
        else:
            gr.update(frags=[[p[0] / self.S, p[1] / self.S, self.ang(k, tau), sep(dx)] for k, p in enumerate(fr)],
                      dx=dx, pe=[self.pe[0] / self.S, self.pe[1] / self.S], vpe=[self.V0[0] / self.S, 0.0], calor=calor(dx))
        if self.fant.get_value() > 0.5:
            gr["fant"] = self.fantasmas(tau)
        return r4({"gr": gr, "cam": cam, "tau": tau})

    def m(self, p_metros, cam=None):
        return projeta3d(cam or self.f3d.e["cam"], (p_metros[0] / self.S, 0.0, p_metros[1] / self.S))

    def r_tela(self, k=None):
        """Raio equivalente na tela (Manim) da granada inteira (k=None) ou do caco k, no quadro corrente."""
        c = self.f3d.e["cam"]
        return c["K"] * self.f3d.e["gr"]["esc"] * (REQ_CORPO if k is None else REQ[k])

    def raio(self, massa):
        return self.r_tela(None if massa == MT else MS.index(massa))

    def cm(self):
        """⊕ calculado dos pontos físicos dos pedaços do estado do quadro (em metros → Manim)."""
        g = self.f3d.e["gr"]
        if "cen" in g:
            return self.m(np.array(g["cen"]) * self.S)
        ps = [np.array(q[:2]) * self.S for q in g["frags"]]
        return self.m(sum(m * p for m, p in zip(MS, ps)) / MT)


# ── explosão no espaço (T2-6, lote 2) ─────────────────────────────────────────────────────────────────────
class Explosao3D:
    """A mesma granada no espaço (exp: céu sem piso): corpo a V0 se parte nos mesmos três cacos (2, 1 e 1,5; 90°, 210°, 330°;
    uᵢ = C/mᵢ). Cada caco começa encaixado no corpo (centroide = centro + esc·cᵢ; Σ mᵢcᵢ = 0) e sai com uᵢ: o CM não muda."""
    V0, C, TE = 1.0, 0.8, 1.2
    ESC = 0.8                                     # v4: cacos maiores (o PALCO ocupado, 55–75%)

    def __init__(self, cena, K=1.25, camx=0.0, xc=-3.35, yc=-0.3, op=1.0, x0=-2.6):
        self.cena, self.x0 = cena, x0
        self.tau = ValueTracker(0.0)
        self.K, self.camx, self.xc, self.yc, self.seg = (ValueTracker(v) for v in (K, camx, xc, yc, 0.0))
        self.dolly = None                        # (K0, K1, camx0, camx1, T): recuo da câmera do chão em função de tau
        self.f3d = Fundo3D(cena, "exp", self.estado, op=op)

    def fis(self, tau):
        """corpo (x, z) ou None; pontos físicos dos cacos [(x, z)] (sem o encaixe) ou None; CM; velocidades (chão)."""
        cm = np.array([self.x0 + self.V0 * tau, 0.0])
        if tau < self.TE:
            return cm, None, cm, None
        fr = [cm + d * (self.C / m) * (tau - self.TE) for m, d in zip(MS, DIRS)]
        vs = [np.array([self.V0, 0.0]) + d * self.C / m for m, d in zip(MS, DIRS)]
        return None, fr, cm, vs

    def cam(self, tau):
        s = suave(self.seg.get_value())
        cmx = self.x0 + self.V0 * tau
        K, cx = self.K.get_value(), self.camx.get_value()
        if self.dolly:
            K0, K1, c0, c1, T = self.dolly
            u = suave(tau / T)
            K, cx = K0 + (K1 - K0) * u, c0 + (c1 - c0) * u
        return cam_frente(K=K, xc=self.xc.get_value() + s * (PALCO_C[0] - self.xc.get_value()), yc=self.yc.get_value(),
                          camx=cx + s * (cmx - cx), fov=16, el=0)

    def estado(self, t):
        tau = self.tau.get_value()
        corpo, fr, _, _ = self.fis(tau)
        dx = tau - self.TE
        on = (tau - (self.TE - 0.45)) / 0.45 * 1.15                        # as emendas acendem antes de estilhaçar
        gr = {"esc": self.ESC, "chao": 0, "onda": on, "brilho": (2.2 if on > 0 else 0.0) * (math.exp(-dx / 0.3) if dx > 0 else 1.0)}
        if corpo is not None:
            gr.update(cen=[corpo[0], corpo[1]], deco=1)
        else:
            gr.update(frags=[[p[0], p[1], giro(k, dx * 0.6), 0.0] for k, p in enumerate(fr)], dx=dx,
                      pe=[self.x0 + self.V0 * self.TE, 0.0], vpe=[self.V0, 0.0], calor=calor(dx))
        return r4({"gr": gr, "cam": self.cam(tau), "tau": tau})

    # pontos do quadro corrente (Manim)
    def m(self, p, prof=0.0):
        return projeta3d(self.f3d.e["cam"], (p[0], prof, p[1]))

    def corpos(self):
        """[(centro Manim, raio Manim, massa)] do quadro corrente: o corpo inteiro ou os três cacos (centroide da malha)."""
        e = self.f3d.e
        K, g = e["cam"]["K"], e["gr"]
        if "cen" in g:
            return [(self.m(g["cen"]), K * self.ESC * REQ_CORPO, MT)]
        return [(self.m((q[0] + self.ESC * c[0], q[1] + self.ESC * c[2]), self.ESC * c[1]), K * self.ESC * REQ[k], m)
                for k, (q, c, m) in enumerate(zip(g["frags"], CEN, MS))]

    def cm(self):
        """⊕ calculado dos centroides dos cacos do estado do quadro."""
        cs = self.corpos()
        if len(cs) == 1:
            return cs[0][0]
        return sum(m * c for c, _, m in cs) / MT


# ── semiesfera com fatias ────────────────────────────────────────────────────────────────────────────────
class Semiesfera3D:
    R, DZ = 1.8, 0.14

    def __init__(self, cena, K=1.57, xc=-3.35, yc=-0.95, op=1.0, el=16.0):
        self.cena = cena
        self.fz = ValueTracker(self.DZ / 2)
        self.camf = cam_obl(-40.0, el, (0, 0, 0.0), K=K, xc=xc, yc=yc, fov=16)
        self.f3d = Fundo3D(cena, "hem", lambda t: r4({"fz": self.fz.get_value(), "vis": 1, "cam": self.camf}), op=op)

    def p(self, q):
        return projeta3d(self.camf, q)

    def varrer(self, periodo=6.0):
        t0 = self.cena.clk.get_value()
        R, DZ = self.R, self.DZ
        self.fz.add_updater(lambda m: m.set_value(DZ / 2 + (R - DZ) * (0.5 - 0.5 * math.cos(2 * PI * (self.cena.clk.get_value() - t0) / periodo))))


# ── bandeja do T1-7 ──────────────────────────────────────────────────────────────────────────────────────
class Bandeja3D:
    """Bandeja de aço horizontal com as massas do T1-6 (metros): 2 kg em (0, 0), 1 kg em (4, 0), 1 kg em (2, 4); ⊕ em (1,5; 1,0).
    Um pino por baixo em (px, py); com o pino fora do ⊕ a bandeja gira `ang` em torno do eixo horizontal que passa pelo apoio e é
    perpendicular à direção apoio → ⊕ (o ⊕ desce: tomba para o lado do 2 kg). A câmera vai do topo (el 90°) a ~25°, com o ⊕ fixo na tela."""
    DADOS = [(2.0, (0.0, 0.0)), (1.0, (4.0, 0.0)), (1.0, (2.0, 4.0))]
    CM = np.array([1.5, 1.0])
    CG = np.array([2.0, 4.0 / 3.0])                     # centro geométrico do triângulo

    def __init__(self, cena, K=1.05, cm_tela=P3(-5.025, -1.75), op=1.0):
        self.cena, self.K, self.cmt = cena, K, cm_tela
        self.el, self.ang = ValueTracker(89.999), ValueTracker(0.0)
        self.px, self.py, self.pz, self.pv = ValueTracker(2.0), ValueTracker(4.0 / 3.0), ValueTracker(-1.2), ValueTracker(0.0)
        self.f3d = Fundo3D(cena, "band", self.estado, op=op)

    def trackers(self):
        return [self.el, self.ang, self.px, self.py, self.pz, self.pv]

    def eixo(self):
        d = self.CM - np.array([self.px.get_value(), self.py.get_value()])
        n = np.linalg.norm(d)
        return (np.array([1.0, 0.0]) if n < 1e-6 else np.array([-d[1], d[0]]) / n)

    def cam(self):
        return cam_obl(-90.0, self.el.get_value(), (1.5, 1.0, 0.0), K=self.K, xc=self.cmt[0], yc=self.cmt[1], fov=16)

    def estado(self, t):
        a = self.eixo()
        return r4({"band": {"px": self.px.get_value(), "py": self.py.get_value(), "ax": a[0], "ay": a[1], "ang": self.ang.get_value()},
                   "pino": [self.px.get_value(), self.py.get_value(), self.pz.get_value(), int(self.pv.get_value() > 0.5)], "cam": self.cam()})

    def mundo(self, q, e=None):
        """Ponto da bandeja (x, y, z) depois da rotação do quadro (Rodrigues em torno do eixo pelo apoio)."""
        e = e or self.f3d.e
        b = e["band"]
        k = np.array([b["ax"], b["ay"], 0.0])
        k = k / np.linalg.norm(k)
        piv = np.array([b["px"], b["py"], 0.0])
        v = np.asarray(q, float) - piv
        th = b["ang"]
        v = v * math.cos(th) + np.cross(k, v) * math.sin(th) + k * (k @ v) * (1 - math.cos(th))
        return piv + v

    def p(self, q):
        return projeta3d(self.f3d.e["cam"], self.mundo(q))

    def bolas(self):
        """[(centro Manim, raio Manim, massa)] do quadro."""
        out = []
        for m, (x, y) in self.DADOS:
            r = 0.3 * m ** (1 / 3)
            c = self.p((x, y, r))
            out.append((c, float(np.linalg.norm(self.p((x, y, 2 * r)) - c)), m))
        return out

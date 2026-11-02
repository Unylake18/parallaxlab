"""yt_0018 — o lado Manim das três cenas Three.js novas (threejs/cena3d/cm18.js): física, câmera e estado por quadro; pontos projetados com
a mesma câmera do b3d.js (projeta3d). As camadas leem sempre `f3d.e` (o estado do próprio quadro).

Cubo18   — X2: fio de aço em três arestas de um cubo de 1 m; arestas acendem e encolhem até partículas; câmera oblíqua (az, el).
Rojao3D  — X5: v₀ = 31,305 m/s a 45° (H = 25 m, topo em (50; 25) m aos 2,2588 s); no topo, 100 g a 17,709 m/s e 50 g a 30,990 m/s, na
           horizontal; os dois pousam juntos em t = 4,5175 s, em 90 m e 120 m. O ⊕ é sempre calculado dos pedaços (física).
Foguete3D — EN2: foguete que ejeta gás discreto (conservação exata a cada ejeção); o ⊕ do conjunto anda a velocidade constante.
"""
from prob2 import *  # noqa: F401,F403


# ════════════════════════════════════════ cubo ════════════════════════════════════════
class Cubo18:
    CM = (5 / 6, 1 / 2, 1 / 6)
    MEIOS = ((0.5, 0, 0), (1, 0.5, 0), (1, 1, 0.5))
    CANTOS = ((0, 0, 0), (1, 0, 0), (1, 1, 0), (1, 1, 1))

    def __init__(self, cena, K=3.0, xc=-3.8, yc=-0.45, az=-52.0, el=27.0, op=1.0):
        self.cena = cena
        self.Kt, self.xct, self.yct = ValueTracker(K), ValueTracker(xc), ValueTracker(yc)           # v6: a câmera do cubo anima (escala e posição no ESQUEMA)
        self.az, self.el = ValueTracker(az), ValueTracker(el)
        self.br = [ValueTracker(0.0) for _ in range(3)]
        self.enc = [ValueTracker(0.0) for _ in range(3)]
        self.part = [ValueTracker(0.0) for _ in range(3)]
        self.dr = [ValueTracker(1.0) for _ in range(3)]
        self.cx = ValueTracker(1.0)
        self.f3d = Fundo3D(cena, "cubo", self.estado, op=op)

    K = property(lambda s: s.Kt.get_value())
    xc = property(lambda s: s.xct.get_value())
    yc = property(lambda s: s.yct.get_value())

    def trackers(self):
        return [self.az, self.el, self.cx, self.Kt, self.xct, self.yct, *self.br, *self.enc, *self.part, *self.dr]

    def cam(self):
        return cam_obl(self.az.get_value(), self.el.get_value(), (0.5, 0.5, 0.5), K=self.K, xc=self.xc, yc=self.yc, fov=16)

    def estado(self, t):
        return r4({"cubo": {"ar": [[b.get_value(), e.get_value(), d.get_value()] for b, e, d in zip(self.br, self.enc, self.dr)], "part": [p.get_value() for p in self.part],
                            "caixa": self.cx.get_value()}, "cam": self.cam()})

    def p(self, q):
        return projeta3d(self.f3d.e["cam"], q)


# ════════════════════════════════════════ rojão ════════════════════════════════════════
MASSAS = (0.100, 0.050)                     # kg: pedaço de trás (aletas) e da frente (ogiva)
MED_RJ = None


class Rojao3D:
    S, G = 20.0, 9.8
    V0 = math.sqrt(25.0 * 4 * 9.8)          # H = v₀² sen²45°/(2g) = v₀²/(4g) = 25 m → v₀ = 31,305 m/s
    VX = V0 / math.sqrt(2)                  # 22,136 m/s
    TE = VX / 9.8                           # 2,2588 s
    PE = np.array([VX * TE, 25.0])          # (50,0; 25,0) m
    VF = ((90.0 - 50.0) / TE, (120.0 - 50.0) / TE)    # 17,709 e 30,990 m/s
    TL = 2 * TE                             # 4,5175 s
    OMEGA = (2 * PI * 0.55, -2 * PI * 0.95)  # giro dos pedaços (voltas/s)
    EL = 6.0

    def __init__(self, cena, K=1.05, camx=3.1, yc=-1.2, xc=-3.8, comp=0.7, op=1.0):
        self.cena = cena
        self.tau = ValueTracker(0.0)
        self.K, self.camx, self.yc, self.xc = ValueTracker(K), ValueTracker(camx), ValueTracker(yc), ValueTracker(xc)
        self.seg, self.ycm, self.xcm = ValueTracker(0.0), ValueTracker(-0.3), ValueTracker(-3.8)
        self.emenda, self.comp = ValueTracker(0.0), comp
        self.f3d = Fundo3D(cena, "roj", self.estado, op=op)

    def trackers(self):
        return [self.tau, self.K, self.camx, self.yc, self.xc, self.seg, self.ycm, self.xcm, self.emenda]

    def ideal(self, tau):
        return np.array([self.VX * tau, self.VX * tau - 0.5 * self.G * tau * tau])

    def fis(self, tau):
        """(corpo | None, [p_trás, p_frente] | None, CM, V_cm) em m e m/s."""
        if tau < self.TE:
            p = self.ideal(tau)
            return p, None, p, np.array([self.VX, self.VX - self.G * tau])
        s = min(tau, self.TL) - self.TE
        fr = [self.PE + np.array([v * s, -0.5 * self.G * s * s]) for v in self.VF]
        fr = [np.array([p[0], max(0.0, p[1])]) for p in fr]
        cm = (MASSAS[0] * fr[0] + MASSAS[1] * fr[1]) / sum(MASSAS)
        vs = [np.zeros(2) if tau >= self.TL else np.array([v, -self.G * s]) for v in self.VF]
        return None, fr, cm, (MASSAS[0] * vs[0] + MASSAS[1] * vs[1]) / sum(MASSAS)

    def cam(self):
        K, s = self.K.get_value(), suave(self.seg.get_value())
        tau = self.tau.get_value()
        cmx = self.fis(tau)[2]
        cx = (1 - s) * self.camx.get_value() + s * cmx[0] / self.S
        xc = (1 - s) * self.xc.get_value() + s * self.xcm.get_value()
        c0 = dict(cam_frente(K=K, xc=xc, yc=0.0, camx=cx, fov=16, el=self.EL), near=0.25, far=700)
        yseg = self.ycm.get_value() - projeta3d(c0, (cmx[0] / self.S, 0.0, cmx[1] / self.S))[1]
        c0["yc"] = (1 - s) * self.yc.get_value() + s * yseg
        return c0

    def esc(self):
        return self.comp / self.K.get_value()

    def ang(self, k, tau):
        return self.OMEGA[k] * (tau - self.TE) if tau > self.TE else 0.0

    def estado(self, t):
        tau = self.tau.get_value()
        cam = self.cam()
        esc = self.esc()
        lift = 0.13 * esc
        corpo, fr, _, _ = self.fis(tau)
        dx = tau - self.TE
        rj = {"esc": esc, "emenda": self.emenda.get_value(), "marco": math.exp(-((tau - 0.05) / 0.12) ** 2)}
        if corpo is not None:
            vy = self.VX - self.G * tau
            rj.update(cen=[corpo[0] / self.S, corpo[1] / self.S + lift], ang=math.atan2(vy, self.VX))
        else:
            sep = suave(dx / 0.15)
            rj.update(frags=[[p[0] / self.S, p[1] / self.S + lift, self.ang(k, min(tau, self.TL + 0.4)), sep] for k, p in enumerate(fr)],
                      dx=dx, pe=[self.PE[0] / self.S, self.PE[1] / self.S + lift], calor=math.exp(-dx / 0.35))
        return r4({"rj": rj, "cam": cam, "tau": tau})

    def m(self, p_metros, cam=None):
        return projeta3d(cam or self.f3d.e["cam"], (p_metros[0] / self.S, 0.0, p_metros[1] / self.S))

    def cm(self):
        return self.m(self.fis(self.f3d.e["tau"])[2])


# ════════════════════════════════════════ foguete ════════════════════════════════════════
class Foguete3D:
    """Foguete que ejeta gás em pacotes iguais (dm a cada DT): m v = (m − dm) v′ + dm (v′ − u) → o centro de massa do conjunto anda a
    velocidade constante. Unidades de tela (Manim); o 3D recebe x/K."""
    M0, MF, U, V0, TQ, DT, LN = 1.0, 0.45, 1.45, 0.35, 8.0, 1 / 30, 0.62

    def __init__(self, cena, K=1.0, yc=0.6, x0=-6.3, comp=1.5, op=1.0):
        self.cena, self.K, self.yc, self.comp = cena, K, yc, comp
        self.t = ValueTracker(0.0)
        n = int(round(self.TQ / self.DT))
        dm = (self.M0 - self.MF) / n
        rng = np.random.default_rng(5)
        m, v, x, tt = self.M0, self.V0, x0, 0.0
        self.ev = []                                         # (t, x_foguete, v_foguete depois, m depois)
        self.gas = []                                        # (t0, x0, vx, vy)
        for k in range(n):
            vn = v + dm * self.U / m
            vy = rng.normal(0, 0.12) * (1 if k % 2 else -1)
            self.gas.append((tt, x - self.LN, vn - self.U, vy))
            m -= dm
            v = vn
            self.ev.append((tt, x, v, m))
            x += v * self.DT
            tt += self.DT
        self.ev.append((tt, x, v, m))
        self.dm, self.x0 = dm, x0
        self.f3d = Fundo3D(cena, "fog", self.estado, op=op)

    def foguete(self, t):
        """(x, v, m) do foguete no instante t (entre ejeções: movimento uniforme)."""
        if t <= 0:
            return self.x0 + self.V0 * t, self.V0, self.M0
        k = min(int(t / self.DT), len(self.ev) - 1)
        t0, x, v, m = self.ev[k]
        return x + v * (t - t0), v, m

    def gas_pts(self, t):
        out = []
        for t0, x0, vx, vy in self.gas:
            if t0 < t:
                out.append((t - t0, x0 + vx * (t - t0), vy * (t - t0)))
        return out

    def cm_x(self, t):
        x, v, m = self.foguete(t)
        g = self.gas_pts(t)
        return (m * x + self.dm * sum(p[1] for p in g)) / self.M0

    def estado(self, t):
        tt = self.t.get_value()
        x, v, m = self.foguete(tt)
        return r4({"fg": {"x": x / self.K, "z": 0.0, "esc": self.comp, "chama": 1.0 if tt < self.TQ else 0.0, "rol": 0.4 * tt},
                   "cam": cam_frente(K=self.K, xc=0.0, yc=self.yc, camx=0.0, fov=16, el=0)})

"""yt_0018 v2 — o lago do gafanhoto em Three.js (threejs/cena3d/lago3d.js) do lado Manim: a mesma física do v1 (lago.py; auditada a 0,00 px),
a câmera e o estado por quadro, e os pontos projetados (projeta3d, a mesma câmera do b3d.js) onde o Manim prende réguas, cotas, setas, θ, ⊕
e rótulos.

Física (g = 9,8; eixo x na água, z para cima, plano do salto y = 0): x_g = vx·τ, z_g = vy·τ − ½gτ², x_f = −(vx/4)·τ (ponta esquerda da folha);
pouso na folha → os dois param; na água → a folha segue a −V. ⊕ = (m x_g + M (x_f + L/2))/(m + M) = 0,12 m constante no ar.
Câmera: oblíqua (az, el, alvo) com `c` = 0 seguindo a água e c = 1 seguindo a folha (VISTO DA FOLHA: a folha para na tela).
"""
from prob2 import *  # noqa: F401,F403


class Lago3D:
    G, m, M, L, LG = 9.8, 1.0, 4.0, 0.30, 0.07
    HCM = 0.012                                     # altura do CM do gafanhoto acima dos pés (m), para o ⊕ do sistema

    def __init__(self, cena, theta=30.0, v=4.0, K=14.0, az=-90.0, el=3.0, alvo=(0.15, 0.0, 0.03), xc=-3.8, yc=-1.4, fov=10.0, esc=1.5, op=1.0):
        self.cena, self.v = cena, v
        self.th, self.tau, self.c = ValueTracker(theta), ValueTracker(0.0), ValueTracker(0.0)
        self.K, self.az, self.el, self.fov = ValueTracker(K), ValueTracker(az), ValueTracker(el), ValueTracker(fov)
        self.ax, self.ay, self.az_ = ValueTracker(alvo[0]), ValueTracker(alvo[1]), ValueTracker(alvo[2])
        self.xc, self.yc = ValueTracker(xc), ValueTracker(yc)
        self.esc = ValueTracker(esc)
        self.pre = ValueTracker(0.0)                # 0 → 1: agacha antes do salto (pose 3 → 0)
        self.anel, self.op_fant = ValueTracker(0.0), ValueTracker(0.0)
        self.rel_u = False
        self.fant_dt = 0.08
        self.f3d = Fundo3D(cena, "lago", self.estado, op=op)

    def trackers(self):
        return [self.th, self.tau, self.c, self.K, self.az, self.el, self.fov, self.ax, self.ay, self.az_, self.xc, self.yc, self.esc, self.pre,
                self.anel, self.op_fant]

    # ── física (a mesma do v1) ───────────────────────────────────────────────────────────────────────────────────────
    def comp(self):
        a = math.radians(self.th.get_value())
        if self.rel_u:
            ux = self.v * math.cos(a)
            return ux * self.M / (self.m + self.M), self.v * math.sin(a), -ux * self.m / (self.m + self.M)
        vx = self.v * math.cos(a)
        return vx, self.v * math.sin(a), -vx * self.m / self.M

    def T(self):
        return 2 * self.comp()[1] / self.G

    def na_folha(self):
        vx, vy, V = self.comp()
        return (vx - V) * self.T() <= self.L + 1e-9

    def estado_f(self, tau=None):
        tau = self.tau.get_value() if tau is None else tau
        vx, vy, V = self.comp()
        T = self.T()
        if tau <= 0:
            return 0.0, 0.0, 0.0
        if tau <= T:
            return vx * tau, vy * tau - 0.5 * self.G * tau * tau, V * tau
        if self.na_folha():
            return vx * T, 0.0, V * T
        return vx * T, -0.012, V * tau

    def cm(self, tau=None):
        xg, yg, xf = self.estado_f(tau)
        return (self.m * xg + self.M * (xf + self.L / 2)) / (self.m + self.M), self.m * (yg + self.HCM) / (self.m + self.M)

    def pose(self, tau=None):
        tau = self.tau.get_value() if tau is None else tau
        T = self.T()
        if tau <= 0:
            return 3.0 * (1 - suave(self.pre.get_value())) if self.pre.get_value() < 1 else 0.0
        s = tau / T
        if s < 1:
            if s < 0.1:
                return 1.0
            if s < 0.3:
                return 1.0 + (s - 0.1) / 0.2
            if s < 0.8:
                return 2.0
            return 2.0 + (s - 0.8) / 0.2
        if self.na_folha():
            return max(0.0, 3.0 - (tau - T) / 0.25 * 3.0) if tau - T < 0.25 else 0.0
        return 2.0

    # ── câmera e estado ───────────────────────────────────────────────────────────────────────────────────────────
    def cam(self, tau=None):
        xf = self.estado_f(tau)[2]
        return cam_obl(self.az.get_value(), self.el.get_value(), (self.ax.get_value() + self.c.get_value() * xf, self.ay.get_value(), self.az_.get_value()),
                       K=self.K.get_value(), xc=self.xc.get_value(), yc=self.yc.get_value(), fov=self.fov.get_value())

    def estado(self, t):
        tau = self.tau.get_value()
        xg, zg, xf = self.estado_f(tau)
        vx, vy, V = self.comp()
        T = self.T()
        tw = self.cena.clk.get_value()
        e = {"g": {"x": xg, "z": zg, "esc": self.esc.get_value(), "pose": self.pose(tau)}, "f": {"x": xf, "bal": 1.3 * tw}, "tw": tw, "cam": self.cam(tau), "zona": 1.0 if self.cena.lote == "PX3" else 0.0}   # v5 G34: sem brilhos fortes atrás da Pilha
        e["fis"] = [tau, self.th.get_value(), int(self.rel_u)]
        aneis = []
        a = self.anel.get_value()
        if a > 0.01 and not self.na_folha() and tau > T:
            for k in range(3):
                u = a - 0.22 * k
                if u > 0:
                    aneis.append([vx * T, 0.02 + 0.32 * u, 1 - u])
        for k, xm in enumerate((xf, xf + self.L)):                 # a água lambe as pontas da folha (ambiente)
            u = ((tw + 1.1 * k) % 2.4) / 2.4
            aneis.append([xm, 0.01 + 0.08 * u, 0.5 * (1 - u)])
        e["aneis"] = aneis
        if 0 < tau and abs(V) > 1e-6:                              # esteira em V atrás da folha recuando
            e["esteira"] = [xf + self.L + 0.005, min(0.35, abs(xf) * 0.9 + 0.02), min(1.0, tau / 0.1) * (1.0 if tau <= T or not self.na_folha() else max(0.0, 1 - (tau - T)))]
        gotas = []
        if 0 < tau < 0.25:                                         # gotas na decolagem
            for k in range(10):
                ang = 0.4 + 0.25 * k
                gotas.append([0.004 * k - 0.01 + 0.25 * math.cos(ang) * tau, 0.6 * math.sin(ang) * tau - 4.9 * tau * tau, 0.0, 1 - tau / 0.25])
        if tau > T and not self.na_folha() and tau - T < 0.35:     # respingo no pouso
            d = tau - T
            for k in range(14):
                ang = 0.3 + 0.18 * k
                gotas.append([vx * T + 0.4 * math.cos(ang) * d, max(0.0, 1.1 * math.sin(ang) * d - 4.9 * d * d), 0.0, 1 - d / 0.35])
        e["gotas"] = [[q[0], q[1], q[2]] + ([q[3]] if i == 0 else []) for i, q in enumerate(gotas)]
        if self.op_fant.get_value() > 0.5 and tau > 0:             # poses fantasma ao longo do voo
            fs = []
            for s in np.arange(self.fant_dt, min(tau, T), self.fant_dt * max(1.0, T / 0.5)):
                x_, z_, _ = self.estado_f(s)
                fs.append([x_, z_, self.pose(s)])
            e["fant"] = fs[-5:]
        return r4(e)

    # ── projeções (Manim) ───────────────────────────────────────────────────────────────────────────────────────
    def P(self, x, z, y=0.0, cam=None):
        return projeta3d(cam or self.f3d.e["cam"], (x, y, z))

    def pe(self):
        g = self.f3d.e["g"]
        return self.P(g["x"], g["z"])

    def futuro(self, dt=2.0):
        tau = self.tau.get_value()
        T = self.T()
        if tau <= 0 or tau >= T:
            return np.zeros((0, 3))
        return np.array([self.P(*self.estado_f(s)[:2][::1]) for s in np.linspace(tau, min(T, tau + dt), 10)])

    def reg(self):
        e = self.f3d.e
        tau = e.get("g") and self.tau.get_value()
        xg, zg, xf = self.estado_f()
        self.cena.reg("lago", tau=self.tau.get_value(), th=self.th.get_value(), c=self.c.get_value(), rel=int(self.rel_u), xg=xg, yg=zg, xf=xf,
                      pe=self.P(xg, zg), folha=self.P(xf, 0.0), cam=None)

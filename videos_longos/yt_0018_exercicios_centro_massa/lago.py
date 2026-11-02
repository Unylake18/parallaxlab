"""yt_0018 — o lago do gafanhoto (hook, X3, S1): física exata quadro a quadro (handoff §4, g = 9,8).

Eixo x na água; folha de 0 a 0,30 m no início (ponta esquerda em x_f), gafanhoto (pés) em x = 0, salta para a direita com v = 4 m/s
em relação à água (ou u em relação à folha, `rel_u`). Sem força horizontal externa: m·vx = M·V → a folha recua com V = vx/4.
  x_g(τ) = vx·τ, y_g(τ) = vy·τ − ½gτ² (τ ≤ T = 2vy/g); x_f(τ) = −V·τ.
Pouso: na folha (alcance relativo ≤ L) → os dois param juntos (momento total zero); na água → ele fica, a folha segue a −V.
⊕ do sistema: x = (m x_g + M (x_f + L/2))/(m + M) = 0,12 m constante no ar; y = m (y_g + h_cm)/(m + M).
Câmera: X(x) = X0 + K·(x − c·x_f(τ)); c = 0 → VISTO DA ÁGUA, c = 1 → VISTO DA FOLHA (a folha para na tela, a água desliza).
"""
from prob import *  # noqa: F401,F403


class Lago:
    G, m, M, L, LG = 9.8, 1.0, 4.0, 0.30, 0.07
    HCM = 0.15 * 0.07                       # altura do CM do gafanhoto acima dos pés (m)

    def __init__(self, cena, K=7.0, X0=-5.6, YW=-2.9, xa=-7.4, xb=-0.2, theta=30.0, v=4.0, fundo=-4.5):
        self.cena, self.YW, self.xa, self.xb, self.v = cena, YW, xa, xb, v
        self.Kt, self.X0t, self.K0 = ValueTracker(K), ValueTracker(X0), K
        self.th, self.tau, self.c = ValueTracker(theta), ValueTracker(0.0), ValueTracker(0.0)
        self.op_traj, self.op_rw, self.op_rf, self.op_cm = ValueTracker(0.0), ValueTracker(0.0), ValueTracker(0.0), ValueTracker(0.0)
        self.op_ini, self.anel, self.op_g = ValueTracker(0.0), ValueTracker(0.0), ValueTracker(1.0)
        self.rel_u = False
        self.extra = []                     # camadas extras: funções () → VGroup, desenhadas por cima
        self.agua = agua(xa, xb, YW, fundo=fundo)
        rng = np.random.default_rng(7)
        self._riscos = [(rng.uniform(xa - 4, xb + 4), YW - rng.uniform(0.12, min(1.4, YW - fundo - 0.1)), rng.uniform(0.15, 0.55),
                         rng.uniform(0.12, 0.3)) for _ in range(int((xb - xa + 8) * 2.2))]
        self._folha = folha(self.L * K)
        self._gaf = {s_: gafanhoto(self.LG * K, salto=s_) for s_ in (0.0, 1.0)}
        self._rw = {}
        self.ultimo = {}

    def trackers(self):
        return [self.Kt, self.X0t, self.th, self.tau, self.c, self.op_traj, self.op_rw, self.op_rf, self.op_cm, self.op_ini, self.anel, self.op_g]

    @property
    def K(self):
        return self.Kt.get_value()

    @property
    def X0(self):
        return self.X0t.get_value()

    def folha_mob(self, x):
        return self._folha.copy().scale(self.K / self.K0, about_point=ORIGIN).shift(P3(self.X(x), self.YW))

    # ── física ────────────────────────────────────────────────────────────────────────────────────────────────
    def comp(self):
        a = math.radians(self.th.get_value())
        if self.rel_u:                       # u em relação à folha: no chão, o gafanhoto leva M/(m+M) de u cos θ e a folha −m/(m+M)
            ux = self.v * math.cos(a)
            return ux * self.M / (self.m + self.M), self.v * math.sin(a), -ux * self.m / (self.m + self.M)
        vx = self.v * math.cos(a)
        return vx, self.v * math.sin(a), -vx * self.m / self.M

    def T(self):
        return 2 * self.comp()[1] / self.G

    def na_folha(self):
        vx, vy, V = self.comp()
        return (vx - V) * self.T() <= self.L + 1e-9

    def estado(self, tau=None):
        """(x_g, y_g, x_f) em metros no referencial da água."""
        tau = self.tau.get_value() if tau is None else tau
        vx, vy, V = self.comp()
        T = self.T()
        if tau <= 0:
            return 0.0, 0.0, 0.0
        if tau <= T:
            return vx * tau, vy * tau - 0.5 * self.G * tau * tau, V * tau
        if self.na_folha():
            return vx * T, 0.0, V * T
        return vx * T, 0.0, V * tau

    def cm(self, tau=None):
        xg, yg, xf = self.estado(tau)
        return (self.m * xg + self.M * (xf + self.L / 2)) / (self.m + self.M), self.m * (yg + self.HCM) / (self.m + self.M)

    # ── tela ───────────────────────────────────────────────────────────────────────────────────────────────────
    def X(self, x, tau=None):
        return self.X0 + self.K * (x - self.c.get_value() * self.estado(tau)[2])

    def P(self, x, y, tau=None):
        return P3(self.X(x, tau), self.YW + self.K * y)

    def regua_agua(self, y=None):
        c = self.c.get_value() * self.estado()[2]
        y = self.YW - 0.42 if y is None else y
        k = (round(c, 4), round(self.K, 3), round(self.X0, 3))
        if k not in self._rw:
            if len(self._rw) > 300:
                self._rw.clear()
            xm0 = (self.xa + 0.25 - self.X0) / self.K + c
            xm1 = (self.xb - 0.25 - self.X0) / self.K + c
            self._rw[k] = regua(self.X(xm0), self.X(xm1), y, self.K, xm0, xm1, passo=0.05, rot_cada=0.1)
        return self._rw[k].copy()

    def desenho(self):
        tau = self.tau.get_value()
        xg, yg, xf = self.estado(tau)
        vx, vy, V = self.comp()
        T = self.T()
        K, YW = self.K, self.YW
        g = VGroup()
        # água: os reflexos andam com a água (no referencial da folha ela desliza)
        dx = -K * self.c.get_value() * xf
        riscos = VGroup()
        for x0, y0, L_, o in self._riscos:
            xx = x0 + dx
            if self.xa + 0.05 < xx and xx + L_ < self.xb - 0.05:
                riscos.add(Line(P3(xx, y0), P3(xx + L_, y0)).set_stroke(WHITE_ if o < 0.2 else mix(BLUE_L, 0.3), 1.3, opacity=o))
        riscos._fundo = True
        g.add(riscos.set_z_index(-4))
        if self.op_ini.get_value() > 0.01:                                  # marcador tracejado: a folha onde estava no começo
            f0 = self.folha_mob(0.0)
            g.add(DashedVMobject(f0[0].copy().set_fill(opacity=0).set_stroke(WHITE_, 2, opacity=0.7 * self.op_ini.get_value()), num_dashes=40)
                  .set_z_index(3))
        if self.op_rw.get_value() > 0.01:
            g.add(escala_op(self.regua_agua(), self.op_rw.get_value()))
        fo = self.folha_mob(xf)
        g.add(fo)
        if self.op_rf.get_value() > 0.01:
            o = self.op_rf.get_value()
            g.add(regua(self.X(xf), self.X(xf + self.L), YW + 0.3, K, 0.0, self.L, passo=0.05, rot_cada=0.1, cor=mix(GEO, 0.25), cima=True, op=o))
        # trajetória (violeta fina) no referencial da câmera
        if self.op_traj.get_value() > 0.01 and tau > 0:
            t1 = min(tau, T)
            ss = np.linspace(0, t1, max(2, int(40 * t1 / max(T, 1e-3)) + 2))
            pts = [self.P(*self.estado(s)[:2], tau=s) for s in ss]                # no referencial da folha: o traço relativo a ela
            g.add(VMobject().set_points_as_corners(pts).set_stroke(VEL, 2.6, opacity=self.op_traj.get_value()).set_z_index(6))
        # anéis na água no pouso
        a = self.anel.get_value()
        if a > 0.01 and not self.na_folha():
            c0 = P3(self.X(vx * T), YW)
            for k in range(3):
                u = a - 0.22 * k
                if u > 0:
                    g.add(onda_agua(c0, 0.15 + 1.2 * u, 0.8 * (1 - u)).set_z_index(5))
        # gafanhoto
        if self.op_g.get_value() > 0.01:
            no_ar = 0 < tau < T
            ga = self._gaf[1.0 if no_ar else 0.0].copy().scale(K / self.K0, about_point=ORIGIN)
            pe = self.P(xg, yg) + P3(0, 0.012)
            if tau > T and not self.na_folha():
                pe = pe + P3(0, -0.06)                                     # caiu na água: afunda um pouco
            ga.shift(pe)
            g.add(escala_op(ga, self.op_g.get_value()).set_z_index(7))
        # ⊕ do sistema
        if self.op_cm.get_value() > 0.01:
            xc, yc = self.cm(tau)
            o = self.op_cm.get_value()
            pc = self.P(xc, yc)                                           # o ⊕ na posição verdadeira (média ponderada)
            g.add(tracejado(P3(pc[0], YW - 0.5), P3(pc[0], YW + K * 0.2 + 0.5), WHITE_, 2, 0.6 * o).set_z_index(8),
                  marcador_cm(pc, r=0.17, op=o))
            self.ultimo["cm"] = pc
        for fn in self.extra:
            g.add(fn())
        self.ultimo.update(pe=self.P(xg, yg), folha=P3(self.X(xf), YW))
        self.cena.reg("lago", tau=tau, th=self.th.get_value(), c=self.c.get_value(), X0=self.X0, K=K, YW=YW, rel=int(self.rel_u),
                      pe=self.P(xg, yg), folha=P3(self.X(xf), YW), cm=self.ultimo.get("cm") if self.op_cm.get_value() > 0.01 else None,
                      xg=xg, yg=yg, xf=xf)
        return g

    def montar(self):
        """(fundo estático da água, camada viva)."""
        self.viva = vivo(self.desenho)
        return self.agua, self.viva

    def futuro(self, dt=2.0):
        """Pontos da trajetória do gafanhoto nos próximos dt s de física (auditoria G6)."""
        tau = self.tau.get_value()
        T = self.T()
        if tau >= T or (tau <= 0 and self.op_traj.get_value() < 0.01):          # só durante um salto
            return np.zeros((0, 3))
        return np.array([self.P(*self.estado(s)[:2], tau=s) + P3(0, 0.1) for s in np.linspace(tau, min(T, tau + dt), 12)])

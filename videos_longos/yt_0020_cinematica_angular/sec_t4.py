"""Lote PT4 (v2): T4 — e cada ponto do corpo? Disco de referência (C = (−3,75; −0,55), R = 2,1: ø 68% da altura do ESQUEMA); o ponto de fora é o de estudo.
T4-1 o ponto varre só o arco s (D21) e o ângulo θ; s = rθ → d/dt dos dois lados → o r sai da derivada (selo r CONSTANTE) → v_t = rω → |v_t| = r|ω|.
T4-2 a hélice Three.js volta (câmera do hook, ×90), PARA numa pose (pá marcada para a esquerda) para os rótulos presos aos pontos: cotas GEO do eixo a
r₁ = 0,10 m e r₂ = 0,95 m, 282,7 rad/s no cubo (no vão entre as pás, sem linha-guia); v = rω com os números voando do desenho e × 3,6 por glyph map;
ela volta a girar em "o cubo não gira mais devagar" (rastros de mesmo Δt). T4-3 dois pontos opostos: |v⃗_A| = |v⃗_B| = rω e v⃗_A = −v⃗_B (o sinal sai da seta).
T4-4 o disco acelera: a seta verde a_t nasce na ponta da violeta (freando, nasce no ponto e aponta para trás); v_t = rω → dv_t/dt = r dω/dt → a_t = rα.
T4-5 ω constante: a_c = v²/r → (rω)²/r → r²ω²/r → (risco) ω²r. T4-6 ω(t) = 0,625 + 0,175 sen(1,6 t): o disco vai para a esquerda e encolhe; inset de zoom
(×2,5, borda GEO) no topo da borda com a_t, a_c, a soma e φ (rótulos fora do inset); a = √(a_t² + a_c²), tan φ = |a_t|/a_c; fecho: a hélice grande volta
com a seta verde para o eixo na ponta, a_c = ω²r = 282,7² · 0,95 ≈ 7,6 × 10⁴ m/s², a_c ≈ 7.750 g.
Álgebra do v2: nenhuma linha de equação da CONTA entra por FadeIn de linha inteira (escrita em ordem, voos do desenho, passo/TransformByGlyphMap)."""
from pecas20 import *  # noqa: F401,F403
from sec_hook import camada_helice, REV_TELA, K_H, C_H  # noqa: E402

CD, RD = P3(-3.75, -0.55), 2.45       # v3 §4: disco no tamanho do T1/T2 (ø 5,0 u ≈ 60% da altura); as setas e os rótulos cabem no ESQUEMA
KH4, CH4 = 2.7, P3(-3.75, -0.27)        # v3 §4: hélice do T4 maior (ø 5,1 u ≈ 64% da altura); sobe um pouco para a ponta não cruzar o selo CÂMERA LENTA
KV = 0.55                            # seta v = KV · r · ω
KT = 7.0                              # T4-4: seta a_t = KT · |a_t| (só ela na tela)
KC = 1.0                              # T4-5: seta a_c = KC · a_c
KA = 0.6                              # T4-6: a_t e a_c na MESMA escala (SETAS PROPORCIONAIS); o inset amplia ZOOM×
ZOOM = 2.5
C6, R6 = P3(-5.0, -1.4), 1.9          # T4-6 (v3): o disco vai para a esquerda e encolhe menos (era 1,6); o inset mora à direita, acima
CI, RI = P3(-2.0, 1.0), 1.2           # inset (círculo com borda GEO)
W_H = 2 * PI * REV_TELA               # giro de tela da hélice (o mesmo do hook)
POSE = PI                             # hélice parada: a pá marcada aponta para a esquerda (os rótulos cabem nos vãos entre as pás)
ZX = (-7.2, 0.1, -3.5, 2.42)          # caixa do ESQUEMA para rótulos que se movem


def no_esq(m, z=ZX, d=None):
    """Rótulo vivo sempre dentro do ESQUEMA; com o disco `d`, nunca sobre a linha de referência tracejada (sai para cima ou para baixo dela)."""
    if d is not None:
        C, R = d.C, d.R
        y0, y1 = m.get_bottom()[1], m.get_top()[1]
        if m.get_right()[0] > C[0] + R - 0.15 and m.get_left()[0] < C[0] + R + 0.75 and y0 < C[1] + 0.2 and y1 > C[1] - 0.2:
            m.shift(UP * ((C[1] + 0.2 - y0) if m.get_y() >= C[1] else (C[1] - 0.2 - y1)))
    dx = max(0.0, z[0] - m.get_left()[0]) - max(0.0, m.get_right()[0] - z[1])
    dy = max(0.0, z[2] - m.get_bottom()[1]) - max(0.0, m.get_top()[1] - z[3])
    return m.shift(P3(dx, dy))


def Mm(*pares, size):
    """Proxy de TransformMatchingTex: o mesmo TeX da linha da CONTA (eqp), mas em partes (cada parte é uma chave do matching), cor por parte."""
    m = Mc(*pares, size=size)
    for sub, (t, c) in zip(m.submobjects, pares):
        if c:
            sub.set_stroke(c, width=1.8, background=False)
    return m


def pos_vab(p, s_, u, n, L):
    """Rótulo de v⃗_A/v⃗_B: por fora do ponto, ao lado da seta; se isso sair do ESQUEMA (ponto perto do rodapé/topo), vai para depois da ponta da seta."""
    c1 = p + s_ * n * L / 2 + s_ * u * 0.58
    if ZX[2] + 0.55 < c1[1] < ZX[3] - 0.25:
        return c1
    return p + s_ * n * (L + 0.75) + s_ * u * 0.3


def cota_h(x0, x1, y, cor=GEO):
    return VGroup(Line(P3(x0, y), P3(x1, y)).set_stroke(cor, 2.2), *[Line(P3(x, y - 0.1), P3(x, y + 0.1)).set_stroke(cor, 2.2) for x in (x0, x1)]).set_z_index(9)


class GiroT4:
    """Ângulo da hélice no tempo do lote: giro uniforme a W_H (CÂMERA LENTA ×90, como no hook), parada suave numa pose e retomada suave."""

    def __init__(self, t0, a0):
        self.f = [("u", t0, a0, 0.0)]

    def ang(self, t):
        tipo, t0, a0, T = next((x for x in reversed(self.f) if x[1] <= t + 1e-9), self.f[0])
        s = t - t0
        if tipo == "u":
            return a0 + W_H * s
        if tipo == "d":
            u = min(1.0, max(0.0, s / T))
            return a0 + W_H * T * (u - u * u / 2)
        if s < T:
            return a0 + W_H * s * s / (2 * T)
        return a0 + W_H * T / 2 + W_H * (s - T)

    def parar(self, t, pose=POSE, T0=1.4):
        """Freia até a pose (a pá marcada em `pose`, mod 2π); com a_0 escolhido na criação, a freada dura T0."""
        a = self.ang(t)
        k = math.ceil((a + W_H * 0.35 * T0 / 2 - pose) / (2 * PI))       # atraso pequeno só encurta a freada (nunca uma volta a mais)
        T = 2 * (pose + 2 * PI * k - a) / W_H
        self.f.append(("d", t, a, T))
        return T

    def retomar(self, t, T=1.2):
        self.f.append(("a", t, self.ang(t), T))


def a0_para(t0, t_stop, T0=1.4, pose=POSE):
    """Ângulo inicial que faz a freada começada em t_stop (com duração T0) terminar exatamente na pose."""
    return pose - W_H * (t_stop - t0) - W_H * T0 / 2


class DiscoMov(DiscoRef):
    """DiscoRef que muda de lugar e de tamanho (T4-6 abre espaço para o inset): centro e raio em ValueTrackers."""

    def __init__(self, cena, C, R, th0):
        self._cr = [ValueTracker(float(C[0])), ValueTracker(float(C[1])), ValueTracker(float(R))]
        cena.add(*self._cr)
        super().__init__(cena, C=C, R=R, th0=th0)

    C = property(lambda s: P3(s._cr[0].get_value(), s._cr[1].get_value()), lambda s, v: (s._cr[0].set_value(v[0]), s._cr[1].set_value(v[1])))
    R = property(lambda s: s._cr[2].get_value(), lambda s, v: s._cr[2].set_value(v))

    def move(self, C2, R2):
        k = R2 / self.R
        return [self._cr[0].animate.set_value(C2[0]), self._cr[1].animate.set_value(C2[1]), self._cr[2].animate.set_value(R2),
                self.corpo.animate.scale(k).move_to(C2), Transform(self.ref, tracej(C2, C2 + (R2 + 0.55) * RIGHT, GEO, 2.5, 0.85, z=3)),
                Transform(self.eixo, eixo_mob(C2))]


def selo_r():
    """Selo curto `r CONSTANTE` (PANEL, borda BLUE_L) que aponta para o r que saiu da derivada."""
    t = VGroup(lbl("r", GEO_, 38), txt("CONSTANTE", 24, bold=True)).arrange(RIGHT, buff=0.12)
    bx = RoundedRectangle(corner_radius=0.08, width=t.width + 0.34, height=t.height + 0.24).move_to(t).set_fill(PANEL, 0.9).set_stroke(BLUE_L, 1.6)
    bx._fundo = bx._caixa = True
    g = VGroup(bx, t).set_z_index(30)
    g._selo_tag = True
    return g


class LoteT4(L20):

    def construct(self):
        self.setup_base()
        self.t4()
        self.fim()
        self.relatorio()
        self.gravar_reg()

    def pg(self, src, dst, *mapas, **kw):
        """passo com conferência: todo glifo da mãe e da filha está em algum mapa (senão o MF-Tools põe os índices no vídeo)."""
        a = sorted({j for m in mapas for j in m[0]})
        b = sorted({j for m in mapas for j in m[1]})
        assert a == list(range(len(src[0]))) and b == list(range(len(dst[0]))), (src.get_tex_string(), dst.get_tex_string(), a, b)
        return self.passo(src, dst, *mapas, **kw)

    def hel_rotulos(self, cam, r1=True):
        """Rótulos da hélice PARADA na pose: cotas GEO do eixo aos pontos (por cima e por baixo da pá marcada) e o 282,7 rad/s no vão do cubo."""
        c = projeta3d(cam, (0, -0.07, 0))
        p1, p2 = hel_pt(cam, 0.10, POSE), hel_pt(cam, 0.95, POSE)
        out = {}
        hub = VGroup(lbl(r"282{,}7", VEL, 44), lbl(r"\mathrm{rad/s}", VEL, 38)).arrange(DOWN, buff=0.1).move_to(c + P3(1.85, 0.0))   # v3 §5.14: ao lado do cubo (vão entre as pás), com linha-guia curta
        out["hub"] = hub
        out["hubl"] = Line(c + P3(0.3, 0.0), P3(hub.get_left()[0] - 0.22, c[1])).set_stroke(GEO, 2.2, opacity=0.9).set_z_index(9)
        y2 = c[1] + 0.45
        L2, i2 = M("r_2" if r1 else "r", "=", r"0{,}95", r"\,\mathrm{m}", size=42, cores={0: GEO_, 2: GEO_, 3: GEO_})
        L2.move_to(P3((p2[0] + c[0]) / 2 - 0.15, y2 + 0.42))
        out["c2"], out["l2"], out["i2"] = cota_h(p2[0], c[0], y2), L2, i2
        if r1:
            y1 = c[1] - 0.42
            L1, i1 = M("r_1", "=", r"0{,}10", r"\,\mathrm{m}", size=40, cores={0: GEO_, 2: GEO_, 3: GEO_})
            L1.move_to(P3(p1[0] + 0.1 - L1.width / 2, y1 - 0.34))
            out["c1"], out["l1"], out["i1"] = cota_h(p1[0], c[0], y1), L1, i1
        return out

    def tmt(self, src, dst, ps, pd, size_s, size_d, key_map=None, rt=1.1, extra=()):
        """v3 §7: TransformMatchingTex entre a linha-mãe `src` e a linha nova `dst` da Pilha. As partes (`ps`, `pd`: [(tex, cor)]) são as chaves do
        matching (Mm = o mesmo TeX das linhas eqp, em partes); no fim a linha eqp `dst` assume o lugar dos proxies (mesma posição e mesmo desenho)."""
        print(f"[alg] {self._aid} tmt {' '.join(t for t, _ in pd)[:40]}")
        a = Mm(*ps, size=size_s).move_to(src.get_center())
        b = Mm(*pd, size=size_d).move_to(dst.get_center())
        tops_antes = set(id(m) for m in self.mobjects)
        self._voando = set(id(x) for x in a.get_family()) | set(id(x) for x in b.get_family())
        self._voando_raiz = [a, b]
        self._fontes_extra = [src]
        self.play(TransformMatchingTex(a, b, key_map=key_map), *extra, run_time=max(0.8, rt))
        self._fontes_extra = []
        self._voando, self._voando_raiz = set(), []
        self.remove(a, b)
        self.add(dst)
        self._sobras(tops_antes, [dst] + [getattr(e, "mobject", None) for e in extra])
        self.foco = dst
        return dst

    def t4(self):
        mot = VGroup()
        d = DiscoMov(self, CD, RD, th0=0.5)
        st = {"w": 0.0, "al": 0.0, "t": self.clk.get_value()}
        prog = {"ts": [self.clk.get_value()], "ws": [0.0]}
        modo = {"osc": False, "t0": 0.0}

        def w_em(t):
            ts, ws = prog["ts"], prog["ws"]
            if t >= ts[-1]:
                return ws[-1], 0.0
            k = max(0, int(np.searchsorted(ts, t, side="right")) - 1)
            dt_ = ts[k + 1] - ts[k]
            al_ = (ws[k + 1] - ws[k]) / dt_ if dt_ > 1e-9 else 0.0
            return ws[k] + al_ * (t - ts[k]), al_

        def rampa(dur, w1):
            """ω(t) linear daqui até w1 em `dur` s (α constante na rampa, 0 depois)."""
            t = self.clk.get_value()
            w0, _ = w_em(t)
            ks = [i for i, x in enumerate(prog["ts"]) if x < t]
            prog["ts"] = [prog["ts"][i] for i in ks] + [t, t + dur]
            prog["ws"] = [prog["ws"][i] for i in ks] + [w0, w1]

        def motor(m):
            t = self.clk.get_value()
            dt = t - st["t"]
            st["t"] = t
            if modo["osc"]:
                u = t - modo["t0"]
                st["w"], st["al"] = 0.625 + 0.175 * math.sin(1.6 * u), 0.28 * math.cos(1.6 * u)
            else:
                st["w"], st["al"] = w_em(t)
            d.th.set_value(d.th.get_value() + st["w"] * dt)
        mot.add_updater(motor)
        self.add(mot, d.g)
        # ── T4-1: v_t = rω ──
        self.an("T4-1")
        self.secao("E CADA PONTO DO CORPO?")
        H0a = linha_m(txt("PONTO A DISTÂNCIA", 28, bold=True), lbl("r", GEO_, 50), txt("DO EIXO", 28, bold=True), buff=0.16)
        self.pilha.poe(H0a)                                           # v3 §4: a coluna não fica vazia nos primeiros 5 s
        self.play(FadeIn(H0a), run_time=0.6)
        th_a = d.th.get_value()
        op_s, op_r, op_v, op_tg = (ValueTracker(0.0) for _ in range(4))
        self.add(op_s, op_r, op_v, op_tg)

        def pos_s(th):
            am = (th + th_a) / 2
            return d.C + (d.R + 0.38) * P3(math.cos(am), math.sin(am))

        def pos_th(th):                                            # v3 §6: θ fora do arco, do lado de trás da linha pintada (dentro do setor varrido, nunca sobre o raio nem os pontos)
            return d.C + 1.0 * P3(math.cos(th - 0.45), math.sin(th - 0.45))

        def pos_r(th):
            u, n = d.u(th)
            return d.C + 0.5 * d.R * u + 0.38 * n                  # entre o 1º e o 2º ponto, do lado da frente da linha pintada (fora do setor varrido)

        def ponto():
            th = d.th.get_value()
            C, R = d.C, d.R
            u, n = d.u(th)
            p = d.p(3, th)
            g = VGroup()
            o = op_s.get_value()
            if o > 0.01 and th - th_a > 0.02:                         # D21: só o arco varrido (nunca o círculo inteiro)
                g.add(arco(C, R, th_a, th, ANG, 9, o, z=8), arco(C, 0.6, th_a, th, ANG, 7, o, z=8))
                g.add(escala_op(mtex("s", ANG, 44).move_to(pos_s(th)), o), escala_op(mtex(r"\theta", ANG, 42).move_to(pos_th(th)), o))
            if op_r.get_value() > 0.01:
                g.add(escala_op(mtex("r", GEO_, 44).move_to(pos_r(th)), op_r.get_value()))
            if op_tg.get_value() > 0.01:
                g.add(tracej(p - n * 1.1, p + n * 1.1, WHITE_, 2.5, 0.8 * op_tg.get_value(), z=7))
            ov = op_v.get_value()
            if ov > 0.01:
                L = KV * R * st["w"]
                g.add(seta(p, p + n * L, VEL, 8, tip=min(0.26, 0.45 * L), op=ov, z=11))
                g.add(escala_op(no_esq(mtex("v_t", VEL, 44).move_to(p + n * L / 2 + u * 0.55), d=d), ov))
            return g
        pv = vivo(ponto)
        self.add(pv)
        self.gat("um ponto a uma certa distância do eixo")
        self.play(op_r.animate.set_value(1.0), run_time=0.6)
        self.gat("percorre um arco igual")
        rampa(0.8, 0.33)
        self.play(op_s.animate.set_value(1.0), run_time=0.9)
        A1, ia1 = M("s", "=", "r", r"\theta", size=60, cores={0: ANG, 2: GEO_, 3: ANG})
        self.pilha.poe(A1)
        self.gat("igual a essa distância")
        th_ = d.th.get_value()
        ls, lt_, lr_ = mtex("s", ANG, 44).move_to(pos_s(th_)), mtex(r"\theta", ANG, 42).move_to(pos_th(th_)), mtex("r", GEO_, 44).move_to(pos_r(th_))
        # §5 T4-1: s voa do arco, r da linha pintada, θ do ângulo varrido; o "=" é escrito na vaga
        self.voa([(ls, mp(A1, ia1, [0])), (lr_, mp(A1, ia1, [2])), (lt_, mp(A1, ia1, [3]))], extra=[FadeIn(mp(A1, ia1, [1]))], rt=1.2, origem=False)
        self.gat("como a distância ao eixo não muda")
        rampa(0.6, 0.15)
        self.foco = A1
        self.wait(0.9)
        # d/dt dos dois lados (E do operador, intercalado por x) → o r sai da derivada (GM) → ds/dt vira v_t e dθ/dt vira ω (GM)
        A2, ia2 = M(r"\frac{d}{dt}", "s", "=", r"\frac{d}{dt}", "(", "r", r"\theta", ")", size=58, cores={1: ANG, 5: GEO_, 6: ANG})
        A3, ia3 = M(r"\frac{d}{dt}", "s", "=", r"r\,", r"\frac{d}{dt}", r"\theta", size=58, cores={1: ANG, 3: GEO_, 5: ANG})
        A4, ia4 = M("v_t", "=", "r", r"\omega", size=60, cores={0: VEL, 2: GEO_, 3: VEL})
        self.pilha.poe(A2)
        self.gat("é só derivar dos dois lados")
        rampa(1.6, 0.6)
        # v3 §7: TransformMatchingTex (s, =, r, θ são as partes que se repetem; os d/dt entram novos e os parênteses saem)
        PA1 = [("s", ANG), ("=", None), ("r", GEO_), (r"\theta", ANG)]
        PA2 = [(r"\frac{d}{dt}", None), ("s", ANG), ("=", None), (r"\dfrac{d}{dt}", None), ("(", None), ("r", GEO_), (r"\theta", ANG), (")", None)]
        PA3 = [(r"\frac{d}{dt}", None), ("s", ANG), ("=", None), (r"r\,", GEO_), (r"\dfrac{d}{dt}", None), (r"\theta", ANG)]
        self.tmt(A1, A2, PA1, PA2, 60, 58, rt=1.2, extra=[op_s.animate.set_value(0.0), op_r.animate.set_value(0.0)])
        self.pilha.poe(A3)
        self.tmt(A2, A3, PA2, PA3, 58, 58, key_map={"r": r"r\,"}, rt=1.1)
        sr = selo_r()
        xr = A3[0][ia3[3][0]].get_center()[0]
        self.pilha.poe(sr, dx=max(0.0, xr - X_CONTA - 0.35))
        sr.shift(0.3 * DOWN)
        sr.add(seta(P3(xr, sr.get_top()[1] + 0.03), P3(xr, A3.get_bottom()[1] - 0.2), WHITE_, 3, tip=0.13, z=30))
        self.play(FadeIn(sr), run_time=0.4)
        self.gat("a velocidade do ponto ao longo do círculo")
        self.play(op_v.animate.set_value(1.0), run_time=0.5)
        self.pilha.poe(A4)
        self.gat("é a distância ao eixo vezes a velocidade angular")
        self.pg(A3, A4, (J(ia3, 0, 1), J(ia4, 0)), (J(ia3, 2), J(ia4, 1)), (J(ia3, 3), J(ia4, 2)), (J(ia3, 4, 5), J(ia4, 3)), rt=1.2, origem=False)
        self.foco = A4
        self.gat("ela tem sinal")
        self.pilha.so(A4)
        A5 = linha_m(txt("SINAL:", 28, bold=True), M("v_t", ">", "0", size=48, cores={0: VEL})[0], txt("ANTI-HORÁRIO", 26), buff=0.18)
        self.pilha.poe(A5)
        self.play(FadeIn(A5), run_time=0.9)
        A6, ia6 = M(r"|v_t|", "=", "r", r"|\omega|", size=60, cores={0: VEL, 2: GEO_, 3: VEL})
        A6l = linha_m(txt("RAPIDEZ:", 28, bold=True), A6, buff=0.22)
        self.pilha.poe(A6l)
        self.gat("e a rapidez")
        # GM: as barras do módulo entram em volta de v_t e de ω (intercaladas por x); a palavra RAPIDEZ é escrita antes
        self.pg(A4, A6, ([], [ia6[0][0]]), (J(ia4, 0), ia6[0][1:3]), ([], [ia6[0][3]]), (J(ia4, 1), J(ia6, 1)), (J(ia4, 2), J(ia6, 2)), ([], [ia6[3][0]]),
                (J(ia4, 3), [ia6[3][1]]), ([], [ia6[3][2]]), rt=1.3, origem=False, extra=[FadeIn(A6l[0])])
        self.foco = A6
        self.gat("sempre tangente ao círculo do ponto")
        self.play(op_tg.animate(rate_func=there_and_back).set_value(1.0), run_time=1.4)
        self.ate(0.99)
        # ── T4-2: a hélice (Three.js, câmera do hook) ──
        self.an("T4-2")
        cam = cam_hel(KH4, CH4)
        t0 = self.clk.get_value()
        t_st = t0 + self.ate_t("tem uma velocidade angular só")
        giro = GiroT4(t0, a0_para(t0, t_st))
        f3 = Fundo3D(self, "helice", lambda t: {"ang": round(giro.ang(t), 4), "cam": cam}, op=0.0)
        k_seta, op_set, op_mk, op_ras = ValueTracker(1.0), ValueTracker(0.0), ValueTracker(0.0), ValueTracker(0.0)
        self.add(f3, k_seta, op_set, op_mk, op_ras)
        ch = camada_helice(self, giro, lambda: cam, k_seta, op_set, op_mk, op_rastro=op_ras)
        self.add(ch)
        velhos = [d.g, pv]
        self.pilha.limpa(rt=0.3)
        self.play(*[FadeOut(m) for m in velhos], f3.op.animate.set_value(1.0), op_mk.animate.set_value(1.0), op_set.animate.set_value(1.0),
                  *self.troca_marcador("CÂMERA LENTA ×90", "dir"), run_time=0.8)
        self.remove(*velhos)
        mot.clear_updaters()
        F1, if1 = M("v", "=", "r", r"\omega", size=54, cores={0: VEL, 2: GEO_, 3: VEL})
        F0 = linha_m(txt("O MESMO", 30, bold=True), lbl(r"\omega", VEL, 54), txt("·", 30, bold=True), F1[0], buff=0.2)   # v3 §5.8: uma só chamada curta
        self.pilha.poe(F0)
        self.gat("a hélice inteira")
        self.play(FadeIn(F0), run_time=0.8)
        self.gat("tem uma velocidade angular só")
        giro.parar(self.clk.get_value())                              # S9: a hélice para na pose para os rótulos ficarem presos aos pontos
        self.play(*self.troca_marcador(None), run_time=0.4)
        R_ = self.hel_rotulos(cam)
        self.gat("uns duzentos e oitenta e três")
        self.play(FadeIn(R_["hub"]), Create(R_["hubl"]), run_time=0.7)
        self.gat("mas cada ponto multiplica")
        F2, if2 = M("v_1", "=", r"0{,}10", r"\cdot", r"282{,}7", r"\approx", r"28\ \mathrm{m/s}", size=48, cores={0: VEL, 2: GEO_, 4: VEL, 6: VEL})
        F3, if3 = M("28", r"\cdot", r"3{,}6", r"\approx", r"100\ \mathrm{km/h}", size=48, cores={0: VEL, 4: VEL})
        F4, if4 = M("v_2", "=", r"0{,}95", r"\cdot", r"282{,}7", r"\approx", r"269\ \mathrm{m/s}", size=48, cores={0: VEL, 2: GEO_, 4: VEL, 6: VEL})
        F5, if5 = M("269", r"\cdot", r"3{,}6", r"\approx", r"970\ \mathrm{km/h}", size=48, cores={0: VEL, 4: VEL})
        F5b = caixa_l(F5, VEL)
        self.gat("a dez centímetros")
        self.play(Create(R_["c1"]), FadeIn(R_["l1"]), run_time=0.5)
        self.pilha.poe(F2)
        # §5 T4-2: 0,10 voa da cota de r₁, 282,7 voa do cubo; v₁, =, ·, ≈ e o resultado são escritos na vaga (ordem de x)
        self.voa([(mp(R_["l1"], R_["i1"], [2]), mp(F2, if2, [2])), (R_["hub"][0], mp(F2, if2, [4]))], extra=[FadeIn(mp(F2, if2, [0, 1, 3, 5, 6]))], rt=1.6)
        self.pilha.poe(F3)
        self.gat("uns cem quilômetros")
        # GM × 3,6: o 28 desce, o resto da linha-mãe fica; · 3,6 ≈ 100 km/h entram por x
        self.pg(F2, F3, (J(if2, 0, 1, 2, 3, 4, 5) + if2[6][2:], []), (if2[6][:2], J(if3, 0)), ([], J(if3, 1)), ([], J(if3, 2)), ([], J(if3, 3)), ([], J(if3, 4)),
                rt=1.1, origem=False)
        self.gat("na ponta a noventa e cinco")
        self.pilha.so(F0)                                             # v3 §5.8: a conta do v₁ sai; a da ponta abre um bloco novo sob a chamada
        self.play(Create(R_["c2"]), FadeIn(R_["l2"]), run_time=0.5)
        self.pilha.poe(F4)
        self.voa([(mp(R_["l2"], R_["i2"], [2]), mp(F4, if4, [2])), (R_["hub"][0], mp(F4, if4, [4]))], extra=[FadeIn(mp(F4, if4, [0, 1, 3, 5, 6]))], rt=1.6)
        self.pilha.poe(F5b, dx=0.2)
        self.gat("quase mil quilômetros")
        self.pg(F4, F5, (J(if4, 0, 1, 2, 3, 4, 5) + if4[6][3:], []), (if4[6][:3], J(if5, 0)), ([], J(if5, 1)), ([], J(if5, 2)), ([], J(if5, 3)), ([], J(if5, 4)),
                rt=1.1, origem=False, extra=[FadeIn(F5b[0])])
        self.foco = F5b
        self.gat("o cubo não gira mais devagar")
        rot_ = VGroup(R_["hub"], R_["hubl"], R_["c1"], R_["l1"], R_["c2"], R_["l2"])
        self.play(FadeOut(rot_), run_time=0.4)                        # os rótulos saem antes de as pás voltarem a passar por eles
        self.remove(rot_)
        giro.retomar(self.clk.get_value())
        self.play(*self.troca_marcador("CÂMERA LENTA ×90", "dir"), run_time=0.5)
        self.gat("ele gira junto")
        self.play(op_ras.animate.set_value(1.0), run_time=0.8)        # rastros de mesmo Δt: o cubo gira junto, só que perto do eixo
        self.gat("e essa rapidez na ponta")
        self.foco = F5
        self.wait(0.9)
        self.gat("ela é medida em relação ao eixo")
        self.selo("EM RELAÇÃO AO EIXO", "")
        self.gat("perto da velocidade do som")
        self.foco = F4
        self.wait(0.9)
        self.ate(0.99)
        # ── T4-3: dois pontos opostos ──
        self.an("T4-3")
        self.sem_selo()
        self.pilha.limpa(rt=0.3)
        d = DiscoMov(self, CD, RD, th0=0.9)
        st["t"] = self.clk.get_value()
        prog["ts"], prog["ws"] = [self.clk.get_value()], [0.5]
        mot.add_updater(motor)
        op2, pul, op_rr = ValueTracker(0.0), ValueTracker(0.0), ValueTracker(0.0)
        self.add(op2, pul, op_rr)

        def opostos():
            o = op2.get_value()
            th = d.th.get_value()
            u, n = d.u(th)
            g = VGroup()
            L = KV * d.R * st["w"] * 1.8
            for s_, nm in ((1, r"\vec v_A"), (-1, r"\vec v_B")):
                p = d.C + s_ * d.R * u
                g.add(ponto_mob(p, 0.1, z=12))
                if op_rr.get_value() > 0.01:                         # "à mesma distância do eixo": os dois raios acendem em GEO
                    g.add(Line(d.C, p).set_stroke(GEO, 7, opacity=0.9 * op_rr.get_value()).set_z_index(7))
                if o > 0.01:
                    g.add(seta(p, p + s_ * n * L, VEL, 6 + 3 * pul.get_value(), op=o, z=11))
                    g.add(escala_op(no_esq(mtex(nm, VEL, 44).move_to(pos_vab(p, s_, u, n, L)), d=d), o))
            if not PEDIDOS3D and o > 0.5:
                self.reg("opostos", L1=L, L2=L, d=(d.R * u + n * L - (-d.R * u - n * L)).tolist())
            return g
        ov = vivo(opostos)

        def lab_op(s_):
            th = d.th.get_value()
            u, n = d.u(th)
            L = KV * d.R * st["w"] * 1.8
            return no_esq(mtex(r"\vec v_A" if s_ > 0 else r"\vec v_B", VEL, 44).move_to(pos_vab(d.C + s_ * d.R * u, s_, u, n, L)), d=d)
        velhos = [f3, ch] + ([self._marc] if getattr(self, "_marc", None) is not None else [])
        self._marc = None
        self.troca(velhos, FadeIn(d.g), FadeIn(ov), seq=True)
        H3a = linha_m(txt("DOIS PONTOS OPOSTOS DO CORPO", 28, bold=True), buff=0.16)
        self.pilha.poe(H3a)                                           # v3 §4: a coluna não fica vazia nos primeiros 6 s
        self.play(FadeIn(H3a), run_time=0.5)
        self.gat("olha esses dois pontos")
        self.play(op2.animate.set_value(1.0), run_time=0.7)
        H3b = linha_m(txt("MESMA DISTÂNCIA", 28, bold=True), lbl("r", GEO_, 50), txt("DO EIXO", 28, bold=True), buff=0.16)
        self.pilha.poe(H3b)
        self.gat("à mesma distância do eixo")
        self.play(op_rr.animate.set_value(1.0), FadeIn(H3b), run_time=0.6)
        G1, ig1 = M(r"|\vec v_A|", "=", r"|\vec v_B|", "=", "r", r"\omega", size=56, cores={0: VEL, 2: VEL, 4: GEO_, 5: VEL})
        G2, ig2 = M(r"\vec v_A", "=", "-", r"\vec v_B", size=56, cores={0: VEL, 3: VEL})
        self.pilha.poe(G1)
        self.gat("o tamanho da velocidade é o mesmo")
        # D22: v⃗_A e v⃗_B voam das setas (com as barras do módulo: o de fechamento nunca antes do que está dentro)
        self.voa([(lab_op(1), mp(G1, ig1, [0])), (lab_op(-1), mp(G1, ig1, [2]))], extra=[FadeIn(mp(G1, ig1, [1, 3, 4, 5]))], rt=1.4, origem=False)
        self.pilha.poe(G2)
        self.gat("mas as setas apontam")
        th = d.th.get_value()
        u, n = d.u(th)
        pB = d.C - d.R * u
        sB = seta(pB, pB - n * KV * d.R * st["w"] * 1.8, VEL, 6, z=11)
        # o sinal "−" sai da seta de B (a que aponta ao contrário)
        self.voa([(lab_op(1), mp(G2, ig2, [0])), (sB, mp(G2, ig2, [2])), (lab_op(-1), mp(G2, ig2, [3]))], extra=[FadeIn(mp(G2, ig2, [1]))], rt=1.3, origem=False)
        fr2 = VGroup(txt("MESMA RAPIDEZ", 32, bold=True), txt("VELOCIDADES OPOSTAS", 32, bold=True)).arrange(DOWN, buff=0.18, aligned_edge=LEFT)
        self.pilha.poe(fr2)
        self.gat("mesma rapidez velocidades diferentes")
        self.play(FadeIn(fr2), run_time=0.6)
        self.gat("a fórmula que a gente acabou de ver")
        self.foco = G1
        self.wait(0.9)
        self.gat("a direção completa no espaço")
        self.play(pul.animate(rate_func=there_and_back).set_value(1.0), run_time=1.0)
        self.ate(0.99)
        # ── T4-4: a_t = rα ──
        self.an("T4-4")
        self.pilha.limpa(rt=0.3, anims=[op2.animate.set_value(0.0)])
        self.remove(ov)
        prog["ts"], prog["ws"] = [self.clk.get_value()], [st["w"]]
        rampa(0.4, 0.55)
        op_v.set_value(0.0)
        op_t, op_c = ValueTracker(0.0), ValueTracker(0.0)
        self.add(op_t, op_c)

        def acel():
            th = d.th.get_value()
            p = d.p(3, th)
            u, n = d.u(th)
            g = VGroup()
            w_, al_ = st["w"], st["al"]
            Lv = KV * d.R * w_
            ov_ = op_v.get_value()
            if ov_ > 0.01:
                g.add(seta(p, p + n * Lv, VEL, 6, op=ov_, z=11))
                g.add(escala_op(no_esq(mtex("v", VEL, 44).move_to(p + n * Lv * 0.45 + u * 0.4), d=d), ov_))
            at, ac = d.R * al_, w_ * w_ * d.R
            ot = op_t.get_value() * min(1.0, abs(at) * KT / 0.18)
            if ot > 0.01:                                          # D23: acelerando, a seta verde nasce na ponta da violeta; freando, nasce no ponto e aponta para trás
                q0 = p + n * Lv if at > 0 else p
                q1 = q0 + n * at * KT
                g.add(seta(q0, q1, ACC, 6, op=ot, z=12))
                g.add(escala_op(no_esq(mtex("a_t", ACC, 44).move_to(q1 + np.sign(at) * n * 0.42 + u * 0.12), d=d), ot))
                if not PEDIDOS3D:
                    self.reg("t4_acel", at=at, ac=ac, Lt=abs(at) * KT, Lv=Lv, w=w_, al=al_)
            oc = op_c.get_value()
            if oc > 0.01:                                          # a_c para o eixo; o rótulo fica fora do disco, do lado de fora do ponto
                g.add(seta(p, p - u * ac * KC, ACC, 6, op=oc, z=12))
                g.add(escala_op(no_esq(mtex("a_c", ACC, 44).move_to(p + u * 0.42 - n * 0.42), d=d), oc))
            return g
        av = vivo(acel)
        self.add(av)
        K1, ik1 = M("v_t", "=", "r", r"\omega", size=60, cores={0: VEL, 2: GEO_, 3: VEL})
        K2, ik2 = M(r"\frac{d}{dt}", "v_t", "=", r"r\,", r"\frac{d}{dt}", r"\omega", size=58, cores={1: VEL, 3: GEO_, 5: VEL})
        K3, ik3 = M("a_t", "=", r"r\,", r"\alpha", size=60, cores={0: ACC, 2: GEO_, 3: ACC})
        self.pilha.poe(K1)
        self.gat("derivando mais uma vez")
        self.play(FadeIn(K1), op_v.animate.set_value(1.0), run_time=0.8)
        self.pilha.poe(K2)
        self.gat("se o giro acelera")
        rampa(13.8, 1.0)                                              # acelera até "quando o giro acelera"; freia em "contra ela quando freia"
        # d/dt dos dois lados: o d e a barra nascem com o v_t (numerador → barra → denominador), o r fica fora
        # v3 §7: TransformMatchingTex (v_t, =, r, ω se repetem; os d/dt entram novos); d/dt à esquerda como no T4-1
        PK1 = [("v_t", VEL), ("=", None), ("r", GEO_), (r"\omega", VEL)]
        PK2 = [(r"\frac{d}{dt}", None), ("v_t", VEL), ("=", None), (r"r\,", GEO_), (r"\dfrac{d}{dt}", None), (r"\omega", VEL)]
        PK3 = [("a_t", ACC), ("=", None), (r"r\,", GEO_), (r"\alpha", ACC)]
        self.tmt(K1, K2, PK1, PK2, 60, 58, key_map={"r": r"r\,"}, rt=1.2)
        self.gat("acelera a velocidade do ponto")
        self.play(op_t.animate.set_value(1.0), run_time=0.6)
        self.pilha.poe(K3)
        self.gat("essa é a aceleração tangencial")
        self.tmt(K2, K3, PK2, PK3, 58, 60, key_map={"v_t": "a_t", r"\omega": r"\alpha"}, rt=1.2)
        self.foco = K3
        self.gat("a distância ao eixo vezes a aceleração angular")
        self.foco = K3
        self.wait(0.9)
        self.gat("contra ela quando freia")
        rampa(2.0, 0.86)
        self.wait(1.2)
        self.ate(0.99)
        # ── T4-5: a_c = ω²r ──
        self.an("T4-5")
        rampa(1.0, 0.7)
        self.play(op_t.animate.set_value(0.0), run_time=0.5)
        self.gat("sem aceleração angular nenhuma")
        self.pilha.limpa(rt=0.3)
        N1 = M(r"\alpha", "=", "0", r"\ \Rightarrow\ ", "a_t", "=", "0", size=50, cores={0: ACC, 4: ACC})[0]
        self.pilha.poe(N1)
        self.play(FadeIn(N1), run_time=0.9)
        self.gat("é a aceleração centrípeta")
        self.play(op_c.animate.set_value(1.0), run_time=0.7)
        C1, ic1 = M("a_c", "=", r"\frac{v^2}{r}", size=58, cores={0: ACC})
        C2, ic2 = M("=", r"\frac{(r\omega)^2}{r}", size=58)
        C3, ic3 = M("=", r"\frac{r^2\omega^2}{r}", size=58)
        C4, ic4 = M("=", r"\omega^2", "r", size=58, cores={1: VEL, 2: GEO_})
        for Mx, ix, cs in ((C1, ic1[2], (VEL, VEL, WHITE_, GEO_)), (C2, ic2[1], (WHITE_, GEO_, VEL, WHITE_, VEL, WHITE_, GEO_)),
                           (C3, ic3[1], (GEO_, GEO_, VEL, VEL, WHITE_, GEO_))):
            for j, c in zip(ix, cs):
                Mx[0][j].set_color(c)
                Mx[0][j].set_stroke(c, width=1.8 if c != WHITE_ else 0, background=False)
        self.pilha.poe(C1)
        self.gat("velocidade ao quadrado dividida")
        th = d.th.get_value()
        u, n = d.u(th)
        p = d.p(3, th)
        Lv = KV * d.R * st["w"]
        lv = mtex("v", VEL, 44).move_to(p + n * Lv * 0.45 + u * 0.4)
        lac = mtex("a_c", ACC, 44).move_to(p + u * 0.42 - n * 0.42)
        # §5 T4-5: a_c voa do rótulo da seta verde, v do rótulo da violeta; =, ², barra e r escritos na vaga (numerador → barra → denominador)
        # (o v pousa junto com a barra: sozinha, a barra, mais larga, nasceria antes do numerador)
        self.voa([(lac, mp(C1, ic1, [0])), (lv, gl(C1, [ic1[2][0], ic1[2][2]]))], extra=[FadeIn(mp(C1, ic1, [1])), FadeIn(gl(C1, [ic1[2][1], ic1[2][3]]))],
                 rt=1.2, origem=False)
        self.pilha.poe(C2)
        self.gat("trocando a velocidade pela distância")
        # GM substituição: v → (rω); o ² e a barra e o r ficam (o a_c da mãe não desce)
        self.pg(C1, C2, (J(ic1, 0), []), (J(ic1, 1), J(ic2, 0)), (ic1[2][:1], ic2[1][:4]), (ic1[2][1:2], ic2[1][4:5]), (ic1[2][2:3], ic2[1][5:6]),
                (ic1[2][3:4], ic2[1][6:7]), rt=1.2, origem=False)
        self.pilha.poe(C3)
        # GM: o quadrado entra no parêntese (o ² se duplica: r² e ω²); os parênteses saem antes
        self.pg(C2, C3, (J(ic2, 0), J(ic3, 0)), (ic2[1][0:1], []), (ic2[1][1:2], ic3[1][0:1]), (ic2[1][2:3], ic3[1][2:3]), (ic2[1][3:4], []),
                (ic2[1][4:5], ic3[1][1:2]), ([], ic3[1][3:4]), (ic2[1][5:6], ic3[1][4:5]), (ic2[1][6:7], ic3[1][5:6]), rt=1.0, origem=False)
        self.gat("fica velocidade angular ao quadrado")
        rk1 = risco(VGroup(C3[0][ic3[1][1]]), cor=WHITE_, w=3)
        rk2 = risco(VGroup(C3[0][ic3[1][5]]), cor=WHITE_, w=3)
        self.play(Create(rk1), Create(rk2), run_time=0.5)
        self.pilha.poe(C4)
        # GM cancelamento: um r de cima (o expoente riscado) e o r de baixo saem primeiro; o r que sobra vai para depois do ω²
        self.pg(C3, C4, (J(ic3, 0), J(ic4, 0)), (ic3[1][0:1], J(ic4, 2)), (ic3[1][1:2], []), (ic3[1][2:4], J(ic4, 1)), (ic3[1][4:5], []), (ic3[1][5:6], []),
                rt=1.2, origem=False, extra=[FadeOut(rk1), FadeOut(rk2)])
        self.foco = C4
        self.gat("e ela aponta sempre para o eixo")
        self.foco = C4
        self.wait(0.9)
        self.ate(0.99)
        # ── T4-6: a soma e φ (inset ×2,5); fecho na hélice ──
        self.an("T4-6")
        self.pilha.limpa(rt=0.3, anims=[op_c.animate.set_value(0.0), op_v.animate.set_value(0.0)])
        modo["osc"], modo["t0"] = True, self.clk.get_value() - 0.6
        Z6, Zc = C6 + R6 * UP, C6 + (R6 - 0.2) * UP                    # ponto da borda ampliado (o topo do disco) e o centro da lupa
        Zi = CI + ZOOM * (Z6 - Zc)                                      # o ponto dentro do inset
        lupa = Circle(radius=RI / ZOOM).move_to(Zc).set_stroke(GEO, 2.4).set_z_index(13)
        moldura = Circle(radius=RI).move_to(CI).set_stroke(GEO, 3).set_fill(PANEL, 0.92).set_z_index(13)
        moldura._fundo = True
        Cr = CI + ZOOM * (C6 - Zc)
        miolo = Intersection(Circle(radius=RI - 0.02).move_to(CI), Circle(radius=ZOOM * R6).move_to(Cr)).set_stroke(width=0).set_fill("#3A4252", 0.85).set_z_index(13)
        bmax = math.acos(max(-1.0, min(1.0, (np.linalg.norm(CI - Cr) ** 2 + (ZOOM * R6) ** 2 - (RI - 0.03) ** 2) / (2 * np.linalg.norm(CI - Cr) * ZOOM * R6))))
        borda = Arc(radius=ZOOM * R6, start_angle=PI / 2 - bmax, angle=2 * bmax, arc_center=Cr).set_stroke("#7FB2FF", 3).set_z_index(13)
        q_a = Zc + RI / ZOOM * P3(math.cos(0.35), math.sin(0.35))
        q_b = CI + RI * P3(math.cos(PI + 0.35), math.sin(PI + 0.35))
        guia = Line(q_a, q_b).set_stroke(GEO, 2.2, opacity=0.9).set_z_index(13)
        esc = lbl(r"\times 2{,}5", GEO_, 36).move_to(CI + P3(1.25, 1.25))
        inset_g = VGroup(lupa, guia, moldura, miolo, borda, esc)
        op6, op6t, op6c, op6s, op6f = (ValueTracker(0.0) for _ in range(5))
        self.add(op6, op6t, op6c, op6s, op6f)
        ANC6 = {"ac+": CI + P3(0.55, -RI - 0.42), "ac-": CI + P3(-0.55, -RI - 0.42), "at+": CI + 1.62 * P3(math.cos(2.7), math.sin(2.7)), "at-": CI + 1.62 * P3(math.cos(0.44), math.sin(0.44)),
                "a+": CI + 1.62 * P3(math.cos(3.84), math.sin(3.84)), "a-": CI + 1.62 * P3(math.cos(5.58), math.sin(5.58)),
                "f+": CI + 1.62 * P3(math.cos(4.36), math.sin(4.36)), "f-": CI + 1.62 * P3(math.cos(5.06), math.sin(5.06))}

        def rot6(nome, sg):
            tex_, cor = {"ac": ("a_c", ACC), "at": ("a_t", ACC), "a": ("a", ACC), "f": (r"\varphi", ANG)}[nome]
            return mtex(tex_, cor, 42).move_to(ANC6[nome + ("+" if sg >= 0 else "-")])

        def zoom6():
            o = op6.get_value()
            if o < 0.01:
                return VGroup()
            w_, al_ = st["w"], st["al"]
            R = d.R
            at, ac = R * al_, w_ * w_ * R
            sg = 1 if at >= 0 else -1
            phi = math.atan2(abs(at), ac)
            g = VGroup()
            tg, rad = LEFT, DOWN                                      # no topo da borda: tangente (anti-horário) para a esquerda, eixo para baixo
            vt, vc = tg * at * KA, rad * ac * KA
            ot, oc, os_ = op6t.get_value() * o, op6c.get_value() * o, op6s.get_value() * o
            for (q, k, wd, tp) in ((Z6, 1.0, 5, 0.12), (Zi, ZOOM, 8, 0.26)):          # no disco (pequenas) e no inset (×2,5)
                if ot > 0.01 and abs(at) * KA * k > 0.03:
                    g.add(seta(q, q + vt * k, ACC, wd, tip=tp, op=ot, z=14))
                if oc > 0.01:
                    g.add(seta(q, q + vc * k, ACC, wd, tip=tp, op=oc, z=14))
                if os_ > 0.01:
                    g.add(seta(q, q + (vt + vc) * k, ACC, wd + 2, tip=tp * 1.1, op=os_, z=15))
            if o > 0.01:
                g.add(ponto_mob(Zi, 0.09, z=16))
            if os_ > 0.01:
                fl = op6f.get_value()                                 # "medido a partir da direção que aponta para o eixo": a referência e o arco acendem
                g.add(tracej(Zi, Zi + rad * 1.25, WHITE_, 2 + 2 * fl, (0.65 + 0.35 * fl) * os_, z=14))
                if phi > 0.02:
                    g.add(arco(Zi, 0.55, -PI / 2, -PI / 2 - sg * phi, ANG, 5 + 4 * fl, os_, z=15))
            if ot > 0.01:
                g.add(escala_op(rot6("at", sg), ot))
            if oc > 0.01:
                g.add(escala_op(rot6("ac", sg), oc))
            if os_ > 0.01:
                g.add(escala_op(rot6("a", sg), os_), escala_op(rot6("f", sg), os_))
                if not PEDIDOS3D:
                    self.reg("t4_6", at=at, ac=ac, phi=math.degrees(phi), Lt=abs(at) * KA, Lc=ac * KA, w=w_, al=al_)
            return g
        zv = vivo(zoom6)
        self.add(zv)
        self.play(*d.move(C6, R6), run_time=1.0)
        self.gat("cada ponto tem duas acelerações")
        self.play(FadeIn(inset_g), op6.animate.set_value(1.0), run_time=0.8)
        P1, ip1 = M("a_t", "=", "r", r"\alpha", size=58, cores={0: ACC, 2: GEO_, 3: ACC})
        P2, ip2 = M("a_c", "=", r"\omega^2", "r", size=58, cores={0: ACC, 2: VEL, 3: GEO_})
        P3_, ip3 = M("a", "=", r"\sqrt{a_t^2+a_c^2}", size=58, cores={0: ACC, 2: ACC})
        P4, ip4 = M(r"\tan\varphi", "=", r"\frac{|a_t|}{a_c}", size=58, cores={2: ACC})
        P4[0][ip4[0][3]].set_color(ANG)
        P4[0][ip4[0][3]].set_stroke(ANG, width=1.8, background=False)

        def sg6():
            return 1 if st["al"] >= 0 else -1
        self.gat("a tangencial que muda o tamanho")
        self.play(op6t.animate.set_value(1.0), run_time=0.6)
        self.pilha.poe(P1)
        self.voa([(rot6("at", sg6()), mp(P1, ip1, [0]))], extra=[FadeIn(mp(P1, ip1, [1, 2, 3]))], rt=1.0, origem=False)
        self.gat("e a centrípeta que muda")
        self.play(op6c.animate.set_value(1.0), run_time=0.6)
        self.pilha.poe(P2)
        self.voa([(rot6("ac", sg6()), mp(P2, ip2, [0]))], extra=[FadeIn(mp(P2, ip2, [1, 2, 3]))], rt=1.0, origem=False)
        self.gat("a aceleração total é a soma")
        self.play(op6s.animate.set_value(1.0), run_time=0.8)
        self.pilha.poe(P3_)
        self.gat("o tamanho vem do pitágoras")
        # raiz: símbolo → radicando; a_t² + voa do rótulo de a_t, a_c² do rótulo de a_c
        self.voa([(rot6("at", sg6()), gl(P3_, ip3[2][2:6])), (rot6("ac", sg6()), gl(P3_, ip3[2][6:9]))],
                 extra=[FadeIn(mp(P3_, ip3, [0, 1])), FadeIn(gl(P3_, ip3[2][:2]))], rt=1.3, origem=False)
        self.gat("e o ângulo dela medido a partir")
        self.play(op6f.animate(rate_func=there_and_back).set_value(1.0), run_time=0.9)
        self.pilha.poe(P4)
        self.gat("tem tangente igual")
        self.voa([(rot6("f", sg6()), gl(P4, ip4[0][3:4])), (rot6("at", sg6()), gl(P4, ip4[2][:5])), (rot6("ac", sg6()), gl(P4, ip4[2][5:]))],
                 extra=[FadeIn(gl(P4, ip4[0][:3])), FadeIn(mp(P4, ip4, [1]))], rt=1.3, origem=False)
        self.foco = P4
        self.gat("para a frente se o giro acelera")
        self.foco = P4
        self.wait(0.9)
        # fecho: a hélice grande volta, com a seta verde para o eixo na ponta
        self.gat("repara também que a centrípeta cresce")
        self.pilha.limpa(rt=0.3)
        t0 = self.clk.get_value()
        t_st6 = t0 + self.ate_t("na ponta da hélice")
        giro6 = GiroT4(t0, a0_para(t0, t_st6))
        f6 = Fundo3D(self, "helice", lambda t: {"ang": round(giro6.ang(t), 4), "cam": cam}, op=0.0)
        op_h, op_hl = ValueTracker(0.0), ValueTracker(0.0)
        self.add(f6, op_h, op_hl)

        def ponta():
            o = op_h.get_value()
            if o < 0.01:
                return VGroup()
            a = giro6.ang(self.clk.get_value())
            p = hel_pt(cam, 0.95, a)
            c = projeta3d(cam, (0, -0.07, 0))
            uu = (c - p) / max(np.linalg.norm(c - p), 1e-6)
            Lh = 0.55 * float(np.linalg.norm(c - p))                      # v3 §5.6: a seta de a_c cresce com a hélice (G8)
            g = VGroup(seta(p, p + uu * Lh, ACC, 9, tip=0.3, op=o, z=12), escala_op(ponto_mob(p, 0.09, z=13), o))
            if op_hl.get_value() > 0.01:
                g.add(escala_op(mtex("a_c", ACC, 46).move_to(p + uu * Lh / 2 + P3(0, -0.5)), op_hl.get_value()))
            if not PEDIDOS3D:
                self.reg("helice6", p=p, ang=a)
            return g
        hp = vivo(ponta)
        self.add(hp)
        velhos = [d.g, zv, inset_g]
        self.play(*[FadeOut(m) for m in velhos], f6.op.animate.set_value(1.0), *self.troca_marcador("CÂMERA LENTA ×90", "dir"), run_time=0.5)
        self.remove(*velhos)                                          # a seta verde da ponta só entra depois que os rótulos do inset saíram
        mot.clear_updaters()
        H1 = M("a_c", "=", r"\omega^2", "r", size=58, cores={0: ACC, 2: VEL, 3: GEO_})
        H0 = txt("NA PONTA DA HÉLICE", 30, bold=True)               # título em linha própria: o "=" da conta fica perto da borda (nada encolhe)
        H1l = H1[0]
        self.pilha.poe(H0)                                            # v3 §5.6: a coluna entra junto com a hélice (nada de coluna vazia)
        self.play(op_h.animate.set_value(1.0), FadeIn(H0), run_time=0.5)
        self.pilha.poe(H1l)
        self.play(FadeIn(H1l), run_time=0.6)
        H2, ih2 = M("=", r"282{,}7^2", r"\cdot", r"0{,}95", size=56, cores={1: VEL, 3: GEO_})
        H3 = M(r"\approx", r"7{,}6\times 10^4\ \mathrm{m/s^2}", size=56, cores={1: ACC})[0]
        H4 = M("a_c", r"\approx", r"7{.}750\ g", size=58, cores={0: ACC, 2: ACC})[0]
        H4b = caixa_l(H4, ACC)
        self.gat("com o quadrado da velocidade angular")
        self.foco = H1l
        self.gat("na ponta da hélice")
        giro6.parar(self.clk.get_value())
        self.play(*self.troca_marcador(None), run_time=0.25)                       # um marcador por vez: o velho sai antes
        self.play(*self.troca_marcador("FORA DE ESCALA", "dir"), run_time=0.3)
        R6_ = self.hel_rotulos(cam, r1=False)
        self.gat("dá uns setenta")
        self.play(FadeIn(R6_["hub"]), Create(R6_["hubl"]), Create(R6_["c2"]), FadeIn(R6_["l2"]), op_hl.animate.set_value(1.0), run_time=0.6)
        self.pilha.poe(H2)
        # §5 T4-6: 282,7 voa do cubo e 0,95 da cota da ponta; o ² nasce junto da base
        self.voa([(R6_["hub"][0], gl(H2, ih2[1][:5])), (mp(R6_["l2"], R6_["i2"], [2]), mp(H2, ih2, [3]))],
                 extra=[FadeIn(mp(H2, ih2, [0, 2])), FadeIn(gl(H2, ih2[1][5:]))], rt=1.3)
        self.pilha.poe(H3, dx=max(0.0, H2[0][ih2[0][0]].get_left()[0] - X_CONTA))
        self.play(FadeIn(H3), run_time=0.9)
        self.pilha.poe(H4b, dx=0.2)
        self.gat("perto de sete mil e setecentas")
        self.play(FadeIn(H4b), run_time=1.0)
        self.foco = H4b
        self.ate(0.99)

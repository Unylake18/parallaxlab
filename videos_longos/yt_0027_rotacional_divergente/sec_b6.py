"""Lote PB6 · NO ESPAÇO (handoff v3 §3.3; alvo v3 05 e v2 18, 19). Three.js à esquerda (caixa 150–1070 × 170–950 px), fórmulas na coluna x = 1120.
B6-1 (v3): `cubo` = cubo3 — chapa a 32 %, uma seta por parede (entra 0,55 / sai 1,1), câmera do lado (+x, +y, +z) com giro de 10° em azimute que para
no quadro do alvo quando a fórmula termina; cada par de paredes acende (moldura da cor do eixo) quando a parcela correspondente é escrita.
B6-2: `roda` — n sai de W e inclina até ⟂ W em 6 s; rapidez W·n (fase = ∫ W·n dt); eixo do giro tracejado; ω_roda em número (1,00 → 0,00), sem texto
de depuração (S12). B6-3: n volta a W em 2 s; a seta violeta do rot cresce (comprimento 2|W|); determinante, rot = ∇ × F com as legendas DIREÇÃO/TAMANHO
logo abaixo e div = ∇ · F por último (S13).
v4: B6-0 novo (§3.3, alvo 16): EM QUALQUER DIMENSÃO, Ω ⊂ ℝⁿ, div geral, painéis n = 2 e n = 3; o painel n = 3 fica e desce para a coluna do cubo.
B6-1: as setas de cada par crescem e o par acende quando a sua parcela é escrita. B6-3 (§3.4, alvo 17): legendas embaixo da rodinha; coluna em x = 1000
com o determinante, a forma aberta (a 3ª componente pisca em violeta), ∇ × F e ∇ · F. Câmera da roda menor e à esquerda (cabe a coluna em 1000)."""
from v27 import *  # noqa: F401,F403

S35, C35 = math.sin(math.radians(35)), math.cos(math.radians(35))
W = np.array([S35, 0.0, C35])
U = np.array([C35, 0.0, -S35])
XC, YC = (610 - 960) / 120, 4.5 - 560 / 120          # centro da caixa do 3D (610, 560) px
CAM_R = cam_obl(-41.2, 15.1, (0.2, 0, 0.1), K=1.30, xc=(500 - 960) / 120, yc=4.5 - 545 / 120)      # v4: centro (500, 545) px, 90 % do v3
AZ_ALVO = 36.5                                        # câmera do alvo 05 (sonda renders/v2/qa/sonda_cubo3_lado.png)


def cam_cubo(az):
    return cam_obl(az, 29.2, (0, 0, -0.08), K=1.75, xc=-3.0, yc=-0.08)


def inicio_glifo(m, cor, ritmo=1.0, atraso=0.0):
    """Fração do run_time da caneta(m) em que TERMINA o primeiro glifo da cor `cor` (mesma ordem de glifos da _Caneta)."""
    gs = sorted(glifos(m), key=lambda g: (round(g.get_left()[0], 2), -g.get_center()[1]))
    passo, dg = PASSO * ritmo, DG * ritmo
    tot = atraso + passo * max(0, len(gs) - 1) + dg
    alvo = ManimColor(cor).to_hex().upper()
    i = next(k for k, g in enumerate(gs) if ManimColor(g.get_fill_color()).to_hex().upper() == alvo)
    return min(1.0, (atraso + passo * i + dg) / tot)


class EstadoRoda:
    """Estado por quadro: β (inclinação de n a partir de W, para o lado U) e rot vêm de ValueTrackers; fase = ∫ W·n dt (|W| = 1 rad/s, tempo de tela)."""

    def __init__(self, beta, rot, eixo):
        self.beta, self.rot, self.eixo = beta, rot, eixo
        self.cache, self.f_ult, self.fase, self.rap = {}, None, 0.0, []

    def n(self):
        b = self.beta.get_value()
        return math.cos(b) * W + math.sin(b) * U

    def __call__(self, t):
        f = int(round(t * FPS))
        if f in self.cache:
            return self.cache[f]
        n = self.n()
        wn = float(W @ n)
        if self.f_ult is not None and f > self.f_ult:
            self.fase += wn * (f - self.f_ult) / FPS
        self.f_ult = f
        self.rap.append((f, wn))
        e = {"cam": CAM_R, "n": [float(v) for v in n], "fase": self.fase, "giro": 0.6 * t, "rot": self.rot.get_value(), "eixo": bool(self.eixo.get_value() > 0.5)}
        self.cache[f] = e
        return e


class LoteB6(Base):
    ANTES = "A FALSA FONTE"

    def corpo(self):
        # ── B6-0 · em qualquer dimensão (v4 §3.3, alvo 16) ──
        self.an("B6-0")
        self.secao("NO ESPAÇO")
        F1 = r"\textcolor{cc}{F_1}"
        F2 = r"\textcolor{cc}{F_2}"
        F3 = r"\textcolor{cc}{F_3}"
        Fn = r"\textcolor{cc}{F_n}"
        tit = T("EM QUALQUER DIMENSÃO", 960, 215, 46, "center")
        l1 = TC(r"\Omega \subset \mathbb{R}^n \ \text{aberto}, \qquad \F = (" + F1 + r",\ " + F2 + r",\ \dots,\ " + Fn + ")", 960, 310, 48, "c")
        lg1 = legenda("CADA COMPONENTE COM DERIVADAS PARCIAIS EM Ω", 960, 385, GEO, "center")
        dg = TC(r"\dv \F = \dfrac{\partial " + F1 + r"}{\partial x_1} + \dfrac{\partial " + F2 + r"}{\partial x_2} + \cdots + \dfrac{\partial " + Fn + r"}{\partial x_n}", 960, 505, 62, "c")
        p2, p3 = painel(150, 620, 780, 170), painel(990, 620, 780, 170)
        g2 = VGroup(p2, legenda_mat(["NO PLANO", (r"(n = 2)",)], 540, 668), TC("(" + F1 + "," + F2 + r") = (\Pp,\Qq) \qquad (x_1,x_2) = (\X,\Y)", 540, 735, 40, "c", caneta=False))
        g3 = VGroup(p3, legenda_mat(["NO ESPAÇO", (r"(n = 3)",)], 1380, 668),
                    TC("(" + F1 + "," + F2 + "," + F3 + r") = (\Pp,\Qq,\Rr) \quad (x_1,x_2,x_3) = (\X,\Y,\Z)", 1380, 735, 31, "c", caneta=False))
        g2[2]._esc = g3[2]._esc = True
        pe = VGroup(legenda_mat(["DIVERGENTE: VALE EM QUALQUER", ("n",)], 960, 880, SAI), legenda("ROTACIONAL: CAMPO NO ESPAÇO (O DO PLANO É O CASO R = 0)", 960, 935, VEL, "center"))
        self.play(FadeIn(tit, shift=0.1 * DOWN), run_time=0.6)
        self.gat("a definição do divergente")                                  # final: a voz real é mais rápida; Ω e F começam aqui
        self.play(caneta(l1))
        self.gat("tem n componentes")
        self.play(FadeIn(lg1), run_time=0.4)
        self.gat("e o divergente é a soma")
        self.play(caneta(dg), self.em("no plano as duas componentes", self.surge(g2)))
        self.gat("no espaço chega o r")
        self.play(FadeIn(g3, shift=0.1 * UP), run_time=0.6)
        self.gat("já o rotacional")
        self.play(FadeIn(pe[0]), run_time=0.4)
        self.play(FadeIn(pe[1]), run_time=0.4)
        self.ate(0.97)

        # ── B6-1 · cubo3 (o painel n = 3 fica e desce para a coluna; o resto sai enquanto o cubo entra) ──
        self.an("B6-1")
        onda, az = ValueTracker(0.0), ValueTracker(AZ_ALVO + 6.0)
        ac = [ValueTracker(0.0) for _ in range(3)]
        cubo = Fundo3D(self, "cubo", lambda t: {"cam": cam_cubo(az.get_value()), "onda": onda.get_value(),
                                                "acende": [int(a.get_value() > 0.5) for a in ac]}, op=0.0)
        sai0 = [m_ for m_ in self.snap() if m_ not in g3 and m_ is not g3]
        self.add(cubo)
        self.grade()                                                          # final: no 3D o fundo fica liso (a grade ficaria por cima do PNG 3D)
        self.play(*[FadeOut(m_) for m_ in sai0], cubo.op.animate.set_value(1.0), g3.animate.scale(0.78).move_to(PX(1124 + 0.78 * 390, 690 + 0.78 * 85)), run_time=0.8)
        self.remove(*sai0)
        fD = TC(r"\dv \F = \dfrac{\partial \Pp}{\dx} + \dfrac{\partial \Qq}{\dy} + \dfrac{\partial \Rr}{\dz}", 1120, 380, 50)
        fr = [inicio_glifo(fD, c) for c in ("#FFC24D", "#EA63FF", "#35D9FF")]       # o x, o y e o z dos denominadores
        print(f"[cubo3] B6-1: cada par cresce e acende com a sua parcela: {', '.join(f'{f:.2f}' for f in fr)} da caneta (x, y, z)")
        self.gat("o divergente tem três parcelas")
        cn = caneta(fD)
        r_onda = lambda u: sum(min(1.0, max(0.0, (u - s_ + 0.18) / 0.18)) for s_ in fr) / 3.0
        f04 = 0.4 / cn.tot                                                       # final §2.7: o painel n = 3 sai em 0,4 s no começo da frase
        self.play(cn, az.animate.set_value(AZ_ALVO), onda.animate(rate_func=r_onda).set_value(3.0), FadeOut(g3, rate_func=lambda u: smooth(min(1.0, u / f04))),
                  *[a.animate(rate_func=lambda u, s=s: 1.0 if u >= s else 0.0).set_value(1.0) for a, s in zip(ac, fr)])
        self.remove(g3)
        print(f"[cubo3] B6-1: câmera parada em az = {az.get_value():.2f}° (alvo {AZ_ALVO}°) no fim da fórmula")
        self.gat("com seis paredes")
        self.play(FadeIn(legenda("CADA PAR DE PAREDES: SAI − ENTRA", 1124, 500, SAIF)), run_time=0.5)
        self.gat("agora por unidade de volume")
        self.play(FadeIn(legenda("SALDO POR UNIDADE DE VOLUME", 1124, 560)), run_time=0.5)
        self.gat("continua sendo um número")
        self.play(FadeIn(legenda("CONTINUA SENDO UM NÚMERO", 1124, 620, SAI)), run_time=0.5)
        self.ate(0.97)

        # ── B6-2 · a roda (entra enquanto o cubo sai: sem quadro vazio) ──
        self.an("B6-2")
        beta, rot, eixo = ValueTracker(0.0), ValueTracker(0.0), ValueTracker(0.0)
        est = EstadoRoda(beta, rot, eixo)
        rd = Fundo3D(self, "roda", est, op=0.0)
        sai = [m_ for m_ in self.snap()]
        self.add(rd)
        self.play(*[m_.op.animate.set_value(0.0) if isinstance(m_, Fundo3D) else FadeOut(m_) for m_ in sai], rd.op.animate.set_value(1.0), run_time=0.8)
        for m_ in sai:
            m_.clear_updaters()
        self.remove(*sai)
        wl = TC(r"\w_{\text{\C{roda}}} =", 1120, 440, 52, caneta=False)
        wn = NumBR(1.0, num_decimal_places=2, font_size=fs(52), color=VIO).next_to(wl, RIGHT, buff=0.18)
        un = TC(r"\ \text{rad/s}", 0, 440, 52, caneta=False).next_to(wn, RIGHT, buff=0.12)
        for m_ in (*wn.get_family(), *un.get_family()):
            m_._sem_contorno = True
        wl._esc = un._esc = True
        wn.add_updater(lambda m_: m_.set_value(max(0.0, float(W @ est.n()))))
        self.gat("com o eixo da rodinha alinhado")
        self.play(FadeIn(wl), FadeIn(wn), FadeIn(un), eixo.animate.set_value(1.0), run_time=0.6)
        self.gat("inclina a rodinha")
        self.play(beta.animate.set_value(PI / 4), run_time=2.4, rate_func=linear)
        self.gat("deita a rodinha de lado")
        self.play(beta.animate.set_value(PI / 2), run_time=3.0, rate_func=linear)
        self.ate(0.97)

        # ── B6-3 ──
        self.an("B6-3")
        self.play(beta.animate.set_value(0.0), eixo.animate.set_value(0.0), run_time=2.0)
        wn.clear_updaters()
        self.play(FadeOut(VGroup(wl, wn, un)), run_time=0.4)
        self.remove(wl, wn, un)
        det = TC(r"\rot \F = \begin{vmatrix} \vec\imath & \vec\jmath & \vec k \\[2pt] \partial_{\X} & \partial_{\Y} & \partial_{\Z} \\[2pt] \Pp & \Qq & \Rr \end{vmatrix}",
                 1000, 290, 46)
        ab = TC(r"= \Big(\dfrac{\partial \Rr}{\dy} - \dfrac{\partial \Qq}{\dz},\ \dfrac{\partial \Pp}{\dz} - \dfrac{\partial \Rr}{\dx},\ \dfrac{\partial \Qq}{\dx} - \dfrac{\partial \Pp}{\dy}\Big)", 1000, 470, 40)
        l3 = legenda("3ª COMPONENTE = O ROTACIONAL DO PLANO", 1004, 570, VEL)
        n1 = TC(r"\rot\F = \nabla \times \F \qquad (\nabla \wedge \F)", 1000, 680, 44)
        n2 = TC(r"\dv\F = \nabla \cdot \F", 1000, 790, 44)
        lD = legenda("DIREÇÃO: EIXO DO GIRO MAIS RÁPIDO", 510, 935, VEL, "center")          # v4 N6: embaixo da rodinha
        lT = legenda("TAMANHO: O DOBRO DESSA RAPIDEZ", 510, 985, VEL, "center")
        # a 3ª componente da forma aberta: os glifos entre a 2ª vírgula e o parêntese final (pela largura da expressão isolada)
        w3 = TC(r"\dfrac{\partial \Qq}{\dx} - \dfrac{\partial \Pp}{\dy}", 0, 0, 40, caneta=False).width
        wp = TC(r"\Big)", 0, 0, 40, caneta=False).width
        x1_ = ab.get_right()[0] - wp
        c3 = VGroup(*[g for g in glifos(ab) if x1_ - w3 - 0.02 < g.get_center()[0] < x1_ + 0.01])
        print(f"[layout] B6-3: forma aberta {ab.width * 120:.0f} px (x de 1000 a {(ab.get_right()[0] * 120 + 960):.0f}); 3ª componente = {len(c3)} glifos")
        self.gat("o rotacional é um vetor de verdade")
        self.play(rot.animate.set_value(1.0), run_time=1.2)
        self.play(FadeIn(lD), run_time=0.5)
        self.gat("o tamanho é o dobro dessa rapidez")
        self.play(FadeIn(lT), run_time=0.5)
        self.gat("se organizam num determinante simbólico")
        self.play(caneta(det))
        # final: "abrindo o determinante, a terceira componente…": a 3ª componente é escrita primeiro (logo depois do "= ("), e em "a do plano"
        # o destaque (moldura VEL e a legenda) acende enquanto as outras duas são escritas
        ini_ = [g for g in glifos(ab) if g.get_center()[0] < ab.get_left()[0] + 0.55]
        ordem_ab = lambda gs: [g for g in gs if g in ini_] + [g for g in gs if g in c3] + [g for g in gs if g not in ini_ and g not in c3]
        mold = SurroundingRectangle(c3, color=VEL, buff=0.08, stroke_width=3).set_z_index(26)
        mold._sem_contorno = True
        self.gat("abrindo o determinante")
        self.play(caneta(ab, ordem=ordem_ab, ritmo=0.7), self.em("a do plano", self.surge(mold, l3)))
        self.gat("um produto vetorial do nabla com o campo")
        self.play(caneta(n1))
        self.gat("como um produto escalar")
        self.play(caneta(n2))
        self.ate(0.97)
        fs_ = sorted(est.cache)
        err = max((abs((est.cache[b]["fase"] - est.cache[a]["fase"]) * FPS - float(W @ np.array(est.cache[b]["n"]))) for a, b in zip(fs_[:-1], fs_[1:]) if b == a + 1), default=0)
        b50 = [r for r in est.rap if abs(r[1] - math.cos(math.radians(50))) < 0.01]
        print(f"[3d] B6 roda: rapidez = W·n em {len(fs_)} quadros; maior |dfase/dt − W·n| = {err:.1e}; mínimo W·n = {min(r[1] for r in est.rap):.4f}; "
              f"W·n = cos 50° = {math.cos(math.radians(50)):.3f} no quadro {b50[0][0] if b50 else '—'} do lote")
        self.sai_fim()

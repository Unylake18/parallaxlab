"""Lote P10 (v4): T10 — como a energia se divide. PALCO: os blocos do T9 disparando pela mola uma vez (sem atrito; param nos batentes; um replay em T10-3), com as setas de
momento iguais e as barras de momento (iguais) e de energia (2 J e 1 J) crescendo juntas. CONTA: P = 0 ⇒ m1v1 = m2v2 → v1/v2 = m2/m1
→ K1/K2 = m2/m1; fração do leve 2/3 (67%); massas iguais 50%."""
from fractions import Fraction

from kit import *  # noqa: F401,F403

M1, M2, PP = 1.0, 2.0, 2.0
K1, K2 = PP ** 2 / (2 * M1), PP ** 2 / (2 * M2)
assert (K1, K2) == (2.0, 1.0) and Fraction(int(K1), int(K1 + K2)) == Fraction(2, 3)
Y_CH = 0.45                           # v6 (1.6): palco maior e mais baixo
XC = -2.9
LL, HL, LP, HP = 1.3, 1.3, 1.75, 1.69
TP = 0.25                             # o empurrão da mola (s)
ESC = 0.09                            # u por metro na tela (v6, palco vivo: os blocos levam ~8 s até os batentes)
YB = -3.1                             # base das barras
DL, DP = 1.0, 1.25                    # v7: profundidade dos blocos 3D (os mesmos do T9)
CAM_BL = {"modo": "frente", "K": 1.0, "xc": XC, "yc": Y_CH, "camx": XC, "camz": 0.0, "fov": 14, "el": 12}


def num_br(x):
    return f"{x:.1f}".replace(".", "{,}")


class LoteT10(Base):
    def construct(self):
        self.setup_base(cap="COMO A ENERGIA SE DIVIDE")
        self.an("T10-1")                          # v5: a âncora abre antes do PALCO (o disparo é marcado na fala)
        self.palco()
        self.t10_1()
        self.t10_2()
        self.t10_3_4()
        self.fim()
        self.relatorio()

    def palco(self):
        """v4: a mola dispara UMA vez (T10-1); os blocos param nos batentes das bordas do PALCO e ficam; as barras crescem com o
        empurrão e ficam. Em T10-3, um replay (chip REPLAY): os blocos somem (0,25 s), voltam com a mola comprimida (0,25 s) e disparam
        de novo; as barras não somem, só acendem."""
        sl = txt("SEM ATRITO AGORA", 16, color=DIM).move_to(P3(-1.0, Y_CH - 0.95))
        WL, WR = -6.6, 0.45                                       # faces internas dos batentes
        # v7 (3D): gelo polido com reflexo, batentes de aço e os blocos do T9 (blocos.html); setas, barras e rótulos no Manim
        self._b3 = (XC - 0.45 - LL / 2, XC + 0.45 + LP / 2, 0.0, 1.0, 0.0)

        def est(tt):
            xa, xb, u, op, sm = self._b3
            e = {"chao": "gelo", "cam": CAM_BL, "batentes": [WL - 0.1, WR + 0.1],
                 "blocos": [{"x": xa, "w": LL, "h": HL, "d": DL, "mat": "aco", "op": op}, {"x": xb, "w": LP, "h": HP, "d": DP, "mat": "grafite", "op": op}]}
            if sm > 0.01:
                e["mola"] = {"xa": xa + LL / 2, "xb": xb - LP / 2, "z": 0.55, "n": 7, "op": sm * op}
            return e
        self.f3d = Fundo3D(self, "blocos", est, op=0.0)
        self.f3d.conta.set_value(1.0)
        self.add(self.f3d)
        piso = batentes = VGroup()
        self.bm, self.be, self.sb = ValueTracker(0.0), ValueTracker(0.0), ValueTracker(0.0)   # v6 (1.2): barras e selo na fala
        self.disparos = [self.clk.get_value() + self.ate_dizer("A mola dispara os dois", mover=False)]
        self.replay = None

        def blocos(s):
            u = 0.0 if s < 0 else min(1.0, s / TP)                # fração do empurrão
            tl = max(0.0, s - TP)
            d1 = ESC * (2.0 * (0.5 * u * u * TP if u < 1 else 0.5 * TP) + 2.0 * tl)
            d2 = ESC * (1.0 * (0.5 * u * u * TP if u < 1 else 0.5 * TP) + 1.0 * tl)
            xa = max(XC - 0.45 - LL / 2 - d1, WL + LL / 2)        # param nos batentes (sem rebote)
            xb = min(XC + 0.45 + LP / 2 + d2, WR - LP / 2)
            self._bat = xa <= WL + LL / 2 + 1e-6 or xb >= WR - LP / 2 - 1e-6     # v5: algum bloco já parou no batente
            g = VGroup()                                         # v7: os corpos são do 3D; os rótulos vão embaixo de cada bloco
            self._rot = (proj3d(CAM_BL, (xa, -DL / 2, 0)), proj3d(CAM_BL, (xb, -DP / 2, 0)))
            sm = 1.0 if s < TP else max(0.0, 1 - (s - TP) / 0.3)    # a mola some logo depois do empurrão
            self._b3 = (xa, xb, u, self._op, sm)
            y = Y_CH + HP + 0.4
            for x, sx, livre, nm in ((xa, -1, xa > WL + LL / 2 + 1e-6, r"\vec p_1"), (xb, 1, xb < WR - LP / 2 - 1e-6, r"\vec p_2")):
                if u > 0 and livre:                               # o momento de cada bloco enquanto anda
                    g.add(arrow(P3(x, y), P3(x + sx * 0.95 * u, y), color=MAG, width=8, tip=0.2, z=10),
                          mtex(nm, MAG, 32).move_to(P3(x + sx * 0.5, y + 0.35)))
            return g

        def cena():
            tt = self.clk.get_value()
            R = self.replay
            self._op = 1.0
            if R is not None and tt >= R - 0.6:
                if tt < R - 0.35:                                 # os blocos parados somem
                    self._op = (R - 0.35 - tt) / 0.25
                    return escala_op(blocos(tt - self.disparos[0]), self._op)
                self._op = min(1.0, (tt - R + 0.35) / 0.25)
                g = blocos(tt - R)                                # voltam com a mola comprimida e disparam de novo
                return escala_op(g, self._op)
            return blocos(tt - self.disparos[0])

        def rotulos():
            ca, cb = self._rot
            g = VGroup(mtex(r"1\ \mathrm{kg}", WHITE_, 28).move_to(ca + P3(0, -0.38)), mtex(r"2\ \mathrm{kg}", WHITE_, 28).move_to(cb + P3(0, -0.38)))
            return escala_op(g, self._op).set_z_index(11) if self._op < 1 else g.set_z_index(11)

        def barras():
            tt = self.clk.get_value()
            u = min(1.0, max(0.0, (tt - self.disparos[0]) / TP))
            R = self.replay
            luz = 0.0 if R is None else max(0.0, 1.0 - abs(tt - R - 0.4) / 0.6)
            g = VGroup()
            xs = (-6.4, -5.6, -3.9, -3.1)
            bm, be = self.bm.get_value(), self.be.get_value()
            alt = (1.2 * u * bm, 1.2 * u * bm, 0.9 * K1 * u * u * be, 0.9 * K2 * u * u * be)
            vals = (PP * u * bm, PP * u * bm, K1 * u * u * be, K2 * u * u * be)
            for x, h, c, val in zip(xs, alt, (MAG, MAG, KC, KC), vals):
                if h > 0.01:            # v7 (2D+): cantos arredondados, degradê vertical, brilho no topo e o valor contando até o número
                    r_ = RoundedRectangle(width=0.58, height=max(h, 0.13), corner_radius=min(0.06, h / 2.2)).move_to(P3(x, YB + max(h, 0.13) / 2))
                    r_.set_stroke(interpolate_color(ManimColor(mix(c, 0.3)), ManimColor(WHITE_), luz), 1.5 + 3 * luz)
                    r_.set_fill(color=[escuro(c, 0.55), c], opacity=0.85 + 0.15 * luz).set_sheen_direction(UP)
                    g.add(r_, Line(P3(x - 0.22, YB + h - 0.035), P3(x + 0.22, YB + h - 0.035)).set_stroke(mix(c, 0.6), 3, 0.85))
                    g.add(mtex(num_br(val), mix(c, 0.25), 24).move_to(P3(x, YB + h + 0.2)))
            if u * bm > 0.01:   # v5: momentos iguais em módulo e opostos — uma setinha de sentido sobre cada barra de momento
                for x, sx in ((-6.4, -1), (-5.6, 1)):
                    g.add(escala_op(arrow(P3(x - 0.25 * sx, YB + 1.2 * u * bm + 0.62), P3(x + 0.25 * sx, YB + 1.2 * u * bm + 0.62), color=MAG,
                                          width=5, tip=0.13), min(1.0, bm * 2)))
            sb = self.sb.get_value()
            if sb > 0.01 and (R is None or tt < R - 0.6 or tt > R + 3.0):
                g.add(mtxt("ANTES DOS BATENTES", 15, color=DIM, op=sb).move_to(P3(-4.75, YB + 2.5)))    # as barras ficam congeladas
            return g
        self.cn = always_redraw(cena)
        self.cr = always_redraw(rotulos)
        self.cb = always_redraw(barras)
        base = Line(P3(-6.9, YB), P3(-2.6, YB)).set_stroke(DIM, 1.5)
        rot = VGroup(*[tex(r, c, 28).move_to(P3(x, YB - 0.28)) for x, r, c in
                       ((-6.4, r"p_1", MAG), (-5.6, r"p_2", MAG), (-3.9, r"K_1", KC), (-3.1, r"K_2", KC))])
        lm = txt("MOMENTO", 16, color=MAG).move_to(P3(-6.0, YB - 0.65))
        le = txt("ENERGIA", 16, color=KC).move_to(P3(-3.5, YB - 0.65))
        self.barras = VGroup(base, rot, lm, le)
        self.play(self.f3d.op.animate.set_value(1.0), FadeIn(sl), FadeIn(self.cn), FadeIn(self.cr), FadeIn(self.cb), FadeIn(self.barras), run_time=0.3)

    def t10_1(self):
        ri = txt("SÓ FORÇA INTERNA (A MOLA)", 18, color=INT)
        na_conta(ri, 2.25)
        e0 = VGroup(Mc((r"\vec P", MAG), "=", "0", size=50))
        na_conta(e0, 1.45)
        e0.add(txt("(ANTES DOS BATENTES)", 18, color=DIM).next_to(e0, RIGHT, buff=0.3))   # v5: os batentes são externos
        self.diz("Antes de qualquer um bater")
        self.play(self.sb.animate.set_value(1.0), run_time=0.5)             # v6 (1.3): o selo na fala
        self.diz("a única força na horizontal")
        self.play(FadeIn(ri), run_time=0.5)
        self.diz("o momento total continua zero")
        self.play(FadeIn(e0[0], shift=0.1 * UP), run_time=0.7)
        self.play(FadeIn(e0[1]), run_time=0.4)
        self.diz("os dois momentos têm o mesmo tamanho")
        self.play(self.bm.animate.set_value(1.0), run_time=1.0)            # v6 (1.2): as barras de momento crescem na fala
        e1 = Mc("m_1 v_1", "=", "m_2 v_2", size=54)
        na_conta(e1, 0.35)
        mo = txt("(MÓDULOS)", 18, color=DIM).next_to(e1, RIGHT, buff=0.25)
        self.diz("a massa do primeiro bloco")
        self.play(FadeIn(e1[0], shift=0.1 * UP), run_time=0.6)
        self.diz("é igual à massa do segundo")
        self.play(FadeIn(e1[1:], shift=0.1 * UP), FadeIn(mo), run_time=0.7)     # v6 (1.3): (MÓDULOS) junto com a igualdade
        self.diz("Repara nas barras")
        self.play(Indicate(self.barras[2], color=WHITE_, scale_factor=1.15), Circumscribe(Rectangle(width=1.6, height=1.7)
                  .move_to(P3(-6.0, YB + 0.75)), color=MAG, time_width=0.7), run_time=1.0)
        self.diz("Mas as energias")
        self.play(self.be.animate.set_value(1.0), Indicate(self.barras[3], color=WHITE_, scale_factor=1.15), run_time=1.0)
        self.ate(0.97)
        self.e0, self.e1, self.mo, self.ri = e0, e1, mo, ri

    def t10_2(self):
        self.an("T10-2")
        kp = Mc((r"K", KC), "=", (r"\frac{p^2}{2m}", MAG), size=48)
        nk = txt("DO VÍDEO ANTERIOR", 16, color=DIM)
        self.play(FadeOut(self.ri), FadeOut(self.e0), run_time=0.4)
        na_conta(kp, 2.05)
        nk.next_to(kp, RIGHT, buff=0.3)
        self.diz("a energia cinética é o momento")
        self.play(FadeIn(kp, shift=0.1 * UP), FadeIn(nk), run_time=0.8)
        inv = txt("MESMO MOMENTO: ENERGIA INVERSA À MASSA", 16, color=DIM)
        na_conta(inv, 1.2)
        self.diz("Com o mesmo momento")
        self.play(FadeIn(inv), run_time=0.6)
        self.play(self.e1.animate.move_to(P3(XC0 + self.e1.width / 2, 0.45)), self.mo.animate.next_to(P3(XC0 + self.e1.width, 0.45), RIGHT, buff=0.25),
                  run_time=0.5)
        e2 = Mc(r"\frac{v_1}{v_2}", "=", r"\frac{m_2}{m_1}", size=52)
        na_conta(e2, -0.75)
        self.diz("a razão entre as velocidades")
        self.play(TransformMatchingTex(self.e1.copy(), e2), run_time=1.2)
        self.diz("o mais leve anda mais rápido")
        self.play(Indicate(e2, color=WHITE_, scale_factor=1.05), run_time=0.8)
        e3 = Mc((r"\frac{K_1}{K_2}", KC), "=", r"\frac{m_1}{m_2}", r"\left(\frac{v_1}{v_2}\right)^2", "=", r"\frac{m_2}{m_1}", size=50)
        na_conta(e3, -2.2)
        self.diz("Na razão das energias")
        self.play(FadeIn(e3[:3], shift=0.1 * UP), run_time=0.8)
        self.diz("a velocidade entra ao quadrado")
        self.play(FadeIn(e3[3], shift=0.1 * UP), run_time=0.6)
        self.diz("sobra uma coisa bem simples")
        self.play(FadeIn(e3[4:], shift=0.1 * LEFT), run_time=0.7)
        cx = SurroundingRectangle(e3[5], buff=0.12, corner_radius=0.08).set_stroke(KC, 2.5)
        self.diz("é a massa do segundo dividida")
        self.play(Create(cx), run_time=0.5)
        self.ate(0.97)
        self.esq = VGroup(kp, nk, inv, self.e1, self.mo, e2, cx)
        self.e3 = e3

    def t10_3_4(self):
        self.an("T10-3")
        topo = Mc((r"\frac{K_1}{K_2}", KC), "=", r"\frac{m_2}{m_1}", size=50)
        na_conta(topo, 2.0)
        self.play(FadeOut(self.esq), FadeOut(self.e3[1:5]), run_time=0.5)
        self.play(ReplacementTransform(self.e3[0], topo[0]), ReplacementTransform(self.e3[5], topo[2]), FadeIn(topo[1]), run_time=0.8)
        dm = txt("MOMENTOS IGUAIS EM MÓDULO; ENERGIAS, NÃO", 20, bold=True)
        na_conta(dm, 1.05)
        self.ate(0.12)
        self.play(FadeIn(dm), Indicate(self.barras[2], color=WHITE_), run_time=0.7)
        k1 = Mc((r"v_1=2\ \mathrm{m/s}", VEL), r"\ \to\ ", (r"K_1=2\ \mathrm{J}", KC), size=38)
        k2 = Mc((r"v_2=1\ \mathrm{m/s}", VEL), r"\ \to\ ", (r"K_2=1\ \mathrm{J}", KC), size=38)
        k12 = VGroup(k1, k2)
        fr = linha("FRAÇÃO DO MAIS LEVE:", tex(r"\tfrac{2}{3}\ (67\%)", KC, 40), size=20, buff=0.2)
        ig = linha("MASSAS IGUAIS:", tex(r"50\%", KC, 40), size=20, buff=0.2)
        for m_, y in ((k1, 0.4), (k2, -0.15), (fr, -0.8), (ig, -1.4)):
            na_conta(m_, y)
        rp = chip_replay()
        self.diz("O leve sai a dois metros")
        self.replay = self.clk.get_value() + 0.6                  # um replay só, para a frente; as barras ficam e acendem
        self.play(FadeIn(k1[0], shift=0.1 * UP), FadeIn(rp), run_time=0.6)
        self.diz("fica com dois joules")
        self.play(FadeIn(k1[1:], shift=0.1 * UP), run_time=0.5)
        self.diz("o pesado sai a um metro")
        self.play(FadeIn(k2[0], shift=0.1 * UP), run_time=0.5)
        self.diz("fica com um joule")
        self.play(FadeIn(k2[1:], shift=0.1 * UP), run_time=0.5)
        while self.clk.get_value() < self.replay + 3.4:
            self.wait(1 / FPS)
        self.play(FadeOut(rp), run_time=0.3)
        self.diz("Dois terços")
        self.play(FadeIn(fr, shift=0.1 * UP), run_time=0.7)
        self.diz("Com massas iguais")
        self.play(FadeIn(ig, shift=0.1 * UP), run_time=0.6)
        # v4: no corpo BODY (20, o de "MOMENTO SE DIVIDE IGUAL"), sem encolher; quebra no menor número de linhas que cabe na CONTA
        # (em duas linhas, como pedia o handoff, não cabe)
        quebras = (("QUANTO MAIOR A DIFERENÇA DE MASSAS, MAIOR A FRAÇÃO", "DA ENERGIA CINÉTICA QUE FICA COM O MAIS LEVE"),
                   ("QUANTO MAIOR A DIFERENÇA DE MASSAS,", "MAIOR A FRAÇÃO DA ENERGIA CINÉTICA", "QUE FICA COM O MAIS LEVE"),
                   ("QUANTO MAIOR A DIFERENÇA", "DE MASSAS, MAIOR A FRAÇÃO", "DA ENERGIA CINÉTICA QUE", "FICA COM O MAIS LEVE"))
        for q in quebras:
            ls = [txt(l, 20, color=WHITE_ if i == 0 else KC) for i, l in enumerate(q)]
            if max(m_.width for m_ in ls) <= 6.6 - XC0:
                break
        self.n_linhas_t10 = len(ls)
        y0 = -1.95
        for i, m_ in enumerate(ls):
            na_conta(m_, y0 - 0.36 * i)
        f3 = txt("GUARDA PARA O CAÇADOR", 16, color=DIM)
        na_conta(f3, y0 - 0.36 * len(ls) - 0.05)
        f1, f2 = ls[0], VGroup(*ls[1:])
        self.diz("E quanto maior a diferença")
        self.play(FadeIn(VGroup(f1, f2)), run_time=0.8)
        self.diz("Guarda isso")
        self.play(FadeIn(f3), run_time=0.5)
        self.ate(0.97)
        # T10-4 — DICA
        self.an("T10-4")
        d = dica("MESMO MOMENTO: QUANTO MAIS LEVE,", "MAIOR A FRAÇÃO DA ENERGIA")
        self.play(FadeOut(VGroup(f1, f2, f3)), run_time=0.25)                 # v7 (1.1): o texto sai antes de a DICA entrar
        self.play(FadeIn(d, shift=0.15 * UP), run_time=0.35)
        self.sobra(0.5)
        self.cn.clear_updaters(); self.cb.clear_updaters(); self.cr.clear_updaters()
        self.clear(rt=0.5)

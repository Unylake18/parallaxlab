"""yt_0039 · E3 · o oitavo de bola (alvos 06 e 07). E3-1: palco xy (origem (300, 900), a = 520 px); o enunciado; a leitura dos limites (marcas,
tira que varre com a saída deixando o rastro do quarto de círculo; y² = a² − x² ⇒ x² + y² = a² por mapa; QUARTO DE DISCO); o integrando
(z = √… ⇒ x² + y² + z² = a²); a cena 3D `octante` entra POR CIMA do palco no mesmo quadro (vista de cima ortográfica = o quarto de disco 2D),
a câmera sobe para a vista do alvo 06 (2,5 s) e a casca cresce do chão (2 s); UM OITAVO DE BOLA. E3-2: pouso ao contrário (a casca baixa, vista
de cima ortográfica com a origem em (220, 900) e a = 560 px) e o palco 2D do alvo 07 herda o quarto de disco; C3 etapa A (polares, w, limites,
O MENOS INVERTE OS LIMITES) e etapa B (a³/3, πa³/6, conferência pela bola ÷ 8 ✓)."""
from k39 import *
from k39 import _troca_col  # noqa: F401

SC3 = 2.4
V1 = Vw(300, 900, 520)
V2 = Vw(220, 900, 560)
LX = (SC3 + .55) / SC3              # a ponta das setas dos eixos (em unidades de a), igual à do 3D


class PE3(B39x):
    ANTES = "3 · O OITAVO DE BOLA"
    COLX = 1060

    def corpo(self):
        v = V1
        a = 1.0
        # ═══ E3-1 · ler a região nos limites ═══
        self.an("E3-1")
        self.gat("terceiro problema")
        g = papel_tela(v)
        self.grade = g
        sx = seta_px(v.px(0, 0), v.px(LX, 0), E1, 3, 16, z=6)
        sy = seta_px(v.px(0, 0), v.px(0, LX), E2, 3, 16, z=6)
        Lx = TC(r"\X", v.px(LX, 0)[0] + 22, v.px(LX, 0)[1], 32, "c")
        Ly = TC(r"\Y", v.px(0, LX)[0], v.px(0, LX)[1] - 26, 32, "c")
        self.play(FadeIn(g), GrowFromPoint(sx, v.P(0, 0)), GrowFromPoint(sy, v.P(0, 0)), run_time=0.6)
        self.pena(Lx, Ly, lag=0.05)
        self.colY = 230
        En = linha(self, [("o", r"\int_0^{a}"), ("lb", r"\left["), ("i", r"\int_0^{\sqrt{a^2-x^2}}"), ("f", r"\sqrt{a^2-x^2-y^2}"), ("d", r"\,dy"),
                          ("rb", r"\right]"), ("dx", r"dx")], 36)
        # v2 §5 (9:26): cada limite lido no enunciado nasce no desenho no mesmo gatilho
        self.gat("a integral de zero a a")
        t1 = tk(v, "x", 1, "a")
        t0 = tk(v, "x", 0.0001, "0")
        self.play(Create(t1[0]), run_time=0.3)
        self.pena(t0[1], t1[1], lag=0.1)
        self.leitura(G(En, ix_(En, "o")), rt=0.8)
        self.gat("da integral de zero a raiz")
        arq = lin_px([v.px(math.cos(t), math.sin(t)) for t in np.linspace(0, math.pi / 2, 61)], CORAL, 2, dash=(8, 8), alpha=.6, z=5)
        self.play(Create(arq), run_time=0.8)
        self.leitura(G(En, ix_(En, "i")), rt=0.8)
        self.gat("pausa e tenta")
        pz = poe_pausa(self, 1060, 980)
        self.gat("x vai de zero a a")
        self.leitura(t0[1], t1[1], rt=0.8)
        L1 = linha(self, [("x", r"0\le x\le a")], 36, gap=30, voos=[(t0[1], [0]), (t1[1], [len(MathTex("0\\le x\\le", tex_template=TEX31)[0])])])
        origem(self, "0 e a de 0 ≤ x ≤ a", "marcas do eixo x")
        self.gat("a fatia entra em y")
        xt = ValueTracker(.45)
        tira = always_redraw(lambda: VGroup(tiraV(v, xt.get_value(), 0, math.sqrt(max(0, 1 - xt.get_value() ** 2)), h=.025, cor=E1),
                                            *pontos_es(v, (xt.get_value(), 0), (xt.get_value(), math.sqrt(max(0, 1 - xt.get_value() ** 2))))))
        self.add(xt)
        self.play(FadeIn(tira), run_time=0.4)
        L1 = cad(self, L1, [("q", r"\qquad"), ("y", r"\Az{0}\le y\le")], [], n=12, nota="entrada y = 0")
        self.gat("e sai na raiz")
        L1 = cad(self, L1, [("s", r"\Co{\sqrt{a^2-x^2}}")], [], n=12, nota="saída √(a² − x²)",
                 voos=[])
        rastro = VMobject()
        pts_r = []

        def upd_r(m):
            X = xt.get_value()
            pts_r.append(v.P(X, math.sqrt(max(0, 1 - X * X))))
            if len(pts_r) > 1:
                m.set_points_as_corners(pts_r)
            m.set_stroke(CORAL, W(3)).set_fill(opacity=0)
        rastro.add_updater(upd_r)
        self.add(rastro)
        self.play(xt.animate.set_value(0.0), run_time=1.0)
        pts_r.clear()
        self.play(xt.animate.set_value(1.0), run_time=2.6, rate_func=linear)
        rastro.clear_updaters()
        self.gat("elevando ao quadrado")
        L2 = linha(self, [("y2", r"y^2"), ("e", "="), ("a2", r"a^2"), ("m", "-"), ("x2", r"x^2")], 36, gap=22)
        self.gat("Elevando ao quadrado")
        L2 = cad(self, L2, [("im", r"\enspace\Rightarrow\enspace"), ("x2", r"x^2"), ("p", "+"), ("y2", r"y^2"), ("e", "="), ("a2", r"a^2")],
                 [("x2", "x2"), ("m", "p"), ("y2", "y2"), ("e", "e"), ("a2", "a2")], n=12, nota="C3: o x² atravessa a igualdade")
        degrau(self, "C3", "y² = a² − x² ⇒ x² + y² = a²")
        self.gat("é o círculo de raio")
        self.play(FadeOut(tira), FadeOut(arq), run_time=0.3)
        self.remove(tira, xt, arq)
        arc = lin_px([v.px(math.cos(t), math.sin(t)) for t in np.linspace(0, math.pi / 2, 91)], CORAL, 3, z=6)
        self.play(ReplacementTransform(rastro, arc), run_time=0.5)
        self.gat("a região é um quarto")
        qd = poly_px([v.px(0, 0)] + [v.px(math.cos(t), math.sin(t)) for t in np.linspace(0, math.pi / 2, 91)], FUNDO_R, 1.0, z=1)
        lq = palavra(self, "QUARTO DE DISCO", GEO, 28, gap=18)
        self.play(FadeIn(qd), run_time=0.6)
        self.gat("e o integrando")
        L3 = linha(self, [("z", r"z"), ("e", "="), ("f", r"\sqrt{a^2-x^2-y^2}")], 34, gap=26, voos=[(G(En, ix_(En, "f")), "f")])
        self.gat("é a esfera de raio")
        L3 = cad(self, L3, [("im", r"\enspace\Rightarrow\enspace"), ("r", r"x^2+y^2+z^2=a^2")], [("z", "r"), ("^f", "r")], n=12, nota="C3: z² vai para o lado de x² + y²")
        degrau(self, "C3", "z = √(a² − x² − y²) ⇒ x² + y² + z² = a²")
        # 3D por cima do palco, no mesmo quadro (vista de cima ortográfica = o quarto de disco 2D)
        k1 = 520 / SC3
        self.play(arc.animate.set_stroke(GEO), run_time=0.4)
        pal = Palco37(self, "octante", cam_oct(), casca=0.0, zl=0.0)
        pal.fundo.set_z_index(-5)
        pal.sobe(k1, 300, 900)
        pal.tr["s"].set_value(1.0)
        self.add(pal.fundo)
        sai2d = [qd, arc, sx, sy, t1[0], t0[1], t1[1]]
        self.remove(*[m for m in sai2d if m in self.mobjects])
        qx, qy = pal.pt("ex"), pal.pt("ey")
        lx3 = pal.prende(TC(r"\X", 0, 0, 32, "c"), "ex", pxof(Lx.get_center())[0] - qx[0], pxof(Lx.get_center())[1] - qx[1])
        ly3 = pal.prende(TC(r"\Y", 0, 0, 32, "c"), "ey", pxof(Ly.get_center())[0] - qy[0], pxof(Ly.get_center())[1] - qy[1])
        pronto(lx3, ly3)
        self.remove(Lx, Ly)
        self.add(lx3, ly3)
        print(f"[pouso3d] {self.lote} E3-1 entrada quadro {self.nq} (2D → 3D, vista de cima)")
        self.play(FadeOut(self.grade), *pal.anim(2.5, s=0.0), *pal.anim(2.5, zl=1.0), run_time=2.5)
        self.grade = None
        self.play(*pal.anim(2.0, casca=1.0), run_time=2.0)
        lz3 = pal.prende(TC("z", 0, 0, 32, "c"), "ez", 24, 10)
        self.pena(lz3)
        cs = pal.pt("casca")
        # C5: o rótulo nasce FORA da peça (à esquerda do arco, ≥ 14 px de qualquer traço), com fio-guia fino até o ponto que nomeia, escrito no lugar
        le = pal.prende(TP(r"x^2+y^2+z^2=a^2", 0, 0, 30, "l"), "casca", 380 - cs[0], 330 - cs[1], ancora="r")
        gf = lin_px([(392, 330), (cs[0] - 8, cs[1] - 4)], GEO, 1.3, z=6)
        gf.set_stroke(opacity=.8)
        self.play(Create(gf), run_time=0.3)
        self.pena(le)
        self.gat("um oitavo de bola")
        uo = T("UM OITAVO DE BOLA", 300, 1010, 34, "left", MEN)
        self.pena(uo)
        self.marca("06_E3-1")
        self.wait(1.5)
        self._fecha(antes=0.4)

        # ═══ E3-2 · polares e o oitavo de bola ═══
        self.an("E3-2")
        v = V2
        k2 = 560 / SC3
        self.play(FadeOut(uo), FadeOut(le), FadeOut(lz3), FadeOut(gf), run_time=0.4)
        self.remove(uo, le, lz3, gf)
        pal.sobe(k2, 220, 900)
        self.play(*pal.anim(2.0, casca=0.0), *pal.anim(2.0, zl=0.0), run_time=2.0)
        self.play(*pal.anim(2.5, s=1.0), run_time=2.5)
        print(f"[pouso3d] {self.lote} E3-2 pouso quadro {self.nq} (3D → 2D, vista de cima)")
        qd2 = poly_px([v.px(0, 0)] + [v.px(math.cos(t), math.sin(t)) for t in np.linspace(0, math.pi / 2, 91)], FUNDO_R, 1.0, z=1)
        arc2 = lin_px([v.px(math.cos(t), math.sin(t)) for t in np.linspace(0, math.pi / 2, 91)], CORAL, 3, z=6)
        sx2 = seta_px(v.px(0, 0), v.px(LX, 0), E1, 3, 16, z=6)
        sy2 = seta_px(v.px(0, 0), v.px(0, LX), E2, 3, 16, z=6)
        qx, qy = pal.pt("ex"), pal.pt("ey")
        lx2 = TC(r"\X", *pxof(lx3.get_center()), 32, "c")
        ly2 = TC(r"\Y", *pxof(ly3.get_center()), 32, "c")
        pronto(qd2, arc2, sx2, sy2, lx2, ly2)
        troca_para_2d(self, pal, [qd2, arc2, sx2, sy2, lx2, ly2])
        for m in (lx3, ly3):
            m.clear_updaters()
        self.remove(lx3, ly3)
        g2 = papel_tela(v)
        tka, tkb = tk(v, "x", 1, "a"), tk(v, "y", 1, "a")
        self.play(FadeIn(g2), Create(tka[0]), Create(tkb[0]), run_time=0.5)
        self.grade = g2
        self.pena(tka[1], tkb[1], lag=0.1)
        limpa_col(self)
        self.colY = 240
        self.gat("x ao quadrado mais y ao quadrado é r ao quadrado")
        A1 = linha(self, [("l", r"x^2+y^2"), ("e", "="), ("r", r"\R^2")], 36)
        self.gat("e o integrando fica")
        A1b = linha(self, [("a", r"a^2-x^2-y^2"), ("e", "="), ("b", r"a^2-(x^2+y^2)"), ("e2", "="), ("r", r"a^2-\R^2")], 30, gap=16)
        th = ValueTracker(0.0)
        raio = always_redraw(lambda: VGroup(lin_px([v.px(0, 0), v.px(math.cos(th.get_value()), math.sin(th.get_value()))], LAR, 4, z=7),
                                            ponto_px(*v.px(0, 0), AZC, 8, z=9), ponto_px(*v.px(math.cos(th.get_value()), math.sin(th.get_value())), CORAL, 8, z=9)))
        self.add(th)
        self.play(FadeIn(raio), run_time=0.4)
        self.gat("r de zero a a")
        A2 = linha(self, [("r", r"0\le\R\le a"), ("q", r"\qquad"), ("t", r"0\le\th\le\dfrac{\pi}{2}")], 36, gap=22, escreve=False)
        self.pena(parte(A2, ix_(A2, "r"), "r"))
        self.gat("e téta de zero a pi")
        aT = always_redraw(lambda: lin_px([v.px(.125 * math.cos(t), .125 * math.sin(t)) for t in np.linspace(0, max(1e-3, th.get_value()), 30)], VAG, 3, z=7))
        self.add(aT)
        self.play(th.animate.set_value(math.pi / 2), run_time=2.0)
        self.pena(parte(A2, ix_(A2, "q", "t"), "θ"))
        self.play(th.animate.set_value(.62), run_time=1.0)
        raio.clear_updaters()
        aT.clear_updaters()
        lr = TC(r"\R", *v.px(.5 * math.cos(.62) - .05, .5 * math.sin(.62) + .07), 30, "c")
        lt = TC(r"\th", *v.px(.2, .06), 30, "c")
        self.pena(lr, lt, lag=0.1)
        self.gat("e não esquece o fator")
        A3 = linha(self, [("i1", r"\int_0^{\pi/2}"), ("i2", r"\!\!\int_0^a"), ("f", r"\sqrt{a^2-\R^2}"), ("j", r"\;\Rj"), ("d", r"\,\dr\,\dth")], 36, gap=24, escreve=False)
        hi1 = lims(A3, "i1")[1]
        escreve_seq(self, A3, [(G(A2, ix_(A2, "t")[-4:]), hi1)], so=[i for i in range(len(A3[0])) if i not in ix_(A3, "j")])
        self.gat("vezes r o jacobiano")
        escreve_seq(self, A3, [(lr, ix_(A3, "j"))], so=ix_(A3, "j"))
        self.gat("o jacobiano das polares")
        jx0, jx1 = pxof(G(A3, ix_(A3, "j")).get_left())[0], pxof(G(A3, ix_(A3, "j")).get_right())[0]
        yb_ = pxof(A3.get_bottom())[1] + 20
        chj = chave_h(jx0 - 4, jx1 + 4, yb_, LIMA, 2, True)
        lj = T("JACOBIANO", (jx0 + jx1) / 2, yb_ + 44, 26, "center", LIMA, bold=False)
        self.play(Create(chj), run_time=0.4)
        self.pena(lj)
        self.colms += [chj, lj]
        self.colY = pxof(lj.get_bottom())[1]
        sobe_col(self, [A1b], y0=250)
        self.gat("w igual a a ao quadrado")
        W1 = linha(self, [("w", r"\w=a^2-\R^2,"), ("q", r"\quad"), ("dw", r"\dw=-2\R\,\dr")], 34, gap=22, voos=[(G(A3, ix_(A3, "f")[-5:]), [2, 3, 4, 5, 6])])
        self.gat("então r d r é menos")
        W1 = cad(self, W1, [("im", r"\enspace\Rightarrow\enspace"), ("r", r"\R\,\dr=-\dfrac{\dw}{2}")], [("^dw", "r")], n=13, nota="C3: r dr = −dw/2")
        degrau(self, "C3", "w = a² − r², dw = −2r dr ⇒ r dr = −dw/2")
        self.gat("os limites mudam")
        # v2 §5: a faixa de w em lilás no raio (w = a² no centro, w = 0 na borda)
        pw = v.px(math.cos(.62), math.sin(.62))
        wl = lin_px([v.px(0, 0), pw], LIL, 7, alpha=.75, z=8)
        lw0 = TP(r"\w=a^2", *v.px(0, 0), 26, "c")
        lw0.move_to(PX(v.px(0, 0)[0] + 70, v.px(0, 0)[1] + 40))
        lw1 = TP(r"\w=0", pw[0] + 64, pw[1] - 26, 26, "c")
        self.play(Create(wl), run_time=0.6)
        self.pena(lw0, lw1, lag=0.1)
        W2 = linha(self, [("a", r"\R=0\to\w=a^2"), ("q", r"\qquad"), ("b", r"\R=a\to\w=0")], 34, gap=20)
        degrau(self, "C3", "r = 0 → w = a²; r = a → w = 0")
        self.gat("o sinal de menos inverte")
        W3 = linha(self, [("i", r"\int_{a^2}^{0}"), ("f", r"\sqrt{\w}"), ("p", r"\left(-\dfrac{\dw}{2}\right)")], 34, gap=22, escreve=False)
        loW, hiW = lims(W3, "i")
        escreve_seq(self, W3, [(G(W2, ix_(W2, "a")[-3:]), loW), (G(W2, ix_(W2, "b")[-1:]), hiW)])
        W3 = cad(self, W3, [("e", "="), ("h", r"\dfrac12"), ("i", r"\int_0^{a^2}"), ("w", r"\w^{1/2}"), ("d", r"\,\dw")],
                 [("^p", "h"), ("^p", "d"), ("^i", "i"), ("^f", "w")], n=13, nota="C3: o menos inverte os limites")
        sl = selo_t("O MENOS INVERTE OS LIMITES", 1060, pxof(W3.get_bottom())[1] + 44, AL, 26)
        poe_selo_t(self, sl)
        self.colms += list(sl)
        degrau(self, "C3", "∫_{a²}^0 √w (−dw/2) = (1/2)∫₀^{a²} w^{1/2} dw")
        self.gat("a primitiva é dois terços")
        chI = chip(self, r"\int_0^{\pi/2}\!\!\int_0^a\sqrt{a^2-\R^2}\;\Rj\,\dr\,\dth", 1060, 180, de=A3.copy(), size=28)
        limpa_col(self, keep=[W3])
        self.play(W3.animate.shift(PX(1060, 280) - PX(pxof(W3.get_left())[0], pxof(W3.get_center())[1])), run_time=0.6)
        self.colms = [W3]
        self.colY = pxof(W3.get_bottom())[1]
        B1 = linha(self, [("h", r"\dfrac12"), ("c", r"\left[\dfrac23\,\w^{3/2}\right]_0^{a^2}")], 36, gap=26, voos=[(G(W3, ix_(W3, "h")), "h")])
        degrau(self, "C3", "(1/2)[(2/3) w^{3/2}]₀^{a²}")
        self.gat("a ao quadrado elevado a três")
        B1 = cad(self, B1, [("e", "="), ("h", r"\dfrac12"), ("c", r"\cdot"), ("t", r"\dfrac23"), ("p", r"\left((a^2)^{3/2}-0\right)")], [("^h", "h"), ("^c", "t"), ("^c", "p")],
                 n=14, nota="C3: G(a²) − G(0)")
        self.leitura(G(B1, ix_(B1, "p")[1:8]), rt=0.6)
        self.gat("a ao cubo sobre três")
        B1 = cad(self, B1, [("e", "="), ("h", r"\dfrac12"), ("c", r"\cdot"), ("t", r"\dfrac23"), ("a3", r"a^3")], [("^h", "h"), ("^t", "t")], n=14, nota="D13: (a²)^{3/2} = a³")
        B1 = cad(self, B1, [("e", "="), ("r", r"\dfrac{2a^3}{6}")], [("^h", "r"), ("^t", "r"), ("^a3", "r")], n=14, nota="D13: 1/2 · 2/3 = 2/6")
        B1 = cad(self, B1, [("e", "="), ("r", r"\dfrac{a^3}{3}")], [("^r", "r")], n=14, nota="= a³/3")
        degrau(self, "C3", "= (1/2)(2/3)((a²)^{3/2} − 0) = a³/3")
        self.gat("A de fora só multiplica")
        B2 = linha(self, [("f", r"\dfrac{a^3}{3}"), ("c", r"\Big[\th\Big]_0^{\pi/2}")], 36, gap=26, voos=[(G(B1, ix_(B1, "r")), "f")])
        B2 = cad(self, B2, [("e", "="), ("f", r"\dfrac{a^3}{3}"), ("p", r"\left(\dfrac{\pi}{2}-0\right)")], [("^f", "f"), ("^c", "p")], n=14, nota="(π/2 − 0)")
        self.gat("pi a ao cubo sobre seis")
        B2 = cad(self, B2, [("e", "="), ("r", r"\dfrac{\pi a^3}{6}")], [("^f", "r"), ("^p", "r")], n=14, nota="= πa³/6")
        degrau(self, "C3", "(a³/3)[θ]₀^{π/2} = (a³/3)(π/2 − 0) = πa³/6")
        self.gat("confere com a bola inteira")
        ic = icone_oitavo(1790, 880)
        li = TC(r"\dfrac{4\pi a^3}{3}", 1790, 975, 30, "c")
        self.play(Create(ic), run_time=0.6)
        self.pena(li)
        B3 = linha(self, [("b", r"\dfrac{4\pi a^3}{3}"), ("d", r"\div 8")], 36, gap=26, voos=[(li, "b")])
        self.gat("dividido por oito")
        B3 = cad(self, B3, [("e", "="), ("r", r"\dfrac{4\pi a^3}{24}")], [("^b", "r"), ("^d", "r")], n=14, nota="4πa³/24")
        B3 = cad(self, B3, [("e", "="), ("r", r"\dfrac{\pi a^3}{6}")], [("^r", "r")], n=14, nota="= πa³/6")
        degrau(self, "C3", "(4πa³/3) ÷ 8 = 4πa³/24 = πa³/6")
        self.gat("um oitavo certinho")
        ok_ao_lado(self, B3)
        uo2 = T("UM OITAVO DA BOLA", 1060, pxof(B3.get_bottom())[1] + 56, 30, "left", MEN)
        self.pena(uo2)
        self.marca("07_E3-2")
        self.wait(1.0)
        self.sai_fim()

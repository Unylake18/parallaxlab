"""yt_0037 · B5 · um disco fora do centro — v2 (alvo 07; E22–E25). O disco de centro (1, 0) se desenha no 1º gatilho; coluna em 2 páginas (G2):
p1 = o quadrado se completa (GM9), r ≤ 2 cos θ (GM10), cos θ ≥ 0; p2 = o chip do domínio e a área (GM11, CONTA INTEIRA até π) com CONFERE π · 1² ✓.
A reta-sonda fica viva o bloco todo: varre de −π/2 a π/2, para em π/3 (θ = π/3 ⇒ r = 1, placa por fora da circunferência), mostra o limite que
depende de θ e, em "confere com a área", pinta o disco; nos degraus da área ela varre de novo (G7). Rótulos de ±π/2 à direita do eixo y (E23)."""
from v2kit import *

V5 = Vw(150, 650, 285)
X5 = 1000
FD = mixh(BG_, GEO, .14)


def ordx(m, key):
    return sorted(sel(m, key), key=lambda i: m[0][i].get_center()[0])


def sup_sub(m, key):
    ix_ = sel(m, key)
    base = max(ix_, key=lambda i: m[0][i].height)
    resto = [i for i in ix_ if i != base]
    cy = m[0][base].get_center()[1]
    up = sorted([i for i in resto if m[0][i].get_center()[1] >= cy], key=lambda i: m[0][i].get_center()[0])
    lo = sorted([i for i in resto if m[0][i].get_center()[1] < cy], key=lambda i: m[0][i].get_center()[0])
    return base, up, lo


def saida(t):
    r = 2 * math.cos(t)
    return (r * math.cos(t), r * math.sin(t))


class PB5(B37):
    ANTES = "O DISCO DO COMEÇO"
    SUB = "A CASCA DE RAIO r"
    CARTAO = True

    def varre(self, th, alvo, rt):
        self.play(th.animate(rate_func=smooth).set_value(alvo), run_time=rt)

    def corpo(self):
        v = V5
        self.an("B5")
        g = papel_v(v, (-.1, 2.25, -1.25, 1.25))
        self.grade = g
        sx, sy, lx, ly = eixos_xy(v, -.1, 2.3, -1.25, 1.28, size=40)
        df = disco(v, 1, FD, 1.0, c=(1, 0), z=1)
        dc = circulo(v, 1, CORAL, 4, c=(1, 0), z=5)
        # E22/E25: o palco começa a se desenhar no 1º quadro do bloco; o disco entra no 1º gatilho, antes da coluna
        self.play(FadeIn(g), GrowFromPoint(sx, v.P(0, 0)), GrowFromPoint(sy, v.P(0, 0)), run_time=0.6)
        self.secao("O DISCO QUE PASSA PELA ORIGEM")
        self.subt("A RETA-SONDA SAI DO POLO")
        self.pena(lx, ly, lag=0.05)
        self.gat("não está centrada")
        self.play(FadeIn(df), Create(dc), run_time=1.0)
        # ── página 1 · C5-0 e GM9 ──
        self.gat("menor ou igual a dois xis")
        A0 = col(L([("x2", r"\X^2"), ("p", "+"), ("y2", r"\Y^2"), ("le", r"\le"), ("dx", r"2\X")], X5, 220, 44))
        self.pena(A0)
        self.gat("completa o quadrado")
        A2 = col(L([("x2", r"\X^2"), ("m", "-"), ("dx", r"2\X"), ("p1", "+1"), ("p", "+"), ("y2", r"\Y^2"), ("le", r"\le"), ("um", "1")], X5, 220, 44))
        A2.shift(UP * (A0[0][sel(A0, "le")[0]].get_center()[1] - A2[0][sel(A2, "le")[0]].get_center()[1]))
        gmap(self, 9, A0, A2, [("x2", "x2"), ("dx", "dx"), ("p", "p"), ("y2", "y2"), ("le", "le")], rt=1.4, copia=False,
             nota="a) o 2x atravessa e troca de sinal; +1 dos dois lados")
        degrau(self, "B5 disco", "x² + y² ≤ 2x ⇔ x² − 2x + 1 + y² ≤ 1")
        self.gat("xis menos um ao")
        A3 = col(L([("iff", r"\iff"), ("sq", r"(\X-1)^2"), ("p", "+"), ("y2", r"\Y^2"), ("le", r"\le"), ("um", "1")], X5 + 40, 0, 44))
        abaixo(A2, A3, X5 + 40, 30)
        x2, sq, p1 = ordx(A2, "x2"), ordx(A3, "sq"), ordx(A2, "p1")
        gmap(self, 9, A2, A3, [(x2[0:1], sq[1:2]), (x2[1:2], sq[5:6]), ("m", sq[2:3]), (p1[1:2], sq[3:4]), ("p", "p"), ("y2", "y2"), ("le", "le"),
                               ("um", "um")], rt=1.4, nota="b) o quadrado se completa")
        degrau(self, "B5 disco", "⇔ (x − 1)² + y² ≤ 1")
        self.gat("é o disco de centro")
        cc = ponto_px(*v.px(1, 0), GEO, 7, z=6)
        r1 = lin_px([v.px(1, 0), v.px(1 + math.cos(-.9), math.sin(-.9))], GEO, 3, dash=(8, 6), z=6)
        l1 = TC("1", *v.px(1 + .5 * math.cos(-.9) + .17 * .78, .5 * math.sin(-.9) + .17 * .62), 40, "c")      # ao lado do raio, fora da linha
        self.play(FadeIn(cc, scale=.5), Create(r1), run_time=0.6)
        self.pena(l1)
        self.gat("que passa pela origem")
        o = ponto_px(*v.px(0, 0), AZC, 9, z=9)
        self.play(FadeIn(o, scale=.5), Flash(v.P(0, 0), color=AZC, line_length=.12, num_lines=10, flash_radius=.16), run_time=0.6)
        # GM10: em polares
        self.gat("em polares o lado")
        sai = saindo([r1, l1])
        self.play(FadeOut(r1), FadeOut(l1), run_time=0.3)
        self.remove(r1, l1)
        B0 = col(L([("r2", r"\R^2"), ("le", r"\le"), ("rhs", r"2\R\cos\T")], X5, 0, 44))
        abaixo(A3, B0, X5, 34)
        self.pena(parte(B0, sel(B0, ["r2"]), "r²"))
        self.gat("o dois xis vira")
        self.pena(parte(B0, sel(B0, ["le", "rhs"]), "≤ 2r cos θ"))
        self.gat("divide por erre")
        rh = ordx(B0, "rhs")
        acende(self, (B0[0][sel(B0, "r2")[0]:sel(B0, "r2")[0] + 1], AL), (B0[0][rh[1]:rh[1] + 1], AL), rt=0.4)
        B1 = col(L([("im", r"\ \Rightarrow\ "), ("r", r"\R"), ("le", r"\le"), ("rhs", r"\Co{2\cos\T}"), ("cond", r"\quad(\R>0)")], X5, 0, 44))
        ao_lado(B0, B1, 14, ia=sel(B0, "le")[0], ib=sel(B1, "le")[0])
        rb = ordx(B1, "rhs")
        gmap(self, 10, B0, B1, [(sel(B0, "r2")[0:1], "r"), ("le", "le"), (rh[0:1], rb[0:1]), (rh[2:6], rb[1:5])], rt=1.3,
             nota="um r de cada lado sai; (r > 0)")
        degrau(self, "B5 polares", "r² ≤ 2r cos θ ⇒ r ≤ 2 cos θ (r > 0)")
        lr2 = TP(r"\Co{\R=2\cos\T}", 684, 425, 40, "l")          # fora da circunferência, à direita (folga ≥ 10 px)
        self.pena(lr2)
        self.gat("o cosseno tem que")
        C3 = col(L([("c", r"\cos\T\ge 0"), ("im", r"\ \ \Rightarrow\ \ "), ("t", r"-\pi/2\le\T\le\pi/2")], X5, 0, 44))
        abaixo(B0, C3, X5, 34)
        self.pena(C3)
        lt1 = TC(r"\T=\pi/2", 168, v.px(0, 1.13)[1], 40, "l")      # E23: à direita do eixo y, na altura das pontas
        lt2 = TC(r"\T=-\pi/2", 168, v.px(0, -1.13)[1], 40, "l")
        hp = VGroup(lin_px([v.px(0, -1.2), v.px(0, 1.2)], TH, 5, alpha=.9, z=6))
        self.play(Create(hp), run_time=0.5)
        self.pena(lt1, lt2, lag=0.1)
        self.play(FadeOut(hp), run_time=0.4)
        self.remove(hp)
        # a reta-sonda (fica viva até o fim do bloco)
        self.gat("a reta-sonda sai da")
        th = ValueTracker(-math.pi / 2 + .03)
        son = always_redraw(lambda: VGroup(lin_px([v.px(0, 0), v.px(*saida(th.get_value()))], RR, 6, z=7),
                                           ponto_px(*v.px(*saida(th.get_value())), CORAL, 9, z=9)))
        for x in son.get_family():
            x._sem_foco = True
        self.add(th)
        self.play(FadeIn(son), run_time=0.3)
        self.varre(th, math.pi / 2 - .03, 2.6)
        self.gat("entra em erre igual")
        en = leg("ENTRA NA ORIGEM", 168, 700, AZC, "left", 30)
        self.pena(en)
        self.gat("com téta igual a pi")
        aT = always_redraw(lambda: arco(v, .3, 0, th.get_value(), TH, 3, z=7))
        self.add(aT)
        self.varre(th, math.pi / 3, 1.4)
        ltt = TC(r"\T", *v.px(.42 * math.cos(.5), .42 * math.sin(.5)), 40, "c")
        self.pena(ltt)
        self.gat("sai em erre igual a um")
        pq = TP(r"\T=\pi/3\ \Rightarrow\ \R=1", 0, 0, 40, "l")    # E23: por fora da circunferência, com guia até o ponto coral
        pq.shift(PX(345, 318) - np.array([pq.get_left()[0], pq.get_center()[1], 0]))
        gq = guia_px((360, 345), (v.px(*saida(math.pi / 3))[0] + 6, v.px(*saida(math.pi / 3))[1] - 8), CORAL, pq, 2, 10)
        for x in gq.get_family():
            x._guia_de = pq.f
        voa(self, son[1].copy(), pq, rt=0.9)
        self.play(Create(gq), run_time=0.3)
        origem(self, "θ = π/3 ⇒ r = 1", "ponto de saída da sonda (voo)")
        self.gat("não vira retângulo")
        gc = leg("A GRADE CERTA SIMPLIFICA A REGIÃO", X5, pxof(C3.get_bottom())[1] + 70, MEN, "left", 30)
        self.pena(gc, passo=0.025)
        self.gat("o limite de dentro depende")
        aT.clear_updaters()
        sai = saindo([pq, gq, en, ltt, aT])                 # o estado π/3 cumpriu; a sonda vai varrer por ali
        self.play(*[FadeOut(m) for m in sai], run_time=0.3)
        self.remove(pq, gq, en, ltt, aT)
        self.varre(th, -math.pi / 3, 1.4)
        self.varre(th, math.pi / 4, 1.2)
        # ── página 2 · a área (G2): o chip do domínio no topo ──
        self.gat("montar os limites")                       # a página 2 abre com o chip dos limites (o assunto da frase)
        KD1 = L([("r", r"\R"), ("le", r"\le"), ("rhs", r"\Co{2\cos\T}")], X5 + 14, 222, 40)
        KD2 = L([("t", r"-\pi/2\le\T\le\pi/2")], 0, 222, 40)
        KD2.shift(RIGHT * ((pxof(KD1.get_right())[0] + 40 - pxof(KD2.get_left())[0]) / 120))
        KD2.shift(UP * (KD1[0][1].get_center()[1] - KD2[0][4].get_center()[1]))
        kd1 = ja_escrita(parte(KD1, list(range(len(KD1[0]))), "domínio r"))
        kd2 = ja_escrita(parte(KD2, list(range(len(KD2[0]))), "domínio θ"))
        s1 = VGroup(*[B1[0][i] for i in sel(B1, ["r", "le", "rhs"])])
        s2 = VGroup(*[C3[0][i] for i in sel(C3, "t")])
        resto = [m for m in (A2, A3, B0, gc) if m in self.mobjects] + [B1[0][i] for i in sel(B1, ["im", "cond"])] + \
            [C3[0][i] for i in sel(C3, ["c", "im"])]
        sai = saindo(resto)
        self.play(*[FadeOut(m) for m in sai], run_time=0.3)
        self.remove(A2, A3, B0, gc)
        self.play(ReplacementTransform(s1, kd1), ReplacementTransform(s2, kd2), run_time=0.7)
        self.remove(B1, C3)
        molD = em_volta(VGroup(KD1, KD2), GEO, 14, 2, .55, 10)
        self.play(Create(molD), th.animate(rate_func=smooth).set_value(-math.pi / 2 + .03), run_time=0.6)
        self.gat("confere com a área")
        # a sonda pinta o disco de −π/2 a π/2 (a área que a conta vai dar)
        pint = always_redraw(lambda: poly_px([v.px(0, 0)] + [v.px(*saida(t)) for t in np.linspace(-math.pi / 2, th.get_value(), 60)],
                                             mixh(BG_, MEN, .34), 1.0, z=2))
        self.add(pint)
        ar = leg("ÁREA", X5, 352, GEO, "left", 30)
        self.pena(ar, extra=[th.animate(rate_func=linear).set_value(math.pi / 2 - .03)], rt=1.2)
        pint.clear_updaters()
        Q0 = col(L([("eq", "="), ("i1", r"\displaystyle\int_{-\pi/2}^{\pi/2}"), ("i2", r"\!\int_0^{\Co{2\cos\T}}"), ("J", r"\J"), ("dr", r"\,\dr"),
                    ("dt", r"\,\dt")], X5, 0, 44))
        abaixo(ar, Q0, X5, 22)
        b2, u2, l2 = sup_sub(Q0, "i2")
        escreve_seq(self, Q0, [(lr2.f[0][2:], u2)], rt_voo=0.9, passo=0.04)
        origem(self, "limite 2 cos θ", "rótulo da circunferência coral (voo)")
        self.gat("a de dentro dá erre")
        self.varre(th, 0.0, 0.8)
        Q1 = col(L([("eq", "="), ("i1", r"\displaystyle\int_{-\pi/2}^{\pi/2}"), ("lb", r"\Big["), ("F", r"\dfrac{\R^2}{2}"), ("rb", r"\Big]_0^{\Co{2\cos\T}}"),
                    ("dt", r"\dt")], X5, 0, 44))
        abaixo(Q0, Q1, X5, 30)                                # FINAL: cada degrau na sua linha (os voos descem sem cruzar a linha de cima)
        _, ub, lb = sup_sub(Q1, "rb")
        gmap(self, 11, Q0, Q1, [("eq", "eq"), ("i1", "i1"), ("J", sel(Q1, "F")[0:1]), (u2, ub), (l2, lb), ("dt", "dt")], rt=1.3, nota="a) [r²/2]₀^{2cos θ}")
        degrau(self, "B5 área", "∫∫ r dr dθ = ∫ [r²/2]₀^{2cos θ} dθ")
        # ── K12 · Q1b: G(b) − G(a) com os valores substituídos (o 2cos θ voa do limite de cima, o 0 do de baixo) ──
        self.gat("em dois cosseno de téta")
        Q1b = col(L([("eq", "="), ("i1", r"\displaystyle\int_{-\pi/2}^{\pi/2}"), ("lp", r"\Big("), ("F", r"\dfrac{(\Co{2\cos\T})^2}{2}"), ("m", "-"),
                     ("Z", r"\dfrac{0^2}{2}"), ("rp", r"\Big)"), ("dt", r"\,\dt")], X5, 0, 44))
        abaixo(Q1, Q1b, X5, 30)
        FF, nF, bF, dF = frac_partes(Q1b, "F")
        ZZ, nZ, bZ, dZ = frac_partes(Q1b, "Z")
        src_u = VGroup(*[Q1[0][i_] for i_ in ub])
        src_l = VGroup(*[Q1[0][i_] for i_ in lb])
        escreve_seq(self, Q1b, [(src_u, nF[1:6]), (src_l, nZ[0:1])], rt_voo=0.6, passo=0.03)
        origem(self, "(2cos θ)² e 0²", "limites de cima e de baixo do colchete [r²/2] (voos)")
        degrau(self, "B5 área", "= ∫ ( (2cos θ)²/2 − 0²/2 ) dθ   [G(b) − G(a) com os valores]")
        self.gat("quatro cosseno ao quadrado")
        Q1c = col(L([("eq", "="), ("i1", r"\displaystyle\int_{-\pi/2}^{\pi/2}"), ("g", r"\dfrac{4\cos^2\T}{2}"), ("dt", r"\,\dt")], X5, 0, 44))
        abaixo(Q1b, Q1c, X5, 30)
        _, nG, bG, dG = frac_partes(Q1c, "g")
        gmap(self, 11, Q1b, Q1c, [("eq", "eq"), ("i1", "i1"), ("dt", "dt"), (nF[1:2] + nF[7:8], nG[0:1]), (nF[2:5], nG[1:4]), (nF[5:6], nG[5:6]), (bF, bG), (dF, dG)],
             rt=1.4, nota="b) (2cos θ)² = 4cos²θ; o 0²/2 some")
        degrau(self, "B5 área", "= ∫ 4cos²θ/2 dθ")
        # página 2b: as linhas que já cumpriram (a legenda ÁREA, Q0 e Q1) saem; Q1b e Q1c sobem
        self.gat("fica dois cosseno ao quadrado")
        self.varre(th, math.pi / 4, 0.8)
        sai = saindo([ar, Q0, Q1])
        dy = UP * ((pxof(Q1b.get_top())[1] - 330) / 120)
        self.play(*[FadeOut(m) for m in sai], Q1b.animate.shift(dy), Q1c.animate.shift(dy), run_time=0.5)
        self.remove(ar, Q0, Q1)
        Q2 = col(L([("eq", "="), ("i1", r"\displaystyle\int_{-\pi/2}^{\pi/2}"), ("f", r"2\cos^2\T"), ("dt", r"\,\dt"), ("cm", ",")], X5, 0, 44))
        abaixo(Q1c, Q2, X5, 30)
        fq = ordx(Q2, "f")
        gmap(self, 11, Q1c, Q2, [("eq", "eq"), ("i1", "i1"), ("dt", "dt"), (nG[1:6], fq[1:6]), (nG[0:1] + bG + dG, fq[0:1])], rt=1.3,
             nota="c) 4cos²θ/2 = 2cos²θ")
        degrau(self, "B5 área", "= ∫ 2cos²θ dθ")
        self.gat("um mais cosseno de")
        self.varre(th, math.pi / 3, 0.8)
        idn = col(TC(r"2\cos^2\T=1+\cos 2\T", pxof(Q2.get_right())[0] + 44, pxof(Q2.get_center())[1], 44, "l"))
        self.pena(idn)
        self.gat("cuja primitiva é")
        self.varre(th, 0.0, 0.8)
        # página 3: Q1b e Q1c já cumpriram; Q2 e a identidade sobem
        sai = saindo([Q1b, Q1c])
        dy2 = UP * ((pxof(Q2.get_top())[1] - 330) / 120)
        self.play(*[FadeOut(m) for m in sai], Q2.animate.shift(dy2), idn.animate.shift(dy2), run_time=0.5)
        self.remove(Q1b, Q1c)
        Q3 = col(L([("eq", "="), ("lb", r"\Big["), ("F", r"\T+\dfrac{\sen 2\T}{2}"), ("rb", r"\Big]_{-\pi/2}^{\pi/2}")], X5, 0, 44))
        abaixo(Q2, Q3, X5, 30)
        _, u1, l1_ = sup_sub(Q2, "i1")
        _, u3, l3 = sup_sub(Q3, "rb")
        gmap(self, 11, Q2, Q3, [("eq", "eq"), (u1, u3), (l1_, l3)], rt=1.3, nota="c) primitiva θ + sen 2θ/2 (com 2cos²θ = 1 + cos 2θ)")
        degrau(self, "B5 área", "= [θ + sen 2θ/2]_{−π/2}^{π/2}")
        self.gat("em pi sobre dois")
        self.varre(th, math.pi / 2 - .03, 0.8)
        Q4 = col(L([("eq", "="), ("a", r"\Big(\dfrac{\pi}{2}+0\Big)"), ("m", "-"), ("b", r"\Big(-\dfrac{\pi}{2}+0\Big)")], X5, 0, 44))
        abaixo(Q3, Q4, X5, 30)
        fo, nu, ba, de = frac_partes(Q3, "F")
        fa, na, baa, da = frac_partes(Q4, "a")
        fb, nb, bab, db = frac_partes(Q4, "b")
        plus = fo[1:2]                                     # fo = [θ, +] (fora da fração, em ordem de x)
        gmap(self, 11, Q3, Q4, [("eq", "eq"), (u3[0:1], na), (u3[1:], baa + da), (plus[-1:], fa[1:2]), (nu + ba + de, fa[2:3]),
                                (l3[0:1], fb[1:2]), (l3[1:2], nb), (l3[2:], bab + db), (plus[-1:], fb[2:3]), (nu + ba + de, fb[3:4])], rt=1.5,
             nota="d) F(π/2) − F(−π/2) com os valores")
        degrau(self, "B5 área", "= (π/2 + 0) − (−π/2 + 0)   [F(b) − F(a)]")
        # K12: de onde vem cada 0 (sen π e sen(−π)), pequeno por 1 s e some
        self.gat("que é zero")
        z0 = Q4[0][fa[2]]
        sp1 = TP(r"\Ge{\sen\pi=0}", pxof(z0.get_center())[0], pxof(z0.get_bottom())[1] + 56, 30, "c")
        self.pena(sp1)
        self.wait(0.3)
        self.play(FadeOut(sp1), run_time=0.3)
        self.remove(sp1)
        degrau(self, "B5 área", "sen π = 0   [o 0 da primeira parcela]")
        self.gat("em menos pi sobre dois")
        self.varre(th, -math.pi / 2 + .03, 0.8)
        self.gat("mais zero")
        z1 = Q4[0][fb[3]]
        sp2 = TP(r"\Ge{\sen(-\pi)=0}", pxof(z1.get_center())[0], pxof(z1.get_bottom())[1] + 56, 30, "c")
        self.pena(sp2)
        self.wait(0.2)
        self.play(FadeOut(sp2), run_time=0.3)
        self.remove(sp2)
        degrau(self, "B5 área", "sen(−π) = 0   [o 0 da segunda parcela]")
        self.gat("a diferença dá pi")
        Q5 = col(L([("eq", "="), ("pi", r"\Me{\pi}")], X5, 0, 44))
        ao_lado(Q4, Q5, 14)
        gmap(self, 11, Q4, Q5, [("eq", "eq"), (na + nb, "pi")], rt=1.2, nota="e) = π", extra=[pint.animate.set_fill(mixh(BG_, MEN, .5))])
        degrau(self, "B5 área", "= π")
        self.gat("a área de um disco")
        r1b = lin_px([v.px(1, 0), v.px(2, 0)], MEN, 4, z=8)
        l1b = TC("1", *v.px(1.5, -.12), 40, "c")
        cf = leg("CONFERE:", X5, 1006, GEO, "left", 30)
        CK = col(L([("pi", r"\pi"), ("c", r"\cdot"), ("u", "1"), ("sq", "^2")], 1215, 996, 44))
        self.pena(l1b, cf, lag=0.1, passo=0.03, extra=[Create(r1b, run_time=0.4)])
        escreve_seq(self, CK, [(Q5[0][sel(Q5, "pi")[0]:sel(Q5, "pi")[-1] + 1], "pi", 0.9), (l1b, "u", -0.3)], rt_voo=0.8, passo=0.05)
        origem(self, "π · 1²", "π do resultado; 1 do raio do disco (voos)")
        ck = check_px(pxof(CK.get_right())[0] + 32, 996, MEN, .9)
        molk = em_volta(VGroup(CK, ck), GEO, 14, 2, .55, 10)
        self.play(Create(ck), Create(molk), run_time=0.4)
        self.marca("07")
        son.clear_updaters()
        self.sai_fim()

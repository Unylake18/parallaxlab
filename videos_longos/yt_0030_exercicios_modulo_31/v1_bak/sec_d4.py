"""Lote PD4 · D4 O CAMPO QUE NÃO MELHORA DE PERTO (alvos 15, 16, 17, 18). F₄ = xy/(x² + y²)·(x, y), F₄(0, 0) = 0⃗, setas proporcionais com teto.
Palco (alvo 15): diagonais e círculo de raio 2 tracejados (recortados), fórmula, legendas das direções, itens + PAUSE E TENTE; item a (‖F‖ por polares).
ε-δ no layout B (alvo 16): disco δ = 2ε, mancha das pontas ρ = ε|sen 2θ| que encosta no disco ε só nas diagonais; ε de 1 a 0,5 e de volta. Item b
(três caixinhas ✓, CONTÍNUO); item c no palco (pontos andando nos eixos, tabela zero); item d zoom × 1 / × 10 / × 100 (alvo 17) com os dois
quadradinhos (RK4); item e no palco em contexto (∂P/∂x pela regra do quociente, pontos nas três circunferências, NÃO É C¹, alvo 18)."""
from lib30 import *  # noqa: F401,F403

FUNDO_M = "#141031"
MENTA35 = mix(CAMPO, FUNDO_M, 0.65).to_hex()
Q4 = [((1 / SQ2) * 1.2, (1 / SQ2) * 1.2), (-(1 / SQ2) * 1.2, (1 / SQ2) * 1.2)]


def diagonais(v=VA, box=LA):
    return VGroup(linha_rec(v, [(-4, -4), (4, 4)], box, GEO, 2, .4, dash=(8, 8)), linha_rec(v, [(-4, 4), (4, -4)], box, GEO, 2, .4, dash=(8, 8)))


def rosa_pts(eps, n=400):
    th = np.linspace(0, 2 * PI, n + 1)
    r = eps * np.abs(np.sin(2 * th))
    return np.stack([r * np.cos(th), r * np.sin(th)], 1)


class Rosa(VGroup):
    def __init__(self, v, eps):
        super().__init__()
        self.v = v
        self.ch = VMobject().set_fill(MENTA35, 1).set_stroke(width=0)
        self.bd = VMobject().set_fill(opacity=0).set_stroke(CAMPO2, 2 / 1.2, 1)
        for m in (self.ch, self.bd):
            m._sem_contorno = True
        self.add(self.ch, self.bd)
        self.em(eps)
        self.set_z_index(4)

    def em(self, eps):
        P = [self.v.c2p(*p) for p in rosa_pts(eps)]
        self.ch.set_points_as_corners(P)
        self.bd.set_points_as_corners(P)
        return self


def caixinha(txt_, x, y):
    t = T(txt_, 0, y, 30)
    ck = MathTex(r"\checkmark", font_size=fs(30)).set_color(CAMPO2)
    ck._sem_contorno = True
    g = VGroup(t, ck)
    ck.next_to(t, RIGHT, buff=10 / 120).set_y(t.get_center()[1])
    g.shift(RIGHT * (PX(x, 0)[0] - g.get_center()[0]))
    r = RoundedRectangle(width=g.width + 28 / 120, height=g.height + 22 / 120, corner_radius=8 / 120).move_to(g.get_center())
    r.set_fill(PLACA_V4, 0.9).set_stroke(GEO, 2 / 1.2, 1)
    r._sem_contorno, r._placa = True, True
    return VGroup(r.set_z_index(24), g.set_z_index(25))


class LoteD4(Base):
    ANTES = "DUAS REGRAS · UM ROTACIONAL NUNCA DIVERGE"

    def palco(self, ctx=False, skip=None, mref=1.6, nome="D4 F₄"):
        zera_chapas()
        ch = chapa_px(*LA, nome=f"{nome} palco A", v=VA)
        cp = campoP30(VA, F4, passo=.5, rmin=.3, mref=mref, ctx=ctx, skip=skip, nome=nome)
        return ch, cp

    def corpo(self):
        # ── D4-1 · a fórmula ──
        self.an("D4-1")
        self.secao("O CAMPO QUE NÃO MELHORA DE PERTO")
        ch, cp = self.palco(skip=clar28([(-.2, -2.75, 1.8, -2.25)]))
        o0 = ponto7(VA.c2p(0, 0), POS, 8, 9)
        troca(self, "D3b → D4 (palco)")
        self.play(FadeIn(ch), cresce_campo(cp, 0.8), FadeIn(o0), run_time=0.8)
        FF = Pz([r"\F=\dfrac{\X\Y}{\X^2+\Y^2}\,(\X,\ \Y)", r",\quad \F(0,0)=\vec0"], 1110, 300, 38, caneta=False)
        s_ = lambda m, *ii: VGroup(*[m[0][g] for i in ii for g in m._rg[i]])
        self.gat("este campo pega o vetor posição")
        self.play(caneta(s_(FF, 0), ritmo=0.4))
        self.gat("a gente define a seta como zero")
        self.play(caneta(s_(FF, 1), ritmo=0.4))
        self.remove(*[m for m in self.mobjects if isinstance(m, VGroup) and len(m) and all(g in FF[0].submobjects for g in m.submobjects)])
        self.add(FF)
        self.ate(1.0)

        # ── D4-2 · o desenho; os itens (alvo 15) ──
        self.an("D4-2")
        dg = diagonais()
        c2 = vcirc(VA, 2, GEO, 2, dash=(8, 8), alpha=.8).set_z_index(5)
        r2 = TP(r"\text{raio } 2", *canto_xy(VA, .8, -2.5), 28)
        self.gat("olha o desenho")
        self.play(Create(dg), Create(c2), FadeIn(r2), run_time=0.8)
        lgs = [legenda("DIAGONAIS DE SUBIDA: PARA FORA", 1114, 560, GEO), legenda("AS OUTRAS: PARA DENTRO", 1114, 605, GEO),
               legenda("NOS EIXOS: NENHUMA SETA", 1114, 650, GEO)]
        for fr, m in zip(("nas diagonais de subida", "nas outras diagonais", "em cima dos eixos"), lgs):
            self.gat(fr)
            self.play(FadeIn(m, shift=0.05 * UP), run_time=0.4)
        it1, it2 = legenda("ITENS: LIMITE · CONTINUIDADE · PARCIAIS", 1114, 760, BR), legenda("ZOOM · CLASSE C¹", 1114, 805, BR)
        self.gat("pausa o vídeo e tenta")
        self.pausa()
        self.play(FadeIn(it1, shift=0.05 * UP), FadeIn(it2, shift=0.05 * UP), run_time=0.5)
        self.ate(1.0)

        # ── D4-3 · item a ──
        self.an("D4-3")
        NF = Pz([r"\|\F\|=", r"\dfrac{|\X\Y|}{r}", "=", r"\dfrac{r\,|\operatorname{sen}2\theta|}{2}", r"\le\dfrac r2"], 1110, 440, 42, caneta=False)
        self.gat("a seta tem tamanho igual ao módulo")
        self.play(caneta(s_(NF, 0, 1), ritmo=0.4))
        self.gat("em polares")
        self.play(caneta(s_(NF, 2, 3), ritmo=0.4))
        self.gat("e isso nunca passa da metade")
        self.play(caneta(s_(NF, 4), ritmo=0.4))
        self.remove(*[m for m in self.mobjects if isinstance(m, VGroup) and len(m) and all(g in NF[0].submobjects for g in m.submobjects)])
        self.add(NF)
        self.ate(1.0)

        # ── D4-4 · ε-δ no layout B (alvo 16) ──
        self.an("D4-4")
        self.secao("O CAMPO QUE NÃO MELHORA DE PERTO · LIMITE")
        zera_chapas()
        vl, vr = VB(BE, 480, 540, 140), VB(BD, 1440, 540, 140)
        pe, pd = chapa_px(*BE, nome="D4 ε-δ esq.", v=vl), chapa_px(*BD, nome="D4 ε-δ dir.", v=vr)
        ce = campoP30(vl, F4, -2.25, 2.25, -1.75, 2.25, .5, rmin=.3, mref=1, ctx=True, skip=lambda X, Y: abs(math.hypot(X, Y) - 2) < .3 or (-2.35 < X < -.75 and 1.45 < Y < 2.3), nome="D4 ε-δ (contexto)")
        eps = ValueTracker(1.0)
        dc = vcirc(vl, 2, POS, 3).set_z_index(6)
        dc.add_updater(lambda m: m.become(vcirc(vl, 2 * eps.get_value(), POS, 3).set_z_index(6)))
        oe = ponto7(vl.c2p(0, 0), POS, 9, 9)
        de = TP(r"\del = 2\eps", *canto_xy(vl, -1.55, 1.85), 32)
        ne = legenda("ONDE VOCÊ ANDA", 480, 868, GEO, "center", 28)
        ex = VGroup(vlinha(vr, [(-2.4, 0), (2.4, 0)], GEO, 2, alpha=.35), vlinha(vr, [(0, -2.4), (0, 2.4)], GEO, 2, alpha=.35)).set_z_index(2)
        ro = Rosa(vr, 1.0)
        ro.add_updater(lambda m: m.em(eps.get_value()))
        ec = vcirc(vr, 1, CAMPO2, 3).set_z_index(6)
        ec.add_updater(lambda m: m.become(vcirc(vr, eps.get_value(), CAMPO2, 3).set_z_index(6)))
        od = ponto7(vr.c2p(0, 0), GEO, 6, 9)
        el = TP(r"\eps", *canto_xy(vr, .95, 1.0), 34)
        ml = leg_mix(["A MANCHA DAS PONTAS CABE NO DISCO ", r"$\varepsilon$"], 1440, 860, GEO, "center", 26)
        self.gat("agora o desafio do épsilon")
        self.limpa_junto()
        troca(self, "D4 palco → layout B (ε-δ)")
        self.play(FadeIn(pe), FadeIn(pd), cresce_campo(ce, 0.6), FadeIn(oe), FadeIn(ex), FadeIn(od), FadeIn(ne), run_time=0.8)
        self.gat("alguém escolhe um épsilon")
        self.play(Create(ec), FadeIn(el), run_time=0.6)
        self.gat("você responde com delta")
        self.play(Create(dc), FadeIn(de), run_time=0.6)
        self.gat("a seta tem tamanho de no máximo")
        self.play(FadeIn(ro), FadeIn(ml, shift=0.05 * UP), run_time=0.6)
        IM = TC(r"0<\|\Xp\|<\del=2\eps\ \Rightarrow\ \|\F(\Xp)\|\le\dfrac{\|\Xp\|}{2}<\eps", 960, 965, 40, "c")
        self.play(caneta(IM, ritmo=0.25))
        self.gat("venceu para qualquer épsilon")
        self.play(eps.animate.set_value(.5), run_time=1.2)
        self.play(eps.animate.set_value(1.0), run_time=1.2)
        for m in (dc, ro, ec):
            m.clear_updaters()
        self.ate(1.0)

        # ── D4-5 · item b (caixinhas) e item c (no palco) ──
        self.an("D4-5")
        cx = [caixinha("DOMÍNIO", 620, 985), caixinha("LIMITE", 900, 985), caixinha("IGUAL À SETA", 1220, 985)]
        self.gat("o ponto está no domínio")
        self.play(FadeOut(IM), FadeIn(cx[0]), run_time=0.4)
        self.remove(IM)
        self.gat("o limite existe")
        self.play(FadeIn(cx[1]), run_time=0.4)
        self.gat("e é igual à seta do ponto")
        self.play(FadeIn(cx[2]), run_time=0.4)
        ct = T("CONTÍNUO", 1560, 1000, 40, "center", CAMPO2)
        self.gat("os três pedaços passam")
        self.play(FadeIn(ct, shift=0.05 * UP), run_time=0.4)
        # item c: volta ao palco
        self.secao("O CAMPO QUE NÃO MELHORA DE PERTO")
        ch, cp = self.palco(skip=clar28([(-.2, -2.75, 1.8, -2.25)]), nome="D4 F₄ (item c)")
        o0 = ponto7(VA.c2p(0, 0), POS, 8, 9)
        dg, c2 = diagonais(), vcirc(VA, 2, GEO, 2, dash=(8, 8), alpha=.8).set_z_index(5)
        r2 = TP(r"\text{raio } 2", *canto_xy(VA, .8, -2.5), 28)
        FF2 = TC(FF._tex, 1110, 300, 38, caneta=False)
        self.gat("item c as derivadas parciais")
        self.limpa_junto()
        troca(self, "D4 layout B → palco (item c)")
        self.play(FadeIn(ch), FadeIn(cp), FadeIn(o0), FadeIn(dg), FadeIn(c2), FadeIn(r2), FadeIn(FF2), run_time=0.8)
        pa = ponto7(VA.c2p(-3.6, 0), AMB, 9, 12)
        pm = ponto7(VA.c2p(0, -2.6), MAG, 9, 12)
        self.gat("andando pelo eixo horizontal")
        self.play(FadeIn(pa), run_time=0.2)
        self.play(pa.animate.move_to(VA.c2p(3.6, 0)), run_time=1.5, rate_func=linear)
        self.gat("pelo vertical a mesma coisa")
        self.play(FadeOut(pa), FadeIn(pm), run_time=0.2)
        self.remove(pa)
        self.play(pm.animate.move_to(VA.c2p(0, 2.6)), run_time=1.5, rate_func=linear)
        self.play(FadeOut(pm), run_time=0.2)
        self.remove(pm)
        J0 = TC(r"J=\begin{pmatrix}\Am{0} & \Mg{0}\\ \Am{0} & \Mg{0}\end{pmatrix}", 1120, 470, 44)
        self.gat("a tabela é toda zero")
        self.play(caneta(J0, ritmo=0.4))
        M0 = TC(r"\rot=\V0\ \cdot\ \dv=\D0\ \cdot\ d_1=\Lm0\ \cdot\ d_2=\Lm0", 1120, 600, 34)
        self.gat("rotacional zero")
        self.play(caneta(M0, ritmo=0.25))
        pv = legenda("PREVISÃO: PERTO DA ORIGEM, NADA ACONTECE", 1124, 690, GEO, "left", 26)
        self.gat("a previsão seria")
        self.play(FadeIn(pv, shift=0.05 * UP), run_time=0.4)
        self.ate(1.0)

        # ── D4-6 · item d: o zoom (alvo 17) ──
        self.an("D4-6")
        self.secao("O CAMPO QUE NÃO MELHORA DE PERTO · ZOOM")
        zera_chapas()
        pe, pd = chapa_px(*BE, nome="D4 zoom esq.", v=vl), chapa_px(*BD, nome="D4 zoom dir.", v=vr)
        z1 = campoP30(vl, F4, -2.25, 2.25, -1.75, 2.25, .5, rmin=.3, mref=1, nome="D4 zoom × 1")
        peds = [quad30(vr, c, .4) for c in Q4]
        fans = [fantasma(vr, quad_pts(c, .4)) for c in Q4]
        z10 = campoP30(vr, F4, -2.25, 2.25, -1.75, 2.25, .5, rmin=.3, mref=1, nome="D4 zoom × 10")
        st = {"on": False}
        clareira(z10, lambda: ou(*[clar_ped(p, .2) for p in peds], *[dq(c, .4) for c in Q4]) if st["on"] else NADA)
        oz1, oz2 = ponto7(vl.c2p(0, 0), POS, 8, 9), ponto7(vr.c2p(0, 0), POS, 8, 9)
        nz1 = legenda("ZOOM × 1", 480, 868, GEO, "center", 28)
        nz2 = legenda("ZOOM × 10 (MESMO DESENHO)", 1440, 868, GEO, "center", 28)
        nz3 = legenda("ZOOM × 100 (MESMO DESENHO)", 1440, 868, GEO, "center", 28)
        self.gat("item d confere com um zoom")
        self.limpa_junto()
        troca(self, "D4 palco → layout B (zoom)")
        self.play(FadeIn(pe), FadeIn(pd), cresce_campo(z1, 0.6), FadeIn(oz1), FadeIn(nz1), run_time=0.8)
        self.gat("aqui olha o zoom de dez vezes")
        self.play(cresce_campo(z10, 0.6), FadeIn(oz2), FadeIn(nz2), run_time=0.6)
        self.gat("e o de cem vezes também")
        troca_linha(self, nz2, nz3)
        hom = TC(r"\F(s\,\Xp)=s\,\F(\Xp)", 960, 948, 40, "c")
        self.gat("esse campo é homogêneo")
        self.play(caneta(hom, ritmo=0.4))
        nl = legenda("DE PERTO, O CAMPO NUNCA FICA PARECIDO COM A TABELA ZERO", 960, 1020, GEO, "center", 26)
        self.gat("então ele nunca fica parecido")
        self.play(FadeIn(nl, shift=0.05 * UP), run_time=0.4)
        self.gat("tem quadradinho crescendo")
        st["on"] = True
        self.play(*[FadeIn(p) for p in peds], *[FadeIn(f) for f in fans], run_time=0.4)
        a0 = [p.area() for p in peds]
        self.play(*[anda(p, fl4, .6, 2.0, rate=linear, nome=f"D4 zoom quadradinho {i + 1}") for i, p in enumerate(peds)])
        for i, p in enumerate(peds):
            print(f"[D4] quadradinho {Q4[i]}: área {a0[i]:.4f} → {p.area():.4f}")
        self.ate(1.0)

        # ── D4-7 · item e: não é C¹ (alvo 18) ──
        self.an("D4-7")
        self.secao("O CAMPO QUE NÃO MELHORA DE PERTO · CLASSE C¹")
        z10.clear_updaters()
        RR = (2.5, 1.25, .625)
        ch, cp = self.palco(ctx=True, skip=lambda X, Y: any(abs(math.hypot(X, Y) - r) < .3 for r in RR) or any(math.hypot(X - 2.85 * math.cos(t), Y - 2.75 * math.sin(t)) < .55 for t in (PI / 4, 3 * PI / 4)), nome="D4 F₄ (contexto, item e)")
        circs = [vcirc(VA, r, GEO, 2, alpha=.5).set_z_index(5) for r in RR]
        Pq = TC(r"\Pp=\dfrac{\X^2\Y}{\X^2+\Y^2}", 1120, 300, 40)
        self.gat("item e calcula a derivada")
        self.limpa_junto()
        troca(self, "D4 layout B → palco (item e)")
        self.play(FadeIn(ch), FadeIn(cp), *[Create(c) for c in circs], run_time=0.8)
        self.gat("a componente horizontal é o quadrado")
        self.play(caneta(Pq, ritmo=0.4))
        Q1 = TC(r"\dfrac{\partial\Pp}{\dx}=\dfrac{2\X\Y\,(\X^2+\Y^2)-\X^2\Y\cdot 2\X}{(\X^2+\Y^2)^2}", 1120, 420, 36)
        self.gat("regra do quociente")
        self.play(caneta(Q1, ritmo=0.3))
        Q2 = Pz(["=", r"\big(", r"2\X^3\Y", "+", r"2\X\Y^3", "-", r"2\X^3\Y", r"\big)", "/", r"(\X^2+\Y^2)^2"], 1120, 520, 36)
        Q3 = Pz(["=", r"2\X\Y^3", "/", r"(\X^2+\Y^2)^2"], 1120, 520, 36, caneta=False)
        Q2.shift(RIGHT * (Q1[0][5].get_left()[0] - Q2.get_left()[0]))
        Q3.shift(RIGHT * (Q2.get_left()[0] - Q3.get_left()[0]))
        self.gat("os termos com a quarta potência")
        self.play(caneta(Q2, ritmo=0.25))
        self.play(tbgm30(Q2, Q3, [(0, 0), (4, 1), (8, 2), (9, 3)], rt=1.2))
        self.remove(Q2)
        limpa_soltos(self)
        self.add(Q3)
        RES = TC(r"\dfrac{\partial\Pp}{\dx}=\dfrac{2\X\Y^3}{(\X^2+\Y^2)^2}", 1120, 300, 44, caneta=False)
        self.gat("agora olha essa derivada")
        self.play(FadeOut(Pq), FadeOut(Q1), TransformMatchingShapes(Q3, ja_escrita(RES)), run_time=1.0)
        self.remove(Pq, Q1, Q3)
        self.add(RES)
        dP = lambda X, Y: 2 * X * Y ** 3 / (X * X + Y * Y) ** 2
        eixo_p, diag_p = [], []
        for r in RR:
            e_, d_ = [], []
            for k in range(8):
                t = k * PI / 4
                p = (r * math.cos(t), r * math.sin(t))
                v_ = dP(*p)
                (e_ if abs(v_) < 1e-6 else d_).append(ponto7(VA.c2p(*p), GEO if abs(v_) < 1e-6 else AMB, 6 if abs(v_) < 1e-6 else 9, 9))
                if abs(v_) > 1e-6:
                    print(f"[D4] ∂P/∂x em r = {r}, θ = {k}·45°: {v_:+.4f}")
            eixo_p.append(e_)
            diag_p.append(d_)
        labs = {t: TP(s, *canto_xy(VA, 2.85 * math.cos(t), 2.75 * math.sin(t)), 30) for t, s in ((PI / 4, r"\dfrac12"), (3 * PI / 4, r"-\dfrac12"), (0, "0"), (PI / 2, "0"))}
        ne_ = legenda("NOS EIXOS: 0", 1124, 420, GEO)
        self.gat("nos eixos ela vale zero")
        for e_ in eixo_p:
            self.play(*[FadeIn(p, scale=0.5) for p in e_], run_time=0.3)
        self.play(FadeIn(labs[0]), FadeIn(labs[PI / 2]), FadeIn(ne_, shift=0.05 * UP), run_time=0.4)
        nd = leg_mix(["NA DIAGONAL: ½, POR MAIS PERTO QUE SE CHEGUE"], 1124, 465, AMB, "left", 26)
        self.gat("na diagonal vale meio")
        for d_ in diag_p:
            self.play(*[FadeIn(p, scale=0.5) for p in d_], run_time=0.3)
        self.play(FadeIn(labs[PI / 4]), FadeIn(labs[3 * PI / 4]), FadeIn(nd, shift=0.05 * UP), run_time=0.4)
        nc = T("NÃO É C¹", 1120, 570, 44, cor=CORAL)
        self.gat("o campo não é de classe")
        self.play(FadeIn(nc, shift=0.05 * UP), run_time=0.4)
        ra = TC(r"\dfrac{\|\text{erro}\|}{\|\Hh\|}=\dfrac12\ \text{na diagonal}\ \not\to 0", 1120, 680, 36)
        self.gat("e a tabela perde a garantia")
        self.play(caneta(ra, ritmo=0.25))
        cg = legenda("C¹ GARANTE A TABELA; AQUI ELA FALHA", 1124, 825, GEO, "left", 26)
        self.gat("o cê um é uma garantia")
        self.play(FadeIn(cg, shift=0.05 * UP), run_time=0.4)
        nd2 = legenda("NÃO É DIFERENCIÁVEL NA ORIGEM", 1124, 780, BR)
        self.gat("que a aproximação falha")
        self.play(FadeIn(nd2, shift=0.05 * UP), run_time=0.4)
        self.ate(1.0)

        # ── D4-8 · a escada ──
        self.an("D4-8")
        pb = legenda("TER DERIVADAS PARCIAIS NÃO BASTA", 1124, 875, CORAL, "left", 26)
        self.gat("ter derivadas parciais não basta")
        self.play(FadeIn(pb, shift=0.05 * UP), run_time=0.4)
        self.sai_fim()

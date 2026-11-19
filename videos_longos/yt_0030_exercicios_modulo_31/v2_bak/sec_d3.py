"""Lote PD3 · D3 A FAMÍLIA DE REDEMOINHOS · v2 (alvos v2_d3r1, v2_d3r2, v2_d3r3, v2_d3g + 09–12 v1). Palco: v_α numa rede viva (α só muda nas
trocas) com as circunferências r = 1, 2, 3 tracejadas. Rapidez em três glyph maps. rot: molde, Q = x s^{−α} (x e s voam de v), molde da regra do produto,
a cadeia em caneta sincronizada, fusão, evidência, ∂P/∂y por cópia, substituição no molde e 6 glyph maps até (2 − 2α)/(x² + y²)^α. div: molde, só a
cadeia, cópia, substituição, cancelamento R14. Leitura: α voa do seletor para a substituição. Origem e giro de 90° (w = (Q, −P))."""
from alg30 import *  # noqa: F401,F403

C0, S0 = (1.75, 0.0), 0.7
PTS = [(X, Y) for X in np.arange(-3.5, 3.5 + 1e-6, .5) for Y in np.arange(-2.5, 2.5 + 1e-6, .5) if math.hypot(X, Y) >= .3]
MM = interp_tab([(0, 3.0), (.5, 1.0), (1, 1.2), (2, 1.2)])
T_FL = lambda a, c=C0: .35 * math.hypot(*c) ** (2 * a)
IDX_A = {0: 1, .5: 2, 1: 3, 2: 4}
A_, S_, SM, SM1 = r"\alpha", "s", r"s^{-\alpha}", r"s^{-\alpha-1}"
VV = [("v", r"\vv="), ("fr", r"\dfrac{(-\Y,\ \X)}{(\X^2+\Y^2)^{\alpha}}")]


def cartao_alpha(k, a, ccw, c=(2.2, 0.0), s=.6):
    X0 = CC[k][0]
    v = VB(CC[k], X0 + 240, 540, 56)
    ch = chapa_px(*CC[k], nome=f"D3 cartão α = {a}", v=v)
    T_ = .35 / math.pow(2.2, -2 * a)
    fl = flV(a)
    Fc = ponto_fl(fl, c, T_)
    sk = ou(clarPoly(borda_fl(fl, c, s, T_), .25), dq(c, s), clarPoly(circ_pts(.8, Fc, 12), .1))
    cmp = campo30(v, VORTA(a), -3.5, 3.5, -3.5, 3.5, .75, rmin=.6, mmax=3 if a == 0 else 1.2, skip=sk, nome=f"D3 cartão α = {a}")
    ped = quad30(v, c, s).em(fl, T_)
    g = VGroup(ch, cmp, fantasma(v, quad_pts(c, s)), ped, ponto7(v.c2p(0, 0), GEO, 5, 8))
    if ccw is not None:
        g.add(giro30(v, Fc, .62, ccw))
    return g


def SUB(a):
    """Substituição do α na fórmula do rot (a linha de baixo da leitura)."""
    return {0: [("rot", r"\V{\rot}="), ("o", r"(2-2\cdot"), ("a", r"\Am{0}"), ("c", ")"), ("d", r"/s^{0}"), ("res", r"=\V{2}")],
            .5: [("rot", r"\V{\rot}="), ("o", r"(2-"), ("a", r"\Am{1}"), ("c", ")"), ("d", r"/s^{1/2}"), ("res", r"=\V{1/r}")],
            1: [("rot", r"\V{\rot}="), ("o", r"(2-"), ("a", r"\Am{2}"), ("c", ")"), ("d", r"/s"), ("res", r"=\V{0}")],
            2: [("rot", r"\V{\rot}="), ("o", r"(2-"), ("a", r"\Am{4}"), ("c", ")"), ("d", r"/s^{2}"), ("res", r"=\V{-2/r^4}")]}[a]


class LoteD3(Base):
    ANTES = "DESENHAR SEM MIL SETAS"

    def corpo(self):
        # ── D3-1 · enunciado ──
        self.an("D3-1")
        self.secao("A FAMÍLIA DE REDEMOINHOS")
        zera_chapas()
        chA = chapa_px(*LA, nome="D3 palco A", v=VA)
        cmp = CampoVivo(VA, PTS, VORTA, MM, .5, p0=0.0, nome="D3 v_α")
        circs = VGroup(*[linha_rec(VA, circ_pts(r), LA, GEO, 2, .35, dash=(8, 9)) for r in (1, 2, 3)])
        troca(self, "D2 → D3 (palco)")
        self.play(FadeIn(chA), cresce_campo(cmp, 1.0), run_time=1.0)
        fv = L(VV, 1120, 285, 40)
        self.gat("menos a coordenada vertical")
        escreve(self, fv, 0.4)
        fa = L([("a", r"\alpha="), ("0", r"0\quad"), ("m", r"\tfrac12\quad"), ("1", r"1\quad"), ("2", "2")], 1120, 380, 38)
        grp = lambda a: fa.pi(IDX_A[a])
        cx = caixa_em(grp(0), pad=10)
        self.gat("cada valor do expoente alfa")
        escreve(self, fa, 0.4)
        self.play(Create(cx), run_time=0.4)
        self.gat("pausa o vídeo e tenta")
        self.pausa()
        self.ate(1.0)

        # ── D3-2 · as circunferências; a rapidez em três glyph maps; α correndo ──
        self.an("D3-2")
        self.gat("tangentes às circunferências")
        self.play(Create(circs), run_time=1.0)
        n1 = L([("n", r"\|\vv\|="), ("num", r"\|(-\Y,\ \X)\|"), ("bar", "/"), ("den", r"s^{\alpha}")], 1120, 470, 38)
        raio = vlinha(VA, [(0, 0), (2 * math.cos(2.4), 2 * math.sin(2.4))], GEO, 3).set_z_index(8)
        self.gat("o vetor de cima tem tamanho")
        escreve(self, n1, 0.35)
        n2 = L([("n", r"\|\vv\|="), ("num", "r"), ("bar", "/"), ("den", r"r^{2\alpha}")], 1120, 470, 38)
        gm(self, n1, n2, rt=0.8, extra=[Create(raio)])
        acende(self, [n2.p("num"), raio], AMB, 1.0)
        self.gat("então a rapidez é a distância")
        n3 = gm(self, n2, L([("n", r"\|\vv\|="), ("num", r"r^{\,1-2\alpha}")], 1120, 470, 38), rt=0.8)
        self.play(FadeOut(raio), run_time=0.3)
        self.remove(raio)
        self.gat("com alfa zero a rapidez cresce")              # R16: o expoente e o α = 0 citados acendem
        acende(self, [n3.p("num"), grp(0)], AMB, 1.0)
        est = {"a": 0}

        def troca_a(a, rt=1.5):
            self.play(troca_p(cmp, a, rt), cx.animate.become(caixa_em(grp(a), pad=10)), run_time=rt)
            est["a"] = a
            print(f"[D3] α = {a}: mmax {MM(a):.2f}")
        self.gat("com alfa meio a rapidez")
        troca_a(.5)
        self.gat("com alfa um ela cai")
        troca_a(1)
        self.ate(1.0)

        # ── D3-3 · a conta do rotacional (alvos v2_d3r1 e v2_d3r2) e do divergente (v2_d3r3) ──
        self.an("D3-3")
        fan = fantasma(VA, quad_pts(C0, S0))
        R0 = L([("rot", r"\V{\rot}="), ("dQ", r"\dfrac{\partial\Qq}{\dx}"), ("men", "-"), ("dP", r"\dfrac{\partial\Pp}{\dy}")], 1120, 400, 38)
        self.gat("agora a conta do rotacional")
        self.play(FadeOut(fa), FadeOut(cx), FadeOut(n3), troca_p(cmp, .5, 1.0), FadeIn(fan), run_time=1.0)
        self.remove(fa, cx, n3)
        est["a"] = .5
        escreve_p(self, R0, ["rot", "dQ"], 0.35)
        self.gat("menos a derivada da componente horizontal")
        escreve_p(self, R0, ["men", "dP"], 0.35)
        junta(self, R0)
        QL = L([("Q", r"\Qq="), ("x", r"\X\,"), ("sm", SM), ("vg", r",\qquad "), ("s", "s="), ("s2", r"\X^2+\Y^2")], 1120, 495, 36)
        eixo = [s for s in cmp if abs(s._xy[1]) < 1e-6 and s._xy[0] > 0]
        num, den = num_den(fv.p("fr"))
        self.gat("a componente vertical é a coordenada")
        escreve_p(self, QL, ["Q"], 0.4)
        acende(self, eixo, CAMPO2, 1.0)
        voa(self, num[4], QL.p("x"), rt=0.6)
        escreve_p(self, QL, ["sm", "vg", "s"], 0.35)
        voa(self, VGroup(*den[1:6]), QL.p("s2"), rt=0.6)
        junta(self, QL)
        PR = L([("dQ", r"\dfrac{\partial\Qq}{\dx}="), ("a", r"(\X)^{\prime}"), ("sm", SM), ("m", "+"), ("x", r"\X\,"), ("b", r"(s^{-\alpha})^{\prime}")], 1120, 600, 36)
        self.gat("regra do produto")
        escreve(self, PR, 0.15)
        P2 = L([("eq", "="), ("um", r"1\cdot "), ("sm", SM), ("m", "+"), ("x", r"\X\cdot\big("), ("ch", r"-\alpha\,s^{-\alpha-1}"), ("dx", r"\cdot 2\X"), ("fp", r"\big)")],
               1150, 700, 36)
        self.gat("a primeira parte dá a própria")
        escreve_p(self, P2, ["eq", "um", "sm"], 0.35)
        self.gat("a segunda pela regra da cadeia")
        escreve_p(self, P2, ["m", "x", "ch"], 0.35)
        self.gat("vezes duas vezes a coordenada horizontal")
        escreve_p(self, P2, ["dx", "fp"], 0.35)
        junta(self, P2)
        lg = legenda("REGRA DO PRODUTO · REGRA DA CADEIA", 1124, 790, GEO, "left", 26)
        self.play(FadeIn(lg), run_time=0.3)
        # fusão (R13): as duas linhas da regra viram uma; depois a evidência
        F1 = L([("dQ", r"\dfrac{\partial\Qq}{\dx}="), ("sm", SM), ("m2", "-"), ("ax", r"2\alpha\X^2"), ("sm1", SM1)], 1120, 580, 36)
        self.gat("põe a potência com um a menos")
        funde(self, [PR, P2], F1, rt=1.0, ka=["dQ", "a_", "sm", "m_", "x_", "b_", "eq_", "um_", "sm", "m2", "ax", "sm1", "ax", "fp_"])
        F2 = L([("dQ", r"\dfrac{\partial\Qq}{\dx}="), ("sm1", SM1), ("ab", r"\,(s"), ("m2", "-"), ("ax", r"2\alpha\X^2"), ("fc", ")")], 1120, 580, 36)
        gm(self, F1, F2, rt=0.9, ka=["dQ", "ab", "m2", "ax", "sm1"])
        PQ = L([("P", r"\Pp="), ("my", r"-\Y\,"), ("smp", SM), ("vp", r",\ \ "), ("Q", r"\Qq="), ("x", r"\X\,"), ("sm", SM), ("vg", r",\ \ "), ("s", "s="), ("s2", r"\X^2+\Y^2")],
               1120, 485, 34)
        self.gat("a outra derivada é igualzinha")
        gm(self, QL, PQ, rt=0.8, voos={"my": VGroup(*num[1:3])})
        F3 = L([("dQ", r"\dfrac{\partial\Pp}{\dy}="), ("neg", "-"), ("sm1", SM1), ("ab", r"\,(s"), ("m2", "-"), ("ax", r"2\alpha\Y^2"), ("fc", ")")], 1120, 680, 36)
        gm(self, F2, F3, rt=0.9, copia=True)
        # substituição no molde do rot e os 6 glyph maps (alvo v2_d3r2 → r3)
        RS = L([("rot", r"\V{\rot}="), ("A", r"s^{-\alpha-1}(s-2\alpha\X^2)"), ("men", "-"), ("ap", r"\big("), ("B", r"-s^{-\alpha-1}(s-2\alpha\Y^2)"), ("fp", r"\big)")],
               1120, 790, 34)
        self.gat("e o sinal trocado")
        self.play(FadeOut(lg), run_time=0.3)
        self.remove(lg)
        gm(self, R0, RS, rt=0.9, copia=True, voos={"A": F2.p("sm1", "ab", "m2", "ax", "fc"), "B": F3.p("neg", "sm1", "ab", "m2", "ax", "fc")})
        RS2 = L([("rot", r"\V{\rot}="), ("A", r"s^{-\alpha-1}(s-2\alpha\X^2)"), ("pl", "+"), ("B", r"s^{-\alpha-1}(s-2\alpha\Y^2)")], 1120, 790, 34)
        gm(self, RS, RS2, rt=0.7)
        RS3 = L([("rot", r"\V{\rot}="), ("e", SM1), ("ap", "("), ("s1", "s"), ("ax", r"-2\alpha\X^2"), ("pl", "+"), ("s2", "s"), ("ay", r"-2\alpha\Y^2"), ("fp", ")")], 1120, 790, 34)
        self.gat("a distância ao quadrado aparece duas vezes")
        AA = Duas(RS2)
        AA.ks = ["rot", "e", "ap", "s1", "ax", "fp", "pl", "e", "ap2", "s2", "ay", "fp"]
        AA._rg = [RS2._rg[0]] + _split(RS2, 1, [5, 1, 1, 5, 1]) + [RS2._rg[2]] + _split(RS2, 3, [5, 1, 1, 5, 1])
        gm(self, AA, RS3, rt=0.9)
        self.remove(RS2)
        RS4 = L([("rot", r"\V{\rot}="), ("e", SM1), ("ap", "("), ("s1", "2s"), ("m", "-"), ("al", r"2\alpha"), ("q", r"(\X^2+\Y^2)"), ("fp", ")")], 1120, 790, 34)
        self.gat("os dois termos com alfa se juntam")
        gm(self, RS3, RS4, rt=0.9, ka=["rot", "e", "ap", "s1", "ax", "pl", "s1", "ax", "fp"], kb=["rot", "e", "ap", "s1", "m", "ax", "ax", "fp"])
        RS5 = L([("rot", r"\V{\rot}="), ("e", SM1), ("ap", "("), ("s1", "2s"), ("m", "-"), ("al", r"2\alpha"), ("q", "s"), ("fp", ")")], 1120, 790, 34)
        self.gat("que é a distância ao quadrado de novo")
        gm(self, RS4, RS5, rt=0.8, extra=[pisca_cor(PQ.p("s", "s2"), AMB, 0.8)])
        RS6 = L([("rot", r"\V{\rot}="), ("fr", r"\V{\dfrac{2-2\alpha}{s^{\alpha}}}")], 1120, 790, 36)
        self.gat("sobra uma fórmula curtinha")
        gm(self, RS5, RS6, rt=0.9, ka=["rot", "fr", "fr", "fr", "fr", "fr", "fr", "fr"])
        RS7 = L([("rot", r"\V{\rot}="), ("fr", r"\V{\dfrac{2-2\alpha}{(\X^2+\Y^2)^{\alpha}}}")], 1120, 790, 36)
        gm(self, RS6, RS7, rt=0.8)
        # o divergente (alvo v2_d3r3): as linhas de ∂Q/∂x e ∂P/∂y fundem-se no rot final, que sobe
        RT = L([("rot", r"\V{\rot}="), ("fr", r"\V{\dfrac{2-2\alpha}{(\X^2+\Y^2)^{\alpha}}}")], 1120, 395, 36)
        self.gat("e o divergente")
        AT = Duas(R0, PQ, F2, F3, RS7)
        AT.ks = ["x"] * (len(R0.ks) + len(PQ.ks) + len(F2.ks) + len(F3.ks)) + ["rot", "fr"]
        gm(self, AT, RT, rt=1.0, nota="(fusão)")
        self.remove(R0, PQ, F2, F3, RS7)
        limpa_soltos(self)
        DV = L([("div", r"\D{\dv}="), ("dPx", r"\dfrac{\partial\Pp}{\dx}"), ("pl", "+"), ("dQy", r"\dfrac{\partial\Qq}{\dy}")], 1120, 505, 36)
        self.gat("agora é a soma")
        escreve(self, DV, 0.35)
        DP = L([("dPx", r"\dfrac{\partial\Pp}{\dx}="), ("my", r"-\Y"), ("c", r"\big(-\alpha s^{-\alpha-1}\cdot2\X\big)"), ("r", r"=2\alpha\X\Y\,s^{-\alpha-1}")], 1120, 605, 32)
        self.gat("só a regra da cadeia trabalha")
        escreve_p(self, DP, ["dPx", "my", "c"], 0.3)
        self.gat("e sai o mesmo termo")
        escreve_p(self, DP, ["r"], 0.3)
        junta(self, DP)
        DQ = L([("dPx", r"\dfrac{\partial\Qq}{\dy}="), ("my", r"\X"), ("c", r"\big(-\alpha s^{-\alpha-1}\cdot2\Y\big)"), ("r", r"=-2\alpha\X\Y\,s^{-\alpha-1}")], 1120, 700, 32)
        gm(self, DP, DQ, rt=0.8, copia=True)
        DS = L([("div", r"\D{\dv}="), ("t1", r"2\alpha\X\Y\,s^{-\alpha-1}"), ("t2", r"-2\alpha\X\Y\,s^{-\alpha-1}")], 1120, 800, 34)
        self.gat("uma vez com sinal de mais")
        gm(self, DV, DS, rt=0.9, copia=True, voos={"t1": DP.p("r")[1:], "t2": DQ.p("r")[1:]})
        self.gat("eles se cancelam zero")
        tr = cancela(self, DS, "t1", "t2")
        DZ = L([("div", r"\D{\dv}="), ("z", r"\D0")], 1120, 800, 34)
        gm(self, DS, DZ, rt=0.7, somem=tr)
        self.gat("nenhum desses redemoinhos")
        ped = quad30(VA, C0, S0)
        st = {"ped": ped, "giro": None}
        clareira(cmp, lambda: ou(clar_ped(st["ped"], .2), dq(C0, S0), clarPoly(circ_pts(.75, st["giro"]._giro[0], 12), .1) if st["giro"] else None))
        self.play(FadeIn(ped), run_time=0.3)
        self.play(anda(ped, flV(.5), T_FL(.5), 2.0, rate=linear, nome="D3 α = ½ (div)"))
        print(f"[D3] α = ½: área {S0 * S0:.3f} → {ped.area():.4f}")
        self.ate(1.0)

        # ── D3-4 · lendo a fórmula (alvo 09 v1 no α = ½) ──
        self.an("D3-4")
        RL = L([("rot", r"\V{\rot\vv}="), ("fr", r"\V{\dfrac{2-2\alpha}{(\X^2+\Y^2)^{\alpha}}}")], 1120, 600, 40)
        DL0 = L([("div", r"\D{\dv}\vv="), ("z", r"\D0")], 1120, 780, 40)
        self.gat("agora lê a fórmula")
        AD = Duas(DV, DP, DQ, DZ)
        AD.ks = ["x"] * (len(DV.ks) + len(DP.ks) + len(DQ.ks)) + ["div", "z"]
        fa2 = L([("a", r"\alpha="), ("0", r"0\quad"), ("m", r"\tfrac12\quad"), ("1", r"1\quad"), ("2", "2")], 1120, 400, 38)
        grp = lambda a: fa2.pi(IDX_A[a])
        fa2._origem = "a"
        print(f"[origem] a {self.lote} D3-4 {self.t:.2f} {fa2._tex!r}")
        em_paralelo(self, 0.8, lambda: gm(self, AD, DL0, nota="(fusão)"), lambda: gm(self, RT, RL), extra=[FadeOut(ped), caneta(fa2, ritmo=0.12)])
        self.remove(DV, DP, DQ, DZ, ped)
        limpa_soltos(self)
        st["ped"] = quad30(VA, C0, S0)
        cx = caixa_em(grp(1 if False else 0), pad=10)
        est["sub"] = None

        def le(a, ccw, legenda_txt, fr_solta=None):
            sai = [m for m in (st["ped"], st["giro"], st.get("lg")) if m is not None]
            st["giro"], st["lg"] = None, None
            ped = quad30(VA, C0, S0)
            self.play(*[FadeOut(m) for m in sai], FadeIn(ped), troca_p(cmp, a, 1.0), cx.animate.become(caixa_em(grp(a), pad=10)) if cx in self.mobjects else Create(cx), run_time=1.0)
            self.remove(*sai)
            st["ped"] = ped
            nova = L(SUB(a), 1150, 690, 36)
            if est["sub"] is None:
                gm(self, RL, nova, rt=0.8, copia=True, voos={"a": grp(a)})
            else:
                gm(self, est["sub"], nova, rt=0.7, voos={"a": grp(a)})
            est["sub"] = nova
            if fr_solta:
                self.gat(fr_solta)
            T_ = T_FL(a)
            self.play(anda(ped, flV(a), T_, 2.0, rate=linear, nome=f"D3 α = {a}"))
            c1 = ponto_fl(flV(a), C0, T_)
            print(f"[D3] α = {a}: t = {T_:.4f}, centro girou {math.atan2(c1[1], c1[0]):.4f} rad; área {S0 * S0:.3f} → {ped.area():.4f}")
            ans = []
            if ccw is not None:
                st["giro"] = giro30(VA, c1, .68, ccw)
                ans.append(Create(st["giro"]))
            if legenda_txt:
                st["lg"] = legenda(legenda_txt, 1124, 850, GEO, "left", 26)
                ans.append(FadeIn(st["lg"], shift=0.05 * UP))
            if ans:
                self.play(*ans, run_time=0.4)

        self.gat("alfa zero dois menos zero")
        le(0, True, "O DISCO GIRANDO RÍGIDO")
        self.gat("alfa meio dois menos um")
        le(.5, True, "SETAS DO MESMO TAMANHO, E O QUADRADINHO GIRA")
        self.gat("e mesmo assim o rotacional")                  # R16: a linha do rotacional citada acende
        acende(self, [est["sub"]], VIO, 1.0)
        self.gat("alfa um dois menos dois")
        le(1, None, "DÃO A VOLTA, E O QUADRADINHO NÃO GIRA")
        self.ate(1.0)

        # ── D3-5 · α = 2: gira no sentido horário ──
        self.an("D3-5")
        self.gat("e alfa dois")
        le(2, False, "VOLTA ANTI-HORÁRIA, GIRO HORÁRIO", fr_solta="e o quadradinho gira no sentido horário")
        a_ = math.atan2(*ponto_fl(flV(2), C0, T_FL(2))[::-1])
        u_ = np.array([math.cos(a_), math.sin(a_)])
        t_ = np.array([-u_[1], u_[0]])
        dest = []
        for r, Lr in ((1.75 - .35 - .2, .62), (1.75 + .35 + .2, .62 * ((1.75 + .55) / (1.75 - .55)) ** -1.8)):
            p = u_ * r
            dest.append(seta7(VA.c2p(*(p - t_ * Lr / 2)), VA.c2p(*(p + t_ * Lr / 2)), CAMPO2, 7, 22).set_z_index(12))
        self.gat("olha por quê")
        self.play(*[GrowArrow(d) for d in dest], run_time=0.5)
        self.wait(2.5)
        self.play(*[FadeOut(d) for d in dest], run_time=0.4)
        self.remove(*dest)
        zera_chapas()
        cards = [cartao_alpha(0, 0, True), cartao_alpha(1, 1, None), cartao_alpha(2, 2, False)]
        tits = [leg_mix([r"$\alpha=0$", " · GIRA ", r"$\circlearrowleft$"], 360, 835, BR, "center", 32, bold=True),
                leg_mix([r"$\alpha=1$", " · NÃO GIRA"], 960, 835, BR, "center", 32, bold=True),
                leg_mix([r"$\alpha=2$", " · GIRA ", r"$\circlearrowright$"], 1560, 835, BR, "center", 32, bold=True)]
        rots = [L([("r", r"\rot = \V{2}")], 360, 895, 34, "c"), L([("r", r"\rot = \V{0}")], 960, 895, 34, "c"), L([("r", r"\rot = \V{-\dfrac{2}{r^4}}")], 1560, 895, 34, "c")]
        lgc = legenda("TODAS AS SETAS DÃO A VOLTA NO SENTIDO ANTI-HORÁRIO", 960, 968, GEO, "center", 28)
        cmp.clear_updaters()
        self.gat("o sentido da volta não é")
        self.limpa_junto()
        troca(self, "D3 palco → cartões α = 0/1/2")
        for r_, srcs in zip(rots, ("2", "0", "-2/r^4")):
            r_._origem = "b"
        self.play(*[FadeIn(c) for c in cards], *[FadeIn(t) for t in tits], *[TransformFromCopy(est["sub"].p("res"), r_) for r_ in rots], FadeIn(lgc), run_time=0.8)
        self.ate(1.0)

        # ── D3-6 · na origem (alvo 11 v1) ──
        self.an("D3-6")
        self.secao("A FAMÍLIA DE REDEMOINHOS · NA ORIGEM")
        zera_chapas()
        orig = []
        for k, (a, mref) in enumerate(((.25, 2), (.5, 1), (1, 1))):
            X0 = CC[k][0]
            v = VB(CC[k], X0 + 240, 540, 56)
            ch = chapa_px(*CC[k], nome=f"D3 origem α = {a}", v=v)
            cp = campoP30(v, VORTA(a), -3.5, 3.5, -3.5, 3.5, .75, rmin=.3, mref=mref, nome=f"D3 origem α = {a}")
            pt = ponto7(v.c2p(0, 0), CAMPO2, 9, 9) if a == .25 else anel7(v.c2p(0, 0), GEO, 9, 3)
            orig.append(VGroup(ch, cp, pt))
        t1 = [rotulo_tex(r"0<\alpha<\tfrac12", 360, 830, 32), rotulo_tex(r"\alpha=\tfrac12", 960, 830, 32), rotulo_tex(r"\alpha=1", 1560, 830, 32)]
        for m in t1:
            m._origem = "legenda"
        t2 = [legenda(s, x, 875, GEO, "center", 26) for s, x in (("A SETA VAI A ZERO", 360), ("TAMANHO 1, DIREÇÃO MUDA", 960), ("A SETA EXPLODE", 1560))]
        t3 = [T("CONTÍNUO SE v(0) = 0", 360, 920, 28, "center", CAMPO2, up=False), T("SEM LIMITE", 960, 920, 28, "center", CORAL),
              T("SEM LIMITE", 1560, 920, 28, "center", CORAL)]
        a0 = leg_mix([r"$\alpha=0$", " NÃO DIVIDE POR NADA: JÁ É CONTÍNUO NA ORIGEM"], 960, 985, GEO, "center", 26)
        self.limpa_junto()
        troca(self, "D3 cartões α → cartões da origem")
        self.play(*[FadeIn(g) for g in orig], run_time=0.8)
        self.gat("com alfa zero não tem divisão")
        self.play(FadeIn(a0, shift=0.05 * UP), run_time=0.4)
        rz = L([("n", r"\|\vv\|=r^{\,1-2\alpha}"), ("t", r"\ \to\ 0\ \ \text{se}\ \alpha<1/2")], 960, 245, 34, "c")
        for k, (f1_, f2_) in enumerate((("com alfa entre zero e meio", "o campo fica contínuo"), ("com alfa meio a rapidez", "não tem limite"),
                                        ("com alfa maior que meio", "a seta explode"))):
            self.gat(f1_)
            self.play(FadeIn(t1[k], shift=0.05 * UP), FadeIn(t2[k], shift=0.05 * UP), run_time=0.4)
            if k == 0:
                self.gat("a rapidez vai a zero")
                escreve(self, rz, 0.3)
            self.gat(f2_)
            self.play(FadeIn(t3[k], shift=0.05 * UP), run_time=0.4)
        self.ate(1.0)

        # ── D3-7 · giro de 90° (alvo v2_d3g) ──
        self.an("D3-7")
        self.secao("A FAMÍLIA DE REDEMOINHOS · GIRO DE 90°")
        zera_chapas()
        vl, vr = VB(BE, 480, 540, 140), VB(BD, 1440, 540, 140)
        pe, pd = chapa_px(*BE, nome="D3 giro esq.", v=vl), chapa_px(*BD, nome="D3 giro dir.", v=vr)
        ce = campo30(vl, VORTA(1), -2.25, 2.25, -1.75, 2.25, .5, rmin=.45, mmax=2, nome="D3 redemoinho α = 1")
        cd = campo30(vr, VORTA(1), -2.25, 2.25, -1.75, 2.25, .5, rmin=.45, mmax=2, nome="D3 cópia (vai girar)")
        ok = {s._xy for s in campo30(vr, EXPLA(1), -2.25, 2.25, -1.75, 2.25, .5, rmin=.45, mmax=2, nome="D3 explosão (só p/ R7)")}
        for s in [s for s in cd if s._xy not in ok]:
            cd.remove(s)
        oe, od = ponto7(vl.c2p(0, 0), GEO, 6, 8), ponto7(vr.c2p(0, 0), GEO, 6, 8)
        n1 = legenda("REDEMOINHO", 480, 868, GEO, "center", 28)
        n2 = leg_mix(["CADA SETA GIRADA 90° ", r"$\circlearrowright$"], 1440, 868, GEO, "center", 28)
        VPQ = L([("v", r"\vv="), ("p", "("), ("P", r"\Pp"), ("vg", r",\ "), ("Q", r"\Qq"), ("fp", ")"), ("eq", "="), ("fr", r"\dfrac{(-\Y,\ \X)}{s^{\alpha}}")], 480, 955, 34, "c")
        self.limpa_junto()
        troca(self, "D3 cartões → layout B (giro de 90°)")
        self.play(FadeIn(pe), FadeIn(pd), cresce_campo(ce, 0.3), FadeIn(oe), FadeIn(n1), run_time=0.3)
        self.gat("gira cada seta noventa graus")
        escreve(self, VPQ, 0.25, extra=[FadeIn(cd), FadeIn(od)])
        self.play(gira_setas(cd, -PI / 2, 1.2), FadeIn(n2), run_time=1.2)
        WQP = L([("w", r"\ww="), ("p", "("), ("Q", r"\Qq"), ("vg", r",\ "), ("mP", r"-\Pp"), ("fp", ")"), ("eq", "="), ("fr", r"\dfrac{(\X,\ \Y)}{s^{\alpha}}")], 1440, 955, 34, "c")
        self.gat("a componente horizontal nova")
        gm(self, VPQ, WQP, rt=1.0, copia=True, voos={"Q": VPQ.p("Q"), "mP": VPQ.p("P")})
        DW = L([("dw", r"\D{\dv\ww}="), ("dq", r"\dfrac{\partial\Qq}{\dx}-\dfrac{\partial\Pp}{\dy}"), ("rv", r"=\V{\rot\vv}"), ("fr", r"=\dfrac{2-2\alpha}{s^{\alpha}}")], 960, 1035, 30, "c")
        self.gat("então o divergente novo")
        escreve_p(self, DW, ["dw", "dq"], 0.3)
        self.gat("exatamente a conta do rotacional antigo")
        escreve_p(self, DW, ["rv", "fr"], 0.3)
        junta(self, DW)
        DW2 = L([("dw", r"\D{\dv\ww}="), ("dq", r"\dfrac{\partial\Qq}{\dx}-\dfrac{\partial\Pp}{\dy}"), ("rv", r"=\V{\rot\vv}"), ("fr", r"=\dfrac{2-2\alpha}{s^{\alpha}}"),
                  ("rw", r",\quad \V{\rot\ww}=0")], 960, 1035, 30, "c")
        self.gat("o rotacional vira zero")
        gm(self, DW, DW2, rt=0.7)
        self.sai_fim()


def _split(lin, i, ns):
    """Divide a faixa de glifos da peça i de `lin` em sub-faixas de tamanhos ns (para mapear partes de uma peça)."""
    r = lin._rg[i]
    out, k = [], 0
    for n in ns:
        out.append(r[k:k + n])
        k += n
    if k != len(r):
        out[-1] = r[k - ns[-1]:]
    return out

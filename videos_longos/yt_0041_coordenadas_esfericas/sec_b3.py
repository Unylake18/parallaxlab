"""yt_0041 · B3 · o teorema, metade por metade (B3-1, alvo 10) e a receita com a sonda radial (B3-2, sem alvo).
B3-1: em cima as peças 3D lisas (a caixa e a bola com a célula), a seta T; embaixo o painel opaco do enunciado sobre o papel de borda a borda,
escrito item a item; glyph map 9 para o caso esférico (o lima voa do chip dV, miniatura do B2-3); a costura acende; a caixa se parte em θ = π
(as metades se afastam 0,15 e voltam: o único afastamento do vídeo); O CORTE: VOLUME ZERO. B3-2: a bola em traço com a região genérica, os selos
①②③ na coluna, a sonda (entra azul-claro, sai coral) e o cartão θ E φ FORA: NÚMEROS · r DENTRO: DA SONDA."""
from k41 import *
from sec_b1 import depois


def numero(n, X, Y, cor=GEO, r=20):
    """Selo numerado (círculo fino + algarismo), no lugar do ① ② ③ (o Space Grotesk não tem os círculos)."""
    c = circ_px(X, Y, r, cor, 2)
    t = T(str(n), X, Y + 9, 26, "center", cor)
    return c, t


class PB3(B41):
    ANTES = "O TESTE: A BOLA"

    def corpo(self):
        # ── B3-1 ──────────────────────────────────────────────────────────────────────────────────────────
        self.an("B3-1")
        cx = self.palco("caixa", cam_alvo("b31a"), bordas=0.0, celula=0.0, meia=0.0, sep=0.0, corte=0.0)
        bg = self.palco("bolagrade", cam_alvo("b31b"), bordas=2.0, celula=1.0)
        self.add(cx.fundo, bg.fundo)
        self.grade = papel(passo=0.5).set_z_index(-10)        # o papel de borda a borda fica atrás do painel (as peças 3D por cima, lisas)
        self.add(self.grade)
        seta = seta_px((760, 360), (920, 360), BR, 4, 18)
        tT = TC("T", 840, 320, 32, "c")
        self.titulo("O TEOREMA", rt=0.3)
        self.play(Create(seta), run_time=0.4)
        self.pena(tT)
        pn = painel41(60, 650, 1800, 300)
        self.gat("do jeito do Guidorizzi")
        self.play(Create(pn), run_time=0.5)
        l1 = mixl([("m", r"T:\Omega\subset\mathbb{R}^3\to\mathbb{R}^3"), ("t", "DE CLASSE", GEO), ("m", r"C^1"), ("t", "·", GEO), ("m", r"B_{uvw}"),
                   ("t", "COMPACTO, FRONTEIRA DE CONTEÚDO NULO", GEO)], 100, 710, 40)
        self.gat("qualquer transformação T")
        self.pena(l1.p[0])
        self.gat("de classe C um")
        self.pena(*l1.p[1:3], lag=0.1)
        self.gat("a região B U V W é compacta")
        self.pena(*l1.p[3:5], lag=0.1)
        self.gat("com fronteira de conteúdo nulo")
        self.pena(l1.p[5])
        self.degrau("C7b", "T: Ω ⊂ ℝ³ → ℝ³ de classe C¹; B_uvw compacto, fronteira de conteúdo nulo")
        self.gat("três coisas")
        l2 = mixl([("t", "NO INTERIOR:", BR), ("m", r"T(\mathring B_{uvw})=\mathring B"), ("t", "·  T INJETORA  ·", BR),
                   ("m", r"\dfrac{\partial(\X,\Y,\Z)}{\partial(u,v,w)}\neq 0")], 100, 805, 40)
        self.pena(l2.p[0])
        self.gat("T leva o interior")
        self.pena(l2.p[1])
        self.gat("T é injetora")
        self.pena(l2.p[2])
        self.gat("e o jacobiano não se anula")
        self.pena(l2.p[3])
        self.degrau("C7b", "no interior: T(B̊_uvw) = B̊ · T injetora · ∂(x,y,z)/∂(u,v,w) ≠ 0")
        self.gat("aí a integral tripla")
        G = L([("i", r"\iiint_B"), ("f", r"f(\X,\Y,\Z)"), ("d", r"\,\dX\,\dY\,\dZ"), ("eq", "="), ("i2", r"\iiint_{B_{uvw}}"), ("ft", r"f\big(T(u,v,w)\big)"),
               ("j", r"\left|\dfrac{\partial(\X,\Y,\Z)}{\partial(u,v,w)}\right|"), ("dd", r"du\,dv\,dw")], 100, 910, 38)
        self.pena(parte(G, sel(G, ["i", "f", "d", "eq"]), "∭_B f dx dy dz ="))
        self.gat("vira a integral em u v w")
        self.pena(parte(G, sel(G, ["i2", "ft"]), "∭ f(T(u,v,w))"))
        self.gat("com o módulo do jacobiano")
        self.pena(parte(G, sel(G, ["j", "dd"]), "|∂/∂| du dv dw"))
        self.degrau("C7b", "∭_B f dx dy dz = ∭_{B_uvw} f(T(u,v,w)) |∂(x,y,z)/∂(u,v,w)| du dv dw")
        self.dentro((60, 610, 1860, 1030), l1, l2, G)

        self.gat("nas esféricas")
        # o painel cresce para caber a linha do caso esférico (sem sair da tela)
        pn2 = painel41(60, 610, 1800, 420)
        self.play(Transform(pn, pn2), VGroup(l1, l2, G).animate.shift(UP * 40 / 120), run_time=0.6)
        cg, cf, cm_ = chip(r"dV=\J\;\dR\,\dF\,\dT", 1480, 910 - 40, 34, MEN)
        self.chip_pena(cg, cf, cm_)                 # a miniatura do chip dV do B2-3
        S_ = L([("i", r"\iiint_B"), ("f", r"f(\X,\Y,\Z)"), ("d", r"\,\dX\,\dY\,\dZ"), ("eq", "="), ("i2", r"\iiint_{B_{\R\F\T}}"),
                ("ft", r"f\big(T(\R,\F,\T)\big)"), ("j", r"\J"), ("dd", r"\,\dR\,\dF\,\dT")], 100, 985, 38)
        i2a, i2b = sel(G, "i2"), sel(S_, "i2")         # ∭, B, u, v, w → ∭, B, r, φ, θ
        fa, fb = sel(G, "ft"), sel(S_, "ft")           # f ( T ( u , v , w ) )
        da, db = sel(G, "dd"), sel(S_, "dd")           # d u d v d w
        self.gm(9, G, S_, [("i", "i"), ("f", "f"), ("d", "d"), ("eq", "eq"), (i2a, i2b), (fa, fb), (da, db)], voos=[(VGroup(*cf[0][3:9]), "j")], copia=True,
                nota="∭_{B_uvw} f(T(u,v,w)) |∂/∂| du dv dw → ∭_{B_rφθ} f(T(r,φ,θ)) r² sen φ dr dφ dθ")
        self.degrau("C7b", "caso esférico: ∭_{B_rφθ} f(T(r,φ,θ)) r² sen φ dr dφ dθ")
        self.sai(cg, rt=0.4)
        self.dentro((60, 610, 1860, 1030), S_)

        self.gat("tem um problema")
        bg.set(bordas=3.0)                                      # a costura acende em ALERTA na bola
        self.gat("a página téta igual a zero")
        self.wait(0.1)
        self.gat("em duas metades")
        cx.set(meia=1.0, bordas=3.0, corte=1.0)
        m1 = leg("METADE  θ ≤ π", 110, 590, AZC, "left", 28)
        m2 = leg("METADE  θ ≥ π", 430, 590, CORAL, "left", 28)
        self.play(cx.tr["sep"].animate(rate_func=there_and_back).set_value(0.15), run_time=1.6)     # as metades se afastam e voltam
        self.pena(m1, m2, lag=0.3)
        self.gat("volume zero")
        vz = leg("O CORTE: VOLUME ZERO", 1380, 420, AL, "left", 28)
        self.pena(vz)
        self.marca("10_B3-1")

        # ── B3-2 ──────────────────────────────────────────────────────────────────────────────────────────
        self.an("B3-2")
        saem = [m for m in self.mobjects if m not in self.fixos() and not isinstance(m, ValueTracker) and m is not self.clk and m is not self.grade]
        rc = self.palco("receita", cam_alvo("b32"), sonda=0.0)
        rc.fundo.op.set_value(0.0)
        self.add(rc.fundo)
        self.titulo("A RECEITA")
        # corte seco depois do B3-1 (sem dissolve sobre a caixa): o 3D da receita entra no lugar, o papel fica
        self.remove(*saem)
        for m in saem:
            m.clear_updaters()
        rc.fundo.op.set_value(1.0)
        rzr = self.rot3(rc, "ez", r"\Z", dx=14, size=36)
        self.pena(rzr)
        sel_ = []
        textos = [[("m", r"\T"), ("t", ": QUANTO GIRA EM VOLTA DE", BR), ("m", r"\Z")], [("m", r"\F"), ("t", ": DE QUE CONE A QUE CONE", BR)],
                  [("m", r"\R"), ("t", ": A SONDA SAI DA ORIGEM", BR)]]
        cores = [TH, FI, RO]
        for k, (fr, tx) in enumerate(zip(["téta de que ângulo", "fi de que cone", "e r para cada direção"], textos)):
            self.gat(fr)
            c, t = numero(k + 1, 1035, 250 + 110 * k, cores[k], 24)
            ln = mixl(tx, 1075, 250 + 110 * k, 44)
            self.play(Create(c), run_time=0.3)
            self.pena(t, *ln.p, lag=0.1)
            sel_ += [c, t, ln]
        self.gat("solta uma sonda")
        self.play(rc.tr["sonda"].animate(rate_func=linear).set_value(0.35), run_time=0.8)
        self.gat("onde ela entra")
        self.play(rc.tr["sonda"].animate(rate_func=linear).set_value(0.5 / 1.3 + 0.01), run_time=0.5)
        le = self.rot3(rc, "entra", "ENTRA", dx=-105, dy=35, size=30, txtp=True, cor=AZC)
        self.pena(le)
        self.add(self.fio(rc, "entra", le))
        lbx = leg("ENTRA NA REGIÃO: LIMITE DE BAIXO", 1075, 550, AZC, "left", 30)
        self.pena(lbx)
        self.gat("onde ela sai")
        self.play(rc.tr["sonda"].animate(rate_func=linear).set_value(1.0 / 1.3 + 0.01), run_time=0.7)
        ls = self.rot3(rc, "sai", "SAI", dx=62, dy=-39, size=30, txtp=True, cor=CORAL)
        self.pena(ls)
        self.add(self.fio(rc, "sai", ls))
        lcx = leg("SAI DA REGIÃO: LIMITE DE CIMA", 1075, 600, CORAL, "left", 30)
        self.pena(lcx)
        self.play(rc.tr["sonda"].animate(rate_func=linear).set_value(1.0), run_time=0.5)
        self.gat("é por isso")
        pc = painel41(1020, 700, 840, 200)
        c1 = mixl([("m", r"\T"), ("t", "E", GEO), ("m", r"\F"), ("t", "FORA: NÚMEROS", BR)], 1050, 775, 44)
        c2 = mixl([("m", r"\R"), ("t", "DENTRO: DA SONDA", BR)], 1050, 855, 44)
        self.play(Create(pc), run_time=0.4)
        self.pena(*c1.p, *c2.p, lag=0.08)
        self.dentro((1020, 700, 1860, 900), c1, c2)
        self.col("B3-2", *[x for x in sel_ if isinstance(x, VGroup) and hasattr(x, "p")], c1, c2)
        self.marca("B3-2", agora=True)
        self.sai_fim()

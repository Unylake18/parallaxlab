"""Lote PD3 · D3 A FAMÍLIA DE REDEMOINHOS (alvos 09, 10, 11, 12). Palco A com v_α = (−y, x)/(x² + y²)^α numa rede viva (α só muda durante as
trocas); a linha α = 0 ½ 1 2 com a caixa no valor atual; ‖v‖ = r^{1−2α}; a conta do rotacional e do divergente em caneta (as linhas antigas sobem e
somem; os termos com α se juntam por TransformByGlyphMap). Lendo a fórmula: α = 0, ½, 1, 2 (troca 1 s, quadradinho solto 2 s, seta curva ↺/—/↻);
no α = 2, as setas de dentro e de fora em destaque. Cartões α = 0/1/2 (alvo 10); na origem (alvo 11); giro de 90° (layout B, alvo 12)."""
from lib30 import *  # noqa: F401,F403

C0, S0 = (1.75, 0.0), 0.7
PTS = [(X, Y) for X in np.arange(-3.5, 3.5 + 1e-6, .5) for Y in np.arange(-2.5, 2.5 + 1e-6, .5) if math.hypot(X, Y) >= .3]
MM = interp_tab([(0, 3.0), (.5, 1.0), (1, 1.2), (2, 1.2)])
T_FL = lambda a, c=C0: .35 * math.hypot(*c) ** (2 * a)
CAUDAS = {0: (r"=r", r"=\V{2}"), .5: (r"=1", r"=\V{\dfrac1r}"), 1: (r"=\dfrac1r", r"=\V{0}"), 2: (r"=\dfrac{1}{r^3}", r"=\V{-\dfrac{2}{r^4}}")}
IDX_A = {0: 1, .5: 2, 1: 3, 2: 4}


def cauda(tex, ref, y, size):
    m = TC(tex, 1120, y, size)
    m.shift(RIGHT * (ref.get_right()[0] + 14 / 120 - m.get_left()[0]))
    return m


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


class LoteD3(Base):
    ANTES = "DESENHAR SEM MIL SETAS"

    def corpo(self):
        # ── D3-1 · enunciado ──
        self.an("D3-1")
        self.secao("A FAMÍLIA DE REDEMOINHOS")
        zera_chapas()
        chA = chapa_px(*LA, nome="D3 palco A", v=VA)
        cmp = CampoVivo(VA, PTS, VORTA, MM, .5, p0=0.0, nome="D3 v_α")
        troca(self, "D2 → D3 (palco)")
        self.play(FadeIn(chA), cresce_campo(cmp, 1.0), run_time=1.0)
        fv = TC(r"\vv=\dfrac{(-\Y,\ \X)}{(\X^2+\Y^2)^{\alpha}}", 1120, 300, 46)
        self.gat("menos a coordenada vertical")
        self.play(caneta(fv, ritmo=0.4))
        fa = Pz([r"\alpha=", r"0\quad", r"\tfrac12\quad", r"1\quad", "2"], 1120, 415, 38)
        grp = lambda a: VGroup(*[fa[0][i] for i in fa._rg[IDX_A[a]]])
        cx = caixa_em(grp(0))
        self.gat("cada valor do expoente alfa")
        self.play(caneta(fa, ritmo=0.4))
        self.play(Create(cx), run_time=0.4)
        self.gat("pausa o vídeo e tenta")
        self.pausa()
        self.ate(1.0)

        # ── D3-2 · α correndo; a rapidez ──
        self.an("D3-2")
        fn = TC(r"\|\vv\| = r^{\,1-2\alpha}", 1120, 505, 40)
        self.gat("a rapidez é a distância")
        self.play(caneta(fn, ritmo=0.4))
        est = {"cn": None, "a": 0}

        def poe_cauda(a, extra=(), rt=1.5):
            novo = cauda(CAUDAS[a][0], fn, 505, 40)
            ans = [troca_p(cmp, a, rt), cx.animate.become(caixa_em(grp(a)))] if a != est["a"] else []
            if est["cn"] is not None:
                ans.append(FadeOut(est["cn"], run_time=0.3))
            self.play(*ans, *extra, caneta(novo, ritmo=0.3, atraso=max(0.0, rt - 0.6) if ans else 0.0), run_time=max(rt, 0.8))
            if est["cn"] is not None:
                self.remove(est["cn"])
            est["cn"], est["a"] = novo, a
            print(f"[D3] α = {a}: mmax {MM(a):.2f}")
        self.gat("com alfa zero a rapidez")
        poe_cauda(0)
        self.gat("com alfa meio a rapidez")
        poe_cauda(.5)
        self.gat("com alfa um ela cai")
        poe_cauda(1)
        self.ate(1.0)

        # ── D3-3 · a conta do rotacional e do divergente (na coluna) ──
        self.an("D3-3")
        sd = TC(r"s=\X^2+\Y^2", 1120, 590, 34)
        self.gat("agora a conta do rotacional")
        self.play(FadeOut(est["cn"]), caneta(sd, ritmo=0.3), run_time=1.0)
        self.remove(est["cn"])
        est["cn"] = None
        L1 = TC(r"\dfrac{\partial\Qq}{\dx}=s^{-\alpha}-\alpha\,s^{-\alpha-1}\cdot 2\X\cdot\X", 1120, 670, 38)
        self.gat("regra do produto")
        self.play(caneta(L1, ritmo=0.45))
        L2 = TC(r"=s^{-\alpha-1}\,(s-2\alpha\X^2)", 1120, 750, 38)
        L2.shift(RIGHT * (L1[0][4].get_left()[0] - L2[0][0].get_left()[0]))          # alinhado pelo "=" de cima
        self.gat("põe a potência com um a menos")
        self.play(caneta(L2, ritmo=0.4))
        L3 = TC(r"\dfrac{\partial\Pp}{\dy}=-s^{-\alpha-1}\,(s-2\alpha\Y^2)", 1120, 830, 38)
        self.gat("a outra derivada é igualzinha")
        self.play(caneta(L3, ritmo=0.4))
        # as linhas antigas sobem e somem (R3): sai a 1ª, as outras sobem 80 px
        L4a = Pz([r"\V{\rot}", "=", r"s^{-\alpha-1}", "(", "2s", "-", r"2\alpha", r"\X^2", "-", r"2\alpha", r"\Y^2", ")"], 1120, 830, 38)
        L4b = Pz([r"\V{\rot}", "=", r"s^{-\alpha-1}", "(", "2s", "-", r"2\alpha", "(", r"\X^2", "+", r"\Y^2", ")", ")"], 1120, 830, 38)
        self.gat("na subtração")
        self.play(FadeOut(L1, shift=0.3 * UP), L2.animate.shift(80 / 120 * UP), L3.animate.shift(80 / 120 * UP), run_time=0.6)
        self.remove(L1)
        self.play(caneta(L4a, ritmo=0.35))
        self.gat("os dois termos com alfa se juntam")
        self.play(tbgm30(L4a, L4b, [(i, i) for i in range(6)] + [([6, 9], 6), (7, 8), (8, 9), (10, 10), (11, 12)], rt=1.3))
        self.remove(L4a)
        limpa_soltos(self)
        self.add(L4b)
        L4c = Pz([r"\V{\rot}", "=", r"\V{\dfrac{2-2\alpha}{s^{\alpha}}}"], 1120, 848, 40)
        self.gat("sobra uma fórmula curtinha")
        self.play(TransformMatchingShapes(L4b, ja_escrita(L4c)), run_time=1.2)
        self.remove(L4b)
        self.add(L4c)
        L5 = TC(r"\D{\dv}=2\alpha\X\Y\,s^{-\alpha-1}-2\alpha\X\Y\,s^{-\alpha-1}=\D{0}", 1120, 750, 36)
        self.gat("e o divergente")
        self.play(FadeOut(L2, shift=0.3 * UP), FadeOut(L3, shift=0.3 * UP), run_time=0.5)
        self.remove(L2, L3)
        self.play(caneta(L5, ritmo=0.35))
        rot0 = TC(r"\rot\vv=\V{\dfrac{2-2\alpha}{(\X^2+\Y^2)^{\alpha}}}", 1120, 625, 42)
        div0 = TC(r"\dv\vv=\D{0}", 1120, 745, 42)
        self.gat("nenhum desses redemoinhos")
        self.play(FadeOut(sd), TransformMatchingShapes(L4c, ja_escrita(rot0)), TransformMatchingShapes(L5, ja_escrita(div0)), run_time=1.2)
        self.remove(sd, L4c, L5)
        self.add(rot0, div0)
        self.ate(1.0)

        # ── D3-4 · lendo a fórmula: α = 0, ½, 1 (alvo 09 = α ½) ──
        self.an("D3-4")
        fan = fantasma(VA, quad_pts(C0, S0))
        st = {"ped": None, "giro": None, "cr": None, "lg": None}
        clareira(cmp, lambda: ou(*(f for f in (clar_ped(st["ped"], .2) if st["ped"] else None, dq(C0, S0),
                                                 clarPoly(circ_pts(.75, st["giro"]._giro[0], 12), .1) if st["giro"] else None) if f)))

        def le(a, ccw, legenda_txt, fr_solta=None):
            sai = [m for m in (st["ped"], st["giro"], st["lg"]) if m is not None]
            st["giro"], st["lg"] = None, None
            ped = quad30(VA, C0, S0)
            nc = cauda(CAUDAS[a][0], fn, 505, 40)
            nr = cauda(CAUDAS[a][1], rot0, 625, 42)
            olds = [m for m in (est["cn"], st["cr"]) if m is not None]
            self.play(*[FadeOut(m) for m in sai + olds], FadeIn(ped), troca_p(cmp, a, 1.0), cx.animate.become(caixa_em(grp(a))),
                      caneta(nc, ritmo=0.3, atraso=0.5), caneta(nr, ritmo=0.3, atraso=0.5), run_time=1.0)
            self.remove(*sai, *olds)
            st["ped"], est["cn"], st["cr"], est["a"] = ped, nc, nr, a
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
                st["lg"] = legenda(legenda_txt, 1124, 830, GEO, "left", 26)
                ans.append(FadeIn(st["lg"], shift=0.05 * UP))
            if ans:
                self.play(*ans, run_time=0.4)

        self.gat("agora lê a fórmula")
        self.play(FadeIn(fan), run_time=0.4)
        self.gat("alfa zero rotacional dois")
        le(0, True, "O DISCO GIRANDO RÍGIDO")
        self.gat("alfa meio")
        le(.5, True, "SETAS DO MESMO TAMANHO, E O QUADRADINHO GIRA")
        self.gat("alfa um dois menos dois")
        le(1, None, "DÃO A VOLTA, E O QUADRADINHO NÃO GIRA")
        self.ate(1.0)

        # ── D3-5 · α = 2: gira no sentido horário ──
        self.an("D3-5")
        self.gat("e alfa dois")
        le(2, False, "AS SETAS DÃO A VOLTA ANTI-HORÁRIA; O QUADRADINHO GIRA HORÁRIO", fr_solta="e o quadradinho gira no sentido horário")
        a_ = .35 * 0 + math.atan2(*ponto_fl(flV(2), C0, T_FL(2))[::-1])
        u_ = np.array([math.cos(a_), math.sin(a_)])
        t_ = np.array([-u_[1], u_[0]])
        dest = []
        for r, L in ((1.75 - .35 - .2, .62), (1.75 + .35 + .2, .62 * ((1.75 + .55) / (1.75 - .55)) ** -1.8)):
            p = u_ * r
            dest.append(seta7(VA.c2p(*(p - t_ * L / 2)), VA.c2p(*(p + t_ * L / 2)), CAMPO2, 7, 22).set_z_index(12))
        self.gat("olha por quê")
        self.play(*[GrowArrow(d) for d in dest], run_time=0.5)
        self.wait(2.5)
        self.play(*[FadeOut(d) for d in dest], run_time=0.4)
        self.remove(*dest)

        # cartões α = 0 / 1 / 2 (alvo 10)
        zera_chapas()
        cards = [cartao_alpha(0, 0, True), cartao_alpha(1, 1, None), cartao_alpha(2, 2, False)]
        tits = [leg_mix([r"$\alpha=0$", " · GIRA ", r"$\circlearrowleft$"], 360, 835, BR, "center", 32, bold=True),
                leg_mix([r"$\alpha=1$", " · NÃO GIRA"], 960, 835, BR, "center", 32, bold=True),
                leg_mix([r"$\alpha=2$", " · GIRA ", r"$\circlearrowright$"], 1560, 835, BR, "center", 32, bold=True)]
        rots = [TC(r"\rot = \V{2}", 360, 895, 34, "c", caneta=False), TC(r"\rot = \V{0}", 960, 895, 34, "c", caneta=False),
                TC(r"\rot = \V{-\dfrac{2}{r^4}}", 1560, 895, 34, "c", caneta=False)]
        lgc = legenda("TODAS AS SETAS DÃO A VOLTA NO SENTIDO ANTI-HORÁRIO", 960, 968, GEO, "center", 28)
        cmp.clear_updaters()
        self.gat("o sentido da volta não é")
        zera_chapas()
        self.limpa_junto()
        troca(self, "D3 palco → cartões α = 0/1/2")
        self.play(*[FadeIn(c) for c in cards], *[FadeIn(t) for t in tits], *[FadeIn(r) for r in rots], FadeIn(lgc), run_time=0.8)
        self.ate(1.0)

        # ── D3-6 · na origem (alvo 11) ──
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
        t2 = [legenda(s, x, 875, GEO, "center", 26) for s, x in (("A SETA VAI A ZERO", 360), ("TAMANHO 1, DIREÇÃO MUDA", 960), ("A SETA EXPLODE", 1560))]
        t3 = [T("CONTÍNUO SE v(0) = 0", 360, 920, 28, "center", CAMPO2, up=False), T("SEM LIMITE", 960, 920, 28, "center", CORAL),
              T("SEM LIMITE", 1560, 920, 28, "center", CORAL)]
        a0 = leg_mix([r"$\alpha=0$", " NÃO DIVIDE POR NADA: JÁ É CONTÍNUO NA ORIGEM"], 960, 985, GEO, "center", 26)
        self.limpa_junto()
        troca(self, "D3 cartões α → cartões da origem")
        self.play(*[FadeIn(g) for g in orig], run_time=0.8)
        self.gat("com alfa zero não tem divisão")
        self.play(FadeIn(a0, shift=0.05 * UP), run_time=0.4)
        for k, (f1_, f2_) in enumerate((("com alfa entre zero e meio", "o campo fica contínuo"), ("com alfa meio a rapidez", "não tem limite"),
                                        ("com alfa maior que meio", "a seta explode"))):
            self.gat(f1_)
            self.play(FadeIn(t1[k], shift=0.05 * UP), FadeIn(t2[k], shift=0.05 * UP), run_time=0.4)
            self.gat(f2_)
            self.play(FadeIn(t3[k], shift=0.05 * UP), run_time=0.4)
        self.ate(1.0)

        # ── D3-7 · giro de 90° (layout B, alvo 12) ──
        self.an("D3-7")
        self.secao("A FAMÍLIA DE REDEMOINHOS · GIRO DE 90°")
        zera_chapas()
        vl, vr = VB(BE, 480, 540, 140), VB(BD, 1440, 540, 140)
        pe, pd = chapa_px(*BE, nome="D3 giro esq.", v=vl), chapa_px(*BD, nome="D3 giro dir.", v=vr)
        ce = campo30(vl, VORTA(1), -2.25, 2.25, -1.75, 2.25, .5, rmin=.45, mmax=2, nome="D3 redemoinho α = 1")
        cd = campo30(vr, VORTA(1), -2.25, 2.25, -1.75, 2.25, .5, rmin=.45, mmax=2, nome="D3 cópia (vai girar)")
        ok = {s._xy for s in campo30(vr, EXPLA(1), -2.25, 2.25, -1.75, 2.25, .5, rmin=.45, mmax=2, nome="D3 explosão (só p/ R7)")}
        for s in [s for s in cd if s._xy not in ok]:
            cd.remove(s)                                  # a seta tem de caber na chapa antes E depois de girar 90°
        oe, od = ponto7(vl.c2p(0, 0), GEO, 6, 8), ponto7(vr.c2p(0, 0), GEO, 6, 8)
        n1 = legenda("REDEMOINHO", 480, 868, GEO, "center", 28)
        n2 = leg_mix(["CADA SETA GIRADA 90° ", r"$\circlearrowright$"], 1440, 868, GEO, "center", 28)
        FE = [r"\rot", r"\vv", "=", r"\V{\dfrac{2-2\alpha}{(\X^2+\Y^2)^{\alpha}}}", r",\ \ ", r"\dv", r"\vv", "=", r"\D0"]
        FD = [r"\dv", r"\ww", "=", r"\D{\dfrac{2-2\alpha}{(\X^2+\Y^2)^{\alpha}}}", r",\ \ ", r"\rot", r"\ww", "=", r"\V0"]
        fe = Pz(FE, 480, 965, 34, "c")
        fc = Pz(FE, 1440, 965, 34, "c", caneta=False)
        fd = Pz(FD, 1440, 965, 34, "c", caneta=False)
        self.limpa_junto()
        troca(self, "D3 cartões → layout B (giro de 90°)")
        self.play(FadeIn(pe), FadeIn(pd), cresce_campo(ce, 0.8), FadeIn(oe), FadeIn(n1), caneta(fe, ritmo=0.12, atraso=0.3), run_time=1.0)
        self.gat("gira cada seta noventa graus")
        self.play(FadeIn(cd), FadeIn(od), TransformFromCopy(fe, ja_escrita(fc)), run_time=0.6)        # o painel direito começa como cópia
        self.play(gira_setas(cd, -PI / 2, 1.2), FadeIn(n2), run_time=1.2)
        self.gat("os papéis se trocam")
        self.play(tbgm30(fc, fd, [(0, 5), (1, 6), (2, 7), (3, 3), (4, 4), (5, 0), (6, 1), (7, 2), (8, 8)], rt=1.4))
        self.remove(fc)
        limpa_soltos(self)
        self.add(fd)
        self.sai_fim()

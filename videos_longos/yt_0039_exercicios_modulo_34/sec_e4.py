"""yt_0039 · E4 · a elipse e a meia elipse pesada (alvos 08 e 09). E4-1: o círculo e UMA célula polar esticam num movimento até a elipse (a = 1,6;
b = 1); C4a (substituição com os pares a²/a² e b²/b² cancelando, cos² + sen² = 1, a matriz, abr, a área pela metade de cima × 2 = πab, a = b ⇒ πa²
✓). E4-2: a meia elipse x² + 4y² ≤ 1 com o mapa ciano ρ = k y; C4b (x̄ = 0; |J| = r/2; m = k/6 com o selo SEPARA). E4-3 (alvo 09): C4c (M_x =
kπ/64) e ȳ = 3π/32 ≈ 0,295 com o par k/k cancelando; o ⊕ pousa. E4-4: C4d (m = k/6 fatiando em pé ✓); o meio disco achata até a meia elipse e o
⊕ vazado desce de 4/(3π) para 2/(3π) (ESTICA JUNTO); A DENSIDADE PUXA PARA CIMA."""
from k39 import *
from k39 import _troca_col  # noqa: F401

V8 = Vw(470, 560, 240)
V9 = Vw(545, 900, 470)
A8, B8 = 1.6, 1.0
YB = 3 * math.pi / 32
YH = 2 / (3 * math.pi)


def elipse_pts(v, a, b, n=180, t0=0.0, t1=2 * math.pi):
    return [v.px(a * math.cos(t), b * math.sin(t)) for t in np.linspace(t0, t1, n + 1)]


def cel(v, r0, r1, t0, t1, sx, sy, cor, z=6):
    pts = [v.px(sx * r1 * math.cos(t), sy * r1 * math.sin(t)) for t in np.linspace(t0, t1, 13)]
    pts += [v.px(sx * r0 * math.cos(t), sy * r0 * math.sin(t)) for t in np.linspace(t1, t0, 13)]
    return poly_px(pts, cor, 1.0, z=z)


def mat_ent(m, key):
    """As quatro entradas de uma matriz 2×2 (peça key): [sup-esq, sup-dir, inf-esq, inf-dir] em índices, sem as barras."""
    iM = ix_(m, key)
    h = max(m[0][i].height for i in iM)
    corpo = [i for i in iM if m[0][i].height < .8 * h]
    barras = [i for i in iM if i not in corpo]
    c = G(m, iM).get_center()
    ent = [[i for i in corpo if (m[0][i].get_center()[1] > c[1]) == up and (m[0][i].get_center()[0] < c[0]) == esq] for up, esq in ((1, 1), (1, 0), (0, 1), (0, 0))]
    return [sorted(e, key=lambda i: m[0][i].get_center()[0]) for e in ent], barras


class PE4(B39x):
    ANTES = "4 · A ELIPSE"
    COLX = 1040

    def corpo(self):
        v = V8
        # ═══ E4-1 · polares esticadas (alvo 08) ═══
        self.an("E4-1")
        self.gat("quarto problema")
        P = monta_palco(self, v, -1.85, 1.9, -1.3, 1.45)
        ci = lin_px(elipse_pts(v, 1, 1), GEO, 2, dash=(8, 8), z=5)
        fi = poly_px(elipse_pts(v, 1, 1)[:-1], mixh(BG_, GEO, .26), 1.0, z=1)
        bo = lin_px(elipse_pts(v, 1, 1), GEO, 3, z=5)
        self.play(Create(ci), FadeIn(fi), Create(bo), run_time=0.8)
        self.colY = 220
        L1 = linha(self, [("e", r"\dfrac{x^2}{\aa^2}+\dfrac{y^2}{\bb^2}\le 1")], 32)
        self.gat("polares comuns não")
        c0 = cel(v, .55, .8, .6, 1.0, 1, 1, mixh(BG_, LIMA, .45))
        c1 = cel(v, .55, .8, .6, 1.0, 1, 1, LIMA, z=7)
        self.play(FadeIn(c0), FadeIn(c1), run_time=0.5)
        self.gat("estica as polares")
        ta, tb = tk(v, "x", A8, r"\aa"), tk(v, "y", B8, r"\bb")
        qa_, qb_ = v.px(A8, 0), v.px(0, B8)
        ta[1].move_to(PX(qa_[0] + 26, qa_[1] + 30))
        tb[1].move_to(PX(qb_[0] - 26, qb_[1] - 30))
        sa = seta_px(v.px(1.03, .1), v.px(A8 - .04, .1), E1, 3, 12, z=7)
        self.play(Transform(fi, poly_px(elipse_pts(v, A8, B8)[:-1], mixh(BG_, GEO, .26), 1.0, z=1)), Transform(bo, lin_px(elipse_pts(v, A8, B8), GEO, 3, z=5)),
                  Transform(c1, cel(v, .55, .8, .6, 1.0, A8, B8, LIMA, z=7)), Create(sa), Create(ta[0]), Create(tb[0]), run_time=2.0)
        self.pena(ta[1], tb[1], lag=0.1)
        L1 = cad(self, L1, [("q", r"\qquad"), ("x", r"x=\aa\,\R\cos\th")], [], n=15, nota="x = a r cos θ")
        self.gat("e y igual a b")
        L1 = cad(self, L1, [("q2", r"\quad"), ("y", r"y=\bb\,\R\sen\th")], [], n=15, nota="y = b r sen θ")
        self.gat("joga na desigualdade")
        L2 = linha(self, [("f1", r"\dfrac{\aa^2\R^2\cos^2\th}{\aa^2}"), ("p", "+"), ("f2", r"\dfrac{\bb^2\R^2\sen^2\th}{\bb^2}")], 30, gap=26)
        n1, b1, d1 = frac_ix(L2, "f1")
        n2, b2, d2 = frac_ix(L2, "f2")
        self.gat("embaixo cancelam")
        cancela(self, G(L2, n1[:2]), G(L2, d1))
        self.gat("b ao quadrado com b")
        cancela(self, G(L2, n2[:2]), G(L2, d2))
        self.gat("sobra r ao quadrado vezes")
        L2 = cad(self, L2, [("e", "="), ("r2", r"\R^2"), ("pa", r"(\cos^2\th+\sen^2\th)")], [(n1[2:4], "r2"), (n2[2:4], "r2"), (n1[4:], "pa"), (n2[4:], "pa"), ("p", "pa")],
                 n=15, nota="C4a: os a² e os b² cancelam; r²(cos²θ + sen²θ)")
        self.leitura(G(L2, ix_(L2, "pa")), rt=0.7)
        self.gat("o disco de raio um")
        L2 = cad(self, L2, [("e", "="), ("r", r"\R^2\le 1")], [("^r2", "r")], n=15, nota="= r² ≤ 1")
        degrau(self, "C4a", "a²r²cos²θ/a² + b²r²sen²θ/b² = r²(cos²θ + sen²θ) = r² ≤ 1")
        sobe_col(self, [L2], y0=230)
        self.gat("Olha a matriz na tela")
        L3 = linha(self, [("J", "J"), ("e", "="), ("M", r"\begin{vmatrix}\aa\cos\th & -\aa\R\sen\th\\[6pt] \bb\sen\th & \bb\R\cos\th\end{vmatrix}")], 30, gap=26)
        L3._matriz = True
        ent, _b = mat_ent(L3, "M")
        self.gat("diagonal menos diagonal")
        L3 = cad(self, L3, [("e1", "="), ("d1", r"\aa\cos\th\cdot\bb\R\cos\th-\left(-\aa\R\sen\th\right)\left(\bb\sen\th\right)")], [], n=16, nota="D14: diagonal − antidiagonal")
        self.gat("a b r cosseno ao quadrado")
        L3 = cad(self, L3, [("e2", "="), ("t1", r"\aa\bb\R\cos^2\th"), ("p", "+"), ("t2", r"\aa\bb\R\sen^2\th")], [(ent[0], "t1"), (ent[3], "t1"), (ent[1], "t2"), (ent[2], "t2")],
                 n=16, nota="C4a: o determinante abre por mapa")
        self.gat("põe a b r em evidência")
        L3 = cad(self, L3, [("e", "="), ("r", r"\Jl{\aa\bb\R}")], [("^t1", "r"), ("^t2", "r")], n=16, nota="= abr")
        degrau(self, "C4a", "J = |…| = abr cos²θ + abr sen²θ = abr")
        self.gat("esticar por a e por b")
        lab = TP(r"\times\,\aa\bb", *v.px(A8 * .7 * math.cos(.82), B8 * .7 * math.sin(.82)), 28, "l")
        lab.shift(PX(60, -40) - PX(0, 0))
        self.pena(lab)
        chJ = chip(self, r"|J|=\Jl{\aa\bb\R}", 1420, 175, de=G(L3, ix_(L3, "r")).copy())
        sobe_col(self, [L1, L3], y0=230)
        self.gat("faz a metade de cima")
        mc = palavra(self, "METADE DE CIMA × 2", GEO, 26, gap=18)
        L4 = linha(self, [("A", "A"), ("e", "="), ("d", "2"), ("i1", r"\int_0^{\pi}"), ("i2", r"\!\!\int_0^1"), ("j", r"\Jl{\aa\bb\R}"), ("dd", r"\,\dr\,\dth")], 30, gap=34)
        self.gat("faz a metade de cima")
        L4 = cad(self, L4, [("e", "="), ("d", r"2\aa\bb"), ("c1", r"\left[\dfrac{\R^2}{2}\right]_0^1"), ("c2", r"\Big[\th\Big]_0^{\pi}")],
                 [("d", "d"), ("j", "d"), ("i2", "c1"), ("i1", "c2")], n=16, nota="C4a: 2ab[r²/2]₀¹[θ]₀^π")
        self.gat("A integral de r d r dá um meio")
        L4 = cad(self, L4, [("e", "="), ("d", r"2\aa\bb\cdot\dfrac12\cdot\pi")], [("^d", "d"), ("^c1", "d"), ("^c2", "d")], n=16, nota="2ab · 1/2 · π")
        self.gat("pi a b com")
        L4 = cad(self, L4, [("e", "="), ("r", r"\pi\aa\bb")], [("^d", "r")], n=16, nota="= πab")
        degrau(self, "C4a", "A = 2∫∫ abr dr dθ = 2ab[r²/2]₀¹[θ]₀^π = 2ab·½·π = πab")
        self.gat("volta o pi a ao quadrado")
        yb4 = max(pxof(m.get_bottom())[1] for m in self.colms if m is not mc and m in self.mobjects) + 46
        self.play(mc.animate.shift(UP * ((pxof(mc.get_center())[1] - yb4) / 120)), run_time=0.4)
        L5 = linha(self, [("c", r"\aa=\bb\enspace\Rightarrow\enspace\pi a^2")], 30, gap=50, x=pxof(mc.get_right())[0] + 30, y=pxof(mc.get_center())[1] - 6)
        ok_ao_lado(self, L5)
        self.marca("08_E4-1")
        self._fecha(antes=0.6)

        # ═══ E4-2 · a meia elipse pesada: a massa ═══
        self.an("E4-2")
        self.secao("4 · A MEIA ELIPSE PESADA")
        v = V9
        xs = lambda Y: np.sqrt(np.clip(1 - 4 * Y * Y, 0, None))
        mp = mapa_y(v, xs, 0, .5, lambda Y: Y, .5, z=1)
        bd = lin_px([v.px(math.cos(t), .5 * math.sin(t)) for t in np.linspace(0, math.pi, 121)] + [v.px(1, 0)], GEO, 3, z=5)
        sx, sy, lx, ly = eixos_c(v, -1.1, 1.12, -.04, .78)
        tks = [tk(v, "x", -1, r"\Am{-1}"), tk(v, "x", 1, r"\Am{1}")]
        q5 = v.px(0, .5)
        t5 = (lin_px([(q5[0] - 7, q5[1]), (q5[0] + 7, q5[1])], GEO, 2, z=6), TC(r"\Mg{0{,}5}", q5[0] - 46, q5[1] - 52, 28, "r"))
        pronto(sx, sy, lx, ly, *[x for t in tks for x in t], *t5)
        g9 = papel_tela(v)
        sai = palco_sai(self)
        tira_chips(self)
        self.play(*[FadeOut(m) for m in sai + [self.grade]], FadeIn(g9), *[FadeIn(m) for m in [sx, sy, lx, ly] + [x for t in tks for x in t] + list(t5)], run_time=0.8)
        self.remove(*sai)
        self.grade = g9
        limpa_col(self)
        self.colX, self.colY = 1130, 230
        self.gat("a forma da meia elipse")
        # v2 B1 · o mapa em ação: o meio disco de raio 1 com a grade polar (4 anéis × 8 setores) achata para a meia elipse,
        # (x, y) → (x, y/2): a elipse é o círculo esticado (a = 1, b = ½); as células de teste mostram a área × ab
        cel_ = celulas(0, 1, 0, math.pi, 4, 8, k=8)
        MA = MapaAcao(cel_, lambda r_, t_, a: v.px(r_ * math.cos(t_), (1 - a / 2) * r_ * math.sin(t_)), fill=mixh(BG_, GEO, .42),
                      teste={(1, 2): AZC, (3, 2): CORAL, (3, 5): LIMA}, z=3)
        self.play(FadeIn(MA.g), FadeOut(ly), run_time=0.5)
        self.play(MA.anim(2.5), run_time=2.5)
        self.play(FadeIn(ly), run_time=0.3)
        print(f"[mapa] {self.lote} E4-2 mapa em ação meio disco → meia elipse (x, y) → (x, y/2): 32 células, 2,5 s")
        self.play(Create(bd), *MA.so_linhas(), run_time=0.8)
        E1_ = linha(self, [("e", r"x^2+4y^2\le 1,\ y\ge 0")], 32)
        self.gat("rô igual a k vezes")
        mp.set_opacity(1)
        self.play(FadeIn(mp), run_time=0.8)
        lr = rot_m(v, r"\rr=\kk\,y", (-1.05, .72), 0, 0, 32, "l")
        lp = leg("MAIS PESADA EM CIMA", *v.px(-1.05, .605), CI, "left", 26)
        self.pena(lr, lp, lag=0.1)
        E1_ = cad(self, E1_, [("q", r"\qquad"), ("r", r"\rr=\kk\,y")], [], voos=[(lr.f, "r")], n=0, nota="ρ = k y voa da legenda")
        self.gat("pausa e tenta")
        pz = poe_pausa(self, 1130, pxof(E1_.get_bottom())[1] + 52)
        self.colms.append(pz)
        self.colY = pxof(pz.get_bottom())[1]
        self.gat("Aproveita a simetria")
        sim = lin_px([v.px(0, 0), v.px(0, .62)], BR, 2, dash=(8, 8), z=6)
        self.play(Create(sim), run_time=0.5)
        X1 = linha(self, [("x", r"\xb=0")], 32, gap=26)
        leg_ao_lado(self, X1, "SIMETRIA", GEO, 24, 26)
        self.gat("aqui a é um")
        X2 = linha(self, [("ab", r"\aa=1,\ \bb=\dfrac12:"), ("q", r"\quad"), ("x", r"x=\R\cos\th,\ y=\dfrac12\R\sen\th")], 30, gap=22)
        self.gat("a b r ou seja")
        X3 = linha(self, [("J", r"|J|"), ("e", "="), ("p", r"1\cdot\dfrac12\cdot\R")], 30, gap=22, voos=[(chJ.m, "p")])
        X3 = cad(self, X3, [("e", "="), ("r", r"\Jl{\dfrac{\R}{2}}")], [("^p", "r")], n=17, nota="|J| = 1·½·r = r/2")
        self.gat("é r de zero a um")
        X4 = linha(self, [("l", r"0\le\R\le 1,\quad 0\le\th\le\pi")], 30, gap=22)
        degrau(self, "C4b", "a = 1, b = ½: x = r cos θ, y = ½ r sen θ, |J| = r/2; 0 ≤ r ≤ 1, 0 ≤ θ ≤ π")
        self.gat("A massa é a integral")
        chJ2 = chip(self, r"|J|=\Jl{\dfrac{\R}{2}}", 1130, 175, de=G(X3, ix_(X3, "r")).copy())
        limpa_col(self)
        self.play(FadeOut(MA.g), run_time=0.4)
        self.remove(MA.g)
        self.colY = 240
        M1 = linha(self, [("m", r"\mm"), ("e", "="), ("i1", r"\int_0^{\pi}"), ("i2", r"\!\!\int_0^1"), ("k", r"\kk"), ("c", r"\cdot"), ("y", r"\dfrac{\R\sen\th}{2}"),
                          ("c2", r"\cdot"), ("j", r"\Jl{\dfrac{\R}{2}}"), ("d", r"\,\dr\,\dth")], 32, voos=[(chJ2.m, "j")])
        P0 = linha(self, [("r", r"\rr\cdot|J|"), ("e", "="), ("a", r"\kk\cdot\dfrac{\R\sen\th}{2}\cdot\dfrac{\R}{2}"), ("e2", "="), ("b", r"\dfrac{\kk\R^2\sen\th}{4}")], 28, gap=18)
        self.gat("o integrando separa")
        # v2 §5 (13:37): um anel (só r, laranja) e um raio (só θ, verde-água) na grade da meia elipse: o integrando separa assim
        anel_ = lin_px([v.px(.62 * math.cos(t_), .31 * math.sin(t_)) for t_ in np.linspace(0, math.pi, 61)], LAR, 4, z=7)
        raio_ = lin_px([v.px(0, 0), v.px(math.cos(1.0), .5 * math.sin(1.0))], VAG, 4, z=7)
        self.play(Create(anel_), Create(raio_), run_time=0.8)
        M2 = cad(self, M1, [("e", "="), ("k4", r"\dfrac{\kk}{4}"), ("it", r"\int_0^{\pi}\sen\th\,\dth"), ("ir", r"\int_0^1\R^2\,\dr")],
                 [("k", "k4"), ("y", "k4"), ("j", "k4"), ("i1", "it"), ("y", "it"), ("i2", "ir"), ("y", "ir"), ("j", "ir")], n=17, desce=True, nota="C4b: separa só θ · só r")
        sp = mixl([("t", "SEPARA: SÓ", GEO), ("m", r"\th"), ("t", "· SÓ", GEO), ("m", r"\R")], 1130, pxof(M2.get_bottom())[1] + 34, 30)
        self.pena(*sp.p, lag=0.04)
        self.colms += list(sp.p)
        self.colY = pxof(sp.get_bottom())[1]
        sobe_col(self, [M1, P0], y0=230)
        self.gat("A de téta é a integral do seno")
        T1 = linha(self, [("c", r"\Big[-\cos\th\Big]_0^{\pi}")], 32, gap=24, voos=[(G(M2, ix_(M2, "it")), "c")])
        T1 = cad(self, T1, [("e", "="), ("d", r"-\cos\pi+\cos 0")], [("^c", "d")], n=17, nota="G(π) − G(0)")
        self.gat("um mais um dois")
        T1 = cad(self, T1, [("e", "="), ("d", r"1+1")], [("^d", "d")], n=17, nota="1 + 1")
        T1 = cad(self, T1, [("e", "="), ("r", "2")], [("^d", "r")], n=17, nota="= 2")
        degrau(self, "C4b", "[−cos θ]₀^π = −cos π + cos 0 = 1 + 1 = 2")
        self.gat("A de r é r ao quadrado")
        T2 = linha(self, [("c", r"\left[\dfrac{\R^3}{3}\right]_0^1")], 32, gap=22, voos=[(G(M2, ix_(M2, "ir")), "c")])
        T2 = cad(self, T2, [("e", "="), ("r", r"\dfrac13")], [("^c", "r")], n=17, nota="= 1/3")
        degrau(self, "C4b", "[r³/3]₀¹ = 1/3")
        self.gat("Junta tudo com o k sobre quatro")
        T3 = linha(self, [("m", r"\mm"), ("e", "="), ("p", r"\dfrac{\kk}{4}\cdot 2\cdot\dfrac13")], 32, gap=22,
)
        self.gat("k sobre seis")
        T3 = cad(self, T3, [("e", "="), ("r", r"\dfrac{2\kk}{12}")], [("^p", "r")], n=17, nota="D15: k/4 · 2 · 1/3 = 2k/12")
        T3 = cad(self, T3, [("e", "="), ("r", r"\Me{\dfrac{\kk}{6}}")], [("^r", "r")], n=17, nota="m = k/6")
        degrau(self, "C4b", "m = (k/4)·2·(1/3) = k/6")
        self._fecha(antes=0.6)

        # ═══ E4-3 · o momento e o centro de massa (alvo 09) ═══
        self.an("E4-3")
        chm = chip(self, r"\mm=\dfrac{\kk}{6}", 1420, 175, de=G(T3, ix_(T3, "r")).copy())
        limpa_col(self)
        self.play(FadeOut(anel_), FadeOut(raio_), run_time=0.3)
        self.remove(anel_, raio_)
        self.colY = 240
        self.gat("o momento em relação ao eixo")
        hide43 = [mp, bd, sx, sy] + [x for t in tks for x in t] + list(t5)
        pal43, lx43, ly43 = massa_entra(self, "elipse", CAM_M43, 470, 545, 900, hide43, lx, ly, H=.8)
        N1 = linha(self, [("M", r"\Mx"), ("e", "="), ("ii", r"\iint_B"), ("y", r"\Y"), ("r", r"\,\rr"), ("d", r"\,dA")], 32)
        self.gat("a integral de y vezes rô")
        self.leitura(G(N1, ix_(N1, "y", "r")), rt=0.6)
        N1 = cad(self, N1, [("e", "="), ("i1", r"\int_0^{\pi}"), ("i2", r"\!\!\int_0^1"), ("q", r"\left(\dfrac{\R\sen\th}{2}\right)^{\!2}"), ("k", r"\kk"),
                            ("j", r"\,\Jl{\dfrac{\R}{2}}"), ("d", r"\,\dr\,\dth")], [("y", "q"), ("r", "k"), ("ii", "i1"), ("ii", "i2"), ("d", "d")], n=18, desce=True,
                 voos=[(chJ2.m, "j")], nota="C4c: y² k r/2")
        Nz = linha(self, [("a", r"y\,\rr\,|J|"), ("e", "="), ("b", r"\dfrac{\R\sen\th}{2}\cdot\kk\dfrac{\R\sen\th}{2}\cdot\dfrac{\R}{2}"), ("e2", "="), ("c", r"\dfrac{\kk\R^3\sen^2\th}{8}")], 28, gap=18)
        self.gat("os números viram um oitavo")
        iN2 = len(self.colms)
        N2 = cad(self, N1, [("e", "="), ("k8", r"\dfrac{\kk}{8}"), ("it", r"\int_0^{\pi}\sen^2\th\,\dth"), ("ir", r"\int_0^1\R^3\,\dr")],
                 [("^q", "k8"), ("^j", "k8"), ("^k", "k8"), ("^i1", "it"), ("^q", "it"), ("^i2", "ir"), ("^q", "ir"), ("^j", "ir")], n=18, desce=True,
                 nota="C4c: o 1/4 do quadrado e o 1/2 do jacobiano: k/8")
        degrau(self, "C4c", "M_x = ∫∫ ((r sen θ)/2)² k r/2 dr dθ = (k/8)∫ sen²θ dθ ∫ r³ dr")
        self.gat("seno ao quadrado a gente não integra")
        iI1 = len(self.colms)
        I1 = linha(self, [("s", r"\sen^2\th=\dfrac{1-\cos 2\th}{2}")], 30, gap=22)
        leg_ao_lado(self, I1, "IDENTIDADE", GEO, 20, 26)
        self.gat("Integra termo a termo")
        iI2 = len(self.colms)
        I2 = linha(self, [("c", r"\left[\dfrac{\th}{2}-\dfrac{\sen 2\th}{4}\right]_0^{\pi}")], 30, gap=20)
        self.gat("Aplica de zero a pi")
        I2 = cad(self, I2, [("e", "="), ("d", r"\dfrac{\pi}{2}-\dfrac{\sen 2\pi}{4}-0")], [("^c", "d")], n=18, nota="G(π) − G(0)")
        self.gat("sobra pi sobre dois")
        I2 = cad(self, I2, [("e", "="), ("r", r"\dfrac{\pi}{2}")], [("^d", "r")], n=18, nota="= π/2 (sen 2π = 0)")
        degrau(self, "C4c", "[θ/2 − sen 2θ/4]₀^π = π/2 − (sen 2π)/4 − 0 = π/2")
        self.gat("A de r ao cubo")
        sobe_col(self, self.colms[:iN2] + self.colms[iI1:iI2], y0=230)       # v2 §4.1: a coluna maior; saem as linhas já usadas
        I3 = linha(self, [("c", r"\left[\dfrac{\R^4}{4}\right]_0^1")], 30, gap=20, voos=[(G(N2, ix_(N2, "ir")), "c")])
        I3 = cad(self, I3, [("e", "="), ("r", r"\dfrac14")], [("^c", "r")], n=18, nota="= 1/4")
        self.gat("Junta o momento")
        I3 = cad(self, I3, [("q", r"\qquad"), ("M", r"\Mx=\dfrac{\kk}{8}\cdot\dfrac{\pi}{2}\cdot\dfrac14")], [("^r", "M")], n=18, nota="M_x = (k/8)(π/2)(1/4)",
                 voos=[(G(I2, ix_(I2, "r")), "M")])
        self.gat("k pi sobre sessenta e quatro")
        I3 = cad(self, I3, [("e", "="), ("r", r"\dfrac{\kk\pi}{64}")], [("^M", "r")], n=18, nota="= kπ/64")
        degrau(self, "C4c", "M_x = (k/8)(π/2)(1/4) = kπ/64")
        self.gat("é momento sobre massa")
        massa_volta(self, pal43, [mp, bd, sx, sy] + [x for t in tks for x in t] + list(t5), lx43, ly43, lx, ly)
        sobe_col(self, self.colms[:-2], y0=230)
        Y1 = linha(self, [("y", r"\yb"), ("e", "="), ("f", r"\dfrac{\Mx}{\mm}")], 32, gap=26)
        Y1 = cad(self, Y1, [("e", "="), ("f", r"\dfrac{\kk\pi/64}{\kk/6}")], [], n=19, voos=[(G(I3, ix_(I3, "r")), "f")], nota="(kπ/64)/(k/6)")
        self.gat("inverte e multiplica")
        Y1 = cad(self, Y1, [("e", "="), ("a", r"\dfrac{\kk\pi}{64}"), ("c", r"\cdot"), ("b", r"\dfrac{6}{\kk}")], [("^f", "a"), ("^f", "b")], n=19, nota="inverte e multiplica")
        self.gat("o k cancela")
        na, ba, da = frac_ix(Y1, "a")
        nb, bb_, db = frac_ix(Y1, "b")
        cancela(self, G(Y1, na[:1]), G(Y1, db))
        Y2 = cad(self, Y1, [("e", "="), ("r", r"\dfrac{6\pi}{64}")], [(na[1:], "r"), (da, "r"), (nb, "r")], n=19, desce=True, nota="C4c: o k cancela; 6π/64")
        self.gat("três pi sobre trinta e dois")
        Y2 = cad(self, Y2, [("e", "="), ("r", r"\dfrac{3\pi}{32}")], [("^r", "r")], n=19, nota="= 3π/32")
        Y2 = cad(self, Y2, [("e", r"\approx"), ("n", r"\dfrac{9{,}425}{32}"), ("e2", r"\approx"), ("r", r"\Me{0{,}295}")], [], n=19, desce=True, nota="D16: ≈ 9,425/32 ≈ 0,295")
        degrau(self, "C4c", "ȳ = (kπ/64)/(k/6) = (kπ/64)(6/k) = 6π/64 = 3π/32 ≈ 0,295")
        self.gat("zero vírgula duzentos")
        pc = cm(*v.px(0, .75), 16)
        self.play(FadeIn(pc), run_time=0.3)
        self.play(pc.animate.move_to(v.P(0, YB)), run_time=1.2)
        ly_ = lin_px([v.px(-.95, YB), v.px(.95, YB)], E2, 2, dash=(8, 8), z=6)
        lyb = TC(r"\yb", v.px(-.97, YB)[0] - 8, v.px(0, YB)[1], 32, "r")
        self.play(Create(ly_), run_time=0.5)
        self.pena(lyb)
        self.marca("09_E4-3")
        self._fecha(antes=0.6)

        # ═══ E4-4 · conferindo a massa e comparando ═══
        self.an("E4-4")
        tira_chips(self, chJ2)
        limpa_col(self)
        self.colY = 240
        self.gat("conferir a massa sem")
        xa = .35
        ya = math.sqrt(1 - xa * xa) / 2
        tt = tiraV(v, xa, 0, ya, h=.03, cor=E1)
        pt_ = pontos_es(v, (xa, 0), (xa, ya))
        self.play(FadeIn(tt), FadeIn(pt_[0]), FadeIn(pt_[1]), run_time=0.5)
        lsa = rot_m(v, r"y=\dfrac{\sqrt{1-x^2}}{2}", (xa, ya), 30, -46, 26, "l")
        self.pena(lsa)
        self.gat("x vai de menos um")
        C1 = linha(self, [("m", r"\mm"), ("e", "="), ("i1", r"\int_{-1}^{1}"), ("i2", r"\!\!\int_0^{\sqrt{1-x^2}/2}"), ("f", r"\kk\,y"), ("d", r"\,dy\,dx")], 32)
        self.gat("A de dentro é k vezes")
        palavra(self, "DE DENTRO", GEO, 26, gap=14)
        C2 = linha_de(self, C1, [("i", r"\int_0^{\sqrt{1-x^2}/2}\kk\,y\,dy"), ("e", "="), ("c", r"\kk\left[\dfrac{y^2}{2}\right]_0^{\sqrt{1-x^2}/2}")],
                      [("i2", "i"), ("f", "c")], n=20, size=30, gap=10, nota="∫ k y dy = k[y²/2]")
        self.gat("aplicado no topo")
        C2 = cad(self, C2, [("e", "="), ("d0", r"\dfrac{\kk}{2}\left(\dfrac{\sqrt{1-x^2}}{2}\right)^{2}")], [("^c", "d0")], n=20, nota="D17: G(topo) − G(0)")
        self.gat("o quadrado da raiz")
        C2 = cad(self, C2, [("e", "="), ("d", r"\kk\cdot\dfrac12\cdot\dfrac{1-x^2}{4}")], [("^d0", "d")], n=20, nota="(√(1−x²)/2)² = (1−x²)/4")
        self.gat("k vezes um menos x ao quadrado sobre oito")
        C2 = cad(self, C2, [("e", "="), ("r", r"\dfrac{\kk(1-x^2)}{8}")], [("^d", "r")], n=20, nota="= k(1 − x²)/8")
        degrau(self, "C4d", "k[y²/2]₀^{√(1−x²)/2} = k·½·(1 − x²)/4 = k(1 − x²)/8")
        sobe_col(self, [C1], y0=240)
        self.gat("A de fora integra")
        palavra(self, "DE FORA", GEO, 26, gap=14)
        C3 = linha(self, [("f", r"\dfrac{\kk}{8}"), ("c", r"\left[x-\dfrac{x^3}{3}\right]_{-1}^{1}")], 30, gap=10, voos=[(G(C2, ix_(C2, "r")), "f")])
        self.gat("dois terços mais dois")
        C3 = cad(self, C3, [("e", "="), ("f", r"\dfrac{\kk}{8}"), ("p", r"\left[\left(1-\dfrac13\right)-\left(-1+\dfrac13\right)\right]")], [("^f", "f"), ("^c", "p")], n=20,
                 nota="G(1) − G(−1) com os valores")
        C3 = cad(self, C3, [("e", "="), ("f", r"\dfrac{\kk}{8}"), ("p", r"\left(\dfrac23+\dfrac23\right)")], [("^f", "f"), ("^p", "p")], n=20, nota="2/3 + 2/3")
        C3 = cad(self, C3, [("e", "="), ("f", r"\dfrac{\kk}{8}\cdot\dfrac43")], [("^f", "f"), ("^p", "f")], n=20, nota="(k/8)(4/3)")
        self.gat("k sobre seis de novo")
        C4 = cad(self, C3, [("e", "="), ("r", r"\Me{\dfrac{\kk}{6}}")], [("^f", "r")], n=20, desce=True, nota="= k/6")
        ok_ao_lado(self, C4)
        self.leitura(chm.m, rt=0.8)
        degrau(self, "C4d", "(k/8)[x − x³/3]₋₁¹ = (k/8)[(1 − 1/3) − (−1 + 1/3)] = (k/8)(2/3 + 2/3) = (k/8)(4/3) = k/6 ✓")
        self.gat("e se a chapa fosse")
        self.play(FadeOut(tt), FadeOut(pt_[0]), FadeOut(pt_[1]), FadeOut(lsa), run_time=0.4)
        self.remove(tt, *pt_, lsa)
        limpa_col(self)
        self.colY = 260
        self.play(lr.animate.shift(UP * 2.0), lp.animate.shift(UP * 2.0), lyb.animate.move_to(PX(48 - lyb.width * 60, v.px(0, YB)[1])), run_time=0.5)
        md = lin_px([v.px(math.cos(t), math.sin(t)) for t in np.linspace(0, math.pi, 121)], GEO, 1.5, z=4)
        pv = cm(*v.px(0, 4 / (3 * math.pi)), 13, vaz=True)
        self.play(Create(md), FadeIn(pv), run_time=0.8)
        self.gat("achatado pela metade")
        md2 = lin_px([v.px(math.cos(t), .5 * math.sin(t)) for t in np.linspace(0, math.pi, 121)], GEO, 1.5, z=4)
        self.play(Transform(md, md2), pv.animate.move_to(v.P(0, YH)), run_time=1.8)
        ej = leg("ACHATA JUNTO", *v.px(.12, .07), GEO, "left", 26)
        self.pena(ej)
        self.gat("quatro b sobre três pi")
        RX = 1050
        hp_ = lambda h_: v.px(0, h_)[1]
        reg = lin_px([(RX, hp_(0)), (RX, hp_(.5))], GEO, 2, z=6)
        mk1 = lin_px([(RX - 9, hp_(YH)), (RX + 9, hp_(YH))], GEO, 3, z=7)
        lg1 = lin_px([(RX + 10, hp_(YH)), (RX + 50, 835)], GEO, 1.2, z=6)
        lk1 = mixl([("t", "HOMOGÊNEA", GEO), ("m", r"\ 0{,}212")], RX + 60, 840, 22)
        self.play(Create(reg), Create(mk1), Create(lg1), run_time=0.5)
        self.pena(*lk1.p)
        H1, rh = linha(self, [("f", r"\dfrac{4\bb}{3\pi}"), ("e", "="), ("g", r"\dfrac{4\cdot\dfrac12}{3\pi}")], 32, rot="HOMOGÊNEA", rot_cor=GEO)
        self.gat("dois sobre três pi")
        H1 = cad(self, H1, [("e2", "="), ("r", r"\dfrac{2}{3\pi}\approx 0{,}212")], [("^g", "r")], n=20, desce=True, nota="2/(3π) ≈ 0,212")
        degrau(self, "C4d", "HOMOGÊNEA 4b/(3π) = 4·½/(3π) = 2/(3π) ≈ 0,212")
        self.gat("a densidade que cresce")
        mk0 = lin_px([(RX - 9, hp_(.25)), (RX + 9, hp_(.25))], BR, 1.5, dash=(4, 4), z=7)
        lg0 = lin_px([(RX + 10, hp_(.25)), (RX + 50, 790)], BR, 1.2, z=6)
        lk0 = mixl([("t", "METADE", BR), ("m", r"\ 0{,}25")], RX + 60, 795, 22)
        mk2 = lin_px([(RX - 9, hp_(YB)), (RX + 9, hp_(YB))], E2, 3, z=7)
        lg2 = lin_px([(RX + 10, hp_(YB)), (RX + 50, 745)], E2, 1.2, z=6)
        lk2 = mixl([("t", "ρ = k y", E2), ("m", r"\ 0{,}295")], RX + 60, 750, 22)
        self.play(Create(mk0), Create(mk2), Create(lg0), Create(lg2), run_time=0.5)
        self.pena(*lk0.p, *lk2.p, lag=0.1)
        Pc = linha(self, [("a", r"\rr=\kk\,y:"), ("b", r"\dfrac{3\pi}{32}\approx 0{,}295")], 32, gap=26)
        st = seta_px(v.px(.18, YH), v.px(.18, YB), E2, 3, 12, z=8)
        self.play(Create(st), run_time=0.6)
        lpu = leg("A DENSIDADE PUXA PARA CIMA", *v.px(.08, .66), E2, "left", 26)
        self.pena(lpu)
        self.marca("E4-4", agora=True)
        self.sai_fim()

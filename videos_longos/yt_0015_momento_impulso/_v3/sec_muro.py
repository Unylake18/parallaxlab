"""Lote PG: E4-2..E4-6 (de volta ao muro pelos dois caminhos, Moysés 9.1) e E5 (a pulga, Moysés 4.7). v3: F_res(t) em escala real
num gráfico só (pernas duras 56.000 N em 0,01 s, alto e fino; joelhos parábola de pico 5.880 N em 1/7 s, baixa e larga; mesma área),
DOIS PAINÉIS que entram com o conteúdo, números finais piscando juntos, pulga de 6 patas e o manequim 3D no 70 kg × 35 t."""
from kit import *  # noqa: F401,F403

M_PES, H_MURO, G_ = 80.0, 2.5, 9.8
V_CHEGADA = math.sqrt(2 * G_ * H_MURO)           # 7,0 m/s
DP = M_PES * V_CHEGADA                           # 560 kg·m/s = N·s
DT_DURA, DT_JOELHO = 0.01, 2 * 0.5 / V_CHEGADA   # 0,01 s ; 1/7 s ≈ 0,143 s (meio metro de agachamento)
PESO = M_PES * G_                                # 784 N
DK = 0.5 * M_PES * V_CHEGADA ** 2                # 1960 J
D_DURA = V_CHEGADA * DT_DURA / 2                 # 3,5 cm
F_DURA = DP / DT_DURA                            # 56.000 N (força constante no modelo das pernas duras)
PICO_J = 1.5 * DP / DT_JOELHO                    # 5.880 N (parábola de área 560 N·s)
IMG_MANEQUIM = AQUI / "renders" / "manequim_pe.png"


def f_dura(t):
    return F_DURA if 0.0 <= t <= DT_DURA else 0.0


def f_joelho(t):
    u = t / DT_JOELHO
    return PICO_J * 4 * u * (1 - u) if 0.0 <= u <= 1.0 else 0.0


def tex(s, cor=WHITE_, size=M_MID):
    return MathTex(s, font_size=size, color=cor)


def grafico_escala(x0=-6.3, y0=-2.5, w=7.3, h=4.7):
    """Os dois F_res(t) nos MESMOS eixos e em escala real. Devolve dict com eixos, curvas, áreas e marcas."""
    G = Graf(x0, y0, w, h, 0.2, 60000, MathTex(r"F_{res}", font_size=40, color=FC))
    ret = Polygon(G.pt(0, 0), G.pt(0, F_DURA), G.pt(DT_DURA, F_DURA), G.pt(DT_DURA, 0)).set_stroke(FC, 4).set_fill(JC, 0.55).set_z_index(5)
    cb = G.curva(f_joelho, 0, DT_JOELHO, n=300, w=4)
    ab = G.area(f_joelho, 0, DT_JOELHO, n=200, op=0.55)
    marcas = VGroup()
    for f, s in ((F_DURA, r"56.000"), (DT_JOELHO and DP / DT_JOELHO, r"3.920")):
        y = G.pt(0, f)[1]
        marcas.add(Line(P3(x0 - 0.1, y), P3(x0 + 0.1, y)).set_stroke(DIM, 2.5),
                   MathTex(s, font_size=28, color=DIM).next_to(P3(x0 - 0.12, y), LEFT, buff=0.1))
    media = DashedLine(G.pt(0, DP / DT_JOELHO), G.pt(DT_JOELHO, DP / DT_JOELHO), color=FC, stroke_width=2.5, dash_length=0.12)
    la = txt("PERNAS DURAS", T_SMALL, color=GEO).next_to(G.pt(DT_DURA, F_DURA * 0.82), RIGHT, buff=0.2)
    lb = txt("JOELHOS", T_SMALL, color=GEO).next_to(G.pt(DT_JOELHO / 2, PICO_J), UP, buff=0.2)
    aa = Mc((r"\text{ÁREA}=560\ \mathrm{N\cdot s}", JC), size=28).next_to(la, DOWN, buff=0.22, aligned_edge=LEFT)
    ab_l = Mc((r"\text{ÁREA}=560\ \mathrm{N\cdot s}", JC), size=28).next_to(G.pt(DT_JOELHO / 2, 0), DOWN, buff=0.3)
    return dict(G=G, ret=ret, cb=cb, ab=ab, marcas=marcas, media=media, la=la, lb=lb, aa=aa, ab_l=ab_l)


def mostra_grafico(cena, g, rt=1.0):
    """Construção padrão: eixos → marcas → curvas → áreas (da esquerda para a direita)."""
    cena.play(Create(g["G"].eixos), run_time=0.8)
    cena.play(FadeIn(g["marcas"]), run_time=0.5)
    cena.play(GrowFromEdge(g["ret"], DOWN), Create(g["cb"]), FadeIn(g["la"]), FadeIn(g["lb"]), run_time=1.2 * rt)
    cena.play(FadeIn(g["ab"], shift=0.0 * RIGHT), run_time=0.7 * rt)


class LoteMuro(Base):
    def construct(self):
        self.setup_base(cap="EXERCÍCIO 4 · DE VOLTA AO MURO", selo="MOYSÉS · PROB. 9.1")
        self.e4()
        self.e5()
        self.fim()
        self.relatorio()

    # ── E4 ──────────────────────────────────────────────────────────────────────────────────────────────────
    def e4(self):
        self.an("E4-2")
        g = grafico_escala()
        Ja, Jb = area_num(f_dura, 0, 0.2, 200001), area_num(f_joelho, 0, DT_JOELHO)
        print(f"[QA] E4-2 áreas em escala real: pernas duras {Ja:.3f} N·s, joelhos {Jb:.3f} N·s (alvo 560); "
              f"alturas {F_DURA:.0f} N × pico {PICO_J:.0f} N; larguras {DT_DURA} s × {DT_JOELHO:.4f} s")
        c1 = linha(txt("PERNAS DURAS", T_SMALL, color=GEO), tex(r"\Delta t=0{,}01\ \mathrm{s}", DIM, 38), buff=0.25)
        c2 = linha(txt("JOELHOS", T_SMALL, color=GEO), tex(r"\Delta t\approx0{,}143\ \mathrm{s}", DIM, 38), buff=0.25)
        c3 = Mc((r"\text{MESMA ÁREA}=560\ \mathrm{N\cdot s}", JC), size=38)
        conta(c1, c2, c3, topo=1.6, buff=0.6, x0=1.7)
        mostra_grafico(self, g)
        self.ate(0.2)
        self.play(FadeIn(g["aa"]), FadeIn(g["ab_l"]), Write(c3), run_time=0.9)
        self.ate(0.5)
        self.play(FadeIn(c1), Indicate(g["ret"], color=WHITE_, scale_factor=1.0), run_time=0.8)
        self.ate(0.75)
        self.play(FadeIn(c2), Create(g["media"]), FadeIn(g["marcas"][3]), run_time=0.8)
        self.play(Indicate(VGroup(g["aa"], g["ab_l"]), color=WHITE_, scale_factor=1.1), run_time=0.8)
        self.ate(0.97)
        self.g4 = g
        # E4-3 e E4-4 · DOIS PAINÉIS: cada um entra com o seu conteúdo ---------------------------------------------------
        self.an("E4-3")
        self.clear(rt=0.5)
        XL, XR = 0.0, PAINEL_X                                # o caminho 1 começa no centro e desliza para a esquerda no E4-4
        pl, pr = painel(0, 5.5), painel(1, 5.5)
        t1 = linha(txt("CAMINHO 1", T_LAB, color=DIM), txt("IMPULSO", T_LAB, color=JC, bold=True), buff=0.25).move_to(P3(XL, 1.85))
        t2 = linha(txt("CAMINHO 2", T_LAB, color=DIM), txt("TRABALHO", T_LAB, bold=True), buff=0.25).move_to(P3(XR, 1.85))
        f1 = Mc((r"F_{res,\mathrm{m\acute{e}d}}", FC), "=", (r"\frac{560}{\Delta t}", WHITE_), size=46).move_to(P3(XL, 0.95))
        ya, yb = -0.45, -1.95
        a1 = Mc(r"\frac{560}{0{,}01}", "=", (r"56.000\ \mathrm{N}", FC), size=44).move_to(P3(XL, ya - 0.4))
        b1 = Mc(r"\frac{560}{1/7}", r"\approx", (r"3.920\ \mathrm{N}", FC), size=44).move_to(P3(XL, yb - 0.4))
        ra1 = txt("PERNAS DURAS", T_SMALL, color=GEO).move_to(P3(XL, ya + 0.35))
        rb1 = txt("JOELHOS", T_SMALL, color=GEO).move_to(P3(XL, yb + 0.35))
        self.play(FadeIn(pl), FadeIn(t1), Write(f1), run_time=1.0)
        self.ate(0.45)
        self.play(FadeIn(ra1), Write(a1), run_time=0.8)
        self.ate(0.72)
        self.play(FadeIn(rb1), Write(b1), run_time=0.8)
        print(f"[QA] E4-3 F_res,méd: {DP / DT_DURA:.0f} N e {DP / DT_JOELHO:.1f} N")
        self.ate(0.97)
        self.an("E4-4")
        cam1 = VGroup(t1, f1, ra1, a1, rb1, b1)
        fdl = Mc((r"F_{res}\cdot d", FC), "=", (r"\Delta K", WHITE_), size=34).move_to(P3(XR, 1.3))
        f2 = Mc((r"\Delta K", WHITE_), "=", r"\tfrac{1}{2}\cdot 80\cdot 7{,}0^{2}", "=", r"1.960\ \mathrm{J}", size=40).move_to(P3(XR, 0.65))
        a2 = Mc(r"\frac{1.960}{0{,}035}", "=", (r"56.000\ \mathrm{N}", FC), size=44).move_to(P3(XR, ya - 0.4))
        b2 = Mc(r"\frac{1.960}{0{,}5}", "=", (r"3.920\ \mathrm{N}", FC), size=44).move_to(P3(XR, yb - 0.4))
        ra2 = linha(txt("PERNAS DURAS", T_SMALL, color=GEO), tex(r"d=3{,}5\ \mathrm{cm}", DIM, 30), buff=0.2).move_to(P3(XR, ya + 0.35))
        rb2 = linha(txt("JOELHOS", T_SMALL, color=GEO), tex(r"d=0{,}5\ \mathrm{m}", DIM, 30), buff=0.2).move_to(P3(XR, yb + 0.35))
        self.ate(0.04)
        self.play(VGroup(pl, cam1).animate.shift(LEFT * PAINEL_X), run_time=0.7)
        self.play(cam1.animate.set_opacity(0.45), FadeIn(pr), FadeIn(t2), Write(fdl), run_time=0.9)
        self.play(Write(f2), run_time=0.9)
        self.ate(0.42)
        self.play(FadeIn(rb2), Write(b2), run_time=0.8)
        self.ate(0.68)
        self.play(FadeIn(ra2), Write(a2), run_time=0.8)
        print(f"[QA] E4-4 ΔK = {DK:.1f} J; d dura = {D_DURA * 100:.2f} cm; F = {DK / 0.5:.0f} N e {DK / D_DURA:.0f} N")
        self.ate(0.8)
        self.play(cam1.animate.set_opacity(1), run_time=0.4)
        self.play(Indicate(a1[2], color=WHITE_, scale_factor=1.2), Indicate(a2[2], color=WHITE_, scale_factor=1.2), run_time=0.9)
        self.play(Indicate(b1[2], color=WHITE_, scale_factor=1.2), Indicate(b2[2], color=WHITE_, scale_factor=1.2), run_time=0.9)
        self.ate(0.97)
        # E4-5 · N = F_res + mg: o gráfico em escala real com a faixa do peso -----------------------------------------
        self.an("E4-5")
        self.clear(rt=0.5)
        g = grafico_escala()
        nn = Mc((r"N=F_{res}+m g", FC), size=48)
        n1 = linha(txt("PERNAS DURAS", T_SMALL, color=GEO), tex(r"\frac{56.784}{784}", WHITE_, 36), buff=0.25)
        n2 = linha(txt("JOELHOS", T_SMALL, color=GEO), tex(r"\frac{4.704}{784}", WHITE_, 36), buff=0.25)
        conta(nn, n1, n2, topo=2.0, buff=0.55, x0=1.7)
        G = g["G"]
        banda = Rectangle(width=G.w, height=max(G.h * PESO / G.fmax, 0.02)).set_stroke(width=0).set_fill(FC, 0.95)
        banda.move_to((G.pt(0, 0) + G.pt(0.2, PESO)) / 2).set_z_index(8)
        pw = Mc((r"m g=784\ \mathrm{N}", FC), size=30).next_to(G.pt(0.2, PESO), RIGHT, buff=0.55).shift(UP * 0.3)
        na = Mc((r"\approx 72\ \mathrm{pesos}", FC), size=36).next_to(g["la"], DOWN, buff=0.25, aligned_edge=LEFT)
        nb = Mc((r"\approx 6\ \mathrm{pesos}", FC), size=36).next_to(g["lb"], RIGHT, buff=0.3)
        mostra_grafico(self, g, rt=0.7)
        self.play(Write(nn), run_time=0.9)
        self.ate(0.3)
        self.play(GrowFromEdge(banda, LEFT), FadeIn(pw), run_time=0.8)
        self.ate(0.5)
        self.play(FadeIn(n1), FadeIn(n2), run_time=0.7)
        self.ate(0.66)
        self.play(FadeIn(na), FadeIn(nb), run_time=0.7)
        self.play(Indicate(na, color=WHITE_, scale_factor=1.2), Indicate(nb, color=WHITE_, scale_factor=1.2), run_time=0.9)
        print(f"[QA] E4-5 N/(m g): {(F_DURA + PESO) / PESO:.2f} e {(DP / DT_JOELHO + PESO) / PESO:.2f}")
        self.ate(0.97)
        # E4-6 · CENTRO -------------------------------------------------------------------------------------------
        self.an("E4-6")
        self.clear(rt=0.5)
        fr1 = centro(txt("MAIS TEMPO E MAIS DISTÂNCIA", 42, bold=True), 2.1)
        fr2 = centro(txt("MENOS FORÇA", 42, color=FC, bold=True), 1.3)
        self.play(Write(fr1), run_time=0.9)
        self.play(FadeIn(fr2, shift=0.1 * UP), run_time=0.6)
        linhas = [(txt("SAQUE DE TÊNIS", T_MAIN), tex(r"\approx 49\ \mathrm{kgf}", WHITE_, 46)),
                  (txt("PÊNALTI", T_MAIN), tex(r"\approx 92\ \mathrm{kgf}", WHITE_, 46)),
                  (txt("CARRO A 60 KM/H NO MURO", T_MAIN), tex(r"\approx 25\ \mathrm{tf}", WHITE_, 46))]
        for (a, b), y in zip(linhas, (0.0, -1.1, -2.2)):
            a.move_to(P3(0, y)).align_to(P3(-5.2, 0), LEFT)
            b.move_to(P3(0, y)).align_to(P3(5.2, 0), RIGHT)
        regua = centro(Line(P3(-5.4, 0.6), P3(5.4, 0.6)).set_stroke(GEO, 1.5, opacity=0.4))
        self.ate(0.25)
        self.play(Create(regua), Indicate(fr2, color=WHITE_, scale_factor=1.08), run_time=0.8)
        for k, frac in ((0, 0.38), (1, 0.55), (2, 0.72)):
            self.ate(frac)
            self.play(FadeIn(linhas[k][0], shift=0.1 * RIGHT), Write(linhas[k][1]), run_time=0.7)
        self.play(Indicate(linhas[2][1], color=WHITE_, scale_factor=1.15), run_time=0.8)
        self.ate(0.97)

    # ── E5 · a pulga ────────────────────────────────────────────────────────────────────────────────────────
    def e5(self):
        self.clear(rt=0.5)
        self.secao("EXERCÍCIO 5 · A PULGA", "MOYSÉS · PROB. 4.7")
        self.an("E5-1")
        YC = -2.8
        chao = Line(P3(-6.6, YC), P3(-0.2, YC)).set_stroke(GEO, 2.5, opacity=0.6)
        H = 3.6                                                  # 50 cm na tela
        regua = DoubleArrow(P3(-6.2, YC), P3(-6.2, YC + H), buff=0, color=GEO, stroke_width=3, tip_length=0.15)
        h_lab = tex(r"h=50\ \mathrm{cm}", GEO, 38).next_to(regua, RIGHT, buff=0.15).shift(UP * 0.9)
        ref = DashedLine(P3(-6.4, YC + H), P3(-0.8, YC + H), color=DIM, stroke_width=2)
        s_ = ValueTracker(0.0)
        x0, x1 = -4.4, -1.6

        def pos(s):
            return P3(x0 + (x1 - x0) * s, YC + 4 * H * s * (1 - s))
        traj = DashedVMobject(VMobject().set_points_smoothly([pos(s) + P3(0.1, 0.3) for s in np.linspace(0, 1, 40)]).set_stroke(DIM, 2), num_dashes=40)
        pu = always_redraw(lambda: pulga(0.0, 0.75).shift(pos(s_.get_value()) - P3(0, 0)))
        # ZOOM no painel da direita
        pz = painel(1, 5.0)
        zl = txt("ZOOM", T_SMALL, color=DIM).move_to(P3(PAINEL_X, 1.95))
        dados = linha(tex(r"m=2\ \mathrm{mg}", WHITE_, 40), tex(r"d=1\ \mathrm{mm}", WHITE_, 40), buff=0.6).move_to(P3(PAINEL_X, 1.3))
        ext = ValueTracker(0.0)
        YZ = -2.3
        zpu = always_redraw(lambda: pulga(ext.get_value(), 2.3).shift(P3(PAINEL_X - 0.2, YZ)))
        chz = Line(P3(PAINEL_X - 2.8, YZ), P3(PAINEL_X + 2.8, YZ)).set_stroke(GEO, 2, opacity=0.6)
        y0 = YZ + 0.55 * 2.3 + 0.33 * 2.3
        zd = DoubleArrow(P3(PAINEL_X + 1.95, y0), P3(PAINEL_X + 1.95, y0 + 0.26 * 2.3), buff=0, color=GEO, stroke_width=2.5, tip_length=0.1)
        zd_l = tex(r"d=1\ \mathrm{mm}", GEO, 30).next_to(zd, UP, buff=0.12)
        self.play(Create(chao), FadeIn(pu), run_time=0.7)
        self.play(GrowFromEdge(regua, DOWN), FadeIn(h_lab), FadeIn(ref), run_time=0.8)
        self.play(FadeIn(pz), FadeIn(zl), FadeIn(chz), FadeIn(zpu), Write(dados), run_time=0.9)
        self.ate(0.25)
        self.play(Create(traj), run_time=0.5)
        self.play(s_.animate.set_value(1.0), run_time=1.6, rate_func=linear)
        self.ate(0.6)
        self.play(ext.animate.set_value(1.0), GrowFromEdge(zd, DOWN), FadeIn(zd_l), run_time=1.3)
        self.play(ext.animate.set_value(0.0), run_time=0.6)
        self.play(ext.animate.set_value(1.0), run_time=0.6)
        self.ate(0.97)
        pu.clear_updaters()
        zpu.clear_updaters()
        # E5-2 e E5-3 · DOIS PAINÉIS com o conteúdo; v centrado acima -------------------------------------------------
        self.an("E5-2")
        self.clear(rt=0.5)
        XL, XR = 0.0, PAINEL_X                                # caminho 1 no centro; desliza para a esquerda no E5-3
        vv = centro(Mc((r"v=\sqrt{2gh}=3{,}13\ \mathrm{m/s}", VEL), size=46), 2.1)
        self.play(Write(vv), run_time=0.9)
        pl, pr = painel(0, 4.6, topo=1.45), painel(1, 4.6, topo=1.45)
        t1 = linha(txt("CAMINHO 1", T_LAB, color=DIM), txt("DISTÂNCIA", T_LAB, bold=True), buff=0.25).move_to(P3(XL, 1.0))
        t2 = linha(txt("CAMINHO 2", T_LAB, color=DIM), txt("TEMPO", T_LAB, color=JC, bold=True), buff=0.25).move_to(P3(XR, 1.0))
        e1 = Mc("a", "=", r"\frac{v^{2}}{2d}", "=", r"\frac{g\,h}{d}", "=", r"500\,g", size=44).move_to(P3(XL, -0.2))
        f1 = Mc((r"F_{res}", FC), "=", r"m\,a", "=", r"\frac{m\,v^{2}}{2d}", size=44).move_to(P3(XL, -1.85))
        self.ate(0.45)
        self.play(FadeIn(pl), FadeIn(t1), Write(e1), run_time=1.2)
        print(f"[QA] E5-2 v = {math.sqrt(2 * 9.8 * 0.5):.3f} m/s; a/g = h/d = {0.5 / 0.001:.0f}")
        self.play(Indicate(e1[6], color=WHITE_, scale_factor=1.2), run_time=0.8)
        self.ate(0.88)
        self.play(Write(f1), run_time=0.9)
        self.ate(0.97)
        self.an("E5-3")
        e2 = Mc(r"\Delta t", "=", r"\frac{2d}{v}", "=", r"0{,}64\ \mathrm{ms}", size=44).move_to(P3(XR, -0.2))
        f2 = Mc((r"F_{res}", FC), "=", r"\frac{m\,v}{\Delta t}", "=", r"\frac{m\,v^{2}}{2d}", size=44).move_to(P3(XR, -1.85))
        print(f"[QA] E5-3 Δt = {2 * 0.001 / math.sqrt(2 * 9.8 * 0.5) * 1000:.3f} ms")
        self.play(VGroup(pl, t1, e1, f1).animate.shift(LEFT * PAINEL_X), run_time=0.7)
        self.play(FadeIn(pr), FadeIn(t2), Write(e2), run_time=1.1)
        self.ate(0.4)
        self.play(Write(f2), run_time=0.9)
        self.ate(0.6)
        self.play(Indicate(f1[4], color=WHITE_, scale_factor=1.25), Indicate(f2[4], color=WHITE_, scale_factor=1.25), run_time=1.0)
        mesma = legenda("A MESMA FÍSICA PELOS DOIS TEOREMAS")
        self.play(FadeIn(mesma), run_time=0.5)
        self.ate(0.97)
        # E5-4 · CENTRO: N = m(a + g) = 501 pesos ---------------------------------------------------------------------
        self.an("E5-4")
        self.clear(rt=0.5)
        n1 = centro(Mc((r"N", FC), "=", r"m\,(a+g)", "=", r"m\,g\,\Big(\frac{h}{d}", r"+1\Big)", size=60), 1.2)
        n2 = centro(Mc((r"N", FC), "=", (r"501\ \mathrm{pesos}", FC), size=72), -0.5)
        nao = centro(txt("NÃO 500", T_LAB, color=DIM), -1.55)
        self.play(Write(n1), run_time=1.2)
        self.ate(0.4)
        self.play(Indicate(n1[5], color=WHITE_, scale_factor=1.35), run_time=0.9)
        self.play(Indicate(n1[5], color=WHITE_, scale_factor=1.35), run_time=0.9)
        self.play(Write(n2), FadeIn(nao), run_time=0.9)
        cx = SurroundingRectangle(n2, color=FC, buff=0.25, stroke_width=2.5, corner_radius=0.1)
        self.play(Create(cx), run_time=0.5)
        self.ate(0.7)
        self.dica_entra(dica(["CONTATO", MathTex(r"\neq", font_size=32), "RESULTANTE"]))
        self.ate(0.97)
        # E5-5 · 1 gf; o manequim do hook (70 kg) ao lado de um bloco de 35 t ------------------------------------------
        self.an("E5-5")
        self.clear(rt=0.5)
        n3 = centro(Mc((r"N\approx9{,}8\times10^{-3}\ \mathrm{N}\approx1{,}0\times10^{-3}\ \mathrm{kgf}", FC), size=42, w=9.0), 2.15)
        um = centro(txt("UM GRAMA-FORÇA", T_SMALL, color=DIM), 1.55)
        chao = centro(Line(P3(-5.5, -2.9), P3(5.5, -2.9)).set_stroke(GEO, 2.5, opacity=0.6))
        if IMG_MANEQUIM.exists():
            pes = ImageMobject(str(IMG_MANEQUIM)).set_height(3.6)
            pes.move_to(P3(-2.6, -2.9 + 1.8))
        else:
            pes = silhueta(3.0).shift(P3(-2.6, -2.9))
        pl = tex(r"70\ \mathrm{kg}", WHITE_, 42).next_to(pes, UP, buff=0.2)
        bloco = Corpo("", STEEL, 3.2, 2.4).at(2.8, -2.9)
        bloco.front.set_stroke(GEO, 2.5)
        bl = tex(r"35\ \mathrm{t}", WHITE_, 52).move_to(bloco)
        self.play(Write(n3), FadeIn(um), run_time=1.0)
        self.ate(0.35)
        self.play(Create(chao), FadeIn(pes, shift=0.2 * UP), FadeIn(pl), run_time=0.8)
        self.play(GrowFromEdge(bloco, DOWN), run_time=0.8)
        self.play(Write(bl), run_time=0.6)
        print(f"[QA] E5-5 N = {2e-6 * 9.8 * 501:.4e} N; 70 kg × 501 = {70 * 501 / 1000:.2f} t")
        self.ate(0.97)

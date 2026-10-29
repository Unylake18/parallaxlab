"""Lote PG: E4-2..E4-6 (de volta ao muro pelos dois caminhos) e E5 (a pulga). v4: o gráfico/a pulga ficam no PALCO; caminhos na CONTA. v3: F_res(t) em escala real
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
        self.setup_base(cap="EXERCÍCIO 4 · DE VOLTA AO MURO", selo="DOIS CAMINHOS: TEMPO E DISTÂNCIA")
        self.e4()
        self.e5()
        self.fim()
        self.relatorio()

    # ── E4 · PALCO: o gráfico em escala real o tempo todo; CONTA: os dois caminhos, um embaixo do outro ───────────────
    def e4(self):
        self.an("E4-2")
        g = grafico_escala(x0=-5.7, y0=-2.45, w=5.9, h=4.55)
        Ja, Jb = area_num(f_dura, 0, 0.2, 200001), area_num(f_joelho, 0, DT_JOELHO)
        print(f"[QA] E4-2 áreas em escala real: pernas duras {Ja:.3f} N·s, joelhos {Jb:.3f} N·s (alvo 560); "
              f"alturas {F_DURA:.0f} N × pico {PICO_J:.0f} N; larguras {DT_DURA} s × {DT_JOELHO:.4f} s")
        c1 = linha(txt("PERNAS DURAS", T_SMALL, color=GEO), tex(r"\Delta t=0{,}01\ \mathrm{s}", DIM, 38), buff=0.25)
        c2 = linha(txt("JOELHOS", T_SMALL, color=GEO), tex(r"\Delta t\approx0{,}143\ \mathrm{s}", DIM, 38), buff=0.25)
        c3 = Mc((r"\text{MESMA ÁREA}=560\ \mathrm{N\cdot s}", JC), size=38)
        conta(c1, c2, c3, topo=1.6, buff=0.6, x0=1.4)
        mostra_grafico(self, g)
        self.ate(0.2)
        self.play(FadeIn(g["aa"]), FadeIn(g["ab_l"]), Write(c3), run_time=0.9)
        self.ate(0.5)
        self.play(FadeIn(c1), Indicate(g["ret"], color=WHITE_, scale_factor=1.0), run_time=0.8)
        self.ate(0.75)
        self.play(FadeIn(c2), Create(g["media"]), run_time=0.8)
        self.play(Indicate(VGroup(g["aa"], g["ab_l"]), color=WHITE_, scale_factor=1.1), run_time=0.8)
        self.ate(0.97)
        self.g4 = g
        G4, t04 = g["G"], self.clk.get_value()

        def corre():
            u = ((self.clk.get_value() - t04) % 3.0) / 3.0
            ta, tb = u * 0.03, u * DT_JOELHO
            return VGroup(Dot(G4.pt(min(ta, DT_DURA), f_dura(min(ta, DT_DURA))), radius=0.06, color=WHITE_).set_opacity(0.9 if ta <= DT_DURA else 0.0),
                          Dot(G4.pt(tb, f_joelho(tb)), radius=0.07, color=WHITE_)).set_z_index(9)
        self.ponto4 = VGroup(always_redraw(corre), cursor(self, G4, 0.0, 0.2, 4.0))
        self.add(self.ponto4)
        # E4-3 · CAMINHO 1 (impulso) na metade de cima da CONTA -------------------------------------------------------
        self.an("E4-3")
        self.play(FadeOut(c1), FadeOut(c2), FadeOut(c3), run_time=0.4)
        t1 = linha(txt("CAMINHO 1", T_SMALL, color=DIM), txt("IMPULSO", T_LAB, color=JC, bold=True), buff=0.25)
        f1 = Mc((r"F_{res,\mathrm{m\acute{e}d}}", FC), "=", (r"560/\Delta t", WHITE_), size=40)
        a1 = linha(txt("DURAS", T_SMALL, color=GEO), Mc(r"560/0{,}01", "=", (r"56.000\ \mathrm{N}", FC), size=38), buff=0.25)
        b1 = linha(txt("JOELHOS", T_SMALL, color=GEO), Mc(r"560/(1/7)", r"\approx", (r"3.920\ \mathrm{N}", FC), size=38), buff=0.25)
        cam1 = conta(t1, f1, a1, b1, topo=2.3, buff=0.16, x0=1.2)
        self.play(FadeIn(t1), Write(f1), Indicate(VGroup(g["aa"], g["ab_l"]), color=WHITE_, scale_factor=1.05), run_time=1.0)
        self.ate(0.45)
        self.play(FadeIn(a1[0]), Write(a1[1]), Indicate(g["ret"], color=WHITE_, scale_factor=1.0), run_time=0.9)
        self.ate(0.72)
        self.play(FadeIn(b1[0]), Write(b1[1]), FadeIn(g["marcas"][3]), Indicate(g["media"], color=WHITE_), run_time=0.9)
        print(f"[QA] E4-3 F_res,méd: {DP / DT_DURA:.0f} N e {DP / DT_JOELHO:.1f} N")
        self.ate(0.97)
        # E4-4 · CAMINHO 2 (trabalho) embaixo; o caminho 1 apaga a 40%; os números finais piscam juntos ----------------------
        self.an("E4-4")
        sep = Line(P3(1.2, -0.3), P3(6.5, -0.3)).set_stroke(GEO, 1.2, opacity=0.35)
        t2 = linha(txt("CAMINHO 2", T_SMALL, color=DIM), txt("TRABALHO", T_LAB, bold=True), buff=0.25)
        f2 = Mc((r"F_{res}\,d", FC), "=", (r"\Delta K", WHITE_), "=", r"\tfrac{1}{2}\cdot 80\cdot 7{,}0^{2}", "=", r"1.960\ \mathrm{J}", size=34)
        b2 = Mc(r"d=0{,}5\ \mathrm{m}\!:\ 1.960/0{,}5", "=", (r"3.920\ \mathrm{N}", FC), size=36)
        a2 = Mc(r"d=3{,}5\ \mathrm{cm}\!:\ 1.960/0{,}035", "=", (r"56.000\ \mathrm{N}", FC), size=36)
        conta(t2, f2, b2, a2, topo=-0.45, buff=0.14, x0=1.2)
        self.ate(0.04)
        self.play(cam1.animate.set_opacity(0.4), Create(sep), FadeIn(t2), run_time=0.7)
        self.play(Write(f2), run_time=1.1)
        self.ate(0.42)
        self.play(Write(b2), run_time=0.8)
        self.ate(0.68)
        self.play(Write(a2), run_time=0.8)
        print(f"[QA] E4-4 ΔK = {DK:.1f} J; d dura = {D_DURA * 100:.2f} cm; F = {DK / 0.5:.0f} N e {DK / D_DURA:.0f} N")
        self.ate(0.8)
        self.play(cam1.animate.set_opacity(1), run_time=0.4)
        self.play(Indicate(a1[1][2], color=WHITE_, scale_factor=1.2), Indicate(a2[2], color=WHITE_, scale_factor=1.2), run_time=0.9)
        self.play(Indicate(b1[1][2], color=WHITE_, scale_factor=1.2), Indicate(b2[2], color=WHITE_, scale_factor=1.2), run_time=0.9)
        self.ate(0.97)
        # E4-5 · N = F_res + mg: o mesmo gráfico ganha a faixa do peso ----------------------------------------------------
        self.an("E4-5")
        self.play(FadeOut(cam1), FadeOut(sep), FadeOut(VGroup(t2, f2, b2, a2)), run_time=0.5)
        nn = Mc((r"N=F_{res}+m g", FC), size=48)
        n1 = linha(txt("PERNAS DURAS", T_SMALL, color=GEO), tex(r"\frac{56.784}{784}", WHITE_, 36), buff=0.25)
        n2 = linha(txt("JOELHOS", T_SMALL, color=GEO), tex(r"\frac{4.704}{784}", WHITE_, 36), buff=0.25)
        conta(nn, n1, n2, topo=2.0, buff=0.55, x0=1.6)
        G = g["G"]
        banda = Rectangle(width=G.w, height=max(G.h * PESO / G.fmax, 0.02)).set_stroke(width=0).set_fill(FC, 0.95)
        banda.move_to((G.pt(0, 0) + G.pt(0.2, PESO)) / 2).set_z_index(8)
        pw = Mc((r"m g=784\ \mathrm{N}", FC), size=30).next_to(G.pt(0.2, PESO), UP, buff=0.3).shift(LEFT * 0.3)
        na = Mc((r"\approx 72\ \mathrm{pesos}", FC), size=36).next_to(g["la"], DOWN, buff=0.25, aligned_edge=LEFT)
        nb = Mc((r"\approx 6\ \mathrm{pesos}", FC), size=36).next_to(g["lb"], RIGHT, buff=0.3)
        self.play(Write(nn), FadeOut(g["aa"]), run_time=0.9)
        self.ate(0.3)
        self.play(GrowFromEdge(banda, LEFT), FadeIn(pw), run_time=0.8)
        self.ate(0.5)
        self.play(FadeIn(n1), FadeIn(n2), run_time=0.7)
        self.ate(0.66)
        self.play(FadeIn(na), FadeIn(nb), run_time=0.7)
        self.play(Indicate(na, color=WHITE_, scale_factor=1.2), Indicate(nb, color=WHITE_, scale_factor=1.2), run_time=0.9)
        print(f"[QA] E4-5 N/(m g): {(F_DURA + PESO) / PESO:.2f} e {(DP / DT_JOELHO + PESO) / PESO:.2f}")
        self.ate(0.97)
        # E4-6 · o gráfico fica no PALCO; CONTA: a conclusão e a mini-tabela ---------------------------------------------
        self.an("E4-6")
        self.play(FadeOut(VGroup(nn, n1, n2)), run_time=0.4)
        fr1 = txt("MAIS TEMPO E MAIS DISTÂNCIA", T_LAB, bold=True)
        fr2 = txt("MENOS FORÇA", T_MAIN, color=FC, bold=True)
        conta(fr1, fr2, topo=2.2, buff=0.25, x0=1.2)
        self.play(Write(fr1), run_time=0.9)
        self.play(FadeIn(fr2, shift=0.1 * UP), Indicate(g["cb"], color=WHITE_), run_time=0.7)
        linhas = [(txt("SAQUE DE TÊNIS", T_SMALL), tex(r"\approx 49\ \mathrm{kgf}", WHITE_, 36)),
                  (txt("PÊNALTI", T_SMALL), tex(r"\approx 92\ \mathrm{kgf}", WHITE_, 36)),
                  (txt("CARRO A 60 KM/H NO MURO", T_SMALL), tex(r"\approx 25\ \mathrm{tf}", WHITE_, 36))]
        for (a, b), y in zip(linhas, (0.2, -0.75, -1.7)):
            a.move_to(P3(0, y)).align_to(P3(1.2, 0), LEFT)
            b.move_to(P3(0, y)).align_to(P3(6.6, 0), RIGHT)
        regua = Line(P3(1.2, 0.8), P3(6.6, 0.8)).set_stroke(GEO, 1.5, opacity=0.4)
        self.ate(0.25)
        self.play(Create(regua), Indicate(fr2, color=WHITE_, scale_factor=1.08), run_time=0.8)
        for k, frac in ((0, 0.38), (1, 0.55), (2, 0.72)):
            self.ate(frac)
            self.play(FadeIn(linhas[k][0], shift=0.1 * RIGHT), Write(linhas[k][1]), run_time=0.7)
        self.play(Indicate(linhas[2][1], color=WHITE_, scale_factor=1.15), run_time=0.8)
        self.ate(0.97)

    # ── E5 · a pulga: o salto e o zoom ficam no PALCO; os dois caminhos na CONTA ─────────────────────────────────────
    def e5(self):
        self.clear(rt=0.5)
        self.secao("EXERCÍCIO 5 · A PULGA", "FORÇA DE CONTATO × RESULTANTE")
        self.an("E5-1")
        YC = -2.8
        chao = Line(P3(-6.6, YC), P3(-3.3, YC)).set_stroke(GEO, 2.5, opacity=0.6)
        H = 3.6                                                  # 50 cm na tela
        regua = DoubleArrow(P3(-6.35, YC), P3(-6.35, YC + H), buff=0, color=GEO, stroke_width=3, tip_length=0.15)
        h_lab = tex(r"h=50\ \mathrm{cm}", GEO, 34).next_to(regua, RIGHT, buff=0.12).shift(UP * 1.2)
        ref = DashedLine(P3(-6.5, YC + H), P3(-3.4, YC + H), color=DIM, stroke_width=2)
        s_ = ValueTracker(0.0)
        x0, x1 = -5.4, -4.0

        def pos(s):
            return P3(x0 + (x1 - x0) * s, YC + 4 * H * s * (1 - s))
        traj = DashedVMobject(VMobject().set_points_smoothly([pos(s) + P3(0.08, 0.25) for s in np.linspace(0, 1, 40)]).set_stroke(DIM, 2), num_dashes=40)
        pu = always_redraw(lambda: pulga(0.0, 0.6).shift(pos(s_.get_value())))
        # ZOOM dentro do PALCO
        ZX = -1.35
        pz = placa(3.7, 4.9, P3(ZX, -0.45))
        zl = txt("ZOOM", T_SMALL, color=DIM).move_to(P3(ZX, 1.85))
        dados = linha(tex(r"m=2\ \mathrm{mg}", WHITE_, 34), tex(r"d=1\ \mathrm{mm}", WHITE_, 34), buff=0.4)
        ext = ValueTracker(0.0)
        YZ = -2.45
        k = 1.75
        zpu = always_redraw(lambda: pulga(ext.get_value(), k).shift(P3(ZX - 0.25, YZ)))
        chz = Line(P3(ZX - 1.7, YZ), P3(ZX + 1.7, YZ)).set_stroke(GEO, 2, opacity=0.6)
        y0 = YZ + 0.55 * k + 0.33 * k
        zd = DoubleArrow(P3(ZX + 1.35, y0), P3(ZX + 1.35, y0 + 0.26 * k), buff=0, color=GEO, stroke_width=2.5, tip_length=0.1)
        zd_l = tex(r"d", GEO, 30).next_to(zd, RIGHT, buff=0.08)
        self.play(Create(chao), FadeIn(pu), run_time=0.7)
        self.play(GrowFromEdge(regua, DOWN), FadeIn(h_lab), FadeIn(ref), run_time=0.8)
        dados.arrange(DOWN, buff=0.25, aligned_edge=LEFT)
        hq = tex(r"h=50\ \mathrm{cm}", WHITE_, 34)
        pq = txt("FORÇA NO CHÃO ÷ PESO = ?", T_SMALL, color=CYAN)
        conta(hq, dados, pq, topo=1.9, buff=0.3, x0=1.4)
        self.play(FadeIn(pz), FadeIn(zl), FadeIn(chz), FadeIn(zpu), Write(dados), Write(hq), run_time=0.9)
        self.ate(0.25)
        self.play(Create(traj), run_time=0.5)
        self.play(s_.animate.set_value(1.0), run_time=1.6, rate_func=linear)
        self.ate(0.6)
        self.play(ext.animate.set_value(1.0), GrowFromEdge(zd, DOWN), FadeIn(zd_l), run_time=1.3)
        self.play(ext.animate.set_value(0.0), run_time=0.6)
        self.play(ext.animate.set_value(1.0), FadeIn(pq, shift=0.1 * UP), run_time=0.6)
        # o salto se repete devagar no PALCO enquanto a CONTA trabalha
        t0 = self.clk.get_value()
        s_.add_updater(lambda m: m.set_value(((self.clk.get_value() - t0) % 4.0) / 4.0))
        ext.add_updater(lambda m: m.set_value(0.5 - 0.5 * math.cos(2 * PI * (self.clk.get_value() - t0) / 4.0)))
        self.add(s_, ext)
        self.ate(0.97)
        # E5-2 · CAMINHO 1 (distância) em cima; E5-3 · CAMINHO 2 (tempo) embaixo -------------------------------------------
        self.an("E5-2")
        vv = Mc((r"v=\sqrt{2gh}=3{,}13\ \mathrm{m/s}", VEL), size=42)
        t1 = linha(txt("CAMINHO 1", T_SMALL, color=DIM), txt("DISTÂNCIA", T_LAB, bold=True), buff=0.25)
        e1 = Mc("a", "=", r"\frac{v^{2}}{2d}", "=", r"\frac{g\,h}{d}", "=", r"500\,g", size=40)
        f1 = Mc((r"F_{res}", FC), "=", r"m\,a", "=", r"\frac{m\,v^{2}}{2d}", size=40)
        conta(vv, t1, e1, f1, topo=2.3, buff=0.2, x0=1.2)
        self.play(FadeOut(VGroup(hq, dados, pq)), run_time=0.4)
        self.play(Write(vv), run_time=0.9)
        self.ate(0.45)
        self.play(FadeIn(t1), Write(e1), Indicate(zd_l, color=WHITE_, scale_factor=1.5), run_time=1.2)
        print(f"[QA] E5-2 v = {math.sqrt(2 * 9.8 * 0.5):.3f} m/s; a/g = h/d = {0.5 / 0.001:.0f}")
        self.play(Indicate(e1[6], color=WHITE_, scale_factor=1.2), run_time=0.8)
        self.ate(0.88)
        self.play(Write(f1), run_time=0.9)
        self.ate(0.97)
        self.an("E5-3")
        cam1 = VGroup(t1, e1, f1)
        t2 = linha(txt("CAMINHO 2", T_SMALL, color=DIM), txt("TEMPO", T_LAB, color=JC, bold=True), buff=0.25)
        e2 = Mc(r"\Delta t", "=", r"\frac{2d}{v}", "=", r"0{,}64\ \mathrm{ms}", size=40)
        f2 = Mc((r"F_{res}", FC), "=", r"\frac{m\,v}{\Delta t}", "=", r"\frac{m\,v^{2}}{2d}", size=40)
        conta(t2, e2, f2, topo=-0.95, buff=0.2, x0=1.2)
        print(f"[QA] E5-3 Δt = {2 * 0.001 / math.sqrt(2 * 9.8 * 0.5) * 1000:.3f} ms")
        self.play(cam1.animate.set_opacity(0.4), FadeIn(t2), Write(e2), run_time=1.1)
        self.ate(0.4)
        self.play(Write(f2), run_time=0.9)
        self.ate(0.6)
        self.play(cam1.animate.set_opacity(1), run_time=0.3)
        self.play(Indicate(f1[4], color=WHITE_, scale_factor=1.25), Indicate(f2[4], color=WHITE_, scale_factor=1.25), run_time=1.0)
        mesma = legenda("A MESMA FÍSICA PELOS DOIS TEOREMAS", x=-3.0)
        self.play(FadeIn(mesma), run_time=0.5)
        self.ate(0.97)
        # E5-4 · N = m(a + g) = 501 pesos (a pulga continua no PALCO) ------------------------------------------------------
        self.an("E5-4")
        self.play(FadeOut(VGroup(vv, cam1, t2, e2, f2, mesma)), run_time=0.5)
        n1 = Mc((r"N", FC), "=", r"m\,(a+g)", "=", r"m\,g\,\Big(\frac{h}{d}", r"+1\Big)", size=40)
        n2 = Mc((r"N", FC), "=", (r"501\ \mathrm{pesos}", FC), size=60)
        nao = txt("NÃO 500", T_LAB, color=DIM)
        conta(n1, n2, nao, topo=1.9, buff=0.45, x0=1.3)
        self.play(Write(n1), run_time=1.2)
        self.ate(0.4)
        self.play(Indicate(n1[5], color=WHITE_, scale_factor=1.35), run_time=0.9)
        self.play(Indicate(n1[5], color=WHITE_, scale_factor=1.35), run_time=0.9)
        self.play(Write(n2), FadeIn(nao), run_time=0.9)
        cx = caixa(n2, FC, buff=0.22)
        self.play(Create(cx), run_time=0.5)
        self.ate(0.7)
        self.dica_entra(dica(["CONTATO", MathTex(r"\neq", font_size=32), "RESULTANTE"]))
        self.ate(0.97)
        s_.clear_updaters()
        ext.clear_updaters()
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
        self.play(Write(n3), FadeIn(um), FadeIn(pes, shift=0.2 * UP), Create(chao), run_time=1.0)
        self.play(FadeIn(pl), run_time=0.5)
        self.ate(0.35)
        self.play(GrowFromEdge(bloco, DOWN), run_time=0.8)
        self.play(Write(bl), run_time=0.6)
        print(f"[QA] E5-5 N = {2e-6 * 9.8 * 501:.4e} N; 70 kg × 501 = {70 * 501 / 1000:.2f} t")
        self.ate(0.97)

"""Lote PB7 · LAPLACIANO (handoff v2; quadros 22 e 23). B7-1: curvas de nível de φ = x² + y² (círculos azul-claros com os valores, placa) e o gradiente
(2x, 2y) cheio; ∇²φ = ∇·∇φ. B7-2: as contas na coluna; o gradiente vira contexto. B7-3: P = (1, ½), a circunferência tracejada de raio 0,4 e os 8 vizinhos;
φ(P) = 1,25 e 1,41 na coluna (sem barras). B7-4: a chapa 720×720 com o mapa frio → quente pelo núcleo exato do calor, com o tempo esticado (t 0 → 1,5)
ao longo de toda a fala; ∇²T > 0 / ESQUENTA no ponto frio.
v3: clareira em volta dos números das curvas de nível (S16) e na região do P (S17, P abaixo do ponto); B7-4 reescrito (§3.4): gráfico de corte
T(x, 0, t) com o vale, P e os vizinhos, a seta SOBE, e a chapa vista de cima alinhada; 4αt de 0,06 a 0,5 em 6 s."""
from v27 import *  # noqa: F401,F403

V = Vista(600, 540, 120)
PHI = lambda x, y: x * x + y * y


def lbl(s, X, Y, size=34, al="c"):
    x, y = canto_xy(V, X, Y)
    return TP(s, x, y, size, al)


LABS = [(-math.sqrt(v) * 0.72, -math.sqrt(v) * 0.72) for v in (1, 2, 3, 4)]
CL_P = [(0.45, -0.05, 1.6, 1.05)]


def longe_dos_rotulos(X, Y, folga=0.3, meio=0.13):
    """final §2.8: clareira de `folga` u entre a SETA INTEIRA do gradiente (não só o centro) e a placa de cada rótulo 1–4 (meia-caixa `meio` u)."""
    m = math.hypot(2 * X, 2 * Y)
    if m < 1e-9:
        return False
    L = 0.84 * 0.5 * (0.4 + 0.6 * min(1.0, m / 6.0))
    ux, uy = 2 * X / m * L / 2, 2 * Y / m * L / 2
    for a, b in LABS:
        dx, dy = ux * 2, uy * 2
        t = max(0.0, min(1.0, ((a - X + ux) * dx + (b - Y + uy) * dy) / (dx * dx + dy * dy)))
        if math.hypot(X - ux + t * dx - a, Y - uy + t * dy - b) < folga + meio:
            return True
    return False


class LoteB7(Base):
    ANTES = "NA FÍSICA"

    def corpo(self):
        # ── B7-1 ──
        self.an("B7-1")
        self.secao("LAPLACIANO")
        niv = VGroup(*[vcirc(V, math.sqrt(v), SAI, 3) for v in (1, 2, 3, 4)])
        rot_n = VGroup(*[lbl(r"\D{" + str(v) + "}", *LABS[i]) for i, v in enumerate((1, 2, 3, 4))])
        self.play(LaggedStart(*[Create(c) for c in niv], lag_ratio=0.12), run_time=1.0)
        self.gat("uma função que dá um número em cada ponto")
        self.play(LaggedStart(*[FadeIn(r) for r in rot_n], lag_ratio=0.2), run_time=0.8)
        gr = campo7(V, lambda x, y: (2 * x, 2 * y), mmax=6.0, skip=longe_dos_rotulos, nome="B7 gradiente (2x, 2y)")   # S16 / v4 N7: clareira 0,45 u
        self.gat("calcula o gradiente dela")
        self.play(cresce_campo(gr, 1.5))
        fL = TC(r"\nabla^2\phi = \nabla\cdot\nabla\phi", 1120, 330, 52)
        self.gat("o resultado se chama laplaciano")
        self.play(caneta(fL))
        self.ate(0.97)

        # ── B7-2 ──
        self.an("B7-2")
        self.play(UpdateFromAlphaFunc(gr, lambda m_, a: m_.contexto(a > 0.5)), run_time=0.6)
        linhas = [(r"\phi = \X^2 + \Y^2", 450, 46, "a soma dos quadrados"), (r"\nabla\phi = (2\X,\ 2\Y)", 550, 46, "o gradiente dela é uma explosão"),
                  (r"\nabla^2\phi = 2 + 2 = \D{4}", 650, 46, "agora calcula o divergente dessa explosão"), (r"\phi = \X^2 + \Y^2 + \Z^2 \;\Rightarrow\; \nabla^2\phi = \D{6}", 770, 44, "no espaço")]
        fs_ = []
        for s, y, sz, fr in linhas:
            self.gat(fr)
            f = TC(s, 1120, y, sz)
            fs_.append(f)
            self.play(caneta(f))
        self.ate(0.97)

        # ── B7-3 ──
        self.an("B7-3")
        sai73 = [fL, *fs_]                                                          # final: a saída do B7-2 vai junto do φ
        self.remove()
        p = (1.0, 0.5)
        cc = vcirc(V, 0.4, GEO, 2.5, c=p, dash=(6, 6))
        viz = [ponto7(V.c2p(p[0] + 0.4 * math.cos(2 * PI * i / 8), p[1] + 0.4 * math.sin(2 * PI * i / 8)), POS, 6, 10) for i in range(8)]
        pp = ponto7(V.c2p(*p), POS, 10, 11)
        lp = lbl(r"P", 1.0, -0.12, 36)                                  # S17: abaixo do ponto, fora do anel
        clP = esconde(gr, clar(CL_P))
        val = PHI(*p)
        med = float(np.mean([PHI(p[0] + 0.4 * math.cos(a), p[1] + 0.4 * math.sin(a)) for a in np.linspace(0, 2 * PI, 4000, endpoint=False)]))
        print(f"[laplaciano] B7-3: φ(P) = {val:.4f}; média na circunferência de raio 0,4 = {med:.4f}; diferença {med - val:.4f} = ρ²/4·∇²φ = {0.16 / 4 * 4:.4f}")
        f0 = TC(r"\phi = \X^2 + \Y^2", 1120, 300, 50)
        cf0 = caneta(f0, atraso=0.3)                                         # R6: as contas do B7-2 saem antes do 1º glifo
        self.play(*[FadeOut(m_, rate_func=so_no_inicio(cf0, 0.28)) for m_ in sai73], some(clP), FadeIn(pp, scale=0.5), FadeIn(lp), cf0)
        self.remove(*sai73)                       # final: φ entra no começo da âncora
        self.gat("ele compara o valor da função num ponto")
        self.play(FadeIn(legenda("VALOR NO PONTO", 1124, 420, POS)), caneta(TC(r"\phi(P) = 1{,}25", 1450, 410, 46)))
        self.gat("com a média dos vizinhos")
        self.play(Create(cc), LaggedStart(*[FadeIn(d, scale=0.4) for d in viz], lag_ratio=0.18), run_time=1.4)
        self.play(FadeIn(legenda("MÉDIA EM VOLTA", 1124, 520, POS)), caneta(TC(r"1{,}41", 1450, 510, 46)))
        self.gat("laplaciano positivo")
        self.play(caneta(TC(r"1{,}25 < 1{,}41", 1120, 640, 46)))
        self.play(caneta(TC(r"\nabla^2\phi = \nabla\cdot\nabla\phi = 4 > 0", 1120, 770, 48)), FadeIn(legenda("ABAIXO DA MÉDIA DOS VIZINHOS", 1124, 870)))
        self.ate(0.97)

        # ── B7-4 · calor (handoff v3 §3.4; alvos 08 e 09): gráfico de corte com o vale e a chapa vista de cima, na mesma escala em x ──
        self.an("B7-4")
        S2 = 0.36                                                       # σ²; tt = 4αt vai de 0,06 a 0,5
        TT = lambda X, Y, tt: 1 - (S2 / (S2 + tt)) * np.exp(-(X * X + Y * Y) / (S2 + tt))
        GX, GY = (lambda X: 560 + X * 150), (lambda Tv: 640 - Tv * 330)
        H_ = 0.75
        tt = ValueTracker(0.06)
        # chapa vista de cima (px 170–950 × 720–900), mapa #4F8CFF → #F09A4A
        X0, X1, Y0, Y1 = GX(-2.6), GX(2.6), 720, 900
        NW, NH = 390, 90
        cf, cq = np.array([0x4F, 0x8C, 0xFF], float), np.array([0xF0, 0x9A, 0x4A], float)
        XX = ((X0 + (np.arange(NW) + 0.5) * (X1 - X0) / NW) - 560) / 150
        YY = ((Y0 + Y1) / 2 - (Y0 + (np.arange(NH) + 0.5) * (Y1 - Y0) / NH)) / 150
        XM, YM = np.meshgrid(XX, YY)

        def chapa_px(t_):
            Tm = TT(XM, YM, t_)
            rgb = cf[None, None, :] + (cq - cf)[None, None, :] * Tm[..., None]
            return np.concatenate([rgb, np.full((NH, NW, 1), 255.0)], 2).astype(np.uint8)
        mapa = ImageMobject(chapa_px(0.06)).set_resampling_algorithm(RESAMPLING_ALGORITHMS["linear"])
        mapa.stretch_to_fit_width((X1 - X0) / 120).stretch_to_fit_height((Y1 - Y0) / 120).move_to(PX((X0 + X1) / 2, (Y0 + Y1) / 2)).set_z_index(1)
        borda = linha7([PX(X0, Y0), PX(X1, Y0), PX(X1, Y1), PX(X0, Y1), PX(X0, Y0)], GEO, 2.5)
        corte = linha7([PX(X0, (Y0 + Y1) / 2), PX(X1, (Y0 + Y1) / 2)], BR, 2, 0.7, dash=(8, 8))
        lch = legenda("CHAPA VISTA DE CIMA", X0, Y0 - 18, GEO)
        esc = Rectangle(width=260 / 120, height=16 / 120).set_stroke(width=0).set_fill(color=[ManimColor("#4F8CFF"), ManimColor("#F09A4A")], opacity=1)
        esc.set_sheen_direction(RIGHT).move_to(PX(X0 + 90 + 130, 956))
        esc._sem_contorno = True
        lfr, lqu = T("FRIO", X0, 966, 26, "left", "#7FA8FF", bold=False), T("QUENTE", X0 + 364, 966, 26, "left", "#F09A4A", bold=False)
        self.grade()                                                          # final: o gráfico de corte e a chapa ficam no violeta liso (escalas x e T diferentes)
        sai = self.snap()                                                     # v4 N8: o B7-3 sai INTEIRO primeiro
        self.play(*[FadeOut(m_) for m_ in sai], run_time=0.5)
        self.remove(*sai)
        # gráfico do corte
        eixos = linha7([PX(GX(-2.6), GY(1.15)), PX(GX(-2.6), GY(0)), PX(GX(2.75), GY(0))], GEO, 2.5, 0.8)
        lx, lT = TC(r"\X", GX(2.9), GY(0), 40, "c", caneta=False), TC(r"\T", GX(-2.6), GY(1.25), 40, "c", caneta=False)
        lx._esc = lT._esc = True
        xs = np.linspace(-2.6, 2.6, 301)

        def pts_curva(t_):
            return [PX(GX(x_), GY(TT(x_, 0, t_))) for x_ in xs]
        curva = VMobject().set_points_smoothly(pts_curva(0.06)).set_stroke(BR, 5 / 1.2).set_fill(opacity=0).set_z_index(5)
        curva._sem_contorno = True
                                                                              # o gráfico entra logo (sem tela vazia) e, 0,3 s depois, a chapa embaixo dele
        chapa = Group(mapa, borda, corte, lch, esc, lfr, lqu)
        self.play(Create(eixos), FadeIn(lx), FadeIn(lT), Create(curva), FadeIn(chapa, rate_func=lambda a: smooth(max(0.0, (a * 1.2 - 0.3) / 0.9))), run_time=1.2)
        mapa.add_updater(lambda m_: setattr(m_, "pixel_array", chapa_px(tt.get_value())))   # depois do FadeIn (o updater repõe o alfa da imagem)
        curva.add_updater(lambda m_: m_.set_points_smoothly(pts_curva(tt.get_value())))
        # P e os vizinhos
        T0f, T1f = (lambda: TT(0, 0, tt.get_value())), (lambda: TT(H_, 0, tt.get_value()))
        seg = always_redraw(lambda: linha7([PX(GX(-H_), GY(T1f())), PX(GX(H_), GY(T1f()))], GEO, 3, dash=(9, 8)).set_z_index(5))
        vz = VGroup(ponto7(PX(GX(-H_), GY(T1f())), GEO, 9, 9), ponto7(PX(GX(H_), GY(T1f())), GEO, 9, 9))
        vz.add_updater(lambda m_: [d.move_to(PX(GX(s * H_), GY(T1f()))) for d, s in zip(m_, (-1, 1))])
        pP = ponto7(PX(GX(0), GY(T0f())), POS, 11, 10)
        pP.add_updater(lambda m_: m_.move_to(PX(GX(0), GY(T0f()))))
        lmv = segue(T("MÉDIA DOS VIZINHOS", GX(H_) + 24, GY(T1f()) + 10, 26, "left", GEO, bold=False), lambda: (GX(H_) + 24, GY(T1f()) + 10))
        u_ = lambda: (tt.get_value() - 0.06) / 0.44                     # 0 no alvo 08, 1 no alvo 09

        def pos_P():
            u = u_()
            return (GX(0) - 34 * (1 - u) - 6 * u, GY(T0f()) + 6 * (1 - u) + 44 * u)
        lP = segue(TP(r"\Pt{P}", *pos_P(), 36), pos_P)
        self.gat("abaixo da média dos vizinhos")
        self.play(FadeIn(vz), FadeIn(seg), FadeIn(pP, scale=0.5), FadeIn(lP), FadeIn(lmv), run_time=0.7)

        def seta_sobe():
            ya, yb = GY(T0f()) - 16, GY(T1f()) + 14
            s_ = seta7(PX(GX(0), ya), PX(GX(0), min(yb, ya - 2)), POS, 6, 22).set_z_index(6)
            if ya - yb <= 30:
                s_.set_opacity(0)
            return s_
        sb = always_redraw(seta_sobe)

        def pos_S():                                                          # pedido do Kaio: SOBE fora da curva, logo acima da linha da média,
            return (GX(0), GY(T1f()) - 14)                                    # centrado sobre a seta (ali a curva não passa: acima da média ela só
        lS = segue(T("SOBE", *pos_S(), 30, "center", POS, bold=True), pos_S)  # existe fora dos dois vizinhos)
        fS = TC(r"\nabla^2 \T > 0 \;\Rightarrow\; \T\ \text{sobe}", 1120, 580, 48)
        lA = legenda("ABAIXO DA MÉDIA DOS VIZINHOS: ESQUENTA", 1124, 680, POS)
        self.play(caneta(fS), self.em("o laplaciano é positivo", pulso(pP, 1.4, run_time=0.6)))      # final: a fórmula começa logo depois do ponto
        self.gat("esquenta")
        self.play(FadeIn(sb), FadeIn(lS), FadeIn(lA), run_time=0.6)
        # o vale se enche: 4αt de 0,06 a 0,5 em 6 s (pelo relógio, para as falas seguintes seguirem)
        antes = VMobject().set_points_smoothly(pts_curva(0.06)).set_stroke(GEO, 3 / 1.2, 0.55).set_fill(opacity=0)
        antes = DashedVMobject(antes, num_dashes=90, dashed_ratio=10 / 19).set_z_index(4)
        lan = T("ANTES", GX(0.42), GY(0.06) + 8, 26, "left", GEO, bold=False)
        for m_ in (*antes.get_family(), *lan.get_family()):
            m_._sem_contorno = True
        self.gat("vai se enchendo")
        t_ini, RT = self.clk.get_value(), 6.0
        print(f"[calor] B7-4: T(0) {TT(0, 0, 0.06):.3f} → {TT(0, 0, 0.5):.3f}; média dos vizinhos (x = ±0,75) {TT(H_, 0, 0.06):.3f} → {TT(H_, 0, 0.5):.3f}; "
              f"∇²T(0) = 4σ²/s² > 0 ({4 * S2 / (S2 + 0.06) ** 2:.2f} → {4 * S2 / (S2 + 0.5) ** 2:.2f}); 4αt em {RT:.0f} s")
        mot = VMobject()
        mot.add_updater(lambda m_: tt.set_value(0.06 + 0.44 * suave(min(1.0, (self.clk.get_value() - t_ini) / RT))))
        self.add(mot)
        self.play(FadeIn(antes), FadeIn(lan), run_time=0.6)
        fC = TC(r"\dfrac{\partial \T}{\partial t} = \alpha\,\nabla^2 \T", 1120, 340, 58)
        self.gat("equação do calor")
        self.play(caneta(fC), FadeIn(legenda("EQUAÇÃO DO CALOR", 1124, 450)))
        self.gat("e ele volta nas ondas")
        self.play(FadeIn(legenda("E TAMBÉM: ONDAS, POTENCIAL ELÉTRICO…", 1124, 800, GEO)), run_time=0.5)
        if self.clk.get_value() - t_ini < RT:
            self.wait(RT - (self.clk.get_value() - t_ini))
        print(f"[calor] B7-4: 4αt final = {tt.get_value():.3f}")
        mot.clear_updaters()
        self.remove(mot)
        self.ate(0.97)
        self.sai_fim()

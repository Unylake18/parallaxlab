"""yt_0031 · B9 · num exercício (alvos 28 e 29)."""
from v31 import *


def arr_funcao(L, fn, dom):
    """mapa L×L de fn(a, b) ∈ [0, 1] na rampa RAMP0 → CI; dom(a, b) → máscara (alfa)."""
    t = (np.arange(L) + 0.5) / L * 2 - 1
    A, B = np.meshgrid(t, -t)
    v = np.clip(fn(A, B), 0, 1)[..., None]
    rgb = hx(RAMP0) * (1 - v) + hx(CI) * v
    alfa = np.where(dom(A, B), 255, 0)[..., None]
    return np.concatenate([rgb, alfa], 2)


class PB9(B31):
    ANTES = "NUM EXERCÍCIO"          # v2 (G2): a linha 2 do canto já está na tela no 1º quadro do bloco

    def corpo(self):
        # ── B9-1 · o teste em três perguntas (alvo 28) ──────────────────────────────────────────────
        self.an("B9-1")
        # v2 (alvo 28 v2): chips numerados, um por pergunta; o 1º chip começa a nascer no 1º quadro (G2)
        chips, X = [], 180
        for c, fr in zip(["1 · LIMITADA?", "2 · DESCONTINUIDADES: NULO?", "3 · FRONTEIRA: NULO?"], ["a função é limitada", "as descontinuidades ficam", "a fronteira dela tem"]):
            w = txt(c, ts(28), up=False).width * 120 + 48
            chips.append((caixa_px(X, 150, w, 56, GEO, 2, .5, 10), leg(c, X + 24, 188, BR, "left", 28), fr))
            X += w + 30
        # a chapa do B8-2 (com a grade) está na tela no 1º quadro e sai quando a 1ª pergunta é escrita
        ch8 = img_chapa(__import__("sec_b8").arr_racionais())
        bv8 = borda_ch(CH, AL, 4, z=6)
        self.grade = papel(CH).set_z_index(-10)
        self.add(self.grade, ch8, bv8)
        # v3 (alvo 28a): cada pergunta entra grande, no centro, numa moldura; em "Os exemplos do livro passam nas três" as molduras
        # sobem e encolhem até virar os chips do topo (o texto é o mesmo) e o cartão 1 entra
        teste = leg("O TESTE DO TEOREMA", 960, 300, GEO, "center", 30)
        self.gat("num exercício o teorema")          # v3: a chapa sai antes do título entrar (o título não cruza a borda que sai)
        self.play(FadeOut(ch8), FadeOut(bv8), FadeOut(self.grade), run_time=0.5)
        self.remove(ch8, bv8, self.grade)
        self.grade = None
        self.pena(teste, rt=0.8)                       # final: o título entra logo depois da chapa (palco vazio ≤ 0,5 s)
        grandes = []
        for k, (cx_, tt, fr) in enumerate(chips):
            Yq = 430 + k * 110
            tb = T(tt._txt, 960, Yq + 6, 44, "center")
            wq = tb.width * 120 + 80
            fb = caixa_px(960 - wq / 2, Yq - 50, wq, 80, GEO, 2.5, .6, 14)
            self.gat(fr)
            self.pena(tb, extra=[Create(fb)], rt=0.8)
            grandes.append((fb, tb))
        self.marca("28a", agora=True, dt=0.6)
        cards = [(100, 240), (980, 240), (100, 640), (980, 640)]
        pns = [painel(X0, Y0, 840, 370) for X0, Y0 in cards]
        # os ✓ de cada cartão ficam sob os números 1 2 3 (alinhados com os chips)
        cks = [[check_px(X0 + 620 + k * 60, Y0 + 336, MEN, .8) for k in range(3)] for X0, Y0 in cards]
        nums = [[leg(str(k + 1), X0 + 620 + k * 60, Y0 + 300, GEO, "center", 24) for k in range(3)] for X0, Y0 in cards]
        # ex. 3: x + y no disco
        d3 = img_px(arr_funcao(300, lambda a, b: (a + b + 1.42) / 2.84, lambda a, b: a * a + b * b <= 1), 150, 275, 300, 300, z=2)
        c3 = circ_px(300, 425, 150, BR, 3)
        self.gat("os exemplos do livro passam")
        # final §7: as molduras viram chips sem se cruzar — (1) encolhem e andam na horizontal até o x do chip, cada uma na própria linha,
        # enquanto o título sai; (2) sobem juntas (colunas disjuntas); (3) só então o cartão 1 entra
        f1_, f2_ = [], []
        for (fb, tb), (cx_, tt, _) in zip(grandes, chips):
            tt._esc = True
            dy = fb.get_center()[1] - cx_.get_center()[1]
            fm, tm = cx_.copy().shift(UP * dy), tt.copy().shift(UP * dy)
            tm._esc = True
            f1_ += [ReplacementTransform(fb, fm), ReplacementTransform(tb, tm)]
            f2_ += [ReplacementTransform(fm, cx_), ReplacementTransform(tm, tt)]
        self.play(*f1_, FadeOut(teste), run_time=0.5)
        self.remove(teste)
        self.play(*f2_, run_time=0.45)
        self.play(FadeIn(pns[0]), FadeIn(d3), Create(c3), run_time=0.4)
        for _, tt, _ in chips:
            self.origem(tt, "moldura grande → chip (ReplacementTransform)")
        self.gat("xis mais ípsilon no disco")
        f3 = TC(r"\X+\Y\ \text{no disco}\ \X^2+\Y^2\le 1", 500, 330, 30)
        self.pena(f3, *nums[0], rt=1.2)
        self.gat("contínua e a fronteira é uma")
        l3 = leg("CONTÍNUA · CIRCUNFERÊNCIA", 500, 400, GEO, "left", 24)
        self.pena(l3, extra=[Create(cks[0][0]), Create(cks[0][1])], rt=0.8)
        self.gat("é uma circunferência")
        self.play(Create(cks[0][2]), run_time=0.4)
        # ex. 4: entre as parábolas
        self.gat("xis mais ípsilon entre")
        v4 = Vw(1200, 560, 95)
        reg = [v4.px(a, a * a) for a in np.linspace(-1, 1, 41)] + [v4.px(a, 1 + a * a) for a in np.linspace(1, -1, 41)]
        p4 = poly_px(reg, mixh(BG_, CI, .45), z=2)
        o4 = lin_px(reg + reg[:1], BR, 3, z=3)
        f4 = TC(r"\X+\Y\ \text{entre}\ \Y=\X^2\ \text{e}\ \Y=1+\X^2", 1320, 330, 28)
        self.play(FadeIn(pns[1]), FadeIn(p4), Create(o4), run_time=0.8)
        self.pena(f4, *nums[1], rt=1.2)
        self.gat("a fronteira são dois")
        l4 = leg("2 GRÁFICOS + 2 SEGMENTOS", 1380, 400, GEO, "left", 24)
        self.pena(l4, extra=[Create(cks[1][0]), Create(cks[1][1])], rt=0.8)
        self.gat("e dois segmentos no")
        self.play(Create(cks[1][2]), run_time=0.4)
        # ex. 5: ±1 no disco
        self.gat("no disco a função que vale")
        cima = sem_ctn(Sector(radius=150 / 120, start_angle=0, angle=PI).move_arc_center_to(PX(300, 825)).set_fill(PESADO, 1).set_stroke(width=0)).set_z_index(2)
        baixo = sem_ctn(Sector(radius=150 / 120, start_angle=PI, angle=PI).move_arc_center_to(PX(300, 825)).set_fill(LEVE, 1).set_stroke(width=0)).set_z_index(2)
        sg = lin_px([(150, 825), (450, 825)], BR, 4, z=4)
        u1, um = TP("1", 300, 760, 30), TP("-1", 300, 890, 30)
        f5 = TC(r"\f=\pm 1\ \text{no disco}", 500, 730, 30)
        self.play(FadeIn(pns[2]), FadeIn(cima), FadeIn(baixo), run_time=0.7)
        self.play(Create(sg), run_time=0.5)
        self.pena(u1, um, f5, *nums[2], rt=1.2)
        self.gat("uma chapa de dois metais")
        l5 = leg("SALTA NUM SEGMENTO", 500, 800, GEO, "left", 24)
        self.pena(l5, extra=[Create(cks[2][0]), Create(cks[2][1])], rt=0.8)
        self.gat("com solda reta")
        self.play(Create(cks[2][2]), run_time=0.4)
        # ex. 6: x²/(x² + y²)
        self.gat("e xis ao quadrado sobre")
        d6 = img_px(arr_funcao(280, lambda a, b: a * a / np.maximum(a * a + b * b, 1e-9), lambda a, b: np.ones_like(a, bool)), 1040, 685, 280, 280, z=2)
        b6 = lin_px([(1040, 685), (1320, 685), (1320, 965), (1040, 965), (1040, 685)], BR, 2, z=3)
        o6 = ponto_px(1180, 825, POS, 7)
        f6 = TC(r"\dfrac{\X^2}{\X^2+\Y^2},\ \ \f(0,0)=1", 1380, 740, 30)
        self.play(FadeIn(pns[3]), FadeIn(d6), Create(b6), FadeIn(o6), run_time=0.8)
        self.pena(f6, *nums[3], rt=1.2)
        self.gat("valendo um na origem")
        self.play(Create(cks[3][0]), run_time=0.4)
        self.gat("só é descontínua na origem")
        l6 = leg("SÓ SALTA NA ORIGEM", 1380, 810, GEO, "left", 24)
        self.pena(l6, extra=[Create(cks[3][1])], rt=0.8)
        self.gat("e um ponto tem")
        self.play(Create(cks[3][2]), run_time=0.4)
        self.gat("as quatro são")
        q4 = T("AS QUATRO SÃO INTEGRÁVEIS", 960, 1050, 30, "center", MEN)
        self.pena(q4)
        self.marca("28", agora=True)

        # ── B9-2 · por que isso importa (alvo 29) ───────────────────────────────────────────────────
        self.an("B9-2")
        velhos = self.snap()
        Xs = [140, 720, 1300]
        pn = [painel(X0, 230, 480, 440) for X0 in Xs]
        v1 = Vw(240, 600, 140)
        m1 = Group(img_chapa(arr_metais_liso(280), v1), borda_ch(v1, GEO, 2), solda_px(v1, BR, 3))
        v2 = Vw(800, 600, 140)
        dv = [v2.px(1.1 + .15 * math.sin(6 * t), 2 * t) for t in np.linspace(0, 1, 31)]
        e2 = poly_px([v2.px(0, 0)] + dv + [v2.px(0, 2)], mixh(BG_, CI, .35), z=1)
        d2 = poly_px([v2.px(2, 0)] + dv + [v2.px(2, 2)], mixh(BG_, CI, .8), z=1)
        m2 = Group(e2, d2, lin_px(dv, BR, 3, z=4), borda_ch(v2, GEO, 2))
        m3 = circ_px(1540, 450, 140, BR, 3, fill=mixh(BG_, CI, .6), fop=1, z=2)
        tits = [T(t, X, 730, 30, "center") for X, t in ((380, "DOIS MATERIAIS"), (960, "DIVISA NO MAPA"), (1540, "ALVO REDONDO"))]
        subs = [leg(t, X, 780, CI, "center", 26) for X, t in ((380, "MASSA"), (960, "POPULAÇÃO"), (1540, "PROBABILIDADE"))]
        self.play(*[FadeOut(m_, scale=0.6) for m_ in velhos], *[FadeIn(p_) for p_ in pn], FadeIn(m1), run_time=0.8)
        self.remove(*velhos)
        for k, (fr, m) in enumerate(zip(["uma peça feita", "a densidade de população", "a probabilidade espalhada"], [m1, m2, m3])):
            self.gat(fr)
            if k:
                self.play(FadeIn(m), run_time=0.6)
            self.pena(tits[k], subs[k], lag=0.4)
        self.gat("mas são limitadas")
        o1 = T("OS SALTOS MORAM EM CURVAS", 960, 900, 40, "center")
        self.pena(o1)
        self.gat("então a integral existe")
        o2 = leg("CURVAS TÊM CONTEÚDO NULO → A INTEGRAL EXISTE", 960, 960, GEO, "center", 26)
        self.pena(o2)
        self.marca("29")
        self.sai_fim()

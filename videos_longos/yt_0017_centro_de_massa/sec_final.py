"""Lote P5 (handoff v4, lote 3): E1, E2, síntese, encerramento. Regra G19 nos exercícios: ESQUEMA fixo à esquerda (~45%), CONTA à direita;
tudo que entra na conta sai do esquema. Céu dos exercícios com metade das estrelas (fundo_lab_ex.png); a síntese volta ao céu do vídeo.
E1 placa de 1 m com o triângulo de cima recortado: três triângulos (centroide na média dos vértices) → 7/18 m; massa negativa → o mesmo
ponto (o ⊕ não pula); FOGE DO FURO; desafio do disco (sem resposta) · E2 remador (75 kg) e canoa (150 kg, 3 m): ⊕ parado em 2 m; canoa
+1,0 m; faltam 20 cm · S1 a granada de novo no campo de provas · S2 as quatro perguntas · EN1 inscrição · EN2 a cena C04 do vídeo de
colisões (exemplo-base 2 kg a +2 m/s e 1 kg a −2 m/s, grudam a +⅔ m/s) com o ⊕ andando reto a ⅔ m/s antes, durante e depois da batida;
v_f = … = V_cm · EN3 três prévias (placa com furo, fio no cubo em Three.js, gafanhoto) e PRÓXIMO VÍDEO."""
from MF_Tools import TransformByGlyphMap

from camadas import *  # noqa: F401,F403
from sec_t4 import barra_aco


def mp(m, idx, partes):
    return VGroup(*[m[0][j] for k in partes for j in idx[k]])


J = lambda idx, *ks: [j for k in ks for j in idx[k]]
F = lambda a, b: rf"\tfrac{{{a}}}{{{b}}}"


class Cubo3D:
    """Fio de aço dobrado em três arestas de um cubo de 1 m (x, depois y, depois z); a câmera gira em volta. ⊕ em (5/6; 1/2; 1/6)."""
    CM = (5 / 6, 1 / 2, 1 / 6)

    def __init__(self, cena, K=2.1, xc=0.0, yc=0.0, op=0.0):
        self.cena, self.K, self.xc, self.yc = cena, K, xc, yc
        self.az = ValueTracker(-55.0)
        self.f3d = Fundo3D(cena, "cubo", self.estado, op=op)

    def cam(self):
        return cam_obl(self.az.get_value(), 24.0, (0.5, 0.5, 0.5), K=self.K, xc=self.xc, yc=self.yc, fov=16)

    def estado(self, t):
        return r4({"cubo": 1, "cam": self.cam()})

    def p(self, q):
        return projeta3d(self.f3d.e["cam"], q)


class LoteFinal(Camadas):
    FUNDO = "fundo_lab_ex.png"

    def construct(self):
        self.setup_base(cap="EXERCÍCIO 1 · PLACA COM ENTALHE", selo="POR PARTES: CADA PEDAÇO VIRA UMA PARTÍCULA")
        self.e1()
        self.e2()
        self.sintese()
        self.encerramento()
        self.fim()
        self.relatorio()
        self.gravar_reg()

    # ════════════════════════════════════════ E1 — placa com entalhe ════════════════════════════════════════
    def e1(self):
        S, O = 4.2, P3(-6.35, -2.75)
        Pw = lambda x, y: O + S * P3(x, y)
        self.Pw = Pw
        G, X_ = GEO, CMC
        # ── E1-1 ──
        self.an("E1-1")
        sobra = Polygon(Pw(0, 0), Pw(1, 0), Pw(1, 1), Pw(0.5, 0.5), Pw(0, 1))
        sobra.set_fill(["#9AA6B8", "#7A8696", "#3A4252"], 1).set_sheen_direction(UP).set_stroke("#7FB2FF", 2, opacity=0.7)
        sobra._degrade = "aco"
        tri = Polygon(Pw(0, 1), Pw(1, 1), Pw(0.5, 0.5)).set_fill(["#9AA6B8", "#7A8696"], 1).set_sheen_direction(UP).set_stroke("#7FB2FF", 2, opacity=0.7)
        tri._degrade = "aco"
        vazio = DashedVMobject(Polygon(Pw(0, 1), Pw(1, 1), Pw(0.5, 0.5)).set_stroke(WHITE_, 2.2, opacity=0.7), num_dashes=36, dashed_ratio=0.55)
        ax = VGroup(Line(O + 0.3 * LEFT, O + (S + 0.55) * RIGHT).set_stroke(G, 2, opacity=0.8), Line(O + 0.3 * DOWN, O + (S + 0.55) * UP).set_stroke(G, 2, opacity=0.8),
                    mtex("x", G, 36).next_to(O + (S + 0.55) * RIGHT, DOWN, buff=0.12), mtex("y", G, 36).next_to(O + (S + 0.55) * UP, LEFT, buff=0.12))
        nt_ = lambda v: mtex(F(1, 2), G, 36) if v < 1 else rot("1", 30, G)
        for v in (0.5, 1):
            ax.add(Line(Pw(v, 0) + 0.09 * DOWN, Pw(v, 0) + 0.09 * UP).set_stroke(G, 2), nt_(v).next_to(Pw(v, 0), DOWN, buff=0.16),
                   Line(Pw(0, v) + 0.09 * LEFT, Pw(0, v) + 0.09 * RIGHT).set_stroke(G, 2), nt_(v).next_to(Pw(0, v), LEFT, buff=0.16))
        ax.set_z_index(-1)
        self.play(FadeIn(ax), FadeIn(sobra), FadeIn(tri), run_time=0.8)
        self.ate(0.15)
        self.play(tri.animate.shift(0.9 * UP).set_opacity(0.0), Create(vazio), run_time=1.2)      # "recortou um triângulo em cima"
        self.remove(tri)
        sim = DashedLine(Pw(0.5, 0.0), Pw(0.5, 1.0), dash_length=0.1).set_stroke(WHITE_, 2, opacity=0.6)
        Xe, ix = eqp("X", "=", F(1, 2), r"\ \mathrm{m}", size=52, cores={0: X_})
        na_conta(Xe, 1.8)
        ps = txt("POR SIMETRIA", 28).next_to(Xe, RIGHT, buff=0.35)
        Ye, iy = eqp("Y", "=", "?", size=52, cores={0: X_})
        na_conta(Ye, 0.75)
        self.ate(0.5)
        self.play(Create(sim), run_time=0.8)
        self.play(FadeIn(Xe), FadeIn(ps), run_time=0.7)
        self.ate(0.72)
        self.play(FadeIn(Ye), run_time=0.6)
        self.ate(0.88)
        self.play(Indicate(Ye, color=WHITE_, scale_factor=1.15), run_time=0.8)                     # "e dá para fazer de dois jeitos"
        self.ate(0.97)
        # ── E1-2: três triângulos ──
        self.an("E1-2")
        tris = [((0, 0), (1, 0), (0.5, 0.5)), ((0, 0), (0.5, 0.5), (0, 1)), ((1, 0), (1, 1), (0.5, 0.5))]
        bordas = (BLUE_L, GEO, JC)
        pecas = VGroup(*[Polygon(*[Pw(*v) for v in t_]).set_fill(["#9AA6B8", "#3A4252"], 0.9).set_sheen_direction(UP).set_stroke(c_, 3.2)
                         for t_, c_ in zip(tris, bordas)])
        for p_ in pecas:
            p_._degrade = "aco"
        cents = [np.mean(np.array(t_), axis=0) for t_ in tris]                                    # (½; ⅙), (⅙; ½), (⅚; ½)
        quartos = VGroup(*[mtex(F(1, 4), WHITE_, 40).move_to(Pw(*c_) + (P3(0.42, -0.28) if k == 0 else P3(0, -0.45))) for k, c_ in enumerate(cents)])
        self.play(FadeOut(sobra), FadeIn(pecas), run_time=0.8)
        self.ate(0.1)
        self.play(FadeIn(quartos), run_time=0.6)                                                  # "um quarto da área"
        self.ate(0.2)
        for k, t_ in enumerate(tris):                                                              # os vértices piscam; o centroide nasce na média
            vs = VGroup(*[Dot(Pw(*v), radius=0.08, color=bordas[k]) for v in t_])
            self.play(FadeIn(vs, scale=1.6), run_time=0.35)
            self.play(*[d_.animate.move_to(Pw(*cents[k])).scale(0.6) for d_ in vs], run_time=0.55)
            self.remove(vs)
            self.add(Dot(Pw(*cents[k]), radius=0.06, color=bordas[k]))
        coords = VGroup(mtex(rf"({F(1, 2)};\ {F(1, 6)})", G, 36).next_to(Pw(*cents[0]), RIGHT, buff=0.32),
                        mtex(rf"({F(1, 6)};\ {F(1, 2)})", G, 36).next_to(Pw(*cents[1]), UP, buff=0.25),
                        mtex(rf"({F(5, 6)};\ {F(1, 2)})", G, 36).next_to(Pw(*cents[2]), UP, buff=0.25))
        # as placas somem, ficam as três partículas de massa ¼
        parts = VGroup(*[esfera_aco(0.17).move_to(Pw(*c_)) for c_ in cents])
        self.ate(0.42)
        self.play(FadeOut(pecas), FadeIn(parts), FadeIn(coords), *[q_.animate.next_to(p_, LEFT if k == 0 else RIGHT, buff=0.1) for k, (q_, p_) in enumerate(zip(quartos, parts))],
                  run_time=0.9)   # as coordenadas só entram sem as bordas das peças
        A, ia = eqp("Y", "=", r"\Big(", F(1, 4), r"\cdot", F(1, 6), "+", F(1, 4), r"\cdot", F(1, 2), "+", F(1, 4), r"\cdot", F(1, 2), r"\Big)", "/", F(3, 4),
                    size=46, cores={0: X_, 5: G, 9: G, 13: G})
        na_conta(A, 0.75, x0=1.25)
        self.ate(0.5)
        self.play(FadeOut(Ye), FadeIn(mp(A, ia, [0, 1, 2, 4, 6, 8, 10, 12, 14, 15, 16])),
                  *[TransformFromCopy(quartos[k], mp(A, ia, [3 + 4 * k])) for k in range(3)],
                  TransformFromCopy(coords[0][0][3:6], mp(A, ia, [5])), TransformFromCopy(coords[1][0][1:4], mp(A, ia, [9])),
                  TransformFromCopy(coords[2][0][5:8], mp(A, ia, [13])), run_time=1.5)
        B, ib = eqp("=", r"\big(", F(1, 6), "+", F(1, 2), "+", F(1, 2), r"\big)", "/", "3", size=48)
        B.move_to(P3(XC0 + 0.55 + B.width / 2, -0.3))
        self.ate(0.62)                                                                              # "as três massas são iguais"
        self.play(TransformByGlyphMap(A.copy(), B, (J(ia, 1), J(ib, 0)), (J(ia, 2), J(ib, 1)), (J(ia, 5), J(ib, 2)), (J(ia, 6), J(ib, 3)), (J(ia, 9), J(ib, 4)),
                                      (J(ia, 10), J(ib, 5)), (J(ia, 13), J(ib, 6)), (J(ia, 14), J(ib, 7)), (J(ia, 15), J(ib, 8)),
                                      (J(ia, 0, 3, 4, 7, 8, 11, 12, 16), []), ([], J(ib, 9)), auto_fade=True), run_time=1.5)   # o ¼ comum cancela
        C, ic = eqp("=", r"\tfrac{7/6}{3}", r"=\ ", F(7, 18), r"\ \mathrm{m}", r"\approx", r"0{,}39\ \mathrm{m}", size=48, cores={3: X_, 6: X_})
        C.move_to(P3(XC0 + 0.55 + C.width / 2, -1.35))
        self.ate(0.72)
        self.play(FadeIn(C, shift=0.1 * DOWN), run_time=0.9)
        bx = caixa(mp(C, ic, [3, 4]), cor=X_)
        Y7 = 7 / 18
        cm = self.cm_e1 = marcador_cm(Pw(0.5, Y7))
        self.ate(0.78)
        self.play(FadeIn(bx), FadeIn(cm, scale=1.5), run_time=0.7)
        meio = Dot(Pw(0.5, 0.5), radius=0.05, color=WHITE_)
        nota = txt("ABAIXO DO MEIO", 26).next_to(Pw(0.5, Y7), RIGHT, buff=0.55)
        self.ate(0.88)
        self.play(FadeIn(meio), FadeIn(nota), run_time=0.7)                                       # "ficou abaixo do meio"
        self.ate(0.97)
        # ── E1-3: massa negativa ──
        self.an("E1-3")
        sq = Square(S).move_to(Pw(0.5, 0.5)).set_fill(["#9AA6B8", "#3A4252"], 0.55).set_sheen_direction(UP).set_stroke(X_, 3)
        sq._degrade = "aco"
        neg = DashedVMobject(Polygon(Pw(0, 1), Pw(1, 1), Pw(0.5, 0.5)).set_stroke(escuro(MAG, 0.35), 3.5), num_dashes=36, dashed_ratio=0.6)
        negf = Polygon(Pw(0, 1), Pw(1, 1), Pw(0.5, 0.5)).set_stroke(width=0).set_fill(escuro(MAG, 0.55), 0.35)
        lneg = txt("MASSA −¼", 26, color=mix(MAG, 0.2)).move_to(Pw(0.5, 1) + P3(0, 0.42))
        p_sq = VGroup(esfera_aco(0.2).move_to(Pw(0.5, 0.5)), mtex("1", WHITE_, 40).next_to(Pw(0.5, 0.5), RIGHT, buff=0.45).shift(0.15 * UP))
        p_tr = VGroup(Dot(Pw(0.5, 5 / 6), radius=0.07, color=mix(MAG, 0.2)), mtex(F(5, 6), G, 36).next_to(Pw(0.5, 5 / 6), RIGHT, buff=0.2))
        velhos = VGroup(parts, quartos, coords, A, B, *self.mobjects_dots(), meio, nota)
        self.play(FadeOut(velhos), VGroup(C, bx).animate.set_opacity(0.0), FadeIn(sq), cm.animate.set_opacity(0.0), VGroup(Xe, ps).animate.shift(0.65 * UP), run_time=0.8)
        self.remove(C, bx)
        self.ate(0.1)
        self.play(FadeIn(p_sq), run_time=0.6)                                                     # "o quadrado inteiro, massa um, no meio"
        self.ate(0.2)
        self.play(Create(neg), FadeIn(negf), FadeIn(lneg), run_time=0.9)                           # "e soma o triângulo com massa negativa"
        self.ate(0.38)
        self.play(FadeIn(p_tr), run_time=0.6)                                                     # "a cinco sextos de altura"
        D1, d1 = eqp("Y", "=", r"\dfrac{M_\square Y_\square+M_\triangle Y_\triangle}{M_\square+M_\triangle}", size=46, cores={0: X_})
        D2, d2 = eqp("=", r"\big(", "1", r"\cdot", F(1, 2), "+", r"(-\tfrac{1}{4})", r"\cdot", F(5, 6), r"\big)", "/", r"\big(", "1", "-", F(1, 4), r"\big)",
                     size=46, cores={4: G, 8: G})
        D3, d3 = eqp("=", r"\big(", F(1, 2), "-", F(5, 24), r"\big)", "/", F(3, 4), "=", r"\tfrac{7/24}{3/4}", r"=\ ", F(7, 18), r"\ \mathrm{m}", size=46, cores={11: X_})
        na_conta(D1, 1.3)
        na_conta(D2, 0.2)
        na_conta(D3, -0.8, x0=1.15)
        self.ate(0.48)
        self.play(FadeIn(D1), run_time=0.8)
        self.ate(0.55)
        self.play(FadeIn(mp(D2, d2, [0, 1, 3, 5, 7, 9, 10, 11, 13, 15])), TransformFromCopy(p_sq[1], mp(D2, d2, [2])), TransformFromCopy(p_sq[1], mp(D2, d2, [12])),
                  TransformFromCopy(lneg, mp(D2, d2, [6])), TransformFromCopy(lneg, mp(D2, d2, [14])), TransformFromCopy(p_tr[1], mp(D2, d2, [8])),
                  FadeIn(mp(D2, d2, [4])), run_time=1.5)                                           # o −¼ sai do rótulo MASSA −¼
        self.ate(0.7)
        self.play(FadeIn(D3, shift=0.1 * DOWN), run_time=1.0)
        bx3 = caixa(mp(D3, d3, [11, 12]), cor=X_)
        cm.set_opacity(1.0)
        anel = Circle(radius=0.36).move_to(Pw(0.5, Y7)).set_stroke(WHITE_, 3)
        self.ate(0.82)
        self.play(FadeIn(bx3), FadeIn(cm), run_time=0.6)                                          # o mesmo ponto: o ⊕ não pula
        self.play(FadeOut(anel, scale=2.2), run_time=0.8)
        selo = txt("OS DOIS JEITOS DÃO O MESMO", 28, bold=True)
        na_conta(selo, -1.8)
        self.ate(0.9)
        self.play(FadeIn(selo, shift=0.1 * UP), run_time=0.6)
        self.ate(0.97)
        # ── E1-4: foge do furo; desafio ──
        self.an("E1-4")
        fg = seta(Pw(0.5, 0.5) + 0.06 * DOWN, Pw(0.5, Y7) + 0.25 * UP, WHITE_, 5, tip=0.2)
        lfg = VGroup(txt("FOGE", 28, bold=True), txt("DO FURO", 28, bold=True)).arrange(DOWN, buff=0.08, aligned_edge=LEFT).next_to(Pw(0.5, 0.47), RIGHT, buff=0.55)
        self.play(FadeOut(VGroup(D1, D2, D3, bx3, selo, Xe, ps)), run_time=0.5)
        self.ate(0.06)
        self.play(GrowArrow(fg[0]) if False else Create(fg), FadeIn(lfg), run_time=0.8)
        self.ate(0.14)
        self.dica_entra(dica("BURACO = MASSA NEGATIVA.", "O CENTRO DE MASSA FOGE DO FURO"))
        self.ate(0.48)
        self.dica_sai()
        # desafio: disco R = 1 m com furo de 0,5 m, centro do furo a 0,25 m do centro do disco
        Cd, Rd = P3(4.3, 0.15), 1.65
        furo_c = Cd + P3(0.25 * Rd, 0.0)
        disco = Difference(Circle(radius=Rd).move_to(Cd), Circle(radius=0.5 * Rd).move_to(furo_c))
        disco.set_fill(["#9AA6B8", "#3A4252"], 1).set_sheen_direction(UP).set_stroke("#7FB2FF", 2, opacity=0.7)
        disco._degrade = "aco"
        bfuro = DashedVMobject(Circle(radius=0.5 * Rd).move_to(furo_c).set_stroke(WHITE_, 2, opacity=0.7), num_dashes=28)
        tit = txt("DESAFIO", 30, bold=True, color=CYAN).move_to(Cd + P3(0, Rd + 0.85))
        dados = VGroup(rot("R = 1 m", 28), rot("furo: r = 0,5 m", 28), rot("a 0,25 m do centro", 28)).arrange(DOWN, buff=0.08, aligned_edge=LEFT)
        dados.move_to(Cd + P3(0, -Rd - 0.75))
        q = txt("ONDE FICA O CENTRO DE MASSA?", 30, bold=True).move_to(P3(Cd[0] - 0.2, -3.45))
        self.ate(0.55)
        self.play(FadeIn(tit), FadeIn(disco), Create(bfuro), run_time=1.0)
        self.ate(0.68)
        self.play(FadeIn(dados), run_time=0.8)
        self.ate(0.82)
        self.play(FadeIn(q, shift=0.1 * UP), run_time=0.7)
        self.ate(0.97)

    def mobjects_dots(self):
        """Os pontinhos dos centroides (Dot) que ficaram soltos na cena."""
        return [m for m in self.mobjects if isinstance(m, Dot)]

    # ════════════════════════════════════════ E2 — remador e estaca ════════════════════════════════════════
    def e2(self):
        self.an("E2-1")
        velhos = self.snap()
        self.secao("EXERCÍCIO 2 · REMADOR E ESTACA", selo="SEM FORÇA EXTERNA, O CENTRO DE MASSA NÃO SE MOVE")
        S, X0, YW = 1.45, -6.35, -1.05                    # tela por metro; estaca; linha d'água
        PX = lambda x: X0 + S * x
        self.xc = ValueTracker(0.0)                       # deslocamento da canoa (m)
        self.s_ = ValueTracker(0.0)                       # 0 = remador na popa … 1 = na proa
        self.fase = ValueTracker(0.0)
        self.add(self.xc, self.s_, self.fase)
        casco = [(0, 0.36), (0.22, 0.08), (0.6, -0.1), (1.5, -0.16), (2.4, -0.1), (2.78, 0.08), (3.0, 0.36)]
        agua = VGroup(Rectangle(width=PX(4.6) - X0, height=2.2).move_to(P3((X0 + PX(4.6)) / 2, YW - 1.1)).set_stroke(width=0).set_fill(BLUE_L, 0.13),
                      Line(P3(X0, YW), P3(PX(4.6), YW)).set_stroke(mix(BLUE_L, 0.3), 2.4, opacity=0.8))
        rng = np.random.default_rng(4)
        for _ in range(14):
            x_ = rng.uniform(X0 + 0.3, PX(4.4))
            yy = YW - rng.uniform(0.15, 1.9)
            agua.add(Line(P3(x_, yy), P3(x_ + rng.uniform(0.3, 0.8), yy)).set_stroke(mix(BLUE_L, 0.4), 1.4, opacity=0.4))
        agua._fundo = True
        margem = Rectangle(width=X0 + 7.6, height=1.0).move_to(P3((X0 - 7.6) / 2, YW - 0.5 + 0.12)).set_fill(TERRA, 1).set_stroke(mix(TERRA, 0.3), 1.5)
        margem._fundo = True
        estaca = VGroup(RoundedRectangle(corner_radius=0.04, width=0.16, height=1.9).move_to(P3(X0 - 0.08, YW + 0.35)).set_fill(["#9AA6B8", "#3A4252"], 1)
                        .set_sheen_direction(RIGHT).set_stroke("#7FB2FF", 1.5, opacity=0.6))
        estaca[0]._degrade = "aco"
        PES = {}

        def pessoa(fase, s):
            k_ = (round(fase, 2), s >= 1.0)
            if k_ not in PES:
                pose = "mira" if s >= 1.0 else andar(fase)
                PES.clear() if len(PES) > 80 else None
                PES[k_] = silhueta(PessoaPerfil(0.0, 0.0, 1.75 * S * 0.82, -1, pose))
            return PES[k_]

        def canoa_cena():
            xc, s = self.xc.get_value(), self.s_.get_value()
            base = lambda x, y: P3(PX(x + xc), YW + S * y)
            c_ = Polygon(*[base(x, y) for x, y in casco]).set_fill(["#9AA6B8", "#7A8696", "#3A4252"], 1).set_sheen_direction(UP).set_stroke("#7FB2FF", 2, opacity=0.7)
            c_._degrade = "aco"
            refl = c_.copy().flip(RIGHT, about_point=P3(0, YW)).set_fill(opacity=0.12).set_stroke(opacity=0.0)
            refl._degrade = "aco"
            xr = 2.7 - 2.45 * s                                            # remador sobre o convés (m, na canoa)
            p_ = pessoa(self.fase.get_value(), s).copy()
            p_.move_to(P3(PX(xr + xc), YW + S * 0.36 + p_.height / 2))
            xs = (75 * (xr + xc) + 150 * (1.5 + xc)) / 225                  # ⊕ do sistema (m)
            cmv = P3(PX(xs), YW + 1.25)
            g = VGroup(refl, c_, p_, DashedLine(cmv + 0.25 * DOWN, P3(PX(xs), YW), dash_length=0.08).set_stroke(WHITE_, 1.8, opacity=0.7), marcador_cm(cmv))
            self.reg("canoa", cm=cmv, x_cm=P3(xs, 0.0))
            return g
        cv = vivo(canoa_cena)
        eixo = VGroup(Line(P3(X0, YW - 2.25), P3(PX(4.4), YW - 2.25)).set_stroke(GEO, 2))
        for xm in range(0, 5):
            eixo.add(Line(P3(PX(xm), YW - 2.35), P3(PX(xm), YW - 2.15)).set_stroke(GEO, 2), rot(str(xm), 28, GEO).next_to(P3(PX(xm), YW - 2.35), DOWN, buff=0.1))
        eixo.add(VGroup(mtex("x", GEO, 36), rot("(m)", 28, GEO)).arrange(RIGHT, buff=0.08).next_to(P3(PX(4.4), YW - 2.25), RIGHT, buff=0.1))
        Lc0 = cota(PX(0), PX(3), YW + 2.65, rot_cota("3 m"), lado=UP)
        Lc = vivo(lambda: Lc0.copy().shift(S * self.xc.get_value() * RIGHT))      # a cota do comprimento anda com a canoa
        ya = YW + 1.55                                                               # acima da cabeça da estaca
        alc = VGroup(Line(P3(PX(0), ya), P3(PX(-0.8), ya)).set_stroke(VREL, 2.6), Line(P3(PX(-0.8), ya - 0.1), P3(PX(-0.8), ya + 0.1)).set_stroke(VREL, 2.6),
                     rot("0,80 m", 28, VREL).next_to(P3(PX(-0.4), ya), UP, buff=0.2))
        self.troca(velhos, FadeIn(agua), FadeIn(margem), FadeIn(estaca), FadeIn(cv), FadeIn(eixo), seq=True)
        dd = VGroup(eqp("m", "=", r"75\ \mathrm{kg}", size=46)[0], eqp(r"M_c", "=", r"150\ \mathrm{kg}", size=46)[0], eqp("L", "=", r"3\ \mathrm{m}", size=46)[0],
                    VGroup(txt("ALCANCE", 28), rot("= 0,80 m", 32)).arrange(RIGHT, buff=0.14))
        for k, d_ in enumerate(dd):
            na_conta(d_, 2.3 - 0.72 * k)
        self.ate(0.08)
        self.play(FadeIn(dd[0]), Indicate(cv, color=WHITE_, scale_factor=1.0) if False else Wait(0.01), run_time=0.6)
        self.ate(0.2)
        self.play(FadeIn(dd[1]), FadeIn(Lc0), FadeIn(dd[2]), run_time=0.8)
        self.remove(Lc0)
        self.add(Lc)
        self.ate(0.5)
        self.play(FadeIn(alc), FadeIn(dd[3]), run_time=0.8)                     # "o braço alcança oitenta centímetros"
        q = txt("ALCANÇA A ESTACA?", 32, bold=True)
        na_conta(q, -0.75)
        self.ate(0.85)
        self.play(FadeIn(q, shift=0.1 * UP), run_time=0.6)
        self.ate(0.97)
        # ── E2-2: o ⊕ não se mexe ──
        self.an("E2-2")
        E, ie = eqp(r"F_{ext,x}", "=", "0", r"\ \ \mathrm{e}\ \ ", r"V_{cm}", "=", "0", size=46, cores={0: FC, 4: VEL})
        na_conta(E, -0.75)
        L3 = VGroup(eqp(r"\Rightarrow\ ", r"X_{cm}", size=46, cores={1: CMC})[0], txt("FIXO", 30, bold=True)).arrange(RIGHT, buff=0.18)
        na_conta(L3, -1.65)
        self.play(FadeOut(q), FadeOut(alc), run_time=0.4)
        self.ate(0.15)
        self.play(FadeIn(E), run_time=0.7)
        self.ate(0.42)
        self.play(FadeIn(L3), onda(P3(PX(2.0), YW + 1.25)), run_time=0.8)
        self.ate(0.55)
        dur = max(2.5, self.resta() - 1.2)
        self.play(self.s_.animate(rate_func=linear).set_value(0.999), self.xc.animate(rate_func=linear).set_value(0.999),
                  self.fase.animate(rate_func=linear).set_value(2 * PI * 3), run_time=dur)          # ele anda, a canoa recua; o ⊕ fica
        self.fase.set_value(0.0)

        def deslocs():
            s = self.s_.get_value()
            g = VGroup()
            if s > 0.02:
                xr0, xr1 = 2.7, 2.7 - 2.45 * s + self.xc.get_value()
                g.add(seta(P3(PX(xr0), YW + 3.35), P3(PX(xr1), YW + 3.35), VEL, 6, tip=0.22),
                      seta(P3(PX(0), YW - 0.55), P3(PX(self.xc.get_value()), YW - 0.55), VEL, 6, tip=0.22))
            return g
        self.dv = vivo(deslocs)
        self.play(FadeIn(self.dv), run_time=0.6)
        self.ate(0.97)
        # ── E2-3: a conta ──
        self.an("E2-3")
        self.play(FadeOut(VGroup(dd, E, L3)), run_time=0.5)
        A1, a1 = eqp(r"\Delta x_r", "=", "-3", "+", r"\Delta x_c", size=48, cores={0: VEL, 4: VEL})
        A2, a2 = eqp("m", r"\,\Delta x_r", "+", r"M_c", r"\,\Delta x_c", "=", "0", size=48, cores={1: VEL, 4: VEL})
        A3, a3 = eqp("75", r"\,(-3+\Delta x_c)", "+", "150", r"\,\Delta x_c", "=", "0", size=46)
        A4, a4 = eqp("225", r"\,\Delta x_c", "=", "225", size=48, cores={1: VEL})
        A5, a5 = eqp(r"\Delta x_c", "=", r"+1{,}0\ \mathrm{m}", size=48, cores={0: VEL})
        A6, a6 = eqp(r"\Delta x_r", "=", r"-2{,}0\ \mathrm{m}", size=48, cores={0: VEL})
        for M_, y_ in ((A1, 2.5), (A2, 1.65), (A3, 0.8), (A4, -0.05), (A5, -0.9), (A6, -1.65)):
            na_conta(M_, y_, x0=1.25 if M_ is A3 else XC0)
        # o PALCO revive: o mesmo passeio de novo, devagar, enquanto a conta corre
        self.s_.set_value(0.0); self.xc.set_value(0.0)
        self.ate(0.06)
        self.play(FadeIn(mp(A1, a1, [0, 1, 3, 4])), TransformFromCopy(Lc[0][1], mp(A1, a1, [2])), run_time=1.1)   # o −3 sai da cota da canoa
        self.ate(0.3)
        self.play(FadeIn(A2), self.s_.animate(rate_func=linear).set_value(0.35), self.xc.animate(rate_func=linear).set_value(0.35),
                  self.fase.animate(rate_func=linear).set_value(2 * PI), run_time=1.0)
        self.ate(0.48)
        self.play(TransformByGlyphMap(A2.copy(), A3, (J(a2, 0), J(a3, 0)), (J(a2, 1), J(a3, 1)), (J(a2, 2), J(a3, 2)), (J(a2, 3), J(a3, 3)),
                                      (J(a2, 4), J(a3, 4)), (J(a2, 5, 6), J(a3, 5, 6))),
                  self.s_.animate(rate_func=linear).set_value(0.6), self.xc.animate(rate_func=linear).set_value(0.6), self.fase.animate(rate_func=linear).set_value(4 * PI),
                  run_time=1.4)
        self.ate(0.62)
        self.play(TransformByGlyphMap(A3.copy(), A4, (J(a3, 0, 2, 3), J(a4, 0)), (J(a3, 1, 4), J(a4, 1)), (J(a3, 5), J(a4, 2)), (J(a3, 6), J(a4, 3)), auto_fade=True),
                  self.s_.animate(rate_func=linear).set_value(0.8), self.xc.animate(rate_func=linear).set_value(0.8), self.fase.animate(rate_func=linear).set_value(6 * PI),
                  run_time=1.4)                                                         # junta e o −225 atravessa
        self.ate(0.74)
        self.play(FadeIn(VGroup(A5, A6), shift=0.1 * DOWN), self.s_.animate(rate_func=linear).set_value(0.999), self.xc.animate(rate_func=linear).set_value(0.999),
                  self.fase.animate(rate_func=linear).set_value(8 * PI), run_time=1.2)
        self.fase.set_value(0.0)
        bx5 = caixa(VGroup(A5, A6), cor=VEL)
        l2 = rot("2,0 m", 30, VEL).next_to(P3(PX(2.7), YW + 3.35), RIGHT, buff=0.15)
        l1 = rot("1,0 m", 30, VEL).next_to(P3(PX(0.5), YW - 0.55), DOWN, buff=0.24)
        ver = mtex(r"75\cdot 2=150\cdot 1", WHITE_, 46)
        na_conta(ver, -2.6)
        self.ate(0.84)
        self.play(FadeIn(bx5), FadeIn(l2), FadeIn(l1), run_time=0.8)
        self.ate(0.9)
        self.play(FadeIn(ver, shift=0.1 * UP), run_time=0.6)
        self.ate(0.97)
        # ── E2-4: não alcança ──
        self.an("E2-4")
        self.play(FadeOut(VGroup(A1, A2, A3, A4, ver)), VGroup(A5, A6, bx5).animate.move_to(P3(CONTA_C[0], 2.1)), FadeOut(self.dv), FadeOut(l2), FadeOut(l1), run_time=0.6)
        self.dv.clear_updaters()
        d1 = cota(PX(0), PX(1.0), YW + 2.65, rot_cota("1,0 m"), lado=UP)
        Lc.clear_updaters()
        self.play(FadeOut(Lc), FadeIn(d1), run_time=0.6)
        self.s_.set_value(1.0)                                                          # o braço estica (pose de alcance)
        braco = VGroup(Line(P3(PX(1.0), YW + 0.9), P3(PX(0.2), YW + 0.9)).set_stroke(VREL, 3), Line(P3(PX(0.2), YW + 0.8), P3(PX(0.2), YW + 1.0)).set_stroke(VREL, 3),
                       rot("0,80 m", 28, VREL).next_to(P3(PX(0.6), YW + 0.9), DOWN, buff=0.2).shift(0.2 * LEFT))
        falta = VGroup(Line(P3(PX(0.2), YW + 0.9), P3(PX(0.0), YW + 0.9)).set_stroke(HEAT, 6), rot("0,20 m", 30, HEAT).next_to(P3(PX(0.1), YW + 0.9), UP, buff=0.45))
        self.ate(0.08)
        self.play(Create(braco), run_time=0.9)
        self.ate(0.2)
        self.play(FadeIn(falta), run_time=0.7)
        R1, r1 = eqp(r"1{,}0\ \mathrm{m}", "-", r"0{,}80\ \mathrm{m}", "=", r"0{,}20\ \mathrm{m}", size=48)
        na_conta(R1, 0.75)
        na = txt("NÃO ALCANÇA", 32, bold=True, color=HEAT)
        na_conta(na, -0.15)
        self.ate(0.26)
        self.play(TransformFromCopy(d1[1], mp(R1, r1, [0])), TransformFromCopy(braco[2], mp(R1, r1, [2])), FadeIn(mp(R1, r1, [1, 3])),
                  TransformFromCopy(falta[1], mp(R1, r1, [4])), run_time=1.2)
        self.play(FadeIn(na, shift=0.1 * UP), run_time=0.5)
        self.ate(0.45)
        self.play(Indicate(falta, color=HEAT, scale_factor=1.15), run_time=0.8)          # "o certo era ter amarrado antes"
        self.ate(0.55)
        self.play(FadeOut(eixo), run_time=0.4)                                          # a régua sai: a DICA ocupa o canto
        self.dica_entra(dica("DESLOCAMENTO EM RELAÇÃO À CANOA NÃO É", "DESLOCAMENTO EM RELAÇÃO À ÁGUA"))
        self.ate(0.85)
        self.play(onda(P3(PX(2.0), YW + 1.25)), run_time=0.9)                             # "quem está parado é o centro de massa"
        self.ate(0.97)

    # ════════════════════════════════════════ síntese ════════════════════════════════════════
    def sintese(self):
        self.an("S1")
        velhos = self.snap()
        self.secao("RESUMO")
        self.y_lado = True                                # o rótulo y (m) vai para o lado: no topo ele bate no cabeçalho RESUMO
        novo = ImageMobject(str(AQUI / "fundo_lab.png")).set_width(16).move_to(ORIGIN).set_z_index(-99)
        g = self.nova_granada(cam=self.CAM_PARABOLA, op=0.0, tau=self.T0_HOOK)
        g.fant.set_value(1.0)
        self.troca(velhos, FadeIn(novo), g.f3d.op.animate.set_value(1.0), seq=True)
        self.remove(self.fundo)
        self.fundo = novo
        par = self.g_par = self.parabola(g)
        self.play(Create(par), self.g_eix.animate.set_value(1.0), self.g_ras.animate.set_value(1.0), self.g_cm.animate.set_value(1.0),
                  g.tau.animate(rate_func=linear).set_value(1.0), run_time=1.2)
        self.play(self.g_peso.animate.set_value(1.0), g.tau.animate(rate_func=linear).set_value(1.6), run_time=0.8)
        tauF = g.ttoque[1] - 1.0
        self.play(g.tau.animate(rate_func=linear).set_value(g.TE + 0.3), run_time=max(1.0, 0.45 * self.resta()))   # "forças internas"
        self.play(self.g_peso.animate.set_value(0.0), g.tau.animate(rate_func=linear).set_value(tauF - 0.6), run_time=max(1.0, 0.45 * self.resta()))
        resp = VGroup(txt("QUEM CONTINUA NA PARÁBOLA É O", 32, bold=True), marcador_cm(r=0.17)).arrange(RIGHT, buff=0.2).move_to(P3(0, 3.0)).set_z_index(30)
        self.play(FadeIn(resp, shift=0.1 * UP), self.g_pul.animate(rate_func=there_and_back).set_value(1.0), g.tau.animate(rate_func=linear).set_value(tauF - 0.3),
                  run_time=0.9)
        self.ate_mov(0.97, g.tau, tauF)
        # ── S2: as quatro perguntas ──
        self.an("S2")
        self.cam_gra.clear_updaters()
        velhos = self.snap()
        linhas = []
        ys = (2.0, 0.6, -0.8, -2.2)
        perg = ("ONDE ESTÁ?", "COMO SE MOVE?", "QUE ENERGIA É RELATIVA?", "CORPO INTEIRO?")
        frm = [eqp(r"\vec R_{cm}", "=", r"\frac{\sum_i m_i\vec r_i}{M}", size=46, cores={0: CMC})[0],
               eqp("M", r"\vec A_{cm}", "=", r"\vec F^{\,ext}", size=46, cores={3: FC})[0],
               eqp("K", "=", r"\tfrac{1}{2}", "M", r"V_{cm}^2", "+", r"K_{rel}", size=46, cores={0: KC, 4: VEL, 6: KC})[0],
               eqp(r"\vec R_{cm}", "=", r"\frac{1}{M}", r"\int", r"\vec r", r"\,dm", size=46, cores={0: CMC, 4: GEO})[0]]
        icones = [self.icone(k) for k in range(4)]
        for k in range(4):
            icones[k].move_to(P3(-5.6, ys[k]))
            t_ = txt(perg[k], 30, bold=True).move_to(P3(-2.55, ys[k]))
            t_.align_to(P3(-3.9, 0), LEFT)
            na_conta(frm[k], ys[k], x0=2.3)
            linhas.append(VGroup(icones[k], t_, frm[k]))
        self.troca(velhos, FadeIn(linhas[0]), seq=True)
        for k, f_ in zip((1, 2, 3), (0.27, 0.52, 0.8)):
            self.ate(f_)
            self.play(FadeIn(linhas[k], shift=0.15 * UP), run_time=0.8)
        self.ate(0.97)

    def icone(self, k):
        """Desenhos pequenos da síntese: bandeja + placa · granada + canoa · barras · barra λ = cx."""
        aco = lambda m: (m.set_fill(["#9AA6B8", "#3A4252"], 1).set_sheen_direction(UP).set_stroke("#7FB2FF", 1.6, opacity=0.6), setattr(m, "_degrade", "aco"), m)[2]
        if k == 0:
            b = aco(Polygon(P3(-0.75, -0.35), P3(0.45, -0.35), P3(-0.15, 0.45)))
            bolas = VGroup(*[esfera_aco(r).move_to(p) for r, p in ((0.12, P3(-0.62, -0.25)), (0.09, P3(0.32, -0.27)), (0.09, P3(-0.15, 0.3)))])
            pl = aco(Polygon(P3(0.75, -0.45), P3(1.45, -0.45), P3(1.45, 0.25), P3(1.1, -0.1), P3(0.75, 0.25)))
            return VGroup(b, bolas, pl, marcador_cm(P3(-0.3, -0.12), r=0.1))
        if k == 1:
            gr = aco(Ellipse(width=0.5, height=0.64)).move_to(P3(-0.55, 0.05))
            arco = DashedVMobject(ArcBetweenPoints(P3(-1.2, -0.45), P3(0.1, -0.45), angle=-1.6).set_stroke(WHITE_, 2, opacity=0.5), num_dashes=14)
            canoa = aco(Polygon(P3(0.55, 0.0), P3(0.7, -0.25), P3(1.35, -0.3), P3(1.6, 0.0)))
            return VGroup(arco, gr, canoa, marcador_cm(P3(-0.55, 0.05), r=0.1))
        if k == 2:
            return VGroup(Rectangle(width=0.4, height=0.9).set_stroke(width=0).set_fill(KC, 1).move_to(P3(-0.35, 0.0)),
                          Rectangle(width=0.4, height=0.38).set_stroke(width=0).set_fill(mix(KC, 0.25), 1).move_to(P3(0.25, -0.26)),
                          Line(P3(-0.7, -0.45), P3(0.6, -0.45)).set_stroke(GEO, 2))
        return VGroup(barra_aco(-0.9, 0.9, 0.0, h=0.3, cores=["#C9D2DE", "#7A8696", "#262C38"]), marcador_cm(P3(0.3, 0.0), r=0.1))

    # ════════════════════════════════════════ encerramento ════════════════════════════════════════
    def encerramento(self):
        # ── EN1 ──
        self.an("EN1")
        velhos = self.snap()
        self.secao(None)
        logo = self.logo(5.4).move_to(P3(0, 0.75))
        aneis = VGroup(*[Circle(radius=r).move_to(P3(0, 0.75)).set_stroke(BLUE_L, 2, opacity=o) for r, o in ((2.5, 0.25), (2.9, 0.15))])
        ins = txt("INSCREVA-SE PARA ACOMPANHAR OS PRÓXIMOS VÍDEOS", 32, bold=True).move_to(P3(0, -3.0))
        self.troca(velhos, FadeIn(logo, scale=0.95), FadeIn(aneis), seq=True)
        self.ate(0.2)
        self.play(FadeIn(ins, shift=0.1 * UP), aneis.animate.scale(1.06).set_stroke(opacity=0.3), run_time=0.9)
        self.ate(0.6)
        self.play(aneis.animate.scale(1 / 1.06), run_time=1.2)
        self.ate(0.97)
        self.en2()
        self.en3()

    def en2(self):
        """A cena C04 do vídeo de colisões (re-renderizada aqui: mesmas cores e notação) com o ⊕ do par: x_cm = (2x₁ + 1x₂)/3 anda a ⅔ m/s
        antes, durante e depois da batida, com rastro em degradê e fotos a cada 0,5 s (igualmente espaçadas: velocidade constante)."""
        self.an("EN2")
        velhos = self.snap()
        C1F, C2F = GEO, STEEL
        m1, m2, u1, u2, vf = 2.0, 1.0, 2.0, -2.0, 2 / 3
        w1, w2, xc0, ty, kx, ka = 1.0, 0.8, -1.4, -2.25, 0.85, 0.55
        t = ValueTracker(-2.3)
        self.add(t)
        t_ini = -2.3
        selo = txt("DO VÍDEO DE COLISÕES EM 1D", 26, color=DIM).move_to(P3(0, 2.95))
        b1, b2 = Corpo("m_1", C1F, w1), Corpo("m_2", C2F, w2)

        def xs(tt):
            if tt < 0:
                return xc0 - w1 / 2 + u1 * tt * kx, xc0 + w2 / 2 + u2 * tt * kx
            return xc0 - w1 / 2 + vf * tt * kx, xc0 + w2 / 2 + vf * tt * kx

        def cena():
            tt = t.get_value()
            x1, x2 = xs(tt)
            g = VGroup(Line(P3(-7.2, ty), P3(7.2, ty)).set_stroke(WHITE_, 2.5, opacity=0.4))
            g.add(b1.copy().at(x1, ty), b2.copy().at(x2, ty))
            y0 = ty + 0.32
            if tt < 0:
                for x_, w_, v_, n_ in ((x1, w1, u1, r"v_{1i}"), (x2, w2, u2, r"v_{2i}")):
                    a = seta(P3(x_, y0 + w_), P3(x_ + v_ * ka, y0 + w_), VEL, 5, tip=0.2)
                    g.add(a, mtex(n_, VEL, 40).next_to(P3(x_ + v_ * ka / 2, y0 + w_), UP, buff=0.12))
            else:
                xm = (x1 + x2) / 2
                g.add(seta(P3(xm, y0 + w1), P3(xm + vf * ka, y0 + w1), VEL, 5, tip=0.2), mtex(r"v_f", VEL, 40).next_to(P3(xm + vf * ka / 2, y0 + w1), UP, buff=0.12))
            xcm = (m1 * x1 + m2 * x2) / (m1 + m2)
            ycm = ty - 0.5
            ts = np.linspace(t_ini, tt, max(2, int((tt - t_ini) * 12)))
            q = [P3((m1 * xs(s)[0] + m2 * xs(s)[1]) / (m1 + m2), ycm) for s in ts]
            g.add(rastro_cm(q, w=4, op=0.9))
            for s in np.arange(t_ini, tt + 1e-9, 0.5):
                g.add(marcador_cm(P3((m1 * xs(s)[0] + m2 * xs(s)[1]) / (m1 + m2), ycm), r=0.12, op=0.3, leve=True))
            g.add(marcador_cm(P3(xcm, ycm), r=0.2))
            ctr1, ctr2 = g[1].front.get_center(), g[2].front.get_center()
            self.reg("en2", cm=P3(xcm, ycm), media=P3((m1 * ctr1[0] + m2 * ctr2[0]) / (m1 + m2), ycm))
            return g
        cv = vivo(cena)
        self.troca(velhos, FadeIn(selo), FadeIn(cv), seq=True)
        self.play(t.animate(rate_func=linear).set_value(0.0), run_time=2.3 / 0.9)
        self.play(Flash(P3(xc0, ty + 0.4), color=WHITE_, line_length=0.2, flash_radius=0.1, num_lines=10), t.animate(rate_func=linear).set_value(0.08), run_time=0.4)
        self.play(t.animate(rate_func=linear).set_value(1.6), run_time=2.0)
        Fq, fi = eqp(r"v_f", "=", r"\frac{m_1v_{1i}+m_2v_{2i}}{m_1+m_2}", size=56, cores={0: VEL})
        fr_ = fi[2]
        for j in fr_[2:5] + fr_[8:11]:
            Fq[0][j].set_color(VEL)
        Fq.move_to(P3(-1.2, 1.25))
        Nq = mtex(r"=\frac{2\cdot 2+1\cdot(-2)}{3}=\tfrac{2}{3}\ \mathrm{m/s}", WHITE_, 48).next_to(Fq, RIGHT, buff=0.3)
        self.ate(0.22)
        self.play(FadeIn(Fq), t.animate(rate_func=linear).set_value(2.0), run_time=0.9)
        self.ate(0.32)
        self.play(FadeIn(Nq), run_time=0.8)
        G2, g2 = eqp("=", r"V_{cm}", size=56, cores={1: VEL})
        G2.next_to(Fq, DOWN, buff=0.35).align_to(Fq[0][fi[1][0]], LEFT)
        self.ate(0.42)
        self.play(TransformByGlyphMap(Fq.copy(), G2, (fi[1], g2[0]), (fi[0], g2[1]), (fi[2], []), auto_fade=True), run_time=1.3)   # ganha "= V_cm"
        bx = caixa(G2, cor=VEL)
        self.play(FadeIn(bx), run_time=0.4)
        # "ele já andava assim antes da batida, e continua igual depois": replay com o ⊕ reto, fotos igualmente espaçadas
        self.ate(0.6)
        self.play(t.animate.set_value(-2.3), run_time=0.6)
        self.play(t.animate(rate_func=linear).set_value(1.9), run_time=max(2.5, 0.78 * self.resta() * 0.25 + 2.5))
        card = VGroup(txt("JÁ ESTÁ NO CANAL:", 26, color=DIM), txt("COLISÕES EM 1D", 30, bold=True)).arrange(DOWN, buff=0.08, aligned_edge=LEFT)
        cx_ = RoundedRectangle(corner_radius=0.12, width=card.width + 0.5, height=card.height + 0.4).move_to(card).set_fill(PANEL, 0.9).set_stroke(BLUE_L, 2)
        cx_._fundo = True
        cartao_ = VGroup(cx_, card).to_corner(UR, buff=0.5).shift(0.95 * DOWN)            # o canto do cartão final do YouTube
        self.ate(0.82)
        self.play(FadeIn(cartao_, shift=0.1 * LEFT), run_time=0.7)
        self.ate(0.97)
        cv.clear_updaters()

    def en3(self):
        self.an("EN3")
        velhos = self.snap()
        topo = txt("NO PRÓXIMO VÍDEO: SÓ EXERCÍCIOS", 30, bold=True).move_to(P3(0, 2.85))
        self.troca(velhos, FadeIn(topo), seq=True)
        # (1) placa com furo fora do centro; o ⊕ foge do furo
        c1 = P3(-4.9, 0.1)
        pl = Difference(Square(2.6).move_to(c1), Circle(radius=0.55).move_to(c1 + P3(0.55, 0.45)))
        pl.set_fill(["#9AA6B8", "#3A4252"], 1).set_sheen_direction(UP).set_stroke("#7FB2FF", 2, opacity=0.7)
        pl._degrade = "aco"
        d_ = -(PI * 0.55 ** 2) / (2.6 ** 2 - PI * 0.55 ** 2) * P3(0.55, 0.45)
        cm1 = marcador_cm(c1, r=0.17)
        self.ate(0.18)
        self.play(FadeIn(pl), FadeIn(cm1), run_time=0.7)
        self.play(cm1.animate.move_to(c1 + d_ * 2.2), run_time=1.0)                       # foge do furo
        # (2) fio nas arestas de um cubo (Three.js): o ⊕ flutua fora do fio
        cb = self.cubo = Cubo3D(self, K=1.95, xc=0.0, yc=0.0, op=0.0)
        self.add(cb.az, cb.f3d)
        cmc = vivo(lambda: marcador_cm(self.reg("cubo", cm=cb.p(Cubo3D.CM))["cm"], r=0.17))
        self.t_cubo = self.clk.get_value()
        cb.az.add_updater(lambda m, dt=0: m.set_value(-55.0 + 14.0 * (self.clk.get_value() - self.t_cubo)))
        self.ate(0.32)
        self.play(cb.f3d.op.animate.set_value(1.0), FadeIn(cmc), run_time=0.8)
        # (3) gafanhoto numa folha que recua na água
        c3 = P3(4.9, -0.6)
        gt = ValueTracker(0.0)
        self.add(gt)

        def gafa():
            u = gt.get_value()
            g = VGroup(Line(P3(2.6, c3[1]), P3(7.3, c3[1])).set_stroke(mix(BLUE_L, 0.3), 2.4, opacity=0.8))
            g.add(Rectangle(width=4.7, height=1.0).move_to(P3(4.95, c3[1] - 0.5)).set_stroke(width=0).set_fill(BLUE_L, 0.12))
            folha_x = c3[0] - 0.9 * u
            folha = Ellipse(width=1.7, height=0.22).move_to(P3(folha_x, c3[1] + 0.02)).set_fill(["#9AA6B8", "#3A4252"], 1).set_sheen_direction(UP) \
                .set_stroke("#7FB2FF", 1.6, opacity=0.6)
            folha._degrade = "aco"
            gx = c3[0] + 1.8 * u
            gy = c3[1] + 0.25 + 1.8 * u * (1 - u) * 2.2
            corpo = Ellipse(width=0.62, height=0.2).move_to(P3(gx, gy)).set_fill(["#9AA6B8", "#3A4252"], 1).set_sheen_direction(UP).set_stroke("#7FB2FF", 1.4, opacity=0.6)
            corpo._degrade = "aco"
            pern = VGroup(Line(P3(gx - 0.1, gy - 0.05), P3(gx - 0.3, gy + 0.18)).set_stroke("#9AA6B8", 3),
                          Line(P3(gx - 0.3, gy + 0.18), P3(gx - 0.42, gy - 0.12 - 0.15 * (1 - u))).set_stroke("#9AA6B8", 3),
                          Dot(P3(gx + 0.33, gy + 0.04), radius=0.07, color="#9AA6B8"))
            g.add(folha, corpo, pern)
            return g
        gv = vivo(gafa)
        self.ate(0.6)
        self.play(FadeIn(gv), run_time=0.5)
        self.play(gt.animate.set_value(1.0), run_time=1.4)                                 # salta; a folha foge dele
        disco = Difference(Circle(radius=0.55).move_to(P3(-1.0, -2.45)), Circle(radius=0.27).move_to(P3(-0.86, -2.45)))
        disco.set_fill(["#9AA6B8", "#3A4252"], 1).set_sheen_direction(UP).set_stroke("#7FB2FF", 1.6, opacity=0.6)
        disco._degrade = "aco"
        rd = txt("E A RESPOSTA DO DESAFIO", 28).next_to(disco, RIGHT, buff=0.3)
        self.ate(0.82)
        self.play(FadeIn(disco), FadeIn(rd), run_time=0.7)
        prox = txt("PRÓXIMO VÍDEO: CENTRO DE MASSA · EXERCÍCIOS", 32, bold=True, color=CYAN).move_to(P3(0, -3.45))
        self.ate(0.9)
        self.play(FadeIn(prox, shift=0.1 * UP), run_time=0.7)
        self.ate(0.97)
        cb.az.clear_updaters()

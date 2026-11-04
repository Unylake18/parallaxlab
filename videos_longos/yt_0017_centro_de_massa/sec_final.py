"""Lote P5 (handoff v5, narração v3.2): E1, E2, síntese, encerramento. Regra G19 nos exercícios: ESQUEMA fixo à esquerda, CONTA à direita;
tudo que entra na conta sai do esquema; cada entrada ancorada na palavra da fala (self.em). Céu dos exercícios com metade das estrelas
(fundo_lab_ex.png); a síntese volta ao céu do vídeo.
E1 placa de 1 m com o triângulo de cima recortado: três triângulos → 7/18 m; massa negativa → o mesmo ponto; seta FOGE DO FURO; desafio do
disco com o furo deslocado 0,25 m (resposta nos comentários) · E2 remador (75 kg) e canoa (150 kg, 3 m): ⊕ parado em 2 m; canoa +1,0 m;
faltam 20 cm · S1 a granada de novo · S2 as quatro perguntas, cada miniatura repetindo a ação-chave · EN1 o centro de massa nas colisões
(blocos que grudam, vistos do chão e do ⊕) · EN2 inscrição. Nenhuma referência a vídeo que ainda não está no canal."""
from MF_Tools import TransformByGlyphMap

from camadas import *  # noqa: F401,F403
from sec_t4 import barra_aco


def mp(m, idx, partes):
    return VGroup(*[m[0][j] for k in partes for j in idx[k]])


J = lambda idx, *ks: [j for k in ks for j in idx[k]]
F = lambda a, b: rf"\tfrac{{{a}}}{{{b}}}"


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
    # v5: cada entrada ancorada na palavra da fala (self.em); ESQUEMA maior (S = 4,8); coordenadas e massas ≥ 46; ⊕ no tamanho normal
    def e1(self):
        S, O = 4.8, P3(-6.4, -2.6)
        Pw = lambda x, y: O + S * P3(x, y)
        self.Pw = Pw
        G, X_ = GEO, CMC
        Y7 = 7 / 18
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
        nt_ = lambda v: mtex(F(1, 2), G, 40) if v < 1 else rot("1", 30, G)
        for v in (0.5, 1):
            ax.add(Line(Pw(v, 0) + 0.09 * DOWN, Pw(v, 0) + 0.09 * UP).set_stroke(G, 2), nt_(v).next_to(Pw(v, 0), DOWN, buff=0.16),
                   Line(Pw(0, v) + 0.09 * LEFT, Pw(0, v) + 0.09 * RIGHT).set_stroke(G, 2), nt_(v).next_to(Pw(0, v), LEFT, buff=0.16))
        ax.set_z_index(-1)
        uns = VGroup(ax[9], ax[11])                                                                 # os dois "1" dos eixos
        self.play(FadeIn(ax), FadeIn(sobra), FadeIn(tri), run_time=0.8)
        self.em("de um metro de lado")
        self.play(Indicate(uns, color=WHITE_, scale_factor=1.35), run_time=0.8)
        self.em("recortou um triângulo")
        self.play(tri.animate.shift(0.9 * UP).set_opacity(0.0), Create(vazio), run_time=1.2)       # o triângulo se solta e sai
        self.remove(tri)
        ponta = Dot(Pw(0.5, 0.5), radius=0.065, color=WHITE_)
        self.em("com a ponta no centro")
        self.play(FadeIn(ponta, scale=2.0), Flash(Pw(0.5, 0.5), color=WHITE_, line_length=0.18, flash_radius=0.14, num_lines=10), run_time=0.7)
        self.em("Onde fica o centro")
        self.play(ShowPassingFlash(sobra.copy().set_fill(opacity=0).set_stroke(CYAN, 5), time_width=0.6), run_time=1.2)   # "o que sobrou"
        sim = DashedLine(Pw(0.5, 0.0), Pw(0.5, 1.0), dash_length=0.1).set_stroke(WHITE_, 2, opacity=0.6)
        Xe, ix = eqp("X", "=", F(1, 2), r"\ \mathrm{m}", size=52, cores={0: X_})
        na_conta(Xe, 1.8)
        ps = txt("POR SIMETRIA", 28).next_to(Xe, RIGHT, buff=0.35)
        Ye, iy = eqp("Y", "=", "?", size=52, cores={0: X_})
        na_conta(Ye, 0.75)
        self.em("Por simetria")
        self.play(Create(sim), run_time=0.8)
        self.em("na vertical do meio")
        self.play(sim.animate.set_stroke(CYAN, 4, opacity=1.0), run_time=0.5)
        self.play(sim.animate.set_stroke(WHITE_, 2, opacity=0.6), run_time=0.6)
        self.em("a meio metro de cada lado")
        self.play(FadeIn(Xe), FadeIn(ps), run_time=0.7)
        self.em("Falta a altura")
        self.play(FadeIn(Ye), run_time=0.6)
        self.em("dois jeitos")
        self.play(Indicate(Ye, color=WHITE_, scale_factor=1.15), run_time=0.8)
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
        quartos = VGroup(*[mtex(F(1, 4), WHITE_, 46).move_to(Pw(*c_) + (P3(0.5, -0.3) if k == 0 else P3(0, -0.5))) for k, c_ in enumerate(cents)])
        self.em("se divide em três")
        self.play(FadeOut(sobra), FadeOut(ponta), FadeIn(pecas), run_time=0.8)
        self.em("um quarto da área")
        self.play(FadeIn(quartos), run_time=0.6)
        self.em("de um triângulo uniforme")
        self.play(LaggedStart(*[ShowPassingFlash(p_.copy().set_fill(opacity=0).set_stroke(c_, 5), time_width=0.6) for p_, c_ in zip(pecas, bordas)],
                              lag_ratio=0.3), run_time=1.4)
        self.em("na média dos três vértices")
        pontos = VGroup()
        for k, t_ in enumerate(tris):                                                              # os vértices piscam; o centroide nasce na média
            vs = VGroup(*[Dot(Pw(*v), radius=0.08, color=bordas[k]) for v in t_])
            self.play(FadeIn(vs, scale=1.6), run_time=0.25)
            self.play(*[d_.animate.move_to(Pw(*cents[k])).scale(0.6) for d_ in vs], run_time=0.4)
            self.remove(vs)
            pontos.add(Dot(Pw(*cents[k]), radius=0.06, color=bordas[k]))
            self.add(pontos[-1])
        coords = VGroup(mtex(rf"({F(1, 2)};\ {F(1, 6)})", G, 46).next_to(Pw(*cents[0]), RIGHT, buff=0.34),
                        mtex(rf"({F(1, 6)};\ {F(1, 2)})", G, 46).next_to(Pw(*cents[1]), DOWN, buff=0.32),
                        mtex(rf"({F(5, 6)};\ {F(1, 2)})", G, 46).next_to(Pw(*cents[2]), DOWN, buff=0.32))
        parts = VGroup(*[esfera_aco(0.17).move_to(Pw(*c_)) for c_ in cents])
        self.em("Trocando cada triângulo")
        self.play(FadeOut(pecas), FadeOut(pontos), FadeIn(parts),
                  *[q_.animate.next_to(p_, LEFT if k == 0 else RIGHT, buff=0.12) for k, (q_, p_) in enumerate(zip(quartos, parts))], run_time=0.9)
        self.em("no centro dele")
        self.play(FadeIn(coords), run_time=0.6)                                                   # as coordenadas só entram sem as bordas das peças
        A, ia = eqp("Y", "=", r"\Big(", F(1, 4), r"\cdot", F(1, 6), "+", F(1, 4), r"\cdot", F(1, 2), "+", F(1, 4), r"\cdot", F(1, 2), r"\Big)", "/", F(3, 4),
                    size=46, cores={0: X_, 5: G, 9: G, 13: G})
        na_conta(A, 0.75, x0=1.25)
        self.em("as alturas dão")
        self.play(FadeOut(Ye), FadeIn(mp(A, ia, [0, 1, 2, 4, 6, 8, 10, 12, 14, 15, 16])),
                  *[TransformFromCopy(quartos[k], mp(A, ia, [3 + 4 * k])) for k in range(3)],
                  TransformFromCopy(coords[0][0][5:8], mp(A, ia, [5])), TransformFromCopy(coords[1][0][5:8], mp(A, ia, [9])),
                  TransformFromCopy(coords[2][0][5:8], mp(A, ia, [13])), run_time=1.5)              # cada altura sai da coordenada dela
        B, ib = eqp("=", r"\big(", F(1, 6), "+", F(1, 2), "+", F(1, 2), r"\big)", "/", "3", size=48)
        B.move_to(P3(XC0 + 0.55 + B.width / 2, -0.3))
        self.em("o centro de massa é a média simples")
        self.play(TransformByGlyphMap(A.copy(), B, (J(ia, 1), J(ib, 0)), (J(ia, 2), J(ib, 1)), (J(ia, 5), J(ib, 2)), (J(ia, 6), J(ib, 3)), (J(ia, 9), J(ib, 4)),
                                      (J(ia, 10), J(ib, 5)), (J(ia, 13), J(ib, 6)), (J(ia, 14), J(ib, 7)), (J(ia, 15), J(ib, 8)),
                                      (J(ia, 0, 3, 4, 7, 8, 11, 12, 16), []), ([], J(ib, 9)), auto_fade=True), run_time=1.5)   # o ¼ comum cancela
        C, ic = eqp("=", r"\tfrac{7/6}{3}", r"=\ ", F(7, 18), r"\ \mathrm{m}", r"\ \approx", r"0{,}39\ \mathrm{m}", size=48, cores={3: X_, 6: X_})
        C.move_to(P3(XC0 + 0.55 + C.width / 2, -1.35))
        self.em("sete dezoito avos")
        self.play(FadeIn(C, shift=0.1 * DOWN), run_time=0.9)
        bx = caixa(mp(C, ic, [3, 4]), cor=X_)
        cm = marcador_cm(Pw(0.5, Y7))
        self.em("uns trinta e nove")
        self.play(FadeIn(bx), FadeIn(cm, scale=1.5), run_time=0.7)
        meio = Dot(Pw(0.5, 0.5), radius=0.065, color=WHITE_)
        nota = txt("ABAIXO DO MEIO", 28, bold=True)
        na_conta(nota, -2.35)
        self.em("abaixo do meio")
        self.play(FadeIn(meio), FadeIn(nota), run_time=0.7)                                       # "ficou abaixo do meio"
        self.em("o recorte tirou massa")
        self.play(ShowPassingFlash(Polygon(Pw(0, 1), Pw(1, 1), Pw(0.5, 0.5)).set_stroke(MAG, 5), time_width=0.6), run_time=1.1)
        self.ate(0.97)
        # ── E1-3: massa negativa ──
        self.an("E1-3")
        sq = Square(S).move_to(Pw(0.5, 0.5)).set_fill(["#9AA6B8", "#3A4252"], 0.55).set_sheen_direction(UP).set_stroke(X_, 3)
        sq._degrade = "aco"
        neg = DashedVMobject(Polygon(Pw(0, 1), Pw(1, 1), Pw(0.5, 0.5)).set_stroke(escuro(MAG, 0.35), 3.5), num_dashes=36, dashed_ratio=0.6)
        negf = Polygon(Pw(0, 1), Pw(1, 1), Pw(0.5, 0.5)).set_stroke(width=0).set_fill(escuro(MAG, 0.55), 0.35)
        lneg = txt("MASSA −¼", 28, color=mix(MAG, 0.2)).move_to(Pw(0.5, 1) + P3(0, 0.42))
        p_sq = VGroup(esfera_aco(0.2).move_to(Pw(0.5, 0.5)), mtex("1", WHITE_, 46).next_to(Pw(0.5, 0.5), RIGHT, buff=0.58).shift(0.12 * UP))
        p_tr = VGroup(Dot(Pw(0.5, 5 / 6), radius=0.07, color=mix(MAG, 0.2)), mtex(F(5, 6), G, 46).next_to(Pw(0.5, 5 / 6), RIGHT, buff=0.2))
        velhos = VGroup(parts, quartos, coords, A, B, meio, nota, C, bx, cm)
        self.play(FadeOut(velhos), FadeIn(sq), VGroup(Xe, ps).animate.shift(0.65 * UP), run_time=0.8)
        self.em("massa negativa")
        self.play(Create(neg), FadeIn(negf), FadeIn(lneg), run_time=0.9)                           # o triângulo vira massa negativa
        self.em("menos o triângulo")
        self.play(ShowPassingFlash(sq.copy().set_fill(opacity=0).set_stroke(X_, 5), time_width=0.6), Indicate(negf, color=MAG, scale_factor=1.0), run_time=1.1)
        self.em("com massa um")
        self.play(FadeIn(p_sq), run_time=0.6)                                                     # "o quadrado inteiro, massa um, no meio"
        D1, d1 = eqp("Y", "=", r"\dfrac{M_\square Y_\square+M_\triangle Y_\triangle}{M_\square+M_\triangle}", size=46, cores={0: X_})
        D2, d2 = eqp("=", r"\big(", "1", r"\cdot", F(1, 2), "+", r"(-\tfrac{1}{4})", r"\cdot", F(5, 6), r"\big)", "/", r"\big(", "1", "-", F(1, 4), r"\big)",
                     size=46, cores={4: G, 8: G})
        D3, d3 = eqp("=", r"\big(", F(1, 2), "-", F(5, 24), r"\big)", "/", F(3, 4), "=", r"\tfrac{7/24}{3/4}", r"=\ ", F(7, 18), r"\ \mathrm{m}", size=46, cores={11: X_})
        na_conta(D1, 1.3)
        na_conta(D2, 0.2)
        na_conta(D3, -0.8, x0=1.15)
        self.em("e soma o triângulo")
        self.play(FadeIn(D1), run_time=0.8)
        self.em("Não é que exista")
        self.play(Indicate(VGroup(negf, lneg), color=MAG, scale_factor=1.04), run_time=0.9)
        self.em("artifício matemático")
        self.play(Circumscribe(lneg, color=MAG, buff=0.08), run_time=1.0)
        self.em("um quarto da área")
        self.play(Indicate(lneg, color=WHITE_, scale_factor=1.15), run_time=0.7)
        self.em("cinco sextos de altura")
        self.play(FadeIn(p_tr), run_time=0.6)
        self.em("Meio, menos")
        self.play(FadeIn(mp(D2, d2, [0, 1, 3, 5, 7, 9, 10, 11, 13, 15])), TransformFromCopy(p_sq[1], mp(D2, d2, [2])), TransformFromCopy(p_sq[1], mp(D2, d2, [12])),
                  TransformFromCopy(lneg, mp(D2, d2, [6])), TransformFromCopy(lneg, mp(D2, d2, [14])), TransformFromCopy(p_tr[1], mp(D2, d2, [8])),
                  FadeIn(mp(D2, d2, [4])), run_time=1.5)                                           # o −¼ sai do rótulo MASSA −¼
        self.em("dividido por três quartos")
        self.play(FadeIn(D3, shift=0.1 * DOWN), run_time=1.0)
        bx3 = caixa(mp(D3, d3, [11, 12]), cor=X_)
        cm = marcador_cm(Pw(0.5, Y7))                                                              # o ⊕ volta inteiro (tamanho normal)
        self.em("sete dezoito avos")
        self.play(FadeIn(bx3), FadeIn(cm), run_time=0.6)                                          # o mesmo ponto: o ⊕ não pula
        anel = Circle(radius=0.36).move_to(Pw(0.5, Y7)).set_stroke(WHITE_, 3)
        selo = txt("OS DOIS JEITOS DÃO O MESMO", 28, bold=True)
        na_conta(selo, -1.8)
        self.em("O mesmo ponto")
        self.play(FadeOut(anel, scale=2.2), FadeIn(selo, shift=0.1 * UP), run_time=0.8)
        self.ate(0.97)
        # ── E1-4: foge do furo; desafio ──
        self.an("E1-4")
        self.play(FadeOut(VGroup(D1, D2, D3, bx3, selo, Xe, ps, p_sq)), run_time=0.5)   # a massa 1 do quadrado já entrou na conta
        centro = Dot(Pw(0.5, 0.5), radius=0.06, color=WHITE_)
        fg = Arrow(Pw(0.5, 0.5), Pw(0.5, Y7) + 0.18 * UP, buff=0, stroke_width=9, color=WHITE_, max_tip_length_to_length_ratio=0.5, tip_length=0.18)
        lfg = VGroup(txt("FOGE", 26, bold=True), txt("DO FURO", 26, bold=True)).arrange(DOWN, buff=0.08, aligned_edge=LEFT)
        lfg.move_to(P3(Pw(0.5, 0)[0] + 0.55 + lfg.width / 2, Pw(0.5, 0.5)[1] + 0.05))          # à direita da seta, acima do anel do ⊕
        self.em("Guarda essa dica")
        self.dica_entra(dica("BURACO = MASSA NEGATIVA.", "O CENTRO DE MASSA FOGE DO FURO"))
        self.em("um buraco funciona")
        self.play(Indicate(VGroup(negf, lneg), color=MAG, scale_factor=1.04), run_time=0.9)
        self.em("o centro de massa sempre")
        self.play(Flash(Pw(0.5, Y7), color=CYAN, line_length=0.16, flash_radius=0.3, num_lines=12), run_time=0.7)
        self.em("foge do furo")
        self.play(FadeIn(centro), GrowArrow(fg), FadeIn(lfg), run_time=0.8)
        self.em("para o lado onde sobrou")
        self.play(ShowPassingFlash(Polygon(Pw(0, 0), Pw(1, 0), Pw(1, 1), Pw(0.5, 0.5), Pw(0, 1)).set_stroke(CYAN, 5), time_width=0.6), run_time=1.2)
        # desafio: disco R = 1 m com furo de 0,5 m; o furo nasce no centro e sobe 0,25 m (um quarto do raio) quando a fala diz "vinte e cinco centímetros"
        Cd, Rd = P3(2.1, 0.3), 1.65
        hr, hy = ValueTracker(0.0), ValueTracker(0.0)
        self.add(hr, hy)

        def disco_cena():
            r_, cf = 0.5 * Rd * hr.get_value(), Cd + UP * 0.25 * Rd * hy.get_value()
            d_ = Circle(radius=Rd).move_to(Cd)
            if r_ > 0.02:
                d_ = Difference(d_, Circle(radius=r_).move_to(cf))
            d_.set_fill(["#9AA6B8", "#3A4252"], 1).set_sheen_direction(UP).set_stroke("#7FB2FF", 2, opacity=0.7)
            d_._degrade = "aco"
            g = VGroup(d_)
            if r_ > 0.02:
                g.add(DashedVMobject(Circle(radius=r_).move_to(cf).set_stroke(WHITE_, 2, opacity=0.7), num_dashes=28))
            return g
        dv_ = vivo(disco_cena)
        tit = txt("DESAFIO", 30, bold=True, color=CYAN).move_to(Cd + P3(0, Rd + 0.5))
        dados = VGroup(rot("R = 1 m", 26), rot("furo: r = 0,5 m", 26), rot("a 0,25 m do centro", 26)).arrange(DOWN, buff=0.16, aligned_edge=LEFT)
        dados.move_to(Cd + P3(Rd + 0.3 + dados.width / 2, 0))
        cf1 = Cd + UP * 0.25 * Rd
        xe = Cd[0] - Rd - 0.3
        cota_f = VGroup(DashedLine(Cd, P3(xe - 0.1, Cd[1]), dash_length=0.07).set_stroke(WHITE_, 1.4, opacity=0.55),
                        DashedLine(cf1, P3(xe - 0.1, cf1[1]), dash_length=0.07).set_stroke(WHITE_, 1.4, opacity=0.55),
                        Line(P3(xe, Cd[1]), P3(xe, cf1[1])).set_stroke(GEO, 2.4), Line(P3(xe - 0.1, Cd[1]), P3(xe + 0.1, Cd[1])).set_stroke(GEO, 2.4),
                        Line(P3(xe - 0.1, cf1[1]), P3(xe + 0.1, cf1[1])).set_stroke(GEO, 2.4))
        cota_f.add(rot("0,25 m", 28, GEO).next_to(P3(xe, (Cd[1] + cf1[1]) / 2), LEFT, buff=0.15))
        ctr = VGroup(Dot(Cd, radius=0.055, color=WHITE_), Dot(cf1, radius=0.055, color=CYAN))
        q = txt("ONDE FICA O CENTRO DE MASSA?", 30, bold=True).move_to(P3(Cd[0], -2.05))
        com = VGroup(txt("DEIXE SUA RESPOSTA", 26, color=CYAN), txt("NOS COMENTÁRIOS", 26, color=CYAN)).arrange(DOWN, buff=0.08).move_to(P3(Cd[0], -2.85))
        self.em("E fica um desafio")
        self.dica_sai()
        self.play(FadeIn(tit), run_time=0.5)
        self.em("um disco de um metro")
        d0 = disco_cena()                                                                          # entra parado; depois vira a camada viva
        self.play(FadeIn(d0), FadeIn(dados[0]), run_time=0.8)
        self.remove(d0)
        self.add(dv_)
        self.em("com um furo de meio")
        self.play(hr.animate.set_value(1.0), FadeIn(dados[1]), run_time=0.9)
        self.em("vinte e cinco centímetros")
        self.play(hy.animate.set_value(1.0), run_time=1.0)                                        # o furo sai do centro: 0,25 m para cima
        self.play(FadeIn(ctr), FadeIn(cota_f), FadeIn(dados[2]), run_time=0.7)
        self.em("Onde fica o centro")
        self.play(FadeIn(q, shift=0.1 * UP), run_time=0.7)
        self.em("deixa a sua resposta")
        self.play(FadeIn(com, shift=0.1 * UP), run_time=0.7)
        self.ate(0.97)
        dv_.clear_updaters()

    # ════════════════════════════════════════ E2 — remador e estaca ════════════════════════════════════════
    # v5: entradas ancoradas na fala; amarra solta (E2-1) e amarrada em fantasma (E2-4); cotas do E2-4 cada uma na sua altura; DICA na CONTA
    def e2(self):
        self.an("E2-1")
        velhos = self.snap()
        self.secao("EXERCÍCIO 2 · REMADOR E ESTACA", selo="SEM FORÇA EXTERNA, O CENTRO DE MASSA NÃO SE MOVE")
        S, X0, YW = 1.45, -6.35, -1.05                    # tela por metro; estaca; linha d'água
        PX = lambda x: X0 + S * x
        YA = YW + 2.15                                    # altura do braço esticado
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
            xr = 3.0 - 3.0 * s                                              # remador de ponta a ponta (3 m na canoa): X_cm fica em 2 m
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
        # amarra solta na proa (pendurada na água) e o fantasma do remador na proa com o braço esticado
        corda = VMobject().set_points_smoothly([P3(PX(0.06), YW + 0.5), P3(PX(-0.08), YW + 0.25), P3(PX(-0.02), YW + 0.02), P3(PX(0.18), YW - 0.3)])
        corda.set_stroke("#C9A27A", 3.2)
        fant = pessoa(0.0, 1.0).copy().set_opacity(0.3)
        fant.move_to(P3(PX(0.0), YW + S * 0.36 + fant.height / 2))
        alc = VGroup(Line(P3(PX(0), YA), P3(PX(-0.8), YA)).set_stroke(VREL, 2.6), Line(P3(PX(-0.8), YA - 0.1), P3(PX(-0.8), YA + 0.1)).set_stroke(VREL, 2.6),
                     rot("0,80 m", 26, VREL).next_to(P3(PX(-0.45), YA), UP, buff=0.14))
        self.troca(velhos, FadeIn(agua), FadeIn(margem), FadeIn(estaca), FadeIn(cv), FadeIn(eixo), seq=True)
        dd = VGroup(eqp("m", "=", r"75\ \mathrm{kg}", size=46)[0], eqp(r"M_c", "=", r"150\ \mathrm{kg}", size=46)[0], eqp("L", "=", r"3\ \mathrm{m}", size=46)[0],
                    VGroup(txt("ALCANCE", 28), rot("= 0,80 m", 32)).arrange(RIGHT, buff=0.14))
        for k, d_ in enumerate(dd):
            na_conta(d_, 2.3 - 0.72 * k)
        self.em("setenta e cinco")
        self.play(FadeIn(dd[0]), run_time=0.6)
        self.em("cento e cinquenta")
        self.play(FadeIn(dd[1]), run_time=0.6)
        self.em("e três metros")
        self.play(FadeIn(Lc0), FadeIn(dd[2]), run_time=0.7)
        self.remove(Lc0)
        self.add(Lc)
        self.em("encostada numa estaca")
        self.play(Indicate(estaca, color=CYAN, scale_factor=1.12), run_time=0.8)
        self.em("esqueceu de amarrar")
        self.play(Create(corda), run_time=0.7)
        self.play(Indicate(corda, color=HEAT, scale_factor=1.1), run_time=0.7)                     # a amarra solta pisca
        self.em("anda até a proa")
        self.play(FadeIn(fant), run_time=0.7)                                                     # o remador (fantasma) na proa, braço esticado
        self.em("alcança oitenta")
        self.play(Create(alc[:2]), FadeIn(alc[2]), FadeIn(dd[3]), run_time=0.9)                   # a cota do alcance se desenha
        q = txt("ALCANÇA A ESTACA?", 32, bold=True)
        na_conta(q, -0.75)
        self.em("consegue pegar a estaca")
        self.play(FadeIn(q, shift=0.1 * UP), Indicate(estaca, color=CYAN, scale_factor=1.15), run_time=0.8)   # a estaca acende
        self.ate(0.97)
        # ── E2-2: o ⊕ não se mexe ──
        self.an("E2-2")
        E, ie = eqp(r"F_{ext,x}", "=", "0", r"\ \ \mathrm{e}\ \ ", r"V_{cm}", "=", "0", size=46, cores={0: FC, 4: VEL})
        na_conta(E, -0.75)
        L3 = VGroup(eqp(r"\Rightarrow\ ", r"X_{cm}", size=46, cores={1: CMC})[0], txt("FIXO", 30, bold=True)).arrange(RIGHT, buff=0.18)
        na_conta(L3, -1.65)
        self.play(FadeOut(q), FadeOut(alc), FadeOut(fant), FadeOut(corda), run_time=0.4)
        self.em("vamos desprezar a resistência")
        self.play(ShowPassingFlash(Line(P3(X0, YW), P3(PX(4.6), YW)).set_stroke(CYAN, 5), time_width=0.6), run_time=1.0)   # a água
        self.em("remador mais canoa")
        self.play(Flash(P3(PX(3.0), YW + 1.6), color=WHITE_, line_length=0.18, flash_radius=0.5, num_lines=12),
                  Flash(P3(PX(1.5), YW + 0.2), color=WHITE_, line_length=0.18, flash_radius=0.7, num_lines=12), run_time=0.8)
        self.em("a força externa resultante")
        self.play(FadeIn(mp(E, ie, [0, 1, 2])), run_time=0.7)
        self.em("E tudo começa parado")
        self.play(FadeIn(mp(E, ie, [3, 4, 5, 6])), run_time=0.6)
        self.em("o centro de massa do sistema")
        self.play(FadeIn(L3), onda(P3(PX(2.0), YW + 1.25)), run_time=0.8)
        self.em("não pode sair do lugar")
        self.play(onda(P3(PX(2.0), YW + 1.25)), Indicate(L3, color=WHITE_, scale_factor=1.08), run_time=0.9)

        def deslocs():
            s = self.s_.get_value()
            g = VGroup()
            if s > 0.02:
                xr0, xr1 = 3.0, 3.0 - 3.0 * s + self.xc.get_value()
                g.add(seta(P3(PX(xr0), YW + 3.35), P3(PX(xr1), YW + 3.35), VEL, 6, tip=0.22),
                      seta(P3(PX(0), YW - 0.55), P3(PX(self.xc.get_value()), YW - 0.55), VEL, 6, tip=0.22))
            return g
        self.dv = vivo(deslocs)
        self.add(self.dv)
        self.em("Quando ele anda")
        dur = max(2.5, self.resta() - 0.6)
        self.play(self.s_.animate(rate_func=linear).set_value(0.999), self.xc.animate(rate_func=linear).set_value(0.999),
                  self.fase.animate(rate_func=linear).set_value(2 * PI * 3), run_time=dur)          # ele anda, a canoa recua; o ⊕ fica
        self.fase.set_value(0.0)
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
        passo = lambda v, f: (self.s_.animate(rate_func=linear).set_value(v), self.xc.animate(rate_func=linear).set_value(v),
                              self.fase.animate(rate_func=linear).set_value(f))
        self.em("três metros em relação à canoa")
        self.play(FadeIn(mp(A1, a1, [0, 1])), TransformFromCopy(Lc[0][1], mp(A1, a1, [2])), run_time=1.1)   # o −3 sai da cota da canoa
        self.em("na direção da estaca")
        self.play(ShowPassingFlash(Line(P3(PX(4.0), YW - 2.25), P3(PX(1.0), YW - 2.25)).set_stroke(VEL, 6), time_width=0.7), run_time=1.0)
        self.em("em relação à água")
        self.play(ShowPassingFlash(Line(P3(X0, YW), P3(PX(4.6), YW)).set_stroke(CYAN, 5), time_width=0.6), run_time=1.0)
        self.em("esses três metros")
        self.play(Indicate(mp(A1, a1, [2]), color=WHITE_, scale_factor=1.25), run_time=0.7)
        self.em("mais o que a canoa andou")
        self.play(FadeIn(mp(A1, a1, [3, 4])), *passo(0.2, PI), run_time=0.9)
        self.em("O centro de massa fixo")
        self.play(FadeIn(A2), *passo(0.4, 2 * PI), run_time=1.0)
        self.em("a massa do remador vezes")
        self.play(Indicate(mp(A2, a2, [0, 1]), color=WHITE_, scale_factor=1.2), *passo(0.47, 2.5 * PI), run_time=0.9)
        self.em("mais a massa da canoa")
        self.play(Indicate(mp(A2, a2, [3, 4]), color=WHITE_, scale_factor=1.2), *passo(0.53, 3 * PI), run_time=0.9)
        self.em("dá zero")
        self.play(TransformByGlyphMap(A2.copy(), A3, (J(a2, 0), J(a3, 0)), (J(a2, 1), J(a3, 1)), (J(a2, 2), J(a3, 2)), (J(a2, 3), J(a3, 3)),
                                      (J(a2, 4), J(a3, 4)), (J(a2, 5, 6), J(a3, 5, 6))), *passo(0.6, 4 * PI), run_time=1.4)
        self.em("Resolvendo")
        self.play(TransformByGlyphMap(A3.copy(), A4, (J(a3, 0, 2, 3), J(a4, 0)), (J(a3, 1, 4), J(a4, 1)), (J(a3, 5), J(a4, 2)), (J(a3, 6), J(a4, 3)), auto_fade=True),
                  *passo(0.8, 6 * PI), run_time=1.2)                                                # junta e o −225 atravessa
        l1 = rot("1,0 m", 30, VEL).next_to(P3(PX(0.5), YW - 0.55), DOWN, buff=0.24)
        l2 = rot("2,0 m", 30, VEL).next_to(P3(PX(3.0), YW + 3.35), RIGHT, buff=0.15)
        self.em("a canoa anda um metro")
        self.play(FadeIn(A5, shift=0.1 * DOWN), *passo(0.999, 8 * PI), run_time=1.0)
        self.fase.set_value(0.0)
        self.play(FadeIn(l1), run_time=0.5)                                                       # a seta da canoa ganha o valor
        self.em("o remador anda só dois")
        bx5 = caixa(VGroup(A5, A6), cor=VEL)
        self.play(FadeIn(A6, shift=0.1 * DOWN), FadeIn(l2), run_time=0.8)
        self.play(FadeIn(bx5), run_time=0.4)
        ver = mtex(r"75\cdot 2=150\cdot 1", WHITE_, 46)
        na_conta(ver, -2.6)
        self.em("Confere")
        self.play(FadeIn(ver, shift=0.1 * UP), run_time=0.6)
        self.em("setenta e cinco vezes dois")
        self.play(Indicate(VGroup(ver[0][:4], l2), color=WHITE_, scale_factor=1.2), run_time=0.9)   # o remador: 75 · 2
        self.em("cento e cinquenta vezes um")
        self.play(Indicate(VGroup(ver[0][5:], l1), color=WHITE_, scale_factor=1.2), run_time=0.9)   # a canoa: 150 · 1
        self.ate(0.97)
        # ── E2-4: não alcança ──
        self.an("E2-4")
        self.dv.clear_updaters()
        Lc.clear_updaters()
        self.play(FadeOut(VGroup(A1, A2, A3, A4, ver)), VGroup(A5, A6, bx5).animate.move_to(P3(CONTA_C[0], 2.1)), FadeOut(self.dv), FadeOut(l2), FadeOut(l1),
                  FadeOut(Lc), run_time=0.6)
        self.s_.set_value(1.0)                                                          # o braço estica (pose de alcance)
        self.xc.set_value(1.0)                                                          # a canoa no fim exato do recuo (X_cm = 2 m)
        d1 = cota(PX(0), PX(1.0), YW + 0.12, rot_cota("1,0 m"), lado=UP)                  # 1,0 m logo acima da água
        braco = VGroup(Line(P3(PX(1.0), YA), P3(PX(0.2), YA)).set_stroke(VREL, 3), Line(P3(PX(0.2), YA - 0.1), P3(PX(0.2), YA + 0.1)).set_stroke(VREL, 3),
                       rot("0,80 m", 28, VREL).next_to(P3(PX(0.45), YA), UP, buff=0.14))  # 0,80 m acima do braço
        falta = VGroup(Line(P3(PX(0.2), YA), P3(PX(0.0), YA)).set_stroke(HEAT, 6),
                       rot("0,20 m", 30, HEAT).next_to(P3(PX(0.1), YA), DOWN, buff=0.18))     # 0,20 m entre a mão e a estaca
        amarra = DashedLine(P3(PX(1.0) + 0.05, YW + 0.62), P3(X0 - 0.08, YW + 1.25), dash_length=0.09).set_stroke("#C9A27A", 3, opacity=0.45)
        R1, r1 = eqp(r"1{,}0\ \mathrm{m}", "-", r"0{,}80\ \mathrm{m}", "=", r"0{,}20\ \mathrm{m}", size=48)
        na_conta(R1, 0.75)
        na = txt("NÃO ALCANÇA", 32, bold=True, color=HEAT)
        na_conta(na, -0.15)
        self.em("a um metro da estaca")
        self.play(FadeIn(d1), run_time=0.7)
        self.em("o braço alcança")
        self.play(Create(braco[:2]), FadeIn(braco[2]), run_time=0.9)                              # o braço estica e para
        self.em("Faltam vinte")
        self.play(FadeIn(falta), TransformFromCopy(d1[1], mp(R1, r1, [0])), TransformFromCopy(braco[2], mp(R1, r1, [2])), FadeIn(mp(R1, r1, [1, 3])),
                  TransformFromCopy(falta[1], mp(R1, r1, [4])), run_time=1.1)
        self.play(FadeIn(na, shift=0.1 * UP), Indicate(falta, color=HEAT, scale_factor=1.15), run_time=0.7)   # o vão pulsa em laranja
        self.em("O certo era ter amarrado")
        self.play(Create(amarra), run_time=0.9)                                                   # a amarra, em fantasma, como devia estar
        self.em("E a dica")
        self.dica_entra(dica("DESLOCAMENTO EM RELAÇÃO", "À CANOA NÃO É DESLOCAMENTO", "EM RELAÇÃO À ÁGUA"))   # na coluna da CONTA
        na_canoa = VGroup(seta(P3(PX(4.0), YW + 3.0), P3(PX(1.0), YW + 3.0), GEO, 5, tip=0.2),
                          rot("3 m em relação à canoa", 26, GEO).next_to(P3(PX(2.5), YW + 3.0), UP, buff=0.22))
        na_agua = VGroup(seta(P3(PX(3.0), YW - 0.55), P3(PX(1.0), YW - 0.55), VEL, 6, tip=0.22),
                         rot("2 m em relação à água", 26, VEL).next_to(P3(PX(2.0), YW - 0.55), DOWN, buff=0.24))
        self.em("o deslocamento em relação à canoa")
        self.play(Create(na_canoa[0]), FadeIn(na_canoa[1]), run_time=0.9)
        self.em("o deslocamento em relação à água")
        self.play(Create(na_agua[0]), FadeIn(na_agua[1]), run_time=0.9)
        self.em("Quem está parado")
        self.play(onda(P3(PX(2.0), YW + 1.25)), run_time=0.9)                             # "quem está parado é o centro de massa"
        self.em("em relação à água que ele")
        self.play(Flash(P3(PX(2.0), YW), color=CYAN, line_length=0.16, flash_radius=0.2, num_lines=10), run_time=0.7)
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
        # ── S2: as quatro perguntas; a miniatura de cada uma repete a ação-chave enquanto a linha é falada (foco: a linha a 100%, as outras a 50%) ──
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
            t_.align_to(P3(-3.55, 0), LEFT)
            na_conta(frm[k], ys[k], x0=2.3)
            linhas.append(VGroup(icones[k], t_, frm[k]))
        veus = [Rectangle(width=15.0, height=1.3).move_to(P3(0, y_)).set_stroke(width=0).set_fill("#0B1A3A", 0.0).set_z_index(25) for y_ in ys]
        for v_ in veus:
            v_._fundo = True                                                     # véu de foco (50%): não é objeto da cena
        self.add(*veus)

        def foco(k, *extra, rt=0.6):
            vis = [j for j in range(4) if linhas[j] in self.mobjects or j == k]
            self.play(*[veus[j].animate.set_fill(opacity=0.0 if (k is None or j == k) else 0.5) for j in vis], *extra, run_time=rt)
        self.troca(velhos, FadeIn(linhas[0]), seq=True)
        b0, bolas0, pl0, cm0 = icones[0]
        self.em("na média das posições")
        self.play(Indicate(frm[0], color=WHITE_, scale_factor=1.08), run_time=0.9)
        self.em("pesada pelas massas")
        self.play(Indicate(bolas0, color=WHITE_, scale_factor=1.3), run_time=0.8)
        self.em("por partes")
        self.play(Rotate(VGroup(b0, bolas0), angle=-0.3, about_point=cm0.get_center(), rate_func=there_and_back), run_time=1.3)   # a bandeja tomba e volta
        self.em("massa negativa")
        self.play(ShowPassingFlash(pl0.copy().set_fill(opacity=0).set_stroke(MAG, 4), time_width=0.6), run_time=1.0)   # a placa com o recorte
        self.em("Como se move")
        foco(1, FadeIn(linhas[1], shift=0.15 * UP), rt=0.8)
        arco1, gr1, canoa1, cm1 = icones[1]
        cacos1 = VGroup(*[Ellipse(width=0.22, height=0.17).set_fill(["#9AA6B8", "#3A4252"], 1).set_sheen_direction(UP).set_stroke("#7FB2FF", 1.2, opacity=0.6)
                          .move_to(gr1.get_center()) for _ in range(3)])
        for c_ in cacos1:
            c_._degrade = "aco"
        self.em("como uma partícula")
        self.play(FadeOut(gr1), FadeIn(cacos1), run_time=0.2)
        self.play(*[c_.animate.shift(0.42 * d_) for c_, d_ in zip(cacos1, (UP, rotate_vector(UP, 2.1), rotate_vector(UP, -2.1)))], run_time=0.8)   # a granada estilhaça; o ⊕ fica
        self.em("empurrada só")
        self.play(canoa1.animate.shift(0.15 * RIGHT), run_time=0.9)                              # a canoa recua
        self.em("Que energia é relativa")
        foco(2, FadeIn(linhas[2], shift=0.15 * UP), rt=0.8)
        barras2 = icones[2][:2]
        self.em("a energia cinética se divide")
        self.play(*[GrowFromEdge(r_, DOWN) for r_ in barras2], run_time=1.0)                      # as duas barras sobem
        self.em("na do centro de massa")
        self.play(Indicate(barras2[0], color=WHITE_, scale_factor=1.15), run_time=0.8)
        self.em("que só muda com força externa")
        self.play(Indicate(frm[2][0][2:7], color=WHITE_, scale_factor=1.15), run_time=0.8)
        self.em("e na do movimento relativo")
        self.play(Indicate(VGroup(barras2[1], frm[2][0][-4:]), color=WHITE_, scale_factor=1.15), run_time=0.8)
        self.em("como na explosão")
        self.play(Indicate(barras2[1], color=mix(KC, 0.4), scale_factor=1.15), run_time=0.7)
        self.em("ou consumir")
        self.play(barras2[1].animate.stretch(0.05, 1, about_edge=DOWN).set_fill(HEAT), run_time=0.8)   # a colisão consome a relativa
        self.em("E num corpo inteiro")
        foco(3, FadeIn(linhas[3], shift=0.15 * UP), rt=0.8)
        barra3 = icones[3][0]
        cortes3 = VGroup(*[Line(barra3.get_top() + RIGHT * x_, barra3.get_bottom() + RIGHT * x_).set_stroke(BACKGROUND_COLOR, 2)
                           for x_ in np.linspace(-0.9, 0.9, 9)[1:-1]])
        self.em("a soma vira integral")
        self.play(LaggedStart(*[Create(c_) for c_ in cortes3], lag_ratio=0.15), run_time=1.0)    # a barra vira pedacinhos
        self.em("simetria primeiro")
        foco(None, Flash(icones[3][1].get_center(), color=CYAN, line_length=0.15, flash_radius=0.18, num_lines=10), rt=0.7)   # as quatro de volta a 100%
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
    # v5 (narração v3.2): nenhuma referência a vídeo que ainda não está no canal. EN1 = o centro de massa nas colisões (aplicação deste vídeo),
    # visto do chão e depois do referencial do ⊕; EN2 = logo e inscrição.
    def encerramento(self):
        self.en1()
        self.en2()

    def en1(self):
        """Blocos de 2 kg (+2 m/s) e 1 kg (−2 m/s) que grudam (+⅔ m/s). O ⊕ fica sobre os blocos, na altura do centro deles, em
        x_cm = (2x₁ + 1x₂)/3, reto a ⅔ m/s com rastro em degradê. Depois a câmera passa a andar com o ⊕ (troca de referencial do T3-2):
        momentos ±8/3 kg·m/s, iguais e opostos; os blocos grudam e param; a K relativa (16/3 J) vira laranja e sai, a K do CM (⅔ J) fica."""
        self.an("EN1")
        velhos = self.snap()
        self.secao("CENTRO DE MASSA NAS COLISÕES")
        C1F, C2F = GEO, STEEL
        m1, m2, u1, u2, vf = 2.0, 1.0, 2.0, -2.0, 2 / 3
        w1, w2, xc0, ty, kx, ka, kp = 1.0, 0.8, -1.4, -2.25, 0.85, 0.55, 0.42
        t, wref = ValueTracker(-2.3), ValueTracker(0.0)                                          # wref: 0 = chão, 1 = câmera no ⊕
        self.add(t, wref)
        t_ini = -2.3
        b1, b2 = Corpo(None, C1F, w1), Corpo(None, C2F, w2)

        def xs(tt):
            if tt < 0:
                return xc0 - w1 / 2 + u1 * tt * kx, xc0 + w2 / 2 + u2 * tt * kx
            return xc0 - w1 / 2 + vf * tt * kx, xc0 + w2 / 2 + vf * tt * kx
        xcm = lambda tt: (m1 * xs(tt)[0] + m2 * xs(tt)[1]) / (m1 + m2)
        XF = xcm(0.0)                                                                             # onde o ⊕ fica parado no referencial dele
        ycm = ty + 0.45                                                                           # na altura do centro dos blocos

        mrg = ValueTracker(0.0)                                                                   # 0 = rótulos 2 kg e 1 kg; 1 = um só, 3 kg
        self.add(mrg)
        Y_AR = ty + w1 + 0.62                                                                     # setas acima dos rótulos de massa

        def cena():
            tt, w, mm = t.get_value(), suave(wref.get_value()), mrg.get_value()
            x1, x2 = xs(tt)
            xc = xcm(tt)
            dx = -w * (xc - XF)
            g = VGroup(Line(P3(-7.2, ty), P3(7.2, ty)).set_stroke(WHITE_, 2.5, opacity=0.4))
            g.add(b1.copy().at(x1 + dx, ty), b2.copy().at(x2 + dx, ty))
            xm = (x1 + x2) / 2 + dx
            pm = P3(xm, ty + w1 + 0.24)                                                          # rótulo acima de cada bloco; grudados, 3 kg no centro
            if mm < 0.999:
                for x_, w_, n_ in ((x1 + dx, w1, "2 kg"), (x2 + dx, w2, "1 kg")):
                    q_ = P3(x_, ty + w_ + 0.24)
                    g.add(mrot(n_, 28, op=1 - mm).move_to(q_ + (pm - q_) * mm))
            if mm > 0.001:
                g.add(mrot("3 kg", 28, op=mm).move_to(pm))
            if w < 0.999:                                                                         # velocidades em relação ao chão
                o = 1 - w
                if tt < 0:
                    for x_, v_, n_ in ((x1 + dx, u1, r"2\ \mathrm{m/s}"), (x2 + dx, u2, r"-2\ \mathrm{m/s}")):   # os dados da fala
                        a = seta(P3(x_, Y_AR), P3(x_ + v_ * ka, Y_AR), VEL, 5, tip=0.2, op=o)
                        g.add(a, mtex(n_, VEL, 38).set_opacity(o).next_to(P3(x_ + v_ * ka / 2, Y_AR), UP, buff=0.12))
                else:
                    g.add(seta(P3(xm, Y_AR), P3(xm + vf * ka, Y_AR), VEL, 5, tip=0.2, op=o),
                          mtex(r"\tfrac{2}{3}\ \mathrm{m/s}", VEL, 38).set_opacity(o).next_to(P3(xm + vf * ka / 2, Y_AR), UP, buff=0.12))
            if w > 0.001 and tt < 0:                                                              # momentos no referencial do ⊕: iguais e opostos
                for x_, p_ in ((x1 + dx, m1 * (u1 - vf)), (x2 + dx, m2 * (u2 - vf))):
                    a = seta(P3(x_, Y_AR), P3(x_ + p_ * kp, Y_AR), MAG, 6, tip=0.22, op=w)
                    g.add(a, mtex(r"\tfrac{8}{3}\ \mathrm{kg\cdot m/s}", MAG, 36).set_opacity(w).next_to(P3(x_ + p_ * kp / 2, Y_AR), UP, buff=0.12))
            ts = np.linspace(t_ini, tt, max(2, int((tt - t_ini) * 12)))
            if w < 0.999:
                q = [P3(xcm(s) + dx, ycm) for s in ts]
                g.add(rastro_cm(q, w=4, op=0.9 * (1 - w)))
            g.add(marcador_cm(P3(xc + dx, ycm), r=0.2))
            ctr1, ctr2 = g[1].front.get_center(), g[2].front.get_center()
            v1, v2 = (u1, u2) if tt < 0 else (vf, vf)
            self.reg("en1", cm=P3(xc + dx, ycm), media=P3((m1 * ctr1[0] + m2 * ctr2[0]) / (m1 + m2), ycm),
                     p_rel=P3(m1 * (v1 - vf) + m2 * (v2 - vf), 0.0))                              # soma dos momentos no referencial do CM
            return g
        cv = vivo(cena)
        self.troca(velhos, FadeIn(cv), seq=True)
        self.em("Dois blocos")
        self.play(t.animate(rate_func=linear).set_value(0.0), run_time=self.ate_fala("batem e grudam", 1.2))
        self.play(Flash(P3(xc0, ty + 0.4), color=WHITE_, line_length=0.2, flash_radius=0.1, num_lines=10), t.animate(rate_func=linear).set_value(0.1),
                  mrg.animate.set_value(1.0), run_time=0.5)                                       # grudados: 2 kg + 1 kg = 3 kg
        self.em("A batida é interna")
        self.play(onda(P3(xcm(0.1), ycm), r=0.3), t.animate(rate_func=linear).set_value(0.5), run_time=0.9)
        self.play(t.animate(rate_func=linear).set_value(2.0), run_time=self.ate_fala("Então a velocidade final", 1.0))
        # a fórmula sai deste vídeo: v_f = V_cm (grudados, andam com o ⊕) = Σ mᵢvᵢ/M (a caixa do T2-2) = (m₁v₁ᵢ + m₂v₂ᵢ)/(m₁ + m₂)
        def partes(m_):                                                                           # "=", numerador, barra, denominador (pela altura)
            gl = list(m_[0])
            k_ = max(range(1, len(gl)), key=lambda q: gl[q].width)
            yb = gl[k_].get_y()
            return ([0], [q for q in range(1, len(gl)) if q != k_ and gl[q].get_y() > yb], [k_],
                    [q for q in range(1, len(gl)) if q != k_ and gl[q].get_y() < yb])
        L1, l1 = eqp(r"v_f", "=", r"V_{cm}", size=52, cores={0: VEL, 2: VEL})
        L1.move_to(P3(-4.6 + L1.width / 2, 2.35))
        bx1 = caixa(L1, cor=VEL)
        L1b = MathTex(r"=\frac{\sum_i m_i v_i}{M}", font_size=52, color=WHITE_).next_to(L1, RIGHT, buff=0.35)
        L2 = MathTex(r"=\frac{m_1v_{1i}+m_2v_{2i}}{m_1+m_2}", font_size=52, color=WHITE_)
        L2.move_to(P3(-4.6 + 0.55 + L2.width / 2, 0.75))
        L3 = MathTex(r"=\frac{2\cdot 2+1\cdot(-2)}{3}=\tfrac{2}{3}\ \mathrm{m/s}", font_size=48, color=WHITE_).next_to(L2, RIGHT, buff=0.3)
        mini_eq = MathTex(r"\vec V_{cm}=\frac{\sum_i m_i\vec v_i}{M}", font_size=46, color=WHITE_)
        mini_eq[0][0:4].set_color(VEL)
        mini = VGroup(caixa(mini_eq, cor=VEL), mini_eq)
        selo_t2 = txt('DO BLOCO "COMO SE MOVE?"', 24, color=DIM).next_to(mini, UP, buff=0.12)
        VGroup(mini, selo_t2).move_to(P3(5.2, 2.2))
        self.em("Então a velocidade final")
        self.play(FadeIn(L1), FadeIn(bx1), t.animate(rate_func=linear).set_value(2.2), run_time=0.8)   # grudados, os dois andam com o ⊕
        self.play(FadeIn(mini), FadeIn(selo_t2), run_time=0.4)
        self.play(TransformFromCopy(mini_eq[0][4:], L1b[0][0:]), run_time=0.9)                          # a média pesada das velocidades
        self.play(FadeOut(mini), FadeOut(selo_t2), run_time=0.3)
        p1, p2 = partes(L1b), partes(L2)
        self.play(TransformByGlyphMap(L1b.copy(), L2, *[(a_, b_) for a_, b_ in zip(p1, p2)]), run_time=0.9)   # dois blocos: m₁v₁ᵢ + m₂v₂ᵢ sobre m₁ + m₂
        self.em("dois terços")
        self.play(FadeIn(L3, shift=0.1 * RIGHT), run_time=0.8)
        # o mesmo choque visto do ⊕: a câmera passa a andar com ele
        rot_ref = VGroup(txt("VISTO DO CENTRO DE MASSA:", 26), MathTex(r"\vec P=\vec 0", font_size=40, color=MAG), txt("ANTES E DEPOIS", 26)).arrange(RIGHT, buff=0.18)
        rot_ref.move_to(P3(-1.6, -3.3))
        KCM_, KREL_ = 2 / 3, 16 / 3
        e_ = 0.3
        base_b = P3(5.2, -1.25)
        bar_cm = Rectangle(width=0.5, height=KCM_ * e_).set_stroke(width=0).set_fill(KC, 1).move_to(base_b + P3(0, KCM_ * e_ / 2))
        bar_rel = Rectangle(width=0.5, height=KREL_ * e_).set_stroke(width=0).set_fill(mix(KC, 0.25), 1).move_to(base_b + P3(1.55, KREL_ * e_ / 2))
        for r_ in (bar_cm, bar_rel):
            r_._fundo = True
        lb = VGroup(VGroup(mtex("K", KC, 36), txt("DO CM", 24)).arrange(DOWN, buff=0.06).next_to(base_b, DOWN, buff=0.12),
                    VGroup(mtex("K", KC, 36), txt("RELATIVA", 24)).arrange(DOWN, buff=0.06).next_to(base_b + P3(1.55, 0), DOWN, buff=0.12))
        chao_b = Line(base_b + P3(-0.45, 0), base_b + P3(2.0, 0)).set_stroke(GEO, 2)
        self.em("Agora olha a mesma batida")
        self.play(t.animate.set_value(t_ini), mrg.animate.set_value(0.0), run_time=0.5)
        self.play(wref.animate.set_value(1.0), FadeIn(rot_ref), FadeIn(VGroup(bar_cm, bar_rel, lb, chao_b)), run_time=1.4)   # a câmera passa a andar com o ⊕
        self.em("Os dois chegam")
        self.play(t.animate(rate_func=linear).set_value(0.0), run_time=self.ate_fala("e param", 1.2))
        self.play(Flash(P3(XF, ty + 0.4), color=WHITE_, line_length=0.2, flash_radius=0.1, num_lines=10), t.animate(rate_func=linear).set_value(0.1),
                  mrg.animate.set_value(1.0), run_time=0.5)
        self.em("Toda a energia relativa")
        self.play(bar_rel.animate.set_fill(HEAT), run_time=0.5)
        self.play(bar_rel.animate.stretch(0.02, 1, about_edge=DOWN).shift(0.6 * UP).set_opacity(0.0), t.animate(rate_func=linear).set_value(0.6), run_time=1.2)   # a relativa vira outra coisa
        self.em("e a do centro de massa fica")
        self.play(Indicate(VGroup(bar_cm, lb[0]), color=WHITE_, scale_factor=1.15), run_time=0.8)
        selo_mod = txt("NO MÓDULO DE COLISÕES", 28, color=DIM).next_to(P3(7.4, -3.3), LEFT, buff=0)
        chao_ref = txt("VISTO DO CHÃO", 26).move_to(rot_ref)
        self.em("É isso que a gente")
        self.play(wref.animate.set_value(0.0), t.animate(rate_func=linear).set_value(1.6), FadeTransform(rot_ref, chao_ref),
                  FadeIn(selo_mod, shift=0.1 * UP), run_time=1.6)                                 # de volta ao chão; o selo fica ≥ 1,5 s na tela
        self.em("módulo de colisões")
        self.play(Indicate(selo_mod, color=WHITE_, scale_factor=1.06), t.animate(rate_func=linear).set_value(2.0), run_time=0.8)
        self.ate(0.97)
        cv.clear_updaters()

    def en2(self):
        self.an("EN2")
        velhos = self.snap()
        self.secao(None)
        logo = self.logo(5.4).move_to(P3(0, 0.75))
        aneis = VGroup(*[Circle(radius=r).move_to(P3(0, 0.75)).set_stroke(BLUE_L, 2, opacity=o) for r, o in ((2.5, 0.25), (2.9, 0.15))])
        ins = txt("INSCREVA-SE PARA ACOMPANHAR OS PRÓXIMOS VÍDEOS", 32, bold=True).move_to(P3(0, -3.0))
        self.troca(velhos, FadeIn(logo, scale=0.95), FadeIn(aneis), seq=True)
        self.em("se inscreve")
        self.play(FadeIn(ins, shift=0.1 * UP), aneis.animate.scale(1.06).set_stroke(opacity=0.3), run_time=0.9)
        self.em("Até a próxima")
        self.play(aneis.animate.scale(1 / 1.06), run_time=1.0)
        self.ate(0.97)

"""Lote PE1 (v2): E1 — O BLOCO E O CARRETEL. ESQUEMA fixo à esquerda: carretel (disco de aço, R = 0,10 m desenhado 0,9 u; marca branca mostra o giro) com
corda e bloco (m = 1,0 kg, queda h = 1,0 m = 3,0 u); barras de energia U, K_bloco, K_carretel à direita do ESQUEMA com a legenda acima (U + K_b + K_c = mgh
em todo quadro). Álgebra construída: cada símbolo/número da CONTA voa do rótulo (m, M, R, h, g, v, ω) ou da barra; sem linha de substituição por FadeIn.
Contas por energia: v² = 2mgh/(m + M/2) → 3,13 m/s; ω = 31,3 rad/s em CÂMERA LENTA ×4 (≤ 30° por quadro). E1-6: o aro (I = MR²) → 2,56 m/s."""
import kit as _kit
from pecas21 import *  # noqa: F401,F403

KE = 2.9                                            # u/m: h = 1 m
OC = P3(-5.3, 1.0)                                 # eixo do carretel
RC = 0.9
XR = OC[0] + RC                                     # a corda desce pela direita do carretel
YB0 = -0.35                                         # centro do bloco no começo
WB, HBk = 0.85, 0.6
XB = (-1.2, -0.65, -0.1)                             # barras U, K_bloco, K_carretel
YE0, HE = -3.0, 2.8
LENTA = 4.0
C_U, C_KB, C_K2 = "#35D9FF", "#9FEFFF", "#E6F7FF"      # U, K bloco, K carretel: três tons da família ciano (v3)


def gidx(m, idx, simbolo, k=0):
    """Índice (em m[0]) do glifo de `idx` que a forma reconhece como `simbolo` com tamanho óptico k."""
    for j in idx:
        r = _kit._id_glifo(m[0][j])
        if r is not None and r == (simbolo, k):
            return j
    return idx[0]


class LoteE1(Lote21):
    FUNDO = "fundo_lab_ex.png"

    def corpo(self):
        self.an("E1-1")
        self.secao("EXERCÍCIO 1 · O BLOCO E O CARRETEL")
        self.guia(['ENUNCIADO:', 'BLOCO DESCE E GIRA O', 'CARRETEL, SEM ESCORREGAR.', 'VELOCIDADE APÓS DESCER 1 m?'])                                      # v6 G4: a coluna da direita não fica vazia
        s = ValueTracker(0.0)                       # fração da descida (0 → 1)
        aro = ValueTracker(0.0)                     # 0 disco · 1 aro
        vis = ValueTracker(0.0)                     # setas v e ω visíveis
        self.add(s, aro, vis)
        self.s, self.aro = s, aro

        def frac_c():                               # fração da energia no carretel: (M/2)/(m + M/2) no disco, M/(m + M) no aro
            a = aro.get_value()
            return (1 - a) * 0.5 + a * (2 / 3)

        def esquema():
            u = s.get_value()
            y = YB0 - u * KE
            th = -u * 1.0 / 0.10                     # ângulo do carretel = descida / R (rad)
            g = VGroup()
            a = aro.get_value()
            if a < 0.99:
                g.add(escala_op(disco_aco(OC, RC), 1 - a))
            if a > 0.01:
                g.add(escala_op(aro2d(OC, RC, 0.12), a))
            g.add(Line(OC, OC + RC * np.array([math.cos(th + PI / 2), math.sin(th + PI / 2), 0])).set_stroke(WHITE_, 3).set_z_index(8))
            g.add(eixo_cruz(OC, 0.13))
            g.add(Line(P3(XR, OC[1]), P3(XR, y + HBk / 2)).set_stroke(GEO, 2.6).set_z_index(3))
            g.add(bloco_aco(WB, HBk).move_to(P3(XR, y)))
            if vis.get_value() > 0.01 and u > 0.03:
                g.add(seta(P3(XR - 0.62, y + 0.2), P3(XR - 0.62, y - 0.35 * vis.get_value()), VEL, 6, tip=0.2, z=12))
            fc = frac_c()
            U = 9.8 * (1 - u)
            Kb, Kc = 9.8 * u * (1 - fc), 9.8 * u * fc
            g.add(barra_E(XB[0], YE0, HE * U / 9.8, 0.34, C_U, hmax=HE), barra_E(XB[1], YE0, HE * Kb / 9.8, 0.34, C_KB, hmax=HE),
                  barra_E(XB[2], YE0, HE * Kc / 9.8, 0.34, C_K2, hmax=HE))
            if not PEDIDOS3D:
                self.reg("e1", u=u, U=U, Kb=Kb, Kc=Kc, soma=U + Kb + Kc, mgh=9.8, th=th, lenta=LENTA,
                         pos_bloco=float(y), pos_marca=[float(math.cos(th + PI / 2)), float(math.sin(th + PI / 2))],
                         alturas=[float(U / 9.8 * HE), float(Kb / 9.8 * HE), float(Kc / 9.8 * HE)])
            return g
        ev = vivo(esquema)
        lbar = VGroup(T("U", 36).move_to(P3(XB[0], YE0 - 0.3)), T("K_b", 36).move_to(P3(XB[1], YE0 - 0.3)), T("K_c", 36).move_to(P3(XB[2], YE0 - 0.3)))
        leg = VGroup(*[VGroup(Square(side_length=0.2).set_fill(c, 0.95).set_stroke(c, 1), T(sy, 36), txt(t, 24)).arrange(RIGHT, buff=0.14)
                       for c, sy, t in ((C_U, "U", "POTENCIAL"), (C_KB, "K_b", "BLOCO"), (C_K2, "K_c", "CARRETEL"))]).arrange(DOWN, buff=0.22, aligned_edge=LEFT).move_to(P3(-1.4, 1.0))
        self.play(FadeIn(ev), FadeIn(lbar), run_time=0.7)
        lM = VGroup(T("M=", 38), nm(r"2{,}0\ \mathrm{kg}", MAS, 38)).arrange(RIGHT, buff=0.08).move_to(P3(-6.2, 2.3))
        rl = Line(OC, OC + RC * UP).set_stroke(GEO, 3).set_z_index(9)
        lR = VGroup(T("R=", 38), nm(r"0{,}10\ \mathrm{m}", GEO, 38)).arrange(RIGHT, buff=0.08).move_to(P3(-3.85, 2.25))
        lm = VGroup(T("m=", 38), nm(r"1{,}0\ \mathrm{kg}", MAS, 38)).arrange(RIGHT, buff=0.08).move_to(P3(-2.5, YB0))
        XC = XR + 0.55                                # cota da altura, à direita do bloco
        cot = VGroup(DashedLine(P3(XC, YB0), P3(XC, YB0 - KE), dash_length=0.08).set_stroke(GEO, 2.2),
                     Line(P3(XC - 0.12, YB0), P3(XC + 0.12, YB0)).set_stroke(GEO, 2.2), Line(P3(XC - 0.12, YB0 - KE), P3(XC + 0.12, YB0 - KE)).set_stroke(GEO, 2.2))
        lh = VGroup(T("h=", 38), nm(r"1{,}0\ \mathrm{m}", GEO, 38)).arrange(RIGHT, buff=0.08).move_to(P3(-2.7, YB0 - KE / 2))
        lg = VGroup(T("g=", 38), nm(r"9{,}8\ \mathrm{m/s^2}", ACC, 38)).arrange(RIGHT, buff=0.08).move_to(P3(-1.15, 2.1))
        lv = T("v", 44)
        lw = T(r"\omega", 44)
        aw = seta_curva(OC, RC + 0.28, math.radians(205), -math.radians(65), VEL, 6)
        lw.move_to(OC + (RC + 0.7) * np.array([math.cos(math.radians(172)), math.sin(math.radians(172)), 0]))
        lv.add_updater(lambda m: m.move_to(P3(XR - 0.98, YB0 - s.get_value() * KE - 0.05)))
        self.gat("um carretel")
        self.play(FadeIn(lM), Create(rl), FadeIn(lR), run_time=0.7)
        self.pede([[MathTex("v", font_size=38, color=VEL), "APÓS DESCER", nm(r"1{,}0\ \mathrm{m}", GEO, 34)]])
        self.gat("na ponta tem um bloco de um quilo")
        self.play(FadeIn(lm), run_time=0.5)
        self.gat("depois de descer um metro")
        self.play(Create(cot), FadeIn(lh), run_time=0.6)
        self.gat("a corda não escorrega")
        self.hip("CORDA NÃO ESCORREGA · SAI DO REPOUSO")
        self.play(FadeIn(lg), FadeIn(leg), run_time=0.6)
        self.ate(0.99)
        # ── E1-2 ──
        self.an("E1-2")
        A, ia = M("m", "g", "h", "=", r"\tfrac{1}{2}", "m", "v^2", "+", r"\tfrac{1}{2}", "I", r"\omega^2", size=48, cores={0: KC, 1: KC, 2: KC})
        lA = linha_m(txt("ENERGIA:", 26, bold=True), A, buff=0.2)
        self.pilha.poe(lA)
        self.gat("a energia potencial que o bloco perde")
        self.play(FadeIn(lA[0]), run_time=0.3)
        self.monta(A, ia, {0: lm[0][0][:1], 1: lg[0][0][:1], 2: lh[0][0][:1]}, ate=3)
        self.gat("a do bloco, que desce")
        self.add(lv)
        self.play(vis.animate.set_value(1.0), FadeIn(lv), run_time=0.5)
        self.voa([(lm[0][0][:1], mp(A, ia, [5])), (lv, mp(A, ia, [6])[:1])], extra=[FadeIn(mp(A, ia, [4])), FadeIn(mp(A, ia, [6])[1:]), FadeIn(mp(A, ia, [7]))], rt=1.0, origem=False)
        self.gat("e a do carretel, que gira")
        self.play(FadeIn(aw), FadeIn(lw), run_time=0.5)
        self.voa([(lw, mp(A, ia, [10])[:1])], extra=[FadeIn(mp(A, ia, [8, 9])), FadeIn(mp(A, ia, [10])[1:])], rt=0.9, origem=False)
        self.gat("e a corda não escorrega")
        self.selo("CONDIÇÃO", [[T(r"v=\omega R", 38), "· SEM ESCORREGAR"]])
        self.foco = A
        self.ate(0.99)
        # ── E1-3 ──
        self.an("E1-3")
        B, ib = M("I", "=", r"\tfrac{1}{2}", "M", "R^2", size=48)
        self.pilha.poe(B)
        self.gat("o momento de inércia do disco")
        self.monta(B, ib, {3: lM[0][0][:1], 4: lR[0][0][:1]})
        B2, ib2 = M(r"\omega", "=", r"\tfrac{v}{R}", size=48)
        self.pilha.poe(B2)
        self.gat("e ômega é v sobre r")
        self.monta(B2, ib2, {0: lw, 2: lv}, rt=0.9)
        C_, ic = M(r"\tfrac{1}{2}", "I", r"\omega^2", "=", r"\tfrac{1}{2}", r"\big(\tfrac{1}{2}MR^2\big)", r"\big(\tfrac{v}{R}\big)^2", size=46)
        self.pilha.poe(C_)
        self.gat("quando você substitui")
        self.passo(A, C_, (J(ia, 8), J(ic, 0)), (J(ia, 9), J(ic, 1)), (J(ia, 10), J(ic, 2)), rt=1.0, origem=False)
        self.voa([(mp(B, ib, [2, 3, 4]), mp(C_, ic, [4, 5])), (mp(B2, ib2, [2]), mp(C_, ic, [6]))], extra=[FadeIn(mp(C_, ic, [3]))], rt=1.0, origem=False)
        j5 = [j for j in ic[5] if _kit._id_glifo(C_[0][j]) == ("R", 0)]
        j6 = sorted([j for j in ic[6] if C_[0][j].height > 0.12], key=lambda j: C_[0][j].get_y())
        rr = VGroup(risco(VGroup(*[C_[0][j] for j in (j5 or ic[5][-2:-1])]), cor=HEAT, w=4), risco(VGroup(C_[0][j6[0]]), cor=HEAT, w=4))
        self.gat("o r ao quadrado do momento de inércia cancela")
        self.play(Create(rr), run_time=0.6)
        D_, id_ = M("=", r"\tfrac{1}{4}", "M", "v^2", size=50)
        self.pilha.poe(D_)
        self.passo(C_, D_, (J(ic, 4), J(id_, 1)), (J(ic, 5), J(id_, 2)), (J(ic, 6), J(id_, 3)), rt=1.4, extra=[FadeOut(rr)], origem=False)
        self.remove(rr)
        self.gat("olha que bonito: o raio sumiu")
        self.play(self.ind(D_, id_, [1, 2, 3], MAS, 1.1, 0.9), run_time=0.9)
        self.gat("como se o carretel fosse uma massa extra")
        self.pilha.limpa(rt=0.3)
        F1, if1 = M("m", "g", "h", "=", r"\tfrac{1}{2}", "m", "v^2", "+", r"\tfrac{1}{4}", "M", "v^2", size=46, cores={0: KC, 1: KC, 2: KC})
        F2, if2 = M("=", r"\tfrac{1}{2}", r"\big(m+\tfrac{M}{2}\big)", "v^2", size=46)
        self.pilha.poe(F1)
        self.pilha.poe(F2)
        self.monta(F1, if1, {0: lm[0][0][:1], 1: lg[0][0][:1], 2: lh[0][0][:1], 5: lm[0][0][:1], 6: lv, 9: lM[0][0][:1]}, rt=1.3)
        self.passo(F1, F2, (J(if1, 4), J(if2, 1)), (J(if1, 5), J(if2, 2)[:1]), (J(if1, 9), J(if2, 2)[2:4]), (J(if1, 6), J(if2, 3)), rt=1.3, origem=False)
        self.foco = D_
        self.ate(0.99)
        # ── E1-4 ──
        self.an("E1-4")
        V1, iv1 = eqf(["v^2", "="], ["2", "m", "g", "h"], ["m", "+", r"\tfrac{M}{2}"], size=46)
        V1l = V1
        self.pilha.poe(V1)
        self.gat("agora substitui")
        self.passo(F2, V1, (J(if2, 2), [j for j in iv1["den"][0] + iv1["den"][1] + iv1["den"][2]]), (J(if2, 3), iv1["pre"][0]), rt=1.3, origem=False)
        V2, iv2 = eqf(["v^2", "="], ["2", r"\cdot", "1{,}0", r"\cdot", "9{,}8", r"\cdot", "1{,}0"], ["1{,}0", "+", r"\tfrac{2{,}0}{2}"], size=46,
                      cores={("num", 2): MAS, ("num", 4): ACC, ("num", 6): GEO, ("den", 0): MAS, ("den", 2): MAS})
        self.pilha.poe(V2)
        self.gat("duas vezes um")
        self.voa([(lm[1][0][:3], gl(V2, iv2["num"][2])), (lg[1][0][:3], gl(V2, iv2["num"][4])), (lh[1][0][:3], gl(V2, iv2["num"][6]))],
                 extra=[FadeIn(gl(V2, iv2["pre"][0] + iv2["pre"][1])), FadeIn(gl(V2, iv2["num"][0] + iv2["num"][1] + iv2["num"][3] + iv2["num"][5])),
                        FadeIn(gl(V2, iv2["bar"]))], rt=1.0, origem=False, cada=0.5)
        self.gat("sobre um mais dois sobre dois")
        self.voa([(lm[1][0][:3], gl(V2, iv2["den"][0])), (lM[1][0][:3], gl(V2, iv2["den"][2][:3]))], extra=[FadeIn(gl(V2, iv2["den"][1])), FadeIn(gl(V2, iv2["den"][2][3:]))],
                 rt=1.0, origem=False)
        V3, iv3 = M("v", "=", r"\sqrt{9{,}8}", "=", r"3{,}13\ \mathrm{m/s}", size=52, cores={4: VEL})
        mp(V3, iv3, [3, 4]).set_opacity(0)                       # v8: o 3,13 só aparece quando é dito ("tirando a raiz")
        V3b = caixa_l(V3, VEL)
        self.pilha.poe(V3b)
        self.gat("dá nove vírgula oito dentro da raiz quadrada")
        self.passo(V2, V3, (iv2["pre"][0][:1], J(iv3, 0)), rt=1.3, origem=False)
        self.gat("tirando a raiz")
        self.cx(V3b[0])
        self.play(mp(V3, iv3, [3, 4]).animate.set_opacity(1.0), run_time=0.7)
        W1, iw1 = M(r"\omega", "=", r"\tfrac{v}{R}", "=", r"\tfrac{3{,}13}{0{,}10}", "=", r"31{,}3\ \mathrm{rad/s}", size=46, cores={4: VEL, 6: VEL})
        self.pilha.poe(W1)
        self.gat("dividindo pelo raio de zero vírgula um metro")
        self.voa([(lR[1][0][:4], mp(W1, iw1, [4])[-4:])], extra=[FadeIn(mp(W1, iw1, [0, 1, 2, 3])), FadeIn(mp(W1, iw1, [4])[:-4])], rt=1.0, origem=False)
        self.gat("trinta e um vírgula três")
        self.play(FadeIn(mp(W1, iw1, [5, 6])), run_time=0.7)
        self.gat("por isso a animação está em câmera lenta")
        self.selo("CÂMERA LENTA ×4", ["OS NÚMEROS SÃO OS REAIS"])
        t_real = 2 * 1.0 / NUM["E1_v"]                    # descida com aceleração constante: t = 2h/v
        self.play(s.animate(rate_func=lambda x: x * x).set_value(1.0), run_time=t_real * LENTA)
        self.reg("e1_giro", graus_por_quadro_max=math.degrees(NUM["E1_w"] / LENTA / FPS), lenta=LENTA, t_real=t_real)
        self.foco = V3b
        self.ate(0.99)
        # ── E1-5: conferência pelas barras ──
        self.an("E1-5")
        self.sem_selo()
        self.vivos = [leg]
        self.pilha.limpa(rt=0.3)
        pb = [Dot(P3(x, YE0 + HE * f), radius=0.06, color=KC).set_z_index(12) for x, f in zip(XB, (1.0, 0.5, 0.5))]
        G_, ig = M(r"9{,}8\ \mathrm{J}", "=", r"4{,}9\ \mathrm{J}", "+", r"4{,}9\ \mathrm{J}", size=48, cores={0: KC, 2: KC, 4: KC})
        self.pilha.poe(G_)
        self.gat("de nove vírgula oito joules disponíveis")
        pb[0].move_to(P3(XB[0], YE0 + HE * 1.0))
        self.voa([(pb[0], mp(G_, ig, [0]))], extra=[FadeIn(mp(G_, ig, [1]))], rt=0.9, origem=False)
        self.play(ApplyWave(lbar, amplitude=0.12, run_time=1.5), ApplyWave(leg, amplitude=0.1, run_time=1.5))      # v7 parado 16:06: as barras e a legenda ondulam enquanto a fala chega nos 4,9 J
        self.gat("quatro vírgula nove vão para o bloco")
        self.voa([(pb[1], mp(G_, ig, [2]))], extra=[FadeIn(mp(G_, ig, [3]))], rt=0.9, origem=False)
        self.gat("e quatro vírgula nove para o carretel")
        self.voa([(pb[2], mp(G_, ig, [4]))], rt=0.9, origem=False)
        self.selo("CONFERE", [["A SOMA DAS BARRAS É", MathTex("mgh", font_size=38, color=KC)]])
        H_, ih = M(r"\tfrac{M}{2}", "=", r"1{,}0\ \mathrm{kg}", "=", "m", size=48, cores={2: MAS})
        self.pilha.poe(H_)
        self.gat("o carretel conta como m sobre dois")
        self.voa([(lM[0][0][:1], mp(H_, ih, [0])[:1]), (lm[0][0][:1], mp(H_, ih, [4]))], extra=[FadeIn(mp(H_, ih, [0])[1:]), FadeIn(mp(H_, ih, [1, 2, 3]))], rt=1.0, origem=False)
        self.play(s.animate(rate_func=smooth).set_value(0.0), run_time=0.6)
        self.play(s.animate(rate_func=lambda x: x * x).set_value(1.0), run_time=2.6)         # v9: a descida roda de novo enquanto M/2 aparece como "massa extra" andando com o bloco
        I_, ii = M(r"v_{queda}", "=", r"\sqrt{2gh}", "=", r"4{,}43\ \mathrm{m/s}", size=48, cores={4: VEL})
        self.pilha.poe(I_)
        self.gat("menos que os quatro vírgula quarenta e três")
        self.monta(I_, ii, {2: VGroup(lg[0][0][:1], lh[0][0][:1])}, rt=1.2)
        self.reg("e1_5", barras=[9.8, 4.9, 4.9], queda=NUM["E1_queda"])
        self.foco = I_
        self.gat("porque parte da energia ficou no giro")
        self.play(s.animate(rate_func=smooth).set_value(0.0), run_time=0.6)
        self.play(s.animate(rate_func=lambda x: x * x).set_value(1.0), run_time=2.6)         # v9: a descida roda de novo (a energia vai para o bloco e para o giro do carretel)
        self.ate(0.99)
        # ── E1-6: o aro ──
        self.an("E1-6")
        self.sem_selo()
        self.pilha.limpa(rt=0.3)
        self.guia(['PERGUNTA:', 'E SE O CARRETEL FOR UM ARO,', 'E NÃO UM DISCO?'])                                      # v6 G4: a coluna da direita não fica vazia
        self.gat("e se o carretel fosse um aro")
        self.play(s.animate.set_value(0.0), vis.animate.set_value(0.0), run_time=0.6)
        self.play(aro.animate.set_value(1.0), run_time=0.8)
        J1, ij1 = M("I", "=", r"\tfrac{1}{2}", "M", "R^2", size=48)
        J1b, ij1b = M("I", "=", "M", "R^2", size=48)
        self.pilha.poe(J1)
        self.monta(J1, ij1, {3: lM[0][0][:1], 4: lR[0][0][:1]}, rt=0.9)
        self.pilha.poe(J1b)
        self.gat("o momento de inércia dobra")
        self.passo(J1, J1b, (J(ij1, 0), J(ij1b, 0)), (J(ij1, 1), J(ij1b, 1)), (J(ij1, 3), J(ij1b, 2)), (J(ij1, 4), J(ij1b, 3)), rt=1.1, origem=False)
        K1, ik1 = eqf(["v^2", "="], ["2", "m", "g", "h"], ["m", "+", "M"], size=46)
        self.pilha.poe(K1)
        self.gat("o carretel passa a valer uma massa extra")
        self.voa([(mp(J1b, ij1b, [2]), gl(K1, ik1["den"][2]))], extra=[FadeIn(gl(K1, ik1["pre"][0] + ik1["pre"][1])), FadeIn(gl(K1, ik1["num"][0] + ik1["num"][1] + ik1["num"][2] + ik1["num"][3])),
                                                                           FadeIn(gl(K1, ik1["bar"])), FadeIn(gl(K1, ik1["den"][0] + ik1["den"][1]))], rt=1.0, origem=False)
        K2, ik2 = M("v", "=", r"2{,}56\ \mathrm{m/s}", size=52, cores={2: VEL})
        K2b = caixa_l(K2, VEL)
        self.pilha.poe(K2b)
        self.gat("o bloco desce a dois vírgula cinquenta e seis")
        self.play(FadeIn(K2b[0]), s.animate(rate_func=lambda x: x * x).set_value(1.0), vis.animate.set_value(1.0), run_time=2 * 1.0 / NUM["E1_aro"] * LENTA * 0.6)
        self.passo(K1, K2, (ik1["pre"][0][:1], J(ik2, 0)), rt=1.2, origem=False)
        self.reg("e1_aro", v=NUM["E1_aro"])
        self.gat("fica a dica")
        self.dica18([["SEM ESCORREGAR: TUDO EM", MathTex("v", font_size=38, color=VEL)], [T(r"I/R^2", 38), "VIRA MASSA EXTRA"]])
        self.ate(0.99)

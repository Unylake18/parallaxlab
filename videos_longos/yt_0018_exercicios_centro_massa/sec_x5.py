"""Lote PX5 (v3): X5 a balança que marca menos (máquina de Atwood sobre a balança; 2D, piso com a grade ciano).
Física (g = 9,8; y para cima): suporte em ∏ de 2 kg com polia; blocos de 3 kg e 1 kg. Parado: N = 6·9,8 = 58,8 N → 6,0 kg. Soltos: a = (3 − 1)·g/4
= 4,9 m/s² (3 kg desce, 1 kg sobe), T = 2·3·1·g/4 = 14,7 N; A_cm = (3·(−4,9) + 1·(+4,9) + 2·0)/6 = −1,633 m/s²; N = 6·(9,8 − 1,633) = 49,0 N → 5,0 kg.
O mostrador muda no mesmo quadro da soltura. ⊕ = média ponderada das alturas (suporte no CM dele), calculada por quadro.
v3: a montagem nasce na ordem física (balança → suporte → polia → fio → blocos → trava); massas escritas DENTRO dos blocos; forças de cada
bloco do lado de fora (nada no vão entre os blocos); ±4,9 na ponta das setas de aceleração; REPLAY quando os blocos voltam (o mostrador volta a
6,0 até a soltura); CONFERE uma linha por vez, com os blocos virando 2 kg + 2 kg; elevador com cabine, pessoa e a aceleração no ⊕.
Auditoria BALANÇA (qa.py): mostrador × N/g em todo quadro; ⊕ × média ponderada (≤ 1 px); a do bloco medida nas posições = 4,9 m/s².
v4 §2 #5–#6, §6: −4,9 à esquerda da seta do bloco pesado, acima da plataforma (folga ≥ 0,3); M = 6 kg acima do tracejado do SISTEMA (≥ 0,2),
sem cópia pousando no rótulo antigo; X5-7 com o selo só CONFERE, os blocos viram 2 kg + 2 kg (tamanho e rótulo) antes do mostrador voltar a
6,0, voltam a 3 e 1 kg com REPLAY, e no BLOCO LEVE → 0 o leve some, o pesado cai livre e o mostrador vai a 2,0 kg."""
from prob2 import *  # noqa: F401,F403

G = 9.8
M1, M2, MS = 3.0, 1.0, 2.0
A_ = (M1 - M2) * G / (M1 + M2)                 # 4,9 m/s²
TRA = 2 * M1 * M2 * G / (M1 + M2)              # 14,7 N
S = 1.1                                        # Manim por metro
CURSO = 0.75                                   # m que cada bloco anda depois da soltura
X3, X1, XS = -4.85, -3.15, -4.0                # x dos blocos (3 kg, 1 kg) e do suporte
L3, L1 = 0.8, 0.7                              # lados dos blocos
Y0, YS = -1.15, 0.6                            # altura inicial dos centros dos blocos; CM do suporte
YB = -2.45                                     # topo da balança
YP = 0.88                                      # centro da polia (v4: tudo 0,12 mais baixo; M = 6 kg cabe acima do tracejado)
RP = (X1 - X3) / 2                             # raio da polia
XCM = (MS * XS + M1 * X3 + M2 * X1) / 6        # x do ⊕ (só os blocos se movem, na vertical)
TOPO = YP + 1.0                                # topo da barra do suporte (a polia de raio 0,85 cabe embaixo)
XA3, XA1 = X3 - L3 / 2 - 0.22, X1 + L1 / 2 + 0.22        # setas de a: do lado de fora de cada bloco


class LoteX5(Prob2):
    def construct(self):
        self.setup_base(cap="PROBLEMA 6 · A BALANÇA")
        self.x5()
        self.fim()
        self.relatorio()
        self.gravar_reg()

    def x5(self):
        tb, solto = ValueTracker(0.0), ValueTracker(0.0)     # tempo desde a soltura (s de física); 0 = travado
        estro, op_cm, op_f, op_t, op_a = [ValueTracker(0.0) for _ in range(5)]
        op_fio, op_blk, op_trava = [ValueTracker(0.0) for _ in range(3)]          # montagem na ordem física
        leitura = ValueTracker(6.0)                         # o que o mostrador mostra (sobreposto nos casos-limite do X5-7)
        override = ValueTracker(0.0)
        w3, w1, yo, rot3, rot1 = ValueTracker(L3), ValueTracker(L1), ValueTracker(0.0), ValueTracker(0.0), ValueTracker(0.0)   # casos-limite
        queda = ValueTracker(0.0)                           # BLOCO LEVE → 0: o pesado cai livre (m)
        mostra = ValueTracker(1.0)                          # o número do mostrador some enquanto o 5,0 da conta pousa nele (nada pousa sobre outro)
        op_sup, leve = ValueTracker(0.0), ValueTracker(0.0)  # v5 G33: o suporte (2 kg) e os blocos (4 kg) só contam quando existem; `leve`: o bloco leve some
        self.add(mostra, op_sup, leve)
        self.add(tb, solto, estro, op_cm, op_f, op_t, op_a, leitura, override, op_fio, op_blk, op_trava, w3, w1, yo, rot3, rot1, queda)

        def ys(t=None):
            t = tb.get_value() if t is None else t
            d = 0.5 * A_ * t * t if solto.get_value() > 0.5 else 0.0
            y3, y1 = Y0 - S * d, Y0 + S * d                  # 3 kg desce, 1 kg sobe
            u = yo.get_value()                              # casos-limite: os blocos voltam à mesma altura
            return y3 + (Y0 - y3) * u - S * queda.get_value(), y1 + (Y0 - y1) * u

        def massa_presente():
            return 2.0 * op_sup.get_value() + 4.0 * op_blk.get_value()                  # o que está na balança em cada quadro (0 → 2 → 6)

        def N_kg():
            return 5.0 if solto.get_value() > 0.5 else massa_presente()

        def cm():
            y3, y1 = ys()
            return P3(XCM, (MS * YS + M1 * y3 + M2 * y1) / 6)
        # ── cenário estático: piso com grade, balança, suporte, polia ──
        piso = VGroup(Rectangle(width=7.2, height=1.1).move_to(P3(-3.8, -3.5)).set_stroke(width=0).set_fill("#070B18", 0.9))
        for xg in np.arange(-7.2, -0.2, 0.45):
            piso.add(Line(P3(xg, -2.95), P3(xg + (xg + 3.8) * 0.25, -4.05)).set_stroke(CYAN, 1, opacity=0.22))
        for yg in (-3.2, -3.5, -3.85):
            piso.add(Line(P3(-7.4, yg), P3(-0.2, yg)).set_stroke(CYAN, 1, opacity=0.22))
        piso.add(Line(P3(-7.4, -2.95), P3(-0.2, -2.95)).set_stroke(mix(CYAN, 0.4), 2, opacity=0.6))
        piso._fundo = True
        base = aco(RoundedRectangle(corner_radius=0.06, width=5.8, height=0.5).move_to(P3(-4.0, YB - 0.25)), 2.0)
        tela = RoundedRectangle(corner_radius=0.06, width=1.5, height=0.38).move_to(P3(-4.0, YB - 0.3)).set_fill("#04161E", 1).set_stroke(CMC, 2)
        tela._fundo = tela._caixa = True                                              # o mostrador: o texto mora dentro dele
        base._fundo = True                                                            # a plataforma da balança: o mostrador fica nela
        balanca = VGroup(piso, base, tela)
        sup = VGroup(aco(Rectangle(width=0.16, height=TOPO - YB).move_to(P3(-6.6, (TOPO + YB) / 2)), 1.4),
                     aco(Rectangle(width=0.16, height=TOPO - YB).move_to(P3(-1.4, (TOPO + YB) / 2)), 1.4),
                     aco(Rectangle(width=5.36, height=0.16).move_to(P3(-4.0, TOPO - 0.08)), 1.4),
                     aco(Rectangle(width=0.1, height=TOPO - 0.16 - YP).move_to(P3(-4.0, (TOPO - 0.16 + YP) / 2)), 1.2))
        pol = VGroup(Circle(radius=RP).move_to(P3(-4.0, YP)).set_fill("#3A4252", 1).set_stroke("#7FB2FF", 2),
                     Circle(radius=0.14).move_to(P3(-4.0, YP)).set_fill("#9AA6B8", 1).set_stroke(width=0))

        def bloco(w, nome, op, nome2=None, r=0.0):
            """Bloco de aço com a massa escrita dentro; `nome2`/`r`: o rótulo troca (3 kg → 2 kg) junto com o tamanho (v4 §6)."""
            b = aco(Square(w), 1.6, op=op)
            o_ = op * (0.0 if leve.get_value() > 0.5 else min(1.0, max(0.0, (w - 0.6) / 0.08)))     # o rótulo some antes do bloco (no caso do leve, vai ao lado)
            g_ = VGroup(b)
            if r < 0.5:                                                                   # troca em sequência: o velho sai, depois o novo entra
                g_.add(mrot(nome, 24, WHITE_, o_ * (1 - 2 * r)).move_to(b))
            elif nome2 is not None:
                g_.add(mrot(nome2, 24, WHITE_, o_ * (2 * r - 1)).move_to(b))
            return g_

        def mostrador():
            v = leitura.get_value() if override.get_value() > 0.5 else N_kg()
            self.reg("balanca", leitura=v, caso=override.get_value(), N_g=N_kg(), massa=massa_presente(), solto=solto.get_value(), tb=tb.get_value(), y3=ys()[0], y1=ys()[1], cm=cm(),
                     media=P3(XCM, (MS * YS + M1 * ys()[0] + M2 * ys()[1]) / 6))
            return mrot(f"{v:.1f} kg".replace(".", ","), 30, CMC, mostra.get_value()).move_to(tela.get_center())

        def cena():
            y3, y1 = ys()
            g = VGroup()
            fio_cor = INT if op_t.get_value() > 0.5 else GEO
            of = op_fio.get_value()
            h3, h1 = w3.get_value() / 2, w1.get_value() / 2
            if of > 0.01:
                g.add(Line(P3(X3, YP), P3(X3, y3 + h3)).set_stroke(fio_cor, 2.4, opacity=of),
                      Arc(radius=RP, start_angle=0, angle=PI, arc_center=P3(-4.0, YP)).set_stroke(fio_cor, 2.4, opacity=of))
                if w1.get_value() > 0.05:
                    g.add(Line(P3(X1, YP), P3(X1, y1 + h1)).set_stroke(fio_cor, 2.4, opacity=of))
            ob = op_blk.get_value()
            if ob > 0.01:
                g.add(bloco(w3.get_value(), "3 kg", ob, "2 kg", rot3.get_value()).move_to(P3(X3, y3)))
                if w1.get_value() > 0.05:
                    g.add(bloco(w1.get_value(), "1 kg", ob, "2 kg", rot1.get_value()).move_to(P3(X1, y1)))
                    if leve.get_value() > 0.5:
                        g.add(mtex(r"m\to 0", WHITE_, 36).set_opacity(ob).next_to(P3(X1 + h1 + 0.03, y1), RIGHT, buff=0.04))        # v5: "m → 0" enquanto encolhe (junto do bloco: o suporte está a 1,5 dele)
            if solto.get_value() < 0.5 and op_trava.get_value() > 0.01:              # a trava: alças presas na balança
                ot = op_trava.get_value()
                for x_, y_, h_ in ((X3 - 0.22, y3 - h3, 0), (X1 + 0.18, y1 - h1, 0)):
                    g.add(Line(P3(x_, y_), P3(x_, YB)).set_stroke("#9AA6B8", 3, opacity=0.9 * ot), Dot(P3(x_, YB), radius=0.06, color=HEAT).set_opacity(ot))
            o = op_a.get_value()
            if o > 0.01:                                                     # setas de aceleração do lado de fora de cada bloco
                g.add(seta(P3(XA3, y3 + 0.3), P3(XA3, y3 - 0.4), ACC, 5, tip=0.18, op=o), seta(P3(XA1, y1 - 0.3), P3(XA1, y1 + 0.4), ACC, 5, tip=0.18, op=o))
            if op_f.get_value() > 0.01:                                      # peso (embaixo) e tração (em cima) de cada bloco
                o = op_f.get_value()
                g.add(seta(P3(X3 - 0.15, y3 - h3 - 0.04), P3(X3 - 0.15, y3 - h3 - 0.72), FC, 6, tip=0.2, op=o),
                      seta(P3(X3, y3 + h3 + 0.04), P3(X3, y3 + h3 + 0.62), FC, 6, tip=0.2, op=o),
                      seta(P3(X1 + 0.12, y1 - h1 - 0.04), P3(X1 + 0.12, y1 - h1 - 0.5), FC, 6, tip=0.18, op=o),
                      seta(P3(X1, y1 + h1 + 0.04), P3(X1, y1 + h1 + 0.62), FC, 6, tip=0.2, op=o))
            if estro.get_value() > 0.01 and solto.get_value() > 0.5:
                for k in range(1, 6):
                    t = k * TF / 5.5
                    if t > tb.get_value() + 1e-6:
                        break
                    y3k, y1k = ys(t)
                    cmk = P3(XCM, (MS * YS + M1 * y3k + M2 * y1k) / 6)
                    g.add(marcador_cm(cmk, r=0.12, op=0.32, leve=True))
            if op_cm.get_value() > 0.01:
                c = cm()
                g.add(tracejado(P3(c[0], YP - RP - 0.1), P3(c[0], YB + 0.05), WHITE_, 1.6, 0.45), marcador_cm(c, r=0.17, op=op_cm.get_value()))
            g.add(mostrador())
            return g
        TF = math.sqrt(2 * CURSO / A_)
        cv = vivo(cena)
        l2 = rot("2 kg", 28).move_to(P3(-5.6, YP + 0.36))                                 # o suporte: embaixo da barra, à esquerda da polia
        # ══ X5-1: monta na ordem física ══
        self.an("X5-1")
        self.add(balanca)                                                                 # quadro 0: a balança já está lá
        self.chip(2)
        self.pede("⊕ ACELERA → FORÇA EXTERNA")                                           # v5 G32: o selo entra primeiro
        self.play(Indicate(tela, color=CMC, scale_factor=1.05), run_time=0.5)
        self.add(cv)
        self.play(FadeIn(sup[:3]), op_sup.animate.set_value(1.0), run_time=0.45)            # o mostrador sobe de 0,0 para 2,0 junto com o suporte
        self.play(FadeIn(sup[3]), FadeIn(pol), run_time=0.4)
        self.play(op_fio.animate.set_value(1.0), run_time=0.4)
        self.play(op_blk.animate.set_value(1.0), run_time=0.45)
        self.play(op_trava.animate.set_value(1.0), run_time=0.35)
        self.ate(0.3)
        self.play(FadeIn(l2), run_time=0.4)
        self.foco = l2
        self.ate(0.6)
        self.gat("seis quilos")
        self.play(Indicate(tela, color=CMC, scale_factor=1.12), run_time=0.8)              # "seis quilos"
        self.foco = tela
        self.ate(0.97)
        # ══ X5-2: a trava se abre; o mostrador cai no mesmo quadro ══
        self.an("X5-2")
        solto.set_value(1.0)                                                              # o mesmo quadro: trava aberta e mostrador em 5,0
        self.play(Indicate(tela, color=CMC, scale_factor=1.12), op_a.animate.set_value(1.0),
                  tb.animate(rate_func=linear).set_value(TF * 0.35), run_time=1.2)
        la = vivo(lambda: VGroup(mtex("a", ACC, 38).set_opacity(op_a.get_value()).next_to(P3(XA3, ys()[0]), LEFT, buff=0.24),
                                 mtex("a", ACC, 38).set_opacity(op_a.get_value()).next_to(P3(XA1, ys()[1]), RIGHT, buff=0.24)))
        self.add(la)
        self.play(tb.animate(rate_func=linear).set_value(TF * 0.97), run_time=2.0)
        q = cartao("POR QUE A BALANÇA", "MARCA MENOS?", size=30)
        self.pilha.poe(q)
        self.ate(0.6)
        self.gat("cinco quilos")
        self.play(FadeIn(q, shift=0.1 * UP), run_time=0.6)
        self.foco = q
        self.ate(0.97)
        # ══ X5-3: sistema, forças externas ══
        self.an("X5-3")
        self.pilha.limpa()
        topo_fr = TOPO + 0.05
        fr = DashedVMobject(RoundedRectangle(corner_radius=0.3, width=5.5, height=topo_fr - (YB + 0.03)).move_to(P3(-4.0, (topo_fr + YB + 0.03) / 2))
                            .set_stroke(WHITE_, 2.2, opacity=0.62), num_dashes=70, dashed_ratio=0.55).set_z_index(1)
        lsis = txt("SISTEMA", 24, op=0.85).next_to(fr, UP, buff=0.26).align_to(fr, LEFT)              # v4: à esquerda (o M = 6 kg voa para a direita sem cruzá-lo)
        self.gat("qual é o sistema")
        self.play(Create(fr), FadeIn(lsis), op_a.animate.set_value(0.0), run_time=0.9)
        self.remove(la)
        self.hip("FIO E POLIA IDEAIS · BALANÇA MEDE A FORÇA QUE FAZ PARA CIMA")
        self.ate(0.3)
        self.gat("força interna")
        self.play(op_t.animate.set_value(1.0), run_time=0.5)
        lint = txt("T: FORÇA INTERNA", 28, color=INT)                                         # v5: texto na CONTA (T é do fio, não se confunde com o desenho)
        self.pilha.poe(lint)
        self.play(FadeIn(lint, shift=0.08 * UP), run_time=0.5)
        self.ate(0.48)
        c0 = cm()
        Mg = VGroup(seta(c0 + P3(0, -0.2), c0 + P3(0, -0.8), FC, 7, tip=0.22), mtex(r"M\vec g", FC, 40).next_to(c0 + P3(0, -0.7), RIGHT, buff=0.3))    # abaixo do ⊕
        Nv = VGroup(seta(P3(-2.5, YB), P3(-2.5, YB + 1.0), FC, 7, tip=0.22), mtex(r"\vec N", FC, 40).next_to(P3(-2.5, YB + 0.55), RIGHT, buff=0.26))
        lM = rot("M = 6 kg", 26).next_to(fr, UP, buff=0.26).align_to(fr, RIGHT)                    # acima do tracejado, à direita (v4 #6)
        self.gat("o peso de tudo")
        self.play(op_cm.animate.set_value(1.0), FadeIn(Mg), FadeIn(Nv), run_time=0.9)
        self.play(Indicate(l2, color=WHITE_, scale_factor=1.15), FadeIn(lM, shift=0.08 * UP), run_time=0.9)      # 6 kg = 2 + 3 + 1 (nasce no lugar)
        E1, e1 = M("N", "-", "M", "g", "=", "M", r"A_{cm}", size=50, cores={0: FC, 3: ACC, 6: ACC})
        self.pilha.poe(E1)
        self.ate(0.72)
        self.voa([(Nv[1], mp(E1, e1, [0])), (Mg[1], mp(E1, e1, [2, 3])), (lM, mp(E1, e1, [5]))], extra=[FadeIn(mp(E1, e1, [1, 4, 6]))], rt=1.3)
        self.foco = E1
        self.ate(0.97)
        # ══ X5-4: a dos blocos; T e −T riscam ══
        self.an("X5-4")
        self.pilha.tira(lint)
        self.play(FadeOut(VGroup(lint, Mg, Nv)), op_cm.animate.set_value(0.0), op_t.animate.set_value(0.0), run_time=0.5)
        self.selo("REPLAY", None, rt=0.4)                                                  # os blocos voltam: o mostrador volta a 6,0 até a soltura
        solto.set_value(0.0)
        self.play(tb.animate.set_value(0.0), op_trava.animate.set_value(1.0), run_time=0.6)
        solto.set_value(1.0)
        self.play(tb.animate(rate_func=linear).set_value(0.12), op_f.animate.set_value(1.0), op_a.animate.set_value(1.0), run_time=0.6)
        self.sem_selo(rt=0.3)
        y3, y1 = ys()
        h3, h1 = L3 / 2, L1 / 2
        lf = VGroup(mtex("3g", FC, 38).next_to(P3(X3 - 0.15, y3 - h3 - 0.42), LEFT, buff=0.27), mtex("T", FC, 38).next_to(P3(X3, y3 + h3 + 0.36), LEFT, buff=0.27),
                    mtex("1g", FC, 38).next_to(P3(X1 + 0.12, y1 - h1 - 0.38), RIGHT, buff=0.27), mtex("T", FC, 38).next_to(P3(X1, y1 + h1 + 0.36), RIGHT, buff=0.27))
        la_ = VGroup(mtex("a", ACC, 38).next_to(P3(XA3, y3), LEFT, buff=0.24), mtex("a", ACC, 38).next_to(P3(XA1, y1), RIGHT, buff=0.24))
        n3, n1 = mrot("3 kg", 24).move_to(P3(X3, y3)), mrot("1 kg", 24).move_to(P3(X1, y1))      # cópias dos rótulos de dentro dos blocos (origem do 3 e do 1)
        self.play(FadeIn(lf), FadeIn(la_), run_time=0.6)
        A1, a1 = M("3", "g", "-", "T", "=", "3", "a", size=48, cores={1: ACC, 3: FC, 6: ACC})
        A2, a2 = M("T", "-", "1", "g", "=", "1", "a", size=48, cores={0: FC, 3: ACC, 6: ACC})
        self.pilha.poe(A1)
        self.ate(0.18)
        self.gat("no bloco pesado")
        self.voa([(lf[0], mp(A1, a1, [0, 1])), (lf[1], mp(A1, a1, [3])), (n3[0], mp(A1, a1, [5])), (la_[0], mp(A1, a1, [6]))], extra=[FadeIn(mp(A1, a1, [2, 4]))], rt=1.2)
        self.pilha.poe(A2)
        self.ate(0.36)
        self.voa([(lf[3], mp(A2, a2, [0])), (lf[2], mp(A2, a2, [2, 3])), (n1[0], mp(A2, a2, [5])), (la_[1], mp(A2, a2, [6]))], extra=[FadeIn(mp(A2, a2, [1, 4]))], rt=1.2)
        rk = VGroup(risco(mp(A1, a1, [2, 3]), FC, 4), risco(mp(A2, a2, [0]), FC, 4))
        self.ate(0.5)
        self.gat("a tração some")
        self.play(Create(rk), mp(A1, a1, [2, 3]).animate.set_color(mix(FC, 0.3)), mp(A2, a2, [0]).animate.set_color(mix(FC, 0.3)), run_time=0.9, sutil=True)   # T e −T riscam juntos
        A4, a4 = M(r"(3-1)", "g", "=", r"(3+1)", "a", size=48, cores={1: ACC, 4: ACC})
        self.pilha.poe(A4)
        self.ate(0.68)
        p0, p3 = mp(A4, a4, [0]), mp(A4, a4, [3])
        self.voa([(mp(A1, a1, [0]), p0[1:2]), (mp(A2, a2, [2]), p0[3:4]), (mp(A1, a1, [1]), mp(A4, a4, [1])),
                  (mp(A1, a1, [5]), p3[1:2]), (mp(A2, a2, [5]), p3[3:4]), (mp(A2, a2, [6]), mp(A4, a4, [4]))],
                 extra=[FadeIn(VGroup(p0[0], p0[2], p0[4], p3[0], p3[2], p3[4], mp(A4, a4, [2])))], rt=1.4)                    # v5 G29: o "=" também no esqueleto
        A5, a5 = eqf(["a", "="], ["g"], ["2"], ["=", r"4{,}9\ \mathrm{m/s^2}"], size=50, cores={("pre", 0): ACC, ("num", 0): ACC, ("post", 1): ACC})
        A5b = caixa_l(A5, ACC)
        self.pilha.poe(A5b)
        self.ate(0.84)
        self.gat("quatro vírgula nove")
        self.passo(A4, A5, (J(a4, 1), a5["num"][0]), (J(a4, 0, 3), a5["bar"] + a5["den"][0]), (J(a4, 2), a5["pre"][1]), (J(a4, 4), a5["pre"][0]),
                   extra=[FadeIn(A5b[0])], rt=1.4)                                   # v5: o a, que cruza a linha toda, parte por último (a linha já se esvaziou)
        self.foco = A5b
        self.ate(0.97)
        # ══ X5-5: o ⊕ desce acelerando (REPLAY) ══
        self.an("X5-5")
        self.pilha.so(E1, A5b, anims=[FadeOut(lf), FadeOut(la_), FadeOut(rk), op_f.animate.set_value(0.0), op_a.animate.set_value(0.0)])
        self.selo("REPLAY", None, rt=0.4)
        solto.set_value(0.0)
        self.play(tb.animate.set_value(0.0), op_trava.animate.set_value(1.0), op_cm.animate.set_value(1.0), estro.animate.set_value(1.0), run_time=0.6)   # travado: 6,0
        self.ate(0.12)
        solto.set_value(1.0)                                                              # v4 §8: o replay começa em "agora repara no centro de massa"
        self.play(tb.animate(rate_func=linear).set_value(TF * 0.97), op_a.animate.set_value(1.0), run_time=2.4)
        self.sem_selo(rt=0.3)
        y3, y1 = ys()
        lv = VGroup(rot("−4,9", 26, ACC).next_to(P3(XA3, max(y3 + 0.15, YB + 0.3 + 0.17)), LEFT, buff=0.2),    # v4 #5: à esquerda da seta (longe da ponta), acima da plataforma
                    rot("+4,9", 26, ACC).next_to(P3(XA1, y1 - 0.15), RIGHT, buff=0.2))
        l0 = VGroup(mtex("a", ACC, 36), rot("= 0", 28, ACC)).arrange(RIGHT, buff=0.08).next_to(l2, DOWN, buff=0.3)      # o suporte não se mexe
        self.play(FadeIn(lv), FadeIn(l0), run_time=0.5)
        B1, b1 = M("6", r"A_{cm}", "=", "3(", r"-4{,}9", ")", "+", "1(", r"4{,}9", ")", "+", "2(", "0", ")", size=46, cores={1: ACC, 4: ACC, 8: ACC, 12: ACC})
        self.pilha.poe(B1)
        self.ate(0.42)
        self.voa([(lM, mp(B1, b1, [0])), (lv[0], mp(B1, b1, [4])), (lv[1], mp(B1, b1, [8])), (l0[1], mp(B1, b1, [12]))],
                 extra=[FadeIn(mp(B1, b1, [1, 2, 3, 5, 6, 7, 9, 10, 11, 13]))], rt=1.3)
        B2, b2 = M(r"A_{cm}", "=", r"-1{,}63\ \mathrm{m/s^2}", size=50, cores={0: ACC, 2: ACC})
        B2b = caixa_l(B2, ACC)
        self.pilha.poe(B2b)
        self.gat("um vírgula sessenta e três")
        self.passo(B1, B2, (J(b1, 1), J(b2, 0)), (J(b1, 2), J(b2, 1)), (J(b1, 0, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13), J(b2, 2)), extra=[FadeIn(B2b[0])], rt=1.3)
        self.foco = B2b
        self.ate(0.97)
        # ══ X5-6: N = M (g + A_cm) → 49 N → 5,0 kg ══
        self.an("X5-6")
        self.pilha.so(E1, B2b, anims=[FadeOut(lv), FadeOut(l0), estro.animate.set_value(0.0), op_a.animate.set_value(0.0)])
        C1, c1 = M("N", "=", "M", r"\,(", "g", "+", r"A_{cm}", ")", size=50, cores={0: FC, 4: ACC, 6: ACC})
        self.pilha.poe(C1)
        self.ate(0.08)
        self.passo(E1, C1, (J(e1, 0), J(c1, 0)), (J(e1, 4), J(c1, 1)), (J(e1, 2) + J(e1, 5), J(c1, 2)), (J(e1, 3), J(c1, 4)), (J(e1, 6), J(c1, 6)), (J(e1, 1), []), rt=1.3)
        C2, c2 = M("=", "6", r"\cdot(", r"9{,}8", "-", r"1{,}63", ")", "=", r"49\ \mathrm{N}", size=48, cores={3: ACC, 5: ACC, 8: FC})
        self.pilha.poe(C2)
        self.ate(0.3)
        self.gat("quarenta e nove newtons")
        self.passo(C1, C2, (J(c1, 1), J(c2, 0)), (J(c1, 2), J(c2, 1)), (J(c1, 3), J(c2, 2)), (J(c1, 4), J(c2, 3)), (J(c1, 5), J(c2, 4)), (J(c1, 6), J(c2, 5)),
                   (J(c1, 7), J(c2, 6)), extra=[FadeIn(mp(C2, c2, [7, 8]))], rt=1.0)
        C3, c3 = M("N", "=", r"49\ \mathrm{N}", size=50, cores={0: FC, 2: FC})
        C3b = caixa_l(C3, FC)
        self.pilha.poe(C3b)
        self.voa([(mp(C2, c2, [8]), mp(C3, c3, [2]))], extra=[FadeIn(C3b[0]), FadeIn(mp(C3, c3, [0, 1]))], rt=0.8)          # v5 G29/G31: a caixa nasce com "N =" e o 49 N desce
        C4, c4 = eqf([], [r"49\ \mathrm{N}"], [r"9{,}8\ \mathrm{m/s^2}"], ["=", r"5{,}0\ \mathrm{kg}"], size=48, cores={("num", 0): FC, ("den", 0): ACC})
        self.pilha.poe(C4)
        self.ate(0.46)
        self.voa([(mp(C3, c3, [2]), gl(C4, c4["num"][0])), (mp(C2, c2, [3]), gl(C4, c4["den"][0])[:3])],
                 extra=[FadeIn(gl(C4, c4["bar"] + sum(c4["post"], []) + c4["den"][0][3:]))], rt=1.0, cada=0.15)
        alvo_m = mrot("5,0 kg", 30, CMC).move_to(tela.get_center())
        self.gat("cinco quilos")
        self._voando_raiz = [alvo_m]
        self.play(TransformFromCopy(gl(C4, c4["post"][1]), alvo_m, rate_func=rush_from), mostra.animate(rate_func=lambda u: min(1.0, 4 * u)).set_value(0.0),
                  run_time=1.0)                                                                           # o 5,0 desce até o mostrador (o número dele some antes)
        self._voando_raiz = []
        self.remove(alvo_m)
        mostra.set_value(1.0)
        self.play(Indicate(tela, color=CMC, scale_factor=1.12), run_time=0.8)
        self.foco = C3b
        self.ate(0.97)
        # ══ X5-7: confere, uma linha por vez ══
        self.an("X5-7")
        self.pilha.limpa(anims=[op_cm.animate.set_value(0.0)])
        self.confere(None)                                                                               # v4 §6: o selo diz só CONFERE; os casos entram na CONTA
        self.play(op_t.animate.set_value(1.0), run_time=0.4)
        tr = VGroup(seta(P3(X3, YP - 0.05), P3(X3, YP - 0.75), FC, 6, tip=0.2), seta(P3(X1, YP - 0.05), P3(X1, YP - 0.75), FC, 6, tip=0.2),
                    mtex("T", FC, 38).next_to(P3(X3, YP - 0.4), LEFT, buff=0.26), mtex("T", FC, 38).next_to(P3(X1, YP - 0.4), RIGHT, buff=0.26))
        self.gat("a tração no fio")
        self.play(FadeIn(tr), run_time=0.6)                                                              # as duas trações puxam a polia
        D1, d1 = eqf(["T", "="], [r"2\cdot 3\cdot 1\cdot ", "{g}"], ["4"], ["=", r"14{,}7\ \mathrm{N}"], size=46, cores={("pre", 0): FC, ("num", 1): ACC, ("post", 1): FC})
        D2, d2 = M("N", "=", r"2\cdot ", r"9{,}8", "+", r"2\cdot ", r"14{,}7", "=", r"49\ \mathrm{N}", size=46, cores={0: FC, 3: ACC, 6: FC, 8: FC})
        self.pilha.poe(D1)
        self.ate(0.1)
        self.voa([(tr[2], gl(D1, d1["pre"][0]))], extra=[FadeIn(gl(D1, d1["pre"][1] + sum(d1["num"], []) + d1["bar"] + d1["den"][0] + sum(d1["post"], [])))], rt=1.0)
        self.ate(0.25)
        self.pilha.poe(D2)
        self.voa([(gl(D1, d1["post"][1][:4]), mp(D2, d2, [6]))], extra=[FadeIn(mp(D2, d2, [0, 1, 2, 3, 4, 5, 7, 8]))], rt=1.1)
        self.gat("quarenta e nove newtons de novo")
        self.play(FadeOut(tr), op_t.animate.set_value(0.0), run_time=0.4)
        self.ate(0.47)
        D3 = linha_m("MASSAS IGUAIS:", M("a", "=", "0", size=46, cores={0: ACC})[0], MathTex(r"\Rightarrow", font_size=46), rot("6,0 kg", 32, CMC))
        D3[2]._partes = [(r"\Rightarrow", WHITE_)]
        self.pilha.poe(D3)
        self.gat("com blocos iguais")
        override.set_value(1.0)
        leitura.set_value(5.0)
        self.play(FadeIn(D3[0]), yo.animate.set_value(1.0), w3.animate.set_value(0.75), w1.animate.set_value(0.75), rot3.animate.set_value(1.0),
                  rot1.animate.set_value(1.0), run_time=1.0)                                             # os blocos viram 2 kg + 2 kg (tamanho e rótulo)
        self.wait(0.3)
        leitura.set_value(6.0)
        self.play(FadeIn(D3[1:]), Indicate(tela, color=CMC, scale_factor=1.12), run_time=0.9)            # e só então o mostrador volta a 6,0
        self.ate(0.66)
        self.selo("TRAVADO", None, rt=0.3)                                                              # v5 G33: voltam a 3 kg e 1 kg, travados (6,0)
        solto.set_value(0.0)
        self.play(w3.animate.set_value(L3), w1.animate.set_value(L1), rot3.animate.set_value(0.0), rot1.animate.set_value(0.0), run_time=0.6)
        D4 = linha_m("BLOCO LEVE → 0", MathTex(r"\Rightarrow", font_size=46), rot("2,0 kg", 32, CMC))
        D4[1]._partes = [(r"\Rightarrow", WHITE_)]
        self.pilha.poe(D4)
        self.gat("se o bloco leve fosse sumindo")
        self.sem_selo(rt=0.25)
        solto.set_value(1.0)                                                                             # a trava se abre de novo (os blocos ficam onde estão)
        leve.set_value(1.0)
        self.play(FadeIn(D4[0]), w1.animate.set_value(0.0), run_time=0.9)                                # o leve encolhe até sumir
        leitura.set_value(2.0)
        self.play(queda.animate(rate_func=lambda u: u * u).set_value(0.7), op_fio.animate.set_value(0.0), FadeIn(D4[1:]),
                  Indicate(tela, color=CMC, scale_factor=1.12), run_time=0.9)                             # o pesado cai livre; a balança marca só o suporte
        self.foco = D4
        self.ate(0.97)
        # ══ X5-8: dica ══
        self.an("X5-8")
        leve.set_value(0.0)
        cav, _ = cavalo(0.0, 0.0)
        cav = silhueta_cav(cav).scale(0.45)
        mini = VGroup(cav, elevador()).arrange(RIGHT, buff=0.9)
        mini.move_to(P3(X_CONTA + mini.width / 2, TOPO_PILHA - mini.height / 2))
        self.pilha.limpa(anims=[w1.animate.set_value(L1), w3.animate.set_value(L3), yo.animate.set_value(0.0), queda.animate.set_value(0.0),
                                op_fio.animate.set_value(1.0), FadeIn(mini, rate_func=lambda u: min(1.0, max(0.0, (u - 0.7) / 0.3)))], rt=0.8)   # volta ao estado real; v5 G32: a miniatura nasce no fim do apagar
        override.set_value(0.0)
        self.pilha.poe(mini)
        self.dica18(["SE O CENTRO DE MASSA ACELERA PARA BAIXO,", "O APOIO EMPURRA MENOS"])
        self.foco = mini
        # v7: a dica ganha a imagem da fala — o ⊕ desce e o mostrador cai em "acelera para baixo, o apoio empurra menos"; o ⊕ sobe e o mostrador sobe em
        # "acelera para cima, empurra mais"; o elevador e o cavalo acendem nas palavras deles.
        solto.set_value(0.0)
        tb.set_value(0.0)
        self.play(op_cm.animate.set_value(1.0), op_trava.animate.set_value(1.0), run_time=0.5)
        self.gat("acelera para baixo")
        solto.set_value(1.0)                                                                                # o mesmo quadro: trava aberta e mostrador em 5,0
        self.play(tb.animate(rate_func=linear).set_value(TF * 0.97), Indicate(tela, color=CMC, scale_factor=1.0), run_time=2.6)
        self.gat("acelera para cima")
        override.set_value(1.0)
        leitura.set_value(5.0)
        self.play(tb.animate(rate_func=linear).set_value(0.0), run_time=2.2)                            # o ⊕ sobe (os blocos voltam)
        leitura.set_value(6.0)                                                                           # o mostrador sobe a 6,0 de uma vez (só 5,0 e 6,0 aparecem)
        self.play(Indicate(tela, color=CMC, scale_factor=1.0), run_time=0.6)
        solto.set_value(0.0)
        override.set_value(0.0)
        self.gat("do elevador")
        self.play(Indicate(mini[1], color=CYAN, scale_factor=1.0), run_time=0.9)
        self.gat("do cavalo")
        self.play(Indicate(mini[0], color=CYAN, scale_factor=1.0), run_time=0.9)
        self.ate(0.97)
        override.set_value(0.0)


def elevador():
    """Cabine (aço) com cabos, uma pessoa de pé (silhueta limpa) e a aceleração para baixo no ⊕ da pessoa."""
    cab = aco(RoundedRectangle(corner_radius=0.06, width=1.35, height=2.05), 2.0)
    dentro = RoundedRectangle(corner_radius=0.04, width=1.1, height=1.8).set_fill("#0A1430", 1).set_stroke("#5A6476", 1.2)
    cabos = VGroup(*[Line(P3(x, 1.02), P3(x, 1.45)).set_stroke(GEO, 2) for x in (-0.25, 0.25)])
    pes = silhueta(PessoaPerfil(0.0, 0.0, 1.45, 1, "pe")).move_to(P3(-0.12, -0.1))
    c = pes.get_center() + P3(0, 0.05)
    cmk = marcador_cm(c, r=0.12, z=40)
    a_ = seta(c + P3(0.38, 0.25), c + P3(0.38, -0.55), ACC, 5, tip=0.18)
    return VGroup(cabos, cab, dentro, pes, cmk, a_)


def silhueta_cav(g):
    for m in g.family_members_with_points():
        if isinstance(m, VMobject):
            m.set_fill("#7A8696", opacity=max(m.get_fill_opacity(), 0.0))
    return g

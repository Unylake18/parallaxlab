"""Lote PE3: E3 — a esteira de areia (2D). ESQUEMA fixo: esteira de aço sobre roletes, piso com grade, funil despejando areia na vertical.
Física (visto do chão): esteira a v = 1,5 m/s; cada grão chega com velocidade horizontal 0 e escorrega com desaceleração relativa μ g (μ = 0,5):
escorrega 0,31 s e 0,23 m em relação à esteira, depois anda com ela. Escala da tela: 0,6 unidade por metro, tempo real.
E3-2: SISTEMA na porção de areia; FC: atrito da esteira na areia (frente), reação na esteira (trás), motor no rolete. 30 N.
E3-3: 45 W × 22,5 W (+ 22,5 W em laranja). E3-4: inset do grão visto do chão e no referencial da esteira (chega a 1,5 m/s para trás,
escorrega e para, rastro laranja)."""
from pecas19 import *  # noqa: F401,F403

VEX_C = VREL
ESC = 0.6                       # unidades de tela por metro
VB = 1.5 * ESC                  # velocidade da esteira na tela
A_ATR = 0.5 * 9.8 * ESC         # μ g na tela
T_ESC = VB / A_ATR              # 0,306 s
XF, YT = -4.2, -1.0             # funil (x) e topo da esteira (y)
X0E, X1E = -6.6, 1.1
A_EXIT = None                  # instante (desde a chegada) em que o grão sai pela ponta da esteira


def _aexit():
    return T_ESC + (X1E - XF - 0.5 * A_ATR * T_ESC ** 2) / VB


def x_grao(t, t0):
    """x do grão (visto do chão) que tocou a esteira em t0."""
    a = t - t0
    if a <= 0:
        return XF
    if a < T_ESC:
        return XF + 0.5 * A_ATR * a * a
    return XF + 0.5 * A_ATR * T_ESC ** 2 + VB * (a - T_ESC)


class LoteE3(Prob2):
    FUNDO = "fundo_lab_ex.png"

    def construct(self):
        self.setup_base()
        self.layout_v = True                                            # esteira larga: sem divisão ESQUEMA × CONTA
        self.pilha = Pilha(self, x0=2.0, larg=5.2)
        self.e3()
        self.fim()
        self.relatorio()
        self.gravar_reg()

    def e3(self):
        self.an("E3-1")
        self.secao("EXERCÍCIO 3 · A ESTEIRA DE AREIA")
        clk = self.clk
        rng = np.random.default_rng(21)
        T_TOT = sum(dur(a) for a in ("E3-1", "E3-2", "E3-3", "E3-4", "E3-5")) + 5
        n_g = int(T_TOT * 12.0)
        chegadas = (np.arange(n_g) + rng.uniform(-0.45, 0.45, n_g)) / 12.0 + 0.2                  # chegadas irregulares (12 grãos/s, como no T1)
        jit = rng.uniform(-0.07, 0.07, len(chegadas))
        rads = rng.uniform(0.015, 0.03, len(chegadas))                  # grãos de 2–4 px
        A_EX = _aexit()
        H_QUEDA, G_V = 2.3, 6.0
        t_q = math.sqrt(2 * H_QUEDA / G_V)
        op_sis = ValueTracker(0.0)
        self.add(op_sis)
        self.t_porcao = None
        CICLO = 4.2                                                    # a porção acompanhada recomeça no funil a cada ciclo (fica na esteira)

        def t_p(t):
            if self.t_porcao is None:
                return None
            return self.t_porcao + CICLO * math.floor(max(0.0, t - self.t_porcao) / CICLO)

        def op_ciclo(t):
            if self.t_porcao is None:
                return 0.0
            f = (t - t_p(t)) / CICLO
            return min(1.0, f / 0.06, (1 - f) / 0.06)
        self.t_p, self.op_ciclo = t_p, op_ciclo

        def esteira():
            t = clk.get_value()
            g = VGroup(piso_grade(-7.35, 0.2, -2.55, prof=0.4))
            g.add(RoundedRectangle(corner_radius=0.32, width=X1E - X0E + 0.64, height=0.64).move_to(P3((X0E + X1E) / 2, YT - 0.32)).set_stroke("#9AA6B8", 5).set_fill(opacity=0))
            for xr in np.linspace(X0E, X1E, 6):
                g.add(aco(Circle(radius=0.26).move_to(P3(xr, YT - 0.32)), 1.6), Dot(P3(xr, YT - 0.32), radius=0.05, color=GEO))
            for xm in np.arange(X0E - 0.6 + (VB * t) % 0.6, X1E + 0.01, 0.6):            # marcas da lona andando
                if X0E <= xm <= X1E:
                    g.add(Line(P3(xm, YT - 0.02), P3(xm, YT + 0.06)).set_stroke(GEO, 2, opacity=0.8))
            g.add(Line(P3(X0E - 0.4, -2.55), P3(X0E - 0.4, YT - 0.32)).set_stroke("#4A5262", 4), Line(P3(X1E + 0.4, -2.55), P3(X1E + 0.4, YT - 0.32)).set_stroke("#4A5262", 4))
            # funil fixo
            g.add(aco(Polygon(P3(XF - 0.55, 1.9), P3(XF + 0.55, 1.9), P3(XF + 0.1, 1.35), P3(XF - 0.1, 1.35)), 1.8))
            # grãos: caindo (vertical) e na esteira
            for t0, j, rd in zip(chegadas, jit, rads):
                a = t - (t0 - t_q)
                if a < 0:
                    continue
                if t < t0:
                    y = 1.3 - 0.5 * G_V * a * a
                    g.add(Dot(P3(XF + j * 0.5, y), radius=rd, color=SAND))
                else:
                    x = x_grao(t, t0) + j
                    if x < X1E:
                        g.add(Dot(P3(x, YT + 0.03 + abs(j) * 0.5), radius=rd, color=SAND))
                    else:
                        pass                                            # v5 #62: o grão some atrás do rolete (nada solto no vazio)
            # porção acompanhada (SISTEMA)
            o = op_sis.get_value()
            if o > 0.01 and self.t_porcao is not None:
                tp = t_p(t)
                xs = x_grao(t, tp)
                oc = o * op_ciclo(t)
                oc = oc * min(1.0, max(0.0, (xs - XF - 0.35) / 0.3))
                if oc > 0.01:
                    g.add(DashedVMobject(RoundedRectangle(corner_radius=0.14, width=1.76, height=1.2).move_to(P3(xs + 0.05, YT + 0.55)), num_dashes=30).set_stroke(WHITE_, 2.4, opacity=0.9 * oc))
                    g.add(seta(P3(xs - 0.3, YT + 1.4), P3(xs - 0.3 + VB, YT + 1.4), VEL, 6, tip=0.2, op=oc))      # a porção sai andando a 1,5 m/s
                self.reg("esteira", t=t, x=xs, v=(min(t - tp, T_ESC) * A_ATR if t >= tp else 0.0))
            return g
        ev = vivo(esteira)
        q = VGroup(txt("QUE FORÇA FAZ O MOTOR?", 28, bold=True), txt("COM QUE POTÊNCIA?", 28, bold=True)).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        self.pilha.poe(q)
        self.play(FadeIn(ev), FadeIn(q), run_time=0.8)                                    # v6: a pergunta já entra com a esteira
        self.pede("MASSA QUE ENTRA")
        sv = arrow(P3(-6.7, YT - 0.95), P3(-6.7 + VB, YT - 0.95), VEL, 7, tip=0.22)
        lv = VGroup(MathTex("v=", font_size=40, color=VEL), rot("1,5 m/s", 30, VEL)).arrange(RIGHT, buff=0.08).next_to(sv, RIGHT, buff=0.15)
        ldm = VGroup(MathTex(r"\left|\frac{dm}{dt}\right|=", font_size=36, color=MAS), rot("20 kg/s", 26, MAS)).arrange(RIGHT, buff=0.1).next_to(P3(XF - 0.35, 0.7), LEFT, buff=0.1)
        self.gat("vinte quilos por segundo")
        self.play(FadeIn(ldm), run_time=0.6)
        self.gat("a esteira anda")
        self.play(GrowArrow(sv), FadeIn(lv), run_time=0.6)
        self.gat("a areia cai na vertical")
        self.hip([["AREIA CHEGA PARADA · ESTEIRA A VELOCIDADE CONSTANTE"]], x0=-5.8, wmax=11.0)
        self.gat("que força o motor")
        self.play(Indicate(q, color=WHITE_, scale_factor=1.04), run_time=0.6)
        self.ate(0.97)
        # ── E3-2 ──
        self.an("E3-2")
        self.pilha.limpa(rt=0.3)
        self.sem_selo()
        self.t_porcao = clk.get_value() + 0.3
        self.gat("escolhe o sistema seguindo a areia")
        self.t_porcao = clk.get_value() + 0.05
        self.play(op_sis.animate.set_value(1.0), run_time=0.6)
        ls = txt("SISTEMA", 24)
        def pos_s(m):
            t = clk.get_value()
            m.move_to(P3(x_grao(t, t_p(t)) + 0.85, YT + 1.85))
            m.set_opacity(op_ciclo(t) * min(1.0, max(0.0, (x_grao(t, t_p(t)) - XF - 0.35) / 0.3)))
        pos_s(ls)
        self.play(FadeIn(ls), run_time=0.3)
        ls.add_updater(pos_s)
        A, ia = M(r"20\ \mathrm{kg/s}", r"\cdot", r"(1{,}5-0)\ \mathrm{m/s}", "=", r"30\ \mathrm{kg\cdot m/s}", size=46, cores={2: VEL, 4: MAG})
        A.scale_to_fit_width(min(A.width, 5.1))
        Ab = txt("DE MOMENTO, A CADA SEGUNDO", 24)
        self.pilha.poe(A)
        self.pilha.poe(Ab)
        self.gat("chegam vinte quilos")
        self.voa([(ldm[1][:2], mp(A, ia, [0])[:2]), (lv[1][:3], mp(A, ia, [2])[1:4])], extra=[FadeIn(mp(A, ia, [0])[2:]), FadeIn(mp(A, ia, [1])), FadeIn(mp(A, ia, [2])[:1]), FadeIn(mp(A, ia, [2])[4:])], rt=1.0, arco_esq=-0.5)
        self.gat("trinta quilogramas metro por segundo")
        self.play(FadeIn(mp(A, ia, [3, 4])), FadeIn(Ab), run_time=0.7)
        # setas FC: atrito na areia (frente), reação na esteira (trás), motor no rolete
        xp = lambda: x_grao(clk.get_value(), t_p(clk.get_value()))
        B, ib = M(r"F_{esteira\to areia}", "=", r"30\ \mathrm{N}", size=46, cores={0: FC, 2: FC})
        self.pilha.poe(B)
        self.gat("isso é uma força de trinta newtons")
        self.play(FadeIn(B), run_time=0.6)
        op_x = lambda: op_ciclo(clk.get_value()) * min(1.0, max(0.0, (xp() - XF - 0.35) / 0.3))     # só depois que a porção sai de baixo do funil
        fa = vivo(lambda: VGroup(seta(P3(xp() - 0.35, YT + 0.38), P3(xp() + 0.45, YT + 0.38), FC, 6, tip=0.2, op=op_x())))              # G33: nasce na porção
        self.play(FadeIn(fa), run_time=0.4)
        C = linha_m(txt("3ª LEI:", 26, bold=True), M(r"F_{areia\to esteira}", "=", r"30\ \mathrm{N}", size=46, cores={0: FC, 2: FC})[0], buff=0.2)
        C2 = txt("PARA TRÁS", 26)
        self.pilha.poe(C)
        self.pilha.poe(C2)
        self.gat("por ação e reação")
        fr = vivo(lambda: VGroup(seta(P3(xp() + 0.6, YT - 0.82), P3(xp() - 0.3, YT - 0.82), FC, 6, tip=0.2, op=op_x())))              # na superfície da esteira, logo abaixo da porção
        self.play(FadeIn(C), FadeIn(C2), FadeIn(fr), run_time=0.8)
        D = linha_m(txt("v CONSTANTE →", 26, bold=True), M(r"F_{motor}", "=", r"30\ \mathrm{N}", size=46, cores={0: FC, 2: FC})[0], buff=0.2)
        self.pilha.poe(D)
        anel_m = Circle(radius=0.36).move_to(P3(X1E, YT - 0.32)).set_stroke(FC, 3.5)                   # o rolete motor (o da direita) em destaque
        fm = arrow(P3(X1E + 0.05, YT - 0.32), P3(X1E + 1.0, YT - 0.32), FC, 7, tip=0.22)               # a força nasce no rolete motor
        lm = txt("MOTOR", 24, color=FC).move_to(P3(X1E - 0.45, YT - 1.0))
        self.gat("o motor tem que compensar")
        Dn = VGroup(txt("PELA EQUAÇÃO GERAL:", 24), M("F", "=", "v", r"\left|\frac{dm}{dt}\right|", size=46, cores={0: FC, 2: VEL})[0]).arrange(DOWN, buff=0.1, aligned_edge=LEFT)      # v7 #40: duas linhas
        self.pilha.poe(Dn)
        self.play(FadeIn(D), FadeIn(anel_m), GrowArrow(fm), FadeIn(lm), FadeIn(Dn), run_time=0.8)               # fica na tela até o fim do bloco (≥ 3 s legível)
        self.foco = D
        self.ate(0.97)
        # ── E3-3: potência ──
        self.an("E3-3")
        ls.clear_updaters()
        self.play(FadeOut(fa), FadeOut(fr), FadeOut(ls), op_sis.animate.set_value(0.0), run_time=0.4)
        fa.clear_updaters()
        fr.clear_updaters()
        self.remove(fa, fr, ls)
        self.pilha.limpa(rt=0.3)
        E, ie = M(r"P_{motor}", "=", r"F\,v", size=46, cores={0: KC})
        pinta(E, ie, 2, [(0, FC), (1, VEL)])
        E2, ie2 = M("=", r"30\cdot 1{,}5", "=", r"45\ \mathrm{W}", size=46, cores={3: KC})
        pinta(E2, ie2, 1, [(0, FC), (1, FC), (3, VEL), (4, VEL), (5, VEL)])
        self.pilha.poe(E)
        self.pilha.poe(E2)
        self.gat("a potência é força vezes velocidade")
        self.play(FadeIn(E), run_time=0.6)
        self.play(FadeIn(E2), run_time=0.6)
        F_, if_ = M(r"\frac{dK}{dt}", "=", r"\tfrac12\left|\frac{dm}{dt}\right|v^2", size=46, cores={0: KC})
        F2, if2 = M("{}=", r"\tfrac12\cdot 20\cdot 1{,}5^2", "=", r"22{,}5\ \mathrm{W}", size=46, cores={3: KC})
        F2.scale_to_fit_width(min(F2.width, 5.05))                                          # v7 #42: x <= 912 px (linha alinhada à esquerda, não mais sob o "=" da mãe)
        self.pilha.poe(F_)
        self.pilha.poe(F2, dx=0.1)
        self.gat("a energia cinética que a areia ganha")
        self.voa([(ldm[1][:2], mp(F2, if2, [1])[4:6]), (lv[1][:3], mp(F2, if2, [1])[7:10])], extra=[FadeIn(mp(F_, if_, [0, 1, 2])), FadeIn(mp(F2, if2, [0])), FadeIn(mp(F2, if2, [1])[:4]), FadeIn(mp(F2, if2, [1])[6:7]), FadeIn(mp(F2, if2, [1])[10:])], rt=1.0, arco_esq=-0.5)
        self.play(FadeIn(mp(F2, if2, [2, 3])), run_time=0.5)
        # barras: 45 W do motor (ciano), 22,5 W da areia (ciano) e a diferença em laranja com "?"
        yb, kb = -3.4, 1.9 / 45.0                                        # uma barra empilhada: MOTOR 45 W = K da areia (ciano) + o resto (laranja)
        xB = 3.0
        b1 = Rectangle(width=0.8, height=45 * kb).move_to(P3(xB, yb + 45 * kb / 2)).set_stroke(FC, 3).set_fill(opacity=0)
        b2 = Rectangle(width=0.8, height=22.5 * kb).move_to(P3(xB, yb + 22.5 * kb / 2)).set_stroke(width=0).set_fill(KC, 0.9)
        b3 = Rectangle(width=0.8, height=22.5 * kb).move_to(P3(xB, yb + 22.5 * kb * 1.5)).set_stroke(HEAT, 2).set_fill(HEAT, 0.85)
        lb1 = VGroup(txt("MOTOR", 24, color=FC), rot("45 W", 26, FC)).arrange(RIGHT, buff=0.14).move_to(P3(xB + 0.5 + 1.0, yb + 45 * kb + 0.2))
        lb2 = VGroup(txt("K DA AREIA", 24), rot("22,5 W", 26, KC)).arrange(RIGHT, buff=0.14).next_to(P3(xB + 0.5, yb + 22.5 * kb / 2), RIGHT, buff=0.12)
        lb3 = VGroup(rot("22,5 W", 26, HEAT), MathTex("?", font_size=46, color=HEAT)).arrange(RIGHT, buff=0.12).next_to(P3(xB + 0.5, yb + 22.5 * kb * 1.5), RIGHT, buff=0.12)
        self.gat("exatamente a metade")
        self.play(FadeIn(b1), FadeIn(lb1), FadeIn(b2, shift=0.2 * UP), FadeIn(lb2), run_time=0.8)
        self.gat("para onde foi o resto")
        self.play(FadeIn(b3), FadeIn(lb3), run_time=0.7)
        self.reg("e3_3", P=45.0, K=22.5)
        self.foco = lb3
        self.ate(0.97)
        # ── E3-4: o grão no referencial da esteira ──
        self.an("E3-4")
        self.pilha.limpa(rt=0.3)
        u, modo = ValueTracker(0.0), ValueTracker(0.0)                 # modo 0: visto do chão · 1: no referencial da esteira
        self.add(u, modo)
        cx, cy, Z = -3.2, -2.92, 5.0                                   # inset embaixo, sob o piso (52% da largura), longe da cena e das barras: zoom 5×

        def inset():
            t = u.get_value()
            chao = modo.get_value() < 0.5
            g = VGroup(RoundedRectangle(corner_radius=0.1, width=8.4, height=1.1).move_to(P3(cx, cy)).set_stroke(GEO, 1.5, opacity=0.6).set_fill(PANEL, 0.6))
            g.add(Rectangle(width=8.0, height=0.26).move_to(P3(cx, cy - 0.42)).set_stroke("#9AA6B8", 3).set_fill("#3A4252", 1))
            vlon = VB * Z if chao else 0.0
            for xm in np.arange(-3.9 + (vlon * t) % 0.7, 3.9, 0.7):
                g.add(Line(P3(cx + xm, cy - 0.55), P3(cx + xm, cy - 0.29)).set_stroke(GEO, 2))
            a_ = max(0.0, t - 0.5)                                     # uma passagem por referencial (sem loop)
            if chao:                                                   # o grão chega parado e acelera até a esteira, e sai andando com ela
                xg = -3.7 + (0.5 * A_ATR * min(a_, T_ESC) ** 2 + VB * max(0.0, a_ - T_ESC)) * Z
                og = 1.0 if xg < 3.8 else 0.0
                if og:
                    g.add(Dot(P3(cx + xg, cy - 0.16), radius=0.14, color=SAND).set_z_index(5))
                    if a_ > T_ESC:
                        g.add(seta(P3(cx + xg - 0.1, cy + 0.28), P3(cx + xg - 0.1 + VB * 1.3, cy + 0.28), VEL, 6, tip=0.2))
            else:                                                      # chega a 1,5 m/s para trás, escorrega e para: o rastro laranja fica
                d = VB * min(a_, T_ESC) - 0.5 * A_ATR * min(a_, T_ESC) ** 2
                xg = 2.0 - d * Z
                if a_ > 0:
                    g.add(Line(P3(cx + 2.0, cy - 0.22), P3(cx + xg, cy - 0.22)).set_stroke(HEAT, 7, opacity=0.85))
                if a_ < T_ESC:
                    g.add(seta(P3(cx + xg - 0.1, cy + 0.28), P3(cx + xg - 0.1 - VB * 1.3, cy + 0.28), VEL, 6, tip=0.2))
                g.add(Dot(P3(cx + xg, cy - 0.16), radius=0.14, color=SAND).set_z_index(5))
            return g
        iv = vivo(inset)
        self.play(FadeIn(iv), FadeOut(VGroup(ldm)), run_time=0.6)               # as barras do E3-3 ficam na tela (lado direito)
        self.referencial("DO CHÃO", pos=2.75)
        self.ref_mob.move_to(P3(-4.25 + self.ref_mob.width / 2, 2.75))
        self.gat("quando o grão cai na esteira")
        self.play(u.animate(rate_func=linear).set_value(4.4), run_time=4.4)
        self.gat("agora olha do referencial da esteira")
        modo.set_value(1.0)
        u.set_value(0.0)
        novo_ref = self.referencial("NO REFERENCIAL DA ESTEIRA", pos=2.45) if False else None
        self.ref_mob_txt = None
        self.referencial(None)
        rs = txt("NO REFERENCIAL DA ESTEIRA", 24, bold=True)
        bx = RoundedRectangle(corner_radius=0.1, width=rs.width + 0.3, height=rs.height + 0.18).move_to(rs).set_fill(PANEL, 0.9).set_stroke(VEL, 2)
        bx._fundo = True
        selo_ref = VGroup(bx, rs).set_z_index(36)
        selo_ref._selo = "ref"
        selo_ref.move_to(P3(-4.25 + selo_ref.width / 2, 2.75))
        self.ref_mob, self.ref_atual = selo_ref, "NO REFERENCIAL DA ESTEIRA"
        self.play(FadeIn(selo_ref), run_time=0.4)
        G1 = linha_m(txt("CADA", 26), MathTex("dm", font_size=46), txt("PERDE", 26), MathTex(r"\tfrac12\,dm\,v^2", font_size=46), buff=0.15)
        G1[3][0][5:6].set_color(VEL)
        G1b = tx("→ CALOR", 26, color=HEAT)
        self.pilha.poe(G1)
        self.pilha.poe(G1b, dx=0.3)
        self.gat("chega a um vírgula cinco")
        lb3n = VGroup(txt("CALOR", 24, color=HEAT), rot("22,5 W", 26, HEAT)).arrange(RIGHT, buff=0.12).move_to(lb3)
        lb3n.align_to(lb3, LEFT)
        self.play(FadeIn(G1), FadeIn(G1b), FadeOut(lb3), FadeIn(lb3n), Indicate(b3, color=WHITE_, scale_factor=1.08), u.animate(rate_func=linear).set_value(2.2), run_time=2.2)
        self.play(u.animate(rate_func=linear).set_value(4.4), run_time=2.2)
        G2 = VGroup(txt("NÃO DEPENDE DO", 28, bold=True), txt("COEFICIENTE DE ATRITO", 28, bold=True)).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        self.pilha.poe(G2)
        self.gat("não depende do coeficiente de atrito")
        self.play(FadeIn(G2), u.animate(rate_func=linear).set_value(6.6), run_time=2.2)
        resto = max(0.5, self.resta() - 0.1)
        self.play(u.animate(rate_func=linear).set_value(6.6 + resto), run_time=resto)
        self.ate(0.99)
        # ── E3-5 ──
        self.an("E3-5")
        self.play(FadeOut(iv), FadeOut(selo_ref), run_time=0.4)               # o inset sai com a entrada do CONFERE; as barras ficam
        iv.clear_updaters()
        self.remove(iv)
        self.ref_mob = None
        self.confere([[MathTex(r"(\mathrm{kg/s})\cdot(\mathrm{m/s})^2", font_size=34), "= J/s = W", MathTex(r"\checkmark", font_size=34)]], x0=-2.0, wmax=9.4)
        self.gat("e a dica")
        self.dica18([["MOTOR PAGA 2 ×", MathTex("K", font_size=36, color=KC), "ENTREGUE"]])
        self.ate(0.97)

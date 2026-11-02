"""Lote PT3: T3 — quanta velocidade o combustível compra. T3-1 (barra de massa que esvazia; inset do mesmo cubinho de gás num foguete cheio e
num quase vazio: setas dv 1 : 5; a integral), T3-2 (Tsiolkovsky em PANEL, R = razão de massas), T3-3 (CONFERE: os dois limites), T3-4 (v × t de
dois foguetes, 10 s e 10 min, mesmo eixo de v, o mesmo Δv), T3-5 (Δv/v_ex × R, marcas em e, e², e³ e setas ×e), T3-6 (3 e 9 km/s → R = e³ ≈ 20
→ 95%), T3-7/T3-8 (Three.js 'esp': a mesma SimEsp, cor de cada partícula pelo sentido visto de fora, fixada no nascimento; medidor v/v_ex).
T3-7/T3-8: a queima inteira em 24 s de tela (fator constante FAT3 = 80/24): o cruzamento v = v_ex cai no fim do T3-7 e o empuxo continua no
começo do T3-8 (com 12 s a queima acabaria antes do T3-8; ver qa.txt)."""
from pecas19 import *  # noqa: F401,F403

FAT3 = 80.0 / 24.0
VEX_C = VREL


class LoteT3(Prob2):
    FUNDO = "fundo_lab_ex.png"

    def construct(self):
        self.setup_base()
        self.sim = SimEsp()
        self.t3_conta()
        self.t3_graficos()
        self.t3_numeros()
        self.t3_esp()
        self.fim()
        self.relatorio()
        self.gravar_reg()

    # ── T3-1 a T3-3 ──
    def t3_conta(self):
        self.an("T3-1")
        self.secao("QUANTA VELOCIDADE O COMBUSTÍVEL COMPRA?")
        fg = foguete2d(3.9, 0.7).shift(P3(-6.2, -3.0))
        xb, yb, H = -4.75, -3.0, 3.9
        mm = ValueTracker(1.0)                                          # m/m₀ (vai a 0,2: R = 5)
        self.add(mm)

        def barra():                                                    # a mesma barra do hook: propelente (azul) embaixo, estrutura (aço), carga (branca) em cima
            f = mm.get_value()
            g, y = VGroup(), yb
            for h_, c_ in ((H * max(0.0, f - 0.2), MAS), (H * 0.15, STEEL), (H * 0.05, WHITE_)):
                if h_ > 0.002:
                    g.add(Rectangle(width=0.5, height=h_).move_to(P3(xb, y + h_ / 2)).set_stroke(width=0).set_fill(c_, 1.0 if c_ == WHITE_ else 0.9))
                y += h_
            g.add(Rectangle(width=0.5, height=H).move_to(P3(xb, yb + H / 2)).set_stroke(GEO, 2, opacity=0.8).set_fill(opacity=0))
            return g.set_z_index(3)
        bv = vivo(barra)
        lm0 = MathTex("m_0", font_size=40, color=MAS).next_to(P3(xb - 0.25, yb + H), LEFT, buff=0.15)
        lm = MathTex("m", font_size=40, color=MAS)
        lm.add_updater(lambda m_: m_.next_to(P3(xb + 0.25, yb + H * mm.get_value()), RIGHT, buff=0.22))        # acompanha o nível enquanto a barra esvazia
        lm.next_to(P3(xb + 0.25, yb + H), RIGHT, buff=0.22)
        self.play(FadeIn(fg), FadeIn(bv), FadeIn(lm0), FadeIn(lm), run_time=0.8)
        self.gat("queimando todo o propelente")
        self.play(mm.animate(rate_func=linear).set_value(0.2), run_time=1.6)                    # o propelente vai esvaziando desde o começo do bloco
        kx = ValueTracker(0.0)                                          # setas v_ex e Δv do CONFERE (encolhem até sumir)
        self.add(kx)
        sxv = vivo(lambda: VGroup(seta_tr(P3(-6.2, -3.05), P3(-6.2, -3.05 - 0.6 * kx.get_value()), VEX_C, 7, tip=0.24),
                                  seta(P3(-6.2, 1.2), P3(-6.2, 1.2 + 1.5 * kx.get_value()), VEL, 7, tip=0.24)))
        lvx = MathTex(r"v_{ex}", font_size=40, color=VEX_C).move_to(P3(-5.4, -3.3))
        ldvx = MathTex(r"\Delta v", font_size=40, color=VEL).move_to(P3(-5.5, 2.2))
        for m_ in (lvx, ldvx):
            m_.add_updater(lambda q_: q_.set_opacity(min(1.0, 8.0 * kx.get_value())))
        self.add(sxv, lvx, ldvx)
        A, ia = M("m", r"\,dv", "=", "-", r"v_{ex}", r"\,dm", size=50, cores={1: VEL, 4: VEX_C})
        self.pilha.poe(A)
        self.gat("volta na equação")
        lm.clear_updaters()
        self.voa([(lm, mp(A, ia, [0]))], extra=[FadeIn(mp(A, ia, [1, 2, 3, 4, 5]))], rt=1.0, origem=False)
        self.remove(lm)
        B, ib = M("dv", "=", "-", r"v_{ex}", r"\frac{dm}{m}", size=50, cores={0: VEL, 3: VEX_C})
        self.pilha.poe(B)
        self.gat("passa a massa para o outro lado")
        self.play(FadeIn(B, shift=0.1 * UP), run_time=0.9)                                   # G34: a linha nova entra sem a sopa de glifos do passo
        # inset: o mesmo cubinho de gás num foguete cheio e num quase vazio (setas dv 1 : 5)
        self.gat("repara no que isso diz")
        ins = VGroup()
        for k, (y, f, nome) in enumerate(((0.9, 1.0, "CHEIO"), (-1.6, 0.2, "QUASE VAZIO"))):
            ff = fog_h(3.7, 0.74, bocal=P3(-2.7 + 5.0 * k, -2.5))
            nv = Rectangle(width=2.4, height=0.3).move_to(ff.meio + P3(0.2, 0)).set_stroke(width=0).set_fill(MAS, 0.65)
            nv.stretch_to_fit_width(2.4 * f).align_to(nv, LEFT)
            cub = Square(0.26).move_to(ff.bocal + P3(-0.7, 0)).set_fill(MAS, 1).set_stroke(MAS, 1)
            Ldv = 0.5 / f
            sd = arrow(ff.nariz + P3(-2.3, 0.95), ff.nariz + P3(-2.3 + Ldv, 0.95), VEL, 7, tip=0.22)
            ldv = MathTex("dv", font_size=40, color=VEL).next_to(sd, RIGHT if k == 0 else UP, buff=0.14)
            nm = txt(nome, 26, color=DIM).next_to(ff, DOWN, buff=0.3)
            self.reg(f"inset{k}", k=k, massa=f, seta=Ldv)
            ins.add(VGroup(ff, nv, cub, sd, ldv, nm))
        self.play(FadeIn(ins[0][:3]), FadeIn(ins[0][5]), run_time=0.6)
        self.gat("no começo, esse quilo")
        self.play(GrowArrow(ins[0][3]), FadeIn(ins[0][4]), ins[0][2].animate.shift(0.5 * LEFT), run_time=0.8)
        self.gat("no fim, empurra só")
        self.play(FadeIn(ins[1][:3]), FadeIn(ins[1][5]), run_time=0.6)
        self.play(GrowArrow(ins[1][3]), FadeIn(ins[1][4]), ins[1][2].animate.shift(0.5 * LEFT), run_time=0.8)
        self.gat("é essa massa no denominador")
        den = mp(B, ib, [4])[3:]
        self.play(Indicate(den, color=WHITE_, scale_factor=1.4), run_time=0.9)
        C, ic = M(r"\int_{v_0}^{v_f}dv", "=", "-", r"v_{ex}", r"\int_{m_0}^{m_f}\frac{dm}{m}", size=46, cores={0: VEL, 3: VEX_C})
        self.pilha.poe(C)
        alvo_i = mp(C, ic, [0]).get_left() + 0.25 * RIGHT                          # v6 §4.2: onde nasce o ∫
        cps = [ins[k][3].copy() for k in (0, 1)]
        self.add(*cps)
        self.play(*[cp.animate(path_arc=-1.1).move_to(alvo_i).scale(0.4) for cp in cps], run_time=1.0)
        self.play(*[FadeOut(cp) for cp in cps], FadeOut(ins), FadeIn(C, shift=0.1 * UP), run_time=0.3)
        self.remove(ins, *cps)
        self.gat("então integra")
        self.wait(0.2)                                                                       # v7: C já entrou junto com a chegada das setas dv
        lmf = MathTex("m_f", font_size=40, color=MAS)
        lmf.add_updater(lambda m_: m_.next_to(P3(xb + 0.25, yb + H * mm.get_value()), RIGHT, buff=0.22))       # sobe junto com o nível
        self.play(FadeIn(lmf), run_time=0.4)
        Cn, icn = M(r"\int\frac{dm}{m}", "=", r"\ln m", size=42)
        self.pilha.poe(Cn, dx=1.5)
        self.gat("a integral de dm sobre a massa")
        self.play(FadeIn(Cn), run_time=0.7)
        D, id_ = M(r"\Delta v", "=", "-", r"v_{ex}", r"(\ln m_f-\ln m_0)", size=46, cores={0: VEL, 3: VEX_C})
        self.pilha.poe(D)
        self.passo(C, D, (J(ic, 1), J(id_, 1)), (J(ic, 2), J(id_, 2)), (J(ic, 3), J(id_, 3)), rt=1.2, origem=False)
        E, ie = M(r"\Delta v", "=", r"v_{ex}", r"\ln\frac{m_0}{m_f}", size=50, cores={0: VEL, 2: VEX_C})
        Sg, isg = M("-", r"\ln\frac{m_f}{m_0}", "=", r"\ln\frac{m_0}{m_f}", size=40)
        self.pilha.poe(Sg, dx=1.2)
        self.pilha.poe(E)
        self.gat("e o sinal de menos inverte")
        self.play(FadeIn(Sg), run_time=0.5)
        self.passo(D, E, (J(id_, 0), J(ie, 0)), (J(id_, 1), J(ie, 1)), (J(id_, 3), J(ie, 2)), rt=1.3, origem=False)
        self.foco = E
        self.ate(0.97)
        # ── T3-2 ──
        self.an("T3-2")
        self.pilha.so(E)
        Eb = caixa_l(E.copy(), VEL)
        self.pilha.linhas = [(Eb, 0.0)]
        Eb.move_to(E)
        Eb.shift((X_CONTA - Eb.get_left()[0]) * RIGHT)
        self.play(FadeIn(Eb[0]), run_time=0.5)
        self.remove(E)
        self.add(Eb)
        nome = txt("EQUAÇÃO DE TSIOLKOVSKY", 28, bold=True)
        self.pilha.poe(nome)
        self.gat("a equação de tsiolkovsky")
        self.play(FadeIn(nome, shift=0.1 * UP), run_time=0.6)
        R_, ir = M("R", "=", r"\frac{m_0}{m_f}", size=50)
        R2 = linha_m(R_, txt("RAZÃO DE MASSAS", 26), buff=0.3)
        self.pilha.poe(R2)
        self.gat("essa razão tem nome")
        self.play(FadeIn(R2), Indicate(Eb[1][0][ie[3][2]:][:6] if False else Eb, color=VEL, scale_factor=1.03), run_time=0.8)
        self.foco = Eb
        self.ate(0.97)
        # ── T3-3: CONFERE ──
        self.an("T3-3")
        self.confere("OS DOIS LIMITES")
        K1, ik1 = M(r"m_f=m_0", r"\ \Rightarrow\ ", "R=1", r"\ \Rightarrow\ ", r"\Delta v=0", size=44, cores={4: VEL})
        K2, ik2 = M(r"v_{ex}\to 0", r"\ \Rightarrow\ ", r"\Delta v\to 0", size=44, cores={0: VEX_C, 2: VEL})
        self.pilha.poe(K1)
        self.pilha.poe(K2)
        self.gat("se o foguete não queima nada")
        self.play(FadeIn(K1), mm.animate.set_value(1.0), run_time=0.9)
        self.gat("se o gás sai cada vez mais devagar")
        self.play(FadeIn(K2), kx.animate.set_value(1.0), run_time=0.7)
        self.play(kx.animate(rate_func=smooth).set_value(0.0), run_time=1.8)                    # v_ex → 0: a seta e o Δv encolhem juntos até sumir
        self.foco = K2
        self.ate(0.97)
        lmf.clear_updaters()
        self.remove(sxv, lvx, ldvx)
        self.esq = VGroup(fg, bv, lm0, lmf)
        self.mm = mm

    # ── T3-4 e T3-5 (v2: um gráfico largo só em cada; sem divisão ESQUEMA × CONTA) ──
    def t3_graficos(self):
        self.an("T3-4")
        self.sem_selo()
        self.layout_v = True
        self.esq[1].clear_updaters()
        R, vf = 5.0, math.log(5.0)
        TM = 600.0                                                      # 10 min no eixo
        g1 = Graf(-6.4, -2.3, 10.2, TM, 0, 1.9, 2.0, rot_y=MathTex("v", font_size=36, color=VEL), rot_x=r"t\ (\mathrm{min})")
        fv = lambda tq: (lambda t: math.log(1 / (1 - 0.8 * min(t, tq) / tq)))
        k1, k2 = ValueTracker(0.0), ValueTracker(0.0)
        self.add(k1, k2)
        c1 = vivo(lambda: g1.curva(fv(10.0), 0, max(1e-3, TM * k1.get_value()), n=260, cor=VEL))           # 10 s: cheia, quase vertical
        c2 = vivo(lambda: DashedVMobject(g1.curva(fv(TM), 0, max(1e-3, TM * k2.get_value()), n=200, cor=VEL), num_dashes=46, dashed_ratio=0.62))   # 10 min: tracejada longa
        marcas_t = VGroup(*[VGroup(Line(g1.pt(60 * m_, 0) + 0.07 * DOWN, g1.pt(60 * m_, 0) + 0.07 * UP).set_stroke(GEO, 2),
                                   rot(str(m_), 24, color=GEO).next_to(g1.pt(60 * m_, 0), DOWN, buff=0.14)) for m_ in (2, 4, 6, 8, 10)])
        t1 = txt("QUEIMA DE 10 s", 24, color=VEL).move_to(g1.pt(10.0, vf * 0.55) + P3(1.5, 0))                       # v7 #17: junto da curva rápida, à direita da subida
        t2 = VGroup(txt("QUEIMA DE", 24, color=VEL), txt("10 min", 24, color=VEL)).arrange(DOWN, buff=0.06)

        pt_fim = g1.pt(TM, fv(TM)(TM))
        t2.move_to(P3(pt_fim[0] + 0.5, pt_fim[1] - 1.1))                               # v8 #4: fixo, onde fica a partir de 8:54     # acompanha a ponta e termina abaixo dela
        ldv = MathTex(r"\Delta v", font_size=40, color=VEL).next_to(g1.pt(TM, vf), RIGHT, buff=0.3)
        alvo_ = DashedLine(g1.pt(0, vf), g1.pt(TM, vf), dash_length=0.12).set_stroke(VEL, 2.2, opacity=0.8)
        fml_ = M(r"\Delta v", "=", r"v_{ex}", r"\ln R", size=44, cores={0: VEL, 2: VEX_C})[0].next_to(alvo_, UP, buff=0.22).shift(0.9 * LEFT)
        self.pilha.limpa(rt=0.7, anims=[FadeOut(self.esq), FadeIn(g1.eixos), FadeIn(marcas_t), FadeIn(c1), FadeIn(c2), FadeIn(t1), FadeIn(alvo_), FadeIn(fml_)])
        self.remove(self.esq)
        lab = VGroup(txt("MESMO", 24, color=DIM), MathTex(r"v_{ex}", font_size=36, color=VEX_C), txt("E MESMA", 24, color=DIM), MathTex("R", font_size=36)).arrange(RIGHT, buff=0.12)
        lab.move_to(P3(-1.3, -3.55))
        self.play(FadeIn(lab), run_time=0.4)
        self.gat("queima tudo em dez segundos")
        self.play(k1.animate(rate_func=linear).set_value(1.0), run_time=1.6)
        self.gat("e outro que queima em dez minutos")
        self.add(t2)
        self.play(k2.animate(rate_func=linear).set_value(1.0), run_time=4.0)
        pass
        self.play(FadeIn(ldv), run_time=0.5)
        self.reg("t3_4", v1=fv(10.0)(10.0), v2=fv(TM)(TM))
        self.selo("NO ESPAÇO", [["A VAZÃO NÃO MUDA O", MathTex(r"\Delta v", font_size=34, color=VEL)]])
        self.foco = ldv
        self.ate(0.97)
        # ── T3-5: Δv/v_ex × R ──
        self.an("T3-5")
        self.sem_selo()
        velhos = [m for m in self.snap()]
        G = Graf(-6.2, -1.7, 11.0, 24.0, 0, 3.35, 1.1, rot_y=MathTex(r"\Delta v/v_{ex}", font_size=36, color=VEL), rot_x="R")
        k = ValueTracker(0.0)
        self.add(k)
        cur = vivo(lambda: G.curva(lambda r: math.log(1 + r), 0, max(1e-3, 24.0 * k.get_value()), cor=VEL, w=6))
        tk = VGroup(*[VGroup(Line(G.pt(r - 1, 0) + 0.08 * DOWN, G.pt(r - 1, 0) + 0.08 * UP).set_stroke(GEO, 2), rot(str(r), 24, color=GEO).next_to(G.pt(r - 1, 0), DOWN, buff=0.14))
                      for r in (5, 10, 15, 20, 25)])
        fml5 = M(r"\Delta v", "/", r"v_{ex}", "=", r"\ln R", size=46, cores={0: VEL, 2: VEX_C})[0].move_to(P3(2.9, -0.3))
        self.troca(velhos, FadeIn(G.eixos), FadeIn(tk), FadeIn(cur), FadeIn(fml5), k.animate.set_value(0.2), seq=True)
        self.play(k.animate.set_value(1.0), run_time=2.0)
        self.gat("a curva é um logaritmo")
        marcas = VGroup()
        for n, (s_, val) in enumerate(((r"e", "2,7"), (r"e^2", "7,4"), (r"e^3", "20,1")), start=1):
            r = math.e ** n
            p = G.pt(r - 1, n)
            gm = VGroup(DashedLine(G.pt(r - 1, 0), p, dash_length=0.08).set_stroke(GEO, 1.4, opacity=0.7),
                        DashedLine(G.pt(0, n), p, dash_length=0.08).set_stroke(GEO, 1.4, opacity=0.7), Dot(p, radius=0.07, color=WHITE_).set_z_index(9),
                        MathTex(str(n), font_size=36, color=VEL).next_to(G.pt(0, n), LEFT, buff=0.34),
                        MathTex(s_ + r"\approx" + val.replace(",", "{,}"), font_size=36, color=WHITE_).move_to(G.pt(r - 1, 0) + P3(0, -0.72)))
            marcas.add(gm)
            self.reg("t3_5", n=n, R=r)
        frases = ("a razão de massas é o número e", "vai a e ao quadrado", "para três, e ao cubo")
        for n in range(3):
            self.gat(frases[n])
            self.play(Create(marcas[n][0]), Create(marcas[n][1]), FadeIn(marcas[n][2:]), run_time=0.9)
        xe = VGroup(*[CurvedArrow(G.pt(math.e ** n - 1, 0) + P3(0.05, -1.08), G.pt(math.e ** (n + 1) - 1, 0) + P3(-0.05, -1.08), angle=0.7, color=WHITE_, stroke_width=3, tip_length=0.15)
                      for n in (1, 2)])
        lxe = VGroup(*[MathTex(r"\times e", font_size=36, color=WHITE_).move_to((a.get_center() + P3(0, -0.4))) for a in xe])
        self.gat("cada degrau a mais")
        self.play(Create(xe), run_time=0.9)
        self.play(FadeIn(lxe), run_time=0.3)                                                # v8 #5: o rótulo só aparece com o arco já desenhado
        self.foco = marcas[2]
        self.wait(2.0)                                                       # pausa útil: os degraus ×e (hold)
        self.ate(0.97)
        self.g35 = VGroup(G.eixos, tk, cur, marcas, xe, lxe, fml5)
        self.layout_v = False

    # ── T3-6: os números ──
    def t3_numeros(self):
        self.an("T3-6")
        velhos = self.snap()
        fg = foguete2d(5.2, 0.95).shift(P3(-5.8, -3.3))
        xb, yb, H = -3.5, -3.3, 4.6
        part = ValueTracker(1.0)                                              # a barra já nasce com a cor da estrutura e da carga
        self.add(part)

        def barra():
            f = part.get_value()
            hp = H * 0.95 * f
            g = VGroup(Rectangle(width=0.6, height=H).move_to(P3(xb, yb + H / 2)).set_stroke(GEO, 2, opacity=0.8).set_fill(WHITE_, 0.08))
            if hp > 0.01:
                g.add(Rectangle(width=0.6, height=hp).move_to(P3(xb, yb + hp / 2)).set_stroke(width=0).set_fill(MAS, 0.9))
                g.add(Rectangle(width=0.6, height=H * 0.05 * f).move_to(P3(xb, yb + H * 0.95 + H * 0.05 * f / 2)).set_stroke(width=0).set_fill(STEEL, 1))
            return g.set_z_index(3)
        bv = vivo(barra)
        self.troca(velhos, FadeIn(fg), FadeIn(bv), seq=True)
        L1, i1 = M(r"v_{ex}", r"\approx", r"3{,}0\ \mathrm{km/s}", size=46, cores={0: VEX_C, 2: VEX_C})
        L2, i2 = M(r"v_{\acute{o}rbita}", r"\approx", r"7{,}8\ \mathrm{km/s}", size=46, cores={0: VEL, 2: VEL})
        L3 = VGroup(linha_m(txt("ORÇAMENTO", 26, bold=True), M(r"\Delta v", r"\approx", r"9\ \mathrm{km/s}", size=46, cores={0: VEL, 2: VEL})[0], buff=0.18),
                    txt("(COM AS PERDAS)", 24)).arrange(DOWN, buff=0.08, aligned_edge=LEFT)
        L4, i4 = M(r"\frac{\Delta v}{v_{ex}}", "=", "3", r"\ \Rightarrow\ ", "R", "=", "e^3", r"\approx", "20", size=46)
        pinta(L4, i4, 0, [(0, VEL), (1, VEL), (3, VEX_C), (4, VEX_C), (5, VEX_C)])
        L5, i5 = M(r"m_f", "=", r"\frac{m_0}{20}", size=46)
        for L_, fr in ((L1, "um bom motor químico"), (L2, "para ficar em órbita baixa"), (L3, "a gente adota um orçamento"), (L4, "nove dividido por três")):
            self.pilha.poe(L_)
            self.gat(fr)
            self.play(FadeIn(L_, shift=0.08 * UP), run_time=0.7)
        self.pilha.poe(L5)
        self.gat("sobra um vigésimo da massa")
        self.play(FadeIn(L5), run_time=0.6)
        self.gat("noventa e cinco por cento")
        r95 = VGroup(txt("95% PROPELENTE", 26, color=MAS), txt("5% O RESTO", 26, color="#B9C4D6"))
        r95[0].move_to(P3(xb + 0.6 + r95[0].width / 2, yb + H * 0.47))
        r95[1].move_to(P3(xb + 0.45 + r95[1].width / 2, yb + H + 0.25))
        self.play(FadeIn(r95), run_time=0.6)
        self.reg("t3_6", prop=0.95, exato=NUM["95%"])
        self.selo("ORDEM DE GRANDEZA", "")
        self.foco = r95[0]
        self.ate(0.97)

    # ── T3-7 e T3-8: a simulação com cor pelo sentido ──
    def t3_esp(self):
        self.an("T3-7")
        velhos = self.snap()
        s = self.sim
        es = EspSim(self, s, "sentido", yc=-0.6, op=0.0, larg=5.6, xc=-1.4)
        self.add(es.ts, es.chama, es.f3d)
        X_M, Y0, HM, VMAX = 6.0, -2.9, 4.6, 1.75                                # medidor v/v_ex
        KB = 2 * (int(round(s.t_cruza / s.DT)) + 8)                              # a primeira parcela que sai PARA A FRENTE (logo depois do cruzamento)

        def camada():
            ts = es.ts.get_value()
            x, v, m = s.foguete(ts)
            cm = es.tela(ts, s.cm(ts)[0])
            g = VGroup(marcador_cm(cm, r=0.17))
            r_ = v / s.VEX
            hh = HM * min(r_, VMAX) / VMAX
            g.add(Rectangle(width=0.42, height=HM).move_to(P3(X_M, Y0 + HM / 2)).set_stroke(GEO, 2, opacity=0.8).set_fill(PANEL, 0.6))
            if hh > 0.005:
                g.add(Rectangle(width=0.42, height=hh).move_to(P3(X_M, Y0 + hh / 2)).set_stroke(width=0).set_fill(VEL, 0.9))
            y1 = Y0 + HM / VMAX
            g.add(Line(P3(X_M - 0.34, y1), P3(X_M + 0.34, y1)).set_stroke(WHITE_, 3))
            b = es.tela(ts, x)
            o = es.chama.get_value() * (1.0 if ts < s.TQ else max(0.0, 1 - (ts - s.TQ) / (0.5 * FAT3)))
            if self._setas_t38 > 0.01 and o > 0.02:
                oo = self._setas_t38 * o
                g.add(seta(b + P3(0.0, 0.34), b + P3(1.1, 0.34), FC, 7, tip=0.22, op=oo))                                   # nasce no bocal e corre logo acima do corpo (como no T2-5)
                self.reg("forca", lugar="T3-8", d_px=float(np.hypot(0.0, 0.34) * 60))
            if self._setas_t38 > 0.01:                                                                                   # uma partícula branca: v vista de fora
                k = KB
                if ts > s.g_t0[k]:
                    px = s.g_x0[k] + s.g_vx[k] * (ts - s.g_t0[k])
                    q = es.tela(ts, px)
                    g.add(Dot(q, radius=0.06, color=WHITE_).set_z_index(9),
                          seta(q + P3(0, -0.32), q + P3(S_V * s.g_vx[k], -0.32), VEL, 6, tip=0.18, op=self._setas_t38))
                    if AUDITORIA:
                        self.seta_v(q, q + P3(1, 0), "DE FORA (O FOGUETE PARTIU DO REPOUSO)", nome="gás novo")
            self._selo_sobre_3d(b, es.L_TELA)
            nb = int(np.sum(s.g_frente[s.g_t0 <= ts + 1e-9]))
            self.reg("t3_cor", t=ts, v=v, n_branco=nb, cm_px=float(cm[0]) * 60, cm_m=s.cm(ts)[0], P=s.momento(ts), K=es.cam(ts)["K"])
            return g.set_z_index(8)
        self._setas_t38 = 0.0
        cv = vivo(camada)
        cv._tela_cheia = True
        lmed = MathTex(r"v/v_{ex}", font_size=36, color=VEL).move_to(P3(X_M, Y0 + HM + 0.32))
        l1 = MathTex("1", font_size=36, color=WHITE_).move_to(P3(X_M - 0.75, Y0 + HM / VMAX))
        esc = txt("FOGUETE FORA DE ESCALA", 24, color=DIM).move_to(P3(-4.7, -3.7))
        self.troca(velhos, es.f3d.op.animate.set_value(1.0), FadeIn(cv), FadeIn(lmed), FadeIn(l1), FadeIn(esc), seq=True)
        self.referencial("DE FORA (O FOGUETE PARTIU DO REPOUSO)")
        leg = VGroup(VGroup(Dot(radius=0.09, color=MAS), txt("PARA TRÁS", 24)).arrange(RIGHT, buff=0.14),
                     VGroup(Circle(radius=0.1).set_stroke(WHITE_, 2.5).set_fill(MAS, 0.3), txt("PARA A FRENTE", 24)).arrange(RIGHT, buff=0.14)).arrange(RIGHT, buff=0.5)
        leg.move_to(P3(-7.0 + leg.width / 2, -3.05))
        self.play(FadeIn(leg), run_time=0.5)
        t_cr = s.t_cruza / FAT3
        t_ini = dur("T3-7") - 0.4 - t_cr                                  # o cruzamento cai no fim do T3-7
        self.wait(max(0.1, t_ini - (self.nq - self._q0) / FPS - 0.6))
        self.play(es.chama.animate.set_value(1.0), es.ts.animate(rate_func=linear).set_value(0.6 * FAT3), run_time=0.6)
        self.play(es.ts.animate(rate_func=linear).set_value(s.t_cruza - 0.05), run_time=(s.t_cruza - 0.05 - 0.6 * FAT3) / FAT3)
        self.selo("63% QUEIMADO", [[MathTex("v", font_size=36, color=VEL), "=", MathTex(r"v_{ex}", font_size=36, color=VEX_C)]], rt=0.4,
                  anims=[es.ts.animate(rate_func=linear).set_value(s.t_cruza + 0.4 * FAT3)])                              # G35: selo na faixa, não rótulo solto sobre o foguete
        self.ate(0.99)
        # ── T3-8 ──
        self.an("T3-8")
        lF = MathTex(r"F_{emp}", font_size=34, color=FC)
        lvg = M("v", "-", r"v_{ex}", ">", "0", size=36, cores={0: VEL, 2: VEX_C})[0]

        def pos_l(m_):
            ts = es.ts.get_value()
            x_, _, _ = s.foguete(ts)
            b = es.tela(ts, x_)
            o = self._setas_t38 * es.chama.get_value() * (1.0 if ts < s.TQ else max(0.0, 1 - (ts - s.TQ) / (0.5 * FAT3)))
            m_[0].move_to(b + P3(0.55, 0.88))
            k_ = KB
            q_ = es.tela(ts, s.g_x0[k_] + s.g_vx[k_] * (ts - s.g_t0[k_])) if ts > s.g_t0[k_] else b
            m_[1].next_to(q_ + P3(0, 0.32), UP, buff=0.1).shift(1.0 * LEFT)               # v8 #6: acima do rastro, ≥ 20 px do F_emp
            for x in m_[0].family_members_with_points():
                x.set_opacity(o)
            for x in m_[1].family_members_with_points():
                x.set_opacity(self._setas_t38 if ts > s.g_t0[k_] else 0.0)
        gl = VGroup(lF, lvg)
        self._setas_t38 = 1.0
        pos_l(gl)
        self.add(gl)
        gl.add_updater(pos_l)
        # inset: o mesmo gás, visto do foguete (todas as parcelas novas saem para trás com v_ex)
        IX0, IX1, IY0, IY1 = 0.7, 5.3, -3.65, -1.45
        NX, NY, SK = 3.4, -2.45, 0.00044
        caixa_i = RoundedRectangle(corner_radius=0.12, width=IX1 - IX0, height=IY1 - IY0).move_to(P3((IX0 + IX1) / 2, (IY0 + IY1) / 2)).set_fill(PANEL, 0.88).set_stroke(GEO, 1.8, opacity=0.8)
        caixa_i._fundo = True
        fi = fog_h(1.5, 0.3, bocal=P3(NX, NY))
        chi = chama2d(P3(NX, NY), 0.4, 0.2, vertical=False)
        sxi = seta_tr(P3(NX - 0.1, NY - 0.55), P3(NX - 1.4, NY - 0.55), VEX_C, 5, tip=0.2)
        lxi = MathTex(r"v_{ex}", font_size=34, color=VEX_C).next_to(sxi, UP, buff=0.12)
        rli = txt("EM RELAÇÃO AO FOGUETE", 24).move_to(P3((IX0 + IX1) / 2, IY1 - 0.32))
        inset = VGroup(caixa_i, fi, chi, sxi, lxi, rli)
        n_t = 0                                                                        # v3: nenhum rótulo de objeto na faixa do título do inset
        for m_ in (lxi, sxi, fi, chi):
            if min(rli.get_right()[0], m_.get_right()[0]) - max(rli.get_left()[0], m_.get_left()[0]) > 0.02 and min(rli.get_top()[1], m_.get_top()[1]) - max(rli.get_bottom()[1], m_.get_bottom()[1]) > 0.02:
                n_t += 1
                print(f"[audit] ROTULO NA LINHA DE TITULO inset T3-8: {type(m_).__name__} dentro da faixa de EM RELAÇÃO AO FOGUETE")
        self.reg("titulo_t38", n=n_t)
        for m_ in (inset,):
            m_._tela_cheia = True
        op_in = ValueTracker(0.0)
        self.add(op_in)

        def pontos_i():
            ts = es.ts.get_value()
            g = VGroup()
            k0 = min(int(ts / s.DT + 1e-9), len(s.ev) - 1)
            x_f = s.foguete(ts)[0]
            for j in range(0, 40, 2):
                kk = 2 * max(0, k0 - j)
                px = s.g_x0[kk] + s.g_vx[kk] * (ts - s.g_t0[kk])
                xq_ = NX + SK * (px - x_f) - 0.1
                if xq_ > IX0 + 0.12:                                                  # o conteúdo fica dentro da moldura
                    g.add(Dot(P3(xq_, NY), radius=0.045, color=WHITE_).set_opacity(max(0.0, op_in.get_value()) * (1.0 - 0.6 * j / 40)))
            self.reg("inset_t38", t=ts, todas_tras=bool(np.all(s.g_vx[2 * np.maximum(0, k0 - np.arange(0, 40, 2))] - s.foguete(ts)[1] < 0)))
            return g.set_z_index(12)
        pi_ = vivo(pontos_i)
        self.add(pi_)
        self.gat("visto do foguete") if False else None
        self.play(FadeIn(inset), op_in.animate.set_value(1.0), run_time=0.6)
        self._refs.append([int(round(self.clk.get_value() * FPS)), "v_ex", "EM RELAÇÃO AO FOGUETE", "rótulo junto da seta"]) if AUDITORIA else None
        t_rest8 = max(2.0, dur("T3-8") - 2.0 - 0.6)                             # a queima ocupa o bloco menos os 2 s finais (corte do motor 2 s antes do fim)
        t_mk = min(3.2, t_rest8 - 0.5)
        self.play(es.ts.animate(rate_func=linear).set_value(s.t_cruza + 0.4 * FAT3 + t_mk * FAT3), run_time=t_mk)     # o marcador 63% fica ≥ 3 s
        self.play(FadeOut(self.s1), es.ts.animate(rate_func=linear).set_value(s.TQ - 0.01), run_time=t_rest8 - t_mk)
        self.remove(self.s1)
        self.s1 = None
        self.reg("t38_corte", resta=float(self.resta()), inset=True)
        self.play(es.ts.animate(rate_func=linear).set_value(s.TQ + 2.0 * FAT3), run_time=max(1.0, self.resta() - 0.15))
        self.ate(0.99)
        gl.clear_updaters()

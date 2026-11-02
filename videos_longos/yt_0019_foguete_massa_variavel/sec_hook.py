"""Lote PH: hook H1–H3 (Three.js 'rampa': foguete de dois estágios na rampa, corte com os tanques, barra de massa 89,0 / 8,9 / 2,1) e abertura
A1 (logo), A2 (três ícones), A3 (patinadores no gelo: momentos iguais e opostos, ⊕ parado; ΣF⃗_ext = dP⃗/dt acende token a token).
H3: barras de propelente f e 2f sobre a mesma estrutura s (f = 10 s, sem carga) e setas de Δv ∝ ln 11 = 2,40 e ln 21 = 3,04 (1 : 1,27)."""
from pecas19 import *  # noqa: F401,F403

# barra de massa do hook = a do E2-5 (números do E2): propelente, estrutura, carga
FR_HOOK = (NUM["prop%"] / 100, NUM["estr%"] / 100, NUM["carga%"] / 100)
ROT_HOOK = (f"{NUM['prop%']:.1f}".replace(".", ",") + "% PROPELENTE", f"{NUM['estr%']:.1f}".replace(".", ",") + "% ESTRUTURA",
            f"{NUM['carga%']:.1f}".replace(".", ",") + "% CARGA ÚTIL")


def barra_hook(x, yb, H, mostra=1.0, size=24, larg=0.62):
    """A barra do hook (e do E2-5/S1): fatias e rótulos à direita, cada rótulo na altura da sua fatia (a carga, fina, com chamada)."""
    b = barra_massa(x, yb, H, FR_HOOK, larg=larg, cores=[MAS, STEEL, WHITE_], mostra=mostra)
    ys = [yb + FR_HOOK[0] * H / 2, yb + FR_HOOK[0] * H + FR_HOOK[1] * H / 2 - 0.12, yb + H + 0.32]
    rs = VGroup(*[txt(s, size, color=c) for s, c in zip(ROT_HOOK, (MAS, WHITE_, WHITE_))])
    for r_, y in zip(rs, ys):
        r_.move_to(P3(x + larg / 2 + 0.22 + r_.width / 2, y))
    rs[2].move_to(P3(x - larg / 2 + rs[2].width / 2, ys[2]))                 # a carga (fatia fina) com o rótulo logo acima da barra
    ch = VGroup()
    return b, rs, ch


class LoteHook(Prob2):
    FUNDO = "fundo_lab.png"

    def construct(self):
        self.setup_base()
        self.hook()
        self.abertura()
        self.fim()
        self.relatorio()
        self.gravar_reg()

    # ════════════════════════════════════════ hook ════════════════════════════════════════
    def hook(self):
        el, az, K, alvo, xc, corte, tq, carga = (ValueTracker(v) for v in (2.0, -90.0, 9.5, 0.1, 0.0, 0.0, 0.0, 0.0))
        modo = ValueTracker(0.0)                                       # 0 = rampa de pé · 1 = foguete-mestre no espaço vazio (pergunta de H3)
        self.add(el, az, K, alvo, xc, corte, tq, carga, modo)

        def est(t):
            if modo.get_value() > 0.5:
                n, P, A = 70, [], []
                for i in range(n):
                    a = (t * 0.9 + i / n) % 1.0
                    P += [-0.5 - 0.62 * a, 0.035 * a * math.sin(i * 12.9898), 0.5 + 0.035 * a * math.sin(i * 78.233)]
                    A.append(round(1.0 - 0.75 * a, 2))
                return {"f": r4(est_foguete(-0.5, 0.0, 0.5, 1.0, "x", ch1=1.0, torre=0, espaco=1)),
                        "gas": {"p": [round(q, 4) for q in P], "c": [0] * n, "a": A, "s": 3.5},
                        "cam": r4(cam_obl_(0.0, (0.0, 0.0, 0.5), K.get_value(), xc=0.0, yc=0.0, fov=18, az=-90.0))}
            return {"f": r4(est_foguete(0.0, 0.0, 0.03, 1.0, "z", corte=corte.get_value(), tq=[tq.get_value()] * 2, carga=carga.get_value())),
                    "cam": r4(cam_obl_(el.get_value(), (0.03, 0.0, alvo.get_value()), K.get_value(), xc=xc.get_value(), yc=-0.2, fov=20, az=az.get_value()))}
        f3 = Fundo3D(self, "rampa", est)
        self.add(f3)
        # ── H1 ──
        self.an("H1")
        self.play(alvo.animate(rate_func=smooth).set_value(0.86), el.animate.set_value(7.0), az.animate.set_value(-84.0), run_time=dur("H1") - 0.1)
        self.ate(0.99)
        # ── H2: corte, tanques, barra ──
        self.an("H2")
        self.play(K.animate.set_value(7.4), alvo.animate.set_value(0.5), xc.animate.set_value(-3.0), el.animate.set_value(6.0), az.animate.set_value(-90.0),
                  run_time=1.8)
        self.play(corte.animate.set_value(1.0), tq.animate.set_value(1.0), run_time=1.4)
        xb, yb, H = 0.9, -2.75, 4.0
        mostra = ValueTracker(0.0)
        self.add(mostra)
        bv = vivo(lambda: barra_massa(xb, yb, H, FR_HOOK, larg=0.62, cores=[MAS, STEEL, WHITE_], mostra=mostra.get_value()))
        _, rs, ch = barra_hook(xb, yb, H, size=26)
        self.play(FadeIn(bv), run_time=0.3)
        self.gat("nove décimos da massa é propelente")
        self.play(mostra.animate.set_value(FR_HOOK[0]), run_time=1.6)
        self.play(FadeIn(rs[0], shift=0.1 * RIGHT), run_time=0.5)
        self.play(mostra.animate.set_value(FR_HOOK[0] + FR_HOOK[1]), FadeIn(rs[1], shift=0.1 * RIGHT), run_time=0.8)
        self.gat("a carga que de fato vai")
        self.play(mostra.animate.set_value(1.0), FadeIn(rs[2], shift=0.1 * RIGHT), Create(ch), carga.animate.set_value(1.0), run_time=0.8)
        self.play(carga.animate(rate_func=there_and_back).set_value(0.2), run_time=0.8)
        self.play(carga.animate(rate_func=there_and_back).set_value(0.2), run_time=0.8)
        self.selo("ORDEM DE GRANDEZA", "")
        self.foco = rs[2]
        self.ate(0.97)
        # ── H3: f e 2f; Δv ∝ ln 11 e ln 21 ──
        self.an("H3")
        bv.clear_updaters()
        self.play(FadeOut(bv), FadeOut(rs), FadeOut(ch), corte.animate.set_value(0.0), tq.animate.set_value(0.0), carga.animate.set_value(0.0), run_time=0.6)
        self.remove(bv, rs, ch)
        self.sem_selo()
        q = VGroup(txt("POR QUE UM FOGUETE É", 34, bold=True), txt("QUASE TODO COMBUSTÍVEL?", 34, bold=True)).arrange(DOWN, buff=0.14).move_to(P3(2.75, 2.55))
        s_, f_ = 0.22, 1.6                                             # estrutura s; propelente f = 10 s → a escala: f = 1,6
        ybase = -2.95
        k_v = 0.95                                                     # Δv/v_ex → tela
        bars, labs, arrs = VGroup(), VGroup(), VGroup()
        for i, (x, nf) in enumerate(((-0.2, 1), (2.9, 2))):
            hp = nf * f_
            g = VGroup(Rectangle(width=0.62, height=s_).move_to(P3(x, ybase + s_ / 2)).set_stroke(width=0).set_fill(STEEL, 1),
                       Rectangle(width=0.62, height=hp).move_to(P3(x, ybase + s_ + hp / 2)).set_stroke(width=0).set_fill(MAS, 0.9),
                       Rectangle(width=0.62, height=hp + s_).move_to(P3(x, ybase + (hp + s_) / 2)).set_stroke(GEO, 2, opacity=0.8))
            bars.add(g)
            labs.add(MathTex("f" if nf == 1 else "2f", font_size=40, color=MAS).next_to(g, LEFT, buff=0.2).align_to(g[1], UP).shift(0.1 * DOWN))
            dv = math.log(1 + nf * 10)                                 # sem carga: R = (s + n f)/s = 1 + 10 n
            a = arrow(P3(x + 0.75, ybase), P3(x + 0.75, ybase + k_v * dv), VEL, 7, tip=0.24)
            arrs.add(a)
            self.reg(f"h3_seta{i}", i=i, dv=dv, comp=k_v * dv)
        lab_dv = VGroup(*[MathTex(r"\Delta v", font_size=40, color=VEL).next_to(a, UP if i == 0 else RIGHT, buff=0.14 if i == 0 else 0.26) for i, a in enumerate(arrs)])
        lab_dv[1].align_to(arrs[1], UP)
        lab_s = VGroup(*[txt("ESTRUTURA", 24, color=DIM).next_to(b_[0], DOWN, buff=0.14) for b_ in bars])
        self.play(FadeIn(q, shift=0.1 * DOWN), run_time=0.8)
        self.gat("se precisa ir mais rápido")
        self.play(FadeIn(bars[0]), FadeIn(labs[0]), FadeIn(lab_s[0]), run_time=0.7)
        self.play(GrowArrow(arrs[0]), FadeIn(lab_dv[0]), run_time=0.7)
        self.gat("por que não é só dobrar o combustível")
        self.play(FadeIn(bars[1], shift=0.1 * UP), FadeIn(labs[1]), FadeIn(lab_s[1]), run_time=0.8)
        x2 = MathTex(r"\times 2", font_size=40, color=WHITE_).next_to(bars[1], UP, buff=0.18)
        self.play(FadeIn(x2), run_time=0.4)
        self.gat("dobrar o combustível não dobra a velocidade")
        self.play(GrowArrow(arrs[1]), FadeIn(lab_dv[1]), run_time=1.0)
        x127 = MathTex(r"\times 1{,}27", font_size=40, color=VEL).next_to(lab_dv[1], RIGHT, buff=0.3)
        fant = DashedLine(arrs[0].get_end() + 0.0 * UP, P3(arrs[1].get_x(), arrs[0].get_end()[1]), dash_length=0.08).set_stroke(VEL, 2, opacity=0.6)
        self.play(FadeIn(x127), Create(fant), run_time=0.6)
        self.foco = x127
        self.gat("como um foguete acelera no espaço")
        self.h3 = VGroup(q, bars, labs, arrs, lab_dv, lab_s, x2, x127, fant)
        self.play(FadeOut(self.h3), run_time=0.4)
        self.remove(self.h3)
        K.set_value(6.8)
        modo.set_value(1.0)                                            # corte: o foguete-mestre no espaço vazio, jato aceso, vista lateral
        eq = txt("EMPURRA O QUÊ?", 36, bold=True, op=1.0).move_to(P3(0, 2.3)).set_z_index(40)
        self.play(FadeIn(eq, shift=0.1 * UP), K.animate(rate_func=linear).set_value(7.4), run_time=max(1.0, self.resta() - 0.5))
        self.ate(0.99)
        self.play(FadeOut(eq), run_time=0.3)
        self.f3 = f3

    # ════════════════════════════════════════ abertura ════════════════════════════════════════
    def abertura(self):
        # ── A1 ──
        self.an("A1")
        velhos = self.snap()
        logo = self.logo(5.6).move_to(P3(0, 0.9))
        bv = txt("BEM-VINDOS AO PARALLAX LAB", 30).move_to(P3(0, -0.5))
        self.troca(velhos, FadeIn(logo, scale=0.94), FadeIn(bv, shift=0.1 * UP), seq=True)
        self.ate(0.97)
        # ── A2: três ícones ──
        self.an("A2")
        tt = txt("POR QUE UM FOGUETE É", 46, bold=True).move_to(P3(0, 2.75))
        tt2 = txt("QUASE TODO COMBUSTÍVEL?", 46, bold=True).next_to(tt, DOWN, buff=0.18)
        nv = txt("NESTE VÍDEO:", 28).move_to(P3(-5.4, 0.55))
        ics = VGroup(*[self.item(k) for k in range(3)])
        for k, it in enumerate(ics):
            it.move_to(P3(-4.2 + 4.2 * k, -1.35))
        self.play(FadeOut(logo), FadeOut(bv), FadeIn(tt, shift=0.1 * UP), FadeIn(tt2, shift=0.1 * UP), FadeIn(nv), FadeIn(ics), run_time=0.9)   # palco desde o começo
        ul = VGroup()
        for k, frase in enumerate(("de onde vem a força", "quanta velocidade cada quilo", "por que os foguetes que vão")):
            self.gat(frase)
            ul.add(Line(ics[k].get_corner(DL) + 0.16 * DOWN, ics[k].get_corner(DR) + 0.16 * DOWN).set_stroke(CYAN, 3.5))
            self.play(Create(ul[-1]), ics[k].animate.scale(1.06), run_time=0.5)      # destaque por borda ciano, nunca por opacidade
            self.foco = ics[k][0]
        self.ate(0.97)
        # ── A3: faixa no rodapé → patinadores ──
        self.an("A3")
        faixa = VGroup(*[VGroup(self.icone(k, 0.42), txt(self.CURTOS[k], 24)).arrange(RIGHT, buff=0.12) for k in range(3)]).arrange(RIGHT, buff=0.5)
        faixa.move_to(P3(0, -3.5))
        yg, d = -2.3, ValueTracker(0.0)
        self.add(d)
        xc_ = -3.6
        pL = patinador(0, yg, sen=1, alt=3.6)
        pR = patinador(0, yg, sen=-1, alt=3.6)
        hw = 0.8
        topo_antes = self.pilha.topo
        self.pilha.topo = 1.3                                          # a CONTA na altura dos patinadores

        def pat():
            s_ = d.get_value()
            g = VGroup(pL.copy().move_to(P3(xc_ - hw - s_, pL.get_y())), pR.copy().move_to(P3(xc_ + hw + s_, pR.get_y())))
            if s_ > 0.05:                                              # o ⊕ só nasce depois que as mãos se separam
                o = min(1.0, (s_ - 0.05) / 0.25)
                g.add(marcador_cm(P3(xc_, yg + 1.95), r=0.21, op=o))
                g.add(seta(P3(xc_ - hw - s_ + 0.1, yg + 4.15), P3(xc_ - hw - s_ - 1.0, yg + 4.15), MAG, 7, tip=0.22, op=o),
                      seta(P3(xc_ + hw + s_ - 0.1, yg + 4.15), P3(xc_ + hw + s_ + 1.0, yg + 4.15), MAG, 7, tip=0.22, op=o))
            self.reg("patinadores", cm=P3(xc_, yg), d=s_)
            return g
        pv = vivo(pat)
        gl_ = gelo(-7.3, 0.1, yg)
        self.play(FadeOut(tt), FadeOut(tt2), FadeOut(nv), FadeOut(ics, shift=0.3 * DOWN), FadeOut(ul), FadeIn(faixa, shift=0.2 * UP), run_time=0.45)
        self.play(FadeIn(gl_), FadeIn(pv), run_time=0.5)
        self.play(FadeOut(faixa, shift=0.2 * DOWN), run_time=0.5)
        # CONTA: ΣF⃗_ext = dP⃗/dt acende token a token
        A, ia = M(r"\sum \vec F_{ext}", "=", r"\frac{d\vec P}{dt}", size=56, cores={0: FC, 2: MAG})
        B0, ib = M(r"\vec F_{ext}", "=", r"\vec 0", r"\ \Rightarrow\ ", r"\vec P", size=52, cores={0: FC, 4: MAG})
        B_ = linha_m(B0, txt("CONSTANTE", 30, bold=True), buff=0.22)
        self.pilha.poe(A)
        self.gat("a força externa resultante")
        self.play(FadeIn(mp(A, ia, [0])), run_time=0.5)
        self.play(FadeIn(mp(A, ia, [1])), run_time=0.3)
        self.gat("taxa de variação do momento total")
        self.play(FadeIn(mp(A, ia, [2])), run_time=0.6)
        self.remove(*[m for m in self.mobjects if m is not A and isinstance(m, VGroup) and all(any(x is y for y in A.get_family()) for x in m.get_family()) and m.get_family()])
        self.add(A)
        self.pilha.poe(B_)
        self.gat("sem força externa")
        self.play(FadeIn(mp(B0, ib, [0, 1, 2])), run_time=0.7)                        # A3: esta linha acende token a token (exceção do G19)
        self.gat("o momento total não muda")
        self.play(FadeIn(mp(B0, ib, [3, 4])), FadeIn(B_[1]), run_time=0.7)
        self.remove(*[m for m in list(self.mobjects) if m is not B_ and isinstance(m, VGroup) and m.get_family()[1:] and all(any(x is y for y in B_.get_family()) for x in m.get_family()[1:])])
        self.add(B_)
        self.gat("dois patinadores parados")
        lab_m = VGroup(rot("60 kg", 28).move_to(P3(xc_ - hw - 0.1, yg - 0.75)), rot("60 kg", 28).move_to(P3(xc_ + hw + 0.1, yg - 0.75)))
        self.play(FadeIn(lab_m), run_time=0.4)
        self.gat("se empurram")
        lab_m[0].add_updater(lambda m: m.move_to(P3(xc_ - hw - d.get_value() - 0.1, yg - 0.75)))
        lab_m[1].add_updater(lambda m: m.move_to(P3(xc_ + hw + d.get_value() + 0.1, yg - 0.75)))
        self.play(d.animate(rate_func=lambda u: u ** 1.0).set_value(1.6), run_time=5.0)
        lp = VGroup(MathTex(r"\vec p_1", font_size=40, color=MAG).move_to(P3(xc_ - hw - 1.6 - 0.45, yg + 4.6)),
                    MathTex(r"\vec p_2", font_size=40, color=MAG).move_to(P3(xc_ + hw + 1.6 + 0.45, yg + 4.6)))
        self.play(FadeIn(lp), run_time=0.5)
        self.foco = pv
        self.gat("um dos patinadores virando gás")
        self.play(Indicate(B_, color=MAG, scale_factor=1.04), run_time=0.8)
        self.ate(0.97)
        for m in lab_m:
            m.clear_updaters()
        self.pilha.topo = topo_antes

    CURTOS = ("EMPURRAR O PRÓPRIO GÁS", "QUANTO O COMBUSTÍVEL COMPRA", "ESTÁGIOS")

    def icone(self, k, s=1.0):
        if k == 0:
            f = foguete2d(1.3, 0.3).rotate(-PI / 2, about_point=ORIGIN).shift(P3(-0.25, 0))
            rng = np.random.default_rng(3)
            nuv = VGroup(*[Dot(P3(-0.45 - rng.uniform(0, 0.8), rng.normal(0, 0.12)), radius=0.035, color=GAS_C).set_opacity(0.8) for _ in range(18)])
            g = VGroup(nuv, f)
        elif k == 1:
            ax = VGroup(Line(P3(-0.8, -0.55), P3(0.85, -0.55)).set_stroke(GEO, 2.5), Line(P3(-0.8, -0.55), P3(-0.8, 0.65)).set_stroke(GEO, 2.5))
            cur = VMobject().set_points_smoothly([P3(-0.8 + 1.6 * u, -0.55 + 0.42 * math.log(1 + 24 * u)) for u in np.linspace(0, 1, 30)]).set_stroke(VEL, 5)
            g = VGroup(ax, cur)
        else:
            baixo = FogueteMestre(1.0, 0.34).rotate(0.28, about_point=P3(0, 0.5)).shift(0.25 * DOWN + 0.12 * LEFT)      # estágios que se separam (G29)
            cima = FogueteMestre(0.8, 0.28).shift(0.55 * UP)
            g = VGroup(baixo, cima, chama2d(P3(0, 0.55), 0.3, 0.14)).move_to(ORIGIN)
        return g.scale(s)

    def item(self, k):
        ic = self.icone(k, 1.0)
        if ic.height > 1.4:
            ic.scale_to_fit_height(1.4)
        lin = self.CURTOS[k].split(" ", 1) if k < 2 else [self.CURTOS[k]]
        if k == 1:
            lin = ["QUANTO O COMBUSTÍVEL", "COMPRA"]
        if k == 0:
            lin = ["EMPURRAR O", "PRÓPRIO GÁS"]
        t = VGroup(*[txt(l, 26) for l in lin]).arrange(DOWN, buff=0.24)
        return VGroup(ic, t).arrange(DOWN, buff=0.3)

"""Lote PE2: E2 — por que estágios? ESQUEMA fixo em corte com o foguete-mestre (CARGA P, PROPELENTE f, ESTRUTURA 0,1 f); E2-2: o tanque esvazia e o casco
fica; P → 0: R_máx = 11, Δv_máx = 3 ln 11 = 7,2 km/s < 9. E2-3: Three.js 'esp' (foguete-mestre VERTICAL na metade direita, câmera presa ao 2º estágio): o
1º estágio apaga, separa no anel e segue com a velocidade que tinha (constante, visto de fora), girando devagar; o 2º acende. No 2D o 1º estágio fica
translúcido (não some) e o v_ex passa para o sino do 2º. E2-4: R = e^1,5 = 4,48 → f₂ = 5,34 P → m₀₂ = 6,88 P → m₀₁ = 6,88 · 6,88 P = 47,3 P (o 2º estágio
vira a carga do 1º, com a chave m₀₂). E2-5: a barra do hook (89,0 / 8,9 / 2,1). E2-6: ESTRUTURA → 0, um estágio, barra 95/5."""
from pecas19 import *  # noqa: F401,F403
from sec_hook import barra_hook, FR_HOOK

VEX_C = VREL
N_ = lambda s: s.replace(".", "{.}").replace(",", "{,}")


def estagio(x, yb, w, ht, nivel=1.0):
    """O 1º estágio em corte (foguete-mestre sem ogiva): casco (ESTRUTURA, aço), tanque com nível (PROPELENTE), sino e aletas. Corpo de yb a yb + ht."""
    h = ht / 0.94
    g = FogueteMestre(h, w, corte=True, nivel=nivel, ogiva=False).shift(P3(x, yb - 0.06 * h))
    g.topo = yb + ht
    return g


class LoteE2(Prob2):
    FUNDO = "fundo_lab_ex.png"

    def construct(self):
        self.setup_base()
        self.e2()
        self.fim()
        self.relatorio()
        self.gravar_reg()

    def e2(self):
        self.an("E2-1")
        self.secao("EXERCÍCIO 2 · POR QUE ESTÁGIOS?")
        X, Y0, WU, HU = -5.0, -3.5, 1.55, 6.0                             # foguete-mestre em corte: base do sino, largura, altura (v3: ~1,2×)
        niv = ValueTracker(1.0)
        self.add(niv)
        ref = FogueteMestre(HU, WU, corte=True)
        yP = Y0 + ref.pts["carga"][1]
        yf = Y0 + ref.pts["tanque"][1]
        um = vivo(lambda: FogueteMestre(HU, WU, corte=True, nivel=niv.get_value()).shift(P3(X, Y0)))
        lP = MathTex("P", font_size=42).next_to(P3(X + WU / 2, yP), RIGHT, buff=0.35)
        lf = MathTex("f", font_size=42, color=MAS).next_to(P3(X + WU / 2, yf), RIGHT, buff=0.35)
        lfn = txt("PROPELENTE", 24, color=MAS).next_to(lf, RIGHT, buff=0.22)
        ls = VGroup(txt("ESTRUTURA", 24), MathTex(r"0{,}1\,f", font_size=40)).arrange(RIGHT, buff=0.15).next_to(P3(X + WU / 2, Y0 + 0.75), RIGHT, buff=0.85)
        lPn = txt("CARGA", 24).next_to(lP, RIGHT, buff=0.22)
        q = VGroup(txt("DÁ COM UM", 36, bold=True), txt("ESTÁGIO SÓ?", 36, bold=True)).arrange(DOWN, buff=0.14, aligned_edge=LEFT)
        self.pilha.poe(q)
        XB = (2.25, 4.2, 6.15)                                                                 # v8 D1: o orçamento vira um medidor, ocupando a metade direita desde o início
        blocos = VGroup(*[RoundedRectangle(corner_radius=0.08, width=1.8, height=0.6).set_fill(VREL, 0.85).set_stroke(VREL, 1.5).move_to(P3(xc, -0.5)) for xc in XB])
        rotb = VGroup(*[VGroup(MathTex(r"v_{ex}", font_size=34, color=VEX_C), rot("3,0 km/s", 24, VEX_C)).arrange(DOWN, buff=0.06).move_to(P3(xc, -1.25)) for xc in XB])
        chave = Brace(blocos, UP, buff=0.12, color=VEL)
        tot = VGroup(txt("ORÇAMENTO", 24), MathTex(r"\Delta v\approx", font_size=38, color=VEL), rot("9 km/s", 28, VEL)).arrange(RIGHT, buff=0.1).next_to(chave, UP, buff=0.12)
        lorc = VGroup(blocos, rotb, chave, tot)
        self.play(FadeIn(um), FadeIn(q, shift=0.1 * UP), FadeIn(lorc), run_time=0.8)         # a pergunta entra grande logo no início do bloco
        self.pede("RAZÃO DE MASSAS")
        self.play(FadeIn(lP), FadeIn(lPn), FadeIn(lf), FadeIn(lfn), run_time=0.6)
        self.gat("essa estrutura pese dez por cento")
        self.play(FadeIn(ls), Indicate(um, color=STEEL, scale_factor=1.02), run_time=0.8)
        sx = seta_tr(P3(X + 1.3, Y0 + 0.15), P3(X + 1.3, Y0 - 0.4), VEX_C, 6, tip=0.2)
        lvx = VGroup(MathTex(r"v_{ex}=", font_size=38, color=VEX_C), rot("3,0 km/s", 28, VEX_C)).arrange(RIGHT, buff=0.08).next_to(sx, RIGHT, buff=0.15)
        self.gat("gás a três quilômetros")
        self.play(Create(sx), FadeIn(lvx), run_time=0.7)
        self._refs.append([int(round(self.clk.get_value() * FPS)), "v_ex", "EM RELAÇÃO AO FOGUETE", "seta no bocal (dado do exercício)"]) if AUDITORIA else None
        self.gat("o orçamento, de novo")
        self.play(Indicate(tot, color=VEL, scale_factor=1.04), run_time=0.6)
        self.hip([["ESTRUTURA = 0,1", MathTex("f", font_size=32, color=MAS), "· PERDAS JÁ NOS", rot("9 km/s", 24)]], x0=-2.0, wmax=9.4)
        self.gat("dá para fazer com um estágio só")
        self.play(Indicate(q, color=WHITE_, scale_factor=1.05), run_time=0.5)
        self.ate(0.97)
        # ── E2-2 ──
        self.an("E2-2")
        self.pilha.limpa(rt=0.3, anims=[FadeOut(lorc)])
        A, ia = M("m_0", "=", "P", "+", r"1{,}1\,f", size=48)
        B, ib = M("m_f", "=", "P", "+", r"0{,}1\,f", size=48)
        self.pilha.poe(A)
        self.pilha.poe(B)
        self.gat("no começo, o foguete tem")
        self.acende([(lP, mp(A, ia, [2])), (lf, mp(A, ia, [4])[-1:])], extra=[FadeIn(mp(A, ia, [0, 1, 3])), FadeIn(mp(A, ia, [4])[:-1])], rt=1.0)
        self.gat("no fim, sobram a carga")
        self.play(niv.animate.set_value(0.0), run_time=1.6)
        self.acende([(lP, mp(B, ib, [2])), (ls[1], mp(B, ib, [4]))], extra=[FadeIn(mp(B, ib, [0, 1, 3]))], rt=1.0)
        C, ic = M(r"R_{m\acute{a}x}", "=", r"\frac{1{,}1\,f}{0{,}1\,f}", "=", "11", size=50)
        self.pilha.poe(C)
        self.gat("carga zero")
        P0 = VGroup(mp(A, ia, [2]), mp(B, ib, [2]))
        p0 = MathTex(r"P\to 0", font_size=40, color=HEAT).next_to(P3(X + WU / 2, yP), RIGHT, buff=0.35)            # no limite de carga zero
        self.play(*[Indicate(p, color=HEAT, scale_factor=1.3) for p in P0], FadeIn(p0), run_time=0.7)
        rkP = VGroup(risco(P0[0], HEAT, 4), risco(P0[1], HEAT, 4))                          # v5 §4.3: P → 0 é riscado, sai, e a linha fecha o buraco
        self.play(Create(rkP), FadeOut(lP), FadeOut(lPn), run_time=0.5)
        gA = mp(A, ia, [4]).get_left()[0] - mp(A, ia, [2]).get_left()[0]
        gB = mp(B, ib, [4]).get_left()[0] - mp(B, ib, [2]).get_left()[0]
        self.play(FadeOut(P0), FadeOut(mp(A, ia, [3])), FadeOut(mp(B, ib, [3])), FadeOut(rkP), run_time=0.35)
        self.play(mp(A, ia, [4]).animate.shift(gA * LEFT), mp(B, ib, [4]).animate.shift(gB * LEFT), run_time=0.6)
        self.play(FadeIn(mp(C, ic, [0, 1])), TransformFromCopy(mp(A, ia, [4]), mp(C, ic, [2])[:5]), TransformFromCopy(mp(B, ib, [4]), mp(C, ic, [2])[6:]),
                  FadeIn(mp(C, ic, [2])[5:6]), run_time=1.2)
        self.remove(*[m for m in list(self.mobjects) if m is not C and isinstance(m, VGroup) and m.get_family()[1:] and all(any(x is y for y in C.get_family()) for x in m.get_family()[1:])])
        self.add(*[x for x in mp(C, ic, [0, 1, 2])])
        self.gat("que é onze")
        self.play(FadeIn(mp(C, ic, [3, 4])), run_time=0.5)
        self.remove(*[m for m in list(self.mobjects) if m is not C and isinstance(m, VGroup) and m.get_family()[1:] and all(any(x is y for y in C.get_family()) for x in m.get_family()[1:])])
        self.add(C)
        D, id_ = M(r"\Delta v_{m\acute{a}x}", "=", r"3{,}0\cdot\ln 11", r"\approx", r"7{,}2\ \mathrm{km/s}", size=46, cores={0: VEL, 4: VEL})
        D2, id2 = M(r"7{,}2\ \mathrm{km/s}", "<", r"9\ \mathrm{km/s}", size=46, cores={0: VEL, 2: VEL})
        pinta(D, id_, 2, [(0, VEX_C), (1, VEX_C), (2, VEX_C)])
        Dx = MathTex(r"\times", font_size=56, color=HEAT)
        self.pilha.poe(D)
        self.gat("e três vezes o logaritmo de onze")
        self.acende([(lvx[1][:3], mp(D, id_, [2])[:3])], extra=[FadeIn(mp(D, id_, [0, 1])), FadeIn(mp(D, id_, [2])[3:])], rt=0.9)
        self.play(FadeIn(mp(D, id_, [3, 4])), run_time=0.6)
        self.gat("não chega")
        self.pilha.poe(D2)
        self.play(FadeIn(D2), run_time=0.5)
        Dx.next_to(D2, RIGHT, buff=0.2)
        self.play(FadeIn(Dx, scale=1.3), run_time=0.4)
        self.reg("e2_2", R=11, dv=NUM["dv11"])
        self.foco = Dx
        self.ate(0.97)
        # ── E2-3: dois estágios; separação no espaço (Three.js vertical na metade direita) ──
        self.an("E2-3")
        self.pilha.limpa(rt=0.3, anims=[FadeOut(Dx), FadeOut(p0)])
        self.sem_selo()
        um.clear_updaters()
        W = 1.55
        H1, H2, YB = 2.9, 3.3, -3.5
        st1 = estagio(X, YB, W, H1, 1.0)
        st2 = FogueteMestre(H2, W * 0.92, corte=True).shift(P3(X, YB + H1))
        dois = VGroup(st1, st2)
        anel = Line(P3(X - W / 2 - 0.12, YB + H1), P3(X + W / 2 + 0.12, YB + H1)).set_stroke(CYAN, 3, opacity=0.8)
        l1 = VGroup(txt("ESTRUTURA", 24), MathTex(r"0{,}1\,f_1", font_size=38)).arrange(RIGHT, buff=0.12).next_to(P3(X + W / 2, YB + 0.7), RIGHT, buff=0.55)
        l2 = VGroup(txt("ESTRUTURA", 24), MathTex(r"0{,}1\,f_2", font_size=38)).arrange(RIGHT, buff=0.12).next_to(P3(X + W / 2, YB + H1 + 0.9), RIGHT, buff=0.35)
        n1 = txt("1º ESTÁGIO", 24, color=DIM).next_to(P3(X + W / 2, YB + 1.55), RIGHT, buff=0.55)
        n2 = txt("2º ESTÁGIO", 24, color=DIM).next_to(l2, UP, buff=0.22).align_to(l2, LEFT)
        for m_ in (l1, l2, n1, n2):
            m_.shift((X + W / 2 + 0.85 - m_.get_left()[0]) * RIGHT)         # v6: uma só margem esquerda para os quatro rótulos
        self.play(FadeOut(um), FadeOut(ls), FadeOut(lf), FadeOut(lfn), FadeIn(dois), FadeIn(anel), run_time=0.8)
        self.play(FadeIn(l1), FadeIn(l2), FadeIn(n1), FadeIn(n2), run_time=0.6)
        # Three.js: câmera presa ao 2º estágio; 1º estágio com velocidade constante depois da separação (visto de fora)
        tt = ValueTracker(0.0)
        self.add(tt)
        A1, A2, V0, T_OFF, T_SEP, T_ON, VREL_S, VG = 0.10, 0.32, 0.4, 4.3, 5.0, 6.2, 0.06, 1.6
        ESC = 1.0
        ZR = -0.55

        def mov(t):
            """x do 2º (raiz) e do 1º estágio, e as velocidades (mundo, unidades do corpo)."""
            tb = min(t, T_OFF)
            x = V0 * tb + 0.5 * A1 * tb * tb
            v = V0 + A1 * tb
            if t > T_OFF:
                dt_ = t - T_OFF
                x += v * dt_
            x2, v2 = x, v
            if t > T_ON:
                d2 = t - T_ON
                x2 += 0.5 * A2 * d2 * d2
                v2 += A2 * d2
            if t > T_SEP:
                x1 = (V0 * T_OFF + 0.5 * A1 * T_OFF ** 2) + (V0 + A1 * T_OFF) * (t - T_OFF) - VREL_S * (t - T_SEP)
                v1 = V0 + A1 * T_OFF - VREL_S
            else:
                x1, v1 = x, v
            return x2, x1, v2, v1
        rng = np.random.default_rng(12)
        NE = 45
        emis = []                                                  # (t0, estágio, vy, vz)
        for k in range(int(15.6 * NE)):
            t0 = k / NE
            if t0 < T_OFF:
                emis.append((t0, 1, rng.normal(0, 0.1), rng.normal(0, 0.05)))
            if t0 > T_ON:
                emis.append((t0, 2, rng.normal(0, 0.08), rng.normal(0, 0.04)))
        mov0 = [mov(e[0]) for e in emis]

        def est(t):
            t_ = tt.get_value()
            x2, x1, v2, v1 = mov(t_)
            pts, al = [], []
            for (t0, k, vy, vz), m0_ in zip(emis, mov0):
                if t0 > t_:
                    continue
                a = t_ - t0
                if a > 3.0:
                    continue
                xn = m0_[1] if k == 1 else m0_[0] + 0.6 * ESC
                vn = (m0_[3] if k == 1 else m0_[2]) - VG
                pts += [vz * a, vy * a, ZR + (xn + vn * a - x2)]            # câmera presa ao 2º estágio: z relativo à raiz
                al.append(round(max(0.0, 1 - a / 3.0), 2))
            sep_d = (x2 - x1) / ESC
            ang = 0.22 * max(0.0, t_ - T_SEP)
            ch1 = 1.0 if t_ < T_OFF else max(0.0, 1 - (t_ - T_OFF) / 0.3)
            ch2 = 0.0 if t_ < T_ON else min(1.0, (t_ - T_ON) / 0.3)
            self.reg("estagios", t=t_, x1=x1, v1=v1, x2=x2, v2=v2)
            return {"f": r4(est_foguete(0.0, 0.0, ZR, ESC, "z", ch1=ch1, ch2=ch2, sep=[sep_d, ang], torre=0)),
                    "gas": {"p": [round(float(q), 4) for q in pts], "c": [0] * len(al), "a": al, "s": 4.0},
                    "cam": r4(cam_frente(K=5.4, xc=3.9, yc=-0.1, camx=0.0, fov=16, el=0))}
        f3 = Fundo3D(self, "esp", est, op=0.0)
        self.add(f3)
        cam_l = txt("CÂMERA PRESA AO 2º ESTÁGIO", 24, color=DIM).move_to(P3(3.9, 3.05))
        self.play(f3.op.animate.set_value(1.0), FadeIn(cam_l), tt.animate(rate_func=linear).set_value(0.8), run_time=0.8)
        self.gat("o primeiro estágio queima")
        t_a = max(0.5, T_OFF - tt.get_value())
        v_a = tt.get_value()
        self.play(tt.animate(rate_func=linear).set_value(T_OFF), run_time=t_a)
        self.play(tt.animate(rate_func=linear).set_value(T_SEP), Indicate(anel, color=CYAN, scale_factor=1.15), run_time=T_SEP - T_OFF)
        # o 1º estágio fica translúcido e tracejado (não some); o v_ex passa para o sino do 2º no instante da ignição
        st1_sep = st1.copy().set_opacity(0.4)                                   # v6: sólido e esmaecido, sem tracejado
        self.remove(dois)
        self.add(st1, st2, st1_sep)
        self.play(tt.animate(rate_func=linear).set_value(T_ON), FadeOut(st1), FadeOut(VGroup(l1, n1, anel)),
                  sx.animate.shift((H1) * UP), lvx.animate.shift((H1) * UP), run_time=T_ON - T_SEP)
        resto = self.resta() - 0.15
        self.play(tt.animate(rate_func=linear).set_value(T_ON + resto), run_time=resto)
        self.ate(0.99)
        # ── E2-4 ──
        self.an("E2-4")
        self.play(f3.op.animate.set_value(0.0), FadeOut(cam_l), FadeOut(st1_sep), FadeIn(st1), FadeIn(VGroup(l1, n1, anel)),
                  sx.animate.shift(H1 * DOWN), lvx.animate.shift(H1 * DOWN), run_time=0.6)                            # v7 #34: v_ex sob o bocal de baixo
        self.remove(st1_sep)
        self.remove(f3)
        L1 = linha_m(txt("CADA ESTÁGIO:", 26, bold=True), M(r"\Delta v", "=", r"4{,}5\ \mathrm{km/s}", size=46, cores={0: VEL, 2: VEL})[0], buff=0.2)
        L1b, il1 = M("R", "=", r"e^{1{,}5}", r"\approx", r"4{,}48", size=46)
        self.pilha.poe(L1)
        self.pilha.poe(L1b, dx=0.4)
        E, ie = M(r"\frac{P+1{,}1\,f_2}{P+0{,}1\,f_2}", "=", r"4{,}48", size=46)
        self.pilha.poe(E)
        lR = MathTex(r"R=4{,}48", font_size=34, color=VEL)
        lR.move_to(P3(X - W * 0.92 / 2 - 0.3 - lR.width / 2, YB + H1 + 1.7))
        lR = VGroup(lR, Line(P3(X - W * 0.92 / 2 - 0.25, YB + H1 + 1.7), P3(X - W * 0.92 / 2 - 0.02, YB + H1 + 1.7)).set_stroke(VEL, 2.4))      # v8 #11
        self.gat("meio a meio")
        self.play(FadeIn(L1), FadeIn(L1b), FadeIn(E), run_time=0.8)                # v7 #35: três linhas de uma vez (sem 15 s com duas)
        self.gat("começa pelo de cima")
        self.play(Indicate(st2, color=WHITE_, scale_factor=1.04), FadeIn(lR), run_time=1.0)
        F_, if_ = M(r"f_2", r"\approx", r"5{,}34\,P", size=46)
        self.pilha.poe(F_)
        self.gat("o propelente do segundo estágio")
        self.play(FadeIn(F_, shift=0.1 * UP), Indicate(E, color=WHITE_, scale_factor=1.03), run_time=1.0)
        G_, ig = M(r"m_{02}", "=", r"P+1{,}1\,f_2", r"\approx", r"6{,}88\,P", size=46)
        self.pilha.poe(G_)
        self.gat("o segundo estágio inteiro, cheio")
        self.play(FadeIn(G_), run_time=0.8)
        self.gat("agora o truque")
        # o 2º estágio inteiro vira a CARGA do 1º: encolhe sobre o anel e ganha a chave m₀₂ (a pilha da esquerda não se duplica)
        self.play(FadeOut(VGroup(l1, l2, n1, n2, lorc, sx, lvx, anel, lR)), run_time=0.4)
        base2 = st2.get_bottom()
        self.play(st2.animate.scale(0.82, about_point=base2), run_time=0.8)
        br2 = Brace(st2, RIGHT, buff=0.18, color=WHITE_)
        lm02 = VGroup(MathTex(r"m_{02}=", font_size=40), txt("CARGA DO 1º ESTÁGIO", 24)).arrange(DOWN, buff=0.08, aligned_edge=LEFT).next_to(br2, RIGHT, buff=0.15)
        self.play(GrowFromCenter(br2), FadeIn(lm02), run_time=0.8)
        H_, ih = M(r"\frac{m_{02}+1{,}1\,f_1}{m_{02}+0{,}1\,f_1}", "=", r"4{,}48", size=46)
        self.pilha.poe(H_)
        self.play(FadeIn(H_, shift=0.1 * UP), self.ind_copia(E, WHITE_, 1.03, 1.0), run_time=1.1)                       # v10 F10: a razão nova acende por baixo; a linha anterior não é copiada por cima
        I_, ii = M(r"m_{01}", r"\approx", r"6{,}88\cdot 6{,}88\,P", r"\approx", r"47{,}3\,P", size=48)
        Ib = caixa_l(I_, WHITE_)
        self.pilha.poe(Ib)
        self.gat("o foguete completo na rampa")
        self.play(FadeIn(Ib), run_time=0.9)
        self.reg("e2_4", R=NUM["R15"], f2=NUM["f2"], m02=NUM["m02"], m01=NUM["m01"], conf=NUM["conf_est1"])
        self.foco = Ib
        self.ate(0.97)
        # ── E2-5: a barra do hook volta ──
        self.an("E2-5")
        self.pilha.limpa(rt=0.4, anims=[FadeOut(VGroup(br2, lm02))])
        xb, yb, HB = -1.2, -3.0, 4.6
        mostra = ValueTracker(0.0)
        self.add(mostra)
        bv = vivo(lambda: barra_massa(xb, yb, HB, FR_HOOK, larg=0.62, cores=[MAS, STEEL, WHITE_], mostra=mostra.get_value()))
        _, rs, _ = barra_hook(xb, yb, HB, size=26)
        self.play(FadeIn(bv), FadeIn(rs), run_time=0.35)                                # v6: a barra entra já com os rótulos
        self.play(mostra.animate.set_value(1.0), run_time=1.6)
        self.reg("barra_e2", prop=100 * FR_HOOK[0], estr=100 * FR_HOOK[1], carga=100 * FR_HOOK[2])
        tt_ = VGroup(txt("NESTE MODELO", 24, color=CYAN, bold=True), rot("1 t DE CARGA", 34), VGroup(MathTex(r"\rightarrow", font_size=48), rot("47 t NA RAMPA", 34)).arrange(RIGHT, buff=0.18)).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        tt_.move_to(P3(3.5 + tt_.width / 2, -0.2))
        self.gat("para cada tonelada de carga")
        self.play(FadeIn(tt_, shift=0.1 * UP), run_time=0.7)
        self.foco = tt_
        self.ate(0.97)
        # ── E2-6 ──
        self.an("E2-6")
        bv.clear_updaters()
        um2 = FogueteMestre(HU, WU, corte=True).shift(P3(X, Y0))
        ls2 = VGroup(txt("ESTRUTURA", 24), MathTex(r"0{,}1\,f", font_size=40)).arrange(RIGHT, buff=0.15).next_to(P3(X + WU / 2, Y0 + 0.75), RIGHT, buff=0.85)
        self.confere([["ESTRUTURA → 0 · UM ESTÁGIO BASTA (", MathTex("R", font_size=34), rot("= 20)", 26)]], x0=-2.0, wmax=9.4)
        self.play(FadeOut(VGroup(bv, rs, tt_)), FadeOut(st1), FadeOut(st2), FadeIn(um2), run_time=0.8)
        self.play(Indicate(um2, color=STEEL, scale_factor=1.02), run_time=1.2)          # v7 #36: sem o rótulo ESTRUTURA 0,1 f na cena do CONFERE
        b95 = barra_massa(-1.2, -3.0, 4.6, (0.95, 0.05), larg=0.62, cores=[MAS, STEEL])
        r95 = VGroup(txt("95% PROPELENTE", 26, color=MAS), txt("5% O RESTO", 26, color="#B9C4D6"))
        r95[0].move_to(P3(-1.2 + 0.62 / 2 + 0.25 + r95[0].width / 2, -3.0 + 4.6 * 0.47))
        r95[1].move_to(P3(-1.2 - 0.31 - 0.25 - r95[1].width / 2, -3.0 + 4.6 + 0.02))
        self.play(FadeIn(b95), FadeIn(r95), run_time=0.8)
        nota = VGroup(txt("DIVISÃO MEIO A MEIO =", 26), txt("ESCOLHA DIDÁTICA", 26)).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        self.pilha.poe(nota)
        self.gat("uma observação honesta")
        self.play(FadeIn(nota), run_time=0.6)
        self.gat("a dica fica")
        self.dica18("CADA ESTÁGIO, RAZÃO NOVA")
        self.ate(0.97)

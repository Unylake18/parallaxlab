"""Lote PD5 · D5 O DESAFIO PROMETIDO (alvos 19, 20, 21, 22). Para cada campo: enunciado e PAUSE E TENTE → tabela (cada derivada voa da componente
para a sua célula) → quatro medidas (rot violeta, div azul-claro, d₁/d₂ lima) → previsão em selos (GIRA ✗/✓ · ÁREA ✗/✓ · DEFORMA ✗/✓) → soltar.
① f₁ (t = 0,5): SÓ DEFORMA e a resposta do palpite. ② f₂ (t = 0,7): o 1 e o −1 da tabela piscam com as setas que empinam/abaixam; a viagem tracejada.
③ f₃ (origem (360, 780), 240 px/u): três quadradinhos de lado 0,3 em (1, 0), (0, 1), (1, 1), t = 0,1; NUNCA ENTORTA; quinas medidas.
No fim, por 2 s, FÓRMULA → TABELA → 4 NÚMEROS → QUADRADINHO."""
from lib30 import *  # noqa: F401,F403

V3 = Vista(360, 780, 240)
PTS3 = [(1, 0), (0, 1), (1, 1)]


def jtex(a, b, c, d):
    return r"J=\begin{pmatrix}\Am{%s} & \Mg{%s}\\ \Am{%s} & \Mg{%s}\end{pmatrix}" % (a, b, c, d)


def selos(estados, y=680):
    """GIRA ✗/✓ · ÁREA ✗/✓ · DEFORMA ✗/✓ (✗ coral, ✓ menta): devolve os três selos (cada um palavra + marca) e os separadores."""
    pec, itens = [], []
    for k, (nome, ok) in enumerate(zip(("GIRA", "ÁREA", "DEFORMA"), estados)):
        t = T(nome, 0, y, 32)
        mk = MathTex(r"\checkmark" if ok else r"\boldsymbol{\times}", font_size=fs(32)).set_color(CAMPO2 if ok else CORAL)
        mk._sem_contorno = True
        it = VGroup(t, mk)
        mk.next_to(t, RIGHT, buff=8 / 120).set_y(t.get_center()[1])
        itens.append(it)
        pec.append(it)
        if k < 2:
            pec.append(T("·", 0, y, 32, cor=GEO, bold=False))
    g = VGroup(*pec).arrange(RIGHT, buff=14 / 120, center=False)
    for p in pec[1::2]:
        p.set_y(pec[0][0].get_center()[1])
    g.shift(RIGHT * (PX(1120, 0)[0] - g.get_left()[0]))
    return g, itens


class LoteD5(Base):
    ANTES = "O CAMPO QUE NÃO MELHORA DE PERTO · CLASSE C¹"

    def monta_tabela(self, J, fonte_l1, fonte_l2, gat1, gat2, x=1120):
        """'J =' e parênteses em caneta; a linha 1 (derivadas de P) voa de fonte_l1, a linha 2 (de Q) de fonte_l2."""
        cel, resto = celulas(J)
        self.play(caneta(resto, ritmo=0.5))
        for fr, linha, fonte in ((gat1, 0, fonte_l1), (gat2, 1, fonte_l2)):
            self.gat(fr)
            self.play(*[TransformFromCopy(fonte, cel[(linha, j)]) for j in (0, 1)], run_time=0.9)
        junta_partes(self, J)
        return cel

    def medidas(self, rot, div, d1, d2, Y, gats):
        R1 = Pz([r"\rot=\V{%s}\qquad" % rot, r"\dv=\D{%s}" % div], 1120, Y, 42, caneta=False)
        R2 = Pz([r"d_1=\Lm{%s}\qquad " % d1, r"d_2=\Lm{%s}" % d2], 1120, Y + 80, 42, caneta=False)
        for (m, i), fr in zip(((R1, 0), (R1, 1), (R2, 0), (R2, 1)), gats):
            if fr:
                self.gat(fr)
            self.play(caneta(sub_pz(m, i), ritmo=0.35))
        junta_partes(self, R1)
        junta_partes(self, R2)
        return R1, R2

    def corpo(self):
        # ── D5-1 · topo da escada ──
        self.an("D5-1")
        self.secao("O DESAFIO")
        zera_chapas()
        chA = chapa_px(*LA, nome="D5 palco A", v=VA)
        mt = legenda("MONTA A TABELA E PREVÊ:", 1124, 450, GEO)
        qs = [T("GIRA?", 1120, 540, 40, cor=VIO), T("MUDA DE ÁREA?", 1120, 610, 40, cor=SAIC), T("DEFORMA?", 1120, 680, 40, cor=LIMA)]
        troca(self, "D4 → D5 (palco)")
        self.play(FadeIn(chA), run_time=0.6)
        self.gat("para cada um monta a tabela")
        self.play(FadeIn(mt, shift=0.05 * UP), run_time=0.4)
        for fr, m in zip(("prevê se o quadradinho gira", "muda de área", "ou deforma"), qs):
            self.gat(fr)
            self.play(FadeIn(m, shift=0.05 * UP), run_time=0.4)
        self.ate(1.0)

        # ── D5-2 · campo ① (alvo 19) ──
        self.an("D5-2")
        self.secao_n("O DESAFIO · CAMPO", 1)
        c1, s1 = (0.0, 0.0), 1.2
        ped = quad30(VA, c1, s1)
        cmp = campo30(VA, F1, rmin=0, mmax=5, nome="D5 f₁")
        st = {"extra": NADA}
        clareira(cmp, lambda: ou(clar_ped(ped), dq(c1, s1), st["extra"]))
        F = Pz([r"\F=(", r"\X+\Y", r",\ ", r"\X-\Y", ")"], 1120, 330, 48)
        self.gat("primeiro campo")
        self.play(cresce_campo(cmp, 0.8), FadeIn(ped), run_time=0.8)
        self.gat("a soma e a diferença")
        self.play(caneta(F, ritmo=0.4))
        self.gat("pausa o vídeo e tenta")
        self.pausa()
        self.ate(1.0)

        # ── D5-3 · tabela, medidas e previsão ──
        self.an("D5-3")
        J = TC(jtex(1, 1, 1, -1), 1120, 320, 46, caneta=False)
        self.gat("a tabela")
        self.play(FadeOut(mt), *[FadeOut(q) for q in qs], F.animate.scale(0.8).move_to(PX(1120, 225), aligned_edge=LEFT), run_time=0.5)
        self.remove(mt, *qs)
        self.monta_tabela(J, sub_pz(F, 1), sub_pz(F, 3), "as derivadas dela são um e um", "a vertical é a diferença")
        self.gat("agora as medidas")
        self.play(FadeOut(F), run_time=0.4)
        self.remove(F)
        R1, R2 = self.medidas(0, 0, 2, 2, 470, ("rotacional o de baixo", "divergente a diagonal", "primeira deformação", "segunda um mais um"))
        sl, its = selos((False, False, True))
        self.gat("previsão não gira")
        self.play(FadeIn(its[0]), run_time=0.3)
        self.gat("não muda de área")
        self.play(FadeIn(sl[1]), FadeIn(its[1]), run_time=0.3)
        self.gat("só deforma")
        self.play(FadeIn(sl[3]), FadeIn(its[2]), run_time=0.3)
        self.ate(1.0)

        # ── D5-4 · solta (alvo 20) ──
        self.an("D5-4")
        sd = T("SÓ DEFORMA", 1120, 680, 44, cor=LIMA)
        fan = fantasma(VA, quad_pts(c1, s1))
        self.gat("solta")
        self.play(FadeOut(sl), FadeIn(sd), FadeIn(fan), run_time=0.4)
        self.remove(sl)
        a0 = ped.area()
        self.play(anda(ped, fl1, .5, 2.0, rate=linear, nome="D5 campo ①"))
        print(f"[D5] ①: área {a0:.4f} → {ped.area():.4f}")
        self.ate(1.0)

        # ── D5-5 · a resposta do palpite ──
        self.an("D5-5")
        ct = legenda("COMO TRANSFORMAÇÃO: ÁREA × 2", 1124, 815, CORAL, "left", 26)
        ac = leg_mix(["ÁREA CONSTANTE (", r"$\operatorname{div}=0$", ")"], 1124, 740, GEO, "left", 28)
        self.gat("como transformação essa fórmula")
        self.play(FadeIn(ct, shift=0.05 * UP), run_time=0.4)
        self.gat("como campo ela não muda")
        self.play(FadeIn(ac, shift=0.05 * UP), run_time=0.4)
        self.ate(1.0)

        # ── D5-6 · campo ② ──
        self.an("D5-6")
        self.secao_n("O DESAFIO · CAMPO", 2)
        c2, s2, T2 = (-1.8, -.6), 1.1, .7
        cmp.clear_updaters()
        p2 = quad30(VA, c2, s2)
        novo = mesma_grade(cmp, F2, 5)
        f2 = Pz([r"\ff=(", "1", r",\ ", r"\X-\Y", ")"], 1120, 270, 42)
        sai = [J, R1, R2, sd, ct, ac, ped, fan]
        self.gat("segundo campo")
        troca(self, "D5 campo ① → ②")
        self.play(*[FadeOut(m) for m in sai], Transform(cmp, novo), FadeIn(p2), run_time=1.0)
        self.remove(*sai)
        herda(cmp, novo)
        st2 = {"tr": NADA, "giro": NADA}
        clareira(cmp, lambda: ou(clar_ped(p2), dq(c2, s2), st2["tr"], st2["giro"]))
        self.gat("um na horizontal")
        self.play(caneta(f2, ritmo=0.4))
        self.gat("pausa e tenta")
        self.pausa()
        self.ate(1.0)

        # ── D5-7 · tabela e medidas ──
        self.an("D5-7")
        J2 = TC(jtex(0, 0, 1, -1), 1120, 380, 44, caneta=False)
        cel2 = self.monta_tabela(J2, sub_pz(f2, 1), sub_pz(f2, 3), "derivadas zero e zero", "a vertical um na direção")
        R1b, R2b = self.medidas(1, "-1", 1, 1, 520, ("rotacional um menos zero", "divergente zero mais", "deformações zero menos", "e um mais zero"))
        sl2, its2 = selos((True, True, True), 730)
        self.gat("previsão tudo junto")
        self.play(FadeIn(sl2), run_time=0.4)
        gt = leg_mix(["GIRA ", r"$\circlearrowleft$", " · ENCOLHE · ENTORTA"], 1120, 730, BR, "left", 38, up=True, bold=True)
        self.gat("gira no sentido anti-horário")
        self.play(FadeOut(sl2), FadeIn(gt), run_time=0.4)
        self.remove(sl2)
        self.ate(1.0)

        # ── D5-8 · dava para ler no desenho; solta (alvo 21) ──
        self.an("D5-8")
        ach = {xy: next(s for s in cmp if abs(s._xy[0] - xy[0]) < 1e-6 and abs(s._xy[1] - xy[1]) < 1e-6) for xy in ((1.5, -2.0), (2.5, -2.0), (2.5, -1.0))}
        for fr, cel, pts in (("andando para a direita a seta empina", (1, 0), ((1.5, -2.0), (2.5, -2.0))),
                             ("andando para cima a seta abaixa", (1, 1), ((2.5, -2.0), (2.5, -1.0)))):
            self.gat(fr)
            ds = [destaca_seta(ach[p]) for p in pts]
            g = cel2[cel]
            self.play(*[FadeIn(d) for d in ds], g.animate.scale(1.25), run_time=0.3)
            self.play(g.animate.scale(1 / 1.25), run_time=0.3)
            self.wait(0.6)
            self.play(*[FadeOut(d) for d in ds], run_time=0.3)
            self.remove(*ds)
        fan2 = fantasma(VA, quad_pts(c2, s2))
        tr = [ponto_fl(fl2, c2, T2 * i / 30) for i in range(31)]
        trl = vlinha(VA, tr, BR, 3, alpha=.9, dash=(6, 7)).set_z_index(8)
        trh = seta7(VA.c2p(*tr[27]), VA.c2p(*tr[30]), BR, 3, 14).set_z_index(8)
        c0 = ponto7(VA.c2p(*c2), BR, 5, 9)
        self.gat("solta o quadradinho viaja")
        self.add(fan2, c0)
        st2["tr"] = clarSeg([(tr[i], tr[i + 1]) for i in range(30)], .2)
        a0 = p2.area()
        self.play(anda(p2, fl2, T2, 2.0, rate=linear, nome="D5 campo ②"), Create(trl), run_time=2.0)
        self.play(FadeIn(trh), run_time=0.3)
        Fc = ponto_fl(fl2, c2, T2)
        gi = giro30(VA, Fc, .7, True)
        st2["giro"] = clarPoly(circ_pts(.8, Fc, 12), .1)
        self.play(Create(gi), run_time=0.4)
        print(f"[D5] ②: área {a0:.4f} → {p2.area():.4f} (× {p2.area() / a0:.3f}; e^(−0,7) = {math.exp(-.7):.3f}); centro {c2} → ({Fc[0]:.3f}, {Fc[1]:.3f})")
        v1, v2 = legenda("A VIAGEM É A SETA DO CENTRO,", 1124, 800, GEO, "left", 26), legenda("NÃO ESTÁ NA TABELA", 1124, 840, GEO, "left", 26)
        self.gat("a viagem não está na tabela")
        self.play(FadeIn(v1, shift=0.05 * UP), FadeIn(v2, shift=0.05 * UP), run_time=0.4)
        self.ate(1.0)

        # ── D5-9 · campo ③ (origem (360, 780), 240 px/u) ──
        self.an("D5-9")
        self.secao_n("O DESAFIO · CAMPO", 3)
        cmp.clear_updaters()
        zera_chapas()
        ch3 = chapa_px(*LA, nome="D5 ③ palco (360, 780) 240 px/u", v=V3)
        peds = [quad30(V3, p, .3) for p in PTS3]
        fans = [fantasma(V3, quad_pts(p, .3)) for p in PTS3]
        labs = [TXP30("(1, 0): SÓ CRESCE", *canto_xy(V3, 1.0, -.38), 26), TXP30("(0, 1): SÓ GIRA", *canto_xy(V3, 0, 1.4), 26),
                TXP30("(1, 1): GIRA E CRESCE", *canto_xy(V3, 1.8, 1.4), 26)]
        st3 = {"on": [False] * 3, "fan": False, "giros": []}
        rotl = clar28([(.45, -.45, 1.55, -.3), (-.6, 1.38, .6, 1.52), (1.15, 1.38, 2.45, 1.52)])
        c3 = campo30(V3, F3, -.75, 2.75, -.25, 2.25, .25, rmin=0, mmax=6, skip=rotl, nome="D5 f₃")
        clareira(c3, lambda: ou(*[clar_ped(p, .12) for p, on in zip(peds, st3["on"]) if on],
                                *([dq(p, .3, .12) for p in PTS3] if st3["fan"] else []), *st3["giros"]))
        ex3 = VGroup(linha_rec(V3, [(-.95, 0), (2.95, 0)], LA, GEO, 2, .4), linha_rec(V3, [(0, -.45), (0, 2.45)], LA, GEO, 2, .4))
        F3t = Pz([r"\F=(", r"\X^2-\Y^2", r",\ ", r"2\X\Y", ")"], 1120, 260, 42)
        self.gat("terceiro campo")
        self.limpa_junto()
        troca(self, "D5 campo ② → ③ (muda a origem do palco: a grade nova entra com o campo)")
        self.play(FadeIn(ch3), FadeIn(ex3), cresce_campo(c3, 0.8), run_time=0.8)
        self.play(caneta(F3t, ritmo=0.35))
        J3 = TC(r"J=\begin{pmatrix}\Am{2x} & \Mg{-2y}\\ \Am{2y} & \Mg{2x}\end{pmatrix}", 1120, 380, 42, caneta=False)
        self.monta_tabela(J3, sub_pz(F3t, 1), sub_pz(F3t, 3), "derivando a diferença dos quadrados", "derivando duas vezes o produto")
        self.gat("pausa o vídeo e prevê")
        self.pausa()
        st3["fan"] = True
        self.play(*[FadeIn(f) for f in fans], run_time=0.5)
        self.ate(1.0)

        # ── D5-10 · as medidas e a previsão ponto a ponto ──
        self.an("D5-10")
        R13 = Pz([r"\rot=\V{4\Y}\qquad", r"\dv=\D{4\X}"], 1120, 510, 42, caneta=False)
        R23 = TC(r"d_1=\Lm{0}\qquad d_2=\Lm{0}", 1120, 590, 42)
        self.gat("rotacional quatro vezes")
        self.play(caneta(sub_pz(R13, 0), ritmo=0.35))
        self.gat("divergente quatro vezes")
        self.play(caneta(sub_pz(R13, 1), ritmo=0.35))
        junta_partes(self, R13)
        ne = T("NUNCA ENTORTA", 1120, 700, 44, cor=LIMA)
        self.gat("e as duas deformações dão zero")
        self.play(caneta(R23, ritmo=0.35))
        self.play(FadeIn(ne, shift=0.05 * UP), run_time=0.4)
        for k, fr in enumerate(("no ponto um zero", "no zero um", "no um um")):
            self.gat(fr)
            st3["on"][k] = True
            self.play(FadeIn(peds[k]), FadeIn(labs[k]), run_time=0.4)
        self.ate(1.0)

        # ── D5-11 · solta os três (alvo 22) ──
        self.an("D5-11")
        self.gat("solta os três")
        a0 = [p.area() for p in peds]
        self.play(*[anda(p, fl3, .1, 2.0, rate=linear, nome=f"D5 ③ {PTS3[i]}") for i, p in enumerate(peds)])
        gs = []
        for p in ((0, 1), (1, 1)):
            Fc = ponto_fl(fl3, p, .1)
            gs.append(giro30(V3, Fc, .3, True))
            st3["giros"].append(clarPoly(circ_pts(.36, Fc, 10), .05))
        self.play(*[Create(g) for g in gs], run_time=0.4)
        for i, p in enumerate(peds):
            q = angulos_quinas(p)
            print(f"[D5] ③ {PTS3[i]}: área {a0[i]:.4f} → {p.area():.4f} (× {p.area() / a0[i]:.3f}); quinas {', '.join(f'{x:.2f}°' for x in q)}; "
                  f"maior desvio do reto {max(abs(x - 90) for x in q):.2f}°")
        q1, q2 = legenda("QUINAS A MENOS DE 2° DO ÂNGULO RETO:", 1124, 775, GEO, "left", 26), legenda("A TABELA FALA DO PONTO, NAQUELE INSTANTE", 1124, 815, GEO, "left", 26)
        self.gat("e nenhum entorta")
        self.play(FadeIn(q1, shift=0.05 * UP), run_time=0.4)
        self.gat("a tabela fala do que acontece")
        self.play(FadeIn(q2, shift=0.05 * UP), run_time=0.4)
        self.ate(1.0)

        # ── D5-12 · desafio cumprido: a cadeia por 2 s ──
        self.an("D5-12")
        col = [F3t, J3, R13, R23, ne, q1, q2]
        cad1 = leg_mix(["FÓRMULA ", T("→", 0, 0, 32, cor=GEO), " TABELA ", T("→", 0, 0, 32, cor=GEO)], 1120, 520, BR, "left", 32, bold=True)
        cad2 = leg_mix(["4 NÚMEROS ", T("→", 0, 0, 32, cor=GEO), " QUADRADINHO"], 1120, 580, BR, "left", 32, bold=True)
        self.gat("desafio cumprido")
        self.play(*[FadeOut(m) for m in col], FadeIn(cad1), FadeIn(cad2), run_time=0.4)
        self.wait(2.0)
        self.play(FadeOut(cad1), FadeOut(cad2), *[FadeIn(m) for m in col], run_time=0.4)
        self.remove(cad1, cad2)
        c3.clear_updaters()
        self.sai_fim()

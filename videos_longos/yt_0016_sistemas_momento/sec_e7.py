"""Lote Q7 (v3): E7 — o caçador no lago. PALCO fixo: manequim 3D com a arma no lago congelado; um tiro por bloco (horizontal, 56°,
horizontal), cada tiro em câmera lenta (chip CÂMERA LENTA) e o recuo em VELOCIDADE REAL (0,0559 e 0,0313 m/s); as trocas de tiro são
crossfade entre duas instâncias do manequim. No tiro a 56°, a normal do gelo cresce nos pés e fica marcada; o momento da bala é decomposto
(p_x, p_y) a partir da ponta real do cano. 72,5 kg; bala 4,20 g a 965 m/s. Energias 1.956 J × 0,113 J (razão ≈ 17.262), barras na CONTA."""
from kit import *  # noqa: F401,F403
from sec_manequim import ManequimTomadas, boca, pose_mira

MC, MBALA, VBALA, ANG = 72.5, 0.00420, 965.0, math.radians(56.0)
V_H = MBALA * VBALA / MC
V_56 = V_H * math.cos(ANG)
KB, KCZ = MBALA * VBALA ** 2 / 2, MC * V_H ** 2 / 2
RAZ = MC / MBALA
assert abs(V_H - 0.0559) < 1e-4 and abs(V_56 - 0.0313) < 1e-4 and abs(KB - 1955.6) < 0.1 and abs(KCZ - 0.1133) < 1e-3
assert abs(KB / KCZ - RAZ) < 1e-6 * RAZ and round(RAZ) == 17262 and abs(KB / (KB + KCZ) - 0.999942) < 1e-6

TS = 1.6                      # disparo, s depois do começo do ciclo
SL = 1.4                      # janela de câmera lenta (s de tela) a partir do disparo
VBV = 1.2                     # a bala na tela durante a câmera lenta (m/s); a física fica ×VBV/VBALA mais lenta
R_LENTO = VBV / VBALA
DBALA = 0.3                   # a bala some depois de 0,3 m (antes de sair do PALCO)
KV = 9.0                      # seta do recuo: unidades por m/s
LPB = 0.8                     # seta do momento da bala na tela (a ponta fica dentro da fronteira)


def tau(s, ts=TS):
    """Tempo físico desde o começo do ciclo (s de tela), com a câmera lenta na janela do disparo."""
    if s < ts:
        return s
    if s < ts + SL:
        return ts + (s - ts) * R_LENTO
    return ts + SL * R_LENTO + (s - ts - SL)


class LoteE7(Base):
    def construct(self):
        self.setup_base(cap="EXERCÍCIO 7 · O CAÇADOR NO LAGO", selo="MOMENTO POR COMPONENTE")
        self.cic = [dict(ang=0.0, V=V_H, ts=TS + 2.0, x0=0.0)]  # o primeiro tiro sai um pouco depois
        # v4: uma instância só; cada tiro começa numa virada em sequência (nunca dois caçadores em crossfade)
        self.ml = ManequimTomadas(self, self.pose, K=1.75, xt=-3.2, yc=-3.15, camx=0.0, op=0.0)
        self.ml.f3d.conta.set_value(1.0)
        for f in self.ml.f3ds:
            self.add(f)
        self.e7_1_2()
        self.e7_3_4()
        self.e7_5()
        self.fim()
        self.relatorio()

    def c(self):
        """(parâmetros do ciclo corrente, s dentro dele)."""
        k, n, s = self.ml.ciclo(self.clk.get_value())
        return self.cic[k], s

    def pose(self, k, n, s):
        c = self.cic[k]
        ts = c["ts"]
        dtau = max(0.0, tau(s, ts) - ts)
        x = c.get("x0", 0.0) - c["V"] * dtau
        rec = math.exp(-max(0.0, s - ts) / 0.25) * (1 if s >= ts else 0)
        ang = c["ang"]
        if k == 0 and s < ts:                       # v6 (palco vivo): antes do primeiro tiro o caçador ajusta a mira devagar
            ang = ang + 0.11 * math.sin(0.9 * s) * min(1.0, s / 1.5) * min(1.0, (ts - s) / 1.0)
        p = pose_mira(x, ang, 1, recuo=rec)
        p["rifle"] = {"on": True, "ang": ang}
        d = VBALA * dtau
        p["bala"] = d if 0 < d < DBALA and s < ts + SL else None
        return p

    def boca_real(self):
        """Ponta do cano como o 3D a projetou; sem pontos.json, o mapa analítico."""
        e = self.ml.e()
        r = self.ml.real("pb")
        if r is not None:
            return r
        bx, bz, _ = boca(e, e["rifle"]["ang"])
        return self.ml.m(bx, bz)

    def maos_real(self):
        a, b = self.ml.real("mao0"), self.ml.real("mao1")
        if a is None or b is None:
            e = self.ml.e()
            _, _, (cx, cz) = boca(e, e["rifle"]["ang"])
            return self.ml.m(cx, cz)
        return (a + b) / 2

    def lento(self):
        def f():
            c, s = self.c()
            ts = c["ts"]
            o = min(1.0, max(0.0, (s - ts + 0.4) / 0.3), max(0.0, (ts + SL + 0.3 - s) / 0.3))
            return chip_lento(0.85 * o, x=-2.0, y=2.5)        # v5 (V12): canto superior direito do PALCO, fora da fronteira
        return always_redraw(f)

    def setas(self):
        """Clarão e seta do recuo (velocidade real) do ciclo corrente; fades nas trocas de ciclo."""
        def f():
            e = self.ml.e()
            c, s = self.c()
            k = self.ml.ciclo(self.clk.get_value())[0]
            g = VGroup()
            op = self.ml.resta(self.clk.get_value())
            op = min(op, s / 0.3) if k > 0 else op
            ts = c["ts"]
            if ts <= s < ts + 0.25:
                g.add(Star(n=7, outer_radius=0.22, inner_radius=0.09, color=WHITE_).set_fill(WHITE_, 0.9).set_stroke(width=0)
                      .move_to(self.boca_real()).set_z_index(13))
            if ts <= s < ts + 1.1:                       # v6 (1.2): a bala, em traço de aço, sai pela borda do PALCO
                d = P3(math.cos(c["ang"]), math.sin(c["ang"]))
                b0 = self.boca_real()
                a_ = b0 + d * (0.15 + 7.5 * (s - ts) / 1.1)
                if a_[0] < 0.55 and a_[1] < 2.6:
                    g.add(Line(a_ - 0.55 * d, a_).set_stroke(GEO, 5).set_z_index(13), Dot(a_, radius=0.05, color=GEO).set_z_index(13))
            if s >= ts + 0.2:
                q = self.ml.m(e["hx"], 0.5)
                L = KV * c["V"]
                a = arrow(q + P3(-0.35, 0), q + P3(-0.35 - L, 0), color=VEL, width=7, tip=0.17, z=12)
                g.add(a, mtex(r"\vec V", VEL, 32).next_to(a, UP, buff=0.15))
            return escala_op(g, max(op, 0)) if op < 1 else g
        return always_redraw(f)

    def tiro(self, ang, V, x0=0.0, *saem):
        """Tomada nova (virada em sequência: o 3D sai, a pose troca, volta) com o disparo TS s depois."""
        self.cic.append(dict(ang=ang, V=V, ts=TS, x0=x0))
        self.ml.troca(*[FadeOut(m) for m in saem])

    # ── E7-1, E7-2: tiro horizontal ───────────────────────────────────────────────────────────────────────
    def e7_1_2(self):
        self.an("E7-1")
        self.cic[0]["ts"] = self.clk_de("E7-2", "o tiro na horizontal", -0.4) - self.ml.inicios[0]
        self.play(*self.ml.fade(1.0), run_time=1.0)
        # no canto de cima da fronteira (à esquerda: no canto direito ficam o cano a 56° e a seta p da bala)
        lg = txt("LAGO CONGELADO · SEM ATRITO", 16, color=BLUE_L).move_to(P3(-7.1, 1.85), aligned_edge=LEFT)
        fr = fronteira(7.4, 5.6, P3(-3.75, -0.6), rotulo=["CAÇADOR", mais(22), "ARMA", mais(22), "BALA"])
        sg = self.sg = self.setas()
        self.lt = self.lento()
        self.add(sg, self.lt)
        self.diz("num lago congelado")
        self.play(FadeIn(lg), run_time=0.6)
        dados = VGroup(MathTex(r"M=72{,}5\ \mathrm{kg}", font_size=40), MathTex(r"m=4{,}20\ \mathrm{g}", font_size=40),
                       MathTex(r"v=965\ \mathrm{m/s}", font_size=40, color=VEL)).arrange(DOWN, buff=0.22, aligned_edge=LEFT)
        na_conta(dados, 1.5)
        self.diz("Ele e a arma têm")
        self.play(Create(fr[0]), FadeIn(fr[1]), run_time=0.9)
        self.diz("setenta e dois vírgula cinco")
        self.play(FadeIn(dados[0]), run_time=0.5)
        self.diz("quatro vírgula dois gramas")
        self.play(FadeIn(dados[1]), run_time=0.5)
        self.diz("novecentos e sessenta e cinco")
        self.play(FadeIn(dados[2]), run_time=0.5)
        self.ate(0.97)
        self.an("E7-2")
        th = txt("TIRO HORIZONTAL", 20, bold=True)
        e1 = MathTex(r"0=m\,v-M\,V", font_size=42)
        e2 = Mc(r"V=\frac{0{,}00420\cdot 965}{72{,}5}=", (r"0{,}0559\ \mathrm{m/s}", VEL), size=40)
        for m_, y in ((th, 0.15), (e1, -0.45), (e2, -1.35)):
            na_conta(m_, y)
        self.play(FadeIn(th), run_time=0.5)
        self.diz("Depois, continua zero")
        self.play(FadeIn(e1, shift=0.1 * UP), run_time=0.8)
        LP2 = 1.1

        def iguais():                                   # v6 (1.2): p⃗_bala na ponta do cano e p⃗_caçador nas costas, opostas, iguais
            e = self.ml.e()
            b = self.boca_real() + P3(0.15, 0.32)
            c_ = self.ml.m(e["hx"], 1.25) + P3(-0.55, 0)
            a1 = arrow(b, b + P3(LP2, 0), color=MAG, width=7, tip=0.18, z=13)
            a2 = arrow(c_, c_ + P3(-LP2, 0), color=MAG, width=7, tip=0.18, z=13)
            return VGroup(a1, mtex(r"\vec p_{\text{bala}}", MAG, 30).next_to(a1.get_end(), UP, buff=0.15),
                          a2, mtex(r"\vec p_{\text{caçador}}", MAG, 30).next_to(a2.get_end(), UP, buff=0.15))
        ig = always_redraw(iguais)
        mt = txt("MESMO TAMANHO", 16, color=MAG).next_to(e1, RIGHT, buff=0.4)
        self.diz("o momento da bala para a frente")
        self.play(FadeIn(ig), FadeIn(mt), run_time=0.8)
        self.diz("A velocidade de recuo")
        self.play(FadeIn(e2[0], shift=0.1 * UP), run_time=0.8)
        cm = txt("UNS 5,6 CENTÍMETROS POR SEGUNDO: DÁ PARA VER", 16, color=DIM)
        na_conta(cm, -2.05)
        self.diz("cinco vírgula seis centímetros")
        self.play(FadeIn(e2[1:], shift=0.1 * UP), FadeIn(cm), run_time=0.7)       # v6 (1.3): o resultado quando é dito
        self.ate(0.97)
        self.fr, self.lg = fr, lg
        self.c2 = VGroup(dados, th, e1, e2, cm, mt)
        self.ig = ig

    # ── E7-3, E7-4: tiro a 56°, a normal do gelo, p_x e p_y ───────────────────────────────────────────────
    def e7_3_4(self):
        self.an("E7-3")
        self.tiro(ANG, V_56, 0.35)
        t_ciclo = self.ml.inicios[-1]
        self.cic[-1]["ts"] = max(TS, self.clk_de("E7-3", "A bala leva momento para cima", 0.1) - t_ciclo)
        TSc = self.cic[-1]["ts"]
        self.ig.clear_updaters()
        self.play(self.c2.animate.set_opacity(0.4), FadeOut(self.ig), run_time=0.3)
        self.remove(self.ig)
        marca = ValueTracker(0.0)          # 1 = a normal fica marcada a 50 %
        nv = ValueTracker(0.0)             # v6 (1.3): a normal entra no "Foi o gelo!"…
        pg = ValueTracker(0.0)             # …e cresce no "a normal do gelo cresce de repente"
        dec = ValueTracker(0.0)            # decomposição p_x, p_y
        xy = ValueTracker(0.0)             # X sobre p_y
        lig = ValueTracker(0.0)            # p_x ligado ao recuo

        def arco():
            c = self.maos_real()
            r = 0.75
            return VGroup(Arc(radius=r, start_angle=0, angle=ANG, arc_center=c).set_stroke(WHITE_, 2),
                          DashedLine(c, c + P3(1.1, 0), dash_length=0.06).set_stroke(DIM, 1.5),
                          mtex(r"56^\circ", WHITE_, 28).move_to(c + P3(1.22, 0.4)))
        ar = always_redraw(arco)

        def normal():
            s = self.clk.get_value() - t_ciclo
            e = self.ml.e()
            g = VGroup()
            if nv.get_value() < 0.01:
                return g
            o = nv.get_value()
            L = 0.65 + 1.75 * pg.get_value()
            pe = self.ml.m(e["hx"], 0.0) + P3(-1.3, 0)          # v5 (V13): mais atrás, longe da seta do recuo; rótulo à esquerda
            a = arrow(pe, pe + P3(0, L), color=BLUE_L, width=9, tip=0.22, z=12)
            lab = VGroup(mtex(r"\vec N", BLUE_L, 32), mtxt("(EXTERNA,", 14, color=BLUE_L), mtxt("IMPULSIVA)", 14, color=BLUE_L)) \
                .arrange(DOWN, buff=0.06, aligned_edge=RIGHT)
            lab.next_to(pe + P3(0, 0.6), LEFT, buff=0.2)
            g.add(a, lab)
            o *= 1.0 - 0.5 * marca.get_value()
            return escala_op(g, o) if o < 1 else g
        nm = always_redraw(normal)

        def pbala():
            s = self.clk.get_value() - t_ciclo
            g = VGroup()
            if s < TSc + 0.15:
                return g
            o = min(1.0, (s - TSc - 0.15) / 0.4)
            b = self.boca_real()
            d = P3(math.cos(ANG), math.sin(ANG))
            tip = b + LPB * d
            a = arrow(b, tip, color=MAG, width=7, tip=0.2, z=13)
            g.add(a, mtex(r"\vec p_{\text{bala}}", MAG, 32).next_to(b + 0.45 * LPB * d, LEFT, buff=0.3))   # v5 (V14): longe da ponta
            return escala_op(g, o) if o < 1 else g
        pb = always_redraw(pbala)
        self.add(nm, pb)
        self.play(FadeOut(self.c2), run_time=0.4)
        self.diz("a cinquenta e seis graus")
        self.play(FadeIn(ar), run_time=0.6)
        q = txt("QUEM SEGUROU ELE?", 26, bold=True)
        na_conta(q, 2.3)
        e_ = self.ml.e()
        topo, pe_ = self.ml.m(e_["hx"], 1.05) + P3(1.0, 0), self.ml.m(e_["hx"], 0.3) + P3(1.0, 0)
        bx = VGroup(DashedVMobject(Arrow(topo, pe_, buff=0, color=MAG, stroke_width=6, tip_length=0.2), num_dashes=9),
                    txt("?", 28, bold=True, color=MAG).next_to((topo + pe_) / 2, RIGHT, buff=0.3))
        self.diz("deveria ganhar momento para baixo")
        self.play(FadeIn(bx), run_time=0.6)                                       # v6 (1.2)
        rk = risco(bx[0], cor=WHITE_, w=5)
        self.diz("não afunda no gelo")
        self.play(Create(rk), run_time=0.5)
        self.diz("Então quem segurou ele")
        self.play(FadeIn(q), run_time=0.6)
        self.ate(0.97)
        self.an("E7-4")
        self.diz("Foi o gelo")
        self.play(FadeOut(q), FadeOut(bx), FadeOut(rk), nv.animate.set_value(1.0), run_time=0.6)
        self.diz("a normal do gelo cresce")
        self.play(pg.animate(rate_func=there_and_back).set_value(1.0), run_time=1.4)
        g1 = linha(tex(r"\vec N", FC, 34), "DO GELO: EXTERNA E IMPULSIVA", size=18, buff=0.12)
        g1[1].set_color(FC)
        p1 = linha(tex(r"P_y", MAG, 42), "NÃO SE CONSERVA", size=24, buff=0.2)
        p2 = linha(tex(r"P_x", MAG, 42), "SE CONSERVA", size=24, buff=0.2)
        mv = Mc(r"M\,V", "=", (r"m\,v\cos 56^\circ", MAG), size=40)
        e3 = Mc(r"V=0{,}0559\cdot\cos 56^\circ=", (r"0{,}031\ \mathrm{m/s}", VEL), size=40)
        for m_, y in ((g1, 2.3), (p1, 1.45), (p2, 0.65), (mv, -0.1), (e3, -1.05)):
            na_conta(m_, y)
        # v6 (N6): a decomposição numa cópia ampliada de p⃗_bala, na CONTA
        O2, LB = P3(5.15, 0.05), 1.9
        dv = P3(math.cos(ANG), math.sin(ANG))
        tip2, cx2 = O2 + LB * dv, O2 + P3(LB * math.cos(ANG), 0)
        big = arrow(O2, tip2, color=MAG, width=8, tip=0.22)
        lbig = mtex(r"\vec p_{\text{bala}}", MAG, 30).next_to(O2 + 0.5 * LB * dv, LEFT, buff=0.3)
        px2 = DashedLine(O2, cx2, dash_length=0.09).set_stroke(MAG, 4)
        py2 = DashedLine(cx2, tip2, dash_length=0.09).set_stroke(MAG, 4)
        lx2 = mtex(r"p_x", MAG, 32).next_to(px2, DOWN, buff=0.15)
        ly2 = mtex(r"p_y", MAG, 32).next_to(py2, RIGHT, buff=0.18)
        m2 = cx2 + 0.5 * (tip2 - cx2)
        X2 = VGroup(Line(m2 + P3(-0.15, -0.15), m2 + P3(0.15, 0.15)), Line(m2 + P3(-0.15, 0.15), m2 + P3(0.15, -0.15))).set_stroke(WHITE_, 5)
        self.diz("Ela é externa e impulsiva")
        self.play(FadeIn(g1), marca.animate.set_value(1.0), run_time=0.7)
        self.diz("na vertical, o momento não se conserva")
        self.play(TransformFromCopy(pb[0], big), FadeIn(lbig), run_time=0.8)
        self.play(Create(px2), Create(py2), FadeIn(lx2), FadeIn(ly2), run_time=0.6)
        # as variáveis saem do desenho para a conta
        self.play(TransformFromCopy(ly2, p1[0]), FadeIn(p1[1], shift=0.1 * UP), Create(X2), run_time=0.9)
        self.diz("Mas na horizontal")
        self.play(TransformFromCopy(lx2, p2[0]), FadeIn(p2[1], shift=0.1 * UP), run_time=0.9)
        self.diz("Só a parte horizontal")
        # p_x sai da cópia ampliada, passa POR CIMA da cabeça do caçador, gira 180° e pousa como a seta do recuo
        b = O2
        cxp = cx2
        copia = Arrow(b, cxp, buff=0, color=MAG, stroke_width=6, tip_length=0.18)
        e = self.ml.e()
        qv = self.ml.m(e["hx"], 0.5)
        alvo = Arrow(qv + P3(-0.35, 0), qv + P3(-0.35 - KV * V_56, 0), buff=0, color=VEL, stroke_width=7, tip_length=0.17)
        cab = self.ml.real("cab")
        cab = self.ml.m(e["hx"], e["hz"] + 0.86) if cab is None else cab
        caminho = VMobject().set_points_smoothly([(b + cxp) / 2, P3(1.0, 2.2), cab + P3(0.7, 0.9), cab + P3(-0.5, 1.0),
                                                   qv + P3(-1.6, 0.9), alvo.get_center()])
        self.play(MoveAlongPath(copia, caminho), Rotate(copia, PI), FadeIn(mv, shift=0.1 * UP), run_time=1.6)
        self.play(ReplacementTransform(copia, alvo), run_time=0.3)
        self.play(FadeOut(alvo), Indicate(mv, color=WHITE_, scale_factor=1.05), run_time=0.6)
        self.diz("o cosseno de cinquenta e seis graus")
        self.play(Indicate(mv[2], color=WHITE_, scale_factor=1.06), run_time=0.8)
        self.diz("O recuo cai")
        self.play(FadeIn(e3[0], shift=0.1 * UP), run_time=0.8)
        tc = txt("UNS 3 CENTÍMETROS POR SEGUNDO", 16, color=DIM)
        na_conta(tc, -1.7)
        self.diz("três centímetros por segundo")
        self.play(FadeIn(e3[1:], shift=0.1 * UP), FadeIn(tc), run_time=0.6)
        self.ate(0.97)
        for m_ in (ar, nm, pb):
            m_.clear_updaters()
        self.c4 = VGroup(g1, p1, p2, mv, e3, tc, ar, nm, pb, big, lbig, px2, py2, lx2, ly2, X2)

    # ── E7-5: energias (barras na CONTA, em painel escuro), o PALCO repetindo o tiro horizontal ─────────────
    def e7_5(self):
        self.an("E7-5")
        self.tiro(0.0, V_H, 0.0, *self.c4)               # o tiro horizontal de novo: um replay só (chip REPLAY)
        rp = chip_replay(x=-0.3, y=2.5)                   # v6 (N2): folga ≥ 0,4 do CÂMERA LENTA
        self.play(FadeIn(rp), run_time=0.3)
        self.rp = rp
        th = txt("TIRO HORIZONTAL", 16, color=DIM)
        na_conta(th, -3.3)
        ra = Mc((r"\frac{K_{\text{bala}}}{K_{\text{caçador}}}", KC), r"\approx 17.262=", (r"\frac{72{,}5}{0{,}0042}", KC), size=38)
        na_conta(ra, 2.15)
        pc = linha(tex(r"\approx 99{,}994\%", KC, 40), "NA BALA", size=22, buff=0.15)
        na_conta(pc, 1.25)
        yb = -2.09                                        # v5 (V15): folga ≥ 0,25 do texto de cima e da DICA
        painel = RoundedRectangle(corner_radius=0.12, width=5.55, height=3.35).set_stroke(BLUE_L, 1.5, opacity=0.5) \
            .set_fill(PANEL, 0.92).move_to(P3(XC0 + 2.62, yb - 0.4 + 3.35 / 2)).set_z_index(-1)
        # momento: barras iguais
        pm = VGroup(*[barra2(0.6, 2.2, MAG).move_to(P3(x, yb + 1.1))
                      for x in (1.85, 2.75)])
        lpm = VGroup(txt("BALA", 14, color=DIM).next_to(pm[0], DOWN, buff=0.08), txt("CAÇADOR", 14, color=DIM).next_to(pm[1], DOWN, buff=0.08))
        tpm = txt("MOMENTO", 16, color=MAG).next_to(pm, UP, buff=0.12)
        vpm = tex(r"4{,}05\ \mathrm{kg\cdot m/s}", MAG, 24).next_to(tpm, UP, buff=0.06)
        # energia em escala log (10^-2 a 10^4 J)
        xa, hd = 4.15, 0.38
        ylog = lambda v: yb + hd * (math.log10(v) + 2)
        eixo = Line(P3(xa, yb), P3(xa, ylog(1e4) + 0.1)).set_stroke(DIM, 2)
        tk = VGroup(*[VGroup(Line(P3(xa - 0.06, ylog(10 ** k)), P3(xa + 0.06, ylog(10 ** k))).set_stroke(DIM, 2),
                             tex(rf"10^{{{k}}}", DIM, 20).next_to(P3(xa - 0.06, ylog(10 ** k)), LEFT, buff=0.06)) for k in (-2, 0, 2, 4)])
        te = txt("ENERGIA (ESCALA LOG)", 15, color=KC).move_to(P3(xa + 1.0, ylog(1e4) + 0.38))
        eb = barra2(0.6, ylog(KB) - yb, KC).move_to(P3(xa + 0.6, (ylog(KB) + yb) / 2))
        ec = barra2(0.6, ylog(KCZ) - yb, KC).move_to(P3(xa + 1.4, (ylog(KCZ) + yb) / 2))
        veb = tex(r"1.956\ \mathrm{J}", KC, 22).next_to(eb, RIGHT, buff=0.06).align_to(eb, UP)
        vec = tex(r"0{,}11\ \mathrm{J}", KC, 22).next_to(ec, UP, buff=0.06)
        lec = VGroup(txt("BALA", 14, color=DIM).next_to(eb, DOWN, buff=0.08), txt("CAÇADOR", 14, color=DIM).next_to(ec, DOWN, buff=0.08))
        base = Line(P3(1.45, yb), P3(6.4, yb)).set_stroke(DIM, 2)
        self.play(FadeIn(painel), FadeIn(th), FadeIn(base), run_time=0.5)
        self.diz("momentos do mesmo tamanho")
        self.play(GrowFromEdge(pm[0], DOWN), GrowFromEdge(pm[1], DOWN), FadeIn(lpm), FadeIn(tpm), FadeIn(vpm), run_time=0.9)
        self.diz("Olha as barras")
        self.play(FadeIn(eixo), FadeIn(tk), FadeIn(te), run_time=0.6)
        self.diz("quase dois mil joules")
        self.play(GrowFromEdge(eb, DOWN), FadeIn(veb), FadeIn(lec[0]), run_time=0.9)
        self.diz("onze centésimos de joule")
        self.play(GrowFromEdge(ec, DOWN), FadeIn(vec), FadeIn(lec[1]), run_time=0.8)
        self.diz("dezessete mil vezes")
        self.play(FadeIn(ra[:2], shift=0.1 * UP), run_time=0.8)
        self.diz("a massa do caçador dividida")
        self.play(FadeIn(ra[2:], shift=0.1 * UP), run_time=0.6)
        self.diz("noventa e nove vírgula nove nove")
        self.play(FadeIn(pc, shift=0.1 * UP), run_time=0.7)
        # v5 (revisão de física): energia pequena no caçador não quer dizer coice fraco (a força depende da duração do impulso)
        ck = VGroup(txt("ENERGIA PEQUENA", 16, color=WHITE_), linha(tex(r"\neq", WHITE_, 30), "COICE FRACO", size=16, buff=0.12)) \
            .arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        ck.move_to(P3(4.9 + ck.width / 2, 1.3))                 # v5: à direita do 99,994 %, longe da DICA e do painel
        d = dica("ISOLADO NA HORIZONTAL", "NÃO É ISOLADO NA VERTICAL")
        self.diz("Por isso o caçador recua")                   # v6 (1.3): a DICA antes do "Mas cuidado", não durante a frase do coice
        self.play(FadeOut(th), run_time=0.3)
        self.dica_entra(d)
        self.diz("Mas cuidado")
        self.play(FadeIn(ck), run_time=0.5)
        self.diz("depende também de quanto tempo")
        self.play(Indicate(ck, color=WHITE_, scale_factor=1.05), run_time=0.9)
        self.sobra(0.55)
        self.sg.clear_updaters(); self.lt.clear_updaters()
        self.remove(self.rp)
        self.clear(rt=0.5)

"""Patch da rodada final pré-narração (aplicado uma vez sobre o cena.py da entrega de referência)."""
import os, sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()
fails = []


def rep(a, b, count=1):
    global s
    n = s.count(a)
    if n != count:
        fails.append("(%d x) %s" % (n, a[:100].replace("\n", "⏎")))
        return
    s = s.replace(a, b)


# ── 1 · STEEL: matéria condutora ≠ corrente ≠ carga ─────────────────────────────────────────────────────────
rep('''GREEN = "#3FE08B"           # CORRENTE (I, K, J): o mesmo verde do vid_0009; carga continua azul
''', '''GREEN = "#3FE08B"           # CORRENTE (I, K, J): o mesmo verde do vid_0009; carga continua azul
STEEL = "#7A8696"           # matéria condutora / fio (corpo material): cinza-aço neutro, distinto da corrente (verde) e da carga (azul)
''')
rep('''color=BLUE_L, stroke_width=LW_WIRE))''', '''color=STEEL, stroke_width=LW_WIRE))''')
rep('''g.add(Line(P3(0, 0, 0), P3(L, 0, 0), color=BLUE_L, stroke_width=6))''', '''g.add(Line(P3(0, 0, 0), P3(L, 0, 0), color=STEEL, stroke_width=6))''')
rep('''top = Polygon(P3(0, 0, t), P3(L, 0, t), P3(L, w, t), P3(0, w, t), color=BLUE_L, stroke_width=2.5,
                              fill_color=BLUE, fill_opacity=0.16)''', '''top = Polygon(P3(0, 0, t), P3(L, 0, t), P3(L, w, t), P3(0, w, t), color=STEEL, stroke_width=2.5,
                              fill_color=STEEL, fill_opacity=0.16)''')
rep('''front = Polygon(P3(0, 0, 0), P3(L, 0, 0), P3(L, 0, t), P3(0, 0, t), color=BLUE_L, stroke_width=2.5,
                                    fill_color=BLUE, fill_opacity=0.10)''', '''front = Polygon(P3(0, 0, 0), P3(L, 0, 0), P3(L, 0, t), P3(0, 0, t), color=STEEL, stroke_width=2.5,
                                    fill_color=STEEL, fill_opacity=0.10)''')
rep('''end = Polygon(P3(L, 0, 0), P3(L, w, 0), P3(L, w, t), P3(L, 0, t), color=BLUE_L, stroke_width=2.5,
                                  fill_color=BLUE, fill_opacity=0.22)''', '''end = Polygon(P3(L, 0, 0), P3(L, w, 0), P3(L, w, t), P3(L, 0, t), color=STEEL, stroke_width=2.5,
                                  fill_color=STEEL, fill_opacity=0.22)''')
rep('''wire = Line([-6.2, WY, 0], [3.9, WY, 0], color=BLUE_L, stroke_width=7).set_opacity(0.45)''',
    '''wire = Line([-6.2, WY, 0], [3.9, WY, 0], color=STEEL, stroke_width=7).set_opacity(0.85)''')
rep('''wire = Line([-3.0, 0.3, 0], [3.0, 0.3, 0], color=BLUE_L, stroke_width=6).set_opacity(0.45)''',
    '''wire = Line([-3.0, 0.3, 0], [3.0, 0.3, 0], color=STEEL, stroke_width=6).set_opacity(0.85)''')
rep('''wl = Line([-WX, -2.0, 0], [-WX, 1.9, 0], color=BLUE_L, stroke_width=6)''', '''wl = Line([-WX, -2.0, 0], [-WX, 1.9, 0], color=STEEL, stroke_width=6)''')
rep('''wr = Line([WX, -2.0, 0], [WX, 1.9, 0], color=BLUE_L, stroke_width=6)''', '''wr = Line([WX, -2.0, 0], [WX, 1.9, 0], color=STEEL, stroke_width=6)''')

# ── 2 · morph: tudo numa só passada (nunca um estado intermediário incompleto, como "P_B = · v") ──────────────
rep('''        # fases: 1) sai o que não sobrevive; 2) os símbolos que ficam se movem; 3) entram os novos (nunca dois símbolos no mesmo lugar)
        fases = [(outs, 0.3), (moves, 0.7), (ins, 0.5)]
        fases = [f for f in fases if f[0]]
        for a_, w in fases:
            self.play(*a_, run_time=run if len(fases) == 1 else max(0.35, run * w), rate_func=smooth)
        self.cur = new
        return new''', '''        # uma só passada: o que sai e o que entra se cruzam NO LUGAR e os símbolos que ficam se movem juntos; a igualdade
        # nunca fica incompleta (antes: "P_B = · v", "F = ∫ ▢ × B") durante a transformação
        todas = outs + moves + ins
        if todas:
            self.play(*todas, run_time=run, rate_func=smooth)
        self.cur = new
        return new''')

# limpa com animações extras na MESMA passada (troca cruzada: sem tela vazia entre dois blocos)
rep('''    def limpa(self, run=0.9, keep_extra=()):
        """Fecha o bloco anterior: tudo sai, menos marca, cabeçalho e o que for pedido (os relógios/trackers ficam)."""
        keep = (self.wm, self.tag) + tuple(keep_extra)
        mobs = [m for m in self.mobjects if m not in keep and not isinstance(m, ValueTracker)]
        dyn = [m for m in mobs if getattr(m, "dyn", False)]      # estrutura variável: não aceita FadeOut (sai direto)
        self.remove(*dyn)
        mobs = [m for m in mobs if m not in dyn]
        if mobs:
            self.play(*[FadeOut(m) for m in mobs], run_time=run)
        self.cur = {}''', '''    def limpa(self, run=0.9, keep_extra=(), extra_anims=()):
        """Fecha o bloco anterior: tudo sai, menos marca, cabeçalho e o que for pedido (os relógios/trackers ficam).
        `extra_anims` entram na MESMA passada (troca cruzada: o bloco novo já começa a aparecer enquanto o antigo sai)."""
        keep = (self.wm, self.tag) + tuple(keep_extra)
        mobs = [m for m in self.mobjects if m not in keep and not isinstance(m, ValueTracker)]
        dyn = [m for m in mobs if getattr(m, "dyn", False)]      # estrutura variável: não aceita FadeOut (sai direto)
        self.remove(*dyn)
        mobs = [m for m in mobs if m not in dyn]
        anims = [FadeOut(m) for m in mobs] + list(extra_anims)
        if anims:
            self.play(*anims, run_time=run)
        self.cur = {}''')

# ── 3 · K: hipóteses (uma vez), determinante sem "=" antes do resultado, substituição e soma de quadrados completas ─
rep('''        nvx = eq(r"v_x\\ \\text{ao longo de}\\ \\mathbf B\\ (\\odot)", size=28, colors={}).move_to([RX, -1.2, 0])
        self.play(FadeIn(nvx), run_time=0.7)
        self.hold(2.4)
''', '''        nvx = eq(r"v_x\\ \\text{ao longo de}\\ \\mathbf B\\ (\\odot)", size=28, colors={}).move_to([RX, -1.2, 0])
        self.play(FadeIn(nvx), run_time=0.7)
        # hipóteses da análise (uma vez, antes de qualquer conclusão sobre ω_c, R, T, rapidez e hélice)
        hip = VGroup(txt("hipóteses: B uniforme e constante,", 20, opacity=0.9),
                     txt("só a força magnética, regime não relativístico", 20, opacity=0.9)).arrange(DOWN, buff=0.08).move_to([RX, -2.25, 0])
        self.play(FadeIn(hip, shift=0.1 * UP), run_time=0.8)
        self.hold(2.8)
''')
rep('''self.play(FadeOut(l1), FadeOut(l2), FadeOut(cap1), FadeOut(nvx), FadeIn(ref1), FadeIn(mat), run_time=1.1)''',
    '''self.play(FadeOut(l1), FadeOut(l2), FadeOut(cap1), FadeOut(nvx), FadeOut(hip), FadeIn(ref1), FadeIn(mat), run_time=1.1)''')
rep('''FadeIn(t_j[4]), FadeIn(t_j[5]), FadeIn(t_j[6:8]),''', '''FadeIn(t_j[4]), FadeIn(t_j[5]), FadeIn(t_j[6]),''')
rep('''self.play(FadeIn(t_j[8]), FadeIn(t_j[9]), FadeIn(t_j[10]), FadeIn(t_j[11]),''', '''self.play(FadeIn(t_j[7]), FadeIn(t_j[8]), FadeIn(t_j[9]), FadeIn(t_j[10]), FadeIn(t_j[11]),''')
rep('''FadeIn(t_k[4]), FadeIn(t_k[5]), FadeIn(t_k[6:8]),''', '''FadeIn(t_k[4]), FadeIn(t_k[5]), FadeIn(t_k[6]),''')
rep('''self.play(FadeIn(t_k[8]), FadeIn(t_k[9]), FadeIn(t_k[10]), FadeIn(t_k[11]),''', '''self.play(FadeIn(t_k[7]), FadeIn(t_k[8]), FadeIn(t_k[9]), FadeIn(t_k[10]), FadeIn(t_k[11]),''')
rep('''        self.play(FadeOut(e1[3]), run_time=0.6)
        self.play(ReplacementTransform(e1[0:3], e2[0:3]), FadeIn(e2[3]), FadeIn(e2[6]), run_time=0.8)
        self.play(TransformFromCopy(cz_[2], e2[4]), TransformFromCopy(cz_[3], e2[5]), run_time=1.2)''',
    '''        # numa só passada: dv_z/dt sai enquanto o lado direito da 3ª equação entra (a igualdade nunca fica falsa nem incompleta)
        self.play(FadeOut(e1[3]), ReplacementTransform(e1[0:3], e2[0:3]), FadeIn(e2[3]), FadeIn(e2[6]),
                  TransformFromCopy(cz_[2], e2[4]), TransformFromCopy(cz_[3], e2[5]), run_time=1.9)''')
rep('''        self.play(FadeIn(sm[0]), FadeIn(sm[1]), FadeIn(sm[2]), FadeIn(sm[3]),''', '''        self.play(FadeIn(sm[0]), FadeIn(sm[1]), FadeIn(sm[2]),''')
rep('''        self.play(FadeIn(sm[4]), FadeIn(sm[5]),''', '''        self.play(FadeIn(sm[3]), FadeIn(sm[4]), FadeIn(sm[5]),''')

# ── 4 · B06: UMA fonte física (contadores de portadores que entram e saem) para Q_int, dQ/dt e portadores ─────
rep('''class YT0005MagnetostaticaM1(Scene):
''', '''class BalancoB06:
    """Balanço de carga do B06, UMA fonte física: A = portadores que entraram, B = portadores que saíram (contadores contínuos).
    dA/dt = R0·I_ent e dB/dt = R0·I_sai com R0 = N0·S_PHYS, logo  Q_int = (A − B)/N0 obedece EXATAMENTE a
    dQ_int/dt (físico) = I_ent − I_sai  (S_PHYS = segundos físicos por segundo de tela; câmera lenta).
    Cada portador k nasce na face de entrada quando A cruza k, atravessa e sai quando B cruza k; entre uma coisa e outra sua
    posição é a fração s = (A − k)/(A − B) (densidade uniforme): ninguém aparece nem some no interior."""

    def __init__(self, n0=24, s_phys=0.11, q0=1.0):
        self.n0, self.s_phys, self.q0 = n0, s_phys, q0
        self.r0 = n0 * s_phys / q0
        self.A, self.B = n0 + 0.5, 0.5

    def step(self, i_in, i_out, dt):
        self.A += self.r0 * i_in * dt
        self.B += self.r0 * i_out * dt

    def q(self):
        return self.q0 * (self.A - self.B) / self.n0

    def particles(self):
        n = max(self.A - self.B, 1e-6)
        return [(k, (self.A - k) / n) for k in range(int(math.floor(self.B)) + 1, int(math.floor(self.A)) + 1)]


class YT0005MagnetostaticaM1(Scene):
''')
rep('''        S_PHYS = 0.11                        # segundos físicos por segundo de tela: a lei física dQ/dt = I_ent − I_sai é mantida internamente
        self.Iin, self.Iout, self.Q = ValueTracker(1.0), ValueTracker(1.0), ValueTracker(1.0)
        self.Q.add_updater(lambda m, dt: m.set_value(min(1.9, max(0.15, m.get_value() + (self.Iin.get_value() - self.Iout.get_value()) * S_PHYS * dt))))
        self.add(self.Q)''', '''        self.Iin, self.Iout, self.Q = ValueTracker(1.0), ValueTracker(1.0), ValueTracker(1.0)
        mdl = BalancoB06()                   # câmera lenta: 1 s de tela = 0,11 s físico; Q_int, dQ/dt e portadores saem do MESMO balanço
        self.mdl = mdl

        def bal_step(m, dt):
            mdl.step(self.Iin.get_value(), self.Iout.get_value(), dt)
            m.set_value(mdl.q())

        self.Q.add_updater(bal_step)
        self.add(self.Q)''')
a = s.index("        # carga interna: portadores positivos efetivos que entram, atravessam e saem.")
b = s.index("        self.qd = always_redraw(dots)")
s = s[:a] + '''        # carga interna: portadores positivos efetivos que entram, atravessam e saem (posições vêm do balanço único `mdl`)
        rng = np.random.RandomState(11)
        YZ = [(0.3 + (H_ - 0.6) * rng.rand(), 0.3 + (D_ - 0.6) * rng.rand()) for _ in range(1024)]

        def dots():
            g = VGroup()
            gq = self.gq.get_value()
            if gq < 0.02:
                return g
            s = self.vsc.get_value()
            for k, sf in mdl.particles():
                x = W_ * sf
                y, z = YZ[k % 1024]
                op = min(1.0, x / 0.35, (W_ - x) / 0.35) * gq
                if op > 0.02:
                    g.add(Dot(pm(x, y, z), radius=0.075 * s, color=BLUE_L).set_opacity(op * (1.0 - 0.35 * z / D_)))
            return g.set_z_index(3)

''' + s[b:]
rep('''        self.play(FadeIn(rp), FadeIn(self.reads), run_time=0.8)''', '''        slow = txt("câmera lenta: 1 s de tela = 0,11 s", 15, opacity=0.55).move_to([4.1, -1.0, 0])
        self.slow_note = slow
        self.play(FadeIn(rp), FadeIn(self.reads), FadeIn(slow), run_time=0.8)''')
rep('''        self.play(FadeOut(self.reads), FadeOut(rp), run_time=0.6)''', '''        self.play(FadeOut(self.reads), FadeOut(rp), FadeOut(self.slow_note), run_time=0.6)''')

# ── 5 · transições sem tela vazia ───────────────────────────────────────────────────────────────────────────────
# B04 → B05: o esquema de energia sai enquanto o fio entra (troca cruzada)
rep('''    def b05_muitas_cargas(self):
        self.seg("F")
        self.limpa()
        WY = 1.5''', '''    def b05_muitas_cargas(self):
        self.seg("F")
        WY = 1.5''')
rep('''        self.play(FadeIn(self.wire5), self.g5.animate.set_value(1.0), run_time=1.2)''',
    '''        self.limpa(1.2, keep_extra=(self.car5,), extra_anims=(FadeIn(self.wire5), self.g5.animate.set_value(1.0)))   # troca cruzada''')
# B05 → B06: o prisma de J vira referência e se dissolve enquanto o fluxo do volume entra
rep('''        self.prism = always_redraw(prism)
        right = np.array([4.4, 0.0, 0.0])''', '''        self.pgate = ValueTracker(1.0)

        def prism_g():
            g = prism()
            k = self.pgate.get_value()
            if k < 0.999:
                for sm in g.family_members_with_points():
                    sm.set_stroke(opacity=sm.get_stroke_opacity() * k)
                    sm.set_fill(opacity=sm.get_fill_opacity() * k)
            return g

        self.prism = always_redraw(prism_g)
        right = np.array([4.4, 0.0, 0.0])''')
rep('''        self.seg("G")
        self.limpa()
''', '''        self.seg("G")
        self.limpa(0.8, keep_extra=(self.prism,))          # o prisma de J fica como referência até o fluxo do volume entrar
''')
rep('''        self.play(self.gj.animate.set_value(1.0), FadeIn(jl), run_time=1.4)
        self.hold(1.6)''', '''        self.play(self.gj.animate.set_value(1.0), FadeIn(jl), self.pgate.animate.set_value(0.0), run_time=1.4)
        self.remove(self.prism)
        self.hold(1.6)''')
# B06 → B07: o volume com J vira referência e se dissolve enquanto o aparato entra
rep('''        self.seg("H")
        self.cores_novas = True
        self.limpa(0.8)
        # estado do aparato: UMA variável física v controla gráfico, valor de F_y/q e deflexão do feixe
        self.vth, self.qs7 = ValueTracker(0.6), ValueTracker(1.0)
        self.asc, self.aox, self.aoy = ValueTracker(1.0), ValueTracker(-3.0), ValueTracker(0.35)   # aparato ~58% esquerdo, fixo em todo o B07/B08
        self.pop, self.eop = ValueTracker(0.0), ValueTracker(0.0)          # opacidade das placas / das setas de E
        self.mode7 = "cross"
        self.ph7 = ValueTracker(0.0)
        self.ph7.add_updater(lambda m, dt: m.increment_value(dt * self.vth.get_value() / (E7 / B7)))     # avanço do pulso ∝ v (mesma variável do gráfico)
        self.add(self.ph7)
        self.b07_montar_aparato()
        self.b07_aparato()''', '''        self.seg("H")
        self.cores_novas = True
        # estado do aparato: UMA variável física v controla gráfico, valor de F_y/q e deflexão do feixe
        self.vth, self.qs7 = ValueTracker(0.6), ValueTracker(1.0)
        self.asc, self.aox, self.aoy = ValueTracker(1.0), ValueTracker(-3.0), ValueTracker(0.35)   # aparato ~58% esquerdo, fixo em todo o B07/B08
        self.pop, self.eop = ValueTracker(0.0), ValueTracker(0.0)          # opacidade das placas / das setas de E
        self.bop7 = ValueTracker(0.0)                                      # opacidade dos símbolos de B do aparato
        self.mode7 = "cross"
        self.ph7 = ValueTracker(0.0)
        self.ph7.add_updater(lambda m, dt: m.increment_value(dt * self.vth.get_value() / (E7 / B7)))     # avanço do pulso ∝ v (mesma variável do gráfico)
        self.add(self.ph7)
        self.b07_montar_aparato()
        self.add(*self.ap_mobs)
        # troca cruzada: o volume de J (B06) se dissolve enquanto o feixe e o campo B do aparato entram; sem tela vazia
        self.limpa(1.2, keep_extra=tuple(self.ap_mobs) + (self.jf, self.vol, self.qd),
                   extra_anims=(self.gj.animate.set_value(0.0), self.gbox.animate.set_value(0.0), self.gq.animate.set_value(0.0),
                                FadeIn(self.beam_t), FadeIn(self.beam_p), FadeIn(self.detec), self.bop7.animate.set_value(1.0)))
        self.remove(self.jf, self.vol, self.qd)
        self.b07_aparato()''')
rep('''        self.add(*self.ap_mobs)
        self.play(FadeIn(self.beam_t), FadeIn(self.beam_p), FadeIn(self.detec), run_time=1.2)
        # eixos e v''', '''        # (feixe, detector e B já entraram na troca cruzada do início do bloco)
        # eixos e v''')
rep('''                    g.add(Circle(radius=0.075 * self.asc.get_value(), color=MAG, stroke_width=2).set_opacity(0.45).move_to(c),
                          Dot(c, radius=0.025, color=MAG).set_opacity(0.45))''', '''                    g.add(Circle(radius=0.075 * self.asc.get_value(), color=MAG, stroke_width=2).set_opacity(0.45 * self.bop7.get_value()).move_to(c),
                          Dot(c, radius=0.025, color=MAG).set_opacity(0.45 * self.bop7.get_value()))''')

# ── 6 · síntese: a legenda anterior sai ANTES da nova (sem texto sobre texto) ─────────────────────────────────────
rep('''        self.play(FadeOut(VGroup(wire, cars, arr, il)), g9.animate.set_value(1.0), FadeIn(jl), FadeOut(t3), FadeIn(t4), run_time=1.4)''',
    '''        self.play(FadeOut(t3), run_time=0.4)
        self.play(FadeOut(VGroup(wire, cars, arr, il)), g9.animate.set_value(1.0), FadeIn(jl), run_time=1.0)
        self.play(FadeIn(t4), run_time=0.7)''')

open(dst, "w", encoding="utf-8").write(s)
print("falhas:", len(fails))
for f in fails:
    print(" -", f)

from pathlib import Path
p = Path(__file__).resolve().parents[1] / 'cena.py'
s = p.read_text(encoding='utf-8')


def R(a, b):
    global s
    assert s.count(a) == 1, (s.count(a), a[:90])
    s = s.replace(a, b)


def cut(i0, i1, novo):
    """substitui o trecho entre as duas âncoras (i1 exclusivo)"""
    global s
    i, j = s.index(i0), s.index(i1)
    assert i < j, (i0[:50], i1[:50])
    s = s[:i] + novo + s[j:]


for k in ('-5.3', '-5.2'):
    s = s.replace(f'self.off = {k}', 'self.off = 0.')
# ---- C01
cut("        self.jogar(.3, FadeIn(self.selos), FadeIn(av), run_time=.5)", "        self.jogar(6.0, FadeOut(eqq)",
    "        self.jogar(.1, FadeIn(self.selos), FadeIn(av), FadeIn(eqq), run_time=.7)\n        self.jogar(6.1, FadeIn(pre), run_time=.5)\n")
R("        self.jogar(6.0, FadeOut(eqq), FadeOut(pre), FadeOut(self.selos), FadeOut(av), run_time=.5)\n        sl = self.chip(6.8, 'só com moléculas batendo na parede', ICE)\n        self.jogar(10.0, FadeOut(sl), run_time=.4)",
  "        self.jogar(7.2, FadeOut(eqq), FadeOut(pre), FadeOut(self.selos), FadeOut(av), run_time=.45)\n        sl = self.chip(7.9, 'só com moléculas batendo na parede', ICE)\n        self.jogar(10.3, FadeOut(sl), run_time=.3)")
# ---- C02
R("            return float(np.clip((t - 14.3) / .8, 0, 1) * np.clip((75.4 - t) / .5, 0, 1))", "            return float(np.clip((t - 16.2) / .8, 0, 1) * np.clip((70.9 - t) / .5, 0, 1))")
cut("        self.jogar(17.9, FadeIn(g_m), Create(lin_m), run_time=.6)", "        # antes e depois da batida", """        # p = m vₓ: a equação nasce em "o momento"; m e vₓ viajam dos rótulos quando a fala os nomeia
        e1 = MT(c(MOM, 'p'), '=', m_, vx_, size=ACT_FS)
        self.passo('p=mv')
        self.act_write(15.33, e1, ocultas=(2, 3), run=.5)
        self.jogar(16.27, FadeIn(g_m), Create(lin_m), run_time=.4)
        self.apres['m'] = self.nq / FPS
        self.jogar(17.0, FadeIn(g_v), Create(lin_v), run_time=.4)
        self.apres['v_x'] = self.nq / FPS
        for lin in (lin_m, lin_v):
            lin.clear_updaters()
        cps = []
        for fonte, alvo in ((sim_m, e1[2]), (sim_v, e1[3])):
            cp = fonte.copy()
            cp._qa = None
            self.add(cp)
            cps.append((cp, alvo.copy().set_opacity(1)))
        self.jogar(17.45, *[Transform(cp, tg) for cp, tg in cps], FadeOut(VGroup(g_m, lin_m, g_v, lin_v)), run_time=.4)
        e1[2].set_opacity(1)
        e1[3].set_opacity(1)
        for cp, _ in cps:
            self.remove(cp)
""")
cut("        self.act_to_fix(34.4)\n        j1 =", "    # ══ C03", """        self.act_to_fix(28.8)
        j1 = MT(JJ + '=+2' + m_ + vx_, size=ACT_FS)
        yc = self.pt('parede', qb + 14)[1]
        a_mol = seta(np.array([-2.7, yc, 0.]), np.array([-3.6, yc, 0.]), ICE, 6.)
        a_par = seta(np.array([2.7, yc, 0.]), np.array([3.6, yc, 0.]), ICE, 10.)
        guia = tracejada(np.array([-2.65, yc, 0.]), np.array([2.65, yc, 0.]), ICE, 1.6, .3)
        guia._guia = True
        l_mol = MT(c(IMP, r'-2mv_x'), size=30).move_to([-3.15, yc + .45, 0])
        l_par = MT(c(IMP, r'+2m|v_x|'), size=30).move_to([3.2, yc + .45, 0])
        l_mol._fora = l_par._fora = True
        glow = traco(a_par.copy().set_stroke(ICE, 20, .22))
        self.jogar(29.9, GrowArrow(a_mol), GrowArrow(a_par), Create(guia), FadeIn(glow), FadeIn(l_mol), FadeIn(l_par), run_time=.7)
        self.passo('J')
        self.act_write(30.6, j1, run=.5)
        self.contorno(33.15, 'A', ICE)
        self.jogar(33.55, FadeOut(VGroup(a_mol, a_par, guia, l_mol, l_par, glow)), run_time=.45)
        self.act_to_fix(34.05)

""")
# ---- C03
cut("        self.jogar(40.0, FadeIn(g_L), Create(lin_L), run_time=.6)", "        # Δt = (L + L)/vₓ → 2L/vₓ", """        self.jogar(37.1, Create(rl1), FadeIn(lL1), run_time=.4)
        self.jogar(37.5, Create(rl2), FadeIn(lL2), run_time=.4)
        self.jogar(37.92, FadeIn(g_L), Create(lin_L), run_time=.4)
        self.apres['L'] = self.nq / FPS
        self.g_i = self.rotulo('molécula i', 'v_{x,i}', VEL, 3.25, 3.6, lambda: clamp_pt(self.pt('tx'), .2), 'D')
""")
cut("        self.jogar(57.0, FadeIn(g_A), Create(lin_A), run_time=.6)", "        self.act_troca(60.4, p2", """        self.passo('P1=F/A')
        self.act_write(50.55, p1, ocultas=(4,), run=.5)
        self.jogar(51.88, FadeIn(g_A), Create(lin_A), run_time=.4)
        self.apres['A'] = self.nq / FPS
        self.passo('A')
        self.voa(52.3, sim_A, p1[4], run=.4)
        self.passo('P1=(mv2/L)/L2')
""")
R("        self.act_troca(60.4, p2, 'seq', run=.9)", "        self.act_troca(53.3, p2, 'seq', run=.9)")
cut("        self.passo('L3')\n        self.act_troca(62.2, p3, 'seq', run=.9)", "        self.act_troca(66.2, p5", """        self.passo('L3')
        self.act_troca(54.85, p3, 'seq', run=.9)
        self.jogar(55.66, FadeIn(g_V), Create(lin_V), run_time=.35)
        self.apres['V'] = self.nq / FPS
        self.passo('L3=V')
        p4[5].set_opacity(0)
        self.act_troca(56.05, p4, 'seq', run=.9)
        p4[5].set_opacity(0)
        self.voa(56.75, sim_V, p4[5], run=.4)
        self.passo('P1V')
""")
R("        self.act_troca(66.2, p5, 'tmt', run=1.0)\n        self.contorno(67.4, 'A', '#' + PC)", "        self.act_troca(60.4, p5, 'tmt', run=.8)\n        self.contorno(61.25, 'A', '#' + PC)")
R("        self.jogar(68.4, FadeOut(VGroup(rl1, rl2, lL1, lL2, g_L, lin_L, g_A, lin_A, g_V, lin_V)), run_time=.5)\n        self.act_to_fix(69.2)",
  "        self.act_to_fix(61.65, extra=[FadeOut(VGroup(rl1, rl2, lL1, lL2, g_L, lin_L, g_A, lin_A, g_V, lin_V)), FadeIn(self.g_i[0]), Create(self.g_i[2])])")
# ---- C04
R("        tipo = lambda k: clamp_pt(self.pt(k), .2)\n        g_i, sim_i, lin_i = self.rotulo('molécula i', 'v_{x,i}', VEL, 3.25, 3.6, lambda: tipo('tx'), 'D')\n        self.jogar(71.2, FadeIn(g_i), Create(lin_i), run_time=.6)",
  "        g_i, sim_i, lin_i = self.g_i")
R("        self.jogar(79.2, FadeOut(g_i), FadeOut(lin_i), run_time=.4)\n", "")
R("        self.act_to_fix(79.5, run=.8, extra=[FadeIn(cub)])", "        self.act_to_fix(70.5, run=.8, extra=[FadeIn(cub), FadeOut(g_i), FadeOut(lin_i)])")
R("        self.jogar(109.0, FadeOut(VGroup(bars, rotb, linha, pilha, l_v2, l_13)), run_time=.4)       # as barras ficam até a linha final\n        self.act_to_fix(109.8)",
  "        self.act_to_fix(97.4, extra=[FadeOut(VGroup(bars, rotb, linha, pilha, l_v2, l_13))])       # as barras ficam até a linha final")
R("            self.play(ReplacementTransform(bars, novo), run_time=.55)", "            self.play(ReplacementTransform(bars, novo), run_time=.42)")
R("            tt += .75", "            tt += .5")
# ---- C05
R("        self.limpa(135.0, 'AF', run=.5, extra=", "        self.limpa(121.28, 'AF', run=.3, extra=")
R("        self.contorno(140.2, 'F', '#' + PC)\n        self.passo('2/3NEc=NkBT')\n        self.act_write(140.8, q1, run=1.0)", "        self.contorno(127.8, 'F', '#' + PC)\n        self.passo('2/3NEc=NkBT')\n        self.act_write(128.2, q1, run=.5)")
# ---- C06
R("        self.ate(150.4)\n        self._flush()\n        self.trans.append(150.4 + self.off)", "        self.ate(138.2)\n        self._flush()\n        self.trans.append(138.2 + self.off)")
R("auto_fade=True), run_time=1.6)\n        self.Fx = dict(eq=C", "auto_fade=True), run_time=.9)\n        self.Fx = dict(eq=C")
R("        self.limpa(157.7, 'A', run=.5)\n        self.jogar(158.3, D.animate.scale(1.75).move_to([0, -1.0, 0]), run_time=.9)\n", "        self.limpa(148.5, 'A', run=.5, extra=[D.animate.scale(1.75).move_to([0, -1.0, 0])])\n")
R("        self.jogar(159.5, FadeIn(r), run_time=.4)", "        self.jogar(149.05, FadeIn(r), run_time=.35)")
# ---- C07 inteira
cut("    def c07(self):", "    # ══ CTA", """    def c07(self):
        self.off = 0.
        sel = T('temperatura constante', 26, ICE).move_to([0, Y_CHIP, 0])
        et1 = T('estado 1 · V', 30, DIM).move_to([0, -.75, 0])
        et2 = T('estado 2 · V/2', 30, DIM).move_to([0, -.75, 0])
        W = RT.PIST['W']
        nA, nB = TL['cont_estado1'], TL['cont_estado2']                 # valores medidos (qa/contadores.txt), texto fixo
        numA = tabnum(str(nA), 100).move_to([0, -2.0, 0])
        numB = tabnum(str(nB), 100).move_to([-.55, -2.0, 0])
        dobro = MT(r'\\times2', size=72).move_to([1.05, -2.0, 0])
        leg = T(f'batidas na parede em {str(W).replace(".", ",")} s', 26, DIM).move_to([0, -3.15, 0])
        self.jogar(149.5, FadeOut(self.Fx['eq']), FadeOut(self.Fx['out']), FadeIn(et1), FadeIn(numA), FadeIn(leg), run_time=.5)
        self.Fx = None
        self.jogar(152.1, FadeOut(et1), FadeOut(numA), FadeIn(et2), FadeIn(numB), run_time=.4)
        self.jogar(153.55, FadeIn(dobro), run_time=.3)
        self.jogar(155.3, FadeIn(sel), run_time=.4)
        r2x = MT(c(PC, r'P') + c(GEO, 'V') + r'=\\mathrm{const.}\\ \\Rightarrow\\ ' + c(GEO, r'V/2') + r'\\Rightarrow ' + c(PC, r'2P'), size=52).move_to([0, -4.0, 0])
        self.jogar(156.75, FadeIn(r2x), run_time=.5)
        self.jogar(159.3, FadeOut(VGroup(et2, numB, dobro, leg, r2x, sel)), run_time=.4)
        n517 = MT(c(VEL, r'517\\ \\mathrm{m/s}'), size=100).move_to([0, -3.6, 0])
        out517 = SurroundingRectangle(n517, color=VIOLET, buff=.3, corner_radius=.2, stroke_width=2.5).set_z_index(35)
        sub = T('nitrogênio · 300 K', 28, TEXT_COLOR).move_to([0, -1.5, 0])
        rot = T('velocidade quadrática média', 28, VIOLET).move_to([0, -2.25, 0])
        self.jogar(161.35, FadeIn(sub), run_time=.4)
        self.jogar(163.4, FadeIn(rot), run_time=.4)
        self.jogar(165.35, FadeIn(n517), FadeIn(out517), run_time=.5)
        self.c07_obj = VGroup(n517, out517, sub, rot)

""")
p.write_text(s, encoding='utf-8')
print('A ok')

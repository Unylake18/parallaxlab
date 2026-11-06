from pathlib import Path
p = Path(__file__).resolve().parents[1] / 'cena.py'
s = p.read_text(encoding='utf-8')
PARES = [
    # C02
    ("self.act_troca(24.0, ea, 'seq', run=.9)", "self.act_troca(17.92, ea, 'seq', run=.9)"),
    ("self.act_troca(27.0, eb, 'gm', glifos=[(list(range(6)), list(range(6)))], run=1.0)", "self.act_troca(22.5, eb, 'gm', glifos=[(list(range(6)), list(range(6)))], run=1.0)"),
    ("self.act_to_fix(29.2)", "self.act_to_fix(23.8)"),
    ("self.act_write(30.0, s1, run=.8)", "self.act_write(24.66, s1, run=.55)"),
    ("self.act_troca(31.4, s2, 'seq', run=.9)", "self.act_troca(25.3, s2, 'seq', run=.9)"),
    ("self.act_troca(32.8, s3, 'seq', run=.9)", "self.act_troca(26.62, s3, 'seq', run=.9)"),
    # C03
    ("self.act_write(43.6, d1, ocultas=(2, 4), run=.6)", "self.act_write(38.78, d1, ocultas=(2, 4), run=.4)"),
    ("self.voa(44.4, lL1, d1[2])", "self.voa(39.3, lL1, d1[2], run=.4)"),
    ("self.voa(45.0, lL2, d1[4])", "self.voa(39.75, lL2, d1[4], run=.4)"),
    ("self.act_troca(46.4, d2, 'seq', run=.9)", "self.act_troca(41.2, d2, 'seq', run=.9)"),
    ("self.act_to_fix(47.9, novo=comb, run=.8)", "self.act_to_fix(42.75, novo=comb, run=.8)"),
    ("self.act_write(49.0, f1, run=.8)", "self.act_write(43.78, f1, run=.5)"),
    ("self.act_troca(51.2, F2, 'seq', run=.9)", "self.act_troca(44.45, F2, 'seq', run=.9)"),
    ("self.jogar(53.4, FadeOut(F2[0][3]), FadeOut(F2[0][8]), run_time=.7)", "self.jogar(45.74, FadeOut(F2[0][3]), FadeOut(F2[0][8]), run_time=.6)"),
    ("self.act_troca(54.5, F3, 'seq', run=.9)", "self.act_troca(46.9, F3, 'seq', run=.9)"),
    ("self.act_to_fix(56.0)\n", "self.act_to_fix(49.7)\n"),
    # C04
    ("self.act_write(72.6, sm1, run=.9)", "self.act_write(62.82, sm1, run=.5)"),
    ("self.act_troca(75.0, sm2, 'tmt', run=.9)", "self.act_troca(64.35, sm2, 'tmt', run=.9)"),
    ("self.act_troca(77.0, sm3, 'seq', run=1.0)", "self.act_troca(67.55, sm3, 'seq', run=.9)"),
    ("self.fix_troca(78.2, defn, run=1.0)", "self.fix_troca(69.1, defn, run=.8)"),
    ("self.jogar(81.2, GrowArrow(vt), FadeIn(l_v), run_time=.6)", "self.jogar(71.5, GrowArrow(vt), FadeIn(l_v), run_time=.5)"),
    ("self.jogar(82.2, GrowArrow(vx_a), FadeIn(l_x), GrowArrow(vy_a), FadeIn(l_y), GrowArrow(vz_a), FadeIn(l_z), run_time=.8)", "self.jogar(72.3, GrowArrow(vx_a), FadeIn(l_x), GrowArrow(vy_a), FadeIn(l_y), GrowArrow(vz_a), FadeIn(l_z), run_time=.6)"),
    ("self.act_write(84.6, pi1, run=1.0)", "self.act_write(73.05, pi1, run=.5)"),
    ("self.act_troca(86.6, pi2, 'seq', run=1.0)", "self.act_troca(77.0, pi2, 'seq', run=.9)"),
    ("self.jogar(87.6, FadeOut(diag1), *[FadeIn(g) for g in grupos], run_time=.5)", "self.jogar(78.0, FadeOut(diag1), *[FadeIn(g) for g in grupos], run_time=.5)"),
    ("self.jogar(91.0, FadeOut(VGroup(*grupos)), FadeIn(bars), FadeIn(rotb), Create(linha), run_time=.45)", "self.jogar(81.25, FadeOut(VGroup(*grupos)), FadeIn(bars), FadeIn(rotb), Create(linha), run_time=.45)"),
    ("self.jogar(91.5, FadeIn(cnt), run_time=.3)", "self.jogar(81.7, FadeIn(cnt), run_time=.25)"),
    ("tt = 92.3", "tt = 81.95"),
    ("self.act_troca(96.0, ig, 'seq', run=.9)", "self.act_troca(84.48, ig, 'seq', run=.9)"),
    ("self.jogar(97.0, FadeOut(cnt), run_time=.3)", "self.jogar(85.2, FadeOut(cnt), run_time=.25)"),
    ("self.act_troca(97.4, d1, 'seq', run=.9)", "self.act_troca(86.08, d1, 'seq', run=.9)"),
    ("self.jogar(98.6, FadeIn(pilha, shift=UP * .15), FadeIn(l_v2), FadeIn(l_13), run_time=.6)", "self.jogar(88.95, FadeIn(pilha, shift=UP * .15), FadeIn(l_v2), FadeIn(l_13), run_time=.5)"),
    ("self.act_troca(99.8, d2, 'gm', glifos=gm, run=1.6)", "self.act_troca(89.5, d2, 'gm', glifos=gm, run=1.0)"),
    ("self.act_to_fix(102.3)", "self.act_to_fix(90.52)"),
    ("self.act_write(103.2, sb0, run=.8)", "self.act_write(91.3, sb0, run=.4)"),
    ("self.act_troca(104.6, sb1, 'seq', run=.9)", "self.act_troca(92.7, sb1, 'seq', run=.9)"),
    ("self.act_troca(106.2, sb2, 'seq', run=1.0)", "self.act_troca(95.5, sb2, 'seq', run=.9)"),
    ("self.contorno(108.5, 'A', VIOLET)", "self.contorno(96.95, 'A', VIOLET)"),
    # C05
    ("self.act_write(112.2, ec1, run=1.0)", "self.act_write(98.84, ec1, run=.5)"),
    ("self.act_troca(114.4, ec2, 'seq', run=.9)", "self.act_troca(101.45, ec2, 'seq', run=.9)"),
    ("self.limpa(116.0, 'F', run=.3)", "self.limpa(102.45, 'F', run=.25)"),
    ("self.act_troca(116.4, sb, 'seq', run=.9)", "self.act_troca(102.72, sb, 'seq', run=.9)"),
    ("self.act_troca(118.4, sc, 'tmt', run=1.2)", "self.act_troca(104.5, sc, 'tmt', run=.9)"),
    ("self.contorno(120.2, 'A', CYAN)", "self.contorno(108.0, 'A', CYAN)"),
    ("self.act_to_fix(121.4)\n", "self.act_to_fix(108.4)\n"),
    ("self.jogar(122.2, Create(ax), FadeIn(lx), FadeIn(ly), FadeIn(sel), run_time=.9)", "self.jogar(112.45, Create(ax), FadeIn(lx), FadeIn(ly), FadeIn(sel), run_time=.8)"),
    ("self.jogar(124.4, FadeIn(p0), FadeIn(t0), run_time=.5)", "self.jogar(113.74, FadeIn(p0), FadeIn(t0), run_time=.4)"),
    ("self.jogar(126.2, FadeIn(p1), FadeIn(t1), run_time=.5)", "self.jogar(114.2, FadeIn(p1), FadeIn(t1), run_time=.4)"),
    ("self.jogar(127.6, Create(reta), run_time=.7)", "self.jogar(114.9, Create(reta), run_time=.5)"),
    ("self.fix_troca(128.8, ta, run=1.0)", "self.fix_troca(116.2, ta, run=.8)"),
    ("self.act_write(130.4, tb, run=1.2)", "self.act_write(119.45, tb, run=.6)"),
    ("self.jogar(133.4, FadeIn(kb), run_time=.5)", "self.jogar(120.95, FadeIn(kb), run_time=.3)"),
    ("self.act_write(135.8, pk, run=1.0)", "self.act_write(121.6, pk, run=.4)"),
    ("self.contorno(137.2, 'A', '#' + PC)", "self.contorno(126.6, 'A', '#' + PC)"),
    ("self.act_to_fix(139.2, novo=", "self.act_to_fix(127.0, novo="),
    ("self.act_troca(142.8, q2, 'gm', glifos=gf, run=1.6)", "self.act_troca(129.45, q2, 'gm', glifos=gf, run=1.0)"),
    ("self.contorno(145.0, 'A', CYAN)", "self.contorno(134.1, 'A', CYAN)"),
    # C06
    ("self.limpa(147.6, 'A', run=.4)", "self.limpa(134.55, 'A', run=.25)"),
    ("self.act_write(148.2, h1, run=1.0)", "self.act_write(135.65, h1, run=.5)"),
    ("self.act_troca(152.4, h2, 'seq', run=.9)", "self.act_troca(139.15, h2, 'seq', run=.9)"),
    ("self.act_troca(154.2, h3, 'seq', run=1.0)", "self.act_troca(141.5, h3, 'seq', run=.9)"),
    ("self.fix_troca(155.9, D, run=1.0)", "self.fix_troca(143.55, D, run=.8)"),
]
for a, b in PARES:
    assert s.count(a) == 1, (s.count(a), a)
    s = s.replace(a, b)
p.write_text(s, encoding='utf-8')
print('B ok', len(PARES))

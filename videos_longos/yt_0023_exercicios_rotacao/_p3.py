P = 'sec_e1a.py'
s = open(P, encoding='utf-8').read()


def rep(a, b):
    global s
    assert s.count(a) == 1, (s.count(a), a[:80])
    s = s.replace(a, b)


rep('"BLOCO": (-60.0, 12.0, 5.2, -3.85, 0.95, 0.0, -0.45)}', '"BLOCO": (-60.0, 12.0, 4.4, -3.85, 0.35, 0.0, -0.22)}')
rep('self.plano_v("E1-3 CORTE", -18.0, 8.0, 5.4, -3.85, 0.95,', 'self.plano_v("E1-3 CORTE", -36.0, 10.0, 5.6, -3.85, 0.95,')
rep('lbl(r"D=0{,}25\\ \\mathrm{m}", GEO, 40), lado=UP, d=1.1)', 'lbl(r"D=0{,}25\\ \\mathrm{m}", GEO, 40), lado=UP, d=1.6)')
rep('LEFT + 0.6 * DOWN, 2.6)\n        self.play(FadeIn(cota), FadeIn(dk_)', 'DOWN + 0.25 * LEFT, 1.9)\n        self.play(FadeIn(cota), FadeIn(dk_)')
rep('vt["K"].animate.set_value(4.8), vt["yc"].animate.set_value(1.1), vt["th"].animate.set_value(0.0), run_time=1.6)',
    'vt["K"].animate.set_value(5.1), vt["yc"].animate.set_value(1.0), vt["th"].animate.set_value(0.0), vt["wov"].animate.set_value(0.0), run_time=1.6)')
rep('LEFT + 0.2 * DOWN, 2.7)       # v2 §5 #7', 'LEFT + 0.2 * DOWN, 2.3)       # v2 §5 #7')
open(P, 'w', encoding='utf-8').write(s)
print('ok')

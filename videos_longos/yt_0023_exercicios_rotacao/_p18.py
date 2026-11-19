def edit(P, pares):
    s = open(P, encoding='utf-8').read()
    for a, b in pares:
        assert s.count(a) == 1, (P, s.count(a), a[:110])
        s = s.replace(a, b)
    open(P, 'w', encoding='utf-8').write(s)
edit('sec_e3.py', [
    ('from sec_e1a import chamada\n', 'from sec_e1a import chamada, chamada_em\n'),
    ('K0, Y0 = 5.2, 0.7\n', 'K0, Y0 = 5.2, 0.7\nK3, Y3 = 6.4, 1.15          # v5 §1.2: frontal do carretel ≥ 50% da altura útil (Rg = 1,96 u); os blocos pendem comprimidos (comp) para caber\n'),
    ('        exc, ff1, ff2 = ValueTracker(0.0), ValueTracker(0.0), ValueTracker(0.0)\n', '        exc, ff1, ff2 = ValueTracker(0.0), ValueTracker(0.0), ValueTracker(0.0)\n        comp = ValueTracker(1.0)        # 1 = pendura como no 3D; < 1 = o esquema 2.5D encurta o fio (E3-3 a E3-7)\n'),
    ('self.add(tc, th_x, ucam, Kc, ycc, trava, flash, m2, wov, maz, mel, mK, mxc, myc, max_, maz_, exc, ff1, ff2)', 'self.add(tc, th_x, ucam, Kc, ycc, trava, flash, m2, wov, maz, mel, mK, mxc, myc, max_, maz_, exc, ff1, ff2, comp)'),
    ('''        pb1 = lambda dz=0.0: pr(cam(), (XB1, YG, Z1 - RC * thv() + dz))
        pb2 = lambda dz=0.0: pr(cam(), (XB2, YP, Z2 + rc * thv() + dz))''', '''        def _comp(p, ta):
            c_ = comp.get_value()
            return p if c_ >= 0.9999 else np.array([p[0], ta[1] + c_ * (p[1] - ta[1]), 0.0])
        pb1 = lambda dz=0.0: _comp(pr(cam(), (XB1, YG, Z1 - RC * thv() + dz)), pr(cam(), (XB1, YG, 0.0)))
        pb2 = lambda dz=0.0: _comp(pr(cam(), (XB2, YP, Z2 + rc * thv() + dz)), pr(cam(), (XB2, YP, 0.0)))'''),
    ('''lbl(r"R=0{,}30\ \mathrm{m}", GEO, 40), RIGHT + 0.35 * UP, 2.6)
        cr = chamada(pr(c, (-0.07, YP - 0.05, 0.07)), lbl(r"r=0{,}10\ \mathrm{m}", GEO, 40), 0.75 * LEFT + UP, 1.7)''', '''lbl(r"R=0{,}30\ \mathrm{m}", C_RAIO, 40), RIGHT + 0.35 * UP, 2.6, cor=C_RAIO)
        cr = chamada(pr(c, (-0.07, YP - 0.05, 0.07)), lbl(r"r=0{,}10\ \mathrm{m}", C_RAIO_MENOR, 40), 0.75 * LEFT + UP, 1.7, cor=C_RAIO_MENOR)'''),
    ('        self.play(ucam.animate.set_value(1.0), run_time=3.0, rate_func=smooth)\n', '        self.play(ucam.animate.set_value(1.0), Kc.animate.set_value(K3), ycc.animate.set_value(Y3), run_time=3.0, rate_func=smooth)\n'),
    ('''        p1, p2 = pb1(), pb2()
        q1, q2 = pb1(0.056), pb2(0.4 * L2())
        print("[cam] E3-3 FRONTAL-FÍSICA", flush=True)''', '''        print("[cam] E3-3 FRONTAL-FÍSICA", flush=True)'''),
    ('''        self.play(f3.op.animate.set_value(0.0), run_time=0.4)
        cR3 = cota23(o_, t1, lbl(r"R=0{,}30\ \mathrm{m}", C_RAIO, 40), lado=UP, d=1.5, cor=C_RAIO)
        cr3 = cota23(o_, t2, lbl(r"r=0{,}10\ \mathrm{m}", C_RAIO_MENOR, 40), lado=UP + LEFT, d=1.3, cor=C_RAIO_MENOR)''', '''        self.play(f3.op.animate.set_value(0.0), comp.animate.set_value(0.7), run_time=0.8)       # match cut 3D → 2.5D; o fio encurta para o carretel crescer
        p1, p2 = pb1(), pb2()
        q1, q2 = pb1(0.056), pb2(0.4 * L2())
        cR3 = VGroup(linha_halo(o_, t1, cor=C_RAIO, w=4.5), chamada_em(t1, lbl(r"R=0{,}30\ \mathrm{m}", C_RAIO, 34), P3(-0.62, 2.5), cor=C_RAIO))
        cr3 = VGroup(linha_halo(o_, t2, cor=C_RAIO_MENOR, w=4.5), chamada_em(t2, lbl(r"r=0{,}10\ \mathrm{m}", C_RAIO_MENOR, 34), P3(-6.6, 2.9), cor=C_RAIO_MENOR))'''),
    ('a_c1 = arco_torque(o_, r=1.95, sentido=-1, a0=1.2, amp=1.1, cor=FC)', 'a_c1 = arco_torque(o_, r=Rg25 + 0.3, sentido=-1, a0=0.95, amp=0.85, cor=FC)'),
    ('l_c2 = chamada(t2 + 0.5 * DOWN, lbl("T_2", FC, 40), LEFT + 0.3 * DOWN, 2.45, cor=FC)', 'l_c2 = chamada_em(t2 + 0.5 * DOWN, lbl("T_2", FC, 40), P3(-6.9, 0.45), cor=FC)'),
    ('a_c2 = arco_torque(o_, r=0.8, sentido=1, a0=1.9, amp=1.2, cor=FC, w=5)', 'a_c2 = arco_torque(o_, r=Rp25 * 1.5, sentido=1, a0=1.9, amp=1.2, cor=FC, w=5)'),
    ('.arrange(DOWN, buff=0.06).move_to(P3(-6.4, 0.2))', '.arrange(DOWN, buff=0.06).move_to(P3(-6.5, -1.45))'),
    ('self.play(Kc.animate.set_value(3.5), ycc.animate.set_value(1.75), FadeOut(rot), f3.op.animate.set_value(1.0), run_time=1.0)', 'self.play(Kc.animate.set_value(3.5), ycc.animate.set_value(1.75), FadeOut(rot), f3.op.animate.set_value(1.0), comp.animate.set_value(1.0), run_time=1.0)'),
])
print('ok')

def edit(P, pares):
    s = open(P, encoding='utf-8').read()
    for a, b in pares:
        assert s.count(a) == 1, (s.count(a), a[:90])
        s = s.replace(a, b)
    open(P, 'w', encoding='utf-8').write(s)


edit('sec_e3.py', [
    (r'lbl(r"2R=0{,}60\ \mathrm{m}", GEO, 40), lado=RIGHT, d=1.5)', r'lbl(r"2R=0{,}60\ \mathrm{m}", C_RAIO, 40), lado=RIGHT, d=1.5, cor=C_RAIO)'),
    (r'lbl(r"R=0{,}30\ \mathrm{m}", GEO, 44)).arrange(RIGHT, buff=0.2)', r'lbl(r"R=0{,}30\ \mathrm{m}", C_RAIO, 44)).arrange(RIGHT, buff=0.2)'),
    (r'lbl(r"2r=0{,}20\ \mathrm{m}", GEO, 40), lado=LEFT, d=1.6)', r'lbl(r"2r=0{,}20\ \mathrm{m}", C_RAIO_MENOR, 40), lado=LEFT, d=1.6, cor=C_RAIO_MENOR)'),
    (r'lbl(r"r=0{,}10\ \mathrm{m}", GEO, 44)).arrange(RIGHT, buff=0.2)', r'lbl(r"r=0{,}10\ \mathrm{m}", C_RAIO_MENOR, 44)).arrange(RIGHT, buff=0.2)'),
    # E3-3: esquema 2.5D frontal (carretel, fios, blocos) no lugar do 3D, com os círculos de raio lima/magenta
    (r'''        cR3 = cota23(o_, t1, lbl(r"R=0{,}30\ \mathrm{m}", GEO, 40), lado=UP, d=1.5)
        cr3 = cota23(o_, t2, lbl(r"r=0{,}10\ \mathrm{m}", GEO, 40), lado=UP + LEFT, d=1.3)
        pt3 = VGroup(*[VGroup(Dot(p_, radius=0.09, color=HALO), Dot(p_, radius=0.055, color=WHITE_)) for p_ in (t1, t2)]).set_z_index(18)
        self.play(FadeIn(cR3), FadeIn(cr3), FadeIn(pt3), run_time=0.6)''',
     r'''        sc25 = abs(t1[0] - o_[0]) / RC
        Rg25, Rp25 = abs(t1[0] - o_[0]), abs(t2[0] - o_[0])

        def esq25():
            cc = cam()
            o = pr(cc, (0, 0, 0))
            th0 = thv()
            ta = pr(cc, (XB1, YG, 0.0))
            tang = np.array([-(ta[1] - o[1]), ta[0] - o[0], 0.0])
            dl_ = pr(cc, (XB1, YG, Z1 - RC * (th0 + 0.02))) - pr(cc, (XB1, YG, Z1 - RC * th0))
            sg = 1.0 if float(np.dot(tang, dl_)) >= 0 else -1.0
            g_ = VGroup(carretel25(o, Rg25, Rp25, sg * th0))
            b1_, b2_ = pb1(), pb2()
            s1_, s2_ = 0.14 * sc25, L2() * sc25
            ta2 = pr(cc, (XB2, YP, 0.0))
            g_.add(Line(ta, b1_ + 0.5 * s1_ * UP).set_stroke(HALO, 6).set_z_index(5), Line(ta, b1_ + 0.5 * s1_ * UP).set_stroke(LINHA_CL, 2.4).set_z_index(5.1),
                   Line(ta2, b2_ + 0.5 * s2_ * UP).set_stroke(HALO, 6).set_z_index(5), Line(ta2, b2_ + 0.5 * s2_ * UP).set_stroke(LINHA_CL, 2.4).set_z_index(5.1))
            g_.add(bloco25(b1_, s1_).set_z_index(6), bloco25(b2_, s2_).set_z_index(6))
            return g_
        esq = vivo(esq25)
        self.add(esq)
        self.play(f3.op.animate.set_value(0.0), run_time=0.4)
        cR3 = cota23(o_, t1, lbl(r"R=0{,}30\ \mathrm{m}", C_RAIO, 40), lado=UP, d=1.5, cor=C_RAIO)
        cr3 = cota23(o_, t2, lbl(r"r=0{,}10\ \mathrm{m}", C_RAIO_MENOR, 40), lado=UP + LEFT, d=1.3, cor=C_RAIO_MENOR)
        cc3 = VGroup(circ_raio(o_, Rg25, C_RAIO, 4.0, tracejado=False), circ_raio(o_, Rp25, C_RAIO_MENOR, 4.0, tracejado=True))
        pt3 = VGroup(*[VGroup(Dot(p_, radius=0.09, color=HALO), Dot(p_, radius=0.055, color=cor_)) for p_, cor_ in ((t1, C_RAIO), (t2, C_RAIO_MENOR))]).set_z_index(18)
        self.play(FadeIn(cc3), FadeIn(cR3), FadeIn(cr3), FadeIn(pt3), run_time=0.6)'''),
    (r'fbd = VGroup(s_m1,', r'fbd = VGroup(cc3, s_m1,'),
])
print('ok')

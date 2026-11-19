B = chr(92)
def edit(P, pares):
    s = open(P, encoding='utf-8').read()
    for a, b in pares:
        assert s.count(a) == 1, (P, s.count(a), a[:100])
        s = s.replace(a, b)
    open(P, 'w', encoding='utf-8').write(s)
edit('sec_e3.py', [
    ('self.play(ucam.animate.set_value(1.0), Kc.animate.set_value(K3), ycc.animate.set_value(Y3), run_time=3.0, rate_func=smooth)',
     'self.play(ucam.animate.set_value(1.0), Kc.animate.set_value(6.0), ycc.animate.set_value(1.1), run_time=3.0, rate_func=smooth)        # o 3D fecha em K = 6,0 (o bloco pesado não corta a borda de baixo)'),
    ('''            g_ = VGroup(carretel25(o, Rg25, Rp25, sg * th0))
            b1_, b2_ = pb1(), pb2()
            s1_, s2_ = 0.14 * sc25, L2() * sc25
            ta2 = pr(cc, (XB2, YP, 0.0))''', '''            ta2 = pr(cc, (XB2, YP, 0.0))
            Rg_, Rp_ = float(np.linalg.norm(ta - o)), float(np.linalg.norm(ta2 - o))        # escala viva (o zoom K = 6,0 → 7,2 acontece depois da troca 3D → 2.5D)
            sc_ = Rg_ / RC
            g_ = VGroup(carretel25(o, Rg_, Rp_, sg * th0))
            b1_, b2_ = pb1(), pb2()
            s1_, s2_ = 0.14 * sc_, L2() * sc_'''),
    ('''        self.play(f3.op.animate.set_value(0.0), comp.animate.set_value(0.6), run_time=0.8)       # match cut 3D → 2.5D; o fio encurta para o carretel crescer
''', '''        self.play(f3.op.animate.set_value(0.0), comp.animate.set_value(0.6), Kc.animate.set_value(K3), ycc.animate.set_value(Y3), run_time=0.8)       # match cut 3D → 2.5D; o fio encurta e o carretel cresce
        c = cam()
        o_ = pr(c, (0, 0, 0))
        t1 = pr(c, (XB1, YG, 0.0))
        t2 = pr(c, (XB2, YP, 0.0))
        Rg25, Rp25 = abs(t1[0] - o_[0]), abs(t2[0] - o_[0])
'''),
    ('plano("E3-1 EXPLODIDO", -25.0, 12.0, 5.2, -3.85, 0.62,', 'plano("E3-1 EXPLODIDO", -25.0, 12.0, 4.7, -3.85, 0.4,'),
])
print('ok')

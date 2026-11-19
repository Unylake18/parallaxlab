def edit(P, pares):
    s = open(P, encoding='utf-8').read()
    for a, b in pares:
        assert s.count(a) == 1, (P, s.count(a), a[:100])
        s = s.replace(a, b)
    open(P, 'w', encoding='utf-8').write(s)
edit('sec_e3.py', [
    ('plano("E3-1 CLOSE", -50.0, 10.0, 8.5, -3.85, 0.55, 0.05, -0.25,', 'plano("E3-1 CLOSE", -50.0, 10.0, 6.2, -3.85, 0.9, 0.05, -0.25,'),
    ('ca = chamada(pr(cC, (RC + 0.008, YG, -0.15)), l_a, RIGHT + 0.2 * DOWN, 2.2, cor=MAS)', 'ca = chamada_em(pr(cC, (RC + 0.008, YG, -0.15)), l_a, P3(1.6, -1.8), cor=MAS)'),
    ('cb_ = chamada(pr(cC, (-(rc + 0.008), YP, -0.15)), l_b, LEFT + 0.2 * DOWN, 2.4, cor=MAS)', 'cb_ = chamada_em(pr(cC, (-(rc + 0.008), YP, -0.15)), l_b, P3(-6.0, -2.0), cor=MAS)'),
    ('.next_to(pb1(), RIGHT, buff=1.0)', '.next_to(pb1(), RIGHT, buff=0.85)'),
])

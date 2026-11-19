def edit(P, pares):
    s = open(P, encoding='utf-8').read()
    for a, b in pares:
        assert s.count(a) == 1, (P, s.count(a), a[:100])
        s = s.replace(a, b)
    open(P, 'w', encoding='utf-8').write(s)
edit('sec_e1a.py', [
    ('l_T2 = lbl("T", FC, 42).next_to(s_T2._fim, LEFT, buff=0.2)', 'l_T2 = lbl("T", FC, 42).next_to(s_T2._fim, RIGHT, buff=0.22)'),
    ('bz = chamada(o_, txt("BRAÇO ZERO", 30, bold=True, color=GEO), LEFT + 0.2 * DOWN, 2.3)', 'bz = chamada_em(o_, txt("BRAÇO ZERO", 30, bold=True, color=GEO), P3(-1.05, 2.15))'),
])

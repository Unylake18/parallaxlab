def edit(P, pares):
    s = open(P, encoding='utf-8').read()
    for a, b in pares:
        assert s.count(a) == 1, (P, s.count(a), a[:100])
        s = s.replace(a, b)
    open(P, 'w', encoding='utf-8').write(s)
edit('sec_e1a.py', [
    ('S6, C6 = 4.3, P3(-4.55, 0.6)                    # v5 §1.1: volante 2.5D com tambor, fio e bloco; anel de 3,4 u (≥ 55% da altura útil)',
     'S6, C6 = 4.8, P3(-4.5, 0.9)                     # v5 §1.1: volante 2.5D com tambor, fio e bloco; anel de 3,8 u (≥ 55% da altura útil)'),
    ('cx_, cy_ = -6.3, -1.4', 'cx_, cy_ = -1.2, -1.3'),
])
edit('sec_e1b.py', [
    ('S12, C12 = 4.6, P3(-4.3, 0.3)', 'S12, C12 = 5.0, P3(-4.4, 0.4)'),
    ('S17, C17 = 2.8, P3(-5.0, 1.75)', 'S17, C17 = 3.0, P3(-5.2, 1.9)'),
])

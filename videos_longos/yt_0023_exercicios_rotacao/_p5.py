def edit(P, pares):
    s = open(P, encoding='utf-8').read()
    for a, b in pares:
        assert s.count(a) == 1, (s.count(a), a[:80])
        s = s.replace(a, b)
    open(P, 'w', encoding='utf-8').write(s)


edit('sec_e1a.py', [
    ('"CUBO": (-50.0, 8.0, 11.0, -3.85, 0.95, 0.0, 0.0)', '"CUBO": (-50.0, 8.0, 8.5, -3.85, 0.15, 0.0, 0.0)'),
    ('"DISCOS": (-35.0, 8.0, 6.8, -3.85, 0.95, 0.0, 0.0)', '"DISCOS": (-35.0, 8.0, 6.2, -3.85, 0.45, 0.0, 0.0)'),
    ('"TAMBOR": (-55.0, 10.0, 9.0, -3.85, 0.95, 0.0, -0.05)', '"TAMBOR": (-55.0, 10.0, 8.0, -3.85, 0.15, 0.0, -0.05)'),
    ('self.plano_v("E1-4 CLOSE cubo", -50.0, 8.0, 11.0, -3.85, 0.95,', 'self.plano_v("E1-4 CLOSE cubo", -50.0, 8.0, 8.5, -3.85, 0.15,'),
    ('self.plano_v("E1-4 CLOSE disco", -35.0, 8.0, 6.8, -3.85, 0.95,', 'self.plano_v("E1-4 CLOSE disco", -35.0, 8.0, 6.2, -3.85, 0.45,'),
    ('self.plano_v("E1-5 EXPLODIDO", -32.0, 12.0, 4.2, -3.5, 0.9,', 'self.plano_v("E1-5 EXPLODIDO", -32.0, 12.0, 4.9, -3.5, 0.55,'),
    ('lbl(r"1{,}875", MAS, 40), UP + 0.2 * RIGHT, 1.1, cor=MAS)', 'lbl(r"1{,}875", MAS, 40), RIGHT + 0.3 * UP, 1.7, cor=MAS)'),
])
edit('sec_e3.py', [
    ('.move_to(P3(-3.85, -3.35)).set_z_index(16)', '.move_to(P3(-3.85, -4.05)).set_z_index(16)'),
])
print('ok')

def patch(p, pares):
    s = open(p, encoding='utf-8').read()
    for a, b in pares:
        assert s.count(a) == 1, (p, a[:60], s.count(a))
        s = s.replace(a, b)
    open(p, 'w', encoding='utf-8').write(s)


patch('sec_e1.py', [
    ('        degrau(self, "C1d", "= [x]₀¹ + [2x − x²/2]₁²")\n', '        degrau(self, "C1d", "= [x]₀¹ + [2x − x²/2]₁²")\n'),
    ('        B1 = linha(self, [("a", r"2-\\dfrac12")', '        sobe_col(self, [A1, ra1, A5], y0=220)\n        B1 = linha(self, [("a", r"2-\\dfrac12")'),
    ('        self.gat("um mais um meio")\n        A7 = linha(', '        self.gat("um mais um meio")\n        sobe_col(self, [A6], y0=220)\n        A7 = linha('),
])
patch('sec_e2.py', [
    ('        self.gat("A de fora é três quartos")\n', '        sobe_col(self, [M1, M2], y0=250)\n        self.gat("A de fora é três quartos")\n'),
])
patch('sec_e3.py', [
    ('        self.gat("w igual a a ao quadrado")\n', '        sobe_col(self, [A1b], y0=250)\n        self.gat("w igual a a ao quadrado")\n'),
])
patch('sec_e4.py', [
    ('        self.gat("Olha a matriz na tela")\n', '        sobe_col(self, [L2], y0=230)\n        self.gat("Olha a matriz na tela")\n'),
    ('        self.gat("faz a metade de cima")\n        mc = palavra', '        sobe_col(self, [L3], y0=230)\n        self.gat("faz a metade de cima")\n        mc = palavra'),
    ('        self.gat("A de fora integra")\n', '        sobe_col(self, [C1], y0=240)\n        self.gat("A de fora integra")\n'),
])
patch('sec_e6.py', [
    ('pl = painel(1180, 600, 680, 440)', 'pl = painel(1180, 520, 680, 440)'),
    ('1220, 830, 40)', '1220, 750, 40)'),
])
print('ok')

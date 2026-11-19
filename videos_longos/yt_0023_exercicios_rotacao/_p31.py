def edit(P, pares):
    s = open(P, encoding='utf-8').read()
    for a, b in pares:
        assert s.count(a) == 1, (P, s.count(a), a[:100])
        s = s.replace(a, b)
    open(P, 'w', encoding='utf-8').write(s)
edit('sec_e3.py', [
    ('''        self.play(FadeIn(V1t), run_time=0.3)
''', '''        self.play(FadeIn(V1t), run_time=0.3)
        Vl, ivl, vlb = self.linha(("T_1", "R", "-", "T_2", "r", "=", "I", r"\alpha"), size=46, rt=1.0, metodo="lei")        # v5 LEI PRIMEIRO: a lei literal antes dos números
'''),
    ('''        E0, ie0, _ = self.linha((r"\Delta U", "=", "m_1", "g", r"\cdot", r"1{,}0",''', '''        El, iel, _ = self.linha((r"\Delta U", "=", "m_1", "g", "h_1", "-", "m_2", "g", "h_2"), size=46, rt=1.0, metodo="lei")        # v5 LEI PRIMEIRO
        self.pilha.so(El)
        E0, ie0, _ = self.linha((r"\Delta U", "=", "m_1", "g", r"\cdot", r"1{,}0",'''),
])
edit('sec_e4.py', [
    ('''        A, ia, _ = self.linha(("l_{min}", "=", r"7{,}07\ \mathrm{cm}", "<", "R"), cores={2: C_RAIO}, size=46, rt=1.1)''', '''        Al, ial, _ = self.linha(("l_{min}", "=", r"\tfrac{R}{\sqrt{2}}"), size=46, rt=0.9, metodo="lei")        # v5 LEI PRIMEIRO
        A, ia, _ = self.linha(("l_{min}", "=", r"7{,}07\ \mathrm{cm}", "<", "R"), cores={2: C_RAIO}, size=46, rt=1.1)'''),
])
edit('sec_e1b.py', [
    ('''        L0, i0, l0b = self.linha((r"\alpha", "=", r"6{,}56\ \mathrm{rad/s^2}"), cores={2: ACC}, size=46, rt=1.0)''', '''        Ll, ill, _ = self.linha((r"\alpha", "=", r"\tfrac{a}{r}"), size=46, rt=0.9, metodo="lei")        # v5 LEI PRIMEIRO
        L0, i0, l0b = self.linha((r"\alpha", "=", r"6{,}56\ \mathrm{rad/s^2}"), cores={2: ACC}, size=46, rt=1.0)'''),
])
print('ok')

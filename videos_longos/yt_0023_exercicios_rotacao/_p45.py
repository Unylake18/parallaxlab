def edit(P, pares):
    s = open(P, encoding='utf-8').read()
    for a, b in pares:
        assert s.count(a) == 1, (P, s.count(a), a[:100])
        s = s.replace(a, b)
    open(P, 'w', encoding='utf-8').write(s)
edit('sec_e1a.py', [
    ('cx_, cy_ = -1.2, -1.3', 'cx_, cy_ = -6.2, -1.75'),
    ('mold = RoundedRectangle(corner_radius=0.1, width=2.0, height=2.0)', 'mold = RoundedRectangle(corner_radius=0.1, width=1.9, height=1.6)'),
    ('t_f = VGroup(txt("INÉRCIA EQUIVALENTE", 30, bold=True, color=MAS), txt("NÃO É PESO EXTRA", 30, bold=True, color=CYAN))', 't_f = VGroup(txt("INÉRCIA EQUIVALENTE", 26, bold=True, color=MAS), txt("NÃO É PESO EXTRA", 26, bold=True, color=CYAN))'),
])

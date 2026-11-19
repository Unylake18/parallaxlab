def edit(P, pares):
    s = open(P, encoding='utf-8').read()
    for a, b in pares:
        assert s.count(a) == 1, (P, s.count(a), a[:100])
        s = s.replace(a, b)
    open(P, 'w', encoding='utf-8').write(s)
edit('sec_ph.py', [
    ('b1 = VGroup(Line(p_dob + 0.95 * UP, p_meio + 0.95 * UP).set_stroke(GEO, 2.6), lbl(r"L/2", GEO, 40)', 'b1 = VGroup(Line(p_dob + 0.95 * UP, p_meio + 0.95 * UP).set_stroke(C_RAIO, 4.0), lbl(r"L/2", C_RAIO, 40)'),
    ('b2 = VGroup(Line(p_dob + 1.75 * UP, p_pt + 1.75 * UP).set_stroke(GEO, 2.6), lbl("L", GEO, 40)', 'b2 = VGroup(Line(p_dob + 1.75 * UP, p_pt + 1.75 * UP).set_stroke(C_RAIO, 4.0), lbl("L", C_RAIO, 40)'),
])

def edit(P, pares):
    s = open(P, encoding='utf-8').read()
    for a, b in pares:
        assert s.count(a) == 1, (P, s.count(a), a[:100])
        s = s.replace(a, b)
    open(P, 'w', encoding='utf-8').write(s)
edit('pecas23.py', [
    ('.set_stroke(HALO, w + 4).set_z_index(z - 0.2)\n    l = (DashedVMobject', '.set_stroke(HALO, w + 11).set_z_index(z - 0.2)\n    l = (DashedVMobject'),
    ('return VGroup(mk().set_stroke(HALO, w + 4).set_z_index(z - 0.2), mk().set_stroke(cor, w).set_z_index(z))', 'return VGroup(mk().set_stroke(HALO, w + 11).set_z_index(z - 0.2), mk().set_stroke(cor, w).set_z_index(z))'),
    ('    h = Line(a, b).set_stroke(HALO, w + 5).set_z_index(z - 0.2)\n', '    h = Line(a, b).set_stroke(HALO, w + (12 if w >= 4.0 else 5)).set_z_index(z - 0.2)      # v5 §4: lima/magenta (w ≥ 4) sobre halo escuro largo\n'),
])
edit('sec_e3.py', [
    ('K3, Y3 = 6.4, 1.15 ', 'K3, Y3 = 7.2, 0.95 '),
    ('comp.animate.set_value(0.7), run_time=0.8)', 'comp.animate.set_value(0.6), run_time=0.8)'),
    ('.next_to(pb1(), RIGHT, buff=0.65)', '.next_to(pb1(), RIGHT, buff=1.0)'),
])
print('ok')

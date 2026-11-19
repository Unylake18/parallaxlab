s = open('sec_e4.py', encoding='utf-8').read()
pares = [
    ('pg = lambda l, T_: P3(gx0 + gw * (l - 0.0) / 0.40,', 'pg = lambda l, T_: P3(gx0 + gw * (l - 0.02) / 0.38,'),
    ('Line(pg(0.0, 0.70), pg(0.40, 0.70))', 'Line(pg(0.02, 0.70), pg(0.40, 0.70))'),
    ('Line(pg(0.0, 0.70), pg(0.0, 1.30) + 0.1 * UP)', 'Line(pg(0.02, 0.70), pg(0.02, 1.30) + 0.1 * UP)'),
    ('lbl("T", W_, 40).move_to(pg(0.0, 1.30) + 0.35 * LEFT)', 'lbl("T", W_, 40).move_to(pg(0.02, 1.30) + 0.35 * LEFT)'),
    ('Line(pg(0.10 * k / 12, 1.30), pg(min(0.10, 0.10 * k / 12 + 0.045), 1.08))', 'Line(pg(0.02 + 0.08 * k / 12, 1.30), pg(min(0.10, 0.02 + 0.08 * k / 12 + 0.036), 1.08))'),
    ('Rectangle(width=gw * 0.10 / 0.40, height=gh).move_to((pg(0.0, 0.70) + pg(0.10, 1.30)) / 2)', 'Rectangle(width=gw * 0.08 / 0.38, height=gh).move_to((pg(0.02, 0.70) + pg(0.10, 1.30)) / 2)'),
]
for a, b in pares:
    assert s.count(a) == 1, a
    s = s.replace(a, b)
open('sec_e4.py', 'w', encoding='utf-8').write(s)
print('ok')

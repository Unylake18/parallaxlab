P = 'sec_e3.py'
s = open(P, encoding='utf-8').read()


def rep(a, b):
    global s
    assert s.count(a) == 1, (s.count(a), a[:80])
    s = s.replace(a, b)


rep('t_perf = txt("DOIS TAMBORES NO MESMO EIXO · GIRAM JUNTOS", 28, bold=True, color=GEO_CL)',
    't_perf = txt("DOIS TAMBORES · MESMO EIXO · GIRAM JUNTOS", 26, bold=True, color=GEO_CL)\n        t_perf.scale_to_fit_width(min(t_perf.width, 6.2))')
rep(".move_to(P3(-6.2, 2.45))", ".move_to(P3(-6.2, 1.15))")
open(P, 'w', encoding='utf-8').write(s)
print('ok')

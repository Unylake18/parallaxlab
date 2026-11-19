import re
pat = re.compile(r'lbl\((?:"d"|"l"|"R"|"l<R"|r"\\frac\{d\}\{4\}"|r"\\tfrac\{d\}\{4\}[^"]*"|r"l_\{eq\}[^"]*"|r"\d+\\ \\mathrm\{cm\}"), GEO')
for p in ('sec_e2.py', 'sec_e4.py'):
    s = open(p, encoding='utf-8', newline='').read()
    s, n = pat.subn(lambda m: m.group(0).replace('GEO', 'C_RAIO'), s)
    if p == 'sec_e2.py':
        s = s.replace('Line(a_ + 0.6 * DOWN, b_ + 0.6 * DOWN).set_stroke(GEO, 2.4)', 'Line(a_ + 0.6 * DOWN, b_ + 0.6 * DOWN).set_stroke(C_RAIO, 4.0)')
        s = s.replace('Line(a_ + 0.5 * UP, O + 0.5 * UP).set_stroke(GEO, 2.4)', 'Line(a_ + 0.5 * UP, O + 0.5 * UP).set_stroke(C_RAIO, 4.0)')
    s = s.replace('cores={0: GEO, 2: GEO, 4: GEO, 6: GEO}', 'cores={0: C_RAIO, 2: C_RAIO, 4: C_RAIO, 6: C_RAIO}').replace('cores={2: GEO}, size=46', 'cores={2: C_RAIO}, size=46')
    open(p, 'w', encoding='utf-8', newline='').write(s)
    print(p, n)

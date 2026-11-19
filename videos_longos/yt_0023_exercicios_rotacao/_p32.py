B = chr(92)
s = open('sec_e4.py', encoding='utf-8').read()
s = s.replace('r"\tfrac{R}{' + B + 'sqrt{2}}"', 'r"' + B + 'tfrac{R}{' + B + 'sqrt{2}}"')
open('sec_e4.py', 'w', encoding='utf-8').write(s)
s = open('sec_e1b.py', encoding='utf-8').read()
a = '        L0, i0, l0b = self.linha((r"' + B + 'alpha", "=", r"6{,}56' + B + ' ' + B + 'mathrm{rad/s^2}"), cores={2: ACC}, size=46, rt=1.0)'
b = '        Ll, ill, _ = self.linha((r"' + B + 'alpha", "=", r"' + B + 'tfrac{a}{r}"), size=46, rt=0.9, metodo="lei")        # v5 LEI PRIMEIRO\n' + a
assert s.count(a) == 1
open('sec_e1b.py', 'w', encoding='utf-8').write(s.replace(a, b))

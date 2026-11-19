P = 'sec_e3.py'
s = open(P, encoding='utf-8').read()
a = 'b2=pr(c, (XB2, YP, Z2 + rc * th)),'
assert s.count(a) == 1
s = s.replace(a, 'b2=pr(c, (XB2, YP - 0.15 * exc.get_value(), Z2 + rc * th)),')
open(P, 'w', encoding='utf-8').write(s)
print('ok')

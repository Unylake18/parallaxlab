s = open('sec_e1b.py', encoding='utf-8').read()
a = '        vt["th"].add_updater(lambda m: m.set_value(self.v_thfn()))\n'
assert s.count(a) == 1
s = s.replace(a, '        vt["th"].clear_updaters()                                       # v5 ALIASING: um só updater de θ (o do E1-13 competia e dava salto de ângulo)\n' + a)
open('sec_e1b.py', 'w', encoding='utf-8').write(s)

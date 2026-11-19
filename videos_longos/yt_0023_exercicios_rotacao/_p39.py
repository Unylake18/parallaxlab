s = open('pecas23.py', encoding='utf-8').read()
a = '''    h = (DashedVMobject(base.copy(), num_dashes=n, dashed_ratio=0.62) if tracejado else base.copy()).set_stroke(HALO, w + 11).set_z_index(z - 0.2)'''
b = '''    h = base.copy().set_stroke(HALO, w + 21).set_z_index(z - 0.2)                 # v5 CONTRASTE: halo escuro contínuo (mesmo no tracejado), ~6 px por lado a 960×540'''
assert s.count(a) == 1
s = s.replace(a, b)
a2 = 'return VGroup(mk().set_stroke(HALO, w + 11).set_z_index(z - 0.2), mk().set_stroke(cor, w).set_z_index(z))'
assert s.count(a2) == 1
s = s.replace(a2, 'return VGroup(base.copy().set_stroke(HALO, w + 21).set_z_index(z - 0.2), mk().set_stroke(cor, w).set_z_index(z))')
a3 = 'w + (12 if w >= 4.0 else 5)'
assert s.count(a3) == 1
s = s.replace(a3, 'w + (22 if w >= 4.0 else 5)')
open('pecas23.py', 'w', encoding='utf-8').write(s)

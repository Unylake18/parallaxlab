def edit(P, pares):
    s = open(P, encoding='utf-8').read()
    for a, b in pares:
        assert s.count(a) == 1, (P, s.count(a), a[:100])
        s = s.replace(a, b)
    open(P, 'w', encoding='utf-8').write(s)
edit('sec_e2.py', [
    ('from pecas23 import *  # noqa: F401,F403\n', 'from pecas23 import *  # noqa: F401,F403\nfrom pecas23b import haste25, lupa_pivo\n'),
    ('        fl = dict(peso=False,', '        h25op = ValueTracker(0.0)\n        self.add(h25op)\n        fl = dict(h25=False, lupa=False, peso=False,'),
    ('''            g = VGroup()
            if fl["cm"]:''', '''            g = VGroup()
            if fl["h25"]:                                  # v5 §1.3: a barra em 2.5D frontal (azul-aço escuro, pino e mancal) no lugar do 3D
                h_ = haste25(O, cm, t, LH)
                if h25op.get_value() < 0.999:
                    escala_op(h_, h25op.get_value())
                g.add(h_)
            if fl["cm"]:'''),
    ('''            return g

        dv = vivo(desenho)''', '''            if fl["lupa"]:                                 # v5 §1.3: lupa do pivô (E2-6 a E2-10)
                f = forca_eixo(t)
                g.add(lupa_pivo(O, t, f["F"] * KF, (-f["fr"] * KF * u) if fl["comp"] == "rp" else None, (f["fp"] * KF * n) if fl["comp"] == "rp" else None))
            return g

        dv = vivo(desenho)'''),
    ('''        self.play(ucam.animate.set_value(1.0), run_time=1.4)
        fl["lbl_d"] = True''', '''        self.play(ucam.animate.set_value(1.0), run_time=1.4)
        fl["h25"] = True
        self.play(h25op.animate.set_value(1.0), f3.op.animate.set_value(0.0), run_time=0.6)        # match cut 3D → 2.5D (mesma posição e comprimento)
        fl["lbl_d"] = True'''),
    ('        fl["F"] = "dash"\n', '        fl["F"] = "dash"\n        fl["lupa"] = True\n'),
    ('        self.an("E2-11")\n', '        self.an("E2-11")\n        fl["lupa"] = False\n'),
])
print("ok")

P = 'sec_ph.py'
s = open(P, encoding='utf-8').read()
a = '        self.play(fA.op.animate.set_value(1.0), FadeIn(dv), run_time=0.6)'
assert s.count(a) == 1
b = '''        disc_a = VGroup(Circle(radius=RD).move_to(C).set_fill(AÇO_FRIO, 1).set_stroke(AÇO_ARESTA, 3.5),
                        Circle(radius=RD * 0.9).move_to(C).set_fill("#2B3A55", 1).set_stroke(AÇO_ARESTA, 1.5, opacity=0.4),
                        *[Circle(radius=RD * f).move_to(C).set_stroke(AÇO_ARESTA, 1.4, opacity=0.3) for f in (0.7, 0.5)],
                        Circle(radius=0.28).move_to(C).set_fill("#1B2742", 1).set_stroke(AÇO_ARESTA, 2.0), Dot(C, radius=0.06, color=GEO_CL)).set_z_index(4)
        self.play(FadeIn(disc_a), FadeIn(dv), run_time=0.6)'''
s = s.replace(a, b)
s = s.replace('lbl("D", C_RAIO, 40).move_to((C + p2) / 2 + 0.32 * DOWN))', 'lbl("D", C_RAIO, 40).move_to((C + p2) / 2 + 0.42 * DOWN))')
open(P, 'w', encoding='utf-8').write(s)
print('ok')

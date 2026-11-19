P = 'sec_ph.py'
s = open(P, encoding='utf-8').read()


def rep(a, b):
    global s
    assert s.count(a) == 1, (s.count(a), a[:90])
    s = s.replace(a, b)


rep('''("o momento de inércia a soma", (r"I", "=", r"\\sum", "m", "r^2"), None),''',
    '''("o momento de inércia a soma", (r"I", "=", r"\\sum", "m", "r^2"), {3: MAS, 4: C_RAIO}),''')
rep('''("o teorema dos eixos paralelos", (r"I", "=", r"I_{cm}", "+", "M", "D^2"), None),''',
    '''("o teorema dos eixos paralelos", (r"I", "=", r"I_{cm}", "+", "M", "D^2"), {4: MAS, 5: C_RAIO}),''')
rep('''("e as pontes entre o giro", ("v", "=", r"\\omega", "r", r"\\quad", "a_t", "=", r"\\alpha", "r", r"\\quad", "a_c", "=", r"\\omega^2", "r"), None),''',
    '''("e as pontes entre o giro", ("v", "=", r"\\omega", "r", r"\\quad", "a_t", "=", r"\\alpha", "r", r"\\quad", "a_c", "=", r"\\omega^2", "r"), {3: C_RAIO, 8: C_RAIO, 13: C_RAIO}),''')
rep('''                mk = VGroup(*[VGroup(Dot(C + rr * np.array([math.cos(t_), math.sin(t_), 0]), radius=0.08, color=MAS),
                                     Line(C, C + rr * np.array([math.cos(t_), math.sin(t_), 0])).set_stroke(GEO, 2, opacity=0.8))
                              for rr, t_ in ((0.8, 2.3), (1.6, 3.6), (1.9, 5.2))])
                mk.add(lbl("r", GEO, 36).move_to(C + 1.05 * np.array([math.cos(3.6), math.sin(3.6), 0]) + 0.3 * UP))''',
    '''                mk = VGroup(*[VGroup(Line(C, C + rr * np.array([math.cos(t_), math.sin(t_), 0])).set_stroke(HALO, 9),
                                     Line(C, C + rr * np.array([math.cos(t_), math.sin(t_), 0])).set_stroke(C_RAIO, 4.5),
                                     Dot(C + rr * np.array([math.cos(t_), math.sin(t_), 0]), radius=0.13, color=HALO),
                                     Dot(C + rr * np.array([math.cos(t_), math.sin(t_), 0]), radius=0.09, color=MAS))
                              for rr, t_ in ((0.8, 2.3), (1.6, 3.6), (1.9, 5.2))])
                mk.add(VGroup(pilula(lbl("r", C_RAIO, 38).move_to(C + 1.05 * np.array([math.cos(3.6), math.sin(3.6), 0]) + 0.3 * UP), C_RAIO, 0.08),
                              lbl("r", C_RAIO, 38).move_to(C + 1.05 * np.array([math.cos(3.6), math.sin(3.6), 0]) + 0.3 * UP).set_z_index(17)))''')
rep('''DashedLine(C, p2, dash_length=0.08).set_stroke(GEO, 2.5), lbl("D", GEO, 36).move_to((C + p2) / 2 + 0.32 * DOWN))''',
    '''DashedLine(C, p2, dash_length=0.1).set_stroke(C_RAIO, 4.5), lbl("D", C_RAIO, 40).move_to((C + p2) / 2 + 0.32 * DOWN))''')
rep('''            self.play(FadeIn(mk), *[FadeOut(m) for m in velhas], run_time=0.5)''',
    '''            self.play(FadeIn(mk), *[FadeOut(m) for m in velhas], run_time=0.5)
            if k in (0, 1):                                  # v4 §1.2 #5: o r / D da fórmula e a linha do desenho pulsam juntos
                self.play(Indicate(mp(A, ia, [4 if k == 0 else 5]), color=None, scale_factor=1.25), Indicate(mk[0] if k == 0 else mk[1], color=None, scale_factor=1.08), run_time=0.7)''')
open(P, 'w', encoding='utf-8').write(s)
print('ok')

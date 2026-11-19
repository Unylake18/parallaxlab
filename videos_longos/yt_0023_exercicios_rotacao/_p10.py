def edit(P, pares):
    s = open(P, encoding='utf-8').read()
    for a, b in pares:
        assert s.count(a) == 1, (s.count(a), a[:90])
        s = s.replace(a, b)
    open(P, 'w', encoding='utf-8').write(s)


edit('pecas23.py', [
    ('def _pts3d(proj, R, y, n=72):\n    return [proj((R * math.cos(2 * PI * k / n), y, R * math.sin(2 * PI * k / n))) for k in range(n)]',
     'def _pts3d(proj, R, y, n=72, c=(0.0, 0.0)):\n    return [proj((c[0] + R * math.cos(2 * PI * k / n), y, c[1] + R * math.sin(2 * PI * k / n))) for k in range(n)]'),
    ('def circ3d(proj, R, y, cor, w=4.0, tracejado=False, z=14):', 'def circ3d(proj, R, y, cor, w=4.0, tracejado=False, z=14, c=(0.0, 0.0)):'),
    ('    pts = _pts3d(proj, R, y)\n    base', '    pts = _pts3d(proj, R, y, c=c)\n    base'),
])
edit('sec_e1a.py', [
    ('''        self.play(FadeIn(cb_), run_time=0.5)
        G0, ig0''', '''        circ_cb = VGroup(circ3d(self.vp, 0.10, -0.045, C_RAIO, w=4.5), linha_halo(self.v_eixo(), self.vp((0.10, -0.045, 0.0)), cor=C_RAIO, w=4.5))
        self.play(FadeIn(cb_), FadeIn(circ_cb), run_time=0.5)
        G0, ig0'''),
    ('''        self.play(FadeIn(cota), FadeIn(dk_), run_time=0.7)''', '''        circ_dk = VGroup(*[circ3d(self.vp, 0.05, -0.03, C_RAIO, w=4.5, c=(sx_ * 0.25, 0.0)) for sx_ in (1, -1)])
        self.play(FadeIn(cota), FadeIn(dk_), FadeIn(circ_dk), run_time=0.7)'''),
    ('anims=[FadeOut(cb_)])', 'anims=[FadeOut(cb_), FadeOut(circ_cb)])'),
    ('anims=[FadeOut(cota), FadeOut(dk_)])', 'anims=[FadeOut(cota), FadeOut(dk_), FadeOut(circ_dk)])'),
])
print('ok')

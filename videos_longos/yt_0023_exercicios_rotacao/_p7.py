import re
P = 'sec_e1a.py'
s = open(P, encoding='utf-8').read()


def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:90])
    s = s.replace(a, b)


rep(r'(r"R_1=0{,}30\ \mathrm{m}", GEO), (r"R_2=0{,}40\ \mathrm{m}", GEO)', r'(r"R_1=0{,}30\ \mathrm{m}", C_RAIO_MENOR), (r"R_2=0{,}40\ \mathrm{m}", C_RAIO)')
rep(r'(r"0{,}10\ \mathrm{m}", GEO), None, (0.0, -0.04, 0.0)', r'(r"0{,}10\ \mathrm{m}", C_RAIO), None, (0.0, -0.04, 0.0)')
rep(r'(r"0{,}05\ \mathrm{m}", GEO), (r"\text{a }0{,}25\ \mathrm{m}", GEO)', r'(r"0{,}05\ \mathrm{m}", C_RAIO), (r"\text{a }0{,}25\ \mathrm{m}", C_RAIO)')
rep(r'(r"r=0{,}15\ \mathrm{m}", GEO), None, None, (0.0, -0.11, 0.13)', r'(r"r=0{,}15\ \mathrm{m}", C_RAIO), None, None, (0.0, -0.11, 0.13)')
rep(r'lbl(r"R_1=0{,}30\ \mathrm{m}", GEO, 40), lado=LEFT, d=2.4)', r'lbl(r"R_1=0{,}30\ \mathrm{m}", C_RAIO_MENOR, 40), lado=LEFT, d=2.4, cor=C_RAIO_MENOR)')
rep(r'lbl(r"R_2=0{,}40\ \mathrm{m}", GEO, 40), lado=RIGHT, d=2.4)', r'lbl(r"R_2=0{,}40\ \mathrm{m}", C_RAIO, 40), lado=RIGHT, d=2.4, cor=C_RAIO)')
rep('cores={4: MAS, 6: GEO, 8: GEO}, size=46, rt=1.6)', 'cores={4: MAS, 6: C_RAIO_MENOR, 8: C_RAIO}, size=46, rt=1.6)')
rep(r'[lbl(r"R_1\to 0", GEO, 36)', r'[lbl(r"R_1\to 0", C_RAIO_MENOR, 36)')
rep(r'[lbl(r"R_1\to R_2", GEO, 36)', r'[lbl(r"R_1\to R_2", C_RAIO_MENOR, 36)')
rep(r'lbl(r"r=0{,}10\ \mathrm{m}", GEO, 40)).arrange(DOWN, buff=0.12, aligned_edge=LEFT)', r'lbl(r"r=0{,}10\ \mathrm{m}", C_RAIO, 40)).arrange(DOWN, buff=0.12, aligned_edge=LEFT)')
rep('voos={4: cb_[2][0], 6: cb_[2][1]}, cores={4: MAS, 6: GEO}, rt=1.2)', 'voos={4: cb_[2][0], 6: cb_[2][1]}, cores={4: MAS, 6: C_RAIO}, rt=1.2)')
rep(r'cota23(o_, pc, lbl(r"D=0{,}25\ \mathrm{m}", GEO, 40), lado=UP, d=1.6)', r'cota23(o_, pc, lbl(r"D=0{,}25\ \mathrm{m}", C_RAIO, 40), lado=UP, d=1.6, cor=C_RAIO)')
rep(r'lbl(r"r=0{,}05\ \mathrm{m}", GEO, 40)).arrange(DOWN, buff=0.12, aligned_edge=RIGHT)', r'lbl(r"r=0{,}05\ \mathrm{m}", C_RAIO, 40)).arrange(DOWN, buff=0.12, aligned_edge=RIGHT)')
rep('cores={4: MAS, 6: GEO, 8: MAS, 10: GEO}, size=46, rt=1.6)', 'cores={4: MAS, 6: C_RAIO, 8: MAS, 10: C_RAIO}, size=46, rt=1.6)')
rep('braco = VGroup(Line(o_, p_tg).set_stroke(GEO, 3.5), lbl("r", GEO, 40)', 'braco = VGroup(Line(o_, p_tg).set_stroke(HALO, 8), Line(o_, p_tg).set_stroke(C_RAIO, 4.5), lbl("r", C_RAIO, 40)')
rep(r'r15 = lbl(r"r=0{,}15\ \mathrm{m}", GEO, 40)', r'r15 = lbl(r"r=0{,}15\ \mathrm{m}", C_RAIO, 40)')
rep('cores={2: MAS, 4: GEO}, rt=1.2)', 'cores={2: MAS, 4: C_RAIO}, rt=1.2)')
rep('cores={2: ACC, 4: GEO}, rt=1.1)', 'cores={2: ACC, 4: C_RAIO}, rt=1.1)')

# E1-3: círculos de raio sobre o corte (elipses projetadas), tinte lima entre R1 e R2
rep(r'''        self.play(FadeIn(r_lbl), run_time=0.5)
        self.gat("então a densidade por área")''',
    r'''        circ_ = VGroup(anel_tinta3d(self.vp, 0.30, 0.40, 0.0, C_RAIO), circ3d(self.vp, 0.40, 0.0, C_RAIO, w=4.5), circ3d(self.vp, 0.30, 0.0, C_RAIO_MENOR, w=4.5, tracejado=True))
        self.play(FadeIn(circ_), FadeIn(r_lbl), run_time=0.6)
        self.gat("então a densidade por área")''')
open(P, 'w', encoding='utf-8').write(s)

P = 'pecas23.py'
s = open(P, encoding='utf-8').read()
rep('def carretel25(o, Rg, Rp, ang, destaque=None):', '''def _pts3d(proj, R, y, n=72):
    return [proj((R * math.cos(2 * PI * k / n), y, R * math.sin(2 * PI * k / n))) for k in range(n)]


def circ3d(proj, R, y, cor, w=4.0, tracejado=False, z=14):
    """Círculo de raio R no plano x–z (eixo y) projetado pela câmera atual `proj` (vira elipse nas vistas oblíquas), sobre halo escuro."""
    pts = _pts3d(proj, R, y)
    base = VMobject().set_points_as_corners(pts + [pts[0]])
    mk = lambda: (DashedVMobject(base.copy(), num_dashes=40, dashed_ratio=0.6) if tracejado else base.copy())
    return VGroup(mk().set_stroke(HALO, w + 4).set_z_index(z - 0.2), mk().set_stroke(cor, w).set_z_index(z))


def anel_tinta3d(proj, R1, R2, y, cor, op=0.18, z=13):
    """Faixa entre R1 e R2 (v4 §1.2 #2): tinte de 15–20% na cor do raio maior."""
    a, b = _pts3d(proj, R2, y), _pts3d(proj, R1, y)
    m = VMobject().set_points_as_corners(a + [a[0]] + b[::-1] + [b[-1]])
    return m.set_fill(cor, op).set_stroke(width=0).set_z_index(z)


def carretel25(o, Rg, Rp, ang, destaque=None):''')
open(P, 'w', encoding='utf-8').write(s)
print('ok')

def edit(P, pares):
    s = open(P, encoding='utf-8').read()
    for a, b in pares:
        assert s.count(a) == 1, (s.count(a), a[:100])
        s = s.replace(a, b)
    open(P, 'w', encoding='utf-8').write(s)


edit('pecas23.py', [
    ('def carretel25(o, Rg, Rp, ang, destaque=None):', '''def volante25(o, s, ang=0.0):
    """v5 §1.1: volante 2.5D frontal. Anel azul-aço escuro (R1 = 0,30 m, R2 = 0,40 m) com aro claro; cubo, quatro raios e dois discos pequenos
    (0,05 m a ±0,25 m, posição fixa e simétrica) em cinza-azulado; marca de giro no anel. `s` = unidades de tela por metro."""
    o = np.asarray(o, float)
    R2, R1 = 0.40 * s, 0.30 * s
    g = VGroup()
    g.add(Annulus(inner_radius=R1, outer_radius=R2).move_to(o).set_fill(AÇO_FRIO, 1).set_stroke(AÇO_ARESTA, 3.0))
    g.add(Circle(radius=R2 * 0.97).move_to(o).set_stroke(AÇO_ARESTA, 1.4, opacity=0.4))
    for k in range(4):
        a = ang + k * PI / 2 + PI / 4
        u = np.array([math.cos(a), math.sin(a), 0.0])
        g.add(Line(o + 0.1 * s * u, o + R1 * u).set_stroke("#1E2A44", 12), Line(o + 0.1 * s * u, o + R1 * u).set_stroke("#5B6B8C", 8))
    a = ang + 0.9
    u = np.array([math.cos(a), math.sin(a), 0.0])
    g.add(Line(o + (R1 + 0.02 * s) * u, o + (R2 - 0.02 * s) * u).set_stroke(AÇO_CLARO, 3.0, opacity=0.8))
    for sx in (1, -1):
        c = o + sx * 0.25 * s * RIGHT
        g.add(Circle(radius=0.05 * s).move_to(c).set_fill(AÇO_CLARO, 1).set_stroke("#1E2A44", 2.5), Dot(c, radius=0.012 * s, color="#1E2A44"))
    g.add(Circle(radius=0.10 * s).move_to(o).set_fill("#5B6B8C", 1).set_stroke(AÇO_CLARO, 2.5), Circle(radius=0.04 * s).move_to(o).set_fill(AÇO_CLARO, 1).set_stroke(width=0), Dot(o, radius=0.012 * s, color=GEO_CL))
    return g.set_z_index(4)


def carretel25(o, Rg, Rp, ang, destaque=None):'''),
])

s = open('sec_e1a.py', encoding='utf-8').read()
i = s.index('        self.v_flags["foco"] = "anel"\n        self.v_flags["cord"] = False')
j = s.index('        self.gat("então a densidade por área")')
novo13 = '''        self.v_flags["foco"] = "anel"
        self.v_flags["cord"] = False
        S25, C25 = 5.0, P3(-4.4, -0.1)         # v5 §1.1: esquema 2.5D frontal; escala (u/m) e centro; diâmetro 4,0 u (≥ 55% da altura útil)
        v25 = volante25(C25, S25)
        self.play(f3.op.animate.set_value(0.0), FadeIn(v25), run_time=0.8)
        self.gat("um disco cheio de quarenta centímetros")
        disco_l = Circle(radius=0.40 * S25).move_to(C25).set_fill(C_RAIO, 0.2).set_stroke(width=0).set_z_index(5)
        c2_ = circ_raio(C25, 0.40 * S25, C_RAIO, 4.5, tracejado=False)
        self.play(FadeIn(disco_l), FadeIn(c2_), run_time=0.8)
        self.gat("menos um disco de trinta")
        fatia = Circle(radius=0.30 * S25).move_to(C25).set_fill(C_RAIO_MENOR, 0.30).set_stroke(width=0).set_z_index(5.5)
        c1_ = circ_raio(C25, 0.30 * S25, C_RAIO_MENOR, 4.5, tracejado=True)
        self.play(FadeIn(fatia), FadeIn(c1_), run_time=0.7)
        tint_ = Annulus(inner_radius=0.30 * S25, outer_radius=0.40 * S25).move_to(C25).set_fill(C_RAIO, 0.18).set_stroke(width=0).set_z_index(5)
        self.play(fatia.animate.scale(1.18).set_fill(opacity=0.0), FadeOut(disco_l), FadeIn(tint_), run_time=1.0)
        rim2 = C25 + 0.40 * S25 * np.array([math.cos(0.35), math.sin(0.35), 0.0])
        rim1 = C25 + 0.30 * S25 * np.array([math.cos(-0.5), math.sin(-0.5), 0.0])
        pM = C25 + 0.35 * S25 * DOWN
        r_lbl = VGroup(chamada(rim1, lbl(r"R_1=0{,}30\\ \\mathrm{m}", C_RAIO_MENOR, 40), RIGHT, -1.1 - rim1[0], cor=C_RAIO_MENOR),
                       chamada(rim2, lbl(r"R_2=0{,}40\\ \\mathrm{m}", C_RAIO, 40), RIGHT, -1.1 - rim2[0], cor=C_RAIO),
                       chamada(pM, lbl(r"M=15\\ \\mathrm{kg}", MAS, 42), DOWN, 0.9, cor=MAS))
        circ_ = VGroup(c2_, c1_, tint_, fatia, linha_halo(C25, rim2, cor=C_RAIO, w=4.5), linha_halo(C25, rim1, cor=C_RAIO_MENOR, w=4.5))
        self.play(FadeIn(r_lbl), run_time=0.6)
'''
s = s[:i] + novo13 + s[j:]
open('sec_e1a.py', 'w', encoding='utf-8').write(s)

edit('sec_e1a.py', [
    ('''        self.plano_v("E1-4 CLOSE cubo", -50.0, 8.0, 8.5, -3.85, 0.15, rt=1.2, extra=(vt["corte"].animate.set_value(0.0), vt["th"].animate.set_value(0.0)))
        pcb = self.vp((0.0, -0.045, 0.06))
        cb_ = chamada(pcb, VGroup(lbl(r"M=3{,}0\\ \\mathrm{kg}", MAS, 40), lbl(r"r=0{,}10\\ \\mathrm{m}", C_RAIO, 40)).arrange(DOWN, buff=0.12, aligned_edge=LEFT), RIGHT + 0.9 * UP, 2.9)
        circ_cb = VGroup(circ3d(self.vp, 0.10, -0.045, C_RAIO, w=4.5), linha_halo(self.v_eixo(), self.vp((0.10, -0.045, 0.0)), cor=C_RAIO, w=4.5))''',
     '''        pcb = C25 + 0.10 * S25 * np.array([math.cos(0.9), math.sin(0.9), 0.0])
        cb_ = chamada(pcb, VGroup(lbl(r"M=3{,}0\\ \\mathrm{kg}", MAS, 40), lbl(r"r=0{,}10\\ \\mathrm{m}", C_RAIO, 40)).arrange(DOWN, buff=0.12, aligned_edge=LEFT), RIGHT, -0.8 - pcb[0], cor=C_RAIO)
        circ_cb = VGroup(circ_raio(C25, 0.10 * S25, C_RAIO, 4.5, tracejado=False), linha_halo(C25, pcb, cor=C_RAIO, w=4.5))'''),
    ('''        self.plano_v("E1-4 CLOSE disco", -35.0, 8.0, 6.2, -3.85, 0.45, 0.0, 0.0, rt=1.2)
        pc = self.vp((0.25, -0.03, 0.0))
        o_ = self.v_eixo()
        cota = cota23(o_, pc, lbl(r"D=0{,}25\\ \\mathrm{m}", C_RAIO, 40), lado=UP, d=1.6, cor=C_RAIO)
        pdk = self.vp((-0.25, -0.03, 0.0))
        dk_ = chamada(pdk, VGroup(lbl(r"m=1{,}0\\ \\mathrm{kg}", MAS, 40), lbl(r"r=0{,}05\\ \\mathrm{m}", C_RAIO, 40)).arrange(DOWN, buff=0.12, aligned_edge=RIGHT), DOWN + 0.25 * LEFT, 1.9)
        circ_dk = VGroup(*[circ3d(self.vp, 0.05, -0.03, C_RAIO, w=4.5, c=(sx_ * 0.25, 0.0)) for sx_ in (1, -1)])''',
     '''        pc = C25 + 0.25 * S25 * RIGHT + 0.05 * S25 * UP
        cota = chamada(pc, lbl(r"D=0{,}25\\ \\mathrm{m}", C_RAIO, 40), RIGHT, -1.2 - pc[0] + 0.0, cor=C_RAIO)
        pdk = C25 - 0.25 * S25 * RIGHT + 0.05 * S25 * DOWN
        dk_ = chamada(pdk, VGroup(lbl(r"m=1{,}0\\ \\mathrm{kg}", MAS, 40), lbl(r"r=0{,}05\\ \\mathrm{m}", C_RAIO, 40)).arrange(DOWN, buff=0.12, aligned_edge=RIGHT), DOWN, pdk[1] + 2.75, cor=C_RAIO)
        circ_dk = VGroup(*[circ_raio(C25 + sx_ * 0.25 * S25 * RIGHT, 0.05 * S25, C_RAIO, 4.5, tracejado=False) for sx_ in (1, -1)], linha_halo(C25, C25 + 0.25 * S25 * RIGHT, cor=C_RAIO, w=4.5))'''),
    ('''self.pilha.so(maeb, fb, gb, kb, anims=[FadeOut(cota), FadeOut(dk_), FadeOut(circ_dk)])''',
     '''self.pilha.so(maeb, fb, gb, kb, anims=[FadeOut(cota), FadeOut(dk_), FadeOut(circ_dk), FadeOut(v25), f3.op.animate.set_value(1.0)])'''),
])
print('ok')

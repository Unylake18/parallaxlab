def edit(P, pares):
    s = open(P, encoding='utf-8').read()
    for a, b in pares:
        assert s.count(a) == 1, (P, s.count(a), a[:100])
        s = s.replace(a, b)
    open(P, 'w', encoding='utf-8').write(s)
edit('sec_e4.py', [
    ('from pecas23 import *  # noqa: F401,F403\n', 'from pecas23 import *  # noqa: F401,F403\nfrom pecas23b import mancal25, pino25, AÇO_ESC\n'),
    ('''def simples(o, l, ang, cor=MAS):''', '''def disco25(c, ang, R=None):
    """v5 §1.3: disco de aço 2.5D frontal (azul-aço escuro, aro claro, marca de giro)."""
    c = np.asarray(c, float)
    R = S * R_ if R is None else R
    g = VGroup(Circle(radius=R).move_to(c).set_fill(AÇO_FRIO, 1).set_stroke(AÇO_ARESTA, 3.0),
               Circle(radius=R * 0.86).move_to(c).set_fill(AÇO_ESC, 0.55).set_stroke(AÇO_ARESTA, 1.4, opacity=0.4),
               Line(c + 0.38 * R * np.array([math.cos(ang + 0.5), math.sin(ang + 0.5), 0]), c + 0.84 * R * np.array([math.cos(ang + 0.5), math.sin(ang + 0.5), 0])).set_stroke(AÇO_CLARO, 3.0, opacity=0.85),
               Circle(radius=R * 0.14).move_to(c).set_fill("#5B6B8C", 1).set_stroke(AÇO_CLARO, 1.8))
    return g


def pend25(o, l, ang, duplo=True):
    """Pêndulo 2.5D: haste leve do pino ao centro do disco de baixo; o disco de cima (se houver) no próprio pino; mancal fixo."""
    o = np.asarray(o, float)
    u = np.array([math.sin(ang), -math.cos(ang), 0.0])
    c = o + S * l * u
    g = VGroup(mancal25(o, 3))
    if l > 0.01:
        g.add(Line(o, c).set_stroke(HALO, 8).set_z_index(3.4), Line(o, c).set_stroke("#8FA6C9", 4.5).set_z_index(3.5))
    if duplo:
        g.add(disco25(o, ang).set_z_index(4))
    g.add(disco25(c, ang).set_z_index(4.2), pino25(o, 0.12, 4.8))
    return g


def simples(o, l, ang, cor=MAS):'''),
    ('''        f3 = Fundo3D(self, "pendulo", est, op=0.0)
        self.add(f3)
''', '''        f3 = Fundo3D(self, "pendulo", est, op=0.0)
        self.add(f3)
        sw = {"t": None}                                       # v5 §1.3: depois do dolly o 3D cede lugar ao 2.5D (mesma posição: tela = S·(x, z))
        f3.mult = lambda t: 1.0 if sw["t"] is None else 1.0 - clamp((t - sw["t"]) / 0.4, 0.0, 1.0)

        def camada25():
            g = VGroup()
            o25 = (0.0 if sw["t"] is None else clamp((self.clk.get_value() - sw["t"]) / 0.4, 0.0, 1.0)) * f3.op.get_value()
            if o25 < 0.01:
                return g
            for o, l, a, d in self.pend_fn():
                g.add(pend25(o, l, a, d))
            if o25 < 0.999:
                escala_op(g, o25)
            return g

        p25 = vivo(camada25)
        self.add(p25)
'''),
    ('''            if not flags["pesos"]:
                g.add(lbl("M", MAS, 42).move_to(c + P3(-1.45, 0.0)), lbl("R", C_RAIO, 42).move_to(c + P3(1.4, -0.75)),''', '''            if not flags["pesos"]:
                rim = c + S * R_ * np.array([math.cos(-0.5), math.sin(-0.5), 0.0])
                g.add(circ_raio(c, S * R_, C_RAIO, 4.0, tracejado=True), linha_halo(c, rim, cor=C_RAIO, w=4.0), linha_halo(rim, c + P3(1.18, -0.68), cor=C_RAIO, w=1.8))
                g.add(lbl("M", MAS, 42).move_to(c + P3(-1.45, 0.0)), lbl("R", C_RAIO, 42).move_to(c + P3(1.4, -0.75)),'''),
    ('''        flags["ov"] = True
        self.gat("com os centros a uma distância l")''', '''        flags["ov"] = True
        sw["t"] = self.clk.get_value()
        self.gat("com os centros a uma distância l")'''),
])
print("ok")

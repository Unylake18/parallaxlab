"""v5: volante25 com giro/calor/aro, rig25 (volante + tambor + fio + bloco + pastilha, redesenhado por quadro) e modo 2.5D do VolanteMix."""
p = 'pecas23.py'
s = open(p, encoding='utf-8').read()
i = s.index('def volante25(o, s, ang=0.0):')
j = s.index('def carretel25(o, Rg, Rp, ang, destaque=None):')
novo = '''def volante25(o, s, ang=0.0, heat=0.0, aro=False):
    """v5 §1.1: volante 2.5D frontal. Anel azul-aço escuro (R1 = 0,30 m, R2 = 0,40 m) com aro claro; cubo, quatro raios e dois discos pequenos
    (0,05 m a ±0,25 m; giram junto com o volante) em cinza-azulado; marca de giro no anel. `s` = unidades de tela por metro. `heat` (0–1) esquenta o
    anel; `aro` desenha só o aro fino (E1-17)."""
    o = np.asarray(o, float)
    R2, R1 = 0.40 * s, (0.385 * s if aro else 0.30 * s)
    quente = "#C4452A"
    fc = interpolate_color(ManimColor(AÇO_FRIO), ManimColor(quente), 0.8 * heat)
    ac = interpolate_color(ManimColor(AÇO_ARESTA), ManimColor("#FFB38A"), 0.8 * heat)
    g = VGroup()
    g.add(Annulus(inner_radius=R1, outer_radius=R2).move_to(o).set_fill(fc, 1).set_stroke(ac, 3.0))
    g.add(Circle(radius=R2 * 0.97).move_to(o).set_stroke(ac, 1.4, opacity=0.4))
    for k in range(4):
        a = ang + k * PI / 2 + PI / 4
        u = np.array([math.cos(a), math.sin(a), 0.0])
        if aro:
            g.add(Line(o + 0.1 * s * u, o + R1 * u).set_stroke("#1E2A44", 7), Line(o + 0.1 * s * u, o + R1 * u).set_stroke("#5B6B8C", 4))
        else:
            g.add(Line(o + 0.1 * s * u, o + R1 * u).set_stroke("#1E2A44", 12), Line(o + 0.1 * s * u, o + R1 * u).set_stroke("#5B6B8C", 8))
    a = ang + 0.9
    u = np.array([math.cos(a), math.sin(a), 0.0])
    g.add(Line(o + (R1 + 0.0 * s) * u, o + (R2 - 0.0 * s) * u).set_stroke(AÇO_CLARO, 3.0, opacity=0.9) if aro else Line(o + (R1 + 0.02 * s) * u, o + (R2 - 0.02 * s) * u).set_stroke(AÇO_CLARO, 3.0, opacity=0.8))
    if not aro:
        for sg in (1, -1):
            c = o + sg * 0.25 * s * np.array([math.cos(ang), math.sin(ang), 0.0])
            g.add(Circle(radius=0.05 * s).move_to(c).set_fill(AÇO_CLARO, 1).set_stroke("#1E2A44", 2.5), Dot(c, radius=0.012 * s, color="#1E2A44"))
    g.add(Circle(radius=0.10 * s).move_to(o).set_fill("#5B6B8C", 1).set_stroke(AÇO_CLARO, 2.5), Circle(radius=0.04 * s).move_to(o).set_fill(AÇO_CLARO, 1).set_stroke(width=0), Dot(o, radius=0.012 * s, color=GEO_CL))
    return g.set_z_index(4)


BLOCO_L = 0.62            # lado do bloco de 10 kg em unidades de tela (fixo; o "fantasma" de 90 kg compara com este)
Y_FUNDO = -3.15           # abaixo disto o bloco sai de cena (fica por cima da trilha)


def rig25(o, S, th, cai=0.0, cord=True, freio=False, heat=0.0, aro=False, bloco=True, tambor=True):
    """v5 §1.1: esquema 2.5D vivo do volante (eixo em `o`, `S` u/m): volante, tambor leve (r = 0,15 m, contorno lima), fio e bloco rosa (que desce
    0,15·θ + cai) e a pastilha do freio. Redesenhado por quadro a partir de θ, cai e calor."""
    o = np.asarray(o, float)
    g = VGroup(volante25(o, S, -th, heat=heat, aro=aro))
    if tambor:
        g.add(Circle(radius=0.15 * S).move_to(o).set_fill(AÇO_CLARO, 0.22).set_stroke(C_RAIO, 3.2).set_z_index(4.6))
        g.add(Dot(o, radius=0.012 * S, color=GEO_CL).set_z_index(4.7))
    xt = o[0] + 0.158 * S
    yb = o[1] + S * (ZB - 0.15 * th - cai)
    if bloco and yb - BLOCO_L / 2 > Y_FUNDO - 0.4:
        op = clamp((yb - Y_FUNDO + 0.4) / 0.8, 0.0, 1.0)
        if cord:
            g.add(Line([xt, o[1], 0], [xt, yb + BLOCO_L / 2, 0]).set_stroke(HALO, 6, opacity=op).set_z_index(4.8))
            g.add(Line([xt, o[1], 0], [xt, yb + BLOCO_L / 2, 0]).set_stroke("#D8E2F5", 2.6, opacity=op).set_z_index(4.9))
        g.add(RoundedRectangle(corner_radius=0.07, width=BLOCO_L, height=BLOCO_L).move_to([xt, yb, 0]).set_fill(MAS, 0.88 * op).set_stroke("#FFD0E5", 2.6, opacity=op).set_z_index(5))
    if freio:
        h = 0.07 * S
        pc = interpolate_color(ManimColor("#4A4F66"), ManimColor(HEAT), heat)
        g.add(RoundedRectangle(corner_radius=0.05, width=0.22 * S, height=h).move_to(o + (0.40 * S + h / 2) * UP).set_fill(pc, 1).set_stroke(AÇO_ARESTA, 2.4).set_z_index(5))
        g.add(Line(o + (0.40 * S + h) * UP, o + (0.40 * S + h + 0.12 * S) * UP).set_stroke("#8FA6C9", 5).set_z_index(5))
    return g.set_z_index(4)


'''
s = s[:i] + novo + s[j:]

a = '''    def vp(self, p):
        """Ponto 3D do volante → tela (câmera corrente)."""
        return pr(self.vcam(), p)'''
b = '''    def vp(self, p):
        """Ponto 3D do volante → tela (câmera corrente). No modo 2.5D (`modo25`) é o esquema frontal plano: x → horizontal, z → vertical."""
        m = getattr(self, "m25", None)
        if m is not None:
            return m[0] + m[1] * np.array([p[0], p[2], 0.0])
        return pr(self.vcam(), p)

    def modo25(self, C=None, S=None):
        """Liga (C e S) ou desliga o modo 2.5D: `vp`, `v_eixo` e `v_bloco` passam a valer no esquema frontal plano (u/m = S, eixo em C)."""
        self.m25 = None if C is None else (np.asarray(C, float), float(S))

    def rig25_vivo(self, dois=False, x2=1.25, S2=None):
        """Esquema 2.5D vivo guiado pelos mesmos trackers do 3D (θ, cai, calor, flags cord/freio). `dois`: o aro fino ao lado (E1-17)."""
        vt = self.vt
        C, S = self.m25

        def f():
            th = self.v_thfn() if self.v_thfn else vt["th"].get_value()
            g = VGroup(rig25(C, S, th, cai=vt["cai"].get_value(), cord=self.v_flags["cord"], freio=self.v_flags["freio"], heat=vt["heat"].get_value()))
            if self.v_flags.get("dois"):
                g.add(rig25(C + S * x2 * RIGHT, S, vt["th2"].get_value(), cord=True, aro=True))
            return g
        return vivo(f)'''
assert s.count(a) == 1
s = s.replace(a, b)
open(p, 'w', encoding='utf-8').write(s)
print('ok')

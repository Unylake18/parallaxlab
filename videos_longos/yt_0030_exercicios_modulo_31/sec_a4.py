"""Lote PA4 · A4 MAPAS QUE NÃO ENTORTAM · v3 (alvo v3_a4 + 25 v1). Malha à esquerda; à direita, o campo ③ do desafio até a morfose. d₁ = P_x − Q_y = 0: o Q_y atravessa o
"=" (glyph map) → P_x = Q_y; d₂ = Q_x + P_y = 0 → P_y = −Q_x. (x + iy)² aberto (leitura do i); i² = −1 por glyph map; os dois parênteses voam para
F = (x² − y², 2xy). "Lê como transformação": uma cópia da malha vai para a direita e se dobra continuamente por z^s (s de 1 a 2), com três cantinhos
de 90° andando junto (z^s é conforme fora da origem). O círculo pequeno é copiado e vira o círculo da direita. Mercator: meridianos e paralelos
em y = ln tan(π/4 + φ/2) (só linhas e círculos); círculos do mesmo tamanho na Terra em 0°, 45° e 70°, raio ∝ 1/cos φ; o de 70° acende na Groenlândia.
O irmão embaixo, longe do rodapé."""
from alg30 import *  # noqa: F401,F403
from sec_d5 import V3  # noqa: E402  (v4 C16: o palco do campo ③ é o mesmo do D5-9)

VL4 = VB(BE, 300, 760, 140)
VR4 = VB(BD, 1260, 800, 140)
dPx, dPy, dQx, dQy = r"\Pp_{\Am{x}}", r"\Pp_{\Mg{y}}", r"\Qq_{\Am{x}}", r"\Qq_{\Mg{y}}"
MARCAS = [(1.0, .5), (.75, .25), (1.25, .75)]
C0, R0 = (1.125, .625), .07


def eixos_rec(v, box, a, b, c, d):
    return VGroup(linha_rec(v, [(a, 0), (b, 0)], box, GEO, 2, .55), linha_rec(v, [(0, c), (0, d)], box, GEO, 2, .55)).set_z_index(2)


def zpow(z, s):
    """z^s pelo ramo principal (o argumento fica em [0, π/2] na malha): r·e^{iθ} → r^s·e^{isθ}."""
    return np.abs(z) ** s * np.exp(1j * s * np.angle(z))


def _pos(P, s, voa):
    """Pontos (plano) → px: (1 − voa)·[malha na esquerda] + voa·[z^s na direita]."""
    z = P[:, 0] + 1j * P[:, 1]
    w = zpow(z, s)
    a = np.array([VL4.c2p(x, y) for x, y in zip(z.real, z.imag)])
    b = np.array([VR4.c2p(x, y) for x, y in zip(w.real, w.imag)])
    return (1 - voa) * a + voa * b


class Malha(VGroup):
    """Malha [0,5; 1,5] × [0; 1] (passo 0,25): chapa + linhas coral 3 px. em(s, voa): s = expoente de z^s; voa = posição entre os painéis."""

    def __init__(self, z=6):
        super().__init__()
        self.ch = VMobject().set_fill(CHAPA_C, 1).set_stroke(width=0)
        self.ls = VGroup(*[VMobject().set_stroke(CORAL, 3 / 1.2, 1).set_fill(opacity=0) for _ in range(10)])
        for m in (self.ch, *self.ls):
            m._sem_contorno = True
        self.add(self.ch, self.ls)
        u = np.linspace(0, 1, 41)
        self.lin = [np.stack([np.full_like(u, .5 + k * .25), u], 1) for k in range(5)] + [np.stack([.5 + u, np.full_like(u, k * .25)], 1) for k in range(5)]
        self.bd = np.asarray(ret_pts((1, .5), 1, 30))
        self.set_z_index(z)
        self.ls.set_z_index(z + .1)
        self.em(1, 0)

    def em(self, s, voa):
        self.ch.set_points_as_corners(list(_pos(self.bd, s, voa)))
        for m, Lp in zip(self.ls, self.lin):
            m.set_points_as_corners(list(_pos(Lp, s, voa)))
        return self


def marca_pts(p, s, voa, ml=.09, mr=.15):
    """Cantinho de 90° na imagem do ponto p por z^s: lados ao longo das imagens das direções x e y (tamanho ml na esquerda, mr na direita)."""
    e = 1e-4
    z = p[0] + 1j * p[1]
    A, Bx, By = zpow(z, s), zpow(z + e, s), zpow(z + 1j * e, s)
    u, v = (Bx - A) / abs(Bx - A), (By - A) / abs(By - A)
    esq = [VL4.c2p(*(np.array([z.real, z.imag]) + d)) for d in (np.array([ml, 0]), np.array([ml, ml]), np.array([0, ml]))]
    dirx = [A + u * mr, A + u * mr + v * mr, A + v * mr]
    dir_ = [VR4.c2p(w.real, w.imag) for w in dirx]
    return [(1 - voa) * np.array(a) + voa * np.array(b) for a, b in zip(esq, dir_)]


class Marcas(VGroup):
    def __init__(self, s=1.0, voa=0.0):
        super().__init__(*[VMobject().set_stroke(BR, 2.5 / 1.2, 1).set_fill(opacity=0) for _ in MARCAS])
        for m in self:
            m._sem_contorno = True
        self.set_z_index(12)
        self.em(s, voa)

    def em(self, s, voa):
        for m, p in zip(self, MARCAS):
            m.set_points_as_corners(marca_pts(p, s, voa))
        return self


def circ_pequeno(s=None):
    pts = circ_pts(R0, C0, 60)
    if s is None:
        return vlinha(VL4, pts, BR, 3).set_z_index(13)
    z = np.array([p[0] + 1j * p[1] for p in pts])
    w = zpow(z, s)
    return vlinha(VR4, [(q.real, q.imag) for q in w], BR, 3).set_z_index(13)


def mercator():
    """Reticulado de Mercator (só linhas): meridianos igualmente espaçados e paralelos em y = k·ln tan(π/4 + φ/2), φ = 0°, 15°, …, 75°."""
    k = 1.5
    ym = lambda f: k * math.log(math.tan(PI / 4 + math.radians(f) / 2))
    xs = [-.6 + .393 * i for i in range(11)]
    g = VGroup()
    for x in xs:
        g.add(linha_rec(VR4, [(x, 0), (x, ym(75))], BD, GEO, 2, .75))
    for f in range(0, 76, 15):
        g.add(linha_rec(VR4, [(xs[0], ym(f)), (xs[-1], ym(f))], BD, GEO, 2, .75))
    circs = VGroup()
    for f, x in ((0, 1.0), (45, 1.6), (70, 2.2)):
        r = .12 / math.cos(math.radians(f))
        circs.add(vlinha(VR4, circ_pts(r, (x, ym(f)), 60), CORAL, 3).set_z_index(12))
    rot_f = VGroup(*[TXP30(t, *canto_xy(VR4, -.95, ym(f) + .02), 22, "right", GEO) for t, f in (("0°", 0), ("45°", 45), ("70°", 70))])
    return g.set_z_index(5), circs, rot_f


class LoteA4(Base):
    ANTES = "APLICAÇÃO · ÁGUA BATENDO NA PAREDE"

    def chaves(self, Fl, P_, Q_):
        """As chaves P e Q sob as componentes (o mesmo das chaves do D5)."""
        from alg30 import _nglifos
        t1, t2 = Fl.ts[Fl.ks.index("c1")], Fl.ts[Fl.ks.index("c2")]
        nb = lambda t, s_: _nglifos(r"\underbrace{" + t + "}_{" + s_ + "}") - _nglifos(t) - 1
        Fb = L([("F", Fl.ts[0]), ("u1", r"\underbrace{", 0), ("c1", t1), ("b1", "}", nb(t1, P_)), ("s1", "_{" + P_ + "}", 1), ("vg", r",\ "),
                ("u2", r"\underbrace{", 0), ("c2", t2), ("b2", "}", nb(t2, Q_)), ("s2", "_{" + Q_ + "}", 1), ("f", ")")], 0, 0, Fl.size)
        Fb.shift(Fl.p("c1").get_center() - Fb.p("c1").get_center())
        gm(self, Fl, Fb, rt=0.7, nota="(as chaves P e Q nascem sob as componentes)")
        return Fb

    def corpo(self):
        # ── A4-1 · v4 C16: LAYOUT A, palco = o campo ③ do desafio (o mesmo do D5-9); Cauchy-Riemann na coluna ──
        self.an("A4-1")
        self.secao("APLICAÇÃO · MAPAS QUE NÃO ENTORTAM")
        zera_chapas()
        ch3 = chapa_px(*LA, nome="A4 palco ③ (360, 780) 240 px/u", v=V3)
        ex3 = VGroup(linha_rec(V3, [(-.95, 0), (2.95, 0)], LA, GEO, 2, .4), linha_rec(V3, [(0, -.45), (0, 2.45)], LA, GEO, 2, .4))
        c3 = campo30(V3, F3, -.75, 2.75, -.25, 2.25, .25, rmin=0, mmax=6, nome="A4 f₃ (palco)")
        troca(self, "A2 → A4 (layout A: o campo ③ do desafio)")
        self.play(FadeIn(ch3), FadeIn(ex3), cresce_campo(c3, 0.8), run_time=0.8)
        pulsa = lambda rt=0.6: acende(self, [c3], CAMPO2, rt)
        D1 = L([("d", r"d_1="), ("px", dPx), ("m", "-"), ("qy", dQy), ("z", "=0")], 1120, 280, 34)
        D2 = L([("d", r"d_2="), ("qx", dQx), ("p", "+"), ("py", dPy), ("z", "=0")], 1120, 360, 34)
        self.gat("deformação zero em todo lugar")
        D2._origem = "a"
        escreve(self, D1, 0.2, extra=[caneta(D2, ritmo=0.2)])
        D1b = L([("d", r"d_1="), ("px", dPx), ("m", "-"), ("qy", dQy), ("z", "=0"), ("i", r"\ \Rightarrow\ "), ("px", dPx), ("eq", "="), ("qy", dQy)], 1120, 280, 34)
        self.gat("iguala cada deformação a zero")
        gm(self, D1, D1b, rt=0.9, nota="(Q_y atravessa o =)")
        D2b = L([("d", r"d_2="), ("qx", dQx), ("p", "+"), ("py", dPy), ("z", "=0"), ("i", r"\ \Rightarrow\ "), ("py", dPy), ("eq", "="), ("qx", r"-" + dQx)], 1120, 360, 34)
        self.gat("e a derivada vertical da primeira")
        gm(self, D2, D2b, rt=0.9, nota="(Q_x atravessa o = e troca de sinal)")
        lcr = legenda("EQUAÇÕES DE CAUCHY-RIEMANN", 1124, 425, GEO, "left", 26)
        self.gat("essas são as equações de cauchy")
        self.play(FadeIn(lcr, shift=0.05 * UP), run_time=0.4)
        self.ate(1.0)

        # ── A4-2 · z² inteiro: o molde (a + b)², i² = −1, o agrupamento; depois a conferência de Cauchy-Riemann no próprio z² ──
        self.an("A4-2")
        FZ0 = L([("F", r"\F=("), ("c1", r"\X^2-\Y^2"), ("vg", r",\ "), ("c2", r"2\X\Y"), ("f", ")")], 1120, 510, 34)
        self.gat("o nosso campo é exatamente o quadrado")
        pulsa(0.8)
        escreve(self, FZ0, 0.2)
        Z0 = L([("q", r"(\X+i\Y)^2")], 1120, 620, 34)
        self.gat("abre o quadrado")
        escreve(self, Z0, 0.2)
        MO = L([("m", r"(a+b)^2=a^2+2ab+b^2")], 1120, 690, 30)
        MO.set_color(GEO)
        self.gat("com o molde da soma ao quadrado")
        escreve(self, MO, 0.12)
        self.gat("o i da tela é a unidade imaginária")             # leitura 21: i
        le(self, Z0.p("q")[3], 21, "o i da tela é a unidade imaginária", ate="o quadrado da horizontal")
        zq = Z0.p("q")                                                 # ( x + i y ) 2
        Z1a = L([("q", r"(\X+i\Y)^2"), ("e", "="), ("a2", r"\X^2"), ("p1", "+"), ("ab", r"2\X(i\Y)"), ("p2", "+"), ("b2", r"(i\Y)^2")], 1120, 620, 34)
        self.gat("mais duas vezes i vezes o produto")
        fz = [zq[1].copy(), VGroup(zq[1], zq[3], zq[4]).copy(), VGroup(zq[3], zq[4]).copy()]
        gm(self, Z0, Z1a, rt=0.9, copia=True, voos={"a2": fz[0], "ab": fz[1], "b2": fz[2]}, nota="(a = x, b = iy no molde)")
        self.remove(Z0, *fz)                                           # o (x + iy)² da Z1a fica no mesmo lugar; as cópias-fonte dos voos saem
        Z1b = L([("q", r"(\X+i\Y)^2"), ("e", "="), ("a2", r"\X^2"), ("p1", "+"), ("ab", r"2i\X\Y"), ("p2", "+"), ("b2", r"i^2\Y^2")], 1120, 620, 34)
        gm(self, Z1a, Z1b, rt=0.7, nota="(2x(iy) = 2ixy; (iy)² = i²y²)")
        I2c = L([("i", r"i^2"), ("e", "="), ("m", "-1")], 1120, 690, 30)
        Z2 = L([("q", r"(\X+i\Y)^2"), ("e", "="), ("a2", r"\X^2"), ("p1", "+"), ("ab", r"2i\X\Y"), ("b2", r"-\Y^2")], 1120, 620, 34)
        self.gat("é menos um")
        self.play(FadeOut(MO), run_time=0.3)
        self.remove(MO)
        escreve(self, I2c, 0.15)
        pulsa()
        gm(self, Z1b, Z2, rt=0.8, voos={"b2": I2c.p("m")}, nota="(i² = −1: i²y² → −y²)")
        Z3 = L([("q", r"(\X+i\Y)^2"), ("e", "="), ("re", r"(\X^2-\Y^2)"), ("pi", r"+i\,"), ("im", r"(2\X\Y)")], 1120, 620, 34)
        self.gat("junta o que não tem i")
        gm(self, Z2, Z3, rt=0.9, ka=["q", "e", "re", "pi", "im", "re"], nota="(x² − y² juntos; 2ixy = i(2xy))")
        self.gat("sobra a diferença dos quadrados")
        acende(self, [Z3.p("re", "im")], AMB, 0.5)
        k1, k2 = Z3.p("re").copy(), Z3.p("im").copy()
        self.add(k1, k2)
        self.play(Transform(k1, FZ0.p("c1").copy()), Transform(k2, FZ0.p("c2").copy()), run_time=0.7)
        self.remove(k1, k2)
        acende(self, [FZ0, c3], CAMPO2, 0.8)
        self.gat("a primeira e a segunda componente")
        FZb = self.chaves(FZ0, r"\Pp", r"\Qq")
        CR1 = L([("p", r"\Pp_{\Am x}="), ("d", r"\dfrac{\partial(\X^2-\Y^2)}{\dx}"), ("r", r"=2\X"), ("eq", r"\ =\ "), ("q", r"\dfrac{\partial(2\X\Y)}{\dy}"),
                 ("qr", r"=\Qq_{\Mg y}"), ("ck", r"\ \checkmark")], 1120, 645, 30)
        CR2 = L([("p", r"\Pp_{\Mg y}="), ("d", r"\dfrac{\partial(\X^2-\Y^2)}{\dy}"), ("r", r"=-2\Y"), ("eq", r"\ =\ "), ("q", r"-\dfrac{\partial(2\X\Y)}{\dx}"),
                 ("qr", r"=-\Qq_{\Am x}"), ("ck", r"\ \checkmark")], 1120, 725, 30)
        self.gat("confere as equações")
        sai = [D1b, D2b, Z3, I2c, lcr]
        self.play(*[FadeOut(m) for m in sai], run_time=0.4)
        self.remove(*sai)
        pulsa()
        escreve_p(self, CR1, ["p"], 0.15)
        voa(self, FZb.p("c1"), CR1.p("d"), rt=0.45)
        escreve_p(self, CR1, ["r"], 0.15)
        self.gat("igual à derivada vertical da segunda")
        escreve_p(self, CR1, ["eq"], 0.15)
        voa(self, FZb.p("c2"), CR1.p("q"), rt=0.45)
        escreve_p(self, CR1, ["qr", "ck"], 0.15)
        junta(self, CR1, "b")
        self.gat("a derivada vertical da primeira é menos")
        pulsa()
        escreve_p(self, CR2, ["p"], 0.15)
        voa(self, FZb.p("c1"), CR2.p("d"), rt=0.45)
        escreve_p(self, CR2, ["r"], 0.15)
        self.gat("igual a menos a derivada horizontal")
        escreve_p(self, CR2, ["eq"], 0.15)
        voa(self, FZb.p("c2"), CR2.p("q"), rt=0.45)
        escreve_p(self, CR2, ["qr", "ck"], 0.15)
        junta(self, CR2, "b")
        self.gat("passou")
        acende(self, [CR1.p("ck"), CR2.p("ck"), c3], CAMPO2, 0.5)
        ltf = leg_mix(["TODA FUNÇÃO COMPLEXA DERIVÁVEL: ", r"$z^3$", ",", r"$e^z$"], 1124, 805, GEO, "left", 26)
        self.gat("e toda função complexa derivável")
        self.play(FadeIn(ltf, shift=0.05 * UP), run_time=0.4)
        pulsa()
        self.ate(1.0)

        # ── A4-3 · v4 C17: de volta ao LAYOUT B; a tabela de z² na faixa (J = |J|·rotação); a morfose z^s; Mercator ──
        self.an("A4-3")
        zera_chapas()
        pe, pd = chapa_px(*BE, nome="A4 esq. (300, 756)", v=VL4), chapa_px(*BD, nome="A4 dir. (1260, 792)", v=VR4)
        ee, ed = eixos_rec(VL4, BE, -1, 3.8, -.5, 4), eixos_rec(VR4, BD, -1, 3.8, -.25, 4.2)   # os eixos verticais param em 828 px, acima dos rótulos
        me = Malha()
        mk = Marcas()
        c_e = circ_pequeno()
        n1 = legenda("UMA MALHA DE QUADRADINHOS", 480, 868, GEO, "center", 28)
        mv = Malha(z=8)
        mk2 = Marcas()
        self.gat("agora lê como transformação")
        c3.clear_updaters()
        sai = [ch3, ex3, c3, FZb, CR1, CR2, ltf]
        self.play(*[FadeOut(m) for m in sai], run_time=0.4)
        self.remove(*sai)
        troca(self, "A4 layout A → layout B (malha à esquerda; a malha a transformar à direita)")
        self.play(FadeIn(pe), FadeIn(pd), Create(ee), Create(ed), FadeIn(me), FadeIn(n1), Create(mk), Create(c_e), run_time=0.6)
        self.add(mv, mk2)
        JC1 = L([("J", r"J="), ("m", r"\begin{pmatrix}\Am{2x} & \Mg{-2y}\\ \Am{2y} & \Mg{2x}\end{pmatrix}"), ("e", "="),
                 ("ab", r"\begin{pmatrix}a & -b\\ b & a\end{pmatrix}"), ("q", r",\quad a=2\X,\ \ b=2\Y")], 140, 958, 30)
        self.gat("a tabela desse campo")
        escreve_p(self, JC1, ["J", "m"], 0.1, extra=[UpdateFromAlphaFunc(mv, lambda m, a: m.em(1, smooth(a))), UpdateFromAlphaFunc(mk2, lambda m, a: m.em(1, smooth(a)))])   # a malha voa para a direita junto com a tabela
        self.gat("tem a forma a menos b")
        escreve_p(self, JC1, ["e", "ab", "q"], 0.1)
        junta(self, JC1)
        JC2 = L([("ab", r"\begin{pmatrix}a & -b\\ b & a\end{pmatrix}"), ("e", "="), ("s", r"\sqrt{a^2+b^2}\cdot"),
                 ("R", r"\begin{pmatrix}\cos\theta & -\sen\theta\\ \sen\theta & \cos\theta\end{pmatrix}")], 140, 958, 30)
        JC2b = L([("ab", r"\begin{pmatrix}a & -b\\ b & a\end{pmatrix}"), ("e", "="), ("s", r"\sqrt{a^2+b^2}\cdot"),
                  ("R", r"\begin{pmatrix}\cos\theta & -\sen\theta\\ \sen\theta & \cos\theta\end{pmatrix}"), ("q", r",\quad \sqrt{a^2+b^2}=2\sqrt{\X^2+\Y^2}=2r")],
                 140, 958, 30)
        self.gat("uma tabela assim é um número vezes")
        gm(self, JC1, JC2, rt=0.9, ka=["z", "z", "z", "ab", "z"], nota="(a −b; b a) = √(a² + b²) · rotação")
        acende(self, [mk, mk2], AMB, 0.6)
        self.gat("que dá duas vezes a distância")
        gm(self, JC2, JC2b, rt=0.6, nota="(√(4x² + 4y²) = 2r)")
        JC3 = L([("p", r"(1,1):\ \ "), ("J", r"J="), ("m", r"\begin{pmatrix}2 & -2\\ 2 & 2\end{pmatrix}"), ("e", "="), ("s", r"2\sqrt2\cdot"),
                 ("R", r"\begin{pmatrix}\cos45^\circ & -\sen45^\circ\\ \sen45^\circ & \cos45^\circ\end{pmatrix}")], 140, 958, 30)
        qa_ = .1
        qL = vlinha(VL4, [(1 - qa_, 1 - qa_), (1 + qa_, 1 - qa_), (1 + qa_, 1 + qa_), (1 - qa_, 1 + qa_), (1 - qa_, 1 - qa_)], CAMPO2, 3).set_z_index(14)
        d4 = 4 * qa_                                                   # J·(±a, ±a) com J = (2 −2; 2 2): gira 45° e cresce × 2√2
        qR = vlinha(VR4, [(0, 2 - d4), (d4, 2), (0, 2 + d4), (-d4, 2), (0, 2 - d4)], CAMPO2, 3).set_z_index(14)
        self.gat("no ponto um um ela é")
        gm(self, JC2b, JC3, rt=0.9, ka=["m", "e", "s", "R", "z"], nota="((1,1): a = b = 2; √8 = 2√2; θ = 45°)")
        self.play(Create(qL), run_time=0.3)
        qv = qL.copy()
        self.add(qv)
        self.play(Transform(qv, qR), run_time=1.0)                     # gira 45° e cresce × 2√2 no caminho: a JC3 acontecendo
        PtR = VR4.c2p(0, 2)
        col1 = Arrow(PtR, VR4.c2p(.3, 2.3), buff=0, stroke_width=2, max_tip_length_to_length_ratio=.2, color=BR).set_z_index(15)
        col2 = Arrow(PtR, VR4.c2p(-.3, 2.3), buff=0, stroke_width=2, max_tip_length_to_length_ratio=.2, color=BR).set_z_index(15)
        u1, u2 = np.array([1, 1, 0]) / math.sqrt(2), np.array([-1, 1, 0]) / math.sqrt(2)
        ang = VMobject().set_points_as_corners([PtR + u1 * .12, PtR + (u1 + u2) * .12, PtR + u2 * .12]).set_stroke(BR, 2 / 1.2, 1).set_z_index(15)
        for m_ in (col1, col2, ang):
            m_._sem_contorno = True
        self.gat("as duas colunas têm o mesmo tamanho")
        self.play(GrowArrow(col1), GrowArrow(col2), run_time=0.5)
        self.play(Create(ang), run_time=0.3)
        n2 = leg_mix(["DEPOIS DE z²: ÂNGULOS RETOS"], 1440, 868, GEO, "center", 28)
        c_d = circ_pequeno(2.0)
        self.gat("quadradinhos pequenos viram quadradinhos")
        self.play(FadeOut(qL), FadeOut(qv), FadeOut(col1), FadeOut(col2), FadeOut(ang), run_time=0.3)
        self.remove(qL, qv, col1, col2, ang)
        self.play(UpdateFromAlphaFunc(mv, lambda m, a: m.em(1 + smooth(a), 1)), UpdateFromAlphaFunc(mk2, lambda m, a: m.em(1 + smooth(a), 1)), FadeIn(n2),
                  run_time=2.0)
        for s in (1.0, 1.5, 2.0):
            print(f"[A4] z^{s:g}: cantinhos {[round(math.degrees(abs(np.angle((zpow(complex(*p) + 1j * 1e-4, s) - zpow(complex(*p), s)) / (zpow(complex(*p) + 1e-4, s) - zpow(complex(*p), s))))), 2) for p in MARCAS]}°")
        cp_ = c_e.copy()
        self.add(cp_)
        self.play(Transform(cp_, c_d), run_time=0.8)
        self.remove(cp_)
        self.add(c_d)
        self.gat("mas sempre com ângulos retos")
        acende(self, [mk, mk2], AMB, 1.2)
        grade_m, circs, rot_f = mercator()
        n3 = legenda("MERCATOR: ÂNGULOS PRESERVADOS", 1440, 868, GEO, "center", 28)
        self.gat("o mapa múndi de mercator")
        self.play(FadeOut(mv), FadeOut(mk2), FadeOut(c_d), FadeOut(n2), run_time=0.4)
        self.remove(mv, mk2, c_d, n2)
        self.play(Create(grade_m), FadeIn(n3), run_time=1.0)
        self.gat("preserva os ângulos")
        self.play(*[Create(c) for c in circs], FadeIn(rot_f), run_time=0.8)
        self.gat("por isso a groenlândia aparece")
        acende(self, [circs[2]], CAMPO2, 1.6)
        self.ate(1.0)

        # ── A4-4 · v4 C18: o irmão com as derivadas, na faixa ──
        self.an("A4-4")
        I0 = L([("F", r"\F=(\X^2-\Y^2,\ -2\X\Y)")], 140, 930, 30)
        I1 = TC(r"J=\begin{pmatrix}\Am{2x} & \Mg{-2y}\\ \Am{-2y} & \Mg{-2x}\end{pmatrix}", 560, 958, 30, caneta=False)
        celI, restoI = celulas(I1)
        I2 = L([("r", r"\V{\rot}=" + dQx + "-" + dPy + r"=-2y-(-2y)="), ("r0", r"\V0"), ("vg", r",\qquad "), ("d", r"\D{\dv}=" + dPx + "+" + dQy + "=2x-2x="),
                ("d0", r"\D0")], 860, 930, 26)
        I3 = L([("a", r"d_1=" + dPx + "-" + dQy + r"=2x-(-2x)=\Lm{4x}"), ("vg", r",\qquad "), ("b", r"d_2=" + dQx + "+" + dPy + r"=-2y-2y=\Lm{-4y}")], 860, 990, 26)
        self.gat("e o irmão desse campo")
        self.play(FadeOut(JC3), run_time=0.3)
        self.remove(JC3)
        escreve(self, I0, 0.12)
        self.gat("as derivadas da primeira são")
        print(f"[origem] a {self.lote} A4-4 {self.t:.2f} {I1._tex[:60]!r} (1ª linha)")
        self.play(caneta(VGroup(*restoI, *celI[(0, 0)], *celI[(0, 1)]), ritmo=0.2))
        self.gat("as da segunda menos dois ípsilon")
        self.play(caneta(VGroup(*celI[(1, 0)], *celI[(1, 1)]), ritmo=0.2))
        junta(self, I1)
        self.gat("rotacional menos dois ípsilon")
        escreve_p(self, I2, ["r", "r0"], 0.08)
        self.gat("divergente dois xis menos")
        escreve_p(self, I2, ["vg", "d", "d0"], 0.08)
        junta(self, I2)
        self.gat("rotacional zero divergente zero")
        acende(self, [I2.p("r0", "d0")], AMB, 0.8)
        self.gat("e as duas deformações quatro xis")
        escreve(self, I3, 0.08)
        so = T("SÓ DEFORMA", 1440, 868, 30, "center", LIMA)
        self.gat("esse irmão não gira")
        self.play(FadeOut(n3), run_time=0.25)                        # troca sequencial: sai, depois entra
        self.remove(n3)
        self.play(FadeIn(so, shift=0.05 * UP), run_time=0.3)
        self.sai_fim()

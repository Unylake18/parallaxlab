"""Lote PA4 · A4 MAPAS QUE NÃO ENTORTAM · v2 (alvo v2_a4 + 25 v1). Layout B com as duas malhas paradas desde o início. d₁ = P_x − Q_y = 0: o Q_y
atravessa o "=" (glyph map) → P_x = Q_y; d₂ = Q_x + P_y = 0 → P_y = −Q_x. (x + iy)² aberto; i² = −1 por glyph map; os dois parênteses voam para
F = (x² − y², 2xy). A malha voa e se curva; marcas de ângulo reto; Mercator no nome do painel; o irmão nas linhas de baixo."""
from alg30 import *  # noqa: F401,F403

VL4 = VB(BE, 300, 760, 140)
VR4 = VB(BD, 1260, 800, 140)
dPx, dPy, dQx, dQy = r"\Pp_{\Am{x}}", r"\Pp_{\Mg{y}}", r"\Qq_{\Am{x}}", r"\Qq_{\Mg{y}}"


def eixos_rec(v, box, a, b, c, d):
    return VGroup(linha_rec(v, [(a, 0), (b, 0)], box, GEO, 2, .55), linha_rec(v, [(0, c), (0, d)], box, GEO, 2, .55)).set_z_index(2)


class Malha(VGroup):
    """Malha [0,5; 1,5] × [0; 1] (passo 0,25): chapa + linhas coral 3 px. em(s, voa): s = quanto de z²; voa = posição entre os painéis."""

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
        self.em(0, 0)

    def _p(self, P, s, voa):
        z = P[:, 0] + 1j * P[:, 1]
        w = (1 - s) * z + s * z * z
        a = np.array([VL4.c2p(x, y) for x, y in zip(z.real, z.imag)])
        b = np.array([VR4.c2p(x, y) for x, y in zip(w.real, w.imag)])
        if voa <= 0:
            return np.array([VL4.c2p(x, y) for x, y in zip(w.real, w.imag)])
        return (1 - voa) * a + voa * b

    def em(self, s, voa):
        self.ch.set_points_as_corners(list(self._p(self.bd, s, voa)))
        for m, Lp in zip(self.ls, self.lin):
            m.set_points_as_corners(list(self._p(Lp, s, voa)))
        return self


def marcas_z2(m=.06):
    """Marcas de ângulo reto em 3 quinas da malha da direita (imagens de (0,5; 0), (1,5; 0), (1,5; 1))."""
    g = VGroup()
    for z0, du, dv in ((0.5 + 0j, 1, 1j), (1.5 + 0j, -1, 1j), (1.5 + 1j, -1, -1j)):
        w = z0 * z0
        dw = 2 * z0
        u = dw * du / abs(dw * du) * m
        v = dw * dv / abs(dw * dv) * m
        pts = [(w + u).real, (w + u).imag], [(w + u + v).real, (w + u + v).imag], [(w + v).real, (w + v).imag]
        g.add(vlinha(VR4, pts, BR, 2).set_z_index(12))
    return g


class LoteA4(Base):
    ANTES = "APLICAÇÃO · ÁGUA BATENDO NA PAREDE"

    def corpo(self):
        # ── A4-1 · as duas malhas desde o início; Cauchy-Riemann a partir de d₁ = d₂ = 0 ──
        self.an("A4-1")
        self.secao("APLICAÇÃO · MAPAS QUE NÃO ENTORTAM")
        zera_chapas()
        pe, pd = chapa_px(*BE, nome="A4 esq. (300, 756)", v=VL4), chapa_px(*BD, nome="A4 dir. (1260, 792)", v=VR4)
        ee, ed = eixos_rec(VL4, BE, -1, 3.8, -.8, 4), eixos_rec(VR4, BD, -1, 3.8, -.6, 4.2)
        me, md = Malha(), Malha(z=7).em(1, 1)
        n1 = legenda("UMA MALHA DE QUADRADINHOS", 480, 868, GEO, "center", 28)
        n2 = leg_mix(["DEPOIS DE z²: ÂNGULOS RETOS"], 1440, 868, GEO, "center", 28)
        troca(self, "A2 → A4 (layout B com as duas malhas)")
        self.play(FadeIn(pe), FadeIn(pd), Create(ee), Create(ed), FadeIn(me), FadeIn(md), FadeIn(n1), FadeIn(n2), run_time=0.8)
        D1 = L([("d", r"d_1="), ("px", dPx), ("m", "-"), ("qy", dQy), ("z", "=0")], 480, 945, 36, "c")
        D2 = L([("d", r"d_2="), ("qx", dQx), ("p", "+"), ("py", dPy), ("z", "=0")], 1440, 945, 36, "c")
        self.gat("deformação zero em todo lugar")
        D2._origem = "a"
        escreve(self, D1, 0.2, extra=[caneta(D2, ritmo=0.2)])
        D1b = L([("d", r"d_1="), ("px", dPx), ("m", "-"), ("qy", dQy), ("z", "=0"), ("i", r"\ \Rightarrow\ "), ("px", dPx), ("eq", "="), ("qy", dQy)], 480, 945, 36, "c")
        self.gat("iguala cada deformação a zero")
        gm(self, D1, D1b, rt=0.9, nota="(Q_y atravessa o =)")
        D2b = L([("d", r"d_2="), ("qx", dQx), ("p", "+"), ("py", dPy), ("z", "=0"), ("i", r"\ \Rightarrow\ "), ("py", dPy), ("eq", "="), ("qx", r"-" + dQx)], 1440, 945, 36, "c")
        self.gat("e a derivada vertical da primeira")
        gm(self, D2, D2b, rt=0.9, nota="(Q_x atravessa o = e troca de sinal)")
        self.ate(1.0)

        # ── A4-2 · o número complexo ──
        self.an("A4-2")
        self.gat("o nosso campo é exatamente o quadrado")         # R16: a malha transformada citada acende
        acende(self, [md], CORAL, 1.0)
        Z1 = L([("q", r"(\X+i\Y)^2"), ("e", "="), ("x2", r"\X^2"), ("t2", r"+2i\X\Y"), ("t3", r"+i^2\Y^2")], 720, 1022, 34, "c")
        self.gat("abre o quadrado")
        escreve(self, Z1, 0.2)
        Z2 = L([("q", r"(\X+i\Y)^2"), ("e", "="), ("x2", r"\X^2"), ("t2", r"+2i\X\Y"), ("t3", r"+i^2\Y^2"), ("e2", "="), ("re", r"(\X^2-\Y^2)"), ("pi", r"+i\,"),
                 ("im", r"(2\X\Y)")], 720, 1022, 34, "c")
        self.gat("é menos um")
        gm(self, Z1, Z2, rt=0.9, kb=["q", "e", "x2", "t2", "t3", "e2", "x2", "pi", "t2"])
        FZ = L([("F", r"\F=("), ("re", r"\X^2-\Y^2"), ("vg", r",\ "), ("im", r"2\X\Y"), ("f", ")")], 1440, 1022, 34, "c")
        self.gat("sobra a diferença dos quadrados")
        escreve_p(self, FZ, ["F", "vg", "f"], 0.3)
        voa(self, Z2.p("re"), FZ.p("re"), rt=0.6, extra=[TransformFromCopy(Z2.p("im"), FZ.p("im"))])
        junta(self, FZ, "b")
        self.ate(1.0)

        # ── A4-3 · como transformação: mapa conforme ──
        self.an("A4-3")
        mv = Malha(z=8)
        self.gat("agora lê como transformação")
        self.add(mv)
        self.play(UpdateFromAlphaFunc(mv, lambda m, a: m.em(smooth(a), smooth(a))), run_time=2.0)
        self.remove(mv)
        mr = marcas_z2()
        self.gat("sempre com ângulos retos")
        self.play(Create(mr), run_time=0.5)
        n3 = legenda("COMO NO MAPA DE MERCATOR: ÂNGULOS PRESERVADOS", 1440, 868, GEO, "center", 24)
        self.gat("o mapa múndi de mercator")
        troca_linha(self, n2, n3)
        self.ate(1.0)

        # ── A4-4 · o irmão ──
        self.an("A4-4")
        I1 = L([("c", r"(\X^2-\Y^2,\ -2\X\Y):\quad "), ("J", r"J=\begin{pmatrix}\Am{2x} & \Mg{-2y}\\ \Am{-2y} & \Mg{-2x}\end{pmatrix}")], 960, 950, 30, "c")
        I2 = L([("r", r"\V{\rot}=-2y-(-2y)=\V0"), ("d", r"\quad \D{\dv}=2x-2x=\D0")], 960, 1035, 30, "c")
        so = T("SÓ DEFORMA", 1560, 1045, 30, "center", LIMA)
        self.gat("e o irmão desse campo")
        self.play(*[FadeOut(m) for m in (D1b, D2b, Z2, FZ)], run_time=0.4)
        self.remove(D1b, D2b, Z2, FZ)
        escreve(self, I1, 0.15)
        self.gat("rotacional zero divergente zero")
        escreve(self, I2, 0.12)
        self.play(FadeIn(so, shift=0.05 * UP), run_time=0.3)
        self.sai_fim()

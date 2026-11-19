"""Lote PA4 · A4 MAPAS QUE NÃO ENTORTAM (alvo 25). Layout B (origens (300, 756) e (1260, 792), 144 px/u). Primeiro as duas equações de
Cauchy-Riemann em caneta (embaixo). Depois a malha de quadradinhos [0,5; 1,5] × [0; 1] à esquerda e a sua imagem por z² à direita: uma cópia voa e se
curva (z ↦ (1 − s)z + s·z², s de 0 a 1 em 2 s, junto com o voo de um painel ao outro). As quinas ficam em ângulo reto. Mercator e o irmão
(x² − y², −2xy) entram como rótulos com placa no alto do painel da esquerda."""
from lib30 import *  # noqa: F401,F403

VL4 = VB(BE, 300, 760, 140)
VR4 = VB(BD, 1260, 800, 140)


def eixos_rec(v, box, a, b, c, d):
    return VGroup(linha_rec(v, [(a, 0), (b, 0)], box, GEO, 2, .55), linha_rec(v, [(0, c), (0, d)], box, GEO, 2, .55)).set_z_index(2)


def borda_q():
    return ret_pts((1, .5), 1, 30)


class Malha(VGroup):
    """Malha [0,5; 1,5] × [0; 1] (passo 0,25): chapa + linhas coral 3 px. em(s, voa): s = quanto de z² (0 → z, 1 → z²); voa = posição entre os painéis."""

    def __init__(self, z=6):
        super().__init__()
        self.ch = VMobject().set_fill(CHAPA_C, 1).set_stroke(width=0)
        self.ls = VGroup(*[VMobject().set_stroke(CORAL, 3 / 1.2, 1).set_fill(opacity=0) for _ in range(10)])
        for m in (self.ch, *self.ls):
            m._sem_contorno = True
        self.add(self.ch, self.ls)
        u = np.linspace(0, 1, 41)
        self.lin = [np.stack([np.full_like(u, .5 + k * .25), u], 1) for k in range(5)] + [np.stack([.5 + u, np.full_like(u, k * .25)], 1) for k in range(5)]
        self.bd = np.asarray(borda_q())
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
        for m, L in zip(self.ls, self.lin):
            m.set_points_as_corners(list(self._p(L, s, voa)))
        self.s = s
        return self


class LoteA4(Base):
    ANTES = "APLICAÇÃO · ÁGUA BATENDO NA PAREDE"

    def corpo(self):
        # ── A4-1 · Cauchy-Riemann ──
        self.an("A4-1")
        self.secao("APLICAÇÃO · MAPAS QUE NÃO ENTORTAM")
        zera_chapas()
        pe, pd = chapa_px(*BE, nome="A4 esq. (300, 756)", v=VL4), chapa_px(*BD, nome="A4 dir. (1260, 792)", v=VR4)
        ee, ed = eixos_rec(VL4, BE, -1, 3.8, -.8, 4), eixos_rec(VR4, BD, -1, 3.8, -.6, 4.2)
        troca(self, "A2 → A4 (layout B)")
        self.play(FadeIn(pe), FadeIn(pd), Create(ee), Create(ed), run_time=0.8)
        CR = Pz([r"d_1=d_2=0\iff", r"\ \dfrac{\partial\Pp}{\dx}=\dfrac{\partial\Qq}{\dy},", r"\ \ \dfrac{\partial\Pp}{\dy}=-\dfrac{\partial\Qq}{\dx}"], 960, 950, 36, "c", caneta=False)
        for fr, i in (("deformação zero em todo lugar", 0), ("a derivada horizontal da primeira", 1), ("e a derivada vertical da primeira", 2)):
            self.gat(fr)
            self.play(caneta(sub_pz(CR, i), ritmo=0.35))
        junta_partes(self, CR)
        cr = leg_mix(["CAUCHY-RIEMANN · (x + iy)² = x² − y² + i·2xy"], 960, 1015, GEO, "center", 26)
        self.gat("equações de cauchy riemann")
        self.play(FadeIn(cr, shift=0.05 * UP), run_time=0.4)
        self.ate(1.0)

        # ── A4-2 · o número complexo; a malha ──
        self.an("A4-2")
        me = Malha()
        n1 = legenda("UMA MALHA DE QUADRADINHOS", 480, 868, GEO, "center", 28)
        self.gat("o nosso campo é exatamente o quadrado")
        self.play(FadeIn(me), FadeIn(n1), run_time=0.6)
        self.ate(1.0)

        # ── A4-3 · como transformação: mapa conforme (alvo 25) ──
        self.an("A4-3")
        md = Malha(z=7)
        n2 = leg_mix(["DEPOIS DE z²: ÂNGULOS RETOS"], 1440, 868, GEO, "center", 28)
        self.gat("agora lê como transformação")
        self.add(md)
        self.play(UpdateFromAlphaFunc(md, lambda m, a: m.em(smooth(a), smooth(a))), run_time=2.0)
        self.play(FadeIn(n2, shift=0.05 * UP), run_time=0.4)
        mc = TXP30("MAPA DE MERCATOR: PRESERVA OS ÂNGULOS", 480, 300, 26, "center", GEO)
        self.gat("o mapa múndi de mercator")
        self.play(FadeIn(mc), run_time=0.4)
        self.ate(1.0)

        # ── A4-4 · o irmão ──
        self.an("A4-4")
        ir = leg_mix([r"$(x^2-y^2,\ -2xy)$", ": rot 0 · div 0 · SÓ DEFORMA"], 480, 365, BR, "center", 26)
        ir = VGroup(placa7(ir, 8, 4), ir)
        self.gat("e o irmão desse campo")
        self.play(FadeIn(ir), run_time=0.4)
        self.sai_fim()

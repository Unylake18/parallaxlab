"""Lote PB5 · O ENGANO (layout A; alvo 09). O campo G (proporcional); a reta âmbar sobre o eixo x e a magenta sobre o eixo y (onde não há seta);
∂G/∂x(0,0) = ∂G/∂y(0,0) = 0⃗; as setas das diagonais acendem (verde claro, 7 px); classe C¹ e a aproximação."""
from v28 import *  # noqa: F401,F403

V = Vista(600, 540, 120)
DIAGS = [(1, 1), (1.5, 1.5), (2, 2), (-1, -1), (-1.5, -1.5), (-2, -2), (-1, 1), (-1.5, 1.5), (-2, 2), (1, -1), (1.5, -1.5), (2, -2)]


class LoteB5(Base):
    ANTES = "DERIVADA PARCIAL"

    def corpo(self):
        # ── B5-1 ──
        self.an("B5-1")
        self.secao("O ENGANO")
        cmp = campo28(V, F_DIAG, prop=True, rmin=.3, skip=lambda X, Y: abs(X) < .05 or abs(Y) < .05, nome="B5 campo das diagonais")
        P = ponto7(V.c2p(0, 0), POS, 10, 11)
        self.play(cresce_campo(cmp, 1.0), FadeIn(P), run_time=1.0)
        lx = vlinha(V, [(-3.1, 0), (3.1, 0)], E1, 4).set_z_index(6)
        ly = vlinha(V, [(0, -3.1), (0, 3.1)], E2, 4).set_z_index(6)
        self.gat("andando pelo eixo horizontal")
        self.play(Create(lx), run_time=1.0)
        d1 = TC(r"\dfrac{\partial\G}{\dx}(0,0)=\vec 0", 1120, 290, 44)
        self.gat("então a derivada na direção horizontal é zero")
        self.play(caneta(d1, ritmo=0.6))
        self.gat("pelo eixo vertical")
        self.play(Create(ly), run_time=1.0)
        d2 = TC(r"\dfrac{\partial\G}{\dy}(0,0)=\vec 0", 1120, 410, 44)
        self.gat("a derivada na direção vertical é zero")
        self.play(caneta(d2, ritmo=0.6))
        self.ate(0.97)

        # ── B5-2 ──
        self.an("B5-2")
        nc = legenda("E G NEM É CONTÍNUO EM (0, 0)", 1124, 555, BR)
        self.gat("e ele nem é contínuo ali")
        self.play(FadeIn(nc, shift=0.06 * UP), run_time=0.5)
        so = legenda("AS PARCIAIS SÓ OLHAM DUAS RETAS", 1124, 505, GEO)
        self.gat("as derivadas parciais só olham duas retas")
        self.play(FadeIn(so, shift=0.06 * UP), run_time=0.5)
        alvo = {s._xy: s for s in cmp}
        tr = []
        for X, Y in DIAGS:
            s = alvo.get((X, Y)) or next((a for a in cmp if abs(a._xy[0] - X) < 1e-6 and abs(a._xy[1] - Y) < 1e-6), None)
            if s is None:
                continue
            g = F_DIAG(X, Y)
            n = seta_prop(V, X, Y, g, .42, cor=CAMPO2, w=7, head=22)
            tr.append(Transform(s, n))
        self.gat("esconde tudo nas diagonais")
        self.play(LaggedStart(*tr, lag_ratio=0.08), run_time=1.4)
        self.ate(0.97)

        # ── B5-3 ──
        self.an("B5-3")
        c1 = leg_mix(["CLASSE", r"$\mathrm{C}^{1}$", "(PARCIAIS CONTÍNUAS)", r"$\Rightarrow$"], 1124, 680, SAIF, "left", 28, up=True, gap=6)
        self.gat("classe cê um")
        self.play(FadeIn(c1, shift=0.06 * UP), run_time=0.5)
        ap = TC(r"\F(\Pt+H)\approx\F(\Pt)+\h\,\dfrac{\partial\F}{\dx}+\k\,\dfrac{\partial\F}{\dy}", 1120, 780, 42)
        self.gat("a seta num ponto vizinho")
        self.play(caneta(ap, ritmo=0.6))
        self.ate(0.97)
        self.sai_fim()

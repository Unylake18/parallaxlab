"""yt_0036 · B2 · a transformação (alvo 05). Layout B: plano u, v à esquerda com o retângulo A (chapa + malha), plano x, y à direita.
Refino em três movimentos: um ponto voa pela seta φ; o lado Δu vira curva, depois o lado Δv; a célula inteira vira o quadrilátero curvo MNPQ.
Faixa de baixo a caneta (linhas mistas): (x, y) = φ(u, v) · φ DE CLASSE C¹ NO ABERTO Ω · B = φ(A) · ÁREA DE B = ?"""
from j36 import *

VU, AU = Vw(160, 790, 540), (-.05, 1.1, -.05, 1.1)
VX, AX = Vw(1300, 820, 265), (-1.1, 1.15, -.05, 2.15)
EMENDA_B2 = 975                                     # meio do vão entre o painel u, v (com v₀ CONSTANTE) e o x, y
u0, u1, v0, v1 = .55, .85, .35, .7


def curva_v(v, F, a, b, fixo, tipo, cor, wpx=4, n=24, z=8):
    ts = np.linspace(a, b, n + 1)
    pts = [v.px(*F(t, fixo)) if tipo == "u" else v.px(*F(fixo, t)) for t in ts]
    return lin_px(pts, cor, wpx, z=z)


class PB2(J36):
    ANTES = "O FATOR NUMA CURVA"

    def corpo(self):
        self.an("B2-1")
        self.secao("A TRANSFORMAÇÃO")
        dU = monta_plano(VU, AU, 1.12, 1.12, -.05, -.05, uv=True, ticks=[("x", u0, r"\Uc{u_0}"), ("y", v0, r"\Vc{v_0}")])
        dX = monta_plano(VX, AX, 1.15, 2.2, -1.1, -.05)
        self.fundo(VU, VX, emenda=EMENDA_B2)          # v2 §1.2: cada grade cobre a sua metade; emenda no meio do vão
        self.play(FadeIn(dU["g"]), FadeIn(dX["g"]), GrowFromPoint(dU["sx"], VU.P(0, 0)), GrowFromPoint(dU["sy"], VU.P(0, 0)),
                  GrowFromPoint(dX["sx"], VX.P(0, 0)), GrowFromPoint(dX["sy"], VX.P(0, 0)), run_time=0.8)
        self.pena(dU["lx"], dU["ly"], dX["lx"], dX["ly"], lag=0.05)
        self.gat("fi de u, vê igual")
        f1 = TC(r"(\X,\Y)=\varphi(\uu,\vv)", 150, 960, 40, "l")
        self.pena(f1)
        self.gat("de classe cê um")
        f2 = mixl([("m", r"\varphi"), ("t", "DE CLASSE"), ("m", r"C^1"), ("t", "NO ABERTO"), ("m", r"\Omega")], 600, 960, 34)
        self.pena(f2)
        # o retângulo A no plano u, v
        self.gat("um retângulo a")
        du_ = lin_px([VU.px(u0, .06), VU.px(u0, 1.1)], CU, 1.5, alpha=.7, dash=(6, 8), z=2)
        dv_ = lin_px([VU.px(.06, v0), VU.px(1.1, v0)], CVV, 1.5, alpha=.7, dash=(6, 8), z=2)
        cA = celula(VU, ID, u0, u1, v0, v1, n=3, wb=3)
        self.play(Create(du_), Create(dv_), *[Create(t[0]) for t in dU["tk"]], *anim_cel(cA), run_time=1.0)
        lA = TP("A", *VU.px((u0 + u1) / 2, (v0 + v1) / 2), 40, "c")
        self.pena(*[t[1] for t in dU["tk"]], lA, lag=0.1)
        # v2 Q03: u₀ CONSTANTE 12 px acima do topo da reta, à direita dela; v₀ CONSTANTE na ponta direita da tracejada, depois da célula
        ru = rotm([("m", r"\Uc{u_0}"), ("t", "CONSTANTE", GEO)], VU.px(u0, 1.1)[0] + 10, VU.px(u0, 1.1)[1] - 12 - 13, 26, "l")
        rv = rotm([("m", r"\Vc{v_0}"), ("t", "CONSTANTE", GEO)], VU.px(1.1, v0)[0] + 14, VU.px(1.1, v0)[1], 26, "l")
        self.pena(ru, rv, lag=0.2)
        self.gat("com lados delta u")
        ldu = rot_v(VU, r"\Du", ((u0 + u1) / 2, v0), 0, 16 + 15, 28, "c")       # v2 Q03: centrado, 16 px abaixo da aresta de baixo
        ldv = rot_v(VU, r"\Dv", (u1, (v0 + v1) / 2), 16, 0, 28, "l")
        self.pena(ldu, ldv, lag=0.2)
        # a imagem B = φ(A)
        self.gat("a imagem dele")
        ps, pl = phi_seta(780, 960, 250)
        f3 = TC(r"B=\varphi(A)", 1180, 960, 40, "l")
        self.play(Create(ps), run_time=0.6)
        self.pena(pl, f3, lag=0.3)
        # um ponto vai num ponto
        self.gat("um ponto vai num")
        pA = ponto_px(*VU.px(u0, v0), BR, 7)
        self.play(FadeIn(pA), run_time=0.3)
        pM = ponto_px(*VX.px(*mapC(u0, v0)), BR, 7)
        self.play(TransformFromCopy(pA, pM, path_arc=-1.0), run_time=1.4)
        # um lado vira uma curva, e o outro também
        self.gat("vira uma curva")
        sU = curva_v(VU, ID, u0, u1, v0, "u", CU)
        sX = curva_v(VX, mapC, u0, u1, v0, "u", CU)
        self.play(Create(sU), run_time=0.4)
        voa(self, sU, sX, rt=1.4, arco=-0.8, livre=(lA, ldu, ldv, ru, rv))
        self.gat("e o lado delta vê")
        tU = curva_v(VU, ID, v0, v1, u1, "v", CVV)
        tX = curva_v(VX, mapC, v0, v1, u1, "v", CVV)
        self.play(Create(tU), run_time=0.4)
        voa(self, tU, tX, rt=1.4, arco=-0.8, livre=(lA, ldu, ldv, ru, rv))
        # o retângulo inteiro vira o quadrilátero curvo MNPQ
        self.gat("e o retângulo inteiro")
        cB = celula(VX, mapC, u0, u1, v0, v1, n=3, wb=3)
        ivu = lin_px([VX.px(*mapC(u0, t)) for t in np.linspace(0, 1, 40)], CU, 1.5, alpha=.7, dash=(6, 8), z=2)
        ivv = lin_px([VX.px(*mapC(t, v0)) for t in np.linspace(0, 1, 40)], CVV, 1.5, alpha=.7, dash=(6, 8), z=2)
        voos(self, [(cA, cB), (du_, ivu, None), (dv_, ivv, None)], rt=1.8, arco=-0.8, seq=False, livre=(lA, ldu, ldv, ru, rv))      # um movimento só: a célula e as suas retas
        self.play(FadeOut(sU), FadeOut(tU), run_time=0.3)
        self.remove(sU, tU)
        ru2 = rotm([("m", r"\Uc{u_0}"), ("t", "CONSTANTE", GEO)], VX.px(*mapC(u0, 1))[0] - 8, VX.px(*mapC(u0, 1))[1] - 26, 26, "r")
        rv2 = rotm([("m", r"\Vc{v_0}"), ("t", "CONSTANTE", GEO)], VX.px(*mapC(1, v0))[0] + 12, VX.px(*mapC(1, v0))[1] - 22, 26, "l")
        self.pena(ru2, rv2, lag=0.2)
        self.gat("com cantos m")
        cs = {"M": (u0, v0, -36, -12), "N": (u1, v0, 28, 22), "P": (u1, v1, 24, -20), "Q": (u0, v1, -34, 18)}
        pts, labs = [], []
        for nome, (a, b, dx, dy) in cs.items():
            q = VX.px(*mapC(a, b))
            if nome != "M":
                pts.append(ponto_px(*q, BR, 6))
            labs.append(TC(nome, q[0] + dx, q[1] + dy, 30, "c"))
        self.play(*[FadeIn(p) for p in pts], run_time=0.4)
        self.pena(*labs, lag=0.15)
        self.gat("quanto vale a área")
        c_ = VX.px(*mapC((u0 + u1) / 2, (v0 + v1) / 2))
        lB = TP("B", 1490, 570, 40, "c")
        f4 = mixl([("t", "ÁREA DE"), ("m", r"B=?")], 1500, 960, 34)
        self.play(cB.fill.animate.set_fill(mixh(CHAPA, MALHA, .25)), run_time=0.6)
        self.pena(lB, f4, lag=0.3)
        self.marca("05")
        self.sai_fim()

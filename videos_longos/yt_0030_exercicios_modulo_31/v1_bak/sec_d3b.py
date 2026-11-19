"""Lote PD3B · D3b DUAS REGRAS (alvos 13, 14). 1) rot ∇φ: as três componentes em caneta, uma por vez; as mistas trocadas acendem em pares; = 0⃗ no
"tudo cancela"; legenda de Schwarz. No palco entra a sela (∇φ = (x, −y)) e o quadradinho deforma sem girar (alvo 13). 2) div(rot F⃗): as seis mistas
cancelam aos pares, = 0; no palco o giro rígido com o quadradinho que gira sem mudar de área (alvo 14). O teste (x sen y, cos y, z − xy): cada parcela
voa para a soma; NÃO EXISTE. div B = 0 ⇔ B = rot A. No fim, o C² da legenda de Schwarz acende em coral por 1 s."""
from lib30 import *  # noqa: F401,F403

C1, S1, T1 = (0.0, 0.0), 1.2, .55
C2, S2, T2 = (1.6, 0.0), 1.0, .6


def pinta(gs, cor):
    """cor=None devolve a cor original de cada glifo (guardada na primeira pintura)."""
    out = []
    for g in gs:
        if not hasattr(g, "_cor0"):
            g._cor0 = g.get_fill_color()
        c = g._cor0 if cor is None else cor
        out.append(g.animate.set_fill(c).set_stroke(c))
    return out


class LoteD3b(Base):
    ANTES = "A FAMÍLIA DE REDEMOINHOS · GIRO DE 90°"

    def corpo(self):
        # ── D3b-1 · um gradiente nunca gira ──
        self.an("D3b-1")
        self.secao("DUAS REGRAS · UM GRADIENTE NUNCA GIRA")
        zera_chapas()
        chA = chapa_px(*LA, nome="D3b palco A", v=VA)
        troca(self, "D3 → D3b (palco)")
        R = Pz([r"\rot\,\nabla\varphi=(", r"\varphi_{zy}", "-", r"\varphi_{yz}", r",\ ", r"\varphi_{xz}", "-", r"\varphi_{zx}", r",\ ",
                r"\varphi_{yx}", "-", r"\varphi_{xy}", ")"], 1110, 440, 34, caneta=False)
        sub = lambda *ii: VGroup(*[R[0][g] for i in ii for g in R._rg[i]])
        self.play(FadeIn(chA), run_time=0.6)
        self.gat("calcula o rotacional")
        self.play(caneta(sub(0), ritmo=0.4))
        self.gat("a primeira componente é")
        self.play(caneta(sub(1, 2, 3, 4), ritmo=0.5))
        self.gat("e as outras duas componentes")
        self.play(caneta(sub(5, 6, 7, 8), ritmo=0.4))
        self.play(caneta(sub(9, 10, 11, 12), ritmo=0.4))
        self.remove(*[m for m in self.mobjects if isinstance(m, VGroup) and len(m) and all(g in R[0].submobjects for g in m.submobjects)])
        self.add(R)
        self.gat("as derivadas mistas são iguais")
        for a, b in ((1, 3), (5, 7), (9, 11)):
            self.play(*pinta(sub(a, b), AMB), run_time=0.3)
            self.play(*pinta(sub(a, b), None), run_time=0.3)
        zz = TC(r"=\V{\vec 0}", 1120, 540, 46)
        self.gat("tudo cancela")
        self.play(caneta(zz, ritmo=0.5))
        sw = leg_mix(["SCHWARZ:", r"$\varphi$", "DE CLASSE", "C²", r"$\Rightarrow$", "MISTAS IGUAIS"], 1124, 640, GEO, "left", 26, gap=9)
        self.play(FadeIn(sw, shift=0.05 * UP), run_time=0.4)
        self.ate(1.0)

        # ── D3b-2 · a sela do EP. 03 (alvo 13) ──
        self.an("D3b-2")
        ped = quad30(VA, C1, S1)
        fan = fantasma(VA, quad_pts(C1, S1))
        sela = campo30(VA, F_SELA, mmax=3, rmin=0, nome="D3b sela")
        clareira(sela, lambda: ou(clar_ped(ped), dq(C1, S1)))
        ep = legenda("O CAMPO QUE ESTICAVA O QUADRADINHO NO EP. 03", 1124, 690, GEO, "left", 24)
        self.gat("lembra do campo que esticava")
        self.play(cresce_campo(sela, 1.0), FadeIn(ped), FadeIn(fan), FadeIn(ep, shift=0.05 * UP), run_time=1.0)
        ph = TC(r"\varphi=\tfrac12(\X^2-\Y^2),\quad \nabla\varphi=(\X,\ -\Y)", 1120, 300, 40)
        self.gat("ele é o gradiente da metade")
        self.play(caneta(ph, ritmo=0.35))
        self.gat("por isso o quadradinho deformava")
        a0 = ped.area()
        self.play(anda(ped, fl_sela, T1, 2.0, rate=linear, nome="D3b sela"))
        print(f"[D3b] sela: área {a0:.4f} → {ped.area():.4f}")
        dm = T("DEFORMA, MAS NÃO GIRA", 1120, 760, 40, cor=LIMA)
        self.play(FadeIn(dm, shift=0.05 * UP), run_time=0.4)
        self.ate(1.0)

        # ── D3b-3 · um rotacional nunca diverge (alvo 14) ──
        self.an("D3b-3")
        self.secao("DUAS REGRAS · UM ROTACIONAL NUNCA DIVERGE")
        sela.clear_updaters()
        col = [R, zz, ph, ep, dm]
        sw.save_state()
        p2 = quad30(VA, C2, S2)
        f2 = fantasma(VA, quad_pts(C2, S2))
        giro = campo30(VA, F_GIRO, mmax=4, rmin=0, nome="D3b giro")
        clareira(giro, lambda: ou(clar_ped(p2), dq(C2, S2)))
        o0 = ponto7(VA.c2p(0, 0), GEO, 6, 8)
        troca(self, "D3b sela → giro (palco)")
        self.play(*[FadeOut(m) for m in col + [sw, ped, fan]], FadeOut(sela), cresce_campo(giro, 0.8), FadeIn(p2), FadeIn(f2), FadeIn(o0), run_time=0.8)
        self.remove(*col, sw, ped, fan, sela)
        D1_ = Pz([r"\dv(\rot\F)=", r"(\R_{yx}", "-", r"\R_{xy})", "+", r"(\Pp_{zy}", "-", r"\Pp_{yz})"], 1110, 270, 34)
        D2a = Pz(["+", r"(\Qq_{xz}", "-", r"\Qq_{zx})"], 1250, 335, 34)
        D2b = Pz(["+", r"(\Qq_{xz}", "-", r"\Qq_{zx})", r"=\D0"], 1250, 335, 34, caneta=False)
        self.gat("calcula o rotacional de um campo")
        self.play(caneta(D1_, ritmo=0.35))
        self.play(caneta(D2a, ritmo=0.35))
        self.gat("elas se cancelam aos pares")
        s1 = lambda m, *ii: VGroup(*[m[0][g] for i in ii for g in m._rg[i]])
        for m, a, b in ((D1_, 1, 3), (D1_, 5, 7), (D2a, 1, 3)):
            self.play(*pinta(s1(m, a, b), CORAL), run_time=0.3)
            self.play(*pinta(s1(m, a, b), None), run_time=0.25)
        self.play(tbgm30(D2a, D2b, [(i, i) for i in range(4)], rt=0.8))
        self.remove(D2a)
        limpa_soltos(self)
        self.add(D2b)
        self.gat("um rotacional nunca diverge")
        a0 = p2.area()
        self.play(anda(p2, fl_giro, T2, 1.6, rate=linear, nome="D3b giro rígido"))
        print(f"[D3b] giro: área {a0:.4f} → {p2.area():.4f}")
        npal = legenda("NO PALCO: GIRA SEM MUDAR DE ÁREA", 1124, 815, GEO, "left", 24)
        self.play(FadeIn(npal, shift=0.05 * UP), run_time=0.4)
        self.ate(1.0)

        # ── D3b-4 · o teste ──
        self.an("D3b-4")
        ex = T("EXISTE UM CAMPO G COM", 1120, 430, 32)
        G = Pz([r"\rot\Gg=(", r"\X\operatorname{sen}\Y", r",\ ", r"\cos\Y", r",\ ", r"\Z-\X\Y", r")\ ?"], 1120, 495, 38)
        DV = Pz([r"\dv=", r"\operatorname{sen}\Y", r"-\operatorname{sen}\Y", r"+1", r"=\D{1}\neq 0"], 1120, 590, 38, caneta=False)
        sg = lambda m, *ii: VGroup(*[m[0][g] for i in ii for g in m._rg[i]])
        self.gat("existe outro campo cujo rotacional")
        self.play(FadeIn(ex, shift=0.05 * UP), caneta(G, ritmo=0.3), run_time=1.6)
        self.gat("calcula o divergente")
        self.play(caneta(sg(DV, 0), ritmo=0.5))
        for fr, src, dst in (("a primeira parcela dá seno", 1, 1), ("a segunda dá menos seno", 3, 2), ("e a terceira dá um", 5, 3)):
            self.gat(fr)
            self.play(TransformFromCopy(sg(G, src), sg(DV, dst)), run_time=0.8)
        self.gat("total um")
        self.play(caneta(sg(DV, 4), ritmo=0.4))
        self.remove(*[m for m in self.mobjects if isinstance(m, VGroup) and len(m) and all(g in DV[0].submobjects for g in m.submobjects)])
        self.add(DV)
        ne = T("NÃO EXISTE", 1120, 690, 44, cor=CORAL)
        self.gat("então não existe")
        self.play(FadeIn(ne, shift=0.05 * UP), run_time=0.4)
        self.ate(1.0)

        # ── D3b-5 · na física ──
        self.an("D3b-5")
        bb = leg_mix(["div B = 0 ", r"$\Leftrightarrow$", " B = rot A (NO ESPAÇO TODO)"], 1124, 860, CAMPO2, "left", 24)
        self.gat("no espaço todo isso permite")
        self.play(FadeIn(bb, shift=0.05 * UP), run_time=0.4)
        tr = legenda("TODO ROTACIONAL TEM DIVERGENTE ZERO", 1124, 770, GEO)
        self.gat("todo rotacional tem divergente zero")
        self.play(FadeIn(tr, shift=0.05 * UP), run_time=0.4)
        self.ate(1.0)

        # ── D3b-6 · a hipótese C² (puxa o D4) ──
        self.an("D3b-6")
        sw2 = leg_mix(["SCHWARZ:", r"$\varphi$", "DE CLASSE", "C²", r"$\Rightarrow$", "MISTAS IGUAIS"], 1124, 905, GEO, "left", 24, gap=9)
        self.gat("e repara na hipótese")
        self.play(FadeIn(sw2, shift=0.05 * UP), run_time=0.4)
        c2 = sw2[3]
        self.gat("classe cê dois sem")
        self.play(c2.animate.set_color(CORAL), run_time=0.25)
        self.wait(1.0)
        self.play(c2.animate.set_color(GEO), run_time=0.25)
        giro.clear_updaters()
        self.sai_fim()

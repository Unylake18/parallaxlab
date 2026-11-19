"""Lote PA1 · P2 transição (PARTE 2 · AS APLICAÇÕES + ÁGUA DE VERDADE / LEIS DA FÍSICA) + A1 O RIO · v2 (alvo v2_a1 + 23 v1). Margens em x = ±3
(recortadas); perfil, depois a rede; v = (0, 1 − x²/9) em caneta, o 1 acende com a seta do meio, x = ±3 dá zero (rótulos v = 0⃗ e x = ±3 nas margens).
Molde J → valores; div e rot pela fórmula-mãe com voo das células; x = −3: rot = 2/3 (o −3 voa do rótulo); ω = rot/2 = 1/3 rad/s; T = 2π/ω = 6π ≈ 19 s;
três quadradinhos; as setas das bordas acendem; d₁ e d₂ com voo."""
from alg30 import *  # noqa: F401,F403

CS = [(-2.4, -1.6), (0.0, -1.6), (2.4, -1.6)]
SR, TR = .9, 1.2
dPx, dPy, dQx, dQy = r"\Pp_{\Am{x}}", r"\Pp_{\Mg{y}}", r"\Qq_{\Am{x}}", r"\Qq_{\Mg{y}}"


def margens():
    g = VGroup()
    for X in (-3, 3):
        g.add(linha_rec(VA, [(X, -3.2), (X, 3.2)], LA, GEO, 5))
        for k in range(16):
            Y = -2.9 + .4 * k
            g.add(linha_rec(VA, [(X, Y), (X + (-.25 if X < 0 else .25), Y - .25)], LA, GEO, 2, .6))
    return g.set_z_index(5)


class LoteA1(Base):
    ANTES = None

    def corpo(self):
        # ── P2 · PARTE 2 ──
        self.an("P2-1")
        p1 = T("PARTE 2", 960, 500, 28, "center", GEO, bold=False)
        p2 = T("AS APLICAÇÕES", 960, 580, 54, "center")
        troca(self, "D5 → P2 (tela de passagem)")
        self.play(FadeIn(p1, shift=0.05 * UP), run_time=0.5)
        self.gat("agora vem a melhor parte")                     # R16: o nome da parte entra na fala
        self.play(FadeIn(p2, shift=0.05 * UP), run_time=0.6)
        aq = legenda("ÁGUA DE VERDADE", 960, 660, CAMPO2, "center", 30)
        lf = legenda("LEIS DA FÍSICA", 960, 710, SAIC, "center", 30)
        self.gat("água de verdade")
        self.play(FadeIn(aq, shift=0.05 * UP), run_time=0.4)
        self.gat("leis da física")
        self.play(FadeIn(lf, shift=0.05 * UP), run_time=0.4)
        self.ate(1.0)

        # ── A1-1 · o canal; v; zero nas margens ──
        self.an("A1-1")
        self.secao("APLICAÇÃO · O RIO")
        zera_chapas()
        chA = chapa_px(*LA, nome="A1 palco", v=VA)
        mg = margens()
        peds = [quad30(VA, c, SR) for c in CS]
        fans = [fantasma(VA, quad_pts(c, SR)) for c in CS]
        st = {"q": False, "g": []}
        rede = campoP30(VA, RIO, -2.5, 2.5, passo=.5, rmin=0, mref=1, nome="A1 rio")
        perfil = VGroup(*[s for s in rede if abs(s._xy[1] + 2.5) < 1e-6])
        resto = VGroup(*[s for s in rede if abs(s._xy[1] + 2.5) >= 1e-6])
        en = leg_mix(["CANAL DE 6 m · 1 m/s NO MEIO · ZERO NAS MARGENS"], 1124, 348, GEO, "left", 28)
        self.limpa_junto()
        troca(self, "P2 → A1 (palco do rio)")
        self.play(FadeIn(chA), Create(mg), run_time=0.8)
        self.play(FadeIn(en, shift=0.05 * UP), run_time=0.4)
        self.gat("a água corre a um metro")
        self.play(cresce_campo(perfil, 0.6, chave=lambda s: s._xy[0]))
        VL_ = L([("v", r"\vv=\Big(0,\ "), ("um", "1"), ("m", r"-\dfrac{\X^2}{9}"), ("f", r"\Big)")], 1120, 270, 34)
        self.gat("numa parábola")
        self.play(cresce_campo(resto, 0.8, chave=lambda s: s._xy[1]))
        clareira(rede, lambda: ou(*([clar_ped(p) for p in peds] + [dq(c, SR) for c in CS] if st["q"] else []), *st["g"]))
        self.gat("a componente na direção do canal")
        escreve(self, VL_, 0.3)
        meio = [s for s in rede if abs(s._xy[0]) < 1e-6]
        self.gat("no meio dá um")
        acende(self, [VL_.p("um"), *meio], CAMPO2, 0.9)
        v0e, v0d = rot(r"\vv=\vec0", *canto_xy(VA, -2.62, 2.6), 28), rot(r"\vv=\vec0", *canto_xy(VA, 2.62, 2.6), 28)
        xe, xd = rot(r"\X=-3", *canto_xy(VA, -2.6, -2.62), 26), rot(r"\X=3", *canto_xy(VA, 2.62, -2.62), 26)
        V2 = L([("v", r"\vv=\Big(0,\ "), ("um", "1"), ("m", r"-\dfrac{\X^2}{9}"), ("f", r"\Big)"), ("x3", r"\qquad \X=\pm3:\ "), ("z", r"1-\dfrac99=0")], 1120, 270, 34)
        self.gat("nas margens a três metros")
        gm(self, VL_, V2, rt=0.7)
        cant = [s for s in rede if abs(abs(s._xy[0]) - 2.5) < 1e-6 and abs(abs(s._xy[1]) - 2.5) < 1e-6]   # R5: as 4 setas sob as etiquetas
        self.play(*[UpdateFromAlphaFunc(s, lambda m, a: op_seta(m, 1 - a)) for s in cant], run_time=0.3)
        st["g"].append(lambda X, Y: abs(abs(X) - 2.5) < 1e-6 and abs(abs(Y) - 2.5) < 1e-6)
        for r_ in (v0e, v0d, xe, xd):
            self.add(r_[0])
            r_.f._origem = "a"
        self.play(*[caneta(r_.f, ritmo=0.3) for r_ in (v0e, v0d, xe, xd)], run_time=0.6)
        self.gat("um menos nove nonos")                          # R16: o zero das margens citado acende; depois as margens (o atrito)
        acende(self, [V2.p("z")], CAMPO2, 1.0)
        self.gat("onde o atrito é maior")
        acende(self, [mg], CORAL, 0.8)
        self.gat("pausa o vídeo e tenta")
        self.pausa()
        self.ate(1.0)

        # ── A1-2 · a tabela; incompressível ──
        self.an("A1-2")
        Jm = TC(r"J=\begin{pmatrix}%s & %s\\ %s & %s\end{pmatrix}" % (dPx, dPy, dQx, dQy), 1120, 390, 34)
        self.gat("primeira a velocidade só tem")
        self.play(FadeOut(en), run_time=0.3)
        self.remove(en)
        escreve(self, Jm, 0.25)
        Jv = TC(r"=\begin{pmatrix}\Am0 & \Mg0\\ \Am{-\frac{2x}{9}} & \Mg0\end{pmatrix}", Jm.get_right()[0] * 120 + 960 + 10, 390, 34, caneta=True)
        self.gat("e ela não muda ao longo do canal")
        escreve(self, Jv, 0.3)
        cel, _ = celulas(Jv)
        DV = L([("n", r"\D{\dv}="), ("f", dPx + "+" + dQy)], 1120, 490, 34)
        self.gat("divergente zero incompressível")
        escreve(self, DV, 0.25)
        DV2 = L([("n", r"\D{\dv}="), ("f", dPx + "+" + dQy), ("e", "="), ("a", "0"), ("op", "+"), ("b", "0"), ("r", r"=\D0")], 1120, 490, 34)
        gm(self, DV, DV2, rt=0.5, voos={"a": cel[(0, 0)], "b": cel[(1, 1)]})
        self.ate(1.0)

        # ── A1-3 · o rotacional; o galho ──
        self.an("A1-3")
        RT = L([("n", r"\V{\rot}="), ("f", dQx + "-" + dPy)], 1120, 570, 34)
        self.gat("o rotacional é a derivada")
        escreve(self, RT, 0.25)
        RT2 = L([("n", r"\V{\rot}="), ("f", dQx + "-" + dPy), ("e", "="), ("a", r"-\dfrac{2\X}{9}"), ("op", "-"), ("b", "0"), ("r", r"=\V{-\dfrac{2\X}{9}}")], 1120, 570, 34)
        self.gat("dá menos dois nonos")
        gm(self, RT, RT2, rt=0.7, voos={"a": cel[(1, 0)], "b": cel[(0, 1)]})
        XR = L([("x", r"\X=-3:\ "), ("r", r"\V{\rot}=\V{\tfrac23}")], 1120, 655, 34)
        self.gat("na margem esquerda menos dois nonos")
        voa(self, xe.f, XR.p("x"), rt=0.5)
        escreve_p(self, XR, ["r"], 0.3)
        junta(self, XR, "b")
        self.gat("um galho ali gira")                            # R16: o rotacional da margem e depois o "rot" citados acendem
        acende(self, [XR.p("r")], VIO, 1.0)
        self.gat("lembra que o rotacional é o dobro")
        acende(self, [RT2.p("n")], VIO, 1.0)
        OM = L([("w", r"\omega=\dfrac{\rot}{2}=\dfrac13\ \text{rad/s}"), ("T", r",\quad T=\dfrac{2\pi}{\omega}=6\pi\approx19\ \text{s}")], 1120, 745, 34)
        self.gat("o galho gira a um terço")
        escreve_p(self, OM, ["w"], 0.2)
        self.gat("dois pi dividido por um terço")
        escreve_p(self, OM, ["T"], 0.2)
        junta(self, OM)
        XR2 = L([("x", r"\X=-3:\ "), ("r", r"\V{\rot}=\V{\tfrac23}"), ("x2", r"\qquad \X=3:\ "), ("r2", r"\V{\rot}=\V{-\tfrac23}")], 1120, 655, 34)
        self.gat("na margem direita menos dois terços")
        gm(self, XR, XR2, rt=0.6, voos={"x2": xd.f})
        self.ate(1.0)

        # ── A1-4 · os três quadradinhos; as bordas ──
        self.an("A1-4")
        self.gat("olha os três quadradinhos")
        st["q"] = True
        self.play(*[FadeIn(p) for p in peds], *[FadeIn(f) for f in fans], run_time=0.5)
        a0 = [p.area() for p in peds]
        self.play(*[anda(p, flRio, TR, 2.0, rate=linear, nome=f"A1 quadradinho {CS[i]}") for i, p in enumerate(peds)])
        for i, p in enumerate(peds):
            print(f"[A1] quadradinho {CS[i]}: área {a0[i]:.4f} → {p.area():.4f}")
        gs = []
        for c, ccw in ((CS[0], True), (CS[2], False)):
            Fc = ponto_fl(flRio, c, TR)
            gs.append(giro30(VA, Fc, .78, ccw))
            st["g"].append(clarPoly(circ_pts(.85, Fc, 12), .05))
        self.gat("cada um para um lado")
        self.play(*[Create(g) for g in gs], run_time=0.4)
        borda = [s for s in rede if abs(s._xy[1] - .5) < 1e-6 and s._xy[0] in (-2.5, -2.0)]
        self.gat("a água do lado de dentro corre")
        self.play(recolore(self, rede, lambda s: s not in borda), run_time=0.4)
        self.wait(2.0)
        self.play(recolore(self, rede, lambda s: False), run_time=0.4)
        self.ate(1.0)

        # ── A1-5 · o atrito ──
        self.an("A1-5")
        self.gat("terceira o atrito")                            # R13: ω e T (o galho) voltam para o rotacional da margem; R16: as margens acendem
        XR3 = L(list(zip(XR2.ks, XR2.ts)), 0, 0, XR2.size).move_to(XR2.get_center())
        AO = Duas(XR2, OM)
        AO.ks = list(XR2.ks) + ["r"] * len(OM.ks)
        gm(self, AO, XR3, rt=0.6, nota="(R13: ω e T voltam para o rotacional)")
        self.remove(XR2, OM)
        acende(self, [mg], CORAL, 1.0)
        self.gat("o atrito viscoso vem da deformação")
        acende(self, [mg], LIMA, 1.0)
        viz_m = [s for s in rede if abs(s._xy[1] - 1.5) < 1e-6 and s._xy[0] in (-2.5, -2.0)]
        viz_c = [s for s in rede if abs(s._xy[1] - 1.5) < 1e-6 and s._xy[0] in (-.5, 0.0)]
        self.gat("da diferença de velocidade entre camadas")
        self.play(recolore(self, rede, lambda s: s not in viz_m), run_time=0.3)
        self.wait(0.8)
        self.play(recolore(self, rede, lambda s: s not in viz_c), run_time=0.3)
        self.wait(0.8)
        self.play(recolore(self, rede, lambda s: False), run_time=0.3)
        DD = L([("a", r"d_1="), ("af", dPx + "-" + dQy), ("av", r"=\Lm0"), ("sp", r",\quad "), ("b", r"d_2="), ("bf", dQx + "+" + dPy), ("bv", r"=\Lm{-\dfrac{2\X}{9}}")],
               1120, 840, 34)
        self.gat("aqui a primeira deformação")
        escreve_p(self, DD, ["a", "af", "sp", "b", "bf"], 0.15)
        voa(self, VGroup(cel[(0, 0)], cel[(1, 1)]), DD.p("av"), rt=0.5, extra=[TransformFromCopy(cel[(1, 0)], DD.p("bv"))])
        junta(self, DD, "b")
        at = legenda("ATRITO VISCOSO: MÁXIMO NAS MARGENS", 1124, 910, LIMA, "left", 26)
        self.gat("máxima nas margens")
        self.play(FadeIn(at, shift=0.05 * UP), run_time=0.4)
        rede.clear_updaters()
        self.sai_fim()

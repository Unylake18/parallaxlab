"""Lote PA1 · P2 transição (PARTE 2 · AS APLICAÇÕES + ÁGUA DE VERDADE / LEIS DA FÍSICA) + A1 O RIO · v2 (alvo v2_a1 + 23 v1). Margens em x = ±3
(recortadas); perfil, depois a rede; v = (0, 1 − x²/9) em caneta, o 1 acende com a seta do meio, x = ±3 dá zero (rótulos v = 0⃗ e x = ±3 nas margens).
Molde J → valores; div e rot pela fórmula-mãe com voo das células; x = −3: rot = 2/3 (o −3 voa do rótulo); ω = rot/2 = 1/3 rad/s; T = 2π/ω = 6π ≈ 19 s;
três quadradinhos; as setas das bordas acendem; d₁ e d₂ com voo."""
from escada30 import *  # noqa: F401,F403

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
        self.an("P2-1")                                            # v3: a escada da abertura volta (Parte 1 a 100 %, Parte 2 a 45 %)
        self.secao("PARTE 2")                                      # C4 (final): a linha 2 do canto também na passagem
        D = [Degrau(i, 1, "ab") for i in range(6)]
        Ap = [Degrau(i, 2, "ab", .45) for i in range(4)]
        e1, e2 = titulos_escada()
        troca(self, "D5 → P2 (a escada volta)")
        self.play(*[FadeIn(d) for d in D], *[FadeIn(a) for a in Ap], FadeIn(e1), FadeIn(e2), run_time=0.7)
        self.gat("agora vem a melhor parte")
        acende(self, [e2], BR, 1.0)
        self.gat("água de verdade")
        self.play(*[UpdateFromAlphaFunc(Ap[i], lambda m, a: m.opacidade(.45 + .55 * a)) for i in range(3)], run_time=0.5)
        self.gat("leis da física")
        self.play(UpdateFromAlphaFunc(Ap[3], lambda m, a: m.opacidade(.45 + .55 * a)), run_time=0.5)
        alvo = RoundedRectangle(width=(LA[2] - LA[0]) / 120, height=(LA[3] - LA[1]) / 120, corner_radius=8 / 120).move_to(PX((LA[0] + LA[2]) / 2,
                                                                                                                              (LA[1] + LA[3]) / 2))
        alvo.set_fill(PLACA_V4, 0.92).set_stroke(VEL, 3 / 1.2, 1)
        self.gat("vamos começar por um rio")                      # a caixa do rio cresce até virar o palco do A1
        resto = [*D, *Ap[1:], Ap[0].ic, Ap[0].rot, e1, e2]
        self.play(Transform(Ap[0].caixa, alvo), *[FadeOut(m) for m in resto], run_time=0.9)
        self.remove(*resto)
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
        self.gat("e ela não muda ao longo do canal")
        acende(self, meio, CAMPO2, 0.8)
        # v4 C9: a tabela do rio pelas derivadas, célula a célula (deriva_cel, o mesmo caminho do D5)
        Jv = TC(r"=\begin{pmatrix}\Am0 & \Mg0\\ \Am{-\frac{2x}{9}} & \Mg0\end{pmatrix}", Jm.get_right()[0] * 120 + 960 + 10, 390, 34, caneta=False)
        cel, restoJ = celulas(Jv)
        self.gat("monta a tabela pelas derivadas")
        escreve(self, Jm, 0.2)
        print(f"[origem] a {self.lote} A1-2 {self.t:.2f} 'parênteses da J' (resto)")
        self.play(caneta(restoJ, ritmo=0.25))
        zero_v = V2.p("v")[-2]                                         # o 0 de v = (0, …)
        UM = [("u", "1"), ("mn", "-"), ("fr", r"\dfrac{\X^2}{9}")]
        vals = []
        self.gat("a primeira componente é zero")
        vals.append(deriva_cel(self, zero_v, cel[(0, 0)], 0, [("z", "0")], [("z", r"\Am0")], ["z"], x_mid=1680))
        vals.append(deriva_cel(self, zero_v, cel[(0, 1)], 1, [("z", "0")], [("z", r"\Mg0")], ["z"], x_mid=1680))
        self.gat("a segunda um menos xis")
        vals.append(deriva_cel(self, V2.p("um", "m"), cel[(1, 1)], 1, UM, [("z", r"\Mg0")], ["z", "z", "z"], some=("u", "mn", "fr"), x_mid=1680))
        self.gat("em xis o um some")
        vals.append(deriva_cel(self, V2.p("um", "m"), cel[(1, 0)], 0, UM, [("v", r"\Am{-\frac{2x}{9}}")], None, some=("u",), x_mid=1680,
                               inter=([("z0", "0"), ("mn", "-"), ("fr", r"\dfrac{2\X}{9}")], ["z0", "mn", "fr"], ["z", "v", "v"])))
        self.remove(*vals)
        junta(self, Jv, "b")
        DV = L([("n", r"\D{\dv}="), ("f", dPx + "+" + dQy)], 1120, 490, 34)
        DV2 = L([("n", r"\D{\dv}="), ("f", dPx + "+" + dQy), ("e", "="), ("a", "0"), ("op", "+"), ("b", "0"), ("r", r"=\D0")], 1120, 490, 34)
        self.gat("divergente zero mais zero")
        escreve(self, DV, 0.2)
        gm(self, DV, DV2, rt=0.5, voos={"a": cel[(0, 0)], "b": cel[(1, 1)]})
        self.gat("divergente zero incompressível")
        acende(self, [DV2.p("r")], CAMPO2, 0.8)
        self.ate(1.0)

        # ── A1-3 · o rotacional; o galho ──
        self.an("A1-3")
        DVc = L([("n", r"\D{\dv}="), ("r", r"\D0")], 1600, 390, 30)       # v4 C9 (R13): o div vira chip ao lado da J
        gm(self, DV2, DVc, rt=0.5, ka=["n", "z", "z", "z", "z", "z", "r"], nota="(R13: div = 0 vira chip)")
        RT = L([("n", r"\V{\rot}="), ("f", dQx + "-" + dPy)], 1120, 490, 34)
        self.gat("o rotacional é a derivada")
        escreve(self, RT, 0.25)
        self.gat("menos a derivada da primeira componente")
        acende(self, [cel[(0, 1)]], CAMPO2, 0.7)
        RT2 = L([("n", r"\V{\rot}="), ("f", dQx + "-" + dPy), ("e", "="), ("a", r"-\dfrac{2\X}{9}"), ("op", "-"), ("b", "0"), ("r", r"=\V{-\dfrac{2\X}{9}}")], 1120, 490, 34)
        self.gat("dá menos dois nonos")
        gm(self, RT, RT2, rt=0.7, voos={"a": cel[(1, 0)], "b": cel[(0, 1)]})
        # v4 C10: rot(−3) com a substituição; −2(−3)/9 = 6/9 = 2/3
        m3 = VGroup(*xe.f[0][2:4])                                     # o −3 do rótulo x = −3
        XR = L([("r", r"\V{\rot}("), ("v", "-3"), ("p", ")="), ("fa", r"\dfrac{", 0), ("n1", "-2("), ("v2", "-3"), ("n2", ")"), ("fb", "}{", 1), ("d", "9"),
                ("fc", "}", 0)], 1120, 575, 34)
        self.gat("na margem esquerda menos dois nonos")
        escreve_p(self, XR, ["r"], 0.15)
        voa(self, m3, XR.p("v"), rt=0.45)
        escreve_p(self, XR, ["p", "n1", "fb", "d"], 0.12)
        voa(self, m3, XR.p("v2"), rt=0.45)
        escreve_p(self, XR, ["n2"], 0.15)
        junta(self, XR, "b")
        XRb = L([("r", r"\V{\rot}("), ("v", "-3"), ("p", ")="), ("fa", r"\dfrac{", 0), ("n1", "6"), ("fb", "}{", 1), ("d", "9"), ("fc", "}", 0)], 1120, 575, 34)
        self.gat("menos com menos dá mais")
        gm(self, XR, XRb, rt=0.7, ka=["r", "v", "p", "fa", "n1", "n1", "n1", "fb", "d", "fc"], nota="(−2·(−3) = 6)")
        XRc = L([("r", r"\V{\rot}("), ("v", "-3"), ("p", ")="), ("fa", r"\dfrac{", 0), ("n1", r"\V{2}"), ("fb", "}{", 1), ("d", r"\V{3}"), ("fc", "}", 0)], 1120, 575, 34)
        self.gat("que simplifica para dois terços")
        acende(self, [XRb.p("n1", "d")], AMB, 0.5)
        gm(self, XRb, XRc, rt=0.6, nota="(6/9 = 2/3, ÷3)")
        self.gat("um galho ali gira")                            # R16: o rotacional da margem e depois o "rot" citados acendem
        acende(self, [XRc.p("n1", "fb", "d")], VIO, 1.0)
        self.gat("lembra que o rotacional é o dobro")
        acende(self, [RT2.p("n")], VIO, 1.0)
        OM1 = L([("w", r"\omega="), ("a", r"\dfrac{\rot}{2}"), ("b", r"=\dfrac{2/3}{2}"), ("c", r"=\dfrac13"), ("u", r"\ \text{rad/s}")], 1120, 660, 34)
        self.gat("o galho gira com ômega")                         # leitura 17: ω
        escreve_p(self, OM1, ["w", "a"], 0.15)
        le(self, OM1.p("w")[0], 17, "ômega, a velocidade angular", ate="igual a um terço")
        bb = OM1.p("b")                                                # = 2 / 3 — 2
        self.play(caneta(VGroup(bb[0], *bb[4:]), ritmo=0.15))
        voa(self, XRc.p("n1", "fb", "d"), VGroup(*bb[1:4]), rt=0.45)    # o 2/3 voa de XR
        escreve_p(self, OM1, ["c", "u"], 0.15)
        junta(self, OM1, "b")
        OM2 = L([("T", r"T="), ("a", r"\dfrac{2\pi}{\omega}"), ("b", r"=\dfrac{2\pi}{1/3}"), ("c", r"=2\pi\cdot3"), ("d", r"=6\pi"), ("e", r"\approx18{,}8\approx19\ \text{s}")],
                1120, 745, 34)
        self.gat("e o período o t da tela")                        # leitura 18: T
        escreve_p(self, OM2, ["T", "a"], 0.15)
        le(self, OM2.p("T")[0], 18, "o período, o T da tela, o tempo de uma volta", ate="dois pi dividido por um terço")
        b2 = OM2.p("b")                                                # = 2 π — 1 / 3
        self.gat("que é dois pi vezes três")
        self.play(caneta(VGroup(*b2[0:4]), ritmo=0.12))
        voa(self, VGroup(*OM1.p("c")[1:]), VGroup(*b2[4:]), rt=0.45)   # o 1/3 voa de OM1
        escreve_p(self, OM2, ["c", "d"], 0.15)
        self.gat("com pi perto de três vírgula catorze")
        escreve_p(self, OM2, ["e"], 0.12)
        junta(self, OM2, "b")
        XR2 = L([("r", r"\V{\rot}("), ("v", "-3"), ("p", ")="), ("fa", r"\dfrac{", 0), ("n1", r"\V{2}"), ("fb", "}{", 1), ("d", r"\V{3}"), ("fc", "}", 0),
                 ("vg", r",\quad "), ("r2", r"\V{\rot}("), ("v3", "3"), ("p2", ")=")], 1120, 575, 30)
        self.gat("na margem direita menos dois terços")
        gm(self, XRc, XR2, rt=0.6, voos={"v3": VGroup(*xd.f[0][2:])}, nota="(x = 3 na margem direita)")
        XR2b = L(list(zip(XR2.ks, XR2.ts, XR2.ns)) + [("f2", r"\dfrac{-2\cdot3}{9}"), ("g2", r"=\V{-\tfrac23}")], 1120, 575, 30)
        self.gat("porque agora é menos dois nonos")
        gm(self, XR2, XR2b, rt=0.6, nota="(−2·3/9 = −2/3)")
        XR3f = L(list(zip(XR2b.ks, XR2b.ts, XR2b.ns)) + [("vg2", r",\quad "), ("r3", r"\V{\rot}(0)=\V0")], 1120, 575, 30)
        self.gat("bem no centro com xis zero")
        gm(self, XR2b, XR3f, rt=0.5, extra=[pisca_cor(VGroup(*meio), CAMPO2, 0.8)], nota="(no centro, rot = 0)")
        XR = XR3f
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
        XR3 = L(list(zip(XR.ks, XR.ts, XR.ns)), 0, 0, XR.size).move_to(XR.get_center())
        AO = Duas(XR, OM1, OM2)
        AO.ks = list(XR.ks) + ["r"] * (len(OM1.ks) + len(OM2.ks))
        gm(self, AO, XR3, rt=0.6, nota="(R13: ω e T voltam para o rotacional)")
        self.remove(XR, OM1, OM2)
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
        # v4 C11: d₁ e d₂ em duas linhas com os valores, e d₂ nas margens e no centro
        DD1 = L([("a", r"d_1="), ("af", dPx + "-" + dQy), ("e", "="), ("x", "0"), ("m", "-"), ("y", "0"), ("r", r"=\Lm0")], 1120, 660, 32)
        self.gat("aqui a primeira deformação")
        escreve_p(self, DD1, ["a", "af", "e", "m"], 0.12)
        voa(self, cel[(0, 0)], DD1.p("x"), rt=0.4, extra=[TransformFromCopy(cel[(1, 1)], DD1.p("y"))])
        escreve_p(self, DD1, ["r"], 0.15)
        junta(self, DD1, "b")
        DD2 = L([("b", r"d_2="), ("bf", dQx + "+" + dPy), ("e", "="), ("x", r"-\dfrac{2\X}{9}"), ("p", "+"), ("y", "0"), ("r", r"=\Lm{-\dfrac{2\X}{9}}")], 1120, 745, 32)
        self.gat("a segunda é menos dois nonos")
        escreve_p(self, DD2, ["b", "bf", "e", "p"], 0.12)
        voa(self, cel[(1, 0)], DD2.p("x"), rt=0.4, extra=[TransformFromCopy(cel[(0, 1)], DD2.p("y"))])
        escreve_p(self, DD2, ["r"], 0.15)
        junta(self, DD2, "b")
        DD3 = L([("a", r"|d_2(\pm3)|"), ("b", r"=\dfrac{2\cdot3}{9}"), ("c", r"=\Lm{\tfrac23}"), ("vg", r",\qquad "), ("d", r"d_2(0)=0")], 1120, 830, 32)
        self.gat("na margem com xis igual a três")
        acende(self, [mg], LIMA, 0.6)
        escreve_p(self, DD3, ["a", "b", "c"], 0.12)
        self.gat("no centro com xis zero")
        escreve_p(self, DD3, ["vg", "d"], 0.12)
        junta(self, DD3)
        at = legenda("ATRITO VISCOSO: MÁXIMO NAS MARGENS", 1124, 945, LIMA, "left", 26)
        self.gat("máxima nas margens")
        self.play(FadeIn(at, shift=0.05 * UP), run_time=0.4)
        rede.clear_updaters()
        self.sai_fim()

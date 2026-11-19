"""Lote PA2 · A2 ÁGUA BATENDO NA PAREDE · v2 (alvo v2_a2 + 24 v1). Parede desde o primeiro quadro. v(x, 0) = (x, −0) = (x, 0) com o 0 voando da parede e a
fileira de baixo acendendo; MODELO IDEAL: SEM A CAMADA QUE GRUDA; a tabela (1 0; 0 −1) e as medidas pela fórmula-mãe (voo das células); a gota.
Hipérboles: d(xy)/dt = u·y + x·v, u e v voam de (u, v), R14 → 0, um ponto laranja anda em xy = 2. φ: φ_x = x, φ_y = −y ⇒ ∇φ = v; ∇²φ = 1 + (−1) = 0.
A cadeia até a equação de Laplace, um pedaço por frase."""
from alg30 import *  # noqa: F401,F403

VP = VB(LA, 600, 840, 120)
CG, SG_, TG = (0.0, 3.0), 1.0, .9
dPx, dPy, dQx, dQy = r"\Pp_{\Am{x}}", r"\Pp_{\Mg{y}}", r"\Qq_{\Am{x}}", r"\Qq_{\Mg{y}}"


def parede():
    g = VGroup(linha_rec(VP, [(-4, 0), (4, 0)], LA, GEO, 6))
    X = -3.9
    while X < 4:
        g.add(linha_rec(VP, [(X, 0), (X - .25, -.25)], LA, GEO, 2, .6))
        X += .35
    return g.set_z_index(6)


def hiperboles():
    g = VGroup()
    for k in (.5, 1, 2, 3.5):
        for sg in (1, -1):
            pts = [(sg * X, k / X) for X in np.arange(.12, 4.0001, .04) if k / X <= 5.5]
            g.add(linha_rec(VP, pts, LA, GEO, 2, .55, dash=(8, 8)))
    return g.set_z_index(4)


class LoteA2(Base):
    ANTES = "APLICAÇÃO · O RIO"

    def corpo(self):
        # ── A2-1 · o jato e a parede (a parede desde o primeiro quadro) ──
        self.an("A2-1")
        self.secao("APLICAÇÃO · ÁGUA BATENDO NA PAREDE")
        zera_chapas()
        chA = chapa_px(*LA, nome="A2 palco (600, 840)", v=VP)
        pw = parede()
        ped = quad30(VP, CG, SG_)
        fan = fantasma(VP, quad_pts(CG, SG_))
        st = {"q": False}
        cmp = campo30(VP, F_SELA, -3.5, 3.5, .5, 5.5, .5, rmin=0, mmax=4, nome="A2 (x, −y), y ≥ 0,5")
        troca(self, "A1 → A2 (palco com a parede)")
        self.play(FadeIn(chA), Create(pw), run_time=0.8)
        VV = L([("v", r"\vv=("), ("x", r"\X"), ("vg", r",\ "), ("my", r"-\Y"), ("f", ")"), ("uv", r"=(u,\ v)")], 1120, 270, 38)
        mi = legenda("MODELO IDEAL PERTO DO PONTO DE CHOQUE", 1124, 340, GEO, "left", 26)
        self.gat("num modelo ideal")
        self.play(FadeIn(mi, shift=0.05 * UP), run_time=0.4)
        self.gat("a velocidade tem a coordenada horizontal")
        VV._origem = "a"
        self.play(cresce_campo(cmp, 0.8), caneta(VV, ritmo=0.25), run_time=1.6)
        clareira(cmp, lambda: ou(clar_ped(ped), dq(CG, SG_)) if st["q"] else NADA)
        self.ate(1.0)

        # ── A2-2 · desliza; a tabela; a gota; as hipérboles ──
        self.an("A2-2")
        V0 = L([("v", r"\vv(\X,0)="), ("x", r"(\X,\ "), ("m0", "-0"), ("f", ")"), ("r", r"=(\X,\ 0)")], 1120, 410, 34)
        fila = [s for s in cmp if abs(s._xy[1] - .5) < 1e-6]
        self.gat("na parede a componente vertical é zero")
        escreve_p(self, V0, ["v", "x", "f"], 0.25)
        voa(self, pw[0], V0.p("m0"), rt=0.5)
        escreve_p(self, V0, ["r"], 0.25)
        junta(self, V0, "b")
        acende(self, fila, CAMPO2, 1.0)
        cg = legenda("MODELO IDEAL: SEM A CAMADA QUE GRUDA", 1124, 470, GEO, "left", 26)
        self.gat("numa parede de verdade")
        self.play(FadeOut(mi), FadeIn(cg, shift=0.05 * UP), run_time=0.4)
        self.remove(mi)
        Jm = TC(r"J=\begin{pmatrix}\Am1 & \Mg0\\ \Am0 & \Mg{-1}\end{pmatrix}", 1120, 570, 34)
        MS = [("rot", r"\V{\rot}=", dQx + "-" + dPy, ((1, 0), (0, 1)), "0", "-", "0", r"\V0", "rotacional zero"),
              ("div", r"\D{\dv}=", dPx + "+" + dQy, ((0, 0), (1, 1)), "1", "+", "(-1)", r"\D0", "divergente um menos um"),
              ("d1", r"d_1=", dPx + "-" + dQy, ((0, 0), (1, 1)), "1", "-", "(-1)", r"\Lm2", "primeira deformação um menos")]
        Ms = [L([("n", n), ("f", f)], 1120, 670 + i * 58, 32) for i, (k, n, f, *_r) in enumerate(MS)]
        self.gat("a tabela tem um e zero")
        for M in Ms:
            M._origem = "a"
        escreve(self, Jm, 0.3, extra=[caneta(M, ritmo=0.12) for M in Ms])
        cel, _ = celulas(Jm)
        Rm = []
        for i, (k, n, f, cs, a, op, b, r, fr) in enumerate(MS):
            self.gat(fr)
            Rm.append(gm(self, Ms[i], L([("n", n), ("f", f), ("e", "="), ("a", a), ("op", op), ("b", b), ("r", "=" + r)], 1120, 670 + i * 58, 32), rt=0.5,
                         voos={"a": cel[cs[0]], "b": cel[cs[1]]}))
        self.gat("uma gota de tinta")
        st["q"] = True
        self.play(FadeIn(ped), FadeIn(fan), run_time=0.4)
        a0 = ped.area()
        self.play(anda(ped, fl_sela, TG, 2.0, rate=linear, nome="A2 gota"))
        print(f"[A2] gota: área {a0:.4f} → {ped.area():.4f}")
        hp = hiperboles()
        bloco = [V0, cg, Jm, *Rm]
        self.gat("e as linhas de corrente são hipérboles")
        self.play(Create(hp), *[FadeOut(m) for m in bloco], run_time=0.8)
        self.remove(*bloco)
        DT = L([("d", r"\dfrac{d(\X\Y)}{dt}="), ("u", r"u\,"), ("y", r"\Y"), ("pl", "+"), ("x", r"\X\,"), ("v", "v")], 1120, 375, 36)
        self.gat("o produto muda pela velocidade horizontal")
        escreve(self, DT, 0.2)
        D2 = L([("e", "="), ("u", r"\X\,"), ("y", r"\Y"), ("pl", "+"), ("x", r"\X\,"), ("v", r"(-\Y)")], 1150, 470, 34)
        self.gat("mais a horizontal vezes a velocidade vertical")
        gm(self, DT, D2, rt=0.7, copia=True, voos={"u": VV.p("x"), "v": VV.p("my")})
        D3 = L([("e", "="), ("u", r"\X\,"), ("y", r"\Y"), ("pl", "+"), ("x", r"\X\,"), ("v", r"(-\Y)"), ("p1", r"=\X\Y"), ("p2", r"-\X\Y")], 1150, 470, 34)
        self.gat("dá o produto menos o produto")
        gm(self, D2, D3, rt=0.5)
        tr = cancela(self, D3, "p1", "p2", rt=0.2)
        D4 = L([("e", "="), ("u", r"\X\,"), ("y", r"\Y"), ("pl", "+"), ("x", r"\X\,"), ("v", r"(-\Y)"), ("p1", r"=\X\Y"), ("p2", r"-\X\Y"), ("z", "=0")], 1150, 470, 34)
        for g in D4.p("p1", "p2"):
            g.set_color(CORAL_C)
        gm(self, D3, D4, rt=0.5)
        pl = ponto7(VP.c2p(.5, 4.0), POS, 9, 12)
        pn = legenda("O PRODUTO NÃO MUDA: A ÁGUA ANDA NA HIPÉRBOLE", 1124, 550, GEO, "left", 26)
        self.gat("o produto não muda")
        xs = np.linspace(.5, 3.5, 60)
        self.add(pl)
        self.play(UpdateFromAlphaFunc(pl, lambda m, a: m.move_to(VP.c2p(xs[0] + (xs[-1] - xs[0]) * a, 2 / (xs[0] + (xs[-1] - xs[0]) * a)))),
                  caneta(pn, ritmo=0.12), run_time=2.0)
        self.play(FadeOut(pl), FadeOut(VGroup(*tr)), run_time=0.3)
        self.remove(pl, *tr)
        self.ate(1.0)

        # ── A2-3 · o potencial; o laplaciano ──
        self.an("A2-3")
        PH = L([("p", r"\varphi=\tfrac12(\X^2-\Y^2):\quad "), ("d", r"\varphi_{\Am x}=\X,\ \ \varphi_{\Mg y}=-\Y"), ("i", r"\ \Rightarrow\ \nabla\varphi="), ("v", r"\vv")], 1120, 640, 34)
        self.gat("esse campo é o gradiente")
        escreve_p(self, PH, ["p", "d", "i"], 0.15)
        voa(self, VV.p("v"), PH.p("v"), rt=0.5)
        junta(self, PH, "b")
        LP = L([("l", r"\nabla^2\varphi=\varphi_{\Am{xx}}+\varphi_{\Mg{yy}}"), ("s", r"=1+(-1)"), ("z", "=0")], 1120, 730, 36)
        self.gat("e o laplaciano dela")
        escreve_p(self, LP, ["l"], 0.2)
        self.gat("dá um menos um")
        escreve_p(self, LP, ["s", "z"], 0.2)
        junta(self, LP)
        self.ate(1.0)

        # ── A2-4 · a cadeia até Laplace ──
        self.an("A2-4")
        C1 = L([("a", r"\vv=\nabla\varphi\ \Rightarrow\ \V{\rot}\,\vv=0"), ("b", r",\quad \D{\dv}\,\vv=0"), ("c", r"\ \Rightarrow\ \D{\dv}\,\nabla\varphi=0")], 1120, 905, 32)
        C2 = L([("d", r"\D{\dv}\,\nabla\varphi=\nabla^2\varphi"), ("e", "=0")], 1120, 965, 32)
        for fr, lin, ks in (("se a velocidade é um gradiente", C1, ["a"]), ("se além disso o divergente é zero", C1, ["b"]),
                            ("então o divergente do gradiente é zero", C1, ["c"]), ("e o divergente do gradiente é o laplaciano", C2, ["d"]),
                            ("quer dizer laplaciano do potencial igual a zero", C2, ["e"])):
            self.gat(fr)
            if ks == ["a"]:                  # R13: as duas linhas do produto se fundem (lado esquerdo da primeira + resultado da última)
                DF_ = L([("d", r"\dfrac{d(\X\Y)}{dt}="), ("z", "0")], 1120, 375, 36)
                AD_ = Duas(DT, D4)
                AD_.ks = ["d"] + ["x"] * (len(DT.ks) - 1) + ["x"] * (len(D4.ks) - 1) + ["z"]
                gm(self, AD_, DF_, rt=0.6, nota="(R13: fusão do produto)")
                self.remove(DT, D4)
            escreve_p(self, lin, ks, 0.2)
        junta(self, C1)
        junta(self, C2)
        eq = T("EQUAÇÃO DE LAPLACE", 1120, 820, 36)
        self.play(FadeIn(eq, shift=0.05 * UP), run_time=0.4)
        self.gat("aparece no potencial elétrico")                # R16: a equação citada acende de novo em cada aparição
        acende(self, [C2], CAMPO2, 1.0)
        self.gat("e na temperatura de uma chapa")
        acende(self, [C2], AMB, 1.0)
        cmp.clear_updaters()
        self.sai_fim()

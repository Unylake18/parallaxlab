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
    """xy = k (k = 0,5; 1; 2; 3,5), tracejadas GEO; a de xy = 1 (lado direito) em branco, contínua (alvo v3_a2)."""
    g = VGroup()
    for k in (.5, 1, 2, 3.5):
        for sg in (1, -1):
            pts = [(sg * X, k / X) for X in np.arange(.12, 4.0001, .04) if k / X <= 5.5]
            um = k == 1 and sg == 1
            g.add(linha_rec(VP, pts, LA, BR if um else GEO, 3 if um else 2, .9 if um else .55, dash=None if um else (8, 8)))
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
        self.play(FadeIn(chA), Create(pw), run_time=0.5)
        VV = L([("v", r"\vv=("), ("x", r"\X"), ("vg", r",\ "), ("my", r"-\Y"), ("f", ")"), ("uv", r"=(u,\ v)")], 1120, 270, 38)
        mi = legenda("MODELO IDEAL PERTO DO PONTO DE CHOQUE", 1124, 340, GEO, "left", 26)
        self.gat("um jato de água descendo")                       # v3 §1.3: o campo nasce linha a linha, de cima para baixo, até a parede
        self.play(cresce_campo(cmp, 1.4, chave=lambda s: -s._xy[1]), run_time=1.4)
        self.gat("num modelo ideal")
        self.play(FadeIn(mi, shift=0.05 * UP), run_time=0.4)
        self.gat("a velocidade tem a coordenada horizontal")
        escreve(self, VV, 0.25)
        self.gat("só na metade de cima")                          # palco v3: a parede citada acende (só o traço)
        acende(self, [pw], BR, 1.0)
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
        # v4 C12: a tabela do jato pelas derivadas (deriva_cel, o mesmo caminho do D5)
        Jmo = TC(r"J=\begin{pmatrix}%s & %s\\ %s & %s\end{pmatrix}" % (dPx, dPy, dQx, dQy), 1120, 570, 34)
        Jm = TC(r"=\begin{pmatrix}\Am1 & \Mg0\\ \Am0 & \Mg{-1}\end{pmatrix}", Jmo.get_right()[0] * 120 + 960 + 10, 570, 34, caneta=False)
        cel, restoJ = celulas(Jm)
        MS = [("rot", r"\V{\rot}=", dQx + "-" + dPy, ((1, 0), (0, 1)), "0", "-", "0", r"\V0", "rotacional zero"),
              ("div", r"\D{\dv}=", dPx + "+" + dQy, ((0, 0), (1, 1)), "1", "+", "(-1)", r"\D0", "divergente um menos um"),
              ("d1", r"d_1=", dPx + "-" + dQy, ((0, 0), (1, 1)), "1", "-", "(-1)", r"\Lm2", "primeira deformação um menos")]
        Ms = [L([("n", n), ("f", f)], 1120, 670 + i * 58, 32) for i, (k, n, f, *_r) in enumerate(MS)]
        self.gat("segundo a tabela derivada por derivada")
        self.play(FadeOut(cg), run_time=0.3)                           # a legenda da parede sai: o caminho das derivadas passa por ali
        self.remove(cg)
        for M in Ms:
            M._origem = "a"
        escreve(self, Jmo, 0.25, extra=[caneta(M, ritmo=0.12) for M in Ms])
        print(f"[origem] a {self.lote} A2-2 {self.t:.2f} 'parênteses da J' (resto)")
        self.play(caneta(restoJ, ritmo=0.25))
        vals = []
        self.gat("a primeira componente é xis")
        vals.append(deriva_cel(self, VV.p("x"), cel[(0, 0)], 0, [("x", r"\X")], [("v", r"\Am1")], ["v"], y_mid=480))
        vals.append(deriva_cel(self, VV.p("x"), cel[(0, 1)], 1, [("x", r"\X")], [("v", r"\Mg0")], ["v"], some=("x",), y_mid=480))
        self.gat("a segunda é menos ípsilon")
        MY = [("m", "-"), ("y", r"\Y")]
        vals.append(deriva_cel(self, VV.p("my"), cel[(1, 0)], 0, MY, [("v", r"\Am0")], ["v", "v"], some=("m", "y"), y_mid=480))
        vals.append(deriva_cel(self, VV.p("my"), cel[(1, 1)], 1, MY, [("v", r"\Mg{-1}")], ["v", "v"], y_mid=480))
        self.remove(*vals)
        junta(self, Jm, "b")
        self.gat("a tabela tem um e zero")
        acende(self, [VGroup(*[cel[k] for k in cel])], BR, 0.8)
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
        bloco = [V0, Jmo, Jm, *Rm]
        self.gat("e as linhas de corrente são hipérboles")
        self.play(Create(hp), *[FadeOut(m) for m in bloco], run_time=0.8)
        self.remove(*bloco)
        # v4 C13: y = c/x; a regra do produto no tempo com dx/dt = u e dy/dt = v
        HP = L([("a", r"\X\Y=c"), ("i", r"\ \Rightarrow\ "), ("b", r"\Y=\dfrac{c}{\X}")], 1120, 340, 34)
        self.gat("ípsilon igual a uma constante sobre xis")
        escreve(self, HP, 0.2)
        DT = L([("d", r"\dfrac{d(\X\Y)}{dt}="), ("a", r"\dfrac{d\X}{dt}\,"), ("y", r"\Y"), ("pl", "+"), ("x", r"\X\,"), ("b", r"\dfrac{d\Y}{dt}")], 1120, 420, 34)
        self.gat("lê-se dê xis ípsilon dê tê")                     # leitura 19: d(xy)/dt (escrito a caneta nessa hora)
        escreve_p(self, DT, ["d"], 0.2)
        ln19 = le_abre(self, VGroup(*DT.p("d")[:-1]), 19, "dê xis ípsilon, dê tê: a taxa de variação do produto no tempo")
        self.gat("regra do produto agora no tempo")
        escreve_p(self, DT, ["a", "y", "pl", "x", "b"], 0.15)
        junta(self, DT)
        le_fecha(self, ln19, 19, "andando com a água")
        CH = L([("a", r"\dfrac{d\X}{dt}"), ("e1", "="), ("u", "u"), ("vg", r",\qquad "), ("b", r"\dfrac{d\Y}{dt}"), ("e2", "="), ("v", "v")], 1120, 505, 30)
        uv = VV.p("uv")                                                # = ( u , v )
        self.gat("a posição muda com a velocidade")
        escreve_p(self, CH, ["a", "e1"], 0.12)
        voa(self, uv[2], CH.p("u"), rt=0.4)
        escreve_p(self, CH, ["vg", "b", "e2"], 0.12)
        voa(self, uv[4], CH.p("v"), rt=0.4)
        junta(self, CH, "b")
        DT2 = L([("d", r"\dfrac{d(\X\Y)}{dt}="), ("u", r"u\,"), ("y", r"\Y"), ("pl", "+"), ("x", r"\X\,"), ("v", "v")], 1120, 420, 34)
        self.gat("o produto muda pela velocidade horizontal")
        gm(self, DT, DT2, rt=0.7, ka=["d", "z", "y", "pl", "x", "z"], voos={"u": CH.p("u"), "v": CH.p("v")}, nota="(dx/dt = u, dy/dt = v)")
        self.gat("mais a horizontal vezes a velocidade vertical")
        acende(self, [DT2.p("x", "v")], AMB, 0.7)
        D2 = L([("e", "="), ("u", r"\X\,"), ("y", r"\Y"), ("pl", "+"), ("x", r"\X\,"), ("v", r"(-\Y)")], 1150, 585, 34)
        self.gat("com u igual a xis")
        gm(self, DT2, D2, rt=0.7, copia=True, voos={"u": VV.p("x"), "v": VV.p("my")})
        D3 = L([("e", "="), ("u", r"\X\,"), ("y", r"\Y"), ("pl", "+"), ("x", r"\X\,"), ("v", r"(-\Y)"), ("p1", r"=\X\Y"), ("p2", r"-\X\Y")], 1150, 585, 34)
        self.gat("dá o produto menos o produto")
        gm(self, D2, D3, rt=0.5)
        tr = cancela(self, D3, "p1", "p2", rt=0.2)
        D4 = L([("e", "="), ("u", r"\X\,"), ("y", r"\Y"), ("pl", "+"), ("x", r"\X\,"), ("v", r"(-\Y)"), ("p1", r"=\X\Y"), ("p2", r"-\X\Y"), ("z", "=0")], 1150, 585, 34)
        for g in D4.p("p1", "p2"):
            g.set_color(CORAL_C)
        gm(self, D3, D4, rt=0.5)
        pn = legenda("O PRODUTO NÃO MUDA: A ÁGUA ANDA NA HIPÉRBOLE", 1124, 650, GEO, "left", 26)
        # a gota laranja anda em xy = 1 pelo fluxo exato (e^t, e^−t), deixando um ponto a cada 0,4 s (alvo v3_a2)
        lb = rot(r"\X\Y=1", *canto_xy(VP, 2.75, .76), 30)
        self.gat("o produto não muda")
        self.add(lb[0])
        sob = [s for s in cmp if hasattr(s, "_xy") and abs(s._xy[0] - 2.75) < .5 and abs(s._xy[1] - .76) < .45]   # R5: as setas sob o rótulo xy = 1
        escreve(self, lb.f, 0.3, rt=0.6, extra=[*[UpdateFromAlphaFunc(s, lambda m, a: op_seta(m, 1 - a)) for s in sob], caneta(pn, ritmo=0.12), FadeOut(VGroup(*tr))])
        self.remove(*tr)
        ts = [-1.2 + .4 * k for k in range(7)]
        gota = ponto7(VP.c2p(math.exp(ts[0]), math.exp(-ts[0])), POS, 11, 12)
        marcas = [ponto7(VP.c2p(math.exp(t), math.exp(-t)), POS, 6, 11) for t in ts[:-1]]
        self.add(gota)
        for k in range(6):
            t0, t1 = ts[k], ts[k + 1]
            self.add(marcas[k])
            self.play(UpdateFromAlphaFunc(gota, lambda m, a, t0=t0, t1=t1: m.move_to(VP.c2p(math.exp(t0 + (t1 - t0) * a), math.exp(-(t0 + (t1 - t0) * a))))),
                      rate_func=linear, run_time=0.4)
        print(f"[A2] gota em xy = 1: {', '.join(f'({math.exp(t):.3f}, {math.exp(-t):.3f})' for t in ts)} (produto 1,000 em todos)")
        self.ate(1.0)

        # ── A2-3 · o potencial; o laplaciano ──
        self.an("A2-3")
        # v4 C14: o produto vira chip; o potencial com as derivadas (o 2 do expoente desce)
        CHP = L([("a", r"\X\Y=c"), ("vg", r",\quad "), ("d", r"\dfrac{d(\X\Y)}{dt}=0")], 1120, 340, 30)
        PH1 = L([("phi", r"\varphi="), ("h", r"\tfrac12"), ("p", r"(\X^2-\Y^2)")], 1120, 420, 34)
        self.gat("esse campo é o gradiente")
        AP = Duas(HP, DT2, CH, D4)
        AP.ks = ["a", "z", "z"] + ["d"] + ["z"] * 5 + ["z"] * len(CH.ks) + ["z"] * 8 + ["d"]
        gm(self, AP, CHP, rt=0.7, nota="(R13: o produto vira chip)", extra=[FadeOut(pn)])
        self.remove(HP, DT2, CH, D4, pn)
        escreve(self, PH1, 0.2)
        PH = L([("fx", r"\varphi_{\Am x}"), ("ex", r"=\tfrac12\cdot2\X"), ("rx", r"=\X"), ("vg", r",\ \ "), ("fy", r"\varphi_{\Mg y}"), ("ey", r"=\tfrac12\cdot(-2\Y)"),
                ("ry", r"=-\Y"), ("i", r"\ \Rightarrow\ \nabla\varphi="), ("v", r"\vv")], 1110, 500, 28)
        pp, ex, ey = PH1.p("p"), PH.p("ex"), PH.p("ey")
        self.gat("derivando o meio vezes dois xis")
        print(f"[origem] a {self.lote} A2-3 {self.t:.2f} {PH._tex[:60]!r} (φ_x; o 2 do expoente voa)")
        self.play(caneta(VGroup(*PH.p("fx"), *ex[0:5]), ritmo=0.12))
        voa(self, pp[2], ex[5], rt=0.4)
        self.play(caneta(VGroup(ex[6], *PH.p("rx")), ritmo=0.15))
        self.gat("e o meio vezes menos dois ípsilon")
        self.play(caneta(VGroup(*PH.p("vg", "fy"), *ey[0:7]), ritmo=0.12))
        voa(self, pp[5], ey[7], rt=0.4)
        self.play(caneta(VGroup(*ey[8:], *PH.p("ry", "i")), ritmo=0.12))
        voa(self, VV.p("v"), PH.p("v"), rt=0.45)
        junta(self, PH, "b")
        pv = legenda("POTENCIAL DE VELOCIDADE", PH1.get_right()[0] * 120 + 960 + 24, 420, GEO, "left", 24)
        self.gat("essa função se chama potencial")
        self.play(FadeIn(pv, shift=0.05 * UP), run_time=0.4)
        # v3 §3 #7: φ_x = x → φ_xx = 1 (o índice ganha o segundo x e o valor vira 1); o mesmo no y
        LX = L([("fx", r"\varphi_{\Am{x}", 2), ("nx", r"\Am{x}}", 1), ("e1", "="), ("ux", "1"), ("vg", r",\ \ "), ("fy", r"\varphi_{\Mg{y}", 2), ("ny", r"\Mg{y}}", 1),
                ("e2", "="), ("uy", "-1")], 1120, 580, 34)
        LP = L([("l", r"\nabla^2\varphi=\varphi_{\Am{xx}}+\varphi_{\Mg{yy}}"), ("s", r"=1+(-1)"), ("z", "=0")], 1120, 660, 36)
        self.gat("e o laplaciano dela")
        escreve_p(self, LP, ["l"], 0.12)
        self.gat("escrito nabla dois fi")                          # leitura 20: ∇²φ
        le(self, VGroup(*LP.p("l")[:3]), 20, "nabla dois fi, a soma das duas derivadas segundas", ate="aquela curiosidade do segundo episódio")
        self.gat("derivando de novo")
        gm(self, PH, LX, rt=0.6, copia=True, ka=["fx", "z", "ux", "vg", "fy", "z", "uy", "z", "z"], nota="(φ_x = x → φ_xx = 1; φ_y = −y → φ_yy = −1)")
        self.gat("dá um menos um")
        escreve_p(self, LP, ["s", "z"], 0.2)
        junta(self, LP)
        self.ate(1.0)

        # ── A2-4 · a cadeia até Laplace ──
        self.an("A2-4")
        C1 = L([("a", r"\vv=\nabla\varphi\ \Rightarrow\ \V{\rot}\,\vv=0"), ("b", r",\quad \D{\dv}\,\vv=0"), ("c", r"\ \Rightarrow\ \D{\dv}\,\nabla\varphi=0")], 1110, 905, 30)
        C2 = L([("d", r"\D{\dv}\,\nabla\varphi="), ("f", r"\dfrac{\partial\varphi_{\Am x}}{\dx}+\dfrac{\partial\varphi_{\Mg y}}{\dy}"),
                ("g", r"=\varphi_{\Am{xx}}+\varphi_{\Mg{yy}}=\nabla^2\varphi"), ("e", "=0")], 1110, 965, 28)
        for fr, lin, ks in (("se a velocidade é um gradiente", C1, ["a"]), ("se também tem divergente zero", C1, ["b"]),
                            ("então o divergente do gradiente é zero", C1, ["c"]), ("e o divergente do gradiente é o laplaciano", C2, ["d", "f"]),
                            ("deriva fi xis em xis", C2, ["g"]), ("quer dizer laplaciano do potencial igual a zero", C2, ["e"])):
            self.gat(fr)
            if ks == ["a"]:                  # R13: as derivadas segundas entram no laplaciano (a fusão do produto foi para o A2-3)
                LP2 = L(list(zip(LP.ks, LP.ts)), 0, 0, LP.size).move_to(LP.get_center())
                AL = Duas(LX, LP)
                AL.ks = ["x"] * len(LX.ks) + list(LP.ks)
                gm(self, AL, LP2, rt=0.5, nota="(R13: as derivadas segundas entram no laplaciano)")
                self.remove(LX, LP)
            escreve_p(self, lin, ks, 0.15)
            if ks == ["a"]:                  # v4 C15: lembrança da primeira regra (rot ∇φ = 0), 1,5 s
                self.gat("é a primeira das duas regras")
                lr = TC(r"\rot\,\nabla\varphi=\vec0", 1120, 858, 26, caneta=False).set_color(VIO)
                lr._origem = "lembrança"
                print(f"[origem] lembrança {self.lote} A2-4 {self.t:.2f} {lr._tex!r} (a primeira das duas regras, 1,5 s)")
                self.play(FadeIn(lr), run_time=0.3)
                self.wait(1.2)
                self.play(FadeOut(lr), run_time=0.3)
                self.remove(lr)
        junta(self, C1)
        junta(self, C2)
        eq = T("EQUAÇÃO DE LAPLACE", 1120, 838, 36)
        self.play(FadeIn(eq, shift=0.05 * UP), run_time=0.4)
        self.gat("aparece no potencial elétrico")                # R16: a equação citada acende de novo em cada aparição
        acende(self, [C2], CAMPO2, 1.0)
        self.gat("e na temperatura de uma chapa")
        acende(self, [C2], AMB, 1.0)
        cmp.clear_updaters()
        self.sai_fim()

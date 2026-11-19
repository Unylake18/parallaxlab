"""Lote PD5 · D5 O DESAFIO PROMETIDO · v2 (alvos v2_d5a, v2_d5c1, v2_d5c2 + 19–22 v1). Abertura: o molde J = (P_x P_y; Q_x Q_y) e as quatro
fórmulas-mãe, cada uma com as células que usa acendendo na cor da medida. Para cada campo: P e Q voam de F; as derivadas em caneta; as células voam para
J; cada medida ganha a substituição (os números voam das células) e o resultado por glyph map; selos; solta. ① e a resposta do palpite (o salto da
transformação × o fluxo; o div acende). ② com a seta do centro. ③ simbólico, com R14 em d₁ e d₂; a previsão ponto a ponto; quinas retas; lado 0,1."""
from alg30 import *  # noqa: F401,F403

V3 = Vista(360, 780, 240)
PTS3 = [(1, 0), (0, 1), (1, 1)]
LAB3 = [(1, -.36), (-.5, 1), (1.5, 1.38)]
dPx, dPy, dQx, dQy = r"\Pp_{\Am{x}}", r"\Pp_{\Mg{y}}", r"\Qq_{\Am{x}}", r"\Qq_{\Mg{y}}"
MAE = [("rot", r"\V{\rot}=", dQx + "-" + dPy, ((1, 0), (0, 1)), "-", VIO), ("div", r"\D{\dv}=", dPx + "+" + dQy, ((0, 0), (1, 1)), "+", SAIC),
       ("d1", r"d_1=", dPx + "-" + dQy, ((0, 0), (1, 1)), "-", LIMA), ("d2", r"d_2=", dQx + "+" + dPy, ((1, 0), (0, 1)), "+", LIMA)]
YM = [590, 652, 714, 776]


def tex_v(v, col):
    c = r"\Am" if col == 0 else r"\Mg"
    return c + "{" + v + "}"


def par(v, col, op):
    t = tex_v(v, col)
    return "(" + t + ")" if op == "+" and v.startswith("-") or op == "-" and v.startswith("-") else t


def med(i, va=None, vb=None, res=None, y=None, size=36):
    k, n, f, cs, op, cor = MAE[i]
    p = [("n", n), ("f", f)]
    if va is not None:
        p += [("e", "="), ("a", par(va, cs[0][1], "")), ("op", op), ("b", par(vb, cs[1][1], op))]
    if res is not None:
        p += [("r", "=" + res)]
    return L(p, 1120, y or YM[i], size)


def selos(estados, y=868, x=1120):
    pec, itens = [], []
    for k, (nome, ok) in enumerate(zip(("GIRA", "ÁREA", "DEFORMA"), estados)):
        t = T(nome, 0, y, 32)
        mk = MathTex(r"\checkmark" if ok else r"\boldsymbol{\times}", font_size=fs(32)).set_color(CAMPO2 if ok else CORAL)
        mk._sem_contorno, mk._origem = True, "legenda"
        it = VGroup(t, mk)
        mk.next_to(t, RIGHT, buff=8 / 120).set_y(t.get_center()[1])
        itens.append(it)
        pec.append(it)
        if k < 2:
            pec.append(T("·", 0, y, 32, cor=GEO, bold=False))
    g = VGroup(*pec).arrange(RIGHT, buff=14 / 120, center=False)
    for p in pec[1::2]:
        p.set_y(pec[0][0].get_center()[1])
    g.shift(RIGHT * (PX(x, 0)[0] - g.get_left()[0]))
    return g, itens


def marcas_reto(v, ped, m=.05):
    k = len(ped.XY) // 4
    P = ped.XY
    g = VGroup()
    for c in range(4):
        A = P[c * k]
        B = P[c * k + 1]
        C = P[c * k - 2]
        u = (B - A) / np.linalg.norm(B - A)
        w = (C - A) / np.linalg.norm(C - A)
        g.add(vlinha(v, [A + u * m, A + u * m + w * m, A + w * m], BR, 2).set_z_index(12))
    return g


class LoteD5(Base):
    ANTES = "O CAMPO QUE NÃO MELHORA DE PERTO · CLASSE C¹"

    def jvals(self, vals, x0, src):
        """Matriz de valores à direita do molde: '=' em caneta e cada célula voando da sua derivada (src[(i, j)])."""
        Jv = TC(r"=\begin{pmatrix}%s & %s\\ %s & %s\end{pmatrix}" % (tex_v(vals[0], 0), tex_v(vals[1], 1), tex_v(vals[2], 0), tex_v(vals[3], 1)), x0, 480, 34, caneta=False)
        cel, resto = celulas(Jv)
        self.play(caneta(resto, ritmo=0.3), *[TransformFromCopy(src[k], cel[k]) for k in cel], run_time=0.8)
        junta(self, Jv, "b")
        return Jv, cel

    def chaves(self, Fl, P_, Q_):
        """v3 §1.5: P e Q nascem como chaves sob as componentes do F, num glyph map sobre a própria linha do F (a componente não sai do lugar)."""
        from alg30 import _nglifos
        t1, t2 = Fl.ts[Fl.ks.index("c1")], Fl.ts[Fl.ks.index("c2")]
        nb = lambda t, s_: _nglifos(r"\underbrace{" + t + "}_{" + s_ + "}") - _nglifos(t) - 1      # pedaços da chave (dependem da largura)
        Fb = L([("F", Fl.ts[0]), ("u1", r"\underbrace{", 0), ("c1", t1), ("b1", "}", nb(t1, P_)), ("s1", "_{" + P_ + "}", 1), ("vg", r",\ "),
                ("u2", r"\underbrace{", 0), ("c2", t2), ("b2", "}", nb(t2, Q_)), ("s2", "_{" + Q_ + "}", 1), ("f", ")")], 0, 0, Fl.size)
        Fb.shift(Fl.p("c1").get_center() - Fb.p("c1").get_center())
        gm(self, Fl, Fb, rt=0.7, nota="(as chaves P e Q nascem sob as componentes)")
        return Fb

    def deriva(self, comp, alvo, col, mid_p, val_p, ka, some=(), extra=(), inter=None):
        """v3 §1.5: a derivada é calculada no caminho até a célula. Cópia da componente (voo) até acima da tabela, com o rótulo ∂/∂x por 0,5 s;
        glyph map da expressão para o número, que pousa na célula `alvo`. Nada fica escrito fora da J."""
        return deriva_cel(self, comp, alvo, col, mid_p, val_p, ka, some, extra, y_mid=372, inter=inter)       # v4 C9: função comum (alg30)

    def tabela(self, Jv, cel, plano, resto=None):
        """Preenche as quatro células pelo caminho (plano: [(frase, comp, k, mid, val, ka, some[, inter])]) e junta a J; os parênteses da J (resto) são
        escritos junto com o primeiro voo. inter = (peças do degrau do meio, ka mid → meio, ka meio → valor)."""
        vals = []
        for i, item in enumerate(plano):
            fr, comp, k, mid_p, val_p, ka, some = item[:7]
            inter = item[7] if len(item) > 7 else None
            if fr:
                self.gat(fr)
            ex = [caneta(resto, ritmo=0.3)] if (i == 0 and resto is not None) else []
            vals.append(self.deriva(comp, cel[k], k[1], mid_p, val_p, ka, some, extra=ex, inter=inter))
        self.remove(*vals)
        junta(self, Jv, "b")

    def lembra_gancho(self, k, rede):
        """v3 §2 H: ao fechar cada campo, a caixa da fórmula do gancho aparece pequena no canto do palco por 2 s (lembrança)."""
        from escada30 import caixa30
        x0, y0, w, h = 790, 796, 280, 96
        f = TC([r"\F=(\X+\Y,\ \X-\Y)", r"\F=(1,\ \X-\Y)", r"\F=(\X^2-\Y^2,\ 2\X\Y)"][k], x0 + w / 2, y0 + 64, 30, "c")
        f._origem = "lembrança"
        print(f"[origem] lembrança {self.lote} {self._aid} {self.t:.2f} {f._tex!r} (a caixa do gancho, 2 s)")
        lg = legenda(["SÓ ENTORTA", "GIRA, ENCOLHE E ENTORTA", "UM GIRA · OUTRO CRESCE"][k], x0 + w / 2, y0 + 30, GEO, "center", 20)
        bx = caixa30(x0, y0, w, h, GEO, .95, z=26)
        f.set_z_index(28)
        lg.set_z_index(28)
        sob = []
        for s in rede:
            if hasattr(s, "_xy") and not getattr(s, "_escondida", False):
                cx, cy = s.get_center()[0] * 120 + 960, 540 - s.get_center()[1] * 120
                if x0 - 24 < cx < x0 + w + 24 and y0 - 24 < cy < y0 + h + 24:
                    sob.append(s)
        self.play(FadeIn(bx), FadeIn(f), FadeIn(lg), *[UpdateFromAlphaFunc(s, lambda m, a: op_seta(m, 1 - a)) for s in sob], run_time=0.4)
        self.wait(2.0)
        self.play(FadeOut(bx), FadeOut(f), FadeOut(lg), *[UpdateFromAlphaFunc(s, lambda m, a: op_seta(m, a)) for s in sob], run_time=0.4)
        self.remove(bx, f, lg)

    def recolhe_PQ(self, Fl, P, Q):
        """R13: com os valores já na tabela, as linhas P e Q voltam para a linha do campo (glyph map: P e Q sobre as componentes, o resto some)."""
        Fn = L(list(zip(Fl.ks, Fl.ts)), 0, 0, Fl.size).move_to(Fl.get_center())
        A = Duas(Fl, P, Q)
        A.ks = list(Fl.ks) + [("c1" if k == "pc" else "x") for k in P.ks] + [("c2" if k == "qc" else "x") for k in Q.ks]
        gm(self, A, Fn, rt=0.6, nota="(R13: P e Q voltam para o campo)")
        self.remove(Fl, P, Q)
        return Fn

    def medidas(self, Ms, cel, vals, res, gats, fala_sub=True):
        """Para cada medida: (gatilho) a linha-mãe ganha a substituição com voo das células; depois o resultado por glyph map."""
        out = []
        V = {(0, 0): vals[0], (0, 1): vals[1], (1, 0): vals[2], (1, 1): vals[3]}
        for i, (M, fr) in enumerate(zip(Ms, gats)):
            cs = MAE[i][3]
            if fr:
                self.gat(fr)
            S = med(i, V[cs[0]], V[cs[1]])
            gm(self, M, S, rt=0.6, voos={"a": cel[cs[0]], "b": cel[cs[1]]})
            R = med(i, V[cs[0]], V[cs[1]], res[i])
            gm(self, S, R, rt=0.5)
            out.append(R)
        return out

    def corpo(self):
        # ── D5-1 · topo da escada: o molde da tabela e as quatro fórmulas-mãe ──
        self.an("D5-1")
        self.secao("O DESAFIO")
        zera_chapas()
        chA = chapa_px(*LA, nome="D5 palco A", v=VA)
        c1, s1 = (0.0, 0.0), 1.2
        ped = quad30(VA, c1, s1)
        cmp = campo30(VA, F1, rmin=0, mmax=5, nome="D5 f₁")
        clareira(cmp, lambda: ou(clar_ped(ped), dq(c1, s1)))
        troca(self, "D4 → D5 (palco com f₁ e o quadradinho)")
        self.play(FadeIn(chA), cresce_campo(cmp, 0.8), FadeIn(ped), run_time=0.8)
        Jm = TC(r"J=\begin{pmatrix}%s & %s\\ %s & %s\end{pmatrix}" % (dPx, dPy, dQx, dQy), 1120, 480, 34)
        celm, _ = celulas(Jm)
        self.gat("monta a tabela")                               # R16: o molde da tabela entra quando a fala diz "monta a tabela"
        escreve(self, Jm, 0.3)
        self.gat("prevê se o quadradinho gira")
        acende(self, [ped], AMB, 1.0)
        self.gat("a tabela se chama jacobiana")                    # leitura 15: J
        le(self, Jm[0][0], 15, "a tabela se chama jacobiana, a letra J", ate="derivadas de p em cima")
        self.gat("lembra das quatro medidas")
        Ms = [med(i) for i in range(4)]
        for i, fr in enumerate(("rotacional o de baixo à esquerda", "divergente a diagonal somada", "primeira deformação dê um",
                                "segunda dê dois")):
            self.gat(fr)
            cor = MAE[i][5]
            escreve(self, Ms[i], 0.2, extra=[pisca_cor(VGroup(celm[MAE[i][3][0]], celm[MAE[i][3][1]]), cor, 1.0)])
            if i >= 2:                                             # leitura 16: d₁ e d₂
                le(self, VGroup(*Ms[i].p("n")[:2]), 16, ["primeira deformação, dê um", "segunda, dê dois"][i - 2], dur=0.6)
        self.ate(1.0)

        # ── D5-2 · campo ① ──
        self.an("D5-2")
        self.secao_n("O DESAFIO · CAMPO", 1)
        F = L([("F", r"\F=("), ("c1", r"\X+\Y"), ("vg", r",\ "), ("c2", r"\X-\Y"), ("f", ")")], 1120, 255, 38)
        self.gat("a soma e a diferença")
        escreve(self, F, 0.3)
        self.gat("pausa o vídeo e tenta")
        self.pausa()
        self.ate(1.0)

        # ── D5-3 · tabela, medidas e previsão (alvo v2_d5a) ──
        self.an("D5-3")

        V1 = ["1", "1", "1", "-1"]
        MS = [("x", r"\X"), ("p", "+"), ("y", r"\Y")]
        MD = [("x", r"\X"), ("m", "-"), ("y", r"\Y")]
        self.gat("a tabela")
        F = self.chaves(F, r"\Pp", r"\Qq")
        Jv = TC(r"=\begin{pmatrix}%s & %s\\ %s & %s\end{pmatrix}" % tuple(tex_v(v, i % 2) for i, v in enumerate(V1)), Jm.get_right()[0] * 120 + 960 + 10, 480, 34,
                caneta=False)
        cel, resto = celulas(Jv)
        self.tabela(Jv, cel, [
            ("a componente horizontal é a soma", F.p("c1"), (0, 0), MS, [("v", r"\Am{1}")], ["v", "z", "z"], ("p", "y")),
            (None, F.p("c1"), (0, 1), MS, [("v", r"\Mg{1}")], ["z", "z", "v"], ("x", "p")),
            ("a vertical é a diferença", F.p("c2"), (1, 0), MD, [("v", r"\Am{1}")], ["v", "z", "z"], ("m", "y")),
            (None, F.p("c2"), (1, 1), MD, [("m", r"\Mg{-}"), ("v", r"\Mg{1}")], ["z", "m", "v"], ("x",))], resto)
        self.gat("em cima um e um")
        acende(self, [VGroup(cel[(0, 0)], cel[(0, 1)])], BR, 0.8)
        Rs = self.medidas(Ms, cel, V1, [r"\V0", r"\D0", r"\Lm2", r"\Lm2"],
                          ("rotacional o de baixo à esquerda menos o de cima à direita um", "divergente a diagonal um", "primeira deformação um menos", "segunda um mais um"))
        sl, its = selos((False, False, True))
        self.gat("previsão não gira")
        self.play(FadeIn(its[0]), run_time=0.3)
        self.gat("não muda de área")
        self.play(FadeIn(sl[1]), FadeIn(its[1]), run_time=0.3)
        self.gat("só deforma")
        self.play(FadeIn(sl[3]), FadeIn(its[2]), run_time=0.3)
        self.ate(1.0)

        # ── D5-4 · solta ──
        self.an("D5-4")
        fan = fantasma(VA, quad_pts(c1, s1))
        self.gat("solta")
        self.play(FadeIn(fan), run_time=0.3)
        a0 = ped.area()
        self.play(anda(ped, fl1, .5, 2.0, rate=linear, nome="D5 campo ①"))
        print(f"[D5] ①: área {a0:.4f} → {ped.area():.4f}")
        self.lembra_gancho(0, cmp)
        self.ate(1.0)

        # ── D5-5 · a resposta do palpite: o salto da transformação × o fluxo ──
        self.an("D5-5")
        im = [(-1.2, 0), (0, -1.2), (1.2, 0), (0, 1.2)]
        sal = vlinha(VA, quad_pts(c1, s1) + [quad_pts(c1, s1)[0]], CORAL, 3, alpha=.8, dash=(9, 8)).set_z_index(9)
        sal2 = vlinha(VA, [(a + b, a - b) for a, b in quad_pts(c1, s1)] + [(quad_pts(c1, s1)[0][0] + quad_pts(c1, s1)[0][1], quad_pts(c1, s1)[0][0] - quad_pts(c1, s1)[0][1])],
                      CORAL, 3, alpha=.8, dash=(9, 8)).set_z_index(9)
        self.gat("como transformação essa fórmula")              # R16: o quadrado tracejado entra no "como transformação"; o div = 0 acende no "como campo"
        self.play(Create(sal), run_time=0.6)
        self.gat("como campo ela não muda")
        acende(self, [Rs[1]], SAIC, 1.0)
        self.gat("a transformação leva cada ponto")
        self.play(Transform(sal, sal2), run_time=0.6)
        self.gat("o campo é uma velocidade")
        ped.em(fl1, 0)
        self.play(anda(ped, fl1, .5, 2.0, rate=linear, nome="D5 ① de novo"))
        self.gat("e quem mede a taxa de área")
        acende(self, [Rs[1]], SAIC, 1.2)
        ct = legenda("COMO TRANSFORMAÇÃO: ÁREA × 2", 1124, 930, CORAL, "left", 26)
        self.gat("mudança de variáveis")
        self.play(FadeIn(ct, shift=0.05 * UP), run_time=0.4)
        self.ate(1.0)

        # ── D5-6 · campo ② ──
        self.an("D5-6")
        c2, s2_, T2 = (-1.8, -.6), 1.1, .7
        cmp.clear_updaters()
        p2 = quad30(VA, c2, s2_)
        novo = mesma_grade(cmp, F2, 5)
        F2l = L([("F", r"\ff=("), ("c1", "1"), ("vg", r",\ "), ("c2", r"\X-\Y"), ("f", ")")], 1120, 255, 38)
        self.gat("segundo campo")
        self.secao_n("O DESAFIO · CAMPO", 2)
        troca(self, "D5 campo ① → ②")
        sai = [Jv, sl, ct, ped, fan, sal]
        self.play(*[FadeOut(m) for m in sai], Transform(cmp, novo), FadeIn(p2), run_time=0.8)
        self.remove(*sai)
        herda(cmp, novo)
        gm(self, F, F2l, rt=0.6)
        st2 = {"tr": NADA, "giro": NADA}
        clareira(cmp, lambda: ou(clar_ped(p2), dq(c2, s2_), st2["tr"], st2["giro"]))
        Ms = []
        em_paralelo(self, 0.6, *[(lambda R=R, i=i: Ms.append(gm(self, R, med(i)))) for i, R in enumerate(Rs)])
        F2l = self.chaves(F2l, r"\Pp", r"\Qq")
        self.gat("pausa e tenta")
        self.pausa()
        self.ate(1.0)

        # ── D5-7 · tabela e medidas de ② ──
        self.an("D5-7")
        V2 = ["0", "0", "1", "-1"]
        Jv = TC(r"=\begin{pmatrix}%s & %s\\ %s & %s\end{pmatrix}" % tuple(tex_v(v, i % 2) for i, v in enumerate(V2)), Jm.get_right()[0] * 120 + 960 + 10, 480, 34,
                caneta=False)
        cel2, resto = celulas(Jv)
        MC = [("c", "1")]
        self.tabela(Jv, cel2, [
            ("a componente horizontal é constante", F2l.p("c1"), (0, 0), MC, [("v", r"\Am{0}")], ["z"], ("c",)),
            (None, F2l.p("c1"), (0, 1), MC, [("v", r"\Mg{0}")], ["z"], ("c",)),
            ("a vertical um na direção", F2l.p("c2"), (1, 0), MD, [("v", r"\Am{1}")], ["v", "z", "z"], ("m", "y")),
            (None, F2l.p("c2"), (1, 1), MD, [("m", r"\Mg{-}"), ("v", r"\Mg{1}")], ["z", "m", "v"], ("x",))], resto)
        self.gat("tabela zero e zero em cima")
        acende(self, [VGroup(*cel2.values())], BR, 0.8)
        Rs = self.medidas(Ms, cel2, V2, [r"\V1", r"\D{-1}", r"\Lm1", r"\Lm1"],
                          ("rotacional um menos zero", "divergente zero mais", "deformações zero menos", "e um mais zero"))
        sl2, its2 = selos((True, True, True))
        self.gat("previsão tudo junto")
        self.play(FadeIn(sl2), run_time=0.4)
        gt = leg_mix(["GIRA ", r"$\circlearrowleft$", " · ENCOLHE · ENTORTA"], 1120, 868, BR, "left", 32, up=True, bold=True)
        self.gat("gira no sentido anti-horário")
        self.play(FadeOut(sl2), run_time=0.2)                      # v3: o selo sai antes de a frase entrar (sem as duas uma sobre a outra)
        self.remove(sl2)
        self.play(FadeIn(gt), run_time=0.25)
        self.ate(1.0)

        # ── D5-8 · dava para ler no desenho; a seta do centro; solta (alvo 21 v1) ──
        self.an("D5-8")
        ach = {xy: next(s for s in cmp if abs(s._xy[0] - xy[0]) < 1e-6 and abs(s._xy[1] - xy[1]) < 1e-6) for xy in ((1.5, -2.0), (2.5, -2.0), (2.5, -1.0))}
        for fr, cl, pts in (("esse é o um embaixo à esquerda", (1, 0), ((1.5, -2.0), (2.5, -2.0))), ("andando para cima a seta abaixa", (1, 1), ((2.5, -2.0), (2.5, -1.0)))):
            self.gat(fr)                                           # v3 §1.3: as duas setas acendem (só a cor), com a célula da tabela
            self.play(pisca_cor(cel2[cl], AMB if cl == (1, 0) else MAG, 1.0), run_time=0.3)
            acende(self, [ach[p] for p in pts], AMB if cl == (1, 0) else MAG, 1.4)
        fan2 = fantasma(VA, quad_pts(c2, s2_))
        tr = [ponto_fl(fl2, c2, T2 * i / 30) for i in range(31)]
        trl = vlinha(VA, tr, BR, 3, alpha=.9, dash=(6, 7)).set_z_index(8)
        trh = seta7(VA.c2p(*tr[27]), VA.c2p(*tr[30]), BR, 3, 14).set_z_index(8)
        c0 = ponto7(VA.c2p(*c2), BR, 5, 9)
        self.gat("solta o quadradinho viaja")
        self.add(fan2, c0)
        st2["tr"] = clarSeg([(tr[i], tr[i + 1]) for i in range(30)], .2)
        a0 = p2.area()
        self.play(anda(p2, fl2, T2, 2.0, rate=linear, nome="D5 campo ②"), Create(trl), run_time=2.0)
        self.play(FadeIn(trh), run_time=0.3)
        Fc = ponto_fl(fl2, c2, T2)
        gi = giro30(VA, Fc, .7, True)
        st2["giro"] = clarPoly(circ_pts(.8, Fc, 12), .1)
        self.play(Create(gi), run_time=0.4)
        self.lembra_gancho(1, cmp)
        print(f"[D5] ②: área {a0:.4f} → {p2.area():.4f} (× {p2.area() / a0:.3f}; e^(−0,7) = {math.exp(-.7):.3f}); centro {c2} → ({Fc[0]:.3f}, {Fc[1]:.3f})")
        sc = seta7(VA.c2p(*c2), VA.c2p(c2[0] + .5, c2[1] - .6), BR, 5, 19).set_z_index(13)
        self.gat("porque a gente tirou a seta do centro")
        self.play(GrowArrow(sc), run_time=0.5)
        v1_, v2_ = legenda("A VIAGEM É A SETA DO CENTRO,", 1124, 930, GEO, "left", 26), legenda("NÃO ESTÁ NA TABELA", 1124, 970, GEO, "left", 26)
        self.play(FadeIn(v1_, shift=0.05 * UP), FadeIn(v2_, shift=0.05 * UP), run_time=0.4)
        self.ate(1.0)

        # ── D5-9 · campo ③ (alvo v2_d5c1) ──
        self.an("D5-9")
        cmp.clear_updaters()
        zera_chapas()
        ch3 = chapa_px(*LA, nome="D5 ③ palco (360, 780) 240 px/u", v=V3)
        peds = [quad30(V3, p, .3) for p in PTS3]
        fans = [fantasma(V3, quad_pts(p, .3)) for p in PTS3]
        labs = [TXP30(t, *canto_xy(V3, a, b - .04), 26, "center") for t, (a, b) in zip(("(1, 0)", "(0, 1)", "(1, 1)"), LAB3)]
        st3 = {"on": [False] * 3, "fan": False, "lab": False, "giros": []}
        rotl = ou(*[clar28([(a - .3, b - .1, a + .3, b + .1)]) for a, b in LAB3])
        c3 = campo30(V3, F3, -.75, 2.75, -.25, 2.25, .25, rmin=0, mmax=6, nome="D5 f₃")     # v3: sem área livre antes de o rótulo existir
        clareira(c3, lambda: ou(*[clar_ped(p, .12) for p, on in zip(peds, st3["on"]) if on], *([rotl] if st3["lab"] else []),
                                *([dq(p, .3, .12) for p in PTS3] if st3["fan"] else []), *st3["giros"]))
        ex3 = VGroup(linha_rec(V3, [(-.95, 0), (2.95, 0)], LA, GEO, 2, .4), linha_rec(V3, [(0, -.45), (0, 2.45)], LA, GEO, 2, .4))
        F3l = L([("F", r"\F=("), ("c1", r"\X^2-\Y^2"), ("vg", r",\ "), ("c2", r"2\X\Y"), ("f", ")")], 1120, 250, 38)
        self.gat("terceiro campo")
        self.secao_n("O DESAFIO · CAMPO", 3)
        self.limpa_junto()
        troca(self, "D5 campo ② → ③ (muda a origem do palco: a grade nova entra com o campo)")
        self.play(FadeIn(ch3), FadeIn(ex3), cresce_campo(c3, 0.8), run_time=0.8)
        escreve(self, F3l, 0.25)
        J3 = TC(r"J=\begin{pmatrix}\Am{2x} & \Mg{-2y}\\ \Am{2y} & \Mg{2x}\end{pmatrix}", 1120, 485, 34, caneta=False)
        cel3, resto3 = celulas(J3)
        MQ = [("x", r"\X"), ("e", "^2"), ("m", "-"), ("yb", r"\Y"), ("ye", "^2")]
        MP = [("c", "2"), ("x", r"\X"), ("y", r"\Y")]
        self.gat("agora a tabela não é constante")
        F3l = self.chaves(F3l, r"\Pp", r"\Qq")
        self.tabela(J3, cel3, [
            ("derivando a diferença dos quadrados", F3l.p("c1"), (0, 0), MQ, [("e", r"\Am{2}"), ("x", r"\Am{x}")], ["x", "e", "z", "z", "z"], ("m", "yb", "ye"),
             ([("e", "2"), ("x", r"\X"), ("m", "-"), ("z0", "0")], ["x", "e", "m", "z0", "z0"], ["e", "x", "z", "z"])),
            ("em ípsilon o xis ao quadrado", F3l.p("c1"), (0, 1), MQ, [("m", r"\Mg{-}"), ("e", r"\Mg{2}"), ("y", r"\Mg{y}")], ["z", "z", "m", "y", "e"], ("x", "e"),
             ([("z0", "0"), ("m", "-"), ("e", "2"), ("y", r"\Y")], ["z0", "z0", "m", "y", "e"], ["z", "m", "e", "y"])),
            ("derivando duas vezes o produto", F3l.p("c2"), (1, 0), MP, [("c", r"\Am{2}"), ("y", r"\Am{y}")], ["c", "z", "y"], ("x",),
             ([("c", "2"), ("d1", r"\cdot"), ("y", r"\Y"), ("d2", r"\cdot"), ("u", "1")], ["c", "u", "y"], ["c", "z", "y", "z", "z"])),
            (None, F3l.p("c2"), (1, 1), MP, [("c", r"\Mg{2}"), ("x", r"\Mg{x}")], ["c", "x", "z"], ("y",),
             ([("c", "2"), ("d1", r"\cdot"), ("x", r"\X"), ("d2", r"\cdot"), ("u", "1")], ["c", "x", "u"], ["c", "z", "x", "z", "z"]))], resto3)
        self.gat("pausa o vídeo e prevê")
        self.pausa()
        sob = [s for s in c3 if hasattr(s, "_xy") and (rotl(*s._xy) or any(dq(p, .3, .12)(*s._xy) for p in PTS3))]
        self.play(*[FadeIn(f) for f in fans], *[FadeIn(l) for l in labs], *[UpdateFromAlphaFunc(s, lambda m, a: op_seta(m, 1 - a)) for s in sob], run_time=0.5)
        st3["lab"] = st3["fan"] = True
        self.ate(1.0)

        # ── D5-10 · as medidas de ③ (R14 em d₁ e d₂) e a previsão ponto a ponto (alvo v2_d5c2) ──
        self.an("D5-10")
        YM3 = [580, 642, 704, 766]
        M3 = [med(i, y=YM3[i], size=34) for i in range(4)]
        self.gat("rotacional duas vezes a vertical")
        for m in M3[1:]:
            m._origem = "a"
        escreve(self, M3[0], 0.12, extra=[caneta(m, ritmo=0.12) for m in M3[1:]])
        V = {(0, 0): "2x", (0, 1): "-2y", (1, 0): "2y", (1, 1): "2x"}
        res3 = [r"\V{4\Y}", r"\D{4\X}", r"\Lm0", r"\Lm0"]
        R3, riscos = [], []
        for i, fr in enumerate(("rotacional duas vezes a vertical", "divergente duas vezes a horizontal mais", "e as duas deformações cada uma", None)):
            if fr and i:
                self.gat(fr)
            cs = MAE[i][3]
            S = med(i, V[cs[0]], V[cs[1]], y=YM3[i], size=34)
            gm(self, M3[i], S, rt=0.5, voos={"a": cel3[cs[0]], "b": cel3[cs[1]]})
            if i >= 2:
                tr = cancela(self, S, "a", "b", rt=0.2)
                riscos += tr
                R = med(i, V[cs[0]], V[cs[1]], res3[i], y=YM3[i], size=34)
                for g in R.p("a", "b"):
                    g.set_color(CORAL_C)
                R3.append(gm(self, S, R, rt=0.5))
            else:
                R3.append(gm(self, S, med(i, V[cs[0]], V[cs[1]], res3[i], y=YM3[i], size=34), rt=0.5))
        ne = T("NUNCA ENTORTA", 1120, 868, 36, cor=LIMA)
        self.gat("zero em qualquer ponto")
        self.play(FadeIn(ne, shift=0.05 * UP), run_time=0.4)
        FU = L([("r", r"\V{\rot}=\V{4\Y},"), ("d", r"\quad \D{\dv}=\D{4\X},"), ("z", r"\quad d_1=d_2=\Lm0")], 1120, 260, 34)
        self.gat("no ponto um zero")
        AF = Duas(F3l, *R3)
        AF.ks = ["x"] * len(F3l.ks) + ["x"] * 6 + ["r"] + ["x"] * 6 + ["d"] + ["x"] * 6 + ["z"] + ["x"] * 6 + ["z"]
        gm(self, AF, FU, rt=0.8, nota="(fusão)", extra=[FadeOut(J3), FadeOut(ne), *[FadeOut(t) for t in riscos]])
        self.remove(*riscos)
        self.remove(F3l, J3, *R3, ne)
        PT = [("1", "0", r"4\cdot\Mg0=\V0", r"4\cdot\Am1=\D4", "SÓ CRESCE", "quatro vezes zero rotacional", "só cresce"),
              ("0", "1", r"4\cdot\Mg1=\V4", r"4\cdot\Am0=\D0", "SÓ GIRA", "no zero um", "só gira"),
              ("1", "1", r"4\cdot\Mg1=\V4", r"4\cdot\Am1=\D4", "GIRA E CRESCE", "no um um", "gira e cresce")]
        for k, (a, b, rv, dv, lt, f1_, f2_) in enumerate(PT):
            if k:
                self.gat(f1_)
            ln = L([("p", r"(\Am{%s},\Mg{%s}):\ \ " % (a, b)), ("r", r"\V{\rot}=" + rv), ("vg", r",\ \ "), ("d", r"\D{\dv}=" + dv)], 1120, 380 + k * 125, 32)
            ln._origem = "b"
            print(f"[origem] b {self.lote} D5-10 {self.t:.2f} {ln._tex!r} ← rótulo do ponto + linha fundida")
            self.play(TransformFromCopy(labs[k][1], ln.p("p")), TransformFromCopy(FU.p("r"), ln.p("r")), TransformFromCopy(FU.p("d"), ln.p("d")),
                      caneta(ln.p("vg"), ritmo=0.3), run_time=0.7)
            junta(self, ln, "b")
            lg = legenda(lt, 1160, 430 + k * 125, BR, "left", 28)
            self.gat(f2_)
            self.play(FadeIn(lg, shift=0.05 * UP), run_time=0.3)
        self.ate(1.0)

        # ── D5-11 · solta os três; quinas retas; o (1, 1) pequeno ──
        self.an("D5-11")
        self.gat("solta os três")
        for k in range(3):
            st3["on"][k] = True
        self.play(*[FadeIn(p) for p in peds], run_time=0.3)
        a0 = [p.area() for p in peds]
        self.play(*[anda(p, fl3, .1, 2.0, rate=linear, nome=f"D5 ③ {PTS3[i]}") for i, p in enumerate(peds)])
        gs = []
        for p in ((0, 1), (1, 1)):
            Fc = ponto_fl(fl3, p, .1)
            gs.append(giro30(V3, Fc, .3, True))
            st3["giros"].append(clarPoly(circ_pts(.36, Fc, 10), .05))
        self.play(*[Create(g) for g in gs], run_time=0.4)
        for i, p in enumerate(peds):
            q = angulos_quinas(p)
            print(f"[D5] ③ {PTS3[i]}: área {a0[i]:.4f} → {p.area():.4f} (× {p.area() / a0[i]:.3f}); quinas {', '.join(f'{x:.2f}°' for x in q)}; "
                  f"maior desvio do reto {max(abs(x - 90) for x in q):.2f}°")
        mr = marcas_reto(V3, peds[2])
        q1 = legenda("QUINAS RETAS (90°) NOS TRÊS", 1124, 790, GEO, "left", 26)
        self.gat("as quinas continuam em ângulo reto")
        self.play(Create(mr), FadeIn(q1, shift=0.05 * UP), run_time=0.5)
        q2 = legenda("A TABELA FALA DO PONTO, NAQUELE INSTANTE", 1124, 790, GEO, "left", 26)
        self.gat("a tabela fala do que acontece")                # R13: no máximo duas legendas seguidas: a nova toma o lugar da anterior
        troca_linha(self, q1, q2)
        self.gat("um quadradinho de tamanho finito")             # R16: os quadradinhos citados acendem
        acende(self, peds, AMB, 1.0)
        self.gat("e os lados até se curvam")
        acende(self, [peds[1]], CORAL, 1.0)
        pp = quad30(V3, (1, 1), .1, z=8)
        self.gat("bem pequeno esse campo")
        self.play(FadeOut(mr), FadeIn(pp), run_time=0.3)
        self.remove(mr)
        self.play(anda(pp, fl3, .1, 1.5, rate=linear, nome="D5 ③ (1, 1) lado 0,1"))
        print(f"[D5] ③ (1, 1) lado 0,1: quinas {', '.join(f'{x:.2f}°' for x in angulos_quinas(pp))}")
        self.gat("guarda isso")
        self.lembra_gancho(2, c3)
        self.ate(1.0)

        # ── D5-12 · desafio cumprido: a coluna sai (os resultados ficam nos rótulos do palco); a cadeia é escrita sozinha, frase a frase ──
        self.an("D5-12")
        col = [m for m in self.snap() if m.get_center()[0] > PX(1090, 0)[0]]          # fórmulas E legendas da coluna
        res = [TXP30(t, *canto_xy(V3, a, b - .04), 26, "center", BR, bold=True) for t, (a, b) in zip(("SÓ CRESCE", "SÓ GIRA", "GIRA E CRESCE"), LAB3)]
        cad = [T("FÓRMULA", 1120, 500, 34), T("→", 1310, 500, 34, cor=GEO), T("TABELA", 1365, 500, 34), T("→", 1535, 500, 34, cor=GEO),
               T("4 NÚMEROS", 1120, 580, 34), T("→", 1345, 580, 34, cor=GEO), T("QUADRADINHO", 1400, 580, 34)]
        self.gat("desafio cumprido")
        self.play(*[FadeOut(m) for m in col], *[FadeOut(l) for l in labs], run_time=0.3)
        self.play(*[FadeIn(r) for r in res], run_time=0.3)
        self.remove(*col, *labs)
        self.gat("a fórmula do campo vira uma tabela")
        self.play(caneta(cad[0], ritmo=0.12), run_time=0.5)
        self.play(FadeIn(cad[1], shift=0.05 * RIGHT), caneta(cad[2], ritmo=0.12), run_time=0.5)
        self.gat("a tabela vira quatro números")
        self.play(FadeIn(cad[3], shift=0.05 * RIGHT), caneta(cad[4], ritmo=0.12), run_time=0.5)
        self.gat("e os quatro números contam")
        self.play(FadeIn(cad[5], shift=0.05 * RIGHT), caneta(cad[6], ritmo=0.12), run_time=0.5)
        self.gat("e o cê um garante")
        acende(self, cad, LIMA, 1.2)
        c3.clear_updaters()
        self.sai_fim()

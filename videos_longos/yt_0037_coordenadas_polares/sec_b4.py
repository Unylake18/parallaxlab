"""yt_0037 · B4 · o disco do começo — v2 (alvo 06 no B4-1; alvo v2_01 no B4-2; E15–E21). Uma cena 3D só: `casca` (c37.js), câmera do §4.1
enquadrada pelo setViewOffset (G3). B4-1: o sino entra por corte no 1º quadro; a coluna em 3 páginas (G2) — p1 = C4-1…C4-3 (com a miniatura
do retângulo rθ embaixo), p2 = C4-4…C4-7 com o chip x² + y² = r², dA = r dr dθ no topo, p3 = C4-8 com o chip ∫₀¹ e^(−r²) r dr = (1 − 1/e)/2 ≈ 0,316;
a câmera gira poucos graus nos gatilhos da conta (G7: o palco nunca fica parado > 5 s). B4-2: VOLUME ≈ 1,99; o sino vira traço e a casca anda;
o anel lima inteiro (0 → 2π); COMPRIMENTO 2πr, ALTURA e^(−r²), ESPESSURA dr; na coluna, VOLUME DE UMA CASCA ≈ 2πr · e^(−r²) · dr (voos dos
três rótulos), a soma das cascas (GM: o 2π sai da integral), o (1 − 1/e)/2 voando do chip, π(1 − 1/e) e O MESMO VOLUME: ANÉIS × CASCAS."""
from v2kit import *

X4 = 1080
VM = Vw(1130, 760, 120, 100)      # miniatura do retângulo rθ (θ/π em unidades): 200 px de altura, embaixo da página 1
SCC, ZSC = 2.0, .95


def ordx(m, key):
    return sorted(sel(m, key), key=lambda i: m[0][i].get_center()[0])


def sup_sub(m, key):
    ix_ = sel(m, key)
    base = max(ix_, key=lambda i: m[0][i].height)
    resto = [i for i in ix_ if i != base]
    cy = m[0][base].get_center()[1]
    up = sorted([i for i in resto if m[0][i].get_center()[1] >= cy], key=lambda i: m[0][i].get_center()[0])
    lo = sorted([i for i in resto if m[0][i].get_center()[1] < cy], key=lambda i: m[0][i].get_center()[0])
    return base, up, lo


def gl(m, key):
    return VGroup(*[m[0][i] for i in sel(m, key)])


def cam_az(az):
    """A câmera do §4.1 girada az graus em torno do eixo vertical do alvo (0, 0,05)."""
    a = math.radians(az)
    px, py = 7.0, -6.3 - .05
    return cam_esc((px * math.cos(a) - py * math.sin(a), px * math.sin(a) + py * math.cos(a) + .05, 6.4), (0, .05, .45), 540, 560, .9, 40, 102)


def _fonte_de(alvo, fonte):
    alvo._fonte = fonte
    return alvo


class Orbita:
    """Giro curto da câmera disparado por um gatilho de texto (G7): o tracker s vai de 0 a 1 pelo relógio da cena, sem prender o play."""

    def __init__(self, sc, pal):
        self.sc, self.pal = sc, pal

    def vai(self, az, dur=4.0):
        sc, pal = self.sc, self.pal
        s = pal.tr["s"]
        s.clear_updaters()
        pal.rumo(cam_az(az))
        t0 = sc.clk.get_value()

        def f(m):
            u = min(1.0, max(0.0, (sc.clk.get_value() - t0) / dur))
            m.set_value(u * u * (3 - 2 * u))
        s.add_updater(f)
        print(f"[orbita] {sc.lote} {sc._aid} az={az} dur={dur}")

    def para(self):
        self.pal.tr["s"].clear_updaters()


def silhueta(pal):
    """Ponto mais à direita do topo da parede de fora (r₁) e o pé dele, em px — para a chave da ALTURA."""
    r1 = pal.tr["r0"].get_value() + .10
    h = SCC * ZSC * math.exp(-r1 * r1)
    best = None
    for t in np.linspace(0.0, 1.6, 65):
        p = proj_p(pal, (SCC * r1 * math.cos(t), SCC * r1 * math.sin(t), h))
        if best is None or p[0] > best[0][0]:
            best = (p, t)
    (xt, yt), t = best
    xb, yb = proj_p(pal, (SCC * r1 * math.cos(t), SCC * r1 * math.sin(t), 0.0))
    return max(xt, xb), yt, yb


class PB4(B37):
    ANTES = "A RECEITA EM POLARES"
    SUB = "A RETA-SONDA SAI DA ORIGEM"
    CARTAO = True

    def corpo(self):
        # ── B4-1 · o disco do começo (alvo 06) ──
        self.an("B4-1")
        pal = Palco37(self, "casca", CAM_CASCA, traco=0.0, r0=0.45, anel=0.0)
        pal.fundo.op.set_value(1.0)
        self.add(pal.fundo)                                   # E15: o sino entra por corte no 1º quadro do B4-1
        orb = Orbita(self, pal)
        self.secao("O DISCO DO COMEÇO")
        self.subt("PASSO 4 · CALCULAR")
        lx = pal.prende(TC(r"\X", 0, 0, 40, "c"), "ex", 10, -30)        # acima e à direita da ponta (fora da seta e da borda)
        ly = pal.prende(TC(r"\Y", 0, 0, 40, "c"), "ey", 22, -14)     # K10: só no B4-2 (no B4-1 a ponta do eixo y fica atrás do sino opaco)
        lz = pal.prende(TC(r"\Ci{z=e^{-(\X^2+\Y^2)}}", 0, 0, 40, "l"), "ez", 28, 32, "l")
        self.pena(lx, lz, lag=0.05)                                     # K6: o canto troca no 1º play do bloco, com os rótulos do 3D
        self.gat("de volta ao disco")
        L1 = col(L([("ii", r"\iint_{D}"), ("f", r"\Ci{e^{-(\X^2+\Y^2)}}"), ("dA", r"\,dA")], X4, 250, 44))
        self.pena(L1)
        # a miniatura do retângulo rθ (embaixo da página 1, ≥ 200 px)
        self.gat("é um retângulo erre")
        orb.vai(5, 4.0)
        mr = ret_v(VM, 0, 1, 0, 2, mixh(BG_, GEO, .16), z=1)
        mb = borda_v(VM, 0, 1, 0, 2, GEO, 2, z=4)
        ma = VGroup(seta_px(VM.px(0, 0), VM.px(1.35, 0), RR, 3, 14, z=5), seta_px(VM.px(0, 0), VM.px(0, 2.3), TH, 3, 14, z=5))
        mc = ret_v(VM, .5, .75, 1 / 3, .5, mixh(BG_, LI, .8), z=3)
        self.play(FadeIn(mr), Create(mb), Create(ma), FadeIn(mc), run_time=0.6)
        m1 = TC("1", *VM.px(1, -.3), 40, "c")
        m2 = TC(r"2\pi", *VM.px(-.38, 2), 40, "c")
        mlr = TC(r"\R", *VM.px(1.48, 0), 40, "l")
        mlt = TC(r"\T", *VM.px(0, 2.55), 40, "c")
        self.pena(m1, m2, mlr, mlt, lag=0.05)
        mini = [mr, mb, ma, mc, m1, m2, mlr, mlt]
        # o chip, à direita da linha 1 (nada voa por cima dele)
        self.gat("o integrando vira")
        orb.vai(0, 4.0)
        # página 1: o chip em duas linhas à direita da linha 1 (numa linha só ele passaria da borda)
        CHa = L([("xy", r"\X^2+\Y^2"), ("eq1", "="), ("r2", r"\R^2")], 0, 230, 40)
        CHb = L([("dA", "dA"), ("eq2", "="), ("J", r"\J"), ("dr", r"\,\dr"), ("dt", r"\,\dt")], 0, 290, 40)
        x0c = pxof(L1.get_right())[0] + 70
        CHa.shift(RIGHT * ((x0c - pxof(CHa.get_left())[0]) / 120))
        CHb.shift(RIGHT * ((x0c - pxof(CHb.get_left())[0]) / 120))
        CH = VGroup(CHa, CHb)
        self.pena(CHa)
        self.gat("o jacobiano traz o erre")
        self.pena(parte(CHb, sel(CHb, ["dA", "eq2"]), "dA ="))
        voos(self, [(mc.copy(), parte(CHb, sel(CHb, ["J"]), "r lima"))], rt=0.9)
        origem(self, "r lima de dA = r dr dθ", "célula da miniatura rθ (voo)")
        self.pena(parte(CHb, sel(CHb, ["dr", "dt"]), "dr dθ"))
        molc = em_volta(CH, GEO, 16, 2, .55, 10)
        self.play(Create(molc), run_time=0.3)                 # a moldura nasce depois do texto (G4)
        # GM6: ∬_D e^(−(x²+y²)) dA → ∫₀^{2π}∫₀¹ e^(−r²) · r dr dθ (a linha de baixo, colada na 1)
        self.gat("a integral fica")
        orb.vai(5, 4.0)
        L3 = col(L([("eq", "="), ("i1", r"\displaystyle\int_0^{2\pi}"), ("i2", r"\!\!\int_0^{1}"), ("f", r"\Ci{e^{-\R^2}}"), ("c", r"\cdot"), ("J", r"\J"),
                    ("dr", r"\,\dr"), ("dt", r"\,\dt")], X4, 0, 44))
        abaixo(L1, L3, X4, 66)                                  # abaixo do chip de duas linhas
        fA, fB = ordx(L1, "f"), ordx(L3, "f")
        b1, u1, l1 = sup_sub(L3, "i1")
        b2, u2, l2 = sup_sub(L3, "i2")
        gmap(self, 6, L1, L3, [(ordx(L1, "ii")[:1], [b1, b2]), (fA[0:2], fB[0:2])],
             voos=[(CHa[0][sel(CHa, "r2")[0]:sel(CHa, "r2")[-1] + 1].copy(), fB[2:4]),
                   (CHb[0][sel(CHb, "J")[0]:sel(CHb, "dt")[-1] + 1].copy(), sel(L3, ["J", "dr", "dt"])),
                   (m2.copy(), u1), (m1.copy(), u2)], rt=1.4, nota="x²+y² → r², dA → r dr dθ (do chip); 1 e 2π da miniatura")
        origem(self, "limites 1 e 2π", "miniatura do retângulo rθ (voos)")
        degrau(self, "B4-1 disco", "∬_D e^(−(x²+y²)) dA = ∫₀^{2π}∫₀¹ e^(−r²) · r dr dθ")
        self.gat("vezes erre dê erre")
        orb.vai(0, 4.0)
        # o r é o fator que faltava
        self.gat("e olha o que esse")
        acende(self, (L3[0][sel(L3, "J")[0]:sel(L3, "J")[-1] + 1], LI), rt=0.8)
        self.gat("o fator que faltava")
        orb.vai(5, 4.0)
        # ── página 2: o chip sobe; a de dentro fica; o resto sai (G2)
        self.gat("chama u de erre")
        inner = sel(L3, ["i2", "f", "c", "J", "dr"])
        resto3 = [L3[0][k] for k in range(len(L3[0])) if k not in inner]
        sai = saindo([L1, *mini, *resto3])
        self.play(*[FadeOut(m) for m in sai], run_time=0.3)
        self.remove(L1, *mini)
        P0 = col(L([("i", r"\displaystyle\int_0^{1}"), ("f", r"\Ci{e^{-\R^2}}"), ("c", r"\cdot"), ("J", r"\J"), ("dr", r"\,\dr")], X4, 0, 44))
        P0.shift(UP * ((pxof(P0.get_center())[1] - 362) / 120))
        P0.shift(RIGHT * ((X4 - pxof(P0.get_left())[0]) / 120))
        kp0 = ja_escrita(parte(P0, list(range(len(P0[0]))), "de dentro"))
        kp0._col = True
        src = VGroup(*[L3[0][k] for k in inner])
        # o chip vira uma linha só no topo: a 1ª linha vai para a esquerda, a 2ª sobe para o lado dela; a moldura renasce depois (G4)
        da = PX(X4 + 12, 250) - np.array([CHa.get_left()[0], CHa.get_center()[1], 0])
        db = PX(X4 + 12 + CHa.width * 120 + 40, 250) - np.array([CHb.get_left()[0], CHb.get_center()[1], 0])
        sm = saindo([molc])
        self.play(FadeOut(molc), CHa.animate.shift(da), ReplacementTransform(src, kp0), run_time=0.5)
        self.play(CHb.animate.shift(db), run_time=0.4)        # a 2ª linha sobe depois que a 1ª abriu espaço (sem cruzar)
        self.remove(L3, molc)
        molc = em_volta(CH, GEO, 12, 2, .55, 10)
        self.play(Create(molc), run_time=0.3)
        self.subt("A DE DENTRO, POR SUBSTITUIÇÃO")
        S = col(L([("u", r"\uu=\R^2"), ("i1", r"\ \Rightarrow\ "), ("du", r"\du=2\R\,\dr"), ("i2", r"\ \Rightarrow\ "), ("p", r"\R\,\dr=\dfrac{\du}{2}")],
                  X4, 0, 40))
        abaixo(P0, S, X4, 26)
        self.pena(parte(S, sel(S, ["u"]), "u = r²"))
        degrau(self, "B4-1 substituição", "u = r²")
        self.gat("dê u é dois")
        orb.vai(0, 4.0)
        self.pena(parte(S, sel(S, ["i1", "du"]), "⇒ du = 2r dr"))
        degrau(self, "B4-1 substituição", "du = 2r dr")
        self.gat("então erre dê erre vira")
        self.pena(parte(S, sel(S, ["i2", "p"]), "⇒ r dr = du/2"))
        degrau(self, "B4-1 substituição", "r dr = du/2")
        self.gat("e os limites erre zero")
        orb.vai(5, 4.0)
        Lm = col(L([("a", r"\R=0\to\uu="), ("ua", "0"), ("v", r",\ \ "), ("b", r"\R=1\to\uu="), ("ub", "1")], X4, 0, 40))     # estreita: o du/2 desce pela direita dela
        abaixo(S, Lm, X4, 20)
        self.pena(parte(Lm, sel(Lm, ["a", "ua"]), "r = 0 → u = 0"))
        degrau(self, "B4-1 limites novos", "r = 0 → u = 0")
        self.gat("erre um dá u um")
        self.pena(parte(Lm, sel(Lm, ["v", "b", "ub"]), "r = 1 → u = 1"))
        degrau(self, "B4-1 limites novos", "r = 1 → u = 1")
        # GM7: ∫₀¹ e^(−u) du/2 → [−e^(−u)/2]₀¹ → −e^(−1)/2 − (−1/2) → (1 − 1/e)/2
        self.gat("fica a integral de zero")
        orb.vai(0, 4.0)
        P1 = col(L([("eq", "="), ("i", r"\displaystyle\int_0^{1}"), ("f", r"\Ci{e^{-\uu}}"), ("du", r"\,\dfrac{\du}{2}")], X4, 0, 44))
        abaixo(Lm, P1, X4, 28)
        bi1, ui1, li1 = sup_sub(P1, "i")
        _, nu1, ba1, de1 = frac_partes(P1, "du")
        escreve_seq(self, P1, [(S[0][sel(S, "p")[-4]:sel(S, "p")[-1] + 1], nu1 + ba1 + de1, 2.4), (Lm[0][sel(Lm, "ua")[0]:sel(Lm, "ua")[0] + 1], li1),
                               (Lm[0][sel(Lm, "ub")[0]:sel(Lm, "ub")[0] + 1], ui1)], rt_voo=0.7, passo=0.04)
        origem(self, "du/2 e limites 0, 1", "linha da substituição e linha dos limites novos (voos)")
        degrau(self, "B4-1 de dentro", "∫₀¹ e^(−r²) r dr = ∫₀¹ e^(−u) du/2")
        self.gat("a primitiva é menos")
        orb.vai(5, 4.0)
        P2 = col(L([("eq", "="), ("lb", r"\Big["), ("F", r"-\dfrac{\Ci{e^{-\uu}}}{2}"), ("rb", r"\Big]_0^1")], X4, 0, 44))
        abaixo(P1, P2, X4, 30)                                  # FINAL: a primitiva na linha de baixo (os voos do P3 não cruzam o P1)
        f1 = ordx(P1, "f")
        rbI = sel(P2, "rb")
        upB = max(rbI[1:], key=lambda i: P2[0][i].get_center()[1])
        loB = min(rbI[1:], key=lambda i: P2[0][i].get_center()[1])
        fo2, nu2, ba2, de2 = frac_partes(P2, "F")
        gmap(self, 7, P1, P2, [("eq", "eq"), (f1, nu2), (ba1 + de1, ba2 + de2), (ui1, [upB]), (li1, [loB])], rt=1.3, nota="b) primitiva [−e^(−u)/2]₀¹")
        degrau(self, "B4-1 de dentro", "= [−e^(−u)/2]₀¹")
        # ── K9 · página 2b: a coluna limpa (sai o chip da substituição e os degraus S e Lm); o P0 e a linha P1|P2 sobem ──
        self.gat("em um menos é elevado")
        orb.vai(0, 4.0)
        sai = saindo([CHa, CHb, molc, S, Lm])
        d0 = UP * ((pxof(kp0.get_center())[1] - 262) / 120)
        d1 = UP * ((pxof(P1.get_center())[1] - 362) / 120)
        self.play(*[FadeOut(m) for m in sai], kp0.animate.shift(d0), P1.animate.shift(d1), P2.animate.shift(d1), run_time=0.5)
        self.remove(CHa, CHb, molc, S, Lm)
        P3 = col(L([("eq", "="), ("a", r"-\dfrac{\Ci{e^{-1}}}{2}"), ("m", "-"), ("po", r"\Big("), ("b", r"-\dfrac{\Ci{e^{0}}}{2}"), ("pc", r"\Big)")], X4, 0, 44))
        abaixo(P2, P3, X4, 30)
        fa3, na3, ba3, da3 = frac_partes(P3, "a")
        fb3, nb3, bb3, db3 = frac_partes(P3, "b")
        c2 = lambda idx: VGroup(*[P2[0][i_].copy() for i_ in idx])            # cópias da primitiva (a fonte fica: ninguém é mapeado duas vezes)
        self.pena(parte(P3, sel(P3, ["eq"]), "="))
        # F(1): o 1 do limite de cima vira o expoente −1; o resto da primitiva voa (cópia)
        voos(self, [(c2(fo2), _fonte_de(parte(P3, fa3, "−"), P2)), (c2(nu2[:2]), _fonte_de(parte(P3, na3[:2], "e −"), P2)),
                    (c2([upB]), _fonte_de(parte(P3, na3[2:3], "1"), P2)), (c2(ba2 + de2), _fonte_de(parte(P3, ba3 + da3, "/2"), P2))], rt=1.1)
        origem(self, "F(1) = −e^(−1)/2", "primitiva [−e^(−u)/2] e o 1 do limite de cima (voos)")
        degrau(self, "B4-1 de dentro", "F(1) = −e^(−1)/2   [o 1 do limite vira o expoente]")
        # F(0): o 0 do limite de baixo vira o expoente 0
        self.gat("em zero menos é elevado")
        orb.vai(5, 4.0)
        self.pena(parte(P3, sel(P3, ["m", "po"]), "− ("))
        voos(self, [(c2(fo2), _fonte_de(parte(P3, fb3, "−"), P2)), (c2(nu2[:1]), _fonte_de(parte(P3, nb3[:1], "e"), P2)),
                    (c2([loB]), _fonte_de(parte(P3, nb3[1:2], "0"), P2)), (c2(ba2 + de2), _fonte_de(parte(P3, bb3 + db3, "/2"), P2))], rt=1.1)
        self.pena(parte(P3, sel(P3, ["pc"]), ")"))
        origem(self, "F(0) = −e⁰/2", "primitiva [−e^(−u)/2] e o 0 do limite de baixo (voos)")
        degrau(self, "B4-1 de dentro", "F(1) − F(0) = −e^(−1)/2 − (−e⁰/2)   [o 0 do limite vira o expoente]")
        # P4: e^(−1) → 1/e, e⁰ → 1, −(− → +
        self.gat("menos com menos dá mais")
        orb.vai(0, 4.0)
        P4 = col(L([("eq", "="), ("a", r"-\dfrac{1}{2\Ci{e}}"), ("p", "+"), ("b", r"\dfrac{1}{2}")], X4, 0, 44))
        abaixo(P3, P4, X4, 34)
        fa4, na4, ba4, da4 = frac_partes(P4, "a")
        fb4, na4b, bb4, db4 = frac_partes(P4, "b")
        gmap(self, 7, P3, P4, [("eq", "eq"), (fa3, fa4), (na3[2:3], na4), (na3[0:1], da4[1:2]), (ba3, ba4), (da3, da4[0:1]),
                               (sel(P3, ["m", "po"]) + fb3, sel(P4, ["p"])), (nb3, na4b), (bb3, bb4), (db3, db4)],
             rt=1.5, nota="d) e^(−1) → 1/e, e⁰ → 1, −(− → +")
        degrau(self, "B4-1 de dentro", "e⁰ = 1   (e^(−1) = 1/e;  menos com menos dá mais)")
        degrau(self, "B4-1 de dentro", "= −1/(2e) + 1/2")
        # P5: o 1/2 em evidência
        self.gat("a metade de um menos")
        orb.vai(5, 4.0)
        P5 = col(L([("eq", "="), ("fr", r"\dfrac{1-1/e}{2}")], X4, 0, 44))
        abaixo(P4, P5, X4, 34)
        _, n5, b5, d5 = frac_partes(P5, "fr")
        gmap(self, 7, P4, P5, [("eq", "eq"), (na4b, n5[0:1]), (fa4, n5[1:2]), (na4, n5[2:3]), (da4[1:2], n5[4:5]), (bb4, b5), (db4, d5)],
             rt=1.3, nota="e) (1 − 1/e)/2")
        degrau(self, "B4-1 de dentro", "= (1 − 1/e)/2")
        # ── página 3: o chip da de dentro (E16) ──
        self.gat("guarda esse número")
        orb.vai(0, 3.0)
        KI = L([("i", r"\displaystyle\int_0^{1}"), ("f", r"\Ci{e^{-\R^2}}"), ("J", r"\J"), ("dr", r"\,\dr"), ("eq", "="), ("fr", r"\dfrac{1-1/e}{2}"),
                ("ap", r"\approx 0{,}316")], X4 + 12, 0, 40)
        KI.shift(UP * ((pxof(KI.get_center())[1] - 262) / 120))
        cdot = P0[0][sel(P0, "c")[0]]
        sai = saindo([P1, P2, P3, P4, cdot])
        self.play(*[FadeOut(m) for m in sai], run_time=0.3)
        self.remove(P1, P2, P3, P4, cdot)
        keep = [k for k in range(len(P0[0])) if k not in sel(P0, "c")]
        kki = ja_escrita(parte(KI, sel(KI, ["i", "f", "J", "dr"]) + sel(KI, ["eq", "fr"]), "chip"))
        src = VGroup(*[P0[0][k] for k in keep], *P5[0])
        self.play(ReplacementTransform(src, kki), run_time=0.7)
        self.remove(kp0, P5)
        self.subt("A DE FORA: SÓ MULTIPLICA")
        self.gat("zero vírgula três um")
        self.pena(parte(KI, sel(KI, ["ap"]), "≈ 0,316"))
        molk = em_volta(KI, LI, 12, 2, .8, 10)
        self.play(Create(molk), run_time=0.3)
        # GM8: ∫₀^{2π} (1 − 1/e)/2 dθ → 2π · (1 − 1/e)/2 → π(1 − 1/e)
        self.gat("só multiplica por dois")
        orb.vai(5, 4.0)
        Q0 = col(L([("i", r"\displaystyle\int_0^{2\pi}"), ("fr", r"\dfrac{1-1/e}{2}"), ("dt", r"\,\dt")], X4, 0, 44))
        abaixo(KI, Q0, X4, 50)
        bq, uq, lq = sup_sub(Q0, "i")
        escreve_seq(self, Q0, [(KI[0][sel(KI, "fr")[0]:sel(KI, "fr")[-1] + 1], "fr")], rt_voo=0.8, passo=0.04)
        origem(self, "(1 − 1/e)/2 da linha de fora", "chip da de dentro (voo)")
        Q1 = col(L([("eq", "="), ("tp", r"2\pi"), ("c", r"\cdot"), ("fr", r"\dfrac{1-1/e}{2}")], X4, 0, 44))
        ao_lado(Q0, Q1, 14, ia=sel(Q0, "fr")[0], ib=sel(Q1, "fr")[0])
        Q1.shift(UP * (Q0[0][sel(Q0, "fr")[0]].get_center()[1] - Q1[0][sel(Q1, "fr")[0]].get_center()[1]))
        gmap(self, 8, Q0, Q1, [(uq, "tp"), ("fr", "fr")], rt=1.2, nota="a) 2π · (1 − 1/e)/2")
        degrau(self, "B4-1 de fora", "∫₀^{2π} (1 − 1/e)/2 dθ = 2π · (1 − 1/e)/2")
        self.gat("pi vezes a diferença")
        orb.vai(0, 4.0)
        tp_ = ordx(Q1, "tp")
        _, nq, bq_, dq = frac_partes(Q1, "fr")
        acende(self, (Q1[0][tp_[0]:tp_[0] + 1], AL), (VGroup(*[Q1[0][i] for i in bq_ + dq]), AL), rt=0.5)
        Q2 = col(L([("eq", "="), ("r", r"\Me{\pi\,(1-1/e)}")], X4, 0, 44))
        abaixo(Q0, Q2, X4 + 40, 34)
        rq = ordx(Q2, "r")
        gmap(self, 8, Q1, Q2, [("eq", "eq"), (tp_[1:2], rq[0:1]), (nq, rq[2:7])], rt=1.2, nota="b) o 2 cancela: π(1 − 1/e)")
        degrau(self, "B4-1 de fora", "= π(1 − 1/e)")
        self.gat("mais ou menos um")
        ap2 = col(TC(r"\approx 1{,}986", 0, 0, 44, "l"))
        ao_lado(Q2, ap2, 14)
        self.pena(ap2)
        self.marca("06")
        orb.para()
        # ── B4-2 · o anel, a casca e o volume (alvo v2_01, cena casca §4.1) ──
        self.an("B4-2")
        self.subt("A CASCA DE RAIO r")
        self.gat("o volume debaixo do")
        vt = T("VOLUME ≈", 0, 0, 30, "left", BR)
        vm = TC(r"1{,}99", 0, 0, 40, "l")
        vm.next_to(vt, RIGHT, buff=12 / 120)
        vm.shift(UP * (vt.get_center()[1] - vm.get_center()[1]))
        VV = VGroup(vt, vm)
        VV.shift(PX(560, 196) - np.array([VV.get_left()[0], VV.get_center()[1], 0]))
        lz_ = saindo([lz])
        self.play(FadeOut(lz), run_time=0.3)
        self.remove(lz)
        self.pena(vt, vm, lag=0.1)
        # o sino vira traço e a casca acende em r₀ = 0,45
        self.gat("cada anel fino")
        self.pena(ly, rt=1.0, extra=pal.anim(1.0, traco=1.0, rate=linear))          # K10: o y nasce junto, preso à ponta (agora visível) do eixo y
        self.gat("uma altura só é")
        self.play(*pal.anim(1.4, r0=0.10), run_time=1.4)
        self.play(*pal.anim(2.4, r0=0.85), run_time=2.4)
        self.play(*pal.anim(1.2, r0=0.45), run_time=1.2)
        # COMPRIMENTO 2πr: o anel lima inteiro (0 → 2π, sem raio) e a guia até a base da frente
        self.gat("o comprimento é dois")
        ct = T("COMPRIMENTO", 70, 1022, 30, "left", LI)
        cm = TC(r"\Li{2\pi}\,\J", 0, 0, 40, "l")
        cm.next_to(ct, RIGHT, buff=14 / 120)
        cm.shift(UP * (ct.get_center()[1] - cm.get_center()[1]))
        gC = always_redraw(lambda: seta_px((260, 990), pal.pt("baseFrente"), LI, 2.5, 12, z=7))
        for x in gC.get_family():
            x._guia_de = ct
        gC._guia_de = ct
        self.play(*pal.anim(2.0, anel=1.0, rate=linear), run_time=2.0)
        self.pena(ct, cm, lag=0.1, extra=[Create(gC)])
        origem(self, "COMPRIMENTO 2πr", "anel lima da base da casca")
        # ALTURA e^(−r²): a chave ciano ao lado da parede
        self.gat("a altura é é")

        def chave():
            x, yt, yb = silhueta(pal)
            x += 22
            return lin_px([(x - 10, yt + 4), (x, yt + 4), (x, yb - 4), (x - 10, yb - 4)], CI, 3, z=8)
        ch = always_redraw(chave)
        at = T("ALTURA", 0, 0, 30, "left", CI)
        am = TC(r"\Ci{e^{-\R^2}}", 0, 0, 40, "l")
        am.next_to(at, DOWN, buff=8 / 120, aligned_edge=LEFT)
        pla = placa_min(VGroup(at, am), 8, 6)
        AG = VGroup(pla, at, am)
        ok3d(AG)
        for x in ch.get_family():
            x._guia_de = at

        def poe_alt(m):
            x, yt, yb = silhueta(pal)
            alvo = PX(max(x + 22 + 18, pal.pt("ey")[0] + 30), (yt + yb) / 2)          # K11: nunca por cima da seta do eixo y
            m.shift(alvo - np.array([m.get_left()[0], m.get_center()[1], 0]))
        poe_alt(AG)
        pla.add_updater(lambda m: poe_alt(AG))           # a placa leva o rótulo junto (os três andam com a casca)
        self.play(Create(ch), run_time=0.5)
        self.pena(at, am, lag=0.1, extra=[FadeIn(pla)])
        # ESPESSURA dr: seta até a faixa do teto
        self.gat("e a espessura é")
        et = T("ESPESSURA", 812, 262, 30, "left", RR)
        em = TC(r"\dr", 0, 0, 40, "l")
        em.next_to(et, RIGHT, buff=12 / 120)
        em.shift(UP * (et.get_center()[1] - em.get_center()[1]))
        sE = always_redraw(lambda: seta_px((850, 286), pal.pt("tetoMeio"), RR, 2.5, 12, z=8))
        for x in sE.get_family():
            x._guia_de = et
        sE._guia_de = et
        self.pena(et, em, lag=0.1)
        self.play(Create(sE), run_time=0.5)
        # a coluna limpa (G2); o chip desce; VOLUME DE UMA CASCA ≈ 2πr · e^(−r²) · dr (voos dos três rótulos)
        self.gat("o volume da casca é")
        sai = saindo([Q0, Q1, Q2, ap2])
        self.play(*[FadeOut(m) for m in sai], run_time=0.3)
        self.remove(Q0, Q1, Q2, ap2)
        dk = DOWN * ((866 - pxof(KI.get_center())[1]) / 120)
        self.play(KI.animate.shift(dk), molk.animate.shift(dk), run_time=0.5)
        tv = T("VOLUME DE UMA CASCA", X4, 262, 32, "left", CANTO_S)
        self.pena(tv, passo=0.025)
        R1 = col(L([("ap", r"\approx"), ("tp", r"\Li{2\pi}\,\J"), ("c1", r"\cdot"), ("e", r"\Ci{e^{-\R^2}}"), ("c2", r"\cdot"), ("dr", r"\dr")], X4, 0, 46))
        R1.shift(UP * ((pxof(R1.get_center())[1] - 340) / 120))
        escreve_seq(self, R1, [(cm, "tp", 1.2), (am, "e", -2.0), (em, "dr", -0.9)], rt_voo=0.9, passo=0.04)
        origem(self, "2πr · e^(−r²) · dr", "rótulos COMPRIMENTO, ALTURA e ESPESSURA (voos)")
        degrau(self, "B4-2 casca", "volume da casca ≈ 2πr · e^(−r²) · dr")
        # a soma das cascas: a casca anda de novo; ∫₀¹ 2πr e^(−r²) dr = 2π ∫₀¹ e^(−r²) r dr
        self.gat("somando as cascas")
        self.play(*pal.anim(0.9, r0=0.10), run_time=0.9)
        self.play(*pal.anim(2.2, r0=0.85), run_time=2.2)
        self.play(*pal.anim(0.9, r0=0.45), run_time=0.9)
        R2a = col(L([("i", r"\displaystyle\int_0^{1}"), ("tp", r"2\pi"), ("J", r"\,\J"), ("e", r"\Ci{e^{-\R^2}}"), ("dr", r"\,\dr")], X4, 0, 46))
        abaixo(R1, R2a, X4, 44)
        escreve_seq(self, R2a, [(gl(R1, "tp"), sel(R2a, ["tp", "J"])), (gl(R1, "e"), "e"), (gl(R1, "dr"), "dr")], rt_voo=0.8, passo=0.04)
        degrau(self, "B4-2 soma", "∫₀¹ 2πr e^(−r²) dr")
        self.gat("dois pi vezes a integral")
        R2b = col(L([("eq", "="), ("tp", r"2\pi"), ("i", r"\displaystyle\int_0^{1}"), ("e", r"\Ci{e^{-\R^2}}"), ("J", r"\J"), ("dr", r"\,\dr")], X4, 0, 46))
        ao_lado(R2a, R2b, 16, ia=sel(R2a, "i")[0], ib=sel(R2b, "i")[0])
        gmap(self, 9, R2a, R2b, [("tp", "tp"), ("i", "i"), ("e", "e"), ("J", "J"), ("dr", "dr")], rt=1.3, nota="o 2π sai da integral")
        degrau(self, "B4-2 soma", "= 2π ∫₀¹ e^(−r²) r dr")
        # o (1 − 1/e)/2 voa do chip da página 3
        self.gat("acabou de fazer")
        R3 = col(L([("eq", "="), ("tp", r"2\pi"), ("c", r"\cdot"), ("fr", r"\dfrac{1-1/e}{2}")], X4, 0, 46))
        abaixo(R2a, R3, X4, 36)
        escreve_seq(self, R3, [(gl(R2a, "tp"), "tp"), (gl(KI, "fr"), "fr")], rt_voo=0.9, passo=0.04)
        origem(self, "(1 − 1/e)/2 da soma das cascas", "chip ∫₀¹ e^(−r²) r dr = (1 − 1/e)/2 (voo)")
        degrau(self, "B4-2 soma", "= 2π · (1 − 1/e)/2")
        self.gat("de novo pi vezes")
        R4 = col(L([("eq", "="), ("r", r"\Me{\pi\,(1-1/e)}")], X4, 0, 46))
        ao_lado(R3, R4, 16)
        t3 = ordx(R3, "tp")
        _, n3, b3_, d3 = frac_partes(R3, "fr")
        r4 = ordx(R4, "r")
        gmap(self, 9, R3, R4, [("eq", "eq"), (t3[1:2], r4[0:1]), (n3, r4[2:7])], rt=1.2, nota="o 2 cancela: π(1 − 1/e)")
        degrau(self, "B4-2 soma", "= π(1 − 1/e)")
        lmv = leg("O MESMO VOLUME: ANÉIS × CASCAS", X4, pxof(R3.get_bottom())[1] + 52, MEN, "left", 30)
        self.pena(lmv, passo=0.025)
        self.gat("o comprimento do anel")
        acende(self, (cm, LI), rt=0.8)
        self.marca("v2_01")
        self.sai_fim()

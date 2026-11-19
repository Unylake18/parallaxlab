"""yt_0037 · B2 · de onde vem o r — v2 (alvos 03, 04 em cima e v2_02; E06–E11). B2-1: o quarto de plano (grade polar até r = 2,2), o setor acende,
o setor pequeno some e sobra a célula; coluna (44 px) com os glyph maps 1 e 2 (a metade da soma vira r̄ e a diferença vira Δr, com a chave no
desenho); π/16 e 7π/48 com os voos glifo a glifo; cada célula ganha o valor numa placa só (E07); a de fora ocupa exatamente r ∈ [1,5; 2] (E08).
B2-2: a lupa (E09): a grade pequena com a célula à esquerda e a ampliação ao lado, ligadas por duas linhas-guia; rΔθ e Δr por fora; ÁREA ≈ r Δr Δθ;
o jacobiano escrito em ordem (E10) e o glyph map 3; o chip dA = r dr dθ. B2-3 (alvo v2_02, E11): SEM O r ✗ e COM O r ✓ com os glyph maps 4 e 5
e o degrau (a²/2 − 0); o perímetro em ALERTA e a área em menta no disco."""
from v2kit import *

VQ = Vw(170, 980, 320)            # B2-1: quarto de plano
VP = Vw(100, 950, 175)            # B2-2: a grade pequena (a lupa parte dela)
VD = Vw(480, 650, 285)            # B2-3: disco de raio a (alvo v2_02)
T6, T3 = math.pi / 6, math.pi / 3
X1 = 1060                         # coluna do B2-1 e do B2-2
LUP = (470, 250, 1000, 950)       # painel da lupa (px)
KZ = 175 * 2.7
VZ = Vw(735 - 1.75 * math.cos(math.pi / 4) * KZ, 600 + 1.75 * math.sin(math.pi / 4) * KZ, KZ)


def lbase(m, key):
    ix_ = sel(m, key)
    b = ix_[0]
    resto = ix_[1:]
    sub = min(resto, key=lambda i: m[0][i].get_center()[1]) if resto else None
    return [b] + ([sub] if sub is not None else [])


def sup_sub(m, key):
    ix_ = sel(m, key)
    base = max(ix_, key=lambda i: m[0][i].height)
    resto = [i for i in ix_ if i != base]
    cy = m[0][base].get_center()[1]
    up = sorted([i for i in resto if m[0][i].get_center()[1] >= cy], key=lambda i: m[0][i].get_center()[0])
    lo = sorted([i for i in resto if m[0][i].get_center()[1] < cy], key=lambda i: m[0][i].get_center()[0])
    return base, up, lo


def ordx(m, key):
    return sorted(sel(m, key), key=lambda i: m[0][i].get_center()[0])


def rot_txt(s, X, Y, size=34, cor=BR):
    return T(s, X, Y, size, "left", cor)


def cel_pol(v, r1, r2, alpha=.55, w=3):
    return setor(v, r1, r2, T6, T3, fill=mixh(BG_, LI, alpha), stroke=LI, wpx=w, z=4)


def fonte(alvo, src):
    alvo._fonte = src
    return alvo


class PB2(B37):
    ANTES = "COORDENADAS POLARES"
    SUB = "A GRADE DO PLANO rθ VIRA CÍRCULOS E RAIOS"
    CARTAO = True

    def corpo(self):
        v = VQ
        # ── B2-1 · o retângulo polar: diferença de setores (alvo 03) ──
        self.an("B2-1")
        self.secao("O RETÂNGULO POLAR")
        self.subt("MESMO Δr, MESMO Δθ, ÁREAS DIFERENTES")
        g = papel_v(v, (-.1, 2.3, -.1, 2.3))
        self.grade = g
        sx, sy, lx, ly = eixos_xy(v, -.1, 2.4, -.1, 2.35, size=40)
        gp = gpolar(v, 2, 4, 3, 0, math.pi / 2)
        g22 = VGroup(*[lin_px([v.px(2 * math.cos(t), 2 * math.sin(t)), v.px(2.2 * math.cos(t), 2.2 * math.sin(t))], GEO, 1.6, alpha=.42, z=3)
                       for t in (0, T6, T3, math.pi / 2)], arco(v, 2.2, 0, math.pi / 2, GEO, 1.6, z=3, alpha=.42))
        self.play(FadeIn(g), GrowFromPoint(sx, v.P(0, 0)), GrowFromPoint(sy, v.P(0, 0)), Create(gp), Create(g22), run_time=0.4)
        self.pena(lx, ly, lag=0.05)
        self.gat("quanto vale a área de um")
        c1 = cel_pol(v, .5, 1)
        self.play(FadeIn(c1[0]), Create(c1[1]), run_time=0.6)
        self.gat("de raios erre um")
        r1l = TC(r"\R_1", *[a + b for a, b in zip(v.px(.5, 0), (0, 40))], 40, "c")
        r2l = TC(r"\R_2", *[a + b for a, b in zip(v.px(1, 0), (0, 40))], 40, "c")
        mk = VGroup(lin_px([v.px(.5, -.03), v.px(.5, .03)], GEO, 2, z=6), lin_px([v.px(1, -.03), v.px(1, .03)], GEO, 2, z=6))
        self.play(Create(mk), run_time=0.3)
        self.pena(r1l, r2l, lag=0.1)
        self.gat("um ângulo delta téta")
        adt = arco(v, .3, T6, T3, TH, 4, z=7)
        ldt = dentro(TC(r"\Dt", *v.px(.41 * math.cos(math.pi / 4), .41 * math.sin(math.pi / 4)), 40, "c"))     # dentro da cunha que nomeia
        self.play(Create(adt), run_time=0.5)
        self.pena(ldt)
        self.gat("começa pelo setor")
        sg = setor(v, 0, 1, T6, T3, fill=mixh(BG_, LI, .18), z=2)
        self.play(FadeOut(c1), FadeIn(sg), run_time=0.7)
        self.remove(c1)
        self.gat("o círculo de raio erre")
        ar2 = arco(v, 1, T6, T3, RR, 5, z=7)
        self.play(Create(ar2), run_time=0.5)
        S1t = rot_txt("SETOR", X1, 268)
        S1 = col(L([("eq", "="), ("pi", r"\pi"), ("r2", r"\R^2"), ("c", r"\cdot"), ("fr", r"\dfrac{\Dt}{2\pi}"), ("e2", "="), ("h", r"\dfrac{1}{2}"),
                    ("q2", r"\R^2"), ("d", r"\,\Dt")], pxof(S1t.get_right())[0] + 14, 256, 44))
        self.pena(S1t)
        self.pena(parte(S1, sel(S1, ["eq", "pi", "r2"]), "= πr²"))
        self.gat("a fração delta téta")
        self.pena(parte(S1, sel(S1, ["c", "fr"]), "· Δθ/2π"))
        self.gat("então o setor tem área")
        self.pena(parte(S1, sel(S1, ["e2", "h", "q2", "d"]), "= ½ r² Δθ"))
        degrau(self, "B2-1 setor", "πr² · Δθ/2π = ½ r² Δθ")
        self.gat("a célula é o setor grande")
        ar1 = arco(v, .5, T6, T3, AZC, 4, dash=(8, 6), z=7)
        sp = setor(v, 0, .5, T6, T3, fill=mixh(BG_, AZC, .30), z=3)
        self.play(Create(ar1), FadeIn(sp), run_time=0.6)
        c1 = cel_pol(v, .5, 1)
        self.play(Transform(sg, c1[0]), FadeOut(sp), FadeOut(ar1), Create(c1[1]), run_time=1.2)
        self.remove(sp, ar1)
        lcel = leg("CÉLULA = SETOR GRANDE − SETOR PEQUENO", X1, 1000, LI, "left", 30)
        self.pena(lcel, passo=0.025)
        self.gat("um meio de erre dois")
        S2t = rot_txt("CÉLULA", X1, 383)
        L2 = col(L([("eq", "="), ("h1", r"\dfrac{1}{2}"), ("a2", r"\R_2^2"), ("d1", r"\,\Dt"), ("m", "-"), ("h2", r"\dfrac{1}{2}"), ("a1", r"\R_1^2"),
                    ("d2", r"\,\Dt")], pxof(S2t.get_right())[0] + 14, 371, 44))
        self.pena(S2t)
        self.pena(parte(L2, sel(L2, ["eq", "h1", "a2", "d1"]), "= ½ r₂² Δθ"))
        self.gat("menos um meio de erre um")
        self.pena(parte(L2, sel(L2, ["m", "h2", "a1", "d2"]), "− ½ r₁² Δθ"))
        # GM1: ½ r₂²Δθ − ½ r₁²Δθ → ½(r₂² − r₁²)Δθ
        self.gat("põe em evidência")
        L3a = col(L([("eq", "="), ("h", r"\dfrac{1}{2}"), ("po", "("), ("a2", r"\R_2^2"), ("m", "-"), ("a1", r"\R_1^2"), ("pc", ")"), ("d", r"\,\Dt")], X1, 0, 44))
        abaixo(L2, L3a, X1, 26)
        gmap(self, 1, L2, L3a, [("eq", "eq"), (["h1", "h2"], "h"), ("a2", "a2"), ("m", "m"), ("a1", "a1"), (["d1", "d2"], "d")], rt=1.2,
             nota="½ e Δθ em evidência")
        degrau(self, "B2-1 célula", "½ r₂²Δθ − ½ r₁²Δθ = ½(r₂² − r₁²)Δθ")
        # GM2: diferença de quadrados → metade da soma (r̄) e diferença (Δr) → r̄ Δr Δθ
        self.gat("diferença de quadrados")
        L3b = col(L([("eq", "="), ("h", r"\dfrac{1}{2}"), ("p1", "("), ("r2a", r"\R_2"), ("pl", "+"), ("r1a", r"\R_1"), ("q1", ")"), ("p2", "("),
                     ("r2b", r"\R_2"), ("mi", "-"), ("r1b", r"\R_1"), ("q2", ")"), ("d", r"\,\Dt")], X1, 0, 44))
        ao_lado(L3a, L3b, 14)
        b2, b1 = lbase(L3a, "a2"), lbase(L3a, "a1")
        gmap(self, 2, L3a, L3b, [("eq", "eq"), ("h", "h"), ("po", "p1"), (b2, "r2a"), (b1, "r1a"), (b2, "r2b"), ("m", "mi"), (b1, "r1b"),
                                 ("pc", "q2"), ("d", "d")], rt=1.2, nota="a) diferença de quadrados")
        degrau(self, "B2-1 célula", "½(r₂² − r₁²)Δθ = ½(r₂ + r₁)(r₂ − r₁)Δθ")
        self.gat("a metade da soma")
        L4a = col(L([("eq", "="), ("fr", r"\dfrac{\R_1+\R_2}{2}"), ("c1", r"\cdot"), ("p2", "("), ("r2", r"\R_2"), ("mi", "-"), ("r1", r"\R_1"), ("q2", ")"),
                     ("c2", r"\cdot"), ("d", r"\,\Dt")], X1, 0, 44))
        abaixo(L3a, L4a, X1, 30)
        fr = sel(L4a, "fr")
        hh = sel(L3b, "h")
        gmap(self, 2, L3b, L4a, [("eq", "eq"), ("r1a", fr[0:2]), ("pl", fr[2:3]), ("r2a", fr[3:5]), (hh[1:], fr[5:7]), ("p2", "p2"), ("r2b", "r2"),
                                 ("mi", "mi"), ("r1b", "r1"), ("q2", "q2"), ("d", "d")], rt=1.0, nota="b) a metade da soma")
        degrau(self, "B2-1 célula", "½(r₂ + r₁)(r₂ − r₁)Δθ = [(r₁ + r₂)/2] · (r₂ − r₁) · Δθ")
        self.gat("o raio médio erre barra")
        arb = arco(v, .75, T6, T3, LI, 3, dash=(7, 5), z=8)
        lrb = TP(r"\rb", 105, 752, 40, "c")
        grb = guia_px((128, 752), v.px(.75 * math.cos(1.0), .75 * math.sin(1.0)), LI, lrb, 2, 10)
        self.play(Create(arb), run_time=0.4)
        self.pena(lrb, passo=0.04, extra=[Create(grb)])
        UB1 = r"\underbrace{\dfrac{\R_1+\R_2}{2}}_{\rb}"
        L4b = col(L([("eq", "="), ("ub1", UB1), ("c1", r"\cdot"), ("p2", "("), ("r2", r"\R_2"), ("mi", "-"), ("r1", r"\R_1"), ("q2", ")"),
                     ("c2", r"\cdot"), ("d", r"\,\Dt")], X1, 0, 44))
        L4b.shift(L4a[0][0].get_center() - L4b[0][0].get_center())
        u1 = sel(L4b, "ub1")
        L4b._fonte = L4a
        passo(self, L4a, L4b, [("eq", "eq"), ("fr", u1[:7]), ("c1", "c1"), ("p2", "p2"), ("r2", "r2"), ("mi", "mi"), ("r1", "r1"), ("q2", "q2"),
                               ("c2", "c2"), ("d", "d")], voos=[(lrb.f.copy(), u1[13:15])], rt=0.8, nota="GM2 chave r̄")
        self.gat("a diferença é delta erre")
        A_, B_ = v.px(.5 * math.cos(T6), .5 * math.sin(T6)), v.px(math.cos(T6), math.sin(T6))
        cdr, nrm = chave_seg(A_, B_, 20, RR, 2.5)
        mdr = ((A_[0] + B_[0]) / 2 + nrm[0] * 56, (A_[1] + B_[1]) / 2 + nrm[1] * 56)
        ldr = TP(r"\Dr", *mdr, 40, "c")
        for x in cdr.get_family():
            x._guia_de = ldr                      # a chave é do próprio rótulo
        self.play(Create(cdr), run_time=0.35)
        self.pena(ldr, passo=0.04)
        UB2 = r"\underbrace{(\R_2-\R_1)}_{\Dr}"
        L4 = col(L([("eq", "="), ("ub1", UB1), ("c1", r"\cdot"), ("ub2", UB2), ("c2", r"\cdot"), ("d", r"\,\Dt")], X1, 0, 44))
        L4.shift(L4b[0][0].get_center() - L4[0][0].get_center())
        u2 = sel(L4, "ub2")
        L4._fonte = L4b
        passo(self, L4b, L4, [("eq", "eq"), ("ub1", "ub1"), ("c1", "c1"), (["p2", "r2", "mi", "r1", "q2"], u2[:7]), ("c2", "c2"), ("d", "d")],
              voos=[(ldr.f.copy(), u2[13:15])], rt=0.8, nota="GM2 chave Δr")
        self.gat("a célula tem área exata")
        L5 = col(L([("eq", "="), ("rb", r"\rb"), ("Dr", r"\,\Dr"), ("d", r"\,\Dt")], X1, 0, 44))
        ao_lado(L4, L5, 36)
        gmap(self, 2, L4, L5, [("eq", "eq"), (sel(L4, "ub1")[13:15], "rb"), (u2[13:15], "Dr"), ("d", "d")], rt=1.0, nota="c) r̄ Δr Δθ")
        degrau(self, "B2-1 célula", "= r̄ Δr Δθ (exata)")
        mol5 = em_volta(L5, LI, 12, 2, .9, 8)
        self.play(Create(mol5), run_time=0.4)
        # os números: Δr = ½, Δθ = π/6; células de dentro e de fora
        self.gat("com delta erre igual")
        lnum = TC(r"\Dr=\dfrac{1}{2},\ \ \Dt=\dfrac{\pi}{6}", *v.px(1.2, 2.32), 40, "l")
        self.pena(lnum)
        self.gat("de raio médio três quartos")
        Y5 = pxof(L4.get_bottom())[1] + 66
        N1 = col(L([("a", r"\dfrac{3}{4}"), ("c1", r"\cdot"), ("b", r"\dfrac{1}{2}"), ("c2", r"\cdot"), ("t", r"\dfrac{\pi}{6}"), ("eq", "="),
                    ("r", r"\dfrac{\pi}{16}")], X1, Y5, 44))
        l34 = L([("rb", r"\rb"), ("v", r"=\dfrac{3}{4}")], 0, 0, 40)
        l34.shift(lrb.f[0][1].get_center() - l34[0][sel(l34, "rb")[1]].get_center())
        pl34 = placa_min(l34, 8, 5)
        pr = ja_escrita(parte(l34, sel(l34, "rb"), "r̄"))
        self.remove(lrb)
        self.add(pr)
        for x in grb.get_family():
            x._guia_de = l34
        self.pena(parte(l34, sel(l34, "v"), "= 3/4"), extra=[FadeIn(pl34)])
        escreve_seq(self, N1, [(l34[0][sel(l34, "v")[1]:sel(l34, "v")[-1] + 1], "a")], rt_voo=0.7, passo=0.04)
        origem(self, "3/4 · 1/2 · π/6", "r̄ = 3/4 no desenho e Δr = 1/2, Δθ = π/6 do rótulo (voos glifo a glifo)")
        self.gat("dá pi sobre dezesseis")
        degrau(self, "B2-1 números", "3/4 · 1/2 · π/6 = π/16")
        lp16 = dentro(TP(r"\dfrac{\pi}{16}", *v.px(.75 * math.cos(math.pi / 4), .75 * math.sin(math.pi / 4)), 40, "c"))
        self.play(FadeOut(arb), FadeOut(pr), FadeOut(pl34), FadeOut(grb), *[FadeOut(m) for m in self.mobjects if getattr(m, "_pai", None) is l34],
                  run_time=0.3)
        self.remove(arb, pr, pl34, grb, l34, *[m for m in self.mobjects if getattr(m, "_pai", None) is l34])
        self.pena(lp16)
        self.gat("a de fora de raio médio")
        c2 = cel_pol(v, 1.5, 2)
        arb2 = arco(v, 1.75, T6, T3, LI, 3, dash=(7, 5), z=8)
        l74 = TP(r"\rb=\dfrac{7}{4}", 105, 380, 40, "c")
        g74 = guia_px((128, 420), v.px(1.75 * math.cos(1.0), 1.75 * math.sin(1.0)), LI, l74, 2, 10)
        self.play(FadeIn(c2[0]), Create(c2[1]), Create(arb2), run_time=0.6)
        self.pena(l74, passo=0.04, extra=[Create(g74)])
        N2 = col(L([("a", r"\dfrac{7}{4}"), ("c1", r"\cdot"), ("b", r"\dfrac{1}{2}"), ("c2", r"\cdot"), ("t", r"\dfrac{\pi}{6}"), ("eq", "="),
                    ("r", r"\dfrac{7\pi}{48}")], X1, Y5 + 112, 44))
        escreve_seq(self, N2, [(l74.f[0][3:6], "a")], rt_voo=0.7, passo=0.04)
        origem(self, "7/4 · 1/2 · π/6", "r̄ = 7/4 no desenho e Δr, Δθ do rótulo (voos glifo a glifo)")
        self.gat("sete pi sobre quarenta")
        degrau(self, "B2-1 números", "7/4 · 1/2 · π/6 = 7π/48")
        lp48 = dentro(TP(r"\dfrac{7\pi}{48}", *v.px(1.75 * math.cos(math.pi / 4), 1.75 * math.sin(math.pi / 4)), 40, "c"))
        self.play(FadeOut(l74), FadeOut(g74), FadeOut(arb2), run_time=0.3)
        self.remove(l74, g74, arb2)
        self.pena(lp48)
        self.gat("sete terços da área")
        st_ = leg("A DE FORA: SETE TERÇOS", pxof(N2.get_right())[0] + 40, pxof(N2.get_center())[1] + 11, CANTO_S, "left", 30)
        self.pena(st_, passo=0.03)
        self.marca("03")
        # ── B2-2 · a lupa e o jacobiano (alvo 04, coluna de cima) ──
        self.an("B2-2")
        sai = saindo(self.snap() + [self.grade])
        self.grade = None
        self.secao("O FATOR É O JACOBIANO")
        self.subt("dA = r dr dθ")
        # a grade pequena com a célula de fora, à esquerda
        gpP = gpolar(VP, 2, 4, 3, 0, math.pi / 2, wpx=1.6)
        gpP22 = arco(VP, 2.2, 0, math.pi / 2, GEO, 1.6, z=3, alpha=.42)
        exP = VGroup(seta_px(VP.px(-.06, 0), VP.px(2.3, 0), E1, 3, 14, z=6), seta_px(VP.px(0, -.06), VP.px(0, 2.3), E2, 3, 14, z=6))
        cP = cel_pol(VP, 1.5, 2, w=3)
        gP = papel_v(VP, None)                                          # K2: tela inteira (a lupa tem fundo opaco próprio)
        self.play(*[FadeOut(m) for m in sai], FadeIn(gP), Create(gpP), Create(gpP22), Create(exP), FadeIn(cP[0]), Create(cP[1]), run_time=0.9)
        self.remove(*sai)
        self.grade = gP
        # a lupa: painel ao lado, ligado à célula pequena por duas linhas-guia
        pn = painel(LUP[0], LUP[1], LUP[2] - LUP[0], LUP[3] - LUP[1], .45)
        pn.set_fill("#1E1A46", .94)                                     # K2: fundo opaco (a grade da tela não passa por dentro da lupa)
        cz = cel_pol(VZ, 1.5, 2, w=4)
        q1, q2 = VP.px(2 * math.cos(T3), 2 * math.sin(T3)), VP.px(2 * math.cos(T6), 2 * math.sin(T6))
        gl = VGroup(lin_px([q1, (LUP[0], LUP[1] + 40)], GEO, 1.5, alpha=.6, z=2), lin_px([q2, (LUP[0], LUP[3] - 40)], GEO, 1.5, alpha=.6, z=2))
        self.play(Create(pn), Create(gl), TransformFromCopy(VGroup(cP[0], cP[1]), VGroup(cz[0], cz[1])), run_time=1.2)
        self.gat("um lado é delta erre")
        A_, B_ = VZ.px(1.5 * math.cos(T6), 1.5 * math.sin(T6)), VZ.px(2 * math.cos(T6), 2 * math.sin(T6))
        lado = lin_px([A_, B_], RR, 6, z=7)
        cdr, nrm = chave_seg(A_, B_, 22, GEO, 2.5)
        mdr = ((A_[0] + B_[0]) / 2 + nrm[0] * 66, (A_[1] + B_[1]) / 2 + nrm[1] * 66)
        ldr = TP(r"\Dr", *mdr, 40, "c")
        self.play(Create(lado), Create(cdr), run_time=0.6)
        self.pena(ldr)
        self.gat("o outro é um arco")
        arc_ = arco(VZ, 2, T6, T3, RR, 6, z=7)
        ch_ = VGroup(arco(VZ, 2.06, T6, T3, GEO, 2.5, z=7),
                     *[lin_px([VZ.px(2.03 * math.cos(t), 2.03 * math.sin(t)), VZ.px(2.09 * math.cos(t), 2.09 * math.sin(t))], GEO, 2.5, z=7) for t in (T6, T3)])
        self.play(Create(arc_), Create(ch_), run_time=0.7)
        self.gat("erre delta téta lado")
        lrd = TP(r"\R\,\Dt", *VZ.px(2.24 * math.cos(math.pi / 4), 2.24 * math.sin(math.pi / 4)), 40, "c")
        self.pena(lrd)
        self.gat("lado vezes lado")
        K1t = rot_txt("ÁREA ≈", X1, 262)
        K1 = col(L([("J", r"\J"), ("dr", r"\,\Dr"), ("dt", r"\,\Dt")], pxof(K1t.get_right())[0] + 16, 250, 46))
        self.pena(K1t)
        escreve_seq(self, K1, [(lrd.f[0][0:1], "J"), (ldr.f, "dr"), (lrd.f[0][1:], "dt")], rt_voo=0.8)
        origem(self, "ÁREA ≈ r Δr Δθ", "rótulos rΔθ do arco e Δr do lado (voos)")
        # o jacobiano
        self.gat("o terceiro jeito")
        K2 = col(TC(r"\X=\R\cos\T,\qquad \Y=\R\sen\T", X1, 345, 44, "l"))
        self.pena(K2)
        self.gat("a matriz das derivadas")
        VMX = r"\begin{vmatrix}\cos\T & -\R\sen\T\\ \sen\T & \R\cos\T\end{vmatrix}"
        K3 = col(L([("J", r"\dfrac{\partial(\X,\Y)}{\partial(\R,\T)}"), ("eq", "="), ("M", VMX)], X1, 0, 44))
        K3._matriz = True
        abaixo(K2, K3, X1, 24)
        M0 = sel(K3, "M")[0]
        mi = lambda a, b: [M0 + k for k in range(a, b)]
        self.pena(parte(K3, sel(K3, ["J", "eq"]) + mi(0, 4), "∂(x,y)/∂(r,θ) = |"))
        for frase, (a, b), nome in (("cosseno de téta e a derivada", (4, 8), "cos θ"), ("menos erre seno de téta na", (8, 14), "−r sen θ"),
                                    ("seno de téta e em téta", (14, 18), "sen θ"), ("erre cosseno de téta o", (18, 23), "r cos θ")):
            self.gat(frase)
            self.pena(parte(K3, mi(a, b) + (mi(23, 27) if a == 18 else []), nome))
        self.gat("o determinante é")
        D1 = col(L([("eq", "="), ("a", r"\cos\T"), ("c1", r"\cdot"), ("d", r"\R\cos\T"), ("m", "-"), ("po", "("), ("b", r"-\R\sen\T"), ("pc", ")"),
                    ("c2", r"\cdot"), ("c", r"\sen\T")], X1, 0, 44))
        abaixo(K3, D1, X1, 22)
        escreve_seq(self, D1, [(K3[0][M0 + 4:M0 + 8], "a"), (K3[0][M0 + 18:M0 + 23], "d"), (K3[0][M0 + 8:M0 + 14], "b"), (K3[0][M0 + 14:M0 + 18], "c")],
                    rt_voo=0.8)
        degrau(self, "B2-2 det", "det = cos θ · r cos θ − (−r sen θ) · sen θ")
        self.gat("erre cosseno ao quadrado mais")
        D2a = col(L([("eq", "="), ("r1", r"\R"), ("cs", r"\cos^2\T"), ("pl", "+"), ("r2", r"\R"), ("sn", r"\sen^2\T")], X1, 0, 44))
        abaixo(D1, D2a, X1, 24)
        a_, d_, b_, c_ = sel(D1, "a"), sel(D1, "d"), sel(D1, "b"), sel(D1, "c")
        cs, sn = sel(D2a, "cs"), sel(D2a, "sn")
        gmap(self, 3, D1, D2a, [("eq", "eq"), (d_[0:1], "r1"), (a_[0:3], cs[0:3]), (d_[1:4], cs[0:3]), (a_[3:4], cs[4:5]), (d_[4:5], cs[4:5]),
                                (["m"], "pl"), (b_[0:1], "pl"), (b_[1:2], "r2"), (b_[2:5], sn[0:3]), (c_[0:3], sn[0:3]), (b_[5:6], sn[4:5]),
                                (c_[3:4], sn[4:5])], rt=1.3, nota="a) r cos²θ + r sen²θ")
        degrau(self, "B2-2 det", "= r cos²θ + r sen²θ")
        self.gat("põe o erre em evidência")
        D2b = col(L([("eq", "="), ("r", r"\R"), ("po", "("), ("cs", r"\cos^2\T"), ("pl", "+"), ("sn", r"\sen^2\T"), ("pc", ")")], X1, 0, 44))
        abaixo(D2a, D2b, X1, 22)
        gmap(self, 3, D2a, D2b, [("eq", "eq"), (["r1", "r2"], "r"), ("cs", "cs"), ("pl", "pl"), ("sn", "sn")], rt=1.0, nota="b) r em evidência")
        degrau(self, "B2-2 det", "= r(cos²θ + sen²θ)")
        self.gat("ao quadrado é um")
        acende(self, (D2b[0][sel(D2b, "po")[0]:sel(D2b, "pc")[0] + 1], TH), rt=0.3)
        D2c1 = col(L([("eq", "="), ("r", r"\J"), ("c", r"\cdot"), ("um", "1")], X1, 0, 44))
        ao_lado(D2b, D2c1, 16)
        gmap(self, 3, D2b, D2c1, [("eq", "eq"), ("r", "r"), (["po", "cs", "pl", "sn", "pc"], "um")], rt=0.9, nota="c) cos² + sen² vira 1")
        degrau(self, "B2-2 det", "= r · 1")
        self.gat("sobra erre")
        D2c = col(L([("eq", "="), ("r", r"\J")], X1, 0, 44))
        D2c.shift(D2c1[0][0].get_center() - D2c[0][0].get_center())
        gmap(self, 3, D2c1, D2c, [("eq", "eq"), ("r", "r")], rt=0.7, copia=False, nota="d) o 1 some: sobra r")
        degrau(self, "B2-2 det", "= r")
        self.gat("três caminhos o mesmo")
        yb = pxof(D2b.get_bottom())[1]
        l7a = leg("TRÊS CAMINHOS, O MESMO r", X1, yb + 158, CANTO_S, "left", 30)
        l7b = leg("SETORES · ARCO × LADO · DETERMINANTE", X1, yb + 200, GEO, "left", 30)
        self.pena(l7a, l7b, lag=0.2, passo=0.025)
        self.gat("dê a igual a erre")
        K6 = L([("dA", "dA"), ("eq", "="), ("J", r"\J"), ("dr", r"\,\dr"), ("dt", r"\,\dt"), ("cond", r"\qquad(\R\ge 0)")], X1 + 18, yb + 64, 44)
        mol6 = em_volta(K6, LI, 14, 2, .9, 10)
        escreve_seq(self, K6, [(D2c[0][1:2], "J")], rt_voo=0.7, arco=0.9)
        self.play(Create(mol6), run_time=0.4)          # a moldura nasce depois do texto (G4)
        origem(self, "dA = r dr dθ (r lima)", "o r do determinante (voo)")
        # ── B2-3 · o teste da unidade (alvo v2_02) ──
        self.marca("04")                                   # o fim do B2-2 (alvo 04, metade de cima: o jacobiano)
        self.an("B2-3")
        self.secao("O TESTE DA UNIDADE")
        self.subt("SEM O r, A CONTA DÁ O PERÍMETRO")
        chip = L([("dA", "dA"), ("eq", "="), ("J", r"\J"), ("dr", r"\,\dr"), ("dt", r"\,\dt")], X1 + 14, 215, 44)
        molc = em_volta(chip, LI, 14, 2, .9, 10)
        sai = saindo([m for m in self.snap() if m not in (K6, mol6)])
        gd = papel_v(VD, (-1.35, 1.4, -1.35, 1.3))
        ex = eixos_xy(VD, -1.35, 1.45, -1.35, 1.33, size=40)
        dfill = disco(VD, 1.15, mixh(BG_, GEO, .14), 1.0, z=1)
        dcont = circulo(VD, 1.15, GEO, 3, z=5)
        rad = lin_px([VD.px(0, 0), VD.px(1.15 * math.cos(.55), 1.15 * math.sin(.55))], RR, 5, z=6)
        la = TC("a", *VD.px(.5 * math.cos(.55) - .06, .5 * math.sin(.55) + .14), 40, "c")
        for x in chip.get_family():
            x._esc = True
        # o palco velho sai primeiro (0,3 s); no quadro seguinte o novo começa e o chip sobe por cima da coluna já vazia
        self.play(*[FadeOut(m) for m in sai], FadeOut(VGroup(*[K6[0][i] for i in sel(K6, "cond")])), run_time=0.3)
        self.remove(*sai)
        self.play(ReplacementTransform(VGroup(K6[0][0:sel(K6, "dt")[-1] + 1]), chip), ReplacementTransform(mol6, molc),
                  FadeIn(gd), GrowFromPoint(ex[0], VD.P(0, 0)), GrowFromPoint(ex[1], VD.P(0, 0)), FadeIn(dfill), Create(dcont), run_time=0.7)
        self.remove(K6)
        self.grade = gd
        self.gat("num disco de raio á")
        self.play(Create(rad), run_time=0.5)
        self.pena(ex[2], ex[3], la, lag=0.05)
        # GM4 (errado): ∫∫ dr dθ → ∫ a dθ → 2πa
        self.gat("sem o erre a de")
        ls1 = T("SEM O r", X1, 326, 32, "left", AL)
        self.pena(ls1)
        W0 = col(L([("i1", r"\Al{\displaystyle\int_0^{2\pi}}\!\!"), ("i2", r"\Al{\displaystyle\int_0^{a}}"), ("dr", r"\Al{dr}"), ("dt", r"\Al{\,d\theta}")], X1, 400, 44))
        self.pena(W0)
        self.gat("a de dentro dá á")
        W1 = col(L([("eq", r"\Al{=}"), ("i1", r"\Al{\displaystyle\int_0^{2\pi}}"), ("a", r"\Al{a}"), ("dt", r"\Al{\,d\theta}")], 0, 0, 44))
        ao_lado(W0, W1, 12, ia=sel(W0, "dr")[0], ib=sel(W1, "eq")[0])
        _, _, _ = sup_sub(W0, "i2")
        _, ui2, _ = sup_sub(W0, "i2")
        gmap(self, 4, W0, W1, [("i1", "i1"), (ui2, "a"), ("dt", "dt")], rt=1.1, nota="a) a de dentro dá a")
        degrau(self, "B2-3 sem r", "∫₀^{2π}∫₀^a dr dθ = ∫₀^{2π} a dθ")
        self.gat("dois pi á o perímetro")
        W2 = col(L([("eq", r"\Al{=}"), ("tp", r"\Al{2\pi}"), ("a", r"\Al{a}")], 0, 0, 44))
        ao_lado(W1, W2, 12)
        _, ui1, _ = sup_sub(W1, "i1")
        gmap(self, 4, W1, W2, [("eq", "eq"), (ui1, "tp"), ("a", "a")], rt=1.1, nota="b) 2πa")
        degrau(self, "B2-3 sem r", "= 2πa")
        xx = cruz_px(pxof(W2.get_right())[0] + 70, pxof(W2.get_center())[1], AL, 1.2)
        acc = circulo(VD, 1.15, AL, 5, z=6)
        lper = T("PERÍMETRO", *VD.px(-.95, 1.08 + .2), 30, "center", AL)
        l2pa = TP(r"\Al{2\pi a}", *VD.px(-.95, 1.08), 40, "c")
        self.play(Create(xx), Create(acc), run_time=0.6)
        self.pena(lper, l2pa, lag=0.15)
        self.gat("em metro com")
        lm = leg("UNIDADE: METRO · É O PERÍMETRO", X1, pxof(W0.get_bottom())[1] + 52, AL, "left", 30)
        self.pena(lm, passo=0.025)
        # GM5 (certo): ∫∫ r dr dθ → ∫[r²/2]₀^a dθ → ∫(a²/2 − 0) dθ → 2π · a²/2 → πa²
        self.gat("com o erre a de")
        lc1 = T("COM O r", X1, pxof(lm.get_bottom())[1] + 92, 32, "left", MEN)
        self.pena(lc1)
        R0 = col(L([("i1", r"\displaystyle\int_0^{2\pi}\!\!"), ("i2", r"\displaystyle\int_0^{a}"), ("J", r"\J"), ("dr", r"\,\dr"), ("dt", r"\,\dt")],
                   X1, pxof(lc1.get_bottom())[1] + 66, 44))
        self.pena(R0)
        self.gat("erre ao quadrado sobre dois de")
        R1 = col(L([("eq", "="), ("i1", r"\displaystyle\int_0^{2\pi}"), ("lb", r"\Big["), ("F", r"\dfrac{\R^2}{2}"), ("rb", r"\Big]_0^{a}"), ("dt", r"\,\dt")], 0, 0, 44))
        ao_lado(R0, R1, 12, ia=sel(R0, "dt")[0], ib=sel(R1, "eq")[0])
        _, upA, loA = sup_sub(R0, "i2")
        rb_ = sel(R1, "rb")
        upB = [max(rb_[1:], key=lambda i: R1[0][i].get_center()[1])]
        loB = [min(rb_[1:], key=lambda i: R1[0][i].get_center()[1])]
        gmap(self, 5, R0, R1, [("i1", "i1"), ("J", sel(R1, "F")[0:1]), (upA, upB), (loA, loB), ("dt", "dt")], rt=1.2, nota="a) primitiva r²/2")
        degrau(self, "B2-3 com r", "∫₀^{2π}∫₀^a r dr dθ = ∫₀^{2π}[r²/2]₀^a dθ")
        self.gat("que dá á ao quadrado")
        R2 = col(L([("eq", "="), ("i1", r"\displaystyle\int_0^{2\pi}"), ("po", r"\Big("), ("F", r"\dfrac{a^2}{2}"), ("m", "-"), ("z", "0"), ("pc", r"\Big)"),
                    ("dt", r"\,\dt")], X1, 0, 44))
        abaixo(R0, R2, X1, 30)
        F1, F2 = sel(R1, "F"), sel(R2, "F")
        gmap(self, 5, R1, R2, [("eq", "eq"), ("i1", "i1"), (upB, F2[0:1]), (F1[1:], F2[1:]), (loB, "z"), ("dt", "dt")], rt=1.3,
             nota="b) F(a) − F(0) com os valores: (a²/2 − 0)")
        degrau(self, "B2-3 com r", "= ∫₀^{2π}(a²/2 − 0) dθ   [F(a) − F(0)]")
        self.gat("multiplica por dois pi pi")
        R3 = col(L([("eq", "="), ("tp", r"2\pi"), ("c", r"\cdot"), ("F", r"\dfrac{a^2}{2}")], 0, 0, 44))
        ao_lado(R2, R3, 12, ia=0, ib=0)
        _, ui2b, _ = sup_sub(R2, "i1")
        gmap(self, 5, R2, R3, [("eq", "eq"), (ui2b, "tp"), ("F", "F")], rt=1.1, nota="c) a de fora multiplica por 2π")
        degrau(self, "B2-3 com r", "= 2π · a²/2")
        R4 = col(L([("eq", "="), ("pi", r"\Me{\pi}"), ("a2", r"\Me{a^2}")], 0, 0, 44))
        ao_lado(R3, R4, 12)
        tp3 = ordx(R3, "tp")
        F3 = sel(R3, "F")
        gmap(self, 5, R3, R4, [("eq", "eq"), (tp3[1:2], "pi"), (F3[0:2], "a2")], rt=1.1, nota="d) o 2 cancela: πa²")
        degrau(self, "B2-3 com r", "= πa² (o 2 cancela)")
        ok = check_px(pxof(R4.get_right())[0] + 56, pxof(R4.get_center())[1], MEN, 1.2)
        pint = disco(VD, 1.15, mixh(BG_, MEN, .16), 1.0, z=1)
        lpa = TC(r"\Me{\pi a^2}", *VD.px(-.35, -.42), 46, "c")
        lar = T("ÁREA", *VD.px(-.35, -.42 - .24), 30, "center", MEN)
        self.play(Create(ok), Transform(dfill, pint), run_time=0.7)
        self.pena(lpa, lar, lag=0.15)
        self.gat("em metro quadrado")
        lm2 = leg("UNIDADE: METRO² · É A ÁREA", X1, pxof(R2.get_bottom())[1] + 52, MEN, "left", 30)
        self.pena(lm2, passo=0.025)
        self.marca("v2_02")
        self.sai_fim()

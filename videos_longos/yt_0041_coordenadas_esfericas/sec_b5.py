"""yt_0041 · B5 · a bola pesada: M = π (alvo 12). A bola do H1 volta parada (mesmo 3D, sem girar). ρ = √(x²+y²+z²) = √(r²) = r (o r² voa do chip
x² + y² + z² = r², miniatura do B1-2); M com o r da densidade em ciano e o fator em lima (chaves DENSIDADE e JACOBIANO por 2 s); glyph map 12
(r · r² sen φ → r³ sen φ; depois os três colchetes com os valores → 1/4 · 2 · 2π → π); CONFERE (não está no alvo). Etapa 2 (a coluna sobe): MÉDIA
(glyph map 13, o π cancela em dois tempos) e MASSA ATÉ c (glyph map 14), com a casca de 0,84 a 1 acesa na bola."""
from k41 import *
from sec_b1 import depois

X0 = 1020


class PB5(B41):
    ANTES = "A BOLA É UMA CEBOLA"

    def corpo(self):
        self.an("B5")
        bl = self.palco("bola", cam_alvo("b5"), cunha=1.0, casca084=0.0)
        self.add(bl.fundo)                                       # a bola do H1 volta parada, já no 1º quadro
        self.papel_on(rt=0)                                      # G1: papel também atrás do 3D
        rx = self.rot3(bl, "ex", r"\X", dx=18, dy=14, size=38)
        ry = self.rot3(bl, "ey", r"\Y", dx=18, dy=-6, size=38)
        rz = self.rot3(bl, "ez", r"\Z", dx=28, dy=-6, size=38)
        self.pena(rx, ry, rz, lag=0.12)
        self.titulo("DE VOLTA À BOLA", rt=0.3)
        self.gat("a bola pesada do começo")
        cg, cf, cm_ = chip(r"\X^2+\Y^2+\Z^2=\R^2", 1330, 140, 26, MEN)            # miniatura do chip do B1-2
        self.chip_pena(cg, cf, cm_)
        r1 = mixl([("L", [("rho", r"\de"), ("eq", "="), ("raiz", r"\sqrt{\X^2+\Y^2+\Z^2}"), ("eq2", "="), ("rq", r"\sqrt{\R^2}"), ("eq3", "="), ("r", r"\R")]),
                   ("t", "(r ≥ 0)", GEO)], X0, 200, 44)
        F1 = r1.p[0]
        self.gat("a densidade raiz da soma")
        self.pena(parte(F1, sel(F1, ["rho", "eq", "raiz"]), "ρ = √(x²+y²+z²)"))
        self.degrau("C9", "ρ = √(x² + y² + z²)")
        self.gat("em esféricas é só r")
        rq = sel(F1, "rq")             # √, traço do radical, r, 2
        self.pena(parte(F1, sel(F1, "eq2") + rq[:2], "= √"))
        self.voos([(VGroup(*cf[0][-2:]), parte(F1, rq[2:], "r²"))], rt=0.8, nota="B5: o r² voa do chip x²+y²+z² = r² (B1-2)")
        self.pena(parte(F1, sel(F1, ["eq3", "r"]), "= r"), r1.p[1], lag=0.2)
        self.degrau("C9", "= √(r²) = r (r ≥ 0)")
        self.sai(cg, rt=0.3)

        M = L([("M", "M"), ("eq", "="), ("i", r"\int_0^{2\pi}\!\!\int_0^{\pi}\!\!\int_0^{1}"), ("rd", r"\Ci{r}"), ("d", r"\cdot"), ("j", r"\J"),
               ("dd", r"\;\dR\,\dF\,\dT")], X0, 300, 46)
        self.gat("na massa o r da densidade")
        self.pena(parte(M, sel(M, ["M", "eq", "i"]), "M = ∫∫∫"))
        self.gat("o r da densidade multiplica")
        self.voos([(gl(F1, "r"), parte(M, sel(M, "rd"), "r (densidade)"))], rt=0.8, nota="B5: o r da densidade voa da linha ρ (ciano)")
        self.pena(parte(M, sel(M, ["d", "j", "dd"]), "· r² sen φ dr dφ dθ"))
        self.degrau("C9", "M = ∫₀^{2π}∫₀^π∫₀^1 r · r² sen φ dr dφ dθ")
        self.gat("multiplica o r ao quadrado")
        x0, x1 = pxof(gl(M, "rd").get_left())[0], pxof(gl(M, "rd").get_right())[0]
        yb = pxof(M.get_bottom())[1] + 8
        k1 = chave_h(x0 - 4, x1 + 4, yb, CI, 2)
        t1 = T("DENSIDADE", x1 + 6, yb + 36, 26, "right", CI, bold=False)
        self.play(Create(k1), run_time=0.3)
        self.pena(t1)
        self.gat("do fator e junta")
        x0, x1 = pxof(gl(M, "j").get_left())[0], pxof(gl(M, "j").get_right())[0]
        k2 = chave_h(x0 - 2, x1 + 2, yb, LI, 2)
        t2 = T("JACOBIANO", x0 + 4, yb + 36, 26, "left", LI, bold=False)
        self.play(Create(k2), run_time=0.3)
        self.pena(t2)
        self.gat("junta")
        self.sai(k1, t1, k2, t2, rt=0.3)
        M2 = L([("eq", "="), ("i", r"\int_0^{2\pi}\!\!\int_0^{\pi}\!\!\int_0^{1}"), ("r3", r"\R^3"), ("sf", r"\sen\F"), ("dd", r"\;\dR\,\dF\,\dT")], X0, 400, 42)
        j_ = sel(M, "j")               # r, ², s, e, n, φ
        self.gm(12, M, M2, [("eq", "eq"), ("i", "i"), (["rd", j_[0]], sel(M2, "r3")[:1]), ([j_[1]], sel(M2, "r3")[1:]), (j_[2:], "sf"), ("dd", "dd")],
                copia=True, nota="r · r² sen φ → r³ sen φ")
        self.degrau("C9", "= ∫∫∫ r³ sen φ dr dφ dθ")

        P3_ = L([("eq", "="), ("a", r"\Big[\dfrac{\R^4}{4}\Big]_0^1"), ("d1", r"\cdot"), ("b", r"\big[-\cos\F\big]_0^{\pi}"), ("d2", r"\cdot"),
                 ("c", r"\big[\T\big]_0^{2\pi}")], X0, 500, 42)
        P4 = L([("eq", "="), ("a", r"\Big(\dfrac14-0\Big)"), ("d1", r"\cdot"), ("b", "(1+1)"), ("d2", r"\cdot"), ("c", r"(2\pi-0)")], X0, 600, 42)
        self.gat("então separa em três")
        self.pena(parte(P3_, sel(P3_, "eq"), "="))
        self.gat("a de R")
        self.pena(parte(P3_, sel(P3_, "a"), "[r⁴/4]₀¹"))
        self.degrau("C9", "[r⁴/4]₀¹")
        self.gat("em um dá um quarto")
        self.pena(parte(P4, sel(P4, ["eq", "a"]), "= (1/4 − 0)"))
        self.degrau("C9", "(1/4 − 0)")
        self.gat("a de fi")
        self.pena(parte(P3_, sel(P3_, ["d1", "b"]), "· [−cos φ]₀^π"))
        self.degrau("C9", "· [−cos φ]₀^π")
        self.gat("velha conhecida dois")
        self.pena(parte(P4, sel(P4, ["d1", "b"]), "· (1 + 1)"))
        self.degrau("C9", "· (1 + 1)")
        self.gat("a de téta")
        self.pena(parte(P3_, sel(P3_, ["d2", "c"]), "· [θ]₀^{2π}"))
        self.degrau("C9", "· [θ]₀^{2π}")
        self.gat("dois pi multiplica")
        self.pena(parte(P4, sel(P4, ["d2", "c"]), "· (2π − 0)"))
        self.degrau("C9", "· (2π − 0)")
        self.gat("o quatro de baixo come o dois")
        P5 = depois(L([("eq", "="), ("a", r"\dfrac14"), ("d1", r"\cdot"), ("b", "2"), ("d2", r"\cdot"), ("c", r"2\pi")], 0, 600, 42), P4, 0, 0)
        a4, b4, c4 = sel(P4, "a"), sel(P4, "b"), sel(P4, "c")      # a: (, 1, —, 4, −, 0, )   b: (, 1, +, 1, )   c: (, 2, π, −, 0, )
        self.gm(12, P4, P5, [(a4[1:4], "a"), ("d1", "d1"), (b4[1:4], "b"), ("d2", "d2"), (c4[1:3], "c")], copia=True, nota="(1/4 − 0)(1 + 1)(2π − 0) → 1/4 · 2 · 2π")
        self.degrau("C9", "= 1/4 · 2 · 2π")
        self.gat("a massa é pi")
        P6 = depois(L([("eq", "="), ("pi", r"\Me{\pi}")], 0, 600, 42), P5, 0, 0)
        self.gm(12, P5, P6, [(sel(P5, ["a", "b", "c"]), "pi")], copia=True, nota="1/4 · 2 · 2π → π")
        self.degrau("C9", "= π")
        ck = check_px(pxof(P6.get_right())[0] + 40, 570)
        self.play(Create(ck), run_time=0.4)
        self.gat("e o computador")
        cf_ = leg("CONFERE: CARTESIANAS NO COMPUTADOR = 3,14159…", X0, 690, GEO, "left", 28)
        self.pena(cf_)
        self.col("B5-1", r1, M, M2, P3_, P4, cf_)
        self.marca("12_B5a", agora=True)

        # etapa 2: a coluna sobe (a tela velha sobe e sai)
        self.gat("o que esse pi diz")
        self.sobe_sai(r1, M, M2, P3_, dy=0.5, rt=0.5)
        sobe = self.velhos(P4, P5, P6, ck, cf_)
        self.play(sobe.animate.shift(UP * (600 - 200) / 120), run_time=0.7)
        self.col_zera("B5-1")
        self.gat("a densidade seria a média")
        md = mixl([("t", "MÉDIA", GEO), ("L", [("a", r"\dfrac{M}{V}"), ("eq", "="), ("b", r"\dfrac{\pi}{4\pi/3}")])], X0, 400, 40)
        self.pena(md.p[0])
        A_ = md.p[1]
        self.pena(parte(A_, sel(A_, ["a", "eq"]), "M/V ="))
        bb = sel(A_, "b")              # π, —, 4, π, /, 3
        self.voos([(gl(P6, "pi"), parte(A_, [bb[0]], "π"))], rt=0.8, nota="B5: o π voa do resultado para a MÉDIA")
        self.pena(parte(A_, bb[1:], "/ (4π/3)"))
        self.degrau("C10", "M/V = π/(4π/3)")
        self.gat("mantém a primeira e inverte a segunda")
        B_ = depois(L([("eq", "="), ("pi", r"\pi"), ("d", r"\cdot"), ("f", r"\dfrac{3}{4\pi}")], 0, 400, 40), A_, sel(A_, "eq")[0], 0)
        ff = sel(B_, "f")              # 3, —, 4, π
        self.gm(13, A_, B_, [([bb[0]], "pi"), ([bb[5]], [ff[0]]), ([bb[1]], [ff[1]]), ([bb[2]], [ff[2]]), ([bb[3]], [ff[3]])], copia=True,
                nota="π/(4π/3) → π · 3/(4π)")
        self.degrau("C10", "= π · 3/(4π)")
        self.gat("os pis se cancelam")
        C_ = depois(L([("eq", "="), ("f", r"\dfrac34")], 0, 400, 40), B_, 0, 0)
        self.acende_sai(gl(B_, "pi"), VGroup(B_[0][ff[3]]), cor=MEN, rt=0.4, rt_vis=0.3)            # o π cancela em dois tempos: acende…
        self.gm(13, B_, C_, [([ff[0]], [1]), ([ff[1]], [2]), ([ff[2]], [3])], copia=True, nota="π · 3/(4π) → 3/4 (o π sai)")
        self.acende_sai(gl(B_, "pi"), VGroup(B_[0][ff[3]]), cor=BR, rt=0.3, rt_vis=0, volta=False)
        self.degrau("C10", "= 3/4")

        self.gat("até um raio C")
        self.sobe_sai(md, A_, B_, C_, dy=0.3, rt=0.4)                      # a MÉDIA já foi lida: sai, e a MASSA ATÉ c ocupa o lugar
        mc = mixl([("t", "MASSA ATÉ", GEO), ("L", [("c", "c:"), ("i", r"\int_0^{2\pi}\!\!\int_0^{\pi}\!\!\int_0^{c}"), ("f", r"\R^3\sen\F"),
                                                    ("dd", r"\;\dR\,\dF\,\dT")])], X0, 510, 38)
        self.pena(mc.p[0])
        F0 = mc.p[1]
        self.pena(F0)
        self.degrau("C10", "massa até c = ∫₀^{2π}∫₀^π∫₀^c r³ sen φ dr dφ dθ")
        self.gat("muda só o limite de cima")
        mc1 = L([("i", r"\int_0^c\R^3\,\dR"), ("eq", "="), ("pr", r"\Big[\dfrac{\R^4}{4}\Big]_0^c")], X0, 600, 38)
        self.pena(mc1)
        self.degrau("C10", "∫₀^c r³ dr = [r⁴/4]₀^c")
        self.gat("agora o colchete dá c à quarta")
        mc2 = depois(L([("eq", "="), ("v", r"\dfrac{c^4}{4}-0")], 0, 600, 38), mc1, 0, 0, gap=14)
        self.pena(mc2)
        self.degrau("C10", "= c⁴/4 − 0")
        self.gat("menos zero vezes o mesmo dois")
        F_ = L([("eq", "="), ("a", r"\dfrac{c^4}{4}\cdot2\cdot2\pi"), ("eq2", "="), ("b", r"\pi c^4")], X0, 705, 38)
        self.pena(parte(F_, sel(F_, ["eq", "a"]), "= c⁴/4 · 2 · 2π"))
        self.degrau("C10", "= c⁴/4 · 2 · 2π")
        self.gat("pi C à quarta metade")
        self.pena(parte(F_, sel(F_, ["eq2", "b"]), "= πc⁴"))
        self.degrau("C10", "= πc⁴")
        self.gat("metade da massa é pi")
        G1 = L([("lhs", r"\pi c^4"), ("eq", "="), ("rhs", r"\dfrac{\pi}{2}")], X0, 795, 38)
        self.pena(parte(G1, sel(G1, "lhs"), "πc⁴"))
        self.pena(parte(G1, sel(G1, "eq"), "="))
        self.voos([(gl(P6, "pi"), parte(G1, [sel(G1, "rhs")[0]], "π"))], rt=0.8, nota="B5: o π voa do resultado para MASSA ATÉ c")
        self.pena(parte(G1, sel(G1, "rhs")[1:], "/2"))
        self.degrau("C10", "πc⁴ = π/2")
        self.gat("c à quarta é um meio")
        G2 = L([("lhs", r"c^4"), ("eq", "="), ("rhs", r"\dfrac12")], X0, 795, 38)
        lh, rh = sel(G1, "lhs"), sel(G1, "rhs")       # π, c, 4 ; π, —, 2
        self.acende_sai(VGroup(G1[0][lh[0]]), VGroup(G1[0][rh[0]]), cor=MEN, rt=0.4, rt_vis=0.3)
        self.gm(14, G1, G2, [(lh[1:], "lhs"), ("eq", "eq"), (rh[1:], sel(G2, "rhs")[1:])], nota="πc⁴ = π/2 → c⁴ = 1/2")
        self.degrau("C10", "c⁴ = 1/2")
        self.gat("tira a raiz quarta")
        G3 = depois(L([("im", r"\Rightarrow"), ("c", "c"), ("eq", "="), ("r", r"\sqrt[4]{1/2}"), ("ap", r"\approx 0{,}84")], 0, 795, 38), G2, 2, 2, gap=14)
        self.gm(14, G2, G3, [([0], "c")], copia=True, nota="c⁴ = 1/2 → c = ⁴√(1/2)")
        self.degrau("C10", "⇒ c = ⁴√(1/2) ≈ 0,84")
        self.gat("mora na casca de fora")
        bl.set(casca084=1.0)
        sq84, t84 = legq(RO, "r = 0,84: METADE DA MASSA DE CADA LADO", 120, 1020)
        self.pena(t84, extra=[Create(sq84)])
        l16 = leg("METADE DA MASSA MORA NOS 16% DE FORA DO RAIO", X0, 935, RO, "left", 30)
        self.pena(l16)
        self.col("B5-2", P4, P5, mc, mc1, F_, G2, G3)
        self.marca("12_B5")
        self.sai_fim()

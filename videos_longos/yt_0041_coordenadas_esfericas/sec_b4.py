"""yt_0041 · B4 · a cebola: área da esfera (alvo 11). A casca de r ∈ [0,6; 0,7] acende; a integral em φ e θ com os colchetes (glyph map 10);
a bola é uma cebola: 5 cascas acendem do centro para fora e voltam para a casca do alvo (um movimento só, ~2 s, só contorno); somando as cascas
(4πr² voa da linha 2; glyph map 11); derivando: ENGORDAR = UMA CASCA; por último ρ SÓ DE r (não está no alvo)."""
from k41 import *
from sec_b1 import depois


class PB4(B41):
    ANTES = "A BOLA É UMA CEBOLA"

    def corpo(self):
        self.an("B4")
        cb = self.palco("cebola", cam_alvo("b4"), casca=0.0, onda=0.0)
        self.add(cb.fundo)
        self.papel_on(rt=0)                                                     # G1: papel também atrás do 3D
        rx = self.rot3(cb, "ex", r"\X", dy=14, size=36)
        ry = self.rot3(cb, "ey", r"\Y", size=36)
        rz = self.rot3(cb, "ez", r"\Z", dx=16, size=36)
        self.pena(rx, ry, rz, lag=0.12)
        self.gat("fixa r")
        cb.set(casca=1.0)
        sq, tl = legq(RO, "CASCA DE RAIO r, ESPESSURA dr", 120, 1020)
        g1 = VGroup(sq, tl)
        g1._txt = "CASCA DE RAIO r, ESPESSURA dr"
        A = L([("i", r"\int_0^{2\pi}\!\!\int_0^{\pi}"), ("j", r"\J"), ("d", r"\,\dF\,\dT"), ("eq", "="), ("r2", r"\R^2"), ("d1", r"\cdot"),
               ("c1", r"\big[-\cos\F\big]_0^{\pi}"), ("d2", r"\cdot"), ("c2", r"\big[\T\big]_0^{2\pi}")], 1020, 230, 38)
        self.gat("fixa r e integra")
        self.pena(parte(A, sel(A, ["i", "j", "d"]), "∫∫ r² sen φ dφ dθ"))
        self.degrau("C8", "∫₀^{2π}∫₀^π r² sen φ dφ dθ")
        self.pena(tl, extra=[Create(sq)])
        self.gat("a de fi dá dois")
        self.pena(parte(A, sel(A, ["eq", "r2", "d1", "c1"]), "= r² · [−cos φ]₀^π"))
        self.degrau("C8", "= r² · [−cos φ]₀^π")
        self.gat("a de téta dá dois pi")
        self.pena(parte(A, sel(A, ["d2", "c2"]), "· [θ]₀^{2π}"))
        self.degrau("C8", "· [θ]₀^{2π}")
        B = L([("eq", "="), ("r2", r"\R^2"), ("d1", r"\cdot"), ("b", "2"), ("d2", r"\cdot"), ("c", r"2\pi")], 1060, 350, 42)
        self.gm(10, A, B, [("r2", "r2"), ("d1", "d1"), ("d2", "d2")], copia=True, nota="r² · [−cos φ]₀^π · [θ]₀^{2π} → r² · 2 · 2π")
        self.degrau("C8", "= r² · 2 · 2π")
        self.gat("dois vezes dois pi vezes r ao quadrado")
        C = depois(L([("eq", "="), ("r", r"4\pi\R^2")], 0, 350, 42), B, 0, 0)
        b_, c_ = sel(B, "b"), sel(B, "c")
        rr = sel(C, "r")               # 4, π, r, 2
        self.gm(10, B, C, [(b_ + [c_[0]], [rr[0]]), ([c_[1]], [rr[1]]), ("r2", rr[2:])], copia=True, nota="r² · 2 · 2π → 4πr²")
        self.degrau("C8", "= 4πr²")
        self.gat("a área da esfera")
        ae = mixl([("t", "ÁREA DA ESFERA", MEN)], pxof(C.get_right())[0] + 40, 350, 36)
        self.pena(ae)

        self.gat("a bola é uma cebola")
        self.play(cb.tr["onda"].animate(rate_func=linear).set_value(1.0), run_time=2.0)          # 5 cascas do centro para fora, e volta à do alvo
        cb.set(onda=0.0)
        self.gat("somar as cascas é integrar")
        V = L([("V", "V"), ("eq", "="), ("i", r"\int_0^R"), ("f", r"4\pi\R^2"), ("dr", r"\,\dR"), ("eq2", "="), ("p", r"4\pi\Big[\dfrac{\R^3}{3}\Big]_0^R")],
              1020, 505, 42)
        self.pena(parte(V, sel(V, ["V", "eq", "i"]), "V = ∫₀^R"))
        self.voos([(gl(C, "r"), parte(V, sel(V, "f"), "4πr²"))], rt=0.8, nota="B4: 4πr² voa da linha 2 para a integral V")
        self.pena(parte(V, sel(V, "dr"), "dr"))
        self.degrau("C8", "V = ∫₀^R 4πr² dr")
        self.gat("sobe o expoente divide por três")
        self.pena(parte(V, sel(V, ["eq2", "p"]), "= 4π[r³/3]₀^R"))
        self.degrau("C8", "= 4π[r³/3]₀^R")
        self.gat("sai quatro pi R ao cubo sobre três")
        V2 = depois(L([("eq", "="), ("r", r"\dfrac{4}{3}\pi R^3")], 0, 505, 42), V, sel(V, "eq2")[0], 0)
        p_ = sel(V, "p")               # 4, π, [, r, ³, —, 3, ], R, 0
        rr = sel(V2, "r")              # 4, —, 3, π, R, ³
        self.gm(11, V, V2, [([p_[0]], [rr[0]]), ([p_[1]], [rr[3]]), ([p_[5]], [rr[1]]), ([p_[6]], [rr[2]]), ([p_[3]], [rr[4]]), ([p_[4]], [rr[5]])],
                copia=True, nota="4π[r³/3]₀^R → 4πR³/3")
        self.degrau("C8", "= 4πR³/3")

        self.gat("deriva o volume em relação ao raio")
        D = mixl([("L", [("d", r"\dfrac{d}{dR}"), ("a", r"\Big(\dfrac43\pi R^3\Big)"), ("eq", "="), ("r", r"4\pi R^2")]), ("t", "ENGORDAR = UMA CASCA", GEO)], 1020, 660, 40)
        self.pena(parte(D.p[0], sel(D.p[0], ["d", "a"]), "d/dR (4πR³/3)"))
        self.degrau("C8", "d/dR (4πR³/3)")
        self.gat("e volta a área")
        self.pena(parte(D.p[0], sel(D.p[0], ["eq", "r"]), "= 4πR²"))
        self.degrau("C8", "= 4πR²")
        self.gat("engordar a bola")
        self.pena(D.p[1])
        self.gat("se a densidade só depende")
        E = mixl([("m", r"\de"), ("t", "SÓ DE", GEO), ("m", r"\R:"), ("m", r"\iiint\de\,dV=\int_0^R\de(\R)\,4\pi\R^2\,\dR")], 1020, 810, 36)
        self.pena(*E.p, lag=0.1)
        self.col("B4", A, B, V, D, E)
        self.marca("11_B4")
        self.sai_fim()

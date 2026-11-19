"""yt_0032 · B7 · integral sem integrar (alvos 23 e 24). 2D: o mapa de x²/(x² + y²) em quadradinhos, que encolhe, se espelha e se soma."""
from lib32 import *


def fx(X, Y):
    a, b = X - 1, Y - 1
    return a * a / (a * a + b * b + 1e-9)


def fy(X, Y):
    a, b = X - 1, Y - 1
    return b * b / (a * a + b * b + 1e-9)


class PB7(B32):
    ANTES = "VALOR MÉDIO"

    def corpo(self):
        # ── B7-1 · a função com um furo (alvo 23) ──
        self.an("B7-1")
        self.secao("INTEGRAL SEM INTEGRAR")
        v = Vw(360, 840, 240)
        NS = 240
        self.grade_on(v, rt=0.3)
        D1 = disco_img(600, 600, 240, lambda t: np.cos(t) ** 2, "#1A1534", E1)
        c1 = circ_px(*v.px(1, 1), 240, GEO, 2, z=4)
        self.play(FadeIn(D1), Create(c1), run_time=1.0)
        self.gat("considera a função xis")
        F1 = TC(r"\Am{\dfrac{x^2}{x^2+y^2}}\ \text{no disco de raio 1}", 1120, 280, 40)
        self.pena(F1)
        self.gat("na origem a fórmula")
        furo = circ_px(*v.px(1, 1), 12, BR, 2, dash=(5, 4), fill=BG_, fop=1, z=6)
        self.play(FadeIn(furo, scale=0.4), run_time=0.4)
        F2 = TC(r"(0,0):\ \tfrac{0}{0}", 1120, 400, 38)
        self.pena(F2)
        self.gat("e o limite na")
        sl = leg("SEM LIMITE: 1 NO EIXO x, 0 NO EIXO y", 1120, 450, GEO, "left", 26)
        self.pena(sl)
        self.gat("pelo eixo horizontal o")
        ex = lin_px([v.px(-.15, 1), v.px(2.2, 1)], GEO, 1.5, dash=(6, 6), z=5)
        ey = lin_px([v.px(1, -.15), v.px(1, 2.2)], GEO, 1.5, dash=(6, 6), z=5)
        self.play(Create(ex), Create(ey), run_time=0.6)
        l1 = TP("1", *v.px(1.85, 1.12), 30)
        self.pena(l1)
        self.gat("pelo vertical zero")
        l0 = TP("0", *v.px(1.12, 1.85), 30)
        self.pena(l0)
        self.gat("e um ponto tem")
        cn = leg("UM PONTO TEM CONTEÚDO NULO", 1120, 540, MEN, "left", 26)
        self.pena(cn)
        self.gat("fica entre zero e")
        F3 = TC(r"0\le\Am{f}\le 1", 1120, 600, 38)
        self.pena(F3)
        self.gat("então podemos preencher o")
        tampa = circ_px(*v.px(1, 1), 11, mixh("#1A1534", E1, .5), 1, fill=mixh("#1A1534", E1, .5), fop=1, z=7)
        self.play(FadeIn(tampa, scale=0.4), run_time=0.5)
        pf = leg("PREENCHE O FURO: INTEGRÁVEL", 1120, 680, CI, "left", 26)
        self.pena(pf)
        self.marca("23")

        # ── B7-2 · pi sobre dois, sem fazer conta (alvo 24) ──
        self.an("B7-2")
        G1 = Group(D1, c1, furo, tampa)
        sai = [m for m in self.snap() if m not in (D1, c1, furo, tampa)]
        k = 130 / 240
        G1.generate_target()
        G1.target.scale(k, about_point=PX(*v.px(1, 1))).shift(PX(250, 570) - PX(*v.px(1, 1)))
        self.play(*[FadeOut(m) for m in sai], MoveToTarget(G1), run_time=1.2)
        self.remove(*sai)
        self.grade_off(rt=0.3)
        self.gat("cria uma segunda função")
        v2 = Vw(500, 700, 130)
        D2 = disco_img(630, 570, 130, lambda t: np.sin(t) ** 2, "#1A1534", E2)
        c2 = circ_px(630, 570, 130, GEO, 2, z=4)
        mais = TC("+", 460, 570, 48, "c")
        self.pena(mais)
        self.play(FadeIn(D2), Create(c2), run_time=0.8)
        self.gat("somando as duas fora")
        igual = TC("=", 840, 570, 48, "c")
        self.pena(igual)
        D3 = sem_ctn(Circle(radius=130 / 120).move_to(PX(1010, 570)).set_fill(mixh(BG_, CI, .7), 1).set_stroke(width=0)).set_z_index(2)
        self.play(FadeTransform(D1.copy(), D3.copy()), FadeTransform(D2.copy(), D3), run_time=1.4)
        self.remove(*[m for m in self.mobjects if isinstance(m, Circle) and m is not D3 and m.get_center()[0] > PX(900, 0)[0]])
        self.add(D3)
        self.gat("resultado um")
        um = TC("1", 1010, 570, 40, "c")
        self.pena(um)
        lf = leg("FORA DA ORIGEM, A SOMA É 1", 580, 800, GEO, "center", 26)
        self.pena(lf)
        self.gat("exceto talvez naquele ponto")
        f3 = circ_px(1010, 570, 7, BR, 2, dash=(4, 3), fill=mixh(BG_, CI, .7), fop=1, z=6)
        self.play(FadeIn(f3, scale=0.4), um.animate.shift(UP * 30 / 120), run_time=0.6)
        self.gat("pela propriedade da soma")
        Lx = r"\iint\Am{\tfrac{x^2}{x^2+y^2}}"
        Ly = r"\iint\Mg{\tfrac{y^2}{x^2+y^2}}"
        A1 = L([("a", Lx), ("p", "+"), ("b", Ly), ("e1", "="), ("ar", r"\text{área}"), ("e2", "="), ("pi", r"\pi")], 1240, 330, 34)
        self.pena(A1)
        self.gat("agora a simetria espelhando")
        cp = D1.copy().set_z_index(5)
        self.add(cp)
        DIAG = np.array([1, 1, 0]) / math.sqrt(2)
        sem_meio = lambda t: (lambda v: 0.47 if 0.47 < v <= 0.5 else (0.53 if 0.5 < v < 0.53 else v))(smooth(t))   # a imagem não passa pela espessura zero
        self.play(Rotate(cp, PI, axis=DIAG, about_point=PX(250, 570), rate_func=sem_meio), run_time=1.2)
        alvo = recolore_img(D1, "#1A1534", E2).rotate(PI, axis=DIAG, about_point=PX(250, 570)).shift(PX(630, 570) - PX(250, 570))
        self.play(Transform(cp, alvo), run_time=1.4)          # o x² espelhado coincide com o y²: só anda até o disco de y² e troca a cor
        self.remove(cp)
        le = leg("ESPELHO NA DIAGONAL: AS DUAS SÃO IGUAIS", 1240, 420, GEO, "left", 26)
        self.pena(le)
        self.gat("dois números iguais que")
        Dx = r"\iint\Am{\dfrac{x^2}{x^2+y^2}}"
        Dy = r"\iint\Mg{\dfrac{y^2}{x^2+y^2}}"
        B1 = L([("a", Dx), ("p", "+"), ("b", Dy), ("eq", "="), ("pi", r"\pi")], 1240, 560, 40)
        gm(self, A1, B1, [("a", "a"), ("p", "p"), ("b", "b"), ("e2", "eq"), ("pi", "pi")], rt=1.3, copia=True, nota="mapa 8a")
        B2 = L([("two", r"2\cdot"), ("a", Dx), ("eq", "="), ("pi", r"\pi")], 1240, 560, 44)
        gm(self, B1, B2, [("p", "two"), ("b", "two"), ("a", "a"), ("eq", "eq"), ("pi", "pi")], rt=1.3, nota="mapa 8b")
        self.gat("cada um vale pi")
        B3 = L([("a", r"\iint_{\text{disco}}\Am{\dfrac{x^2}{x^2+y^2}}"), ("eq", "="), ("pi", r"\dfrac{\pi}{2}")], 1240, 560, 48)
        gm(self, B2, B3, [("a", "a"), ("eq", "eq"), ("pi", [B3._ix["pi"][0]]), ("two", [B3._ix["pi"][1], B3._ix["pi"][2]])], rt=1.4, nota="mapa 8c")
        self.gat("soma conteúdo nulo e")
        ls = leg("SOMA · CONTEÚDO NULO · SIMETRIA", 1240, 670, CI, "left", 26)
        self.pena(ls)
        self.marca("24")
        self.sai_fim()

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
        F1 = mista([("m", r"\Am{\dfrac{x^2}{x^2+y^2}}"), ("t", "NO DISCO DE RAIO 1")], 1120, 280, 32)      # T1
        self.pena(F1)
        self.gat("na origem a fórmula")
        furo = circ_px(*v.px(1, 1), 12, BR, 2, dash=(5, 4), fill=BG_, fop=1, z=6)
        self.play(FadeIn(furo, scale=0.4), run_time=0.4)
        F2 = TC(r"(0,0):\ \dfrac{0}{0}", 1120, 380, 38)                                                  # T2
        self.pena(F2)
        self.gat("e o limite na")
        sl = leg("SEM LIMITE NA ORIGEM", 1120, 448, GEO, "left", 26)                       # C9 (final)
        self.pena(sl)
        self.gat("pelo eixo horizontal o")
        ex = lin_px([v.px(-.15, 1), v.px(2.2, 1)], GEO, 1.5, dash=(6, 6), z=5)
        ey = lin_px([v.px(1, -.15), v.px(1, 2.2)], GEO, 1.5, dash=(6, 6), z=5)
        self.play(Create(ex), Create(ey), run_time=0.4)
        Ex = L([("t", r"\text{eixo }\X:\ "), ("fr", r"\dfrac{\X^2}{\X^2+0}"), ("eq", "="), ("r", "1")], 1120, 505, 34)       # C9 (final)
        self.pena(Ex)
        l1 = TP("1", *v.px(1.62, 1.14), 32)                                                             # R9: dentro do disco
        ja_escrita(l1.f)                                   # voo: liberado do portão FLASH antes do play
        self.play(FadeIn(l1[0]), TransformFromCopy(gl(Ex, "r"), l1.f, path_arc=-0.6), run_time=0.7)
        self.gat("pelo vertical zero")
        Ey = L([("t", r"\text{eixo }\Y:\ "), ("fr", r"\dfrac{0}{0+\Y^2}"), ("eq", "="), ("r", "0")], 1120, 580, 34)
        self.pena(Ey)
        l0 = TP("0", *v.px(1.14, 1.62), 32)
        ja_escrita(l0.f)                                   # voo: liberado do portão FLASH antes do play
        self.play(FadeIn(l0[0]), TransformFromCopy(gl(Ey, "r"), l0.f, path_arc=-0.6), run_time=0.7)
        self.gat("e um ponto tem")
        cn = leg("UM PONTO TEM CONTEÚDO NULO", 1120, 650, MEN, "left", 26)
        self.pena(cn)
        self.gat("fora dele a função")
        raio = lin_px([v.px(1, 1), v.px(2, 1)], BR, 2, z=8)
        self.play(Create(raio), run_time=0.4)
        self.play(Rotate(raio, PI, about_point=PX(*v.px(1, 1))), run_time=1.6, rate_func=linear)
        self.play(FadeOut(raio), run_time=0.3)
        self.remove(raio)
        self.gat("fica entre zero e")
        F3 = TC(r"0\le\Am{f}\le 1", 1120, 708, 38)
        self.pena(F3)
        self.gat("então podemos preencher o")
        tampa = circ_px(*v.px(1, 1), 11, mixh("#1A1534", E1, .5), 1, fill=mixh("#1A1534", E1, .5), fop=1, z=7)
        self.play(FadeIn(tampa, scale=0.4), run_time=0.5)
        pf = leg("PREENCHE O FURO: INTEGRÁVEL", 1120, 772, CI, "left", 26)
        self.pena(pf)
        self.gat("não depende do valor")                   # palco: o furo recebe outros valores; nada mais muda
        for c in (E2, CORAL, mixh("#1A1534", E1, .5)):
            self.play(tampa.animate.set_fill(c, 1).set_stroke(c), run_time=0.5)
            self.wait(0.5)
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
        Xf, Yf = r"\Am{\dfrac{x^2}{x^2+y^2}}", r"\Mg{\dfrac{y^2}{x^2+y^2}}"
        S16a = L([("a", Xf), ("p", "+"), ("b", Yf)], 1180, 300, 36)                         # C10 (final): mapa 16
        self.pena(S16a, passo=0.032)                       # sync
        self.gat("o numerador fica igual")
        S16b = L([("fr", r"\dfrac{\Am{x^2}+\Mg{y^2}}{x^2+y^2}")], 1180, 300, 36)
        ia, ib, fr = S16a._ix["a"], S16a._ix["b"], S16b._ix["fr"]
        # os dois numeradores sobre UMA barra; os dois denominadores viram um
        gm(self, S16a, S16b, [(ia[0:2], fr[0:2]), ("p", [fr[2]]), (ib[0:2], fr[3:5]), ([ia[2], ib[2]], [fr[5]]), (ia[3:8] + ib[3:8], fr[6:11])],
           rt=1.5, nota="mapa 16a (C10, B7-2: numeradores sobre uma barra)")
        self.gat("resultado um")
        self.play(gl(S16b, "fr").animate.set_color(CI), run_time=0.4)          # numerador e denominador iguais: acendem e somem juntos
        S16c = L([("um", "1")], 1180, 300, 40)
        gm(self, S16b, S16c, [("fr", "um")], rt=1.0, nota="mapa 16b (C10, B7-2: = 1)")
        um = TC("1", 1010, 570, 40, "c")
        self.play(TransformFromCopy(S16c[0], um[0], path_arc=-0.7), run_time=0.9)    # o 1 voa para o disco azul
        ja_escrita(um)
        self.play(FadeOut(S16c), run_time=0.3)
        self.remove(S16c)
        lf = leg("FORA DA ORIGEM, A SOMA É 1", 580, 800, GEO, "center", 26)
        self.pena(lf)
        self.gat("exceto talvez naquele ponto")
        f3 = circ_px(1010, 570, 7, BR, 2, dash=(4, 3), fill=mixh(BG_, CI, .7), fop=1, z=6)
        self.play(FadeIn(f3, scale=0.4), um.animate.shift(UP * 30 / 120), run_time=0.6)
        self.gat("pela propriedade da soma")
        Dx = r"\iint\Am{\dfrac{x^2}{x^2+y^2}}"
        Dy = r"\iint\Mg{\dfrac{y^2}{x^2+y^2}}"
        A1 = L([("a", Dx), ("p", "+"), ("b", Dy), ("eq", "="), ("pi", r"\pi")], 1180, 300, 36)          # T2: dfrac
        A1p = parte(A1, A1._ix["a"] + A1._ix["p"] + A1._ix["b"] + A1._ix["eq"], "sem π")
        self.pena(A1p)
        self.gat("valem a integral de")                   # C10 (final): ∬_disco 1 = área nasce quando a voz fala da integral de um
        P0 = L([("ii", r"\iint_{\text{disco}}"), ("um", "1"), ("eq", "="), ("ar", r"\text{área}")], 1180, 380, 34)
        self.escreve(P0, voos=[(um[0], P0._ix["um"])], atraso_caneta=0.2)
        self.gat("que é a área")                          # mapa 17: = π · 1² = π
        P1 = L([("ii", r"\iint_{\text{disco}}"), ("um", "1"), ("eq", "="), ("ar", r"\text{área}"), ("eq2", "="), ("pi", r"\pi\cdot 1^2"), ("eq3", "="),
                ("res", r"\pi")], 1180, 380, 34)
        gm(self, P0, P1, [(k, k) for k in ("ii", "um", "eq", "ar")] + [("ar", "pi"), ("um", "res")], rt=1.0, copia=True,
           nota="mapa 17 (C10, B7-2: área = π·1² = π)")
        self.remove(P0)
        pi_ = ja_escrita(parte(A1, A1._ix["pi"], "π"))
        self.play(TransformFromCopy(gl(P1, "res"), pi_, path_arc=-0.6), run_time=0.5)      # o π segue para a linha de cima
        A1._caneta, A1._esc = False, True
        self.gat("agora a simetria espelhando")
        cp = D1.copy().set_z_index(5)
        self.add(cp)
        DIAG = np.array([1, 1, 0]) / math.sqrt(2)
        sem_meio = lambda t: (lambda v: 0.47 if 0.47 < v <= 0.5 else (0.53 if 0.5 < v < 0.53 else v))(smooth(t))   # a imagem não passa pela espessura zero
        self.play(Rotate(cp, PI, axis=DIAG, about_point=PX(250, 570), rate_func=sem_meio), run_time=1.2)
        alvo = recolore_img(D1, "#1A1534", E2).rotate(PI, axis=DIAG, about_point=PX(250, 570)).shift(PX(630, 570) - PX(250, 570))
        self.play(Transform(cp, alvo), run_time=1.4)          # o x² espelhado coincide com o y²: só anda até o disco de y² e troca a cor
        self.remove(cp)
        le = leg("ESPELHO NA DIAGONAL: AS DUAS SÃO IGUAIS", 1180, 450, GEO, "left", 26)
        self.pena(le)
        self.gat("se as duas integrais")
        B2 = L([("two", "2"), ("a", Dx), ("eq", "="), ("pi", r"\pi")], 1180, 530, 38)                  # uma conta por linha
        gm(self, A1, B2, [("p", "two"), ("b", "two"), ("a", "a"), ("eq", "eq"), ("pi", "pi")], rt=1.4, copia=True, nota="mapa 8a (B7-2: duas iguais = 2·)")
        self.gat("cada uma vale pi")
        B3 = L([("a", r"\iint_{\text{disco}}\Am{\dfrac{x^2}{x^2+y^2}}"), ("eq", "="), ("pi", r"\dfrac{\pi}{2}")], 1180, 660, 46)
        gm(self, B2, B3, [("a", "a"), ("eq", "eq"), ("pi", [B3._ix["pi"][0]]), ("two", [B3._ix["pi"][1], B3._ix["pi"][2]])], rt=1.4, copia=True,
           nota="mapa 8b (B7-2: o 2 desce para o denominador)")
        self.gat("soma conteúdo nulo e")
        ls = leg("SOMA · CONTEÚDO NULO · SIMETRIA", 1180, 770, CI, "left", 26)
        self.pena(ls)
        self.marca("24")
        self.sai_fim()

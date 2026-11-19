"""yt_0044 · Lote PE4: E4-1 a E4-3 (a meia bola: z̄ em esféricas, conferência por fatias, densidade ρ = k r). C4.1–C4.14, GM16, alvos 16 a 18."""
from k44 import *  # noqa: F401,F403

COLM = 860
C43 = 1060


def lado(A, B, ga=None, gb=0, gap=12):
    B.shift(RIGHT * (A.get_right()[0] - B.get_left()[0] + gap / 120))
    ya = A[0][ga].get_center()[1] if ga is not None else A.get_center()[1]
    B.shift(UP * (ya - B[0][gb].get_center()[1]))
    return B


class PE4(B44):
    ANTES = "CONFERINDO EM ESFÉRICAS"

    def corpo(self):
        # ── E4-1 · a meia bola: o centro de massa em esféricas (alvo 16, C4.1–C4.5, GM16) ─────────────────────
        self.an("E4-1")
        pal = self.palco("semi", OM, P=0.0)
        rz = self.rot3(pal, "ez", r"\Z", size=34, ancora="c")
        self.titulo("A MEIA BOLA: ONDE ELA EQUILIBRA", rt=0.5, junto=self.ent3d(pal))

        self.gat("uma meia bola")
        self.degrau("C4.0", "meia bola: 0 <= r <= R, 0 <= phi <= pi/2, 0 <= theta <= 2pi, rho = k")
        self.pena(rz)
        l1 = TC(r"0\le\R\le R,\ \ 0\le\F\le\frac{\pi}{2},\ \ 0\le\T\le2\pi,\ \ \de=k", COLM, 160, 38)
        self.pena(l1)
        self.col("E4-1", l1)

        self.gat("A massa primeiro")
        self.degrau("C4.1a", "M = k * 2pi * [-cos phi]_0^{pi/2} * R^3/3")
        l2a = TC(r"M=k\cdot2\pi\cdot\Big[-\cos\F\Big]_0^{\pi/2}\cdot\dfrac{R^3}{3}", COLM, 260, 38)
        self.pena(l2a)
        self.col("E4-1", l2a)

        self.gat("o de fi")
        cg_c, cf_c, cm_c = chip(r"[-\cos\F]_0^{\pi/2}=0-(-1)=1", COLM, 345, 26)
        self.chip_pena(cg_c, cf_c, cm_c)
        self.col("E4-1", cg_c, chips=1)

        self.gat("metade da bola")
        self.degrau("C4.1", "M = k * 2pi * 1 * R^3/3 = (2/3) pi k R^3")
        l2b = TC(r"=k\cdot2\pi\cdot1\cdot\dfrac{R^3}{3}=\dfrac23\pi kR^3", COLM, 260, 38)
        l2b.shift(RIGHT * (pxof(l2a.get_right())[0] + 12 - pxof(l2b.get_left())[0]) / 120)
        self.pena(l2b)
        self.col("E4-1", l2b, chips=1)

        self.gat("A altura, nas esféricas")
        self.degrau("C4.2a", "z = r cos phi")
        rr = self.rot3(pal, "r", r"\R", size=28, ancora="c")
        rf = self.rot3(pal, "phi", r"\F", size=28, ancora="c")
        rzz = self.rot3(pal, "z", r"\Z", size=28, ancora="c")
        sqZ, lqZ = legq(EZ, "z = r cos φ", 120, 1020, 30)
        self.play(*pal.anim(1.0, P=1.0), FadeIn(sqZ), run_time=1.0)
        self.pena(rr, rf, rzz, lqZ)

        self.gat("o momento em relação ao chão")
        self.degrau("C4.2b", "M_xy = k int int int r cos phi * r^2 sen phi dr dphi dtheta")
        l3 = TC(r"\Mxy=k\int_0^{2\pi}\!\!\int_0^{\pi/2}\!\!\int_0^R\R\cos\F\cdot\Jr\,\dR\,\dF\,\dT", COLM, 450, 40)
        self.pena(l3)
        self.col("E4-1", l3, chips=1)

        self.gat("cada letra separa")
        self.degrau("C4.2", "= k * 2pi * (int_0^{pi/2} sen phi cos phi dphi) * R^4/4")
        l4 = TC(r"=k\cdot2\pi\cdot\Big(\int_0^{\pi/2}\sen\F\cos\F\,\dF\Big)\cdot\dfrac{R^4}{4}", COLM + 40, 560, 38)
        self.pena(l4)
        self.col("E4-1", l4, chips=1)

        self.gat("seno vezes o cosseno")
        self.degrau("C4.3", "int_0^{pi/2} sen phi cos phi dphi = [sen^2 phi/2]_0^{pi/2} = 1/2 - 0 = 1/2")
        l5 = TC(r"\int_0^{\pi/2}\sen\F\cos\F\,\dF=\Big[\dfrac{\sen^2\F}{2}\Big]_0^{\pi/2}=\dfrac12-0=\dfrac12", COLM, 670, 38)
        self.pena(l5)
        self.col("E4-1", l5, chips=1)

        self.gat("Juntando")
        self.degrau("C4.4", "M_xy = k * 2pi * 1/2 * R^4/4 = pi k R^4/4")
        l6 = TC(r"\Mxy=k\cdot2\pi\cdot\dfrac12\cdot\dfrac{R^4}{4}=\dfrac{\pi kR^4}{4}", COLM, 775, 40)
        self.pena(l6)
        self.col("E4-1", l6, chips=1)

        self.gat("dividindo pela massa")
        self.degrau("C4.5", "zbar = (pi k R^4/4)/((2/3) pi k R^3) = (1/4)/(2/3) R = 3R/8")
        za = L([("lhs", r"\zb="), ("fr", r"\dfrac{\pi kR^4/4}{\frac23\pi kR^3}")], COLM + 10, 895, 46)
        self.pena(za)
        zb_ = L([("eq", "="), ("fr", r"\dfrac{1/4}{2/3}"), ("r", r"\,R")], COLM + 10, 895, 46)
        lado(za, zb_, ultimo(za, "lhs"), 0)
        self.gm(16, za, zb_, [("fr", ["fr", "r"])], rt=1.0, copia=True, nota="GM16a: (pi k R^4/4)/((2/3) pi k R^3) -> (1/4)/(2/3) R")
        zc = L([("eq", "="), ("fr", r"\dfrac{3R}{8}")], COLM + 10, 895, 46)
        lado(zb_, zc, 0, 0)
        self.gm(16, zb_, zc, [(["fr", "r"], "fr")], rt=0.9, copia=True, nota="GM16b: (1/4)/(2/3) R -> 3R/8")
        x0, _ = pxof(za.get_corner(UL))
        x1, _ = pxof(zc.get_corner(DR))
        top = min(pxof(m.get_corner(UL))[1] for m in (za, zb_, zc))
        bot = max(pxof(m.get_corner(DR))[1] for m in (za, zb_, zc))
        molz = moldura(x0 - 14, top - 10, (x1 - x0) + 28, (bot - top) + 20, MEN, 1.0, 3, 12)
        xm, ym = pal.pt("z38")
        cmk = cm_mark(xm, ym, 14)
        sqL, lqL = legq(LIL, "CENTRO DE MASSA", 440, 1020, 30)
        self.play(Create(molz), FadeIn(cmk), FadeIn(sqL), run_time=0.4)
        self.pena(lqL)
        self.col("E4-1", za, zb_, zc, chips=1)
        self.marca("16_E4-1")
        cg_z, cf_z, cm_z = chipm([("m", r"\zb=\dfrac{3R}{8}"), ("t", "(ESFÉRICAS)", BR)], COLM, 140, 28)
        self.sobe_sai(l1, l2a, l2b, cg_c, l3, l4, l5, l6, za, zb_, molz, rr, rf, rzz, cmk, sqZ, lqZ, sqL, lqL, rt=0.3)
        self.chip_vira(cg_z, cf_z, cm_z, zc, rt=0.45, nota="o 3R/8 vira o chip do E4-2")

        # ── E4-2 · conferindo por fatias (alvo 17, C4.6–C4.8) ──────────────────────────────────────────────────
        self.an("E4-2")
        pal, rots = self.troca3d(pal, [rz], "semiFatia", OM, fatia=0.0, rots=[("ez", r"\Z", dict(size=34, ancora="c"))])
        self.titulo("CONFERINDO POR FATIAS", rt=0.25)
        self.col("E4-2", cg_z, chips=1)

        self.gat("fatiar a meia bola")
        self.degrau("C4.6a", "fatia na altura z: disco de raio sqrt(R^2 - z^2)")
        rra = self.rot3(pal, "raio", r"\sqrt{R^2-\Z^2}", size=26, ancora="c")
        rzf = self.rot3(pal, "zf", r"\Z", size=28, ancora="c")
        sqF, lqF = legq(LI, "FATIA NA ALTURA z: UM DISCO", 120, 1020, 30)
        self.play(*pal.anim(1.0, fatia=1.0), FadeIn(sqF), run_time=1.0)
        self.pena(rra, rzf, lqF)
        f1 = mixl([("t", "FATIA NA ALTURA z: DISCO DE RAIO", LI), ("m", r"\sqrt{R^2-\Z^2}")], COLM, 250, 38)
        self.pena(f1)
        self.col("E4-2", f1, chips=1)

        self.gat("pelo teorema de Pitágoras")
        self.degrau("C4.6", "área = pi(R^2 - z^2)")
        f2 = mixl([("t", "ÁREA =", GEO), ("m", r"\pi(R^2-\Z^2)")], COLM, 340, 42)
        self.pena(f2)
        self.col("E4-2", f2, chips=1)

        self.gat("a integral dupla de cada fatia")
        self.degrau("C4.7a", "iiint z dV = int_0^R z (iint_FATIA dA) dz = int_0^R z pi(R^2 - z^2) dz")
        f3 = TC(r"\iiint\Z\,dV=\int_0^R\Z\cdot\Big(\iint_{\mathrm{FATIA}}dA\Big)\dZ=\int_0^R\Z\cdot\pi(R^2-\Z^2)\,\dZ", COLM, 450, 38)
        self.pena(f3)
        self.col("E4-2", f3, chips=1)

        self.gat("polinômio simples")
        self.degrau("C4.7", "= pi[R^2 z^2/2 - z^4/4]_0^R = pi(R^4/2 - R^4/4) = pi R^4/4 ✓")
        f4 = TC(r"=\pi\Big[\dfrac{R^2\Z^2}{2}-\dfrac{\Z^4}{4}\Big]_0^R=\pi\Big(\dfrac{R^4}{2}-\dfrac{R^4}{4}\Big)=\dfrac{\pi R^4}{4}\ \Me{\checkmark}", COLM + 40, 570, 38)
        self.pena(f4)
        self.col("E4-2", f4, chips=1)

        self.gat("O volume sai igual")
        self.degrau("C4.8a", "V = int_0^R pi(R^2 - z^2) dz = pi[R^2 z - z^3/3]_0^R = pi(R^3 - R^3/3) = 2 pi R^3/3 ✓")
        f5 = TC(r"V=\int_0^R\pi(R^2-\Z^2)\,\dZ=\pi\Big[R^2\Z-\dfrac{\Z^3}{3}\Big]_0^R=\pi\Big(R^3-\dfrac{R^3}{3}\Big)=\dfrac{2\pi R^3}{3}\ \Me{\checkmark}", COLM, 690, 34)
        self.pena(f5)
        self.col("E4-2", f5, chips=1)

        self.gat("três oitavos de novo")
        self.degrau("C4.8", "zbar = (pi R^4/4)/(2 pi R^3/3) = 3R/8 ✓")
        f6 = TC(r"\zb=\dfrac{\pi R^4/4}{2\pi R^3/3}=\dfrac{3R}{8}\ \Me{\checkmark}", COLM + 10, 820, 48)
        self.pena(f6)
        mol6 = caixa_men(f6)
        xm, ym = pal.pt("z38")
        cmk2 = cm_mark(xm, ym, 14)
        self.play(Create(mol6), FadeIn(cmk2), run_time=0.4)
        self.col("E4-2", f6, chips=1)
        self.marca("17_E4-2")
        cards, cms, rot_cm = [], [], []
        for i, (t, zb, grad) in enumerate((("UNIFORME", .375, False), ("ρ = k r", .4, True))):
            X0 = 60 + i * 480
            pn = painel2d44(X0, 180, 450, 560)
            lb = leg(t, X0 + 24, 222, CI if grad else GEO, "left", 28)
            v = Vista2D(X0 + 225, 640, 170)
            semi = [(math.cos(a), math.sin(a)) for a in np.linspace(0, PI, 61)]
            if grad:     # uma imagem só (RGBA): o FadeOut de 25 polígonos sobrepostos deixava um fantasma de ~30 % no fim do lote
                W_, H_ = 680, 340
                ys_, xs_ = np.mgrid[0:H_, 0:W_]
                rad = np.hypot((xs_ + .5 - W_ / 2) / (W_ / 2), (H_ - ys_ - .5) / H_)
                tt_ = np.clip(rad, 0, 1) ** .85
                c0_, c1_ = np.array([0x10, 0x24, 0x3A], float), np.array([0x35, 0xD9, 0xFF], float)
                arr_ = np.zeros((H_, W_, 4), np.uint8)
                arr_[..., :3] = (c0_ * (1 - tt_[..., None]) + c1_ * tt_[..., None]).round().astype(np.uint8)
                arr_[..., 3] = (np.clip((1.0 - rad) * H_ / 2, 0, 1) * 255).round().astype(np.uint8)
                fill = img_px(arr_, X0 + 225 - 170, 640 - 170, 340, 170, z=1)
            else:
                fill = poly_px([v.P(*p) for p in semi], mixh("#16123A", GEO, .32), 1.0, z=1)
            cont = v.linha(semi + [(1, 0)], GEO, 3)
            eixo = v.linha([(0, 0), (0, 1.25)], EZ, 2, dash=(7, 6))
            q = v.P(0, zb)
            cmk = cm_mark(q[0], q[1], 15)
            tz = TC(r"0{,}4\,R" if grad else r"0{,}375\,R", q[0] + 30, q[1], 28, "l")
            gz = VGroup(placa_min(tz), tz)
            gz._txt = "zbar card"
            cards.append((pn, lb, fill, cont, eixo, tz))
            cms.append(cmk)
            rot_cm.append(gz)

        an = []
        for pn, lb, fill, cont, eixo, tz in cards:
            an += [FadeIn(pn), FadeIn(fill), Create(cont), Create(eixo)]
            self.dentro(pn._painel, lb, tz, cont)
        self.sai(pal.fundo, *rots, rra, rzf, cmk2, sqF, lqF, cg_z, f1, f2, f3, f4, f5, f6, mol6, rt=0.35, extra=an)

        # ── E4-3 · e se a densidade crescer para fora? (alvo 18, C4.9–C4.14) ──────────────────────────────────
        self.an("E4-3")
        self.titulo("E SE A DENSIDADE CRESCER PARA FORA?", rt=0.4)
        self.pena(cards[0][1], cards[1][1])

        self.gat("mais densa conforme se afasta do centro")
        self.degrau("C4.9a", "rho = k r (cresce com a distância)")
        self.pena(rot_cm[0], extra=[FadeIn(cms[0])])
        g1 = mixl([("m", r"\de=k\,\R"), ("t", "(CRESCE COM A DISTÂNCIA)", GEO)], C43, 200, 44)
        self.pena(g1)
        self.col("E4-3", g1)

        self.gat("A massa ganha um r")
        self.degrau("C4.9", "M = k iiint r * r^2 sen phi dr dphi dtheta = k * 2pi * 1 * R^4/4 = pi k R^4/2")
        g2 = TC(r"M=k\iiint\R\cdot\Jr\,\dR\,\dF\,\dT=k\cdot2\pi\cdot1\cdot\dfrac{R^4}{4}=\dfrac{\pi kR^4}{2}", C43, 320, 32)
        self.pena(g2)
        self.col("E4-3", g2)

        self.gat("E o momento")
        self.degrau("C4.10", "M_xy = k iiint r * r cos phi * r^2 sen phi ... = k * 2pi * 1/2 * R^5/5 = pi k R^5/5")
        g3 = TC(r"\Mxy=k\iiint\R\cdot\R\cos\F\cdot\Jr\,d\cdots=k\cdot2\pi\cdot\dfrac12\cdot\dfrac{R^5}{5}=\dfrac{\pi kR^5}{5}", C43, 440, 30)
        self.pena(g3)
        self.col("E4-3", g3)

        self.gat("Dividindo um pelo outro")
        self.degrau("C4.11a", "zbar = (pi k R^5/5)/(pi k R^4/2) = (2/5) R")
        g4 = TC(r"\zb=\dfrac{\pi kR^5/5}{\pi kR^4/2}=\dfrac25\,R", C43 + 10, 580, 50)
        mol4 = caixa_men(g4)
        self.pena(g4)
        self.gat("dois quintos de R")
        self.play(Create(mol4), FadeIn(cms[1]), run_time=0.4)
        self.pena(rot_cm[1])
        self.col("E4-3", g4)

        self.gat("Subiu")
        self.degrau("C4.11", "3R/8 = 0,375 R < 2R/5 = 0,4 R")
        g5 = TC(r"\dfrac{3R}{8}=0{,}375\,R\ <\ \dfrac{2R}{5}=0{,}4\,R", C43, 720, 42)
        X0r, X1r, Yb = 140, 900, 870
        pxv = lambda val: X0r + (X1r - X0r) * (val - .3) / .25
        regua = lin_px([(X0r, Yb), (X1r, Yb)], GEO, 3, z=6)
        tk = [lin_px([(pxv(val), Yb - 14), (pxv(val), Yb + 14)], c, 3, z=7) for val, c in ((.375, GEO), (.4, CI))]
        tl = [leg(lab, pxv(val), Yb + 48, c, "center", 28) for val, lab, c in ((.375, "3/8", GEO), (.4, "2/5", CI))]
        tzr = leg("z̄ / R", X1r + 20, Yb + 10, GEO, "left", 28)
        self.play(Create(regua), *[Create(m) for m in tk], run_time=0.4)
        self.pena(*tl, tzr)
        self.pena(g5)
        self.col("E4-3", g5)

        self.gat("o caso extremo")
        self.degrau("C4.13", "caso-limite: tudo na casca => zbar = R/2")
        cg_k, cf_k, cm_k = chipm([("t", "CASO-LIMITE: TUDO NA CASCA", MEN), ("m", r"\Rightarrow\zb=\dfrac R2")], C43, 840, 30, MEN)
        self.chip_pena(cg_k, cf_k, cm_k)
        tk3 = lin_px([(pxv(.5), Yb - 14), (pxv(.5), Yb + 14)], MEN, 3, z=7)
        tl3 = leg("1/2", pxv(.5), Yb + 48, MEN, "center", 28)
        tc3 = leg("TUDO NA CASCA", pxv(.5) - 90, Yb - 34, MEN, "left", 26)
        self.play(Create(tk3), run_time=0.3)
        self.pena(tl3, tc3)
        self.col("E4-3", cg_k, chips=1)
        self.marca("18_E4-3")

        self.sai_fim(rt=0.35)

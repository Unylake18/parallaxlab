"""yt_0041 · S · síntese (S1, sem alvo) e a lata com o próximo vídeo (S2, alvo 14).
S1: três colunas com ✓ sobre o papel: ENDEREÇO (r, φ, θ) com o mini desenho do B1-1; dV = r² sen φ dr dφ dθ com ARESTAS · DUAS POLARES ·
DETERMINANTE; BOLA, BOLA PESADA e CASQUINHA, com os resultados voando das suas fontes (miniaturas da bola e da casquinha).
S2: a lata 3D, MESMO INTEGRANDO, as duas sondas (uma por vez), a diagonal da quina e RACHA EM φ = π/4; o cartão NO PRÓXIMO VÍDEO por ≥ 8 s;
o CTA liso."""
from k41 import *
from sec_b1 import de_ponto
from sec_b2 import MINI
from sec_b6 import rotP

XC = [340, 960, 1580]
CW = 560


def img_mini(nome, cx, cy, wmax, hmax):
    from PIL import Image
    a = np.array(Image.open(MINI / f"mini_{nome}.png").convert("RGBA"))
    h, w = a.shape[:2]
    k = min(wmax / w, hmax / h)
    return img_px(a, cx - w * k / 2, cy - h * k / 2, w * k, h * k, z=3)


class PS(B41):
    ANTES = "QUANDO USAR"

    def corpo(self):
        # ── S1 ────────────────────────────────────────────────────────────────────────────────────────────
        self.an("S1")
        self.grade = papel(passo=0.5).set_z_index(-10)
        cards = [painel41(XC[k] - CW / 2, 190, CW, 700) for k in range(3)]
        self.play(FadeIn(self.grade), Create(cards[0]), run_time=0.4)
        self.titulo("RESUMINDO", rt=0.3)
        t1 = mixl([("t", "ENDEREÇO", BR), ("m", r"(\R,\F,\T)")], XC[0] - 220, 250, 40)
        self.pena(*t1.p, lag=0.1)
        im = img_mini("ponto", XC[0], 520, 460, 400)
        self.play(FadeIn(im), run_time=0.5)
        e1 = leg("r: A DISTÂNCIA ATÉ A ORIGEM", XC[0] - 240, 770, RO, "left", 26)
        e2 = leg("φ: A PARTIR DO POLO NORTE", XC[0] - 240, 810, FI, "left", 26)
        e3 = leg("θ: O ÂNGULO DAS POLARES", XC[0] - 240, 850, TH, "left", 26)
        self.gat("a distância até a origem")
        self.pena(e1)
        self.gat("o ângulo a partir do polo")
        self.pena(e2)
        self.gat("e téta o ângulo das polares")
        self.pena(e3)
        c1 = check_px(XC[0] + 230, 250)
        self.play(Create(c1), run_time=0.3)

        self.gat("o pedacinho de volume")
        self.play(Create(cards[1]), run_time=0.4)
        dv = TC(r"dV=\J\;\dR\,\dF\,\dT", XC[1], 330, 46, "c")
        self.pena(dv)
        cam = [leg("ARESTAS", XC[1], 470, GEO, "center", 30), leg("DUAS POLARES", XC[1], 540, GEO, "center", 30),
               leg("DETERMINANTE", XC[1], 610, GEO, "center", 30)]
        for t_, fr in zip(cam, ["as arestas", "as duas polares", "e o determinante"]):
            self.gat(fr)
            self.pena(t_)
        self.gat("o teorema pede as hipóteses")
        tt = leg("TEOREMA: HIPÓTESES NO INTERIOR", XC[1], 720, BR, "center", 26)
        t2 = leg("A BOLA EM DUAS METADES", XC[1], 760, BR, "center", 26)
        self.pena(tt, t2, lag=0.3)
        c2 = check_px(XC[1] + 240, 250)
        self.play(Create(c2), run_time=0.3)

        self.gat("com isso a bola deu")
        self.play(Create(cards[2]), run_time=0.4)
        mb = img_mini("bola", XC[2] - 180, 330, 150, 150)
        mq = img_mini("casquinha", XC[2] - 180, 680, 150, 160)
        self.play(FadeIn(mb), FadeIn(mq), run_time=0.4)
        r1 = mixl([("t", "BOLA", BR), ("m", r"\Me{\dfrac43\pi R^3}")], XC[2] - 80, 290, 38)
        r2 = mixl([("t", "BOLA PESADA", BR), ("m", r"\Me{\pi}")], XC[2] - 80, 420, 38)
        r3 = mixl([("t", "CASQUINHA", BR), ("m", r"\Me{\pi}")], XC[2] - 80, 680, 38)
        self.pena(r1.p[0])
        self.voos([(de_ponto(r1.p[1], *pxof(mb.get_center())), r1.p[1])], rt=0.8, nota="S1: 4πR³/3 voa da bola (B2-4)")
        self.gat("a bola pesada deu pi")
        self.pena(r2.p[0])
        self.voos([(de_ponto(r2.p[1], *pxof(mb.get_center())), r2.p[1])], rt=0.8, nota="S1: π voa da bola pesada (B5)")
        self.gat("e a casquinha deu pi")
        self.pena(r3.p[0])
        self.voos([(de_ponto(r3.p[1], *pxof(mq.get_center())), r3.p[1])], rt=0.8, nota="S1: π voa da casquinha (B6-2)")
        cg = leg("CONFERIDA PELA GEOMETRIA", XC[2] - 80, 740, GEO, "left", 26)
        self.gat("conferida pela geometria")
        self.pena(cg)
        c3 = check_px(XC[2] + 240, 250)
        self.play(Create(c3), run_time=0.3)
        for k, ms in enumerate([[t1, e1, e2, e3], [dv, *cam, tt, t2], [r1, r2, r3, cg]]):
            self.dentro((XC[k] - CW / 2, 190, XC[k] + CW / 2, 890), *ms)
        self.marca("S1", agora=True)

        # ── S2 ────────────────────────────────────────────────────────────────────────────────────────────
        self.an("S2")
        self.titulo("E UMA LATA?", rt=0.3)
        self.gat("a mesma densidade")
        saem = [m for m in self.mobjects if m not in self.fixos() and not isinstance(m, ValueTracker) and m is not self.clk and m is not self.grade]
        lt = self.palco("lata", cam_alvo("s2"), obst=["O", "parede", "tampa"], sonda1=0.0, sonda2=0.0, quina=0.0)
        self.play(*[FadeOut(m) for m in saem], run_time=0.5)
        self.remove(*saem)
        m1 = mixl([("t", "MESMO INTEGRANDO", GEO), ("m", r"\Ci{\sqrt{\X^2+\Y^2+\Z^2}}")], 780, 200, 44)
        self.pena(*m1.p, lag=0.1)
        self.gat("numa lata")
        lt.fundo.op.set_value(0.0)
        self.add(lt.fundo)
        self.play(lt.fundo.op.animate.set_value(1.0), run_time=0.6)                          # G1: o papel fica sob a lata
        m2 = TC(r"\X^2+\Y^2\le1,\quad 0\le\Z\le1", 780, 300, 46)
        self.pena(m2)
        # o corte 1 × 1 (painel2d de 640 × 480 em (60, 560)): a lata pequena fica no alto, sem nada dela dentro do painel
        pcq = painel2d41(60, 560, 640, 480)
        self.play(Create(pcq), run_time=0.5)
        tcp = leg("O CORTE: UMA PÁGINA", 84, 604, TH, "left", 26)
        Vq = Vista2D(150, 990, 300)
        quad = Polygon(*[PX(*Vq.P(*p)) for p in [(0, 0), (1, 0), (1, 1), (0, 1)]]).set_fill(mixh("#16123A", GEO, .25), 1).set_stroke(width=0).set_z_index(-1)
        eixq = VGroup(Vq.seta((0, 0), (1.25, 0), SOMB, 4, 16), Vq.seta((0, 0), (0, 1.15), EZ, 4, 16))
        bordq = Vq.linha([(1, 0), (1, 1), (0, 1)], GEO, 4)
        self.play(FadeIn(quad), Create(eixq), Create(bordq), run_time=0.6)
        zq = TC(r"\Z", Vq.P(0, 1.15)[0] + 14, Vq.P(0, 1.15)[1] + 8, 32, "c")
        sq_ = TC(r"\Rs", Vq.P(1.25, 0)[0] - 4, Vq.P(1.25, 0)[1] - 26, 32, "c")
        self.pena(tcp, zq, sq_, lag=0.1)
        pw = (1, 1 / math.tan(PI / 3))
        ptp = (math.tan(PI / 8), 1)
        self.gat("pela parede")
        sw = VGroup(Vq.linha([(0, 0), pw], RO, 6), Vq.ponto(pw, CORAL, 10), Vq.ponto((0, 0), AZC, 10))
        self.play(lt.tr["sonda1"].animate(rate_func=linear).set_value(1.0), Create(sw), run_time=1.0)
        l1 = rotP(r"\Co{\R=\dfrac{1}{\sen\F}}", Vq.P(*pw)[0] + 18, Vq.P(*pw)[1], 32, "l")
        self.pena(l1)
        self.gat("pela tampa")
        st = VGroup(Vq.linha([(0, 0), ptp], RO, 6), Vq.ponto(ptp, CORAL, 10))
        self.play(lt.tr["sonda2"].animate(rate_func=linear).set_value(1.0), Create(st), run_time=1.0)
        l2 = rotP(r"\Co{\R=\dfrac{1}{\cos\F}}", Vq.P(*ptp)[0] + 20, Vq.P(*ptp)[1] + 56, 32, "l")
        self.pena(l2)
        self.dentro(pcq._painel, tcp, zq, sq_, l1, l2)
        self.gat("a região racha")
        dq = Vq.linha([(0, 0), (1, 1)], AL, 3, dash=(9, 7))
        self.play(lt.tr["quina"].animate(rate_func=linear).set_value(1.0), Create(dq), run_time=0.8)
        rq = leg("A FÓRMULA RACHA NA DIAGONAL: φ = π/4", 780, 500, AL, "left", 30)
        self.pena(rq)
        ds1 = leg("A SONDA PARA NA PAREDE OU NA TAMPA:", 780, 400, GEO, "left", 30)
        ds2 = leg("DUAS FÓRMULAS PARA r", 780, 445, GEO, "left", 30)
        self.pena(ds1, ds2, lag=0.2)
        self.gat("para uma lata")
        cd = painel41(1060, 560, 800, 330)
        n1 = T("NO PRÓXIMO VÍDEO", 1460, 640, 30, "center", GEO)
        n2 = T("COORDENADAS", 1460, 720, 48, "center", BR)
        n3 = T("CILÍNDRICAS", 1460, 785, 48, "center", SOMB)
        n4 = leg("POLARES NO CHÃO + A ALTURA z", 1460, 850, GEO, "center", 30)
        t_card = self.t
        self.play(Create(cd), run_time=0.4)
        self.pena(n1)
        self.gat("no próximo vídeo")
        self.pena(n2, n3, lag=0.3)
        self.gat("as polares no chão")
        self.pena(n4)
        self.dentro((1060, 560, 1860, 890), n1, n2, n3, n4)
        self.marca("14_S2", agora=True)
        self.gat("deixa o like")
        print(f"[cartao] próximo vídeo na tela por {self.t - t_card:.2f} s antes do CTA")
        cta41(self, rt_fim=0.0)

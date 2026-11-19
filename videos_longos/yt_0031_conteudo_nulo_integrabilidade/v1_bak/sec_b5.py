"""yt_0031 · B5 · fronteira: a borda é uma solda (alvos 18 e 19). 3D: b52 (quarto de disco, f = 1 estendida por zero)."""
from PIL import Image

from v31 import *


def miniatura_muro(x0, y0, w, h, crop=(140, 180, 1240, 880)):
    """Recorte do quadro do muro (b21, n = 16, renderizado pelo mesmo c31.js) dentro de um painel."""
    a = np.array(Image.open(AQUI / "threejs" / "fixos" / "b21_muro_1080.png").convert("RGBA").crop(crop))
    return img_px(a, x0, y0, w, h, z=3)


def disco_pts(v, n=90):
    return [v.px(0, 0)] + [v.px(2 * math.cos(PI / 2 * k / n), 2 * math.sin(PI / 2 * k / n)) for k in range(n + 1)]


class PB5(B31):
    ANTES = "CURVAS TÊM CONTEÚDO NULO"

    def corpo(self):
        # ── B5-1 · interior, exterior e fronteira (alvo 18) ────────────────────────────────────────────
        self.an("B5-1")
        self.secao("FRONTEIRA")
        self.grade_on(rt=0.4)
        disco = poly_px(disco_pts(CH), mixh(BG_, CI, .45), z=1)
        bd = borda_ch(CH, mixh(BG_, GEO, .5), 2)
        arco = arco_px(CH, BR, 4, z=7)
        s1, s2 = lin_px([CH.px(0, 0), CH.px(2, 0)], BR, 4, z=7), lin_px([CH.px(0, 0), CH.px(0, 2)], BR, 4, z=7)
        self.play(FadeIn(disco), Create(bd), Create(arco), Create(s1), Create(s2), run_time=1.2)
        lB = TP("B", *CH.px(.45, .95), 40)
        self.pena(lB)
        self.gat("desenha em volta dele")
        ba = leg("BOLA ABERTA: DISCO SEM A BORDA", 1124, 420, GEO, "left", 24)
        self.pena(ba)
        U = 240

        def sonda(c, r, cor, w=3):
            X, Y = CH.px(*c)
            return circ_px(X, Y, r * U, cor, w, dash=(8, 6), z=8)
        self.gat("uma bola inteira dentro")
        pi_ = ponto_px(*CH.px(.9, .55), BR, 6)
        bi = sonda((.9, .55), .25, BR)
        self.play(FadeIn(pi_, scale=0.5), Create(bi), run_time=0.7)
        li = leg("INTERIOR", *CH.px(.9, .18), BR, "center", 22)
        self.pena(li)
        self.gat("se dá para escolher uma inteira fora")
        pe = ponto_px(*CH.px(1.82, 1.8), BR, 6)
        be = sonda((1.82, 1.8), .15, BR)
        self.play(FadeIn(pe, scale=0.5), Create(be), run_time=0.7)
        lex = leg("EXTERIOR", *CH.px(1.82, 2.08), BR, "center", 22)
        self.pena(lex)
        self.gat("não importa o quanto")
        fb = (math.sqrt(2), math.sqrt(2))
        pf = ponto_px(*CH.px(*fb), POS, 7, z=9)
        bf = sonda(fb, .28, POS)
        self.play(FadeIn(pf, scale=0.5), Create(bf), run_time=0.7)
        prev = bf
        for r in (.17, .08):
            nv = sonda(fb, r, POS)
            self.play(TransformFromCopy(prev, nv), run_time=0.7)
            prev = nv
        self.gat("ela sempre pega")
        t1 = leg("TODA BOLA PEGA B", 1124, 280, POS, "left", 30)
        t2 = leg("E PEGA FORA DE B", 1124, 325, POS, "left", 30)
        self.pena(t1, t2, lag=0.6)
        self.gat("esses são os pontos")
        lf = leg("FRONTEIRA", *CH.px(1.78, 1.42), POS, "left", 24)
        self.pena(lf)
        self.gat("no quarto de disco a fronteira")
        borda3 = VGroup(arco, s1, s2)
        self.play(borda3.animate.set_stroke(width=W(7)), run_time=0.4)
        self.play(borda3.animate.set_stroke(width=W(4)), run_time=0.4)
        fr = T("FRONTEIRA DE B", 1120, 540, 36)
        fa = leg("O ARCO + OS 2 SEGMENTOS", 1124, 590, BR, "left", 28)
        self.pena(fr)
        self.pena(fa)
        self.gat("um ponto de fronteira pode")
        pd = leg("PODE ESTAR EM B OU NÃO", 1124, 680, GEO, "left", 24)
        self.pena(pd)
        self.marca("18")

        # ── B5-2 · a borda é uma solda (alvo 19) ─────────────────────────────────────────────────────
        self.an("B5-2")
        sai = [ba, pi_, bi, li, pe, be, lex, pf, bf, *self._sondas(bf, prev), t1, t2, lf, fr, fa, pd, lB]
        self.play(*[FadeOut(m) for m in sai], run_time=0.4)
        self.remove(*sai)
        self.gat("coloca a região dentro")
        self.play(bd.animate.set_stroke(BR, W(5), 1), run_time=0.4)
        self.play(bd.animate.set_stroke(mixh(BG_, GEO, .5), W(2), 1), run_time=0.4)
        gform = TC(r"g=\begin{cases}\f & \text{em } B\\ 0 & \text{fora de } B\end{cases}", 1120, 290, 40)
        self.gat("e faz a função valer")
        self.pena(gform)
        self.gat("no quarto de disco a função")
        u1 = TP(r"\f=1", *CH.px(.7, .7), 30)
        u0 = TP(r"\f=0", *CH.px(1.72, 1.82), 30)
        self.pena(u1)
        self.pena(u0)
        self.gat("e o que acontece quando")
        pp = ponto_px(*CH.px(1.05, 1.05), POS, 9, z=12)
        self.play(FadeIn(pp, scale=0.5), run_time=0.3)
        self.play(pp.animate.move_to(CH.P(1.62, 1.62)), run_time=1.6, rate_func=linear)
        self.gat("a função salta de")
        pal = Palco3D("b52", self, CAM_BAIXO, cresce=0.0, muro=0.0)
        entra3d(self, pal, saem=[disco, bd, arco, s1, s2, u1, u0, pp], rt_cam=1.6)
        ex = pal.prende(TC(r"\X", 0, 0, 30, "c"), "ex")
        self.play(*pal.anim(0.8, cresce=1.0), run_time=0.8)
        f1 = pal.prende(TP(r"\f=1", 0, 0, 30), "B")
        f0 = pal.prende(TP(r"\f=0\ \text{fora}", 0, 0, 28), "fora")
        self.pena(ex, f1, f0, rt=1.0)
        self.gat("a borda funciona exatamente")
        bs = T("BORDA = SOLDA", 1120, 450, 48)
        bz = T("ENTRE f E ZERO", 1120, 510, 48, cor=CI)
        self.pena(bs)
        self.pena(bz)
        self.gat("olha o prédio")
        self.play(*pal.anim(1.2, muro=1.0), run_time=1.2)
        mx, my = pal.pt("muro")
        tb = leg("TAMPAS SÓ NA BORDA", mx + 30, my - 60, CORAL, "left", 26)
        self.pena(tb)
        self.gat("e se a fronteira tem")
        pn = painel(1120, 600, 640, 330)
        mini = miniatura_muro(1130, 610, 620, 320)
        self.play(Create(pn), FadeIn(mini), run_time=0.8)
        cm = leg("A CHAPA DE DOIS METAIS", 1440, 970, GEO, "center", 22)
        self.pena(cm)
        self.marca("19")
        self.sai_fim()

    def _sondas(self, a, b):
        return [m for m in self.mobjects if isinstance(m, DashedVMobject) and m is not a]

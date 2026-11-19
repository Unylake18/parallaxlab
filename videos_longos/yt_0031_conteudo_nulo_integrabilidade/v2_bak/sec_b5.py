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
    ANTES = "FRONTEIRA"          # v2 (G2): a linha 2 do canto já está na tela no 1º quadro do bloco

    def corpo(self):
        # ── B5-1 · interior, exterior e fronteira (alvo 18) ────────────────────────────────────────────
        self.an("B5-1")
        self.grade_on(rt=0)               # v2 (G2): a grade entra junto da figura, sem quadro vazio
        disco = poly_px(disco_pts(CH), mixh(BG_, CI, .45), z=1)
        bd = borda_ch(CH, mixh(BG_, GEO, .5), 2)
        arco = arco_px(CH, BR, 4, z=7)
        s1, s2 = lin_px([CH.px(0, 0), CH.px(2, 0)], BR, 4, z=7), lin_px([CH.px(0, 0), CH.px(0, 2)], BR, 4, z=7)
        self.play(FadeIn(disco), Create(bd), Create(arco), Create(s1), Create(s2), run_time=0.6)
        lB = TP("B", *CH.px(.45, .95), 40)
        self.pena(lB)
        self.gat("desenha em volta dele")
        ba = leg("BOLA ABERTA: DISCO SEM A BORDA", 1124, 420, GEO, "left", 24)
        self.pena(ba)
        U = 240

        def sonda(c, r, cor, w=3):
            X, Y = CH.px(*c)
            return circ_px(X, Y, r * U, cor, w, dash=(8, 6), z=8)
        # v2: cada sonda entra na sua palavra; a da fronteira ENCOLHE de verdade (os tamanhos anteriores ficam tracejados, finos)
        self.gat("o ponto é interior")
        pi_ = ponto_px(*CH.px(.9, .55), BR, 6)
        bi = sonda((.9, .55), .25, BR)
        li = leg("INTERIOR", *CH.px(.9, .18), BR, "center", 24)
        self.play(FadeIn(pi_, scale=0.5), Create(bi), run_time=0.5)
        self.pena(li)
        self.gat("é exterior")
        pe = ponto_px(*CH.px(1.82, 1.8), BR, 6)
        be = sonda((1.82, 1.8), .15, BR)
        lex = leg("EXTERIOR", *CH.px(1.66, 2.11), BR, "center", 24)
        self.play(FadeIn(pe, scale=0.5), Create(be), run_time=0.5)
        self.pena(lex)
        self.gat("não importa o quanto")
        fb = (math.sqrt(2), math.sqrt(2))
        pf = ponto_px(*CH.px(*fb), POS, 7, z=9)
        bf = sonda(fb, .28, POS)
        self.play(FadeIn(pf, scale=0.5), Create(bf), run_time=0.5)
        fant = []
        for r_ant, r in ((.28, .17), (.17, .08)):
            fa_ = sonda(fb, r_ant, POS, 1.5)
            fa_.set_stroke(opacity=0.5)
            self.play(Transform(bf, sonda(fb, r, POS)), FadeIn(fa_), run_time=0.8)
            fant.append(fa_)
        prev = bf
        self.gat("ela sempre pega")
        t1 = leg("TODA BOLA PEGA B", 1124, 280, POS, "left", 30)
        t2 = leg("E PEGA FORA DE B", 1124, 325, POS, "left", 30)
        self.pena(t1, t2, lag=0.6)
        self.gat("pontos de fronteira no")
        lf = leg("FRONTEIRA", *CH.px(2.07, 1.40), POS, "left", 24)          # v2: fora da borda direita da chapa
        self.pena(lf)
        self.gat("no quarto de disco a fronteira")
        fr = T("FRONTEIRA DE B", 1120, 540, 36)
        fa = leg("O ARCO + OS 2 SEGMENTOS", 1124, 590, BR, "left", 28)
        self.pena(fr)
        self.gat("é o arco e")
        self.acende([arco], cor=POS, rt=1.0)
        self.gat("os dois segmentos sobre")
        self.acende([s1, s2], cor=POS, rt=1.0)
        self.pena(fa)
        self.gat("um ponto de fronteira pode")
        pd = leg("PODE ESTAR EM B OU NÃO", 1124, 680, GEO, "left", 24)
        self.pena(pd)
        self.marca("18")

        # ── B5-2 · a borda é uma solda (alvo 19) ─────────────────────────────────────────────────────
        self.an("B5-2")
        sai = [ba, pi_, bi, li, pe, be, lex, pf, bf, *fant, t1, t2, lf, fr, fa, pd, lB]
        self.play(*[FadeOut(m) for m in sai], run_time=0.4)
        self.remove(*sai)
        u1 = TP(r"\f=1", *CH.px(.7, .7), 30)
        u0 = TP(r"\f=0", *CH.px(1.72, 1.82), 30)
        self.gat("coloca a região dentro")
        self.acende([bd], cor=BR, rt=1.0)                # v2: a moldura do retângulo acende e a parte de fora ganha f = 0
        self.pena(u0)
        gform = TC(r"g=\begin{cases}\f & \text{em } B\\ 0 & \text{fora de } B\end{cases}", 1120, 290, 40)
        self.gat("e faz a função valer")
        self.pena(gform)
        self.gat("vale um dentro")
        self.pena(u1)
        self.gat("e o que acontece quando")
        pp = ponto_px(*CH.px(1.05, 1.05), POS, 9, z=12)
        self.play(FadeIn(pp, scale=0.5), run_time=0.3)
        self.play(pp.animate.move_to(CH.P(1.62, 1.62)), run_time=1.6, rate_func=linear)
        self.gat("salta de um para")
        self.acende([arco], cor=POS, rt=0.5)             # v2: a borda acende no salto
        pal = Palco3D("b52", self, CAM_BAIXO, cresce=0.0, muro=0.0)
        entra3d(self, pal, saem=[disco, bd, arco, s1, s2, u1, u0, pp], rt_cam=0.9, rt_x=0.35)
        ex = pal.prende(TC(r"\X", 0, 0, 30, "c"), "ex")
        bs = T("BORDA = SOLDA", 1120, 450, 48)
        bz = T("ENTRE f E ZERO", 1120, 510, 48, cor=CI)
        self.gat("a borda funciona exatamente")
        self.pena(bs, extra=pal.anim(0.9, cresce=1.0), rt=0.9)
        self.pena(bz)
        f1 = pal.prende(TP(r"\f=1", 0, 0, 30), "B")
        f0 = pal.prende(TP(r"\f=0\ \text{fora}", 0, 0, 28), "fora", dx=140, dy=10)       # fora da base, sem cruzar as arestas
        self.pena(ex, f1, f0, rt=1.0)
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
        self.gat("a área dessas células")
        pal.acende3d(1.4)
        self.gat("uma borda curva e")
        self.sublinha(bs, 1.2)
        self.marca("19")
        # v2 (G2): o 3D fica na tela no fim do bloco; o B6 nasce desta cena
        if self._aid is not None:
            self._fecha(antes=0.4)
        for m in self.snap():
            if not isinstance(m, Fundo3D):
                m.clear_updaters()
        self.limpa(pal.fundo, *pal.tr.values(), pal.acende, rt=0.4)

    def _sondas(self, a, b):
        return [m for m in self.mobjects if isinstance(m, DashedVMobject) and m is not a]

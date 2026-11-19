"""yt_0041 · B7 · quando usar esféricas (sem alvo). Papel de borda a borda; três miniaturas com ✓ (bola, casca, casquinha: recortes dos PNGs 3D
em cartões opacos) e a lata em silhueta com ✗; as três legendas da Tela, cada uma no seu gatilho."""
from k41 import *
from sec_b2 import MINI

CARD_Y, CARD_W, CARD_H = 200, 380, 330
XS = [150, 570, 990, 1410]


def mini_card(nome, X, silhueta=False):
    from PIL import Image
    a = np.array(Image.open(MINI / f"mini_{nome}.png").convert("RGBA"))
    if silhueta:                                 # só a silhueta: a forma em GEO chapado (sem o desenho de dentro)
        m = a[..., 3] > 12
        a = np.zeros_like(a)
        a[m] = [int(GEO[1:3], 16), int(GEO[3:5], 16), int(GEO[5:7], 16), 90]
    h, w = a.shape[:2]
    k = min((CARD_W - 40) / w, (CARD_H - 40) / h)
    W_, H_ = w * k, h * k
    im = img_px(a, X + (CARD_W - W_) / 2, CARD_Y + (CARD_H - H_) / 2, W_, H_, z=3)
    return painel41(X, CARD_Y, CARD_W, CARD_H), im


class PB7(B41):
    ANTES = "A CASQUINHA"

    def corpo(self):
        self.an("B7")
        self.grade = papel(passo=0.5).set_z_index(-10)
        cards = [("bola", None), ("cebola", "cascas e cones"), ("casquinha", "cones com vértice")]
        for k, (nome, fr) in enumerate(cards):
            if fr:
                self.gat(fr)
            p, im = mini_card(nome, XS[k])
            ck = check_px(XS[k] + CARD_W / 2, CARD_Y + CARD_H + 40)
            self.play(Create(p), FadeIn(im), *([FadeIn(self.grade)] if k == 0 else []), run_time=0.2)
            if k == 0:
                self.titulo("QUANDO USAR", rt=0.3)
                self.gat("de bolas")
            self.play(Create(ck), run_time=0.2)
        self.gat("com vértice na origem")
        l1 = mixl([("t", "BOLAS, CASCAS, CONES COM VÉRTICE NA ORIGEM", BR)], 240, 720, 44)
        c1 = check_px(180, 720)
        self.play(Create(c1), run_time=0.2)
        self.pena(*l1.p)
        self.gat("e quando o integrando")
        l2 = mixl([("m", r"\X^2+\Y^2+\Z^2"), ("t", "NO INTEGRANDO", BR)], 240, 810, 44)
        c2 = check_px(180, 810)
        self.play(Create(c2), run_time=0.2)
        self.pena(*l2.p, lag=0.1)
        self.gat("e quando não usar")
        p, im = mini_card("lata", XS[3], silhueta=True)
        x4 = cruz_px(XS[3] + CARD_W / 2, CARD_Y + CARD_H + 40)
        self.play(Create(p), FadeIn(im), run_time=0.2)
        self.play(Create(x4), run_time=0.2)
        self.gat("paredes que não passam")
        l3 = mixl([("t", "PAREDES QUE NÃO PASSAM PELA ORIGEM", AL)], 240, 900, 44)
        c3 = cruz_px(180, 900)
        self.play(Create(c3), run_time=0.2)
        self.pena(*l3.p)
        self.col("B7", l1, l2, l3)
        self.marca("B7", agora=True)
        self.sai_fim()

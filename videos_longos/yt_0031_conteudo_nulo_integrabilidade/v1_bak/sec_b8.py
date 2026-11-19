"""yt_0031 · B8 · quando falha (alvos 26 e 27). Os pontinhos da Dirichlet são imagens fixas (uma por nível de zoom)."""
from v31 import *


class LCG:
    """o mesmo gerador do sb31 (s ← 16807·s mod 2³¹ − 1)."""

    def __init__(self, s):
        self.s = s

    def __call__(self):
        self.s = (self.s * 16807) % 2147483647
        return self.s / 2147483647


def arr_pontinhos(L, seed, n=1400, tam=4):
    a = np.zeros((L, L, 3))
    a[:] = hx(RAMP0)
    r = LCG(seed)
    for _ in range(n):
        c = hx(CI) if r() < .5 else hx("#2B2558")
        x, y = int(r() * L), int(r() * L)
        a[y:y + tam, x:x + tam] = c
    return a


def arr_racionais(W_=480, seed=11, n=2600):
    a = np.zeros((W_, W_, 3))
    a[:] = hx(mixh(BG_, AL, .18))
    r = LCG(seed)
    for _ in range(n):
        x, y = int(r() * W_), int(r() * W_)
        a[y:y + 3, x:x + 3] = hx(CI)
    return a


class PB8(B31):
    ANTES = "O TEOREMA"

    def corpo(self):
        # ── B8-1 · a função de Dirichlet (alvo 26) ──────────────────────────────────────────────────
        self.an("B8-1")
        self.secao("QUANDO FALHA")
        self.gat("olha esta função")
        fd = TC(r"\f(\X,\Y)=\begin{cases}1 & \X,\Y\ \text{racionais}\\ 0 & \text{senão}\end{cases}", 1160, 330, 40)
        self.pena(fd)
        self.gat("aqueles que se escrevem")
        rac = leg("RACIONAL: FRAÇÃO DE INTEIROS", 1164, 450, GEO, "left", 24)
        self.pena(rac)
        self.gat("pega qualquer retanguinho")
        ims, bords, nomes = [], [], []
        for i, (X, t) in enumerate(((120, "CÉLULA"), (460, "ZOOM ×10"), (800, "ZOOM ×100"))):
            ims.append(img_px(arr_pontinhos(280, 7 + i * 13), X, 260, 280, 280, z=2, nearest=True))
            bords.append(ret_px(X, 260, X + 280, 540, stroke=GEO, wpx=2, z=3))
            nomes.append(leg(t, X + 140, 580, GEO, "center", 24))
        setas = [T("→", X + 310, 410, 40, "center", GEO, bold=False) for X in (120, 460)]
        self.play(FadeIn(ims[0]), Create(bords[0]), run_time=0.6)
        self.pena(nomes[0])
        self.gat("por menor que seja")
        for k in (1, 2):
            self.pena(setas[k - 1], rt=0.4)
            self.play(TransformFromCopy(Group(ims[k - 1], bords[k - 1]), Group(ims[k], bords[k])), run_time=0.8)
            self.pena(nomes[k], rt=0.5)
        mm = leg("A MISTURA NÃO MUDA", 560, 640, BR, "center", 30)
        self.pena(mm)
        self.gat("então em todas as células")
        ec = TC(r"\text{em toda célula:}\ \ \mij=\Az0,\ \ \Mij=\Co1", 1160, 540, 36)
        self.pena(ec)
        X0, Y0, k_ = 170, 720, 60
        base = lin_px([(X0, Y0 + 240), (X0 + 1500, Y0 + 240)], GEO, 2)
        frases = ["a soma por cima dá", "refina quanto quiser", "a diferença continua quatro", "as paredes nunca"]
        for i, (t, fr) in enumerate(zip(["4 × 4", "8 × 8", "16 × 16", "64 × 64"], frases)):
            self.gat(fr)
            X = X0 + 120 + i * 360
            bc = ret_px(X, Y0 + 240 - 4 * k_ * .9, X + 60, Y0 + 240, fill=CORAL, z=4)
            ba = ret_px(X + 80, Y0 + 236, X + 140, Y0 + 240, fill=AZC, z=4)
            l4 = TC(r"\Co4", X + 30, Y0 + 240 - 4 * k_ * .9 - 24, 26, "c")
            l0 = TC(r"\Az0", X + 110, Y0 + 210, 26, "c")
            nm = leg(t, X + 70, Y0 + 280, GEO, "center", 22)
            if i == 0:
                self.play(Create(base), run_time=0.4)
            self.play(GrowFromEdge(bc, DOWN), GrowFromEdge(ba, DOWN), run_time=0.6)
            self.pena(l4, l0, nm, rt=0.8)
        fim = leg("4 CONTRA ZERO: NÃO É INTEGRÁVEL", 1680, 1030, BR, "right", 26)
        self.pena(fim)
        self.marca("26")

        # ── B8-2 · uma fronteira que não some (alvo 27) ─────────────────────────────────────────────
        self.an("B8-2")
        self.play(*[FadeOut(m) for m in self.snap()], run_time=0.5)
        self.remove(*self.snap())
        self.grade_on(rt=0.3)
        self.gat("pega o conjunto dos pontos")
        ch = img_chapa(arr_racionais())
        cj = TC(r"\{(\X,\Y):\ \X,\Y\ \text{racionais}\}", 1120, 280, 40)
        bdr = borda_ch(CH, GEO, 2)
        self.play(FadeIn(ch), Create(bdr), run_time=0.8)
        self.pena(cj)
        self.gat("qualquer disquinho")
        sd = circ_px(*CH.px(1.2, 1.1), 40, POS, 3, dash=(8, 6), z=8)
        self.play(Create(sd), run_time=0.6)
        tb = leg("TODA BOLA PEGA PONTOS DOS DOIS", 600, 262, POS, "center", 24)
        self.pena(tb)
        self.play(sd.animate.move_to(CH.P(.6, 1.5)), run_time=0.9)
        self.play(sd.animate.move_to(CH.P(1.2, 1.1)), run_time=0.9)
        self.gat("então a fronteira dele")
        bv = borda_ch(CH, AL, 4, z=6)
        self.play(ReplacementTransform(bdr, bv), run_time=0.6)
        fq = T("FRONTEIRA = O QUADRADO TODO", 1120, 380, 34, cor=AL)
        self.pena(fq)
        self.gat("e não tem conteúdo nulo")
        a4 = leg("ÁREA 4: NÃO É CONTEÚDO NULO", 1124, 430, GEO, "left", 26)
        self.pena(a4)
        self.gat("um último cuidado")
        cs = T("CONDIÇÃO SUFICIENTE", 1120, 580, 40, cor=CI)
        self.pena(cs)
        self.gat("quando as hipóteses valem")
        hv = leg("HIPÓTESES VALEM → INTEGRAL EXISTE", 1124, 650, BR, "left", 26)
        self.pena(hv)
        self.gat("quando não valem")
        nv = leg("NÃO VALEM → OLHE AS SOMAS", 1124, 700, GEO, "left", 26)
        self.pena(nv)
        self.gat("aqui a não integrabilidade")
        gn = sorted(nv.family_members_with_points(), key=lambda g_: g_.get_left()[0])
        self.sublinha(VGroup(*gn[-12:]), 1.2)
        self.marca("27")
        self.sai_fim()

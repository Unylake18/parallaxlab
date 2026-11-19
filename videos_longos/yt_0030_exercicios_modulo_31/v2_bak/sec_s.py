"""Lote PS · S RESUMO (alvo 28), NO PRÓXIMO VÍDEO (alvo 29) e CTA. A escada sobe degrau a degrau, cada um no seu trecho de fala; as quatro aplicações
entram à direita no "e nas aplicações". O cartão do próximo vídeo não tem canto nem logo: a chapa colorida [0, 2]² (densidade x² + y²), a régua
0–20 kg e os palpites 8 kg? (âmbar) e 16 kg? (magenta). Depois o CTA padrão da série (o do EP. 03)."""
from alg30 import *  # noqa: F401,F403

DEG = [("MESMA FÓRMULA, DOIS FILMES", GEO, "a mesma fórmula conta dois filmes"), ("CURVAS ONDE NÃO MUDA", CAMPO2, "um campo se desenha pelas curvas"),
       ("VOLTA ≠ GIRO", VIO, "o sentido da volta"), ("GRADIENTE NÃO GIRA", VIO, "um gradiente nunca gira"),
       ("PARCIAIS NÃO BASTAM", CORAL, "ter derivadas parciais não basta"), ("A TABELA PREVÊ", LIMA, "e com ela você prevê")]
APL = [("RIO QUE GIRA NAS MARGENS", VIO, "um rio reto que gira"), ("PAREDE: SÓ DEFORMA", LIMA, "uma parede onde a água"),
       ("MAPAS QUE NÃO ENTORTAM", CORAL, "mapas que nunca entortam"), ("1/r E 1/r²", CAMPO2, "e o rotacional e o divergente escolhendo")]


def degrau(i):
    t, c, _ = DEG[i]
    X0, Y0, w = 120 + i * 120, 860 - i * 95, 520
    r = RoundedRectangle(width=w / 120, height=78 / 120, corner_radius=8 / 120).move_to(PX(X0 + w / 2, Y0 - 62 + 39))
    r.set_fill(PLACA_V4, 0.9).set_stroke(c, 3 / 1.2, 1)
    r._sem_contorno = True
    return VGroup(r.set_z_index(20), T(t, X0 + 22, Y0 - 12, 28, cor=BR))


def aplic(i):
    t, c, _ = APL[i]
    Y0 = 380 + i * 120
    r = RoundedRectangle(width=470 / 120, height=84 / 120, corner_radius=8 / 120).move_to(PX(1320 + 235, Y0 + 42))
    r.set_fill(opacity=0).set_stroke(c, 3 / 1.2, 1)
    r._sem_contorno = True
    return VGroup(r.set_z_index(20), T(t, 1555, Y0 + 54, 28, "center", up=False))


def chapa_densa():
    X0, Y0, S, N = 360, 420, 440, 44
    g = VGroup()
    for i in range(N):
        for j in range(N):
            xx, yy = (i + .5) / N * 2, (j + .5) / N * 2
            c = mix("#0E3A40", "#8CFFD2", (xx * xx + yy * yy) / 8)
            q = Rectangle(width=(S / N + .6) / 120, height=(S / N + .6) / 120).move_to(PX(X0 + (i + .5) * S / N, Y0 + S - (j + .5) * S / N))
            q.set_fill(c, 1).set_stroke(width=0)
            q._sem_contorno = True
            g.add(q)
    bd = Rectangle(width=S / 120, height=S / 120).move_to(PX(X0 + S / 2, Y0 + S / 2)).set_fill(opacity=0).set_stroke(GEO, 3 / 1.2, 1)
    bd._sem_contorno = True
    l1 = T("2 m", X0 + S / 2, Y0 + S + 44, 28, "center", GEO, bold=False, up=False)
    l2 = T("2 m", X0 - 20, Y0 + S / 2, 28, "right", GEO, bold=False, up=False)
    return VGroup(g, bd, l1, l2)


def regua():
    rx, ry, rw = 1060, 640, 600
    g = VGroup()
    ln = VMobject().set_points_as_corners([PX(rx, ry), PX(rx + rw, ry)]).set_stroke(GEO, 3 / 1.2, 1)
    ln._sem_contorno = True
    g.add(ln)
    for k in range(0, 21, 4):
        X = rx + k / 20 * rw
        tk = VMobject().set_points_as_corners([PX(X, ry - 10), PX(X, ry + 10)]).set_stroke(GEO, 3 / 1.2, 1)
        tk._sem_contorno = True
        g.add(tk, T(str(k), X, ry + 44, 24, "center", GEO, bold=False))
    g.add(T("MASSA (kg)", rx + rw / 2, ry + 90, 26, "center", GEO, bold=False, up=False))
    return g


def palpite(k, cor):
    rx, ry, rw = 1060, 640, 600
    X = rx + k / 20 * rw
    tri = Polygon(PX(X, ry - 14), PX(X - 12, ry - 38), PX(X + 12, ry - 38)).set_fill(cor, 1).set_stroke(width=0)
    tri._sem_contorno = True
    return VGroup(tri, T(f"{k} kg?", X, ry - 56, 34, "center", cor, up=False))


class LoteS(Base):
    ANTES = "APLICAÇÃO · POR QUE UM SOBRE A DISTÂNCIA AO QUADRADO"

    def corpo(self):
        # ── S-1 · a escada inteira (alvo 28) ──
        self.an("S-1")
        self.secao("RESUMO")
        ae = legenda("A ESCADA", 300, 940, GEO, "left", 28)
        dg = [degrau(i) for i in range(6)]
        troca(self, "A3 → S (resumo)")
        self.play(FadeIn(ae), FadeIn(dg[0], shift=0.06 * UP), run_time=0.6)
        for i in range(1, 6):
            if i == 2:
                caixa3 = dg[2][0]
                self.gat("saem da mesma conta")
                self.play(FadeIn(caixa3, shift=0.06 * UP), run_time=0.4)
                mini = L([("m", r"\V{2-2\alpha}")], 0, 0, 30, "c").move_to(caixa3.get_center() + RIGHT * 1.4)
                escreve(self, mini, 0.4)
                self.gat(DEG[2][2])
                self.play(FadeIn(dg[2][1]), run_time=0.4)
                continue
            if i == 3:
                X0, Y0 = 120 + 3 * 120, 860 - 3 * 95
                cx4 = dg[3][0]
                l1 = T("GRADIENTE NÃO GIRA", X0 + 22, Y0 - 36, 22, cor=BR)
                l2 = T("ROTACIONAL NÃO DIVERGE", X0 + 22, Y0 - 10, 22, cor=BR)
                self.gat(DEG[3][2])
                self.play(FadeIn(cx4, shift=0.06 * UP), FadeIn(l1), run_time=0.5)
                self.gat("e um rotacional nunca diverge")
                self.play(FadeIn(l2, shift=0.04 * UP), run_time=0.4)
                continue
            self.gat(DEG[i][2])
            self.play(FadeIn(dg[i], shift=0.06 * UP), run_time=0.5)
        aa = legenda("AS APLICAÇÕES", 1555, 350, GEO, "center", 28)
        ap = [aplic(i) for i in range(4)]
        self.gat("e nas aplicações")
        self.play(FadeIn(aa, shift=0.05 * UP), run_time=0.4)
        for i in range(4):
            self.gat(APL[i][2])
            self.play(FadeIn(ap[i], shift=0.05 * UP), run_time=0.4)
        self.ate(1.0)

        # ── S-2 · no próximo vídeo (alvo 29) ──
        self.an("S-2")
        g1 = T("NO PRÓXIMO VÍDEO", 960, 215, 34, "center", GEO, bold=False)
        g2 = T("SOMA DE RIEMANN E INTEGRAL DUPLA", 960, 305, 64, "center")
        sai = self.snap() + [m for m in (self.h1, self.h2, self.wm) if m is not None]
        self.gat("no próximo vídeo")
        troca(self, "S → cartão do próximo vídeo (sem canto e sem logo)")
        self.play(*[FadeOut(m) for m in sai], FadeIn(g1, shift=0.06 * UP), FadeIn(g2, shift=0.06 * UP), run_time=0.6)
        self.remove(*sai)
        self.h2 = None
        ch = chapa_densa()
        q0 = Square(side_length=66 / 120).move_to(PX(580, 640)).set_fill(CHAPA_C, 1).set_stroke(CORAL, 4 / 1.2, 1)
        q0._sem_contorno = True
        pt = Dot(PX(580, 640), radius=6 / 120, color=CORAL)
        pt._sem_contorno = True
        self.gat("tudo foi medido num ponto")
        self.play(FadeIn(q0), run_time=0.3)
        self.play(Transform(q0, pt), run_time=1.0)
        grade4 = VGroup(*[linha7([PX(360 + k * 110, 420), PX(360 + k * 110, 860)], GEO, 2) for k in range(1, 4)],
                        *[linha7([PX(360, 420 + k * 110), PX(800, 420 + k * 110)], GEO, 2) for k in range(1, 4)]).set_z_index(30)
        self.gat("somar pedacinhos")
        self.play(FadeOut(q0), FadeIn(ch[1]), Create(grade4), FadeIn(ch[0]), FadeIn(ch[2]), FadeIn(ch[3]), run_time=0.7)
        lv = legenda("LEVE NUM CANTO, DENSA NO OPOSTO", 360 + 220, 420 - 24, GEO, "center", 26)
        self.gat("uma chapa quadrada")
        self.gat("leve num canto")
        self.play(FadeIn(lv, shift=0.05 * UP), run_time=0.4)
        rg = regua()
        self.gat("qual é a massa dela")
        self.play(FadeIn(rg), run_time=0.5)
        for k, cor, fr in ((8, AMB, "oito quilos"), (16, MAG, "dezesseis")):
            self.gat(fr)
            self.play(FadeIn(palpite(k, cor), shift=0.05 * DOWN), run_time=0.4)
        self.ate(1.0)

        # ── S-3 · CTA padrão ──
        self.an("S-3")
        self.gat("se essa aula te ajudou")
        troca(self, "cartão → CTA")
        logo_cta(self, rt_fim=2.0)

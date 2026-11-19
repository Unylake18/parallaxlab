"""yt_0031 · H · as três perguntas (alvos 01 e 02). Sem canto."""
from v31 import *


def metais_vetor(v, n=16, alphaV=0.6, z=1):
    """Chapa de dois metais em peças vetoriais: leve (sob a solda), pesado (sobre), células vermelhas (n×n) e grade."""
    xs = np.linspace(0, 2, 121)
    curva = [v.px(a, float(g_solda(a))) for a in xs]
    leve = poly_px([v.px(0, 0), v.px(2, 0)] + curva[::-1], LEVE, z=z)
    pes = poly_px([v.px(0, 2), v.px(2, 2)] + curva[::-1], PESADO, z=z)
    h = 2 / n
    verm = VGroup(*[ret_px(*v.px(i * h, (j + 1) * h), *v.px((i + 1) * h, j * h), fill=mixh(BG_, AL, alphaV), z=z + 1)
                    for i, j in sorted(celulas_verm(n))])
    return leve, pes, verm


class PH(B31):
    CANTO = False

    def corpo(self):
        self.an("H1")
        tit = leg("TRÊS PERGUNTAS DO VÍDEO PASSADO", 960, 150, GEO, "center", 30)
        Xs, L = [80, 690, 1300], 420
        pn = [painel(X0, 200, 540, 700) for X0 in Xs]
        # ── painel 1: dois metais ──
        v1 = Vw(140, 760, L / 2)
        leve, pes, verm = metais_vetor(v1, 16)
        sold = solda_px(v1, BR, 3)
        bord = borda_ch(v1, GEO, 2)
        self.play(FadeIn(pn[0]), run_time=0.4)
        self.pena(tit, extra=[GrowFromEdge(leve, DOWN), FadeIn(bord)], rt=1.6)
        self.gat("em cima três")
        self.play(GrowFromEdge(pes, UP), run_time=1.0)
        r1 = TP(r"\rr=1", *v1.px(.4, .35), 30)
        r3 = TP(r"\rr=3", *v1.px(1.6, 1.7), 30)
        self.pena(r1)
        self.pena(r3)
        self.gat("uma linha de solda")
        self.play(Create(sold), run_time=1.4, rate_func=linear)
        self.gat("agora divide a chapa")
        gr = grade_ch(16, v1, mixh(BG_, GEO, .35), 1, z=3)
        self.play(LaggedStart(*[Create(l) for l in gr], lag_ratio=0.03), run_time=1.6)
        self.gat("e os pedaços que cruzam")
        self.play(LaggedStart(*[FadeIn(c) for c in verm], lag_ratio=0.08), run_time=1.6)
        self.gat("se o ponto escolhido")
        cel = ret_px(*v1.px(1.125, 1.5), *v1.px(1.25, 1.375), stroke=POS, wpx=3, z=9)
        self.play(Create(cel), run_time=0.5)
        fio = lin_px([(389, 445), (355, 327)], POS, 2, z=9)
        lp = VGroup(ret_px(300, 215, 410, 288, fill=PESADO, z=9), ret_px(300, 288, 410, 325, fill=LEVE, z=9),
                    lin_px([(300, 287), (410, 289)], BR, 3, z=10))
        lpb = ret_px(300, 215, 410, 325, stroke=POS, wpx=3, z=11)
        self.play(Create(fio), GrowFromPoint(lp, PX(372, 400)), GrowFromPoint(lpb, PX(372, 400)), run_time=0.7)
        p1 = ponto_px(331, 309, POS, 7, z=12)
        l1 = TP(r"\rr=1", 430, 309, 24, "l")
        self.play(FadeIn(p1, scale=0.5), run_time=0.3)
        self.pena(l1)
        self.gat("se cai do lado pesado")
        p2 = ponto_px(375, 250, POS, 7, z=12)
        self.play(TransformFromCopy(p1, p2, path_arc=-1.2), run_time=0.6)
        l3 = TP(r"\rr=3", 430, 250, 24, "l")
        self.pena(l3)
        self.gat("será que as somas")
        q1 = T("1 OU 3?", 358, 820, 30, "center", POS)
        q2 = T("A INTEGRAL EXISTE?", 350, 872, 30, "center")
        self.pena(q1, q2, lag=0.4)
        # ── painel 2: quarto de disco ──
        self.gat("e lembra do quarto")
        v2 = Vw(750, 760, L / 2)
        im8 = img_chapa(arr_escadaB(8), v2)
        g8 = grade_ch(8, v2, mixh(BG_, GEO, .3), 1)
        bd2, arc2 = borda_ch(v2, GEO, 2), arco_px(v2, CI, 3)
        self.play(FadeIn(pn[1]), FadeIn(im8), FadeIn(g8), FadeIn(bd2), Create(arc2), run_time=1.0)
        self.gat("quando a grade refinava")
        im, gg = im8, g8
        for n in (16, 32):
            im2 = img_chapa(arr_escadaB(n), v2)
            g2 = grade_ch(n, v2, mixh(BG_, GEO, .3), 1)
            novas = VGroup(*[l for k, l in enumerate(g2) if (k // 2 + 1) % 2 == 1])
            velhas = VGroup(*[l for k, l in enumerate(g2) if (k // 2 + 1) % 2 == 0])
            self.add(velhas)
            self.remove(gg)
            self.play(FadeIn(im2), LaggedStart(*[GrowFromCenter(l) for l in novas], lag_ratio=0.01), run_time=0.8)
            self.remove(im)
            im, gg = im2, g2
            self.add(gg)
            self.remove(velhas, novas)
            self.add(gg)
            self.wait(0.6)
        self.gat("mas isso acontece")
        q3 = T("A BORDA SEMPRE SOME?", 960, 872, 30, "center")
        self.pena(q3)
        # ── painel 3: x² + y² ──
        self.gat("e tem a terceira")
        v3 = Vw(1360, 760, L / 2)
        md = img_chapa(arr_dens(48), v3)
        bd3 = borda_ch(v3, GEO, 2)
        self.play(FadeIn(pn[2]), FadeIn(md), FadeIn(bd3), run_time=0.8)
        self.gat("para provar que a massa")
        fr = TP(r"|S-\tfrac{32}{3}|\le 16\Delta", 1570, 560, 40)
        self.pena(fr)
        self.gat("a gente fez uma conta")
        car = VGroup(RoundedRectangle(width=380 / 120, height=62 / 120, corner_radius=8 / 120).set_stroke(CORAL, W(4)).set_fill(opacity=0),
                     txt("CONTA SOB MEDIDA", ts(32), color=CORAL, bold=True, up=False))
        car[1].move_to(car[0]).shift(DOWN * 0 / 120)
        sem_ctn(car)
        car.move_to(PX(1570, 447)).rotate(0.12).set_z_index(26)
        car._txt = "CONTA SOB MEDIDA"
        self.play(FadeIn(car, scale=1.18), run_time=0.22, rate_func=rush_into)
        self.gat("será que precisa")
        q4 = T("TODA FUNÇÃO PRECISA DE UMA?", 1570, 872, 30, "center")
        self.pena(q4)
        self.marca("01")

        # ── H2 ──
        self.an("H2")
        sai = [lp, lpb, fio, p1, p2, l1, l3, q1, q2, q3, q4, fr, car, tit, cel, r1, r3]
        self.play(*[FadeOut(m) for m in sai], run_time=0.8)
        self.remove(*sai)
        self.gat("como saber se uma")
        G1 = Group(leve, pes, verm, sold, bord, gr)
        G2 = Group(im, gg, bd2, arc2)
        G3 = Group(md, bd3)
        destinos = [560, 860, 1160]
        Ls = 200
        anims = []
        for G, X0, (Xp, _) in zip((G1, G2, G3), destinos, ((140, 0), (750, 0), (1360, 0))):
            k = Ls / L
            G.generate_target()
            G.target.scale(k, about_point=PX(Xp, 760)).shift(PX(X0, 110 + Ls + 20) - PX(Xp, 760))
            anims.append(MoveToTarget(G))
        novos_p = [painel(X0 - 20, 110, Ls + 40, Ls + 40) for X0 in destinos]
        anims += [ReplacementTransform(a, b) for a, b in zip(pn, novos_p)]
        self.play(*anims, run_time=2.0)
        self.remove(*sai)
        h1 = T("O PROBLEMA NÃO É O SALTO", 960, 600, 76, "center")
        h2 = T("É ONDE ELE ACONTECE", 960, 700, 76, "center", CI)
        self.gat("uma função pode ter")
        self.pena(h1)
        self.gat("o que importa é onde")
        self.pena(h2)
        self.gat("e quanto espaço")
        h3 = leg("E QUANTO ESPAÇO OCUPA", 960, 790, GEO, "center", 30)
        self.pena(h3)
        self.gat("a chapa de dois metais tem")
        self.pulso(Group(G1, novos_p[0]), 1.08, 1.0)
        self.marca("02")
        self.sai_fim()

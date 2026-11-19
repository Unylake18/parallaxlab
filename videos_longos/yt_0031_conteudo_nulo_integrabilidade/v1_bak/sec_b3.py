"""yt_0031 · B3 · conteúdo nulo (alvos 12 a 14)."""
from v31 import *

MEN22 = mixh(BG_, MEN, 0.22)


def cobertura(n, fill=0.22, wpx=2, eng=0.0, dash=None, z=4):
    h = 2 / n
    rs, area = VGroup(), 0.0
    for i in range(n):
        a, b = i * h, i * h + h
        mn, mx = faixa(a, b)
        area += (b - a) * (mx - mn)
        r = ret_px(*CH.px(a - eng, mx + eng), *CH.px(b + eng, mn - eng), fill=mixh(BG_, MEN, fill) if fill else None, stroke=MEN, wpx=wpx, z=z)
        if dash:
            r = sem_ctn(DashedVMobject(r, num_dashes=max(8, int(r.get_arc_length() * 120 / sum(dash))), dashed_ratio=dash[0] / sum(dash))).set_z_index(z)
        rs.add(r)
    rs.area = area
    return rs


class Orc:
    """barra do orçamento ε (altura fixa 400 px = ε) e o gasto (sb31 `orc`)."""
    X, YB, H = 930, 780, 400

    def __init__(self, eps, gasto):
        X, YB, H = self.X, self.YB, self.H
        self.caixa = ret_px(X, YB - H, X + 46, YB, stroke=MEN, wpx=2, z=5)
        self.fill = ret_px(X, YB - H * gasto / eps, X + 46, YB, fill=mixh(BG_, MEN, .75), z=4)
        self.marca = ret_px(X - 8, YB - H - 2, X + 54, YB - H + 2, fill=MEN, z=6)
        self.leps = TC(r"\eps=" + self.num(eps), X + 23, YB - H - 30, 26, "c")
        self.lg = leg("GASTO", X + 23, YB + 34, MEN, "center", 20)
        self.lv = self.rot_gasto(eps, gasto)

    @staticmethod
    def num(v):
        return {1: "1", 0.25: r"\tfrac14", 0.05: r"0{,}05"}.get(v, str(v).replace(".", "{,}"))

    def rot_gasto(self, eps, gasto):
        return TP(r"\Me{" + f"{gasto:.2f}".replace(".", "{,}") + "}", self.X + 23, self.YB - self.H * gasto / eps - 22, 22)

    def ret_fill(self, eps, gasto):
        return ret_px(self.X, self.YB - self.H * gasto / eps, self.X + 46, self.YB, fill=mixh(BG_, MEN, .75), z=4)

    def ret_marca(self, alt):
        return ret_px(self.X - 8, self.YB - alt - 2, self.X + 54, self.YB - alt + 2, fill=MEN, z=6)


class PB3(B31):
    ANTES = "A CHAPA DE DOIS METAIS"

    def corpo(self):
        # ── B3-1 · a definição (alvo 12) ──────────────────────────────────────────────────────────────
        self.an("B3-1")
        self.secao("CONTEÚDO NULO")
        self.grade_on(rt=0.4)
        bd = borda_ch(CH, mixh(BG_, GEO, .6), 2)
        sold = solda_px(CH, BR, 4)
        self.play(Create(bd), Create(sold), run_time=1.0)
        lD = TP("D", *CH.px(-.14, .8), 34)
        self.pena(lD)
        self.gat("a ideia é cobrir")
        cob = cobertura(4)
        rot = []
        for i in range(4):
            mn, mx = faixa(i * .5, i * .5 + .5)
            rot.append(TP(r"\Me{A_%d}" % (i + 1), *CH.px(i * .5 + .25, mx + .12), 26))
        for r, l in zip(cob, rot):
            self.play(FadeIn(r), run_time=0.35)
            self.pena(l, passo=0.04)
        self.gat("desde que seja um número")
        nf = leg("NÚMERO FINITO DE RETÂNGULOS", 1124, 740, GEO, "left", 24)
        self.pena(nf)
        self.gat("a soma das áreas tem")
        o = Orc(1, cob.area)
        self.play(Create(o.caixa), FadeIn(o.marca), run_time=0.5)
        self.pena(o.lg)
        self.play(GrowFromEdge(o.fill, DOWN), run_time=1.0)
        self.pena(o.lv)
        self.gat("o épsilon")
        self.pena(o.leps)
        self.gat("então a definição diz")
        d1 = TC(r"D\ \text{tem conteúdo nulo}\ \iff", 1120, 270, 40)
        d2 = TC(r"\forall\eps>0\ \ \exists\ \Me{A_1},\dots,\Me{A_n}\ \text{retângulos}:", 1120, 370, 40)
        d3 = TC(r"D\subset \Me{A_1}\cup\Me{A_2}\cup\cdots\cup\Me{A_n}", 1120, 470, 40)
        d4 = TC(r"\text{e}\ \ \sum_{i=1}^{n} m(\Me{A_i})<\eps", 1120, 580, 40)
        self.pena(d1)
        self.gat("se para todo épsilon")
        self.pena(d2)
        self.gat("tais que d está")
        self.pena(d3)
        self.gat("e a soma das áreas é")
        self.pena(d4)
        self.gat("esse u grande")
        self.sublinha(d3[0][4], 1.2)
        lu = leg("∪: UNIÃO   ·   m(Aᵢ): ÁREA DE Aᵢ", 1124, 690, GEO, "left", 24)
        self.gat("e eme de a")
        self.sublinha(VGroup(*d4[0][-7:-2]), 1.2)
        self.pena(lu)
        self.marca("12")

        # ── B3-2 · um orçamento de área (alvo 13) ───────────────────────────────────────────────────
        self.an("B3-2")
        self.play(*[FadeOut(m) for m in (d1, d2, d3, d4, lu, nf, lD, *rot)], run_time=0.4)
        self.remove(d1, d2, d3, d4, lu, nf, lD, *rot)
        oa = leg("ORÇAMENTO DE ÁREA", 1124, 260, MEN, "left", 30)
        self.pena(oa)
        R = [("1", "4", "0{,}46"), (r"\tfrac14", "16", "0{,}12"), (r"0{,}05", "64", "0{,}03")]
        linhas = [TC(r"\eps=" + a + r"\ \ \to\ \ " + b + r"\ \text{retângulos}\ \to\ \Me{" + c + r"\ \text{m}^2}", 1120, 350 + k * 90, 36) for k, (a, b, c) in enumerate(R)]
        self.gat("quatro retângulos em volta")
        self.play(Indicate(cob, color=MEN, scale_factor=1.0), run_time=0.8)
        n0 = len(linhas[0][0])
        self.escreve(linhas[0], voos=[(o.lv, list(range(n0 - 6, n0)))], passo=0.04)
        eps, gasto = 1.0, cob.area
        for k, (e2, n2, fr1, fr2) in enumerate(((0.25, 16, "agora o orçamento cai", "tudo bem dezesseis"), (0.05, 64, "e se cair para", "sessenta e quatro retângulos"))):
            self.gat(fr1)
            # a marca desce até o novo ε (na escala antiga): a cobertura velha estoura
            self.play(Transform(o.marca, o.ret_marca(o.H * e2 / eps)), run_time=0.6)
            self.gat(fr2)
            cob2 = cobertura(n2, fill=0.22 if n2 < 64 else 0.35, wpx=2 if n2 < 64 else 1)
            g2 = cob2.area
            self.play(FadeOut(cob), FadeIn(cob2), Transform(o.fill, o.ret_fill(eps, g2)), FadeOut(o.lv), run_time=0.6)
            self.remove(cob, o.lv)
            cob = cob2
            # a escala se ajusta: a marca volta ao topo
            novo_eps = TC(r"\eps=" + Orc.num(e2), o.X + 23, o.YB - o.H - 30, 26, "c")
            self.play(Transform(o.marca, o.ret_marca(o.H)), Transform(o.fill, o.ret_fill(e2, g2)), FadeOut(o.leps), run_time=0.5)
            self.remove(o.leps)
            o.leps = novo_eps
            o.lv = o.rot_gasto(e2, g2)
            self.pena(o.leps, o.lv, rt=0.6)
            nk = len(linhas[k + 1][0])
            self.escreve(linhas[k + 1], voos=[(o.lv, list(range(nk - 6, nk)))], passo=0.04)
            eps = e2
            if k == 1:
                sold2 = solda_px(CH, BR, 2)
                self.play(ReplacementTransform(sold, sold2), run_time=0.3)
                sold = sold2
        self.gat("mas cuidado")
        e3 = leg("3 EXEMPLOS NÃO SÃO PROVA", 1124, 680, GEO, "left", 26)
        self.pena(e3)
        self.gat("o que a definição pede")
        qq = T("QUALQUER ε POSITIVO DÁ CONTA", 1120, 770, 36)
        self.pena(qq)
        self.marca("13")

        # ── B3-3 · o que tem e o que não tem (alvo 14) ──────────────────────────────────────────────
        self.an("B3-3")
        tudo = [oa, *linhas, e3, qq, cob, sold, bd, o.caixa, o.fill, o.marca, o.leps, o.lg, o.lv]
        self.grade_off(rt=0.4, junto=[FadeOut(m) for m in tudo])
        self.remove(*tudo)
        cards = [(140, 200, "UM PONTO", 1), (1000, 200, "PONTOS EM NÚMERO FINITO", 1), (140, 580, "UM SEGMENTO", 1), (1000, 580, "UM DISCO CHEIO", 0)]
        pns = [painel(X0, Y0, 780, 340) for X0, Y0, _, _ in cards]
        tts = [T(t, X0 + 30, Y0 + 300, 30) for X0, Y0, t, _ in cards]
        mk = [check_px(X0 + 720, Y0 + 290) if ok else cruz_px(X0 + 720, Y0 + 290) for X0, Y0, _, ok in cards]
        sq = lambda cx, cy, s_: ret_px(cx - s_ / 2, cy - s_ / 2, cx + s_ / 2, cy + s_ / 2, fill=MEN22, stroke=MEN, wpx=2, z=4)
        dot = lambda X, Y: ponto_px(X, Y, BR, 6, z=6)
        # um ponto
        self.gat("um ponto tem")
        self.play(FadeIn(pns[0]), run_time=0.4)
        p0 = dot(330, 330)
        self.play(FadeIn(p0, scale=0.5), run_time=0.3)
        self.pena(tts[0])
        self.gat("basta um quadradinho")
        s0 = sq(330, 330, 90)
        self.play(FadeIn(s0), run_time=0.4)
        prev = VGroup(s0, p0)
        for k, s_ in enumerate((56, 30)):
            nv = VGroup(sq(480 + k * 150, 330, s_), dot(480 + k * 150, 330))
            self.play(TransformFromCopy(prev, nv), run_time=0.6)
            prev = nv
        self.play(Create(mk[0]), run_time=0.4)
        # pontos em número finito
        self.gat("um número finito de pontos")
        self.play(FadeIn(pns[1]), run_time=0.4)
        pts = [(1150, 300), (1300, 360), (1420, 280), (1560, 340), (1680, 300)]
        self.play(LaggedStart(*[FadeIn(dot(X, Y), scale=0.5) for X, Y in pts], lag_ratio=0.15), run_time=0.8)
        self.pena(tts[1])
        self.gat("um quadradinho para cada")
        self.play(LaggedStart(*[FadeIn(sq(X, Y, 30)) for X, Y in pts], lag_ratio=0.15), Create(mk[1]), run_time=1.0)
        # segmento
        self.gat("um segmento de reta")
        self.play(FadeIn(pns[2]), run_time=0.4)
        segs = []
        for i, hh in enumerate((34, 18, 8)):
            Y = 680 + i * 40
            segs.append(VGroup(ret_px(260, Y - hh / 2, 760, Y + hh / 2, fill=MEN22, stroke=MEN, wpx=2, z=4), lin_px([(270, Y), (750, Y)], BR, 4, z=6)))
        self.play(Create(segs[0][1]), run_time=0.6)
        self.pena(tts[2])
        self.gat("um retângulo comprido")
        self.play(FadeIn(segs[0][0]), run_time=0.4)
        for i in (1, 2):
            self.play(TransformFromCopy(segs[i - 1], segs[i]), run_time=0.6)
        self.play(Create(mk[2]), run_time=0.4)
        self.gat("e daí saem duas")
        r1 = leg("PEDAÇO DE NULO: NULO", 140, 1010, GEO, "left", 26)
        r2 = leg("UNIÃO FINITA DE NULOS: NULO", 1000, 1010, GEO, "left", 26)
        self.pena(r1)
        self.gat("e juntar um número finito")
        self.pena(r2)
        # disco cheio
        self.gat("agora um disco cheio")
        self.play(FadeIn(pns[3]), run_time=0.4)
        disco = circ_px(1250, 730, 95, mixh(BG_, CI, .55), 0, fill=mixh(BG_, CI, .55), fop=1, z=2)
        self.play(FadeIn(disco), run_time=0.5)
        self.pena(tts[3])
        self.gat("para cobri lo")
        quads = VGroup()
        for i in range(-3, 3):
            for j in range(-3, 3):
                X, Y = 1250 + i * 34, 730 + j * 34
                if math.hypot(max(abs(X + 17 - 1250) - 17, 0), max(abs(Y + 17 - 730) - 17, 0)) < 95:
                    quads.add(ret_px(X, Y, X + 34, Y + 34, fill=MEN, fop=0.18, stroke=MEN, wpx=1.5, z=4))
        self.play(LaggedStart(*[FadeIn(q_) for q_ in quads], lag_ratio=0.03), run_time=1.2)
        self.gat("e um orçamento menor")
        bar_ok = ret_px(1500, 640, 1546, 840, fill=MEN, z=4)
        mark = ret_px(1490, 638, 1556, 642, fill=BR, z=6)
        le = leg("ε", 1560, 650, MEN, "left", 26)
        self.play(FadeIn(mark), run_time=0.3)
        self.pena(le)
        bar_v = ret_px(1500, 596, 1546, 640, fill=AL, z=4)
        self.play(GrowFromEdge(bar_ok, DOWN), run_time=0.8)
        self.play(GrowFromEdge(bar_v, DOWN), run_time=0.4)
        es = leg("ESTOURA", 1600, 610, AL, "left", 22)
        self.pena(es)
        self.play(Create(mk[3]), run_time=0.4)
        self.gat("então a ideia não é")
        self.pulso(mk[3], 1.4, 0.8)
        self.gat("é dar para cobri")
        for k in (0, 1, 2):
            self.pulso(mk[k], 1.4, 0.5)
        self.marca("14")
        self.sai_fim()

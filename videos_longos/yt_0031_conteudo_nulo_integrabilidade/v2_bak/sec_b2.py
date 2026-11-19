"""yt_0031 · B2 · a chapa de dois metais (alvos 08 a 11). 3D: b21 (n = 16, muro de tampas na solda)."""
from v31 import *

TAB = {4: (5, "6{,}00", "8{,}50", "2{,}50", 6.0, 8.5), 8: (11, "6{,}38", "7{,}75", "1{,}38", 6.375, 7.75),
       16: (24, "6{,}66", "7{,}41", "0{,}75", 6.6562, 7.4062), 32: (47, "6{,}88", "7{,}25", "0{,}37", 6.8828, 7.25),
       64: (95, "6{,}97", "7{,}15", "0{,}19", 6.9668, 7.1523)}


def regua(Y, X0=1120, k=52):
    """régua da massa (0–12 kg) do sb31: eixo, seta, marcas, kg."""
    g = VGroup(lin_px([(X0, Y), (X0 + 12 * k + 24, Y)], GEO, 3),
               poly_px([(X0 + 12 * k + 34, Y), (X0 + 12 * k + 18, Y - 8), (X0 + 12 * k + 18, Y + 8)], GEO, z=4))
    for t in range(0, 13, 2):
        g.add(lin_px([(X0 + t * k, Y - 7), (X0 + t * k, Y + 7)], GEO, 3))
    nums = [leg(str(t), X0 + t * k, Y + 38, GEO, "center", 24) for t in range(0, 13, 2)] + [leg("kg", X0 + 12 * k + 40, Y + 36, GEO, "left", 22)]
    return g, nums


def faixa_regua(Y, a, b, X0=1120, k=52):
    return VGroup(ret_px(X0 + a * k, Y - 13, X0 + b * k, Y + 13, fill=mixh(BG_, GEO, 0.22), z=4),
                  ret_px(X0 + a * k - 3, Y - 18, X0 + a * k + 3, Y + 18, fill=AZC, z=5),
                  ret_px(X0 + b * k - 3, Y - 18, X0 + b * k + 3, Y + 18, fill=CORAL, z=5))


class PB2(B31):
    ANTES = "A CHAPA DE DOIS METAIS"          # v2 (G2): a linha 2 do canto já está na tela no 1º quadro do bloco

    def corpo(self):
        # ── B2-1 · onde estão as tampas? (alvos 08 e 09) ────────────────────────────────────────────
        self.an("B2-1")
        self.grade_on(rt=0)               # v2 (G2): a grade entra junto da figura, sem quadro vazio
        liso = img_chapa(arr_metais_liso())
        bd = borda_ch(CH, GEO, 3)
        sold = solda_px(CH, BR, 4)
        sx, sy, lx, ly = eixos_chapa()
        self.play(FadeIn(liso), Create(bd), FadeIn(sx), FadeIn(sy), run_time=0.5)
        self.play(Create(sold), run_time=1.0, rate_func=linear)
        self.pena(lx, ly)
        self.gat("embaixo da solda um")
        r1 = TP(r"\rr=1", *CH.px(1.75, .25), 30)
        c1 = TC(r"\text{leve: }\rr=1\ \text{kg/m}^2", 1120, 260, 40)
        self.pena(r1)
        self.pena(c1)
        self.gat("em cima três é")
        r3 = TP(r"\rr=3", *CH.px(.25, 1.75), 30)
        c2 = TC(r"\text{pesado: }\rr=3\ \text{kg/m}^2", 1120, 340, 40)
        self.pena(r3)
        self.pena(c2)
        self.gat("é mais ou menos")
        c3 = leg("≈ ALUMÍNIO E AÇO, MESMA ESPESSURA", 1124, 400, GEO, "left", 24)
        self.pena(c3)
        self.gat("coloca uma grade")
        cel4 = img_chapa(arr_metais(4, verm=False))
        g4 = VGroup(*[lin_px([CH.px(a, 0), CH.px(a, 2)], BG_, 3, z=3) for a in (.5, 1, 1.5)],
                    *[lin_px([CH.px(0, b), CH.px(2, b)], BG_, 3, z=3) for b in (.5, 1, 1.5)])
        self.play(FadeIn(cel4), LaggedStart(*[Create(l) for l in g4], lag_ratio=0.12), run_time=1.0)
        self.remove(liso)
        self.gat("numa célula inteira")
        k0 = ret_px(*CH.px(1.5, .5), *CH.px(2, 0), stroke=BR, wpx=4, z=9)
        self.play(Create(k0), run_time=0.5)
        t0 = leg("TAMPA 0", *CH.px(1.75, .43), BR, "center", 24)        # v2: dentro da célula inteira no metal leve
        l0 = leg("NUM METAL SÓ", 1124, 500, GEO, "left", 26)
        self.gat("o piso é um")
        self.pena(l0)
        f0 = TC(r"\mij=\Mij\ \Rightarrow\ \text{tampa }0", 1120, 555, 38)
        self.pena(f0)
        self.gat("e a tampa tem altura zero")
        self.pena(t0)
        self.gat("mas nas células atravessadas")
        verm = VGroup(*[ret_px(*CH.px(i * .5, j * .5 + .5), *CH.px(i * .5 + .5, j * .5), fill=mixh(BG_, AL, .75), z=2) for i, j in sorted(celulas_verm(4))])
        self.play(LaggedStart(*[FadeIn(c) for c in verm], lag_ratio=0.2), run_time=1.2)
        k2 = ret_px(*CH.px(1, 1.5), *CH.px(1.5, 1), stroke=BR, wpx=4, z=9)
        self.play(Create(k2), run_time=0.5)
        l2 = leg("NA SOLDA", 1124, 650, AL, "left", 26)
        self.pena(l2)
        self.gat("o piso é um e")
        f2 = TC(r"\mij=\Az1,\ \ \Mij=\Co3\ \Rightarrow\ \text{tampa }2", 1120, 705, 38)
        self.pena(f2)
        self.gat("tampa de altura dois")
        t2 = leg("TAMPA 2", *CH.px(1.25, 1.06), BR, "center", 24)
        l5 = leg("5 CÉLULAS CRUZAM A SOLDA", 1124, 800, AL, "left", 26)
        self.pena(t2)
        self.pena(l5)
        self.marca("08", agora=True)
        self.gat("e juntas essas tampas")
        col = [r1, r3, c1, c2, c3, k0, k2, t0, l0, f0, l2, f2, t2, l5]
        self.play(*[FadeOut(m) for m in col], run_time=0.4)
        self.remove(*col)
        # o 2D vira 3D (pouso de entrada; a vista de cima do b21 tem a grade 16 × 16 por baixo da chapa 2D)
        pal = Palco3D("b21", self, CAM_BAIXO, n=16, cresce=0.0, muro=0.0)
        entra3d(self, pal, saem=[cel4, verm, g4, bd, sold, sx, sy, lx, ly], rt_cam=1.8)
        e3x = pal.prende(TC(r"\X", 0, 0, 30, "c"), "ex")
        e3z = pal.prende(TC(r"\Ci{z}", 0, 0, 30, "c"), "ez")
        m1 = pal.prende(TC(r"\Ci1", 0, 0, 24, "c"), "m1", dx=-14)
        m3 = pal.prende(TC(r"\Ci3", 0, 0, 24, "c"), "m3", dx=-14)
        mu = leg("MURO DE TAMPAS", 640, 165, CORAL, "center", 28)
        fio = lin_px([(640, 178), (640, 300)], CORAL, 2, z=12)
        rl = pal.prende(TP(r"\rr=1", 0, 0, 28), "leve")
        rp = TP(r"\rr=3", 820, 250, 28)
        q = leg("16 × 16 · 24 CÉLULAS NA SOLDA", 1124, 260, GEO, "left", 26)
        self.pena(e3x, e3z, m1, m3, rl, extra=pal.anim(0.9, cresce=1.0), rt=0.9)
        self.pena(mu, rp, q, extra=[Create(fio), *pal.anim(1.0, muro=1.0)], rt=1.0)

        # ── B2-2 · o muro vai sumindo (alvos 09 e 10) ──────────────────────────────────────────────
        self.an("B2-2")
        self.gat("é o salto dois")
        alt = TC(r"\text{altura de cada tampa}=\Co{3-1}=\Co2", 1120, 350, 38)
        mx, my = pal.pt("muro")
        cota = VGroup(lin_px([(mx + 26, my), (mx + 26, my + 78)], CORAL, 3, z=12))
        self.play(Create(cota), run_time=0.3)
        n_alt = len(alt[0])
        assert n_alt == 23, n_alt
        # v2: o 3 e o 1 voam dos rótulos ρ = 3 e ρ = 1; o 2 voa do muro (a cota da tampa)
        self.escreve(alt, voos=[(rp.f[0][-1], [18]), (rl.f[0][-1], [20]), (cota, [22])], rt_voo=0.7, atraso_caneta=0.0, passo=0.03)
        self.play(FadeOut(cota), run_time=0.3)
        self.remove(cota)
        self.gat("vezes a área das células")
        dsp = TC(r"\SP-\sP=\Co2\cdot(\text{área das células na solda})", 1120, 460, 34)
        fz = leg("FORA DA SOLDA: TAMPA ZERO", 1124, 560, GEO, "left", 26)
        self.pena(dsp, fz, lag=0.6, passo=0.03)
        self.marca("09", agora=True, dt=0.3)
        sai = [e3x, e3z, m1, m3, mu, fio, rl, rp, q, alt, dsp, fz]
        for m in sai:
            m.clear_updaters()
        self.play(*[FadeOut(m) for m in sai], run_time=0.4)
        self.remove(*sai)
        im = img_chapa(arr_metais(4, alphaV=.85))
        gr = grade_ch(4, CH, mixh(BG_, GEO, .35), 1)
        bd = borda_ch(CH, GEO, 3)
        sold = solda_px(CH, BR, 2)
        sai3d(self, pal, entram=[im, gr, bd, sold], rt_cam=0.8, rt_x=0.35, junto_cam=pal.anim(0.8, muro=0.0, cresce=0.0))
        # tabela
        cx = [1130, 1260, 1420, 1580, 1750]
        cab = [leg(h, cx[i], 250, [GEO, AL, AZC, CORAL, BR][i], "left", 22) for i, h in enumerate(["n", "CÉLULAS", "POR BAIXO", "POR CIMA", "DIFERENÇA"])]
        topo = leg("4 × 4 · 5 CÉLULAS NA SOLDA", 600, 262, AL, "center", 24)
        rg, rgn = regua(760)
        self.pena(*cab, topo, *rgn, extra=[Create(rg)], rt=1.2)
        fx = None
        n_ant, frases = 4, {4: "com quatro divisões", 8: "com oito divisões", 16: "com dezesseis", 32: "com trinta e duas", 64: "com sessenta e quatro"}
        linhas = []
        for k, n in enumerate((4, 8, 16, 32, 64)):
            self.gat(frases[n])
            if n > 4:
                im2 = img_chapa(arr_metais(n, alphaV=.85))
                topo2 = leg(f"{n} × {n} · {TAB[n][0]} CÉLULAS NA SOLDA", 600, 262, AL, "center", 24)
                self.play(FadeOut(topo), run_time=0.15)
                self.remove(topo)
                anims = [FadeIn(im2)]
                if n <= 32:
                    g2 = grade_ch(n, CH, mixh(BG_, GEO, .35), 1)
                    novas = VGroup(*[l for j, l in enumerate(g2) if (j // 2 + 1) % 2 == 1])
                    velhas = VGroup(*[l for j, l in enumerate(g2) if (j // 2 + 1) % 2 == 0])
                    self.remove(gr)
                    self.add(velhas)
                    anims.append(LaggedStart(*[GrowFromCenter(l) for l in novas], lag_ratio=0.004))
                else:
                    anims.append(FadeOut(gr))
                    g2 = None
                fx2 = faixa_regua(760, TAB[n][4], TAB[n][5])
                anims.append(Transform(fx, fx2))
            Y = 312 + k * 56
            ln = [TC(str(n), cx[0], Y, 32), TC(r"\Al{%d}" % TAB[n][0], cx[1] + 30, Y, 32), TC(r"\Az{%s}" % TAB[n][1], cx[2], Y, 32),
                  TC(r"\Co{%s}" % TAB[n][2], cx[3], Y, 32), TC(TAB[n][3], cx[4], Y, 32)]
            if n == 4:
                fx = faixa_regua(760, TAB[4][4], TAB[4][5])
                self.pena(ln[0], extra=[FadeIn(fx)], rt=0.5)
                for fr, m in (("cinco células cruzam", ln[1]), ("seis quilos", ln[2]), ("oito e meio", ln[3]), ("diferença de dois e meio", ln[4])):
                    self.gat(fr)
                    self.pena(m, rt=0.5)
            else:
                # v2: no número que a voz diz, a linha da tabela, a grade que refina e a faixa da régua que aperta, juntas
                self.pena(topo2, *ln, extra=anims, rt=1.0)
                self.remove(im)
                if g2 is not None:
                    self.remove(velhas, novas)
                    self.add(g2)
                else:
                    self.remove(gr)
                im, gr, topo = im2, g2, topo2
            linhas.append(ln)
            if n == 8:
                db = leg("DOBROU n → DIFERENÇA ÷ 2", 1124, 620, GEO, "left", 26)
                self.pena(db)
        box = caixa_px(1112, 312 + 4 * 56 - 26, 780, 52, GEO, 2, 0.5, 8)
        self.play(Create(box), run_time=0.5)
        self.gat("as duas somas apertam")
        pm = ponto_px(1120 + 7.06 * 52, 760, BR, 9, z=8)
        lm = leg("≈ 7,06", 1120 + 7.06 * 52, 734, BR, "center", 24)
        self.play(FadeIn(pm, scale=0.5), run_time=0.3)
        self.pena(lm)
        self.gat("e repara o salto")
        sm = leg("O SALTO NÃO MUDA; A ÁREA DIMINUI", 1124, 880, CORAL, "left", 26)
        self.pena(sm)
        self.marca("10")

        # ── B2-3 · a pergunta certa (alvo 11) ───────────────────────────────────────────────────────
        self.an("B2-3")
        tudo = [m for L_ in linhas for m in L_] + cab + [topo, box, db, pm, lm, sm, fx, rg, *rgn]
        bd2 = borda_ch(CH, mixh(BG_, GEO, .6), 2)
        sold2 = solda_px(CH, BR, 5)
        sx, sy, lx, ly = eixos_chapa()
        self.play(*[FadeOut(m) for m in tudo + [im, bd]], FadeIn(bd2), ReplacementTransform(sold, sold2), FadeIn(sx), FadeIn(sy), run_time=1.0)
        self.remove(*tudo, im, bd)
        self.pena(lx, ly)
        self.gat("o problema não era")
        oc = leg("O CONJUNTO ONDE f SALTA", *CH.px(1, 2.12), BR, "center", 26)
        self.pena(oc)
        self.gat("se a região problemática")
        a1 = T("A SOLDA CABE", 1120, 420, 58)
        a2 = T("EM ÁREA PEQUENA?", 1120, 500, 58, cor=MEN)
        self.pena(a1)
        self.pena(a2)
        self.gat("tão pequena quanto")
        b1 = leg("RETÂNGULOS COM ÁREA TOTAL", 1124, 600, GEO, "left", 28)
        b2 = leg("TÃO PEQUENA QUANTO SE QUEIRA", 1124, 644, GEO, "left", 28)
        self.pena(b1, b2, lag=0.6)
        self.marca("11")
        self.sai_fim()

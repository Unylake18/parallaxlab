"""yt_0032 · B3 · a solda não pesa (alvos 10 v2, 11 v2, 12 v2). 3D: b31 (muro de altura M, n = 16) que segue no b32 (muro de 100, n = 64 → 1024)
na mesma cena (o estado muda: n e a altura desenhada). v2: |∬_B f| ≤ M·área (D3), M e ρ = 100 presos ao topo do muro, inset de vista de cima
que afina junto com o muro (R4), f LIMITADA em Space Grotesk (T3); B3-3: massa do cordão com fórmula-mãe e mapa M9 (D4)."""
from lib32 import *

VI = Vw(1130, 1000, 135)          # inset: vista de cima (canto inferior direito da coluna)


def celulas_inset(n):
    h = 2 / n
    g = VGroup()
    for i, j in sorted(celulas_verm(n)):
        g.add(ret_px(*VI.px(i * h, (j + 1) * h), *VI.px((i + 1) * h, j * h), fill=CORAL, z=3))
    return g


class PB3(B32):
    ANTES = "SINAL E COMPARAÇÃO"

    def corpo(self):
        # ── B3-1 · uma linha pode ter massa? (alvo 10 v2) ──
        self.an("B3-1")
        self.secao("A SOLDA NÃO PESA")
        pal = Palco3D(self, "b31", CAM_BAIXO, n=16, cob=0.0, muro=0.0, alt=1.5, lz=1.95, marca=0.0)
        pal.fundo.op.set_value(0.0)
        self.add(pal.fundo)
        self.play(pal.fundo.op.animate.set_value(1.0), run_time=0.9)
        self.gat("começa pela solda matemática")            # C12 (final): a solda se chama S
        lS = pal.prende(TP(r"\Me{S}", 0, 0, 34), "solda", -30, -26)
        self.pena(lS)
        self.gat("uma curva sem espessura")
        sm = leg("SOLDA MATEMÁTICA: SÓ UMA CURVA", 1120, 660, GEO, "left", 26)
        self.pena(sm)
        self.gat("dá para cobri la")
        self.play(*pal.anim(1.4, cob=1.0), run_time=1.4)
        self.gat("existe um número eme")
        pal.set(marca=1.0)
        f1 = TC(r"|\f|\le M", 1120, 390, 40)
        self.pena(f1)
        lim = leg("f LIMITADA", 1330, 398, GEO, "left", 26)               # T3: com respiro, em Space Grotesk
        self.pena(lim)
        self.gat("a contribuição das células")
        self.play(*pal.anim(2.2, muro=1.0), run_time=2.2)
        lM = pal.prende(TP(r"M", 0, 0, 32), "muro", 0, -34)                 # R4: M preso no TOPO do muro
        self.pena(lM)
        self.gat("fica limitada por eme")
        f2 = TC(r"\left|\iint_S\f\right|\le M\cdot\Me{\text{área da cobertura}}", 1120, 500, 40)   # D3: com integrando e módulo
        self.pena(f2)
        self.gat("a altura pode ser")
        l3 = leg("ALTO, MAS CADA VEZ MAIS FINO", 1120, 585, CORAL, "left", 26)
        self.pena(l3)
        self.gat("essa é a quarta")
        f0 = mista([("m", r"\Me{S}"), ("t", "TEM CONTEÚDO NULO"), ("m", r"\Rightarrow\ \iint_S\f=0")], 1120, 280, 34)
        self.pena(f0)
        self.gat("mas fica tão fino")
        pal.set(n=32)                                    # a grade refina uma vez: o muro já afina (a cobertura encolhe)
        self.play(*pal.anim(0.8, muro=1.0), run_time=0.8)
        self.marca("10")

        # ── B3-2 · um muro de cem (alvo 11 v2) ──
        self.an("B3-2")
        self.some(f0, f1, f2, lim, l3, sm, lS, rt=0.4)
        self.gat("densidade de cem quilos")
        self.some(lM, rt=0.25)
        self.play(*pal.anim(2.0, alt=2.0, lz=2.35), run_time=2.0)
        l100 = pal.prende(TP(r"\rr=100", 0, 0, 32), "muro", 0, -34)        # R4: ρ = 100 no topo do muro
        esc = leg("ESCALA VERTICAL REDUZIDA", 420, 1010, GEO, "left", 26)
        self.pena(l100, esc, lag=0.3)
        self.gat("o muro coral fica")
        tit = T("COTA SUPERIOR", 1120, 230, 32, "left", CORAL)
        fcota = TC(r"\text{cota}=100\cdot\text{área}", 1120, 282, 36)          # C4 (final): a regra antes do número
        self.pena(tit, fcota, lag=0.5)                                                 # sync: título e regra quase juntos
        cab = VGroup(*[leg(c, 1140 + j * 230, 340, GEO, "left", 26) for j, c in enumerate(("n", "ÁREA (m²)", "COTA (kg)"))])
        self.pena(cab)
        linhas = [("64", "0,093", "9,3"), ("128", "0,046", "4,6"), ("256", "0,023", "2,3"), ("512", "0,011", "1,2"), ("1024", "0,006", "0,6")]
        gats = ["com sessenta e quatro", "dobra a resolução", "depois dois vírgula três", "depois um vírgula dois", "e continuando seis décimos"]
        cel = None
        for i, ((n, a, c), gg) in enumerate(zip(linhas, gats)):
            self.gat(gg)
            pal.set(n=int(n))
            novas = celulas_inset(int(n))
            lv = leg(f"VISTA DE CIMA, n = {n}", 1130, 712, GEO, "left", 26)
            if cel is None:                              # o inset nasce no primeiro passo
                il, ip = metais_liso(VI, z=2)
                ib = borda_ch(VI, GEO, 2, z=5)
                self.play(FadeIn(il), FadeIn(ip), Create(ib), FadeIn(novas), run_time=0.8)
                self.pena(lv)
                vleg = lv
            else:                                        # a grade nova nasce da velha: as células afinam junto com o muro
                ja_escrita(lv)                           # contador que muda (n), não fórmula nova: transforma do anterior
                self.play(ReplacementTransform(cel, novas), ReplacementTransform(vleg, lv), run_time=0.8)
                vleg = lv
            cel = novas
            Yr = 340 + (i + 1) * 54
            row = VGroup(T(n, 1140, Yr, 30), T(a, 1370, Yr, 30), T(c, 1600, Yr, 30, "left", CORAL))
            if i == 0:                                   # C4: n e área primeiro; a cota sai da conta 100 · 0,093 (mapa 14)
                self.pena(VGroup(row[0], row[1]), passo=0.045)
                self.gat("chega a nove vírgula")
                K0 = L([("c", "100"), ("d", r"\cdot"), ("a", r"0{,}093")], 1700, Yr - 11, 30)
                self.escreve(K0, voos=[(VGroup(*l100.f[0][2:5]), K0._ix["c"]), (VGroup(*row[1][0]), K0._ix["a"])], atraso_caneta=0.2)
                K1 = L([("r", r"\Co{9{,}3}")], 1700, Yr - 11, 30)
                gm(self, K0, K1, [(["c", "d", "a"], "r")], rt=1.1, nota="mapa 14 (C4, B3-2: 100 · 0,093 = 9,3)")
                self.play(ReplacementTransform(K1, row[2]), run_time=0.7)          # o 9,3 desce para a célula COTA
                ja_escrita(row[2])
            else:
                self.pena(row, passo=0.045)
            if i == 0:
                self.gat("atenção é uma cota")
                cn = leg("COTA, NÃO MASSA", 1420, 230, CORAL, "left", 26)   # R4: ao lado do título da tabela
                self.pena(cn)
        self.gat("a altura continua cem")
        c_ = pal.cam()                                    # palco: a cota da altura do muro (a altura fica)
        xb, yb = proj3d(c_, (1.159, float(g_solda(1.159)), 0.0))
        xt, yt = proj3d(c_, (1.159, float(g_solda(1.159)), 2.0))
        cota_h = VGroup(seta_px((xb - 46, (yb + yt) / 2), (xt - 46, yt + 4), GEO, 3, 16), seta_px((xb - 46, (yb + yt) / 2), (xb - 46, yb - 4), GEO, 3, 16))
        self.play(GrowFromCenter(cota_h), run_time=0.9)
        lf1 = leg("A ALTURA FICA;", 1450, 820, GEO, "left", 28)
        lf2 = leg("A LARGURA SOME", 1450, 862, GEO, "left", 28)
        self.pena(lf1, lf2, lag=0.4)
        self.gat("refinando sempre a cota")
        z0 = TC(r"\to 0", 1450, 930, 40)
        self.pena(z0)
        self.gat("então a solda matemática")
        na = leg("A SOLDA NÃO ACRESCENTA MASSA", 1120, 672, MEN, "left", 26)
        self.pena(na)
        self.gat("e contar zero duas")
        zz = TC(r"0+0=0", 1580, 930, 36)
        self.pena(zz)
        self.marca("11")

        # ── B3-3 · mas uma solda real pesa (alvo 12 v2) ──
        self.an("B3-3")
        self.limpa(rt=0.5)
        self.grade_on(CH, rt=0.4)
        leve, pes = metais_liso(CH)
        bord = borda_ch(CH, GEO, 2)
        cord = cordao_ch(CH, 6)
        sx, sy, lx, ly = eixos_chapa(CH)
        self.play(FadeIn(leve), FadeIn(pes), FadeIn(bord), GrowFromPoint(sx, CH.P(0, 0)), GrowFromPoint(sy, CH.P(0, 0)), run_time=0.9)
        self.pena(lx, ly)
        self.play(deposita(cord, 1.6), run_time=1.6)
        self.gat("uma solda de verdade")
        cx = lin_px([CH.px(.8, 1.65), CH.px(1.4, 1.65), CH.px(1.4, 1.05), CH.px(.8, 1.05), CH.px(.8, 1.65)], BR, 2, dash=(8, 6), z=9)
        pn = painel(1100, 170, 700, 300)
        pn.set_z_index(2)
        lz1 = lin_px([CH.px(1.4, 1.65), (1100, 184)], GEO, 1.5, alpha=0.45, z=1)
        lz2 = lin_px([CH.px(1.4, 1.05), (1100, 456)], GEO, 1.5, alpha=0.45, z=1)
        self.play(Create(cx), run_time=0.6)
        self.play(Create(lz1), Create(lz2), Create(pn), run_time=0.8)
        pts = [(1150 + 600 * k / 40, 350 - 70 * math.sin(PI * k / 40)) for k in range(41)]
        zc = Cordao(pts, 28, z=8)
        meio = lin_px(pts, BR, 2, dash=(6, 5), z=12)
        ttl = T("CORDÃO DE 1 cm (ZOOM)", 1450, 220, 26, "center")
        self.play(deposita(zc, 2.0), run_time=2.0)
        self.play(Create(meio), run_time=0.6)
        self.pena(ttl)
        # cota da largura do cordão (fonte do 0,01)
        cota = VGroup(lin_px([(1770, 336), (1770, 364)], GEO, 2, z=9), lin_px([(1762, 336), (1778, 336)], GEO, 2, z=9),
                      lin_px([(1762, 364), (1778, 364)], GEO, 2, z=9))
        lcota = TP(r"0{,}01\ \text{m}", 1700, 300, 26)
        self.gat("vamos representá lo como")
        M0 = L([("m", "m"), ("ap", r"\approx"), ("r", r"\rr"), ("d1", r"\cdot"), ("L", "L"), ("d2", r"\cdot"), ("w", r"\text{largura}")], 1120, 540, 40)
        self.pena(M0)                                     # D4: a fórmula-mãe antes do número
        self.play(Create(cota), run_time=0.4)
        self.pena(lcota)
        self.gat("com seis quilos por")
        src = L([("r", "6"), ("u", r"\ \text{kg/m}^2")], 1450, 440, 30, "c")      # a densidade do cordão (fica no zoom)
        self.pena(src)
        self.gat("a linha da solda")                      # C5 (final): a solda inteira é percorrida em laranja; L fica sobre ela
        perc = solda_px(CH, POS, 5, z=9)
        self.play(Create(perc), run_time=1.2, rate_func=linear)
        lL = TP(r"\Lr{L\approx 2{,}25\ \text{m}}", *CH.px(1.16, 1.86), 30)
        self.pena(lL)
        self.play(FadeOut(perc), run_time=0.4)
        self.remove(perc)
        self.gat("com um centímetro de")
        V1 = L([("ap", r"\approx"), ("v6", "6"), ("d1", r"\cdot"), ("vL", r"2{,}25"), ("d2", r"\cdot"), ("vw", r"0{,}01")], 1120, 615, 40)
        self.escreve(V1, voos=[(gl(src, "r"), V1._ix["v6"]), (VGroup(*lL.f[0][2:6]), V1._ix["vL"]), (VGroup(*lcota.f[0][:4]), V1._ix["vw"])], atraso_caneta=0.5)
        V2 = L([("ap", r"\approx"), ("v6", "6"), ("d1", r"\cdot"), ("vL", r"2{,}25"), ("d2", r"\cdot"), ("vw", r"0{,}01"), ("ap2", r"\approx"),
                ("res", r"\Ci{0{,}135}"), ("kg", r"\ \text{kg}")], 1120, 615, 40)
        gm(self, V1, V2, [(k, k) for k in ("ap", "v6", "d1", "vL", "d2", "vw")] + [(["v6", "d1", "vL", "d2", "vw"], "res")], rt=1.4, copia=True,
           nota="mapa 9a (B3-3: ρ·L·largura → 0,135 kg)")
        self.remove(V1)
        C3 = L([("a", r"0{,}01"), ("ar", r"\to"), ("b", r"0{,}001"), ("c", r":\ \ "), ("g1", r"\Ci{135}"), ("u1", r"\ \text{g}"), ("t1", r"\to"),
                ("g2", r"\Ci{13{,}5}"), ("u2", r"\ \text{g}"), ("t2", r"\to"), ("z", "0")], 1120, 705, 38, caneta=False)
        p135 = ja_escrita(parte(C3, C3._ix["g1"] + C3._ix["u1"], "135 g"))
        self.play(TransformFromCopy(gl(V2, "res", "kg"), p135, path_arc=-0.5), run_time=1.0)    # mapa 9b: 0,135 kg = 135 g
        GM_LOG.append((self.lote, self._aid, round(self.t, 2), V2._tex, C3._tex + " [135 g]"))
        print(f"[gm] {self.lote} {self._aid} {self.t:.2f} mapa 9b (B3-3: 0,135 kg → 135 g)")
        self.gat("com um milímetro uns")
        ttl2 = T("CORDÃO DE 1 mm (ZOOM)", 1450, 220, 26, "center")
        pa_ = ja_escrita(parte(C3, C3._ix["a"], "0,01"))
        lcota_mm = TP(r"0{,}001\ \text{m}", 1700, 300, 26)        # a cota do zoom acompanha o cordão de 1 mm
        self.play(Transform(zc, Cordao(pts, 2.8, z=8)), FadeOut(ttl), TransformFromCopy(gl(V2, "vw"), pa_, path_arc=-0.5),
                  Transform(lcota, lcota_mm), run_time=1.1)   # sync: afina e o 0,01 voa juntos
        self.remove(ttl)
        self.pena(ttl2, parte(C3, C3._ix["ar"] + C3._ix["b"] + C3._ix["c"], "→ 0,001"),
                  parte(C3, C3._ix["t1"] + C3._ix["g2"] + C3._ix["u2"], "→ 13,5 g"), lag=0.35)       # C19: → 13,5 g                   # C19 (final): 6 · 2,25 · 0,001 = 0,0135 kg = 13,5 g
        GM_LOG.append((self.lote, self._aid, round(self.t, 2), "0,01 → 0,001", "13,5 g"))
        print(f"[gm] {self.lote} {self._aid} {self.t:.2f} mapa 9c (B3-3/C19: 0,01 → 0,001 ⇒ 13,5 g)")
        self.gat("e conforme a largura")
        self.play(Transform(zc, Cordao(pts, 1.2, z=8, corpo=BR, borda=BR, escama=BR)), FadeOut(meio), FadeOut(cota), FadeOut(lcota), run_time=1.4)
        self.remove(meio, cota, lcota)
        self.pena(parte(C3, C3._ix["t2"] + C3._ix["z"], "→ 0"))
        self.gat("uma massa realmente concentrada")
        mq = leg("E UMA MASSA SÓ NA LINHA?", 1120, 770, GEO, "left", 26)
        self.pena(mq)
        self.gat("aí usamos uma densidade")
        lk = leg("kg/m (MASSA NUMA LINHA) → INTEGRAL DE LINHA", 1120, 815, MEN, "left", 26)
        lin_m = solda_px(CH, MEN, 7, z=9)                 # palco: a massa concentrada NA linha (densidade linear) acende sobre a solda
        self.pena(lk, extra=[Create(lin_m, rate_func=linear)])
        self.gat("é uma descrição diferente")
        self.play(FadeOut(lin_m), run_time=0.8)           # não é o modelo da integral dupla: a linha volta a não pesar
        self.remove(lin_m)
        self.marca("12")
        self.sai_fim()

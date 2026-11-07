"""Lote PE2 (v2): E2 — a corrente da bicicleta (2,5D, vista lateral, aço). Coroa r₁ = 10 cm (40 dentes), catraca r₂ = 4 cm (16 dentes), roda R = 35 cm,
na proporção real entre os três (K = 0,06 cena/cm). Cinemática exata: ω₂ = 2,5 ω₁ a cada quadro; os elos andam com v_c = ω₁ r₁ ao longo do laço
(mesmo passo dos dentes nas duas engrenagens: 2π r₁/40 = 2π r₂/16), sem escorregar (auditoria CORRENTE); o chão corre sob o pneu com ω₂R (sem
escorregar). Pedal a 60 rpm (1 volta/s) desenhado em CÂMERA LENTA ×4 (marcador de canto). E2-4: cadência 60 → 90 rpm em 4 s (uniforme); contador
do pedal termina em 5,00 voltas. E2-3 e E2-5: insets de zoom ×3 na coroa e na catraca (elo, seta violeta v e, no E2-5, a seta verde a_c na razão
1 : 2,5). Álgebra do v2: nenhuma linha de equação da CONTA por FadeIn de linha inteira (escrita em ordem, voos do desenho, passo/TransformByGlyphMap)."""
from pecas20 import *  # noqa: F401,F403

KCM = 0.06
R1, R2, RR = 10 * KCM, 4 * KCM, 35 * KCM
C1, C2 = P3(-5.9, -0.95), P3(-2.45, -0.8)
LENTA = 4.0
NZ1, NZ2 = 40, 16
PASSO = 2 * PI * R1 / NZ1
L_PED = 0.74                          # pedivela (desenho)
Y_CHAO = C2[1] - RR
Y_MARC = -3.32
ZI = 3.0                              # zoom dos insets
RI = 0.72                             # raio dos insets
CI1, CI2 = P3(-6.32, 1.62), P3(-0.85, 1.65)
TH1, TH2 = 150 * DEGREES, 30 * DEGREES        # elo ampliado: ângulo na coroa / na catraca (dentro do trecho em que a corrente abraça cada uma)
P_1, P_2 = C1 + R1 * P3(math.cos(TH1), math.sin(TH1)), C2 + R2 * P3(math.cos(TH2), math.sin(TH2))
LV_I, LC1_I = 0.55, 0.22              # setas dos insets: v (as duas) e a_c da coroa; a_c da catraca = 2,5 × LC1_I
SW1 = 0.6                             # varredura (rad) da seta curva ω₁ a 60 rpm; a da roda é 2,5 × (mesma escala: ângulo ∝ ω)


def laco():
    """Laço da corrente: trechos (reta de cima, arco da coroa, reta de baixo, arco da catraca), no sentido do movimento com ω > 0 (anti-horário)."""
    dv = C2 - C1
    dd = np.linalg.norm(dv)
    e = dv / dd
    n = P3(-e[1], e[0])
    sb = (R1 - R2) / dd
    cb = math.sqrt(1 - sb * sb)
    mu, ml = sb * e + cb * n, sb * e - cb * n
    p1u, p2u, p1l, p2l = C1 + R1 * mu, C2 + R2 * mu, C1 + R1 * ml, C2 + R2 * ml
    au, al = math.atan2(mu[1], mu[0]), math.atan2(ml[1], ml[0])
    da1 = (al - au) % (2 * PI)
    da2 = (au - al) % (2 * PI)
    seg = [("reta", p2u, p1u), ("arco", C1, R1, au, da1), ("reta", p1l, p2l), ("arco", C2, R2, al, da2)]
    L = [np.linalg.norm(p1u - p2u), R1 * da1, np.linalg.norm(p2l - p1l), R2 * da2]
    return seg, L


SEG, LS = laco()
LT = sum(LS)
NEL = round(LT / PASSO)


def pos_laco(s):
    s = s % LT
    for sg, L in zip(SEG, LS):
        if s <= L:
            if sg[0] == "reta":
                a, b = sg[1], sg[2]
                return a + (b - a) * s / L, (b - a) / L, None
            c, r, a0, da = sg[1:]
            a = a0 + s / r
            return c + r * P3(math.cos(a), math.sin(a)), P3(-math.sin(a), math.cos(a)), c
        s -= L
    return SEG[0][1], (SEG[0][2] - SEG[0][1]) / LS[0], None


def _seg(a, b):
    """Segmento reto como uma curva cúbica (sem criar um Line: as camadas vivas fazem centenas por quadro)."""
    a, b = np.asarray(a, float), np.asarray(b, float)
    return np.array([a, a + (b - a) / 3, a + 2 * (b - a) / 3, b])


# ── desenho 2,5D ────────────────────────────────────────────────────────────────────────────────────────────
def dentes(c, r, ang, n, h_out=0.045, h_in=0.032):
    """Contorno de engrenagem com dentes trapezoidais (mesmo passo nas duas: o dente tem o mesmo tamanho)."""
    pts = []
    da = 2 * PI / n
    for k in range(n):
        a0 = ang + k * da
        for f, rr in ((0.0, r - h_in), (0.2, r - h_in), (0.34, r + h_out), (0.6, r + h_out), (0.74, r - h_in)):
            a = a0 + f * da
            pts.append(c + rr * P3(math.cos(a), math.sin(a)))
    return pts


def engrenagem_fixa(c, r, z=4):
    """Partes da engrenagem que não mudam com o giro (criadas uma vez): sombra projetada, borda clara, miolo escuro, cubo com brilho."""
    c = np.asarray(c, float)
    ri = 0.62 * r
    return VGroup(Circle(radius=r).move_to(c + P3(0.05, -0.06)).set_stroke(width=0).set_fill(BLACK, 0.28).set_z_index(z - 1),
                  Arc(radius=r - 0.05, start_angle=0.55 * PI, angle=0.45 * PI, arc_center=c).set_stroke(WHITE_, 1.6, opacity=0.35).set_z_index(z + 0.1),
                  Circle(radius=ri).move_to(c).set_fill("#141B29", 0.95).set_stroke("#5A6476", 1.2).set_z_index(z + 0.1),
                  aco(Circle(radius=0.18 * r + 0.04).move_to(c), 1.2).set_z_index(z + 0.3),
                  Circle(radius=0.03).move_to(c + P3(-0.03, 0.03)).set_fill(WHITE_, 0.8).set_stroke(width=0).set_z_index(z + 0.3))


def engrenagem25(c, r, ang, n, braços=5, z=4):
    """Parte que gira: dentes (aço com luz B) e a aranha com braços e parafusos."""
    g = VGroup(aco(Polygon(*dentes(c, r, ang, n)), 1.0).set_z_index(z))
    ri = 0.62 * r
    w0, w1 = 0.11 * r + 0.03, 0.07 * r + 0.02
    for k in range(braços):
        a = ang + 2 * PI * k / braços
        u, t = P3(math.cos(a), math.sin(a)), P3(-math.sin(a), math.cos(a))
        g.add(aco(Polygon(c - t * w0, c + u * ri - t * w1, c + u * ri + t * w1, c + t * w0), 0.8).set_z_index(z + 0.2))
    return g


def roda_fixa(c, z=2):
    """Partes da roda que não giram: sombra no chão, pneu com espessura, brilho, aro e o chão."""
    c = np.asarray(c, float)
    x0, x1 = C2[0] - 1.5, C2[0] + 2.05
    return VGroup(Line(P3(x0, Y_CHAO), P3(x1, Y_CHAO)).set_stroke(GEO, 2.5, opacity=0.55).set_z_index(1),
                  Ellipse(width=2 * RR * 0.68, height=0.12).move_to(P3(c[0], Y_CHAO - 0.01)).set_stroke(width=0).set_fill(BLACK, 0.3).set_z_index(z - 1),
                  Circle(radius=RR - 0.1).move_to(c).set_stroke("#1B2029", 20).set_z_index(z),
                  Arc(radius=RR - 0.04, start_angle=0.55 * PI, angle=0.4 * PI, arc_center=c).set_stroke("#6A7488", 2.5, opacity=0.7).set_z_index(z + 0.1),
                  Circle(radius=RR - 0.22).move_to(c).set_stroke(STEEL, 4).set_z_index(z),
                  Circle(radius=RR - 0.27).move_to(c).set_stroke(GEO, 1.4, opacity=0.45).set_z_index(z),
                  Line(C1, C1 + P3(0, -R1)).set_stroke(GEO, 3).set_z_index(5.5),
                  Line(C2, C2 + P3(0, -R2)).set_stroke(GEO, 3).set_z_index(5.5))


def roda25(c, a2, off, z=2):
    """Parte que gira: banda de rodagem, raios finos cruzados, válvula; e os riscos do chão que correm com ω₂R."""
    c = np.asarray(c, float)
    banda, raios, rs = VMobject(), VMobject(), VMobject()
    for k in range(64):
        a = a2 + 2 * PI * k / 64
        u = P3(math.cos(a), math.sin(a))
        banda.append_points(_seg(c + (RR - 0.03) * u, c + (RR - 0.12) * u))
    for k in range(24):
        a = a2 + 2 * PI * k / 24
        s_ = 1 if k % 2 == 0 else -1
        raios.append_points(_seg(c + 0.12 * P3(math.cos(a - s_ * 0.5), math.sin(a - s_ * 0.5)), c + (RR - 0.27) * P3(math.cos(a), math.sin(a))))
    u2 = P3(math.cos(a2), math.sin(a2))
    x0, x1 = C2[0] - 1.5, C2[0] + 2.05
    span = x1 - x0 - 0.12
    for k in range(10):
        x = x0 + 0.12 + (off + k * span / 10) % span
        rs.append_points(_seg(P3(x, Y_CHAO - 0.02), P3(x - 0.05, Y_CHAO - 0.055)))
    valv = VMobject().set_points(_seg(c + (RR - 0.3) * u2, c + (RR - 0.2) * u2))
    return VGroup(banda.set_stroke("#3B4554", 2.2).set_z_index(z + 0.05), raios.set_stroke(GEO, 1.1, opacity=0.55).set_z_index(z),
                  valv.set_stroke(WHITE_, 4).set_z_index(z), rs.set_stroke(GEO, 1.6, opacity=0.4).set_z_index(1))


def pedivela(a1, z=7):
    """Pedivela e pedal do lado de cá (aço) e o do lado de lá (escuro, atrás da coroa): profundidade 2,5D."""
    g = VGroup()
    for lado, (zz, op) in ((-1, (2.5, 0.55)), (1, (z, 1.0))):
        a = a1 + PI / 2 + (PI if lado < 0 else 0.0)
        pe = C1 + L_PED * P3(math.cos(a), math.sin(a))
        u, t = P3(math.cos(a), math.sin(a)), P3(-math.sin(a), math.cos(a))
        braco = Polygon(C1 - 0.05 * u - 0.055 * t, pe + 0.05 * u - 0.04 * t, pe + 0.05 * u + 0.04 * t, C1 - 0.05 * u + 0.055 * t)   # afina para o pedal
        pedal = Polygon(pe + P3(-0.14, -0.05), pe + P3(0.14, -0.05), pe + P3(0.14, 0.05), pe + P3(-0.14, 0.05))
        if lado < 0:
            g.add(braco.set_fill("#2A3242", op).set_stroke("#46506A", 1).set_z_index(zz), pedal.set_fill("#2A3242", op).set_stroke("#46506A", 1).set_z_index(zz))
        else:
            g.add(aco(braco, 1.0).set_z_index(zz), aco(pedal, 1.0).set_z_index(zz),
                  Circle(radius=0.045).move_to(C1).set_fill("#D7DEEA", 1).set_stroke(width=0).set_z_index(zz))
    return g


def corrente(s, flash=0.0, z=6):
    """Elos (placas externas claras e internas escuras, alternadas) que andam com s; `flash` acende a corrente (E2-2)."""
    ext, inn = VMobject(), VMobject()
    for k in range(NEL):
        p, t_, _ = pos_laco(s + k * LT / NEL)
        (ext if k % 2 == 0 else inn).append_points(_seg(p - 0.44 * PASSO * t_, p + 0.44 * PASSO * t_))
    c_e = interpolate_color(ManimColor(VEL), ManimColor(WHITE_), flash)             # v8: a corrente leva a cor da grandeza que ela carrega (v_c, violeta)
    c_i = interpolate_color(ManimColor("#5B4FA8"), ManimColor(CYAN), flash)
    g = VGroup(ext.set_stroke(c_e, 6.5).set_z_index(z), inn.set_stroke(c_i, 5).set_z_index(z))
    if flash > 0.01:
        halo = ext.copy().set_stroke(CYAN, 14, opacity=0.35 * flash).set_z_index(z - 0.5)
        g.add(halo)
    return g


def bicicleta(a1, s, off=0.0, flash=0.0):
    """Parte móvel da transmissão no estado (a1 = ângulo da coroa, s = posição da corrente, off = chão); a parte fixa é `bicicleta_fixa()`."""
    a2 = 2.5 * a1
    return VGroup(roda25(C2, a2, off), engrenagem25(C2, R2, a2, NZ2, braços=4, z=4), engrenagem25(C1, R1, a1, NZ1, braços=5, z=4),
                  corrente(s, flash), pedivela(a1))


def bicicleta_fixa():
    return VGroup(roda_fixa(C2), engrenagem_fixa(C2, R2), engrenagem_fixa(C1, R1))


def setas_cadeia():
    """v3 §3: setas violeta de v_c sobre os dois trechos retos da corrente (no sentido do movimento)."""
    g = VGroup()
    for idx, u0, u1 in ((2, 0.30, 0.50), (0, 0.62, 0.82)):
        a_, b_ = np.asarray(SEG[idx][1], float), np.asarray(SEG[idx][2], float)
        d = (b_ - a_) / np.linalg.norm(b_ - a_)
        n = P3(-d[1], d[0])
        L = np.linalg.norm(b_ - a_)
        g.add(seta(a_ + d * L * u0 - n * 0.22, a_ + d * L * u1 - n * 0.22, VEL, 8, tip=0.2, z=9))
    return g


def inset_vivo(qual, a1, s, ac=0.0):
    """Conteúdo móvel do inset (zoom ×3 em volta do elo P): dentes da engrenagem recortados pelo círculo e os elos que passam."""
    if qual == 1:
        c, r, ang, n, P, Ci = C1, R1, a1, NZ1, P_1, CI1
    else:
        c, r, ang, n, P, Ci = C2, R2, 2.5 * a1, NZ2, P_2, CI2
    z = lambda q: Ci + ZI * (np.asarray(q, float) - P)
    th = TH1 if qual == 1 else TH2
    jan = 1.5 * (RI / ZI) / r                                    # só os dentes perto do elo (cunha até o centro): recorte barato
    da_ = lambda q: (math.atan2(q[1] - c[1], q[0] - c[0]) - th + PI) % (2 * PI) - PI
    perto = sorted([q for q in dentes(c, r, ang, n) if abs(da_(q)) < jan], key=da_)
    pts = [z(q) for q in perto] + [z(c)]
    disco = Circle(radius=RI - 0.03).move_to(Ci)
    g = VGroup(aco(Intersection(Polygon(*pts), disco), 1.0).set_z_index(19))
    ext, inn = VMobject(), VMobject()
    for k in range(NEL):
        p, t_, _ = pos_laco(s + k * LT / NEL)
        if np.linalg.norm(p - P) * ZI > RI - 0.12:
            continue
        (ext if k % 2 == 0 else inn).append_points(_seg(z(p - 0.44 * PASSO * t_), z(p + 0.44 * PASSO * t_)))
    g.add(ext.set_stroke("#C9D2E0", 15).set_z_index(20), inn.set_stroke("#6E7A8C", 11).set_z_index(20))
    return g


def inset_fixo(qual, com_ac=False):
    """Parte fixa do inset: disco PANEL com borda GEO, anel no ponto ampliado e a linha fina até ele, escala, marca do elo, setas v (e a_c)."""
    if qual == 1:
        c, r, th, P, Ci = C1, R1, TH1, P_1, CI1
    else:
        c, r, th, P, Ci = C2, R2, TH2, P_2, CI2
    u = P3(math.cos(th), math.sin(th))
    tg = P3(-math.sin(th), math.cos(th))
    disc = Circle(radius=RI).move_to(Ci).set_stroke(GEO, 3).set_fill(PANEL, 0.92).set_z_index(18)
    disc._fundo = True
    d = (Ci - P) / np.linalg.norm(Ci - P)
    anel = Circle(radius=0.16).move_to(P).set_stroke(GEO, 2.2).set_fill(opacity=0).set_z_index(13)
    lig = Line(P + d * 0.16, Ci - d * RI).set_stroke(GEO, 1.6, opacity=0.9).set_z_index(13)
    esc = txt("×3", 24, bold=True).move_to(P3(-6.88, 0.72) if qual == 1 else P3(-0.1, 0.8)).set_z_index(22)   # fora do círculo (o dente ampliado passa rente por dentro)
    marca = Circle(radius=0.07).move_to(Ci).set_stroke(WHITE_, 2).set_fill(opacity=0).set_z_index(21)
    sv = seta(Ci, Ci + LV_I * tg, VEL, 8, tip=0.18, z=22)
    lc = LC1_I * (1.0 if qual == 1 else 2.5)
    sa = seta(Ci, Ci - lc * u, ACC, 8, tip=0.14 if qual == 1 else 0.17, z=22)
    return VGroup(disc, anel, lig, esc, marca), sv, sa, lc


class LoteE2(L20):

    def construct(self):
        self.setup_base()
        self.pilha.x0, self.pilha.larg = X_CONTA + 0.1, LARG_CONTA - 0.1     # o respiro do destaque (escala 1,06) das linhas não entra na CALHA
        self.e2()
        self.fim()
        self.relatorio()
        self.gravar_reg()

    def e2(self):
        self.an("E2-1")
        self.secao("EXERCÍCIO 2 · A CORRENTE DA BICICLETA")
        S = {"t": self.clk.get_value(), "a1": 0.0, "s": 0.0, "off": 0.0, "w1": 2 * PI, "al1": 0.0, "acel": None, "volt": 0.0}

        def motor(m):
            t = self.clk.get_value()
            dt = t - S["t"]
            S["t"] = t
            if S["acel"] is not None:
                t0, = S["acel"]
                u = min(4.0, max(0.0, t - t0))
                S["w1"] = 2 * PI + (PI / 4) * u
                S["al1"] = PI / 4 if 0 < t - t0 < 4.0 else 0.0
                S["volt"] = (2 * PI * u + 0.5 * (PI / 4) * u * u) / (2 * PI)
            da = S["w1"] / LENTA * dt                     # desenho: ×4 mais lento
            S["a1"] += da
            S["s"] += da * R1                              # os elos andam com v_c = ω₁ r₁ (em escala de desenho)
            S["off"] += 2.5 * da * RR                      # o chão corre sob o pneu com ω₂ R (sem escorregar)
            if not PEDIDOS3D:
                self.reg("corrente", w1=S["w1"], w2=2.5 * S["w1"], v_coroa=S["w1"] * R1, v_catraca=2.5 * S["w1"] * R2, volt=S["volt"])
        mot = VGroup()
        mot.add_updater(motor)
        self.add(mot)
        fl = ValueTracker(0.0)
        self.add(fl)
        bfix = bicicleta_fixa()
        bv = vivo(lambda: bicicleta(S["a1"], S["s"], S["off"], fl.get_value()))
        self.play(FadeIn(bfix), FadeIn(bv), *self.troca_marcador("CÂMERA LENTA ×4", lado="esq", y=Y_MARC), run_time=0.8)

        # ── rótulos do desenho (fora das engrenagens, dos raios e do pneu) ──
        l1 = M("r_1", "=", r"10\ \mathrm{cm}", size=38, cores={0: GEO_, 2: GEO_})[0].move_to(P3(-5.9, -2.35))
        n_co = txt("COROA", 24).move_to(P3(-5.9, -2.73))
        l2 = M("r_2", "=", r"4\ \mathrm{cm}", size=38, cores={0: GEO_, 2: GEO_})[0]
        n_ca = txt("CATRACA", 24)
        n_ca.move_to(P3(-3.92 + n_ca.width / 2, Y_MARC))
        l2.next_to(n_ca, RIGHT, buff=0.24).align_to(n_ca, DOWN)
        x_r2 = l2[0][0:2].get_center()[0]
        lig2 = Line(C2 + P3(0, -R2 - 0.04), P3(x_r2, l2.get_top()[1] + 0.2)).set_stroke(GEO, 1.6, opacity=0.9).set_z_index(5.5)
        lR = M("R", "=", r"35\ \mathrm{cm}", size=38, cores={0: GEO_, 2: GEO_})[0].move_to(P3(-3.55, 1.75))
        aR = 1.9
        cotaR = Line(C2, C2 + (RR - 0.02) * P3(math.cos(aR), math.sin(aR))).set_stroke(GEO, 3).set_z_index(5.5)
        l60 = valor(r"60\ \mathrm{RPM}", VEL, 38).move_to(P3(-5.2, 0.5))   # v5 §2.1: à esquerda do pneu (folga ≥ 0,2 do arco), acima da seta violeta da coroa
        w_on = ValueTracker(0.0)
        self.add(w_on)

        def setas_w():
            o = w_on.get_value()
            if o < 0.01:
                return VGroup()
            sw = SW1 * S["w1"] / (2 * PI)
            return escala_op(seta_curva(C1, 1.1, 0.5, sw, VEL, 8), o)
        wv = vivo(setas_w)
        self.add(wv)
        l_ped = VGroup(txt("PEDALANDO", 24), txt("(RODA LIVRE", 24), txt("ENGATADA)", 24)).arrange(DOWN, aligned_edge=LEFT, buff=0.05)   # v4 §2.2: duas linhas perto do pedal; a linha-guia não cruza a roda nem o 60 RPM
        l_ped.move_to(P3(-7.25 + l_ped.width / 2, 2.0))
        op_pl = ValueTracker(0.0)
        self.add(op_pl)

        def lig_ped():                                         # v3 §5.16: linha-guia do rótulo até o pedal (que gira)
            o = op_pl.get_value()
            if o < 0.01:
                return VGroup()
            a = S["a1"] + PI / 2
            pe = C1 + L_PED * P3(math.cos(a), math.sin(a))
            a0 = P3(l_ped.get_left()[0] + 0.03, l_ped.get_bottom()[1] - 0.3)
            d = (pe - a0) / np.linalg.norm(pe - a0)
            return escala_op(VGroup(Line(a0, pe - d * 0.13).set_stroke(GEO, 1.8, opacity=0.9).set_z_index(9),
                                    Circle(radius=0.11).move_to(pe).set_stroke(GEO, 2.4).set_fill(opacity=0).set_z_index(9)), o)
        lpv = vivo(lig_ped)
        self.add(lpv)
        D1, id1 = M("r_1", "=", r"10\ \mathrm{cm}", size=50, cores={0: GEO_, 2: GEO_})
        D2, id2 = M("r_2", "=", r"4\ \mathrm{cm}", size=50, cores={0: GEO_, 2: GEO_})
        D3, id3 = M("R", "=", r"35\ \mathrm{cm}", size=50, cores={0: GEO_, 2: GEO_})
        D4, id4 = M(r"\omega_1", "=", r"60\ \mathrm{RPM}", size=50, cores={0: VEL, 2: VEL})
        enun = VGroup(txt("BICICLETA DE CORRENTE", 28, bold=True), txt("COROA → CATRACA → RODA", 26)).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        self.gat("uma bicicleta com a coroa")
        self.pilha.poe(enun)
        self.play(FadeIn(n_co), FadeIn(enun), run_time=0.5)
        self.gat("dez centímetros de raio")
        self.play(FadeIn(l1), run_time=0.4)
        self.pilha.poe(D1)
        self.voa([(l1[0][0:2], mp(D1, id1, [0])), (l1[0][3:7], mp(D1, id1, [2]))], extra=[FadeIn(mp(D1, id1, [1]))], rt=0.9)
        self.gat("a catraca a engrenagem pequena")
        self.play(FadeIn(n_ca), run_time=0.5)
        self.gat("de quatro centímetros")
        self.play(FadeIn(l2), Create(lig2), run_time=0.4)
        self.pilha.poe(D2)
        self.voa([(l2[0][0:2], mp(D2, id2, [0])), (l2[0][3:6], mp(D2, id2, [2]))], extra=[FadeIn(mp(D2, id2, [1]))], rt=0.9)
        self.gat("e a roda de trinta e cinco")
        self.play(FadeIn(lR), Create(cotaR), run_time=0.45)
        self.pilha.poe(D3)
        self.voa([(lR[0][0:1], mp(D3, id3, [0])), (lR[0][2:6], mp(D3, id3, [2]))], extra=[FadeIn(mp(D3, id3, [1]))], rt=0.9)
        self.gat("o ciclista pedala a sessenta")
        self.play(w_on.animate.set_value(1.0), op_pl.animate.set_value(1.0), FadeIn(l60), FadeIn(l_ped), run_time=0.5)
        self.pilha.poe(D4)
        self.voa([(l60[0], mp(D4, id4, [2]))], extra=[FadeIn(mp(D4, id4, [0, 1]))], rt=0.9)
        self.gat("com que velocidade angular gira a roda")
        self.selo("PEDE", "O QUE SE IGUALA NO ACOPLAMENTO")
        self.ate(0.99)

        # ── E2-2: dois corpos ──
        self.an("E2-2")
        op_p, op_c1, op_c2 = ValueTracker(0.0), ValueTracker(0.0), ValueTracker(0.0)
        self.add(op_p, op_c1, op_c2)

        def corpos():
            g = VGroup()
            o = op_p.get_value()
            if o > 0.01:                                   # três pontos da coroa (mesmo corpo rígido): giram juntos
                for k, rr in enumerate((0.22, 0.38, 0.54)):
                    a = S["a1"] + 2 * PI / 5 * 0.5
                    g.add(Circle(radius=0.05).move_to(C1 + rr * P3(math.cos(a), math.sin(a))).set_fill(WHITE_, o).set_stroke(VEL, 2, opacity=o).set_z_index(8))
            if op_c1.get_value() > 0.01:
                g.add(Circle(radius=0.95).move_to(C1).set_stroke(VEL, 7, opacity=0.9 * op_c1.get_value()).set_z_index(8))
            if op_c2.get_value() > 0.01:
                o2 = 0.9 * op_c2.get_value()
                g.add(Circle(radius=RR + 0.05).move_to(C2).set_stroke(VEL, 7, opacity=o2).set_z_index(8),
                      Circle(radius=R2 + 0.11).move_to(C2).set_stroke(VEL, 6, opacity=o2).set_z_index(8))
            return g
        cv_ = vivo(corpos)
        self.add(cv_)
        c1l = txt("CORPO 1", 26, bold=True, color=VEL).move_to(P3(-6.25, 1.3))
        c2l = txt("CORPO 2", 26, bold=True, color=VEL).move_to(P3(-0.65, 1.6))
        N1 = linha_m(txt("NUM CORPO RÍGIDO", 26, bold=True), lbl(r"\Rightarrow", WHITE_, 44), txt("MESMO", 26, bold=True), lbl(r"\omega", VEL, 46), buff=0.14)
        N2 = linha_m(txt("CORPOS DIFERENTES", 26, bold=True), lbl(r"\Rightarrow", WHITE_, 44), lbl(r"\omega_1", VEL, 46), lbl(r"\neq", WHITE_, 46),
                     lbl(r"\omega_2", VEL, 46), buff=0.14)
        N3 = linha_m(txt("CATRACA + RODA", 26, bold=True), lbl(r"\Rightarrow", WHITE_, 44), txt("MESMO", 26, bold=True), lbl(r"\omega_2", VEL, 46), buff=0.14)
        self.gat("todos os pontos de um corpo rígido")
        self.play(op_p.animate.set_value(1.0), run_time=0.5)
        self.pilha.poe(N1)
        self.gat("têm a mesma velocidade angular")
        self.play(FadeIn(N1), run_time=0.6)
        self.gat("porque são corpos diferentes")
        self.play(op_p.animate.set_value(0.0), FadeOut(l_ped), op_pl.animate.set_value(0.0), run_time=0.3)          # v8: a legenda velha sai antes de CORPO 1 entrar (não se cruzam no fade)
        self.play(op_c1.animate.set_value(1.0), FadeIn(c1l), run_time=0.3)
        self.pilha.poe(N2)
        self.play(FadeIn(N2), run_time=0.6)
        self.gat("ligados pela corrente")
        self.play(fl.animate(rate_func=there_and_back).set_value(1.0), run_time=0.9)
        self.gat("já a catraca e a roda")
        self.play(op_c2.animate.set_value(1.0), FadeIn(c2l), run_time=0.7)
        self.pilha.poe(N3)
        self.gat("um corpo só com a mesma velocidade angular")
        self.play(FadeIn(N3), run_time=0.6)
        self.ate(0.99)

        # ── E2-3: v_c iguala nas bordas ──
        self.an("E2-3")
        self.play(op_c1.animate.set_value(0.0), op_c2.animate.set_value(0.0), FadeOut(c1l), FadeOut(c2l), op_pl.animate.set_value(0.0), run_time=0.4)   # os dados ficam até a 1ª conta
        self.remove(cv_, lpv)
        self.gat("e o que a corrente faz")
        self.selo("HIPÓTESES", "CORRENTE NÃO ESTICA NEM ESCORREGA", cor=CYAN, borda=GEO)
        op_i = ValueTracker(0.0)
        self.add(op_i)

        def insets():
            o = op_i.get_value()
            if o < 0.01:
                return VGroup()
            return escala_op(VGroup(inset_vivo(1, S["a1"], S["s"]), inset_vivo(2, S["a1"], S["s"])), o)
        iv = vivo(insets)
        self.add(iv)
        f1, sv1, sa1, lc1 = inset_fixo(1)
        f2, sv2, sa2, lc2 = inset_fixo(2)
        lvc1 = lbl("v_c", VEL, 42).move_to(P3(-5.2, 1.95))
        lvc2 = lbl("v_c", VEL, 42).move_to(P3(-2.0, 2.0))
        ch_s = setas_cadeia()
        self.gat("então todos os elos andam com a mesma velocidade")
        self.play(op_i.animate.set_value(1.0), FadeIn(ch_s), FadeIn(f1), FadeIn(f2), FadeIn(sv1), FadeIn(sv2), FadeIn(lvc1), FadeIn(lvc2), run_time=0.8)
        V1, iv1 = M("v_c", "=", r"\omega_1", "r_1", "=", r"\omega_2", "r_2", size=56, cores={0: VEL, 2: VEL, 3: GEO_, 5: VEL, 6: GEO_})
        self.gat("na coroa essa velocidade")
        self.sem_selo()
        self.pilha.limpa(rt=0.35)
        self.pilha.poe(V1)
        self.voa([(lvc1[0], mp(V1, iv1, [0])), (l1[0][0:2], mp(V1, iv1, [3]))], extra=[FadeIn(mp(V1, iv1, [1, 2]))], rt=1.0, origem=False)
        self.gat("na catraca a da catraca")
        self.voa([(l2[0][0:2], mp(V1, iv1, [6]))], extra=[FadeIn(mp(V1, iv1, [4, 5]))], rt=1.0, origem=False)
        V2, iv2 = M(r"\omega_2", "=", r"\omega_1", r"\frac{r_1}{r_2}", size=56, cores={0: VEL, 2: VEL})
        for j in iv2[3][:2] + iv2[3][3:]:
            V2[0][j].set_color(GEO_)
        self.pilha.poe(V2)
        for j in iv2[3][:2] + iv2[3][3:]:
            V2[0][j].set_color(GEO_).set_opacity(1)
        self.gat("igualando a catraca gira")
        # GM: ω₂ vai para a esquerda e o r₂ ATRAVESSA o "=" (sai de ω₂r₂ e desce para o denominador); v_c e o primeiro "=" saem antes
        self.passo(V1, V2, (J(iv1, 0, 1), []), (J(iv1, 5), J(iv2, 0), {"path_arc": -2.3}), (J(iv1, 4), J(iv2, 1)), (J(iv1, 2), J(iv2, 2)), (J(iv1, 3), iv2[3][:2]),
                   ([], iv2[3][2:3]), (J(iv1, 6), iv2[3][3:], {"path_arc": -1.6, "delay": 0.25}), rt=1.5, origem=False)
        V2b, iv2b = M(r"\omega_2", "=", r"2{,}5", r"\,\omega_1", size=56, cores={0: VEL, 3: VEL})
        V2bb = caixa_l(V2b, VEL)
        self.pilha.poe(V2bb, dx=0.2)
        op_w2 = ValueTracker(0.0)
        self.add(op_w2)

        def seta_w2():
            o = op_w2.get_value()
            if o < 0.01:
                return VGroup()
            sw = 2.5 * SW1 * S["w1"] / (2 * PI)
            return escala_op(seta_curva(C2, RR + 0.22, -0.9, sw, VEL, 8), o)
        w2v = vivo(seta_w2)
        self.add(w2v)
        lw2 = lbl(r"\omega_2", VEL, 40).move_to(P3(-0.12, -2.42))
        self.gat("duas vezes e meia mais rápido")
        self.voa([(mp(V2, iv2, [0]), mp(V2b, iv2b, [0])), (mp(V2, iv2, [2]), mp(V2b, iv2b, [3]))],
                 extra=[FadeIn(V2bb[0]), FadeIn(mp(V2b, iv2b, [1, 2])), op_w2.animate.set_value(1.0), FadeIn(lw2)],
                 rt=1.0, origem=False)
        V3, iv3 = M(r"\omega_1", "=", r"60\ \mathrm{RPM}", "=", r"2\pi\ \mathrm{rad/s}", size=48, cores={0: VEL, 2: VEL, 4: VEL})
        self.pilha.poe(V3)
        self.gat("sessenta rotações por minuto são dois pi")
        self.voa([(l60[0], mp(V3, iv3, [2]))], extra=[FadeIn(mp(V3, iv3, [0, 1, 3, 4]))], rt=1.2)
        V3b, iv3b = M(r"\omega_2", "=", r"5\pi", r"\approx", r"15{,}7\ \mathrm{rad/s}", size=50, cores={0: VEL, 2: VEL, 4: VEL})
        self.pilha.poe(V3b)
        self.gat("então a roda gira a cinco pi")
        self.voa([(mp(V2b, iv2b, [0]), mp(V3b, iv3b, [0]))], extra=[FadeIn(mp(V3b, iv3b, [1, 2, 3, 4]))], rt=1.3, origem=False)
        V4, iv4 = M(r"v_{borda}", "=", r"15{,}7", r"\cdot", r"0{,}35", size=50, cores={0: VEL, 2: VEL, 4: GEO_})
        V4m, iv4m = M(r"\approx", r"5{,}50\ \mathrm{m/s}", r"\approx", r"19{,}8\ \mathrm{km/h}", size=48, cores={1: VEL, 3: VEL})
        V4bx = caixa_l(V4m, VEL)
        self.pilha.poe(V4)
        self.gat("e a borda do pneu anda")
        self.voa([(mp(V3b, iv3b, [4])[:4], mp(V4, iv4, [2])), (lR[0][2:4], mp(V4, iv4, [4]))], extra=[FadeIn(mp(V4, iv4, [0, 1, 3]))], rt=1.3)
        self.pilha.poe(V4bx, dx=0.2)
        self.gat("cinco e meio metros por segundo")
        self.play(FadeIn(V4bx[0]), FadeIn(mp(V4m, iv4m, [0, 1])), run_time=0.8)
        self.gat("quase vinte quilômetros por hora")
        self.play(FadeIn(mp(V4m, iv4m, [2, 3])), run_time=0.7)
        l_pn = txt("PNEU SEM ESCORREGAR", 24).move_to(P3(-2.1, Y_MARC))
        self.gat("se o pneu não escorrega no chão")
        self.play(FadeOut(l2), FadeOut(n_ca), FadeOut(lig2), run_time=0.3)
        self.play(FadeIn(l_pn), run_time=0.4)
        nb = txt("É A VELOCIDADE DA BICICLETA", 26, bold=True)
        self.pilha.poe(nb)
        self.gat("essa é a velocidade da bicicleta")
        self.play(FadeIn(nb), run_time=0.6)
        self.foco = V4bx
        self.ate(0.99)

        # ── E2-4: a cadência acelera ──
        self.an("E2-4")
        self.pilha.so(V2bb, anims=[op_i.animate.set_value(0.0), FadeOut(VGroup(f1, f2, sv1, sv2, lvc1, lvc2)), FadeOut(ch_s)])
        self.remove(iv)
        lrpm = vivo(lambda: VGroup(num_mob(f"{S['w1'] * 60 / (2 * PI):.0f}", VEL, 38), mtex(r"\mathrm{RPM}", VEL, 38)).arrange(RIGHT, buff=0.12)
                    .move_to(l60.get_center()))
        self.remove(l60)
        self.add(lrpm)
        opA = ValueTracker(0.0)
        self.add(opA)

        def acel_setas():
            o = opA.get_value()
            if o < 0.01:
                return VGroup()
            return VGroup(escala_op(seta_curva(C1, 1.1, 2.55, 0.8, ACC, 8), o), escala_op(seta_curva(C2, RR + 0.22, 3.7, 0.55, ACC, 8), o))
        av = vivo(acel_setas)
        self.add(av)
        la1 = lbl(r"\alpha_1", ACC, 40).move_to(P3(-6.95, -1.8))
        la2 = lbl(r"\alpha_2", ACC, 40).move_to(P3(-4.58, -2.64))      # folga do rótulo r₁ (x) e do marcador de canto (y) (G28 ENCOSTADO)

        def contador():
            return VGroup(mtxt("PEDAL:", 26), num_mob(f"{S['volt']:.2f}".replace(".", ","), WHITE_, 42), mtxt("VOLTAS", 26)).arrange(RIGHT, buff=0.22)\
                .move_to(P3(-7.25, 2.35), aligned_edge=LEFT)
        cv = vivo(contador)
        A0 = linha_m(lbl(r"60\rightarrow 90\ \mathrm{RPM}", VEL, 46), txt("EM", 26), lbl(r"4\ \mathrm{s}", WHITE_, 46), buff=0.14)
        self.pilha.poe(A0)
        self.gat("agora o ciclista acelera a cadência")
        self.play(FadeIn(A0), FadeIn(cv), opA.animate.set_value(1.0), FadeIn(la1), FadeIn(la2), run_time=0.7)
        S["acel"] = (self.clk.get_value(),)
        S["volt"] = 0.0
        A1, ia1 = M(r"\alpha_1", "=", r"\frac{3\pi-2\pi}{4}", size=50, cores={0: ACC})
        for j in (ia1[2][0], ia1[2][1], ia1[2][3], ia1[2][4]):
            A1[0][j].set_color(VEL)
        A1b, ia1b = M("=", r"\frac{\pi}{4}", r"\approx", r"0{,}785\ \mathrm{rad/s^2}", size=50, cores={1: ACC, 3: ACC})
        self.pilha.poe(A1)
        self.gat("a aceleração angular da coroa")
        self.play(FadeIn(A1), run_time=0.9)
        self.pilha.poe(A1b)
        self.gat("pi sobre quatro")
        # GM: (3π − 2π) vira π (troca, sem sopa); a barra e o 4 descem para a linha de baixo; ≈ 0,785 é escrito na fila por x
        self.passo(A1, A1b, (J(ia1, 0), []), (J(ia1, 1), J(ia1b, 0)), (ia1[2][:5], ia1b[1][:1]), (ia1[2][5:6], ia1b[1][1:2]), (ia1[2][6:7], ia1b[1][2:3]),
                   ([], J(ia1b, 2, 3)), rt=1.3, origem=False)
        A2, ia2 = M(r"\alpha_2", "=", r"2{,}5", r"\,\alpha_1", r"\approx", r"1{,}96\ \mathrm{rad/s^2}", size=50, cores={0: ACC, 3: ACC, 5: ACC})
        self.pilha.poe(A2)
        self.gat("como a relação da corrente vale")
        # GM da relação do E2-3 (vale a cada instante): ω₂ → α₂, ω₁ → α₁; o 2,5 viaja da caixa
        self.passo(V2b, A2, (J(iv2b, 0), J(ia2, 0)), (J(iv2b, 1), J(ia2, 1)), (J(iv2b, 2), J(ia2, 2)), (J(iv2b, 3), J(ia2, 3)), ([], J(ia2, 4, 5)),
                   rt=1.3, origem=False)
        A3, ia3 = M("a", "=", r"\alpha_2", "R", r"\approx", r"0{,}69\ \mathrm{m/s^2}", size=50, cores={0: ACC, 2: ACC, 3: GEO_, 5: ACC})
        self.pilha.poe(A3)
        self.gat("com o pneu sem escorregar")
        self.play(Indicate(l_pn, color=WHITE_, scale_factor=1.06), run_time=0.7)
        self.gat("a bicicleta acelera isso vezes trinta e cinco")
        self.voa([(mp(A2, ia2, [0]), mp(A3, ia3, [2])), (lR[0][0:1], mp(A3, ia3, [3]))], extra=[FadeIn(mp(A3, ia3, [0, 1, 4, 5]))], rt=1.3, origem=False)
        A4, ia4 = M(r"\Delta\theta_1", "=", r"\tfrac12", r"(2\pi+3\pi)", r"\cdot", "4", size=50, cores={0: ANG})
        for j in (ia4[3][1], ia4[3][2], ia4[3][4], ia4[3][5]):
            A4[0][j].set_color(VEL)
        A4m, ia4m = M(r"\Delta\theta_1", "=", r"10\pi\ \mathrm{rad}", "=", "5", size=48, cores={0: ANG, 2: ANG, 4: ANG})
        A4b = caixa_l(linha_m(A4m, txt("VOLTAS", 26), buff=0.3), ANG)
        self.pilha.poe(A4)
        self.gat("e nesses quatro segundos o pedal dá")
        self.play(FadeIn(A4), Indicate(cv, color=WHITE_, scale_factor=1.04), run_time=1.0)
        self.pilha.poe(A4b, dx=0.2)
        self.gat("exatamente cinco voltas")
        self.passo(A4, A4m, (J(ia4, 0), J(ia4m, 0)), (J(ia4, 1), J(ia4m, 1)), (J(ia4, 2, 3, 4, 5), J(ia4m, 2)), ([], J(ia4m, 3, 4)), rt=1.3, origem=False,
                   extra=[Write(A4b[1][1])])
        self.play(Create(A4b[0]), run_time=0.4)      # v6 §2.2: a caixa nasce depois do conteúdo (nunca vazia)
        self.foco = A4b
        self.ate(0.99)
        S["acel"] = None

        # ── E2-5: elo na coroa e elo na catraca ──
        self.an("E2-5")
        S["w1"] = 2 * PI
        self.pilha.limpa(rt=0.4, anims=[opA.animate.set_value(0.0), FadeOut(cv), FadeOut(la1), FadeOut(la2), FadeOut(lR), FadeOut(cotaR), FadeOut(l_pn)])
        self.remove(cv, av, lrpm)
        self.play(FadeIn(l2), FadeIn(n_ca), FadeIn(lig2), FadeIn(ch_s), run_time=0.4)
        W5, iw5 = M("v_c", "=", r"\omega_1", "r_1", size=54, cores={0: VEL, 2: VEL, 3: GEO_})      # v3 §4: a coluna entra com a conta de partida
        W5b, iw5b = M("=", r"2\pi", r"\cdot", r"0{,}10", r"\approx", r"0{,}63\ \mathrm{m/s}", size=54, cores={1: ANG, 3: GEO_, 5: VEL})
        self.pilha.poe(W5)
        self.play(FadeIn(W5), run_time=0.9)
        f1, sv1, sa1, lc1 = inset_fixo(1, True)
        f2, sv2, sa2, lc2 = inset_fixo(2, True)
        iv = vivo(insets)
        self.add(iv)
        lv1 = lbl(r"0{,}63\ \mathrm{m/s}", VEL, 36).move_to(P3(-4.65, 2.2))
        lv2 = lbl(r"0{,}63\ \mathrm{m/s}", VEL, 36).move_to(P3(-2.85, 2.3))
        la_1 = lbl(r"3{,}9\ \mathrm{m/s^2}", ACC, 36).move_to(P3(-4.65, 1.42))
        la_2 = lbl(r"9{,}9\ \mathrm{m/s^2}", ACC, 36).move_to(P3(-2.85, 1.73))
        self.gat("um elo andando a zero vírgula sessenta")
        self.play(op_i.animate.set_value(1.0), FadeIn(f1), FadeIn(f2), FadeIn(sv1), FadeIn(sv2), FadeIn(lv1), FadeIn(lv2), run_time=0.8)
        self.pilha.poe(W5b)
        self.voa([(lv1[0], mp(W5b, iw5b, [5]))], extra=[FadeIn(mp(W5b, iw5b, [0, 1, 2, 3, 4]))], rt=1.1)
        if not PEDIDOS3D:
            self.reg("e2_5c", r=R1, Lc=lc1, v=LV_I)
            self.reg("e2_5k", r=R2, Lc=lc2, v=LV_I)
        B1, ib1 = M("a_c", "=", r"\frac{v^2}{r_1}", r"\approx", r"3{,}9\ \mathrm{m/s^2}", size=54, cores={0: ACC, 4: ACC})
        B1[0][ib1[2][0]].set_color(VEL)
        B1[0][ib1[2][1]].set_color(VEL)
        for j in ib1[2][3:]:
            B1[0][j].set_color(GEO_)
        self.pilha.poe(B1)
        self.gat("tem aceleração centrípeta de três vírgula nove na coroa")
        self.play(FadeIn(sa1), FadeIn(la_1), run_time=0.5)
        self.voa([(sv1, VGroup(B1[0][ib1[2][0]])), (l1[0][0:2], VGroup(*[B1[0][j] for j in ib1[2][3:]]))],
                 extra=[FadeIn(mp(B1, ib1, [0, 1, 3, 4])), FadeIn(VGroup(B1[0][ib1[2][1]], B1[0][ib1[2][2]]))], rt=1.3, origem=False)
        B2, ib2 = M("a_c", "=", r"\frac{v^2}{r_2}", r"\approx", r"9{,}9\ \mathrm{m/s^2}", size=54, cores={0: ACC, 4: ACC})
        B2[0][ib2[2][0]].set_color(VEL)
        B2[0][ib2[2][1]].set_color(VEL)
        for j in ib2[2][3:]:
            B2[0][j].set_color(GEO_)
        self.pilha.poe(B2)
        self.gat("e de nove vírgula nove na catraca")
        self.play(FadeIn(sa2), FadeIn(la_2), run_time=0.5)
        self.voa([(sv2, VGroup(B2[0][ib2[2][0]])), (l2[0][0:2], VGroup(*[B2[0][j] for j in ib2[2][3:]]))],
                 extra=[FadeIn(mp(B2, ib2, [0, 1, 3, 4])), FadeIn(VGroup(B2[0][ib2[2][1]], B2[0][ib2[2][2]]))], rt=1.3, origem=False)
        self.gat("mesma velocidade raio menor")
        B3 = linha_m(txt("RAIO MENOR", 26, bold=True), lbl(r"\Rightarrow", WHITE_, 42), lbl(r"\omega", VEL, 44), txt("E", 26), lbl("a_c", ACC, 44),
                     txt("MAIORES", 26, bold=True), buff=0.1)
        self.pilha.poe(B3)
        self.play(FadeIn(B3), run_time=0.6)
        self.gat("a dica que fica")
        self.pilha.x0, self.pilha.larg = 0.9, 5.8        # o respiro do destaque (escala 1,06) da DICA não entra na CALHA
        self.dica18([["NUM CORPO RÍGIDO: MESMO", lbl(r"\omega", VEL, 34)], ["ACOPLADOS: MESMA", lbl("v", VEL, 34), "NO CONTATO"]])
        self.ate(0.99)
        mot.clear_updaters()

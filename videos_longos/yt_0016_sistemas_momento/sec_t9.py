"""Lote P9 (v4): T9 — escolher o sistema. Bola de 1 kg caindo 10 m (uma vez; um replay com a Terra); blocos de 1 kg e 2 kg com mola num
chão com atrito (μ = 0,2). v4 (regra 1.2): cada evento roda UMA vez sincronizado com a fala (câmera lenta 4×, o contador t só sobe) e o
estado final fica; em T9-6 o pico acende com o bloco pesado parado; em T9-7 um replay (chip REPLAY) desenha P_Terra(t), espelhado.
P(t) = −1,96 t até 0,510 s, depois −(2,0 − 1,96 t) até 1,020 s; P_Terra = −P."""
from kit import *  # noqa: F401,F403

G_ = 9.8
MU = 0.2
M1, M2, V1, V2 = 1.0, 2.0, -2.0, 1.0
AF = MU * G_                                     # 1,96 m/s²
T2, T1 = V2 / AF, -V1 / AF                       # 0,510 s (pesado para) · 1,020 s (leve para)
F1, F2 = MU * M1 * G_, -MU * M2 * G_             # +1,96 N · −3,92 N
assert abs(M1 * V1 + M2 * V2) < 1e-12 and abs(F1 - 1.96) < 1e-12 and abs(F2 + 3.92) < 1e-12


def v1(t):
    return V1 + AF * t if t < T1 else 0.0


def v2(t):
    return V2 - AF * t if t < T2 else 0.0


def x1(t):
    t = min(t, T1)
    return V1 * t + AF * t * t / 2


def x2(t):
    t = min(t, T2)
    return V2 * t - AF * t * t / 2


def P(t):
    return M1 * v1(t) + M2 * v2(t)


assert abs(T2 - 0.5102) < 1e-3 and abs(T1 - 1.0204) < 1e-3
assert abs(P(T2) + 1.0) < 1e-9 and abs(P(T1)) < 1e-9 and abs(P(0.3) + 1.96 * 0.3) < 1e-9 and abs(P(0.8) + (2.0 - 1.96 * 0.8)) < 1e-9
assert abs(x1(T1) + 1.0204) < 1e-3 and abs(x2(T2) - 0.2551) < 1e-3
assert abs(1 * math.sqrt(2 * G_ * 10) / 5.97e24 - 2.35e-24) < 0.01e-24

Y_CH = 0.45                    # chão dos blocos (v6: palco ×1,3 e centralizado na altura; os gráficos embaixo)
ESC = 2.2                      # u por metro
XC = -3.0                      # centro da mola
LL, HL, LP, HP = 1.3, 1.3, 1.75, 1.69
SLOW, T0P = 4.0, 0.6           # câmera lenta ×4; tempo parado antes do disparo
TMAX = 1.2                     # fim do eixo t (s)
# v7: palco 3D (Three.js). Blocos: câmera lateral elevada 12° (as setas comparam comprimentos); 3D = Manim no plano y = 0.
DL, DP = 1.0, 1.25             # profundidade dos blocos (leve, pesado)
CAM_BL = {"modo": "frente", "K": 1.0, "xc": XC, "yc": Y_CH, "camx": XC, "camz": 0.0, "fov": 14, "el": 12}
# bola e Terra: a Terra tem raio RE (3D) e o topo tangente ao chão; no fim do dolly-out ela tem raio RS no Manim
XB, RE, RS, EC = -3.6, 60.0, 2.3, P3(-4.0, -0.9)
KE = RS / RE


def cam_terra(w, k0=1.0):
    """w = 0: vista de perto (o chão em y = −2,3); w = 1: o planeta inteiro com centro em EC. Zoom exponencial."""
    k = math.exp((1 - w) * math.log(k0) + w * math.log(KE))
    return {"modo": "frente", "K": k, "xc": XB + (EC[0] - XB) * w, "yc": -2.3 + (EC[1] + 2.3) * w, "camx": XB,
            "camz": -RE * (k0 - k) / (k0 - KE), "fov": 14, "el": 8}


class LoteT9(Base):
    def construct(self):
        self.setup_base(cap="ESCOLHER O SISTEMA")
        self.warps = {}
        self.t9_1_2()
        self.t9_3()
        self.t9_4()
        self.t9_5_6()
        self.t9_7()
        self.fim()
        self.relatorio()

    # ── T9-1, T9-2: bola e Terra; a bola cai uma vez e tem um replay ───────────────────────────────────────
    def t9_1_2(self):
        self.an("T9-1")
        YT, YB = 2.0, -2.0
        self.terra_on = ValueTracker(0.0)
        TQ = 2.4                                # a queda na tela (câmera lenta ≈ 1,7×)
        TQ2 = 5.0                               # v6 (palco vivo): o replay com a Terra, ≈ 3,5×
        quedas = self.quedas = [self.clk.get_value() + self.ate_dizer("cai de dez metros", mover=False)]   # v5: na fala
        tA = self.clk.get_value()
        dol = [1e9]                             # v7: início do dolly-out (T9-2)

        def u_():
            tt = self.clk.get_value()
            ti = max([x for x in quedas if x <= tt + 1e-9] or [quedas[0]])
            s = max(0.0, tt - ti)
            T_ = TQ if ti == quedas[0] else TQ2                 # v6: o replay (bola + Terra) em câmera lenta mais forte
            return min(1.0, (s / T_) ** 2), s

        def w_(t=None):                         # progresso do dolly-out (3,2 s, suave)
            t = self.clk.get_value() if t is None else t
            u = min(1.0, max(0.0, (t - dol[0]) / 3.2))
            return u * u * (3 - 2 * u)

        def cam_(t=None):
            t = self.clk.get_value() if t is None else t
            k0 = 1.0 + 0.004 * max(0.0, min(t, dol[0]) - tA)      # v7 (palco vivo): aproximação lenta na vista de perto (0,4 %/s)
            c = cam_terra(w_(t), k0)
            return c

        def bz():
            return 4.3 - 4.0 * u_()[0]

        def est(t):
            w = w_(t)
            return {"bx": XB, "bz": bz(), "piso": max(0.0, 1 - 2.2 * w), "terra": min(1.0, max(0.0, (w - 0.12) / 0.35)),
                    "rot": 0.2 * (t - tA), "cam": cam_(t)}
        self.f3t = Fundo3D(self, "terra", est, op=0.0)
        self.f3t.conta.set_value(1.0)
        self.add(self.f3t)

        def bola_cai():
            u, s = u_()
            w = w_()
            cam = cam_()
            c = proj3d(cam, (XB, 0, bz()))
            v = 14.0 * math.sqrt(u) if u < 1 else 0.0
            oc = max(0.0, 1 - 3 * w)                                      # o que é da vista de perto some no afastamento
            g = VGroup()
            if oc > 0.01:
                g.add(escala_op(VGroup(arrow(c, c + P3(0, -0.85), color=FC, width=6, tip=0.16, z=9)), oc))
                lab = mtex(r"m\vec g", FC, 30)
                g.add(escala_op(lab.move_to(c + P3(-0.56 - 0.18 - lab.width / 2, 0.12)), oc))
            if w > 0.5:                                                   # no planeta a bola é um ponto: marcador claro
                g.add(Dot(c, radius=0.075, color=WHITE_).set_z_index(9), Dot(c, radius=0.14, color=WHITE_).set_opacity(0.2).set_z_index(9))
            if v > 0.3:
                if w < 0.5:
                    g.add(arrow(c + P3(0.55, 0), c + P3(0.55, -0.12 * v), color=MAG, width=7, tip=0.17, z=9))
                    g.add(mtex(r"\vec p", MAG, 34).next_to(c + P3(0.55, -0.06 * v), RIGHT, buff=0.12))
                else:                       # v7: na vista do planeta os rótulos ficam fora do corpo 3D
                    g.add(arrow(c + P3(0.42, 0), c + P3(0.42, -0.12 * v), color=MAG, width=7, tip=0.17, z=9))
                    g.add(mtex(r"\vec p", MAG, 34).move_to(c + P3(0.95, 0.2)))
                if self.terra_on.get_value() > 0.5:
                    sp = P3(EC[0] + RS + 0.4, EC[1] - 0.65)
                    g.add(arrow(sp, sp + P3(0, 0.12 * v), color=MAG, width=7, tip=0.17, z=9))
                    g.add(mtex(r"-\vec p", MAG, 34).move_to(P3(EC[0] + RS - 0.15, 0.5)))   # fora da Terra, à esquerda da seta
            return g
        bg = always_redraw(bola_cai)

        def fronteira_():                       # v7: a fronteira cresce com o afastamento, da bola até englobar a Terra
            w = w_()
            c = proj3d(cam_(), (XB, 0, bz()))
            cc = c + (EC - c) * w
            r = 0.56 + (RS + 0.9 - 0.56) * w
            return DashedVMobject(Circle(radius=r, arc_center=cc).set_stroke(WHITE_, 2, opacity=0.65), num_dashes=int(16 + 40 * w))
        fr_b = always_redraw(fronteira_)

        def cota_():
            w = w_()
            oc = max(0.0, 1 - 3 * w)
            if oc < 0.01:
                return VGroup()
            cam = cam_()
            top, chao_ = proj3d(cam, (XB, 0, 4.3)), proj3d(cam, (XB, 0, 0))
            x = chao_[0] - 1.85 * cam["K"]
            return escala_op(VGroup(DoubleArrow(P3(x, top[1]), P3(x, chao_[1]), buff=0, color=DIM, stroke_width=2, tip_length=0.12),
                                    tex(r"10\ \mathrm{m}", DIM, 30).move_to(P3(x - 0.55, (top[1] + chao_[1]) / 2))), oc)       # v6 (N8)
        cota = always_redraw(cota_)

        def lt_():
            w = w_()
            a, b = P3(XB + 2.4, -3.0), EC + P3(2.75, -2.6)                  # v7: fora da fronteira tracejada
            return txt("TERRA", 22, color=GEO).move_to(a + (b - a) * w)
        lt = always_redraw(lt_)
        lento = chip_lento()
        self.play(self.f3t.op.animate.set_value(1.0), FadeIn(lt), FadeIn(cota), FadeIn(bg), FadeIn(lento), run_time=0.6)
        ls = txt("SISTEMA: SÓ A BOLA", 22, op=0.85).move_to(P3(XB + 2.3, YT + 0.62))
        r1 = Mc((r"v=", VEL), (r"\sqrt{2gh}", VEL), (r"=14{,}0\ \mathrm{m/s}", VEL), size=42)
        r2 = linha(tex(r"\vec p", MAG, 42), "MUDA O TEMPO TODO", size=24, buff=0.18)
        r3 = txt("O PESO É EXTERNO", 24, color=FC)
        for m_, y in ((r1, 1.8), (r2, 0.85), (r3, 0.1)):
            na_conta(m_, y)
        self.diz("A velocidade de chegada")
        self.play(FadeIn(r1[0], shift=0.1 * UP), run_time=0.5)
        self.diz("a raiz quadrada")
        self.play(FadeIn(r1[1], shift=0.1 * UP), run_time=0.6)
        while self.clk.get_value() < quedas[0] + TQ:
            self.wait(1 / FPS)
        self.play(FadeOut(lento), run_time=0.3)
        self.diz("catorze metros por segundo")
        self.play(FadeIn(r1[2], shift=0.1 * UP), run_time=0.6)
        self.diz("Se o sistema é só a bola")
        self.play(Create(fr_b), FadeIn(ls), run_time=0.8)
        self.diz("o momento dela cresce")
        self.play(FadeIn(r2, shift=0.1 * UP), run_time=0.7)
        self.diz("o peso vem da Terra")
        self.play(FadeIn(r3, shift=0.1 * UP), run_time=0.7)
        self.ate(0.97)
        # T9-2 — bola + Terra: a câmera se afasta até o planeta e a fronteira cresce junto; um replay da queda nessa vista
        self.an("T9-2")
        dol[0] = self.clk.get_value()
        lsb = linha("SISTEMA: BOLA", mais(30), "TERRA", size=22, buff=0.12).set_opacity(0.85).move_to(ls)
        self.play(FadeOut(ls), FadeIn(lsb), FadeOut(r2), FadeOut(r3), run_time=1.4)
        self.terra_on.set_value(1.0)
        ie = txt("A FORÇA ENTRE ELAS FICA INTERNA", 22, color=INT)
        na_conta(ie, 0.85)
        self.diz("A atração entre as duas")
        self.play(FadeIn(ie), run_time=0.6)
        e0 = Mc((r"\vec P_{\text{total}}", MAG), "=", "0", size=50)
        n0 = txt("EM TODO INSTANTE", 20, color=DIM)
        na_conta(e0, -0.1); na_conta(n0, -0.75)
        self.diz("o momento total fica zero")
        self.play(FadeIn(e0, shift=0.1 * UP), FadeIn(n0), run_time=0.8)
        rp = chip_replay()
        lento = chip_lento(x=PALCO_X[0] + 1.35)
        self.diz("A bola ganha momento para baixo")
        quedas.append(self.clk.get_value() + 0.3)
        self.play(FadeIn(rp), FadeIn(lento), run_time=0.4)
        # v5 (V9): quebra depois do "=": a segunda linha alinhada pelo sinal, longe da borda direita
        et1 = MathTex(r"v_{\text{Terra}}=\frac{1\cdot 14}{5{,}97\times10^{24}}", font_size=38, color=mix(VEL, 0.45))   # v6: contraste
        et2 = MathTex(r"\approx 2{,}3\times10^{-24}\ \mathrm{m/s}", font_size=38, color=mix(VEL, 0.45))
        na_conta(et1, -1.6)
        et2.next_to(et1, DOWN, buff=0.22).align_to(et1[0][6], LEFT)
        et = VGroup(et1, et2)
        assert et.get_right()[0] <= 7.7
        ni = txt("IMPOSSÍVEL DE PERCEBER", 18, color=DIM)
        na_conta(ni, -2.95)
        self.diz("Só que a Terra tem")
        self.play(FadeIn(et1, shift=0.1 * UP), run_time=0.9)
        self.diz("dois vírgula três vezes dez")
        self.play(FadeIn(et2, shift=0.1 * UP), run_time=0.7)
        self.diz("Ninguém percebe")
        self.play(FadeIn(ni), run_time=0.5)
        while self.clk.get_value() < quedas[-1] + TQ2:      # v6: o replay lento corre junto com a conta; os chips saem no fim dele
            self.wait(1 / FPS)
        self.play(FadeOut(rp), FadeOut(lento), run_time=0.3)
        self.ate(0.97)
        for m_ in (bg, fr_b, cota, lt):
            m_.clear_updaters()

    # ── experimento dos blocos (uma vez, em câmera lenta) ──────────────────────────────────────────────────
    def tau(self, t0):
        """Tempo físico do experimento disparado em t0 (−1 = antes do disparo); só sobe, sem loop."""
        s = self.clk.get_value() - t0
        w = self.warps.get(t0)
        if w is not None:                       # v5: câmera lenta ajustada à fala (marcos de tela → tempo físico)
            xs, ys = w
            return -1.0 if s < xs[0] else float(np.interp(s, xs, ys))
        if s < T0P:
            return -1.0
        return min((s - T0P) / SLOW, TMAX)

    def warp(self, t0, *marcos):
        """marcos: (instante do relógio do lote, tempo físico); o primeiro é o disparo (τ = 0)."""
        self.warps[t0] = ([m[0] - t0 for m in marcos], [m[1] for m in marcos])

    def fis(self, t0, iguais):
        """Física dos blocos no quadro corrente: posições (Manim = 3D no plano y = 0), velocidades, forças, tamanhos."""
        t = self.tau(t0) if t0 is not None else -1.0
        if iguais:
            ve = 1.5
            T = ve / AF
            tc = min(max(t, 0), T)
            d = ve * tc - AF * tc * tc / 2
            xa, xb = XC - 0.5 - LP / 2 - ESC * d, XC + 0.5 + LP / 2 + ESC * d
            va, vb = (-(ve - AF * tc), ve - AF * tc) if 0 <= t < T else (0.0, 0.0)
            la, ha, lb, hb, da = LP, HP, LP, HP, DP
            fa, fb = (MU * 1.5 * G_, -MU * 1.5 * G_) if 0 <= t < T else (0, 0)
        else:
            xa, xb = XC - 0.5 - LL / 2 + ESC * x1(max(t, 0)), XC + 0.5 + LP / 2 + ESC * x2(max(t, 0))
            va, vb = (v1(t), v2(t)) if t >= 0 else (0.0, 0.0)
            la, ha, lb, hb, da = LL, HL, LP, HP, DL
            fa = F1 if 0 <= t < T1 else 0.0
            fb = F2 if 0 <= t < T2 else 0.0
        return dict(t=t, xa=xa, xb=xb, va=va, vb=vb, la=la, ha=ha, lb=lb, hb=hb, da=da, fa=fa, fb=fb, iguais=iguais)

    def poeira(self, t0, iguais):
        """v7: poeira fina de atrito (determinística): emitida na traseira de cada bloco enquanto ele desliza; vive ~1 s (tempo físico)."""
        f = self.fis(t0, iguais)
        t = f["t"]
        out = []
        if t <= 0:
            return out
        rng = np.random.default_rng(16)
        for k in range(int(t / 0.04) + 1):
            tk = 0.04 * k
            if tk > t:
                break
            for lado in (0, 1):
                r1, r2, r3 = rng.uniform(-1, 1), rng.uniform(0, 1), rng.uniform(0.8, 1.2)
                if iguais:
                    ve = 1.5
                    T = ve / AF
                    if tk >= T:
                        continue
                    dk = ve * tk - AF * tk * tk / 2
                    x = (XC - 0.5 - LP / 2 - ESC * dk + LP / 2) if lado == 0 else (XC + 0.5 + LP / 2 + ESC * dk - LP / 2)
                    sg, dd = (1, DP) if lado == 0 else (-1, DP)
                else:
                    if lado == 0 and tk >= T1 or lado == 1 and tk >= T2:
                        continue
                    x = (XC - 0.5 - LL / 2 + ESC * x1(tk) + LL / 2) if lado == 0 else (XC + 0.5 + LP / 2 + ESC * x2(tk) - LP / 2)
                    sg, dd = (1, DL) if lado == 0 else (-1, DP)
                a = t - tk
                op = 0.42 * math.exp(-a / 0.32) * r3
                if op < 0.03:
                    continue
                out.append([round(x + sg * (0.05 + 0.25 * a), 3), round(r1 * dd * 0.45, 3), round(0.04 + 0.22 * (1 - math.exp(-a / 0.3)) * r2, 3),
                            round(0.12 + 0.3 * a, 3), round(op, 3)])
        return out[:60]

    def est_bl(self, t):
        c = self.bcfg
        if c is None:
            return {"chao": "concreto", "blocos": [], "cam": CAM_BL}
        t0, iguais, _ = c
        f = self.fis(t0, iguais)
        o = self.bop.get_value()                                       # os blocos 3D somem e voltam nas trocas de experimento
        e = {"chao": "concreto", "cam": CAM_BL,
             "blocos": [{"x": f["xa"], "w": f["la"], "h": f["ha"], "d": f["da"], "mat": "grafite" if iguais else "aco", "op": o},
                        {"x": f["xb"], "w": f["lb"], "h": f["hb"], "d": DP, "mat": "grafite", "op": o}],
             "poeira": self.poeira(t0, iguais) if t0 is not None else []}
        if f["t"] < 0.02:                                               # a mola comprimida entre os blocos (antes do disparo)
            e["mola"] = {"xa": f["xa"] + f["la"] / 2, "xb": f["xb"] - f["lb"] / 2, "z": 0.55, "n": 7, "op": o}
        return e

    def blocos(self, t0, iguais=False, forcas=False, setas_v=True, acende=None):
        def f():
            F = self.fis(t0, iguais)
            t, xa, xb, va, vb = F["t"], F["xa"], F["xb"], F["va"], F["vb"]
            la, ha, lb, hb, da = F["la"], F["ha"], F["lb"], F["hb"], F["da"]
            fa, fb = F["fa"], F["fb"]
            self.bcfg = (t0, iguais, None)
            g = VGroup()
            pa, pb = proj3d(CAM_BL, (xa, -da / 2, 0)), proj3d(CAM_BL, (xb, -DP / 2, 0))     # aresta de baixo, na frente
            self._rot = (pa, pb, iguais)
            if acende is not None and acende.get_value() > 0.01:
                q0, q1 = proj3d(CAM_BL, (xb - lb / 2, -DP / 2, 0)), proj3d(CAM_BL, (xb + lb / 2, DP / 2, hb))
                g.add(RoundedRectangle(width=q1[0] - q0[0] + 0.2, height=q1[1] - q0[1] + 0.2, corner_radius=0.08)
                      .move_to((q0 + q1) / 2).set_stroke(WHITE_, 3, opacity=acende.get_value()))
            if forcas and t >= 0:
                if abs(fa) > 0:
                    g.add(arrow(pa + P3(0, -0.2), pa + P3(0.32 * fa, -0.2), color=FC, width=7, tip=0.17, z=10))
                if abs(fb) > 0:
                    g.add(arrow(pb + P3(0, -0.2), pb + P3(0.32 * fb, -0.2), color=FC, width=7, tip=0.17, z=10))
            if setas_v:
                yv = Y_CH + max(ha, hb) + 0.35
                for x, v in ((xa, va), (xb, vb)):
                    if abs(v) > 0.04:
                        g.add(arrow(P3(x, yv), P3(x + 0.55 * v, yv), color=VEL, width=6, tip=0.16, z=10))
            return g
        return f

    def rotulos(self, nomes=None):
        """v7: os rótulos de massa ficam embaixo de cada bloco (nada escrito sobre o corpo 3D); `nomes` (ValueTracker 0–2) mostra
        LEVE / PESADO embaixo deles (só no T9-3)."""
        def f():
            pa, pb, iguais = getattr(self, "_rot", (ORIGIN, ORIGIN, False))
            g = VGroup(mtex(r"m" if iguais else r"1\ \mathrm{kg}", WHITE_, 28).move_to(pa + P3(0, -0.55)),
                       mtex(r"m" if iguais else r"2\ \mathrm{kg}", WHITE_, 28).move_to(pb + P3(0, -0.55))).set_z_index(11)
            if nomes is not None:
                n = nomes.get_value()
                for k, (pp, s_) in enumerate(((pa, "LEVE"), (pb, "PESADO"))):
                    o = min(1.0, max(0.0, n - k))
                    if o > 0.01:
                        g.add(txt(s_, 18, color=DIM, op=o).move_to(pp + P3(0, -0.9)))
            return g
        return always_redraw(f)

    def t9_3(self):
        self.an("T9-3")
        # virada em sequência: a bola, a Terra, a fronteira e a conta saem inteiras; depois entram os blocos
        self.virada(tudo=True)
        self.remove(self.f3t)
        self.bcfg = None
        self.bop = ValueTracker(1.0)
        self.f3b = Fundo3D(self, "blocos", self.est_bl, op=0.0)
        self.f3b.conta.set_value(1.0)
        self.add(self.f3b)
        self.piso = self.f3b.op                                         # v7: o chão é o concreto do 3D
        # v7: à direita, abaixo dos rótulos de massa (que agora ficam sob os blocos), acima do gráfico
        self.lat = txt("CHÃO COM ATRITO", 16, color=DIM).move_to(P3(0.55, Y_CH - 1.22), aligned_edge=RIGHT)
        self.eixo = VGroup(arrow(P3(-1.7, 2.95), P3(-0.7, 2.95), color=DIM, width=3, tip=0.13), tex(r"+x", DIM, 30).move_to(P3(-0.35, 2.95)))
        t0 = self.clk.get_value()
        ts = self.clk_de("T9-3", "A mola dispara os dois", 0.05)      # v6 (1.2): o disparo curto em câmera lenta, e congela
        self.warp(t0, (ts, 0.0), (ts + 0.9, 0.08))
        bg = always_redraw(self.blocos(t0))
        chip = always_redraw(lambda: chip_lento(0.85, s="CÂMERA LENTA") if ts <= self.clk.get_value() < ts + 0.9 else
                             chip_lento(0.85, s="LOGO APÓS O DISPARO") if self.clk.get_value() >= ts + 0.9 else VMobject())
        nomes = ValueTracker(0.0)
        self.rt = self.rotulos(nomes)
        tl = tp = VMobject()
        self.add(bg)
        self.play(self.f3b.op.animate.set_value(1.0), run_time=0.3)
        self.add(chip)
        self.diz("num chão com atrito")
        self.play(FadeIn(self.lat), run_time=0.5)
        self.diz("o leve, de um quilograma")
        self.play(FadeIn(self.rt), nomes.animate.set_value(1.0), run_time=0.5)
        self.diz("e o pesado, de dois")
        self.play(nomes.animate.set_value(2.0), run_time=0.4)
        self.diz("O sentido positivo")
        self.play(FadeIn(self.eixo), run_time=0.6)
        d1 = Mc((r"v_1=-2\ \mathrm{m/s}", VEL), size=40)
        d2 = Mc((r"v_2=+1\ \mathrm{m/s}", VEL), size=40)
        na_conta(d1, 1.8); na_conta(d2, 1.15)
        sv = VGroup()                                                   # v6: as setas de velocidade vêm presas aos blocos (blocos())
        self.diz("a dois metros por segundo")
        self.play(FadeIn(d1, shift=0.1 * UP), run_time=0.6)
        self.diz("a um metro por segundo")
        self.play(FadeIn(d2, shift=0.1 * UP), run_time=0.6)
        pm = Mc((r"p_1=-2", MAG), ",", (r"\ p_2=+2\ \mathrm{kg\cdot m/s}", MAG), size=40)
        p0 = Mc((r"P", MAG), "=", "0", size=48)
        lg = txt("LOGO DEPOIS DO DISPARO", 18, color=DIM)
        na_conta(pm, 0.1); na_conta(p0, -0.75); na_conta(lg, -1.35)
        self.diz("Logo depois do disparo")
        self.play(FadeIn(p0, shift=0.1 * UP), FadeIn(lg), run_time=0.6)
        self.diz("menos dois de um lado")
        self.play(FadeIn(pm[0], shift=0.1 * UP), run_time=0.5)
        self.diz("mais dois do outro")
        self.play(FadeIn(pm[1:], shift=0.1 * UP), run_time=0.5)
        self.ate(0.97)
        chip.clear_updaters()
        self.bg, self.tl, self.sv = bg, VGroup(chip), sv
        self.nomes = nomes
        self.conta3 = VGroup(d1, d2, pm, p0, lg)

    # ── gráficos P(t) e P_Terra(t), no PALCO, logo abaixo dos blocos ───────────────────────────────────────
    def graficos(self):
        # empilhados com folga (≥ 0,4): P(t) em cima (−1,2 a +0,2), P_Terra(t) embaixo (−0,2 a +1,2); rótulos à esquerda dos eixos
        self.GP = Graf(-5.6, -1.4, 5.8, TMAX, -1.2, 0.2, 0.9, rot_y=tex(r"P", MAG, 32))
        self.GT = Graf(-5.6, -3.78, 5.8, TMAX, -0.2, 1.2, 0.9, rot_y=tex(r"P_{\text{Terra}}", MAG, 28))
        self.GP.ey.next_to(self.GP.pt(0, 0.1), LEFT, buff=0.18)
        self.GT.ey.next_to(self.GT.pt(0, 0.55), LEFT, buff=0.15)
        for G, ys in ((self.GP, (-1.0,)), (self.GT, (1.0,))):
            for y in ys:
                G.eixos.add(DashedLine(G.pt(0, y), G.pt(TMAX, y), dash_length=0.06).set_stroke(DIM, 1, opacity=0.4))
                G.eixos.add(tex(f"{y:+.1f}".replace(".", "{,}"), DIM, 22).next_to(G.pt(0, y), LEFT, buff=0.12))
        self.GP.eixos.add(tex(r"\mathrm{kg\cdot m/s}", DIM, 22).next_to(self.GP.pt(0, -0.42), LEFT, buff=0.12))

    def traco(self, G, fun, t0, cor=MAG, ponto=True):
        def f():
            t = self.tau(t0)
            g = VGroup()
            if t > 0:
                cv = G.curva(fun, 0.0, t, n=80, cor=cor)
                ts = np.linspace(0.0, t, 40)                      # v7 (2D+): área sob a curva em degradê e brilho na linha
                area = Polygon(*([G.pt(0.0, 0.0)] + [G.pt(x, fun(x)) for x in ts] + [G.pt(t, 0.0)])).set_stroke(width=0)
                area.set_fill(color=[escuro(cor, 0.85), cor], opacity=0.28).set_sheen_direction(DOWN if fun(t / 2) < 0 else UP).set_z_index(5)
                g.add(area, cv.copy().set_stroke(cor, 12, 0.12), cv)
                if ponto:
                    g.add(Dot(G.pt(t, fun(t)), radius=0.07, color=WHITE_).set_z_index(9))
            return g
        return always_redraw(f)

    # ── T9-4: massas iguais (o evento uma vez) ────────────────────────────────────────────────────────────
    def t9_4(self):
        self.an("T9-4")
        self.graficos()
        self.bg.clear_updaters()
        self.play(FadeOut(self.bg), FadeOut(self.tl), FadeOut(self.sv), FadeOut(self.conta3), FadeOut(self.rt), self.bop.animate.set_value(0.0),
                  run_time=0.3)
        self.remove(self.bg)
        self.rt = self.rotulos()
        t0 = self.clk.get_value()
        ts, tf = self.clk_de("T9-4", "Os blocos saem", 0.1), self.clk_de("T9-4", "os dois param juntos", 0.1)
        self.warp(t0, (ts, 0.0), (tf, 1.5 / AF), (tf + 0.6, TMAX))
        bi = always_redraw(self.blocos(t0, iguais=True, forcas=True))
        cu = self.traco(self.GP, lambda t: 0.0, t0)
        lento = chip_lento()
        tit = txt("MASSAS IGUAIS", 26, bold=True)
        r1 = txt("ATRITOS IGUAIS E OPOSTOS", 20, color=FC)
        r0 = Mc((r"P(t)", MAG), "=", "0", size=44)
        r2 = txt("PARAM JUNTOS", 20, color=DIM)
        for m_, y in ((tit, 1.8), (r1, 1.15), (r0, 0.2), (r2, -0.45)):
            na_conta(m_, y)
        self.play(FadeIn(bi), FadeIn(cu), FadeIn(tit), FadeIn(self.GP.eixos), FadeIn(lento), self.bop.animate.set_value(1.0), run_time=0.3)
        self.add(self.rt)
        self.diz("os atritos também são iguais")
        self.play(FadeIn(r1), run_time=0.6)
        self.diz("o momento total fica zero")
        self.play(FadeIn(r0, shift=0.1 * UP), run_time=0.6)
        while self.tau(t0) < 1.5 / AF:
            self.wait(1 / FPS)
        self.play(FadeOut(lento), FadeIn(r2), run_time=0.5)
        self.ate(0.95)
        bi.clear_updaters(); cu.clear_updaters()
        self.play(FadeOut(bi), FadeOut(cu), FadeOut(VGroup(tit, r1, r0, r2)), FadeOut(self.rt), self.bop.animate.set_value(0.0), run_time=0.3)
        self.remove(bi, cu)
        self.rt = self.rotulos()

    # ── T9-5, T9-6: massas diferentes (o evento uma vez, sincronizado), P(t) ─────────────────────────────────
    def t9_5_6(self):
        self.an("T9-5")
        acende = ValueTracker(0.0)
        bg0 = always_redraw(self.blocos(None))
        d = MathTex(r"m_1=1\ \mathrm{kg},\ m_2=2\ \mathrm{kg},\ \mu=0{,}2", font_size=34, color=WHITE_)
        f1 = linha("ATRITO NO LEVE", tex(r"+1{,}96\ \mathrm{N}", FC, 36), size=20, buff=0.2)
        f2 = linha("ATRITO NO PESADO", tex(r"-3{,}92\ \mathrm{N}", FC, 36), size=20, buff=0.2)
        f3 = linha("RESULTANTE", tex(r"-1{,}96\ \mathrm{N}", FC, 40), size=22, buff=0.2)
        for m_, y in ((d, 2.0), (f1, 1.2), (f2, 0.55), (f3, -0.2)):
            na_conta(m_, y)
        self.play(FadeIn(bg0), FadeIn(self.rt), self.bop.animate.set_value(1.0), run_time=0.3)
        self.diz("O coeficiente de atrito")
        self.play(FadeIn(d), run_time=0.6)
        self.diz("O bloco leve vai para a esquerda")
        t0 = self.t0p = self.clk.get_value()
        th, tl_ = self.clk_de("T9-6", "O pesado para primeiro", 0.1), self.clk_de("T9-6", "Quando o leve também para", -0.6)
        self.warp(t0, (t0 + 0.2, 0.0), (th, T2), (tl_, T1), (tl_ + 0.5, TMAX))
        bg0.clear_updaters(); self.remove(bg0)
        bg = always_redraw(self.blocos(t0, forcas=True, acende=acende))
        cu = self.traco(self.GP, P, t0)
        relog = always_redraw(lambda: mtex(rf"t={max(0.0, self.tau(t0)):.2f}".replace(".", "{,}") + r"\ \mathrm{s}", DIM, 28)
                              .move_to(P3(-4.7, 2.95)))
        lento = chip_lento()
        self.add(bg, cu)
        self.play(FadeIn(relog), FadeIn(lento), run_time=0.3)
        self.diz("aponta para a direita")
        self.play(FadeIn(f1), run_time=0.6)
        self.diz("aponta para a esquerda")
        self.play(FadeIn(f2), run_time=0.6)
        self.diz("A força externa resultante")
        self.play(FadeIn(f3[0], shift=0.1 * UP), run_time=0.5)
        self.diz("um vírgula noventa e seis newtons para a esquerda")
        self.play(FadeIn(f3[1:], shift=0.1 * UP), run_time=0.5)
        dc = txt("O MOMENTO TOTAL DESCE", 18, color=MAG)
        na_conta(dc, -0.85)
        self.diz("começa a descer")
        self.play(FadeIn(dc), run_time=0.5)
        self.ate(0.97)
        # T9-6 — o pesado para em 0,51 s (pico); o leve para em 1,02 s; depois tudo fica, e o pico acende com o pesado parado
        self.an("T9-6")
        pk = Dot(self.GP.pt(T2, -1.0), radius=0.075, color=WHITE_).set_z_index(9)
        tpk = self.clk.get_value()
        halo = always_redraw(lambda: Circle(radius=0.12 + 0.07 * (0.5 + 0.5 * math.sin(2 * PI * (self.clk.get_value() - tpk) / 1.6)),
                                            arc_center=self.GP.pt(T2, -1.0)).set_stroke(MAG, 3, 0.55).set_z_index(9))   # v7: o mínimo pulsa
        lpk = MathTex(r"(0{,}51\ \mathrm{s};\ -1{,}0)", font_size=24, color=WHITE_).next_to(pk, DOWN, buff=0.12)
        z = Dot(self.GP.pt(T1, 0.0), radius=0.075, color=WHITE_).set_z_index(9)
        lz = MathTex(r"(1{,}02\ \mathrm{s};\ 0)", font_size=24, color=WHITE_).next_to(z, UP, buff=0.12)
        r1 = linha(txt("PESADO PARA:", 20, color=DIM), tex(r"t=0{,}51\ \mathrm{s},\ P=-1{,}0", MAG, 34), buff=0.2)
        r2 = linha(txt("LEVE PARA:", 20, color=DIM), tex(r"t=1{,}02\ \mathrm{s},\ P=0", MAG, 34), buff=0.2)
        na_conta(r1, 1.1); na_conta(r2, 0.3)
        self.diz("O pesado para primeiro")
        self.play(FadeOut(VGroup(d, f1, f2, dc)), acende.animate.set_value(1.0), run_time=0.25)   # v7 (1.1): as linhas saem antes de a
        self.play(f3.animate.move_to(P3(XC0 + f3.width / 2, 2.0)), run_time=0.25)                 # RESULTANTE subir (nada se cobre)
        self.play(FadeIn(pk, scale=0.5), FadeIn(lpk), FadeIn(r1[0]), FadeIn(halo), run_time=0.6)
        self.diz("cinquenta e um centésimos")
        self.play(FadeIn(r1[1]), run_time=0.5)
        self.diz("o ponto mais baixo do gráfico")
        self.play(Indicate(pk, color=MAG, scale_factor=1.6), Indicate(lpk, color=WHITE_), acende.animate.set_value(0.0), run_time=0.9)
        self.diz("Quando o leve também para")
        while self.tau(t0) < T1 - 1e-6:
            self.wait(1 / FPS)
        self.play(FadeIn(z, scale=0.5), FadeIn(lz), FadeIn(r2), run_time=0.7)
        self.diz("ele volta a zero")
        self.play(Indicate(z, color=MAG, scale_factor=1.6), Indicate(lz, color=WHITE_), run_time=0.9)
        while self.tau(t0) < TMAX - 1e-6:
            self.wait(1 / FPS)
        self.play(FadeOut(lento), run_time=0.3)
        self.ate(0.97)
        self.bg, self.cu, self.relog = bg, cu, relog
        self.conta6 = VGroup(f3, r1, r2)
        self.marcas = VGroup(pk, lpk, z, lz)
        self.halo = halo

    # ── T9-7: a Terra (um replay desenha P_Terra; depois tudo fica) ──────────────────────────────────────
    def t9_7(self):
        self.an("T9-7")
        for m_ in (self.bg, self.cu, self.relog):
            m_.clear_updaters()
        self.diz("foi até menos um e voltou")
        self.play(Indicate(self.marcas[0], color=MAG, scale_factor=1.6), Indicate(self.marcas[1], color=WHITE_), run_time=0.9)
        self.diz("Para a Terra")
        self.play(FadeOut(self.conta6), FadeOut(self.lat), FadeIn(self.GT.eixos), run_time=0.7)
        self.diz("Com a Terra dentro do sistema")
        # replay para a frente: os blocos voltam ao começo (em sequência) e disparam de novo; o ponto de P corre sobre a curva já feita
        # e P_Terra(t) se desenha embaixo, espelhado
        self.play(FadeOut(self.bg), FadeOut(self.relog), FadeOut(self.rt), self.bop.animate.set_value(0.0), run_time=0.25)
        self.remove(self.bg, self.relog)
        self.rt = self.rotulos()
        t0 = self.clk.get_value()
        tdv = self.clk_de("T9-7", "e depois devolve", 0.0)
        self.warp(t0, (t0 + 0.3, 0.0), (tdv, T1), (tdv + 0.4, TMAX))
        bg = always_redraw(self.blocos(t0, forcas=True))
        pt = always_redraw(lambda: Dot(self.GP.pt(max(0.0, self.tau(t0)), P(max(0.0, self.tau(t0)))), radius=0.07, color=WHITE_)
                           .set_z_index(9))
        ct = self.traco(self.GT, lambda t: -P(t), t0)
        relog = always_redraw(lambda: mtex(rf"t={max(0.0, self.tau(t0)):.2f}".replace(".", "{,}") + r"\ \mathrm{s}", DIM, 28)
                              .move_to(P3(-4.7, 2.95)))
        rp = chip_replay()
        self.play(FadeIn(bg), FadeIn(pt), FadeIn(relog), FadeIn(rp), FadeIn(self.rt), self.bop.animate.set_value(1.0), run_time=0.25)
        self.add(ct)
        lt = txt("O CHÃO GANHA, DEPOIS DEVOLVE", 18, color=DIM)
        na_conta(lt, -0.9)
        GS = Graf(1.6, 0.9, 4.6, TMAX, -0.6, 0.6, 1.0, rot_y=None)
        ls = Mc((r"P+P_{\text{Terra}}", MAG), size=32).next_to(GS.pt(0, 0.6), UP, buff=0.12).align_to(GS.pt(0, 0), LEFT)
        soma = GS.curva(lambda t: P(t) - P(t), 0.0, TMAX, n=60, cor=WHITE_, w=5)
        z0 = Mc("=", "0", size=40).next_to(GS.pt(1.0, 0), UP, buff=0.2)
        at = txt("A TODO INSTANTE", 18, color=DIM).next_to(GS.pt(0.6, 0), DOWN, buff=0.45)
        self.diz("o momento total é zero")
        self.play(FadeIn(GS.eixos), FadeIn(ls), run_time=0.6)
        self.play(Create(soma), run_time=1.2)
        self.play(FadeIn(z0), FadeIn(at), run_time=0.5)
        self.diz("O gráfico de baixo")
        self.play(Indicate(self.GT.ey, color=WHITE_), run_time=0.8)
        self.diz("o chão ganha momento")
        self.play(FadeIn(lt), run_time=0.5)
        while self.tau(t0) < TMAX - 1e-6:
            self.wait(1 / FPS)
        self.play(FadeOut(rp), FadeOut(pt), run_time=0.3)
        self.diz("Então fica a dica")
        d = dica("NÃO CONSERVA? PERGUNTE QUEM", "FICOU DE FORA DO SISTEMA")
        self.dica_entra(d)
        self.sobra(0.55)
        for m_ in (bg, relog, ct, self.rt, self.halo):
            m_.clear_updaters()
        self.clear(rt=0.5)

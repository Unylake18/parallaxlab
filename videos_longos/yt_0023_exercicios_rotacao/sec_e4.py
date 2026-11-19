"""Lote PE4 (v2): E4-1 a E4-10 — o pêndulo de discos em Three.js (discos de aço com chanfro e aresta, haste leve, pino no eixo, garfo);
física e alinhamento na frontal (E4-1 abre em 3/4 e faz o dolly). O pêndulo simples de comparação fica 2D (bolinha rosa e fio GEO).
Escala: 1 m = 10 u (R = 1,0 u: cada disco ≥ 22% da altura). Período T em branco.
Álgebra do zero (v2 §2): Στ = Iα → α = −(g/l) sen θ com m e l cancelando; I = Σ Iᵢ com Steiner → M(R² + l²); 2M·l/2 → Ml;
l_eq = I/(M d) → (R² + l²)/l; l_eq = l + R²/(2l); derivada por glyph map; produto fixo l·l' = R²/2."""
from pecas23 import *  # noqa: F401,F403
from pecas23b import mancal25, pino25, AÇO_ESC

S = 12.0              # v6: discos maiores (R = 1,2 u = 27% da altura); o E4-5 em diante usa S = 14
R_ = 0.10
AMP = math.radians(5.0)
W_ = WHITE_
XC, YC = -5.0, -0.4                 # alvo da câmera (frontal: tela = S·(x, z) exatamente)


def cam_pend(u):
    s = smooth(clamp(u, 0, 1))
    alvo = [XC / S, 0.0, YC / S]
    if s >= 0.9999:
        return cam_obl(-90.0, 0.0, alvo, K=S, xc=XC, yc=YC, fov=FOV3)
    return cam_obl(-62.0 - 28.0 * s, 14.0 * (1 - s), alvo, K=S, xc=XC, yc=YC, fov=FOV3)


def disco_pend(o, l, ang, duplo=False, cm=False):
    """Marcas 2D por cima do pêndulo 3D: centro do disco de baixo e o ⊕ (o disco, a haste, o pino e o garfo são do Three.js)."""
    o = np.asarray(o, float)
    u = np.array([math.sin(ang), -math.cos(ang), 0.0])
    c = o + S * l * u
    g = VGroup(Dot(c, radius=0.05, color=WHITE_).set_z_index(13))
    if cm:
        g.add(marcador_cm(o + S * l / 2 * u, r=0.15, z=16))
    return g


def disco25(c, ang, R=None):
    """v5 §1.3: disco de aço 2.5D frontal (azul-aço escuro, aro claro, marca de giro)."""
    c = np.asarray(c, float)
    R = S * R_ if R is None else R
    g = VGroup(Circle(radius=R).move_to(c).set_fill(AÇO_FRIO, 1).set_stroke(AÇO_ARESTA, 3.0),
               Circle(radius=R * 0.86).move_to(c).set_fill(AÇO_ESC, 0.55).set_stroke(AÇO_ARESTA, 1.4, opacity=0.4),
               Line(c + 0.38 * R * np.array([math.cos(ang + 0.5), math.sin(ang + 0.5), 0]), c + 0.84 * R * np.array([math.cos(ang + 0.5), math.sin(ang + 0.5), 0])).set_stroke(AÇO_CLARO, 3.0, opacity=0.85),
               Circle(radius=R * 0.14).move_to(c).set_fill("#5B6B8C", 1).set_stroke(AÇO_CLARO, 1.8))
    return g


def pend25(o, l, ang, duplo=True):
    """Pêndulo 2.5D: haste leve do pino ao centro do disco de baixo; o disco de cima (se houver) no próprio pino; mancal fixo."""
    o = np.asarray(o, float)
    u = np.array([math.sin(ang), -math.cos(ang), 0.0])
    c = o + S * l * u
    g = VGroup(mancal25(o, 3))
    if l > 0.01:
        g.add(Line(o, c).set_stroke(HALO, 8).set_z_index(3.4), Line(o, c).set_stroke("#8FA6C9", 4.5).set_z_index(3.5))
    if duplo:
        g.add(disco25(o, ang).set_z_index(4))
    g.add(disco25(c, ang).set_z_index(4.2), pino25(o, 0.12, 4.8))
    return g


def simples(o, l, ang, cor=MAS):
    o = np.asarray(o, float)
    u = np.array([math.sin(ang), -math.cos(ang), 0.0])
    c = o + S * l * u
    return VGroup(Line(o, c).set_stroke(GEO, 2.4), Dot(c, radius=0.14, color=cor), pino(o, 0.08, z=14)).set_z_index(6)


class Fase:
    """Fase acumulada 2π∫dt/T(l(t)) quadro a quadro (o período muda com a posição do eixo)."""

    def __init__(self, cena, per):
        self.c, self.per, self.ph, self.t0 = cena, per, 0.0, cena.clk.get_value()

    def ang(self, amp=AMP):
        t = self.c.clk.get_value()
        self.ph += 2 * math.pi * (t - self.t0) / self.per()
        self.t0 = t
        return amp * math.cos(self.ph)


class LoteE4(Lote23):
    def corpo(self):
        global S
        S = 12.0
        O1 = P3(-5.0, 1.6)
        T2 = periodo(0.30, duplo=True)
        leq2 = (R_ ** 2 + 0.3 ** 2) / 0.3
        t0 = self.clk.get_value()
        ang2 = lambda: AMP * math.cos(2 * math.pi * (self.clk.get_value() - t0) / T2)
        flags = dict(cm=False, pesos=False, ov=False)
        ucam = ValueTracker(0.0)
        self.add(ucam)
        self.pend_fn = lambda: [(O1, 0.30, ang2(), True)]

        def est(t):
            lst = self.pend_fn()
            e = {"p": [[float(o[0]) / S, float(o[1]) / S, float(l), float(a), int(d)] for o, l, a, d in lst], "cam": cam_pend(ucam.get_value())}
            if not PEDIDOS3D and lst:
                o, l, a, _ = lst[0]
                u = np.array([math.sin(a), -math.cos(a), 0.0])
                self.reg("pendulo", eixo=[float(o[0]), float(o[1])], disco=[float((o + S * l * u)[0]), float((o + S * l * u)[1])], u=ucam.get_value())
            return r4(e)

        f3 = Fundo3D(self, "pendulo", est, op=0.0)
        self.add(f3)
        sw = {"t": None}                                       # v5 §1.3: depois do dolly o 3D cede lugar ao 2.5D (mesma posição: tela = S·(x, z))
        f3.mult = lambda t: 1.0 if sw["t"] is None else 1.0 - clamp((t - sw["t"]) / 0.4, 0.0, 1.0)

        def camada25():
            g = VGroup()
            o25 = (0.0 if sw["t"] is None else clamp((self.clk.get_value() - sw["t"]) / 0.4, 0.0, 1.0)) * f3.op.get_value()
            if o25 < 0.01:
                return g
            for o, l, a, d in self.pend_fn():
                g.add(pend25(o, l, a, d))
            if o25 < 0.999:
                escala_op(g, o25)
            return g

        p25 = vivo(camada25)
        self.add(p25)

        def cena2():
            a = ang2()
            g = VGroup()
            if not flags["ov"]:
                return g
            g.add(disco_pend(O1, 0.30, a, duplo=True, cm=flags["cm"]))
            u = np.array([math.sin(a), -math.cos(a), 0.0])
            c = O1 + S * 0.3 * u
            if not flags["pesos"]:
                rim = c + S * R_ * np.array([math.cos(-0.5), math.sin(-0.5), 0.0])
                g.add(circ_raio(c, S * R_, C_RAIO, 4.0, tracejado=True), linha_halo(c, rim, cor=C_RAIO, w=4.0), linha_halo(rim, c + P3(1.42, -0.82), cor=C_RAIO, w=1.8))
                g.add(lbl("M", MAS, 42).move_to(c + P3(-(S * R_ + 0.45), 0.0)), lbl("R", C_RAIO, 42).move_to(c + P3(1.7, -0.9)), lbl("M", MAS, 42).move_to(O1 + P3(-(S * R_ + 0.45), 0.0)),
                      lbl("l", C_RAIO, 42).move_to(O1 + S * 0.15 * u + 0.4 * RIGHT))
            else:
                g.add(seta_s(c + 0.1 * DOWN, c + 1.3 * DOWN, FC, 6), lbl("Mg", FC, 40).next_to(c + 1.3 * DOWN, RIGHT, buff=0.2),
                      seta_s(O1 + 0.15 * DOWN, O1 + 1.3 * DOWN, FC, 5), chamada23(O1, VGroup(txt("BRAÇO", 26, bold=True, color=GEO), txt("ZERO", 26, bold=True, color=GEO)).arrange(DOWN, buff=0.05), RIGHT + 0.25 * UP, 2.0))     # v7: entre o disco e o fio (antes: sobre o título)
            return g

        dv = vivo(cena2)
        self.add(dv)

        # ── E4-1: os dois discos em 3/4 (garfo, eixo, pino); dolly até a frontal ──
        self.an("E4-1")
        self.secao("EXERCÍCIO 4 · O PÊNDULO MAIS RÁPIDO")
        self.play(f3.op.animate.set_value(1.0), run_time=0.6)
        self.gat("dois discos iguais")
        d1 = VGroup(txt("DOIS DISCOS IGUAIS:", 30, bold=True, color=GEO), lbl("M", MAS, 44), txt("E", 30), lbl("R", C_RAIO, 44)).arrange(RIGHT, buff=0.18)
        self.pilha.poe(d1)
        self.play(FadeIn(d1, shift=0.08 * UP), run_time=0.5)
        self.gat("o de cima é preso ao eixo pelo centro")
        d2 = txt("O DE CIMA: EIXO NO CENTRO", 30, bold=True, color=GEO)
        self.pilha.poe(d2)
        self.play(FadeIn(d2, shift=0.08 * UP), ucam.animate.set_value(1.0), run_time=1.4)
        flags["ov"] = True
        sw["t"] = self.clk.get_value()
        self.gat("com os centros a uma certa distância")
        d3 = VGroup(txt("CENTROS A", 30, bold=True, color=GEO), lbl("l", C_RAIO, 44)).arrange(RIGHT, buff=0.18)
        self.pilha.poe(d3)
        self.play(FadeIn(d3, shift=0.08 * UP), run_time=0.5)
        self.gat("qual é o período das oscilações pequenas")
        self.selo("O QUE ESTE PEDE", "O PERÍODO PARA ÂNGULOS PEQUENOS")
        self.ate(0.99)

        # ── E4-2: pêndulo simples: Στ = Iα → ml²α = −mgl sen θ → α = −(g/l) sen θ → T = 2π√(l/g) ──
        self.an("E4-2")
        self.pilha.limpa()
        OS = P3(-1.5, 1.6)
        lm_ = lbl("m", MAS, 40)
        ll_ = lbl("l", C_RAIO, 40)

        def simp():
            a = ang2()
            u = np.array([math.sin(a), -math.cos(a), 0.0])
            c = OS + S * leq2 * u
            return VGroup(simples(OS, leq2, a), lm_.copy().move_to(c + 0.5 * RIGHT), ll_.copy().move_to(OS + S * leq2 / 2 * DOWN + 0.35 * RIGHT),
                          seta_s(c + 0.2 * DOWN, c + 1.2 * DOWN, FC, 5), lbl("mg", FC, 40).next_to(c + 1.2 * DOWN, RIGHT, buff=0.2))

        ps = vivo(simp)
        self.gat("uma bolinha na ponta de um fio")
        self.play(FadeIn(ps), run_time=0.6)
        self.gat("uma bolinha na ponta de um fio")
        L0, il0, _ = self.lei("newton_rot", (r"\sum", r"\tau", "=", "I", r"\alpha"), rt=0.9)
        A, ia, _ = self.gm(L0, il0, (r"\tau", "=", "-", "m", "g", "l", r"\operatorname{sen}\theta"), sai=[0, 3, 4], voos={3: ps[0][1], 4: ps[0][4][0][1], 5: ps[0][2]}, rt=1.3)
        self.gat("o momento de inércia dela")
        B, ib, _ = self.linha(("I", "=", "m", "l^2"), voos={2: ps[0][1], 3: ps[0][2]}, rt=1.0)
        C, ic, _ = self.gm(L0, il0, ("m", "l^2", r"\alpha", "=", "-", "m", "g", "l", r"\operatorname{sen}\theta"), sai=[0, 1, 3],
                           voos={0: mp(B, ib, [2]), 1: mp(B, ib, [3]), 4: mp(A, ia, [2]), 5: mp(A, ia, [3]), 6: mp(A, ia, [4]), 7: mp(A, ia, [5]), 8: mp(A, ia, [6])}, rt=1.4)
        D, idd, _ = self.gm(C, ic, (r"\alpha", "=", "-", r"\tfrac{g}{l}", r"\operatorname{sen}\theta"), riscar=[0, 5, 7], mapas=[([6, 1], [3])], rt=1.3)
        self.gat("para ângulos pequenos")
        self.selo("ÂNGULOS PEQUENOS", [[lbl(r"\operatorname{sen}\theta\approx\theta", ANG, 40)]])
        E, ie, _ = self.gm(D, idd, (r"\alpha", r"\approx", "-", r"\tfrac{g}{l}", r"\theta"), mapas=[([1], [1]), ([4], [4])], rt=1.1)
        self.gat("o período é dois pi vezes")
        F, if_, fb = self.lei("pendulo", ("T", "=", r"2\pi", r"\sqrt{\tfrac{l}{g}}"), cores={0: W_}, size=52, rt=1.1, caixa_cor=GEO)
        self.gat("é só usar esse comprimento equivalente")
        G_, ig_, _ = self.linha(("l", r"\ \rightarrow\ ", "l_{eq}"), size=48, rt=0.8)
        self.ate(0.99)

        # ── E4-3: I = Σ Iᵢ (Steiner do cartão) → M(R² + l²); τ do ⊕; 2M·l/2 → Ml; l_eq → (R² + l²)/l; T = 1,159 s ──
        self.an("E4-3")
        self.sem_selo()
        self.pilha.limpa()
        self.gat("o torque vem só do disco de baixo")
        flags["pesos"] = True
        T0, it0, t0b = self.linha((r"\tau", "=", "-", "M", "g", "l", r"\operatorname{sen}\theta"), rt=1.1)
        self.gat("já o momento de inércia tem os dois")
        flags["pesos"] = False
        S0, is0, _ = self.linha(("I", "=", r"\sum", "I_i"), rt=0.8)
        self.cartao_lei("steiner")
        S1, is1, _ = self.gm(S0, is0, ("I", "=", r"\tfrac{1}{2}", "M", "R^2", "+", "(", r"\tfrac{1}{2}", "M", "R^2", "+", "M", "l^2", ")"),
                             mapas=[([2, 3], [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13])], voos={12: ll_}, rt=1.5)
        self.card_sai()
        S2, is2, s2b = self.gm(S1, is1, ("I", "=", "M", r"(R^2+l^2)"), mapas=[([3, 8, 11], [2]), ([2, 4, 5, 6, 7, 9, 10, 12, 13], [3])], cores={2: MAS}, caixa_cor=MAS, rt=1.2)
        self.gat("a massa total é o dobro")
        flags["cm"] = True
        self.pilha.so(t0b, s2b)
        D0, id0, _ = self.linha(("M_{total}", "d_{CM}", "=", "2", "M", r"\cdot", r"\tfrac{l}{2}"), rt=1.2)
        D1, id1, d1b = self.gm(D0, id0, ("M_{total}", "d_{CM}", "=", "M", "l"), riscar=[3], mapas=[([6], [4])], sai=[5], rt=1.1)
        self.gat("dividindo o momento de inércia por isso")
        self.pilha.so(s2b, d1b)
        E0, ie0, _ = self.linha({"pre": ("l_{eq}", "="), "num": ("I",), "den": ("M_{total}", "d_{CM}")}, rt=1.0, metodo="lei")
        E1, ie1, _ = self.gm(E0, ie0, {"pre": ("l_{eq}", "="), "num": ("M", r"(R^2+l^2)"), "den": ("M", "l")}, sai=[2, 4, 5],
                             voos={2: mp(S2, is2, [2]), 3: mp(S2, is2, [3]), 5: mp(D1, id1, [3]), 6: mp(D1, id1, [4])}, rt=1.3)
        E2, ie2, e2b = self.gm(E1, ie1, {"pre": ("l_{eq}", "="), "num": (r"R^2+l^2",), "den": ("l",)}, riscar=[2, 5], mapas=[([3], [2])], caixa_cor=GEO, rt=1.2)
        self.gat("o período dá um vírgula um seis")
        self.pilha.so(e2b)
        F0, if0, _ = self.lei("pendulo", ("T", "=", r"2\pi", r"\sqrt{\frac{R^2+l^2}{g\,l}}"), cores={0: W_}, rt=1.2)
        F1, if1, _ = self.gm(F0, if0, ("T", "=", r"2\pi", r"\sqrt{\frac{0{,}01+0{,}09}{9{,}8\cdot 0{,}30}}", "=", r"1{,}159\ \mathrm{s}"), sai=[3],
                             cores={0: W_, 5: W_}, caixa_cor=GEO, rt=1.4)
        self.gat("e o pêndulo simples equivalente")
        tl = lbl(r"l_{eq}=0{,}333\ \mathrm{m}", C_RAIO, 40).move_to(OS + P3(0.4, 0.6))
        self.play(FadeIn(tl), self.ind_copia(ps[0][0], None, 1.04, 0.9), run_time=0.9)
        self.ate(0.99)

        # ── E4-4: com × sem o disco de cima, soltos juntos do repouso ──
        self.an("E4-4")
        self.selo("SOLTOS JUNTOS", "DO REPOUSO · DO MESMO ÂNGULO")
        self.card_sai()
        self.pilha.limpa(anims=[FadeOut(dv), FadeOut(ps), FadeOut(tl), f3.op.animate.set_value(0.0)])
        Oa, Ob = P3(-5.6, 1.6), P3(-2.3, 1.6)
        Ta, Tb = T2, periodo(0.30)
        t1 = [None]

        def angs():
            if t1[0] is None:
                return AMP, AMP
            dt = self.clk.get_value() - t1[0]
            return AMP * math.cos(2 * math.pi * dt / Ta), AMP * math.cos(2 * math.pi * dt / Tb)

        self.pend_fn = lambda: [(Oa, 0.30, angs()[0], True), (Ob, 0.30, angs()[1], False)]

        def par():
            a, b = angs()
            return VGroup(disco_pend(Oa, 0.30, a, duplo=True), disco_pend(Ob, 0.30, b, duplo=False))

        rot_cs = VGroup(VGroup(txt("COM:", 30, bold=True, color=GEO), lbl(r"1{,}159\ \mathrm{s}", W_, 42)).arrange(RIGHT, buff=0.15).move_to(Oa + P3(0, -5.3)),
                        VGroup(txt("SEM:", 30, bold=True, color=GEO), lbl(r"1{,}129\ \mathrm{s}", W_, 42)).arrange(RIGHT, buff=0.15).move_to(Ob + P3(0, -5.3)))
        pv = vivo(par)
        self.play(FadeIn(pv), f3.op.animate.set_value(1.0), run_time=0.4)
        self.play(FadeIn(rot_cs), run_time=0.25)        # R4-v9: rótulo só depois do objeto inteiro
        self.gat("solta dois pêndulos juntos")
        t1[0] = self.clk.get_value()
        self.gat("soma momento de inércia")
        A, ia, _ = self.linha((r"I_{cima}", "=", r"\tfrac{1}{2}", "M", "R^2", r",\quad", r"\tau_{cima}", "=", "0"), size=46, rt=1.2)
        self.gat("sem ele o período cai")
        B, ib, _ = self.linha((r"T_{sem}", "=", r"1{,}129\ \mathrm{s}"), cores={0: W_, 2: W_}, size=50, rt=1.0, caixa_cor=GEO)
        self.ate(0.99)

        # ── E4-5 a E4-9: um disco só, eixo deslizando; gráfico T(l) ──
        self.an("E4-5")
        self.sem_selo()
        S = 11.5
        lt = ValueTracker(0.30)
        self.add(lt)
        OE = P3(-4.3, 2.0)
        fase = Fase(self, lambda: periodo(max(0.012, lt.get_value())))
        estado = dict(cota=True)
        self.pend_fn = lambda: [(OE, max(0.0, lt.get_value()), fase.ang(math.radians(4)), False)]

        def um():
            l = lt.get_value()
            a = fase.ang(math.radians(4))
            g = VGroup(disco_pend(OE, l, a))
            if estado["cota"]:
                g.add(Line(OE + (S * R_ + 0.3) * RIGHT, OE + (S * R_ + 0.3) * RIGHT + S * l * DOWN).set_stroke(GEO, 2.4),
                      lbl("l", C_RAIO, 42).move_to(OE + (S * R_ + 0.65) * RIGHT + S * l / 2 * DOWN))
            return g

        um_ = vivo(um)
        self.pilha.limpa(anims=[FadeOut(pv), FadeOut(rot_cs), f3.op.animate.set_value(0.0)])
        self.play(FadeIn(um_), f3.op.animate.set_value(1.0), run_time=0.5)
        gx0, gy0, gw, gh = 1.35, -3.15, 5.0, 1.95
        pg = lambda l, T_: P3(gx0 + gw * (l - 0.02) / 0.38, gy0 + gh * (T_ - 0.70) / 0.60)
        ax = VGroup(Line(pg(0.02, 0.70), pg(0.40, 0.70)).set_stroke(GEO, 2), Line(pg(0.02, 0.70), pg(0.02, 1.30) + 0.1 * UP).set_stroke(GEO, 2),
                    lbl("T", W_, 40).move_to(pg(0.02, 1.30) + 0.35 * LEFT), VGroup(lbl("l", C_RAIO, 40), txt("(CM)", 30, color=GEO)).arrange(RIGHT, buff=0.08).next_to(pg(0.40, 0.70), UP, buff=0.12)).set_z_index(10)
        for v, s in ((0.10, "10"), (0.20, "20"), (0.30, "30"), (0.40, "40")):
            ax.add(Line(pg(v, 0.70), pg(v, 0.70) + 0.1 * DOWN).set_stroke(GEO, 2))
            ax.add(txt(s, 30, color=GEO).move_to(pg(v, 0.70) + 0.36 * DOWN))
        curva = VMobject().set_points_as_corners([pg(l, periodo(l)) for l in np.linspace(0.026, 0.40, 200)]).set_stroke(W_, 3.5).set_z_index(11)

        def pto_():
            l = clamp(lt.get_value(), 0.026, 0.4)
            d = Dot(pg(l, periodo(l)), radius=0.08, color=ANG).set_z_index(13)
            self.reg("curva", l=l, T=periodo(l), ponto=d.get_center(), eixo_y=float(OE[1]), centro_y=float(OE[1] - S * lt.get_value()))
            return d

        pto = vivo(pto_)
        self.gat("com o eixo a uma certa distância do centro")
        self.play(lt.animate.set_value(0.15), run_time=2.0)
        self.play(lt.animate.set_value(0.30), run_time=1.6)
        self.gat("onde pôr o eixo para o período ser o menor possível")
        self.selo("PROJETO", "ONDE PÔR O EIXO? PERÍODO MÍNIMO")
        self.pilha.base = -0.85
        q = VGroup(txt("ONDE PÔR O EIXO?", 32, bold=True), txt("PERÍODO MÍNIMO", 30, bold=True, color=CYAN)).arrange(DOWN, buff=0.1)
        self.pilha.poe(q)
        self.play(FadeIn(q, shift=0.08 * UP), run_time=0.5)
        self.ate(0.99)

        # E4-6: I = ½MR² + Ml² (Steiner) → l_eq = I/(Ml) → l + R²/(2l) (M cancela)
        self.an("E4-6")
        self.sem_selo()
        self.pilha.limpa()
        self.gat("o momento de inércia é metade da massa")
        St, ist, _ = self.lei("steiner", ("I", "=", r"I_{cm}", "+", "M", "D^2"), rt=0.8)
        A, ia, _ = self.gm(St, ist, ("I", "=", r"\tfrac{1}{2}", "M", "R^2", "+", "M", "l^2"), mapas=[([2], [2, 3, 4]), ([5], [7])], rt=1.2)
        self.gat("o comprimento equivalente fica")
        B0, ib0, _ = self.linha({"pre": ("l_{eq}", "="), "num": (r"\tfrac{1}{2}MR^2+Ml^2",), "den": ("M", "l")}, voos={2: mp(A, ia, [2, 3, 4, 5, 6, 7])}, rt=1.2)
        B, ib, bb = self.gm(B0, ib0, ("l_{eq}", "=", "l", "+", r"\frac{R^2}{2\,l}"), mapas=[([2, 3, 4, 5], [2, 3, 4])], caixa_cor=GEO, rt=1.3)
        self.play(FadeIn(ax), Create(curva), FadeIn(pto), run_time=1.0)
        self.gat("eixo muito longe")
        self.play(lt.animate.set_value(0.40), run_time=1.6)
        self.pilha.so(bb)
        L1, _, _ = self.linha(("l", r"\gg", "R", r":\ ", "l_{eq}", r"\approx", "l"), size=46, rt=0.9)
        self.gat("eixo quase no centro")
        self.play(lt.animate.set_value(0.03), run_time=2.2)
        L2, _, _ = self.linha(("l", r"\to", "0", r":\ ", "T", r"\to", r"\infty"), cores={4: W_}, size=46, rt=0.9)
        self.gat("tem que haver um mínimo")
        self.play(lt.animate.set_value(0.2), run_time=2.0)
        self.ate(0.99)

        # E4-7: três caminhos em sequência (derivada por glyph map; produto fixo; a curva)
        self.an("E4-7")
        self.selo("TRÊS CAMINHOS", "UMA RESPOSTA")
        self.pilha.so(bb)
        self.gat("primeiro a derivada")
        D1, id1, _ = self.gm(B, ib, (r"\frac{d\,l_{eq}}{d\,l}", "=", "1", "-", r"\frac{R^2}{2\,l^2}", "=", "0"), mapas=[([0], [0]), ([2], [2]), ([3], [3]), ([4], [4])], rt=1.3)
        self.gat("a distância é o raio sobre raiz de dois")
        self.play(lt.animate.set_value(0.1 / math.sqrt(2)), run_time=1.6)
        R1, ir1, rb = self.gm(D1, id1, ("l", "=", r"\frac{R}{\sqrt{2}}"), mapas=[([4], [2])], caixa_cor=GEO, rt=1.1)
        self.gat("segundo sem derivada")
        self.pilha.so(bb, rb)
        D2, id2, _ = self.gm(B, ib, ("l", r"\cdot", r"\frac{R^2}{2\,l}", "=", r"\frac{R^2}{2}"), mapas=[([2], [0]), ([3], [1]), ([4], [2])], sai=[0, 1], rt=1.2)
        self.gat("é mínima quando eles são iguais")
        D3, id3, _ = self.gm(D2, id2, ("l", "=", r"\frac{R^2}{2\,l}", r"\ \Rightarrow\ ", "l", "=", r"\frac{R}{\sqrt{2}}", r"\ \checkmark"), mapas=[([1], [1]), ([3], [3])], cores={7: ACC}, rt=1.2)
        self.gat("terceiro a curva do período")
        self.pilha.so(rb)
        self.play(lt.animate.set_value(0.30), run_time=1.2)
        self.play(lt.animate.set_value(0.1 / math.sqrt(2)), run_time=2.2)
        mn = VGroup(DashedLine(pg(0.0707, 0.70), pg(0.0707, periodo(0.0707)), dash_length=0.06).set_stroke(ANG, 2.5),
                    lbl(r"0{,}755\ \mathrm{s}", W_, 36).next_to(pg(0.0707, periodo(0.0707)), UP + 0.4 * RIGHT, buff=0.35)).set_z_index(12)
        self.gat("sete vírgula zero sete centímetros")
        self.play(FadeIn(mn), run_time=0.5)
        self.gat("período mínimo")
        Tm, itm, tmb = self.lei("pendulo", ("T_{min}", "=", r"2\pi", r"\sqrt{\tfrac{\sqrt{2}\,R}{g}}"), cores={0: W_}, rt=1.1)
        Tm2, itm2, tmb2 = self.gm(Tm, itm, ("T_{min}", "=", r"0{,}755\ \mathrm{s}"), cores={0: W_, 2: W_}, caixa_cor=GEO, rt=1.0)
        self.ate(0.99)

        # E4-8: 5 cm e 10 cm com o mesmo período: l·l' = R²/2 (os dois termos voam para o produto)
        self.an("E4-8")
        self.sem_selo()
        self.card_sai()
        self.pilha.limpa(anims=[FadeOut(um_), FadeOut(mn), f3.op.animate.set_value(0.0)])
        Oa, Ob = P3(-5.6, 2.0), P3(-2.4, 2.0)
        Tq = periodo(0.05)
        tq0 = self.clk.get_value()
        angq = lambda: math.radians(4) * math.cos(2 * math.pi * (self.clk.get_value() - tq0) / Tq)
        self.pend_fn = lambda: [(Oa, 0.05, angq(), False), (Ob, 0.10, angq(), False)]
        l5 = lbl(r"5\ \mathrm{cm}", C_RAIO, 42).move_to(Oa + P3(0, -(S * 0.05 + S * R_ + 0.6)))
        l10 = lbl(r"10\ \mathrm{cm}", C_RAIO, 42).move_to(Ob + P3(0, -(S * 0.10 + S * R_ + 0.6)))
        dois = vivo(lambda: VGroup(disco_pend(Oa, 0.05, angq()), disco_pend(Ob, 0.10, angq())))
        self.play(FadeIn(dois), FadeIn(l5), FadeIn(l10), f3.op.animate.set_value(1.0), run_time=0.6)
        p5 = VGroup(Dot(pg(0.05, periodo(0.05)), radius=0.08, color=ANG), Dot(pg(0.10, periodo(0.10)), radius=0.08, color=ANG),
                    DashedLine(pg(0.05, periodo(0.05)), pg(0.10, periodo(0.10)), dash_length=0.06).set_stroke(ANG, 2.5),
                    lbl(r"0{,}777\ \mathrm{s}", W_, 36).move_to(pg(0.075, periodo(0.05)) + 0.62 * UP)).set_z_index(13)
        self.gat("o período é o mesmo")
        self.play(FadeIn(p5), FadeOut(pto), run_time=0.6)
        self.gat("trocar a distância pelo raio ao quadrado")
        A, ia, _ = self.linha(("l", r"\cdot", "l'", "=", r"\frac{R^2}{2}"), voos={0: l5, 2: l10}, size=48, rt=1.1)
        self.gat("cinco vezes dez dá cinquenta")
        B, ib, _ = self.gm(A, ia, ("5", r"\cdot", "10", "=", "50", "=", r"\frac{10^2}{2}"), sai=[0, 2, 4], voos={0: l5, 2: l10}, cores={0: C_RAIO, 2: C_RAIO, 4: C_RAIO, 6: C_RAIO}, caixa_cor=GEO, rt=1.2)
        self.ate(0.99)

        # E4-9: eixo dentro do disco; faixa l < R hachurada (v7: o rótulo fica à direita da faixa, sobre a hachura nada); l = R → +3%
        self.an("E4-9")
        self.selo("CONFERE", "PERTO DO FUNDO, A CURVA É QUASE PLANA")
        self.pilha.limpa(anims=[FadeOut(dois), FadeOut(p5), FadeOut(l5), FadeOut(l10), f3.op.animate.set_value(0.0)])
        lt.set_value(0.1 / math.sqrt(2))
        fase.t0 = self.clk.get_value()
        self.pend_fn = lambda: [(OE, max(0.0, lt.get_value()), fase.ang(math.radians(4)), False)]
        self.play(FadeIn(um_), FadeIn(pto), f3.op.animate.set_value(1.0), run_time=0.5)
        self.gat("o eixo está dentro do disco")
        hach = VGroup(*[Line(pg(0.02 + 0.08 * k / 12, 1.30), pg(min(0.10, 0.02 + 0.08 * k / 12 + 0.036), 1.08)).set_stroke(GEO, 1.5) for k in range(12)])
        hach.add(Rectangle(width=gw * 0.08 / 0.38, height=gh).move_to((pg(0.02, 0.70) + pg(0.10, 1.30)) / 2).set_stroke(GEO, 1.5))
        lr_ = lbl("l<R", C_RAIO, 40).move_to(pg(0.165, 1.12))           # v6 #16: dentro da faixa hachurada, em pílula (longe da curva e dos traços)
        lr = VGroup(pilula(lr_, cor=C_RAIO, buff=0.08), lr_).set_z_index(15)
        hach.add(lr)
        self.play(FadeIn(hach), run_time=0.6)
        Al, ial, _ = self.linha(("l_{min}", "=", r"\tfrac{R}{\sqrt{2}}"), size=46, rt=0.9, metodo="lei")        # v5 LEI PRIMEIRO
        A, ia, _ = self.linha(("l_{min}", "=", r"7{,}07\ \mathrm{cm}", "<", "R"), cores={2: C_RAIO}, size=46, rt=1.1)
        eid = txt("EIXO DENTRO DO DISCO", 30, bold=True, color=GEO)
        self.pilha.poe(eid)
        self.play(FadeIn(eid), run_time=0.4)
        self.gat("a distância não pode ser menor que o raio")
        B, ib, _ = self.linha(("l", r"\ge", "R"), size=48, rt=0.8)
        self.gat("o eixo bem na borda")
        self.play(lt.animate.set_value(0.10), run_time=1.2)
        mR = VGroup(Dot(pg(0.10, periodo(0.10)), radius=0.09, color=ACC), lbl(r"0{,}777\ \mathrm{s}\ (+3\%)", W_, 36).move_to(pg(0.10, 1.33))).set_z_index(14)
        self.play(FadeIn(mR), run_time=0.5)
        C_, ic, _ = self.linha(("T(R)", "=", r"0{,}777\ \mathrm{s}", r"\ \ (+3\%)"), cores={0: W_, 2: W_}, size=46, rt=1.1, caixa_cor=GEO)
        self.gat("errar um pouco a posição do eixo")
        self.play(lt.animate.set_value(0.085), run_time=1.0)
        self.play(lt.animate.set_value(0.10), run_time=1.0)
        self.ate(0.99)

        # E4-10: dica
        self.an("E4-10")
        self.selo("DICA", "O RESTO É PÊNDULO SIMPLES")
        self.pilha.base = -3.25
        self.pilha.limpa(anims=[FadeOut(VGroup(ax, curva, pto, hach, mR))])
        self.gat("divide o momento de inércia em torno do eixo")
        A, ia, _ = self.linha({"pre": ("l_{eq}", "="), "num": ("I_{eixo}",), "den": ("M_{total}", "d_{CM}")}, size=56, rt=1.3, caixa_cor=GEO, metodo="lei")
        self.gat("esse é o comprimento equivalente")
        B, ib, _ = self.lei("pendulo", ("T", "=", r"2\pi", r"\sqrt{\tfrac{l_{eq}}{g}}"), cores={0: W_}, size=52, rt=1.0)
        self.ate(0.99)


def chamada23(p, rot, lado=RIGHT, d=1.2, cor=GEO):
    rot.move_to(p + d * lado)
    a = rot.get_edge_center(-lado) + 0.08 * (-lado)
    return VGroup(Line(a, p).set_stroke(cor, 2), rot).set_z_index(16)

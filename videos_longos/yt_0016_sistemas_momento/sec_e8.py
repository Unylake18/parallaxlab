"""Lote Q8 (v2): E8 — os gases do rifle. O tiro se repete no PALCO (bala, recuo, nuvem de gases) o exercício inteiro. Bala 7,20 g a 601 m/s em relação ao cano; rifle 2,80 kg recua a 1,85 m/s
em relação ao chão: v_bala = 599,15 m/s; p_bala = 4,31, p_rifle = −5,18, p_gases = +0,866 kg·m/s; sistema = bala + rifle + gases."""
from kit import *  # noqa: F401,F403

MB, MR, VREL, VR = 0.00720, 2.80, 601.0, 1.85
VB = VREL - VR
PB, PR = MB * VB, -MR * VR
PG = -(PB + PR)
assert abs(VB - 599.15) < 1e-9 and abs(PB - 4.314) < 1e-3 and abs(PR + 5.18) < 1e-9 and abs(PG - 0.866) < 1e-3
XR = 3.9
YR = 0.15                      # altura do cano (v6: palco ×1,4 e centralizado na altura)
SC, X0P, DXP = 1.4, -4.95, 0.8   # escala do PALCO, x do ponto fixo e o deslocamento (o rifle inteiro dentro do PALCO)


def M(x, y):
    """Ponto do desenho original (escala 1) → PALCO ampliado ×SC em torno de (X0P, YR)."""
    return P3(X0P + SC * (x - X0P) + DXP, YR + SC * (y - YR))
K = 0.35                       # u por kg·m/s no diagrama (v4: a de 0,866 fica legível e tudo cabe na CONTA)
# v7: rifle 3D (Three.js), câmera lateral levemente de 3/4; a boca do cano fica onde estava a do desenho 2D (−1,59; 0,31)
CAM_R = {"modo": "obl", "az": -82, "el": 10, "alvo": [-3.0, 0, 0], "K": 1.0, "xc": -3.0, "yc": -2.06, "fov": 14}


def _boca3d(alvo=(-1.5922, 0.3096)):
    xr, zb = -1.59, 2.38
    for _ in range(30):                        # dois passos de Newton numérico por eixo bastam; 30 por folga
        q = proj3d(CAM_R, (xr, 0, zb))
        xr += (alvo[0] - q[0]) * 0.9
        zb += (alvo[1] - q[1]) * 0.9
    return xr, zb


XR0, ZB = _boca3d()


def num(s, cor=WHITE_, size=M_LAB):
    return MathTex(s, font_size=size, color=cor)


class LoteE8(Base):
    def construct(self):
        self.setup_base(cap="EXERCÍCIO 8 · OS GASES DO RIFLE", selo="QUEM ESTÁ NO SISTEMA?")
        self.e8_1()
        self.e8_2()
        self.e8_3_4()
        self.fim()
        self.relatorio()

    def e8_1(self):
        self.an("E8-1")
        self.boca = proj3d(CAM_R, (XR0, 0, ZB))
        self.disparos, self.tw, self.nv0 = [], [], None
        self.f3d = Fundo3D(self, "rifle", self.est_rf, op=0.0)
        self.f3d.conta.set_value(1.0)
        self.add(self.f3d)
        la = txt("APOIO FROUXO", 15, color=DIM).move_to(M(-4.95, YR - 1.85))
        self.play(self.f3d.op.animate.set_value(1.0), run_time=0.9)
        rf = None
        self.rf = rf
        dados = VGroup(num(r"m_{\text{rifle}}=2{,}80\ \mathrm{kg}"), num(r"m_{\text{bala}}=7{,}20\ \mathrm{g}")) \
            .arrange(DOWN, buff=0.28, aligned_edge=LEFT).move_to(P3(XR, 1.75))
        self.diz("dois vírgula oito quilogramas")
        self.play(FadeIn(dados[0]), run_time=0.5)
        self.diz("num apoio frouxo")
        self.tw.append(self.clk.get_value())            # v7: a forquilha do bipé balança (articulação solta)
        self.play(FadeIn(la), run_time=0.8)
        self.diz("sete vírgula dois gramas")
        self.play(FadeIn(dados[1]), run_time=0.5)
        vb = arrow(self.boca + P3(0.1, 1.05), self.boca + P3(1.9, 1.05), color=VEL, width=6, tip=0.17)
        lb = num(r"601\ \mathrm{m/s}", VEL, 32).next_to(vb, UP, buff=0.08)
        rb = txt("EM RELAÇÃO AO CANO", 15, color=VEL).next_to(lb, UP, buff=0.06)
        vr = arrow(M(-5.3, YR + 0.6), M(-6.4, YR + 0.6), color=VEL, width=6, tip=0.17)
        lr = num(r"1{,}85\ \mathrm{m/s}", VEL, 30).next_to(vr, UP, buff=0.08)
        rr = txt("EM RELAÇÃO AO CHÃO", 15, color=VEL).next_to(lr, UP, buff=0.06)
        self.diz("A bala sai")
        self.loop_tiro()                 # v6 (1.2): o tiro (clarão e a bala em traço) no "A bala sai"; o rifle desliza para trás
        self.diz("seiscentos e um metros")
        self.play(GrowArrow(vb), FadeIn(lb), run_time=0.7)
        self.diz("em relação ao cano")
        self.play(FadeIn(rb), run_time=0.5)
        self.diz("um vírgula oitenta e cinco")
        self.play(GrowArrow(vr), FadeIn(lr), run_time=0.7)
        self.diz("em relação ao chão")
        self.play(FadeIn(rr), run_time=0.5)
        pg = txt("OS GASES CARREGAM MOMENTO?", 22).move_to(P3(XR, 0.3))
        self.diz("Os gases da explosão")
        self.play(FadeIn(pg), run_time=0.6)
        self.play(pg.animate.scale(0.8).move_to(P3(7.3, 2.55), aligned_edge=RIGHT), run_time=0.7)   # v6 (1.2): fica no canto
        self.ate(0.97)
        self.dados, self.pg = dados, pg
        self.setas = VGroup(vb, lb, rb, vr, lr, rr)

    def recuo(self, s):
        return min(0.4, 0.08 * s + 0.1 * min(1.0, s / 0.15)) if s > 0.0 else 0.0

    def fase(self, tt=None):
        tt = self.clk.get_value() if tt is None else tt
        ds = [x for x in self.disparos if x <= tt + 1e-9]
        return (tt - ds[-1]) if ds else -1.0

    def est_rf(self, t):
        """v7: estado do rifle 3D. O rifle desliza para trás no apoio; a bala é um traço até a borda do PALCO; os gases (partículas no
        3D) saem de cada tiro; a forquilha balança depois de cada tiro e no "apoio frouxo"."""
        s = self.fase(t)
        xr = XR0 - self.recuo(s)
        bala = None
        if 0 <= s < 1.2:
            xb = XR0 + 0.3 + 3.2 * s
            if proj3d(CAM_R, (xb, 0, ZB))[0] < 0.55:
                bala = xb
        wob = 0.0
        for t0 in self.tw + self.disparos:
            if t0 <= t:
                wob += 0.1 * math.sin(2 * PI * (t - t0) / 0.7) * math.exp(-(t - t0) / 0.9)
        return {"xr": xr, "xr0": XR0, "xb0": XR0, "zb": ZB, "tiros": [round(t - x, 4) for x in self.disparos if x <= t + 1e-9],
                "bala": bala, "nv": None if self.nv0 is None or t < self.nv0 else round(t - self.nv0, 4), "wob": wob, "cam": CAM_R}

    def loop_tiro(self):
        """v4 (regra 1.2): o tiro roda uma vez (e um replay, em self.disparos). v7: tudo no 3D (rifle.js)."""
        self.disparos.append(self.clk.get_value())

    def e8_2(self):
        self.an("E8-2")
        self.play(FadeOut(self.dados), run_time=0.4)
        e1 = Mc((r"v_{\text{bala,chão}}", VEL), "=", "601", "-", (r"1{,}85", VEL), "=", (r"599{,}15\ \mathrm{m/s}", VEL), size=44)
        x0e = XC0 + 0.35                                 # v7 (1.1): folga da legenda EM RELAÇÃO AO CANO (no PALCO)
        if e1.width > 7.55 - x0e:
            e1.scale((7.55 - x0e) / e1.width)
        e1.move_to(P3(x0e + e1.width / 2, 1.85))
        n1 = txt("O CANO ANDA PARA TRÁS", 16, color=DIM).next_to(e1, DOWN, buff=0.16)
        self.diz("Os seiscentos e um são")
        self.play(Indicate(self.setas[2], color=WHITE_, scale_factor=1.15), run_time=0.9)       # v6 (1.2): EM RELAÇÃO AO CANO
        self.diz("o cano está andando para trás")
        self.play(Indicate(self.setas[5], color=WHITE_, scale_factor=1.15), run_time=0.9)       # EM RELAÇÃO AO CHÃO
        self.diz("a bala anda seiscentos e um")
        self.play(FadeIn(e1[:3], shift=0.1 * UP), run_time=0.7)
        self.diz("menos um vírgula oitenta e cinco")
        self.play(FadeIn(e1[3:5], shift=0.1 * UP), FadeIn(n1), run_time=0.7)
        self.diz("quinhentos e noventa e nove")
        self.play(FadeIn(e1[5:]), run_time=0.6)
        # diagrama do momento, ponta com cauda: bala (+4,31) e rifle (−5,18) não fecham
        # v4: cada rótulo na ponta livre da sua seta (buff 0,15); a linha do zero para antes deles
        self.O = O = P3(3.25, 0.05)                       # v5 (V16): o diagrama sobe; o Σp = 0 cabe embaixo dele
        ref = DashedLine(O + P3(0, 0.35), O + P3(0, -1.35), dash_length=0.07).set_stroke(DIM, 1.5, opacity=0.7)
        l0 = num(r"0", DIM, 26).next_to(ref, UP, buff=0.05)
        ab = arrow(O, O + P3(PB * K, 0), color=MAG, width=7, tip=0.2, z=10)
        lab = num(r"p_{\text{bala}}=+4{,}31", MAG, 28).next_to(ab, RIGHT, buff=0.15)
        ar = arrow(O + P3(PB * K, -0.6), O + P3((PB + PR) * K, -0.6), color=MAG, width=7, tip=0.2, z=10)
        lar = num(r"p_{\text{rifle}}=-5{,}18", MAG, 28).next_to(ar, LEFT, buff=0.15)
        un = num(r"\mathrm{kg\cdot m/s}", MAG, 26).move_to(P3(5.6, 0.75))
        self.diz("o momento da bala é quatro")
        rp = chip_replay(x=PALCO_X[0] + 0.25)
        self.disparos.append(self.clk.get_value())          # o replay do tiro, junto com a seta do momento da bala
        self.play(FadeIn(ref), FadeIn(l0), GrowArrow(ab), FadeIn(lab), FadeIn(un), FadeIn(rp), run_time=0.9)
        self.wait(1.5)
        self.play(FadeOut(rp), run_time=0.3)
        self.diz("cinco vírgula dezoito")
        self.play(GrowArrow(ar), FadeIn(lar), run_time=0.9)
        self.ate(0.97)
        self.diag = VGroup(ref, l0, ab, lab, ar, lar, un)
        self.e1, self.n1 = e1, n1

    def e8_3_4(self):
        self.an("E8-3")
        O = self.O
        fx = (PB + PR) * K
        gap = Line(O + P3(fx, -1.2), O + P3(0, -1.2)).set_stroke(APAGADO, 4)
        nf = txt("NÃO FECHA", 16, color=APAGADO).next_to(gap, LEFT, buff=0.15)
        self.diz("o momento total era zero")
        self.play(Indicate(self.diag[1], color=WHITE_, scale_factor=1.5), Indicate(self.diag[0], color=WHITE_), run_time=0.9)
        self.diz("essas duas setas não se cancelam")
        self.play(Create(gap), FadeIn(nf), run_time=0.7)
        self.diz("a do rifle é maior")
        self.play(Indicate(self.diag[4], color=WHITE_), run_time=0.8)
        self.diz("São os gases")
        self.play(FadeOut(self.pg), run_time=0.4)
        # nuvem de gases saindo da boca do cano (v7: partículas no 3D, em destaque azulado), com a seta que fecha a soma
        self.nv0 = self.clk.get_value()
        boca = self.boca + P3(-0.25, 0)
        self.wait(1.4)
        pgv = arrow(boca + P3(0.5, -0.85), boca + P3(0.5 + PG * K * 1.6, -0.85), color=MAG, width=6, tip=0.16, z=10)
        lgv = txt("GASES", 16, color=DIM).next_to(pgv, DOWN, buff=0.08)
        ag = arrow(O + P3(fx, -1.2), O + P3(0, -1.2), color=MAG, width=7, tip=0.17, z=11)
        lag = num(r"p_{\text{gases}}=+0{,}866", MAG, 28).next_to(ag, RIGHT, buff=0.15)
        self.diz("zero vírgula oitenta e sete")
        self.play(FadeOut(gap), FadeOut(nf), GrowArrow(pgv), FadeIn(lgv), GrowArrow(ag), FadeIn(lag), run_time=0.9)
        zero = Mc((r"\sum \vec p", MAG), "=", "0", size=40).move_to(P3(O[0] + 0.25, O[1] - 1.9))   # v5 (V16): abaixo do diagrama, centralizado
        self.diz("a soma dá zero")
        self.play(FadeIn(zero, shift=0.1 * UP), run_time=0.7)
        self.ate(0.97)
        # E8-4 -----------------------------------------------------------------------------------------------
        self.an("E8-4")
        fr = fronteira(7.0, 4.0, P3(-3.0, YR + 0.55), rotulo=None)
        sis = linha("SISTEMA", mais(36, "="), "BALA", mais(36), "RIFLE", mais(36), "GASES", size=28, buff=0.16).move_to(P3(-3.5, -3.3))
        self.play(Create(fr[0]), run_time=0.9)
        self.diz("O sistema certo aqui")
        self.play(FadeIn(sis, shift=0.1 * UP), run_time=0.7)
        self.diz("Se a conta do momento")
        d = dica("VELOCIDADE EM RELAÇÃO AO CANO", "NÃO É EM RELAÇÃO AO CHÃO.", "A CONTA FECHA COM OS GASES", size=20)   # v5: folga do Σp
        self.dica_entra(d)                 # no rodapé da CONTA, abaixo de Σp = 0, com folga
        self.sobra(0.55)
        self.clear(rt=0.5)

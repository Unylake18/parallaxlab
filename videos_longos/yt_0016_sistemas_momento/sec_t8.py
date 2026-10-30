"""Lote P8 (v4): T8 — força interna não move o sistema. Cavalo 3D (asset do yt_0015, com o balancim da unidade) arrastando a pedra.
v4: UMA tomada contínua do cavalo (sem emendas nem crossfade): passo de 1,0 m/s em T8-1/T8-2; no "a = 0,32" acelera a 0,32 m/s² até
3,5 m/s (≈ 7,8 s); segue a 3,5 m/s; no gelo freia a −1,26 m/s² até parar (mostrada em câmera lenta) e depois as patas escorregam no
lugar. Duas câmeras alternando por corte seco no começo das frases: lateral (setas) em T8-1, T8-2, T8-4, T8-5 e 3/4 baixa perto das
patas em T8-3 e no gelo. Setas da corda no balancim e na pedra (cinza, internas), rótulos no vão; nada escrito sobre os corpos (as massas
são dados na CONTA). Cyrano 2D (T8-7, um lançamento + um replay); manequim 3D andando (T8-8). Viradas em sequência.
Números: 2.352 / 2.800 / 448 / 0,32 / 2.608 / 192 / 588 N."""
from kit import *  # noqa: F401,F403
from sec_cavalo import Cavalo3D
from sec_manequim import ANK, Manequim3D, pose_andar

MC, MP, MU, G_ = 600, 800, 0.3, 9.8
FP = MU * MP * G_                    # atrito cinético na pedra
FCH = 2800.0
A = (FCH - FP) / (MC + MP)
T = MP * A + FP
FM = 0.1 * MC * G_                   # gelo: as patas escorregam → atrito cinético nas patas (v5, revisão de física)
A_GELO = (FM - FP) / (MC + MP)
assert abs(FP - 2352) < 1e-9 and abs(A - 0.32) < 1e-12 and abs(T - 2608) < 1e-9 and abs(FCH - T - MC * A) < 1e-9 and abs(FM - 588) < 1e-9
assert abs(A_GELO + 1.26) < 0.005
V_C, V_MAX = 1.0, 3.5                # passo de T8-1/T8-2; velocidade depois da aceleração
T_AC = (V_MAX - V_C) / A             # ≈ 7,8 s acelerando
LENTO_G = 2.2                        # a frenagem no gelo (≈ 2,8 s) em câmera lenta (≈ 6 s na tela)
KS = 0.00057                         # comprimento das setas por newton
KV = 0.45                            # seta da velocidade: unidades por m/s
CAM_A = dict(K=0.85, xt=-0.75, yc=-2.3)                       # lateral
CAM_B = dict(modo="obl", az=-40, el=7, fov=30, K=1.1, xc=-3.3, yc=-1.55, dx=-1.2, z=0.55)    # 3/4 baixa, perto das patas


def num(s, cor=WHITE_, size=40):
    return MathTex(s, font_size=size, color=cor)


def vfmt(v):
    return f"{v:.2f}".replace(".", "{,}")


class LoteT8(Base):
    def construct(self):
        self.setup_base(cap="FORÇA INTERNA NÃO MOVE O SISTEMA")
        self.t_acc = None
        self.t_gelo = None
        self.lento_g = LENTO_G
        self.nvis = [ValueTracker(1.0), ValueTracker(1.0)]   # v5: os valores nas setas do chão entram quando a voz os diz
        self.montar()
        self.t8_1()
        self.t8_2_3_4()
        self.t8_5()
        self.t8_6()
        self.t8_7()
        self.t8_8()
        self.fim()
        self.relatorio()

    # ── a tomada contínua: velocidade física, tempo de tela e câmera ─────────────────────────────────────
    def vfis(self, t):
        """Velocidade física (m/s) no instante t da cena."""
        if self.t_gelo is not None and t >= self.t_gelo:
            tau = (t - self.t_gelo) / self.lento_g
            return max(0.0, V_MAX + A_GELO * tau)
        if self.t_acc is not None and t >= self.t_acc:
            return V_C + A * min(T_AC, t - self.t_acc)
        return V_C

    def v(self, t):
        """Velocidade na tela (a câmera lenta do gelo divide); parado no gelo, o corpo balança ±2 cm."""
        if self.t_gelo is not None and t >= self.t_gelo:
            vf = self.vfis(t) / self.lento_g
            if vf <= 0:
                return 0.02 * 2 * PI / 1.4 * math.cos(2 * PI * (t - self.t_gelo) / 1.4)
            return vf
        return self.vfis(t)

    def deslize(self, t):
        if self.t_gelo is not None and t >= self.t_gelo:
            return 0.5 + 1.4 * (1.0 - self.vfis(t) / V_MAX)          # os cascos patinam cada vez mais
        return 0.0

    def gelo(self, t):
        if self.t_gelo is None or t < self.t_gelo - 1.6:
            return 0.0
        return min(1.0, (t - self.t_gelo + 1.6) / 1.2)

    def montar(self):
        cv = self.cv = Cavalo3D(self, v=self.v, op=0.0, deslize=self.deslize, gelo=self.gelo, **CAM_A)
        cv.f3d.conta.set_value(1.0)                    # o chão 3D não passa atrás da CONTA
        self.add(cv.f3d)
        self.cam = "a"
        orig = cv.cam

        def cam(xp):
            if self.cam == "a":
                return orig(xp)
            c = dict(CAM_B)
            c["alvo"] = [round(xp + c.pop("dx"), 4), 0, c.pop("z")]
            return c
        cv.cam = cam
        self._gx = None

        def faixa(t, xp):                           # placa de gelo fixa no chão, só onde as patas passam até parar
            if self.t_gelo is None:
                return (0.0, 0.0)
            if self._gx is None:
                x0 = cv._acum(int(round(self.t_gelo * FPS)))[0]
                xs = x0 + V_MAX ** 2 / (2 * -A_GELO)    # onde o peitoral para
                self._gx = (x0 - 1.1, xs + 0.6)          # das patas da frente na entrada às da frente na parada (a pedra nunca entra no gelo)
            return self._gx
        cv.gx = faixa

    def corte(self, cam, saem=(), entram=()):
        """Corte seco de câmera (no começo de uma frase): o 3D troca de enquadramento de um quadro para o outro."""
        for m in saem:
            m.clear_updaters()
        self.remove(*saem)
        self.cam = cam
        self.cv.f3d._quadro()
        self.add(*entram)

    def setas(self, fch=lambda: FCH, rot=True, tens=True, num_=False, gelo=False):
        """Índices fixos: [0] chão nas patas, [1] chão na pedra, [2]/[3] nomes, [4]/[5] valores (abaixo da linha do chão, sem tocar
        nos cascos), [6] as duas forças da corda (no balancim e na pedra, cinza: internas, rótulos no vão)."""
        def f():
            cv = self.cv
            p = cv.pts()
            g = VGroup()
            yb = p["cascos"][1] - 0.42
            xh = p["cascos"][0] - 0.2
            F = fch()
            g.add(arrow(P3(xh, yb), P3(xh + KS * F * 1.1, yb), color=FC, width=7, tip=0.2, z=12))
            xs = p["pedra_base"][0] + 0.2
            g.add(arrow(P3(xs, yb), P3(xs - KS * FP * 1.1, yb), color=FC, width=7, tip=0.2, z=12))
            n1 = mtxt("GELO SOB AS PATAS" if gelo else "CHÃO NAS PATAS", 15, color=BLUE_L if gelo else FC)
            n2 = mtxt("CHÃO NA PEDRA", 15, color=FC)
            v1 = mtex(rf"{int(round(F)):,}".replace(",", ".") + r"\ \mathrm{N}", FC, 28)
            v2 = mtex(r"2.352\ \mathrm{N}", FC, 28)
            for a_, nm, vl in ((g[0], n1, v1), (g[1], n2, v2)):
                vl.next_to(a_, DOWN, buff=0.12)
                nm.next_to(vl if num_ else a_, DOWN, buff=0.08)
                if not rot:
                    nm.set_opacity(0)
                if not num_:
                    vl.set_opacity(0)
            if num_:
                v1.set_opacity(self.nvis[0].get_value()); v2.set_opacity(self.nvis[1].get_value())
            g.add(n1, n2, v1, v2)
            ts = cv.setas_corda(INT, INT, L=0.9, w=6, lab_a=r"-\vec T", lab_b=r"\vec T", size=32)
            if not tens:
                ts.set_opacity(0)
            g.add(ts)
            return g
        return always_redraw(f)

    def fronteira_c(self, rot="SISTEMA: CAVALO + CORDA + PEDRA"):
        def f():
            p = self.cv.pts()
            xl, xr = p["pedra_tras"][0] - 0.3, p["cabeca"][0] + 0.35
            y0, y1 = p["cascos"][1] - 0.15, p["topo"][1] + 0.22
            r = RoundedRectangle(corner_radius=0.3, width=xr - xl, height=y1 - y0).move_to(P3((xl + xr) / 2, (y0 + y1) / 2))
            r.set_stroke(WHITE_, 2.2, opacity=0.62)
            d = DashedVMobject(r, num_dashes=int((xr - xl + y1 - y0) * 5), dashed_ratio=0.55).set_z_index(1)
            lab = mtxt(rot, 16, op=0.8).next_to(r.get_corner(UL), UP, buff=0.1).align_to(r, LEFT).shift(0.25 * RIGHT)
            return VGroup(d, lab)
        return always_redraw(f)

    def velocidade(self, acel=False):
        """O mostrador `v = … m/s` no canto do PALCO, com a seta violeta da velocidade logo embaixo (posição fixa: serve às duas
        câmeras e nunca encosta no header); com acel, a seta de a embaixo dela."""
        def f():
            v = self.vfis(self.clk.get_value())
            c = P3(-4.25, 2.15)                       # à direita do mostrador, na mesma linha
            g = VGroup(mtex(r"v=" + vfmt(v) + r"\ \mathrm{m/s}", VEL, 32).move_to(P3(-6.9, 2.15), aligned_edge=LEFT),
                       arrow(c, c + P3(KV * v, 0), color=VEL, width=6, tip=0.17, z=12),
                       mtex(r"\vec v", VEL, 32).next_to(c + P3(KV * v, 0), RIGHT, buff=0.12).set_opacity(min(1.0, v / 0.15)))
            if acel:
                ca = P3(-6.55, 1.72)                      # embaixo do mostrador, acima do rótulo da fronteira
                g.add(arrow(ca, ca + P3(1.1, 0), color=VEL, width=5, tip=0.15, z=12),
                      mtex(r"\vec a", VEL, 32).next_to(ca, LEFT, buff=0.12))
            return g
        return always_redraw(f)

    # ── T8-1 ─────────────────────────────────────────────────────────────────────────────────────────────
    def t8_1(self):
        self.an("T8-1")
        fr = self.fronteira_c()
        self.play(self.cv.f3d.op.animate.set_value(1.0), run_time=0.6)
        self.diz("A fronteira envolve")
        self.play(FadeIn(fr), run_time=0.7)
        sg = self.setas(tens=True)
        d1 = Mc(r"m_{\text{cavalo}}=", r"600\ \mathrm{kg}", size=40)
        d2 = Mc(r"m_{\text{pedra}}=", r"800\ \mathrm{kg}", size=40)
        li = txt("INTERNA: A CORDA", 22, color=INT, bold=True)
        di = txt("PUXA A PEDRA E O CAVALO; SOME DA CONTA", 18, color=DIM)
        le = txt("EXTERNAS NA HORIZONTAL", 22, color=FC, bold=True)
        de = txt("CHÃO NAS PATAS E CHÃO NA PEDRA", 18, color=DIM)
        pn = txt("PESO E NORMAL: VERTICAIS, SE CANCELAM", 18, color=DIM)
        for m_, y in ((d1, 2.3), (d2, 1.8), (li, 1.05), (di, 0.65), (le, -0.05), (de, -0.45), (pn, -1.2)):
            na_conta(m_, y)
        self.diz("A corda puxa os dois")
        self.play(FadeIn(sg), FadeIn(li), FadeIn(di), run_time=0.9)
        self.diz("Sobram as forças externas")
        self.play(FadeIn(le), FadeIn(de), run_time=0.8)
        self.diz("O peso e a normal")
        self.play(FadeIn(pn), run_time=0.6)
        self.ate(0.97)
        self.fr, self.sg, self.d12 = fr, sg, VGroup(d1, d2)
        self.conta1 = VGroup(li, di, le, de, pn)

    # ── T8-2, T8-3, T8-4 ─────────────────────────────────────────────────────────────────────────────────
    def t8_2_3_4(self):
        self.an("T8-2")
        self.play(FadeOut(self.conta1), run_time=0.4)
        self.sg.clear_updaters(); self.remove(self.sg)
        self.nvis[0].set_value(0.0); self.nvis[1].set_value(0.0)
        sg = self.setas(num_=True)
        self.add(sg)
        d1, d2 = self.d12
        e1 = Mc((r"f_{\text{pedra}}", FC), r"=0{,}3\cdot 800\cdot 9{,}8=", (r"2.352\ \mathrm{N}", FC), size=40)
        na_conta(e1, 1.05)
        lc = txt("CINÉTICO: A PEDRA JÁ DESLIZA", 16, color=DIM)
        na_conta(lc, 0.6)
        self.diz("O cavalo tem seiscentos")
        self.play(FadeIn(d1), run_time=0.6)
        self.diz("e a pedra, oitocentos")
        self.play(FadeIn(d2), run_time=0.6)
        self.diz("Como a pedra já está deslizando")
        self.play(FadeIn(lc), run_time=0.6)
        self.diz("Então o atrito na pedra")
        self.play(FadeIn(e1[:2]), run_time=0.8)
        self.diz("dois mil trezentos e cinquenta e dois")
        self.play(self.nvis[1].animate.set_value(1.0), run_time=0.4)
        self.play(TransformFromCopy(sg[5], e1[2]), run_time=0.8)
        e2 = Mc((r"F_{\text{chão}}", FC), "=", (r"2.800\ \mathrm{N}", FC), size=40)
        na_conta(e2, -0.05)
        self.diz("o chão empurre o cavalo")
        self.play(FadeIn(e2[:2]), run_time=0.6)
        self.diz("dois mil e oitocentos")
        self.play(self.nvis[0].animate.set_value(1.0), run_time=0.4)
        self.play(TransformFromCopy(sg[4], e2[2]), run_time=0.8)
        self.ate(0.97)
        # T8-3 — sistema inteiro (a corda nem aparece). Corte seco para a câmera 3/4 baixa, perto das patas
        self.an("T8-3")
        self.corte("b", saem=(sg, self.fr))
        e3 = Mc(r"(2.800-2.352)", "=", r"(600+800)", r"\,a", size=42)
        na_conta(e3, -0.75)
        e3b = Mc((r"448\ \mathrm{N}", FC), "=", r"1.400\ \mathrm{kg}", r"\cdot a", size=40)
        na_conta(e3b, -1.45)
        cn = txt("A CORDA NEM APARECE", 16, color=INT).next_to(e2, RIGHT, buff=0.5)
        self.diz("Ela nem aparece na conta")
        self.play(FadeIn(cn), run_time=0.6)
        self.diz("dois mil e oitocentos menos")
        self.play(TransformFromCopy(VGroup(e2[2], e1[2]), e3[0]), run_time=1.0)
        self.diz("quatrocentos e quarenta e oito")
        self.play(FadeIn(e3b[0], shift=0.1 * UP), run_time=0.6)
        self.diz("acelera a massa total")
        self.play(FadeIn(e3[1]), TransformFromCopy(VGroup(d1[1], d2[1]), e3[2]), FadeIn(e3[3]), run_time=1.0)
        self.diz("mil e quatrocentos quilogramas")
        self.play(FadeIn(e3b[1:], shift=0.1 * UP), run_time=0.6)
        e4 = Mc(r"a=", (r"0{,}32\ \mathrm{m/s^2}", VEL), size=46)
        na_conta(e4, -2.25)
        cx = SurroundingRectangle(e4, buff=0.12, corner_radius=0.08).set_stroke(VEL, 2.5)
        self.diz("zero vírgula trinta e dois")
        # a aceleração começa com o "a = 0,32" (a mesma tomada: a velocidade sobe sem salto), com seta e mostrador
        self.t_acc = self.clk.get_value()
        vl = self.velocidade(acel=True)
        self.play(FadeIn(e4, shift=0.1 * UP), Create(cx), FadeIn(vl), run_time=0.8)
        self.ate(0.97)
        # T8-4 — separando os corpos. Corte seco de volta para a lateral, com as setas
        self.an("T8-4")
        fr = self.fronteira_c()
        sg = self.setas(num_=True)
        self.corte("a", entram=(fr, sg))
        self.play(FadeOut(VGroup(d1, d2, e1, lc, e2, e3, e3b, cn)), e4.animate.move_to(P3(6.2, 2.3)), cx.animate.move_to(P3(6.2, 2.3)), run_time=0.8)
        p1 = txt("PEDRA", 20, color=DIM)
        q1 = Mc((r"T", INT), r"-2.352=800\cdot 0{,}32", size=42)
        q1b = Mc(r"\Rightarrow", (r"T", INT), "=", (r"2.608\ \mathrm{N}", INT), size=44)
        p2 = txt("CAVALO", 20, color=DIM)
        q2 = Mc(r"2.800-", (r"T", INT), r"=600\cdot 0{,}32", size=42)
        q2b = Mc(r"\Rightarrow", r"192\ \mathrm{N}", r"=192\ \mathrm{N}", size=44)
        for m_, y in ((p1, 1.6), (q1, 1.1), (q1b, 0.45), (p2, -0.35), (q2, -0.85), (q2b, -1.5)):
            na_conta(m_, y)
        self.diz("Na pedra")
        self.play(FadeIn(p1), FadeIn(q1), run_time=0.9)
        # fim da aceleração (3,5 m/s): a seta e o mostrador saem; o cavalo segue a 3,5 m/s
        while self.clk.get_value() < self.t_acc + T_AC:
            self.wait(1 / FPS)
        vl.clear_updaters()
        self.play(FadeOut(vl), run_time=0.5)
        self.remove(vl)
        self.diz("dois mil seiscentos e oito")
        self.play(FadeIn(q1b, shift=0.1 * UP), run_time=0.8)
        self.diz("No cavalo")
        self.play(FadeIn(p2), FadeIn(q2), run_time=0.9)
        self.diz("cento e noventa e dois")
        self.play(FadeIn(q2b[:2], shift=0.1 * UP), run_time=0.7)
        self.diz("cento e noventa e dois")
        self.play(FadeIn(q2b[2:], shift=0.1 * UP), run_time=0.6)
        ok = txt("FECHA: MESMA TENSÃO NAS DUAS PONTAS", 18, color=DIM)
        na_conta(ok, -2.2)
        self.diz("Fecha certinho")
        self.play(FadeIn(ok), run_time=0.6)
        self.ate(0.97)
        self.sg, self.fr = sg, fr
        self.conta4 = VGroup(p1, q1, q1b, p2, q2, q2b, ok)
        self.e4 = VGroup(e4, cx)

    # ── T8-5 — a resposta ─────────────────────────────────────────────────────────────────────────────────
    def t8_5(self):
        self.an("T8-5")
        pq = VGroup(txt("SE A CORDA PUXA O CAVALO PARA TRÁS", 16, color=DIM), txt("COM A MESMA FORÇA, COMO ELE ANDA?", 16, color=DIM)) \
            .arrange(DOWN, buff=0.08, aligned_edge=LEFT)
        na_conta(pq, 2.3)
        self.play(FadeOut(self.conta4), FadeOut(self.e4), FadeIn(pq, shift=0.1 * DOWN), run_time=0.6)   # v6 (1.2)
        # o valor da tensão junto da seta da pedra, acima da corda, no vão (longe da cabeça e da CONTA)
        cmp_ = always_redraw(lambda: VGroup(mtex(r"2.608\ \mathrm{N}", INT, 28).next_to(self.sg[6][3], UP, buff=0.15)))
        self.diz("dois mil seiscentos e oito")
        self.play(FadeIn(cmp_), run_time=0.6)
        r1 = txt("O CAVALO ANDA PORQUE", 30, bold=True)
        r2 = txt("O CHÃO O EMPURRA;", 30, bold=True, color=FC)
        r3 = txt("A CORDA SÓ TRANSMITE", 30, bold=True, color=INT)
        rr = VGroup(r1, r2, r3).arrange(DOWN, buff=0.22, aligned_edge=LEFT)
        na_conta(rr, 0.9)
        cp = Mc((r"2.800\ \mathrm{N}", FC), ">", (r"2.608\ \mathrm{N}", INT), size=44)
        na_conta(cp, -0.85)
        self.play(TransformFromCopy(cmp_[0], cp[2]), run_time=0.8)
        self.diz("dois mil e oitocentos")
        self.play(TransformFromCopy(self.sg[4], cp[0]), FadeIn(cp[1]), FadeOut(pq), run_time=0.9)
        self.diz("ele anda porque")
        self.play(FadeIn(r1, shift=0.1 * UP), run_time=0.6)
        self.diz("ganha a briga com o chão")
        self.play(FadeIn(r2, shift=0.1 * UP), run_time=0.6)
        self.play(FadeIn(r3, shift=0.1 * UP), run_time=0.6)
        self.ate(0.97)
        self.conta5 = VGroup(rr, cp)
        self.cmp_ = cmp_

    # ── T8-6 — gelo sob as patas: corte para a 3/4, frenagem em câmera lenta, patas escorregando ─────────────
    def t8_6(self):
        self.an("T8-6")
        self.cmp_.clear_updaters()
        t_esc = self.ate_dizer("As patas começam a escorregar", mover=False)
        t_par_ = self.ate_dizer("até parar", mover=False)
        self.t_gelo = self.clk.get_value() + max(2.0, t_esc)     # o gelo surge 1,6 s antes; a frenagem acaba em "até parar"
        self.lento_g = min(16.0, max(LENTO_G, (t_par_ - max(2.0, t_esc)) / (V_MAX / -A_GELO)))   # v6 (1.3): para no "até parar"
        self.corte("b", saem=(self.sg, self.fr, self.cmp_))
        self.play(FadeOut(self.conta5), run_time=0.5)
        vl = self.velocidade()
        lt = chip_lento()
        # v5 (revisão de física): no gelo as patas escorregam → coeficiente CINÉTICO; sai "estático" e "f_máx"
        e1 = VGroup(linha("COEFICIENTE CINÉTICO", tex(r"\approx 0{,}1", WHITE_, 38), size=20, buff=0.15),
                    txt("(AS PATAS ESCORREGAM)", 16, color=DIM)).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        e2 = Mc((r"f_{\text{chão}}", FC), r"=0{,}1\cdot 600\cdot 9{,}8=", (r"588\ \mathrm{N}", FC), size=40)
        e3 = Mc((r"588", FC), "<", (r"2.352", FC), size=44)
        e4 = Mc(r"a\approx", (r"-1{,}26\ \mathrm{m/s^2}", VEL), size=44)
        for m_, y in ((e1, 2.2), (e2, 1.45), (e3, 0.85), (e4, 0.25)):
            na_conta(m_, y)
        while self.clk.get_value() < self.t_gelo - 0.3:
            self.wait(1 / FPS)
        self.play(FadeIn(vl), FadeIn(lt), run_time=0.6)
        t_par = self.t_gelo + V_MAX / -A_GELO * self.lento_g  # onde para (tempo de tela)
        self.diz("Vamos supor um coeficiente")
        self.play(FadeIn(e1), run_time=0.7)
        self.diz("com zero vírgula um, vezes seiscentos")
        self.play(FadeIn(e2[:2]), run_time=0.7)
        self.diz("quinhentos e oitenta e oito")
        self.play(FadeIn(e2[2:]), run_time=0.5)
        self.diz("Só que a pedra continua raspando")
        self.play(FadeIn(e3, shift=0.1 * UP), run_time=0.7)
        self.diz("um vírgula vinte e seis")
        self.play(FadeIn(e4, shift=0.1 * UP), run_time=0.7)
        while self.clk.get_value() < t_par + 0.2:
            self.wait(1 / FPS)
        self.play(FadeOut(lt), run_time=0.4)
        # parado: as patas escorregam no lugar (as de trás derrapando para trás), com um spray fino de gelo
        rng = np.random.default_rng(4)
        sem = [(rng.uniform(0, 1), rng.uniform(-0.25, 0.25), rng.uniform(0.6, 1.0)) for _ in range(14)]

        def spray():
            p = self.cv.pts()
            t = self.clk.get_value()
            base = p["cascos_tras"] + P3(0.25, 0.04)
            g = VGroup()
            for ph, dy, sp in sem:
                u = ((t * sp + ph) % 0.7) / 0.7
                g.add(Dot(base + P3(-0.9 * u, 0.25 * math.sin(PI * u) + dy * u), radius=0.03 * (1 - 0.5 * u), color=JC)
                      .set_opacity(0.5 * (1 - u)))
            return g.set_z_index(11)
        sp_ = always_redraw(spray)
        self.play(FadeIn(sp_), run_time=0.5)
        # a comparação: a mesma pedra (2.352 N) contra o chão firme (2.800 N) e contra o gelo (588 N)
        # duas colunas: à esquerda o rótulo e o veredito (empilhados); à direita as barras (patas em cima, pedra embaixo) e os valores
        y1, y2, x0, k = -0.75, -1.95, XC0 + 1.75, 0.00082
        def linha_cmp(y, rotulo, F, cor_v, veredito):
            r = txt(rotulo, 17, color=DIM).move_to(P3(XC0, y + 0.18), aligned_edge=LEFT)
            vd = txt(veredito, 22, bold=True, color=cor_v).move_to(P3(XC0, y - 0.2), aligned_edge=LEFT)
            bf = Rectangle(width=k * F, height=0.2).set_stroke(width=0).set_fill(FC, 0.9).move_to(P3(x0 + k * F / 2, y + 0.18))
            bp = Rectangle(width=k * FP, height=0.2).set_stroke(width=0).set_fill(escuro(FC, 0.45), 1).move_to(P3(x0 + k * FP / 2, y - 0.16))
            vf = mtex(rf"{int(F):,}".replace(",", ".") + r"\ \mathrm{N}", FC, 26).next_to(bf, RIGHT, buff=0.12)
            vp = mtex(r"2.352\ \mathrm{N}", mix(FC, 0.2), 24).next_to(bp, RIGHT, buff=0.12)
            return VGroup(r, bf, bp, vf, vp, vd)
        L1 = linha_cmp(y1, "CHÃO FIRME", FCH, FC, "ANDA")
        L2 = linha_cmp(y2, "GELO", FM, BLUE_L, "PARA")
        leg = txt("PATAS · PEDRA", 15, color=DIM)
        na_conta(leg, -2.65)
        self.diz("Olha as barras")
        self.play(FadeIn(L1[:5]), FadeIn(L2[:5]), FadeIn(leg), run_time=0.8)
        self.play(FadeIn(L1[5]), FadeIn(L2[5]), run_time=0.5)
        self.diz("O que mudou foi a força do chão")
        self.play(Indicate(L2[1], color=WHITE_), Indicate(L2[3], color=WHITE_), run_time=0.9)
        self.ate(0.97)
        self.vl, self.sp, self.conta6 = vl, sp_, VGroup(e1, e2, e3, e4, L1, L2, leg)

    def t8_7(self):
        cv = self.cv
        self.an("T8-7")
        # virada em sequência: o cavalo e tudo do T8 saem inteiros; depois entra o Cyrano
        self.virada(self.vl, self.sp, self.conta6, cv.f3d)
        Y_CH = -2.2
        PER = 2.6
        # v5: o lançamento quando a voz diz "jogar um ímã para cima"; o replay em "você joga o ímã de novo"
        jogadas = self.jogadas = [-1e9, self.clk.get_value() + self.ate_dizer("jogar um ímã para cima", mover=False)]
        # v7 (3D): o manequim sentado na placa de ferro, o ímã em ferradura na mão e a Lua 3D ao fundo. A câmera sobe até a Lua no
        # "chegar à Lua" (dolly-zoom: a Lua cresce atrás do Cyrano) e desce no "Pena que não funciona".
        XP, KM = 0.0, 2.05
        camA = {"modo": "obl", "az": -90, "el": 5, "alvo": [XP, 0, 0], "K": KM, "fov": 16, "xc": -3.4, "yc": Y_CH}
        camB = {"modo": "obl", "az": -90, "el": 0, "alvo": [XP, 0, 0], "K": 1.5, "fov": 4.5, "xc": -4.6, "yc": -2.4}   # a Lua grande em cima
        LUA = self.lua3 = [2.6, 60.0, 0.0, 1.0]
        for _ in range(40):                                       # a Lua em (−0,7; 2,0) na vista de perto, como no v6
            q = proj3d(camA, LUA[:3])
            LUA[0] += (-0.7 - q[0]) * 0.6
            LUA[2] += (2.0 - q[1]) * 0.6
        tsobe = self.clk.get_value() + self.ate_dizer("chegar à Lua", mover=False)
        tdesce = self.clk_de("T8-7", "Pena que não funciona", 0.1)

        def sobe(t):
            a = min(1.0, max(0.0, (t - tsobe) / 1.6)) * (1 - min(1.0, max(0.0, (t - tdesce) / 1.6)))
            return a * a * (3 - 2 * a)

        def cam_(t):
            u = sobe(t)
            c = {"modo": "obl", "az": -90}
            for kk in ("el", "K", "xc", "yc"):
                c[kk] = camA[kk] + (camB[kk] - camA[kk]) * u
            c["fov"] = math.exp(math.log(camA["fov"]) + (math.log(camB["fov"]) - math.log(camA["fov"])) * u)
            c["alvo"] = [camA["alvo"][q] + (camB["alvo"][q] - camA["alvo"][q]) * u for q in range(3)]
            return c

        def fase(tt):
            ti = max(x for x in jogadas if x <= tt + 1e-9)
            return min(1.0, (tt - ti) / PER) if ti > -1e8 else 0.0

        def est(t):
            s = fase(t)
            yp = 0.06 * math.sin(PI * s) / KM                    # a placa (com a pessoa) dá um pulinho; o ímã sobe e volta (v6)
            yi = 1.5 * math.sin(PI * s) / KM
            topo = 0.06 + yp
            hx = XP - 0.25
            br = 0.0 if s <= 0 or s >= 1 else min(1.0, s / 0.08) * min(1.0, (1 - s) / 0.1)
            braco = [0.25 + (0.12 - 0.25) * br, 1.25 + (2.7 - 1.25) * br, 1.5 + (0.25 - 1.5) * br]
            return {"hx": hx, "hz": topo + 0.11, "pes": [[hx + 0.55, topo + ANK, 0], [hx + 0.5, topo + ANK, 0]], "lam": -0.06,
                    "cab": -0.3, "bracos": [[0.15, 0.7, 0.6], braco], "esp": 1, "chao": "terra", "placa": {"x": XP, "z": topo},
                    "ima": {"mao": 1, "dz": yi, "dx": 0.12 * math.sin(PI * s)}, "lua": LUA, "cam": cam_(t)}
        self.f3c = Fundo3D(self, "manequim", est, op=0.0)
        self.f3c.conta.set_value(1.0)
        self.f3c.conta.add_updater(lambda m: m.set_value(1.0 - sobe(self.clk.get_value())))   # na subida a Lua passa por cima da CONTA vazia
        self.add(self.f3c, self.f3c.conta)

        def ima_m():
            r = self.f3c.real("ima")
            if r is not None:
                return r
            e = self.f3c.e
            return proj3d(e["cam"], (e["hx"] + 0.3, 0, e["hz"] + 1.0 + e["ima"]["dz"]))

        def setas():
            tt = self.clk.get_value()
            s = fase(tt)
            g = VGroup()
            if 0.12 < s < 0.88:
                e = self.f3c.e
                im = ima_m()
                pl = proj3d(e["cam"], (XP + 0.45, 0, e["placa"]["z"]))
                g.add(arrow(im + P3(0, -0.28), im + P3(0, -0.83), color=INT, width=5, tip=0.15, z=10))
                g.add(arrow(pl + P3(0, 0.02), pl + P3(0, 0.6), color=INT, width=5, tip=0.15, z=10))
            return g
        cy = always_redraw(setas)
        lua = VGroup()

        def lua_c():
            return proj3d(cam_(self.clk.get_value()), LUA[:3])
        self.play(self.f3c.op.animate.set_value(1.0), FadeIn(cy), run_time=0.3)
        fr = fronteira(5.2, 4.7, P3(-3.4, -0.05), rotulo=["PESSOA", mais(), "PLACA", mais(), "ÍMÃ"])
        self.diz("chegar à Lua")
        self.play(Flash(lua_c() + P3(0, 0), color=GEO, line_length=0.22, num_lines=12, flash_radius=0.62, time_width=0.4), run_time=0.9)
        self.diz("sentar numa placa de ferro")
        e = self.f3c.e
        q0, q1 = proj3d(e["cam"], (XP - 0.83, -0.45, 0)), proj3d(e["cam"], (XP + 0.83, 0.45, 0.12))
        self.play(Circumscribe(Rectangle(width=abs(q1[0] - q0[0]) + 0.3, height=abs(q1[1] - q0[1]) + 0.3).move_to((q0 + q1) / 2), color=GEO,
                               time_width=0.7), run_time=1.0)
        self.diz("você joga o ímã de novo")
        rp = chip_replay()
        jogadas.append(self.clk.get_value())
        self.play(FadeIn(rp), run_time=0.3)
        while self.clk.get_value() < jogadas[-1] + PER:
            self.wait(1 / FPS)
        self.play(FadeOut(rp), run_time=0.3)
        self.diz("Coloca a pessoa, a placa e o ímã")
        self.play(Create(fr[0]), FadeIn(fr[1]), run_time=1.0)
        self.play(Indicate(fr[1], color=WHITE_, scale_factor=1.05), run_time=0.8)
        # v5 (revisão de física): ímã × placa é interna e não levanta o conjunto; o peso (externo) continua puxando
        c1 = txt("ÍMÃ E PLACA:", 30, bold=True)
        c2 = txt("FORÇA INTERNA", 30, bold=True, color=INT)
        nf = VGroup(txt("NÃO LEVANTA O CONJUNTO;", 20, color=DIM),
                    txt("O PESO (EXTERNO) CONTINUA", 20, color=FC)).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
        VGroup(c1, c2, nf).arrange(DOWN, buff=0.25, aligned_edge=LEFT)
        for m_ in (c1, c2, nf):
            na_conta(m_, m_.get_y() + 0.6)
        peso = VGroup(arrow(P3(-2.05, Y_CH + 1.15), P3(-2.05, Y_CH + 0.05), color=FC, width=7, tip=0.18, z=12),
                      txt("PESO", 16, color=FC).move_to(P3(-1.82, Y_CH + 0.75), aligned_edge=LEFT))
        self.diz("a atração entre o ímã e a placa")
        self.play(FadeIn(c1, shift=0.1 * UP), FadeIn(c2, shift=0.1 * UP), run_time=0.8)
        self.diz("Ela não consegue levantar")
        self.play(FadeIn(nf[0]), run_time=0.5)
        self.diz("E a gravidade, que é externa")
        self.play(FadeIn(nf[1]), GrowArrow(peso[0]), FadeIn(peso[1]), run_time=0.7)
        self.diz("A Lua vai ter que esperar")
        self.play(Flash(lua_c(), color=GEO, line_length=0.22, num_lines=12, flash_radius=0.62, time_width=0.4), run_time=0.9)
        self.ate(0.97)
        cy.clear_updaters()
        self.cyr = VGroup(cy, fr, c1, c2, nf, peso)
        self.cyr3 = self.f3c

    # ── T8-8 — o manequim andando: o atrito do chão no pé ────────────────────────────────────────────────
    def t8_8(self):
        self.an("T8-8")
        t0 = self.clk.get_value()
        VA, PS = 1.05, 0.62
        CYC = PS / 0.6

        def pose(t):
            x = VA * max(0.0, t - t0)
            p = pose_andar(x, x / CYC, 1, passo=PS)
            p["chao"] = "terra"
            return p
        self.virada(*self.cyr, self.cyr3)      # o diagrama do Cyrano (e o 3D dele) sai inteiro antes de o manequim entrar
        self.remove(self.cyr3)
        mq = self.mq = Manequim3D(self, pose, K=2.05, xt=-3.4, yc=-2.75, op=0.0, seguir=True)
        mq.f3d.conta.set_value(1.0)
        self.add(mq.f3d)
        self.play(mq.f3d.op.animate.set_value(1.0), run_time=0.3)

        def atrito():
            e = mq.f3d.e
            x = e["hx"]
            fase = (x / CYC) % 1.0
            # pé de apoio mais atrás (empurrando)
            cand = [(i, (fase + 0.5 * i) % 1.0) for i in (0, 1)]
            cand = [c for c in cand if c[1] < 0.6]
            i = max(cand, key=lambda c: c[1])[0] if cand else 0
            pe = mq.m(e["pes"][i][0], 0.0)
            # v4: as duas setas e os rótulos abaixo da linha do chão (nada sobre o pé): o par da terceira lei, opostas a partir do pé
            # v5 (V7): cada rótulo na ponta livre da sua seta (o do atrito à direita, o do pé à esquerda), folga ≥ 0,25 entre eles
            g = VGroup(arrow(pe + P3(0.1, -0.22), pe + P3(1.15, -0.22), color=FC, width=7, tip=0.18, z=12),
                       mtxt("ATRITO DO CHÃO", 15, color=FC).move_to(pe + P3(1.15 + 0.18, -0.22), aligned_edge=LEFT))
            ch = arrow(pe + P3(-0.1, -0.22), pe + P3(-0.95, -0.22), color=INT, width=5, tip=0.15, z=12)
            return VGroup(g, ch, mtxt("PÉ EMPURRA O CHÃO", 14, color=INT).move_to(pe + P3(-0.95 - 0.18, -0.22), aligned_edge=RIGHT))
        at = always_redraw(atrito)
        l1 = txt("A GENTE EMPURRA A TERRA PARA TRÁS", 22)
        l2 = txt("O ATRITO EMPURRA A GENTE PARA A FRENTE", 22, color=FC, bold=True)
        l3 = txt("NO GELO, QUASE NÃO HÁ ATRITO", 18, color=DIM)
        for m_, y in ((l1, 1.8), (l2, 1.2), (l3, 0.35)):
            na_conta(m_, y)
        self.diz("o seu pé empurra o chão")
        self.play(FadeIn(at), FadeIn(l1), run_time=0.7)
        self.diz("e o atrito do chão")
        self.play(FadeIn(l2), run_time=0.6)
        self.diz("Quem acelera você")
        d = dica("QUEM ACELERA O CONJUNTO É A FORÇA EXTERNA.", "A CORDA SÓ TRANSMITE")
        d.move_to(P3(7.68 - d.width / 2, -1.05))                         # v6 (N1)
        self.dica_entra(d)
        self.diz("Por isso andar no gelo")
        self.play(FadeIn(l3), run_time=0.5)
        self.sobra(0.55)
        at.clear_updaters()
        self.clear(rt=0.5)

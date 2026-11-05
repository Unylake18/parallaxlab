"""Lote PS: S1 (três cartões PANEL com o disco de referência girando atrás), S2 (a hélice Three.js do hook com as duas setas violeta), EN1 (encerramento
padrão: FadeOut geral, logo horizontal com anéis violeta, INSCREVA-SE) e EN2 (desafio dos ponteiros com relógio estilizado). Sem prévia de próximo
vídeo, sem PRÓXIMO VÍDEO:, nenhum vídeo citado."""
from pecas20 import *  # noqa: F401,F403
from sec_hook import GiroHel, camada_helice  # noqa: E402


class LoteFim(L20):

    def construct(self):
        self.setup_base()
        self.sintese1()
        self.sintese2()
        self.en()
        self.fim()
        self.relatorio()
        self.gravar_reg()

    def sintese1(self):
        self.an("S1")
        self.secao("RESUMO")
        # v2 D43: o disco gira de verdade e mostra o que os cartões dizem: setor âmbar θ (da referência à linha pintada), seta curva violeta ω,
        # setas violeta v = ωr proporcionais nos três pontos, giro acelerando com a seta curva verde α, e setas verdes a_c = ω²r para o eixo.
        d = DiscoRef(self, C=P3(-4.0, -0.4), R=2.3, th0=0.4, reg=False)
        C = d.C
        W0, W1 = 0.5, 0.77                                  # ω (rad/s de tela): a seta da ponta vai de 0,75 a 1,15 u (a do 1º ponto ≥ 0,25 u)
        KV, KA = 0.75 / (W0 * 2.3), 0.65 / (W1 ** 2 * 2.3)  # escalas de v = ωr e a_c = ω²r (a_c da ponta para antes do 2º ponto)
        wv, o_th, o_w, o_al, o_ac = (ValueTracker(v) for v in (W0, 0.0, 0.0, 0.0, 0.0))
        self.add(wv, o_th, o_w, o_al, o_ac)
        mot = VGroup()
        st = {"t": self.clk.get_value()}

        def gira(m):
            t = self.clk.get_value()
            d.th.set_value(d.th.get_value() + wv.get_value() * (t - st["t"]))
            st["t"] = t
        mot.add_updater(gira)
        self.add(mot)

        def camada():
            th, w = d.th.get_value(), wv.get_value()
            u, n = d.u(th)
            g = VGroup()
            a, o = th % TAU, o_th.get_value()
            if o > 0.01 and a > 0.02:
                g.add(AnnularSector(inner_radius=0, outer_radius=0.62, angle=a, start_angle=0, arc_center=C).set_fill(ANG, 0.6 * o)
                      .set_stroke(ANG, 3, opacity=o).set_z_index(4))
            o = o_w.get_value()
            if o > 0.01:
                g.add(seta_curva(C, 1.15, th + 0.45, 1.3, VEL, 6, op=o))
                for k in (1, 2, 3):
                    p = d.p(k, th)
                    g.add(seta(p, p + KV * w * 2.3 * k / 3 * n, VEL, 6, 0.22, op=o))
            o = o_al.get_value()
            if o > 0.01:
                g.add(seta_curva(C, 1.95, th + 0.55, 1.2, ACC, 6, op=o))
            o = o_ac.get_value()
            if o > 0.01:
                for k in (1, 2, 3):
                    p = d.p(k, th)
                    g.add(seta(p, p - KA * w * w * 2.3 * k / 3 * u, ACC, 6, 0.2, op=o).set_z_index(9))
            return g
        cam = vivo(camada)
        self.add(cam)
        self.play(FadeIn(d.g), run_time=0.6)

        def card(conteudo, cor):
            bx = RoundedRectangle(corner_radius=0.12, width=max(5.6, conteudo.width + 0.5), height=conteudo.height + 0.42).move_to(conteudo) \
                .set_fill(PANEL, 0.88).set_stroke(cor, 4.5)   # v3 §3: borda na cor da família
            bx._fundo = bx._caixa = True
            return VGroup(bx, conteudo).set_z_index(20)
        c1 = card(VGroup(txt("UM CORPO, UM GIRO:", 28, bold=True),
                         M(r"\theta", ",", r"\ \omega", ",", r"\ \alpha", size=54, cores={0: ANG, 2: VEL, 4: ACC})[0]).arrange(RIGHT, buff=0.25), ANG)
        lin2 = VGroup(M("v", "=", r"\omega", "r", size=50, cores={0: VEL, 2: VEL, 3: GEO_})[0], lbl(r"\cdot", WHITE_, 46),
                      M("a_t", "=", r"\alpha", "r", size=50, cores={0: ACC, 2: ACC, 3: GEO_})[0], lbl(r"\cdot", WHITE_, 46),
                      M("a_c", "=", r"\omega^2", "r", size=50, cores={0: ACC, 2: VEL, 3: GEO_})[0]).arrange(RIGHT, buff=0.22)
        c2 = card(lin2, VEL)
        c3 = card(M(r"\vec v", "=", r"\vec\omega", r"\times", r"\vec r", size=58, cores={0: VEL, 2: VEL, 4: GEO_})[0], VEL)
        cs = VGroup(c1, c2, c3)
        for c in cs:
            c.move_to(P3(3.85, 0))
        c1.move_to(P3(3.85, 1.55))
        c2.move_to(P3(3.85, 0.0))
        c3.move_to(P3(3.85, -1.55))
        self.gat("um corpo rígido girando em torno de um eixo fixo tem um ângulo")
        self.play(FadeIn(c1, shift=0.1 * UP), run_time=0.7)
        self.gat("tem um ângulo")
        self.play(o_th.animate.set_value(1.0), run_time=0.6)
        self.gat("uma velocidade angular")
        self.play(o_w.animate.set_value(1.0), run_time=0.6)
        self.gat("com aceleração angular constante")
        self.play(o_al.animate.set_value(1.0), run_time=0.4)
        self.play(wv.animate.set_value(W1), run_time=3.2, rate_func=linear)      # α constante: ω cresce em reta e as setas v crescem juntas
        self.play(o_al.animate.set_value(0.0), run_time=0.4)
        self.gat("cada ponto transforma esse giro em movimento")
        self.play(FadeIn(c2, shift=0.1 * UP), run_time=0.7)
        self.play(c2[0].animate.set_stroke(ACC, 4.5), run_time=1.2)
        self.gat("a aceleração tangencial e a centrípeta")
        self.play(o_ac.animate.set_value(1.0), run_time=0.6)
        self.gat("e como vetor")
        self.play(FadeIn(c3, shift=0.1 * UP), run_time=0.7)
        self.foco = c3
        self.ate(0.99)
        self.mot_s1 = mot

    def sintese2(self):
        self.an("S2")
        cam = cam_hel(K=3.3, c=P3(-3.75, 0.2))       # v3 §4: hélice ≥ 65% da altura (2R ≈ 5,3 u de 8)
        giro = GiroHel(t0=self.clk.get_value())
        f3 = Fundo3D(self, "helice", lambda t: {"ang": round(giro.ang(t), 4), "cam": cam}, op=0.0)
        k_seta, op_set, op_mk = ValueTracker(1.0), ValueTracker(0.0), ValueTracker(0.0)
        self.add(f3, k_seta, op_set, op_mk)
        ch = camada_helice(self, giro, lambda: cam, k_seta, op_set, op_mk)
        velhos = self.snap()
        self.secao(None)
        self.mot_s1.clear_updaters()
        self.troca([m for m in velhos if m is not f3 and m not in (k_seta, op_set, op_mk)], f3.op.animate.set_value(1.0), seq=True)   # v2: o 3D entra na troca (sem quadro SEM PALCO)
        self.add(ch)
        q = VGroup(txt("POR QUE A PONTA DA HÉLICE", 26, bold=True), VGroup(txt("CHEGA A QUASE", 26, bold=True), valor(r"1.000\ \mathrm{km/h}".replace(".", "{.}"), VEL, 38),
                   txt("?", 26, bold=True)).arrange(RIGHT, buff=0.12)).arrange(DOWN, buff=0.18).move_to(P3(3.75, 1.85))
        # v2 §3: CÂMERA LENTA vira o marcador de canto (como no hook), nunca sobre a hélice
        self.play(op_mk.animate.set_value(1.0), op_set.animate.set_value(1.0), *self.troca_marcador("CÂMERA LENTA ×90", "esq", y=-3.5), FadeIn(q), run_time=0.9)
        fr = VGroup(linha_m(txt("O MESMO", 32, bold=True), lbl(r"\omega", VEL, 54), buff=0.18),
                    txt("DISTÂNCIAS DIFERENTES AO EIXO", 32, bold=True)).arrange(DOWN, buff=0.22, aligned_edge=LEFT).move_to(P3(3.75, -0.6))
        self.gat("o corpo inteiro compartilha o mesmo giro")
        self.play(FadeIn(fr[0], shift=0.1 * UP), run_time=0.7)
        self.gat("cada ponto transforma esse giro")
        self.play(FadeIn(fr[1], shift=0.1 * UP), run_time=0.7)
        self.gat("ela só está mais longe do eixo")
        self.play(Indicate(fr[1], color=WHITE_, scale_factor=1.04), run_time=0.9)
        self.foco = fr
        self.ate(0.99)

    def en(self):
        # ── EN1: encerramento padrão ──
        self.an("EN1")
        velhos = self.snap()
        self.secao(None)
        c0 = P3(0, 1.0)
        logo = self.logo(5.4).move_to(c0)
        aneis = VGroup(*[Circle(radius=r).move_to(c0).set_stroke(VEL, 2.5, opacity=o) for r, o in ((2.2, 0.35), (2.55, 0.2))])
        t_en = self.clk.get_value()

        def ondas():
            t = self.clk.get_value() - t_en
            g = VGroup()
            for k in range(3):
                ph = (t / 2.4 + k / 3) % 1.0
                g.add(Circle(radius=2.2 + 0.6 * ph).move_to(c0).set_stroke(VEL, 3.5, opacity=0.5 * math.sin(math.pi * ph)))
            return g
        ov = vivo(ondas)
        ins = txt("INSCREVA-SE PARA ACOMPANHAR OS PRÓXIMOS VÍDEOS", 32, bold=True).move_to(P3(0, -2.6))
        self.troca(velhos, FadeIn(logo, scale=0.95), FadeIn(aneis), FadeIn(ov), seq=True)      # v2: troca sequencial (sem quadro SEM PALCO)
        self._marc = None                                                                       # o marcador do S2 saiu com a cena velha
        self.gat("se inscreve no parallax lab")
        self.play(FadeIn(ins, shift=0.1 * UP), run_time=0.7)
        self.foco = ins
        self.ate(0.99)
        # ── EN2: desafio dos ponteiros ──
        self.an("EN2")
        velhos = self.snap()
        rc, rr = P3(-4.3, -0.4), 2.0
        t0 = self.clk.get_value()

        def relogio():
            t = self.clk.get_value() - t0
            g = VGroup(Circle(radius=rr).move_to(rc).set_fill(PANEL, 0.9).set_stroke(GEO, 4))
            for k in range(12):
                a = PI / 2 - 2 * PI * k / 12
                g.add(Line(rc + 0.86 * rr * P3(math.cos(a), math.sin(a)), rc + 0.97 * rr * P3(math.cos(a), math.sin(a))).set_stroke(GEO, 4 if k % 3 == 0 else 2))
            am = PI / 2 - 2 * PI * (t * 0.22) % (2 * PI)          # minutos (desenho; horas 12× mais devagar)
            ah = PI / 2 - 2 * PI * (t * 0.22) / 12
            # v2 D44: arco âmbar do ângulo entre os ponteiros (do minuto ao das horas, anti-horário: o quanto o minuto ainda tem de ganhar),
            # setas curvas violeta cheias atrás da ponta de cada ponteiro, dentro do mostrador (fora da borda e das marcas)
            dlt = (ah - am) % (2 * PI)
            if dlt > 0.03:
                g.add(AnnularSector(inner_radius=0, outer_radius=0.5 * rr, angle=dlt, start_angle=am, arc_center=rc).set_fill(ANG, 0.62)
                      .set_stroke(ANG, 4).set_z_index(3))
            g.add(Line(rc, rc + 0.82 * rr * P3(math.cos(am), math.sin(am))).set_stroke(WHITE_, 6).set_z_index(5),
                  Line(rc, rc + 0.55 * rr * P3(math.cos(ah), math.sin(ah))).set_stroke(WHITE_, 9).set_z_index(5),
                  Dot(rc, radius=0.09, color=WHITE_).set_z_index(6))
            g.add(seta_curva(rc, 0.72 * rr, am + 0.75, -0.6, VEL, 9, tip=0.32), seta_curva(rc, 0.42 * rr + 0.05, ah + 0.95, -0.75, VEL, 9, tip=0.3))
            return g
        rv = vivo(relogio)
        d1 = txt("DESAFIO PARA OS COMENTÁRIOS", 30, bold=True, color=CYAN).move_to(P3(3.2, 2.2))
        d2 = VGroup(txt("DEPOIS DO MEIO-DIA,", 30, bold=True), txt("DE QUANTO EM QUANTO TEMPO", 30, bold=True),
                    txt("OS PONTEIROS DAS HORAS E DOS", 30, bold=True), txt("MINUTOS SE ENCONTRAM?", 30, bold=True)).arrange(DOWN, buff=0.16).move_to(P3(3.2, 0.25))
        bal = VGroup(RoundedRectangle(corner_radius=0.25, width=1.5, height=1.0).set_stroke(BLUE_L, 3).set_fill(PANEL, 0.9),
                     Polygon(P3(-0.35, -0.5), P3(-0.05, -0.5), P3(-0.45, -0.85)).set_stroke(BLUE_L, 3).set_fill(PANEL, 0.9),
                     VGroup(*[Dot(P3(x, 0), radius=0.07, color=WHITE_) for x in (-0.35, 0, 0.35)])).move_to(P3(3.2, -2.55))
        bal[1].shift(bal[0].get_bottom() - bal[1].get_top() + 0.02 * UP)
        self.troca(velhos, FadeIn(rv), FadeIn(d1), seq=True)
        self.gat("depois do meio dia")
        self.play(FadeIn(d2, shift=0.1 * UP), run_time=0.8)
        self.gat("dica pense na velocidade angular")
        self.play(FadeIn(bal, scale=0.8), run_time=0.6)
        self.ate(0.99)

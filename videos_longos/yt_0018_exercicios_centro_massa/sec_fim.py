"""Lote PEP (v2): epílogo EP1–EP2 (a caixa de Einstein, 2D, sem números, FORA DE ESCALA; m = E/c² só como PISTA), síntese S2 (o checklist
2 s no centro e sobe; cinco cartões — o S1 saiu no v2), encerramento EN1 (logo com anéis, inscrição) e EN2 (Three.js 'fog': o foguete
acelera cuspindo gás; o ⊕ do foguete + gás anda reto a velocidade constante).
v3 §9: o EP2 não fica parado: replay fantasma 0,5× do pulso, a caixa original tracejada e a deslocada com a cota Δx (FORA DE ESCALA), a linha do ⊕
pisca no "não podia ter andado" e, com m = E/c², um ponto ciano acompanha o pulso ("energia que leva massa"). S2: cartões nascem no lugar final, da
esquerda para a direita; o checklist do resumo em 28 pt. EN2 (v2.1): O FOGUETE em ciano embaixo da pergunta."""
from icones import *  # noqa: F401,F403
from prob2 import Prob2
from pecas18 import Foguete3D



class LoteFim(Prob2):
    FUNDO = "fundo_lab.png"

    def construct(self):
        self.setup_base(cap="EPÍLOGO · A LUZ TAMBÉM EMPURRA")
        self.epilogo()
        self.sintese()
        self.encerramento()
        self.fim()
        self.relatorio()
        self.gravar_reg()

    # ════════════════════════════════════════ epílogo ════════════════════════════════════════
    def epilogo(self):
        W, H, C = 8.4, 1.7, P3(0, -0.5)
        u = ValueTracker(0.0)                       # 0 → 1: o pulso vai da parede esquerda à direita
        rc = ValueTracker(0.0)                      # 0 → 1: o recuo da caixa (v7: separado do pulso; recua só no 2º voo, "a caixa recua")
        rec = 0.42                                  # recuo total da caixa (FORA DE ESCALA)
        self.add(u, rc)

        def caixa_():
            x = -rec * min(1.0, max(0.0, rc.get_value()))
            c = C + P3(x, 0)
            casco = aco(RoundedRectangle(corner_radius=0.08, width=W, height=H).move_to(c), 2.0)
            dentro = RoundedRectangle(corner_radius=0.05, width=W - 0.5, height=H - 0.36).move_to(c).set_fill("#0A1430", 1).set_stroke("#5A6476", 1.2)
            g = VGroup(casco, dentro)
            uu = u.get_value()
            if 0.0 < uu < 1.0:
                xp = c[0] - W / 2 + 0.25 + (W - 0.5) * uu
                g.add(Line(P3(xp - 0.35, c[1]), P3(xp + 0.05, c[1])).set_stroke(mix(CYAN, 0.6), 7), Dot(P3(xp + 0.05, c[1]), radius=0.06, color=WHITE_))
                g.add(seta(P3(xp - 0.2, c[1] + 0.45), P3(xp + 0.9, c[1] + 0.45), MAG, 6, tip=0.2), mtex(r"E/c", MAG, 40).move_to(P3(xp + 0.35, c[1] + 2.0)))
                g.add(seta(P3(c[0] - W / 2 - 0.1, c[1] - 1.25), P3(c[0] - W / 2 - 1.2, c[1] - 1.25), MAG, 6, tip=0.2))
            self.reg("caixa", x=x, u=uu)
            return g.set_z_index(4)
        cx = vivo(caixa_)
        linha_cm = tracejado(C + P3(0, -1.6), C + P3(0, 1.6), WHITE_, 2.2, 0.7)
        cm = marcador_cm(C, r=0.2)
        fe = txt("FORA DE ESCALA", 24, color=DIM).move_to(P3(-5.6, -2.95))
        self.an("EP1")
        self.add(cx)                                                            # quadro 0 já tem palco (a transição do capítulo acende o lote)
        A1_ = ANC["EP1"]

        def abs_de(frase):
            k_ = self._k_frase("EP1", frase)
            return A1_["ini"] + A1_["t"][k_] - LEAD

        # v7: o pulso atravessa a caixa em VELOCIDADE CONSTANTE de "sai um pulso" a "na outra parede"; o 2º voo ("quando ela sai") leva o recuo junto e a
        # caixa para quando o pulso chega ("a caixa para"). Tudo vem do relógio da cena: o movimento acompanha a fala sem esperar por tween.
        t1a, t1b = abs_de("sai um pulso"), abs_de("outra parede")
        t2a, t2b = abs_de("ela sai"), abs_de("a caixa para") - 0.5

        def pulso_rec(m):
            t = self.clk.get_value() + self._off / FPS
            if t < t1a:
                m.set_value(0.0)
                rc.set_value(0.0)
            elif t < t1b:
                m.set_value((t - t1a) / (t1b - t1a))
                rc.set_value(0.0)
            elif t < t2a:
                m.set_value(0.0)
                rc.set_value(0.0)
            elif t < t2b:
                m.set_value((t - t2a) / (t2b - t2a))
                rc.set_value((t - t2a) / (t2b - t2a))
            else:
                m.set_value(1.0)
                rc.set_value(1.0)
        ult = txt("UMA ÚLTIMA IDEIA PARA LEVAR PARA CASA", 32, bold=True).move_to(P3(0, 2.45))
        self.play(FadeIn(ult, shift=0.1 * UP), run_time=0.7)                       # v7: a tela não fica parada antes da caixa nascer na fala
        self.foco = ult
        self.gat("caixa parada")
        self.play(Create(linha_cm), FadeIn(cm), FadeOut(ult), run_time=0.7)
        self.foco = cm
        self.gat("no espaço")
        u.add_updater(pulso_rec)
        self.gat("sai um pulso")
        self.foco = cx
        self.gat("a caixa recua")
        self.play(FadeIn(fe), run_time=0.6)
        self.foco = fe
        self.ate(0.97)
        u.clear_updaters()
        u.set_value(1.0)
        rc.set_value(1.0)
        # ── EP2 ──
        self.an("EP2")
        cx.clear_updaters()
        cd = C + P3(-rec, 0)                                                    # a caixa parou deslocada
        orig = DashedVMobject(RoundedRectangle(corner_radius=0.08, width=W, height=H).move_to(C).set_stroke(GEO, 2, opacity=0.6), num_dashes=60, dashed_ratio=0.5).set_z_index(3)
        meio = Line(cd + P3(0, -1.1), cd + P3(0, 1.1)).set_stroke(GEO, 2.5)
        yq = C[1] - H / 2 - 0.35
        cota_dx = VGroup(Line(P3(cd[0], yq), P3(C[0], yq)).set_stroke(GEO, 2.2), Line(P3(cd[0], yq - 0.1), P3(cd[0], yq + 0.1)).set_stroke(GEO, 2.2),
                         Line(P3(C[0], yq - 0.1), P3(C[0], yq + 0.1)).set_stroke(GEO, 2.2))
        ldx = mtex(r"\Delta x", GEO, 38).next_to(cota_dx, LEFT, buff=0.2)
        self.play(FadeIn(meio), Create(orig), FadeIn(cota_dx), FadeIn(ldx), run_time=0.8)
        self.foco = orig                                                        # v7: o contorno original da caixa (grande) é o destaque enquanto a fala explica
        self.gat("não podia ter andado")
        for _ in range(2):                                                      # v7: a linha do ⊕ pisca em "não podia ter andado" (com o contorno da caixa realçado)
            self.pulsa([linha_cm, orig], 0.6, linha_cm.animate(rate_func=there_and_back).set_stroke(width=5, opacity=1.0))
        r_, ponto = ValueTracker(0.0), ValueTracker(0.0)                         # replay fantasma 0,5× do pulso (e o ponto ciano depois do m = E/c²)
        self.add(r_, ponto)

        def fant():
            u = r_.get_value() % 1.0
            xp = cd[0] - W / 2 + 0.25 + (W - 0.5) * u
            g = VGroup(Line(P3(xp - 0.35, cd[1]), P3(xp + 0.05, cd[1])).set_stroke(mix(CYAN, 0.6), 7, opacity=0.45))
            if ponto.get_value() > 0.01:
                g.add(Dot(P3(xp + 0.05, cd[1] + 0.32), radius=0.08, color=CYAN).set_opacity(ponto.get_value()))
            return g.set_z_index(5)
        fv = vivo(fant)
        self.add(fv)
        q = VGroup(txt("O QUE ATRAVESSOU A CAIXA PARA", 32, bold=True), tx("O ⊕ NÃO ANDAR?", 32, bold=True)).arrange(DOWN, buff=0.15).move_to(P3(0, 2.35))
        seta_q = VGroup(seta(P3(C[0] + W / 2 + 0.2, C[1] + 0.0), P3(C[0] + W / 2 + 1.9, C[1] + 0.0), MAG, 6, tip=0.22), mtex("?", MAG, 52).move_to(P3(C[0] + W / 2 + 1.05, C[1] + 0.55)))
        tR = {"v": None}

        def rodar(m):                                                           # 0,5×: o pulso fantasma leva 6 s por volta, preso ao relógio da cena
            if tR["v"] is not None:
                m.set_value((self.clk.get_value() + self._off / FPS - tR["v"]) / 6.0)
        r_.add_updater(rodar)
        self.gat("o que foi para a direita")
        tR["v"] = (self.nq + self._off) / FPS
        self.play(FadeIn(q, shift=0.1 * UP), FadeIn(seta_q, shift=0.4 * RIGHT), run_time=0.8)               # v7: a seta "?" para a direita cresce em "o que foi para a direita"
        self.foco = q
        pista = VGroup(mtex(r"m=\tfrac{E}{c^2}", WHITE_, 46), txt("PISTA, NÃO DEMONSTRAÇÃO", 24, color=DIM)).arrange(RIGHT, buff=0.3).move_to(P3(0, -3.05))
        pista[0]._partes = [("m", WHITE_), ("=", WHITE_), ("E", KC), ("c^2", WHITE_)]
        pista[0][0][2].set_color(KC)
        self.gat("a própria energia carregue inércia")
        self.play(FadeIn(pista), ponto.animate.set_value(1.0), run_time=0.8)
        self.foco = pista
        self.ate(0.97)
        r_.clear_updaters()
        fv.clear_updaters()

    # ════════════════════════════════════════ síntese (S2) ════════════════════════════════════════
    def sintese(self):
        self.an("S2")
        velhos = self.snap()
        self.secao("RESUMO")
        ck = Checklist.grande().move_to(P3(0, 0.2))
        self.troca(velhos, FadeIn(ck), seq=True)
        ck2 = VGroup(*[VGroup(Checklist.icone(k, 1.2), txt(f"{k + 1}.", 28, color=CYAN, bold=True), txt(Checklist.LONGAS[k], 28, bold=True)).arrange(RIGHT, buff=0.2)
                       for k in range(3)]).arrange(DOWN, buff=0.16, aligned_edge=LEFT).move_to(P3(0, 2.05))     # o checklist do resumo em 28 pt
        frases = (("TIRAR MASSA",), ("MONTAR", "POR PARTES"), ("⊕ PARADO,", "DOIS", "REFERENCIAIS"), ("NO REFERENCIAL", "DO CM"), ("⊕ ACELERA →", "FORÇA", "EXTERNA"))
        cards = VGroup()
        for k in range(5):
            ic = icone(k, 0.8)
            lab = VGroup(*[tx(l, 24, bold=True) for l in frases[k]]).arrange(DOWN, buff=0.08)
            g = VGroup(ic, lab).arrange(DOWN, buff=0.28)
            bx = RoundedRectangle(corner_radius=0.14, width=2.85, height=3.15).move_to(g).set_fill(PANEL, 0.88).set_stroke(BLUE_L, 1.8)
            bx._fundo = True
            bx._caixa = True
            cards.add(VGroup(bx, g))
        cards.arrange(RIGHT, buff=0.2).move_to(P3(0, -1.75))                    # cada cartão nasce já no lugar final, da esquerda para a direita
        self.foco = ck
        self.gat("um buraco")
        self.play(ReplacementTransform(ck, ck2), FadeIn(cards[0]), run_time=0.8)               # v5 G32: o primeiro cartão entra no mesmo play em que a lista sobe
        ck = ck2
        self.foco = ck
        for k, ger_ in ((1, "um corpo complicado"), (2, "sem força externa"), (3, "trocar de régua"), (4, "quando o centro de massa acelera")):
            self.gat(ger_)
            self.foco = cards[k - 1]
            self.play(FadeIn(cards[k]), cards[k - 1].animate.set_opacity(0.6), run_time=0.7)             # v7: o cartão anterior apaga para 60%
        self.foco = cards[4]
        self.gat("as três perguntas")
        self.play(cards[4].animate.set_opacity(0.6), Indicate(ck, color=WHITE_, scale_factor=1.05), run_time=1.0)
        self.foco = ck
        fim_ = txt("ESCOLHA BEM O SISTEMA E O REFERENCIAL", 30, bold=True).move_to(P3(0, 0.4))
        self.gat("o mais difícil sumiu")
        self.play(FadeIn(fim_, shift=0.1 * UP), run_time=0.7)
        self.foco = fim_
        self.ate(0.97)

    # ════════════════════════════════════════ encerramento ════════════════════════════════════════
    def encerramento(self):
        self.an("EN1")
        velhos = self.snap()
        self.secao(None)
        logo = self.logo(5.4).move_to(P3(0, 1.3))
        aneis = VGroup(*[Circle(radius=r).move_to(P3(0, 1.3)).set_stroke(BLUE_L, 2, opacity=o) for r, o in ((2.2, 0.25), (2.55, 0.15))])
        ins = txt("INSCREVA-SE PARA ACOMPANHAR OS PRÓXIMOS VÍDEOS", 32, bold=True).move_to(P3(0, -3.45))
        # v7: ondas que se expandem a partir do logo, com o relógio da cena (CTA nunca parado; sem tween, sem piscar)
        t_en1 = ANC["EN1"]["ini"]

        def giro_f():
            t = self.clk.get_value() + self._off / FPS - t_en1
            g = VGroup()
            for k in range(3):
                ph = (t / 2.4 + k / 3) % 1.0
                g.add(Circle(radius=2.2 + 0.6 * ph).move_to(P3(0, 1.3)).set_stroke(BLUE_L, 3.5, opacity=0.5 * math.sin(math.pi * ph)))
            return g
        giro = vivo(giro_f)
        self.troca(velhos, FadeIn(logo, scale=0.95), FadeIn(aneis), FadeIn(giro), seq=True)
        self.gat("se inscreve no parallax lab")
        self.play(FadeIn(ins, shift=0.1 * UP), aneis.animate.scale(1.06).set_stroke(opacity=0.3), run_time=0.9)
        self.foco = ins
        # v6 (CTA explicado): um cartão por ideia, entre os anéis e a chamada
        cta = [cartao("A FÍSICA QUE PARECE DIFÍCIL", "ANIMADA, CONTA POR CONTA", size=24), cartao("ATIVE O SININHO", "E DEIXE O SEU LIKE", size=24),
               cartao("COMENTE: QUAL DOS SEIS", "FOI O SEU FAVORITO?", size=24)]
        for c_ in cta:
            c_.move_to(P3(0, -2.3))
        self.gat("aqui no canal")
        self.play(FadeIn(cta[0], shift=0.1 * UP), run_time=0.6)
        self.foco = cta[0]
        self.gat("ativa o sininho")
        self.play(FadeOut(cta[0]), run_time=0.3)
        self.play(FadeIn(cta[1], shift=0.1 * UP), run_time=0.5)
        self.gat("conta nos comentários")
        self.play(FadeOut(cta[1]), run_time=0.3)
        self.play(FadeIn(cta[2], shift=0.1 * UP), run_time=0.5)
        self.foco = cta[2]
        self.play(aneis.animate.scale(1 / 1.06), run_time=1.2)
        self.ate(0.97)
        # ── EN2: o foguete ──
        self.an("EN2")
        velhos = self.snap()
        fg = Foguete3D(self, op=0.0)
        self.add(fg.t, fg.f3d)
        yc = fg.yc

        def gas():
            t = fg.t.get_value()
            g = VGroup()
            for age, x, y in fg.gas_pts(t):
                o = max(0.0, 1 - age / 2.0)
                if o > 0.02 and abs(x) < 7.4:
                    g.add(Dot(P3(x, yc + y), radius=0.05, color=CMC).set_opacity(0.9 * o))
            ts = np.linspace(0, t, max(2, int(t * 6) + 2))
            g.add(rastro_cm([P3(fg.cm_x(s), yc - 0.0) for s in ts], w=4, op=0.9))
            g.add(marcador_cm(P3(fg.cm_x(t), yc), r=0.17))
            self.reg("foguete", t=t, cm=P3(fg.cm_x(t), yc))
            return g.set_z_index(6)
        gv = vivo(gas)
        self.troca(velhos, fg.f3d.op.animate.set_value(1.0), FadeIn(gv), seq=True)
        T = dur("EN2")
        q = txt("COMO ACELERAR NO VÁCUO SEM SE APOIAR EM NADA?", 32, bold=True).move_to(P3(0, 2.6))
        prox = txt("O FOGUETE", 34, bold=True, color=CYAN).next_to(q, DOWN, buff=0.3)                    # v2.1: embaixo da pergunta
        t_ini = ANC["EN2"]["ini"]
        # v7: o foguete anda com o relógio da cena (o tempo do 3D = segundos desde o início do EN2): nunca fica parado e não depende de tween
        fg.t.add_updater(lambda m: m.set_value(min(T - 0.2, max(0.0, self.clk.get_value() + self._off / FPS - t_ini))))
        self.gat("como um foguete acelera")
        self.play(FadeIn(q, shift=0.1 * UP), run_time=0.8)
        self.foco = q
        self.gat("o foguete")
        self.play(FadeIn(prox, shift=0.1 * UP), run_time=0.8)
        self.foco = prox
        self.ate(0.99)
        fg.t.clear_updaters()

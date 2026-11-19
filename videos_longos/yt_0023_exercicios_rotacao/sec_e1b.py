"""Lote PE1b (v2): E1-11 a E1-18 — o volante girando (simulação real de 1,5 s), acelerações na borda, balanço de energia (barras e P(t)),
o freio em tempo real (calor na pastilha e no anel), o aro fino solto do repouso lado a lado (os dois param em 1,5 s) e a dica.
Álgebra do zero (v2 §2): lei literal → riscos dos termos nulos → glyph map → números voando dos rótulos/contadores."""
from pecas23 import *  # noqa: F401,F403
from sec_e1a import ITENS, item_mob, chamada, chamada_em


def fixa(p, rot, pos, cor=GEO):
    """Rótulo num lugar FIXO da tela (fora da peça e dentro do quadro) com chamada GEO até o ponto p."""
    rot.move_to(pos)
    v = p - rot.get_center()
    a = rot.get_center() + v * min(1.0, (rot.width / 2 + 0.1) / max(1e-6, abs(v[0])) if abs(v[0]) > 1e-6 else 1.0)
    return VGroup(Line(a, p).set_stroke(cor, 2), Dot(p, radius=0.045, color=cor), rot).set_z_index(16)

KQ, YQ, XQ = 2.6, 1.7, -1.4          # v9: volante INTEIRO abaixo da máscara do cabeçalho (antes 3,2 / 2,7 cortava o topo); bloco ainda cai 1,11 m acima da trilha


class LoteE1b(Lote23, VolanteMix):
    def corpo(self):
        f3 = self.volante3d(u0=1.0, K0=KQ, yc0=YQ, op=0.0)
        vt = self.vt
        vt["alvo_x"].set_value(-(XQ + 3.85) / KQ)
        tr = self.trilha([(a, item_mob(b)) for a, b in ITENS])
        for k in (0, 1):
            tr[k]._feito = True
            escala_op(tr[k], 0.85)
            self._tr_ok.add(T(r"\checkmark", 36, ACC).next_to(tr[k], UP, buff=0.1))
        self.play(f3.op.animate.set_value(1.0), FadeIn(tr), FadeIn(self._tr_ok), run_time=0.5)

        # ── E1-11: item c — 1,5 s de simulação real; ω = ω₀ + αt e θ = θ₀ + ω₀t + ½αt² com os termos nulos riscados ──
        self.an("E1-11")
        self.secao("EXERCÍCIO 1 · O VOLANTE")
        self.tr_acende(2)
        tsim = ValueTracker(0.0)
        self.add(tsim)
        vt["th"].add_updater(lambda m: m.set_value(vol_th(tsim.get_value())))
        cont = vivo(lambda: VGroup(lbl(r"\Delta\theta=" + br(vol_th(tsim.get_value()), 2) + r"\ \mathrm{rad}", ANG, 40),
                                   lbl(r"\omega=" + br(AL_VOL * tsim.get_value(), 2) + r"\ \mathrm{rad/s}", VEL, 40),
                                   lbl(r"t=" + br(tsim.get_value(), 2) + r"\ \mathrm{s}", WHITE_, 40)).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
                    .move_to(P3(-5.85, 1.0)).set_z_index(20))
        b0 = self.v_bloco(0.085)
        x_r = self.v_eixo()[0] - 0.5                        # régua do h à esquerda do pedestal (fora da CONTA)
        regua_ = vivo(lambda: VGroup(Line(P3(x_r, b0[1]), P3(x_r, self.v_bloco(0.085)[1])).set_stroke(GEO, 3),
                                     Line(P3(x_r - 0.12, b0[1]), P3(x_r + 0.12, b0[1])).set_stroke(GEO, 3),
                                     Line(P3(x_r - 0.12, self.v_bloco(0.085)[1]), P3(x_r + 0.12, self.v_bloco(0.085)[1])).set_stroke(GEO, 3),
                                     lbl("h=" + br(0.15 * vol_th(tsim.get_value()), 2) + r"\ \mathrm{m}", GEO, 40)
                                     .next_to(P3(x_r - 0.15, (b0[1] + self.v_bloco(0.085)[1]) / 2), LEFT, buff=0.1)).set_z_index(18))
        self.gat("a aceleração angular é constante")
        Ll, ill, _ = self.linha((r"\alpha", "=", r"\tfrac{a}{r}"), size=46, rt=0.9, metodo="lei")        # v5 LEI PRIMEIRO
        L0, i0, l0b = self.linha((r"\alpha", "=", r"6{,}56\ \mathrm{rad/s^2}"), cores={2: ACC}, size=46, rt=1.0)
        self.gat("a velocidade angular é aceleração angular vezes tempo")
        W0, iw0, _ = self.linha((r"\omega", "=", r"\omega_0", "+", r"\alpha", "t"), rt=0.9, metodo="lei")
        W1, iw1, _ = self.gm(W0, iw0, (r"\omega", "=", r"\alpha", "t"), riscar=[2], sai=[3], rt=1.0)
        W2a, iw2a, _ = self.gm(W1, iw1, (r"\omega", "=", r"6{,}56", r"\cdot", r"1{,}5"), sai=[2, 3], voos={2: mp(L0, i0, [2])}, cores={2: ACC}, rt=1.1)
        W2, iw2, w2b = self.gm(W2a, iw2a, (r"\omega", "=", r"9{,}83\ \mathrm{rad/s}"), cores={2: VEL}, rt=0.9)
        self.gat("o ângulo é metade")
        self.play(FadeIn(cont), FadeIn(regua_), run_time=0.4)
        self.play(tsim.animate.set_value(1.5), run_time=1.5, rate_func=linear)
        self.pilha.so(l0b, w2b)
        A0, ia0, _ = self.linha((r"\theta", "=", r"\theta_0", "+", r"\omega_0", "t", "+", r"\tfrac{1}{2}", r"\alpha", "t^2"), rt=1.1, metodo="lei")
        A1, ia1, _ = self.gm(A0, ia0, (r"\theta", "-", r"\theta_0", "=", r"\tfrac{1}{2}", r"\alpha", "t^2"), riscar=[4, 5], sai=[6], mapas=[([3], [1])], rt=1.2)
        A2, ia2, _ = self.gm(A1, ia1, (r"\Delta\theta", "=", r"\tfrac{1}{2}", r"\alpha", "t^2"), mapas=[([0, 1, 2], [0])], rt=1.0)
        A3a, ia3a, _ = self.gm(A2, ia2, (r"\Delta\theta", "=", r"\tfrac{1}{2}", r"\cdot", r"6{,}56", r"\cdot", r"1{,}5^2"), sai=[3, 4],
                               voos={4: mp(L0, i0, [2]), 6: cont[0][2]}, cores={4: ACC}, rt=1.3)
        A3, ia3, _ = self.gm(A3a, ia3a, (r"\Delta\theta", "=", r"7{,}37\ \mathrm{rad}"), cores={2: ANG}, rt=0.9)
        A4, ia4, a4b = self.gm(A3, ia3, (r"\Delta\theta", "=", r"1{,}17\ \mathrm{volta}"), cores={2: ANG}, rt=0.8)
        self.gat("o bloco desce esse ângulo")
        self.pilha.so(w2b, a4b)
        V0, iv0, _ = self.lei("pontes", ("h", "=", "r", r"\Delta\theta"), rt=0.9)
        V1, iv1, v1b = self.gm(V0, iv0, ("h", "=", r"0{,}15", r"\cdot", r"7{,}37", "=", r"1{,}11\ \mathrm{m}"), sai=[2, 3],
                               voos={2: self.r_tambor_lbl(), 4: mp(A3, ia3, [2])}, cores={2: GEO, 6: GEO}, rt=1.2)
        self.gat("com velocidade de um vírgula quatro sete")
        U0, iu0, _ = self.lei("pontes", ("v", "=", r"\omega", "r"), rt=0.8)
        U1, iu1, _ = self.gm(U0, iu0, ("v", "=", r"9{,}83", r"\cdot", r"0{,}15", "=", r"1{,}47"), sai=[2, 3],
                             voos={2: mp(W2, iw2, [2]), 4: self._rt_lbl}, cores={6: VEL}, caixa_cor=VEL, rt=1.1)
        self.tr_ok(2)
        self.ate(0.99)
        vt["th"].clear_updaters()
        vt["th"].set_value(vol_th(1.5))

        # ── E1-12: um ponto na borda (t = 1,5 s): a_t e a_c, rótulos FORA do anel ──
        self.an("E1-12")
        self.selo("FORA DE ESCALA", [[lbl(r"a_t/a_c=0{,}068", ACC, 38)], ["EM", lbl(r"t=1{,}5\ \mathrm{s}", WHITE_, 38)]])
        self.pilha.limpa(anims=[FadeOut(cont), FadeOut(regua_), FadeOut(self._rt_lbl)])
        S12, C12 = 5.0, P3(-4.4, 0.4)                    # v5 §1.1: esquema 2.5D frontal do volante já girado (θ de t = 1,5 s)
        self.modo25(C12, S12)
        r12 = self.rig25_vivo()
        self.play(f3.op.animate.set_value(0.0), FadeIn(r12), run_time=1.0)
        o_ = self.v_eixo()
        ang_p = 2.3
        P_ = self.vp((0.4 * math.cos(ang_p), -0.04, 0.4 * math.sin(ang_p)))
        u_in = vet_unit(o_ - P_)
        tg = np.array([u_in[1], -u_in[0], 0])
        pt_ = Dot(P_, radius=0.09, color=WHITE_).set_z_index(16)
        s_ac = seta_s(P_, P_ + 1.2 * u_in, ACC, 6)
        s_at = seta_s(P_, P_ + 0.62 * tg, ACC, 6)
        l_ac = fixa(P_ + 0.6 * u_in, lbl("a_c", ACC, 42), P3(-6.6, 2.75))
        l_at = lbl("a_t", ACC, 42).next_to(P_ + 0.62 * tg, UP, buff=0.18)
        self.gat("um ponto na borda do anel")
        r_ = VGroup(DashedLine(o_, P_, dash_length=0.07).set_stroke(GEO, 2), fixa((o_ + P_) / 2, lbl(r"R_2=0{,}40\ \mathrm{m}", GEO, 40), P3(-6.1, -2.55)))
        self.play(FadeIn(pt_), Create(r_[0]), FadeIn(r_[1]), run_time=0.6)
        self.gat("a aceleração tangencial é a aceleração angular vezes o raio")
        self.play(FadeIn(s_at), FadeIn(l_at), run_time=0.5)
        E0, ie0, _ = self.lei("pontes", ("a_t", "=", r"\alpha", "r", r"\quad", "a_c", "=", r"\omega^2", "r"), rt=1.0)
        self._voa_estrito = True                         # v8: a caneta escreve "=" e o resultado só depois de o 0,40 pousar, da esquerda para a direita
        E1, ie1, _ = self.gm(E0, ie0, ("a_t", "=", r"6{,}56", r"\cdot", r"0{,}40", "=", r"2{,}62\ \mathrm{m/s^2}"), sai=[2, 3, 4, 5, 6, 7, 8],
                             voos={4: r_[1][2]}, cores={2: ACC, 6: ACC}, rt=1.2)
        self._voa_estrito = False
        self.gat("a centrípeta é a velocidade angular ao quadrado")
        self.play(FadeIn(s_ac), FadeIn(l_ac), run_time=0.5)
        E2a, ie2a, _ = self.linha(("a_c", "=", r"9{,}83^2", r"\cdot", r"0{,}40"), voos={0: mp(E0, ie0, [5]), 4: r_[1][2]}, size=46, rt=1.1)
        E2, ie2, _ = self.gm(E2a, ie2a, ("a_c", "=", r"38{,}7\ \mathrm{m/s^2}", r"\approx", r"3{,}9", "g"), cores={2: ACC, 4: ACC}, rt=1.1)
        self.gat("só uns quatro graus")
        dang = math.radians(3.9)
        rot_ = np.array([[math.cos(-dang), -math.sin(-dang), 0], [math.sin(-dang), math.cos(-dang), 0], [0, 0, 1]])
        u_tot = rot_ @ u_in
        s_tot = seta_s(P_, P_ + 1.25 * u_tot, ACC, 5)
        arco = Arc(radius=0.9, start_angle=math.atan2(u_in[1], u_in[0]), angle=-dang, arc_center=P_).set_stroke(ANG, 4)
        self.play(FadeIn(s_tot), Create(arco), run_time=0.7)
        E3, ie3, _ = self.linha((r"\arctan\frac{a_t}{a_c}", "=", r"3{,}9^\circ"), cores={2: ANG}, size=46, rt=1.0)
        self.ate(0.99)
        borda = VGroup(pt_, r_, s_ac, s_at, l_ac, l_at, s_tot, arco)

        # ── E1-13: item d — energia: U_i + K_i = U_f + K_f; riscos; barras viram os termos ──
        self.an("E1-13")
        self.sem_selo()
        self.tr_acende(3)
        self.pilha.limpa(anims=[FadeOut(borda)])
        self.play(FadeOut(r12), run_time=0.35)
        self.modo25(None)
        vt["K"].set_value(KQ)
        vt["yc"].set_value(YQ)
        vt["alvo_x"].set_value(-(XQ + 3.85) / KQ)
        vt["th"].set_value(0.0)
        self.play(f3.op.animate.set_value(1.0), run_time=0.35)
        tsim2 = ValueTracker(0.0)
        self.add(tsim2)
        vt["th"].add_updater(lambda m: m.set_value(vol_th(tsim2.get_value())))
        HB, yb0 = 2.8, -2.45
        E_TOT = M_BL * G * 0.15 * vol_th(1.5)

        def barras_():
            t = tsim2.get_value()
            U_ = M_BL * G * 0.15 * vol_th(t)
            Kv = I_VOL * (AL_VOL * t) ** 2 / 2
            Kb = M_BL * (0.15 * AL_VOL * t) ** 2 / 2
            g = VGroup()
            for x in (-6.75, -5.75):
                g.add(Rectangle(width=0.6, height=HB).move_to(P3(x, yb0 + HB / 2)).set_stroke(GEO, 1.6))
            h = U_ / E_TOT * HB
            if h > 0.005:
                g.add(Rectangle(width=0.56, height=h).move_to(P3(-6.75, yb0 + h / 2)).set_stroke(width=0).set_fill(KC, 1.0))
            hv, hb_ = Kv / E_TOT * HB, Kb / E_TOT * HB
            if hv > 0.005:
                g.add(Rectangle(width=0.56, height=hv).move_to(P3(-5.75, yb0 + hv / 2)).set_stroke(width=0).set_fill(KC, 1.0))
            if hb_ > 0.005:
                g.add(Rectangle(width=0.56, height=hb_).move_to(P3(-5.75, yb0 + hv + hb_ / 2)).set_stroke(BACKGROUND_COLOR, 1.2).set_fill(mix(KC, 0.55), 1.0))
            return g.set_z_index(12)

        bv = vivo(barras_)
        nomes = VGroup(lbl("mgh", KC, 40).move_to(P3(-6.75, yb0 + HB + 0.38)), lbl(r"K", KC, 40).move_to(P3(-5.75, yb0 + HB + 0.38)))
        self.gat("o peso do bloco realizou um trabalho")
        C0, ic0, _ = self.linha(("U_i", "+", "K_i", "=", "U_f", "+", "K_f"), rt=1.0, metodo="lei")
        self.play(FadeIn(bv), FadeIn(nomes), run_time=0.4)
        self.play(tsim2.animate.set_value(1.5), run_time=1.5, rate_func=linear)
        C1, ic1, _ = self.gm(C0, ic0, ("m", "g", "h", "=", r"\tfrac{1}{2}", "m", "v^2", "+", r"\tfrac{1}{2}", "I", r"\omega^2"),
                             riscar=[2, 4], sai=[1, 5], mapas=[([0], [0, 1, 2]), ([6], [4, 5, 6, 7, 8, 9, 10])], rt=1.4)
        self.gat("a energia cinética do bloco")
        C2, ic2, _ = self.gm(C1, ic1, (r"108{,}4", "=", r"10{,}9", "+", r"97{,}5"), mapas=[([0, 1, 2], [0]), ([4, 5, 6], [2]), ([8, 9, 10], [4])],
                             cores={0: KC, 2: KC, 4: KC}, rt=1.3)
        lkb = txt("BLOCO 10%", 30, color=mix(KC, 0.55)).move_to(P3(-6.25, yb0 - 0.38))
        self.play(FadeIn(lkb), self.ind_copia(mp(C2, ic2, [2]), KC, 1.1, 0.6), run_time=0.6)
        self.gat("a de rotação do volante")
        self.play(self.ind_copia(mp(C2, ic2, [4]), KC, 1.1, 0.6), run_time=0.6)
        self.gat("somando cento e oito vírgula quatro")
        C3, ic3, c3b = self.gm(C2, ic2, (r"10{,}9", "+", r"97{,}5", "=", r"108{,}4\ \mathrm{J}", r"\ \checkmark"), cores={0: KC, 2: KC, 4: KC, 5: ACC}, caixa_cor=KC, rt=1.2)
        lkv = txt("VOLANTE 90%", 30, color=KC).move_to(P3(-6.1, yb0 - 0.38))
        self.play(ReplacementTransform(lkb, lkv), run_time=0.4)
        self.gat("nove vezes a do bloco")
        G5, ig5, _ = self.linha({"pre": (), "num": ("K_{vol}",), "den": ("K_{bloco}",), "post": ("=", r"\tfrac{I}{m\,r^2}", "=", r"8{,}97")}, size=46, rt=1.2)
        self.ate(0.99)
        vt["th"].clear_updaters()
        vt["th"].set_value(vol_th(1.5))

        # ── E1-14: potência P = τω = Tv e a área do triângulo que vira ½Pt ──
        self.an("E1-14")
        self.selo("CONFERE", "A ÁREA SOB P(t) É A ENERGIA DO VOLANTE")
        self.pilha.limpa(anims=[FadeOut(lkv)])
        self.gat("a potência é a tração")
        P1, ip1, _ = self.linha(("P", "=", r"\tau", r"\omega", "=", "T", "v"), size=48, rt=1.1, metodo="lei")
        self.gat("cento e trinta watts")
        P2, ip2, _ = self.gm(P1, ip1, ("P", r"(1{,}5\ \mathrm{s})", "=", r"88{,}2", r"\cdot", r"1{,}47", "=", r"130\ \mathrm{W}"), sai=[2, 3, 4, 5, 6],
                             cores={7: KC}, rt=1.2)
        gx0, gy0, gw, gh = 1.3, -3.1, 4.6, 1.15        # v7: gráfico mais baixo (o rótulo P e o 130 W não podem tocar a caixa K_vol)
        ax = VGroup(Line(P3(gx0, gy0), P3(gx0 + gw, gy0)).set_stroke(GEO, 2), Line(P3(gx0, gy0), P3(gx0, gy0 + gh + 0.2)).set_stroke(GEO, 2),
                    lbl("P", KC, 40).move_to(P3(gx0 + 0.05, gy0 + gh + 0.5)), lbl("t", WHITE_, 40).move_to(P3(gx0 + gw + 0.28, gy0)),
                    lbl(r"1{,}5\ \mathrm{s}", WHITE_, 36).move_to(P3(gx0 + gw * 0.9, gy0 - 0.36)), lbl(r"130\ \mathrm{W}", KC, 36).move_to(P3(gx0 - 0.85, gy0 + gh))).set_z_index(10)
        reta = Line(P3(gx0, gy0), P3(gx0 + gw * 0.9, gy0 + gh)).set_stroke(KC, 4).set_z_index(11)
        area = Polygon(P3(gx0, gy0), P3(gx0 + gw * 0.9, gy0), P3(gx0 + gw * 0.9, gy0 + gh)).set_fill(KC, 0.45).set_stroke(width=0).set_z_index(9)
        self.gat("cresce em linha reta")
        self.play(FadeIn(ax), Create(reta), run_time=0.9)
        self.gat("a área do triângulo")
        self.play(FadeIn(area), run_time=0.7)
        self.gat("metade de cento e trinta vezes um e meio")
        P3_, ip3, _ = self.linha(("K_{vol}", "=", r"\tfrac{1}{2}", "P", "t"), voos={2: area, 3: ax[5], 4: ax[4]}, size=48, rt=1.3)
        P4, ip4, p4b = self.gm(P3_, ip3, ("K_{vol}", "=", r"\tfrac{1}{2}", r"\cdot", "130", r"\cdot", r"1{,}5", "=", r"97{,}5\ \mathrm{J}"), sai=[3, 4],
                               voos={4: ax[5], 6: ax[4]}, cores={4: KC, 8: KC}, caixa_cor=KC, rt=1.3)
        self.tr_ok(3)
        self.ate(0.99)
        graf = VGroup(ax, reta, area)

        # ── E1-15: item e — o fio se solta; a pastilha (com volume) encosta; f_at = μ_c N; τ = f_at R₂ ──
        self.an("E1-15")
        self.sem_selo()
        self.tr_acende(4)
        self.pilha.limpa(anims=[FadeOut(graf), FadeOut(bv), FadeOut(nomes)])
        t_ini = self.clk.get_value()
        th0 = vol_th(1.5)
        self.v_thfn = lambda: th0 + W15 * (self.clk.get_value() - t_ini)
        vt["th"].clear_updaters()                                       # v5 ALIASING: um só updater de θ (o do E1-13 competia e dava salto de ângulo)
        vt["th"].add_updater(lambda m: m.set_value(self.v_thfn()))
        S15, C15 = 5.0, P3(-2.6, -0.55)                   # v5 §1.1: esquema 2.5D vivo (volante, tambor, fio, bloco e pastilha)
        self.modo25(C15, S15)
        self.v_flags["cord"] = True
        r15 = self.rig25_vivo()
        self.play(f3.op.animate.set_value(0.0), FadeIn(r15), run_time=0.8)
        self.gat("o fio se solta")
        self.play(vt["cai"].animate.set_value(3.0), run_time=1.0, rate_func=rate_functions.ease_in_quad)
        self.v_flags["cord"] = False
        self.v_flags["freio"] = True
        self.gat("uma pastilha encosta na borda do anel")
        topo = self.vp((0, 0.0, 0.47))
        s_N = seta_s(topo + 0.95 * UP, topo + 0.1 * UP, FC, 6)
        l_N = lbl(r"N=25\ \mathrm{N}", FC, 42).next_to((s_N._ini + s_N._fim) / 2, RIGHT, buff=0.25)
        mu_ = chamada_em(self.vp((-0.08, -0.04, 0.43)), lbl(r"\mu_c=0{,}40", WHITE_, 42), P3(-6.4, 2.6))
        self.play(FadeIn(s_N), FadeIn(l_N), run_time=0.5)
        self.gat("o coeficiente de atrito cinético")
        self.play(FadeIn(mu_), run_time=0.5)
        self.gat("o atrito é esse coeficiente vezes a normal")
        s_f = seta_s(topo + 0.05 * LEFT + 0.05 * DOWN, topo + 1.25 * LEFT + 0.05 * DOWN, FC, 6)
        l_f = lbl(r"f_{at}", FC, 42).next_to(s_f._fim, DOWN, buff=0.16).shift(0.1 * LEFT).set_z_index(22)
        self.play(FadeIn(s_f), FadeIn(l_f), run_time=0.5)
        F1, if1, _ = self.linha((r"f_{at}", "=", r"\mu_c", "N"), voos={0: l_f, 2: mu_[2], 3: l_N}, size=48, rt=1.1, metodo="lei")
        F2, if2, _ = self.gm(F1, if1, (r"f_{at}", "=", r"0{,}40", r"\cdot", "25", "=", r"10\ \mathrm{N}"), sai=[2, 3], voos={2: mu_[2], 4: l_N}, cores={6: FC}, rt=1.2)
        self.gat("o torque é dez vezes quarenta centímetros")
        pR2 = self.vp((-0.28, -0.04, -0.28))
        r2c = chamada_em(pR2, lbl(r"R_2=0{,}40\ \mathrm{m}", C_RAIO, 40), P3(-5.9, -2.4), cor=C_RAIO)
        r2h = VGroup(circ_raio(self.v_eixo(), 0.40 * S15, C_RAIO, 4.5, tracejado=False), linha_halo(self.v_eixo(), pR2, cor=C_RAIO, w=4.5))
        self.play(FadeIn(r2c), FadeIn(r2h), run_time=0.4)
        F3, if3, _ = self.linha((r"\tau", "=", r"f_{at}", "R_2"), voos={2: mp(F2, if2, [0]), 3: r2c[2]}, size=48, rt=1.0)
        F4, if4, f4b = self.gm(F3, if3, (r"\tau", "=", "10", r"\cdot", r"0{,}40", "=", r"4{,}0\ \mathrm{N\,m}"), sai=[2, 3],
                               voos={2: mp(F2, if2, [6]), 4: r2c[2]}, cores={6: FC}, caixa_cor=FC, rt=1.2)
        self.gat("a normal aponta direto para o eixo")
        nz = txt("BRAÇO ZERO", 26, bold=True, color=GEO).next_to(l_N, RIGHT, buff=0.3).set_z_index(22)         # v7: não cobre o μc nem o título
        self.play(FadeIn(nz), run_time=0.5)
        self.ate(0.99)

        # ── E1-16: Στ = Iα → α_f = τ/I; ω = ω₀ − α_f t (ω = 0) → t; ω² = ω₀² − 2α_fΔθ → Δθ; W = τΔθ = K_vol ──
        self.an("E1-16")
        self.selo("TEMPO REAL", "CALOR NA PASTILHA E NO ANEL")
        self.pilha.so(f4b, anims=[FadeOut(r2c), FadeOut(r2h), FadeOut(mu_)])
        self.gat("a desaceleração angular")
        H0, ih0, _ = self.lei("newton_rot", (r"\sum", r"\tau", "=", "I", r"\alpha"), rt=0.8)
        H1, ih1, _ = self.gm(H0, ih0, {"pre": (r"\alpha_f", "="), "num": (r"\tau",), "den": ("I",)}, sai=[0, 4], rt=1.0)
        H1b, ih1b, h1b = self.gm(H1, ih1, {"pre": (r"\alpha_f", "="), "num": (r"4{,}0",), "den": (r"2{,}0175",), "post": ("=", r"1{,}98\ \mathrm{rad/s^2}")},
                                 sai=[2, 4], voos={2: mp(F4, if4, [6])}, cores={6: ACC}, rt=1.2)
        tf = ValueTracker(0.0)
        self.add(tf)
        vt["th"].clear_updaters()
        thb = self.v_thfn()
        self.v_thfn = None
        vt["th"].set_value(thb)
        vt["th"].add_updater(lambda m: m.set_value(thb + freio_th(tf.get_value())))
        vt["heat"].add_updater(lambda m: m.set_value(clamp(1 - (1 - tf.get_value() / T_PARA) ** 2, 0, 1)))
        HB2, yb2 = 2.8, -3.1

        def barras_f():
            fr = clamp(1 - (1 - tf.get_value() / T_PARA) ** 2, 0, 1)
            g = VGroup()
            for x, h, cor in ((-6.85, (1 - fr) * HB2, KC), (-5.95, fr * HB2, HEAT)):
                g.add(Rectangle(width=0.58, height=HB2).move_to(P3(x, yb2 + HB2 / 2)).set_stroke(GEO, 1.6))
                if h > 0.005:
                    g.add(Rectangle(width=0.54, height=h).move_to(P3(x, yb2 + h / 2)).set_stroke(width=0).set_fill(cor, 1.0))
            return g.set_z_index(12)

        bf = vivo(barras_f)
        nb = VGroup(lbl("K_{vol}", KC, 40).move_to(P3(-6.85, yb2 + HB2 + 0.36)), txt("CALOR", 30, bold=True, color=HEAT).move_to(P3(-5.85, yb2 + HB2 + 0.75)))
        contf = vivo(lambda: lbl(r"\Delta\theta=" + br(freio_th(tf.get_value()), 1) + r"\ \mathrm{rad}", ANG, 40).move_to(P3(-6.1, 1.0)).set_z_index(20))
        self.gat("para zerar nove vírgula oito três")
        self.play(FadeIn(bf), FadeIn(nb), FadeIn(contf), run_time=0.4)
        self.play(tf.animate.set_value(T_PARA), run_time=T_PARA, rate_func=linear)
        self.pilha.so(f4b, h1b)
        T0, it0, _ = self.linha((r"\omega", "=", r"\omega_0", "-", r"\alpha_f", "t"), rt=0.9, metodo="lei")
        T1, it1, _ = self.gm(T0, it0, {"pre": ("t", "="), "num": (r"\omega_0",), "den": (r"\alpha_f",), "post": ("=", r"4{,}96\ \mathrm{s}")}, riscar=[0], sai=[1, 3], rt=1.3)
        self.gat("velocidade angular ao quadrado sobre duas vezes")
        self.pilha.so(f4b, h1b, T1)
        Q0, iq0, _ = self.linha((r"\omega^2", "=", r"\omega_0^2", "-", r"2", r"\alpha_f", r"\Delta\theta"), rt=1.0, metodo="lei")
        Q1, iq1, q1b = self.gm(Q0, iq0, {"pre": (r"\Delta\theta", "="), "num": (r"\omega_0^2",), "den": ("2", r"\alpha_f"), "post": ("=", r"24{,}4\ \mathrm{rad}")},
                               riscar=[0], sai=[1, 3], cores={7: ANG}, rt=1.3)
        self.gat("o trabalho do atrito é o torque vezes o ângulo")
        self.pilha.so(f4b, q1b)
        W0, iw0, _ = self.linha(("W", "=", r"\tau", r"\Delta\theta"), voos={2: mp(F4, if4, [0]), 3: mp(Q1, iq1, [0])}, rt=1.0)
        W1, iw1, _ = self.gm(W0, iw0, ("W", "=", r"4{,}0", r"\cdot", r"24{,}4", "=", r"97{,}5\ \mathrm{J}"), sai=[2, 3],
                             voos={2: mp(F4, if4, [6]), 4: mp(Q1, iq1, [7])}, cores={6: KC}, rt=1.2)
        W2, iw2, _ = self.gm(W1, iw1, ("W", "=", "K_{vol}", r"\ \checkmark"), mapas=[([6], [2])], sai=[2, 3, 4, 5], cores={3: ACC}, caixa_cor=KC, rt=0.9)
        self.gat("virou calor na pastilha e no anel")
        self.tr_ok(4)
        self.ate(0.99)
        vt["th"].clear_updaters()
        vt["heat"].clear_updaters()

        # ── E1-17: item f — o aro fino lado a lado; a fórmula volta e SÓ o I troca; os dois param em t = 1,5 s ──
        self.an("E1-17")
        self.selo("OUTRO VOLANTE", "SOLTO DO REPOUSO · MESMOS 20 KG")
        self.tr_acende(5)
        self.pilha.limpa(anims=[FadeOut(VGroup(bf, nb, contf, s_N, l_N, s_f, l_f, nz))])
        self.play(FadeOut(r15), run_time=0.4)
        self.v_flags.update(freio=False, cord=True, dois=True)
        vt["cai"].set_value(0.0)
        vt["heat"].set_value(0.0)
        vt["th"].set_value(0.0)
        vt["th2"].set_value(0.0)
        vt["K"].set_value(3.1)
        vt["yc"].set_value(2.75)
        vt["alvo_x"].set_value(0.625 - (-3.45 + 3.85) / 3.1)
        S17, C17 = 3.7, P3(-6.05, 1.6)                   # v5 §1.1: dois volantes lado a lado no esquema 2.5D (o aro fino à direita)
        self.modo25(C17, S17)
        r17 = self.rig25_vivo()
        self.play(FadeIn(r17), run_time=0.5)
        self.gat("todos num aro fino")
        J0, ij0, _ = self.linha({"pre": ("a", "="), "num": ("g",), "den": ("1", r"+\tfrac{I}{m\,r^2}")}, caixa_cor=ACC, rt=1.0, metodo="lei")
        self.gat("o momento de inércia do aro")
        A0, ja0, _ = self.linha(("I_{aro}", "=", "M", "R^2"), rt=0.9, metodo="lei")
        A1, ja1, _ = self.gm(A0, ja0, ("I_{aro}", "=", "20", r"\cdot", r"0{,}40^2", "=", r"3{,}2\ \mathrm{kg\,m^2}"), sai=[2, 3], cores={2: MAS, 4: GEO, 6: MAS}, rt=1.2)
        self.gat("a inércia equivalente pula")
        J1, ij1, _ = self.gm(J0, ij0, {"pre": ("a", "="), "num": ("g",), "den": ("1", r"+\tfrac{I_{aro}}{m\,r^2}")}, sai=[5], voos={5: mp(A1, ja1, [0])}, caixa_cor=ACC, rt=1.1)
        self.gat("e a aceleração do bloco cai")
        J2, ij2, _ = self.gm(J1, ij1, {"pre": ("a", "="), "num": (r"9{,}8",), "den": ("1", r"+14{,}2")}, sai=[2, 5], cores={2: ACC}, rt=1.1)
        J3, ij3, _ = self.gm(J2, ij2, ("a", "=", r"0{,}644\ \mathrm{m/s^2}"), cores={2: ACC}, caixa_cor=ACC, rt=0.9)
        ts3 = ValueTracker(0.0)
        self.add(ts3)
        vt["th"].add_updater(lambda m: m.set_value(vol_th(min(1.5, ts3.get_value()))))                      # v2 §6.1: os dois param em 1,5 s
        vt["th2"].add_updater(lambda m: m.set_value(AL_ARO * min(1.5, ts3.get_value()) ** 2 / 2))
        k_a = 0.85                    # v7: as setas de aceleração não saem pelo rodapé durante a queda
        setas = vivo(lambda: VGroup(seta_s(self.vp((0.158, Y_TB, ZB - 0.15 * vt["th"].get_value() - 0.12)), self.vp((0.158, Y_TB, ZB - 0.15 * vt["th"].get_value() - 0.12)) + A_VOL * k_a * DOWN, ACC, 6),
                                    seta_s(self.vp((1.408, Y_TB, ZB - 0.15 * vt["th2"].get_value() - 0.12)), self.vp((1.408, Y_TB, ZB - 0.15 * vt["th2"].get_value() - 0.12)) + A_ARO * k_a * DOWN, ACC, 6)).set_z_index(14))
        la = VGroup(lbl(r"0{,}983", ACC, 40), lbl(r"0{,}644", ACC, 40))
        def _acima_(m_):                                       # v7: o número do bloco que saiu de quadro fica acima da borda de baixo
            if m_.get_y() < -3.3:
                m_.set_y(-3.3)
            return m_
        la_v = vivo(lambda: VGroup(_acima_(la[0].copy().next_to(self.vp((0.158, Y_TB, ZB - 0.15 * vt["th"].get_value())), LEFT, buff=0.55)),
                                   _acima_(la[1].copy().next_to(self.vp((1.408, Y_TB, ZB - 0.15 * vt["th2"].get_value())), RIGHT, buff=0.45))).set_z_index(14))
        self.play(FadeIn(setas), FadeIn(la_v), FadeOut(self._tr), FadeOut(self._tr_ok), run_time=0.5)      # a trilha sai durante a queda (os blocos descem até ela)
        self.play(ts3.animate.set_value(1.5), run_time=1.5, rate_func=linear)
        self.wait(0.6)
        self.play(FadeOut(setas), FadeOut(la_v), FadeOut(r17), run_time=0.4)          # os blocos voltam ao repouso por fade (sem giro de volta)
        vt["th"].clear_updaters()
        vt["th2"].clear_updaters()
        vt["th"].set_value(0.0)
        vt["th2"].set_value(0.0)
        self.play(FadeIn(r17), FadeIn(self._tr), FadeIn(self._tr_ok), run_time=0.4)
        self.tr_ok(5)
        self.ate(0.99)
        vt["th"].clear_updaters()
        vt["th2"].clear_updaters()

        # ── E1-18: moral + DICA ──
        self.an("E1-18")
        self.selo("DICA", "SEPARA OS CORPOS · UMA EQUAÇÃO POR CORPO · O VÍNCULO AMARRA")
        self.pilha.limpa()
        self.gat("a massa total não decide sozinha")
        m1 = VGroup(txt("MESMOS 20 KG,", 32, bold=True, color=MAS), txt("ACELERAÇÕES DIFERENTES", 32, bold=True, color=ACC)).arrange(DOWN, buff=0.1)
        self.pilha.poe(m1)
        self.play(FadeIn(m1, shift=0.1 * UP), run_time=0.6)
        self.gat("decide onde ela está")
        F_, if_, _ = self.linha({"pre": ("a", "="), "num": ("g",), "den": ("1", r"+\tfrac{I}{m\,r^2}")}, size=52, rt=1.2, caixa_cor=ACC, metodo="lei")
        self.gat("que transforma três incógnitas")
        self.play(self.ind_copia(self._tr, ACC, 1.06, 0.9), run_time=0.9)
        self.ate(0.99)

    def r_tambor_lbl(self):
        """Rótulo r = 0,15 m preso ao tambor (chamada fora do volante), para o vínculo h = rΔθ e v = rω."""
        if getattr(self, "_rt_lbl", None) is None:
            p = self.vp((-0.15, -0.09, 0.0))
            self._rt_lbl = chamada(p, lbl(r"r=0{,}15\ \mathrm{m}", C_RAIO, 40), LEFT + 0.2 * UP, 2.2, cor=C_RAIO)
            self.play(FadeIn(self._rt_lbl), run_time=0.4)
        return self._rt_lbl[2]

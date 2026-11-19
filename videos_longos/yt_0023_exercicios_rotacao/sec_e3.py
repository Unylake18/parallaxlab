"""Lote PE3 (v2): E3-1 a E3-10 — o carretel com números (Three.js, garfo + eixo único, trava em pino). 3/4 com os enrolamentos opostos;
previsão por energia (massa × raio, g e Δθ cancelando); dolly até a frontal (eixo para a câmera, centros coincidem) antes dos diagramas;
ΣF = ma e Στ = Iα → cinco equações montadas da esquerda para a direita; α fechado por glyph map (os termos com α atravessam);
números; trações; as duas verificações; energia em 1,0 m (o MESMO carretel 3D, zoom contínuo); 18 kg parado; dica."""
from pecas23 import *  # noqa: F401,F403
from sec_ph import Z1, Z2, XB1, XB2
from sec_e1a import chamada, chamada_em

YG, YP = 0.05, -0.085
K0, Y0 = 4.0, 0.6
K3, Y3 = 6.4, 0.95          # v5 §1.2: frontal do carretel ≥ 50% da altura útil (Rg = 1,96 u); os blocos pendem comprimidos (comp) para caber


class LoteE3(Lote23):
    def corpo(self):
        tc = ValueTracker(0.0)
        th_x = ValueTracker(0.0)        # giro extra (E3-2: ângulo pequeno de ida e volta)
        ucam = ValueTracker(0.0)
        Kc = ValueTracker(K0)
        ycc = ValueTracker(Y0)
        trava = ValueTracker(1.0)
        flash = ValueTracker(0.0)
        m2 = ValueTracker(10.0)
        # v3 §2: planos de câmera por mistura (wov) entre a trilha 3/4 → frontal (ucam) e um plano manual (az, el, K, xc, yc, alvo)
        wov, maz, mel, mK, mxc, myc, max_, maz_ = [ValueTracker(v) for v in (0.0, -56.0, 14.0, K0, -3.85, Y0, 0.0, 0.0)]
        exc, ff1, ff2 = ValueTracker(0.0), ValueTracker(0.0), ValueTracker(0.0)
        comp = ValueTracker(1.0)        # 1 = pendura como no 3D; < 1 = o esquema 2.5D encurta o fio (E3-3 a E3-7)
        foco_c = {"v": ""}
        self.add(tc, th_x, ucam, Kc, ycc, trava, flash, m2, wov, maz, mel, mK, mxc, myc, max_, maz_, exc, ff1, ff2, comp)

        def cam():
            b = cam_car(ucam.get_value(), K=Kc.get_value(), yc=ycc.get_value())
            w = wov.get_value()
            if w <= 1e-6:
                return b
            m = dict(b)
            for k, tg in (("az", maz), ("el", mel), ("K", mK), ("xc", mxc), ("yc", myc)):
                m[k] = round(b[k] + w * (tg.get_value() - b[k]), 4)
            m["alvo"] = [round(b["alvo"][0] + w * (max_.get_value() - b["alvo"][0]), 4), 0.0, round(b["alvo"][2] + w * (maz_.get_value() - b["alvo"][2]), 4)]
            return m

        def plano(nome, az, el, K, xc, yc, ax=0.0, az_=0.0, rt=1.3, extra=()):
            """Plano de câmera nomeado (v3 §2.1): movimento contínuo (ease in-out) e linha [cam] no log."""
            print(f"[cam] {nome} az={az} el={el} K={K}", flush=True)
            self.play(wov.animate.set_value(1.0), maz.animate.set_value(az), mel.animate.set_value(el), mK.animate.set_value(K), mxc.animate.set_value(xc),
                      myc.animate.set_value(yc), max_.animate.set_value(ax), maz_.animate.set_value(az_), *extra, run_time=rt, rate_func=smooth)

        def thv():
            return car_th(tc.get_value()) + th_x.get_value()

        def est(t):
            th = thv()
            e = {"th": th, "trava": round(trava.get_value(), 3), "esp_flash": round(flash.get_value(), 3), "z1": Z1, "z2": Z2, "m2": m2.get_value(), "cam": cam(),
                 "explode": round(exc.get_value(), 3), "fio_flash": [round(ff1.get_value(), 3), round(ff2.get_value(), 3)], "foco": foco_c["v"]}
            if not PEDIDOS3D:
                c = cam()
                self.reg("carretel", th=th, eixo=pr(c, (0, 0, 0)), b1=pr(c, (XB1, YG, Z1 - RC * th)), b2=pr(c, (XB2, YP - 0.15 * exc.get_value(), Z2 + rc * th)),
                         vinc1=(Z1 - (Z1 - RC * th)) / max(1e-9, th) if th else RC, vinc2=((Z2 + rc * th) - Z2) / max(1e-9, th) if th else rc)
            return r4(e)

        f3 = Fundo3D(self, "carretel", est, op=0.0)
        self.add(f3)
        self.f3 = f3
        def _comp(p, ta):
            c_ = comp.get_value()
            return p if c_ >= 0.9999 else np.array([p[0], ta[1] + c_ * (p[1] - ta[1]), 0.0])
        pb1 = lambda dz=0.0: _comp(pr(cam(), (XB1, YG, Z1 - RC * thv() + dz)), pr(cam(), (XB1, YG, 0.0)))
        def pb2(dz=0.0):                                 # v6 §2 #8: o bloco do fio pequeno pende por baixo do disco (≥ 0,3 u da borda), não por cima dele
            cc_ = cam()
            ta_ = pr(cc_, (XB2, YP, 0.0))
            p0 = _comp(pr(cc_, (XB2, YP, Z2 + rc * thv())), ta_)
            p1 = _comp(pr(cc_, (XB2, YP, Z2 + rc * thv() + dz)), ta_)
            if comp.get_value() >= 0.9999:
                return p1
            o_ = pr(cc_, (0, 0, 0))
            Rg_ = float(np.linalg.norm(pr(cc_, (XB1, YG, 0.0)) - o_))
            lim = o_[1] - Rg_ - 0.3 - 0.5 * L2() * Rg_ / RC
            return p1 + np.array([0.0, min(0.0, lim - p0[1]), 0.0])
        L2 = lambda: 0.166 * (m2.get_value() / 10) ** (1 / 3)
        rot = vivo(lambda: VGroup(lbl(r"m_1=6{,}0\ \mathrm{kg}", MAS, 40).next_to(pb1(), DOWN, buff=0.95).shift(0.35 * RIGHT),
                                  lbl((r"m_2=18\ \mathrm{kg}" if m2.get_value() > 14 else r"m_2=10{,}0\ \mathrm{kg}"), MAS, 40).next_to(pb2(), LEFT, buff=0.72 + 1.2 * (L2() - 0.166))).set_z_index(20))

        # ── E3-1 ──
        self.an("E3-1")
        self.secao("EXERCÍCIO 3 · O CARRETEL")
        self.play(f3.op.animate.set_value(1.0), run_time=0.45)       # R4-v9: rótulo só depois do objeto inteiro
        self.play(FadeIn(rot), run_time=0.25)
        self.gat("momento de inércia de zero vírgula cinco")
        d0 = VGroup(txt("CARRETEL:", 30, bold=True, color=GEO), lbl(r"I=0{,}50\ \mathrm{kg\,m^2}", MAS, 44)).arrange(RIGHT, buff=0.2)
        self.pilha.poe(d0)
        self.play(FadeIn(d0, shift=0.08 * UP), run_time=0.5)
        self.gat("o tambor grande tem trinta centímetros")
        foco_c["v"] = "grande"
        plano("E3-1 PERFIL", 0.0, 3.0, 5.0, -3.85, 0.5, rt=1.4, extra=(FadeOut(rot),))
        cP = cam()
        c2R = cota23(pr(cP, (0.0, YG, RC)), pr(cP, (0.0, YG, -RC)), lbl(r"2R=0{,}60\ \mathrm{m}", C_RAIO, 40), lado=RIGHT, d=2.3, cor=C_RAIO)
        t_perf = txt("DOIS TAMBORES · MESMO EIXO · GIRAM JUNTOS", 26, bold=True, color=GEO_CL)
        t_perf.scale_to_fit_width(min(t_perf.width, 6.2))
        t_perf = VGroup(pilula(t_perf, GEO, 0.12), t_perf).move_to(P3(-3.85, -3.75)).set_z_index(16)
        d1 = VGroup(txt("TAMBOR GRANDE:", 30, bold=True, color=GEO), lbl(r"R=0{,}30\ \mathrm{m}", C_RAIO, 44)).arrange(RIGHT, buff=0.2)
        self.pilha.poe(d1)
        self.play(FadeIn(d1, shift=0.08 * UP), FadeIn(c2R), FadeIn(t_perf), run_time=0.6)
        self.gat("o pequeno tem dez")
        foco_c["v"] = "pequeno"
        plano("E3-1 EXPLODIDO", -25.0, 12.0, 2.9, -3.85, -0.2, 0.0, -0.03, rt=1.2, extra=(exc.animate.set_value(1.0), FadeOut(c2R)))
        cE = cam()
        c2r = cota23(pr(cE, (0.0, YP - 0.15, rc)), pr(cE, (0.0, YP - 0.15, -rc)), lbl(r"2r=0{,}20\ \mathrm{m}", C_RAIO_MENOR, 40), lado=LEFT, d=1.6, cor=C_RAIO_MENOR)
        d2 = VGroup(txt("TAMBOR PEQUENO:", 30, bold=True, color=GEO), lbl(r"r=0{,}10\ \mathrm{m}", C_RAIO_MENOR, 44)).arrange(RIGHT, buff=0.2)
        self.pilha.poe(d2)
        self.play(FadeIn(d2, shift=0.08 * UP), FadeIn(c2r), run_time=0.6)
        self.gat("com o fio em sentido contrário")
        foco_c["v"] = ""
        plano("E3-1 CLOSE", -50.0, 10.0, 4.1, -3.85, -0.27, 0.05, -0.25, rt=1.3, extra=(exc.animate.set_value(0.0), FadeOut(c2r), FadeOut(t_perf)))
        cC = cam()
        l_a = lbl(r"\mathrm{ESTE\ FIO}\to 6{,}0\ \mathrm{kg}", MAS, 34)
        l_b = lbl(r"\mathrm{ESTE\ FIO}\to 10{,}0\ \mathrm{kg}", MAS, 34)
        ca = chamada_em(pr(cC, (RC + 0.008, YG, -0.15)), l_a, P3(1.6, -1.8), cor=MAS)
        cb_ = chamada_em(pr(cC, (-(rc + 0.008), YP, -0.15)), l_b, P3(-5.2, -2.0), cor=MAS)
        d3 = txt("ENROLAMENTOS OPOSTOS", 30, bold=True, color=GEO)
        self.pilha.poe(d3)
        self.play(FadeIn(d3, shift=0.08 * UP), FadeIn(ca), ff1.animate.set_value(1.0), run_time=0.6)
        self.play(FadeIn(cb_), ff1.animate.set_value(0.0), ff2.animate.set_value(1.0), run_time=0.6)
        self.play(ff2.animate.set_value(0.0), run_time=0.4)
        self.gat("antes da conta qual desce")
        self.play(FadeOut(ca), FadeOut(cb_), run_time=0.4)                          # v7 E3-1: as chamadas saem ANTES de o rótulo de m₂ entrar (nunca dois textos no mesmo ponto)
        self.play(wov.animate.set_value(0.0), FadeIn(rot), run_time=0.9, rate_func=smooth)
        self.selo("ANTES DA CONTA", "QUAL DESCE?")
        self.ate(0.99)

        # ── E3-2: previsão por energia: perde m₁gRΔθ, ganha m₂grΔθ; g e Δθ cancelam ──
        self.an("E3-2")
        self.selo("QUEM DECIDE", "MASSA × RAIO")
        self.pilha.limpa()
        print("[cam] E3-2 GERAL quase frontal az=-73", flush=True)
        self.play(ucam.animate.set_value(0.5), run_time=1.0, rate_func=smooth)
        c = cam()
        cR = chamada(pr(c, (0.0, YG - 0.06, RC * 0.98)), lbl(r"R=0{,}30\ \mathrm{m}", C_RAIO, 40), RIGHT + 0.35 * UP, 2.6, cor=C_RAIO)
        cr = chamada(pr(c, (-0.07, YP - 0.05, 0.07)), lbl(r"r=0{,}10\ \mathrm{m}", C_RAIO_MENOR, 40), 0.75 * LEFT + UP, 1.7, cor=C_RAIO_MENOR)
        self.play(FadeIn(cR), FadeIn(cr), run_time=0.5)
        self.gat("imagina um giro pequeno")
        DTH = 0.5
        y1a, y2a = pb1(0.056)[1], pb2(0.08)[1]
        self.play(th_x.animate.set_value(DTH), run_time=1.6)
        x1, x2 = pb1()[0] + 0.62, pb2()[0] - 0.7
        rg1 = VGroup(Line(P3(x1, y1a), P3(x1, pb1(0.056)[1])).set_stroke(GEO, 3.5), lbl(r"R\,\Delta\theta", GEO, 40).next_to(P3(x1 + 0.1, (y1a + pb1(0.056)[1]) / 2), RIGHT, buff=0.12))
        rg2 = VGroup(Line(P3(x2, y2a), P3(x2, pb2(0.08)[1])).set_stroke(GEO, 3.5), lbl(r"r\,\Delta\theta", GEO, 40).next_to(P3(x2 - 0.1, pb2(0.08)[1] + 0.2), LEFT, buff=0.12))
        self.gat("o leve desce o ângulo vezes trinta centímetros")
        self.play(FadeIn(rg1), run_time=0.5)
        self.gat("o pesado sobe o mesmo ângulo")
        self.play(FadeIn(rg2), run_time=0.5)
        self.gat("compara a energia potencial")
        A, ia, _ = self.linha((r"\mathrm{perde}:", "m_1", "g", "R", r"\Delta\theta"), voos={3: rg1[1][0][0], 4: rg1[1]}, rt=1.1)
        B, ib, _ = self.linha((r"\mathrm{ganha}:", "m_2", "g", "r", r"\Delta\theta"), voos={3: rg2[1][0][0], 4: rg2[1]}, rt=1.1)
        self.gat("o leve perde seis vezes")
        A2, ia2, _ = self.gm(A, ia, ("m_1", "R", "=", r"6{,}0", r"\cdot", r"0{,}30", "=", r"1{,}8"), riscar=[2, 4], sai=[0],
                             voos={3: rot[0][0], 5: cR[2]}, cores={7: MAS}, rt=1.3)
        self.gat("o pesado ganha dez vezes")
        B2, ib2, _ = self.gm(B, ib, ("m_2", "r", "=", r"10", r"\cdot", r"0{,}10", "=", r"1{,}0"), riscar=[2, 4], sai=[0],
                             voos={3: rot[0][1], 5: cr[2]}, cores={7: MAS}, rt=1.3)
        self.gat("sobra energia")
        D_, id_, db = self.linha(("m_1", "R", ">", "m_2", "r"), voos={0: mp(A2, ia2, [0]), 1: mp(A2, ia2, [1]), 3: mp(B2, ib2, [0]), 4: mp(B2, ib2, [1])},
                                 size=52, rt=1.0, caixa_cor=MAS)
        self.play(th_x.animate.set_value(0.0), FadeOut(rg1), FadeOut(rg2), run_time=1.0)
        self.ate(0.99)

        # ── E3-3: dolly até a frontal (centros coincidem); diagramas de corpo livre com rótulos FORA do carretel e dos blocos ──
        self.an("E3-3")
        self.sem_selo()
        self.pilha.limpa(anims=[FadeOut(cR), FadeOut(cr)])
        self.gat("quem faz torque não são os pesos")
        self.play(ucam.animate.set_value(1.0), Kc.animate.set_value(6.0), ycc.animate.set_value(1.1), run_time=3.0, rate_func=smooth)        # o 3D fecha em K = 6,0 (o bloco pesado não corta a borda de baixo)
        c = cam()
        o_ = pr(c, (0, 0, 0))
        t1 = pr(c, (XB1, YG, 0.0))
        t2 = pr(c, (XB2, YP, 0.0))
        k = 1.05 / (M2 * G)
        print("[cam] E3-3 FRONTAL-FÍSICA", flush=True)
        sc25 = abs(t1[0] - o_[0]) / RC
        Rg25, Rp25 = abs(t1[0] - o_[0]), abs(t2[0] - o_[0])

        def esq25():
            cc = cam()
            o = pr(cc, (0, 0, 0))
            th0 = thv()
            ta = pr(cc, (XB1, YG, 0.0))
            tang = np.array([-(ta[1] - o[1]), ta[0] - o[0], 0.0])
            dl_ = pr(cc, (XB1, YG, Z1 - RC * (th0 + 0.02))) - pr(cc, (XB1, YG, Z1 - RC * th0))
            sg = 1.0 if float(np.dot(tang, dl_)) >= 0 else -1.0
            ta2 = pr(cc, (XB2, YP, 0.0))
            Rg_, Rp_ = float(np.linalg.norm(ta - o)), float(np.linalg.norm(ta2 - o))        # escala viva (o zoom K = 6,0 → 7,2 acontece depois da troca 3D → 2.5D)
            sc_ = Rg_ / RC
            g_ = VGroup(carretel25(o, Rg_, Rp_, sg * th0))
            b1_, b2_ = pb1(), pb2()
            s1_, s2_ = 0.14 * sc_, L2() * sc_
            g_.add(Line(ta, b1_ + 0.5 * s1_ * UP).set_stroke(HALO, 6).set_z_index(5), Line(ta, b1_ + 0.5 * s1_ * UP).set_stroke(LINHA_CL, 2.4).set_z_index(5.1),
                   Line(ta2, b2_ + 0.5 * s2_ * UP).set_stroke(HALO, 6).set_z_index(5), Line(ta2, b2_ + 0.5 * s2_ * UP).set_stroke(LINHA_CL, 2.4).set_z_index(5.1))
            g_.add(bloco25(b1_, s1_).set_z_index(6), bloco25(b2_, s2_).set_z_index(6))
            return g_
        esq = vivo(esq25)
        self.add(esq)
        self.play(f3.op.animate.set_value(0.0), comp.animate.set_value(0.6), Kc.animate.set_value(K3), ycc.animate.set_value(Y3), run_time=0.8)       # match cut 3D → 2.5D; o fio encurta e o carretel cresce
        c = cam()
        o_ = pr(c, (0, 0, 0))
        t1 = pr(c, (XB1, YG, 0.0))
        t2 = pr(c, (XB2, YP, 0.0))
        Rg25, Rp25 = abs(t1[0] - o_[0]), abs(t2[0] - o_[0])
        p1, p2 = pb1(), pb2()
        q1, q2 = pb1(0.056), pb2(0.4 * L2())
        cR3 = VGroup(linha_halo(o_, t1, cor=C_RAIO, w=4.5), chamada_em(t1, lbl(r"R=0{,}30\ \mathrm{m}", C_RAIO, 34), P3(-0.62, 2.5), cor=C_RAIO))
        cr3 = VGroup(linha_halo(o_, t2, cor=C_RAIO_MENOR, w=4.5), chamada_em(t2, lbl(r"r=0{,}10\ \mathrm{m}", C_RAIO_MENOR, 34), P3(-6.6, 2.9), cor=C_RAIO_MENOR))
        cc3 = VGroup(circ_raio(o_, Rg25, C_RAIO, 4.0, tracejado=False), circ_raio(o_, Rp25, C_RAIO_MENOR, 4.0, tracejado=True))
        pt3 = VGroup(*[VGroup(Dot(p_, radius=0.09, color=HALO), Dot(p_, radius=0.055, color=cor_)) for p_, cor_ in ((t1, C_RAIO), (t2, C_RAIO_MENOR))]).set_z_index(18)
        self.play(FadeIn(cc3), FadeIn(cR3), FadeIn(cr3), FadeIn(pt3), run_time=0.6)
        nota = VGroup(txt("TORQUE: AS TRAÇÕES", 30, bold=True, color=FC), txt("EM MOVIMENTO: TRAÇÃO ≠ PESO", 30, bold=True, color=GEO)).arrange(DOWN, buff=0.1)
        self.pilha.poe(nota)
        self.play(FadeIn(nota, shift=0.08 * UP), run_time=0.6)
        self.gat("no bloco leve o peso para baixo")
        s_m1 = seta_s(p1 + 0.45 * DOWN, p1 + (0.45 + M1 * G * k) * DOWN, FC, 6)
        s_T1 = seta_s(q1, q1 + 0.75 * UP, FC, 6)
        l_m1 = lbl("m_1g", FC, 40).next_to(s_m1._fim, RIGHT, buff=0.18)
        l_T1 = lbl("T_1", FC, 40).next_to(s_T1._fim, RIGHT, buff=0.18)
        self.play(FadeIn(VGroup(s_m1, s_T1, l_m1, l_T1)), FadeOut(rot), run_time=0.6)
        self.gat("no pesado o peso para baixo")
        s_m2 = seta_s(p2 + 0.5 * DOWN, p2 + (0.5 + M2 * G * k) * DOWN, FC, 6)
        s_T2 = seta_s(q2, q2 + 0.8 * UP, FC, 6)
        l_m2 = lbl("m_2g", FC, 40).next_to(s_m2._fim, LEFT, buff=0.18)
        l_T2 = lbl("T_2", FC, 40).next_to(s_T2._ini + 0.35 * UP, LEFT, buff=0.9)
        self.play(FadeIn(VGroup(s_m2, s_T2, l_m2, l_T2)), run_time=0.6)
        self.gat("no carretel cada tração puxa")
        s_c1 = seta_s(t1, t1 + 0.85 * DOWN, FC, 6)
        l_c1 = lbl("T_1", FC, 40).next_to(t1 + 0.42 * DOWN, RIGHT, buff=0.32)
        a_c1 = arco_torque(o_, r=Rg25 + 0.3, sentido=-1, a0=0.95, amp=0.85, cor=FC)
        self.play(FadeIn(s_c1), FadeIn(l_c1), FadeIn(a_c1), run_time=0.6)
        self.gat("a borda do seu tambor")
        s_c2 = seta_s(t2, t2 + 0.85 * DOWN, FC, 6)
        l_c2 = chamada_em(t2 + 0.5 * DOWN, lbl("T_2", FC, 40), P3(-6.9, 0.45), cor=FC)
        a_c2 = arco_torque(o_, r=Rp25 * 1.5, sentido=1, a0=1.9, amp=1.2, cor=FC, w=5)
        self.play(FadeIn(s_c2), FadeIn(l_c2), FadeIn(a_c2), run_time=0.6)
        self.gat("os torques também são opostos")
        bz_t = VGroup(txt("NO CENTRO:", 26, bold=True, color=GEO), txt("BRAÇO ZERO", 26, bold=True, color=GEO)).arrange(DOWN, buff=0.06).move_to(P3(-6.35, -2.25))
        bz = VGroup(Line(bz_t.get_right() + 0.1 * RIGHT, o_).set_stroke(GEO, 2), Dot(o_, radius=0.045, color=GEO), bz_t).set_z_index(16)
        self.play(FadeIn(bz), Indicate(a_c1, color=None), Indicate(a_c2, color=None), run_time=0.9)
        self.ate(0.99)
        fbd = VGroup(cc3, s_m1, s_T1, l_m1, l_T1, s_m2, s_T2, l_m2, l_T2, s_c1, l_c1, a_c1, s_c2, l_c2, a_c2, bz, cR3, cr3, pt3)

        # ── E3-4: ΣF = ma → LEVE e PESADO; Στ = Iα → CARRETEL; v = ωr → os dois vínculos (forças, braços voando do desenho) ──
        self.an("E3-4")
        self.selo("CINCO EQUAÇÕES", "DOIS BLOCOS · CARRETEL · DOIS VÍNCULOS")
        self.pilha.limpa()
        self.gat("bloco leve peso menos primeira tração")
        F0, if0, _ = self.linha((r"\sum", "F", "=", "m", "a"), rt=0.8, metodo="lei")
        e1, ie1, g1 = self.gm(F0, if0, ("m_1", "g", "-", "T_1", "=", "m_1", "a_1"), sai=[0, 1], mapas=[([3], [5]), ([4], [6])],
                              voos={0: l_m1[0][0:2], 1: l_m1[0][2:], 3: l_T1}, tag="LEVE", rt=1.3)
        self.gat("bloco pesado segunda tração menos peso")
        e2, ie2, g2 = self.gm(F0, if0, ("T_2", "-", "m_2", "g", "=", "m_2", "a_2"), sai=[0, 1], mapas=[([3], [5]), ([4], [6])],
                              voos={0: l_T2, 2: l_m2[0][0:2], 3: l_m2[0][2:]}, tag="PESADO", rt=1.3)
        self.gat("carretel primeira tração vezes raio grande")
        self.pilha.so(g1, g2)
        L0, il0, _ = self.lei("newton_rot", (r"\sum", r"\tau", "=", "I", r"\alpha"), rt=0.8)
        e3, ie3, g3 = self.gm(L0, il0, ("T_1", "R", "-", "T_2", "r", "=", "I", r"\alpha"), sai=[0, 1], voos={0: l_c1, 3: l_c2[2]}, rt=1.4)
        self.gat("e dois vínculos")
        self.pilha.so(g1, g2, g3)
        P0, ip0, _ = self.lei("pontes", ("v", "=", r"\omega", "r"), rt=0.7)
        e4, ie4, g4 = self.gm(P0, ip0, ("a_1", "=", r"\alpha", "R"), mapas=[([0], [0]), ([2], [2]), ([3], [3])], tag="VÍNCULO", rt=1.0)
        e5, ie5, g5 = self.gm(P0, ip0, ("a_2", "=", r"\alpha", "r"), mapas=[([0], [0]), ([2], [2])], tag="VÍNCULO", rt=1.0)
        self.pilha.so(g1, g2, g3, g4, g5, rt=0.4)
        self.ate(0.99)

        # ── E3-5: α fechado — trações isoladas, voando para o carretel; os termos com α atravessam; α em evidência ──
        self.an("E3-5")
        self.sem_selo()
        self.card_sai()
        self.play(FadeOut(fbd), run_time=0.4)
        self.gat("isola as trações")
        self.pilha.so(g1, g2, g3)
        T1a, it1a, t1b = self.gm(e1, ie1, ("T_1", "=", "m_1", "g", "-", "m_1", r"\alpha", "R"), mapas=[([6], [6, 7])], rt=1.2)
        T2a, it2a, t2b = self.gm(e2, ie2, ("T_2", "=", "m_2", "g", "+", "m_2", r"\alpha", "r"), mapas=[([1], [4]), ([6], [6, 7])], rt=1.2)
        self.pilha.so(g3, t1b, t2b)
        # cada tração vezes o seu raio (linhas curtas); depois os termos com α atravessam para a direita do carretel
        S1, is1, s1b = self.gm(T1a, it1a, ("T_1", "R", "=", "m_1", "g", "R", "-", "m_1", "R^2", r"\alpha"), mapas=[([7], [5, 8])], rt=1.2)
        S2, is2, s2b = self.gm(T2a, it2a, ("T_2", "r", "=", "m_2", "g", "r", "+", "m_2", "r^2", r"\alpha"), mapas=[([7], [5, 8])], rt=1.2)
        self.gat("aparece algo bonito")
        self.pilha.so(g3, s1b, s2b)
        C1a, ic1a, c1ab = self.gm(S1, is1, ("m_1", "g", "R", "-", "m_2", "g", "r"), sai=[0, 1, 2, 6, 7, 8, 9], voos={3: mp(S2, is2, [6]), 4: mp(S2, is2, [3]),
                                                                                                             5: mp(S2, is2, [4]), 6: mp(S2, is2, [5])}, rt=1.3)
        C1b, ic1b, _ = self.linha(("=", "I", r"\alpha", "+", "m_1", "R^2", r"\alpha", "+", "m_2", "r^2", r"\alpha"),
                                  voos={1: mp(e3, ie3, [6]), 2: mp(e3, ie3, [7]), 4: mp(S1, is1, [7]), 5: mp(S1, is1, [8]), 6: mp(S1, is1, [9]),
                                        8: mp(S2, is2, [7]), 9: mp(S2, is2, [8]), 10: mp(S2, is2, [9])}, rt=1.4)
        C1c, ic1c, c1cb = self.gm(C1b, ic1b, ("=", r"\alpha", r"(I+m_1R^2+m_2r^2)"), mapas=[([2, 6, 10], [1]), ([1, 3, 4, 5, 7, 8, 9], [2])], rt=1.3)
        self.pilha.so(c1ab, c1cb)
        al_, ial, bx = self.linha({"pre": (r"\alpha", "="), "num": (r"(m_1R-m_2r)", "g"), "den": ("I", "+", "m_1", "R^2", "+", "m_2", "r^2")},
                                  voos={0: mp(C1c, ic1c, [1]), 2: mp(C1a, ic1a, [0, 2, 3, 4, 6]), 3: mp(C1a, ic1a, [1, 5]), 5: mp(C1c, ic1c, [2])},
                                  size=50, caixa_cor=ACC, rt=1.6)
        num_ = mp(al_, ial, [2])
        den_ = mp(al_, ial, [5, 6, 7, 8, 9, 10, 11])
        self.gat("o de cima é a comparação da energia")
        sub = Line(num_.get_corner(DL) + 0.05 * DOWN, num_.get_corner(DR) + 0.05 * DOWN).set_stroke(MAS, 4)
        tn = VGroup(txt("MASSA × RAIO:", 30, bold=True, color=MAS), txt("A COMPARAÇÃO DA ENERGIA", 30, bold=True, color=MAS)).arrange(DOWN, buff=0.08, aligned_edge=LEFT)
        self.pilha.poe(tn)
        self.play(Create(sub), FadeIn(tn), self.ind_copia(num_, MAS, 1.1, 0.7), run_time=0.7)
        self.gat("o de baixo é sempre positivo")
        tdn = txt("DENOMINADOR: SEMPRE > 0", 30, bold=True, color=GEO)
        self.pilha.poe(tdn)
        self.play(FadeIn(tdn), self.ind_copia(den_, GEO, 1.06, 0.8), run_time=0.8)
        self.gat("o sinal do numerador já prevê o sentido")
        self.play(self.ind_copia(num_, MAS, 1.12, 0.9), run_time=0.9)
        self.ate(0.99)
        self.formula = (al_, ial, bx)

        # ── E3-6: números um por vez; setas a₁ e a₂ (3 : 1) ──
        self.an("E3-6")
        self.selo("CONFERE", [[lbl(r"a_1/a_2=R/r=3", ACC, 40)]])
        self.pilha.so(bx, anims=[FadeOut(sub), FadeOut(tn), FadeOut(tdn)])
        self.play(FadeIn(rot), run_time=0.4)
        self.gat("com os números")
        N1, in1, _ = self.gm(al_, ial, {"pre": (r"\alpha", "="), "num": (r"(1{,}8-1{,}0)", r"\cdot 9{,}8"), "den": (r"0{,}50", "+", r"0{,}54", "+", r"0{,}10")},
                             mapas=[([2], [2]), ([3], [3]), ([5], [5]), ([7, 8], [7]), ([10, 11], [9])], rt=1.4)
        N1b, in1b, n1b = self.gm(N1, in1, (r"\alpha", "=", r"6{,}88\ \mathrm{rad/s^2}"), cores={2: ACC}, caixa_cor=ACC, rt=1.0)
        self.gat("o bloco leve desce com")
        self.pilha.so(n1b, g4, g5)
        N2, in2, _ = self.gm(e4, ie4, ("a_1", "=", r"6{,}88", r"\cdot", r"0{,}30", "=", r"2{,}06\ \mathrm{m/s^2}", r"\downarrow"), sai=[2, 3],
                             voos={2: mp(N1b, in1b, [2])}, cores={6: ACC, 7: ACC}, rt=1.2)
        ka = 0.62
        sa1 = seta_s(pb1(-0.11) + 0.08 * LEFT, pb1(-0.11) + 0.08 * LEFT + 2.063 * ka * DOWN, ACC, 6)
        self.play(FadeIn(sa1), run_time=0.4)
        self.gat("o pesado sobe com")
        N3, in3, _ = self.gm(e5, ie5, ("a_2", "=", r"6{,}88", r"\cdot", r"0{,}10", "=", r"0{,}688\ \mathrm{m/s^2}", r"\uparrow"), sai=[2, 3],
                             voos={2: mp(N1b, in1b, [2])}, cores={6: ACC, 7: ACC}, rt=1.2)
        sa2 = seta_s(pb2(0.16), pb2(0.16) + 0.688 * ka * UP, ACC, 6)
        self.play(FadeIn(sa2), run_time=0.4)
        self.gat("a razão entre as acelerações é três")
        N4, in4, _ = self.linha({"pre": (), "num": ("a_1",), "den": ("a_2",), "post": ("=", r"\tfrac{R}{r}", "=", "3")}, size=48, rt=1.0, caixa_cor=ACC)
        self.ate(0.99)

        # ── E3-7: trações (das linhas LEVE e PESADO por glyph map) e as duas verificações ──
        self.an("E3-7")
        self.sem_selo()
        self.pilha.limpa(anims=[FadeOut(sa1), FadeOut(sa2)])
        self.gat("agora as trações leve")
        self.selo("CONFERE", [[lbl("T_1", FC, 38), lbl("<", FC, 38), lbl(r"m_1g=58{,}8\ \mathrm{N}", FC, 38)], [lbl("T_2", FC, 38), lbl(">", FC, 38), lbl(r"m_2g=98\ \mathrm{N}", FC, 38)]])
        self.pilha.poe(g1)
        self.play(FadeIn(g1), run_time=0.3)
        T1_, it1, _ = self.gm(e1, ie1, ("T_1", "=", "m_1", "(g-a_1)", "=", r"46{,}4\ \mathrm{N}"), mapas=[([1, 2, 6], [3])], cores={5: FC}, rt=1.3)
        self.gat("pesado dez vezes")
        self.pilha.poe(g2)
        self.play(FadeIn(g2), run_time=0.3)
        T2_, it2, _ = self.gm(e2, ie2, ("T_2", "=", "m_2", "(g+a_2)", "=", r"104{,}9\ \mathrm{N}"), mapas=[([1, 3, 6], [3])], cores={5: FC}, rt=1.3)
        self.gat("o torque resultante das trações no carretel")
        self.pilha.so(T1_, T2_)
        V1t = txt("CARRETEL SOZINHO", 30, bold=True, color=FC)
        self.pilha.poe(V1t)
        self.play(FadeIn(V1t), run_time=0.3)
        Vl, ivl, vlb = self.linha(("T_1", "R", "-", "T_2", "r", "=", "I", r"\alpha"), size=46, rt=1.0, metodo="lei")        # v5 LEI PRIMEIRO: a lei literal antes dos números
        V1, iv1, v1b = self.linha(("T_1", "R", "-", "T_2", "r", "=", r"3{,}44", "=", r"0{,}50", r"\,\alpha"), voos={0: mp(T1_, it1, [5]), 3: mp(T2_, it2, [5])},
                                  cores={6: FC, 8: MAS}, size=46, rt=1.4, caixa_cor=FC)
        self.gat("aquela equação é do sistema inteiro")
        self.pilha.so(V1t, v1b)
        V2t = txt("SISTEMA INTEIRO", 30, bold=True, color=MAS)
        self.pilha.poe(V2t)
        self.play(FadeIn(V2t), run_time=0.3)
        V2, iv2, v2b = self.linha((r"(m_1R-m_2r)", "g", "=", r"7{,}84", "=", r"1{,}14", r"\,\alpha"), cores={3: FC, 5: MAS}, size=46, rt=1.4, caixa_cor=MAS)
        self.gat("inclui os blocos")
        V3, iv3, _ = self.linha((r"\alpha", "=", r"6{,}88\ \mathrm{rad/s^2}", r"\ \ \mathrm{nas\ duas}\ \checkmark"), cores={2: ACC, 3: ACC}, size=46, rt=1.0)
        self.gat("o erro clássico é dividir")
        V4, iv4, _ = self.linha(({"pre": (), "num": (r"7{,}84",), "den": (r"0{,}50",), "post": ("=", r"15{,}7", r"\ \times")}), cores={4: MAS}, size=46, rt=0.9)
        rk = risco(mp(V4, iv4, [0, 1, 2, 3, 4]))
        self.play(Create(rk), run_time=0.5)
        V4.add(rk)
        self.ate(0.99)

        # ── E3-8: energia em 1,0 m — o MESMO carretel Three.js em frontal; zoom contínuo para a queda caber ──
        self.an("E3-8")
        self.selo("CÂMERA LENTA", "×2 · O LEVE DESCE 1,0 M")
        self.pilha.limpa()
        self.play(Kc.animate.set_value(3.5), ycc.animate.set_value(1.75), FadeOut(rot), f3.op.animate.set_value(1.0), comp.animate.set_value(1.0), run_time=1.0)
        self.remove(esq)
        self.gat("quando o leve desce um metro")
        y10 = pb1(0.056)[1]
        y20 = pb2(0.08)[1]
        self.play(tc.animate.set_value(T_1M), run_time=2 * T_1M, rate_func=linear)
        xm1, xm2 = pb1()[0] + 0.55, pb2()[0] - 0.62
        rg1 = VGroup(Line(P3(xm1, y10), P3(xm1, pb1(0.056)[1])).set_stroke(GEO, 3.5), lbl(r"1{,}0\ \mathrm{m}", GEO, 40).next_to(P3(xm1 + 0.1, (y10 + pb1(0.056)[1]) / 2), RIGHT, buff=0.12))
        rg2 = VGroup(Line(P3(xm2, y20), P3(xm2, pb2(0.08)[1])).set_stroke(GEO, 3.5), lbl(r"\frac{1}{3}\ \mathrm{m}", GEO, 40).next_to(P3(xm2 - 0.1, (y20 + pb2(0.08)[1]) / 2), LEFT, buff=0.12))
        self.play(FadeIn(rg1), FadeIn(rg2), run_time=0.5)
        self.gat("a energia potencial perdida")
        El, iel, _ = self.linha((r"\Delta U", "=", "m_1", "g", "h_1", "-", "m_2", "g", "h_2"), size=46, rt=1.0, metodo="lei")        # v5 LEI PRIMEIRO
        self.pilha.so(El)
        E0, ie0, _ = self.linha((r"\Delta U", "=", "m_1", "g", r"\cdot", r"1{,}0", "-", "m_2", "g", r"\cdot", r"\tfrac{1}{3}"), voos={5: rg1[1], 10: rg2[1]}, size=46, rt=1.3)
        E1, ie1, _ = self.gm(E0, ie0, (r"\Delta U", "=", r"58{,}8", "-", r"32{,}7", "=", r"26{,}1\ \mathrm{J}"), mapas=[([2, 3, 4, 5], [2]), ([7, 8, 9, 10], [4])], cores={6: KC}, rt=1.3)
        yb = -1.3
        b1 = VGroup(lbl(r"\Delta U", KC, 40).move_to(P3(0.95, yb)), barra_h(1.6, yb, 4.6, 1.0, KC))
        fr1, fr2 = M1 * 2.031 ** 2 / 2 / 26.13, M2 * 0.677 ** 2 / 2 / 26.13
        b2 = VGroup(lbl("K", KC, 40).move_to(P3(0.95, yb - 0.6)))
        x = 1.6
        for fr, cor, nome, dy in ((fr1, KC, "K_1", -1.05), (fr2, mix(KC, 0.4), "K_2", -1.05), (1 - fr1 - fr2, escuro(KC, 0.3), r"K_{c}", -1.05)):
            b2.add(Rectangle(width=4.6 * fr, height=0.26).move_to(P3(x + 4.6 * fr / 2, yb - 0.6)).set_fill(cor, 1.0).set_stroke(BACKGROUND_COLOR, 1.2),
                   lbl(nome, cor if cor != escuro(KC, 0.3) else KC, 40).move_to(P3(x + 4.6 * fr / 2, yb + dy)))
            x += 4.6 * fr
        self.gat("que viram energia cinética dos dois blocos")
        self.play(FadeIn(b1), FadeIn(b2), run_time=0.7)
        self.gat("o leve chega a dois vírgula zero três")
        self.pilha.so(E1)
        self.pilha.base = -2.6
        E2, ie2, _ = self.linha(("v_1", "=", r"2{,}03\ \mathrm{m/s}"), cores={2: VEL}, size=46, rt=1.0)
        self.gat("pela cinemática")
        E3_, ie3, _ = self.linha(("v_1", "=", r"\sqrt{2\,a_1\cdot 1{,}0}", "=", r"2{,}03\ \mathrm{m/s}", r"\ \checkmark"), cores={4: VEL, 5: ACC}, size=46, rt=1.2, caixa_cor=VEL)
        self.ate(0.99)
        self.pilha.base = -3.25

        # ── E3-9: volta ao repouso, travado; α = 0 ⟺ m₁R − m₂r = 0 → m₂ = m₁R/r = 18 kg; solta e fica parado ──
        self.an("E3-9")
        self.sem_selo()
        self.pilha.limpa(anims=[FadeOut(VGroup(rg1, rg2, b1, b2))])
        self.play(tc.animate.set_value(0.0), trava.animate.set_value(1.0), Kc.animate.set_value(K0), ycc.animate.set_value(Y0), run_time=1.4)
        self.play(FadeIn(rot), run_time=0.3)
        self.gat("o numerador precisa zerar")
        self.pilha.poe(bx)
        self.play(FadeIn(bx), run_time=0.4)
        Q0, iq0, _ = self.linha((r"\alpha=0", r"\iff", r"m_1R", "-", "m_2", "r", "=", "0"), voos={2: mp(al_, ial, [2])}, rt=1.1)
        Q1, iq1, _ = self.gm(Q0, iq0, ("m_2", "r", "=", r"m_1R"), sai=[0, 1, 7], mapas=[([3], [])], rt=1.2)
        Q2, iq2, _ = self.gm(Q1, iq1, {"pre": ("m_2", "="), "num": (r"m_1R",), "den": ("r",)}, rt=1.1)
        self.gat("dezoito quilos")
        Q3, iq3, q3b = self.gm(Q2, iq2, {"pre": ("m_2", "="), "num": (r"6\cdot 0{,}30",), "den": (r"0{,}10",), "post": ("=", r"18\ \mathrm{kg}")}, sai=[2, 4], cores={6: MAS}, caixa_cor=MAS, rt=1.2)
        self.play(m2.animate.set_value(18.0), run_time=1.0)
        self.gat("a aceleração angular zera")
        self.selo("DO REPOUSO",[[lbl(r"\alpha=0", ACC, 38), "· FICA PARADO"]])
        self.play(trava.animate.set_value(0.0), run_time=0.6)
        sp = txt("SEM TRAVA: CONTINUA PARADO", 30, bold=True, color=GEO)
        self.pilha.poe(sp)
        self.play(FadeIn(sp), run_time=0.5)
        self.gat("continuaria com velocidade constante")
        self.pilha.so(q3b, sp)
        Q4, iq4, _ = self.linha((r"\alpha", "=", "0", r"\ \Rightarrow\ ", r"\omega", "=", r"\mathrm{constante}"), size=46, rt=1.1)
        self.gat("e a pergunta do começo está respondida")
        perg = VGroup(txt("COMO O MAIS LEVE VENCE?", 30, bold=True), txt("BRAÇO 3× MAIOR", 32, bold=True, color=GEO)).arrange(DOWN, buff=0.24)
        self.pilha.poe(perg)
        self.play(FadeIn(perg, shift=0.08 * UP), run_time=0.6)
        self.ate(0.99)

        # ── E3-10: DICA ──
        self.an("E3-10")
        self.selo("DICA", "MASSA × RAIO PREVÊ O SENTIDO")
        self.pilha.limpa()
        self.gat("compara massa vezes raio")
        X1, _, _ = self.linha(("m_1", "R", r"\ \gtrless\ ", "m_2", "r"), size=52, rt=1.0, caixa_cor=MAS)
        self.gat("e confere pela razão das acelerações")
        X2, _, _ = self.linha((r"\frac{a_1}{a_2}", "=", r"\frac{R}{r}", r"\quad", r"\Delta U", "=", r"\sum K"), size=46, rt=1.1)
        self.ate(0.99)

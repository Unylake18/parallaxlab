"""Lote PE3 (v2): E3 — A PLACA COM RECORTE. ESQUEMA fixo à esquerda: placa circular R = 0,30 m (6,5 u/m) com recorte de raio R/2 centrado a R/2 de O (tangente à
borda externa e passando por O); eixo horizontal em O, perpendicular à placa; o recorte (rosa) é TIRADO do disco inteiro no E3-1; CM (ponto branco) a R/6 de O, do
lado oposto. Começa com O–CM na horizontal e gira 90° até o CM ficar embaixo de O (barras U → K). Álgebra construída a partir dos rótulos (M₀, M, R, R/2, M₀/4,
R/6, g): I como soma com sinal (massa negativa), eixos paralelos para o recorte (frações com denominador comum), x_cm por média ponderada, energia."""
from pecas21 import *  # noqa: F401,F403

O3 = P3(-3.9, -0.1)
K3 = 6.5
RP = 0.30 * K3                                       # raio da placa na tela
XE3, YE3, HE3 = -0.45, -2.9, 2.4


def placa_recorte(fi, o=O3, op=1.0):
    """Placa com o recorte; fi = ângulo da direção O → centro do recorte. Devolve (placa, contorno do recorte, centro do recorte)."""
    cr = o + (RP / 2) * np.array([math.cos(fi), math.sin(fi), 0])
    pl = Difference(Circle(radius=RP).move_to(o), Circle(radius=RP / 2).move_to(cr))
    aco(pl, 2.0, op)
    pl.set_z_index(5)
    tr = DashedVMobject(Circle(radius=RP / 2).move_to(cr).set_stroke(MAS, 3, opacity=op), num_dashes=36, dashed_ratio=0.55).set_z_index(7)
    return pl, tr, cr


class LoteE3(Lote21):
    FUNDO = "fundo_lab_ex.png"

    def corpo(self):
        self.an("E3-1")
        self.secao("EXERCÍCIO 3 · A PLACA COM RECORTE")
        self.guia(['ENUNCIADO:', 'PLACA CIRCULAR COM', 'RECORTE. QUAL O I', 'PELO CENTRO O?'])                                      # v6 G4: a coluna da direita não fica vazia
        fi = ValueTracker(0.0)                      # recorte à direita de O → CM à esquerda (O–CM horizontal)
        cmo = ValueTracker(0.0)                     # CM visível
        bars = ValueTracker(0.0)
        tira = ValueTracker(0.0)                    # 0: o pedaço está no lugar · 1: o pedaço saiu e sumiu
        self.add(fi, cmo, bars, tira)
        I_O, Mr = NUM["E3_IO"], 1.5
        dcm = 0.05

        def esquema():
            f = fi.get_value()
            pl, tr, cr = placa_recorte(f)
            g = VGroup(pl, tr)
            tt = tira.get_value()
            if tt < 0.999:                           # o recorte (disco menor) sai do lugar e some: a placa que sobrou é a do problema
                d_ = np.array([math.cos(f), math.sin(f), 0])
                pc = cr + d_ * (2.6 * tt)
                pe = Circle(radius=RP / 2).move_to(pc)
                aco(pe, 2.0)
                pe.set_fill(MAS, 0.5).set_stroke(MAS, 3, opacity=1)
                g.add(escala_op(pe.set_z_index(6), 1 - max(0.0, tt - 0.6) / 0.4))
            c = O3 - (RP / 6) * np.array([math.cos(f), math.sin(f), 0])
            if cmo.get_value() > 0.01:
                g.add(escala_op(cm_pt(c, 0.09), cmo.get_value()))
            g.add(eixo_cruz(O3, 0.16))
            b = bars.get_value()
            if b > 0.01:
                desc = dcm * (math.sin(f))                # o CM desce dcm·sen(fi) (fi: 0 → 90°)
                U = Mr * G * (dcm - desc)
                K = Mr * G * desc
                tot = Mr * G * dcm
                g.add(barra_E(XE3 - 0.3, YE3, HE3 * U / tot, 0.34, KC, hmax=HE3), barra_E(XE3 + 0.3, YE3, HE3 * K / tot, 0.34, mix(KC, 0.38), hmax=HE3))
                if not PEDIDOS3D:
                    w = math.sqrt(max(0.0, 2 * K / I_O))
                    self.reg("e3", fi=f, U=U, K=K, soma=U + K, tot=tot, w=w, alturas=[float(HE3 * U / tot), float(HE3 * K / tot)])
            if not PEDIDOS3D:
                self.reg("e3_geo", O=O3, cr=cr, r_rec=RP / 2, RP=RP, cm=c, fi=f)
            return g
        ev = vivo(esquema)
        self.play(FadeIn(ev), run_time=0.7)
        lO = T("O", 42).move_to(O3 + P3(-0.5, -0.45))
        lR = VGroup(T("R=", 38), nm(r"0{,}30\ \mathrm{m}", GEO, 38)).arrange(RIGHT, buff=0.08).move_to(P3(O3[0] - 0.9, O3[1] + RP + 0.4))
        cotR = Line(O3, O3 + RP * np.array([math.cos(2.3), math.sin(2.3), 0])).set_stroke(GEO, 2.6).set_z_index(9)
        lM = VGroup(T("M=", 38), nm(r"1{,}5\ \mathrm{kg}", MAS, 38)).arrange(RIGHT, buff=0.08).move_to(P3(O3[0] - 1.2, O3[1] - RP - 0.42))
        lM0 = VGroup(T("M_0=", 36), nm(r"2{,}0\ \mathrm{kg}", MAS, 36)).arrange(RIGHT, buff=0.08).move_to(P3(O3[0] + 1.35, O3[1] - RP - 0.42))
        lrec = VGroup(txt("RECORTE", 24, color=MAS), VGroup(T(r"\tfrac{M_0}{4}=", 36), nm(r"0{,}50\ \mathrm{kg}", MAS, 36)).arrange(RIGHT, buff=0.08)).arrange(DOWN, buff=0.08).move_to(P3(-0.95, 1.9))      # v6 S14
        cr0 = O3 + (RP / 2) * RIGHT
        lRh = T(r"\tfrac{R}{2}", 40).move_to(cr0 + P3(0.0, 0.0))
        self.gat("uma placa circular de trinta centímetros")
        self.play(Create(cotR), FadeIn(lR), FadeIn(lO), run_time=0.7)
        self.gat("um recorte circular com metade do raio")
        self.play(tira.animate(rate_func=smooth).set_value(1.0), run_time=2.4)
        self.play(FadeIn(lRh), run_time=0.4)
        self.gat("a placa que sobrou tem um quilo e meio")
        self.play(FadeIn(lM), run_time=0.5)
        self.gat("o disco inteiro teria dois quilos")
        self.play(FadeIn(lM0), run_time=0.5)
        self.gat("o eixo é horizontal")
        self.play(Flash(O3, color=GEO, line_length=0.2, flash_radius=0.3), run_time=0.6)
        self.play(fi.animate(rate_func=there_and_back).set_value(0.5), run_time=1.6)      # v6 G6/§5: a placa balança em torno de O (prévia do movimento)
        self.pede("VELOCIDADE ANGULAR QUANDO O CM PASSA ABAIXO DE O")
        self.gat("eixo ideal sem atrito")
        self.hip("SAI DO REPOUSO · EIXO SEM ATRITO")
        self.play(fi.animate(rate_func=there_and_back).set_value(-0.45), run_time=1.4)
        self.ate(0.99)
        # ── E3-2 ──
        self.an("E3-2")
        self.sem_selo()
        A, ia = M(r"I_O", "=", r"I_{disco}", "-", r"I_{rec}", size=50)
        self.pilha.poe(A)
        self.gat("momento de inércia do disco inteiro")
        self.monta(A, ia, {}, rt=0.8)                                  # v9: a linha se escreve da esquerda para a direita (antes: FadeIn)
        B, ib = M(r"I_{disco}", "=", r"\tfrac{1}{2}", "M_0", "R^2", size=48)
        B2, ib2 = M("=", r"0{,}090\ \mathrm{kg\cdot m^2}", size=48, cores={1: MAS})
        self.pilha.poe(B)
        self.gat("o disco inteiro em torno de o")
        self.monta(B, ib, {3: lM0[0][0][:2], 4: lR[0][0][:1]}, rt=1.0)
        self.pilha.poe(B2)
        self.monta(B2, ib2, {}, rt=0.6)                                  # v9: a linha se escreve da esquerda para a direita (antes: FadeIn)
        self.gat("o pedaço retirado tem um quarto da área")
        C0, ic0 = M(r"M_{rec}", "=", r"\tfrac{M_0}{4}", size=48)
        self.pilha.poe(C0)
        self.play(FadeIn(lrec), run_time=0.6)
        self.monta(C0, ic0, {2: lM0[0][0][:2]}, rt=0.9)
        C1, ic1 = M("=", r"0{,}50\ \mathrm{kg}", size=48, cores={1: MAS})
        self.pilha.poe(C1)
        self.monta(C1, ic1, {}, rt=0.5)                                  # v9: a linha se escreve da esquerda para a direita (antes: FadeIn)
        self.foco = C1
        self.ate(0.99)
        # ── E3-3 ──
        self.an("E3-3")
        self.pilha.so(A)
        D1, id1 = M(r"I_{rec}", "=", r"\tfrac{1}{2}", r"\tfrac{M_0}{4}", r"\big(\tfrac{R}{2}\big)^2", size=46)
        D1b, id1b = M("+", r"\tfrac{M_0}{4}", r"\big(\tfrac{R}{2}\big)^2", size=46)
        self.pilha.poe(D1)
        self.pilha.poe(D1b, dx=0.7)
        self.gat("eixos paralelos meio m")
        self.monta(D1, id1, {3: lrec[1][0][:4], 4: lRh}, rt=1.0)
        self.gat("mais m vezes r sobre dois ao quadrado")
        self.monta(D1b, id1b, {1: lrec[1][0][:4], 2: lRh}, rt=1.0)
        D2, id2 = M("=", r"\Big(\tfrac{1}{32}", "+", r"\tfrac{2}{32}\Big)", "M_0", "R^2", size=46)
        self.pilha.poe(D2)
        self.gat("dá três trinta e dois avos")
        self.passo(D1, D2, (J(id1, 1), J(id2, 4)), (J(id1, 3), J(id2, 4)), rt=1.4, origem=False)
        D3, id3 = M("=", r"\tfrac{3}{32}", "M_0", "R^2", "=", r"0{,}0169\ \mathrm{kg\cdot m^2}", size=46, cores={5: MAS})
        self.pilha.poe(D3)
        self.passo(D2, D3, (J(id2, 4), J(id3, 2)), (J(id2, 5), J(id3, 3)), rt=1.2, origem=False)
        E1, ie1 = M(r"I_O", "=", r"\tfrac{1}{2}", "M_0", "R^2", "-", r"\tfrac{3}{32}", "M_0", "R^2", size=46)
        self.pilha.so()
        self.pilha.poe(E1)
        self.gat("tira do disco inteiro")
        self.voa([(mp(B, ib, [2, 3, 4]), mp(E1, ie1, [2, 3, 4])), (mp(D3, id3, [1, 2, 3]), mp(E1, ie1, [6, 7, 8]))], extra=[FadeIn(mp(E1, ie1, [0, 1, 5]))], rt=1.4, origem=False)
        E2, ie2 = M(r"I_O", "=", r"\tfrac{13}{32}", "M_0", "R^2", "=", r"0{,}0731\ \mathrm{kg\cdot m^2}", size=44, cores={6: MAS})      # v6: o número dentro da caixa (a linha "= 0,0731" ficava órfã sob ela)
        E2b = caixa_l(E2, MAS)
        self.pilha.poe(E2b)
        self.cx(E2b[0])
        self.passo(E1, E2, (J(ie1, 0), J(ie2, 0)), (J(ie1, 1), J(ie2, 1)), (J(ie1, 3), J(ie2, 3)), (J(ie1, 4), J(ie2, 4)), rt=1.4, origem=False)
        E3, ie3 = M(r"I_O", "=", r"\tfrac{13}{24}", "M", "R^2", size=46)      # v7: linha com mãe própria (a "= 13/24 MR²" ficava órfã sob a caixa)
        self.pilha.poe(E3)
        self.gat("em termos da massa que sobrou")
        self.passo(E2, E3, (J(ie2, 0), J(ie3, 0)), (J(ie2, 1), J(ie3, 1)), (J(ie2, 3), J(ie3, 3)), (J(ie2, 4), J(ie3, 4)), rt=1.2, origem=False)
        self.dica18(["SUBTRAIA I SÓ DEPOIS DE LEVAR TUDO PARA O MESMO EIXO"])
        self.reg("e3_3", I_disco=NUM["E3_Id"], I_rec=NUM["E3_Ir"], I_O=NUM["E3_IO"])
        self.foco = E2b
        self.ate(0.99)
        # ── E3-4: o CM ──
        self.an("E3-4")
        self.pilha.so(E2b)
        lcm = txt("CM", 24).move_to(O3 + P3(-RP / 6, -0.55))
        lR6 = T(r"\tfrac{R}{6}", 40).move_to(O3 + P3(-RP / 12, 0.45))
        F_, if_ = eqf([r"x_{cm}", "="], [r"M_0\cdot 0", "-", r"\tfrac{M_0}{4}", r"\cdot", r"\tfrac{R}{2}"], [r"\tfrac{3M_0}{4}"], size=44)
        self.pilha.poe(F_)
        self.selo("MASSA NEGATIVA", ["PARA O RECORTE"])
        self.gat("a média ponderada dá")
        self.voa([(lM0[0][0][:2], gl(F_, if_["num"][0])), (lrec[1][0][:4], gl(F_, if_["num"][2])), (lRh, gl(F_, if_["num"][4]))],
                 extra=[FadeIn(gl(F_, if_["pre"][0] + if_["pre"][1])), FadeIn(gl(F_, if_["num"][1] + if_["num"][3])), FadeIn(gl(F_, if_["bar"])), FadeIn(gl(F_, if_["den"][0]))],
                 rt=1.2, origem=False, cada=0.5)
        F2, if2 = M("=", r"-\tfrac{R}{6}", "=", r"-5\ \mathrm{cm}", size=48, cores={3: GEO})
        self.pilha.poe(F2)
        self.gat("do lado oposto ao recorte")
        self.play(cmo.animate.set_value(1.0), FadeIn(lcm), FadeIn(lR6), run_time=0.7)
        self.voa([(lR6, mp(F2, if2, [1])[1:])], extra=[FadeIn(mp(F2, if2, [0, 2, 3])), FadeIn(mp(F2, if2, [1])[:1])], rt=1.0, origem=False)
        self.foco = F2
        self.ate(0.99)
        # ── E3-5: a queda (energia) ──
        self.an("E3-5")
        self.sem_selo()
        self.play(FadeOut(lcm), FadeOut(lrec), FadeOut(cotR), FadeOut(lR), FadeOut(lRh), run_time=0.3)
        lb = VGroup(T("U", 36).move_to(P3(XE3 - 0.3, YE3 - 0.3)), T("K", 36).move_to(P3(XE3 + 0.3, YE3 - 0.3)))
        lg = VGroup(T("g=", 36), nm(r"9{,}8\ \mathrm{m/s^2}", ACC, 36)).arrange(RIGHT, buff=0.08).move_to(P3(-1.6, 2.1))
        self.play(bars.animate.set_value(1.0), FadeIn(lb), FadeIn(lg), run_time=0.5)
        G1, ig1 = M("M", "g", r"\tfrac{R}{6}", "=", r"\tfrac{1}{2}", "I_O", r"\omega^2", size=48, cores={1: ACC})
        self.pilha.so(E2b)
        self.pilha.poe(G1)
        self.gat("o centro de massa desce r sobre seis")
        self.voa([(lM[0][0][:1], mp(G1, ig1, [0])), (lg[0][0][:1], mp(G1, ig1, [1])), (lR6, mp(G1, ig1, [2]))], extra=[FadeIn(mp(G1, ig1, [3, 4, 5, 6]))], rt=1.2, origem=False,
                 cada=0.5)
        self.play(fi.animate(rate_func=smooth).set_value(PI / 2), run_time=2.4)
        self.play(FadeOut(lR6), run_time=0.2)
        G1b, ig1b = M("=", r"\tfrac{1}{2}", r"\tfrac{13}{24}", "M", "R^2", r"\omega^2", size=48)
        self.pilha.poe(G1b)
        self.passo(G1, G1b, (J(ig1, 4), J(ig1b, 1)), (J(ig1, 6), J(ig1b, 5)), rt=1.2, origem=False)
        rm = VGroup(risco(VGroup(G1[0][ig1[0][0]]), cor=HEAT, w=4), risco(VGroup(G1b[0][gidx(G1b, ig1b[3], "M")]), cor=HEAT, w=4))
        self.gat("cancela a massa")
        self.play(Create(rm), run_time=0.6)
        G2, ig2 = M(r"\omega^2", "=", r"\tfrac{8g}{13R}", size=48, cores={2: VEL})
        self.pilha.poe(G2)
        self.passo(G1b, G2, (J(ig1b, 5), J(ig2, 0)), rt=1.2, extra=[FadeOut(rm)], origem=False)
        self.remove(rm)
        G3, ig3 = eqf([r"\omega^2", "="], ["8", r"\cdot", "9{,}8"], ["13", r"\cdot", "0{,}30"], post=["=", r"20{,}1"], size=46)
        self.pilha.poe(G3)
        self.gat("com r de trinta centímetros")
        self.voa([(lg[1][0][:3], gl(G3, ig3["num"][2])), (lR[1][0][:4], gl(G3, ig3["den"][2]))],
                 extra=[FadeIn(gl(G3, ig3["pre"][0] + ig3["pre"][1])), FadeIn(gl(G3, ig3["num"][0] + ig3["num"][1])), FadeIn(gl(G3, ig3["bar"])), FadeIn(gl(G3, ig3["den"][0] + ig3["den"][1])),
                        FadeIn(gl(G3, ig3["post"][0] + ig3["post"][1]))], rt=1.2, origem=False)
        G4, ig4 = M(r"\omega", "=", r"\sqrt{20{,}1}", "=", r"4{,}48\ \mathrm{rad/s}", size=50, cores={4: VEL})
        G4b = caixa_l(G4, VEL)
        self.pilha.poe(G4b)
        self.cx(G4b[0])
        self.passo(G3, G4, (ig3["pre"][0][:1], J(ig4, 0)), (ig3["post"][1], ig4[2][1:]), rt=1.3, origem=False)
        self.reg("e3_5", w=NUM["E3_w"], fi_final=PI / 2)
        self.foco = G3
        self.ate(0.99)
        # ── E3-6 ──
        self.an("E3-6")
        self.pilha.so(G4b)
        c_fin = O3 - (RP / 6) * np.array([math.cos(PI / 2), math.sin(PI / 2), 0])
        svc = seta(c_fin, c_fin + 0.224 * 3.0 * RIGHT, VEL, 5, tip=0.16, z=14)
        p_long = O3 - RP * np.array([math.cos(PI / 2), math.sin(PI / 2), 0])
        svm = seta(p_long, p_long + 1.345 * 1.2 * RIGHT, VEL, 6, tip=0.2, z=14)
        lR6b = T(r"\tfrac{R}{6}", 40).move_to(c_fin + P3(-1.5, -0.5))
        lRb = T("R", 42).move_to(p_long + P3(1.61 + 0.45, 0.0))
        H1, ih1 = M(r"v_{cm}", "=", r"\omega", r"\tfrac{R}{6}", "=", r"0{,}22\ \mathrm{m/s}", size=46, cores={5: VEL})
        H2, ih2 = M(r"v_{m\acute{a}x}", "=", r"\omega", "R", "=", r"1{,}34\ \mathrm{m/s}", size=46, cores={5: VEL})
        self.pilha.poe(H1)
        self.pilha.poe(H2)
        self.gat("o centro de massa passa a vinte e dois")
        self.play(FadeIn(svc), FadeIn(lR6b), run_time=0.5)
        self.monta(H1, ih1, {2: mp(G4, ig4, [0]), 3: lR6b}, rt=0.8)
        self.gat("e os pontos mais afastados")
        self.play(FadeIn(svm), FadeIn(lRb), run_time=0.5)
        self.monta(H2, ih2, {2: mp(G4, ig4, [0]), 3: lRb}, rt=0.8)
        self.play(FadeOut(lRb), FadeOut(lR6b), run_time=0.3)
        H3a, ih3a = M(r"I_{cm}", "=", r"\tfrac{13}{24}", "M", "R^2", "-", "M", r"\big(\tfrac{R}{6}\big)^2", size=44)
        H3, ih3 = M("=", r"\tfrac{37}{72}", "M", "R^2", "=", r"0{,}0694\ \mathrm{kg\cdot m^2}", size=44, cores={5: MAS})
        H4, ih4 = M(r"I_{cm}", "<", "I_O", size=46)
        self.pilha.poe(H3a)
        self.pilha.poe(H3)
        self.pilha.poe(H4)
        self.gat("o momento de inércia em torno do próprio centro de massa")
        self.monta(H3a, ih3a, {3: lM[0][0][:1], 6: lM[0][0][:1], 7: lR6b}, rt=1.2)
        self.passo(H3a, H3, (J(ih3a, 3), J(ih3, 2)), (J(ih3a, 4), J(ih3, 3)), rt=1.2, origem=False)
        self.monta(H4, ih4, {}, rt=0.5)                                  # v9: a linha se escreve da esquerda para a direita (antes: FadeIn)
        self.selo("CONFERE", [[T(r"I_O=I_{cm}+M\big(\tfrac{R}{6}\big)^2", 38)]])
        self.reg("e3_6", v_cm=NUM["E3_w"] * 0.05, v_max=NUM["E3_w"] * 0.30, I_cm=NUM["E3_Icm"], soma=NUM["E3_Icm"] + 1.5 * 0.05 ** 2, I_O=NUM["E3_IO"])
        self.foco = H3
        self.ate(0.99)
        # ── E3-7: eixo no CM, depois pêndulo ──
        self.an("E3-7")
        self.play(FadeOut(svc), FadeOut(svm), FadeOut(lR6b), FadeOut(lRb), run_time=0.3)
        self.sem_selo()
        ev.clear_updaters()
        self.pilha.limpa(rt=0.3)
        gir = ValueTracker(0.0)
        eixo = ValueTracker(1.0)                     # 1: eixo no CM · 0: eixo em O (pêndulo)
        self.add(gir, eixo)
        c0 = O3 - (RP / 6) * np.array([math.cos(PI / 2), math.sin(PI / 2), 0])

        def no_cm():
            a = gir.get_value()
            e = eixo.get_value()
            pc = c0 if e > 0.5 else O3
            pl, tr, _ = placa_recorte(PI / 2)
            g = VGroup(pl, tr).rotate(a, about_point=pc)
            cmp_ = pc + (c0 - pc) if e > 0.5 else O3 + (c0 - O3)
            cmp_ = O3 + np.array([math.cos(-PI / 2 + a), math.sin(-PI / 2 + a), 0]) * (RP / 6) if e < 0.5 else c0
            g.add(cm_pt(cmp_, 0.09), eixo_cruz(pc, 0.16))
            return g
        cv = vivo(no_cm)
        self.troca([ev, lb, lO, lM, lM0, lg], FadeIn(cv), seq=True)
        self.dica18(["SE O EIXO PASSASSE PELO CM, NADA SE MOVERIA"])
        self.gat("a placa ficaria parada")
        for a_ in (0.0, 1.1, 2.2):
            self.play(gir.animate.set_value(a_), run_time=0.8)
            self.wait(0.5)
        self.gat("o recorte é o que a transforma")
        self.play(eixo.animate.set_value(0.0), gir.animate.set_value(0.0), run_time=0.6)
        T0 = self.clk.get_value()
        self.gat("massa negativa para o centro de massa")
        self.play(gir.animate(rate_func=lambda x: 0.55 * math.sin(2 * PI * x * 1.5)).set_value(1.0), run_time=max(3.0, self.resta() - 0.6))
        self.foco = cv
        self.ate(0.99)

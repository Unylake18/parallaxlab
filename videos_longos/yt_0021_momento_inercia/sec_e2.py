"""Lote PE2 (v2): E2 — A HASTE QUE TOMBA. ESQUEMA fixo à esquerda: haste uniforme L = 1,0 m (3,7 u) articulada num pino no chão, quase vertical; CM em L/2
(ponto branco); a queda é animada pelo ângulo; setas violeta ⊥ à haste valem ωr (ω da energia: ω² = 3g(1 − sen θ)/L); barras U e K ao lado (U + K constante).
Álgebra construída: cada símbolo/número voa do rótulo (M, L, L/2, g) ou do gráfico; M e g cancelam por glyph map. E2-3: ω = √(3g/L) = 5,42 rad/s,
v_ponta = ωL = 5,42 m/s × pedra √(2gL) = 4,43 m/s; E2-4: gráfico ωr × √(2gr) (cruzam em 2L/3); E2-6: bola na ponta."""
import kit as _kit
from pecas21 import *  # noqa: F401,F403

PIV = P3(-6.3, -1.2)
KL = 3.4                                             # u/m
Y_CHAO = PIV[1] - 0.12
SV = 0.3                                             # u por m/s nas setas de velocidade
XU, XK, YU0, HU = -1.0, -0.45, -3.0, 2.0             # barras U e K


def tabela_queda(k, th0=math.radians(86), dt=2e-4):
    """Queda real da haste (θ medido do chão): θ'' = −k cos θ (k = 3g/2L; com a bola na ponta k = 9g/8L), a partir do repouso. Devolve (t, θ)."""
    t_, th_, w_ = [0.0], [th0], 0.0
    th, t = th0, 0.0
    while th > 0.0 and t < 5.0:
        w_ -= k * math.cos(th) * dt
        th += w_ * dt
        t += dt
        t_.append(t)
        th_.append(max(th, 0.0))
    return np.array(t_), np.array(th_)


T_HASTE, TH_HASTE = tabela_queda(1.5 * 9.8 / 1.0)
T_BOLA, TH_BOLA = tabela_queda(9 * 9.8 / (8 * 1.0))


def rate_queda(tt, thh):
    """rate_func para th.animate(...).set_value(0): reproduz a queda REAL, em câmera lenta (o tempo desenhado é esticado por T_desenho/T_real)."""
    th0 = thh[0]
    return lambda u: float((th0 - np.interp(u * tt[-1], tt, thh)) / th0)


class LoteE2(Lote21):
    FUNDO = "fundo_lab_ex.png"

    def corpo(self):
        self.an("E2-1")
        self.secao("EXERCÍCIO 2 · A HASTE QUE TOMBA")
        self.guia(['ENUNCIADO:', 'HASTE DE 1 m NO PINO,', 'SOLTA DA VERTICAL.', 'VELOCIDADE DA PONTA', 'NA HORIZONTAL?'])                                      # v6 G4: a coluna da direita não fica vazia
        th = ValueTracker(math.radians(86))         # ângulo da haste com o chão
        setas = ValueTracker(0.0)
        bola = ValueTracker(0.0)
        barras = ValueTracker(0.0)
        dy = ValueTracker(0.0)                       # a haste sobe 2 u no E2-4 para o gráfico ocupar o pé do ESQUEMA
        self.add(th, setas, bola, barras, dy)

        def w_de(t_):                               # ω pela energia (haste sozinha ou com a bola na ponta), saindo de 90°
            h = max(0.0, 1 - math.sin(t_))
            return math.sqrt(3 * G * h / 1.0) if bola.get_value() < 0.5 else math.sqrt(9 * G * h / (4 * 1.0))

        def haste():
            PIVc = PIV + dy.get_value() * UP
            t_ = th.get_value()
            u = np.array([math.cos(t_), math.sin(t_), 0])
            n = np.array([-math.sin(t_), math.cos(t_), 0])
            pt = PIVc + KL * u
            g = VGroup()
            corpo = Polygon(PIVc + 0.1 * n, pt + 0.1 * n, pt - 0.1 * n, PIVc - 0.1 * n)
            aco(corpo, 1.8)
            g.add(corpo.set_z_index(6))
            g.add(cm_pt(PIVc + 0.5 * KL * u, 0.09))
            g.add(Dot(pt, radius=0.08, color=WHITE_).set_z_index(9))
            if bola.get_value() > 0.01:
                g.add(escala_op(esfera_aco(0.13).move_to(pt), bola.get_value()), Circle(radius=0.15).move_to(pt).set_stroke(MAS, 3, opacity=bola.get_value()).set_z_index(9))
            s_ = setas.get_value()
            if s_ > 0.01:
                w = w_de(t_)
                for f in (0.25, 0.5, 0.75, 1.0):
                    p = PIVc + f * KL * u
                    v = w * f * 1.0
                    if v * SV > 0.12:
                        g.add(seta(p, p - n * v * SV * s_, VEL, 5, tip=0.18, z=12))
            g.add(eixo_cruz(PIVc, 0.16))
            h_ = max(0.0, 1 - math.sin(t_))
            bb = barras.get_value()
            tot = (1.5 if bola.get_value() > 0.5 else 0.5)
            if bb > 0.01:
                U = tot * (1 - h_) * 1.0
                K = tot * h_
                g.add(barra_E(XU, YU0, HU * U / tot, 0.34, KC, hmax=HU), barra_E(XK, YU0, HU * K / tot, 0.34, mix(KC, 0.38), hmax=HU))
            if not PEDIDOS3D:
                self.reg("e2", th=t_, w=w_de(t_), U=G * 0.5 * math.sin(t_), K=0.5 * (1 / 3) * w_de(t_) ** 2 if bola.get_value() < 0.5 else None,
                         pos_ponta=[float(pt[0]), float(pt[1])], pos_cm=[float(PIVc[0] + 0.5 * KL * u[0]), float(PIVc[1] + 0.5 * KL * u[1])])
            return g
        hv = vivo(haste)
        chao_ = chao(-7.3, -0.4, Y_CHAO)
        self.play(FadeIn(chao_), FadeIn(hv), run_time=0.7)
        self.play(th.animate(rate_func=there_and_back).set_value(math.radians(89)), run_time=1.4)       # v6 parado 17:03: a haste balança no pino antes de a fala começar
        u0 = np.array([math.cos(th.get_value()), math.sin(th.get_value()), 0])
        lL = VGroup(T("L=", 38), nm(r"1{,}0\ \mathrm{m}", GEO, 38)).arrange(RIGHT, buff=0.08).next_to(PIV + 0.8 * KL * u0, RIGHT, buff=0.4)
        lcm = T(r"\tfrac{L}{2}", 40).next_to(PIV + 0.5 * KL * u0, LEFT, buff=0.35)
        lMh = T("M", 42).next_to(PIV + 0.3 * KL * u0, RIGHT, buff=0.35)
        lpo = txt("PONTA", 24).next_to(PIV + KL * u0, RIGHT, buff=0.3)
        lpi = txt("PINO", 26).next_to(PIV, DL, buff=0.35)
        lg = VGroup(T("g=", 38), nm(r"9{,}8\ \mathrm{m/s^2}", ACC, 38)).arrange(RIGHT, buff=0.08).move_to(P3(-5.6, -3.4))
        self.gat("uma haste uniforme de um metro")
        self.play(FadeIn(lL), FadeIn(lMh), run_time=0.6)
        self.gat("presa na base por um pino")
        self.play(FadeIn(lpi), FadeIn(lpo), run_time=0.5)
        self.gat("com uma inclinação tão pequena")
        self.hip("SAI DO REPOUSO · PINO SEM ATRITO · INCLINAÇÃO INICIAL DESPREZÍVEL")
        self.gat("qual é a velocidade da ponta")
        self.pede("VELOCIDADE DA PONTA AO CHEGAR NA HORIZONTAL")
        lbarE0 = VGroup(T("U", 36).move_to(P3(XU, YU0 - 0.3)), T("K", 36).move_to(P3(XK, YU0 - 0.3)))
        self.gat("mais rápida ou mais devagar")                         # v9: a preparação do E2-2 corre na última frase da pergunta (a voz é contínua)
        self.play(FadeOut(lpo), FadeOut(lpi), FadeIn(lcm), FadeIn(lg), FadeIn(lbarE0), barras.animate.set_value(1.0), run_time=0.5)
        self.play(th.animate(rate_func=there_and_back).set_value(math.radians(89)), run_time=1.8)       # v6 parado 17:28: balança no pino enquanto as barras U/K se explicam
        self.ate(0.99)
        # ── E2-2 ──
        self.an("E2-2")
        self.sem_selo()
        A, ia = M("M", "g", r"\tfrac{L}{2}", "=", r"\tfrac{1}{2}", "I", r"\omega^2", size=50, cores={1: ACC})
        lA = linha_m(txt("ENERGIA:", 26, bold=True), A, buff=0.2)
        self.pilha.poe(lA)
        self.gat("a energia potencial que a haste perde")
        self.play(FadeIn(lA[0]), run_time=0.3)
        self.monta(A, ia, {0: lMh, 1: lg[0][0][:1], 2: lcm})
        self.gat("ela vira energia de rotação")
        self.play(self.ind(A, ia, [5, 6], VEL, 1.12, 0.8), run_time=0.8)
        B, ib = M("I", "=", r"\tfrac{ML^2}{3}", size=50)
        self.pilha.poe(B)
        self.gat("o da barra pela ponta")
        self.monta(B, ib, {2: VGroup(lMh, lL[0][0][:1])}, rt=1.0)
        self.dica18(["ENERGIA POTENCIAL É A DO CM; CINÉTICA, A DO GIRO EM TORNO DO PINO"])
        self.gat("que a gente calculou no começo")                      # v9: a substituição de I corre ainda no E2-2 (a fala do E2-3 já abre em "cancela a massa")
        self.pilha.so(A, B)
        C_, ic = M("M", "g", r"\tfrac{L}{2}", "=", r"\tfrac{1}{2}", r"\tfrac{ML^2}{3}", r"\omega^2", size=48, cores={1: ACC})
        self.pilha.poe(C_)
        self.passo(A, C_, (J(ia, 0), J(ic, 0)), (J(ia, 1), J(ic, 1)), (J(ia, 2), J(ic, 2)), (J(ia, 3), J(ic, 3)), (J(ia, 4), J(ic, 4)), (J(ia, 6), J(ic, 6)), rt=0.8, origem=False)
        self.voa([(mp(B, ib, [2]), mp(C_, ic, [5]))], rt=0.6, origem=False)
        self.sem_selo(rt=0.1)                                           # v10 B2: a DICA sai ainda no fim do E2-2 (o E2-3 abre em "cancela a massa", sem pausa na voz)
        self.foco = B
        self.ate(0.99)
        # ── E2-3 ──
        self.an("E2-3")
        jM = gidx(C_, ic[5], "M")
        jL = gidx(C_, ic[2], "L")
        rs = VGroup(risco(VGroup(C_[0][ic[0][0]]), cor=HEAT, w=4), risco(VGroup(C_[0][jM]), cor=HEAT, w=4), risco(VGroup(C_[0][jL]), cor=HEAT, w=4))
        self.gat("cancela a massa")
        self.play(Create(rs), run_time=0.7)
        D_, id_ = M(r"\omega^2", "=", r"\tfrac{3g}{L}", size=50, cores={2: VEL})
        self.pilha.poe(D_)
        self.passo(C_, D_, (J(ic, 6), J(id_, 0)), (J(ic, 3), J(id_, 1)), rt=1.4, extra=[FadeOut(rs)], origem=False)
        self.remove(rs)
        D2, id2 = eqf([r"\omega^2", "="], ["3", r"\cdot", "9{,}8"], ["1{,}0"], post=["=", r"29{,}4"], size=48)
        self.pilha.poe(D2)
        self.gat("cinco vírgula quarenta e dois radianos por segundo")
        self.voa([(lg[1][0][:3], gl(D2, id2["num"][2])), (lL[1][0][:3], gl(D2, id2["den"][0]))],
                 extra=[FadeIn(gl(D2, id2["pre"][0] + id2["pre"][1])), FadeIn(gl(D2, id2["num"][0] + id2["num"][1])), FadeIn(gl(D2, id2["bar"])),
                        FadeIn(gl(D2, id2["post"][0] + id2["post"][1]))], rt=1.0, origem=False)
        D3, id3 = M(r"\omega", "=", r"5{,}42\ \mathrm{rad/s}", size=50, cores={2: VEL})
        self.pilha.so(D2)
        self.pilha.poe(D3)
        self.monta(D3, id3, {}, rt=0.7)                                  # v9: a linha se escreve da esquerda para a direita (antes: FadeIn)
        E_, ie = M(r"v_{ponta}", "=", r"\omega", "L", "=", r"5{,}42\ \mathrm{m/s}", size=50, cores={5: VEL})
        Eb = caixa_l(E_, VEL)
        self.pilha.poe(Eb)
        self.gat("a ponta anda ômega vezes l")
        self.cx(Eb[0])
        lL2 = T("L", 44).next_to(PIV + 0.37 * KL * RIGHT, UP, buff=0.3)
        self.play(FadeIn(lL2), run_time=0.3)
        self.voa([(mp(D3, id3, [0]), mp(E_, ie, [2])), (lL2, mp(E_, ie, [3]))], extra=[FadeIn(mp(E_, ie, [0, 1, 4, 5]))], rt=1.0, origem=False)
        self.play(FadeOut(lcm), FadeOut(lMh), FadeOut(lL), run_time=0.2)
        RS_, XS_ = (1 / 3, 2 / 3, 1.0), (-2.3, -1.9, -1.5)                # pedras soltas das alturas L/3, 2L/3 e L (ao lado da ponta)
        pu = ValueTracker(0.0)
        self.add(pu)
        pedras = vivo(lambda: VGroup(*[pedra().scale_to_fit_height(0.3).move_to(P3(x, PIV[1] + 0.16 + r * KL * (1 - pu.get_value() ** 2))).set_z_index(8) for x, r in zip(XS_, RS_)]))
        self.play(FadeIn(pedras), run_time=0.4)
        self.play(th.animate(rate_func=rate_queda(T_HASTE, TH_HASTE)).set_value(0.0), setas.animate.set_value(1.0), pu.animate(rate_func=lambda x: x ** 1.6).set_value(1.0), run_time=2.4, fixo=True)
        sarr = VGroup(*[seta(P3(x, PIV[1] + 0.2), P3(x, PIV[1] + 0.2 - math.sqrt(2 * G * r) * SV), mix(VEL, 0.45), 5, tip=0.18) for x, r in zip(XS_, RS_)])
        lped = txt("PEDRAS", 24).move_to(P3(-2.9, PIV[1] - 1.75))      # v6 S13
        self.play(FadeIn(sarr), FadeIn(lped), run_time=0.6)
        F_, if_ = M(r"v_{pedra}", "=", r"\sqrt{2gL}", "=", r"4{,}43\ \mathrm{m/s}", size=48, cores={4: VEL})
        self.pilha.poe(F_)
        self.gat("uma pedra solta de um metro")
        self.monta(F_, if_, {1: VGroup(lg[0][0][:1], lL2)}, rt=1.2)
        self.reg("e2_3", w=NUM["E2_w"], v_ponta=NUM["E2_w"] * 1.0, v_pedra=NUM["E1_queda"])
        self.gat("a ponta da haste chega mais rápido")
        self.play(self.ind_copia(Eb, WHITE_, 1.06, 0.8), run_time=0.8)
        self.foco = Eb
        self.ate(0.99)
        # ── E2-4: o gráfico ωr × √(2gr) ──
        self.an("E2-4")
        self.play(FadeOut(pedras), FadeOut(sarr), FadeOut(lped), FadeOut(lL2), FadeOut(chao_), FadeOut(lg), FadeOut(lbarE0), barras.animate.set_value(0.0), run_time=0.4)
        pedras.clear_updaters()
        self.remove(pedras)
        self.play(dy.animate.set_value(2.0), run_time=0.9)
        self.pilha.limpa(rt=0.3)
        self.guia(['PERGUNTA:', 'UMA PEDRA SOLTA DA', 'PONTA CAI MAIS RÁPIDO', 'QUE A HASTE?'])                                      # v6 G4: a coluna da direita não fica vazia
        gw, gh, x0g, y0g = 5.0, 1.6, -6.3, -3.3
        rmax, vmax = 1.0, 6.0
        P_ = lambda r, v: P3(x0g + gw * r / rmax, y0g + gh * v / vmax)
        eix = VGroup(Arrow(P_(0, 0), P_(1.08, 0), buff=0, stroke_width=3, tip_length=0.14).set_color(GEO),
                     Arrow(P_(0, 0), P_(0, 6.4), buff=0, stroke_width=3, tip_length=0.14).set_color(GEO))
        lr_ = T("r", 38).next_to(eix[0].get_end(), RIGHT, buff=0.06)
        lv_ = T("v", 38).next_to(eix[1].get_end(), LEFT, buff=0.08)
        lin = Line(P_(0, 0), P_(1.0, NUM["E2_w"])).set_stroke(VEL, 5)
        raiz = VMobject().set_points_smoothly([P_(r, math.sqrt(2 * G * r)) for r in np.linspace(0, 1.0, 60)]).set_stroke(mix(VEL, 0.55), 4)
        lw_ = T(r"\omega r", 36).next_to(P_(1.0, NUM["E2_w"]), RIGHT, buff=0.1)
        lq_ = T(r"\sqrt{2gr}", 34, mix(VEL, 0.55)).next_to(P_(1.0, math.sqrt(2 * G)), DR, buff=0.1)
        xc = 2 / 3
        cruz = Dot(P_(xc, NUM["E2_w"] * xc), radius=0.09, color=WHITE_).set_z_index(9)
        lxc = T(r"\tfrac{2L}{3}", 38).next_to(P_(xc, 0), DOWN, buff=0.14)
        tick = DashedLine(P_(xc, 0), P_(xc, NUM["E2_w"] * xc), dash_length=0.06).set_stroke(GEO, 2)
        graf = VGroup(eix, lr_, lv_, lin, raiz, lw_, lq_, cruz, lxc, tick)
        self.gat("se a gente compara cada ponto da haste")
        self.play(FadeIn(eix), FadeIn(lr_), FadeIn(lv_), Create(lin), FadeIn(lw_), run_time=0.9)
        self.play(Create(raiz), FadeIn(lq_), run_time=0.8)
        self.gat("só o ponto que está a dois terços")
        self.play(FadeIn(cruz, scale=0.5), Create(tick), FadeIn(lxc), run_time=0.7)
        p23 = PIV + 2.0 * UP + xc * KL * RIGHT
        d23 = Dot(p23, radius=0.1, color=WHITE_).set_z_index(14)
        l23 = T(r"\tfrac{2L}{3}", 38).next_to(p23, UP, buff=0.4)
        self.play(FadeIn(d23), FadeIn(l23), run_time=0.5)
        G0, ig0 = M(r"\omega", "r", "=", r"\sqrt{2gr}", size=48, cores={0: VEL})
        self.pilha.topo = 2.35
        self.pilha.poe(G0, dx=0.0)
        self.gat("é a velocidade crescendo linearmente")
        self.voa([(lw_, mp(G0, ig0, [0, 1])), (lq_, mp(G0, ig0, [3]))], extra=[FadeIn(mp(G0, ig0, [2]))], rt=1.0, origem=False)
        G1, ig1 = M("r", "=", r"\tfrac{2g}{\omega^2}", size=48)
        for j_ in ig1[2]:                                              # v5 D8: o ω² do denominador com a cor cheia da grandeza (VEL), nunca apagado
            r_ = _kit._id_glifo(G1[0][j_])
            if r_ is not None and r_[0] == "\\omega":
                G1[0][j_].set_color(VEL).set_stroke(VEL, 1.6, background=False)
        self.pilha.poe(G1)
        self.gat("com a distância ao pino")
        self.passo(G0, G1, (J(ig0, 1), J(ig1, 0)), (J(ig0, 2), J(ig1, 1)), rt=1.2, origem=False)
        G2, ig2 = M("r", "=", r"\tfrac{2g\,L}{3g}", "=", r"\tfrac{2L}{3}", size=48)
        self.pilha.poe(G2)
        self.passo(G1, G2, (J(ig1, 0), J(ig2, 0)), (J(ig1, 1), J(ig2, 1)), rt=1.2, origem=False)
        gs = [k for k in ig2[2] if _kit._id_glifo(G2[0][k]) == ("g", 0)]
        rg = VGroup(*[risco(VGroup(G2[0][j]), cor=HEAT, w=4) for j in gs])
        self.play(Create(rg), FadeIn(mp(G2, ig2, [3, 4])), run_time=0.9)
        self.reg("e2_4", r_igual=(2 * G / NUM["E2_w"] ** 2), dois_tercos=2 / 3)
        self.foco = G2
        self.ate(0.99)
        # ── E2-5 ──
        self.an("E2-5")
        self.pilha.so(G2)
        self.selo("CUIDADO", ["VELOCIDADE FINAL, NÃO TEMPO DE QUEDA"])
        nt = VGroup(txt("O PINO NÃO REALIZA TRABALHO:", 24), txt("O PONTO FIXO NÃO SE DESLOCA", 24)).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        self.pilha.poe(nt)
        self.gat("o pino exerce forças")
        self.play(Flash(PIV + 2.0 * UP, color=WHITE_, line_length=0.2, flash_radius=0.3), run_time=0.7)        # v9: o pino está 2,0 u acima (a haste subiu para o gráfico)
        self.gat("essa força não realiza trabalho")
        self.play(FadeIn(nt), run_time=0.7)
        self.gat("a conservação da energia basta")
        self.play(self.ind_copia(G2, WHITE_, 1.05, 0.8), run_time=0.8)
        self.foco = nt
        self.ate(0.99)
        # ── E2-6: uma bola na ponta ──
        self.an("E2-6")
        self.sem_selo()
        self.play(FadeOut(rg), FadeOut(d23), FadeOut(l23), FadeOut(graf), setas.animate.set_value(0.0), run_time=0.4)
        self.remove(graf)
        self.pilha.limpa(rt=0.3)
        self.play(th.animate.set_value(math.radians(86)), dy.animate.set_value(0.0), FadeIn(chao_), FadeIn(lg), FadeIn(lbarE0), barras.animate.set_value(1.0), run_time=0.9)
        self.gat("bolinha tão pequena")
        self.selo("MASSA PONTUAL NA PONTA", "")
        self.play(bola.animate.set_value(1.0), run_time=0.6)
        self.play(th.animate(rate_func=there_and_back).set_value(math.radians(68)), run_time=2.4)       # v9: a haste balança no pino com a bolinha (a tela não fica parada)
        u1 = np.array([math.cos(th.get_value()), math.sin(th.get_value()), 0])
        lMb = T("M", 42).next_to(PIV + KL * u1, RIGHT, buff=0.45)
        lMh2 = T("M", 42).next_to(PIV + 0.3 * KL * u1, RIGHT, buff=0.35)
        lL3 = T("L", 42).next_to(PIV + 0.75 * KL * u1, RIGHT, buff=0.35)
        lcm2 = T(r"\tfrac{L}{2}", 40).next_to(PIV + 0.5 * KL * u1, LEFT, buff=0.35)
        self.play(FadeIn(lMb), FadeIn(lMh2), FadeIn(lL3), FadeIn(lcm2), run_time=0.5)
        H1, ih1 = M("I", "=", r"\tfrac{ML^2}{3}", "+", "M", "L^2", size=48)
        self.pilha.poe(H1)
        self.gat("o momento de inércia passa de um terço")
        self.monta(H1, ih1, {2: VGroup(lMh2, lL3), 4: lMb, 5: lL3}, rt=1.0)
        H1b, ih1b = M("=", r"\tfrac{4}{3}", "M", "L^2", size=48)
        self.pilha.poe(H1b)
        self.passo(H1, H1b, (J(ih1, 4), J(ih1b, 2)), (J(ih1, 5), J(ih1b, 3)), rt=1.0, origem=False)
        H2, ih2 = M("U", "=", "M", "g", r"\tfrac{L}{2}", "+", "M", "g", "L", size=48, cores={3: ACC, 7: ACC})
        self.pilha.poe(H2)
        self.gat("a energia disponível sobe")
        self.monta(H2, ih2, {2: lMh2, 4: lcm2, 6: lMb, 8: lL3}, rt=1.0)
        H2b, ih2b = M("=", r"\tfrac{3}{2}", "M", "g", "L", size=48, cores={3: ACC})
        self.pilha.poe(H2b)
        self.passo(H2, H2b, (J(ih2, 2), J(ih2b, 2)), (J(ih2, 3), J(ih2b, 3)), (J(ih2, 8), J(ih2b, 4)), rt=1.0, origem=False)
        self.play(FadeOut(lMb), FadeOut(lMh2), FadeOut(lL3), FadeOut(lcm2), run_time=0.3)
        H3a, ih3a = M(r"\omega^2", "=", r"\tfrac{9g}{4L}", size=48)
        self.pilha.poe(H3a)
        self.gat("resultado a ponta chega")
        self.passo(H2b, H3a, (J(ih2b, 3), [ih3a[2][1]]), (J(ih2b, 4), [ih3a[2][4]]), rt=1.2, origem=False)
        H3, ih3 = M(r"v_{ponta}", "=", r"\tfrac{3}{2}\sqrt{gL}", "=", r"4{,}70\ \mathrm{m/s}", size=48, cores={4: VEL})
        H3b = caixa_l(H3, VEL)
        self.pilha.poe(H3b)
        self.gat("quatro vírgula setenta")
        self.cx(H3b[0])
        self.monta(H3, ih3, {}, rt=0.8)                                  # v9: idem
        self.play(th.animate(rate_func=rate_queda(T_BOLA, TH_BOLA)).set_value(0.0), setas.animate.set_value(1.0), run_time=2.2, fixo=True)
        self.reg("e2_6", v=NUM["E2_bola"])
        self.selo("MAIS MASSA NA PONTA", ["PONTA MAIS LENTA"])
        self.foco = H3b
        self.ate(0.99)

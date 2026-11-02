"""Lote PX3 (v4): X3 o gafanhoto na folha, no lago em Three.js (lago3d.js) de lado; réguas, cotas, setas, θ, ⊕ e rótulos no Manim (projeta3d).
v4 §4: câmera de lado mas 13° acima da água (a lâmina vira uma faixa, não uma linha); dois enquadramentos com dolly explícito: PERTO (folha a
~62% do ESQUEMA, gafanhoto ×2) nos dados, forças, componentes, réguas e contas (X3-1, X3-2, X3-3, conta do X3-5b, X3-6, X3-8, X3-9) e LONGE
(÷3, selo ESCALA ÷3) só quando o voo inteiro precisa caber (X3-4 o voo, X3-5, voos do X3-5b, salto quase vertical do X3-7, voo do X3-9 e o
fecho X3-10, mantido como no v3); volta para PERTO assim que o voo termina. O salto de demonstração (X3-4 a X3-5b) é a 84°: cai na água 12 cm
além da folha, e o pouso cabe no PERTO para a conta de Δx. v3 §6: nos saltos altos o ápice fica ≥ 0,5 abaixo do topo do ESQUEMA. Gafanhoto desenhado ×2 em torno dos pés (física intacta; selo
GAFANHOTO AMPLIADO ×2 na primeira vez). Uma régua com números por vez: a da água (GEO, embaixo, marcas a cada 10 cm, números −10…30 e 40–70 só
quando o gafanhoto passa) e a da folha (marcas na borda de cima da folha, números só 0 e 30); VISTO DA ÁGUA → números na da água, VISTO DA
FOLHA → números na da folha. Deslocamentos (Δx, 24 cm, 6 cm) em setas GEO acima da régua da água, rótulo na ponta de fora. t_voo (violeta) no
lugar do T. Ângulo de demonstração: 45° no diagrama do salto (setas ≥ 0,6, G8) e 78° nos voos (o θ gira de 45° a 78° no recuo do X3-4).
G23: m, M, v cos θ, V, 2 v sen θ, g, Δx, 0,30 saem dos rótulos do desenho; substituições e passos por glyph map na Pilha (P1–P3)."""
from lago2 import *  # noqa: F401,F403

SEN = r"\operatorname{sen}"
TH_R = math.degrees(math.asin(0.30 * 9.8 / (1.25 * 16))) / 2
TH_V = 90 - TH_R
TH_U = 90 - math.degrees(math.asin(0.30 * 9.8 / 16)) / 2
SV = 0.6                                                                  # Manim por m/s (diagrama do salto)
PERTO = dict(K=15.5, az=-90.0, el=13.0, ax=0.15, az_=0.0, xc=-3.6, yc=-1.75, fov=10.0)
LONGE = dict(K=15.5 / 3, az=-90.0, el=13.0, ax=0.35, az_=0.0, xc=-3.55, yc=-2.45, fov=10.0)    # ápice ≥ 0,3 abaixo do selo VISTO DA…
TH_D = 84.0                                                               # salto de demonstração (X3-4 a X3-5b): o pouso cabe no PERTO
DYR = 0.85                                                                # régua da água: abaixo da linha d'água (tela)


def igual_e_depois(m):
    """Glifos depois do primeiro "=" de uma linha montada por M() (a parte direita), para o voa."""
    t = m if isinstance(m, MathTex) else next(x for x in m.get_family() if isinstance(x, MathTex))
    k = 0
    for tx_, _ in t._partes:
        if tx_.strip() == "=":
            return VGroup(*t[0][k + 1:])
        k += ng(tx_)
    return VGroup(*t[0])


class LoteX3(Prob2):
    def construct(self):
        self.setup_base(cap="PROBLEMA 4 · O GAFANHOTO")
        self.x3()
        self.fim()
        self.relatorio()
        self.gravar_reg()

    def vista(self, v, rt=None):
        lg = self.lg
        alvo = dict(K=lg.K, az=lg.az, el=lg.el, ax=lg.ax, az_=lg.az_, xc=lg.xc, yc=lg.yc, fov=lg.fov)
        if rt is None:
            for k, val in v.items():
                alvo[k].set_value(val)
            return []
        return [alvo[k].animate(rate_func=smooth).set_value(val) for k, val in v.items()]

    def selo_esq(self, texto, rt=0.4, extra=()):
        """Selo pequeno no canto de cima à direita do ESQUEMA (ESCALA ÷3, GAFANHOTO AMPLIADO ×2): sai antes de outro entrar."""
        velho = getattr(self, "s_esq", None)
        if velho is not None:
            self.play(FadeOut(velho), run_time=0.25)
            self.remove(velho)
            self.s_esq = None
        if not texto:
            if extra:
                self.play(*extra, run_time=rt)
            return None
        t = txt(texto, 24, bold=True)
        bx = RoundedRectangle(corner_radius=0.08, width=t.width + 0.26, height=t.height + 0.16).move_to(t).set_fill(PANEL, 0.9).set_stroke(GEO, 1.6)
        bx._fundo = True
        s = VGroup(bx, t).set_z_index(36)
        s._selo = "esq"
        s.move_to(P3(0.1 - s.width / 2, 2.5 - s.height / 2))
        self.play(FadeIn(s), *extra, run_time=rt)
        self.s_esq = s
        return s

    def rot_gaf(self, lab):
        """G27 / v4 §2 #13: rótulo logo acima do gafanhoto (≤ 0,4 do desenho), terminando à esquerda da seta de v (que sai de pé + 0,25)."""
        fo, ga = self._lago_polis(self.lg.f3d)
        xd = self.lg.pe()[0] + 0.1
        lab.next_to(P3(xd, ga[:, 1].max()), UP, buff=0.22)
        return lab.shift((xd - lab.get_right()[0]) * RIGHT)

    def rot_folha(self, lab, dx=0.0):
        """v4 §2 #13: rótulo logo abaixo do meio da folha."""
        fo, ga = self._lago_polis(self.lg.f3d)
        return lab.next_to(P3(fo[:, 0].mean() + dx, fo[:, 1].min()), DOWN, buff=0.24)

    def remador(self):
        casco = aco(Polygon(P3(-0.9, 0.12), P3(-0.75, -0.05), P3(-0.3, -0.12), P3(0.35, -0.12), P3(0.78, -0.05), P3(0.9, 0.12)), 1.4)
        pe = silhueta(PessoaPerfil(0.0, 0.0, 0.62, -1, "pe")).move_to(P3(0.35, 0.43))
        ag = Line(P3(-1.15, -0.02), P3(1.15, -0.02)).set_stroke(mix(BLUE_L, 0.35), 2)
        g = VGroup(ag, casco, pe, marcador_cm(P3(0.0, 0.62), r=0.1))
        return VGroup(g, txt("O REMADOR", 24, op=0.85).next_to(g, DOWN, buff=0.12))

    def x3(self):
        lg = self.lg = Lago3D(self, theta=45.0, esc=2.0, op=1.0, **{k: v for k, v in PERTO.items() if k not in ("ax", "az_")}, alvo=(PERTO["ax"], 0, PERTO["az_"]))
        self.add(*lg.trackers(), lg.f3d)
        lg.f3d._quadro()
        self._futuros.append(lg.futuro)
        T_ = {k: ValueTracker(0.0) for k in ("rw", "rf", "nag", "nfo", "L", "v", "comp", "V", "p", "F", "traj", "cm", "g")}
        self.add(*T_.values())
        o = lambda k: T_[k].get_value()

        def camada():
            e = lg.f3d.e
            cam = e["cam"]
            P = lambda x, z, y=0.0: lg.P(x, z, y, cam=cam)
            xg, zg, xf = lg.estado_f()
            g = VGroup()
            pe = P(xg, zg)
            cf = P(xf + lg.L / 2, 0.0)
            yw = P(0, 0)[1]
            if o("rw") > 0.01:                                         # régua da água (GEO, embaixo); números só com VISTO DA ÁGUA
                y = yw - (DYR if cam["K"] > 10 else 0.7)                 # no LONGE a régua sobe um pouco (cabe no ESQUEMA)
                pts = [(xm, P(xm, 0.0)[0]) for xm in np.arange(-0.2, 0.8 + 1e-9, 0.1)]
                pts = [(xm, X) for xm, X in pts if -7.15 < X < 0.05]
                if len(pts) > 1:
                    g.add(Line(P3(pts[0][1] - 0.1, y), P3(pts[-1][1] + 0.1, y)).set_stroke(GEO, 2.2, opacity=o("rw")))
                    nag = o("rw") * o("nag")
                    for xm, X in pts:
                        g.add(Line(P3(X, y), P3(X, y - 0.14)).set_stroke(GEO, 2, opacity=o("rw")))
                        ve = xm < 0.35 or xg >= xm - 0.05                 # 40–70 só quando o gafanhoto passa lá
                        if nag > 0.01 and ve and (xm > -0.15):
                            g.add(mrot(f"{round(xm * 100)}".replace("-", "−"), 24, GEO, nag).next_to(P3(X, y - 0.14), DOWN, buff=0.06))
                    la_ = mrot("ÁGUA", 24, GEO, o("rw")).next_to(P3(pts[0][1] - 0.1, y), LEFT, buff=0.12)
                    la_.shift(0.1 * LEFT)
                    g.add(la_ if la_.get_left()[0] > -7.28 else VGroup())
            if o("rf") > 0.01:                                         # régua da folha: marcas finas na borda de cima da folha; números 0 e 30
                cor_f = mix(GEO, 0.3)
                larg_r = 2.0 if cam["K"] > 10 else 3.4                     # v4: no LONGE as marcas engrossam (a folha continua legível)
                for s in np.arange(0, lg.L + 1e-9, 0.05):
                    big = abs(s / 0.1 - round(s / 0.1)) < 1e-6
                    a_ = P(xf + s, 0.006)
                    g.add(Line(a_, a_ + (0.16 if big else 0.09) * UP).set_stroke(cor_f, larg_r, opacity=o("rf")))
                nfo = o("rf") * o("nfo")
                if nfo > 0.01:
                    for s in (0.0, 0.3):
                        g.add(mrot(f"{round(s * 100)}", 24, cor_f, nfo).move_to(P(xf + s, 0.0) + (0.40 if cam["K"] > 10 else 0.3) * DOWN))   # perto: os números descem para fora da caixa da folha (3D × TEXTO)
                    g.add(mrot("FOLHA", 24, cor_f, nfo).next_to(P(xf + lg.L, 0.0) + 0.3 * DOWN, RIGHT, buff=0.48))
            if o("L") > 0.01:                                          # cota L embaixo da folha
                a, b = P(xf, -0.065), P(xf + lg.L, -0.065)
                self.Lpos = (a, b)
                g.add(Line(a, b).set_stroke(GEO, 2.4, opacity=o("L")), Line(a + 0.1 * DOWN, a + 0.1 * UP).set_stroke(GEO, 2.2, opacity=o("L")),
                      Line(b + 0.1 * DOWN, b + 0.1 * UP).set_stroke(GEO, 2.2, opacity=o("L")))
            a_ = math.radians(lg.th.get_value())
            p0 = pe + P3(0.25, 0.8)                                       # acima do gafanhoto ampliado (θ e rótulos fora dele)
            if o("v") > 0.01:                                          # seta de v, θ e EM RELAÇÃO À ÁGUA
                tip = p0 + SV * lg.v * P3(math.cos(a_), math.sin(a_))
                g.add(self.seta_v(p0, tip, "ÁGUA", VEL, 6, tip=0.24, op=o("v"), nome="v"),
                      DashedLine(p0, p0 + P3(1.3, 0), dash_length=0.08).set_stroke(WHITE_, 1.8, opacity=0.6 * o("v")),
                      Arc(radius=0.8, start_angle=0, angle=a_, arc_center=p0).set_stroke(WHITE_, 2, opacity=0.8 * o("v")),
                      mtex(r"\theta", GEO, 40).set_opacity(o("v")).move_to(p0 + 1.22 * P3(math.cos(a_ / 2), math.sin(a_ / 2))))
            if o("comp") > 0.01:
                vx, vy = lg.v * math.cos(a_), lg.v * math.sin(a_)
                g.add(self.seta_v(p0, p0 + P3(SV * vx, 0), "ÁGUA", VEL, 6, tip=0.22, op=o("comp"), nome="vx"),
                      self.seta_v(p0, p0 + P3(0, SV * vy), "ÁGUA", VEL, 6, tip=0.22, op=o("comp"), nome="vy"),
                      tracejado(p0 + P3(SV * vx, 0), p0 + P3(SV * vx, SV * vy), VEL, 1.6, 0.6 * o("comp")))
            if o("V") > 0.01:
                vx = lg.v * math.cos(a_)
                xa = P(xf + lg.L * 0.62, 0.0)[0]
                g.add(self.seta_v(P3(xa, yw - 0.32), P3(xa - SV * vx / 4 * 2, yw - 0.32), "ÁGUA", VEL, 6, tip=0.2, op=o("V"), nome="V"))
            if o("p") > 0.01:
                yp = yw - 1.15
                g.add(seta(P3(pe[0] + 0.2, yp), P3(pe[0] + 1.45, yp), MAG, 7, tip=0.22, op=o("p")),
                      seta(P3(cf[0] + 0.6, yp - 0.45), P3(cf[0] - 0.65, yp - 0.45), MAG, 7, tip=0.22, op=o("p")))
            if o("F") > 0.01:
                g.add(seta(pe + P3(-0.4, 0.2), pe + P3(-0.4, -0.45), FC, 5, tip=0.18, op=o("F")), seta(cf + P3(0.25, -0.05), cf + P3(0.25, -0.75), FC, 6, tip=0.2, op=o("F")),
                      seta(cf + P3(0.95, 0.05), cf + P3(0.95, 1.1), FC, 6, tip=0.2, op=o("F")))
            if o("traj") > 0.01 and lg.tau.get_value() > 0:
                ss = np.linspace(0, min(lg.tau.get_value(), lg.T()), 40)
                g.add(VMobject().set_points_smoothly([P(*lg.estado_f(s)[:2]) for s in ss]).set_stroke(VEL, 2.4, opacity=o("traj")))
            if o("cm") > 0.01:
                xc_, yc_ = lg.cm()
                pc = P(xc_, yc_)
                topo_ = P(xc_, 0.9)[1]
                g.add(tracejado(P(xc_, 0.0), P3(pc[0], min(topo_, 1.55)), WHITE_, 2, 0.6 * o("cm")), marcador_cm(pc, r=0.16, op=o("cm")))   # longe do selo VISTO DA…
                self.reg("lago_cm", cm=pc, x_agua=(pc[0] - cam["xc"]), tau=lg.tau.get_value())
            if o("g") > 0.01:
                g.add(seta(P3(-0.55, 1.7), P3(-0.55, 0.95), ACC, 6, tip=0.2, op=o("g")))            # v5: g na borda direita do ESQUEMA (longe do v sen θ)
            lg.reg()
            return g
        cam_ = vivo(camada)
        self.add(cam_)
        # ══ X3-1 ══
        self.an("X3-1")
        self.chip(2, 3)
        self.pede("⊕ PARADO, DOIS REFERENCIAIS")                                         # v5 G32: o selo entra primeiro
        self.play(lg.f3d.op.animate.set_value(1.0), run_time=0.8)
        pe0, cf0, yw = lg.pe(), lg.P(lg.L / 2, 0.0), lg.P(0, 0)[1]
        lm = self.rot_gaf(VGroup(mtex("m", WHITE_, 40), rot("= 1 g", 30)).arrange(RIGHT, buff=0.1))
        lM = self.rot_folha(VGroup(mtex("M", WHITE_, 40), rot("= 4 g", 30)).arrange(RIGHT, buff=0.1))
        self.ate(0.12)
        self.gat("quatro vezes a massa")
        self.play(FadeIn(lM), FadeIn(lm), run_time=0.7)
        lL = VGroup(mtex("L", GEO, 40), rot("= 30 cm", 30, GEO)).arrange(RIGHT, buff=0.1)
        T_["L"].set_value(1.0)
        lL.next_to(lg.P(lg.L / 2, -0.065), DOWN, buff=0.16)
        self.play(FadeIn(lL), run_time=0.5)
        self.ate(0.2)
        self.selo_esq("GAFANHOTO AMPLIADO ×2")
        self.ate(0.27)
        self.selo_esq(None)
        self.gat("quatro metros por segundo")
        self.play(T_["v"].animate.set_value(1.0), run_time=0.8)
        tip = lg.pe() + P3(0.25, 0.8) + SV * 4 * P3(math.cos(math.radians(45)), math.sin(math.radians(45)))
        lv = VGroup(mrot("v = 4 m/s", 30, VEL), txt("EM RELAÇÃO À ÁGUA", 24)).arrange(DOWN, buff=0.08, aligned_edge=LEFT).next_to(tip, RIGHT, buff=0.3)
        self.gat("em relação à água")
        self.play(FadeIn(lv), run_time=0.6)
        self.foco = lv
        self.ate(0.6)
        hl = cartao("HIPÓTESES", "· ÁGUA SEM RESISTÊNCIA HORIZONTAL", "· FOLHA RÍGIDA", "· DECOLAGEM RÁPIDA", size=24, cor=GEO)
        hl[1][0].set_color(CYAN)
        self.pilha.poe(hl)
        self.play(FadeIn(hl, shift=0.1 * UP), run_time=0.6)                                 # v5: as hipóteses na CONTA como lista
        self.ate(0.97)
        # ══ X3-2: forças externas ══
        self.an("X3-2")
        self.play(T_["v"].animate.set_value(0.0), FadeOut(lv), FadeOut(lm), FadeOut(lM), T_["L"].animate.set_value(0.0), FadeOut(lL), run_time=0.5)   # sai a cota: as forças entram
        self.ate(0.08)
        pe0, cf0 = lg.pe(), lg.P(lg.L / 2, 0.0)
        fl = VGroup(mtex(r"m\vec g", FC, 38).next_to(pe0 + P3(-0.4, -0.45), DOWN, buff=0.14),        # abaixo dos pés, à esquerda da folha
                    mtex(r"M\vec g", FC, 38).next_to(cf0 + P3(0.25, -0.75), DOWN, buff=0.14),          # v5: o rótulo fica enquanto a seta existir
                    txt("EMPUXO", 26, color=WHITE_).next_to(cf0 + P3(0.95, 0.75), RIGHT, buff=0.32))
        print(f"[dbg] pe0 ({pe0[0]:.2f}; {pe0[1]:.2f}) cf0 ({cf0[0]:.2f}; {cf0[1]:.2f}) mg x {fl[0].get_left()[0]:.2f}…{fl[0].get_right()[0]:.2f} y {fl[0].get_bottom()[1]:.2f}…{fl[0].get_top()[1]:.2f}")
        self.gat("os pesos e o empuxo")
        self.play(T_["F"].animate.set_value(1.0), FadeIn(fl), run_time=0.9)
        self.foco = fl
        self.ate(0.5)
        F1, f1 = M(r"F_{ext,x}", "=", "0", size=48, cores={0: FC})
        self.pilha.poe(F1)
        self.gat("nenhuma força de fora")
        self.voa([(fl[0], mp(F1, f1, [0]))], extra=[FadeIn(mp(F1, f1, [1, 2]))], rt=1.0, arco_esq=1.3)       # v6: o m g⃗ sobe por fora da folha (3D × TEXTO)
        F2, f2 = M(r"\Rightarrow\ ", "P_x", "=", "0", size=48, cores={1: MAG})
        F2l = linha_m(F2, "DO COMEÇO AO FIM")
        self.pilha.poe(F2l)
        self.ate(0.72)
        self.passo(F1, F2, (J(f1, 1, 2), J(f2, 2, 3)), (J(f1, 0), J(f2, 1)), extra=[FadeIn(F2l[1])], rt=1.0)
        self.selo("SÓ A COMPONENTE HORIZONTAL", "SE CONSERVA", cor=CYAN, borda=CYAN)
        self.foco = F2l
        self.ate(0.97)
        # ══ X3-3: componentes; V; momentos iguais e opostos ══
        self.an("X3-3")
        self.play(T_["F"].animate.set_value(0.0), FadeOut(fl), T_["v"].animate.set_value(0.25), run_time=0.5)
        self.play(T_["comp"].animate.set_value(1.0), run_time=0.8)
        pe0, cf0 = lg.pe(), lg.P(lg.L / 2, 0.0)
        p0 = pe0 + P3(0.25, 0.8)
        vx = 4 * math.cos(math.radians(45))
        lvx = mtex(r"v\cos\theta", VEL, 38).next_to(p0 + P3(SV * vx, 0), RIGHT, buff=0.3)                  # na ponta da seta, do lado de fora
        lvy = mtex(r"v\," + SEN + r"\theta", VEL, 38).next_to(p0 + P3(0, SV * vx), UP, buff=0.36)
        self.play(FadeIn(lvx), FadeIn(lvy), run_time=0.5)
        yp = yw - 1.15
        lpg = mtex(r"m\,v\cos\theta", MAG, 38).next_to(P3(pe0[0] + 1.45, yp), RIGHT, buff=0.14)
        lpf = mtex(r"M\,V", MAG, 38).next_to(P3(cf0[0] - 0.65, yp - 0.45), LEFT, buff=0.14)
        self.gat("a folha ganha o mesmo momento para trás")                                          # v4 §8: as setas de momento (MAG) nascem na palavra
        self.play(T_["p"].animate.set_value(1.0), FadeIn(lpg), FadeIn(lpf), run_time=0.7)
        xa = lg.P(lg.L * 0.62, 0.0)[0]
        lV = mtex("V", VEL, 40).next_to(P3(xa, yw - 0.52), RIGHT, buff=0.2)
        lm2 = self.rot_gaf(VGroup(mtex("m", WHITE_, 40), rot("= 1 g", 30)).arrange(RIGHT, buff=0.1))
        lM2 = self.rot_folha(VGroup(mtex("M", WHITE_, 40), rot("= 4 g", 30)).arrange(RIGHT, buff=0.1), dx=-1.6)
        self.ate(0.3)
        self.play(T_["V"].animate.set_value(1.0), FadeIn(lV), FadeIn(lm2), FadeIn(lM2), run_time=0.7)
        A, ia = M("m", r"\,v\cos\theta", "=", "M", r"\,V", size=50, cores={1: VEL, 4: VEL})
        self.pilha.poe(A)
        self.ate(0.42)
        self.voa([(lm2[0], mp(A, ia, [0])), (lvx, mp(A, ia, [1])), (lM2[0], mp(A, ia, [3])), (lV, mp(A, ia, [4]))], extra=[FadeIn(mp(A, ia, [2]))], rt=1.2)
        B, ib = M("V", "=", r"\tfrac{m}{M}", r"\,v\cos\theta", size=50, cores={0: VEL, 3: VEL})
        self.pilha.poe(B)
        self.ate(0.6)
        self.passo(A, B, (J(ia, 4), J(ib, 0)), (J(ia, 2), J(ib, 1)), (J(ia, 0), [J(ib, 2)[0]]), (J(ia, 3), [J(ib, 2)[2]]), (J(ia, 1), J(ib, 3)), ([], [J(ib, 2)[1]]), rt=1.4)
        C_, ic = M("V", "=", r"\tfrac{v\cos\theta}{4}", size=50, cores={0: VEL, 2: VEL})
        Cb = caixa_l(C_, VEL)
        self.pilha.poe(Cb)
        self.ate(0.82)
        self.gat("um quarto da velocidade")
        self.passo(B, C_, (J(ib, 0, 1), J(ic, 0, 1)), (J(ib, 3), J(ic, 2)[:-2]), (J(ib, 2), J(ic, 2)[-2:]), extra=[FadeIn(Cb[0]), Indicate(lM2, color=WHITE_)], rt=1.2)
        self.foco = Cb
        self.ate(0.97)
        # ══ X3-4: tempo de voo; o recuo da câmera (ESCALA ÷3) e a parábola de 78° ══
        self.an("X3-4")
        self.play(T_["p"].animate.set_value(0.0), FadeOut(VGroup(lpg, lpf, lV, lvx, lm2, lM2)), T_["V"].animate.set_value(0.0), T_["g"].animate.set_value(1.0),
                  T_["v"].animate.set_value(0.0), run_time=0.5)
        lg_ = mtex("g", ACC, 40).next_to(P3(-0.55, 1.32), LEFT, buff=0.3)
        self.play(FadeIn(lg_), run_time=0.4)
        Tq, it = M(r"t_{voo}", "=", r"\frac{2\,v\," + SEN + r"\theta}{g}", size=54, cores={0: VEL})
        fr_ = mp(Tq, it, [2])                                                     # 2 v sen θ ─ g: v violeta, θ GEO, g violeta claro
        fr_[1].set_color(VEL)
        fr_[5].set_color(GEO)
        fr_[-1].set_color(ACC)
        Tb = caixa_l(Tq, VEL)
        self.pilha.poe(Tb)
        self.ate(0.12)
        self.gat("o tempo de voo")
        self.voa([(lvy, fr_[1:6]), (lg_, fr_[-1:])], extra=[FadeIn(mp(Tq, it, [0, 1])), FadeIn(fr_[0:1]), FadeIn(fr_[6:-1]), FadeIn(Tb[0])], rt=1.2, origem=False,
                 cada=0.75)                                                                       # um voo depois do outro (os caminhos se cruzam)
        self.foco = Tb
        self.ate(0.4)
        self.selo_esq("ESCALA ÷3", rt=1.6, extra=[FadeOut(lvy), T_["comp"].animate.set_value(0.0), lg.th.animate.set_value(TH_D), *self.vista(LONGE, 1)])   # dolly PERTO → LONGE: o selo acende junto
        par = DashedVMobject(VMobject().set_points_smoothly([lg.P(*lg.estado_f(s)[:2]) for s in np.linspace(0, lg.T(), 40)]), num_dashes=70, dashed_ratio=0.5) \
            .set_stroke(VEL, 2.6, opacity=0.9)
        self.play(Create(par), T_["v"].animate.set_value(0.0), run_time=1.2)
        self.foco = par
        self.ate(0.9)
        self.play(FadeOut(lg_), T_["g"].animate.set_value(0.0), run_time=0.6)
        # ══ X3-5: as réguas; VISTO DA ÁGUA → VISTO DA FOLHA (câmera recuada) ══
        self.an("X3-5")
        T = lg.T()
        self.pilha.so(Tb, anims=[T_["rw"].animate.set_value(1.0), T_["rf"].animate.set_value(1.0), T_["nag"].animate.set_value(1.0)])
        self.referencial("DA ÁGUA", anims=[FadeOut(par)], rt=0.5)                     # v5: a parábola tracejada sai com o selo (não encosta nele)
        T_["traj"].set_value(1.0)
        lg.op_fant.set_value(1.0)
        self.gat("vista da água")
        # v7: UM replay em câmera lenta, contínuo, preso ao relógio: o mesmo salto visto da água e depois da folha, até "um vírgula vinte e cinco"
        # (o gafanhoto nunca fica parado no ar)
        t0_ = (self.nq + self._off) / FPS
        A5_ = ANC["X3-5"]
        t1_ = A5_["ini"] + A5_["dur"] - 0.2                                                  # o replay anda até o fim da fala (o gafanhoto nunca pára no ar)
        lg.tau.add_updater(lambda m: m.set_value(T * 0.999 * min(1.0, max(0.0, (self.clk.get_value() + self._off / FPS - t0_) / (t1_ - t0_)))))
        self.gat("vista da folha")
        self.referencial("DA FOLHA", anims=[lg.c.animate.set_value(1.0), T_["nag"].animate.set_value(0.0), T_["nfo"].animate.set_value(1.0)], rt=1.0)
        lg.op_fant.set_value(0.0)
        V1, iv = M(r"v_{rel}", "=", r"v\cos\theta", "+", r"\tfrac{v\cos\theta}{4}", size=48, cores={0: VREL, 2: VEL, 4: VEL})
        self.pilha.poe(V1)
        self.ate(0.68)
        self.voa([(mp(C_, ic, [2]), mp(V1, iv, [4]))], extra=[FadeIn(mp(V1, iv, [0, 1, 2, 3]))], rt=1.0)
        V1b, iv1 = M("=", r"1{,}25\,v\cos\theta", size=50, cores={1: VREL})
        V1b._lhs = lambda: caixa_l(M(r"v_{rel}", "=", r"1{,}25\,v\cos\theta", size=50, cores={0: VREL, 2: VREL})[0], VREL)   # P1: herda o lado esquerdo
        self.pilha.poe(V1b)
        self.ate(0.84)
        self.gat("um vírgula vinte e cinco vezes")
        self.passo(V1, V1b, (J(iv, 1), J(iv1, 0)), (J(iv, 2, 3, 4), J(iv1, 1)), (J(iv, 0), []), rt=1.1)
        self.foco = V1b
        self.ate(0.97)
        lg.tau.clear_updaters()
        # ══ X3-5b: o ⊕ só sobe e desce na vertical ══
        self.an("X3-5b")
        self.play(lg.tau.animate.set_value(0.0), T_["traj"].animate.set_value(0.0), lg.anel.animate.set_value(0.0), run_time=0.5)
        self.referencial("DA ÁGUA", anims=[lg.c.animate.set_value(0.0), T_["nag"].animate.set_value(1.0), T_["nfo"].animate.set_value(0.0)], rt=0.6)
        self.play(T_["cm"].animate.set_value(1.0), run_time=0.6)
        self.ate(0.12)
        self.gat("ele sobe e desce")
        for k in range(2):
            self.play(lg.tau.animate(rate_func=linear).set_value(T - 0.012), run_time=(T - 0.012) / 0.5)
            self.wait(0.4)
            if k == 0:
                self.play(lg.tau.animate.set_value(0.0), run_time=0.5)
        # pousa na água e a câmera volta para o PERTO (v4 §4): a conta de Δx acontece perto, com o pouso no quadro
        self.play(lg.tau.animate(rate_func=linear).set_value(T), run_time=0.3)
        self.selo_esq(None)
        self.play(lg.tau.animate.set_value(0.0), T_["cm"].animate.set_value(0.0), T_["rw"].animate.set_value(0.0), T_["nag"].animate.set_value(0.0), T_["rf"].animate.set_value(0.0), run_time=0.5)
        lg.th.set_value(TH_R)                                                         # v5 G30: a conta de Δx é a do rasante (24 e 6 cm) e cabe no ESQUEMA
        self.play(*self.vista(PERTO, 1), run_time=0.6)
        self.play(lg.tau.animate(rate_func=linear).set_value(lg.T()), run_time=1.0)   # o rasante em câmera lenta: pousa na ponta da folha
        # rótulos m e M: viram "m = 1 g" e "M = 4 g" no lugar (sem duas camadas); setas Δx acima da régua da água, rótulo na ponta de fora
        xg, _, xf = lg.estado_f()
        yw = lg.P(0, 0)[1]
        yF, yG = yw - 1.0, yw - 1.7                                                   # v5: duas setas, cada uma na sua linha, as duas saindo da posição inicial
        X0, Xg, Xf = lg.P(0, 0)[0], lg.P(xg, 0)[0], lg.P(xf, 0)[0]
        d0 = DashedLine(P3(X0, yw - 0.2), P3(X0, yG - 0.2), dash_length=0.08).set_stroke(WHITE_, 2, opacity=0.75)
        dg = seta(P3(X0, yG), P3(Xg, yG), GEO, 6, tip=0.2)
        df = seta(P3(X0, yF), P3(Xf, yF), GEO, 6, tip=min(0.2, 0.45 * abs(X0 - Xf)))
        ldg = mtex(r"\Delta x_g", GEO, 38).next_to(P3(Xg, yG), RIGHT, buff=0.25)       # à direita da ponta
        ldf = mtex(r"\Delta x_f", GEO, 38)
        ldf.move_to(P3(X0 - 0.14 - ldf.width / 2, yF + 0.24 + ldf.height / 2))        # em cima da seta curta, encostado à esquerda do tracejado (nunca em cima dele nem da ponta)   # embaixo do meio da seta curta
        lm3 = self.rot_gaf(mtex("m", WHITE_, 40))
        lM3 = self.rot_folha(mtex("M", WHITE_, 40))
        self.play(FadeIn(VGroup(d0, dg, df, ldg, ldf, lm3, lM3)), run_time=0.5)
        lm3b = M("m", "=", r"1\ \mathrm{g}", size=40)[0].move_to(lm3)
        lM3b = M("M", "=", r"4\ \mathrm{g}", size=40)[0].move_to(lM3)
        self.gat("a massa do gafanhoto vezes o deslocamento")
        self.play(TransformMatchingShapes(lm3, lm3b), TransformMatchingShapes(lM3, lM3b), run_time=0.7)
        D1, d1 = M("m", r"\,\Delta x_g", "+", "M", r"\,\Delta x_f", "=", "0", size=48, cores={1: GEO, 4: GEO})
        D2, d2 = M(r"\Delta x_f", "=", r"-\tfrac{\Delta x_g}{4}", size=48, cores={0: GEO, 2: GEO})
        D3, d3 = M(r"\Delta x_{rel}", "=", r"\Delta x_g", "-", r"\Delta x_f", size=48, cores={0: GEO, 2: GEO, 4: GEO})
        D3b, d3b = M("=", r"1{,}25\,\Delta x_g", size=48, cores={1: GEO})
        self.pilha.poe(D1, manter=(Tb, V1b))
        self.ate(0.4)
        self.voa([(lm3b[0][0:1], mp(D1, d1, [0])), (ldg, mp(D1, d1, [1])), (lM3b[0][0:1], mp(D1, d1, [3])), (ldf, mp(D1, d1, [4]))], extra=[FadeIn(mp(D1, d1, [2, 5, 6]))], rt=1.2)
        self.pilha.poe(D2, manter=(Tb, V1b))
        self.ate(0.55)
        self.gat("um quarto do que o gafanhoto anda")
        self.passo(D1, D2, (J(d1, 4), J(d2, 0)), (J(d1, 5), J(d2, 1)), (J(d1, 1), J(d2, 2)[1:4]), (J(d1, 0, 2, 3, 6), []), rt=1.3)
        self.pilha.poe(D3, manter=(Tb, V1b))
        self.ate(0.72)
        self.passo(D2, D3, (J(d2, 0), J(d3, 4)), (J(d2, 2)[1:4], J(d3, 2)), rt=1.2)
        self.pilha.poe(D3b, manter=(Tb, V1b))
        vrel = getattr(V1b, "_herdeira", V1b)
        self.voa([(mp(D3, d3, [2]), mp(D3b, d3b, [1])[-3:]), (igual_e_depois(vrel)[:4], mp(D3b, d3b, [1])[:4])], extra=[FadeIn(mp(D3b, d3b, [0]))], rt=1.0,
                 cada=0.75)
        rm = self.remador().scale(0.85).move_to(P3(-1.5, 1.1))
        self.ate(0.84)
        self.gat("o mesmo um vírgula vinte e cinco")
        self.play(FadeIn(rm), run_time=0.8)
        self.foco = D3b
        self.ate(0.93)
        # o X3-6 começa na primeira palavra ("multiplicando"): a arrumação acontece no fim do X3-5b
        self.play(FadeOut(VGroup(d0, dg, df, ldg, ldf, lm3b, lM3b, rm)), T_["rw"].animate.set_value(0.0), T_["rf"].animate.set_value(0.0), run_time=0.4)
        lg.tau.set_value(0.0)                                                         # e só então volta à folha de uma vez (no PERTO, o voo de volta sairia do quadro)
        lg.th.set_value(45.0)
        Tb, vrel = self.pilha.so(Tb, getattr(V1b, "_herdeira", V1b), rt=0.5)
        self.referencial(None)
        # ══ X3-6: a conta → duas faixas (a câmera volta: folha a 60%) ══
        self.an("X3-6")
        E1, e1 = M(r"\Delta x_{rel}", "=", r"1{,}25\,v\cos\theta", r"\cdot", r"\tfrac{2\,v\," + SEN + r"\theta}{g}", size=48, cores={0: GEO, 2: VREL})
        self.pilha.poe(E1)
        self.gat("multiplicando essa velocidade relativa")
        self.voa([(igual_e_depois(vrel), mp(E1, e1, [2])), (mp(Tq, it, [2]), mp(E1, e1, [4]))], extra=[FadeIn(mp(E1, e1, [0, 1, 3]))], rt=1.1, origem=False)
        self.play(T_["L"].animate.set_value(1.0), FadeIn(lL), run_time=0.4)
        E2, e2 = M("=", r"1{,}25\,v^2", r"\cdot", r"\tfrac{2" + SEN + r"\theta\cos\theta}{g}", size=48)
        self.pilha.poe(E2)
        self.passo(E1, E2, (J(e1, 1), J(e2, 0)), (J(e1, 2)[:4] + J(e1, 4)[1:2], J(e2, 1)), (J(e1, 3), J(e2, 2)), (J(e1, 4)[0:1], J(e2, 3)[0:1]),
                   (J(e1, 4)[2:6], J(e2, 3)[1:5]), (J(e1, 2)[4:], J(e2, 3)[5:8]), (J(e1, 4)[6:], J(e2, 3)[8:]), rt=1.5)
        E3, e3 = M("=", r"1{,}25\,v^2", r"\tfrac{\operatorname{sen}2\theta}{g}", size=48)
        self.pilha.poe(E3)
        self.gat("o seno do dobro do ângulo")
        self.passo(E2, E3, (J(e2, 0, 1), J(e3, 0, 1)), (J(e2, 3)[:8], J(e3, 2)[:5]), (J(e2, 3)[8:], J(e3, 2)[5:]), (J(e2, 2), []), rt=1.4)  # 2 sen θ cos θ → sen 2θ
        E4, e4 = M(r"2{,}04\ \mathrm{m}", r"\cdot\operatorname{sen}2\theta", r"\le", r"0{,}30\ \mathrm{m}", size=48, cores={0: GEO, 3: GEO})
        self.pilha.poe(E4)
        self.ate(0.36)
        self.passo(E3, E4, (J(e3, 1) + J(e3, 2)[-2:], J(e4, 0)), (J(e3, 2)[:-2], J(e4, 1)), (J(e3, 0), []), rt=1.2, origem=False)   # 2,04 m = 1,25·v²/g (valor, não troca)
        self.ate(0.46)
        self.gat("trinta centímetros da folha")
        self.voa([(lL[1], mp(E4, e4, [3]))], extra=[FadeIn(mp(E4, e4, [2]))], rt=1.0)          # o 0,30 sai da cota L
        E5, e5 = M(r"\operatorname{sen}2\theta", r"\le", r"0{,}147", size=48)
        self.pilha.poe(E5)
        self.ate(0.58)
        self.passo(E4, E5, (J(e4, 1), J(e5, 0)), (J(e4, 2), J(e5, 1)), (J(e4, 0, 3), J(e5, 2)), rt=1.1, origem=False)          # 0,147 = 0,30/2,04 (razão)
        E6 = linha_m(M(r"2\theta\le 8{,}45^\circ", size=46)[0], "OU", M(r"2\theta\ge 171{,}55^\circ", size=46)[0])
        self.pilha.poe(E6)
        self.ate(0.7)
        self.gat("dá duas faixas")
        self.play(FadeIn(E6, shift=0.1 * UP), Indicate(E5, color=WHITE_, scale_factor=1.0), run_time=0.8)
        E7 = VGroup(M(r"0^\circ<\theta\le 4{,}23^\circ", size=48)[0], linha_m("OU", M(r"85{,}77^\circ\le\theta<90^\circ", size=48)[0])).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        E7b = caixa_l(E7, WHITE_)
        self.pilha.poe(E7b)
        self.ate(0.8)
        self.play(FadeIn(E7b[0]), run_time=0.3)
        self.play(FadeIn(E7[0], shift=0.08 * UP), run_time=0.45)
        self.play(FadeIn(E7[1], shift=0.08 * UP), run_time=0.45)
        self.remove(E7[0], E7[1])
        self.add(E7b)
        self.foco = E7b
        self.ate(0.97)
        # ══ X3-7: os dois saltos-limite (v4 §5: o inset nasce com o rasante desenhado; o quase vertical começa em "no quase vertical") ══
        self.an("X3-7")
        self.pilha.so(E7b, anims=[FadeOut(lL), T_["L"].animate.set_value(0.0)])
        lg.th.set_value(TH_R)
        Tr = lg.T()
        bxi = RoundedRectangle(corner_radius=0.08, width=4.4, height=1.8).move_to(P3(-4.6, 1.2)).set_fill(PANEL, 0.82).set_stroke(BLUE_L, 1.6)
        bxi._fundo = bxi._caixa = True
        tag = VGroup(txt("AMPLIADO", 24, color=CYAN, bold=True), txt("ALTURA ×20", 24)).arrange(RIGHT, buff=0.2).next_to(bxi, UP, buff=0.08).align_to(bxi, LEFT)
        yb = bxi.get_bottom()[1] + 0.2
        cam_i = lg.f3d.e["cam"]
        Xs = lambda x: lg.P(x, 0, cam=cam_i)[0]
        Kx = cam_i["K"]
        rasante = VMobject().set_points_as_corners([P3(Xs(lg.estado_f(s_)[0]), yb + 20 * Kx * lg.estado_f(s_)[1]) for s_ in np.linspace(0, Tr, 30)]) \
            .set_stroke(VEL, 2.6, opacity=0.55).set_z_index(37)                                   # o rasante inteiro já desenhado (fantasma)

        def inset():
            cam = lg.f3d.e["cam"]
            tau = lg.tau.get_value()
            xg_, yg_, xf_ = lg.estado_f(tau)
            Xs_ = lambda x: lg.P(x, 0, cam=cam)[0]
            gg = VGroup(Line(P3(Xs_(xf_), yb), P3(Xs_(xf_ + lg.L), yb)).set_stroke(GEO, 4))
            if tau > 0:
                gg.add(VMobject().set_points_as_corners([P3(Xs_(lg.estado_f(s_)[0]), yb + 20 * Kx * lg.estado_f(s_)[1]) for s_ in np.linspace(0, min(tau, lg.T()), 30)])
                       .set_stroke(VEL, 2.6))
            gg.add(Dot(P3(Xs_(xg_), yb + 20 * Kx * yg_), radius=0.07, color="#9AA6B8").set_z_index(9))
            return gg.set_z_index(37)
        ins = vivo(inset)
        L7a = VGroup(mtex(r"\theta=4{,}23^\circ", GEO, 46), linha_m("VOO", rot("0,06 s", 26, VEL), "· ALTURA", rot("4,4 mm", 26, GEO), buff=0.12, size=26)).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        self.pilha.poe(L7a)
        self.gat("no rasante")
        self.play(FadeIn(bxi), FadeIn(tag), FadeIn(rasante), FadeIn(ins), FadeIn(L7a), T_["rf"].animate.set_value(1.0), run_time=0.6)
        T_["traj"].set_value(1.0)
        self.play(lg.tau.animate(rate_func=linear).set_value(Tr), run_time=1.6)
        self.play(FadeOut(VGroup(bxi, tag, ins, rasante)), lg.tau.animate.set_value(0.0), T_["traj"].animate.set_value(0.0), run_time=0.5)
        ins.clear_updaters()
        lg.th.set_value(TH_V)
        Tv = lg.T()
        L7b = VGroup(mtex(r"\theta=85{,}77^\circ", GEO, 46), linha_m("VOO", rot("0,81 s", 26, VEL), "· ALTURA", rot("81 cm", 26, GEO), buff=0.12, size=26)).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        self.pilha.poe(L7b)
        T_["traj"].set_value(1.0)
        self.gat("no quase vertical")
        self.selo_esq("ESCALA ÷3", rt=0.9, extra=[FadeIn(L7b), *self.vista(LONGE, 1), T_["rw"].animate.set_value(1.0)])            # dolly PERTO → LONGE antes do voo alto
        self.play(lg.tau.animate(rate_func=linear).set_value(Tv), run_time=2 * Tv)
        self.play(T_["traj"].animate.set_value(0.0), run_time=0.3)                                    # pousou na ponta: o voo some e a câmera volta
        self.selo_esq(None)
        self.play(*self.vista(PERTO, 1), T_["rw"].animate.set_value(0.0), run_time=0.9)
        ar = self.desloc()
        self.ate(0.66)
        self.gat("vinte e quatro centímetros")
        self.play(FadeIn(ar), T_["nfo"].animate.set_value(1.0), run_time=0.7)
        self.ate(0.8)
        self.confere([[rot("24 + 6 = 30 cm", 26)]])
        self.foco = ar
        self.ate(0.9)
        self.play(FadeOut(VGroup(ar, L7a, L7b)), T_["traj"].animate.set_value(0.0), T_["rf"].animate.set_value(0.0), T_["nfo"].animate.set_value(0.0), run_time=0.4)   # v6: a arrumação sai no fim do X3-7
        # ══ X3-8: folha pesadíssima (a câmera volta) ══
        self.an("X3-8")
        Mf = ValueTracker(4.0)
        self.add(Mf)

        def recuos():
            M_ = Mf.get_value()
            xg_ = 0.24
            xf_ = -xg_ / M_
            cam = lg.f3d.e["cam"]
            y_ = lg.P(0, 0.0, cam=cam)[1] - 0.3
            X = lambda x: lg.P(x, 0, cam=cam)[0]
            yG_, yF_ = y_ - 0.25, y_ - 0.95
            gg = VGroup(seta(P3(X(0), yG_), P3(X(xg_), yG_), GEO, 6, tip=0.2), mrot("24 cm", 26, GEO).next_to(P3(X(xg_), yG_), RIGHT, buff=0.22))
            gg.add(DashedLine(P3(X(0), y_ + 0.1), P3(X(0), yF_ - 0.04), dash_length=0.08).set_stroke(WHITE_, 2, opacity=0.75))
            if abs(X(xf_) - X(0)) > 0.08:
                gg.add(seta(P3(X(0), yF_), P3(X(xf_), yF_), GEO, 6, tip=min(0.2, 0.45 * abs(X(xf_) - X(0)))))
            if -xf_ >= 0.005:
                v_ = -xf_ * 100
                lab = mrot((f"{v_:.0f}" if abs(v_ - round(v_)) < 0.05 else f"{v_:.1f}").replace(".", ",") + " cm", 26, GEO)
                gg.add(lab.next_to(P3((X(0) + X(xf_)) / 2, yF_), DOWN, buff=0.3))
            return gg
        rc = vivo(recuos)
        G1, g1 = M(r"1{,}25", "=", "1", "+", r"\tfrac{m}{M}", size=48)
        G1b, g1b = M(r"M\to\infty", r"\ \Rightarrow\ ", r"1{,}25\to 1", size=48)
        G2, g2 = M(r"\Delta x", "=", r"\tfrac{v^2\operatorname{sen}2\theta}{g}", size=50, cores={0: GEO})
        lg.tau.set_value(0.0)                                                         # e só então de volta à folha de uma vez (no PERTO)
        lg.th.set_value(45.0)
        self.pilha.tira(L7a, L7b)
        self.pilha.poe(G1)
        self.play(FadeIn(rc), FadeIn(G1), run_time=0.4)
        self.pilha.poe(G1b)
        self.gat("pesadíssima")
        self.play(FadeIn(G1b), Mf.animate(rate_func=lambda s: s ** 3).set_value(400.0), run_time=2.4)
        self.pilha.poe(G2)
        self.ate(0.3)
        self.gat("o alcance de qualquer lançamento")
        self.play(FadeIn(G2, shift=0.1 * UP), run_time=0.9)
        rm = self.remador().move_to(P3(-1.6, 1.1))
        self.ate(0.45)
        self.play(FadeIn(rm), run_time=0.7)
        self.foco = G2
        self.ate(0.68)
        self.dica18(["ÂNGULOS COMPLEMENTARES DÃO O MESMO ALCANCE.", "AQUI ISSO VIRA A RESPOSTA"])
        self.ate(0.97)
        # ══ X3-9: u em relação à folha ══
        self.an("X3-9")
        rc.clear_updaters()
        H1, h1 = M(r"\tfrac{u^2\operatorname{sen}2\theta}{g}", r"\le", r"0{,}30\ \mathrm{m}", size=48, cores={2: GEO})
        H1.move_to(P3(X_CONTA + H1.width / 2, TOPO_PILHA - H1.height / 2))
        self.sem_selo(rt=0.3)                                                         # o DICA anterior sai antes de a primeira linha nascer sob ele
        self.pilha.limpa(anims=[FadeOut(VGroup(rc, rm)), T_["rw"].animate.set_value(0.0), T_["nag"].animate.set_value(0.0), FadeIn(H1, rate_func=lambda u: min(1.0, max(0.0, (u - 0.7) / 0.3)))])   # v5 G32: a primeira linha já nasce na CONTA
        self.pilha.poe(H1)
        lg.rel_u = True
        lg.th.set_value(50.0)
        self.referencial("DA FOLHA", anims=[lg.c.animate.set_value(1.0), T_["rf"].animate.set_value(1.0), T_["nfo"].animate.set_value(1.0)], rt=0.8)
        du = ValueTracker(0.0)
        self.add(du)

        def seta_u():
            o_ = du.get_value()
            if o_ < 0.01:
                return VGroup()
            p0_ = lg.pe() + P3(0.0, 0.35)
            a__ = math.radians(50)
            tip_ = p0_ + 2.4 * P3(math.cos(a__), math.sin(a__))
            lab = VGroup(mrot("u = 4 m/s", 30, VREL, o_), mtxt("EM RELAÇÃO À FOLHA", 24, WHITE_, o_)).arrange(DOWN, buff=0.08, aligned_edge=LEFT)
            return VGroup(self.seta_v(p0_, tip_, "FOLHA", VREL, 6, tip=0.24, op=o_, nome="u"), lab.next_to(tip_ + P3(0.12, 0.0), RIGHT, buff=0.16))
        su = vivo(seta_u)
        self.add(su)
        self.ate(0.1)
        self.gat("em relação à folha")
        self.play(du.animate.set_value(1.0), run_time=0.7)
        H2, h2 = M(r"\operatorname{sen}2\theta", r"\le", r"0{,}184", size=48)
        H3 = linha_m(M(r"\theta\le 5{,}29^\circ", size=48)[0], "OU", M(r"\theta\ge 84{,}71^\circ", size=48)[0])
        self.ate(0.25)
        self.pilha.poe(H2)
        self.ate(0.38)
        self.play(FadeIn(H2, shift=0.1 * UP), Indicate(H1, color=WHITE_, scale_factor=1.0), run_time=0.9)    # v4 TRÂNSITO: nasce no lugar
        self.pilha.poe(H3)
        self.ate(0.52)
        self.gat("cinco vírgula três graus")
        self.voa([(H2, H3)], rt=1.0, origem=False)
        self.ate(0.6)
        lg.th.set_value(TH_U)
        T_["traj"].set_value(1.0)
        self.play(du.animate.set_value(0.0), run_time=0.4)                                             # a seta e o rótulo saem antes do dolly
        self.selo_esq("ESCALA ÷3", rt=1.0, extra=[*self.vista(LONGE, 1)])
        self.play(lg.tau.animate(rate_func=linear).set_value(lg.T()), run_time=lg.T() / 0.6)
        cart = cartao("O REFERENCIAL DO ENUNCIADO", "MUDA A RESPOSTA", size=30)
        self.pilha.poe(cart)
        self.ate(0.82)
        self.gat("velocidade em relação a quê")
        self.play(FadeIn(cart, shift=0.1 * UP), run_time=0.7)
        self.foco = cart
        self.ate(0.97)
        # ══ X3-10: fecho do gafanhoto (câmera recuada: as duas trajetórias-limite cabem) ══
        self.an("X3-10")
        su.clear_updaters()
        FIN = linha_m(M(r"\theta\le 4{,}23^\circ", size=48)[0], "OU", M(r"\theta\ge 85{,}77^\circ", size=48)[0])
        FINb = caixa_l(FIN, WHITE_)
        FINb.move_to(P3(X_CONTA + FINb.width / 2, TOPO_PILHA - FINb.height / 2))
        self.pilha.limpa(anims=[FadeOut(su), T_["rf"].animate.set_value(0.0), T_["nfo"].animate.set_value(0.0), T_["traj"].animate.set_value(0.0),
                                lg.tau.animate.set_value(0.0), lg.c.animate.set_value(0.0), FadeIn(FINb, rate_func=lambda u: min(1.0, max(0.0, (u - 0.7) / 0.3)))])                        # v5 G32: a resposta já nasce na CONTA
        self.pilha.poe(FINb)
        self.referencial(None)
        lg.rel_u = False
        p0 = lg.pe()

        def curva(th):
            a__ = math.radians(th)
            vx_, vy_ = 4 * math.cos(a__), 4 * math.sin(a__)
            T__ = 2 * vy_ / 9.8
            return VMobject().set_points_smoothly([lg.P(1.25 * vx_ * s, vy_ * s - 4.9 * s * s, cam=lg.f3d.e["cam"]) for s in np.linspace(0, T__, 40)]).set_stroke(VEL, 2.6)
        cr, cv_ = curva(TH_R), curva(TH_V)
        self.play(Create(cv_), run_time=1.2)
        self.play(Create(cr), run_time=0.5)
        R0, R1 = 1.4, 1.75
        trf = VGroup(Arc(radius=R1, start_angle=0, angle=PI / 2, arc_center=p0).set_stroke(GEO, 2), Line(p0, p0 + P3(R1 + 0.15, 0)).set_stroke(GEO, 2),
                     Line(p0, p0 + P3(0, R1 + 0.15)).set_stroke(GEO, 2))
        for g_ in range(0, 91, 15):
            aa = math.radians(g_)
            trf.add(Line(p0 + R1 * P3(math.cos(aa), math.sin(aa)), p0 + (R1 - 0.12) * P3(math.cos(aa), math.sin(aa))).set_stroke(GEO, 1.6))
        fx = VGroup(AnnularSector(inner_radius=R0, outer_radius=R1, angle=math.radians(TH_R), start_angle=0, arc_center=p0).set_stroke(width=0).set_fill(VEL, 0.85),
                    AnnularSector(inner_radius=R0, outer_radius=R1, angle=math.radians(90 - TH_V), start_angle=math.radians(TH_V), arc_center=p0)
                    .set_stroke(width=0).set_fill(VEL, 0.85))
        lb = VGroup(rot("0° a 4,23°", 28, VEL).next_to(p0 + P3(R1 + 0.2, 0.12), RIGHT, buff=0.1),
                    VGroup(rot("85,77°", 26, VEL), rot("a 90°", 26, VEL)).arrange(DOWN, buff=0.06, aligned_edge=RIGHT).next_to(p0 + P3(-0.12, R1 * 0.8), LEFT, buff=0.55))
        self.ate(0.2)
        resp = cartao("SÓ QUASE RASANTE", "OU QUASE NA VERTICAL", size=30)
        lim = cartao("NOS LIMITES: A PONTA OPOSTA", size=28)                            # v6 §1.6: entra com a fala sobre os ângulos-limite
        self.pilha.poe(resp)
        self.pilha.poe(lim)
        self.gat("quase rasante, ou quase na vertical")
        self.play(FadeIn(trf), FadeIn(fx), FadeIn(lb), FadeIn(resp, shift=0.1 * UP), run_time=0.9)
        lg.th.set_value(TH_R)
        self.gat("nos dois ângulos limite")
        self.play(lg.tau.animate(rate_func=linear).set_value(lg.T()), FadeIn(lim, shift=0.1 * UP), run_time=1.0)            # ele pousa na ponta da folha
        self.play(lg.tau.animate.set_value(lg.T() + 0.3), run_time=0.4)
        self.gat("a folha foge dele")
        self.play(Indicate(resp, color=WHITE_, scale_factor=1.0), run_time=0.6, sutil=True)
        self.foco = resp
        self.ate(0.97)

    def desloc(self):
        """v4 §5: duas setas GEO saindo da posição inicial (tracejado vertical): uma para trás com 6 cm (o recuo da folha, logo abaixo da
        água) e outra para a frente com 24 cm (o gafanhoto, mais embaixo); a régua da folha marca os 30."""
        lg = self.lg
        cam = lg.f3d.e["cam"]
        X = lambda x: lg.P(x, 0, cam=cam)[0]
        yw_ = lg.P(0, 0, cam=cam)[1]
        y6, y24 = yw_ - 0.85, yw_ - 1.45                                                # v5: um pouco mais fundo (o "0" da régua da folha fica entre a folha e a seta)
        g = VGroup(DashedLine(P3(X(0), yw_ - 0.2), P3(X(0), y24 - 0.22), dash_length=0.08).set_stroke(WHITE_, 2, opacity=0.75),
                   seta(P3(X(0), y6), P3(X(-0.06), y6), GEO, 6, tip=min(0.2, 0.45 * abs(X(0) - X(-0.06)))),
                   rot("6 cm", 26, GEO).next_to(P3((X(0) + X(-0.06)) / 2, y6), DOWN, buff=0.14),
                   seta(P3(X(0), y24), P3(X(0.24), y24), GEO, 6, tip=0.2),
                   rot("24 cm", 26, GEO).next_to(P3(X(0.24), y24), DOWN, buff=0.16))
        return g

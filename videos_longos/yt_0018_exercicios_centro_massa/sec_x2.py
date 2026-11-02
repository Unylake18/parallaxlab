"""Lote PX2 (v2): X2 o fio nas arestas do cubo (Three.js 'cubo' + camadas Manim presas pela mesma câmera).
X2-1 o cubo gira devagar e o fio se desenha aresta a aresta com "comprimento", "largura", "altura"; a cota 1 m nasce na primeira aresta ·
X2-2 para numa vista fixa; cada aresta acende e encolhe até uma partícula M/3 (rótulos acima e para fora, sem tocar eixos, G27) ·
X2-3 projeções nos eixos; cada valor voa da projeção para a conta (G23); o ⊕ nasce em (5/6; 1/2; 1/6) · X2-3b PEGADINHA troca o selo;
a linha errada na Pilha, riscada · X2-4 volta a girar; cota √2/6 ≈ 24 cm; CONFERE e DICA na faixa de selo.
v4 §2 #11–#12, §6: cubo ×0,85 (K 2,8) e mais alto: cubo, eixos e rótulos dentro do ESQUEMA em todo ângulo. Na pegadinha a câmera gira até a
vista em que os dois pontos mais se separam, mas a 12 cm um do outro eles não passam de 0,33 na tela nesta escala: o ⊕ (CERTO) e o ⊗ (CANTOS)
aparecem num quadro AMPLIADO ×5, separados ≥ 0,6. A cota d ganha o rótulo no desenho (d ≈ 24 cm)."""
from pecas18 import *  # noqa: F401,F403

F = lambda a, b: rf"\tfrac{{{a}}}{{{b}}}"
FR = {0: "0", 0.5: F(1, 2), 1: "1"}


class LoteX2(Prob2):
    def construct(self):
        self.setup_base(cap="PROBLEMA 3 · O FIO NO CUBO")
        self.x2()
        self.fim()
        self.relatorio()
        self.gravar_reg()

    def pts_cubo(self, az=None, K=None, xc=None):
        """Pontos projetados das arestas do cubo e dos eixos (estão no 3D, o Manim não os vê): obstáculos para os rótulos."""
        cb = self.cb
        if az is not None or K is not None or xc is not None:
            az = cb.az.get_value() if az is None else az
            cam_a = cam_obl(az, cb.el.get_value(), (0.5, 0.5, 0.5), K=cb.K if K is None else K, xc=cb.xc if xc is None else xc, yc=cb.yc, fov=16)
            cb = type("CbAz", (), {"p": staticmethod(lambda q: projeta3d(cam_a, q))})
        out = []
        for a, b in (((0, 0, 0), (1.38, 0, 0)), ((0, 0, 0), (0, 1.38, 0)), ((0, 0, 0), (0, 0, 1.38))):
            out += [cb.p(tuple(np.array(a) + (np.array(b) - np.array(a)) * u)) for u in np.linspace(0, 1, 24)]
        for p_ in ((0, 0, 0), (1, 0, 0), (0, 1, 0), (1, 1, 0), (0, 0, 1), (1, 0, 1), (0, 1, 1), (1, 1, 1)):
            for d_ in ((1, 0, 0), (0, 1, 0), (0, 0, 1)):
                q = tuple(a + b for a, b in zip(p_, d_))
                if max(q) <= 1:
                    out += [cb.p(tuple(np.array(p_) + np.array(d_) * u)) for u in np.linspace(0, 1, 14)]
        return np.array(out)

    def x2(self):
        VV2 = [(0, 0, 0), (1, 0, 0), (1, 1, 0), (1, 1, 1)]
        AZ = -52.0
        A0 = AZ - 3.0 * dur("X2-1") - 3.0
        cb = self.cb = Cubo18(self, K=2.8, xc=-3.85, yc=-0.6, az=A0, el=24.0, op=1.0)        # quadro 0 já com o cubo (v4: ×0,85 e mais alto)
        for d_ in cb.dr:
            d_.set_value(0.0)
        self.add(*cb.trackers(), cb.f3d)
        cb.f3d._quadro()

        op_ev = ValueTracker(0.0)                                                          # v5: os rótulos x/y/z entram com o cubo e saem quando o ZOOM aparece
        self.add(op_ev)

        def eixos():
            g = VGroup()
            o3 = cb.p((0, 0, 0))
            Qe = None
            for q, n in (((1.38, 0, 0), "x"), ((0, 1.38, 0), "y"), ((0, 0, 1.38), "z")):
                tip = cb.p(q)
                u3 = (tip - o3) / max(float(np.linalg.norm(tip - o3)), 1e-6)
                pq = tip + 0.38 * u3                                                       # logo depois da ponta do eixo, na direção dele (nunca em cima do fio)
                if op_ev.get_value() > 0.3:
                    Qe = self.pts_cubo() if Qe is None else Qe
                    for r_ in (0.38, 0.55, 0.75):
                        for fi_ in (0.0, 0.6, -0.6, 1.2, -1.2):
                            c_, s_ = math.cos(fi_), math.sin(fi_)
                            cand = tip + r_ * np.array([c_ * u3[0] - s_ * u3[1], s_ * u3[0] + c_ * u3[1], 0.0])
                            if not ((Qe[:, 0] > cand[0] - 0.2) & (Qe[:, 0] < cand[0] + 0.2) & (Qe[:, 1] > cand[1] - 0.26) & (Qe[:, 1] < cand[1] + 0.26)).any():
                                pq = cand
                                break
                        else:
                            continue
                        break
                if -7.0 < pq[0] < -0.25 and -3.42 < pq[1] < 2.25 and not getattr(self, "_sem_eixos", False):   # sem x/y/z durante as projeções (X2-3); v4: só dentro do ESQUEMA
                    g.add(mtex(n, GEO, 38).move_to(pq).set_opacity(op_ev.get_value()))
            self.reg("cubo", cm=cb.p(Cubo18.CM), meios=[cb.p(q) for q in Cubo18.MEIOS], az=cb.az.get_value())
            return g
        ev = vivo(eixos)
        # ── X2-1 ──
        self.an("X2-1")
        self.chip(1)
        t0 = self.clk.get_value()
        cb.az.add_updater(lambda m: m.set_value(A0 + 3.0 * (self.clk.get_value() - t0)))

        def cota_1m():
            a, b = cb.p((0, -0.16, 0)), cb.p((1, -0.16, 0))
            u = (b - a) / np.linalg.norm(b - a)
            n = np.array([-u[1], u[0], 0.0])
            n = n if n[1] < 0 else -n
            return VGroup(Line(a, b).set_stroke(GEO, 2.4), Line(a - 0.09 * n, a + 0.09 * n).set_stroke(GEO, 2.2), Line(b - 0.09 * n, b + 0.09 * n).set_stroke(GEO, 2.2),
                          mrot("1 m", 30, GEO).move_to((a + b) / 2 + 0.36 * n))
        c1 = vivo(cota_1m)
        gh, gho = ValueTracker(0.0), ValueTracker(1.0)
        self.add(gh, gho)
        VV = [(0, 0, 0), (1, 0, 0), (1, 1, 0), (1, 1, 1)]

        def caminho():
            """v5 G32: o caminho das três arestas (tracejado) cresce junto com a fala; some quando o fio sólido o cobre."""
            u_ = gh.get_value() * 3.0
            o_ = gho.get_value()
            g_ = VGroup()
            for i_ in range(3):
                f_ = min(1.0, max(0.0, u_ - i_))
                if f_ <= 0.01 or o_ < 0.01:
                    continue
                a_, b_ = np.array(VV[i_], float), np.array(VV[i_ + 1], float)
                sg = VMobject().set_points_as_corners([cb.p(tuple(a_ + (b_ - a_) * s_)) for s_ in np.linspace(0, f_, 8)])
                g_.add(DashedVMobject(sg, num_dashes=max(4, int(14 * f_)), dashed_ratio=0.55).set_stroke(GEO, 2.6, opacity=0.8 * o_))
            return g_.set_z_index(9)
        cmn = vivo(caminho)
        self.add(cmn)
        self.pede("MONTAR POR PARTES")                                                      # v5 G32: o selo entra logo depois do chip
        dados = cartao("FIO UNIFORME DOBRADO", "EM 3 ARESTAS DE 1 m", size=30)              # v5 G32: o enunciado já está na CONTA desde o primeiro quadro
        self.pilha.poe(dados)
        self.add(ev, dados)                                                                 # o cartão já está na tela no primeiro quadro (a transição do lote não deixa a tela vazia)
        self.play(cb.f3d.op.animate.set_value(1.0), op_ev.animate.set_value(1.0), run_time=0.6)
        self.ate(0.1)
        self.gat("dobrado ao longo")
        self.play(gh.animate(rate_func=linear).set_value(1.0), run_time=max(1.0, 0.5 * dur("X2-1") - (self.nq - self._q0) / FPS))
        for k, f_ in enumerate((0.32, 0.45, 0.58)):                  # "comprimento", "largura", "altura"
            self.ate(f_)
            self.gat(("comprimento", "largura", "altura")[k])
            self.play(cb.dr[k].animate.set_value(1.0), *([FadeIn(c1)] if k == 0 else []), *([gho.animate.set_value(0.0)] if k == 2 else []), run_time=0.8)
        cmn.clear_updaters()
        self.remove(cmn)
        self.ate(0.68)
        self.hip("FIO UNIFORME → MASSA ∝ COMPRIMENTO")
        q = tx("ONDE FICA O ⊕ DO FIO?", 32, bold=True)
        self.pilha.poe(q)
        self.ate(0.86)
        self.play(FadeIn(q, shift=0.1 * UP), run_time=0.6)
        self.foco = q
        self.ate(0.92)
        # ── X2-2 ──
        self.an("X2-2")
        cb.az.clear_updaters()
        a0 = cb.az.get_value()
        m0 = 3.0 * 2.0 / max(AZ - a0, 1e-3)
        c1.clear_updaters()
        self.play(cb.az.animate(rate_func=lambda s: (s ** 3 - 2 * s ** 2 + s) * m0 + (-2 * s ** 3 + 3 * s ** 2)).set_value(AZ), FadeOut(c1), run_time=2.0)
        self.pilha.limpa()
        L1 = VGroup(VGroup(txt("CADA ARESTA", 30), MathTex(r"\rightarrow\ \tfrac{M}{3}", font_size=48, color=WHITE_)).arrange(RIGHT, buff=0.2),
                    txt("NO MEIO DELA", 30)).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
        L1[0][1]._partes = [(r"\rightarrow", WHITE_)]
        self._evitar = [self.pts_cubo]
        self.pilha.poe(L1)
        self.play(FadeIn(L1, shift=0.1 * UP), run_time=0.6)                                 # v5 G32: a regra da aresta já está na CONTA enquanto os rótulos nascem
        rot_m = []
        for k, f_ in enumerate((0.12, 0.34, 0.56)):
            self.ate(f_)
            self.play(cb.br[k].animate.set_value(1.0), run_time=0.5)
            lab = self.rotulo(mtex(r"\tfrac{M}{3}", WHITE_, 38), cb.p(Cubo18.MEIOS[k]), lados=(UP, UR, UL, RIGHT, LEFT), buffs=(0.22, 0.38, 0.55))
            self.play(cb.enc[k].animate.set_value(1.0), cb.part[k].animate.set_value(1.0), cb.br[k].animate.set_value(0.0), FadeIn(lab), run_time=1.0)
            rot_m.append(lab)
        self.foco = L1
        self.ate(0.97)
        # ── X2-3 ──
        self.an("X2-3")
        P = Cubo18.MEIOS
        specs = [("X", 0, lambda q: (q[0], 0, 0), (0.5, 1, 1), F(5, 6), 5 / 6), ("Y", 1, lambda q: (0, q[1], 0), (0, 0.5, 1), F(1, 2), 0.5),
                 ("Z", 2, lambda q: (0, 0, q[2]), (0, 0, 0.5), F(1, 6), 1 / 6)]
        self.pilha.so(L1, anims=[FadeOut(m) for m in rot_m])                                # v5 G32: a regra da aresta fica no topo (a CONTA não esvazia)
        eqs, medias, marcas = [], [], []
        self._sem_eixos = True
        zero_lab = None
        esferas = np.array([cb.p(m_) for m_ in P])
        ring = np.array([[e_[0] + 0.3 * math.cos(a_), e_[1] + 0.3 * math.sin(a_), 0.0] for e_ in esferas for a_ in np.linspace(0, 2 * PI, 12, endpoint=False)])
        for j, (nome, ax, pj, vals, media, mv) in enumerate(specs):
            self.ate(0.08 + 0.26 * j)
            linhas = VGroup(*[tracejado(cb.p(P[k]), cb.p(pj(P[k])), WHITE_, 2, 0.65) for k in range(3)]).set_z_index(9)
            pts = VGroup(*[Dot(cb.p(pj(P[k])), radius=0.055, color=GEO).set_z_index(10) for k in range(3)])
            self.play(Create(linhas), FadeIn(pts), run_time=0.8)
            labs, vistos = {}, {}
            for k in range(3):
                v = vals[k]
                if v == 0 and zero_lab is not None:                                 # o "0" da origem nasce uma vez só e fica até o fim do Z
                    vistos[v] = zero_lab
                elif v not in vistos:
                    q3 = [0, 0, 0]
                    q3[ax] = v
                    m = MathTex(FR[v], font_size=36, color=GEO)
                    m._partes = [(FR[v], GEO)]
                    vistos[v] = self.rotulo(m, cb.p(tuple(q3)), lados=(DOWN, DL, DR, LEFT, RIGHT), buffs=(0.3, 0.4, 0.55),
                                            extra_pts=np.vstack([np.array([d.get_center() for d in pts]), ring]))[0]
                    if v == 0:
                        zero_lab = vistos[v]
                labs[k] = vistos[v]
            self.play(*[FadeIn(m) for m in vistos.values() if m is not zero_lab or j == specs.index(next(s for s in specs if 0 in s[3]))], run_time=0.5)
            E, ie = M(nome, "=", r"\big(", FR[vals[0]], "+", FR[vals[1]], "+", FR[vals[2]], r"\big)", "/", "3", "=", media, r"\ \mathrm{m}",
                      size=48, cores={0: CMC, 3: GEO, 5: GEO, 7: GEO, 12: CMC})
            self.pilha.poe(E)
            self.voa([(labs[k], mp(E, ie, [3 + 2 * k])) for k in range(3)], extra=[FadeIn(mp(E, ie, [0, 1, 2, 4, 6, 8, 9, 10]))], rt=1.1)
            q3 = [0, 0, 0]
            q3[ax] = mv
            mk = Dot(cb.p(tuple(q3)), radius=0.07, color=CMC).set_z_index(11)
            self.play(FadeIn(mp(E, ie, [11, 12, 13])), FadeIn(mk, scale=1.6), run_time=0.8)
            self.foco = E
            eqs.append(E)
            medias.append(mp(E, ie, [12]))
            marcas.append(mk)
            self.play(FadeOut(linhas), FadeOut(pts), FadeOut(VGroup(*[m for m in vistos.values() if m is not zero_lab or j == 2])), run_time=0.4)
        self._sem_eixos = False
        cmq = Cubo18.CM
        guia = VGroup(tracejado(cb.p((5 / 6, 0, 0)), cb.p((5 / 6, 0.5, 0)), CMC, 2.2, 0.8), tracejado(cb.p((0, 0.5, 0)), cb.p((5 / 6, 0.5, 0)), CMC, 2.2, 0.8),
                      tracejado(cb.p((5 / 6, 0.5, 0)), cb.p(cmq), CMC, 2.2, 0.8)).set_z_index(9)
        self.play(Create(guia), run_time=1.0)
        cm = marcador_cm(cb.p(cmq), r=0.16)
        R, ir = M(r"\vec R_{cm}", "=", r"\big(", F(5, 6), r";\,", F(1, 2), r";\,", F(1, 6), r"\big)\ \mathrm{m}", size=48, cores={0: CMC, 3: CMC, 5: CMC, 7: CMC})
        Rb = caixa_l(R, CMC)
        self.pilha.poe(Rb)
        self.voa([(medias[0], mp(R, ir, [3])), (medias[1], mp(R, ir, [5])), (medias[2], mp(R, ir, [7]))],
                 extra=[FadeIn(cm, scale=1.6), FadeIn(Rb[0]), FadeIn(mp(R, ir, [0, 1, 2, 4, 6, 8]))], rt=1.0)
        self.reg("cubo_cm", cm=cm.get_center(), esperado=cb.p(cmq))
        self.foco = Rb
        self.ate(0.97)
        # ── X2-3b ──
        self.an("X2-3b")
        self.play(FadeOut(guia), *[FadeOut(m) for m in marcas], run_time=0.5)
        self.selo("PEGADINHA", ["A MASSA ESTÁ NAS ARESTAS, NÃO NOS CANTOS"], cor=HEAT, borda=HEAT)
        ER = (0.75, 0.5, 0.25)
        sep = lambda az_: float(np.linalg.norm(projeta3d(cam_obl(az_, 24.0, (0.5, 0.5, 0.5), K=cb.K, xc=cb.xc, yc=cb.yc, fov=16), ER)
                                               - projeta3d(cam_obl(az_, 24.0, (0.5, 0.5, 0.5), K=cb.K, xc=cb.xc, yc=cb.yc, fov=16), Cubo18.CM)))
        az_b = max(np.arange(AZ - 40.0, AZ + 40.1, 2.0), key=sep)                  # a vista em que o ⊕ e o ⊗ mais se separam (perto da atual)
        cm.add_updater(lambda m: m.move_to(cb.p(cmq)))                             # o ⊕ acompanha o cubo quando a câmera gira
        KZ, XCZ = 0.8 * cb.K, -5.15                                                 # v6 §1.1: o cubo encolhe a 80% e vai para a esquerda: abre um canto para o painel
        self.play(cb.Kt.animate.set_value(KZ), cb.xct.animate.set_value(XCZ), op_ev.animate.set_value(0.0), run_time=0.6)
        self.play(cb.az.animate.set_value(az_b), run_time=0.9)
        cantos = VGroup(*[Dot(cb.p(c), radius=0.08, color=HEAT).set_z_index(12) for c in Cubo18.CANTOS])
        self.ate(0.12)
        self.play(FadeIn(cantos), op_ev.animate.set_value(0.0), run_time=0.5)                       # x/y/z saem antes de o ZOOM entrar
        self.play(cantos.animate.set_opacity(0.2), run_time=0.35)
        self.play(cantos.animate.set_opacity(1.0), run_time=0.35)
        # quadro AMPLIADO ×5 em volta dos dois pontos: CERTO (⊕) e CANTOS (⊗), separados ≥ 0,6
        pc_, pe_ = cm.get_center(), cb.p(ER)
        meio = (pc_ + pe_) / 2
        AMP = 5.0
        bxa = RoundedRectangle(corner_radius=0.08, width=2.9, height=1.36).set_fill(PANEL, 0.9).set_stroke(BLUE_L, 1.6)
        bxa._fundo = bxa._caixa = True
        Qc = np.vstack([self.pts_cubo(az=az_b + d_, K=KZ, xc=XCZ) for d_ in (-10.0, 0.0, 7.0, 14.0, 24.0)])                  # o cubo balança até +14° no fim da fala
        cands = [P3(x_, y_) for x_ in np.linspace(-6.0, -1.7, 12) for y_ in np.linspace(-3.0, 1.2, 10)]
        nin = lambda c_: int(((Qc[:, 0] > c_[0] - 1.6) & (Qc[:, 0] < c_[0] + 1.6) & (Qc[:, 1] > c_[1] - 0.82) & (Qc[:, 1] < c_[1] + 1.15)).sum())      # pontos do cubo na caixa (e na etiqueta)
        bxa.move_to(min(cands, key=lambda q: (nin(q), -np.linalg.norm(q - meio))))                       # a caixa mais vazia do ESQUEMA (de preferência longe dos dois pontos)
        print(f"[dbg] ZOOM: caixa em ({bxa.get_x():.1f}; {bxa.get_y():.1f}) com {nin(bxa.get_center())} pontos do cubo")
        c0 = bxa.get_center() + 0.18 * UP
        sep_a = max(0.6, min(1.6, AMP * float(np.linalg.norm(pe_ - pc_))))
        qc, qe = c0 + 0.5 * sep_a * LEFT, c0 + 0.5 * sep_a * RIGHT                                 # lado a lado, ≥ 0,6 (×5)
        tag_a = txt("ZOOM ×5", 24, color=CYAN, bold=True).next_to(bxa, UP, buff=0.08).align_to(bxa, LEFT if bxa.get_x() < meio[0] else RIGHT)       # do lado oposto à linha de ligação
        cm_a = marcador_cm(qc, r=0.15)
        fant = VGroup(Circle(radius=0.15).move_to(qe).set_stroke(HEAT, 3), Dot(qe, radius=0.05, color=HEAT)).set_z_index(38)
        xis = VGroup(Line(qe + P3(-0.17, -0.17), qe + P3(0.17, 0.17)).set_stroke(HEAT, 3.5), Line(qe + P3(-0.17, 0.17), qe + P3(0.17, -0.17)).set_stroke(HEAT, 3.5)).set_z_index(38)
        l_c = txt("CERTO", 24).next_to(qc, DOWN, buff=0.42)
        l_e = txt("CANTOS", 24, color=HEAT).next_to(qe, DOWN, buff=0.42)
        anel = Circle(radius=0.32).move_to(meio).set_stroke(BLUE_L, 1.6, opacity=0.8).set_z_index(12)                 # onde fica o trecho ampliado
        lig = VGroup(*[Line(meio + 0.32 * (c_ - meio) / max(np.linalg.norm(c_ - meio), 1e-6), c_).set_stroke(BLUE_L, 1.2, opacity=0.6)
                       for c_ in (bxa.get_corner(UR if bxa.get_x() < meio[0] else UL), bxa.get_corner(DR if bxa.get_x() < meio[0] else DL))]).set_z_index(11)
        Wm, iw = M("=", r"\big(", F(3, 4), r";\,", F(1, 2), r";\,", F(1, 4), r"\big)", size=46)
        W = linha_m("MÉDIA DOS 4 CANTOS", Wm)
        self.pilha.poe(W)
        self.ate(0.3)
        self.play(FadeIn(bxa), FadeIn(tag_a), FadeIn(anel), FadeIn(lig), FadeIn(cm_a), FadeIn(l_c), run_time=0.5)
        self.play(FadeIn(W), *[TransformFromCopy(cantos[k], fant[1]) for k in range(4)], run_time=1.1)                 # os cantos se juntam no ⊗ (no ampliado)
        self.add(fant)
        self.play(FadeIn(fant[0]), FadeIn(l_e), run_time=0.4)
        self.ate(0.5)
        rk = risco(W, HEAT, 4.5)
        self.play(Create(rk), W.animate.set_opacity(0.4), Create(xis), run_time=0.8)
        self.play(FadeOut(cantos), run_time=0.4)
        self.foco = W
        self.ate(0.75)
        mm = VGroup(*[Dot(cb.p(q_), radius=0.09, color=WHITE_).set_z_index(12) for q_ in Cubo18.MEIOS])
        self.play(FadeIn(mm, scale=1.8), run_time=0.5)
        self.play(FadeOut(mm), run_time=0.5)
        self.ate_mov(0.97, cb.az, cb.az.get_value() + 14.0, rate=there_and_back)        # PAUSAS: o cubo balança enquanto a fala termina
        # ── X2-4 ──
        self.an("X2-4")
        self.play(FadeOut(VGroup(fant, xis, rk, bxa, tag_a, anel, lig, cm_a, l_c, l_e)), *[e.animate.set_value(0.0) for e in cb.enc], *[p_.animate.set_value(0.0) for p_ in cb.part],
                  FadeOut(cm), run_time=0.9)
        self.play(cb.Kt.animate.set_value(2.8), cb.xct.animate.set_value(-3.85), run_time=0.6)        # v6 §1.1: o cubo volta ao tamanho (0,6 s) depois de o painel sair
        self.pilha.limpa()
        t1 = self.clk.get_value()
        a1 = cb.az.get_value()
        cb.az.add_updater(lambda m: m.set_value(a1 + 5.0 * min(1.0, max(0.0, self.clk.get_value() - t1)) - 2.5 * min(1.0, max(0.0, self.clk.get_value() - t1)) ** 2))
        az_f = a1 + 2.5                                                                           # v5: a câmera para em 1 s (o rótulo d não corre mais risco de cruzar o fio)
        cam_f = cam_obl(az_f, cb.el.get_value(), (0.5, 0.5, 0.5), K=cb.K, xc=cb.xc, yc=cb.yc, fov=16)
        Pf = lambda q: projeta3d(cam_f, q)
        cm_f = Pf(Cubo18.CM)
        Qf = self.pts_cubo(az=az_f)
        fio = np.array([Pf(tuple(np.array(a_, float) + (np.array(b_, float) - np.array(a_, float)) * s_)) for a_, b_ in zip(VV2[:-1], VV2[1:]) for s_ in np.linspace(0, 1, 40)])
        ld0 = mtex(r"d\approx 24\ \mathrm{cm}", GEO, 36)
        melhor = None
        for livre_chamada in (True, False):
            for r_ in (0.95, 1.25, 1.55, 1.9, 2.3):
                for ang in np.arange(0, 360, 20):
                    c_ = cm_f + r_ * P3(math.cos(math.radians(ang)), math.sin(math.radians(ang)))
                    x0_, x1_, y0_, y1_ = c_[0] - ld0.width / 2 - 0.14, c_[0] + ld0.width / 2 + 0.14, c_[1] - ld0.height / 2 - 0.14, c_[1] + ld0.height / 2 + 0.14
                    if x0_ < -7.2 or x1_ > -0.1 or y0_ < -3.5 or y1_ > 2.3 or ((Qf[:, 0] > x0_) & (Qf[:, 0] < x1_) & (Qf[:, 1] > y0_) & (Qf[:, 1] < y1_)).any():
                        continue
                    u_ = (c_ - cm_f) / np.linalg.norm(c_ - cm_f)
                    fim_ = max(0.4, float(np.linalg.norm(c_ - cm_f)) - 0.5 * max(ld0.width * abs(u_[0]), ld0.height * abs(u_[1])) - 0.1)
                    seg_ = np.array([cm_f + u_ * s_ for s_ in np.linspace(0.3, fim_, 16)])
                    if livre_chamada and float(np.min(np.linalg.norm(fio[None, :, :2] - seg_[:, None, :2], axis=2))) < 0.13:
                        continue
                    melhor = (c_, cm_f + u_ * 0.3, cm_f + u_ * fim_)
                    break
                if melhor:
                    break
            if melhor:
                break
        pos_d, ini_d, fim_d = melhor

        def cm_cota():
            c, a = cb.p(Cubo18.CM), cb.p((1, 0.5, 0))
            self.reg("cubo_cm", cm=c, esperado=c, aresta=a)
            u_ = (a - c) / max(np.linalg.norm(a - c), 1e-6)
            n_ = np.array([-u_[1], u_[0], 0.0])
            n_ = n_ if n_[1] > 0 else -n_                                                            # o rótulo do lado de cima da cota
            ld = mtex(r"d\approx 24\ \mathrm{cm}", GEO, 36).set_opacity(op_d.get_value())
            ld.move_to(pos_d)                                                                          # v5: do lado livre do ⊕, longe do fio
            return VGroup(tracejado(c, a, WHITE_, 2.4, 0.85, dash=0.07).set_z_index(10), Dot(a, radius=0.05, color=WHITE_).set_z_index(10), marcador_cm(c, r=0.16), ld,
                          Line(ini_d, fim_d).set_stroke(GEO, 1.6, opacity=0.8 * op_d.get_value()).set_z_index(10))
        op_d = ValueTracker(0.0)
        self.add(op_d)
        cc = vivo(cm_cota)
        R2, _ = M(r"\vec R_{cm}", "=", r"\big(", F(5, 6), r";\,", F(1, 2), r";\,", F(1, 6), r"\big)\ \mathrm{m}", size=48, cores={0: CMC, 3: CMC, 5: CMC, 7: CMC})
        self.pilha.poe(R2)
        self.play(FadeIn(cc), FadeIn(R2), run_time=0.8)
        D_, id_ = M("d", "=", r"\tfrac{\sqrt2}{6}\ \mathrm{m}", r"\approx", r"24\ \mathrm{cm}", size=48, cores={0: GEO, 2: GEO, 4: GEO})
        self.pilha.poe(D_)
        self.ate(0.12)
        self.play(FadeIn(D_, shift=0.1 * UP), op_d.animate.set_value(1.0), run_time=0.7)
        cdc = cartao("O CENTRO DE MASSA NÃO PRECISA", "ESTAR EM CIMA DO MATERIAL", size=26)
        self.pilha.poe(cdc)
        self.ate(0.3)
        self.play(FadeIn(cdc, shift=0.1 * UP), run_time=0.6)
        self.foco = cdc
        self.ate(0.45)
        self.confere(["AS TRÊS COORDENADAS ENTRE 0 E 1 → DENTRO DO CUBO"])
        self.ate(0.72)
        self.dica18(["EM 3D, CADA COORDENADA É UMA CONTA DE UMA DIMENSÃO"])
        self.ate(0.97)
        cb.az.clear_updaters()

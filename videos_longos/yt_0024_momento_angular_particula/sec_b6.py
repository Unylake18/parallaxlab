"""Lote PB6 v2: B6 — DE VOLTA À MESA (Three.js 'mesa_furo' v2: C_34 → C_TOPO; reprise da puxada em CÂMERA LENTA ×0,5).
HUD (no máximo 3, à direita da mesa, fora da CONTA): r (barra 0…0,60 m), ω (arco 0…10 rad/s) e L (cadeado) → İ (B6-4) → v_θ (B6-5…7).
Setas NA MESA durante a reprise (v2 §3.2): T⃗ (azul, para o furo) e v⃗ (violeta), presas ao disco do B6-2 ao B6-7. Os anéis de 0,60 e 0,30 m
da grade acendem e o raio antigo fica como fantasma até o fim do B6-5. τ = dL/dt com I variável: τ_z = I α + İ ω (r = 0,45 m: I = 0,0405,
ω = 4,44, İ = −0,054 ⇒ α = +5,9 rad/s²). Triângulos de 0,20 s varridos junto com o disco (0,090 m² cada). B6-7: inset ZOOM ×3 no MESMO
referencial da mesa (sem girar): v⃗ = v_r + v_θ com o retângulo da decomposição, T⃗ paralela a v_r e no mesmo sentido ⇒ W > 0, 8,5° entre v⃗
e a tangente. B6-8: barras de energia (a mesa sai). B6-9: a mesa volta com a reprise e o gráfico T × r (grafico_lab) com o ponto vivo."""
from pecas24 import *  # noqa: F401,F403


def cartao_ideia(pecas, cor=BLUE_L):
    """Cartão curto (mesmo desenho do PS): peças em linha de base dentro de um painel com borda na cor."""
    g = linha_base([txt(p, 28, bold=True) if isinstance(p, str) else p for p in pecas], 0.12)
    r = RoundedRectangle(corner_radius=0.1, width=g.width + 0.5, height=g.height + 0.36).move_to(g).set_fill(PANEL, 0.92).set_stroke(cor, 2)
    r._fundo = True
    return VGroup(r, g).set_z_index(20)

T45 = F.TR + (F.R0 - F.VR * F.TR / 2 - 0.45) / F.VR       # tempo da puxada em que r = 0,45 m (fase de v_r constante)


class LoteB6(Lote24):
    def estado3d(self, _t=0.0):
        e = super().estado3d(_t)
        k = float(self.aneis_tr.get_value())
        if k > 0:
            e["aneis"] = {"r30": round(k, 3), "r60": round(k, 3)}
        return e

    def corpo(self):
        self.camA = self.camB = C34B6
        self.mov = mov_puxada(self)
        self.zp = zp_puxada(self)
        self.vth = vth_puxada(self)
        self.aneis_tr = ValueTracker(0.0)
        self.add(self.aneis_tr)
        self.anda(1.0, tf=0.0)
        f3 = self.mesa()
        f3.op.set_value(1.0)
        self.canto("DE VOLTA À MESA")
        Z = 0.012

        self.fant_on, self.loop = False, None

        def est():
            if self.fant_on:                              # v3 §2.4: durante a conta o HUD mostra o instante congelado (r = 0,45 m)
                return F.puxada(T45)
            return F.puxada(self.tf() - self.tp)

        def pD():
            x, y = self.disco()
            return np.array([x, y, Z])

        def dirs():
            x, y = self.disco()
            r = math.hypot(x, y)
            er = np.array([x / r, y / r, 0.0])
            et = np.array([-y / r, x / r, 0.0])
            return er, et

        def t_viva(w=6, comp=1.0):
            def f():
                a, o = self.tela(pD()), self.tela((0, 0, Z))
                u = (o - a) / max(np.linalg.norm(o - a), 1e-6)
                n = np.array([-u[1], u[0], 0])
                vd = v_dir()
                if float(np.dot(n[:2], vd[:2])) > 0:        # v5 #21: o rótulo T⃗ fica do lado OPOSTO ao de v⃗ (nunca encostado nele)
                    n = -n
                return VGroup(etiqueta_vec(vetor_lab(a + 0.22 * u, a + (0.22 + 0.8 * comp) * u, FC, w=w, origem=False), "aponta", alvo=lambda: self.tela((0, 0, Z)), nome="T⃗ B6"),
                              T(r"\vec T", 38, FC).move_to(a + 0.70 * u - 0.66 * n))                  # v5 G28: mais afastado do v⃗
            return f

        def v_dir():
            e = est()
            er, et = dirs()
            v = e["vr"] * er + e["vth"] * et
            d_ = self.tela(pD() + 0.10 * v) - self.tela(pD())
            return d_ / max(np.linalg.norm(d_), 1e-6)

        def v_viva():
            e = est()
            er, et = dirs()
            v = e["vr"] * er + e["vth"] * et
            a, b = self.tela(pD()), self.tela(pD() + 0.10 * v)        # 0,10 m por m/s (v até 3,0 m/s cabe na mesa)
            u = (b - a) / max(np.linalg.norm(b - a), 1e-6)
            nv_ = np.array([-u[1], u[0], 0.0])
            if float(np.dot(nv_[:2], (self.tela((0, 0, Z)) - a)[:2])) > 0:     # v5 G28: o rótulo de v⃗ sai do lado oposto ao de T⃗
                nv_ = -nv_
            return VGroup(etiqueta_vec(vetor_lab(a + 0.2 * u, b, VEL, w=6, origem=False), "sentido", ref=lambda: self.tela(pD() + 0.10 * (est()["vr"] * dirs()[0] + est()["vth"] * dirs()[1])) - self.tela(pD()), nome="v⃗ B6"),
                          T(r"\vec v", 38, VEL).move_to(b + 0.40 * u + 0.30 * nv_))

        # ── B6-1: C_34, órbita de 0,60 m; hipóteses em chips; tração central ⇒ L constante ──
        self.an("B6-1")
        self.transicao(0.5)
        self.gat("de volta à mesa")
        hip = chips(["SEM ATRITO", "FIO IDEAL", "DISCO PEQUENO"]).move_to(P3(3.75, 3.02))
        hip._chip = True
        self.play(LaggedStart(*[FadeIn(c, shift=0.06 * DOWN) for c in hip], lag_ratio=0.3), run_time=0.8)
        anel_d = vivo(lambda: Circle(radius=0.34).set_stroke(WHITE_, 1.6, opacity=0.9).move_to(self.tela_disco()).set_z_index(9))      # v4 §2: disco ≥ 2 % com anel de destaque (raio 2,2× o do disco)
        self.play(OpVivo(anel_d), run_time=0.4)
        Tv = vivo(t_viva())
        self.gat("a tração aponta sempre para o furo")
        self.play(OpVivo(Tv), run_time=0.5)
        A, ia = Mx(r"\vec\tau", "=", "0", r"\ \Rightarrow\ ", r"\vec L", "=")
        self.pilha.poe(A)
        self.gat("é uma força central")
        self.lei(A, ia, rt=1.3, metodo="lei")
        self.texto_na_linha(A, "CONSTANTE", LMAG, size=30)
        self.gat("mesmo enquanto alguém puxa")
        self.play(Indicate(gl(A, J(ia, 4)), color=LMAG, scale_factor=1.2), run_time=0.7)
        self.ate(0.99)

        # ── B6-2: C_TOPO; reprise ×0,5; anéis acendem; fantasma do raio; setas na mesa; HUD r, ω, L; CONTA ──
        self.an("B6-2")
        self.play(OpVivo(Tv, entra=False), FadeOut(hip), run_time=0.3)
        self.remove(Tv)
        self.pilha.limpa()
        self.dolly(CPLANO, 1.6)
        self.selo("CÂMERA LENTA", "×0,5")
        mr = hud("r", lambda: est()["r"], 2, "M", VETC, slot=0, ind="barra", faixa=(0.0, 0.60))
        mw = hud(r"\omega", lambda: est()["w"], 2, "RAD/S", VEL, slot=1, ind="arco", faixa=(0.0, 10.0))
        mL = hud("L", lambda: est()["L"], 3, "KG·M²/S", LMAG, slot=2, trava=lambda: True)
        Tm = vivo(t_viva(w=5, comp=0.9))
        vm = vivo(v_viva)
        self.play(OpVivo(mr), OpVivo(mw), OpVivo(mL), OpVivo(Tm), OpVivo(vm), self.aneis_tr.animate.set_value(1.0), run_time=0.6)
        print(f"[seta] TV on {self.clk.get_value():.3f}")
        # v13 §2.3.3: mini-inset (esquema do ZOOM do B6-7) enquanto a fala separa a velocidade em duas partes: v_r ∥ r⃗ não entra em r⃗ × p⃗
        Zm = P3(4.9, 0.45)
        ur_m, ut_m = LEFT, UP
        p_vt_m, p_vr_m = Zm + 1.15 * ut_m, Zm + 0.62 * ur_m
        p_v_m = p_vt_m + (p_vr_m - Zm)
        q_m = RoundedRectangle(width=5.8, height=3.7, corner_radius=0.12).move_to(P3(3.95, 0.45)).set_fill(PANEL, 0.72).set_stroke(GEO, 1.6)
        q_m._fundo = True
        d_m = VGroup(Circle(radius=0.26).move_to(Zm).set_fill("#2A303B", 1).set_stroke(MAS, 4), Dot(Zm, radius=0.05, color=WHITE_)).set_z_index(9)
        f_m = DashedLine(Zm + 0.30 * ur_m, Zm + 2.45 * ur_m, dash_length=0.08).set_stroke(VETC, 1.8, opacity=0.8)
        o_m = Dot(Zm + 2.45 * ur_m, radius=0.07, color=WHITE_)
        lr_m = T(r"\vec r", 38, VETC).move_to(Zm + 1.4 * ur_m + 0.36 * DOWN)
        sv_m = vetor_lab(Zm, p_v_m, VEL, w=6)
        lv_m = T(r"\vec v", 40, VEL).move_to(p_v_m + 0.42 * RIGHT + 0.12 * UP)
        self.gat("a velocidade dele tem duas partes")
        self.play(FadeIn(q_m), FadeIn(d_m), FadeIn(f_m), FadeIn(o_m), FadeIn(lr_m), FadeIn(sv_m), FadeIn(lv_m), run_time=0.6)
        svr_m = vetor_lab(Zm, p_vr_m, VEL, w=5, origem=False, tip=0.16)
        lvr_m = T("v_r", 38, VEL).move_to(p_vr_m + 0.42 * DOWN)
        self.gat("uma para o furo")
        self.play(FadeIn(svr_m), FadeIn(lvr_m), run_time=0.4)
        svt_m = vetor_lab(Zm, p_vt_m, VEL, w=5, origem=False)
        lvt_m = T(r"v_\theta", 38, VEL)
        lvt_m[0][1].set_color(ANG)
        lvt_m.move_to(p_vt_m + 0.55 * RIGHT)
        self.gat("outra ao longo da volta")
        self.play(FadeIn(svt_m), FadeIn(lvt_m), run_time=0.4)
        nota_m = linha_base([txt("PARALELO A", 24, bold=True, color=CYAN), T(r"\vec r", 34, VETC), txt(": NÃO ENTRA", 24, bold=True, color=CYAN)], 0.12)
        nota_m.move_to(P3(3.95, -0.85))
        self.gat("não entra no produto vetorial")
        self.play(FadeIn(nota_m), Indicate(svr_m, color=VEL, scale_factor=1.2), run_time=0.8)
        self.gat("mesmo na espiral")
        mini_m = [q_m, d_m, f_m, o_m, lr_m, sv_m, lv_m, svr_m, lvr_m, svt_m, lvt_m, nota_m]
        self.play(*[FadeOut(m) for m in mini_m], run_time=0.4)
        self.remove(*mini_m)
        B1, b1 = Mx("L", "=", "I", r"\omega")
        self.pilha.poe(B1)
        self.gat("continua sendo o momento de inércia")
        self.lei(B1, b1, rt=0.9, metodo="lei")
        B2, b2 = Mx("I", "=", "m", "r^2")
        self.pilha.poe(B2)
        self.gat("com o momento de inércia igual")
        self.lei(B2, b2, rt=0.8, metodo="lei")
        self.gat("quando o raio cai pela metade")
        self.anda(0.5)
        self.tp = self.tf() + 0.15
        # v5 #5/#21: o "raio antigo" é um ANEL tracejado em r = 0,60 m (na cor da grade, não do r⃗); nunca uma seta/linha laranja
        pts_f = [self.tela((F.R0 * math.cos(a_), F.R0 * math.sin(a_), Z)) for a_ in np.linspace(0, 2 * math.pi, 120)]
        fant = DashedVMobject(VMobject().set_points_as_corners(pts_f), num_dashes=64, dashed_ratio=0.55).set_stroke(GEO, 2.4, opacity=0.85)
        fant.set_z_index(6)
        fant._fantasma = True
        self.play(FadeIn(fant), run_time=0.3)
        B3, b3 = Mx("m", "r^2", r"\omega", "=")
        self.pilha.poe(B3)
        self.gm(B1, B3, (J(b1, 2), J(b3, 0, 1)), (J(b1, 3), J(b3, 2)), (J(b1, 1), J(b3, 3)), (J(b1, 0), []), rt=1.4)
        self.texto_na_linha(B3, "CONSTANTE", LMAG)
        B4, b4 = Mx("r", r"\div 2", r"\Rightarrow", "I", r"\div 4", r"\Rightarrow", r"\omega", r"\times 4")
        self.pilha.so(B2, B3)
        self.pilha.poe(B4)
        self.gat("cai para um quarto")
        self.lei(B4, b4, {0: mr, 6: mw}, rt=1.6)
        self.resultado(B4, VEL)
        self.ate(0.99)

        # ── B6-3: congela em r = 0,45 m; cartão LEI GERAL (fora da cadeia) → cadeia τ_z = d(Iω)/dt → = I dω/dt + (dI/dt) ω → = Iα + İω (hold) ──
        self.an("B6-3")
        self.anda(0.0, tf=self.tp + T45)
        self.sem_selo()
        self.pilha.limpa()
        self.remove(anel_d)
        marca = Circle(radius=0.30).set_stroke(WHITE_, 2.6).set_z_index(9)
        marca.move_to(self.tela_disco())
        self.play(Create(marca), run_time=0.4)
        cart, cm, ic_ = cartao([r"\vec\tau", "=", r"\frac{d\vec L}{dt}"], "LEI GERAL")
        self.gat("a lei geral")
        self.play(FadeIn(cart[0]), Caneta(cart[1]), run_time=1.2)
        C2, c2 = Mx(r"\tau_z", "=", r"\frac{d(I\omega)}{dt}")
        self.pilha.poe(C2)
        self.gat("derivando o momento de inércia")
        self.lei(C2, c2, rt=1.3, metodo="lei")
        C3, c3 = Mx("=", "I", r"\frac{d\omega}{dt}", "+", r"\frac{dI}{dt}", r"\omega")
        self.pilha.poe(C3)
        self.gat("a regra do produto")
        self.gm(C2, C3, (J(c2, 2)[2:3], J(c3, 1)), (J(c2, 2)[3:4], J(c3, 2)[1:2]), (J(c2, 2)[0:1], J(c3, 2)[0:1]), (J(c2, 2)[5:], J(c3, 2)[2:]),
                (J(c2, 2)[1:2] + J(c2, 2)[4:5], J(c3, 3)), ([], J(c3, 4, 5)), ([], J(c3, 0)), rt=1.8)
        C4, c4 = Mx("=", "I", r"\alpha", "+", r"\frac{dI}{dt}", r"\omega")
        self.pilha.poe(C4)
        self.gat("mais a taxa de variação")
        self.gm(C3, C4, *[(J(c3, k), J(c4, k)) for k in range(6)], rt=1.4)
        self.resultado(C4, FC)
        self.gat("a versão curta")
        Cc, cc = Mx(r"\tau_z", "=", "I", r"\alpha")
        self.pilha.poe(Cc)
        self.lei(Cc, cc, rt=0.6, metodo="escrita")
        self.texto_na_linha(Cc, "SÓ COM I CONSTANTE", MAS, size=26)
        self.gat("aqui não é")
        self.play(pulso(gl(C4, J(c4, 4, 5)), 1.2), run_time=0.8)
        self.ate(0.99)

        # ── B6-4: fantasma congelado em r = 0,45 m (HUD do fantasma); 0 = Iα + İω → Iα = −İω → α = −İω/I → números → α = +5,9 rad/s² ──
        self.an("B6-4")
        self.pilha.so(C2, C3, C4)
        self.fant_on = True
        Tf, Vf = t_viva(w=6, comp=1.0)(), v_viva()            # v5 #21: fantasma com a espessura do vetor padrão (6)
        for g in (Tf, Vf):
            g.set_opacity(0.55)
            for x in g.get_family():
                x._fantasma = True
        chip_i = linha_base([txt("INSTANTE", 24, bold=True, color=GEO), T(r"r=0{,}45\,\mathrm{m}", 36)], 0.14).move_to(P3(-4.25, -3.2)).set_z_index(30)
        for x in chip_i.get_family():
            x._chip = True
        # v13 §2.3.4: o 5,9 só vale com o fio recolhido a v_r = 0,30 m/s (a fala supõe isso)
        chip_f = linha_base([txt("FIO RECOLHIDO A", 24, bold=True, color=GEO), T(r"0{,}30\,\mathrm{m/s}", 36, VEL)], 0.14).move_to(P3(-4.25, -2.55)).set_z_index(30)
        for x in chip_f.get_family():
            x._chip = True
        self.loop = (self.tp - 0.2, 1.75)
        self.anda(0.5, tf=self.tp - 0.2)
        self.play(OpVivo(Tm, entra=False), OpVivo(vm, entra=False), FadeIn(Tf), FadeIn(Vf), FadeIn(chip_i), FadeIn(chip_f), FadeOut(cart), run_time=0.5)
        self.remove(Tm, vm)
        D1, d1 = Mx("0", "=", "I", r"\alpha", "+", r"\frac{dI}{dt}", r"\omega")
        self.pilha.poe(D1)
        self.gat("com torque zero")
        self.gm(C4, D1, (J(c4, 0), J(d1, 1)), (J(c4, 1), J(d1, 2)), (J(c4, 2), J(d1, 3)), (J(c4, 3), J(d1, 4)), (J(c4, 4), J(d1, 5)), (J(c4, 5), J(d1, 6)),
                ([], J(d1, 0)), rt=1.2)
        D2, d2 = Mx("I", r"\alpha", "=", "-", r"\frac{dI}{dt}", r"\omega")
        self.pilha.poe(D2)
        self.gat("tem que cancelar a segunda")
        self.gm(D1, D2, (J(d1, 2), J(d2, 0)), (J(d1, 3), J(d2, 1)), (J(d1, 1), J(d2, 2)), (J(d1, 4), J(d2, 3)), (J(d1, 5), J(d2, 4)), (J(d1, 6), J(d2, 5)),
                (J(d1, 0), []), rt=1.4)
        D2b, d2b = Mx(r"\alpha", "=", r"\frac{-\frac{dI}{dt}\,\omega}{I}")
        self.pilha.poe(D2b)
        self.gm(D2, D2b, ([1], [0]), ([2], [1]), ([3], [2]), ([4], [3]), ([5], [4]), ([6], [5]), ([7], [6]), ([8], [7]), ([9], [8]), ([0], [10]), ([], [9]), rt=1.4)
        mId = hud(r"dI/dt", lambda: est()["Idot"], 3, "KG·M²/S", MAS, slot=2, unid_baixo=True)
        self.play(OpVivo(mL, entra=False), run_time=0.25)
        self.remove(mL)
        self.play(OpVivo(mId), run_time=0.25)
        D3, d3 = Mx("=", r"\frac{-(-0{,}054)\cdot 4{,}44}{0{,}0405}")
        self.pilha.poe(D3)
        self.gat("a quarenta e cinco centímetros")
        self.lei(D3, d3, {1: mId}, rt=1.4, numero=True)
        D4, d4 = Mx("=", "+", r"5{,}9", r"\,\mathrm{rad/s^2}", cores={2: ACC})
        self.pilha.poe(D4)
        self.gat("quase seis radianos")
        self.lei(D4, d4, rt=0.8, numero=True)
        self.resultado(D4, ACC)
        self.ate(0.99)

        # ── B6-5: o fantasma sai; ω × 4 e v_θ × 2 lado a lado no HUD; a reprise termina (hold) ──
        self.an("B6-5")
        self.pilha.limpa()
        self.fant_on = False
        self.loop = None
        self.anda(0.0, tf=self.tp + T45)
        mv = hud(r"v_\theta", lambda: est()["vth"], 2, "M/S", VEL, slot=2, ind="barra", faixa=(0.0, 3.0))
        Tm = vivo(t_viva(w=5, comp=0.9))
        vm = vivo(v_viva)
        self.play(OpVivo(mId, entra=False), FadeOut(marca), FadeOut(Tf), FadeOut(Vf), FadeOut(chip_i), FadeOut(chip_f), run_time=0.25)
        self.remove(mId)
        self.play(OpVivo(mv), OpVivo(Tm), OpVivo(vm), run_time=0.25)
        self.gat("a velocidade angular quadruplicou")
        self.anda(0.5)
        self.wait(1.4)
        E1, e1 = Mx(r"v_\theta", "=", r"\frac{L}{m r}", r"\ \Rightarrow\ ", r"\times 2")
        E2, e2 = Mx(r"\omega", "=", r"\frac{L}{m r^2}", r"\ \Rightarrow\ ", r"\times 4")
        self.pilha.poe(E1)
        self.gat("só dobrou")
        self.lei(E1, e1, {0: mv}, rt=1.2)
        self.pilha.poe(E2)
        self.gat("depende do inverso do raio ao quadrado")
        self.lei(E2, e2, {0: mw}, rt=1.2)
        self.play(pulso(gl(E2, J(e2, 4)), 1.2), pulso(gl(E1, J(e1, 4)), 1.2), run_time=0.8)
        self.ate(0.99)

        # ── B6-6: triângulos de 0,20 s varridos junto com o disco ao longo da espiral (0,090 m² cada) ──
        self.an("B6-6")
        self.pilha.limpa()
        self.play(FadeOut(fant), self.aneis_tr.animate.set_value(0.35), run_time=0.3)
        t0 = self.tp - 0.1
        self.anda(0.0, tf=t0)

        def tri_vivo(k):
            ta = t0 + 0.2 * k

            def f():
                t = min(self.tf(), ta + 0.2)
                if t <= ta + 1e-4:
                    return VGroup()
                if k < int((self.tf() - t0) / 0.2 + 1e-6) - 2:          # §3 #14: no máximo 3 triângulos visíveis (os mais velhos apagam)
                    return VGroup()
                pts = [self.tela((*self.mov(x), Z)) for x in np.linspace(ta, t, 14)]
                return area_lab([self.tela((0, 0, Z))] + pts, op=0.40 if k % 2 == 0 else 0.25)
            return vivo(f)
        tris = [tri_vivo(k) for k in range(6)]
        self.add(*tris)
        f_tri = linha_base([txt("TRIÂNGULOS DE", 30, bold=True, color=GEO), T(r"0{,}20\,\mathrm{s}", 40, WHITE_)], 0.14)
        self.pilha.poe(f_tri)
        self.play(FadeIn(f_tri), run_time=0.3)
        self.gat("e as áreas")
        self.anda(0.5, tf=t0)
        self.wait(2.5)
        self.anda(0.0)
        a_lbl = T(r"0{,}090\,\mathrm{m^2}", 40, WHITE_)
        fr = txt("CADA TRIÂNGULO:", 28, bold=True, color=GEO)
        linha_a = VGroup(fr, a_lbl).arrange(RIGHT, buff=0.25)
        self.pilha.poe(linha_a)
        self.gat("continuam iguais")
        self.play(FadeIn(linha_a), run_time=0.5)
        f6 = txt("MAIS BAIXO, MAIS LARGO", 30, bold=True, color=GEO)
        self.pilha.poe(f6)
        self.gat("tem que ficar mais largo")
        self.play(FadeIn(f6), run_time=0.5)
        self.ate(0.99)

        # ── B6-7: congela em r = 0,45 m; inset ZOOM ×3 no referencial da mesa ──
        self.an("B6-7")
        self.pilha.limpa()
        self.play(*[OpVivo(t, entra=False) for t in tris], run_time=0.4)
        self.remove(*tris)
        self.anda(0.0, tf=self.tp + T45)
        self.selo("ZOOM ×3", "PERTO DO DISCO")
        e = est()
        er, et = dirs()
        ur, ut = -er, et                      # para o furo; tangente (anti-horário) — mesmas direções da tela (vista de cima)
        Zc = P3(3.9, -0.35)
        k = 0.95
        p_vr = Zc + k * abs(e["vr"]) * ur * 2.2                 # v_r ampliada ×2,2 dentro do inset para ser lida (rótulo diz 0,30 m/s)
        p_vt = Zc + k * e["vth"] * ut
        p_v = p_vt + (p_vr - Zc)
        quadro = RoundedRectangle(width=6.0, height=5.0, corner_radius=0.12).move_to(P3(3.7, -0.35)).set_fill(PANEL, 0.72).set_stroke(GEO, 1.6)
        quadro._fundo = True
        disco_i = VGroup(Circle(radius=0.30).move_to(Zc).set_fill("#2A303B", 1).set_stroke(MAS, 4),
                         Dot(Zc, radius=0.05, color=WHITE_)).set_z_index(9)
        furo_dir = DashedLine(Zc + 0.35 * ur, Zc + 1.45 * ur, dash_length=0.08).set_stroke(GEO, 1.5, opacity=0.6)
        l_furo = VGroup()
        cham = Circle(radius=0.30).move_to(self.tela_disco()).set_stroke(WHITE_, 2.6).set_z_index(9)      # o disco marcado na mesa (sem linha de chamada pela calha)
        s_v = vetor_lab(Zc, p_v, VEL, w=7)
        l_v = T(r"\vec v", 42, VEL)
        self.gat("olha a velocidade durante a puxada")
        self.play(FadeIn(quadro), Create(cham), FadeIn(disco_i), FadeIn(furo_dir), FadeIn(l_furo), FadeIn(s_v), run_time=0.6)
        nv_ = np.array([-(p_v - Zc)[1], (p_v - Zc)[0], 0]); nv_ /= np.linalg.norm(nv_)
        if np.dot(nv_, ur) > 0:
            nv_ = -nv_
        l_v.move_to(P3(4.85, 1.55), aligned_edge=LEFT)          # legenda à direita do inset (sem colisão com as setas)               # v⃗ do lado de fora (longe do furo)
        self.play(FadeIn(l_v), run_time=0.3)
        self.gat("uma parte ao longo da volta")
        s_vt = vetor_lab(Zc, p_vt, VEL, w=5, origem=False)
        l_vt = T(r"v_\theta", 38, VEL)
        l_vt[0][1].set_color(ANG)                  # v5 COR OPERADOR: θ âmbar, v violeta
        l_vt.move_to(P3(4.85, 0.95), aligned_edge=LEFT)     # do lado do furo, oposto ao v⃗
        ret = VGroup(DashedLine(p_vt, p_v, dash_length=0.07), DashedLine(p_vr, p_v, dash_length=0.07)).set_stroke(VEL, 1.8, opacity=0.8)
        self.play(FadeIn(s_vt), FadeIn(l_vt), run_time=0.5)
        s_vr = vetor_lab(Zc, p_vr, VEL, w=5, origem=False, tip=0.16)
        l_vr = VGroup(T("v_r", 40, VEL), T(r"0{,}30\,\mathrm{m/s}", 36, VEL)).arrange(DOWN, buff=0.06, aligned_edge=LEFT).move_to(P3(4.85, 0.20), aligned_edge=LEFT)
        self.gat("uma parte apontando para o furo")
        self.play(FadeIn(s_vr), FadeIn(l_vr), Create(ret), run_time=0.5)
        ang = arco_ang(Zc, Zc + ut, p_v, r=1.7, cor=ANG, w=4)
        l_ang = T(r"8{,}5^\circ", 36, ANG).move_to(Zc + 1.75 * ut - 0.48 * ur)
        self.play(Create(ang), FadeIn(l_ang), run_time=0.5)
        self.gat("a tração também aponta para o furo")
        sT = vetor_lab(Zc - 0.20 * ut, Zc - 0.20 * ut + 1.6 * ur, FC, w=6)     # v5 #34: T⃗ nasce NO disco (lado oposto a v_θ), ao lado de v_r, que não fica escondido
        lT = T(r"\vec T", 40, FC).move_to(P3(4.85, -0.65), aligned_edge=LEFT)
        self.play(FadeIn(sT), FadeIn(lT), run_time=0.5)
        a0 = Arc(radius=0.35, start_angle=math.atan2(ur[1], ur[0]) - 0.25, angle=0.5, arc_center=Zc + 0.75 * ur - 0.10 * ut).set_stroke(ANG, 3)
        l0 = T(r"0^\circ", 36, ANG).next_to(a0, -ut, buff=0.25)
        self.gat("tem uma componente na direção do movimento")
        self.play(Create(a0), FadeIn(l0), Indicate(s_vr, color=FC, scale_factor=1.15), run_time=0.7)
        f7 = linha_base([txt("MESMO SENTIDO", 26, bold=True, color=CYAN), T(r"\Rightarrow", 34, WHITE_), T("W", 36, KC), T(r">0", 36, WHITE_)], 0.14)
        f7.move_to(P3(3.7, -2.6))
        self.gat("faz trabalho positivo")
        self.play(FadeIn(f7), run_time=0.4)
        self.ate(0.99)

        # ── B6-8: barras de energia (estados com v_r = 0); W = ΔK; P = T v_r (hold); a mesa sai ──
        self.an("B6-8")
        inset = [quadro, cham, disco_i, furo_dir, l_furo, s_v, l_v, s_vt, l_vt, ret, s_vr, l_vr, ang, l_ang, sT, lT, a0, l0, f7]
        self.play(*[FadeOut(m) for m in inset], f3.op.animate.set_value(0.0), *[OpVivo(m, entra=False) for m in (mr, mw, mv, Tm, vm)], run_time=0.5)
        print(f"[seta] TV off {self.clk.get_value() - 0.5:.3f}")
        self.remove(*inset, mr, mw, mv, Tm, vm)
        self.selo("ESTADOS COM", [[T(r"v_r", 36, VEL), txt("= 0", 28, bold=True, color=WHITE_)]])
        y0, esc = -2.45, 4.2                  # v5 G28: barras mais baixas (o rótulo de K_f saía da zona do esquema)
        b_K0 = Rectangle(width=0.9, height=0.225 * esc).set_fill(KC, 0.85).set_stroke(KC, 2).move_to(P3(-5.9, y0 + 0.225 * esc / 2))
        b_Kf = Rectangle(width=0.9, height=0.900 * esc).set_fill(KC, 0.85).set_stroke(KC, 2).move_to(P3(-3.4, y0 + 0.900 * esc / 2))
        b_W = Rectangle(width=0.9, height=0.675 * esc).set_fill(KC, 0.35).set_stroke(KC, 2.5).move_to(P3(-1.4, y0 + 0.225 * esc + 0.675 * esc / 2))
        base_l = Line(P3(-6.8, y0), P3(-0.6, y0)).set_stroke(GEO, 2)
        lK0 = VGroup(T("K_0", 36, KC), T(r"0{,}225\,\mathrm{J}", 36, WHITE_)).arrange(DOWN, buff=0.08).next_to(b_K0, UP, buff=0.15)
        lKf = VGroup(T("K_f", 36, KC), T(r"0{,}900\,\mathrm{J}", 36, WHITE_)).arrange(DOWN, buff=0.08).next_to(b_Kf, UP, buff=0.15)
        lW = VGroup(T("W", 36, KC), T(r"0{,}675\,\mathrm{J}", 36, WHITE_)).arrange(DOWN, buff=0.08).next_to(b_W, UP, buff=0.15)
        def mini_disco(cx, rr):           # §2.5: o anel da órbita sob a barra (0,60 m sob K₀, 0,30 m sob K_f), com furo e disco
            c = P3(cx, -3.17)
            return VGroup(Circle(radius=rr).move_to(c).set_stroke(GEO, 2.4), Dot(c, radius=0.05, color=WHITE_),
                          Dot(c + P3(rr * 0.7, rr * 0.7), radius=0.09, color=MAS)).set_z_index(8)
        md0, md1 = mini_disco(-5.9, 0.40), mini_disco(-3.4, 0.20)
        self.gat("a energia cinética vai de")
        self.play(Create(base_l), GrowFromEdge(b_K0, DOWN), FadeIn(lK0), FadeIn(md0), run_time=0.7)
        self.play(GrowFromEdge(b_Kf, DOWN), FadeIn(lKf), FadeIn(md1), run_time=0.7)
        # v13 SYNC: a conta de W = ΔK é distribuída pela fala (4 linhas não cabiam entre "quatro vezes mais" e "são o trabalho da mão")
        G1, g1 = Mx("W", "=", r"\Delta K")
        self.pilha.poe(G1)
        self.lei(G1, g1, rt=0.8, metodo="lei")
        G2, g2 = Mx("=", r"\tfrac{1}{2} m v_{\theta,f}^2", "-", r"\tfrac{1}{2} m v_{\theta,0}^2")
        self.pilha.poe(G2)
        self.gat("duzentos e vinte e cinco")
        self.lei(G2, g2, rt=1.3, metodo="lei")
        G2b, g2b = Mx("=", r"\tfrac{1}{2}", r"0{,}20", r"\cdot 3{,}0^2", "-", r"\tfrac{1}{2}", r"0{,}20", r"\cdot 1{,}5^2", cores={2: MAS, 3: VEL, 6: MAS, 7: VEL})
        self.pilha.poe(G2b)
        if G2b.get_right()[0] > 7.05:                      # exceção registrada no relatório: só esta linha encolhe (~7 %) para caber na zona da CONTA
            G2b.scale((7.05 - G2b.get_left()[0]) / G2b.width, about_point=G2b.get_left())
        self.gat("novecentos joule")
        self.lei(G2b, g2b, rt=1.3, numero=True)
        G3, g3 = Mx("=", r"0{,}900", "-", r"0{,}225", cores={1: KC, 3: KC})
        self.pilha.poe(G3)
        self.gat("comparando os dois estados")
        self.lei(G3, g3, {1: lKf[1], 3: lK0[1]}, rt=1.2, numero=True)
        G4, g4 = Mx("W", "=", r"0{,}675", r"\,\mathrm{J}", cores={2: KC})
        self.pilha.poe(G4)
        self.gat("são o trabalho da mão")
        self.lei(G4, g4, rt=0.8, numero=True)
        self.play(GrowFromEdge(b_W, DOWN), FadeIn(lW), run_time=0.7)
        self.resultado(G4, KC)
        self.pilha.so(G4)
        G5, g5 = Mx("P", "=", "T", "v_r")
        self.pilha.poe(G5)
        self.lei(G5, g5, rt=0.8, metodo="lei")
        G6, g6 = Mx("=", r"1{,}78", r"\cdot", r"0{,}30", "=", r"0{,}53", r"\,\mathrm{W}", cores={1: FC, 3: VEL, 5: KC})
        self.pilha.poe(G6)
        self.lei(G6, g6, rt=1.2, numero=True)
        self.gat("se conservou")
        f8 = linha_base([T("L", 40, LMAG), txt("CONSERVA,", 30, bold=True), T("K", 40, KC), txt("NÃO", 30, bold=True)], 0.14)
        self.pilha.so(G4, G5, G6)
        self.pilha.poe(f8)
        self.play(FadeIn(f8), run_time=0.5)
        # v13 §2.3.5: duas leis com condições diferentes (fica 3 s e sai antes do B6-9)
        crt_L = cartao_ideia([T("L", 40, LMAG), txt(": SEM TORQUE", 26, bold=True), T(r"\Rightarrow", 34, WHITE_), txt("CONSTANTE", 26, bold=True, color=LMAG)], LMAG)
        crt_K = cartao_ideia([T("K", 40, KC), txt(": HÁ TRABALHO", 26, bold=True), T(r"\Rightarrow", 34, WHITE_), txt("AUMENTA", 26, bold=True, color=KC)], KC)
        crts = VGroup(crt_L, crt_K).arrange(DOWN, buff=0.22, aligned_edge=LEFT).move_to(P3(3.7, -2.45))
        self.gat("duas leis com condições diferentes")
        self.play(FadeIn(crts, shift=0.06 * UP), run_time=0.5)
        self.wait(2.5)
        self.play(FadeOut(crts), run_time=0.4)
        self.remove(crts)
        self.ate(0.99)

        # ── B6-9: ATENÇÃO; a mesa volta com a reprise; gráfico T × r (grafico_lab) com o ponto vivo correndo a curva ──
        self.an("B6-9")
        self.pilha.limpa()
        self.anda(0.0, tf=self.tp - 0.2)
        self.play(FadeOut(VGroup(b_K0, b_Kf, b_W, base_l, lK0, lKf, lW, md0, md1)), f3.op.animate.set_value(1.0), run_time=0.5)
        self.selo("ATENÇÃO", "SEM ACELERAÇÃO RADIAL")
        H1, h1 = Mx("T", "=", r"\frac{L^2}{m r^3}")
        self.pilha.poe(H1)
        graf, c2p = grafico_lab(1.55, -2.85, 4.6, 2.8, (0.25, 0.65), (0.0, 6.6), [0.30, 0.45, 0.60], [0.75, 6.0],
                                T("r", 36, VETC), T("T", 36, FC), rotx=[r"0{,}30", r"0{,}45", r"0{,}60"], roty=[r"0{,}75", r"6{,}0"])
        self.play(FadeIn(graf), run_time=0.5)
        self.gat("cada vez mais difícil puxar")
        curva = curva_lab(c2p, F.tracao_rdd0, 0.30, 0.60, FC)
        self.play(Create(curva), run_time=1.0)

        def pv():
            r = min(F.R0, max(F.R1, est()["r"]))
            return ponto_vivo(c2p(r, F.tracao_rdd0(r)), FC)
        ponto = vivo(pv)
        self.add(ponto)
        self.gat("com o inverso do cubo do raio")
        self.lei(H1, h1, rt=1.0, metodo="lei")
        self.gat("de zero vírgula setenta e cinco")
        self.anda(0.5)
        self.wait(0.6)                                  # v5: cortes para caber na âncora (a escrita sequencial passou a gastar mais tempo)
        self.anda(0.0)
        self.play(Indicate(curva, color=FC, scale_factor=1.0), run_time=0.6)
        self.ate(0.995)

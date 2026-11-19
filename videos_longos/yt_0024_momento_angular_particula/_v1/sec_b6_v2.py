"""Lote PB6 v2: B6 — DE VOLTA À MESA (Three.js 'mesa_furo' v2: C_34 → C_TOPO; reprise da puxada em CÂMERA LENTA ×0,5).
HUD (no máximo 3, à direita da mesa, fora da CONTA): r (barra 0…0,60 m), ω (arco 0…10 rad/s) e L (cadeado) → İ (B6-4) → v_θ (B6-5…7).
Setas NA MESA durante a reprise (v2 §3.2): T⃗ (azul, para o furo) e v⃗ (violeta), presas ao disco do B6-2 ao B6-7. Os anéis de 0,60 e 0,30 m
da grade acendem e o raio antigo fica como fantasma até o fim do B6-5. τ = dL/dt com I variável: τ_z = I α + İ ω (r = 0,45 m: I = 0,0405,
ω = 4,44, İ = −0,054 ⇒ α = +5,9 rad/s²). Triângulos de 0,20 s varridos junto com o disco (0,090 m² cada). B6-7: inset ZOOM ×3 no MESMO
referencial da mesa (sem girar): v⃗ = v_r + v_θ com o retângulo da decomposição, T⃗ paralela a v_r e no mesmo sentido ⇒ W > 0, 8,5° entre v⃗
e a tangente. B6-8: barras de energia (a mesa sai). B6-9: a mesa volta com a reprise e o gráfico T × r (grafico_lab) com o ponto vivo."""
from pecas24 import *  # noqa: F401,F403

T45 = F.TR + (F.R0 - F.VR * F.TR / 2 - 0.45) / F.VR       # tempo da puxada em que r = 0,45 m (fase de v_r constante)


class LoteB6(Lote24):
    def estado3d(self, _t=0.0):
        e = super().estado3d(_t)
        k = float(self.aneis_tr.get_value())
        if k > 0:
            e["aneis"] = {"r30": round(k, 3), "r60": round(k, 3)}
        return e

    def corpo(self):
        self.camA = self.camB = C34
        self.mov = mov_puxada(self)
        self.zp = zp_puxada(self)
        self.aneis_tr = ValueTracker(0.0)
        self.add(self.aneis_tr)
        self.anda(1.0, tf=0.0)
        f3 = self.mesa()
        f3.op.set_value(1.0)
        self.canto("DE VOLTA À MESA")
        Z = 0.012

        def est():
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
                return VGroup(vetor_lab(a + 0.22 * u, a + (0.22 + 0.8 * comp) * u, FC, w=w, origem=False), T(r"\vec T", 38, FC).move_to(a + 0.62 * u - 0.40 * n))
            return f

        def v_viva():
            e = est()
            er, et = dirs()
            v = e["vr"] * er + e["vth"] * et
            a, b = self.tela(pD()), self.tela(pD() + 0.10 * v)        # 0,10 m por m/s (v até 3,0 m/s cabe na mesa)
            u = (b - a) / max(np.linalg.norm(b - a), 1e-6)
            return VGroup(vetor_lab(a + 0.2 * u, b, VEL, w=6, origem=False), T(r"\vec v", 38, VEL).move_to(b + 0.35 * u))

        # ── B6-1: C_34, órbita de 0,60 m; hipóteses em chips; tração central ⇒ L constante ──
        self.an("B6-1")
        self.transicao(0.5)
        self.gat("de volta à mesa")
        hip = chips(["SEM ATRITO", "FIO IDEAL", "DISCO PEQUENO"]).move_to(P3(3.75, 3.02))
        hip._chip = True
        self.play(LaggedStart(*[FadeIn(c, shift=0.06 * DOWN) for c in hip], lag_ratio=0.3), run_time=0.8)
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
        self.dolly(CTOPO, 1.6)
        self.selo("CÂMERA LENTA", "×0,5")
        mr = hud("r", lambda: est()["r"], 2, "M", VETC, slot=0, ind="barra", faixa=(0.0, 0.60))
        mw = hud(r"\omega", lambda: est()["w"], 2, "RAD/S", VEL, slot=1, ind="arco", faixa=(0.0, 10.0))
        mL = hud("L", lambda: est()["L"], 3, "KG·M²/S", LMAG, slot=2, trava=lambda: True)
        Tm = vivo(t_viva(w=5, comp=0.9))
        vm = vivo(v_viva)
        self.play(OpVivo(mr), OpVivo(mw), OpVivo(mL), OpVivo(Tm), OpVivo(vm), self.aneis_tr.animate.set_value(1.0), run_time=0.6)
        print(f"[seta] TV on {self.clk.get_value():.3f}")
        B1, b1 = Mx("L", "=", "I", r"\omega")
        self.pilha.poe(B1)
        self.gat("no disco")
        self.lei(B1, b1, rt=0.9, metodo="lei")
        B2, b2 = Mx("I", "=", "m", "r^2")
        self.pilha.poe(B2)
        self.lei(B2, b2, rt=0.8, metodo="lei")
        self.gat("quando o raio cai pela metade")
        self.anda(0.5)
        self.tp = self.tf() + 0.15
        # raio antigo como fantasma (r⃗ a 40 %, contorno 1,0) até o fim do B6-5
        th_p = F.W0 * self.tp
        fant = VGroup(Line(self.tela((0, 0, Z)), self.tela((F.R0 * math.cos(th_p), F.R0 * math.sin(th_p), Z))).set_stroke(VETC, 5, opacity=0.4),
                      Line(self.tela((0, 0, Z)), self.tela((F.R0 * math.cos(th_p), F.R0 * math.sin(th_p), Z))).set_stroke(VETC, 1.0, opacity=0.9))
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

        # ── B6-3: congela em r = 0,45 m; τ⃗ = dL⃗/dt (LEI GERAL acima dela) → … → I α + İ ω (hold) ──
        self.an("B6-3")
        self.anda(0.0, tf=self.tp + T45)
        self.sem_selo()
        self.pilha.limpa()
        marca = Circle(radius=0.30).set_stroke(WHITE_, 2.6).set_z_index(9)
        marca.move_to(self.tela_disco())
        self.play(Create(marca), run_time=0.4)
        C1, c1 = Mx(r"\vec\tau", "=", r"\frac{d\vec L}{dt}")
        self.pilha.topo = 2.0
        self.pilha.poe(C1)
        self.gat("a lei geral")
        self.lei(C1, c1, rt=1.0, metodo="lei")
        lg = txt("LEI GERAL", 24, bold=True, color=GEO).next_to(C1, UP, buff=0.14, aligned_edge=LEFT)     # caso 26: acima da linha, só nela
        self.play(FadeIn(lg), run_time=0.3)
        C2, c2 = Mx(r"\tau_z", "=", r"\frac{d(I\omega)}{dt}")
        self.pilha.poe(C2)
        self.gat("derivando o momento de inércia")
        self.gm(C1, C2, (J(c1, 0), J(c2, 0)), (J(c1, 1), J(c2, 1)), (J(c1, 2)[0:1], J(c2, 2)[0:1]), (J(c1, 2)[1:3], J(c2, 2)[1:5]), (J(c1, 2)[3:], J(c2, 2)[5:]), rt=1.3)
        C3, c3 = Mx(r"\tau_z", "=", "I", r"\frac{d\omega}{dt}", "+", r"\frac{dI}{dt}", r"\omega")
        self.pilha.poe(C3)
        self.gat("a regra do produto")
        # caso 27: GM numa chamada só da linha inteira (todos os termos novos nascem de glifos da linha de cima)
        self.gm(C2, C3, (J(c2, 0), J(c3, 0)), (J(c2, 1), J(c3, 1)), (J(c2, 2)[2:3], J(c3, 2)), (J(c2, 2)[3:4], J(c3, 3)[1:2]), (J(c2, 2)[0:1], J(c3, 3)[0:1]),
                (J(c2, 2)[5:], J(c3, 3)[2:]), (J(c2, 2)[1:2] + J(c2, 2)[4:5], J(c3, 4)), ([], J(c3, 5, 6)), rt=1.8)
        C4, c4 = Mx(r"\tau_z", "=", "I", r"\alpha", "+", r"\dot I", r"\omega")
        self.pilha.poe(C4)
        self.gat("mais a taxa de variação")
        self.gm(C3, C4, (J(c3, 0), J(c4, 0)), (J(c3, 1), J(c4, 1)), (J(c3, 2), J(c4, 2)), (J(c3, 3), J(c4, 3)), (J(c3, 4), J(c4, 4)), (J(c3, 5), J(c4, 5)),
                (J(c3, 6), J(c4, 6)), rt=1.4)
        self.resultado(C4, FC)
        self.gat("a versão curta")
        Cc, cc = Mx(r"\tau_z", "=", "I", r"\alpha")
        self.pilha.so(C1, C4)
        self.pilha.poe(Cc)
        self.lei(Cc, cc, rt=0.6, metodo="escrita")
        self.texto_na_linha(Cc, "SÓ COM I CONSTANTE", MAS, size=26)
        self.gat("aqui não é")
        self.play(Indicate(gl(C4, J(c4, 5, 6)), color=MAS, scale_factor=1.2), run_time=0.8)
        self.ate(0.99)

        # ── B6-4: 0 = I α + İ ω → I α = −İ ω → números em r = 0,45 m → α = +5,9 rad/s² ──
        self.an("B6-4")
        self.play(FadeOut(lg), run_time=0.2)
        self.pilha.topo = 2.35
        self.pilha.so(C4)
        D1, d1 = Mx("0", "=", "I", r"\alpha", "+", r"\dot I", r"\omega")
        self.pilha.poe(D1)
        self.gat("com torque zero")
        self.gm(C4, D1, (J(c4, 0), J(d1, 0)), (J(c4, 1), J(d1, 1)), (J(c4, 2), J(d1, 2)), (J(c4, 3), J(d1, 3)), (J(c4, 4), J(d1, 4)), (J(c4, 5), J(d1, 5)),
                (J(c4, 6), J(d1, 6)), rt=1.2)
        D2, d2 = Mx("I", r"\alpha", "=", "-", r"\dot I", r"\omega")
        self.pilha.poe(D2)
        self.gat("tem que cancelar a segunda")
        self.gm(D1, D2, (J(d1, 2), J(d2, 0)), (J(d1, 3), J(d2, 1)), (J(d1, 1), J(d2, 2)), (J(d1, 4), J(d2, 3)), (J(d1, 5), J(d2, 4)), (J(d1, 6), J(d2, 5)),
                (J(d1, 0), []), rt=1.4)
        mId = hud(r"\dot I", lambda: est()["Idot"], 3, "KG·M²/S", MAS, slot=2)
        self.play(OpVivo(mL, entra=False), run_time=0.25)
        self.remove(mL)
        self.play(OpVivo(mId), run_time=0.25)
        D3, d3 = Mx(r"\alpha", "=", r"\frac{-(-0{,}054)\cdot 4{,}44}{0{,}0405}")
        self.pilha.so(D2)
        self.pilha.poe(D3)
        self.gat("a quarenta e cinco centímetros")
        self.lei(D3, d3, {2: mId}, rt=1.4, numero=True)
        D4, d4 = Mx("=", r"+5{,}9", r"\,\mathrm{rad/s^2}", cores={1: ACC})
        self.pilha.poe(D4)
        self.gat("quase seis radianos")
        self.lei(D4, d4, rt=0.8, numero=True)
        self.resultado(D4, ACC)
        self.ate(0.99)

        # ── B6-5: ω × 4 e v_θ × 2 lado a lado no HUD; a reprise termina (hold) ──
        self.an("B6-5")
        self.pilha.limpa()
        mv = hud(r"v_\theta", lambda: est()["vth"], 2, "M/S", VEL, slot=2, ind="barra", faixa=(0.0, 3.0))
        self.play(OpVivo(mId, entra=False), FadeOut(marca), run_time=0.25)
        self.remove(mId)
        self.play(OpVivo(mv), run_time=0.25)
        self.gat("a velocidade angular quadruplicou")
        self.anda(0.5)
        self.wait(1.4)
        E1, e1 = Mx(r"v_\theta", "=", r"\frac{L}{m r}", r"\ \Rightarrow\ ", r"\times 2")
        E2, e2 = Mx(r"\omega", "=", r"\frac{L}{m r^2}", r"\ \Rightarrow\ ", r"\times 4")
        self.pilha.poe(E1)
        self.gat("só dobrou")
        self.lei(E1, e1, {0: mv}, rt=1.2)
        self.pilha.poe(E2)
        self.gat("depende do raio ao quadrado")
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
        furo_dir = DashedLine(Zc + 0.35 * ur, Zc + 2.4 * ur, dash_length=0.08).set_stroke(GEO, 1.5, opacity=0.6)
        l_furo = VGroup()
        cham = Circle(radius=0.30).move_to(self.tela_disco()).set_stroke(WHITE_, 2.6).set_z_index(9)      # o disco marcado na mesa (sem linha de chamada pela calha)
        s_v = vetor_lab(Zc, p_v, VEL, w=7)
        l_v = T(r"\vec v", 42, VEL)
        self.gat("olha a velocidade durante a puxada")
        self.play(FadeIn(quadro), Create(cham), FadeIn(disco_i), FadeIn(furo_dir), FadeIn(l_furo), FadeIn(s_v), run_time=0.6)
        nv_ = np.array([-(p_v - Zc)[1], (p_v - Zc)[0], 0]); nv_ /= np.linalg.norm(nv_)
        if np.dot(nv_, ur) > 0:
            nv_ = -nv_
        l_v.move_to(Zc + 0.65 * (p_v - Zc) + 0.42 * nv_)               # v⃗ do lado de fora (longe do furo)
        self.play(FadeIn(l_v), run_time=0.3)
        self.gat("uma parte ao longo da volta")
        s_vt = vetor_lab(Zc, p_vt, VEL, w=5, origem=False)
        l_vt = T(r"v_\theta", 38, VEL).move_to(Zc + 0.55 * (p_vt - Zc) - 0.40 * ur)     # do lado do furo, oposto ao v⃗
        ret = VGroup(DashedLine(p_vt, p_v, dash_length=0.07), DashedLine(p_vr, p_v, dash_length=0.07)).set_stroke(VEL, 1.8, opacity=0.8)
        self.play(FadeIn(s_vt), FadeIn(l_vt), run_time=0.5)
        s_vr = vetor_lab(Zc, p_vr, VEL, w=5, origem=False, tip=0.16)
        l_vr = VGroup(T("v_r", 40, VEL), T(r"0{,}30\,\mathrm{m/s}", 36, VEL)).arrange(DOWN, buff=0.06, aligned_edge=LEFT).next_to(p_vr, -ut, buff=0.18)
        self.gat("uma parte apontando para o furo")
        self.play(FadeIn(s_vr), FadeIn(l_vr), Create(ret), run_time=0.5)
        ang = arco_ang(Zc, Zc + ut, p_v, r=1.7, cor=ANG, w=4)
        l_ang = T(r"8{,}5^\circ", 36, ANG).move_to(Zc + 1.75 * ut - 0.48 * ur)
        self.play(Create(ang), FadeIn(l_ang), run_time=0.5)
        self.gat("a tração também aponta para o furo")
        sT = vetor_lab(Zc + 0.36 * ur - 0.42 * ut, Zc + 1.6 * ur - 0.42 * ut, FC, w=6)
        lT = T(r"\vec T", 40, FC).next_to(Zc + 1.0 * ur - 0.42 * ut, -ut, buff=0.18)
        self.play(FadeIn(sT), FadeIn(lT), run_time=0.5)
        a0 = Arc(radius=0.35, start_angle=math.atan2(ur[1], ur[0]) - 0.25, angle=0.5, arc_center=Zc + 0.75 * ur - 0.21 * ut).set_stroke(ANG, 3)
        l0 = T(r"0^\circ", 36, ANG).next_to(a0, ur, buff=0.2)
        self.gat("tem uma componente na direção do movimento")
        self.play(Create(a0), FadeIn(l0), Indicate(s_vr, color=FC, scale_factor=1.15), run_time=0.7)
        f7 = linha_base([txt("MESMO SENTIDO", 26, bold=True, color=CYAN), T(r"\Rightarrow", 34, WHITE_), T("W", 36, KC), T(r">0", 36, WHITE_)], 0.14)
        f7.move_to(P3(3.7, -2.45))
        self.gat("faz trabalho positivo")
        self.play(FadeIn(f7), run_time=0.4)
        self.ate(0.99)

        # ── B6-8: barras de energia (estados com v_r = 0); W = ΔK; P = T v_r (hold); a mesa sai ──
        self.an("B6-8")
        inset = [quadro, cham, disco_i, furo_dir, l_furo, s_v, l_v, s_vt, l_vt, ret, s_vr, l_vr, ang, l_ang, sT, lT, a0, l0, f7]
        self.play(*[FadeOut(m) for m in inset], f3.op.animate.set_value(0.0), *[OpVivo(m, entra=False) for m in (mr, mw, mv, Tm, vm)], run_time=0.5)
        print(f"[seta] TV off {self.clk.get_value() - 0.5:.3f}")
        self.remove(*inset, mr, mw, mv, Tm, vm)
        self.selo("ESTADOS COM", "VELOCIDADE RADIAL NULA")
        y0, esc = -3.0, 4.6
        b_K0 = Rectangle(width=0.9, height=0.225 * esc).set_fill(KC, 0.85).set_stroke(KC, 2).move_to(P3(-5.9, y0 + 0.225 * esc / 2))
        b_Kf = Rectangle(width=0.9, height=0.900 * esc).set_fill(KC, 0.85).set_stroke(KC, 2).move_to(P3(-3.4, y0 + 0.900 * esc / 2))
        b_W = Rectangle(width=0.9, height=0.675 * esc).set_fill(KC, 0.35).set_stroke(KC, 2.5).move_to(P3(-1.4, y0 + 0.225 * esc + 0.675 * esc / 2))
        base_l = Line(P3(-6.8, y0), P3(-0.6, y0)).set_stroke(GEO, 2)
        lK0 = VGroup(T("K_0", 36, KC), T(r"0{,}225\,\mathrm{J}", 36, WHITE_)).arrange(DOWN, buff=0.08).next_to(b_K0, UP, buff=0.15)
        lKf = VGroup(T("K_f", 36, KC), T(r"0{,}900\,\mathrm{J}", 36, WHITE_)).arrange(DOWN, buff=0.08).next_to(b_Kf, UP, buff=0.15)
        lW = VGroup(T("W", 36, KC), T(r"0{,}675\,\mathrm{J}", 36, WHITE_)).arrange(DOWN, buff=0.08).next_to(b_W, UP, buff=0.15)
        self.gat("a energia cinética vai de")
        self.play(Create(base_l), GrowFromEdge(b_K0, DOWN), FadeIn(lK0), run_time=0.7)
        self.play(GrowFromEdge(b_Kf, DOWN), FadeIn(lKf), run_time=0.7)
        self.gat("quatro vezes mais")
        G1, g1 = Mx("W", "=", r"\Delta K")
        self.pilha.poe(G1)
        self.lei(G1, g1, rt=0.8, metodo="lei")
        G2, g2 = Mx(r"\Delta K", "=", r"\tfrac{1}{2} m v_{\theta,f}^2", "-", r"\tfrac{1}{2} m v_{\theta,0}^2")
        self.pilha.poe(G2)
        self.lei(G2, g2, rt=1.3, metodo="lei")
        G3, g3 = Mx("=", r"0{,}900", "-", r"0{,}225", cores={1: KC, 3: KC})
        self.pilha.poe(G3)
        self.lei(G3, g3, {1: lKf[1], 3: lK0[1]}, rt=1.2, numero=True)
        G4, g4 = Mx("W", "=", r"0{,}675", r"\,\mathrm{J}", cores={2: KC})
        self.pilha.poe(G4)
        self.gat("são o trabalho da mão")
        self.lei(G4, g4, rt=0.8, numero=True)
        self.play(GrowFromEdge(b_W, DOWN), FadeIn(lW), run_time=0.7)
        self.resultado(G4, KC)
        self.pilha.so(G1, G4)
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
        self.ate(0.99)

        # ── B6-9: ATENÇÃO; a mesa volta com a reprise; gráfico T × r (grafico_lab) com o ponto vivo correndo a curva ──
        self.an("B6-9")
        self.pilha.limpa()
        self.anda(0.0, tf=self.tp - 0.2)
        self.play(FadeOut(VGroup(b_K0, b_Kf, b_W, base_l, lK0, lKf, lW)), f3.op.animate.set_value(1.0), run_time=0.5)
        self.selo("ATENÇÃO", "PUXADA SEM ACELERAÇÃO RADIAL")
        H1, h1 = Mx("T", "=", r"\frac{L^2}{m r^3}")
        self.pilha.poe(H1)
        graf, c2p = grafico_lab(1.55, -2.7, 4.6, 3.1, (0.25, 0.65), (0.0, 6.6), [0.30, 0.45, 0.60], [0.75, 6.0],
                                T("r", 36, VETC), T("T", 36, FC), rotx=[r"0{,}30", r"0{,}45", r"0{,}60"], roty=[r"0{,}75", r"6{,}0"])
        self.play(FadeIn(graf), run_time=0.5)
        self.gat("cada vez mais difícil puxar")
        curva = curva_lab(c2p, F.tracao_rdd0, 0.30, 0.60, FC)
        self.play(Create(curva), run_time=1.4)

        def pv():
            r = min(F.R0, max(F.R1, est()["r"]))
            return ponto_vivo(c2p(r, F.tracao_rdd0(r)), FC)
        ponto = vivo(pv)
        self.add(ponto)
        self.gat("com o inverso do cubo do raio")
        self.lei(H1, h1, rt=1.0, metodo="lei")
        self.gat("de zero vírgula setenta e cinco")
        self.anda(0.5)
        self.wait(2.6)
        self.anda(0.0)
        self.play(Indicate(curva, color=FC, scale_factor=1.0), run_time=0.8)
        self.ate(0.995)

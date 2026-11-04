"""Lote PT3: T3 — A SEGUNDA LEI DE NEWTON DA ROTAÇÃO.
O DiscoPedacos 2,5D (4 anéis × 10 setores) permanece na metade esquerda de T3-1 até T3-6 (regra UM OBJETO).
T3-1: pedaço i destacado a distância r_i do eixo; aceleração angular α.
T3-2: a_{t,i} = r_i α e F_{t,i} = m_i a_{t,i} = m_i r_i α (F_{r,i} aponta para o eixo → não faz torque).
T3-3: multiplica por r_i dos dois lados via TransformByGlyphMap (passo): r_i F_{t,i} = m_i r_i² α ⇒ τ_i = m_i r_i² α, destacando m_i r_i² em rosa.
T3-4: soma em todos os pedaços: Σ τ_i = Σ m_i r_i² α, separando Σ τ_i = Σ τ_ext + Σ τ_int.
T3-5: par A–B no disco com F⃗_{AB} = −F⃗_{BA} colineares e mesmo braço r_⊥: τ_{AB} + τ_{BA} = 0; varredura dos pares internos → Σ τ_int = 0.
T3-6: α sai da soma e Σ m_i r_i² vira I_z → caixa PANEL Σ τ_{ext,z} = I_z α + tabela de tradução F ↔ τ, m ↔ I, a ↔ α, ΣF=ma ↔ Στ=Iα.
T3-7: três painéis de validade: (1) eixo fixo ✓, (2) roda rolando pelo CM ✓ (MOVIMENTO PLANO), (3) pião inclinado ✗ (PRECISA DE MOMENTO ANGULAR)."""
from pecas22 import *  # noqa: F401,F403

C_D3, R_D3 = P3(-3.75, -0.45), 2.2
NR3, NT3 = 4, 10
K_I = 3 * NT3 + 1
K_A = 2 * NT3 + 3
K_B = 3 * NT3 + 8


class LoteT3(Lote22):
    def corpo(self):
        self.an("T3-1")
        self.secao("2ª LEI DE NEWTON DA ROTAÇÃO")
        ang = ValueTracker(0.0)
        gira = ValueTracker(0.25)
        ang.add_updater(lambda m, dt: m.increment_value(gira.get_value() * dt))
        fi = lambda: ang.get_value()

        ref = DiscoPedacos(C_D3, R_D3, NR3, NT3)
        dados = ref.dados
        realce_i = ValueTracker(0.0)
        realce_ab = ValueTracker(0.0)
        varre_pares = ValueTracker(0.0)
        self.add(ang, gira, realce_i, realce_ab, varre_pares)

        PARK = 0.35

        def pos(k, extra=0.0, r=None):
            d = dados[k]
            a = d["a"] + fi() + extra
            rr = d["r"] if r is None else r
            return C_D3 + rr * np.array([math.cos(a), math.sin(a), 0.0])

        PARES_INT = [(2 * NT3 + k, 3 * NT3 + ((k + 3) % NT3)) for k in range(NT3)]

        def _disco():
            g = DiscoPedacos(C_D3, R_D3, NR3, NT3)
            g.rotate(fi(), about_point=C_D3)
            oi = realce_i.get_value()
            if oi > 0.01:
                g.pec[K_I].set_fill(mix(MAS, 0.25), 0.55 + 0.40 * oi).set_stroke(WHITE_, 3.0, opacity=oi)
            oab = realce_ab.get_value()
            if oab > 0.01:
                for kk in (K_A, K_B):
                    g.pec[kk].set_fill(mix(MAS, 0.28), 0.60 + 0.35 * oab).set_stroke(WHITE_, 2.8, opacity=oab)
            vp = varre_pares.get_value()
            if vp > 0.01:
                for idx_p, (ka, kb) in enumerate(PARES_INT):
                    w_p = math.sin(math.pi * min(1.0, max(0.0, vp * 1.4 - idx_p * 0.04)))
                    if w_p > 0.02:
                        pa, pb = pos(ka), pos(kb)
                        g.add(Line(pa, pb).set_stroke(FC, 2.6, opacity=0.85 * w_p).set_z_index(14))
                        g.add(Dot(pa, radius=0.055, color=WHITE_).set_opacity(w_p).set_z_index(15))
                        g.add(Dot(pb, radius=0.055, color=WHITE_).set_opacity(w_p).set_z_index(15))
            g.add(eixo_cruz(C_D3, 0.17))
            return g

        dv = vivo(_disco)
        self.play(FadeIn(dv), run_time=0.6)
        a_alp = seta_curva(C_D3, R_D3 + 0.36, 1.85, 0.85, ACC, 6)
        l_alp = T(r"\alpha", 44, ACC).next_to(C_D3 + (R_D3 + 0.36) * np.array([math.cos(2.3), math.sin(2.3), 0.0]), UL, buff=0.26)
        self.play(FadeIn(a_alp), FadeIn(l_alp), run_time=0.5)
        self.hip("CORPO RÍGIDO · EIXO FIXO")
        A0 = VGroup(
            txt("CORPO RÍGIDO COM EIXO FIXO:", 24, bold=True, color=GEO),
            VGroup(T(r"\omega,\ \alpha", 46), txt("IGUAIS EM TODOS OS PEDAÇOS", 24, bold=True)).arrange(RIGHT, buff=0.16),
        ).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
        self.pilha.poe(A0)
        self.play(FadeIn(A0, shift=0.1 * UP), run_time=0.6)

        self.gat("hipóteses ditas uma vez")
        gira.set_value(0.0)
        alvo = ang.get_value() + ((PARK - dados[K_I]["a"] - ang.get_value()) % (2 * PI))
        self.play(ang.animate(rate_func=rate_functions.ease_out_sine).set_value(alvo), realce_i.animate.set_value(1.0), run_time=1.4)

        p_i = pos(K_I)
        a_i = dados[K_I]["a"] + fi()
        u_rad = np.array([math.cos(a_i), math.sin(a_i), 0.0])
        u_tan = np.array([-math.sin(a_i), math.cos(a_i), 0.0])

        lin_ri = DashedLine(C_D3, p_i, dash_length=0.08).set_stroke(GEO, 3.0).set_z_index(13)
        l_mi = T("m_i", 40, MAS).move_to(p_i + u_rad * 0.56 + DOWN * 0.24)
        l_ri = T("r_i", 40, GEO).move_to((C_D3 + p_i) / 2 + u_tan * 0.36)
        self.play(Create(lin_ri), FadeIn(l_mi), FadeIn(l_ri), run_time=0.7)

        self.gat("ao longo desse eixo")
        self.play(a_alp.animate.scale(1.12), l_alp.animate.scale(1.18), rate_func=there_and_back, run_time=0.8)
        self.foco = dv
        self.ate(0.99)

        # ── T3-2: a_{t,i} = r_i α e F_{t,i} = m_i a_{t,i} = m_i r_i α ──
        self.an("T3-2")
        self.sem_selo()
        self.pilha.limpa()
        s_at = seta(p_i, p_i + u_tan * 1.15, ACC, 5, tip=0.18)
        l_at = T("a_{t,i}", 38, ACC).next_to(p_i + u_tan * 1.15, UP, buff=0.14)
        A1, ia1 = M("a_{t,i}", "=", "r_i", r"\alpha", size=50)
        self.pilha.poe(A1)
        self.play(FadeOut(A0), FadeIn(s_at), FadeIn(l_at), run_time=0.6)
        self.monta(A1, ia1, {0: l_at, 2: l_ri, 3: l_alp}, rt=1.0)
        self.gat("distância ao eixo vezes a aceleração angular")

        # Força radial F_{r,i} apontando para o eixo (apagada logo em seguida: não produz torque) e força tangencial F_{t,i}
        s_fr = seta(p_i, p_i - u_rad * 0.85, GEO, 4, tip=0.16, op=0.65)
        l_fr = T("F_{r,i}", 32, GEO).next_to(s_fr, DOWN, buff=0.08)
        s_ft = seta(p_i, p_i + u_tan * 1.35, FC, 6, tip=0.20)
        l_ft = T("F_{t,i}", 40, FC).next_to(p_i + u_tan * 1.35, UR, buff=0.08)

        self.gat("aplica newton nesse pedaço")
        self.play(FadeIn(s_fr), FadeIn(l_fr), run_time=0.6)
        self.gat("força tangencial sobre ele")
        self.play(FadeOut(s_fr), FadeOut(l_fr), FadeOut(s_at), FadeOut(l_at), FadeIn(s_ft), FadeIn(l_ft), run_time=0.7)

        A2, ia2 = M("F_{t,i}", "=", "m_i", "a_{t,i}", size=50)
        self.pilha.poe(A2)
        self.gat("massa vezes a aceleração tangencial")
        self.monta(A2, ia2, {0: l_ft, 2: l_mi, 3: mp(A1, ia1, [0])}, rt=1.0)

        A3, ia3 = M("F_{t,i}", "=", "m_i", "r_i", r"\alpha", size=50)
        self.pilha.poe(A3)
        self.gat("massa vezes distância vezes aceleração angular")
        self.passo(
            A2, A3,
            (J(ia2, 0), J(ia3, 0)),
            (J(ia2, 1), J(ia3, 1)),
            (J(ia2, 2), J(ia3, 2)),
            (J(ia2, 3), J(ia3, 3, 4)),
            rt=1.1,
            origem=False,
        )
        self.foco = A3
        self.ate(0.99)

        # ── T3-3: multiplica por r_i dos dois lados (TransformByGlyphMap) → τ_i = m_i r_i² α ──
        self.an("T3-3")
        self.pilha.so(A3)

        B1, ib1 = M("r_i", "F_{t,i}", "=", "m_i", "r_i^2", r"\alpha", size=52)
        self.pilha.poe(B1)
        self.gat("multiplica os dois lados pela distância")
        self.passo(
            A3, B1,
            (J(ia3, 0), J(ib1, 1)),
            (J(ia3, 1), J(ib1, 2)),
            (J(ia3, 2), J(ib1, 3)),
            (J(ia3, 3), J(ib1, 4)[:2]),
            (J(ia3, 4), J(ib1, 5)),
            rt=1.3,
            origem=True,
        )

        B2, ib2 = M(r"\tau_i", "=", "m_i", "r_i^2", r"\alpha", size=54)
        self.pilha.poe(B2)
        self.gat("isso é justamente o torque")
        self.passo(
            B1, B2,
            (J(ib1, 0, 1), J(ib2, 0)),
            (J(ib1, 2), J(ib2, 1)),
            (J(ib1, 3), J(ib2, 2)),
            (J(ib1, 4), J(ib2, 3)),
            (J(ib1, 5), J(ib2, 4)),
            rt=1.2,
            origem=True,
        )

        self.gat("massa vezes distância ao quadrado")
        dest_mr2 = SurroundingRectangle(mp(B2, ib2, [2, 3]), buff=0.09, corner_radius=0.08).set_stroke(MAS, 3.0)
        self.play(Create(dest_mr2), self.ind(B2, ib2, [2, 3], MAS, 1.15, 0.9), run_time=0.9)
        self.foco = B2
        self.ate(0.99)

        # ── T3-4: soma em todos os pedaços e separa forças externas vs forças internas ──
        self.an("T3-4")
        self.pilha.so(B2, anims=[FadeOut(dest_mr2)])
        self.play(FadeOut(lin_ri), FadeOut(l_mi), FadeOut(l_ri), FadeOut(s_ft), FadeOut(l_ft), realce_i.animate.set_value(0.0), run_time=0.4)

        C1, ic1 = M(r"\sum", r"\tau_i", "=", r"\sum", "m_i", "r_i^2", r"\alpha", size=52)
        self.pilha.poe(C1)
        self.gat("soma isso para todos os pedaços")
        self.passo(
            B2, C1,
            (J(ib2, 0), J(ic1, 1)),
            (J(ib2, 1), J(ic1, 2)),
            (J(ib2, 2), J(ic1, 4)),
            (J(ib2, 3), J(ic1, 5)),
            (J(ib2, 4), J(ic1, 6)),
            rt=1.2,
            origem=False,
        )

        C2, ic2 = M(r"\sum", r"\tau_i", "=", r"\sum", r"\tau_{\mathrm{ext}}", "+", r"\sum", r"\tau_{\mathrm{int}}", size=48)
        self.pilha.poe(C2)
        self.gat("forças externas")
        self.monta(C2, ic2, {0: mp(C1, ic1, [0]), 1: mp(C1, ic1, [1])}, rt=1.1)
        self.foco = C2
        self.ate(0.99)

        # ── T3-5: par interno A–B com forças opostas na mesma linha de ação e mesmo r_⊥ → Σ τ_int = 0 ──
        self.an("T3-5")
        pa, pb = pos(K_A), pos(K_B)
        u_ab = vet_unit(pb - pa)
        # Linha de ação colinear passando por A e B + perpendicular r_⊥ do eixo C_D3 até essa linha
        lin_ab = DashedLine(pa - u_ab * 0.9, pb + u_ab * 0.9, dash_length=0.08).set_stroke(GEO, 2.2, opacity=0.85).set_z_index(13)
        p_proj = pa + np.dot(C_D3 - pa, u_ab) * u_ab
        seg_rp = Line(C_D3, p_proj).set_stroke(GEO, 4.5).set_z_index(14)
        l_rp = T(r"r_\perp", 36, GEO).move_to((C_D3 + p_proj) / 2 + P3(-0.32, -0.22))
        s_fab = seta(pa, pa + u_ab * 0.78, FC, 5.5, tip=0.18, z=16)
        s_fba = seta(pb, pb - u_ab * 0.78, FC, 5.5, tip=0.18, z=16)
        l_fab = T(r"\vec F_{AB}", 34, FC).next_to(pa, UL, buff=0.08)
        l_fba = T(r"\vec F_{BA}", 34, FC).next_to(pb, UR, buff=0.08)

        self.gat("olha um par de pedaços")
        self.play(realce_ab.animate.set_value(1.0), Create(lin_ab), FadeIn(s_fab), FadeIn(s_fba), FadeIn(l_fab), FadeIn(l_fba), run_time=0.9)

        self.gat("mesmo braço de alavanca")
        self.play(Create(seg_rp), FadeIn(l_rp), run_time=0.7)

        D1, id1 = M(r"\tau_{AB}", "+", r"\tau_{BA}", "=", "+", r"r_\perp", "F", "-", r"r_\perp", "F", "=", "0", size=44)
        self.pilha.poe(D1)
        self.gat("os torques se cancelam")
        self.monta(D1, id1, {5: l_rp, 8: l_rp}, rt=1.1)

        # Varredura rápida mostrando todos os pares internos se cancelando aos pares
        self.gat("todos os torques internos somem")
        self.play(
            FadeOut(VGroup(lin_ab, seg_rp, l_rp, s_fab, s_fba, l_fab, l_fba)),
            realce_ab.animate.set_value(0.0),
            varre_pares.animate.set_value(1.0),
            run_time=1.4,
        )
        risco_int = Line(mp(C2, ic2, [6, 7]).get_corner(DL) + 0.06 * DL, mp(C2, ic2, [6, 7]).get_corner(UR) + 0.06 * UR).set_stroke(MAS, 4.0)
        z_int = T("0", 38, MAS).next_to(mp(C2, ic2, [6, 7]), UP, buff=0.10)
        self.play(Create(risco_int), FadeIn(z_int), varre_pares.animate.set_value(0.0), run_time=0.6)
        self.foco = D1
        self.ate(0.99)

        # ── T3-6: α sai da soma e Σ m_i r_i² = I_z → Σ τ_{ext,z} = I_z α em caixa PANEL + tabela de tradução ──
        self.an("T3-6")
        self.pilha.so(C1, anims=[FadeOut(C2), FadeOut(D1), FadeOut(risco_int), FadeOut(z_int)])
        self.play(gira.animate.set_value(0.35), run_time=0.5)

        E1, ie1 = M(r"\sum", r"\tau_{\mathrm{ext},z}", "=", r"\Big(", r"\sum", "m_i", "r_i^2", r"\Big)", r"\alpha", size=50)
        self.pilha.poe(E1)
        self.gat("soma dos torques externos é igual")
        self.passo(
            C1, E1,
            (J(ic1, 0), J(ie1, 0)),
            (J(ic1, 1), J(ie1, 1)),
            (J(ic1, 2), J(ie1, 2)),
            (J(ic1, 3), J(ie1, 4)),
            (J(ic1, 4), J(ie1, 5)),
            (J(ic1, 5), J(ie1, 6)),
            (J(ic1, 6), J(ie1, 8)),
            rt=1.3,
            origem=False,
        )

        self.gat("exatamente o momento de inércia")
        self.play(self.ind(E1, ie1, [3, 4, 5, 6, 7], MAS, 1.14, 0.8), run_time=0.8)

        E2, ie2 = M(r"\sum", r"\tau_{\mathrm{ext},z}", "=", "I_z", r"\alpha", size=58)
        Eb = caixa_l(E2, TQ)
        self.pilha.poe(Eb)
        self.gat("segunda lei da rotação é esta")
        self.cx(Eb[0])
        self.passo(
            E1, E2,
            (J(ie1, 0), J(ie2, 0)),
            (J(ie1, 1), J(ie2, 1)),
            (J(ie1, 2), J(ie2, 2)),
            (J(ie1, 3, 4, 5, 6, 7), J(ie2, 3)),
            (J(ie1, 8), J(ie2, 4)),
            rt=1.2,
            origem=False,
        )
        self.pilha.so(Eb)

        # Tabela de tradução Translação ↔ Rotação
        cab = VGroup(txt("TRANSLAÇÃO", 24, bold=True, color=GEO), txt("ROTAÇÃO", 24, bold=True, color=TQ)).arrange(RIGHT, buff=1.25)
        self.pilha.poe(cab, dx=0.2)
        self.gat("tradução fica completa")
        self.play(FadeIn(cab), run_time=0.4)
        linhas_tab = [
            M("F", r"\ \leftrightarrow\ ", r"\tau", size=44),
            M("m", r"\ \leftrightarrow\ ", "I", size=44),
            M("a", r"\ \leftrightarrow\ ", r"\alpha", size=44),
            M(r"\sum F = m a", r"\ \leftrightarrow\ ", r"\sum\tau = I\alpha", size=44),
        ]
        for lt, ilt in linhas_tab:
            self.pilha.poe(lt, dx=0.2)
            self.monta(lt, ilt, {}, rt=0.45)
        self.foco = Eb
        self.ate(0.99)

        # ── T3-7: três painéis de validade de Σ τ_z = I_z α ──
        self.an("T3-7")
        dv.clear_updaters()
        self.pilha.limpa()
        self.play(
            FadeOut(VGroup(dv, a_alp, l_alp, Eb, cab, *[lt for lt, _ in linhas_tab])),
            run_time=0.45,
        )

        # Três cartões lado a lado mostrando os 3 casos
        def _painel_val(x, tit_s, sub_s, ok, fig):
            cor_b = ACC if ok else MAS
            cx = RoundedRectangle(width=4.4, height=4.8, corner_radius=0.16).move_to(P3(x, -0.55))
            cx.set_fill(PANEL, 0.86).set_stroke(cor_b, 2.6)
            cx._fundo = True
            selo_v = VGroup(
                txt("✓ VALE" if ok else "✗ NÃO BASTA", 22, bold=True, color=cor_b),
                M(r"\sum\tau = I\alpha", size=38)[0],
            ).arrange(RIGHT, buff=0.14).move_to(P3(x, 1.38))
            fig.move_to(P3(x, -0.35))
            t1 = txt(tit_s, 22, bold=True).move_to(P3(x, -2.05))
            t2 = txt(sub_s, 20, color=GEO if ok else MAS).move_to(P3(x, -2.50))
            return VGroup(cx, selo_v, fig, t1, t2)

        # Caso 1: Eixo fixo
        f_fixo = VGroup(disco_aco(ORIGIN, 0.92), eixo_cruz(ORIGIN, 0.16), arco_torque(ORIGIN, 0.62, 1, 0.2, 1.8, TQ))
        p1 = _painel_val(-4.9, "1. EIXO FIXO", "DIREÇÃO E POSIÇÃO FIXAS", True, f_fixo)

        # Caso 2: Eixo pelo CM em movimento plano (roda rolando)
        f_cm = VGroup(
            Line(P3(-1.3, -0.92), P3(1.3, -0.92)).set_stroke(GEO, 2.4),
            roda(ORIGIN, R=0.90, ang=0.4, raios=6),
            cm_pt(ORIGIN, 0.09),
            seta(ORIGIN, P3(0.95, 0.0), VEL, 5, tip=0.16),
        )
        p2 = _painel_val(0.0, "2. EIXO PELO CM", "MOVIMENTO PLANO (DIREÇÃO FIXA)", True, f_cm)

        # Caso 3: Pião inclinado precessando (eixo muda de direção)
        eixo_piao = Line(P3(-0.55, -0.85), P3(0.55, 0.85)).set_stroke(MAS, 3.2)
        corpo_piao = Polygon(P3(-0.55, -0.85), P3(0.72, 0.12), P3(-0.18, 0.68)).set_fill("#6E7E98", 0.9).set_stroke(GEO, 2.0)
        cone_prec = DashedVMobject(Ellipse(width=1.4, height=0.42).move_to(P3(0.0, 0.85)).set_stroke(MAS, 2.0), num_dashes=18)
        f_piao = VGroup(corpo_piao, eixo_piao, cone_prec)
        p3 = _painel_val(4.9, "3. EIXO MUDANDO DE DIREÇÃO", "PRECISA DE MOMENTO ANGULAR", False, f_piao)

        self.play(FadeIn(p1, shift=0.12 * UP), FadeIn(p2, shift=0.12 * UP), FadeIn(p3, shift=0.12 * UP), run_time=0.8)
        self.gat("eixo fixo")
        self.play(p1[0].animate.set_stroke(ACC, 4.2), rate_func=there_and_back, run_time=0.7)
        self.gat("centro de massa")
        self.play(p2[0].animate.set_stroke(ACC, 4.2), rate_func=there_and_back, run_time=0.7)
        self.gat("pião inclinado")
        self.play(p3[0].animate.set_stroke(MAS, 4.2), rate_func=there_and_back, run_time=0.7)
        self.foco = p2
        self.ate(0.99)

"""Lote PB5 v2: B5 — FORÇA CENTRAL, no Three.js 'orbita' (handoff v2 §2.4): estrela no centro de força (O, com bloom), plano orbital de
vidro escuro com grade polar, órbita e planeta de aço com anel rosa. Câmera inclinada 35° (B5-1 a B5-4) e dolly até a vista de cima
ortográfica (B5-5). Unidades da cena: u do desenho (a órbita do B5-5 tem a = 2,6 u, e = 0,6; posições pela equação de Kepler).
B5-1 F⃗ sempre para O: τ⃗ = r⃗ × F⃗ → F⃗ ∥ r⃗ → τ⃗ = 0 → dL⃗/dt = 0 → L⃗ CONSTANTE. B5-2 L⃗ fixo perpendicular ao plano; L = 0: reta pelo
centro. B5-3 setores de mesmo tempo varridos junto com o planeta (area_lab). B5-4 construção de Newton sobre o plano em perspectiva: o
ponto luminoso anda A → B → (c fantasma); chute Δp⃗ como pulso magenta; triângulos OAB, OBc (tracejado), OBC em tons alternados.
B5-5 12 setores de mesmo tempo varridos pelo planeta; ele acelera perto da estrela."""
from pecas24 import *  # noqa: F401,F403

C35 = camd(-90, 35, (-1.56, 0.0, 0.0), 1.0, 43.6, -3.9, -0.45)
CTO = camd(-90, 90, (-1.56, 0.0, 0.0), 0.95, 0.0, -3.9, -0.65)


def kep(Mk, a, e):
    E = Mk
    for _ in range(40):
        E -= (E - e * math.sin(E) - Mk) / (1 - e * math.cos(E))
    return np.array([a * (math.cos(E) - e), a * math.sqrt(1 - e * e) * math.sin(E), 0.0])


class LoteB5(Lote24):
    def corpo(self):
        self.canto("FORÇA CENTRAL")
        self.camA = self.camB = C35
        Mt = ValueTracker(0.6)
        self.add(Mt)
        orb = {"a": 2.2, "e": 0.45, "op": 1.0, "plan": True}

        def planeta():
            return kep(Mt.get_value(), orb["a"], orb["e"])

        def estado(_t=0.0):
            p = planeta()
            return r4(dict(cam=self.cam(), planeta=[float(p[0]), float(p[1])] if orb["plan"] else None, a=orb["a"], ex=orb["e"], orbOp=orb["op"]))
        f3 = Fundo3D(self, "orbita", estado)
        f3._fundo3d = True
        self.add(f3)
        pr = lambda p: self.tela(p)
        O = np.zeros(3)

        # ── B5-1: força sempre para O; τ⃗ = 0 → L⃗ constante ──
        self.an("B5-1")
        Mt.add_updater(lambda m, dt: m.increment_value(0.55 * dt))
        self.transicao(0.5)
        lO = T("O", 40, WHITE_).next_to(pr(O), DL, buff=0.35)

        def cena1():
            p = planeta()
            a, b = pr(O), pr(p + np.array([0, 0, 0.15]))          # centro do planeta (raio 0,15 acima do plano)
            u = (a - b) / np.linalg.norm(a - b)
            n = np.array([-u[1], u[0], 0.0])
            # caso 23 / §3 #10: perto do Sol (periélio) tudo encolhe e os rótulos saem para FORA da órbita (longe de O)
            dist = float(np.linalg.norm(b - a))
            perto = dist < 1.9
            ub = (b - a) / dist
            lf = 0.42 if perto else 0.70
            if perto:
                l_r = T(r"\vec r", 38, VETC).move_to(b + 0.50 * ub + 0.42 * n)
                l_f = T(r"\vec F", 38, FC).move_to(b + 0.50 * u - 0.42 * n)
            else:
                l_r = T(r"\vec r", 38, VETC).move_to((a + b) / 2 - 0.42 * n)
                l_f = T(r"\vec F", 38, FC).move_to(b + 0.45 * u + 0.42 * n)
            return VGroup(vetor_lab(a + 0.30 * ub, b - 0.16 * ub, VETC, w=5, tip=0.18, origem=False),
                          etiqueta_vec(vetor_lab(b + 0.18 * u, b + lf * u, FC, w=6, tip=0.2), "aponta", alvo=lambda: pr(O), nome="F⃗ B5-1"),
                          l_f, l_r)
        c1 = vivo(cena1)
        self.play(FadeIn(lO), OpVivo(c1), run_time=0.7)
        A, ia = Mx(r"\vec\tau", "=", r"\vec r", r"\times", r"\vec F")
        self.pilha.poe(A)
        self.gat("uma força central")
        self.lei(A, ia, rt=1.0, metodo="lei")
        B, ib = Mx(r"\vec F", r"\parallel", r"\vec r")
        self.pilha.poe(B)
        self.gat("na mesma direção do vetor posição")
        self.lei(B, ib, {0: c1[0][2], 2: c1[0][3]}, rt=1.0)
        C, ic = Mx(r"\vec\tau", "=", "0")
        self.pilha.poe(C)
        self.gat("o torque em relação a esse ponto é zero")
        self.gm(A, C, (J(ia, 0), J(ic, 0)), (J(ia, 1), J(ic, 1)), (J(ia, 2, 3, 4), J(ic, 2)), rt=1.2)
        D, id_ = Mx(r"\frac{d\vec L}{dt}", "=", "0")
        self.pilha.poe(D)
        self.gat("torque zero significa")
        self.lei(D, id_, {2: C[0][J(ic, 2)[0]]}, rt=1.0)
        E, ie = Mx(r"\vec L", "=")
        self.pilha.so(B, C, D)
        self.pilha.poe(E)
        self.lei(E, ie, rt=0.6)
        self.texto_na_linha(E, "CONSTANTE", LMAG)
        self.resultado(E, LMAG)
        self.gat("não importa o tamanho da força")
        self.play(pulso(E), run_time=0.8)
        self.ate(0.99)

        # ── B5-2: L⃗ fixo perpendicular ao plano de vidro; a trajetória presa ao plano; L = 0 → reta pelo centro ──
        self.an("B5-2")
        self.play(OpVivo(c1, entra=False), FadeOut(lO), run_time=0.4)
        self.remove(c1)
        self.pilha.so(E)
        Lseta = vetor_lab(pr(O + np.array([0, 0, 0.25])), pr(O + np.array([0, 0, 2.3])), LMAG, origem=False)
        lL = T(r"\vec L", 44, LMAG).next_to(pr(O + np.array([0, 0, 2.3])), LEFT, buff=0.3)
        # marca de ângulo reto entre L⃗ e o plano
        ret = angulo_reto(pr(O + np.array([0, 0, 0.25])), pr(O + np.array([0, 0, 0.75])), pr(O + np.array([0.5, 0, 0.25])), s=0.22, cor=WHITE_)
        self.gat("perpendicular ao vetor posição")
        self.play(FadeIn(Lseta, shift=0.3 * UP), FadeIn(lL), FadeIn(ret), run_time=0.8)
        self.gat("nunca sai do plano")
        self.play(Indicate(lL, color=LMAG), run_time=0.8)
        f1 = txt("O MOVIMENTO FICA NUM PLANO", 30, bold=True, color=GEO)
        self.pilha.poe(f1)
        self.gat("o movimento fica num plano")
        self.play(FadeIn(f1), run_time=0.5)
        self.gat("se o momento angular for zero")
        radial = DashedLine(pr(np.array([-3.6, -0.9, 0])), pr(np.array([2.3, 0.58, 0])), dash_length=0.1).set_stroke(MAG, 3).set_z_index(8)
        L0 = VGroup(T("L", 40, LMAG), T(r"=\,0", 40, WHITE_)).arrange(RIGHT, buff=0.08)
        L0.next_to(pr(np.array([2.3, 0.58, 0])), UL, buff=0.12)      # caso 24: na ponta da reta, fora do plano
        self.play(Create(radial), FadeIn(L0), run_time=0.7)
        self.ate(0.99)

        # ── B5-3: setores de mesmo tempo varridos junto com o planeta; dA/dt = |L⃗|/2m ──
        self.an("B5-3")
        self.play(FadeOut(VGroup(Lseta, lL, ret, radial, L0)), run_time=0.4)
        self.gat("a área varrida por segundo")
        G_, ig = Mx(r"\frac{dA}{dt}", "=", r"\frac{|\vec L|}{2m}")
        self.pilha.poe(G_)
        janelas = ((-0.35, 0.40), (2.55, 3.30))
        Mt.clear_updaters()
        Mt.set_value(-0.6)
        Mt.add_updater(lambda m, dt: m.increment_value(0.85 * dt))

        def setor(k):
            t0, t1 = janelas[k]

            def f():
                t = min(Mt.get_value(), t1)
                if t <= t0 + 1e-3:
                    return VGroup()
                return area_lab([pr(O)] + [pr(kep(x, orb["a"], orb["e"])) for x in np.linspace(t0, t, 14)], op=(0.40, 0.25)[k])
            return vivo(f)
        sets = [setor(0), setor(1)]
        self.add(*sets)
        self.lei(G_, ig, rt=1.2, metodo="lei")
        self.gat("áreas iguais em tempos iguais")
        self.wait(1.0)
        f2 = VGroup(txt("UM FIO · UMA MOLA ·", 26, bold=True, color=GEO), txt("A GRAVIDADE DO SOL", 26, bold=True, color=GEO)).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
        self.pilha.poe(f2)
        self.gat("para qualquer força central")
        self.play(FadeIn(f2), run_time=0.5)
        self.ate(0.99)

        # ── B5-4: construção de Newton sobre o plano de vidro em perspectiva (hold) ──
        self.an("B5-4")
        Mt.clear_updaters()
        orb["plan"] = False
        self.play(*[OpVivo(s_, entra=False) for s_ in sets], run_time=0.4)
        self.remove(*sets)
        orb["op"] = 0.0
        self.pilha.limpa()
        A3, B3 = np.array([-3.95, 1.2, 0]), np.array([-1.9, 2.2, 0])
        c3 = 2 * B3 - A3
        kick = 0.33 * (O - B3)
        C3 = c3 + kick
        pA, pB, pc, pC, pO = pr(A3), pr(B3), pr(c3), pr(C3), pr(O)
        lab = lambda s, p, d, cor=WHITE_: T(s, 40, cor).next_to(p, d, buff=0.28)
        self.play(FadeIn(lab("O", pO, DL)), FadeIn(lab("A", pA, LEFT)), run_time=0.4)
        self.gat("sem força")
        # o ponto luminoso anda A → B; os triângulos varrem junto (area_lab)
        s = ValueTracker(0.0)
        self.add(s)

        def ponto():
            u = s.get_value()
            if u <= 1:
                p = pA + (pB - pA) * u
            elif u <= 2:
                p = pB + (pc - pB) * (u - 1)
            else:
                p = pB + (pC - pB) * min(1.0, u - 2)
            return ponto_vivo(p, MAS)

        def tri_vivo(i0, i1, op, k0):
            def f():
                u = min(1.0, s.get_value() - k0)
                if u <= 1e-3:
                    return VGroup()
                return area_lab([pO, i0, i0 + (i1 - i0) * u], op=op)
            return vivo(f)
        pv = vivo(ponto)
        t1 = tri_vivo(pA, pB, 0.40, 0.0)
        seg1 = vivo(lambda: Line(pA, pA + (pB - pA) * min(1, s.get_value())).set_stroke(RAST, 3).set_z_index(9))
        self.add(t1, seg1, pv)
        self.play(s.animate.set_value(1.0), run_time=1.2, rate_func=linear)
        lB = lab("B", pB, LEFT)
        self.play(FadeIn(lB), run_time=0.3)
        t2 = tri_vivo(pB, pc, 0.25, 1.0)
        fant = vivo(lambda: DashedLine(pB, pB + (pc - pB) * max(0.02, min(1, s.get_value() - 1)), dash_length=0.1).set_stroke(RAST, 3).set_z_index(9))
        self.add(t2, fant)
        self.play(s.animate.set_value(2.0), run_time=1.2, rate_func=linear)
        lc = lab("C'", pc, UL, GEO)
        lc._fantasma = True
        ring_c = Circle(radius=0.17).move_to(pc).set_stroke(GEO, 2.6).set_z_index(10)      # v13 §2.3.1: o ponto onde ela estaria sem o chute
        self.gat("onde ela estaria sem o chute")
        self.play(FadeIn(lc), Create(ring_c), run_time=0.4)
        self.play(Indicate(ring_c, color=GEO, scale_factor=1.5), run_time=0.5)
        N1, n1 = Mx(r"A_{OAB}", "=", r"A_{OBC'}", cores={0: GEO, 2: GEO})
        self.pilha.poe(N1)
        self.lei(N1, n1, rt=1.0)
        self.gat("ela leva um chute")
        # caso 25: Δp⃗ como pulso magenta em B (acende e apaga com brilho), rótulo fora da aresta OB
        uk = (pO - pB) / np.linalg.norm(pO - pB)
        nk = np.array([-uk[1], uk[0], 0.0])
        off = 0.16 * nk if np.dot(nk, pA - pB) < 0 else -0.16 * nk          # caso 25: o pulso corre paralelo à aresta OB, do lado de fora
        sk = vetor_lab(pB + off, pB + off + 1.1 * uk, MAG)
        lk = T(r"\Delta\vec p", 40, MAG).move_to(pB + 0.85 * uk - 0.70 * (off / 0.16))
        self.play(FadeIn(sk, scale=0.6), FadeIn(lk), run_time=0.4)
        self.play(sk.animate.set_opacity(0.35), run_time=0.4)
        self.gat("vai parar no ponto c")
        s.set_value(2.0)
        t3 = tri_vivo(pB, pC, 0.40, 2.0)
        seg2 = vivo(lambda: Line(pB, pB + (pC - pB) * max(0.02, min(1, s.get_value() - 2))).set_stroke(RAST, 3).set_z_index(9))
        self.add(t3, seg2)
        self.play(s.animate.set_value(3.0), run_time=1.2, rate_func=linear)
        nC = np.array([-(pB - pO)[1], (pB - pO)[0], 0.0]); nC /= np.linalg.norm(nC)
        if np.dot(nC, pC - pO) < 0:
            nC = -nC
        lC = T("C", 40, WHITE_).move_to(pC + 0.52 * nC)
        self.play(FadeIn(lC), run_time=0.3)
        self.gat("é paralela à reta que liga")
        u = (pB - pO) / np.linalg.norm(pB - pO)
        par = DashedLine(pc + 0.9 * u, pC - 1.2 * u, dash_length=0.12).set_stroke(WHITE_, 2.4).set_z_index(9)
        base = Line(pO, pB).set_stroke(VETC, 4).set_z_index(9)
        cc_seg = Line(pc, pC).set_stroke(MAG, 5).set_z_index(10)                            # v13 §2.3.1: a diferença C′C, paralela a OB
        self.play(Create(par), Create(base), Create(cc_seg), run_time=0.8)
        self.play(Indicate(cc_seg, color=MAG, scale_factor=1.1), Indicate(base, color=VETC, scale_factor=1.05), run_time=0.7)
        tri_a = Polygon(pO, pB, pc).set_fill(GEO, 0.38).set_stroke(GEO, 2).set_z_index(4)      # os dois triângulos na mesma cor: mesma base e mesma altura
        tri_b = Polygon(pO, pB, pC).set_fill(GEO, 0.38).set_stroke(GEO, 2).set_z_index(4)
        self.gat("a mesma base e a mesma altura")
        self.play(FadeIn(tri_a), FadeIn(tri_b), Indicate(base, color=VETC, scale_factor=1.0), run_time=0.7)
        N2, n2 = Mx(r"A_{OBC}", "=", r"A_{OBC'}", cores={0: GEO, 2: GEO})
        self.pilha.poe(N2)
        self.lei(N2, n2, rt=1.0)
        f3_ = txt("CHUTE CENTRAL NÃO MUDA A ÁREA", 30, bold=True, color=GEO)
        self.pilha.poe(f3_)
        self.gat("chute central não muda a área")
        self.play(FadeIn(f3_), run_time=0.5)
        self.ate(0.99)

        # ── B5-5: dolly até a vista de cima; 12 setores de mesmo tempo varridos pelo planeta; ele acelera perto da estrela ──
        self.an("B5-5")
        vivos_ = [t1, t2, t3, seg1, seg2, fant, pv]
        self.play(*[OpVivo(m, entra=False) for m in vivos_], *[FadeOut(m_) for m_ in (sk, lk, lB, lc, lC, par, base, ring_c, cc_seg, tri_a, tri_b)],
                  *[FadeOut(m) for m in self.mobjects if isinstance(m, MathTex) and m.get_x() < 0.3 and m not in self.fixos()], run_time=0.4)
        self.remove(*vivos_)
        self.pilha.limpa()
        orb.update(a=F.A_ELI, e=F.E_ELI, plan=True)
        Mt.set_value(0.0)
        opv = ValueTracker(0.0)
        self.add(opv)
        opv.add_updater(lambda m: orb.__setitem__("op", float(m.get_value())))
        self.dolly(CTO, 1.6, opv.animate.set_value(1.0))
        opv.clear_updaters()
        orb["op"] = 1.0
        self.gat("por isso um planeta")
        Mt.add_updater(lambda m, dt: m.increment_value(2 * math.pi / 7.2 * dt))

        def setor12(k):
            t0, t1_ = 2 * math.pi * k / 12, 2 * math.pi * (k + 1) / 12

            def f():
                t = min(Mt.get_value(), t1_)
                if t <= t0 + 1e-3:
                    return VGroup()
                return area_lab([pr(O)] + [pr(kep(x, orb["a"], orb["e"])) for x in np.linspace(t0, t, 10)], op=0.40 if k % 2 == 0 else 0.22)
            return vivo(f)
        setores = [setor12(k) for k in range(12)]
        self.add(*setores)
        self.wait(2.0)
        K1, k1 = Mx(r"\frac{dA}{dt}", "=", r"\frac{|\vec L|}{2m}")
        self.pilha.poe(K1)
        self.lei(K1, k1, rt=1.2)
        f4 = txt("PERTO DO SOL: MAIS RÁPIDO", 28, bold=True, color=GEO)
        self.pilha.poe(f4)
        self.gat("perto, o braço é curto")
        self.play(FadeIn(f4), run_time=0.5)
        # v13 §2.3.2: a Terra passa mais rápido por volta de janeiro (periélio) e mais devagar por volta de julho (afélio)
        pp_, pa_ = pr(kep(0.0, orb["a"], orb["e"])), pr(kep(math.pi, orb["a"], orb["e"]))
        l_per = txt("PERIÉLIO ~ JAN", 22, bold=True, color=GEO).next_to(pp_, RIGHT, buff=0.18)
        l_afe = txt("AFÉLIO ~ JUL", 22, bold=True, color=GEO).next_to(pa_, DOWN, buff=1.2)
        self.gat("por volta de janeiro")
        self.play(FadeIn(l_per), run_time=0.4)
        self.play(Indicate(l_per, color=GEO, scale_factor=1.15), run_time=0.5)
        self.gat("por volta de julho")
        self.play(FadeIn(l_afe), run_time=0.4)
        self.play(Indicate(l_afe, color=GEO, scale_factor=1.15), run_time=0.5)
        self.ate(0.995)

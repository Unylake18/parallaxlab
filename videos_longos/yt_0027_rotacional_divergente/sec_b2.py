"""Lote PB2 · ROTACIONAL (handoff v2; quadros 04 a 07). Layout A, campo (−y, 2x) com os braços NA ORIGEM (F = 0: a cruz fica parada no centro).
B2-1/2: braço AB (0, 0)–(1,5; 0), seta em B, fluxo exato t 0 → 0,28 com fantasma; ω_AB ≈ … → ∂Q/∂x (TransformByGlyphMap, a linha 1 fica).
B2-3: braço AC, a regra geral em miniatura (HORÁRIO ⇒ sinal −), ω_AC. B2-4: a tesoura t 0 → 0,5 (2 e 1 rad/s), a rodinha R = 1,05 a 1,5 rad/s.
B2-5: rot F e os números (TransformByGlyphMap da forma geral). B2-6: (−y, x) em anéis, fita e rodinha em órbita (uma volta)."""
from MF_Tools import TransformByGlyphMap

from v27 import *  # noqa: F401,F403

V = Vista(600, 540, 120)


def lbl(s, X, Y, size=40):
    x, y = canto_xy(V, X, Y)
    return TP(s, x, y, size)


def tbgm(a, b, *mapa, rt=1.6, copia=True):
    an = TransformByGlyphMap(a, b, *mapa, from_copy=copia, printing=False, run_time=rt)
    ja_escrita(b)
    return an


class LoteB2(Base):
    ANTES = "UM PEDACINHO DE FLUIDO"
    def corpo(self):
        # ── B2-1 ──
        self.an("B2-1")
        self.secao("ROTACIONAL")
        cmp = campo7(V, F_Y2X, mmax=6.0, nome="B2 (−y, 2x)")
        self.play(cresce_campo(cmp, 1.6))
        o = ponto7(V.c2p(0, 0), CORAL, 8, 9)
        AB = Material(V, seg_pts((0, 0), (1.5, 0)), fl_y2x, CORAL, 7, pontas=True)
        lA, lB, lh = lbl(r"\C{A}", -0.22, -0.28), lbl(r"\C{B}", 1.62, -0.32), lbl(r"\h", 0.75, -0.32)
        esc1 = esconde(cmp, clar([(-0.35, -0.6, 2.0, 1.4)]))          # R1: clareira do braço AB, da seta em B, do arco e dos rótulos
        self.gat("pega só duas partículas")
        self.play(UpdateFromAlphaFunc(cmp, lambda m, a: m.contexto(a > 0.5)), some(esc1), FadeIn(AB.pontas[0], scale=0.4), FadeIn(AB.pontas[1], scale=0.4), FadeIn(o), run_time=0.6)
        self.gat("ligadas por um braço")
        self.play(Create(AB.tr), FadeIn(lA), FadeIn(lB), run_time=0.6)
        self.add(AB)
        self.gat("cada ponta do braço é carregada")
        self.play(FadeIn(lh), run_time=0.4)
        self.ate(0.97)

        # ── B2-2 ──
        self.an("B2-2")
        vB = seta7(V.c2p(1.5, 0), V.c2p(1.5, 1.2), CAMPO2, 6, 24).set_z_index(10)
        self.gat("repara só na parte vertical")
        self.play(GrowArrow(vB), run_time=0.7)
        fant = vlinha(V, [(0, 0), (1.5, 0)], CORAL, 4, alpha=0.7, dash=(10, 9))
        arc = giro_seta(V, (0, 0), 1.85, 0.05, 0.3)
        self.gat("se a ponta da direita sobe")
        self.add(fant)
        self.play(*corre(self, [AB], 0.28, 2.0), run_time=2.0)
        self.play(Create(arc), run_time=0.5)
        print(f"[braços] B2-2: o braço AB girou {AB.ang():.3f} rad em t = 0,28 (taxa média {AB.ang() / 0.28:.3f} rad/s; inicial 2)")
        L1 = TC(r"\w_{\C{AB}} \approx \dfrac{\Qq(\xo+\h,\,\yo) - \Qq(\xo,\,\yo)}{\h}", 1120, 400, 48)
        L2 = TC(r"\w_{\C{AB}} = \dfrac{\partial \Qq}{\dx}", 1120, 400, 56)          # v4 N3: no lugar da L1
        self.gat("e com que rapidez")
        self.play(caneta(L1))
        self.gat("essa razão vira a derivada")
        self.play(tbgm(L1, L2, ([0], [0]), ([1], [1]), ([2], [2]), ([3], [3]), ([4], [5]), ([23], [6]), (list(range(5, 23)) + [24], []), ([], [4, 7, 8]), copia=False))   # final §2.12: o h e o ∂x por fade (regra 3)
        self.remove(L1)
        self.limpa_tbgm()
        self.add(L2)
        lg = legenda("BRAÇO HORIZONTAL", 1124, 520, CORAL)
        self.gat("essa é a velocidade angular")
        self.play(FadeIn(lg, shift=0.1 * UP), run_time=0.5)
        self.ate(0.97)

        # ── B2-3 ──
        self.an("B2-3")
        sai = [AB, vB, fant, arc, lA, lB, lh, L2, lg]
        esc2 = esconde(cmp, clar([(-0.75, -0.6, 0.65, 2.05)]))
        AC = Material(V, seg_pts((0, 0), (0, 1.5)), fl_y2x, CORAL, 7, pontas=True)
        lA2, lC, lk = lbl(r"\C{A}", 0.28, -0.25), lbl(r"\C{C}", 0.3, 1.6), lbl(r"\k", 0.3, 0.75)
        self.gat("agora um braço vertical")                                   # final: a saída do B2-2 vai junto da entrada (a fala começa logo)
        self.play(*[FadeOut(m) for m in sai], volta(VGroup(*[s_ for s_ in esc1 if s_ not in esc2])), some(VGroup(*[s_ for s_ in esc2 if s_ not in esc1])),
                  Create(AC.tr), FadeIn(AC.pontas[0]), FadeIn(AC.pontas[1]), FadeIn(lA2), FadeIn(lC), FadeIn(lk), run_time=0.7)
        self.remove(*sai)
        self.limpa_tbgm()
        lA = lA2
        self.add(AC)
        vC = seta7(V.c2p(0, 1.5), V.c2p(-0.6, 1.5), CAMPO2, 6, 24).set_z_index(10)
        self.gat("o que importa é a parte horizontal")
        self.play(GrowArrow(vC), run_time=0.6)
        # a regra geral, em miniatura
        vm = Vista(1210, 720, 70)
        mini = VGroup(vlinha(vm, [(0, -1), (0, 1)], GEO, 5, dash=(9, 8)), seta7(vm.c2p(0, 1), vm.c2p(1.3, 1), CAMPO2, 6, 20),
                      seta7(vm.c2p(0, -1), vm.c2p(0.45, -1), CAMPO2, 6, 20), giro_seta(vm, (0, 0), 1.25, PI / 2 + 0.15, PI / 2 - 0.6, VIO, 4))
        hor = legenda("HORÁRIO", 1330, 705, VIO, size=30)
        sinal = TC(r"\Rightarrow\ \text{sinal } -", 1330, 760, 40)
        self.gat("se a ponta de cima anda para a direita")
        self.play(FadeIn(mini), run_time=0.6)
        self.play(FadeIn(hor), caneta(sinal))
        fC = TC(r"\w_{\C{AC}} = -\dfrac{\partial \Pp}{\dy}", 1120, 400, 56)
        menos = fC[0][4]
        lv = legenda("BRAÇO VERTICAL", 1124, 520, CORAL)
        self.gat("por isso a velocidade angular dele")
        self.play(caneta(fC, ordem=lambda gs: [g for g in gs if g is not menos] + [menos]))
        self.play(FadeIn(lv, shift=0.1 * UP), run_time=0.4)
        fant2 = vlinha(V, [(0, 0), (0, 1.5)], CORAL, 4, alpha=0.7, dash=(10, 9))
        arc2 = giro_seta(V, (0, 0), 1.85, PI / 2 + 0.05, PI / 2 + 0.3)
        self.gat("neste campo a ponta de cima vai para a esquerda")
        self.add(fant2)
        self.play(*corre(self, [AC], 0.15, 1.6), run_time=1.6)
        self.play(Create(arc2), run_time=0.5)
        print(f"[braços] B2-3: o braço AC girou {AC.ang() - PI / 2:.3f} rad em t = 0,15 (taxa média {(AC.ang() - PI / 2) / 0.15:.3f} rad/s; inicial 1)")
        fc = TC(r"\dfrac{\partial \Pp}{\dy} = -1 \;\Rightarrow\; \w_{\C{AC}} = -(-1) = 1", 1120, 900, 44)
        self.gat("menos com menos dá mais")
        self.play(caneta(fc))
        self.ate(0.97)

        # ── B2-4 · a tesoura e a rodinha ──
        self.an("B2-4")
        sai = [AC, vC, fant2, arc2, lA, lC, lk, mini, hor, sinal, fC, lv, fc]
        Hf, Vf = fl_y2x(np.array([1.5]), np.array([0.0]), 0.5), fl_y2x(np.array([0.0]), np.array([1.5]), 0.5)
        lH = (float(Hf[0][0]) + 0.75, float(Hf[1][0]) + 0.05)
        lV = (float(Vf[0][0]) - 0.75, float(Vf[1][0]) + 0.25)
        cam = []
        for t_ in np.linspace(0, 0.5, 9):                                       # R6: o caminho inteiro dos dois rótulos
            h_, v_ = fl_y2x(np.array([1.5]), np.array([0.0]), t_), fl_y2x(np.array([0.0]), np.array([1.5]), t_)
            cam += [(float(h_[0][0]) + 0.75, float(h_[1][0]) + 0.05), (float(v_[0][0]) - 0.75, float(v_[1][0]) + 0.25)]
        rl = [(x_ - 0.6, y_ - 0.22, x_ + 0.6, y_ + 0.22) for x_, y_ in cam]
        esc3 = esconde(cmp, clar(rl, [(0, 0)], 1.2))
        self.play(*[FadeOut(m) for m in sai], volta(VGroup(*[s_ for s_ in esc2 if s_ not in esc3])), some(VGroup(*[s_ for s_ in esc3 if s_ not in esc2])), run_time=0.5)
        self.remove(*sai)
        g1, g2 = vlinha(V, [(0, 0), (1.5, 0)], GEO, 3, alpha=0.6, dash=(6, 8)), vlinha(V, [(0, 0), (0, 1.5)], GEO, 3, alpha=0.6, dash=(6, 8))
        H = Material(V, seg_pts((0, 0), (1.5, 0)), fl_y2x, CORAL, 7, pontas=True)
        Vv = Material(V, seg_pts((0, 0), (0, 1.5)), fl_y2x, CORAL, 7, pontas=True)
        self.play(FadeIn(g1), FadeIn(g2), Create(H.tr), Create(Vv.tr), FadeIn(H.pontas[1]), FadeIn(Vv.pontas[1]), run_time=0.7)
        self.add(H, Vv)
        l2 = lbl(r"\V{2\ \text{rad/s}}", 1.5 + 0.75, 0.05, 38)
        l1 = lbl(r"\V{1\ \text{rad/s}}", -0.75, 1.5 + 0.25, 38)

        def segue(lb, mat, d):
            def f(m):
                p = mat.XY[-1]
                x, y = canto_xy(V, p[0] + d[0], p[1] + d[1])
                m.move_to(PX(x, y))
            return f
        f1, f2 = TC(r"\w_{\C{AB}} = \V{2}", 1120, 360, 52), TC(r"\w_{\C{AC}} = \V{1}", 1120, 470, 52)
        self.gat("o horizontal gira a dois")                                  # final: cada ω escrito na sua frase
        self.play(FadeIn(l2, run_time=0.4), caneta(f1))
        self.gat("e o vertical a um só")
        l2.add_updater(segue(l2, H, (0.75, 0.05)))
        l1.add_updater(segue(l1, Vv, (-0.75, 0.25)))
        self.play(FadeIn(l1, run_time=0.4), caneta(f2), self.em("a cruz abre e fecha", AnimationGroup(*corre(self, [H, Vv], 0.5, 2.5, rate=smooth))))
        print(f"[braços] B2-4: pontas em t = 0,5: H = ({H.XY[-1][0]:.3f}; {H.XY[-1][1]:.3f}), V = ({Vv.XY[-1][0]:.3f}; {Vv.XY[-1][1]:.3f}) "
              f"(alvo (1,140; 1,378) e (−0,689; 1,140))")
        for lb in (l1, l2):
            lb.clear_updaters()
        rd = Roda(V, 1.05).pose((0, 0), 0.0)
        self.gat("uma rodinha de pás não vira tesoura")
        self.play(FadeOut(H), FadeOut(Vv), FadeOut(l1), FadeOut(l2), FadeOut(g1), FadeOut(g2), run_time=0.5)
        self.remove(H, Vv, l1, l2, g1, g2)
        self.play(FadeIn(rd, scale=0.7), run_time=0.6)
        mr = Motor(self, 1.0, "B2-4/5 rodinha a 1,5 rad/s (tempo de tela)").liga()
        rd.add_updater(lambda m: m.pose((0, 0), 1.5 * mr.tau()))
        arc3 = giro_seta(V, (0, 0), 1.3, -0.6, 0.1)
        f3 = TC(r"\w_{\text{\C{roda}}} = \dfrac{\V{2} + \V{1}}{2} = \V{\dfrac{3}{2}}", 1120, 620, 52)
        lg = legenda("A RODINHA GIRA NA MÉDIA DOS DOIS BRAÇOS", 1124, 760)
        self.gat("na média dos dois braços")
        self.play(caneta(f3), Create(arc3), FadeIn(lg, shift=0.1 * UP))
        self.ate(0.97)

        # ── B2-5 · rot F ──
        self.an("B2-5")
        sai = [f1, f2, f3, lg, arc3]
        esc4 = esconde(cmp, clar([], [(0, 0), (1.45, 1.1)], 1.35))          # S03: clareira de raio 1,35 em volta da rodinha e do ⊙k
        arc4 = giro_seta(V, (0, 0), 1.3, -0.4, 1.1)
        od = lbl(r"\odot\,\kk", 1.45, 1.1, 46)
        R1 = TC(r"\rot \F = \left(\dfrac{\partial \Qq}{\dx} - \dfrac{\partial \Pp}{\dy}\right)\kk = 2\,\w\,\kk", 1120, 380, 50)
        self.gat("é daí que nasce o rotacional")                              # final: a saída do B2-4 vai junto da caneta
        cR1 = caneta(R1, atraso=0.45)                                         # R6: a coluna velha sai antes do 1º glifo
        vo_, so_ = volta(VGroup(*[s_ for s_ in esc3 if s_ not in esc4]), 0.5), some(VGroup(*[s_ for s_ in esc4 if s_ not in esc3]), 0.5)
        vo_.rate_func = so_.rate_func = so_no_inicio(cR1, 0.45)
        self.play(*[FadeOut(m, rate_func=so_no_inicio(cR1, 0.4)) for m in sai], vo_, so_, cR1, Create(arc4))
        self.remove(*sai)
        R2 = TC(r"\F = (-\Y,\ 2\X)", 1120, 530, 48)
        R3 = TC(r"\dfrac{\partial \Qq}{\dx} = 2,\qquad \dfrac{\partial \Pp}{\dy} = -1", 1120, 650, 46)
        R4 = TC(r"\rot \F = \bigl(2 - (-1)\bigr)\kk = \V{3}\,\kk", 1120, 790, 50)
        self.gat("repara que a fórmula não apareceu")                         # final: o campo e os dois termos entram com "cada termo veio de um braço"
        self.play(caneta(R2))
        self.gat("cada termo veio do movimento")
        self.play(caneta(R3))
        self.gat("um vetor perpendicular à folha")
        self.play(FadeIn(od), run_time=0.5)
        self.gat("neste campo ele vale três")
        self.play(caneta(R4), self.em("a rodinha gira a três meios", pulso(arc4, 1.12, run_time=0.8)))   # v4 R6: sem cópia descendo por cima de R2 e R3
        self.gat("e o dobro de um e meio é três")
        self.play(pulso(R4[0][17], 1.35), run_time=0.8)
        self.ate(0.97)
        rd.clear_updaters()

        # ── B2-6 · o primeiro redemoinho ──
        self.an("B2-6")
        self.limpa_tbgm()
        self.limpa_junto(rt=0.5)
        cg = campo_polar(V, F_GIRO, [1, 1.5, 2, 2.5], mmax=2.5, nome="B2-6 (−y, x)")
        r6 = Roda(V, 0.42).pose((1.5, 0), 0)
        clareira_viva(cg, lambda: [r6.c], 0.62)
        self.play(cresce_campo(cg, 1.0, lambda s: (round(math.hypot(*s._xy), 3), math.atan2(s._xy[1], s._xy[0]))), FadeIn(r6), run_time=1.0)
        self.add(cg)                                   # o grupo entra na cena: o updater da clareira da rodinha passa a rodar
        linhas = [(r"\F = (-\Y,\ \X)", 250, 52, "troca as coordenadas de lugar"),
                  (r"\Pp = -\Y, \qquad \Qq = \X", 345, 46, "o p é menos y"),
                  (r"\dfrac{\partial \Qq}{\dx} = 1, \qquad \dfrac{\partial \Pp}{\dy} = -1", 470, 48, "a derivada do q em x dá um"),
                  (r"\rot \F = \big(1 - (-1)\big)\kk = \V{2}\,\kk", 600, 50, "um menos menos um"),
                  (r"\w = 1", 710, 50, "a rodinha gira a um radiano")]
        fs_ = []
        for s, y, sz, frase in linhas:
            self.gat(frase)
            f = TC(s, 1120, y, sz)
            fs_.append(f)
            self.play(caneta(f))
        # uma volta inteira (t de 0 a 2π) terminando na frase "completa um giro a cada volta"
        rt = max(3.0, self.falta("por isso ela completa um giro") + 0.8)

        def volta_r6(m, a):
            t = 2 * PI * a
            x, y = fl_giro(np.array([1.5]), np.array([0.0]), t)
            r6.pose((float(x[0]), float(y[0])), t)
        print(f"[motor] B2-6: uma volta (t = 2π) em {rt:.2f} s (fator {2 * PI / rt:.3f})")
        self.play(UpdateFromAlphaFunc(r6, volta_r6), run_time=rt, rate_func=linear)
        v1 = legenda("VORTICIDADE =", 1124, 800, VEL)                                # v4 N4: por último, embaixo de tudo
        v2 = TC(r"\V{2\omega}", 0, 0, 34, caneta=False)
        v2.next_to(v1, RIGHT, buff=0.12).align_to(v1, DOWN)
        v3 = legenda("(CORPO RÍGIDO)", 0, 800, VEL)
        v3.next_to(v2, RIGHT, buff=0.18).align_to(v1, DOWN)
        v2._esc = True
        vt = VGroup(v1, v2, v3)
        self.gat("vorticidade")
        self.play(FadeIn(vt, shift=0.1 * UP), run_time=0.5)
        self.ate(0.97)
        cg.clear_updaters()
        self.sai_fim()

    def limpa_tbgm(self):
        """O TransformByGlyphMap deixa grupos soltos na cena; tira os que não estão mais visíveis."""
        for m in list(self.mobjects):
            if isinstance(m, VGroup) and not len(m.family_members_with_points()):
                self.remove(m)

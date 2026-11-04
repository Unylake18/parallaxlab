"""Lote PA: abertura A1 (logo Parallax Lab + ondas), A2 (título + três ícones da agenda que se animam quando citados: porta com seta e braço de
alavanca, disco em pedaços girando com α, engrenagens + gangorra), A3 (bloco 2,5D com F = m a na translação → disco preso num eixo onde a mesma
força empurra em lugares diferentes → pergunta τ = ?)."""
from pecas22 import *  # noqa: F401,F403

C_A3 = P3(-3.6, -0.45)


class LoteA(Lote22):
    def corpo(self):
        # ── A1 ──
        self.an("A1")
        logo = self.logo(5.6).move_to(P3(0, 0.9))
        aneis = VGroup(*[Circle(radius=r).move_to(P3(0, 0.9)).set_stroke(VEL, 2.2, opacity=o) for r, o in ((2.1, 0.35), (2.45, 0.2))])
        bv = txt("BEM-VINDOS AO PARALLAX LAB", 30).move_to(P3(0, -1.6))
        self.play(FadeIn(logo, scale=0.94), FadeIn(aneis), FadeIn(bv, shift=0.1 * UP), run_time=0.8)
        self.play(aneis.animate.scale(1.05), run_time=max(0.5, self.resta() - 0.4))
        self.ate(0.99)

        # ── A2 ──
        self.an("A2")
        tt = txt("TORQUE:", 44, bold=True).move_to(P3(0, 2.7))
        tt2 = txt("POR QUE A PONTA DA RÉGUA ACELERA MAIS QUE A GRAVIDADE?", 28, bold=True).next_to(tt, DOWN, buff=0.2)
        nv = txt("NESTE VÍDEO:", 28).move_to(P3(-5.4, 0.85))
        ics = VGroup(*[self.item(k) for k in range(3)])
        for k, it in enumerate(ics):
            it.move_to(P3(-4.3 + 4.3 * k, -1.3))
        self.play(FadeOut(logo), FadeOut(aneis), FadeOut(bv), run_time=0.35)
        self.play(FadeIn(tt, shift=0.1 * UP), FadeIn(tt2, shift=0.1 * UP), FadeIn(nv), FadeIn(ics), run_time=0.8)
        ul = VGroup()
        for k, frase in enumerate(("primeiro por que a posição", "depois a segunda lei de newton", "por fim trabalho e potência")):
            self.gat(frase)
            ul.add(Line(ics[k].get_corner(DL) + 0.16 * DOWN, ics[k].get_corner(DR) + 0.16 * DOWN).set_stroke(CYAN, 3.5))
            self.play(Create(ul[-1]), self.ind_copia(ics[k][0], WHITE_, 1.08, 0.7), run_time=0.7)
            self.foco = ics[k][0]
        self.ate(0.99)

        # ── A3: translação (F = m a) → rotação (mesma força em pontos diferentes, o que faz o papel da força?) ──
        self.an("A3")
        self.play(FadeOut(VGroup(tt, tt2, nv, ics, ul)), run_time=0.35)

        # Bloco 2,5D de aço deslizando na translação
        bloco = RoundedRectangle(width=1.8, height=1.1, corner_radius=0.12).move_to(P3(-4.6, 1.35))
        aco(bloco, 2.2)
        cm_b = cm_pt(bloco.get_center(), 0.08)
        s_F = seta(bloco.get_left() + LEFT * 1.35, bloco.get_left() + LEFT * 0.05, FC, 6, tip=0.20)
        l_F = T("F", 42, FC).next_to(s_F, UP, buff=0.12)
        s_a = seta(bloco.get_right() + RIGHT * 0.12, bloco.get_right() + RIGHT * 1.15, ACC, 6, tip=0.20)
        l_a = T("a", 42, ACC).next_to(s_a, UP, buff=0.12)
        g_bloco = VGroup(bloco, cm_b, s_F, l_F, s_a, l_a)
        self.play(FadeIn(g_bloco, shift=0.15 * RIGHT), run_time=0.7)

        A, ia = M("F", "=", "m", "a", size=54)
        self.pilha.poe(A)
        self.gat("força resultante é massa vezes aceleração")
        self.monta(A, ia, {0: l_F, 3: l_a}, rt=0.9)

        # Disco 2,5D preso num eixo central na parte inferior esquerda
        ang_d = ValueTracker(0.0)
        vel_d = ValueTracker(0.0)
        ang_d.add_updater(lambda m, dt: m.increment_value(vel_d.get_value() * dt))
        self.add(ang_d, vel_d)

        C_D = P3(-3.6, -1.55)
        R_D = 1.55
        dv = vivo(lambda: VGroup(roda(C_D, R=R_D, ang=ang_d.get_value(), raios=6)))

        self.gat("prende o corpo num eixo")
        self.play(FadeIn(dv), run_time=0.7)

        # Mesma força F empurrando na borda (gira mais), perto do eixo (gira menos) e apontando para o eixo (não gira nada)
        s_borda = seta(C_D + P3(R_D, -1.25), C_D + P3(R_D, -0.05), FC, 6, tip=0.20)
        l_fb = T("F", 38, FC).next_to(s_borda, RIGHT, buff=0.12)
        self.gat("em lugares diferentes")
        self.play(FadeIn(s_borda), FadeIn(l_fb), vel_d.animate.set_value(1.5), run_time=0.8)

        self.gat("girar menos")
        s_perto = seta(C_D + P3(0.45 * R_D, -1.25), C_D + P3(0.45 * R_D, -0.05), FC, 6, tip=0.20)
        self.play(Transform(s_borda, s_perto), l_fb.animate.next_to(s_perto, RIGHT, buff=0.12), vel_d.animate.set_value(0.35), run_time=0.8)

        self.gat("não girar nada")
        s_radial = seta(C_D + P3(R_D + 1.25, 0.0), C_D + P3(R_D + 0.05, 0.0), FC, 6, tip=0.20)
        self.play(Transform(s_borda, s_radial), l_fb.animate.next_to(s_radial, UP, buff=0.12), vel_d.animate.set_value(0.0), run_time=0.8)

        self.gat("o que faz o papel da força")
        B, ib = M(r"\tau", "=", r"\,?", size=58)
        lb = VGroup(B, txt("NA ROTAÇÃO", 28, bold=True)).arrange(RIGHT, buff=0.28)
        self.pilha.poe(lb)
        self.monta(B, ib, {}, rt=0.8)
        self.play(FadeIn(lb[1], shift=0.1 * UP), run_time=0.5)
        self.foco = lb
        self.ate(0.99)

    def icone(self, k):
        if k == 0:
            p = porta2d(P3(-0.75, 0.0), comp=1.55, esp=0.14, ang=0.18)
            sf = seta(p.mac + P3(0.0, -0.65), p.mac + P3(0.0, -0.05), FC, 5, tip=0.16)
            return VGroup(p, sf)
        if k == 1:
            d = DiscoPedacos(ORIGIN, 0.72, nr=3, nt=8)
            ac = seta_curva(ORIGIN, 0.90, 0.25, 1.3, ACC, 5, tip=0.16)
            return VGroup(d, eixo_cruz(ORIGIN, 0.11), ac)
        eng = engrenagens(P3(0.0, 0.22), ang1=0.2, r1=0.26, razao=2, n1=8)
        gan = gangorra(P3(0.0, -0.45), escala=0.38, ang=0.0)
        return VGroup(eng, gan)

    ROT = (("BRAÇO DE", "ALAVANCA"), ("2ª LEI NA", "ROTAÇÃO"), ("POTÊNCIA E", "EQUILÍBRIO"))

    def item(self, k):
        ic = self.icone(k)
        ic.scale(min(1.9 / ic.width, 1.45 / ic.height))
        t = VGroup(*[txt(l, 26) for l in self.ROT[k]]).arrange(DOWN, buff=0.18)
        return VGroup(ic, t).arrange(DOWN, buff=0.35)

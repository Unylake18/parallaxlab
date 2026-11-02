from ptch6 import patch
# ───────── E2 ─────────
patch("sec_e2.py", [
 # #34: no foguete recomposto, v_ex volta para o bocal de baixo
 (r'''        self.play(f3.op.animate.set_value(0.0), FadeOut(cam_l), FadeOut(st1_sep), FadeIn(st1), FadeIn(VGroup(l1, n1, anel)), run_time=0.6)''',
  r'''        self.play(f3.op.animate.set_value(0.0), FadeOut(cam_l), FadeOut(st1_sep), FadeIn(st1), FadeIn(VGroup(l1, n1, anel)),
                  sx.animate.shift(H1 * DOWN), lvx.animate.shift(H1 * DOWN), run_time=0.6)                            # v7 #34: v_ex sob o bocal de baixo'''),
 # #35: as três primeiras linhas entram juntas e R = 4,48 marca o tanque do 2º estágio
 (r'''        self.pilha.poe(L1b, dx=0.4)
        self.gat("meio a meio")
        self.play(FadeIn(L1), FadeIn(L1b), run_time=0.8)                           # a razão entra junto, sem tela parada com uma linha só
        E, ie = M(r"\frac{P+1{,}1\,f_2}{P+0{,}1\,f_2}", "=", r"4{,}48", size=46)
        self.pilha.poe(E)
        self.gat("começa pelo de cima")
        self.play(Indicate(st2, color=WHITE_, scale_factor=1.04), FadeIn(E), run_time=1.0)''',
  r'''        self.pilha.poe(L1b, dx=0.4)
        E, ie = M(r"\frac{P+1{,}1\,f_2}{P+0{,}1\,f_2}", "=", r"4{,}48", size=46)
        self.pilha.poe(E)
        lR = MathTex(r"R=4{,}48", font_size=30)
        lR.move_to(P3(X - W * 0.92 / 2 - 0.15 - lR.width / 2, YB + H1 + 1.7))
        self.gat("meio a meio")
        self.play(FadeIn(L1), FadeIn(L1b), FadeIn(E), run_time=0.8)                # v7 #35: três linhas de uma vez (sem 15 s com duas)
        self.gat("começa pelo de cima")
        self.play(Indicate(st2, color=WHITE_, scale_factor=1.04), FadeIn(lR), run_time=1.0)'''),
 (r'''        self.play(FadeOut(VGroup(l1, l2, n1, n2, lorc, sx, lvx, anel)), run_time=0.4)''', r'''        self.play(FadeOut(VGroup(l1, l2, n1, n2, lorc, sx, lvx, anel, lR)), run_time=0.4)'''),
 # #36: a estrutura não aparece na cena do CONFERE
 (r'''self.play(FadeOut(VGroup(bv, rs, tt_)), FadeOut(st1), FadeOut(st2), FadeIn(um2), FadeIn(ls2), run_time=0.8)
        self.play(ls2.animate.scale(0.02).set_opacity(0), run_time=1.2)                 # a estrutura encolhe até sumir: o foguete volta a ser um estágio só''',
  r'''self.play(FadeOut(VGroup(bv, rs, tt_)), FadeOut(st1), FadeOut(st2), FadeIn(um2), run_time=0.8)
        self.play(Indicate(um2, color=STEEL, scale_factor=1.02), run_time=1.2)          # v7 #36: sem o rótulo ESTRUTURA 0,1 f na cena do CONFERE'''),
 # #37: a DICA cabe numa linha
 (r'''self.dica18("CADA ESTÁGIO, UMA RAZÃO NOVA")''', r'''self.dica18("CADA ESTÁGIO, RAZÃO NOVA")'''),
])
# ───────── E1 ─────────
patch("sec_e1.py", [
 # #28: troca de número por fade (sem morph de dígitos)
 (r'''        self.voa([(l_vx[1][:5], mp(A, ia, [2])), (l_dm[1][:3], mp(A, ia, [4]))], extra=[FadeIn(mp(A, ia, [0, 1, 3]))], rt=1.0, arco_esq=-0.5)''',
  r'''        self.play(FadeIn(mp(A, ia, [0, 1, 2, 3, 4])), Indicate(l_vx[1], color=WHITE_, scale_factor=1.06), Indicate(l_dm[1], color=WHITE_, scale_factor=1.06), run_time=0.9)    # v7 #28'''),
 (r'''        self.voa([(l_m0[1][:6], mp(B, ib, [3]))], extra=[FadeIn(mp(B, ib, [0, 1, 2, 4, 5]))], rt=1.0, arco_esq=-0.5)''',
  r'''        self.play(FadeIn(mp(B, ib, [0, 1, 2, 3, 4, 5])), Indicate(l_m0[1], color=WHITE_, scale_factor=1.06), run_time=0.9)                                              # v7 #28'''),
 # #29: as chamadas saem quando as setas entram
 (r'''        self.play(FadeOut(rel), run_time=0.3)''', r'''        self.play(FadeOut(rel), FadeOut(g_m0), FadeOut(g_p), run_time=0.3)                # v7 #29: as chamadas saem antes das setas de força'''),
])
# ───────── E3 ─────────
patch("sec_e3.py", [
 (r'''self.pilha = Pilha(self, x0=2.0, larg=5.7)''', r'''self.pilha = Pilha(self, x0=2.0, larg=5.2)'''),
 (r'''self.hip([["AREIA CHEGA PARADA NA HORIZONTAL · ESTEIRA A VELOCIDADE CONSTANTE"]], x0=-5.8, wmax=12.0)''', r'''self.hip([["AREIA CHEGA PARADA · ESTEIRA A VELOCIDADE CONSTANTE"]], x0=-5.8, wmax=11.0)'''),
 (r'''A.scale_to_fit_width(min(A.width, 5.65))''', r'''A.scale_to_fit_width(min(A.width, 5.1))'''),
 (r'''F2, if2 = M("=", r"\tfrac12\cdot 20\cdot 1{,}5^2", "=", r"22{,}5\ \mathrm{W}", size=46, cores={3: KC})''', r'''F2, if2 = M("=", r"\tfrac12\cdot 20\cdot 1{,}5^2", "=", r"22{,}5\ \mathrm{W}", size=46, cores={3: KC})
        F2.scale_to_fit_width(min(F2.width, 5.0))                                           # v7 #42: x <= 912 px'''),
 (r'''        Dn = linha_m(txt("PELA EQUAÇÃO GERAL:", 24), M("F", "=", "v", r"\left|\frac{dm}{dt}\right|", size=46, cores={0: FC, 2: VEL})[0], buff=0.15)''',
  r'''        Dn = VGroup(txt("PELA EQUAÇÃO GERAL:", 24), M("F", "=", "v", r"\left|\frac{dm}{dt}\right|", size=46, cores={0: FC, 2: VEL})[0]).arrange(DOWN, buff=0.1, aligned_edge=LEFT)      # v7 #40: duas linhas'''),
 # #39: a seta de reação sai de cima dos roletes (abaixo da esteira)
 (r'''fr = vivo(lambda: VGroup(seta(P3(xp() + 0.7, YT - 0.28), P3(xp() - 0.3, YT - 0.28), FC, 6, tip=0.2, op=op_x())))''',
  r'''fr = vivo(lambda: VGroup(seta(P3(xp() + 0.6, YT - 0.82), P3(xp() - 0.3, YT - 0.82), FC, 6, tip=0.2, op=op_x())))'''),
])
# Pilha: encolhe até 18% antes de avisar (margem direita)
patch("prob2.py", [
 (r'''            if m.width > 1.04 * (self.larg - dx):                    # v2: escala mínima 0,96 (nunca encolher fórmula para caber)''',
  r'''            if m.width > 1.18 * (self.larg - dx):                    # v7: encolhe até 18% (margem direita ≤ 912 px) antes de avisar'''),
])
print("ok")

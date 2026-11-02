from ptch6 import patch
# ───────── T2 (v7 #5–#12, §2.1) ─────────
patch("sec_t2.py", [
 # #5: sem o texto grande; m, v e F_emp ? entram com o foguete
 (r'''        q21 = VGroup(txt("DE ONDE VEM", 36, bold=True), txt("O EMPUXO?", 36, bold=True)).arrange(DOWN, buff=0.14, aligned_edge=LEFT)
        self.pilha.poe(q21)
        self.play(f3.op.animate.set_value(1.0), FadeIn(q21), Kt.animate(rate_func=linear).set_value(6.9), run_time=0.8)''',
  r'''        l21 = VGroup(MathTex("m", font_size=44, color=MAS).move_to(P3(0.2, 0.55)),
                     arrow(P3(1.3, 1.0), P3(2.5, 1.0), VEL, 7, tip=0.22), MathTex("v", font_size=44, color=VEL).move_to(P3(2.95, 1.0)),
                     arrow(P3(-2.6, -1.05), P3(-1.2, -1.05), FC, 7, tip=0.22), MathTex(r"F_{emp}\ ?", font_size=44, color=FC).move_to(P3(-0.35, -1.05)))
        self.play(f3.op.animate.set_value(1.0), FadeIn(l21), Kt.animate(rate_func=linear).set_value(6.9), run_time=0.8)'''),
 # painéis: pilha mais alta na tela (topo -2.0, base -3.8, 3 linhas) e painéis mais compactos
 (r'''self.pilha = Pilha(self, x0=-7.2, topo=-2.31, base=-4.45, larg=14.4)''', r'''self.pilha = Pilha(self, x0=-7.2, topo=-2.0, base=-3.8, larg=14.4, buff=0.18)'''),
 (r'''FT, FB, YC, L_, W_ = 2.35, -1.86, 0.2, 3.2, 0.66''', r'''FT, FB, YC, L_, W_ = 2.35, -1.8, 0.33, 3.2, 0.66'''),
 (r'''sis1 = fronteira(3.8, 2.1, P3(-4.8, YC), rotulo=None)''', r'''sis1 = fronteira(3.8, 1.9, P3(-4.8, YC), rotulo=None)'''),
 (r'''lab_s1.move_to(P3(-6.7 + lab_s1.width / 2, YC + 1.05 + 0.36))''', r'''lab_s1.move_to(P3(-6.7 + lab_s1.width / 2, YC + 0.95 + 0.36))'''),
 (r'''lm1 = MathTex("m", font_size=40, color=MAS).move_to(P3(-4.8, YC + 0.72))''', r'''lm1 = MathTex("m", font_size=40, color=MAS).move_to(P3(-4.8, YC + 0.66))'''),
 (r'''sis2 = fronteira(4.9, 2.1, P3(3.25, YC), rotulo=None)''', r'''sis2 = fronteira(5.2, 1.9, P3(3.1, YC), rotulo=None)'''),
 (r'''lab_s2.move_to(P3(0.8 + lab_s2.width / 2, YC + 1.05 + 0.36))''', r'''lab_s2.move_to(P3(0.55 + lab_s2.width / 2, YC + 0.95 + 0.36))'''),
 (r'''lm2 = MathTex("m+dm", font_size=40, color=MAS).move_to(P3(4.15, YC + 1.05 + 0.34))''', r'''lm2 = MathTex("m+dm", font_size=40, color=MAS).move_to(P3(4.15, YC + 0.95 + 0.34))'''),
 (r'''lg = MathTex("-dm", font_size=40, color=MAS).move_to(P3(1.45, YC + 0.64))''', r'''lg = MathTex("-dm", font_size=40, color=MAS).move_to(P3(1.5, YC + 0.58))'''),
 (r'''Y1, Y2 = -1.2, -1.66''', r'''Y1, Y2 = -1.0, -1.44'''),
 # #6: o painel t + dt não fica vazio: silhueta a 30% e a pergunta
 (r'''        self.troca(velhos, FadeIn(fa), FadeIn(ta), FadeIn(f1), FadeIn(fb), FadeIn(tb), seq=True)''',
  r'''        gh = fog_h(L_, W_, bocal=P3(BX, YC)).set_opacity(0.3)
        gq = VGroup(txt("O QUE MUDA EM", 26, color=DIM), MathTex(r"dt\,?", font_size=40, color=DIM)).arrange(RIGHT, buff=0.14).move_to(P3(3.8, YC + 0.75))
        self.troca(velhos, FadeIn(fa), FadeIn(ta), FadeIn(f1), FadeIn(fb), FadeIn(tb), FadeIn(gh), FadeIn(gq), seq=True)'''),
 (r'''        self.play(FadeIn(f2), run_time=0.5)''', r'''        self.play(FadeIn(f2), FadeOut(gh), FadeOut(gq), run_time=0.5)'''),
])
patch("sec_t2.py", [
 # §2.1: tamanho 40 nas linhas do balanço
 (r'''r"v_{ex}", ")", size=44,
                  cores={1: VEL, 7: VEL, 14: VEL, 16: VEX_C})''', r'''r"v_{ex}", ")", size=40,
                  cores={1: VEL, 7: VEL, 14: VEL, 16: VEX_C})'''),
 (r'''r"v\,dm", "+", r"dm\,dv", size=44, cores={3: VEL})''', r'''r"v\,dm", "+", r"dm\,dv", size=40, cores={3: VEL})'''),
 (r'''"+", r"v_{ex}\,dm", size=44)
        pinta(Bg, ibg, 3''', r'''"+", r"v_{ex}\,dm", size=40)
        pinta(Bg, ibg, 3'''),
 (r'''"+", r"v_{ex}\,dm", size=44, cores={1: VEL, 4: VEL})''', r'''"+", r"v_{ex}\,dm", size=40, cores={1: VEL, 4: VEL})'''),
])
# cancelamentos que fecham a linha no mesmo play
src = open("sec_t2.py", encoding="utf-8").read()
i = src.index("        # cancelamentos: o par acende, é riscado e SAI da linha")
j = src.index('        self.gat("sobra um termo dm vezes dv")')
novo = r'''        # cancelamentos (v7 §2.1): o par pisca em calor, sai e a linha se fecha NO MESMO play (nenhum vão dentro da linha)
        def fecha(src_, isrc, dst, idst, pares, sai, novo=()):
            dst.align_to(src_, LEFT)
            dst.move_to(P3(dst.get_center()[0], src_.get_center()[1]))
            self.play(*[ReplacementTransform(mp(src_, isrc, [a]), mp(dst, idst, [b])) for a, b in pares], *[FadeOut(mp(src_, isrc, [k])) for k in sai],
                      *[FadeIn(mp(dst, idst, [k])) for k in novo], run_time=0.5)
            self.remove(src_)
            self.remove(*[m for m in list(self.mobjects) if m is not dst and isinstance(m, VGroup) and m.get_family()[1:] and all(any(x is y for y in dst.get_family()) for x in m.get_family()[1:])])
            self.add(dst)
            self.pilha.linhas = [((dst if l is src_ else l), d) for l, d in self.pilha.linhas]
        B1, ib1 = M("0", "=", r"m\,dv", "+", r"v\,dm", "+", r"dm\,dv", "-", r"v\,dm", "+", r"v_{ex}\,dm", size=40)
        pinta(B1, ib1, 2, [(1, VEL), (2, VEL)])
        pinta(B1, ib1, 4, [(0, VEL)])
        pinta(B1, ib1, 6, [(2, VEL), (3, VEL)])
        pinta(B1, ib1, 8, [(0, VEL)])
        pinta(B1, ib1, 10, [(0, VEX_C), (1, VEX_C), (2, VEX_C)])
        self.gat("aparece dos dois lados e cancela")
        par1 = VGroup(mp(B, ib, [0, 1]), mp(B, ib, [3, 4]))
        self.play(*[Indicate(x, color=HEAT, scale_factor=1.15) for x in par1], run_time=0.4)
        fecha(B, ib, B1, ib1, [(2, 1), (6, 2), (7, 3), (8, 4), (9, 5), (10, 6), (11, 7), (12, 8), (13, 9), (14, 10)], [0, 1, 3, 4, 5], novo=[0])
        S1, is1 = M("0", "=", r"m\,dv", "+", r"dm\,dv", "+", r"v_{ex}\,dm", size=40)
        pinta(S1, is1, 2, [(1, VEL), (2, VEL)])
        pinta(S1, is1, 4, [(2, VEL), (3, VEL)])
        pinta(S1, is1, 6, [(0, VEX_C), (1, VEX_C), (2, VEX_C)])
        self.gat("os termos com velocidade vezes dm")
        par2 = VGroup(mp(B1, ib1, [4]), mp(B1, ib1, [8]))
        self.play(*[Indicate(x, color=HEAT, scale_factor=1.15) for x in par2], run_time=0.4)
        fecha(B1, ib1, S1, is1, [(0, 0), (1, 1), (2, 2), (3, 3), (6, 4), (9, 5), (10, 6)], [4, 5, 7, 8])
        self.wait(0.8)
'''
src = src[:i] + novo + src[j:]
open("sec_t2.py", "w", encoding="utf-8", newline="\n").write(src)
patch("sec_t2.py", [
 # S1 já está na pilha (no lugar de B): S2 e C com tamanho 40/46
 (r'''S2, is2 = M("0", "=", r"m\,dv", "+", r"v_{ex}\,dm", size=44)
        C, ic = M(r"m\,dv", "=", "-", r"v_{ex}", r"\,dm", size=52, cores={3: VEX_C})''',
  r'''S2, is2 = M("0", "=", r"m\,dv", "+", r"v_{ex}\,dm", size=40)
        C, ic = M(r"m\,dv", "=", "-", r"v_{ex}", r"\,dm", size=48, cores={3: VEX_C})'''),
 # #10: a seta F_emp 10 px acima do casco
 (r'''se = arrow(P3(BX, YC + 0.58), P3(BX + 0.7, YC + 0.58), FC, 7, tip=0.22)''', r'''se = arrow(P3(BX, YC + 0.82), P3(BX + 0.7, YC + 0.82), FC, 7, tip=0.22)'''),
 # #11: unidades ao lado da caixa F_emp, y <= 495 px
 (r'''        U_.move_to(P3(-7.2 + U_.width / 2, -3.95))''', r'''        U_.move_to(P3(-7.2 + U_.width / 2, -3.55))'''),
])
# T2-7 (#12)
patch("sec_t2.py", [
 (r'''a1b.move_to(P3(-7.3 + a1b.width / 2, 0.45))''', r'''a1b.move_to(P3(-7.3 + a1b.width / 2, 0.2))'''),
 (r'''b1 = M(r"u_{rel,x}", "=", "0", size=40, cores={0: VEX_C, 2: VEX_C})[0].move_to(P3(-4.3, -0.75))''', r'''b1 = M(r"u_{rel,x}", "=", "0", size=40, cores={0: VEX_C, 2: VEX_C})[0]
        b1.move_to(P3(-7.35 + b1.width / 2, -3.12))                              # v7 #12: abaixo do carrinho, à esquerda da queda do grão'''),
 (r'''        b1b = VGroup(tx("→ NADA NA", 26), tx("HORIZONTAL", 26)).arrange(DOWN, buff=0.08, aligned_edge=LEFT)
        b1b.move_to(P3(-4.85 - b1b.width / 2, -3.45))''', r'''        b1b = tx("→ NADA NA HORIZONTAL", 22)
        b1b.move_to(P3(-7.35 + b1b.width / 2, -3.58))'''),
])
print("ok")

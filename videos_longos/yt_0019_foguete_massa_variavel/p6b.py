from ptch6 import patch
patch("sec_t3.py", [
 # T3-4: a linha-alvo (mesmo Δv) já na tela enquanto a curva espera a fala
 ('''        ldv = MathTex(r"\Delta v", font_size=40, color=VEL).next_to(g1.pt(TM, vf), RIGHT, buff=0.3)
        self.pilha.limpa(rt=0.7, anims=[FadeOut(self.esq), FadeIn(g1.eixos), FadeIn(marcas_t), FadeIn(c1), FadeIn(c2), FadeIn(t1)])''',
  '''        ldv = MathTex(r"\Delta v", font_size=40, color=VEL).next_to(g1.pt(TM, vf), RIGHT, buff=0.3)
        alvo_ = DashedLine(g1.pt(0, vf), g1.pt(TM, vf), dash_length=0.12).set_stroke(VEL, 2.2, opacity=0.8)
        fml_ = M(r"\Delta v", "=", r"v_{ex}", r"\ln R", size=44, cores={0: VEL, 2: VEX_C})[0].next_to(alvo_, UP, buff=0.22).shift(0.9 * LEFT)
        self.pilha.limpa(rt=0.7, anims=[FadeOut(self.esq), FadeIn(g1.eixos), FadeIn(marcas_t), FadeIn(c1), FadeIn(c2), FadeIn(t1), FadeIn(alvo_), FadeIn(fml_)])'''),
 ("t2.add_updater(lambda m_: m_.move_to(g1.pt(max(TM * k2.get_value(), 40.0), fv(TM)(max(TM * k2.get_value(), 40.0))) + P3(0.55, -0.5)))",
  "t2.add_updater(lambda m_: m_.move_to(g1.pt(max(TM * k2.get_value(), 40.0), fv(TM)(max(TM * k2.get_value(), 40.0))) + P3(-0.1, 0.5)))"),
 # T3-5: a fórmula no canto livre da direita
 ('''        self.troca(velhos, FadeIn(G.eixos), FadeIn(tk), FadeIn(cur), k.animate.set_value(0.2), seq=True)''',
  '''        fml5 = M(r"\Delta v", "/", r"v_{ex}", "=", r"\ln R", size=46, cores={0: VEL, 2: VEX_C})[0].move_to(P3(2.9, -0.3))
        self.troca(velhos, FadeIn(G.eixos), FadeIn(tk), FadeIn(cur), FadeIn(fml5), k.animate.set_value(0.2), seq=True)'''),
 ("self.g35 = VGroup(G.eixos, tk, cur, marcas, xe, lxe)", "self.g35 = VGroup(G.eixos, tk, cur, marcas, xe, lxe, fml5)"),
])

from ptch6 import patch
patch("sec_e3.py", [
 # a pergunta entra junto com a esteira
 (r'''        ev = vivo(esteira)
        self.play(FadeIn(ev), run_time=0.8)''',
  r'''        ev = vivo(esteira)
        q = VGroup(txt("QUE FORÇA FAZ O MOTOR?", 28, bold=True), txt("COM QUE POTÊNCIA?", 28, bold=True)).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        self.pilha.poe(q)
        self.play(FadeIn(ev), FadeIn(q), run_time=0.8)                                    # v6: a pergunta já entra com a esteira'''),
 (r'''        q = VGroup(txt("QUE FORÇA FAZ O MOTOR?", 28, bold=True), txt("COM QUE POTÊNCIA?", 28, bold=True)).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        self.pilha.poe(q)
        self.gat("que força o motor")
        self.play(FadeIn(q), run_time=0.6)
''',
  r'''        self.gat("que força o motor")
        self.play(Indicate(q, color=WHITE_, scale_factor=1.04), run_time=0.6)
'''),
 # HIPÓTESES sem v itálico misturado
 (r'''self.hip([["AREIA CHEGA SEM", MathTex("v", font_size=36, color=VEL), "HORIZONTAL · ESTEIRA EM", MathTex("v", font_size=36, color=VEL), "CONSTANTE"]], x0=-5.8, wmax=12.0)''',
  r'''self.hip([["AREIA CHEGA PARADA NA HORIZONTAL · ESTEIRA A VELOCIDADE CONSTANTE"]], x0=-5.8, wmax=12.0)'''),
 # barras mais longe da margem inferior
 (r'''yb, kb = -3.95, 1.9 / 45.0''', r'''yb, kb = -3.6, 1.9 / 45.0'''),
 (r'''self.referencial("DO CHÃO", pos=2.75)
        self.ref_mob.move_to(P3(-4.25 + self.ref_mob.width / 2, 2.75))''',
  r'''self.referencial("DO CHÃO", pos=3.0)
        self.ref_mob.move_to(P3(-4.25 + self.ref_mob.width / 2, 3.0))'''),
 (r'''selo_ref.move_to(P3(-4.25 + selo_ref.width / 2, 2.75))''', r'''selo_ref.move_to(P3(-4.25 + selo_ref.width / 2, 3.0))'''),
])

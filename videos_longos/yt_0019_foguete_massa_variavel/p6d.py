from ptch6 import patch
patch("sec_e2.py", [
 # estrutura: rótulo longe da aleta
 (r'''MathTex(r"0{,}1\,f", font_size=40)).arrange(RIGHT, buff=0.15).next_to(P3(X + WU / 2, Y0 + 0.75), RIGHT, buff=0.35)
        lPn''',
  r'''MathTex(r"0{,}1\,f", font_size=40)).arrange(RIGHT, buff=0.15).next_to(P3(X + WU / 2, Y0 + 0.75), RIGHT, buff=0.85)
        lPn'''),
 (r'''ls2 = VGroup(txt("ESTRUTURA", 24), MathTex(r"0{,}1\,f", font_size=40)).arrange(RIGHT, buff=0.15).next_to(P3(X + WU / 2, Y0 + 0.75), RIGHT, buff=0.35)''',
  r'''ls2 = VGroup(txt("ESTRUTURA", 24), MathTex(r"0{,}1\,f", font_size=40)).arrange(RIGHT, buff=0.15).next_to(P3(X + WU / 2, Y0 + 0.75), RIGHT, buff=0.85)'''),
 # rótulos dos estágios alinhados na mesma margem esquerda
 (r'''        n2 = txt("2º ESTÁGIO", 24, color=DIM).next_to(l2, UP, buff=0.22).align_to(l2, LEFT)
''',
  r'''        n2 = txt("2º ESTÁGIO", 24, color=DIM).next_to(l2, UP, buff=0.22).align_to(l2, LEFT)
        for m_ in (l1, l2, n1, n2):
            m_.shift((X + W / 2 + 0.85 - m_.get_left()[0]) * RIGHT)         # v6: uma só margem esquerda para os quatro rótulos
'''),
 # 1º estágio depois da separação: sólido e esmaecido (não tracejado)
 (r'''        st1_sep = VGroup(*[DashedVMobject(m_.copy().set_fill(opacity=0), num_dashes=30, dashed_ratio=0.5).set_stroke(GEO, 2.4, opacity=0.4)
                           for m_ in st1.family_members_with_points() if isinstance(m_, VMobject) and m_.get_num_points() > 2 and m_.get_stroke_width() > 0])''',
  r'''        st1_sep = st1.copy().set_opacity(0.4)                                   # v6: sólido e esmaecido, sem tracejado'''),
 # barra e rótulos juntos
 (r'''        self.play(FadeIn(bv), run_time=0.3)
        self.play(mostra.animate.set_value(1.0), run_time=1.6)
        self.play(FadeIn(rs), run_time=0.7)''',
  r'''        self.play(FadeIn(bv), FadeIn(rs), run_time=0.35)                                # v6: a barra entra já com os rótulos
        self.play(mostra.animate.set_value(1.0), run_time=1.6)'''),
 # NESTE MODELO sai do topo e vira o cabeçalho do bloco
 (r'''tt_ = VGroup(rot("1 t DE CARGA", 34), VGroup(''',
  r'''tt_ = VGroup(txt("NESTE MODELO", 24, color=CYAN, bold=True), rot("1 t DE CARGA", 34), VGroup('''),
 (r'''        self.selo("NESTE MODELO", "")
''', ''),
 # 5% O RESTO para a esquerda da barra
 (r'''r95[1].move_to(P3(-1.2 - 0.31 + r95[1].width / 2, -3.0 + 4.6 + 0.3))''', r'''r95[1].move_to(P3(-1.2 - 0.31 - 0.25 - r95[1].width / 2, -3.0 + 4.6 + 0.02))'''),
])

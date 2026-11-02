from ptch6 import patch
# ───────── E2: D1 medidor do ORÇAMENTO (3 blocos de v_ex = 3,0 km/s somando Δv ≈ 9 km/s) ─────────
patch("sec_e2.py", [
 (r'''        self.play(FadeIn(um), FadeIn(q, shift=0.1 * UP), run_time=0.8)                      # a pergunta entra grande logo no início do bloco''',
  r'''        XB = (2.3, 4.2, 6.1)                                                                 # v8 D1: o orçamento vira um medidor, ocupando a metade direita desde o início
        blocos = VGroup(*[RoundedRectangle(corner_radius=0.08, width=1.85, height=0.5).set_fill(VREL, 0.85).set_stroke(VREL, 1.5).move_to(P3(xc, -0.5)) for xc in XB])
        rotb = VGroup(*[VGroup(MathTex(r"v_{ex}=", font_size=30, color=VEX_C), rot("3,0 km/s", 24, VEX_C)).arrange(RIGHT, buff=0.06).move_to(P3(xc, -1.05)) for xc in XB])
        chave = Brace(blocos, UP, buff=0.12, color=VEL)
        tot = VGroup(txt("ORÇAMENTO", 24), MathTex(r"\Delta v\approx", font_size=38, color=VEL), rot("9 km/s", 28, VEL)).arrange(RIGHT, buff=0.1).next_to(chave, UP, buff=0.12)
        lorc = VGroup(blocos, rotb, chave, tot)
        self.play(FadeIn(um), FadeIn(q, shift=0.1 * UP), FadeIn(lorc), run_time=0.8)         # a pergunta entra grande logo no início do bloco'''),
 (r'''        lorc = VGroup(txt("ORÇAMENTO", 24), MathTex(r"\Delta v=", font_size=38, color=VEL), rot("9 km/s", 28, VEL)).arrange(RIGHT, buff=0.1)
        self.pilha.poe(lorc)                                           # v4 #52: o dado do orçamento vira linha da Pilha (não cobre o selo)
''', ''),
 (r'''        self.play(FadeIn(lorc), run_time=0.6)
        self.hip(''', r'''        self.play(Indicate(tot, color=VEL, scale_factor=1.04), run_time=0.6)
        self.hip('''),
 (r'''        self.an("E2-2")
        self.pilha.limpa(rt=0.3)''', r'''        self.an("E2-2")
        self.pilha.limpa(rt=0.3, anims=[FadeOut(lorc)])'''),
])
# ───────── E3: inset do referencial e barras longe da borda de baixo (≥ 60 px) ─────────
patch("sec_e3.py", [
 (r'''cx, cy, Z = -3.2, -3.3, 5.0''', r'''cx, cy, Z = -3.2, -2.95, 5.0'''),
 (r'''RoundedRectangle(corner_radius=0.1, width=8.4, height=1.55).move_to(P3(cx, cy))''', r'''RoundedRectangle(corner_radius=0.1, width=8.4, height=1.1).move_to(P3(cx, cy))'''),
 (r'''g.add(Rectangle(width=8.0, height=0.3).move_to(P3(cx, cy - 0.6))''', r'''g.add(Rectangle(width=8.0, height=0.26).move_to(P3(cx, cy - 0.42))'''),
 (r'''Line(P3(cx + xm, cy - 0.75), P3(cx + xm, cy - 0.45))''', r'''Line(P3(cx + xm, cy - 0.55), P3(cx + xm, cy - 0.29))'''),
 (r'''                    g.add(Dot(P3(cx + xg, cy - 0.3), radius=0.14, color=SAND).set_z_index(5))
                    if a_ > T_ESC:
                        g.add(seta(P3(cx + xg - 0.1, cy + 0.35), P3(cx + xg - 0.1 + VB * 1.3, cy + 0.35), VEL, 6, tip=0.2))''',
  r'''                    g.add(Dot(P3(cx + xg, cy - 0.16), radius=0.14, color=SAND).set_z_index(5))
                    if a_ > T_ESC:
                        g.add(seta(P3(cx + xg - 0.1, cy + 0.28), P3(cx + xg - 0.1 + VB * 1.3, cy + 0.28), VEL, 6, tip=0.2))'''),
 (r'''                    g.add(Line(P3(cx + 2.0, cy - 0.38), P3(cx + xg, cy - 0.38)).set_stroke(HEAT, 7, opacity=0.85))
                if a_ < T_ESC:
                    g.add(seta(P3(cx + xg - 0.1, cy + 0.35), P3(cx + xg - 0.1 - VB * 1.3, cy + 0.35), VEL, 6, tip=0.2))
                g.add(Dot(P3(cx + xg, cy - 0.3), radius=0.14, color=SAND).set_z_index(5))''',
  r'''                    g.add(Line(P3(cx + 2.0, cy - 0.22), P3(cx + xg, cy - 0.22)).set_stroke(HEAT, 7, opacity=0.85))
                if a_ < T_ESC:
                    g.add(seta(P3(cx + xg - 0.1, cy + 0.28), P3(cx + xg - 0.1 - VB * 1.3, cy + 0.28), VEL, 6, tip=0.2))
                g.add(Dot(P3(cx + xg, cy - 0.16), radius=0.14, color=SAND).set_z_index(5))'''),
 (r'''yb, kb = -3.6, 1.9 / 45.0''', r'''yb, kb = -3.5, 1.9 / 45.0'''),
])
# ───────── Síntese: pilha de cartões ≥ 60 px da borda e 25 px do título ─────────
patch("sec_fim.py", [
 (r'''.arrange(DOWN, buff=0.08).move_to(P3(3.4, 3.3))''', r'''.arrange(DOWN, buff=0.08).move_to(P3(3.4, 3.55))'''),
 (r'''c0r = RoundedRectangle(corner_radius=0.12, width=5.6, height=1.4)''', r'''c0r = RoundedRectangle(corner_radius=0.12, width=5.6, height=1.2)'''),
 (r'''        c0r.move_to(P3(3.7, 2.1))''', r'''        c0r.move_to(P3(3.7, 2.2))'''),
 (r'''            cx_, cy_ = 3.7, 2.1''', r'''            cx_, cy_ = 3.7, 2.2'''),
 (r'''        mini_g = VGroup(ejs, cur, dg).shift(P3(0, -0.15))''', r'''        mini_g = VGroup(ejs, cur, dg).shift(P3(0, -0.15)).scale(0.85)'''),
 (r'''        c3 = cartao_(c3, extra=0.5, cor=VEL)''', r'''        c3 = cartao_(c3, extra=0.35, cor=VEL)'''),
 (r'''        c2.move_to(P3(3.7, 1.4 - 0.15 - c2.height / 2))''', r'''        c2.move_to(P3(3.7, 1.6 - 0.15 - c2.height / 2))'''),
])
print("ok")

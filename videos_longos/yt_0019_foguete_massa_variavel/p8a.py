from ptch6 import patch
# ───────── T2 ─────────
patch("sec_t2.py", [
 # #1: o original de "m + dm" sai no mesmo play em que a cópia parte
 (r'''        self.voa([(lm2, mp(A, ia, [4])), (lv2, mp(A, ia, [7]))], extra=[FadeIn(mp(A, ia, [3, 5, 6, 8]))], rt=1.0, origem=False)''',
  r'''        self.voa([(lm2, mp(A, ia, [4])), (lv2, mp(A, ia, [7]))], extra=[FadeIn(mp(A, ia, [3, 5, 6, 8])), FadeOut(lm2), FadeOut(nota)], rt=1.0, origem=False)       # v8 #1: nunca duas cópias de "m+dm"'''),
 # #2: escala e inset longe da borda de baixo (≥ 60 px) e afastados entre si
 (r'''            y_ = -3.15''', r'''            y_ = -2.85'''),
 (r'''rot(f"{n_km} km", 26, color=GEO).move_to(P3(-6.4, -3.5)))''', r'''rot(f"{n_km} km", 26, color=GEO).move_to(P3(-6.4, -3.2)))'''),
 (r'''IX, IY, IW, IH = 5.1, -2.62, 5.0, 2.5''', r'''IX, IY, IW, IH = 5.1, -2.2, 5.0, 2.5'''),
 (r'''txt("FOGUETE FORA DE ESCALA", 24, color=DIM).move_to(P3(-2.6, -3.5))''', r'''txt("FOGUETE FORA DE ESCALA", 24, color=DIM).move_to(P3(-2.6, -3.2))'''),
 # #3: o texto não chega perto da setinha do grão
 (r'''        b1b = tx("→ NADA NA HORIZONTAL", 22)''', r'''        b1b = tx("NADA NA HORIZONTAL", 22)                                           # v8 #3: sem a seta inicial, o texto termina longe da setinha do grão'''),
 # D3: a fronteira do SISTEMA em ciano (cor dos selos)
 (r'''        sis1 = fronteira(3.8, 1.9, P3(-4.8, YC), rotulo=None)''', r'''        sis1 = fronteira(3.8, 1.9, P3(-4.8, YC), rotulo=None)
        sis1[0].set_stroke(CYAN, 2.4, opacity=0.95)                                   # v8 D3'''),
 (r'''        sis2 = fronteira(5.2, 1.9, P3(3.1, YC), rotulo=None)''', r'''        sis2 = fronteira(5.2, 1.9, P3(3.1, YC), rotulo=None)
        sis2[0].set_stroke(CYAN, 2.4, opacity=0.95)'''),
])
# ───────── T3 ─────────
patch("sec_t3.py", [
 # #4: "QUEIMA DE 10 MIN" já na posição final, sem seguir a ponta
 (r'''        def pos_t2(m_):
            pt = g1.pt(max(TM * k2.get_value(), 40.0), fv(TM)(max(TM * k2.get_value(), 40.0)))
            m_.move_to(P3(pt[0] + 0.5, max(pt[1] - 1.1, g1.y0 + 0.62)))
        t2.add_updater(pos_t2)''',
  r'''        pt_fim = g1.pt(TM, fv(TM)(TM))
        t2.move_to(P3(pt_fim[0] + 0.5, pt_fim[1] - 1.1))                               # v8 #4: fixo, onde fica a partir de 8:54'''),
 (r'''        t2.clear_updaters()
''', r'''        pass
'''),
 # #5: o ×e entra depois do arco, já embaixo dele
 (r'''        self.play(Create(xe), FadeIn(lxe), run_time=1.2)''', r'''        self.play(Create(xe), run_time=0.9)
        self.play(FadeIn(lxe), run_time=0.3)                                                # v8 #5: o rótulo só aparece com o arco já desenhado'''),
 # #6: v − v_ex > 0 mais longe do F_emp, e F_emp um pouco mais alto
 (r'''            m_[0].move_to(b + P3(0.55, 0.7))''', r'''            m_[0].move_to(b + P3(0.55, 0.88))'''),
 (r'''.shift(0.55 * LEFT)              # v7 #19: acima do rastro, longe do inset e do F_emp''', r'''.shift(1.0 * LEFT)               # v8 #6: acima do rastro, ≥ 20 px do F_emp'''),
])
# ───────── T4 ─────────
patch("sec_t4.py", [
 # #7: o "mg" fica ao lado da seta enquanto a caixa estiver na tela
 (r'''extra=[FadeIn(mp(A, ia, [5])), FadeOut(lp)], rt=1.0, origem=False, arco_esq=-0.6)          # v7 #21: o original sai enquanto a cópia parte''',
  r'''extra=[FadeIn(mp(A, ia, [5]))], rt=1.0, origem=False, arco_esq=-0.6)          # v8 #7: o rótulo original fica ao lado da seta'''),
])
# ───────── E1 ─────────
patch("sec_e1.py", [
 # #8: FORÇA DO ASSENTO no canto de cima do inset, longe da seta e da pessoa
 (r'''        lF.move_to(P3(PXc - PW / 2 + 0.2, y_s + 0.75), aligned_edge=LEFT)''', r'''        lF.move_to(P3(PXc - PW / 2 + 0.2, y_s + 2.85), aligned_edge=LEFT)'''),
])
# ───────── E2 ─────────
patch("sec_e2.py", [
 # #10: rótulo e seta de v_ex 0,3 u para a direita (fora das aletas)
 (r'''        sx = seta_tr(P3(X + 0.95, Y0 + 0.15), P3(X + 0.95, Y0 - 0.4), VEX_C, 6, tip=0.2)''', r'''        sx = seta_tr(P3(X + 1.3, Y0 + 0.15), P3(X + 1.3, Y0 - 0.4), VEX_C, 6, tip=0.2)'''),
 # #11: R = 4,48 do tamanho dos outros rótulos, violeta, preso ao estágio
 (r'''        lR = MathTex(r"R=4{,}48", font_size=30)
        lR.move_to(P3(X - W * 0.92 / 2 - 0.15 - lR.width / 2, YB + H1 + 1.7))''',
  r'''        lR = MathTex(r"R=4{,}48", font_size=34, color=VEL)
        lR.move_to(P3(X - W * 0.92 / 2 - 0.3 - lR.width / 2, YB + H1 + 1.7))
        lR = VGroup(lR, Line(P3(X - W * 0.92 / 2 - 0.25, YB + H1 + 1.7), P3(X - W * 0.92 / 2 - 0.02, YB + H1 + 1.7)).set_stroke(VEL, 2.4))      # v8 #11'''),
])
print("ok")

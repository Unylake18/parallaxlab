def patch(p, pares):
    s = open(p, encoding='utf-8').read()
    for a, b in pares:
        assert s.count(a) == 1, (p, a[:60], s.count(a))
        s = s.replace(a, b)
    open(p, 'w', encoding='utf-8').write(s)


# F3 · a moldura do painel nasce com a primeira palavra da fórmula
patch('sec_h.py', [
    ('        self.play(Create(pn), run_time=0.5)\n', ''),
    ('        self.pena(t1)\n        self.gat("momento sobre massa")', '        self.pena(t1, extra=[Create(pn)])\n        self.gat("momento sobre massa")'),
])

# F8 · linhas de coordenada na região xy; eixos u, v só no "passo dois"
patch('sec_e1.py', [
    ('        cria_uv(self, E, extra=[Create(sphi)])\n        self.pena(lphi)\n        self.colY = 240\n', '        self.colY = 240\n'),
    ('        self.gat("passo dois")\n        L2, r2 = linha_de(',
     '''        self.gat("Chama x de u")
        lin6 = []
        for x_ in (.5, 1.0, 1.5):
            g_ = curva(v, [(x_, lo(x_)), (x_, hi(x_))], "#FF9440", 2)
            lin6.append(g_)
            self.play(Create(g_), run_time=0.5)
        self.gat("adorou de v")
        for c_ in (1.25, 1.5, 1.75):
            g_ = curva(v, cX(lambda X, c_=c_: c_ + X * X, 0, c_), VAG, 2)
            lin6.append(g_)
            self.play(Create(g_), run_time=0.5)
        self.gat("passo dois")
        cria_uv(self, E, extra=[Create(sphi)])
        self.pena(lphi)
        L2, r2 = linha_de('''),
    ('self.play(FadeOut(sl), *MA.so_linhas(), run_time=0.3)', 'self.play(FadeOut(sl), *[FadeOut(g_) for g_ in lin6], *MA.so_linhas(), run_time=0.3)'),
    ('        sobe_col(self, [A2, A3, A4], y0=220)', '        sobe_col(self, [A2, ra2, A3, A4], y0=220)'),
])

# F5 · régua do E4-4 com nomes e fios-guia
patch('sec_e4.py', [
    ('        lk1 = TC(r"0{,}212", RX + 30, hp_(YH) + 6, 24, "l")\n        self.play(Create(reg), Create(mk1), run_time=0.5)\n        self.pena(lk1)\n',
     '''        lg1 = lin_px([(RX + 10, hp_(YH)), (RX + 50, 835)], GEO, 1.2, z=6)
        lk1 = mixl([("t", "HOMOGÊNEA", GEO), ("m", r"\\ 0{,}212")], RX + 60, 840, 22)
        self.play(Create(reg), Create(mk1), Create(lg1), run_time=0.5)
        self.pena(*lk1.p)
'''),
    ('        lk0 = TC(r"0{,}25", RX - 30, hp_(.25), 24, "r")\n', '        lg0 = lin_px([(RX + 10, hp_(.25)), (RX + 50, 790)], BR, 1.2, z=6)\n        lk0 = mixl([("t", "METADE", BR), ("m", r"\\ 0{,}25")], RX + 60, 795, 22)\n'),
    ('        lk2 = TC(r"0{,}295", RX + 30, hp_(YB) - 10, 24, "l")\n        self.play(Create(mk0), Create(mk2), run_time=0.5)\n        self.pena(lk0, lk2, lag=0.1)\n',
     '''        lg2 = lin_px([(RX + 10, hp_(YB)), (RX + 50, 745)], E2, 1.2, z=6)
        lk2 = mixl([("t", "ρ = k y", E2), ("m", r"\\ 0{,}295")], RX + 60, 750, 22)
        self.play(Create(mk0), Create(mk2), Create(lg0), Create(lg2), run_time=0.5)
        self.pena(*lk0.p, *lk2.p, lag=0.1)
'''),
    ('ej = leg("ESTICA JUNTO"', 'ej = leg("ACHATA JUNTO"'),
])

# F6 · ícones do E5-3 mais à direita
patch('sec_e5.py', [('X, Y = 1370 + i * 200, 930', 'X, Y = 1440 + i * 170, 930')])

# F7 · o tracker chega a b e para
patch('sec_e6.py', [('at.animate.set_value(B * .985), run_time=4.0', 'at.animate.set_value(B * .9995), run_time=4.0')])

# F2 · câmera do toro: afastada, toro inteiro no lado esquerdo
patch('k39.py', [('CAM_TORO = cam_dict((6.4, -11.1, 5.4), (0, 0, .2), (0, 0, 1), 640, 540)', 'CAM_TORO = cam_dict((9.6, -16.7, 7.9), (0, 0, .2), (0, 0, 1), 600, 560)')])
print('ok')

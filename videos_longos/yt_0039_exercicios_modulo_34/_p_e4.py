p = 'sec_e4.py'
s = open(p, encoding='utf-8').read()


def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:70], s.count(a))
    s = s.replace(a, b)


# D14 · o determinante com os sinais antes de abrir
rep('''        self.gat("a b r cosseno ao quadrado")
        L3 = cad(self, L3, [("e2", "="), ("t1", r"\\aa\\bb\\R\\cos^2\\th"), ("p", "+"), ("t2", r"\\aa\\bb\\R\\sen^2\\th")]''',
    '''        self.gat("diagonal menos diagonal")
        L3 = cad(self, L3, [("e1", "="), ("d1", r"\\aa\\cos\\th\\cdot\\bb\\R\\cos\\th-\\left(-\\aa\\R\\sen\\th\\right)\\left(\\bb\\sen\\th\\right)")], [], n=16, nota="D14: diagonal − antidiagonal")
        self.gat("a b r cosseno ao quadrado")
        L3 = cad(self, L3, [("e2", "="), ("t1", r"\\aa\\bb\\R\\cos^2\\th"), ("p", "+"), ("t2", r"\\aa\\bb\\R\\sen^2\\th")]''')

# D15a · ρ · |J| = k r² sen θ / 4 (antes de separar)
rep('''        self.gat("o integrando separa")
        # v2 §5''', '''        P0 = linha(self, [("r", r"\\rr\\cdot|J|"), ("e", "="), ("a", r"\\kk\\cdot\\dfrac{\\R\\sen\\th}{2}\\cdot\\dfrac{\\R}{2}"), ("e2", "="), ("b", r"\\dfrac{\\kk\\R^2\\sen\\th}{4}")], 28, gap=18)
        self.gat("o integrando separa")
        # v2 §5''')
rep('''        self.colY = pxof(sp.get_bottom())[1]
        self.gat("A de téta é a integral do seno")''', '''        self.colY = pxof(sp.get_bottom())[1]
        sobe_col(self, [M1, P0], y0=230)
        self.gat("A de téta é a integral do seno")''')
# D15b · 2k/12 = k/6
rep('''        T3 = cad(self, T3, [("e", "="), ("r", r"\\Me{\\dfrac{\\kk}{6}}")], [("^p", "r")], n=17, nota="m = k/6")''',
    '''        T3 = cad(self, T3, [("e", "="), ("r", r"\\dfrac{2\\kk}{12}")], [("^p", "r")], n=17, nota="D15: k/4 · 2 · 1/3 = 2k/12")
        T3 = cad(self, T3, [("e", "="), ("r", r"\\Me{\\dfrac{\\kk}{6}}")], [("^r", "r")], n=17, nota="m = k/6")''')

# D16a · y · ρ · |J|
rep('''        self.gat("os números viram um oitavo")
        iN2 = len(self.colms)''', '''        Nz = linha(self, [("a", r"y\\,\\rr\\,|J|"), ("e", "="), ("b", r"\\dfrac{\\R\\sen\\th}{2}\\cdot\\kk\\dfrac{\\R\\sen\\th}{2}\\cdot\\dfrac{\\R}{2}"), ("e2", "="), ("c", r"\\dfrac{\\kk\\R^3\\sen^2\\th}{8}")], 28, gap=18)
        self.gat("os números viram um oitavo")
        iN2 = len(self.colms)''')
# D16b · 3π/32 ≈ 9,425/32 ≈ 0,295
rep('''        Y2 = cad(self, Y2, [("e", "="), ("r", r"\\Me{\\dfrac{3\\pi}{32}\\approx 0{,}295}")], [("^r", "r")], n=19, nota="= 3π/32 ≈ 0,295")''',
    '''        Y2 = cad(self, Y2, [("e", "="), ("r", r"\\dfrac{3\\pi}{32}")], [("^r", "r")], n=19, nota="= 3π/32")
        Y2 = cad(self, Y2, [("e", r"\\approx"), ("n", r"\\dfrac{9{,}425}{32}"), ("e2", r"\\approx"), ("r", r"\\Me{0{,}295}")], [], n=19, desce=True, nota="D16: ≈ 9,425/32 ≈ 0,295")''')

# D17 · k/2 · (√(1−x²)/2)²
rep('''        self.gat("o quadrado da raiz")
        C2 = cad(self, C2, [("e", "="), ("d", r"\\kk\\cdot\\dfrac12\\cdot\\dfrac{1-x^2}{4}")], [("^c", "d")], n=20, nota="G(topo) − G(0)")''',
    '''        self.gat("aplicado no topo")
        C2 = cad(self, C2, [("e", "="), ("d0", r"\\dfrac{\\kk}{2}\\left(\\dfrac{\\sqrt{1-x^2}}{2}\\right)^{2}")], [("^c", "d0")], n=20, nota="D17: G(topo) − G(0)")
        self.gat("o quadrado da raiz")
        C2 = cad(self, C2, [("e", "="), ("d", r"\\kk\\cdot\\dfrac12\\cdot\\dfrac{1-x^2}{4}")], [("^d0", "d")], n=20, nota="(√(1−x²)/2)² = (1−x²)/4")''')

# D18 · régua vertical do centro de massa
rep('''        self.gat("quatro b sobre três pi")
        H1, rh = linha(''', '''        self.gat("quatro b sobre três pi")
        RX = 1050
        hp_ = lambda h_: v.px(0, h_)[1]
        reg = lin_px([(RX, hp_(0)), (RX, hp_(.5))], GEO, 2, z=6)
        mk1 = lin_px([(RX - 9, hp_(YH)), (RX + 9, hp_(YH))], GEO, 3, z=7)
        lk1 = TC(r"0{,}212", RX + 16, hp_(YH) + 6, 24, "l")
        self.play(Create(reg), Create(mk1), run_time=0.5)
        self.pena(lk1)
        H1, rh = linha(''')
rep('''        self.gat("a densidade que cresce")
        st = seta_px(''', '''        self.gat("a densidade que cresce")
        mk0 = lin_px([(RX - 9, hp_(.25)), (RX + 9, hp_(.25))], BR, 1.5, dash=(4, 4), z=7)
        lk0 = TC(r"0{,}25", RX - 16, hp_(.25), 24, "r")
        mk2 = lin_px([(RX - 9, hp_(YB)), (RX + 9, hp_(YB))], E2, 3, z=7)
        lk2 = TC(r"0{,}295", RX + 16, hp_(YB) - 8, 24, "l")
        self.play(Create(mk0), Create(mk2), run_time=0.5)
        self.pena(lk0, lk2, lag=0.1)
        Pc = linha(self, [("a", r"\\rr=\\kk\\,y:"), ("b", r"\\dfrac{3\\pi}{32}\\approx 0{,}295")], 32, gap=26)
        st = seta_px(''')
open(p, 'w', encoding='utf-8').write(s)
print('ok')

p = 'sec_e2.py'
s = open(p, encoding='utf-8').read()


def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:70], s.count(a))
    s = s.replace(a, b)


# frases das entradas da matriz (v3.1)
rep('(("é ípsilon em relação", 0), ("em relação a ípsilon xis", 1), ("é menos ípsilon sobre xis ao quadrado", 2), ("um sobre xis o determinante", 3))',
    '(("u derivado em x dá y", 0), ("em y dá x", 1), ("dá menos y sobre x ao quadrado", 2), ("em y dá um sobre x", 3))')

# D7 · de onde saem x = √(u/v) e y = √(uv)
rep('''        self.gat("então x é raiz")
        P2b = LL(''', '''        self.gat("o x some")
        M1 = linha(self, [("a", r"\\U\\V"), ("e", "="), ("b", r"xy\\cdot\\dfrac{y}{x}"), ("e2", "="), ("r", r"y^2")], 30, gap=16)
        self.gat("o y some")
        M2 = linha(self, [("a", r"\\dfrac{\\U}{\\V}"), ("e", "="), ("b", r"xy\\div\\dfrac{y}{x}"), ("e2", "="), ("r", r"x^2")], 30, gap=16)
        self.gat("então x é raiz")
        P2b = LL(''')
rep('''        self.gat("Vai o atalho")
''', '''        self.gat("Vai o atalho")
        sobe_col(self, [P1, s1, M1, M2], y0=200)
''')

# D8 · y/x = v
rep('''        D1 = cad(self, D1, [("e", "="), ("r", r"2\\V")], [("^r", "r")], n=7, nota="o y/x vira v: = 2v")
''', '''        D1 = cad(self, D1, [("e", "="), ("r", r"2\\V")], [("^r", "r")], n=7, nota="o y/x vira v: = 2v")
        Dv = linha(self, [("a", r"\\dfrac{y}{x}"), ("e", "="), ("b", r"\\V")], 30, gap=14)
''')

# D9 · tabela dos quatro cantos, diagonais e área da pipa
rep('''        self.play(FadeIn(pts), Create(pipa), run_time=0.8)
        self.pena(*cl, lag=0.05)
''', '''        self.play(FadeIn(pts), Create(pipa), run_time=0.8)
        self.pena(*cl, lag=0.05)
        TT = [linha(self, [t_], 30, gap=14) for t_ in (r"(1,1)\\to(1,1)", r"(1,2)\\to\\left(\\dfrac{1}{\\sqrt2},\\sqrt2\\right)", r"(2,1)\\to(\\sqrt2,\\sqrt2)", r"(2,2)\\to(1,2)")]
''')
rep('''        self.pena(n1)
        self.gat("a outra um sobre raiz de dois")''', '''        self.pena(n1)
        Dg1 = linha(self, [("a", r"2-1"), ("e", "="), ("r", "1")], 30, gap=14)
        self.gat("a outra um sobre raiz de dois")''')
rep('''        self.pena(n2)
        self.gat("diagonal vezes diagonal")
        Pp, rp = linha(self, [("e", "="), ("f", r"\\dfrac{1\\cdot\\dfrac{1}{\\sqrt2}}{2}")], 36, rot="PIPA", rot_cor=GEO, escreve=False, y=330)''',
    '''        self.pena(n2)
        Dg2 = linha(self, [("a", r"\\sqrt2-\\dfrac{1}{\\sqrt2}"), ("e", "="), ("b", r"\\dfrac{2-1}{\\sqrt2}"), ("e2", "="), ("r", r"\\dfrac{1}{\\sqrt2}")], 30, gap=14)
        self.gat("diagonal vezes diagonal")
        sobe_col(self, TT, y0=250)
        Pp, rp = linha(self, [("e", "="), ("f", r"\\dfrac{1\\cdot\\dfrac{1}{\\sqrt2}}{2}")], 36, rot="PIPA", rot_cor=GEO, escreve=False)''')
rep('''        Pp = cad(self, Pp, [("e", "="), ("r", r"\\dfrac{\\sqrt2}{4}\\approx 0{,}354")], [("^f", "r")], n=9, nota="PIPA = √2/4 ≈ 0,354")''',
    '''        Pp = cad(self, Pp, [("e", "="), ("m", r"\\dfrac{1}{2\\sqrt2}")], [("^f", "m")], n=9, nota="D9: 1/(2√2)")
        Pp = cad(self, Pp, [("e2", "="), ("r", r"\\dfrac{\\sqrt2}{4}\\approx 0{,}354")], [("^m", "r")], n=9, nota="PIPA = √2/4 ≈ 0,354")''')

# D11 · degraus da integral de dentro e de fora
rep('''        self.gat("subtração de frações")
        D3 = cad(''', '''        self.gat("aplica de um a dois")
        D3 = cad(self, D3, [("e", "="), ("f", r"\\dfrac{1}{2\\V}"), ("p", r"\\left(\\dfrac{2^2}{2}-\\dfrac{1^2}{2}\\right)")], [("^f", "f"), ("^c", "p")], n=10, nota="D11: u²/2 em 2 e em 1")
        self.gat("subtração de frações")
        D3 = cad(''')
rep('''        F4 = cad(self, F4, [("e", "="), ("h", r"\\dfrac{3}{4}"), ("p", r"(\\ln 2-0)")], [("^h", "h"), ("^c", "p")], n=10, nota="(ln 2 − 0)")''',
    '''        F4 = cad(self, F4, [("e", "="), ("h", r"\\dfrac{3}{4}"), ("p", r"(\\ln 2-\\ln 1)")], [("^h", "h"), ("^c", "p")], n=10, nota="D11: (ln 2 − ln 1)")
        F4 = cad(self, F4, [("e2", "="), ("h", r"\\dfrac{3}{4}"), ("p", r"(\\ln 2-0)")], [("^h", "h"), ("^p", "p")], n=10, desce=True, nota="(ln 2 − 0)")''')
open(p, 'w', encoding='utf-8').write(s)
print('ok')

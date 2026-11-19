p = 'sec_e3.py'
s = open(p, encoding='utf-8').read()


def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:70], s.count(a))
    s = s.replace(a, b)


# D12 · a² − x² − y² = a² − (x² + y²) = a² − r²
rep('''        self.gat("e o integrando fica")
        th = ValueTracker(0.0)''', '''        self.gat("e o integrando fica")
        A1b = linha(self, [("a", r"a^2-x^2-y^2"), ("e", "="), ("b", r"a^2-(x^2+y^2)"), ("e2", "="), ("r", r"a^2-\\R^2")], 30, gap=16)
        th = ValueTracker(0.0)''')

# D13 · 1/2 · 2/3 = 2/6 = 1/3
rep('''        self.gat("a ao cubo sobre três")
        B1 = cad(self, B1, [("e", "="), ("r", r"\\dfrac{a^3}{3}")], [("^h", "r"), ("^t", "r"), ("^p", "r")], n=14, nota="= a³/3")''',
    '''        self.gat("a ao cubo sobre três")
        B1 = cad(self, B1, [("e", "="), ("h", r"\\dfrac12"), ("c", r"\\cdot"), ("t", r"\\dfrac23"), ("a3", r"a^3")], [("^h", "h"), ("^t", "t")], n=14, nota="D13: (a²)^{3/2} = a³")
        B1 = cad(self, B1, [("e", "="), ("r", r"\\dfrac{2a^3}{6}")], [("^h", "r"), ("^t", "r"), ("^a3", "r")], n=14, nota="D13: 1/2 · 2/3 = 2/6")
        B1 = cad(self, B1, [("e", "="), ("r", r"\\dfrac{a^3}{3}")], [("^r", "r")], n=14, nota="= a³/3")''')
open(p, 'w', encoding='utf-8').write(s)
print('ok')

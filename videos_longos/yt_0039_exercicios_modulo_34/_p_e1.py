import sys
p = 'sec_e1.py'
s = open(p, encoding='utf-8').read()


def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:70], s.count(a))
    s = s.replace(a, b)


# frases das bordas (narração v3.1)
rep('("ípsilon igual a um mais", c1', '("y igual a um mais", c1')
rep('("ípsilon igual a dois mais", c2', '("a de dois mais x ao quadrado vira", c2')
rep('("xis igual a zero vira", e0', '("x igual a zero vira", e0')
rep('("xis mais xis ao quadrado vira", c3', '("x mais x ao quadrado vira", c3')

# D1 · o rascunho na placa
rep('''        tv1 = placa_t("TRAVA", *v.px(.5, 2.55), AL, 28, "c")
        self.pena(tv1)
''', '''        tv1 = placa_t("TRAVA", *v.px(.5, 2.55), AL, 28, "c")
        self.pena(tv1)
        # D1: o rascunho da substituição t = y − x² e o selo (degraus escritos a caneta na fala que segue)
        R1 = linha(self, [("t", "t"), ("e", "="), ("y", r"y-x^2"), ("q", r"\\ ,\\ "), ("d", "dt"), ("e2", "="), ("dy", "dy")], 30, gap=14)
        R2 = linha(self, [("i", r"\\int"), ("f", r"\\dfrac{e^{t}}{t}"), ("d", r"\\,dt")], 30, gap=14)
        slo = palavra(self, "SEM PRIMITIVA ELEMENTAR", AL, 26, gap=18)
''')
rep('''        tira(self, Ti)

        # ═══ E1-2''', '''        tira(self, Ti, R1, R2, slo)

        # ═══ E1-2''')

# D2 · o determinante: o par 0·2u acende e vira 0
rep('''        degrau(self, "C1a", "J = 1·1 − 0·2u")
''', '''        degrau(self, "C1a", "J = 1·1 − 0·2u")
        self.leitura(G(L4, ix_(L4, "b", "c2", "cc")), rt=0.9)
        Z0 = linha(self, [("z", r"0\\cdot 2\\U"), ("e", "="), ("r", "0")], 34, gap=18, voos=[(G(L4, ix_(L4, "b", "c2", "cc")), "z")])
''')

# D3 · cada borda em três linhas em cadeia (y = … → y − x² = … → v = …)
a0 = s.index('            Lb0 = linha(self, [("l", ltx)], 36, escreve=False, gap=22)')
a1 = s.index('            segs += [sg, lb]')
novo = '''            if segs:
                limpa_col(self, keep=())
                self.colY = 240
            Lb0 = linha(self, [("l", ltx)], 36, escreve=False, gap=22)
            fonte = lab.f if lab is not None else hl
            voos(self, [(fonte.copy(), parte(Lb0, ix_(Lb0, "l"), "esq"))], rt=0.9)
            il = ix_(Lb0, "l")
            src_ = Lb0
            if ltx.startswith("y"):
                mid = {r"y=1+x^2": r"y-x^2=1", r"y=2+x^2": r"y-x^2=2", r"y=x+x^2": r"y-x^2=x"}[ltx]
                Lm = linha(self, [("l", mid)], 36, escreve=False, gap=22)
                im = ix_(Lm, "l")
                gmap(self, 2, Lb0, Lm, [([il[0]], [im[0]]), ([il[3]], [im[1]]), ([il[4], il[5]], [im[2], im[3]]), ([il[1]], [im[4]]), ([il[2]], [im[5]])],
                     rt=1.2, copia=True, nota=f"D3: {ltx} → {mid} (o x² atravessa a igualdade)")
                src_ = Lm
                il = im
            Lb = linha(self, [("r", rtx)], 36, escreve=False, gap=22)
            ir_ = ix_(Lb, "r")
            if ltx.startswith("y"):
                pares = [(il[:4], [ir_[0]]), ([il[4]], [ir_[1]]), ([il[5]], [ir_[2]])]
            else:
                pares = [([il[0]], [ir_[0]]), ([il[1]], [ir_[1]]), ([il[2]], [ir_[2]])]
            gmap(self, 2, src_, Lb, pares, rt=1.3, copia=True, nota=f"D3: {ltx} → {rtx}")
            sg = lin_px([u.px(*p) for p in seg], cor, 4, z=6)
            q = u.px(*pl)
            lb = TP(rtx, q[0] + dl[0], q[1] + dl[1], 26, "c")
            self.play(Create(sg), run_time=0.6)                       # v2 A11: a borda nova acende no trapézio (sem voo atravessando o palco)
            voos(self, [(G(Lb, ix_(Lb, "r")).copy(), lb)], rt=0.8)
'''
s = s[:a0] + novo + s[a1:]

# D4 · aproximações numéricas em dois degraus
rep('''        F2 = cad(self, F1, [("e", "="), ("r", r"\\Me{e^2-e\\approx 4{,}67}")], [("^d", "r")], n=4, desce=True, nota="C1c: = e² − e ≈ 4,67")''',
    '''        F2a = cad(self, F1, [("e", r"\\approx"), ("n", r"7{,}389-2{,}718")], [], n=4, desce=True, nota="D4: e² ≈ 7,389 e e ≈ 2,718")
        F2 = cad(self, F2a, [("e", "="), ("r", r"\\Me{4{,}671}")], [("^n", "r")], n=4, nota="D4: = 4,671")''')

# D5 · conta do colchete com MMC visível
rep('''        A5 = linha(self, [("e", "="), ("a", r"\\big[x\\big]_0^1")''', '''        sobe_col(self, [A2, A3, A4], y0=220)                                # D5: o que já virou resultado sai; a conta nova sobe
        A5 = linha(self, [("e", "="), ("a", r"\\big[x\\big]_0^1")''')
rep('''        self.gat("um mais um meio")
        A7 = linha_de(self, A6, [("e", "="), ("a", "1"), ("p", "+"), ("b", r"\\dfrac{1}{2}"), ("e2", "="), ("r", r"\\dfrac{3}{2}")], [("e", "e"), ("a", "a"), ("p", "p"), ("b", "b")],
                      n=5, size=30, gap=16, x=pxof(A3.get_left())[0], nota="C1d: 1 + 1/2 = 3/2")
        degrau(self, "C1d", "= 1 + 1/2 = 3/2")''', '''        B1 = linha(self, [("a", r"2-\\dfrac12"), ("e", "="), ("b", r"\\dfrac42-\\dfrac12"), ("e2", "="), ("r", r"\\dfrac32")], 30, gap=14, x=pxof(A3.get_left())[0])
        B2 = linha(self, [("a", r"2-\\dfrac32"), ("e", "="), ("b", r"\\dfrac42-\\dfrac32"), ("e2", "="), ("r", r"\\dfrac12")], 30, gap=14, x=pxof(A3.get_left())[0])
        degrau(self, "D5", "2 − 1/2 = 4/2 − 1/2 = 3/2; 2 − 3/2 = 4/2 − 3/2 = 1/2")
        self.gat("um mais um meio")
        A7 = linha(self, [("e", "="), ("a", "1"), ("p", "+"), ("b", r"\\dfrac{1}{2}"), ("e2", "="), ("a2", r"\\dfrac22"), ("p2", "+"), ("b2", r"\\dfrac12")], 30, gap=14,
                   x=pxof(A3.get_left())[0])
        A7 = cad(self, A7, [("e3", "="), ("r", r"\\dfrac{3}{2}")], [("^a2", "r"), ("^b2", "r")], n=5, desce=True, nota="D5: 1 + 1/2 = 2/2 + 1/2 = 3/2")
        degrau(self, "D5", "= 1 + 1/2 = 2/2 + 1/2 = 3/2")''')
open(p, 'w', encoding='utf-8').write(s)
print('ok')

p = 'sec_e6.py'
s = open(p, encoding='utf-8').read()


def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:70], s.count(a))
    s = s.replace(a, b)


# C11 · a chave b − a (pisca uma vez no gatilho "cancela") e a leitura numérica do centroide
rep('''        self.gat("o b menos a cancela")
        iF4 = len(self.colms)''', '''        self.gat("o b menos a cancela")
        kc_ = chave_h(v.px(1.0, 0)[0], v.px(B, 0)[0], v.px(0, -.44)[1], GEO, 2)
        lc_ = TP(r"b-a", (v.px(1.0, 0)[0] + v.px(B, 0)[0]) / 2, v.px(0, -.62)[1], 28, "c")
        self.play(Create(kc_), run_time=0.4)
        self.pena(lc_)
        gba = VGroup(kc_, lc_)
        self.play(gba.animate.scale(1.15), run_time=0.3)
        self.play(gba.animate.scale(1 / 1.15), run_time=0.3)
        iF4 = len(self.colms)''')
rep('''        sobe_col(self, self.colms[:iF4], y0=230)                       # v2 §4.1: fica só o ȳ fatorado; os limites entram embaixo
        self.play(at.animate.set_value(0.0), run_time=2.0)''', '''        sobe_col(self, self.colms[:iF4], y0=230)                       # v2 §4.1: fica só o ȳ fatorado; os limites entram embaixo
        self.play(FadeOut(gba), run_time=0.3)
        self.remove(gba)
        # C11: o ponto do centroide percorre o eixo continuamente; a leitura (uma casa fixa na vírgula) acompanha o tracker
        lido = always_redraw(lambda: TC(r"\\yb\\approx " + f"{yb_f(at.get_value()) / B:.2f}".replace(".", "{,}") + r"\\,b", 1500, 960, 32, "l"))
        self.add(lido)
        self.play(at.animate.set_value(0.0), run_time=3.0)''')
rep('''        self.play(at.animate.set_value(B * .985), run_time=2.6)''', '''        self.play(at.animate.set_value(B * .985), run_time=4.0)''')
# D23 · a = b dá 0/0: usa a forma simplificada
rep('''        Z2 = linha(self, [("a", r"a=b:\\ \\dfrac{4\\cdot 3b^2}{3\\pi\\cdot 2b}"), ("e", "="), ("r", r"\\dfrac{2b}{\\pi}\\approx 0{,}64\\,b")], 32, gap=22)''',
    '''        Za = linha(self, [("a", r"a=b:\\ \\dfrac{b^3-a^3}{b^2-a^2}"), ("e", r"\\to"), ("r", r"\\Al{\\dfrac{0}{0}}")], 30, gap=18)
        sem = palavra(self, "SEM ÁREA", AL, 26, gap=14)
        Zb = linha(self, [("a", r"\\lim_{a\\to b}\\dfrac{4(a^2+ab+b^2)}{3\\pi(a+b)}")], 30, gap=18)
        Z2 = linha(self, [("e", "="), ("a", r"\\dfrac{4\\cdot 3b^2}{3\\pi\\cdot 2b}"), ("e2", "="), ("m", r"\\dfrac{12b^2}{6\\pi b}"), ("e3", "="), ("r", r"\\dfrac{2b}{\\pi}\\approx 0{,}64\\,b")], 30, gap=18)''')
rep('''        ch_.clear_updaters()
        pcv.clear_updaters()
        self._fecha(antes=0.6)''', '''        ch_.clear_updaters()
        pcv.clear_updaters()
        self.play(FadeOut(lido), run_time=0.3)
        self.remove(lido)
        self._fecha(antes=0.6)''')
# D21 · prova da diferença de cubos (depois das duas fatorações)
rep('''        F3 = linha(self, [("a", r"b^2-a^2=(b-a)(a+b)")], 30, gap=14)
''', '''        F3 = linha(self, [("a", r"b^2-a^2=(b-a)(a+b)")], 30, gap=14)
        Pr = linha(self, [("l", r"(b-a)(a^2+ab+b^2)"), ("e", "="), ("p1", r"a^2b"), ("p2", r"+ab^2"), ("p3", r"+b^3"), ("n3", r"-a^3"), ("n1", r"-a^2b"), ("n2", r"-ab^2")], 26, gap=14)
        cancela(self, G(Pr, ix_(Pr, "p1")), G(Pr, ix_(Pr, "n1")))
        cancela(self, G(Pr, ix_(Pr, "p2")), G(Pr, ix_(Pr, "n2")))
        Pr = cad(self, Pr, [("e2", "="), ("r", r"b^3-a^3")], [("p3", "r"), ("n3", "r")], n=24, desce=True, nota="D21: a²b e ab² cancelam: b³ − a³")
''')
# C12 · a moldura nasce junto da primeira linha
rep('''        self.play(Create(pl), run_time=0.4)
        self.pena(parte(T1, ix_(T1, "v", "e", "cam"), "2π·2"))''', '''        self.pena(parte(T1, ix_(T1, "v", "e", "cam"), "2π·2"), extra=[Create(pl)])''')
# D22 · 4π² com o π² numérico
rep('''        T1 = cad(self, T1, [("e2", "="), ("r", r"\\Me{4\\pi^2\\approx 39{,}5}")], [("cam", "r"), ("ar", "r")], n=0, wrap=1840, nota="C6e: 4π² ≈ 39,5")''',
    '''        T1 = cad(self, T1, [("e2", "="), ("r", r"4\\pi^2")], [("cam", "r"), ("ar", "r")], n=0, wrap=1840, nota="C6e: 4π²")
        T1 = cad(self, T1, [("e3", r"\\approx"), ("n", r"4\\cdot 9{,}870=39{,}48")], [], n=0, wrap=1840, desce=True, nota="D22: π² ≈ 9,870")
        T1 = cad(self, T1, [("e4", r"\\approx"), ("r", r"\\Me{39{,}5}")], [("^n", "r")], n=0, wrap=1840, nota="C6e: ≈ 39,5")''')
open(p, 'w', encoding='utf-8').write(s)
print('ok')

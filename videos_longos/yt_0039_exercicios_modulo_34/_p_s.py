p = 'sec_s.py'
s = open(p, encoding='utf-8').read()


def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:70], s.count(a))
    s = s.replace(a, b)


rep('"um esquecer o jacobiano"', '"esquecer o jacobiano"')
rep('"dois usar o jacobiano"', '"sem módulo"')
rep('"três escrever os limites"', '"sem desenhar"')
rep('"quatro no centro de massa"', '"dividir pela área"')
rep('"cinco usar pappus"', '"usar pappus com chapa"')
rep('self.gat("e a meia arruela homogênea")', 'self.gat("E a meia arruela")')
rep('self.gat("resumindo os cinco erros")\n        Y0, DY = 300, 125\n        for i, (e, cor_, fr) in enumerate(erros):\n            self.gat(fr)\n            Y = Y0 + i * DY\n            cx = cruz_px(150, Y, AL, .9)\n',
    'self.gat("resumindo")\n        Y0, DY = 300, 125\n        # C13: as cinco cruzes nascem já na primeira palavra (a tela nunca fica só com o título); cada linha nasce no seu gatilho\n'
    '        cxs = [cruz_px(150, Y0 + i_ * DY, AL, .9) for i_ in range(5)]\n'
    '        for c_ in cxs:\n            self.play(Create(c_), run_time=0.25)\n'
    '        for i, (e, cor_, fr) in enumerate(erros):\n            self.gat(fr)\n            Y = Y0 + i * DY\n            cx = cxs[i]\n')
rep('            self.play(Create(cx), run_time=0.3)\n            self.pena(te)', '            self.pena(te)')
# C14 · rótulo Δx Δy Δz fora do cubo, com fio-guia
rep('''        lcx = TP(r"\\Delta x\\,\\Delta y\\,\\Delta z", cb[1][0] + 36, (cb[1][1] + cb[2][1]) / 2, 28, "l")
        self.play(FadeIn(caixa), run_time=0.4)
        self.pena(lcx)''', '''        lcx = TP(r"\\Delta x\\,\\Delta y\\,\\Delta z", 300, (cb[1][1] + cb[2][1]) / 2, 28, "r")
        fio_c = lin_px([(308, (cb[1][1] + cb[2][1]) / 2), (cb[0][0] - 8, (cb[1][1] + cb[2][1]) / 2)], GEO, 1.3, z=8)
        fio_c.set_stroke(opacity=.8)
        self.play(FadeIn(caixa), Create(fio_c), run_time=0.4)
        self.pena(lcx)''')
open(p, 'w', encoding='utf-8').write(s)
print('ok')

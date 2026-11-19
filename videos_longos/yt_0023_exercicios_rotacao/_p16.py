"""E1b no esquema 2.5D (E1-12, E1-15, E1-16, E1-17) + helper chamada_em + fio até a borda quando o bloco sai de quadro."""
def edit(P, pares):
    s = open(P, encoding='utf-8').read()
    for a, b in pares:
        assert s.count(a) == 1, (P, s.count(a), a[:100])
        s = s.replace(a, b)
    open(P, 'w', encoding='utf-8').write(s)


edit('pecas23.py', [
    ('''    if bloco and yb - BLOCO_L / 2 > Y_FUNDO - 0.4:''', '''    if bloco and cord and yb - BLOCO_L / 2 <= Y_FUNDO - 0.4:                 # o bloco saiu de quadro: o fio segue até a borda de baixo
        g.add(Line([xt, o[1], 0], [xt, -4.2, 0]).set_stroke(HALO, 6).set_z_index(4.8), Line([xt, o[1], 0], [xt, -4.2, 0]).set_stroke("#D8E2F5", 2.6).set_z_index(4.9))
    if bloco and yb - BLOCO_L / 2 > Y_FUNDO - 0.4:'''),
])

edit('sec_e1a.py', [
    ('''class LoteE1a(Lote23, VolanteMix):''', '''def chamada_em(p, rot, pos, cor=GEO):
    """Chamada com o rótulo centrado exatamente em `pos` (posição fixa fora da peça), linha fina até `p`."""
    v = np.asarray(pos, float) - np.asarray(p, float)
    d = float(np.linalg.norm(v))
    return chamada(p, rot, v / max(d, 1e-6), d, cor=cor)


class LoteE1a(Lote23, VolanteMix):'''),
])

edit('sec_e1b.py', [
    ('from sec_e1a import ITENS, item_mob, chamada\n', 'from sec_e1a import ITENS, item_mob, chamada, chamada_em\n'),
    ('''        self.play(vt["K"].animate.set_value(5.0), vt["yc"].animate.set_value(0.2), vt["alvo_x"].animate.set_value(0.0), run_time=1.0)
        o_ = self.v_eixo()''', '''        S12, C12 = 4.6, P3(-4.3, 0.3)                    # v5 §1.1: esquema 2.5D frontal do volante já girado (θ de t = 1,5 s)
        self.modo25(C12, S12)
        r12 = self.rig25_vivo()
        self.play(f3.op.animate.set_value(0.0), FadeIn(r12), run_time=1.0)
        o_ = self.v_eixo()'''),
    ('''        self.pilha.limpa(anims=[FadeOut(borda)])
        self.play(f3.op.animate.set_value(0.0), run_time=0.35)
        vt["K"].set_value(KQ)''', '''        self.pilha.limpa(anims=[FadeOut(borda)])
        self.play(FadeOut(r12), run_time=0.35)
        self.modo25(None)
        vt["K"].set_value(KQ)'''),
    ('''        self.play(vt["K"].animate.set_value(4.6), vt["yc"].animate.set_value(-0.2), vt["alvo_x"].animate.set_value(-0.6 / 4.6), run_time=0.8)
        self.gat("o fio se solta")''', '''        S15, C15 = 4.3, P3(-3.6, -0.1)                   # v5 §1.1: esquema 2.5D vivo (volante, tambor, fio, bloco e pastilha)
        self.modo25(C15, S15)
        self.v_flags["cord"] = True
        r15 = self.rig25_vivo()
        self.play(f3.op.animate.set_value(0.0), FadeIn(r15), run_time=0.8)
        self.gat("o fio se solta")'''),
    ('''        mu_ = chamada(self.vp((-0.08, -0.04, 0.43)), lbl(r"\\mu_c=0{,}40", WHITE_, 42), LEFT + 0.25 * DOWN, 2.6)''',
     '''        mu_ = chamada_em(self.vp((-0.08, -0.04, 0.43)), lbl(r"\\mu_c=0{,}40", WHITE_, 42), P3(-6.1, 2.3))'''),
    ('''        r2c = chamada(self.vp((-0.28, -0.04, -0.28)), lbl(r"R_2=0{,}40\\ \\mathrm{m}", GEO, 40), LEFT + 0.3 * DOWN, 2.2)
        self.play(FadeIn(r2c), run_time=0.4)''', '''        pR2 = self.vp((-0.28, -0.04, -0.28))
        r2c = chamada_em(pR2, lbl(r"R_2=0{,}40\\ \\mathrm{m}", C_RAIO, 40), P3(-5.9, -2.4), cor=C_RAIO)
        r2h = VGroup(circ_raio(self.v_eixo(), 0.40 * S15, C_RAIO, 4.5, tracejado=False), linha_halo(self.v_eixo(), pR2, cor=C_RAIO, w=4.5))
        self.play(FadeIn(r2c), FadeIn(r2h), run_time=0.4)'''),
    ('''        self.pilha.so(f4b, anims=[FadeOut(r2c), FadeOut(mu_)])''', '''        self.pilha.so(f4b, anims=[FadeOut(r2c), FadeOut(r2h), FadeOut(mu_)])'''),
    ('''        self.play(f3.op.animate.set_value(0.0), run_time=0.4)
        self.v_flags.update(freio=False, cord=True, dois=True)''', '''        self.play(FadeOut(r15), run_time=0.4)
        self.v_flags.update(freio=False, cord=True, dois=True)'''),
    ('''        self.play(f3.op.animate.set_value(1.0), run_time=0.5)
        self.gat("todos num aro fino")''', '''        S17, C17 = 2.8, P3(-5.0, 1.75)                   # v5 §1.1: dois volantes lado a lado no esquema 2.5D (o aro fino à direita)
        self.modo25(C17, S17)
        r17 = self.rig25_vivo()
        self.play(FadeIn(r17), run_time=0.5)
        self.gat("todos num aro fino")'''),
    ('''        self.play(FadeOut(setas), FadeOut(la_v), f3.op.animate.set_value(0.0), run_time=0.4)''', '''        self.play(FadeOut(setas), FadeOut(la_v), FadeOut(r17), run_time=0.4)'''),
    ('''        self.play(f3.op.animate.set_value(1.0), FadeIn(self._tr), FadeIn(self._tr_ok), run_time=0.4)
        self.tr_ok(5)''', '''        self.play(FadeIn(r17), FadeIn(self._tr), FadeIn(self._tr_ok), run_time=0.4)
        self.tr_ok(5)'''),
    ('''            self._rt_lbl = chamada(p, lbl(r"r=0{,}15\\ \\mathrm{m}", GEO, 40), LEFT + 0.2 * UP, 2.2)''', '''            self._rt_lbl = chamada(p, lbl(r"r=0{,}15\\ \\mathrm{m}", C_RAIO, 40), LEFT + 0.2 * UP, 2.2, cor=C_RAIO)'''),
])
print('ok')

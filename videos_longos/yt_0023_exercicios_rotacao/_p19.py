"""E1-1 volta ao tour 3D (v5 §1.2): closes em 3D com pílulas na coluna; o match cut para o 2.5D acontece no fim do tour (E1-3 abre o esquema)."""
def edit(P, pares):
    s = open(P, encoding='utf-8').read()
    for a, b in pares:
        assert s.count(a) == 1, (P, s.count(a), a[:100])
        s = s.replace(a, b)
    open(P, 'w', encoding='utf-8').write(s)

i0 = open('sec_e1a.py', encoding='utf-8').read()
a1 = i0.index('        v25_1, hl = None, None\n')
a2 = i0.index('            linha_ = VGroup(*pcs)') if False else None
edit('sec_e1a.py', [
    ('''        v25_1, hl = None, None
        for fr, nome, *vals, alvo in dados:
            self.gat(fr)
            self.v_flags["foco"] = nome.lower() if nome != "BLOCO" else ""
            if nome in ("ANEL", "CUBO", "DISCOS"):
                if v25_1 is None:                                            # match cut: o volante 3D vira o esquema 2.5D no mesmo lugar
                    v25_1 = volante25(C25, S25)
                    self.play(f3.op.animate.set_value(0.0), FadeIn(v25_1), run_time=0.7)
            else:
                if v25_1 is not None:
                    self.play(FadeOut(v25_1), f3.op.animate.set_value(1.0), run_time=0.6)
                    v25_1 = None
                pl = planos[nome]
                self.plano_v(f"E1-1 CLOSE {nome}", pl[0], pl[1], pl[2], pl[3], pl[4], pl[5], pl[6], rt=1.2)
''', '''        for fr, nome, *vals, alvo in dados:
            self.gat(fr)
            self.v_flags["foco"] = nome.lower() if nome != "BLOCO" else ""
            pl = planos[nome]
            self.plano_v(f"E1-1 CLOSE {nome}", pl[0], pl[1], pl[2], pl[3], pl[4], pl[5], pl[6], rt=1.2)
'''),
    ('''            hl = None
            if nome == "ANEL":
                p = C25 + 0.35 * S25 * np.array([math.cos(-0.5), math.sin(-0.5), 0.0])
                hl = VGroup(Annulus(inner_radius=0.30 * S25, outer_radius=0.40 * S25).move_to(C25).set_fill(C_RAIO, 0.18).set_stroke(width=0).set_z_index(5),
                            circ_raio(C25, 0.40 * S25, C_RAIO, 4.5, tracejado=False), circ_raio(C25, 0.30 * S25, C_RAIO_MENOR, 4.5, tracejado=True))
            elif nome == "CUBO":
                p = C25 + 0.10 * S25 * np.array([math.cos(0.9), math.sin(0.9), 0.0])
                hl = VGroup(circ_raio(C25, 0.10 * S25, C_RAIO, 4.5, tracejado=False), linha_halo(C25, p, cor=C_RAIO, w=4.5))
            elif nome == "DISCOS":
                p = C25 + 0.25 * S25 * RIGHT
                hl = VGroup(*[circ_raio(C25 + sx_ * 0.25 * S25 * RIGHT, 0.05 * S25, C_RAIO, 4.5, tracejado=False) for sx_ in (1, -1)], linha_halo(C25, p, cor=C_RAIO, w=4.5))
            elif alvo is None:''', '''            if alvo is None:'''),
    ('''            self.play(Create(ch), FadeIn(linha_, shift=0.08 * RIGHT), *([FadeIn(hl)] if hl is not None else []), run_time=0.7)
            self.play(FadeOut(ch), run_time=0.3)
            if hl is not None:
                self.play(FadeOut(hl), run_time=0.3)
''', '''            self.play(Create(ch), FadeIn(linha_, shift=0.08 * RIGHT), run_time=0.7)
            self.play(FadeOut(ch), run_time=0.3)
'''),
    ('''        if v25_1 is not None:
            self.play(FadeOut(v25_1), f3.op.animate.set_value(1.0), run_time=0.6)
        self.geral_v(rt=1.2)''', '''        self.geral_v(rt=1.2)'''),
])
print('ok')

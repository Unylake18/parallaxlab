"""sec_e1a: E1-1 em match cut 2.5D (anel, cubo, discos com raios lima/magenta) e E1-6..E1-10 no esquema 2.5D vivo."""
def edit(P, pares):
    s = open(P, encoding='utf-8').read()
    for a, b in pares:
        assert s.count(a) == 1, (s.count(a), a[:100])
        s = s.replace(a, b)
    open(P, 'w', encoding='utf-8').write(s)


edit('sec_e1a.py', [
    ('''        vt = self.vt
        self.play(f3.op.animate.set_value(1.0), run_time=0.5)
''', '''        vt = self.vt
        S25, C25 = 5.4, P3(-4.55, 0.1)         # v5 §1.1: esquema 2.5D frontal (u/m e centro); anel de 4,3 u de diâmetro (≥ 55% da altura útil)
        self.play(f3.op.animate.set_value(1.0), run_time=0.5)
'''),
    ('''        for fr, nome, *vals, alvo in dados:
            self.gat(fr)
            self.v_flags["foco"] = nome.lower() if nome != "BLOCO" else ""
            pl = planos[nome]
            self.plano_v(f"E1-1 CLOSE {nome}", pl[0], pl[1], pl[2], pl[3], pl[4], pl[5], pl[6], rt=1.2)
''', '''        v25_1, hl = None, None
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
'''),
    ('''            if alvo is None:
                p = self.v_bloco()
            else:
                th = vt["th"].get_value()
                x, y, z = alvo
                p = self.vp((x * math.cos(th) + z * math.sin(th), y, -x * math.sin(th) + z * math.cos(th)))
            ch = VGroup(Dot(p, radius=0.06, color=GEO_CL), linha_halo(p, linha_.get_left() + 0.12 * LEFT, cor=GEO_CL, w=2.0)).set_z_index(9)
            self.play(Create(ch), FadeIn(linha_, shift=0.08 * RIGHT), run_time=0.7)
            self.play(FadeOut(ch), run_time=0.3)
''', '''            hl = None
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
            elif alvo is None:
                p = self.v_bloco()
            else:
                th = vt["th"].get_value()
                x, y, z = alvo
                p = self.vp((x * math.cos(th) + z * math.sin(th), y, -x * math.sin(th) + z * math.cos(th)))
            ch = VGroup(Dot(p, radius=0.06, color=GEO_CL), linha_halo(p, linha_.get_left() + 0.12 * LEFT, cor=GEO_CL, w=2.0)).set_z_index(9)
            self.play(Create(ch), FadeIn(linha_, shift=0.08 * RIGHT), *([FadeIn(hl)] if hl is not None else []), run_time=0.7)
            self.play(FadeOut(ch), run_time=0.3)
            if hl is not None:
                self.play(FadeOut(hl), run_time=0.3)
'''),
    ('''        self.gat("o bloco é solto do repouso")
        self.v_flags["foco"] = ""
        self.geral_v(rt=1.2)''', '''        self.gat("o bloco é solto do repouso")
        self.v_flags["foco"] = ""
        if v25_1 is not None:
            self.play(FadeOut(v25_1), f3.op.animate.set_value(1.0), run_time=0.6)
        self.geral_v(rt=1.2)'''),
    ('''        S25, C25 = 5.0, P3(-4.4, -0.1)         # v5 §1.1: esquema 2.5D frontal; escala (u/m) e centro; diâmetro 4,0 u (≥ 55% da altura útil)
''', ''),
    # E1-6: o esquema 2.5D vivo no lugar do 3D (match cut)
    ('''        self.play(vt["u"].animate.set_value(1.0), vt["K"].animate.set_value(5.1), vt["yc"].animate.set_value(1.0), vt["th"].animate.set_value(0.0), vt["wov"].animate.set_value(0.0), run_time=1.6)
        self.gat("separa os corpos")''', '''        vt["th"].set_value(0.0)
        self.v_flags.update(foco="", cord=True)
        S6, C6 = 4.3, P3(-4.55, 0.6)                    # v5 §1.1: volante 2.5D com tambor, fio e bloco; anel de 3,4 u (≥ 55% da altura útil)
        self.modo25(C6, S6)
        r25 = self.rig25_vivo()
        self.play(f3.op.animate.set_value(0.0), FadeIn(r25), run_time=1.0)
        self.gat("separa os corpos")'''),
])
print('ok')

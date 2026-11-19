"""Lote PE1a (v2): E1-1 a E1-10 — o volante (Three.js, garfo + eixo único). Álgebra do zero (v2 §2): cada item abre com a lei geral
literal, especializa com voos do desenho, manipula por glyph map (termo que se move, riscos nos cancelamentos) e só no fim os números,
cada um voando do seu rótulo."""
from pecas23 import *  # noqa: F401,F403

ITENS = (("A", r"I"), ("B", r"a,\alpha,T"), ("C", r"t"), ("D", r"K"), ("E", "FREIO"), ("F", "ARO"))


def item_mob(c):
    return txt(c, 30) if c.isupper() else T(c, 38)


def chamada(p, rot, lado=RIGHT, d=1.2, cor=GEO):
    """Rótulo FORA da peça em PÍLULA (fundo PANEL, texto clareado) com chamada clara sobre halo escuro até o ponto `p` (v3 §3).
    Estrutura mantida: [0] = fundo (pílula + linha), [1] = ponto, [2] = rótulo."""
    corp = GEO_CL if cor == GEO else cor
    if cor == GEO:
        rot.set_color(GEO_CL)
    rot.move_to(p + d * lado).set_z_index(17)
    a = rot.get_edge_center(-lado) + 0.08 * (-lado)
    ch = linha_halo(a, p, cor=corp, w=2.0)
    fundo = VGroup(pilula(rot, cor), ch)
    return VGroup(fundo, Dot(p, radius=0.05, color=corp).set_z_index(16), rot).set_z_index(16)


def chamada_em(p, rot, pos, cor=GEO):
    """Chamada com o rótulo centrado exatamente em `pos` (posição fixa fora da peça), linha fina até `p`."""
    v = np.asarray(pos, float) - np.asarray(p, float)
    d = float(np.linalg.norm(v))
    return chamada(p, rot, v / max(d, 1e-6), d, cor=cor)


class LoteE1a(Lote23, VolanteMix):
    def corpo(self):
        f3 = self.volante3d(u0=0.0, K0=4.8, yc0=0.75, op=0.0)
        vt = self.vt
        S25, C25 = 5.4, P3(-4.55, 0.1)         # v5 §1.1: esquema 2.5D frontal (u/m e centro); anel de 4,3 u de diâmetro (≥ 55% da altura útil)
        self.play(f3.op.animate.set_value(1.0), run_time=0.5)

        # ── E1-1: o volante e os dados, cada um com chamada para a peça ──
        self.an("E1-1")
        self.secao("EXERCÍCIO 1 · O VOLANTE")
        self.play(vt["th"].animate.set_value(0.6), run_time=2.0, rate_func=smooth)
        dados = [
            ("um anel grosso de quinze quilos", "ANEL", (r"15\ \mathrm{kg}", MAS), (r"R_1=0{,}30\ \mathrm{m}", C_RAIO_MENOR), (r"R_2=0{,}40\ \mathrm{m}", C_RAIO), (-0.35, 0, 0.0)),
            ("um cubo central", "CUBO", (r"3{,}0\ \mathrm{kg}", MAS), (r"0{,}10\ \mathrm{m}", C_RAIO), None, (0.0, -0.04, 0.0)),
            ("e dois discos pequenos", "DISCOS", (r"2\times 1{,}0\ \mathrm{kg}", MAS), (r"0{,}05\ \mathrm{m}", C_RAIO), (r"\text{a }0{,}25\ \mathrm{m}", C_RAIO), (0.25, -0.03, 0.0)),
            ("tem um tambor leve", "TAMBOR", (r"r=0{,}15\ \mathrm{m}", C_RAIO), None, None, (0.0, -0.11, 0.13)),
            ("segura um bloco de dez quilos", "BLOCO", (r"m=10\ \mathrm{kg}", MAS), None, None, None),
        ]
        self.dados = {}
        planos = {"ANEL": (-40.0, 10.0, 4.3, -3.3, 0.0, 0.0, 0.0), "CUBO": (-50.0, 8.0, 8.5, -3.85, -0.5, 0.0, 0.0),
                  "DISCOS": (-35.0, 8.0, 6.2, -3.85, -0.2, 0.0, 0.0), "TAMBOR": (-55.0, 10.0, 8.0, -3.85, 0.15, 0.0, -0.05), "BLOCO": (-60.0, 12.0, 4.4, -3.85, 0.35, 0.0, -0.22)}
        for fr, nome, *vals, alvo in dados:
            self.gat(fr)
            self.v_flags["foco"] = nome.lower() if nome != "BLOCO" else ""
            self.v_flags["cord"] = nome == "BLOCO"                   # v5 OBJETO CORTADO: nos closes o fio e o bloco saem (o bloco saía cortado pela borda de baixo)
            pl = planos[nome]
            self.plano_v(f"E1-1 CLOSE {nome}", pl[0], pl[1], pl[2], pl[3], pl[4], pl[5], pl[6], rt=1.2)
            pcs = [txt(nome + ":", 30, bold=True, color=GEO)] + [lbl(v[0], v[1], 40) for v in vals if v]
            linha_ = VGroup(*pcs).arrange(RIGHT, buff=0.22)
            if linha_.width > 6.0:
                linha_.scale_to_fit_width(6.0)
            self.pilha.poe(linha_)
            if alvo is None:
                p = self.v_bloco()
            else:
                th = vt["th"].get_value()
                x, y, z = alvo
                p = self.vp((x * math.cos(th) + z * math.sin(th), y, -x * math.sin(th) + z * math.cos(th)))
            ch = VGroup(Dot(p, radius=0.06, color=GEO_CL), linha_halo(p, linha_.get_left() + 0.12 * LEFT, cor=GEO_CL, w=2.0)).set_z_index(9)
            self.play(Create(ch), FadeIn(linha_, shift=0.08 * RIGHT), run_time=0.7)
            self.play(FadeOut(ch), run_time=0.3)
            self.dados[nome] = linha_
        self.gat("solto do repouso")
        self.v_flags["foco"] = ""
        self.v_flags["cord"] = True
        self.geral_v(rt=1.2)
        tr = self.trilha([(a, item_mob(b)) for a, b in ITENS])
        self.play(FadeIn(tr), run_time=0.6)
        self.ate(0.99)

        # ── E1-2: o que pede (lista) e hipóteses ──
        self.an("E1-2")
        self.selo("O QUE ESTE PEDE", "SEIS ITENS")
        self.pilha.limpa()
        pedidos = [("o momento de inércia do volante", "A", [lbl("I", MAS, 42), txt("DO VOLANTE", 30)]),
                   ("a aceleração do bloco e a tração", "B", [lbl(r"a,\ \alpha", ACC, 42), txt("E", 30), lbl("T", FC, 42)]),
                   ("quanto tudo gira", "C", [txt("O GIRO EM", 30), lbl(r"1{,}5\ \mathrm{s}", WHITE_, 42)]),
                   ("para onde vai a energia", "D", [txt("PARA ONDE VAI A ENERGIA", 30)]),
                   ("quando um freio entra em ação", "E", [txt("O FREIO", 30)])]
        for k, (fr, letra, pcs) in enumerate(pedidos):
            self.gat(fr)
            l_ = VGroup(txt(letra, 34, bold=True, color=CYAN), *pcs).arrange(RIGHT, buff=0.2)
            self.pilha.poe(l_)
            self.play(FadeIn(l_, shift=0.08 * UP), run_time=0.5)
        l_ = VGroup(txt("F", 34, bold=True, color=CYAN), txt("UM ARO NO LUGAR DO VOLANTE", 30)).arrange(RIGHT, buff=0.2)
        self.pilha.poe(l_)
        self.play(FadeIn(l_, shift=0.08 * UP), run_time=0.5)
        self.gat("hipóteses")
        self.hip("EIXO SEM ATRITO · FIO LEVE, SEM ESTICAR · RAIOS E TAMBOR SEM MASSA")
        self.gat("nove vírgula oito metros")
        gl_ = VGroup(lbl("g", ACC, 46), lbl("=", WHITE_, 46), lbl(r"9{,}8\ \mathrm{m/s^2}", ACC, 46)).arrange(RIGHT, buff=0.14)
        self.pilha.poe(gl_)
        self.play(FadeIn(gl_, shift=0.08 * UP), run_time=0.5)
        self.g_val = gl_[2]
        self.ate(0.99)

        # ── E1-3: item a — I = Σ Iᵢ (linha-mãe) e o anel como disco cheio menos disco ──
        self.an("E1-3")
        self.sem_selo()
        self.pilha.limpa()
        self.tr_acende(0)
        mae, imae, maeb = self.linha(("I", "=", r"\sum", "I_i"), rt=0.8)
        self.v_flags["foco"] = "anel"
        self.v_flags["cord"] = False
        v25 = volante25(C25, S25)
        self.play(f3.op.animate.set_value(0.0), FadeIn(v25), run_time=0.8)
        self.gat("um disco cheio de quarenta centímetros")
        disco_l = Circle(radius=0.40 * S25).move_to(C25).set_fill(C_RAIO, 0.2).set_stroke(width=0).set_z_index(5)
        c2_ = circ_raio(C25, 0.40 * S25, C_RAIO, 4.5, tracejado=False)
        self.play(FadeIn(disco_l), FadeIn(c2_), run_time=0.8)
        self.gat("menos um disco de trinta")
        fatia = Circle(radius=0.30 * S25).move_to(C25).set_fill(C_RAIO_MENOR, 0.30).set_stroke(width=0).set_z_index(5.5)
        c1_ = circ_raio(C25, 0.30 * S25, C_RAIO_MENOR, 4.5, tracejado=True)
        self.play(FadeIn(fatia), FadeIn(c1_), run_time=0.7)
        tint_ = Annulus(inner_radius=0.30 * S25, outer_radius=0.40 * S25).move_to(C25).set_fill(C_RAIO, 0.18).set_stroke(width=0).set_z_index(5)
        self.play(fatia.animate.scale(1.18).set_fill(opacity=0.0), FadeOut(disco_l), FadeIn(tint_), run_time=1.0)
        rim2 = C25 + 0.40 * S25 * np.array([math.cos(0.35), math.sin(0.35), 0.0])
        rim1 = C25 + 0.30 * S25 * np.array([math.cos(-0.5), math.sin(-0.5), 0.0])
        pM = C25 + 0.35 * S25 * DOWN
        r_lbl = VGroup(chamada(rim1, lbl(r"R_1=0{,}30\ \mathrm{m}", C_RAIO_MENOR, 40), RIGHT, -1.1 - rim1[0], cor=C_RAIO_MENOR),
                       chamada(rim2, lbl(r"R_2=0{,}40\ \mathrm{m}", C_RAIO, 40), RIGHT, -1.1 - rim2[0], cor=C_RAIO),
                       chamada(pM, lbl(r"M=15\ \mathrm{kg}", MAS, 42), DOWN, 0.9, cor=MAS))
        circ_ = VGroup(c2_, c1_, tint_, fatia, linha_halo(C25, rim2, cor=C_RAIO, w=4.5), linha_halo(C25, rim1, cor=C_RAIO_MENOR, w=4.5))
        self.play(FadeIn(r_lbl), run_time=0.6)
        self.gat("os dois têm a mesma densidade por área")
        A, ia, _ = self.linha({"pre": (r"\sigma", "="), "num": ("M",), "den": (r"\pi", r"(R_2^2-R_1^2)")}, voos={2: r_lbl[2][2]}, size=46, rt=1.2)
        self.gat("o momento de inércia de um disco é metade")
        B, ib, _ = self.linha(("I_{anel}", "=", r"\tfrac{1}{2}", r"\sigma", r"\pi", "R_2^4", "-", r"\tfrac{1}{2}", r"\sigma", r"\pi", "R_1^4"),
                              voos={3: mp(A, ia, [0]), 8: mp(A, ia, [0])}, size=46, rt=1.6)
        self.gat("faz a subtração coloca em evidência")
        C_, ic, _ = self.passo23(B, ib, ("I_{anel}", "=", r"\tfrac{1}{2}", r"\sigma", r"\pi", r"(R_2^2-R_1^2)", r"(R_2^2+R_1^2)"),
                                 [((0,), (0,)), ((1,), (1,)), ((2, 7), (2,)), ((3, 8), (3,)), ((4, 9), (4,)), ((5, 6, 10), (5, 6))], size=46, rt=1.4)
        chave = Brace(mp(C_, ic, [3, 4, 5]), DOWN, buff=0.06, color=MAS)
        l_ch = lbl("M", MAS, 40).next_to(chave, DOWN, buff=0.06)
        self.play(GrowFromCenter(chave), FadeIn(l_ch), run_time=0.6)
        self.gat("metade da massa do anel vezes a soma")
        D_, id_, db = self.passo23(C_, ic, ("I_{anel}", "=", r"\tfrac{1}{2}", "M", r"(R_1^2+R_2^2)"),
                                  [((0,), (0,)), ((1,), (1,)), ((2,), (2,)), ((3, 4, 5), (3,)), ((6,), (4,))], size=48, rt=1.2, caixa_cor=MAS)
        self.play(FadeOut(chave), FadeOut(l_ch), run_time=0.3)
        self.gat("metade de quinze")
        self.pilha.so(maeb, db)
        E_, ie, _ = self.linha(("I_{anel}", "=", r"\tfrac{1}{2}", r"\cdot", "15", r"\cdot", r"(0{,}30^2", "+", r"0{,}40^2)"),
                               voos={4: r_lbl[2][2], 6: r_lbl[0][2], 8: r_lbl[1][2]}, cores={4: MAS, 6: C_RAIO_MENOR, 8: C_RAIO}, size=46, rt=1.6)
        self.gat("dá um vírgula oito sete cinco")
        F_, if_, fb = self.gm(E_, ie, ("I_{anel}", "=", r"1{,}875", r"\ \mathrm{kg\,m^2}"), cores={2: MAS}, caixa_cor=MAS, rt=1.0)
        self.foco = F_
        self.ate(0.99)

        # ── E1-4: confere (limites) + cubo (disco cheio) e discos (eixos paralelos) ──
        self.an("E1-4")
        self.selo("CONFERE", [[lbl(r"R_1\to 0", C_RAIO_MENOR, 36), "·", lbl(r"\tfrac12 MR^2", MAS, 36), "(DISCO)"], [lbl(r"R_1\to R_2", C_RAIO_MENOR, 36), "·", lbl(r"MR^2", MAS, 36), "(ARO)"]])
        self.pilha.so(maeb, fb)
        self.gat("se o furo some")
        L1, il1, _ = self.linha((r"R_1\to 0", r":\ ", r"\tfrac{1}{2}", "M", "R_2^2"), size=46, rt=0.9)
        self.gat("se o anel afina")
        L2, il2, _ = self.linha((r"R_1\to R_2", r":\ ", "M", "R_2^2"), size=46, rt=0.9)
        self.gat("agora o cubo")
        self.pilha.so(maeb, fb, anims=[FadeOut(r_lbl), FadeOut(circ_)])
        self.v_flags["foco"] = "cubo"
        self.v_flags["cord"] = True
        pcb = C25 + 0.10 * S25 * np.array([math.cos(0.9), math.sin(0.9), 0.0])
        cb_ = chamada(pcb, VGroup(lbl(r"M=3{,}0\ \mathrm{kg}", MAS, 40), lbl(r"r=0{,}10\ \mathrm{m}", C_RAIO, 40)).arrange(DOWN, buff=0.12, aligned_edge=LEFT), RIGHT, -0.8 - pcb[0], cor=C_RAIO)
        circ_cb = VGroup(circ_raio(C25, 0.10 * S25, C_RAIO, 4.5, tracejado=False), linha_halo(C25, pcb, cor=C_RAIO, w=4.5))
        self.play(FadeIn(cb_), FadeIn(circ_cb), run_time=0.5)
        G0, ig0, _ = self.linha(("I_{cubo}", "=", r"\tfrac{1}{2}", "M", "r^2"), size=46, rt=0.9)
        G1, ig1, _ = self.gm(G0, ig0, ("I_{cubo}", "=", r"\tfrac{1}{2}", r"\cdot", r"3{,}0", r"\cdot", r"0{,}10^2"), sai=[3, 4],
                             voos={4: cb_[2][0], 6: cb_[2][1]}, cores={4: MAS, 6: C_RAIO}, rt=1.2)
        G_, ig, gb = self.gm(G1, ig1, ("I_{cubo}", "=", r"0{,}015\ \mathrm{kg\,m^2}"), cores={2: MAS}, caixa_cor=MAS, rt=0.9)
        self.gat("e os discos pequenos")
        self.pilha.so(maeb, fb, gb, anims=[FadeOut(cb_), FadeOut(circ_cb)])
        self.v_flags["foco"] = "discos"
        pc = C25 + 0.25 * S25 * RIGHT + 0.05 * S25 * UP
        cota = chamada(pc, lbl(r"D=0{,}25\ \mathrm{m}", C_RAIO, 40), RIGHT, -1.2 - pc[0] + 0.0, cor=C_RAIO)
        pdk = C25 - 0.25 * S25 * RIGHT + 0.05 * S25 * DOWN
        dk_ = chamada(pdk, VGroup(lbl(r"m=1{,}0\ \mathrm{kg}", MAS, 40), lbl(r"r=0{,}05\ \mathrm{m}", C_RAIO, 40)).arrange(DOWN, buff=0.12, aligned_edge=RIGHT), DOWN, pdk[1] + 2.75, cor=C_RAIO)
        circ_dk = VGroup(*[circ_raio(C25 + sx_ * 0.25 * S25 * RIGHT, 0.05 * S25, C_RAIO, 4.5, tracejado=False) for sx_ in (1, -1)], linha_halo(C25, C25 + 0.25 * S25 * RIGHT, cor=C_RAIO, w=4.5))
        self.play(FadeIn(cota), FadeIn(dk_), FadeIn(circ_dk), run_time=0.7)
        S0, is0, _ = self.lei("steiner", ("I", "=", r"I_{cm}", "+", "M", "D^2"), rt=0.9)
        self.gat("cada um tem metade de um quilo")
        H0, ih0, _ = self.gm(S0, is0, ("I_{disco}", "=", r"\tfrac{1}{2}", "m", "r^2", "+", "m", "D^2"), mapas=[([0], [0]), ([2], [2, 3, 4]), ([4], [6])], rt=1.1)
        H_, ih, _ = self.gm(H0, ih0, ("I_{disco}", "=", r"\tfrac{1}{2}", r"\cdot", r"1{,}0", r"\cdot", r"0{,}05^2", "+", r"1{,}0", r"\cdot", r"0{,}25^2"),
                            sai=[3, 4, 6, 7], voos={4: dk_[2][0], 6: dk_[2][1], 8: dk_[2][0], 10: cota[2]}, cores={4: MAS, 6: C_RAIO, 8: MAS, 10: C_RAIO}, size=46, rt=1.6)
        self.gat("os dois juntos")
        H2, ih2, _ = self.gm(H_, ih, ("I_{disco}", "=", r"0{,}06375"), cores={2: MAS}, rt=0.9)
        K_, ik, kb = self.gm(H2, ih2, ("2", "I_{disco}", "=", r"0{,}1275", r"\ \mathrm{kg\,m^2}"), mapas=[([2], [3])], cores={3: MAS}, caixa_cor=MAS, rt=1.0)
        self.ate(0.99)

        # ── E1-5: a linha-mãe vira a soma; as três caixas voam; composição (barras) e o termo M D² ──
        self.an("E1-5")
        self.sem_selo()
        self.v_flags["foco"] = ""
        self.v_flags["foco"] = ""
        self.pilha.so(maeb, fb, gb, kb, anims=[FadeOut(cota), FadeOut(dk_), FadeOut(circ_dk), FadeOut(v25), f3.op.animate.set_value(1.0)])
        self.plano_v("E1-5 EXPLODIDO", -32.0, 12.0, 4.9, -3.5, 0.55, 0.0, 0.0, rt=1.3, extra=(vt["ex"].animate.set_value(1.0),))
        ce = self.vcam()
        pi_an = chamada_em(self.vp((0.0, 0.10 * 1.0 - 0.034, 0.40)), lbl(r"1{,}875", MAS, 40), P3(-0.4, 2.25), cor=MAS)
        pi_cu = chamada_em(self.vp((0.0, -0.16, 0.08)), lbl(r"0{,}015", MAS, 40), P3(-0.4, 1.1), cor=MAS)
        pi_di = chamada_em(self.vp((0.25, -0.30 - 0.005, 0.0)), lbl(r"0{,}1275", MAS, 40), P3(-0.4, -0.05), cor=MAS)
        self.play(FadeIn(pi_an), FadeIn(pi_cu), FadeIn(pi_di), Indicate(mae, color=MAS, scale_factor=1.05), run_time=0.8)
        self.gat("somando")
        S1, is1, _ = self.gm(mae, imae, ("I", "=", "I_{anel}", "+", "I_{cubo}", "+", r"2\,I_{disco}"), mapas=[([2, 3], [2, 4, 6])], rt=1.1)
        self._voos_seq = True
        S2, is2, _ = self.gm(S1, is1, ("I", "=", r"1{,}875", "+", r"0{,}015", "+", r"0{,}1275"), mapas=[([2], []), ([4], []), ([6], [])],
                             voos={2: pi_an[2], 4: pi_cu[2], 6: pi_di[2]}, cores={2: MAS, 4: MAS, 6: MAS}, rt=1.6)
        self._voos_seq = False
        self.gat("dois vírgula zero dois")
        S_, is_, sb = self.gm(S2, is2, ("I", "=", r"2{,}0175\ \mathrm{kg\,m^2}"), cores={2: MAS}, caixa_cor=MAS, rt=1.0)
        self.pilha.so(sb, rt=0.4)
        self.v_flags["foco"] = ""
        self.geral_v(rt=1.3, extra=(vt["ex"].animate.set_value(0.0), FadeOut(pi_an), FadeOut(pi_cu), FadeOut(pi_di)))
        x0, w = 1.0, 5.4
        segs_m = (("ANEL", 0.75), ("CUBO", 0.15), ("DISCOS", 0.10))
        segs_i = (("ANEL", I_ANEL / I_VOL), ("DISCOS", 2 * I_DISCO / I_VOL), ("CUBO", I_CUBO / I_VOL))
        cores_seg = {"ANEL": MAS, "CUBO": mix(MAS, 0.45), "DISCOS": escuro(MAS, 0.35)}

        def barra_comp(y, segs, titulo):
            g = VGroup(txt(titulo, 30, bold=True, color=MAS).move_to(P3(x0 + 0.1, y + 0.45), aligned_edge=LEFT))
            x = x0
            for nome, fr in segs:
                ww = w * fr
                g.add(Rectangle(width=max(0.03, ww), height=0.36).move_to(P3(x + ww / 2, y)).set_fill(cores_seg[nome], 1.0).set_stroke(BACKGROUND_COLOR, 1.5))
                x += ww
            g.add(Rectangle(width=w, height=0.36).move_to(P3(x0 + w / 2, y)).set_stroke(GEO, 1.6))
            return g.set_z_index(10)

        bm = barra_comp(-0.25, segs_m, "MASSA")
        bi = barra_comp(-1.75, segs_i, "MOMENTO DE INÉRCIA")
        self.gat("o anel tem setenta e cinco por cento da massa")
        self.play(FadeIn(bm), run_time=0.7)
        pm = VGroup(txt("ANEL 75%", 30, color=MAS).move_to(P3(x0 + w * 0.375, -0.75)),
                    txt("CUBO 15%", 30, color=mix(MAS, 0.45)).move_to(P3(x0 + w * 0.86, -0.75)))
        self.play(FadeIn(pm), run_time=0.4)
        self.gat("quase noventa e três por cento")
        self.play(FadeIn(bi), run_time=0.7)
        pi_ = VGroup(txt("ANEL 92,9%", 30, color=MAS).move_to(P3(x0 + w * 0.4, -2.25)),
                     txt("DISCOS 6,3% · CUBO 0,7%", 30, color=mix(MAS, 0.45)).move_to(P3(x0 + w * 0.55, -2.7)))
        self.play(FadeIn(pi_), run_time=0.4)
        self.gat("sem o termo do deslocamento")
        self.selo("SEM", [[lbl(r"MD^2", MAS, 38), ":", lbl(r"0{,}0025", MAS, 38), "(51× MENOS)"]], cor=MAS, borda=MAS)
        self.gat("massa longe do eixo")
        self.tr_ok(0)
        frase = txt("MASSA LONGE DO EIXO PESA NO GIRO", 30, bold=True, color=MAS).move_to(P3(3.75, -3.3))
        self.play(FadeIn(frase, shift=0.1 * UP), vt["th"].animate.set_value(0.4), run_time=1.2)
        self.ate(0.99)

        # ── E1-6: item b — vista frontal (eixo para a câmera, centros coincidem) e diagramas de corpo livre ──
        self.an("E1-6")
        self.sem_selo()
        self.pilha.limpa(anims=[FadeOut(VGroup(bm, bi, pm, pi_, frase))])
        self.tr_acende(1)
        vt["th"].set_value(0.0)
        self.v_flags.update(foco="", cord=True)
        S6, C6 = 5.4, P3(-4.55, 0.7)                     # v5 §1.1: volante 2.5D com tambor, fio e bloco; anel de 3,8 u (≥ 55% da altura útil)
        self.modo25(C6, S6)
        r25 = self.rig25_vivo()
        self.play(f3.op.animate.set_value(0.0), FadeIn(r25), run_time=1.0)
        self.gat("separar os corpos")
        pb = self.v_bloco()
        topo_b = self.v_bloco(0.085)
        p_tg = self.vp((0.158, Y_TB, 0.0))
        o_ = self.v_eixo()
        corte = DashedLine(p_tg + 0.55 * DOWN + 0.35 * LEFT, p_tg + 0.55 * DOWN + 0.35 * RIGHT, dash_length=0.06).set_stroke(GEO, 2)
        self.play(Create(corte), run_time=0.4)
        self.gat("o peso para baixo")
        s_mg = seta_s(pb + 0.3 * DOWN, pb + 0.85 * DOWN, FC, 6)
        l_mg = lbl("mg", FC, 42).move_to((s_mg._ini + s_mg._fim) / 2 + 0.5 * RIGHT)
        self.play(FadeIn(s_mg), FadeIn(l_mg), run_time=0.5)
        self.gat("a tração para cima")
        s_T = seta_s(topo_b, topo_b + 0.9 * UP, FC, 6)
        l_T = lbl("T", FC, 42).move_to((s_T._ini + s_T._fim) / 2 + 0.5 * RIGHT)          # v6 #5: no meio da seta, fora das outras peças
        self.play(FadeIn(s_T), FadeIn(l_T), run_time=0.5)
        self.gat("a tração puxa a borda do tambor")
        s_T2 = seta_s(p_tg, p_tg + 0.85 * DOWN, FC, 6)
        l_T2 = chamada_em(s_T2._fim, lbl("T", FC, 42), P3(-1.2, 0.35), cor=FC)          # v6 #5: coluna fora do volante
        braco = VGroup(Line(o_, p_tg).set_stroke(HALO, 8), Line(o_, p_tg).set_stroke(C_RAIO, 4.5), lbl("r", C_RAIO, 40).move_to((o_ + p_tg) / 2 + 0.3 * UP))
        self.play(FadeIn(s_T2), FadeIn(l_T2), Create(braco[0]), FadeIn(braco[1]), run_time=0.7)
        self.gat("o peso do volante e a força do eixo")
        s_P = seta_s(o_ + 0.15 * DOWN, o_ + 1.25 * DOWN, FC, 6)
        s_F = seta_s(o_ + 0.15 * UP, o_ + 1.3 * UP, FC, 6)
        l_P = chamada_em(s_P._fim, lbl(r"M_v g", FC, 40), P3(-1.2, -0.75), cor=FC)
        l_F = chamada_em(s_F._fim, lbl(r"F_{eixo}", FC, 40), P3(-1.2, 1.4), cor=FC)
        self.play(FadeIn(s_P), FadeIn(s_F), FadeIn(l_P), FadeIn(l_F), run_time=0.6)
        self.gat("braço zero torque zero")
        bz = chamada_em(o_, txt("BRAÇO ZERO", 30, bold=True, color=GEO), P3(-1.05, 2.15))       # v2 §5 #7: fora do volante
        self.play(FadeIn(bz), run_time=0.5)
        lz = VGroup(lbl(r"\tau_{M_v g}", FC, 46), lbl("=", WHITE_, 46), lbl(r"\tau_{eixo}", FC, 46), lbl("=0", WHITE_, 46)).arrange(RIGHT, buff=0.12)
        self.pilha.poe(lz)
        self.play(FadeIn(lz, shift=0.08 * UP), run_time=0.5)
        self.ate(0.99)

        # ── E1-7: ΣF = ma e Στ = Iα (literais) → bloco e volante por glyph map, com forças e braço voando do DCL; v = ωr → vínculo ──
        self.an("E1-7")
        self.selo("TRÊS EQUAÇÕES", "UMA POR CORPO · MAIS O VÍNCULO")
        self.pilha.limpa()
        self.play(FadeOut(VGroup(s_P, s_F, l_P, l_F, bz, corte)), run_time=0.35)
        self.gat("newton no bloco")
        F0, if0, _ = self.linha((r"\sum", "F", "=", "m", "a"), rt=0.8, metodo="lei")
        e1, ie1, g1 = self.gm(F0, if0, ("m", "g", "-", "T", "=", "m", "a"), sai=[0, 1], voos={0: l_mg[0][0], 1: l_mg[0][1], 3: l_T}, tag="BLOCO", rt=1.3)
        self.gat("rotação do volante")
        L0, il0, _ = self.lei("newton_rot", (r"\sum", r"\tau", "=", "I", r"\alpha"), rt=0.8)
        e2, ie2, g2 = self.gm(L0, il0, ("T", "r", "=", "I", r"\alpha"), sai=[0, 1], voos={0: l_T2, 1: braco[1]}, tag="VOLANTE", rt=1.2)
        self.gat("e o vínculo")
        P0, ip0, _ = self.lei("pontes", ("v", "=", r"\omega", "r"), rt=0.8)
        e3, ie3, g3 = self.gm(P0, ip0, ("a", "=", r"\alpha", "r"), mapas=[([0], [0]), ([2], [2])], tag="VÍNCULO", rt=1.0)
        self.gat("o vínculo amarra a translação do bloco")
        self.play(self.ind_copia(g3, ACC, 1.08, 0.9), run_time=0.9)
        self.ate(0.99)

        # ── E1-8: álgebra até a fórmula (r atravessa, α vira a/r, T entra no bloco, a em evidência, m cancela) ──
        self.an("E1-8")
        self.sem_selo()
        self.pilha.so(g1, g2, g3)
        self.gat("da equação do volante")
        B1, ib1, _ = self.gm(e2, ie2, {"pre": ("T", "="), "num": ("I", r"\alpha"), "den": ("r",)}, rt=1.2)
        self.gat("trocando a aceleração angular pelo vínculo")
        B2, ib2, b2 = self.gm(B1, ib1, {"pre": ("T", "="), "num": ("I", "a"), "den": ("r^2",)}, sai=[3], mapas=[([5], [5])], voos={3: mp(e3, ie3, [0])}, rt=1.2)
        self.gat("coloca na equação do bloco")
        self.pilha.so(g1, b2)
        B3, ib3, _ = self.gm(e1, ie1, {"pre": ("m", "g", "-"), "num": ("I", "a"), "den": ("r^2",), "post": ("=", "m", "a")}, sai=[3],
                             voos={3: mp(B2, ib2, [2]), 4: mp(B2, ib2, [3]), 5: mp(B2, ib2, [4]), 6: mp(B2, ib2, [5])}, rt=1.3)
        self.gat("junta os termos com a aceleração")
        B4, ib4, _ = self.gm(B3, ib3, {"pre": ("m", "g", "=", "m", "a", "+"), "num": ("I", "a"), "den": ("r^2",)}, mapas=[([9], [4]), ([4], [7]), ([2], [5])], rt=1.2)
        B5, ib5, _ = self.gm(B4, ib4, ("m", "g", "=", "a", r"\left(m+\tfrac{I}{r^2}\right)"), mapas=[([4, 7], [3]), ([3, 5, 6, 8, 9], [4])], rt=1.3)
        self.gat("sai uma fórmula que vale guardar")
        B6, ib6, _ = self.gm(B5, ib5, {"pre": ("a", "="), "num": ("m", "g"), "den": ("m", r"+\tfrac{I}{r^2}")}, mapas=[([4], [5, 6])], rt=1.2)
        B7, ib7, b7 = self.gm(B6, ib6, {"pre": ("a", "="), "num": ("g",), "den": ("1", r"+\tfrac{I}{m\,r^2}")}, riscar=[2, 5],
                              mapas=[([6], [5])], cores={0: ACC}, size=52, caixa_cor=ACC, rt=1.3)
        self.pilha.so(b7)
        self.formula = b7
        self.form_ = (B7, ib7)
        self.ate(0.99)

        # ── E1-9: casos-limite e a inércia equivalente (bloco fantasma, sem fio) ──
        self.an("E1-9")
        self.selo("CONFERE", [[lbl(r"I\to 0", MAS, 36), "·", lbl("a=g", ACC, 36)], [lbl(r"I\to\infty", MAS, 36), "·", lbl(r"a\to 0", ACC, 36)]])
        self.gat("sem inércia nenhuma")
        Lm1, _, _ = self.linha((r"I\to 0", r":\ ", "a", r"\to", "g"), size=46, rt=0.9)
        self.gat("com momento de inércia enorme")
        Lm2, _, _ = self.linha((r"I\to\infty", r":\ ", "a", r"\to", "0"), size=46, rt=0.9)
        self.gat("uma inércia equivalente")
        self.pilha.so(b7, anims=[])
        r15 = lbl(r"r=0{,}15\ \mathrm{m}", C_RAIO, 40).move_to(braco[1].get_center() + 0.4 * LEFT + 0.95 * UP).set_z_index(26)      # v7: acima do cubo central (antes ficava atrás dele)
        self.play(ReplacementTransform(braco[1], r15), run_time=0.5)
        braco[1] = r15
        tb_ = [None, r15]
        Q0, iq0, _ = self.linha({"pre": (), "num": ("I",), "den": ("r^2",)}, voos={0: mp(B7, ib7, [5]), 2: mp(B7, ib7, [5])}, size=48, rt=1.0)
        Q1, iq1, _ = self.gm(Q0, iq0, {"pre": (r"\tfrac{I}{r^2}", "="), "num": (r"2{,}0175",), "den": (r"0{,}15^2",)}, mapas=[([0, 1, 2], [0])],
                             voos={2: mp(S_, is_, [2]), 4: tb_[1]}, cores={2: MAS, 4: C_RAIO}, rt=1.2)
        Q_, iq, _ = self.gm(Q1, iq1, (r"\tfrac{I}{r^2}", r"\approx", r"89{,}7\ \mathrm{kg}"), cores={2: MAS}, rt=1.0)
        cx_, cy_ = -6.2, -1.8
        lado = 0.5
        fant = Square(lado).move_to(P3(cx_, cy_ + 0.21)).set_fill(MAS, 0.35).set_stroke(MAS, 2.6)
        fant._fantasma = True
        mold = RoundedRectangle(corner_radius=0.1, width=1.9, height=1.2).move_to(P3(cx_, cy_)).set_stroke(GEO, 1.6).set_fill(PANEL, 0.4)
        mold._fundo = mold._caixa = True
        t_f = VGroup(txt("INÉRCIA EQUIVALENTE", 20, bold=True, color=MAS), txt("NÃO É PESO EXTRA", 20, bold=True, color=CYAN)).arrange(DOWN, buff=0.04).next_to(mold, DOWN, buff=0.04)
        if t_f.get_left()[0] < -7.45:
            t_f.shift((-7.45 - t_f.get_left()[0]) * RIGHT)
        v_f = lbl(r"\approx 90\ \mathrm{kg}", MAS, 34).move_to(P3(cx_, cy_ - 0.27))
        self.gat("quase noventa quilos")
        self.play(FadeIn(mold), FadeIn(fant), FadeIn(t_f), run_time=0.6)
        self.voa([(mp(Q_, iq, [2]), v_f)], rt=1.0, origem=False)
        self.gat("cuidado não é uma massa extra")
        s_peso = seta_s(self.v_bloco() + 0.3 * DOWN, self.v_bloco() + 0.85 * DOWN, FC, 6)
        l_peso = lbl("mg", FC, 42).move_to((s_peso._ini + s_peso._fim) / 2 + 0.5 * RIGHT)
        self.remove(s_mg, l_mg)                                            # v8: o "mg" e a seta do E1-4 já estão nesse lugar; sem cópia empilhada
        self.play(FadeIn(s_peso), FadeIn(l_peso), run_time=0.5)
        self.gat("o giro acrescenta inércia não força")
        nf = VGroup(txt("O GIRO ACRESCENTA INÉRCIA,", 30, bold=True, color=MAS), txt("NÃO FORÇA", 30, bold=True, color=MAS)).arrange(DOWN, buff=0.1)
        self.pilha.poe(nf)
        self.play(FadeIn(nf, shift=0.08 * UP), run_time=0.6)
        self.ate(0.99)

        # ── E1-10: os números de a, α e T (cada um do seu rótulo); setas na escala ──
        self.an("E1-10")
        self.selo("CONFERE", [[lbl("T", FC, 38), lbl("<", FC, 38), lbl(r"mg=98\ \mathrm{N}", FC, 38)], [lbl(r"Tr=I\alpha", FC, 38)]])
        self.pilha.so(b7, anims=[FadeOut(VGroup(mold, fant, t_f, v_f, nf))])
        self.gat("a aceleração do bloco")
        N0, in0, _ = self.linha({"pre": ("a", "="), "num": ("g",), "den": ("1", r"+\tfrac{I}{m\,r^2}")}, voos={0: mp(B7, ib7, [0]), 2: mp(B7, ib7, [2]), 4: mp(B7, ib7, [4]), 5: mp(B7, ib7, [5])}, rt=1.0)
        N1, in1, _ = self.gm(N0, in0, {"pre": ("a", "="), "num": (r"9{,}8",), "den": ("1", r"+8{,}97")}, sai=[2, 5],
                             voos={5: mp(Q_, iq, [2])}, cores={2: ACC}, rt=1.3)
        N1b, in1b, _ = self.gm(N1, in1, ("a", "=", r"0{,}983\ \mathrm{m/s^2}"), cores={2: ACC}, rt=0.9)
        self.gat("dividindo pelo raio do tambor")
        self.pilha.so(b7, N1b)                                       # v9: abre vaga: o cartão das pontes não cobre mais a linha que nasce
        P1, ip1, _ = self.lei("pontes", ("a_t", "=", r"\alpha", "r"), rt=0.8)
        N2, in2, _ = self.gm(P1, ip1, {"pre": (r"\alpha", "="), "num": ("a",), "den": ("r",)}, mapas=[([0], [2])], rt=1.0)
        N2b, in2b, _ = self.gm(N2, in2, {"pre": (r"\alpha", "="), "num": (r"0{,}983",), "den": (r"0{,}15",)}, sai=[2, 4],
                               voos={2: mp(N1b, in1b, [2]), 4: tb_[1]}, cores={2: ACC, 4: C_RAIO}, rt=1.1)
        N2c, in2c, _ = self.gm(N2b, in2b, (r"\alpha", "=", r"6{,}56\ \mathrm{rad/s^2}"), cores={2: ACC}, rt=0.8)
        self.gat("a tração é a massa")
        self.pilha.so(N1b, N2c, g1)
        pbl = self.v_bloco()
        mb_ = chamada(pbl + 0.45 * LEFT, lbl(r"m=10\ \mathrm{kg}", MAS, 40), LEFT, 1.6)
        self.play(FadeIn(mb_), run_time=0.4)
        N3, in3, _ = self.gm(e1, ie1, ("T", "=", "m", "(g-a)"), mapas=[([0], [2]), ([1, 2, 6], [3])], rt=1.2)
        N3b, in3b, _ = self.gm(N3, in3, ("T", "=", "10", r"(9{,}8-0{,}983)"), sai=[2], mapas=[([3], [3])], voos={2: mb_[2]}, cores={2: MAS}, rt=1.1)
        N3c, in3c, _ = self.gm(N3b, in3b, ("T", "=", r"88{,}2\ \mathrm{N}"), cores={2: FC}, caixa_cor=FC, rt=0.8)
        k = 1.1 / 98
        topo_b = self.v_bloco(0.085)
        s_T_ = seta_s(topo_b, topo_b + T_VOL * k * UP, FC, 6)
        l_T_ = lbl(r"88{,}2\ \mathrm{N}", FC, 40).next_to(s_T_._fim + 0.65 * DOWN, RIGHT, buff=0.3)       # v9: fora do anel (antes só o "N" aparecia)
        l_mg_ = lbl(r"98\ \mathrm{N}", FC, 40).next_to(s_peso._fim, RIGHT, buff=0.2)       # v2 §5 #9: ao lado da ponta
        self.play(Transform(s_T, s_T_), FadeOut(l_T), FadeIn(l_T_), Transform(l_peso, l_mg_), run_time=0.8)
        self.gat("a tração vezes o raio do tambor dá")
        self.tr_ok(1)
        self.ate(0.99)

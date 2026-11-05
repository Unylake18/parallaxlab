"""Lote PE3 (v2): E3 — quanto gira a Terra? (Three.js 'terra').
E3-1 modo órbita, câmera oblíqua: Sol, Terra com eixo inclinado 23,4° em órbita; marcador FORA DE ESCALA no canto do ESQUEMA.
E3-2 câmera de cima do plano da órbita; a órbita do Three.js some e o Manim desenha só o TRECHO entre as duas posições da Terra (C3). Ao meio-dia solar
o meridiano do observador aponta para o Sol e para a estrela; a estrela fica na borda do PALCO, com as direções PARALELAS saindo das duas Terras e o
marcador → ∞ (D38). A Terra dá UMA volta em relação à estrela enquanto avança 30° (marcador EXAGERADO; real ≈ 1°), depois o arco âmbar extra até o Sol
voltar ao meridiano. Cada linha (dia sideral / dia solar médio) nasce quando a estrela ou o Sol volta ao meridiano (D39).
E3-3 contagem anual NA PILHA (D40): 1/T_sid = 1/T_sol + 1/T_ano por passo (divisão termo a termo) e T_sid = (365,24/366,24)·86.400 s com os números
voando dos contadores e do dia solar. E3-4…E3-6 modo geo: Terra grande (ø 4,3 u ≈ 70% da altura do ESQUEMA), eixo vertical, câmera que não gira com
ela; São Paulo a 23,55° S; inset de zoom (×3) em São Paulo com λ, r⊥, v⃗ e a_c (D41, S24). v⃗ = ω⃗ × r⃗ calculado no Three.js. Sem fio de prumo.
Álgebra do v2: nenhuma linha de equação da CONTA entra por FadeIn de linha inteira (escrita em ordem, voos do desenho, passo/TransformByGlyphMap)."""
from pecas20 import *  # noqa: F401,F403


def Mm(*pares, size, final=None):
    """Proxy de TransformMatchingTex (como no PT3): o mesmo TeX da linha eqp em partes; a cor de cada glifo vem da linha final."""
    m = Mc(*pares, size=size)
    for sub, (t, c) in zip(m.submobjects, pares):
        if c:
            sub.set_stroke(c, width=1.8, background=False)
    if final is not None:
        gp = [g for g in m.family_members_with_points()]
        gf = [g for g in final.family_members_with_points()]
        if len(gp) == len(gf):
            for a, b in zip(gp, gf):
                a.set_fill(b.get_fill_color(), b.get_fill_opacity())
                a.set_stroke(b.get_stroke_color(), width=b.get_stroke_width(), background=False)
    return m

RO, RT, RS = 3.0, 0.45, 0.6          # raio da órbita, da Terra e do Sol (mundo, fora de escala)
LAT, LON_SP = math.radians(-23.55), math.radians(-46.63)
CEN_E = P3(-3.75, -0.5)
KG, XG, YG, KWG = 2.15, -5.0, -0.7, 0.45                    # modo geo: Terra de raio 2,15 u em (−5,0; −0,7); seta ω⃗ = 0,45 R acima do polo
CI, RI = P3(-1.3, 1.0), 1.25                                 # inset de zoom em São Paulo (canto livre do ESQUEMA, acima à direita da Terra)
ZE = (-7.3, 0.2, -3.65, 2.5)                                 # zona do ESQUEMA para o teste de rótulo
BGT = "#0B1530"                                              # contorno escuro atrás de rótulo sobre a textura da Terra


def fundo_txt(m):
    m.set_stroke(BGT, 5, background=True)
    return m


def un(v):
    v = np.asarray(v, float)
    return v / np.linalg.norm(v)


class LoteE3(L20):

    def construct(self):
        self.setup_base()
        self.e3()
        self.fim()
        self.relatorio()
        self.gravar_reg()

    def _selo_mob(self, *a, **kw):
        """§3: padding do selo ≥ 0,16 u na horizontal e ≥ 0,10 u na vertical (a peça comum usa 0,12 × 0,06)."""
        kw["wmax"] = kw.get("wmax", LARG_CONTA) - 0.1                    # o texto quebra 0,1 mais estreito: a caixa com o padding novo não passa da largura
        s = super()._selo_mob(*a, **kw)
        bx, g = s[0], s[1]
        bx.stretch_to_fit_width(g.width + 0.34).stretch_to_fit_height(g.height + 0.2).move_to(g)
        return s

    def troca_marcador(self, texto=None, lado="dir", y=-2.95):
        """v3 §5.15: o marcador sobe 0,37 u (não encosta mais no rodapé)."""
        return super().troca_marcador(texto, lado, y)

    def tmt(self, src, dst, ps, pd, size_s, size_d, key_map=None, rt=1.2, extra=()):
        """v3 §7: TransformMatchingTex da linha-mãe `src` (fica na tela) para a linha nova `dst` (mesmo desenho do PT3)."""
        print(f"[alg] {self._aid} tmt {' '.join(t for t, _ in pd)[:40]}")
        a = Mm(*ps, size=size_s, final=src).move_to(src.get_center())
        b = Mm(*pd, size=size_d, final=dst).move_to(dst.get_center())
        tops_antes = set(id(m) for m in self.mobjects)
        self._voando = set(id(x) for x in a.get_family()) | set(id(x) for x in b.get_family())
        self._voando_raiz = [a, b]
        self._fontes_extra = [src]
        self.play(TransformMatchingTex(a, b, key_map=key_map), *extra, run_time=max(0.8, rt))
        self._fontes_extra = []
        self._voando, self._voando_raiz = set(), []
        self.remove(a, b)
        self.add(dst)
        self._sobras(tops_antes, [dst] + [getattr(e, "mobject", None) for e in extra])
        self.foco = dst

    def legenda(self, L_, il, src, rt=1.0):
        """Legenda do desenho (R = 6.371 km, λ = 23,55°): o símbolo voa do rótulo de origem e o resto é escrito na ordem (=, número)."""
        an_ = [TransformFromCopy(src, mp(L_, il, [0])), Write(mp(L_, il, [1])), Write(mp(L_, il, [2]))]
        self._voando_raiz = [L_, src] + [a.mobject for a in an_]
        self.play(AnimationGroup(*an_, lag_ratio=0.45), run_time=rt)
        self._voando_raiz = []
        self.limpa_pecas(L_)
        self.add(L_)

    def e3(self):
        self.pilha.x0, self.pilha.larg = X_CONTA + 0.1, LARG_CONTA - 0.1      # o respiro do pulso (escala 1,06) das linhas não entra na CALHA
        self.an("E3-1")
        self.secao("EXERCÍCIO 3 · QUANTO GIRA A TERRA?")
        T = {"phi": -PI / 2 - PI / 12, "psi": 0.0, "fant": 0.0, "modo": "orbita", "rotg": 0.0, "g": {}}
        az, el, K, alvo_y, orb = ValueTracker(-90.0), ValueTracker(28.0), ValueTracker(1.05), ValueTracker(0.0), ValueTracker(1.0)
        rtv, rsv = ValueTracker(RT), ValueTracker(RS)                     # v3 §5.15: Terra e Sol crescem no E3-2 (ver abaixo)
        self.add(az, el, K, alvo_y, orb, rtv, rsv)
        camG = cam_obl(-90.0, 16.0, (0.0, 0.0, 0.0), K=KG, xc=XG, yc=YG, fov=16)

        def cam():
            if T["modo"] == "geo":
                return camG
            return cam_obl(az.get_value(), el.get_value(), (0.0, alvo_y.get_value(), 0.0), K=K.get_value(), xc=float(CEN_E[0]), yc=float(CEN_E[1]), fov=16)

        def est(t):
            if T["modo"] == "geo":
                return {"modo": "geo", "terras": [{"p": [0, 0, 0], "r": 1.0, "rot": round(T["rotg"], 4), "incl": 0, "op": T["g"].get("opT", 1.0)}],
                        "g": {k: (round(v, 4) if isinstance(v, float) else v) for k, v in T["g"].items()}, "cam": cam()}
            E1 = [RO * math.cos(T["phi"]), RO * math.sin(T["phi"]), 0.0]
            ts = [{"p": [round(x, 4) for x in E1], "r": round(rtv.get_value(), 4), "rot": round(T["psi"], 4), "incl": 23.4 if T.get("incl", True) else 0.0}]
            o = orb.get_value()
            return {"modo": "orbita", "terras": ts, "sol": {"p": [0, 0, 0], "r": round(rsv.get_value(), 4)}, "estrela": {"p": [-30.0, 70.0, 26.0], "s": 1.6} if T.get("estrela", True) else None,
                    "orbita": {"R": RO, "op": round(0.5 * o, 3)} if o > 0.01 else None, "cam": cam()}
        f3 = Fundo3D(self, "terra", est, op=0.2)
        self.add(f3)
        S = {"t": self.clk.get_value(), "wpsi": 0.6, "wphi": 0.05}

        def motor(m):
            t = self.clk.get_value()
            dt = t - S["t"]
            S["t"] = t
            if T["modo"] == "orbita" and T.get("livre", True):
                T["psi"] += S["wpsi"] * dt
                T["phi"] += S["wphi"] * dt
        mot = VGroup()
        mot.add_updater(motor)
        self.add(mot)
        self.play(f3.op.animate.set_value(1.0), *self.troca_marcador("FORA DE ESCALA", "dir"), run_time=0.8)
        q = VGroup(txt("A TERRA DÁ UMA VOLTA", 30, bold=True),
                   VGroup(txt("EM", 30, bold=True), lbl(r"24\ \mathrm{h}", WHITE_, 46), txt("?", 30, bold=True)).arrange(RIGHT, buff=0.14)
                   ).arrange(DOWN, buff=0.12, aligned_edge=LEFT)          # sem encolher: a pergunta quebra em duas linhas
        self.pilha.topo = 2.0                                             # a Pilha já começa abaixo do selo PEDE (duas linhas): nada se move quando ele entra
        self.pilha.poe(q)
        self.play(FadeIn(q), run_time=0.6)
        self.gat("depende uma volta em relação a quê")
        self.pede("EM RELAÇÃO A QUÊ? E QUAL É A DISTÂNCIA AO EIXO?")
        self.ate(0.99)

        # ── E3-2: dia sideral × dia solar (vista de cima; só o trecho da órbita) ──
        self.an("E3-2")
        self.pilha.limpa(rt=0.3)
        self.sem_selo()
        self.pilha.topo = TOPO_PILHA
        T["livre"] = False
        phi1, dphi = -PI / 2 - PI / 12, PI / 6
        T["phi"] = phi1
        s_hat = -np.array([math.cos(phi1), math.sin(phi1), 0.0])         # direção da estrela = Terra → Sol no meio-dia da posição 1
        a_star = math.atan2(s_hat[1], s_hat[0])
        s2 = P3(s_hat[0], s_hat[1])
        T["psi"] = a_star                                                 # observador (meridiano) apontando para o Sol e a estrela
        T["estrela"] = False
        self.play(el.animate.set_value(89.999), az.animate.set_value(-90.0), K.animate.set_value(1.25), alvo_y.animate.set_value(-1.9),
                  orb.animate.set_value(0.0), rtv.animate.set_value(0.62), rsv.animate.set_value(0.85), run_time=1.6)
        T["p0"], T["psi0"] = [RO * math.cos(phi1), RO * math.sin(phi1), 0.0], a_star
        cmT = cam()
        sol_c = projeta3d(cmT, np.zeros(3))
        R_orb = float(np.linalg.norm(projeta3d(cmT, np.array([RO, 0, 0])) - sol_c))
        R_sol = float(np.linalg.norm(projeta3d(cmT, np.array([rsv.get_value(), 0, 0])) - sol_c))
        # C3: só o trecho da órbita entre as duas posições da Terra (um pouco além de cada uma), com o Sol dentro do PALCO
        orb_arc = DashedVMobject(Arc(radius=R_orb, start_angle=phi1 - 0.13, angle=dphi + 0.26, arc_center=sol_c, num_components=40),
                                 num_dashes=24, dashed_ratio=0.55).set_stroke(GEO, 4, opacity=0.8).set_z_index(3)
        tela = lambda p: projeta3d(cam(), np.asarray(p, float))
        c0 = tela(T["p0"])
        sc_T = float(np.linalg.norm(tela(np.array(T["p0"]) + np.array([rtv.get_value(), 0, 0])) - c0))
        c_fim = tela([RO * math.cos(phi1 + dphi), RO * math.sin(phi1 + dphi), 0.0])
        P_EST = c_fim + ((2.2 - c_fim[1]) / s_hat[1]) * s2             # D38: estrela na borda de cima do PALCO, na reta da Terra na posição 2
        L_top = lambda cc: (P_EST[1] - 0.32 - cc[1]) / s_hat[1]
        vis = {"est": ValueTracker(0.0), "sol": ValueTracker(0.0)}
        self.add(*vis.values())

        def comp_seta(cc):
            """Comprimento da seta de cc na direção da estrela: até perto da borda, cortada antes do disco do Sol se a reta passar por ele."""
            L = L_top(cc)
            d = sol_c - cc
            ao_longo = float(np.dot(d[:2], s2[:2]))
            perp = abs(float(d[0] * s2[1] - d[1] * s2[0]))
            if ao_longo > 0 and perp < R_sol + 0.2:
                L = min(L, ao_longo - math.sqrt(max(0.0, (R_sol + 0.2) ** 2 - perp ** 2)))
            return L

        def sobre():
            E1 = np.array([RO * math.cos(T["phi"]), RO * math.sin(T["phi"]), 0.0])
            c = tela(E1)
            psi = T["psi"]
            g = VGroup()
            mer = P3(math.cos(psi), math.sin(psi))
            g.add(DashedLine(c, c + (sc_T + 0.45) * mer, dash_length=0.08).set_stroke(WHITE_, 2.6, opacity=0.9).set_z_index(9))
            g.add(Dot(c + sc_T * mer, radius=0.075, color=WHITE_).set_z_index(11))
            oe = vis["est"].get_value()
            if oe > 0.01:                                                 # a MESMA direção (estrela no infinito), nas duas posições
                for pp in ([T["p0"]] if T["fant"] > 0.01 else []) + [E1.tolist()]:
                    cc = tela(pp)
                    g.add(escala_op(seta(cc + (sc_T + 0.5) * s2, cc + comp_seta(cc) * s2, GEO, 6, tip=0.24, z=8), oe))
            os_ = vis["sol"].get_value()
            if os_ > 0.01:
                sd = un((sol_c - c)[:2])
                sd = P3(sd[0], sd[1])
                g.add(DashedLine(c + (sc_T + 0.1) * sd, sol_c - (R_sol + 0.15) * sd, dash_length=0.08).set_stroke(ANG, 2.2, opacity=0.6 * os_).set_z_index(7))
            if not PEDIDOS3D:
                self.reg("terra_estrela", s=[float(s_hat[0]), float(s_hat[1])], psi=psi, phi=T["phi"])
            return g
        sv = vivo(sobre)
        self.play(FadeIn(orb_arc), run_time=0.4)
        P1 = VGroup(txt("AO MEIO-DIA SOLAR:", 28, bold=True), txt("O SOL CRUZA O MERIDIANO", 28)).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        self.pilha.poe(P1)
        self.gat("ao meio dia solar o sol cruza o meridiano")
        self.play(FadeIn(sv), FadeIn(P1), run_time=0.7)
        l_mer = txt("MERIDIANO", 24)
        l_obs = txt("OBSERVADOR", 24)
        r_mer = self.rotulo(l_mer, c0 + (sc_T + 0.45) * s2, lados=(LEFT, UL, DL), buffs=(0.3, 0.5), zona=ZE, chamada=False)
        r_obs = self.rotulo(l_obs, c0 + sc_T * s2, lados=(RIGHT, DR, UR), buffs=(0.3, 0.5), zona=ZE, chamada=False)
        self.play(FadeIn(r_mer), FadeIn(r_obs), run_time=0.5)
        estrela = Star(n=5, outer_radius=0.17, density=2).set_fill(WHITE_, 1).set_stroke(WHITE_, 1).move_to(P_EST).set_z_index(10)
        l_est = VGroup(txt("ESTRELA", 24), lbl(r"\to\infty", WHITE_, 36)).arrange(DOWN, buff=0.08, aligned_edge=LEFT)
        l_est.next_to(estrela, RIGHT, buff=0.3).align_to(estrela, UP)
        P2 = VGroup(txt("ESTRELA MUITO DISTANTE:", 28, bold=True), txt("NO MESMO MERIDIANO", 28)).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        self.pilha.poe(P2)
        self.gat("vamos marcar também a direção de uma estrela")
        self.play(vis["est"].animate.set_value(1.0), FadeIn(estrela), FadeIn(l_est), FadeIn(P2), run_time=0.7)
        self.gat("depois de uma volta completa em relação às estrelas")
        self.play(FadeOut(r_mer), FadeOut(r_obs), *self.troca_marcador(None), run_time=0.3)
        fant = DashedVMobject(Circle(radius=sc_T).move_to(c0), num_dashes=18, dashed_ratio=0.55).set_stroke(GEO, 2.4, opacity=0.75).set_z_index(6)
        T["fant"] = 1.0
        prog = ValueTracker(0.0)
        self.add(prog)
        upd = VGroup()
        upd.add_updater(lambda m: T.update(phi=phi1 + dphi * prog.get_value(), psi=a_star + 2 * PI * prog.get_value()))
        self.add(upd)
        self.play(prog.animate(rate_func=linear).set_value(1.0), vis["sol"].animate.set_value(1.0), FadeIn(fant), *self.troca_marcador("EXAGERADO", "dir"),
                  run_time=self.ate_t("só que nesse tempo"))
        D1m, id1 = M(r"\approx", r"23\ \mathrm{h}\ 56\ \mathrm{min}", size=46)
        D1 = VGroup(txt("EM RELAÇÃO ÀS ESTRELAS:", 28, bold=True), linha_m(txt("DIA SIDERAL", 28, bold=True), D1m, buff=0.2)).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        self.pilha.poe(D1)
        self.gat("só que nesse tempo a terra também andou")
        self.play(FadeIn(D1), run_time=0.9)                               # D39: nasce quando a estrela volta ao meridiano
        self.gat("então o sol ainda não voltou ao meridiano")
        extra = ValueTracker(0.0)
        self.add(extra)
        upd.clear_updaters()
        upd.add_updater(lambda m: T.update(psi=a_star + 2 * PI + dphi * extra.get_value()))
        c2 = tela([RO * math.cos(phi1 + dphi), RO * math.sin(phi1 + dphi), 0.0])

        def arco_extra():
            e = extra.get_value()
            if e < 0.01:
                return VGroup()
            return VGroup(arco(c2, 1.9, a_star, a_star + dphi * e, ANG, 14, z=10))
        av = vivo(arco_extra)
        self.add(av)
        self.play(extra.animate(rate_func=smooth).set_value(1.0), run_time=2.0)
        D2m, id2 = M("=", r"24\ \mathrm{h}", size=46)
        D2r = linha_m(txt("DIA SOLAR MÉDIO", 28, bold=True), D2m, buff=0.2)
        D2 = VGroup(txt("EM RELAÇÃO AO SOL:", 28, bold=True), D2r).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        self.pilha.poe(D2)
        self.play(FadeIn(D2), run_time=0.9)                               # D39: nasce quando o Sol volta ao meridiano
        l1g = VGroup(lbl(r"\approx 1^\circ", ANG, 36), txt("(REAL)", 24)).arrange(RIGHT, buff=0.12)
        a_mid = a_star + dphi / 2
        r1g = self.rotulo(l1g, c2 + 1.9 * P3(math.cos(a_star), math.sin(a_star)), lados=(RIGHT, UR), buffs=(0.3, 0.5, 0.8), zona=ZE, chamada=False)
        self.gat("quase um grau")
        self.play(FadeIn(r1g), run_time=0.5)
        self.gat("o dia de vinte e quatro horas é o dia solar médio")
        self.foco = D2
        self.wait(1.0)
        self.gat("a volta de verdade em relação às estrelas")
        self.foco = D1
        self.ate(0.99)

        # ── E3-3: contagem anual, na Pilha (D40) ──
        self.an("E3-3")
        upd.clear_updaters()
        self.play(FadeOut(sv), FadeOut(av), FadeOut(VGroup(orb_arc, estrela, l_est, r1g, fant)), *self.troca_marcador(None),
                  K.animate.set_value(0.8), alvo_y.animate.set_value(0.0), orb.animate.set_value(1.0), run_time=0.8)
        self.remove(sv, av)
        T["fant"] = 0.0
        self.play(*self.troca_marcador("FORA DE ESCALA", "esq"), run_time=0.3)   # canto esquerdo: a Terra para à direita, embaixo, no fim do ano
        self.pilha.so(D2)
        # o dia solar em segundos (a origem do 86.400 da conta)
        D2n, id2n = M("=", r"86{.}400\ \mathrm{s}", size=46)
        D2n.move_to(D2m, aligned_edge=LEFT)
        self._voando_raiz = [D2m, D2n]                                    # troca no lugar (24 h → 86.400 s): glifos em trânsito, não objetos (G23)
        self.play(ReplacementTransform(mp(D2m, id2, [0]), mp(D2n, id2n, [0])), FadeOut(mp(D2m, id2, [1])),
                  FadeIn(mp(D2n, id2n, [1])), run_time=0.6)
        self._voando_raiz = []
        for m in list(self.mobjects):
            if m is not D2 and any(x is y for x in m.get_family() for y in D2n.get_family()):
                self.remove(m)
        D2r.remove(D2m)
        D2r.add(D2n)
        self.add(D2n)
        ano = ValueTracker(0.0)
        self.add(ano)
        phi_a = T["phi"]
        upd.add_updater(lambda m: T.update(phi=phi_a + 2 * PI * ano.get_value(), psi=T["psi"]))
        rS = VGroup(txt("VOLTAS (SOL):", 26), num_mob("365,24", ANG, 40)).arrange(RIGHT, buff=0.15)
        rE = VGroup(txt("VOLTAS (ESTRELAS):", 26), num_mob("366,24", ANG, 40)).arrange(RIGHT, buff=0.15)
        self.pilha.poe(rS)
        self.pilha.poe(rE)

        def contagem():
            u = ano.get_value()
            sol = 365.2422 * u
            g = VGroup()
            for row, v in ((rS, sol), (rE, sol + u)):
                g.add(row[0].copy(), num_mob(f"{v:.2f}".replace(".", ","), ANG, 40).move_to(row[1].get_corner(DL), aligned_edge=DL))
            return g
        ctv = vivo(contagem)
        self.gat("conta as voltas num ano inteiro")
        self.play(FadeIn(ctv), run_time=0.4)
        self.play(ano.animate(rate_func=linear).set_value(1.0), run_time=5.0)
        self.remove(ctv)
        self.add(rS, rE)
        mais1 = lbl("+1", ANG, 40).next_to(rE[1], RIGHT, buff=0.3)
        self.gat("em relação às estrelas uma volta a mais")
        self.play(FadeIn(mais1), run_time=0.4)
        N_, iN = M(r"N_{\mathrm{est}}", "=", r"N_{\mathrm{sol}}", "+", "1", size=52, cores={0: ANG, 2: ANG, 4: ANG})
        self.pilha.poe(N_)
        self.gat("porque a órbita inteira acrescenta um giro")
        self.voa([(VGroup(mais1[0][1]), mp(N_, iN, [4]))], extra=[FadeIn(mp(N_, iN, [0, 1, 2, 3]))], rt=1.0, origem=False)
        Y2, iy2 = M(r"\frac{1}{T_{\mathrm{sid}}}", "=", r"\frac{1}{T_{\mathrm{sol}}}", "+", r"\frac{1}{T_{\mathrm{ano}}}", size=52)
        self.pilha.poe(Y2)
        self.gat("dividindo tudo pelo tempo de um ano")
        # GM da divisão termo a termo: N_est → 1/T_sid, N_sol → 1/T_sol, o "1" vira o numerador de 1/T_ano (com a barra) e T_ano entra embaixo
        self.passo(N_, Y2, (J(iN, 0), J(iy2, 0)), (J(iN, 1), J(iy2, 1)), (J(iN, 2), J(iy2, 2)), (J(iN, 3), J(iy2, 3)), (J(iN, 4), iy2[4][:2]),
                   ([], iy2[4][2:]), rt=1.4, origem=False)
        self.pilha.tira(N_)
        self.play(FadeOut(N_), FadeOut(mais1), run_time=0.3)
        self.pilha._reflow(self.pilha.linhas, 0.4)
        Y3, iy3 = M(r"T_{\mathrm{sid}}", "=", r"\frac{365{,}24}{366{,}24}", r"\cdot", r"86{.}400\ \mathrm{s}", size=48)
        for j in iy3[2][:6] + iy3[2][7:]:
            Y3[0][j].set_color(ANG)
            Y3[0][j].set_stroke(ANG, width=1.8, background=False)
        self.pilha.poe(Y3)
        self.gat("dá oitenta e seis mil")
        # números dos contadores e do dia solar; a barra entra junto com o numerador (bug 3 da escreve: barra antes do numerador)
        self.voa([(rS[1], VGroup(*[Y3[0][j] for j in iy3[2][:7]])), (rE[1], VGroup(*[Y3[0][j] for j in iy3[2][7:]])), (mp(D2n, id2n, [1]), mp(Y3, iy3, [4]))],
                 extra=[FadeIn(mp(Y3, iy3, [0, 1, 3]))], rt=1.6, origem=False)
        Y3b, iy3b = M(r"\approx", r"86{.}164\ \mathrm{s}", size=48)
        self.pilha.poe(Y3b)
        self.play(FadeIn(Y3b), run_time=0.6)
        Y3c, iy3c = M(r"\approx", r"23\ \mathrm{h}\ 56\ \mathrm{min}\ 4\ \mathrm{s}", size=48)
        self.pilha.poe(Y3c)
        self.gat("vinte e três horas cinquenta")
        self.play(FadeIn(Y3c), run_time=0.7)
        Y4, iy4 = M(r"\omega", "=", r"\frac{2\pi}{T_{\mathrm{sid}}}", size=52, cores={0: VEL})
        self.pilha.poe(Y4)
        self.gat("e a velocidade angular da terra")
        self.voa([(mp(Y3, iy3, [0]), VGroup(*[Y4[0][j] for j in iy4[2][3:]]))], extra=[FadeIn(mp(Y4, iy4, [0, 1])), FadeIn(VGroup(*[Y4[0][j] for j in iy4[2][:3]]))],
                 rt=1.1, origem=False)
        Y5, iy5 = M(r"\omega", r"\approx", r"7{,}292\times 10^{-5}\ \mathrm{rad/s}", size=48, cores={0: VEL, 2: VEL})
        Y5b = caixa_l(Y5, VEL)
        self.pilha.poe(Y5b, dx=0.2)
        self.gat("sete vírgula duzentos")
        # v3 §7: TransformMatchingTex (o ω se repete de ω = 2π/T_sid para ω ≈ 7,292·10⁻⁵ rad/s; o resto sai e entra)
        self.tmt(Y4, Y5, [(r"\omega", VEL), ("=", None), (r"\frac{2\pi}{T_{\mathrm{sid}}}", None)],
                 [(r"\omega", VEL), (r"\approx", None), (r"7{,}292\times 10^{-5}\ \mathrm{rad/s}", VEL)], 52, 48, rt=1.1, extra=[FadeIn(Y5b[0])])
        self.foco = Y5b
        self.ate(0.99)

        # ── E3-4: São Paulo e v⃗ = ω⃗ × r⃗ (Terra grande + inset de zoom) ──
        self.an("E3-4")
        upd.clear_updaters()
        self.play(f3.op.animate.set_value(0.2), *self.troca_marcador(None), run_time=0.4)     # nunca a 0: o PALCO não fica vazio (SEM PALCO)
        self.pilha.so(Y5b)
        T["modo"] = "geo"
        T["rotg"] = 0.0
        NOMES = ("oeixo", "ow", "olat", "osp", "or", "orp", "ov", "oac", "orad", "opar", "olam")
        G = {k: 0.0 for k in NOMES}
        G.update(w=1.0, kw=KWG, kv=0.55, ka=0.85, lon=LON_SP, opT=1.0)
        T["g"] = G
        gtr = {k: ValueTracker(0.0) for k in NOMES}
        self.add(*gtr.values())
        sync = VGroup()
        sync.add_updater(lambda m: G.update({k: v.get_value() for k, v in gtr.items()}))
        self.add(sync)
        SP = np.array([math.cos(LAT) * math.cos(LON_SP), math.cos(LAT) * math.sin(LON_SP), math.sin(LAT)])
        om = np.array([0, 0, 1.0])
        v_ = np.cross(om, SP)
        ac_ = np.cross(om, np.cross(om, SP))
        self.reg("terra_vet", v=v_.tolist(), ac=ac_.tolist(), SP=SP.tolist(), K=KG, xc=XG, yc=YG)
        pj = lambda p: projeta3d(camG, np.asarray(p, float))
        Cs, SPs = pj((0, 0, 0)), pj(SP)
        d2 = lambda p: (lambda d: P3(d[0], d[1]))(un((pj(p) - SPs)[:2]))
        d_v, d_p, d_r = d2(SP + 0.05 * v_), d2(SP + 0.05 * un(ac_)), d2(SP * 0.95)
        ang = lambda d: math.atan2(d[1], d[0])
        # rótulos da vista principal (presos aos pontos projetados)
        l_w = mtex(r"\vec\omega", VEL, 52).next_to(pj((0, 0, 1.02 + KWG)), RIGHT, buff=0.22).shift(0.15 * DOWN)
        l_sp = txt("SÃO PAULO", 24).move_to(SPs + P3(2.0, 0.17))
        nr = un((SPs - Cs)[:2])
        l_r = fundo_txt(mtex(r"\vec r", GEO_, 44)).move_to((Cs + SPs) / 2 + 0.36 * P3(-nr[1], nr[0]) * (1 if nr[0] > 0 else -1))
        # inset de zoom (§7.5): disco PANEL com borda GEO, anel em São Paulo e a linha fina até ele, escala escrita
        u_l = un((CI - SPs)[:2])
        u_l = P3(u_l[0], u_l[1])
        anel = Circle(radius=0.17).move_to(SPs).set_stroke(GEO, 2.4).set_z_index(12)
        guia = Line(SPs + 0.19 * u_l, CI - (RI + 0.02) * u_l).set_stroke(GEO, 1.6, opacity=0.8).set_z_index(12)
        disco_i = Circle(radius=RI).move_to(CI).set_fill(PANEL, 0.92).set_stroke(GEO, 2.5).set_z_index(20)
        disco_i._fundo = True
        esc_i = txt("×3", 24, color=GEO_).move_to(CI + P3(RI * 0.8, -RI * 0.9))
        sp_i = Dot(CI, radius=0.07, color=WHITE_).set_z_index(24)
        rad_i = DashedLine(CI, CI + 0.7 * d_r, dash_length=0.08).set_stroke(WHITE_, 2.4, opacity=0.85).set_z_index(21)
        per_i = DashedLine(CI, CI + 0.7 * d_p, dash_length=0.08).set_stroke(GEO, 2.6, opacity=0.95).set_z_index(21)
        lam_i = arco(CI, 0.55, ang(d_r), ang(d_p), ANG, 11, z=22)
        v_i = seta(CI, CI + 0.9 * d_v, VEL, 9, tip=0.24, z=23)
        ac_i = seta(CI, CI + 0.56 * d_p, ACC, 6, tip=0.18, z=23)
        bis = P3(math.cos((ang(d_r) + ang(d_p)) / 2), math.sin((ang(d_r) + ang(d_p)) / 2))
        n_v = P3(-d_v[1], d_v[0]) * (1 if d_v[0] > 0 else -1)                     # normal "para cima" de v
        n_p = P3(-d_p[1], d_p[0]) * (-1 if d_p[0] > 0 else 1)                    # normal "para baixo" da reta para o eixo
        lv_i = mtex(r"\vec v", VEL, 48).move_to(CI + 0.62 * d_v + 0.68 * n_v).set_z_index(25)
        ll_i = lbl(r"\lambda", ANG, 48).move_to(CI + 1.0 * bis).set_z_index(25)
        lp_i = mtex(r"r_\perp", GEO_, 40).move_to(CI + 0.8 * d_p + 0.45 * n_p).set_z_index(25)
        la_i = mtex("a_c", ACC, 40).move_to(CI + 0.1 * d_p + 0.38 * n_p).set_z_index(25)
        self.play(f3.op.animate.set_value(1.0), gtr["oeixo"].animate.set_value(1.0), run_time=0.6)
        self.hip("TERRA ESFÉRICA · REFERENCIAL SEM GIRAR COM ELA")
        self.gat("com que velocidade são paulo anda")
        self.play(gtr["osp"].animate.set_value(1.0), gtr["olat"].animate.set_value(1.0), gtr["ow"].animate.set_value(1.0), FadeIn(l_w), FadeIn(l_sp), run_time=0.8)
        X1, ix1 = M(r"\vec v", "=", r"\vec\omega", r"\times", r"\vec r", size=60, cores={0: VEL, 2: VEL, 4: GEO_})
        self.pilha.poe(X1)
        self.gat("usa o produto vetorial")
        self.voa([(l_w, mp(X1, ix1, [2]))], extra=[FadeIn(mp(X1, ix1, [0, 1, 3, 4]))], rt=1.0, origem=False)
        self.gat("com o vetor que vai do centro da terra até são paulo")
        self.play(gtr["or"].animate.set_value(1.0), gtr["opar"].animate.set_value(1.0), FadeIn(l_r), run_time=0.8)
        self.gat("então vale")
        self.play(gtr["ov"].animate.set_value(1.0), Create(anel), Create(guia), FadeIn(disco_i), FadeIn(esc_i), FadeIn(sp_i), FadeIn(v_i), run_time=0.8)
        self.play(FadeIn(lv_i), run_time=0.4)
        self.gat("não até o centro")
        self.play(gtr["orp"].animate.set_value(1.0), gtr["opar"].animate.set_value(0.0), Create(rad_i), Create(per_i), Create(lam_i), FadeIn(lp_i), FadeIn(ll_i),
                  run_time=0.8)
        X2, ix2 = M(r"r_\perp", "=", "R", r"\cos\lambda", size=58, cores={0: GEO_, 2: GEO_})
        X2[0][ix2[3][3]].set_color(ANG)
        X2[0][ix2[3][3]].set_stroke(ANG, width=1.8, background=False)
        self.pilha.poe(X2)
        self.gat("essa distância é o raio da terra vezes o cosseno da latitude")
        self.voa([(lp_i, mp(X2, ix2, [0])), (l_r, mp(X2, ix2, [2])), (ll_i, VGroup(X2[0][ix2[3][3]]))],
                 extra=[FadeIn(mp(X2, ix2, [1])), FadeIn(VGroup(*[X2[0][j] for j in ix2[3][:3]]))], rt=1.3, origem=False)
        self.foco = X2
        self.ate(0.99)

        # ── E3-5: os números ──
        self.an("E3-5")
        self.sem_selo()
        self.pilha.so(Y5b, X2)
        LR, ilr = M("R", "=", r"6{.}371\ \mathrm{km}", size=36, cores={0: GEO_, 2: GEO_})
        LL, ill = M(r"\lambda", "=", r"23{,}55^\circ", size=36, cores={0: ANG, 2: ANG})
        LR.move_to(P3(0.1 - LR.width / 2, -3.0))                          # canto livre de baixo à direita (fora da Terra e do eixo)
        LL.move_to(P3(0.1 - LL.width / 2, -2.4)).align_to(LR, LEFT)
        self.gat("com o raio da terra")
        self.legenda(LR, ilr, l_r)
        self.gat("e a latitude de são paulo")
        self.legenda(LL, ill, ll_i)
        Z1, iz1 = M(r"r_\perp", "=", r"6{.}371\ \mathrm{km}", r"\cdot", r"\cos", r"23{,}55^\circ", size=46, cores={0: GEO_, 2: GEO_, 5: ANG})
        self.pilha.poe(Z1)
        self.gat("graus sul")
        self.voa([(mp(X2, ix2, [0]), mp(Z1, iz1, [0])), (mp(LR, ilr, [2]), mp(Z1, iz1, [2])), (mp(LL, ill, [2]), mp(Z1, iz1, [5]))],
                 extra=[FadeIn(mp(Z1, iz1, [1, 3, 4]))], rt=1.4, origem=False)
        Z1b, iz1b = M(r"\approx", r"5{.}840\ \mathrm{km}", size=46, cores={1: GEO_})
        self.pilha.poe(Z1b)
        self.gat("fica uns cinco mil")
        self.play(FadeIn(Z1b), run_time=0.6)
        Z2m, iz2 = M("v", "=", r"\omega", "R", r"\approx", r"465\ \mathrm{m/s}", size=46, cores={0: VEL, 2: VEL, 3: GEO_, 5: VEL})
        Z2 = linha_m(txt("EQUADOR:", 26, bold=True), Z2m, buff=0.15)
        self.pilha.poe(Z2)
        self.gat("no equador a velocidade seria")
        self.voa([(mp(Y5, iy5, [0]), mp(Z2m, iz2, [2])), (mp(LR, ilr, [0]), mp(Z2m, iz2, [3]))],
                 extra=[FadeIn(Z2[0]), FadeIn(mp(Z2m, iz2, [0, 1, 4, 5]))], rt=1.2, origem=False)
        Z3, iz3 = M("v", "=", r"\omega", "R", r"\cos\lambda", r"\approx", r"426\ \mathrm{m/s}", size=46, cores={0: VEL, 2: VEL, 3: GEO_, 6: VEL})
        Z3[0][iz3[4][3]].set_color(ANG)
        Z3[0][iz3[4][3]].set_stroke(ANG, width=1.8, background=False)
        Z3x = caixa_l(Z3, VEL)
        self.pilha.poe(Z3x, dx=0.2)
        self.gat("em são paulo quatrocentos")
        self.voa([(mp(Z2m, iz2, [2, 3]), mp(Z3, iz3, [2, 3])), (mp(X2, ix2, [3]), mp(Z3, iz3, [4]))],
                 extra=[FadeIn(Z3x[0]), FadeIn(mp(Z3, iz3, [0, 1, 5, 6]))], rt=1.3, origem=False)
        Z4m, iz4 = M(r"\approx", r"1{.}530\ \mathrm{km/h}", size=46, cores={1: VEL})
        Z4 = linha_m(Z4m, txt("PARA LESTE", 26, bold=True), buff=0.2)
        self.pilha.poe(Z4)
        self.gat("mais de mil e quinhentos")
        self.play(FadeIn(Z4), run_time=0.7)
        self.gat("e atenção ao referencial")
        self.selo("SÓ A ROTAÇÃO", "(NÃO É A VOLTA EM TORNO DO SOL)")       # D42: a nota vira selo (não cabe em uma linha a 24: duas, ver relatório)
        self.foco = Z3x
        self.ate(0.99)

        # ── E3-6: a_c para o eixo ──
        self.an("E3-6")
        self.play(FadeOut(self.s1), FadeOut(LR), FadeOut(LL), run_time=0.35)   # as legendas já serviram (saem antes do rótulo PARA O EIXO)
        self.remove(self.s1, LR, LL)
        self.s1 = None
        self.pilha.so(Z3x)
        self.gat("e a aceleração centrípeta de são paulo")
        self.play(gtr["ov"].animate.set_value(0.35), gtr["oac"].animate.set_value(1.0), v_i.animate.set_opacity(0.35), FadeOut(lv_i),
                  FadeIn(ac_i), run_time=0.8)
        self.play(FadeIn(la_i), run_time=0.4)
        W1, iw1 = M("a_c", "=", r"\omega^2", "R", r"\cos\lambda", size=52, cores={0: ACC, 2: VEL, 3: GEO_})
        W1[0][iw1[4][3]].set_color(ANG)
        W1[0][iw1[4][3]].set_stroke(ANG, width=1.8, background=False)
        self.pilha.poe(W1)
        self.gat("velocidade angular ao quadrado")
        # §5 E3-6: GM de v = ωR cos λ para a_c = ω²R cos λ (v vira a_c, o ² é novo, o ≈ 426 m/s sai)
        self.passo(Z3, W1, (J(iz3, 5, 6), []), (J(iz3, 0), J(iw1, 0)), (J(iz3, 1), J(iw1, 1)), (J(iz3, 2), iw1[2][:1]), ([], iw1[2][1:]),
                   (J(iz3, 3), J(iw1, 3)), (J(iz3, 4), J(iw1, 4)), rt=1.3, origem=False)
        W2, iw2 = M(r"\approx", r"0{,}031\ \mathrm{m/s^2}", size=48, cores={1: ACC})
        self.pilha.poe(W2)
        self.gat("uns três centésimos")
        self.play(FadeIn(W2), run_time=0.7)
        W3m, iw3 = M(r"\approx", r"0{,}32\%", size=48, cores={1: ACC})
        W3 = linha_m(W3m, txt("DE", 26, bold=True), lbl("g", ACC, 48), buff=0.15)
        self.pilha.poe(W3)
        self.gat("três décimos por cento")
        self.play(FadeIn(W3), run_time=0.7)
        lr_ = VGroup(txt("PARA O EIXO", 24, bold=True), txt("(NÃO PARA O CENTRO)", 24)).arrange(DOWN, buff=0.08)
        lr_.move_to(P3(0.12 - lr_.width / 2, -3.05))
        self.gat("para o eixo da terra não para o centro")
        self.play(gtr["orad"].animate.set_value(1.0), FadeIn(lr_), run_time=0.8)
        self.gat("um ângulo igual à latitude")
        self.play(ll_i.animate(rate_func=there_and_back).scale(1.15), lam_i.animate(rate_func=there_and_back).set_stroke(width=10), run_time=0.8)
        self.gat("conferindo no polo")
        self.confere([["POLO:", lbl(r"r_\perp", GEO_, 36), "= 0", lbl(r"\to", WHITE_, 36), lbl("v", VEL, 36), "= 0"],
                      ["EQUADOR:", lbl(r"r_\perp", GEO_, 36), "=", lbl("R", GEO_, 36), lbl(r"\to", WHITE_, 36), lbl("v", VEL, 36), "MÁXIMA",
                       lbl(r"\checkmark", WHITE_, 36)]])
        self.gat("e ficam duas dicas")
        self.sem_selo()                                                   # G7: um selo por vez (o CONFERE sai antes da DICA)
        self.pilha.x0, self.pilha.larg = X_CONTA + 0.2, LARG_CONTA - 0.2   # o respiro do pulso da DICA (larga) não entra na CALHA
        self.dica18([[lbl(r"\omega", VEL, 36), "EM RELAÇÃO A QUÊ?"], [lbl("r", GEO_, 36), "É A DISTÂNCIA AO EIXO"]])
        self.ate(0.99)
        mot.clear_updaters()

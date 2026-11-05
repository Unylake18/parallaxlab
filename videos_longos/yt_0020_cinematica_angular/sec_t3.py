"""Lote PT3 (v2): T3 — e quando o giro acelera? T3-1 α no disco grande (seta curva violeta ω crescendo, verde α). T3-2 três discos: ω por fora, α por dentro.
T3-3…T3-5: disco pequeno no alto à esquerda e gráfico ω(t) embaixo (ω₀ = 1,0 e α = 0,25 em unidades de tela). A tirinha ω dt pinta em âmbar NO MESMO
QUADRO em que o disco gira o dθ correspondente (auditoria ÁREA = ÂNGULO); a área se separa em retângulo ω₀t e triângulo ½αt². Inset da área com sinal:
ω(t) triângulo +2π e depois −2π (hachura), o disco vai e volta (Δθ = 0, giro total 4π). T3-5: eliminar t; o trapézio. T3-6: tabela linear × angular
(cada linha angular nasce da linear por TransformByGlyphMap copiado).
Álgebra do v2: nenhuma linha de equação da CONTA entra por FadeIn de linha inteira (escrita em ordem, voos do desenho, passo/TransformByGlyphMap)."""
import kit as _kit
from pecas20 import *  # noqa: F401,F403
from prob2 import _n_gl, troca_anim

W0, AL, TT = 1.0, 0.25, 6.0          # ω₀ (rad/s), α (rad/s²), duração do trecho do gráfico (s), todos de tela
CS, RS = P3(-4.0, 1.05), 1.45        # disco pequeno (T3-3…T3-5; v3 §4: ø 2,9 u, em cima do gráfico; topo em y 2,50 = limite do ESQUEMA)
GX0, GW = -6.35, 5.9                 # gráfico: borda esquerda e largura (cabe no ESQUEMA com os rótulos)
BGT = "#0B1530"                      # contorno escuro atrás de rótulo sobre área pintada


def Mm(*pares, size, final=None):
    """Proxy de TransformMatchingTex: o mesmo TeX da linha da CONTA (eqp), em partes (cada parte é uma chave do matching); a cor de cada glifo vem da
    linha final (`final`), para a fração d/dt não perder o ω violeta e o θ âmbar durante o voo."""
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


def disco_mini(c, r, th, z=3):
    g = VGroup(disco_aco(r, z).move_to(c), Line(c, c + r * P3(math.cos(th), math.sin(th))).set_stroke(WHITE_, 4).set_z_index(z + 2),
               eixo_mob(c, 0.07))
    return g


def sobre_area(m):
    """Rótulo dentro de área pintada: contorno escuro por trás (legibilidade sem mudar a cor da grandeza)."""
    m.set_stroke(BGT, 5, background=True)
    return m


def hachura(pts, cor=ANG, step=0.22, evita=None, w=1.6, op=0.8):
    """Hachura diagonal (y = x + c) dentro do polígono `pts`, sem passar pela caixa `evita` = (x0, y0, x1, y1) (rótulo dentro da área)."""
    pts = np.asarray(pts, float)
    P = _kit._Poli(pts)
    x0, x1, y0, y1 = pts[:, 0].min(), pts[:, 0].max(), pts[:, 1].min(), pts[:, 1].max()
    g = VGroup()
    for c in np.arange(y0 - x1, y1 - x0, step):
        xs = np.linspace(x0, x1, 56)
        ys = xs + c
        ok = P.contains_points(np.stack([xs, ys], 1))
        if evita is not None:
            ok &= ~((xs > evita[0]) & (xs < evita[2]) & (ys > evita[1]) & (ys < evita[3]))
        ini = None
        for i, v in enumerate(list(ok) + [False]):
            if v and ini is None:
                ini = i
            elif not v and ini is not None:
                if i - 1 > ini:
                    g.add(Line(P3(xs[ini], ys[ini]), P3(xs[i - 1], ys[i - 1])).set_stroke(cor, w, opacity=op))
                ini = None
    return g.set_z_index(3)


class LoteT3(L20):

    def construct(self):
        self.setup_base()
        self.t3()
        self.fim()
        self.relatorio()
        self.gravar_reg()

    def tmt(self, src, dst, ps, pd, size_s, size_d, key_map=None, rt=1.2, extra=()):
        """v3 §7: TransformMatchingTex entre a linha-mãe `src` (fica na tela) e a linha nova `dst` da Pilha; ps/pd: [(tex, cor)] são as chaves do matching
        (o mesmo TeX das linhas eqp, em partes). No fim a linha eqp `dst` assume o lugar dos proxies (mesma posição e mesmo desenho)."""
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

    def passo_arco(self, src, dst, *mapas, rt=1.3, arco=1.6, lag=0.35):
        """passo (GlyphMap) com os glifos em ARCO (path_arc) e mais atraso entre os grupos: nenhum atravessa em reta a linha-mãe (v2 §2.4 regra 4)."""
        print(f"[alg] {self._aid} passo mapas={len(mapas)} arco")
        x_dst = lambda e: min((dst[0][j].get_left()[0] for j in (e[1] if len(e) > 1 and isinstance(e[1], (list, tuple)) else [])), default=-1e9)
        mapas = tuple(sorted(mapas, key=x_dst))
        tops_antes = set(id(m) for m in self.mobjects)
        c = src.copy()
        self.add(c)

        def mor(a, b, **kw):
            if _n_gl(a) == _n_gl(b):
                return ReplacementTransform(a, b, path_arc=arco, **kw)
            return troca_anim(a, b, rate=smooth)
        tb_ = TransformByGlyphMap(c, dst, *mapas, default_transformer=mor, lag_ratio=lag)
        self._voando = set(id(x) for x in c.get_family()) | set(id(x) for x in dst.get_family()) | set(id(x) for x in tb_.mobject.get_family())
        self._voando_raiz = [c, dst, tb_.mobject]
        self._fontes_extra = [src]
        self.play(tb_, run_time=max(0.8, rt))      # a linha-mãe esmaece enquanto os glifos viajam: a cópia nunca briga com o original
        self._fontes_extra = []
        self._voando, self._voando_raiz = set(), []
        for m in list(self.mobjects):
            if m is c or (m is not dst and m is not src and any(x is c for x in m.get_family())):
                self.remove(m)
        alvo = self._linha_de(dst)
        self._assenta([], [alvo], revelados=[dst])
        self._sobras(tops_antes, [alvo])
        self.foco = alvo
        return dst

    def t3(self):
        d = DiscoRef(self, C=P3(-3.75, -0.55), R=2.45, th0=1.0)      # v3 §4: disco no tamanho do T1/T2 (ø 4,9 u ≈ 60% da altura); as setas ficam dentro da zona
        self.add(d.g)
        C, R = d.C, d.R
        # ── T3-1: α ──
        self.an("T3-1")
        self.secao("E QUANDO O GIRO ACELERA?")
        w = ValueTracker(0.6)
        self.add(w)
        hist = {"t": self.clk.get_value()}

        def gira(m):
            t = self.clk.get_value()
            d.th.set_value(d.th.get_value() + w.get_value() * (t - hist["t"]))
            hist["t"] = t
        mot = VGroup()
        mot.add_updater(gira)
        self.add(mot)
        opa = ValueTracker(0.0)
        self.add(opa)

        def setas():
            g = VGroup(seta_curva(C, R + 0.32, 0.55, 0.35 + 0.55 * w.get_value(), VEL, 8, tip=0.3))
            lw = mtex(r"\omega", VEL, 56).move_to(C + (R + 0.78) * P3(math.cos(0.45), math.sin(0.45)))
            g.add(lw)
            if opa.get_value() > 0.01:                                  # α do outro lado do ω (esquerda do disco), mesmo raio: nunca no caminho da seta violeta
                g.add(escala_op(seta_curva(C, R + 0.32, 2.45, 0.95, ACC, 8, tip=0.3), opa.get_value()))
                g.add(escala_op(mtex(r"\alpha", ACC, 56).move_to(C + (R + 0.8) * P3(math.cos(2.95), math.sin(2.95))), opa.get_value()))
            return g
        sv = vivo(setas)
        self.play(FadeIn(sv), run_time=0.5)
        self.gat("e se o giro muda de ritmo")
        self.play(w.animate(rate_func=linear).set_value(2.0), run_time=self.ate_t("aí entra a aceleração angular"))
        A1, ia = M(r"\alpha", "=", r"\frac{d\omega}{dt}", size=58, cores={0: ACC})       # d, dt e a barra brancos; ω violeta e θ âmbar pelo pós-passe do eqp (v3 §2)
        A2, ib = M(r"\alpha", "=", r"\frac{d^2\theta}{dt^2}", size=58, cores={0: ACC})
        self.pilha.poe(A1)
        self.pilha.poe(A2)
        self.gat("aí entra a aceleração angular")
        self.play(opa.animate.set_value(1.0), FadeIn(A1), run_time=0.9)
        self.gat("ou derivando duas vezes")
        # v3 §7: TransformMatchingTex (α e = se repetem; a fração dω/dt cede o lugar a d²θ/dt²)
        self.tmt(A1, A2, [(r"\alpha", ACC), ("=", None), (r"\frac{d\omega}{dt}", None)], [(r"\alpha", ACC), ("=", None), (r"\frac{d^2\theta}{dt^2}", None)],
                 58, 58, rt=1.3)
        U, iu = M(r"[\alpha]", "=", r"\mathrm{rad/s^2}", size=52, cores={0: ACC, 2: ACC})
        self.pilha.poe(U)
        self.gat("a unidade é radiano por segundo ao quadrado")
        self.play(FadeIn(U), run_time=0.6)
        self.ate(0.99)
        # ── T3-2: sinais ──
        self.an("T3-2")
        mot.clear_updaters()
        self.remove(mot)
        self.pilha.limpa(rt=0.3)
        RT2, YC = 1.05, 0.15                                              # v3 §4: três discos ø 2,1 u usando a largura toda do ESQUEMA (x −7,15…−0,25)
        CASOS = [(P3(-6.1, YC), 1, 1, "GIRANDO MAIS RÁPIDO"), (P3(-3.7, YC), 1, -1, "FREANDO"), (P3(-1.3, YC), -1, -1, "TAMBÉM ACELERANDO")]
        ths = [ValueTracker(0.3), ValueTracker(1.2), ValueTracker(2.4)]
        ws = [ValueTracker(0.6), ValueTracker(2.6), ValueTracker(-0.6)]
        self.add(*ths, *ws)
        hist2 = {"t": self.clk.get_value()}
        als = [0.1, -0.1, -0.1]                                           # α constante e suave: o ω muda de verdade, sem parar nem saturar em 20 s

        def gira3(m):
            t = self.clk.get_value()
            dt = t - hist2["t"]
            hist2["t"] = t
            for th, ww, a in zip(ths, ws, als):
                ww.set_value(ww.get_value() + a * dt)
                th.set_value(th.get_value() + ww.get_value() * dt)
        mot3 = VGroup()
        mot3.add_updater(gira3)
        op3 = ValueTracker(0.0)
        self.add(op3)

        def tres():
            g = VGroup()
            o = op3.get_value()
            for (c, sw, sa, nome), th, ww in zip(CASOS, ths, ws):
                w_ = ww.get_value()
                s_w = 1 if w_ >= 0 else -1
                Lw = min(1.5, 0.45 + 0.4 * abs(w_))                       # comprimento da seta violeta ∝ |ω|; as duas ficam no alto (centradas em 90°)
                g.add(escala_op(disco_mini(c, RT2, th.get_value()), o),
                      escala_op(seta_curva(c, RT2 + 0.62, PI / 2 - s_w * Lw / 2, s_w * Lw, VEL, 8, tip=0.28), o),                 # ω por fora
                      escala_op(seta_curva(c, RT2 + 0.3, PI / 2 - sa * 0.5, sa * 1.0, ACC, 8, tip=0.28), o))                        # α por dentro
            return g
        tv = vivo(tres)
        self.add(mot3)
        labs = VGroup()
        for c, sw, sa, nome in CASOS:
            l = VGroup(lbl(r"\omega" + (">0" if sw > 0 else "<0"), VEL, 38), lbl(r"\alpha" + (">0" if sa > 0 else "<0"), ACC, 38)).arrange(RIGHT, buff=0.25)
            t_ = VGroup(*[txt(w_, 26, bold=True) for w_ in nome.split(" ", 1)]).arrange(DOWN, buff=0.06)
            labs.add(VGroup(l, t_).arrange(DOWN, buff=0.14).move_to(P3(c[0], YC - RT2 - 1.0)))
        self.play(FadeOut(d.g), FadeOut(sv), op3.animate.set_value(1.0), FadeIn(tv), run_time=0.8)
        self.remove(d.g, sv)
        # v3 §4: a legenda da regra entra junto dos discos (a coluna não fica vazia 10 s); a segunda regra nasce na fala dela
        r1 = linha_m(txt("MESMO SINAL", 30, bold=True), lbl(r"\Rightarrow", WHITE_, 46), txt("MAIS RÁPIDO", 30, bold=True), buff=0.1)
        self.selo("SINAIS", [["DE", lbl(r"\omega", VEL, 34), "E DE", lbl(r"\alpha", ACC, 34)]])
        self.pilha.poe(r1)
        self.play(FadeIn(r1), run_time=0.5)
        self.gat("aceleração angular negativa não quer dizer")
        self.play(FadeIn(labs[2]), run_time=0.6)
        self.gat("se a velocidade angular e a aceleração angular têm o mesmo sinal")
        self.play(FadeIn(labs[0]), run_time=0.6)
        self.gat("se têm sinais opostos")
        self.play(FadeIn(labs[1]), run_time=0.6)
        r2 = linha_m(txt("SINAIS OPOSTOS", 30, bold=True), lbl(r"\Rightarrow", WHITE_, 46), txt("FREANDO", 30, bold=True), buff=0.1)
        self.pilha.poe(r2)
        self.play(FadeIn(r2), run_time=0.5)
        self.ate(0.99)
        # ── T3-3: gráfico ω(t) ──
        self.an("T3-3")
        G = Graf(GX0, -2.9, GW, 8.0, 0.0, 3.0, 0.8, rot_y=lbl(r"\omega", VEL, 42), rot_x=r"t", cor=GEO)
        G.ex.set_color(WHITE_)
        G.ex._partes = [("t", WHITE_)]                                   # v3 §6: o rótulo t do eixo registra a parte (COR POR TOKEN)
        ts = ValueTracker(0.0)
        th_s = 0.3
        self.add(ts)
        wf = lambda t: W0 + AL * t
        thf = lambda t: th_s + W0 * t + 0.5 * AL * t * t
        opA, opP, opR, opT, opG = (ValueTracker(0.0) for _ in range(5))
        self.add(opA, opP, opR, opT, opG)

        def palco():
            t = ts.get_value()
            g = VGroup(disco_mini(CS, RS, thf(t)))
            g.add(arco(CS, 0.78, th_s, thf(t), ANG, 8, 1.0, z=7) if t > 0.01 else VGroup())
            if opG.get_value() > 0.01:
                o = opG.get_value()
                g.add(G.curva(wf, 0.0, TT, cor=VEL, w=5).set_stroke(opacity=o))
                g.add(escala_op(Dot(G.pt(t, wf(t)), radius=0.07, color=VEL).set_z_index(9), o))
            if opA.get_value() > 0.01 and t > 0.02:
                o = opA.get_value()
                if opP.get_value() > 0.01:                                 # área inteira em âmbar 45% (some quando retângulo e triângulo assumem)
                    g.add(Polygon(G.pt(0, 0), G.pt(0, W0), G.pt(t, wf(t)), G.pt(t, 0)).set_stroke(width=0).set_fill(ANG, 0.45 * opP.get_value()).set_z_index(3))
                dt = min(0.18, t)                                          # tirinha ω dt em âmbar 100%
                g.add(Polygon(G.pt(t - dt, 0), G.pt(t - dt, wf(t - dt)), G.pt(t, wf(t)), G.pt(t, 0)).set_stroke(ANG, 2, opacity=o).set_fill(ANG, 1.0 * o).set_z_index(4))
                if not PEDIDOS3D:
                    area = W0 * t + 0.5 * AL * t * t
                    self.reg("area_angulo", area=area, dth=thf(t) - th_s, t=t)
            return g
        pv = vivo(palco)
        self.pilha.limpa(rt=0.6, anims=[FadeOut(tv), FadeOut(labs), FadeIn(pv), FadeIn(G.eixos)])
        self.remove(tv, labs)
        # v3 §4: o selo da regra do gráfico ocupa a coluna desde o começo (35,5–45,3 s não fica vazia); a equação entra na fala dela
        self.selo("ACELERAÇÃO", [["CONSTANTE ·", lbl(r"\omega", VEL, 34), "CRESCE"], ["EM LINHA RETA"]])
        self.gat("aceleração angular constante")
        self.play(opG.animate.set_value(1.0), run_time=0.6)
        self.gat("cresce como uma reta no tempo")
        self.play(ts.animate(rate_func=linear).set_value(TT), run_time=3.0)
        B, ib = M(r"\omega", "=", r"\omega_0", "+", r"\alpha", "t", size=60, cores={0: VEL, 2: VEL, 4: ACC})
        self.pilha.poe(B)
        lw0 = lbl(r"\omega_0", VEL, 40).next_to(G.pt(0, W0), LEFT, buff=0.3)
        self.gat("velocidade angular igual à velocidade angular inicial")
        self.play(FadeIn(lw0), run_time=0.4)
        self.voa([(lw0, mp(B, ib, [2]))], extra=[FadeIn(mp(B, ib, [0, 1]))], rt=0.9)
        self.gat("a inclinação dessa reta")
        q0, q1 = G.pt(2.0, wf(2.0)), G.pt(5.0, wf(5.0))
        tri = VGroup(Line(q0, P3(q1[0], q0[1])).set_stroke(ACC, 3), Line(P3(q1[0], q0[1]), q1).set_stroke(ACC, 3))
        la = lbl(r"\alpha", ACC, 42)
        la.move_to(P3(q1[0] + 0.22 + la.width / 2, q0[1] + 0.25 * (q1[1] - q0[1])))
        self.play(Create(tri), FadeIn(la), run_time=0.7)
        self.voa([(la, mp(B, ib, [4])), (G.ex, mp(B, ib, [5]))], extra=[FadeIn(mp(B, ib, [3]))], rt=1.0, origem=False)
        self.ate(0.99)
        # ── T3-4: a área é o ângulo ──
        self.an("T3-4")
        self.play(FadeOut(tri), FadeOut(la), ts.animate.set_value(0.0), run_time=0.6)
        self.gat("olha a área embaixo dessa reta")
        self.play(opA.animate.set_value(1.0), opP.animate.set_value(1.0), ts.animate(rate_func=linear).set_value(0.8), run_time=1.6)
        self.gat("que é uma tirinha fina de área")
        l_strip = M(r"\omega", "dt'", size=40, cores={0: VEL})[0]
        l_strip.move_to(P3(-5.3, -1.15))
        lead_strip = Line(P3(-5.45, -1.42), G.pt(0.8, wf(0.8)) + 0.04 * UP).set_stroke(ANG, 1.6)
        strip_g = VGroup(l_strip, lead_strip)
        self.play(FadeIn(strip_g), run_time=0.5)
        self.wait(0.5)
        self.gat("somando todas as tirinhas")
        self.play(ts.animate(rate_func=linear).set_value(TT), run_time=self.ate_t("a integral da velocidade angular"))
        D1, i1 = M(r"\Delta\theta", "=", r"\int_0^t", r"\omega\,dt'", size=58, cores={0: ANG})
        self.pilha.poe(D1)                                                # ω violeta (mesma saturação dos outros) e ∫, limites, dt′ brancos pelo eqp (v3 §2)
        self.gat("a integral da velocidade angular")
        self.voa([(l_strip, mp(D1, i1, [3]))], extra=[FadeIn(mp(D1, i1, [0, 1, 2]))], rt=1.4, origem=False)
        self.foco = D1
        self.wait(0.6)
        rect = Rectangle(width=G.w * TT / G.tmax, height=G.hpu * W0).move_to((G.pt(0, 0) + G.pt(TT, W0)) / 2).set_stroke(ANG, 2.5).set_fill(ANG, 0.0)
        triang = Polygon(G.pt(0, W0), G.pt(TT, wf(TT)), G.pt(TT, W0)).set_stroke(ANG, 2.5).set_fill(ANG, 0.70)
        sep = Line(G.pt(0, W0), G.pt(TT, W0)).set_stroke(WHITE_, 1.6).set_z_index(5)
        l_rect = sobre_area(lbl(r"\omega_0 t", ANG, 44)).move_to(rect.get_center())
        l_tri = sobre_area(lbl(r"\tfrac12\alpha t^2", ANG, 36)).move_to(G.pt(TT * 0.84, W0) + 0.40 * UP)
        cot_t = VGroup(Line(G.pt(0, 0) + 0.3 * DOWN, G.pt(TT, 0) + 0.3 * DOWN).set_stroke(GEO, 2), lbl("t", WHITE_, 40).next_to(G.pt(TT / 2, 0) + 0.3 * DOWN, DOWN, buff=0.05))
        cot_h = VGroup(Line(G.pt(TT, W0) + 0.3 * RIGHT, G.pt(TT, wf(TT)) + 0.3 * RIGHT).set_stroke(GEO, 2), M(r"\alpha", "t", size=40, cores={0: ACC})[0])
        cot_h[1].next_to(cot_h[0], RIGHT, buff=0.12)
        self.gat("o retângulo é a velocidade angular inicial vezes o tempo")
        self.play(Create(rect), FadeIn(l_rect), FadeIn(cot_t), run_time=0.9)
        self.gat("e o triângulo")
        self.play(FadeIn(triang), FadeIn(cot_h), FadeIn(sep), opP.animate.set_value(0.0), rect.animate.set_fill(ANG, 0.45), run_time=0.8)
        self.gat("vale meio vezes a aceleração angular")
        self.play(FadeIn(l_tri), run_time=0.6)
        D2, i2 = M(r"\Delta\theta", "=", r"\omega_0", "t", "+", r"\tfrac12", r"\alpha", "t^2", size=58, cores={0: ANG, 2: VEL, 6: ACC})
        self.pilha.poe(D2)
        self.voa([(gl(D1, i1[0]), mp(D2, i2, [0])), (l_rect, mp(D2, i2, [2, 3])), (l_tri, mp(D2, i2, [5, 6, 7]))], extra=[FadeIn(mp(D2, i2, [1, 4]))], rt=1.2, origem=False)
        # Δθ = θ − θ₀  →  θ = θ₀ + …  (θ₀ atravessa o "=")
        P1, ip = M(r"\theta", "-", r"\theta_0", "=", r"\omega_0", "t", "+", r"\tfrac12", r"\alpha", "t^2", size=58, cores={0: ANG, 2: ANG, 4: VEL, 8: ACC})
        D3, i3 = M(r"\theta", "=", r"\theta_0", "+", r"\omega_0", "t", "+", r"\tfrac12", r"\alpha", "t^2", size=58, cores={0: ANG, 2: ANG, 4: VEL, 8: ACC})
        D3b = caixa_l(D3, ANG)
        self.pilha.poe(P1)
        self.pilha.poe(D3b, dx=0.2)
        self.passo_arco(D2, P1, (i2[0][:1], []), (i2[0][1:], ip[0]), (J(i2, 1), J(ip, 3)), (J(i2, 2), J(ip, 4)), (J(i2, 3), J(ip, 5)), (J(i2, 4), J(ip, 6)),
                   (J(i2, 5), J(ip, 7)), (J(i2, 6), J(ip, 8)), (J(i2, 7), J(ip, 9)), ([], J(ip, 1, 2)), rt=1.3)
        self.gat("é o giro a mais que a aceleração deu")
        self.passo(P1, D3, (J(ip, 0), J(i3, 0)), (J(ip, 1), []), (J(ip, 2), J(i3, 2)), (J(ip, 3), J(i3, 1)), (J(ip, 4), J(i3, 4)), (J(ip, 5), J(i3, 5)),
                   (J(ip, 6), J(i3, 6)), (J(ip, 7), J(i3, 7)), (J(ip, 8), J(i3, 8)), (J(ip, 9), J(i3, 9)), ([], J(i3, 3)), rt=1.3, origem=False)
        self.play(FadeIn(D3b[0]), run_time=0.3)                          # v3 §5.5: a caixa do resultado entra depois do conteúdo (nunca uma caixa vazia)
        self.foco = D3b
        self.wait(1.4)
        # inset: área com sinal
        self.gat("só um cuidado")
        self.selo("ÁREA COM SINAL", "")
        self.pilha.so(D3b)
        velhos = VGroup(rect, triang, sep, l_rect, l_tri, cot_t, cot_h, G.eixos, lw0, strip_g)
        self.play(FadeOut(velhos), opA.animate.set_value(0.0), opG.animate.set_value(0.0), run_time=0.5)
        G2 = Graf(GX0, -2.2, GW, 8.0, -PI, PI, 0.42, rot_y=lbl(r"\omega", VEL, 40), rot_x=r"t", cor=GEO)
        G2.ex.set_color(WHITE_)
        G2.ex._partes = [("t", WHITE_)]                                  # v3 §6: registra a parte do rótulo t (COR POR TOKEN)
        wi = lambda t: PI * (1 - abs(t - 2) / 2) if t <= 4 else -PI * (1 - abs(t - 6) / 2)
        ti = ValueTracker(0.0)
        self.add(ti)
        th_i0 = thf(TT)

        def thi(t):
            if t <= 4:
                return (PI * t * t / 4) if t <= 2 else (2 * PI - PI * (4 - t) ** 2 / 4)
            u = t - 4
            return 2 * PI - ((PI * u * u / 4) if u <= 2 else (2 * PI - PI * (4 - u) ** 2 / 4))
        lp = sobre_area(lbl(r"+2\pi", ANG, 36)).move_to(G2.pt(2, 1.1))
        lm = sobre_area(lbl(r"-2\pi", ANG, 36)).move_to(G2.pt(6, -1.1))
        ev = (lm.get_left()[0] - 0.22, lm.get_bottom()[1] - 0.18, lm.get_right()[0] + 0.22, lm.get_top()[1] + 0.18)
        # v3 §5.5: as duas áreas já preenchidas (âmbar 22%, a de baixo com hachura) e rotuladas desde que o inset entra; a varredura pinta 45% por cima
        pts_c = [G2.pt(0, 0), G2.pt(2, PI), G2.pt(4, 0)]
        pts_b = [G2.pt(4, 0), G2.pt(6, -PI), G2.pt(8, 0)]
        fant = VGroup(Polygon(*pts_c).set_stroke(ANG, 1.5, opacity=0.6).set_fill(ANG, 0.22).set_z_index(2),
                      Polygon(*pts_b).set_stroke(ANG, 1.5, opacity=0.6).set_fill(ANG, 0.22).set_z_index(2), hachura(pts_b, ANG, 0.2, ev, op=0.45))

        def inset():
            t = ti.get_value()
            g = VGroup(disco_mini(CS, RS, th_i0 + thi(t)), G2.curva(wi, 0.0, 8.0, cor=VEL, w=5))
            if t > 0.02:
                t1 = min(t, 4.0)
                pts = [G2.pt(0, 0)] + [G2.pt(u, wi(u)) for u in np.linspace(0, t1, 30)] + [G2.pt(t1, 0)]
                g.add(Polygon(*pts).set_stroke(ANG, 2).set_fill(ANG, 0.45).set_z_index(3))
            if t > 4.02:
                pts = [G2.pt(4, 0)] + [G2.pt(u, wi(u)) for u in np.linspace(4, t, 30)] + [G2.pt(t, 0)]
                g.add(Polygon(*pts).set_stroke(ANG, 2).set_fill(ANG, 0.45).set_z_index(3), hachura(pts, ANG, 0.2, ev))
            g.add(Dot(G2.pt(t, wi(t)), radius=0.07, color=VEL).set_z_index(9))
            if not PEDIDOS3D:
                self.reg("inset_sinal", t=t, dth=thi(t))
            return g
        iv = vivo(inset)
        self.remove(pv)
        self.play(FadeIn(G2.eixos), FadeIn(iv), FadeIn(fant), FadeIn(lp), FadeIn(lm), run_time=0.5)
        self.gat("se o disco inverter o sentido")
        self.play(ti.animate(rate_func=linear).set_value(4.0), run_time=2.4)
        self.gat("a parte abaixo do eixo conta negativo")
        self.play(ti.animate(rate_func=linear).set_value(8.0), run_time=4.4)
        E1a, ie = M(r"\Delta\theta", "=", r"+2\pi", r"-2\pi", size=56, cores={0: ANG, 2: ANG, 3: ANG})
        E1b, ie2 = M("=", "0", size=56, cores={1: ANG})
        self.pilha.poe(E1a)
        self.pilha.poe(E1b)
        self.gat("tem deslocamento angular zero")
        self.voa([(lp, mp(E1a, ie, [2])), (lm, mp(E1a, ie, [3]))], extra=[FadeIn(mp(E1a, ie, [0, 1]))], rt=1.2, origem=False)
        self.passo(E1a, E1b, (J(ie, 1), J(ie2, 0)), (J(ie, 2, 3), J(ie2, 1)), rt=1.2, origem=False)
        E1c, ic = M(r"=", r"2\pi", "+", r"2\pi", size=52, cores={1: ANG, 3: ANG})
        E1d, id_ = M("=", r"4\pi", size=52, cores={1: ANG})
        E1g = linha_m(txt("GIRO TOTAL", 28, bold=True), E1c, buff=0.2)
        self.pilha.poe(E1g)
        self.pilha.poe(E1d)
        self.gat("mas girou quatro pi radianos no total")
        self.play(FadeIn(E1g), run_time=0.9)
        self.passo(E1c, E1d, (J(ic, 0), J(id_, 0)), (J(ic, 1, 2, 3), J(id_, 1)), rt=1.2, origem=False)
        self.foco = E1d
        self.ate(0.99)
        # ── T3-5: eliminando t; o trapézio ──
        self.an("T3-5")
        self.sem_selo()
        ts.set_value(TT)
        opA.set_value(1.0)
        opP.set_value(1.0)
        opG.set_value(1.0)
        self.pilha.limpa(rt=0.5, anims=[FadeOut(iv), FadeOut(fant), FadeOut(G2.eixos), FadeOut(lp), FadeOut(lm), FadeIn(pv), FadeIn(G.eixos)])
        self.remove(iv, fant)
        E_a, ea = M(r"\omega", "=", r"\omega_0", "+", r"\alpha", "t", size=52, cores={0: VEL, 2: VEL, 4: ACC})
        E_b, eb = M(r"\Delta\theta", "=", r"\omega_0", "t", "+", r"\tfrac12", r"\alpha", "t^2", size=52, cores={0: ANG, 2: VEL, 6: ACC})
        T_, it = M("t", "=", r"\frac{\omega-\omega_0}{\alpha}", size=52)
        for j in (it[2][0], it[2][2], it[2][3]):
            T_[0][j].set_color(VEL)
            T_[0][j].set_stroke(VEL, width=1.8, background=False)
        T_[0][it[2][5]].set_color(ACC)
        T_[0][it[2][5]].set_stroke(ACC, width=1.8, background=False)
        self.pilha.poe(E_a)
        self.pilha.poe(E_b)
        self.pilha.poe(T_)
        self.play(FadeIn(E_a), FadeIn(E_b), run_time=0.7)
        self.gat("se você eliminar o tempo")
        # GM isolando t: ω₀ e α atravessam o "=" (ω₀ vira "− ω₀" no numerador, α desce para o denominador)
        self.passo(E_a, T_, (J(ea, 5), J(it, 0)), (J(ea, 1), J(it, 1)), (J(ea, 0), it[2][0:1]), (J(ea, 3), it[2][1:2]), (J(ea, 2), it[2][2:4]),
                   ([], it[2][4:5]), (J(ea, 4), it[2][5:6]), rt=1.4, origem=False)
        F_, if_ = M(r"\omega^2", "=", r"\omega_0^2", "+", "2", r"\alpha", r"\Delta\theta", size=58, cores={0: VEL, 2: VEL, 5: ACC, 6: ANG})
        Fb = caixa_l(F_, VEL)
        self.pilha.poe(Fb, dx=0.2)
        self.gat("velocidade angular ao quadrado igual")
        # v3 §7: TransformMatchingTex a partir de ω = ω₀ + αt (=, + e α se repetem; ω, ω₀ e t saem; ω², ω₀², o 2 e o Δθ entram)
        self.tmt(E_a, F_, [(r"\omega", VEL), ("=", None), (r"\omega_0", VEL), ("+", None), (r"\alpha", ACC), ("t", None)],
                 [(r"\omega^2", VEL), ("=", None), (r"\omega_0^2", VEL), ("+", None), ("2", None), (r"\alpha", ACC), (r"\Delta\theta", ANG)],
                 52, 58, rt=1.4, extra=[FadeIn(Fb[0])])       # sem key_map: o Manim 0.21 não aceita chave com número de glifos diferente (ω → ω²)
        self.foco = Fb
        self.gat("olhando a mesma área como um trapézio")
        trap = Polygon(G.pt(0, 0), G.pt(0, W0), G.pt(TT, wf(TT)), G.pt(TT, 0)).set_stroke(WHITE_, 4).set_fill(ANG, 0.0).set_z_index(6)
        lb0 = lbl(r"\omega_0", VEL, 40).next_to(G.pt(0, W0 / 2), LEFT, buff=0.3)
        lb1 = lbl(r"\omega", VEL, 40).next_to(G.pt(TT, wf(TT) / 2), RIGHT, buff=0.3)
        lt = lbl("t", WHITE_, 40).next_to(G.pt(TT / 2, 0), DOWN, buff=0.3)
        self.play(Create(trap), FadeIn(lb0), FadeIn(lb1), FadeIn(lt), run_time=0.9)
        H_, ih = M(r"\Delta\theta", "=", r"\tfrac12", r"(\omega_0", "+", r"\omega)", "t", size=58, cores={0: ANG})
        for j in ih[3][1:] + ih[5][:-1]:
            H_[0][j].set_color(VEL)
            H_[0][j].set_stroke(VEL, width=1.8, background=False)
        self.pilha.poe(caixa_l(H_, ANG), dx=0.2)
        self.gat("é a média das velocidades angulares")
        self.voa([(lb0, VGroup(*[H_[0][j] for j in ih[3][1:]])), (lb1, VGroup(*[H_[0][j] for j in ih[5][:-1]])), (lt, mp(H_, ih, [6]))],
                 extra=[FadeIn(self.pilha.ultima()[0]), FadeIn(mp(H_, ih, [0, 1, 2, 4])), FadeIn(H_[0][ih[3][0]]), FadeIn(H_[0][ih[5][-1]])], rt=1.1, origem=False)
        self.foco = H_
        self.ate(0.99)
        # ── T3-6: a mesma matemática ──
        self.an("T3-6")
        self.selo("MESMA MATEMÁTICA", "")
        lin = [M("v", "=", "v_0", "+", "a", "t", size=46, cores={0: VEL, 2: VEL, 4: ACC}),
               M("x", "=", "x_0", "+", "v_0", "t", "+", r"\tfrac12", "a", "t^2", size=46, cores={4: VEL, 8: ACC}),
               M("v^2", "=", "v_0^2", "+", "2", "a", r"\Delta x", size=46, cores={0: VEL, 2: VEL, 5: ACC}), M(r"\Delta x", "=", r"\tfrac12", r"(v_0+v)", "t", size=46)]
        ang_ = [M(r"\omega", "=", r"\omega_0", "+", r"\alpha", "t", size=46, cores={0: VEL, 2: VEL, 4: ACC}),
                M(r"\theta", "=", r"\theta_0", "+", r"\omega_0", "t", "+", r"\tfrac12", r"\alpha", "t^2", size=46, cores={0: ANG, 2: ANG, 4: VEL, 8: ACC}),
                M(r"\omega^2", "=", r"\omega_0^2", "+", "2", r"\alpha", r"\Delta\theta", size=46, cores={0: VEL, 2: VEL, 5: ACC, 6: ANG}),
                M(r"\Delta\theta", "=", r"\tfrac12", r"(\omega_0+\omega)", "t", size=46, cores={0: ANG})]
        for M_, ix in ((lin[3][0], lin[3][1]), (ang_[3][0], ang_[3][1])):       # (v₀ + v) e (ω₀ + ω): as velocidades de dentro do parêntese na cor delas
            for j in (ix[3][1], ix[3][2], ix[3][4]):
                M_[0][j].set_color(VEL)
                M_[0][j].set_stroke(VEL, width=1.8, background=False)
        for L_, il in lin:                                               # posição 1D em GEO (x ↔ θ)
            for k, t_ in enumerate(L_._partes):
                if t_[0] in ("x", "x_0", r"\Delta x"):
                    for j in il[k]:
                        L_[0][j].set_color(GEO_)
        t_l = txt("MOVIMENTO EM LINHA", 28, bold=True)
        t_a = txt("GIRO", 28, bold=True)
        antigas = self.pilha.linhas                                      # posições da tabela calculadas antes de limpar: o PALCO nunca fica vazio (SEM PALCO)
        self.pilha.linhas = []
        self.pilha.poe(t_a)
        for L_, il in ang_:
            self.pilha.poe(L_)
        novas = self.pilha.linhas
        self.pilha.linhas = antigas
        XL = -6.9                                                        # coluna da esquerda (ESQUEMA), alinhada às linhas da CONTA
        t_l.move_to(P3(XL + t_l.width / 2, t_a.get_y()))
        for k in range(4):
            lin[k][0].move_to(P3(XL + lin[k][0].width / 2, ang_[k][0].get_y()))
        lin[0][0]._dono = t_l                                            # linha de dado sob o título da coluna (RÓTULO SOLTO: o título é o "dono")
        self.pilha.limpa(rt=0.5, anims=[FadeOut(VGroup(trap, lb0, lb1, lt, G.eixos)), FadeOut(pv), FadeIn(t_l), FadeIn(t_a)])
        self.pilha.linhas = novas
        self.remove(pv)
        opA.set_value(0.0)
        opG.set_value(0.0)
        pares = VGroup(*[linha_m(lbl(a, ca, 44), lbl(r"\leftrightarrow", WHITE_, 44), lbl(b, c, 44), buff=0.12) for a, b, c, ca in
                         (("x", r"\theta", ANG, GEO_), ("v", r"\omega", VEL, VEL), ("a", r"\alpha", ACC, ACC))]).arrange(RIGHT, buff=0.55)
        pares.move_to(P3(XL + pares.width / 2, -2.6))
        self.gat("são exatamente as equações do movimento")
        for k in range(4):
            self.play(Write(lin[k][0]), run_time=0.45)
        self.gat("com o ângulo no lugar da posição")
        self.play(FadeIn(pares[0]), run_time=0.5)
        self.gat("a velocidade angular no lugar da velocidade")
        self.play(FadeIn(pares[1]), run_time=0.5)
        self.gat("e a aceleração angular no lugar da aceleração")
        self.play(FadeIn(pares[2]), run_time=0.5)
        self.gat("e não é coincidência")
        for k in range(4):                                               # GM copiado da linha linear: x → θ, v → ω, a → α; a linha 1D fica
            (Lk, ik), (Ak, ika) = lin[k], ang_[k]
            c = Lk.copy()                                                # a cópia viaja inteira até a coluna GIRO (rígida: nenhum glifo cruza outro)
            self.add(c)
            self._voando, self._voando_raiz = set(id(x) for x in c.get_family()), [c]
            self.play(c.animate.shift((Ak.get_left()[0] - c.get_left()[0]) * RIGHT), run_time=0.5)
            self._voando, self._voando_raiz = set(), []
            self.remove(c)
            self.passo(c, Ak, *[(J(ik, i), J(ika, i)) for i in range(len(ik))], rt=0.8, origem=False)       # e só então x → θ, v → ω, a → α no lugar
        self.gat("então a física nova não está aqui")
        self.foco = ang_[3][0]
        self.ate(0.99)

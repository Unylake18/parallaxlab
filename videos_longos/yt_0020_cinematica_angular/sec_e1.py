"""Lote PE1 (v2): E1 — o ventilador que desliga (2D). ESQUEMA fixo à esquerda: ventilador de teto visto de baixo (2,5D: pás com degradê, sombra suave, cubo com volume),
raio 0,60 m até a ponta. Simulação com os valores reais: ω₀ = 10π rad/s, α = −π/3 rad/s², parada em 30 s. Tempo de tela comprimido 30 s → 10 s (fator 3);
o desenho gira a 1/30 do ω real (marcador de canto CÂMERA LENTA ×30). O contador Δθ acumulado (0 → 471 rad, 0 → 75 voltas) e o mostrador (Δθ mod 2π, em graus)
ficam presos ao ventilador e saem da mesma variável (auditoria MOSTRADOR: reg "mostrador"). E1-3 gráfico ω(t) com o triângulo âmbar pintado junto
(ÁREA = ÂNGULO). E1-4 faixa 0–10 s (5/9 da área). E1-5 setas na ponta FORA DE ESCALA (marcador de canto) com inset de zoom ×2; E1-6 escala log
(0,1 a 1.000 m/s²) × t: |a_t| = 0,63 fixo e a_c(t) caindo, cruzando em t = 29,0 s. Toda linha da CONTA é escrita em ordem (voos do desenho, passo, TMT)."""
from pecas20 import *  # noqa: F401,F403
from sec_t3 import Mm  # noqa: F401  (proxy de TransformMatchingTex, v3 §7)

W0, AL0, T_P, RP = 10 * PI, -PI / 3, 30.0, 0.60
FATOR_T = 3.0                 # s de simulação por s de tela
LENTA = 30.0                  # o desenho gira a ω_real / 30
FC_, FR = P3(-3.9, 0.35), 1.7     # centro e raio (cena) do ventilador; K = FR / 0.60
AF = -0.5                     # ângulo da pá marcada em E1-5/E1-6 (a ponta fica embaixo à direita, com folga para o inset)
Y_MARC = -3.4                 # marcador de canto (CÂMERA LENTA / FORA DE ESCALA)


def w_real(ts):
    return max(0.0, W0 + AL0 * min(ts, T_P))


def th_real(ts):
    t = min(ts, T_P)
    return W0 * t + 0.5 * AL0 * t * t


def tab(s, cor, size, padrao):
    """v3 §5.4: número em células de largura fixa (alinhado à direita; `padrao` = o maior texto do campo), para o contador não tremer nem trocar de largura."""
    def adv(ch, w0):
        return 0.45 * w0 if ch in ",." else (0.75 * w0 if ch == "°" else w0 + 0.03)
    g = num_mob(s, cor, size)
    w0 = num_mob("0", cor, size)[0].width
    cur = 0.0
    for m, ch in reversed(list(zip(g, s))):
        a = adv(ch, w0)
        m.set_x(cur - a / 2)
        cur -= a
    campo = sum(adv(ch, w0) for ch in padrao)
    g.campo = campo
    return g


def ventilador_e1(c, R, ang, n=3):
    """Ventilador 2,5D: sombra suave deslocada, pás de aço com degradê, filete de luz na borda, cubo em disco de aço com tampa e parafusos."""
    c = np.asarray(c, float)
    sombra, pas = VGroup(), VGroup()
    off = np.array([0.05 * R, -0.075 * R, 0.0])
    fs = np.linspace(0.2, 1.0, 16)

    def hw(f):
        k = 1.0 if f < 0.92 else 1.0 - 0.6 * (f - 0.92) / 0.08
        return R * (0.068 + 0.05 * math.sin(PI * (f - 0.2) / 0.8)) * k

    for k in range(n):
        a = ang + 2 * PI * k / n
        u, t = P3(math.cos(a), math.sin(a)), P3(-math.sin(a), math.cos(a))
        cur = lambda f: 0.05 * R * f * f
        esq = [c + u * R * f + t * (cur(f) - hw(f)) for f in fs]
        dir_ = [c + u * R * f + t * (cur(f) + hw(f)) for f in fs]
        pts = esq + dir_[::-1]
        sombra.add(Polygon(*[p + off for p in pts]).set_stroke(width=0).set_fill("#000000", 0.24))
        pas.add(aco(Polygon(*pts), 1.6).set_z_index(5))
        fil = [c + u * R * f + t * (cur(f) + hw(f) * 0.55) for f in fs[2:13]] + [c + u * R * f + t * (cur(f) + hw(f) * 0.92) for f in fs[2:13][::-1]]
        pas.add(Polygon(*fil).set_stroke(width=0).set_fill(WHITE_, 0.17).set_z_index(5))
    sombra.set_z_index(4)
    hub = disco_aco(0.27 * R, z=6).move_to(c)
    cap = Circle(radius=0.11 * R).set_fill("#1A2234", 1).set_stroke("#7FB2FF", 1.6, opacity=0.8).move_to(c).set_z_index(7)
    br = Arc(radius=0.1 * R, start_angle=0.9 * PI, angle=0.5 * PI, arc_center=c).set_stroke(WHITE_, 1.4, opacity=0.55).set_z_index(8)
    par = VGroup(*[Dot(c + 0.19 * R * P3(math.cos(ang + 2 * PI * k / 3 + 0.5), math.sin(ang + 2 * PI * k / 3 + 0.5)), radius=0.018 * R * 2.4)
                   .set_color("#C7D2E5").set_z_index(8) for k in range(3)])
    return VGroup(sombra, pas, hub, cap, br, par)


class LoteE1(L20):

    def construct(self):
        self.setup_base()
        self.e1()
        self.fim()
        self.relatorio()
        self.gravar_reg()

    def tmt(self, src, dst, ps, pd, size_s, size_d, key_map=None, rt=1.2, extra=()):
        """v3 §7: TransformMatchingTex entre a linha-mãe `src` (fica na tela) e a linha nova `dst` da Pilha (mesmo molde do sec_t3): ps/pd = [(tex, cor)] são as
        chaves do matching; no fim a linha eqp `dst` assume o lugar dos proxies."""
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

    def e1(self):
        self.an("E1-1")
        self.secao("EXERCÍCIO 1 · O VENTILADOR QUE DESLIGA")
        # relógio do desenho: antes de desligar gira a ω₀/30; depois segue th_real(ts)/90 (ts = 3 · tempo de tela); termina em AF (a pá marcada)
        S = {"ang0": 0.3, "K": 1.0, "ts": 0.0, "modo": "liga", "t": self.clk.get_value(), "ang": 0.3}

        def motor(m):
            t = self.clk.get_value()
            dt = t - S["t"]
            S["t"] = t
            if S["modo"] == "liga":
                S["ang"] += W0 / LENTA * dt
            elif S["modo"] == "freia":
                S["ts"] = min(T_P, S["ts"] + FATOR_T * dt)
                S["ang"] = S["ang0"] + S["K"] * th_real(S["ts"]) / th_real(T_P)
                if not PEDIDOS3D:
                    self.reg("e1_sim", ts=S["ts"], th=th_real(S["ts"]), w=w_real(S["ts"]), ang=S["ang"])
        mot = VGroup()
        mot.add_updater(motor)
        self.add(mot)
        fan = vivo(lambda: ventilador_e1(FC_, FR, S["ang"]))
        self.play(FadeIn(fan), *self.troca_marcador("CÂMERA LENTA ×30", y=Y_MARC), run_time=0.8)
        arc_w = seta_curva(FC_, FR + 0.3, 1.95, 0.75, VEL, 8)        # v3 §3: setas curvas na espessura do G8, número grande na cor da grandeza
        l_w = valor(r"300\ \mathrm{RPM}", VEL, 40).move_to(P3(-6.5, 2.05))

        def cx(m, cor):                                      # v3 §3: caixa do resultado com borda na cor da família; acompanha a linha se a Pilha a reposicionar
            b = caixa(m, cor, buff=0.14)
            b.set_stroke(cor, 3.2)
            b.add_updater(lambda x: x.move_to(m))
            return b
        y_t = FC_[1] - FR                                    # v3 §5.3: a cota GEO vai do eixo à ponta da pá (raio vertical) e o rótulo fica na ponta
        cota_r = VGroup(Line(FC_, P3(FC_[0], y_t)).set_stroke(GEO, 3.2), Line(P3(FC_[0] - 0.13, y_t), P3(FC_[0] + 0.13, y_t)).set_stroke(GEO, 3.2),
                        Dot(P3(FC_[0], y_t), radius=0.06, color=GEO)).set_z_index(10)
        l_r = M("r", "=", r"0{,}60\ \mathrm{m}", size=40, cores={0: GEO_, 2: GEO_})[0].next_to(P3(FC_[0], y_t), DOWN, buff=0.36).shift(0.45 * RIGHT)
        # v3 §5.1: o número do rótulo original fica a 40% enquanto a cópia voa (sem cópia sobre o original). UpdateFromAlphaFunc sobre o próprio l_r (uma fatia
        # em ApplyMethod entraria na cena como grupo à parte e levaria os glifos `r =` embora).
        def _op(k, de, ate):
            return UpdateFromAlphaFunc(l_r, lambda m, a: [g.set_opacity(de + (ate - de) * a) for g in m[0][2:k]], suspend_mobject_updating=False)
        dim_r = lambda k=6: _op(k, 1.0, 0.4)
        des_r = lambda k=6: _op(k, 0.4, 1.0)
        l_p = VGroup(txt("PARA EM", 26, bold=True), valor(r"30\ \mathrm{s}", WHITE_, 40)).arrange(DOWN, buff=0.1).move_to(P3(-1.0, 1.65))
        Da, ida = M(r"\omega_0", "=", r"300\ \mathrm{RPM}", size=50, cores={0: VEL, 2: VEL})
        Db, idb = M("r", "=", r"0{,}60\ \mathrm{m}", size=50, cores={0: GEO_, 2: GEO_})
        Dc, idc = M(r"\Delta t", "=", r"30\ \mathrm{s}", size=50)
        self.gat("gira a trezentas rotações por minuto")
        self.play(Create(arc_w), FadeIn(l_w), run_time=0.7)
        self.pilha.poe(Da)
        self.voa([(l_w[0], mp(Da, ida, [2]))], extra=[FadeIn(mp(Da, ida, [0, 1]))], rt=1.0)
        self.gat("com pás de sessenta centímetros")
        self.play(Create(cota_r), FadeIn(l_r), run_time=0.7)
        self.pilha.poe(Db)
        self.voa([(l_r[0][2:7], mp(Db, idb, [2]))], extra=[FadeIn(mp(Db, idb, [0, 1])), dim_r(7)], rt=1.0)
        self.gat("desligado ele para em trinta segundos")
        self.play(FadeIn(l_p), des_r(7), run_time=0.5)
        self.pilha.poe(Dc)
        self.voa([(l_p[1][0], mp(Dc, idc, [2]))], extra=[FadeIn(mp(Dc, idc, [0, 1]))], rt=1.0)
        self.gat("com aceleração angular constante")
        self.hip([[lbl(r"\alpha", ACC, 36), "CONSTANTE ATÉ PARAR"]])
        self.gat("quantas voltas ele dá até parar")
        self.selo("PEDE", [[lbl(r"\alpha", ACC, 36), "E AS ACELERAÇÕES DA PONTA"]])
        self.ate(0.99)
        # ── E1-2: ω₀ e α ──
        self.an("E1-2")
        self.pilha.limpa(rt=0.3)
        A1, ia1 = M(r"\omega_0", "=", "300", r"\cdot", r"\frac{2\pi}{60}", size=50, cores={0: VEL, 2: VEL})
        A1b, ia1b = M("=", r"10\pi", r"\approx", r"31{,}4\ \mathrm{rad/s}", size=50, cores={1: VEL, 3: VEL})
        self.pilha.poe(A1)
        self.gat("primeiro tudo em radianos")
        self.voa([(l_w[0][:3], mp(A1, ia1, [2]))], extra=[FadeIn(mp(A1, ia1, [0, 1, 3, 4]))], rt=1.0)
        self.pilha.poe(A1b)
        self.gat("dez pi radianos por segundo")
        self.play(FadeIn(A1b), run_time=1.0)
        A2, ia2 = M(r"\alpha", "=", r"\frac{0-31{,}4}{30}", size=50, cores={0: ACC})
        g2 = ia2[2]                                  # frac: 0, −, 3, 1, ',', 4, barra, 3, 0
        for j in g2[2:6]:
            A2[0][j].set_color(VEL)
        A2b, ia2b = M("=", r"-\frac{\pi}{3}", r"\approx", r"-1{,}05\ \mathrm{rad/s^2}", size=50, cores={1: ACC, 3: ACC})
        self.pilha.poe(A2)
        self.gat("a aceleração angular é a variação")
        self.voa([(mp(A1b, ia1b, [3])[:4], VGroup(*[A2[0][j] for j in g2[2:6]])), (l_p[1][0][:2], VGroup(*[A2[0][j] for j in g2[7:9]]))],
                 extra=[FadeIn(VGroup(*[A2[0][j] for j in ia2[0] + ia2[1] + [g2[0], g2[1], g2[6]]]))], rt=1.3)
        self.pilha.poe(A2b)
        self.gat("menos pi sobre três")
        self.play(FadeIn(A2b), run_time=1.0)
        bxA = cx(A2b, ACC)
        self.play(FadeIn(bxA), run_time=0.3)
        arc_a = seta_curva(FC_, FR + 0.3, 4.276, -0.75, ACC, 8)
        l_a = lbl(r"\alpha", ACC, 42).move_to(P3(-6.45, -0.4))
        self.gat("sinal contrário ao da velocidade angular")
        self.play(Create(arc_a), FadeIn(l_a), run_time=0.7)
        so = linha_m(txt("SINAIS OPOSTOS", 26, bold=True), lbl(r"\Rightarrow", WHITE_, 40), txt("FREANDO", 26, bold=True), buff=0.14)
        self.pilha.poe(so)
        self.play(FadeIn(so), run_time=0.5)
        self.ate(0.99)
        # ── E1-3: o triângulo; 471 rad = 75 voltas; mostrador × acumulado ──
        self.an("E1-3")
        self.pilha.limpa(rt=0.3, anims=[FadeOut(l_p), FadeOut(bxA)])
        self.remove(bxA)
        self.pilha.topo = -0.7
        G = Graf(1.7, 0.15, 4.4, 32.0, 0.0, W0, 0.052, rot_y=lbl(r"\omega", VEL, 38), rot_x=r"t", cor=GEO)
        G.ex.set_color(WHITE_)
        G.ex._partes = [("t", WHITE_)]                       # v3 §6: a MathTex `t` do eixo do Graf sem partes registradas
        G.ey.move_to(P3(G.x0 + 0.55, G.y0 + W0 * 0.052 + 0.32))
        l31 = lbl(r"10\pi", VEL, 36).next_to(G.pt(0, W0), LEFT, buff=0.26)
        l30 = lbl(r"30\ \mathrm{s}", WHITE_, 36).next_to(G.pt(30, 0), DOWN, buff=0.26)
        opT, faixa = ValueTracker(0.0), ValueTracker(0.0)
        self.add(opT, faixa)

        def graf():
            ts = S["ts"]
            g = VGroup(G.curva(w_real, 0.0, 30.0, cor=VEL, w=5))
            if ts > 0.05:
                pts = [G.pt(0, 0), G.pt(0, W0), G.pt(ts, w_real(ts)), G.pt(ts, 0)]
                g.add(Polygon(*pts).set_stroke(ANG, 2).set_fill(ANG, 0.45).set_z_index(3))
            g.add(Dot(G.pt(ts, w_real(ts)), radius=0.07, color=VEL).set_z_index(9))
            f = faixa.get_value()
            if f > 0.01:
                pts = [G.pt(0, 0), G.pt(0, W0), G.pt(10, w_real(10)), G.pt(10, 0)]
                g.add(Polygon(*pts).set_stroke(WHITE_, 3, opacity=f).set_fill(ANG, 1.0 * f).set_z_index(4))
            return g
        gv = vivo(graf)

        dth_, un_rad = lbl(r"\Delta\theta", ANG, 40), lbl(r"\mathrm{rad}", ANG, 40)
        sim_ig, sim_ap = lbl("=", WHITE_, 40), lbl(r"\approx", WHITE_, 40)
        un_vol = txt("VOLTAS", 26, bold=True)
        X0C, YC1, YC2 = -5.6, -2.8, -3.3                       # contador: bordas e linhas fixas (células de largura fixa: nada tremelica)
        xs_ = X0C + dth_.width + 0.16 + sim_ig.width / 2        # centro fixo do "=" / "≈"
        CAMPO_R, CAMPO_V = tab("000", ANG, 40, "000").campo, tab("00,0", WHITE_, 40, "00,0").campo

        def pon(g, xr, yb):
            """alinha a borda direita do campo em xr e a base dos dígitos em yb"""
            g.shift(P3(xr, yb - g[0].get_bottom()[1]))
            return g

        def contadores():
            ts = S["ts"]
            th = th_real(ts)
            fim_ = th >= 150 * PI - 0.5
            vt = th / (2 * PI)
            g = VGroup()
            d_, sm_, ur_ = dth_.copy().move_to(P3(X0C + dth_.width / 2, YC1)), (sim_ap if fim_ else sim_ig).copy().move_to(P3(xs_, YC1)), un_rad.copy()
            xl_ = xs_ + sim_ig.width / 2 + 0.14
            nr_ = pon(tab(f"{max(th, 0.0):.0f}", ANG, 40, "000"), xl_ + CAMPO_R, YC1 - 0.13)
            ur_.move_to(P3(xl_ + CAMPO_R + 0.1 + ur_.width / 2, YC1))
            g.add(VGroup(d_, sm_, nr_, ur_))
            vtxt = "75" if fim_ else f"{max(vt, 0.0):.1f}".replace(".", ",")
            nv_ = pon(tab(vtxt, WHITE_, 40, "00,0"), X0C + CAMPO_V, YC2 - 0.13)
            uv_ = un_vol.copy()
            uv_.move_to(P3(X0C + CAMPO_V + 0.14 + uv_.width / 2, YC2))
            g.add(VGroup(nv_, uv_))
            return g
        cv = vivo(contadores)

        def mostrador():
            th = th_real(S["ts"])
            mod = math.degrees(th) % 360.0
            if mod > 359.999:
                mod = 0.0
            mi = int(mod)
            if not PEDIDOS3D:
                self.reg("mostrador", mostrador_deg=float(mi), acum_rad=th, mod_deg=mod)
            nm_ = tab(f"{mi:d}°", ANG, 46, "000°")
            tit_ = txt("MOSTRADOR", 26, bold=True).move_to(P3(-0.85, 0.7))
            pon(nm_, -0.85 + nm_.campo / 2, 0.12)
            return VGroup(tit_, nm_)
        mv = vivo(mostrador)
        self.play(FadeIn(G.eixos), FadeIn(gv), FadeIn(l31), FadeIn(l30), FadeIn(cv), FadeIn(mv), run_time=0.7)
        self.gat("a área embaixo do gráfico")
        S["modo"], S["ang0"] = "freia", S["ang"]
        S["K"] = 5.236 + ((AF - S["ang"] - 5.236 + PI) % (2 * PI) - PI)       # a pá marcada termina exatamente em AF (aceleração suave, sem salto)
        S["t"] = self.clk.get_value()
        self.wait(T_P / FATOR_T + 0.2)
        C1, ic1 = M(r"\Delta\theta", "=", r"\tfrac12", r"\cdot", r"10\pi", r"\cdot", "30", size=50, cores={0: ANG, 4: VEL})
        C1b, ic1b = M("=", r"150\pi", r"\approx", r"471\ \mathrm{rad}", size=50, cores={1: ANG, 3: ANG})
        self.pilha.poe(C1)
        self.gat("metade de dez pi vezes trinta")
        self.voa([(l31[0], mp(C1, ic1, [4])), (l30[0][:2], mp(C1, ic1, [6]))], extra=[FadeIn(mp(C1, ic1, [0, 1, 2, 3, 5]))], rt=1.3)
        self.pilha.poe(C1b)
        self.gat("dá cento e cinquenta pi radianos")
        self.play(FadeIn(C1b), run_time=1.0)
        C2, ic2 = M(r"\frac{150\pi}{2\pi}", "=", "75", r"\ \mathrm{VOLTAS}", size=50, cores={2: WHITE_})
        f2 = ic2[0]                                  # frac: 1, 5, 0, π, barra, 2, π
        for j in f2[:4] + f2[5:7]:
            C2[0][j].set_color(ANG)
        self.pilha.poe(C2, dx=0.2)
        self.gat("dividindo por dois pi")
        self.passo(C1b, C2, (J(ic1b, 1), f2[:4]), rt=1.5)
        bxC = cx(C2, ANG)
        self.play(FadeIn(bxC), run_time=0.3)
        self.gat("e repara no mostrador")
        rr = RoundedRectangle(corner_radius=0.1, width=1.9, height=1.15).move_to(P3(-0.85, 0.35)).set_stroke(WHITE_, 3).set_fill(opacity=0)
        rr._fundo = True
        self.play(FadeIn(rr), run_time=0.4)
        self.play(FadeOut(rr), run_time=0.5)
        self.ate(0.99)
        # ── E1-4: 0 a 10 s ──
        self.an("E1-4")
        self.pilha.limpa(rt=0.3, anims=[FadeOut(bxC)])
        self.remove(bxC)
        self.pilha.topo = -0.8                                    # folga entre a equação do ângulo e os rótulos do eixo (10 s, 30 s)
        l10 = lbl(r"10\ \mathrm{s}", WHITE_, 36).next_to(G.pt(10, 0), DOWN, buff=0.26)
        l314 = lbl(r"31{,}4", VEL, 36).next_to(G.pt(0, W0), LEFT, buff=0.26)
        l_al = lbl(r"\alpha\approx-1{,}05", ACC, 36).move_to(P3(5.4, 1.10))
        D1, id1 = M(r"\Delta\theta", "=", r"31{,}4", r"\cdot", "10", size=50, cores={0: ANG, 2: VEL})
        D1b, id1b = M("-", r"\tfrac12", r"\cdot", r"1{,}05", r"\cdot", r"10^2", size=50, cores={3: ACC})
        D2, id2 = M(r"\approx", r"262\ \mathrm{rad}", r"\approx", r"41{,}7", size=50, cores={1: ANG})
        D2l = linha_m(D2, txt("VOLTAS", 26, bold=True), buff=0.15)
        # v3 §7: a equação do ângulo entra em símbolos e vira a forma com |α| por TransformMatchingTex (Δθ, =, ω₀t, ½ e t² se repetem; + vira −; α sai e |α| entra)
        PG1 = [(r"\Delta\theta", ANG), ("=", None), (r"\omega_0 t", ANG), ("+", None), (r"\tfrac12", ANG), (r"\alpha", ACC), ("t^2", ANG)]
        PG2 = [(r"\Delta\theta", ANG), ("=", None), (r"\omega_0 t", ANG), ("-", None), (r"\tfrac12", ANG), (r"|\alpha|", ACC), ("t^2", ANG)]
        G1, _ = M(*[p[0] for p in PG1], size=50, cores={0: ANG, 2: ANG, 4: ANG, 5: ACC, 6: ANG})
        G2, _ = M(*[p[0] for p in PG2], size=50, cores={0: ANG, 2: ANG, 4: ANG, 5: ACC, 6: ANG})
        self.pilha.poe(G1)
        self.pilha.poe(G2)
        self.gat("quanto ele gira nos primeiros dez segundos")
        self.play(FadeIn(G1), TransformMatchingTex(l31, l314), FadeIn(l10), FadeIn(l_al), run_time=1.0)       # os rótulos do gráfico entram aqui, longe do voo da equação
        self.gat("com a equação do ângulo")
        self.tmt(G1, G2, PG1, PG2, 50, 50, key_map={"+": "-"}, rt=1.0)
        self.pilha.poe(D1)
        self.voa([(l314[0], mp(D1, id1, [2])), (l10[0][:2], mp(D1, id1, [4]))], extra=[FadeIn(mp(D1, id1, [0, 1, 3]))], rt=1.1)
        eq_x = D1[0][id1[1][0]].get_left()[0] - self.pilha.x0
        self.pilha.poe(D1b, dx=eq_x)
        self.gat("menos meio vezes um vírgula zero cinco vezes cem")
        self.voa([(l_al[0][3:], mp(D1b, id1b, [3])), (l10[0][:2], mp(D1b, id1b, [5])[:2])],
                 extra=[FadeIn(VGroup(mp(D1b, id1b, [0, 1, 2, 4]), D1b[0][id1b[5][2]]))], rt=1.4)
        self.pilha.poe(D2l, dx=eq_x - 0.2)
        self.gat("uns duzentos e sessenta e dois radianos")
        self.play(FadeIn(D2l), run_time=1.0)
        self.gat("no gráfico dá para ver")
        self.play(faixa.animate.set_value(1.0), run_time=0.8)
        l59 = VGroup(lbl(r"\tfrac{5}{9}", ANG, 44), txt("DA ÁREA", 24, bold=True)).arrange(RIGHT, buff=0.14).move_to(P3(4.85, 1.78))
        self.play(FadeIn(l59), run_time=0.5)
        self.ate(0.99)
        # ── E1-5: a ponta no instante em que desliga (FORA DE ESCALA, inset de zoom ×2) ──
        self.an("E1-5")
        self.pilha.limpa(rt=0.3, anims=[faixa.animate.set_value(0.0), FadeOut(l59), FadeOut(l_al), FadeOut(l10)])
        am_ = self.troca_marcador("FORA DE ESCALA", y=Y_MARC)
        self.play(FadeOut(gv), FadeOut(G.eixos), FadeOut(l314), FadeOut(l30), FadeOut(cv), FadeOut(mv), *am_[:1], run_time=0.4)
        self.remove(gv, cv, mv)
        self.pilha.topo = min(TOPO_PILHA, self.s1.get_bottom()[1] - 0.15) if self.s1 is not None else TOPO_PILHA
        S["modo"] = "parado"
        a = AF
        u, n = P3(math.cos(a), math.sin(a)), P3(-math.sin(a), math.cos(a))
        p = FC_ + FR * u
        ia_c, ia_t = 0.6, 0.45
        sv_ = VGroup(seta(p, p + 1.15 * n, VEL, 6, z=12), seta(p, p - ia_t * n, ACC, 6, z=12), seta(p, p - ia_c * u, ACC, 7, z=12))
        l_v = mtex("v", VEL, 42).move_to(p + 1.15 * n + 0.38 * n + 0.1 * u)
        # inset: disco com borda GEO, a ponta ampliada ×2 (pá, a_c e a_t) e os rótulos fora do círculo
        Ci, ri = P3(-0.7, -1.0), 0.9
        Ai = Ci + P3(0.5, 0.0)
        disc = Circle(radius=ri).move_to(Ci).set_stroke(GEO, 3).set_fill(PANEL, 0.85)
        disc._fundo = True
        disc.set_z_index(18)
        tt = P3(-math.sin(a), math.cos(a))
        stub = aco(Polygon(Ai - tt * 0.18, Ai + tt * 0.18, Ai - u * 1.0 + tt * 0.36, Ai - u * 1.0 - tt * 0.36), 1.4).set_z_index(19)
        ia_ = VGroup(seta(Ai, Ai - 2 * ia_t * n, ACC, 6, z=21), seta(Ai, Ai - 2 * ia_c * u, ACC, 7, z=21))
        if not PEDIDOS3D:                                      # v3 §6: razão a_c : a_t do inset (FORA DE ESCALA: desenhada ≈ 1,3 : 1; real ≈ 940 : 1)
            self.reg("e1_5_inset", ac_len=2 * ia_c, at_len=2 * ia_t, razao_tela=ia_c / ia_t, razao_real=(W0 ** 2 * RP) / (RP * PI / 3), fora_de_escala=True)
        d_ct = (Ai - 2 * ia_c * u) - Ci
        d_tt = (Ai - 2 * ia_t * n) - Ci
        d_ct, d_tt = d_ct / np.linalg.norm(d_ct), d_tt / np.linalg.norm(d_tt)
        l_ic = mtex("a_c", ACC, 40).move_to(Ci + P3(-0.35, ri + 0.4))
        l_it = mtex("a_t", ACC, 40).move_to(Ci + d_tt * (ri + 0.42))
        esc = txt("×2", 24, bold=True).move_to(Ci + P3(-0.5, -0.5)).set_z_index(22)
        dr = (Ci - p) / np.linalg.norm(Ci - p)
        anel = Circle(radius=0.28).move_to(p).set_stroke(GEO, 2.2).set_fill(opacity=0).set_z_index(13)
        lig = Line(p + dr * 0.28, Ci - dr * ri).set_stroke(GEO, 1.6, opacity=0.9).set_z_index(13)
        inset = VGroup(disc, stub, ia_, esc)
        self.gat("agora a ponta da pá")
        self.play(*am_[1:], FadeIn(sv_), FadeIn(l_v), FadeIn(anel), FadeIn(lig), FadeIn(inset), FadeIn(l_ic), FadeIn(l_it), run_time=0.9)
        E1_, ie1 = M("v_0", "=", r"0{,}60", r"\cdot", r"31{,}4", size=50, cores={0: VEL, 2: GEO_, 4: VEL})
        E1b, ie1b = M(r"\approx", r"18{,}8\ \mathrm{m/s}", size=50, cores={1: VEL})
        self.pilha.poe(E1_)
        self.gat("a velocidade é zero vírgula sessenta")
        self.voa([(l_r[0][2:6], mp(E1_, ie1, [2])), (l_w[0][:3], mp(E1_, ie1, [4]))], extra=[FadeIn(mp(E1_, ie1, [0, 1, 3])), dim_r()], rt=1.3)
        self.pilha.poe(E1b, dx=E1_[0][ie1[1][0]].get_left()[0] - self.pilha.x0)
        self.play(FadeIn(E1b), des_r(), run_time=0.8)
        Ea, iea = M("a_c", "=", r"31{,}4^2", r"\cdot", r"0{,}60", size=50, cores={0: ACC, 2: VEL, 4: GEO_})
        Eb, ieb = M(r"\approx", r"592\ \mathrm{m/s^2}", r"\approx", "60", "g", size=50, cores={1: ACC, 3: ACC, 4: ACC})
        self.pilha.poe(Ea)
        self.gat("a aceleração centrípeta é a velocidade angular ao quadrado")
        self.voa([(mp(E1_, ie1, [4]), mp(Ea, iea, [2])), (l_r[0][2:6], mp(Ea, iea, [4]))], extra=[FadeIn(mp(Ea, iea, [0, 1, 3])), dim_r()], rt=1.3)
        self.pilha.poe(Eb, dx=Ea[0][iea[1][0]].get_left()[0] - self.pilha.x0)
        self.gat("uns quinhentos e noventa e dois metros por segundo ao quadrado")
        self.play(FadeIn(Eb), des_r(), run_time=1.0)
        Ec, iec = M("a_t", "=", r"0{,}60", r"\cdot", r"1{,}05", size=50, cores={0: ACC, 2: GEO_, 4: ACC})
        Ed, ied = M(r"\approx", r"0{,}63\ \mathrm{m/s^2}", size=50, cores={1: ACC})
        self.pilha.poe(Ec)
        self.gat("e a tangencial")
        self.voa([(l_r[0][2:6], mp(Ec, iec, [2])), (l_a[0], mp(Ec, iec, [4]))], extra=[FadeIn(mp(Ec, iec, [0, 1, 3])), dim_r()], rt=1.3)
        self.pilha.poe(Ed, dx=Ec[0][iec[1][0]].get_left()[0] - self.pilha.x0)
        self.play(FadeIn(Ed), des_r(), run_time=0.8)
        self.gat("dez segundos depois")
        self.pilha.limpa(rt=0.3)
        E4 = linha_m(txt("EM", 26, bold=True), M("t", "=", r"10\ \mathrm{s}", size=46)[0], txt(":", 26, bold=True), buff=0.12)
        E5, ie5 = M(r"\omega", r"\approx", r"20{,}9\ \mathrm{rad/s}", size=50, cores={0: VEL, 2: VEL})
        E6, ie6 = M("a_c", r"\approx", r"263\ \mathrm{m/s^2}", size=50, cores={0: ACC, 2: ACC})
        E7, ie7 = M(r"\varphi", r"\approx", r"0{,}14^\circ", size=50, cores={0: ANG, 2: ANG})
        self.pilha.poe(E4)
        self.pilha.poe(E5)
        self.play(FadeIn(E4), FadeIn(E5), run_time=1.2)
        self.gat("e a centrípeta ainda está em duzentos e sessenta e três")
        self.pilha.poe(E6)
        self.play(FadeIn(E6), run_time=0.9)
        self.gat("o ângulo dela com o raio")
        self.pilha.poe(E7)
        self.play(FadeIn(E7), run_time=0.9)
        self.ate(0.99)
        # ── E1-6: quando a tangencial passa a centrípeta (escala log) ──
        self.an("E1-6")
        self.pilha.limpa(rt=0.3)
        self.pilha.topo = -0.65
        self.pilha.topo_fixo = True
        lx0, ly0, lw_, lh_ = 1.9, 0.2, 4.2, 1.3           # eixo log: 10^-1 … 10^3 → 4 décadas
        dec = lh_ / 4
        Y = lambda a_: ly0 + (math.log10(max(a_, 0.1)) + 1) * dec
        X = lambda t: lx0 + lw_ * t / 30
        eixos = VGroup(Line(P3(lx0, ly0), P3(lx0 + lw_ + 0.2, ly0)).set_stroke(GEO, 3), Line(P3(lx0, ly0), P3(lx0, ly0 + lh_ + 0.1)).set_stroke(GEO, 3))
        for k, s_ in enumerate(("0{,}1", "1", "10", "100", "1000")):
            eixos.add(Line(P3(lx0 - 0.08, ly0 + k * dec), P3(lx0, ly0 + k * dec)).set_stroke(GEO, 2))
            if k in (0, 2, 4):
                eixos.add(lbl(s_.replace("1000", "10^3"), ACC, 36).next_to(P3(lx0 - 0.08, ly0 + k * dec), LEFT, buff=0.2))
        eixos.add(lbl(r"\mathrm{m/s^2}", WHITE_, 36).next_to(P3(lx0 + 0.2, ly0 + lh_ + 0.1), UP, buff=0.04).align_to(P3(lx0 + 0.2, 0), LEFT))
        eixos.add(lbl("t", WHITE_, 36).next_to(P3(lx0 + lw_ + 0.2, ly0), RIGHT, buff=0.06))
        at_c = RP * PI / 3
        lin_t = Line(P3(X(0), Y(at_c)), P3(X(30), Y(at_c))).set_stroke(ACC, 5)
        curva = VMobject().set_points_as_corners([P3(X(t), Y(w_real(t) ** 2 * RP)) for t in np.linspace(0, 29.999, 300)]).set_stroke(ACC, 5)
        l_at = lbl(r"|a_t|", ACC, 36).next_to(P3(X(8), Y(at_c)), UP, buff=0.22)
        l_ac = lbl("a_c", ACC, 36).next_to(P3(X(20), Y(w_real(20) ** 2 * RP)), UP, buff=0.26)      # v3 §5.2: afastado do `m/s²` do eixo
        tc = NUM["tcruz"]
        ult = Rectangle(width=X(30) - X(tc), height=lh_).move_to(P3((X(tc) + X(30)) / 2, ly0 + lh_ / 2)).set_stroke(width=0).set_fill(ACC, 0.25)
        mk = DashedLine(P3(X(tc), ly0), P3(X(tc), ly0 + lh_), dash_length=0.06).set_stroke(WHITE_, 2)
        l29 = lbl(r"29{,}0\ \mathrm{s}", WHITE_, 36).next_to(P3(X(tc), ly0), DOWN, buff=0.26).shift(0.35 * LEFT)
        self.reg("e1_6", tc=tc, wc=NUM["wcruz"], at=at_c)
        self.gat("e quando a aceleração tangencial da freada")
        self.play(FadeIn(eixos), run_time=0.6)
        self.gat("com os mesmos zero vírgula sessenta e três o tempo todo")
        self.play(Create(lin_t), FadeIn(l_at), run_time=0.8)
        self.gat("só que a aceleração que mantém a ponta")
        self.play(Create(curva), FadeIn(l_ac), run_time=1.4)
        F1, if1 = M(r"|a_t|", ">", "a_c", size=50)
        F2, if2 = M(r"\iff", r"r\,|\alpha|", ">", r"\omega^2 r", size=50)
        for j, c in zip(if2[1], (GEO_, WHITE_, ACC, WHITE_)):
            F2[0][j].set_color(c)
        for j, c in zip(if2[3], (VEL, VEL, GEO_)):
            F2[0][j].set_color(c)
        F3, if3 = M(r"\iff", r"\omega^2", "<", r"|\alpha|", size=50, cores={1: VEL, 3: ACC})
        F4, if4 = M(r"\iff", r"\omega", "<", r"1{,}02\ \mathrm{rad/s}", size=50, cores={1: VEL, 3: VEL})
        F5, if5 = M(r"\omega", "=", r"\omega_0", "+", r"\alpha", "t", size=50, cores={0: VEL, 2: VEL, 4: ACC})
        F6, if6 = M(r"\Longrightarrow", "t", ">", r"29{,}0\ \mathrm{s}", size=50)
        self.pilha.poe(F1)
        self.gat("a distância ao eixo cancela dos dois lados")
        self.play(FadeIn(F1), run_time=0.8)
        self.pilha.poe(F2)
        self.play(FadeIn(F2), run_time=1.0)
        rk = VGroup(risco(VGroup(F2[0][if2[1][0]]), cor=WHITE_, w=3), risco(VGroup(F2[0][if2[3][-1]]), cor=WHITE_, w=3))
        self.play(Create(rk), run_time=0.5)
        self.pilha.poe(F3)
        self.gat("velocidade angular ao quadrado menor")
        self.passo(F2, F3, (J(if2, 0), J(if3, 0)), (if2[3][:2], if3[1]), (if2[2], if3[2]), (if2[1][1:], if3[3]), rt=1.3)
        self.play(FadeOut(rk), run_time=0.3)
        self.pilha.poe(F4)
        self.gat("abaixo de um vírgula zero dois")
        self.passo(F3, F4, (J(if3, 0), J(if4, 0)), (if3[1][:1], if4[1]), (if3[2], if4[2]), rt=1.3)
        self.pilha.poe(F5)
        self.play(FadeIn(F5), run_time=0.9)
        self.pilha.poe(F6, dx=0.3)
        self.gat("depois dos vinte e nove segundos")
        self.passo(F5, F6, (if5[5], if6[1]), rt=1.2)
        bx6 = RoundedRectangle(corner_radius=0.1, width=F6.width + 0.36, height=F6.height + 0.2).set_stroke(ACC, 3).set_fill(opacity=0)
        bx6.move_to(F6)
        bx6.align_to(P3(self.pilha.x0, 0), LEFT)
        bx6._fundo = bx6._caixa = True
        bx6.add_updater(lambda b: b.move_to(F6))         # a Pilha pode reposicionar F6 depois (selo/DICA): a caixa vai junto
        self.play(FadeIn(bx6), FadeIn(ult), Create(mk), FadeIn(l29), run_time=0.9)
        self.gat("só no último segundo")
        self.play(ult.animate.set_fill(ACC, 0.55), run_time=0.6)
        self.play(ult.animate.set_fill(ACC, 0.3), run_time=0.6)
        self.gat("para conferir as voltas")
        self.confere([[lbl(r"\tfrac12\cdot 5", VEL, 36), "VOLTAS/S ·", lbl(r"30\ \mathrm{s}", WHITE_, 36)], ["= 75 VOLTAS", lbl(r"\checkmark", WHITE_, 36)]], x0=X_CONTA + 0.12, wmax=LARG_CONTA - 0.12)
        self.wait(1.2)
        self.sem_selo()                                  # G7: um selo por vez (o CONFERE sai antes da DICA)
        self.dica18([[lbl(r"\mathrm{rpm}\rightarrow\mathrm{rad/s}", VEL, 36), "ANTES DE TUDO"]])
        self.ate(0.99)
        mot.clear_updaters()

"""Camadas Manim (fundo transparente, -t) dos trechos Three.js do v2: hook (H1–H3, manequim), T2 (trilho de ar, T2-1..T2-4)
e E4-1 (muro recuado). O compor.py põe cada camada sobre os PNGs do 3D. Tempos: threejs/timeline_*.json; rótulos presos ao 3D
(cota do muro, pouso) usam as projeções de threejs/proj_*.json (câmera parada em cada janela; QA em qa/muro_proj.js)."""
from kit import *  # noqa: F401,F403


def clampf(x, a, b):
    return min(b, max(a, x))


def rampa(t, t0, d):
    return suave(clampf((t - t0) / d, 0, 1))


def cota(base, topo, rot, lado=LEFT, dx=0.32, tam=34):
    """Cota vertical GEO ao lado de uma aresta projetada do 3D."""
    a, b = P3(*base) + dx * lado, P3(*topo) + dx * lado
    seta = DoubleArrow(a, b, buff=0, color=GEO, stroke_width=3, tip_length=0.15)
    lab = MathTex(rot, font_size=tam, color=GEO).next_to(seta, lado, buff=0.15)
    return VGroup(seta, lab)


# ══════════════════════════════════════════════════════════════════════════════════════════════════════════
# HOOK — H1–H3
# ══════════════════════════════════════════════════════════════════════════════════════════════════════════
class CamadaHook(Camada):
    def construct(self):
        TL = timeline("hook")
        PR = projecoes("hook")
        S, E = TL["ancoras"], TL["eventos"]
        self.setup_base()
        c1, c2 = PR["c1"]["pontos"], PR["c2"]["pontos"]
        ct = cota(c1["A_base"], c1["A_topo"], r"2{,}5\ \mathrm{m}", tam=40)
        ct[1].become(screen_text("2,5 m", 40, color=GEO).next_to(ct[0], LEFT, buff=0.15))       # vírgula visível (v4)
        lento = txt("CÂMERA LENTA", 20, color=DIM, op=0.8).move_to(P3(6.45, 3.45))
        janelas = E["camera_lenta"]

        def lent():
            t = self.clk.get_value()
            a = max([rampa(t, t0, 0.3) * (1 - rampa(t, t1 - 0.3, 0.3)) for t0, t1 in janelas] + [0])
            return lento.copy().set_opacity(0.8 * a)
        self.add(always_redraw(lent))
        # H1 — cota do muro (câmera parada)
        self.ate_t(0.9)
        self.play(FadeIn(ct), run_time=0.7)
        clk = self.clk
        ct.add_updater(lambda m: m.set_opacity(0.72 + 0.28 * math.cos(2 * PI * (clk.get_value() - 1.6) / 1.8)))   # v4: nada parado
        self.ate_t(S["H2"] - 0.6)
        ct.clear_updaters()
        self.play(FadeOut(ct), run_time=0.4)
        # H3 — rótulos sob os pousos e a pergunta
        base = min(c2["A_base"][1], c2["B_base"][1], c2["A_pouso"][1], c2["B_pouso"][1]) - 0.45     # mesma linha de base
        xa = (c2["A_meio"][0] + c2["A_pouso"][0]) / 2
        xb = (c2["B_meio"][0] + c2["B_pouso"][0]) / 2
        la = txt("PERNAS DURAS", T_LAB, color=GEO).move_to(P3(xa, base))
        lb = txt("JOELHOS DOBRADOS", T_LAB, color=GEO).move_to(P3(xb, base))
        self.ate_t(S["H3"] + 3.4)
        self.play(FadeIn(la), FadeIn(lb), run_time=0.6)
        t2 = txt("POR QUE DOBRAR OS JOELHOS", 40, bold=True).move_to(P3(0, 2.55))
        t3 = txt("SALVA SUAS PERNAS?", 40, color=CYAN, bold=True).move_to(P3(0, 1.75))
        self.ate_t(S["H3"] + 0.42 * ANC["H3"]["dur"])
        self.play(FadeIn(t2, shift=0.1 * UP), run_time=0.7)
        self.play(FadeIn(t3, shift=0.1 * UP), run_time=0.7)
        t_q = self.clk.get_value()
        t3.add_updater(lambda m: m.set_opacity(0.7 + 0.3 * math.cos(2 * PI * (self.clk.get_value() - t_q) / 1.6)))
        la.add_updater(lambda m: m.set_opacity(0.75 + 0.25 * math.cos(2 * PI * (self.clk.get_value() - t_q) / 2.0)))
        lb.add_updater(lambda m: m.set_opacity(0.75 + 0.25 * math.cos(2 * PI * (self.clk.get_value() - t_q - 1.0) / 2.0)))
        self.ate_t(TL["duracao_s"] - 0.9)
        for m in (t3, la, lb):
            m.clear_updaters()
        self.play(*[FadeOut(m) for m in (la, lb, t2, t3)], run_time=0.6)
        self.fim_camada(TL["duracao_s"])


# ══════════════════════════════════════════════════════════════════════════════════════════════════════════
# E4-1 — muro recuado
# ══════════════════════════════════════════════════════════════════════════════════════════════════════════
class CamadaE4(Camada):
    def construct(self):
        TL = timeline("e4")
        c3 = projecoes("e4")["c3"]["pontos"]
        self.setup_base(cap="EXERCÍCIO 4 · DE VOLTA AO MURO", selo="DOIS CAMINHOS: TEMPO E DISTÂNCIA")
        T = TL["duracao_s"]
        ct = cota(c3["A_base_d"], c3["A_topo_d"], r"h=2{,}5\ \mathrm{m}", lado=RIGHT, dx=0.3)
        m_ = MathTex(r"m=80\ \mathrm{kg}", font_size=46)
        v_ = Mc((r"v=\sqrt{2\cdot 9{,}8\cdot 2{,}5}=7{,}0\ \mathrm{m/s}", VEL), size=46)
        dp = Mc((r"\Delta p=80\cdot 7{,}0=560\ \mathrm{kg\cdot m/s}", MAG), size=46)
        ig = txt("NOS DOIS CASOS", T_LAB, color=MAG)
        conta(m_, v_, dp, ig, topo=1.9, buff=0.55)
        self.ate_t(0.5)
        self.play(FadeIn(ct), FadeIn(m_), run_time=0.8)
        self.ate_t(0.32 * T)
        self.play(FadeIn(v_, shift=0.1 * UP), run_time=0.8)
        self.ate_t(0.6 * T)
        self.play(FadeIn(dp, shift=0.1 * UP), run_time=0.8)
        self.ate_t(0.8 * T)
        self.play(FadeIn(ig), run_time=0.5)
        self.ate_t(T - 0.8)
        self.play(*[FadeOut(m) for m in (ct, m_, v_, dp, ig)], run_time=0.6)
        print(f"[QA] E4-1 v = {math.sqrt(2 * 9.8 * 2.5):.3f} m/s; Δp = {80 * math.sqrt(2 * 9.8 * 2.5):.1f} kg·m/s")
        self.fim_camada(T)


# ══════════════════════════════════════════════════════════════════════════════════════════════════════════
# T2 (v3, fora do v4) — trilho de ar em 3D: T2-1..T2-4
# ══════════════════════════════════════════════════════════════════════════════════════════════════════════
class CamadaTrilho(Camada):
    def construct(self):
        self.TL = TL = timeline("trilho")
        G = TL["geometria"]
        self.MEIA = G["carrinho_meia_largura"]
        self.cx, self.cy = G["centro_manim"]
        self.setup_base(cap="POR QUE MASSA VEZES VELOCIDADE?")
        self.V = TL["ensaios"][0]["v"]
        L = 1.6
        E = TL["eventos"]
        T = TL["duracao_s"]
        e3 = TL["ensaios"][2]

        def estado(t):
            r = dict(xa=1e3, xb=1e3, va=0.0, vb=0.0, vis=0.0, juntos=False, car=False)
            for e in TL["ensaios"]:
                vis = rampa(t, e["vis"][0], 0.4) * (1 - rampa(t, e["vis"][1] - 0.4, 0.4))
                if vis <= 0:
                    continue
                r["vis"] = vis
                if e["tipo"] == "explosao":
                    d = e["v"] * (t - e["t_evento"]) if t > e["t_evento"] else 0.0
                    r.update(xa=-e["x0"] - d, xb=e["x0"] + d, va=-e["v"] if t > e["t_evento"] else 0.0)
                    r["vb"] = -r["va"]
                else:
                    tc = e["t_move"] + (2 * e["x0"] - 2 * self.MEIA) / (2 * e["v"])
                    r["car"] = bool(e.get("visao_do_carro"))
                    if t < e["t_move"]:
                        r.update(xa=-e["x0"], xb=e["x0"])
                    elif t < tc:
                        r.update(xa=-e["x0"] + e["v"] * (t - e["t_move"]), xb=e["x0"] - e["v"] * (t - e["t_move"]), va=e["v"], vb=-e["v"])
                    else:
                        r.update(xa=-self.MEIA, xb=self.MEIA, juntos=True)
                    r["janela"] = (e["t_move"], e["vis"][1])
            return r

        def chaves(lista, t, campo):
            if t <= lista[0]["t"]:
                return lista[0][campo]
            for a, b in zip(lista, lista[1:]):
                if t <= b["t"]:
                    u = (t - a["t"]) / max(b["t"] - a["t"], 1e-9)
                    if b.get("ease") != "linear":
                        u = suave(u)
                    return a[campo] + (b[campo] - a[campo]) * u
            return lista[-1][campo]

        t_frente = TL["camera"][2]["t"]

        def quadro():
            t = self.clk.get_value()
            s = estado(t)
            g = VGroup()
            if s["vis"] <= 0.02 or t < t_frente + 0.2:               # antes da vista de frente o 3D é só cênico
                return g
            camx = chaves(TL["cam_x"], t, "x")
            vcam = self.V if (s["car"] and s.get("janela") and s["janela"][0] <= t <= s["janela"][1]) else 0.0
            xa, xb = self.cx + s["xa"] - camx, self.cx + s["xb"] - camx
            alfa = s["vis"]
            for x in (xa, xb):
                g.add(MathTex("m", font_size=44, color=WHITE_).move_to(P3(x, self.cy + 0.45)).set_z_index(12).set_opacity(alfa))
            ya = self.cy + 1.55
            if s["juntos"]:
                xm = (xa + xb) / 2
                g.add(MathTex("2m", font_size=40, color=WHITE_).move_to(P3(xm, self.cy + 1.1)).set_z_index(12).set_opacity(alfa))
                rel = -vcam
                if abs(rel) > 1e-6:
                    g.add(arrow(P3(xm, ya + 0.35), P3(xm + L * rel / self.V, ya + 0.35), color=VEL, width=7).set_opacity(alfa))
                    g.add(MathTex("v", font_size=44, color=VEL).move_to(P3(xm + L * rel / self.V / 2, ya + 0.85)).set_opacity(alfa))
            else:
                for x, v in ((xa, s["va"] - vcam), (xb, s["vb"] - vcam)):
                    if abs(v) > 1e-6:
                        g.add(arrow(P3(x, ya), P3(x + L * v / self.V, ya), color=VEL, width=7).set_opacity(alfa))
                        g.add(MathTex("2v" if abs(v) > 1.5 * self.V else "v", font_size=44, color=VEL)
                              .move_to(P3(x + L * v / self.V / 2, ya + 0.5)).set_opacity(alfa))
                if s["car"]:
                    g.add(MathTex("0", font_size=40, color=DIM).move_to(P3(xa, ya)).set_opacity(alfa * 0.8))
            return g
        self.add(always_redraw(quadro))

        def observador():                                         # carro estilizado + VISÃO DO CARRO (só no T2-3)
            t = self.clk.get_value()
            f = rampa(t, e3["vis"][0], 0.5) * (1 - rampa(t, e3["vis"][1] - 0.5, 0.5))
            if f <= 0.02:
                return VGroup()
            corpo = RoundedRectangle(corner_radius=0.12, width=1.4, height=0.42).set_stroke(mix(STEEL, 0.5), 2).set_fill(STEEL, 1.0)
            cab = RoundedRectangle(corner_radius=0.1, width=0.7, height=0.3).set_stroke(mix(STEEL, 0.5), 2).set_fill(GEO, 1.0)
            cab.next_to(corpo, UP, buff=-0.02)
            rodas = VGroup(*[Circle(radius=0.14).set_stroke(mix(STEEL, 0.5), 2).set_fill(BACKGROUND_COLOR, 1.0) for _ in range(2)])
            rodas[0].move_to(corpo.get_center() + P3(-0.4, -0.22))
            rodas[1].move_to(corpo.get_center() + P3(0.4, -0.22))
            carro = VGroup(corpo, cab, rodas).move_to(P3(-4.6, -2.35)).set_opacity(f)
            lab = txt("VISÃO DO CARRO", T_LAB, color=WHITE_, op=f).next_to(carro, RIGHT, buff=0.3)
            return VGroup(carro, lab)
        self.add(always_redraw(observador))

        # T2-4: a equação do carro; depois o trilho some e os três casos ficam em coluna no CENTRO, alinhados pelo "="
        def linha_eq(esq, dir_, tam=52):
            m = MathTex(esq, "=", dir_, font_size=tam, color=MAG)
            m.shift(RIGHT * (-m[1].get_center()[0]))
            return m
        eq = linha_eq(r"m\cdot 2v+m\cdot 0", r"2m\cdot v").set_y(-2.35)
        k1 = linha_eq(r"m\cdot 2v+2m\cdot(-v)", r"3m\cdot 0")
        k2 = linha_eq(r"2m\cdot 3v+3m\cdot(-2v)", r"5m\cdot 0")
        cap = legenda("ANTES = DEPOIS")
        self.ate_t(E["equacao_entra"])
        self.play(Write(eq), run_time=1.2)
        self.ate_t(E["casos"] - 0.9)
        self.play(eq.animate.set_y(1.35), run_time=0.9)
        k1.set_y(0.0)
        k2.set_y(-1.35)
        for m in (eq, k1, k2):
            m.modo_centro = False
        self.play(Write(k1), run_time=1.0)
        self.play(Write(k2), run_time=1.0)
        self.play(FadeIn(cap), *[Indicate(m[1], color=WHITE_, scale_factor=1.3) for m in (eq, k1, k2)], run_time=1.0)
        self.ate_t(T - 1.1)
        self.play(*[FadeOut(m) for m in (eq, k1, k2, cap)], run_time=0.6)
        self.fim_camada(T)


# ══════════════════════════════════════════════════════════════════════════════════════════════════════════
# F2 — o cavalo e a corda (asset CC0 da Quaternius, assets_unidade/cavalo)
# ══════════════════════════════════════════════════════════════════════════════════════════════════════════
class CamadaCavalo(Camada):
    def construct(self):
        TL = timeline("cavalo")
        Q = json.loads((AQUI / "threejs" / "proj_cavalo_quadros.json").read_text(encoding="utf-8"))["quadros"]
        self.setup_base()
        self.remove(self.h1, self.wm, self.faixa)                          # sem header nesta cena (como no v2)
        T = TL["duracao_s"]
        nq = len(Q)
        Lf = 1.5

        def pts():
            f = min(int(round(self.clk.get_value() * FPS)), nq - 1)
            q = Q[f]
            a, b = np.array(q["corda_pedra"] + [0.0]), np.array(q["corda_peito"] + [0.0])
            d = (b - a) / np.linalg.norm(b - a)
            n = np.array([-d[1], d[0], 0.0]) * 0.3
            return a, b, d, n, q

        vis = ValueTracker(0.0)

        def setas():
            a, b, d, n, q = pts()
            t = self.clk.get_value()
            pulso = 1.0 + 0.12 * math.sin(2 * PI * t / 1.4)
            op = vis.get_value()
            if op < 0.02:
                return VGroup()
            s1 = arrow(a + n, a + n + d * Lf * pulso, color=FC, width=8, tip=0.24).set_opacity(op)
            # −F⃗ fora do corpo: à frente do peitoral, na altura da corda, mesmo comprimento da F⃗ (ponta no peitoral)
            ponta = b + d * 0.15 - 1.3 * n
            s2 = arrow(ponta + d * Lf * pulso, ponta, color=FC, width=8, tip=0.24).set_opacity(op)
            l1 = MathTex(r"\vec F", font_size=40, color=FC).move_to(a + 2.2 * n + d * Lf * 0.5).set_opacity(op)
            l2 = MathTex(r"-\vec F", font_size=40, color=FC).move_to(ponta - 1.5 * n + d * Lf * 0.55).set_opacity(op)
            return VGroup(s1, s2, l1, l2)
        self.add(always_redraw(setas))
        qv = ValueTracker(0.0)

        def interrog():
            a, b, d, n, q = pts()
            t = self.clk.get_value()
            return MathTex("?", font_size=64, color=GEO).move_to(P3(q["topo"][0] + 0.3, 1.75 + 0.06 * math.sin(2 * PI * t / 2.0))) \
                .set_opacity(qv.get_value() * (0.7 + 0.08 * math.sin(2 * PI * t / 2.0)))
        self.add(always_redraw(interrog))
        p1 = centro(txt("SE A CORDA PUXA O CAVALO PARA TRÁS COM A MESMA FORÇA,", 28, bold=True), 3.65)
        p2 = centro(txt("COMO ELE ANDA?", 32, bold=True), 3.05)
        prox = centro(linha(txt("PRÓXIMO VÍDEO:", 26, op=0.9), txt("CONSERVAÇÃO DO MOMENTO EM SISTEMAS", 30, color=CYAN, bold=True), buff=0.3),
                      LEGENDA_Y - 0.25)
        self.ate_t(0.8)
        self.play(vis.animate.set_value(1.0), run_time=0.8)
        self.ate_t(0.2 * T)
        self.play(FadeIn(p1, shift=0.1 * UP), run_time=0.8)
        self.play(FadeIn(p2, shift=0.1 * UP), qv.animate.set_value(1.0), run_time=0.7)
        self.ate_t(0.62 * T)
        self.play(FadeIn(prox, shift=0.1 * UP), run_time=0.8)
        self.ate_t(T - 0.7)
        self.play(FadeOut(p1), FadeOut(p2), FadeOut(prox), vis.animate.set_value(0.0), qv.animate.set_value(0.0), run_time=0.6)
        self.fim_camada(T)

"""Camadas Manim (fundo transparente, -t) dos trechos Three.js: T1 (C01-1..5) e T2 (C13-2..5).

O compor.py põe esta camada por cima dos PNGs do Three.js. Todos os tempos vêm de threejs/timeline_*.json; a lógica de
movimento (carrinhos, corpúsculos) espelha cena3d/c01.js e cena3d/c13.js. Mapeamento na vista 'frente':
Manim = (cx + K·(x − x_cam), cy + K·z).
"""
from kit import *  # noqa: F401,F403


def tex(s, cor=WHITE_, size=M_MID):
    return MathTex(s, font_size=size, color=cor)


def _tl(nome):
    return json.loads((AQUI / "threejs" / f"timeline_{nome}.json").read_text(encoding="utf-8"))


def clampf(x, a, b):
    return min(b, max(a, x))


def rampa(t, t0, d):
    return suave(clampf((t - t0) / d, 0, 1))


class Camada(Base):
    """Base das camadas: tempo absoluto do trecho (self.t) e espera até um instante."""

    def ate_t(self, alvo):
        n = round((alvo - self.nq / FPS) * FPS)
        if n >= 1:
            self.wait(n / FPS)

    def fim_camada(self, T):
        self.ate_t(T)
        total = round(T * FPS)
        print(f"[camada] {self.nq} quadros (3D: {total})" + ("" if self.nq == total else "  <-- DIFERENTE"))


# ══════════════════════════════════════════════════════════════════════════════════════════════════════════
# T1 — C01
# ══════════════════════════════════════════════════════════════════════════════════════════════════════════
class Camada01(Camada):
    def construct(self):
        self.TL = TL = _tl("c01")
        self.G = TL["geometria"]
        self.MEIA = self.G["carrinho_meia_largura"]
        self.cx, self.cy = self.G["centro_manim"]
        self.setup_base(cap="POR QUE MASSA VEZES VELOCIDADE?")
        self.V = TL["ensaios"][0]["v"]
        L = 1.6                                         # u de tela por v (2v = 3,2)
        E = TL["eventos"]

        # estado dos carrinhos (espelho de c01.js)
        def estado(t):
            r = dict(xa=1e3, xb=1e3, va=0.0, vb=0.0, vis=0.0, juntos=False, car=False, ens=-1)
            for k, e in enumerate(TL["ensaios"]):
                vis = rampa(t, e["vis"][0], 0.4) * (1 - rampa(t, e["vis"][1] - 0.4, 0.4))
                if vis <= 0:
                    continue
                r["vis"], r["ens"] = vis, k
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
        self.estado = estado

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

        def sx(x, camx):
            return self.cx + (x - camx)

        def quadro():
            t = self.clk.get_value()
            s = estado(t)
            g = VGroup()
            if s["vis"] <= 0.02 or t < 12.2:                  # antes da vista de frente o 3D é só cênico
                return g
            camx = chaves(TL["cam_x"], t, "x")
            vcam = self.V if (s["car"] and s.get("janela") and s["janela"][0] <= t <= s["janela"][1]) else 0.0
            xa, xb = sx(s["xa"], camx), sx(s["xb"], camx)
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
                for x, v, nome in ((xa, s["va"] - vcam, "A"), (xb, s["vb"] - vcam, "B")):
                    if abs(v) > 1e-6:
                        a = arrow(P3(x, ya), P3(x + L * v / self.V, ya), color=VEL, width=7).set_opacity(alfa)
                        g.add(a)
                        g.add(MathTex("2v" if abs(v) > 1.5 * self.V else "v", font_size=44, color=VEL)
                              .move_to(P3(x + L * v / self.V / 2, ya + 0.5)).set_opacity(alfa))
                if s["car"]:
                    g.add(MathTex("0", font_size=40, color=DIM).move_to(P3(xa, ya)).set_opacity(alfa * 0.8))
            return g

        self.add(always_redraw(quadro))
        self.t0_car = TL["eventos"]["visao_do_carro_1"]

        # observador (carrinho estilizado) e rótulo da visão do carro
        def observador():
            t = self.clk.get_value()
            s = estado(t)
            if not (s["car"] and s["vis"] > 0.02):
                return VGroup()
            f = s["vis"]
            corpo = RoundedRectangle(corner_radius=0.12, width=1.4, height=0.42).set_stroke(mix(STEEL, 0.5), 2).set_fill(STEEL, 1.0)
            cab = RoundedRectangle(corner_radius=0.1, width=0.7, height=0.3).set_stroke(mix(STEEL, 0.5), 2).set_fill(GEO, 1.0)
            cab.next_to(corpo, UP, buff=-0.02)
            rodas = VGroup(*[Circle(radius=0.14).set_stroke(mix(STEEL, 0.5), 2).set_fill(BACKGROUND_COLOR, 1.0) for _ in range(2)])
            rodas[0].move_to(corpo.get_center() + P3(-0.4, -0.22))
            rodas[1].move_to(corpo.get_center() + P3(0.4, -0.22))
            carro = VGroup(corpo, cab, rodas).move_to(P3(self.cx, 2.55)).set_opacity(f)
            lab = txt("VISÃO DO CARRO", T_LAB, color=WHITE_, op=f).next_to(carro, DOWN, buff=0.18)
            return VGroup(carro, lab)
        self.add(always_redraw(observador))

        # equação (C01-5): m·2v + m·0 = 2m·v em magenta
        eq = MathTex(r"m\cdot 2v", "+", r"m\cdot 0", "=", r"2m\cdot v", font_size=58, color=MAG).move_to(P3(0, -2.9))
        self.ate_t(E["equacao_entra"])
        self.play(FadeIn(eq, shift=0.1 * UP), run_time=1.0)
        self.fim_camada(TL["duracao_s"])


# ══════════════════════════════════════════════════════════════════════════════════════════════════════════
# T2 — C13
# ══════════════════════════════════════════════════════════════════════════════════════════════════════════
class Camada13(Camada):
    def construct(self):
        TL = self.TL = _tl("c13")
        R, ST, E = TL["raio"], TL["ancoras"], TL["eventos"]
        self.setup_base(cap="EXERCÍCIO 9 · NEWTON E A LUZ", selo="MOYSÉS · PROB. 9.2")
        cx, cy = TL["geometria"]["centro_manim"]
        th1 = math.radians(R["theta1"])
        th2 = math.asin(math.sin(th1) / R["n"])
        Lr = R["L"]
        M = lambda x, z: P3(cx + x, cy + z)
        P = M(0, 0)
        S = M(-Lr * math.sin(th1), Lr * math.cos(th1))
        Rf = M(Lr * math.sin(th1), Lr * math.cos(th1))
        W_ = M(-R["z_fundo"] / math.cos(th2) * math.sin(th2), R["z_fundo"])
        d1 = np.array([math.sin(th1), -math.cos(th1), 0])
        d2 = np.array([math.sin(th2), -math.cos(th2), 0])
        print(f"[QA] θ1 = {R['theta1']}°, θ2 = {math.degrees(th2):.2f}° (sen θ1/sen θ2 = {math.sin(th1) / math.sin(th2):.3f} = n)")

        def traco(a, b, op=0.6, w=2.2):
            return Line(a, b).set_stroke(WHITE_, w, opacity=op).set_z_index(4)

        normal = DashedLine(M(0, -3.5), M(0, 2.75), color=DIM, stroke_width=2.5, dash_length=0.15).set_z_index(3)
        n_lab = txt("NORMAL", 18, color=DIM).move_to(M(0.6, -3.3))
        inc = traco(S, P)
        ref = traco(P, Rf)
        refr = traco(P, W_)

        def arco(raio, a0, ang, c=P):
            return Arc(radius=raio, start_angle=a0, angle=ang, arc_center=c, color=WHITE_, stroke_width=2).set_z_index(6)
        # ângulos medidos a partir da normal (eixo vertical)
        arc_i = arco(1.0, PI / 2 + th1, -th1)               # entre a normal (cima) e o raio incidente (à esquerda)
        arc_r = arco(1.0, PI / 2 - th1, th1)                        # normal (cima) → raio refletido (à direita)
        arc_t = arco(1.0, -PI / 2, th2 * -1 if False else th2 * -1)  # normal (baixo) → raio refratado
        arc_t = Arc(radius=1.0, start_angle=-PI / 2, angle=th2, arc_center=P, color=WHITE_, stroke_width=2).set_z_index(6)
        l_i = MathTex(r"\theta_1", font_size=34, color=WHITE_).move_to(P + P3(-0.42, 1.28))
        l_r = MathTex(r"\theta_1'", font_size=34, color=WHITE_).move_to(P + P3(0.55, 1.28))
        l_t = MathTex(r"\theta_2", font_size=34, color=WHITE_).move_to(P + P3(0.42, -1.3))

        J_up = arrow(P + P3(-0.0, 0.1), P + P3(0, 1.5), color=JC, width=7, tip=0.2) if False else arrow(P3(P[0] + 0.35, P[1] - 0.05), P3(P[0] + 0.35, P[1] + 1.35), color=JC, width=7)
        J_dn = arrow(P3(P[0] - 0.35, P[1] + 0.05), P3(P[0] - 0.35, P[1] - 1.35), color=JC, width=7)
        j_lab = MathTex(r"\vec J", font_size=42, color=JC).move_to(P3(P[0] + 0.75, P[1] + 0.75))
        j_lab2 = MathTex(r"\vec J", font_size=42, color=JC).move_to(P3(P[0] - 0.75, P[1] - 0.75))

        # velocidades em escala: |v1| = 1,8 u ; |v2| = n·1,8 (os dois com a mesma projeção horizontal)
        u1 = 1.8 * d1
        u2 = 1.8 * R["n"] * d2
        v1a = arrow(P - u1, P, color=VEL, width=6)
        v2a = arrow(P, P + u2, color=VEL, width=6)
        v1l = MathTex(r"\vec v_1", font_size=38, color=VEL).move_to(P - u1 + P3(-0.45, 0.2))
        v2l = MathTex(r"\vec v_2", font_size=38, color=VEL).move_to(P + u2 + P3(0.45, -0.1))
        q1 = P - u1
        tan1 = DashedLine(q1, q1 + P3(u1[0], 0), color=VEL, stroke_width=3).set_stroke(opacity=0.8)
        nor1 = DashedLine(q1 + P3(u1[0], 0), P, color=VEL, stroke_width=3).set_stroke(opacity=0.8)
        tan2 = DashedLine(P, P + P3(u2[0], 0), color=VEL, stroke_width=3).set_stroke(opacity=0.8)
        nor2 = DashedLine(P + P3(u2[0], 0), P + u2, color=VEL, stroke_width=3).set_stroke(opacity=0.8)
        vt1 = MathTex(r"v_t", font_size=32, color=VEL).next_to(tan1, UP, buff=0.08).shift(LEFT * 0.55)
        vt2 = MathTex(r"v_t", font_size=32, color=VEL).next_to(tan2, UP, buff=0.08)
        vn1 = MathTex(r"v_n", font_size=32, color=VEL).next_to(nor1, RIGHT, buff=0.06)
        vn2 = MathTex(r"v_n", font_size=32, color=VEL).next_to(nor2, RIGHT, buff=0.06)

        X = 4.9                                               # coluna direita
        # ── C13-2 · espelho ─────────────────────────────────────────────────────────────────────────────
        self.ate_t(E["espelho"] + 7.6)                         # a câmera já está de frente
        self.play(Create(normal), FadeIn(n_lab), Create(inc), run_time=1.0)
        self.play(Create(ref), run_time=0.8)
        self.play(Create(arc_i), FadeIn(l_i), run_time=0.7)
        self.ate_t(ST["C13-2"] + 10.0)
        self.play(GrowArrow(J_up), FadeIn(j_lab), run_time=0.8)
        a1 = Mc((r"\vec J\ \perp\ \text{espelho}", JC), size=36).move_to(P3(X, 2.4))
        a2 = Mc((r"v_t\ \text{igual},\ \ v_n\to -v_n", VEL), size=36).move_to(P3(X, 1.2))
        a3 = Mc((r"\theta_1'=\theta_1", WHITE_), size=M_MID).move_to(P3(X, -0.1))
        self.play(FadeIn(a1, shift=0.1 * UP), run_time=0.7)
        self.play(Create(arc_r), FadeIn(l_r), FadeIn(a2), run_time=0.9)
        self.ate_t(ST["C13-2"] + 14.2)
        self.play(FadeIn(a3, shift=0.1 * UP), run_time=0.8)
        # ── C13-3 · ar → água ───────────────────────────────────────────────────────────────────────────
        self.ate_t(E["troca_espelho_agua"] - 0.3)
        self.play(*[FadeOut(m) for m in (ref, arc_r, l_r, J_up, j_lab, a1, a2, a3)], run_time=0.6)
        self.play(Create(refr), Create(arc_t), FadeIn(l_t), run_time=1.2)
        self.play(GrowArrow(J_dn), FadeIn(j_lab2), run_time=0.8)
        self.ate_t(ST["C13-3"] + 6.0)
        self.play(GrowArrow(v1a), FadeIn(v1l), Create(tan1), Create(nor1), FadeIn(vt1), FadeIn(vn1), run_time=1.0)
        self.play(GrowArrow(v2a), FadeIn(v2l), Create(tan2), Create(nor2), FadeIn(vt2), FadeIn(vn2), run_time=1.0)
        snell = Mc((r"v_1", VEL), (r"\sin\theta_1", WHITE_), "=", (r"v_2", VEL), (r"\sin\theta_2", WHITE_), size=M_MID).move_to(P3(X, 1.6))
        iguais = txt("PARTE PARALELA SE CONSERVA", T_SMALL, color=DIM).move_to(P3(X, 0.3))
        self.ate_t(E["equacao_snell"])
        self.play(FadeIn(snell, shift=0.1 * UP), FadeIn(iguais), run_time=0.9)
        # ── C13-4 · a forma de Snell ────────────────────────────────────────────────────────────────────
        self.ate_t(ST["C13-4"] + 0.2)
        self.play(*[FadeOut(m) for m in (v1a, v2a, v1l, v2l, tan1, tan2, nor1, nor2, vt1, vt2, vn1, vn2, iguais)], run_time=0.6)
        self.play(snell.animate.move_to(P3(X, 2.6)).scale(0.8), run_time=0.7)
        c1 = Mc((r"\frac{\sin\theta_1}{\sin\theta_2}", WHITE_), "=", (r"\text{constante}", WHITE_), size=M_MID).move_to(P3(X, 0.9))
        c2 = txt("MODELO DE NEWTON:", T_SMALL, color=DIM).move_to(P3(X, -0.35))
        c3 = Mc("=", (r"\frac{v_2}{v_1}", VEL), size=M_MID).move_to(P3(X, -1.2))
        self.play(FadeIn(c1, shift=0.1 * UP), run_time=0.9)
        self.ate_t(ST["C13-4"] + 7.0)
        self.play(FadeIn(c2), FadeIn(c3, shift=0.1 * UP), run_time=0.9)
        # ── C13-5 · aproxima-se da normal ───────────────────────────────────────────────────────────────
        self.ate_t(ST["C13-5"] + 0.3)
        self.play(Indicate(arc_t, color=WHITE_), Indicate(l_t), run_time=1.0)
        self.play(*[FadeOut(m) for m in (snell, c1, c2, c3)], run_time=0.5)
        k1 = Mc((r"\theta_2<\theta_1", WHITE_), size=M_MID).move_to(P3(X, 2.2))
        k2 = Mc((r"\frac{v_2}{v_1}>1", VEL), size=M_MID).move_to(P3(X, 0.8))
        k3 = txt("NEWTON: LUZ MAIS RÁPIDA NA ÁGUA", T_SMALL, color=WHITE_).move_to(P3(X, -0.5))
        self.play(FadeIn(k1, shift=0.1 * UP), run_time=0.8)
        self.ate_t(ST["C13-5"] + 7.0)
        self.play(FadeIn(k2, shift=0.1 * UP), run_time=0.8)
        self.ate_t(ST["C13-5"] + 11.0)
        self.play(FadeIn(k3), run_time=0.8)
        self.fim_camada(TL["duracao_s"])

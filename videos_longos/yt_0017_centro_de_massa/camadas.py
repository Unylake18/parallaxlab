"""yt_0017 — camadas Manim sobre as peças 3D (pecas3d.py), reutilizadas pelo teste (X1) e pelas seções. Cada método recebe as
durações (as seções passam as das âncoras). Regras da avaliação de 2026-10-28: um referencial por imagem; setas saindo da borda das
esferas; ⊕ calculado dos pedaços; camadas sempre do estado do próprio quadro (f3d.e); registro por quadro para o QA (qa_overlay_<lote>.json)."""
from pecas3d import *  # noqa: F401,F403
from pecas3d import _hermite

SP = 0.75          # Manim por (u·m/s): momentos do chão na explosão (a P inteira = 3,4)
SR = 1.5           # Manim por (u·m/s): momentos relativos (outra imagem, outra escala)
SV = 1.1           # Manim por (u/s): velocidades da explosão
SVG = 0.03         # Manim por (m/s): V_cm da granada


def cota(xa, xb, y, rotulo, cor=GEO, size=34, lado=DOWN):
    """Cota horizontal entre xa e xb na altura y, com marcas nas pontas e o rótulo (MathTex) abaixo/acima."""
    g = VGroup(Line(P3(xa, y), P3(xb, y)).set_stroke(cor, 2.2),
               Line(P3(xa, y - 0.11), P3(xa, y + 0.11)).set_stroke(cor, 2.2), Line(P3(xb, y - 0.11), P3(xb, y + 0.11)).set_stroke(cor, 2.2))
    lab = (rotulo if isinstance(rotulo, Mobject) else MathTex(rotulo, font_size=size, color=cor)).next_to(P3((xa + xb) / 2, y), lado, buff=0.14)
    return VGroup(g, lab)


def rot_cota(valor, var=None, cor=GEO):
    """G9: rótulo de cota em Space Grotesk (`3 m`, `d₁ = 3 m`: a variável em MathTex, o número e a unidade no texto do canal)."""
    if var is None:
        return rot(valor, 32, cor)
    return VGroup(mtex(var, cor, 38), rot("= " + valor, 32, cor)).arrange(RIGHT, buff=0.1)


def cota_v(x, ya, yb, cor=GEO, w=2.2):
    """Cota vertical (marcas nas pontas)."""
    return VGroup(Line(P3(x, ya), P3(x, yb)).set_stroke(cor, w), Line(P3(x - 0.09, ya), P3(x + 0.09, ya)).set_stroke(cor, w),
                  Line(P3(x - 0.09, yb), P3(x + 0.09, yb)).set_stroke(cor, w))


class Haltere2D:
    """1 kg + 3 kg, separação 4 (a leve a 3 do ⊕, a pesada a 1), bolas de aço 2D com a luz B e haste. Vista de cima: gira no plano da
    tela em torno do ⊕ (ang); para com a haste horizontal (leve à esquerda) e passa ao perfil no mesmo lugar (nada pula); no perfil o
    apoio triangular desliza por baixo e a haste balança (tilt > 0: o lado +x desce) até equilibrar no ⊕."""
    M1, M2, SEP = 1.0, 3.0, 4.0
    X1, X2 = -SEP * M2 / (M1 + M2), SEP * M1 / (M1 + M2)             # −3 e +1
    R1, R2 = 0.8 * (M1 / 3) ** (1 / 3), 0.8 * (M2 / 3) ** (1 / 3)

    def __init__(self, cena, K=0.95, cm=P3(-2.1, 0.0)):
        self.cena, self.K, self.cm = cena, K, cm
        self.ang, self.tilt, self.orb = ValueTracker(0.0), ValueTracker(0.0), ValueTracker(0.0)
        self.ax, self.av, self.ab = ValueTracker(-1.6), ValueTracker(0.0), ValueTracker(0.3)
        self.a_ini = 0.0

    def trackers(self):
        return [self.ang, self.tilt, self.orb, self.ax, self.av, self.ab]

    def p(self, x):
        a = self.ang.get_value() - self.tilt.get_value()
        return self.cm + self.K * x * P3(math.cos(a), math.sin(a))

    def desenho(self):
        b1, b2 = self.p(self.X1), self.p(self.X2)
        g = VGroup(Line(b1, b2).set_stroke(mix(STEEL, 0.3), 10), Line(b1, b2).shift(0.025 * UP).set_stroke(WHITE_, 1.6, opacity=0.35))
        if self.av.get_value() > 0.5:                                       # apoio triangular (aço, com recorte)
            xa, yb = self.cm[0] + self.K * self.ax.get_value(), self.cm[1] - 0.05 - self.ab.get_value()
            tri = Polygon(P3(xa, yb), P3(xa + 0.36, yb - 0.62), P3(xa - 0.36, yb - 0.62))
            tri.set_fill([mix(STEEL, 0.25), escuro(STEEL, 0.3)], 1).set_sheen_direction(UP).set_stroke(BLUE_L, 1.6, opacity=0.55)
            tri._degrade = "aco"
            pe = RoundedRectangle(corner_radius=0.03, width=1.3, height=0.12).move_to(P3(xa, yb - 0.68)).set_fill(escuro(STEEL, 0.4), 1) \
                .set_stroke(mix(STEEL, 0.3), 1.2)
            g.add(pe, tri)
        g.add(esfera2d(self.R1 * self.K).move_to(b1), esfera2d(self.R2 * self.K).move_to(b2))
        return g

    def girar(self, omega=1.6):
        t0, a0 = self.cena.clk.get_value(), self.ang.get_value()
        self.omega, self.a_ini = omega, a0
        self.ang.add_updater(lambda m: m.set_value(a0 + omega * (self.cena.clk.get_value() - t0)))

    def parar(self, dur=2.6):
        """Desacelera até um múltiplo exato de 2π (haste horizontal, leve à esquerda); os rastros apagam: é a vista de perfil."""
        self.ang.clear_updaters()
        a0, w = self.ang.get_value(), self.omega
        h = dur * 0.75
        af = 2 * PI * math.ceil((a0 + 0.5 * w * h) / (2 * PI))
        m0 = w * h / (af - a0)
        self.cena.play(self.ang.animate(rate_func=_hermite(m0)).set_value(af), self.orb.animate(rate_func=linear).set_value(0.0), run_time=h)
        self.ang.set_value(af)
        self.cena.wait(dur * 0.25)

    def apoiar(self, dur=1.6, balanco=2.6):
        """Apoio entra por baixo, sobe até tocar a haste sob o ⊕; a haste balança (amortecido) e se acomoda."""
        self.av.set_value(1.0)
        self.cena.play(self.ax.animate.set_value(0.0), run_time=dur)
        self.cena.play(self.ab.animate.set_value(0.0), run_time=0.5)
        t0 = self.cena.clk.get_value()
        self.tilt.add_updater(lambda m: m.set_value(0.11 * math.exp(-(self.cena.clk.get_value() - t0) / 0.75)
                                                    * math.sin(5.0 * (self.cena.clk.get_value() - t0))))
        self.cena.wait(balanco)
        self.tilt.clear_updaters()
        self.tilt.set_value(0.0)


class Camadas(Base):
    # ── registro para o QA ────────────────────────────────────────────────────────────────────────────────
    def reg(self, cena, **pts):
        if not hasattr(self, "_reg"):
            self._reg = {}
        f = int(round(self.clk.get_value() * FPS))
        conv = lambda v: [np.asarray(x)[:2].tolist() for x in v] if isinstance(v, list) else np.asarray(v)[:2].tolist()
        self._reg.setdefault(cena, {})[f] = {k: conv(v) for k, v in pts.items()}
        return pts

    def ate_mov(self, frac, tracker, alvo):
        """Como ate(frac), mas sem tela parada: leva `tracker` até `alvo` (linear) no tempo que falta até a fração da âncora."""
        falta = (self._q0 + frac * (self.alvo - self._q0) - self.nq) / FPS
        if falta >= 0.2:
            self.play(tracker.animate(rate_func=linear).set_value(alvo), run_time=falta)

    def gravar_reg(self):
        if not PEDIDOS3D and getattr(self, "_reg", None):
            (AQUI / f"qa_overlay_{self.lote}.json").write_text(json.dumps(self._reg), encoding="utf-8")

    # ── granada (hook, A2, A4, T2-7, T2-8) ────────────────────────────────────────────────────────────────
    # v3: campo de provas (Three.js) + gráfico no Manim: eixos em metros (marcas a cada 50 m), parábola tracejada branca a 50%,
    # rastro do ⊕ em degradê com glow, rastros finos aço-azulados dos corpos, fotos fantasma do ⊕ a 25% a cada 0,5 s com a marca de
    # tempo a cada 1 s, vetor de lançamento com as componentes, peso M g⃗ no ⊕. Enquadramentos (K, camx, yc):
    CAM_PARABOLA = (1.0, 6.12, -2.58)               # a parábola inteira centrada (H3, A4)
    CAM_VOO = (0.75, 7.3, -3.05)                     # o voo inteiro até o último pouso (T2-7, T2-8): o 2 kg passa abaixo do painel e os
                                                     # números do eixo x (duas linhas) ficam dentro da margem
    SVL = 0.035                                      # Manim por m/s: vetor de lançamento
    T0_HOOK, T0_VOO = 0.3, 0.3                       # a granada aparece já saindo do marco (s de física)

    def granada_cam(self, g, cam, run_time=None, **kw):
        """Leva a câmera da granada a (K, camx, yc) (solta da granada: seg → 0): na hora ou animando junto com `kw`."""
        K, cx, yc = cam
        if run_time is None:
            g.K.set_value(K); g.camx.set_value(cx); g.yc.set_value(yc); g.seg.set_value(0.0)
            return
        self.play(g.K.animate.set_value(K), g.camx.animate.set_value(cx), g.yc.animate.set_value(yc), g.seg.animate.set_value(0.0), **kw,
                  run_time=run_time)

    def _granada_camadas(self, g):
        T = dict(cm=0.0, pul=0.0, peso=0.0, eix=0.0, ras=0.0, lanc=0.0, cota=0.0, alc=0.0, v0lab=0.0)
        for k, v in T.items():
            setattr(self, "g_" + k, ValueTracker(v))
            self.add(getattr(self, "g_" + k))
        self.g_par = None                        # parábola tracejada (feita com a câmera parada)
        self.g_extra, self.g_evita = [], []
        self.mem_peso, self.mem_t = {}, {}

        def vis_frag(k, tau):
            """Centroide visível do caco k no instante tau (o ponto físico + o encaixe no corpo que some em T_SEP)."""
            fr = g.fis(tau)[1]
            e = g.f3d.e
            esc = e["gr"]["esc"]
            o = CEN[k] * esc * (1 - sep(tau - g.TE))
            return projeta3d(e["cam"], (fr[k][0] / g.S + o[0], o[1], fr[k][1] / g.S + o[2]))

        def corpos():
            if g.f3d.op.get_value() < 0.15 or g.f3d not in self.mobjects:
                return []
            e = g.f3d.e
            tau, cam = e["tau"], e["cam"]
            out = []
            seg = suave(g.seg.get_value()) > 0.5                     # câmera presa à granada: ela não sai do lugar na tela
            for dt in ((0.0,) if seg else (0.0, 0.25, 0.5, 0.75, 1.0)):   # agora e ~2 s de tela à frente
                corpo, fr, _, _, _ = g.fis(tau + dt)
                if corpo is not None:
                    out.append((g.m(corpo, cam), g.r_tela(), dt > 0))
                else:
                    out += [(vis_frag(k, tau + dt), g.r_tela(k), dt > 0) for k in range(3)]
            for q in e["gr"].get("fant", []):                        # fotos fantasma (25%): texto não passa por cima; saem do quadro com a câmera
                out.append((projeta3d(cam, (q[1], 0.0, q[2])), g.r_tela(None if q[0] < 0 else q[0]), True))
            return out
        self._corpos3d = [corpos]

        def eixos(cam, o):
            G_ = VGroup()
            px = lambda x, y: g.m((x, y), cam)
            a, b = px(0, 0), px(300, 0)
            xa, xb = max(-7.45, a[0]), min(7.45, b[0])
            if xb > xa and -3.95 < a[1] < 3.9:
                G_.add(Line(P3(xa, a[1]), P3(xb, b[1])).set_stroke(GEO, 2.4, opacity=0.8 * o))
                ult = None
                for xm in range(50, 301, 50):
                    q = px(xm, 0)
                    if -7.2 < q[0] < 7.2:
                        ocm = self.g_cm.get_value() * min(1.0, max(0.0, (np.linalg.norm(q + 0.45 * DOWN - g.cm()) - 0.55) / 0.3))
                        oalc = 1 - self.g_alc.get_value() if xm == 250 else 1.0
                        ult = mrot(f"{xm}", 30, GEO, op=0.9 * o * oalc * (1 - self.g_cm.get_value() + ocm)).next_to(q, DOWN, buff=0.22)
                        G_.add(Line(q + 0.1 * DOWN, q + 0.1 * UP).set_stroke(GEO, 2.4, opacity=0.8 * o), ult)
                xl = VGroup(mtex("x", GEO, 36), mrot("(m)", 30, GEO)).arrange(RIGHT, buff=0.08).set_opacity(0.9 * o)
                if ult is not None and ult.get_right()[0] + 0.3 + xl.width < 7.45:     # na linha dos números, depois do último
                    G_.add(xl.next_to(ult, RIGHT, buff=0.3))
                else:
                    G_.add(xl.next_to(ult if ult is not None else P3(7.3, b[1]), DOWN, buff=0.1).align_to(P3(7.3, 0), RIGHT))   # sem lugar: embaixo dos números
            c, d = px(0, 0), px(0, 112)
            ya, yb = max(-3.95, c[1]), min(3.3, d[1])
            if yb > ya and -7.4 < c[0] < 7.0:
                G_.add(Line(P3(c[0], ya), P3(d[0], yb)).set_stroke(GEO, 2.4, opacity=0.8 * o))
                for ym in (50, 100):
                    q = px(0, ym)
                    if -3.7 < q[1] < 3.2:
                        G_.add(Line(q + 0.1 * LEFT, q + 0.1 * RIGHT).set_stroke(GEO, 2.4, opacity=0.8 * o),
                               mrot(f"{ym}", 30, GEO, op=0.9 * o).next_to(q, LEFT, buff=0.22))
                if d[1] < 3.2:
                    G_.add(VGroup(mtex("y", GEO, 36), mrot("(m)", 30, GEO)).arrange(RIGHT, buff=0.08)
                           .set_opacity(0.9 * o).next_to(P3(d[0], yb - 0.35) if getattr(self, 'y_lado', False) else P3(d[0], yb),
                                                     RIGHT if getattr(self, 'y_lado', False) else UP, buff=0.12))
            return G_

        def camada():
            e = g.f3d.e
            tau, cam = e["tau"], e["cam"]
            gr = e["gr"]
            out = VGroup()

            def linha(pts, cor, w, op):
                q = projeta3d_n(cam, [(p[0] / g.S, 0.0, p[1] / g.S) for p in pts])
                q = q[(np.abs(q[:, 0]) < 7.5) & (np.abs(q[:, 1]) < 4.0)]
                return VMobject().set_points_as_corners(q).set_stroke(cor, w, opacity=op) if len(q) > 1 else VMobject()
            oe = self.g_eix.get_value()
            if oe > 0.01:
                out.add(eixos(cam, oe))
            orr = self.g_ras.get_value()
            if orr > 0.01:
                ss = np.linspace(0.0, min(tau, g.TE), 40)
                if ss[-1] > 1e-3:
                    out.add(linha([g.ideal(s) for s in ss], RAST, 2, 0.85 * orr))
                if tau > g.TE:
                    for i, tt in enumerate(g.ttoque):
                        s1 = min(tau, tt)
                        if s1 > g.TE + 1e-3:
                            ss_ = np.linspace(0.0, s1 - g.TE, 30)[:, None]
                            out.add(linha(g.pe + ss_ * g.vf[i] + np.c_[0 * ss_, -0.5 * g.G * ss_ ** 2], RAST, 2, 0.85 * orr))
            # topo cotado (linhas-guia tracejadas até os dois eixos, os valores nos eixos) e alcance (T2-7)
            oc = self.g_cota.get_value()
            if oc > 0.01:
                tp = g.m(g.ideal(g.TE), cam)
                xb_, yb_ = g.m((g.pe[0], 0.0), cam), g.m((0.0, g.pe[1]), cam)
                out.add(DashedLine(tp, xb_, dash_length=0.08).set_stroke(GEO, 1.8, opacity=0.7 * oc),
                        DashedLine(tp, yb_, dash_length=0.08).set_stroke(GEO, 1.8, opacity=0.7 * oc),
                        Dot(tp, radius=0.05, color=GEO).set_opacity(oc),
                        mrot("122,4", 30, GEO, op=oc).next_to(xb_, DOWN, buff=0.62),
                        mrot("81,6", 30, GEO, op=oc).next_to(yb_, LEFT, buff=0.22))
            oa = self.g_alc.get_value()
            if oa > 0.01:
                ra = g.m((2 * g.pe[0], 0.0), cam)
                lr = mrot("R = 244,9 m", 30, GEO, op=oa).next_to(ra, DOWN, buff=0.62)
                out.add(Line(ra + 0.16 * UP, lr.get_top() + 0.04 * UP).set_stroke(GEO, 2, opacity=0.8 * oa), lr)
            # marcas de tempo (a cada 1 s) ao lado das fotos fantasma do ⊕ (a granada inteira antes da explosão)
            o = self.g_cm.get_value()
            if gr.get("fant") is not None:
                fant_cm = [(g.m(g.fis(0.5 * j_)[3], cam), 0.2) for j_ in range(1, int(tau / 0.5 + 1e-9) + 1)]
                pts_t = None
                for j in range(1, int(tau / 0.5 + 1e-9) + 1):
                    tg = 0.5 * j
                    pc = g.m(g.fis(tg)[3], cam)
                    if not (-7.3 < pc[0] < 7.3 and -3.9 < pc[1] < 3.6):
                        continue
                    if o > 0.01:
                        out.add(marcador_cm(pc, r=0.15, op=0.25 * o, z=7, leve=True))
                    if j % 2 == 0:
                        v = g.fis(tg)[4]
                        n_ = P3(-v[1], v[0]) / (np.linalg.norm(v) + 1e-9)
                        rt = g.r_tela() if tg < g.TE else 0.2
                        lt = mrot(f"{j // 2} s", 24, GEO, op=0.9)
                        if pts_t is None:                                 # desvia do que já está desenhado e dos textos fixos da cena
                            pts_t = [q for m_ in out.family_members_with_points()
                                     for q in (m_.points[::4] if len(m_.points) > 16 else amostra(m_.points[0], m_.points[-1], 16))]
                            if self.g_peso.get_value() > 0.01:
                                pts_t += amostra(g.cm() + 0.26 * DOWN, g.cm() + 1.35 * DOWN) + amostra(g.cm() + P3(-1.0, -0.85), g.cm() + P3(1.0, -0.85))
                            if self.g_par is not None and self.g_par in self.mobjects:
                                pts_t += list(self.g_par.get_all_points()[::6])
                            for m_ in self.g_extra + self.g_evita:
                                if m_ is not None:
                                    (x0_, y0_, _), (x1_, y1_, _) = m_.get_corner(DL), m_.get_corner(UR)
                                    pts_t += [P3(x_, y_) for x_ in np.linspace(x0_, x1_, 5) for y_ in np.linspace(y0_, y1_, 3)]
                        if np.linalg.norm(pc - g.cm()) < 0.3:             # a foto coincide com o ⊕ já parado no chão: sem marca
                            continue
                        lt.move_to(lugar_livre(lt, [pc + n_ * (rt + d_ + lt.height / 2) for d_ in (0.25, 0.4, 0.55, 0.75, 0.95, 1.2)],   # só fora da curva
                                               [(pc, rt), (g.cm(), 0.75)] + [(c0_, r0_) for c0_, r0_, _ in corpos()] + fant_cm, pts_t, self.mem_t, j, folga=0.08))
                        out.add(lt)
            if o > 0.01:
                ss = np.linspace(0.0, tau, max(2, int(tau * 14)))
                q = projeta3d_n(cam, [(p[0] / g.S, 0.0, p[1] / g.S) for p in (g.fis(s)[3] for s in ss)])
                q = q[(np.abs(q[:, 0]) < 7.5) & (np.abs(q[:, 1]) < 4.0)]
                out.add(rastro_cm(q, w=5, op=0.95 * o))
                out.add(marcador_cm(g.cm(), r=0.215 * (1 + 0.45 * self.g_pul.get_value()), op=o))
            # vetor de lançamento (30; 40) m/s com as componentes, saindo da borda da granada no ponto de lançamento
            ol = self.g_lanc.get_value()
            if ol > 0.01:
                seg_ = suave(g.seg.get_value()) > 0.5
                c0 = g.cm() if seg_ else g.m((0.0, 0.0), cam)            # câmera presa: o vetor sai da granada
                u = P3(0.6, 0.8)
                a0 = da_borda(c0, u, g.r_tela() * 1.05)
                sv = self.SVL * max(1.0, cam["K"] / 1.6)                 # no close a granada é grande: o vetor acompanha o zoom
                v_ = seta(a0, a0 + u * 50 * sv, VEL, 6, tip=0.22, op=ol)
                hx = seta(a0, a0 + RIGHT * 30 * sv, VREL, 4, tip=0.18, op=0.9 * ol)
                vy = seta(a0, a0 + UP * 40 * sv, VREL, 4, tip=0.18, op=0.9 * ol)
                tr_ = VGroup(DashedLine(a0 + RIGHT * 30 * sv, a0 + u * 50 * sv, dash_length=0.07),
                             DashedLine(a0 + UP * 40 * sv, a0 + u * 50 * sv, dash_length=0.07)).set_stroke(VREL, 1.6, opacity=0.6 * ol)
                if seg_:                                                   # close (câmera presa): rótulos nas pontas
                    l30 = mrot("30 m/s", 28, VREL, op=ol).next_to(a0 + RIGHT * 30 * sv, RIGHT, buff=0.16)
                    l40 = mrot("40 m/s", 28, VREL, op=ol).next_to(a0 + UP * 40 * sv, UP, buff=0.14)
                else:                                                      # gráfico: abaixo do eixo x e à esquerda do eixo y
                    l30 = mrot("30 m/s", 28, VREL, op=ol).next_to(a0 + RIGHT * 15 * sv, DOWN, buff=0.42)
                    l40 = mrot("40 m/s", 28, VREL, op=ol).next_to(P3(c0[0], a0[1] + 20 * sv), LEFT, buff=0.18)
                out.add(tr_, v_, hx, vy, l30, l40)
                if self.g_v0lab.get_value() > 0.01:
                    out.add(mtex(r"\vec V_0", VEL, 38).set_opacity(ol * self.g_v0lab.get_value()).move_to(self.pos_v0(a0, sv)))
            c_ = g.cm()
            op_ = self.g_peso.get_value() * min(1.0, max(0.0, (c_[1] + 1.9) / 0.5))
            if op_ > 0.01:
                lg = mtex(r"M\vec g", FC, 40)
                pts_ = [q for m_ in out.family_members_with_points() for q in m_.points[::3]]   # rastros já desenhados
                for m_ in [self.g_par] + self.g_extra:
                    if m_ is not None and m_ in self.mobjects:
                        pts_ += list(m_.get_all_points()[::3])
                pts_ += amostra(c_ + 0.26 * DOWN, c_ + 1.35 * DOWN)
                cands = [c_ + P3(s_ * (0.14 + lg.width / 2 + dx_), -dy_) for dx_ in (0.0, 0.25) for dy_ in (0.85, 1.15, 0.6) for s_ in (1, -1)]
                lg.move_to(lugar_livre(lg, cands, [(c0_, r0_) for c0_, r0_, _ in corpos()], pts_, self.mem_peso, "Mg"))
                out.add(seta(c_ + 0.26 * DOWN, c_ + 1.35 * DOWN, FC, 6, tip=0.22, op=op_), lg.set_opacity(op_))
            if "frags" in gr:
                self.reg("gra", cm=g.cm(), fis=[g.m(np.array(q[:2]) * g.S, cam) for q in gr["frags"]])
            else:
                self.reg("gra", cm=g.cm())
            return out.set_z_index(8)
        return vivo(camada)

    def pos_v0(self, a0, sv):
        """Lugar do rótulo V⃗₀: acima e à esquerda da ponta do vetor de lançamento (fora do triângulo das componentes)."""
        return a0 + P3(0.6, 0.8) * 50 * sv + P3(-0.5, 0.45)

    def parabola(self, g):
        cam = g.f3d.e["cam"]
        curva = VMobject().set_points_smoothly([g.m(g.ideal(s), cam) for s in np.linspace(0.0, 2 * g.TE, 60)])
        return DashedVMobject(curva, num_dashes=70, dashed_ratio=0.55).set_stroke(WHITE_, 3, opacity=0.5).set_z_index(6)

    def pulso_cm(self, rt=0.5, **kw):
        self.play(self.g_pul.animate(rate_func=there_and_back).set_value(1.0), **kw, run_time=rt)

    def nova_granada(self, cam=None, op=1.0, w=1.0, tau=0.0):
        """Granada no campo de provas, já com as camadas (eixos, rastros, ⊕) prontas para acender."""
        K, cx, yc = cam or self.CAM_PARABOLA
        g = self.g = Granada3D(self, K=K, camx=cx, yc=yc, op=op, w=w)
        g.tau.set_value(tau)
        g.f3d._quadro()                                                  # o estado do quadro já com o tau certo (camadas e registro)
        self.add(*g.trackers(), g.f3d)
        self.cam_gra = self._granada_camadas(g)
        self.add(self.cam_gra)
        return g

    def granada_hook(self, ancoras=False):
        """H1 perto, câmera presa à granada que sobe do marco (o vetor de lançamento e as componentes por ~2 s; os eixos acendem; fotos
        fantasma) · H2 as emendas acendem, câmera lenta 0,5× na fratura, os cacos voam · H3 a câmera recua até o gráfico inteiro (troca
        de escala), tracejado, o ⊕ acende com o rastro em degradê, replay com o ⊕, pergunta, congela 2 s antes do primeiro toque."""
        g = self.nova_granada(cam=(3.2, 0.0, -0.35), w=0.0, tau=self.T0_HOOK)   # já no ar, saindo do marco (nunca dentro dele)
        g.seg.set_value(1.0); g.yseg.set_value(-0.35); g.fant.set_value(1.0)
        tauF = g.ttoque[1] - 1.0                   # 2 s de tela (a 0,5×) antes do primeiro toque
        tA = g.TE - 0.25
        self.an("H1")
        T1 = max(3.0, self.resta() - 0.3)
        t0 = self.T0_HOOK
        rho = (tA - t0) / T1
        self.play(g.tau.animate(rate_func=linear).set_value(t0 + 0.45 * rho), self.g_lanc.animate.set_value(1.0), self.g_ras.animate.set_value(1.0),
                  g.K.animate(rate_func=linear).set_value(3.2 - 1.5 * 0.45 / T1), run_time=0.45)
        self.play(g.tau.animate(rate_func=linear).set_value(t0 + 1.6 * rho), self.g_eix.animate.set_value(1.0),
                  g.K.animate(rate_func=linear).set_value(3.2 - 1.5 * 1.6 / T1), run_time=1.15)
        self.play(g.tau.animate(rate_func=linear).set_value(t0 + 2.0 * rho), self.g_lanc.animate.set_value(0.0),
                  g.K.animate(rate_func=linear).set_value(3.2 - 1.5 * 2.0 / T1), run_time=0.4)
        self.play(g.tau.animate(rate_func=linear).set_value(tA), g.K.animate(rate_func=linear).set_value(1.7), run_time=T1 - 2.0)
        self.an("H2")
        self.play(g.tau.animate(rate_func=linear).set_value(g.TE - 0.05), g.onda.animate(rate_func=linear).set_value(1.25),
                  g.brilho.animate.set_value(2.2), run_time=0.6)                                     # as emendas acendem, do centro para fora
        self.play(g.tau.animate(rate_func=linear).set_value(g.TE + 0.2), run_time=1.2)               # câmera lenta 0,5× na fratura
        resto = self.resta() - 0.15
        self.play(g.tau.animate(rate_func=linear).set_value(tauF - 0.35), g.K.animate.set_value(1.45), run_time=max(1.0, resto))
        self.an("H3")
        # a câmera recua até o gráfico inteiro; os cacos passam para o tamanho de tela constante
        self.play(g.tau.animate(rate_func=linear).set_value(tauF - 0.2), g.K.animate.set_value(self.CAM_PARABOLA[0]),
                  g.camx.animate.set_value(self.CAM_PARABOLA[1]), g.yc.animate.set_value(self.CAM_PARABOLA[2]), g.seg.animate.set_value(0.0),
                  g.w.animate.set_value(1.0), run_time=2.2)
        par = self.g_par = self.parabola(g)
        self.play(Create(par), g.tau.animate(rate_func=linear).set_value(tauF - 0.15), run_time=0.7)
        self.play(self.g_cm.animate.set_value(1.0), self.g_pul.animate(rate_func=there_and_back).set_value(1.0), run_time=0.6)   # "esse ponto brilhando"
        self.play(g.tau.animate.set_value(g.TE), run_time=0.8)              # volta à explosão: agora com o ⊕ aceso
        base = 2.2 + 0.7 + 0.6 + 0.8 + 0.8
        rep = max((tauF - g.TE) / 0.5, 0.97 * self.resta() - 0.8 - 2.0) if ancoras else (tauF - g.TE) / 0.5
        self.play(g.tau.animate(rate_func=linear).set_value(tauF), run_time=rep)          # replay com o ⊕ sobre o tracejado
        p1 = txt("SE A GRANADA EXPLODE NO MEIO DO VOO,", 34, bold=True)
        p2 = txt("O QUE CONTINUA NA PARÁBOLA?", 34, bold=True)
        self.pergunta = VGroup(p1, p2).arrange(DOWN, buff=0.2).move_to(P3(0, 3.2)).set_z_index(30)
        self.play(FadeIn(self.pergunta, shift=0.1 * UP), run_time=0.8)
        self.ate(0.97) if ancoras else self.wait(2.0)
        return g

    def granada_toque(self, g, dur=21.0, frac=None, toque_em=0.35):
        """T2-8: o pedaço de 1 kg toca a linha do chão ("bate no chão") e para; flash azul-claro da força do chão e o impulso J (azul-impulso);
        o ⊕ não salta e muda de direção. A CONTA vira um painel PANEL no terço superior direito (a câmera deixa o terço de cima livre):
        J = m (0 − v) = 1 · (−4,02; 42,72) N·s → ΔV_cm = J/M = (−0,89; 9,49) m/s, com o triângulo V_cm antes/depois/ΔV ao lado das equações."""
        t1 = g.ttoque[1]
        if frac:
            self.ate_mov(toque_em - 0.04, g.tau, t1 - 0.06)
        cam = g.cam()
        v1 = g.vf[1] + np.array([0, -g.G * (t1 - g.TE)])                         # velocidade de chegada do pedaço de 1 kg
        pchega = g.m(g.fis(t1)[1][1], cam)
        r1 = g.raio(1.0)
        uv = P3(*(v1 / np.linalg.norm(v1)))
        sv = seta(da_borda(pchega, -uv, r1) - uv * 1.1, da_borda(pchega, -uv, r1) - 0.03 * uv, VEL, 6, tip=0.22)
        vlab = MathTex(r"\vec v=(4{,}02;\ -42{,}72)", font_size=46, color=VEL)
        vlab.next_to(P3(-3.4, 2.85), DOWN, buff=0.45).align_to(P3(-6.2, 0), LEFT)     # céu livre, sob o aviso (perto do chão não cabe)
        self.play(g.tau.animate(rate_func=linear).set_value(t1), FadeIn(sv), FadeIn(vlab), run_time=0.6)
        v_antes, v_dep = g.fis(t1 - 1e-6)[4], g.fis(t1)[4]
        Jv = -v1
        uJ = P3(*(Jv / np.linalg.norm(Jv)))
        a0 = da_borda(pchega, DOWN, r1) + 0.02 * DOWN
        fch = seta(a0, a0 + uJ * 1.2, FC, 7, tip=0.24)
        Jseta = seta(a0 + 0.14 * LEFT, a0 + 0.14 * LEFT + uJ * 1.45, JC, 8, tip=0.28)
        Jlab = mtex(r"\vec J", JC, 44).next_to(a0 + 0.14 * LEFT + uJ * 1.0, LEFT, buff=0.22)
        aviso = txt("O CHÃO ENTROU NA CONTA", 32, bold=True, color=FC).move_to(P3(-3.4, 3.05)).set_z_index(30)
        # painel da CONTA (terço superior direito): triângulo à esquerda, equações à direita
        painel = RoundedRectangle(corner_radius=0.12, width=6.15, height=2.8).move_to(P3(4.375, 2.15)).set_fill(PANEL, 0.88).set_stroke(BLUE_L, 2.2)
        painel._fundo = True
        painel.set_z_index(18)
        SQ = 0.066                                                        # ΔV⃗_cm ≥ 0,6 na tela
        o_ = P3(-4.6, 2.45)                                               # PALCO, céu livre sobre o braço de subida (longe do J⃗, do pico e dos cacos)
        ta, td = o_ + P3(*v_antes) * SQ, o_ + P3(*v_dep) * SQ
        sa = seta(o_, ta, VREL, 7, tip=0.24).set_z_index(22)
        sd = seta(o_, td, VEL, 7, tip=0.24).set_z_index(22)
        cm0 = g.cm()
        fa = seta(da_borda(cm0, UP, 0.3) + 0.2 * UP, da_borda(cm0, UP, 0.3) + 0.2 * UP + P3(*v_antes) * SQ, VREL, 6, tip=0.22).set_z_index(25)
        fd = seta(da_borda(cm0, UP, 0.3) + 0.2 * UP, da_borda(cm0, UP, 0.3) + 0.2 * UP + P3(*v_dep) * SQ, VEL, 6, tip=0.22).set_z_index(25)
        dv = DashedLine(ta, td, dash_length=0.07).set_stroke(VEL, 4).set_z_index(22)
        def fora(m_, a_, b_, lado):                                           # centro do rótulo a 0,15 da seta, contando o tamanho da caixa
            u_ = (b_ - a_) / np.linalg.norm(b_ - a_)
            n_ = P3(-u_[1], u_[0]) * lado
            return m_.move_to(a_ + (b_ - a_) * 0.5 + n_ * (0.15 + abs(n_[0]) * m_.width / 2 + abs(n_[1]) * m_.height / 2))
        la = fora(txt("ANTES", 28, color=VREL), o_, ta, -1).set_z_index(22)        # do lado de fora de cada seta
        ld = fora(txt("DEPOIS", 28, color=VEL), o_, td, 1).set_z_index(22)
        ldv = mtex(r"\Delta\vec V_{cm}", VEL, 40).set_z_index(22)
        ldv.move_to((ta + td) / 2 + P3(0.2 + ldv.width / 2, -0.12))
        X0 = 1.75
        L1, i1 = eqp(r"\vec J", "=", "m", r"\,(", r"\vec 0", "-", r"\vec v", ")", size=46, cores={0: JC, 6: VEL})
        L2, i2 = eqp("=", "1", r"\cdot", "(", "-", r"4{,}02", ";", r"\ 42{,}72", ")", r"\ \mathrm{N\cdot s}", size=46)
        L3, i3 = eqp(r"\Delta\vec V_{cm}", "=", r"\vec J", "/", "M", size=46, cores={0: VEL, 2: JC})
        L4, _ = eqp("=", "(", r"-0{,}89", ";", r"\ 9{,}49", ")", r"\ \mathrm{m/s}", size=46)
        for L_, x_, y_ in ((L1, X0, 3.15), (L2, X0 + 0.25, 2.5), (L3, X0, 1.75), (L4, X0 + 0.25, 1.1)):
            L_.move_to(P3(x_ + L_.width / 2, y_)).set_z_index(22)
        tri_ = VGroup(sa, sd, la, ld, ldv, Line(o_, ta), Line(o_, td))
        self.g_evita = [vlab, sv, painel, aviso, Jlab, tri_]           # as marcas de tempo desviam deles
        out = [m for m in (getattr(self, "pergunta", None),) if m is not None and m in self.mobjects]
        self.play(FadeIn(fch), *[FadeOut(m) for m in out], run_time=0.4)                        # "bate no chão"
        self.play(ReplacementTransform(fch, Jseta), FadeIn(Jlab), FadeIn(aviso), FadeIn(painel), run_time=0.5)
        self.play(TransformFromCopy(Jlab, L1[0][i1[0][0]:i1[0][-1] + 1]), FadeIn(VGroup(*[L1[0][j] for k in (1, 2, 3, 4, 5, 7) for j in i1[k]])),
                  TransformFromCopy(vlab[0][0:2], VGroup(*[L1[0][j] for j in i1[6]])), g.tau.animate(rate_func=linear).set_value(t1 + 0.06), run_time=1.0)
        # o sinal troca: (4,02; −42,72) → (−4,02; 42,72)
        src = vlab[0][3:]                                                   # glifos depois de "v =": ( 4 , 0 2 ; − 4 2 , 7 2 )
        alvo_ = lambda k: [L2[0][j] for j in i2[k]]
        pares = [(src[0], alvo_(3)[0]), (src[6], alvo_(4)[0]), (src[5], alvo_(6)[0]), (src[12], alvo_(8)[0])]
        pares += list(zip(src[1:5], alvo_(5))) + list(zip(src[7:12], alvo_(7)))
        self.play(FadeIn(VGroup(*[L2[0][j] for k in (0, 1, 2, 9) for j in i2[k]])), *[TransformFromCopy(a_, b_) for a_, b_ in pares],
                  g.tau.animate(rate_func=linear).set_value(t1 + 0.12), run_time=1.1)          # o sinal troca: o "−" pula para a frente
        self.play(FadeOut(vlab), run_time=0.3)                                                 # o v⃗ já está na conta: sai (G6)
        self.g_evita = [m for m in self.g_evita if m is not vlab]
        self.play(TransformFromCopy(fa, sa), TransformFromCopy(fd, sd), FadeIn(fa), FadeIn(fd), g.tau.animate(rate_func=linear).set_value(t1 + 0.17),
                  run_time=0.9)
        self.play(FadeOut(fa), FadeOut(fd), Create(dv), FadeIn(la), FadeIn(ld), FadeIn(ldv), FadeIn(L3), g.tau.animate(rate_func=linear).set_value(t1 + 0.24),
                  run_time=0.9)
        self.play(FadeIn(L4, shift=0.1 * DOWN), g.tau.animate(rate_func=linear).set_value(t1 + 0.32), run_time=0.8)   # segura no descolamento
        rt = (g.ttoque[0] + 0.05 - t1 - 0.32) / 0.5
        if frac:
            rt = max(rt, self.resta() - 0.6)
        self.play(g.tau.animate(rate_func=linear).set_value(g.ttoque[0] - 0.15), run_time=max(0.5, rt - 0.4))
        self.play(g.tau.animate(rate_func=linear).set_value(g.ttoque[0] + 0.05), FadeOut(Jseta), FadeOut(Jlab), FadeOut(sv), run_time=0.4)
        if frac:
            frac(0.97)
        else:
            self.wait(0.5)
        self.g_evita = []
        return VGroup(painel, sa, sd, dv, la, ld, ldv, L1, L2, L3, L4, aviso)                      # triângulo no PALCO, conta no painel

    # ── haltere 2D (T1; v3: sem 3D, §1.5) ─────────────────────────────────────────────────────────────────
    def haltere_giro(self, giro=3.0):
        """T1-1: vista de cima, o haltere (1 kg e 3 kg, separação 4) girando em torno do ⊕ em degradê, rastros circulares finos."""
        h = self.h = Haltere2D(self)
        self.h_pul = ValueTracker(0.0)
        self.add(*h.trackers(), self.h_pul)

        def cena():
            g = VGroup()
            o = h.orb.get_value()
            if o > 0.01:
                a = h.ang.get_value() - h.tilt.get_value()
                a0 = max(h.a_ini, a - 2 * PI)
                for X in (h.X1, h.X2):
                    if a - a0 > 0.02:
                        g.add(Arc(radius=abs(X) * h.K, start_angle=a0 + (PI if X < 0 else 0), angle=a - a0, arc_center=h.cm)
                              .set_stroke(RAST, 2, opacity=0.75 * o))
            g.add(h.desenho())
            g.add(marcador_cm(h.cm, r=0.215 * (1 + 0.45 * self.h_pul.get_value())))
            self.reg("hal", cm=h.cm, b1=h.p(h.X1), b2=h.p(h.X2))
            return g
        h.mob = vivo(cena)
        self.selo_cam = txt("CÂMERA ACOMPANHANDO O CENTRO DE MASSA", 24, color=DIM, op=0.95).move_to(P3(PALCO_C[0], -3.75))
        h.girar()
        self.add(h.mob)
        self.play(FadeIn(self.selo_cam), h.orb.animate.set_value(1.0), run_time=0.6)
        self.wait(giro)
        return h

    # ── explosão no espaço (T2-6, T3-1, T3-2, T3-3) ───────────────────────────────────────────────────────
    def _explosao_camadas(self, e):
        T = self.ex = dict(modo="P", op_p=ValueTracker(1.0), op_mv=ValueTracker(0.0), op_lab=ValueTracker(0.0), u=ValueTracker(0.0),
                           op_vel=ValueTracker(0.0), w=ValueTracker(0.0), op_rel=ValueTracker(0.0), u_tri=ValueTracker(0.0),
                           pul=ValueTracker(0.0), op_30=ValueTracker(0.0), ref="VISTO DO CHÃO")
        self.add(*[v for v in T.values() if isinstance(v, ValueTracker)])

        def camada():
            cs = e.corpos()
            cmv = e.cm()
            tau = e.f3d.e["tau"]
            g = VGroup()
            fr = [c for c, _, _ in cs]
            self.reg("exp", cm=cmv, frags=fr) if len(cs) == 3 else self.reg("exp", cm=cmv, corpo=fr[0])
            if len(cs) == 1:
                c, r, _ = cs[0]
                if T["op_p"].get_value() > 0.01:
                    a = da_borda(c, RIGHT, r)
                    ar = seta(a, a + RIGHT * SP * MT * e.V0, MAG, 6, op=T["op_p"].get_value())
                    g.add(ar, mtex(r"\vec P", MAG, 38).set_opacity(T["op_p"].get_value()).next_to(ar, UP, buff=0.08))
                if T["op_vel"].get_value() > 0.01:
                    a = da_borda(c, RIGHT, r)
                    g.add(seta(a, a + RIGHT * SV * e.V0, VEL, 6, op=T["op_vel"].get_value()))
            else:
                vs = [np.array([e.V0, 0.0]) + d * e.C / m for m, d in zip(MS, DIRS)]
                # T2-6: m_i v_i (chão), deslizando para a soma ponta com ponta ao lado do ⊕ (à direita, na altura dele), sobre o fantasma
                # tracejado da P de antes: a cadeia termina exatamente na ponta dele (pulso quando fecha)
                o, u = T["op_mv"].get_value(), suave(T["u"].get_value())
                if o > 0.01:
                    s0 = cmv + 0.5 * RIGHT
                    cad = [s0]
                    for m, v in zip(MS, vs):
                        cad.append(cad[-1] + P3(*(m * v)) * SP)
                    if u > 0.02:
                        ponta = s0 + RIGHT * SP * MT * e.V0
                        fant = DashedLine(s0, ponta - 0.18 * RIGHT, dash_length=0.1).set_stroke(MAG, 5, opacity=0.5 * o * u)
                        g.add(fant, seta(ponta - 0.2 * RIGHT, ponta, MAG, 5, tip=0.2, op=0.5 * o * u),
                              VGroup(mtex(r"\vec P", MAG, 40), txt("ANTES", 24, color=MAG)).arrange(RIGHT, buff=0.12)
                              .set_opacity(0.8 * o * u).next_to(ponta, RIGHT, buff=0.18))
                    w_ = 5 + 4 * T["pul"].get_value()
                    for k, ((c, r, m), v) in enumerate(zip(cs, vs)):
                        vec = P3(*(m * v)) * SP
                        a = (1 - u) * da_borda(c, vec, r) + u * cad[k]
                        g.add(seta(a, a + vec, MAG, w_, tip=0.2, op=o))
                ol = T["op_lab"].get_value()
                if ol > 0.01:
                    for (c, r, m), d, v in zip(cs, DIRS, vs):
                        perp = P3(-d[1], d[0])
                        if perp @ P3(*(m * v)) > 0:                       # do lado oposto à seta do pedaço
                            perp = -perp
                        g.add(rot((f"{m:g}".replace(".", ",")) + " kg", 32, WHITE_, op=ol).move_to(c + perp * (r + 0.55)))
                # T3-1/T3-2: velocidades (chão → relativas: a parte comum sai)
                ov, w = T["op_vel"].get_value(), suave(T["w"].get_value())
                if ov > 0.01:
                    for (c, r, m), v in zip(cs, vs):
                        vv = P3(*(v - w * np.array([e.V0, 0.0]))) * SV
                        a = da_borda(c, vv, r)
                        g.add(seta(a, a + vv, interpolate_color(ManimColor(VEL), ManimColor(VREL), w).to_hex(), 5, tip=0.18, op=ov))
                # T3-3: momentos relativos iguais → triângulo
                orl, ut = T["op_rel"].get_value(), suave(T["u_tri"].get_value())
                if orl > 0.01:
                    s0 = P3(PALCO_C[0] + 2.9, 0.75)
                    cad = [s0]
                    for d in DIRS:
                        cad.append(cad[-1] + P3(*d) * SR * e.C)
                    o30 = T["op_30"].get_value()
                    for k, ((c, r, m), d) in enumerate(zip(cs, DIRS)):
                        vec = P3(*d) * SR * e.C
                        a = (1 - ut) * da_borda(c, vec, r) + ut * cad[k]
                        g.add(seta(a, a + vec, MAG, 6, tip=0.22, op=orl))
                        if o30 > 0.01:                                     # o mesmo tamanho: 30 N·s cada
                            perp = P3(-d[1], d[0])
                            g.add(mrot("30 N·s", 26, MAG, op=o30 * orl).move_to(a + vec / 2 + perp * 0.32))
            if 0 < T["w"].get_value():
                w = suave(T["w"].get_value())
                a0 = da_borda(cmv, RIGHT, 0.26)
                ini, fim = a0, P3(-1.6, 2.45)                            # canto de cima à direita do PALCO (os cacos não passam)
                a = (1 - w) * ini + w * fim
                ar = seta(a, a + RIGHT * SV * e.V0, VEL, 5)
                g.add(ar, mtex(r"\vec V_{cm}", VEL, 36).next_to(ar, UP, buff=0.06))
            g.add(marcador_cm(cmv))
            o_ = e.f3d.op.get_value()
            if o_ < 0.999:                                       # a camada sai e entra junto com o 3D
                g.fade(1 - o_)
            return g.set_z_index(8)
        self._refs = {k: txt(k, 26, color=DIM, op=0.95) for k in ("VISTO DO CHÃO", "VISTO DO CENTRO DE MASSA")}
        for m in self._refs.values():
            m.move_to(P3(-7.0 + m.width / 2, 2.95))
        ref_ = self._refs["VISTO DO CHÃO"]
        return vivo(camada), ref_

    def troca_ref(self, k, rt=0.5):
        velho = [m for m in self._refs.values() if m in self.mobjects]
        self.ex["ref"] = k
        self.play(*[FadeOut(m) for m in velho], FadeIn(self._refs[k]), run_time=rt)

    def explosao_chao_momento(self, dur=25.0, frac=None, velhos=(), eq=None):
        """T2-6 (visto do chão): P = M V_cm antes; depois as três mᵢv⃗ᵢ do chão, rotuladas, que deslizam e somam a mesma P.
        `velhos`: a cena anterior, que sai em crossfade com esta (G5). `eq`: (MathTex da CONTA, índice do glifo "0") — o 0 sai do selo
        SEM GRAVIDADE (TransformFromCopy) e o resto entra junto."""
        sai = [m.op.animate.set_value(0.0) if isinstance(m, Fundo3D) else FadeOut(m) for m in velhos if not isinstance(m, ValueTracker)]
        e = self.e = Explosao3D(self, K=1.5, camx=-1.6, xc=PALCO_C[0], yc=-0.05, op=0.0)
        e.dolly = (1.5, 1.15, -1.6, 0.6, 4.8)
        self.add(e.tau, e.K, e.camx, e.xc, e.yc, e.seg, e.f3d)
        cam, rot = self._explosao_camadas(e)
        self._corpos3d = [lambda: [(c_, r_) for c_, r_, _ in e.corpos()] if e.f3d in self.mobjects and e.f3d.op.get_value() > 0.15 else []]
        selo = self.selo_esp = txt("NO ESPAÇO, SEM GRAVIDADE", 24, color=DIM, op=0.95)
        selo.move_to(P3(-7.0 + selo.width / 2, 2.55))
        self.add(cam)
        T = self.ex
        if frac:
            # 1ª passada (a fala: "o centro de massa nem percebe"): só o ⊕ seguindo reto, os pedaços voando em velocidade de tela legível
            e.dolly = (1.5, 1.1, -1.6, 0.9, 5.5)
            T["op_p"].set_value(0.0)
            if sai:
                self.play(*sai, run_time=0.35)
            for m in velhos:
                m.clear_updaters()
            self.remove(*velhos)
            self._em_troca = True
            self.play(e.f3d.op.animate.set_value(1.0), FadeIn(rot), FadeIn(selo), run_time=0.35)
            self._em_troca = False
            if eq is not None:
                E, i0 = eq[:2]
                extra = list(eq[2]) if len(eq) > 2 else []
                i0 = list(i0) if isinstance(i0, (list, tuple)) else [i0]
                resto = VGroup(*[g_ for k, g_ in enumerate(E[0]) if k not in i0])
                self.play(e.tau.animate(rate_func=linear).set_value(0.8), TransformFromCopy(selo, VGroup(*[E[0][j] for j in i0])), FadeIn(resto),
                          *[FadeIn(m) for m in extra], run_time=1.0)
            self.play(e.tau.animate(rate_func=linear).set_value(e.TE), run_time=(e.TE - e.tau.get_value()) / 0.8)
            self.play(e.tau.animate(rate_func=linear).set_value(e.TE + 0.5), run_time=0.8)
            self.ate_mov(0.5, e.tau, 5.5)
            # 2ª passada ("E olha o momento: antes, uma seta só"): replay com P, as três m v do chão e a soma ponta com ponta
            self.play(e.f3d.op.animate.set_value(0.0), run_time=0.3)
            e.tau.set_value(0.0)
            self.play(e.f3d.op.animate.set_value(1.0), T["op_p"].animate.set_value(1.0), run_time=0.4)
        else:
            self.play(e.f3d.op.animate.set_value(1.0), FadeIn(rot), FadeIn(selo), *sai, run_time=0.6)
            self.remove(*velhos)
        self.play(e.tau.animate(rate_func=linear).set_value(e.TE), run_time=e.TE * 1.4)
        self.play(e.tau.animate(rate_func=linear).set_value(e.TE + 0.6), self.ex["op_p"].animate.set_value(0.0), run_time=0.8)
        self.play(e.tau.animate(rate_func=linear).set_value(3.0), self.ex["op_mv"].animate.set_value(1.0), run_time=1.6)
        self.play(e.tau.animate(rate_func=linear).set_value(4.0), self.ex["op_lab"].animate.set_value(1.0), run_time=1.6)
        if frac:
            self.ate_mov(0.8, e.tau, 4.25)
        self.play(e.tau.animate(rate_func=linear).set_value(4.6), self.ex["u"].animate.set_value(1.0), self.ex["op_lab"].animate.set_value(0.0),
                  run_time=1.8)
        self.play(e.tau.animate(rate_func=linear).set_value(4.75), self.ex["pul"].animate(rate_func=there_and_back).set_value(1.0),
                  run_time=0.6)                                     # a cadeia fecha na ponta da P de antes
        if frac:
            self.play(e.tau.animate(rate_func=linear).set_value(5.0), run_time=max(0.5, self.resta() - 0.3))
        else:
            self.play(e.tau.animate(rate_func=linear).set_value(5.0), run_time=max(0.5, dur - 0.6 - e.TE * 1.4 - 0.8 - 1.6 - 1.6 - 1.8))
        return e

    def explosao_chao_velocidades(self, e, dur=13.0):
        """T3-1 (visto do chão, replay): velocidades violeta do chão, todas com a parte comum para a direita."""
        T = self.ex
        self.play(e.f3d.op.animate.set_value(0.0), T["op_mv"].animate.set_value(0.0), run_time=0.4)
        e.tau.set_value(0.0)
        T["u"].set_value(0.0)
        self.play(e.f3d.op.animate.set_value(1.0), T["op_vel"].animate.set_value(1.0), run_time=0.4)
        self.play(e.tau.animate(rate_func=linear).set_value(e.TE), run_time=e.TE)
        self.play(e.tau.animate(rate_func=linear).set_value(3.0), run_time=2.0)
        self.play(e.tau.animate(rate_func=linear).set_value(3.4), run_time=max(0.3, dur - 0.8 - e.TE - 2.0))

    def explosao_segue_cm(self, e, dur=20.0):
        """T3-2: a câmera passa a acompanhar o ⊕ (troca suave); a parte comum V_cm sai de todas as velocidades e vai para o canto."""
        T = self.ex
        tau = e.tau.get_value()
        K0, K1, c0, c1, Td = e.dolly
        u = suave(tau / Td)
        e.K.set_value(K0 + (K1 - K0) * u)
        e.camx.set_value(c0 + (c1 - c0) * u)
        e.dolly = None
        self.play(e.seg.animate.set_value(1.0), T["w"].animate.set_value(1.0), e.tau.animate(rate_func=linear).set_value(tau + 0.4), run_time=2.0)
        self.troca_ref("VISTO DO CENTRO DE MASSA")
        self.play(e.tau.animate(rate_func=linear).set_value(tau + 0.6), run_time=max(0.5, dur - 2.5))

    def explosao_relativos(self, e, dur=10.0, frac=None):
        """T3-3: momentos relativos (magenta), os três do mesmo tamanho; depois ponta com ponta fecham o triângulo."""
        T = self.ex
        tau = e.tau.get_value()
        self.play(T["op_vel"].animate.set_value(0.0), T["op_rel"].animate.set_value(1.0), e.tau.animate(rate_func=linear).set_value(tau + 0.15),
                  run_time=1.0)
        self.play(e.tau.animate(rate_func=linear).set_value(tau + 0.3), run_time=1.6)
        if frac:
            self.ate_mov(0.35, e.tau, tau + 0.38)
        self.play(T["u_tri"].animate.set_value(1.0), e.tau.animate(rate_func=linear).set_value(tau + 0.45), run_time=1.6)
        self.play(e.tau.animate(rate_func=linear).set_value(tau + 0.55), run_time=max(0.5, dur - 4.2) if not frac else max(0.5, self.resta() - 0.3))

    # ── semiesfera (E4-3, E4-4) ───────────────────────────────────────────────────────────────────────────
    def semiesfera_cotas(self, dur=7.0, op=1.0):
        s = self.s = Semiesfera3D(self, K=1.5, yc=-1.75, op=op)
        self.add(s.fz, s.f3d)
        R = s.R
        base = [s.p((R * math.cos(t), R * math.sin(t), 0)) for t in np.linspace(0, 2 * PI, 72)]
        xmin, xmax = min(p[0] for p in base), max(p[0] for p in base)
        col_d = xmax + 0.45

        def camada():
            z = s.f3d.e["fz"]
            r = math.sqrt(max(R * R - z * z, 0))
            pc, pb, p0 = s.p((0, 0, z)), s.p((r, 0, z)), s.p((0, 0, 0))
            g = VGroup(Line(pc, pb).set_stroke(GEO, 3))
            lab = mtex(r"\sqrt{R^2-z^2}", GEO, 40)
            lab.move_to(P3(col_d + lab.width / 2, pb[1] + 0.32))
            g.add(Line(pb, P3(col_d - 0.08, pb[1] + 0.32)).set_stroke(GEO, 1.5, opacity=0.8), lab)
            # dz na espessura, na borda esquerda da fatia
            pe_ = s.p((-r, 0, z))
            dzt = VGroup(*[Line(s.p((-r, 0, z + k * s.DZ / 2)) + 0.12 * LEFT, s.p((-r, 0, z + k * s.DZ / 2)) + 0.32 * LEFT).set_stroke(GEO, 2)
                           for k in (-1, 1)])
            g.add(dzt, mtex(r"dz", GEO, 32).next_to(pe_ + 0.32 * LEFT, LEFT, buff=0.1))
            # z: cota vertical da base até a fatia, à direita do eixo
            g.add(cota_v(p0[0] + 0.32, p0[1], pc[1]), mtex("z", GEO, 34).move_to(P3(p0[0] + 0.55, (p0[1] + pc[1]) / 2)))
            self.reg("hem", borda_fatia=pb, cm=s.p((0, 0, 3 * R / 8)))
            return g.set_z_index(8)
        viva = vivo(camada)
        p0, pcm = s.p((0, 0, 0)), s.p((0, 0, 3 * R / 8))
        c38 = cota_v(p0[0] - 0.32, p0[1], pcm[1], WHITE_)
        l38 = mtex(r"\tfrac{3R}{8}", WHITE_, 46)
        l38.move_to(P3(xmin - 0.35 - l38.width / 2, (p0[1] + pcm[1]) / 2))
        guia = Line(P3(p0[0] - 0.4, (p0[1] + pcm[1]) / 2), P3(xmin - 0.3, (p0[1] + pcm[1]) / 2)).set_stroke(WHITE_, 1.4, opacity=0.6)
        cm = marcador_cm(pcm)
        s.varrer(6.0)
        self.add(viva)
        self.play(FadeIn(c38), FadeIn(l38), FadeIn(guia), FadeIn(cm), *([s.f3d.op.animate.set_value(1.0)] if op < 1 else []), run_time=0.6)
        self.wait(max(0.5, dur - 0.6))
        return VGroup(c38, l38, guia, cm), viva

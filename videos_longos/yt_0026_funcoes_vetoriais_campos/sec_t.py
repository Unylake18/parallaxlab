"""Lote PT: abertura do Cálculo III (handoff v6, T0–T5): do infinitamente pequeno ao espaço inteiro, tudo em movimento e com texto desde o primeiro quadro.
T0 uma seta → partículas e o redemoinho (a câmera recua) · T1 colunas viram volume (3D) · T2 trabalho: ponto andando pela curva num campo vivo, barra que sobe e
desce (2D) · T3 fluxo: chuva de setas atravessa a tigela em retalhos (3D), barra crescente, corte seco · T4 as trocas entre vizinhos se cancelam: (a) Green no plano,
(b) Stokes na calota, (c) Gauss nos cubinhos, o trio ainda em movimento e a frase grande · T5 o redemoinho se fecha numa seta, que vira o acento do cartão CÁLCULO III.
Sem canto, sem fórmulas, sem porcentagem."""
from kit import *  # noqa: F401,F403

GIRO = lambda x, y: (-y, x)
# constantes da cena 3D `tigela` (as mesmas do f26.js): o Manim recalcula o instante em que a ponta cruza cada retalho
R_T, NA_T, NS_T, ZT_T, VQ_T = 1.4, 3, 12, 3.4, 1.05
PER = 4.5            # período dos laços do trio do T4 (s)
BRANCO_C = "#E8F0FF"


def manchete(s, y=3.45, color=WHITE_, size=30):
    return txt(s, size, bold=True, color=color).move_to(P3(0, y)).set_z_index(30)


class Barra(VGroup):
    """Barra de medidor: placa ESC + preenchimento. `centro=True`: zero no meio (menta para a direita, coral para a esquerda); senão cresce da esquerda."""

    def __init__(self, pos, w=6.0, h=0.5, centro=False):
        super().__init__()
        self.pos, self.w, self.h, self.centro = np.asarray(pos, float), w, h, centro
        self.placa = RoundedRectangle(width=w + 0.2, height=h + 0.2, corner_radius=0.1).set_fill(ESC, 0.9).set_stroke(SAI_F, 2).move_to(pos).set_z_index(8)
        self.placa._sem_contorno = True
        self.fill = Rectangle(width=0.01, height=h).set_fill(CAMPO, 1).set_stroke(width=0).move_to(pos).set_z_index(9)
        self.fill._sem_contorno = True
        self.add(self.placa, self.fill)
        if centro:
            z = Line(self.pos + UP * (h / 2 + 0.12), self.pos + DOWN * (h / 2 + 0.12)).set_stroke(GEO, 2.5).set_z_index(10)
            z._sem_contorno = True
            self.add(z)
        self.poe(0.0)

    def poe(self, v):
        """v em [-1, 1] (centro) ou [0, 1]."""
        L = max(0.01, abs(v) * (self.w / 2 if self.centro else self.w))
        cor = CAMPO if v >= 0 else DEST
        cx = self.pos[0] + np.sign(v) * L / 2 if self.centro else self.pos[0] - self.w / 2 + L / 2
        self.fill.become(Rectangle(width=L, height=self.h).set_fill(cor, 1).set_stroke(width=0).move_to(P3(cx, self.pos[1])).set_z_index(9))
        self.fill._sem_contorno = True


class Redemoinho:
    """O redemoinho (−y, x) que nasce de UMA seta. `estado(a, W, big)`: a = 0 só o pé do ponto (0,75; 0) ampliado ×S0·big e parado em C; a = 1 o campo inteiro.
    A câmera 'recua' escalando os PONTOS do grupo; as vizinhas acendem em onda (raio W em unidades normalizadas) a partir do pé da seta."""
    S0 = 4.0

    def __init__(self, cena, nome, C=(0.0, 0.0), origem=(0.0, -0.15), n_part=180):
        self.pl = Plano(origem, 1.0)
        self.g = campo(self.pl, GIRO, grade_pts(3.0, 0.75), 0.2, nome, passo=0.75)
        self.foot = [s for s in self.g if s._xy == (0.75, 0.0)][0]
        self.Fn = self.pl.c2p(0.75, 0.0)
        self.C = P3(*C)
        self.s, self.P = 1.0, self.Fn.copy()
        self.dot = ponto(self.Fn, SAI_F, 0.07, z=9)
        dmax = max(math.hypot(s._xy[0] - 0.75, s._xy[1]) for s in self.g)
        self.ar = [(s, math.hypot(s._xy[0] - 0.75, s._xy[1]) / dmax) for s in self.g]
        self.base = [(m, m.points.copy()) for m in self.g.get_family() if isinstance(m, VMobject) and len(m.points)]
        self.op = {}
        self.part = Particulas(cena, GIRO, self.proj, lambda x, y: math.hypot(x, y) < 3.15, n=n_part, vel=0.7, rmax=3.1)
        self.estado(0.0)

    def proj(self, xy):
        p = np.zeros((len(xy), 3))
        p[:, 0], p[:, 1] = self.pl.o[0] + xy[:, 0], self.pl.o[1] + xy[:, 1]
        return self.s * (p - self.Fn) + self.P

    def estado(self, a, W=None, big=1.0):
        ap = suave(a)
        s = self.S0 ** (1 - ap) * big
        P = self.Fn + (self.C - self.Fn) * (1 - ap)
        self.s, self.P = s, P
        for m, b in self.base:
            m.points = s * (b - self.Fn) + P
        W = (0.05 + 1.35 * ap) if W is None else W
        for sa, dn in self.ar:
            o = 1.0 if sa is self.foot else round(min(1.0, max(0.0, (W - dn) / 0.15)), 2)
            if self.op.get(id(sa)) != o:
                sa.set_opacity(o)
                self.op[id(sa)] = o
        self.dot.move_to(P)

    def anim(self, a0, a1, rt, rate=smooth, **kw):
        return UpdateFromAlphaFunc(self.g, lambda m, al: self.estado(a0 + (a1 - a0) * al, **kw), run_time=rt, rate_func=rate)


class Green2D(VGroup):
    """Quadrado n×n de células no plano: em cada célula um rotor GIRANDO (o rotacional de (−y, x) vale 2 em todo ponto) e traços correndo no sentido
    anti-horário em volta; os 12 lados internos piscam e somem aos pares (em tc0 + 0,25 i) e sobra a borda, mais acesa. `tfun()` = tempo local (s)."""

    def __init__(self, cena, centro, k, tfun, tc0=1e9, n=3, lado=1.15, passo=0.25):
        super().__init__()
        self.tf, self.tc0, self.k, self.n, self.passo = tfun, tc0, k, n, passo
        self.lado = lado * k
        self.c = np.asarray(centro, float)
        L = self.lado
        o = self.c - L * n / 2 * (RIGHT + UP)
        self.o = o
        ch = Rectangle(width=L * n, height=L * n).set_fill(CH_DOM, 0.85).set_stroke(width=0).move_to(self.c).set_z_index(1)
        ch._sem_contorno = True
        self.add(ch)
        self.lados = {}
        q = 0
        for j in range(n + 1):
            for i in range(n):
                self._lado(("h", j, i), o + L * (i * RIGHT + j * UP), o + L * ((i + 1) * RIGHT + j * UP), 0 < j < n)
        for i in range(n + 1):
            for j in range(n):
                self._lado(("v", i, j), o + L * (i * RIGHT + j * UP), o + L * (i * RIGHT + (j + 1) * UP), 0 < i < n)
        for ch_, l in self.lados.items():
            if l["int"]:
                l["tc"] = q * passo
                q += 1
        self.dots, self.rot = [], []
        for i in range(n):
            for j in range(n):
                cc = o + L * ((i + 0.5) * RIGHT + (j + 0.5) * UP)
                r = VGroup(VMobject(), VMobject()).set_z_index(6)
                r._cc, r._ang = cc, 0.0
                for m in r:
                    m._sem_contorno = True
                self.rot.append(r)
                self.add(r)
                self._rotor(r)
                for u0 in (0.0, 1 / 3, 2 / 3):
                    d = Dot(cc, radius=max(0.03, 0.055 * k), color=BRANCO_C).set_z_index(7)
                    d._sem_contorno, d._cel, d._u0 = True, (i, j), u0
                    self.dots.append(d)
                    self.add(d)
        self.tprev = None
        self.add_updater(lambda m: m._quadro())
        self._quadro()

    def _lado(self, chave, a, b, interno):
        ln = Line(a, b).set_stroke(SAI_F, 3.0, 1).set_z_index(5)
        ln._sem_contorno = True
        self.add(ln)
        self.lados[chave] = {"m": ln, "int": interno, "tc": 1e9}

    def _rotor(self, r):
        cc, ang, rad = r._cc, r._ang, 0.24 * self.k
        r[0].become(Arc(radius=rad, start_angle=ang, angle=4.5, arc_center=cc).set_stroke(CAMPO_FORTE, 3.2, 1).set_fill(opacity=0))
        th = ang + 4.5
        p = cc + rad * np.array([math.cos(th), math.sin(th), 0.0])
        tg, nn, s_ = np.array([-math.sin(th), math.cos(th), 0.0]), np.array([math.cos(th), math.sin(th), 0.0]), 0.12 * self.k
        r[1].set_points_as_corners([p + tg * s_ * 1.7, p + nn * s_, p - nn * s_, p + tg * s_ * 1.7]).set_fill(CAMPO_FORTE, 1).set_stroke(CAMPO_FORTE, 1.0, 1)
        for m in r:
            m._sem_contorno = True

    def _perim(self, i, j, u):
        """Ponto da célula (i, j) no perímetro, anti-horário (u em [0, 1): 0 = canto inferior esquerdo) e a chave do lado em que está."""
        L, o = self.lado, self.o
        a = o + L * (i * RIGHT + j * UP)
        s = (u % 1.0) * 4
        q, f = int(s), s - int(s)
        if q == 0:
            return a + L * f * RIGHT, ("h", j, i)
        if q == 1:
            return a + L * RIGHT + L * f * UP, ("v", i + 1, j)
        if q == 2:
            return a + L * (RIGHT + UP) - L * f * RIGHT, ("h", j + 1, i)
        return a + L * UP - L * f * UP, ("v", i, j)

    def _quadro(self):
        t, n = self.tf(), self.n
        dt = 0.0 if self.tprev is None else max(0.0, min(0.5, t - self.tprev))
        self.tprev = t
        fim = self.tc0 + 12 * self.passo + 0.1
        vivo = {}
        for ch, l in self.lados.items():
            tc = self.tc0 + l["tc"] if l["int"] else 1e9
            viva, flash = t < tc, l["int"] and tc - 0.1 <= t < tc + 0.12
            vivo[ch] = viva
            ln = l["m"]
            if viva or flash:
                borda_acesa = (not l["int"]) and t > fim
                ln.set_stroke(BRANCO_C if flash else (CAMPO_FORTE if borda_acesa else SAI_F), 6.5 if flash else (7.0 if borda_acesa else 3.0), 1)
            else:
                ln.set_stroke(opacity=0)
        for d in self.dots:
            i, j = d._cel
            p, ch = self._perim(i, j, 0.5 * t + d._u0 + 0.13 * (i + 3 * j))
            d.move_to(p)
            d.set_fill(opacity=1.0 if vivo.get(ch, True) else 0.0)
        vis = t <= fim + 0.4
        for r in self.rot:
            r._ang += 2.0 * dt
            self._rotor(r)
            r[0].set_stroke(opacity=1.0 if vis else 0.0)
            r[1].set_fill(opacity=1.0 if vis else 0.0).set_stroke(opacity=1.0 if vis else 0.0)
        return self


class LoteT(Base):
    CANTO = False

    def corte(self, velhos, novos, rt=0.25):
        """Dissolve curto: o quadro velho sai e o novo entra no mesmo play."""
        anims = [m.op.animate.set_value(0.0) if isinstance(m, Fundo3D) else FadeOut(m) for m in velhos]
        anims += [m.op.animate.set_value(1.0) if isinstance(m, Fundo3D) else FadeIn(m) for m in novos]
        self.play(*anims, run_time=rt)
        for m in velhos:
            m.clear_updaters()
        self.remove(*velhos)

    def corpo(self):
        seg = {}
        self.papel(True)

        # ── T0 · uma seta, num ponto só; partículas e o redemoinho; a câmera recua ──
        self.an("T0")
        rd = Redemoinho(self, "T0 giro (−y, x)", C=(0.0, 0.0))
        rd.estado(0.0, W=0.0, big=1.9)
        t0a = manchete("UMA SETA")
        self.add(rd.g, rd.dot)
        self.play(FadeIn(t0a), FadeIn(rd.dot, scale=0.5), GrowArrow(rd.foot), run_time=0.8)
        self.play(pulso(rd.foot, 1.12, 1.4), run_time=0.7)
        self.gat("quase não diz nada")
        self.play(UpdateFromAlphaFunc(rd.g, lambda m, al: rd.estado(0.0, W=0.0, big=1.9 - 0.9 * al), run_time=0.7, rate_func=smooth))
        self.gat("junta infinitas delas")
        t0b = manchete("INFINITAS SETAS: UM CAMPO")
        self.add(rd.part)
        rt0 = max(2.0, self.resta() - 0.15)
        self.play(FadeOut(t0a, run_time=0.3), FadeIn(t0b, run_time=0.3),
                  UpdateFromAlphaFunc(rd.g, lambda m, al: rd.estado(al, W=0.05 + 1.4 * min(1.0, al * 6.0)), run_time=rt0, rate_func=smooth), run_time=rt0)   # onda em ~0,8 s e a câmera recua junto
        self._fecha()

        # ── T1 · colunas finíssimas viram volume ──
        self.an("T1")
        seg["c"] = self.t

        def est_col(t):
            u = t - seg["c"]
            nivel = 0
            for k, n in (("l1", 1), ("l2", 2), ("l3", 3), ("l4", 4)):
                if k in seg and t >= seg[k]:
                    nivel = n
            return {"nivel": nivel, "cam": cam_obl(-58 + 5 * u, 30, (1.5, 1, 0.9), K=2.0, yc=-0.3)}
        col = Fundo3D(self, "colunas", est_col, op=0.0)
        self.add(col)
        h1 = manchete("VOLUME")
        self.corte([rd.g, rd.dot, rd.part, t0b], [col, h1], rt=0.5)
        self.gat("empilha colunas finíssimas")
        seg["l1"] = self.t
        self.gat("debaixo de uma superfície")
        seg["l2"] = self.t
        self.gat("e elas viram um volume")
        seg["l3"] = self.t
        self.wait(0.6)
        seg["l4"] = self.t
        self.wait(max(0.1, self.resta() - 0.2))
        self._fecha()

        # ── T2 · trabalho: um ponto anda pela curva num campo vivo ──
        self.an("T2")
        self.papel(False)
        F2 = lambda x, y: (math.cos(0.8 * x), 0.5)
        pl2 = Plano((0, 0), 1.0)
        pts2 = [(x, y) for x in np.arange(-6.5, 6.6, 1.0) for y in np.arange(-2.5, 2.6, 1.0)]
        cmp2 = campo(pl2, F2, pts2, 0.5, "T2 (cos 0,8x ; 0,5)", w=4.5).set_opacity(0.55)
        part2 = Particulas(self, F2, lambda xy: np.c_[xy, np.zeros(len(xy))], lambda x, y: abs(x) < 6.7 and -2.9 < y < 2.8, n=170, vel=0.9, rmax=6.7, semente=5)
        fc = lambda s: P3(s, 1.1 * math.sin(0.75 * s) - 0.5 + 0.25 * math.cos(1.9 * s))
        curva = ParametricFunction(fc, t_range=[-5.6, 5.6]).set_stroke(POS, W_GAMA, 1.0).set_z_index(4)
        contorno(curva)
        N2 = 400
        pp = np.array([fc(x) for x in np.linspace(-5.6, 5.6, N2 + 1)])
        dr = np.diff(pp, axis=0)
        cum = np.concatenate([[0.0], np.cumsum([F2(*pp[k][:2])[0] * dr[k][0] + F2(*pp[k][:2])[1] * dr[k][1] for k in range(N2)])])
        vmax = float(np.max(np.abs(cum)))
        h2 = manchete("TRABALHO")
        bar2 = Barra(P3(0, -3.55), w=6.0, centro=True)
        rot_a, rot_b = txt("ATRAPALHA", 20, color=DIM).move_to(P3(-4.4, -3.55)), txt("AJUDA", 20, color=DIM).move_to(P3(4.1, -3.55))
        andado = VMobject().set_stroke(POS, W_GAMA + 3, 1.0).set_z_index(5)
        andado._sem_contorno = True
        pv = ponto(fc(-5.6), POS, r=0.1, z=8)
        tg_ = seta(pp[0], pp[0] + RIGHT, WHITE_, 5, tip=0.22).set_z_index(7)
        fp = seta(pp[0], pp[0] + RIGHT, CAMPO_FORTE, 4.5, tip=0.2).set_z_index(6)
        self.add(part2)
        self.corte([col, h1], [cmp2, curva, h2, bar2, rot_a, rot_b, pv], rt=0.25)
        self.add(andado, fp, tg_)

        def anda(g, al):
            k = max(2, int(round(al * N2)))
            P = pp[k]
            tg = pp[min(N2, k + 1)] - pp[max(0, k - 1)]
            tg = tg / np.linalg.norm(tg)
            Fv = np.array([*F2(P[0], P[1]), 0.0])
            comp = float(np.dot(Fv, tg))
            andado.set_points_as_corners(pp[:k + 1])
            pv.move_to(P)
            tg_.become(seta(P, P + 0.95 * (comp if abs(comp) > 0.05 else 0.05) * tg, WHITE_, 5, tip=0.22).set_z_index(7))
            fp.become(seta(P, P + 0.8 * Fv, CAMPO_FORTE, 4.5, tip=0.2).set_z_index(6))
            bar2.poe(float(cum[k] / vmax))
        anda(None, 0.001)
        self.play(UpdateFromAlphaFunc(VGroup(andado, pv, tg_, fp, bar2), anda), rate_func=linear, run_time=max(2.0, self.resta() - 0.3))
        self._fecha()
        print(f"[qa] T2 trabalho: barra de {min(cum) / vmax:+.2f} a {max(cum) / vmax:+.2f} (sobe e desce)")

        # ── T3 · fluxo: a chuva de setas atravessa a tigela em retalhos (3D) ──
        self.an("T3")
        seg["tg"] = self.t

        def est_tg(t):
            u = t - seg["tg"]
            return {"t": u, "cam": cam_obl(-62 + 3.0 * u, 32, (0, 0, 1.3), K=1.5, xc=-1.8, yc=-0.1)}
        tg3 = Fundo3D(self, "tigela", est_tg, op=0.0)
        self.add(tg3)
        self.papel(True)
        h3 = manchete("FLUXO")
        bar3 = Barra(P3(4.7, 0.3), w=3.2, centro=False)
        rot3 = txt("O QUE JÁ ATRAVESSOU", 20, color=DIM).move_to(P3(4.7, -0.3))
        pesos = [((i + 1) ** 2 - i ** 2) / NA_T ** 2 for i in range(NA_T) for _ in range(NS_T)]
        tcs = [(ZT_T - (R_T * (i + 0.5) / NA_T) ** 2) / VQ_T for i in range(NA_T) for _ in range(NS_T)]
        tot = sum(pesos)

        def fluxo(m):
            t = self.clk.get_value() - seg["tg"]
            m.poe(sum(w * min(1.0, max(0.0, (t - tc) / 0.3)) for w, tc in zip(pesos, tcs)) / tot)
        bar3.add_updater(fluxo)
        self.corte([cmp2, curva, h2, bar2, rot_a, rot_b, pv, andado, tg_, fp, part2], [tg3, h3, bar3, rot3], rt=0.25)
        self._fecha()
        print(f"[qa] T3 tigela: cruzamentos de {min(tcs):.2f} a {max(tcs):.2f} s (cena dura {self.t - seg['tg']:.1f} s)")

        # ── T4 · as trocas entre vizinhos se cancelam: (a) Green, (b) Stokes, (c) Gauss; trio e frase ──
        self.an("T4")
        bar3.clear_updaters()
        seg["a"] = self.t
        self.papel(False)
        ref = P3(0, -0.55)
        rdm = campo(Plano(ref, 1.0), GIRO, grade_pts(3.0, 0.75), 0.2, "T4 giro (−y, x)", passo=0.75).set_opacity(0.4)
        part4 = Particulas(self, GIRO, lambda xy: np.c_[xy + np.array([ref[0], ref[1]]), np.zeros(len(xy))], lambda x, y: math.hypot(x, y) < 3.15, n=140, vel=0.7, rmax=3.1, semente=3)
        verde = Green2D(self, ref, 1.0, lambda: self.clk.get_value() - seg["a"])
        h4a = manchete("PEDACINHO POR PEDACINHO")
        self.add(part4)
        self.corte([tg3, h3, bar3, rot3], [rdm, verde, h4a], rt=1 / FPS)
        self.gat("as trocas entre vizinhos se cancelam")
        verde.tc0 = self.clk.get_value() - seg["a"] + 0.05
        self.gat("no plano")
        h4b = manchete("GREEN · NO PLANO", color=SAI_F)
        self.play(FadeOut(h4a), FadeIn(h4b), run_time=0.3)
        # (b) Stokes: calota em células
        self.gat("numa superfície")
        seg["b"] = self.t
        cal = Fundo3D(self, "calota", lambda t: {"t": t - seg["b"], "cam": cam_obl(-58 + 2 * (t - seg["b"]), 38, (0, 0, 0.5), K=1.7, yc=-0.2)}, op=0.0)
        self.add(cal)
        self.papel(True)
        h4c = manchete("STOKES · NUMA SUPERFÍCIE", color=SAI_F)
        self.corte([rdm, verde, part4, h4b], [cal, h4c], rt=0.25)
        # (c) Gauss: cubinhos
        self.gat("num volume")
        seg["c2"] = self.t
        gau = Fundo3D(self, "gauss", lambda t: {"t": t - seg["c2"], "cam": cam_obl(-58 + 3 * (t - seg["c2"]), 28, (0, 0, 0.7), K=1.7, yc=-0.1)}, op=0.0)
        self.add(gau)
        h4d = manchete("GAUSS · NUM VOLUME", color=SAI_F)
        self.corte([cal, h4c], [gau, h4d], rt=0.25)
        # trio, ainda em movimento (laços de 4,5 s)
        self.gat("o local e o global")
        seg["trio"] = self.t
        X = (-5.3, 0.0, 5.3)
        Y3 = 1.35
        lo = lambda: ((self.clk.get_value() - seg["trio"]) % PER)
        verde3 = Green2D(self, P3(X[0], Y3), 0.5, lo, tc0=0.4)
        cal3 = Fundo3D(self, "calota", lambda t: {"t": (t - seg["trio"]) % PER, "cam": cam_obl(-58 + 2 * ((t - seg["trio"]) % PER), 38, (0, 0, 0.5), K=3.0, xc=X[1], yc=Y3 - 0.05)}, op=0.0)
        gau3 = Fundo3D(self, "gauss", lambda t: {"t": (t - seg["trio"]) % PER, "cam": cam_obl(-58 + 3 * ((t - seg["trio"]) % PER), 28, (0, 0, 0.7), K=3.0, xc=X[2], yc=Y3 - 0.05)}, op=0.0)
        self.add(cal3, gau3)
        nomes = VGroup()
        for (nm, sub), x in zip((("GREEN", "NO PLANO"), ("STOKES", "NUMA SUPERFÍCIE"), ("GAUSS", "NUM VOLUME")), X):
            nomes.add(VGroup(txt(nm, 38, bold=True), txt(sub, 22, color=SAI_F)).arrange(DOWN, buff=0.12).move_to(P3(x, -0.55)))
        self.play(FadeOut(h4d), FadeIn(verde3), FadeIn(nomes), cal3.op.animate.set_value(1.0), gau3.op.animate.set_value(1.0), gau.op.animate.set_value(0.0), run_time=0.7)
        gau.clear_updaters()
        self.remove(gau)
        l1 = linha_texto(txt("O LOCAL", 58, bold=True, color=CAMPO), txt("E", 58, bold=True), txt("O GLOBAL", 58, bold=True, color=SAI_F), buff=0.3)
        fim = VGroup(l1, txt("ESTÃO CONECTADOS.", 58, bold=True)).arrange(DOWN, buff=0.22).move_to(P3(0, -2.5))
        self.wait(0.5)
        self.play(FadeIn(fim, shift=0.12 * UP), run_time=0.6)
        self.wait(max(0.1, self.resta() - 0.1))
        self._fecha()

        # ── T5 · o redemoinho se fecha numa seta, que vira o acento do cartão ──
        self.an("T5")
        rd5 = Redemoinho(self, "T5 giro (−y, x)", C=(0.0, -1.9))
        rd5.estado(1.0)
        self.add(rd5.part)
        self.corte([verde3, cal3, gau3, nomes, fim], [rd5.g, rd5.dot], rt=0.2)
        self.gat("isso é cálculo três")
        self.play(rd5.anim(1.0, 0.0, 1.3), FadeOut(rd5.part, run_time=0.5), run_time=1.3)
        self.remove(rd5.part)
        painel = RoundedRectangle(width=12.4, height=3.4, corner_radius=0.2).move_to(P3(0, 0.9)).set_fill(ESC, 0.9).set_stroke(SAI_F, 2).set_z_index(20)
        painel._sem_contorno = True
        card = txt("CÁLCULO III", 96, bold=True).move_to(P3(0, 1.65)).set_z_index(21)
        linha = txt("DO INFINITAMENTE PEQUENO AO ESPAÇO INTEIRO.", 30, bold=True, color=SAI_F).move_to(P3(0, 0.1)).set_z_index(21)
        self.gat("do infinitamente pequeno")
        acento = rd5.foot
        self.play(FadeIn(painel), FadeIn(card, scale=0.96), FadeIn(linha, shift=0.1 * UP), FadeOut(rd5.dot),
                  acento.animate.scale(0.55).move_to(P3(0, 0.88)).set_z_index(22), run_time=0.9)
        self.gat("aquela seta")
        self.play(pulso(acento, 1.25, 1.6), run_time=1.0)
        self.sai_fim()

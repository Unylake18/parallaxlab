"""Lote PT5 (v2): T5 — para onde aponta um giro? (Three.js 'disco' e 'livros').
T5-1 o disco 2D ganha volume: no quadro da troca o disco 3D tem o mesmo centro, raio e θ (câmera de cima, K = DR); depois a câmera inclina até a
elevação EL3 (o círculo de P bem aberto) e o eixo aparece. Pião e Terra grandes, com o eixo e a seta ω⃗ violeta. T5-2 dois livros grandes (capa com
logo, contracapa escura, seta normal à capa), câmera 3/4 por baixo e de lado, eixos x, y, z FIXOS NO LABORATÓRIO, giros extrínsecos (R_final = R₂·R₁):
esquerda Rx(90°) e depois Ry(90°) → capa em −y; direita Ry(90°) e depois Rx(90°) → capa em +x. Os livros ocupam o quadro inteiro no T5-2 (a CONTA
está vazia) e deslizam para o ESQUEMA no T5-3. T5-3 vetores comutam (A⃗ + B⃗ = B⃗ + A⃗, os termos trocam de lugar), giros finitos não. T5-4 10°, 1°,
5° (tabela 10° · 5° · 1° preenchida na ordem da fala, ÷4) com o fantasma do livro da direita sobre o da esquerda e o arco âmbar entre as normais.
T5-5…T5-8: disco de aço (Three.js) em câmera 3/4; o disco gira devagar (FR × ω mostrado) para o ponto P passar pela FRENTE quando v⃗ e a⃗ estão na tela
(v⃗ nunca sai paralela a ω⃗ na tela, D31). T5-6 O no eixo ACIMA do disco, r⃗, paralelogramo entre ω⃗ e r⃗, φ, r_⊥; v⃗ = ω⃗ × r⃗ calculado no Three.js; O
desliza pelo eixo (v⃗ não muda). T5-7 pontos opostos. T5-8 α⃗ (2D, ao lado do eixo, na ponta de ω⃗ ela nunca some dentro do disco) e
a⃗ = α⃗ × r⃗ + ω⃗ × (ω⃗ × r⃗) com as duas setas verdes no ponto P. Álgebra do v2: nenhuma linha de equação por FadeIn (escrita em ordem, voos, passo)."""
from pecas20 import *  # noqa: F401,F403
import prob2 as _p2

EL3 = 38.0                     # elevação da câmera do disco 3D (T5-1 fim, T5-5…T5-8)
KD, CD = 2.5, P3(-3.75, -0.85)  # escala e centro do disco 3D em câmera 3/4
KW, KV, KA3 = 1.5, 1.25, 1.7    # escalas das setas 3D (mundo por rad/s, por m/s, por m/s²) — fora de escala entre si (marcador no T5-8)
FR = 0.03                      # giro na tela = FR × ω mostrado: P fica na frente do disco enquanto v⃗ e a⃗ estão na tela
W5 = 0.6                       # ω mostrado no T5-5…T5-7
AL5 = 0.3                     # α mostrado no T5-8
TH6 = math.radians(-166.0)     # θ de P no início do T5-6 (v⃗ nasce com P na frente-esquerda e passa pela frente no T5-6_82)
AZL, ELL = -62.0, -18.0         # livros: câmera 3/4, por baixo e de lado
BGT = "#0B1530"                # contorno escuro atrás dos rótulos sobre o aço claro
DIRS = [P3(math.cos(k * PI / 4), math.sin(k * PI / 4)) for k in range(8)]


def Rx(a):
    c, s = math.cos(a), math.sin(a)
    return np.array([[1, 0, 0], [0, c, -s], [0, s, c]])


def Ry(a):
    c, s = math.cos(a), math.sin(a)
    return np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]])


def ang_rot(D):
    return math.degrees(math.acos(max(-1.0, min(1.0, (np.trace(D) - 1) / 2))))


def fl(R):
    return [round(float(x), 5) for x in np.asarray(R).reshape(-1)]


def dif_g(g_):
    a = math.radians(g_)
    return ang_rot((Ry(a) @ Rx(a)) @ (Rx(a) @ Ry(a)).T)


def fmt_g(v):
    return (f"{v:.3f}" if v < 0.1 else f"{v:.2f}").replace(".", ",")


def opa(m, o):
    """Opacidade de fill, stroke e contorno de fundo de toda a família (escala_op só mexe no fill)."""
    for x in m.family_members_with_points():
        if isinstance(x, VMobject):
            x.set_fill(opacity=x.get_fill_opacity() * o, family=False)
            x.set_stroke(opacity=x.get_stroke_opacity() * o, family=False)
            x.set_stroke(opacity=x.get_stroke_opacity(background=True) * o, background=True, family=False)
    return m


def fundo(m):
    """Rótulo sobre o aço claro do 3D: contorno escuro por trás (a cor da grandeza não muda)."""
    return m                                                    # contorno de fundo desligado: no Cairo ele escurecia o glifo inteiro


def rot(tex_, cor, size=44):
    return fundo(mtex(tex_, cor, size))


def mtp(*partes, size=48, cores=None):
    """MathTex com uma submobject por parte (para TransformMatchingTex), cor por parte e os registros do eqp (_partes, _gl)."""
    m = MathTex(*partes, font_size=size, color=WHITE_)
    cores = cores or {}
    idx, k = [], 0
    for i, p_ in enumerate(partes):
        n = len([x for x in m[i].family_members_with_points() if not x.submobjects]) or 1
        idx.append(list(range(k, k + n)))
        k += n
        c = cores.get(i)
        if c is not None:
            m[i].set_color(c)
            m[i].set_stroke(c, width=1.8, background=False)
    m._partes = [(t, cores.get(i, WHITE_)) for i, t in enumerate(partes)]
    m._gl = list(zip(partes, idx))
    return m


def pinta(M_, js, cor):
    for j in js:
        M_[0][j].set_color(cor)
        M_[0][j].set_stroke(cor, width=1.8, background=False)


def dseg(p, a, b):
    p, a, b = np.asarray(p, float)[:2], np.asarray(a, float)[:2], np.asarray(b, float)[:2]
    ab = b - a
    L2 = float(ab @ ab)
    u = 0.0 if L2 < 1e-9 else max(0.0, min(1.0, float((p - a) @ ab) / L2))
    return float(np.linalg.norm(p - (a + u * ab)))


class Lados:
    """Rótulo vivo no lado livre (G27): 8 direções em volta da âncora, nota = menor distância às setas/linhas e aos rótulos já postos;
    histerese (o rótulo só troca de lado quando o outro lado fica claramente melhor)."""

    def __init__(self, zona=(-7.2, 0.1, -3.5, 2.4)):
        self.k, self.zona = {}, zona

    def poe(self, nome, m, a, segs, pts, d=0.1, pref=None):
        w, h = m.width, m.height
        sc, best, bk = {}, -99.0, 0
        z = self.zona
        for k, u in enumerate(DIRS):
            c = np.asarray(a, float) + u * (d + abs(u[0]) * w / 2 + abs(u[1]) * h / 2)
            cant = [c + P3(sx * w / 2, sy * h / 2) for sx in (-1, 0, 1) for sy in (-1, 0, 1)]
            s = min([min(dseg(q, p0, p1) for q in cant) for p0, p1 in segs] + [9.0])
            s = min([s] + [np.linalg.norm(c[:2] - np.asarray(p)[:2]) - 0.62 * (w + h) for p in pts])
            if c[0] - w / 2 < z[0] or c[0] + w / 2 > z[1] or c[1] - h / 2 < z[2] or c[1] + h / 2 > z[3]:
                s -= 3.0
            if pref is not None and k in pref:
                s += 0.08
            sc[k] = (s, c)
            if s > best:
                best, bk = s, k
        k0 = self.k.get(nome)
        if k0 is not None and sc[k0][0] >= best - 0.12:
            bk = k0
        self.k[nome] = bk
        m.move_to(sc[bk][1])
        pts.append(sc[bk][1])
        return m


class LoteT5(L20):

    def construct(self):
        self.setup_base()
        self.pilha.x0, self.pilha.larg = X_CONTA + 0.1, LARG_CONTA - 0.1      # o respiro do destaque (escala 1,06) das linhas não entra na CALHA
        self.t5()
        self.fim()
        self.relatorio()
        self.gravar_reg()

    def pg(self, src, dst, *mapas, **kw):
        """passo com conferência: todo glifo da mãe e da filha está em algum mapa (senão o MF-Tools põe os índices no vídeo)."""
        a = sorted({j for m in mapas for j in m[0]})
        b = sorted({j for m in mapas for j in m[1]})
        assert a == list(range(len(src[0]))) and b == list(range(len(dst[0]))), (src.get_tex_string(), dst.get_tex_string(), a, b)
        return self.passo(src, dst, *mapas, **kw)

    def tmt(self, src, dst, rt=1.2):
        """Passo por TransformMatchingTex (src e dst montados por `mtp`, uma MathTex por parte): a cópia de `src` viaja para a vaga de `dst`."""
        print(f"[alg] {self._aid} tmt")
        tops = set(id(m) for m in self.mobjects)
        c = src.copy()
        self.add(c)
        self._fontes_extra = [src]
        self.play(TransformMatchingTex(c, dst, path_arc=3.0), run_time=max(0.8, rt))
        self._fontes_extra = []
        for m in list(self.mobjects):
            if id(m) not in tops and m is not dst:
                self.remove(m)
        self.add(dst)
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
            if _p2._n_gl(a) == _p2._n_gl(b):
                return ReplacementTransform(a, b, path_arc=arco, **kw)
            return _p2.troca_anim(a, b, rate=smooth)
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

    # ══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
    def t5(self):
        d = DiscoRef(self, th0=0.6)
        self.add(d.g)
        st = {"t": self.clk.get_value(), "w": 0.0, "th": 0.6, "fr": 1.0}
        wv, alv = ValueTracker(0.0), ValueTracker(0.0)        # ω e α MOSTRADOS (setas); o disco gira st["fr"] × ω
        ucam = ValueTracker(0.0)                              # 0: câmera de cima (= disco 2D); 1: câmera 3/4 (EL3, KD, CD)
        T = {k: ValueTracker(0.0) for k in ("esp", "eixo", "ow", "or", "ov", "opar", "ophi", "orp", "oO", "or2", "ov2", "oat", "oac", "omao", "fl")}
        T["esp"].set_value(0.02)
        z0 = ValueTracker(0.5)
        self.add(wv, alv, ucam, z0, *T.values())
        cfg = {"wbase": "O", "disco2d": d}

        def motor(m):
            t = self.clk.get_value()
            dt = t - st["t"]
            st["t"] = t
            st["w"] = wv.get_value()
            st["th"] += st["fr"] * st["w"] * dt
            if cfg["disco2d"] is not None:
                cfg["disco2d"].th.set_value(st["th"])
        mot = VGroup()
        mot.add_updater(motor)
        self.add(mot)

        def camd():
            u = ucam.get_value()
            el = 89.999 + (EL3 - 89.999) * smooth(u)
            return cam_disco(el, K=DR + (KD - DR) * u, c=P3(DC[0], DC[1] + (CD[1] - DC[1]) * u))

        def est_d(t):
            e = {"th": round(st["th"], 5), "w": round(st["w"], 4), "al": round(alv.get_value(), 4), "kw": KW, "kv": KV, "ka": KA3,
                 "z0": round(z0.get_value(), 4), "wbase": cfg["wbase"], "ref": 0.85, "oal": 0.0, "cam": camd()}
            for k, v in T.items():
                if k != "fl":
                    e[k] = round(v.get_value(), 3)
            return e
        camD = cam_disco(EL3, K=KD, c=CD)
        pj = lambda q: projeta3d(camD, q)
        LD = Lados()

        # ── T5-1: o disco ganha volume ──
        self.an("T5-1")
        self.secao("PARA ONDE APONTA UM GIRO?")
        self.play(wv.animate.set_value(0.35), run_time=0.8)
        f3 = Fundo3D(self, "disco", est_d, op=0.0)
        self.add(f3)
        self.gat("até agora todo giro acontecia")
        if not PEDIDOS3D:
            self.reg("troca_2d3d", th=st["th"], p3=d.p(3), c=d.C)
        self.play(f3.op.animate.set_value(1.0), FadeOut(d.g), run_time=0.6)
        self.remove(d.g)
        cfg["disco2d"] = None
        self.play(ucam.animate(rate_func=linear).set_value(1.0), T["esp"].animate.set_value(1.0), run_time=2.4)
        self.play(T["eixo"].animate.set_value(1.0), run_time=0.5)
        self.gat("nesse caso bastava um ângulo com sinal")
        self.selo("ATÉ AQUI", "UM EIXO FIXO · UM ÂNGULO COM SINAL")
        self.foco = self.s1
        self.gat("mas e quando o corpo pode girar")
        # D26: pião e Terra grandes (≥ 1,2), com o eixo tracejado e a seta ω⃗ violeta ao longo dele
        piao = aco(Polygon(P3(0, -0.75), P3(0.6, 0.1), P3(0.45, 0.38), P3(-0.45, 0.38), P3(-0.6, 0.1)), 1.6)
        pi_g = VGroup(DashedLine(P3(0, -1.0), P3(0, 0.75), dash_length=0.08).set_stroke(GEO, 2.5), piao,
                      Line(P3(0, 0.38), P3(0, 0.72)).set_stroke(GEO, 5), arrow(P3(0, 0.75), P3(0, 1.5), VEL, 7, z=9, tip=0.24))
        pi_g.rotate(0.3, about_point=ORIGIN).shift(P3(2.3, 0.45))
        ter = Circle(radius=0.75).set_fill("#163055", 1).set_stroke(GEO, 2.5)
        ter_g = VGroup(ter, Arc(radius=0.75, start_angle=-0.7, angle=1.5).set_stroke("#5C7E55", 9),
                       Arc(radius=0.75, start_angle=2.3, angle=0.9).set_stroke("#5C7E55", 9),
                       DashedLine(P3(0, -1.05), P3(0, 1.05), dash_length=0.08).set_stroke(GEO, 2.5), arrow(P3(0, 1.05), P3(0, 1.65), VEL, 7, z=9, tip=0.24))
        ter_g.rotate(-0.41, about_point=ORIGIN).shift(P3(5.3, 0.4))
        lab_i = VGroup(txt("PIÃO", 28).move_to(P3(2.3, -0.95)), txt("TERRA", 28).move_to(P3(5.3, -0.95)))
        self.play(FadeIn(pi_g), FadeIn(ter_g), FadeIn(lab_i), run_time=0.8)
        self.foco = lab_i
        self.gat("aí a gente precisa dizer também em torno de qual eixo")
        self.play(Rotate(pi_g, 0.45, about_point=pi_g[1].get_center()), Rotate(ter_g, -0.3, about_point=ter.get_center()), run_time=1.2)
        self.gat("dá para juntar tudo numa seta")
        q = VGroup(txt("UMA SETA?", 34, bold=True), txt("UM VETOR?", 34, bold=True)).arrange(DOWN, buff=0.2).move_to(P3(3.8, -2.2))
        self.play(FadeIn(q, shift=0.1 * UP), run_time=0.7)
        self.foco = q
        self.ate(0.99)

        # ── T5-2: os livros ──
        self.an("T5-2")
        I3 = np.eye(3)
        LV = {"L": I3.copy(), "R": I3.copy(), "G": I3.copy()}
        CEN = [[-0.2, 0.0, 0.0], [0.2, 0.0, 0.0]]
        SXL = 0.12
        kL, xL, yL = ValueTracker(13.5), ValueTracker(0.0), ValueTracker(-0.9)
        LT = {k: ValueTracker(0.0) for k in ("oe", "on", "oG", "fx", "fy", "sl")}
        LT["on"].set_value(1.0)
        lnv = ValueTracker(0.14)
        self.add(kL, xL, yL, lnv, *LT.values())
        camL = lambda: cam_obl(AZL, ELL, (0.0, 0.0, 0.0), K=round(kL.get_value(), 4), xc=round(xL.get_value(), 4), yc=round(yL.get_value(), 4), fov=16)

        def est_livros(t):
            o = LT["oe"].get_value()
            return {"c": CEN, "L": fl(LV["L"]), "R": fl(LV["R"]), "G": fl(LV["G"]), "oG": round(LT["oG"].get_value(), 3), "sx": SXL,
                    "oe": round(o, 3), "oz": round(o, 3), "on": round(LT["on"].get_value(), 3), "ln": round(lnv.get_value(), 4), "cam": camL()}
        f3b = Fundo3D(self, "livros", est_livros, op=0.0)
        self.add(f3b)
        self.play(f3.op.animate.set_value(0.0), f3b.op.animate.set_value(1.0), FadeOut(VGroup(pi_g, ter_g, lab_i, q)), run_time=0.6)
        self.sem_selo(rt=0.25)
        self.remove(f3, pi_g, ter_g, lab_i, q)
        mot.clear_updaters()

        def eixos_rot():
            g = VGroup()
            o = LT["oe"].get_value() * (1 - LT["sl"].get_value())      # os rótulos somem no meio do deslize (não atravessam a CALHA)
            if o < 0.01:
                return g
            cam = camL()
            for k, c in enumerate(CEN):
                pc = projeta3d(cam, c)
                for nome, dv, fk in (("x", (SXL, 0, 0), "fx" if k == 0 else "fy"), ("y", (0, 0, SXL), "fy" if k == 0 else "fx"), ("z", (0, -SXL, 0), None)):
                    pt = projeta3d(cam, (c[0] + dv[0], c[1] + dv[1], c[2] + dv[2]))
                    u = (pt - pc) / max(np.linalg.norm(pt - pc), 1e-6)
                    f_ = 1.0 + 0.35 * (LT[fk].get_value() if fk else 0.0)
                    m = fundo(mtex(nome, GEO_, 40)).scale(f_)
                    m.move_to(pt + u * ((0.2 if nome == "y" else 0.26) + 0.12 * (f_ - 1)))
                    g.add(opa(m, o))
            return g
        rx = vivo(eixos_rot)
        self.add(rx)

        def ordem(a, b):
            return VGroup(linha_m(lbl(r"90^\circ", ANG, 40), txt("EM", 24), lbl(a, GEO_, 40), txt(",", 24), buff=0.1),
                          linha_m(txt("DEPOIS", 24), lbl(r"90^\circ", ANG, 40), txt("EM", 24), lbl(b, GEO_, 40), buff=0.1)).arrange(DOWN, buff=0.12)
        t_esq, t_dir = ordem("x", "y"), ordem("y", "x")

        def pos_ordem(k, cam):
            return P3(projeta3d(cam, CEN[k])[0], 2.4 - t_esq.height / 2)      # bloco alto e compacto: o rótulo y do livro da direita não encosta no "DEPOIS 90°"
        t_esq.move_to(pos_ordem(0, camL()))
        t_dir.move_to(pos_ordem(1, camL()))
        self.gat("os dois eixos ficam parados no laboratório")
        self.play(LT["oe"].animate.set_value(1.0), run_time=0.7)
        self.selo("EIXOS FIXOS", "NO LABORATÓRIO")
        self.foco = self.s1
        u1, u2 = ValueTracker(0.0), ValueTracker(0.0)
        self.add(u1, u2)
        ang = {"g": 90.0}

        def gira_livros(m):
            a1, a2 = u1.get_value() * math.radians(ang["g"]), u2.get_value() * math.radians(ang["g"])
            LV["L"] = Ry(a2) @ Rx(a1)
            LV["R"] = Rx(a2) @ Ry(a1)
            LV["G"] = LV["R"]
            if not PEDIDOS3D and ang["g"] == 90.0:
                self.reg("livros", L=fl(LV["L"]), R=fl(LV["R"]), a1=a1, a2=a2)
        gl_ = VGroup()
        gl_.add_updater(gira_livros)
        self.add(gl_)
        self.gat("na esquerda primeiro a gente gira")
        self.play(FadeIn(t_esq), FadeIn(t_dir), run_time=0.5)
        self.foco = VGroup(t_esq, t_dir)
        self.play(u1.animate(rate_func=smooth).set_value(1.0), LT["fx"].animate(rate_func=there_and_back).set_value(1.0), run_time=1.6)
        self.gat("e depois noventa graus em torno deste outro")
        self.play(u2.animate(rate_func=smooth).set_value(1.0), LT["fy"].animate(rate_func=there_and_back).set_value(1.0), run_time=1.6)
        self.gat("olha como eles terminam")
        dif = lbl(r"\neq", WHITE_, 72).move_to(P3(-0.2, -2.0))
        cap = VGroup(txt("CAPA PARA BAIXO", 26, bold=True), txt("CAPA PARA A DIREITA", 26, bold=True))
        cap[0].move_to(P3(projeta3d(camL(), CEN[0])[0] - 0.35 - cap[0].width / 2, -3.0))      # ao lado da normal, que desce
        cap[1].move_to(P3(projeta3d(camL(), CEN[1])[0], -3.0))
        self.play(FadeIn(dif, scale=0.8), lnv.animate(rate_func=there_and_back).set_value(0.18), run_time=0.8)
        self.gat("a capa de um aponta para um lado")
        self.play(FadeIn(cap[0]), run_time=0.5)
        self.gat("a do outro para outro lado")
        self.play(FadeIn(cap[1]), run_time=0.5)
        self.foco = dif
        self.ate(0.99)

        # ── T5-3: vetores comutam; giros finitos não ──
        self.an("T5-3")
        cam2 = cam_obl(AZL, ELL, (0.0, 0.0, 0.0), K=10.0, xc=-3.55, yc=-0.6, fov=16)
        self.play(FadeOut(cap), FadeOut(dif), run_time=0.3)
        self.remove(cap, dif)
        self.play(kL.animate.set_value(10.0), xL.animate.set_value(-3.55), yL.animate.set_value(-0.6), LT["sl"].animate(rate_func=there_and_back).set_value(1.0),
                  t_esq.animate.move_to(pos_ordem(0, cam2)), t_dir.animate.move_to(pos_ordem(1, cam2)), run_time=1.2)
        self.sem_selo(rt=0.25)
        # D28: 3 m para leste e 4 m para norte nas duas ordens, setas GEO com ponta, o mesmo ponto final marcado
        o_, k_ = P3(1.35, -2.55), 0.5
        pA, pB, pAB = o_ + 3 * k_ * RIGHT, o_ + 4 * k_ * UP, o_ + 3 * k_ * RIGHT + 4 * k_ * UP
        L1 = arrow(o_, pA, GEO, 5, z=8, tip=0.2)
        L2 = arrow(pA, pAB, GEO, 5, z=8, tip=0.2)
        L3 = DashedVMobject(Line(o_, pB).set_stroke(GEO, 3), num_dashes=14).set_z_index(7)
        L3t = arrow(pB - 0.25 * UP, pB, GEO, 3, z=7, tip=0.16)
        L4 = DashedVMobject(Line(pB, pAB).set_stroke(GEO, 3), num_dashes=10).set_z_index(7)
        L4t = arrow(pAB - 0.25 * RIGHT, pAB, GEO, 3, z=7, tip=0.16)
        fim_ = Dot(pAB, radius=0.1, color=WHITE_).set_z_index(12)
        lA = lbl(r"\vec A", GEO_, 44).next_to((o_ + pA) / 2, DOWN, buff=0.14).shift(0.75 * LEFT)
        l3 = lbl(r"3\ \mathrm{m}", GEO_, 36).next_to((o_ + pA) / 2, DOWN, buff=0.18).shift(0.1 * RIGHT)
        lB = lbl(r"\vec B", GEO_, 44).next_to((pA + pAB) / 2, RIGHT, buff=0.18).shift(0.4 * UP)
        l4 = lbl(r"4\ \mathrm{m}", GEO_, 36).next_to((pA + pAB) / 2, RIGHT, buff=0.18).shift(0.4 * DOWN)
        rosa = VGroup(txt("N", 26, bold=True).move_to(P3(5.6, -0.55)), arrow(P3(5.6, -1.75), P3(5.6, -0.85), WHITE_, 4, tip=0.16))
        self.gat("andar três metros para leste")
        self.play(GrowArrow(L1), FadeIn(lA), FadeIn(l3), FadeIn(rosa), run_time=0.7)
        self.gat("e depois quatro para norte")
        self.play(GrowArrow(L2), FadeIn(lB), FadeIn(l4), run_time=0.7)
        self.gat("leva ao mesmo lugar")
        V1a, ia = M(r"\vec A", "+", r"\vec B", size=54, cores={0: GEO_, 2: GEO_})
        V1 = linha_m(txt("VETORES:", 28, bold=True), V1a, buff=0.25)
        self.pilha.poe(V1)
        V1b, ib = M("=", r"\vec B", "+", r"\vec A", size=54, cores={1: GEO_, 3: GEO_})
        x_eq = V1a.get_left()[0] - 0.62
        self.pilha.poe(V1b, dx=x_eq - self.pilha.x0)
        self.voa([(lA, mp(V1a, ia, [0])), (lB, mp(V1a, ia, [2]))], extra=[FadeIn(V1[0]), FadeIn(mp(V1a, ia, [1]))], rt=1.1, origem=False)
        self.gat("que fazer o contrário")
        self.play(Create(L3), Create(L3t), run_time=0.5)
        self.play(Create(L4), Create(L4t), FadeIn(fim_, scale=0.6), run_time=0.5)
        # GM: os dois termos trocam de lugar (A⃗ vai para a direita, B⃗ para a esquerda) e o "=" entra antes
        self.pg(V1a, V1b, (J(ia, 0), J(ib, 3)), (J(ia, 1), J(ib, 2)), (J(ia, 2), J(ib, 1)), ([], J(ib, 0)), rt=1.2, origem=False)
        self.foco = V1b
        self.gat("até dá para descrever um giro de noventa graus com uma seta")
        c0 = projeta3d(cam2, CEN[0])
        sg = arrow(c0, projeta3d(cam2, (CEN[0][0] + 0.09, 0, 0)), ANG, 9, z=13, tip=0.26)
        l90 = lbl(r"90^\circ", ANG, 40).next_to(sg, UP, buff=0.32).shift(0.25 * LEFT)
        self.play(GrowArrow(sg), FadeIn(l90), run_time=0.8)
        self.foco = sg
        self.gat("mas juntar dois giros não é somar essas setas")
        self.play(FadeOut(VGroup(L1, L2, L3, L3t, L4, L4t, fim_, lA, l3, lB, l4, rosa, sg, l90)), run_time=0.4)
        self.remove(L1, L2, L3, L3t, L4, L4t, fim_, lA, l3, lB, l4, rosa, sg, l90)
        V2a = linha_m(txt("GIROS FINITOS:", 28, bold=True))
        V2b = linha_m(txt("(A, DEPOIS B)", 28), lbl(r"\neq", WHITE_, 52), txt("(B, DEPOIS A)", 28), buff=0.2)
        self.pilha.poe(V2a)
        self.pilha.poe(V2b)
        self.play(FadeIn(V2a), FadeIn(V2b), run_time=0.9)          # §5.9: o rótulo nunca fica órfão: a continuação entra junto
        self.gat("o resultado depende da ordem")
        self.foco = V2b
        self.gat("então giros finitos não se somam como vetores")
        self.selo("ATENÇÃO", "GIRO FINITO NÃO SE SOMA COMO VETOR")
        self.foco = self.s1
        self.ate(0.99)

        # ── T5-4: giros pequenos ──
        self.an("T5-4")
        self.sem_selo(rt=0.25)
        self.pilha.limpa(rt=0.3, anims=[FadeOut(t_esq), FadeOut(t_dir)])
        self.remove(t_esq, t_dir)
        med_t = txt("DIFERENÇA ENTRE AS ORDENS", 26, bold=True).move_to(P3(-3.55, -2.45))
        cx_ = {"v": 0.0}

        def medidor():
            return num_mob(fmt_g(cx_["v"]) + "°", ANG, 54).move_to(P3(-3.55, -3.12))
        mv = vivo(medidor)
        self.play(FadeIn(med_t), FadeIn(mv), run_time=0.4)

        def arco_n():
            """D29: o ângulo entre a normal do livro da esquerda e a do fantasma (ordem da direita), em âmbar: o traço é grosso (o ângulo real é
            pequeno demais para ver) e o valor real é o do medidor."""
            g = VGroup()
            o = LT["oG"].get_value()
            if o < 0.05:
                return g
            cam = camL()
            n_l = LV["L"] @ np.array([0, 0, 1.0])
            n_g = LV["G"] @ np.array([0, 0, 1.0])
            mund = lambda v: np.array([v[0], -v[2], v[1]])
            b = np.array(CEN[0]) + mund(n_l) * 0.02
            pb = projeta3d(cam, b)
            ln_ = lnv.get_value()
            p1, p2 = projeta3d(cam, b + mund(n_l) * ln_ * 0.8), projeta3d(cam, b + mund(n_g) * ln_ * 0.8)
            a1, a2 = math.atan2(*(p1 - pb)[1::-1]), math.atan2(*(p2 - pb)[1::-1])
            da = (a2 - a1 + PI) % (2 * PI) - PI
            r_ = float(np.linalg.norm(p1 - pb))
            sg_ = 1.0 if da >= 0 else -1.0                           # traço exagerado (×8, entre 0,3 e 0,8 rad) no sentido da normal do fantasma;
            da = sg_ * min(0.8, max(0.3, 8 * abs(da)))               # o valor real é o do medidor
            g.add(opa(arco(pb, r_, a1, a1 + da, ANG, 9, 1.0, z=13), o))
            return g
        an_ = vivo(arco_n)
        self.add(an_)
        rows = {}
        for g_ in (10.0, 5.0, 1.0):                                  # tabela 10° · 5° · 1°: as vagas existem desde já, preenchidas na ordem da fala
            R_, ir_ = M(f"{int(g_)}" + r"^\circ", r"\rightarrow", fmt_g(dif_g(g_)).replace(",", "{,}") + r"^\circ", size=48, cores={0: ANG, 2: ANG})
            self.pilha.poe(R_)
            rows[g_] = (R_, ir_)

        def rodada(g_):
            self.play(u1.animate.set_value(0.0), u2.animate.set_value(0.0), LT["oG"].animate.set_value(0.0), run_time=0.4)
            ang["g"] = g_
            self.play(u1.animate(rate_func=smooth).set_value(1.0), run_time=0.7)
            self.play(u2.animate(rate_func=smooth).set_value(1.0), LT["oG"].animate.set_value(1.0), run_time=0.7)
            cx_["v"] = ang_rot(LV["L"] @ LV["R"].T)
            if not PEDIDOS3D:
                self.reg("livros_peq", g=g_, dif=cx_["v"], dif_g=dif_g(g_))
            R_, ir_ = rows[g_]
            self.voa([(medidor(), mp(R_, ir_, [2]))], extra=[FadeIn(mp(R_, ir_, [0, 1]))], rt=1.0, origem=False)
            self.foco = R_
        self.gat("com dez graus")
        rodada(10.0)
        self.gat("com um grau quase some")
        rodada(1.0)
        nota_ = linha_m(txt("DIFERENÇA", 28, bold=True), lbl(r"\propto", WHITE_, 46), lbl(r"\theta_1\cdot\theta_2", ANG, 46), buff=0.18)
        self.pilha.poe(nota_)
        self.gat("com o produto dos dois ângulos")
        self.play(FadeIn(nota_), run_time=0.7)
        self.gat("se os dois giros caem pela metade")
        rodada(5.0)
        R10, R5 = rows[10.0][0], rows[5.0][0]
        q4 = lbl(r"\div 4", WHITE_, 46).move_to(P3(max(R10.get_right()[0], R5.get_right()[0]) + 0.75, (R10.get_y() + R5.get_y()) / 2))
        cv4 = CurvedArrow(R10.get_right() + P3(0.12, 0), R5.get_right() + P3(0.12, 0), angle=-PI / 2, color=WHITE_, stroke_width=3, tip_length=0.14)
        self.gat("a diferença cai para um quarto")
        self.play(Create(cv4), FadeIn(q4), run_time=0.8)
        self.foco = q4
        G1a = mtp(r"d\vec\theta_1", "+", r"d\vec\theta_2", size=54, cores={0: ANG, 2: ANG})
        G1b = mtp("=", r"d\vec\theta_2", "+", r"d\vec\theta_1", size=54, cores={1: ANG, 3: ANG})
        self.pilha.poe(G1a, dx=0.62)
        self.pilha.poe(G1b, dx=0.0)
        self.gat("para giros infinitesimais")
        self.play(FadeIn(G1a), run_time=0.8)
        self.gat("e os giros pequenininhos se somam")
        self.tmt(G1a, G1b, rt=1.8)                                   # §7: os dois termos trocam de lugar pela correspondência de TransformMatchingTex
        self.foco = G1b
        self.ate(0.99)

        # ── T5-5: ω⃗ e a mão direita ──
        self.an("T5-5")
        gl_.clear_updaters()
        self.remove(gl_)
        for k in ("esp", "eixo"):
            T[k].set_value(1.0)
        ucam.set_value(1.0)
        cfg["wbase"] = 0.02
        wv.set_value(W5)
        st["fr"], st["w"] = FR, W5
        st["th"] = TH6 - FR * W5 * self.resta()                     # P chega ao início do T5-6 em TH6
        st["t"] = self.clk.get_value()
        mot.add_updater(motor)
        f3 = Fundo3D(self, "disco", est_d, op=0.0)
        self.add(f3)
        self.pilha.limpa(rt=1.0, anims=[FadeOut(med_t), FadeOut(mv), FadeOut(rx), FadeOut(an_), FadeOut(cv4), FadeOut(q4),
                                        f3b.op.animate.set_value(0.0), f3.op.animate.set_value(1.0)])
        self.remove(f3b, mv, rx, an_, med_t, cv4, q4)

        def lab5():
            g = {}
            o = T["ow"].get_value()
            if o > 0.01:
                pt = pj((0, 0, 0.02 + KW * st["w"]))
                f_ = 1 + 0.3 * T["fl"].get_value()
                g["w"] = opa(rot(r"\vec\omega", VEL, 46).scale(f_).move_to(pt + P3(-0.5, 0.12)), o)    # S12: do lado oposto ao da mão
            return g
        rw = vivo(lambda: VGroup(*lab5().values()))
        self.add(rw)
        self.gat("a velocidade angular pode ser")
        self.play(T["ow"].animate.set_value(1.0), run_time=0.8)
        W1, iw1 = M(r"\vec\omega", "=", r"\frac{d\vec\theta}{dt}", size=60, cores={0: VEL})
        pinta(W1, iw1[2][1:3], ANG)
        self.pilha.poe(W1)
        self.gat("ela é um giro infinitesimal")
        self.voa([(lab5()["w"], mp(W1, iw1, [0]))], extra=[FadeIn(mp(W1, iw1, [1, 2]))], rt=1.3, origem=False)
        self.gat("a seta fica em cima do eixo")
        self.play(T["fl"].animate(rate_func=there_and_back).set_value(1.0), run_time=0.8)
        W2, iw2 = M(r"|\vec\omega|", "=", r"|\omega|", size=56, cores={0: VEL, 2: VEL})
        self.pilha.poe(W2)
        self.gat("com tamanho igual ao tamanho")
        self.pg(W1, W2, (J(iw1, 0), iw2[0][1:3]), ([], [iw2[0][0], iw2[0][3]]), (J(iw1, 1), J(iw2, 1)), (J(iw1, 2), J(iw2, 2)), rt=1.2, origem=False)
        W3 = linha_m(lbl(r"\omega", VEL, 46), txt("(COM SINAL) =", 26), buff=0.14)
        W3b = linha_m(txt("COMPONENTE DE", 26), lbl(r"\vec\omega", VEL, 46), txt("NO EIXO", 26), buff=0.14)
        self.pilha.poe(W3)
        self.pilha.poe(W3b)
        self.gat("aquele sinal de antes")
        self.play(FadeIn(W3), run_time=0.7)
        self.gat("vira o sentido da seta")
        self.play(FadeIn(W3b), run_time=0.8)
        self.foco = W3b
        self.gat("e o sentido vem da regra da mão direita")
        lm = fundo(txt("MÃO DIREITA", 28, bold=True)).move_to(pj((0.3, 0, 0.55)) + P3(2.0, 0.05))
        self.play(T["omao"].animate.set_value(0.85), FadeIn(lm), run_time=1.0)
        self.foco = lm
        self.gat("e o polegar aponta o vetor")
        self.play(T["fl"].animate(rate_func=there_and_back).set_value(1.0), run_time=0.8)
        self.ate(0.99)

        # ── T5-6: v⃗ = ω⃗ × r⃗ ──
        self.an("T5-6")
        cfg["wbase"] = "O"
        z0.set_value(0.02)                                           # ω⃗ continua no disco; sobe pelo eixo até O quando O aparece
        self.remove(rw)
        circ_o = ValueTracker(0.0)
        self.add(circ_o)

        def lab6(oO2=None):
            """Rótulos do T5-6/T5-7/T5-8 presos aos pontos projetados, cada um no lado livre (Lados)."""
            th, w = st["th"], st["w"]
            P = np.array([math.cos(th), math.sin(th), 0.01])
            zz = z0.get_value() if cfg["wbase"] == "O" else 0.0
            O = np.array([0, 0, zz])
            wb = zz if cfg["wbase"] == "O" else 0.02
            r = P - O
            v = np.cross([0, 0, w], r)
            al = alv.get_value()
            at = np.cross([0, 0, al], P)
            ac = np.cross([0, 0, w], np.cross([0, 0, w], P))
            pO, pP, pC = pj(O), pj(P), pj((0, 0, 0.01))
            pW1 = pj((0, 0, wb + KW * w))
            segs = [(pj((0, 0, -0.05)), pj((0, 0, 1.25))), (pC, pP)]
            pts = []
            ops = {k: T[k].get_value() for k in T}
            if ops["ow"] > 0.01:
                segs.append((pj((0, 0, wb)), pW1))
            if ops["or"] > 0.01:
                segs.append((pO, pP))
            pv = pj(P + KV * v)
            if ops["ov"] > 0.01:
                segs.append((pP, pv))
            if ops["opar"] > 0.01:
                A2 = pj(np.array([0, 0, wb + KW * w]) + r)
                segs += [(pW1, A2), (A2, pP)]
            phi = math.acos(max(-1.0, min(1.0, r[2] / max(np.linalg.norm(r), 1e-9))))
            hu = np.array([math.cos(th), math.sin(th), 0])
            arc_pts = [pj(O + 0.32 * (np.array([0, 0, 1]) * math.cos(a) + hu * math.sin(a))) for a in np.linspace(0, phi, 7)]
            if ops["ophi"] > 0.01:
                segs += list(zip(arc_pts[:-1], arc_pts[1:]))
            P2 = -P + np.array([0, 0, 0.02])
            r2 = P2 - O
            v2 = np.cross([0, 0, w], r2)
            if ops["or2"] > 0.01:
                segs.append((pO, pj(P2)))
            if ops["ov2"] > 0.01:
                segs.append((pj(P2), pj(P2 + KV * v2)))
            pat, pac = pj(P + KA3 * at), pj(P + KA3 * ac)
            if ops["oat"] > 0.01:
                segs.append((pP, pat))
            if ops["oac"] > 0.01:
                segs.append((pP, pac))
            pa0, pa1 = pj((0.12, 0, 0.62 - 0.5 * KW * al)), pj((0.12, 0, 0.62 + 0.5 * KW * al))
            if cfg.get("oal", 0) > 0.01 and abs(al) > 1e-3:
                segs.append((pa0, pa1))
            g = {}
            if ops["ow"] > 0.01:
                g["w"] = LD.poe("w", rot(r"\vec\omega", VEL, 46), pW1, segs, pts, d=0.12, pref=(3, 4))
            if ops["oO"] > 0.01:
                g["O"] = LD.poe("O", rot("O", WHITE_, 42), pO, segs, pts, d=0.1)
            if ops["ophi"] > 0.01:
                g["phi"] = LD.poe("phi", rot(r"\varphi", ANG, 44), arc_pts[3], segs, pts, d=0.08)
            if ops["or"] > 0.01:
                g["r"] = LD.poe("r", rot(r"\vec r", GEO_, 46), pO + 0.55 * (pP - pO), segs, pts, d=0.24)
            if ops["orp"] > 0.01:
                f_ = 1 + 0.35 * T["fl"].get_value()
                g["rp"] = LD.poe("rp", rot(r"r_\perp", GEO_, 44).scale(f_), pC + 0.5 * (pP - pC), segs, pts, d=0.08)
            if ops["ov"] > 0.01:
                g["v"] = LD.poe("v", rot(r"\vec v", VEL, 46), pv, segs, pts, d=0.1)
            if ops["oat"] > 0.01 and np.linalg.norm(at) > 1e-3:
                g["at"] = LD.poe("at", rot("a_t", ACC, 44), pat, segs, pts, d=0.1)
            if ops["oac"] > 0.01:
                g["ac"] = LD.poe("ac", rot("a_c", ACC, 44), pac, segs, pts, d=0.1)
            if cfg.get("oal", 0) > 0.01 and abs(al) > 1e-3:
                g["al"] = LD.poe("al", rot(r"\vec\alpha", ACC, 46), (pa0 + pa1) / 2 + P3(0.1, 0), segs, pts, d=0.12, pref=(0, 1, 7))
            for k, m in g.items():
                o = {"w": ops["ow"], "O": ops["oO"], "phi": ops["ophi"], "r": ops["or"], "rp": ops["orp"], "v": ops["ov"], "at": ops["oat"],
                     "ac": ops["oac"], "al": cfg.get("oal", 0)}[k]
                opa(m, o)
            if not PEDIDOS3D and (ops["oat"] > 0.5 or ops["oac"] > 0.5):      # §6: α⃗ × r⃗ e ω⃗ × (ω⃗ × r⃗) para a auditoria do produto vetorial
                self.reg("a3d", at=at.tolist(), ac=ac.tolist(), al=al, w=w, a=(at + ac).tolist(), r=P.tolist())
            cfg["anc"] = {"O": pO, "r": pO + 0.55 * (pP - pO)}
            if not PEDIDOS3D and ops["ov"] > 0.5:
                self.reg("pv", v=v.tolist(), r=r.tolist(), z0=zz, th=th, w=w, vtopo=pv.tolist())
            return g

        def desenho6():
            g = VGroup()
            L_ = lab6()
            for k_, m in L_.items():                                # §5.12: rótulo sem caixa; O e r⃗ levam uma linha-guia curta até a âncora
                g.add(m)
                a_ = cfg.get("anc", {}).get(k_)
                if a_ is not None:
                    c_, hw, hh = m.get_center(), m.width / 2 + 0.04, m.height / 2 + 0.04
                    q_ = c_[:2] + np.clip(np.asarray(a_)[:2] - c_[:2], [-hw, -hh], [hw, hh])
                    if np.linalg.norm(q_ - np.asarray(a_)[:2]) > 0.12:
                        o_ = max([x.get_fill_opacity() for x in m.family_members_with_points()] or [0])
                        g.add(opa(Line(P3(a_[0], a_[1]), P3(q_[0], q_[1])).set_stroke(GEO, 2.5).set_z_index(11), o_))
            if cfg.get("oal", 0) > 0.01 and abs(alv.get_value()) > 1e-3:          # α⃗ (2D) ao lado do eixo, centrado a meia altura de ω⃗: nunca entra no disco
                al = alv.get_value()
                a0, a1 = pj((0.12, 0, 0.62 - 0.5 * KW * al)), pj((0.12, 0, 0.62 + 0.5 * KW * al))
                g.add(opa(seta(a0, a1, ACC, 9, tip=0.22, z=11), cfg["oal"]))
            co = circ_o.get_value()
            if co > 0.01:                                            # o círculo de P (tangente ao círculo do ponto)
                q = projeta3d_n(camD, np.array([[math.cos(a), math.sin(a), 0.012] for a in np.linspace(0, 2 * PI, 73)]))
                c_ = VMobject().set_points_as_corners(q)
                g.add(opa(DashedVMobject(c_, num_dashes=48).set_stroke(GEO, 3).set_z_index(6), co))
            return g
        r6 = vivo(desenho6)
        self.add(r6)
        self.pilha.limpa(rt=0.4, anims=[T["omao"].animate.set_value(0.0), FadeOut(lm)])
        self.remove(lm)
        self.gat("a velocidade de cada ponto")
        self.play(T["oO"].animate.set_value(1.0), T["or"].animate.set_value(1.0), z0.animate.set_value(0.5), run_time=0.9)
        X1, ix1 = M(r"\vec v", "=", r"\vec\omega", r"\times", r"\vec r", size=60, cores={0: VEL, 2: VEL, 4: GEO_})
        self.pilha.poe(X1)
        self.gat("ganha uma fórmula completa")
        L6 = lab6()
        self.voa([(L6["w"], mp(X1, ix1, [2])), (L6["r"], mp(X1, ix1, [4]))], extra=[FadeIn(mp(X1, ix1, [0, 1, 3]))], rt=1.3, origem=False)
        self.gat("dá um terceiro")
        self.play(T["ov"].animate.set_value(1.0), run_time=0.8)
        self.gat("com tamanho igual à área desse paralelogramo")
        self.play(T["opar"].animate.set_value(1.0), run_time=0.8)
        X2, ix2 = M(r"|\vec v|", "=", r"\omega", "r", r"\operatorname{sen}", r"\varphi", size=60, cores={0: VEL, 2: VEL, 3: GEO_, 5: ANG})
        self.pilha.poe(X2)
        self.gat("vezes o seno do ângulo entre eles")
        self.play(T["ophi"].animate.set_value(1.0), run_time=0.6)
        self.voa([(lab6()["phi"], mp(X2, ix2, [5]))], extra=[FadeIn(mp(X2, ix2, [0, 1, 2, 3, 4]))], rt=1.3, origem=False)
        X3, ix3 = M("=", r"\omega", r"r_\perp", size=60, cores={1: VEL, 2: GEO_})
        self.pilha.poe(X3)
        self.gat("é exatamente a distância do ponto ao eixo")
        self.play(T["orp"].animate.set_value(1.0), run_time=0.6)
        # GM r sen φ → r_⊥ (o r_⊥ do desenho pisca junto)
        self.pg(X2, X3, (J(ix2, 0), []), (J(ix2, 1), J(ix3, 0)), (J(ix2, 2), J(ix3, 1)), (J(ix2, 3, 4, 5), J(ix3, 2)), rt=1.3, origem=False,
                extra=[T["fl"].animate(rate_func=there_and_back).set_value(1.0)])
        self.foco = X3
        self.gat("por isso o vetor posição pode começar em qualquer ponto do eixo")
        self.play(z0.animate(rate_func=smooth).set_value(0.6), run_time=2.4)
        self.play(z0.animate(rate_func=smooth).set_value(0.1), run_time=3.0)
        self.gat("o tamanho volta a ser")
        self.play(z0.animate(rate_func=smooth).set_value(0.5), run_time=1.6)
        self.gat("tangente ao círculo do ponto")
        self.play(circ_o.animate.set_value(1.0), run_time=0.6)
        self.ate(0.99)

        # ── T5-7: os dois pontos opostos ──
        self.an("T5-7")
        self.play(T["opar"].animate.set_value(0.0), T["ophi"].animate.set_value(0.0), T["orp"].animate.set_value(0.0), circ_o.animate.set_value(0.0),
                  run_time=0.4)
        self.gat("o produto vetorial resolve sozinho")
        self.play(T["or2"].animate.set_value(1.0), run_time=0.7)
        self.gat("e as velocidades saem opostas")
        self.play(T["ov2"].animate.set_value(1.0), run_time=0.7)
        if not PEDIDOS3D:
            th = st["th"]
            self.reg("opostos3d", v1=np.cross([0, 0, st["w"]], [math.cos(th), math.sin(th), 0]).tolist(),
                     v2=np.cross([0, 0, st["w"]], [-math.cos(th), -math.sin(th), 0]).tolist())
        self.ate(0.99)

        # ── T5-8: α⃗ e a⃗ ──
        self.an("T5-8")
        # O desce pelo eixo até o centro do disco (ω⃗ e r⃗ vão junto: r⃗ fica radial); P segue girando e passa pela frente (v⃗ deitada na tela)
        self.pilha.limpa(rt=0.8, anims=[*[T[k].animate.set_value(0.0) for k in ("or2", "ov2", "oO")], z0.animate.set_value(0.02)])
        Y1, iy1 = M(r"\vec\alpha", "=", r"\frac{d\vec\omega}{dt}", size=56, cores={0: ACC})
        pinta(Y1, iy1[2][1:3], VEL)
        self.pilha.poe(Y1)
        self.gat("a aceleração angular também vira vetor")
        self.voa([(lab6()["w"], gl(Y1, iy1[2][1:3]))], extra=[FadeIn(mp(Y1, iy1, [0, 1])), FadeIn(gl(Y1, [iy1[2][0]] + iy1[2][3:]))], rt=1.3, origem=False)
        self.gat("com eixo fixo ela fica em cima do eixo")
        cfg["oal"] = 0.0
        oal = ValueTracker(0.0)
        self.add(oal)
        ual = VGroup()
        ual.add_updater(lambda m: cfg.__setitem__("oal", oal.get_value()))
        self.add(ual)
        alv.set_value(AL5)
        self.play(oal.animate.set_value(1.0), run_time=0.7)
        self.play(wv.animate(rate_func=linear).set_value(0.72), run_time=self.ate_t("quando o giro acelera", 0.6))
        self.gat("quando o giro acelera")
        self.selo("ACELERA", "", rt=0.4, anims=[wv.animate(rate_func=linear).set_value(0.75)])
        self.gat("no sentido oposto quando freia")
        alv.set_value(-AL5)
        self.selo("FREIA", "", rt=0.4)
        self.play(wv.animate(rate_func=linear).set_value(W5), run_time=1.4)
        self.gat("e agora dá para juntar tudo numa linha")
        alv.set_value(AL5)
        self.selo("ACELERA", "", rt=0.4)
        t_rest = self.resta()
        acel_fim = {"t0": self.clk.get_value(), "d": t_rest}
        wacel = VGroup()
        wacel.add_updater(lambda m: wv.set_value(W5 + 0.2 * min(1.0, (self.clk.get_value() - acel_fim["t0"]) / max(acel_fim["d"], 1.0))))
        self.add(wacel)
        A1, ia1 = M(r"\vec a", "=", r"\frac{d\vec v}{dt}", size=52, cores={0: ACC})
        pinta(A1, ia1[2][1:3], VEL)
        self.pilha.poe(A1)
        self.voa([(lab6()["v"], gl(A1, ia1[2][1:3]))], extra=[FadeIn(mp(A1, ia1, [0, 1])), FadeIn(gl(A1, [ia1[2][0]] + ia1[2][3:]))], rt=1.2, origem=False)
        A2, ia2 = M("=", r"\frac{d}{dt}", "(", r"\vec\omega", r"\times", r"\vec r", ")", size=52, cores={3: VEL, 5: GEO_})
        self.pilha.poe(A2)
        self.gat("derivando a velocidade do ponto")
        f1 = ia1[2]
        self.pg(A1, A2, (J(ia1, 0), []), (J(ia1, 1), J(ia2, 0)), ([f1[0]], [ia2[1][0]]), (f1[1:3], J(ia2, 2, 3, 4, 5, 6)), ([f1[3]], [ia2[1][1]]),
                (f1[4:], ia2[1][2:]), rt=1.2, origem=False)
        A3, ia3 = M("=", r"\vec\alpha", r"\times", r"\vec r", "+", r"\vec\omega", r"\times", r"\vec v", size=52, cores={1: ACC, 3: GEO_, 5: VEL, 7: VEL})
        self.pilha.poe(A3)
        self.gat("aparecem dois termos")
        # GM regra do produto: o d/dt vira α⃗ no primeiro fator; ω⃗ passa para o segundo termo, onde o r⃗ derivado é v⃗
        self.passo_arco(A2, A3, (J(ia2, 0), J(ia3, 0)), (J(ia2, 1), J(ia3, 1)), (J(ia2, 2), []), (J(ia2, 3), J(ia3, 5)), (J(ia2, 4), J(ia3, 2)),
                (J(ia2, 5), J(ia3, 3)), (J(ia2, 6), []), ([], J(ia3, 4)), ([], J(ia3, 6)), ([], J(ia3, 7)), rt=2.2)
        self.foco = A3
        self.gat("o primeiro é a aceleração angular")
        self.foco = A3
        self.gat("é a aceleração tangencial")
        self.play(T["ov"].animate.set_value(0.0), T["oat"].animate.set_value(1.0), *self.troca_marcador("FORA DE ESCALA", "dir", y=-2.95), run_time=0.7)
        A4, ia4 = M("=", r"\vec\alpha", r"\times", r"\vec r", "+", r"\vec\omega", r"\times", r"(\vec\omega\times\vec r)", size=52,
                    cores={1: ACC, 3: GEO_, 5: VEL})
        pinta(A4, ia4[7][1:3], VEL)
        pinta(A4, ia4[7][4:6], GEO_)
        A4f, ia4f = M(r"\vec a", "=", r"\vec\alpha", r"\times", r"\vec r", "+", r"\vec\omega", r"\times", r"(\vec\omega\times\vec r)", size=52,
                      cores={0: ACC, 2: ACC, 4: GEO_, 6: VEL})
        pinta(A4f, ia4f[8][1:3], VEL)
        pinta(A4f, ia4f[8][4:6], GEO_)
        A4._lhs = lambda: A4f
        self.pilha.poe(A4)
        self.gat("o segundo é a velocidade angular")
        self.foco = A3
        self.gat("com a velocidade do próprio ponto")
        # GM v⃗ → (ω⃗ × r⃗)
        self.pg(A3, A4, *[(J(ia3, k), J(ia4, k)) for k in range(8)], rt=1.2, origem=False)
        self.foco = A4
        self.gat("ele aponta para o eixo")
        self.play(T["oac"].animate.set_value(1.0), T["or"].animate.set_value(0.0), run_time=0.7)      # r⃗ sai: a_c corre sobre ele
        self.gat("e tem tamanho velocidade angular")
        A4f = self.pilha.so(A4, rt=0.6)[0]
        br1 = Brace(mp(A4f, ia4f, [2, 3, 4]), DOWN, buff=0.24, color=WHITE_)
        br2 = Brace(mp(A4f, ia4f, [6, 7, 8]), DOWN, buff=0.24, color=WHITE_)
        for br in (br1, br2):                                       # as duas chaves na mesma altura, abaixo dos parênteses da linha
            br.shift(UP * ((A4f.get_bottom()[1] - 0.24) - br.get_top()[1]))
        tb1 = txt("TANGENCIAL", 24, bold=True).next_to(br1, DOWN, buff=0.16)
        tb2 = txt("CENTRÍPETA", 24, bold=True).next_to(br2, DOWN, buff=0.16)
        self.play(GrowFromCenter(br1), GrowFromCenter(br2), Write(tb1), Write(tb2), run_time=0.8)
        Z1, iz1 = M("a_t", "=", r"\alpha", r"r_\perp", size=50, cores={0: ACC, 2: ACC, 3: GEO_})
        Z2m, iz2 = M(r"\vec a_c", "=", r"-\omega^2", r"\vec r_\perp", size=50, cores={0: ACC, 2: VEL, 3: GEO_})
        Z2 = linha_m(Z2m, txt("PARA O EIXO", 26), buff=0.22)
        bb = self.pilha.buff
        self.pilha.buff = (A4f.get_bottom()[1] - min(tb1.get_bottom()[1], tb2.get_bottom()[1])) + 0.3
        self.pilha.poe(Z1)
        self.pilha.buff = bb
        self.pilha.poe(Z2)
        self.voa([(lab6()["at"], mp(Z1, iz1, [0]))], extra=[FadeIn(mp(Z1, iz1, [1, 2, 3]))], rt=1.0, origem=False)
        self.gat("vezes a distância ao eixo")
        self.voa([(lab6()["ac"], mp(Z2m, iz2, [0]))], extra=[FadeIn(mp(Z2m, iz2, [1, 2, 3])), FadeIn(Z2[1])], rt=1.1, origem=False)
        self.foco = Z2
        self.gat("as duas acelerações do disco estavam escondidas")
        self.play(self.ind(A4f, ia4f, [2, 3, 4], f=1.0), self.ind(A4f, ia4f, [6, 7, 8], f=1.0), run_time=0.9)
        self.gat("e quando o próprio eixo muda de direção")
        self.play(*self.troca_marcador(None), run_time=0.4)
        self.foco = A4f
        self.ate(0.99)
        mot.clear_updaters()
        wacel.clear_updaters()

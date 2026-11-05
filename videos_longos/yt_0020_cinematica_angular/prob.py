"""yt_0019 (copiado do yt_0018) — base dos problemas (handoff v1 §2.3, §3): esqueleto fixo de cada problema e desenhos comuns.

Layout: ESQUEMA à esquerda (x de −7,4 a −0,2; ~45%), CONTA à direita (alinhada em XC0). Faixa de selos acima da CONTA: linha 1 (y = 2,85)
`O QUE ESTE PEDE` → `CONFERE` → `DICA`; linha 2 (y = 2,25) `HIPÓTESES` (G21: entram com a fala, saem na primeira conta). Checklist das três
perguntas (A4) pequeno no canto inferior direito, aceso na pergunta que decide. Selo de referencial (G20) no alto do ESQUEMA.
Auditorias novas (AUDITORIA=1): texto sobre a trajetória dos próximos 2 s (`self._futuros`), REFERENCIAL (cada seta de velocidade com o
selo ativo no quadro) e o registro por quadro para GAFANHOTO × FÍSICA / ROJÃO / CUBO (qa_overlay_<lote>.json, lido por qa.py).
"""
from kit import *  # noqa: F401,F403

XC0 = 0.95                    # borda esquerda da CONTA
ESQ_C = P3(-3.8, -0.35)       # centro do ESQUEMA
ESQ_X = (-7.4, -0.2)
Y_SELO, Y_HIP = 2.85, 2.25
ACO3 = ["#9AA6B8", "#7A8696", "#3A4252"]


def na_conta(m, y, x0=XC0):
    return m.move_to(P3(x0 + m.width / 2, y))


def aco(m, borda=2.0, op=1.0):
    """Corpo 2D em aço com a luz B (gradiente vertical + recorte BLUE_L): marcado para a auditoria G15."""
    m.set_fill(ACO3, op).set_sheen_direction(UP).set_stroke("#7FB2FF", borda, opacity=0.75 * op)
    m._degrade = "aco"
    return m


def cota(xa, xb, y, rotulo, cor=GEO, lado=DOWN, buff=0.14):
    g = VGroup(Line(P3(xa, y), P3(xb, y)).set_stroke(cor, 2.2),
               Line(P3(xa, y - 0.11), P3(xa, y + 0.11)).set_stroke(cor, 2.2), Line(P3(xb, y - 0.11), P3(xb, y + 0.11)).set_stroke(cor, 2.2))
    lab = rotulo.next_to(P3((xa + xb) / 2, y), lado, buff=buff)
    return VGroup(g, lab)


def cota_v(x, ya, yb, rotulo=None, cor=GEO, lado=RIGHT):
    g = VGroup(Line(P3(x, ya), P3(x, yb)).set_stroke(cor, 2.2), Line(P3(x - 0.1, ya), P3(x + 0.1, ya)).set_stroke(cor, 2.2),
               Line(P3(x - 0.1, yb), P3(x + 0.1, yb)).set_stroke(cor, 2.2))
    if rotulo is not None:
        g = VGroup(g, rotulo.next_to(P3(x, (ya + yb) / 2), lado, buff=0.14))
    return g


def tracejado(a, b, cor=WHITE_, w=2.2, op=0.7, dash=0.09):
    return DashedLine(np.asarray(a, float), np.asarray(b, float), dash_length=dash, dashed_ratio=0.55).set_stroke(cor, w, opacity=op)


def fantasma_circ(c, r, cor=None):
    """G22: massa negativa = contorno tracejado magenta-escuro por cima do corpo inteiro (nunca furo pintado)."""
    cor = cor or escuro(MAG, 0.45)
    return DashedVMobject(Circle(radius=r).move_to(c).set_stroke(cor, 3.6), num_dashes=max(18, int(28 * r)), dashed_ratio=0.6).set_z_index(9)


def M(*partes, size=48, cores=None):
    """MathTex de string única (cor por token, G12) + índices das partes: atalho de eqp."""
    return eqp(*partes, size=size, cores=cores)


def tx(s, size=T_MAIN, color=WHITE_, bold=False):
    """txt() que aceita '⊕' no meio (a fonte não tem o glifo): o ⊕ vira o marcador em degradê, do tamanho da letra."""
    if not any(c in s for c in "⊕→∝"):
        return txt(s, size, color, bold=bold)
    itens, buf = [], ""
    for ch in s + "\0":
        if ch in "⊕→∝\0":
            if buf.strip():
                itens.append(txt(buf.strip(), size, color, bold=bold))
            buf = ""
            if ch == "⊕":
                itens.append(marcador_cm(r=0.0055 * size, z=37, leve=True))      # sem o halo: a caixa do ⊕ é do tamanho da letra
            elif ch == "→":
                itens.append(MathTex(r"\rightarrow", font_size=max(36, size * 1.4), color=color))
                itens[-1]._partes = [(r"\rightarrow", color)]
            elif ch == "∝":
                itens.append(MathTex(r"\propto", font_size=max(36, size * 1.4), color=color))
                itens[-1]._partes = [(r"\propto", color)]
        else:
            buf += ch
    return VGroup(*itens).arrange(RIGHT, buff=0.12)


def quebra(s, size, larg):
    """Quebra um texto de selo em linhas que cabem em `larg` (Manim): primeiro nos ' · ', depois por palavras."""
    if tx(s, size).width <= larg:
        return [s]
    pal = s.replace(" · ", " ·· ").split(" ")                                   # v3: quebra gulosa por palavras (o "·" é uma palavra)
    linhas, atual = [], ""
    for w in pal:
        w = "·" if w == "··" else w
        c2 = (atual + " " + w) if atual else w
        if atual and tx(c2, size).width > larg:
            linhas.append(atual.rstrip(" ·"))
            atual = "" if w == "·" else w
        else:
            atual = c2
    if atual:
        linhas.append(atual.rstrip(" ·"))
    if len(linhas) <= 2:
        return linhas
    itens = s.split(" · ")
    linhas, atual = [], ""
    for it in itens:
        cand = (atual + " · " + it) if atual else it
        if tx(cand, size).width <= larg:
            atual = cand
            continue
        if atual:
            linhas.append(atual)
        atual = ""
        for w in it.split(" "):
            c2 = (atual + " " + w) if atual else w
            if atual and tx(c2, size).width > larg:
                linhas.append(atual)
                atual = w
            else:
                atual = c2
    if atual:
        linhas.append(atual)
    return linhas


def eqf(pre, num, den, post=(), size=48, cores=None):
    r"""MathTex de string única `pre + \frac{num}{den} + post` com os índices de glifo de cada parte (ordem do dvisvgm: antes, numerador,
    traço, denominador, depois). Retorna (MathTex, {"pre": [...], "num": [...], "bar": [i], "den": [...], "post": [...]}); `cores` usa
    chaves ("num", k) etc."""
    tex_ = junta(pre) + r"\frac{" + junta(num) + "}{" + junta(den) + "}" + junta(post)
    m = MathTex(tex_, font_size=size, color=WHITE_)
    idx, k = {}, 0
    for nome, partes in (("pre", pre), ("num", num), ("bar", None), ("den", den), ("post", post)):
        if partes is None:
            idx["bar"] = [k]
            k += 1
            continue
        idx[nome] = []
        for t in partes:
            n = ng(t)
            idx[nome].append(list(range(k, k + n)))
            k += n
    assert k == len(m[0]), f"glifos {k} != {len(m[0])} em {tex_}"
    m._partes = []
    for (nome, i), c in (cores or {}).items():
        for j in idx[nome][i]:
            m[0][j].set_color(c)
    m._gl = []
    for nome in ("pre", "num", "den", "post"):
        for i, t in enumerate({"pre": pre, "num": num, "den": den, "post": post}[nome]):
            m._partes.append((t, (cores or {}).get((nome, i), WHITE_)))
            m._gl.append((t, idx[nome][i]))
    return m, idx


def gl(m, lista):
    return VGroup(*[m[0][j] for j in lista])


def mp(m, idx, partes):
    g = VGroup(*[m[0][j] for k in partes for j in idx[k]])
    if hasattr(m, "_partes") and len(m._partes) == len(idx):
        g._tex = "".join(m._partes[k][0] for k in partes)                      # G24 v3: o voa sabe se o que entra é número
    return g


J = lambda idx, *ks: [j for k in ks for j in idx[k]]


# ── desenhos ────────────────────────────────────────────────────────────────────────────────────────────────
def agua(x0, x1, y, fundo=-4.5, seed=11, estrelas=True):
    """Lago à noite: superfície lisa (linha clara), água escura sem degradê, reflexos finos das estrelas e do brilho magenta (fundo, isento
    da auditoria de texto)."""
    rng = np.random.default_rng(seed)
    g = VGroup(Rectangle(width=x1 - x0, height=y - fundo).move_to(P3((x0 + x1) / 2, (y + fundo) / 2)).set_stroke(width=0).set_fill("#071026", 0.92))
    for k in range(int((x1 - x0) * 1.3)):                                   # brilho magenta do horizonte refletido logo abaixo da superfície
        xx = rng.uniform(x0 + 0.1, x1 - 0.6)
        yy = y - rng.uniform(0.08, 0.5)
        g.add(Line(P3(xx, yy), P3(xx + rng.uniform(0.3, 0.9), yy)).set_stroke(MAG, 1.6, opacity=rng.uniform(0.08, 0.16)))
    if estrelas:
        for k in range(int((x1 - x0) * 2.2)):                               # estrelas refletidas: traços curtos tremidos
            xx, yy = rng.uniform(x0 + 0.1, x1 - 0.2), rng.uniform(fundo + 0.2, y - 0.3)
            g.add(Line(P3(xx, yy), P3(xx + rng.uniform(0.06, 0.18), yy)).set_stroke(WHITE_, 1.3, opacity=rng.uniform(0.1, 0.24)))
    g.add(Line(P3(x0, y), P3(x1, y)).set_stroke(mix(BLUE_L, 0.35), 2.6, opacity=0.85))
    g._fundo = True
    return g.set_z_index(-5)


def onda_agua(c, r, op):
    """Anel na água (perspectiva: elipse achatada) no ponto c."""
    return Ellipse(width=2 * r, height=0.36 * r).move_to(c).set_stroke(mix(BLUE_L, 0.4), 2.2, opacity=op)


def folha(L, h=0.3):
    """Folha alongada em aço-azulado com a luz B (vista quase de lado: achatada), nervura central em GEO. Ponta esquerda em x = 0,
    nervura em y = 0."""
    pts = []
    for s in np.linspace(0, 1, 40):
        pts.append(P3(L * s, 0.5 * h * math.sin(PI * s) ** 0.8))
    for s in np.linspace(1, 0, 40):
        pts.append(P3(L * s, -0.5 * h * math.sin(PI * s) ** 0.8 * 0.9))
    f = aco(Polygon(*pts), borda=1.8)
    ner = Line(P3(0.02 * L, 0), P3(0.98 * L, 0)).set_stroke(GEO, 2.2, opacity=0.9)
    vs = VGroup(*[Line(P3(L * s, 0), P3(L * (s + 0.07), 0.32 * h * math.sin(PI * s) ** 0.8)).set_stroke(GEO, 1.2, opacity=0.5) for s in (0.2, 0.38, 0.56, 0.74)])
    return VGroup(f, ner, vs).set_z_index(4)


_GAF = {}


def gafanhoto(L=0.5, salto=0.0):
    """Gafanhoto de perfil, virado para a direita, em silhueta de aço com a luz B (G18: proporção real, nunca palito). L = comprimento do
    corpo (Manim). Pés em y = 0, x = 0 no centro de massa (≈ meio do corpo). `salto` 0 → 1 estica a perna de trás."""
    k = (round(L, 3), round(salto, 2))
    if k not in _GAF:
        u = lambda x, y: P3(L * x, L * y)
        e = salto
        joelho = (-0.27 + 0.05 * e, 0.24 - 0.12 * e)
        pe = (-0.12 - 0.3 * e, 0.0 - 0.06 * e)
        partes = [
            Polygon(u(-0.5, 0.13), u(-0.36, 0.2), u(0.0, 0.23), u(0.12, 0.22), u(0.12, 0.08), u(-0.1, 0.07), u(-0.42, 0.1)),     # abdômen
            Ellipse(width=0.32 * L, height=0.21 * L).move_to(u(0.2, 0.16)),                                                     # tórax
            Ellipse(width=0.18 * L, height=0.2 * L).move_to(u(0.39, 0.17)),                                                     # cabeça
            Polygon(u(0.06, 0.19), u(0.1, 0.12), u(joelho[0], joelho[1] - 0.025), u(joelho[0] - 0.02, joelho[1] + 0.035)),   # fêmur
            Polygon(u(joelho[0], joelho[1] + 0.01), u(joelho[0] + 0.02, joelho[1] - 0.02), u(pe[0] + 0.02, pe[1]), u(pe[0] - 0.02, pe[1] + 0.01)),   # tíbia
            Polygon(u(0.17, 0.1), u(0.2, 0.1), u(0.24, 0.0), u(0.21, 0.0)),                                                    # pata do meio
            Polygon(u(0.28, 0.1), u(0.31, 0.1), u(0.36, 0.0), u(0.33, 0.0)),                                                   # pata da frente
            Polygon(u(0.43, 0.25), u(0.45, 0.27), u(0.66, 0.42), u(0.65, 0.4)),                                                # antena
        ]
        try:
            s = Union(*partes)
        except Exception:
            s = VGroup(*partes)
        aco(s, borda=1.4)
        olho = Dot(u(0.42, 0.2), radius=0.022 * L, color="#1A2030")
        g = VGroup(s, olho)
        g._pe = 0.0
        _GAF[k] = g
    return _GAF[k].copy()


def nave(comp, alt, sen=1):
    """Nave 2D de perfil em aço com a luz B: casco, nariz, janela, aletas e bocal. sen = +1 nariz para a direita. Centro em (0, 0)."""
    w, h = comp, alt
    casco = Polygon(P3(-0.5 * w, 0.32 * h), P3(0.18 * w, 0.42 * h), P3(0.38 * w, 0.32 * h), P3(0.5 * w, 0.0), P3(0.38 * w, -0.32 * h),
                    P3(0.18 * w, -0.42 * h), P3(-0.5 * w, -0.32 * h))
    aleta_c = Polygon(P3(-0.5 * w, 0.3 * h), P3(-0.3 * w, 0.36 * h), P3(-0.42 * w, 0.62 * h), P3(-0.55 * w, 0.62 * h))
    aleta_b = aleta_c.copy().flip(RIGHT, about_point=ORIGIN)
    bocal = Polygon(P3(-0.5 * w, 0.18 * h), P3(-0.58 * w, 0.26 * h), P3(-0.58 * w, -0.26 * h), P3(-0.5 * w, -0.18 * h))
    g = VGroup(aco(aleta_c), aco(aleta_b), aco(bocal, 1.2), aco(casco))
    g.add(Circle(radius=0.11 * h).move_to(P3(0.22 * w, 0.06 * h)).set_fill("#1A2A44", 1).set_stroke("#7FB2FF", 1.6, opacity=0.8),
          Line(P3(-0.3 * w, -0.05 * h), P3(0.1 * w, -0.05 * h)).set_stroke(GEO, 1.4, opacity=0.4))
    if sen < 0:
        g.flip(UP, about_point=ORIGIN)
    return g.set_z_index(5)


def regua(x0, x1, y, K, xm0, xm1, passo=0.05, rot_cada=0.1, cor=GEO, cima=False, unidade="cm", op=1.0, rotulos=True):
    """Régua: traço de x0 a x1 (Manim), marcas de `passo` m nas posições xm (m) → x0 + K·(xm − xm0); números em cm a cada `rot_cada`."""
    g = VGroup(Line(P3(x0, y), P3(x1, y)).set_stroke(cor, 2.2, opacity=op))
    n0, n1 = int(math.ceil(xm0 / passo - 1e-6)), int(math.floor(xm1 / passo + 1e-6))
    s = 1 if cima else -1
    for n in range(n0, n1 + 1):
        xm = n * passo
        X = x0 + K * (xm - xm0)
        grande = abs(xm / rot_cada - round(xm / rot_cada)) < 1e-6
        g.add(Line(P3(X, y), P3(X, y + s * (0.16 if grande else 0.09))).set_stroke(cor, 2, opacity=op))
        if grande and rotulos:
            g.add(mrot(f"{round(xm * 100):d}".replace("-", "−"), 24, cor, op).next_to(P3(X, y + s * 0.16), UP if cima else DOWN, buff=0.07))
    return g


class Checklist:
    """As três perguntas (A4): versão grande (centro) e compacta (canto inferior direito, discreta); `acende(ns)` destaca as que decidem."""
    LONGAS = ("QUAL É O SISTEMA?", "TEM FORÇA EXTERNA? EM QUE DIREÇÃO?", "DE QUAL REFERENCIAL EU OLHO?")
    CURTAS = ("SISTEMA?", "FORÇA EXTERNA?", "REFERENCIAL?")

    @staticmethod
    def icone(k, s=1.0):
        if k == 0:
            r = RoundedRectangle(corner_radius=0.08 * s, width=0.42 * s, height=0.3 * s).set_stroke(WHITE_, 1.8)
            return VGroup(DashedVMobject(r, num_dashes=12, dashed_ratio=0.6), Dot(radius=0.04 * s, color=WHITE_).shift(0.07 * s * LEFT),
                          Dot(radius=0.04 * s, color=WHITE_).shift(0.08 * s * RIGHT))
        if k == 1:
            return VGroup(Square(0.18 * s).set_stroke(WHITE_, 1.6).set_fill(STEEL, 1).shift(0.1 * s * LEFT),
                          seta(P3(0.0, 0) * s, P3(0.26, 0) * s, FC, 3, tip=0.1 * s))
        return VGroup(Line(ORIGIN, 0.3 * s * RIGHT).set_stroke(GEO, 1.8), Line(ORIGIN, 0.3 * s * UP).set_stroke(GEO, 1.8),
                      Dot(radius=0.035 * s, color=WHITE_)).shift(0.15 * s * LEFT + 0.12 * s * DOWN)

    @classmethod
    def grande(cls):
        linhas = VGroup()
        for k in range(3):
            linhas.add(VGroup(cls.icone(k, 1.5), txt(f"{k + 1}.", 32, color=CYAN, bold=True), txt(cls.LONGAS[k], 32, bold=True)).arrange(RIGHT, buff=0.25))
        linhas.arrange(DOWN, buff=0.45, aligned_edge=LEFT)
        return linhas

    @classmethod
    def compacta(cls, acesas=()):
        linhas = VGroup()
        for k in range(3):
            on = k + 1 in acesas
            op = 1.0 if on else 0.42
            l = VGroup(cls.icone(k, 0.85), txt(f"{k + 1}", 24, color=CYAN if on else WHITE_, bold=True), txt(cls.CURTAS[k], 24, bold=on)).arrange(RIGHT, buff=0.14)
            escala_op(l, op)
            linhas.add(l)
        linhas.arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        caixa_ = RoundedRectangle(corner_radius=0.1, width=linhas.width + 0.34, height=linhas.height + 0.26).move_to(linhas) \
            .set_fill(PANEL, 0.7).set_stroke(BLUE_L, 1.4, opacity=0.5)
        caixa_._fundo = True
        g = VGroup(caixa_, linhas).set_z_index(38)
        return g.move_to(P3(7.42 - g.width / 2, -3.98 + g.height / 2))


class Prob(Base):
    """Base dos lotes: esqueleto dos problemas, checklist, selo de referencial e auditorias novas."""
    FUNDO = "fundo_lab_ex.png"

    def setup_base(self, cap=None, selo=None):
        super().setup_base(cap, selo)
        self.chk = None
        self.s1 = self.s2 = None          # selo da linha 1 (PEDE/CONFERE/DICA) e HIPÓTESES
        self.ref_mob, self.ref_atual = None, None
        self._futuros = []
        self._refs = []

    def fixos(self):
        f = super().fixos()
        if getattr(self, "chk", None) is not None:
            f.add(self.chk)
        return f

    # ── registro (qa_overlay_<lote>.json) ─────────────────────────────────────────────────────────────────────
    def reg(self, cena, **pts):
        if not hasattr(self, "_reg"):
            self._reg = {}
        f = int(round(self.clk.get_value() * FPS))

        def conv(v):
            if isinstance(v, (int, float, str)) or v is None:
                return v
            if isinstance(v, list):
                return [conv(x) for x in v]
            return np.asarray(v, float)[:3].tolist()
        self._reg.setdefault(cena, {})[f] = {k: conv(v) for k, v in pts.items()}
        return pts

    def gravar_reg(self):
        if PEDIDOS3D:
            return
        if getattr(self, "_reg", None):
            (AQUI / f"qa_overlay_{self.lote}.json").write_text(json.dumps(self._reg), encoding="utf-8")
        if AUDITORIA:
            (AQUI / f"qa_ref_{self.lote}.json").write_text(json.dumps(self._refs), encoding="utf-8")

    def ate_mov(self, frac, tracker, alvo, rate=linear):
        falta = (self._q0 + frac * (self.alvo - self._q0) - self.nq) / FPS
        if falta >= 0.2:
            self.play(tracker.animate(rate_func=rate).set_value(alvo), run_time=falta)

    # ── selos ─────────────────────────────────────────────────────────────────────────────────────────────────
    def _selo_mob(self, tag, corpo, cor=CYAN, borda=BLUE_L, size=26, wmax=6.85):
        t = txt(tag, 24, color=cor, bold=True)
        brutas = corpo if isinstance(corpo, (list, tuple)) else [corpo]

        def montar(larg, sz):
            out = []
            for l in brutas:
                out += quebra(l, sz, larg) if isinstance(l, str) else [l]
            return out
        opcoes = []
        for empilha in (False, True):
            larg = wmax - 0.36 if empilha else wmax - t.width - 0.58
            sz = size if all(not isinstance(l, str) or tx(l, size).width <= larg for l in brutas) else 24
            ls = montar(larg, sz)
            opcoes.append((len(ls) + (1 if empilha else 0), empilha, ls, sz))
        _, empilha, linhas, sz = min(opcoes, key=lambda o: (o[0], o[1]))
        cs = VGroup(*[(tx(l, sz) if isinstance(l, str) else VGroup(*[tx(i, sz) if isinstance(i, str) else i for i in l]).arrange(RIGHT, buff=0.1))
                      for l in linhas]).arrange(DOWN, buff=0.08, aligned_edge=LEFT)
        g = VGroup(t, cs).arrange(DOWN, buff=0.1, aligned_edge=LEFT) if empilha else VGroup(t, cs).arrange(RIGHT, buff=0.22, aligned_edge=UP)
        bx = RoundedRectangle(corner_radius=0.1, width=g.width + 0.36, height=g.height + 0.24).move_to(g).set_fill(PANEL, 0.88).set_stroke(borda, 1.8)
        bx._fundo = True
        sg = VGroup(bx, g).set_z_index(36)
        sg._selo_tag = True
        return sg

    def selo(self, tag, corpo, cor=CYAN, borda=BLUE_L, rt=0.5, x0=XC0 - 0.4):
        """Linha 1 da faixa de selos: o anterior sai e o novo entra no mesmo lugar (topo fixo em y = 3,12)."""
        novo = self._selo_mob(tag, corpo, cor, borda)
        novo.move_to(P3(x0 + novo.width / 2, 3.12 - novo.height / 2))
        anims = [FadeIn(novo, shift=0.1 * DOWN)]
        if self.s1 is not None:
            anims.append(FadeOut(self.s1))
        self.play(*anims, run_time=rt)
        if self.s1 is not None:
            self.remove(self.s1)
        self.s1 = novo
        return novo

    def pede(self, corpo, **kw):
        return self.selo("O QUE ESTE PEDE", corpo, **kw)

    def confere(self, corpo, **kw):
        return self.selo("CONFERE", corpo, cor=CYAN, **kw)

    def dica18(self, corpo, **kw):
        return self.selo("DICA", corpo, cor=CYAN, borda=CYAN, **kw)

    def hip(self, corpo, rt=0.5):
        """Linha 2: HIPÓTESES em uma linha (G21); vai embora na primeira conta (hip_sai)."""
        novo = self._selo_mob("HIPÓTESES" if not isinstance(corpo, str) or "·" in corpo else "HIPÓTESE", corpo, cor=CYAN, borda=GEO, size=24)
        topo = (self.s1.get_bottom()[1] - 0.12) if self.s1 is not None else 3.12
        novo.move_to(P3(XC0 - 0.3 + novo.width / 2, topo - novo.height / 2))
        self.play(FadeIn(novo, shift=0.1 * DOWN), run_time=rt)
        self.s2 = novo
        return novo

    def hip_sai(self, *anims, rt=0.4):
        if self.s2 is not None:
            self.play(FadeOut(self.s2), *anims, run_time=rt)
            self.remove(self.s2)
            self.s2 = None
        elif anims:
            self.play(*anims, run_time=rt)

    def selos_sai(self, rt=0.4):
        ms = [m for m in (self.s1, self.s2, self.ref_mob) if m is not None]
        if ms:
            self.play(*[FadeOut(m) for m in ms], run_time=rt)
            self.remove(*ms)
        self.s1 = self.s2 = self.ref_mob = None
        self.ref_atual = None

    # ── checklist ───────────────────────────────────────────────────────────────────────────────────────────
    def check(self, *acesas, rt=0.5):
        novo = Checklist.compacta(acesas)
        if self.chk is None:
            self.play(FadeIn(novo), run_time=rt)
        else:
            velho = self.chk
            self.chk = None
            self.play(FadeOut(velho), FadeIn(novo), run_time=rt)
            self.remove(velho)
        self.chk = novo

    # ── referencial (G20) ───────────────────────────────────────────────────────────────────────────────────
    def referencial(self, nome, pos=None, rt=0.5, anims=()):
        """Selo VISTO DA … no alto do ESQUEMA; enquanto durar, toda seta de velocidade registra este referencial."""
        novo = None
        if nome:
            t = txt(f"VISTO {nome}", 26, bold=True)
            bx = RoundedRectangle(corner_radius=0.1, width=t.width + 0.36, height=t.height + 0.24).move_to(t).set_fill(PANEL, 0.9).set_stroke(VEL, 2)
            bx._fundo = True
            novo = VGroup(bx, t).set_z_index(36)
            p = P3(-7.25 + novo.width / 2, pos) if isinstance(pos, (int, float)) else (pos if pos is not None else P3(-7.25 + novo.width / 2, 2.85))   # pos número = y, encostado à esquerda
            novo.move_to(p)
        ani = list(anims)
        if self.ref_mob is not None:
            ani.append(FadeOut(self.ref_mob))
        if novo is not None:
            ani.append(FadeIn(novo, shift=0.08 * DOWN))
        velho = self.ref_mob
        self.ref_mob, self.ref_atual = novo, nome
        if ani:
            self.play(*ani, run_time=rt)
        if velho is not None:
            self.remove(velho)
        return novo

    def seta_v(self, a, b, ref, cor=VEL, width=6, tip=0.2, op=1.0, z=12, nome=""):
        """Seta de velocidade (G20): registra (quadro, referencial da seta, selo ativo) para a auditoria REFERENCIAL."""
        if AUDITORIA and op > 0.15:
            f = int(round(self.clk.get_value() * FPS))
            self._refs.append([f, nome, ref, self.ref_atual])
        return seta(a, b, cor, width, tip=tip, op=op, z=z)

    # ── auditoria extra: texto sobre a trajetória dos próximos 2 s ─────────────────────────────────────────────────
    def _auditar(self, dentro=False):
        super()._auditar(dentro)
        if not self._futuros:
            return
        pts = []
        for fn in self._futuros:
            try:
                q = np.asarray(fn(), float).reshape(-1, 3)
                if len(q):
                    pts.append(q)
            except Exception:
                pass
        if not pts:
            return
        P_ = np.vstack(pts)
        fx = self.fixos()
        t = self.clk.get_value()

        def walk(m):
            if isinstance(m, ImageMobject):
                return
            if isinstance(m, (Text, SingleStringMathTex)):
                try:
                    o = max(max(x.get_fill_opacity(), x.get_stroke_opacity()) for x in m.family_members_with_points())
                except Exception:
                    o = 1.0
                if o > 0.08 and m.width > 0.01:
                    (x0, y0, _), (x1, y1, _) = m.get_critical_point(DL), m.get_critical_point(UR)
                    d = (P_[:, 0] > x0 - 0.02) & (P_[:, 0] < x1 + 0.02) & (P_[:, 1] > y0 - 0.02) & (P_[:, 1] < y1 + 0.02)
                    if d.any():
                        nm = m.text[:30] if isinstance(m, Text) else m.get_tex_string()[:30]
                        print(f"[audit] {t:7.1f}s TEXTO SOBRE TRAJETÓRIA '{nm}'")
                return
            for s_ in m.submobjects:
                walk(s_)
        for top in self.mobjects:
            if top not in fx and top is not self.clk and top is not getattr(self, "dica_atual", None):
                walk(top)

    def fim(self):
        super().fim()


# TransformByGlyphMap com auto_fade por padrão (os glifos fora do mapa entram/saem em fade): sobrescreve o import do MF_Tools nas seções
from MF_Tools import TransformByGlyphMap as _TBGM  # noqa: E402


def TransformByGlyphMap(*a, **k):
    k.setdefault("auto_fade", True)
    return _TBGM(*a, **k)

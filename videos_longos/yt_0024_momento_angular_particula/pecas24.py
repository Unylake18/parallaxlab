"""yt_0024 — peças comuns: câmeras da mesa (C_34, C_TOPO, C_L) com a MESMA projeção do mesa.js, a mesa viva (Fundo3D 'mesa_furo' dirigido
pelo relógio da cena e pela física de fisica24.py), camadas Manim presas à mesa, mostradores, ⊙/⊗, sublinhado de resultado, auditoria de
OPACIDADE (yt_0023) e registro ÁLGEBRA. Base dos lotes: Lote24."""
from pecas22 import *  # noqa: F401,F403
import fisica24 as F
from prob2 import _log_flash

LMAG = "#F19AFF"
RAD = math.pi / 180


# ── câmeras ────────────────────────────────────────────────────────────────────────────────────────────────
def camd(az, el, alvo, K, fov, xc, yc):
    return dict(az=float(az), el=float(el), alvo=[float(a) for a in alvo], K=float(K), fov=float(fov), xc=float(xc), yc=float(yc))


C34H = camd(-55, 16, (0, 0, -0.30), 5.6, 43.6, 0.0, 0.10)        # v2 hook: mesa a ~80 % da largura, disco ≥ 3 % (≈ 60 px a 1080p)
C34 = camd(-57, 34, (0.0, 0.0, -0.15), 2.95, 43.6, -3.85, 0.55)    # v2 teoria: a mesa na coluna esquerda inteira (x −7,3 … −0,7)
CTOPO = camd(-90, 90, (0, 0, 0), 3.6, 0.0, -4.50, -0.75)           # v2 ortográfica: tampo inteiro (x −7,1 … −1,3); o HUD fica à direita da mesa
C34B1 = camd(-57, 34, (0.05, 0.0, -0.15), 4.9, 43.6, -4.3, 0.15)      # v3 §2.2 B1: close de bancada (disco ≥ 3 % da largura; a mesa pode sair pela esquerda e por baixo)
C34B6 = camd(-57, 34, (0.0, 0.0, -0.15), 4.2, 43.6, -4.0, 0.10)      # v3 §4: B6-1 com o disco ≥ 3 % da largura (órbita de 0,60 m dentro da coluna)
CPLANO = camd(-68, 42, (0, 0, 0), 3.5, 0.0, -5.3, -0.30)         # v4 §1: mesa inclinada de verdade (el 42°, az 22° fora da simetria; ortográfica: paralelismo e razões de área preservados); close de bancada: a ponta esquerda sai do quadro, o canto direito fica antes do HUD (x ≤ −1,6)
CL = camd(-55, 35, (0, 0, 0), 2.9, 43.6, -3.85, -0.55)             # L⃗ saindo do plano
HUD_X = (-1.48, 0.19)                                               # faixa do HUD: entre a borda direita da mesa (C_TOPO) e a calha


def interp_cam(a, b, u):
    """Dolly contínuo a → b (u já suavizado). Para a ortográfica: o fov encolhe até 0,5° com a escala do alvo fixa; no fim (u = 1) troca para
    a ortográfica (diferença ≤ 0,03 px no plano do tampo)."""
    if u <= 0:
        return dict(a)
    if u >= 1:
        return dict(b)
    c = {k: a[k] + (b[k] - a[k]) * u for k in ("az", "el", "K", "xc", "yc")}
    c["alvo"] = [a["alvo"][i] + (b["alvo"][i] - a["alvo"][i]) * u for i in range(3)]
    fa, fb = a["fov"] or 0.5, b["fov"] or 0.5
    c["fov"] = math.exp(math.log(fa) + (math.log(fb) - math.log(fa)) * u)
    return c


def _base(c):
    a, e = c["az"] * RAD, c["el"] * RAD
    al = np.array(c["alvo"], float)
    d = np.array([math.cos(e) * math.cos(a), math.cos(e) * math.sin(a), math.sin(e)])
    up = np.array([-math.sin(e) * math.cos(a), -math.sin(e) * math.sin(a), math.cos(e)])
    f = -d
    r = np.cross(f, up)
    r /= np.linalg.norm(r)
    u = np.cross(r, f)
    return al, d, f, r, u


def proj(c, p):
    """Ponto 3D (m) → Manim, pela mesma câmera do mesa.js (perspectiva com setViewOffset, ou ortográfica)."""
    al, d, f, r, u = _base(c)
    p = np.asarray(p, float)
    if c["fov"] > 0:
        th = math.tan(c["fov"] * RAD / 2)
        D = (9 / c["K"] / 2) / th
        q = p - (al + D * d)
        z = q @ f
        return np.array([c["xc"] + 8 / (th * 16 / 9) * (q @ r) / z, c["yc"] + 4.5 / th * (q @ u) / z, 0.0])
    q = p - al
    return np.array([c["xc"] + c["K"] * (q @ r), c["yc"] + c["K"] * (q @ u), 0.0])


def px_de(m):
    return [(m[0] + 8) / 16 * 960, (4.5 - m[1]) / 9 * 540]


# ── símbolos e peças ────────────────────────────────────────────────────────────────────────────────────────
def sai_entra(c, saindo=True, r=0.22, cor=LMAG, z=14):
    """⊙ (saindo do plano) / ⊗ (entrando) na cor do momento angular."""
    circ = Circle(radius=r).move_to(c).set_stroke(cor, 3.2)
    if saindo:
        mio = Dot(c, radius=0.06 * r / 0.22 + 0.01, color=cor)
    else:
        k = 0.62 * r
        mio = VGroup(Line(c + P3(-k, -k), c + P3(k, k)), Line(c + P3(-k, k), c + P3(k, -k))).set_stroke(cor, 3.0)
    return VGroup(circ, mio).set_z_index(z)


def sublinha(m, cor, w=3, buff=0.1):
    """Sublinhado fino do resultado (no lugar da caixa), na cor da grandeza do lado esquerdo."""
    l = Line(m.get_corner(DL) + DOWN * buff, m.get_corner(DR) + DOWN * buff).set_stroke(cor, w)
    l._sub = True
    return l.set_z_index(m.z_index or 0)


def angulo_reto(v, a, b, s=0.2, cor=GEO, w=2.4):
    """Marca de ângulo reto no vértice v entre as direções v→a e v→b."""
    u1 = (np.asarray(a) - v) / max(np.linalg.norm(np.asarray(a) - v), 1e-6)
    u2 = (np.asarray(b) - v) / max(np.linalg.norm(np.asarray(b) - v), 1e-6)
    return VMobject().set_points_as_corners([v + s * u1, v + s * (u1 + u2), v + s * u2]).set_stroke(cor, w).set_z_index(13)


def cantoneira(v, a, b, s=0.34, cor=GEO, w=2.4):
    """Ângulo reto limpo entre v→a e v→b: três lados de um quadrado de lado s, com o vértice interno em v + s·(u1 + u2) (fora do disco, que ocupa o vértice)."""
    v, a, b = np.asarray(v, float), np.asarray(a, float), np.asarray(b, float)
    u1 = (a - v) / max(np.linalg.norm(a - v), 1e-6)
    u2 = (b - v) / max(np.linalg.norm(b - v), 1e-6)
    return VMobject().set_points_as_corners([v + s * u1, v + s * (u1 + u2), v + s * u2]).set_stroke(cor, w).set_z_index(13)


def arco_ang(v, a, b, r=0.5, cor=ANG, w=4):
    """Arco âmbar no vértice v de v→a até v→b (menor ângulo)."""
    a0 = math.atan2(a[1] - v[1], a[0] - v[0])
    a1 = math.atan2(b[1] - v[1], b[0] - v[0])
    da = (a1 - a0 + math.pi) % (2 * math.pi) - math.pi
    return Arc(radius=r, start_angle=a0, angle=da, arc_center=v).set_stroke(cor, w).set_z_index(13)


def pino2d(c, r=0.13):
    """Ponto fixo O como pino de aço 2.5D (disco com brilho)."""
    g = VGroup(Circle(radius=r).move_to(c).set_fill("#7A8696", 1).set_stroke("#C9D3E3", 2),
               Circle(radius=r * 0.45).move_to(c + P3(-0.3 * r, 0.3 * r)).set_fill("#DDE6F3", 0.85).set_stroke(width=0))
    g._degrade = "aco"
    return g.set_z_index(10)


def pedra2d(c, r=0.30):
    """Pedra rosa 2.5D (massa): polígono irregular com sombreado."""
    rng = np.random.default_rng(5)
    pts = [c + r * (0.85 + 0.25 * rng.random()) * np.array([math.cos(a), math.sin(a), 0]) for a in np.linspace(0, 2 * math.pi, 11)[:-1]]
    corpo = Polygon(*pts).set_fill(escuro(MAS, 0.35), 1).set_stroke(MAS, 3)
    luz = Polygon(*[c + 0.45 * (p - c) + P3(-0.08, 0.08) for p in pts]).set_fill(mix(MAS, 0.35), 0.5).set_stroke(width=0)
    return VGroup(corpo, luz).set_z_index(10)


def sol2d(c, r=0.32):
    g = VGroup(*[Circle(radius=r * k).move_to(c).set_fill("#FFC24D", 0.10 + 0.0 * k).set_stroke(width=0) for k in (2.4, 1.8, 1.35)],
               Circle(radius=r).move_to(c).set_fill("#FFD27A", 1).set_stroke("#FFF1C9", 2))
    return g.set_z_index(9)


def mao_rd(c, s=1.0, cor="#C9D3E3"):
    """Ícone 2.5D da regra da mão direita: quatro dedos curvando (de r para p) e o polegar para cima (L)."""
    palma = RoundedRectangle(width=0.55 * s, height=0.42 * s, corner_radius=0.12 * s).move_to(c).set_fill("#3A465A", 1).set_stroke(cor, 2)
    dedos = VGroup(*[Arc(radius=(0.30 - 0.03 * k) * s, start_angle=-0.2, angle=2.6, arc_center=c + P3(0.20 * s, (0.12 - 0.08 * k) * s))
                     .set_stroke(cor, 5 - 0.4 * k) for k in range(4)])
    polegar = Line(c + P3(-0.12 * s, 0.18 * s), c + P3(-0.12 * s, 0.78 * s)).set_stroke(LMAG, 7)
    ponta = Triangle().scale(0.09 * s).move_to(c + P3(-0.12 * s, 0.84 * s)).set_fill(LMAG, 1).set_stroke(width=0)
    return VGroup(palma, dedos, polegar, ponta).set_z_index(16)


def num(v, casas=2, sinal=False):
    s = f"{v:+.{casas}f}" if sinal else f"{v:.{casas}f}"
    return s.replace("-", "-").replace(".", "{,}")


def dentro_poly(poly, q):
    """Ponto q (x, y) dentro do polígono (lista de vértices) — raio horizontal."""
    x, y, dentro = q[0], q[1], False
    n = len(poly)
    for i in range(n):
        (x0, y0), (x1, y1) = poly[i], poly[(i + 1) % n]
        if (y0 > y) != (y1 > y) and x < x0 + (y - y0) * (x1 - x0) / (y1 - y0):
            dentro = not dentro
    return dentro


class Pilha24(Pilha):
    """v3 §1.3: no máximo 4 linhas (a coluna rola: a mais antiga sobe e apaga); registra cada linha para TAMANHO ÚNICO e CADEIA."""

    def poe(self, m, dx=0.0, rt=0.35, manter=()):
        while len(self.linhas) >= 4 and not (eh_filha(m) and len(self.blocos()) == 1):
            idx = self.blocos()[0]                      # rola um BLOCO inteiro (mãe e filhas): nunca deixa filha órfã
            vel = [self.linhas[i][0] for i in idx]
            self.cena.play(*[FadeOut(l, shift=0.25 * UP) for l in vel], run_time=0.3)
            for l in vel:
                self.cena.remove(l)
            self.linhas = [it for k, it in enumerate(self.linhas) if k not in idx]
            self._reflow(self.linhas, 0.3)
        if isinstance(m, MathTex):
            tex = (getattr(m, "tex_string", "") or "").strip()
            acima = "nada"
            if self.linhas:
                l_ = self.linhas[-1][0]
                acima = "tex" if isinstance(l_, MathTex) else "txt"
            print(f"[linha] {self.cena.clk.get_value():7.2f} fs={m.font_size:.1f} cont={int(tex.startswith('='))} acima={acima} | {tex[:70]}")
        return super().poe(m, dx=dx, rt=rt, manter=manter)


def cartao(tex_partes, rotulo, cores=None):
    """v3 §1.4: cartão de referência FORA da cadeia (acima, à esquerda da CONTA): MathTex 40 a 70 % e rótulo pequeno; acende quando citado."""
    m, im = M(*tex_partes, size=46, cores=cores)
    lab = txt(rotulo, 24, bold=True, color=DIM)
    g = VGroup(lab, m).arrange(RIGHT, buff=0.25).move_to(P3(0.85, 2.98), aligned_edge=LEFT)
    g.set_opacity(0.7)
    g._chip = True
    for x in g.get_family():
        x._chip = True
    return g.set_z_index(30), m, im


# ── base dos lotes ─# ── base dos lotes ─────────────────────────────────────────────────────────────────────────────────────────
class Lote24(Lote22):
    """Base: mesa viva (opcional), relógio físico, canto de duas linhas com MathTex, OPACIDADE e ÁLGEBRA."""

    def setup_base(self, cap=None, selo=None):
        super().setup_base(cap, selo)
        self.pilha = Pilha24(self, x0=0.7, topo=2.35, base=-3.30, buff=0.30)
        self.f3 = None
        self.camA = self.camB = C34
        self.camu = ValueTracker(0.0)
        self.add(self.camu)
        self._tf0, self._c0, self._vel = 0.0, 0.0, 0.0          # tempo físico = tf0 + vel·(clk − c0)
        self.mov = lambda tf: (F.R0 * math.cos(F.W0 * tf), F.R0 * math.sin(F.W0 * tf))
        self.zp = lambda tf: 0.0
        self.fio, self.pinos, self.desf, self.rastro_on = True, [], 0.0, True
        self.disco_on = True
        self.extra3 = {}
        self.desf_tr = ValueTracker(0.0)
        self.add(self.desf_tr)
        self.tp = 1e9                                            # início da puxada (tempo físico); 1e9 = sem puxada

    def play(self, *anims, **kw):
        """v3 §1.3 CANETA: termo da CONTA nunca entra por FadeIn de MathTex pronto (só caneta, voo ou glyph map)."""
        def varre(an_):
            for b_ in getattr(an_, "animations", None) or []:
                varre(b_)
            m_ = getattr(an_, "mobject", None)
            if type(an_) is FadeIn and m_ is not None and any(isinstance(x, Text) for x in m_.get_family()):
                _log_flash(self.clk.get_value(), an_)          # v5 #10: FLASH POR QUADRO também para texto (txt) e selos: o retângulo tem que estar vazio antes da vez
            if type(an_) is FadeIn and m_ is not None and not getattr(m_, "_chip", False):
                for x in m_.get_family():
                    if isinstance(x, MathTex) and x.get_x() > 0.7 and x.get_y() < 2.45 and not getattr(x, "_hud", False) and "=" in (getattr(x, "tex_string", "") or ""):
                        print(f"[audit] {self.clk.get_value():7.1f}s CANETA FadeIn de termo pronto {(getattr(x, 'tex_string', '') or '')[:40]!r}")
                        break
        for an_ in anims:
            varre(an_)
        return super().play(*anims, **kw)

    # relógio físico
    def tf(self):
        return self._tf0 + self._vel * (self.clk.get_value() - self._c0)

    def anda(self, vel=1.0, tf=None):
        """Muda a velocidade do tempo físico (0 = congela) sem salto de posição; `tf` reposiciona."""
        t = self.tf() if tf is None else tf
        self._tf0, self._c0, self._vel = t, self.clk.get_value(), vel

    def cam(self):
        u = float(self.camu.get_value())
        return interp_cam(self.camA, self.camB, u)

    def dolly(self, para, rt=1.6, *anims):
        """Dolly contínuo da câmera atual até `para` (1,6 s); para exatamente no último quadro."""
        self.camA, self.camB = self.cam(), para
        self.camu.set_value(0.0)
        self.play(self.camu.animate.set_value(1.0), *anims, run_time=rt, rate_func=smooth)
        self.camA = self.camB = para
        self.camu.set_value(0.0)

    def disco(self, tf=None):
        return self.mov(self.tf() if tf is None else tf)

    def rastro(self, tf):
        if not self.rastro_on:
            return []
        n = 150
        pts = [self.mov(tf - 0.9 + 0.9 * k / (n - 1)) for k in range(n)]
        for k in range(n - 1, 0, -1):      # v13: a reprise em laço (self.loop) emenda o fim da volta anterior (r = 0,30) com o começo (r = 0,60): o rastro começa depois do salto
            if math.hypot(pts[k][0] - pts[k - 1][0], pts[k][1] - pts[k - 1][1]) > 0.12:
                pts = pts[k:]
                break
        if len(pts) < 2:
            return []
        return [[round(x, 4), round(y, 4)] for x, y in pts]

    def estado3d(self, _t=0.0):
        tf = self.tf()
        e = dict(cam=self.cam(), fio=self.fio, zp=self.zp(tf), pinos=self.pinos, desf=float(self.desf_tr.get_value()))
        if self.disco_on:
            x, y = self.mov(tf)
            e["disco"] = [x, y]
            e["rastro"] = self.rastro(tf)
            if getattr(self, "vth", None):
                e["vth"] = self.vth(tf)
        e.update(self.extra3)
        e = r4(e)
        e["solT"] = round(float(self.clk.get_value()), 2)
        e["t_tab"] = round(float(tf), 6)          # v2 §1: tempo da tabela gravado por quadro (o QA mede L por ele, não pelo índice do quadro)
        return e

    def mesa(self):
        f3 = Fundo3D(self, "mesa_furo", self.estado3d)
        f3._fundo3d = True
        self.f3 = f3
        self.add(f3)
        return f3

    def tela(self, xyz):
        return proj(self.cam(), xyz)

    def tela_disco(self, dz=0.0):
        x, y = self.disco()
        return proj(self.cam(), (x, y, 0.010 + dz))

    # canto (linha 2) com símbolos em MathTex
    def canto(self, *pecas):
        velhos = [m for m in (self.h2,) if m is not None]
        if velhos:
            self.play(*[FadeOut(m) for m in velhos], run_time=0.25)
        pcs = [txt(p, 30) if isinstance(p, str) else p for p in pecas]
        novo = linha_base(pcs, 0.14).next_to(self.h1, DOWN, buff=0.14, aligned_edge=LEFT).set_z_index(40)
        self.h2 = novo
        self._pend.append(FadeIn(novo))

    # ── v2 §4.1 OPACIDADE (yt_0023) ──
    def _auditar_v5(self, t, itens, op):
        super()._auditar_v5(t, itens, op)
        runs = getattr(self, "_op_runs", None)
        if runs is None:
            runs = self._op_runs = {}
        vivos = set()
        for m in itens:
            for x in m.get_family():
                if isinstance(x, (Text, SingleStringMathTex)) and 0.05 < op(x) < 0.6 and not getattr(x, "_fantasma", False):
                    k = id(x)
                    vivos.add(k)
                    runs[k] = runs.get(k, 0) + 1
                    if runs[k] == 3:
                        s = getattr(x, "text", None) or getattr(x, "tex_string", "?")
                        print(f"[audit] {t:7.1f}s OPACIDADE BAIXA {s[:40]!r} em {op(x):.2f} por mais de 6 quadros")
        for k in list(runs):
            if k not in vivos:
                del runs[k]
        audita_vetor(self, itens, op, t)
        # ── v2 §7 HUD: no máximo 3 mostradores; nenhum dentro da CONTA (x > 0,7) nem sobre a mesa ──
        huds = [m for m in self.mobjects if any(getattr(x, "_hud", False) for x in m.get_family()) and m.get_family()
                and max((op(x) for x in m.family_members_with_points()), default=0) > 0.3]
        if len(huds) > 3:
            print(f"[audit] {t:7.1f}s HUD {len(huds)} mostradores visíveis (> 3)")
        mesa_poly = None
        if self.f3 is not None and float(self.f3.op.get_value()) > 0.3:
            c = self.cam()
            mesa_poly = [proj(c, (x, y, 0.0))[:2] for x, y in ((-.8, -.8), (.8, -.8), (.8, .8), (-.8, .8))]
        for m in huds:
            x0, x1 = m.get_left()[0], m.get_right()[0]
            if x1 > 0.7:
                print(f"[audit] {t:7.1f}s HUD dentro da coluna da CONTA (x até {x1:.2f})")
            if mesa_poly is not None:
                cc = [m.get_left()[:2] + np.array([0.05, 0]), m.get_center()[:2]]
                if any(dentro_poly(mesa_poly, q) for q in cc):
                    print(f"[audit] {t:7.1f}s HUD sobre a mesa em ({m.get_x():.2f}; {m.get_y():.2f})")

    # ── ÁLGEBRA: registro por linha (lei, voo, GM, escrita) ──
    def alg(self, metodo, linha, n_voos=0, numero=False):
        tex_ = getattr(linha, "tex_string", None) or "?"
        print(f"[alg] {self._aid} {metodo} voos={n_voos} num={int(numero)} | {tex_[:90]}")

    def lei(self, A, ia, voos=None, rt=1.0, metodo=None, numero=False):
        """Linha já posta na Pilha, construída da esquerda para a direita (voos do desenho; o resto escreve na vez)."""
        voos = voos or {}
        self.monta(A, ia, voos, rt=rt)
        self.alg(metodo or ("voo" if voos else "escrita"), A, len(voos), numero)
        return A

    def gm(self, src, dst, *mapas, rt=1.2, numero=False, extra=()):
        self.passo(src, dst, *mapas, rt=rt, extra=extra)
        # v2 §7 GM PARCIAL: ao fim do glyph map a linha tem que estar inteira na tela (nenhum glifo faltando ou apagado)
        cena = set(id(x) for m in self.mobjects for x in m.get_family())
        falta = [g for g in dst.family_members_with_points() if id(g) not in cena or max(g.get_fill_opacity(), g.get_stroke_opacity()) < 0.9]
        if falta:
            print(f"[audit] {self.clk.get_value():7.1f}s GM PARCIAL {len(falta)} glifos de {getattr(dst, 'tex_string', '?')[:40]!r} ausentes depois do GM")
        self.alg("GM", dst, 0, numero)
        return dst

    def resultado(self, m, cor, rt=0.35):
        """Sublinhado fino na cor da grandeza; ele passa a fazer parte da linha (anda e sai com ela na Pilha)."""
        if not any(m is x for x in self.mobjects):
            self.add(m)
        s = sublinha(m, cor)
        self.play(Create(s), run_time=rt)
        self.remove(s)
        m.add(s)
        return s

    def texto_na_linha(self, A, texto, cor, size=34, rt=0.5):
        """v2 §1/§6: texto dentro de fórmula nunca em \text{} (serifa): Space Grotesk maiúsculo (txt) na cor, preso à linha da Pilha."""
        if not any(A is m for m in self.mobjects):
            self.add(A)              # a linha montada por voa() fica em pedaços na cena; o texto preso a A precisa de A na cena
        t = txt(texto, size, bold=True, color=cor).next_to(A, RIGHT, buff=0.24)
        t.align_to(A, DOWN).shift(UP * 0.02)
        self.play(FadeIn(t, shift=0.05 * RIGHT), run_time=rt)
        self.remove(t)
        A.add(t)
        return t

    def transicao(self, rt=0.5, *anims):
        """v5 (handoff v5 §2 / ajuste 1): SEM varredura de luz (a barra branca vertical foi removida). A transição entre blocos é só o crossfade de
        0,5 s da montagem (montar_preview.py); aqui o bloco apenas segue em movimento durante `rt` (o 3D já está vivo)."""
        vt = ValueTracker(0.0)
        self.add(vt)
        self.play(vt.animate.set_value(1.0), *anims, run_time=rt, rate_func=linear)
        self.remove(vt)

    def selo_canto(self, tag, corpo, **kw):
        return self.selo(tag, corpo, **kw)


def mov_puxada(cena):
    """Órbita de r0 até cena.tp, puxada de 1,15 s e órbita de r1 depois (θ contínuo)."""
    def f(tf):
        lp = getattr(cena, "loop", None)
        if lp:                                                  # v3 §2.4: a puxada repete em laço (disco vivo ao fundo do fantasma)
            tf = lp[0] + ((tf - lp[0]) % lp[1])
        if cena.tp > 1e8:
            return (F.R0 * math.cos(F.W0 * tf), F.R0 * math.sin(F.W0 * tf))
        e = F.puxada(tf - cena.tp)
        th = e["th"] + F.W0 * cena.tp
        return (e["r"] * math.cos(th), e["r"] * math.sin(th))
    return f


def zp_puxada(cena):
    def z(tf):
        lp = getattr(cena, "loop", None)
        if lp:
            tf = lp[0] + ((tf - lp[0]) % lp[1])
        return 0.0 if cena.tp > 1e8 else F.puxada(tf - cena.tp)["zp"]
    return z


def vth_puxada(cena):
    """v_θ da física no instante exportado (§4: o QA mede L = m r v_θ pelo estado do quadro, não por Δθ/Δt entre quadros)."""
    def v(tf):
        lp = getattr(cena, "loop", None)
        if lp:
            tf = lp[0] + ((tf - lp[0]) % lp[1])
        return F.W0 * F.R0 if cena.tp > 1e8 else F.puxada(tf - cena.tp)["vth"]
    return v


def Mx(*partes, size=54, cores=None):
    """Linha da CONTA (MathTex de string única, cor por token)."""
    return M(*partes, size=size, cores=cores)


def mostrador(rot, fn, casas, unidade, cor, pos, size=38):
    """Mostrador vivo: rótulo (MathTex na cor) = valor (na cor) unidade (branca), num painel PANEL com borda na cor."""
    def f():
        v = fn()
        g = VGroup(T(rot, size, cor), T("=", size, WHITE_), T(num(v, casas), size, cor), T(unidade, size, WHITE_)).arrange(RIGHT, buff=0.1)
        g[3].align_to(g[2], DOWN)
        g.move_to(pos, aligned_edge=LEFT)
        bx = RoundedRectangle(corner_radius=0.08, width=g.width + 0.3, height=0.62).move_to(g).set_fill(PANEL, 0.88).set_stroke(cor, 1.6)
        bx._fundo = True
        return VGroup(bx, g).set_z_index(30)
    return vivo(f)


# ══ v2 §2.3 · componentes do "laboratório Parallax" (uma função por componente, reusada no vídeo inteiro) ══════════════════════════
def vetor_lab(a, b, cor, w=7, tip=0.24, origem=True, brilho=True, z=12):
    """Vetor: haste stroke 7, ponta afiada, ponto de origem (r 0,06) e brilho suave (cópia stroke 18 a 22 %)."""
    a, b = np.asarray(a, float), np.asarray(b, float)
    g = VGroup()
    if brilho and np.linalg.norm(b - a) > 0.05:
        u = (b - a) / np.linalg.norm(b - a)
        gl = Line(a, b - u * tip * 0.6).set_stroke(cor, 18, opacity=0.22)
        gl._brilho = True
        g.add(gl)
    g.add(seta(a, b, cor, w, tip=tip))
    if origem:
        g.add(Dot(a, radius=0.06, color=cor))
    g._geo = (a.copy(), b.copy())                 # v5: extremos reais da seta (a auditoria VETOR compara com a regra, não com a própria tela)
    return g.set_z_index(z)


# ══ v5 · CONVENÇÃO DE VETORES (handoff v5 §1): função única por tipo; cada vetor leva `_vec` para a auditoria VETOR ═════════════════
def seta_curva(a, b, cor, w=6, tip=0.2, lado=1.0, arq=0.10, z=12):
    """Seta levemente curva (Bézier quadrática, flecha `arq` × comprimento para o lado `lado` = ±1): cauda EXATA em a, ponta EXATA em b.
    Usada quando r⃗ é paralelo a p⃗ (referência sobre a reta do momento) para r⃗ não se fundir com p⃗."""
    a, b = np.asarray(a, float), np.asarray(b, float)
    L = float(np.linalg.norm(b - a))
    if L < 0.08:
        return VGroup()
    u = (b - a) / L
    n = np.array([-u[1], u[0], 0.0]) * lado
    c = (a + b) / 2 + n * arq * L * 2
    ts = np.linspace(0, 1, 18)
    pts = [(1 - t) ** 2 * a + 2 * t * (1 - t) * c + t * t * b for t in ts]
    tg = pts[-1] - pts[-3]
    tg = tg / max(np.linalg.norm(tg), 1e-6)
    tl = min(tip, 0.45 * L)
    nn = np.array([-tg[1], tg[0], 0.0])
    corpo = VMobject().set_points_as_corners(pts[:-1] + [b - tg * tl * 0.92]).set_stroke(cor, w)
    ponta = VMobject().set_points_as_corners([b, b - tg * tl + nn * tl * 0.55, b - tg * tl - nn * tl * 0.55, b]).set_stroke(cor, 1, opacity=1).set_fill(cor, 1)
    br = VMobject().set_points_as_corners(pts[:-1] + [b - tg * tl * 0.6]).set_stroke(cor, 18, opacity=0.22)
    g = VGroup(br, corpo, ponta, Dot(a, radius=0.06, color=cor))
    g._geo = (a.copy(), b.copy())
    return g.set_z_index(z)


def vec_r(cena, O3d, cor, lado=1.0, curvo=False, w=6, tip=0.2):
    """r⃗: CAUDA NO PONTO DE REFERÊNCIA (O3d), PONTA NO CENTRO DO DISCO. Única função que desenha r⃗ nas cenas da mesa vista de cima/inclinada."""
    a, b = cena.tela(O3d), cena.tela_disco()
    g = seta_curva(a, b, cor, w=w, tip=tip, lado=lado) if curvo else vetor_lab(a, b, cor, w=w, tip=tip)
    g._vec = dict(tipo="r", ref=lambda: cena.tela(O3d), part=lambda: cena.tela_disco())
    return g


def etiqueta_vec(g, tipo, **spec):
    """Etiqueta a seta `g` (resultado de vetor_lab/seta_curva) para a auditoria VETOR. tipo: 'r' (ref, part), 'aponta' (alvo), 'sentido' (ref = vetor de tela)."""
    for x in (g.get_family() if isinstance(g, VMobject) else [g]):
        if getattr(x, "_geo", None) is not None:
            x._vec = dict(tipo=tipo, **spec)
            break
    return g


def pino_ref(cena, O3d, r_m=0.034, cor=WHITE_, z=13):
    """Pino de referência VISÍVEL: anel (elipse projetada do círculo de r_m sobre o tampo) com ponto no centro; segue a câmera."""
    def f():
        c = np.asarray(O3d, float)
        pts = [cena.tela(c + r_m * np.array([math.cos(a), math.sin(a), 0.0])) for a in np.linspace(0, 2 * math.pi, 40)]
        g = VGroup(VMobject().set_points_as_corners(pts).set_stroke(cor, 3.0), Dot(cena.tela(c), radius=0.035, color=cor))
        return g.set_z_index(z)
    return vivo(f)


def audita_vetor(cena, itens, op, t):
    """Auditoria VETOR (handoff v5 §1.6), por quadro, nas setas com `_vec`: 'r' → cauda a ≤ 3 px do ponto de referência e ponta a ≤ 3 px da partícula;
    'aponta' → a seta tem produto escalar > 0 com (alvo − cauda) (T⃗/F⃗ para o furo/centro); 'sentido' → produto escalar > 0 com o vetor de referência (p⃗ ∥ v⃗)."""
    for m in itens:
        for x in m.get_family():
            v, geo = getattr(x, "_vec", None), getattr(x, "_geo", None)
            if not v or geo is None:
                continue
            if max((op(y) for y in x.family_members_with_points()), default=0) < 0.3:
                continue
            a, b = geo
            if v["tipo"] == "r":
                da = float(np.linalg.norm((a - v["ref"]())[:2])) / 16 * 960
                db = float(np.linalg.norm((b - v["part"]())[:2])) / 16 * 960
                if da > 3.0 or db > 3.0:
                    print(f"[audit] {t:7.1f}s VETOR r⃗ cauda a {da:.1f} px do ponto de referência / ponta a {db:.1f} px da partícula")
            elif v["tipo"] == "aponta":
                if float(np.dot((b - a)[:2], (v["alvo"]() - a)[:2])) <= 0:
                    print(f"[audit] {t:7.1f}s VETOR seta não aponta para o alvo ({v.get('nome', '?')})")
            elif v["tipo"] == "sentido":
                if float(np.dot((b - a)[:2], np.asarray(v["ref"]())[:2])) <= 0:
                    print(f"[audit] {t:7.1f}s VETOR seta contra o sentido de referência ({v.get('nome', '?')})")


def pulso(m, s=1.08):
    """Destaque de linha da CONTA só por escala (ida e volta): os operadores continuam brancos (COR OPERADOR)."""
    return m.animate(rate_func=there_and_back).scale(s)


def cadeado(c, s=0.22, cor=LMAG):
    corpo = RoundedRectangle(corner_radius=0.03, width=s, height=0.8 * s).move_to(c).set_fill(cor, 0.9).set_stroke(cor, 1.5)
    arco = Arc(radius=0.32 * s, start_angle=0, angle=PI).move_to(c + UP * 0.52 * s).set_stroke(cor, 2.4)
    return VGroup(corpo, arco)


def _sim_hud(sim, cor):
    """Símbolo do HUD com a cor de cada glifo (COR OPERADOR): dI/dt → d, t, barra brancos; v_θ → v na cor da grandeza e θ âmbar."""
    if "theta" in sim:
        m = T(sim, 36, cor)
        m[0][-1].set_color(ANG)
        return m
    return T(sim, 36, None if "/" in sim else cor)


HUD_SLOTS = (1.55, 0.05, -1.45)


def hud(sim, fn, casas, unidade, cor, slot=0, ind=None, faixa=(0.0, 1.0), trava=None, x=None, unid_baixo=False):
    """Mostrador HUD: faixa vertical fina sem caixa à direita da mesa (fora da CONTA): símbolo + unidade pequenos (DIM), valor grande
    na cor da grandeza (MathTex 40) e um indicador: 'arco' (ponteiro), 'barra' ou None; `trava()` → True mostra um cadeado ao lado."""
    x0 = HUD_X[0] if x is None else x
    y = HUD_SLOTS[slot] if isinstance(slot, int) else slot

    def f():
        v = fn()
        if unid_baixo:                          # símbolo largo (dI/dt): a unidade desce para a linha de baixo (não invade a calha da CONTA)
            top = _sim_hud(sim, cor).move_to(P3(x0, y + 0.42), aligned_edge=LEFT)      # v5 COR OPERADOR: dI/dt e v_θ levam a cor de cada glifo (d, t, / brancos; θ âmbar)
        else:
            top = linha_base([_sim_hud(sim, cor), txt(unidade, 24, color=DIM)], 0.12).move_to(P3(x0, y + 0.42), aligned_edge=LEFT)
        val = T(num(v, casas), 42, cor).move_to(P3(x0, y - 0.08), aligned_edge=LEFT)
        g = VGroup(top, val)
        if unid_baixo:
            g.add(txt(unidade, 24, color=DIM).move_to(P3(x0, y - 0.52), aligned_edge=LEFT))
        u = min(1.0, max(0.0, (v - faixa[0]) / (faixa[1] - faixa[0])))
        if ind == "barra":
            fundo = Line(P3(x0, y - 0.55), P3(x0 + 1.1, y - 0.55)).set_stroke(DIM, 5, opacity=0.35)
            g.add(fundo, Line(P3(x0, y - 0.55), P3(x0 + max(0.02, 1.1 * u), y - 0.55)).set_stroke(cor, 5))
        elif ind == "arco":
            c = P3(x0 + 0.30, y - 0.72)
            g.add(Arc(radius=0.24, start_angle=PI, angle=-PI, arc_center=c).set_stroke(DIM, 4, opacity=0.35),
                  Arc(radius=0.24, start_angle=PI, angle=-PI * max(0.01, u), arc_center=c).set_stroke(cor, 4),
                  Line(c, c + 0.21 * np.array([math.cos(PI - PI * u), math.sin(PI - PI * u), 0])).set_stroke(WHITE_, 2.5), Dot(c, radius=0.035, color=WHITE_))
        if trava is not None and trava():
            g.add(cadeado(P3(val.get_right()[0] + 0.25, val.get_y()), 0.2, cor))
        for m in g.get_family():
            m._hud = True
        return g.set_z_index(30)
    return vivo(f)


def area_lab(pts, op=0.40, cor=GEO, z=5):
    """Área varrida: polígono a partir de O (pts[0]) com degradê radial (≈ op no O → 0,35·op na borda) e borda fina."""
    pts = [np.asarray(p, float) for p in pts]
    if len(pts) < 3:
        return VGroup()
    o = pts[0]
    g = VGroup(Polygon(*pts).set_fill(cor, 0.38 * op).set_stroke(cor, 1.4, opacity=0.85))
    for k, f in enumerate((0.72, 0.45)):
        g.add(Polygon(*[o + f * (p - o) for p in pts]).set_fill(cor, 0.30 * op).set_stroke(width=0))
    return g.set_z_index(z)


def chips(textos, cor=CYAN, size=24, buff=0.18):
    """Selo em chips pequenos lado a lado, numa linha."""
    out = VGroup()
    for t_ in textos:
        t = txt(t_, size, bold=False, color=cor) if isinstance(t_, str) else t_
        r = RoundedRectangle(corner_radius=0.08, width=t.width + 0.22, height=t.height + 0.2).move_to(t).set_fill(PANEL, 0.85).set_stroke(cor, 1.4)
        r._fundo = True
        ch = VGroup(r, t)
        ch._chip = True
        out.add(ch)
    out._chip = True
    return out.arrange(RIGHT, buff=buff).set_z_index(35)


def grafico_lab(x0, y0, larg, alt, xr, yr, xt, yt, xlab, ylab, cor_eixo=GEO, rotx=None, roty=None):
    """Gráfico HUD: grade fina (DIM 12 %), eixos com marcas e números. Devolve (grupo, c2p) com c2p(x, y) → ponto Manim.
    xt/yt: listas de marcas; rotx/roty: textos dos números (padrão: num)."""
    def c2p(x, y):
        return P3(x0 + (x - xr[0]) / (xr[1] - xr[0]) * larg, y0 + (y - yr[0]) / (yr[1] - yr[0]) * alt)
    g = VGroup()
    for v in xt:
        g.add(Line(c2p(v, yr[0]), c2p(v, yr[1])).set_stroke(DIM, 1.2, opacity=0.12))
    for v in yt:
        g.add(Line(c2p(xr[0], v), c2p(xr[1], v)).set_stroke(DIM, 1.2, opacity=0.12))
    y_e = 0 if yr[0] < 0 <= yr[1] else yr[0]
    fim_x = c2p(xr[1], y_e) + RIGHT * 0.25
    ex = seta(c2p(xr[0], y_e), fim_x, cor_eixo, 3, tip=0.14)
    xe = xr[0] if xr[0] >= 0 else 0
    fim_y = c2p(xe, yr[1]) + UP * 0.25
    if yr[1] <= 0:
        fim_y = c2p(xe, yr[0]) + DOWN * 0.25
        ey = seta(c2p(xe, yr[1]), fim_y, cor_eixo, 3, tip=0.14)
    else:
        ey = seta(c2p(xe, yr[0]), fim_y, cor_eixo, 3, tip=0.14)
    g.add(ex, ey)
    y_eixo = y_e
    for k, v in enumerate(xt):
        g.add(Line(c2p(v, y_eixo) + DOWN * 0.06, c2p(v, y_eixo) + UP * 0.06).set_stroke(cor_eixo, 2))
        s_ = rotx[k] if rotx else num(v, 1)
        lab = T(s_, 36, WHITE_)
        lab.next_to(c2p(v, y_eixo), UP if yr[0] < 0 else DOWN, buff=0.12)
        g.add(lab)
    for k, v in enumerate(yt):
        g.add(Line(c2p(xr[0], v) + LEFT * 0.06, c2p(xr[0], v) + RIGHT * 0.06).set_stroke(cor_eixo, 2))
        s_ = roty[k] if roty else num(v, 2)
        g.add(T(s_, 36, WHITE_).next_to(c2p(xr[0], v), LEFT, buff=0.12))
    g.add(xlab.next_to(fim_x, UP if yr[0] < 0 else DOWN, buff=0.12), ylab.next_to(fim_y, RIGHT, buff=0.12))
    return g.set_z_index(14), c2p


def curva_lab(c2p, f, a, b, cor, n=80, w=5):
    xs = np.linspace(a, b, n)
    c = VMobject().set_points_smoothly([c2p(x, f(x)) for x in xs]).set_stroke(cor, w)
    gl = c.copy().set_stroke(cor, 14, opacity=0.2)
    return VGroup(gl, c).set_z_index(15)


def ponto_vivo(p, cor):
    return VGroup(Dot(p, radius=0.11, color=cor).set_opacity(0.25), Dot(p, radius=0.06, color=cor)).set_z_index(16)


def varredura(cena, rt=0.5):
    """Transição de bloco: linha fina ciano-claro passando da esquerda para a direita."""
    vt = ValueTracker(-8.2)
    ln = always_redraw(lambda: VGroup(Line(P3(vt.get_value(), -4.5), P3(vt.get_value(), 4.5)).set_stroke("#BFF3FF", 2.5, opacity=0.85),
                                      Line(P3(vt.get_value(), -4.5), P3(vt.get_value(), 4.5)).set_stroke("#BFF3FF", 16, opacity=0.12)).set_z_index(60))
    ln._fundo = True
    cena.add(ln)
    return vt, ln

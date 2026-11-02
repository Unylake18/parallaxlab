"""yt_0018 v3 — camada sobre prob.py (handoff v2 §2: G23–G28; v3 §4: zonas 16×9, Pilha em blocos, selo sequencial).

Zonas (v3 §4, quadro 16×9): canto x < −1, y > 3,05 · chip do checklist x −7,3…−2,5, y 2,60…3,00 · faixa de selo (uma só) x 0,7…7,3, y 2,85…3,50 ·
Pilha x 0,7…7,3, y −3,65…2,60 · ESQUEMA x −7,3…0,2, y −3,65…2,50.
Pilha (v3 §4): P1 uma linha que começa com "=", "⇒" ou "→" é FILHA da de cima; a Pilha tira blocos inteiros (mãe + filhas), do mais antigo
para o mais novo; se a mãe sai e a filha fica, a filha ganha o lado esquerdo antes (`_lhs`, TransformMatchingShapes) · P2 as filhas alinham o
"=" com o "=" da mãe · P3 caixa sempre com lado esquerdo. Troca de selo: o velho sai em 0,25 s e só então o novo entra (nunca dois).
G27 `rotulo()` testa colisão antes de pôr um rótulo. G23 `passo()` (glyph map numa linha nova) e `voa()` (TransformFromCopy do desenho para a
conta); G24 v3: cada par símbolo → número confere a cor de origem (`_origem`). PAUSAS: hold longo vira destaque do termo em foco.
"""
from prob import *  # noqa: F401,F403

X_CONTA, TOPO_PILHA, BASE_PILHA = 0.7, 2.60, -3.65
LARG_CONTA = 6.6
Y_SELO_TOPO, H_SELO = 3.55, 0.85                 # faixa de selo: duas linhas de 24 pt ao lado da etiqueta (topo 3,55, base ≥ 2,75)
FILHAS = ("=", r"\Rightarrow", r"\rightarrow", r"\to")


def _desc(m):
    """Texto curto que identifica uma linha (para o log da auditoria)."""
    for x in m.get_family():
        if getattr(x, "tex_string", None):
            return x.tex_string[:50]
        if getattr(x, "text", None):
            return str(x.text)[:50]
    return type(m).__name__


def eh_numero(t):
    """Parte de TeX que é só número (com sinal, vírgula, parênteses, ·, fração numérica e unidade)."""
    if not t:
        return False
    import re as _r
    u = _r.sub(r"\\(mathrm|tfrac|frac|cdot|,|;|\ |big|left|right)", " ", t)
    u = _r.sub(r"\\ *\{?[a-zA-Z/^0-9]*\}?", " ", u) if "mathrm" in t else u
    u = _r.sub(r"[{}()\s]", "", u)
    u = _r.sub(r"(kg|m/s\^?2?|m|cm|s|J|N|g)$", "", u)
    return bool(_r.fullmatch(r"[-−+]?[0-9.,]+", u))


def _tex0(m):
    """A primeira MathTex de uma linha (a própria, a de dentro da caixa ou a primeira de uma linha mista)."""
    for x in m.get_family():
        if isinstance(x, MathTex):
            return x
    return None


def eh_filha(m):
    t = _tex0(m)
    if t is None or (isinstance(m, VGroup) and not isinstance(m, MathTex) and m.submobjects and m[0] is not t
                     and not isinstance(m[0], RoundedRectangle)):
        return False
    return t.get_tex_string().strip().startswith(FILHAS)


def x_igual(m):
    """x do primeiro "=" (ou ⇒, ≤) de uma linha montada por M()/eqf() (partes conhecidas); None se não achar."""
    t = _tex0(m)
    if t is None or not hasattr(t, "_partes"):
        return None
    k = 0
    for tx_, _ in t._partes:
        if tx_.strip() in ("=", r"\le", r"\Rightarrow", r"\approx"):
            return t[0][k].get_center()[0]
        k += ng(tx_)
    return None


class Pilha:
    def __init__(self, cena, x0=X_CONTA, topo=TOPO_PILHA, base=BASE_PILHA, buff=0.26):
        self.cena, self.x0, self.topo, self.base, self.buff = cena, x0, topo, base, buff
        self.linhas = []                                  # [(mob, dx)]

    def _y_topo(self):
        return self.topo if not self.linhas else self.linhas[-1][0].get_bottom()[1] - self.buff

    def blocos(self):
        """Índices agrupados em blocos: uma mãe e as filhas que vêm logo embaixo (P1)."""
        out = []
        for i, (l, _) in enumerate(self.linhas):
            if out and eh_filha(l):
                out[-1].append(i)
            else:
                out.append([i])
        return out

    def _sai_blocos(self, ficar, manter):
        """Separa (ficam, saem, herdam) tirando blocos inteiros dos mais antigos até `ficar(ficam)` ser verdade. Bloco com linha em
        `manter`: se a mãe está em `manter`, o bloco fica; se só uma filha está, ela herda o lado esquerdo e o resto do bloco sai."""
        ficam, saem, herdam = list(self.linhas), [], []
        for bl in self.blocos():
            if ficar(ficam):
                break
            itens = [self.linhas[i] for i in bl]
            mant = [it for it in itens if it[0] in manter]
            if not mant:
                for it in itens:
                    ficam.remove(it)
                    saem.append(it)
            elif itens[0] in mant or not all(getattr(it[0], "_lhs", None) for it in mant):
                continue
            else:
                for it in itens:
                    if it in mant:
                        herdam.append(it)
                    else:
                        ficam.remove(it)
                        saem.append(it)
        return ficam, saem, herdam

    def _reflow(self, ficam, rt, anims=()):
        y, mov = self.topo, list(anims)
        for l, d in ficam:
            alvo = P3(self.x0 + d + l.width / 2, y - l.height / 2)
            if np.linalg.norm(l.get_center() - alvo) > 1e-3:
                mov.append(l.animate.move_to(alvo))
            y -= l.height + self.buff
        if mov:
            self.cena.play(*mov, run_time=rt)

    def _herda(self, herdam, rt=0.6):
        """A filha que fica ganha o lado esquerdo (e a caixa) antes de a mãe sair (P1)."""
        for it in herdam:
            l, d = it
            nova = l._lhs()
            nova.move_to(P3(self.x0 + nova.width / 2, l.get_y()))
            nt = _tex0(nova)
            anims = [TransformMatchingShapes(l, nt)]
            resto = [x for x in nova.submobjects if x is not nt] if isinstance(nova, VGroup) and nt in nova.submobjects else []
            anims += [FadeIn(x) for x in resto]
            self.cena.play(*anims, run_time=rt)
            self.cena.remove(nt, *resto)
            self.cena.add(nova)
            k = self.linhas.index(it)
            self.linhas[k] = (nova, 0.0)
            l._herdeira = nova

    def poe(self, m, dx=0.0, rt=0.35, manter=()):
        """Posiciona m na próxima vaga (o chamador anima a entrada) e registra a linha. Filha (P1): alinha o "=" com o da mãe (P2)."""
        if m.width > LARG_CONTA - dx + 0.01:
            print(f"[audit] {self.cena.clk.get_value():7.1f}s FORA DA MARGEM linha da pilha larga demais ({m.width:.2f}) {_desc(m)}")
        h_ = m.height
        if self._y_topo() - h_ < self.base:
            ficam, saem, herdam = self._sai_blocos(lambda f: self.topo - sum(l.height + self.buff for l, _ in f) - h_ >= self.base, manter)
            if herdam:
                self._herda(herdam)
                ficam = [it for it in self.linhas if it not in saem]
            if saem:
                self.cena.play(*[FadeOut(l) for l, _ in saem], run_time=rt * 0.6)
                for l, _ in saem:
                    self.cena.remove(l)
                    if hasattr(self.cena, "limpa_pecas"):
                        self.cena.limpa_pecas(l)
            self.linhas = ficam
            self._reflow(ficam, rt)
        y = self._y_topo()
        if eh_filha(m) and self.linhas:
            mae = next((l for l, _ in reversed(self.linhas) if not eh_filha(l)), None)
            m.move_to(P3(self.x0 + m.width / 2, y - m.height / 2))
            xm, xf = (x_igual(mae) if mae is not None else None), x_igual(m)          # depois de posicionar (P2: "=" embaixo do "=")
            if xm is not None and xf is not None:
                m.shift((xm - xf) * RIGHT)
            elif dx:
                m.shift(dx * RIGHT)
            if m.get_left()[0] < self.x0:                                            # v4 CALHA: a filha nunca começa antes da borda da Pilha
                m.shift((self.x0 - m.get_left()[0]) * RIGHT)
            dx = m.get_left()[0] - self.x0
        else:
            m.move_to(P3(self.x0 + dx + m.width / 2, y - m.height / 2))
        self.linhas.append((m, dx))
        return m

    def tira(self, *ms):
        self.linhas = [(l, d) for l, d in self.linhas if l not in ms]

    def limpa(self, rt=0.4, anims=()):
        ms = [l for l, _ in self.linhas]
        if ms or anims:
            self.cena.play(*[FadeOut(l) for l in ms], *anims, run_time=rt)
            self.cena.remove(*ms)
            for l in ms:
                self.cena.limpa_pecas(l)
        self.linhas = []

    def so(self, *keep, anims=(), rt=0.5):
        """Tira da tela todas as linhas menos `keep`, que sobem para o topo (na ordem em que estavam). Filha mantida sem a mãe herda o
        lado esquerdo antes (P1); sem `_lhs`, a mãe fica junto."""
        keep = list(keep)
        for bl in self.blocos():
            itens = [self.linhas[i][0] for i in bl]
            if any(l in keep for l in itens[1:]) and itens[0] not in keep and not all(getattr(l, "_lhs", None) for l in itens[1:] if l in keep):
                keep.append(itens[0])
        herdam = []
        for bl in self.blocos():
            itens = [self.linhas[i] for i in bl]
            if itens[0][0] not in keep:
                herdam += [it for it in itens[1:] if it[0] in keep]
        if herdam:
            self._herda(herdam)
            keep = [getattr(l, "_herdeira", l) for l in keep]
        saem = [l for l, _ in self.linhas if l not in keep]
        ficam = [(l, d) for l, d in self.linhas if l in keep]
        if saem:
            self.cena.play(*[FadeOut(l) for l in saem], run_time=min(0.3, rt))
            self.cena.remove(*saem)
            for l in saem:
                self.cena.limpa_pecas(l)
        self.linhas = ficam
        self._reflow(ficam, max(0.2, rt - 0.3), anims)
        return [getattr(l, "_herdeira", l) for l in keep]

    def ultima(self):
        return self.linhas[-1][0] if self.linhas else None


def _n_gl(m):
    return len([x for x in m.family_members_with_points() if x.points.size])


def troca_anim(src, dst, rate=rush_from, corte=0.45, desvio=None):
    """v4 TRÂNSITO: troca de glifos que não casam (m₁ → 1, 1600 → ∝ 1600). O `src` viaja até o lugar do `dst` sumindo na primeira
    metade e o `dst` acende parado na vaga na segunda: nunca dois glifos diferentes visíveis um sobre o outro (sem sopa)."""
    a0 = src.copy()
    c0, c1 = src.get_center(), dst.get_center()
    d_ = c1 - c0
    dv = np.zeros(3) if desvio is None else np.asarray(desvio, float)          # deslocamento no meio do caminho (arco por fora)

    def upd(m, t):
        u = rate(t)
        p = c0 + d_ * u + dv * 4 * u * (1 - u)
        m.become(a0).move_to(p)
        escala_op(m, max(0.0, 1.0 - t / corte))
    return AnimationGroup(UpdateFromAlphaFunc(src, upd), FadeIn(dst, rate_func=lambda t: min(1.0, max(0.0, (t - corte) / (1 - corte)))))


def dim_origens(janelas, total, nivel=0.35):
    """v5 G31: enquanto uma cópia viaja, a origem fica a 35% (volta a 100% nos últimos 20% da janela). `janelas`: [(origem, t0, t1)] em segundos
    dentro de uma animação de duração `total`; a mesma origem em vários voos vira uma janela só (da primeira partida à última chegada)."""
    por = {}
    for a, t0, t1 in janelas:
        fam = [x for x in a.family_members_with_points() if isinstance(x, VMobject)]
        for x in fam:                                           # chave por glifo: grupos novos (mp/gl) com os mesmos glifos se fundem
            e = por.setdefault(id(x), [x, x.get_fill_opacity(), x.get_stroke_opacity(), t0, t1, t1 - t0])
            if t1 > e[4]:
                e[5] = t1 - t0                                  # a rampa de volta mede 20% do ÚLTIMO voo
            e[3], e[4] = min(e[3], t0), max(e[4], t1)
    itens = list(por.values())

    def upd(m, u):
        ts = u * total
        for x, f, s, t0, t1, dl in itens:
            ro = min(0.2 * dl, 0.1)                                 # a origem volta no último décimo (a auditoria ignora os últimos 0,1 s do voo)
            if ts < t0 or ts > t1:
                k = 1.0
            elif ts < t0 + 0.07:
                k = 1.0 - (1.0 - nivel) * (ts - t0) / 0.07
            elif ts > t1 - ro:
                k = nivel + (1.0 - nivel) * min(1.0, (ts - (t1 - ro)) / max(ro, 1e-6))
            else:
                k = nivel
            x.set_fill(opacity=f * k, family=False)
            x.set_stroke(opacity=s * k, family=False)
    return UpdateFromAlphaFunc(ValueTracker(0.0), upd, rate_func=linear, run_time=total)       # o animado é um rastreador: a origem não entra na cena


def Morph4(a, b, **kw):
    """Transformador padrão do passo (TransformByGlyphMap): grupos com o mesmo número de glifos fazem o morph; com número diferente, a troca
    sem sopa (troca_anim)."""
    if _n_gl(a) == _n_gl(b):
        return ReplacementTransform(a, b, **kw)
    return troca_anim(a, b, rate=smooth)


def linha_m(*itens, buff=0.18, size=28):
    """Linha mista da CONTA: palavras em txt() (Space Grotesk, G24), símbolos em MathTex."""
    return VGroup(*[txt(i, size) if isinstance(i, str) else i for i in itens]).arrange(RIGHT, buff=buff)


def caixa_l(m, cor=BLUE_L):
    """Resultado em PANEL como uma linha só da pilha (a caixa faz parte da linha). P3: nunca uma caixa que começa com "="."""
    t = _tex0(m)
    if t is not None and t.get_tex_string().strip().startswith(FILHAS):
        print(f"[audit] CAIXA SEM LADO ESQUERDO '{t.get_tex_string()[:30]}'")
    return VGroup(caixa(m, cor), m)


class Prob2(Prob):
    def setup_base(self, cap=None, selo=None):
        super().setup_base(cap, selo)
        self.pilha = Pilha(self)
        self.foco = None
        self.chk = None
        self._orig_n = [0, 0]

    def _selo_mob(self, tag, corpo, cor=CYAN, borda=BLUE_L, size=24, wmax=LARG_CONTA):
        """Selo da faixa (v3 §4): altura ≤ 0,65. A etiqueta abre a primeira linha e o texto continua nela e na de baixo, na largura toda
        (no máximo duas linhas; quebra por palavras, o "·" vai junto)."""
        t = txt(tag, 24, color=cor, bold=True)
        brutas = corpo if isinstance(corpo, (list, tuple)) else ([corpo] if corpo else [])
        if brutas and all(isinstance(l, str) for l in brutas):
            brutas = [" ".join(brutas)]
        larg1, larg2 = wmax - 0.24 - t.width - 0.18, wmax - 0.24
        linhas = []
        for l in brutas:
            if not isinstance(l, str):
                linhas.append(l)
                continue
            if tx(l, size).width > larg1 and tx(l, size).width <= larg2 and larg1 < 2.2:      # etiqueta longa: o texto inteiro vai para a linha de baixo
                linhas += [None, l]
                continue
            pal = l.replace(" · ", " ·· ").split(" ")
            atual, lim = "", larg1
            for w in pal:
                w = "·" if w == "··" else w
                c2 = (atual + " " + w) if atual else w
                if atual and tx(c2, size).width > lim:
                    linhas.append(atual.rstrip(" ·"))
                    atual, lim = ("" if w == "·" else w), larg2
                else:
                    atual = c2
            if atual:
                linhas.append(atual.rstrip(" ·"))
        mk = lambda l: tx(l, size) if isinstance(l, str) else VGroup(*[tx(i, size) if isinstance(i, str) else i for i in l]).arrange(RIGHT, buff=0.1)
        if linhas:
            l1 = VGroup(t, mk(linhas[0])).arrange(RIGHT, buff=0.18, aligned_edge=DOWN) if linhas[0] is not None else VGroup(t)
            g = VGroup(l1, *[mk(l) for l in linhas[1:]]).arrange(DOWN, buff=0.06, aligned_edge=LEFT)
        else:
            g = VGroup(t)
        bx = RoundedRectangle(corner_radius=0.08, width=g.width + 0.24, height=g.height + 0.12).move_to(g).set_fill(PANEL, 0.9).set_stroke(borda, 1.8)
        bx._fundo = bx._caixa = True
        s = VGroup(bx, g).set_z_index(36)
        s._selo = "faixa"
        if s.height > H_SELO + 0.01 or s.width > wmax + 0.01:
            print(f"[audit] FORA DA ZONA selo '{tag}' grande demais ({s.width:.2f} × {s.height:.2f})")
        return s

    # ── selo único na faixa (v3 §4): o velho sai em 0,25 s e só então o novo entra ──
    def selo(self, tag, corpo, cor=CYAN, borda=BLUE_L, rt=0.5, x0=X_CONTA):
        novo = self._selo_mob(tag, corpo, cor, borda)
        novo.move_to(P3(x0 + novo.width / 2, Y_SELO_TOPO - novo.height / 2))
        velho = self.s1
        if velho is not None:
            self.play(FadeOut(velho), run_time=0.25)
            self.remove(velho)
        self.s1 = None
        topo = min(TOPO_PILHA, novo.get_bottom()[1] - 0.15)                 # selo de três linhas: a Pilha desce junto (nunca um por cima do outro)
        mov = []
        if abs(topo - self.pilha.topo) > 1e-3:
            self.pilha.topo = topo
            y = topo
            for l, d in self.pilha.linhas:
                mov.append(l.animate.move_to(P3(self.pilha.x0 + d + l.width / 2, y - l.height / 2)))
                y -= l.height + self.pilha.buff
        self.play(FadeIn(novo, shift=0.06 * DOWN), *mov, run_time=max(0.25, rt - (0.25 if velho is not None else 0.0)))
        self.s1 = novo
        return novo

    def selo_reflow(self, novo):
        return novo

    def hip(self, corpo, rt=0.5):
        tag = "HIPÓTESES" if (not isinstance(corpo, str) or "·" in corpo) else "HIPÓTESE"
        return self.selo(tag, corpo, cor=CYAN, borda=GEO, rt=rt)

    def hip_sai(self, *anims, rt=0.4):
        if anims:
            self.play(*anims, run_time=rt)

    def sem_selo(self, rt=0.35):
        if self.s1 is not None:
            self.play(FadeOut(self.s1), run_time=rt)
            self.remove(self.s1)
            self.s1 = None

    def referencial(self, nome, pos=None, rt=0.5, anims=()):
        """Selo VISTO DA … no alto do ESQUEMA (encostado à esquerda, topo em y = 2,50); troca sequencial (nunca dois)."""
        novo = None
        if nome:
            t = txt(f"VISTO {nome}", 24, bold=True)
            bx = RoundedRectangle(corner_radius=0.1, width=t.width + 0.3, height=t.height + 0.18).move_to(t).set_fill(PANEL, 0.9).set_stroke(VEL, 2)
            bx._fundo = True
            novo = VGroup(bx, t).set_z_index(36)
            novo._selo = "ref"
            novo.move_to(P3(-7.25 + novo.width / 2, (pos if isinstance(pos, (int, float)) else 2.50 - novo.height / 2)))
        velho = self.ref_mob
        self.ref_mob, self.ref_atual = novo, nome
        ani = list(anims)
        if velho is not None:
            self.play(FadeOut(velho), *ani, run_time=0.25 if novo is not None else rt)
            self.remove(velho)
            ani = []
        if novo is not None:
            self.play(FadeIn(novo, shift=0.06 * DOWN), *ani, run_time=max(0.25, rt - (0.25 if velho is not None else 0.0)))
        elif ani:
            self.play(*ani, run_time=rt)
        return novo

    # ── chip da pergunta que decide (G26; v3 §4: x −7,3…−2,5, y 2,60…3,00, ~4 s; duas perguntas em sequência) ──
    def chip(self, *ns, dur_=4.2):
        partes = []
        for n in ns:
            k = n - 1
            frase = Checklist.LONGAS[k]
            l = VGroup(Checklist.icone(k, 0.8), txt(f"{n}.", 24, color=CYAN, bold=True), txt(frase, 24, bold=True)).arrange(RIGHT, buff=0.12)
            if l.width > 4.5:
                l = VGroup(Checklist.icone(k, 0.8), txt(f"{n}.", 24, color=CYAN, bold=True), txt(Checklist.CURTAS[k], 24, bold=True)).arrange(RIGHT, buff=0.12)
            bx = RoundedRectangle(corner_radius=0.08, width=l.width + 0.26, height=0.38).move_to(l).set_fill(PANEL, 0.92).set_stroke(CYAN, 1.6)
            bx._fundo = bx._caixa = True
            g0 = VGroup(bx, l).set_z_index(39)
            g0.move_to(P3(-7.3 + g0.width / 2, 2.80))
            partes.append(g0)
        t0 = self.clk.get_value()
        cada = dur_ / len(partes)

        def f():
            t = self.clk.get_value() - t0
            k = min(len(partes) - 1, int(t // cada))
            tl = t - k * cada
            o = min(1.0, max(0.0, tl / 0.3)) * min(1.0, max(0.0, (cada - tl) / 0.3))
            return escala_op(partes[k].copy(), o) if o > 0.01 and t < dur_ else VGroup()
        v = vivo(f)
        v._chip = True
        self.add(v)
        return v

    # ── rótulo com teste de colisão (G27) ──
    def _obstaculos(self, ignorar=()):
        pts, caixas = [], []
        ig = set(id(x) for m in ignorar for x in m.get_family())
        fx = self.fixos()

        def walk(m):
            if id(m) in ig or isinstance(m, (ImageMobject, Fundo3D)):
                return
            if isinstance(m, (Text, SingleStringMathTex)) or getattr(m, "_caixa", False):
                try:
                    o = max(max(x.get_fill_opacity(), x.get_stroke_opacity()) for x in m.family_members_with_points())
                except Exception:
                    o = 1.0
                if o > 0.08:
                    (x0, y0, _), (x1, y1, _) = m.get_critical_point(DL), m.get_critical_point(UR)
                    caixas.append((x0, y0, x1, y1))
                return
            if getattr(m, "_fundo", False):
                return
            if isinstance(m, VMobject) and m.points.size and not m.submobjects:
                try:
                    if max(m.get_fill_opacity(), m.get_stroke_opacity()) > 0.15:
                        pts.append(m.points)
                except Exception:
                    pass
                return
            for s_ in m.submobjects:
                walk(s_)
        for top in self.mobjects:
            if top not in fx and top is not self.clk:
                walk(top)
        for fn in self._futuros:
            try:
                q = np.asarray(fn(), float).reshape(-1, 3)
                if len(q):
                    pts.append(q)
            except Exception:
                pass
        for q in getattr(self, "_evitar", []):
            pts.append(np.asarray(q() if callable(q) else q, float).reshape(-1, 3))
        return (np.vstack(pts) if pts else np.zeros((0, 3))), caixas

    def livre(self, m, extra_pts=None, ignorar=(), pad=0.07, zona=(-7.45, 7.45, -4.0, 3.3)):
        P_, cx = self._obstaculos((*ignorar, m))
        if extra_pts is not None and len(extra_pts):
            P_ = np.vstack([P_, np.asarray(extra_pts, float).reshape(-1, 3)])
        (x0, y0, _), (x1, y1, _) = m.get_critical_point(DL), m.get_critical_point(UR)
        x0, y0, x1, y1 = x0 - pad, y0 - pad, x1 + pad, y1 + pad
        if x0 < zona[0] or x1 > zona[1] or y0 < zona[2] or y1 > zona[3]:
            return False
        if len(P_) and ((P_[:, 0] > x0) & (P_[:, 0] < x1) & (P_[:, 1] > y0) & (P_[:, 1] < y1)).any():
            return False
        return not any(min(x1, b[2]) - max(x0, b[0]) > 0 and min(y1, b[3]) - max(y0, b[1]) > 0 for b in cx)

    def rotulo(self, m, alvo, lados=(UP, DOWN, RIGHT, LEFT, UR, UL, DR, DL), buffs=(0.14, 0.3, 0.5), extra_pts=None, ignorar=(),
               zona=(-7.45, 0.45, -4.0, 3.3), chamada=True):
        ref = alvo if isinstance(alvo, Mobject) else Dot(np.asarray(alvo, float), radius=0.001)
        ig = (*ignorar, ref)
        for b in buffs:
            for l in lados:
                m.next_to(ref, l, buff=b)
                if self.livre(m, extra_pts, ignorar=ig, zona=zona):
                    return VGroup(m)
        for b in (0.8, 1.2, 1.6):
            for l in lados:
                m.next_to(ref, l, buff=b)
                if self.livre(m, extra_pts, ignorar=ig, zona=zona):
                    if not chamada:
                        return VGroup(m)
                    a = ref.get_center()
                    q = m.get_center()
                    u = (a - q) / max(np.linalg.norm(a - q), 1e-6)
                    ini = q + u * (0.5 * min(m.width, m.height) + 0.08)
                    return VGroup(m, Line(ini, a - u * 0.08).set_stroke(WHITE_, 1.4, opacity=0.6))
        m.next_to(ref, lados[0], buff=buffs[0])
        print(f"[audit] {self.nq / FPS:7.1f}s SOBREPOSICAO rótulo sem lugar livre")
        return VGroup(m)

    # ── passos da conta (G23) ──
    def _linha_de(self, m):
        """A linha da Pilha que contém m (ou o próprio m)."""
        fs = [id(x) for x in (self._folhas(m) or [m])]                 # m costuma ser um VGroup novo (mp/gl) com glifos da linha
        for l, _ in self.pilha.linhas:
            fam = set(id(x) for x in l.get_family())
            if any(x is m for x in l.get_family()) or any(i in fam for i in fs):   # any: o Transform pendura cópias vazias no grupo de destino
                return l
        return m

    def _folhas(self, m):
        return [x for x in m.get_family() if isinstance(x, VMobject) and x.points.size]

    def _sobras(self, tops_antes, manter):
        """v4: tira da cena os grupos que a própria animação pendurou no topo (o Group do LaggedStart/TBGM, cópias e fantasmas da troca),
        menos as linhas e o que o chamador quer manter."""
        manter = set(id(m) for m in manter)
        linhas = set(id(l) for l, _ in self.pilha.linhas)
        fam = set(id(x) for l, _ in self.pilha.linhas for x in l.get_family())
        na_cena = set(id(m) for m in self.mobjects)
        fam_inteira = set(id(x) for l, _ in self.pilha.linhas if id(l) in na_cena for x in l.get_family())
        for m in list(self.mobjects):
            if id(m) in tops_antes or id(m) in manter or id(m) in linhas or m in self.fixos() or isinstance(m, ValueTracker):
                continue
            fs = self._folhas(m)
            if fs and all(id(x) in fam for x in fs) and not all(id(x) in fam_inteira for x in fs):   # pedaço de uma linha que ainda vai completar
                continue
            self.remove(m)

    def _assenta(self, anims, alvos, revelados=()):
        """Depois de um play: tira as cópias (TransformFromCopy) e os grupos parciais; uma linha só entra inteira quando todos os glifos dela
        já foram revelados (senão ficam só as peças reveladas). Nada do original fica solto por cima (G23.5)."""
        if not hasattr(self, "_mostrados"):
            self._mostrados = {}
        fam = set(id(x) for a in alvos for x in a.get_family())
        pecas = list(revelados)
        for an_ in anims:
            m = getattr(an_, "mobject", None)
            if m is None:
                continue
            if isinstance(an_, TransformFromCopy):           # no Manim o TransformFromCopy anima o próprio destino (.mobject); a origem fica onde está
                self.remove(m)
                pecas.append(m)
                continue
            fs = self._folhas(m)
            if fs and all(id(x) in fam for x in fs) and m not in alvos:
                self.remove(m)
                pecas.append(m)
        for a in alvos:
            vis = self._mostrados.setdefault(id(a), set())
            for pc in pecas:
                for x in self._folhas(pc):
                    if any(x is y for y in a.get_family()):
                        vis.add(id(x))
            todas = self._folhas(a)
            if all(id(x) in vis for x in todas):
                self.limpa_pecas(a)
                self.add(a)
            else:
                for pc in pecas:
                    if any(x is y for x in self._folhas(pc) for y in a.get_family()):
                        self.add(pc)
        # glifos soltos no topo da cena que já fazem parte de uma linha inteira na cena (sobra de Transform/TBGM): desenhados duas vezes
        topo = set(id(m) for m in self.mobjects)
        for l, _ in self.pilha.linhas:
            if id(l) in topo:
                fam = set(id(x) for x in l.get_family() if x is not l)
                self.mobjects = [m for m in self.mobjects if id(m) not in fam]     # sem Scene.remove: ele quebraria a linha em pedaços

    def limpa_pecas(self, linha):
        """Tira da cena os grupos soltos que só mostram pedaços de `linha`."""
        fam = set(id(x) for x in linha.get_family())
        for m in list(self.mobjects):
            if m is linha:
                continue
            fs = self._folhas(m)
            if fs and all(id(x) in fam for x in fs):
                self.remove(m)

    def relatorio(self):
        super().relatorio()
        if AUDITORIA:
            print(f"[cor] origem (G24 v3): {self._orig_n[0]} pares conferidos; fora da cor de origem: {self._orig_n[1]}")

    def _cor1(self, ms):
        """Cor única de um grupo de glifos (None se misturado ou vazio)."""
        cs = set()
        for x in ms:
            for y in x.family_members_with_points():
                cs.add(ManimColor(y.get_fill_color()).to_hex().upper())
        return cs.pop() if len(cs) == 1 else None

    def _origem(self, a, b, ctx="", numero=None):
        """G24 v3: o número que entra herda a cor do símbolo que ele substitui (a origem). Só número: derivação (F → P, v² → p²) não conta."""
        if numero is None:
            numero = eh_numero(getattr(b, "_tex", None))
        if not numero:
            return
        ca, cb = self._cor1([a]), self._cor1([b])
        if ca is None or cb is None:
            return
        self._orig_n[0] += 1
        if ca != cb:
            self._orig_n[1] += 1
            print(f"[audit] {self.clk.get_value():7.1f}s COR POR TOKEN origem {ca} → {cb} ({ctx})")

    def passo(self, src, dst, *mapas, rt=1.2, extra=(), origem=True):
        for a_, b_ in (mapas if origem else ()):
            if len(a_) and len(b_) and not isinstance(a_[0], (list, tuple)) and not isinstance(b_[0], (list, tuple)):
                try:
                    texs = {tx_ for tx_, ids in getattr(dst, "_gl", []) if set(b_) & set(ids)}
                    num = bool(texs) and all(eh_numero(tx_) for tx_ in texs)
                    self._origem(VGroup(*[src[0][j] for j in a_]), VGroup(*[dst[0][j] for j in b_]), "passo", numero=num)
                except Exception:
                    pass
        tops_antes = set(id(m) for m in self.mobjects)
        c = src.copy()
        self.add(c)
        tb_ = TransformByGlyphMap(c, dst, *mapas, default_transformer=Morph4, lag_ratio=0.12)       # v4: um grupo depois do outro, sem sopa
        self._voando = set(id(x) for x in c.get_family()) | set(id(x) for x in dst.get_family()) | set(id(x) for x in tb_.mobject.get_family())
        self._voando_raiz = [c, dst, tb_.mobject]
        self._fontes_extra = [src]                                    # v4 TRÂNSITO: o passo sai de cima da linha-mãe
        self._em_passo = True
        self.play(tb_, *extra, run_time=max(0.8, rt))
        self._em_passo = False
        self._fontes_extra = []
        self._voando, self._voando_raiz = set(), []
        for m in list(self.mobjects):
            if m is c or (m is not dst and m is not src and any(x is c for x in m.get_family())):
                self.remove(m)
        alvo = self._linha_de(dst)
        self._assenta(list(extra), [alvo], revelados=[dst])
        self._sobras(tops_antes, [alvo] + [getattr(e, "mobject", None) for e in extra if not isinstance(e, (FadeOut, Indicate))])
        self.foco = alvo
        return dst

    def _eh_vaga(self, m, fam_alvo):
        """Glifos da própria linha de destino (o "+", o "=", o "0"): entram na vaga depois de os voos pousarem (v4 §2 #7)."""
        if isinstance(m, RoundedRectangle) or getattr(m, "_caixa", False):
            return False
        fs = self._folhas(m)
        return bool(fs) and all(id(x) in fam_alvo for x in fs) and not any(getattr(x, "_caixa", False) for x in m.get_family())

    def voa(self, pares, extra=(), rt=1.1, alvo=None, origem=True, cada=0.5, arco_esq=0.0):
        """v4 §2 #7–#9: vagas reservadas. A linha de destino já está montada na posição final; cada glifo voa para a sua vaga, um termo por
        vez na ordem da linha (a cada `cada` s), saindo rápido de cima do desenho (rush_from: a cópia não fica dobrada sobre a origem) e
        pousando devagar. Caixas e marcadores entram junto com o primeiro voo (a caixa nasce vazia); os glifos que não voam (+, =, 0) entram
        nas vagas só depois de todos pousarem. Dentro da CONTA, o que desce faz um arco pela direita (por fora da Pilha)."""
        for a, b in (pares if origem else ()):
            self._origem(a, b, "voa")
        tops_antes = set(id(m) for m in self.mobjects)
        fam_alvo = set()
        for _, b in pares:
            fam_alvo |= set(id(x) for x in self._linha_de(b).get_family())
        antes, depois = [], []
        for an_ in extra:
            m = getattr(an_, "mobject", None)
            esq_ = isinstance(an_, FadeIn) and m is not None and (self._eh_vaga(m, fam_alvo) or isinstance(m, RoundedRectangle) or getattr(m, "_caixa", False))
            (depois if esq_ else antes).append(an_)           # v5 G29: o esqueleto (=, +, ·, barra, caixa) nasce antes dos tokens
        ordem = sorted(pares, key=lambda ab: (-round(ab[1].get_y(), 1), ab[1].get_x()))
        n = len(ordem)
        d = max(0.8, rt) if n == 1 else 0.7

        def arco(a, b):
            if a.get_x() > 0.45 and b.get_x() > 0.45 and b.get_y() < a.get_y() - 0.2:
                return -2.6                                                 # dentro da CONTA, descendo: por fora da Pilha (pela direita)
            if a.get_x() > 0.45 > b.get_x():
                return arco_esq                                             # v6: da CONTA para o ESQUEMA (arco_esq > 0: sai por baixo da linha de origem)
            return arco_esq if a.get_x() < 0.45 < b.get_x() else 0.0       # do ESQUEMA para a CONTA: arco por cima (arco_esq < 0)

        def desvio(a, b):
            d_ = float(np.linalg.norm(b.get_center() - a.get_center()))
            if arco(a, b) == -2.6:
                return RIGHT * max(0.0, min(0.6 * d_, 7.1 - max(a.get_right()[0], b.get_right()[0])))   # por fora da Pilha, sem sair do quadro
            return UP * (-arco_esq) * 0.25 * d_ if arco(a, b) else None
        if depois:
            self.play(*depois, run_time=0.35)                                            # G29: esqueleto com as vagas vazias
        voos, proxies, revela, par_voo, janelas = [], [], [], [], []
        for k_, (a, b) in enumerate(ordem):
            janelas.append((a, k_ * cada, k_ * cada + d))
            if _n_gl(a) == _n_gl(b):
                voos.append(TransformFromCopy(a, b, path_arc=arco(a, b), rate_func=rush_from, run_time=d))
                par_voo.append((a, b, k_ * cada, k_ * cada + d))
            else:                                                           # número de glifos diferente: a cópia chega sumindo, o destino acende na vaga
                px = a.copy()
                proxies.append(px)
                g_ = troca_anim(px, b, desvio=desvio(a, b))
                g_.run_time = d
                voos.append(g_)
                revela.append(g_.animations[1])
                par_voo.append((a, px, k_ * cada, k_ * cada + d))
        anims = voos[0] if n == 1 else LaggedStart(*voos, lag_ratio=cada / d, run_time=d + cada * (n - 1))
        dim_ = dim_origens(janelas, d + cada * (n - 1))
        self._voando = set(id(x) for a, b in pares for x in b.get_family())
        self._voando_raiz = [b for _, b in pares] + proxies         # o Transform recria os filhos no meio: a auditoria refaz a família a cada passada
        self._fontes_extra = [a for a, _ in pares]                    # a cópia sai de cima da própria origem (inclusive na troca)
        c0_ = self.clk.get_value()
        sc_ = self.ritmo                                                    # o play inteiro é escalado pelo ritmo da âncora
        self._pares_voo = [(a, b, c0_ + r0 * sc_, c0_ + r1 * sc_) for a, b, r0, r1 in par_voo]       # janela de cada voo (tempo do relógio) para a auditoria
        self.play(anims, dim_, *antes, run_time=d + cada * (n - 1))
        self._pares_voo = []
        self._fontes_extra = []
        self._voando, self._voando_raiz = set(), []
        if proxies:
            self.remove(*proxies)
        alvos = alvo if isinstance(alvo, (list, tuple)) else ([alvo] if alvo is not None else [])
        if not alvos:
            for a, b in pares:
                l = self._linha_de(b)
                if l not in alvos:
                    alvos.append(l)
        self._assenta([v for v in voos if isinstance(v, TransformFromCopy)] + revela + list(extra), alvos)
        self._sobras(tops_antes, list(alvos) + [getattr(e, "mobject", None) for e in antes if not isinstance(e, (FadeOut, Indicate))])

    # ── PAUSAS: hold longo vira destaque do termo em foco ──
    QUIETO = 0.4                                   # v7 CONGELAMENTO: nenhum trecho sem movimento passa de ~1,2 s (o QA conta > 1,5 s)

    def _introduzidos(self, anims):
        """v7: os objetos que acabaram de entrar (FadeIn/Write/Create/Grow...): o narrador está falando deles, então são o destaque de reserva."""
        saida = []

        def visita(x):
            for b in getattr(x, "animations", None) or []:
                visita(b)
            if isinstance(x, (FadeIn, Write, Create, GrowFromCenter, GrowArrow, DrawBorderThenFill, Indicate)):
                m = getattr(x, "mobject", None)
                if m is not None and not isinstance(m, ValueTracker) and 0.05 < max(m.width, m.height) < 9.0:
                    saida.append(m)
        for x in anims:
            visita(x)
        return saida

    def play(self, *a, **kw):
        sutil = kw.pop("sutil", False)                 # sutil: muda pouco pixel por quadro (risco fino, cor): não conta como movimento
        q = getattr(self, "_quieto", 0.0)
        novos = self._introduzidos(a)
        if novos:
            self._intro = (getattr(self, "_intro", []) + novos)[-8:]
        super().play(*a, **kw)
        self._quieto = q + (kw.get("run_time") or 1.0) if sutil else 0.0

    def _destaques(self, n=3):
        """Até `n` coisas que podem pulsar sem mentir: o termo em foco, a última linha da conta, a HIPÓTESE, o selo, o referencial e o que acabou de entrar."""
        out, vistos = [], set()
        for m in (self.foco, self.pilha.ultima(), getattr(self, "s2", None), getattr(self, "s1", None), getattr(self, "ref_mob", None),
                  *reversed(getattr(self, "_intro", []))):
            if m is None or id(m) in vistos:
                continue
            vis_ = max([max(x.get_fill_opacity(), x.get_stroke_opacity()) for x in m.family_members_with_points()] or [0]) > 0.3
            if vis_ and (m in self.mobjects or any(m in t.get_family() for t in self.mobjects)) and not m.get_updaters() \
                    and not any(x.get_updaters() for x in m.get_family()):
                out.append(m)
                vistos.add(id(m))
            else:
                partes = [t for t in self.mobjects if any(t is x for x in m.get_family())]       # entrou em pedaços (cada um é um topo)
                if vis_ and partes and not any(x.get_updaters() for p_ in partes for x in p_.get_family()):
                    out.append(VGroup(*partes))
                    vistos.add(id(m))
            if len(out) >= n:
                break
        return out

    def _destaque(self):
        d = self._destaques(1)
        return d[0] if d else None

    def pulsa(self, alvos, dp, *extra):
        """v7 (sem piscar): roda as animações `extra` em `dp` s. Nada pisca nem realça: o alinhamento com a voz vem do plano() e do conteúdo."""
        if extra:
            self.play(*extra, run_time=dp, fixo=True)
        else:
            self._wait_q(dp)

    def wait(self, duration=1.0, *a, interno=False, **kw):
        if not interno:
            if SYNC == "medir":
                self._cur["W"] += duration
            else:
                duration = duration * self.ritmo_w
        self._wait_q(duration)

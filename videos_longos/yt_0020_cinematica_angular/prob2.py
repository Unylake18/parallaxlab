"""yt_0019 (copiado do yt_0018 v4) — camada sobre prob.py (handoff v2 §2: G23–G28; v3 §4: zonas 16×9, Pilha em blocos, selo sequencial).

Zonas (v3 §4, quadro 16×9): canto x < −1, y > 3,05 · chip do checklist x −7,3…−2,5, y 2,60…3,00 · faixa de selo (uma só) x 0,7…7,3, y 2,85…3,50 ·
Pilha x 0,7…7,3, y −3,65…2,60 · ESQUEMA x −7,3…0,2, y −3,65…2,50.
Pilha (v3 §4): P1 uma linha que começa com "=", "⇒" ou "→" é FILHA da de cima; a Pilha tira blocos inteiros (mãe + filhas), do mais antigo
para o mais novo; se a mãe sai e a filha fica, a filha ganha o lado esquerdo antes (`_lhs`, TransformMatchingShapes) · P2 as filhas alinham o
"=" com o "=" da mãe · P3 caixa sempre com lado esquerdo. Troca de selo: o velho sai em 0,25 s e só então o novo entra (nunca dois).
G27 `rotulo()` testa colisão antes de pôr um rótulo. G23 `passo()` (glyph map numa linha nova) e `voa()` (TransformFromCopy do desenho para a
conta); G24 v3: cada par símbolo → número confere a cor de origem (`_origem`). PAUSAS: hold longo vira destaque do termo em foco.
"""
from prob import *  # noqa: F401,F403

X_CONTA, TOPO_PILHA, BASE_PILHA = 0.7, 2.35, -3.25          # yt_0019 §3 G25
LARG_CONTA = 6.0                                             # x 0,7…6,7
Y_SELO_TOPO, H_SELO = 3.15, 1.12                             # faixa de selo: topo 3,15 (§2.3)                 # faixa de selo: duas linhas de 24 pt ao lado da etiqueta (topo 3,55, base ≥ 2,75)
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
    def __init__(self, cena, x0=X_CONTA, topo=TOPO_PILHA, base=BASE_PILHA, buff=0.26, larg=None):
        self.cena, self.x0, self.topo, self.base, self.buff = cena, x0, topo, base, buff
        self.larg = larg or LARG_CONTA
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
        if m.width > self.larg - dx + 0.01:                          # yt_0020: a linha larga sempre encolhe para caber (fator no qa.txt)
            print(f"[ajuste] {self.cena.clk.get_value():7.1f}s linha encolhida para caber na Pilha ({m.width:.2f} → {self.larg - dx:.2f}, "
                  f"fator {(self.larg - dx) / m.width:.2f}) {_desc(m)}")
            m.scale_to_fit_width(self.larg - dx)
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
            if m.get_right()[0] > self.x0 + self.larg + 0.01:                        # yt_0020: filha alinhada no "=" que passaria da margem encolhe
                print(f"[ajuste] {self.cena.clk.get_value():7.1f}s filha encolhida (fator {(self.x0 + self.larg - m.get_left()[0]) / m.width:.2f}) {_desc(m)}")
                m.scale_to_fit_width(self.x0 + self.larg - m.get_left()[0], about_edge=LEFT)
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


def _desc(m):
    """Descida abaixo da linha de base de um texto txt()/tx() (Ç, Q, vírgula…): altura do texto − altura do mesmo texto sem as descidas."""
    s = getattr(m, "_s", None)
    if not s or not isinstance(m, Mobject):
        return 0.0
    # v7: parênteses, colchetes, barras, setas e as descendentes minúsculas (g j p q y) também descem da linha de base
    mapa = {"Ç": "C", "ç": "c", "Q": "O", "q": "o", ",": "", ";": "", "J": "I", "j": "i", "Ô": "O", "g": "o", "p": "o", "y": "v",
            "(": "I", ")": "I", "[": "I", "]": "I", "/": "I", "|": "I", "→": "I", "⇒": "I", "<": "I", ">": "I"}
    rot_ = getattr(m, "_rot", False)
    base = s if rot_ else s.upper()
    s2 = base.translate(str.maketrans(mapa))
    if s2 == base or not s2.strip():
        return 0.0
    ref = rot(s2, getattr(m, "_tam", 24)) if rot_ else txt(s2, getattr(m, "_tam", 24), bold=getattr(m, "_bold", False))
    return max(0.0, m.height - ref.height)


def linha_base(pcs, buff=0.1, extra=0.0):
    """Peças lado a lado com a MESMA linha de base (base das maiúsculas), não a base da caixa. `extra` afasta a primeira peça das demais."""
    pcs = [p for p in pcs if p is not None]
    g = VGroup(*pcs).arrange(RIGHT, buff=buff)
    if extra and len(pcs) > 1:
        VGroup(*pcs[1:]).shift(extra * RIGHT)
    for p in pcs:
        p.shift(UP * (-(p.get_bottom()[1] + _desc(p))))
    return g


# ── yt_0020 R1 §2: ESCRITA em ordem de x — a linha nasce da esquerda para a direita, como se alguém escrevesse ─────────────────────────
class _Temporizado(AnimationGroup):
    """AnimationGroup em que cada filha começa no instante dado (`starts`), em vez de seguir um lag_ratio."""

    def __init__(self, *anims, starts, **kw):
        self._starts = list(starts)
        super().__init__(*anims, lag_ratio=0.0, **kw)

    def build_animations_with_timings(self):
        n = len(self.animations)
        awt = np.zeros(n, dtype=[("anim", "O"), ("start", "f8"), ("end", "f8")])
        self.anims_begun = np.zeros(n, dtype=bool)
        self.anims_finished = np.zeros(n, dtype=bool)
        self.anims_with_timings = awt
        if n:
            awt["anim"] = self.animations
            awt["start"] = self._starts
            awt["end"] = awt["start"] + np.array([a.run_time for a in self.animations], dtype=float)


def _unidades(pedacos):
    """Unidades de escrita (chave → folhas) dos pedaços, na ordem em que aparecem: uma parte do eqp, um txt(), um MathTex inteiro, uma caixa."""
    us, ordem, vistos = {}, [], set()

    def add(k, x):
        if id(x) in vistos:                                             # o mesmo glifo pode vir em dois pedaços (voo e vaga)
            return
        vistos.add(id(x))
        if k not in us:
            us[k] = []
            ordem.append(k)
        us[k].append(x)

    def walk(n, k):
        if getattr(n, "_caixa", False):
            add(("caixa", id(n)), n)
            return
        u = getattr(n, "_unid", None)
        if u is not None:
            k = ("u",) + tuple(u)
        elif k is None:
            if getattr(n, "_s", None) is not None:
                k = ("txt", id(n))
            elif isinstance(n, MathTex) and not hasattr(n, "_gl"):
                k = ("tex", id(n))
        if isinstance(n, VMobject) and n.points.size and not n.submobjects:
            add(k or ("f", id(n)), n)
            return
        for s in n.submobjects:
            walk(s, k)
    for p in pedacos:
        walk(p, None)
    return us, ordem


def _linha_txt(m):
    """Descrição curta de uma linha da CONTA para o log: o TeX das partes (eqp) ou o texto."""
    for x in m.get_family():
        gl = getattr(x, "_gl", None)
        if gl:
            return "".join(t for t, _ in gl)[:60]
    return _desc(m)


def _ordena_glifos(gs):
    """Ordem de escrita dentro de uma unidade (§2 item 3): fração = numerador → barra → denominador; raiz = símbolo → traço → radicando; o resto por x."""
    barras = [g for g in gs if g.width > 0.12 and g.height < 0.04 and g.width > 5 * g.height]
    if not barras:
        return sorted(gs, key=lambda g: g.get_left()[0])
    chave = {}
    for g in gs:
        for b in sorted(barras, key=lambda b: -b.width):
            if g is b:
                chave[id(g)] = (b.get_left()[0], 1, g.get_left()[0])
                break
            if b.get_left()[0] - 0.05 <= g.get_center()[0] <= b.get_right()[0] + 0.05 and abs(g.get_center()[1] - b.get_center()[1]) < 1.2:
                chave[id(g)] = (b.get_left()[0], 0 if g.get_center()[1] > b.get_center()[1] else 2, g.get_left()[0])
                break
        else:
            chave[id(g)] = (g.get_left()[0], 0, g.get_left()[0])
    return sorted(gs, key=lambda g: chave[id(g)])


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
        mk = lambda l: tx(l, size) if isinstance(l, str) else linha_base([tx(i, size) if isinstance(i, str) else i for i in l], 0.1)
        if linhas:
            if linhas[0] is not None:
                l0 = linhas[0]
                pcs0 = [tx(l0, size)] if isinstance(l0, str) else [tx(i, size) if isinstance(i, str) else i for i in l0]
                l1 = linha_base([t] + pcs0, 0.1, extra=0.08)                     # G35: DICA, CONFERE… na mesma linha de base da frase
            else:
                l1 = VGroup(t)
            g = VGroup(l1, *[mk(l) for l in linhas[1:]]).arrange(DOWN, buff=0.06, aligned_edge=LEFT)
        else:
            g = VGroup(t)
        bx = RoundedRectangle(corner_radius=0.08, width=g.width + 0.24, height=g.height + 0.12).move_to(g).set_fill(PANEL, 0.9).set_stroke(borda, 1.8)
        bx._fundo = bx._caixa = True
        s = VGroup(bx, g).set_z_index(36)
        s._selo = "faixa"
        print(f"[selo] {tag} linhas={max(1, len(linhas))} w={s.width:.2f} h={s.height:.2f}")
        if s.height > H_SELO + 0.01 or s.width > wmax + 0.01:
            print(f"[audit] FORA DA ZONA selo '{tag}' grande demais ({s.width:.2f} × {s.height:.2f})")
        return s

    # ── selo único na faixa (v3 §4): o velho sai em 0,25 s e só então o novo entra ──
    def selo(self, tag, corpo, cor=CYAN, borda=BLUE_L, rt=0.5, x0=X_CONTA, anims=(), wmax=LARG_CONTA):
        novo = self._selo_mob(tag, corpo, cor, borda, wmax=wmax)
        novo.move_to(P3(x0 + novo.width / 2, Y_SELO_TOPO - novo.height / 2))
        velho = self.s1
        if velho is not None:
            self.play(FadeOut(velho), run_time=0.25)
            self.remove(velho)
        self.s1 = None
        topo = min(TOPO_PILHA, novo.get_bottom()[1] - 0.15)                 # selo de três linhas: a Pilha desce junto (nunca um por cima do outro)
        mov = []
        if abs(topo - self.pilha.topo) > 1e-3 and not self.layout_v and not getattr(self.pilha, "topo_fixo", False):
            self.pilha.topo = topo
            y = topo
            for l, d in self.pilha.linhas:
                mov.append(l.animate.move_to(P3(self.pilha.x0 + d + l.width / 2, y - l.height / 2)))
                y -= l.height + self.pilha.buff
        self.play(FadeIn(novo, shift=0.06 * DOWN), *mov, *anims, run_time=max(0.25, rt - (0.25 if velho is not None else 0.0)))
        self.s1 = novo
        return novo

    def selo_reflow(self, novo):
        return novo

    def dica18(self, corpo, **kw):
        """v4 G36: a DICA mora junto do que ela resume: última linha da Pilha, borda esquerda alinhada, 0,35 u abaixo da linha anterior, uma linha."""
        kw.pop("x0", None)
        kw.pop("wmax", None)
        s = self._selo_mob("DICA", corpo, cor=CYAN, borda=CYAN, wmax=self.pilha.larg)
        s.__dict__.pop("_selo", None)
        s._tela_cheia = False
        velho = self.pilha.buff
        self.pilha.buff = 0.35
        ant = self.pilha.linhas[-1][0].get_bottom()[1] if self.pilha.linhas else None
        self.pilha.poe(s)
        self.pilha.buff = velho
        print(f"[dica] borda_esq_dx={abs(s.get_left()[0] - self.pilha.x0):.3f} gap={(ant - s.get_top()[1]) if ant is not None else -1:.3f} linhas=1")
        self.play(FadeIn(s), run_time=0.35)
        self.foco = s
        return s

    def hip(self, corpo, rt=0.5, **kw):
        tag = "HIPÓTESES" if (not isinstance(corpo, str) or "·" in corpo) else "HIPÓTESE"
        return self.selo(tag, corpo, cor=CYAN, borda=GEO, rt=rt, **kw)

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
        for m in list(self.mobjects):
            if id(m) in tops_antes or id(m) in manter or id(m) in linhas or m in self.fixos() or isinstance(m, ValueTracker):
                continue
            fs = self._folhas(m)
            if fs and all(id(x) in fam for x in fs):                        # pedaço revelado de uma linha que ainda vai completar
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
        print(f"[alg] {self._aid} passo mapas={len(mapas)}")

        def _x_dst(e):                                                      # yt_0020 R1 §2.4: glifos mapeados e novos na mesma fila por x; o que sai, antes
            to = e[1] if len(e) > 1 and isinstance(e[1], (list, tuple)) else []
            return min((dst[0][j].get_left()[0] for j in to), default=-1e9)
        mapas = tuple(sorted(mapas, key=_x_dst))
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
        self.play(tb_, *extra, run_time=max(0.8, rt))
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

    def voa(self, pares, extra=(), rt=1.1, alvo=None, origem=True, cada=0.4, arco_esq=0.0):
        """yt_0020 R1 §2: o voo agora faz parte da ESCRITA em ordem de x. Cada origem sai do desenho e pousa na vaga no instante da sua parte;
        os glifos que não voam (+, =, 0) são escritos na própria vaga, intercalados por x (nunca depois de todos os voos)."""
        fam_alvo = set()
        for _, b in pares:
            fam_alvo |= set(id(x) for x in self._linha_de(b).get_family())
        pedacos, resto = [], []
        for an_ in extra:
            m = getattr(an_, "mobject", None)
            (pedacos if isinstance(an_, FadeIn) and m is not None and self._eh_vaga(m, fam_alvo) else resto).append(an_)
        self.escreve(*[an_.mobject for an_ in pedacos], voos=pares, extra=resto, rt=rt, origem=origem, arco_esq=arco_esq, alvo=alvo)


    # ── ESCRITA (yt_0020 R1 §2) ──
    def _arco_voo(self, a, b, arco_esq=0.0):
        if self.layout_v:
            return arco_esq
        if a.get_x() > 0.45 and b.get_x() > 0.45 and b.get_y() < a.get_y() - 0.2:
            return -2.6                                                 # dentro da CONTA, descendo: por fora da Pilha (pela direita)
        return arco_esq if a.get_x() < 0.45 < b.get_x() else 0.0       # do ESQUEMA para a CONTA: arco por cima (arco_esq < 0)

    def _desvio_voo(self, a, b, arco_esq=0.0):
        d_ = float(np.linalg.norm(b.get_center() - a.get_center()))
        arc = self._arco_voo(a, b, arco_esq)
        if arc == -2.6:
            return RIGHT * 0.6 * d_
        return UP * (-arco_esq) * 0.25 * d_ if arc else None

    def _escrevivel(self, x):
        """FadeIn de uma linha da CONTA (ou de um pedaço dela) que tem MathTex: vira escrita em ordem. Selo, DICA e texto puro continuam por FadeIn."""
        if type(x) is not FadeIn:
            return False
        m = getattr(x, "mobject", None)
        if m is None or isinstance(m, ImageMobject):
            return False
        ln = self._linha_de(m)
        if not any(ln is l for l, _ in self.pilha.linhas):
            return False
        if getattr(ln, "_selo_tag", False):
            print(f"[alg] {self._aid} fadein-selo")
            return False
        if not any(isinstance(y, MathTex) for y in ln.get_family()):
            print(f"[alg] {self._aid} fadein-texto")
            return False
        return True

    def escreve(self, *pedacos, voos=(), extra=(), rt=None, dur=0.2, d_voo=0.4, dx=None, pausa=0.3, arco_esq=0.0, origem=True, alvo=None, **kw):
        """§2: constrói a(s) linha(s) da CONTA da esquerda para a direita (x do glifo). Parte fixa: escrita curta na própria vaga, no seu instante.
        Parte que voa (`voos` = [(origem, destino)]): cópia que sai do desenho e POUSA na vaga no seu instante (o original fica). Caixa: contorno e primeira
        parte juntos. Registra a ordem (qa_overlay: ordem*) para a auditoria ORDEM e o tipo de construção para o algebra.txt."""
        pedacos = [p for p in pedacos if p is not None]
        if origem:
            for a_, b_ in voos:
                self._origem(a_, b_, "voa")
        us, ordem = _unidades(list(pedacos) + [b_ for _, b_ in voos])
        voo_de = {}
        for i, (a_, b_) in enumerate(voos):
            ids = set(id(x) for x in b_.get_family())
            folhas = []
            for k in list(ordem):
                lv = [g for g in us[k] if id(g) in ids]
                if lv:
                    us[k] = [g for g in us[k] if id(g) not in ids]
                    folhas += lv
                    if not us[k]:
                        ordem.remove(k)
                        del us[k]
            if folhas:
                us[("voo", i)] = folhas
                ordem.append(("voo", i))
                voo_de[("voo", i)] = (a_, b_)
        U_ = []
        for k in ordem:
            gs = us[k]
            if k[0] == "caixa":
                U_.append(dict(k=k, gs=gs, tipo="caixa"))
                continue
            if k[0] != "voo":
                gs = _ordena_glifos(gs)
            U_.append(dict(k=k, gs=gs, tipo="voo" if k[0] == "voo" else "fixo", xl=min(g.get_left()[0] for g in gs), xr=max(g.get_right()[0] for g in gs),
                           yc=float(np.mean([g.get_center()[1] for g in gs]))))
        cont = sorted([u for u in U_ if u["tipo"] != "caixa"], key=lambda u: (round(u["xl"], 2), -u["yc"]))
        caixas = [u for u in U_ if u["tipo"] == "caixa"]
        n = len(cont)
        if dx is None:
            alvo_t = rt if rt is not None else 0.2 + 0.15 * max(n - 1, 0)
            dx = min(0.25, max(0.12, (alvo_t - dur) / max(n - 1, 1)))
        for k_, u in enumerate(cont):
            u["t"] = k_ * dx
            u["ini"] = u["t"] - d_voo if u["tipo"] == "voo" else u["t"]
        lead = max([0.0] + [-u["ini"] for u in cont])
        for u in cont:
            u["ini"] += lead
            u["t"] += lead
        t_cx = max(0.0, (cont[0]["t"] - 0.1) if cont else 0.0)
        anims, ini, assenta, proxies, revelas, raizes = [], [], [], [], [], []
        for u in cont:
            if u["tipo"] == "fixo":
                an_ = Write(VGroup(*u["gs"]), run_time=dur)
                anims.append(an_)
                ini.append(u["ini"])
                assenta.append(an_)
                u["inst"] = u["ini"] + 0.5 * dur
            else:
                a_, b_ = voo_de[u["k"]]
                arc = self._arco_voo(a_, b_, arco_esq)
                if _n_gl(a_) == _n_gl(b_):
                    an_ = TransformFromCopy(a_, b_, path_arc=arc, rate_func=rush_from, run_time=d_voo)
                    assenta.append(an_)
                else:                                                       # número de glifos diferente: a cópia chega sumindo, o destino acende na vaga
                    px = a_.copy()
                    proxies.append(px)
                    an_ = troca_anim(px, b_, desvio=self._desvio_voo(a_, b_, arco_esq))
                    an_.run_time = d_voo
                    revelas.append(an_.animations[1])
                raizes.append(b_)
                anims.append(an_)
                ini.append(u["ini"])
                u["inst"] = u["ini"] + d_voo
        for c in caixas:
            an_ = FadeIn(c["gs"][0] if len(c["gs"]) == 1 else VGroup(*c["gs"]), run_time=0.25)
            anims.append(an_)
            ini.append(t_cx)
            assenta.append(an_)
        if not anims:
            return
        grp = _Temporizado(*anims, starts=ini)
        D = grp.max_end_time
        alvos = []
        for u in U_:
            ln = self._linha_de(VGroup(u["gs"][0]))
            if not any(ln is x for x in alvos):
                alvos.append(ln)
        if alvo is not None:
            alvos = list(alvo) if isinstance(alvo, (list, tuple)) else [alvo]
        tops_antes = set(id(m) for m in self.mobjects)
        self._voando = set(id(x) for u in U_ for g in u["gs"] for x in g.get_family())
        self._voando_raiz = list(raizes) + proxies
        self._em_escreve = True
        try:
            self.play(grp, *extra, run_time=D, **kw)
        finally:
            self._em_escreve = False
        self._voando, self._voando_raiz = set(), []
        if proxies:
            self.remove(*proxies)
        self._assenta(assenta + revelas, alvos)
        self._sobras(tops_antes, list(alvos) + [getattr(e, "mobject", None) for e in extra if not isinstance(e, (FadeOut, Indicate))])
        self._n_ord = getattr(self, "_n_ord", 0) + 1
        if not PEDIDOS3D:
            self.reg(f"ordem{self._n_ord}", aid=self._aid or "-", linha=_linha_txt(alvos[0]) if alvos else "-", dx=dx, voos=len(voos),
                     u=[[u["xl"], u["xr"], u["inst"], 1.0 if u["tipo"] == "voo" else 0.0] for u in cont],
                     caixa=[[c["gs"][0].get_left()[0], t_cx, (cont[0]["inst"] if cont else 0.0)] for c in caixas[:1]])
        print(f"[alg] {self._aid} escreve n={n} voos={len(voos)} dx={dx:.2f} D={D:.2f} {_linha_txt(alvos[0]) if alvos else ''}")
        if pausa and self.resta() > 1.2:
            self.wait(pausa, interno=True)                                  # §2 item 6: pausa de leitura depois da linha completa
        self.foco = alvos[-1] if alvos else self.foco

    # ── PAUSAS: hold longo vira destaque do termo em foco ──
    QUIETO = 1.9                                   # v7 CONGELAMENTO: nenhum trecho sem movimento passa de ~1,2 s (o QA conta > 1,5 s)

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
        if not getattr(self, "_em_escreve", False):                                # yt_0020 R1 §2: FadeIn de linha da CONTA com MathTex vira escrita em ordem
            conv = [x for x in a if self._escrevivel(x)]
            if conv:
                resto = [x for x in a if not any(x is c for c in conv)]
                kws = {k: v for k, v in kw.items() if k in ("fixo", "sutil")}
                self.escreve(*[c.mobject for c in conv], extra=resto, rt=kw.get("run_time"), **kws)
                return
        sutil = kw.pop("sutil", False)                 # sutil: muda pouco pixel por quadro (risco fino, cor): não conta como movimento
        q = getattr(self, "_quieto", 0.0)
        novos = self._introduzidos(a)
        if novos:
            self._intro = (getattr(self, "_intro", []) + novos)[-8:]
        hls = []
        if not kw.get("fixo", False) and SYNC != "medir" and not getattr(self, "_em_troca", False):
            rt_ = (kw.get("run_time") or max([getattr(x, "run_time", 1.0) for x in a] or [1.0])) * self.ritmo
            if False and rt_ >= 0.6:                                                         # v9: SEM caixas de realce (pedido do Kaio); v7: jogada longa e lenta (voo de termo pequeno, FadeIn): o destino ganha um realce suave
                alvos_ = list(novos[:3])
                ult_ = self.pilha.ultima() if getattr(self, "pilha", None) is not None else None
                if ult_ is not None and ult_.width > 0.2:
                    alvos_.append(ult_)
                for al_ in alvos_[:3]:
                    hl = RoundedRectangle(corner_radius=0.08, width=al_.width + 0.5, height=al_.height + 0.34).move_to(al_.get_center()).set_stroke(width=0).set_fill(CYAN, 0.0)
                    hl._fundo = hl._caixa = True
                    hl.set_z_index(max([m.get_z_index() for m in al_.get_family()] + [0]) + 0.1)
                    self.add(hl)
                    hls.append(hl)
                nb_ = max(1, int(math.ceil(rt_ / 1.0)))                                        # jogada longa: um realce por segundo (nunca um só, lento)
                bump_ = lambda t_, nb_=nb_: there_and_back((t_ * nb_) % 1.0 if t_ < 1.0 else 0.0)
                a = (*a, *[hl.animate(rate_func=bump_).set_fill(CYAN, 0.34) for hl in hls])
        if os.environ.get("DEBUGPLAY"):
            print(f"[play] {self._aid} abs {(self.nq + self._off) / FPS:.1f} rt {(kw.get('run_time') or 0):.2f}x{self.ritmo:.2f} fixo {kw.get('fixo', False)} sutil {sutil} hls {len(hls)} {[type(x).__name__ for x in a[:4]]}")
        super().play(*a, **kw)
        for hl in hls:
            self.remove(hl)
        self._quieto = q + (kw.get("run_time") or 1.0) if sutil else 0.0

    # ── v10 R-F: realce e revelação de termos de uma equação SEM desmontá-la (Scene.add de grupos de glifos repartia a linha e ela sumia) ──
    def ind(self, M_, idx, partes, color=WHITE_, f=1.12, rt=0.8):
        """Realce de termos de `M_` (MathTex de string única): uma CÓPIA dos glifos cresce e muda de cor por cima, e some; a linha original não é tocada."""
        if isinstance(partes, int):
            partes = [partes]
        base = VGroup(*[M_[0][j].copy() for k in partes for j in idx[k]])
        base.set_z_index(max([x.get_z_index() for x in M_.get_family()] + [0]) + 1)
        cores0 = [g.get_color() for g in base.family_members_with_points()]

        def f_(m, a, base=base, cores0=cores0):
            b = there_and_back(a)
            m.become(base)
            m.scale(1 + (f - 1) * b)
            for g, c0 in zip(m.family_members_with_points(), cores0):
                g.set_color(interpolate_color(ManimColor(c0), ManimColor(color), min(1.0, 1.6 * b)))
        return UpdateFromAlphaFunc(base.copy(), f_, introducer=True, remover=True, run_time=rt, suspend_mobject_updating=False)

    def ind_copia(self, src, color=WHITE_, f=1.12, rt=0.8):
        """Realce de qualquer mobject (ou pedaço de glifos) por CÓPIA: a cópia cresce e muda de cor por cima da origem e some; a origem não é tocada."""
        base = src.copy()
        base.set_z_index(max([x.get_z_index() for x in src.get_family()] + [0]) + 1)
        cores0 = [g.get_color() for g in base.family_members_with_points()]

        def f_(m, a, base=base, cores0=cores0):
            b = there_and_back(a)
            m.become(base)
            m.scale(1 + (f - 1) * b)
            for g, c0 in zip(m.family_members_with_points(), cores0):
                g.set_color(interpolate_color(ManimColor(c0), ManimColor(color), min(1.0, 1.6 * b)))
        return UpdateFromAlphaFunc(base.copy(), f_, introducer=True, remover=True, run_time=rt, suspend_mobject_updating=False)

    def acende(self, pares, extra=(), rt=0.9, **_):
        """v10 R-F: no lugar do voo de glifos (`voa`): as origens pulsam (cópia) enquanto os termos novos acendem no lugar. Nada atravessa a tela nem se sobrepõe a rótulos."""
        self.play(*[self.ind_copia(a, WHITE_, 1.12, min(rt, 0.9)) for a, _ in pares], *[FadeIn(b) for _, b in pares], *extra, run_time=rt)

    def revela(self, M_, idx, partes, rt=0.8):
        """Acende (opacidade 0→1) só os glifos `partes` de `M_`, que já está em cena com esses termos apagados: a linha continua inteira, um só mobject."""
        gl = [M_[0][j] for k in partes for j in idx[k]]

        def f_(m, a):
            for g in gl:
                g.set_opacity(a)
        return UpdateFromAlphaFunc(M_, f_, run_time=rt, suspend_mobject_updating=False)

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
                ids_ = set(id(x) for x in m.get_family())
                partes = [t for t in self.mobjects if t is not self.fundo and any(id(x) in ids_ for x in t.get_family())]       # v9: entrou em pedaços (topos que repartem glifos com m)
                if vis_ and partes and not any(x.get_updaters() for p_ in partes for x in p_.get_family()):
                    out.append(VGroup(*partes))
                    vistos.add(id(m))
            if len(out) >= n:
                break
        return out

    def _destaque(self):
        d = self._destaques(1)
        return d[0] if d else None

    def _pulso_anims(self, alvos, dp):
        """Um pulso de `dp` s em cada alvo (v7: o movimento que acompanha a fala; opacidade na CONTA, escala no resto). Roda como um play."""
        anims, envelopes = [], []
        for alvo in alvos:
            f = min(1.5, max(1.08, 1 + 0.3 / max(alvo.width, alvo.height, 0.05)))   # objeto pequeno pulsa mais (o QA mede pixels)
            if alvo.get_x() > 0.45 or max(alvo.width, alvo.height) > 1.2:               # v10 R-F: equação nunca escurece nem some: o pulso é só um respiro de escala
                anims.append(alvo.animate(rate_func=there_and_back).scale(1.06))
            else:
                anims.append(alvo.animate(rate_func=there_and_back).scale(f, about_edge=ORIGIN))
            if alvo not in self.mobjects and not any(alvo in t.get_family() for t in self.mobjects):
                envelopes.append(alvo)
        self._pulso = True                                                       # o pulso de destaque escala no lugar: não é trânsito
        return anims, envelopes

    _hls = None

    def pulsa(self, alvos, dp, *extra):
        print(f"[pulso] {self._aid} abs {(self.nq + self._off) / FPS:.1f} s dp {dp:.2f} alvos {[type(x).__name__ + ':' + format(x.get_x(), '.1f') + ',' + format(x.width, '.1f') for x in alvos]}")
        self._hls = []
        anims, envelopes = self._pulso_anims(alvos, dp)
        self.play(*anims, *extra, run_time=dp, fixo=True)
        self._pulso = False
        for hl in self._hls:
            self.remove(hl)
        self._hls = []
        for alvo in envelopes:                                                         # v10: o envelope sai E devolve os pedaços à cena (antes eles sumiam junto: a equação apagava até a próxima animação)
            pos = self.mobjects.index(alvo) if alvo in self.mobjects else len(self.mobjects)
            self.mobjects = [m for m in self.mobjects if m is not alvo]
            for sub in reversed(list(alvo.submobjects)):
                self.mobjects.insert(min(pos, len(self.mobjects)), sub)

    def wait(self, duration=1.0, *a, interno=False, **kw):
        if not interno:
            if SYNC == "medir":
                self._cur["W"] += duration
            else:
                duration = duration * self.ritmo_w
        d = duration
        q = getattr(self, "_quieto", 0.0)
        while d > 1e-3:
            livre = max(0.0, self.QUIETO - q)
            if d <= livre + 0.05:
                self._wait_q(d)
                q += d
                break
            alvos = self._destaques(3)
            if not alvos:                                          # sem o que pulsar: segue parado (o QA acusa e a cena ganha movimento próprio)
                if d > 1.0:
                    print(f"[parado] {self._aid} abs {(self.nq + self._off) / FPS:.1f} s: {d:.1f} s sem destaque")
                    ul_ = None
                    ul_ = self.pilha.ultima()
                    if ul_ is not None:
                        ids_ = set(id(x) for x in ul_.get_family())
                        pp_ = [t for t in self.mobjects if any(id(x) in ids_ for x in t.get_family())]
                        print(f"[parado-dbg2] partes={len(pp_)} ops={[round(max([max(x.get_fill_opacity(), x.get_stroke_opacity()) for x in t.family_members_with_points()] or [0]),2) for t in pp_]} upds={[any(x.get_updaters() for x in t.get_family()) for t in pp_]} foco={type(self.foco).__name__}")
                    if False: print(f"[parado-dbg] foco={type(self.foco).__name__} ultima={type(ul_).__name__ if ul_ is not None else None} em_mobjects={ul_ in self.mobjects if ul_ is not None else None} upd={[bool(x.get_updaters()) for x in (ul_.get_family() if ul_ is not None else [])][:3]} n_intro={len(getattr(self, '_intro', []))}")
                self._wait_q(d)
                q += d
                break
            if livre > 0.05:
                self._wait_q(livre)
                d -= livre
            dp = min(0.8, d)                                       # v7: o pulso cabe no que sobra (mínimo 0,3 s); nunca > ~1 s parado
            if dp < 0.3:
                self._wait_q(d)
                q += d
                break
            self.pulsa(alvos, dp)
            d -= dp
            q = 0.0
        self._quieto = q

"""yt_0021 (copiado do yt_0019) — kit comum: paleta, marcador do centro de massa, texto, setas, corpos 2D, fronteira, cavalo, pedra, pessoa de perfil,
cabeçalho e relógio por quadro.

yt_0021: copiado do kit do yt_0019 (não importa entre unidades); muda o TITULO, a paleta (massa e I em rosa) e a tabela de cor por token. Preview silencioso: o tempo de cada âncora vem de ancoras.json
(palavras da narração congelada ÷ 2,7 palavras/s); a cena se estica para a voz depois. Pessoas e cavalo são silhuetas 2D preenchidas
(cápsulas), nunca linhas.
"""
import json
import math
import os
import sys
from pathlib import Path

import numpy as np
from manim import *  # noqa: F401,F403

Circle.set_default(color=WHITE)   # fill padrão RED aparecia ao esmaecer com set_opacity

AQUI = Path(__file__).resolve().parent
ROOT = AQUI.parents[1]
sys.path.insert(0, str(ROOT))
from template.config_horizontal import BACKGROUND_COLOR, PRIMARY_COLOR, TEXT_COLOR, WATERMARK_PATH  # noqa: E402
from template.fonts import DISPLAY_FONT, official_text, screen_text  # noqa: E402

config.media_dir = os.environ.get("MEDIA_DIR", str(AQUI / "media"))

# ── paleta (padrão de Mecânica, docs/padrao_video_longo.md §4 + handoff §4) ─────────────────────────────────
WHITE_ = TEXT_COLOR          # #F5F7FF
CYAN = PRIMARY_COLOR         # #35D9FF (energia cinética e assunto do próximo vídeo)
KC = CYAN                    # energia cinética
HEAT = "#FF5A36"             # calor / energia dissipada (v5: mais vermelho, separa do âmbar da massa)
MAS = "#FF7EB6"              # yt_0021: massa e inércia (m, M, dm, λ, σ, ρ, I, c): rosa (decisão do Kaio, 2026-11-02)
ANG = "#FFC24D"              # yt_0021: ângulo (θ, φ, arcos): âmbar
MAG = "#EA63FF"              # momento p, P, Δp
VEL = "#9C8CFF"              # yt_0021: velocidade (v, ω, v_cm, rpm)
FC = "#5AA2FF"               # yt_0022: torque e força (azul-claro #5AA2FF)
TQ = FC                      # torque τ (mesma família de cor da força; distingue-se pelo desenho)
INT = "#7D8798"              # força interna / tensão (cinza apagado)
JC = "#9CC7FF"               # impulso
STEEL = "#7A8696"
GEO = "#B8C4DA"
VETC = "#D2823A"              # yt_0021 v3: vetores de posição/deslocamento (r⃗, r⃗′, d⃗): laranja queimado, legível sobre o aço claro e sobre o fundo
DIM = "#8FA3C4"
PANEL = "#0E2A52"
BLUE_L = "#7FB2FF"
TERRA = "#4A5262"            # Terra / chão como corpo: aço mais escuro
APAGADO = "#6B7788"          # conta errada riscada
GELO = "#7FB2FF"
CM_COL = WHITE_              # cruz do ⊕ (branca, fina)
CM_A, CM_B = "#35D9FF", "#EA63FF"   # v3: o ⊕ é o degradê ciano → magenta da marca (exclusivo: nenhuma grandeza usa degradê, G15)
CMC = "#8BE9FF"              # posição do ⊕ nas contas (R⃗_cm, X, Y, X_cm, R⃗₀): ciano-claro
RAST = "#9FB4D6"             # rastros finos dos corpos (aço-azulado)
VREL = "#A898FF"             # yt_0019: velocidade relativa ao foguete/carrinho/esteira (v_ex, u_rel): violeta clareado 35% (mix(VEL, 0.35))
ACC = "#3FE08B"              # v7: aceleração (a, g e as setas de aceleração): verde da corrente dos outros vídeos (não amarelo)


def mix(c, w):
    return interpolate_color(ManimColor(c), ManimColor(WHITE_), w).to_hex()


def escuro(c, w):
    return interpolate_color(ManimColor(c), ManimColor(BACKGROUND_COLOR), w).to_hex()


T_HL, T_MAIN, T_LAB, T_SMALL = 44, 34, 26, 22
M_MAIN, M_MID, M_REF, M_LAB = 68, 56, 46, 40
FPS = 15
FRAC = 0.02 / FPS            # folga p/ np.arange não criar um quadro extra

AUDITORIA = os.environ.get("AUDITORIA") == "1"
STILL = float(os.environ["STILL"]) if os.environ.get("STILL") else None   # still num instante (use com -s)

ANC = json.loads((AQUI / "ancoras.json").read_text(encoding="utf-8"))["ancoras"]


SYNC = os.environ.get("SYNC", "final")      # v9: "medir" (passe a seco: mede o tempo nominal de cada trecho) | "final" (encaixa cada trecho na voz)
LEAD = 0.12                                  # v9: a imagem começa ~0,12 s antes da palavra; tolerância -0,15 s … +0,20 s


def plano(A, W, D):
    """(escala das animações, escala das esperas) para encaixar um trecho (A s de animação + W s de espera) em D s (copiado do yt_0010/yt_0018)."""
    if A + W < 1e-6:
        return 1.0, 1.0
    if D >= A + W:
        s_ = min(1.8, max(1.0, (D / (A + W)) ** 0.5))
        return s_, (max(1.0, (D - s_ * A) / W) if W > 1e-6 else 1.0)
    wp = max(0.15 * W, D - A)
    if A + wp <= D + 1e-6:
        return 1.0, wp / W if W > 1e-6 else 1.0
    return max(0.5, (D - wp) / A), (wp / W if W > 1e-6 else 1.0)


def poeira_estelar(clk, n=200, seed=19):
    """v10 R-M: campo de estrelas minúsculas à deriva (3 camadas, parallax) atrás de todo o conteúdo. Movimento contínuo e discreto; sem texto, sem física."""
    rng = np.random.default_rng(seed)
    xs, ys = rng.uniform(-8.4, 8.4, n), rng.uniform(-4.7, 4.7, n)
    cam = rng.integers(0, 3, n)
    vel = np.array([0.16, 0.30, 0.52])[cam] * rng.uniform(0.85, 1.15, n)
    rad = np.array([0.010, 0.016, 0.022])[cam]
    op = np.array([0.18, 0.28, 0.40])[cam]
    pts = [Dot(P3(xs[i], ys[i]), radius=float(rad[i]), color="#DCE8FF").set_opacity(float(op[i])) for i in range(n)]
    g = VGroup(*pts)
    g._fundo = True
    for d_ in pts:
        d_._fundo = True
    g.set_z_index(-60)

    def f_(m):
        t = clk.get_value()
        for i, d_ in enumerate(m.submobjects):
            x = ((xs[i] - vel[i] * t + 8.4) % 16.8) - 8.4
            d_.move_to(P3(x, ys[i] + 0.06 * math.sin(0.5 * t + i)))
    f_(g)
    g.add_updater(f_)
    return g


def dur(aid):
    return ANC[aid]["dur"]


# ── texto e matemática ───────────────────────────────────────────────────────────────────────────────────
def txt(s, size=T_MAIN, color=WHITE_, op=1.0, bold=False):
    """Texto editorial: Space Grotesk em CAIXA ALTA (símbolos matemáticos vão em MathTex, nunca aqui)."""
    s = s.upper()
    if bold:
        m = official_text(s, DISPLAY_FONT, BOLD, size, oversample=2, color=color).set_opacity(op)
    else:
        m = screen_text(s, size, color=color, oversample=4 if len(s) < 34 else 2).set_opacity(op)
    m._tam = size
    m._s, m._bold = s, bold
    return m


def rot(s, size=30, color=WHITE_, op=1.0):
    """Rótulo de massa/número no texto do canal (Space Grotesk), sem caixa alta: `1 kg`, `60 kg`, `2`."""
    m = screen_text(s, size, color=color, oversample=4).set_opacity(op)
    m._tam = size
    m._s, m._rot = s, True
    return m


_MEMO = {}


def memo(chave, fazer):
    """Cópia de um mobject criado uma vez só (textos dentro de always_redraw: criar Text a cada quadro é caro)."""
    if chave not in _MEMO:
        _MEMO[chave] = fazer()
    return _MEMO[chave].copy()


def mtxt(s, size=T_MAIN, color=WHITE_, op=1.0, bold=False):
    return memo(("txt", s, size, color, bold), lambda: txt(s, size, color, 1.0, bold)).set_opacity(op)


def mrot(s, size=30, color=WHITE_, op=1.0):
    """rot() guardado (rótulos e números dentro de camadas vivas: unidade do SI em minúscula, G9)."""
    m = memo(("rot", s, size, color), lambda: rot(s, size, color))
    m._tam = size
    return m.set_opacity(op)


def mtex(s, cor=WHITE_, size=M_MID):
    m = memo(("tex", s, cor, size), lambda: MathTex(s, font_size=size, color=cor))
    m._partes = [(s, cor)]
    return m


def tex(s, cor=WHITE_, size=M_MID):
    return MathTex(s, font_size=size, color=cor)


def Mc(*pares, size=M_MID, w=None):
    """MathTex em partes coloridas: cada par é (tex, cor|None). Cada parte precisa ser um TeX completo."""
    partes = [p[0] if isinstance(p, tuple) else p for p in pares]
    cores = [p[1] if isinstance(p, tuple) else None for p in pares]
    m = MathTex(*partes, font_size=size, color=WHITE_)
    for sub, c in zip(m.submobjects, cores):
        if c:
            sub.set_color(c)
    if w and m.width > w:
        m.scale_to_fit_width(w)
    m._partes = [(t, c or WHITE_) for t, c in zip(partes, cores)]
    return m


_NG = {}


def ng(tex_):
    """Quantos glifos um pedaço de TeX gera (sozinho)."""
    if tex_ not in _NG:
        _NG[tex_] = len(MathTex(tex_)[0]) if tex_.strip() else 0
    return _NG[tex_]


_MT_INIT = MathTex.__init__
_FORTES = {str(c).upper() for c in (VEL, VREL, MAS, FC, ACC, HEAT, MAG, KC)}


def _mt_init(self, *a, **k):
    """v7 #25/#30: MathTex de uma cor saturada ganha contorno da mesma cor (a 960×540 o glifo fino de v_ex lavava sobre painel e fundo)."""
    _MT_INIT(self, *a, **k)
    c = k.get("color")
    if c is not None and str(c).upper() in _FORTES:
        self.set_stroke(c, width=1.4, background=False)


MathTex.__init__ = _mt_init
_REF_M = {}


def _massas_em_compostos(m, partes, idx, cores, size, COMP):
    """v7 #15/#33: massa (m, m_0, m_f, m_{02}, dm, P, f, f_1, f_2) dentro de ln, frac e int sai âmbar. Acha os glifos do tamanho principal por forma
    (a ordem do SVG segue a da string) e pareia com os tokens da string, em ordem; subíndice e o 'd' do dm acompanham."""
    for sym, pad in (("m", r"(?<![A-Za-z\\])(d?)m(?:_\{([^}]*)\}|_([0-9A-Za-z]))?(?![A-Za-z])"),
                     ("P", r"(?<![A-Za-z\\])()P(?:_\{([^}]*)\}|_([0-9A-Za-z]))?(?![A-Za-z])"),
                     ("f", r"(?<![A-Za-z\\_])()f(?:_\{([^}]*)\}|_([0-9A-Za-z]))?(?![A-Za-z])")):
        key = (sym, size)
        if key not in _REF_M:
            _REF_M[key] = MathTex(sym, font_size=size)[0][0]
        ref = _REF_M[key]
        rp = ref.points - ref.get_center()
        for i, t in enumerate(partes):
            if i in cores or t in COMP or "mathrm" in t or cor_esperada(t) is not None:
                continue
            toks = [mt for mt in _re.finditer(pad, t)]
            if not toks:
                continue
            ms = []
            for j in idx[i]:
                g_ = m[0][j]
                if g_.width < 1e-6 or g_.height < 1e-6:
                    continue
                if sym == "m":                                                        # 'm' também em índices/limites (outro tamanho óptico): forma por razão e escala
                    k_ = g_.height / ref.height
                    if 0.4 < k_ < 1.08 and abs((g_.width / g_.height) / (ref.width / ref.height) - 1) < 0.16:
                        ms.append(j)
                elif g_.points.shape == ref.points.shape and np.abs((g_.points - g_.get_center()) - rp).max() < 2e-3:
                    ms.append(j)
            if len(ms) != len(toks):
                print(f"[aviso] massas em composto ({sym}): {len(toks)} tokens × {len(ms)} glifos em {t!r}")
                continue
            for mt, j in zip(toks, ms):
                gl = [j]
                if mt.group(1):
                    gl.append(j - 1)
                sub = mt.group(2) if mt.group(2) is not None else (mt.group(3) or "")
                gl += [j + 1 + k for k in range(len(sub.replace("\\", "")))]
                for g_ in gl:
                    m[0][g_].set_color(MAS)
                    m[0][g_].set_stroke(MAS, width=1.8, background=False)


def eqp(*partes, size=M_MID, cores=None):
    """MathTex de string única montado por partes, com o índice de glifos de cada parte (para TransformByGlyphMap sem contar à mão).
    Retorna (MathTex, lista de listas de índices). `cores`: {índice da parte: cor} (G12: cor por grandeza)."""
    m = MathTex(" ".join(partes), font_size=size, color=WHITE_)          # yt_0021: espaço entre partes (\omega + r não vira \omegar)
    idx, k = [], 0
    for t in partes:
        n = ng(t)
        idx.append(list(range(k, k + n)))
        k += n
    assert k == len(m[0]), f"glifos {k} != {len(m[0])} em {''.join(partes)}"
    cores = dict(cores or {})
    for i, t in enumerate(partes):                          # v5 §3.2: toda grandeza com a cor dela (m, dm em âmbar; v, a, F…); branco só para estrutura
        if i not in cores:
            ce = cor_esperada(t)
            if ce and len(ce) == 1 and ce[0] != WHITE_:
                cores[i] = ce[0]
    COMP = {r"m\,dv": [(0, MAS), (1, VEL), (2, VEL)], r"v\,dm": [(0, VEL), (1, MAS), (2, MAS)], r"dm\,dv": [(0, MAS), (1, MAS), (2, VEL), (3, VEL)],
            r"v_{ex}\,dm": [(0, VREL), (1, VREL), (2, VREL), (3, MAS), (4, MAS)], r"m\,dm": [(0, MAS), (1, MAS), (2, MAS)]}
    for i, t in enumerate(partes):
        if i not in cores and t in COMP:
            for off, c in COMP[t]:
                m[0][idx[i][off]].set_color(c)
    for i, c in cores.items():
        for j in idx[i]:
            m[0][j].set_color(c)
    tinge(m, pular={j for i in cores for j in idx[i]})                     # yt_0021: letras pela forma do glifo
    for i, c in list(cores.items()) + [(i, None) for i, t in enumerate(partes) if t in COMP and i not in cores]:   # v5: contorno da mesma cor recupera a saturação do glifo fino a 960×540
        for j in idx[i]:
            gl = m[0][j]
            gl.set_stroke(gl.get_fill_color(), width=1.8, background=False)
    m._partes = [(t, (cores or {}).get(i) or (_cor_dom(VGroup(*[m[0][j] for j in idx[i]])) if idx[i] else WHITE_)) for i, t in enumerate(partes)]
    m._gl = list(zip(partes, idx))
    return m, idx


# ── cor por token (G12, handoff v3 §1.1): a cor esperada de cada grandeza (None = parte composta, não conferida) ───────────────
import re as _re
_NUM = r"[-+−]?\\?,?[0-9{},.]+"
_REGRAS = [   # yt_0022 (handoff §5.1): número com unidade herda a cor da grandeza; as letras são pintadas por tinge() (forma do glifo)
    ((FC,), (_NUM + r"\\ ?\\mathrm\{N\}", _NUM + r"\\ ?\\mathrm\{N\\cdot ?m\}", _NUM + r"\\ ?\\mathrm\{N\\,m\}")),
    ((MAS,), (_NUM + r"\\ ?\\mathrm\{k?g\}", _NUM + r"\\ ?\\mathrm\{kg\\cdot ?m\^2\}", _NUM + r"\\ ?\\mathrm\{kg\\,m\^2\}")),
    ((VEL,), (_NUM + r"\\ ?\\mathrm\{m/s\}", _NUM + r"\\ ?\\mathrm\{rad/s\}", _NUM + r"\\ ?\\mathrm\{RPM\}", _NUM + r"\\ ?\\mathrm\{rpm\}")),
    ((ACC,), (_NUM + r"\\ ?\\mathrm\{m/s\^2\}", _NUM + r"\\ ?\\mathrm\{rad/s\^2\}")),
    ((KC,), (_NUM + r"\\ ?\\mathrm\{J\}", _NUM + r"\\ ?\\mathrm\{kW\}", _NUM + r"\\ ?\\mathrm\{W\}", _NUM + r"\\ ?\\mathrm\{cv\}")),
    ((GEO,), (_NUM + r"\\ ?\\mathrm\{c?m\}",)),
    ((WHITE_,), (r"[=+\-()<>]", r"\\cdot")),
]

# ── tinge(): cor por token nas letras de qualquer MathTex, pela FORMA do glifo (três tamanhos ópticos do Computer Modern) ──────────────
LETRA_COR = {r"\tau": TQ, "F": FC, "N": FC, "T": FC,
             "m": MAS, "M": MAS, "I": MAS, r"\lambda": MAS, r"\sigma": MAS, r"\rho": MAS, "c": MAS,
             "v": VEL, r"\omega": VEL, "K": KC, "U": KC, "W": KC, "P": KC,
             "g": ACC, r"\alpha": ACC, "a": ACC, r"\theta": ANG, r"\varphi": ANG,
             "r": GEO, "R": GEO, "L": GEO, "s": GEO, "x": GEO, "y": GEO, "z": GEO, "k": GEO, "h": GEO, "d": GEO}
_SIMB = list(LETRA_COR) + list("0123456789") + ["i", "j", "A", "B", "O", "n", "b"]
_REFS = None


def _forma(g):
    p = g.points[:, :2]
    c = (p.max(0) + p.min(0)) / 2
    h = max(p[:, 1].max() - p[:, 1].min(), 1e-6)
    return (p - c) / h


def _refs():
    global _REFS
    if _REFS is None:
        _REFS = {}
        for s_ in _SIMB:
            m = MathTex(s_ + "_{" + s_ + "_{" + s_ + "}}", font_size=48)
            for k, g in enumerate(m[0][:3]):
                _REFS.setdefault(len(g.points), []).append((s_, k, _forma(g)))
        pr = MathTex("r'", font_size=48)[0][1]
        _REFS.setdefault(len(pr.points), []).append(("'", 1, _forma(pr)))
        mv = MathTex(r"\vec r", font_size=48)[0]
        vr = mv[0] if mv[0].get_center()[1] > mv[1].get_center()[1] else mv[1]
        _REFS.setdefault(len(vr.points), []).append(("vec", 1, _forma(vr)))
    return _REFS


def _id_glifo(g):
    if not len(g.points):
        return None
    f = _forma(g)
    for s_, k, rf in _refs().get(len(g.points), []):
        if rf.shape == f.shape and np.abs(rf - f).max() < 0.03:
            return s_, k
    return None


def tinge(m, pular=()):
    """Pinta as letras de uma MathTex de string única com a cor da grandeza (LETRA_COR). Índice/expoente herda a cor da letra principal à
    esquerda (I_x, v_{cm}, r_i^2, I_{disco}, I_{rec}): v3 — o subscrito de PALAVRA (letras sem tamanho óptico conhecido ou com outra regra de cor) herda sempre,
    reconhecido pela geometria (menor que a base e abaixo/acima dela). 'd' de diferencial toma a cor do que vem depois (dm rosa, dx GEO); número e operador ficam brancos.
    yt_0022: \vec r ganha VETC (#D2823A); \vec \tau e \vec F ganham FC (#5AA2FF)."""
    gls = m[0] if len(m) and len(m[0]) else m
    ids = [_id_glifo(g) for g in gls]
    herda, base = None, None
    barras = [(g.get_left()[0], g.get_right()[0], g.get_center()[1]) for g in gls if g.height < 0.035 and g.width > 0.08]       # traços de fração

    def em_fracao(g):
        gx, gy = g.get_center()[0], g.get_center()[1]
        return any(x0 - 0.03 <= gx <= x1 + 0.03 and abs(gy - by) < 0.45 for x0, x1, by in barras)

    def pinta(g, c, k):
        g.set_color(c)
        g.set_stroke(c, width=1.6 if k == 0 else 1.0, background=False)
    vecs = {j for j, i_ in enumerate(ids) if i_ and i_[0] == "vec"}
    for j, (g, i_) in enumerate(zip(gls, ids)):
        if j in vecs:
            continue
        gh, gy = g.height, g.get_center()[1]
        gb = gy - gh / 2
        sub = base is not None and gh < 0.85 * base[0] and (gb < base[2] - 0.02 or gb > base[1]) and not em_fracao(g)
        if i_ is None:
            if herda is not None and sub:
                if j not in pular:
                    pinta(g, herda, 1)
            else:
                herda, base = None, None
            continue
        s_, k = i_
        jv = next((v for v in vecs if abs(gls[v].get_center()[0] - g.get_center()[0]) < max(0.28, 0.9 * g.width)
                   and 0.0 < gls[v].get_center()[1] - gy < 1.6 * gh), None) if k == 0 else None
        if k == 0:
            if s_ == "d":
                prox = ids[j + 1] if j + 1 < len(ids) else None
                c = LETRA_COR.get(prox[0]) if prox and prox[1] == 0 and prox[0] != "d" else GEO
                c = c or GEO
            elif jv is not None and s_ == "r":
                c = VETC
            else:
                c = LETRA_COR.get(s_)
            herda, base = c, (gh, gy, gb)
            if jv is not None and c is not None and jv not in pular:
                pinta(gls[jv], c, 1)
        else:
            c = herda if (herda is not None and not em_fracao(g)) else LETRA_COR.get(s_)
        if c is not None and j not in pular:
            pinta(g, c, k)
    return m


def T(s, size=M_LAB, cor=None):
    """MathTex de string única com cor por token (rótulos e linhas curtas)."""
    m = MathTex(s, font_size=size, color=WHITE_)
    if cor is not None:
        m.set_color(cor)
    else:
        tinge(m)
    m._partes = [(s, _cor_dom(m))]
    return m


def _cor_dom(ms):
    from collections import Counter
    cs = Counter(ManimColor(g.get_fill_color()).to_hex().upper() for g in ms.family_members_with_points())
    return cs.most_common(1)[0][0] if cs else WHITE_


def cor_esperada(t):
    """Cores aceitas para o token t (tupla) ou None se a parte é composta (não conferida)."""
    t = t.strip()
    for cores, pads in _REGRAS:
        if any(_re.fullmatch(p, t) for p in pads):
            return cores
    return None


def caixa(m, cor=BLUE_L, buff=0.18):
    """Caixa de resultado (G11): PANEL a 85% com borda na cor da grandeza (BLUE_L se não houver uma). Nunca branca."""
    r = RoundedRectangle(corner_radius=0.1, width=m.width + 2 * buff, height=m.height + 2 * buff).move_to(m) \
        .set_fill(PANEL, 0.85).set_stroke(cor, 2.5)
    r._fundo = r._caixa = True
    return r.set_z_index(m.z_index - 1 if m.z_index else -1)


def cartao(*linhas, size=28, cor=BLUE_L):
    """Frase explicativa em cartão PANEL com texto branco (no lugar de texto DIM solto)."""
    t = VGroup(*[txt(l, size) for l in linhas]).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
    r = RoundedRectangle(corner_radius=0.1, width=t.width + 0.44, height=t.height + 0.32).move_to(t).set_fill(PANEL, 0.9).set_stroke(cor, 2)
    r._fundo = True
    return VGroup(r, t).set_z_index(20)


def linha(*itens, buff=0.2, size=T_MAIN, color=WHITE_):
    """Linha mista: str vira txt(); mobjects entram como estão (alinhados pela base visual)."""
    return VGroup(*[txt(i, size, color) if isinstance(i, str) else i for i in itens]).arrange(RIGHT, buff=buff)


def P3(x, y):
    return np.array([x, y, 0.0])


def arrow(a, b, color=WHITE_, width=5, z=8, tip=0.2, op=1.0):
    a, b = np.asarray(a, dtype=float), np.asarray(b, dtype=float)
    L = np.linalg.norm(b - a)
    if L < 0.03:
        return VMobject()
    if L < 3 * tip:                     # ponta sempre visível
        b = a + (b - a) / L * 3 * tip
    m = Arrow(a, b, buff=0, color=color, stroke_width=width, tip_length=tip, max_tip_length_to_length_ratio=0.45,
              max_stroke_width_to_length_ratio=50)
    return m.set_opacity(op).set_z_index(z)


def placa(w, h, centro, op=0.05, borda=0.24):
    return RoundedRectangle(corner_radius=0.12, width=w, height=h).set_stroke(WHITE_, 1.4, opacity=borda) \
        .set_fill(WHITE_, op).move_to(centro).set_z_index(-2)


def risco(m, cor=APAGADO, w=4):
    """Traço diagonal sobre um mobject (item riscado)."""
    r_ = Line(m.get_corner(DL) + 0.04 * UR, m.get_corner(UR) - 0.04 * UR).set_stroke(cor, w).set_z_index(30)
    r_._risco = True                                                    # o risco é sobre o texto de propósito (fora da auditoria)
    return r_


class Corpo(VGroup):
    """Bloco 2D chato: aço, contorno claro e filete interno (sem 3D falso)."""

    def __init__(self, nome, cor, lado, alt=None, size=36):
        super().__init__()
        alt = alt or lado
        self.lado, self.alt = lado, alt
        f = RoundedRectangle(corner_radius=0.04, width=lado, height=alt).set_stroke(mix(cor, 0.5), 2).set_fill(cor, 1.0)
        ins = min(0.07, 0.12 * min(lado, alt))
        filete = RoundedRectangle(corner_radius=0.03, width=max(lado - 2 * ins, 0.02), height=max(alt - 2 * ins, 0.02)) \
            .set_stroke(WHITE_, 1, opacity=0.35).set_fill(cor, 0).move_to(f)
        self.front = f
        self.add(f, filete)
        if nome:
            esc = cor == GEO
            self.lab = MathTex(nome, font_size=size, color=BACKGROUND_COLOR if esc else WHITE_).move_to(f)
            self.add(self.lab)

    def at(self, x, yb):
        self.shift(P3(x, yb + self.alt / 2) - self.front.get_center())
        return self


def bola(r=0.28, cor=STEEL):
    c = Circle(radius=r).set_stroke(mix(cor, 0.5), 2).set_fill(cor, 1.0)
    return VGroup(c, Circle(radius=r * 0.78).set_stroke(WHITE_, 1, opacity=0.3).set_fill(cor, 0)).set_z_index(5)


def dica(*linhas, size=28):
    """Cartão PANEL com borda BLUE_L no canto inferior direito: 'DICA' em ciano e a frase em maiúsculas. Cada linha é uma str
    ou uma lista de str/mobjects (símbolos matemáticos entram como MathTex, nunca dentro de txt())."""
    corpo = VGroup()
    for l in linhas:
        corpo.add(txt(l, size) if isinstance(l, str) else linha(*l, buff=0.1, size=size))
    corpo.arrange(DOWN, buff=0.14, aligned_edge=LEFT)
    tag = txt("DICA", 24, color=CYAN, bold=True)
    g = VGroup(tag, corpo).arrange(DOWN, buff=0.16, aligned_edge=LEFT)
    cx_ = RoundedRectangle(corner_radius=0.12, width=g.width + 0.6, height=g.height + 0.44).set_stroke(BLUE_L, 2) \
        .set_fill(PANEL, 0.97).move_to(g)
    cx_._fundo = True
    return VGroup(cx_, g).set_z_index(35).to_corner(DR, buff=0.5)


def fronteira(w, h, centro, rotulo="SISTEMA", lado=UL, size=20, op=0.62):
    """Fronteira tracejada do sistema (retângulo arredondado) com o rótulo pequeno no canto de fora."""
    r = RoundedRectangle(corner_radius=0.3, width=w, height=h).move_to(centro).set_stroke(WHITE_, 2.2, opacity=op)
    d = DashedVMobject(r, num_dashes=max(24, int((w + h) * 5)), dashed_ratio=0.55).set_z_index(1)
    g = VGroup(d)
    if rotulo:
        lab = (txt(rotulo, size, color=WHITE_, op=0.8) if isinstance(rotulo, str) else
               linha(*rotulo, size=size, buff=0.1).set_opacity(0.8)).next_to(r.get_corner(lado), UP, buff=0.1)
        lab.align_to(r, LEFT if lado[0] <= 0 else RIGHT).shift((0.25 if lado[0] <= 0 else -0.25) * RIGHT)
        g.add(lab)
    return g


def mais(size=28, s="+"):
    """Conectivo matemático (+, =) para textos de tela montados com linha()."""
    return MathTex(s, font_size=size, color=WHITE_)


def chao(x0, x1, y, cor=GEO, op=0.5, seed=3, dens=2.2):
    """Chão com textura: linha + riscos curtos e pedrinhas abaixo (fixos)."""
    rng = np.random.default_rng(seed)
    g = VGroup(Line(P3(x0, y), P3(x1, y)).set_stroke(cor, 2.5, opacity=op))
    n = int((x1 - x0) * dens)
    for _ in range(n):
        x = rng.uniform(x0 + 0.1, x1 - 0.2)
        dy = rng.uniform(0.08, 0.3)
        L = rng.uniform(0.08, 0.22)
        g.add(Line(P3(x, y - dy), P3(x + L, y - dy)).set_stroke(cor, 1.5, opacity=op * 0.45))
    for _ in range(n // 2):
        g.add(Dot(P3(rng.uniform(x0 + 0.1, x1 - 0.1), y - rng.uniform(0.06, 0.32)), radius=0.022, color=cor).set_opacity(op * 0.5))
    return g.set_z_index(0)


def gelo(x0, x1, y, h=0.26, seed=5):
    """Faixa de gelo azulada (lago congelado / chão de gelo) com reflexos finos."""
    rng = np.random.default_rng(seed)
    g = VGroup(Rectangle(width=x1 - x0, height=h).move_to(P3((x0 + x1) / 2, y - h / 2)).set_stroke(width=0).set_fill(GELO, 0.16),
               Line(P3(x0, y), P3(x1, y)).set_stroke(mix(GELO, 0.4), 2.5, opacity=0.8))
    for _ in range(int((x1 - x0) * 1.6)):
        x = rng.uniform(x0 + 0.1, x1 - 0.5)
        g.add(Line(P3(x, y - rng.uniform(0.05, h - 0.04)), P3(x + rng.uniform(0.2, 0.5), y - rng.uniform(0.05, h - 0.04)))
              .set_stroke(mix(GELO, 0.5), 1.4, opacity=0.45))
    return g.set_z_index(0)


# ── silhueta humana de perfil (cápsulas preenchidas; nunca linhas) ─────────────────────────────────────────
def capsula2d(a, b, r, cor=STEEL, borda=None):
    a, b = np.asarray(a, float), np.asarray(b, float)
    L = max(np.linalg.norm(b - a), 1e-3)
    c = RoundedRectangle(corner_radius=r * 0.999, width=L + 2 * r, height=2 * r).set_stroke(borda or mix(cor, 0.45), 1.5) \
        .set_fill(cor, 1.0)
    c.rotate(math.atan2(*(b - a)[[1, 0]])).move_to((a + b) / 2)
    return c


POSES = {
    # ângulos a partir da vertical para baixo; positivo = para a frente (rad). tr: inclinação do tronco para a frente.
    "pe": dict(cf=0.04, jf=0.0, ct=-0.04, jt=0.0, bf=0.12, af=0.22, bt=-0.08, at=0.05, tr=0.0),
    "agarra": dict(cf=0.06, jf=0.0, ct=-0.12, jt=-0.12, bf=1.15, af=1.45, bt=0.9, at=1.35, tr=0.08),
    "mira": dict(cf=0.18, jf=0.05, ct=-0.2, jt=-0.2, bf=1.25, af=1.6, bt=0.75, at=1.55, tr=0.05),
    "sentado": dict(cf=1.45, jf=0.15, ct=1.5, jt=0.25, bf=2.6, af=2.95, bt=0.55, at=1.05, tr=-0.05),
    "joga": dict(cf=1.45, jf=0.15, ct=1.5, jt=0.25, bf=2.9, af=3.05, bt=0.45, at=0.9, tr=-0.1),
}


class PessoaPerfil(VGroup):
    """Pessoa de perfil olhando para `sen` (+1 direita). Pés (ou o quadril, se `quadril` for dado) apoiados em y.
    self.pts guarda pontos úteis: mao_f, mao_t, pe_f, pe_t, peito, cabeca, quadril, ombro."""

    def __init__(self, x=0.0, y=0.0, alt=1.9, sen=1, pose="pe", cor=STEEL, quadril=None, extra=None):
        super().__init__()
        k = alt / 1.76
        p = dict(POSES[pose] if isinstance(pose, str) else pose)
        if extra:
            p.update(extra)
        s = sen
        d = lambda a, L: L * k * np.array([math.sin(a) * s, -math.cos(a), 0.0])
        hip = np.array([0.0, 0.95 * k, 0.0])
        ombro = hip + 0.52 * k * np.array([math.sin(p["tr"]) * s, math.cos(p["tr"]), 0.0])
        joelho_f, joelho_t = hip + d(p["cf"], 0.45), hip + d(p["ct"], 0.45)
        tor_f, tor_t = joelho_f + d(p["jf"], 0.44), joelho_t + d(p["jt"], 0.44)
        cot_f, cot_t = ombro + d(p["bf"], 0.29), ombro + d(p["bt"], 0.29)
        mao_f, mao_t = cot_f + d(p["af"], 0.26), cot_t + d(p["at"], 0.26)
        pesc = ombro + 0.07 * k * np.array([math.sin(p["tr"]) * s, 1.0, 0.0])
        cab = ombro + k * np.array([(0.04 + 0.17 * math.sin(p["tr"])) * s, 0.2, 0.0])
        if quadril is None:
            base = min(tor_f[1], tor_t[1]) - 0.045 * k
            off = np.array([x, y - base, 0.0])
        else:
            off = np.array([x, quadril - hip[1], 0.0])
        fundo = escuro(cor, 0.38)

        def perna(j, t, c):
            pe = RoundedRectangle(corner_radius=0.035 * k, width=0.25 * k, height=0.075 * k).set_stroke(mix(c, 0.4), 1.5) \
                .set_fill(c, 1).move_to(t + np.array([0.08 * k * s, -0.01 * k, 0]))
            return VGroup(capsula2d(hip, j, 0.088 * k, c), capsula2d(j, t, 0.062 * k, c), pe)

        def braco(cv, m, c):
            return VGroup(capsula2d(ombro, cv, 0.056 * k, c), capsula2d(cv, m, 0.045 * k, c),
                          Ellipse(width=0.075 * k, height=0.1 * k).set_stroke(mix(c, 0.4), 1.5).set_fill(c, 1).move_to(m))

        self.add(braco(cot_t, mao_t, fundo), perna(joelho_t, tor_t, fundo))
        tronco = VGroup(capsula2d(hip + 0.04 * k * UP, ombro - 0.03 * k * np.array([math.sin(p["tr"]) * s, 1, 0]), 0.155 * k, cor),
                        capsula2d(ombro - 0.02 * k * UP, pesc, 0.045 * k, cor))
        cabeca = Ellipse(width=0.2 * k, height=0.25 * k).set_stroke(mix(cor, 0.45), 1.5).set_fill(cor, 1).move_to(cab)
        nariz = Ellipse(width=0.05 * k, height=0.04 * k).set_stroke(width=0).set_fill(cor, 1).move_to(cab + np.array([0.1 * k * s, -0.01 * k, 0]))
        self.add(perna(joelho_f, tor_f, cor), tronco, nariz, cabeca, braco(cot_f, mao_f, cor))
        for q in (hip, joelho_f, ombro, cot_f):
            self.add(Dot(q, radius=0.03 * k, color=GEO).set_z_index(1))
        self.shift(off)
        self.pts = {n: v + off for n, v in dict(mao_f=mao_f, mao_t=mao_t, pe_f=tor_f, pe_t=tor_t, peito=ombro + d(1.6, 0.12) - 0.15 * k * UP,
                                                cabeca=cab, quadril=hip, ombro=ombro).items()}
        self.k = k


def silhueta(p_, cor=STEEL):
    """G18: a pessoa (PessoaPerfil) vira uma silhueta só de corpo inteiro (união das partes, sem juntas nem pontos), em aço com
    sombreado (claro em cima, escuro embaixo) e o recorte BLUE_L na borda. Guarda .pts do original."""
    partes = [m for m in p_.submobjects if not isinstance(m, Dot)]
    folhas = [x for m in partes for x in m.family_members_with_points() if isinstance(x, VMobject) and not isinstance(x, Dot)]
    try:
        s = Union(*folhas)
    except Exception:                                   # a união falha em algumas poses: as partes, todas no mesmo aço (sem juntas nem pontos)
        s = VGroup(*[f.copy() for f in folhas])
    s.set_fill(["#9AA6B8", "#7A8696", "#3A4252"], 1.0).set_sheen_direction(UP).set_stroke("#7FB2FF", 2.4, opacity=0.8)   # luz B
    s._degrade = "aco"
    s.pts, s.k = dict(p_.pts), p_.k
    return s


def andar(fase, amp=0.42):
    """Pose de caminhada (perfil) na fase `fase` (rad): pernas e braços alternados, joelho dobrando no balanço."""
    a = amp * math.sin(fase)
    dob = lambda u: -0.6 * max(0.0, math.sin(u + 0.6))
    return dict(cf=a, jf=a + dob(fase), ct=-a, jt=-a + dob(fase + PI), bf=-0.6 * a, af=-0.6 * a + 0.35, bt=0.6 * a, at=0.6 * a + 0.35,
                tr=0.06)


# ── cavalo de perfil, patas articuladas (dois segmentos), preenchido em aço ─────────────────────────────────
CAV_PERNAS = ((-0.95, 1.5, 0.0, True), (0.72, 1.52, 0.5 * PI, True), (-0.7, 1.5, PI, False), (0.95, 1.52, 1.5 * PI, False))


def cavalo(fase=0.0, passo=0.0, cor=STEEL):
    """Cavalo virado para a direita, cascos em y≈0. `fase` (rad) do ciclo de passo; `passo` = 0 parado … 1 passo cheio.
    Retorna (VGroup, pontos) com 'peito' (peitoral), 'traseira', 'cascos' (lista dos 4 cascos), 'dorso'."""
    borda = mix(cor, 0.45)
    longe = escuro(cor, 0.35)
    g_tras, g_frente = VGroup(), VGroup()
    cascos = []
    L1, L2 = 0.74, 0.72
    for x, y, ph, perto in CAV_PERNAS:
        u = fase + ph
        a1 = passo * 0.3 * math.sin(u)
        dobra = passo * 0.75 * max(0.0, math.sin(u + 1.2))
        dianteira = x > 0
        a2 = a1 - dobra if dianteira else a1 + 0.45 * dobra
        top = P3(x, y)
        jo = top + L1 * P3(math.sin(a1), -math.cos(a1))
        pe = jo + L2 * P3(math.sin(a2), -math.cos(a2))
        c = cor if perto else longe
        casco = RoundedRectangle(corner_radius=0.04, width=0.25, height=0.13).set_stroke(width=0).set_fill(GEO if perto else escuro(GEO, 0.3), 1) \
            .move_to(pe + P3(0.02, -0.02))
        perna = VGroup(capsula2d(top, jo, 0.13, c, borda), capsula2d(jo, pe, 0.08, c, borda), casco)
        (g_frente if perto else g_tras).add(perna)
        cascos.append(pe + P3(0.02, -0.085))
    base = min(p[1] for p in cascos)
    corpo = Ellipse(width=2.55, height=1.08).set_stroke(borda, 2).set_fill(cor, 1).move_to(P3(0, 1.78))
    anca = Ellipse(width=1.0, height=1.0).set_stroke(width=0).set_fill(cor, 1).move_to(P3(-0.85, 1.86))
    pesc = Polygon(P3(0.7, 1.98), P3(1.05, 2.4), P3(1.5, 3.05), P3(1.85, 2.85), P3(1.45, 2.05), P3(1.15, 1.58)) \
        .set_stroke(borda, 2).set_fill(cor, 1)
    cab = Polygon(P3(1.5, 3.05), P3(1.75, 3.25), P3(2.42, 2.78), P3(2.52, 2.56), P3(2.32, 2.44), P3(1.75, 2.68)) \
        .set_stroke(borda, 2).set_fill(cor, 1)
    orelha = Polygon(P3(1.62, 3.1), P3(1.7, 3.45), P3(1.82, 3.15)).set_stroke(borda, 2).set_fill(cor, 1)
    crina = Polygon(P3(0.82, 2.12), P3(1.5, 3.14), P3(1.42, 2.76), P3(1.0, 2.05)).set_stroke(width=0).set_fill(GEO, 0.85)
    cauda = Polygon(P3(-1.2, 2.05), P3(-1.55, 1.88), P3(-1.78, 1.1), P3(-1.56, 1.14), P3(-1.36, 1.66)).set_stroke(width=0).set_fill(GEO, 0.85)
    olho = Dot(P3(2.03, 2.86), radius=0.04, color=BACKGROUND_COLOR)
    peitoral = RoundedRectangle(corner_radius=0.06, width=0.16, height=0.72).set_stroke(width=0).set_fill(GEO, 1).rotate(-0.35) \
        .move_to(P3(1.12, 1.7))
    tirante = Line(P3(1.05, 1.62), P3(-1.25, 1.62)).set_stroke(GEO, 3.5)
    g = VGroup(cauda, g_tras, anca, corpo, pesc, crina, cab, orelha, olho, g_frente, tirante, peitoral).shift(P3(0, -base))
    pts = dict(peito=P3(1.12, 1.62 - base), traseira=P3(-1.25, 1.62 - base), dorso=P3(0.0, 2.4 - base),
               cascos=[c + P3(0, -base) for c in cascos], cabeca=P3(1.9, 3.3 - base))
    return g, pts


def pedra(cor=TERRA):
    """Pedra grande facetada; base em y = 0, frente (onde amarra a corda) em x≈1,0."""
    contorno = [P3(-1.05, 0.0), P3(-1.18, 0.55), P3(-0.85, 1.12), P3(-0.1, 1.32), P3(0.62, 1.12), P3(1.05, 0.62), P3(1.0, 0.0)]
    base = Polygon(*contorno).set_stroke(mix(cor, 0.4), 2).set_fill(cor, 1)
    f1 = Polygon(P3(-0.85, 1.12), P3(-0.1, 1.32), P3(0.15, 0.8), P3(-0.55, 0.62)).set_stroke(mix(cor, 0.25), 1.2).set_fill(mix(cor, 0.12), 1)
    f2 = Polygon(P3(0.15, 0.8), P3(-0.1, 1.32), P3(0.62, 1.12), P3(1.05, 0.62), P3(0.55, 0.42)).set_stroke(mix(cor, 0.25), 1.2) \
        .set_fill(mix(cor, 0.06), 1)
    f3 = Polygon(P3(-1.18, 0.55), P3(-0.55, 0.62), P3(-0.3, 0.0), P3(-1.05, 0.0)).set_stroke(mix(cor, 0.2), 1.2).set_fill(escuro(cor, 0.15), 1)
    gancho = Circle(radius=0.08).set_stroke(GEO, 3).set_fill(cor, 0).move_to(P3(1.06, 0.55))
    return VGroup(base, f3, f1, f2, gancho)


# ── objetos pequenos ─────────────────────────────────────────────────────────────────────────────────────
def rifle(ang=0.0, comp=1.5, cor=STEEL):
    """Rifle preenchido (coronha, ação, cano), apontando no ângulo `ang`; origem na coronha (ombro). Retorna (VGroup, boca)."""
    g = VGroup(
        Polygon(P3(0, -0.06), P3(0.32, -0.04), P3(0.42, 0.05), P3(0.0, 0.1), P3(-0.04, -0.02)).set_stroke(mix(cor, 0.45), 1.5).set_fill(escuro(cor, 0.15), 1),
        RoundedRectangle(corner_radius=0.03, width=0.4, height=0.12).set_stroke(mix(cor, 0.45), 1.5).set_fill(cor, 1).move_to(P3(0.58, 0.04)),
        RoundedRectangle(corner_radius=0.02, width=comp - 0.7, height=0.055).set_stroke(mix(cor, 0.45), 1.2).set_fill(mix(cor, 0.2), 1)
        .move_to(P3(0.78 + (comp - 0.7) / 2, 0.06)),
        Polygon(P3(0.5, -0.02), P3(0.55, -0.14), P3(0.62, -0.14), P3(0.62, -0.02)).set_stroke(width=0).set_fill(cor, 1))
    g.rotate(ang, about_point=ORIGIN)
    boca = P3((comp + 0.08) * math.cos(ang) - 0.06 * math.sin(ang), (comp + 0.08) * math.sin(ang) + 0.06 * math.cos(ang))
    return g.set_z_index(6), boca


def bala_mob(ang=0.0, cor=GEO):
    return RoundedRectangle(corner_radius=0.035, width=0.2, height=0.07).set_stroke(width=0).set_fill(cor, 1).rotate(ang).set_z_index(7)


def ima(cor=STEEL):
    """Ímã em U preenchido (pontas claras)."""
    arco = AnnularSector(inner_radius=0.12, outer_radius=0.26, angle=PI, start_angle=PI).set_stroke(mix(cor, 0.45), 1.5).set_fill(cor, 1)
    perna_e = Rectangle(width=0.14, height=0.22).set_stroke(mix(cor, 0.45), 1.5).set_fill(cor, 1).move_to(P3(-0.19, 0.11))
    perna_d = perna_e.copy().move_to(P3(0.19, 0.11))
    ponta_e = Rectangle(width=0.14, height=0.08).set_stroke(width=0).set_fill(GEO, 1).move_to(P3(-0.19, 0.26))
    ponta_d = ponta_e.copy().move_to(P3(0.19, 0.26))
    return VGroup(arco, perna_e, perna_d, ponta_e, ponta_d).set_z_index(6)


def mola(a, b, n=9, amp=0.14, cor=GEO, w=3):
    """Mola em zigue-zague entre a e b (horizontal)."""
    a, b = np.asarray(a, float), np.asarray(b, float)
    pts = [a]
    for i in range(1, 2 * n):
        u = i / (2 * n)
        pts.append(a + (b - a) * u + P3(0, amp * (1 if i % 2 else -1)))
    pts.append(b)
    return VMobject().set_points_as_corners(pts).set_stroke(cor, w).set_z_index(4)


def flash(centro, r=0.12, cor=WHITE_):
    g = VGroup(Circle(radius=r).set_stroke(cor, 3).move_to(centro))
    g._flash = True                                         # brilho de explosão: não é um marcador de ponto (MARCADORES COLADOS)
    for k in range(8):
        a = k * PI / 4
        g.add(Line(centro + (r + 0.04) * P3(math.cos(a), math.sin(a)), centro + (r + 0.22) * P3(math.cos(a), math.sin(a))).set_stroke(cor, 3))
    return g


_CM_MOLDE = {}


def marcador_cm(centro=ORIGIN, r=0.215, z=30, op=1.0, leve=False):
    """⊕ do centro de massa (cópia de um molde: barato dentro de always_redraw). `leve`: só anel e cruz (fotos fantasma)."""
    if (r, leve) not in _CM_MOLDE:
        m0 = _marcador_cm(ORIGIN, r, z)
        if leve:
            m0.remove(*m0.submobjects[:3])
        _CM_MOLDE[(r, leve)] = m0
    m = _CM_MOLDE[(r, leve)].copy().shift(np.asarray(centro, dtype=float))
    m._cm = True
    if op < 0.999:
        escala_op(m, op)
    return m


def vivo(func):
    """Como always_redraw, mas troca os submobjects a cada quadro em vez de `become` (que alinha pontos e custava ~0,4 s por quadro
    nas camadas sobre o 3D)."""
    g = VGroup()
    g._vivo_ = True

    def upd(m):
        novo = func()
        # o Cairo guarda, no início de cada play, a lista dos membros que se movem: a camada antiga continuaria sendo
        # desenhada até o fim do play (rastro duplicado). Por isso ela fica invisível antes de sair.
        for velho in m.submobjects:
            for x in velho.family_members_with_points():
                if isinstance(x, VMobject):
                    x.set_stroke(opacity=0, family=False)
                    x.set_fill(opacity=0, family=False)
        m.submobjects = [novo]
        m.z_index = novo.z_index
    g.add_updater(upd)
    upd(g)
    return g


def seta(a, b, color=WHITE_, width=5, tip=0.2, op=1.0, z=8):
    """Seta leve (linha + ponta triangular) para camadas redesenhadas a cada quadro; a `arrow()` do kit custa ~15 ms."""
    a, b = np.asarray(a, dtype=float), np.asarray(b, dtype=float)
    L = np.linalg.norm(b - a)
    if L < 0.03:
        return VMobject()
    u = (b - a) / L
    n = np.array([-u[1], u[0], 0.0])
    tl = min(tip, 0.45 * L)
    base = b - u * tl * 0.92
    corpo = VMobject().set_points_as_corners([a, base]).set_stroke(color, width, opacity=op)
    ponta = VMobject().set_points_as_corners([b, b - u * tl + n * tl * 0.55, b - u * tl - n * tl * 0.55, b])         .set_stroke(color, 1, opacity=op).set_fill(color, op)
    return VGroup(corpo, ponta).set_z_index(z)


def grad_cm(u):
    """Cor do degradê do ⊕ em u (0 = ciano, 1 = magenta)."""
    return interpolate_color(ManimColor(CM_A), ManimColor(CM_B), min(1.0, max(0.0, u)))


def _marcador_cm(centro=ORIGIN, r=0.215, z=30, op=1.0):
    """⊕ do centro de massa (v3): glow suave e halo em degradê ciano → magenta (~35%), anel em degradê angular (36 arcos, ciano em cima à
    esquerda, magenta embaixo à direita), cruz branca fina; contorno escuro fino sob o anel e a cruz para ler sobre qualquer fundo.
    Exclusivo do CM (G15)."""
    c = np.asarray(centro, dtype=float)
    esc = BACKGROUND_COLOR
    g = VGroup()
    for rr, o in ((r * 2.25, 0.07), (r * 1.75, 0.13)):                             # glow
        g.add(Circle(radius=rr).set_stroke(width=0).set_fill([CM_A, CM_B], o * op).move_to(c))
    g.add(Circle(radius=r * 1.32).set_stroke(width=0).set_fill([CM_A, CM_B], 0.35 * op).move_to(c))      # halo
    for x in g.submobjects:
        x._halo = True                                                             # brilho translúcido: a auditoria olha o anel e a cruz
    g.add(Circle(radius=r).set_stroke(esc, 6.5, opacity=0.6 * op).move_to(c))
    n, a0 = 36, 0.75 * PI
    for i in range(n):
        th = 2 * PI * i / n
        g.add(Arc(radius=r, start_angle=th, angle=2 * PI / n + 0.02, arc_center=c).set_stroke(grad_cm((1 - math.cos(th - a0)) / 2), 3.4, opacity=op))
    k = 1.22
    cruz = lambda: VGroup(Line(c + r * k * LEFT, c + r * k * RIGHT), Line(c + r * k * DOWN, c + r * k * UP))
    g.add(cruz().set_stroke(esc, 5.0, opacity=0.6 * op), cruz().set_stroke(CM_COL, 2.0, opacity=op))
    g._degrade = "cm"
    return g.set_z_index(z)


def rastro_cm(pts, w=5, op=1.0, n=18):
    """Rastro do ⊕ (v3): degradê ao longo do comprimento (ciano no começo → magenta na ponta), espessura `w`, com glow."""
    pts = np.asarray(pts, dtype=float)
    if len(pts) < 2 or op < 0.01:
        return VGroup()
    L, glow, nucleo = len(pts), VGroup(), VGroup()
    n = max(1, min(n, L - 1))
    for i in range(n):
        a, b = int(i * (L - 1) / n), int((i + 1) * (L - 1) / n)
        seg = pts[a:b + 1]
        if len(seg) < 2:
            continue
        cor = grad_cm(i / max(1, n - 1))
        glow.add(VMobject().set_points_as_corners(seg).set_stroke(cor, w * 2.8, opacity=0.16 * op))
        nucleo.add(VMobject().set_points_as_corners(seg).set_stroke(cor, w, opacity=op))
    g = VGroup(glow, nucleo)
    g._degrade = "rastro"
    return g


def esfera_aco(r=0.3, z=5):
    """Esfera 2D de aço com a luz B (v4 §3.2): gradiente radial #9AA6B8 → #7A8696 → #3A4252 (centro claro deslocado para o alto à
    esquerda), especular branco a 70% no alto à esquerda, recorte #7FB2FF a 35% na borda de baixo à esquerda e toque #EA63FF a 12% na
    borda de cima à direita. Uma função só para todos os corpos 2D (haltere, molas, massas do plano, blocos)."""
    g = VGroup()
    c0, c1, c2 = ManimColor("#3A4252"), ManimColor("#7A8696"), ManimColor("#9AA6B8")
    n = 16
    for k in range(n):
        u = k / (n - 1)
        cc = interpolate_color(c0, c1, u / 0.5) if u < 0.5 else interpolate_color(c1, c2, (u - 0.5) / 0.5)
        g.add(Circle(radius=r * (1 - 0.8 * u)).set_stroke(width=0).set_fill(cc, 1).move_to(P3(-0.3 * r * u, 0.32 * r * u)))
    wr = max(2.0, 13 * r)
    g.add(Arc(radius=r * (1 - 0.006 * wr), start_angle=1.05 * PI, angle=0.62 * PI).set_stroke("#7FB2FF", wr, opacity=0.35))   # recorte
    g.add(Arc(radius=r * (1 - 0.005 * wr), start_angle=0.08 * PI, angle=0.36 * PI).set_stroke(MAG, wr * 0.8, opacity=0.12))   # toque
    g.add(Ellipse(width=0.46 * r, height=0.3 * r).set_stroke(width=0).set_fill(WHITE_, 0.7).rotate(0.6).move_to(P3(-0.4 * r, 0.44 * r)))
    g.add(Circle(radius=r).set_stroke("#5A6476", 1.4, opacity=0.9))
    for m in g:
        m._degrade = "aco"
    return g.set_z_index(z)


def bloco_aco(w, h, z=5):
    """Bloco 2D de aço com a luz B (mesma lógica da esfera_aco): gradiente vertical claro em cima → escuro embaixo, recorte #7FB2FF na
    borda de baixo à esquerda, toque #EA63FF na de cima à direita, filete interno."""
    f = RoundedRectangle(corner_radius=0.05, width=w, height=h).set_fill(["#9AA6B8", "#7A8696", "#3A4252"], 1).set_sheen_direction(UP) \
        .set_stroke("#5A6476", 1.4)
    f._degrade = "aco"
    rec = VMobject().set_points_as_corners([P3(-w / 2 + 0.04, h / 2 - 0.1), P3(-w / 2 + 0.04, -h / 2 + 0.04), P3(w / 2 - 0.12, -h / 2 + 0.04)]) \
        .set_stroke("#7FB2FF", 3.2, opacity=0.5)
    toq = VMobject().set_points_as_corners([P3(-w / 2 + 0.12, h / 2 - 0.04), P3(w / 2 - 0.04, h / 2 - 0.04), P3(w / 2 - 0.04, -h / 2 + 0.12)]) \
        .set_stroke(MAG, 2.6, opacity=0.18)
    fil = RoundedRectangle(corner_radius=0.04, width=max(w - 0.14, 0.05), height=max(h - 0.14, 0.05)).set_stroke(WHITE_, 1, opacity=0.25)
    g = VGroup(f, rec, toq, fil).set_z_index(z)
    g.front = f
    return g


def cadeado(aberto=False, s=1.0, cor=STEEL):
    """Cadeado de aço (corpo + alça); aberto: a alça sobe e gira."""
    corpo = bloco_aco(0.5 * s, 0.42 * s)
    alca = Arc(radius=0.16 * s, start_angle=0, angle=PI).set_stroke("#9AA6B8", 5 * s).move_to(corpo.get_top() + 0.14 * s * UP)
    if aberto:
        alca.rotate(0.6, about_point=alca.get_left() + 0.0 * UP).shift(0.12 * s * UP)
    furo = Dot(corpo.get_center() + 0.02 * s * UP, radius=0.045 * s, color="#2A303A")
    return VGroup(alca, corpo, furo).set_z_index(9)


def esfera2d(r=0.3, cor=STEEL, z=5):
    """Compatibilidade: toda bola 2D é a esfera de aço com a luz B."""
    return esfera_aco(r, z)


def da_borda(c, d, r):
    """Ponto na borda de um círculo de centro c e raio r (Manim) na direção d: as setas saem da borda, nunca do centro."""
    c, d = np.asarray(c, float), np.asarray(d, float)
    n = np.linalg.norm(d)
    return c if n < 1e-9 else c + d / n * r


def lugar_livre(mob, cands, circ=(), pts=(), mem=None, chave=None, folga=0.3):
    """Centro, entre os candidatos (em ordem de preferência), em que a caixa de mob fica a pelo menos `folga` dos círculos (centro, raio),
    dos pontos e da margem; com `mem`, mantém o candidato anterior enquanto ele seguir livre (o rótulo não pula de quadro em quadro)."""
    w, h = mob.width / 2, mob.height / 2
    P_ = np.asarray(pts, float).reshape(-1, 3)

    def livre(c):
        f = min(7.55 - abs(c[0]) - w, 4.05 + c[1] - h, 3.3 - c[1] - h)                 # em cima, abaixo do título do canto
        for o, r in circ:
            f = min(f, np.hypot(max(abs(o[0] - c[0]) - w, 0), max(abs(o[1] - c[1]) - h, 0)) - r)
        if len(P_):
            f = min(f, np.hypot(np.maximum(np.abs(P_[:, 0] - c[0]) - w, 0), np.maximum(np.abs(P_[:, 1] - c[1]) - h, 0)).min())
        return f
    fs = [livre(c) for c in cands]
    i = mem.get(chave) if mem is not None else None
    if i is not None and fs[i] >= folga:
        melhor = [k for k in range(i) if fs[k] >= folga + 0.25]           # volta a um lugar preferido quando ele fica bem livre
        i = melhor[0] if melhor else i
    else:
        ok = [k for k, f in enumerate(fs) if f >= folga]
        i = ok[0] if ok else int(np.argmax(fs))
    if mem is not None:
        mem[chave] = i
    return cands[i]


def onda(c, r=0.24):
    """Pulso em anel saindo de um ponto (o ⊕): mostra o lugar sem mexer na física."""
    return FadeOut(Circle(radius=r).move_to(c).set_stroke(WHITE_, 3), scale=2.4)


def amostra(a, b, n=12):
    return [a + (b - a) * u for u in np.linspace(0, 1, n)]


def suave(u):
    u = min(1.0, max(0.0, u))
    return u * u * (3 - 2 * u)


# ── gráficos ─────────────────────────────────────────────────────────────────────────────────────────────
class Graf:
    """Eixos com mapeamento (t, y) → tela; o eixo t passa por y = 0, que fica em `y0`. ymin < 0 permitido."""

    def __init__(self, x0, y0, w, tmax, ymin, ymax, hpu, rot_y=None, rot_x=r"t", z=2, cor=DIM):
        self.x0, self.y0, self.w, self.tmax, self.hpu = x0, y0, w, tmax, hpu
        eixo_x = Arrow(P3(x0 - 0.1, y0), P3(x0 + w + 0.25, y0), buff=0, color=cor, stroke_width=3, tip_length=0.15)
        eixo_y = Line(P3(x0, y0 + ymin * hpu - 0.1), P3(x0, y0 + ymax * hpu + 0.12)).set_stroke(cor, 3)
        self.ey = rot_y.next_to(P3(x0, y0 + ymax * hpu + 0.12), UP, buff=0.06) if rot_y is not None else VGroup()
        self.ex = MathTex(rot_x, font_size=36, color=cor).next_to(P3(x0 + w + 0.28, y0), RIGHT, buff=0.06)
        self.eixos = VGroup(eixo_x, eixo_y, self.ex, self.ey).set_z_index(z)

    def pt(self, t, y):
        return P3(self.x0 + self.w * t / self.tmax, self.y0 + self.hpu * y)

    def curva(self, fun, t0=0.0, t1=None, n=200, cor=MAG, w=5):
        t1 = self.tmax if t1 is None else t1
        if t1 - t0 < 1e-4:
            return VMobject()
        ts = np.linspace(t0, t1, n)
        return VMobject().set_points_as_corners([self.pt(t, fun(t)) for t in ts]).set_stroke(cor, w).set_z_index(6)


# ── grade de layout (handoff v2 §2, em unidades do quadro 16 × 9) ─────────────────────────────────────────
PALCO_X, PALCO_Y = (-7.4, 0.7), (-3.4, 2.8)
CONTA_X, CONTA_Y = (1.1, 7.4), (-3.4, 2.8)
PALCO_C = P3(-3.35, -0.3)
CONTA_C = P3(4.25, -0.3)
XC0 = 1.35                    # borda esquerda da CONTA (alinhamento à esquerda)
Y_LEG = -3.82                 # LEGENDA


def na_conta(m, y, x0=XC0):
    """Alinha à esquerda na CONTA, na altura y."""
    return m.move_to(P3(x0 + m.width / 2, y))


# ── 3D por estado (Three.js): a passagem seca grava pedidos, o r3d.js renderiza, a passagem final cola o PNG ───────
PEDIDOS3D = os.environ.get("PEDIDOS3D") == "1"
DIR3D = AQUI / "threejs"


def manim_de_px(px, py, w, h):
    return P3(px / w * 16 - 8, 4.5 - py / h * 9)


class Fundo3D(Group):
    """Fundo 3D do quadro inteiro. `estado(t)` devolve o dict de estado da cena 3D no tempo t da cena Manim.
    `self.op` (ValueTracker) é a opacidade (recuo do PALCO). `self.e` guarda o estado do quadro corrente."""

    def __init__(self, cena_m, cena3d, estado, op=1.0):
        super().__init__()
        self.cm, self.cena, self.fn = cena_m, cena3d, estado
        self.op = ValueTracker(op)
        self.w, self.h = config.pixel_width, config.pixel_height
        self.dir = DIR3D / "q3d" / f"{cena_m.lote}_{self.w}x{self.h}" / cena3d
        vazio = np.zeros((self.h, self.w, 4), dtype=np.uint8)
        self.alfa = vazio[..., 3].copy()
        self.img = ImageMobject(vazio).set_resampling_algorithm(RESAMPLING_ALGORITHMS["linear"])
        self.img.set_width(16).move_to(ORIGIN)
        self.add(self.img)
        self.set_z_index(-20)
        self.f = -1
        self.mult = None             # multiplicador de opacidade em função do tempo (ex.: troca de tomada)
        self.e = estado(0.0)
        cena_m._ped.setdefault(cena3d, {})
        self.add_updater(lambda m: m._quadro())
        self._quadro()

    def __deepcopy__(self, memo):
        """Cópia estática (o fundo guarda a cena; Transform/FadeOut precisam copiar)."""
        g = Group(ImageMobject(self.img.pixel_array.copy()).set_width(16).move_to(ORIGIN))
        for m in self.submobjects[1:]:
            g.add(m.copy())
        return g.set_z_index(-20)

    def _quadro(self):
        f = int(round(self.cm.clk.get_value() * FPS))
        e = self.fn(f / FPS)
        self.e = e
        if PEDIDOS3D:
            self.cm._ped[self.cena][f] = e
        elif f != self.f:
            arq = self.dir / f"f{f:05d}.png"
            if arq.exists():
                from PIL import Image
                a = np.array(Image.open(arq).convert("RGBA"))
                if a.shape[0] != self.h:
                    a = np.array(Image.open(arq).convert("RGBA").resize((self.w, self.h)))
                self.img.pixel_array = a
                self.alfa = a[..., 3].copy()
        self.f = f
        o = self.op.get_value() * (self.mult(f / FPS) if self.mult else 1.0)
        self.img.pixel_array[..., 3] = (self.alfa * max(0.0, min(1.0, o)) + 0.5).astype(np.uint8)
        return self


class _Poli:
    """Polígono 2D (ponto dentro por paridade de cruzamentos, vetorizado): o mesmo papel do matplotlib.path, sem a dependência."""

    def __init__(self, v):
        self.v = np.asarray(v, float)[:, :2]

    def contains_points(self, q):
        q = np.asarray(q, float).reshape(-1, 2)
        x, y = q[:, 0][:, None], q[:, 1][:, None]
        a, b = self.v, np.roll(self.v, -1, axis=0)
        c = ((a[:, 1] > y) != (b[:, 1] > y)) & (x < (b[:, 0] - a[:, 0]) * (y - a[:, 1]) / (b[:, 1] - a[:, 1] + 1e-12) + a[:, 0])
        return c.sum(axis=1) % 2 == 1


def r4(d):
    """Arredonda floats de um estado (dedupe de quadros iguais no r3d.js)."""
    if isinstance(d, dict):
        return {k: r4(v) for k, v in d.items()}
    if isinstance(d, (list, tuple)):
        return [r4(v) for v in d]
    if isinstance(d, float):
        return round(d, 4)
    return d


def cam_frente(K=1.0, xc=0.0, yc=-2.0, camx=0.0, fov=16, el=3):
    return {"modo": "frente", "K": K, "xc": xc, "yc": yc, "camx": camx, "fov": fov, "el": el}


def mapa_frente(cam, x, z, y=0.0):
    """Ponto 3D (x, y, z) → Manim na vista 'frente' (perspectiva aproximada pela profundidade y)."""
    K = cam["K"]
    D = (9 / K / 2) / math.tan(math.radians(cam["fov"]) / 2)
    s = D / (D + y)
    return P3(cam["xc"] + K * s * (x - cam["camx"]), cam["yc"] + K * s * z)


def cam_topo(K=1.0, xc=0.0, yc=0.0, camx=0.0, camy=0.0, fov=16):
    return {"modo": "topo", "K": K, "xc": xc, "yc": yc, "camx": camx, "camy": camy, "fov": fov}


def cam_obl(az, el, alvo, K=1.0, xc=0.0, yc=0.0, fov=16):
    return {"modo": "obl", "az": az, "el": el, "alvo": list(alvo), "K": K, "xc": xc, "yc": yc, "fov": fov}


_BASES = {}


def _base_cam(cam):
    """Base da câmera (posição, eixos, escalas) do b3d.js, em cache por câmera: a projeção vira só produtos escalares."""
    k = tuple((a, tuple(b) if isinstance(b, list) else b) for a, b in sorted(cam.items()))
    if k in _BASES:
        return _BASES[k]
    K, fov = cam.get("K", 1.0), cam.get("fov", 14)
    if cam.get("modo") == "topo":
        az, el, alvo = -90.0, 89.999, (cam.get("camx", 0.0), cam.get("camy", 0.0), 0.0)
    elif cam.get("modo") == "obl":
        az, el, alvo = cam["az"], cam["el"], cam["alvo"]
    else:
        az, el, alvo = -90.0, cam.get("el", 0.0), (cam.get("camx", 0.0), 0.0, cam.get("camz", 0.0))
    a, e, th = math.radians(az), math.radians(el), math.tan(math.radians(fov) / 2)
    D = (9 / K / 2) / th
    alvo = np.array(alvo, dtype=float)
    pos = alvo + D * np.array([math.cos(e) * math.cos(a), math.cos(e) * math.sin(a), math.sin(e)])
    up = np.array([-math.sin(e) * math.cos(a), -math.sin(e) * math.sin(a), math.cos(e)])
    f = (alvo - pos) / np.linalg.norm(alvo - pos)
    r = np.cross(f, up)
    r /= np.linalg.norm(r)
    u = np.cross(r, f)
    if len(_BASES) > 4000:
        _BASES.clear()
    _BASES[k] = b = (pos, np.stack([r, u, f]), 8 / (th * 16 / 9), 4.5 / th, cam.get("xc", 0.0), cam.get("yc", 0.0))
    return b


def projeta3d(cam, p):
    """Ponto 3D → Manim pela mesma câmera do b3d.js (posicionaCamera + setViewOffset), em qualquer modo. Perspectiva exata."""
    pos, B, sx, sy, xc, yc = _base_cam(cam)
    x, y, z = B @ (np.asarray(p, dtype=float) - pos)
    return np.array([xc + sx * x / z, yc + sy * y / z, 0.0])


def projeta3d_n(cam, pts):
    """Vários pontos 3D (N×3) → Manim (N×3) de uma vez."""
    pos, B, sx, sy, xc, yc = _base_cam(cam)
    q = (np.asarray(pts, dtype=float) - pos) @ B.T
    out = np.zeros((len(q), 3))
    out[:, 0] = xc + sx * q[:, 0] / q[:, 2]
    out[:, 1] = yc + sy * q[:, 1] / q[:, 2]
    return out


def escala_op(m, o):
    """Multiplica as opacidades de fill e stroke de toda a família (preserva traços sem preenchimento)."""
    for x in m.family_members_with_points():
        if isinstance(x, VMobject):
            x.set_fill(opacity=x.get_fill_opacity() * o, family=False)
            x.set_stroke(opacity=x.get_stroke_opacity() * o, family=False)
    return m


class OpVivo(Animation):
    """Fade de um mobject vivo (always_redraw): ele continua se redesenhando e só a opacidade anima."""

    def __init__(self, m, entra=True, **kw):
        super().__init__(m, suspend_mobject_updating=False, remover=not entra, introducer=entra, **kw)
        self.entra = entra

    def interpolate_mobject(self, alpha):
        a = self.rate_func(alpha)
        self.mobject.update(0)
        o = a if self.entra else 1 - a
        if o < 0.999:
            escala_op(self.mobject, o)


def _vivo(a):
    if isinstance(a, (FadeIn, FadeOut)) and isinstance(a.mobject, Fundo3D):
        return a.mobject.op.animate(run_time=a.run_time).set_value(1.0 if isinstance(a, FadeIn) else 0.0).build()             if hasattr(a.mobject.op.animate, "build") else a
    if isinstance(a, (FadeIn, FadeOut)) and a.mobject.get_updaters() and getattr(a.mobject, "_vivo_", False):   # yt_0019: só camadas vivo()
        return OpVivo(a.mobject, entra=isinstance(a, FadeIn), run_time=a.run_time)
    return a


# ── cena-base: relógio por quadro, âncoras, cabeçalho ──────────────────────────────────────────────────────
class Base(Scene):
    """Todo `play` é quantizado em quadros inteiros e arrasta o relógio `self.clk` (segundos da cena), de modo que
    updaters baseados em `self.clk` ficam exatos quadro a quadro e o número de quadros é determinístico."""
    TITULO = "MECÂNICA · TORQUE"
    FUNDO = "fundo_lab.png"           # v4 §2: o céu do laboratório em toda cena (fundo.py); exercícios: fundo_lab_ex.png

    def setup_base(self, cap=None, selo=None):
        self.camera.background_color = "#08122B"
        if os.environ.get("SO_AUDITORIA") == "1":            # v3: passada só de auditoria (com --dry_run): não desenha os quadros
            self.renderer.render = lambda *a, **k: None
        self.fundo = ImageMobject(str(AQUI / self.FUNDO)).set_width(16).move_to(ORIGIN).set_z_index(-100)
        self.add(self.fundo)
        self.clk = ValueTracker(0.0)
        self.poeira = poeira_estelar(self.clk)                # v10 R-M: poeira de estrelas à deriva (parallax), atrás de tudo: a tela nunca fica estática
        self.add(self.poeira)
        self.nq = 0
        self.lote = type(self).__name__
        self._ped = {}
        self.wm = ImageMobject(str(WATERMARK_PATH)).set_width(1.92).set_opacity(0.45).to_corner(UR, buff=0.3).set_z_index(40)
        self.h1 = txt(self.TITULO, 17, color=DIM).to_corner(UL, buff=0.32).set_z_index(40)
        self.h2 = self._sl = None
        self._pend = []
        self.add(self.wm, self.h1)
        self.alvo = 0.0
        self.ritmo = 1.0                                    # v9: fator dos plays do trecho corrente (plano())
        self.ritmo_w = 1.0                                  # v9: fator das esperas explícitas do trecho corrente (plano())
        self._off = None                                    # v9: quadro absoluto (da voz) do quadro 0 deste lote
        self._segs, self._cur = [], {"id": "-", "A": 0.0, "W": 0.0}
        self._med, self._mi, self.faltou, self.abertas = None, 0, [], []
        if SYNC == "final" and (AQUI / f"medicao_{self.lote}.json").exists():
            self._med = json.loads((AQUI / f"medicao_{self.lote}.json").read_text(encoding="utf-8"))["marcas"]
        self.log = []
        self.dica_atual = None
        self._aid, self._q0 = None, 0
        if cap:
            self.h2 = txt(cap, 30, op=0.95).next_to(self.h1, DOWN, buff=0.14, aligned_edge=LEFT).set_z_index(40)
            self.add(self.h2)
            if selo:   # selo de ligação com a teoria (v2: sem referência de livro na tela)
                self._sl = txt(selo, 20, color=DIM).next_to(self.h2, DOWN, buff=0.12, aligned_edge=LEFT).set_z_index(40)
                self.add(self._sl)

    # tempo ---------------------------------------------------------------------------------------------------
    @property
    def t(self):
        return self.nq / FPS

    def play(self, *anims, run_time=None, fixo=False, **kw):
        if self._pend:
            anims, self._pend = (*anims, *self._pend), []
        anims = tuple(_vivo(a) for a in anims)
        self._still()
        rt = run_time
        if rt is None:
            rt = max([getattr(a, "run_time", 1.0) for a in anims] or [1.0])
        if not fixo:
            if SYNC == "medir":
                self._cur["A"] += rt                         # v9: tempo nominal de animação do trecho (medição)
            rt = rt * self.ritmo                             # v9: espera que anima (fixo=True) não escala; o resto acompanha o plano() do trecho
        for a_ in anims:                                     # v5 G40: todo FadeIn/FadeOut de objeto (texto, linha, selo, caixa) chega a 100% / sai em ≤ 0,35 s
            if isinstance(a_, (FadeIn, FadeOut)) and rt > 0.36 and not isinstance(a_.mobject, (ImageMobject, Fundo3D)) and not getattr(a_.mobject, "_fundo3d", False):
                a_.rate_func = (lambda t, r_=rt: smooth(min(1.0, t * r_ / 0.35)))
        n = max(1, round(rt * FPS))
        rtq = n / FPS - FRAC
        t0 = self.nq / FPS
        clk = UpdateFromAlphaFunc(self.clk, lambda m, a: m.set_value(t0 + a * n / FPS), rate_func=linear, run_time=rtq)
        self._em_play, self._kq = True, 0
        self._npl = getattr(self, "_npl", 0) + 1                # v4: id do play (TRÂNSITO compara passadas do mesmo play)

        def fontes(a):                                       # v4: a origem de cada cópia (TransformFromCopy anima o destino a partir dela)
            if isinstance(a, TransformFromCopy):
                yield a.target_mobject
            for b in getattr(a, "animations", []) or []:
                yield from fontes(b)
        self._fontes = [f for a in anims for f in fontes(a)] + list(getattr(self, "_fontes_extra", []))
        super().play(*anims, clk, run_time=rtq, **kw)
        self._fontes = []
        self._em_play = False
        self.nq += n
        if AUDITORIA:
            self._auditar()                                  # v3 §3: e o estado final de cada play (depois dos removers)

    def update_to_time(self, t):
        """v3 §3: a auditoria roda a cada 3 quadros DENTRO do play (crossfade de selos, Pilha rolando, rótulos que seguem corpos, ápice)."""
        super().update_to_time(t)
        if AUDITORIA and getattr(self, "_em_play", False):
            if self._kq % 3 == 0:
                self._auditar(dentro=True)
            self._kq += 1

    def _still(self):
        if STILL is not None and self.nq / FPS >= STILL:
            from manim.utils.exceptions import EndSceneEarlyException
            raise EndSceneEarlyException()

    def wait(self, duration=1.0, *a, interno=False, **kw):
        """Espera explícita da cena (v9: entra na medição e é esticada pelo plano do trecho); `interno=True` é a espera até um gatilho/fim de âncora."""
        if not interno:
            if SYNC == "medir":
                self._cur["W"] += duration
            else:
                duration = duration * self.ritmo_w
        self._wait_q(duration)

    def _wait_q(self, duration):
        self._still()
        n = max(1, round(duration * FPS))
        rtq = n / FPS - FRAC
        t0 = self.nq / FPS
        self._em_play, self._kq = True, 0
        self._npl = getattr(self, "_npl", 0) + 1
        super().play(UpdateFromAlphaFunc(self.clk, lambda m, a_: m.set_value(t0 + a_ * n / FPS), rate_func=linear, run_time=rtq), run_time=rtq)
        self._em_play = False
        self.nq += n

    # v9: marcas de sincronia (início de âncora, gatilho, fração) e plano de cada trecho entre marcas ---------------------
    def _k_frase(self, aid, frase):
        import re as _r
        fala = ANC.get(aid, {}).get("fala", "").split()
        alvo = _r.findall(r"\w+", frase.lower())
        return next((i for i in range(len(fala)) if fala[i:i + len(alvo)] == alvo), None)

    def _tgt(self, kid):
        """Quadro (local do lote) em que a marca `kid` deve acontecer; None se não houver alvo."""
        kind, aid, arg = kid.split(":", 2)
        a = ANC.get(aid)
        if a is None:
            return None
        if kind == "gat":
            k = self._k_frase(aid, arg)
            if k is None:
                return None
            rel = max(0.0, a["t"][k] - LEAD)
        else:
            rel = max(0.0, self.t_ate_aid(aid, float(arg)) - LEAD)
        return round(a["ini"] * FPS) - self._off + rel * FPS

    def _marca(self, kid):
        if SYNC == "medir":
            self._cur = {"id": kid, "A": 0.0, "W": 0.0}
            self._segs.append(self._cur)
        elif self._med is not None and kid != "fim":
            self._plano_para(kid)

    def _plano_para(self, kid):
        """Acha a marca na medição e fixa ritmo/ritmo_w do trecho que começa agora (plano() do yt_0010, por trecho entre marcas)."""
        marcas = self._med
        i = next((j for j in range(self._mi, min(len(marcas), self._mi + 8)) if marcas[j]["id"] == kid), None)
        if i is None:
            self.faltou.append(kid)
            self.ritmo = self.ritmo_w = 1.0
            return
        self._mi = i + 1
        agora = self.nq
        A = W = 0.0
        j, tgt = i, self.alvo
        primeiro = True
        while j < len(marcas):
            A += marcas[j]["A"]
            W += marcas[j]["W"]
            j += 1
            if j >= len(marcas):
                break
            nid = marcas[j]["id"]
            if nid.startswith("an:") or nid == "fim":
                break
            t_ = self._tgt(nid)
            if primeiro and kid.startswith("an:") and t_ is not None and t_ - agora < 0.25 * FPS and A > 0.2:
                # v9: o 1º gatilho cai nas primeiras palavras: a preparação da cena (limpa, entradas) encolhe até ≥ 0,25× para chegar nele
                D0 = max(0.1, (t_ - agora) / FPS)
                self.ritmo, self.ritmo_w = max(0.15, min(1.0, D0 / A)), 1.0
                print(f"[plano] {kid[:50]} A={A:.2f} W={W:.2f} D={D0:.2f} ritmo={self.ritmo:.2f} (1º gatilho nas primeiras palavras)")
                return
            primeiro = False
            if t_ is not None and t_ - agora >= 0.25 * FPS:
                tgt = t_
                break
        D = max(0.3, (tgt - agora) / FPS)
        self.ritmo, self.ritmo_w = plano(A, W, D)
        print(f"[plano] {kid[:50]} A={A:.2f} W={W:.2f} D={D:.2f} ritmo={self.ritmo:.2f} ritmo_w={self.ritmo_w:.2f}")

    def gat(self, frase):
        """Gatilho de fala (v9): espera até LEAD s antes da palavra (alinhamento da voz contínua) e só então começa o evento seguinte; o plano() do trecho
        anterior já esticou as animações para chegar aqui sem sobra. Registra o instante (relativo ao início da âncora) para o QA."""
        k = self._k_frase(self._aid, frase)
        if k is not None:
            tw = ANC.get(self._aid, {}).get("t")
            prev = max(0.0, (tw[k] if tw else 0.15 + k / 2.7) - LEAD)
            agora = (self.nq - self._q0) / FPS
            if prev - agora >= 1 / FPS:
                self.wait(prev - agora, interno=True)
        else:
            print(f"[gatilho-sem-frase] {self._aid}: {frase!r}")
        print(f"[gatilho] {self._aid} {(self.nq - self._q0) / FPS:.2f} {frase}")
        self._marca(f"gat:{self._aid}:{frase}")

    def t_ate_aid(self, aid, frac):
        a = ANC.get(aid, {})
        tw, nom = a.get("t"), a.get("nominal")
        if not tw or not nom:
            return frac * a.get("dur", 0.0)
        xs = [0.0] + [0.15 + k / 2.7 for k in range(len(tw))] + [max(nom, 0.15 + len(tw) / 2.7)]
        ys = [0.0] + list(tw) + [a["dur"]]
        return float(np.interp(frac * nom, xs, ys))

    def t_ate(self, frac):
        """A fração `frac` (0–1) foi escrita para a janela NOMINAL (2,7 palavras/s). Devolve o instante equivalente na voz real (mesmo ponto do texto)
        menos o LEAD, em segundos desde o início da âncora."""
        return max(0.0, self.t_ate_aid(self._aid, frac) - LEAD)

    def ate(self, frac):
        """Espera até a fração `frac` (0–1) da âncora corrente (mapeada para a voz real pelo texto)."""
        alvo = self._q0 + self.t_ate(frac) * FPS
        if alvo - self.nq >= 1:
            self.wait((alvo - self.nq) / FPS, interno=True)
        self._marca(f"ate:{self._aid}:{frac}")

    def resta(self):
        """Segundos que faltam para o fim da âncora corrente."""
        return max(0.0, (self.alvo - self.nq) / FPS)

    def an(self, aid):
        """Fecha a âncora anterior (espera o resto da fala) e abre `aid`, na hora absoluta da voz (v9: a voz contínua é a régua)."""
        self._fecha()
        a = ANC[aid]
        ini_q = round(a["ini"] * FPS)
        if self._off is None:
            self._off = ini_q - self.nq
        self._aid = aid
        self._q0 = ini_q - self._off
        self.alvo = round(a["fim"] * FPS) - self._off
        self.ritmo = self.ritmo_w = 1.0
        self.abertas.append((aid, (self.nq - self._q0) / FPS))
        self._marca(f"an:{aid}")

    def _fecha(self):
        if hasattr(self, "_cx_flush"):
            self._cx_flush()
        if self._aid is not None:
            if self.alvo - self.nq >= 1:
                self.wait((self.alvo - self.nq) / FPS, interno=True)
            self.log.append((self._aid, self._q0 / FPS, dur(self._aid), (self.nq - self._q0) / FPS))
            self._aid = None

    def fim(self):
        self._fecha()
        self.log.append(("FIM", self.nq / FPS, 0, 0))
        self._marca("fim")
        if SYNC == "medir":
            (AQUI / f"medicao_{self.lote}.json").write_text(json.dumps({"lote": self.lote, "marcas": self._segs}, indent=0), encoding="utf-8")

    # cabeçalho -------------------------------------------------------------------------------------------------
    def fixos(self):
        return {self.fundo, self.poeira, self.wm, self.h1, *([self.h2] if self.h2 else []), *([self._sl] if getattr(self, '_sl', None) else [])}

    def secao(self, s, selo=None):
        """Linha 2 do header (e selo da fonte, linha 3): o antigo sai (0,25 s) antes de o novo entrar."""
        velhos = [m for m in (self.h2, getattr(self, "_sl", None)) if m is not None]
        if velhos:
            self.play(*[FadeOut(m) for m in velhos], run_time=0.25)
        self.h2 = self._sl = None
        if not s:
            return
        novo = txt(s, 30).next_to(self.h1, DOWN, buff=0.14, aligned_edge=LEFT).set_z_index(40)
        self.h2 = novo
        self._pend.append(FadeIn(novo))
        if selo:
            self._sl = txt(selo, 20, color=DIM, op=0.85).next_to(novo, DOWN, buff=0.12, aligned_edge=LEFT).set_z_index(40)
            self._pend.append(FadeIn(self._sl))

    def clear(self, *keep, rt=0.6):
        keep = self.fixos() | set(keep)
        mobs = [m for m in self.mobjects if m not in keep and m is not self.clk]
        vis = [m for m in mobs if not isinstance(m, ValueTracker)]          # trackers (estado 3D) só saem, sem animar
        if vis:
            self.play(*[m.op.animate.set_value(0.0) if isinstance(m, Fundo3D) else FadeOut(m) for m in vis], run_time=rt)
        for m in mobs:
            m.clear_updaters()
        self.remove(*mobs)
        self.dica_atual = None

    def snap(self):
        """O que está em cena agora (fora o cabeçalho): use antes de montar a cena nova, e passe para troca()."""
        keep = self.fixos()
        return [m for m in self.mobjects if m not in keep and m is not self.clk]

    def troca(self, velhos, *entram, rt=0.5, seq=False):
        """Troca de cena. Crossfade (G5) entre cenas leves; com `seq` (G13, entre duas cenas cheias) a velha sai em 0,35 s e só então a
        nova entra em 0,35 s, sem as duas a meia opacidade uma sobre a outra."""
        vis = [m for m in velhos if not isinstance(m, ValueTracker)]
        sai = [m.op.animate.set_value(0.0) if isinstance(m, Fundo3D) else FadeOut(m) for m in vis]
        if seq:                                              # v4 G39: a cena velha sai inteira (0,4 s) e só então a nova entra (0,4 s); nunca as duas cruzadas
            self._em_troca = True
            self.play(*sai, run_time=0.4)
            for m in velhos:
                m.clear_updaters()
            self.remove(*velhos)
            if entram:                                       # v6: sem entrantes não há meio segundo de tela vazia
                self.play(*entram, run_time=0.4)
            self._em_troca = False
            return
        self.play(*sai, *entram, run_time=rt)
        for m in velhos:
            m.clear_updaters()
        self.remove(*velhos)
        if self.dica_atual in velhos:
            self.dica_atual = None

    def logo(self, largura):
        img = ImageMobject(str(ROOT / "assets" / "branding" / "overlays" / "parallax_lab_logo_horizontal.png"))
        arr = img.get_pixel_array()
        ys, xs = np.nonzero(arr[:, :, 3] > 8)
        return ImageMobject(arr[ys.min():ys.max() + 1, xs.min():xs.max() + 1]).set_width(largura)

    def hl(self, s, y=3.0, size=T_HL, color=WHITE_, x=0.0, bold=True):
        return txt(s, size, color=color, bold=bold).move_to(P3(x, y))

    def dica_entra(self, d, apagar=True):
        """DICA entra; as equações soltas em cena vão a 40% (G7: uma frase na tela por vez)."""
        self.dica_atual = d
        (a0, b0), (a1, b1) = d.get_corner(DL)[:2] - 0.1, d.get_corner(UR)[:2] + 0.1
        cobre = lambda m: m.get_left()[0] < a1 and m.get_right()[0] > a0 and m.get_bottom()[1] < b1 and m.get_top()[1] > b0
        self._cobertos = [m for m in self.mobjects if m not in self.fixos() and (hasattr(m, "_tam") or isinstance(m, MathTex)) and cobre(m)]   # a DICA nunca cobre texto
        self._apagadas = [m for m in self.mobjects if isinstance(m, MathTex) and m not in self.fixos() and m not in self._cobertos] if apagar else []
        self.play(FadeIn(d, shift=0.15 * UP), *[m.animate.set_opacity(0.4) for m in self._apagadas], *[FadeOut(m) for m in self._cobertos], run_time=0.6)

    def dica_sai(self):
        if self.dica_atual is not None:
            self.play(FadeOut(self.dica_atual), *[m.animate.set_opacity(1.0) for m in getattr(self, "_apagadas", []) if m in self.mobjects],
                      *[FadeIn(m) for m in getattr(self, "_cobertos", [])], run_time=0.4)
            self.remove(self.dica_atual)
            self.dica_atual = None
            self._apagadas = []

    # auditoria de sobreposições (AUDITORIA=1) ---------------------------------------------------------------
    def _auditar(self, dentro=False):
        _final = not dentro
        if not dentro:
            self.update_mobjects(0)
        itens = []

        def op(m):
            vals = []
            for x in m.family_members_with_points():
                try:
                    vals.append(max(x.get_fill_opacity(), x.get_stroke_opacity()))
                except Exception:
                    vals.append(1.0)
            return max(vals) if vals else 0.0

        tams = {}

        def walk(m, tam=None, fixo=False):
            if isinstance(m, ImageMobject):
                return
            tam = getattr(m, "_tam", tam)
            if isinstance(m, (Text, SingleStringMathTex)):
                if op(m) > 0.08 and m.width > 0.01:
                    itens.append(m)
                    tams[id(m)] = (tam, fixo)
                return
            for s in m.submobjects:
                walk(s, tam, fixo)

        fx = self.fixos()
        for top in self.mobjects:
            walk(top, fixo=top in fx)

        bbc = {}

        def bb(m):                                           # caixa (encolhida 0,03) guardada nesta passada: a auditoria roda a cada 3 quadros
            if id(m) not in bbc:
                pts_ = m.get_all_points()
                if len(pts_):
                    x0, y0 = pts_[:, 0].min(), pts_[:, 1].min()
                    x1, y1 = pts_[:, 0].max(), pts_[:, 1].max()
                else:
                    (x0, y0, _), (x1, y1, _) = m.get_critical_point(DL), m.get_critical_point(UR)
                bbc[id(m)] = (x0 + 0.03, y0 + 0.03, x1 - 0.03, y1 - 0.03)
            return bbc[id(m)]

        def nome(m):
            return f"'{m.text[:30]}'" if isinstance(m, Text) else f"'{m.get_tex_string()[:30]}'"

        t = self.clk.get_value()
        # PALCO: algum desenho (não texto) visível fora do cabeçalho/DICA, ou um fundo 3D com opacidade
        fixos = self.fixos() | ({self.dica_atual} if self.dica_atual is not None else set())
        graf = [0]

        def tem_desenho(m):
            if isinstance(m, Fundo3D):
                if m.op.get_value() > 0.15:
                    graf[0] += 1
                return
            if isinstance(m, (Text, SingleStringMathTex, MathTex)) or isinstance(m, ImageMobject):
                return
            if (m.points.size or isinstance(m, DashedVMobject)) and op(m) > 0.15 and m.width + m.height > 0.4:   # tracejado conta inteiro
                graf[0] += 1
                return
            for s in m.submobjects:
                tem_desenho(s)

        for top in self.mobjects:
            if top not in fixos and top is not self.clk:
                tem_desenho(top)
        if graf[0] == 0 and not getattr(self, "_em_troca", False):
            print(f"[audit] {t:7.1f}s SEM PALCO")
        # G15: degradê só no ⊕ (e no rastro dele, e no sombreado de aço dos corpos); qualquer outro gradiente é erro
        tags = getattr(self, "_tags_degrade", None)
        if tags is None:
            tags = self._tags_degrade = {}

        def degr(m, tag=None):
            tag = getattr(m, "_degrade", tag)
            if isinstance(m, VMobject) and m.points.size and op(m) > 0.05:
                multi = any(len(np.unique(np.round(c_, 3), axis=0)) > 1 for c_ in (m.get_fill_rgbas(), m.get_stroke_rgbas()))   # cores distintas
                if tag:
                    tags[tag] = tags.get(tag, 0) + 1
                elif multi:
                    print(f"[audit] {t:7.1f}s DEGRADÊ FORA DO ⊕ {type(m).__name__} em ({m.get_x():.1f}; {m.get_y():.1f})")
            if tag and tag != "cm" and tag != "rastro" and tag != "aco":
                print(f"[audit] {t:7.1f}s DEGRADÊ FORA DO ⊕ marcado '{tag}'")
            for s_ in m.submobjects:
                degr(s_, tag)
        for top in self.mobjects:
            if top not in self.fixos() and top is not self.clk and not isinstance(top, Fundo3D):
                degr(top)
        # G12: cor por token, uma vez por MathTex
        vistos = getattr(self, "_cor_vistos", None)
        if vistos is None:
            vistos = self._cor_vistos = {}
            self._cor_n = [0, 0]

        def cores_tex(m):
            if isinstance(m, MathTex) and hasattr(m, "_partes") and id(m) not in vistos and op(m) > 0.3:
                vistos[id(m)] = True
                for tx, c in m._partes:
                    e_ = cor_esperada(tx)
                    if e_ is None:
                        continue
                    self._cor_n[0] += 1
                    aceitas = {ManimColor(x).to_hex().upper() for x in e_}
                    if ManimColor(c).to_hex().upper() not in aceitas:
                        self._cor_n[1] += 1
                        print(f"[audit] {t:7.1f}s COR POR TOKEN '{tx}' em {ManimColor(c).to_hex()} (esperado {sorted(aceitas)})")
            elif isinstance(m, MathTex) and not hasattr(m, "_partes") and id(m) not in vistos and op(m) > 0.3:
                vistos[id(m)] = True
                print(f"[cor] {t:7.1f}s sem partes registradas: '{m.get_tex_string()[:40]}'")
            for s_ in m.submobjects:
                cores_tex(s_)
        for top in self.mobjects:
            if top not in self.fixos():
                cores_tex(top)
        # objetos (setas, bolas, corpos, molas, trajetórias): pontos de cada folha VMobject com desenho, fora do cabeçalho/DICA/caixas
        objs = []

        voando = getattr(self, "_voando", set()) | set(id(x) for r in getattr(self, "_voando_raiz", []) for x in r.get_family())   # glifos em voo (G23)

        def folhas(m):
            if isinstance(m, (Text, SingleStringMathTex, ImageMobject, Fundo3D)) or getattr(m, "_fundo", False) or getattr(m, "_risco", False) \
                    or getattr(m, "_halo", False):
                return
            if id(m) in voando:
                return
            if isinstance(m, VMobject) and m.points.size and not m.submobjects:
                if op(m) > 0.15:
                    objs.append(m)
                return
            for s_ in m.submobjects:
                folhas(s_)
        for top in self.mobjects:
            if top not in fixos and top is not self.clk:
                folhas(top)
        cache_d = {}

        def densos(o):                                       # pontos ao longo da curva de verdade (Bézier cúbica), a cada ~0,08: v3 (a corda cortava os círculos por dentro)
            if id(o) not in cache_d:
                p_ = o.points
                k_ = len(p_) // 4
                if k_:
                    a0, h1, h2, a1 = p_[0:4 * k_:4], p_[1:4 * k_:4], p_[2:4 * k_:4], p_[3:4 * k_:4]
                    L = np.linalg.norm(a1 - a0, axis=1) + np.linalg.norm(h1 - a0, axis=1) + np.linalg.norm(a1 - h2, axis=1)
                    n_ = int(min(40, max(2, np.ceil(L.max() / 0.08))))
                    t = np.linspace(0, 1, n_)[None, :, None]
                    b = ((1 - t) ** 3) * a0[:, None] + 3 * ((1 - t) ** 2) * t * h1[:, None] + 3 * (1 - t) * t * t * h2[:, None] + (t ** 3) * a1[:, None]
                    cache_d[id(o)] = b.reshape(-1, 3)
                else:
                    cache_d[id(o)] = p_
            return cache_d[id(o)]
        pai_de = {}
        for m in self.mobjects:
            for x in m.get_family():
                for c in x.submobjects:
                    pai_de[id(c)] = x

        def grupo_do(a):
            """Família do menor grupo acima do texto que tem outro desenho e até 12 folhas (o rótulo e o desenho dele)."""
            g, ok_ = pai_de.get(id(a)), set()
            for _ in range(3):                                   # o maior grupo (até 3 níveis acima) com até 10 peças de desenho
                if g is None:
                    break
                txt_ = set(id(y) for x in g.get_family() if isinstance(x, (Text, SingleStringMathTex)) for y in x.get_family())
                pecas = set()                                    # o ⊕ (degradê em dezenas de arcos) e um tracejado contam como uma peça só
                for x in g.family_members_with_points():
                    if id(x) in txt_:
                        continue
                    y, pc = x, x
                    while y is not None and y is not g:
                        if getattr(y, "_cm", False) or isinstance(y, DashedVMobject):
                            pc = y
                        y = pai_de.get(id(y))
                    pecas.add(id(pc))
                des = list(pecas)
                if len(des) > 16:
                    break
                if des:
                    ok_ = set(id(x) for x in g.get_family())
                g = pai_de.get(id(g))
            return ok_
        cache_b = {}

        def caixa_o(o):
            if id(o) not in cache_b:
                p_ = o.points
                cache_b[id(o)] = (p_[:, 0].min(), p_[:, 1].min(), p_[:, 0].max(), p_[:, 1].max())
            return cache_b[id(o)]
        for o in objs:
            pts = o.points
            if (np.abs(pts[:, 0]) > 7.55).any() or (np.abs(pts[:, 1]) > 4.05).any():
                print(f"[audit] {t:7.1f}s OBJETO FORA DA MARGEM {type(o).__name__} em ({o.get_x():.1f}; {o.get_y():.1f})")
        circ = []
        for fn in getattr(self, "_corpos3d", []):
            try:
                circ += list(fn())
            except Exception:
                pass
        circ = [(q[0], q[1], len(q) > 2 and q[2]) for q in circ]           # (centro, raio, futuro?)
        for c_, r_, fut in circ:
            if not fut and (abs(c_[0]) + r_ > 7.55 or abs(c_[1]) + r_ > 4.05):
                print(f"[audit] {t:7.1f}s OBJETO FORA DA MARGEM corpo 3D em ({c_[0]:.1f}; {c_[1]:.1f})")
        for a in itens:
            tam, fixo = tams.get(id(a), (None, False))
            if fixo or (self.dica_atual is not None and a in self.dica_atual.get_family()):
                continue
            ax0, ay0, ax1, ay1 = bb(a)
            fam = set(id(q) for q in a.get_family())
            if voando and id(a) in voando:                     # texto em voo (voa/passo): transitório da construção da conta
                continue
            proprio = grupo_do(a)
            for o in objs:
                if id(o) in fam:
                    continue
                ox0, oy0, ox1, oy1 = caixa_o(o)
                dentro_c = ox0 <= ax0 and ax1 <= ox1 and oy0 <= ay0 and ay1 <= oy1 and o.get_fill_opacity() > 0.05   # texto escrito dentro de um corpo (vale também enquanto ele esmaece)
                fol = 0.03 if id(o) in proprio else (0.06 if dentro_c else (0.09 if math.hypot(ox1 - ox0, oy1 - oy0) < 0.25 else 0.16))   # v3: encostar também conta
                x0, y0, x1, y1 = ax0 - fol, ay0 - fol, ax1 + fol, ay1 + fol
                if ox1 < x0 or ox0 > x1 or oy1 < y0 or oy0 > y1:          # pré-filtro pela caixa do objeto
                    continue
                pts = densos(o)
                dentro = (pts[:, 0] > x0) & (pts[:, 0] < x1) & (pts[:, 1] > y0) & (pts[:, 1] < y1)
                if dentro.any():
                    dono = next((f"{type(tp).__name__}[{len(tp.submobjects)}]" for tp in self.mobjects if o in tp.get_family()), "?") if type(o).__name__ == "VMobjectFromSVGPath" else ""
                    print(f"[audit] {t:7.1f}s TEXTO SOBRE OBJETO {nome(a)} x {type(o).__name__} em ({o.get_x():.1f}; {o.get_y():.1f}) {dono}")
                    break
            x0, y0, x1, y1 = ax0 - 0.09, ay0 - 0.09, ax1 + 0.09, ay1 + 0.09
            for c_, r_, _ in circ:
                dx = max(x0 - c_[0], 0, c_[0] - x1)
                dy = max(y0 - c_[1], 0, c_[1] - y1)
                if math.hypot(dx, dy) < r_ + 0.03:
                    print(f"[audit] {t:7.1f}s TEXTO SOBRE OBJETO {nome(a)} x corpo 3D em ({c_[0]:.1f}; {c_[1]:.1f})")
                    break
        caixas = [m for top in self.mobjects for m in top.get_family() if getattr(m, "_caixa", False) and op(m) > 0.3]
        for c_ in caixas:                                    # caixa (isenta como fundo) cortando texto que não está dentro dela
            cx0, cy0, cx1, cy1 = bb(c_)
            for a in itens:                                  # glifo a glifo: parte da equação pode estar na caixa, o vizinho não pode encostar
                if voando and id(a) in voando:
                    continue
                for gl in a.family_members_with_points():
                    x0, y0, x1, y1 = bb(gl)
                    cruza = min(x1, cx1) - max(x0, cx0) > 0.02 and min(y1, cy1) - max(y0, cy0) > 0.02
                    dentro = x0 >= cx0 - 0.01 and x1 <= cx1 + 0.01 and y0 >= cy0 - 0.01 and y1 <= cy1 + 0.01
                    if cruza and not dentro:
                        print(f"[audit] {t:7.1f}s TEXTO SOBRE CAIXA {nome(a)}")
                        break
        for i, a in enumerate(itens):
            x0, y0, x1, y1 = bb(a)
            tam, fixo = tams.get(id(a), (None, False))
            if not fixo:
                if x0 < -7.55 or x1 > 7.55 or y0 < -4.05 or y1 > 4.05:
                    print(f"[audit] {t:7.1f}s FORA DA MARGEM {nome(a)}")
                if voando and id(a) in voando:
                    pass
                elif isinstance(a, Text):
                    if tam is not None and tam < 24:
                        print(f"[audit] {t:7.1f}s TEXTO PEQUENO {nome(a)} ({tam})")
                else:
                    fs = a.font_size
                    na_conta = (x0 + x1) / 2 > 1.1
                    eq = "=" in a.get_tex_string()
                    minimo = (46 if eq else 34) if na_conta else 36
                    if fs < minimo - 0.5:
                        print(f"[audit] {t:7.1f}s TEXTO PEQUENO {nome(a)} ({fs:.0f} < {minimo})")
            for b in itens[i + 1:]:
                if a in b.get_family() or b in a.get_family():
                    continue
                if voando and (id(a) in voando or id(b) in voando):
                    continue
                bx0, by0, bx1, by1 = bb(b)
                w, h = min(x1, bx1) - max(x0, bx0), min(y1, by1) - max(y0, by0)
                if w > 0.03 and h > 0.03:
                    print(f"[audit] {t:7.1f}s SOBREPOSICAO {nome(a)} x {nome(b)} ({w:.2f}x{h:.2f})")
                elif w > -0.09 and h > -0.09 and not (tams.get(id(a), (0, False))[1] or tams.get(id(b), (0, False))[1]):
                    print(f"[audit] {t:7.1f}s ENCOSTADO {nome(a)} x {nome(b)} (folga < 0,03)")
        self._auditar_v3(t, itens, objs, op, tams, fixos, nome)
        self._auditar_v4(t, itens, objs, op, tams, fixos, nome)
        if _final and not getattr(self, "_em_troca", False):
            self._auditar_v5(t, itens, op)

    def _selo_sobre_3d(self, b, comp):
        """v3 §4: SELO EM CIMA DE OBJETO 3D — selo/etiqueta de referencial sobre a área do foguete 3D (b = bocal na tela, comp = comprimento)."""
        if not AUDITORIA:
            return
        x0, x1, y0, y1 = float(b[0]) - 0.25, float(b[0]) + comp + 0.25, float(b[1]) - 0.3, float(b[1]) + 0.3
        for m in (getattr(self, "s1", None), getattr(self, "ref_mob", None)):
            if m is None or not m.get_family():
                continue
            if min(x1, float(m.get_right()[0])) - max(x0, float(m.get_left()[0])) > 0.02 and min(y1, float(m.get_top()[1])) - max(y0, float(m.get_bottom()[1])) > 0.02:
                print(f"[audit] {self.clk.get_value():7.1f}s SELO EM CIMA DE OBJETO 3D (foguete)")

    def _auditar_v5(self, t, itens, op):
        """v3 §4: OPACIDADE — nenhum texto (CONTA, rótulo, selo) abaixo de 100% depois de terminar de entrar (estado final de cada play)."""
        vistos = getattr(self, "_op_vistos", None)
        if vistos is None:
            vistos = self._op_vistos = set()
        for m in itens:
            for x in m.get_family():
                if isinstance(x, (Text, SingleStringMathTex, MathTex)) and 0.05 < op(x) < 0.985 and not getattr(x, "_op_ok", False):
                    chave = (type(x).__name__, getattr(x, "text", None) or getattr(x, "tex_string", "?"))
                    if chave not in vistos:
                        vistos.add(chave)
                        print(f"[audit] {t:7.1f}s OPACIDADE {chave[1][:40]!r} em {op(x):.2f} (< 1,00 depois de entrar)")

    # ── auditoria v4 (handoff v4 §3) ───────────────────────────────────────────────────────────────────────────────
    def _lago_polis(self, f3):
        """Folha (polígono da lâmina com a largura de verdade) e gafanhoto (retângulo ×esc) projetados pela câmera do quadro."""
        e = f3.e
        cam, g, f = e["cam"], e["g"], e["f"]
        Lg = 0.07 * g.get("esc", 1.5)
        us = np.linspace(0, 1, 16)
        folha = np.array([projeta3d(cam, (f["x"] + u * 0.30, s * 0.042 * math.sin(math.pi * u) ** 0.75, 0.0))
                          for s in (1, -1) for u in (us if s > 0 else us[::-1])])
        gaf = np.array([projeta3d(cam, (g["x"] + dx * Lg, 0.0, g["z"] + dz * Lg)) for dx in (-0.6, 0.6) for dz in (0.0, 0.45)])
        return folha, gaf

    def _contraste_folha(self, f3, folha, gaf):
        """Luminância mediana da lâmina × a da água num anel de 0,25 em volta (sem o gafanhoto), no PNG do Three.js do quadro."""
        a = f3.img.pixel_array
        h_, w_ = a.shape[:2]
        tp = lambda q: np.column_stack([(q[:, 0] + 8) / 16 * w_, (4.5 - q[:, 1]) / 9 * h_])
        F_ = tp(folha)
        x0, y0 = np.floor(F_.min(axis=0) - 15).astype(int)
        x1, y1 = np.ceil(F_.max(axis=0) + 15).astype(int)
        x0, y0, x1, y1 = max(0, x0), max(0, y0), min(w_ - 1, x1), min(h_ - 1, y1)
        if x1 <= x0 or y1 <= y0:
            return None
        xs, ys = np.meshgrid(np.arange(x0, x1 + 1), np.arange(y0, y1 + 1))
        q = np.column_stack([xs.ravel() + 0.5, ys.ravel() + 0.5])
        den = _Poli(F_).contains_points(q)
        G_ = tp(gaf)
        fora_g = ~((q[:, 0] >= G_[:, 0].min() - 4) & (q[:, 0] <= G_[:, 0].max() + 4) & (q[:, 1] >= G_[:, 1].min() - 4) & (q[:, 1] <= G_[:, 1].max() + 4))
        rgb = a[ys.ravel(), xs.ravel(), :3].astype(float) / 255
        Y = 0.2126 * rgb[:, 0] + 0.7152 * rgb[:, 1] + 0.0722 * rgb[:, 2]
        fo, ag = Y[den & fora_g], Y[~den & fora_g]
        if len(fo) < 8 or len(ag) < 8:
            return None
        return abs(float(np.median(fo)) - float(np.median(ag)))

    def _auditar_v4(self, t, itens, objs, op, tams, fixos, nome):
        """v4 §3: CALHA (nada em x 0,2…0,7 fora do canto e da faixa de selo), ENCOSTADO com folga 0,15 entre rótulos de unidades diferentes,
        TRÂNSITO (glifo em movimento sobre outro texto por 2 passadas seguidas), RÓTULO SOLTO (m =, M =, v =, L =, u = a > 0,6 do dono),
        MARCADORES COLADOS (⊕ a < 0,6 de outro marcador), FORA DA ZONA embaixo do ESQUEMA (texto, desenho e projeção do cubo 3D)."""
        import re as _re
        zonas = self.lote in self.ZONAS and not self.layout_v
        isento = set()
        for _, m in self._selos(op):
            isento |= set(id(x) for x in m.get_family())
        for m in self.mobjects:
            if getattr(m, "_chip", False) or getattr(m, "_tela_cheia", False) or getattr(m, "_selo", None):
                isento |= set(id(x) for x in m.get_family())
        if self.dica_atual is not None:
            isento |= set(id(x) for x in self.dica_atual.get_family())
        voando = getattr(self, "_voando", set()) | set(id(x) for r in getattr(self, "_voando_raiz", []) for x in r.get_family())
        pai = {}
        for m in self.mobjects:
            for x in m.get_family():
                for c in x.submobjects:
                    pai[id(c)] = x
        topos = set(id(m) for m in self.mobjects)
        txt_ids = set(id(x) for top in self.mobjects for m in top.get_family() if isinstance(m, (Text, SingleStringMathTex)) for x in m.get_family())
        bxc = {}

        def cx(m):
            if id(m) not in bxc:
                p_ = m.get_all_points()
                bxc[id(m)] = (p_[:, 0].min(), p_[:, 1].min(), p_[:, 0].max(), p_[:, 1].max()) if len(p_) else (0, 0, 0, 0)
            return bxc[id(m)]

        def unidade(a):
            """O rótulo montado (grupo só de texto, ex.: 'm' + '= 1 g') ou o próprio texto."""
            u, p_ = a, pai.get(id(a))
            while p_ is not None and id(p_) not in topos and p_.width < 6 and \
                    all(id(x) in txt_ids for x in p_.family_members_with_points()):
                u, p_ = p_, pai.get(id(p_))
            if p_ is not None and id(p_) in topos and p_.width < 6 and all(id(x) in txt_ids for x in p_.family_members_with_points()):
                u = p_
            return u
        def nm(m):
            if isinstance(m, (Text, SingleStringMathTex)):
                return nome(m)
            if getattr(m, "_tex", None):
                return f"'{str(m._tex)[:30]}'"
            return f"glifo em ({m.get_x():.1f}; {m.get_y():.1f})"
        # TRÂNSITO: posição de cada glifo × passada anterior do mesmo play
        pid = getattr(self, "_npl", 0)
        ant = getattr(self, "_tr_ant", None)
        if ant is None or ant[0] != pid:
            ant = (pid, {}, set(), set())
        pos_ant, cruz_ant, ja = ant[1], ant[2], ant[3]
        gls, dono_gl = [], []

        def rotulo_de(x):
            y = x
            while y is not None:
                if isinstance(y, (Text, SingleStringMathTex)) or getattr(y, "_tex", None):
                    return y
                y = pai.get(id(y))
            return x
        for top in self.mobjects:                            # glifos de verdade (caminhos SVG de Text/MathTex), inclusive os grupos soltos que voam
            if top in fixos or top is self.clk or id(top) in isento:
                continue
            for x in top.family_members_with_points():
                if type(x).__name__ == "VMobjectFromSVGPath" and id(x) not in isento and op(x) > 0.15:
                    gls.append(x)
                    dono_gl.append(rotulo_de(x))
        movendo = set()
        cruz = set()
        fonte_ids = set()                                    # a cópia saindo de cima da própria origem (e do rótulo dela) não é trânsito
        for f_ in getattr(self, "_fontes", []):
            for x in f_.family_members_with_points():
                fonte_ids |= set(id(y) for y in unidade(x).get_family())
        if gls:
            Bx = np.array([cx(g_) for g_ in gls])
            C = np.column_stack([(Bx[:, 0] + Bx[:, 2]) / 2, (Bx[:, 1] + Bx[:, 3]) / 2])
            D = np.array([C[i] - pos_ant[id(g_)] if id(g_) in pos_ant else (0.0, 0.0) for i, g_ in enumerate(gls)])
            mov = np.linalg.norm(D, axis=1) > 0.012
            S = Bx + np.array([0.03, 0.03, -0.03, -0.03])
            cf_ = np.array([((b[0] + b[2]) / 2, (b[1] + b[3]) / 2) for f_ in getattr(self, "_fontes", []) for b in
                            [cx(x) for x in f_.family_members_with_points()]]).reshape(-1, 2)
            na_fonte = np.array([bool(len(cf_)) and float(np.min(np.linalg.norm(cf_ - C[k], axis=1))) < 0.02 for k in range(len(gls))])   # cópia que ainda não saiu
            for i in np.nonzero(mov)[0]:
                movendo.add(id(dono_gl[i]))
                ox = np.minimum(S[i, 2], S[:, 2]) - np.maximum(S[i, 0], S[:, 0])
                oy = np.minimum(S[i, 3], S[:, 3]) - np.maximum(S[i, 1], S[:, 1])
                rel = np.linalg.norm(D - D[i], axis=1) > 0.01
                hit = (ox > 0) & (oy > 0) & rel & np.array([id(g_) not in fonte_ids for g_ in gls]) & ~(na_fonte & ~mov) & \
                    np.array([dono_gl[k] is not dono_gl[i] for k in range(len(gls))])            # vizinhos do mesmo grupo que viaja junto não contam
                hit[i] = False
                for j in np.nonzero(hit)[:1][0][:1]:                     # o glifo que se move cruza algum texto em duas passadas seguidas
                    gi = id(gls[i])
                    cruz.add(gi)
                    if gi in cruz_ant and gi not in ja:
                        ja.add(gi)
                        print(f"[audit] {t:7.1f}s TRÂNSITO glifo de {nm(dono_gl[i])} cruza {nm(dono_gl[j])} por mais de 2 quadros")
            if os.environ.get("TRDEBUG") and float(os.environ["TRDEBUG"].split(",")[0]) <= t <= float(os.environ["TRDEBUG"].split(",")[1]):
                print(f"[trdebug] {t:.2f} pid {pid} glifos {len(gls)} novos {sum(1 for g_ in gls if id(g_) not in pos_ant)} movendo {int(mov.sum())} cruz {len(cruz)} ant {len(cruz_ant)}")
            pos_ant = {id(g_): C[i] for i, g_ in enumerate(gls)}
        self._tr_ant = (pid, pos_ant, cruz, ja)
        parado = lambda a: id(a) not in voando and id(a) not in movendo and id(a) not in isento and not tams.get(id(a), (None, False))[1]
        livres = [a for a in itens if parado(a)]
        # CALHA (v4 §3.1): nada desenhado em x ∈ (0,2; 0,7) abaixo da faixa de selo
        if zonas:
            for a in livres:
                x0, y0, x1, y1 = cx(a)
                if x1 > 0.23 and x0 < 0.67 and y0 < 2.85:
                    print(f"[audit] {t:7.1f}s CALHA texto {nome(a)} em x {x0:.2f}…{x1:.2f}")
            for o in objs:
                if id(o) in isento:
                    continue
                pts = o.points
                m_ = (pts[:, 0] > 0.23) & (pts[:, 0] < 0.67) & (pts[:, 1] < 2.85)
                if m_.any():
                    print(f"[audit] {t:7.1f}s CALHA desenho {type(o).__name__} em ({pts[m_, 0].mean():.2f}; {pts[m_, 1].mean():.2f})")
            for top in self.mobjects:
                if top in fixos:
                    continue
                for m in top.get_family():
                    if getattr(m, "_fundo", False) and id(m) not in isento and m.points.size and op(m) > 0.3:
                        x0, y0, x1, y1 = cx(m)
                        if x1 > 0.23 and x0 < 0.67 and y0 < 2.85:
                            print(f"[audit] {t:7.1f}s CALHA caixa em x {x0:.2f}…{x1:.2f}")
        # ENCOSTADO v4: folga mínima de 0,15 entre rótulos de unidades diferentes (ao menos um no ESQUEMA)
        un = {id(a): unidade(a) for a in livres}
        for i, a in enumerate(livres):
            ax0, ay0, ax1, ay1 = cx(a)
            for b in livres[i + 1:]:
                if un[id(a)] is un[id(b)] or (a.get_x() > self.SX() and b.get_x() > self.SX()):
                    continue
                bx0, by0, bx1, by1 = cx(b)
                gx, gy = max(bx0 - ax1, ax0 - bx1), max(by0 - ay1, ay0 - by1)
                if gx < 0 and gy < 0:
                    continue
                num_ = lambda m: isinstance(m, Text) and _re.fullmatch(r"[−-]?\d+", m.text or "")
                if num_(a) and num_(b) and abs(a.get_y() - b.get_y()) < 0.05:           # números da mesma régua
                    continue
                if 0 <= gy < 0.15 and gx < 0 and min(ax1, bx1) - max(ax0, bx0) > 0.6 * min(ax1 - ax0, bx1 - bx0):   # rótulo de duas linhas (uma embaixo da outra)
                    continue
                if max(gx, gy) < 0.15:
                    print(f"[audit] {t:7.1f}s ENCOSTADO (folga {max(gx, gy):.2f} < 0,15) {nome(a)} x {nome(b)}")
        # texto sobre outro corpo (v4 #5): rótulo no meio de um corpo de aço de outro grupo (fora de um mostrador/caixa)
        topo_id = {}
        for k_, m in enumerate(self.mobjects):
            for x in m.get_family():
                topo_id.setdefault(id(x), k_)
        corpos_v4 = []
        caixas_v4 = []
        for top in self.mobjects:
            if top in fixos:
                continue
            for m in top.get_family():
                if not m.points.size or op(m) < 0.3 or id(m) in isento:
                    continue
                if getattr(m, "_caixa", False):
                    caixas_v4.append(cx(m))
                elif getattr(m, "_degrade", None) == "aco" and getattr(m, "_fundo", False):     # corpo-cenário (plataforma da balança): texto só no mostrador dele
                    x0, y0, x1, y1 = cx(m)
                    if x1 - x0 > 0.4 and y1 - y0 > 0.3:
                        corpos_v4.append((topo_id.get(id(m)), m, (x0, y0, x1, y1)))
        for a in livres:
            x0, y0, x1, y1 = cx(a)
            c_ = ((x0 + x1) / 2, (y0 + y1) / 2)
            if any(b[0] - 0.01 <= x0 and x1 <= b[2] + 0.01 and b[1] - 0.01 <= y0 and y1 <= b[3] + 0.01 for b in caixas_v4):
                continue
            for k_, m, b in corpos_v4:
                if k_ != topo_id.get(id(a)) and b[0] < c_[0] < b[2] and b[1] < c_[1] < b[3]:
                    print(f"[audit] {t:7.1f}s TEXTO SOBRE OBJETO {nome(a)} no meio de outro corpo ({type(m).__name__})")
                    break
        # tracejado de fronteira (SISTEMA): rótulo a pelo menos 0,2 dele (v4 #6)
        for top in self.mobjects:
            if top in fixos:
                continue
            for m in top.get_family():
                if isinstance(m, DashedVMobject) and op(m) > 0.3 and id(m) not in isento and max(m.width, m.height) > 2.5:   # fronteira (não ícone)
                    Q = m.get_all_points()
                    fam = set(id(x) for x in m.get_family())
                    mx0, my0, mx1, my1 = cx(m)
                    for a in livres:
                        if id(a) in fam:
                            continue
                        x0, y0, x1, y1 = cx(a)
                        if mx0 < (x0 + x1) / 2 < mx1 and my0 < (y0 + y1) / 2 < my1:          # rótulo de dentro (o furo, o sistema): vale a regra do corpo
                            continue
                        if any(b[0] - 0.01 <= x0 and x1 <= b[2] + 0.01 and b[1] - 0.01 <= y0 and y1 <= b[3] + 0.01 for b in caixas_v4):   # mostrador
                            continue
                        dx_ = np.maximum.reduce([x0 - Q[:, 0], np.zeros(len(Q)), Q[:, 0] - x1])
                        dy_ = np.maximum.reduce([y0 - Q[:, 1], np.zeros(len(Q)), Q[:, 1] - y1])
                        d_ = float(np.hypot(dx_, dy_).min())
                        if d_ < 0.2:
                            print(f"[audit] {t:7.1f}s ENCOSTADO no tracejado {nome(a)} (folga {d_:.2f} < 0,2)")
        # selo do referencial: nada a menos de 0,3 dele
        for tipo, s_ in self._selos(op):
            if tipo != "ref":
                continue
            fs = set(id(x) for x in s_.get_family())
            x0, y0, x1, y1 = cx(s_)
            x0, y0, x1, y1 = x0 - 0.3, y0 - 0.3, x1 + 0.3, y1 + 0.3
            for a in livres:
                if id(a) in fs:
                    continue
                bx0, by0, bx1, by1 = cx(a)
                if min(x1, bx1) > max(x0, bx0) and min(y1, by1) > max(y0, by0):
                    print(f"[audit] {t:7.1f}s ENCOSTADO no selo do referencial {nome(a)} (< 0,3)")
            for o in objs:
                if id(o) in fs or id(o) in isento:
                    continue
                pts = o.points
                if ((pts[:, 0] > x0) & (pts[:, 0] < x1) & (pts[:, 1] > y0) & (pts[:, 1] < y1)).any():
                    print(f"[audit] {t:7.1f}s ENCOSTADO no selo do referencial desenho {type(o).__name__}")
                    break
        # RÓTULO SOLTO (v4 §3.4): rótulo de dado longe do objeto que ele nomeia
        lagos = [f3 for f3 in self._lago3d() if f3.e and "g" in f3.e and "cam" in f3.e and f3.op.get_value() > 0.3]
        pat = _re.compile(r"^(m|M|v|L|u)(_[a-z0-9]+)?=")
        vistos_u = set()
        for a in (livres if (zonas or lagos) else []):                # rótulo de dado: nos problemas e no lago (não nas fórmulas do epílogo)
            u = un[id(a)]
            if id(u) in vistos_u:
                continue
            vistos_u.add(id(u))
            partes = [x.text if isinstance(x, Text) else x.get_tex_string() for x in u.get_family() if isinstance(x, (Text, MathTex))
                      and not any(isinstance(y, (Text, MathTex)) and y is not x and x in y.get_family() for y in u.get_family())] \
                if not isinstance(u, (Text, MathTex)) else [u.text if isinstance(u, Text) else u.get_tex_string()]
            s = _re.sub(r"\\(vec|mathrm|,|;|!|\ )|[{}\s]", "", "".join(partes))
            mt = pat.match(s)
            if not mt:
                continue
            x0, y0, x1, y1 = cx(u)
            if zonas and (x0 + x1) / 2 > 0.45:
                continue
            d_ = getattr(u, "_dono", None) or getattr(a, "_dono", None)
            P_ = None
            if d_ is not None:
                P_ = np.asarray(d_() if callable(d_) else d_.get_all_points(), float).reshape(-1, 3)
            elif lagos and mt.group(1) in ("m", "M"):
                fo_, ga_ = self._lago_polis(lagos[0])
                P_ = ga_ if mt.group(1) == "m" else fo_
            else:
                fam = set(id(x) for x in u.get_family())
                cand = [o.points for o in objs if id(o) not in fam]
                P_ = np.vstack(cand) if cand else None
            if P_ is None or not len(P_):
                continue
            dx_ = np.maximum.reduce([x0 - P_[:, 0], np.zeros(len(P_)), P_[:, 0] - x1])
            dy_ = np.maximum.reduce([y0 - P_[:, 1], np.zeros(len(P_)), P_[:, 1] - y1])
            dist = float(np.hypot(dx_, dy_).min())
            if dist > 0.6:
                print(f"[audit] {t:7.1f}s RÓTULO SOLTO {nome(a)} a {dist:.2f} do dono")
        # MARCADORES COLADOS: o ⊕ a menos de 0,6 de outro marcador pontual (círculo/ponto pequeno de outro grupo)
        topo_de = {}
        for k_, m in enumerate(self.mobjects):
            for x in m.get_family():
                topo_de.setdefault(id(x), k_)
        cms = [m for top in self.mobjects if top not in fixos for m in top.get_family() if getattr(m, "_cm", False) and op(m) > 0.3]
        if cms:
            fam_cm = set(id(x) for c in cms for x in c.get_family())
            heat = ManimColor(HEAT).to_hex().upper()
            marcas = [o for o in objs if isinstance(o, (Circle, Dot)) and id(o) not in fam_cm and o.width < 0.5 and op(o) > 0.3 and
                      (o.get_fill_opacity() < 0.1 or o.width < 0.14) and
                      heat in (ManimColor(o.get_stroke_color()).to_hex().upper(), ManimColor(o.get_fill_color()).to_hex().upper())]   # outro ponto calculado (laranja)
            for c in cms:
                cc = c.get_center()
                for o in marcas:
                    if topo_de.get(id(o)) == topo_de.get(id(c)) or getattr(self.mobjects[topo_de.get(id(o), 0)], "_flash", False):
                        continue
                    d__ = float(np.linalg.norm(o.get_center()[:2] - cc[:2]))
                    if d__ < 0.6:
                        print(f"[audit] {t:7.1f}s MARCADORES COLADOS ⊕ e {type(o).__name__} a {d__:.2f}")
                        break
        # FORA DA ZONA embaixo do ESQUEMA (y < −3,7) e a projeção do 3D do cubo (FORA DA MARGEM vale para o Three.js)
        if zonas:
            for a in livres:
                x0, y0, x1, y1 = cx(a)
                if (x0 + x1) / 2 < 0.45 and y0 < -3.7:
                    print(f"[audit] {t:7.1f}s FORA DA ZONA texto do ESQUEMA embaixo {nome(a)} (base {y0:.2f})")
            for o in objs:
                if id(o) in isento:
                    continue
                pts = o.points
                e_ = pts[:, 0] < 0.2
                if e_.any() and (pts[e_, 1] < -3.72).any() and pts[:, 0].mean() < 0.45:
                    print(f"[audit] {t:7.1f}s FORA DA ZONA desenho embaixo do ESQUEMA {type(o).__name__} (y {pts[e_, 1].min():.2f})")
            if hasattr(self, "pts_cubo") and any(isinstance(m, Fundo3D) and m.cena == "cubo" and m.op.get_value() > 0.3 for m in self.mobjects):
                try:
                    Q = np.asarray(self.pts_cubo(), float).reshape(-1, 3)
                except Exception:
                    Q = np.zeros((0, 3))
                if len(Q) and ((np.abs(Q[:, 0]) > 7.55).any() or (np.abs(Q[:, 1]) > 4.05).any()):
                    print(f"[audit] {t:7.1f}s OBJETO FORA DA MARGEM cubo 3D (projeção)")
                elif len(Q) and (Q[:, 1] < -3.7).any():
                    print(f"[audit] {t:7.1f}s FORA DA ZONA cubo 3D embaixo do ESQUEMA (y {Q[:, 1].min():.2f})")

    # ── auditoria v3 (handoff v3 §3)───────────────────────────────────────────────────────────────────────────────
    def SX(self):
        return 99.0 if self.layout_v else 0.45

    layout_v = False                                             # v2: T2-2…T2-5 com quadros em cima e CONTA embaixo (sem divisão em x)
    ZONAS = ("PT1", "PT2", "PT3", "PT4", "PT5", "PT6")   # yt_0022: lotes com PALCO/ESQUEMA × CONTA

    def _selos(self, op):
        """Selos na tela: (tipo, mob). Tipo 'ref' (VISTO DA …, borda violeta) ou 'faixa' (PEDE/CONFERE/DICA/HIPÓTESE)."""
        out = []
        for m in self.mobjects:
            tipo = getattr(m, "_selo", None)
            if tipo is None and isinstance(m, VGroup) and m.z_index == 36 and m.submobjects and isinstance(m[0], RoundedRectangle) \
                    and getattr(m[0], "_fundo", False):
                tipo = "ref" if ManimColor(m[0].get_stroke_color()).to_hex().upper() == ManimColor(VEL).to_hex().upper() else "faixa"
            if tipo and op(m) > 0.1:
                out.append((tipo, m))
        return out

    def _lago3d(self):
        """Fundos 3D do lago na cena (estado do quadro e opacidade)."""
        return [m for m in self.mobjects if isinstance(m, Fundo3D) and m.cena == "lago"]

    def _auditar_v3(self, t, itens, objs, op, tams, fixos, nome):
        # densidade de texto (prancha humana do G28 v3): glifos visíveis fora do cabeçalho
        n_gl = sum(len(a.family_members_with_points()) for a in itens if not tams.get(id(a), (None, False))[1])
        print(f"[dens] {t:.2f} {n_gl}")
        # COLUNA VAZIA (yt_0022 §7.3 #4): região x > 0,6 u sem nenhum objeto por mais de 5 s é falha
        tem_dir = any(a.get_right()[0] > 0.6 for a in itens if not tams.get(id(a), (None, False))[1]) or \
                  any(o.points[:, 0].max() > 0.6 for o in objs)
        if not tem_dir:
            for m in self.mobjects:
                if isinstance(m, Fundo3D) and m.op.get_value() > 0.15 and getattr(m, "alfa", None) is not None and m.alfa.size:
                    if m.alfa[:, int((0.6 + 8) / 16 * m.alfa.shape[1]):].max() > 15:
                        tem_dir = True
                        break
        print(f"[col_dir] {t:.2f} {1 if tem_dir else 0}")
        if tem_dir:
            self._t_col_ok = t
        else:
            t0_col = getattr(self, "_t_col_ok", None)
            if t0_col is None:
                self._t_col_ok = t
            elif t - t0_col > 5.0:
                print(f"[audit] {t:7.1f}s COLUNA VAZIA x > 0,6 sem objeto por {t - t0_col:.1f}s (> 5,0s)")
        # SELO DUPLO: dois selos do mesmo tipo com opacidade > 0,1 no mesmo quadro
        sel = self._selos(op)
        for tipo in ("faixa", "ref"):
            n_ = sum(1 for k, _ in sel if k == tipo)
            if n_ > 1:
                print(f"[audit] {t:7.1f}s SELO DUPLO {n_} selos '{tipo}' visíveis")
        # LINHA ÓRFÃ: linha da Pilha que começa com '=', '⇒' ou '→' visível sem a linha-mãe acima
        pil = getattr(self, "pilha", None)
        if pil is not None:
            na_cena = set(id(x) for m in self.mobjects for x in m.get_family())
            vis = lambda l: id(l) in na_cena and op(l) > 0.3
            filhas = (r"=", r"\Rightarrow", r"\rightarrow", r"\to")
            def tex_inicial(l):
                x = next((x for x in l.get_family() if isinstance(x, (Text, MathTex))), None)
                return x.get_tex_string().strip() if isinstance(x, MathTex) else None
            for i, (l, _) in enumerate(pil.linhas):
                tx_ = tex_inicial(l)
                if tx_ is None:
                    continue
                if tx_.startswith(filhas) and vis(l) and (i == 0 or not vis(pil.linhas[i - 1][0])):
                    print(f"[audit] {t:7.1f}s LINHA ÓRFÃ '{tx_[:30]}' sem a linha-mãe")
            dentro_p = set(id(x) for l, _ in pil.linhas for x in l.get_family())
            for l in [m for m in self.mobjects if m not in fixos and id(m) not in dentro_p]:      # linha que saiu da Pilha e ficou na tela
                tx_ = tex_inicial(l)
                if tx_ and tx_.strip().startswith("=") and l.get_x() > 0.5 and op(l) > 0.3 and \
                        not any(id(x) in dentro_p for x in l.get_family()):
                    print(f"[audit] {t:7.1f}s LINHA ÓRFÃ '{tx_.strip()[:30]}' solta (fora da Pilha)")
            for i, (l, _) in enumerate(pil.linhas):                              # P3: caixa que começa com "=" é órfã por definição
                if isinstance(l, VGroup) and l.submobjects and isinstance(l[0], RoundedRectangle) and vis(l):
                    tx_ = next((x.get_tex_string() for x in l.get_family() if isinstance(x, MathTex)), "").strip()
                    if tx_.startswith(filhas):
                        print(f"[audit] {t:7.1f}s LINHA ÓRFÃ caixa sem lado esquerdo '{tx_[:30]}'")
                if i > 0 and vis(l):                                             # filha embaixo de uma caixa (a caixa fecha o bloco)
                    tx_ = tex_inicial(l) or ""
                    ant = pil.linhas[i - 1][0]
                    if tx_.startswith(filhas) and isinstance(ant, VGroup) and ant.submobjects and isinstance(ant[0], RoundedRectangle):
                        print(f"[audit] {t:7.1f}s LINHA ÓRFÃ '{tx_[:30]}' embaixo de uma caixa")
        zonas = self.lote in self.ZONAS and not self.layout_v
        sels = set(id(x) for _, m in sel for x in m.get_family())
        # topo de cada texto (para separar rótulos de grupos diferentes)
        topo_de = {}
        for k_, m in enumerate(self.mobjects):
            for x in m.get_family():
                topo_de.setdefault(id(x), k_)
        pais = {}
        for m in self.mobjects:
            for x in m.get_family():
                for c in x.submobjects:
                    pais[id(c)] = id(x)
        voando_ = getattr(self, "_voando", set()) | set(id(x) for r in getattr(self, "_voando_raiz", []) for x in r.get_family())
        livres = [a for a in itens if not tams.get(id(a), (None, False))[1] and id(a) not in sels and a.get_x() < self.SX() and id(a) not in voando_ and
                  not (self.dica_atual is not None and a in self.dica_atual.get_family())]
        caixa_t = {id(a): (a.get_critical_point(DL)[:2], a.get_critical_point(UR)[:2]) for a in livres}
        # MESMA LINHA / EMPILHADO (ESQUEMA): rótulos de grupos diferentes colados (lidos como um só: "2 kg0", "−4,9" em cima de "3 kg")
        for i, a in enumerate(livres):
            (ax0, ay0), (ax1, ay1) = caixa_t[id(a)]
            for b in livres[i + 1:]:
                if pais.get(id(a)) == pais.get(id(b)) or topo_de.get(id(a)) == topo_de.get(id(b)):     # o mesmo rótulo montado não conta
                    continue
                (bx0, by0), (bx1, by1) = caixa_t[id(b)]
                hy = min(ay1, by1) - max(ay0, by0)
                hx = min(ax1, bx1) - max(ax0, bx0)
                gx = max(bx0 - ax1, ax0 - bx1)
                gy = max(by0 - ay1, ay0 - by1)
                if hy > 0.5 * min(ay1 - ay0, by1 - by0) and 0.0 <= gx < 0.2:
                    print(f"[audit] {t:7.1f}s ENCOSTADO na mesma linha {nome(a)} x {nome(b)} (folga {gx:.2f})")
                elif hx > 0.5 * min(ax1 - ax0, bx1 - bx0) and 0.0 <= gy < 0.22:
                    print(f"[audit] {t:7.1f}s ENCOSTADO empilhado {nome(a)} x {nome(b)} (folga {gy:.2f})")
        # ESPREMIDO: rótulo num vão estreito entre dois corpos de aço (corpo a < 0,6 dos dois lados, na mesma altura)
        corpos_b = []
        for top in self.mobjects:
            if top in fixos:
                continue
            for m in top.get_family():
                if getattr(m, "_degrade", None) == "aco" and op(m) > 0.3 and m.points.size:
                    (cx0, cy0, _), (cx1, cy1, _) = m.get_critical_point(DL), m.get_critical_point(UR)
                    if cx1 - cx0 > 0.3 and cy1 - cy0 > 0.3:
                        corpos_b.append((cx0, cy0, cx1, cy1))
        for a in livres:
            (ax0, ay0), (ax1, ay1) = caixa_t[id(a)]
            esq = any(c[2] <= ax0 + 0.02 and ax0 - c[2] < 0.6 and min(ay1, c[3]) - max(ay0, c[1]) > -0.3 for c in corpos_b)
            dir_ = any(c[0] >= ax1 - 0.02 and c[0] - ax1 < 0.6 and min(ay1, c[3]) - max(ay0, c[1]) > -0.3 for c in corpos_b)
            if esq and dir_:
                print(f"[audit] {t:7.1f}s ESPREMIDO {nome(a)} no vão entre dois corpos")
        # RÉGUA DUPLA: duas fileiras de números de régua no ESQUEMA (uma régua com números por vez)
        import re as _re2
        fil = {}
        for a in livres:
            if isinstance(a, Text) and _re2.fullmatch(r"[−-]?\d+", a.text or ""):
                fil.setdefault(round(a.get_y() * 5), []).append(a)
        if sum(1 for v in fil.values() if len(v) >= 3) >= 2:
            print(f"[audit] {t:7.1f}s RÉGUA DUPLA duas fileiras de números de régua na tela")
        # ZONAS (§4): ESQUEMA x −7,3…0,2 / y −3,65…2,50; Pilha x 0,7…7,3 / y −3,65…2,60; faixa de selo y 2,85…3,50; chip y 2,60…3,00
        if zonas:
            chip = set(id(x) for m in self.mobjects if getattr(m, "_chip", False) for x in m.get_family())
            for a in itens:
                if tams.get(id(a), (None, False))[1] or id(a) in sels or id(a) in chip or \
                        (self.dica_atual is not None and a in self.dica_atual.get_family()):
                    continue
                (x0, y0, _), (x1, y1, _) = a.get_critical_point(DL), a.get_critical_point(UR)
                if (x0 + x1) / 2 < self.SX():
                    if y1 > 2.55 or x0 < -7.35:
                        print(f"[audit] {t:7.1f}s FORA DA ZONA texto do ESQUEMA {nome(a)} (topo {y1:.2f})")
                elif y1 > 2.45 or x1 > 6.8 or y0 < -3.35:      # yt_0019 §3 G25: Pilha x 0,7…6,7 / y −3,25…2,35
                    print(f"[audit] {t:7.1f}s FORA DA ZONA texto da CONTA {nome(a)} ({x0:.2f}…{x1:.2f}; {y0:.2f}…{y1:.2f})")
            for o in objs:
                if id(o) in sels or id(o) in chip:
                    continue
                pts = o.points
                esq = pts[:, 0] < 0.2
                if esq.any() and (pts[esq, 1] > 2.55).any() and pts[:, 0].mean() < self.SX():
                    print(f"[audit] {t:7.1f}s FORA DA ZONA desenho acima do ESQUEMA {type(o).__name__} (y {pts[esq, 1].max():.2f})")
        # chamada cruzando corpo: linha fina (≤ 1,7, opacidade < 0,85) que atravessa um corpo de aço longe da ponta
        corpos = [(k_, m) for k_, top in enumerate(self.mobjects) if top not in fixos for m in top.get_family()
                  if getattr(m, "_degrade", None) == "aco" and op(m) > 0.3]
        polys = []
        for k_, c in corpos:
            for x in c.family_members_with_points():
                an_ = np.asarray(x.get_anchors(), float).reshape(-1, 3)
                if len(an_) > 3 and min(np.ptp(an_[:, 0]), np.ptp(an_[:, 1])) > 0.3:       # corpo com área (barra fina cruzada não conta)
                    polys.append((k_, _Poli(an_[:, :2])))
        if polys:
            for o in objs:
                if not isinstance(o, Line) or isinstance(o, DashedLine) or o.get_stroke_width() > 1.75 or o.get_stroke_opacity() >= 0.85:
                    continue
                a_, b_ = o.get_start(), o.get_end()
                if np.linalg.norm(b_ - a_) < 0.3:
                    continue
                qs = np.array([a_ + (b_ - a_) * u for u in np.linspace(0.0, 0.8, 12)])[:, :2]
                if any(k_ != topo_de.get(id(o)) and pp.contains_points(qs).any() for k_, pp in polys):
                    print(f"[audit] {t:7.1f}s CHAMADA CRUZA CORPO linha de chamada em ({o.get_x():.1f}; {o.get_y():.1f})")
        # PALCO 3D e FORA DO QUADRO 3D (lago): folha e gafanhoto como polígonos de colisão; legíveis enquanto houver desenho preso
        for f3 in self._lago3d():
            e = f3.e
            if not e or "g" not in e or "cam" not in e:
                continue
            cam, g, f = e["cam"], e["g"], e["f"]
            o3 = f3.op.get_value() * (f3.mult(self.clk.get_value()) if f3.mult else 1.0)
            Lg = 0.07 * g.get("esc", 1.5)
            folha = np.array([projeta3d(cam, (f["x"] + u * 0.30, s * 0.042 * math.sin(math.pi * u) ** 0.75, 0.0))
                              for s in (1, -1) for u in (np.linspace(0, 1, 16) if s > 0 else np.linspace(1, 0, 16))])
            gaf = np.array([projeta3d(cam, (g["x"] + dx * Lg, 0.0, g["z"] + dz * Lg)) for dx in (-0.6, 0.6) for dz in (0.0, 0.45)])
            presos = [o for o in objs if o.points[:, 0].mean() < 0.3 and id(o) not in sels] + \
                     [a for a in itens if a.get_x() < 0.3 and not tams.get(id(a), (None, False))[1] and id(a) not in sels]
            if o3 < 0.05 and not presos:
                continue
            if presos and o3 < 0.5 and not getattr(self, "_em_troca", False) and self.lote in self.ZONAS:
                print(f"[audit] {t:7.1f}s PALCO 3D desenho preso com a camada Three.js a {o3:.2f}")
            if o3 >= 0.5 and presos:
                comp_g = float(np.linalg.norm(gaf[2, :2] - gaf[0, :2]))
                comp_f = float(np.linalg.norm(folha[15, :2] - folha[0, :2]))
                if comp_g < 0.45:
                    print(f"[audit] {t:7.1f}s PALCO 3D gafanhoto ilegível ({comp_g:.2f} de comprimento na tela)")
                wf, hf = float(np.ptp(folha[:, 0])), float(np.ptp(folha[:, 1]))          # v4 §3.3: largura ≥ 25% do ESQUEMA, ou faixa com altura
                if not (wf >= 0.25 * 7.5 or (hf >= 0.08 and wf >= 1.2)):
                    print(f"[audit] {t:7.1f}s PALCO 3D folha ilegível ({wf:.2f} × {hf:.2f} na tela)")
                if not PEDIDOS3D and getattr(f3, "alfa", None) is not None and f3.alfa.max() > 0:
                    con = self._contraste_folha(f3, folha, gaf)
                    if con is not None and con < 0.08:
                        print(f"[audit] {t:7.1f}s PALCO 3D folha sem contraste com a água ({con:.3f} < 0,08)")
                if not PEDIDOS3D and getattr(f3, "alfa", None) is not None and f3.alfa.size and f3.alfa.max() > 0:
                    h_, w_ = f3.alfa.shape
                    c_ = folha.mean(axis=0)
                    px_, py_ = int((c_[0] + 8) / 16 * w_), int((4.5 - c_[1]) / 9 * h_)
                    if 0 <= px_ < w_ and 0 <= py_ < h_ and f3.alfa[max(0, py_ - 3):py_ + 4, max(0, px_ - 3):px_ + 4].max() < 10:
                        print(f"[audit] {t:7.1f}s PALCO 3D folha sem pixel no quadro (camada vazia)")
            for nm_, P_ in (("gafanhoto", gaf), ("folha", folha)):
                if o3 > 0.3 and zonas and ((np.abs(P_[:, 0]) > 7.75).any() or (np.abs(P_[:, 1]) > 4.25).any()):
                    print(f"[audit] {t:7.1f}s FORA DO QUADRO 3D {nm_} a menos de 0,25 da borda")
                if o3 > 0.3 and zonas and (P_[:, 1] > 2.5).any():
                    print(f"[audit] {t:7.1f}s FORA DA ZONA {nm_} 3D acima do ESQUEMA")
            pf = _Poli(folha[:, :2])
            gx0, gy0 = gaf[:, :2].min(axis=0)
            gx1, gy1 = gaf[:, :2].max(axis=0)
            if o3 > 0.3:
                for a in itens:
                    if tams.get(id(a), (None, False))[1] or id(a) in sels:
                        continue
                    (x0, y0, _), (x1, y1, _) = a.get_critical_point(DL), a.get_critical_point(UR)
                    grade = np.array([(x, y) for x in np.linspace(x0, x1, 6) for y in np.linspace(y0, y1, 4)])
                    if pf.contains_points(grade).any():
                        print(f"[audit] {t:7.1f}s TEXTO SOBRE OBJETO {nome(a)} x folha 3D")
                    elif min(x1, gx1) - max(x0, gx0) > 0.0 and min(y1, gy1) - max(y0, gy0) > 0.0:
                        print(f"[audit] {t:7.1f}s TEXTO SOBRE OBJETO {nome(a)} x gafanhoto 3D")
        # FORA DO QUADRO 3D: trajetória futura projetada (próximos 2 s) a menos de 0,25 da borda
        for fn in getattr(self, "_futuros", []):
            try:
                q = np.asarray(fn(), float).reshape(-1, 3)
            except Exception:
                continue
            if len(q) and zonas and ((np.abs(q[:, 0]) > 7.75).any() or (np.abs(q[:, 1]) > 4.25).any()):
                print(f"[audit] {t:7.1f}s FORA DO QUADRO 3D trajetória a menos de 0,25 da borda")
            if len(q) and zonas and (q[:, 1] > 2.5).any():
                print(f"[audit] {t:7.1f}s FORA DA ZONA trajetória acima do ESQUEMA (y {q[:, 1].max():.2f})")

    def relatorio(self):
        for aid, t0, prev, real in self.log:
            if aid != "FIM" and real > prev + 0.2:
                print(f"[tempo] {aid}: previsto {prev:.1f} s, real {real:.1f} s (cena mais longa que a fala)")
        for aid, t0, prev, real in self.log:
            print(f"[ancora] {aid} {t0:.2f}")
        for aid, atraso in self.abertas:
            if abs(atraso) > 0.05:
                print(f"[abertura] {aid} atrasada {atraso:+.2f} s")
        if self.faltou:
            print(f"[plano] marcas sem medição (ritmo 1): {self.faltou[:10]}")
        if AUDITORIA:
            print(f"[degrade] objetos com degradê por marca: {getattr(self, '_tags_degrade', {})}")
            n_ = getattr(self, "_cor_n", [0, 0])
            print(f"[cor] tokens conferidos: {n_[0]}; fora da tabela: {n_[1]}")
        print(f"[tempo] total {self.nq / FPS:.1f} s ({self.nq} quadros)")
        if PEDIDOS3D and self._ped:
            (DIR3D / "pedidos3d").mkdir(parents=True, exist_ok=True)
            out = {"cenas": {c: [[f, r4(e)] for f, e in sorted(d.items())] for c, d in self._ped.items()}}
            (DIR3D / "pedidos3d" / f"{self.lote}.json").write_text(json.dumps(out), encoding="utf-8")
            print(f"[3d] pedidos: " + ", ".join(f"{c} {len(d)}" for c, d in self._ped.items()))

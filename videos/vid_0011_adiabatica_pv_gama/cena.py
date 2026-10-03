"""De onde vem PV^gama = constante: preview visual silencioso (1ª versão).

POR TRÁS DA FÓRMULA · EP. 04.

Cadeia: dQ = 0 -> dU = -P dV -> dU = n C_V dT -> C_V dT/T = -R dV/V -> (Mayer) C_P - C_V = R
-> R/C_V = gama - 1 -> T V^(gama-1) = cte -> P V^gama = cte; depois isotérmica x adiabática.

Um único cilindro (classe Cyl) é a referência física recorrente. O volume v (V0 = 1) sai de UM
parâmetro, `prog` = pesos retirados: P_ext = PB + DP (NW - pesos retirados) e v = P_ext^(-1/g)
(g = gama adiabático, g = 1 isotérmico); T = v^(1-g). Pistão, gás, termômetro, pesos e o ponto do
gráfico P x V leem o mesmo `prog`: nenhum keyframe de posição.

Cores: ciano = energia interna (dU, n C_V dT) e adiabática; violeta = trabalho (P dV, n R dT);
magenta = calor (dQ) e isotérmica; azul = geometria; branco = texto e equações.

Tempos seguem os marcos do briefing (segundos): 15, 35, 55, 68, 90, 100, 125, 140, 160, 170.
`ATE=k` renderiza só até o segmento k (iteração); sem a variável, roda tudo.
"""

import json
import os
import sys
from contextlib import contextmanager
from pathlib import Path

import numpy as np
from manim import (
    DOWN, LEFT, PI, RIGHT, UP, UR, DL, Arrow, Axes, Create, DashedLine, Dot, FadeIn, FadeOut, Group,
    ImageMobject, Indicate, Line, Rectangle, MathTex, ParametricFunction, Polygon, ReplacementTransform, Scene,
    SurroundingRectangle, TransformFromCopy, VGroup, ValueTracker, always_redraw, config,
    interpolate_color, ManimColor, linear, smooth, AnimationGroup,
)

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from MF_Tools import TransformByGlyphMap
from template.config import BACKGROUND_COLOR, PRIMARY_COLOR, SECONDARY_COLOR, TEXT_COLOR, WATERMARK_PATH
from template.fonts import screen_text

ATE = int(os.environ.get("ATE", "99"))
PASTA = Path(__file__).resolve().parent
CAL = os.environ.get("SYNC_CAL") == "1"        # calibragem: mede o tempo NATIVO de cada âncora

# ── Paleta ──────────────────────────────────────────────────────────────────
WHITE = TEXT_COLOR
CYAN = PRIMARY_COLOR      # energia interna, adiabática
BLUE = "#267BFF"          # geometria, paredes
BLUE_L = "#7FB2FF"
VIOLET = "#9C8CFF"       # trabalho (SECONDARY_COLOR #745CFF clareado: contraste das equações)
MAGENTA = "#EA63FF"       # calor, isotérmica

SAFE_X = 3.5

# Cores dos termos na legenda queimada (montar_legendado.py --color-module); mesmos significados da cena
SUBTITLE_TERM_COLORS = {
    "energia interna": CYAN, "calor específico": CYAN, "calores específicos": CYAN, "adiabática": CYAN,
    "adiabático": CYAN,
    "trabalho": VIOLET,
    "calor": MAGENTA, "temperatura": MAGENTA, "isotérmica": MAGENTA, "esfria": MAGENTA, "esquentam": MAGENTA,
    "gama": BLUE_L, "Mayer": BLUE_L,
}
VF = 0.4 ** (-1.0 / 1.4)   # volume final comum (P_ext final 0,4 P0, gama 1,4)
EQ_K = 1.2                # escala global dos tamanhos das equações
GAMMA = 1.4               # só para desenhar; a dedução é simbólica


# ── Texto e utilidades de quadro (mesmo idioma do vid_0010) ─────────────────
@contextmanager
def wide_pango():
    pw, ph = config.pixel_width, config.pixel_height
    config.pixel_width, config.pixel_height = 4000, 4000
    try:
        yield
    finally:
        config.pixel_width, config.pixel_height = pw, ph


def text(content, size=24, color=WHITE, opacity=1.0):
    with wide_pango():
        t = screen_text(content, size)
    return t.set_color(color).set_opacity(opacity)


def tex(content, size=40, color=WHITE):
    return MathTex(content, font_size=size, color=color)


def fit(m, w=2 * SAFE_X - 0.3):
    if m.width > w:
        m.scale_to_fit_width(w)
    return m


def boxed_rect(mob, color=WHITE):
    return SurroundingRectangle(mob, color=color, buff=0.15, corner_radius=0.08, stroke_width=2.5)


def soft_swap(old, new, shift=UP * 0.12, lag=0.55):
    return AnimationGroup(FadeOut(old, shift=shift), FadeIn(new, shift=shift), lag_ratio=lag)


def tri(u):
    """Onda triangular em [0, 1]: movimento retilíneo com reflexão nas paredes."""
    u = (u / PI) % 2.0
    return 1.0 - abs(1.0 - u)


def smoothstep(u):
    u = float(np.clip(u, 0.0, 1.0))
    return u * u * (3 - 2 * u)


# ── Equações com índices de glifos (MF-Tools), como no vid_0010 ─────────────
class Eq:
    """MathTex de string única + índices de glifos por parte, para TransformByGlyphMap."""

    def __init__(self, *parts, size=46, colors=None):
        size = size * EQ_K
        multi = MathTex(*parts, font_size=size)
        self.s = np.concatenate([[0], np.cumsum([len(q) for q in multi])]).astype(int)
        self.mob = MathTex(" ".join(parts), font_size=size, color=WHITE)
        assert len(self.mob[0]) == int(self.s[-1]), parts
        for i, c in (colors or {}).items():
            self.mob[0][int(self.s[i]):int(self.s[i + 1])].set_color(c)

    def p(self, *ids):
        return [k for i in ids for k in range(int(self.s[i]), int(self.s[i + 1]))]

    def g(self, *ids):
        return [self.mob[0][k] for k in self.p(*ids)]

    def px(self, i):
        return sorted(self.p(i), key=lambda k: self.mob[0][k].get_center()[0])

    def frac(self, i):
        idx = self.p(i)
        c = {k: self.mob[0][k].get_center() for k in idx}
        bar = max(idx, key=lambda k: self.mob[0][k].width)
        num = sorted((k for k in idx if k != bar and c[k][1] > c[bar][1]), key=lambda k: c[k][0])
        den = sorted((k for k in idx if k != bar and c[k][1] < c[bar][1]), key=lambda k: c[k][0])
        return num, bar, den


def copy_from(src):
    """Introdutor: o destino nasce de uma CÓPIA dos glifos `src`, que ficam onde estão."""
    class _Copy(TransformFromCopy):
        def __init__(self, mob, **kw):
            super().__init__(VGroup(*src), mob, **kw)
    return _Copy


def M(A, pa, B, pb, **kw):
    return (A.p(*pa), B.p(*pb), kw)


def X(A, pa, **kw):
    return (A.p(*pa), [], kw)


def C(src, B, pb, **kw):
    kw.setdefault("delay", 0.2)
    return (copy_from(src), B.p(*pb), kw)


def MG(ga, gb, **kw):
    """Movimento por índices de glifos explícitos."""
    return (list(ga), list(gb), kw)


def CG(src, gb, **kw):
    kw.setdefault("delay", 0.2)
    return (copy_from(src), list(gb), kw)


def strike(eq, *ids, color=MAGENTA):
    """Riscos diagonais sobre as partes `ids` de uma Eq (cancelamento)."""
    return VGroup(*[Line(VGroup(*eq.g(i)).get_corner(DL), VGroup(*eq.g(i)).get_corner(UR),
                         color=color, stroke_width=4) for i in ids])


# ── Cilindro com pistão ─────────────────────────────────────────────────────
class Cyl:
    """Cilindro + pistão + gás + pesos. Coordenadas locais: centro da base do gás em (0, 0).

    mode "peso":  v e T saem de `prog` (pesos retirados) e do expoente `g`.
    mode "livre": v = vf e T = tf (pressão constante: pesos fixos).
    mode "rigido": v = 1 (tampa travada), T = tf.
    """
    W, HW, HP, PT, WT, NW = 2.2, 2.7, 0.95, 0.16, 0.12, 8
    WW, XS, SH = 1.2, 1.95, 2.8
    PB, DP = 0.4, 0.075

    def __init__(self, cx, cy, sc, mode="peso", g=GAMMA, op=1.0, ins=1.0, thm=0.0, heat=0.0, nfix=3, narr=3,
                 seed=0, pb=0.4, dp=0.075):
        self.mode, self.nfix, self.narr = mode, nfix, narr
        self.PB, self.DP = pb, dp
        mk = ValueTracker
        self.cx, self.cy, self.sc, self.op = mk(cx), mk(cy), mk(sc), mk(op)
        self.ins, self.thm, self.heat = mk(ins), mk(thm), mk(heat)
        self.prog, self.g = mk(0.0), mk(g)
        self.vf, self.tf, self.clock = mk(1.0), mk(1.0), mk(0.0)
        rng = np.random.default_rng(seed)
        self.dots = rng.uniform(0, 2 * PI, (14, 4))
        self.fq = rng.uniform(0.6, 1.6, (14, 2))
        self.Tlbl = MathTex("T", font_size=34, color=WHITE)
        self.clock.add_updater(lambda m, dt: m.increment_value(dt * (0.2 + 1.4 * max(self.temp(), 0.1))))
        self.body = always_redraw(self.draw)
        self.group = Group(self.cx, self.cy, self.sc, self.op, self.ins, self.thm, self.heat, self.prog, self.g,
                           self.vf, self.tf, self.clock, self.body)

    # estado físico
    def eff(self):
        p = self.prog.get_value()
        return sum(smoothstep((np.clip(p - j, 0, 1) - 0.45) / 0.5) for j in range(self.NW))

    def pext(self):
        return self.PB + self.DP * (self.NW - self.eff())

    def v(self):
        if self.mode == "peso":
            return self.pext() ** (-1.0 / self.g.get_value())
        return 1.0 if self.mode == "rigido" else self.vf.get_value()

    def p(self):
        return self.pext() if self.mode == "peso" else 1.0

    def temp(self):
        if self.mode == "peso":
            return self.v() ** (1.0 - self.g.get_value())
        return self.tf.get_value()

    def drive(self, target, secs):
        """Leva `prog` até `target` em `secs` s, em linha reta, enquanto a cena roda (updater)."""
        rate = (target - self.prog.get_value()) / secs

        def up(m, dt):
            v = m.get_value() + rate * dt
            if (rate > 0 and v >= target) or (rate < 0 and v <= target):
                v = target
                m.clear_updaters()
            m.set_value(v)
        self.prog.add_updater(up)

    def anchor(self):
        return np.array([self.cx.get_value(), self.cy.get_value(), 0.0])

    def draw(self):
        cx, cy, sc, op = (m.get_value() for m in (self.cx, self.cy, self.sc, self.op))
        ins, heat, thm = self.ins.get_value(), self.heat.get_value(), self.thm.get_value()
        W, HP, PT, WT = self.W, self.HP, self.PT, self.WT
        v, T = self.v(), self.temp()
        rigid = self.mode == "rigido"
        yp = HP * v
        HW = HP + PT if rigid else self.HW
        t = 0.14
        gas = interpolate_color(ManimColor(BLUE), ManimColor(MAGENTA), float(np.clip((T - 0.7) / 0.6, 0, 1)))
        parts = []

        def S(x, y):
            return np.array([cx + sc * x, cy + sc * y, 0.0])

        def poly(pts, fill=None, fo=0.0, stroke=None, sw=0.0, so=1.0):
            m = Polygon(*[S(*p) for p in pts])
            m.set_fill(fill or WHITE, fo * op)
            m.set_stroke(stroke or WHITE, sw * sc, so * op)
            return m

        def box(x0, y0, x1, y1, **kw):
            return poly([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], **kw)

        # isolante (hachura) e paredes
        if ins > 0.01:
            o = 0.22
            parts.append(poly([(-W / 2 - t - o, HW), (-W / 2 - t - o, -t - o), (W / 2 + t + o, -t - o),
                               (W / 2 + t + o, HW), (W / 2 + t, HW), (W / 2 + t, -t), (-W / 2 - t, -t),
                               (-W / 2 - t, HW)], fill="#9FB4E0", fo=0.22 * ins))
            for k in range(int(HW / 0.3)):
                y = 0.05 + 0.3 * k
                for xs in (-W / 2 - t - o, W / 2 + t):
                    ln = Line(S(xs, y), S(xs + o, y + o))
                    ln.set_stroke("#9FB4E0", 1.5 * sc, 0.7 * ins * op)
                    parts.append(ln)
            for k in range(int((W + 2 * t) / 0.3)):
                x = -W / 2 - t + 0.3 * k
                ln = Line(S(x, -t - o), S(x + o, -t))
                ln.set_stroke("#9FB4E0", 1.5 * sc, 0.7 * ins * op)
                parts.append(ln)
        parts.append(poly([(-W / 2 - t, HW), (-W / 2 - t, -t), (W / 2 + t, -t), (W / 2 + t, HW), (W / 2, HW),
                           (W / 2, 0), (-W / 2, 0), (-W / 2, HW)], fill="#16275A", fo=0.9, stroke=BLUE, sw=2.5))
        # gás
        parts.append(box(-W / 2, 0, W / 2, yp, fill=gas, fo=0.34))
        c = self.clock.get_value()
        for k, (a, b, c1, c2) in enumerate(self.dots):
            fx, fy = self.fq[k]
            x = -W / 2 + 0.1 + (W - 0.2) * tri(fx * c + a)
            y = 0.1 + (yp - 0.22) * tri(fy * c + b)
            d = Dot(S(x, y), radius=0.045 * sc, color=WHITE)
            d.set_opacity(0.75 * op)
            parts.append(d)
        if rigid:
            parts.append(box(-W / 2 - t, HP, W / 2 + t, HP + PT, fill="#16275A", fo=0.95, stroke=BLUE, sw=2.5))
            for xb in (-W / 2 + 0.25, W / 2 - 0.25):
                parts.append(Dot(S(xb, HP + PT / 2), radius=0.05 * sc, color=BLUE_L).set_opacity(op))
        else:
            parts.append(box(-W / 2 + 0.02, yp, W / 2 - 0.02, yp + PT, fill="#DDE6FF", fo=0.9, stroke=WHITE, sw=1.5))
        # pesos
        wt = WT - 0.015
        if self.mode == "peso":
            parts.append(box(self.XS - 0.75, self.SH - 0.07, self.XS + 0.75, self.SH, fill="#9FB4E0", fo=0.7))
            parts.append(box(self.XS - 0.05, -t, self.XS + 0.05, self.SH - 0.07, fill="#9FB4E0", fo=0.5))
            p = self.prog.get_value()
            for j in range(self.NW):
                i = self.NW - 1 - j
                y0 = yp + PT + i * WT
                q = float(np.clip(p - j, 0, 1))
                yc, yl = self.SH + 0.35 + j * WT, self.SH + j * WT
                if q <= 0:
                    x, y = 0.0, y0
                elif q < 0.25:
                    u = smoothstep(q / 0.25)
                    x, y = 0.0, y0 + u * (yc - y0)
                else:
                    u = smoothstep((q - 0.25) / 0.3)
                    x, y = u * self.XS, yc + u * (yl - yc)
                parts.append(box(x - self.WW / 2, y, x + self.WW / 2, y + wt, fill="#B9C6EA", fo=0.9,
                                 stroke="#E8EEFF", sw=1))
        elif not rigid:
            for i in range(self.nfix):
                y0 = yp + PT + i * WT
                parts.append(box(-self.WW / 2, y0, self.WW / 2, y0 + wt, fill="#B9C6EA", fo=0.9, stroke="#E8EEFF", sw=1))
        # fonte de calor
        if heat > 0.01:
            parts.append(box(-W / 2, -0.58, W / 2, -0.4, fill=MAGENTA, fo=0.5 * heat))
            for k in range(self.narr):
                x = (k - (self.narr - 1) / 2) * 0.55
                a = Arrow(S(x, -0.40), S(x, -0.04), buff=0, color=MAGENTA, stroke_width=5 * sc,
                          tip_length=0.15 * sc, max_tip_length_to_length_ratio=0.5)
                a.set_opacity(heat * op)
                parts.append(a)
        # termômetro
        if thm > 0.01:
            xt = -W / 2 - 0.75
            parts.append(box(xt - 0.08, 0, xt + 0.08, 2.0, stroke=WHITE, sw=1.5, so=0.6 * thm))
            h = 2.0 * float(np.clip((T - 0.6) / 0.9, 0.02, 1))
            parts.append(box(xt - 0.08, 0, xt + 0.08, h, fill=gas, fo=0.95 * thm))
            lbl = self.Tlbl.copy().scale(sc).move_to(S(xt, 2.3)).set_opacity(thm * op)
            parts.append(lbl)
        return VGroup(*parts)


# ── Cena ────────────────────────────────────────────────────────────────────
class AdiabaticaPVGama011(Scene):
    # ── infraestrutura ──────────────────────────────────────────────────────
    # Sincronia com a narração: cada self.ancora("x") casa um ponto do código com um instante da fala
    # (sync.json). `ntime` é o relógio NOMINAL da cena (soma dos run_time/waits sem escala; until(t) o
    # preenche até t). Entre duas âncoras, play/wait são escalados para o trecho durar o que a fala dura;
    # native.json guarda o tempo nominal de cada âncora (SYNC_CAL=1 regenera). Sem sync.json/native.json a
    # cena roda em tempo nominal (preview silencioso).
    def sync_init(self):
        self.tscale, self.ntime, self.nativos = 1.0, 0.0, {}
        arq = PASTA / "sync.json"
        dados = json.load(open(arq)) if arq.exists() else {}
        self.anc, self.extras = dados.get("anchors", []), dados.get("extras", {})
        nat = PASTA / "native.json"
        self.nat = json.load(open(nat)) if nat.exists() and not CAL else {}

    def _quadro(self, t):
        fps = config.frame_rate
        return max(1, round(t * fps)) / fps

    def play(self, *args, **kwargs):
        if args and not getattr(self, "_cru", False):
            anims = self.compile_animations(*args, **kwargs)
            self.ntime += max(a.run_time for a in anims)
            if abs(self.tscale - 1.0) > 1e-6:
                for a in anims:
                    a.run_time = self._quadro(a.run_time * self.tscale)
            return super().play(*anims)
        return super().play(*args, **kwargs)

    def esperar_cru(self, duracao):
        """Espera SEM escala: Scene.wait chama self.play, que escalaria de novo."""
        self._cru = True
        try:
            Scene.wait(self, duracao)
        finally:
            self._cru = False

    def wait(self, duration=1.0, *a, **k):
        self.ntime += duration
        self.esperar_cru(self._quadro(duration * self.tscale))

    def until(self, t):
        if os.environ.get("NOUNTIL") == "1":
            return
        d = t - self.ntime
        if d > 0.02:
            self.wait(d)

    def ancora(self, nome):
        agora = self.renderer.time
        if CAL:
            self.nativos[nome] = round(agora, 3)
            if nome == "fim":
                json.dump(self.nativos, open(PASTA / "native.json", "w"), indent=1)
            return
        if not self.anc or nome not in self.nat:
            return
        nomes = [n for n, _ in self.anc]
        i = nomes.index(nome)
        t_a = self.anc[i][1]
        if agora < t_a:
            self.esperar_cru(t_a - agora)
            agora = t_a
        elif agora - t_a > 0.25:
            print("SYNC atraso %.2f s em %s" % (agora - t_a, nome))
        self.ntime = self.nat[nome]
        if i + 1 < len(self.anc):
            prox, t_prox = self.anc[i + 1]
            gap_nat = max(0.2, self.nat[prox] - self.nat[nome])
            self.tscale = float(np.clip((t_prox - agora) / gap_nat * 0.985, 0.45, 2.0))
        else:
            self.tscale = 1.0

    def head(self, label):
        new = text(label, 24, opacity=0.75).move_to([0, 6.35, 0])
        if self.hl is None:
            self.play(FadeIn(new, shift=UP * 0.1), run_time=0.5)
        else:
            self.play(FadeOut(self.hl, shift=UP * 0.1), FadeIn(new, shift=UP * 0.1), run_time=0.5)
        self.hl = new

    def place(self, eq, x=0.0, y=0.0):
        fit(eq.mob).move_to([x, y, 0])
        return eq

    def show(self, eq, x=0.0, y=0.0, run_time=0.8, extra=()):
        self.place(eq, x, y)
        self.play(FadeIn(eq.mob, shift=UP * 0.1), *extra, run_time=run_time)
        self.cur = eq
        return eq

    def unbox(self):
        if self.box is not None:
            self.play(FadeOut(self.box), run_time=0.25)
            self.remove(self.box)
            self.box = None

    def mm(self, old, new, *moves, x=None, y=None, rt=1.2, hold=0.3, extra=(), box=False, anims=(), color=WHITE, track=True):
        """old (Eq) -> new (Eq) por TransformByGlyphMap; o que não for citado entra/sai por fade."""
        if track and old is self.cur:
            self.unbox()
        c = old.mob.get_center()
        self.place(new, c[0] if x is None else x, c[1] if y is None else y)
        self.play(TransformByGlyphMap(old.mob, new.mob, *moves, auto_fade=True), *extra, *anims, run_time=rt)
        self.remove(old.mob)
        if track:
            self.cur = new
        if box:
            self.box = boxed_rect(new.mob, color)
            self.play(FadeIn(self.box), run_time=0.3)
        if hold:
            self.wait(hold)
        return new

    def cancel(self, eq, *ids, rt=0.5):
        lines = strike(eq, *ids)
        self.play(*[Create(l) for l in lines], run_time=rt)
        return lines

    def construct(self):
        self.camera.background_color = BACKGROUND_COLOR
        self.hl, self.box, self.cur = None, None, None
        self.sync_init()
        wm = ImageMobject(str(WATERMARK_PATH)).set_width(1.8).set_opacity(0.35)
        self.add(wm.to_corner(UP + RIGHT, buff=0.28))
        series = text("POR TRÁS DA FÓRMULA · EP. 04", 20, opacity=0.65).to_corner(UP + LEFT, buff=0.4)
        self.add(series)
        self.ancora("b01")
        for k, seg in enumerate([self.s1, self.s2, self.s3, self.s4, self.s5, self.s6, self.s7, self.s8,
                                 self.s9, self.s10], 1):
            seg()
            if k >= ATE:
                self.wait(0.5)
                return

    # ── 0:00–0:15 Problema físico ───────────────────────────────────────────
    def s1(self):
        c = self.cyl = Cyl(-0.2, 0.5, 1.4, op=0.0)
        self.add(c.group)
        self.play(c.op.animate.set_value(1), run_time=1.0)
        labs = VGroup(
            text("paredes\nisolantes", 22, opacity=0.85).move_to([-3.4, 0.9, 0]),
            text("pistão\nsem atrito", 22, opacity=0.85).move_to([-3.4, 2.0, 0]),
            text("pesos\npequenos", 22, opacity=0.85).move_to([2.9, 2.6, 0]))
        leads = VGroup(
            Line([-2.7, 0.9, 0], [-2.3, 0.9, 0]), Line([-2.7, 2.0, 0], [-1.8, 1.9, 0]),
            Line([2.2, 2.7, 0], [0.7, 2.9, 0]))
        leads.set_stroke(WHITE, 1.5, 0.5)
        self.play(FadeIn(labs, lag_ratio=0.3), FadeIn(leads), run_time=1.2)
        self.until(5.4)
        self.play(FadeOut(labs), FadeOut(leads), run_time=0.5)
        self.until(6.04)
        self.ancora("b02")
        c.drive(3, 8.0 * self.tscale)
        self.dqE = Eq(r"\delta Q", "=", "0", size=80, colors={0: MAGENTA, 1: MAGENTA, 2: MAGENTA})
        self.dq_big = self.dqE.mob.move_to([0, -2.1, 0])
        self.until(8.6)
        self.play(FadeIn(self.dq_big, shift=UP * 0.15), run_time=0.8)
        self.until(10.47)
        self.ancora("b03")
        self.q1 = text("De onde vem a energia\npara empurrar o pistão?", 28).move_to([0, -3.6, 0])
        self.play(FadeIn(self.q1, shift=UP * 0.1), run_time=0.7)
        self.until(13.63)
        self.ancora("b04")

    # ── 0:15–0:35 Primeira Lei ──────────────────────────────────────────────
    def s2(self):
        c = self.cyl
        self.play(c.cx.animate.set_value(-0.5), c.cy.animate.set_value(2.9), c.sc.animate.set_value(0.8),
                  FadeOut(self.q1),
                  self.dq_big.animate.scale(0.38).move_to([-3.0, 4.9, 0]), run_time=1.2)
        self.dq = self.dq_big
        self.head("Primeira Lei")
        A0 = Eq("dU", "=", r"\delta Q", "-", r"\delta W", size=58, colors={0: CYAN, 2: MAGENTA, 4: VIOLET})
        dqc = Eq(r"\delta Q", "=", "0", size=80, colors={0: MAGENTA, 1: MAGENTA, 2: MAGENTA})
        dqc.mob.replace(self.dq)
        self.add(dqc.mob)
        self.mm(dqc, A0, M(dqc, [0], A0, [2], path_arc=-PI / 3), x=0.0, y=0.0, rt=1.1, hold=0.2, track=False)
        self.cur = A0
        self.until(20.47)
        self.ancora("b05")
        A2 = Eq("dU", "=", "-", r"\delta W", size=58, colors={0: CYAN, 3: VIOLET})
        self.mm(A0, A2, M(A0, [0, 1], A2, [0, 1]), X(A0, [2], shift=UP * 0.3 + LEFT * 0.4), M(A0, [3], A2, [2]),
                M(A0, [4], A2, [3]), rt=1.1, hold=0.2, extra=[Indicate(self.dq, color=MAGENTA, scale_factor=1.15)])
        self.until(24.93)
        self.ancora("b06")
        c.drive(6, 7.5 * self.tscale)
        self.note2 = text("expansão quase-estática,\nsem dissipação", 26).move_to([0, -2.1, 0])
        dWq = Eq(r"\delta W", "=", "P", "dV", size=44, colors={0: VIOLET, 2: VIOLET, 3: VIOLET})
        self.place(dWq, 0, -1.0)
        self.dW = dWq.mob
        rW = boxed_rect(VGroup(*A2.g(3)), VIOLET)
        self.play(FadeIn(self.dW, shift=UP * 0.1), FadeIn(self.note2, shift=UP * 0.1), Create(rW), run_time=0.8)
        self.wait(0.4)
        A3 = Eq("dU", "=", "-", "P", "dV", size=58, colors={0: CYAN, 3: VIOLET, 4: VIOLET})
        self.mm(A2, A3, M(A2, [0, 1, 2], A3, [0, 1, 2]), X(A2, [3]),
                CG(dWq.g(2, 3), A3.p(3, 4), path_arc=PI / 4), rt=1.3, hold=0.3, box=True, anims=[FadeOut(rW)])
        self.A3 = A3
        self.until(28.48)
        self.ancora("b07")
        # V↑ U↓ T↓
        c.thm.set_value(0.0)
        self.chips = VGroup(tex(r"V\uparrow", 40), tex(r"U\downarrow", 40, CYAN), tex(r"T\downarrow", 40, MAGENTA))
        for k, m in enumerate(self.chips):
            m.move_to([-3.2, 3.9 - 0.7 * k, 0])
        self.play(c.thm.animate.set_value(1.0), FadeIn(self.chips, lag_ratio=0.5), run_time=1.6)
        self.side = VGroup(self.dq, self.chips)
        self.until(34.03)
        self.ancora("b08")

    # ── 0:35–0:55 Energia interna e temperatura ─────────────────────────────
    def s3(self):
        c = self.cyl
        self.cyl.drive(7, 2.7 * self.tscale)
        self.head("Gás ideal: U depende só de T")
        self.unbox()
        self.play(FadeOut(self.dW), FadeOut(self.note2), c.op.animate.set_value(0.5),
                  self.side.animate.set_opacity(0.5), self.A3.mob.animate.move_to([0, -1.4, 0]), run_time=0.8)
        P3 = self.A3
        U1 = Eq("U", "=", "U(T)", size=50, colors={0: CYAN, 2: CYAN})
        self.place(U1, -0.5, 1.8)
        self.gi = text("(gás ideal)", 24, opacity=0.8).next_to(U1.mob, RIGHT, buff=0.3)
        self.play(FadeIn(U1.mob, shift=UP * 0.1), FadeIn(self.gi), run_time=0.8)
        self.until(38.24)
        self.ancora("b09")
        qd = text("Como U muda quando T muda?", 26).move_to([0, 0.95, 0])
        self.play(FadeIn(qd, shift=UP * 0.1), run_time=0.6)
        self.until(41.17)
        self.ancora("b10")
        D0 = Eq("C_V", "=", r"\frac{1}{n}", r"\left(\frac{\partial U}{\partial T}\right)_V", size=44, colors={0: CYAN})
        self.place(D0, 0, -0.1)
        tagd = VGroup(text("definição de", 24, CYAN), tex("C_V", 30, CYAN)).arrange(RIGHT, buff=0.15).move_to([0, 0.95, 0])
        self.play(soft_swap(qd, tagd), FadeIn(D0.mob, shift=UP * 0.1), run_time=0.9)
        self.cur = D0
        self.until(43.4)
        # D0 glifos: 0-1 C_V, 2 =, 3 '1', 4 barra, 5 n, 6 '(', 7 ∂, 8 U, 9 barra, 10 ∂, 11 T, 12 ')', 13 V
        D0b = Eq("C_V", "=", r"\frac{1}{n}", r"\frac{dU}{dT}", size=44, colors={0: CYAN})
        nb, bb, db = D0b.frac(3)
        self.mm(D0, D0b, M(D0, [0, 1, 2], D0b, [0, 1, 2]), MG([7, 8], nb), MG([9], [bb]), MG([10, 11], db),
                rt=1.3, hold=0.3, anims=[FadeOut(tagd), Indicate(U1.mob, color=CYAN, scale_factor=1.15)])
        self.ancora("b11")
        D1 = Eq("n", "C_V", "=", r"\frac{dU}{dT}", size=50, colors={0: CYAN, 1: CYAN})
        n1, b1, d1 = D1.frac(3)
        f_num, f_bar, f_den = D0b.frac(2)
        self.mm(D0b, D1, MG(D0b.p(0), D1.p(1)), MG(D0b.p(1), D1.p(2)), MG(f_den, D1.p(0), path_arc=PI / 3),
                MG(nb, n1), MG([bb], [b1]), MG(db, d1), rt=1.2, hold=0.2)
        N1 = Eq("dU", "=", "n", "C_V", "dT", size=50, colors={0: CYAN, 2: CYAN, 3: CYAN, 4: CYAN})
        self.mm(D1, N1, MG(n1, N1.p(0)), MG(d1, N1.p(4), path_arc=-PI / 2), MG([b1], []), M(D1, [2], N1, [1]),
                M(D1, [0], N1, [2]), M(D1, [1], N1, [3]), rt=1.3, hold=0.3)
        self.until(51.19)
        self.ancora("b12")
        B0 = Eq("n", "C_V", "dT", "=", "-", "P", "dV", size=52, colors={0: CYAN, 1: CYAN, 2: CYAN, 5: VIOLET, 6: VIOLET})
        self.cur = P3
        self.place(B0, 0, -1.4)
        self.play(TransformByGlyphMap(P3.mob, B0.mob, X(P3, [0]), M(P3, [1, 2, 3, 4], B0, [3, 4, 5, 6]),
                                      C(N1.g(2, 3, 4), B0, [0, 1, 2], delay=0.3), auto_fade=True),
                  FadeOut(N1.mob), run_time=1.5)
        self.remove(P3.mob)
        self.cur = B0
        self.B0 = B0
        self.box = boxed_rect(B0.mob)
        self.play(FadeIn(self.box), run_time=0.3)
        self.until(50.5)
        PV = Eq("P", "V", "=", "n", "R", "T", size=50)
        self.place(PV, 0, 1.1)
        self.play(FadeOut(U1.mob), FadeOut(self.gi), FadeIn(PV.mob, shift=UP * 0.1), run_time=0.8)
        self.PV = PV
        self.until(53.39)
        self.ancora("b13")

    # ── 0:55–1:08 Manipulação algébrica ─────────────────────────────────────
    def s4(self):
        c = self.cyl
        self.head("Ligando temperatura e volume")
        B0, PV = self.B0, self.PV
        G1 = Eq("n", "C_V", "dT", "=", "-", r"\frac{nRT}{V}", "dV", size=52,
                colors={0: CYAN, 1: CYAN, 2: CYAN, 5: VIOLET, 6: VIOLET})
        P2 = Eq("P", "=", r"\frac{nRT}{V}", size=50, colors={0: VIOLET})
        self.place(P2, 0, 1.1)
        pn_, pb_, pd_ = P2.frac(2)
        self.play(TransformByGlyphMap(PV.mob, P2.mob, M(PV, [0], P2, [0]), M(PV, [2], P2, [1]),
                                      MG(PV.p(3, 4, 5), pn_), MG(PV.p(1), pd_, path_arc=PI / 3), auto_fade=True),
                  run_time=1.2)
        self.remove(PV.mob)
        self.wait(0.2)
        self.place(G1, 0, -1.4)
        num, bar, den = G1.frac(5)
        self.cur = B0
        self.unbox()
        self.mm(B0, G1, M(B0, [0, 1, 2, 3, 4], G1, [0, 1, 2, 3, 4]), X(B0, [5], shift=UP * 0.3),
                M(B0, [6], G1, [6]),
                CG(P2.g(2), G1.p(5), path_arc=-PI / 4),
                rt=1.5, hold=0.2)
        # cancela n
        G2 = Eq("C_V", "dT", "=", "-", r"\frac{RT}{V}", "dV", size=52,
                colors={0: CYAN, 1: CYAN, 4: VIOLET, 5: VIOLET})
        n_l, n_r = G1.p(0), [num[0]]
        lines = VGroup(*[Line(self_g.get_corner(DL), self_g.get_corner(UR), color=MAGENTA, stroke_width=4)
                         for self_g in (G1.mob[0][n_l[0]], G1.mob[0][n_r[0]])])
        self.play(*[Create(l) for l in lines], run_time=0.5)
        num2, bar2, den2 = None, None, None
        self.place(G2, 0, -1.4)
        num2, bar2, den2 = G2.frac(4)
        self.play(TransformByGlyphMap(
            G1.mob, G2.mob, MG(n_l + n_r, []), M(G1, [1, 2, 3, 4], G2, [0, 1, 2, 3]),
            MG(num[1:], num2), MG([bar], [bar2]), MG(den, den2), M(G1, [6], G2, [5]), auto_fade=True),
            FadeOut(lines), run_time=1.2)
        self.remove(G1.mob)
        self.cur = G2
        self.wait(0.2)
        # T atravessa a igualdade
        G3 = Eq("C_V", r"\frac{dT}{T}", "=", "-", r"\frac{R}{V}", "dV", size=52,
                colors={0: CYAN, 1: CYAN, 4: VIOLET, 5: VIOLET})
        self.place(G3, 0, -1.4)
        n3, b3, d3 = G3.frac(1)
        r3, rb3, rd3 = G3.frac(4)
        self.play(TransformByGlyphMap(
            G2.mob, G3.mob, M(G2, [0], G3, [0]), MG(G2.p(1), n3),
            MG([num2[1]], d3, path_arc=-PI / 2), M(G2, [2, 3], G3, [2, 3]),
            MG([num2[0]], r3), MG([bar2], [rb3]), MG(den2, rd3), M(G2, [5], G3, [5]), auto_fade=True),
            run_time=1.5)
        self.remove(G2.mob)
        self.cur = G3
        self.wait(0.15)
        # dV sobe sobre o V
        G4 = Eq("C_V", r"\frac{dT}{T}", "=", "-", "R", r"\frac{dV}{V}", size=54,
                colors={0: CYAN, 1: CYAN, 4: VIOLET, 5: VIOLET})
        self.place(G4, 0, -1.4)
        n5, b5, d5 = G4.frac(5)
        self.play(TransformByGlyphMap(
            G3.mob, G4.mob, M(G3, [0, 1, 2, 3], G4, [0, 1, 2, 3]), MG(r3, G4.p(4)), MG(rd3, d5),
            MG(G3.p(5), n5, path_arc=PI / 3), auto_fade=True), run_time=1.5)
        self.remove(G3.mob)
        self.cur = G4
        self.G4 = G4
        self.box = boxed_rect(G4.mob)
        self.play(FadeIn(self.box), run_time=0.3)
        self.until(60.75)
        self.ancora("b15")
        self.wait(2.0)
        self.unbox()
        self.play(FadeOut(G4.mob), FadeOut(P2.mob), run_time=0.6)

    # ── 1:08–1:30 Mayer ─────────────────────────────────────────────────────
    def s5(self):
        main = self.cyl
        self.ancora("b16")
        self.head("Relação de Mayer")
        side = self.side
        A = self.A = Cyl(-2.2, 2.3, 0.78, mode="rigido", ins=0.0, thm=1.0, narr=2, op=0.0)
        B = self.B = Cyl(1.8, 2.3, 0.78, mode="livre", ins=0.0, thm=1.0, narr=3, op=0.0)
        self.add(A.group, B.group)
        hp, bop = ValueTracker(0.0), ValueTracker(1.0)
        BY, BH = 1.45, 0.24

        def bars():
            h, o = hp.get_value(), bop.get_value()
            out = []
            for x0, w, col in ((-3.2, 1.2 * h, CYAN), (0.85, 1.2 * h, CYAN), (0.85 + 1.2 * h, 0.5 * h, VIOLET)):
                if w > 0.02:
                    out.append(Rectangle(width=w, height=BH, stroke_width=0, fill_color=col,
                                         fill_opacity=0.9 * o).move_to([x0 + w / 2, BY, 0]))
            return VGroup(*out)
        bars_m = always_redraw(bars)
        self.add(hp, bop, bars_m)
        self.play(main.op.animate.set_value(0), A.op.animate.set_value(1), B.op.animate.set_value(1),
                  FadeOut(side), run_time=1.2)
        capA = VGroup(text("Volume constante", 26), tex(r"dV = 0", 40)).arrange(DOWN, buff=0.15).move_to([-2.2, 5.2, 0])
        capB = text("Pressão constante", 26).move_to([2.2, 5.3, 0])
        self.play(FadeIn(capA), FadeIn(capB), run_time=0.7)
        self.until(66.91)
        self.ancora("b17")
        # a mesma energia entra nos dois lados: mesma subida de T; só o lado B também empurra o pistão
        self.play(A.heat.animate.set_value(1), B.heat.animate.set_value(1), run_time=0.4)
        self.play(A.tf.animate.set_value(1.45), B.tf.animate.set_value(1.45), B.vf.animate.set_value(1.45),
                  hp.animate.set_value(1.0), run_time=3.2, rate_func=smooth)
        self.ancora("b18")
        lA = tex(r"\Delta U", 34, CYAN).move_to([-2.6, 1.05, 0])
        lB = tex(r"\Delta U", 34, CYAN).move_to([1.45, 1.05, 0])
        lW = tex("W", 34, VIOLET).move_to([2.3, 1.05, 0])
        labs = VGroup(lA, lB, lW)
        AQ = Eq(r"\delta Q_V", "=", "n", "C_V", "dT", size=40, colors={0: MAGENTA, 2: CYAN, 3: CYAN, 4: CYAN})
        self.place(AQ, -2.2, 0.35)
        BQ = Eq(r"\delta Q_P", "=", "n", "C_P", "dT", size=40, colors={0: MAGENTA, 2: CYAN, 3: CYAN, 4: CYAN})
        self.place(BQ, 2.2, 0.35)
        bA, bB = boxed_rect(AQ.mob), boxed_rect(BQ.mob)
        self.play(FadeIn(labs), FadeIn(AQ.mob, shift=UP * 0.1), FadeIn(BQ.mob, shift=UP * 0.1), FadeIn(bA), FadeIn(bB),
                  A.heat.animate.set_value(0), B.heat.animate.set_value(0), run_time=0.8)
        # a matemática assume: o sistema recua
        self.play(A.op.animate.set_value(0.4), B.op.animate.set_value(0.4), bop.animate.set_value(0.5),
                  labs.animate.set_opacity(0.5), run_time=0.5)
        yk = -1.0
        K0 = Eq(r"\delta Q_P", "=", "dU", "+", "P", "dV", size=48, colors={0: MAGENTA, 2: CYAN, 4: VIOLET, 5: VIOLET})
        self.show(K0, y=yk, run_time=0.9)
        K1 = Eq(r"\delta Q_P", "=", "n", "C_V", "dT", "+", "P", "dV", size=48,
                colors={0: MAGENTA, 2: CYAN, 3: CYAN, 4: CYAN, 6: VIOLET, 7: VIOLET})
        self.mm(K0, K1, M(K0, [0, 1], K1, [0, 1]), X(K0, [2]), CG(AQ.g(2, 3, 4), K1.p(2, 3, 4), path_arc=-PI / 4),
                M(K0, [3, 4, 5], K1, [5, 6, 7]), rt=1.2, hold=0.1)
        K2 = Eq("n", "C_P", "dT", "=", "n", "C_V", "dT", "+", "P", "dV", size=46,
                colors={0: CYAN, 1: CYAN, 2: CYAN, 4: CYAN, 5: CYAN, 6: CYAN, 8: VIOLET, 9: VIOLET})
        self.mm(K1, K2, X(K1, [0], shift=UP * 0.3), M(K1, [1], K2, [3]), M(K1, [2, 3, 4, 5, 6, 7], K2, [4, 5, 6, 7, 8, 9]),
                C(BQ.g(2, 3, 4), K2, [0, 1, 2], path_arc=PI / 4), rt=1.4, hold=0.1)
        # P constante: PV = nRT dá P dV = nR dT, e o P dV da cadeia é substituído por nR dT
        Z0 = Eq("P", "V", "=", "n", "R", "T", size=48)
        self.place(Z0, 0, -2.5)
        rP = boxed_rect(VGroup(*K2.g(8, 9)), VIOLET)
        self.play(FadeIn(Z0.mob, shift=UP * 0.1), Create(rP), run_time=0.8)
        Z1 = Eq("P", "dV", "=", "n", "R", "dT", size=48, colors={0: VIOLET, 1: VIOLET, 3: VIOLET, 4: VIOLET, 5: VIOLET})
        self.mm(Z0, Z1, M(Z0, [0], Z1, [0]), MG(Z0.p(1), Z1.p(1)), M(Z0, [2, 3, 4], Z1, [2, 3, 4]),
                MG(Z0.p(5), Z1.p(5)), x=0.0, y=-2.5, rt=1.2, hold=0.2, track=False)
        K3 = Eq("n", "C_P", "dT", "=", "n", "C_V", "dT", "+", "n", "R", "dT", size=46,
                colors={0: CYAN, 1: CYAN, 2: CYAN, 4: CYAN, 5: CYAN, 6: CYAN, 8: VIOLET, 9: VIOLET, 10: VIOLET})
        self.mm(K2, K3, M(K2, range(8), K3, range(8)), X(K2, [8, 9]), CG(Z1.g(3, 4, 5), K3.p(8, 9, 10), path_arc=PI / 4),
                rt=1.3, hold=0.1, anims=[FadeOut(rP), FadeOut(Z1.mob)])
        self.ancora("b19")
        lines = self.cancel(K3, 0, 2, 4, 6, 8, 10, rt=0.5)
        K4 = Eq("C_P", "=", "C_V", "+", "R", size=56, colors={0: CYAN, 2: CYAN, 4: VIOLET})
        self.place(K4, 0, yk)
        self.play(TransformByGlyphMap(K3.mob, K4.mob, M(K3, [1], K4, [0]), M(K3, [3], K4, [1]),
                                      M(K3, [5], K4, [2]), M(K3, [7], K4, [3]), M(K3, [9], K4, [4]),
                                      X(K3, [0, 2, 4, 6, 8, 10]), auto_fade=True),
                  FadeOut(lines), run_time=1.1)
        self.remove(K3.mob)
        self.cur = K4
        K5 = Eq("C_P", "-", "C_V", "=", "R", size=72, colors={0: CYAN, 2: CYAN, 4: VIOLET})
        self.mm(K4, K5, M(K4, [0], K5, [0]), M(K4, [1], K5, [3]), M(K4, [2], K5, [2], path_arc=PI / 2),
                M(K4, [3], K5, [1]), M(K4, [4], K5, [4]), rt=1.2, hold=1.2, box=True, color=CYAN)
        self.K5 = K5
        self.mayer_txt = VGroup(capA, capB, AQ.mob, bA, BQ.mob, bB, labs, bars_m)

    # ── 1:30–1:40 gama ──────────────────────────────────────────────────────
    def s6(self):
        main, A, B = self.cyl, self.A, self.B
        self.ancora("b20")
        self.head("Razão entre calores específicos")
        K5 = self.K5
        k5g = self.k5g = VGroup(K5.mob, self.box)
        self.box = None
        Gm = Eq(r"\gamma", "=", r"\frac{C_P}{C_V}", size=42, colors={0: BLUE_L, 2: CYAN})
        self.place(Gm, 2.1, 1.3)
        self.Gm = Gm
        self.play(A.op.animate.set_value(0), B.op.animate.set_value(0), main.op.animate.set_value(0.35),
                  FadeOut(self.mayer_txt), FadeIn(self.side), FadeIn(Gm.mob, shift=UP * 0.1),
                  k5g.animate.scale(0.62).move_to([-1.9, 1.3, 0]), run_time=1.2)
        Gm2 = Eq(r"\gamma", "=", r"\frac{C_P}{C_V}", size=42, colors={0: BLUE_L, 2: CYAN})
        self.place(Gm2, 2.1, 1.3)
        self.add(Gm2.mob)
        self.cur = Gm2
        L0 = Eq(r"\gamma", "-", "1", "=", r"\frac{C_P}{C_V}", "-", "1", size=52, colors={0: BLUE_L, 4: CYAN})
        self.until(87.3)
        self.mm(Gm2, L0, M(Gm2, [0], L0, [0]), M(Gm2, [1], L0, [3]), M(Gm2, [2], L0, [4]), x=0.0, y=-1.2,
                rt=1.3, hold=0.3)
        self.ancora("b21")
        L1 = Eq(r"\gamma", "-", "1", "=", r"\frac{C_P-C_V}{C_V}", size=54, colors={0: BLUE_L, 4: CYAN})
        n0, b0, d0 = L0.frac(4)
        n1, b1, d1 = L1.frac(4)
        self.mm(L0, L1, M(L0, [0, 1, 2, 3], L1, [0, 1, 2, 3]), MG(n0, n1[:2]), MG([b0], [b1]), MG(d0, d1),
                MG(L0.p(5), [n1[2]]), MG(L0.p(6), n1[3:]), rt=1.5, hold=0.5)
        L2 = Eq(r"\gamma", "-", "1", "=", r"\frac{R}{C_V}", size=56, colors={0: BLUE_L, 4: VIOLET})
        n2, b2, d2 = L2.frac(4)
        self.mm(L1, L2, M(L1, [0, 1, 2, 3], L2, [0, 1, 2, 3]), MG(n1, []), CG(K5.g(4), n2, path_arc=PI / 4),
                MG([b1], [b2]), MG(d1, d2), rt=1.6, hold=0.2, box=True, color=BLUE_L,
                anims=[Indicate(k5g, color=CYAN, scale_factor=1.08)])
        H3 = L2
        self.H3 = H3
        self.until(96.07)
        self.ancora("b22")

    # ── 1:40–2:05 Integração ────────────────────────────────────────────────
    def s7(self):
        c = self.cyl
        self.head("Integração")
        c.drive(8, 2.7 * self.tscale)
        H3, G4 = self.H3, self.G4
        self.unbox()
        G4.mob.move_to([0, -1.2, 0])
        self.play(H3.mob.animate.scale(0.8).move_to([0, 1.1, 0]), FadeOut(self.Gm.mob), FadeOut(self.k5g),
                  FadeIn(G4.mob, shift=UP * 0.1), run_time=0.9)
        I0 = G4
        self.cur = I0
        I1 = Eq(r"\frac{dT}{T}", "=", "-", r"\frac{R}{C_V}", r"\frac{dV}{V}", size=54,
                colors={0: CYAN, 3: VIOLET, 4: VIOLET})
        self.place(I1, 0, -1.2)
        a0, ab0, ad0 = I0.frac(1)
        t0, tb0, td0 = I1.frac(0)
        r1, rb1, rd1 = I1.frac(3)
        v0, vb0, vd0 = I0.frac(5)
        v1, vb1, vd1 = I1.frac(4)
        self.until(96.9)
        self.mm(I0, I1, MG(a0 + [ab0] + ad0, t0 + [tb0] + td0), M(I0, [2, 3], I1, [1, 2]),
                MG(I0.p(0), rd1, path_arc=-PI / 2), MG(I0.p(4), r1), MG(v0 + [vb0] + vd0, v1 + [vb1] + vd1),
                rt=1.4, hold=0.2)
        I2 = Eq(r"\frac{dT}{T}", "=", "-", r"(\gamma-1)", r"\frac{dV}{V}", size=54,
                colors={0: CYAN, 3: BLUE_L, 4: VIOLET})
        t2, tb2, td2 = I2.frac(0)
        v2, vb2, vd2 = I2.frac(4)
        Hg = H3.mob[0][H3.p(0)[0]:H3.p(2)[-1] + 1]
        self.mm(I1, I2, MG(t0 + [tb0] + td0, t2 + [tb2] + td2), M(I1, [1, 2], I2, [1, 2]),
                X(I1, [3], shift=DOWN * 0.3), CG(list(Hg), I2.p(3), path_arc=-PI / 3),
                MG(v1 + [vb1] + vd1, v2 + [vb2] + vd2), rt=1.5, hold=0.3)
        self.until(100.07)
        self.ancora("b23")
        hyp = VGroup(tex(r"\gamma \approx", 40, BLUE_L), text("constante no intervalo", 28)).arrange(RIGHT, buff=0.15)
        hyp_b = VGroup(hyp, boxed_rect(hyp, BLUE_L)).move_to([0, -2.9, 0])
        self.play(FadeIn(hyp_b, shift=UP * 0.1), run_time=0.8)
        self.hyp = hyp_b
        self.until(104.2)
        self.ancora("b24")
        I3 = Eq(r"\int", r"\frac{dT}{T}", "=", "-", r"(\gamma-1)", r"\int", r"\frac{dV}{V}", size=54,
                colors={0: CYAN, 1: CYAN, 4: BLUE_L, 5: VIOLET, 6: VIOLET})
        self.place(I3, 0, -1.2)
        t3, tb3, td3 = I3.frac(1)
        v3, vb3, vd3 = I3.frac(6)
        self.mm(I2, I3, MG(t2 + [tb2] + td2, t3 + [tb3] + td3), M(I2, [1, 2, 3], I3, [2, 3, 4]),
                MG(v2 + [vb2] + vd2, v3 + [vb3] + vd3), rt=1.4, hold=0.4)
        self.until(105.85)
        self.ancora("b25")
        I4 = Eq(r"\ln T", "+", r"(\gamma-1)", r"\ln V", "=", "C", size=56,
                colors={0: CYAN, 2: BLUE_L, 3: VIOLET, 5: WHITE})
        self.place(I4, 0, -1.2)
        self.mm(I3, I4,
                MG(I3.p(1) + I3.p(0), I4.p(0)), M(I3, [3], I4, [1], path_arc=PI / 3),
                M(I3, [4], I4, [2], path_arc=-PI / 2), M(I3, [5, 6], I4, [3]), M(I3, [2], I4, [4]),
                rt=1.6, hold=0.4)
        ctag = text("C: constante de integração", 28, opacity=0.95).move_to([0, -2.05, 0])
        self.play(FadeIn(ctag, shift=UP * 0.1), run_time=0.5)
        self.until(108.6)
        I5 = Eq(r"\ln", "(", "T", r"V^{\gamma-1}", ")", "=", "C", size=56,
                colors={0: CYAN, 2: CYAN, 3: VIOLET, 6: WHITE})
        self.place(I5, 0, -1.2)
        ln1, T1 = I4.px(0)[:2], I4.px(0)[2]
        g_ = I4.px(2)
        lnV = I4.px(3)
        sup = I5.px(3)
        self.mm(I4, I5,
                MG(ln1, I5.p(0)), MG([T1], I5.p(2)), MG([g_[1], g_[2], g_[3]], sup[1:], path_arc=-PI / 3),
                MG([lnV[2]], [sup[0]]), X(I4, [1]), MG([g_[0], g_[4]], []), MG(lnV[:2], []),
                M(I4, [4], I5, [5]), M(I4, [5], I5, [6]), rt=1.6, hold=0.4)
        self.play(FadeOut(ctag), run_time=0.3)
        I6 = Eq("T", r"V^{\gamma-1}", "=", r"\text{cte}", size=62, colors={0: CYAN, 1: VIOLET, 3: WHITE})
        self.mm(I5, I6, M(I5, [2], I6, [0]), M(I5, [3], I6, [1]), M(I5, [5], I6, [2]), M(I5, [6], I6, [3]),
                X(I5, [0, 1, 4]), rt=1.4, hold=0.3, box=True, color=CYAN)
        self.I6 = I6
        self.until(111.32)
        self.ancora("b26")
        tail = VGroup(tex(r"V\uparrow", 40), tex(r"\Rightarrow", 40), tex(r"T\downarrow", 40, MAGENTA)).arrange(RIGHT, buff=0.3)
        tail.move_to([0, -3.2, 0])
        self.play(FadeOut(self.hyp), FadeIn(tail, shift=UP * 0.1), run_time=0.7)
        self.tail = tail
        self.until(116.36)
        self.ancora("b27")

    # ── 2:05–2:20 Resultado final ───────────────────────────────────────────
    def s8(self):
        c = self.cyl
        self.head("Eliminando T com o gás ideal")
        I6, H3 = self.I6, self.H3
        self.play(FadeOut(self.tail), FadeOut(H3.mob), run_time=0.5)
        Ta = Eq("T", "=", r"\frac{PV}{nR}", size=50, colors={0: CYAN})
        self.show(Ta, y=1.1, run_time=0.7)
        self.unbox()
        J1 = Eq(r"\frac{PV}{nR}", r"V^{\gamma-1}", "=", r"\text{cte}", size=58, colors={1: VIOLET})
        self.place(J1, 0, -1.2)
        n1, b1, d1 = J1.frac(0)
        self.cur = I6
        self.until(117.5)
        rT = boxed_rect(VGroup(*I6.g(0)), CYAN)
        self.play(Create(rT), run_time=0.4)
        self.mm(I6, J1, CG(Ta.g(2), J1.p(0), path_arc=-PI / 4), X(I6, [0], shift=UP * 0.2),
                M(I6, [1, 2, 3], J1, [1, 2, 3]), rt=1.6, hold=0.1, anims=[FadeOut(rT)])
        J2 = Eq(r"\frac{PV\,V^{\gamma-1}}{nR}", "=", r"\text{cte}", size=58)
        self.place(J2, 0, -1.2)
        num2, bar2, den2 = J2.frac(0)
        # J2: numerador P V V γ - 1 ; denominador n R
        self.mm(J1, J2, MG(n1 + [b1] + d1, num2[:2] + [bar2] + den2), MG(J1.p(1), num2[2:], path_arc=PI / 4),
                M(J1, [2, 3], J2, [1, 2]), rt=1.3, hold=0.1)
        J3 = Eq(r"\frac{PV^{\gamma}}{nR}", "=", r"\text{cte}", size=58)
        self.place(J3, 0, -1.2)
        num3, bar3, den3 = J3.frac(0)
        self.mm(J2, J3, MG(num2[:2], num3[:2]), MG([num2[2]], []), MG([num2[3]], [num3[2]]),
                MG(num2[4:], []), MG([bar2], [bar3]), MG(den2, den3), M(J2, [1, 2], J3, [1, 2]),
                rt=1.3, hold=0.1)
        J3b = Eq("P", r"V^{\gamma}", "=", "n", r"R\;", r"\text{cte}", size=62, colors={0: CYAN, 1: CYAN})
        self.place(J3b, 0, -1.2)
        self.mm(J3, J3b, MG(num3[:1], J3b.p(0)), MG(num3[1:], J3b.p(1)), MG([bar3], []),
                MG(den3, J3b.p(3, 4), path_arc=-PI / 3), M(J3, [1], J3b, [2]), M(J3, [2], J3b, [5]),
                rt=1.3, hold=0.1)
        rn = boxed_rect(VGroup(*J3b.g(3, 4)), WHITE)
        self.play(Create(rn), run_time=0.4)
        J3c = Eq("P", r"V^{\gamma}", "=", r"\text{cte}'", size=62, colors={0: CYAN, 1: CYAN})
        self.mm(J3b, J3c, M(J3b, [0, 1, 2], J3c, [0, 1, 2]), MG(J3b.p(3, 4, 5), J3c.p(3)), rt=1.2, hold=0.1,
                anims=[FadeOut(rn)])
        J4 = Eq("P", r"V^{\gamma}", "=", r"\text{cte}", size=66, colors={0: CYAN, 1: CYAN})
        self.mm(J3c, J4, M(J3c, [0, 1, 2, 3], J4, [0, 1, 2, 3]), rt=0.9, hold=0.2, box=True, color=CYAN)
        self.J4 = J4
        self.until(124.33)
        self.ancora("b29")
        # payoff: espaço visual
        self.play(FadeOut(Ta.mob), FadeOut(self.chips), FadeOut(self.dq), run_time=0.6)
        grp = VGroup(J4.mob, self.box)
        self.play(grp.animate.scale(1.35).move_to([0, -0.4, 0]), run_time=0.8)
        self.wait(2.8)
        self.ancora("b30")

    # ── 2:20–2:40 Adiabática × isotérmica ───────────────────────────────────
    def s9(self):
        main = self.cyl
        self.head("Isotérmica × adiabática")
        grp = VGroup(self.J4.mob, self.box)
        self.play(grp.animate.scale(0.6).move_to([0, -3.7, 0]), main.op.animate.set_value(0), run_time=0.9)
        main.prog.clear_updaters()
        main.prog.set_value(0.0)
        main.g.set_value(GAMMA)
        # gêmeos
        iso = self.iso = Cyl(-2.2, 3.0, 0.5, g=1.0, ins=0.0, thm=1.0, narr=3, op=0.0, seed=1,
                       pb=1.0 / VF, dp=(1.0 - 1.0 / VF) / 8)
        ad = self.ad = main
        ad.cx.set_value(1.0)
        ad.cy.set_value(3.0)
        ad.sc.set_value(0.5)
        ad.thm.set_value(1.0)
        self.add(iso.group)
        ax = self.ax = Axes(x_range=[0.5, 2.4, 1], y_range=[0.25, 1.25, 1], x_length=5.5, y_length=3.9, tips=True,
                            axis_config={"include_ticks": False, "stroke_width": 2.5, "stroke_opacity": 0.85,
                                         "color": WHITE})
        ax.shift(np.array([-2.7, -2.0, 0]) - ax.c2p(0.5, 0.25))
        labV = tex("V", 38).next_to(ax.x_axis.get_end(), DOWN, buff=0.15)
        labP = tex("P", 38).next_to(ax.y_axis.get_end(), LEFT, buff=0.15)
        p0 = Dot(ax.c2p(1, 1), radius=0.08, color=WHITE)
        l0 = tex(r"(V_0,P_0)", 32).next_to(p0, UR, buff=0.08)
        capI = text("isotérmica", 24, MAGENTA).move_to([-2.2, 5.3, 0])
        capA = text("adiabática", 24, CYAN).move_to([1.0, 5.3, 0])
        tagI = tex(r"\delta Q>0 \quad T=\text{cte}", 28, MAGENTA).move_to([-1.6, 2.3, 0])
        tagA = tex(r"\delta Q=0 \quad T\downarrow", 28, CYAN).move_to([1.4, 2.3, 0])
        vl = DashedLine(ax.c2p(VF, 0.25), ax.c2p(VF, 1.05), color=WHITE, stroke_width=2).set_opacity(0.55)
        lvf = tex(r"V_f", 34).next_to(ax.c2p(VF, 0.25), DOWN, buff=0.12)
        self.play(Create(ax), FadeIn(labV), FadeIn(labP), iso.op.animate.set_value(1), main.op.animate.set_value(1),
                  FadeIn(capI), FadeIn(capA), run_time=1.5)
        self.play(FadeIn(p0, scale=1.5), FadeIn(l0), FadeIn(tagI), FadeIn(tagA), run_time=0.8)
        self.until(131.5)

        def trail(cyl, color):
            return always_redraw(lambda: ParametricFunction(
                lambda s: ax.c2p(s, s ** (-cyl.g.get_value())), t_range=[1.0, max(cyl.v(), 1.004)],
                color=color, stroke_width=5))

        def tip(cyl, color):
            return always_redraw(lambda: Dot(ax.c2p(cyl.v(), cyl.p()), radius=0.09, color=color))
        tI, dI = trail(iso, MAGENTA), tip(iso, MAGENTA)
        tA, dA = trail(ad, CYAN), tip(ad, CYAN)
        self.add(tI, dI, tA, dA)
        # os dois pistões sobem juntos até V_f; os pontos percorrem as curvas em tempo real
        self.play(iso.heat.animate.set_value(1.0), run_time=0.5)
        iso.drive(8, 9.0 * self.tscale)
        ad.drive(8, 9.0 * self.tscale)
        self.until(134.0)
        eI = tex(r"PV = \text{cte}", 36, MAGENTA).move_to(ax.c2p(1.7, 0.84))
        self.play(FadeIn(eI), run_time=0.5)
        self.until(135.51)
        self.ancora("b31")
        eA = tex(r"PV^{\gamma} = \text{cte}", 36, CYAN).move_to(ax.c2p(1.3, 0.45))
        self.play(FadeIn(eA), run_time=0.5)
        self.until(142.44)
        self.ancora("b32")
        self.play(iso.heat.animate.set_value(0.0), run_time=0.4)
        v1 = VF
        pi_, pa_ = v1 ** (-1.0), v1 ** (-GAMMA)
        dpi, dpa = Dot(ax.c2p(v1, pi_), 0.08, color=MAGENTA), Dot(ax.c2p(v1, pa_), 0.08, color=CYAN)
        lpi = tex(r"P_{\rm iso}", 34, MAGENTA).next_to(dpi, UR, buff=0.08)
        lpa = tex(r"P_{\rm ad}", 34, CYAN).next_to(dpa, RIGHT, buff=0.12)
        ct = tex(r"P_{\rm ad} < P_{\rm iso} \quad (\text{mesmo } V_f)", 40)
        cmp_ = VGroup(ct, boxed_rect(ct, WHITE)).move_to([0, -2.85, 0])
        self.play(Create(vl), FadeIn(lvf), run_time=0.7)
        self.play(FadeIn(dpi), FadeIn(dpa), FadeIn(lpi), FadeIn(lpa), run_time=0.6)
        self.play(FadeIn(cmp_, shift=UP * 0.1), run_time=0.7)
        self.s9_objs = (tI, dI, eI, vl, dpi, dpa, lpi, lpa, cmp_, labV, labP, p0, l0, capI, capA, tagI, lvf)
        self.until(146.0)
        self.ancora("b33")

    # ── 2:40–2:50 Fechamento ────────────────────────────────────────────────
    def s10(self):
        iso, ad = self.iso, self.ad
        tI, dI, eI, vl, dpi, dpa, lpi, lpa, cmp_, labV, labP, p0, l0, capI, capA, tagI, lvf = self.s9_objs
        tI.clear_updaters()
        self.play(FadeOut(VGroup(vl, dpi, dpa, lpi, lpa, cmp_, eI, tagI, lvf)), iso.op.animate.set_value(0), FadeOut(capI),
                  FadeOut(dI), FadeOut(tI), FadeOut(self.hl), FadeOut(self.box), run_time=1.0)
        self.play(ad.cx.animate.set_value(0.2), ad.cy.animate.set_value(3.3), ad.sc.animate.set_value(0.6),
                  capA.animate.move_to([0.2, 5.7, 0]), self.J4.mob.animate.move_to([0, -3.3, 0]), run_time=1.5)
        final = tex(r"PV^{\gamma} = \text{constante}", 64)
        fit(final, 6.0).move_to([0, -3.3, 0])
        self.play(ReplacementTransform(self.J4.mob, final), run_time=0.9)
        fb = boxed_rect(final, CYAN)
        self.play(FadeIn(fb), run_time=0.3)
        hyp = VGroup(text("gás ideal · adiabático reversível · ", 24, opacity=0.9), tex(r"\gamma", 32),
                     text(" aproximadamente constante", 24, opacity=0.9))
        hyp.arrange(RIGHT, buff=0.06)
        fit(hyp).move_to([0, -4.0, 0])
        self.ancora("b34")
        self.play(FadeIn(hyp, shift=UP * 0.1), run_time=0.8)
        self.wait(4.6)
        self.ancora("b35")
        cta = text("Siga o Parallax Lab  ·  @labparallax", 26)
        cta.move_to([0, -4.0, 0])
        self.play(soft_swap(hyp, cta, UP * 0.1, lag=0.6), run_time=1.0)
        self.wait(1.0)
        self.ancora("fim")

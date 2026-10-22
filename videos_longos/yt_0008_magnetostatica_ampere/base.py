"""Núcleo da cena (copiado do yt_0006 e estendido no 5.3): projeção 2.5D, relógio da corrente, slots de equação,
legendas e utilitários. Extensões locais: layout "app", src com vários tokens, laços/discos/anéis 3D."""
import json
import math
import os
import re
import unicodedata
import sys
from pathlib import Path

import numpy as np
from manim import (
    Scene, VGroup, VMobject, ValueTracker, ImageMobject, MathTex, DecimalNumber, Line, DashedLine, Arc, Circle, Dot,
    Polygon, Ellipse, ParametricFunction, FadeIn, FadeOut, Create, ReplacementTransform, Transform, TransformFromCopy,
    Write, Indicate, LaggedStart, AnimationGroup, UP, DOWN, LEFT, RIGHT, UL, UR, BOLD, always_redraw, linear, smooth,
    there_and_back, config, CapStyleType, Wait,
)
from manim.animation.animation import prepare_animation

ROOT = Path(__file__).resolve().parents[2]
UNIT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(UNIT))
from template.config_horizontal import BACKGROUND_COLOR, WATERMARK_PATH  # noqa: E402
from template.fonts import official_text, DISPLAY_FONT  # noqa: E402
from kit import *  # noqa: E402,F401,F403
from kit import _EC  # noqa: E402,F401

SEG = os.environ.get("SEG", "")
# sincronismo com a voz (sync_voz.py → sync_eventos.json); SEM_SYNC=1 desliga e volta ao ritmo livre do preview
SYNC = None if os.environ.get("SEM_SYNC") or not (UNIT / "sync_eventos.json").exists() else json.loads(
    (UNIT / "sync_eventos.json").read_text(encoding="utf-8"))
_semac = lambda t: "".join(c for c in unicodedata.normalize("NFD", t.lower()) if unicodedata.category(c) != "Mn")
PAL = json.loads((UNIT / "sync.json").read_text(encoding="utf-8"))["words"] if SYNC else []   # [palavra, início, fim] da voz
_TXT, _POS = "", []
for _i, _w in enumerate(PAL):
    _POS.append(len(_TXT))
    _TXT += re.sub(r"[^\w]", "", _semac(_w[0])) + " "
# símbolo (substring do token LaTeX) → como a voz o diz; usado para destacar o termo no instante em que é falado
FALADO = [(r"\mu_0", r"mi zero|permeabilidade"), (r"\rm env", r"corrente envolvida"), (r"\oint", r"circulacao"),
          (r"\nabla\times", r"rotacional"), (r"\nabla\cdot", r"divergente"), (r"\delta", r"delta"), (r"\mathbf F", r"fator geometrico|efe"),
          (r"d\tau", r"elemento de volume"), (r"\int", r"integral"), (r"4\pi", r"quatro pi"), (r"nL", r"ene vezes ele"),
          (r"\mathbf J", r"densidade de corrente|jota"), (r"\mathbf B", r"campo magnetico"), (r"\mathbf R", r"vetor separacao|erre maiusculo")]
EV_OFF = 0      # eventos novos antes do 1º evento do log V6 (secao abertura, 3 legendas/eq da abertura, marca n00)
WM_W, WM_OP = 1.92, 0.45
LW_VEC, LW_WIRE = 5, 6
HERO = np.array([3.95, 1.25, 0.0])
AUX = np.array([3.95, -1.45, 0.0])
CARD_W = 6.7
# (centro, largura, altura) de cada cartão por layout: split = padrão; geo = geometria dominante; alg = álgebra dominante
LAYOUTS = {
    "split": {"H": ((3.95, 1.25), 6.7, 2.5), "A": ((3.95, -1.45), 6.7, 2.45)},
    "geo": {"H": ((5.15, 1.95), 4.4, 1.6), "A": ((5.15, -0.1), 4.4, 1.8)},
    "alg": {"H": ((3.05, 1.5), 8.1, 2.4), "A": ((3.05, -1.3), 8.1, 2.3)},
    "app": {"H": ((3.95, 0.95), 6.7, 2.2), "A": ((3.95, -1.6), 6.7, 2.2)},     # aplicações: barra da estratégia no alto
}


class Base(Scene):
    def setup(self):
        self.camera.background_color = BACKGROUND_COLOR
        config.max_files_cached = 1000
        config.disable_caching = True
        self.ox, self.oy, self.gs = ValueTracker(-3.9), ValueTracker(-0.4), ValueTracker(1.1)
        self.beta, self.tau = ValueTracker(0), ValueTracker(0)
        self.checkpoints, self.sections, self.layout_issues = [], [], []
        self.eventos, self.estado_secoes, self.atrasos = [], {}, []
        self._ev, self._t0 = int(os.environ.get("EV0", 0)), float(os.environ.get("T0", 0))
        self._raw = False
        self._win = json.loads(os.environ["WIN0"]) if os.environ.get("WIN0") else None      # janela de sincronismo em curso: [natural, fim, consumido]
        self.head = self.cap = None
        self.slots = {"H": {"pos": HERO, "eq": None, "card": None, "w": 6.7, "h": 2.5},
                      "A": {"pos": AUX, "eq": None, "card": None, "w": 6.7, "h": 2.45}}
        self.layout_name = "split"
        self.clock = ValueTracker(0)
        self.clock.add_updater(lambda m, dt: m.increment_value(dt * 0.18))
        self.add(self.clock)

    # ── projeção 2.5D (a mesma do 5.1: cena inclinada em τ, girada em β em torno de y) ───────────────────────
    def W(self, p):
        b, t = np.deg2rad([self.beta.get_value(), self.tau.get_value()])
        x, y, z = np.asarray(p, dtype=float)
        xp, zp = x * math.cos(b) + z * math.sin(b), -x * math.sin(b) + z * math.cos(b)
        return np.array([self.ox.get_value(), self.oy.get_value(), 0]) + self.gs.get_value() * np.array(
            [xp, y * math.cos(t) + zp * math.sin(t), 0])

    def depth(self, p):
        b, t = np.deg2rad([self.beta.get_value(), self.tau.get_value()])
        x, y, z = p
        return (-x * math.sin(b) + z * math.cos(b)) * math.cos(t) - y * math.sin(t)

    def vec(self, a, v, color=WHITE, scale=1, width=LW_VEC, tip=0.26):
        return arrow(self.W(a), self.W(np.asarray(a, dtype=float) + scale * np.asarray(v, dtype=float)), color, width,
                     z=4 + self.depth(a), tip=tip)

    def lab(self, tex, point, *iso, size=M_S, color=None, colors=None, dx=0.0, dy=0.0):
        """Rótulo de diagrama (MathTex com tokens e halo), em coordenadas de TELA."""
        m = E(tex, *iso, size=size, colors=colors)
        if color:
            m.set_color(color)
        return halo(m.move_to(np.asarray(point, dtype=float) + np.array([dx, dy, 0]))).set_z_index(12)

    def tube(self, a, b, color=STEEL, width=LW_WIRE):
        """Fio/tubo: linha grossa com brilho fino (leitura de volume sem sombreamento caro)."""
        a, b = np.asarray(a, dtype=float), np.asarray(b, dtype=float)
        d = b - a
        n = np.array([-d[1], d[0], 0.0])
        n = n / (np.linalg.norm(n) + 1e-9) * 0.018
        return VGroup(Line(a, b, color=color, stroke_width=width + 3).set_opacity(0.55),
                      Line(a, b, color=color, stroke_width=width),
                      Line(a + n, b + n, color=WHITE, stroke_width=1.6).set_opacity(0.45)).set_z_index(3)

    # ── quadros / render ─────────────────────────────────────────────────────────────────────────────────────
    def dynamic_last(self):
        static, trackers, dynamic = [], [], []
        for m in self.mobjects:
            if isinstance(m, ValueTracker):
                trackers.append(m)
            elif m.get_family_updaters():
                dynamic.append(m)
            else:
                static.append(m)
        self.mobjects = static + trackers + dynamic

    def get_moving_and_static_mobjects(self, animations):
        moving, static = super().get_moving_and_static_mobjects(animations)
        roots, seen = [], set()
        for m in moving:
            if id(m) not in seen:
                roots.append(m)
                seen.update(id(c) for c in m.get_family())
        return roots, static

    def agora(self):
        """Tempo absoluto do vídeo (inclui o deslocamento T0 de quando o render começa numa seção)."""
        return float(self.time) + self._t0

    def quadros(self, d):
        """Duração arredondada à grade de 1/15 s (múltipla de quadro tanto a 15 quanto a 30 fps): o tempo da cena coincide com o do vídeo
        (sem a deriva de ceil por play) e a linha do tempo é a mesma no preview e no render final."""
        n = max(1, round(d * 15))
        return n / 15 - 1e-6 if n > 1 else 1 / 15

    def fator(self):
        """(anim, espera): quanto esticar/encolher o que resta da janela entre dois alvos de voz. Anim ≤ 1,35× e espera ≤ 3× ao esticar;
        anim ≥ 0,4× e espera ≥ 0,05× ao comprimir. Os dois ficam sempre ≤ ao fator da janela: nunca passam do alvo."""
        w = self._win
        if not w:
            return 1.0, 1.0
        f = (w[1] - self.agora()) / max(w[0] - w[2], 0.25)
        if f >= 1:
            return min(f, 1.35), min(f, 3.0)
        fa = max(f, 0.4)
        return fa, min(1.0, max(0.05, 2 * f - fa))

    def play(self, *animations, **kwargs):
        self.dynamic_last()
        if not animations:
            return None
        anims = [prepare_animation(a) for a in animations]
        rt = kwargs.pop("run_time", None)
        fa, fh = (1.0, 1.0) if self._raw else self.fator()
        nat = 0.0
        for a in anims:
            n = rt if rt is not None else a.run_time
            nat = max(nat, n)
            a.run_time = self.quadros(n * (fh if isinstance(a, Wait) else fa))
        if self._win and not self._raw:
            self._win[2] += nat
        return super().play(*anims, **kwargs)

    def hold(self, d):
        if d <= 1e-3:
            return
        self.update_mobjects(0)
        paused = [(m, list(m.updaters)) for m in self.mobjects if getattr(m, "state_geometry", False)]
        for m, _ in paused:
            m.clear_updaters(recursive=False)
        self.dynamic_last()
        try:
            self.wait(d, frozen_frame=False)
        finally:
            for m, ups in paused:
                for u in ups:
                    m.add_updater(u)

    def hold_ate(self, t):
        """Espera (sem compressão) até o instante absoluto t do vídeo."""
        self._raw = True
        try:
            d = t - self.agora()
            if d >= 0.5 / config.frame_rate:
                self.hold(d)
        finally:
            self._raw = False

    def evento(self, tipo, texto=""):
        """Cada legenda/equação/título/seção/marca é um evento (ordinal = o do log V6 + EV_OFF). Os que têm alvo de voz esperam por ele; a janela
        até o próximo alvo é comprimida (play ≥ 0,6×, esperas mais) quando a voz é mais curta que a animação natural."""
        i = self._ev
        self._ev += 1
        self.eventos.append([i, round(self.agora(), 3), tipo, str(texto)[:70]])
        if SYNC is None:
            return
        ab = SYNC["abertura"]
        e = SYNC["eventos"].get(str(i))
        alvo = {1: ab["leg1"], 2: ab["eq"], 3: ab["leg2"]}.get(i, e["alvo"] if e else None)
        if alvo is None:
            return
        self._win = None            # a janela anterior acabou: a espera e a "vida" deste alvo rodam sem esticar/comprimir
        if alvo - self.agora() >= 3.0 and tipo != "marca":
            self.vida(alvo)
        else:
            self.hold_ate(alvo)
        self.atrasos.append([i, round(self.agora() - alvo, 3), tipo, str(texto)[:50]])
        self._win = [e["janela"], e["prox"], 0.0] if e and e.get("janela") and e.get("prox") else None

    def quando(self, rx, t0, t1):
        """Instante em que a voz começa a frase que casa com rx (sem acentos, minúsculas) entre t0 e t1; None se não houver."""
        for m in re.finditer(_semac(rx), _TXT):
            t = PAL[_TXT[:m.start()].count(" ")][1]
            if t0 <= t < t1:
                return t
        return None

    def na_fala(self, rx, antes=0.0):
        """Espera a voz chegar à frase rx (≤ 80 s à frente); False se já passou ou não existe (então não anima)."""
        t = self.quando(rx, self.agora() - 0.4, self.agora() + 80) if SYNC else None
        if t is None:
            return False
        self.hold_ate(t - antes)
        return True

    def destaque(self, m, color=WHITE, scale=1.45, rt=1.0):
        self.play(Indicate(m, color=color, scale_factor=scale), run_time=rt)

    def vida(self, fim):
        """Tela parada esperando a voz: destaca, em ordem, os termos da equação à vista no instante em que a voz os nomeia (FALADO)."""
        eq = next((self.slots[k]["eq"] for k in ("H", "A") if self.slots[k]["eq"] is not None and hasattr(self.slots[k]["eq"], "tok")), None)
        if eq is not None:
            t0, cues = self.agora(), []
            for tok in eq.tok:
                rx = next((r for k, r in FALADO if k in tok), None)
                t = self.quando(rx, t0 + 0.3, fim - 1.0) if rx else None
                if t is not None:
                    cues.append((t, tok))
            for t, tok in sorted(cues):
                if t - 0.15 < self.agora():
                    continue
                self.hold_ate(t - 0.15)
                r = box(glyphs(eq, tok, 0), WHITE, buff=0.1, width=2.5)
                self.play(FadeIn(r), run_time=0.3)
                self.hold(1.2)
                self.play(FadeOut(r), run_time=0.25)
                self.purge(r)
            if not cues and fim - self.agora() >= 2.5:      # nada a destacar na equação: um pulso discreto no que está à vista
                self.hold_ate(self.agora() + (fim - self.agora()) / 2 - 0.5)
                self.destaque(eq, scale=1.05, rt=1.0)
        elif self.cap is not None and fim - self.agora() >= 2.5:
            self.hold_ate(self.agora() + (fim - self.agora()) / 2 - 0.5)
            self.destaque(self.cap, scale=1.06, rt=1.0)
        self.hold_ate(fim)

    def fim_sync(self):
        if SYNC is not None:
            self.hold_ate(SYNC["dur"] + 1.0)

    def flow(self, paths, count=7, direction=1, color=GREEN, dash=0.30, width=8):
        """Marcas convencionais de corrente: traços alongados (cabeça mais clara que a cauda). Não são cargas.
        paths: funções u∈[0,1] → ponto da tela. Usa set_points_as_corners (put_start_and_end_on falha com comprimento ~0)."""
        g = VGroup()
        for path in paths:
            pts = np.array([path(t) for t in np.linspace(0, 1, 41)])
            length = float(np.linalg.norm(np.diff(pts, axis=0), axis=1).sum()) + 1e-6
            du = dash / 2 / length
            for k in range(count):
                tail = Line(LEFT, RIGHT, color=color, stroke_width=width, cap_style=CapStyleType.ROUND).set_opacity(0.5)
                head = Line(LEFT, RIGHT, color=color, stroke_width=width, cap_style=CapStyleType.ROUND)
                for ln in (tail, head):
                    ln.set_stroke(BACKGROUND_COLOR, width + 3.5, background=True)
                mark = VGroup(tail, head).set_z_index(8)

                def move(m, p=path, phase=k / count, du=du):
                    s = direction() if callable(direction) else direction
                    u = (phase + s * self.clock.get_value()) % 1
                    back = p(min(max(u - s * du, 0.0), 1.0))
                    front = p(min(max(u + s * du, 0.0), 1.0))
                    m[0].set_points_as_corners([back, front])
                    m[1].set_points_as_corners([p(u), front])
                mark.add_updater(move)
                mark.update(0)
                g.add(mark)
        return g

    def cached(self, key, builder):
        """Reconstrói o desenho só quando o estado muda (key()), não a cada quadro."""
        last = [key()]
        group = builder()

        def update(m):
            st = key()
            if st != last[0]:
                fresh = builder()
                m.submobjects = fresh.submobjects
                m.points = fresh.points.copy()
                last[0] = st
        group.add_updater(update)
        group.state_geometry = True
        return group

    def view_key(self):
        return tuple(v.get_value() for v in (self.ox, self.oy, self.gs, self.beta, self.tau))

    def reset_view(self, x=-3.9, y=-0.4, scale=1.1, beta=0, tau=0):
        for tr, v in [(self.ox, x), (self.oy, y), (self.gs, scale), (self.beta, beta), (self.tau, tau)]:
            tr.set_value(v)

    def out_symbol(self, p, sign=1, radius=0.17, color=MAG):
        """⊙ (sai da tela, sign>0) ou ⊗ (entra, sign<0)."""
        g = VGroup(Circle(radius=radius, color=color, stroke_width=3.5).set_fill(BACKGROUND_COLOR, 0.9).move_to(p))
        if sign > 0:
            g.add(Dot(p, radius=radius / 2.8, color=color))
        else:
            r = radius * 0.62
            g.add(Line(p + [-r, -r, 0], p + [r, r, 0], color=color, stroke_width=3.5),
                  Line(p + [-r, r, 0], p + [r, -r, 0], color=color, stroke_width=3.5))
        return g.set_z_index(9)

    # ── marcas, seções, legenda ──────────────────────────────────────────────────────────────────────────────
    def mark(self, name):
        self.evento("marca", name)
        self.checkpoints.append({"name": name, "time": round(float(self.time), 3), "part": self.renderer.num_plays})
        if os.environ.get("QA_STILLS"):
            self.update_mobjects(0)
            self.renderer.update_frame(self, ignore_skipping=True)
            out = Path(config.media_dir) / "estados"
            out.mkdir(parents=True, exist_ok=True)
            self.renderer.camera.get_image().save(out / f"{len(self.checkpoints):03d}_{name}.png")
        for root in self.mobjects:
            if root is getattr(self, "tag", None) or root is getattr(self, "wm", None):
                continue
            for m in root.get_family():
                if (isinstance(m, MathTex) or m.__class__.__name__ == "Text") and m.width:
                    if m.get_left()[0] < -7.3 or m.get_right()[0] > 7.3 or m.get_bottom()[1] < -3.75 or m.get_top()[1] > 3.9:
                        self.layout_issues.append({"checkpoint": name, "text": getattr(m, "tex_string", getattr(m, "text", ""))})

    def section(self, name, title=None):
        self.estado_secoes[name] = [round(self.agora(), 3), self._ev, list(self._win) if self._win else None]
        self.evento("secao", name)
        if title:
            self.evento("titulo", title)
        print(f"[5.3] {name} — {float(self.time):.2f}s", flush=True)
        self.next_section(name, skip_animations=bool(SEG and name not in SEG.split(",")))
        self.sections.append({"name": name, "time": round(float(self.time), 3), "part": self.renderer.num_plays})
        if title:
            self.delcap()
            new = txt(title, T_HEAD).move_to([0, 3.3, 0])
            if self.head is not None:
                self.play(FadeOut(self.head), run_time=0.25)
            self.play(FadeIn(new), run_time=0.5)
            self.head = new

    def delcap(self):
        if self.cap is not None:
            self.play(FadeOut(self.cap), run_time=0.35)
            self.cap = None

    def caption(self, s, color=WHITE, rt=0.45):
        """A legenda não aparece mais na tela (a narração já diz o mesmo); o evento continua sendo o ponto de sincronismo com a voz.
        O tempo natural que ela ocupava (saída + entrada) segue contado na janela de ritmo."""
        self.evento("legenda", s)
        if self._win:
            self._win[2] += 0.22 + rt

    # ── layouts: partição da tela que muda conforme a operação (geometria / split / álgebra) ───────────────
    def relayout(self, name, rt=1.0):
        """Anima cartões e equações vivos até o novo layout; sem criar cartões vazios."""
        anims = []
        for k, ((x, y), w, h) in LAYOUTS[name].items():
            s = self.slots[k]
            s.update(pos=np.array([x, y, 0.0]), w=w, h=h)
            eq = s["eq"]
            if s["card"] is not None:
                ch = self._need_h(eq, s) if (eq is not None and hasattr(eq, "tok")) else h
                nc = panel(w, ch, s["pos"])
                anims.append(ReplacementTransform(s["card"], nc))
                s["card"], s["ch"] = nc, ch
            if eq is not None and hasattr(eq, "nat_w"):
                tgt = eq.copy()
                f = min(1.0, (w - 0.55) / eq.nat_w) / max(1e-6, eq.width / eq.nat_w)
                tgt.scale(f)
                tgt.move_to(s["pos"])
                anims.append(eq.animate.become(tgt))
            elif eq is not None:
                tgt = eq.copy()
                if tgt.width > w - 0.55:
                    tgt.scale_to_fit_width(w - 0.55)
                tgt.move_to(s["pos"])
                anims.append(eq.animate.become(tgt))
        self.layout_name = name
        if anims:
            self.play(*anims, run_time=rt)

    # ── slots de equação (HERO / AUX) com proveniência dos termos ────────────────────────────────────────────
    def _need_h(self, eq, s):
        """Altura do cartão acompanha a expressão (margem moderada); s["h"] é o máximo do layout."""
        return float(min(s["h"], max(1.25, eq.height + 0.8)))

    def _card(self, slot):
        s = self.slots[slot]
        if s["card"] is None:
            s["card"] = panel(s["w"], s["h"], s["pos"])
            s["ch"] = s["h"]
            return s["card"]
        return None

    def show(self, new, *pairs, slot="H", src=None, rt=1.6, wait=2.0, auto=True, structure=True):
        """Mostra `new` no slot. Se já havia equação: TransformByGlyphMap (termos transportados, saídas e entradas).
        src={(token, occ): mobject|lista}: o termo nasce voando de uma CÓPIA CONGELADA do objeto do desenho; os glifos de
        destino ficam reservados (o auto-mapeamento não os toca). Cada glifo de destino tem um único proprietário."""
        self.evento("equacao", getattr(new, "tex_string", ""))
        s = self.slots[slot]
        new.move_to(s["pos"])
        new.nat_w = new.width
        max_w = s["w"] - 0.55
        if new.width > max_w:
            new.scale_to_fit_width(max_w)
            new.move_to(s["pos"])
        if new.height > s["h"] - 0.5:          # chaves/frações altas: a expressão inteira cabe no cartão
            new.scale_to_fit_height(s["h"] - 0.5)
            new.move_to(s["pos"])
        need = self._need_h(new, s)
        card = None
        if s["card"] is None:
            s["card"] = panel(s["w"], need, s["pos"])
            s["ch"] = need
            card = s["card"]
        resize = None
        if card is None and abs(need - s.get("ch", need)) > 0.4:
            resize = (s["card"], panel(s["w"], need, s["pos"]))
            s["card"], s["ch"] = resize[1], need
        old = s["eq"]
        flights, restore, reserved = [], [], set()
        for key, mob in (src or {}).items():
            keys = key if isinstance(key[0], tuple) else (key,)      # vários tokens de destino podem voar de um só objeto
            g = VGroup(*[glyphs(new, tok, occ) for tok, occ in keys])
            ghost = g.copy()
            for tok, occ in keys:
                for idx in (new.tok[tok] if occ is None else [new.tok[tok][occ]]):
                    reserved.update(idx)
            restore.append((g, [(x.get_fill_opacity(), x.get_stroke_opacity()) for x in g.family_members_with_points()], ghost))
            g.set_opacity(0)
            source = VGroup(*mob) if isinstance(mob, (list, tuple)) else mob
            snap = source.copy()
            snap.clear_updaters(recursive=True)
            flights.append(TransformFromCopy(snap, ghost))
        anims = list(flights)
        if card is not None:
            anims.append(FadeIn(card))
        if resize is not None:
            anims.append(ReplacementTransform(resize[0], resize[1]))
        if old is not None and not hasattr(old, "tok"):
            anims.append(FadeOut(old))
            old = None
        if old is None:
            anims.append(FadeIn(new))
        else:
            anims.append(gmap(old, new, *pairs, auto=auto, structure=structure, reserved=reserved))
        self.play(*anims, run_time=rt)
        if old is not None:
            self.remove(old)
        for g, ops, ghost in restore:
            for x, (fo, so) in zip(g.family_members_with_points(), ops):
                x.set_fill(opacity=fo)
                x.set_stroke(opacity=so)
            self.remove(ghost)
        s["eq"] = new
        if wait:
            self.hold(wait)
        return new

    def drop(self, slot="H", rt=0.6, keep_card=None):
        s = self.slots[slot]
        if keep_card is None:
            keep_card = slot == "H"
        anims = []
        stale = []
        if s["eq"] is not None:
            anims.append(FadeOut(s["eq"]))
            if not hasattr(s["eq"], "tok"):
                # grupos montados com FadeIn separado: os filhos (e netos) também estão na cena
                stale = list(s["eq"].get_family())[1:]
            s["eq"] = None
        if not keep_card and s["card"] is not None:
            anims.append(FadeOut(s["card"]))
            s["card"] = None
        if anims:
            self.play(*anims, run_time=rt)
        for m in stale:
            self.remove(m)

    def hl(self, tok, occ=0, slot="H", color=MAG, rt=0.9):
        """Destaca a parcela que vai ser substituída/transportada antes da transformação."""
        eq = self.slots[slot]["eq"]
        r = box(glyphs(eq, tok, occ), color, buff=0.1, width=3)
        self.play(FadeIn(r), run_time=0.3)
        self.hold(rt)
        self.play(FadeOut(r), run_time=0.25)

    def pulse(self, m, color=WHITE, rt=0.9):
        self.play(Indicate(m, color=color, scale_factor=1.12), run_time=rt)

    # ── lifecycle (V2): nada sai "pela metade" ─────────────────────────────────────────────────────────────────
    # Animar filhos de um grupo (LaggedStart(Create(f) for f in g)) faz o Manim adicionar CADA filho à cena; remover só o grupo
    # deixa os filhos vivos (foi a origem dos anéis duplicados/congelados da V1). purge() remove a família inteira.
    def purge(self, *mobs):
        for m in mobs:
            fam = m.get_family()
            for x in fam:
                x.clear_updaters(recursive=False)
            self.remove(*fam)

    def out(self, *mobs, rt=0.6):
        mobs = [m for m in mobs if m is not None]
        if mobs:
            self.play(*[FadeOut(m) for m in mobs], run_time=rt)
        self.purge(*mobs)

    def scene_census(self):
        """Objetos vivos na cena além dos fixos (QA de lifecycle: deve ser 0 logo após clear())."""
        fixed = {id(self.tag), id(self.wm), id(self.head)}
        return [type(m).__name__ for m in self.mobjects if id(m) not in fixed and not isinstance(m, ValueTracker)]

    def clear(self, keep=()):
        fixed = [self.tag, self.wm, self.head, *keep]
        mobs = [m for m in self.mobjects if all(m is not f for f in fixed) and not isinstance(m, ValueTracker)]
        for m in mobs:
            m.clear_updaters(recursive=True)
        if mobs:
            self.play(*[FadeOut(m) for m in mobs], run_time=0.9)
        self.purge(*mobs)
        left = [] if keep else self.scene_census()
        self.checkpoints.append({"name": "census_after_clear", "time": round(float(self.time), 3), "alive": left})
        self.cap = None
        for k, ((x, y), w, h) in LAYOUTS["split"].items():
            self.slots[k].update(eq=None, card=None, pos=np.array([x, y, 0.0]), w=w, h=h)
        self.layout_name = "split"

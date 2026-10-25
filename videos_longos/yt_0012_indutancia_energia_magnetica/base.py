"""Núcleo da cena do yt_0012 (cópia local da base do yt_0006): projeção 2.5D, relógio da corrente, slots de equação, legendas e utilitários."""
import json
import math
import os
import sys
from pathlib import Path

import numpy as np
from manim import (
    Scene, VGroup, VMobject, ValueTracker, ImageMobject, MathTex, DecimalNumber, Line, DashedLine, Arc, Circle, Dot,
    Polygon, Ellipse, ParametricFunction, CapStyleType, FadeIn, FadeOut, Create, ReplacementTransform, Transform, TransformFromCopy,
    Write, Indicate, LaggedStart, AnimationGroup, UP, DOWN, LEFT, RIGHT, UL, UR, BOLD, always_redraw, linear, smooth,
    there_and_back, config, Wait,
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
SYNC_LOG = os.environ.get("SYNC_LOG", "")      # arquivo .jsonl: registra cada play/espera (índice, tipo, instante editorial, duração nominal)
SYNC = os.environ.get("SYNC", "")              # ritmo.json: instante de início (s) de cada play(), na ordem das chamadas; vale em qualquer fps
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
}


class Base(Scene):
    def setup(self):
        self.camera.background_color = BACKGROUND_COLOR
        config.max_files_cached = 1000
        config.disable_caching = True
        self.ox, self.oy, self.gs = ValueTracker(-3.9), ValueTracker(-0.4), ValueTracker(1.1)
        self.beta, self.tau = ValueTracker(0), ValueTracker(0)
        self.checkpoints, self.sections, self.layout_issues = [], [], []
        self.head = self.cap = None
        self.slots = {"H": {"pos": HERO, "eq": None, "card": None, "w": 6.7, "h": 2.5, "name": None, "note": None},
                      "A": {"pos": AUX, "eq": None, "card": None, "w": 6.7, "h": 2.45, "name": None, "note": None}}
        self.layout_name = "split"
        self._pi, self._e, self._ritmo = 0, 0.0, None
        if SYNC:
            self._ritmo = json.load(open(SYNC, encoding="utf-8"))["t"]
        self.anchors = []
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

    def tip(self, text, point, size=22, color=DIM):
        """Descrição curta de uma variável, junto ao rótulo (sai quando a relação está consolidada)."""
        return halo(rich(text, size, color).move_to(point)).set_z_index(12)

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

    def play(self, *animations, **kwargs):
        """Todo o tempo da cena passa por aqui. Com SYNC_LOG, registra os intervalos; com SYNC, cada intervalo dura
        exatamente o nº de quadros da tabela (a cena segue a voz, sem deriva)."""
        self.dynamic_last()
        anims = [prepare_animation(a) for a in animations]
        nominal = float(kwargs["run_time"]) if "run_time" in kwargs else max((a.run_time for a in anims), default=0.0)
        kind = "hold" if (len(anims) == 1 and isinstance(anims[0], Wait)) else "anim"
        k = self._pi
        self._pi += 1
        if SYNC_LOG:
            with open(SYNC_LOG, "a", encoding="utf-8") as f:
                f.write(json.dumps({"i": k, "kind": kind, "e0": round(self._e, 4), "nom": round(nominal, 4)}) + chr(10))
        self._e += nominal
        if self._ritmo is not None and nominal > 0:
            if k + 1 >= len(self._ritmo):
                raise RuntimeError(f"ritmo.json tem {len(self._ritmo) - 1} intervalos, mas a cena chamou o {k + 1}º: refaça a tabela")
            fps = config.frame_rate
            F = round(self._ritmo[k + 1] * fps) - round(self._ritmo[k] * fps)    # tempo absoluto: sem deriva em qualquer fps
            if F <= 0 and kind == "hold":
                return None
            kwargs["run_time"] = max(F, 1) / fps - 0.25 / fps    # ceil → exatamente F quadros
        return super().play(*anims, **kwargs)

    def an(self, frase):
        """Âncora: o próximo play() começa LEAD s antes da fala `frase` (primeiras palavras, na ordem da narração).
        A espera mínima registrada aqui é a folga que segura a tela parada até a fala, quando sobra tempo."""
        if SYNC_LOG:
            with open(SYNC_LOG, "a", encoding="utf-8") as f:
                f.write(json.dumps({"anchor": frase, "i": self._pi + 1}, ensure_ascii=False) + chr(10))
        self.anchors.append(frase)
        self.wait(0.01)

    def hold(self, d):
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

    def flow(self, paths, count=7, direction=1, color=GREEN, dash=0.30, width=8):
        """Marcas convencionais de corrente (sentido convencional, nunca velocidade de deriva): traços alongados que
        correm pelo caminho, cabeça mais clara que a cauda. Não são cargas. paths: funções u∈[0,1] → ponto da tela."""
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
    def _ev(self, kind, text):
        """Registro de eventos para ancorar a narração (só com QA_EVENTS=<arquivo>)."""
        path = os.environ.get("QA_EVENTS")
        if path:
            with open(path, "a", encoding="utf-8") as f:
                f.write(json.dumps({"t": round(float(self._e), 2), "kind": kind, "text": text}, ensure_ascii=False) + chr(10))

    def mark(self, name):
        self._ev("mark", name)
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
        print(f"[5.2] {name} — {float(self.time):.2f}s", flush=True)
        self._ev("section", name)
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
        """Nota curta que nomeia a operação atual. Saída e entrada em sequência (nunca duas frases juntas)."""
        self._ev("caption", s)
        new = rich(s, T_CAP, color)
        if new.width > 13.6:
            new.scale_to_fit_width(13.6)
        new.move_to([0, -3.2, 0])
        if self.cap is not None:
            self.play(FadeOut(self.cap), run_time=0.22)
        self.play(FadeIn(new, shift=UP * 0.06), run_time=rt)
        self.cap = new

    # ── layouts: partição da tela que muda conforme a operação (geometria / split / álgebra) ───────────────
    PAD_X, PAD_Y, DECO_H = 0.9, 0.8, 0.42

    def _fit(self, eq, s):
        """Tamanho do cartão = conteúdo (nome + fórmula + nota) com margem fixa; s["w"], s["h"] são só o máximo do layout."""
        nm, nt = s.get("name"), s.get("note")
        dh = self.DECO_H * ((nm is not None) + (nt is not None))
        w = eq.width + self.PAD_X
        for d in (nm, nt):
            if d is not None:
                w = max(w, d.width + 0.8)
        w = min(s["w"], max(3.2, w))
        h = min(s["h"] + dh, max(1.25, eq.height + self.PAD_Y + dh))
        return float(w), float(h)

    def _need_h(self, eq, s):
        return self._fit(eq, s)[1]

    def _eq_pos(self, s):
        """Centro da fórmula dentro do cartão (desloca para dar lugar ao nome, em cima, e à nota, embaixo)."""
        dy = (-0.5 * self.DECO_H if s.get("name") is not None else 0.0) + (0.5 * self.DECO_H if s.get("note") is not None else 0.0)
        return s["pos"] + np.array([0.0, dy, 0.0])

    def _deco_pos(self, s, key):
        h = s.get("ch", s["h"])
        y = s["pos"][1] + (h / 2 - 0.3 if key == "name" else -h / 2 + 0.3)
        return np.array([s["pos"][0], y, 0.0])

    def _resize_rule(self, s, w, h):
        """Histerese: o cartão cresce quando o conteúdo não cabe; só encolhe quando sobra muito (uma vez por etapa)."""
        cw, ch = s.get("cw", s["w"]), s.get("ch", s["h"])
        if w > cw + 0.01 or h > ch + 0.01 or cw - w > 1.2 or ch - h > 0.7:
            return w, h
        return cw, ch

    def relayout(self, name, rt=1.0):
        """Anima cartões e equações vivos até o novo layout; sem criar cartões vazios."""
        anims = []
        for k, ((x, y), w, h) in LAYOUTS[name].items():
            s = self.slots[k]
            s.update(pos=np.array([x, y, 0.0]), w=w, h=h)
            eq = s["eq"]
            if eq is not None and hasattr(eq, "nat_w"):
                f = min(1.0, (w - 0.55) / eq.nat_w) / max(1e-6, eq.width / eq.nat_w)
                tgt = eq.copy()
                tgt.scale(f)
                tgt.move_to(self._eq_pos(s))
                cw, ch = self._fit(tgt, s)
            elif eq is not None:
                tgt = eq.copy()
                if tgt.width > w - 0.55:
                    tgt.scale_to_fit_width(w - 0.55)
                tgt.move_to(self._eq_pos(s))
                cw, ch = (self._fit(tgt, s) if s["card"] is not None else (w, h))
            else:
                tgt, cw, ch = None, w, h
            if s["card"] is not None:
                nc = panel(cw, ch, s["pos"])
                anims.append(ReplacementTransform(s["card"], nc))
                s["card"], s["cw"], s["ch"] = nc, cw, ch
            if tgt is not None:
                anims.append(eq.animate.become(tgt))
            for key in ("name", "note"):
                if s.get(key) is not None:
                    anims.append(s[key].animate.move_to(self._deco_pos(s, key)))
        self.layout_name = name
        if anims:
            self.play(*anims, run_time=rt)

    # ── slots de equação (HERO / AUX) com proveniência dos termos ────────────────────────────────────────────
    def _card(self, slot):
        s = self.slots[slot]
        if s["card"] is None:
            s["card"] = panel(s["w"], s["h"], s["pos"])
            s["cw"], s["ch"] = s["w"], s["h"]
            return s["card"]
        return None

    def show(self, new, *pairs, slot="H", src=None, rt=1.6, wait=2.0, auto=True, structure=True, name=None, note=None):
        """Mostra `new` no slot. Se já havia equação: TransformByGlyphMap (termos transportados, saídas e entradas).
        src={(token, occ): mobject|lista}: o termo nasce voando de uma CÓPIA CONGELADA do objeto do desenho; os glifos de
        destino ficam reservados (o auto-mapeamento não os toca). Cada glifo de destino tem um único proprietário.
        name/note: âncora semântica (nome da lei) e nota curta, dentro do mesmo cartão."""
        s = self.slots[slot]
        self._ev("eq" + ("-aux" if slot == "A" else ""), getattr(new, "tex", "") + (f"  [nome: {name}]" if name else "") + (f"  [nota: {note}]" if note else ""))
        new.nat_w = new.width
        max_w = s["w"] - 0.55
        if new.width > max_w:
            new.scale_to_fit_width(max_w)
        # decorações (nome da lei em cima, nota embaixo): saem se não foram pedidas de novo
        deco_in, deco_anims = [], []
        for key, val, build in (("name", name, lambda v: txt(v, 24, DIM)), ("note", note, lambda v: v if isinstance(v, VMobject) else (defn(*v) if isinstance(v, tuple) else rich(v, 24, DIM)))):
            old = s.get(key)
            if old is not None and (val is None or getattr(old, "src_text", None) != val):
                deco_anims.append(FadeOut(old, rate_func=lambda t: smooth(min(1.0, 2 * t))))   # yt_0012: sai antes
                s[key] = old = None
            if val is not None and old is None:
                m = build(val)
                m.src_text = val
                if m.width > s["w"] - 0.8:
                    m.scale_to_fit_width(s["w"] - 0.8)
                s[key] = m
                deco_in.append((key, m))
        w_need, h_need = self._fit(new, s)
        new.move_to(self._eq_pos(s))
        card = None
        resize = None
        if s["card"] is None:
            s["card"] = card = panel(w_need, h_need, s["pos"])
            s["cw"], s["ch"] = w_need, h_need
        else:
            cw, ch = self._resize_rule(s, w_need, h_need)
            if abs(cw - s.get("cw", s["w"])) > 0.01 or abs(ch - s.get("ch", s["h"])) > 0.01:
                resize = (s["card"], panel(cw, ch, s["pos"]))
                s["card"], s["cw"], s["ch"] = resize[1], cw, ch
        for key, m in deco_in:
            m.move_to(self._deco_pos(s, key))
            deco_anims.append(FadeIn(m, rate_func=lambda t: smooth(max(0.0, 2 * t - 1))))   # yt_0012: entra depois
        for key in ("name", "note"):
            m = s.get(key)
            if m is not None and all(m is not d for _, d in deco_in):
                deco_anims.append(m.animate.move_to(self._deco_pos(s, key)))
        old = s["eq"]
        flights, restore, reserved = [], [], set()
        for (tok, occ), mob in (src or {}).items():
            g = glyphs(new, tok, occ)
            ghost = g.copy()
            lst = new.tok[tok] if occ is None else [new.tok[tok][occ]]
            for idx in lst:
                reserved.update(idx)
            restore.append((g, [(x.get_fill_opacity(), x.get_stroke_opacity()) for x in g.family_members_with_points()], ghost))
            g.set_opacity(0)
            source = VGroup(*mob) if isinstance(mob, (list, tuple)) else mob
            snap = source.copy()
            snap.clear_updaters(recursive=True)
            flights.append(TransformFromCopy(snap, ghost))
        anims = list(flights) + deco_anims
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

    def name_card(self, name, slot="H", rt=0.9):
        """Põe o nome da lei/resultado num cartão já estável (depois que a álgebra terminou)."""
        s = self.slots[slot]
        self._ev("name", name)
        m = txt(name, 22, DIM)
        m.src_text = name
        s["name"] = m
        w, h = self._fit(s["eq"], s)
        cw, ch = max(w, s.get("cw", w)), h
        nc = panel(cw, ch, s["pos"])
        anims = [ReplacementTransform(s["card"], nc), s["eq"].animate.move_to(self._eq_pos(s))]
        s["card"], s["cw"], s["ch"] = nc, cw, ch
        m.move_to(self._deco_pos(s, "name"))
        anims.append(FadeIn(m))
        self.play(*anims, run_time=rt)

    def drop(self, slot="H", rt=0.6, keep_card=None):
        s = self.slots[slot]
        if keep_card is None:
            keep_card = slot == "H"
        anims = []
        stale = []
        if s["eq"] is not None:
            anims.append(FadeOut(s["eq"]))
            if not hasattr(s["eq"], "tok"):
                # grupos montados com FadeIn separado: os filhos também estão na cena
                stale = list(s["eq"].submobjects)
            s["eq"] = None
        for key in ("name", "note"):
            if s.get(key) is not None:
                anims.append(FadeOut(s[key]))
                s[key] = None
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

    def destaca(self, mobs, d, color=WHITE, each=1.0):
        """Troca uma espera de d s por destaques em sequência dos objetos que a fala cita (cada um 'each' s); o resto é espera.
        A tela acompanha a explicação em vez de ficar parada."""
        usado = 0.0
        for m in mobs:
            self.play(Indicate(m, color=color, scale_factor=1.12), run_time=each)
            usado += each
        if d - usado > 0.05:
            self.hold(d - usado)

    def pulse(self, m, color=WHITE, rt=0.9):
        self.play(Indicate(m, color=color, scale_factor=1.12), run_time=rt)

    def clear(self, keep=()):
        fixed = [self.tag, self.wm, self.head, *keep]
        mobs = [m for m in self.mobjects if all(m is not f for f in fixed) and not isinstance(m, ValueTracker)]
        for m in mobs:
            m.clear_updaters(recursive=True)
        if mobs:
            self.play(*[FadeOut(m) for m in mobs], run_time=0.9)
        self.cap = None
        for k, ((x, y), w, h) in LAYOUTS["split"].items():
            self.slots[k].update(eq=None, card=None, name=None, note=None, pos=np.array([x, y, 0.0]), w=w, h=h)
        self.layout_name = "split"

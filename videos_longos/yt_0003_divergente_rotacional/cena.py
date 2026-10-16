"""yt_0003: V1.5 visual; física e ordem V1.2. Preview silencioso horizontal.

TRECHO=A/B/C/D/E/F seleciona os gates antes do preview completo.
Construção principal inteiramente em Manim, conforme handoff V1.5.
"""
import os
import json
import re
import sys
from pathlib import Path
import numpy as np
from manim import *
from manim.mobject.text.tex_mobject import MathTexPart

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from template.config_horizontal import BACKGROUND_COLOR, PRIMARY_COLOR, WATERMARK_PATH
from template.fonts import DISPLAY_FONT, official_text, screen_text
from MF_Tools import TransformByGlyphMap

# Preserva os intermediários desta unidade para retomar correções localizadas.
config.max_files_cached = 600

LOGO_PATH = Path(__file__).resolve().parents[2] / "assets" / "branding" / "overlays" / "parallax_lab_logo_horizontal.png"
TS = .78  # (V1.7) compressão das esperas de marco; na V3.1 quem manda é a voz
RS = 1.3  # animações explicativas um pouco mais lentas, para respirar com a voz
try:
    RSB = json.loads((Path(__file__).resolve().parent / 'rs_v3_1.json').read_text(encoding='utf-8'))
except Exception:
    RSB = {}
try:
    DUR = json.loads((Path(__file__).resolve().parent / 'duracoes_v3_1.json').read_text(encoding='utf-8'))
except Exception:
    DUR = {}
E = PRIMARY_COLOR
Q = "#7FB2FF"
GEO = "#9C8CFF"
FLUX = "#D6CCFF"
NORMAL = "#267BFF"
DAVEC = "#745CFF"
MAG = "#EA63FF"
MUTED = "#8A97B5"
OMEGA = FLUX
# V1.6: sem âmbar. Operador ∇× e circulação seguem a matemática neutra (branco);
# C1 = violeta da série, C2 = lavanda da série.
CM = {r"\mathbf E": E, r"E_x": E, r"E_y": E, r"E_z": E,
      r"\rho": Q, "q": Q, r"Q_{\rm env}": Q, r"\delta^{(3)}": Q,
      r"\Phi_E": FLUX, r"d\Phi_x": FLUX, r"d\Phi_y": FLUX,
      r"d\Phi_z": FLUX, r"d\Phi": FLUX, r"d\Phi_{x,+}": FLUX, r"d\Phi_{x,-}": FLUX,
      r"\Delta V": GEO, "dV": GEO, r"\partial V": GEO, r"\mathbf B": MAG,
      "V": GEO, "S": GEO, r"\nabla\cdot": GEO, r"\nabla\times": WHITE,
      r"d\mathbf A": DAVEC, "dA": DAVEC, "dA_x": DAVEC, r"\hat{\mathbf n}": NORMAL,
      r"\hat{\mathbf n}_+": NORMAL, r"\hat{\mathbf n}_-": NORMAL,
      r"\hat{\mathbf n}_A": NORMAL, r"\hat{\mathbf n}_B": NORMAL,
      r"\hat{\mathbf x}": NORMAL, r"\hat{\mathbf y}": NORMAL, r"\hat{\mathbf z}": NORMAL,
      r"\Omega": OMEGA, "C_1": GEO, "C_2": FLUX, r"\kappa": WHITE}
CM[r"\Phi"] = FLUX
PROSE = {WHITE, MUTED}


def text(s, size=28, color=WHITE, width=13.8):
    """Prosa em branco/cinza (convenção yt_0001/yt_0002); cor semântica só na matemática."""
    if color not in PROSE:
        color = WHITE
    if size <= 30:
        size = size*.82   # annotation/micro-label: abaixo do subtítulo, longe da headline
    # Mesmo cuidado do yt_0001 com o oversampling de títulos longos no Pango.
    old = config.pixel_width
    config.pixel_width = 4000
    try:
        m = screen_text(s, font_size=size, color=color)
    finally:
        config.pixel_width = old
    if m.width > width:
        m.scale_to_fit_width(width)
    return m


def math(s, size=46, pos=ORIGIN, width=13.5, iso=None):
    """MathTex com partes isoladas por {{ }}; `iso` acrescenta trechos extras {tex: cor}."""
    s = s.replace("_S", "_{S}").replace("_V", "_{V}")
    s = s.replace(r"\frac q", r"\frac{q}").replace(r"\frac1", r"\frac{1}")
    table = dict(CM)
    table.update(iso or {})
    # Manim 0.21 usa substrings_to_isolate para selecionar glifos por SVG;
    # o matching exige partes Tex reais, criadas pela notação {{ ... }}.
    def alt(token):
        # Tokens só de letras não casam dentro de outros comandos (ex.: o q de comandos TeX).
        e = re.escape(token)
        return r"(?<![A-Za-z\\])" + e + r"(?![A-Za-z])" if token.isalpha() else e
    pattern = '|'.join(alt(token) for token in sorted(table, key=len, reverse=True))
    marked = re.sub(pattern, lambda match: ' {{ ' + match.group(0) + ' }} ', s)
    m = MathTex(marked, font_size=size, substrings_to_isolate=list(table))
    for part in m:
        part.tex_string = part.tex_string.strip()
        if part.tex_string in table:
            part.set_color(table[part.tex_string])
    if m.width > width:
        m.scale_to_fit_width(width)
    return m.move_to(pos).set_z_index(15)


def mix(lines, size=22, width=7.0):
    """Prosa com símbolos tipografados (subscritos reais): lines = [[("t","texto"),("m",r"r_a"),...], ...]."""
    rows = VGroup()
    for line in lines:
        row = VGroup(*[text(x[1], size) if x[0] == "t" else math(x[1], size*1.75) for x in line])
        row.arrange(RIGHT, buff=.14, aligned_edge=DOWN)
        rows.add(row)
    rows.arrange(DOWN, buff=.14)
    if rows.width > width:
        rows.scale_to_fit_width(width)
    return rows


def vec(a, b, color=E, width=3, opacity=1):
    if np.linalg.norm(np.array(b)-np.array(a))<.025:
        return VMobject()
    return Arrow(a, b, buff=0, color=color, stroke_width=width,
                 max_tip_length_to_length_ratio=.19).set_opacity(opacity)


def charge(p, radius=.16):
    return VGroup(Circle(radius, color=Q, fill_color=BLUE, fill_opacity=.5),
                  text("+", 24, WHITE)).move_to(p).set_z_index(8)


class Track:
    """Curva amostrada: posição, tangente e trecho revelado saem do MESMO parâmetro t em [0,1]."""
    def __init__(self, pts):
        self.p = np.array(pts, dtype=float)

    @classmethod
    def sample(cls, fn, n=240):
        return cls([fn(a) for a in np.linspace(0, 1, n)])

    def _i(self, t):
        x = float(np.clip(t, 0, 1))*(len(self.p)-1)
        i = int(min(np.floor(x), len(self.p)-2))
        return i, x-i

    def at(self, t):
        i, f = self._i(t)
        return self.p[i]*(1-f)+self.p[i+1]*f

    def tangent(self, t):
        i, _ = self._i(t)
        n = len(self.p)
        d = self.p[min(i+3, n-1)]-self.p[i]
        if np.linalg.norm(d) < 1e-9:
            d = self.p[i]-self.p[max(i-3, 0)]
        if np.linalg.norm(d) < 1e-9:
            return np.array([1., 0, 0])
        return d/np.linalg.norm(d)

    def part(self, t, **kw):
        i, _ = self._i(t)
        pts = list(self.p[:i+1])+[self.at(max(t, 1e-4))]
        if len(pts) < 2:
            pts = [self.p[0], self.p[0]+1e-3]
        return VMobject(**kw).set_points_as_corners(pts)


def display(s, size=36, color=WHITE):
    old = config.pixel_width
    config.pixel_width = 4000
    try:
        m = official_text(s, DISPLAY_FONT, BOLD, size, oversample=2)
    finally:
        config.pixel_width = old
    return m.set_color(color)


CUBE_BASES = [np.array([1., 0, 0]), np.array([.44, .32, 0]), np.array([0, 1., 0])]


def cube_point(p, side, i, j, k):
    return np.array(p, dtype=float) + side/2*(i*CUBE_BASES[0]+j*CUBE_BASES[1]+k*CUBE_BASES[2])


def face(p, side, axis, sign, color=GEO, fill=.4, stroke=3):
    """Face do cubo perpendicular ao eixo `axis` (0=x, 1=y, 2=z), no lado `sign`."""
    others = [a for a in range(3) if a != axis]
    pts = []
    for s, t in [(-1, -1), (1, -1), (1, 1), (-1, 1)]:
        idx = [0, 0, 0]
        idx[axis] = sign
        idx[others[0]] = s
        idx[others[1]] = t
        pts.append(cube_point(p, side, *idx))
    return Polygon(*pts, color=color, stroke_width=stroke, fill_color=color, fill_opacity=fill).set_z_index(5)


def convex_hull(points):
    """Envoltória convexa (cadeia monótona) dos pontos 2D, em sentido anti-horário."""
    pts = sorted(set((round(float(x), 5), round(float(y), 5)) for x, y in points))
    def cross(o, a, b):
        return (a[0]-o[0])*(b[1]-o[1])-(a[1]-o[1])*(b[0]-o[0])
    lower, upper = [], []
    for q in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], q) <= 0:
            lower.pop()
        lower.append(q)
    for q in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], q) <= 0:
            upper.pop()
        upper.append(q)
    return lower[:-1] + upper[:-1]


def face_center(p, side, axis, sign):
    return np.array(p, dtype=float) + side/2*sign*CUBE_BASES[axis]


def cube(p, side=2.2, axis=0):
    """Projeção afim de um cubo centrado exatamente em p (faces x, arestas, P)."""
    p = np.array(p, dtype=float)
    faces = [face(p, side, 0, s, GEO, .17, 2) for s in (-1, 1)]
    edges = VGroup()
    for i in [-1,1]:
        for j in [-1,1]:
            edges.add(Line(cube_point(p,side,i,j,-1),cube_point(p,side,i,j,1),color=GEO,stroke_width=1.4))
            edges.add(Line(cube_point(p,side,i,-1,j),cube_point(p,side,i,1,j),color=GEO,stroke_width=1.4))
            edges.add(Line(cube_point(p,side,-1,i,j),cube_point(p,side,1,i,j),color=GEO,stroke_width=1.4))
    return VGroup(*faces, edges, Dot(p, radius=.055, color=WHITE)).set_z_index(4)


class DivergenteRotacional(Scene):
    def construct(self):
        self.camera.background_color = BACKGROUND_COLOR
        self.live = []
        self.layout_checks = []
        self.marks = []
        self.blk = None
        self.off = None
        self.rs = RS
        self.vt = 0.0
        self.vtlog = []
        self.blocos = []
        self.marcos = []
        self.t0 = 0
        self.t0_old = 0
        self.P = np.array([-3.8,.2,0])
        self.atmosphere()
        self.heading = text("DO GLOBAL AO LOCAL", 33).move_to([0,3.4,0])
        self.add(self.heading)
        section = os.getenv("TRECHO", "")
        run = lambda *keys: section == "" or section in keys
        if run("A"):
            self.opening(); self.gauss()
        if run("B"):
            self.divergence()
        if run("C"):
            self.theorem(); self.local_gauss()
        if run("K"):
            self.example()
        if run("D"):
            self.point_delta(); self.comparison(); self.wheel()
        if run("E"):
            self.circulation(); self.stokes()
        if run("F"):
            self.synthesis(); self.coda(); self.outro()
        self.fecha()
        if os.getenv('LOG_VT') == '1':
            (Path(__file__).resolve().parent / 'renders' / 'vtlog.json').write_text(json.dumps(self.vtlog), encoding='utf-8')
        self.marks.append({'secao': 'fim', 'inicio_local': float(self.vt)})
        (Path(__file__).resolve().parent / 'renders' / f'blocos_v3_1_{section or "completo"}.json').write_text(
            json.dumps({'blocos': self.blocos, 'marcos': self.marcos}, ensure_ascii=False, indent=1), encoding='utf-8')
        here = Path(__file__).resolve().parent / 'renders'
        (here / f'secoes_v1_6_{section or "completo"}.json').write_text(
            json.dumps(self.marks, ensure_ascii=False, indent=2), encoding='utf-8')
        if os.getenv('QA_LAYOUT') == '1':
            (here / f'qa_layout_{section or "completo"}_v1_6.json').write_text(
                json.dumps(self.layout_checks, ensure_ascii=False, indent=2), encoding='utf-8')

    def atmosphere(self):
        # Três planos discretos, sem ocupar a faixa inferior ou competir com E.
        stars = VGroup(*[Dot([((i*3.17)%15)-7.5, ((i*1.71)%7.5)-3.7,0],
                                radius=.008+(i%3)*.003,color=MUTED).set_opacity(.14)
                         for i in range(32)]).set_z_index(-100)
        stars.add_updater(lambda m,dt: m.shift(RIGHT*dt*.003))
        self.add(stars)
        for r in (2.8,3.2,3.8):
            self.add(Circle(r,color=GEO,stroke_width=.7,stroke_opacity=.035)
                     .stretch(.65,1).move_to([-3,0,0]).set_z_index(-101))
        self.wm = ImageMobject(str(WATERMARK_PATH)).set_width(1.92).set_opacity(.45).to_corner(UR,buff=.3)
        self.add(self.wm)
        # Mesmo header da série (yt_0002: HEADER, 18, opacidade .6, canto UL com buff .38).
        self.hdr = text("ELETROMAGNETISMO · DIVERGENTE E ROTACIONAL",18).set_opacity(.6).to_corner(UL,buff=.38)
        self.add(self.hdr)
        # y < -3 permanece livre, conforme layout_horizontal.CONTENT_BOTTOM.

    def title(self, s):
        old = self.heading
        new = text(s,33).move_to(old)
        self.play(FadeOut(old),FadeIn(new),run_time=.5)
        self.remove(old); self.heading = new

    def show(self, *items, t=.8):
        for m in items:
            if m not in self.live:
                self.live.append(m)
        self.play(*[FadeIn(m) for m in items],run_time=t)
        return items[0] if len(items)==1 else items

    def erase(self, *items, t=.5):
        items = [m for m in items if m in self.live]
        if not items:
            return
        self.play(*[FadeOut(m) for m in items],run_time=t)
        for m in items:
            m.clear_updaters(recursive=True)
            self.remove(m)
            self.live.remove(m)

    def clear(self, keep=()):
        self.erase(*[m for m in self.live if m not in keep])

    def change(self, a, b, t=1.2, src=None):
        self.morph(a,b,t,src)
        if a in self.live:
            self.live.remove(a)
        self.live.append(b)
        return b

    def morph(self, a, b, t=1.2, src=None):
        """Matching em três fases: retirar, mover identidades, completar.

        Os termos sem correspondência nunca fazem crossfade sobre o destino.
        `src` {tex: mobject} faz um termo novo nascer como cópia de um objeto já visível.
        """
        def parts(m):
            if isinstance(m,MathTexPart):return [m]
            if isinstance(m,(Group,VGroup)):
                return [p for child in m.submobjects for p in parts(child)]
            return list(TransformMatchingTex.get_mobject_parts(m))
        ap=parts(a);bp=parts(b)
        keys=lambda parts:{m.tex_string for m in parts}
        common=keys(ap)&keys(bp)
        old=[m for m in ap if m.tex_string not in common]
        new=[m for m in bp if m.tex_string not in common]
        am=[m for m in ap if m.tex_string in common]
        bm=[m for m in bp if m.tex_string in common]
        self.remove(a);self.add(*ap)
        if old:self.play(*[FadeOut(m) for m in old],run_time=t*.25)
        if am:
            # Contêiner Tex leve: preserva MathTexPart como unidade do matching,
            # inclusive quando a origem é um termo extraído de outra expressão.
            ac,bc=VMobject(),VMobject()
            ac.tex_string=bc.tex_string=''
            ac.add(*am);bc.add(*bm)
            self.play(TransformMatchingTex(ac,bc),run_time=t*.5)
            self.remove(ac)
        if new:
            anims=[];flights=False
            for m in new:
                s=(src or {}).get(m.tex_string)
                if s is not None:
                    anims.append(TransformFromCopy(s,m));flights=True
                else:
                    anims.append(FadeIn(m))
            self.play(*anims,run_time=t*(.5 if flights else .25))
        self.remove(*ap,*bp)
        if am:self.remove(ac,bc)
        # Remove os containers temporários criados pelo matching.
        for mob in list(self.mobjects):
            if mob is not b and isinstance(mob,VGroup) and mob.submobjects and all(x in bp for x in mob.submobjects):
                self.remove(mob)
        self.add(b)

    def fly(self, source, target, t=.8):
        # Cópia geométrica indica a proveniência sem mutar os glifos do alvo.
        ghost = source.copy().clear_updaters()
        self.add(ghost)
        self.play(ghost.animate.move_to(target).scale_to_fit_width(max(target.width,.06)),
                  run_time=t)
        self.remove(ghost)
        self.show(target,t=.25)
        return target

    def note(self,s,anchor,pos,color=GEO,size=25):
        label=text(s,size,color,width=6).move_to(pos).set_z_index(18)
        line=Line(anchor,label.get_bottom() if pos[1]>anchor[1] else label.get_top(),
                  color=color,stroke_width=1.1).set_z_index(10)
        n=VGroup(line,Dot(anchor,radius=.035,color=color),label)
        self.show(n)
        return n

    def play(self, *animations, **kw):
        if kw.get('run_time') is not None:
            kw['run_time'] = kw['run_time']*self.rs
        t0 = self.renderer.time
        r = super().play(*animations, **kw)
        d = self.renderer.time - t0
        if self.renderer.skip_animations:
            # modo seco / animação pulada pelo -n: o Manim soma o tempo EXATO; o render real grava quadros inteiros.
            # Quantiza como o render (espera estática: int(d/dt); demais: len(arange(0,d,dt))) para que o relógio
            # `vt` seja o mesmo em qualquer modo e em qualquer grupo.
            dt = 1 / config.frame_rate
            est = bool(self.animations) and len(self.animations) == 1 and getattr(self.animations[0], 'is_static_wait', False)
            d = (int(d / dt) if est else len(np.arange(0, d, dt))) * dt
        self.vt += d
        if os.getenv('LOG_VT') == '1':
            self.vtlog.append((self.renderer.num_plays, round(self.vt, 4)))
        return r

    def ancora(self, id_):
        """Início de uma unidade conceitual da narração V3.1. Tempos ABSOLUTOS da voz real (sync_v3_1.json):
        o evento entra em d['t']; o bloco termina em d['t']+d['s'] (um bloco longo de animação só atrasa o seguinte)."""
        self.fecha()
        self.rs = RSB.get(id_, RS)
        d = DUR.get(id_)
        if d is None:
            return
        if self.off is None:
            self.off = 0.0 if id_ == "H01" else (d['t'] - float(self.vt) if 't' in d else 0.0)
        t_ev = d['t'] - self.off if 't' in d else None
        if t_ev is not None and t_ev - self.vt > .02:
            self.wait(t_ev - self.vt)
        fim = (t_ev + d['s']) if t_ev is not None else float(self.vt) + d['s']
        self.blk = (float(self.vt), fim, id_, float(self.vt) - (t_ev if t_ev is not None else float(self.vt)))

    def marco(self, t):
        """Espera até o instante absoluto t (s do vídeo com voz); registra se o marco já havia passado."""
        alvo = t - (self.off or 0.0)
        passou = float(self.vt) - alvo
        if alvo - self.vt > .02:
            self.wait(alvo - self.vt)
        self.marcos.append({'alvo_s': round(t, 2), 'atraso_s': round(max(passou, 0.0), 2), 'bloco': self.blk[2] if self.blk else None})

    def playx(self, *anims, run_time=1.0, **kw):
        """play com duração exata (sem o fator de ritmo do bloco)."""
        rs, self.rs = self.rs, 1.0
        try:
            return self.play(*anims, run_time=run_time, **kw)
        finally:
            self.rs = rs

    def pace(self, f):
        """Microbeat: espera até a fração f da fala do bloco corrente."""
        if self.blk is None:
            return
        t0, t1 = self.blk[0], self.blk[1]
        alvo = t0 + f*(t1 - t0)
        if alvo - self.vt > .02:
            self.wait(alvo - self.vt)

    def fecha(self, antecipa=False):
        """Fecha o bloco corrente esperando o fim da fala. antecipa=True (antes de clear/título): sai um pouco antes,
        durante o silêncio entre os blocos, para a transição não atrasar o primeiro evento do bloco seguinte."""
        if self.blk is None:
            return
        t0, t1, i, atraso = self.blk
        if antecipa:
            t1 -= min(1.2, DUR.get(i, {}).get('gap', 0.0))
        folga = t1 - self.vt
        self.blocos.append({'id': i, 'inicio': round(t0, 2), 'voz_s': round(t1 - t0, 2),
                            'animacao_s': round(self.vt - t0, 2), 'excesso_s': round(max(-folga, 0), 2),
                            'atraso_inicio_s': round(atraso, 2)})
        if folga > .02:
            self.wait(folga)
        self.blk = None
        if antecipa:
            self.rs = .6      # clear/título da transição rápidos: caem no silêncio entre os blocos

    def beat(self, target):
        self.qa_layout(str(target))
        if DUR:
            return
        remaining = self.t0 + (target - self.t0_old)*TS - self.vt
        self.marks[-1]['espera'] = round(self.marks[-1].get('espera',0)+max(remaining,0),2)
        if remaining > .01:
            self.wait(remaining)

    def qa_layout(self,tag):
        if os.getenv('QA_LAYOUT')!='1':return
        labels=[];geometries=[]
        def visit(m):
            if isinstance(m,(MathTex,Text,Paragraph)):
                if m.width>.6 and m.height>.1:labels.append(m)
                return
            if isinstance(m,VMobject) and m.has_points() and np.max(m.get_stroke_width())>.1 and np.max(m.get_stroke_opacity())>.05:
                geometries.append(m)
            for child in m.submobjects:visit(child)
        for m in self.live:visit(m)
        labels.append(self.heading)
        issues=[]
        def bounds(m,shrink=.035):
            return [float(m.get_left()[0]+shrink),float(m.get_right()[0]-shrink),
                    float(m.get_bottom()[1]+shrink),float(m.get_top()[1]-shrink)]
        def ident(m):return getattr(m,'tex_string',getattr(m,'text',type(m).__name__))
        boxes=[bounds(m) for m in labels]
        for i,(m,box) in enumerate(zip(labels,boxes)):
            if m is not self.heading and (box[0]<-7.2 or box[1]>7.2 or box[2]<-2.95 or box[3]>3.05):
                issues.append({'tipo':'safe_area','objeto':ident(m),'caixa':box})
            for j in range(i):
                b=boxes[j]
                if min(box[1],b[1])-max(box[0],b[0])>.06 and min(box[3],b[3])-max(box[2],b[2])>.06:
                    issues.append({'tipo':'textos','a':ident(m),'b':ident(labels[j])})
            for g in geometries:
                # Amostragem do traço, sem considerar preenchimentos translúcidos.
                if not g.has_points():continue
                pts=[g.point_from_proportion(t) for t in np.linspace(0,1,81)]
                if any(box[0]<p[0]<box[1] and box[2]<p[1]<box[3] for p in pts):
                    issues.append({'tipo':'traco_texto','texto':ident(m),'traco':type(g).__name__})
        self.layout_checks.append({'marco':tag,'tempo_local':float(self.vt),'problemas':issues})

    def particles(self, paths, color=E, speed=.2, count=2):
        group=VGroup()
        start=self.time
        for i,path in enumerate(paths):
            for j in range(count):
                dot=Dot(radius=.035,color=color).set_z_index(7)
                phase=(i*.137+j/count)%1
                dot.add_updater(lambda m,dt,p=path,f=phase:
                    m.move_to(p((f+(self.time-start)*speed)%1)))
                group.add(dot)
        return group

    def radial(self, origin, radius=3.2, n=18):
        origin=np.array(origin,dtype=float)
        lines=VGroup()
        paths=[]
        for theta in np.linspace(0,TAU,n,endpoint=False):
            u=np.array([np.cos(theta),np.sin(theta),0.])
            lines.add(Line(origin+.3*u,origin+radius*u,color=E,stroke_opacity=.23,stroke_width=1))
            for r in [.65,1.35,2.35]:
                if r<radius-.25:
                    length=min(.65,.68/r**2)
                    lines.add(vec(origin+r*u,origin+(r+length)*u,width=2,opacity=.65))
            paths.append(lambda a,u=u: origin+(.3+a*(radius-.3))*u)
        return VGroup(lines,self.particles(paths,speed=.11,count=2))

    def flow_cube(self,p,kind=1,extent=1.8):
        p=np.array(p,dtype=float)
        arrows=VGroup(); paths=[]
        if kind==0:
            for y in [-.7,0,.7]:
                a=p+[-extent,y,0]; b=p+[extent,y,0]
                arrows.add(vec(a,b,opacity=.8))
                paths.append(lambda t,a=a,b=b:interpolate(a,b,t))
        else:
            for ang in np.linspace(0,TAU,8,endpoint=False):
                u=np.array([np.cos(ang),np.sin(ang),0])
                a=p+.5*u; b=p+extent*u
                if kind<0:a,b=b,a
                arrows.add(vec(a,b,opacity=.75))
                paths.append(lambda t,a=a,b=b:interpolate(a,b,t))
        return VGroup(arrows,self.particles(paths,speed=.3))


    def opening(self):
        self.begin(0, "hook e abertura")
        R = 2.05
        p = self.origin = self.P = np.array([-3.8,.2,0])
        self.field = self.radial(p,2.45,18); self.q = charge(p)
        # ── hook: duas perguntas locais (divergente × rotacional) ──
        self.ancora("H01")
        self.show(self.field,self.q,t=1)
        self.ancora("H02")
        divs = math(r"\nabla\cdot\mathbf E",54,[-3.8,2.6,0])
        ask1 = text("o campo nasce aqui?",30).move_to([-3.8,-2.6,0])
        probe_ring = Circle(.32,color=WHITE,stroke_width=2.5).move_to(p+[1.25,.55,0])
        self.show(divs,ask1,probe_ring,t=.8)
        self.play(Indicate(probe_ring,color=WHITE,scale_factor=1.4),run_time=.9)
        self.ancora("H03")
        cr = np.array([3.8,.2,0])
        spin_field = self.vector_field(cr,rot=True)
        wheel = VGroup(Circle(.3,color=WHITE,stroke_width=2),
                       *[Line(ORIGIN,.3*np.array([np.cos(a),np.sin(a),0]),color=WHITE,stroke_width=2.5) for a in np.linspace(0,TAU,6,endpoint=False)]).move_to(cr)
        wheel.add_updater(lambda m,dt:m.rotate(dt*1.6,about_point=cr))
        curls = math(r"\nabla\times\mathbf F",54,[3.8,2.6,0])
        ask2 = text("o campo gira aqui?",30).move_to([3.8,-2.6,0])
        self.show(spin_field,wheel,curls,ask2,t=.9)
        self.beat(6)
        self.ancora("H04")
        big = text("Como leis sobre superfícies e caminhos inteiros\ndizem o que acontece em UM ponto?",30,width=11.5).move_to([0,-2.55,0])
        self.play(FadeOut(ask1),FadeOut(ask2),run_time=.4)
        self.live.remove(ask1); self.live.remove(ask2)
        self.show(big,t=.8)
        self.beat(10)
        gl = Circle(2.1,color=GEO,stroke_width=3).move_to(p)
        self.pace(.18); self.play(Create(gl),run_time=1.4); self.live.append(gl)
        self.pace(.45)
        sm = Circle(.45,color=GEO,stroke_width=3).move_to(probe_ring.get_center())
        self.play(ReplacementTransform(gl,sm),run_time=1.6); self.live.remove(gl); self.live.append(sm)
        self.pace(.75)
        pt = Dot(probe_ring.get_center(),radius=.07,color=WHITE)
        self.play(ReplacementTransform(sm,pt),run_time=1.2); self.live.remove(sm); self.live.append(pt)
        self.pace(.97); self.erase(pt,t=.3)
        self.ancora("G01")
        self.erase(spin_field,wheel,curls,divs,probe_ring,big,t=.6)
        self.t0 = self.vt; self.t0_old = 0
        # ── superfície gaussiana e dA ──
        self.surface = Circle(R,color=GEO,stroke_width=3,fill_color=GEO,fill_opacity=.06).move_to(p)
        self.show(self.surface,t=1.2)
        self.ancora("G02")
        th = .48; u = np.array([np.cos(th),np.sin(th),0]); tg = np.array([-u[1],u[0],0]); at = p+R*u
        glow = Arc(radius=R,start_angle=th-.15,angle=.3,color=DAVEC,stroke_width=22,stroke_opacity=.28).move_arc_center_to(p)
        patch = Arc(radius=R,start_angle=th-.13,angle=.26,color="#8E7CFF",stroke_width=10).move_arc_center_to(p)
        self.show(glow,patch)
        # dA nasce no próprio patch: rótulo ancorado por uma haste curta.
        dlab = math("dA",42,at+.4*u+1.15*tg)
        lead = Line(at+.04*u,dlab.get_bottom()+[0,-.03,0],color=DAVEC,stroke_width=1.8)
        dgroup = VGroup(lead,dlab)
        self.show(dgroup)
        self.beat(5)
        self.ancora("G03")
        nb = at+.14*tg; ntip = nb+.65*u
        normal = vec(nb,ntip,NORMAL,4.5)
        nlab = math(r"\hat{\mathbf n}",36,ntip+.42*tg+.2*u)
        self.show(normal,nlab)
        area = math(r"d\mathbf A=\hat{\mathbf n}\,dA",52,[3.7,1.0,0],width=6)
        self.build(area,{"dA":dlab,r"\hat{\mathbf n}":nlab},t=1.6)
        self.beat(9)
        self.ancora("G04")
        eb = at-.14*tg; etip = eb+.95*u
        ev = vec(eb,etip,E,4.8)
        elab = math(r"\mathbf E",44,etip+.45*u-.2*tg)
        self.show(ev,elab)
        eside = math(r"\mathbf E",52,[3.7,-.5,0])
        self.build(eside,{r"\mathbf E":elab},t=1.2)
        self.beat(13)
        self.rs = 1.0
        self.marco(119.9)
        c4 = np.array([3.7,-2.0,0]); al = ValueTracker(0)
        seg4 = Line(c4+[-1.0,0,0],c4+[1.0,0,0],color=DAVEC,stroke_width=5)
        n4 = vec(c4,c4+[0,.9,0],NORMAL,4)
        t4 = always_redraw(lambda:vec(c4,c4+1.1*np.array([np.sin(al.get_value()),np.cos(al.get_value()),0]),E,4.5))
        pj = always_redraw(lambda:DashedLine(c4+1.1*np.array([np.sin(al.get_value()),np.cos(al.get_value()),0]),c4+[0,1.1*np.cos(al.get_value()),0],color=MUTED,stroke_width=1.6))
        c4l = text("de frente: contribuição máxima",22,width=5).move_to(c4+[0,-.5,0])
        self.show(seg4,n4,t4,pj,c4l,t=.7)
        c4m = text("tangente: contribuição zero",22,width=5).move_to(c4+[0,-.5,0])
        self.marco(123.5)
        self.playx(al.animate.set_value(PI/2),FadeOut(c4l),FadeIn(c4m),run_time=3.3,rate_func=smooth)
        self.live.remove(c4l); self.live.append(c4m)
        self.marco(127.0)
        self.erase(seg4,n4,t4,pj,c4m,t=.4)
        self.erase(dgroup,nlab,elab,t=.3)
        integrand = math(r"\mathbf E\cdot d\mathbf A",60,[3.7,.35,0],width=6)
        self.merge([area,eside],integrand,1.3)
        self.beat(17)
        self.ancora("G05")
        patches = VGroup(*[Arc(radius=R,start_angle=a-.055,angle=.11,color="#8E7CFF",stroke_width=6).move_arc_center_to(p)
                           for a in np.linspace(0,TAU,12,endpoint=False)])
        stubs = VGroup(*[vec(p+R*np.array([np.cos(a),np.sin(a),0]),p+(R+.42)*np.array([np.cos(a),np.sin(a),0]),E,3.2)
                         for a in np.linspace(0,TAU,12,endpoint=False)])
        self.play(LaggedStart(*[AnimationGroup(Create(m),GrowArrow(s)) for m,s in zip(patches,stubs)],lag_ratio=.13),run_time=3)
        self.live.extend([patches,stubs])
        total = self.change(integrand,math(r"\sum\mathbf E\cdot d\mathbf A",58,[3.7,.35,0],width=6),t=1.2)
        self.beat(23)
        integral = self.change(total,math(r"\oint_S\mathbf E\cdot d\mathbf A",61,[3.7,.35,0],width=6),t=1.7)
        self.play(LaggedStart(*[Indicate(m,color=FLUX,scale_factor=1.08) for m in patches],lag_ratio=.1),run_time=2)
        self.beat(28)
        self.ancora("G06")
        self.erase(glow,patch,patches,stubs,integral,ev,normal)
        self.field.clear_updaters(recursive=True)
        self.local_cube = cube([2.8,.2,0],1.4)
        local = Dot(at,color=WHITE,radius=.07)
        neighborhood = Circle(.16,color=GEO,stroke_width=2).move_to(at)
        self.show(local,neighborhood,t=.4)
        self.play(self.surface.animate.scale(.55),self.field.animate.scale(.8),
                  local.animate.move_to([2.8,.2,0]),ReplacementTransform(neighborhood,self.local_cube),run_time=2.4)
        self.live.remove(neighborhood); self.live.append(self.local_cube)
        self.beat(35); self.clear(keep=(self.local_cube,))

    def gauss(self):
        self.begin(35, "gauss integral")
        self.title("CARGA ENVOLVIDA: DO DISCRETO AO CONTÍNUO")
        p = self.P
        self.play(Transform(self.local_cube,cube(p,2.3)),run_time=1.2)
        charges = VGroup(*[charge(p+[x,y,0],.075) for x,y in [(-.6,-.6),(.5,.6),(.5,-.5),(-.5,.6),(0,0)]])
        self.show(charges)
        qlabel = MathTex(r"Q_{\rm env}",font_size=54,color=Q).move_to([3.7,1.9,0]); self.show(qlabel)
        law = math(r"\oint_S\mathbf E\cdot d\mathbf A=\frac{Q_{\rm env}}{\varepsilon_0}",47,[3.2,.3,0],width=7.6); self.show(law)
        self.beat(43)
        self.ancora("G07")
        more = VGroup(*[Dot(p+[x,y,0],radius=.045,color=Q) for x in np.linspace(-.85,.85,5) for y in np.linspace(-.85,.85,5)])
        self.play(ReplacementTransform(charges,more),run_time=2); self.live.remove(charges); self.live.append(more)
        self.pace(0.35)
        density = VGroup(*[Dot(p+[x,y,0],radius=.023,color=Q) for x in np.linspace(-.9,.9,13) for y in np.linspace(-.9,.9,13)])
        self.play(ReplacementTransform(more,density),run_time=2); self.live.remove(more); self.live.append(density)
        self.pace(0.6)
        integral = MathTex(r"\int_V\rho\,dV",font_size=54).move_to(qlabel)
        assert len(qlabel[0]) == 4 and len(integral[0]) == 5,(len(qlabel[0]),len(integral[0]))
        integral[0][2].set_color(Q)
        for i in [1,4]:integral[0][i].set_color(GEO)
        self.play(TransformByGlyphMap(qlabel,integral,([0],[2]),([1,2,3],[]),([],[0,1,3,4])),run_time=2)
        self.live.remove(qlabel); self.live.append(integral)
        self.beat(52)
        self.ancora("G08")
        continuum = Polygon(p+[-1.2,-1.25,0],p+[1.2,-1.25,0],p+[1.2,1.25,0],p+[-1.2,1.25,0],stroke_width=0,fill_color=Q,fill_opacity=.1)
        self.show(continuum)
        # O Q_env da lei é substituído pela integral: ρ, dV e V nascem de cópias do rótulo.
        law2 = math(r"\oint_S\mathbf E\cdot d\mathbf A=\frac{1}{\varepsilon_0}\int_V\rho\,dV",48,[3.2,.3,0],width=7.6)
        isrc = {"V": None, r"\rho": None, "dV": None}
        self.morph(law,law2,2.0,src={r"\rho":integral[0][2],"dV":integral[0][4],"V":integral[0][1]})
        self.live.remove(law); self.live.append(law2); law = law2
        self.play(Indicate(integral,color=Q),run_time=1)
        self.beat(59)
        self.erase(integral)
        self.pace(0.5)
        question = text("Como isso vale ponto a ponto?",30).move_to([3.2,-1.65,0]); self.show(question)
        self.beat(63)
        # Zoom conceitual: marcar P, aproximar a região e deixar a geometria global recuar.
        self.pace(0.75)
        ring = Circle(.2,color=WHITE,stroke_width=2.5).move_to(p); mark = Dot(p,radius=.05,color=WHITE)
        plab = math("P",36,p+[.38,.34,0])
        self.show(ring,mark,plab,t=.7)
        self.play(Indicate(ring,color=WHITE,scale_factor=1.7),run_time=.9)
        self.beat(66)
        world = VGroup(density,continuum,self.local_cube)
        self.play(world.animate.scale(6,about_point=p).set_opacity(0),ring.animate.scale(4.2),
                  FadeOut(question),FadeOut(law),FadeOut(plab),FadeOut(mark),run_time=3,rate_func=smooth)
        for m in [density,continuum,self.local_cube,question,law,plab,mark]:
            if m in self.live:self.live.remove(m)
            self.remove(m)
        self.zoom_ring = ring; self.live.append(ring)
        self.beat(70)

    def divergence(self):
        self.begin(70, "divergente")
        self.title("FLUXO EM UM CUBO CENTRADO")
        side = 2.6; h = side/2; k = side/1.9; RX = 3.7; W = 6.6
        p = np.array([-3.4,.1,0]); self.local_p = p
        ISO = {"dx":WHITE,"dy":WHITE,"dz":WHITE,r"x+\frac{dx}{2}":WHITE,r"x-\frac{dx}{2}":WHITE}
        ring = getattr(self,'zoom_ring',None)
        # ── 1. eixo, P e o intervalo centrado ────────────────────────────────
        self.ancora("D01")
        axis = vec(p+[-3.1,0,0],p+[3.0,0,0],MUTED,1.5)
        point = Dot(p,radius=.08,color=WHITE)
        plab = math("P",38,p+[-.3,.45,0]); xlab = math(r"x_P=x",34,p+[.95,.5,0])
        anims = [FadeIn(m) for m in (axis,point,plab,xlab)]
        self.live.extend([axis,point,plab,xlab])
        if ring is not None and ring in self.live:
            anims.append(FadeOut(ring)); self.live.remove(ring)
        self.play(*anims,run_time=1.3)
        guide = text("Primeiro, um intervalo centrado em P",28,width=6.6).move_to([RX,1.2,0]); self.show(guide)
        self.at(5)
        self.pace(0.45)
        seg = Line(p+[-h,0,0],p+[h,0,0],color=GEO,stroke_width=6)
        ticks = VGroup(*[Line(p+[s*h,-.18,0],p+[s*h,.18,0],color=GEO,stroke_width=3.5) for s in (-1,1)])
        total = BraceBetweenPoints(p+[-h,-.26,0],p+[h,-.26,0],DOWN,color=GEO)
        dxl = math("dx",46,p+[0,-1.0,0],iso=ISO)
        self.show(seg,ticks,total,dxl)
        self.at(9)
        # ── 2. duas metades dx/2 → extremos x ± dx/2 ─────────────────────────
        self.ancora("D02")
        hb = VGroup(BraceBetweenPoints(p+[-h,-.26,0],p+[0,-.26,0],DOWN,color=GEO),
                    BraceBetweenPoints(p+[0,-.26,0],p+[h,-.26,0],DOWN,color=GEO))
        hl = VGroup(*[math(r"\frac{dx}{2}",38,p+[s*h/2,-1.25,0]) for s in (-1,1)])
        self.play(ReplacementTransform(total,hb),*[TransformFromCopy(dxl,m) for m in hl],FadeOut(dxl),run_time=1.4)
        for m in (total,dxl):
            self.live.remove(m)
        self.live.extend([hb,hl])
        self.at(13)
        self.pace(0.55)
        ends = VGroup(math(r"x-\frac{dx}{2}",42,p+[-h,-2.35,0]),math(r"x+\frac{dx}{2}",42,p+[h,-2.35,0]))
        assert all(len(m[0]) == 4 for m in hl) and all(len(m[0]) == 6 for m in ends),([len(m[0]) for m in hl],[len(m[0]) for m in ends])
        half_map = [([0],[2]),([1],[3]),([2],[4]),([3],[5]),([],[0,1])]
        self.play(*[TransformByGlyphMap(hl[i],ends[i],*half_map) for i in [0,1]],run_time=1.3)
        self.live.remove(hl); self.remove(hl); self.add(ends); self.live.append(ends)
        self.at(17)
        # ── 3. o intervalo vira cubo; dimensões nas arestas ──────────────────
        self.ancora("D03")
        cb = self.local_cube = cube(p,side)
        self.play(ReplacementTransform(seg,cb),FadeOut(hb),FadeOut(ticks),FadeOut(guide),FadeOut(point),
                  FadeOut(axis),FadeOut(xlab),plab.animate.move_to(p+[.32,-.32,0]),run_time=1.7)
        for m in (seg,hb,ticks,guide,point,axis,xlab):
            self.live.remove(m)
        self.live.append(cb)
        e_dx = Line(cube_point(p,side,-1,-1,-1),cube_point(p,side,1,-1,-1),color=WHITE,stroke_width=4)
        e_dy = Line(cube_point(p,side,1,-1,1),cube_point(p,side,1,1,1),color=WHITE,stroke_width=4)
        e_dz = Line(cube_point(p,side,1,1,-1),cube_point(p,side,1,1,1),color=WHITE,stroke_width=4)
        l_dx = math("dx",38,p+[0,-1.32*h-.34,0],iso=ISO); l_dy = math("dy",38,p+[1.3*h,1.45*h+.05,0],iso=ISO)
        l_dz = math("dz",38,p+[1.58*h+.3,.2*h,0],iso=ISO)
        self.show(e_dx,l_dx,t=.5); self.show(e_dy,l_dy,t=.5); self.show(e_dz,l_dz,t=.5)
        self.at(25)
        # ── 4. a face perpendicular a x: dA_x = dy dz ────────────────────────
        self.pace(0.45)
        cR = face_center(p,side,0,1); cL = face_center(p,side,0,-1)
        self.play(cb[1].animate.set_fill(GEO,.4),cb[0].animate.set_fill(GEO,.04),run_time=.7)
        l_dAx = self.tag("dA_x",34,cR+[-.12,.42*k,0]); self.show(l_dAx,t=.5)
        dAx = math(r"dA_x=dy\,dz",54,[RX,1.5,0],width=W,iso=ISO)
        self.build(dAx,{"dA_x":l_dAx[0],"dy":l_dy,"dz":l_dz},t=1.5)
        self.pulse(cb[1],color=DAVEC,t=.8)
        self.at(33)
        # ── 5. normais externas ──────────────────────────────────────────────
        self.ancora("D04")
        ny = -.55*k
        nR = vec(cR+[0,ny,0],cR+[.9*k,ny,0],NORMAL,4.5).set_z_index(9)
        nL = vec(cL+[0,ny,0],cL+[-.9*k,ny,0],NORMAL,4.5).set_z_index(9)
        nRl = math(r"\hat{\mathbf n}_+",38,cR+[1.45*k,ny+.05,0]); nLl = math(r"\hat{\mathbf n}_-",38,cL+[-1.45*k,ny+.05,0])
        self.show(nR,nRl,t=.6)
        call = text("normal externa",25).move_to(cR+[1.45*k,ny-.45,0])
        lead = Line(cR+[.75*k,ny-.3,0],cR+[.55*k,ny-.06,0],color=WHITE,stroke_width=1.5)
        self.show(call,lead,t=.5)
        eqp = math(r"\hat{\mathbf n}_+=+\hat{\mathbf x}",52,[RX,.3,0],width=W)
        self.build(eqp,{r"\hat{\mathbf n}_+":nRl},t=1.2)
        self.at(40)
        self.play(cb[0].animate.set_fill(GEO,.4),cb[1].animate.set_fill(GEO,.04),run_time=.6)
        self.pace(0.5)
        self.show(nL,nLl,t=.6)
        eqm = math(r"\hat{\mathbf n}_-=-\hat{\mathbf x}",52,[RX,-.8,0],width=W)
        self.build(eqm,{r"\hat{\mathbf n}_-":nLl},t=1.2)
        opp = text("normais externas opostas",28).move_to([RX,2.55,0]); self.show(opp)
        self.at(47)
        self.ancora("D05")
        self.erase(call,lead,eqp,eqm,opp,t=.5)
        self.play(dAx.animate.scale(.72).move_to([RX,2.6,0]),run_time=.6)
        # ── 6. fluxo pela face direita: dΦ = E·dA → E_x(x + dx/2) dy dz ─────
        self.erase(e_dx,e_dy,e_dz,l_dx,l_dy,l_dz,l_dAx,t=.4)
        self.play(cb[1].animate.set_fill(GEO,.4),cb[0].animate.set_fill(GEO,.04),run_time=.6)
        eb = cR+[.2*k,.35*k,0]; et = eb+[1.05*k,.55*k,0]
        e_vec = vec(eb,et,E,4.5); e_cmp = vec(eb,eb+[1.05*k,0,0],E,6.5)
        e_drop = DashedLine(et,[et[0],eb[1],0],color=E,stroke_width=1.8)
        e_lab = math(r"\mathbf E",40,et+[.34,.1,0]); ex_lab = math(r"E_x",38,eb+[.55*k,-.34,0])
        self.show(e_vec,e_lab,t=.6); self.show(e_drop,e_cmp,ex_lab,t=.8)
        L1 = math(r"d\Phi=\mathbf E\cdot d\mathbf A",54,[RX,1.0,0],width=W,iso=ISO)
        self.build(L1,{r"\mathbf E":e_lab},t=1.2)
        self.at(53)
        self.pace(0.4)
        L2 = self.change(L1,math(r"d\Phi_{x,+}=\mathbf E\cdot\hat{\mathbf x}\,dy\,dz",52,[RX,1.0,0],width=W,iso=ISO),
                         t=1.5,src={r"\hat{\mathbf x}":nRl,"dy":dAx.get_part_by_tex("dy"),"dz":dAx.get_part_by_tex("dz")})
        self.at(59)
        self.pace(0.65)
        L3 = self.change(L2,math(r"d\Phi_{x,+}=E_x\,dy\,dz",52,[RX,1.0,0],width=W,iso=ISO),t=1.4,src={"E_x":ex_lab})
        self.pulse(e_cmp,ex_lab,color=E,t=.8)
        self.at(65)
        self.ancora("D06")
        L4 = self.change(L3,math(r"d\Phi_{x,+}=E_x\left(\text{face}\right)dy\,dz",52,[RX,1.0,0],width=W,
                                  iso={**ISO,r"\text{face}":WHITE}),t=1.2)
        self.at(69)
        self.pace(0.5)
        L5 = self.change(L4,math(r"d\Phi_{x,+}=E_x\left(x+\frac{dx}{2}\right)dy\,dz",50,[RX,1.0,0],width=W+.2,iso=ISO),
                         t=2.0,src={r"x+\frac{dx}{2}":ends[1]})
        self.play(Indicate(ends[1],color=WHITE),Indicate(cb[1],color=GEO),run_time=.9)
        self.at(76)
        self.ancora("D07")
        self.erase(e_vec,e_cmp,e_drop,e_lab,ex_lab,nR,nRl,dAx,t=.5)
        self.play(L5.animate.move_to([RX,2.4,0]).scale(.86),run_time=.8)
        # ── 7. a face esquerda: sinal negativo e x − dx/2 ────────────────────
        self.play(cb[0].animate.set_fill(GEO,.4),cb[1].animate.set_fill(GEO,.04),run_time=.5)
        eb2 = cL+[-1.25*k,.35*k,0]; et2 = eb2+[1.05*k,.55*k,0]
        e_vec2 = vec(eb2,et2,E,4.5); e_cmp2 = vec(eb2,eb2+[1.05*k,0,0],E,6.5)
        e_drop2 = DashedLine(et2,[et2[0],eb2[1],0],color=E,stroke_width=1.8)
        e_lab2 = math(r"\mathbf E",40,et2+[-.2,.38,0]); ex_lab2 = math(r"E_x",38,eb2+[.5*k,-.34,0])
        self.show(e_vec2,e_lab2,e_drop2,e_cmp2,ex_lab2,t=.8)
        self.pace(0.3)
        M1 = math(r"d\Phi_{x,-}=\mathbf E\cdot\left(-\hat{\mathbf x}\right)dy\,dz",52,[RX,1.1,0],width=W,iso=ISO)
        self.build(M1,{r"\hat{\mathbf x}":nLl,r"\mathbf E":e_lab2},t=1.4)
        self.at(83)
        self.pace(0.55)
        M2 = self.change(M1,math(r"d\Phi_{x,-}=-E_x\,dy\,dz",52,[RX,1.1,0],width=W,iso=ISO),t=1.4,src={"E_x":ex_lab2})
        self.play(Indicate(nL,color=NORMAL),run_time=.7)
        self.at(89)
        self.pace(0.8)
        M3 = self.change(M2,math(r"d\Phi_{x,-}=-E_x\left(x-\frac{dx}{2}\right)dy\,dz",50,[RX,1.1,0],width=W+.2,iso=ISO),
                         t=1.6,src={r"x-\frac{dx}{2}":ends[0]})
        self.play(Indicate(ends[0],color=WHITE),Indicate(cb[0],color=GEO),run_time=.9)
        self.at(96)
        self.ancora("D08")
        self.erase(e_vec2,e_cmp2,e_drop2,e_lab2,ex_lab2,nL,nLl,t=.5)
        self.play(M3.animate.move_to([RX,.1,0]).scale(.86),run_time=.8)
        # ── 8. fluxo líquido nas faces x (termos copiados das duas faces) ────
        self.erase(ends,t=.4)
        self.play(cb[0].animate.set_fill(GEO,.17),cb[1].animate.set_fill(GEO,.17),run_time=.4)
        self.pace(0.4)
        net = math(r"d\Phi_x=\left[E_x\left(x+\frac{dx}{2}\right)-E_x\left(x-\frac{dx}{2}\right)\right]dy\,dz",48,[0,-2.3,0],width=13,iso=ISO)
        pa_ = net.get_part_by_tex(r"x+\frac{dx}{2}"); pb_ = net.get_part_by_tex(r"x-\frac{dx}{2}")
        skeleton = [q for q in net if q is not pa_ and q is not pb_]
        self.play(*[FadeIn(q) for q in skeleton],run_time=1.0)
        self.play(TransformFromCopy(M3.get_part_by_tex(r"x-\frac{dx}{2}"),pb_),FadeOut(M3),run_time=1.2)
        self.play(TransformFromCopy(L5.get_part_by_tex(r"x+\frac{dx}{2}"),pa_),FadeOut(L5),run_time=1.2)
        self.add(net); self.live.remove(L5); self.live.remove(M3); self.live.append(net)
        self.at(103)
        # ── 9. diferença finita → derivada parcial (mini gráfico) ────────────
        self.ancora("D09")
        net2 = self.change(net,math(r"d\Phi_x=\frac{E_x\left(x+\frac{dx}{2}\right)-E_x\left(x-\frac{dx}{2}\right)}{dx}\,dx\,dy\,dz",
                                    48,[0,-2.25,0],width=13,iso=ISO),t=1.6)
        self.pace(0.35)
        ax = Axes(x_range=[0,3.4,1],y_range=[0,5.2,1],x_length=5.0,y_length=2.9,tips=False,
                  axis_config={"color":MUTED,"stroke_width":1.8,"include_ticks":False}).move_to([RX+.4,.85,0])
        f = lambda x:.35+.25*x+.32*x**2
        curve = ax.plot(f,x_range=[.05,3.35],color=E,stroke_width=4.5)
        xl = math("x",34,ax.c2p(3.5,0)+[.1,-.05,0]); yl = math(r"E_x",34,ax.c2p(0,5.5))
        note = text("y e z fixos",24).move_to(ax.c2p(.75,4.5))
        self.show(ax,curve,xl,yl,note,t=1.2)
        self.ancora("D10")
        x0 = 1.7; hv = ValueTracker(.85)
        A = lambda:ax.c2p(x0-hv.get_value(),f(x0-hv.get_value()))
        B = lambda:ax.c2p(x0+hv.get_value(),f(x0+hv.get_value()))
        def secant():
            a,b = A(),B(); d = (b-a)/np.linalg.norm(b-a)
            return Line(a-1.5*d,b+1.5*d,color=WHITE,stroke_width=2.6)
        sec = always_redraw(secant)
        da = always_redraw(lambda:Dot(A(),radius=.07,color=WHITE)); db = always_redraw(lambda:Dot(B(),radius=.07,color=WHITE))
        ga = always_redraw(lambda:DashedLine(A(),ax.c2p(x0-hv.get_value(),0),color=MUTED,stroke_width=1.4))
        gb = always_redraw(lambda:DashedLine(B(),ax.c2p(x0+hv.get_value(),0),color=MUTED,stroke_width=1.4))
        ta = math(r"x-\frac{dx}{2}",28,ax.c2p(x0-.85,0)+[0,-.4,0]); tb = math(r"x+\frac{dx}{2}",28,ax.c2p(x0+.85,0)+[0,-.4,0])
        fade = lambda m,sign:m.add_updater(lambda mm:mm.move_to(ax.c2p(x0+sign*hv.get_value(),0)+[0,-.4,0]).set_opacity(float(np.clip((hv.get_value()-.3)/.2,0,1))))
        fade(ta,-1); fade(tb,1)
        self.show(ga,gb,da,db,sec,ta,tb,t=1.2)
        slope = text("inclinação média\nentre as duas faces",24,width=3.2).move_to([RX+1.55,2.45,0])
        self.show(slope,t=.5)
        self.at(113)
        self.rs = 1.0
        self.marco(347.7)
        self.playx(Indicate(sec,color=WHITE,scale_factor=1.0),run_time=.9)
        self.marco(349.5)
        self.playx(hv.animate.set_value(.04),run_time=6.0,rate_func=smooth)
        tangent = text("dx → 0:\na secante vira tangente",24,width=3.2).move_to([RX+1.55,2.45,0])
        self.playx(Transform(slope,tangent),run_time=.7)
        self.marco(356.1)
        self.rs = .75
        net3 = self.change(net2,math(r"d\Phi_x=\frac{\partial E_x}{\partial x}\,dx\,dy\,dz",54,[0,-2.25,0],iso=ISO),t=1.8)
        self.playx(Indicate(net3,color=WHITE),run_time=.9)
        self.at(122)
        self.ancora("D11")
        self.rs = 1.0
        self.marco(361.0)
        self.playx(Indicate(note,color=WHITE),run_time=1.0)
        self.at(128)
        self.marco(369.2)
        self.erase(ga,gb,da,db,sec,ta,tb,ax,curve,xl,yl,note,slope,t=.6)
        # ── 10. dV = dx dy dz ────────────────────────────────────────────────
        self.ancora("D12")
        dxyz = VGroup(*[next(q for q in net3 if q.tex_string == kk) for kk in ("dx","dy","dz")])
        br = Brace(dxyz,UP,color=GEO); dvl = math(r"dV=dx\,dy\,dz",46,br.get_top()+[0,.5,0],iso=ISO)
        self.rs = 1.0
        self.marco(371.4)
        self.show(br,dvl,t=.9)
        self.marco(377.0)
        self.playx(cb[0].animate.set_fill(GEO,.3),cb[1].animate.set_fill(GEO,.3),run_time=.5)
        self.at(134)
        self.marco(377.6)
        self.erase(br,dvl,t=.4)
        R1 = [RX,2.2,0]
        self.marco(378.0)
        net4 = self.change(net3,math(r"d\Phi_x=\frac{\partial E_x}{\partial x}dV",52,R1,width=W),t=1.8)
        self.at(140)
        # ── 11. y e z: o mesmo cubo, outros pares de faces ───────────────────
        self.ancora("D13")
        rows = [net4]
        for axis_i,(sym,ypos) in enumerate([("y",.75),("z",-.7)],start=1):
            self.pace(.3 if axis_i == 1 else .65)
            grp = self.pair(p,side,axis_i)
            tips = [face_center(p,side,axis_i,s)+s*(.55 if axis_i == 2 else .8)*k*CUBE_BASES[axis_i]/np.linalg.norm(CUBE_BASES[axis_i]) for s in (-1,1)]
            offs = [(-.9,-.15),(.8,.15)] if axis_i == 1 else [(.0,-.42),(0,.42)]
            tl = VGroup(*[math(("+" if s > 0 else "-")+r"\hat{\mathbf "+sym+"}",34,tip+[o[0],o[1],0]) for s,tip,o in zip((-1,1),tips,offs)])
            self.play(FadeIn(grp),FadeIn(tl),run_time=.8)
            row = math(r"d\Phi_"+sym+r"=\frac{\partial E_"+sym+r"}{\partial "+sym+r"}dV",52,[RX,ypos,0],width=W)
            self.play(FadeIn(row,shift=.12*UP),run_time=1.1); self.live.append(row); rows.append(row)
            self.at(140+9*axis_i)
            self.play(FadeOut(grp),FadeOut(tl),run_time=.5)
        self.ancora("D14")
        sumline = math(r"d\Phi=d\Phi_x+d\Phi_y+d\Phi_z",50,[RX,-1.95,0],width=W)
        self.build(sumline,{r"d\Phi_x":rows[0].get_part_by_tex(r"d\Phi_x"),r"d\Phi_y":rows[1].get_part_by_tex(r"d\Phi_y"),
                            r"d\Phi_z":rows[2].get_part_by_tex(r"d\Phi_z")},t=1.6)
        self.at(162)
        self.pace(0.45)
        cap14 = text("três taxas de saída, não três componentes",30,width=6.5).move_to([RX,-2.7,0]); self.show(cap14)
        self.ancora("D15")
        self.erase(cap14,t=.3)
        summed = math(r"d\Phi=\left(\frac{\partial E_x}{\partial x}+\frac{\partial E_y}{\partial y}+\frac{\partial E_z}{\partial z}\right)dV",
                      48,[RX,.5,0],width=W+.3)
        self.merge(rows+[sumline],summed,2.0)
        self.at(168)
        # ── 12. só agora o nome: divergente ──────────────────────────────────
        self.pace(0.5)
        pd = summed.get_part_by_tex(r"d\Phi"); pv = summed.get_part_by_tex("dV")
        brace = BraceBetweenPoints([pd.get_right()[0]+.5,summed.get_bottom()[1]-.08,0],[pv.get_left()[0]-.05,summed.get_bottom()[1]-.08,0],DOWN,color=GEO)
        dlab = VGroup(text("divergente de",27),math(r"\mathbf E",38)).arrange(RIGHT,buff=.2).next_to(brace,DOWN,buff=.14)
        cyc = [self.pair(p,side,a_,.28) for a_ in range(3)]
        self.play(FadeIn(brace),FadeIn(dlab),run_time=.8)
        for g in cyc:
            self.play(FadeIn(g),run_time=.35); self.play(FadeOut(g),run_time=.35)
        self.live.extend([brace,dlab])
        div = self.change(summed,math(r"d\Phi=\left(\nabla\cdot\mathbf E\right)dV",56,[RX,.5,0],width=W),t=1.8)
        self.erase(brace,dlab,t=.4)
        self.title("DIVERGENTE: FLUXO LÍQUIDO POR VOLUME")
        div = self.change(div,math(r"\nabla\cdot\mathbf E=\frac{d\Phi}{dV}",62,[RX,.5,0],width=W),t=1.4)
        self.at(180)
        self.ancora("D16")
        lim = self.change(div,math(r"\nabla\cdot\mathbf E=\lim_{\Delta V\to0}\frac{1}{\Delta V}\oint_{\partial V}\mathbf E\cdot d\mathbf A",48,[RX,.9,0],width=W+.2))
        cap_a = text("fluxo líquido pela fronteira",26,width=6).move_to([RX,-.35,0]); self.pace(.3); self.show(cap_a)
        cap_b = text("dividido pelo volume",26,width=6).move_to([RX,-1.0,0]); self.pace(.52); self.show(cap_b)
        cap_c = text("volume encolhendo até o ponto",26,width=6).move_to([RX,-1.65,0]); self.pace(.7); self.show(cap_c)
        self.play(self.local_cube.animate.scale(.4),run_time=1.6); self.play(self.local_cube.animate.scale(2.5),run_time=1.0)
        self.pace(.96); self.erase(cap_a,cap_b,cap_c,t=.3)
        self.at(186)
        self.ancora("D17")
        self.erase(lim)
        # ── 13. interpretação: o mesmo cubo em três regimes ──────────────────
        self.erase(plab,t=.4)
        prev = None; value = None; cap = None
        for kind,sign,label,when in [(1,'>','Fluxo líquido saindo',194),(-1,'<','Fluxo líquido entrando',200),(0,'=','Fluxo líquido local nulo',206)]:
            self.pace({1:.05,-1:.35,0:.65}[kind])
            f_ = self.flow_cube(p,kind,1.55*k)
            nv = math(r"\nabla\cdot\mathbf E"+sign+'0',60,[RX,1.0,0]); nc = text(label,29).move_to([RX,-.1,0])
            if prev is None:
                self.show(f_,nv,nc,t=.5); value,cap = nv,nc
            else:
                self.live.remove(prev); prev[1].clear_updaters(recursive=True)
                self.play(ReplacementTransform(prev[0],f_[0]),FadeOut(prev[1]),FadeIn(f_[1]),run_time=1.0)
                self.live.append(f_)
                value = self.change(value,nv,t=.9)
                self.play(FadeOut(cap),FadeIn(nc),run_time=.5); self.live.remove(cap); self.live.append(nc); cap = nc
            prev = f_
            if kind == 0:
                self.ancora("D18")
                warn = math(r"\nabla\cdot\mathbf E=0\;\not\Rightarrow\;\mathbf E=0",46,[RX,-1.5,0],width=W+.4); self.show(warn,t=.5)
            self.at(when)
        self.fecha(True)
        self.clear(keep=(self.local_cube,))

    def theorem(self):
        self.begin(155, "teorema da divergência")
        self.ancora("T01")
        self.clear(); self.title("UMA INTERFACE, DUAS NORMAIS EXTERNAS")
        RX = 3.7; W = 6.6; side = 2.2; k = side/1.6; y0 = .3
        pa = np.array([-4.5,y0,0]); pb = np.array([-2.3,y0,0])
        a = cube(pa,side); b = cube(pb,side)
        self.show(a,b)
        la = math("A",44,[-4.6,2.15,0]); lb = math("B",44,[-2.2,2.15,0]); self.show(la,lb,t=.4)
        interface = a[1].copy().set_fill(GEO,.5).set_stroke(FLUX,4)
        assert np.allclose(a[1].get_vertices(),b[0].get_vertices())
        self.show(interface)
        ca = np.array([-3.4,y0,0])
        self.pace(0.5)
        nA = vec(ca+[0,.3*k,0],ca+[.9*k,.3*k,0],NORMAL,4.5); nB = vec(ca+[0,-.3*k,0],ca+[-.9*k,-.3*k,0],NORMAL,4.5)
        self.show(nA,nB)
        tA = self.tag(r"\hat{\mathbf n}_A",38,ca+[1.35*k,.5*k,0]); tB = self.tag(r"\hat{\mathbf n}_B",38,ca+[-1.35*k,-.55*k,0])
        self.show(tA,tB)
        same = text("A mesma face é saída para um volume\ne entrada para o vizinho",28).move_to([RX,2.3,0]); self.show(same)
        self.at(6)
        self.ancora("T02")
        fy = y0+1.0
        field = vec([-6.7,fy,0],[-.7,fy,0],E,4.5)
        flow = self.particles([lambda t:np.array([-6.7+6.0*t,fy,0])],speed=.22,count=4)
        self.show(field,flow)
        eqa = math(r"\hat{\mathbf n}_A=+\hat{\mathbf x}",52,[RX,1.1,0],width=W)
        eqb = math(r"\hat{\mathbf n}_B=-\hat{\mathbf x}",52,[RX,-.1,0],width=W)
        self.build(eqa,{r"\hat{\mathbf n}_A":tA[0]},t=1.1); self.build(eqb,{r"\hat{\mathbf n}_B":tB[0]},t=1.1)
        self.at(14)
        self.erase(eqa,eqb,t=.4)
        self.pace(0.4)
        pa_ = math(r"\Phi_A=+\mathbf E\cdot d\mathbf A",54,[RX,1.1,0],width=W,iso={r"\Phi_A":FLUX})
        pb_ = math(r"\Phi_B=-\mathbf E\cdot d\mathbf A",54,[RX,-.1,0],width=W,iso={r"\Phi_B":FLUX})
        self.show(pa_,pb_)
        self.play(Indicate(nA,color=NORMAL),Indicate(pa_,color=FLUX),run_time=.9)
        self.play(Indicate(nB,color=NORMAL),Indicate(pb_,color=FLUX),run_time=.9)
        self.at(24)
        self.pace(0.75)
        both = math(r"\left(+\mathbf E\cdot d\mathbf A\right)+\left(-\mathbf E\cdot d\mathbf A\right)",50,[RX,.5,0],width=W+.4)
        self.merge([pa_,pb_],both,1.6)
        zero = self.change(both,math(r"\left(+\mathbf E\cdot d\mathbf A\right)+\left(-\mathbf E\cdot d\mathbf A\right)=0",50,[RX,.5,0],width=W+.4),t=1.2)
        self.play(Indicate(interface,color=FLUX),run_time=.8)
        self.at(34)
        self.ancora("T03")
        self.clear()
        # ── 2 → 4 → 8 células: cada interface interna acende, mostra o par de normais e cancela ──
        step = 1.5; h = step/2
        pos = [np.array([-5.7+(i%4)*step,-.3+(i//4)*step,0]) for i in range(8)]
        groups = []; cells = VGroup()
        for count in [2,4,8]:
            new = VGroup(*[cube(pos[i],step) for i in range(len(cells),count)])
            self.show(new,t=.8)
            groups.append(new); cells.add(*new)
        self.at(40)
        self.pace(0.4)
        marks = VGroup()
        for j in range(2):
            for i in range(3):
                fc = face_center(pos[j*4+i],step,0,1)
                hl = face(pos[j*4+i],step,0,1,FLUX,.5,3)
                pr = VGroup(vec(fc+[0,.1,0],fc+[.4,.1,0],NORMAL,3.5),vec(fc+[0,-.1,0],fc+[-.4,-.1,0],NORMAL,3.5))
                marks.add(VGroup(hl,pr))
        for i in range(4):
            fc = face_center(pos[i],step,2,1)
            hl = face(pos[i],step,2,1,FLUX,.5,3)
            pr = VGroup(vec(fc+[.1,0,0],fc+[.1,.4,0],NORMAL,3.5),vec(fc+[-.1,0,0],fc+[-.1,-.4,0],NORMAL,3.5))
            marks.add(VGroup(hl,pr))
        self.play(LaggedStart(*[FadeIn(m) for m in marks],lag_ratio=.18),run_time=3.2)
        self.play(*[m.animate.set_opacity(.12) for m in marks],run_time=1.2)
        self.live.append(marks)
        self.ancora("T04")
        corners = [cube_point(q,step,i,j,kk)[:2] for q in pos for i in (-1,1) for j in (-1,1) for kk in (-1,1)]
        hull = Polygon(*[[x,y,0] for x,y in convex_hull(corners)],color=FLUX,stroke_width=4)
        self.play(cells.animate.set_opacity(.25),Create(hull),run_time=1.2); self.live.append(hull)
        fi = face_center(pos[5],step,0,1)
        a1 = text("faces internas: cancelam",22).move_to([-3.4,2.85,0])
        l1 = Line(a1.get_bottom()+[0,-.05,0],fi+[0,.55,0],color=WHITE,stroke_width=1.3)
        a2 = text("só a fronteira permanece",22).move_to([-3.4,-1.95,0])
        l2 = Line(a2.get_top()+[0,.05,0],[-3.4,-1.3,0],color=FLUX,stroke_width=1.3)
        caption = VGroup(a1,l1,a2,l2); self.show(caption)
        self.at(56)
        # ── matemática: soma sobre células → integral de volume ──
        self.ancora("T05")
        vol = math(r"\sum_{\text{c\'elulas}}\left(\nabla\cdot\mathbf E\right)\Delta V",48,[RX,.9,0],width=W); self.show(vol)
        vol = self.change(vol,math(r"\int_V\nabla\cdot\mathbf E\,dV",60,[RX,.9,0],width=W),t=1.5)
        self.play(Indicate(cells,color=GEO),run_time=.9)
        self.at(68)
        # ── soma sobre faces externas → fluxo na fronteira ──
        self.pace(0.5)
        surf = math(r"\sum_{\text{faces externas}}\mathbf E\cdot d\mathbf A",48,[RX,-.9,0],width=W); self.show(surf)
        surf = self.change(surf,math(r"\oint_S\mathbf E\cdot d\mathbf A",60,[RX,-.9,0],width=W),t=1.5)
        self.play(Indicate(hull,color=FLUX),run_time=.9)
        self.at(80)
        self.ancora("T06")
        self.erase(caption,*groups,hull,marks)
        theorem = math(r"\oint_S\mathbf E\cdot d\mathbf A=\int_V\nabla\cdot\mathbf E\,dV",62,[0,.4,0])
        self.merge([surf,vol],theorem,1.8)
        self.at(90)
        self.fecha(True)
        self.clear(); self.flux = math(r"\oint_S\mathbf E\cdot d\mathbf A",58,[0,1.3,0]); self.show(self.flux,t=.3)

    def local_gauss(self):
        self.begin(205, "gauss diferencial")
        self.title("O MESMO FLUXO, DUAS LEITURAS")
        self.ancora("L01")
        tags = VGroup(text("TEOREMA DA DIVERGÊNCIA",24).move_to([-3.7,2.25,0]),
                      text("LEI DE GAUSS",24).move_to([3.7,2.25,0])); self.show(tags)
        left = math(r"\oint_S\mathbf E\cdot d\mathbf A",43,[-3.7,.5,0],width=6.5)
        right = math(r"\oint_S\mathbf E\cdot d\mathbf A",43,[3.7,.5,0],width=6.5)
        self.play(TransformFromCopy(self.flux,left),TransformFromCopy(self.flux,right),run_time=1.2)
        self.live.extend([left,right]); self.erase(self.flux)
        self.pace(0.35)
        left = self.change(left,math(r"\int_V\nabla\cdot\mathbf E\,dV",51,[-3.7,.5,0],width=6.5))
        right = self.change(right,math(r"\frac{1}{\varepsilon_0}\int_V\rho\,dV",51,[3.7,.5,0],width=6.5))
        same = text("Duas leituras da mesma grandeza",28).move_to([0,-1.1,0]); self.show(same)
        self.beat(216)
        self.ancora("L02")
        self.erase(tags,same)
        equality = math(r"\int_V\nabla\cdot\mathbf E\,dV=\int_V\frac{\rho}{\varepsilon_0}dV",55,[0,.9,0])
        self.merge([left,right],equality,1.8)
        self.beat(222)
        self.ancora("L03")
        equality = self.change(equality,math(r"\int_V\left(\nabla\cdot\mathbf E-\frac{\rho}{\varepsilon_0}\right)dV=0",55,[0,.9,0]),t=1.5)
        self.pace(0.35)
        vol = cube([-3.8,-1.4,0],1.1); self.show(vol)
        note = text("Qualquer volume regular apropriado",27).move_to([2.1,-1.4,0]); self.show(note)
        self.play(vol.animate.scale(.2,about_point=[-3.8,-1.4,0]),run_time=4)
        self.beat(231)
        self.ancora("L04")
        self.erase(vol,note)
        equality = self.change(equality,math(r"\nabla\cdot\mathbf E=\frac{\rho}{\varepsilon_0}",76,[0,.6,0]),t=1.6)
        self.title("LEI DE GAUSS — FORMA DIFERENCIAL")
        box = SurroundingRectangle(equality,color=GEO,buff=.3); self.show(box)
        self.pace(0.6)
        positive = math(r"\rho>0\Rightarrow\nabla\cdot\mathbf E>0",43,[0,-1.2,0]); self.show(positive)
        self.beat(239)
        self.pace(0.8)
        positive = self.change(positive,math(r"\rho<0\Rightarrow\nabla\cdot\mathbf E<0",43,[0,-1.2,0]))
        self.fecha(True)
        self.beat(245); self.clear()

    def example(self):
        self.begin(245, "exemplo kappa r")
        self.title("UM CAMPO QUE CRESCE COM A POSIÇÃO")
        self.ancora("K01")
        base=np.array([-4,.1,0]);progress=ValueTracker(.5)
        arrows=VGroup(*[vec(base+[x,y,0],base+1.25*np.array([x,y,0]),E,2.8,.5) for x in [-1.6,-.8,0,.8,1.6] for y in [-1.4,-.7,0,.7,1.4] if abs(x)+abs(y)>.1])
        probe=always_redraw(lambda:Dot(base+[progress.get_value(),.4,0],radius=.075,color=Q))
        arrow=always_redraw(lambda:vec(base+[progress.get_value(),.4,0],base+1.65*np.array([progress.get_value(),.4,0]),E,5))
        self.show(arrows,probe,arrow)
        formula=math(r"\mathbf E=\kappa(x\hat{\mathbf x}+y\hat{\mathbf y}+z\hat{\mathbf z})",49,[2.9,1.7,0],width=7.9);self.show(formula)
        kap=VGroup(math(r"\kappa",40),text("constante escalar:\nquanto o campo cresce por unidade de distância",30,width=6.2)).arrange(RIGHT,buff=.25).move_to([3.1,2.55,0]);self.show(kap)
        grows=math(r"|\mathbf E|\propto r",42,[2.9,.2,0]);self.show(grows)
        self.pace(0.55)
        self.play(progress.animate.set_value(1.6),run_time=3,rate_func=linear)
        self.ancora("K02")
        self.erase(grows,arrows,probe,arrow)
        basis=[RIGHT,np.array([.5,.35,0]),UP]
        axes=VGroup(*[vec(base,base+1.8*u,MUTED,2) for u in basis]);self.show(axes)
        axislabels=VGroup(math('x',31,[-1.8,-.25,0]),math('y',31,[-3.6,1.15,0]),math('z',31,[-4.3,2.25,0]));self.show(axislabels,t=.3)
        terms=[]
        for i,sym in enumerate('xyz'):
            self.pace([.05,.35,.65][i])
            probe_axis=Dot(base+.3*basis[i],radius=.07,color=Q)
            field_axis=always_redraw(lambda:vec(probe_axis.get_center(),base+1.55*(probe_axis.get_center()-base),E,4))
            self.show(probe_axis,field_axis,t=.25)
            self.play(probe_axis.animate.move_to(base+1.4*basis[i]),run_time=.9)
            self.play(Indicate(axes[i],color=E),run_time=.4)
            component=math(r"E_"+sym+r"=\kappa "+sym,48,[2.9,.1,0]);self.show(component,t=.3)
            component=self.change(component,math(r"\frac{\partial E_"+sym+r"}{\partial "+sym+r"}=\kappa",48,[2.9,.1,0]),t=.8)
            self.wait(.15)
            term=math(r"\kappa",49,[1.5+1.4*i,-1.3,0])
            kappa=component.get_part_by_tex(r"\kappa")
            assert kappa is not None
            self.play(TransformFromCopy(kappa,term),run_time=.5);self.live.append(term);terms.append(term)
            self.erase(component,probe_axis,field_axis,t=.2)
        self.ancora("K03")
        summed=MathTex(r"\kappa+\kappa+\kappa",font_size=54).move_to([2.9,-.4,0])
        for i,m in enumerate(terms):
            self.play(ReplacementTransform(m,summed[0][2*i]),run_time=.35)
            self.live.remove(m)
        self.play(Write(summed[0][1]),Write(summed[0][3]),run_time=.35)
        self.remove(*list(summed[0]));self.add(summed)
        self.live.append(summed)
        result=MathTex(r"3\kappa",font_size=54).move_to(summed)
        self.play(TransformByGlyphMap(summed,result,([0],[1]),([1,2,3,4],[]),([],[0])),run_time=1)
        self.live.remove(summed);self.live.append(result)
        label=math(r"\nabla\cdot\mathbf E=",47).next_to(result,LEFT,buff=.2);self.show(label,t=.3)
        self.rs = 1.0
        self.marco(665.9)
        self.erase(axes,axislabels,t=.3)
        arrows2 = VGroup(*[vec(base+[x,y,0],base+1.25*np.array([x,y,0]),E,2.8,.5) for x in [-1.6,-.8,0,.8,1.6] for y in [-1.4,-.7,0,.7,1.4] if abs(x)+abs(y)>.1])
        dens2 = VGroup(*[Dot(base+[x+.4,y+.35,0],radius=.045,color=Q).set_opacity(.8) for x in [-1.6,-.8,0,.8] for y in [-1.4,-.7,0,.7]])
        self.show(arrows2,dens2,t=.8)
        ctag = text("densidade de carga uniforme",24,width=5.5).move_to([-4,-2.15,0]); self.marco(668.4); self.show(ctag)
        rhoeq=math(r"\rho=3\varepsilon_0\kappa",46,[2.9,-1.6,0]);self.marco(670.6);self.show(rhoeq)
        self.fecha(True)
        self.beat(270);self.clear()


    def point_delta(self):
        self.begin(270, "carga pontual e delta")
        self.title("CARGA PONTUAL: FLUXO SEMPRE IGUAL")
        RX = 3.4
        self.ancora("P01")
        self.origin = np.array([-3.8,.15,0]); self.q = charge(self.origin)
        field = self.radial(self.origin,2.45,24); self.show(field,self.q)
        formula = math(r"\mathbf E=\frac{q}{4\pi\varepsilon_0}\frac{\hat{\mathbf r}}{r^2}",51,[RX,1.5,0],width=7.2)
        outside = math(r"\nabla\cdot\mathbf E=0\;(r\ne0)",46,[RX,-.1,0],width=7.2); self.show(formula,outside)
        self.ancora("P02")
        probe = cube([-2,1.5,0],.5); self.show(probe)
        for target,ctrls,when in [([-5.5,1.4,0],([-2.6,2.7,0],[-4.9,2.7,0]),13),
                                  ([-5.4,-1.3,0],([-6.3,1.2,0],[-6.3,-1.1,0]),23)]:
            path = CubicBezier(probe[3].get_center(),*ctrls,target)
            self.play(MoveAlongPath(probe,path),run_time=5,rate_func=linear)
            self.play(Indicate(outside,color=GEO),Indicate(probe,color=GEO),run_time=.8)
            self.at(when)
        self.ancora("P03")
        self.erase(probe,formula)
        self.play(outside.animate.move_to([RX,-2.25,0]),run_time=.7)
        radius = ValueTracker(2.1)
        surface = always_redraw(lambda:Circle(radius.get_value(),color=GEO,stroke_width=3,fill_color=GEO,fill_opacity=.045).move_to(self.origin))
        boundary_field = always_redraw(lambda:VGroup(*[vec(self.origin+radius.get_value()*np.array([np.cos(a),np.sin(a),0]),
                  self.origin+(radius.get_value()+min(.72,.13/radius.get_value()**2))*np.array([np.cos(a),np.sin(a),0]),E,4)
                  for a in np.linspace(0,TAU,12,endpoint=False)]))
        self.show(surface,boundary_field)
        flux = math(r"\oint_S\mathbf E\cdot d\mathbf A=\frac{q}{\varepsilon_0}",48,[RX,1.6,0],width=7.2); self.show(flux)
        flux = self.change(flux,math(r"\Phi_E=\frac{q}{\varepsilon_0}",61,[RX,1.6,0]),t=1.3)
        constant = text("FLUXO CONSTANTE",27).move_to([RX,.35,0]); self.show(constant)
        bar = Line([RX-1.9,-.35,0],[RX+1.9,-.35,0],color=FLUX,stroke_width=7); self.show(bar)
        self.ancora("P04")
        rlabel = math(r"R/R_0=",40,[RX-1,-1.25,0])
        value = DecimalNumber(1,num_decimal_places=2,font_size=42,color=GEO).move_to([RX+1.1,-1.25,0])
        value.add_updater(lambda m:m.set_value(radius.get_value()/2.1)); self.show(rlabel,value)
        self.at(24)
        self.play(radius.animate.set_value(.315),run_time=10,rate_func=linear)
        self.ancora("P05")
        self.erase(rlabel,value,bar,constant,boundary_field)
        out_n = text("fora da origem, o divergente é zero",22,width=7).move_to([RX,.3,0])
        question = text("Onde está a fonte?",31,width=7.2).move_to([RX,-.7,0]); self.show(out_n,question)
        self.at(52)
        # ── o conflito e a pergunta: como representar uma fonte inteira num ponto? ──
        self.pace(0.3)
        self.erase(question,out_n,flux,surface,field,outside)
        self.title("UMA FONTE CONCENTRADA NUM PONTO")
        c1 = math(r"\nabla\cdot\mathbf E=0\;(r\ne0)",46,[RX,2.2,0],width=7.2)
        c2 = VGroup(math(r"\Phi_E=\frac{q}{\varepsilon_0}",50,[RX,1.3,0]),text("por qualquer superfície em torno da origem",22,width=7).move_to([RX,.6,0]))
        self.show(c1,c2)
        ask = text("Como representar uma fonte inteira\nconcentrada em um único ponto?",26,width=7.2).move_to([RX,-.2,0]); self.show(ask)
        self.pace(0.55)
        rr = ValueTracker(1.5)
        shrink = always_redraw(lambda:Circle(rr.get_value(),color=GEO,stroke_width=3,fill_color=GEO,fill_opacity=.1).move_to(self.origin))
        qenv = math(r"Q_{\rm env}=q",54,[RX,-1.5,0]); self.show(shrink,qenv)
        self.play(rr.animate.set_value(.09),run_time=6,rate_func=smooth)
        keep = text("o volume encolhe; a carga dentro dele não muda",22,width=7).move_to([RX,-2.3,0]); self.show(keep)
        self.at(66)
        self.ancora("P06")
        self.rs = 1.0
        self.erase(ask,keep,t=.4)
        # ── delta de Dirac tridimensional ──
        self.marco(763.1)
        self.erase(c1,c2,qenv,shrink,t=.4)
        self.title("DELTA DE DIRAC TRIDIMENSIONAL")
        namet = text("delta de Dirac tridimensional",34,width=7).move_to([RX,2.55,0]); self.marco(763.95); self.show(namet,t=.6)
        self.marco(766.7)
        self.erase(namet,t=.3)
        delta = math(r"\delta^{(3)}(\mathbf r)",78,[RX-.3,1.35,0]); self.show(delta)
        dpart = delta.get_part_by_tex(r"\delta^{(3)}")
        call = text("(3): três dimensões, não potência",21,width=4.6).move_to(dpart.get_corner(UR)+[1.5,.72,0])
        lead = Line(call.get_left()+[-.05,-.06,0],dpart.get_corner(UR)+[.03,.04,0],color=WHITE,stroke_width=1.3)
        self.show(call,lead,t=.6)
        self.ancora("P07")
        what = text("uma distribuição que concentra integral unitária num ponto",24,width=7).move_to([RX,.45,0]); self.show(what)
        self.at(76)
        self.erase(call,lead,t=.4)
        # ── o que a delta faz: zero fora, um quando contém a origem ──
        self.pace(0.4)
        test = Circle(.85,color=GEO,stroke_width=3,fill_color=GEO,fill_opacity=.12).move_to([-1.7,.15,0])
        vlab = math("V",38,[-1.7,1.25,0]); self.show(test,vlab)
        vlab.add_updater(lambda m:m.move_to(test.get_center()+[0,1.15,0]))
        self.play(delta.animate.scale(.62).move_to([RX,2.4,0]),what.animate.move_to([RX,1.7,0]),run_time=.8)
        integ = math(r"\int_V\delta^{(3)}(\mathbf r)\,dV=0",56,[RX,.5,0],width=7.2); self.show(integ)
        state = text("origem fora de V",24).move_to([RX,-.55,0]); self.show(state)
        self.play(test.animate.move_to([-2.5,.15,0]),run_time=4,rate_func=linear)
        # O valor na fronteira não é afirmado: ocultar antes de atravessá-la.
        self.erase(integ,state,t=.25)
        self.play(FadeOut(test),run_time=.4)
        test.move_to(self.origin+[.45,0,0])
        self.play(FadeIn(test),Flash(self.q,color=Q,flash_radius=.5),run_time=.7)
        integ = math(r"\int_V\delta^{(3)}(\mathbf r)\,dV=1",56,[RX,.5,0],width=7.2)
        state = text("origem dentro de V",24).move_to([RX,-.55,0]); self.show(integ,state,t=.4)
        self.play(test.animate.move_to(self.origin),run_time=2.2,rate_func=linear)
        self.at(94)
        rule = text("não é uma função comum: só ganha sentido sob uma integral",22,width=7.2).move_to([RX,-1.4,0]); self.show(rule)
        units = math(r"[\delta^{(3)}]=\mathrm{m}^{-3}",34,[RX,-2.25,0]); self.show(units)
        self.at(104)
        self.ancora("P08")
        self.erase(integ,state,rule,units,what,t=.4)
        samp1 = math(r"\int_V f(\mathbf r)\,\delta^{(3)}(\mathbf r)\,dV",50,[RX,.5,0],width=7.4)
        cond = text("origem no interior de V",22,width=7).move_to([RX,-.55,0])
        fax = Axes(x_range=[-2,2,1],y_range=[0,2.2,1],x_length=3.8,y_length=1.5,tips=False,axis_config={"color":MUTED,"stroke_width":1.6,"include_ticks":False}).move_to([-3.8,-1.9,0])
        fcur = fax.plot(lambda x:1.0+.5*np.sin(1.4*x)+.12*x,x_range=[-2,2],color=E,stroke_width=4)
        flab = math(r"f(\mathbf r)",34,fax.c2p(1.7,2.0)+[.5,.1,0])
        f0 = fax.c2p(0,1.0)
        fdot = Dot(f0,radius=.08,color=WHITE).set_z_index(9)
        fdash = DashedLine(self.origin+[0,-.25,0],f0,color=MUTED,stroke_width=1.5)
        f0lab = math(r"f(\mathbf 0)",34,f0+[.65,.45,0])
        self.rs = 1.0
        self.marco(793.8); self.show(fax,fcur,flab,t=.8)
        self.marco(796.2); self.show(samp1,cond,t=.8)
        self.marco(800.4); self.playx(fcur.animate.set_stroke(opacity=.22),flab.animate.set_opacity(.25),run_time=.8)
        self.show(fdash,fdot,t=.7)
        self.marco(802.7); self.show(f0lab,t=.5)
        self.marco(804.1)
        samp = self.change(samp1,math(r"\int_V f(\mathbf r)\,\delta^{(3)}(\mathbf r)\,dV=f(\mathbf 0)",50,[RX,.5,0],width=7.4),t=1.6)
        self.marco(815.4)
        self.erase(samp,cond,fax,fcur,flab,fdash,fdot,f0lab,t=.5)
        vlab.clear_updaters(); self.erase(delta,vlab)
        # ── ρ = q δ³ a partir da carga física ──
        self.ancora("P09")
        qlabel = math("q",50,self.origin+[0,1.45,0]); self.show(qlabel)
        rho = self.change(qlabel,math(r"\rho(\mathbf r)=q\delta^{(3)}(\mathbf r)",58,[RX,1.4,0],width=7.4),t=1.9)
        self.pace(0.55)
        tot = text("carga total q concentrada em r = 0",22,width=7).move_to([RX,.4,0]); self.show(tot)
        self.ancora("P10")
        gauss = math(r"\nabla\cdot\mathbf E=\frac{\rho}{\varepsilon_0}",57,[RX,-.9,0]); self.show(gauss)
        self.at(116)
        self.pace(0.35)
        result = math(r"\nabla\cdot\mathbf E=\frac{q}{\varepsilon_0}\delta^{(3)}(\mathbf r)",57,[RX,-.3,0],width=7.4)
        self.erase(tot,t=.3)
        self.merge([gauss,rho],result,2)
        self.play(test.animate.scale(.32,about_point=self.origin),run_time=4)
        self.ancora("P11")
        kw1 = text("massa pontual · gravitação",26,width=6).move_to([RX,-1.25,0]); self.pace(.12); self.show(kw1)
        kw2 = text("força concentrada num instante",26,width=6).move_to([RX,-1.8,0]); self.pace(.4); self.show(kw2)
        kw3 = text("fontes e localizações idealizadas",26,width=6).move_to([RX,-2.35,0]); self.pace(.68); self.show(kw3)
        interior = text("a delta resolve o conflito: divergente zero fora, fonte na origem",22,width=7.2).move_to([RX,-2.85,0]); self.pace(.9); self.show(interior)
        self.fecha(True)
        self.at(130); self.clear()

    def vector_field(self,center,rot=False,scale=.65):
        center=np.array(center,dtype=float); arrows=VGroup();paths=[]
        for x in np.linspace(-1.6,1.6,5):
            for y in np.linspace(-1.4,1.4,5):
                v=np.array([-y,x,0])*scale*.43 if rot else np.array([.62,0,0])
                if np.linalg.norm(v)>.04:
                    a=center+[x,y,0];arrows.add(vec(a,a+v,width=2.2,opacity=.75))
        if rot:
            for r in [.6,1.1,1.6]:
                paths.append(lambda t,r=r:center+r*np.array([np.cos(TAU*t),np.sin(TAU*t),0]))
        else:
            for y in [-1.1,0,1.1]:
                paths.append(lambda t,y=y:center+[-1.6+3.2*t,y,0])
        return VGroup(arrows,self.particles(paths,speed=.13,count=3))


    def comparison(self):
        self.begin(395, "F1, F2 e Ω")
        self.title("MESMO DIVERGENTE, OUTRA GEOMETRIA")
        self.ancora("R01")
        f1 = self.vector_field([-3.7,.1,0]); self.show(f1)
        label1 = math(r"\mathbf F_1=F_0\hat{\mathbf x}",45,[-3.7,2.4,0]); self.show(label1)
        self.pace(0.5)
        probe1 = cube([-3.7,.1,0],.6); self.show(probe1)
        z1 = math(r"\nabla\cdot\mathbf F_1=0",42,[-3.7,-1.9,0]); self.show(z1)
        self.at(7)
        # ── Ω: o que controla o giro ──
        self.ancora("R02")
        c2 = np.array([3.7,-.1,0]); omega = ValueTracker(.6)
        axes = VGroup(vec(c2+[-1.9,0,0],c2+[1.9,0,0],MUTED,1.4),vec(c2+[0,-1.35,0],c2+[0,1.4,0],MUTED,1.4),
                      math("x",28,c2+[2.15,-.05,0]),math("y",28,c2+[.22,1.55,0]))
        guide = DashedVMobject(Circle(1.2,color=MUTED,stroke_width=1.2).move_to(c2),num_dashes=30)
        om = math(r"\Omega",58,[3.7,2.55,0])
        what = mix([[("m",r"\Omega"),("t",": constante escalar que controla")],[("t","a intensidade do giro")]],24,5.5).move_to([3.7,2.0,0])
        self.rs = 1.0
        self.show(axes,guide,t=.8)
        pv0 = Dot(c2+[1.2,0,0],radius=.06,color=WHITE); v0 = vec(c2+[1.2,0,0],c2+[1.2,.9,0],E,4.5)
        self.marco(892.3); self.show(pv0,v0,t=.6)
        self.marco(895.6); self.show(om,what,t=.8)
        self.ancora("R03")
        self.erase(v0,pv0,t=.2)
        pts = [np.array(q) for q in [(1.2,0,0),(0,1.2,0),(-1.2,0,0),(0,-1.2,0)]]
        spin = always_redraw(lambda:VGroup(*[vec(c2+q,c2+q+.9*omega.get_value()*np.array([-q[1],q[0],0]),E,4.5) for q in pts]))
        dots = VGroup(*[Dot(c2+q,radius=.06,color=WHITE) for q in pts])
        self.show(dots,spin,t=.6)
        self.at(14)
        self.play(omega.animate.set_value(1.3),run_time=3,rate_func=smooth)
        self.at(20)
        # ── a fórmula de F2 e o campo completo ──
        self.pace(0.55)
        label2 = self.change(om,math(r"\mathbf F_2=\Omega(-y\hat{\mathbf x}+x\hat{\mathbf y})",40,[3.7,2.5,0],width=6.5),t=1.5)
        self.ancora("R04")
        self.erase(what,guide)
        arrows = always_redraw(lambda:VGroup(*[vec(c2+[x,y,0],c2+np.array([x,y,0])+.42*omega.get_value()/1.3*np.array([-y,x,0]),E,2.5,.7)
                    for x in np.linspace(-1.35,1.35,5) for y in np.linspace(-1.05,1.05,5) if abs(x)+abs(y)>.1]))
        sample = VGroup(*[Dot(c2+[x,y,0],radius=.035,color=E) for x,y in [(-1.3,-.8),(-.8,.5),(.4,1.2),(.9,-.7),(-.2,-1.2),(1.2,.1)]])
        def advect(m,dt):
            m.rotate(.75*omega.get_value()/1.3*dt,about_point=c2)
        for dot in sample:dot.add_updater(advect)
        self.erase(spin,dots,t=.4)
        self.show(arrows,sample)
        probe2 = cube(c2,.6); self.show(probe2)
        z2 = math(r"\nabla\cdot\mathbf F_2=0",42,[3.7,-2.05,0]); self.show(z2)
        self.play(omega.animate.set_value(.7),run_time=2,rate_func=smooth)
        self.play(omega.animate.set_value(1.3),run_time=2,rate_func=smooth)
        self.at(34)
        # ── mesmo divergente, geometrias diferentes ──
        self.pace(0.5)
        same = text("mesmo divergente, geometria diferente",24).move_to([0,-2.65,0]); self.show(same)
        self.at(40)
        self.fecha(True)
        self.erase(same,axes)
        pass
        self.at(46)
        for m in sample:m.clear_updaters()
        self.clear()

    def wheel(self):
        self.begin(420, "rotacional")
        self.ancora("R05")
        self.title("COMO DETECTAR CIRCULAÇÃO LOCAL?")
        cl = np.array([-4.2,.1,0]); cr = np.array([4.2,.1,0]); omega = ValueTracker(0)
        # esquerda: campo sem circulação, sonda parada
        f1 = self.vector_field(cl); wl = self.probe_wheel(cl,.8)
        lab1 = math(r"\mathbf F_1=F_0\hat{\mathbf x}",40,cl+[0,2.3,0])
        self.show(f1,wl,lab1)
        stat = text("sonda parada",22).move_to(cl+[0,-1.95,0]); self.show(stat)
        # direita: campo giratório; a sonda gira com Ω
        self.pace(0.3)
        wr = self.probe_wheel(cr,.8)
        lab2 = math(r"\mathbf F_2=\Omega(-y\hat{\mathbf x}+x\hat{\mathbf y})",38,cr+[0,2.3,0],width=6)
        field2 = always_redraw(lambda:VGroup(*[vec(cr+[x,y,0],cr+np.array([x,y,0])+.38*omega.get_value()*np.array([-y,x,0]),E,3,.7)
                    for x in [-1.8,-1.2,0,1.2,1.8] for y in [-1.5,-1.0,0,1.0,1.5] if x*x+y*y>1.1]))
        phase = ValueTracker(0)
        phase.add_updater(lambda m,dt:m.increment_value(dt*.7*omega.get_value())); self.add(phase)
        parts2 = always_redraw(lambda:VGroup(*[Dot(cr+r*np.array([np.cos(a+phase.get_value()),np.sin(a+phase.get_value()),0]),radius=.045,color=E)
                for r in [1.3,1.8] for a in np.linspace(0,TAU,5,endpoint=False)]))
        wr.add_updater(lambda m,dt:m.rotate(dt*.7*omega.get_value(),about_point=cr))
        self.show(wr,lab2,field2,parts2)
        # o medidor liga o giro da sonda a Ω
        self.pace(0.6)
        track = Line(cr+[-.5,-1.95,0],cr+[1.9,-1.95,0],color=MUTED,stroke_width=3)
        meter = always_redraw(lambda:Line(cr+[-.5,-1.95,0],cr+[-.5+2.4*min(omega.get_value(),1),-1.95,0],color=OMEGA,stroke_width=8))
        mlab = text("GIRO LOCAL",20).move_to(cr+[-1.75,-1.95,0]); self.show(track,meter,mlab)
        self.beat(429)
        # o operador que distingue os dois campos
        self.ancora("R06")
        op = math(r"\nabla\times\mathbf F",64,[0,.9,0]); sub = text("mede o giro local do campo",21,width=3.6).move_to([0,.1,0])
        self.show(op,sub)
        self.pace(0.3)
        z = VGroup(Circle(.17,color=NORMAL,stroke_width=2.5),Dot(radius=.05,color=NORMAL)).move_to([0,-.9,0])
        zlabel = math(r"\hat{\mathbf z}",34,[.55,-.9,0]); zrule = text("regra da mão direita:\nanti-horário → saindo da tela",20,width=3.1).move_to([-.15,-1.65,0])
        self.show(z,zlabel,zrule)
        self.pace(0.5)
        self.play(omega.animate.set_value(1),run_time=9,rate_func=linear)
        self.ancora("R07")
        r1 = math(r"\nabla\times\mathbf F_1=0",38,cl+[0,-2.55,0],width=5); r2 = math(r"\nabla\times\mathbf F_2=2\Omega\hat{\mathbf z}",38,cr+[0,-2.55,0],width=5.4)
        self.show(r1,r2)
        self.pace(0.6)
        self.play(Indicate(r2,color=WHITE),Indicate(z,color=NORMAL),run_time=1.2)
        self.beat(453)
        self.ancora("R08")
        self.erase(f1,wl,lab1,stat,wr,lab2,field2,parts2,track,meter,mlab,sub,r1,r2,z,zlabel,zrule)
        phase.clear_updaters(); self.remove(phase)
        self.play(op.animate.move_to([3,.7,0]),run_time=.8)
        concept = self.change(op,math(r"\nabla\times\mathbf E",66,[0,.4,0]),t=1.7)
        self.pace(0.4)
        self.title("AGORA, O CAMPO ELETROSTÁTICO")
        self.fecha(True)
        self.beat(465); self.clear()

    def circulation(self):
        self.begin(465, "circulação")
        self.title("CIRCULAÇÃO: ACUMULAR AO LONGO DO CAMINHO")
        RX = 3.7; W = 7.2
        self.ancora("C01")
        O = self.origin = np.array([-6.2,.1,0]); self.q = charge(O); self.show(self.q)
        a = np.array([-4.7,-.8,0]); b = np.array([-1.1,1.1,0])
        self.path1 = CubicBezier(a,[-4.4,2,0],[-2.3,2.1,0],b,color=GEO,stroke_width=3)
        self.path2 = CubicBezier(a,[-4,-2,0],[-1.4,-1.7,0],b,color=FLUX,stroke_width=3)
        T1 = Track.sample(lambda t:self.path1.point_from_proportion(t)); T2 = Track.sample(lambda t:self.path2.point_from_proportion(t))
        labels = VGroup(math('a',34,a+[0,-.4,0]),math('b',34,b+[0,.4,0]))
        ra = DashedLine(O,a,color=MUTED,stroke_width=1.8); rb = DashedLine(O,b,color=MUTED,stroke_width=1.8)
        ral = math(r"r_a",32,(O+a)/2+[0,-.32,0]); rbl = math(r"r_b",32,(O+b)/2+[0,.34,0])
        self.pace(0.3)
        self.show(labels,ra,rb,ral,rbl)
        lc1 = math("C_1",34,[-3.2,2.0,0]); lc2 = math("C_2",34,[-3.2,-2.5,0])
        r0 = np.linalg.norm(a-O); r1 = np.linalg.norm(b-O); final = 1/r0-1/r1
        progress = ValueTracker(0)
        track = Line([RX-1.9,-1.55,0],[RX+1.9,-1.55,0],color=MUTED,stroke_width=2)
        accl = text("circulação acumulada",20).move_to([RX,-1.15,0])
        # ── C1: E e dℓ em cada ponto ──
        self.pace(0.7)
        progress.set_value(0); self.path1.set_stroke(opacity=.28); self.show(self.path1,lc1,t=.6)
        self.ancora("C02")
        integ = math(r"\int_{C_1}\mathbf E\cdot d\mathbf l",50,[RX,2.55,0],width=W)
        self.build(integ,{"C_1":lc1},t=.9)
        def accumulated(trk,k):
            pt = trk.at(progress.get_value()); val = (1/r0-1/np.linalg.norm(pt-O))/final
            return Line([RX-1.9,-1.55,0],[RX-1.9+max(.002,3.8*val),-1.55,0],color=[GEO,FLUX][k],stroke_width=7)
        bar = always_redraw(lambda:accumulated(T1,0))
        grp = self.tracer(T1,progress,O)
        work = text("trabalho do campo por unidade de carga",22,width=7).move_to([RX,1.75,0]); self.pace(.3); self.show(work)
        self.show(*grp,bar,track,accl,t=.4)
        self.play(progress.animate.set_value(1),run_time=10,rate_func=linear)
        self.at(12)
        # ── de onde vem 1/r_a − 1/r_b: só a componente radial de dℓ conta ──
        self.ancora("C03")
        self.erase(work,t=.3)
        for m in grp[2:]:
            self.erase(m,t=.2)
        mid = T1.at(.5); tt = T1.tangent(.5); ur = (mid-O)/np.linalg.norm(mid-O)
        dlv = vec(mid,mid+.95*tt,WHITE,5.5).set_z_index(9)
        comp = vec(mid,mid+.95*np.dot(tt,ur)*ur,E,5).set_z_index(10)
        trans = DashedLine(mid+.95*np.dot(tt,ur)*ur,mid+.95*tt,color=MUTED,stroke_width=2)
        dll_ = math(r"d\mathbf l",30,mid+.95*tt+[.1,.32,0]); drl = math(r"dr",30,mid+.95*np.dot(tt,ur)*ur+[.1,-.4,0])
        el_ = vec(mid,mid+.9*ur,E,3,.55)
        self.show(el_,dlv,comp,trans,dll_,drl,t=.7)
        note = mix([[("t","só a componente radial de "),("m",r"d\mathbf l"),("t"," entra no produto escalar")]],20,7).move_to([RX,1.75,0]); self.show(note)
        self.ancora("C04")
        E1 = math(r"\mathbf E\cdot d\mathbf l=\frac{q}{4\pi\varepsilon_0\,r^2}\,dr",46,[RX,.65,0],width=W)
        self.show(E1,t=1.0)
        self.at(22)
        self.pace(0.55)
        E2 = self.change(E1,math(r"\int_{C_1}\mathbf E\cdot d\mathbf l=\frac{q}{4\pi\varepsilon_0}\int_{r_a}^{r_b}\frac{dr}{r^2}",42,[RX,.65,0],width=W),t=1.6)
        self.erase(note,el_,dlv,comp,trans,dll_,drl,t=.4)
        self.at(27)
        self.ancora("C05")
        E3 = self.change(E2,math(r"\int_{C_1}\mathbf E\cdot d\mathbf l=\frac{q}{4\pi\varepsilon_0}\left(\frac{1}{r_a}-\frac{1}{r_b}\right)",42,[RX,.65,0],width=W),t=1.6)
        self.play(Indicate(ral,color=WHITE),Indicate(rbl,color=WHITE),run_time=1.0)
        self.at(32)
        self.ancora("C06")
        self.erase(integ,grp[0],grp[1],bar,t=.3)
        self.play(E3.animate.move_to([RX,2.65,0]).scale(.72),run_time=.7)
        # ── C2: outro caminho, mesmos extremos ──
        progress.set_value(0); self.path2.set_stroke(opacity=.28); self.show(self.path2,lc2,t=.5)
        integ2 = math(r"\int_{C_2}\mathbf E\cdot d\mathbf l",50,[RX,1.15,0],width=W)
        self.build(integ2,{"C_2":lc2},t=.8)
        bar2 = always_redraw(lambda:accumulated(T2,1))
        grp2 = self.tracer(T2,progress,O)
        self.show(*grp2,bar2,t=.4)
        self.play(progress.animate.set_value(1),run_time=7,rate_func=linear)
        full2 = math(r"\int_{C_2}\mathbf E\cdot d\mathbf l=\frac{q}{4\pi\varepsilon_0}\left(\frac{1}{r_a}-\frac{1}{r_b}\right)",34,[RX,1.15,0],width=W)
        self.change(integ2,full2,t=1.1)
        self.erase(*grp2,bar2,t=.3)
        self.at(46)
        self.ancora("C07")
        equal = math(r"\int_{C_1}\mathbf E\cdot d\mathbf l=\int_{C_2}\mathbf E\cdot d\mathbf l",50,[RX,.8,0],width=W)
        self.merge([E3,full2],equal,1.8)
        self.erase(track,accl,t=.4)
        ends = mix([[("t","caminhos diferentes, mesmos extremos: "),("m",r"r_a"),("t"," e "),("m",r"r_b"),("t"," iguais")]],22,7).move_to([RX,-.3,0]); self.show(ends)
        self.play(Indicate(self.path1,color=GEO),run_time=1.0)
        self.play(Indicate(self.path2,color=FLUX),run_time=1.0)
        self.at(54)
        self.ancora("C08")
        self.erase(equal,ends,ra,rb,ral,rbl)
        # ── C = C1 − C2: ida por C1, volta por C2 (sentido inverso) ──
        closed_trk = Track(list(T1.p)+list(T2.p[::-1]))
        self.closed = VMobject(color=GEO,stroke_width=3).set_points_as_corners(list(closed_trk.p))
        union = math(r"C=C_1-C_2",54,[RX,2.2,0],width=W)
        self.build(union,{"C_1":lc1,"C_2":lc2},t=1.4)
        self.at(58)
        self.erase(self.path1,self.path2,lc1,lc2,labels); self.show(self.closed,t=.4)
        progress.set_value(0)
        gc = self.tracer(closed_trk,progress,O)
        def closedbar():
            pt = closed_trk.at(progress.get_value()); val = (1/r0-1/np.linalg.norm(pt-O))/final
            return Line([RX-1.9,-1.55,0],[RX-1.9+max(.002,3.8*val),-1.55,0],color=FLUX,stroke_width=7)
        bar3 = always_redraw(closedbar)
        label = text("volta completa: os extremos coincidem",22,width=7).move_to([RX,-.95,0])
        self.show(label,*gc,bar3,track,t=.5)
        self.play(progress.animate.set_value(1),run_time=10,rate_func=linear)
        self.ancora("C09")
        self.erase(label,*gc,bar3,track,union)
        zero = math(r"\oint_C\mathbf E\cdot d\mathbf l=0",62,[RX,.9,0],width=W); self.show(zero,t=.5)
        self.at(76)
        self.ancora("C10")
        pot = text("independe do caminho → potencial",24,width=7).move_to([RX,-.2,0]); self.show(pot)
        self.fecha(True)
        self.clear(keep=(self.closed,self.q))

    def stokes(self):
        self.begin(515, "Stokes")
        self.title("STOKES: DA BORDA AO INTERIOR")
        RX = 3.7; W = 7.0; cscr = np.array([-3.3,.2,0]); az,el = .45,.55; R = 2.1
        n = np.array([.2,-.28,1.]); n = n/np.linalg.norm(n)
        a_ = np.array([1.,0,0]); u = a_-a_.dot(n)*n; u = u/np.linalg.norm(u); w = np.cross(n,u)
        def lin(P):
            x,y,z = P; xr = x*np.cos(az)-y*np.sin(az); yr = x*np.sin(az)+y*np.cos(az)
            return np.array([xr,z*np.cos(el)+yr*np.sin(el),0])
        pr = lambda P:cscr+lin(P)
        bpt = lambda th:pr(R*(np.cos(th)*u+np.sin(th)*w))
        ring_pts = [bpt(t) for t in np.linspace(0,TAU,90,endpoint=False)]
        contour = Polygon(*ring_pts,color=GEO,stroke_width=3)
        membrane = Polygon(*ring_pts,stroke_width=0,fill_color=GEO,fill_opacity=.13)
        def patch(s,t,size=.4,col=DAVEC,fill=.5,uu=u,ww=w):
            c3 = s*u+t*w
            return Polygon(*[pr(c3+size*(i*uu+j*ww)) for i,j in [(-1,-1),(1,-1),(1,1),(-1,1)]],
                           color=col,stroke_width=2.5,fill_color=col,fill_opacity=fill).set_z_index(6)
        self.ancora("S01")
        self.play(Transform(self.closed,contour),run_time=1.3)
        source = math('r=0',28,[-6.2,-.45,0]); self.show(source,t=.3)
        lab_c = math("C",34,bpt(2.55)+[-.2,.22,0]); self.show(lab_c,t=.4)
        # ── 1. borda: tracer percorre C e dℓ tangente aparece ao longo dela ──
        bt = Track([bpt(t) for t in np.linspace(0,TAU,241)])
        progress = ValueTracker(0)
        dot = always_redraw(lambda:Dot(bt.at(progress.get_value()),radius=.08,color=WHITE).set_z_index(9))
        trail = always_redraw(lambda:bt.part(progress.get_value(),color=WHITE,stroke_width=4.5))
        n_dl = 10; dls = VGroup()
        for k in range(n_dl):
            tk = k/n_dl; p0 = bt.at(tk); tg = bt.tangent(tk)
            arr = vec(p0,p0+.55*tg,WHITE,4.5).set_z_index(8).set_opacity(0)
            arr.add_updater(lambda m,k=k:m.set_opacity(float(np.clip((progress.get_value()-k/n_dl)*25,0,1))))
            dls.add(arr)
        circ = math(r"\oint_C\mathbf F\cdot d\mathbf l",52,[RX,2.3,0],width=W)
        fnote = mix([[("m",r"\mathbf F"),("t",": campo genérico · "),("m",r"d\mathbf l"),("t"," tangente à borda")]],21,7).move_to([RX,1.45,0])
        self.show(dot,trail,dls,circ,fnote,t=.5)
        self.play(progress.animate.set_value(1),run_time=7,rate_func=linear)
        self.ancora("S02")
        self.erase(dot,trail,t=.3)
        self.at(12)
        # ── 2. superfície e pequenos giros locais (rotores) ──
        self.play(DrawBorderThenFill(membrane),run_time=1.4); self.live.append(membrane)
        lab_s = math("S",38,pr(-1.0*u-.75*w)); regular = text("região regular",22,MUTED).move_to([-3.3,-1.8,0])
        self.show(lab_s,regular,t=.4)
        self.ancora("S03")
        specs = [(s_,t_) for s_ in (-.9,0,.9) for t_ in (-.9,0,.9)]
        ps = [patch(s,t,.45,DAVEC,.3) for s,t in specs]
        self.play(LaggedStart(*[FadeIn(q) for q in ps],lag_ratio=.08),run_time=1.6); self.live.extend(ps)
        phase = ValueTracker(0); spin = ValueTracker(1)
        phase.add_updater(lambda m,dt:m.increment_value(dt*2.4*spin.get_value())); self.add(phase)
        def rotor(s,t,rad=.27):
            c3 = s*u+t*w
            def mk():
                ph = phase.get_value()
                pts = [pr(c3+rad*(np.cos(aa+ph)*u+np.sin(aa+ph)*w)) for aa in np.linspace(0,1.65*np.pi,22)]
                m = VMobject(color=WHITE,stroke_width=3).set_points_as_corners(pts)
                d = pts[-1]-pts[-3]; d = d/np.linalg.norm(d); nrm = np.array([-d[1],d[0],0])
                tip = Polygon(pts[-1]+.13*d,pts[-1]+.05*nrm,pts[-1]-.05*nrm,color=WHITE,fill_color=WHITE,fill_opacity=1,stroke_width=1)
                return VGroup(m,tip).set_z_index(9)
            return always_redraw(mk)
        rotors = [rotor(s,t) for s,t in specs]
        rnote = text("cada pedacinho tem a sua circulação",22,width=7).move_to([RX,.7,0])
        self.pace(.2); self.show(*rotors,rnote,t=.8)
        # a borda compartilhada é percorrida duas vezes, em sentidos opostos
        def edge_pair(s,t,axis,L=.7,gap=.07,w_=3.4):
            if axis == 'v':
                a0 = s*u+(t-L/2)*w; a1 = s*u+(t+L/2)*w; off = gap*u
                return VGroup(vec(pr(a0-off),pr(a1-off),WHITE,w_),vec(pr(a1+off),pr(a0+off),FLUX,w_)).set_z_index(10)
            a0 = (s-L/2)*u+t*w; a1 = (s+L/2)*u+t*w; off = gap*w
            return VGroup(vec(pr(a1-off),pr(a0-off),WHITE,w_),vec(pr(a0+off),pr(a1+off),FLUX,w_)).set_z_index(10)
        pairAB = edge_pair(.45,0,'v',L=.8,gap=.08,w_=5)
        note2 = text("a borda compartilhada é percorrida duas vezes,\nem sentidos opostos",21,width=7).move_to([RX,-.4,0])
        self.rs = 1.0
        self.marco(1190.3); self.show(pairAB,note2,t=.8)
        rest = VGroup(*[edge_pair(s_,t_,'v') for s_ in (-.45,.45) for t_ in (-.9,0,.9) if (s_,t_) != (.45,0)],
                      *[edge_pair(s_,t_,'h') for s_ in (-.9,0,.9) for t_ in (-.45,.45)])
        self.marco(1193.0); self.show(rest,t=1.0)
        self.marco(1197.3); self.erase(pairAB,rest,note2,t=1.0)
        self.erase(*rotors,t=.6)
        outer = Polygon(*[pr(a_*u+b_*w) for a_,b_ in [(-1.35,-1.35),(1.35,-1.35),(1.35,1.35),(-1.35,1.35)]],color=WHITE,stroke_width=3.5).set_z_index(9)
        note3 = text("as internas se cancelam; sobra só a borda externa",21,width=7).move_to([RX,-.4,0])
        self.show(outer,note3,t=.7)
        self.at(24)
        # ── 3. loop pequeno: circulação / área → componente normal do rotacional ──
        ia = specs.index((0,0)); s0,t0 = specs[ia]; c0 = pr(s0*u+t0*w)
        cv_dir = n+.45*u
        curls = [vec(pr(s*u+t*w),pr(s*u+t*w)+.75*lin(cv_dir),WHITE,3.0).set_z_index(9) for s,t in specs]
        self.ancora("S04")
        self.erase(*rotors,rnote,outer,note3,t=.4)
        sA = ValueTracker(1)
        def loopA():
            r_ = .27*sA.get_value()
            pts = [pr(s0*u+r_*(np.cos(aa)*u+np.sin(aa)*w)) for aa in np.linspace(.3,1.8*np.pi,26)]
            m = VMobject(color=WHITE,stroke_width=3.2).set_points_as_corners(pts)
            d = pts[-1]-pts[-3]; d = d/np.linalg.norm(d); nrm = np.array([-d[1],d[0],0])
            tip = Polygon(pts[-1]+.13*d,pts[-1]+.05*nrm,pts[-1]-.05*nrm,color=WHITE,fill_color=WHITE,fill_opacity=1,stroke_width=1)
            return VGroup(m,tip).set_z_index(10)
        outlA = always_redraw(lambda:Polygon(*[pr(s0*u+.45*sA.get_value()*(i_*u+j_*w)) for i_,j_ in [(-1,-1),(1,-1),(1,1),(-1,1)]],color=WHITE,stroke_width=2.5).set_z_index(10))
        loopAm = always_redraw(loopA)
        self.show(outlA,loopAm,t=.6)
        ratio = math(r"\frac{\oint\mathbf F\cdot d\mathbf l}{\Delta A}",52,[RX,.35,0],width=6)
        self.pace(.3); self.show(ratio)
        self.pace(.45); self.play(sA.animate.set_value(.25),run_time=3.5,rate_func=smooth)
        lim = math(r"\lim_{\Delta A\to0}\frac{\oint\mathbf F\cdot d\mathbf l}{\Delta A}=\left(\nabla\times\mathbf F\right)\cdot\hat{\mathbf n}",44,[RX,.35,0],width=W)
        self.pace(.65); lim = self.change(ratio,lim,t=1.4)
        self.pace(.82)
        self.erase(outlA,loopAm,t=.4)
        self.play(LaggedStart(*[GrowArrow(q) for q in curls],lag_ratio=.08),run_time=1.4); self.live.extend(curls)
        clab = math(r"\nabla\times\mathbf F",30,cscr+np.array([1.95,1.35,0])); self.show(clab,t=.4)
        dlab = math("dA",34,c0+[.2,-.7,0]); self.show(dlab,t=.3)
        nvec = vec(c0,c0+1.7*lin(n),NORMAL,4).set_z_index(9)
        nlab = math(r"\hat{\mathbf n}",34,c0+1.7*lin(n)+[.05,.32,0]); self.show(nvec,nlab,t=.6)
        self.ancora("S05")
        self.erase(lim,t=.3)
        eq1 = math(r"d\mathbf A=\hat{\mathbf n}\,dA",50,[RX,.7,0],width=6)
        self.build(eq1,{"dA":dlab,r"\hat{\mathbf n}":nlab},t=1.4)
        self.at(32)
        self.pace(0.45)
        eq2 = math(r"\left(\nabla\times\mathbf F\right)\cdot\hat{\mathbf n}\,dA",46,[RX,-.4,0],width=W)
        self.build(eq2,{r"\nabla\times":clab.get_part_by_tex(r"\nabla\times"),r"\hat{\mathbf n}":nlab,"dA":dlab},t=1.6)
        cap = text("quanto do rotacional atravessa este patch",21,width=7).move_to([RX,-1.2,0]); self.show(cap)
        self.at(40)
        self.ancora("S06")
        self.erase(cap,eq1,clab,t=.4)
        tot = self.change(eq2,math(r"\sum\left(\nabla\times\mathbf F\right)\cdot\hat{\mathbf n}\,dA",46,[RX,.3,0],width=W),t=1.2)
        self.play(LaggedStart(*[Indicate(q,color=DAVEC,scale_factor=1.15) for q in ps],lag_ratio=.1),run_time=1.6)
        surf = self.change(tot,math(r"\int_S\left(\nabla\times\mathbf F\right)\cdot d\mathbf A",50,[RX,.3,0],width=W),t=1.6)
        self.at(48)
        # ── 4. borda ↔ interior ──
        self.ancora("S07")
        t1 = text("circulação na borda",21,width=7).move_to([RX,2.85,0])
        t2 = text("rotacional acumulado no interior",21,width=7).move_to([RX,.95,0])
        self.show(t1,t2,t=.4)
        full = math(r"\oint_C\mathbf F\cdot d\mathbf l=\int_S\left(\nabla\times\mathbf F\right)\cdot d\mathbf A",50,[2.7,-2.2,0],width=11.5)
        self.erase(t1,t2,fnote)
        self.merge([circ,surf],full,2.0)
        reg = text("hipótese: F regular na região",22,width=7).move_to([2.7,-1.35,0]); self.pace(.6); self.show(reg)
        self.play(Indicate(contour if False else self.closed,color=WHITE),Indicate(membrane,color=GEO),run_time=1.4)
        self.at(56)
        # ── 5. F → E: os giros param; circulação zero; rotacional zero ──
        self.ancora("S08")
        self.erase(reg,t=.3)
        self.title("NO CAMPO ELETROSTÁTICO")
        fe = self.change(full,math(r"\oint_C\mathbf E\cdot d\mathbf l=\int_S\left(\nabla\times\mathbf E\right)\cdot d\mathbf A",50,[2.7,-2.2,0],width=11.5),t=1.6)
        rotors2 = [rotor(s,t) for s,t in specs]
        self.erase(*curls,t=.3)
        self.show(*rotors2,t=.5)
        self.play(spin.animate.set_value(0),run_time=3,rate_func=smooth)
        self.play(*[FadeOut(q) for q in rotors2],run_time=.6)
        for q in rotors2:
            self.remove(q)
        phase.clear_updaters(); self.remove(phase)
        zero = math(r"\oint_C\mathbf E\cdot d\mathbf l=0",52,[RX,1.9,0],width=W); self.show(zero)
        self.at(70)
        self.title("DA CIRCULAÇÃO ZERO AO ROTACIONAL ZERO")
        z0 = self.change(fe,math(r"0=\int_S\left(\nabla\times\mathbf E\right)\cdot d\mathbf A",52,[RX,.5,0],width=W),t=1.7)
        self.erase(zero,t=.3)
        z1 = self.change(z0,math(r"\int_S\left(\nabla\times\mathbf E\right)\cdot d\mathbf A=0",52,[RX,1.2,0],width=W),t=1.3)
        self.at(76)
        self.ancora("S09")
        for q in dls:
            q.clear_updaters()
        group = VGroup(membrane,self.closed,*ps,nvec,nlab,dlab,dls,lab_c,lab_s,regular)
        self.play(group.animate.scale(2.2,about_point=c0).set_opacity(.0),run_time=1.8)
        for m in [membrane,self.closed,*ps,nvec,nlab,dlab,dls,lab_c,lab_s,regular]:
            if m in self.live:self.live.remove(m)
            self.remove(m)
        th = ValueTracker(0)
        def pose():
            c_,s_ = np.cos(th.get_value()),np.sin(th.get_value())
            return c_*n+s_*w, -s_*n+c_*w
        def local_patch():
            n2,w2 = pose()
            return Polygon(*[cscr+lin(1.3*(i*u+j*w2)) for i,j in [(-1,-1),(1,-1),(1,1),(-1,1)]],
                           color=DAVEC,stroke_width=3,fill_color=DAVEC,fill_opacity=.45).set_z_index(6)
        def local_normal():
            n2,_ = pose()
            return vec(cscr,cscr+2.2*lin(n2),NORMAL,5).set_z_index(9)
        lp = always_redraw(local_patch); ln = always_redraw(local_normal)
        lpl = math(r"\Delta A",38,cscr+[1.9,-1.0,0])
        self.show(lp,ln,lpl,t=.8)
        eq_a = self.change(z1,math(r"\int_{\Delta S}\left(\nabla\times\mathbf E\right)\cdot d\mathbf A=0",48,[RX,1.2,0],width=W),t=1.3)
        self.pace(.45)
        l1 = self.change(eq_a,math(r"\lim_{\Delta A\to0}\frac{1}{\Delta A}\int_{\Delta S}\left(\nabla\times\mathbf E\right)\cdot d\mathbf A=0",44,[RX,1.75,0],width=W),t=1.5)
        self.pace(.62)
        eq_loc = math(r"\left(\nabla\times\mathbf E\right)\cdot\hat{\mathbf n}=0",50,[RX,.75,0],width=W); self.show(eq_loc)
        anyo = text("qualquer pequena superfície,\nem qualquer orientação",22,width=6.5).move_to([RX,-.2,0]); self.show(anyo)
        self.at(84)
        regs = text("região regular: fora da carga pontual",22,width=6.5).move_to([RX,-1.2,0]); self.pace(.5); self.show(regs)
        for target in (.7,-.6,0):
            self.play(th.animate.set_value(target),run_time=2.2,rate_func=smooth)
        self.at(94)
        self.ancora("S10")
        self.erase(regs,l1,t=.3)
        final = self.change(eq_loc,math(r"\nabla\times\mathbf E=0",76,[RX,1.2,0],width=W),t=1.6)
        box = SurroundingRectangle(final,color=GEO,buff=.25,stroke_width=2); self.show(box)
        self.title("CAMPO ELETROSTÁTICO É IRROTACIONAL")
        self.at(100)
        self.fecha(True)
        lp.clear_updaters(); ln.clear_updaters()
        self.clear()

    def synthesis(self):
        self.begin(590, "mapa final")
        self.title("ELETROSTÁTICA: DUAS PERGUNTAS LOCAIS")
        self.ancora("M01")
        central=math(r"\mathbf E(\mathbf r)",58,[0,2.1,0]);self.show(central)
        question=text("Há fonte local?",27,Q).move_to([-4,2.5,0]);self.show(question)
        c=cube([-4,1.05,0],.9);flow=self.flow_cube([-4,1.05,0],1,1);self.show(c,flow)
        leftlink=VMobject().set_points_as_corners([[-.95,2.1,0],[-2.7,2.1,0],[-2.7,1.05,0],[-2.9,1.05,0]]).set_stroke(E,1.5,.45);self.show(leftlink,t=.4)
        mechanism=text("FLUXO",26,FLUX).move_to([-4,-.15,0]);self.show(mechanism)
        self.beat(603)
        self.pace(0.4)
        op=math(r"\nabla\cdot\mathbf E",46,[-4,-.95,0]);self.show(op)
        left=self.change(op,math(r"\nabla\cdot\mathbf E=\frac{\rho}{\varepsilon_0}",52,[-4,-1.6,0],width=6.5))
        tag=text("GAUSS · GLOBAL → LOCAL",22,GEO).move_to([-4,-2.65,0]);self.show(tag)
        self.beat(611)
        self.ancora("M02")
        question2=text("Há circulação local?",27,WHITE).move_to([4,2.5,0]);self.show(question2)
        wheel=VGroup(Circle(.65,color=WHITE,stroke_width=2),*[Line([0,0,0],[.65*np.cos(a),.65*np.sin(a),0],color=WHITE,stroke_width=3) for a in np.linspace(0,TAU,8,endpoint=False)]).move_to([4,1.05,0]);self.show(wheel)
        rightlink=VMobject().set_points_as_corners([[.95,2.1,0],[2.7,2.1,0],[2.7,1.05,0],[2.9,1.05,0]]).set_stroke(E,1.5,.45);self.show(rightlink,t=.4)
        uniform=VGroup(*[vec([2.9,y,0],[3.35,y,0],E,2,.65) for y in [.65,1.05,1.45]],
                       *[vec([4.65,y,0],[5.1,y,0],E,2,.65) for y in [.65,1.05,1.45]])
        dots=self.particles([lambda t,y=y:np.array([2.9+2.2*t,y,0]) for y in [.65,1.45]],speed=.2,count=2);self.show(uniform,dots)
        mechanism2=text("CIRCULAÇÃO LOCAL",25,WHITE).move_to([4,-.15,0]);self.show(mechanism2)
        self.beat(619)
        self.pace(0.5)
        right=math(r"\nabla\times\mathbf E",46,[4,-.95,0]);self.show(right)
        right=self.change(right,math(r"\nabla\times\mathbf E=0",57,[4,-1.6,0],width=6.5))
        tag2=text("STOKES · GLOBAL → LOCAL",22,WHITE).move_to([4,-2.65,0]);self.show(tag2)
        self.beat(627)
        self.ancora("M03")
        self.play(Indicate(left,color=Q),Indicate(c,color=GEO),run_time=1.2)
        self.play(Indicate(right,color=WHITE),Indicate(wheel,color=WHITE),run_time=1.2)
        self.fecha(True)
        self.beat(635);self.clear(keep=(right,));self.map_curl=right


    def coda(self):
        self.begin(635, "Faraday e potencial")
        self.title("FARADAY: QUANDO B VARIA NO TEMPO")
        self.ancora("F01")
        self.play(self.map_curl.animate.move_to([3,.9,0]),run_time=.8)
        law = self.change(self.map_curl,math(r"\nabla\times\mathbf E=-\frac{\partial\mathbf B}{\partial t}",62,[3,.9,0],width=7.8),t=1.5)
        phase = ValueTracker(0); amplitude = ValueTracker(1)
        phase.add_updater(lambda m,dt:m.increment_value(2.2*dt)); self.add(phase)
        cb = np.array([-3.8,.2,0])
        def magnetic():
            inten = .55+.4*amplitude.get_value()*np.sin(phase.get_value())
            g = VGroup()
            for x in np.linspace(-1.2,1.2,5):
                for y in np.linspace(-.9,.9,4):
                    g.add(Circle(.14,color=MAG,stroke_width=2.2,stroke_opacity=inten).move_to(cb+[x,y,0]),
                          Dot(cb+[x,y,0],radius=.045,color=MAG).set_opacity(inten))
            return g
        def induced():
            sg = -amplitude.get_value()*np.cos(phase.get_value())
            g = VGroup()
            for rr in (1.75,2.3):
                for ang in np.linspace(0,TAU,10,endpoint=False):
                    pnt = cb+rr*np.array([np.cos(ang),np.sin(ang),0]); tg = np.array([-np.sin(ang),np.cos(ang),0])
                    peq = sg if abs(sg) > .06 else .06
                    seta = vec(pnt,pnt+.42*peq*tg,E,3.5)
                    if abs(sg) <= .06:
                        seta.set_opacity(0)
                    g.add(seta)
            return g
        self.pace(0.35)
        rings = always_redraw(magnetic); inducedE = always_redraw(induced); self.show(rings,inducedE)
        self.pace(0.7)
        blab = math(r"\mathbf B(t)",46,[-3.8,-2.6,0]); self.show(blab)
        label = text("B saindo da tela, variando · E induzido circula",22).move_to([-3.8,-3.0,0])
        self.show(label)
        self.beat(644)
        self.ancora("F02")
        self.play(amplitude.animate.set_value(0),run_time=4,rate_func=smooth)
        phase.clear_updaters(); self.remove(phase)
        self.pace(0.35)
        static = math(r"\frac{\partial\mathbf B}{\partial t}=0",50,[3,-.9,0]); self.show(static)
        self.erase(label); label = text("B constante: sem circulação induzida",22).move_to([-3.8,-3.0,0]); self.show(label)
        self.beat(653)
        # o zero nasce do termo temporal zerando
        self.pace(0.6)
        zero0 = self.change(law,math(r"\nabla\times\mathbf E=-0",62,[3,.9,0]),t=1.5)
        self.play(Indicate(static,color=MAG),run_time=.8)
        law = self.change(zero0,math(r"\nabla\times\mathbf E=0",63,[3,.9,0]),t=1.2)
        self.ancora("F03")
        self.erase(static,rings,inducedE,label,blab)
        # ── potencial: escalar → gradiente → campo ──
        self.title("PRÓXIMA IDEIA: POTENCIAL ELÉTRICO")
        center = np.array([-5.9,.1,0]); VW = {"V":WHITE}
        src = charge(center)
        pa_pt = center+2.0*np.array([np.cos(-.35),np.sin(-.35),0]); pb_pt = center+3.4*np.array([np.cos(.5),np.sin(.5),0])
        ptA = Dot(pa_pt,radius=.08,color=WHITE).set_z_index(9); ptB = Dot(pb_pt,radius=.08,color=WHITE).set_z_index(9)
        la = math("a",32,pa_pt+[0,-.38,0]); lb = math("b",32,pb_pt+[.15,.35,0])
        pathab = CubicBezier(pa_pt,pa_pt+[.9,-.8,0],pb_pt+[-1.0,-.7,0],pb_pt,color=GEO,stroke_width=3)
        self.show(src,ptA,ptB,la,lb,t=.7)
        self.pace(.3); self.show(pathab,t=.8)
        dv1 = math(r"V_b-V_a",54,[3,1.9,0],iso={"V":WHITE}); self.pace(.5); self.show(dv1)
        self.pace(.68); dv = self.change(dv1,math(r"V_b-V_a=-\int_a^b\mathbf E\cdot d\mathbf l",50,[3,1.9,0],width=7.4,iso={"V":WHITE}),t=1.4)
        self.ancora("F04")
        self.erase(pathab,la,lb,ptA,ptB,t=.4)
        self.rs = 1.0
        radii = [2,2.7,3.4]
        self.marco(1420.0)
        arcs = VGroup(*[Arc(radius=r,start_angle=-.7,angle=1.4,color=FLUX,stroke_width=2.6,stroke_opacity=.8).shift(center) for r in radii])
        self.play(LaggedStart(*[Create(a_) for a_ in arcs],lag_ratio=.2),run_time=1.2); self.live.append(arcs)
        vlabs = VGroup(*[math("V_"+str(i+1),32,center+(r+.05)*np.array([np.cos(.78),np.sin(.78),0])+[.35,.25,0],iso=VW) for i,r in enumerate(radii)])
        eqp = text("equipotenciais: V = constante",21,width=4).move_to([-3.4,-2.5,0])
        self.show(vlabs,eqp)
        radius = ValueTracker(2.7); theta = ValueTracker(-.55)
        point = always_redraw(lambda:Dot(center+radius.get_value()*np.array([np.cos(theta.get_value()),np.sin(theta.get_value()),0]),radius=.075,color=WHITE))
        self.marco(1422.6); self.show(point)
        self.playx(theta.animate.set_value(.45),run_time=1.6,rate_func=linear)
        def direction(sign,color,offset):
            uu = np.array([np.cos(theta.get_value()),np.sin(theta.get_value()),0]); vv = np.array([-uu[1],uu[0],0]); pp = center+radius.get_value()*uu+offset*vv
            return vec(pp,pp+sign*.7*uu,color,4.5)
        gradient = always_redraw(lambda:direction(-1,WHITE,.13)); electric = always_redraw(lambda:direction(1,E,-.13))
        self.marco(1425.3)
        self.show(gradient)
        gradlabel = math(r"\nabla V",50,[3,-.3,0],iso=VW); self.show(gradlabel)
        vnote = text("V é um número em cada ponto (campo escalar)\no gradiente aponta para onde V cresce",28,width=7.2).move_to([3,-1.05,0]); self.show(vnote)
        self.marco(1430.6)
        self.show(electric)
        enote = text("o campo elétrico aponta no sentido oposto:\npara onde V cai mais depressa",28,E,width=7.2).move_to([3,-2.1,0]); self.show(enote)
        self.play(radius.animate.set_value(3.3),run_time=2,rate_func=linear)
        self.ancora("F05")
        target = math(r"\mathbf E=-\nabla V",74,[3,-.3,0],width=7.8,iso=VW)
        self.change(gradlabel,target,t=1.5)
        self.erase(vnote,enote)
        hook = text("um campo vetorial descrito por um escalar",28,width=7.2).move_to([3,-1.4,0]); self.show(hook)
        self.play(theta.animate.set_value(.1),run_time=2.5,rate_func=linear)
        self.fecha(True)
        self.beat(675)

    def begin(self, old_start, name=None):
        """Marca o início de uma seção; os beats passam a ser relativos a ela."""
        self.t0 = self.vt
        self.t0_old = old_start
        self.marks.append({'secao': name or str(old_start), 'inicio_local': float(self.vt)})

    def merge(self, items, target, t=1.4, src=None):
        """Várias expressões vivas → uma, com matching de termos."""
        items = list(items)
        self.morph(VGroup(*items), target, t, src)
        for m in items:
            if m in self.live:
                self.live.remove(m)
        self.live.append(target)
        return target

    def build(self, target, src=None, t=1.2, others=None):
        """Mostra `target` fazendo seus termos nascerem de objetos já visíveis (TransformFromCopy)."""
        src = src or {}
        anims = []
        for part in target:
            s = src.get(getattr(part, 'tex_string', None))
            anims.append(TransformFromCopy(s, part) if s is not None else FadeIn(part))
        self.play(*anims, *(others or []), run_time=t)
        self.add(target)
        self.live.append(target)
        return target

    def pulse(self, *items, color=WHITE, t=.7):
        self.play(*[Indicate(m, color=color) for m in items], run_time=t)

    def at(self, x):
        """Marco relativo ao início da seção atual (segundos)."""
        self.beat(self.t0_old + x)

    def pair(self, p, side, axis, fill=.32, length=.8):
        length = .55 if axis == 2 else length
        """Par de faces ±eixo do cubo com suas normais externas."""
        g = VGroup(); k = side/1.9
        d = CUBE_BASES[axis]/np.linalg.norm(CUBE_BASES[axis])
        for s in (-1,1):
            c = face_center(p,side,axis,s)+(np.array([0,-.55*k,0]) if axis == 0 else 0)
            g.add(face(p,side,axis,s,GEO,fill,2.5),vec(c,c+s*length*k*d,NORMAL,4).set_z_index(9))
        return g

    def tag(self, s, size, pos):
        """Rótulo matemático com fundo escuro (lê sobre arestas translúcidas)."""
        m = math(s,size,pos).set_stroke(BACKGROUND_COLOR,3.5,background=True)
        return VGroup(m).set_z_index(16)

    def probe_wheel(self, center, scale=1.0):
        wheel = VGroup(Circle(.92,color=WHITE,stroke_width=2),Circle(.13,color=WHITE,fill_color=WHITE,fill_opacity=1))
        for a in np.linspace(0,TAU,8,endpoint=False):
            paddle = Polygon([.18,-.06,0],[.85,-.06,0],[.85,.18,0],[.58,.18,0],color=GEO,fill_color=GEO,fill_opacity=.45,stroke_width=2)
            paddle.rotate(a,about_point=ORIGIN); wheel.add(paddle)
        return wheel.scale(scale).move_to(center)

    def tracer(self, trk, progress, O, color=WHITE):
        """Tracer de circulação: ponto, trecho revelado, dℓ tangente e E radial saem do MESMO parâmetro."""
        P = lambda:trk.at(progress.get_value())
        visited = always_redraw(lambda:trk.part(progress.get_value(),color=color,stroke_width=4.5))
        dot = always_redraw(lambda:Dot(P(),radius=.08,color=WHITE).set_z_index(9))
        def dl_mob():
            p0 = P(); return vec(p0,p0+.6*trk.tangent(progress.get_value()),WHITE,5.5).set_z_index(9)
        def e_mob():
            p0 = P(); rv = p0-O; r = np.linalg.norm(rv)
            return vec(p0,p0+rv/r*(.25+.75*min(1,(1.7/r)**2)),E,4.5).set_z_index(9)
        dl = always_redraw(dl_mob); ea = always_redraw(e_mob)
        ell = math(r"\mathbf E",32); dll = math(r"d\mathbf l",32)
        def radial():
            rv = P()-O; return rv/np.linalg.norm(rv)
        ell.add_updater(lambda m:m.move_to(P()+radial()*1.35+[0,.25,0]))
        dll.add_updater(lambda m:m.move_to(P()+trk.tangent(progress.get_value())*1.1-radial()*.6))
        return [visited,dot,dl,ea,ell,dll]

    def outro(self):
        """Payoff, pausa e CTA no mesmo sistema de yt_0001/yt_0002 (end screen)."""
        self.begin(675, "payoff e CTA")
        self.clear()
        for m in [self.heading,self.hdr]:
            pass
        self.ancora("CTA01")
        p1 = display("DIVERGENTE E ROTACIONAL",40).move_to([0,.55,0])
        p2 = display("FLUXO → FONTE LOCAL · CIRCULAÇÃO → GIRO LOCAL",36)
        p2.scale_to_fit_width(min(p2.width,13.6)).move_to([0,-.4,0])
        self.play(FadeOut(self.heading),FadeOut(self.hdr),run_time=1.2)
        self.play(FadeIn(p1,shift=.12*UP),run_time=1.2)
        self.wait(3)
        self.play(FadeIn(p2,shift=.12*UP),run_time=1.4)
        self.wait(4)
        self.wait(2)
        self.ancora("CTA02")
        oc = np.array([0,.2,0])
        rings = VGroup(*[DashedVMobject(Circle(radius=r_,arc_center=oc),num_dashes=int(14*r_),dashed_ratio=.6).set_stroke(GEO,3.5,.16) for r_ in (2.0,3.0,4.0)])
        for i,r_ in enumerate(rings):
            r_.add_updater(lambda m,dt,s_=(1 if i % 2 == 0 else -1)*(.06-.01*i):m.rotate(s_*dt,about_point=oc))
        logo = ImageMobject(str(LOGO_PATH)).set_width(6.0).move_to([0,.6,0])
        msg = text("Inscreva-se para acompanhar os próximos vídeos",28).set_opacity(.9).move_to([0,-1.0,0])
        self.play(FadeOut(VGroup(p1,p2)),FadeOut(self.wm),run_time=1.0)
        self.play(LaggedStart(*[FadeIn(r_,scale=.85) for r_ in rings],lag_ratio=.3),FadeIn(logo,scale=.92),run_time=1.8)
        self.play(FadeIn(msg,shift=.1*UP),run_time=1.0)
        def ripple():
            wv = DashedVMobject(Circle(radius=1.6,arc_center=oc),num_dashes=24,dashed_ratio=.6).set_stroke(GEO,3.5,.35)
            self.play(wv.animate.scale(2.6,about_point=oc).set_stroke(opacity=0.0),run_time=2.6)
            self.remove(wv)
        self.wait(3.5)
        ripple()
        self.wait(3.2)
        ripple()
        self.wait(4)


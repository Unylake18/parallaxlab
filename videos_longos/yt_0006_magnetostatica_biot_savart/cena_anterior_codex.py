"""5.2 · Biot–Savart. Uma cena contínua, preview sem voz.

Referências: gramática B04–B06 de yt_0005; construção geométrica da espira vid_0008.
SEG=<nome> permite diagnóstico localizado; vazio produz a unidade inteira.
Os textos em fala() são a base aprovada de ritmo, sem geração de áudio/sync.
"""
import json
import math
import os
import re
import sys
from functools import lru_cache
from pathlib import Path

import numpy as np
from manim.mobject.text.tex_mobject import MathTexPart
from manim import (
    Scene, VGroup, VMobject, ValueTracker, ImageMobject, MathTex, DecimalNumber,
    Line, DashedLine, Arrow, Arc, Circle, Dot, Polygon, Ellipse, ParametricFunction,
    SurroundingRectangle, FadeIn, FadeOut, Create, ReplacementTransform,
    TransformMatchingTex, Transform, TransformFromCopy, Write, Indicate, LaggedStart, UP, DOWN, LEFT, RIGHT,
    UL, UR, BOLD, always_redraw, linear, smooth, config,
)

ROOT = Path(__file__).resolve().parents[2]
UNIT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(UNIT))
from template.config_horizontal import BACKGROUND_COLOR, TEXT_COLOR, PRIMARY_COLOR, WATERMARK_PATH
from template.fonts import screen_text, official_text, DISPLAY_FONT
from fisica import clinica, trecho, campo_trecho, fios, espira, campo_espira

WHITE, CYAN = TEXT_COLOR, PRIMARY_COLOR
MAG, BLUE_L, VIOLET, FC = "#EA63FF", "#7FB2FF", "#9C8CFF", "#5AA2FF"
WM_W, WM_OP = 1.92, 0.45
T_BODY, T_NOTE = 28, 24
M_L, M_M, M_S = 46, 38, 30
LW_VEC, LW_B, LW_WIRE = 5, 3, 6
SEG = os.environ.get("SEG", "")


def txt(s, size=T_BODY, color=WHITE, opacity=1.0):
    return screen_text(s, size, color=color).set_opacity(opacity)


def eq(s, size=M_M, color=WHITE, width=None):
    # Partes semânticas: o matching acompanha os fatores, em vez da linha inteira.
    tokens = [r"\mu_0", r"d\boldsymbol\ell", r"\hat{\mathbf R}",
              r"\mathbf R", r"\mathbf r'", r"\mathbf r", r"\mathbf B",
              r"\mathbf K", r"\mathbf J", r"\rho", r"\alpha", r"\theta",
              r"\phi", r"d\ell", "dB", "B_z", "B_N", "B_1", "B(0)", r"B_\infty", r"B_{\rm trecho}", "I", "K", "J", r"\mathbf F", "F_2", "R=", "R^2", "R^3", "s=", "s^2s", "s^2", "s^3"]
    m = MathTex(s, font_size=size, color=WHITE, substrings_to_isolate=tokens)
    for token in (r"\mathbf B", "dB", "B_z", "B_N", "B_1", "B(0)", r"B_\infty", r"B_{\rm trecho}"):
        m.set_color_by_tex(token, MAG, substring=False)
    for token in ("I", "K", "J", r"\mathbf K", r"\mathbf J", r"d\ell", r"d\boldsymbol\ell"):
        m.set_color_by_tex(token, CYAN, substring=False)
    for token in (r"\mathbf R", r"\hat{\mathbf R}",r"\mathbf r",r"\mathbf r'"):
        m.set_color_by_tex(token, VIOLET, substring=False)
    m.set_color_by_tex(r"\rho", BLUE_L, substring=False)
    for token in (r"\mathbf F", "F_2"):
        m.set_color_by_tex(token,FC,substring=False)
    for token in ("s=","s^2s","s^2","s^3","R="):
        m.set_color_by_tex(token,VIOLET,substring=False)
    if "z" not in s and "s^" not in s and "B(0)" not in s:
        for token in ("R^2","R^3"):
            m.set_color_by_tex(token,VIOLET,substring=False)
    if color != WHITE:
        # Cor explícita é reservada a rótulos e expressões de uma só grandeza.
        if len(s) < 24:
            m.set_color(color)
    # Manim 0.21 mantém substrings dentro da única MathTexPart principal.
    # Promove seus glifos a partes semânticas sem recompilar nem duplicar formas.
    # Assim TransformMatchingTex realmente transporta I, dℓ, R etc.
    leaves=list(m.family_members_with_points())
    used=set();parts=[]
    for token,svg_id in m.matched_strings_and_ids:
        if not svg_id.endswith("substring"):
            continue
        glyphs=[g for g in m.id_to_vgroup_dict[svg_id].family_members_with_points() if id(g) not in used]
        if glyphs:
            part=MathTexPart();part.tex_string=token;part.add(*glyphs)
            parts.append(part);used.update(id(g) for g in glyphs)
    rest=[g for g in leaves if id(g) not in used]
    if rest:
        part=MathTexPart();part.tex_string="estrutura:"+s;part.add(*rest);parts.append(part)
    if parts:
        m.submobjects=parts
    if width and m.width > width:
        m.scale_to_fit_width(width)
    return m


@lru_cache(maxsize=160)
def _cached(s, size, color):
    return eq(s, size, color)


def label(s, point, size=M_S, color=WHITE):
    return _cached(s, size, color).copy().move_to(point).set_stroke(BACKGROUND_COLOR, 7, background=True).set_z_index(12)


def arrow(a, b, color=WHITE, width=LW_VEC, z=4, tip=0.26):
    if np.linalg.norm(np.asarray(b) - a) < 1e-5:
        return VMobject()  # magnitude física zero: nenhuma seta residual
    return Arrow(a, b, buff=0, color=color, stroke_width=width, tip_length=tip,
                 max_tip_length_to_length_ratio=0.35,
                 max_stroke_width_to_length_ratio=50).set_z_index(z)


def box(m, color=WHITE):
    return SurroundingRectangle(m, color=color, buff=0.22, stroke_width=3, corner_radius=0.1)


class YT0006BiotSavart(Scene):
    def setup(self):
        self.camera.background_color = BACKGROUND_COLOR
        config.max_files_cached = 1000
        config.disable_caching = True  # relógio contínuo: hashes vivos não são reutilizáveis
        self.ox, self.oy, self.gs = ValueTracker(-3.8), ValueTracker(-0.65), ValueTracker(1.05)
        self.beta, self.tau = ValueTracker(0), ValueTracker(0)
        self.checkpoints, self.sections, self.layout_issues = [], [], []
        self.motion_windows=[]
        self.head = self.cap = self.formula = None
        self.clock = ValueTracker(0)
        self.clock.add_updater(lambda m, dt: m.increment_value(dt * 0.18))
        self.add(self.clock)

    def W(self, p):
        # Mesma projeção W do 5.1: texto fica no plano da tela.
        b, t = np.deg2rad([self.beta.get_value(), self.tau.get_value()])
        x, y, z = np.asarray(p, dtype=float)
        xp, zp = x * math.cos(b) + z * math.sin(b), -x * math.sin(b) + z * math.cos(b)
        return np.array([self.ox.get_value(), self.oy.get_value(), 0]) + self.gs.get_value() * np.array([xp, y * math.cos(t) + zp * math.sin(t), 0])

    def depth(self, p):
        b, t = np.deg2rad([self.beta.get_value(), self.tau.get_value()])
        x, y, z = p
        return (-x * math.sin(b) + z * math.cos(b)) * math.cos(t) - y * math.sin(t)

    def vec(self, a, v, color=WHITE, scale=1, width=LW_VEC):
        return arrow(self.W(a), self.W(np.asarray(a) + scale * np.asarray(v)), color, width,
                     z=4 + self.depth(a))

    def dynamic_last(self):
        # Cairo guarda o prefixo estático. Relógio/fluxo vêm depois da marca,
        # títulos e álgebra, para não redesenhar centenas de glifos nas pausas.
        # z_index continua determinando a sobreposição física dos objetos.
        static=[];trackers=[];dynamic=[]
        for m in self.mobjects:
            if isinstance(m,ValueTracker):trackers.append(m)
            elif m.get_family_updaters():dynamic.append(m)
            else:static.append(m)
        self.mobjects=static+trackers+dynamic

    def get_moving_and_static_mobjects(self,animations):
        moving,static=super().get_moving_and_static_mobjects(animations)
        # Cairo recebe raízes vivas, para reler os filhos quando uma construção
        # ganha/perde objetos. Evita renderizar filhos antigos após a troca.
        roots=[];seen=set()
        for m in moving:
            if id(m) not in seen:
                roots.append(m)
                seen.update(id(child) for child in m.get_family())
        return roots,static

    def play(self,*animations,**kwargs):
        self.dynamic_last()
        return super().play(*animations,**kwargs)

    def hold(self, d):
        self.update_mobjects(0)
        # Só a geometria derivada de estados constantes entra no cache estático.
        # Fluxos e relógio são objetos separados e continuam atualizando por dt.
        paused=[(m,list(m.updaters)) for m in self.mobjects if getattr(m,"state_geometry",False)]
        for m,_ in paused:m.clear_updaters(recursive=False)
        self.dynamic_last()
        try:
            self.wait(d,frozen_frame=False)
        finally:
            for m,updaters in paused:
                for updater in updaters:m.add_updater(updater)


    def flow(self, paths, count=7, direction=1):
        """Marcas convencionais de corrente; nunca representam velocidade de deriva.

        Reutiliza Dot e desloca pontos: sem TeX ou reconstrução de curvas por frame.
        paths recebe funções periódicas normalizadas, em coordenadas da tela.
        """
        g = VGroup()
        for path in paths:
            for k in range(count):
                dot = Dot(radius=0.045, color=CYAN).set_z_index(8)
                def move(m, p=path, phase=k/count):
                    sign = direction() if callable(direction) else direction
                    m.move_to(p((phase + sign*self.clock.get_value()) % 1))
                dot.add_updater(move)
                dot.update(0)
                g.add(dot)
        return g

    def cached(self, key, builder):
        """Reutiliza o desenho enquanto os estados geométricos não mudam."""
        last=[key()]
        group=builder()
        def update(m):
            state=key()
            if state!=last[0]:
                fresh=builder()
                # Troca a família inteira: align_data() acumula subobjetos
                # invisíveis quando uma vista retira vetores e rótulos.
                m.submobjects=fresh.submobjects
                m.points=fresh.points.copy()
                last[0]=state
        group.add_updater(update)
        group.state_geometry=True
        return group

    def view_key(self):
        return tuple(v.get_value() for v in (self.ox,self.oy,self.gs,self.beta,self.tau))

    def delcap(self):
        if self.cap is not None:
            self.play(FadeOut(self.cap), run_time=0.35)
            self.cap = None

    def out_symbol(self, p, sign=1, radius=0.15):
        g = VGroup(Circle(radius=radius,color=MAG).move_to(p))
        if sign > 0:
            g.add(Dot(p,radius=radius/3,color=MAG))
        else:
            g.add(Line(p+[-radius*.6,-radius*.6,0],p+[radius*.6,radius*.6,0],color=MAG),
                  Line(p+[-radius*.6,radius*.6,0],p+[radius*.6,-radius*.6,0],color=MAG))
        return g

    def fala(self, texto, minimo=2):
        self.hold(max(minimo, len(texto.split()) / 2.7))

    def motion(self, name, duration):
        self.motion_windows.append({"name":name,"part":self.renderer.num_plays,"duration":duration})

    def mark(self, name):
        self.checkpoints.append({"name": name, "time": round(float(self.time), 3), "part": self.renderer.num_plays})
        if os.environ.get("QA_STILLS"):
            self.update_mobjects(0)
            self.renderer.update_frame(self,ignore_skipping=True)
            out=Path(config.media_dir)/"estados"
            out.mkdir(parents=True,exist_ok=True)
            self.renderer.camera.get_image().save(out/f"{len(self.checkpoints):03d}_{name}.png")

        # Todos os textos estáticos, inclusive MathTex, em checkpoints narrativos.
        for root in self.mobjects:
            for m in root.get_family():
                if isinstance(m, MathTex) or m.__class__.__name__ == "Text":
                    if m.width and (m.get_left()[0] < -7.3 or m.get_right()[0] > 7.3 or m.get_bottom()[1] < -3.15 or m.get_top()[1] > 3.8):
                        # Cabeçalho e marca têm suas margens herdadas.
                        if root is not self.tag and root is not self.wm:
                            self.layout_issues.append({"checkpoint": name, "text": getattr(m, "tex_string", getattr(m, "text", "")), "bounds": [float(m.get_left()[0]), float(m.get_right()[0]), float(m.get_bottom()[1]), float(m.get_top()[1])]})

    def section(self, name, title=None):
        # Render cirúrgico pode herdar a fase exata do prefixo já codificado.
        if SEG and name in SEG.split(",") and os.environ.get("SEG_CLOCK_SEED") and not getattr(self,"_seed_applied",False):
            self.clock.set_value(float(os.environ["SEG_CLOCK_SEED"]))
            self._seed_applied=True
        print(f"[5.2] {name} — {float(self.time):.2f}s", flush=True)
        self.next_section(name, skip_animations=bool(SEG and name not in SEG.split(",")))
        self.sections.append({"name": name, "time": round(float(self.time), 3), "part": self.renderer.num_plays})
        if title:
            self.delcap()
            new = txt(title, 32).move_to([0, 3.05, 0])
            if self.head is not None:
                self.play(ReplacementTransform(self.head, new), run_time=0.8)
            else:
                self.play(FadeIn(new), run_time=0.8)
            self.head = new

    def caption(self, s, color=WHITE):
        # Space Grotesk não contém os gregos: notação matemática usa MathTex,
        # inclusive nas notas, como os captions mistos do 5.1.
        symbols = {"θ": r"\theta", "α": r"\alpha", "φ": r"\phi", "dφ":r"d\phi", "π": r"\pi",
                   "∝": r"\propto", "≫": r"\gg", "⟂":r"\perp", "dτ":r"d\tau", "τ":r"\tau", "dℓ": r"d\ell", "ℓ": r"\ell"}
        symbols.update({f"α{k}": rf"\alpha_{k}" for k in ("1", "2", "A", "B")})
        pieces = re.split(r"(dφ|[θαφπ][12AB]?|dℓ|dτ|[∝≫ℓ⟂τ])", s)
        if len(pieces) > 1:
            parts = [eq(symbols[p], size=30, color=color) if p in symbols else txt(p.strip(), T_NOTE, color)
                     for p in pieces if p.strip()]
            new = VGroup(*parts).arrange(RIGHT, buff=0.10).move_to([0, -2.8, 0])
        else:
            new = txt(s, T_NOTE, color).move_to([0, -2.8, 0])
        if new.width > 13.9:
            new.scale_to_fit_width(13.9)
        self.play(ReplacementTransform(self.cap, new) if self.cap else FadeIn(new), run_time=0.7)
        self.cap = new

    def show_eq(self, s, y=0.4, center=3.65, width=6.7, size=M_M, color=WHITE, matching=True):
        new = eq(s, size, color, width).move_to([center, y, 0])
        if self.formula is None:
            self.play(Write(new), run_time=1.2)
        elif matching:
            self.play(TransformMatchingTex(self.formula, new), run_time=1.5)
        else:
            self.play(FadeOut(self.formula), FadeIn(new), run_time=0.9)
        self.formula = new
        self.hold(2.0)
        return new

    def clear(self, keep=()):
        fixed = [self.tag, self.wm, self.head, *keep]
        mobs = [m for m in self.mobjects if all(m is not f for f in fixed) and not isinstance(m, ValueTracker)]
        # Congela só na saída; estado continua ativo durante toda a explicação.
        for m in mobs:
            m.clear_updaters(recursive=True)
        if mobs:
            self.play(*[FadeOut(m) for m in mobs], run_time=0.9)
        self.cap = self.formula = None

    def reset_view(self, x=-3.8, y=-0.65, scale=1.05, beta=0, tau=0):
        for tracker, val in [(self.ox, x), (self.oy, y), (self.gs, scale), (self.beta, beta), (self.tau, tau)]:
            tracker.set_value(val)

    def construct(self):
        self.wm = ImageMobject(str(WATERMARK_PATH)).set_width(WM_W).set_opacity(WM_OP).to_corner(UR, buff=0.3)
        self.tag = txt("ELETROMAGNETISMO · MAGNETOSTÁTICA", 18, opacity=0.6).to_corner(UL, buff=0.38)
        self.add(self.wm, self.tag)
        self.abertura()
        self.regime_magnetostatico()
        self.geometria_local()
        self.biot_savart()
        self.correntes_distribuidas()
        self.clinica_produto_vetorial()
        self.superposicao()
        self.metodo_geral()
        self.trecho_finito()
        self.limite_infinito()
        self.forca_entre_fios()
        self.espira_no_eixo()
        self.checagens_espira()
        self.sintese()
        self.fechamento()
        out = Path(config.media_dir) / "qa_timeline.json"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps({"sections": self.sections, "checkpoints": self.checkpoints,
                                   "layout_issues": self.layout_issues, "motion_windows":self.motion_windows, "duration": float(self.time), "plays":self.renderer.num_plays}, ensure_ascii=False, indent=2), encoding="utf-8")


    def wire_pair(self, I1, I2, d=3.8, center=0, forces=True, fields=True):
        B1, B2, F1, F2 = fios(I1, I2, d)
        g = VGroup()
        for j,(x,cur,force) in enumerate([(-d/2,I1,F1),(d/2,I2,F2)]):
            x += center
            g.add(Line([x,-1.8,0],[x,1.8,0],color=BLUE_L,stroke_width=LW_WIRE))
            if cur:
                sign=1 if cur>0 else -1
                g.add(arrow([x-.45,.5-.5*sign,0],[x-.45,.5+.5*sign,0],CYAN),
                      label('I_1' if j==0 else 'I_2',[x-.75,1.4,0],color=CYAN),
                      self.flow([lambda u,x=x:np.array([x,-1.8+3.6*u,0])],count=6,direction=sign))
            if forces:
                g.add(arrow([x,-.6,0],[x+force[0]*3.5,-.6,0],FC))
        if fields:
            point=np.array([center+d/2,.15,0])
            g.add(self.out_symbol(point, -1 if B1[2]<0 else 1),
                  label(r'\mathbf B_1',point+RIGHT*.65,color=MAG))
        return g


    def abertura(self):
        self.section('abertura','Como calcular o campo criado pela corrente?')
        pair=self.wire_pair(1,0,center=-3.6,forces=False,fields=False)
        self.play(FadeIn(pair),run_time=1.2)
        self.show_eq(r'I_1\ \longrightarrow\ \mathbf B_1',y=1.15,size=44)
        self.caption('A corrente do primeiro fio é a fonte do campo')
        self.hold(4)
        p=np.array([-1.7,.15,0])
        field=VGroup(self.out_symbol(p,-1),label(r'\mathbf B_1',p+RIGHT*.6,color=MAG))
        self.play(FadeIn(field),run_time=1)
        self.caption('Na posição do segundo fio: campo entrando na tela')
        self.mark('gancho_campo');self.hold(4)
        live=self.wire_pair(1,1,center=-3.6,forces=False,fields=False)
        pair.clear_updaters(recursive=True)
        self.play(FadeOut(pair),FadeIn(live),run_time=.7)
        force=arrow([-1.7,-.6,0],[-2.65,-.6,0],FC)
        self.play(Create(force),run_time=1)
        self.show_eq(r'\mathbf F_2=I_2\mathbf L\times\mathbf B_1',y=1.15)
        self.caption('O campo criado pelo fio 1 age na corrente do fio 2',FC)
        self.mark('gancho_dois_fios');self.hold(5)
        self.delcap()
        question=txt('Como calcular esse campo?',32).move_to([3.65,-.7,0])
        self.play(Write(question),run_time=1.2);self.hold(4)
        self.clear()
        title=official_text('LEI DE BIOT–SAVART',DISPLAY_FONT,BOLD,58).move_to([0,.5,0])
        self.play(Write(title),run_time=1.8);self.hold(3);self.mark('titulo')


    def regime_magnetostatico(self):
        self.section('regime','Corrente estacionária: fluxo sem acúmulo')
        self.clear()
        wire=Line([-6.5,0,0],[-.8,0,0],color=BLUE_L,stroke_width=6)
        region=Polygon([-4.9,-.75,0],[-2.5,-.75,0],[-2.5,.75,0],[-4.9,.75,0],color=VIOLET,fill_color=VIOLET,fill_opacity=.09)
        flow=self.flow([lambda u:np.array([-6.5+5.7*u,0,0])],count=10)
        self.play(Create(wire),Create(region),run_time=1.3);self.add(flow)
        incoming=VGroup(arrow([-6.2,.65,0],[-5.1,.65,0],CYAN),label(r'I_{\rm entra}',[-5.7,1.2,0],color=CYAN))
        outgoing=VGroup(arrow([-2.3,.65,0],[-1.2,.65,0],CYAN),label(r'I_{\rm sai}',[-1.7,1.2,0],color=CYAN))
        self.play(FadeIn(incoming),run_time=.8);self.play(FadeIn(outgoing),run_time=.8)
        charge=label('Q',[-3.7,-.4,0],color=BLUE_L)
        self.play(FadeIn(charge),run_time=.6)
        self.show_eq(r'\frac{dQ}{dt}=I_{\rm entra}-I_{\rm sai}',y=1.2)
        self.caption('O saldo de corrente altera a carga dentro da região')
        self.hold(5)
        self.show_eq(r'I_{\rm entra}=I_{\rm sai}\quad\Rightarrow\quad\frac{dQ}{dt}=0',y=1.2,size=36)
        self.caption('Entra e sai a mesma quantidade: Q permanece constante')
        self.mark('regime_balanco');self.hold(5)
        self.show_eq(r'\frac{\partial\rho}{\partial t}+\nabla\cdot\mathbf J=0',y=1.2)
        density=txt('Densidade constante em cada ponto',24).move_to([3.65,-.15,0])
        self.play(FadeIn(density),run_time=.7)
        self.show_eq(r'\frac{\partial\rho}{\partial t}=0\quad\Rightarrow\quad\nabla\cdot\mathbf J=0',y=1.2,size=36)
        self.caption('Sem acúmulo local; a corrente continua atravessando a região')
        nonzero=eq(r'\mathbf J\ne0',size=42).move_to([3.65,-1.1,0])
        self.play(Write(nonzero),run_time=.8);self.mark('regime_corrente_nao_nula');self.hold(5)
        self.play(FadeOut(density),FadeOut(nonzero),run_time=.6)
        self.show_eq(r'\frac{\partial\mathbf J}{\partial t}=0',y=1.2,matching=False)
        self.caption('Hipótese adicional: a distribuição de corrente também é constante')
        self.mark('regime_hipoteses');self.hold(5)


    def geometria_local(self):
        self.section('geometria','Construir a separação fonte–observador')
        self.clear();self.reset_view(x=-4,y=-.5,scale=1)
        self.theta_local=ValueTracker(math.pi/3)
        self.local=lambda:clinica(self.theta_local.get_value())
        path=ParametricFunction(lambda t:self.W([t,.12*(1-math.cos(1.3*t)),0]),t_range=[-2.6,2.6],color=BLUE_L,stroke_width=6)
        flow=self.flow([lambda u:self.W([-2.6+5.2*u,.12*(1-math.cos(1.3*(-2.6+5.2*u))),0])])
        self.play(Create(path),run_time=1.4);self.add(flow);self.hold(2)
        f=np.zeros(3);p=self.local()[1];o=np.array([-1.9,-1.35,0])
        source=Dot(self.W(f),color=CYAN,radius=.09)
        sl=txt('fonte',22,CYAN).move_to(self.W(f)+DOWN*.4)
        self.play(FadeIn(source),FadeIn(sl),run_time=.8)
        point=VGroup(Dot(self.W(p)),label('P',self.W(p)+UP*.3))
        self.play(FadeIn(point),run_time=.8);self.hold(2)
        origin=VGroup(Dot(self.W(o),radius=.05),label('O',self.W(o)+DOWN*.3))
        self.play(FadeIn(origin),run_time=.6)
        rp=self.vec(o,f-o,VIOLET,width=3);r=self.vec(o,p-o,VIOLET,width=3)
        rpl=label(r"\mathbf r'",self.W((o+f)/2)+LEFT*.25,color=VIOLET)
        rl=label(r'\mathbf r',self.W((o+p)/2)+LEFT*.3,color=VIOLET)
        self.play(Create(rp),FadeIn(rpl),run_time=1.2)
        self.play(Create(r),FadeIn(rl),run_time=1.2)
        R=self.vec(f,p-f,VIOLET);Rl=label(r'\mathbf R',self.W(.55*p)+RIGHT*.3,color=VIOLET)
        self.play(Create(R),FadeIn(Rl),run_time=1.2)
        self.show_eq(r"\mathbf r'+\mathbf R=\mathbf r",y=1.1,size=44)
        self.caption('Dois caminhos partem da mesma origem e chegam a P')
        self.hold(4)
        self.show_eq(r"\mathbf R=\mathbf r-\mathbf r'",y=1.1,size=44)
        self.caption('R aponta da fonte até o observador')
        self.hold(3)
        self.play(FadeOut(VGroup(origin,rp,r,rpl,rl,sl)),run_time=.8)
        dl=self.vec(f,[.75,0,0],CYAN,width=7)
        dll=label(r'd\boldsymbol\ell',self.W([.65,-.45,0]),color=CYAN)
        self.play(Create(dl),FadeIn(dll),run_time=1)
        arc=Arc(radius=.65,start_angle=0,angle=math.pi/3,arc_center=self.W(f),color=WHITE)
        th=label(r'\theta',self.W([.85,.4,0]))
        self.play(Create(arc),FadeIn(th),run_time=1)
        self.caption('dℓ é tangente ao fio; θ é o ângulo entre dℓ e R')
        self.mark('geometria_fonte_observador');self.hold(5)
        self.geom=[path,source,point,R,Rl,dl,dll,arc,th]
        self.geom_flow=flow


    def biot_savart(self):
        self.section('lei','Biot–Savart: uma lei experimental')
        self.clear();self.reset_view(x=-4.4,y=-.8,scale=1)
        self.theta_local.set_value(math.pi/3)
        diagram=self.cached(lambda:(self.theta_local.get_value(),*self.view_key()),self.local_diagram)
        flow=self.flow([lambda u:self.W([-1.4+2.8*u,0,0])],count=4)
        self.add(diagram,flow)
        self.show_eq(r'dB\propto I\,d\ell',y=1.25,size=46)
        self.caption('I e dℓ descrevem a intensidade e a extensão da fonte')
        self.play(Indicate(diagram[0],color=CYAN),run_time=1);self.hold(3)
        self.show_eq(r'dB\propto\frac{I\,d\ell}{R^2}',y=1.25,size=46)
        self.caption('A contribuição diminui com o quadrado da separação')
        self.play(Indicate(diagram[4],color=VIOLET),run_time=1);self.hold(3)
        self.show_eq(r'dB\propto\frac{I\,d\ell\sin\theta}{R^2}',y=1.25,size=44)
        self.caption('O seno seleciona a parte perpendicular do elemento')
        self.play(self.theta_local.animate.set_value(math.pi/2),run_time=2);self.hold(3)
        self.show_eq(r'dB=\frac{\mu_0}{4\pi}\frac{I\,d\ell\sin\theta}{R^2}',y=1.25,size=42)
        factor=VGroup(eq(r'\mu_0/(4\pi)',size=32),txt('fator no vácuo, em SI',23)).arrange(DOWN,buff=.2).move_to([3.65,-.25,0])
        self.play(FadeIn(factor),run_time=.8)
        self.caption('Lei experimental: ponto de partida para deduzir os campos das fontes')
        self.mark('lei_modulo');self.hold(5)
        self.play(FadeOut(factor),run_time=.6)
        self.show_eq(r'd\mathbf B=\frac{\mu_0 I}{4\pi}\frac{d\boldsymbol\ell\times\hat{\mathbf R}}{R^2}',y=1.25,size=40,matching=False)
        self.caption('A ordem dℓ × R fixa o sentido de dB pela mão direita')
        self.mark('lei_unitario');self.hold(4)
        unit=eq(r'\hat{\mathbf R}=\frac{\mathbf R}{R}',size=38).move_to([3.65,-.4,0])
        self.play(Write(unit),run_time=1)
        self.motion('unitario_R_adicional',8)
        self.show_eq(r'd\mathbf B=\frac{\mu_0 I}{4\pi}\frac{d\boldsymbol\ell\times(\mathbf R/R)}{R^2}',y=1.25,size=40)
        self.hold(3)
        self.show_eq(r'd\mathbf B=\frac{\mu_0 I}{4\pi}\frac{d\boldsymbol\ell\times\mathbf R}{R^2\,R}',y=1.25,size=40)
        self.caption('O R adicional veio da definição do vetor unitário')
        self.hold(3)
        self.show_eq(r'd\mathbf B=\frac{\mu_0 I}{4\pi}\frac{d\boldsymbol\ell\times\mathbf R}{R^3}',y=1.25,size=40)
        self.play(FadeOut(unit),run_time=.6);self.mark('lei_R_adicional');self.hold(3)


    def correntes_distribuidas(self):
        self.section('distribuidas','Da linha à superfície e ao volume')
        self.clear();self.reset_view(x=-4,y=-.3,scale=1)
        self.dist_w=ValueTracker(0);self.dist_h=ValueTracker(0)
        def project(x,y,z):
            # Perspectiva só nasce com a espessura; superfície inicial é plana.
            h=self.dist_h.get_value()
            return np.array([-4+x+.4*h*y,-.7+y+.55*z,0])
        def geometry():
            w=self.dist_w.get_value();h=self.dist_h.get_value()
            g=VGroup(Line(project(-2.4,0,0),project(2.4,0,0),color=BLUE_L,stroke_width=6))
            if w>.01:
                g.add(Polygon(*[project(x,y,h) for x,y in [(-2.4,-w),(2.4,-w),(2.4,w),(-2.4,w)]],color=BLUE_L,fill_color=BLUE_L,fill_opacity=.12,stroke_width=2))
                for y in np.linspace(-w,w,5):g.add(Line(project(-2.4,y,h),project(2.4,y,h),color=BLUE_L,stroke_width=1.5).set_opacity(.4))
                if h>.01:
                    for y in [-w,w]:
                        g.add(Polygon(project(-2.4,y,0),project(2.4,y,0),project(2.4,y,h),project(-2.4,y,h),color=BLUE_L,fill_color=BLUE_L,fill_opacity=.1,stroke_width=2))
            return g
        geometry_live=self.cached(lambda:(self.dist_w.get_value(),self.dist_h.get_value()),geometry)
        paths=[lambda u,y=y,z=z:project(-2.4+4.8*u,y*self.dist_w.get_value(),z*self.dist_h.get_value()) for y in [-1,-.5,0,.5,1] for z in [0,1]]
        # As faixas se separam ao aumentar a largura; a espessura separa as camadas.
        flows=self.flow(paths,count=5)
        self.add(geometry_live,flows)
        selected=Line(project(-.4,0,0),project(.4,0,0),color=CYAN,stroke_width=10)
        self.play(Create(selected),run_time=.8)
        self.show_eq(r'I\,d\boldsymbol\ell',y=1.4,size=52)
        self.caption('I: corrente no fio; dℓ: comprimento orientado que será somado')
        self.mark('distribuicao_linha');self.hold(5)
        self.show_eq(r'\mathbf B=\frac{\mu_0}{4\pi}\int\frac{I\,d\boldsymbol\ell\times\hat{\mathbf R}}{R^2}',y=1.4,size=36)
        self.hold(3)
        self.delcap();self.play(FadeOut(selected),self.dist_w.animate.set_value(.8),run_time=2.5)
        patch=Polygon(*[project(x,y,0) for x,y in [(-.4,-.3),(.4,-.3),(.4,.3),(-.4,.3)]],color=CYAN,fill_color=CYAN,fill_opacity=.25)
        self.play(Create(patch),run_time=.8)
        self.show_eq(r'\mathbf K\,da',y=1.4,size=52,matching=False)
        meaning=VGroup(eq(r'[\mathbf K]=\mathrm{A/m}',size=32),eq(r'da=d\ell\,dw',size=32)).arrange(DOWN,buff=.45).move_to([3.65,-.2,0])
        self.play(FadeIn(meaning),run_time=.8)
        self.caption('K: corrente por largura; da: área do elemento da superfície')
        self.hold(4)
        self.show_eq(r'(K\,dw)\,d\ell=K\,da',y=1.4,size=40,matching=False)
        self.mark('distribuicao_superficie');self.hold(4)
        self.show_eq(r'\mathbf B=\frac{\mu_0}{4\pi}\int\frac{\mathbf K\times\hat{\mathbf R}}{R^2}\,da',y=1.4,size=36,matching=False)
        self.hold(3)
        self.delcap();self.play(FadeOut(patch),FadeOut(meaning),self.dist_h.animate.set_value(.9),run_time=2.5)
        block=VGroup()
        for z in [0,.9]:
            block.add(Polygon(*[project(x,y,z) for x,y in [(-.4,-.3),(.4,-.3),(.4,.3),(-.4,.3)]],color=CYAN,fill_color=CYAN,fill_opacity=.2))
        for x in [-.4,.4]:
            for y in [-.3,.3]:block.add(Line(project(x,y,0),project(x,y,.9),color=CYAN))
        self.play(Create(block),run_time=1)
        self.show_eq(r'\mathbf J\,d\tau',y=1.4,size=52,matching=False)
        meaning2=VGroup(eq(r'[\mathbf J]=\mathrm{A/m^2}',size=32),eq(r'd\tau=d\ell\,dA_\perp',size=32)).arrange(DOWN,buff=.45).move_to([3.65,-.2,0])
        self.play(FadeIn(meaning2),run_time=.8)
        self.caption('J: corrente por área transversal; dτ: volume do elemento-fonte')
        self.hold(4)
        self.show_eq(r'(J\,dA_\perp)\,d\ell=J\,d\tau',y=1.4,size=40,matching=False)
        self.mark('distribuicao_volume');self.hold(4)
        self.play(FadeOut(meaning2),run_time=.7)
        self.show_eq(r'\mathbf B=\frac{\mu_0}{4\pi}\int\frac{\mathbf J\times\hat{\mathbf R}}{R^2}\,d\tau',y=1.4,size=36,matching=False)
        self.caption('A medida de integração acompanha a distribuição da fonte')
        self.hold(4)


    def local_diagram(self):
        f,p,dl,Rv,b=clinica(self.theta_local.get_value());th=self.theta_local.get_value()
        g=VGroup(Line(self.W([-1.4,0,0]),self.W([1.4,0,0]),color=BLUE_L,stroke_width=6),
                 Dot(self.W(f),radius=.07,color=CYAN),Dot(self.W(p),radius=.09),
                 self.vec(f,dl,CYAN),self.vec(f,Rv,VIOLET),
                 label('P',self.W(p)+UP*.3),label(r'd\boldsymbol\ell',self.W([.4,-.45,0]),color=CYAN),
                 label(r'\mathbf R',self.W(.55*Rv)+LEFT*.3,color=VIOLET))
        g.add(ParametricFunction(lambda u:self.W([2.6*math.cos(u),2.6*math.sin(u),0]),t_range=[0,math.pi/2],color=VIOLET,stroke_width=1.5).set_stroke(opacity=.3))
        if th>1e-4:
            g.add(ParametricFunction(lambda u:self.W([.65*math.cos(u),.65*math.sin(u),0]),t_range=[0,th],color=WHITE,stroke_width=2),
                  label(r'\theta',self.W([.9*math.cos(th/2),.9*math.sin(th/2),0])))
        if np.linalg.norm(b)>1e-5:
            if abs(self.tau.get_value())<1e-5:
                g.add(self.out_symbol(self.W(p)+RIGHT*.25,1,radius=.17*math.sin(th)),
                      label(r'd\mathbf B',self.W(p)+RIGHT*.8,color=MAG))
            else:
                g.add(self.vec(p,b,MAG,scale=25),label(r'd\mathbf B',self.W(p+25*b)+RIGHT*.35,color=MAG))
        return g

    def clinica_produto_vetorial(self):
        self.section("clinica", "Isolar o efeito do ângulo")
        self.clear()
        self.reset_view(x=-4.6, y=-0.8, scale=1, beta=0, tau=0)
        self.theta_local.set_value(0)
        diagram = self.cached(lambda:(self.theta_local.get_value(),*self.view_key()),self.local_diagram)
        self.add(diagram,self.flow([lambda u:self.W([-1.4+2.8*u,0,0])],count=4))
        self.show_eq(r"dB\propto\sin\theta", y=1.5, color=MAG)
        fixed = eq(r"I,\ d\ell,\ R:\ \mathrm{constantes}", size=30).move_to([3.65,0.4,0])
        nums = VGroup(eq(r"\theta=", size=30), DecimalNumber(0, num_decimal_places=0, unit=r"^\circ", font_size=30),
                      eq(r"\sin\theta=", size=30), DecimalNumber(0, num_decimal_places=2, font_size=30)).arrange(RIGHT,buff=0.18).move_to([3.65,-0.5,0])
        nums[1].add_updater(lambda m: m.set_value(math.degrees(self.theta_local.get_value())))
        nums[3].add_updater(lambda m: m.set_value(math.sin(self.theta_local.get_value())))
        bar = always_redraw(lambda: Line([1.2,-1.5,0], [1.2+4.7*max(1e-6,math.sin(self.theta_local.get_value())),-1.5,0],color=MAG,stroke_width=12))
        status = always_redraw(lambda: label(
            r"dB=0" if abs(self.theta_local.get_value())<1e-6 else
            (r"dB=dB_{\max}" if abs(self.theta_local.get_value()-math.pi/2)<1e-6 else r"dB=dB_{\max}\sin\theta"),
            [3.65,-2.1,0], size=30, color=MAG))
        nums.update(0)
        for m, x in zip(nums, [1.7, 2.65, 4.2, 5.6]):
            m.move_to([x, -0.5, 0])
        self.play(FadeIn(fixed),FadeIn(nums),FadeIn(bar),FadeIn(status),run_time=1)
        self.caption("θ = 0: dB deste elemento é zero; a corrente continua")
        self.fala("Mantenha agora o elemento de corrente fixo. E mova o ponto de observação sem alterar sua distância à fonte. Assim, corrente, comprimento do elemento e distância permanecem constantes. Só o ângulo muda.")
        self.mark("clinica_zero")
        self.fala("Quando o ângulo vale zero, o seno também vale zero e a contribuição desaparece.")
        self.caption("Só θ muda: seno e dB acompanham o mesmo observador")
        for angle, name in [(30,"clinica_30"),(60,"clinica_60"),(90,"clinica_90")]:
            self.play(self.theta_local.animate.set_value(math.radians(angle)),run_time=3,rate_func=linear)
            self.mark(name)
            self.hold(3)
        self.caption("θ = 90°: dB máximo para estes I, dℓ e R; não é B total")
        self.fala("Quando o ângulo chega a noventa graus, o seno vale um e a contribuição é máxima para aquela distância. Nos ângulos intermediários, ela varia exatamente como o seno do ângulo.")
        self.caption("Mão direita: dedos de dℓ para R; polegar no sentido de dB")
        turn = always_redraw(lambda: ParametricFunction(lambda u:self.W([1.05*math.cos(u),1.05*math.sin(u),0]),t_range=[0,math.pi/2],color=CYAN,stroke_width=4))
        turn_tip=always_redraw(lambda: self.vec([0.04,1.05,0],[-0.3,0,0],CYAN,width=4))
        self.play(Create(turn),FadeIn(turn_tip),run_time=2)
        self.play(self.beta.animate.set_value(40),self.tau.animate.set_value(60),run_time=3)
        self.fala("Mas o produto vetorial também determina uma direção. Primeiro o elemento de corrente. Depois o vetor de separação. A regra da mão direita fornece a direção da contribuição de campo. Trocar a ordem dos dois vetores inverteria o resultado.")
        self.mark("clinica_perpendicular_espacial")
        self.play(FadeOut(turn),FadeOut(turn_tip),run_time=0.7)


    def superposicao(self):
        self.section('superposicao','Construir uma soma vetorial')
        self.clear();self.reset_view(x=-4,y=-.9,scale=.9,beta=0,tau=40)
        wire=Line(self.W([-2.5,0,0]),self.W([2.5,0,0]),color=BLUE_L,stroke_width=6)
        P=np.array([0,2.1,0]);p=self.W(P)
        flow=self.flow([lambda u:self.W([-2.5+5*u,0,0])])
        self.play(Create(wire),FadeIn(Dot(p)),FadeIn(label('P',p+LEFT*.35+UP*.2)),run_time=1);self.add(flow)
        self.caption('Um observador; uma contribuição por elemento da fonte')
        base=np.array([2.5,-2.1,0]);start=base.copy();chain=VGroup()
        for i,x in enumerate(np.linspace(-2,2,5)):
            f,pt,dl,Rv,rm,th,al,b=trecho(x,dl=1.)
            source=VGroup(Dot(self.W(f),color=CYAN),self.vec(f,dl,CYAN),self.vec(f,Rv,VIOLET,width=2))
            contribution=self.vec(pt,b,MAG,scale=8)
            self.play(FadeIn(source),Create(contribution),run_time=.8)
            delta=self.W(pt+8*b)-self.W(pt);target=arrow(base,base+delta,MAG,width=4,tip=.15)
            self.motion(f"soma_elemento_{i}",1.1)
            self.play(TransformFromCopy(contribution,target),run_time=1.1)
            chain.add(target);base+=delta
            self.play(FadeOut(source),FadeOut(contribution),run_time=.4)
        total=arrow(start+RIGHT*.7,base+RIGHT*.7,MAG,width=7)
        self.play(Create(total),run_time=1.2)
        self.show_eq(r'\mathbf B_N=\sum_{i=1}^{N}\Delta\mathbf B_i',y=2.15,size=40)
        self.caption('A resultante liga a origem à ponta final da soma')
        self.mark('soma_ponta_cauda');self.hold(4)
        small=VGroup(*[Line(self.W([x,0,0]),self.W([x+.14,0,0]),color=CYAN,stroke_width=8) for x in np.arange(-2.5,2.4,.25)])
        self.play(Create(small),run_time=2)
        fine=VGroup();tip=start.copy()
        for x in np.linspace(-2.375,2.375,20):
            b=trecho(x,dl=.25)[-1]
            delta=self.W(P+8*b)-self.W(P)
            fine.add(arrow(tip,tip+delta,MAG,width=3,tip=.08));tip+=delta
        self.play(ReplacementTransform(chain,fine),Transform(total,arrow(start+RIGHT*.7,tip+RIGHT*.7,MAG,width=7)),run_time=2)
        self.show_eq(r'\Delta\ell\to0,\quad N\to\infty',y=2.15,size=40,matching=False)
        self.caption('Refinar a fonte: mais elementos, cada contribuição menor')
        self.hold(4)
        self.show_eq(r'\mathbf B=\int d\mathbf B',y=2.15,size=46,matching=False)
        self.mark('integral_superposicao');self.hold(4)


    def metodo_geral(self):
        self.section('metodo','Aplicar o método ao desenho')
        self.clear();self.reset_view(x=-4,y=-1,scale=1)
        wire=Line(self.W([-2.5,0,0]),self.W([2.5,0,0]),color=BLUE_L,stroke_width=6)
        P=self.W([0,2.1,0]);f=self.W([1.5,0,0])
        flow=self.flow([lambda u:self.W([-2.5+5*u,0,0])])
        self.play(Create(wire),FadeIn(Dot(P)),FadeIn(label('P',P+UP*.3)),run_time=1);self.add(flow)
        self.caption('Fonte e observador: quem produz o campo, e onde calculá-lo?');self.hold(3)
        sep=arrow(f,P,VIOLET)
        self.play(FadeIn(Dot(f,color=CYAN)),Create(sep),run_time=1)
        self.show_eq(r'\mathbf R=\mathbf r-\mathbf r\prime',y=1.2,size=42)
        self.caption('Separação: a geometria fornece distância e direção');self.hold(3)
        out=self.out_symbol(P+RIGHT*.3)
        self.play(FadeIn(out),run_time=.7)
        self.caption('Direção e simetria: aqui todas as parcelas apontam para fora');self.hold(3)
        limits=VGroup(label('x_A',self.W([-2.5,-.4,0])),label('x_B',self.W([2.5,-.4,0])))
        self.play(FadeIn(limits),run_time=.8)
        self.show_eq(r'd\boldsymbol\ell=dx\,\hat x',y=1.2,size=42)
        self.caption('Variável e limites: percorrer o trecho em x');self.hold(3)
        self.show_eq(r'B_{\rm trecho}=\int_{x_A}^{x_B}dB',y=1.2,size=42)
        self.mark('metodo_aplicado');self.hold(3)

    def segment_diagram(self, alpha=False, theta=True, components=False):
        x=self.x_src.get_value()
        f,p,dl,Rv,rm,th,al,b=trecho(x)
        g=VGroup(Line(self.W([-2.6,0,0]),self.W([2.6,0,0]),color=BLUE_L,stroke_width=6),
                 DashedLine(self.W([0,0,0]),self.W(p),color=VIOLET,stroke_width=2),
                 Dot(self.W(f),color=CYAN,radius=0.07),Dot(self.W(p),radius=0.09),
                 self.vec(f,dl,CYAN),self.vec(f,Rv,VIOLET),
                 (self.out_symbol(self.W(p)+RIGHT*.22) if abs(self.tau.get_value())<.001 else self.vec(p,b,MAG,scale=18)),
                 label("P=(0,a)",self.W(p)+LEFT*.75+UP*.28,size=28),label("a",self.W([0,1,0])+LEFT*0.25),
                 label("x",self.W([x,-0.5,0])),label(r"d\boldsymbol\ell",self.W(f+np.array([0.3,-0.75,0])),size=28,color=CYAN),
                 label(r"\mathbf R",self.W(f+0.55*Rv)+RIGHT*0.3,color=VIOLET))
        g.add(arrow(self.W([-2.9,0,0]),self.W([2.9,0,0]),VIOLET,width=1.4,z=0),label(r"x_{\rm eixo}",self.W([2.85,.35,0]),size=24,color=VIOLET))
        if abs(x)>.3:
            sign=1 if x>0 else -1
            g.add(VMobject(color=WHITE,stroke_width=2).set_points_as_corners([self.W([.2*sign,0,0]),self.W([.2*sign,.2,0]),self.W([0,.2,0])]))
        if theta:
            g.add(ParametricFunction(lambda u:self.W(f+0.5*np.array([math.cos(u),math.sin(u),0])),t_range=[0,th],color=WHITE,stroke_width=2),label(r"\theta",self.W(f+0.75*np.array([math.cos(th/2),math.sin(th/2),0])),size=28))
        if alpha and abs(al)>1e-4:
            # Em P, ambas as semirretas são invertidas: mesmo ângulo orientado.
            g.add(ParametricFunction(lambda u:self.W(p+0.65*np.array([math.sin(u),-math.cos(u),0])),t_range=[min(0,al),max(0,al)],color=CYAN,stroke_width=3),label(r"\alpha",self.W(p+0.95*np.array([math.sin(al/2),-math.cos(al/2),0])),color=CYAN,size=28))
        if components:
            g.add(self.vec(f,[-x,0,0],VIOLET,width=4),self.vec([0,0,0],[0,2.1,0],CYAN,width=4))
        return g

    def trecho_finito(self):
        self.section("trecho", "Contribuição de um trecho retilíneo do circuito")
        self.clear()
        self.reset_view(x=-3.9,y=-1.05,scale=1,beta=0,tau=0)
        self.x_src=ValueTracker(1.7)
        self.seg_alpha=False;self.seg_theta=False;self.seg_components=False
        diagram=self.cached(lambda:(self.x_src.get_value(),self.seg_alpha,self.seg_theta,self.seg_components,*self.view_key()),lambda:self.segment_diagram(self.seg_alpha,self.seg_theta,self.seg_components))
        circuit=VMobject(color=BLUE_L,stroke_width=3).set_points_as_corners([self.W([2.6,0,0]),self.W([2.6,-1.3,0]),self.W([-2.6,-1.3,0]),self.W([-2.6,0,0])]).set_stroke(opacity=0.3)
        flow=VGroup(self.vec([1.9,0,0],[0.6,0,0],CYAN),self.vec([0,-1.3,0],[-0.7,0,0],CYAN,width=3).set_opacity(0.5))
        self.segment_flow=self.flow([lambda u:self.W([-2.6+5.2*u,0,0])])
        self.add(diagram,self.segment_flow)
        self.play(Create(circuit),FadeIn(flow),run_time=1.4)
        self.show_eq(r"\mathbf B_{\rm total}=\mathbf B_{\rm trecho}+\mathbf B_{\rm restante}",y=0.6,size=32)
        self.caption("Calculamos B do trecho; o restante do circuito também pode contribuir")
        self.fala("Considere um trecho retilíneo finito de um circuito percorrido por corrente estacionária. Vamos calcular a contribuição desse trecho para o campo no ponto escolhido. O restante do circuito pode produzir outras contribuições.")
        self.mark("trecho_circuito_fechado")
        self.play(FadeOut(circuit),FadeOut(flow),run_time=0.8)
        self.show_eq(r"d\boldsymbol\ell=dx\,\hat x",y=1.2)
        eR=eq(r"\mathbf R=-x\hat x+a\hat y",color=VIOLET).move_to([3.65,-0.05,0])
        eMag=eq(r"R=\sqrt{x^2+a^2}",size=34).move_to([3.65,-1.15,0])
        self.play(FadeIn(eR),FadeIn(eMag),run_time=1)
        self.fala("Coloque o trecho sobre o eixo horizontal, com corrente para a direita. O ponto de observação está a uma distância perpendicular a. Para um elemento na posição x, o elemento de comprimento é dx na direção horizontal. Do elemento até o observador, o vetor de separação tem uma componente horizontal e outra vertical.")
        self.mark("trecho_modelagem")
        self.play(FadeOut(eR),FadeOut(eMag),run_time=0.7)
        self.delcap()
        self.seg_components=True
        self.show_eq(r"d\boldsymbol\ell\times\mathbf R=dx\hat x\times(-x\hat x+a\hat y)",y=1.2,size=34)
        self.caption("A componente paralela ao fio não contribui")
        self.show_eq(r"dx\hat x\times(-x\hat x)=0",y=1.2)
        self.fala("Agora observe o produto vetorial. A componente do vetor de separação paralela ao fio não contribui.")
        self.mark("trecho_componente_paralela_zero")
        self.caption("A componente perpendicular define o sentido +z")
        self.show_eq(r"dx\hat x\times(a\hat y)=a\,dx\,\hat z",y=1.2)
        # Mesma geometria inclinada: o +z sai efetivamente do plano.
        self.play(self.beta.animate.set_value(18),self.tau.animate.set_value(40),run_time=2)
        self.fala("O termo que sobrevive é o perpendicular. Por isso o produto vetorial aponta no sentido positivo do eixo z.")
        self.show_eq(r"d\mathbf B=\frac{\mu_0I}{4\pi}\frac{a\,dx}{(x^2+a^2)^{3/2}}\,\hat z",y=0.9,size=36)
        self.seg_components=False;self.seg_theta=True
        self.caption("Ao mover a fonte, a intensidade muda; o sentido de dB permanece +z")
        # Números derivados do MESMO x_src; sem MathTex recompilado por quadro.
        numbers=VGroup(eq("x=",size=28),DecimalNumber(1.7,num_decimal_places=2,font_size=28),eq("R=",size=28),DecimalNumber(0,num_decimal_places=2,font_size=28)).arrange(RIGHT,buff=0.15).move_to([3.65,-0.4,0])
        numbers[1].add_updater(lambda m:m.set_value(self.x_src.get_value()))
        numbers[3].add_updater(lambda m:m.set_value(trecho(self.x_src.get_value())[4]))
        angles=VGroup(eq(r"\theta=",size=28),DecimalNumber(0,num_decimal_places=1,unit=r"^\circ",font_size=28),eq(r"\alpha=",size=28,color=CYAN),DecimalNumber(0,num_decimal_places=1,unit=r"^\circ",font_size=28)).arrange(RIGHT,buff=0.15).move_to([3.65,-1.2,0])
        angles[1].add_updater(lambda m:m.set_value(math.degrees(trecho(self.x_src.get_value())[5])))
        angles[3].add_updater(lambda m:m.set_value(math.degrees(trecho(self.x_src.get_value())[6])))
        numbers.update(0)
        for m, xx in zip(numbers, [1.7, 2.75, 4.45, 5.65]):
            m.move_to([xx, -0.4, 0])
        self.play(FadeIn(numbers),run_time=0.8)
        for x in [-2.1,0,2.1]:
            self.play(self.x_src.animate.set_value(x),run_time=3,rate_func=linear)
            self.mark(f"trecho_x_{x}");self.hold(2)
        self.fala("Ao mover o elemento, o vetor de separação muda, a distância muda e a intensidade muda. Mas o sentido de cada contribuição permanece igual ao longo de todo esse trecho. Só agora vamos integrar.")
        self.play(FadeOut(numbers),self.beta.animate.set_value(0),self.tau.animate.set_value(0),run_time=1.5)
        self.seg_alpha=True
        angles.update(0)  # família dos números estabilizada antes do FadeIn
        for m, xx in zip(angles, [1.75, 2.95, 4.55, 5.7]):
            m.move_to([xx, -1.2, 0])
        self.play(FadeIn(angles),run_time=0.8)
        self.caption("θ: entre dℓ e R    ·    α: medido a partir da perpendicular")
        self.show_eq(r"\tan\alpha=\frac{x}{a}",y=1.25,color=CYAN)
        self.fala("Poderíamos integrar em x. Mas a própria geometria sugere uma variável melhor. Agora introduzimos um novo ângulo, alfa, medido em relação à perpendicular ao trecho. Esse não é o ângulo de Biot Savart. Alfa é apenas uma coordenada conveniente para esta geometria.")
        self.mark("triangulo_alpha")
        self.delcap()
        self.show_eq(r"x=a\tan\alpha",y=1.25,color=CYAN)
        self.fala("Pelo triângulo, a tangente do ângulo é a razão entre x e a. Então x é a vezes a tangente de alfa.")
        self.play(FadeOut(angles),run_time=0.7)
        self.seg_theta=False
        self.show_eq(r"dx=a\sec^2\alpha\,d\alpha",y=1.25)
        aux=eq(r"x^2+a^2=a^2(1+\tan^2\alpha)",size=30,width=6.5).move_to([3.65,-0.1,0])
        self.play(FadeIn(aux),run_time=0.8);self.hold(3)
        auxsec=eq(r"x^2+a^2=a^2\sec^2\alpha",size=32,width=6.5).move_to(aux)
        self.play(TransformMatchingTex(aux,auxsec),run_time=1.5);self.hold(3)
        aux2=eq(r"(x^2+a^2)^{3/2}=a^3\sec^3\alpha",size=32,width=6.5).move_to(aux)
        self.play(TransformMatchingTex(auxsec,aux2),run_time=1.5);self.hold(3)
        self.fala("O diferencial recebe o fator a vezes secante ao quadrado. E o denominador fica a ao cubo vezes secante ao cubo.")
        self.mark("substituicao_diferencial_denominador")
        self.play(FadeOut(aux2),run_time=0.6)
        self.show_eq(r"dB=\frac{\mu_0I}{4\pi}\frac{a(a\sec^2\alpha\,d\alpha)}{a^3\sec^3\alpha}",y=0.7,size=36)
        simplify=eq(r"\frac{a^2}{a^3}=\frac1a,\qquad\frac{\sec^2\alpha}{\sec^3\alpha}=\cos\alpha",size=32,width=6.5).move_to([3.65,-.9,0])
        self.play(Write(simplify),run_time=1.4);self.hold(4)
        self.show_eq(r"dB=\frac{\mu_0I}{4\pi a}\cos\alpha\,d\alpha",y=0.7)
        self.play(FadeOut(simplify),run_time=.6)
        self.fala("Os fatores de a se simplificam. A razão entre secante ao quadrado e secante ao cubo vira cosseno. A integral se reduz a uma integral de cosseno.")
        self.mark("integrando_alpha")
        self.delcap()
        self.show_eq(r"B_{\rm trecho}=\frac{\mu_0I}{4\pi a}\int_{\alpha_A}^{\alpha_B}\cos\alpha\,d\alpha",y=0.7,size=36)
        self.show_eq(r"B_{\rm trecho}=\frac{\mu_0I}{4\pi a}[\sin\alpha]_{\alpha_A}^{\alpha_B}",y=0.7,size=36)
        self.show_eq(r"B_{\rm trecho}=\frac{\mu_0I}{4\pi a}(\sin\alpha_B-\sin\alpha_A)",y=0.7,size=36)
        self.fala("Integrando de uma extremidade à outra, obtemos o seno no limite superior menos o seno no limite inferior.")
        for x in [-2.6,2.6]:
            self.play(self.x_src.animate.set_value(x),run_time=2)
            self.caption("Extremidade esquerda: αA < 0" if x<0 else "Extremidade direita: αB > 0")
            self.mark("alpha_esquerda" if x<0 else "alpha_direita");self.hold(3)
        signs=eq(r"\alpha_A=-\alpha_1,\quad\alpha_B=\alpha_2",size=30,color=CYAN).move_to([3.65,-0.8,0])
        self.play(FadeIn(signs),run_time=0.9)
        self.caption("α1 e α2 são módulos positivos dos ângulos das extremidades")
        self.fala("No lado esquerdo, alfa é negativo. No direito, é positivo. Se representarmos os módulos positivos dos ângulos das duas extremidades por alfa um e alfa dois, a diferença dos senos se transforma em uma soma.")
        self.show_eq(r"B_{\rm trecho}=\frac{\mu_0I}{4\pi a}(\sin\alpha_1+\sin\alpha_2)",y=0.7,size=36)
        bx=box(self.formula,MAG);self.play(FadeIn(bx),run_time=0.6)
        self.mark("resultado_trecho_finito")
        self.fala("Esse é o campo produzido por esse trecho retilíneo no ponto escolhido.")
        self.play(FadeOut(signs),FadeOut(bx),run_time=0.7)
        self.segment_group=diagram

    def limite_infinito(self):
        self.section("infinito", "O fio infinito como limite")
        # Fórmula finita permanece; apenas sua geometria dá lugar aos extremos móveis.
        self.segment_group.clear_updaters();self.play(FadeOut(self.segment_group),run_time=0.8)
        self.L_wire=ValueTracker(2.6)
        # Evitar comprimir a geometria angular: projetar extensões reais e recortar na região visual.
        def real_geometry():
            L=self.L_wire.get_value();a=2.1;P=self.W([0,a,0]);g=VGroup()
            clip=2.95;end=min(L,clip)
            g.add(Line(self.W([-end,0,0]),self.W([end,0,0]),color=BLUE_L,stroke_width=6),Dot(P),DashedLine(self.W([0,0,0]),P,color=VIOLET),label("P",P+UP*0.3),label("a",self.W([0,1.,0])+LEFT*.3))
            for sign in [-1,1]:
                # Raios para extremos reais: quando saem do frame, continuam com a inclinação correta.
                frac=min(1,clip/L)
                e=np.array([sign*L*frac,a*(1-frac),0])
                g.add(Line(P,self.W(e),color=VIOLET,stroke_width=2))
                if L<=clip:g.add(Dot(self.W([sign*L,0,0]),color=CYAN))
                al=math.atan2(L,a)
                g.add(ParametricFunction(lambda u,s=sign:self.W([0,a,0]+0.65*np.array([s*math.sin(u),-math.cos(u),0])),t_range=[0,al],color=CYAN,stroke_width=2))
            return g
        diagram=self.cached(lambda:(self.L_wire.get_value(),*self.view_key()),real_geometry);self.add(diagram)
        nums=VGroup(eq(r"\alpha_1=\alpha_2=",size=30,color=CYAN),DecimalNumber(0,num_decimal_places=1,unit=r"^\circ",font_size=30)).arrange(RIGHT,buff=0.2).move_to([3.65,-0.9,0])
        nums[1].add_updater(lambda m:m.set_value(math.degrees(math.atan2(self.L_wire.get_value(),2.1))))
        nums.update(0)
        nums[0].move_to([2.9, -0.9, 0])
        nums[1].move_to([5.2, -0.9, 0])
        self.play(FadeIn(nums),run_time=0.9)
        self.caption("As extremidades se afastam; α1 e α2 tendem a 90°")
        self.play(self.L_wire.animate.set_value(25),run_time=7,rate_func=smooth)
        self.mark("extremidades_distantes")
        self.fala("Agora imagine as duas extremidades se afastando indefinidamente. Os dois ângulos tendem a noventa graus. Os dois senos tendem a um.")
        nums.clear_updaters(recursive=True)
        limit_angles=eq(r"\alpha_1,\alpha_2\longrightarrow90^\circ",size=30,color=CYAN).move_to([3.65,-0.9,0])
        self.remove(nums)
        self.add(limit_angles)
        sins=eq(r"\sin\alpha_1\to1,\quad\sin\alpha_2\to1",size=30).move_to([3.65,-1.7,0])
        self.play(Write(sins),run_time=1);self.hold(3)
        self.show_eq(r"B_\infty=\frac{\mu_0I}{4\pi a}(1+1)",y=0.7)
        self.show_eq(r"B_\infty=\frac{\mu_0I}{2\pi a}",y=0.7,color=MAG)
        self.caption("B ∝ 1/a: o resultado nasce do limite do trecho finito")
        self.mark("resultado_fio_infinito")
        self.fala("O resultado do fio infinito apareceu como limite do caso mais geral.")

    def forca_entre_fios(self):
        self.section("fios", "A corrente cria o campo que produz a força")
        self.clear()
        self.I1=1.;self.I2=1.;self.d=3.8
        group=self.wire_pair(self.I1,0,self.d,center=-3.8,forces=False,fields=False)
        self.play(FadeIn(group),run_time=1.2)
        self.show_eq(r"B_1=\frac{\mu_0I_1}{2\pi d}",y=1.3,color=MAG)
        B1=fios(self.I1,self.I2,self.d)[0]
        p=np.array([-1.9,0.15,0])
        # B1 aponta para dentro da tela no fio direito: símbolo da convenção 5.1.
        symbol=VGroup(Circle(radius=0.18,color=MAG).move_to(p),label(r"\mathbf B_1",p+RIGHT*0.55,color=MAG))
        if B1[2]<0:
            symbol.add(Line(p+[-0.1,-0.1,0],p+[0.1,0.1,0],color=MAG),Line(p+[-0.1,0.1,0],p+[0.1,-0.1,0],color=MAG))
        else:
            symbol.add(Dot(p,color=MAG,radius=0.05))
        dim=VGroup(DashedLine([-5.7,-2.1,0],[-1.9,-2.1,0],color=VIOLET),label("d",[-3.8,-2.3,0]))
        self.play(FadeIn(symbol),FadeIn(dim),run_time=1)
        self.caption("Primeiro: o campo do fio 1 na posição do fio 2")
        self.fala("Agora podemos voltar à situação que abriu o vídeo. O primeiro fio produz um campo na posição do segundo. O segundo fio está dentro desse campo.")
        self.mark("fios_campo_no_segundo")
        self.delcap()
        live=self.wire_pair(self.I1,self.I2,self.d,center=-3.8,forces=False,fields=False)
        group.clear_updaters(recursive=True)
        self.play(FadeOut(group),FadeIn(live),run_time=.8);group=live
        self.show_eq(r"\mathbf F_2=I_2\mathbf L\times\mathbf B_1",y=1.3)
        self.show_eq(r"F_2=I_2LB_1",y=1.3)
        self.show_eq(r"F_2=I_2L\frac{\mu_0I_1}{2\pi d}",y=1.3)
        self.show_eq(r"\frac{|\mathbf F_2|}{L}=\frac{\mu_0|I_1I_2|}{2\pi d}",y=1.3,color=FC)
        units=eq(r"[F/L]=\mathrm{N/m}",size=30).move_to([3.65,-0.1,0]);self.play(FadeIn(units),run_time=0.8)
        self.fala("Para um trecho de comprimento L, a força é corrente vezes o produto vetorial do comprimento orientado com o campo. Nesse caso, corrente e campo são perpendiculares. Portanto chegamos à força por unidade de comprimento.")
        forced=self.wire_pair(self.I1,self.I2,self.d,center=-3.8,forces=True,fields=False)
        group.clear_updaters(recursive=True)
        self.play(FadeOut(group),FadeIn(forced),run_time=1)
        self.caption("Mesmo sentido → atração    ·    L × B1 aponta para o outro fio",FC)
        self.mark("fios_atracao");self.fala("Correntes no mesmo sentido atraem.",minimo=4)
        # Corrente troca em estado discreto; não interpola setas de força sem estado físico.
        self.I2=-1.
        rep=self.wire_pair(self.I1,self.I2,self.d,center=-3.8,forces=True,fields=False)
        forced.clear_updaters(recursive=True)
        self.play(FadeOut(forced),FadeOut(self.cap),run_time=0.4)
        self.cap=None
        self.play(FadeIn(rep),run_time=0.4)
        self.caption("Sentidos opostos → repulsão    ·    I2 inverte; B1 permanece",FC)
        self.mark("fios_repulsao")
        self.fala("Correntes em sentidos opostos repelem. Agora a interação que vimos no vídeo anterior foi reconstruída a partir do campo produzido pela própria corrente.")


    def loop_diagram(self, components=True, many=False, distant=False):
        R=self.loop_radius;z=self.z_obs.get_value();ph=self.phi_src.get_value()
        g=VGroup(ParametricFunction(lambda u:self.W([R*math.cos(u),R*math.sin(u),0]),t_range=[0,2*math.pi],color=BLUE_L,stroke_width=6))
        f,p,dl,sep,b,tr,ax=espira(ph,z,R)
        O=np.zeros(3)
        g.add(Dot(self.W(f),color=CYAN,radius=.075))
        if abs(self.beta.get_value()-90)<.01 and abs(math.cos(ph))<.001:
            # Tangente perpendicular à tela na vista lateral; não é um vetor nulo.
            direction=1 if math.sin(ph)>0 else -1
            tangent=self.out_symbol(self.W(f),direction)
            tangent.set_color(CYAN);g.add(tangent)
        else:
            g.add(self.vec(f,dl,CYAN,scale=.38))
        if self.loop_axis:
            g.add(DashedLine(self.W([0,0,-.3]),self.W([0,0,3.1]),color=VIOLET,stroke_width=2),
                  label('z',self.W([0,0,3.1])+UP*.25,color=VIOLET),
                  Dot(self.W(p)),label('P',self.W(p)+DOWN*.3))
        if self.loop_triangle:
            g.add(Line(self.W(O),self.W(f),color=WHITE,stroke_width=3),
                  Line(self.W(O),self.W(p),color=VIOLET,stroke_width=3),
                  self.vec(f,sep,VIOLET,width=3),
                  label('R',self.W(.5*f)+LEFT*.3),
                  label('z',self.W(.5*p)+DOWN*.35,color=VIOLET),
                  label('s',self.W(f+.5*sep)+UP*.3,color=VIOLET),
                  label('O',self.W(O)+LEFT*.28+DOWN*.25))
            # Ângulo reto formado por raio e eixo; triângulo físico em yz.
            if z>.01 and abs(math.cos(ph))<.001:
                rhat=f/R;zhat=np.array([0,0,1.])
                corner=VMobject(color=WHITE,stroke_width=2).set_points_as_corners([self.W(.2*rhat),self.W(.2*rhat+.2*zhat),self.W(.2*zhat)])
                g.add(corner)
        if self.loop_field:
            scale=4.5
            if not self.loop_decomposed_only:
                g.add(self.vec(p,b,MAG,scale=scale),label(r'd\mathbf B',self.W(p+scale*b)+UP*.3,color=MAG))
            if components and z>1e-5:
                g.add(self.vec(p,ax,MAG,scale=scale,width=4),
                      self.vec(p+scale*ax,tr,VIOLET,scale=scale,width=4))
                if not self.loop_pair:
                    g.add(label(r"dB_z",self.W(p+.5*scale*ax)+DOWN*.32,size=24,color=MAG))
            if many:
                for a in np.linspace(0,2*math.pi,6,endpoint=False):
                    fb,pb,dlb,rb,bb,tb,ab=espira(a,z,R)
                    g.add(Dot(self.W(fb),color=CYAN,radius=.05),self.vec(pb,bb,MAG,scale=3,width=3))
        if self.loop_pair:
            f2,p2,dl2,sep2,b2,tr2,ax2=espira(ph+math.pi,z,R)
            tangent=self.out_symbol(self.W(f2),-1);tangent.set_color(CYAN)
            g.add(tangent,Line(self.W(f2),self.W(p),color=VIOLET,stroke_width=2).set_opacity(.5))
            if not self.loop_decomposed_only:
                g.add(self.vec(p,b2,MAG,scale=4.5))
            if components:
                g.add(self.vec(p+4.5*ax2,tr2,VIOLET,scale=4.5,width=4))
        return g


    def cached_loop_diagram(self):
        key=(self.phi_src.get_value(),self.z_obs.get_value(),self.loop_radius,
             self.loop_components,self.loop_many,self.loop_axis,self.loop_triangle,
             self.loop_field,self.loop_pair,self.loop_decomposed_only,*self.view_key())
        if getattr(self,'_loop_key',None)!=key:
            self._loop_key=key
            self._loop_cached=self.loop_diagram(self.loop_components,self.loop_many)
        return self._loop_cached


    def espira_no_eixo(self):
        self.section('espira','Uma espira, duas vistas da mesma geometria')
        self.clear();self.reset_view(x=-4,y=-.15,scale=1.05,beta=0,tau=0)
        self.loop_radius=1.65;self.phi_src=ValueTracker(math.pi/2);self.z_obs=ValueTracker(1.9)
        self.loop_components=False;self.loop_many=False;self.loop_axis=False
        self.loop_triangle=False;self.loop_field=False;self.loop_pair=False;self.loop_decomposed_only=False
        self.loop_group=self.cached(lambda:(self.phi_src.get_value(),self.z_obs.get_value(),self.loop_radius,self.loop_components,self.loop_many,self.loop_axis,self.loop_triangle,self.loop_field,self.loop_pair,self.loop_decomposed_only,*self.view_key()),lambda:self.loop_diagram(self.loop_components,self.loop_many))
        self.loop_flow=self.flow([lambda u:self.W([self.loop_radius*math.cos(2*math.pi*u),self.loop_radius*math.sin(2*math.pi*u),0])],count=10)
        self.add(self.loop_group,self.loop_flow)
        front=txt('Vista frontal · olhando de +z',23).move_to([-4,2.15,0])
        self.play(FadeIn(front),run_time=.7)
        current=VGroup(arrow(self.W([R:=self.loop_radius,0,0]),self.W([R,.6,0]),CYAN),label('I',self.W([R+.35,.3,0]),color=CYAN))
        self.play(FadeIn(current),run_time=.8);self.hold(3)
        arc=Arc(radius=R*self.gs.get_value(),start_angle=math.pi/2-.35,angle=.35,arc_center=self.W([0,0,0]),color=CYAN,stroke_width=10)
        radius=Line(self.W([0,0,0]),self.W([0,R,0]),color=WHITE,stroke_width=2)
        radiuslab=label('R',self.W([-.3,R/2,0]))
        angle=Arc(radius=.5,start_angle=math.pi/2-.35,angle=.35,arc_center=self.W([0,0,0]),color=WHITE)
        anglelab=label(r'd\phi',self.W([.55,.65,0]))
        self.play(Create(radius),FadeIn(radiuslab),Create(arc),Create(angle),FadeIn(anglelab),run_time=1.4)
        self.show_eq(r'd\ell=R\,d\phi',y=1.3,size=48)
        self.caption('O arco infinitesimal é raio vezes ângulo em radianos')
        self.mark('espira_arco_frontal');self.hold(5)
        self.play(FadeOut(VGroup(front,current,arc,radius,radiuslab,angle,anglelab)),run_time=.8)
        self.delcap()
        self.loop_axis=True
        self.motion('espira_frontal_lateral',4)
        self.play(self.beta.animate.set_value(90),self.ox.animate.set_value(-5.9),self.oy.animate.set_value(-.35),run_time=4)
        side=txt('Vista lateral · espira de perfil',23).move_to([-4.1,2.15,0])
        self.play(FadeIn(side),run_time=.7)
        self.caption('O ponto P está no eixo; a tangente dℓ sai da tela')
        self.hold(4)
        self.loop_triangle=True
        self.hold(.1)
        self.show_eq(r's=|\mathbf R|',y=1.3,size=44,matching=False)
        self.caption('R é o raio da espira; s é a separação da fonte até P')
        self.hold(4)
        self.show_eq(r's^2=R^2+z^2',y=1.3,size=46)
        self.show_eq(r's=\sqrt{R^2+z^2}',y=1.3,size=46)
        self.mark('espira_triangulo');self.hold(4)
        self.show_eq(r'd\boldsymbol\ell\perp\mathbf R\quad\Rightarrow\quad\sin\theta=1',y=1.3,size=36,matching=False)
        self.caption('dℓ é perpendicular ao plano do triângulo, que contém a separação')
        self.mark('espira_ortogonalidade');self.hold(4)
        self.loop_field=True;self.hold(.1)
        self.show_eq(r'dB=\frac{\mu_0 I}{4\pi}\frac{d\ell}{s^2}',y=1.3,size=42,matching=False)
        self.caption('A mão direita fornece dB, perpendicular à separação')
        self.hold(4)
        self.loop_components=True
        self.show_eq(r'dB_z=dB\cos\gamma',y=1.3,size=44,matching=False)
        self.caption('Decompor dB: uma componente axial e uma transversal')
        self.hold(4)
        # Mesmos ângulos por pares de direções perpendiculares.
        gamma=math.atan2(self.z_obs.get_value(),R)
        f,pt,dl,sep,b,tr,ax=espira(math.pi/2,self.z_obs.get_value(),R)
        fs=self.W(f);ps=self.W(pt)
        source_angle=Arc(radius=.5,start_angle=-math.pi/2,angle=gamma,arc_center=fs,color=WHITE)
        field_angle=Arc(radius=.45,start_angle=0,angle=gamma,arc_center=ps,color=WHITE)
        angles=VGroup(source_angle,field_angle,label(r'\gamma',fs+[.35,-.65,0]),label(r'\gamma',ps+[.65,.28,0]))
        self.play(Create(source_angle),Create(field_angle),FadeIn(angles[2]),FadeIn(angles[3]),run_time=1.2)
        self.caption('Ângulos iguais: dB ⟂ separação; eixo ⟂ raio')
        self.hold(5)
        self.show_eq(r'\cos\gamma=\frac{R}{s}',y=1.3,size=46,matching=False)
        self.show_eq(r'dB_z=dB\frac{R}{s}',y=1.3,size=46,matching=False)
        self.mark('espira_projecao_axial');self.hold(4)
        self.play(FadeOut(angles),run_time=.7)
        self.loop_pair=True;self.hold(.1)
        self.caption('Agora selecione o elemento diametralmente oposto')
        self.hold(3)
        self.loop_decomposed_only=True;self.hold(.1)
        # As componentes são copiadas do MESMO par físico e somadas fora de P.
        scale=4.5
        original_t1=self.vec(pt+scale*ax,tr,VIOLET,scale=scale,width=4)
        original_t2=self.vec(pt+scale*ax,-tr,VIOLET,scale=scale,width=4)
        base=np.array([2.,-.95,0]);delta=self.W(pt+scale*tr)-self.W(pt)
        t1=arrow(base,base+delta,VIOLET,width=5)
        t2=arrow(base+delta,base,VIOLET,width=5)
        self.caption('Transversais ponta a ponta: o caminho volta à origem')
        self.show_eq(r'd\mathbf B_\perp(\phi)+d\mathbf B_\perp(\phi+\pi)',y=1.3,size=34,matching=False)
        self.motion("transversais_ponta_a_ponta",2.4)
        self.play(TransformFromCopy(original_t1,t1),run_time=1.2)
        self.play(TransformFromCopy(original_t2,t2),run_time=1.2)
        self.show_eq(r'd\mathbf B_\perp(\phi)+d\mathbf B_\perp(\phi+\pi)=0',y=1.3,size=34,matching=False)
        zero=label(r'\mathbf0',base+RIGHT*.5,color=VIOLET)
        self.play(FadeIn(zero),run_time=.6);self.mark('espira_transversais_fecham');self.hold(4)
        self.play(FadeOut(VGroup(t1,t2,zero)),run_time=.7)
        adelta=self.W(pt+scale*ax)-self.W(pt);abase=np.array([1.5,-.8,0])
        a1=arrow(abase,abase+adelta,MAG,width=5)
        a2=arrow(abase+adelta,abase+2*adelta,MAG,width=5)
        original_a=self.vec(pt,ax,MAG,scale=scale,width=4)
        self.caption('Axiais ponta a ponta: as duas parcelas têm o mesmo sentido')
        self.show_eq(r'dB_z+dB_z',y=1.3,size=44,matching=False)
        self.motion("axiais_ponta_a_ponta",2.2)
        self.play(TransformFromCopy(original_a,a1),run_time=1.1)
        self.play(TransformFromCopy(original_a,a2),run_time=1.1)
        self.show_eq(r'dB_z+dB_z=2dB_z',y=1.3,size=44,matching=False)
        self.caption('Axiais ponta a ponta: a resultante é o dobro de uma parcela')
        result=arrow(abase+DOWN*.4,abase+2*adelta+DOWN*.4,MAG,width=7)
        self.play(Create(result),run_time=.8);self.mark('espira_cancelamento_e_soma');self.hold(5)
        self.play(FadeOut(VGroup(a1,a2,result,side)),run_time=.7)
        self.loop_pair=False;self.loop_decomposed_only=False
        self.section('algebra_espira','Do triângulo ao integrando axial')
        self.show_eq(r'dB_z=\frac{\mu_0 I}{4\pi}\frac{d\ell}{s^2}\frac{R}{s}',y=1.1,size=44,matching=False)
        self.caption('Lei experimental × projeção axial')
        self.hold(4)
        arc_memory=eq(r'd\ell=R\,d\phi',size=34).move_to([3.65,-.45,0])
        self.play(FadeIn(arc_memory),run_time=.8)
        self.show_eq(r'dB_z=\frac{\mu_0 I}{4\pi}\frac{(R\,d\phi)R}{s^2s}',y=1.1,size=44)
        self.caption('Um R vem do arco; o outro, da projeção. A separação aparece três vezes')
        self.hold(5)
        self.show_eq(r'dB_z=\frac{\mu_0 I}{4\pi}\frac{R^2}{s^3}\,d\phi',y=1.1,size=44)
        self.play(FadeOut(arc_memory),run_time=.6)
        self.show_eq(r'dB_z=\frac{\mu_0 I}{4\pi}\frac{R^2}{(R^2+z^2)^{3/2}}\,d\phi',y=1.1,size=42)
        self.mark('espira_origem_integrando');self.hold(4)
        # Volta completa na MESMA espira; inclinação permite reconhecer a trajetória.
        self.loop_triangle=False;self.loop_components=False
        self.play(self.beta.animate.set_value(68),run_time=2)
        self.caption('Percorrer uma volta: I, R, z e s permanecem constantes em φ')
        self.motion("espira_volta_integral",8)
        self.play(self.phi_src.animate.increment_value(2*math.pi),run_time=8,rate_func=linear)
        self.show_eq(r'B_z=\int_0^{2\pi}\frac{\mu_0 I R^2}{4\pi(R^2+z^2)^{3/2}}\,d\phi',y=1.1,size=40)
        self.hold(3)
        self.show_eq(r'B_z=\frac{\mu_0 I R^2}{4\pi(R^2+z^2)^{3/2}}\int_0^{2\pi}d\phi',y=1.1,size=40)
        self.caption('Os fatores constantes saem da integral; resta somar o ângulo da volta')
        self.hold(4)
        self.caption('A integral de dφ em uma volta completa vale 2π')
        self.show_eq(r'\int_0^{2\pi}d\phi=[\phi]_0^{2\pi}=2\pi',y=1.1,size=44,matching=False)
        self.hold(3)
        self.show_eq(r'B_z=\frac{\mu_0 I R^2}{(R^2+z^2)^{3/2}}\frac{2\pi}{4\pi}',y=1.1,size=42,matching=False)
        fraction=eq(r'\frac{2\pi}{4\pi}=\frac{1}{2}',size=38).move_to([3.65,-.55,0])
        self.play(Write(fraction),run_time=1)
        self.caption('A volta inteira fornece 2π; com o 4π da lei, resta 1/2')
        self.hold(4)
        self.play(FadeOut(fraction),run_time=.6)
        self.show_eq(r'B_z(z)=\frac{\mu_0 I R^2}{2(R^2+z^2)^{3/2}}',y=.7,size=46)
        self.mark('resultado_espira_eixo');self.hold(5)

    def checagens_espira(self):
        self.section("centro", "Checagem 1: o centro da espira")
        self.loop_pair=False;self.loop_triangle=False;self.loop_components=False
        self.caption("Mover P até z = 0: cada contribuição se alinha com o eixo")
        self.motion("observador_ate_centro",5)
        self.play(self.z_obs.animate.set_value(0),run_time=5,rate_func=smooth)
        self.caption("Em z = 0, a separação até cada elemento é igual ao raio R")
        self.show_eq(r"B(0)=\frac{\mu_0IR^2}{2R^3}",y=0.7,color=MAG)
        self.show_eq(r"B(0)=\frac{\mu_0I}{2R}",y=0.7,color=MAG)
        self.loop_many=False
        self.loop_components=False;self.loop_pair=False
        self.caption("No centro, cada dB já é axial: não há componente lateral para cancelar")
        self.motion("centro_contribuicoes_axiais",6)
        self.play(self.phi_src.animate.increment_value(2*math.pi),run_time=6,rate_func=linear)
        self.mark("espira_centro_sem_laterais")
        self.fala("No centro, a distância axial vale zero. Aqui existe uma simplificação adicional. Cada contribuição individual já aponta ao longo do eixo. Não existem componentes laterais para cancelar.")
        self.loop_many=False
        self.section("distante", "Checagem 2: muito longe da espira")
        # Primeiro move fisicamente em vista espacial; depois muda para gráfico com escala axial explícita.
        self.show_eq(r"B_z(z)=\frac{\mu_0IR^2}{2(R^2+z^2)^{3/2}}",y=0.7,color=MAG)
        self.caption("O observador se afasta do centro; a expressão geral acompanha a geometria")
        self.play(self.z_obs.animate.set_value(2.4),run_time=4)
        self.loop_group.clear_updaters();self.loop_flow.clear_updaters(recursive=True);self.play(FadeOut(self.loop_group),FadeOut(self.loop_flow),run_time=0.7)
        self.reset_view(x=-5.7,y=0,scale=1,beta=0,tau=0)
        def far_geometry():
            z=self.z_obs.get_value();R=self.loop_radius
            # Eixo graduado em z/R: 0→12. A fonte fica ampliada para leitura.
            x0=-6.7;x1=-0.8;y=-0.3
            px=x0+(x1-x0)*z/(12*R)
            g=VGroup(Line([x0,y,0],[x1,y,0],color=VIOLET,stroke_width=2),
                     Ellipse(width=0.35,height=1.65,color=BLUE_L,stroke_width=5).move_to([x0,y,0]),
                     Dot([px,y,0],radius=0.09),label("P",[px,y+0.4,0]),label("z/R",[-0.8,-1.15,0]))
            for u in [0,3,6,9,12]:
                xx=x0+(x1-x0)*u/12
                g.add(Line([xx,y-0.1,0],[xx,y+0.1,0],color=WHITE,stroke_width=2),label(str(u),[xx,y-0.45,0],size=24))
            return g
        far=self.cached(lambda:self.z_obs.get_value(),far_geometry);self.add(far)
        self.add(self.flow([lambda u:np.array([-6.7+.175*math.cos(2*math.pi*u),-.3+.825*math.sin(2*math.pi*u),0])],count=7))
        self.caption("Esquema axial graduado em z/R; espira ampliada para permanecer legível")
        self.play(self.z_obs.animate.set_value(12*self.loop_radius),run_time=7)
        self.caption("|z| ≫ R: a distância domina o denominador")
        self.fala("Agora leve o ponto muito longe da espira. Nesse limite, o raio se torna pequeno em comparação com a distância axial.")
        self.show_eq(r"(R^2+z^2)^{3/2}=|z|^3(1+R^2/z^2)^{3/2}",y=0.7,size=36)
        self.show_eq(r"R^2/z^2\to0\quad\Rightarrow\quad(R^2+z^2)^{3/2}\sim|z|^3",y=0.7,size=34)
        self.show_eq(r"B_z\sim\frac{\mu_0IR^2}{2|z|^3}",y=0.7,color=MAG)
        self.mark("espira_limite_distante")
        self.fala("O campo distante da espira cai como um sobre o módulo da distância ao cubo. Muito mais rapidamente que o inverso da distância do fio infinito. A geometria da fonte muda a maneira como o campo se espalha pelo espaço.")
        compare=eq(r"\mathrm{fio}:\ B\propto a^{-1}\qquad\mathrm{espira}:\ B\propto|z|^{-3}",size=32,width=12).move_to([0,-1.8,0])
        self.play(FadeIn(compare),run_time=0.9);self.hold(4);self.mark("comparacao_decaimentos")


    def sintese(self):
        self.section('sintese','Uma lei; geometrias diferentes')
        self.clear();self.reset_view(x=-4.5,y=-1,scale=.9,beta=0,tau=0)
        self.theta_local.set_value(math.pi/3)
        line=Line(self.W([-2,0,0]),self.W([2,0,0]),color=BLUE_L,stroke_width=6)
        flow=self.flow([lambda u:self.W([-2+4*u,0,0])],count=6)
        self.play(Create(line),run_time=1);self.add(flow)
        p=self.W(clinica(math.pi/3)[1]);f=self.W([0,0,0])
        self.play(FadeIn(Dot(p)),FadeIn(label('P',p+UP*.3)),Create(arrow(f,p,VIOLET)),run_time=1.2)
        self.show_eq(r'\mathbf R=\mathbf r-\mathbf r\prime',y=1.3,size=42)
        self.caption('A fonte e o observador constroem a separação');self.hold(3)
        self.play(FadeIn(self.out_symbol(p+RIGHT*.3)),run_time=.8)
        self.show_eq(r'd\mathbf B=\frac{\mu_0 I}{4\pi}\frac{d\boldsymbol\ell\times\mathbf R}{R^3}',y=1.3,size=40,matching=False)
        self.caption('Cada elemento contribui com direção e intensidade próprias');self.hold(4)
        self.show_eq(r'\mathbf B=\int d\mathbf B',y=1.3,size=46,matching=False)
        self.caption('Somar as contribuições recupera o campo da fonte');self.hold(3)
        self.clear()
        self.reset_view(x=-4.2,y=-.9,scale=.9)
        wire=Line(self.W([-2.4,0,0]),self.W([2.4,0,0]),color=BLUE_L,stroke_width=6)
        flow=self.flow([lambda u:self.W([-2.4+4.8*u,0,0])])
        self.play(Create(wire),run_time=1);self.add(flow)
        self.show_eq(r'B_\infty=\frac{\mu_0 I}{2\pi a}',y=1.1,size=46,matching=False)
        self.hold(3)
        self.remove(flow)
        loop=Circle(radius=1.5,color=BLUE_L,stroke_width=6).move_to([-4.2,-.3,0])
        self.play(ReplacementTransform(wire,loop),run_time=2)
        self.add(self.flow([lambda u:np.array([-4.2+1.5*math.cos(2*math.pi*u),-.3+1.5*math.sin(2*math.pi*u),0])],count=9))
        self.show_eq(r'B_z=\frac{\mu_0 I R^2}{2(R^2+z^2)^{3/2}}',y=1.1,size=44,matching=False)
        self.caption('A mesma lei; outra geometria, outro campo')
        self.mark('sintese_geometria');self.hold(5)

    def fechamento(self):
        self.section("fechamento", "Que estrutura o campo magnético possui?")
        self.clear()
        rings=VGroup()
        for r in [0.85,1.45,2.05]:
            rings.add(Circle(radius=r,color=MAG,stroke_width=2.5).move_to([-3.3,0,0]))
            rings.add(arrow([-3.3+r,-0.12,0],[-3.3+r,0.25,0],MAG,width=3,tip=0.16))
        source=VGroup(Circle(radius=0.18,color=CYAN).move_to([-3.3,0,0]),Dot([-3.3,0,0],color=CYAN,radius=0.06))
        local=Circle(radius=0.3,color=WHITE,stroke_width=2).move_to([-1.85,0,0])
        for ring in rings:
            self.play(Create(ring),run_time=.25)
        self.play(FadeIn(source),FadeIn(local),run_time=.8)
        probes=VGroup(txt("O que revela o divergente?",28),txt("E o rotacional? E Ampère?",28)).arrange(DOWN,buff=1).move_to([3.2,0.2,0])
        self.play(FadeIn(probes),run_time=1)
        self.fala("Biot Savart nos deu o campo magnético a partir da distribuição de corrente que o produz. Mas agora podemos fazer outra pergunta. Que propriedades esse campo necessariamente possui? O que seu divergente revela? E o que seu rotacional nos diz sobre as correntes que o geram?")
        self.mark("gancho_estrutura_local")
        self.fala("Como o divergente, o rotacional e a Lei de Ampère descrevem esse campo? Essa é a pergunta para a sequência do curso.")
        self.clear()
        end=txt("PARALLAX LAB",32).move_to([0,0.7,0])
        below=txt("LEI DE BIOT–SAVART",24,opacity=0.8).move_to([0,-0.3,0])
        self.play(FadeIn(end),FadeIn(below),run_time=1.2);self.hold(4);self.mark("fim")

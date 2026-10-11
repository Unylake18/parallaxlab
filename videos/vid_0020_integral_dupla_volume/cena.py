"""V6 silenciosa · EP. 07. Construção contínua, refinamento breve e conta completa."""
import json
import sys
from pathlib import Path

import numpy as np
from manim import *
from MF_Tools import TransformByGlyphMap

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from template.config import BACKGROUND_COLOR, PRIMARY_COLOR, TEXT_COLOR, WATERMARK_PATH
from template.fonts import screen_text

BASE_COLOR = PRIMARY_COLOR
HEIGHT_COLOR = "#EA63FF"
VOLUME_COLOR = "#9C8CFF"
INNER_COLOR = "#8CEBFF"
OUTER_COLOR = "#C4B5FF"
LEVELS = (4, 8, 16, 32, 64)
SELECTED = (2, 0)


def f(x, y):
    return 4 - x * x - y * y


def project_xyz(x, y, z):
    """Projeção fixa: x/y independentes, z vertical; vista de x<0, y<0."""
    return np.array([1.55 * (x - y), 0.62 * (x + y) + 1.05 * z - 1.2, 0.0])


def partition(n):
    d = 2 / n
    return [dict(i=i, j=j, x0=-1+i*d, y0=-1+j*d, d=d,
                 xi=-1+(i+0.5)*d, yj=-1+(j+0.5)*d,
                 h=f(-1+(i+0.5)*d, -1+(j+0.5)*d))
            for j in range(n) for i in range(n)]


def cell_polygon(cell, project=project_xyz, z=0, **kwargs):
    x, y, d = cell['x0'], cell['y0'], cell['d']
    return Polygon(*[project(a, b, z) for a, b in
                     ((x, y), (x+d, y), (x+d, y+d), (x, y+d))], **kwargs)


def make_base_grid(n, project=project_xyz):
    region = dict(x0=-1, y0=-1, d=2)
    border = cell_polygon(region, project, color=BASE_COLOR, stroke_width=2,
                          fill_color=BASE_COLOR, fill_opacity=0.035)
    lines = VGroup()
    for t in np.linspace(-1,1,n+1)[1:-1]:
        lines.add(Line(project(t,-1,0),project(t,1,0),color=BASE_COLOR,stroke_width=1),
                  Line(project(-1,t,0),project(1,t,0),color=BASE_COLOR,stroke_width=1))
    return VGroup(border, lines).set_z_index(2)


def make_column(cell, project=project_xyz, selected=False, height=None):
    x, y, d = cell['x0'], cell['y0'], cell['d']
    h = cell['h'] if height is None else height
    colors = ("#51418C", "#6B57AD", VOLUME_COLOR) if selected else ("#253770", "#3F3B83", "#6874BC")
    faces = (
        [(x,y,0), (x,y+d,0), (x,y+d,h), (x,y,h)],
        [(x,y,0), (x+d,y,0), (x+d,y,h), (x,y,h)],
        [(x,y,h), (x+d,y,h), (x+d,y+d,h), (x,y+d,h)],
    )
    return VGroup(*[Polygon(*[project(*p) for p in face],
                           fill_color=color, fill_opacity=1,
                           stroke_color="#AEBAED" if not selected else VOLUME_COLOR,
                           stroke_width=(0.18 if d <= 1/16 else 0.35 if d <= 1/8 else 0.55)
                           if not selected else 1.6)
                    for face, color in zip(faces, colors)])


def make_column_field(n):
    # Oclusão: células distantes (x+y maior) primeiro; faces x0/y0 visíveis.
    cells = sorted(partition(n), key=lambda c: (-(c['xi']+c['yj']), c['xi']))
    return VGroup(*[make_column(c) for c in cells]).set_z_index(10)


def make_dense_column_field(n=64):
    """Topos exatos e faces expostas agrupados em três caminhos compostos.

    Cada topo pertence a uma célula literal e tem z=f no seu ponto médio.
    Incluir o degrau quando uma célula é mais alta que a vizinha à frente
    fecha a superfície de escada sem frestas. Faces internas ocultas são
    omitidas. Três caminhos substituem milhares de prismas/animadores.
    """
    cells = sorted(partition(n), key=lambda c: (-(c['xi']+c['yj']), c['xi']))
    sides = [VMobject(fill_color=color, fill_opacity=1, stroke_width=0)
             for color in ("#253770", "#3F3B83")]
    tops = VMobject(fill_color="#6874BC", fill_opacity=1,
                    stroke_color="#AEBAED", stroke_width=0.08, stroke_opacity=0.45)
    for c in cells:
        x,y,d,h = c['x0'],c['y0'],c['d'],c['h']
        tops.append_points(cell_polygon(c,z=h).points)
        low_x = 0 if c['i']==0 else f(c['xi']-d,c['yj'])
        low_y = 0 if c['j']==0 else f(c['xi'],c['yj']-d)
        if h > low_x:
            sides[0].append_points(Polygon(*[project_xyz(*p) for p in
                ((x,y,low_x),(x,y+d,low_x),(x,y+d,h),(x,y,h))]).points)
        if h > low_y:
            sides[1].append_points(Polygon(*[project_xyz(*p) for p in
                ((x,y,low_y),(x+d,y,low_y),(x+d,y,h),(x,y,h))]).points)
    assert len(tops.get_subpaths()) == n*n
    return VGroup(*sides,tops).set_z_index(10)


def make_surface_wireframe():
    curves = VGroup()
    samples = np.linspace(-1, 1, 65)
    for fixed in np.linspace(-1, 1, 13):
        for swap in (False, True):
            pts = [project_xyz(t, fixed, f(t, fixed)) if not swap
                   else project_xyz(fixed, t, f(fixed, t)) for t in samples]
            curve = VMobject(stroke_color=BASE_COLOR, stroke_width=1.15, stroke_opacity=0.7)
            curve.set_points_as_corners(pts)
            curves.add(curve)
    return curves.set_z_index(30)


def make_axes():
    origin = project_xyz(0,0,0)
    starts = [project_xyz(-1.35,0,0),project_xyz(0,-1.35,0),origin]
    ends = [project_xyz(1.45,0,0),project_xyz(0,1.45,0),project_xyz(0,0,4.4)]
    axes = VGroup(*[Arrow(start,end,buff=0,color=TEXT_COLOR,stroke_width=1.2,
                         max_tip_length_to_length_ratio=0.035).set_opacity(0.55)
                    for start,end in zip(starts,ends)])
    labels = VGroup(*[MathTex(s,font_size=27,color=TEXT_COLOR).next_to(p,d,buff=0.1)
                       for s,p,d in zip(('x','y','z'),ends,(RIGHT,LEFT,UP))])
    labels[2].shift(RIGHT*0.25)
    origin_label = MathTex('0',font_size=19,color=TEXT_COLOR).move_to(origin+LEFT*0.18+DOWN*0.18)
    return VGroup(axes,labels,origin_label).set_z_index(35)


def make_volume_shell():
    """Faces curvas de fronteira indicam o volume sob a malha, sem novo sólido."""
    panels = VGroup()
    for swap in (False,True):
        pts = [project_xyz(-1,-1,0)]
        pts += [project_xyz(1,-1,0) if not swap else project_xyz(-1,1,0)]
        pts += [project_xyz(t,-1,f(t,-1)) if not swap else project_xyz(-1,t,f(-1,t))
                for t in np.linspace(1,-1,65)]
        panels.add(Polygon(*pts,fill_color=VOLUME_COLOR,fill_opacity=0.12,
                           stroke_color=VOLUME_COLOR,stroke_opacity=0.2,stroke_width=1))
    return panels.set_z_index(3)


def make_refinement_start(n):
    """Nova partição 2n×2n, ainda com a altura da célula-mãe em cada filha.

    A união dos prismas é idêntica ao estado anterior. A animação seguinte
    move somente os topos para f nos novos pontos médios.
    """
    parents = {(c['i'],c['j']): c for c in partition(n)}
    children = sorted(partition(2*n),key=lambda c:(-(c['xi']+c['yj']),c['xi']))
    return VGroup(*[make_column(c,height=parents[c['i']//2,c['j']//2]['h'])
                    for c in children]).set_z_index(10)


def new_partition_lines(n):
    lines = VGroup()
    for k in range(1,2*n,2):
        t = -1+k/n
        lines.add(Line(project_xyz(t,-1,0),project_xyz(t,1,0),color=BASE_COLOR,stroke_width=0.85),
                  Line(project_xyz(-1,t,0),project_xyz(1,t,0),color=BASE_COLOR,stroke_width=0.85))
    return lines.set_z_index(2)


def split_top_lines(n):
    lines = VGroup()
    for c in partition(n):
        x,y,d,h = c['x0'],c['y0'],c['d'],c['h']
        lines.add(Line(project_xyz(x+d/2,y,h),project_xyz(x+d/2,y+d,h),
                       color=BASE_COLOR,stroke_width=1.1),
                  Line(project_xyz(x,y+d/2,h),project_xyz(x+d,y+d/2,h),
                       color=BASE_COLOR,stroke_width=1.1))
    return lines.set_z_index(20)


def make_section(x):
    """Seção verdadeira x=constante; área entre z=0 e f(x,y)."""
    ys = np.linspace(-1,1,65)
    plane = Polygon(project_xyz(x,-1,0),project_xyz(x,1,0),
                    project_xyz(x,1,4.3),project_xyz(x,-1,4.3),
                    fill_color=TEXT_COLOR,fill_opacity=0.045,
                    stroke_color=TEXT_COLOR,stroke_width=1,stroke_opacity=0.4)
    area = Polygon(project_xyz(x,-1,0),project_xyz(x,1,0),
                   *[project_xyz(x,y,f(x,y)) for y in ys[::-1]],
                   fill_color=INNER_COLOR,fill_opacity=0.36,
                   stroke_color=INNER_COLOR,stroke_width=1.2)
    curve = VMobject(stroke_color=INNER_COLOR,stroke_width=3)
    curve.set_points_as_corners([project_xyz(x,y,f(x,y)) for y in ys])
    foot = Line(project_xyz(x,-1,0),project_xyz(x,1,0),color=BASE_COLOR,stroke_width=3)
    return VGroup(plane,area,curve,foot).set_z_index(40)


def partial_section_area(x, end_y):
    ys = np.linspace(-1,max(-0.9999,end_y),65)
    return Polygon(project_xyz(x,-1,0),project_xyz(x,ys[-1],0),
                   *[project_xyz(x,y,f(x,y)) for y in ys[::-1]],
                   fill_color=INNER_COLOR,fill_opacity=0.36,
                   stroke_color=INNER_COLOR,stroke_width=1.2).set_z_index(40)


def maximum_height_error(n):
    errors = []
    for c in partition(n):
        x, y, d, h = c['x0'], c['y0'], c['d'], c['h']
        highest = f(np.clip(0, x, x+d), np.clip(0, y, y+d))
        lowest = min(f(a,b) for a in (x,x+d) for b in (y,y+d))
        errors.append(max(highest-h, h-lowest))
    return float(max(errors))


def validate_geometry():
    """Checks locais, incluindo convergência e o resultado por dois caminhos."""
    assert f(0,0) == 4
    assert all(f(x,y) == 2 for x in (-1,1) for y in (-1,1))
    previous_error, previous_peak = float('inf'), 0
    report = []
    for n in LEVELS:
        cells, d = partition(n), 2/n
        assert len(cells) == n*n
        assert len({(c['i'],c['j']) for c in cells}) == n*n
        assert abs(sum(c['d']**2 for c in cells)-4) < 1e-12
        assert min(c['x0'] for c in cells) == min(c['y0'] for c in cells) == -1
        assert max(c['x0']+d for c in cells) == max(c['y0']+d for c in cells) == 1
        assert all(c['h'] == f(c['xi'],c['yj']) > 0 for c in cells)
        peak, error = max(c['h'] for c in cells), maximum_height_error(n)
        assert previous_peak < peak < 4 and error < previous_error
        previous_peak, previous_error = peak, error
        total = sum(c['h']*d*d for c in cells)
        assert abs(total - (40/3+8/(3*n*n))) < 1e-11
        report.append(dict(n=n, columns=len(cells), delta_area=d*d,
                           max_height_error=error, sum_volume=total))
    from fractions import Fraction as F
    assert 2*F(22,3)-F(4,3) == 16-F(4,3)-F(4,3) == F(40,3)
    ys = np.linspace(-1,1,2001)
    for x in (-1,-0.75,0,0.5,1):
        assert abs(np.trapezoid(f(x,ys),ys)-(22/3-2*x*x)) < 1e-6
    return report



class IntegralDuplaVolume020(Scene):
    def cue(self, text, run_time=0.55):
        """Microtexto transitório, sempre na mesma faixa acima da geometria."""
        target = screen_text(text,26,oversample=2).move_to(UP*5.5).set_z_index(110)
        if target.width > 7.7:
            target.scale_to_fit_width(7.7)
        if getattr(self,'current_cue',None) is None:
            self.play(FadeIn(target),run_time=run_time)
        else:
            self.play(FadeOut(self.current_cue),FadeIn(target),run_time=run_time)
        self.current_cue = target

    def clear_cue(self):
        if self.current_cue is not None:
            self.play(FadeOut(self.current_cue),run_time=0.4)
            self.current_cue = None

    def glyph_formula(self, runs, size=42, y=-4.45):
        """MathTex de string única; faixas explícitas após LaTeX estabilizado.

        Cada run é (nome, LaTeX autocontido, cor). Os nomes identificam fatores
        matemáticos, não glifos escolhidos pelo matching automático.
        """
        mob = self.formula(' '.join(tex for name,tex,color in runs),size=size,y=y)
        offset = 0
        mob.glyph_runs = {}
        for name,tex,color in runs:
            count = 0 if tex==r'\quad' else len(MathTex(tex)[0])
            indices = list(range(offset,offset+count))
            mob.glyph_runs[name] = indices
            VGroup(*[mob[0][k] for k in indices]).set_color(color)
            offset += count
        assert offset == len(mob[0]), (offset,len(mob[0]),mob.tex_string)
        return mob

    def glyph_transfer(self, source, target, links, run_time=2.2, from_copy=False, extras=()):
        """MF-Tools transporta fatores conhecidos; o restante entra/sai por fade."""
        entries = [(source.glyph_runs[a] if isinstance(a,str) else a,
                    target.glyph_runs[b] if isinstance(b,str) else b) for a,b in links]
        animation = TransformByGlyphMap(source,target,*entries,auto_fade=True,
                                        from_copy=from_copy,printing=False)
        assert not animation.show_indices
        self.play(animation,*extras,run_time=run_time)
        # Cairo 0.21 pode conservar filhos escritos separadamente na Scene.
        if not from_copy:
            self.remove(*source.get_family())
        self.remove(*target.get_family())
        self.add(target)

    def glyph_group(self, mob, *names):
        return VGroup(*[mob[0][k] for name in names for k in mob.glyph_runs[name]])

    def assemble_formula(self, target, transfers, removes=(), run_time=2):
        """Montagem por cópias de fatores já visíveis; sem dupla animação de glifos."""
        names = [name for source,name in transfers]
        entering = [name for name in target.glyph_runs if name not in names]
        self.play(*[TransformFromCopy(source,self.glyph_group(target,name))
                    for source,name in transfers],
                  *([FadeIn(self.glyph_group(target,*entering))] if entering else []),
                  *[FadeOut(mob) for mob in removes],run_time=run_time)
        for mob in removes:
            self.remove(*mob.get_family())
        self.remove(*target.get_family())
        self.add(target)

    def active_variable(self, mob, variable, color):
        """Colorir só a letra ativa, inclusive dentro de uma fração de string única."""
        def shape(glyph):
            pts = glyph.get_all_points()[:,:2]
            return (pts-pts.min(axis=0))/np.maximum(np.ptp(pts,axis=0),1e-12)
        reference = shape(MathTex(variable)[0][0])
        for glyph in mob[0]:
            candidate = shape(glyph)
            if candidate.shape==reference.shape and np.allclose(candidate,reference,atol=1e-4):
                glyph.set_color(color)
        return mob

    def mark(self, name):
        self.events.append(dict(estado=name,segundos=round(self.time,3)))
        print(f"ESTADO {name}: {self.time:.2f}s")

    def hold(self, duration=0.7):
        assert duration <= 1.2
        self.wait(duration)

    def formula(self, *parts, size=42, y=-4.45):
        mob = MathTex(*parts,font_size=size)
        if mob.width > 7.7:
            mob.scale_to_fit_width(7.7)
        return mob.move_to(UP*y).set_z_index(100)

    def substitute(self, source, target, mapping, run_time=2.2, extras=()):
        """Matching literal + substituições explícitas de fatores completos.

        Evita o FadeTransformPieces interno de key_map no Manim 0.21, que
        falha quando uma substituição muda a estrutura/número de glifos.
        Usa somente TransformMatchingTex e ReplacementTransform públicos.
        """
        if not mapping:
            self.play(TransformMatchingTex(source,target),*extras,run_time=run_time)
            return
        remaining_source,remaining_target = source.copy(),target.copy()
        pairs = []
        for old,new in mapping.items():
            source_parts = [p for p in remaining_source if p.tex_string==old]
            target_parts = [p for p in remaining_target if p.tex_string==new]
            assert source_parts and target_parts, (old,new)
            remaining_source.remove(*source_parts)
            remaining_target.remove(*target_parts)
            pairs.append((VGroup(*source_parts),VGroup(*target_parts)))
        # MathTex escrito por partes pode ter filhos independentes na Scene.
        # remove(parent) não extrai a família no Cairo do Manim 0.21.
        self.remove(*source.get_family())
        assert not set(source.get_family()).intersection(self.get_mobject_family_members())
        self.add(remaining_source,*[a for a,b in pairs])
        self.play(TransformMatchingTex(remaining_source,remaining_target),
                  *[ReplacementTransform(a,b) for a,b in pairs],*extras,run_time=run_time)
        self.remove(*remaining_target.get_family(),*[p for a,b in pairs for p in b.get_family()])
        self.add(target)

    def construct(self):
        print(json.dumps(validate_geometry(),indent=2))
        self.events = []
        self.current_cue = None
        group = self.glyph_group
        self.camera.background_color = BACKGROUND_COLOR
        # Mesmas escala, opacidade e margens do cabeçalho de vid_0011.
        wm = ImageMobject(str(WATERMARK_PATH)).set_width(1.8).set_opacity(0.35)
        wm.to_corner(UP+RIGHT,buff=0.28).set_z_index(200)
        # Oversample 2 evita a quebra automática de uma linha longa no Pango.
        series = screen_text("POR TRÁS DA FÓRMULA · EP. 07",20,oversample=2)
        series.set_opacity(0.65).to_corner(UP+LEFT,buff=0.4).set_z_index(200)
        self.add(wm,series)
        axes = make_axes()
        base = make_base_grid(1)
        surface = make_surface_wireframe()
        shell = make_volume_shell()
        chosen = next(c for c in partition(4) if (c['i'],c['j'])==SELECTED)

        # Geometria e fórmula já dividem o primeiro frame do episódio.
        self.mark('abertura_eixos')
        question = VGroup(screen_text("O QUE ESSA FÓRMULA",30,oversample=2),
                          screen_text("ESTÁ SOMANDO?",32,oversample=2)).arrange(DOWN,buff=0.12)
        question.move_to(UP*5.7).set_z_index(100)
        rim = base[0].copy().set_fill(opacity=0).set_z_index(45)
        hook = self.formula(r"\iint_R",r"f(x,y)",r"dA",size=47)
        hook[0].set_color(VOLUME_COLOR)
        hook[0][-1].set_color(BASE_COLOR)
        hook[1].set_color(HEIGHT_COLOR)
        hook[2].set_color(BASE_COLOR)
        self.add(question,axes,base,rim,surface,shell,hook)
        self.play(ShowPassingFlash(surface.copy().set_stroke(width=2.2,opacity=1),time_width=0.3),
                  Indicate(hook[0],color=VOLUME_COLOR,scale_factor=1.04),run_time=2.4)
        self.mark('superficie')
        self.hold(0.9)
        function_label = self.formula(r"z=f(x,y)=4-x^2-y^2",size=34,y=4.55).set_color(BASE_COLOR)
        surface_arrow = Arrow(function_label.get_bottom(),project_xyz(-0.5,0.25,f(-0.5,0.25)),
                              color=BASE_COLOR,buff=0.16,stroke_width=1.7).set_z_index(100)
        self.play(FadeOut(question),Write(function_label),GrowArrow(surface_arrow),run_time=1.5)
        self.play(FadeOut(shell),FadeOut(hook),run_time=0.8)

        # A célula mantém sua posição no domínio durante toda a extrusão.
        self.mark('regiao_particao')
        region = self.formula(r"R=[-1,1]\times[-1,1]",size=34,y=-3.25).set_color(BASE_COLOR)
        grid4 = make_base_grid(4)
        self.play(Write(region),LaggedStart(*[Create(l) for l in grid4[1]],lag_ratio=0.12),run_time=1.8)
        base.add(grid4[1])
        self.cue("Fixe uma célula.")
        selected_base = cell_polygon(chosen,color=BASE_COLOR,stroke_width=3,
                                     fill_color=BASE_COLOR,fill_opacity=0.45).set_z_index(55)
        self.play(DrawBorderThenFill(selected_base),run_time=1)
        self.mark('celula_selecionada')
        self.cue("A base vale ΔA.")
        # Cópia de leitura, sem mover nem substituir a célula geométrica original.
        inset = Rectangle(width=1.25,height=1.25,color=BASE_COLOR,stroke_width=2,
                          fill_color=BASE_COLOR,fill_opacity=0.16).move_to([-2.5,-4.65,0]).set_z_index(100)
        connector = DashedLine(selected_base.get_bottom(),inset.get_top(),color=BASE_COLOR,
                               stroke_width=1,stroke_opacity=0.5).set_z_index(50)
        self.play(TransformFromCopy(selected_base,inset),Create(connector),FadeOut(region),run_time=1.3)
        domain_tag = MathTex(r"R=[-1,1]^2",font_size=27,color=BASE_COLOR).move_to([-2.35,-3.2,0]).set_z_index(100)
        self.play(FadeIn(domain_tag),run_time=0.7)
        bx,by = Brace(inset,DOWN,color=BASE_COLOR),Brace(inset,LEFT,color=BASE_COLOR)
        dx = MathTex(r"\Delta x",font_size=28,color=BASE_COLOR).next_to(bx,DOWN,buff=0.08).set_z_index(100)
        dy = MathTex(r"\Delta y",font_size=28,color=BASE_COLOR).next_to(by,LEFT,buff=0.08).set_z_index(100)
        area_label = MathTex(r"\Delta A",font_size=31,color=BASE_COLOR).move_to(inset).set_z_index(100)
        self.play(Create(bx),Create(by),Write(dx),Write(dy),run_time=1.3)
        area_eq = self.formula(r"\Delta A",r"=",r"\Delta x",r"\Delta y",size=38,y=-4.45)
        area_eq.move_to([1.05,-4.45,0]).set_color(BASE_COLOR)
        self.play(TransformFromCopy(dx,area_eq[2]),TransformFromCopy(dy,area_eq[3]),run_time=1.6)
        self.play(TransformFromCopy(inset,area_label),TransformFromCopy(area_label,area_eq[0]),
                  Write(area_eq[1]),run_time=1.5)
        self.mark('delta_A')
        self.hold(0.7)
        base_label = MathTex(r"\Delta A",font_size=31,color=BASE_COLOR).move_to([3.25,-2.75,0]).set_z_index(100)
        base_arrow = Arrow(base_label.get_top(),selected_base.get_bottom(),buff=0.12,
                           color=BASE_COLOR,stroke_width=1.8).set_z_index(65)
        self.play(TransformFromCopy(area_eq[0],base_label),GrowArrow(base_arrow),
                  FadeOut(VGroup(inset,connector,bx,by,dx,dy,area_label,area_eq)),run_time=1.4)

        self.mark('vertical_determina_altura')
        self.cue("A altura vem da função f.")
        bottom = project_xyz(chosen['xi'],chosen['yj'],0)
        top = project_xyz(chosen['xi'],chosen['yj'],chosen['h'])
        sample = Dot(bottom,color=BASE_COLOR,radius=0.055).set_z_index(70)
        sample_text = MathTex(r"(x_i,y_j)",font_size=28,color=BASE_COLOR).move_to([3.1,-0.9,0]).set_z_index(100)
        sample_arrow = Arrow(sample_text.get_left(),bottom,color=BASE_COLOR,buff=0.14,stroke_width=1.6).set_z_index(65)
        self.play(FadeIn(sample),Write(sample_text),GrowArrow(sample_arrow),run_time=1.3)
        vertical = Line(bottom,top,color=HEIGHT_COLOR,stroke_width=2.6).set_z_index(65)
        intersection = Dot(bottom,color=HEIGHT_COLOR,radius=0.065).set_z_index(70)
        self.add(intersection)
        self.play(Create(vertical),intersection.animate.move_to(top),run_time=2.4)
        self.play(Indicate(intersection,color=HEIGHT_COLOR,scale_factor=1.8),
                  Indicate(surface,color=BASE_COLOR,scale_factor=1),run_time=1.1)
        h_label = MathTex(r"f(x_i,y_j)",font_size=30,color=HEIGHT_COLOR).move_to([3.2,0.45,0]).set_z_index(100)
        guide = DoubleArrow(bottom+RIGHT*0.95,top+RIGHT*0.95,buff=0,color=HEIGHT_COLOR,
                            stroke_width=2,max_tip_length_to_length_ratio=0.045).set_z_index(65)
        connector_h = DashedLine(top,top+RIGHT*0.95,color=HEIGHT_COLOR,stroke_width=1.4).set_z_index(65)
        self.play(GrowArrow(guide),Create(connector_h),TransformFromCopy(intersection,h_label),
                  FadeOut(sample_text),FadeOut(sample_arrow),run_time=1.5)

        # Os três polígonos começam achatados na própria célula, com altura zero.
        self.mark('extrusao_celula')
        column = make_column(chosen,selected=True,height=0).set_z_index(10)
        self.add(column)
        self.play(Transform(column,make_column(chosen,selected=True).set_z_index(10)),run_time=2.8)
        self.mark('coluna_crescida')
        volume = self.formula(r"\Delta V",r"\approx",r"f(x_i,y_j)",r"\Delta A",size=47)
        volume[0].set_color(VOLUME_COLOR)
        volume[2].set_color(HEIGHT_COLOR)
        volume[3].set_color(BASE_COLOR)
        self.play(TransformFromCopy(column,volume[0]),Write(volume[1]),run_time=1.4)
        self.play(TransformFromCopy(h_label,volume[2]),TransformFromCopy(base_label,volume[3]),run_time=1.8)
        self.mark('formula_nasce_da_geometria')
        self.play(Indicate(selected_base,color=BASE_COLOR),Indicate(volume[3],color=BASE_COLOR),run_time=1.1)
        self.play(Indicate(guide,color=HEIGHT_COLOR),Indicate(volume[2],color=HEIGHT_COLOR),run_time=1.1)
        self.hold()

        # A mesma regra repete-se em ondas de trás para frente.
        self.mark('geracao_16_colunas')
        self.cue("Repita em cada célula.")
        cells4 = sorted(partition(4),key=lambda c:(-(c['xi']+c['yj']),c['xi']))
        starts,targets = [],[]
        for c in cells4:
            selected = (c['i'],c['j'])==SELECTED
            starts.append(column if selected else make_column(c,height=0).set_z_index(10))
            targets.append(make_column(c,selected=selected).set_z_index(10))
        field = VGroup(*starts).set_z_index(10)
        self.remove(column)
        self.add(field)
        self.play(FadeOut(VGroup(selected_base,sample,vertical,intersection,guide,connector_h,h_label,
                                 base_label,base_arrow,function_label,surface_arrow)),run_time=0.8)
        self.play(LaggedStart(*[Transform(s,t) for c,s,t in zip(cells4,starts,targets)
                                if (c['i'],c['j'])!=SELECTED],lag_ratio=0.13),run_time=5)
        sum_eq = self.glyph_formula([
            ('op',r'\sum_{i,j}',VOLUME_COLOR),('fun',r'f(x_i,y_j)',HEIGHT_COLOR),
            ('area',r'\Delta A',BASE_COLOR)],size=46)
        self.play(FadeOut(volume),FadeIn(sum_eq),run_time=1.2)
        self.play(Transform(field,make_column_field(4)),run_time=1.5)
        count = screen_text("4 × 4",24,oversample=2).move_to([3,-3.15,0]).set_z_index(100)
        exact_note = MathTex(r"z=4-x^2-y^2",font_size=31,color=BASE_COLOR).move_to([0,4.35,0]).set_z_index(100)
        exact_arrow = Arrow(exact_note.get_bottom(),project_xyz(-0.25,0.25,f(-0.25,0.25)),buff=0.15,
                            color=BASE_COLOR,stroke_width=1.5).set_z_index(100)
        self.play(FadeIn(count),Write(exact_note),GrowArrow(exact_arrow),run_time=1.5)
        self.cue("Refine a partição.")
        limit_runs = lambda n: [
            ('n',rf'n={n}',TEXT_COLOR),('sep',r'\quad',TEXT_COLOR),
            ('area',rf'\Delta A=\frac{{4}}{{{n*n}}}',BASE_COLOR)]
        limit_readout = self.glyph_formula(limit_runs(4),size=29,y=-5.8)
        shrinking_steps = VGroup(
            self.formula(r'n\uparrow\qquad\Delta x,\Delta y\downarrow',size=27,y=-6.65),
            self.formula(r'\Delta x=\Delta y=\frac2n\quad\Delta A=\frac4{n^2}\downarrow',size=27,y=-7.3))
        shrinking_steps.set_color(BASE_COLOR)
        self.play(Write(limit_readout),Write(shrinking_steps),run_time=0.8)

        # A superfície e os eixos não mudam. Filhas herdam inicialmente a altura
        # da mãe e então se ajustam às próprias amostras: não é troca de slides.
        for n,split_time,adjust_time in ((4,0.6,1.2),(8,0.5,1.1),(16,0.4,1)):
            self.mark(f'subdivisao_{n}_para_{2*n}')
            extra_lines = new_partition_lines(n)
            top_lines = split_top_lines(n)
            if n==16:
                top_lines.set_stroke(width=0.55,opacity=0.5)
            self.play(Create(extra_lines),Create(top_lines),run_time=split_time)
            base.add(extra_lines)
            subdivided = make_refinement_start(n)
            self.remove(field,top_lines)
            self.add(subdivided)
            field = subdivided
            next_count = screen_text(f"{2*n} × {2*n}",24,oversample=2).move_to(count).set_z_index(100)
            # A contagem muda no mesmo frame da subdivisão literal. Não há
            # valores numéricos intermediários disputando a leitura da malha.
            self.remove(count,limit_readout)
            self.add(next_count)
            self.play(Transform(field,make_column_field(2*n)),run_time=adjust_time)
            count = next_count
            self.mark(f'malha_{2*n}')
        self.mark('subdivisao_32_para_64')
        dense_field = make_dense_column_field(64)
        next_count = screen_text("64 × 64",24,oversample=2).move_to(count).set_z_index(100)
        dense_grid = new_partition_lines(32).set_stroke(width=0.35,opacity=0.4)
        next_readout = self.glyph_formula([
            ('n',r'n=64',TEXT_COLOR),('sep',r'\quad',TEXT_COLOR),
            ('area',r'\Delta A=\frac{4}{4096}=\frac{1}{1024}',BASE_COLOR)],size=29,y=-5.8)
        # Retirar 32 antes da entrada conjunta evita qualquer frame com a
        # geometria 64×64 e uma legenda n=32 ainda visível.
        self.play(FadeOut(field),run_time=0.25)
        self.remove(count)
        self.play(FadeIn(dense_field),FadeIn(next_count),FadeIn(next_readout),
                  FadeIn(dense_grid),run_time=0.55)
        base.add(dense_grid)
        field,count = dense_field,next_count
        limit_readout = next_readout
        self.mark('malha_64')
        self.hold(0.7)
        area_limit = self.formula(r'n\to\infty\quad\Delta A=\Delta x\Delta y\to0',size=31,y=-5.8).set_color(BASE_COLOR)
        integral = self.glyph_formula([
            ('op',r'\iint_R',VOLUME_COLOR),('fun',r'f(x,y)',HEIGHT_COLOR),
            ('area',r'\,dA',BASE_COLOR)],size=48)
        # Índices locais desaparecem; eles não se transformam na região R.
        # f, x, y, parênteses e A conservam seus próprios glifos.
        a,b = sum_eq.glyph_runs,integral.glyph_runs
        assert [len(a[k]) for k in ('op','fun','area')] == [4,8,2]
        assert [len(b[k]) for k in ('op','fun','area')] == [3,6,2]
        integral[0][b['op'][-1]].set_color(BASE_COLOR)
        limit_map = [([a['op'][0]],b['op'][:2]),
                     ([a['fun'][k] for k in (0,1,2,4,5,7)],b['fun']),
                     ([a['area'][0]],[b['area'][0]]),([a['area'][1]],[b['area'][1]])]
        self.play(FadeOut(limit_readout),FadeOut(shrinking_steps),Write(area_limit),run_time=0.7)
        self.mark('limite_explicito')
        self.hold(0.4)
        self.glyph_transfer(sum_eq,integral,limit_map,run_time=2)
        self.mark('soma_para_integral')
        self.cue("A integral é o limite dessas somas.")
        self.play(Indicate(base[0],color=BASE_COLOR),run_time=0.6)

        # Seção verdadeira, com área sob a curva; a projeção continua fixa.
        self.mark('secao_x_fixo')
        x0 = -0.75
        section = make_section(x0)
        self.cue("Agora, uma seção com x fixo.")
        section_note = MathTex(r"x=x_0",font_size=32).move_to([0,4.45,0]).set_z_index(100)
        # A malha 64×64 cumpriu a leitura do limite. A casca curva exata deixa
        # a seção legível sem milhares de arestas atravessando sua área.
        self.play(FadeOut(field),FadeIn(shell),FadeOut(VGroup(count,exact_note,exact_arrow,integral,area_limit)),
                  VGroup(*base[1:]).animate.set_opacity(0.12),
                  Write(section_note),Create(section[0]),run_time=1.4)
        self.play(Create(section[2]),Create(section[3]),run_time=1.6)
        self.cue("Primeiro, integramos em y.")
        y_tracker = ValueTracker(-1)
        section[1].become(partial_section_area(x0,-1))
        section[1].add_updater(lambda m:m.become(partial_section_area(x0,y_tracker.get_value())))
        y_marker = always_redraw(lambda: Dot(project_xyz(x0,y_tracker.get_value(),f(x0,y_tracker.get_value())),
                                             color=HEIGHT_COLOR,radius=0.06).set_z_index(65))
        y_height = always_redraw(lambda: Line(project_xyz(x0,y_tracker.get_value(),0),
                                              project_xyz(x0,y_tracker.get_value(),f(x0,y_tracker.get_value())),
                                              color=HEIGHT_COLOR,stroke_width=2).set_z_index(60))
        y_note = self.formula(r'y:\ -1\longrightarrow1',size=31,y=-3.5).set_color(INNER_COLOR)
        self.add(section[1],y_marker,y_height)
        self.play(Write(y_note),y_tracker.animate.set_value(1),run_time=3,rate_func=linear)
        section[1].clear_updaters()
        y_marker.clear_updaters()
        y_height.clear_updaters()
        self.play(FadeOut(y_marker),FadeOut(y_height),FadeOut(y_note),run_time=0.5)
        area_name = MathTex(r"A(x_0)",font_size=32,color=INNER_COLOR).move_to([-2.8,0.6,0]).set_z_index(100)
        area_arrow = Arrow(area_name.get_right(),project_xyz(x0,0,1.5),buff=0.16,
                           color=INNER_COLOR,stroke_width=1.8).set_z_index(100)
        self.play(TransformFromCopy(section[1],area_name),GrowArrow(area_arrow),run_time=1.6)
        area_integral = self.glyph_formula([
            ('area',r'A(x_0)',INNER_COLOR),('eq','=',TEXT_COLOR),
            ('op',r'\int_{-1}^{1}',INNER_COLOR),('fun',r'f(x_0,y)',HEIGHT_COLOR),
            ('dy',r'\,dy',INNER_COLOR)],size=41)
        area_integral[0][area_integral.glyph_runs['fun'][-2]].set_color(INNER_COLOR)
        self.play(TransformFromCopy(area_name,group(area_integral,'area')),
                  Write(group(area_integral,'eq','op','fun','dy')),run_time=1.7)
        self.remove(*area_integral.get_family())
        self.add(area_integral)
        self.play(Circumscribe(VGroup(*[area_integral[0][k] for k in area_integral.glyph_runs['dy']]),
                              color=INNER_COLOR,buff=0.12),run_time=1)

        self.mark('secao_percorre_x')
        tracker = ValueTracker(x0)
        # Só uma seção (4 objetos, 65 amostras) é recalculada por frame.
        section.add_updater(lambda m: m.become(make_section(tracker.get_value())))
        self.add(section)
        live_area = self.glyph_formula([
            ('area',r'A(x)',INNER_COLOR),('eq','=',TEXT_COLOR),
            ('op',r'\int_{-1}^{1}',INNER_COLOR),('fun',r'f(x,y)',HEIGHT_COLOR),
            ('dy',r'\,dy',INNER_COLOR)],size=41)
        live_area[0][live_area.glyph_runs['fun'][-2]].set_color(INNER_COLOR)
        self.glyph_transfer(area_integral,live_area,[(k,k) for k in ('area','eq','op','fun','dy')],
                            run_time=1.3,extras=(FadeOut(area_name),FadeOut(area_arrow),FadeOut(section_note)))
        self.play(tracker.animate.set_value(-1),run_time=0.9)
        self.cue("Depois, integramos em x.")
        outer = self.glyph_formula([
            ('v',r'V=',VOLUME_COLOR),('op',r'\int_{-1}^{1}',OUTER_COLOR),
            ('area',r'A(x)',INNER_COLOR),('dx',r'\,dx',OUTER_COLOR)],size=44,y=-5.9)
        self.play(TransformFromCopy(group(live_area,'area'),group(outer,'area')),
                  Write(group(outer,'v','op','dx')),run_time=1)
        self.remove(*outer.get_family())
        self.add(outer)
        traces = VGroup()
        for x in (-0.5,0,0.5,1):
            trace = make_section(x)[1].set_fill(OUTER_COLOR,opacity=0)
            trace.set_stroke(OUTER_COLOR,width=0.6,opacity=0)
            def reveal_trace(m,position=x):
                passed = tracker.get_value() >= position
                m.set_fill(opacity=0.065 if passed else 0)
                m.set_stroke(opacity=0.25 if passed else 0)
            trace.add_updater(reveal_trace)
            traces.add(trace)
        # Um único movimento atravessa R. Cada rastro só aparece após a seção
        # alcançar sua posição, sem antecipar áreas ainda não percorridas.
        self.add(traces)
        self.play(tracker.animate.set_value(1),run_time=3.6,rate_func=linear)
        traces.clear_updaters()
        section.clear_updaters()
        self.play(Circumscribe(VGroup(*[outer[0][k] for k in outer.glyph_runs['dx']]),
                              color=OUTER_COLOR,buff=0.12),run_time=1)
        self.mark('integral_das_secoes')
        iterated = self.glyph_formula([
            ('v',r'V=',VOLUME_COLOR),('outer',r'\int_{-1}^{1}',OUTER_COLOR),
            ('left',r'\bigl[',INNER_COLOR),('inner',r'\int_{-1}^{1}',INNER_COLOR),
            ('fun',r'f(x,y)',HEIGHT_COLOR),('dy',r'\,dy',INNER_COLOR),
            ('right',r'\bigr]',INNER_COLOR),('dx',r'\,dx',OUTER_COLOR)],size=41)
        iterated[0][iterated.glyph_runs['fun'][-2]].set_color(INNER_COLOR)
        self.cue("Substitua A(x) pela integral em y.")
        self.play(Indicate(group(live_area,'op','fun','dy'),color=INNER_COLOR,scale_factor=1.06),run_time=0.8)
        self.play(ReplacementTransform(group(outer,'v'),group(iterated,'v')),
                  ReplacementTransform(group(outer,'op'),group(iterated,'outer')),
                  ReplacementTransform(group(outer,'dx'),group(iterated,'dx')),
                  TransformFromCopy(group(live_area,'op','fun','dy'),group(iterated,'inner','fun','dy')),
                  FadeIn(group(iterated,'left','right')),FadeOut(group(outer,'area')),
                  FadeOut(live_area),run_time=2.5)
        self.remove(*outer.get_family(),*live_area.get_family(),*iterated.get_family())
        self.add(iterated)
        self.mark('integral_iterada')

        # Uma expressão transforma-se na seguinte; as primitivas ficam explícitas.
        self.play(FadeOut(section),FadeOut(traces),run_time=0.7)
        self.cue("Primeiro, integramos em y.")
        explicit = self.glyph_formula([
            ('v',r'V=',VOLUME_COLOR),('outer',r'\int_{-1}^{1}',OUTER_COLOR),
            ('left',r'\bigl[',INNER_COLOR),('inner',r'\int_{-1}^{1}',INNER_COLOR),
            ('open','(',TEXT_COLOR),('constant',r'4-x^2',TEXT_COLOR),('minus','-',TEXT_COLOR),
            ('yterm',r'y^2',INNER_COLOR),('close',')',TEXT_COLOR),('dy',r'\,dy',INNER_COLOR),
            ('right',r'\bigr]',INNER_COLOR),('dx',r'\,dx',OUTER_COLOR)],size=39)
        self.glyph_transfer(iterated,explicit,[(k,k) for k in ('v','outer','left','inner','dy','right','dx')],run_time=1.6)
        self.mark('integral_iterada_explicita')
        self.hold(0.5)
        # A geometria continua como contexto; a conta ocupa a metade inferior.
        math_geometry = VGroup(axes,base,rim,surface,shell,domain_tag)
        math_geometry.save_state()
        self.play(math_geometry.animate.scale(0.68,about_point=ORIGIN).shift(UP*1.9).fade(0.72),run_time=1)
        algebra = lambda runs,size=45,y=-2.5: self.glyph_formula(runs,size=size,y=y)
        eq = self.glyph_formula([
            ('op',r'\int_{-1}^{1}',INNER_COLOR),('left',r'\bigl(',TEXT_COLOR),
            ('constant',r'4-x^2',TEXT_COLOR),('minus','-',TEXT_COLOR),
            ('yterm',r'y^2',TEXT_COLOR),('right',r'\bigr)',TEXT_COLOR),
            ('dy',r'\,dy',INNER_COLOR)],size=45,y=-2.5)
        self.active_variable(eq,'y',INNER_COLOR)
        self.glyph_transfer(explicit,eq,[('inner','op'),('dy','dy'),('constant','constant'),
                                       ('minus','minus'),('yterm','yterm'),('open','left'),('close','right')],run_time=1.8)
        parked_outer = algebra([
            ('v',r'V=',VOLUME_COLOR),('op',r'\int_{-1}^{1}',OUTER_COLOR),
            ('area',r'A(x)',INNER_COLOR),('dx',r'\,dx',OUTER_COLOR)],size=28,y=-0.8).set_opacity(0.4)
        constant_note = screen_text("x fica constante.",25,oversample=2).move_to([0,-6.8,0]).set_z_index(100)
        self.play(FadeIn(parked_outer),FadeIn(constant_note),
                  Circumscribe(group(eq,'constant'),color=TEXT_COLOR,buff=0.12),run_time=1)
        self.mark('integral_y_isolada')
        self.hold(0.7)
        separated = algebra([
            ('left','(',TEXT_COLOR),('constant',r'4-x^2',TEXT_COLOR),('right',')',TEXT_COLOR),
            ('op_const',r'\int_{-1}^{1}',INNER_COLOR),('dy_const',r'\,dy',INNER_COLOR),
            ('minus','-',TEXT_COLOR),('op_power',r'\int_{-1}^{1}',INNER_COLOR),
            ('yterm',r'y^2',TEXT_COLOR),('dy_power',r'\,dy',INNER_COLOR)],size=43)
        self.active_variable(separated,'y',INNER_COLOR)
        self.glyph_transfer(eq,separated,[('left','left'),('constant','constant'),('right','right'),
            ('op','op_power'),('minus','minus'),('yterm','yterm'),('dy','dy_power')],run_time=2.1)
        self.mark('separacao_integral_y')
        self.hold(0.6)
        rule_constant = algebra([
            ('op',r'\int',INNER_COLOR),('dy',r'\,dy',INNER_COLOR),('eq','=',TEXT_COLOR),
            ('factor','y',INNER_COLOR)],size=37,y=-4.4)
        self.play(Write(group(rule_constant,'op','eq')),
                  TransformFromCopy(group(separated,'dy_const'),group(rule_constant,'dy')),run_time=1)
        self.play(TransformFromCopy(group(rule_constant,'dy'),group(rule_constant,'factor')),run_time=1.3)
        self.remove(*rule_constant.get_family())
        self.add(rule_constant)
        rule_power = algebra([
            ('op',r'\int',INNER_COLOR),('yterm',r'y^2',TEXT_COLOR),('dy',r'\,dy',INNER_COLOR),
            ('eq','=',TEXT_COLOR),('primitive',r'\frac{y^3}{3}',TEXT_COLOR)],size=37,y=-5.8)
        self.active_variable(rule_power,'y',INNER_COLOR)
        self.cue("A potência aumenta de 2 para 3; dividimos por 3.")
        self.play(TransformFromCopy(group(separated,'yterm'),group(rule_power,'yterm')),
                  Write(group(rule_power,'op','dy','eq')),run_time=1.1)
        self.play(TransformFromCopy(group(rule_power,'yterm'),group(rule_power,'primitive')),run_time=1.8)
        self.remove(*rule_power.get_family())
        self.add(rule_power)
        self.mark('regra_potencia_y')
        self.hold(0.8)
        primitive = algebra([
            ('left','(',TEXT_COLOR),('constant',r'4-x^2',TEXT_COLOR),('right',')',TEXT_COLOR),
            ('factor','y',INNER_COLOR),('minus','-',TEXT_COLOR),
            ('yterm',r'\frac{y^3}{3}',TEXT_COLOR)])
        self.active_variable(primitive,'y',INNER_COLOR)
        self.assemble_formula(primitive,[(group(separated,k),k) for k in ('left','constant','right','minus')]+
            [(group(rule_constant,'factor'),'factor'),(group(rule_power,'primitive'),'yterm')],
            removes=(separated,rule_constant,rule_power),run_time=2.1)
        self.mark('primitiva_y_montada')
        self.hold(0.7)
        bounded_y = algebra([
            ('bound_left',r'\bigl[',INNER_COLOR),('left','(',TEXT_COLOR),
            ('constant',r'4-x^2',TEXT_COLOR),('right',')',TEXT_COLOR),
            ('factor','y',INNER_COLOR),('minus','-',TEXT_COLOR),
            ('yterm',r'\frac{y^3}{3}',TEXT_COLOR),('bounds',r'\bigr]_{-1}^{1}',INNER_COLOR)])
        self.active_variable(bounded_y,'y',INNER_COLOR)
        self.glyph_transfer(primitive,bounded_y,[(k,k) for k in primitive.glyph_runs],run_time=1.2)
        self.mark('primitiva_interna')
        self.cue("Aplique y = 1 e y = −1.")
        self.play(FadeOut(constant_note),Circumscribe(group(bounded_y,'bounds'),color=INNER_COLOR,buff=0.12),run_time=0.8)
        upper_y = algebra([
            ('label',r'y=1:\quad',INNER_COLOR),('left','(',TEXT_COLOR),('constant',r'4-x^2',TEXT_COLOR),
            ('right',')',TEXT_COLOR),('factor','(1)',INNER_COLOR),('minus','-',TEXT_COLOR),
            ('yterm',r'\frac{1^3}{3}',TEXT_COLOR)],size=38,y=-4.3)
        lower_y = algebra([
            ('label',r'y=-1:\quad',INNER_COLOR),('left','(',TEXT_COLOR),('constant',r'4-x^2',TEXT_COLOR),
            ('right',')',TEXT_COLOR),('factor','(-1)',INNER_COLOR),('minus','-',TEXT_COLOR),
            ('yterm',r'\frac{(-1)^3}{3}',TEXT_COLOR)],size=38,y=-5.9)
        self.glyph_transfer(bounded_y,upper_y,[(k,k) for k in ('left','constant','right','factor','minus','yterm')],
                            run_time=1.8,from_copy=True)
        self.mark('substituicao_y_mais_1')
        self.hold(0.6)
        self.glyph_transfer(bounded_y,lower_y,[(k,k) for k in ('left','constant','right','factor','minus','yterm')],
                            run_time=1.8,from_copy=True)
        self.mark('substituicao_y_menos_1')
        self.hold(0.7)
        simple_upper_y = algebra([
            ('label',r'y=1:\quad',INNER_COLOR),('left','(',TEXT_COLOR),('constant',r'4-x^2',TEXT_COLOR),
            ('right',')',TEXT_COLOR),('minus','-',TEXT_COLOR),('yterm',r'\frac13',TEXT_COLOR)],size=38,y=-4.3)
        simple_lower_y = algebra([
            ('label',r'y=-1:\quad',INNER_COLOR),('sign','-',TEXT_COLOR),('left','(',TEXT_COLOR),
            ('constant',r'4-x^2',TEXT_COLOR),('right',')',TEXT_COLOR),('plus','+',TEXT_COLOR),
            ('yterm',r'\frac13',TEXT_COLOR)],size=38,y=-5.9)
        self.glyph_transfer(upper_y,simple_upper_y,[(k,k) for k in simple_upper_y.glyph_runs],run_time=1.2)
        self.glyph_transfer(lower_y,simple_lower_y,[(k,k) for k in ('label','left','constant','right','yterm')],run_time=1.2)
        self.cue("Valor em y = 1 menos o valor em y = −1.")
        difference_y = algebra([
            ('open1',r'\bigl[(',TEXT_COLOR),('constant1',r'4-x^2',TEXT_COLOR),('close1',')',TEXT_COLOR),
            ('minus1','-',TEXT_COLOR),('fraction1',r'\frac13',TEXT_COLOR),('bracket1',r'\bigr]',TEXT_COLOR),
            ('minus','-',TEXT_COLOR),('open2',r'\bigl[-(',TEXT_COLOR),('constant2',r'4-x^2',TEXT_COLOR),
            ('close2',')',TEXT_COLOR),('plus','+',TEXT_COLOR),('fraction2',r'\frac13',TEXT_COLOR),
            ('bracket2',r'\bigr]',TEXT_COLOR)],size=41)
        self.assemble_formula(difference_y,[(group(simple_upper_y,'constant'),'constant1'),
            (group(simple_upper_y,'yterm'),'fraction1'),(group(simple_lower_y,'constant'),'constant2'),
            (group(simple_lower_y,'yterm'),'fraction2')],
            removes=(bounded_y,simple_upper_y,simple_lower_y),run_time=2)
        self.mark('subtracao_limites_y')
        self.hold(0.8)
        evaluated = algebra([
            ('factor','2',TEXT_COLOR),('left','(',TEXT_COLOR),('constant',r'4-x^2',TEXT_COLOR),
            ('right',')',TEXT_COLOR),('minus','-',TEXT_COLOR),('yterm',r'\frac23',TEXT_COLOR)])
        self.glyph_transfer(difference_y,evaluated,[
            (difference_y.glyph_runs['constant1']+difference_y.glyph_runs['constant2'],'constant'),
            (difference_y.glyph_runs['fraction1']+difference_y.glyph_runs['fraction2'],'yterm'),('minus','minus')],run_time=1.8)
        self.mark('limites_y_agrupados')
        self.hold(0.6)
        expanded_area = algebra([
            ('constant','8',TEXT_COLOR),('minus','-',TEXT_COLOR),('xterm',r'2x^2',TEXT_COLOR),
            ('minus_fraction','-',TEXT_COLOR),('fraction',r'\frac23',TEXT_COLOR)])
        a,b = evaluated.glyph_runs,expanded_area.glyph_runs
        self.glyph_transfer(evaluated,expanded_area,[([a['constant'][0]],'constant'),
            ([a['constant'][1]],'minus'),(a['factor']+a['constant'][2:],'xterm'),
            ('minus','minus_fraction'),('yterm','fraction')],run_time=1.6)
        self.mark('area_expandida')
        self.hold(0.6)
        result_area = algebra([
            ('area',r'A(x)=',INNER_COLOR),('constant',r'\frac{22}{3}',TEXT_COLOR),
            ('minus','-',TEXT_COLOR),('xterm',r'2x^2',TEXT_COLOR)],size=46)
        self.glyph_transfer(expanded_area,result_area,[
            (expanded_area.glyph_runs['constant']+expanded_area.glyph_runs['fraction'],'constant'),
            ('minus','minus'),('xterm','xterm')],run_time=1.6)
        self.mark('area_calculada')
        self.hold(0.7)
        self.clear_cue()
        area_return = make_section(0)
        area_return.scale(0.68,about_point=ORIGIN).shift(UP*1.9)
        self.play(FadeIn(area_return),run_time=0.8)
        self.play(Indicate(area_return[1],color=INNER_COLOR,scale_factor=1.03),
                  Indicate(group(result_area,'area'),color=INNER_COLOR,scale_factor=1.08),run_time=1.3)
        self.mark('payoff_area_secao')
        self.hold(0.8)
        self.play(FadeOut(area_return),FadeOut(parked_outer),
                  result_area.animate.move_to(UP*-6.5),run_time=0.8)
        self.mark('primitiva_externa')
        self.cue("Depois, integramos em x.")
        outer_definition = algebra([
            ('v',r'V=',VOLUME_COLOR),('op',r'\int_{-1}^{1}',OUTER_COLOR),
            ('area',r'A(x)',TEXT_COLOR),('dx',r'\,dx',OUTER_COLOR)])
        self.glyph_transfer(result_area,outer_definition,[(result_area.glyph_runs['area'][:-1],'area')],
                            run_time=1.6,from_copy=True)
        self.mark('integral_x_de_area')
        self.hold(0.6)
        outer_eval = algebra([
            ('v',r'V=',VOLUME_COLOR),('op',r'\int_{-1}^{1}',OUTER_COLOR),
            ('left','(',TEXT_COLOR),('constant',r'\frac{22}{3}',TEXT_COLOR),
            ('minus','-',TEXT_COLOR),('xterm',r'2x^2',TEXT_COLOR),
            ('right',')',TEXT_COLOR),('dx',r'\,dx',OUTER_COLOR)])
        self.active_variable(outer_eval,'x',OUTER_COLOR)
        self.assemble_formula(outer_eval,[(group(outer_definition,k),k) for k in ('v','op','dx')]+
            [(group(result_area,k),k) for k in ('constant','minus','xterm')],
            removes=(outer_definition,result_area),run_time=2)
        self.mark('substituicao_area_integral_x')
        self.play(Circumscribe(group(outer_eval,'dx'),color=OUTER_COLOR,buff=0.12),run_time=0.8)
        separated_x = algebra([
            ('v',r'V=',VOLUME_COLOR),('op_const',r'\int_{-1}^{1}',OUTER_COLOR),
            ('constant',r'\frac{22}{3}',TEXT_COLOR),('dx_const',r'\,dx',OUTER_COLOR),
            ('minus','-',TEXT_COLOR),('op_power',r'\int_{-1}^{1}',OUTER_COLOR),
            ('xterm',r'2x^2',TEXT_COLOR),('dx_power',r'\,dx',OUTER_COLOR)],size=43)
        self.active_variable(separated_x,'x',OUTER_COLOR)
        self.glyph_transfer(outer_eval,separated_x,[('v','v'),('op','op_const'),('constant','constant'),
            ('dx','dx_const'),('minus','minus'),('xterm','xterm')],run_time=1.8)
        self.mark('separacao_integral_x')
        rule_x_constant = algebra([
            ('op',r'\int',OUTER_COLOR),('constant',r'\frac{22}{3}',TEXT_COLOR),
            ('dx',r'\,dx',OUTER_COLOR),('eq','=',TEXT_COLOR),
            ('primitive',r'\frac{22x}{3}',TEXT_COLOR)],size=37,y=-4.4)
        self.active_variable(rule_x_constant,'x',OUTER_COLOR)
        self.play(TransformFromCopy(group(separated_x,'constant'),group(rule_x_constant,'constant')),
                  Write(group(rule_x_constant,'op','dx','eq')),run_time=1)
        self.play(TransformFromCopy(group(rule_x_constant,'constant'),group(rule_x_constant,'primitive')),run_time=1.5)
        self.remove(*rule_x_constant.get_family())
        self.add(rule_x_constant)
        rule_x_power = algebra([
            ('op',r'\int',OUTER_COLOR),('xterm',r'2x^2',TEXT_COLOR),('dx',r'\,dx',OUTER_COLOR),
            ('eq','=',TEXT_COLOR),('primitive',r'\frac{2x^3}{3}',TEXT_COLOR)],size=37,y=-5.9)
        self.active_variable(rule_x_power,'x',OUTER_COLOR)
        self.play(TransformFromCopy(group(separated_x,'xterm'),group(rule_x_power,'xterm')),
                  Write(group(rule_x_power,'op','dx','eq')),run_time=1)
        self.play(TransformFromCopy(group(rule_x_power,'xterm'),group(rule_x_power,'primitive')),run_time=1.8)
        self.remove(*rule_x_power.get_family())
        self.add(rule_x_power)
        self.mark('regra_potencia_x')
        self.hold(0.8)
        # A primitiva ainda não é V: mostramos o termo entre colchetes no mesmo
        # passo em que entram os limites. Evita igualar V a uma função de x.
        primitive_x = algebra([
            ('constant',r'\frac{22x}{3}',TEXT_COLOR),('minus','-',TEXT_COLOR),
            ('xterm',r'\frac{2x^3}{3}',TEXT_COLOR)])
        self.active_variable(primitive_x,'x',OUTER_COLOR)
        self.assemble_formula(primitive_x,[(group(rule_x_constant,'primitive'),'constant'),
            (group(separated_x,'minus'),'minus'),(group(rule_x_power,'primitive'),'xterm')],
            removes=(separated_x,rule_x_constant,rule_x_power),run_time=2)
        self.mark('primitiva_x_montada')
        self.hold(0.7)
        bounded_x = algebra([
            ('v',r'V=',VOLUME_COLOR),('left',r'\bigl[',OUTER_COLOR),
            ('constant',r'\frac{22x}{3}',TEXT_COLOR),('minus','-',TEXT_COLOR),
            ('xterm',r'\frac{2x^3}{3}',TEXT_COLOR),('bounds',r'\bigr]_{-1}^{1}',OUTER_COLOR)])
        self.active_variable(bounded_x,'x',OUTER_COLOR)
        self.glyph_transfer(primitive_x,bounded_x,[(k,k) for k in primitive_x.glyph_runs],run_time=1.2)
        self.cue("Aplique x = 1 e x = −1.")
        self.play(Circumscribe(group(bounded_x,'bounds'),color=OUTER_COLOR,buff=0.12),run_time=0.8)
        upper_x = algebra([
            ('label',r'x=1:\quad',OUTER_COLOR),('constant',r'\frac{22}{3}',TEXT_COLOR),
            ('minus','-',TEXT_COLOR),('xterm',r'\frac23',TEXT_COLOR)],size=39,y=-4.3)
        lower_x = algebra([
            ('label',r'x=-1:\quad',OUTER_COLOR),('sign','-',TEXT_COLOR),
            ('constant',r'\frac{22}{3}',TEXT_COLOR),('plus','+',TEXT_COLOR),
            ('xterm',r'\frac23',TEXT_COLOR)],size=39,y=-5.9)
        self.glyph_transfer(bounded_x,upper_x,[(k,k) for k in ('constant','minus','xterm')],run_time=1.7,from_copy=True)
        self.mark('substituicao_x_mais_1')
        self.hold(0.6)
        self.glyph_transfer(bounded_x,lower_x,[('constant','constant'),('xterm','xterm')],run_time=1.7,from_copy=True)
        self.mark('substituicao_x_menos_1')
        self.hold(0.7)
        values = []
        for source,sign,y in ((upper_x,'',-4.3),(lower_x,'-',-5.9)):
            runs = [(name,source_tex,TEXT_COLOR) for name,source_tex in
                ([('constant',r'\frac{22}{3}'),('minus','-'),('xterm',r'\frac23')]
                 if not sign else [('sign','-'),('constant',r'\frac{22}{3}'),('plus','+'),('xterm',r'\frac23')])]
            result = algebra([('label',r'x='+('-1' if sign else '1')+r':\quad',OUTER_COLOR)]+
                runs+[('eq','=',TEXT_COLOR),('value',sign+r'\frac{20}{3}',TEXT_COLOR)],size=39,y=y)
            self.glyph_transfer(source,result,[(k,k) for k in source.glyph_runs],run_time=1.2)
            values.append(result)
        self.mark('valores_limites_x')
        self.hold(0.7)
        evaluated_outer = algebra([
            ('v',r'V=',VOLUME_COLOR),('positive',r'\frac{20}{3}',TEXT_COLOR),('minus','-',TEXT_COLOR),
            ('left','(',TEXT_COLOR),('sign','-',TEXT_COLOR),('negative',r'\frac{20}{3}',TEXT_COLOR),
            ('right',')',TEXT_COLOR)],size=48)
        self.assemble_formula(evaluated_outer,[(group(bounded_x,'v'),'v'),
            (group(values[0],'value'),'positive'),
            (VGroup(*[values[1][0][k] for k in values[1].glyph_runs['value'][1:]]),'negative')],
            removes=(bounded_x,*values),run_time=1.7)
        # O sinal de -20/3 pertence ao run 'sign', já presente no destino;
        # transferimos só a fração positiva para evitar dois sinais negativos.
        self.mark('subtracao_limites_x')
        self.hold(0.7)
        sum_values = algebra([
            ('v',r'V=',VOLUME_COLOR),('value',r'\frac{20+20}{3}',TEXT_COLOR)],size=48)
        self.glyph_transfer(evaluated_outer,sum_values,[('v','v'),
            (evaluated_outer.glyph_runs['positive']+evaluated_outer.glyph_runs['negative'],'value')],run_time=1.5)
        self.hold(0.6)
        eq = algebra([('v',r'V=',VOLUME_COLOR),('value',r'\frac{40}{3}',TEXT_COLOR)],size=49)
        self.glyph_transfer(sum_values,eq,[('v','v'),('value','value')],run_time=1.4)
        self.mark('resultado_exato')
        self.hold(0.7)
        nxt = algebra([
            ('v',r'V=',VOLUME_COLOR),('value',r'\frac{40}{3}',TEXT_COLOR),
            ('approx',r'\approx13{,}33',TEXT_COLOR)],size=49)
        self.glyph_transfer(eq,nxt,[('v','v'),('value','value')],run_time=1.2)
        eq = nxt
        self.hold(0.8)
        self.mark('resultado_40_3')

        # Retorno breve à mesma malha 64×64 e à fórmula da abertura.
        self.mark('payoff')
        self.clear_cue()
        self.play(FadeOut(eq),Restore(math_geometry),run_time=1)
        final_field = make_dense_column_field(64)
        self.play(FadeOut(shell),FadeIn(final_field),
                  ShowPassingFlash(surface.copy().set_stroke(width=2.5,opacity=1),time_width=0.3),run_time=1.6)
        final_eq = self.formula(r"V=",r"\iint_R",r"f(x,y)",r"dA",size=48)
        final_eq[0].set_color(VOLUME_COLOR)
        final_eq[1].set_color(VOLUME_COLOR)
        final_eq[1][-1].set_color(BASE_COLOR)
        final_eq[2].set_color(HEIGHT_COLOR)
        final_eq[3].set_color(BASE_COLOR)
        self.play(Write(final_eq[:2]),TransformFromCopy(surface,final_eq[2]),
                  TransformFromCopy(base[0],final_eq[3]),run_time=1.6)
        message = VGroup(screen_text("Somar pequenas contribuições",27,oversample=2),
                         screen_text("sobre toda a área.",27,oversample=2)).arrange(DOWN,buff=0.1)
        message.move_to(UP*5.45).set_z_index(100)
        self.play(FadeIn(message),Indicate(base[0],color=BASE_COLOR),run_time=1)
        self.hold(1.1)
        self.mark('fim')
        Path(config.media_dir,'marcos.json').write_text(json.dumps(self.events,indent=2,ensure_ascii=False),encoding='utf-8')

"""vid_0019 — narração fornecida, 129,6 s, sincronização e legendas.
Final 1080x1920 / 30 fps. Manim-only; EP. 02 confirmado.
"""
import json
import sys
from contextlib import contextmanager
from pathlib import Path
import numpy as np
from manim import (
    AnimationGroup, Arc, Arrow, Circle, Create, DashedLine, DecimalNumber, Dot, DOWN,
    FadeIn, FadeOut, GrowFromEdge, ImageMobject, Indicate, LEFT, Line,
    MathTex, PI, Polygon, Rectangle, RIGHT, Scene, Succession, Transform, TransformFromCopy,
    TransformMatchingTex, UP, ValueTracker, VGroup, WHITE, Write,
    Wait, config, linear,
)
from manim.renderer.cairo_renderer import CairoRenderer
from manim.scene.scene_file_writer import SceneFileWriter
ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from template.config import BACKGROUND_COLOR, PRIMARY_COLOR, TEXT_COLOR, WATERMARK_PATH
from template.fonts import screen_text
CYAN, VIOLET, PINK, BLUE, DIM = PRIMARY_COLOR, '#9C8CFF', '#EA63FF', '#267BFF', '#9AA6C5'
G, HEIGHT = 9.81, 2000
V_FINAL = np.sqrt(2 * G * HEIGHT)
KMH_FINAL = 3.6 * V_FINAL
ENERGY_RATIO = (5 / 2) ** 3

@contextmanager
def wide_pango():
    pw, ph = config.pixel_width, config.pixel_height
    config.pixel_width, config.pixel_height = 4000, 4000
    try:
        yield
    finally:
        config.pixel_width, config.pixel_height = pw, ph

def label(content, size=30, color=TEXT_COLOR, width=7.0, opacity=1.0):
    with wide_pango():
        result = screen_text(content, size, oversample=2 if size >= 30 else 4)
    result.set_color(color).set_opacity(opacity)
    if result.width > width:
        result.scale_to_fit_width(width)
    return result

def formula(*parts, size=44, color=TEXT_COLOR, width=6.9):
    result = MathTex(*parts, font_size=size, color=color)
    if result.width > width:
        result.scale_to_fit_width(width)
    return result

def drop(radius=.48, color=CYAN):
    # Esferoide aproximado. Ambiente e movimento comunicam chuva, sem lágrima.
    glow = VGroup(*[Circle(radius=radius*f, stroke_width=0,
                           fill_color=color, fill_opacity=o)
                    for f,o in ((1.65,.025),(1.35,.05),(1.12,.08))])
    body = Circle(radius=radius, color=color, stroke_width=2.5)
    body.set_fill(BLUE if color == CYAN else '#745CFF', opacity=.70)
    shine = Arc(radius=radius*.63, start_angle=PI/2, angle=PI/2.3,
                color=WHITE, stroke_width=2.2)
    shine.shift(UP*radius*.09 + LEFT*radius*.09)
    return VGroup(glow, body, shine).set_z_index(5)

class RainField(VGroup):
    """Chuva contextual persistente; profundidade e rastros discretos."""
    def __init__(self, phase, intensity, speed):
        super().__init__()
        self.phase, self.intensity, self.speed = phase, intensity, speed
        rng = np.random.default_rng(19)
        self.parameters, self.particles = [], VGroup()
        for _ in range(48):
            depth = rng.uniform(.45,1)
            self.parameters.append((rng.uniform(-4.05,4.05), rng.uniform(0,12), depth))
            self.particles.add(VGroup(
                Line(UP*.1, DOWN*.1, color=CYAN, stroke_width=1.5),
                Dot(radius=.026+.018*depth, color=CYAN)))
        self.origin_line = Line([-4.15,6.23,0],[4.15,6.23,0],color=CYAN,
                                stroke_width=1.5,stroke_opacity=.23)
        self.add(self.origin_line,self.particles)
        self.set_z_index(-5)
        self.add_updater(lambda mob: mob.refresh())
        self.refresh()
    def refresh(self):
        strength = self.intensity.get_value()
        for particle,(x,offset,depth) in zip(self.particles,self.parameters):
            y = 6.12-((offset+self.phase.get_value()*depth)%12)
            length = (.22+.30*self.speed())*depth
            particle[0].put_start_and_end_on([x,min(6.23,y+length),0],[x,y,0])
            particle[1].move_to([x,y,0])
            particle.set_opacity(strength*(.14+.30*depth))

class QualitativeDial(VGroup):
    def __init__(self, center, progress):
        super().__init__()
        self.progress = progress
        radius = 1.48
        self.pivot = Dot(radius=.085,color=CYAN)
        self.arc = Arc(radius=radius,start_angle=5*PI/6,angle=-2*PI/3,
                       color=DIM,stroke_width=4)
        ticks = VGroup()
        for fraction in np.linspace(0,1,9):
            angle = 5*PI/6-2*PI/3*fraction
            direction = np.array([np.cos(angle),np.sin(angle),0])
            ticks.add(Line(direction*radius*.86,direction*radius,color=DIM,stroke_width=2.5))
        self.needle = Line([0,0,0],[0,1.2,0],color=CYAN,stroke_width=6)
        title = label('velocidade',28,width=3).move_to([0,-.60,0])
        note = label('escala qualitativa',18,DIM,width=3).move_to([0,-1.12,0])
        self.add(self.arc,ticks,self.needle,self.pivot,title,note)
        self.shift(center)
        self.add_updater(lambda mob: mob.refresh())
        self.refresh()
    def refresh(self):
        c = self.pivot.get_center()
        radius = self.arc.width/np.sqrt(3)
        angle = 5*PI/6-2*PI/3*np.clip(self.progress(),0,1)
        self.needle.put_start_and_end_on(c,c+.81*radius*np.array([np.cos(angle),np.sin(angle),0]))

class NumericSpeed(VGroup):
    """Número grande com unidade explícita e ancoragem estável."""
    def __init__(self, center, value, color=CYAN, size=66, unit='m/s'):
        super().__init__()
        self.value = value
        self.anchor = Dot(radius=.001).set_opacity(0)
        self.number = DecimalNumber(0,num_decimal_places=0,group_with_commas=False,
                                    font_size=size,color=color)
        self.approx = formula(r'\approx',size=size*.48,color=color)
        self.caption = label('velocidade',size*.37,DIM).move_to([0,.92*size/66,0])
        self.unit = formula(r'\mathrm{'+unit+'}',size=size*.46,color=color).move_to([0,-.78*size/66,0])
        self.add(self.anchor,self.caption,self.number,self.approx,self.unit)
        self.shift(np.array(center)-self.anchor.get_center())
        self.add_updater(lambda mob: mob.refresh())
        self.refresh()
    def refresh(self):
        self.number.set_value(self.value()).move_to(self.anchor)
        self.approx.next_to(self.number,LEFT,buff=.12)
    def set_unit(self, unit):
        self.unit.become(formula(r'\mathrm{'+unit+'}',size=self.unit.font_size,
                                 color=self.unit.get_color()).move_to(self.unit))

class FinalFileWriter(SceneFileWriter):
    """Compressão de alta qualidade somente nesta unidade (Manim CE 0.21)."""
    def open_partial_movie_stream(self, file_path=None):
        super().open_partial_movie_stream(file_path)
        if config.pixel_width >= 1080:
            self._current_encode_job.stream.options = {'an':'1','crf':'16','preset':'medium'}


class ChuvaSemArrasto019(Scene):
    def __init__(self, renderer=None, **kwargs):
        super().__init__(renderer=renderer or CairoRenderer(file_writer_class=FinalFileWriter),**kwargs)

    def construct(self):
        self.always_update_mobjects = True
        self.sync = json.loads(Path(__file__).with_name('sync.json').read_text(encoding='utf-8'))
        self.anchors = dict(self.sync['anchors'])
        self.score_time = 0.0
        # Preserva a coreografia aprovada; retira esperas e ancora cada conceito na voz.
        # Comentários 0–68 abaixo usam o tempo de referência da V5, antes deste mapa.
        # A segunda metade tem coreografia própria para explicar a velocidade relativa.
        self.timing_map = np.array([
            (0,0),(2.2,2.54),(5.8,6.5),(7,7.39),(11.2,10.6),
            (14.6,12.09),(15.5,15.2),(16.3,16.2),(19,17.24),
            (22.8,19.2),(25,20.7),(27,22.7),(28.2,25.05),
            (28.8,25.6),(29.4,26.1),(30.2,26.6),(31.6,28.25),
            (32.2,30.0),(34,31.45),(36.6,32.8),(38.2,34.1),
            (39.2,35.45),(40.6,37.45),(42,38.28),
            (45.6,41.6),(48.2,43.43),(49.5,44.1),(52,45.13),
            (54.6,46.6),(57.5,47.7),(60,49.04),
            (63.5,50.6),(66.5,52.2),(68,53.17),
        ])
        self.camera.background_color = BACKGROUND_COLOR
        self.wm = ImageMobject(str(WATERMARK_PATH)).set_width(1.8).set_opacity(.35)
        self.add(self.wm.to_corner(UP+RIGHT,buff=.28).set_z_index(20))
        self.series = label('ABSURDO CALCULÁVEL · EP. 02',20,opacity=.65)
        self.add(self.series.to_corner(UP+LEFT,buff=.4).set_z_index(20))
        self.caption = None
        speed, drag_factor = ValueTracker(.35), ValueTracker(1)
        elapsed = ValueTracker(0)
        elapsed.add_updater(lambda mob,dt: mob.increment_value(dt))
        self.add(elapsed)
        intensity, phase, force_scale = ValueTracker(.95), ValueTracker(0), ValueTracker(1)
        phase.add_updater(lambda mob,dt: mob.increment_value(dt*(1.4+4*speed.get_value())))
        rain = RainField(phase,intensity,speed.get_value)
        hero = drop().move_to([-1.9,2.65,0])
        dial = QualitativeDial([1.55,1.7,0],lambda: .72*speed.get_value())
        weight = Arrow(np.zeros(3),DOWN,buff=0,color=CYAN)
        drag = Arrow(np.zeros(3),UP,buff=0,color=PINK)
        def weight_update(mob):
            c = hero.get_center()
            mob.become(Arrow(c,c+DOWN*1.65*force_scale.get_value(),buff=0,
                            color=CYAN,stroke_width=7).set_z_index(7))
        def drag_update(mob):
            c = hero.get_center()
            length = 1.65*force_scale.get_value()*speed.get_value()**2
            factor = drag_factor.get_value()
            mob.become(Arrow(c,c+UP*max(.005,length*factor),buff=0,color=PINK,stroke_width=7)
                       .set_opacity(min(1,factor*5)).set_z_index(7))
        weight.add_updater(weight_update)
        drag.add_updater(drag_update)
        trail = VGroup(*[Line(np.zeros(3),UP,color=CYAN,stroke_width=2) for _ in range(3)])
        def trail_update(group):
            c, radius = hero.get_center(), hero[1].width/2
            for i,line in enumerate(group):
                x,y = c[0]+(i-1)*radius*.38, c[1]+radius*1.5+i*.14
                line.put_start_and_end_on([x,y,0],[x,y+.22+.65*speed.get_value(),0])
                line.set_opacity(.12+.15*min(speed.get_value(),1.5))
        trail.add_updater(trail_update)
        weight_update(weight)
        drag_update(drag)
        trail_update(trail)
        self.add(speed,drag_factor,force_scale,intensity,phase,rain,hero,trail,dial,weight,drag)

        # 0–7: headline e chuva desde o primeiro frame, contador numérico rápido.
        self.caption = label('E se o ar parasse\nde frear a chuva?',37,width=7.4)
        self.caption.move_to([0,5.35,0]).set_z_index(15)
        hook_value = ValueTracker(100)
        self.add(hook_value,self.caption)
        hook_hud = NumericSpeed([1.55,1.7,0],hook_value.get_value,size=76,unit='km/h')
        hook_hud.approx.set_opacity(0)
        switch = label('ARRASTO: ON',26,PINK).move_to([0,-1.7,0])
        scope = label('2 km de queda · prévia sem arrasto',22,DIM).move_to([0,-2.6,0])
        self.remove(dial)
        self.add(hook_hud,switch,scope)
        self.play(hero.animate.shift(DOWN*.25),speed.animate.set_value(.65),run_time=.8,rate_func=linear)
        self.play(Transform(switch,label('ARRASTO: OFF',26,PINK).move_to(switch)),
                  drag_factor.animate.set_value(0),hook_value.animate.set_value(250),
                  speed.animate.set_value(1.0),run_time=.6,rate_func=linear)
        self.play(hook_value.animate.set_value(700),speed.animate.set_value(1.7),
                  hero.animate.shift(DOWN*2.0),run_time=3.2,rate_func=lambda t:t*t)
        plus = formula('+',size=48,color=CYAN).next_to(hook_hud.number,RIGHT,buff=.12)
        self.play(FadeIn(plus),run_time=.2)
        self.show_caption('Mas por que isso\nnão acontece de verdade?',size=33,duration=.4)
        self.until(5.8)
        real_time = ValueTracker(0)
        self.add(real_time)
        speed.set_value(0)
        self.play(hero.animate.move_to([-1.9,2.85,0]),drag_factor.animate.set_value(1),
                  Transform(switch,label('ARRASTO: ON',24,PINK).move_to(switch)),
                  FadeOut(hook_hud),FadeOut(plus),FadeOut(scope),FadeIn(dial),run_time=.6)
        self.until(7)

        # 7–19: tanh e log(cosh) ligam movimento, ponteiro e arrasto suave.
        self.show_caption('A gravidade puxa.\nO arrasto cresce.',size=33,duration=.4)
        speed.add_updater(lambda mob:mob.set_value(np.tanh(real_time.get_value())))
        hero.add_updater(lambda mob:mob.move_to(
            [-1.9,2.85-.48*np.log(np.cosh(real_time.get_value())),0]))
        weight_name = label('peso',24,CYAN).move_to([-3,.55,0])
        drag_name = label('arrasto',24,PINK).move_to([-.65,3.5,0])
        self.play(FadeIn(weight_name),FadeIn(drag_name),real_time.animate.set_value(.3),
                  run_time=.6,rate_func=linear)
        self.run_to(11.2,real_time.animate.set_value(1.15),rate_func=linear)
        self.show_caption('Mais velocidade.\nMais resistência.',size=33,duration=.4,
                          extra=[real_time.animate.set_value(1.3)])
        self.run_to(14.6,real_time.animate.set_value(3.5),rate_func=linear)
        force_balance = formula(r'F_{\rm arrasto}\approx mg',size=30).move_to([0,-1.15,0])
        balance = formula(r'a\approx0',size=37).move_to([0,-2.0,0])
        terminal = label('velocidade terminal',31,CYAN).move_to([0,-2.9,0])
        real_range = label('0,5–5 mm → ~2–9 m/s',25,width=6).move_to([0,-3.65,0])
        real_source = label('UCAR / MetEd · precipitação',18,DIM).move_to([0,-4.25,0])
        self.play(FadeOut(switch),Write(force_balance),real_time.animate.set_value(3.6),run_time=.5,rate_func=linear)
        self.play(Write(balance),real_time.animate.set_value(3.7),run_time=.4,rate_func=linear)
        self.play(FadeIn(terminal),FadeIn(real_range),FadeIn(real_source),real_time.animate.set_value(3.8),run_time=.4,rate_func=linear)
        self.show_caption('Ela continua caindo.\nMas quase não acelera.',size=32,duration=.4,
                          extra=[real_time.animate.set_value(3.9)])
        self.run_to(19,real_time.animate.set_value(4.2),rate_func=linear)

        # 19–25: mesma gota, retirada do freio e preparação da queda, sem tela nova.
        speed.clear_updaters()
        hero.clear_updaters()
        self.show_caption('Agora desligamos só esse freio.',size=32,duration=.4)
        intact = label('gota mantida intacta por hipótese',21,DIM).move_to([0,-3.55,0])
        zero_drag = formula(r'F_{\rm arrasto}\to0',size=30,color=PINK).move_to([0,-2.2,0])
        self.play(drag_factor.animate.set_value(0),speed.animate.set_value(1.13),
                  FadeOut(force_balance),FadeOut(balance),FadeOut(terminal),FadeOut(drag_name),
                  FadeOut(real_range),FadeOut(real_source),
                  FadeIn(zero_drag),FadeIn(intact),run_time=.6,rate_func=linear)
        self.run_to(22.8,speed.animate.set_value(1.36),hero.animate.shift(DOWN*.65),rate_func=linear)
        self.show_caption('2 km · sem arrasto',size=34,duration=.4)

        # 25–42: um único progresso temporal para queda, HUD, metros e álgebra.
        flight = ValueTracker(0)
        self.add(flight)
        # Contador inteiro por truncamento: 713 só é exibido na chegada, sem arredondar antes.
        numeric = NumericSpeed([1,-.55,0],lambda: np.floor(KMH_FINAL*flight.get_value()),unit='km/h')
        fall_x,start_y,end_y = -2.55,3.65,-3.35
        ruler = VGroup(
            DashedLine([fall_x,start_y,0],[fall_x,end_y,0],color=DIM,stroke_opacity=.45),
            Line([-3.25,start_y,0],[-3.25,end_y,0],color=DIM,stroke_width=2),
            *[Line([-3.37,y,0],[-3.13,y,0],color=DIM,stroke_width=2)
              for y in np.linspace(end_y,start_y,5)])
        dimension = label('Δh total = 2 km',22,width=3.1).move_to([-2.25,4.45,0])
        rest = label('partida do repouso',20,DIM,width=3.6).move_to([1.25,4.45,0])
        distance_title = label('queda percorrida',19,DIM,width=2.9).move_to([-2.35,-3.95,0])
        distance_number = DecimalNumber(0,num_decimal_places=0,group_with_commas=False,
                                        font_size=30,color=CYAN).move_to([-2.45,-4.4,0])
        distance_unit = formula(r'\mathrm m',size=27,color=CYAN)
        distance = VGroup(distance_title,distance_number,distance_unit)
        def distance_update(_):
            distance_number.set_value(HEIGHT*flight.get_value()**2).move_to([-2.45,-4.4,0])
            distance_unit.next_to(distance_number,RIGHT,buff=.12)
        distance.add_updater(distance_update)
        distance_update(distance)
        self.play(Transform(hero,drop(.29).move_to([fall_x,start_y,0])),
                  force_scale.animate.set_value(.58),intensity.animate.set_value(.24),
                  FadeOut(dial),FadeOut(weight),FadeOut(weight_name),FadeOut(zero_drag),FadeOut(intact),
                  Create(ruler),FadeIn(dimension),FadeIn(rest),FadeIn(numeric),FadeIn(distance),run_time=1.0)
        self.until(25)
        hero.add_updater(lambda mob: mob.move_to([
            fall_x,start_y-(start_y-end_y)*flight.get_value()**2,0]))
        speed.set_value(0)
        speed.add_updater(lambda mob: mob.set_value(2*flight.get_value()))
        traveled = Line([fall_x+.38,start_y,0],[fall_x+.38,start_y-.001,0],color=CYAN,stroke_width=4)
        traveled.add_updater(lambda mob: mob.put_start_and_end_on(
            [fall_x+.38,start_y,0],[fall_x+.38,min(start_y-.001,hero.get_center()[1]),0]))
        self.add(traveled)
        # Cada evento algébrico avança o MESMO tracker. Não há relógio independente.
        fall_start,fall_duration = self.score_time,15.6
        actual_fall_start = self.mapped_time(fall_start)
        actual_fall_duration = self.mapped_time(fall_start+fall_duration)-actual_fall_start
        self.qa_sync = {'fall_start_s':actual_fall_start,'fall_duration_s':actual_fall_duration,'events':[]}
        def advance(elapsed,*animations):
            alpha = (self.mapped_time(fall_start+elapsed)-actual_fall_start)/actual_fall_duration
            duration = max(1/config.frame_rate,self.mapped_time(fall_start+elapsed)-self.time)
            # A queda continua durante a leitura; só a troca de álgebra é curta.
            # A troca termina na mesma âncora da fala, sem esticar glifos por segundos.
            transitions = []
            if animations:
                span = min(.38,duration)
                transition = AnimationGroup(*animations,run_time=span)
                if duration > span:
                    transition = Succession(Wait(run_time=duration-span),transition)
                transitions.append(transition)
            self.run_to(fall_start+elapsed,flight.animate.set_value(alpha),*transitions,rate_func=linear)
            self.qa_sync['events'].append({'elapsed_s':elapsed,'alpha':flight.get_value()})
        eq_pos = [.95,3.1,0]
        eq = formula('m',r'g\Delta h','=',r'\frac12','m',r'v^2',size=45,width=4.8).move_to(eq_pos)
        advance(2.0,Write(eq))
        advance(3.2,eq[0].animate.set_color(PINK),eq[4].animate.set_color(PINK))
        cancellation = VGroup(*[Line(eq[i].get_corner(DOWN+LEFT),eq[i].get_corner(UP+RIGHT),
                                    color=PINK,stroke_width=4) for i in (0,4)])
        advance(3.8,Create(cancellation))
        advance(4.4,FadeOut(eq[0]),FadeOut(eq[4]),FadeOut(cancellation))
        reduced = formula(r'g\Delta h','=',r'\frac12',r'v^2',size=45,width=4.8).move_to(eq_pos)
        advance(5.2,TransformMatchingTex(eq,reduced))
        velocity = formula('v','=',r'\sqrt{2g\Delta h}',size=47,width=4.8).move_to(eq_pos)
        advance(6.6,TransformMatchingTex(reduced,velocity),FadeOut(rest))
        parameters = VGroup(formula(r'g=9{,}81\ \mathrm{m/s^2}',size=29),
                            formula(r'\Delta h=2000\ \mathrm m',size=29))
        parameters.arrange(DOWN,buff=.22).move_to([.95,1.55,0])
        advance(7.2,FadeIn(parameters))
        substitution = formula(r'v=\sqrt{2\cdot9{,}81\cdot2000}',size=42,width=4.8).move_to(eq_pos)
        advance(9.0,FadeOut(velocity),FadeIn(substitution))
        evaluated = formula(r'v=\sqrt{39240}',size=44,width=4.8).move_to(eq_pos)
        advance(11.6,Transform(substitution,evaluated))
        metres = formula(r'v\approx198\ \mathrm{m/s}',size=45,width=4.8).move_to(eq_pos)
        advance(13.2,Transform(substitution,metres),FadeOut(parameters))
        conversion = formula(r'198\ \mathrm{m/s}\ \xrightarrow{\times3{,}6}\ \cdots',size=37,width=4.8).move_to(eq_pos)
        advance(14.2,Transform(substitution,conversion))
        final_result = formula(r'\approx713\ \mathrm{km/h}',size=54,color=CYAN,width=4.8).move_to(eq_pos)
        # 713 na equação só é liberado quando α = 1; a mesma condição fixa a gota.
        def arrival_equation(mob):
            if flight.get_value() >= 1-1e-9:
                mob.become(final_result)
        substitution.add_updater(arrival_equation)
        advance(15.6)
        hero.update(0)
        distance.update(0)
        numeric.update(0)
        substitution.update(0)
        self.qa_sync['arrival'] = {'time_s':self.time,'alpha':flight.get_value(),
            'distance_m':HEIGHT*flight.get_value()**2,'speed_kmh':KMH_FINAL*flight.get_value(),
            'drop_y':float(hero.get_center()[1]),'expected_y':end_y}
        self.play(Indicate(numeric.number,color=CYAN,scale_factor=1.08),run_time=.4)
        self.until(42)
        substitution.clear_updaters()
        result = substitution

        # 42–55: duplicação e microqueda de 2,4 s, sem repetir a queda longa.
        hero.clear_updaters()
        traveled.clear_updaters()
        distance.clear_updaters()
        speed.clear_updaters()
        weight.clear_updaters()
        drag.clear_updaters()
        pair = ValueTracker(0)
        self.add(pair)
        numeric.value = lambda: np.floor(KMH_FINAL*pair.get_value())
        second = NumericSpeed([2,-.55,0],lambda: np.floor(KMH_FINAL*pair.get_value()),color=VIOLET,size=47.5,unit='km/h')
        numeric.caption.set_opacity(0)
        second.caption.set_opacity(0)
        large = drop(.75,VIOLET).move_to([2,3.2,0])
        d_small = formula(r'2\ \mathrm{mm}',size=32,color=CYAN).move_to([-2,4.3,0])
        d_large = formula(r'5\ \mathrm{mm}',size=32,color=VIOLET).move_to([2,4.3,0])
        rails = VGroup(*[DashedLine([x,3.2,0],[x,1.5,0],color=DIM,stroke_opacity=.35) for x in (-2,2)])
        self.show_caption('Uma queda. Duas gotas.',size=33,duration=.4)
        self.play(Transform(hero,drop(.30).move_to([-2,3.2,0])),TransformFromCopy(hero,large),
                  numeric.animate.scale(.72,about_point=numeric.anchor.get_center())
                  .shift(np.array([-2,-.55,0])-numeric.anchor.get_center()),
                  FadeIn(second),Transform(ruler,rails),FadeOut(result),FadeOut(dimension),
                  FadeOut(distance),FadeOut(traveled),FadeOut(drag),FadeIn(d_small),FadeIn(d_large),run_time=.8)
        hero.add_updater(lambda mob: mob.move_to([-2,3.2-1.7*pair.get_value()**2,0]))
        large.add_updater(lambda mob: mob.move_to([2,3.2-1.7*pair.get_value()**2,0]))
        speed.add_updater(lambda mob: mob.set_value(1.5*pair.get_value()))
        self.play(pair.animate.set_value(1),run_time=2.4,rate_func=linear)
        self.qa_sync['microfall_duration_s'] = self.mapped_time(45.6)-self.mapped_time(43.2)
        self.show_caption('Mesma queda.\nMesma velocidade.',size=35,duration=.4,
            extra=[Indicate(numeric.number,color=CYAN,scale_factor=1.08),
                   Indicate(second.number,color=VIOLET,scale_factor=1.08)])
        common = label('mesma Δh · partida do repouso',21,DIM).move_to([0,-2.4,0])
        typical = label('referência típica',21,CYAN,width=3.2).move_to([-2,-1.6,0])
        big_note = label('gota grande',21,VIOLET,width=3.2).move_to([2,-1.6,0])
        typical_source = label('2 mm · UCAR',18,DIM,width=3).move_to([-2,-3.1,0])
        self.play(FadeIn(common),FadeIn(typical),FadeIn(big_note),FadeIn(typical_source),run_time=.3)
        self.until(48.2)

        # Segunda virada e diâmetros já começam enquanto a comparação permanece.
        hero.clear_updaters()
        large.clear_updaters()
        speed.clear_updaters()
        speed.set_value(.6)
        self.show_caption('Então tamanho não importa?',size=33,duration=.4)
        self.until(49.5)
        diameters = VGroup()
        for obj,color in ((hero,CYAN),(large,VIOLET)):
            line = VGroup(Line(LEFT,RIGHT,color=color,stroke_width=3),
                          Line(DOWN*.09,UP*.09,color=color,stroke_width=2),
                          Line(DOWN*.09,UP*.09,color=color,stroke_width=2))
            def update_diameter(mob,obj=obj):
                c,r = obj.get_center(),obj[1].width/2
                mob[0].put_start_and_end_on(c+LEFT*r,c+RIGHT*r)
                mob[1].move_to(c+LEFT*r)
                mob[2].move_to(c+RIGHT*r)
            line.add_updater(update_diameter)
            update_diameter(line)
            diameters.add(line.set_z_index(8))
        assumptions = label('Aproximadamente esféricas · mesma densidade',20,DIM).move_to([0,4.25,0])
        masses = VGroup(formula(r'\approx4{,}19\ \mathrm{mg}',size=29,color=CYAN).move_to([-2,.35,0]),
                        formula(r'\approx65{,}4\ \mathrm{mg}',size=29,color=VIOLET).move_to([2,.35,0]))
        self.play(Create(diameters),d_small.animate.move_to([-2,2.7,0]),d_large.animate.move_to([2,2.7,0]),
                  FadeOut(ruler),FadeOut(common),FadeOut(typical),FadeOut(big_note),FadeOut(typical_source),FadeIn(assumptions),run_time=.6)
        mass = formula(r'm\propto d^3',size=47,color=CYAN).move_to([0,3.35,0])
        self.until(52)
        self.play(Write(mass),run_time=.7)
        self.play(FadeIn(masses[0]),run_time=.4)
        self.play(FadeIn(masses[1]),run_time=.4)
        self.play(Indicate(diameters,color=WHITE,scale_factor=1.03),run_time=.6)
        self.until(54.6)
        self.show_caption('O tamanho entra pela massa.',size=32,duration=.4)
        energy = formula('E','=',r'mg\Delta h',size=42).move_to([0,-2.8,0])
        fixed = label('g e Δh são os mesmos',22,DIM).move_to([0,-3.7,0])
        self.play(Write(energy),run_time=.7)
        self.play(FadeIn(fixed),run_time=.4)
        self.play(Indicate(energy[2],color=CYAN,scale_factor=1.05),run_time=.5)
        self.until(57.5)
        cubic_energy = formula(r'E\propto d^3',size=48,color=VIOLET).move_to(energy)
        self.play(FadeOut(energy),FadeIn(cubic_energy),run_time=.6)
        self.play(Indicate(mass,color=CYAN,scale_factor=1.08),Indicate(cubic_energy,color=VIOLET,scale_factor=1.08),run_time=.6)
        self.show_caption('Na mesma queda,\na energia também cresce com o cubo.',size=30,duration=.4)
        self.until(60)

        # 60–68: barras sob as gotas; zero comum e razão cúbica exata.
        self.show_caption('Mesma velocidade.\nEnergias diferentes.',size=33,duration=.4)
        self.play(hero.animate.move_to([-2,2.9,0]),large.animate.move_to([2,2.9,0]),
                  d_small.animate.move_to([-2,4,0]),d_large.animate.move_to([2,4,0]),
                  numeric.animate.shift(UP*2.15),second.animate.shift(UP*2.15),
                  FadeOut(mass),FadeOut(cubic_energy),FadeOut(fixed),FadeOut(masses),FadeOut(assumptions),run_time=.6)
        baseline,full_height = -2.2,2.5
        zero = Line([-3.15,baseline,0],[3.15,baseline,0],color=DIM,stroke_width=2)
        bars,joules,connectors = VGroup(),VGroup(),VGroup()
        for x,h,color,text in ((-2,full_height/ENERGY_RATIO,CYAN,r'\approx0{,}082\ \mathrm J'),
                                (2,full_height,VIOLET,r'\approx1{,}28\ \mathrm J')):
            bars.add(Rectangle(width=.58,height=h,stroke_width=0,fill_color=color,fill_opacity=.95)
                     .move_to([x,baseline+h/2,0]))
            joules.add(formula(text,size=31,color=color).move_to([x,-2.75,0]))
            connectors.add(DashedLine([x,.65,0],[x,baseline+h,0],color=color,stroke_opacity=.35,stroke_width=2))
        bar_caption = label('Energia · mesma escala',21,DIM,width=3.4).move_to([0,.55,0])
        self.play(Create(zero),FadeIn(bar_caption),Create(connectors),run_time=.4)
        self.play(GrowFromEdge(bars[0],DOWN),FadeIn(joules[0]),run_time=.5)
        self.play(GrowFromEdge(bars[1],DOWN),FadeIn(joules[1]),run_time=1.2,rate_func=linear)
        self.until(63.5)
        ratio = formula(r'\left(\frac52\right)^3=15{,}625',size=36).move_to([0,-3.65,0])
        ratio_words = label('15,625× a energia',28,VIOLET).move_to([0,-4.45,0])
        self.play(Write(ratio),run_time=.7)
        self.play(FadeIn(ratio_words),run_time=.5)
        self.until(66.5)
        self.show_caption('Mesma velocidade não significa\na mesma energia.',size=30,duration=.4)
        self.play(Indicate(joules[0],color=CYAN,scale_factor=1.08),
                  Indicate(joules[1],color=VIOLET,scale_factor=1.08),run_time=.5)
        self.until(68)

        # Daqui em diante, os tempos são diretamente os do WAV de 129,6 s.
        self.timing_map = None
        self.score_time = self.time
        for obj in diameters:
            obj.clear_updaters()
        self.clear_caption()
        research_hud = VGroup(formula(r'\approx198\ \mathrm{m/s}',size=53,color=CYAN),
                             label('713 km/h · modelo sem arrasto',22,CYAN))
        research_hud.arrange(DOWN,buff=.16).move_to([0,3.65,0])
        trail.clear_updaters()
        self.play(FadeIn(research_hud,shift=UP*.25),FadeOut(hero),FadeOut(large),FadeOut(trail),
                  FadeOut(numeric),FadeOut(second),FadeOut(d_small),FadeOut(d_large),
                  FadeOut(diameters),FadeOut(zero),FadeOut(bars),FadeOut(joules),
                  FadeOut(connectors),FadeOut(bar_caption),FadeOut(ratio),FadeOut(ratio_words),
                  intensity.animate.set_value(.12),run_time=.6)
        self.until(self.anchors['relative'])
        self.clear_caption()
        relative_label = label('água em relação à superfície',26,CYAN).move_to([0,2.1,0])
        relative_surface = Line([2.2,1.1,0],[2.2,-1.1,0],color=DIM,stroke_width=5)
        relative_drop = VGroup(*[drop(.14).move_to([-2.5+i*1.45,0,0]) for i in range(3)])
        relative_arrow = Arrow([-2.2,-.8,0],[1.9,-.8,0],buff=0,color=CYAN)
        self.play(FadeIn(relative_label),Create(relative_surface),FadeIn(relative_drop),
                  GrowFromEdge(relative_arrow,LEFT),run_time=.5)
        relative_start = elapsed.get_value()
        def flow_relative(group):
            for i,obj in enumerate(group):
                u = ((elapsed.get_value()-relative_start)/1.45+i/3)%1
                obj.move_to([-2.5+4.45*u,0,0])
                obj.set_opacity(min(1,u/.10,(1-u)/.10))
        relative_drop.add_updater(flow_relative)
        self.until(self.anchors['applications'])
        self.clear_caption()
        relative_drop.clear_updaters()
        self.play(FadeOut(relative_label),FadeOut(relative_surface),FadeOut(relative_drop),
                  FadeOut(relative_arrow),run_time=.3)

        # Escala linear comum; 198 é uma referência de velocidade, não de dano.
        sx = lambda velocity: -3.5+7*velocity/400
        axis = VGroup(Line([-3.5,0,0],[3.5,0,0],color=DIM,stroke_width=2))
        for v in (0,100,200,300,400):
            axis.add(Line([sx(v),-.09,0],[sx(v),.09,0],color=DIM,stroke_width=2))
            axis.add(label(str(v),18,DIM,width=.8).move_to([sx(v),-.38,0]))
        axis_unit = label('velocidade relativa de impacto · m/s',19,DIM).move_to([0,-.78,0])
        marker = VGroup(DashedLine([sx(198),2.95,0],[sx(198),-3.65,0],
                                   color=CYAN,stroke_opacity=.50,stroke_width=2),
                        Dot([sx(198),0,0],radius=.075,color=CYAN))
        def band(lo,hi,y,color):
            return Rectangle(width=sx(hi)-sx(lo),height=.24,stroke_width=0,
                             fill_color=color,fill_opacity=.8).move_to([(sx(lo)+sx(hi))/2,y,0])
        def rotor(center,color,fan=False):
            hub = Circle(radius=.11,color=color,fill_color=color,fill_opacity=1)
            blades = VGroup(*[Polygon([.08,0,0],[.58,.12,0],[.24,.23,0],
                              color=color,fill_color=color,fill_opacity=.6,stroke_width=1.5)
                              .rotate(i*2*PI/(5 if fan else 3),about_point=np.zeros(3))
                              for i in range(5 if fan else 3)])
            result = VGroup(hub,blades)
            if fan:
                result.add(Circle(radius=.65,color=color,stroke_width=2))
            else:
                result.add(Line([0,-.15,0],[0,-.85,0],color=color,stroke_width=3))
            result.blades, result.hub = blades, hub
            return result.scale(.6).move_to(center)
        wind_rotor,fan_rotor = rotor([3.15,2.62,0],VIOLET),rotor([3.15,-1.4,0],PINK,fan=True)
        wind = VGroup(label('Pás de turbinas eólicas',27,width=5.6).move_to([-.35,2.65,0]),
                      label('70–150 m/s · gotas 0,5–5 mm',24,VIOLET).move_to([0,2.03,0]),
                      band(70,150,1.35,VIOLET),wind_rotor,
                      label('Ibrahim & Medraj · Materials, 2020 · tab. 1',18,DIM).move_to([0,.77,0]))
        fan = VGroup(label('Pás de motores aeronáuticos',26,width=5.7).move_to([-.3,-1.45,0]),
                     label('200–400 m/s · gotas 1–5 mm',24,PINK).move_to([0,-2.1,0]),
                     band(200,400,-2.75,PINK),fan_rotor,
                     label('Ibrahim & Medraj · Materials, 2020 · tab. 1',18,DIM).move_to([0,-3.35,0]))
        self.play(Create(axis),FadeIn(axis_unit),Create(marker),FadeIn(wind),run_time=.6)
        wind_rotor.blades.add_updater(lambda mob,dt: mob.rotate(-dt*2.0,about_point=wind_rotor.hub.get_center()))
        self.until(67.6)
        self.play(FadeIn(fan),run_time=.6)
        fan_rotor.blades.add_updater(lambda mob,dt: mob.rotate(-dt*2.8,about_point=fan_rotor.hub.get_center()))
        self.until(self.anchors['titanium'])
        self.clear_caption()
        wind_rotor.clear_updaters()
        fan_rotor.clear_updaters()
        self.play(FadeOut(wind),FadeOut(fan),run_time=.3)
        titanium = VGroup(label('Ti–6Al–4V · exposição repetida',26,width=6.9).move_to([0,2.65,0]),
                          label('Testes: 150–350 m/s',24,VIOLET).move_to([0,2.04,0]),
                          band(150,350,1.35,VIOLET),
                          label('Gujba et al. · Wear, 2016',18,DIM).move_to([0,.77,0]))
        threshold = VGroup(label('Limiar naquele experimento',25,width=6.8).move_to([0,-1.45,0]),
                           formula(r'150\leq V_{\rm limiar}<200\ \mathrm{m/s}',size=30,color=PINK).move_to([0,-2.1,0]),
                           band(150,200,-2.75,PINK),
                           label('Vale para esse material e essas condições',20,DIM).move_to([0,-3.35,0]))
        self.play(FadeIn(titanium),run_time=.5)
        self.until(self.anchors['threshold'])
        self.play(FadeIn(threshold),run_time=.5)
        surface = Line([-2,-4.55,0],[2,-4.55,0],color=DIM,stroke_width=5)
        impacts = VGroup(*[drop(.055).move_to([x,-3.9,0]) for x in (-1.3,0,1.3)])
        impacts.add_updater(lambda mob: [d.move_to([x,-3.85-((phase.get_value()*.45+i*.2)%.65),0])
                                        for i,(d,x) in enumerate(zip(mob,(-1.3,0,1.3)))])
        pits = VGroup(*[Arc(radius=.08,start_angle=PI,angle=PI,color=DIM,stroke_width=2)
                       .move_to([x,-4.59,0]) for x in (-1.3,0,1.3)])
        self.play(Create(surface),FadeIn(impacts),FadeIn(pits),run_time=.3)
        self.until(self.anchors['our_result'])
        self.play(Indicate(research_hud,color=CYAN,scale_factor=1.05),run_time=.65)
        self.until(self.anchors['nasa'])

        self.clear_caption()
        def plane():
            return VGroup(Polygon([-.65,0,0],[.6,.1,0],[.85,0,0],[.1,-.1,0],
                                  color=VIOLET,fill_color=VIOLET,fill_opacity=.5),
                          Line([0,0,0],[-.3,.4,0],color=VIOLET,stroke_width=3),
                          Line([-.5,0,0],[-.65,.25,0],color=VIOLET,stroke_width=3))
        nasa = VGroup(label('Aeronaves: capazes de >178 m/s',25,width=5.7).move_to([-.3,2.65,0]),
                      label('Testes de materiais citados: ~220 m/s',23,VIOLET).move_to([0,2.04,0]),
                      Dot([sx(178),1.35,0],radius=.08,color=VIOLET),
                      Arrow([sx(178),1.35,0],[sx(270),1.35,0],buff=.05,color=VIOLET),
                      Dot([sx(220),1.35,0],radius=.10,color=PINK),plane().scale(.65).move_to([3.15,2.65,0]),
                      label('NASA TM-82473 · 1982 · §4.7 Rain Erosion',18,DIM).move_to([0,.77,0]))
        nasa_note = label('Erosão acumulada por exposição à chuva',23,DIM).move_to([0,-1.65,0])
        self.play(FadeOut(titanium),FadeOut(threshold),FadeIn(nasa),FadeIn(nasa_note),run_time=.6)
        self.until(self.anchors['aircraft'])

        # Não atribuir 198 m/s à queda da chuva real: a aeronave se move pela chuva.
        self.clear_caption()
        moving_plane = plane().scale(1.2).move_to([-3.2,1.0,0])
        rain_drops = VGroup(*[drop(.075).move_to([x,2.5,0]) for x in (-2.8,-.8,1.2,3.0)])
        rain_drops.add_updater(lambda mob: [d.move_to([x,2.5-((phase.get_value()*.6+i*.7)%3.5),0])
                                          for i,(d,x) in enumerate(zip(mob,(-2.8,-.8,1.2,3.0)))])
        plane_arrow = Arrow([-2.7,-.1,0],[2.5,-.1,0],color=VIOLET,buff=0)
        plane_label = label('aeronave em movimento',25,VIOLET).move_to([0,-.65,0])
        rain_label = label('chuva real: queda muito mais lenta',23,CYAN).move_to([0,2.85,0])
        relative_vector = Arrow([.9,-1.4,0],[-.9,-2.6,0],color=PINK,buff=0)
        relative_note = label('água vista da aeronave',22,PINK).move_to([0,-3.3,0])
        nasa_source = label('NASA TM-82473 · §4.7 · referência documental',18,DIM).move_to([0,-4.35,0])
        self.play(FadeOut(axis),FadeOut(axis_unit),FadeOut(marker),FadeOut(nasa),FadeOut(nasa_note),
                  FadeOut(surface),FadeOut(impacts),FadeOut(pits),FadeIn(moving_plane),FadeIn(rain_drops),
                  Create(plane_arrow),FadeIn(plane_label),FadeIn(rain_label),FadeIn(nasa_source),run_time=.6)
        plane_start = elapsed.get_value()
        # Reentrada só fora do quadro: travessia contínua, sem salto visível nem espera parada.
        moving_plane.add_updater(lambda mob: mob.move_to([
            -5.6+((elapsed.get_value()-plane_start)*2.6+2.4)%11.2,1.0,0]))
        self.until(self.anchors['crossing'])
        self.until(self.anchors['relative_again'])
        self.clear_caption()
        self.play(Create(relative_vector),FadeIn(relative_note),run_time=.5)
        self.until(self.anchors['hypothesis'])
        rain_drops.clear_updaters()
        moving_plane.clear_updaters()

        self.clear_caption()
        falling_drop = drop(.22).move_to([0,2.25,0])
        fall_arrow = Arrow([-1.2,2.0,0],[-1.2,-2.0,0],color=CYAN,buff=0)
        model_surface = Line([-2.4,-2.65,0],[2.4,-2.65,0],color=DIM,stroke_width=5)
        model_note = label('sem arrasto · gota intacta por hipótese',21,DIM).move_to([0,-3.45,0])
        self.play(FadeOut(moving_plane),FadeOut(rain_drops),FadeOut(plane_arrow),FadeOut(plane_label),
                  FadeOut(rain_label),FadeOut(relative_vector),FadeOut(relative_note),FadeOut(nasa_source),
                  FadeIn(falling_drop),Create(fall_arrow),Create(model_surface),FadeIn(model_note),run_time=.6)
        self.run_to(self.anchors['compare'],falling_drop.animate.move_to([0,-2.35,0]),rate_func=lambda t:t*t)
        self.clear_caption()
        comparison = VGroup(
            plane().scale(.9).move_to([-2,1.25,0]),
            Arrow([-3,0,0],[-1,0,0],buff=0,color=VIOLET),
            label('aeronave atravessa\na chuva',23,VIOLET,width=3.45).move_to([-2,-1.2,0]),
            drop(.19).move_to([2,1.25,0]),
            Arrow([2,.65,0],[2,-.4,0],buff=0,color=CYAN),
            label('gota cai\nsem arrasto',23,CYAN,width=3.45).move_to([2,-1.2,0]),
            Line([0,2.25,0],[0,-2.1,0],color=DIM,stroke_opacity=.4),
            label('Comparação de velocidade, não de dano',23,DIM).move_to([0,-3.15,0]))
        self.play(FadeOut(falling_drop),FadeOut(fall_arrow),FadeOut(model_surface),FadeOut(model_note),
                  FadeIn(comparison),run_time=.6)
        compare_start = elapsed.get_value()
        def compare_plane(mob):
            u = ((elapsed.get_value()-compare_start)/1.6)%1
            mob.move_to([-3.5+2.75*u,1.25,0]).set_opacity(min(1,u/.12,(1-u)/.12))
        def compare_drop(mob):
            u = ((elapsed.get_value()-compare_start)/1.6)%1
            mob.move_to([2,2.1-2.25*u*u,0]).set_opacity(min(1,u/.12,(1-u)/.12))
        comparison[0].add_updater(compare_plane)
        comparison[3].add_updater(compare_drop)
        self.until(self.anchors['caveat'])
        comparison.clear_updaters()

        self.show_caption('Energia cinética ≠ dano.',size=33,duration=.4)
        caveat = label('impactos repetidos ≠ uma única gota',26,PINK,width=7.3).move_to([0,-2.6,0])
        conditions = label('o dano depende do material e das condições',21,DIM,width=7.3).move_to([0,-3.3,0])
        self.play(FadeOut(comparison),FadeIn(axis),FadeIn(axis_unit),FadeIn(marker),FadeIn(nasa),
                  FadeIn(surface),FadeIn(impacts),FadeIn(pits),FadeIn(caveat),FadeIn(conditions),run_time=.6)
        self.until(self.anchors['repeated'])
        self.play(Indicate(caveat,color=PINK,scale_factor=1.03),run_time=.7)
        self.until(self.anchors['evidence'])
        self.clear_caption()
        evidence_note = label('Materiais específicos · condições controladas',23,DIM).move_to([0,-1.6,0])
        self.play(FadeIn(evidence_note),run_time=.4)
        self.until(116)
        self.play(Indicate(research_hud,color=CYAN,scale_factor=1.04),run_time=.7)
        self.until(self.anchors['return'])
        impacts.clear_updaters()
        self.qa_sync['engineering_marker_ms'] = 198
        self.qa_sync['engineering_top_caption'] = 'Energia cinética ≠ dano; demais frases redundantes removidas'
        self.qa_sync['motion'] = {'relative_stream_period_s':1.45,'aircraft_speed_scene_units_s':2.6,'aircraft_wrap_outside_frame':True,'comparison_period_s':1.6,'algebra_transition_max_s':.38}
        self.qa_sync['rigor_interval_s'] = [self.anchors['caveat'],self.anchors['return']]

        # 120,17–127,76 s do WAV: chuva real, contraste e conclusão sobre a atmosfera.
        self.clear_caption()
        real_time.set_value(0)
        speed.set_value(0)
        force_scale.set_value(1)
        drag_factor.set_value(1)
        hero.become(drop().move_to([-1.9,2.65,0]))
        self.play(FadeOut(research_hud),FadeOut(axis),FadeOut(axis_unit),FadeOut(marker),
                  FadeOut(nasa),FadeOut(surface),FadeOut(impacts),FadeOut(pits),
                  FadeOut(caveat),FadeOut(conditions),FadeOut(evidence_note),FadeIn(hero),FadeIn(trail),intensity.animate.set_value(.75),
                  FadeIn(dial),run_time=.4)
        trail.add_updater(trail_update)
        weight.add_updater(weight_update)
        drag.add_updater(drag_update)
        weight_update(weight)
        drag_update(drag)
        drag_name = label('arrasto',24,PINK).move_to([-.65,3.5,0])
        weight_name.move_to([-3,.55,0])
        speed.add_updater(lambda mob: mob.set_value(np.tanh(real_time.get_value())))
        hero.add_updater(lambda mob: mob.move_to(
            [-1.9,2.65-.32*np.log(np.cosh(real_time.get_value())),0]))
        contrast = VGroup(label('MUNDO REAL',22,CYAN).move_to([-2,-1.75,0]),
                          label('0,5–5 mm · ~2–9 m/s',20,width=3.5).move_to([-2,-2.35,0]),
                          label('UCAR / MetEd',17,DIM).move_to([-2,-2.85,0]),
                          label('SEM ARRASTO · 2 km',21,VIOLET,width=3.7).move_to([2,-1.75,0]),
                          label('~198 m/s · 713 km/h',21,VIOLET,width=3.5).move_to([2,-2.35,0]),
                          label('2 mm · referência típica (UCAR)',20,DIM).move_to([0,-3.65,0]))
        self.play(FadeIn(weight),FadeIn(drag),FadeIn(drag_name),FadeIn(weight_name),FadeIn(contrast),
                  real_time.animate.set_value(.2),run_time=.4,rate_func=linear)
        self.run_to(122.5,real_time.animate.set_value(1.3))
        self.clear_caption(extra=[real_time.animate.set_value(1.6)])
        self.run_to(self.anchors['payoff'],real_time.animate.set_value(3.2))
        self.clear_caption(extra=[real_time.animate.set_value(3.5)])
        self.run_to(self.anchors['cta']-.25,real_time.animate.set_value(4.2))

        # 127,76–129,60 s do WAV: CTA, chuva discreta e asset oficial existente.
        hero.clear_updaters()
        weight.clear_updaters()
        drag.clear_updaters()
        logo = ImageMobject(str(WATERMARK_PATH)).set_width(4.4).set_opacity(.95).move_to([0,1.5,0])
        handle = label('@labparallax',34).set_color_by_gradient(CYAN,VIOLET,PINK)
        handle.move_to([0,.35,0])
        caption_fades = [FadeOut(self.caption)] if self.caption is not None else []
        self.play(*caption_fades,FadeOut(dial),FadeOut(weight),FadeOut(drag),FadeOut(weight_name),FadeOut(drag_name),
                  FadeOut(contrast),intensity.animate.set_value(.4),
                  hero.animate.scale(.45).move_to([-3.5,-.8,0]).set_opacity(.35),
                  FadeIn(logo),FadeIn(handle),run_time=.8)
        hero.add_updater(lambda mob,dt: mob.shift(DOWN*dt*.65))
        self.until(self.sync['audio_duration_s'])
        self.qa_sync['total_duration_s'] = self.time
        Path(config.media_dir, 'qa_sync.json').write_text(json.dumps(self.qa_sync,indent=2),encoding='utf-8')

    def clear_caption(self, duration=.18, extra=None):
        animations = list(extra or [])
        if self.caption is not None:
            animations.append(FadeOut(self.caption))
            self.caption = None
        if animations:
            self.play(*animations,run_time=duration)

    def show_caption(self, content, size=35, duration=.6, extra=None):
        target = label(content,size,width=7.4).move_to([0,5.35,0]).set_z_index(15)
        animations = list(extra or [])
        if self.caption is None:
            animations.append(FadeIn(target,shift=UP*.1))
        else:
            # Frases diferentes não devem se deformar em letras sem significado.
            animations.append(Succession(FadeOut(self.caption),FadeIn(target)))
        self.play(*animations,run_time=duration)
        self.caption = target
    def until(self, target):
        remaining = target-self.score_time
        if remaining < -1/config.frame_rate:
            raise RuntimeError(f'Âncora {target}s excedida: {self.time:.3f}s')
        if remaining > 1/(2*config.frame_rate):
            self.wait(remaining)
    def run_to(self, target, *animations, rate_func=linear):
        duration = target-self.score_time
        if duration <= 0:
            raise RuntimeError(f'Sem tempo até {target}s: {self.time:.3f}s')
        self.play(*animations,run_time=duration,rate_func=rate_func)

    def mapped_time(self, score):
        if self.timing_map is None:
            return float(score)
        return float(np.interp(score,self.timing_map[:,0],self.timing_map[:,1]))

    def play(self, *animations, **kwargs):
        score_duration = kwargs.get('run_time',max((getattr(a,'run_time',1.0) for a in animations),default=1.0))
        target_score = self.score_time + score_duration
        target_frame = round(self.mapped_time(target_score)*config.frame_rate)
        kwargs['run_time'] = max(1/config.frame_rate,target_frame/config.frame_rate-self.time)
        result = super().play(*animations,**kwargs)
        self.score_time = target_score
        return result

    def wait(self, duration=1, **kwargs):
        return self.play(Wait(run_time=duration),**kwargs)

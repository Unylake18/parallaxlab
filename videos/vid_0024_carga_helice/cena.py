"""VID24 — layout, legibilidade e ritmo; preview silencioso Manim 2.5D.
Previews anteriores preservados. Novo render em media_layout_ritmo/.
"""
from pathlib import Path
import json
import sys
import numpy as np
from manim import *
from MF_Tools import TransformByGlyphMap

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from template.config import BACKGROUND_COLOR, PRIMARY_COLOR, TEXT_COLOR, WATERMARK_PATH
from template.fonts import screen_text

UNIT = Path(__file__).resolve().parent
config.media_dir = str(UNIT / 'media_layout_ritmo')
config.background_color = BACKGROUND_COLOR
config.max_files_cached = 240
CYAN, VIOLET, PINK, BLUE, DIM = PRIMARY_COLOR, '#9C8CFF', '#EA63FF', '#267BFF', '#8492AE'
PARALLEL = '#63E6BE'  # Escolha específica desta rodada para a componente paralela.
LAYOUT = {
    'title': 6.1, 'subtitle': 5.25, 'equation': -4.8, 'note': -5.65,
    'algebra': -4.5, 'reference': (-2.0, -3.15, 0), 'legend': 4.05, 'badge': 4.45,
    'geometry_scale': .92, 'geometry_lift': .70,
    'graph_scale': .68, 'graph_lift': 1.75,
    'graph_center': -3.45, 'graph_height': 4.15,
    'measure_rows': (-3.25, -3.90), 'captions_top': -6.25,
}


def state(phi, B=1., vp=1.15, vz=.34, sign=1, common_initial=False):
    """m=|q|=1; phi=omega*t. Na comparação q, r0=0 e v0=(0,-vp,vz).

    Mudar somente q desloca o centro para (-sign*r,0,0), sem alterar v0.
    A vista principal conserva o centro na origem para raio e projeções.
    """
    r = vp/B
    if common_initial:
        p = np.array([sign*r*(np.cos(phi)-1), -r*np.sin(phi), vz*phi/B])
        vt = vp*np.array([-sign*np.sin(phi), -np.cos(phi), 0.])
    else:
        p = np.array([r*np.cos(phi), -sign*r*np.sin(phi), vz*phi/B])
        vt = vp*np.array([-np.sin(phi), -sign*np.cos(phi), 0.])
    vl = np.array([0., 0., vz])
    v = vt+vl
    force = sign*np.cross(v, [0.,0.,B])
    return p, vt, vl, v, force


def graph_components(t_over_T, B=1., vp=1.15, vz=.34, sign=1, common_initial=False):
    """Mesma física da partícula; abscissa t/T, nunca tempo editorial."""
    physical = state(TAU*t_over_T, B, vp, vz, sign, common_initial)
    return physical[3][0], physical[4][0]


def words(content, y, size=28, color=TEXT_COLOR, x=0):
    pw, ph = config.pixel_width, config.pixel_height
    try:
        config.pixel_width = config.pixel_height = 4000
        mob = screen_text(content, size, color=color, oversample=2)
    finally:
        config.pixel_width, config.pixel_height = pw, ph
    if mob.width > 7.5:
        mob.scale_to_fit_width(7.5)
    return mob.move_to([x,y,0]).set_z_index(40)


def math(*parts, y=LAYOUT['equation'], size=43, color=TEXT_COLOR):
    mob = MathTex(*parts, font_size=size, color=color)
    palette = {r'\vec v_\parallel':PARALLEL, r'\vec v_\perp':VIOLET,
               r'v_\parallel':PARALLEL, r'|v_\parallel|':PARALLEL, r'v_\perp':VIOLET,
               r'\vec F':PINK, r'\vec B':BLUE, 'B':BLUE, 'v_x':VIOLET, 'F_x':PINK}
    for token, ink in palette.items():
        mob.set_color_by_tex(token, ink, substring=False)
    for sub, part in zip(mob, parts):
        if part == r'\frac{2\pi m|v_\parallel|}{|q|B}':
            assert len(sub) == 12, len(sub)
            VGroup(*sub[3:7]).set_color(PARALLEL)
            sub[11].set_color(BLUE)
    if mob.width > 7.45:
        mob.scale_to_fit_width(7.45)
    return mob.move_to([0,y,0]).set_z_index(40)


class CargaHelice024(Scene):
    def mark(self, name):
        self.events.append({'estado':name,'segundos':round(self.time,3)})
        print(f'ESTADO {name}: {self.time:.3f}s')

    def until(self, t):
        if self.time > t+.15:
            raise RuntimeError(f'Bloco excedeu {t}s: {self.time:.3f}s')
        if t-self.time > .02:
            self.wait(t-self.time)

    def heading(self,title,sub=None,carry=False,plane=None):
        new=title if isinstance(title,Mobject) else words(title,LAYOUT['title'],33)
        newsub=words(sub,LAYOUT['subtitle'],22,DIM) if sub else VGroup()
        outgoing=[FadeOut(self.title,shift=UP*.08),FadeOut(self.subtitle)]
        if not carry:
            outgoing.extend([FadeOut(self.eq),FadeOut(self.note)])
        incoming=[FadeIn(new,shift=UP*.08),FadeIn(newsub)]
        if plane is not None: incoming.append(self.plane_alpha.animate.set_value(plane))
        self.play(Succession(AnimationGroup(*outgoing),AnimationGroup(*incoming)),run_time=.8)
        self.title,self.subtitle=new,newsub
        if not carry: self.eq,self.note=VGroup(),VGroup()

    def equation(self, *parts, note=None, matching=False, duration=.9):
        new = math(*parts)
        newnote = words(note,LAYOUT['note'],23,DIM) if note else VGroup()
        change = TransformMatchingTex(self.eq,new) if matching else Succession(FadeOut(self.eq),FadeIn(new))
        self.play(change,Succession(FadeOut(self.note),FadeIn(newnote)),run_time=duration)
        self.eq,self.note = new,newnote
        return new

    def consequence(self,component,label,note):
        new=VGroup(math(component,r'\Rightarrow',y=0),words(label,0,30))
        new.arrange(RIGHT,buff=.18).move_to([0,LAYOUT['equation'],0])
        newnote=words(note,LAYOUT['note'],23,DIM)
        self.play(Succession(FadeOut(self.eq),FadeIn(new)),
                  Succession(FadeOut(self.note),FadeIn(newnote)),run_time=.6)
        self.eq,self.note=new,newnote

    def project(self, xyz):
        x,y,z = xyz
        f = self.front.get_value()
        # No limite frontal, +x para a direita, +y para cima: +B sai da tela.
        p = np.array([(1.3+.4*f)*x+.30*(1-f)*z-.75+.75*f,
                      (.68+1.02*f)*y+.90*(1-f)*z-2.65+2.2*f, 0.])
        return self.view_scale.get_value()*p+UP*self.view_lift.get_value()

    def physical(self, phi=None):
        return state(self.phase_tracker.get_value() if phi is None else phi,
                     self.B_tracker.get_value(),self.v_perp_tracker.get_value(),
                     self.v_parallel_tracker.get_value(),self.charge_sign,self.common_initial)

    def orbit_center(self):
        r = self.v_perp_tracker.get_value()/self.B_tracker.get_value()
        return np.array([-self.charge_sign*r if self.common_initial else 0.,0.,0.])

    def curve(self, end=4*PI, circle=False, parameters=None):
        points=[]
        for phi in np.linspace(0,max(end,.001),161):
            p = self.physical(phi)[0] if parameters is None else state(phi,*parameters)[0]
            if circle:
                p[2]=0
            points.append(self.project(p))
        return VMobject(color=VIOLET if circle else CYAN,stroke_width=3.5 if circle else 4.2,
                        fill_opacity=0).set_points_as_corners(points)

    def environment(self):
        # Dez vetores fixos em três profundidades. Brilho não representa fluxo.
        locations=[(-1.8,1.4,.6,5.1,.30),(0,1.4,1.5,5.3,.30),(1.8,1.4,.3,4.9,.30),
                   (-1.8,0,-.2,3.7,.40),(0,0,1.1,5.2,.40),(1.8,0,.3,4.6,.40),
                   (-1.8,-1.4,.1,4.6,.53),(-.6,-1.4,1.2,5.1,.53),
                   (.6,-1.4,-.2,3.8,.53),(1.8,-1.4,.7,5.2,.53)]
        field=VGroup(*[Arrow(ORIGIN,UP,buff=0,color=BLUE,stroke_width=2,
                             max_tip_length_to_length_ratio=.065) for _ in locations]).set_z_index(-4)
        glows=VGroup(*[Line(ORIGIN,UP,color=BLUE,stroke_width=7) for _ in locations]).set_z_index(-5)
        btag=math(r'\vec B',size=32,color=BLUE)
        axis=Line(ORIGIN,UP,color=DIM,stroke_width=1.2)
        plane=Polygon(LEFT,UP,RIGHT,DOWN,color=VIOLET,stroke_width=1.2).set_z_index(-9)
        env=VGroup(plane,glows,field,axis,btag)
        def refresh(g):
            alpha=self.field_alpha.get_value(); strength=self.B_tracker.get_value()
            for arrow,glow,(x,y,z0,z1,depth) in zip(field,glows,locations):
                z1=z0+4.0  # Campo uniforme: mesma extensão, luminosidade indica profundidade.
                a,b=self.project([x,y,z0]),self.project([x,y,z1])
                if np.linalg.norm(b-a)<.001: b=a+UP*.001
                arrow.put_start_and_end_on(a,b); glow.put_start_and_end_on(a,b)
                arrow.set_stroke(width=1.9+1.3*(strength-1),opacity=alpha*min(.82,depth*(1+.65*(strength-1))))
                arrow.get_tip().set_opacity(alpha*min(.9,depth+.22))
                glow.set_stroke(width=6.5+2*(strength-1),opacity=alpha*depth*.13*(1+.5*(strength-1)))
            label_lift=max(0.,3.4*(self.v_perp_tracker.get_value()-1.15))
            btag.move_to(self.project([1.8,0,5.6])+LEFT*.25+UP*label_lift).set_opacity(alpha)
            center=self.orbit_center(); a,b=self.project(center+[0,0,-.25]),self.project(center+[0,0,5.6])
            if np.linalg.norm(b-a)<.001: b=a+UP*.001
            axis.put_start_and_end_on(a,b); axis.set_stroke(opacity=.30*alpha*self.axis_alpha.get_value())
            plane.become(Polygon(*[self.project([x,y,0]) for x,y in
                                  [(-1.65,-1.65),(1.65,-1.65),(1.65,1.65),(-1.65,1.65)]],
                                  fill_color=VIOLET,fill_opacity=.045*self.plane_alpha.get_value(),stroke_color=VIOLET,
                                  stroke_width=1.3,stroke_opacity=.29*self.plane_alpha.get_value()).set_z_index(-9))
        env.field,env.glows,env.plane,env.axis,env.btag=field,glows,plane,axis,btag
        env.add_updater(refresh); refresh(env)
        return env

    def sync_particle(self):
        p=self.project(self.physical()[0])
        self.particle.move_to(p); self.halo.move_to(p)

    def reset_run(self,vp=1.15,vz=.34,sign=1,common=False,phase=0,show=True):
        # Nova condição: o palco e a geometria permanecem, a carga reaparece na entrada.
        old=self.path[1].copy().clear_updaters() if self.path in self.mobjects else self.curve(4*PI)
        visible=[m for m in (self.particle,self.halo) if m in self.mobjects]
        if visible: self.play(*[FadeOut(m) for m in visible],self.axis_alpha.animate.set_value(0),run_time=.4)
        self.remove(self.path)
        if self.reference is not None: self.remove(self.reference)
        self.add(old)
        self.B_tracker.set_value(1); self.v_perp_tracker.set_value(vp); self.v_parallel_tracker.set_value(vz)
        self.charge_sign=sign; self.common_initial=common
        self.phase_tracker.set_value(phase); self.reveal.set_value(phase); self.path_alpha.set_value(1)
        self.sync_particle()
        span=TAU if vz==0 else 4*PI
        target=self.curve(span).set_stroke(opacity=.24,width=2).set_fill(opacity=0).set_z_index(-6)
        self.reference=old
        if show:
            self.add(self.path)
            self.play(Transform(old,target),FadeIn(self.halo),FadeIn(self.particle),self.axis_alpha.animate.set_value(1),run_time=.7)
        else: self.play(Transform(old,target),self.axis_alpha.animate.set_value(1),run_time=.7)
        old.set_z_index(-6)

    def vector(self, kind, color, label, offset):
        arrow=Arrow(ORIGIN,RIGHT,buff=0,color=color,stroke_width=5.2)
        tag=math(label,size=31,color=color)
        group=VGroup(arrow,tag).set_z_index(22)
        tag.set_z_index(42)
        def refresh(g):
            p,vt,vl,v,f=self.physical()
            origin=p.copy()
            scale=self.velocity_scale.get_value()
            if kind=='perp': origin+=scale*vl
            direction={'v':v,'perp':vt,'parallel':vl,'F':f}[kind]
            end=origin+(1.25 if kind=='F' else scale)*direction
            a,b=self.project(origin),self.project(end)
            if np.linalg.norm(b-a)<.001: b=a+RIGHT*.001
            g[0].become(Arrow(a,b,buff=0,color=color,stroke_width=5.2,
                              max_tip_length_to_length_ratio=.12 if kind=='v' else .2))
            g[1].move_to(b+np.array(offset))
        group.add_updater(refresh); refresh(group)
        return group

    def turn(self, end, duration, reveal=True):
        animations=[self.phase_tracker.animate.set_value(end)]
        if reveal: animations.append(self.reveal.animate.set_value(end))
        self.play(*animations,run_time=duration,rate_func=linear)

    def graphs(self):
        panels=VGroup()
        axes=[]
        curves=[]
        for row,(label,color) in enumerate([('v_x',VIOLET),('F_x',PINK)]):
            y=-2.55-row*1.55
            ax=Axes(x_range=[0,2,1],y_range=[-1.2,1.2,1],x_length=5.7,y_length=1.1,
                    tips=False,axis_config={'include_ticks':False,'color':DIM,'stroke_width':1.1})
            ax.move_to([.2,y,0]); axes.append(ax)
            curve=VMobject(color=color,stroke_width=2.8)
            curve.set_points_as_corners([ax.c2p(t,graph_components(t)[row]/(1.15 if row==0 else 1.15))
                                         for t in np.linspace(0,2,161)])
            tag=math(label+'(t)',y=y,size=31,color=color).set_x(-3.4)
            zero=math('0',y=y-.73,size=20,color=DIM).set_x(ax.c2p(0,0)[0])
            panels.add(ax,curve,tag,zero)
            curves.append(curve)
        ticks=VGroup(*[math(str(n),y=-5.1,size=22,color=DIM).set_x(axes[1].c2p(n,0)[0]) for n in (1,2)])
        time=math(r't/T',y=-5.1,size=27,color=DIM).set_x(3.45)
        cursor=always_redraw(lambda: Line(axes[1].c2p(self.phase_tracker.get_value()/TAU,-1.2),
                                         axes[0].c2p(self.phase_tracker.get_value()/TAU,1.2),
                                         color=TEXT_COLOR,stroke_width=1.1,stroke_opacity=.55))
        dots=VGroup(*[Dot(radius=.055,color=color) for color in (VIOLET,PINK)])
        def refresh_dots(g):
            t=self.phase_tracker.get_value()/TAU
            vx,fx=graph_components(t,self.B_tracker.get_value(),self.v_perp_tracker.get_value(),
                                   self.v_parallel_tracker.get_value(),self.charge_sign,self.common_initial)
            g[0].move_to(axes[0].c2p(t,vx/self.v_perp_tracker.get_value()))
            g[1].move_to(axes[1].c2p(t,fx/(self.B_tracker.get_value()*self.v_perp_tracker.get_value())))
        dots.add_updater(refresh_dots); refresh_dots(dots)
        modules=words('As componentes oscilam; os módulos permanecem constantes.',-1.8,22,DIM)
        constant_B=math('B','=','B_0',y=4.15,size=29,color=BLUE).set_x(2.75)
        border=RoundedRectangle(width=7.9,height=LAYOUT['graph_height'],corner_radius=.12,
                                stroke_color=DIM,stroke_width=1,stroke_opacity=.22,
                                fill_color=BLUE,fill_opacity=.018).move_to([0,LAYOUT['graph_center'],0]).set_z_index(-8)
        group=VGroup(border,panels,ticks,time,cursor,dots,modules,constant_B)
        group.curves=VGroup(*curves)
        return group

    def radius_pitch(self,parameters,color,suffix,shift=0,radius=True,pitch=True):
        B,vp,vz,sign,common=parameters; r,p=vp/B,TAU*abs(vz)/B
        group=VGroup()
        if radius:
            y=LAYOUT['measure_rows'][1 if shift else 0]
            a=np.array([-.4,y,0]); b=a+RIGHT*(1.3*self.view_scale.get_value()*r)
            group.add(DoubleArrow(a,b,buff=0,color=color,stroke_width=2.4,max_tip_length_to_length_ratio=.14),
                      math('r_'+suffix,size=28,color=color).move_to(a+LEFT*.65))
        if pitch:
            ink=DIM if suffix=='0' else PARALLEL
            a=np.array([-3.9+(.7 if shift else 0),-2.1,0])
            b=a+self.project([0,0,p])-self.project([0,0,0])
            group.add(DoubleArrow(a,b,buff=0,color=ink,stroke_width=2.4,max_tip_length_to_length_ratio=.1),
                      math('p_'+suffix,size=28,color=ink).move_to((a+b)/2+LEFT*.35))
        return group.set_z_index(18)

    def compare(self,variable,target,title,subtitle,formula,badge,radius,pitch,end=None):
        self.heading(title,subtitle); self.equation(*formula,duration=.8)
        baseline=(1.,1.15,.34,1,False)
        ghost=self.curve(parameters=baseline).set_stroke(color=DIM,opacity=.32,width=2).set_fill(opacity=0).set_z_index(-7)
        self.play(FadeIn(ghost),FadeOut(self.particle),FadeOut(self.halo),run_time=.4)
        self.reveal.set_value(4*PI); self.phase_tracker.set_value(3.35*PI); self.sync_particle()
        self.velocity_scale.set_value(2)
        indicator=math(badge,y=LAYOUT['badge'],size=31,color=BLUE if variable=='B' else VIOLET if variable=='vp' else PARALLEL)
        self.add(indicator)
        comp=None
        if variable!='B':
            comp=self.vector('perp' if variable=='vp' else 'parallel',VIOLET if variable=='vp' else PARALLEL,
                             r'\vec v_\perp' if variable=='vp' else r'\vec v_\parallel',
                             [-.05,.42,0] if variable=='vp' else [-.75,-.25,0])
            if variable=='vp':
                # Aqui só este componente é mostrado: sua origem fica na partícula.
                # Na decomposição, a mesma seta continua ponta com cauda.
                comp.add_updater(lambda g:g.shift(self.project([0,0,0])-
                                                  self.project(self.velocity_scale.get_value()*self.physical()[2])))
            comp.update(0)
        self.play(FadeIn(self.particle),FadeIn(self.halo),*([FadeIn(comp)] if comp is not None else []),run_time=.4)
        tracker={'B':self.B_tracker,'vp':self.v_perp_tracker,'vz':self.v_parallel_tracker}[variable]
        self.play(tracker.animate.set_value(target),run_time=1.4)
        oldmeasure=self.radius_pitch(baseline,DIM,'0',radius=radius,pitch=pitch)
        params=list(baseline);params[{'B':0,'vp':1,'vz':2}[variable]]=target
        newmeasure=self.radius_pitch(tuple(params),CYAN if variable!='vp' else VIOLET,'1',shift=.34,radius=radius,pitch=pitch)
        self.play(FadeIn(oldmeasure),FadeIn(newmeasure),run_time=.45)
        self.mark('comparacao_'+variable+'_geometria')
        self.wait(.9)
        if comp is not None: self.play(FadeOut(comp),run_time=.35)
        self.play(FadeOut(self.particle),FadeOut(self.halo),run_time=.3)
        self.phase_tracker.set_value(0);self.sync_particle()
        baseline_dot=Dot(radius=.065,color=DIM).set_z_index(20)
        baseline_dot.add_updater(lambda m: m.move_to(self.project(state(self.phase_tracker.get_value()/self.B_tracker.get_value(),*baseline)[0])))
        baseline_dot.update(0);self.add(baseline_dot)
        self.play(FadeIn(self.particle),FadeIn(self.halo),run_time=.3)
        self.turn(TAU*self.B_tracker.get_value(),2.6,reveal=False)
        self.mark('comparacao_'+variable+'_tempo_T0')
        self.play(FadeOut(ghost),FadeOut(baseline_dot),FadeOut(oldmeasure),FadeOut(newmeasure),FadeOut(indicator),run_time=.4)
        self.play(tracker.animate.set_value(baseline[{'B':0,'vp':1,'vz':2}[variable]]),
                  self.phase_tracker.animate.set_value(4*PI),run_time=.7)
        self.mark('comparacao_'+variable+'_baseline')
        self.clear_equation(.3)


    def luminous_curve(self,end,circle=False):
        core=self.curve(end,circle=circle).set_z_index(8 if not circle else 7)
        alpha=self.path_alpha.get_value() if not circle else 1
        core.set_stroke(opacity=alpha)
        glow=core.copy().set_stroke(width=10 if not circle else 8,opacity=.12*alpha).set_z_index(6)
        return VGroup(glow,core)

    def clear_equation(self,duration=.4):
        if len(self.eq) or len(self.note): self.play(FadeOut(self.eq),FadeOut(self.note),run_time=duration)
        self.eq,self.note=VGroup(),VGroup()

    def grow_vector(self,vector,duration=.65):
        vector.update(0);vector.suspend_updating()
        self.play(GrowArrow(vector[0]),FadeIn(vector[1]),run_time=duration)
        self.remove(*vector.get_family());vector.resume_updating();self.add(vector)

    def live_until(self,until,end_phase=None):
        if self.time>until+.15: raise RuntimeError(f'Marco {until} excedido: {self.time}')
        duration=until-self.time
        if duration>.02:
            self.turn(self.phase_tracker.get_value()+PI*.08*duration if end_phase is None else end_phase,duration)

    def guides(self):
        p,vt,vl,v,_=self.physical();k=self.velocity_scale.get_value()
        return VGroup(DashedLine(self.project(p),self.project(p+k*vt),color=VIOLET,stroke_width=1.1,stroke_opacity=.35,dash_length=.10),
                      DashedLine(self.project(p+k*vt),self.project(p+k*v),color=PARALLEL,stroke_width=1.1,stroke_opacity=.35,dash_length=.10)).set_z_index(12)

    def glyph_formula(self,key,size=43):
        data={
            'A':(r'|q|v_\perp B=\frac{mv_\perp^2}{r}',13,[3,4,8,10],[5]),
            'B':(r'|q|v_\perp Br=mv_\perp^2',12,[3,4,9,11],[5]),
            'C':(r'|q|v_\perp Br=mv_\perp\cdot v_\perp',14,[3,4,9,10,12,13],[5]),
            'D':(r'|q|Br=mv_\perp',9,[7,8],[3]),
            'E':(r'r=\frac{mv_\perp}{|q|B}',10,[3,4],[9]),
            'W0':(r'\omega_c=\frac{v_\perp}{r}',7,[3,4],[]),
            'W1':(r'\omega_c=\frac{v_\perp}{mv_\perp/(|q|B)}',16,[3,4,7,8],[14]),
            'W2':(r'\omega_c=\frac{|q|B}{m}',9,[],[6]),
            'T0':(r'T=\frac{2\pi}{\omega_c}',7,[],[]),
            'T1':(r'T=\frac{2\pi m}{|q|B}',10,[],[9]),
        }
        tex,count,vp,field=data[key]
        mob=math(tex,y=LAYOUT['algebra'],size=size); assert len(mob[0])==count,(key,len(mob[0]),count)
        VGroup(*[mob[0][i] for i in vp]).set_color(VIOLET)
        VGroup(*[mob[0][i] for i in field]).set_color(BLUE)
        return mob

    def glyph_show(self,key,note=None):
        new=self.glyph_formula(key);newnote=words(note,LAYOUT['note'],23,DIM) if note else VGroup()
        self.play(Succession(FadeOut(self.eq),FadeIn(new)),Succession(FadeOut(self.note),FadeIn(newnote)),run_time=.8)
        self.eq,self.note=new,newnote
        return new

    def glyph_transfer(self,target,links,duration=1.5,name='glyph',extras=()):
        source=self.eq
        animation=TransformByGlyphMap(source,target,*links,auto_fade=True,auto_morph=False,printing=False)
        assert not animation.show_indices
        self.mark(name+'_inicio')
        self.play(animation,*extras,run_time=duration)
        self.remove(*source.get_family());self.remove(*target.get_family());self.add(target);self.eq=target
        self.mark(name+'_fim')

    def radius_algebra(self):
        self.glyph_show('A',note='Força magnética = força centrípeta')
        self.turn(5.7*PI,3)
        gap=self.eq.copy();gap[0].remove(gap[0][11])
        self.glyph_transfer(gap,[(list(range(11))+[12],list(range(12))),([11],[])],.4,'raio_retirar_barra')
        self.glyph_transfer(self.glyph_formula('B'),[([0,1,2],[0,1,2]),([3,4],[3,4]),([5],[5]),([6],[7]),
                            ([7],[8]),([8,10],[9,11]),([9],[10]),([11],[6],{'path_arc':-.7})],1.5,'raio_multiplicar_r')
        self.wait(.65)
        gap=self.eq.copy();gap[0].remove(gap[0][10])
        self.glyph_transfer(gap,[(list(range(10))+[11],list(range(11))),([10],[])],.3,'raio_expoente')
        self.glyph_transfer(self.glyph_formula('C'),[([0,1,2,3,4,5,6,7,8],[0,1,2,3,4,5,6,7,8]),
                            ([9,10],[9,10]),([9,10],[12,13],{'path_arc':PI/2}),([], [11],{'delay':.3})],1.2,'raio_abrir_quadrado')
        self.wait(.35)
        factors=VGroup(*[self.eq[0][i] for i in (3,4,12,13)])
        self.play(factors.animate.set_color(TEXT_COLOR),run_time=.4)
        strikes=VGroup(*[Line(VGroup(*[self.eq[0][i] for i in pair]).get_corner(DL)+DL*.05,
                              VGroup(*[self.eq[0][i] for i in pair]).get_corner(UR)+UR*.05,
                              color=PINK,stroke_width=2.4) for pair in ((3,4),(12,13))])
        constraint=math(r'v_\perp',r'\ne0',y=LAYOUT['note'],size=29)
        self.play(Create(strikes),Succession(FadeOut(self.note),FadeIn(constraint)),run_time=.45);self.note=constraint
        self.wait(.8)
        gap=self.eq.copy();gap[0].remove(*[gap[0][i] for i in (3,4,11,12,13)])
        kept=[0,1,2,5,6,7,8,9,10]
        self.glyph_transfer(gap,[(kept,list(range(9))),([3,4,11,12,13],[])],1,'raio_cancelar_vperp',extras=(FadeOut(strikes),))
        self.wait(.35)
        self.glyph_transfer(self.glyph_formula('D'),[(list(range(9)),list(range(9)))],1,'raio_compactar')
        self.wait(.4)
        self.glyph_transfer(self.glyph_formula('E'),[([4],[0],{'path_arc':.7,'run_time':1.6}),([5],[1],{'run_time':1.6}),
                            ([6,7,8],[2,3,4],{'run_time':1.6}),([0,1,2,3],[6,7,8,9],{'path_arc':.65,'run_time':1.6}),
                            ([],[5],{'delay':1.1,'run_time':.5})],1.6,'raio_isolar_r')
        box=SurroundingRectangle(self.eq,buff=.22,color=CYAN,stroke_width=1.8,corner_radius=.12)
        self.play(Create(box),run_time=.5);self.mark('raio_resultado')
        self.live_until(78,end_phase=8*PI)
        return box

    def period_algebra(self,box):
        radius_reference=self.eq
        self.play(FadeOut(box),radius_reference.animate.scale(.78).move_to(LAYOUT['reference']),FadeOut(self.note),run_time=.7)
        self.eq,self.note=VGroup(),VGroup()
        self.phase_tracker.add_updater(lambda m,dt:m.increment_value(dt*PI*.08))
        self.glyph_show('W0',note='Giro transversal: velocidade dividida pelo raio')
        self.wait(.65)
        gap=self.eq.copy();gap[0].remove(gap[0][6])
        self.glyph_transfer(gap,[(list(range(6)),list(range(6))),([6],[])],.4,'omega_substituir_raio_saida')
        self.glyph_transfer(self.glyph_formula('W1'),[(list(range(6)),list(range(6)))],.9,'omega_substituir_raio')
        self.wait(.65)
        factors=VGroup(*[self.eq[0][i] for i in (3,4,7,8)])
        self.play(factors.animate.set_color(TEXT_COLOR),run_time=.4)
        strikes=VGroup(*[Line(VGroup(*[self.eq[0][i] for i in pair]).get_corner(DL)+DL*.04,
                              VGroup(*[self.eq[0][i] for i in pair]).get_corner(UR)+UR*.04,
                              color=PINK,stroke_width=2.3) for pair in ((3,4),(7,8))])
        self.play(Create(strikes),run_time=.4);self.wait(.7)
        gap=self.eq.copy();gap[0].remove(*[gap[0][i] for i in (3,4,7,8)])
        kept=[0,1,2,5,6,9,10,11,12,13,14,15]
        self.glyph_transfer(gap,[(kept,list(range(12))),([3,4,7,8],[])],.8,'omega_cancelar_vperp',extras=(FadeOut(strikes),))
        self.wait(.35)
        gap=self.eq.copy();gap[0].remove(*[gap[0][i] for i in (3,5,6,11)])
        self.glyph_transfer(gap,[([0,1,2,4,7,8,9,10],list(range(8))),([3,5,6,11],[])],.35,'omega_limpar_divisao')
        self.glyph_transfer(self.glyph_formula('W2'),[([0,1,2],[0,1,2],{'run_time':1.4}),([3],[8],{'path_arc':-.3,'run_time':1.4}),
                            ([4,5,6,7],[3,4,5,6],{'path_arc':.45,'run_time':1.4}),
                            ([],[7],{'delay':.95,'run_time':.45})],1.4,'omega_simplificar')
        omega_box=SurroundingRectangle(self.eq,buff=.20,color=VIOLET,stroke_width=1.6,corner_radius=.10)
        self.play(Create(omega_box),run_time=.4);self.wait(.8)
        self.play(FadeOut(radius_reference),FadeOut(omega_box),run_time=.4)
        self.omega_reference=self.eq
        self.play(self.omega_reference.animate.scale(.78).move_to(LAYOUT['reference']),run_time=.6)
        self.eq=VGroup();self.glyph_show('T0',note='Uma volta: 2π radianos')
        self.wait(.7)
        gap=self.eq.copy();gap[0].remove(*[gap[0][i] for i in (5,6)])
        self.glyph_transfer(gap,[(list(range(5)),list(range(5))),([5,6],[])],.35,'periodo_substituir_omega_saida')
        self.glyph_transfer(self.glyph_formula('T1'),[([0,1,2,3],[0,1,2,3]),([4],[5])],1.1,'periodo_substituir_omega')
        box=SurroundingRectangle(self.eq,buff=.22,color=CYAN,stroke_width=1.8,corner_radius=.12)
        self.play(Create(box),run_time=.45);self.mark('periodo_resultado')
        self.until(94);self.phase_tracker.clear_updaters()
        return box

    def construct(self):
        self.events=[];self.reference=None
        self.B_tracker=ValueTracker(1);self.v_perp_tracker=ValueTracker(0);self.v_parallel_tracker=ValueTracker(.34)
        self.phase_tracker=ValueTracker(0);self.reveal=ValueTracker(0);self.front=ValueTracker(0)
        self.view_scale=ValueTracker(LAYOUT['geometry_scale']);self.view_lift=ValueTracker(LAYOUT['geometry_lift']);self.field_alpha=ValueTracker(1)
        self.path_alpha=ValueTracker(1);self.axis_alpha=ValueTracker(1);self.velocity_scale=ValueTracker(1.25)
        self.plane_alpha=ValueTracker(0)
        self.charge_sign=1;self.common_initial=False
        self.title=words('Qual é a trajetória de uma carga\nem um campo magnético?',6.0,31)
        self.subtitle=words('campo uniforme e constante',5.05,23,DIM)
        self.eq,self.note=VGroup(),VGroup()
        wm=ImageMobject(str(WATERMARK_PATH)).set_width(1.8).set_opacity(.35).to_corner(UR,buff=.28).set_z_index(60)
        brand=words('DA EQUAÇÃO AO FENÔMENO',7.35,18,DIM).to_edge(LEFT,buff=.4)
        self.add(wm,brand,self.title,self.subtitle)
        env=self.environment();env.suspend_updating()
        self.add(env.plane,env.axis,env.btag)
        self.play(LaggedStart(*[GrowArrow(a) for a in env.field],lag_ratio=.07),FadeIn(env.glows),run_time=1.1)
        self.remove(*env.get_family());env.resume_updating();self.add(env)
        self.path=always_redraw(lambda:self.luminous_curve(self.reveal.get_value()))
        self.particle=Dot(radius=.095,color=TEXT_COLOR).set_z_index(32)
        self.halo=Dot(radius=.22,color=CYAN,fill_opacity=.16).set_z_index(31)
        self.particle.add_updater(lambda m:m.move_to(self.project(self.physical()[0])))
        self.halo.add_updater(lambda m:m.move_to(self.project(self.physical()[0])))
        self.sync_particle();self.add(self.path,self.halo,self.particle)
        total=self.vector('v',TEXT_COLOR,r'\vec v',[-.4,-.4,0])
        parallel=self.vector('parallel',PARALLEL,r'\vec v_\parallel',[-.48,.2,0])
        transverse=self.vector('perp',VIOLET,r'\vec v_\perp',[-.05,.42,0])
        force=self.vector('F',PINK,r'\vec F',[-.38,-.4,0])

        # A — o mesmo palco se reconfigura; a condição precede a mudança.
        self.mark('abertura_campo_montado')
        self.equation(r'\vec v',r'\parallel',r'\vec B',r'\Rightarrow',r'\vec F','=0',note='entrada paralela • trajetória reta',duration=.8)
        initial_v=self.vector('v',TEXT_COLOR,r'\vec v',[.3,.15,0]);initial_v.update(0)
        self.add(initial_v);self.turn(4*PI,2.4);self.remove(initial_v)
        self.equation(r'\vec v',r'\perp',r'\vec B',note='nova condição: entrada perpendicular',duration=.8)
        self.reset_run(vz=0);self.mark('abertura_perpendicular');self.add(initial_v);initial_v.update(0)
        self.turn(TAU,2.4);self.remove(initial_v)
        self.equation(r'v_\parallel',r'\ne0,\quad',r'v_\perp',r'\ne0',note='nova condição: entrada oblíqua',duration=.8)
        self.reset_run();self.mark('abertura_obliqua');self.add(initial_v);initial_v.update(0)
        self.turn(4*PI,3.5);self.remove(initial_v)
        self.heading('Três trajetórias. O mesmo campo.','O que muda na velocidade de entrada?',carry=True,plane=1)
        self.live_until(15.5)

        # B — fase comum ao fenômeno, vetores, cursores e pontos nas curvas.
        self.heading('A força muda a direção','Somente força magnética • regime não relativístico',plane=0)
        self.equation(r'\vec F','=','q',r'\vec v',r'\times',r'\vec B',note='B = B₀ • uniforme e constante',duration=.8)
        self.reset_run()
        if self.reference is not None:self.play(FadeOut(self.reference),run_time=.4);self.reference=None
        self.play(self.view_scale.animate.set_value(LAYOUT['graph_scale']),self.view_lift.animate.set_value(LAYOUT['graph_lift']),run_time=.8)
        total.update(0);force.update(0);self.play(FadeIn(total),FadeIn(force),run_time=.6)
        self.turn(.5*PI,2.5)
        self.equation(r'\vec F',r'\cdot',r'\vec v','=0',duration=.8)
        graphs=self.graphs()
        focused_eq=self.eq.copy().scale(.82).move_to([-1.2,4.15,0])
        self.play(Succession(FadeOut(self.eq,run_time=.2),
                             AnimationGroup(FadeIn(graphs),FadeIn(focused_eq),run_time=.4)),run_time=.6)
        self.remove(*self.eq.get_family());self.eq=focused_eq
        self.mark('graficos_sincronizados_inicio');self.wait(.6)
        self.turn(1.8*PI,8.1);self.turn(TAU,1.8);self.wait(.4)
        self.mark('graficos_ultimo_ciclo')
        self.play(graphs.curves.animate.set_stroke(opacity=.16),run_time=.4)
        self.play(FadeOut(graphs,shift=DOWN*.10),run_time=.7)
        restored_eq=self.eq.copy().scale(1/.82).move_to([0,LAYOUT['equation'],0])
        self.play(self.view_scale.animate.set_value(LAYOUT['geometry_scale']),
                  self.view_lift.animate.set_value(LAYOUT['geometry_lift']),
                  Succession(FadeOut(self.eq,run_time=.3),FadeIn(restored_eq,run_time=.6)),run_time=.9)
        self.remove(*self.eq.get_family());self.eq=restored_eq
        self.play(FadeOut(force),run_time=.4)
        self.live_until(38,end_phase=2.35*PI)

        # C — construção geométrica primeiro; a equação entra como síntese.
        self.heading('Uma velocidade, duas componentes','A soma fecha no próprio espaço')
        self.play(self.velocity_scale.animate.set_value(2),run_time=.8)
        self.grow_vector(parallel);self.grow_vector(transverse)
        guides=always_redraw(self.guides);self.play(FadeIn(guides),run_time=.5)
        self.equation(r'\vec v','=',r'\vec v_\parallel','+',r'\vec v_\perp',duration=.8)
        self.mark('decomposicao_construida');self.live_until(44,end_phase=2.42*PI)
        self.equation(r'\vec v_\parallel',r'\times',r'\vec B','=0',note='A componente paralela produz avanço',duration=.8)
        self.play(Indicate(parallel,color=PARALLEL),run_time=.7);self.turn(2.85*PI,2.4)
        self.equation(r'\vec F','=','q',r'\vec v_\perp',r'\times',r'\vec B',note='A componente transversal produz curvatura',duration=.8)
        force.update(0);self.play(FadeOut(total),FadeOut(guides),FadeIn(force),run_time=.6)
        self.turn(3.5*PI,3.5);self.live_until(57)

        # D — a hélice se achata na projeção; o título muda depois da perspectiva.
        self.clear_equation(.4)
        shadow=Dot(radius=.09,color=VIOLET).set_z_index(27)
        shadow.add_updater(lambda m:m.move_to(self.project([*self.physical()[0][:2],0])));shadow.update(0)
        circle=always_redraw(lambda:self.luminous_curve(TAU,circle=True))
        self.play(FadeIn(circle),FadeIn(shadow),FadeOut(parallel),FadeOut(transverse),FadeOut(force),run_time=.6)
        self.play(self.front.animate.set_value(1),self.field_alpha.animate.set_value(0),
                  self.path_alpha.animate.set_value(.13),self.plane_alpha.animate.set_value(1),run_time=1.3)
        self.play(FadeOut(self.path),FadeOut(self.particle),FadeOut(self.halo),run_time=.5)
        heading=VGroup(words('No plano perpendicular a',0,32),math(r'\vec B',y=0,size=35,color=BLUE)).arrange(RIGHT,buff=.14).move_to(UP*LAYOUT['title'])
        self.heading(heading,'Velocidade tangencial • força para o centro')
        field_front=VGroup(math(r'\odot\;\vec B',y=0,size=35,color=BLUE),
                           words('saindo da tela',0,21,BLUE)).arrange(DOWN,buff=.14).move_to([2.5,LAYOUT['legend'],0])
        def circle_vector(which,color):
            p,vt,_,_,f=self.physical();p[2]=0;d=vt if which=='v' else f
            return Arrow(self.project(p),self.project(p+.75*d),buff=0,color=color,stroke_width=5.2).set_z_index(22)
        cv=always_redraw(lambda:circle_vector('v',VIOLET));cf=always_redraw(lambda:circle_vector('F',PINK))
        radius=always_redraw(lambda:Line(self.project([0,0,0]),shadow.get_center(),color=TEXT_COLOR,stroke_width=1.4,stroke_opacity=.65))
        center=always_redraw(lambda:Dot(self.project([0,0,0]),radius=.04,color=DIM))
        rtag=math('r',size=30)
        def place_r(m):
            a,b=self.project([0,0,0]),shadow.get_center();d=b-a;n=np.array([-d[1],d[0],0])/max(np.linalg.norm(d),.001)
            m.move_to((a+b)/2+.42*n)
        rtag.add_updater(place_r)
        legends=VGroup(math(r'\vec v_\perp',y=LAYOUT['legend'],size=31,color=VIOLET).set_x(-2.1),math(r'\vec F',y=LAYOUT['legend'],size=31,color=PINK).set_x(-.5))
        self.play(FadeIn(VGroup(field_front,cv,cf,radius,center,rtag,legends)),run_time=.4)
        # Os objetos dinâmicos são raízes próprias para preservar seus updaters.
        self.remove(field_front,cv,cf,radius,center,rtag,legends)
        self.add(field_front,cv,cf,radius,center,rtag,legends)
        answer=self.radius_algebra()
        answer=self.period_algebra(answer)

        # E — uma volta explícita constrói T e p; fase idêntica nas três projeções.
        self.play(FadeOut(field_front),FadeOut(cv),FadeOut(cf),FadeOut(radius),FadeOut(center),FadeOut(rtag),
                  FadeOut(legends),FadeOut(answer),FadeOut(self.omega_reference),run_time=.6)
        self.heading('Círculo + translação = hélice','Uma volta transversal acompanha um avanço longitudinal')
        self.play(self.front.animate.set_value(0),self.field_alpha.animate.set_value(1),
                  self.phase_tracker.animate.set_value(TAU*np.ceil(self.phase_tracker.get_value()/TAU)),run_time=1.2)
        self.phase_tracker.set_value(0);self.reveal.set_value(0);self.path_alpha.set_value(1);self.sync_particle()
        longitudinal=Dot(radius=.08,color=PARALLEL).set_z_index(26)
        longitudinal.add_updater(lambda m:m.move_to(self.project([0,0,self.physical()[0][2]])));longitudinal.update(0)
        connectors=always_redraw(lambda:VGroup(DashedLine(shadow.get_center(),self.particle.get_center(),dash_length=.12,color=VIOLET,stroke_width=1.2,stroke_opacity=.45),
                                              Line(longitudinal.get_center(),self.particle.get_center(),color=PARALLEL,stroke_width=1.3,stroke_opacity=.5)))
        # O ponto e a guia verdes identificam o avanço descrito no subtítulo.
        circle_label=words('círculo',0,22,VIOLET).scale_to_fit_width(.8).move_to(self.project([1.2,-1.2,0]))
        revolution=always_redraw(lambda:self.curve(min(self.phase_tracker.get_value(),TAU),circle=True).set_stroke(width=4.5))
        timebadge=VGroup(words('1 volta',0,25),math(r'\longleftrightarrow T',y=0,size=32)).arrange(RIGHT,buff=.15).move_to([0,4.2,0])
        a,b=self.physical(0)[0],self.physical(TAU)[0];aa=np.array([1.7,0,a[2]]);bb=np.array([1.7,0,b[2]])
        t0=VGroup(Dot(self.project(a),color=TEXT_COLOR,radius=.065),math('t_0',size=23).move_to(self.project(a)+RIGHT*.35+DOWN*.35))
        self.add(self.path,longitudinal,connectors,circle_label,revolution,timebadge,t0)
        self.play(FadeIn(self.particle),FadeIn(self.halo),run_time=.4)
        self.mark('composicao_volta_inicio');self.turn(TAU,6)
        self.mark('composicao_volta_T')
        endpoint=VGroup(Dot(self.project(b),color=TEXT_COLOR,radius=.065),math('t_0+T',size=23).move_to(self.project(b)+UP*.35))
        pitch=VGroup(DashedLine(self.project(a),self.project(aa),color=DIM,stroke_width=1.2),
                     DashedLine(self.project(b),self.project(bb),color=DIM,stroke_width=1.2),
                     DoubleArrow(self.project(aa),self.project(bb),buff=0,color=PARALLEL,stroke_width=3),
                     math('p',size=32,color=PARALLEL).move_to(self.project((aa+bb)/2)+RIGHT*.40))
        self.play(FadeIn(endpoint),Create(pitch[0]),Create(pitch[1]),run_time=.4)
        self.play(GrowFromPoint(pitch[2],self.project(aa)),FadeIn(pitch[3]),run_time=.6)
        self.phase_tracker.add_updater(lambda m,dt:m.increment_value(dt*PI*.08))
        self.equation('p','=',r'|v_\parallel|','T',note='Passo: deslocamento longitudinal em uma volta',duration=.8)
        self.mark('passo_p_construido')
        self.equation('p','=',r'\frac{2\pi m|v_\parallel|}{|q|B}',duration=.8)
        self.phase_tracker.clear_updaters();self.turn(4*PI,4.6)
        self.live_until(110.8)
        self.play(FadeOut(t0),FadeOut(endpoint),FadeOut(pitch),FadeOut(connectors),FadeOut(longitudinal),FadeOut(shadow),
                  FadeOut(circle),FadeOut(circle_label),FadeOut(revolution),FadeOut(timebadge),run_time=.4)

        # F — baseline contínuo; os rótulos entram depois de a geometria se estabelecer.
        self.compare('B',1.6,'Campo mais intenso','Mesmas velocidades, massa e módulo da carga',
                     [r'r\propto\frac1B',r'\quad',r'p\propto\frac1B'],r'B_1>B_0\quad(\Delta t=T_0)',True,True)
        self.compare('vp',1.5,'Mais velocidade transversal','Mesmo B, avanço paralelo, massa e módulo da carga',
                     ['r',r'\propto',r'v_\perp',r'\qquad T=\mathrm{const.}'],r'v_{\perp1}>v_{\perp0}\quad T_1=T_0',True,False)
        self.compare('vz',.48,'Mais velocidade paralela','Mesmo B, giro transversal, massa e módulo da carga',
                     ['p',r'\propto',r'|v_\parallel|'],r'|v_{\parallel1}|>|v_{\parallel0}|\quad r_1=r_0',False,True)

        # Q — duas entradas idênticas; força inverte ANTES da nova curvatura.
        self.heading('O sinal muda o sentido do giro','Duas partículas • mesma posição e velocidade iniciais',plane=0)
        self.equation(r'\vec r_0,\ \vec v_0,\ m,\ |q|,\ B\ \text{iguais}',note='Somente o sinal da carga é diferente',duration=.8)
        self.reset_run(common=True)
        badge=math('q>0',y=4.05,size=36,color=PINK);self.add(badge)
        self.velocity_scale.set_value(1.1)
        v0=self.vector('v',TEXT_COLOR,r'\vec v_0',[.35,-.3,0]);f0=self.vector('F',PINK,r'\vec F_0',[-.2,.35,0])
        self.play(FadeIn(v0),FadeIn(f0),run_time=.4);self.mark('q_positivo_mesma_entrada');self.wait(.4)
        self.play(FadeOut(v0),FadeOut(f0),run_time=.4);self.turn(4*PI,2.3)
        positive=self.curve(4*PI).set_stroke(color=DIM,opacity=.28,width=2).set_fill(opacity=0).set_z_index(-7)
        self.add(positive)
        if self.reference is not None:self.remove(self.reference);self.reference=None
        self.play(FadeOut(self.particle),FadeOut(self.halo),self.path_alpha.animate.set_value(.25),self.axis_alpha.animate.set_value(0),run_time=.4)
        self.phase_tracker.set_value(0);self.reveal.set_value(0);self.sync_particle()
        v0.update(0);f0.update(0)
        self.play(FadeIn(self.particle),FadeIn(self.halo),FadeIn(v0),FadeIn(f0),run_time=.4)
        f0.suspend_updating();self.charge_sign=-1
        new_badge=math('q<0',y=4.05,size=36,color=PINK)
        new_force=self.physical()[4];tip=self.project(self.physical()[0]+1.25*new_force)
        self.mark('q_forca_inverte_inicio')
        self.play(Rotate(f0[0],angle=PI,about_point=self.particle.get_center()),
                  f0[1].animate.move_to(tip+np.array([-.2,.35,0])),FadeTransform(badge,new_badge),self.axis_alpha.animate.set_value(1),run_time=.8)
        f0.resume_updating();badge=new_badge;self.path_alpha.set_value(1)
        self.mark('q_negativo_mesma_entrada');self.wait(.3)
        self.play(FadeOut(v0),FadeOut(f0),run_time=.4);self.turn(4*PI,2.3)
        self.equation(r'r,\quad T,\quad |p|\quad\text{iguais}',note='Força invertida → curvatura invertida',duration=.8)
        self.wait(.3);self.play(FadeOut(badge),FadeOut(positive),run_time=.4);self.clear_equation(.4)

        # G — a mesma partícula e as duas projeções recompõem a hélice no fim.
        self.heading('Duas componentes explicam a trajetória',plane=1)
        self.consequence(r'\vec v_\perp','círculo',note='entrada perpendicular')
        self.reset_run(vz=0);self.turn(TAU,2.8)
        self.consequence(r'\vec v_\parallel','translação',note='nova condição: entrada paralela')
        self.reset_run(vp=0);self.turn(4*PI,2.8)
        self.equation(r'\vec v','=',r'\vec v_\parallel','+',r'\vec v_\perp',note='entrada oblíqua • trajetória helicoidal',duration=.8)
        self.reset_run();shadow.update(0);longitudinal.update(0)
        self.play(FadeIn(circle),FadeIn(shadow),FadeIn(longitudinal),FadeIn(connectors),run_time=.4)
        self.turn(4*PI,3.4)
        self.heading('Giro transversal + avanço paralelo\n= hélice.',carry=True)
        self.mark('sintese_final')
        self.turn(self.phase_tracker.get_value()+PI*.18,2.7)
        self.mark('sintese_leitura_fim')

        # End card: somente o handle, sem watermark e sem outra linha de texto.
        for m in list(self.mobjects):m.clear_updaters()
        self.play(*[FadeOut(m) for m in list(self.mobjects) if not isinstance(m,ValueTracker)],run_time=.5)
        self.clear()
        handle=words('@labparallax',0,48).set_color_by_gradient(CYAN,VIOLET,PINK)
        self.play(FadeIn(handle,scale=.96),run_time=.5);self.mark('endcard_handle')
        self.wait(1.5);self.play(FadeOut(handle),run_time=.4);self.wait(.15)
        self.mark('fim')
        if not 174<=self.time<=182:raise RuntimeError(f'Duração fora da faixa: {self.time:.3f}s')
        (UNIT/'media_layout_ritmo'/'estados.json').write_text(json.dumps(self.events,ensure_ascii=False,indent=2),encoding='utf-8')

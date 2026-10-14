"""EP. 06 — V7: comparação física, hierarquia visual e genealogia matemática.

Lifecycle: torre -> globo -> corte equatorial -> torre local.
Cada transição conserva sua direção radial e retira os demais objetos do bloco.
Preview silencioso; dinâmica local em primeira ordem em omega_T.
"""
import json
import sys
from pathlib import Path
import numpy as np
from manim import *
from MF_Tools import TransformByGlyphMap
UNIT = Path(__file__).resolve().parent
sys.path.insert(0, str(UNIT))
from visual_v4 import build_torre, glowing_ball, symbol_into_screen
from template.config import BACKGROUND_COLOR, WATERMARK_PATH
from template.fonts import screen_text
config.media_dir = str(UNIT / 'media_v7')
W,C,B,V,M,P = '#F5F7FF','#35D9FF','#267BFF','#745CFF','#8492AE','#EA63FF'

def text(s,y=0,x=0,size=24,color=W,width=7.6):
    m=screen_text(s,font_size=size,color=color,oversample=3)
    if m.width>width: m.scale_to_fit_width(width)
    return m.move_to([x,y,0])

def eq(*s,y=4.5,x=0,size=38,width=7.5,color=W):
    m=MathTex(*s,font_size=size,color=color)
    if m.width>width: m.scale_to_fit_width(width)
    for token,col in [(r'\omega',V),(r'\omega_T',V),(r'\vec\omega',V),
                      (r'\vec\omega_T',V),('u',B),(r'\vec v',B),
                      (r'\vec a_C',C),('a_x',C),(r'\hat x',C),
                      ('v_x(t)',B),('v_x(0)',B),(r'v_\phi',B),
                      (r'\dot v_\phi',B),('x(t)',C),('x_f',C)]:
        m.set_color_by_tex(token,col,substring=False)
    return m.move_to([x,y,0])

def arrow(a,b,color=W,opacity=1):
    return Arrow(a,b,buff=0,color=color,stroke_width=3,tip_length=.16,
                 max_tip_length_to_length_ratio=.25).set_opacity(opacity)

def direction(a): return np.array([np.cos(a),np.sin(a),0.])

class QuedaCoriolis024(Scene):
    def cancel_two(self,old):
        """Cancelar fatores e barra de fração, preservando cada glifo restante."""
        source=eq(r'v_x(t)=2\omega_Tg\frac{t^2}{2}',y=2.7)
        target=eq(r'v_x(t)=\omega_Tgt^2',y=2.7)
        assert len(source[0])==14 and len(target[0])==11
        source[0][7:9].set_color(V);target[0][6:8].set_color(V)
        source[0][:2].set_color(B);target[0][:2].set_color(B)
        self.play(ReplacementTransform(old,source),run_time=.35)
        self.play(TransformByGlyphMap(source,target,
            (list(range(6)),list(range(6))),
            ([7,8,9,10,11],[6,7,8,9,10]),([6,12,13],[]),auto_fade=True),run_time=1.05)
        split=eq('v_x(t)','=',r'\omega_T','g',r't^2',y=2.7)
        self.remove(source,target);self.add(split)
        self.wait(.4)
        return split

    def substitute(self,old,new,index,source):
        """Uma substituição por vez, sem animar duas vezes o mesmo destino."""
        self.play(FadeOut(old[index]),
                  TransformFromCopy(source.copy().clear_updaters(),new[index]),
                  *[Transform(old[i],new[i]) for i in range(len(old)) if i!=index],run_time=1.1)
        self.remove(old,*list(old),*list(new));self.add(new)
        return new


    def earth_lab(self,hook):
        """Mesmo laboratório: globo -> disco -> duas contribuições -> torre.

        Norte entra na tela (x leste à direita, z radial para cima).
        Giro horário; arco é sentido, símbolo/vetor é velocidade angular.
        A altura é exagerada no corte. r² phi_dot é constante na queda.
        Lifecycle: só superfície, raio, tangente, eixo e bola atravessam o zoom.
        """
        tower0,ground0,plumb0,target0,ball0,q1,q2=hook
        tilt=ValueTracker(.4); cy=ValueTracker(-.1); rr=ValueTracker(2.5); phase=ValueTracker(-2)
        def project(lat,lon):
            k=tilt.get_value()
            return np.array([0,cy.get_value(),0])+rr.get_value()*np.array([
                np.cos(lat)*np.sin(lon),
                np.sqrt(max(0,1-k*k))*np.sin(lat)+k*np.cos(lat)*np.cos(lon),0])
        disk=always_redraw(lambda:Circle(rr.get_value(),color='#28436C',stroke_width=1.5,
                  fill_color='#0A1630',fill_opacity=1).move_to([0,cy.get_value(),0]))
        parallels=always_redraw(lambda:VGroup(*[
            ParametricFunction(lambda t,lat=lat:project(lat,t),t_range=[-PI,PI],
                               color=M,stroke_opacity=.22,stroke_width=1)
            for lat in [-.8,-.4,.4,.8]]))
        mer=always_redraw(lambda:VGroup(*[
            ParametricFunction(lambda t,lon=lon:project(t,lon+phase.get_value()),
                t_range=[-PI/2,PI/2],color='#506D9F',stroke_width=1.2,
                stroke_opacity=.5 if np.cos(lon+phase.get_value())>0 else .12)
            for lon in np.linspace(-PI,PI,9)[:-1]]))
        equator=always_redraw(lambda:ParametricFunction(lambda t:project(0,t),
                                     t_range=[-PI,PI],color=C,stroke_width=2.8))
        axis=always_redraw(lambda:Line(project(-PI/2,0)*1.0,
                    np.array([0,cy.get_value(),0])+UP*(3.2*np.sqrt(max(.001,1-tilt.get_value()**2))),
                    color=V,stroke_width=1.5))
        angular_vector=arrow([0,-.1,0],[0,3.1,0],V)
        poles=always_redraw(lambda:VGroup(Dot(project(PI/2,0),radius=.065,color=W),
                                        Dot(project(-PI/2,0),radius=.065,color=W)))
        experiment=Dot(project(0,phase.get_value()),radius=.1,color=C)
        experiment.add_updater(lambda m:m.move_to(project(0,phase.get_value())))
        omega=eq(r'\vec\omega_T',x=.65,y=3.1,size=30,color=V)
        omega_label=text('velocidade angular da Terra',x=1.7,y=3.75,size=17,color=V,width=4)
        spin_arc=Arc(radius=.52,start_angle=PI*.9,angle=-PI*1.4,color=V).add_tip(tip_length=.12).move_to([-2.9,2.65,0])
        spin_label=text('sentido do giro',x=-2.9,y=1.75,size=16,color=V,width=2.8)
        seal=text('EQUADOR · h = 50 m · SEM ARRASTO',y=5.5,size=20,color=M)
        self.play(*[FadeOut(m) for m in [tower0,ground0,plumb0,target0,q1,q2]],
                  ReplacementTransform(ball0,experiment),FadeIn(disk),FadeIn(parallels),
                  FadeIn(mer),Create(equator),FadeIn(axis),FadeIn(poles),
                  Create(angular_vector),Write(omega),FadeIn(omega_label),
                  Create(spin_arc),FadeIn(spin_label),FadeIn(seal),run_time=1.6)
        self.play(phase.animate.set_value(0),run_time=4.2,rate_func=linear)
        self.checkpoint('02 globo: vetor axial separado do arco de giro',.8)

        # A projeção se alinha ao eixo; a elipse abre, os polos convergem.
        O=np.array([0.,-1.8,0.]); R=2.55; H=.55; Rt=R+H
        center=symbol_into_screen(O,radius=.15).set_z_index(3)
        along_axis=text('olhando ao longo do eixo terrestre',y=5.5,size=22,color=M)
        self.play(tilt.animate.set_value(1),cy.animate.set_value(O[1]),rr.animate.set_value(R),
                  ReplacementTransform(angular_vector,center),FadeOut(omega_label),
                  omega.animate.move_to([-.48,-2.25,0]).scale(.8),
                  ReplacementTransform(seal,along_axis),FadeOut(spin_label),
                  spin_arc.animate.move_to([-3.15,-1.5,0]),run_time=1.6)
        for m in [disk,parallels,mer,equator,axis,poles,experiment]:m.clear_updaters()
        surface=Circle(R,color=C,stroke_width=2.5,fill_color='#0A1630',fill_opacity=.75).move_to(O)
        self.play(ReplacementTransform(equator,surface),FadeOut(disk),FadeOut(parallels),
                  FadeOut(mer),FadeOut(axis),FadeOut(poles),FadeOut(along_axis),run_time=.6)

        spin=ValueTracker(0); tau=ValueTracker(0); lock=ValueTracker(0)
        def rad(t):return Rt-H*t*t
        def excess(t):
            s=np.linspace(0,t,60)
            return .6*Rt*Rt*np.trapezoid(1/(Rt-H*s*s)**2,s)-.6*t
        def earth_angle():return spin.get_value()+.6*tau.get_value()
        def camera_angle():return lock.get_value()*earth_angle()
        def a_ref():return PI/2-earth_angle()+camera_angle()
        def a_ball():return a_ref()-excess(tau.get_value())
        def p_floor():return O+R*direction(a_ref())
        def p_ref():return O+rad(tau.get_value())*direction(a_ref())
        def p_ball():return O+rad(tau.get_value())*direction(a_ball())
        floor=Dot(p_floor(),radius=.075,color=C)
        topdot=Dot(O+Rt*UP,radius=.08,color=B)
        radius_line=Line(O,O+Rt*UP,color=W,stroke_width=1.5)
        mast=Line(O+R*UP,O+Rt*UP,color=W,stroke_width=5)
        self.play(ReplacementTransform(experiment,floor),Create(radius_line),Create(mast),
                  FadeIn(topdot),run_time=.7)
        floor.add_updater(lambda m:m.move_to(p_floor()))
        topdot.add_updater(lambda m:m.move_to(p_ball()))
        radius_line.add_updater(lambda m:m.put_start_and_end_on(O,p_ball()))
        mast.add_updater(lambda m:m.put_start_and_end_on(p_floor(),O+Rt*direction(a_ref())))
        mesh=always_redraw(lambda:VGroup(*[
            Line(O+.2*direction(a_ref()+j*PI/4),O+R*direction(a_ref()+j*PI/4),
                 color=M,stroke_width=.8,stroke_opacity=.13) for j in range(8)]))
        self.add(mesh)
        initial=VGroup(radius_line.copy().clear_updaters(),floor.copy().clear_updaters(),
                       topdot.copy().clear_updaters()).set_opacity(.18)
        self.add(initial)
        r_ground=eq('R',x=-.28,y=-.6,size=27)
        r_top=eq('R+h',x=.65,y=1.45,size=25)
        r_generic=eq('r',x=-.3,y=.4,size=28)
        r_ground.add_updater(lambda m:m.move_to(O+.52*R*direction(a_ref())+LEFT*.3))
        r_top.add_updater(lambda m:m.move_to(p_ball()+LEFT*.6+UP*.42))
        r_generic.add_updater(lambda m:m.move_to(O+.8*Rt*direction(a_ref())+LEFT*.27))
        angle_arc=Arc(radius=.7,start_angle=PI/2-.42,angle=.42,arc_center=O,color=V)
        angle_label=eq(r'd\theta',x=.65,y=-.7,size=25,color=V)
        arc_ground=Arc(radius=R,start_angle=PI/2-.42,angle=.42,arc_center=O,color=C,stroke_width=4)
        arc_top=Arc(radius=Rt,start_angle=PI/2-.42,angle=.42,arc_center=O,color=B,stroke_width=4)
        ds=eq('ds',x=1.55,y=1.2,size=27,color=B)
        dt=eq('dt',x=-1.35,y=1.4,size=26)
        caption=text('mesmo dt · mesmo ângulo · arcos diferentes',y=5.5,size=23)
        model=text('CORTE EQUATORIAL · ALTURA EXAGERADA',y=-6.6,size=16,color=M)
        self.play(Write(r_ground),Write(r_top),Write(r_generic),Write(dt),
                  FadeIn(caption),FadeIn(model),run_time=.8)
        self.play(spin.animate.set_value(.42),Create(angle_arc),Create(arc_ground),
                  Create(arc_top),Write(angle_label),Write(ds),run_time=2.4,rate_func=linear)
        arcs=eq('ds','=','r',r'd\theta',y=4.3,size=40)
        self.assemble(arcs,[(ds,0),(r_generic,2),(angle_label,3)])
        speed=eq('v','=',r'\frac{ds}{dt}',y=3,size=38)
        self.assemble(speed,[(arcs[0],2)])
        speed=self.change(speed,'v','=',r'\frac{r\,d\theta}{dt}',pause=.5)
        speed=self.change(speed,'v','=','r',r'\frac{d\theta}{dt}',pause=.5)
        omega_def=eq(r'\omega_T','=',r'\frac{d\theta}{dt}',y=2,size=31,color=V)
        self.assemble(omega_def,[(omega,0),(speed[3],2)])
        next_speed=eq(r'v_{\rm rot}','=',r'\omega_T','r',y=4.3,size=42)
        self.play(TransformFromCopy(omega_def[0],next_speed[2]),
                  TransformFromCopy(speed[2],next_speed[3]),
                  ReplacementTransform(speed[0],next_speed[0]),
                  ReplacementTransform(speed[1],next_speed[1]),FadeOut(speed[3]),
                  FadeOut(arcs),run_time=1.2)
        # Transformações de filhos podem desmontar o grupo pai na Scene.
        # Remover também a família evita deixar o r original solto na tela.
        self.remove(speed,*list(speed),*list(next_speed));self.add(next_speed)
        speed=next_speed
        self.checkpoint('03 ds = r dtheta -> velocidade -> omega r',1.2)
        self.out(omega_def,initial,r_ground,r_top,r_generic,dt,angle_arc,angle_label,
                 arc_ground,arc_top,ds,caption,time=.5)

        vt=always_redraw(lambda:arrow(p_ball(),p_ball()+(.9*Rt/rad(tau.get_value()))*direction(a_ball()-PI/2),B))
        vg=always_redraw(lambda:arrow(p_floor(),p_floor()+(.9*R/Rt)*direction(a_ref()-PI/2),M))
        vtop=eq(r'v_{\rm topo}','=',r'\omega_T','(R+h)',y=3.15,size=32,color=B)
        vground=eq(r'v_{\text{chão}}','=',r'\omega_T','R',y=2.25,size=34,color=M)
        self.play(Create(vt),Create(vg),run_time=.6)
        self.assemble(vground,[(speed[2],2),(speed[3],3)])
        self.assemble(vtop,[(speed[2],2),(speed[3],3)])
        greater=eq(r'v_{\rm topo}','>',r'v_{\text{chão}}',y=1.35,size=29)
        more=text('o topo já se move mais rápido para leste',y=5.5,size=23)
        self.play(Write(greater),FadeIn(more),spin.animate.increment_value(.12),run_time=1.2)
        ball=glowing_ball(p_ball(),radius=.095)
        self.play(ReplacementTransform(topdot,ball),run_time=.5)
        ball.add_updater(lambda m:m.move_to(p_ball()))
        relative=VGroup(text('parada em relação à torre',size=22),
                        text('mas não parada no espaço',size=22,color=B)).arrange(DOWN,buff=.15).move_to([0,-6,0])
        self.play(FadeIn(relative),spin.animate.increment_value(.2),run_time=1.6)
        self.checkpoint('04 topo mais rápido / bola em repouso relativo',1)
        self.out(speed,vtop,vground,greater,more,relative,vg,time=.5)

        view=text('VISTA DO ESPAÇO',y=5.5,size=22)
        rlabel=eq('r',size=25)
        vlabel=eq(r'v_\phi',size=25,color=B)
        rlabel.add_updater(lambda m:m.move_to(O+.58*(p_ball()-O)+LEFT*.2))
        vlabel.add_updater(lambda m:m.move_to(p_ball()+direction(a_ball()-PI/2)*.5+UP*.85))
        angular=eq(r'L_{\rm eixo}','=','m','r',r'v_\phi',r'\approx',r'\text{constante}',y=4.3,size=36)
        self.play(FadeIn(view),Write(rlabel),Write(vlabel),run_time=.7)
        self.assemble(angular,[(rlabel,3),(vlabel,4)])
        torque=text('sem torque → momento angular conservado',y=3.3,size=21,color=M)
        ahead=text('a bola começa a se adiantar para leste',y=-6,size=23,color=C)
        def history():
            t=tau.get_value()
            if t<.001:return VMobject()
            return VMobject(color=C,stroke_width=2.5).set_points_smoothly([
                O+rad(s)*direction(PI/2-spin.get_value()-.6*s-excess(s)+camera_angle())
                for s in np.linspace(0,t,60)])
        path=always_redraw(history);self.add(path)
        self.play(FadeIn(torque),tau.animate.set_value(.28),FadeIn(ahead),run_time=3.2,rate_func=linear)
        self.checkpoint('05 Lz conservado: r diminui, vphi aumenta',1)

        # Derivação na mesma bola; a malha terrestre tem seu próprio ponto no raio r.
        self.play(FadeOut(torque),FadeOut(ahead),
                  Transform(view,text('de onde vem a aceleração relativa?',y=5.5,size=23)),run_time=.5)
        inward=always_redraw(lambda:arrow(p_ball(),p_ball()-
                    min(.62,1.2*tau.get_value())*direction(a_ball()),B))
        usym=eq('u>0',x=2.5,y=-.3,size=27,color=B)
        inward_label=text('para dentro',x=2.55,y=-.85,size=17,color=B,width=2.7)
        usym.add_updater(lambda m:m.move_to(p_ball()-.65*direction(a_ball())+LEFT*.45+UP*.65))
        inward_label.add_updater(lambda m:m.next_to(usym,DOWN,buff=.14))
        radial_speed=eq(r'\dot r','=','-u',y=3.2,size=34,color=B)
        self.play(Create(inward),Write(usym),FadeIn(inward_label),run_time=.7)
        self.assemble(radial_speed,[(usym,2)])
        aexpr=eq('0','=',r'\frac{d}{dt}(rv_\phi)',y=2.05,size=35)
        self.assemble(aexpr,[(angular[3:5],2)])
        aexpr=self.change(aexpr,'0','=',r'\dot r',r'v_\phi','+','r',r'\dot v_\phi',y=2.05,size=34,pause=.5)
        corot=eq(r'v_\phi',r'\approx',r'\omega_T','r',y=1.15,size=30)
        near_release=text('perto da soltura',y=.15,size=17,color=M)
        self.assemble(corot,[(vlabel,0),(omega,2),(rlabel,3)])
        self.add(near_release)
        target=eq('0','=','(-u)',r'v_\phi','+','r',r'\dot v_\phi',y=2.05,size=34)
        aexpr=self.substitute(aexpr,target,2,radial_speed[2])
        # Agora somente a segunda substituição recebe sua cópia.
        target=eq('0',r'\approx','(-u)',r'(\omega_T r)','+','r',r'\dot v_\phi',y=2.05,size=34)
        aexpr=self.substitute(aexpr,target,3,corot[2:])
        self.play(tau.animate.set_value(.43),run_time=1.2,rate_func=linear)
        aexpr=self.change(aexpr,'r',r'\dot v_\phi',r'\approx','u',r'\omega_T','r',y=2.05,pause=.5)
        aexpr=self.change(aexpr,r'\dot v_\phi',r'\approx',r'\omega_T','u',y=2.05,pause=.5)
        gain=text('a bola ganha velocidade tangencial',y=5.5,size=23,color=B)
        self.play(Transform(view,gain),Indicate(vt,color=B),run_time=.8)
        self.checkpoint('06 contribuição A: bola ganha omega u',1.3)
        self.out(angular,corot,near_release,time=.5)
        self.play(aexpr.animate.scale(.8).move_to([-1.8,4.4,0]),
                  radial_speed.animate.scale(.8).move_to([2.2,4.4,0]),run_time=.7)

        refpoint=always_redraw(lambda:Dot(p_ref(),radius=.055,color=M))
        refvec=always_redraw(lambda:arrow(p_ref(),p_ref()+(.9*rad(tau.get_value())/Rt)*direction(a_ref()-PI/2),M))
        ref_label=eq(r'v_{\rm ref}',size=25,color=M)
        ref_label.add_updater(lambda m:m.move_to(p_ref()+LEFT*.25+DOWN*.7))
        self.play(FadeIn(refpoint),Create(refvec),Write(ref_label),run_time=.7)
        bexpr=eq(r'v_{\rm ref}','=',r'\omega_T','r',y=3,size=38,color=M)
        self.assemble(bexpr,[(ref_label,0),(omega,2),(rlabel,3)])
        bexpr=self.change(bexpr,r'\dot v_{\rm ref}','=',r'\omega_T',r'\dot r',y=3,pause=.5)
        btarget=eq(r'\dot v_{\rm ref}','=',r'\omega_T','(-u)',y=3,size=36)
        bexpr=self.substitute(bexpr,btarget,3,radial_speed[2])
        self.play(tau.animate.set_value(.62),run_time=1.5,rate_func=linear)
        bexpr=self.change(bexpr,r'\dot v_{\rm ref}','=','-',r'\omega_T','u',y=3,pause=.5)
        slower=text('mais perto do eixo, menor velocidade linear',y=5.5,size=23,color=M)
        self.play(Transform(view,slower),Indicate(refvec,color=M),run_time=.8)
        comparison_labels=VGroup(text('NO MESMO RAIO r',y=-4.75,size=17,color=M),
            text('bola',x=-2.25,y=-5.2,size=18,color=B,width=1.3),
            text('malha',x=-2.25,y=-5.8,size=18,color=M,width=1.3),
            eq(r'\Delta v',x=1.9,y=-5.2,size=25,color=C,width=1.2))
        def compare_speeds():
            start=np.array([-1.25,-5.2,0.]); rb=rad(tau.get_value())
            length_ball=2.1*Rt/rb; length_ref=2.1*rb/Rt
            return VGroup(arrow(start,start+RIGHT*length_ball,B),
                arrow(start+DOWN*.6,start+DOWN*.6+RIGHT*length_ref,M),
                arrow(start+RIGHT*length_ref,start+RIGHT*length_ball,C))
        comparison=always_redraw(compare_speeds)
        self.play(FadeIn(comparison_labels),FadeIn(comparison),run_time=.6)
        self.checkpoint('07 contribuição B: malha perde omega u',1.1)

        self.out(radial_speed,usym,inward_label,time=.5)
        self.play(aexpr.animate.move_to([-1.9,4.35,0]),bexpr.animate.scale(.8).move_to([1.9,4.35,0]),run_time=.7)
        rel=eq(r'a_{\rm rel}','=',r'\dot v_\phi','-',r'\dot v_{\rm ref}',y=3,size=38)
        self.assemble(rel,[(aexpr[0],2),(bexpr[0],4)])
        values=eq(r'a_{\rm rel}',r'\approx',r'\omega_T','u','-','(',r'-\omega_T','u',')',y=3,size=38)
        self.play(FadeOut(rel),TransformFromCopy(aexpr[2],values[2]),
                  TransformFromCopy(aexpr[3],values[3]),
                  TransformFromCopy(bexpr[2:4],values[6]),TransformFromCopy(bexpr[4],values[7]),
                  *[Write(values[i]) for i in [0,1,4,5,8]],run_time=1.3)
        self.remove(*list(values));self.add(values)
        values=self.change(values,r'a_{\rm rel}',r'\approx',r'\omega_T','u','+',r'\omega_T','u',y=3,pause=.5)
        # Strings únicas estabilizadas; a origem dos dois omega u é explícita.
        expanded=eq(r'a_{\rm rel}\approx\omega_Tu+\omega_Tu',y=3,size=42)
        lhs=len(expanded[0])-7
        expanded[0][lhs:lhs+2].set_color(V);expanded[0][lhs+2].set_color(B)
        expanded[0][lhs+4:lhs+6].set_color(V);expanded[0][lhs+6].set_color(B)
        self.play(ReplacementTransform(values,expanded),run_time=.6)
        fused=eq(r'a_{\rm rel}\approx2\omega_Tu',y=3,size=46)
        fused[0][lhs+1:lhs+3].set_color(V);fused[0][lhs+3].set_color(B)
        # Índices obtidos e conferidos pela topologia local do MathTex.
        lhs=len(expanded[0])-7
        assert len(fused[0])==lhs+4
        self.play(TransformByGlyphMap(expanded,fused,
            (list(range(lhs)),list(range(lhs))),
            ([lhs,lhs+4],[lhs+1]),([lhs+1,lhs+5],[lhs+2]),
            ([lhs+2,lhs+6],[lhs+3]),([lhs+3],[]),([],[lhs]),auto_fade=True),run_time=1.5)
        self.remove(expanded);self.add(fused)
        two=fused[0][lhs];two.set_color(C)
        self.play(Indicate(two,color=C,scale_factor=1.5),run_time=.8)
        twocauses=VGroup(text('a bola ganha',size=21,color=B),
                         text('+ a malha perde',size=21,color=C)).arrange(RIGHT,buff=.25).move_to([0,2,0])
        self.play(FadeIn(twocauses),tau.animate.set_value(.76),run_time=1.2)
        self.checkpoint('08 fator 2 nasce da bola e da malha terrestre',1.4)
        self.out(aexpr,bexpr,twocauses,time=.5)
        self.play(fused.animate.scale(.75).move_to([0,4.35,0]),
                  Transform(view,text('VISTA DO ESPAÇO',y=5.5,size=22)),run_time=.7)
        outside=always_redraw(lambda:VGroup(*[
            Line(O+(R+.18)*direction(j*PI/6+camera_angle()),
                 O+(R+.36)*direction(j*PI/6+camera_angle()),color=M,stroke_opacity=.22,stroke_width=1)
            for j in range(12)]))
        self.add(outside)
        self.play(tau.animate.set_value(.84),run_time=.9,rate_func=linear)
        self.play(lock.animate.set_value(1),
                  Transform(view,text('VISTA DA TERRA',y=5.5,size=22,color=C)),run_time=1.6)
        self.play(tau.animate.set_value(.92),run_time=1.6,rate_func=linear)
        self.checkpoint('09 câmera acompanha Terra; solo fixo, curva para leste',1)
        self.out(vt,ref_label,vlabel,rlabel,inward,comparison,comparison_labels,time=.5)
        cor_name=text('CORIOLIS',y=3.2,size=32,color=C)
        meaning=VGroup(text('No referencial que gira, essa aceleração',size=21),
                       text('aparente é Coriolis.',size=21)).arrange(DOWN,buff=.15).move_to([0,2.25,0])
        self.play(Write(cor_name),FadeIn(meaning),run_time=.8)
        tangent=always_redraw(lambda:arrow(p_ball(),p_ball()+.65*direction(a_ball()-PI/2),C))
        crossvec=always_redraw(lambda:arrow(p_ball(),p_ball()-.65*direction(a_ball()-PI/2),M))
        v_relative=always_redraw(lambda:arrow(p_ball(),p_ball()-.6*direction(a_ball()),B))
        vrel_label=eq(r'\vec v',x=-.65,y=.5,size=28,color=B)
        ac_label=eq(r'\vec a_C',x=1.55,y=.8,size=28,color=C)
        perpendicular=RightAngle(Line(p_ball(),p_ball()-.6*direction(a_ball())),
                                 Line(p_ball(),p_ball()+.65*direction(a_ball()-PI/2)),
                                 length=.14,color=M)
        crosscode=eq(r'\vec\omega',r'\times',r'\vec v',y=1.55,size=32)
        self.play(Create(v_relative),Create(crossvec),Write(vrel_label),
                  Create(perpendicular),run_time=.8)
        self.assemble(crosscode,[(omega,0),(vrel_label,2)])
        minus=eq('-',x=-.9,y=.9,size=35,color=C)
        self.play(Write(minus),ReplacementTransform(crossvec,tangent),Write(ac_label),run_time=.9)
        crossvec=VGroup()  # Já substituído: não ressuscitar a seta antiga na saída.
        self.out(cor_name,meaning,time=.4)
        general=eq(r'\vec a_C','=','-','2',r'\vec\omega',r'\times',r'\vec v',y=2.65,size=43)
        self.assemble(general,[(ac_label,0),(minus,2),(two,3),(crosscode[0],4),
                               (crosscode[1],5),(crosscode[2],6)])
        self.checkpoint('10 fórmula vetorial: duas contribuições, perpendicularidade e sinal',1.8)
        self.out(fused,crosscode,minus,vrel_label,ac_label,perpendicular,time=.5)

        # Zoom local: superfície -> chão; raio -> z; tangente -> x; eixo -> norte.
        for mob in [surface,floor,radius_line,mast,ball,mesh,path,outside,refpoint,refvec,
                    tangent,crossvec,v_relative]:mob.clear_updaters()
        tower,release=build_torre(x_c=-2.1,y_solo=-4.7,y_topo=.8,w_base=.9,w_topo=.35)
        origin=np.array([release,-4.7,0]);top=np.array([release,.8,0])
        arc=ArcBetweenPoints([-4,-4.7,0],[4,-4.7,0],angle=-.16,color=C,stroke_width=2)
        ground=Line([-4,-4.7,0],[4,-4.7,0],color=M,stroke_width=2)
        ex=arrow(origin,origin+RIGHT*3.2,C)
        ez=arrow(origin,origin+UP*1.3,W)
        north=symbol_into_screen(origin+LEFT*1.2+DOWN*.5,radius=.13)
        localball=glowing_ball(top);below=Dot(origin,color=W,radius=.06)
        self.play(surface.animate.set_fill(opacity=0),general.animate.scale(.78).move_to([0,5.7,0]),
                  FadeOut(view),FadeOut(model),FadeOut(spin_arc),FadeOut(omega),
                  FadeOut(mesh),FadeOut(outside),FadeOut(path),FadeOut(refpoint),
                  FadeOut(tangent),FadeOut(crossvec),FadeOut(v_relative),run_time=.8)
        self.play(ReplacementTransform(surface,arc),ReplacementTransform(radius_line,ez),
                  ReplacementTransform(refvec,ex),ReplacementTransform(center,north),
                  ReplacementTransform(mast,tower),ReplacementTransform(ball,localball),
                  ReplacementTransform(floor,below),run_time=2)
        self.play(ReplacementTransform(arc,ground),run_time=.8)
        labels=VGroup(eq(r'+x=\text{leste}',x=1.5,y=-5.1,size=24,color=C),
                      eq(r'+z=\text{cima}',x=-.65,y=-3.9,size=22),
                      eq(r'+y=\text{norte}',x=-1.8,y=-5.7,size=22,color=V))
        axes=VGroup(ex,ez,north,*labels)
        self.play(Write(labels),run_time=.8)
        self.remove(ex,ez,north,labels,*labels);self.add(axes)
        plumb=DashedLine(top,origin,color=W,stroke_opacity=.4,dash_length=.12)
        hub=Dot([-2.1,-4.7,0],radius=.04,color=W)
        self.play(Create(plumb),FadeIn(hub),run_time=.7)
        self.checkpoint('11 zoom da borda gera chão, vertical z, leste x e norte y',1)
        return general,tower,ground,origin,top,plumb,below,localball,axes,hub

    def checkpoint(self,name,hold=.5):
        self.wait(hold)
        self.qa.append({'estado':name,'t':round(float(self.time),3)})

    def change(self,old,*parts,pause=.4,**kw):
        kw.setdefault('y',old.get_center()[1]); kw.setdefault('x',old.get_center()[0])
        new=eq(*parts,**kw)
        self.play(TransformMatchingTex(old,new),run_time=1)
        self.wait(pause)
        return new

    def assemble(self,target,sources):
        """Genealogia explícita: fontes físicas são copiadas para slots da fórmula."""
        used={i for _,i in sources}
        self.play(*[TransformFromCopy(src.copy().clear_updaters(),target[i]) for src,i in sources],
                  *[Write(part) for i,part in enumerate(target) if i not in used],run_time=1.1)
        self.remove(*list(target)); self.add(target)

    def out(self,*mobs,time=.6):
        self.play(*[FadeOut(m) for m in mobs],run_time=time)

    def construct(self):
        self.qa=[]; self.camera.background_color=BACKGROUND_COLOR
        self.add(text('DA EQUAÇÃO AO FENÔMENO · EP. 06',size=18).set_opacity(.65)
                 .to_corner(UP+LEFT,buff=.4).set_z_index(20))
        self.add(ImageMobject(str(WATERMARK_PATH)).set_width(1.8).set_opacity(.35)
                 .to_corner(UP+RIGHT,buff=.28).set_z_index(20))
        # Gancho: a bola se tornará o ponto do laboratório no equador.
        tower,release=build_torre(y_solo=-4,y_topo=3.6)
        ground=Line([-4,-4,0],[4,-4,0],color=M,stroke_width=2)
        plumb=DashedLine([release,3.6,0],[release,-4,0],color=W,stroke_opacity=.4,dash_length=.12)
        target=Dot([release,-4,0],radius=.06,color=W)
        ball=glowing_ball([release,3.6,0])
        q1=text('SE EU SOLTAR A BOLA...',y=5.6,size=30)
        q2=VGroup(text('ELA CAI EXATAMENTE',size=28),text('AQUI?',size=28,color=C))
        q2.arrange(RIGHT,buff=.15).move_to([0,4.9,0])
        self.play(FadeIn(tower),Create(ground),FadeIn(ball),run_time=1.1)
        self.play(Create(plumb),FadeIn(target),Write(q1),run_time=1.1)
        self.play(Write(q2),Indicate(target,color=C,scale_factor=1.8),run_time=.9)
        self.checkpoint('01 gancho',3)

        general,tower,ground,origin,top,plumb,below,ball,axes,hub=self.earth_lab(
            (tower,ground,plumb,target,ball,q1,q2))
        earthomega=eq(r'\vec\omega_T','=',r'\omega_T\hat y',x=1.1,y=-2.8,size=28,color=V,width=4.5)
        vzero=eq(r'\vec v(0)','=','0',x=.1,y=.8,size=30,color=B,width=3)
        self.play(Write(earthomega),Write(vzero),run_time=.8)
        zero=eq(r'\vec a_C','=','-2',r'\vec\omega_T',r'\times',r'\vec0',y=4.2)
        self.assemble(zero,[(general[0],0),(earthomega[0],3),(vzero[2],5)])
        zero=self.change(zero,r'\vec a_C(0)','=','0')
        noac=text('sem velocidade relativa → sem Coriolis',y=3.2,size=21,color=M)
        self.play(FadeIn(noac),run_time=.6); self.checkpoint('12 soltura sem aceleração lateral',1)
        self.out(vzero,zero,noac)

        # Único tempo físico. S altera apenas a representação horizontal.
        tf=np.sqrt(100/9.8); wT=7.29e-5; scale=5.5/50; truexf=wT*9.8*tf**3/3
        t_tracker=ValueTracker(0); exaggeration=ValueTracker(1.85/(scale*truexf)); show_coriolis=ValueTracker(0)
        VELOCITY_MAX=.62; CORIOLIS_MAX=.56
        def position(t):
            return top+np.array([exaggeration.get_value()*scale*wT*9.8*t**3/3,-scale*9.8*t*t/2,0])
        ball.add_updater(lambda m:m.move_to(position(t_tracker.get_value())))
        def trail():
            t=t_tracker.get_value()
            if t<1e-5: return VMobject()
            return VMobject(color=C,stroke_width=2.5).set_points_smoothly([position(s) for s in np.linspace(0,t,55)])
        path=always_redraw(trail)
        velocity=always_redraw(lambda:arrow(position(t_tracker.get_value()),position(t_tracker.get_value())+
                              DOWN*max(0,min(VELOCITY_MAX*t_tracker.get_value()/tf,
                                  VELOCITY_MAX,position(t_tracker.get_value())[1]-origin[1])),B)
                              if .01<t_tracker.get_value()<tf-.005 else VGroup())
        lateral=always_redraw(lambda:arrow(position(t_tracker.get_value()),position(t_tracker.get_value())+
                             RIGHT*min(CORIOLIS_MAX,CORIOLIS_MAX*t_tracker.get_value()/tf),C)
                             if show_coriolis.get_value() and .01<t_tracker.get_value()<tf-.005 else VGroup())
        self.add(path,velocity,lateral)
        vphysical=eq(r'\vec v(t)',r'\approx','-gt',r'\hat z',x=1.1,y=.1,size=29,color=B,width=4.5)
        vlabel=text('a queda cria velocidade relativa',x=1.25,y=-.55,size=18,color=B,width=4)
        self.play(t_tracker.animate.set_value(.7),Write(vphysical),FadeIn(vlabel),run_time=1.5)
        sub=eq(r'\vec a_C','=','-2','(',r'\omega_T\hat y',')',r'\times','(','-gt',r'\hat z',')',y=4.25,size=35)
        self.assemble(sub,[(earthomega[2],4),(vphysical[2],8),(vphysical[3],9)])
        self.checkpoint('13 queda / 14 termos físicos copiados',.5)
        signs=eq('(-2)(-gt)',r'\longrightarrow','+2gt',y=3.15,size=31)
        self.play(TransformFromCopy(VGroup(sub[2],sub[8]),signs),run_time=.8)
        cross=eq(r'\hat y',r'\times',r'\hat z','=',r'\hat x',y=2.25,size=31)
        east=text('LESTE',x=1.25,y=-1.6,size=21,color=C)
        self.play(Write(cross),show_coriolis.animate.set_value(1),FadeIn(east),run_time=1)
        sub=self.change(sub,r'\vec a_C','=','2',r'\omega_T','gt',r'\hat x',y=4.25)
        self.checkpoint('15 direção leste nasce da geometria',.5); self.out(signs,cross)
        ax=self.change(sub,'a_x','=','2',r'\omega_T','gt',y=3.6)
        notice=text('DESVIO EXAGERADO',y=-3.65,x=1.45,size=17,color=M,width=2.7)
        self.play(FadeIn(notice),run_time=.5)
        self.play(t_tracker.animate.set_value(tf),run_time=3.5,rate_func=linear)
        self.checkpoint('16 trajetória e vetores sincronizados',.5)
        velocity.clear_updaters(); lateral.clear_updaters()
        self.out(velocity,lateral,vphysical,vlabel,earthomega,east,general)

        # Integrais definidas: as condições iniciais são termos que desaparecem.
        ax=self.change(ax,'a_x','=',r'\frac{dv_x}{dt}','=','2',r'\omega_T','g','t',y=5.2)
        initial=eq('v_x(0)','=','0',y=4.1,size=27,color=B); self.play(Write(initial),run_time=.7)
        integral=eq('v_x(t)','-','v_x(0)','=',r'\int_0^t',r'2\omega_Tg\tau',r'\,d\tau',y=2.7,size=33)
        self.assemble(integral,[(ax[4:],5),(initial[0],2)])
        self.play(Indicate(integral[2],color=B),run_time=.6)
        integral=self.change(integral,'v_x(t)','=',r'\int_0^t',r'2\omega_Tg\tau',r'\,d\tau',y=2.7,size=33)
        integral=self.change(integral,'v_x(t)','=',r'2\omega_Tg',r'\frac{t^2}{2}',y=2.7)
        # Os dois fatores são marcados antes de desaparecerem; não há morph enganoso.
        numerator=integral[2][0]; denominator=integral[3][-1]
        cancellations=VGroup(Line(numerator.get_corner(DL),numerator.get_corner(UR),color=C),
                             Line(denominator.get_corner(DL),denominator.get_corner(UR),color=C))
        self.play(Create(cancellations),run_time=.5);self.wait(.35)
        self.remove(cancellations)
        vx=self.cancel_two(integral)
        self.checkpoint('17 primeira integração',.8); self.out(ax,initial)
        self.play(vx.animate.move_to([0,5.2,0]),run_time=.6)
        flow=eq(r'\frac{dx}{dt}','=','v_x(t)','=',r'\omega_T','g',r't^2',y=4,size=34)
        self.assemble(flow,[(vx[0],2),(vx[2],4),(vx[3],5),(vx[4],6)])
        initial2=eq('x(0)','=','0',x=2.7,y=2.95,size=26,color=C,width=2.7); self.play(Write(initial2),run_time=.6)
        integral2=eq('x(t)','-','x(0)','=',r'\int_0^t',r'\omega_Tg\tau^2',r'\,d\tau',y=1.9,size=32)
        self.assemble(integral2,[(flow[4:],5),(initial2[0],2)])
        integral2=self.change(integral2,'x(t)','=',r'\int_0^t',r'\omega_Tg\tau^2',r'\,d\tau',y=1.9,size=32)
        integral2=self.change(integral2,'x(t)','=',r'\omega_Tg',r'\frac{t^3}{3}',y=1.9)
        displacement=self.change(integral2,'x(t)','=',r'\frac13',r'\omega_T','g',r't^3',y=1.9)
        self.checkpoint('18 segunda integração',.8); self.out(vx,flow,initial2)

        # Tempo de queda: cota física e operações algébricas consecutivas.
        self.play(displacement.animate.scale(.85).move_to([0,5.7,0]),run_time=.6)
        brace=BraceBetweenPoints([-3.2,-4.7,0],[-3.2,.8,0],direction=LEFT,color=W)
        height=eq('h','=','50',r'\,\mathrm m',x=-3.25,y=1.2,size=28,width=1.7)
        self.play(GrowFromCenter(brace),Write(height),run_time=.8)
        fall=eq('h','=',r'\frac12','g',r't_f^2',y=4.4); self.assemble(fall,[(height[0],0)])
        fall=self.change(fall,'2','h','=','g',r't_f^2')
        fall=self.change(fall,r'\frac{2h}{g}','=',r't_f^2')
        fall=self.change(fall,'t_f','=',r'\sqrt{\frac{2h}{g}}')
        gravity=eq('g','=','9{,}8',r'\,\mathrm{m/s^2}',y=3.1,size=28); self.play(Write(gravity),run_time=.6)
        numeric_t=eq('t_f','=',r'\sqrt{\frac{2\cdot {{50}} }{ {{9{,}8}} }}',y=2,size=35)
        # Isolamento dos números dentro do radical: cópias chegam aos slots exatos.
        hslot=numeric_t.get_part_by_tex('50',substring=False)
        gslot=numeric_t.get_part_by_tex('9{,}8',substring=False)
        other=VGroup(*[p for p in numeric_t if p is not hslot and p is not gslot])
        self.play(Write(other),TransformFromCopy(height[2],hslot),
                  TransformFromCopy(gravity[2],gslot),run_time=1.2)
        self.remove(other,*list(numeric_t));self.add(numeric_t)
        timevalue=self.change(numeric_t,'t_f',r'\approx','3{,}19',r'\,\mathrm s',y=2)
        self.checkpoint('19 tempo de queda',.8); self.out(brace,height,fall)

        # Valores copiados um a um; precisão interna de tf preservada.
        displacement=self.change(displacement,'x_f','=',r'\frac13',r'\omega_T','g',r't_f^3',y=5.5,size=37)
        wvalue=eq(r'\omega_T','=',r'7{,}29\times10^{-5}',r'\,\mathrm{s^{-1}}',y=4.3,size=28,color=V)
        self.play(Write(wvalue),gravity.animate.move_to([0,3.3,0]),timevalue.animate.move_to([0,2.4,0]),run_time=.8)
        num=eq('x_f','=',r'\frac13',r'(7{,}29\times10^{-5})','g',r't_f^3',y=1.2,size=32)
        self.assemble(num,[(displacement[0],0),(wvalue[2],3)])
        num2=eq('x_f','=',r'\frac13',r'(7{,}29\times10^{-5})',r'(9{,}8)',r't_f^3',y=1.2,size=32)
        num=self.substitute(num,num2,4,gravity[2])
        num2=eq('x_f','=',r'\frac13',r'(7{,}29\times10^{-5})',r'(9{,}8)',r'(3{,}19\ldots)^3',y=1.2,size=31)
        num=self.substitute(num,num2,5,timevalue[2])
        self.checkpoint('20 substituição numérica',.5)
        num=self.change(num,'x_f',r'\approx',r'7{,}76\times10^{-3}',r'\,\mathrm m',y=1.2)
        num=self.change(num,'x_f',r'\approx','7{,}76',r'\,\mathrm{mm}',y=1.2)
        num=self.change(num,'x_f',r'\approx','0{,}776',r'\,\mathrm{cm}',y=1.2)
        self.out(displacement,wvalue,gravity,timevalue,time=.6)
        payoff=self.change(num,'x_f',r'\approx','0{,}77',r'\,\mathrm{cm}',y=2,size=49,color=C)
        box=SurroundingRectangle(payoff,color=C,buff=.22,stroke_width=2)
        east2=text('PARA LESTE',y=1.05,size=26,color=C)
        self.play(Create(box),FadeIn(east2),run_time=.6); self.checkpoint('21 payoff',1.2)
        self.out(payoff,box,east2)

        # Mesma curva, mesmo t: S -> 1. Sem segunda trajetória.
        self.play(exaggeration.animate.set_value(1),
                  Transform(notice,text('ESCALA REAL',y=-3.65,x=1.45,size=17,color=M)),run_time=2.5)
        self.checkpoint('22 escala física real',.7)
        self.remove(notice)
        ball.clear_updaters(); path.clear_updaters()
        insetcenter=np.array([1.5,-1.6,0]); inset=Circle(1.6,color=C,stroke_width=2,
                    fill_color='#0A1630',fill_opacity=1).move_to(insetcenter)
        pwhite=insetcenter+LEFT*.8+DOWN*.45; pcyan=insetcenter+RIGHT*.8+DOWN*.45
        insetgroup=VGroup(inset,text('AMPLIAÇÃO',x=1.5,y=-.5,size=20),
             Line(insetcenter+[-1.35,-.45,0],insetcenter+[1.35,-.45,0],color=M),
             DashedLine(pwhite+UP*.6,pwhite,color=W,dash_length=.08,stroke_width=1.5),
             Dot(pwhite,color=W,radius=.07),Dot(pcyan,color=C,radius=.07),
             arrow(pwhite+UP*.3,pcyan+UP*.3,C),eq(r'7{,}7\,\mathrm{mm}',x=1.5,y=-1.1,size=33,color=C),
             text('vertical',x=.7,y=-2.45,size=16,color=W,width=1.3),
             text('impacto',x=2.3,y=-2.45,size=16,color=C,width=1.3),
             eq(r'0{,}77\,\mathrm{cm}',x=1.5,y=-2.95,size=23,color=C))
        leader=VMobject(color=C,stroke_width=1.5).set_points_as_corners([
                     position(tf),[-.2,-4.2,0],insetcenter+DOWN*1.6])
        self.play(Create(leader),FadeIn(insetgroup),run_time=1.2)
        self.checkpoint('23 ampliação ligada ao impacto',2); self.out(insetgroup,leader)
        self.play(VGroup(tower,ground,plumb,below,ball,path,axes,hub).animate.set_opacity(.07),run_time=.7)
        end1=text('A OLHO NU,',y=3.8,size=30); end2=text('A QUEDA PARECE VERTICAL.',y=3,size=29)
        end3=text('MAS ELA TERMINA',y=1.6,size=23)
        end4=text('ALGUNS MILÍMETROS A LESTE.',y=.9,size=27,color=C)
        final=eq(r'50\,\mathrm m',r'\longrightarrow',r'0{,}77\,\mathrm{cm\ para\ leste}',y=-.5,size=35)
        self.play(Write(end1),Write(end2),run_time=1)
        self.play(Write(end3),Write(end4),run_time=1.2); self.play(Write(final),run_time=1)
        self.checkpoint('24 fechamento',3.5)
        (UNIT/'qa_v7_timestamps.json').write_text(json.dumps(self.qa,ensure_ascii=False,indent=2),encoding='utf-8')

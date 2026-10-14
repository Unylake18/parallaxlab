"""vid_0024 · EP. 06 — V8: aplicação de Coriolis à queda de uma torre.

Lifecycle: torre -> globo -> intuição curta -> recap -> torre local.
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
config.media_dir = str(UNIT / 'media_v8')
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
        """Intuição de 10 s e recap; sem derivação de Coriolis.

        O globo permanece durante a intuição e a leitura dos termos.
        Equador, direção radial, tangente e eixo geram o laboratório local.
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
        self.play(phase.animate.set_value(0),run_time=4.6,rate_func=linear)
        self.checkpoint('02 globo girando / equador',.8)


        def origin():return np.array([0.,cy.get_value(),0.])
        altitude=ValueTracker(.22);lead=ValueTracker(0)
        def floor_pos():return project(0,phase.get_value())
        def ball_pos():return origin()+(1+altitude.get_value())*(project(0,phase.get_value()+lead.get_value())-origin())
        def tangent():
            a=phase.get_value()
            t=np.array([np.cos(a),-tilt.get_value()*np.sin(a),0.])
            return t/np.linalg.norm(t)
        # Uma única ilustração curta; não é uma prova de referencial girante.
        experiment.clear_updaters()
        experiment.add_updater(lambda m:m.move_to(floor_pos()))
        radial=always_redraw(lambda:Line(origin(),ball_pos(),color=M,stroke_width=1.3,stroke_opacity=.6))
        mast=always_redraw(lambda:Line(floor_pos(),origin()+
                    (1+altitude.get_value())*(floor_pos()-origin()),color=W,stroke_width=4))
        bead=glowing_ball(ball_pos(),radius=.095)
        bead.add_updater(lambda m:m.move_to(ball_pos()))
        angular_vector.add_updater(lambda m:m.put_start_and_end_on(origin(),origin()+UP*(1.25*rr.get_value())))
        omega.add_updater(lambda m:m.move_to(angular_vector.get_end()+RIGHT*.5))
        vrot=eq(r'v_{\rm rot}','=',r'\omega_T','r',y=5.5,size=39)
        caption=text('no topo, a velocidade tangencial é maior',y=4.55,size=23)
        note=text('ILUSTRAÇÃO AMPLIADA',y=-5.5,size=15,color=M)
        self.play(ReplacementTransform(seal,vrot),FadeIn(caption),FadeIn(note),
                  tilt.animate.set_value(.75),FadeIn(radial),FadeIn(mast),FadeIn(bead),run_time=1)
        ghosts=VGroup(experiment.copy().clear_updaters(),bead.copy().clear_updaters()).set_opacity(.18)
        lower_arc=always_redraw(lambda:ParametricFunction(lambda a:project(0,a),
                              t_range=[0,.36],color=M,stroke_width=3))
        upper_arc=always_redraw(lambda:ParametricFunction(lambda a:origin()+
                         1.22*(project(0,a)-origin()),t_range=[0,.36],color=B,stroke_width=3))
        vf=always_redraw(lambda:arrow(floor_pos(),floor_pos()+.8*tangent(),M))
        vb=always_redraw(lambda:arrow(ball_pos(),ball_pos()+.95*tangent(),B))
        self.add(ghosts)
        self.play(phase.animate.set_value(.36),Create(lower_arc),Create(upper_arc),
                  Create(vf),Create(vb),run_time=2.2,rate_func=linear)
        self.checkpoint('03 intuição: arcos e velocidades no topo e chão',1)
        self.play(Transform(caption,text('a queda não apaga esse movimento para leste',y=4.55,size=23)),
                  phase.animate.set_value(.48),altitude.animate.set_value(.14),
                  lead.animate.set_value(.08),run_time=2.2,rate_func=linear)
        self.checkpoint('04 intuição curta: movimento para leste',1.1)
        self.out(vrot,caption,ghosts,lower_arc,upper_arc,vf,vb,note,time=.5)

        # Recap: v aqui é RELATIVA à Terra, não o v_rot da intuição anterior.
        recap=VGroup(text('No referencial da Terra, usamos',size=23),
                     text('a aceleração aparente de Coriolis.',size=23)).arrange(DOWN,buff=.15).move_to([0,4.25,0])
        self.play(cy.animate.set_value(-2),rr.animate.set_value(2),
                  spin_arc.animate.move_to([-3,-1,0]),FadeOut(omega_label),
                  FadeOut(spin_label),FadeIn(recap),run_time=1.2)
        xs=[-2.65,0,2.65]
        symbols=VGroup(eq(r'\vec\omega_T',x=xs[0],y=2.95,size=34,color=V),
                       eq(r'\vec v',x=xs[1],y=2.95,size=34,color=B),
                       eq(r'\vec a_C',x=xs[2],y=2.95,size=34,color=C))
        meanings=VGroup(text('rotação da Terra',x=xs[0],y=2.2,size=18,color=V,width=2.65),
            VGroup(text('velocidade relativa',size=18,color=B,width=2.65),
                   text('à Terra',size=18,color=B)).arrange(DOWN,buff=.08).move_to([xs[1],2.15,0]),
            VGroup(text('aceleração',size=18,color=C),text('de Coriolis',size=18,color=C))
                   .arrange(DOWN,buff=.08).move_to([xs[2],2.15,0]))
        self.play(TransformFromCopy(omega.copy().clear_updaters(),symbols[0]),
                  Write(symbols[1]),Write(symbols[2]),FadeIn(meanings),run_time=.9)
        self.remove(*list(symbols));self.add(symbols)
        general=eq(r'\vec a_C','=','-','2',r'\vec\omega_T',r'\times',r'\vec v',y=5.6,size=43)
        self.assemble(general,[(symbols[2],0),(symbols[0],4),(symbols[1],6)])
        perpendicular=text('perpendicular à rotação e à velocidade',y=1.2,size=18,color=M)
        self.play(FadeIn(perpendicular),run_time=.5)
        self.play(Indicate(general[4],color=V),Indicate(symbols[0],color=V),run_time=.65)
        self.play(Indicate(general[6],color=B),Indicate(symbols[1],color=B),run_time=.65)
        self.play(Indicate(general[0],color=C),Indicate(symbols[2],color=C),run_time=.65)
        self.checkpoint('05 recap curto: significado da fórmula',1.6)
        # A origem completa da expressão pertence ao futuro vid_0023_coriolis.
        self.out(recap,symbols,meanings,perpendicular,time=.5)

        # Zoom contínuo no laboratório: equador -> chão, raio -> z, tangente -> x.
        for m in [disk,parallels,mer,equator,axis,poles,experiment,radial,mast,bead,angular_vector,omega]:
            m.clear_updaters()
        tower,release=build_torre(x_c=-2.1,y_solo=-4.7,y_topo=.8,w_base=.9,w_topo=.35)
        base=np.array([release,-4.7,0]);top=np.array([release,.8,0])
        local_ball=glowing_ball(top);below=Dot(base,color=W,radius=.06)
        ex=arrow(base,base+RIGHT*3.2,C);ez=arrow(base,base+UP*1.3,W)
        north=symbol_into_screen(base+LEFT*.75+DOWN*.65,radius=.13)
        arc=ArcBetweenPoints([-4,-4.7,0],[4,-4.7,0],angle=-.15,color=C,stroke_width=2)
        ground=Line([-4,-4.7,0],[4,-4.7,0],color=M,stroke_width=2)
        # A tangente vem do ponto equatorial existente.
        tangent_axis=arrow(floor_pos(),floor_pos()+tangent(),C)
        self.play(Create(tangent_axis),general.animate.scale(.78).move_to([0,5.7,0]),run_time=.5)
        self.play(ReplacementTransform(equator,arc),ReplacementTransform(radial,ez),
                  ReplacementTransform(tangent_axis,ex),ReplacementTransform(angular_vector,north),
                  ReplacementTransform(mast,tower),ReplacementTransform(bead,local_ball),
                  ReplacementTransform(experiment,below),FadeOut(disk),FadeOut(parallels),
                  FadeOut(mer),FadeOut(axis),FadeOut(poles),FadeOut(spin_arc),FadeOut(omega),run_time=2)
        self.play(ReplacementTransform(arc,ground),run_time=.8)
        labels=VGroup(eq(r'+x=\text{leste}',x=1.35,y=-5.1,size=24,color=C),
                      eq(r'+z=\text{cima}',x=-.65,y=-3.9,size=22),
                      eq(r'+y=\text{norte}',x=-.8,y=-5.35,size=22,color=V,width=2.2))
        axes=VGroup(ex,ez,north,*labels)
        self.play(Write(labels),run_time=.8)
        self.remove(ex,ez,north,labels,*list(labels));self.add(axes)
        plumb=DashedLine(top,base,color=W,stroke_opacity=.4,dash_length=.12)
        hub=Dot([-2.1,-4.7,0],radius=.04,color=W)
        self.play(Create(plumb),FadeIn(hub),run_time=.7)
        self.checkpoint('06 zoom Terra -> referencial local',.8)
        return general,tower,ground,base,top,plumb,below,local_ball,axes,hub

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
        earthomega=eq(r'\vec\omega_T','=',r'\omega_T\hat y',x=-1.45,y=-6.05,size=27,color=V,width=3.8)
        vzero=eq(r'\vec v(0)','=','0',x=.1,y=.8,size=30,color=B,width=3)
        self.assemble(earthomega,[(axes[2],2),(general[4],0)])
        self.play(Write(vzero),run_time=.6)
        zero=eq(r'\vec a_C','=','-2',r'\vec\omega_T',r'\times',r'\vec0',y=4.2)
        self.assemble(zero,[(general[0],0),(earthomega[0],3),(vzero[2],5)])
        zero=self.change(zero,r'\vec a_C(0)','=','0')
        noac=text('sem velocidade relativa → sem Coriolis',y=3.2,size=21,color=M)
        self.play(FadeIn(noac),run_time=.6); self.checkpoint('07 soltura sem aceleração lateral',1.8)
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
        vphysical=eq(r'\vec v(t)',r'\approx','-gt',r'\hat z',x=1.1,y=1.15,size=31,color=B,width=4.5)
        vlabel=VGroup(text('velocidade',size=17,color=B,width=1.8),
                      text('da bola',size=17,color=B)).arrange(DOWN,buff=.07)
        vlabel.add_updater(lambda m:m.move_to([position(t_tracker.get_value())[0]+1.12,
            max(origin[1]+.55,position(t_tracker.get_value())[1]-.35),0]))
        self.play(t_tracker.animate.set_value(.7),Write(vphysical),FadeIn(vlabel),run_time=1.5)
        sub=eq(r'\vec a_C','=','-2','(',r'\omega_T\hat y',')',r'\times','(','-gt',r'\hat z',')',y=4.25,size=35)
        self.assemble(sub,[(earthomega[2],4),(vphysical[2],8),(vphysical[3],9)])
        self.checkpoint('08 queda e substituição física',.7)
        signs=eq('(-2)(-gt)',r'\longrightarrow','+2gt',y=3.15,size=31)
        self.play(TransformFromCopy(VGroup(sub[2],sub[8]),signs),run_time=.8)
        cross=eq(r'\hat y',r'\times',r'\hat z','=',r'\hat x',y=2.25,size=31)
        east=text('LESTE',x=-.7,y=.4,size=21,color=C)
        self.play(Write(cross[:-1]),run_time=.6)
        self.play(Write(cross[-1]),show_coriolis.animate.set_value(1),t_tracker.animate.set_value(1.2),FadeIn(east),run_time=.6)
        self.remove(*list(cross));self.add(cross)
        sub=self.change(sub,r'\vec a_C','=','2',r'\omega_T','gt',r'\hat x',y=4.25)
        self.checkpoint('09 direção leste nasce da geometria',1); self.out(signs,cross)
        ax=self.change(sub,'a_x','=','2',r'\omega_T','gt',y=3.6)
        notice=text('DESVIO EXAGERADO',y=-.8,x=2.3,size=17,color=M,width=2.8)
        self.play(FadeIn(notice),FadeOut(east),FadeOut(vlabel),run_time=.5)
        vlabel.clear_updaters()
        self.play(t_tracker.animate.set_value(tf),run_time=4.8,rate_func=linear)
        self.checkpoint('10 trajetória e vetores sincronizados',1)
        velocity.clear_updaters(); lateral.clear_updaters()
        vlabel.clear_updaters()
        self.out(velocity,lateral,vphysical,earthomega,general)

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
        self.play(Create(cancellations),run_time=.5);self.checkpoint('11 cancelamento dos fatores 2',.4)
        self.remove(cancellations)
        vx=self.cancel_two(integral)
        self.checkpoint('12 primeira integração',1.2); self.out(ax,initial)
        flow=eq(r'\frac{dx}{dt}','=','v_x(t)','=',r'\omega_T','g',r't^2',y=4.4,size=36)
        self.play(TransformMatchingTex(vx,flow),run_time=1.1)
        initial2=eq('x(0)','=','0',x=2.7,y=2.95,size=26,color=C,width=2.7); self.play(Write(initial2),run_time=.6)
        integral2=eq('x(t)','-','x(0)','=',r'\int_0^t',r'\omega_Tg\tau^2',r'\,d\tau',y=1.9,size=32)
        self.assemble(integral2,[(flow[4:],5),(initial2[0],2)])
        integral2=self.change(integral2,'x(t)','=',r'\int_0^t',r'\omega_Tg\tau^2',r'\,d\tau',y=1.9,size=32)
        integral2=self.change(integral2,'x(t)','=',r'\omega_Tg',r'\frac{t^3}{3}',y=1.9)
        displacement=self.change(integral2,'x(t)','=',r'\frac13',r'\omega_T','g',r't^3',y=1.9)
        self.checkpoint('13 segunda integração',1.2); self.out(flow,initial2)

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
        self.checkpoint('14 tempo de queda',1.1); self.out(brace,height,fall)

        # Valores copiados um a um; precisão interna de tf preservada.
        displacement=self.change(displacement,'x_f','=',r'\frac13',r'\omega_T','g',r't_f^3',y=5.5,size=37)
        wvalue=eq(r'\omega_T','=',r'7{,}29\times10^{-5}',r'\,\mathrm{s^{-1}}',y=4.3,size=28,color=V)
        self.play(Write(wvalue),gravity.animate.move_to([0,3.3,0]),timevalue.animate.move_to([0,2.4,0]),run_time=.8)
        num=eq('x_f','=',r'\frac13',r'(7{,}29\times10^{-5})','g',r't_f^3',y=1.65,size=32)
        self.assemble(num,[(displacement[0],0),(wvalue[2],3)])
        num2=eq('x_f','=',r'\frac13',r'(7{,}29\times10^{-5})',r'(9{,}8)',r't_f^3',y=1.65,size=32)
        num=self.substitute(num,num2,4,gravity[2])
        num2=eq('x_f','=',r'\frac13',r'(7{,}29\times10^{-5})',r'(9{,}8)',r'(3{,}19\ldots)^3',y=1.65,size=31)
        num=self.substitute(num,num2,5,timevalue[2])
        self.checkpoint('15 substituição numérica',1)
        num=self.change(num,'x_f',r'\approx',r'7{,}76\times10^{-3}',r'\,\mathrm m',y=1.65)
        num=self.change(num,'x_f',r'\approx','7{,}76',r'\,\mathrm{mm}',y=1.65)
        num=self.change(num,'x_f',r'\approx','0{,}776',r'\,\mathrm{cm}',y=1.65)
        self.out(displacement,wvalue,gravity,timevalue,time=.6)
        payoff=self.change(num,'x_f',r'\approx','0{,}77',r'\,\mathrm{cm}',y=2,size=49,color=C)
        box=SurroundingRectangle(payoff,color=C,buff=.22,stroke_width=2)
        east2=text('PARA LESTE',y=1.05,size=26,color=C)
        self.play(Create(box),FadeIn(east2),run_time=.6); self.checkpoint('16 payoff',2)
        self.out(payoff,box,east2)

        # Mesma curva, mesmo t: S -> 1. Sem segunda trajetória.
        self.play(exaggeration.animate.set_value(1),
                  Transform(notice,text('ESCALA REAL',y=-.8,x=2.3,size=17,color=M)),run_time=2.5)
        self.checkpoint('17 escala física real',1)
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
        self.checkpoint('18 ampliação ligada ao impacto',2.5); self.out(insetgroup,leader)
        self.play(VGroup(tower,ground,plumb,below,ball,path,axes,hub).animate.set_opacity(.07),run_time=.7)
        end1=text('A OLHO NU,',y=3.8,size=30); end2=text('A QUEDA PARECE VERTICAL.',y=3,size=29)
        end3=text('MAS ELA TERMINA',y=1.6,size=23)
        end4=text('ALGUNS MILÍMETROS A LESTE.',y=.9,size=27,color=C)
        final=eq(r'50\,\mathrm m',r'\longrightarrow',r'0{,}77\,\mathrm{cm\ para\ leste}',y=-.5,size=35)
        self.play(Write(end1),Write(end2),run_time=1)
        self.play(Write(end3),Write(end4),run_time=1.2); self.play(Write(final),run_time=1)
        self.checkpoint('19 fechamento',4.5)
        (UNIT/'qa_v8_timestamps.json').write_text(json.dumps(self.qa,ensure_ascii=False,indent=2),encoding='utf-8')

"""EP. 06 — V5: motivação inercial antes da derivação no referencial girante.

Lifecycle: torre -> globo -> corte equatorial -> haste -> torre local.
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
config.media_dir = str(UNIT / 'media_v5')
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
                      (r'\vec a_C',C),('a_x',C),(r'\hat x',C)]:
        m.set_color_by_tex(token,col,substring=False)
    return m.move_to([x,y,0])

def arrow(a,b,color=W,opacity=1):
    return Arrow(a,b,buff=0,color=color,stroke_width=3,tip_length=.16,
                 max_tip_length_to_length_ratio=.25).set_opacity(opacity)

def direction(a): return np.array([np.cos(a),np.sin(a),0.])

class QuedaCoriolis024(Scene):
    def substitute(self,old,new,index,source):
        """Uma substituição por vez, sem animar duas vezes o mesmo destino."""
        self.play(FadeOut(old[index]),
                  TransformFromCopy(source.copy().clear_updaters(),new[index]),
                  *[Transform(old[i],new[i]) for i in range(len(old)) if i!=index],run_time=1.1)
        self.remove(old,*list(old),*list(new));self.add(new)
        return new

    def motivation(self,equator,dot,disk,parallels,mer,axis,rot,omega,rotlabel,seal):
        """Corte equatorial: mesma rotação, velocidades distintas, queda e câmera.

        h/R é exagerado somente nesta geometria de motivação. A queda segue
        r(t) e a velocidade angular da bola satisfaz r² phi_dot = constante.
        A mudança de observador subtrai o mesmo ângulo de todos os objetos.
        """
        O=np.array([0.,-1.8,0.]); R=2.35; H=.55; Rt=R+H
        turn=ValueTracker(0); fall=ValueTracker(0); lock=ValueTracker(0)
        def ground_angle(): return PI/2-turn.get_value()*(1-lock.get_value())
        def radius(t): return Rt-H*t*t
        def excess(t):
            samples=np.linspace(0,t,45)
            return .6*Rt*Rt*np.trapezoid(1/(Rt-H*samples*samples)**2,samples)-.6*t
        def ball_angle(): return ground_angle()-excess(fall.get_value())
        def ground_pos(): return O+R*direction(ground_angle())
        def ball_pos(): return O+radius(fall.get_value())*direction(ball_angle())
        surface=Circle(R,color=C,fill_color='#0A1630',fill_opacity=.75,stroke_width=2).move_to(O)
        center=symbol_into_screen(O,radius=.16)
        floor=Dot(ground_pos(),color=C,radius=.09)
        radial=Line(O,O+Rt*UP,color=W,stroke_width=2)
        mast=Line(O+R*UP,O+Rt*UP,color=W,stroke_width=6)
        bead=glowing_ball(O+Rt*UP,radius=.095)
        self.play(FadeOut(disk),FadeOut(parallels),FadeOut(mer),FadeOut(axis),
                  ReplacementTransform(equator,surface),ReplacementTransform(dot,floor),
                  FadeOut(seal),FadeOut(rot),FadeOut(omega),FadeOut(rotlabel),
                  Create(radial),Create(mast),FadeIn(center),FadeIn(bead),run_time=1.2)
        radial.add_updater(lambda m:m.put_start_and_end_on(O,O+Rt*direction(ground_angle())))
        mast.add_updater(lambda m:m.put_start_and_end_on(ground_pos(),O+Rt*direction(ground_angle())))
        floor.add_updater(lambda m:m.move_to(ground_pos()))
        bead.add_updater(lambda m:m.move_to(ball_pos()))
        r0=eq('R',x=-.3,y=-.7,size=27)
        r1=eq('R+h',x=.6,y=.4,size=27)
        theta=Arc(radius=.75,start_angle=PI/2-.42,angle=.42,arc_center=O,color=V)
        theta_label=eq(r'd\theta',x=.6,y=-.55,size=27,color=V)
        arc0=Arc(radius=R,start_angle=PI/2-.42,angle=.42,arc_center=O,color=C,stroke_width=5)
        arc1=Arc(radius=Rt,start_angle=PI/2-.42,angle=.42,arc_center=O,color=B,stroke_width=5)
        ds=eq('ds',x=1.45,y=.95,size=27,color=B)
        same=text('mesmo ângulo · arco maior no topo',y=5.5,size=24)
        model=text('CORTE DO EQUADOR · ALTURA EXAGERADA',y=-5,size=15,color=M)
        self.play(Write(r0),Write(r1),FadeIn(same),FadeIn(model),run_time=.7)
        self.play(turn.animate.set_value(.42),Create(theta),Create(arc0),Create(arc1),
                  Write(theta_label),Write(ds),run_time=2,rate_func=linear)
        arceq=eq('ds','=','r',r'd\theta',y=4.35,size=36)
        self.assemble(arceq,[(ds,0),(r1,2),(theta_label,3)])
        speeds=eq('v', '=',r'\frac{ds}{dt}',r'\qquad',r'\omega_T','=',r'\frac{d\theta}{dt}',y=3.05,size=32)
        self.assemble(speeds,[(arceq[0],2),(theta_label,6)])
        speed=eq(r'v_{\rm rot}','=',r'\omega_T','r',y=4.35,size=38)
        self.play(TransformMatchingTex(arceq,speed),run_time=.9)
        self.play(TransformFromCopy(speeds[4],speed[2]),run_time=.55)
        self.checkpoint('03 mesmo ângulo, arco e velocidade maiores no topo',.65)
        self.out(speeds,same,r0,r1,theta,theta_label,arc0,arc1,ds,time=.4)
        vg=always_redraw(lambda:arrow(ground_pos(),ground_pos()+.8*direction(ground_angle()-PI/2),C))
        vt=always_redraw(lambda:arrow(bead.get_center(),bead.get_center()+.92*direction(ball_angle()-PI/2),B))
        gspeed=eq(r'v_{\text{chão}}','=',r'\omega_T','R',y=3.15,size=31,color=C)
        tspeed=eq(r'v_{\rm topo}','=',r'\omega_T','(R+h)',y=2.3,size=31,color=B)
        self.play(Create(vg),Create(vt),run_time=.5)
        self.assemble(gspeed,[(speed[2],2),(speed[3],3)])
        self.assemble(tspeed,[(speed[2],2),(speed[3],3)])
        self.checkpoint('04 velocidades tangenciais no chão e no topo',.6)
        view=text('VISTA DA TERRA',y=5.5,size=23,color=C)
        relative=text('parada em relação à torre ≠ parada no espaço',y=-5.7,size=21)
        self.play(lock.animate.set_value(1),FadeIn(view),FadeIn(relative),run_time=.9)
        self.wait(.65)
        self.play(lock.animate.set_value(0),Transform(view,text('VISTA DO ESPAÇO',y=5.5,size=23)),
                  turn.animate.increment_value(.25),run_time=1.5)
        self.checkpoint('05 repouso relativo e movimento no espaço',.6)
        self.out(speed,gspeed,tspeed,relative,vg,vt,time=.5)
        angular=eq(r'L_z',r'\approx',r'\text{constante}',y=4.25,size=37)
        radial_gravity=always_redraw(lambda:arrow(bead.get_center(),bead.get_center()-.65*direction(ball_angle()),W))
        gravity_label=text('gravidade radial · torque desprezível',y=3.25,size=21,color=M)
        ahead=text('a bola fica ligeiramente à frente do solo',y=-5.7,size=23,color=C)
        self.play(Write(angular),FadeIn(gravity_label),FadeIn(radial_gravity),run_time=.8)
        def track():
            t=fall.get_value()
            if t<.001:return VMobject()
            # Toda a história é reexpressa na câmera atual; nenhum rastro fixo na tela.
            start=turn.get_value()-.6*t
            return VMobject(color=C,stroke_width=2.5).set_points_smoothly([
                O+radius(s)*direction(PI/2-(start+.6*s)-excess(s)+lock.get_value()*turn.get_value())
                for s in np.linspace(0,t,45)])
        path=always_redraw(track)
        self.add(path)
        self.play(fall.animate.set_value(1),turn.animate.increment_value(.6),FadeIn(ahead),
                  run_time=3,rate_func=linear)
        self.checkpoint('06 conservação de momento angular: bola à frente do chão',.8)
        self.play(lock.animate.set_value(1),Transform(view,text('VISTA DA TERRA',y=5.5,size=23,color=C)),
                  FadeOut(angular),FadeOut(gravity_label),FadeOut(radial_gravity),run_time=1.2)
        rotating=text('o referencial agora está girando',y=4.6,size=21,color=V)
        question=text('qual termo reproduz essa curvatura neste referencial?',y=3.7,size=22)
        self.play(FadeIn(rotating),FadeIn(question),FadeOut(ahead),run_time=.7)
        # Repetir a mesma queda com o solo fixo torna a mudança observável.
        self.play(fall.animate.set_value(0),run_time=.65)
        self.play(fall.animate.set_value(1),turn.animate.increment_value(.6),run_time=2.2,rate_func=linear)
        coriolis=text('CORIOLIS',y=2.65,size=34,color=C)
        self.play(Write(coriolis),run_time=.7)
        self.checkpoint('07 necessidade de Coriolis antes da haste',.9)
        definition=VGroup(text('Aceleração aparente de um objeto em movimento',size=21),
                          text('descrito a partir de um referencial que gira.',size=21))
        definition.arrange(DOWN,buff=.16).move_to([0,3.65,0])
        self.play(FadeOut(question),FadeOut(rotating),FadeIn(definition),run_time=.6)
        ingredients=eq(r'\vec\omega',r'\qquad',r'\vec v',r'\qquad',r'\vec a_C',y=1.65,size=35)
        self.play(Write(ingredients),run_time=.8)
        self.checkpoint('08 significado: rotação, velocidade relativa e aceleração aparente',1.2)
        for m in [radial,mast,floor,bead,path]:m.clear_updaters()
        self.out(surface,center,mast,bead,path,model,view,definition,coriolis,ingredients,time=.7)
        context=text('vamos isolar a geometria',y=5.5,size=25)
        rot=Arc(radius=.7,start_angle=-.3,angle=1.6,arc_center=[-2.6,-1.6,0],color=V).add_tip(tip_length=.15)
        omega=eq(r'\omega',x=-3.25,y=-.4,size=32,color=V)
        rotlabel=text('rotação do referencial',x=-2.6,y=.15,size=18,color=V)
        self.play(FadeIn(context),FadeIn(rot),Write(omega),FadeIn(rotlabel),run_time=.7)
        return radial,floor,rot,omega,rotlabel,context

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
        self.play(Write(q2),run_time=.9); self.checkpoint('01 gancho',3)

        # Terra 2.5D: projeção de meridianos em longitudes variáveis.
        center=np.array([0.,-.1,0]); R=2.5; phase=ValueTracker(-.8)
        def project(lat,lon):
            return center+R*np.array([np.cos(lat)*np.sin(lon),
                      .91*np.sin(lat)-.40*np.cos(lat)*np.cos(lon),0])
        disk=Circle(R,color='#28436C',stroke_width=1.7,fill_color='#0A1630',fill_opacity=1).move_to(center)
        parallels=VGroup(*[ParametricFunction(lambda t,lat=lat:project(lat,t),t_range=[-PI,PI],
                    color=M,stroke_opacity=.22,stroke_width=1) for lat in [-.8,-.4,.4,.8]])
        def meridians():
            return VGroup(*[ParametricFunction(lambda t,lon=lon:project(t,lon+phase.get_value()),
                     t_range=[-PI/2,PI/2],color='#506D9F',stroke_width=1.2,
                     stroke_opacity=.52 if np.cos(lon+phase.get_value())>=0 else .12)
                     for lon in np.linspace(-PI,PI,9)[:-1]])
        mer=always_redraw(meridians)
        equator=ParametricFunction(lambda t:project(0,t),t_range=[-PI,PI],color=C,stroke_width=2.8)
        axis=Line(center+DOWN*3.2,center+UP*3.2,color=V,stroke_width=1.6)
        dot=Dot(project(0,phase.get_value()),radius=.1,color=C)
        dot.add_updater(lambda m:m.move_to(project(0,phase.get_value()))
                        .set_opacity(1 if np.cos(phase.get_value())>=0 else .18))
        rot=Arc(radius=.7,start_angle=-.4,angle=4.5,color=V).add_tip(tip_length=.15).move_to([0,3.25,0])
        omega=eq(r'\vec\omega_T',x=1.35,y=3.2,size=32,color=V)
        rotlabel=text('velocidade angular da Terra',x=1.25,y=2.6,size=18,color=V,width=4.5)
        seal=text('EQUADOR · h = 50 m · SEM ARRASTO',y=5.5,size=20,color=M)
        globe=VGroup(disk,parallels,mer,equator,axis)
        self.play(FadeOut(q1),FadeOut(q2),FadeOut(tower),FadeOut(plumb),FadeOut(ground),
                  FadeOut(target),ReplacementTransform(ball,dot),FadeIn(globe),FadeIn(rot),
                  Write(omega),FadeIn(rotlabel),FadeIn(seal),run_time=1.6)
        poles=VGroup(Dot(project(PI/2,0),radius=.065,color=W),Dot(project(-PI/2,0),radius=.065,color=W))
        self.add(poles)
        self.play(phase.animate.set_value(1.6),run_time=5,rate_func=linear)
        self.checkpoint('02 Terra girando',.7)
        dot.clear_updaters(); mer.clear_updaters()
        self.remove(poles)
        equator,dot,rot,omega,rotlabel,context=self.motivation(
            equator,dot,disk,parallels,mer,axis,rot,omega,rotlabel,seal)

        # Globo -> pivô; superfície -> haste; arco violeta preservado.
        pivot=np.array([-2.6,-1.6,0.]); angle=ValueTracker(.12); radius=ValueTracker(1.35)
        rod=Line(pivot,pivot+direction(.12)*5.6,color=W,stroke_width=3)
        bead=Dot(pivot+direction(.12)*radius.get_value(),radius=.13,color=B)
        hub=Dot(pivot,radius=.12,color=W)
        rod.add_updater(lambda m:m.put_start_and_end_on(pivot,pivot+5.6*direction(angle.get_value())))
        bead.add_updater(lambda m:m.move_to(pivot+radius.get_value()*direction(angle.get_value())))
        uvec=always_redraw(lambda:arrow(bead.get_center(),bead.get_center()+direction(angle.get_value()),B))
        usym=eq('u',y=-2.2,x=-.1,size=30,color=B)
        ulab=text('velocidade relativa da conta',y=-2.7,x=-.1,size=18,color=B,width=5)
        newrot=Arc(radius=.7,start_angle=-.3,angle=1.6,arc_center=pivot,color=V).add_tip(tip_length=.15)
        self.play(ReplacementTransform(dot,hub),ReplacementTransform(equator,rod),Transform(rot,newrot),
                  Transform(omega,eq(r'\omega',x=-3.25,y=-.4,size=32,color=V)),
                  Transform(rotlabel,text('rotação do referencial',x=-2.6,y=.15,size=18,color=V)),
                  FadeIn(bead),FadeIn(uvec),Write(usym),FadeIn(ulab),run_time=1.5)
        self.play(angle.animate.set_value(.28),radius.animate.set_value(1.7),run_time=1.2)
        self.checkpoint('04 Terra para haste / 05 variáveis físicas',.7)
        self.out(context)
        ask=text('DE ONDE VEM O 2?',y=5.5,size=25); self.play(FadeIn(ask),run_time=.5)

        # Primeira contribuição: dois raios, duas velocidades tangenciais.
        a=angle.get_value(); d=direction(a); tangent=direction(a+PI/2)
        p0=bead.get_center().copy(); p1=pivot+3.15*d
        ghost=Dot(p0,radius=.13,color=B).set_opacity(.25)
        t0=eq('t',x=p0[0],y=p0[1]-.45,size=23)
        t1=eq('t+dt',x=p1[0],y=p1[1]-.45,size=23)
        drarrow=arrow(p0+DOWN*.75,p1+DOWN*.75,W)
        dr=eq('dr','=','u',r'\,dt',y=-3.3,size=30)
        self.add(ghost)
        self.play(radius.animate.set_value(3.15),Create(drarrow),Write(t0),Write(t1),
                  usym.animate.move_to([1.4,-1.65,0]),ulab.animate.move_to([1.6,-2.15,0]),run_time=1.5)
        self.assemble(dr,[(usym,2)])
        vt0=arrow(p0,p0+.85*tangent,B,.3); vt1=arrow(p1,p1+1.58*tangent,B)
        vtl=eq('v_t',y=p1[1]+1.8,x=p1[0]-.6,size=27,color=B)
        diff=arrow(p1+.85*tangent+RIGHT*.25,p1+1.58*tangent+RIGHT*.25,C)
        self.play(Create(vt0),Create(vt1),Write(vtl),Create(diff),FadeOut(ask),run_time=1)
        desc=text('mudou o módulo tangencial',y=-4.5,size=23)
        algebra=eq('v_t','=',r'\omega','r',y=4.8)
        self.assemble(algebra,[(vtl,0),(omega,2)])
        algebra=self.change(algebra,'dv_t','=',r'\omega','dr')
        sub=eq('dv_t','=',r'\omega','u',r'\,dt',y=3.6)
        self.assemble(sub,[(algebra[0],0),(algebra[2],2),(dr[2],3),(dr[3],4)])
        self.play(FadeIn(desc),run_time=.5)
        sub=self.change(sub,r'\frac{dv_t}{dt}','=',r'\omega','u')
        a1=self.change(sub,'a_1','=',r'\omega','u',y=2.3)
        self.checkpoint('09 primeira contribuição',1)
        self.out(algebra,dr,drarrow,t0,t1,ghost,vt0,vt1,vtl,diff,desc)
        self.play(a1.animate.scale(.8).move_to([-2,5.4,0]),FadeOut(ulab),FadeOut(usym),run_time=.8)

        # Segunda contribuição: caudas alinhadas, módulos iguais, dv entre pontas.
        oldangle=angle.get_value(); newangle=oldangle+.32
        oldrod=rod.copy().clear_updaters().set_opacity(.18); self.add(oldrod)
        self.play(angle.animate.set_value(newangle),run_time=1.3)
        common=bead.get_center().copy()
        uref=arrow(common,common+direction(oldangle),B,.35)
        dv=arrow(common+direction(oldangle),common+direction(newangle),C)
        dvlabel=eq(r'd\vec u',x=common[0]+1.45,y=common[1]+.3,size=25,color=C)
        theta=Arc(radius=1.3,start_angle=oldangle,angle=.32,arc_center=pivot,color=V)
        thlabel=eq(r'd\theta',x=-.8,y=-.6,size=28,color=V)
        threl=eq(r'd\theta','=',r'\omega',r'\,dt',y=-3.3,size=32)
        self.play(Create(uref),Create(dv),Write(dvlabel),Create(theta),Write(thlabel),run_time=1.1)
        self.assemble(threl,[(thlabel,0),(omega,2)])
        desc2=text('mudou a direção da velocidade relativa',y=-4.5,size=23)
        second=eq(r'|d\vec u|',r'\approx','u',r'd\theta',y=4.1)
        self.assemble(second,[(dvlabel,0),(uvec,2),(thlabel,3)])
        self.play(FadeIn(desc2),run_time=.5)
        second=self.change(second,r'|d\vec u|',r'\approx','u',r'\omega',r'\,dt',y=3.1)
        second=self.change(second,r'\lim_{dt\to0}\frac{|d\vec u|}{dt}','=',r'\omega','u',size=34)
        a2=self.change(second,'a_2','=',r'\omega','u',y=2)
        self.checkpoint('10 segunda contribuição',1)
        self.out(oldrod,uref,dv,dvlabel,theta,thlabel,threl,desc2)

        # Glyph map apenas na fusão de dois termos iguais, strings estabilizadas.
        self.play(a1.animate.move_to([-1.9,4.4,0]),a2.animate.scale(.8).move_to([1.9,4.4,0]),run_time=.8)
        total=eq(r'a_\perp','=','a_1','+','a_2',y=3,size=42)
        self.assemble(total,[(a1[0],2),(a2[0],4)])
        expanded=eq(r'a_\perp=\omega u+\omega u',y=3,size=42)
        self.play(FadeOut(total),TransformFromCopy(a1[2:],expanded[0][3:5]),
                  TransformFromCopy(a2[2:],expanded[0][6:8]),
                  Write(expanded[0][:3]),Write(expanded[0][5]),run_time=1)
        self.remove(*expanded[0]);self.add(expanded)
        fused=eq(r'a_\perp=2\omega u',y=3,size=46)
        assert len(expanded[0])==8 and len(fused[0])==6
        self.play(TransformByGlyphMap(expanded,fused,([0,1,2],[0,1,2]),
                  ([3,6],[4]),([4,7],[5]),([5],[]),([],[3]),auto_fade=True),run_time=1.4)
        self.remove(expanded); self.add(fused); fused[0][3].set_color(C)
        self.play(Indicate(fused[0][3],color=C,scale_factor=1.4),run_time=.7)
        self.checkpoint('08 nascimento do fator 2',1); self.out(a1,a2)

        # Coordenadas da tela = theta_laboratorio - theta_camera.
        self.play(fused.animate.scale(.75).move_to([0,5.3,0]),FadeOut(rotlabel),run_time=.7)
        scalar_note=text('o módulo está pronto; falta codificar a direção',y=4.55,size=20,color=M)
        crosscode=eq(r'\vec\omega',r'\times',r'\vec v',y=2.9,size=35)
        rotation_normal=symbol_into_screen(pivot+DOWN*.6,radius=.13,color=V)
        # Na haste, a rotação é anti-horária: normal saindo da tela (ponto).
        rotation_normal=VGroup(Circle(.13,color=V),Dot(radius=.035,color=V)).move_to(pivot+DOWN*.6)
        self.play(FadeIn(scalar_note),FadeIn(rotation_normal),run_time=.6)
        self.assemble(crosscode,[(omega,0),(uvec,2)])
        view=text('vista inercial',y=3.9,size=22,color=M); self.play(FadeIn(view),run_time=.5)
        cameraangle=ValueTracker(0)
        world=VGroup(*[Line(pivot+direction(k*PI/4)*.25,pivot+direction(k*PI/4)*4.8,
                           color=M,stroke_opacity=.2,stroke_width=1) for k in range(8)])
        world0=world.copy()
        world.add_updater(lambda m:m.become(world0.copy().rotate(-cameraangle.get_value(),about_point=pivot)))
        for mob in [rod,bead,uvec]: mob.clear_updaters()
        rod.add_updater(lambda m:m.put_start_and_end_on(pivot,pivot+5.6*direction(angle.get_value()-cameraangle.get_value())))
        bead.add_updater(lambda m:m.move_to(pivot+radius.get_value()*direction(angle.get_value()-cameraangle.get_value())))
        uvec.add_updater(lambda m:m.become(arrow(bead.get_center(),bead.get_center()+direction(angle.get_value()-cameraangle.get_value()),B)))
        acc=always_redraw(lambda:arrow(bead.get_center(),bead.get_center()+1.15*direction(angle.get_value()-cameraangle.get_value()+PI/2),W))
        self.add(world,acc)
        self.play(angle.animate.increment_value(.35),radius.animate.set_value(3.5),run_time=1.8)
        self.checkpoint('09a vista inercial',.5)
        self.play(cameraangle.animate.set_value(angle.get_value()),
                  Transform(view,text('vista que gira com a haste',y=3.9,size=22,color=C)),
                  FadeOut(rot),FadeOut(omega),run_time=1.6)
        self.play(angle.animate.increment_value(.25),cameraangle.animate.increment_value(.25),
                  radius.animate.set_value(3.85),run_time=1.5)
        self.checkpoint('09b haste parada / mundo girando',.5)
        acc.clear_updaters()
        self.play(Transform(acc,arrow(bead.get_center(),bead.get_center()+DOWN*1.15,C)),run_time=.9)
        opposite=eq('-',x=1.65,y=-2.1,size=36,color=C)
        self.play(Write(opposite),run_time=.4)
        acsym=eq(r'\vec a_C',x=2.2,y=-2.2,size=30,color=C)
        aclabel=text('aceleração de Coriolis',y=-3.5,x=1.2,size=21,color=C,width=5.5)
        self.play(Write(acsym),FadeIn(aclabel),run_time=.7)
        general=eq(r'\vec a_C','=','-','2',r'\vec\omega',r'\times',r'\vec v',y=2.3,size=43)
        self.assemble(general,[(acsym,0),(opposite,2),(fused[0][3],3),
                               (crosscode[0],4),(crosscode[1],5),(crosscode[2],6)])
        self.out(scalar_note,crosscode,opposite,rotation_normal,time=.4)
        dirlabel=text('perpendicular à rotação e à velocidade relativa',y=1.3,size=20,color=M)
        self.play(Indicate(general[2],color=C),FadeIn(dirlabel),run_time=.7)
        self.checkpoint('10 fórmula de Coriolis conquistada',1)

        # A haste se torna a estrutura da torre; a fórmula persiste.
        for mob in [rod,bead,uvec,world]: mob.clear_updaters()
        tower,release=build_torre(x_c=-2.1,y_solo=-4.7,y_topo=.8,w_base=.9,w_topo=.35)
        ground=Line([-4,-4.7,0],[4,-4.7,0],color=M,stroke_width=2)
        self.play(ReplacementTransform(rod,tower),hub.animate.move_to([-2.1,-4.7,0]).scale(.6),
                  FadeOut(world),FadeOut(bead),FadeOut(uvec),FadeOut(acc),FadeOut(acsym),FadeOut(aclabel),
                  FadeOut(fused),FadeOut(dirlabel),FadeOut(view),FadeIn(ground),
                  general.animate.scale(.78).move_to([0,5.7,0]),run_time=1.3)
        origin=np.array([release,-4.7,0]); top=np.array([release,.8,0])
        plumb=DashedLine(top,origin,color=W,stroke_opacity=.4,dash_length=.12)
        below=Dot(origin,color=W,radius=.06); ball=glowing_ball(top)
        ex=arrow(origin,origin+RIGHT*3.2,C); ez=arrow(origin,origin+UP*1.3,W)
        north=symbol_into_screen(origin+LEFT*1.2+DOWN*.5,radius=.13)
        axes=VGroup(ex,ez,north,eq(r'+x=\text{leste}',x=1.5,y=-5.1,size=24,color=C),
                    eq(r'+z=\text{cima}',x=-.65,y=-3.9,size=22),
                    eq(r'+y=\text{norte}',x=-1.8,y=-5.7,size=22,color=V))
        earthomega=eq(r'\vec\omega_T','=',r'\omega_T\hat y',x=1.1,y=-2.8,size=28,color=V,width=4.5)
        vzero=eq(r'\vec v(0)','=','0',x=.1,y=.8,size=30,color=B,width=3)
        self.play(Create(plumb),FadeIn(ball),FadeIn(below),FadeIn(axes),Write(earthomega),Write(vzero),run_time=1.1)
        self.checkpoint('11 referencial local ancorado à torre',.5)
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
        notice=text('DESVIO EXAGERADO',y=-2.3,x=.8,size=15,color=P,width=3)
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
        vx=self.change(integral,'v_x(t)','=',r'\omega_T','g',r't^2',y=2.7)
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
        height=eq('h','=','50',r'\,\mathrm m',x=-3.75,y=-1.9,size=24,width=1.05)
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
        payoff=self.change(num,'x_f',r'\approx','0{,}77',r'\,\mathrm{cm}',y=2,size=49,color=C)
        box=SurroundingRectangle(payoff,color=C,buff=.22,stroke_width=2)
        east2=text('PARA LESTE',y=1.05,size=26,color=C)
        self.play(Create(box),FadeIn(east2),run_time=.6); self.checkpoint('21 payoff',1.2)
        self.out(displacement,wvalue,gravity,timevalue,payoff,box,east2)

        # Mesma curva, mesmo t: S -> 1. Sem segunda trajetória.
        self.play(exaggeration.animate.set_value(1),FadeOut(notice),run_time=2.5)
        self.checkpoint('22 escala física real',.7)
        ball.clear_updaters(); path.clear_updaters()
        insetcenter=np.array([1.5,-1.6,0]); inset=Circle(1.6,color=C,stroke_width=2,
                    fill_color='#0A1630',fill_opacity=1).move_to(insetcenter)
        pwhite=insetcenter+LEFT*.8+DOWN*.45; pcyan=insetcenter+RIGHT*.8+DOWN*.45
        insetgroup=VGroup(inset,text('AMPLIAÇÃO',x=1.5,y=-.5,size=20),
             Line(insetcenter+[-1.35,-.45,0],insetcenter+[1.35,-.45,0],color=M),
             DashedLine(pwhite+UP*.6,pwhite,color=W,dash_length=.08,stroke_width=1.5),
             Dot(pwhite,color=W,radius=.07),Dot(pcyan,color=C,radius=.07),
             arrow(pwhite+UP*.3,pcyan+UP*.3,C),eq(r'7{,}7\,\mathrm{mm}',x=1.5,y=-1.1,size=33,color=C),
             eq(r'0{,}77\,\mathrm{cm}',x=1.5,y=-2.55,size=24,color=C))
        leader=VMobject(color=C,stroke_width=1.5).set_points_as_corners([
                     position(tf),[-.2,-4.2,0],insetcenter+DOWN*1.6])
        self.play(Create(leader),FadeIn(insetgroup),run_time=1.2)
        self.checkpoint('23 ampliação ligada ao impacto',2); self.out(insetgroup,leader)
        self.play(VGroup(tower,ground,plumb,below,ball,path,axes,hub).animate.set_opacity(.13),run_time=.7)
        end1=text('A OLHO NU,',y=3.8,size=30); end2=text('A QUEDA PARECE VERTICAL.',y=3,size=29)
        end3=text('MAS ELA TERMINA',y=1.6,size=23)
        end4=text('ALGUNS MILÍMETROS A LESTE.',y=.9,size=27,color=C)
        final=eq(r'50\,\mathrm m',r'\longrightarrow',r'0{,}77\,\mathrm{cm\ para\ leste}',y=-.5,size=35)
        self.play(Write(end1),Write(end2),run_time=1)
        self.play(Write(end3),Write(end4),run_time=1.2); self.play(Write(final),run_time=1)
        self.checkpoint('24 fechamento',4)
        (UNIT/'qa_v5_timestamps.json').write_text(json.dumps(self.qa,ensure_ascii=False,indent=2),encoding='utf-8')

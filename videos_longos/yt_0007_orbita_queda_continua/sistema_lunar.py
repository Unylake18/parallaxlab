"""Identificação, mecanismo e baricentro, mantendo os centros em escala."""
import math
import numpy as np
from manim import *
from modelo_orbital import R_T, integrar
from geometria_visual import globo
from superficie import lua_visual
from matematica_visual import formula, BLUE, CYAN, VIOLET, WHITE
from cena_v1 import texto, seta


class SistemaLunar:
    def n16(self):
        self.titulo('A mesma lei gravitacional')
        self.mostrar_montanha=False; self.mostrar_bola=True
        theta=.12; r=R_T+25
        self.orb=integrar(r*np.array([np.sin(theta),np.cos(theta)]),[0,0],4,dt=.01)
        self.loop=False; self.tracar=False; self.tau.set_value(0); self.path_alpha.set_value(0)
        self.escrever('pedra · novo caso, escala local',(0,2.15),24,WHITE)
        foco=(R_T+12)*np.array([np.sin(theta),np.cos(theta)])/R_T
        self.olhar(foco[0],foco[1],.000013,roll=theta,dur=2.5)
        self.voo(2.8,None,False); self.marco('N16_pedra'); self.wait(.7)
        self.limpar(); self.escrever('satélite · escala orbital',(0,2.15),24,WHITE)
        self.configurar(R_T+400e3,1); self.loop=True; self.tracar=False; self.path_alpha.set_value(1)
        self.olhar(0,0,7,dur=2.7)
        self.play(self.tau.animate.set_value(.7*self.orb.t[-1]),run_time=4,rate_func=linear)
        self.marco('N16_satelite'); self.limpar(); self.titulo('A Lua também está caindo.')
        self.escrever('Terra–Lua · mudança de sistema e escala',(0,2.15),22,VIOLET)
        self.mostrar_bola=False; self.phase=ValueTracker(-.18)
        self.d=384.4e6/R_T; self.rb=4.67e6/R_T
        self.unit_lua=lambda:np.array([math.cos(self.phase.get_value()),math.sin(self.phase.get_value())])
        self.lua_centro=lambda:self.d*self.unit_lua()
        self.lua_amp=ValueTracker(.65); self.earth_marker.set_value(.80)
        self.lua=always_redraw(lambda:lua_visual(self.cam.p(self.lua_centro()),max(.2727*self.cam.k,self.lua_amp.get_value())))
        self.add(self.lua); self.path_alpha.set_value(0)
        self.olhar(self.d/2,0,90,incl=.75,dur=3)
        self.limpar()
        terra_nome=texto('Terra',29,BLUE).set_z_index(100)
        terra_nome.add_updater(lambda m:m.move_to(self.cam.p(self.earth_center())+[0,-max(self.cam.k,self.earth_marker.get_value())-.28,0]))
        lua_nome=texto('Lua',30,WHITE).set_z_index(100)
        lua_nome.add_updater(lambda m:m.move_to(self.cam.p(self.lua_centro())+[.2,-max(.2727*self.cam.k,self.lua_amp.get_value())-.28,0]))
        self.play(FadeIn(terra_nome),run_time=.6); self.play(FadeIn(lua_nome),run_time=.6)
        self.overlays.extend([terra_nome,lua_nome])
        self.escrever('tamanhos ampliados · centros em escala · vista oblíqua',(0,-2.75),20,VIOLET)
        self.marco('N16_lua_identificada'); self.wait(1)
        raio_lua=lambda:max(.2727*self.cam.k,self.lua_amp.get_value())
        def velocidade():
            u=self.unit_lua(); pp=self.cam.p(self.lua_centro())
            v=self.cam.p(self.lua_centro()+np.array([-u[1],u[0]]))-pp
            return seta(pp,pp+(raio_lua()+.8)*v/max(np.linalg.norm(v),1e-8),WHITE,4).set_z_index(45)
        def gravidade():
            pp=self.cam.p(self.lua_centro()); d=self.cam.p(self.earth_center())-pp
            return seta(pp,pp+(raio_lua()+1.0)*d/max(np.linalg.norm(d),1e-8),CYAN,4).set_z_index(45)
        vv=always_redraw(velocidade); gg=always_redraw(gravidade)
        vnome=texto('velocidade',22,WHITE).set_z_index(100)
        vnome.add_updater(lambda m:m.move_to(np.array([vv.get_end()[0]+1.0,min(2.3,max(-2.5,vv.get_end()[1]+.1)),0])))
        gnome=texto('atração da Terra',22,CYAN).set_z_index(100)
        gnome.add_updater(lambda m:m.move_to(np.array([gg.get_end()[0]-.3,min(2.3,max(-2.5,gg.get_end()[1]-.45)),0])))
        self.add(vv,gg,vnome,gnome)
        self.play(self.phase.animate.set_value(.16),run_time=6,rate_func=linear)
        self.marco('N16_lua_velocidade_gravidade'); self.wait(1)
        self.play(*[FadeOut(x) for x in (vv,gg,vnome,gnome)],run_time=.6)
        self.olhar(self.d/2,0,110,incl=.75,dur=2)
        self.play(self.earth_marker.animate.set_value(.30),self.lua_amp.animate.set_value(.13),run_time=1)
        self.marco('N16_terra_lua'); self.wait(1)

    def n17(self):
        self.limpar(); self.titulo('A Terra também se move.')
        self.olhar(0,0,7.5,incl=0,dur=2.2)
        self.earth_marker.set_value(0); self.lua_amp.set_value(.055)
        # Continuidade de coordenadas: os dois centros conservam a posição
        # inicial; B passa a ser o ponto fixo do referencial do centro de massa.
        self.B=self.rb*self.unit_lua().copy()
        self.earth_center=lambda:self.B-self.rb*self.unit_lua()
        self.lua_centro=lambda:self.B+(self.d-self.rb)*self.unit_lua()
        self.escrever('A Terra também responde à atração da Lua.',(0,-2.65),25,CYAN)
        self.play(self.phase.animate.increment_value(.4),run_time=2.2,rate_func=linear)
        centro=always_redraw(lambda:Dot(self.cam.p(self.earth_center()),.06,color=WHITE).set_z_index(50))
        linha_c=always_redraw(lambda:Line([-3.3,1.0,0],self.cam.p(self.earth_center()),color=WHITE,stroke_width=1.4).set_z_index(50))
        self.play(FadeIn(centro),Create(linha_c),run_time=.5)
        self.escrever('centro da Terra',(-4.4,1.3),25,WHITE); self.wait(.8)
        def cruz(p):
            return VGroup(Line(p+[-.09,0,0],p+[.09,0,0],color=CYAN,stroke_width=3),
                          Line(p+[0,-.09,0],p+[0,.09,0],color=CYAN,stroke_width=3)).set_z_index(55)
        bar=always_redraw(lambda:cruz(self.cam.p(self.B)))
        linha_b=always_redraw(lambda:Line([3.2,1.0,0],self.cam.p(self.B),color=CYAN,stroke_width=1.4).set_z_index(50))
        self.play(FadeIn(bar),Create(linha_b),run_time=.6)
        self.escrever('baricentro',(4.0,1.3),25,CYAN); self.wait(1)
        self.marco('N17_centros_nomeados')
        self.play(self.phase.animate.increment_value(.45),run_time=2.8,rate_func=linear)
        self.play(*[FadeOut(x) for x in (centro,linha_c,bar,linha_b)],run_time=.6); self.limpar()
        self.play(self.cam.ax.animate.set_value(-2.8),run_time=.7)
        self.olhar(self.B[0],self.B[1],13.6*(self.d-self.rb)/4.2,incl=1.14,dur=2)
        bary=always_redraw(lambda:cruz(self.cam.p(self.B)).scale(.5))
        ang=np.linspace(0,TAU,500)
        orbit=self.B+np.column_stack([(self.d-self.rb)*np.cos(ang),(self.d-self.rb)*np.sin(ang)])
        guia=always_redraw(lambda:self.cam.linha(orbit,VIOLET,1.4,ocultar=False))
        foco=always_redraw(lambda:Circle(radius=.15,color=VIOLET,stroke_width=1.5).move_to(self.cam.p(self.earth_center())).set_z_index(50))
        bc=np.array([4.,.15,0]); R=1.0
        uv=lambda:np.r_[self.unit_lua(),0]
        ec=lambda:bc-R*self.rb*uv()
        terra_zoom=Group()
        def atualizar_zoom(m):
            m.remove(*m.submobjects)
            m.add(globo(ec(),R))
        terra_zoom.add_updater(atualizar_zoom,call_updater=True)
        raio=always_redraw(lambda:Line(ec(),bc,color=VIOLET,stroke_width=3).set_z_index(45))
        centro2=always_redraw(lambda:Dot(ec(),.045,color=WHITE).set_z_index(50))
        bar2=cruz(bc)
        ligacao=always_redraw(lambda:DashedLine(self.cam.p(self.earth_center())+.15*RIGHT,[2,.15,0],color=VIOLET,dash_length=.12,stroke_width=1).set_z_index(5))
        nome_c=texto('centro da Terra',21,WHITE).move_to([2.7,-2.2,0]).set_z_index(100)
        lc=always_redraw(lambda:Line([2.7,-1.98,0],ec(),color=WHITE,stroke_width=1).set_z_index(45))
        nome_b=texto('baricentro',21,CYAN).move_to([5.5,-2.2,0]).set_z_index(100)
        lb=Line([5.5,-1.98,0],bc,color=CYAN,stroke_width=1).set_z_index(45)
        lua_nome=texto('Lua',20,WHITE).set_z_index(100)
        def seguir_lua(m):
            pos=self.cam.p(self.lua_centro())
            m.move_to(pos+[.35,.15,0])
        lua_nome.add_updater(seguir_lua)
        self.add(bary,guia,foco,ligacao,terra_zoom,raio,centro2,bar2,nome_c,lc,nome_b,lb,lua_nome)
        self.escrever('vista oblíqua · marcadores ampliados',(-2.8,2.15),19,VIOLET)
        self.escrever('distâncias entre centros em escala',(-2.8,-2.15),19,VIOLET)
        self.escrever('ampliação · vista perpendicular',(4,2.4),19,VIOLET)
        medida_rb=self.math(r'r_b\approx0{,}733R_T',(4,-2.72),30)
        self.play(self.phase.animate.increment_value(TAU),run_time=11,rate_func=linear)
        self.marco('N17_baricentro_mesmo_sistema')
        extras=[m for m in self.overlays if m is not self.lua]
        self.play(*[FadeOut(m) for m in extras if m is not self.cabecalho],run_time=.5); self.overlays=[]
        self.escrever('Terra e Lua caem uma em direção à outra\ne orbitam um ponto comum.',(-3.2,-2.6),25,WHITE)
        self.wait(2)
        objetos=(bary,guia,foco,ligacao,terra_zoom,raio,centro2,bar2,nome_c,lc,nome_b,lb,lua_nome,self.lua)
        for m in objetos: m.clear_updaters(recursive=True)
        self.play(*[FadeOut(x) for x in objetos],run_time=.8)
        self.limpar(); self.earth_center=lambda:np.zeros(2)

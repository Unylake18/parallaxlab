"""Kit local 25: projeção, física, vetores 3D, escrita e glyph maps."""
from pecas22 import *
import fisica25 as F
import kit as K25
import re
import hashlib
from collections import defaultdict
from functools import lru_cache

SOURCE_HASH=hashlib.sha256(b''.join((AQUI/n).read_bytes() for n in ['kit.py','prob.py','prob2.py','pecas22.py','pecas25.py','cenas25.py','conteudo25.py','fisica25.py','latex25.py','transicoes25.py','auditoria25.py','telemetria25.py'])).hexdigest()[:16]

_T_original=T
_txt_original=txt
@lru_cache(maxsize=256)
def _T_cache(s,size,cor):return _T_original(s,size,cor)
def T(s,size=40,cor=None):
    m=_T_cache(s,size,cor).copy();m._tam=size;return m
@lru_cache(maxsize=128)
def _txt_cache(s,size,color,op,bold):return _txt_original(s,size,color,op,bold)
def txt(s,size=34,color=WHITE_,op=1.,bold=False):return _txt_cache(s,size,color,op,bold).copy()

def txtc(s,size,cores):
    s=s.upper();m=screen_text(s,size,color=WHITE_,oversample=4 if len(s)<34 else 2,t2c=cores)
    m._tam=size;m._s=s;m._bold=False;return m

K25.LETRA_COR.update({r'\rho':VETC,r'\ell':VETC,'z':VETC,r'\alpha':ANG})
K25._SIMB=list(dict.fromkeys([*K25._SIMB,r'\rho',r'\ell']))

def camd(az,el,alvo,k,xc=-3.85,yc=-.65,fov=43.6):
    return dict(az=az,el=el,alvo=list(alvo),K=k,xc=xc,yc=yc,fov=fov)

CAMS={'P_34':camd(35,18,(0,0,-.48),2.45,fov=math.degrees(2*math.atan((35/(16/9))/(2*35)))),'V_34':camd(30,22,(0,0,0),6.2,yc=-.55),
      'H_34':camd(35,20,(0,0,-.28),3.25,yc=-.4), 'H_LADO':camd(-90,0,(0,0,-.28),3.25,yc=-.4,fov=0),
      'R_34':camd(55,25,(0,0,-.17),4.0,yc=-.55)}

ESC_V=.40/max(np.linalg.norm(F.voxel(0)['L']),np.linalg.norm(F.voxel(0,1)['L']))
ESC_LI=.15/np.linalg.norm(F.voxel(0)['L1'])

def proj(c,p,detalhes=False):
    a,e=math.radians(c['az']),math.radians(c['el'])
    d=np.array([math.cos(e)*math.cos(a),math.cos(e)*math.sin(a),math.sin(e)])
    up=np.array([-math.sin(e)*math.cos(a),-math.sin(e)*math.sin(a),math.cos(e)])
    fw=-d;right=np.cross(fw,up);right/=np.linalg.norm(right);up=np.cross(right,fw)
    al=np.array(c['alvo']);q=np.asarray(p)-al
    if c['fov']>0:
        th=math.tan(math.radians(c['fov'])/2);dist=4.5/c['K']/th
        depth=dist+q@fw;k=c['K']*dist/depth
    else: depth,k=10+q@fw,c['K']
    m=P3(c['xc']+k*(q@right),c['yc']+k*(q@up))
    return (m,depth,k/c['K']) if detalhes else m

def px(p,w=960,h=540):return [(p[0]+8)*w/16,(4.5-p[1])*h/9]

def tokens(s):return re.split(r'(?<!\\)\|',s)

def Mx(s,size=46,acc=False,cores=None):
    p=tokens(s);cs={}
    for i,t in enumerate(p):
        if t.strip() in (r'\alpha','\alpha^2'):cs[i]=ACC if acc else ANG
        if t.strip()=='d' and 'F' in s:cs[i]=GEO
        if t.strip()==r'\hat z':cs[i]=WHITE_
        if t.strip() in ('mxz','myz'):cs[i]=MAS
    cs.update(cores or {})
    m,idx=M(*p,size=size,cores=cs)
    m._gl=list(zip(p,idx))
    for g in m[0]:
        if g.height<.035 and g.width>.18:g.set_color(WHITE_)
    # Substituições dentro de frações/raízes conservam a família sem colorir barras e operadores.
    conhecidos={'9{,}8':ACC,'1{,}00':VETC,'30':ANG,'0{,}5':ANG,'0{,}30':VETC,'0{,}40':MAS,'27{,}8':VEL,'92{,}6':VEL,'0{,}020':MAS,'0{,}20':VETC,'1{,}23':FC,'2{,}37':FC,'0{,}52':GEO,'100':VEL}
    for parte,ids in zip(p,idx):
        if r'\mathrm' in parte:continue
        nums=list(re.finditer(r'\d+(?:\{,\}\d+)?',parte))
        if not nums or not any(n.group() in conhecidos for n in nums):continue
        dig=[j for j in ids if (K25._id_glifo(m[0][j]) or ('',0))[0] in '0123456789' and (K25._id_glifo(m[0][j]) or ('',0))[0]]
        if len(dig)!=sum(sum(c.isdigit() for c in n.group()) for n in nums):continue
        k=0;anterior=None
        for n in nums:
            nn=sum(c.isdigit() for c in n.group());gr=dig[k:k+nn];k+=nn
            cor=conhecidos.get(n.group())
            if n.group()=='0{,}40' and r'\frac{1{,}23}' in parte:cor=GEO
            if n.start()>0 and parte[n.start()-1]=='^':cor=anterior
            if cor:
                for j in range(gr[0],gr[-1]+1):m[0][j].set_color(cor)
            anterior=cor
        for j in ids:
            if m[0][j].height<.035 and m[0][j].width>.18:m[0][j].set_color(WHITE_)
    m._tam=float(m.font_size)
    for parte,ids in zip(p,idx):
        if parte==r'2\pi':
            for j in ids:m[0][j].set_color(VEL)
        elif parte==r'(2\pi)^2':
            for j in ids[1:3]+ids[-1:]:m[0][j].set_color(VEL)
    return m,idx

@lru_cache(maxsize=128)
def _rotulo_modelo(tex,cor):
    if tex.startswith('@'):return txt(tex[1:],30,cor),None
    if '|' not in tex:return T(tex,36,cor),None
    parts=tokens(tex)
    cores={i:cor for i,p in enumerate(parts) if p not in ('=','+','-',r'\hat z') and r'\mathrm' not in p}
    cores.update({i:WHITE_ for i,p in enumerate(parts) if p==r'\hat z'})
    return M(*parts,size=36,cores=cores)

def rotulo_modelo(tex,cor):
    m,idx=_rotulo_modelo(tex,cor)
    return m.copy(),idx

def sublinha(m,cor):
    return Line(m.get_corner(DL)+DOWN*.11,m.get_corner(DR)+DOWN*.11).set_stroke(cor,3)

def vetor3(c,a,b,cor,trace=False,w=5,ocultos=None):
    a,b=np.asarray(a),np.asarray(b);pa,pb=proj(c,a),proj(c,b)
    if np.linalg.norm(pb-pa)<.025:return VGroup()
    persp=proj(c,b,True)[2];tip=.17*np.clip(persp,.8,1.2)
    if ocultos is None:
        if trace:return VGroup(DashedLine(pa,pb,dash_length=.09,dashed_ratio=.65).set_stroke(cor,w),Triangle().scale(tip*.52).rotate(math.atan2(pb[1]-pa[1],pb[0]-pa[0])-PI/2).move_to(pb).set_fill(cor,1).set_stroke(width=0))
        return VGroup(Arrow(pa,pb,buff=0,stroke_width=w*np.clip(persp,.8,1.2),tip_length=tip,max_tip_length_to_length_ratio=.18,color=cor))
    pts=[proj(c,a+(b-a)*u) for u in np.linspace(0,1,25)]
    g=VGroup()
    for j in range(24):
        hidden=ocultos.get(str(j+1),False)
        if hidden or trace:
            if j%2==0:
                seg=Line(pts[j],pts[j+1]).set_stroke(cor,w,opacity=.35 if hidden else 1)
                seg._oclusao25=hidden;g.add(seg)
        else:
            seg=Line(pts[j],pts[j+1]).set_stroke(cor,w);seg._oclusao25=False;g.add(seg)
    g.add(Triangle().scale(tip*.52).rotate(math.atan2(pb[1]-pa[1],pb[0]-pa[0])-PI/2).move_to(pb).set_fill(cor,.35 if ocultos.get('24') else 1).set_stroke(width=0))
    return g

class Fundo25(Fundo3D):
    def _quadro(self):
        if self.cena!=self.cm.tipo and not (self.cm._aid=='S2' and getattr(self.cm,'_s2duplo',False) and self.cena=='haltere_torto'):
            self.img.pixel_array[...,3]=(self.alfa*np.clip(self.op.get_value(),0,1)+.5).astype(np.uint8)
            return self
        return super()._quadro()

class Lote25(Lote22):
    TITULO='MECÂNICA · MOMENTO ANGULAR DO CORPO RÍGIDO'
    def setup_base(self,cap=None,selo=None):
        super().setup_base(cap,selo)
        print(f'[fonte] {SOURCE_HASH}',flush=True)
        offsets=AQUI/'offsets.json'
        if offsets.exists():
            glob=json.loads(offsets.read_text(encoding='utf-8')).get(self.lote,0)
            self.remove(self.poeira)
            self.poeira=poeira_estelar(self.clk,t0=lambda:glob)
            self.add(self.poeira)
        self.pilha=Pilha(self,x0=.75,topo=2.25,base=-3.3,buff=.34,larg=6.5)
        self.tipo='pendulo_conico';self.camera25=dict(CAMS['P_34'])
        self.ph0=0.;self.c0=0.;self.vel=0.;self.cam_u=ValueTracker(0);self.u=ValueTracker(0);self.x=ValueTracker(0);self.bal=ValueTracker(0);self.etapa=ValueTracker(0);self.etapa_h=ValueTracker(0);self.soma_final=ValueTracker(0);self.add(self.u,self.x,self.bal,self.etapa,self.etapa_h,self.soma_final,self.cam_u)
        self.flags={};self.cam_a=self.cam_b=None;self.vetores={};self.rotulos={};self.decoracoes=[];self.reg_alg=[]
        self.fundos={};self.layer=vivo(self.desenho).set_z_index(15);self.add(self.layer)
        self._timeline={};self._geometrias=[]
        self.inicios_real={}
        self.inicios_play={}

    def an(self,aid):
        super().an(aid)
        self.inicios_real[aid]=self.nq/FPS
        self.inicios_play[aid]=self.renderer.num_plays

    def phi(self):return self.ph0+self.vel*(self.clk.get_value()-self.c0)
    def anda(self,vel,phi=None):
        p=self.phi() if phi is None else phi
        self.ph0,self.c0,self.vel=p,self.clk.get_value(),vel
    def cam(self):
        if self.cam_a is None:
            c=dict(self.camera25)
            if self._aid=='S1':c['az']+=8*(self.clk.get_value()-self._q0/FPS)
            return c
        u=self.cam_u.get_value();a,b=self.cam_a,self.cam_b
        if u>=1:return b
        c={k:a[k]+(b[k]-a[k])*u for k in ('az','el','K','xc','yc')}
        c['alvo']=[a['alvo'][i]+(b['alvo'][i]-a['alvo'][i])*u for i in range(3)]
        c['fov']=math.exp(math.log(a['fov'] or .12)*(1-u)+math.log(b['fov'] or .12)*u)
        return c
    def dolly(self,nome,rt=1.5):
        self.cam_a,self.cam_b=dict(self.cam()),dict(CAMS[nome]);self.cam_u.set_value(0)
        self.play(self.cam_u.animate.set_value(1),run_time=rt)
        self.camera25=self.cam_b;self.cam_a=None

    def modelo(self):
        p=self.phi()
        if self.tipo=='pendulo_conico':return F.pendulo(p)
        if self.tipo=='haltere_torto':return F.haltere(p,self.x.get_value(),3 if self._aid=='B5-5' else 1)
        if self.tipo=='corpo_voxel':
            if self._aid=='S2':
                esc,fase,w=F.deformacao(self.clk.get_value()-self._q0/FPS)
                return F.voxel(fase,1)
            return F.voxel(p,round(self.u.get_value(),5))
        return F.roda(p,self.bal.get_value())

    def prepara(self,tipo,cam,vel=0,phi=0,**flags):
        anterior=self.fundos.get(self.tipo)
        self.tipo=tipo;self.camera25=dict(CAMS[cam] if isinstance(cam,str) else cam);self.cam_a=None;self.anda(vel,phi)
        self.flags=flags;self.vetores={};self.rotulos={};self.etapa.set_value(0)
        if tipo not in self.fundos:
            f=Fundo25(self,tipo,lambda t,n=tipo:self.estado(n));self.fundos[tipo]=f;self.add(f)
        novo=self.fundos[tipo]
        for k,f in self.fundos.items():
            if f is not anterior:f.op.set_value(0 if k!=tipo else (0 if anterior is not None and anterior is not novo else 1))
        if anterior is not None and anterior is not novo:
            self.play(anterior.op.animate.set_value(0),novo.op.animate.set_value(1),run_time=.5)

    def especifica(self):
        e=self.modelo();O=e['O'];r=e['massa'];out={}
        for nome,d in self.vetores.items():
            base,vet,esc,cor,tr=d
            a=np.array(base(e) if callable(base) else base,float)
            vv=np.array(vet(e) if callable(vet) else (e[vet] if isinstance(vet,str) else vet),float)
            out[nome]=(a,a+esc*vv,cor,tr)
        return out

    def estado(self,nome=None):
        if nome=='haltere_torto' and self._aid=='S2':
            return r4(dict(tipo=nome,cam=dict(CAMS['H_34'],K=2.1,xc=-4.4,yc=-.55),phi=self.phi(),pontos={},movendo=True))
        e=self.modelo();pontos={'O':e['O'].tolist(),'massa':e['massa'].tolist()}
        for k in ('massa2','L','transversal','axial','torque','v','r'):
            if k in e:pontos[k]=e[k].tolist()
        for seta_nome,(a,b,cor,tr) in self.especifica().items():
            for j,u in enumerate(np.linspace(0,1,25)):pontos[f'{seta_nome}:{j}']=(a+(b-a)*u).tolist()
        est=dict(tipo=self.tipo,cam=self.cam(),phi=self.phi(),pontos=pontos,cone=False,plano=False,rastro=False,movendo=self.vel!=0,t_global=(self._off or 0)/FPS+self.clk.get_value())
        est.update(self.flags)
        est.update(x=self.x.get_value(),balanceada=self.bal.get_value(),rotacao=e.get('rotacao',np.eye(3)).tolist(),destaque=self.flags.get('destaque',False))
        est['onda_u']=self.etapa.get_value() if self._aid=='B2-4' else 0
        if self._aid=='S2':
            est['expansao'],est['phi'],est['omega_deformavel']=F.deformacao(self.clk.get_value()-self._q0/FPS)
            est['livre']=True
        return r4(est)

    def seta25(self,nome,base,vet,esc,cor,trace=False):
        self.vetores[nome]=(base,vet,esc,cor,trace)

    def desenho(self):
        if not hasattr(self,'vetores'):return VGroup()
        g=VGroup();c=self.cam()
        frame=round(self.clk.get_value()*FPS)
        timeline=self._timeline.get(self.tipo,{}) if hasattr(self,'_timeline') else {}
        oc=timeline.get(str(frame),{}).get('pontos',{})
        for nome,(a,b,cor,tr) in self.especifica().items():
            ocultos={str(j):oc.get(f'{nome}:{j}',{}).get('oculto',False) for j in range(25)} if oc else None
            g.add(vetor3(c,a,b,cor,tr,ocultos=ocultos))
        pontos_setas=g.get_all_points()
        e=self.modelo();usados=[];self._rotulos_atuais={}
        decor=[fn(e,c) for fn in self.decoracoes]
        ocupados=[(d.get_left()[0]-.18,d.get_bottom()[1]-.18,d.get_right()[0]+.18,d.get_top()[1]+.18) for d in decor if d.get_all_points().size]
        mask=None
        if not PEDIDOS3D:
            arq=DIR3D/'q3d'/f'{self.lote}_{config.pixel_width}x{config.pixel_height}'/self.tipo/'mascaras'/f'f{frame:05d}.png'
            cache_key=(str(arq),frame)
            if getattr(self,'_mask_cache_key',None)==cache_key:mask=self._mask_cache
            elif arq.exists():
                from PIL import Image
                from scipy.ndimage import maximum_filter
                mask=maximum_filter(np.asarray(Image.open(arq).convert('L')),size=max(1,round(2*.28*config.pixel_height/9)+1))>127
                self._mask_cache_key,self._mask_cache=cache_key,mask
        def livre25(m):
            (x0,y0,_),(x1,y1,_)=m.get_corner(DL),m.get_corner(UR)
            if x0< -7.4 or x1>-.35 or y0< -3.7 or y1>2.5:return False
            if any(min(x1,b[2])-max(x0,b[0])>.01 and min(y1,b[3])-max(y0,b[1])>.01 for b in usados):return False
            if any(min(x1,b[2])-max(x0,b[0])>.01 and min(y1,b[3])-max(y0,b[1])>.01 for b in ocupados):return False
            if len(pontos_setas) and ((pontos_setas[:,0]>x0-.20)&(pontos_setas[:,0]<x1+.20)&(pontos_setas[:,1]>y0-.20)&(pontos_setas[:,1]<y1+.20)).any():return False
            if mask is not None:
                w,h=config.pixel_width,config.pixel_height
                a=max(0,int((x0+8)*w/16));b=min(w,int((x1+8)*w/16)+1);cc=max(0,int((4.5-y1)*h/9));d=min(h,int((4.5-y0)*h/9)+1)
                if b>a and d>cc and mask[cc:d,a:b].any():return False
            return True
        for k,(texto,fn,cor,off) in self.rotulos.items():
            pos=proj(c,fn(e));m,_=rotulo_modelo(texto,cor)
            if not hasattr(self,'_offsets25'):self._offsets25={}
            chave=(self._aid,k,texto)
            m.move_to(pos+np.array(self._offsets25.get(chave,off)))
            if not livre25(m):
                achou=False
                for buff in (.26,.4,.55,.7,.9,1.1,1.35,1.6,1.9,2.2,2.5,2.8,3.1):
                    for lado in (UP,DOWN,LEFT,RIGHT,UL,UR,DL,DR):
                        m.next_to(Dot(pos,radius=.15),lado,buff=buff)
                        if livre25(m):achou=True;break
                    if achou:break
                if not achou:
                    candidatos=[P3(x,y) for x in np.linspace(-7.35+m.width/2,-.4-m.width/2,18) for y in np.linspace(-3.65+m.height/2,2.45-m.height/2,18)]
                    candidatos.sort(key=lambda p:np.linalg.norm(p-pos))
                    for p in candidatos:
                        m.move_to(p)
                        if livre25(m):achou=True;break
                if not achou and AUDITORIA:print(f'[audit] {self.clk.get_value():7.1f}s RÓTULO SEM VAGA {texto!r}')
            self._offsets25[chave]=m.get_center()-pos
            # A chamada liga o rótulo deslocado ao ponto que ele nomeia.
            alvo=Dot(pos,radius=.02)
            perto=m.get_boundary_point(pos-m.get_center())
            if np.linalg.norm(perto-pos)>.6 and k!='g':
                direcao=perto-pos;dist=np.linalg.norm(direcao)
                chamada=Line(pos,perto-.16*direcao/dist).set_stroke(GEO,1.3,opacity=.7)
                chamada._halo=True
                g.add(chamada)
            m._dono=alvo
            usados.append((m.get_left()[0]-.18,m.get_bottom()[1]-.18,m.get_right()[0]+.18,m.get_top()[1]+.18))
            self._rotulos_atuais[k]=m;g.add(m)
        g.add(*decor)
        return g

    def label(self,key,tex,fn,cor,offset=(0,.32,0)):
        # A posição candidata passa pelo mesmo rotulo() do kit. A camada viva mantém a horizontal.
        m,_=rotulo_modelo(tex,cor);p=proj(self.cam(),fn(self.modelo()));alvo=Dot(p,radius=.03)
        lado=np.array(offset);lado=lado/max(np.linalg.norm(lado),1e-9)
        r=self.rotulo(m,alvo,lados=(lado,UP,DOWN,LEFT,RIGHT,UL,UR,DL,DR),buffs=(.16,.28,.38),ignorar=(self.layer,),zona=(-7.4,-.35,-3.7,2.5),chamada=False)
        off=r[0].get_center()-p
        self.rotulos[key]=(tex,fn,cor,off)
        return m

    def alg(self,met,m,origem=None,voos=0):
        err=[];coloridos=0;grandezas=0
        ops={'=','+','-',r'\times',r'\cdot',r'\sum',r'\Rightarrow',r'\quad\Rightarrow\quad',r'\div',r'\propto',r'\ne',r'\approx'}
        for (parte,_),ids in zip(m._partes,getattr(m,'_indices25',[])):
            if parte in ops:
                if any(m[0][j].get_fill_color().to_hex().upper() not in (WHITE_.upper(),'#FFFFFF') for j in ids):err.append(parte)
            if r'\mathrm' in parte:continue
            for j in ids:
                ident=K25._id_glifo(m[0][j])
                if ident and ident[0] in K25.LETRA_COR and K25.LETRA_COR[ident[0]]:
                    grandezas+=1;coloridos+=m[0][j].get_fill_color().to_hex().upper() not in (WHITE_.upper(),'#FFFFFF')
        for g in m[0]:
            if g.height<.035 and g.width>.18 and g.get_fill_color().to_hex().upper() not in (WHITE_.upper(),'#FFFFFF'):err.append('barra')
        evento=dict(ancora=self._aid,metodo=met,tex=m.tex_string,origem=origem,voos=voos,t=self.nq/FPS,operadores_incorretos=err,grandezas=grandezas,coloridos=coloridos,font_size=float(m.font_size))
        self.reg_alg.append(evento);print('[alg]',json.dumps(evento,ensure_ascii=False))

    def escreve(self,s,src=None,met='escrita',voos=None,rt=2.,acc=False,cores=None,mapas=None,final=False,cor_final=LMAG):
        A,ia=Mx(s,size=52 if final else 46,acc=acc,cores=cores)
        A._indices25=ia
        self.pilha.poe(A)
        A._tam=float(A.font_size)
        self._linha_em_construcao25=A
        sub=sublinha(A,cor_final) if final else None
        if sub is not None:sub._resultado25=True;sub._risco=True
        extras=[Create(sub,run_time=rt,rate_func=lambda u:np.clip((u-.85)/.15,0,1))] if sub is not None else []
        if src is None or met!='GM':
            if src is not None and met=='MatchingTex':
                B,ib=src
                def segmenta(linha,indices):
                    partes=[t for t,_ in linha._partes]
                    seg=MathTex(*partes,font_size=float(linha.font_size))
                    for item,tex,ids in zip(seg,partes,indices):
                        item.submobjects=[linha[0][j].copy() for j in ids];item.tex_string=tex
                    return seg
                c,d=segmenta(B,ib),segmenta(A,ia)
                anim=TransformMatchingTex(c,d)
                self._equacao_em_voo25=A
                self._voando_raiz=[c,d,anim.mobject];self._voando={id(z) for r in self._voando_raiz for z in r.get_family()};self._fontes_extra=[B]
                self.play(anim,*extras,run_time=rt)
                self.remove(c,d,anim.mobject);self.add(A)
                self._voando_raiz=[];self._voando=set();self._fontes_extra=[]
                self._equacao_em_voo25=None
                self.alg('MatchingTex',A,B.tex_string)
            else:
                self._construcao25_rt=rt
                if extras:
                    pares=[(src_,mp(A,ia,[k])) for k,src_ in (voos or {}).items()]
                    resto=[k for k in range(len(ia)) if k not in (voos or {}) and ia[k]]
                    self.voa(pares,extra=extras,rt=min(rt,1.) if voos else rt,origem=False,arco_esq=-.5,escrever=[mp(A,ia,[k]) for k in resto],alvo=A)
                else:self.monta(A,ia,voos or {},rt=min(rt,1.) if voos else rt)
                self._construcao25_rt=None
                self.alg('voo' if voos else met,A,voos=len(voos or {}))
        else:
            B,ib=src
            if callable(mapas):mapas=mapas(B,ib,A,ia)
            if mapas is None:
                usados=set();mapas=[]
                for i,(t,_) in enumerate(B._partes):
                    for j,(u,_) in enumerate(A._partes):
                        if t==u and j not in usados:
                            mapas.append((ib[i],ia[j]));usados.add(j);break
            self._equacao_em_voo25=A
            self.passo(B,A,*mapas,rt=rt,extra=extras)
            self._equacao_em_voo25=None
            self.alg('GM',A,B.tex_string)
        if sub is not None:
            self.remove(sub);A.add(sub);A._sublinhado25=sub
        quantidade=3 if self._aid=='S1' else 2
        self.pilha.so(*[m for m,_ in self.pilha.linhas[-quantidade:]],rt=.25)
        self._linha_em_construcao25=None
        return A,ia

    def resultado(self,a,cor=LMAG):
        m=a[0] if isinstance(a,tuple) else a
        if getattr(m,'_sublinhado25',None) is not None:return
        s=sublinha(m,cor);self.play(Create(s),run_time=.3);self.remove(s);m.add(s)

    def quadro(self,aid):
        self.an(aid)
        self.vetores={};self.rotulos={};self.decoracoes=[]
        if aid not in ('B1-2','B1-4','B3-7'):self.pilha.limpa(rt=.4)
        linhas={m for m,_ in self.pilha.linhas}
        extras=[m for m in self.mobjects if m not in self.fixos() and m not in linhas and m is not self.layer and m is not self.s1 and m not in self.fundos.values() and not isinstance(m,ValueTracker)]
        if extras:self.play(*[FadeOut(m) for m in extras],run_time=.4)
        if self.s1 is not None:self.sem_selo()

    def fim(self):
        super().fim()
        (AQUI/f'algebra_{self.lote}.json').write_text(json.dumps(self.reg_alg,ensure_ascii=False,indent=1),encoding='utf-8')
        (AQUI/f'tempos_{self.lote}.json').write_text(json.dumps(dict(inicios=self.inicios_real,plays=self.inicios_play,total=self.nq/FPS),ensure_ascii=False,indent=1),encoding='utf-8')
        if AUDITORIA:(AQUI/f'qa/portao_{self.lote}.json').write_text(json.dumps(getattr(self,'_audit25',{})),encoding='utf-8')
        if AUDITORIA:
            from telemetria25 import salvar
            salvar(self)

    def update_to_time(self,t):
        super().update_to_time(t)
        if AUDITORIA:
            from telemetria25 import medir
            medir(self)

    def _auditar_v4(self,t,itens,objs,op,tams,fixos,nome):
        super()._auditar_v4(t,itens,objs,op,tams,fixos,nome)
        from auditoria25 import auditar
        auditar(self,t,itens,op)

    def construct(self):
        self.setup_base()
        if os.environ.get('CORRECAO_ANCORA25'):
            trace=(Path(os.environ['MEDIA_DIR'])/'frames_absolutos.txt').open('w',encoding='utf-8')
            original=self.renderer.file_writer.write_frame
            def escreve_frame25(frame,*args,**kw):
                n=kw.get('num_frames',args[0] if args else 1);f=round(self.clk.get_value()*FPS)
                trace.write(''.join(f'{f+j}\n' for j in range(n)));trace.flush()
                return original(frame,*args,**kw)
            self.renderer.file_writer.write_frame=escreve_frame25
        if not PEDIDOS3D and (not AUDITORIA or (os.environ.get('CORRECAO_ANCORA25') and config.from_animation_number==0)):
            from transicoes25 import instalar
            instalar(self,AQUI)
        if not PEDIDOS3D:
            for tipo in ('pendulo_conico','haltere_torto','corpo_voxel','roda_balanceamento'):
                p=DIR3D/'q3d'/f'{self.lote}_{config.pixel_width}x{config.pixel_height}'/tipo/'pontos.json'
                if p.exists():self._timeline[tipo]=json.loads(p.read_text(encoding='utf-8'))
        self.corpo();self.fim();self.relatorio()

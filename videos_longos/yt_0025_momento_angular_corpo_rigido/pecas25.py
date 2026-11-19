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

CAMS={'P_34':camd(35,18,(0,0,-.46),2.88,yc=-.08,fov=math.degrees(2*math.atan((35/(16/9))/(2*35)))),'P_CLOSE':camd(35,18,(0,0,-.22),6.0,yc=-.6,fov=math.degrees(2*math.atan((35/(16/9))/(2*35)))),'P_TOPO':camd(35,89,(0,0,0),6.0,yc=-.6,fov=0),'V_34':camd(30,22,(0,0,-.03),6.65,yc=-.6),'V_CLOSE':camd(30,22,(.1,.1,.12),11.0,yc=-.7),
      'H_34':camd(35,20,(0,0,-.02),7.0,yc=-.6),'H_34B':camd(35,20,(0,0,-.02),6.6,yc=-.6), 'H_LADO':camd(-90,0,(0,0,-.02),6.25,yc=-.6,fov=0),'H_TOPO':camd(35,89,(0,0,-.2),5.6,yc=-.6,fov=0),'H_MANCAL':camd(35,20,(0,0,-.38),3.2,yc=-.55,fov=0),
      'R_34':camd(12,18,(0,0,-.17),4.9,yc=-.55),'R_CLOSE':camd(12,18,(.05,.1,.0),9.5,yc=-.6),'R_AXIAL':camd(90,0,(0,0,-.02),6.5,yc=-.4,fov=0),'D_34':camd(35,18,(0,0,-.38),3.15,yc=-.3,fov=0),'D_S1':camd(35,18,(0,0,-.38),3.0,yc=-.3,fov=0),'PL_34':camd(35,25,(0,0,-.2),4.0,yc=-.38),'PL_TOPO':camd(35,82,(0,0,0),5.0,yc=-.6,fov=0)}

def mistura_cam(a,b,u):
    c={k:a[k]+(b[k]-a[k])*u for k in ('az','el','K','xc','yc')}
    c['alvo']=[a['alvo'][i]+(b['alvo'][i]-a['alvo'][i])*u for i in range(3)]
    if u>=1:c['fov']=b['fov']
    elif u<=0:c['fov']=a['fov']
    else:c['fov']=math.exp(math.log(a['fov'] or .12)*(1-u)+math.log(b['fov'] or .12)*u)
    return c

CHAO_Z={'pendulo_conico':-1.06,'haltere_torto':-1.05,'bancada_dupla':-1.115,'corpo_voxel':-1.05,'roda_balanceamento':-.49,'plataforma_livre':-.905}
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

def nota(s):
    """Notação v2 (handoff §1.4): sen (pt-BR), módulo de uma barra, unidades com ponto. Não altera o número de `|` separadores."""
    B=chr(92)
    s=s.replace(B+'left'+B+'|',B+'left'+B+'lvert ').replace(B+'right'+B+'|',B+'right'+B+'rvert ')
    s=re.sub(re.escape(B+'|')+'(.*?)'+re.escape(B+'|'),lambda m:B+'lvert '+m.group(1)+B+'rvert ',s)
    s=re.sub(re.escape(B+'sin')+'(?![a-zA-Z])',lambda m:B+'operatorname{sen}',s)
    for a,b in (('kg'+B+',m^2/s','kg'+B+'cdot m^2/s'),('N'+B+',m','N'+B+'cdot m'),('kg'+B+',m^2','kg'+B+'cdot m^2')):s=s.replace(a,b)
    return s

def Mx(s,size=55,acc=False,cores=None):
    s=nota(s);p=tokens(s);cs={}
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
    if '|' not in tex:return T(tex,44,cor),None
    parts=tokens(tex)
    cores={i:cor for i,p in enumerate(parts) if p not in ('=','+','-',r'\hat z') and r'\mathrm' not in p}
    cores.update({i:WHITE_ for i,p in enumerate(parts) if p==r'\hat z'})
    return M(*parts,size=44,cores=cores)

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
        return VGroup(Arrow(pa,pb,buff=0,stroke_width=w*np.clip(persp,.8,1.2),tip_length=tip,max_tip_length_to_length_ratio=.18,max_stroke_width_to_length_ratio=5 if w<6 else 3*w,color=cor))
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
        self.ph0=0.;self.c0=0.;self.vel=0.;self.cam_u=ValueTracker(0);self.u=ValueTracker(0);self.x=ValueTracker(0);self.bal=ValueTracker(0);self.etapa=ValueTracker(0);self.etapa_h=ValueTracker(0);self.soma_final=ValueTracker(0);self.tilt=ValueTracker(0);self.add(self.u,self.x,self.bal,self.etapa,self.etapa_h,self.soma_final,self.cam_u,self.tilt)
        self.flags={};self.drift=None;self.plano_cam=None;self._ta0=0.;self._dur=1.;self.cam_a=self.cam_b=None;self.sombras25=set();self.vetores={};self.rotulos={};self.decoracoes=[];self.reg_alg=[]
        self.fundos={};self.layer=vivo(self.desenho).set_z_index(15);self.add(self.layer)
        self._timeline={};self._geometrias=[]
        self.inicios_real={}
        self.inicios_play={}

    def an(self,aid):
        super().an(aid)
        self.inicios_real[aid]=self.nq/FPS
        self.inicios_play[aid]=self.renderer.num_plays

    def phi(self):
        f=getattr(self,'fase_fn',None)
        return f(self.clk.get_value()) if f else self.ph0+self.vel*(self.clk.get_value()-self.c0)
    def congela(self,alvo,tmin=.8,tmax=1.8):
        """Desacelera o giro de forma linear e para exatamente na fase `alvo` (sem salto)."""
        t0=self.clk.get_value();p0=self.phi();w=self.vel
        if abs(w)<1e-6:self.anda(0,alvo);return
        d=(alvo-p0)%(2*PI)
        while 2*d/abs(w)<tmin:d+=2*PI
        T=2*d/abs(w);sg=np.sign(w)
        self.fase_fn=lambda t:p0+sg*abs(w)*(min(t-t0,T)-min(t-t0,T)**2/(2*T))
        self.wait(T,interno=True);self.anda(0,p0+sg*d)
    def anda(self,vel,phi=None):
        p=self.phi() if phi is None else phi
        self.fase_fn=None
        self.ph0,self.c0,self.vel=p,self.clk.get_value(),vel
    def cam(self):
        c=self.cam_base()
        pl=getattr(self,'plano_cam',None)
        if pl:
            t=(self.clk.get_value()-self._ta0)/max(self._dur,1e-6);prev=dict(c)
            for f0,f1,nome in pl:
                alvo=CAMS[nome]
                if t>=f1:prev=dict(alvo);continue
                if t>f0:
                    u=(t-f0)/(f1-f0);prev=mistura_cam(prev,alvo,u*u*(3-2*u))
                break
            c=prev
        d=getattr(self,'drift',None)
        if d:
            t=self.clk.get_value()-self._ta0;c=dict(c)
            c['az']=c['az']+d[0]*math.sin(2*math.pi*t/d[2]);c['K']=c['K']*(1+d[1]*math.sin(math.pi*t/d[2])**2)
        return c
    def cam_base(self):
        if self.cam_a is None:
            c=dict(self.camera25)
            return c
        u=self.cam_u.get_value();a,b=self.cam_a,self.cam_b
        if u>=1:return b
        return mistura_cam(a,b,u)
    def dolly(self,nome,rt=1.5):
        self.cam_a,self.cam_b=dict(self.cam()),dict(CAMS[nome]);self.cam_u.set_value(0)
        self.play(self.cam_u.animate.set_value(1),run_time=rt)
        self.camera25=self.cam_b;self.cam_a=None

    def modelo(self):
        p=self.phi()
        if self.tipo=='pendulo_conico':return F.pendulo(p)
        if self.tipo=='haltere_torto':return F.haltere(p,self.x.get_value(),3 if self._aid=='B5-5' else 1)
        if self.tipo=='bancada_dupla':return F.haltere(p,0,1)
        if self.tipo=='plataforma_livre':
            e=F.plataforma(self.clk.get_value()-getattr(self,'_pl_t0',0.));return dict(O=np.zeros(3),massa=np.array([e['r'],0,.06]),pl=e)
        if self.tipo=='corpo_voxel':
            if self._aid=='S2':
                esc,fase,w=F.deformacao(self.clk.get_value()-self._q0/FPS)
                return F.voxel(fase,1)
            return F.voxel(p,round(self.u.get_value(),5))
        return F.roda(p,self.bal.get_value())

    def prepara(self,tipo,cam,vel=0,phi=0,**flags):
        anterior=self.fundos.get(self.tipo)
        self.tipo=tipo;self.camera25=dict(CAMS[cam] if isinstance(cam,str) else cam);self.cam_a=None;self.anda(vel,phi)
        self.flags=flags;self.vetores={};self.sombras25=set();self.rotulos={};self.etapa.set_value(0)
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
        est['tilt']=float(self.tilt.get_value()) if self.tipo=='bancada_dupla' else 0.;est['sombra']=bool(self.cam()['el']<60) and self.tipo!='bancada_dupla'      # v7: sem sombra de chão no gancho/S1
        if self.tipo=='plataforma_livre':est['raio_m']=float(e['pl']['r'])
        est.update(x=self.x.get_value(),balanceada=self.bal.get_value(),rotacao=e.get('rotacao',np.eye(3)).tolist(),destaque=self.flags.get('destaque',False))
        est['onda_u']=self.etapa.get_value() if self._aid=='B2-4' else 0
        if self._aid=='S2' and self.tipo=='corpo_voxel':
            est['expansao'],est['phi'],est['omega_deformavel']=F.deformacao(self.clk.get_value()-self._q0/FPS)
            est['livre']=True
        return r4(est)

    def seta25(self,nome,base,vet,esc,cor,trace=False,sombra=False):
        self.vetores[nome]=(base,vet,esc,cor,trace)
        if sombra:self.sombras25.add(nome)
        else:self.sombras25.discard(nome)

    def desenho(self):
        if not hasattr(self,'vetores'):return VGroup()
        g=VGroup();c=self.cam()
        frame=round(self.clk.get_value()*FPS)
        timeline=self._timeline.get(self.tipo,{}) if hasattr(self,'_timeline') else {}
        oc=timeline.get(str(frame),{}).get('pontos',{})
        esp=self.especifica()
        for nome,(a,b,cor,tr) in esp.items():
            ocultos=None      # v7: vetor sempre inteiro e opaco; o sólido não o apaga nem o tracejado indica oclusão
            if nome in getattr(self,'sem_ocl25',()):ocultos=None
            g.add(vetor3(c,a,b,cor,tr,w=3 if nome.startswith('fino_') else (8 if nome in getattr(self,'grossas25',()) else 5),ocultos=ocultos))
            if nome in self.sombras25:
                zc=CHAO_Z.get(self.tipo,-1.06);sa,sb=np.array([a[0],a[1],zc]),np.array([b[0],b[1],zc])
                if np.linalg.norm(proj(c,sb)-proj(c,sa))>.05 and all(-7.35<q[0]<-.4 and -3.6<q[1]<2.45 for q in (proj(c,sa),proj(c,sb))):g.add(Line(proj(c,sa),proj(c,sb)).set_stroke(cor,2.5,opacity=.38),Dot(proj(c,sb),radius=.035,color=cor).set_opacity(.45))
        pontos_setas=g.get_all_points()
        e=self.modelo();usados=[];self._rotulos_atuais={}
        decor=[fn(e,c) for fn in self.decoracoes]
        if self.tipo=='pendulo_conico':ocupados=[(d.get_left()[0]-.18,d.get_bottom()[1]-.18,d.get_right()[0]+.18,d.get_top()[1]+.18) for d in decor if d.get_all_points().size]
        else:
            # G28 v5: decoração só de traço (círculo, eixos, tracejado) bloqueia pelos próprios pontos (±0,2 u), não pela caixa que a envolve; texto/preenchido segue em caixa
            ocupados=[];extras=[]
            for d in decor:
                if not d.get_all_points().size:continue
                for ch in (list(d.submobjects) if isinstance(d,VGroup) and d.submobjects else [d]):
                    if not ch.get_all_points().size:continue
                    if any(mm.get_fill_opacity()>.05 for mm in ch.family_members_with_points()) or getattr(ch,'_fundo',False):
                        ocupados.append((ch.get_left()[0]-.18,ch.get_bottom()[1]-.18,ch.get_right()[0]+.18,ch.get_top()[1]+.18))
                    else:
                        for mm in ch.family_members_with_points():extras.append(np.array([mm.point_from_proportion(t) for t in np.linspace(0,1,48)]))
            if extras:pontos_setas=np.vstack([pontos_setas]+extras) if len(pontos_setas) else np.vstack(extras)
        mask=None
        girando=self.tipo!='plataforma_livre' and (abs(getattr(self,'vel',0))>1e-6 or getattr(self,'fase_fn',None) is not None)
        if not PEDIDOS3D and not girando:      # v7: com o sólido girando a máscara 3D não move rótulos (sem teletransporte); parado, a máscara continua evitando o sólido
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
            if k in ('Lh','Lperp') and 'Lh' in esp and np.linalg.norm(proj(c,esp['Lh'][1])[:2]-proj(c,esp['Lh'][0])[:2])<.22:continue   # V6: L⊥ e rótulo somem juntos
            pos=proj(c,fn(e));m,_=rotulo_modelo(texto,cor)
            if not hasattr(self,'_offsets25'):self._offsets25={}
            chave=(self._aid,k,texto)
            m.move_to(pos+np.array(self._offsets25.get(chave,off)))
            if girando and k not in getattr(self,'fixo25',()):
                # v7: com o sólido girando, o rótulo é uma função contínua da ponta: na prolongação do vetor (ponta) ou deslocamento fixo (demais). Nenhuma busca, nenhum salto.
                m.move_to(pos+np.array(off));dv_=None
                for _n,(a_,b_,_c,_t) in esp.items():
                    pa_,pb_=proj(c,a_)[:2],proj(c,b_)[:2]
                    if np.linalg.norm(pb_-pos[:2])<.14 and np.linalg.norm(pb_-pa_)>.1:dv_=(pb_-pa_)/np.linalg.norm(pb_-pa_);break
                if dv_ is not None:
                    h_=abs(dv_[0])*m.width/2+abs(dv_[1])*m.height/2+.12
                    m.move_to(np.array([pos[0]+dv_[0]*h_,pos[1]+dv_[1]*h_,0]))
                sx=max(0,-7.4-m.get_left()[0])-max(0,m.get_right()[0]+.35);sy=max(0,-3.7-m.get_bottom()[1])-max(0,m.get_top()[1]-2.5);m.shift(RIGHT*sx+UP*sy)
                for _it in range(5):      # v7: um rótulo não cobre o outro (empurra pelo eixo de menor penetração; função contínua da posição)
                    (x0,y0,_z0),(x1,y1,_z1)=m.get_corner(DL),m.get_corner(UR);mexeu=False
                    for bb in usados:
                        ox=min(x1,bb[2])-max(x0,bb[0]);oy=min(y1,bb[3])-max(y0,bb[1])
                        if ox>0 and oy>0:
                            cx=(x0+x1)/2-(bb[0]+bb[2])/2;cy=(y0+y1)/2-(bb[1]+bb[3])/2
                            if ox<oy:m.shift(RIGHT*(1 if cx>=0 else -1)*(ox+.02))
                            else:m.shift(UP*(1 if cy>=0 else -1)*(oy+.02))
                            mexeu=True;break
                    if not mexeu:break
                usados.append((m.get_left()[0]-.18,m.get_bottom()[1]-.18,m.get_right()[0]+.18,m.get_top()[1]+.18))
                m._dono=Dot(pos,radius=.02);self._rotulos_atuais[k]=m;g.add(m);continue
            if k in getattr(self,'fixo25',()):                      # roda em close/axial: rótulo preso à ponta, sem busca nem chamada
                m.move_to(pos+np.array(off))
                # G28 v5: o rótulo fica na PROLONGAÇÃO da própria seta (até 1,2 u além da ponta), no primeiro ponto livre fora da silhueta 3D; sem vaga, volta ao deslocamento fixo
                o3=proj(c,np.zeros(3));dr=pos[:2]-o3[:2];nr=np.linalg.norm(dr)
                if nr>1e-3:
                    dr=dr/nr
                    for t in np.arange(0,1.25,.08):
                        h_=abs(dr[0])*m.width/2+abs(dr[1])*m.height/2+.1
                        m.move_to(np.array([pos[0]+dr[0]*(h_+t),pos[1]+dr[1]*(h_+t),0]))
                        if livre25(m):break
                    else:
                        # ponta dentro do objeto: vaga livre mais próxima em qualquer direção, (≤ 2,8 u) ligada à ponta por chamada fina
                        cand=[P3(x,y) for x in np.linspace(-7.35+m.width/2,-.4-m.width/2,40) for y in np.linspace(-3.65+m.height/2,2.45-m.height/2,40)]
                        cand=[p for p in cand if np.linalg.norm(p[:2]-pos[:2])<2.8];cand.sort(key=lambda p:np.linalg.norm(p[:2]-pos[:2])+.15*abs(p[1]-pos[1]))
                        for p in cand:
                            m.move_to(p)
                            if livre25(m):break
                        else:m.move_to(pos+np.array(off))
                self._offsets25[chave]=m.get_center()-pos
                m._dono=Dot(pos,radius=.02);usados.append((m.get_left()[0]-.18,m.get_bottom()[1]-.18,m.get_right()[0]+.18,m.get_top()[1]+.18))
                perto_=m.get_boundary_point(pos-m.get_center());dd_=perto_-pos
                if np.linalg.norm(dd_)>.3:
                    ch_=Line(pos,perto_-.1*dd_/np.linalg.norm(dd_)).set_stroke(GEO,1.3,opacity=.7);ch_._halo=True;g.add(ch_)
                self._rotulos_atuais[k]=m;g.add(m);continue
            if not livre25(m):
                achou=False;legado=self.tipo=='pendulo_conico'          # PB1 (pêndulo) mantém a busca original do v3: a regra de chamada curta vale para as demais cenas
                if legado:
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
                dado=bool(re.match(r'^(m|M|v|L|u)(_[a-z0-9]+)?=',re.sub(r'[|\s{}]|\\(vec|mathrm|,)','',texto)))
                for buff in (() if legado else ((.26,.4,.45) if dado else (.26,.4,.55,.7,.85))):     # V1: chamada reta e curta (≤ 0,8 u; dado ≤ 0,6), nunca atravessa a figura
                    for lado in (UP,DOWN,LEFT,RIGHT,UL,UR,DL,DR):
                        m.next_to(Dot(pos,radius=.15),lado,buff=buff)
                        if livre25(m):achou=True;break
                    if achou:break
                if not achou and not legado:
                    candidatos=[P3(x,y) for x in np.linspace(-7.35+m.width/2,-.4-m.width/2,18) for y in np.linspace(-3.65+m.height/2,2.45-m.height/2,18)]
                    candidatos=[p for p in candidatos if np.linalg.norm(p-pos)<.95]
                    candidatos.sort(key=lambda p:np.linalg.norm(p-pos))
                    for p in candidatos:
                        m.move_to(p)
                        if livre25(m):achou=True;break
                if not achou and not legado:
                    # sem vaga livre a ≤ 0,85 u: escolhe a posição de MENOR penalidade (zona > outros rótulos > 3D > setas), sempre presa à zona útil
                    def pena25(mm):
                        (x0,y0,_),(x1,y1,_)=mm.get_corner(DL),mm.get_corner(UR)
                        pz=10*(max(0,-7.4-x0)+max(0,x1+.35)+max(0,-3.7-y0)+max(0,y1-2.5));po=0;ps=0;pm=0
                        for b in usados+ocupados:po+=20*max(0,min(x1,b[2])-max(x0,b[0]))*max(0,min(y1,b[3])-max(y0,b[1]))
                        if len(pontos_setas):ps=.03*int(((pontos_setas[:,0]>x0-.20)&(pontos_setas[:,0]<x1+.20)&(pontos_setas[:,1]>y0-.20)&(pontos_setas[:,1]<y1+.20)).sum())
                        p_=pz+po+ps
                        if mask is not None:
                            w,h=config.pixel_width,config.pixel_height
                            a=max(0,int((x0+8)*w/16));b=min(w,int((x1+8)*w/16)+1);cc=max(0,int((4.5-y1)*h/9));d=min(h,int((4.5-y0)*h/9)+1)
                            if b>a and d>cc:pm=5*float(mask[cc:d,a:b].mean())
                        mm._pen=(round(pz,2),round(po,2),round(ps,2),round(pm,2),[(round(b[0],2),round(b[1],2),round(b[2],2),round(b[3],2)) for b in usados+ocupados if min(x1,b[2])-max(x0,b[0])>0 and min(y1,b[3])-max(y0,b[1])>0],(round(x0,2),round(y0,2),round(x1,2),round(y1,2)));return p_+pm
                    melhor=None
                    for buff in ((.2,.3,.45) if dado else (.2,.3,.45,.6,.75,.9)):
                        for lado in (UP,DOWN,LEFT,RIGHT,UL,UR,DL,DR):
                            m.next_to(Dot(pos,radius=.15),lado,buff=buff)
                            sx=max(0,-7.4-m.get_left()[0])-max(0,m.get_right()[0]+.35);sy=max(0,-3.7-m.get_bottom()[1])-max(0,m.get_top()[1]-2.5)
                            m.shift(RIGHT*sx+UP*sy);pn=pena25(m)+.3*buff
                            if melhor is None or pn<melhor[0]:melhor=(pn,m.get_center().copy())
                    m.move_to(melhor[1]);pena25(m)
                    if AUDITORIA and melhor[0]>=1.0:print(f'[audit] {self.clk.get_value():7.1f}s RÓTULO SEM VAGA {texto!r} (penalidade {melhor[0]:.1f}; zona/rótulos/setas/3D {m._pen})')
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
        if AUDITORIA and frame%15==0:self.audita_conceitos(e,c,frame)
        return g

    def audita_conceitos(self,e,c,frame):
        # C3: setas dos mancais antiparalelas na tela (180° ± 2°). C1: L⊥ e forças da roda a 90° do eixo (± 1°).
        esp=self.especifica();t=self.clk.get_value()
        def vtela(n):a,b,_,_=esp[n];return proj(c,b)[:2]-proj(c,a)[:2]
        def ang(u,v):
            if np.linalg.norm(u)<1e-6 or np.linalg.norm(v)<1e-6:return None
            return math.degrees(math.acos(np.clip(np.dot(u,v)/np.linalg.norm(u)/np.linalg.norm(v),-1,1)))
        par=next(((x,y) for x,y in (('Fsup','Finf'),('fino_Fsup','fino_Finf')) if x in esp and y in esp),None)
        if par:
            a=ang(vtela(par[0]),vtela(par[1]))
            if a is not None:print(f'[audit] {t:7.1f}s MANCAIS ANGULO {a:.1f}'+('' if abs(a-180)<=2 else ' FALHA'))
        if self.tipo=='roda_balanceamento':
            # ÂNGULO NA TELA: vetor dito perpendicular ao eixo deve ler 60–120° do eixo na tela; no plano AXIAL (eixo = ponto), 90° ± 5° em relação à visão.
            eixo_t=proj(c,np.array([0,1,0.]))[:2]-proj(c,np.zeros(3))[:2];az_,el_=math.radians(c['az']),math.radians(c['el'])
            visao=np.array([math.cos(el_)*math.cos(az_),math.cos(el_)*math.sin(az_),math.sin(el_)])
            for k in ('transversal','Fa1','Fa2'):
                v=np.array(e[k],float)
                if np.linalg.norm(v)<1e-9 or (k!='transversal' and k not in esp):continue
                if np.linalg.norm(eixo_t)>.15*c['K']:
                    vt=proj(c,v/np.linalg.norm(v)*.3)[:2]-proj(c,np.zeros(3))[:2];a=ang(eixo_t,vt)
                    ok=a is None or 60<=a<=120
                    print(f'[audit] {t:7.1f}s ANGULO TELA {k} PERFIL {a if a is not None else -1:.1f}'+('' if ok else ' FALHA'))
                else:
                    a=ang(v,visao);ok=abs(a-90)<=5
                    print(f'[audit] {t:7.1f}s ANGULO TELA {k} AXIAL {a:.1f}'+('' if ok else ' FALHA'))
            eixo=np.array([0.,1.,0.])
            for k in ('transversal','Fa1','Fa2'):
                v=np.array(e[k],float)
                if np.linalg.norm(v)>1e-9:
                    a=ang(v,eixo);print(f'[audit] {t:7.1f}s RODA {k} EIXO {a:.1f}'+('' if abs(a-90)<=1 else ' FALHA'))

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
        t0_log=self.clk.get_value()
        A,ia=Mx(s,size=52 if final else 46,acc=acc,cores=cores)
        A._indices25=ia
        self.pilha.poe(A)
        A._tam=float(A.font_size)
        self._linha_em_construcao25=A
        self._janela25=rt
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
        try:self.log_linha25(t0_log,A,ia)
        except Exception as e:print('[linha] erro',e)
        if sub is not None:
            self.remove(sub);A.add(sub);A._sublinhado25=sub
        quantidade=3 if self._aid=='S1' else 2
        self.pilha.so(*[m for m,_ in self.pilha.linhas[-quantidade:]],rt=.25 if getattr(self,'_cad25',.3)>=.3 else .12)
        self._linha_em_construcao25=None;self._janela25=None
        return A,ia

    def log_linha25(self,t0,A,ia):
        """ORDEM POR X: caixa em px (960×540) de cada token da linha pronta; `ordem25.py` mede no vídeo o instante em que cada token ganha tinta."""
        fx=lambda x:(x/14.2222+.5)*960;fy=lambda y:(.5-y/8.)*540
        caixas=[]
        for k,ids in enumerate(ia):
            if not ids:continue
            gl=[A[0][j] for j in ids]
            caixas.append([k,round(fx(min(g.get_left()[0] for g in gl))),round(fy(max(g.get_top()[1] for g in gl))),round(fx(max(g.get_right()[0] for g in gl))),round(fy(min(g.get_bottom()[1] for g in gl)))])
        print('[linha]',json.dumps(dict(aid=self._aid,tex=A.tex_string,t0=round(t0,3),t1=round(self.clk.get_value(),3),caixas=caixas),ensure_ascii=False))

    def resultado(self,a,cor=LMAG):
        m=a[0] if isinstance(a,tuple) else a
        if getattr(m,'_sublinhado25',None) is not None:return
        s=sublinha(m,cor);self.play(Create(s),run_time=.3);self.remove(s);m.add(s)

    def quadro(self,aid):
        self.an(aid)
        self.vetores={};self.rotulos={};self.decoracoes=[];self.fixo25=set();self.sem_ocl25=set();self.grossas25=set()
        if aid not in ('B1-2','B1-4','B3-7'):self.pilha.limpa(rt=.2)
        linhas={m for m,_ in self.pilha.linhas}
        extras=[m for m in self.mobjects if m not in self.fixos() and m not in linhas and not (getattr(m,'_fica25',False) and aid in ('H2','H3')) and m is not self.layer and m is not self.s1 and m not in self.fundos.values() and not isinstance(m,ValueTracker)]
        if extras:self.play(*[FadeOut(m) for m in extras],run_time=.2)
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
        auditar(self,t,itens,op,objs)

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

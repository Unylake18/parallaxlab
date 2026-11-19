"""Tabela por quadro em partes: física SI e projeções raster usadas pelo Manim."""
import json,math,hashlib
from pathlib import Path
import numpy as np
import latex25
from pecas25 import CAMS,proj,px,ESC_V
import fisica25 as F
U=Path(__file__).resolve().parent
le=lambda p:json.loads(p.read_text(encoding='utf-8'))
dest=U/'tab_quadros';dest.mkdir(exist_ok=True)
indice=[]
for l in ['PH','PB1','PB2','PB3','PB4','PB5','PB6','PS']:
    tempos=le(U/f'tempos_{l}.json')['inicios']
    for tipo,estados in le(U/f'threejs/pedidos3d/{l}.json')['cenas'].items():
        pr=U/f'threejs/q3d/{l}_960x540/{tipo}/pontos.json'
        if not pr.exists():continue
        raster=le(pr);lin=[]
        for f,e in estados:
            if str(f) not in raster:continue
            aid=max((a for a,t in tempos.items() if round(t*15)<=f),key=lambda a:tempos[a],default=next(iter(tempos)))
            if tipo=='pendulo_conico':
                fis=F.pendulo(e['phi']);esc=1.6
                if aid=='B1-8':
                    centro=np.array([0.,0.,-math.cos(F.TH)]);rr=fis['massa']-centro;L=np.cross(rr,fis['p'])
                    tp=np.cross(rr,-.2*9.8*F.Z);fis.update(O=centro,r=rr,L=L,axial=L,transversal=np.zeros(3),torque=np.zeros(3),torque_peso=tp,torque_fio=-tp)
            elif tipo=='haltere_torto':fis=F.haltere(e['phi'],e.get('x',0),3 if aid=='B5-5' else 1);esc=1.8
            elif tipo=='roda_balanceamento':fis=F.roda(e['phi'],e.get('balanceada',0));esc=2.1
            else:
                R=np.array(e['rotacao']);s=e.get('expansao',1);I=s*s*R@np.array(F.VOX['tensor'])@R.T;w=e.get('omega_deformavel',math.pi)
                r=s*(R@np.array(F.VOX['posicoes'][F.VOX['destaque']]))
                v=np.cross(w*F.Z,r);L=I@(w*F.Z)
                fis=dict(O=np.zeros(3),r=r,massa=r,v=v,L=L,L1=np.cross(r,.01*v),axial=L*F.Z,transversal=L*np.array([1,1,0]),torque=np.cross(w*F.Z,L));esc=ESC_V
            fisica={k:np.asarray(v).round(8).tolist() for k,v in fis.items() if k not in ('posicoes','rotacao')}
            r=fis['r'];eixo=1 if tipo=='roda_balanceamento' else 2;rho=np.array(r,copy=True);rho[eixo]=0
            fisica.update(rho=rho.round(8).tolist(),z_axial=float(r[eixo]),eixo_global=[0,1,0] if eixo==1 else [0,0,1],dLdt=np.asarray(fis.get('torque',np.zeros(3))).round(8).tolist())
            pts=dict(raster[str(f)].get('pontos',{}))
            if aid=='B1-8':
                pts['prego']=pts['O']
                for k in ['L','axial','transversal','torque','r']:
                    if k in pts:pts[k+'_referencia_prego']=pts.pop(k)
                if 'L:0' in pts:pts['O']=pts['L:0'];pts['L']=pts['L:24']
            if tipo in ('pendulo_conico','haltere_torto'):
                raio=float(np.linalg.norm(fis['transversal'])*esc);z=float(fis['axial'][2]*esc)
                c=e['cam'];th=math.tan(math.radians(c['fov'])/2) if c['fov'] else 0
                D=4.5/c['K']/th if th else 10;near=max(.01,D-4) if th else 5;far=D+6 if th else 15
                for j,a in enumerate(np.linspace(0,2*math.pi,48,endpoint=False)):
                    p=np.asarray(fis['O'])+np.array([raio*math.cos(a),raio*math.sin(a),z]);q,d,k=proj(c,p,True)
                    depth=far/(far-near)-far*near/((far-near)*d) if th else (d-near)/(far-near)
                    pts[f'circulo_L:{j}']=dict(px=px(q),depth=depth,view_depth=d,perspectiva=k,origem='projeção analítica calibrada; círculo auxiliar')
            lin.append(dict(quadro=f,t=f/15,ancora=aid,cam=e['cam'],phi=e['phi'],fisica=fisica,projecoes=pts))
        p=dest/f'{l}_{tipo}.json';p.write_text(json.dumps(lin,separators=(',',':')),encoding='utf-8')
        indice.append(dict(lote=l,tipo=tipo,quadros=len(lin),arquivo=p.relative_to(U).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
    print(l,flush=True)
tab=le(U/'tab25.json');tab['quadros']=dict(resolucao=[960,540],fps=15,partes=indice,convencoes='SI; profundidade normalizada 0..1, view_depth em metros; câmera lenta só no movimento aparente; vetores congelados conservam o estado de referência. Círculo auxiliar com 48 pontos analíticos, demais projeções do rasterizador Three.js.')
(U/'tab25.json').write_text(json.dumps(tab,ensure_ascii=False,indent=1),encoding='utf-8')
print(len(indice),'partes; projeções reais preservadas e tabela física por quadro')

"""Verificações localizadas dos caminhos e da região regular da V1.5."""
import json
from pathlib import Path
import numpy as np

def bezier(a,c,d,b,t):
    return (1-t)**3*a+3*(1-t)**2*t*c+3*(1-t)*t*t*d+t**3*b

q=np.array([-6.2,.1]);a=np.array([-4.7,-.8]);b=np.array([-1.1,1.1])
values=[];minimum=[]
for c,d in [(np.array([-4.4,2]),np.array([-2.3,2.1])),(np.array([-4,-2]),np.array([-1.4,-1.7]))]:
    pts=np.array([bezier(a,c,d,b,t) for t in np.linspace(0,1,20001)])
    mid=(pts[1:]+pts[:-1])/2-q;delta=np.diff(pts,axis=0)
    values.append(float(np.sum(np.sum(mid*delta,axis=1)/np.linalg.norm(mid,axis=1)**3)))
    minimum.append(float(np.linalg.norm(pts-q,axis=1).min()))
analytic=float(1/np.linalg.norm(a-q)-1/np.linalg.norm(b-q))
assert all(abs(v-analytic)<1e-7 for v in values)
assert min(minimum)>1.4
clearance=(-3.5-1.85)-(-6.2);assert clearance>.84
origin=np.array([-3.8,.15]);last=np.array([-2,1.5]);probe_distances=[]
for end,c,d in [(np.array([-5.5,1.4]),np.array([-2.6,2.7]),np.array([-4.9,2.7])),(np.array([-5.4,-1.3]),np.array([-6.3,1.2]),np.array([-6.3,-1.1])),(np.array([-2,-1.3]),np.array([-4.6,-1.7]),np.array([-2.7,-1.7]))]:
    pts=np.array([bezier(last,c,d,end,t) for t in np.linspace(0,1,20001)])
    probe_distances.append(float(np.linalg.norm(pts-origin,axis=1).min()));last=end
radius_bound=.25*np.sqrt(1.44**2+1.32**2)
assert min(probe_distances)>radius_bound
out={'circulacao_valores_numericos':values,'valor_analitico':analytic,
     'distancia_minima_caminhos_origem':minimum,'stokes_separacao_horizontal_minima':clearance,
     'cubo_distancias_minimas_origem':probe_distances,'cubo_raio_projetado_maximo':radius_bound,
     'F2_orientacao':'(-y,x): anti-horária, +z',
     'delta':'I=1 somente após distância entre origem e centro <0.85; valor ocultado na travessia da fronteira'}
Path(__file__).with_name('qa_fisica_v1_5.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
print(out)

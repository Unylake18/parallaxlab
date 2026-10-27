"""Verificações da física preservada, novos voos completos e projeção comum."""
import json, math
from pathlib import Path
import numpy as np
from modelo_orbital import R_T, MU, validar, conica, integrar, periodo, v_circular, energia
from geometria_visual import CameraOrbital
from superficie import recorte_rgba


def verificar():
    resultado=validar()
    voos={}
    for f in (.70,.92,1.,1.2,1.44):
        r=1.5*R_T
        dur=periodo(r)/(2-f*f)**1.5 if f<math.sqrt(2) else periodo(r)
        orb=integrar([0,r],[v_circular(r)*f,0],dur)
        raios=np.linalg.norm(orb.r,axis=1)
        assert orb.impacto==(f==.70)
        assert raios.min()>=R_T-1e-5
        assert (energia(orb.r[0],orb.v[0])<0)==(f<math.sqrt(2))
        if not orb.impacto and f<math.sqrt(2):
            assert np.linalg.norm(orb.r[-1]-orb.r[0])/r<2e-5
        voos[str(f)]={'impacto':orb.impacto,'duracao_s':orb.t[-1],
                      'energia':energia(orb.r[0],orb.v[0]),'raio_minimo_m':float(raios.min())}
    cam=CameraOrbital(); cam.x.set_value(0); cam.y.set_value(0)
    cam.span.set_value(6.4); cam.incl.set_value(.55)
    assert cam.visivel([0,1.06],[0,0])
    assert not cam.visivel([0,-1.06],[0,0])
    assert cam.visivel([1.06,0],[0,0])
    fisico=np.array([[0,1.06*R_T],[R_T,0],[0,-R_T]],dtype=float)
    copia=fisico.copy(); cam.transformar(fisico/R_T)
    assert np.array_equal(fisico,copia)
    cam.incl.set_value(0)
    curva=cam.linha(np.column_stack([1.06*np.sin(np.linspace(0,2*np.pi,20000)),
                                    1.06*np.cos(np.linspace(0,2*np.pi,20000))]))
    for parte in curva:
        assert parte.get_num_curves()<=599
        assert np.isfinite(parte.get_points()).all()
    dados=recorte_rgba(0,0,2,0,0,16.,9.,960,540)
    imagem=dados[0]
    assert imagem.shape[0]<=540 and imagem.shape[1]<=960
    assert imagem[imagem.shape[0]//2,imagem.shape[1]//2,3]==255
    resultado.update(voos_completos_N13=voos,oclusao='aprovada',
                     projecao_independente_SI='aprovada',limite_segmentos=599,
                     baricentro_sobre_raio=4.67e6/R_T)
    assert 0<resultado['baricentro_sobre_raio']<1
    return resultado


if __name__=='__main__':
    r=verificar()
    (Path(__file__).parent/'validacao_repagina.json').write_text(json.dumps(r,indent=2,ensure_ascii=False),encoding='utf-8')
    print('Física preservada, 5 voos completos, oclusão e projeção: OK')

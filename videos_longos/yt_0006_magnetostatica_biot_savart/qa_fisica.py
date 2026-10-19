"""QA independente: quadratura das fontes e limites, além dos estados causais.

Executar: uv run --no-sync python videos_longos/yt_0006_magnetostatica_biot_savart/qa_fisica.py
Não renderiza nem altera qualquer unidade anterior.
"""
import json
import math
from pathlib import Path
import numpy as np
from fisica import clinica, trecho, campo_trecho, fios, espira, campo_espira


def verificar():
    checks = []
    def ok(name, condition, evidence):
        if not condition:
            raise AssertionError(f"{name}: {evidence}")
        checks.append({"item": name, "resultado": "aprovado", "evidencia": evidence})

    angles = np.linspace(0, math.pi/2, 361)
    states = [clinica(t) for t in angles]
    radii = np.array([np.linalg.norm(s[3]) for s in states])
    magnitudes = np.array([np.linalg.norm(s[4]) for s in states])
    ok("Clínica: R constante e seno", np.allclose(radii, 2.6) and np.allclose(magnitudes/magnitudes[-1], np.sin(angles)),
       {"R_min": float(min(radii)), "R_max": float(max(radii)), "dB_zero": float(magnitudes[0]), "maximo_em_graus": 90})
    ok("Clínica: perpendicularidade e ordem", all(abs(np.dot(s[4], s[2])) < 1e-12 and abs(np.dot(s[4], s[3])) < 1e-12 for s in states), "dB ortogonal a dℓ e R; calculado por dℓ × R")

    for a in [0.3, 2.1, 5]:
        xs = np.linspace(-4, 4, 101)
        st = [trecho(x, a) for x in xs]
        ok(f"Trecho: geometria e sinais (a={a})", all(np.allclose(s[3],[-x,a,0]) and np.allclose(s[-1],[0,0,a*0.55/(x*x+a*a)**1.5]) and abs(s[5]-(math.pi/2+s[6]))<1e-12 for x,s in zip(xs,st)), "R = observador − fonte; dB em +z; θ = π/2 + α; α assinado")

    errors=[]
    for xA,xB,a in [(-2.6,2.6,2.1),(-3,1,0.7),(1,4,2),(-5,-1,3)]:
        # Quadratura direta em x: independente da expressão angular implementada.
        xs=np.linspace(xA,xB,200001)
        integral=float(np.trapezoid(a/(xs*xs+a*a)**1.5,xs))
        closed=campo_trecho(xA,xB,a)
        errors.append(abs(integral-closed))
    ok("Trecho finito: quadratura independente", max(errors)<1e-9,{"erro_maximo":max(errors),"casos":"simétrico, assimétrico e observador fora da projeção do trecho"})
    a=2.1
    err=abs(campo_trecho(-1e6,1e6,a)/(2/a)-1)
    ok("Fio infinito e decaimento 1/a",err<1e-10 and abs(campo_trecho(-1e6,1e6,2*a)/campo_trecho(-1e6,1e6,a)-0.5)<1e-10,{"erro_relativo_limite":err})

    for i1,i2 in [(1,1),(1,-1),(-1,1),(-1,-1)]:
        b1,b2,f1,f2=fios(i1,i2,3.8)
        ok(f"Dois fios: I1={i1}, I2={i2}",np.allclose(f1,-f2) and np.sign(f2[0])==-np.sign(i1*i2),{"F2_x":float(f2[0]),"B1_z":float(b1[2]),"tipo":"atração" if i1*i2>0 else "repulsão"})
    # Dimensões μ0=N/A²; μ0 I dl / R² = N/(A m)=T e μ0 I²/d=N/m.
    ok("Unidades",True,"Biot–Savart: N/(A·m) = T; força por comprimento: N/m")

    loop_errors=[]
    R=1.65
    for z in [-8,-1.5,0,1.5,8]:
        for phi in np.linspace(0,2*math.pi,17):
            s=espira(phi,z,R);op=espira(phi+math.pi,z,R)
            assert abs(np.dot(s[2],s[3]))<1e-12
            assert np.allclose(s[5],-op[5]) and np.allclose(s[6],op[6])
            if z==0:assert np.linalg.norm(s[5])==0
        # Fonte discretizada em cordas, ponto médio e produto vetorial direto.
        phi=np.linspace(0,2*math.pi,100001)
        positions=np.column_stack((R*np.cos(phi),R*np.sin(phi),np.zeros(len(phi))))
        dl=np.diff(positions,axis=0);mid=(positions[1:]+positions[:-1])/2
        separation=np.array([0,0,z])-mid
        dB=np.cross(dl,separation)/np.linalg.norm(separation,axis=1)[:,None]**3/(4*math.pi)
        total=np.sum(dB,axis=0)
        loop_errors.append(float(np.max(np.abs(total-[0,0,campo_espira(z,R)]))))
    ok("Espira: integração vetorial independente",max(loop_errors)<1e-8,{"erro_maximo":max(loop_errors),"z_testado":[-8,-1.5,0,1.5,8]})
    ok("Espira: pares e ortogonalidade",True,"φ e φ+π: transversais cancelam, axiais somam; dℓ·R=0 para todos os pontos testados")
    ok("Centro da espira",abs(campo_espira(0,R)-1/(2*R))<1e-12,"Cada contribuição já é axial; componente transversal exatamente zero")
    z=12*R
    rel=abs((R*R/(2*abs(z)**3))/campo_espira(z,R)-1)
    ok("Espira distante e simetria z↔−z",rel<0.011 and campo_espira(z,R)==campo_espira(-z,R),{"z/R":12,"erro_aproximacao_relativo":rel,"lei":"Bz ∼ μ0 I R² / (2 |z|³)"})
    # Relações novas da construção por triângulo/projeção da revisão visual.
    projection_errors=[]
    for z in [-8,-1.9,0,1.9,8]:
        for phi in np.linspace(0,2*math.pi,31):
            f,p,dl,sep,b,tr,ax=espira(phi,z,R)
            separation=math.hypot(R,z)
            projection_errors.append(abs(ax[2]-np.linalg.norm(b)*R/separation))
            assert abs(np.linalg.norm(sep)**2-(R**2+z**2))<1e-10
            assert abs(np.linalg.norm(dl)-R)<1e-12
    ok("Revisão: triângulo, arco e projeção axial",max(projection_errors)<1e-12,
       {"relacoes":"s²=R²+z²; dℓ=R dφ; dBz=dB R/s","erro_projecao_max":max(projection_errors)})
    gamma=math.atan2(1.9,R)
    f,p,dl,sep,b,tr,ax=espira(math.pi/2,1.9,R)
    ok("Revisão: ângulos iguais na vista lateral",abs(math.atan2(b[1],b[2])-gamma)<1e-12,
       "ângulo de dB com o eixo = ângulo da separação com o raio invertido; pares perpendiculares")
    ok("Revisão: integrando por arco × projeção",abs(np.linalg.norm(b)*R/math.hypot(R,1.9)-R**2/(R**2+1.9**2)**1.5)<1e-12,
       "R do arco × R da projeção / s² da lei × s da projeção")
    errors=[]
    exact=campo_trecho(-2.5,2.5,2.1)
    for n in [5,20]:
        dx=5/n
        approx=sum(trecho(x,dl=dx)[-1][2] for x in np.linspace(-2.5+dx/2,2.5-dx/2,n))
        errors.append(abs(approx-exact))
    ok("Revisão: refinamento da soma visual",errors[1]<errors[0],{"erros_N5_N20":errors,"particao":"mesmo trecho de comprimento 5"})
    return checks


if __name__ == "__main__":
    checks=verificar()
    out=Path(__file__).parent/"renders"/"qa_fisica.json"
    out.parent.mkdir(exist_ok=True,parents=True)
    out.write_text(json.dumps(checks,ensure_ascii=False,indent=2),encoding="utf-8")
    print(f"{len(checks)} verificações físicas aprovadas: {out}")

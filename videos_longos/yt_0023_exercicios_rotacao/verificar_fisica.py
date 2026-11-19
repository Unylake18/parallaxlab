"""Conferência independente dos números, sem substituir medição dos quadros renderizados."""
import json,math
from pathlib import Path
import fisica as f
U=Path(__file__).resolve().parent
checks=[]
def check(nome,valor,esperado,tolerancia):
    checks.append(dict(nome=nome,valor=valor,esperado=esperado,tolerancia=tolerancia,passou=abs(valor-esperado)<=tolerancia))
check('I total',f.I,2.0175,1e-9)
check('aceleração bloco',f.A,.9833,.0001)
check('tração volante',f.TRACAO,88.17,.01)
check('omega em 1,5 s',f.OMEGA,9.833,.001)
check('energia volante',f.K_VOL,97.53,.02)
check('tempo frenagem',f.T_STOP,4.96,.01)
check('alpha carretel',f.ALPHA_C,6.877,.001)
check('tração leve',6*(f.G-.3*f.ALPHA_C),46.42,.01)
check('tração pesado',10*(f.G+.1*f.ALPHA_C),104.88,.01)
check('força eixo horizontal',f.forca(0)['fy'],4/7,1e-10)
check('força eixo 45 x',f.forca(math.pi/4)['fx'],-9/14,1e-10)
check('força eixo 45 y',f.forca(math.pi/4)['fy'],17/14,1e-10)
check('força eixo vertical',f.forca(math.pi/2)['fy'],13/7,1e-10)
check('período dois discos',f.periodo(.3,True),1.159,.001)
check('período um disco',f.periodo(.3),1.129,.001)
check('período mínimo',f.periodo(.1/math.sqrt(2)),.755,.001)
check('períodos conjugados',f.periodo(.05)-f.periodo(.1),0,1e-12)
for t in [0,.3,.7,1.5]:
    s=f.volante(t)
    check(f'energia volante t={t}',s['K']+5*s['v']**2,s['U'],1e-9)
for t in [0,1,3,f.T_STOP]:
    s=f.freio(t);check(f'calor+K t={t}',s['K']+s['calor'],f.K_VOL,1e-9)
out=dict(escopo='modelo matemático; NÃO mede alinhamento, vínculos ou setas dos quadros',testes=checks)
(U/'renders'/'fisica_modelo.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf8')
print(f'{sum(c["passou"] for c in checks)}/{len(checks)} conferências do modelo passaram')
assert all(c['passou'] for c in checks)

"""Verificação física e geométrica do candidato `liquido_rotacao` (roda no Blender, sem interface).

    blender.exe -b -P experimentos/blender/arsenal/verificar_liquido_rotacao.py

Confere (falha com SystemExit se algo estourar a tolerância):
  1. Analítico: V(λ) = 2π ∫0^R z(r,λ) r dr, por quadratura de Simpson sobre a MESMA função `altura_superficie` que gera a malha,
     é igual a π R² h0 para todo λ (volume sobre o fundo z=0).
  2. Forma fechada: o termo em λ de ∫ z r dr é exatamente zero (−λαR⁴/4 + λαR⁴/4).
  3. Malha real do Blender (bmesh.calc_volume do corpo do líquido): constante em λ, e igual a π R² h0 × (fator do polígono de
     N_THETA lados) dentro da discretização radial.
  4. Extremos: λ=0 plano em h0; λ=1 centro = h0 − Δh/2, borda = h0 + Δh/2 (na malha); centro desce e borda sobe monotonicamente.
  5. Tracers: r/z constantes no interior, rotação azimutal, independência de λ e fechamento do loop.
  6. Modos opcionais, easing monotônico, hold editorial e payoff.
"""

import json
import math
import sys
from pathlib import Path

import bmesh
import bpy

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
sys.path.insert(0, str(AQUI.parent))
import casca_oca as co  # noqa: E402
import liquido_rotacao as lr  # noqa: E402

FICHA = json.loads((AQUI / 'solidos/liquido_rotacao.json').read_text(encoding='utf-8'))
PARAMETROS = {k: v['valor'] for k, v in FICHA['parametros'].items()}
R, H, H0, DH = (PARAMETROS[k] for k in ['raio','altura_recipiente','nivel','delta_h'])
ALPHA = DH / R ** 2
LAMBDAS = [0.0, 0.1, 0.25, 0.5, 0.75, 0.9, 1.0]
falhas = []


def confere(ok, msg):
    print(("  ok   " if ok else "  FALHA ") + msg)
    if not ok:
        falhas.append(msg)


def simpson(f, a, b, n=2000):
    h = (b - a) / n
    s = f(a) + f(b) + sum((4 if k % 2 else 2) * f(a + k * h) for k in range(1, n))
    return s * h / 3


# 1. analítico ────────────────────────────────────────────────────────────────
print("1. Volume analítico V(λ) = 2π ∫ z r dr  vs  π R² h0")
V_ref = math.pi * R ** 2 * H0
for L in LAMBDAS:
    V = 2 * math.pi * simpson(lambda r: lr.altura_superficie(r, L, R, H0, ALPHA) * r, 0.0, R)
    confere(abs(V - V_ref) / V_ref < 1e-12, f"λ={L:<5} V={V:.12f}  π R² h0={V_ref:.12f}  erro rel={abs(V - V_ref) / V_ref:.2e}")

# 2. forma fechada ────────────────────────────────────────────────────────────
print("2. Termo em λ de ∫0^R z r dr (forma fechada): −λαR⁴/4 + λαR⁴/4")
termo = simpson(lambda r: (-ALPHA * R ** 2 / 2 + ALPHA * r ** 2) * r, 0.0, R)
confere(abs(termo) < 1e-12, f"∫0^R (−αR²/2 + α r²) r dr = {termo:.3e}  (esperado 0)")

# 3 e 4. malha real ───────────────────────────────────────────────────────────
print("3/4. Malha do Blender (corpo do líquido)")
N = lr.N_THETA
fator_poligono = N / (2 * math.pi) * math.sin(2 * math.pi / N)       # área do polígono inscrito / área do círculo
V_malha_esperado = V_ref * fator_poligono
volumes, centros, bordas = [], [], []
for L in LAMBDAS:
    co.limpar_cena()
    lr.liquido_rotacao(raio=R, altura_recipiente=H, nivel=H0, delta_h=DH, lam=L)
    corpo = bpy.data.objects["LiquidoCorpo"]
    bm = bmesh.new()
    bm.from_mesh(corpo.data)
    confere(all(e.is_manifold for e in bm.edges), f"λ={L}: corpo fechado, sem bordas abertas")
    confere(all(v.normal.z > 0 for v in list(bm.faces)[:lr.N_THETA]), f"λ={L}: normais do topo para fora (+z)")
    V = bm.calc_volume(signed=True)
    bm.free()
    zc = corpo.data.vertices[0].co.z                                   # vértice do centro (r=0)
    zb = max(v.co.z for v in corpo.data.vertices)                      # borda (r=R, topo)
    volumes.append(V)
    centros.append(zc)
    bordas.append(zb)
    print(f"  λ={L:<5} V_malha={V:.6f}  centro z={zc:.6f}  borda z={zb:.6f}")
v0 = volumes[0]
confere(all(abs(v - v0) / v0 < 5e-4 for v in volumes),
        f"volume da malha constante em λ: variação máx rel = {max(abs(v - v0) for v in volumes) / v0:.2e} (tolerância 5e-4, discretização radial)")
confere(abs(v0 - V_malha_esperado) / V_malha_esperado < 1e-6, f"λ=0: V_malha={v0:.6f} = π R² h0 × fator do polígono = {V_malha_esperado:.6f}")
confere(abs(volumes[-1] - V_malha_esperado) / V_malha_esperado < 5e-4,
        f"λ=1: V_malha={volumes[-1]:.6f} vs π R² h0 × polígono = {V_malha_esperado:.6f} (rel {abs(volumes[-1] - V_malha_esperado) / V_malha_esperado:.2e})")
confere(abs(centros[0] - H0) < 1e-6 and abs(bordas[0] - H0) < 1e-6, "λ=0: centro e borda em z=h0 (superfície plana)")
confere(abs(centros[-1] - (H0 - DH / 2)) < 1e-6, f"λ=1: centro z={centros[-1]:.6f} = h0 − Δh/2 = {H0 - DH / 2:.6f}")
confere(abs(bordas[-1] - (H0 + DH / 2)) < 1e-6, f"λ=1: borda z={bordas[-1]:.6f} = h0 + Δh/2 = {H0 + DH / 2:.6f}")
confere(all(b < a for a, b in zip(centros, centros[1:])), "o centro desce monotonicamente com λ")
confere(all(b > a for a, b in zip(bordas, bordas[1:])), "a borda sobe monotonicamente com λ")
confere(abs(2 * (bordas[-1] - H0) - DH) < 1e-6 and abs((bordas[-1] - centros[-1]) - DH) < 1e-6, f"desnível borda − centro = Δh = {DH}")

# 5. tracers ──────────────────────────────────────────────────────────────────
print("5. Tracers e independência dos controles")
co.limpar_cena()
proxy, atualizar, _, ctl = lr.liquido_rotacao(raio=R, altura_recipiente=H, nivel=H0, delta_h=DH, lam=0.7,
                                           estado_visual='qa', marcadores=1, voltas=1)
tracers = [o for o in bpy.data.objects if o.name.startswith("Tracer")]


def pos(fase):
    ctl.estado(fase_rotacao=fase)
    return [tuple(o.location) for o in tracers]


def azimute(p):
    return math.atan2(p[1], p[0])


p0, p25, p50, p100 = pos(0.0), pos(0.25), pos(0.5), pos(1.0)
confere(len(tracers) == 18, f"8+10 tracers uniformes: {len(tracers)}")
confere(all(math.dist(a, b) < 1e-6 for a, b in zip(p0, p100)), "fase=1 reproduz fase=0 (loop fecha sem emenda)")
dif = [((azimute(b) - azimute(a)) % (2 * math.pi)) for a, b in zip(p0, p25)]
confere(all(abs(d - math.pi / 2) < 1e-6 for d in dif), "fase 0 → 0,25: giro anti-horário de 90°")
raios = [math.hypot(p[0], p[1]) for p in p0]
confere(all(abs(math.hypot(p[0], p[1]) - r) < 1e-6 and abs(p[2]-q[2]) < 1e-6
            for p, q, r in zip(p50, p0, raios)), "r e z permanecem constantes durante a rotação")
antes = [tuple(v.co) for v in bpy.data.objects['LiquidoCorpo'].data.vertices]
pos(0.37)
confere(antes == [tuple(v.co) for v in bpy.data.objects['LiquidoCorpo'].data.vertices], "fase_rotacao não altera a malha")
tracers_antes = [tuple(o.location) for o in tracers]
for L in LAMBDAS:
    ctl.estado(lam=L)
    confere(tracers_antes == [tuple(o.location) for o in tracers], f"λ={L} não altera r/z/φ dos tracers")
    confere(all(0 < p[2] - lr.TAM_TRACER and p[2] + lr.TAM_TRACER < lr.altura_superficie(r,L,R,H0,ALPHA)
                for p,r in zip(tracers_antes, [math.hypot(p[0],p[1]) for p in tracers_antes])), f"λ={L}: tracers dentro do líquido")

print('6. Modos, morph editorial e payoff')
for modo, esperados in [('fenomeno',(False,False,False,True,False)),
                       ('geometria',(True,True,False,False,False)),('qa',(True,True,True,True,True))]:
    co.limpar_cena()
    lr.liquido_rotacao(estado_visual=modo)
    presentes = tuple(bpy.data.objects.get(nome) is not None for nome in
                      ['GradeSuperficie','SecaoMeridiana','NivelReferencia','SetorRotacao','Tracer'])
    confere(presentes == esperados, f'{modo}: grade/meridiana/referência/setor/tracers = {presentes}')
for modo in ['fenomeno','geometria']:
    co.limpar_cena()
    lr.liquido_rotacao(estado_visual=modo,marcadores=1)
    confere(not any(o.name.startswith('Tracer') for o in bpy.data.objects), f'{modo}: tracers bloqueados mesmo com marcadores=1')
co.limpar_cena()
lr.liquido_rotacao(estado_visual='qa',marcadores=0)
confere(not any(o.name.startswith('Tracer') for o in bpy.data.objects), 'qa: tracers continuam ocultáveis')
seq = [lr.estado_editorial('morph',i/100)['lam'] for i in range(101)]
confere(seq[0] == 0 and seq[-1] == 1 and all(b>=a for a,b in zip(seq,seq[1:])), 'morph cresce monotonicamente de 0 a 1')
confere(all(v == 1 for v in seq[75:]), 'hold no último quarto; não retorna ao plano')
confere(all('fase_rotacao' not in lr.estado_editorial('morph',i/10) for i in range(11)), 'morph não controla rotação')
confere(lr.estado_editorial('payoff',0)['revela'] == 0 and lr.estado_editorial('payoff',1)['revela'] == 1, 'payoff revela superfície de 0 a 1')
co.limpar_cena()
_, loop, _, ctl = lr.liquido_rotacao(movimento=1,varrer_lambda=1)
for fase, L in [(0,0),(0.5,1),(1,0)]:
    loop(fase)
    confere(abs(bpy.data.objects['LiquidoCorpo'].data.vertices[0].co.z - lr.altura_superficie(0,L,ctl.R,ctl.h0,ctl.alpha)) < 1e-6,
            f'loop QA preservado: fase {fase}, λ={L}')

print('7. Adaptador do arsenal com a ficha atual')
from construtores import CONSTRUTORES
co.limpar_cena()
res = CONSTRUTORES['liquido_rotacao'](PARAMETROS)
confere(res['apos_camera'] is not None and len(res['enquadrar']) == 1, 'ficha e construtor compatíveis')

print('8. Setor angular preso à superfície e rotação rígida')
co.limpar_cena()
_, _, _, ctl = lr.liquido_rotacao(raio=R,altura_recipiente=H,nivel=H0,delta_h=DH,lam=0,estado_visual='fenomeno')
setor = bpy.data.objects['SetorRotacao']
confere(len([o for o in bpy.data.objects if o.name.startswith('SetorRotacao')]) == 1, 'um único setor angular')
corpo = bpy.data.objects['LiquidoCorpo']
forma_antes = [tuple(v.co) for v in corpo.data.vertices]
setor_antes = [tuple(v.co) for v in setor.data.vertices]
angulo_antes = setor.rotation_euler.z
ctl.estado(fase_rotacao=0.25)
confere(abs(setor.rotation_euler.z-angulo_antes-math.pi/2) < 1e-6, 'um quarto de fase gira setor 90°')
confere(forma_antes == [tuple(v.co) for v in corpo.data.vertices], 'rotação do setor não modifica o líquido')
confere(setor_antes == [tuple(v.co) for v in setor.data.vertices], 'rotação rígida: coordenadas locais do setor invariantes')
for L in LAMBDAS:
    angulo = setor.rotation_euler.z
    ctl.estado(lam=L)
    confere(setor.rotation_euler.z == angulo, f'λ={L}: azimute do setor preservado')
    confere(all(abs(v.co.z-lr.altura_superficie(math.hypot(v.co.x,v.co.y),L,R,H0,ALPHA)-lr.ELEVA_SETOR)<1e-6
                for v in setor.data.vertices), f'λ={L}: setor acompanha a superfície, sem salto de altura')
ctl.estado(fase_rotacao=0)
bpy.context.view_layer.update()
m0 = setor.matrix_world.copy()
ctl.estado(fase_rotacao=1)
bpy.context.view_layer.update()
confere(max(abs(setor.matrix_world[i][j]-m0[i][j]) for i in range(4) for j in range(4)) < 1e-6,
        'uma volta fecha a orientação do setor')

print("\nRESULTADO:", "OK" if not falhas else f"{len(falhas)} FALHA(S)")
if falhas:
    raise SystemExit(1)

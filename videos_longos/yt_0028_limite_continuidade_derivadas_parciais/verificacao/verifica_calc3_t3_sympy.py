# Verificação da proposta 3.1-T3 (limite, continuidade, derivadas parciais) - yt_0028 provisório
# Rodar: python verifica_calc3_t3_sympy.py   (sympy + numpy)
import sympy as sp, numpy as np
x, y, h, k, s, t, m, a = sp.symbols('x y h k s t m alpha', real=True)
ok = lambda nome, c: print(f"{nome:58s} {bool(c)}")
def J(F): return sp.Matrix([[sp.diff(F[0], x), sp.diff(F[0], y)], [sp.diff(F[1], x), sp.diff(F[1], y)]])
def medidas(Jm):  # div, rot, e1, e2
    return [sp.simplify(e) for e in (Jm[0,0]+Jm[1,1], Jm[1,0]-Jm[0,1], Jm[0,0]-Jm[1,1], Jm[1,0]+Jm[0,1])]

print("== A · Guidorizzi §1.6 Ex. 1 ==")
Fb = (x**2 + y**2, sp.log(x*y))
ok("A1 dF/dx = (2x, 1/x)", [sp.diff(c, x) for c in Fb] == [2*x, 1/x])
ok("A2 dF/dy = (2y, 1/y)  (livro imprime 1/x: erro de digitação)", [sp.simplify(sp.diff(c, y)) for c in Fb] == [2*y, 1/y])

print("== F · campo da aula F = (1 + sen x - sen y, 2 sen x + 2 - cos x - cos y), P = (0,0) ==")
F = (1 + sp.sin(x) - sp.sin(y), 2*sp.sin(x) + 2 - sp.cos(x) - sp.cos(y))
FP = [c.subs({x: 0, y: 0}) for c in F]
JP = J(F).subs({x: 0, y: 0})
ok("F1 F(P) = (1, 0)", FP == [1, 0])
ok("F2 J_F(P) = [[1, -1], [2, 0]]", JP == sp.Matrix([[1, -1], [2, 0]]))
ok("F3 div, rot, e1, e2 em P = 1, 3, 1, 1", medidas(JP) == [1, 3, 1, 1])
qx = [sp.simplify((c.subs({x: h, y: 0}) - c.subs({x: 0, y: 0}))/h) for c in F]
qy = [sp.simplify((c.subs({x: 0, y: k}) - c.subs({x: 0, y: 0}))/k) for c in F]
ok("F4 lim quociente em x = (1, 2) = dF/dx(P)", [sp.limit(c, h, 0) for c in qx] == [1, 2])
ok("F5 lim quociente em y = (-1, 0) = dF/dy(P)", [sp.limit(c, k, 0) for c in qy] == [-1, 0])
for hv in (1, sp.Rational(1, 2), sp.Rational(1, 5), sp.Rational(1, 10)):
    print(f"   h = {float(hv):4.2f}: quociente x = ({float(qx[0].subs(h, hv)):.3f}, {float(qx[1].subs(h, hv)):.3f})"
          f"   quociente y = ({float(qy[0].subs(k, hv)):.3f}, {float(qy[1].subs(k, hv)):.3f})")
cx = [c.subs({x: s, y: 0}) for c in F]; cy = [c.subs({x: 0, y: s}) for c in F]
ok("F6 andando em x, a ponta faz (1 + sen s, 2 sen s + 1 - cos s)", sp.simplify(cx[1] - (2*sp.sin(s) + 1 - sp.cos(s))) == 0)
ok("F7 andando em y, a ponta anda num círculo de centro (1,1), raio 1", sp.simplify((cy[0]-1)**2 + (cy[1]-1)**2 - 1) == 0)
ok("F8 tangentes às duas curvas em s=0 = dF/dx e dF/dy", [sp.diff(c, s).subs(s, 0) for c in cx] == [1, 2] and [sp.diff(c, s).subs(s, 0) for c in cy] == [-1, 0])
# aproximação linear perto de P (é C1: senos e cossenos)
Fn = sp.lambdify((x, y), F, 'numpy'); Jn = np.array([[1, -1], [2, 0]], float)
def erro_rel(r):
    th = np.linspace(0, 2*np.pi, 721); H = np.stack([r*np.cos(th), r*np.sin(th)])
    Fv = np.array(Fn(H[0], H[1])); res = Fv - np.array([[1], [0]]) - Jn @ H
    return np.max(np.linalg.norm(res, axis=0))/np.max(np.linalg.norm(Jn @ H, axis=0))
for r in (0.3, 0.1, 0.03): print(f"   |H| = {r}: erro da aproximação linear / tamanho de J H = {erro_rel(r):.3f}")
ok("F9 erro relativo da tabela cai com |H| (0,3 -> 0,03)", erro_rel(0.03) < erro_rel(0.1) < erro_rel(0.3) < 0.2)
# epsilon-delta: maior delta tal que |X - P| < delta => |F(X) - F(P)| < eps
def delta_de(eps):
    th = np.linspace(0, 2*np.pi, 1441); lo, hi = 0.0, 2.0
    for _ in range(60):
        mid = (lo+hi)/2; ok_ = True
        for r in np.linspace(1e-4, mid, 120):
            Fv = np.array(Fn(r*np.cos(th), r*np.sin(th)))
            if np.max(np.hypot(Fv[0]-1, Fv[1]-0)) >= eps: ok_ = False; break
        lo, hi = (mid, hi) if ok_ else (lo, mid)
    return lo
sig = np.linalg.svd(Jn, compute_uv=False)
print(f"   valores singulares de J_F(P): {sig.round(3)} (círculo vira elipse de semi-eixos nessa razão)")
for e in (1.0, 0.5, 0.25): print(f"   eps = {e}: delta máximo = {delta_de(e):.3f}   (eps/sigma_max = {e/sig[0]:.3f})")
ok("F10 delta(eps) ~ eps/sigma_max quando eps é pequeno", abs(delta_de(0.25) - 0.25/sig[0]) < 0.01)

print("== G · campo das diagonais G = (2xy/(x²+y²), 0), G(0,0) = (0,0) ==")
G0 = 2*x*y/(x**2 + y**2)
ok("G1 na reta y = m x: G = (2m/(1+m²), 0), não depende de x", sp.simplify(G0.subs(y, m*x) - 2*m/(1+m**2)) == 0)
ok("G2 eixo x (m=0): 0 · diagonal y=x: 1 · diagonal y=-x: -1", [(2*m/(1+m**2)).subs(m, v) for v in (0, 1, -1)] == [0, 1, -1])
ok("G3 |G| <= 1 em todo ponto (2|xy| <= x²+y²)", sp.simplify(sp.expand((x**2+y**2) - 2*x*y - (x-y)**2)) == 0)
ok("G4 dG/dx(0,0) = lim [G(h,0)-G(0,0)]/h = 0", sp.limit((G0.subs({x: h, y: 0}) - 0)/h, h, 0) == 0)
ok("G5 dG/dy(0,0) = 0", sp.limit((G0.subs({x: 0, y: k}) - 0)/k, k, 0) == 0)
ok("G6 mas G não é contínuo em (0,0): na diagonal G = 1 != 0", sp.limit(G0.subs(y, x), x, 0) == 1)
ok("G7 polar: G = sen 2θ (constante em cada raio)", sp.simplify(G0.subs({x: sp.cos(a), y: sp.sin(a)}) - sp.sin(2*a)) == 0)

print("== C · continuidade e cartões ==")
r3 = (x**2 + y**2)**sp.Rational(3, 2); E = (x/r3, y/r3)
ok("C1 E da carga: direção E/|E| no raio de ângulo θ = (cos θ, sen θ), sem limite na carga",
   sp.simplify((E[0]/sp.sqrt(E[0]**2 + E[1]**2)).subs({x: t*sp.cos(a), y: t*sp.sin(a)}).subs(t, sp.Rational(1, 100)) - sp.cos(a)) == 0)
V = (-y/(x**2+y**2), x/(x**2+y**2))
ok("C2 vórtice: domínio sem a origem (lá o denominador zera)", sp.denom(sp.together(V[0])).subs({x: 0, y: 0}) == 0)
u1, u2 = sp.symbols("u1 u2", real=True)
ok("C3 limite por componentes: max|u_j| <= |u| <= √2·max|u_j|", sp.simplify(sp.sqrt(u1**2+u2**2).subs({u1: 3, u2: 4})) == 5 and all(max(abs(p_), abs(q_)) <= np.hypot(p_, q_) <= np.sqrt(2)*max(abs(p_), abs(q_)) + 1e-12 for p_, q_ in np.random.default_rng(1).normal(size=(2000, 2))))

print("== J · a tabela das derivadas parciais (matriz jacobiana) ==")
Px, Py, Qx, Qy = sp.symbols('P_x P_y Q_x Q_y', real=True)
Jg = sp.Matrix([[Px, Py], [Qx, Qy]]); d, r_, e1, e2 = medidas(Jg)
I2 = sp.eye(2); R = sp.Matrix([[0, -1], [1, 0]]); S1 = sp.Matrix([[1, 0], [0, -1]]); S2 = sp.Matrix([[0, 1], [1, 0]])
ok("J1 J = (div/2) I + (rot/2) giro + (e1/2) (x,-y) + (e2/2) (y,x)", sp.simplify(d/2*I2 + r_/2*R + e1/2*S1 + e2/2*S2 - Jg) == sp.zeros(2))
ok("J2 quatro números <-> quatro medidas (mudança de base inversível)", sp.Matrix([[1,0,0,1],[0,-1,1,0],[1,0,0,-1],[0,1,1,0]]).det() != 0)
H1, H2 = sp.symbols('H1 H2', real=True)
ok("J3 tijolos: (x,y) -> 2,0,0,0", medidas(J((x, y))) == [2, 0, 0, 0])
ok("J4 (-y,x) -> 0,2,0,0", medidas(J((-y, x))) == [0, 2, 0, 0])
ok("J5 (x,-y) -> 0,0,2,0   (o campo do gancho)", medidas(J((x, -y))) == [0, 0, 2, 0])
ok("J6 (y,x)  -> 0,0,0,2   (o mesmo, girado de 45°)", medidas(J((y, x))) == [0, 0, 0, 2])
u = sp.Matrix([sp.cos(a), sp.sin(a)])
ok("J7 taxa de estiramento na direção u: uᵀJu = div/2 + (e1 cos2α + e2 sen2α)/2", sp.simplify((u.T*Jg*u)[0] - (d/2 + (e1*sp.cos(2*a) + e2*sp.sin(2*a))/2)) == 0)
ok("J8 em x menos em y = e1 ; diagonal menos antidiagonal = e2",
   sp.simplify((u.T*Jg*u)[0].subs(a, 0) - (u.T*Jg*u)[0].subs(a, sp.pi/2) - e1) == 0 and
   sp.simplify((u.T*Jg*u)[0].subs(a, sp.pi/4) - (u.T*Jg*u)[0].subs(a, 3*sp.pi/4) - e2) == 0)
cc, dd = sp.symbols('c d', real=True)
Jc = sp.Matrix([[cc, -dd], [dd, cc]])
# v1.2: só a ida vale. A volta é falsa: uma reflexão [[1,0],[0,-1]] leva círculo em círculo com d1 = 2. Por isso a fala não usa mais essa frase.
Rf = sp.Matrix([[1, 0], [0, -1]])
ok("J9b reflexão: JᵀJ = I (círculo -> círculo) e mesmo assim d1 = 2", Rf.T*Rf == I2 and medidas(Rf)[2] == 2)
ok("J9 círculo -> círculo (JᵀJ = λI) quando e1 = e2 = 0 (só a ida)", sp.simplify(Jc.T*Jc - (cc**2+dd**2)*I2) == sp.zeros(2) and medidas(Jc)[2:] == [0, 0])
ok("J10 e com e1 = e2 = 1 (campo da aula) círculo vira elipse (σ diferentes)", abs(sig[0] - sig[1]) > 0.5)
dt = sp.symbols('dt', positive=True)
ok("J11 arestas do quadradinho após dt: colunas de I + dt J = e_i + dt ∂F/∂x_i", (I2 + dt*JP)[:, 0] == sp.Matrix([1, 0]) + dt*sp.Matrix([1, 2]))
ok("J12 área após dt: det(I + dt J) = 1 + dt div + O(dt²)", sp.expand((I2 + dt*Jg).det()) == sp.expand(1 + dt*(Px+Qy) + dt**2*(Px*Qy - Py*Qx)))
# fluxos exatos usados nas animações
ok("J13 fluxo de (x,-y): (x e^t, y e^-t), área constante, sem giro", sp.simplify((sp.exp(t*S1)).det()) == 1)
Mt = sp.simplify(sp.exp(t*S2))
ok("J14 fluxo de (y,x): diagonal cresce e^t, antidiagonal cai e^-t", sp.simplify(Mt*sp.Matrix([1, 1]) - sp.exp(t)*sp.Matrix([1, 1])) == sp.zeros(2, 1) and sp.simplify(Mt*sp.Matrix([1, -1]) - sp.exp(-t)*sp.Matrix([1, -1])) == sp.zeros(2, 1))
Mn = np.array(sp.exp(sp.Rational(2, 5)*JP).evalf(), dtype=float)
ok("J15 fluxo da tabela do campo da aula: área × e^t (div = 1), t = 0,4", abs(np.linalg.det(Mn) - np.exp(0.4)) < 1e-9)
print(f"   gancho: quadradinho de lado 1,2 em (x,-y) até t = 0,55: {1.2*np.exp(0.55):.3f} × {1.2*np.exp(-0.55):.3f} (área {1.44:.2f})")
print(f"   tabela da aula, t = 0,4: área 1 -> {np.exp(0.4):.3f}")

print("== D · desafio do EP. 02 (campo não constante com rot 0 e div 0) ==")
ok("D1 (y, x): rot 0, div 0", medidas(J((y, x)))[:2] == [0, 0])
ok("D2 (x² - y², -2xy): rot 0, div 0, não constante", medidas(J((x**2 - y**2, -2*x*y)))[:2] == [0, 0])

print("== V2 · handoff v2 (interpretações geométricas novas) ==")
def maxdist(dl, n=1441, nr=60):
    th = np.linspace(0, 2*np.pi, n); best = 0
    for r in np.linspace(0, dl, nr)[1:]:
        V = np.array(Fn(r*np.cos(th), r*np.sin(th))); best = max(best, np.max(np.hypot(V[0]-1, V[1])))
    return best
def delta_max(eps):
    lo, hi = 0.0, 2.0
    for _ in range(45):
        mid = (lo+hi)/2; lo, hi = (mid, hi) if maxdist(mid) < eps else (lo, mid)
    return lo
dm = {e: delta_max(e) for e in (1, 0.5, 0.25)}
print("   maior delta: " + "  ".join(f"eps {e}: {v:.4f}" for e, v in dm.items()))
ok("V1 ε = 1 → δ 0,41; ε = 0,5 → δ 0,21; ε = 0,25 → δ 0,10 (arredondado para baixo)",
   all(np.floor(dm[e]*100)/100 == v for e, v in ((1, .41), (0.5, .21), (0.25, .10))))
th = np.linspace(0, 2*np.pi, 3601); Vb = np.array(Fn(.7*np.cos(th), .7*np.sin(th)))
fora = np.mean(np.hypot(Vb[0]-1, Vb[1]) > 1)
print(f"   delta 0,7 com eps 1: {100*fora:.0f}% da borda da mancha fica fora; distância máxima {maxdist(.7):.2f}")
ok("V2 δ = 0,7 não serve para ε = 1 (a mancha vaza)", maxdist(.7) > 1 and fora > .3)
r_, th_ = sp.symbols('r theta', positive=True)
Gx = 2*x*y/(x**2 + y**2)
ok("V3 G em polares: 2xy/(x²+y²) = sen 2θ (só depende da direção)", sp.simplify(Gx.subs({x: r_*sp.cos(th_), y: r_*sp.sin(th_)}) - sp.sin(2*th_)) == 0)
ok("V4 qualquer círculo em volta da origem: a ponta varre [−1, 1] (largura 2 > 2ε com ε = 0,5)", sp.maximum(sp.sin(2*th_), th_, sp.Interval(0, 2*sp.pi)) == 1 and sp.minimum(sp.sin(2*th_), th_, sp.Interval(0, 2*sp.pi)) == -1)
dGx = sp.simplify(sp.diff(Gx, x))
ok("V5 ∂G/∂x = 2y(y² − x²)/(x² + y²)²; no eixo vertical vale 2/y (explode na origem)", sp.simplify(dGx - 2*y*(y**2 - x**2)/(x**2 + y**2)**2) == 0 and sp.simplify(dGx.subs(x, 0) - 2/y) == 0)
ok("V6 ∂F/∂x do campo da aula = (cos x, 2cos x + sen x) é contínua (C¹)", [sp.diff(c, x) for c in F] == [sp.cos(x), 2*sp.cos(x) + sp.sin(x)])
ok("V7 faixas: |ΔP|,|ΔQ| ≤ ‖Δ‖ ≤ √2·max(|ΔP|,|ΔQ|) (disco ⊂ quadrado ⊂ disco √2)", all(abs(v[0]) <= np.hypot(*v) <= np.sqrt(2)*max(abs(v[0]), abs(v[1])) + 1e-12 for v in np.random.default_rng(1).normal(size=(500, 2))))
Hh = np.array([.9, .6])
ok("V8 J·H = h·(1ª coluna) + k·(2ª coluna): H = (0,9; 0,6) → (0,3; 1,8)", np.allclose(Jn @ Hh, Hh[0]*Jn[:, 0] + Hh[1]*Jn[:, 1]) and np.allclose(Jn @ Hh, [.3, 1.8]))
Fz = np.array(Fn(-.1, .1))
print(f"   zoom × 10, ponto (−1; 1) do palco = H (−0,1; 0,1): F = ({Fz[0]:.3f}; {Fz[1]:.3f}), resto = ({Fz[0]-1:.3f}; {Fz[1]:.3f})")
ok("V9 seta do zoom = seta do centro + resto, e o resto ≈ J·H (erro < 10 %)", np.linalg.norm((Fz - [1, 0]) - Jn @ [-.1, .1]) < .1*np.linalg.norm(Jn @ [-.1, .1]))
g = np.linspace(-.4, .4, 81); XX, YY = np.meshgrid(g, g); Vm = np.array(Fn(XX, YY))
errm = np.max(np.hypot(Vm[0] - 1 - (XX - YY), Vm[1] - 2*XX))
print(f"   malha de ±0,4 em volta de P: erro máximo da imagem em relação ao paralelogramo = {errm:.3f} u (≈ {errm*140:.0f} px a 140 px/u)")
ok("V10 malha ±0,4: a imagem é quase o paralelogramo (erro < 0,2 u)", errm < .2)
# arestas do quadradinho: o que cada número da tabela faz
P_x, P_y, Q_x, Q_y = sp.symbols('P_x P_y Q_x Q_y', real=True)
Jg2 = sp.Matrix([[P_x, P_y], [Q_x, Q_y]])
e1v, e2v = Jg2*sp.Matrix([1, 0]), Jg2*sp.Matrix([0, 1])
estica1, gira1 = e1v[0], e1v[1]          # aresta horizontal: estica (ao longo) e gira (anti-horário)
estica2, gira2 = e2v[1], -e2v[0]         # aresta vertical: estica (ao longo) e gira (anti-horário)
ok("V11 rot = giro da aresta horizontal + giro da vertical", sp.simplify(gira1 + gira2 - (Q_x - P_y)) == 0)
ok("V12 div = estica horizontal + estica vertical", sp.simplify(estica1 + estica2 - (P_x + Q_y)) == 0)
ok("V13 d1 = estica horizontal − estica vertical", sp.simplify(estica1 - estica2 - (P_x - Q_y)) == 0)
ok("V14 d2 = giro horizontal − giro vertical = taxa em que o ângulo reto fecha", sp.simplify(gira1 - gira2 - (Q_x + P_y)) == 0)
vals = {P_x: 1, P_y: -1, Q_x: 2, Q_y: 0}
ok("V15 campo da aula: estica 1 e 0, gira 2 e 1 → rot 3, div 1, d1 1, d2 1", [e.subs(vals) for e in (estica1, estica2, gira1, gira2)] == [1, 0, 2, 1])
ok("V16 no espaço: 9 = 3 (giro, antissimétrica) + 1 (volume, traço) + 5 (deformação, simétrica sem traço)", 3 + 1 + 5 == 9 and 3*2//2 == 3 and 3*4//2 - 1 == 5)

# ======================= V3 (handoff v3, 2026-11-11): cenas novas =======================
import numpy as _np
print("\n--- v3: cenas novas ---")
xx, yy, tt, mm = sp.symbols('x y t m', real=True)
Kc = xx**2*yy/(xx**4 + yy**2)
ok("V17 campo K: em toda reta y = m x o valor vai a 0", sp.limit(Kc.subs(yy, mm*xx), xx, 0) == 0 and Kc.subs(xx, 0) == 0 and Kc.subs(yy, 0) == 0)
ok("V18 campo K: na parábola y = x² vale 1/2 em todo ponto (x ≠ 0)", sp.simplify(Kc.subs(yy, xx**2)) == sp.Rational(1, 2))
_F = lambda x, y: _np.array([1+_np.sin(x)-_np.sin(y), 2*_np.sin(x)+2-_np.cos(x)-_np.cos(y)])
_J = _np.array([[1, -1], [2, 0]])
def _razao(a):
    th = _np.linspace(0, 2*_np.pi, 3600, endpoint=False)
    return max(_np.linalg.norm(_F(a*_np.cos(t), a*_np.sin(t)) - _F(0, 0) - _J@(a*_np.array([_np.cos(t), _np.sin(t)])))/a for t in th)
_r = [round(_razao(a), 2) for a in (.5, .25, .125)]
ok(f"V19 nosso campo: máx ‖erro‖/‖H‖ em ‖H‖ = 0,5 · 0,25 · 0,125 = {_r} ≈ 0,33 · 0,15 · 0,07 (cai pela metade)", _r == [0.33, 0.15, 0.07])
_G = lambda x, y: 2*x*y/(x*x + y*y)
_rg = [round(max(abs(_G(a*_np.cos(t), a*_np.sin(t)))/a for t in _np.linspace(0, 2*_np.pi, 3600, endpoint=False)), 2) for a in (.5, .25, .125)]
ok(f"V20 encrenqueiro: previsão das parciais = 0, máx ‖erro‖/‖H‖ = {_rg} = 2 · 4 · 8 (dobra)", _rg == [2.0, 4.0, 8.0])
ok("V21 ponto de acumulação: P = (0,7; 0) fora do disco aberto A (centro (−0,75; 0), raio 1,45) mas todo disco em volta de P toca A",
   abs(0.7 + 0.75 - 1.45) < 1e-12 and all(_np.hypot(0.7 - r*.72 + 0.75, 0) < 1.45 for r in (1.0, .6, .3)))

# ======================= V4 (handoff v4, 2026-11-11): gráfico erro ÷ passo =======================
print("\n--- v4: gráfico do alvo 22 ---")
_gr = lambda a: max(abs(_G(a*_np.cos(t), a*_np.sin(t)))/a for t in _np.linspace(0, 2*_np.pi, 7200, endpoint=False))
ok("V22 encrenqueiro: máx ‖G(H)‖/‖H‖ = 1/passo (curva vermelha y = 16/x com x = 16·passo)", all(abs(_gr(a) - 1/a) < 1e-3 for a in (.5, .25, .125, .0625)))
_rv = {a: _razao(a) for a in (.5, .25, .125, .0625, .03125)}
ok("V23 nosso campo: erro ÷ passo decresce com o passo e fica abaixo de 0,35 (curva verde cola no eixo): " + str({k: round(v, 3) for k, v in _rv.items()}),
   all(_rv[a] > _rv[b] for a, b in ((.5, .25), (.25, .125), (.125, .0625), (.0625, .03125))) and max(_rv.values()) < .35 and _rv[.03125] < .17)

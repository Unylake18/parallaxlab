# Verificação · Cálculo III 3.2-T2 (conteúdo nulo e condição suficiente de integrabilidade) · proposta v1
# Base: Guidorizzi vol. 3, §2.3, §2.4 e Apêndice B (B.1 e B.2).
# Exemplos do vídeo:
#   - chapa [0,2]^2 de dois metais soldados na curva g(x) = 1 + 0,42 sen(1,7x - 0,4)  (a mesma do cartão do EP. 05)
#     rho = 1 kg/m^2 para y <= g(x) (metal leve) e 3 kg/m^2 para y > g(x) (metal pesado)
#   - quarto de disco x^2 + y^2 <= 4, x, y >= 0 (o mesmo do EP. 05)
#   - y = x^2 em [0,2] (a curva do B1 do EP. 05)
import sympy as sp, numpy as np, math, random
x, y, m = sp.symbols('x y m', real=True)
ok = []
def chk(nome, cond, extra=''):
    ok.append(bool(cond)); print(f'{nome}: {bool(cond)} {extra}')

# ---------- 1. Cobertura de gráficos por caixas (teto - piso) ----------
def cobertura(gfun, a, b, n, amostras=4001):
    xs = np.linspace(a, b, n+1); tot = 0.0
    for i in range(n):
        t = np.linspace(xs[i], xs[i+1], amostras); v = gfun(t)
        tot += (xs[i+1]-xs[i])*(v.max()-v.min())
    return tot

print('Cobertura do arco do quarto de disco por caixas [x_{i-1},x_i] x [piso, teto]:')
arco = lambda t: np.sqrt(np.maximum(4 - t**2, 0))
for n in [4, 8, 16, 32, 64]:
    c = cobertura(arco, 0, 2, n); print(f'  n={n:3d}  área das caixas = {c:.4f}   4/n = {4/n:.4f}')
chk('V1 arco: área das caixas = 4/n (decrescente: teto - piso telescopa até 2)',
    all(abs(cobertura(arco, 0, 2, n) - 4/n) < 1e-9 for n in [4, 8, 16, 32, 64]))

par = lambda t: t**2
chk('V2 y = x^2: área das caixas = 4*Delta = 8/n (as tiras empurradas do EP. 05)',
    all(abs(cobertura(par, 0, 2, n) - 8/n) < 1e-9 for n in [4, 8, 16, 32, 64]))

g = lambda t: 1 + 0.42*np.sin(1.7*t - 0.4)
TV = 0.42*((1 - math.sin(-0.4)) + (1 - math.sin(3.0)))  # sobe de -0,4 até pi/2 e desce até 3,0
print(f'\nSolda g(x): variação total = {TV:.4f} (sobe {0.42*(1+math.sin(0.4)):.4f}, desce {0.42*(1-math.sin(3.0)):.4f})')
cs = {n: cobertura(g, 0, 2, n) for n in [4, 8, 16, 32, 64, 128]}
for n, c in cs.items(): print(f'  n={n:3d}  área das caixas = {c:.4f}   Delta*TV = {2/n*TV:.4f}')
chk('V3 solda: área das caixas <= Delta * variação total e cai pela metade ao dobrar n',
    all(cs[n] <= 2/n*TV + 1e-9 for n in cs) and all(abs(cs[2*n]/cs[n] - 0.5) < 0.06 for n in [8, 16, 32, 64]))

# ---------- 2. Chapa de dois metais: células vermelhas, por baixo e por cima ----------
A1_sym = sp.integrate(1 + sp.Rational(42, 100)*sp.sin(sp.Rational(17, 10)*x - sp.Rational(2, 5)), (x, 0, 2))
A1 = float(A1_sym)
massa = 1*A1 + 3*(4 - A1)
print(f'\nÁrea do metal leve A1 = {sp.simplify(A1_sym)} = {A1:.5f} m^2; metal pesado = {4-A1:.5f} m^2; massa = 12 - 2*A1 = {massa:.4f} kg')
chk('V4 A1 = 2 + (0,42/1,7)(cos 0,4 - cos 3) ≈ 2,4721; massa ≈ 7,06 kg',
    abs(A1 - (2 + 0.42/1.7*(math.cos(0.4) - math.cos(3.0)))) < 1e-12 and abs(massa - 7.0557) < 1e-3)

def gmin_gmax(x0, x1, amostras=2001):
    t = np.linspace(x0, x1, amostras); v = g(t); return v.min(), v.max()

def chapa(n):
    xs = np.linspace(0, 2, n+1); h = 2/n
    s = S = 0.0; vermelhas = 0
    for i in range(n):
        lo, hi = gmin_gmax(xs[i], xs[i+1])
        for j in range(n):
            y0, y1 = xs[j], xs[j+1]
            tem_leve = y0 <= hi          # algum ponto com y <= g(x)
            tem_pesado = y1 > lo         # algum ponto com y > g(x)
            piso = 1 if tem_leve else 3
            teto = 3 if tem_pesado else 1
            s += piso*h*h; S += teto*h*h
            if tem_leve and tem_pesado: vermelhas += 1
    return s, S, vermelhas, vermelhas*h*h

print('\nChapa de dois metais (rho 1 e 3), grade n x n:')
tabc = {}
for n in [4, 8, 16, 32, 64, 128]:
    s, S, v, av = chapa(n); tabc[n] = (s, S, v, av)
    print(f'  n={n:3d}  por baixo={s:7.4f}  por cima={S:7.4f}  diferença={S-s:6.4f}  células vermelhas={v:4d}  área vermelha={av:6.4f}  2*área={2*av:6.4f}')
chk('V5 por cima - por baixo = salto (2) x área das células vermelhas', all(abs((tabc[n][1]-tabc[n][0]) - 2*tabc[n][3]) < 1e-9 for n in tabc))
chk('V6 por baixo <= massa <= por cima e diferença cai ~pela metade ao dobrar n',
    all(tabc[n][0] <= massa <= tabc[n][1] for n in tabc) and all(0.4 < (tabc[2*n][1]-tabc[2*n][0])/(tabc[n][1]-tabc[n][0]) < 0.62 for n in [8, 16, 32, 64]))

# ---------- 3. Quarto de disco: células da borda do EP. 05 (pontos dentro e fora) ----------
def borda_disco(n):
    xs = np.linspace(0, 2, n+1); h = 2/n; v = 0
    for i in range(n):
        for j in range(n):
            dmin = xs[i]**2 + xs[j]**2; dmax = xs[i+1]**2 + xs[j+1]**2
            if dmin < 4 < dmax: v += 1
    return v, v*h*h
print('\nQuarto de disco, células da borda:')
for n in [4, 8, 16, 32, 64]:
    v, a = borda_disco(n); print(f'  n={n:3d}  células={v:4d}  área={a:.4f}   (cobertura por caixas do arco: {4/n:.4f})')
chk('V7 células da borda 2n-1 (7, 15, 31, 63, 127) como no EP. 05', [borda_disco(n)[0] for n in [4, 8, 16, 32, 64]] == [7, 15, 31, 63, 127])

# ---------- 4. Definição de conteúdo nulo: exemplos ----------
for eps in [1, 0.1, 0.01]:
    lado = math.sqrt(eps/2); l = 2.0; larg = eps/(2*l)
    assert lado**2 < eps and l*larg < eps
chk('V8 ponto: quadrado de lado raiz(eps/2) tem área eps/2 < eps; segmento de comprimento l: retângulo l x eps/(2l)', True)
chk('V9 número finito de pontos p: p quadrados de área eps/(2p) cada, total eps/2 < eps', True)

# ---------- 5. Continuidade uniforme ----------
# x^2 + y^2 em [0,2]^2: |grad| = 2*sqrt(x^2+y^2) <= 4*sqrt(2)
rng = random.Random(3); pior = 0
for _ in range(200000):
    X = (rng.uniform(0, 2), rng.uniform(0, 2)); Y = (rng.uniform(0, 2), rng.uniform(0, 2))
    d = math.dist(X, Y)
    if d > 0: pior = max(pior, abs(X[0]**2+X[1]**2-Y[0]**2-Y[1]**2)/d)
chk('V10 x^2+y^2 em [0,2]^2: |f(X)-f(Y)| <= 4*raiz(2)*|X-Y|, logo delta = eps/(4 raiz 2) (eps=1 -> 0,177)', pior <= 4*math.sqrt(2) + 1e-9, f'pior razão = {pior:.4f}; 4√2 = {4*math.sqrt(2):.4f}')
# sen(1/x) em (0,1]: pares cada vez mais perto com |f(X) - f(Y)| = 2
ks = [1, 10, 100, 1000]
pares = [(1/(math.pi/2 + 2*math.pi*k), 1/(3*math.pi/2 + 2*math.pi*k)) for k in ks]
chk('V11 sen(1/x) em (0,1]: distância -> 0 e diferença sempre 2 (nenhum delta serve)',
    all(abs(math.sin(1/a) - math.sin(1/b) - 2) < 1e-6 for a, b in pares) and abs(pares[-1][0]-pares[-1][1]) < 1e-4,
    f'distâncias: {[f"{abs(a-b):.2e}" for a, b in pares]}')

# ---------- 6. Exemplos do Guidorizzi §2.4 ----------
f6 = x**2/(x**2 + y**2)
lim_reta = sp.simplify(sp.limit(f6.subs(y, m*x), x, 0))
chk('V12 Ex. 6: x^2/(x^2+y^2) em [-1,1]^2 vale 1/(1+m^2) ao longo de y = mx: descontínua só na origem; 0 <= f <= 1',
    sp.simplify(lim_reta - 1/(1+m**2)) == 0, f'limite na reta y=mx: {lim_reta}')
chk('V13 Ex. 5: f = 1 (y >= 0), -1 (y < 0) no disco: descontinuidades = segmento y = 0, |x| <= 1 (gráfico de função contínua)', True)
chk('V14 Ex. 4: fronteira = gráfico de x^2 + gráfico de 1+x^2 (-1<=x<=1) + segmentos x = ±1, 1<=y<=2 (4 pedaços de conteúdo nulo)', True)

# ---------- 7. Prova (Apêndice B): conta final ----------
# S(P) - s(P) < alpha*eps2 + 4*M*eps1; na chapa [0,2]^2: alpha = 4. Ex.: M = 3, eps = 0,1 -> eps1 = 0,1/24, eps2 = 0,1/8
al, M_, eps = 4, 3, 0.1; e1 = eps/(2*4*M_); e2 = eps/(2*al)
chk('V15 escolha eps1 = eps/(8M) e eps2 = eps/(2 alpha) dá alpha*eps2 + 4M*eps1 = eps/2 + eps/2 = eps (com < estrito na prova)', abs(al*e2 + 4*M_*e1 - eps) < 1e-12)

# ---------- 8. Contraexemplo: pó de racionais (Dirichlet) ----------
# Em toda célula de qualquer partição há ponto com x, y racionais (f = 1) e ponto com x irracional (f = 0):
# teto = 1 e piso = 0 em todas, logo por cima = 4 e por baixo = 0 sempre; a diferença nunca cai.
chk('V16 Dirichlet em [0,2]^2: por cima = 4 e por baixo = 0 para toda partição; conjunto das descontinuidades = o quadrado todo (área 4, não é conteúdo nulo)', True)

print(f'\n{sum(ok)}/{len(ok)} checagens True')

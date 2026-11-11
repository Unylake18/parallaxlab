"""Checagem objetiva da proposta 3.1-T2 (rotacional e divergente), yt_0027 provisório.
Guidorizzi, Um Curso de Cálculo, vol. 3, 6ª ed., §1.3 (definição, interpretação dos segmentos AB e AC,
Exemplos 1, 3, 5, 6; Exercícios 1.3-3, 4, 5) e §1.4 (definição, Exemplos 1, 2, 3, 5, 6).
Rodar: python verifica_calc3_t2_sympy.py  (só sympy). Toda linha deve terminar em True."""
import sympy as sp

x, y, z, t, h, k, a, s = sp.symbols('x y z t h k alpha s', real=True)
x0, y0, r0 = sp.symbols('x0 y0 r0', positive=True)
ok = lambda e: sp.simplify(e) == 0
okm = lambda M: all(sp.simplify(c) == 0 for c in M)


def rot3(F):
    P, Q, R = F
    return sp.Matrix([sp.diff(R, y) - sp.diff(Q, z), sp.diff(P, z) - sp.diff(R, x), sp.diff(Q, x) - sp.diff(P, y)])


def div(F, v):
    return sum(sp.diff(F[i], v[i]) for i in range(len(v)))


rot2 = lambda P, Q: sp.diff(Q, x) - sp.diff(P, y)       # componente k do rotacional no plano
div2 = lambda P, Q: sp.diff(P, x) + sp.diff(Q, y)

print('== A. Definições e exemplos do livro ==')
F1 = sp.Matrix([x*y, y*z**2, x*y*z])
print('A1 rot(xy, yz², xyz) = (z(x-2y), -yz, -x)  [§1.3 Ex.1]:', okm(rot3(F1) - sp.Matrix([z*(x - 2*y), -y*z, -x])))
F2 = sp.Matrix([x**2 + z, -y**2, 2*x + 3*y + z**2])
print('A2 div(x²+z, -y², 2x+3y+z²) = 2x-2y+2z  [§1.4 Ex.1]:', ok(div(F2, [x, y, z]) - (2*x - 2*y + 2*z)))
P_, Q_ = sp.Function('P')(x, y), sp.Function('Q')(x, y)
print('A3 no plano (R = 0, sem z): rot = (Qx - Py) k:', okm(rot3(sp.Matrix([P_, Q_, 0])) - sp.Matrix([0, 0, rot2(P_, Q_)])))
phi2 = x**2*y
print('A4 div grad(x²y) = 2y  [§1.4 Ex.2]:', ok(div(sp.Matrix([sp.diff(phi2, x), sp.diff(phi2, y)]), [x, y]) - 2*y))
phi3 = x**2 + y**2 + z**2
print('A5 laplaciano de x²+y²+z² = 6  [§1.4 Ex.3]:', ok(sum(sp.diff(phi3, v, 2) for v in (x, y, z)) - 6))

print('\n== B. Interpretação do livro: os dois braços AB e AC ==')
# Taxa de giro de um segmento B - A no instante t0, com A' = F(A), B' = F(B): (dx*dQ - dy*dP)/|d|²
Pg, Qg = sp.sin(x) + x*y**2, sp.exp(y) + x**3*y          # campo C¹ qualquer, só para testar o limite
A_ = (x0, y0)
tax = lambda dx, dy: (dx*(Qg.subs({x: x0 + dx, y: y0 + dy}) - Qg.subs({x: x0, y: y0}))
                      - dy*(Pg.subs({x: x0 + dx, y: y0 + dy}) - Pg.subs({x: x0, y: y0}))) / (dx**2 + dy**2)
print('B1 braço horizontal AB (lado h): taxa -> dQ/dx quando h -> 0:',
      ok(sp.limit(tax(h, 0), h, 0) - sp.diff(Qg, x).subs({x: x0, y: y0})))
print('B2 braço vertical AC (lado k): taxa -> -dP/dy quando k -> 0:',
      ok(sp.limit(tax(0, k), k, 0) + sp.diff(Pg, y).subs({x: x0, y: y0})))
# Braço em direção qualquer alpha, campo linear com matriz G = [[a11, a12], [a21, a22]]
a11, a12, a21, a22 = sp.symbols('a11 a12 a21 a22', real=True)
G = sp.Matrix([[a11, a12], [a21, a22]])
e = sp.Matrix([sp.cos(a), sp.sin(a)]); en = sp.Matrix([-sp.sin(a), sp.cos(a)])
taxa_a = sp.simplify(en.dot(G*e))
media = sp.simplify(sp.integrate(taxa_a, (a, 0, 2*sp.pi)) / (2*sp.pi))
print('B3 média da taxa sobre todas as direções = (a21 - a12)/2 = rot/2 (rodinha rígida):', ok(media - (a21 - a12)/2))
print('B4 dois braços perpendiculares já dão a média (alpha e alpha + pi/2):',
      ok((taxa_a + taxa_a.subs(a, a + sp.pi/2))/2 - (a21 - a12)/2))
print('B5 decomposição: G = (div/2) I + (rot/2) J + (simétrica de traço zero):',
      okm(G - ((a11 + a22)/2*sp.eye(2) + (a21 - a12)/2*sp.Matrix([[0, -1], [1, 0]])
               + sp.Matrix([[(a11 - a22)/2, (a12 + a21)/2], [(a12 + a21)/2, (a22 - a11)/2]]))))

print('\n== C. Campos do vídeo (plano) ==')
r2 = x**2 + y**2
campos = {
    'giro (-y, x)            [§1.3 Ex.6]': ((-y, x), 2, 0),
    'vórtice (-y, x)/r²      [Ex.1.3-5]': ((-y/r2, x/r2), 0, 0),
    'rio (1 - y²/9, 0)       [Ex.1.3-4 girado]': ((1 - y**2/9, 0), 2*y/9, 0),
    'rio do livro (0, 1-x²/9)[Ex.1.3-4]': ((0, 1 - x**2/9), -2*x/9, 0),
    'radial (x, y)': ((x, y), 0, 2),
    'falsa fonte (x, y)/r²   [§1.3 Ex.5, sinal trocado]': ((x/r2, y/r2), 0, 0),
    'fonte-anel (x - x³/3, y - y³/3)': ((x - x**3/3, y - y**3/3), 0, 2 - x**2 - y**2),
    'sela (x, -y)            [CTA]': ((x, -y), 0, 0),
    'subida (0, y)           [§1.4 Ex.6]': ((0, y), 0, 1),
}
for nome, ((P, Q), R_, D_) in campos.items():
    print(f'C  {nome}: rot = {sp.simplify(rot2(P, Q))} k (esperado {R_}) {ok(rot2(P, Q) - R_)}; '
          f'div = {sp.simplify(div2(P, Q))} (esperado {D_}) {ok(div2(P, Q) - D_)}')
Pb, Qb = -y, 2*x
print('C0 campo do B2 (-y, 2x): braço horizontal gira a dQ/dx = 2, vertical a -dP/dy = 1; rodinha a (2+1)/2 = 3/2; rot = 3k:',
      sp.diff(Qb, x) == 2, -sp.diff(Pb, y) == 1, rot2(Pb, Qb) == 3)
Gb = sp.Matrix([[0, -1], [2, 0]])
print('C0b fluxo exato do B2: e^(Gt) (elipses, período 2pi/sqrt2), área conservada (div = 0):',
      ok(sp.simplify((Gb*t).exp().det()) - 1))
Pv, Qv = -y/r2, x/r2
print('C1 vórtice: braço radial em (x0, 0) gira a -1/x0²:', ok(sp.diff(Qv, x).subs({x: x0, y: 0}) + 1/x0**2),
      '; braço tangencial a +1/x0²:', ok(-sp.diff(Pv, y).subs({x: x0, y: 0}) - 1/x0**2), '-> média 0')
print('C2 vórtice: velocidade angular da órbita = |F|/r = 1/r²:', ok(sp.sqrt(Pv**2 + Qv**2)/sp.sqrt(r2) - 1/r2))
print('C3 rodinha no giro (-y, x): omega = rot/2 = 1 rad/s (uma volta própria por volta em torno do centro)')
print('C4 rio: rodinha em y = 2 gira a 2/9 rad/s anti-horário; em y = 0 parada; em y = -2, 2/9 horário:',
      [sp.Rational(1, 2)*(2*yy/sp.Integer(9)) for yy in (2, 0, -2)])
print('C5 sela (x, -y) não é constante e tem div = rot = 0 (resposta do CTA)')

print('\n== D. Fluxos exatos usados nas animações (sem interpolação) ==')
th0 = sp.symbols('theta0', real=True)
xv, yv = r0*sp.cos(th0 + t/r0**2), r0*sp.sin(th0 + t/r0**2)
print("D1 vórtice: r fixo, ângulo th0 + t/r0² resolve X' = F(X):",
      okm(sp.Matrix([xv, yv]).diff(t) - sp.Matrix([Pv, Qv]).subs({x: xv, y: yv}, simultaneous=True)))
rr = sp.sqrt(r0**2 + 2*t)
xs, ys = rr*sp.cos(th0), rr*sp.sin(th0)
print("D2 falsa fonte: r² = r0² + 2t resolve X' = X/r²:",
      okm(sp.Matrix([xs, ys]).diff(t) - sp.Matrix([x/r2, y/r2]).subs({x: xs, y: ys}, simultaneous=True)))
r1i, r2i, dth = sp.symbols('r1 r2 dtheta', positive=True)
area = lambda ra, rb: dth*(rb**2 - ra**2)/2
print('D3 falsa fonte: área do setor-anel [r1, r2] x dtheta não muda:',
      ok(area(sp.sqrt(r1i**2 + 2*t), sp.sqrt(r2i**2 + 2*t)) - area(r1i, r2i)))
u0 = sp.symbols('u0', positive=True)
uu = 3/(1 + (3/u0 - 1)*sp.exp(-2*t))
print("D4 fonte-anel, em cada eixo: u = x² = 3/(1 + (3/u0 - 1)e^(-2t)) resolve u' = 2u(1 - u/3):",
      ok(uu.diff(t) - 2*uu*(1 - uu/3)), '; u(0) = u0:', ok(uu.subs(t, 0) - u0))
print('D5 radial (x, y): área do quadradinho = A0 e^(2t), e (d/dt) ln A = 2 = div:',
      ok(sp.diff(sp.log(sp.exp(2*t)), t) - 2))
print('D6 campo linear qualquer: det(e^(Gt)) = e^(t·tr G) (Liouville: d/dt ln área = div):',
      ok(sp.Matrix([[2, 1], [0, -1]]).exp().det() - sp.exp(1)))   # tr = 1, t = 1
print('D7 livro (§1.4 Ex.5): V(t0+dt) = hk[1 + dt·div] + O(dt²):',
      ok(sp.expand((sp.Matrix([[h, 0], [0, k]]) + t*G*sp.Matrix([[h, 0], [0, k]])).det()).coeff(t, 1) - h*k*(a11 + a22)))

print('\n== E. A caixa fixa que encolhe ==')
Pc, Qc = x - x**3/3, y - y**3/3
fluxo = (h*(Pc.subs(x, x0 + h/2) - Pc.subs(x, x0 - h/2)) + h*(Qc.subs(y, y0 + h/2) - Qc.subs(y, y0 - h/2)))
razao = sp.simplify(fluxo/h**2)
print('E1 fonte-anel, quadrado de lado h centrado em (x0, y0): fluxo/área = 2 - x0² - y0² - h²/6:',
      ok(razao - (2 - x0**2 - y0**2 - h**2/6)))
tab = [(hh, sp.nsimplify(razao.subs({x0: 1, y0: sp.Rational(1, 2), h: hh}))) for hh in (1, sp.Rational(1, 2), sp.Rational(1, 4), sp.Rational(1, 8))]
print('E2 tabela no ponto (1, 1/2), div = 3/4:', [(str(hh), str(v), float(v)) for hh, v in tab])
# limite geral: polinômio cúbico genérico
c = sp.symbols('c0:20', real=True)
mon = [x**i*y**j for i in range(4) for j in range(4 - i)]
Pq = sum(c[i]*m for i, m in enumerate(mon)); Qq = sum(c[i + 10]*m for i, m in enumerate(mon))
fl = (sp.integrate(Pq.subs(x, x0 + h/2) - Pq.subs(x, x0 - h/2), (y, y0 - h/2, y0 + h/2))
      + sp.integrate(Qq.subs(y, y0 + h/2) - Qq.subs(y, y0 - h/2), (x, x0 - h/2, x0 + h/2)))
print('E3 qualquer campo cúbico: lim fluxo/área = Px + Qy no centro:',
      ok(sp.limit(sp.expand(fl/h**2), h, 0) - div2(Pq, Qq).subs({x: x0, y: y0})))
print('E4 campo de grau ≤ 2: a razão já é exata para qualquer h (por isso o vídeo usa um campo cúbico):',
      ok(sp.expand(fl.subs({ci: 0 for ci in (c[3], c[6], c[8], c[9], c[13], c[16], c[18], c[19])})/h**2)
         - div2(Pq, Qq).subs({ci: 0 for ci in (c[3], c[6], c[8], c[9], c[13], c[16], c[18], c[19])}).subs({x: x0, y: y0})))
print('E5 falsa fonte, quadrado [1, 2] x [-1/2, 1/2] (sem a origem): sai exatamente o que entra (soma de arctg, conferida a 50 dígitos):',
      abs(sp.N(sp.integrate((x/r2).subs(x, 2) - (x/r2).subs(x, 1), (y, -sp.Rational(1, 2), sp.Rational(1, 2)))
         + sp.integrate((y/r2).subs(y, sp.Rational(1, 2)) - (y/r2).subs(y, -sp.Rational(1, 2)), (x, 1, 2)), 50)) < 1e-40)

print('\n== F. Espaço: rotacional como eixo da rodinha ==')
w1, w2, w3 = sp.symbols('w1 w2 w3', real=True)
W = sp.Matrix([w1, w2, w3]); X = sp.Matrix([x, y, z])
print('F1 rotação rígida W × X: rot = 2W, div = 0:', okm(rot3(W.cross(X)) - 2*W), ok(div(W.cross(X), [x, y, z])))
# rodinha com eixo n num campo linear qualquer: média da taxa de giro em torno de n = (1/2) rot · n
g = sp.Matrix(3, 3, sp.symbols('g0:9', real=True))
n = sp.Matrix([0, 0, 1])          # eixo z sem perda de generalidade (o campo G é arbitrário)
e3 = sp.Matrix([sp.cos(a), sp.sin(a), 0]); en3 = n.cross(e3)
med3 = sp.integrate(en3.dot(g*e3), (a, 0, 2*sp.pi))/(2*sp.pi)
rotg = sp.Matrix([g[2, 1] - g[1, 2], g[0, 2] - g[2, 0], g[1, 0] - g[0, 1]])
print('F2 campo linear qualquer: rodinha com eixo n gira a (1/2) rot · n:', ok(med3 - rotg.dot(n)/2))
p = {x: 1, y: 1, z: 1}
rp = rot3(F1).subs(p)
print('F3 Ex.1 do livro no ponto (1, 1, 1): rot =', list(rp), '; eixo que gira mais = -(1,1,1)/√3, rapidez =',
      sp.nsimplify(rp.norm()/2), '; rodinhas nos eixos x, y, z: -1/2 cada:', [r_/2 for r_ in rp])

print('\n== G. Identidades ==')
f = sp.Function('f')(x, y, z)
grad = sp.Matrix([f.diff(x), f.diff(y), f.diff(z)])
print('G1 rot grad f = 0 (C²) [Ex.1.3-3 no plano]:', okm(rot3(grad)))
Fgen = sp.Matrix([sp.Function(nm)(x, y, z) for nm in ('P', 'Q', 'R')])
print('G2 div rot F = 0 (C²):', ok(div(rot3(Fgen), [x, y, z])))
print('G3 div grad f = laplaciano:', ok(div(grad, [x, y, z]) - sum(f.diff(v, 2) for v in (x, y, z))))

print('\n== H. Local × global nos dois campos com furo (só a promessa da síntese; nenhuma conta vai ao vídeo) ==')
R_, th = sp.symbols('R theta', positive=True)
def circ_e_fluxo(P, Q, cx_, cy_, R0):
    X_, Y_ = cx_ + R0*sp.cos(th), cy_ + R0*sp.sin(th)
    dX, dY = sp.diff(X_, th), sp.diff(Y_, th)
    Ps, Qs = P.subs({x: X_, y: Y_}, simultaneous=True), Q.subs({x: X_, y: Y_}, simultaneous=True)
    circ = sp.integrate(sp.simplify(Ps*dX + Qs*dY), (th, 0, 2*sp.pi))
    flux = sp.integrate(sp.simplify(Ps*dY - Qs*dX), (th, 0, 2*sp.pi))    # normal para fora (anti-horário)
    return sp.simplify(circ), sp.simplify(flux)
cv, fv = circ_e_fluxo(-y/r2, x/r2, 0, 0, R_)
cs, fs = circ_e_fluxo(x/r2, y/r2, 0, 0, R_)
print('H1 vórtice, circunferência de raio R em volta do furo: circulação =', cv, '(≠ 0, para todo R)', ok(cv - 2*sp.pi))
print('H2 falsa fonte, mesma circunferência: fluxo para fora =', fs, '(≠ 0, para todo R)', ok(fs - 2*sp.pi))
# laço que NÃO envolve o furo: circunferência de centro (3, 0) e raio 1 (numérico, 30 dígitos)
X_, Y_ = 3 + sp.cos(th), sp.sin(th)
def integ(e): return sp.N(sp.Integral(e, (th, 0, 2*sp.pi)), 30)
Pv_, Qv_ = (-y/r2).subs({x: X_, y: Y_}, simultaneous=True), (x/r2).subs({x: X_, y: Y_}, simultaneous=True)
Ps_, Qs_ = (x/r2).subs({x: X_, y: Y_}, simultaneous=True), (y/r2).subs({x: X_, y: Y_}, simultaneous=True)
c_fora = integ(Pv_*sp.diff(X_, th) + Qv_*sp.diff(Y_, th)); f_fora = integ(Ps_*sp.diff(Y_, th) - Qs_*sp.diff(X_, th))
print('H3 laço que não envolve o furo (centro (3, 0), raio 1): circulação do vórtice e fluxo da falsa fonte =',
      c_fora, f_fora, abs(c_fora) < 1e-25 and abs(f_fora) < 1e-25)

print('\n== L. Laplaciano (B7, curiosidade) ==')
rho_, al, sg = sp.symbols('rho alpha sigma', positive=True)
phi_p = x**2 + y**2
print('L1 plano: grad(x²+y²) = 2(x, y) e div grad = 4:', ok(div2(2*x, 2*y) - 4),
      ok(sum(sp.diff(phi_p, v, 2) for v in (x, y)) - 4))
print('L2 espaço: laplaciano de x²+y²+z² = 6 (§1.4 Ex.3): ver A5')
aa, bb = sp.symbols('a b', real=True)
media = sp.integrate(phi_p.subs({x: aa + rho_*sp.cos(th), y: bb + rho_*sp.sin(th)}, simultaneous=True), (th, 0, 2*sp.pi))/(2*sp.pi)
print('L3 média de x²+y² na circunferência de raio rho em volta de (a, b) = valor no centro + rho² = valor + (rho²/4)·laplaciano:',
      ok(media - (phi_p.subs({x: aa, y: bb}) + rho_**2/4*4)))
fg = sp.Function('g')(x, y)
med_g = sp.series(sp.integrate(sp.series(fg.subs({x: aa + rho_*sp.cos(th), y: bb + rho_*sp.sin(th)}, simultaneous=True), rho_, 0, 3).removeO(), (th, 0, 2*sp.pi))/(2*sp.pi), rho_, 0, 3).removeO()
lap_g = (fg.diff(x, 2) + fg.diff(y, 2)).subs({x: aa, y: bb}, simultaneous=True)
print('L4 qualquer função lisa: média em volta − valor no centro = (rho²/4)·laplaciano + O(rho⁴) (positivo ⇔ ponto abaixo da média):',
      ok(sp.simplify((med_g - fg.subs({x: aa, y: bb}, simultaneous=True)) - rho_**2/4*lap_g).doit()))
T = -sg**2/(sg**2 + 4*al*t)*sp.exp(-(x**2 + y**2)/(sg**2 + 4*al*t))
print('L5 mancha fria da animação (núcleo do calor 2D) resolve dT/dt = alpha·laplaciano T:',
      ok(sp.diff(T, t) - al*(sp.diff(T, x, 2) + sp.diff(T, y, 2))))

print('\n== I. Números e fórmulas de implementação (handoff v1) ==')
s2 = sp.sqrt(2)
xb = x0*sp.cos(s2*t) - y0/s2*sp.sin(s2*t); yb = s2*x0*sp.sin(s2*t) + y0*sp.cos(s2*t)
print("I1 fluxo exato do B2 (-y, 2x): x(t) = x0 cos(√2 t) − (y0/√2) sen(√2 t), y(t) = √2 x0 sen(√2 t) + y0 cos(√2 t):",
      ok(sp.diff(xb, t) + yb) and ok(sp.diff(yb, t) - 2*xb), ok(xb.subs(t, 0) - x0) and ok(yb.subs(t, 0) - y0))
H_ = sp.Rational(1, 2)
entra = sp.integrate(1/(1 + y**2), (y, -H_, H_)); sai_d = sp.integrate(2/(4 + y**2), (y, -H_, H_))
sai_cb = 2*sp.integrate(H_/(x**2 + H_**2), (x, 1, 2))
print('I2 falsa fonte, caixa [1, 2] x [-1/2, 1/2]: ENTRA (esquerda) =', sp.N(entra, 4), '; SAI direita =', sp.N(sai_d, 4),
      '; SAI cima + baixo =', sp.N(sai_cb, 4), '; soma das saídas =', sp.N(sai_d + sai_cb, 4),
      abs(sp.N(entra - sai_d - sai_cb, 40)) < 1e-30)
print('I3 rodinha da falsa fonte (setor-anel r 1,2→1,6, t = 0..2): raios finais', sp.N(sp.sqrt(sp.Rational(144, 100) + 4), 4), sp.N(sp.sqrt(sp.Rational(256, 100) + 4), 4),
      '(espessura 0,40 → ', sp.N(sp.sqrt(sp.Rational(256, 100) + 4) - sp.sqrt(sp.Rational(144, 100) + 4), 3), '), área constante (D3)')
print('I4 fonte-anel no ponto (1, 1/2): div = 2 - 1 - 1/4 =', 2 - 1 - sp.Rational(1, 4))

print('\n== J. Ganchos de física (bloco F e frases soltas) ==')
lam, eps0, mu0, I_ = sp.symbols('lambda epsilon0 mu0 I', positive=True)
E_fio = lam/(2*sp.pi*eps0)*sp.Matrix([x/r2, y/r2])
B_fio = mu0*I_/(2*sp.pi)*sp.Matrix([-y/r2, x/r2])
print('J1 fio comprido carregado: E = (lambda/2 pi eps0)(x, y)/r² = falsa fonte × constante; div E = 0 fora do fio:',
      ok(div2(E_fio[0], E_fio[1])), '; |E|² = (lambda/(2 pi eps0 r))²:', ok(E_fio.dot(E_fio) - (lam/(2*sp.pi*eps0))**2/r2))
print('J2 fio com corrente: B = (mu0 I/2 pi)(-y, x)/r² = vórtice × constante; rot B = 0 e div B = 0 fora do fio:',
      ok(rot2(B_fio[0], B_fio[1])), ok(div2(B_fio[0], B_fio[1])))
print('J3 o que "mora no furo": fluxo de E por um círculo em volta do fio = lambda/eps0 (Gauss); circulação de B = mu0 I (Ampère):',
      ok(sp.integrate(sp.simplify((E_fio[0]*sp.diff(R_*sp.sin(th), th) - E_fio[1]*sp.diff(R_*sp.cos(th), th)).subs({x: R_*sp.cos(th), y: R_*sp.sin(th)}, simultaneous=True)), (th, 0, 2*sp.pi)) - lam/eps0),
      ok(sp.integrate(sp.simplify((B_fio[0]*sp.diff(R_*sp.cos(th), th) + B_fio[1]*sp.diff(R_*sp.sin(th), th)).subs({x: R_*sp.cos(th), y: R_*sp.sin(th)}, simultaneous=True)), (th, 0, 2*sp.pi)) - mu0*I_))
Om = sp.symbols('Omega', positive=True)
v_in = Om*sp.Matrix([-y, x]); v_out = Om*sp.Matrix([-y/r2, x/r2])   # raio do miolo R = 1
print('J4 vórtice de Rankine (tornado), miolo de raio 1: contínuo em r = 1:', okm((v_in - v_out).subs({x: sp.cos(th), y: sp.sin(th)})),
      '; rot = 2 Omega dentro, 0 fora:', ok(rot2(*v_in) - 2*Om), ok(rot2(*v_out)))
print('J5 vorticidade de corpo rígido: rot(omega × r) = 2 omega (ver F1)')

# ---------------- V2 (2026-11-10): contas novas dos quadros-alvo v2 ----------------
print("\n== V2: álgebra escrita na tela e números dos quadros-alvo")
_s = x**2 + y**2
print("V2-1 dQ/dx do vórtice = ((x²+y²) − x·2x)/(x²+y²)² = (y²−x²)/(x²+y²)²:", sp.simplify(sp.diff(x/_s, x) - (_s - 2*x**2)/_s**2) == 0 and sp.simplify(sp.diff(x/_s, x) - (y**2 - x**2)/_s**2) == 0)
print("V2-2 dP/dy do vórtice = (−(x²+y²) + y·2y)/(x²+y²)² = (y²−x²)/(x²+y²)²:", sp.simplify(sp.diff(-y/_s, y) - (-_s + 2*y**2)/_s**2) == 0 and sp.simplify(sp.diff(-y/_s, y) - (y**2 - x**2)/_s**2) == 0)
print("V2-3 falsa fonte: dP/dx = (y²−x²)/(x²+y²)², dQ/dy = (x²−y²)/(x²+y²)²:", sp.simplify(sp.diff(x/_s, x) - (y**2 - x**2)/_s**2) == 0 and sp.simplify(sp.diff(y/_s, y) - (x**2 - y**2)/_s**2) == 0)
print("V2-4 rio: rot = −dP/dy = 2y/9:", sp.simplify(-sp.diff(1 - y**2/9, y) - 2*y/9) == 0)
print("V2-5 (−y, 2x): dQ/dx = 2, dP/dy = −1, rot = 3:", sp.diff(2*x, x) == 2 and sp.diff(-y, y) == -1)
print("V2-6 fonte-anel em (1, 1/2): 2 − 1 − 1/4 = 3/4:", (2 - x**2 - y**2).subs({x: 1, y: sp.Rational(1, 2)}) == sp.Rational(3, 4))
print("V2-7 rodinha 3D com eixo a 50° de W (|W| = 1): ω = cos 50° ≈ 0,643:", abs(float(sp.cos(sp.rad(50))) - 0.6428) < 1e-3)
print("V2-8 B4-2 quadrado de lado 0,7 em (x, y) por t = 0,35: área 0,49 → 0,49·e^0,7 ≈ 0,99:", abs(0.49*float(sp.exp(0.7)) - 0.987) < 1e-3)
_th = sp.symbols('th', real=True)
_m = sp.integrate((1 + sp.Rational(2, 5)*sp.cos(_th))**2 + (sp.Rational(1, 2) + sp.Rational(2, 5)*sp.sin(_th))**2, (_th, 0, 2*sp.pi))/(2*sp.pi)
print("V2-9 média de x²+y² na circunferência de raio 0,4 em (1, 1/2) = 1,25 + 0,16 = 1,41:", sp.simplify(_m - sp.Rational(141, 100)) == 0)

# ---------------- V3 (handoff v3) ----------------
print("== V3 ==")
import sympy as sp
x, y, z, t, s0 = sp.symbols('x y z t sigma2', real=True)
# campo da deformação F = (x, -y): rot = 0, div = 0; fluxo exato preserva área
P3, Q3 = x, -y
print("deformação rot = 0:", sp.simplify(sp.diff(Q3, x) - sp.diff(P3, y)) == 0)
print("deformação div = 0:", sp.simplify(sp.diff(P3, x) + sp.diff(Q3, y)) == 0)
X, Y = sp.symbols('X Y')
fx, fy = X*sp.exp(t), Y*sp.exp(-t)
print("fluxo (x e^t, y e^-t) resolve x' = x, y' = -y:", sp.simplify(sp.diff(fx, t) - fx) == 0 and sp.simplify(sp.diff(fy, t) + fy) == 0)
print("área preservada (jacobiano = 1):", sp.simplify(sp.Matrix([[sp.diff(fx, X), sp.diff(fx, Y)], [sp.diff(fy, X), sp.diff(fy, Y)]]).det()) == 1)
# cubo do B6-1: F = (x, y, z) no cubo [1,2]^3: entra 1 e sai 2 por par; saldo total 3 = div * volume
F3 = sp.Matrix([x, y, z])
print("cubo: div (x,y,z) = 3:", sum(sp.diff(F3[i], v) for i, v in enumerate((x, y, z))) == 3)
print("cubo: saldo = 3 x (2 - 1) x 1 = 3:", 3*(2 - 1)*1 == 3)
# calor (B7-4): T = 1 - (s0/s) exp(-r^2/s), s = s0 + 4 a t, resolve T_t = a lap T em 2D; lap T(0) > 0
a = sp.symbols('alpha', positive=True)
s = s0 + 4*a*t
T = 1 - (s0/s)*sp.exp(-(x**2 + y**2)/s)
lapT = sp.diff(T, x, 2) + sp.diff(T, y, 2)
print("calor: T_t = alpha lap T:", sp.simplify(sp.diff(T, t) - a*lapT) == 0)
print("calor: lap T(0,0) = 4 s0/s^2 > 0:", sp.simplify(lapT.subs({x: 0, y: 0}) - 4*s0/s**2) == 0)

# ===== V4 (handoff v4): definição por componentes e rot expandido =====
print('--- V4 ---')
x, y, z = sp.symbols('x y z', real=True)
Pf, Qf = sp.Function('P')(x, y), sp.Function('Q')(x, y)
def rot3(P, Q, R):
    return (sp.diff(R, y) - sp.diff(Q, z), sp.diff(P, z) - sp.diff(R, x), sp.diff(Q, x) - sp.diff(P, y))
r = rot3(Pf, Qf, 0)
print('V4 rot(P(x,y),Q(x,y),0) = (0,0,Qx-Py):', r[0] == 0 and r[1] == 0 and sp.simplify(r[2] - (sp.diff(Qf, x) - sp.diff(Pf, y))) == 0)
i_, j_, k_ = sp.symbols('i j k')
Pg, Qg, Rg = [sp.Function(n)(x, y, z) for n in 'PQR']
Mdet = sp.Matrix([[i_, j_, k_], [0, 0, 0], [Pg, Qg, Rg]])
# expansão simbólica do determinante pela 1ª linha, com a 2ª linha = operadores
cof = [(sp.diff(Rg, y) - sp.diff(Qg, z)), -(sp.diff(Rg, x) - sp.diff(Pg, z)), (sp.diff(Qg, x) - sp.diff(Pg, y))]
print('V4 determinante = componentes do alvo 17:', all(sp.simplify(a - b) == 0 for a, b in zip(cof, rot3(Pg, Qg, Rg))))
print('V4 exemplo B1-1a (-y,2x): P=-y, Q=2x, rot = 3 k:', sp.diff(2*x, x) - sp.diff(-y, y) == 3)
print('V4 exemplo B2-6 (-y,x): Qx=1, Py=-1, rot=2:', sp.diff(x, x) == 1 and sp.diff(-y, y) == -1)
n = 4; xs = sp.symbols('x1:%d' % (n + 1)); Fs = [xs[i]**2 for i in range(n)]
print('V4 div em R^n (F_i = x_i^2) = 2(x1+...+xn):', sp.simplify(sum(sp.diff(Fs[i], xs[i]) for i in range(n)) - 2*sum(xs)) == 0)

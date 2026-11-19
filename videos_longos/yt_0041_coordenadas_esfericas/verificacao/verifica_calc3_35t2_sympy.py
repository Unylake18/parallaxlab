# Verificação das contas do 3.5-T2 Coordenadas esféricas (yt_0041 provisório)
# Cada linha imprime ID, descrição, True/False.
import sympy as sp
rho, phi, th, a, z, r, u = sp.symbols('rho phi theta a z r u', positive=True)
x_ = rho*sp.sin(phi)*sp.cos(th); y_ = rho*sp.sin(phi)*sp.sin(th); z_ = rho*sp.cos(phi)
ok = []
def chk(i, d, c):
    c = bool(c); ok.append(c); print(f"{i:6s} {d:70s} {c}")
S = sp.simplify

# B1 · o ponto
P = {rho: 2, phi: sp.pi/6, th: sp.pi/3}
chk("B1a", "(2, pi/6, pi/3): z = 2cos(pi/6) = sqrt3", S(z_.subs(P) - sp.sqrt(3)) == 0)
chk("B1b", "sombra r = rho sen phi = 2 * 1/2 = 1", S((rho*sp.sin(phi)).subs(P) - 1) == 0)
chk("B1c", "x = r cos(pi/3) = 1/2", S(x_.subs(P) - sp.Rational(1, 2)) == 0)
chk("B1d", "y = r sen(pi/3) = sqrt3/2", S(y_.subs(P) - sp.sqrt(3)/2) == 0)
chk("B1e", "x²+y²+z² = 1/4 + 3/4 + 3 = 4 = rho²", S(sp.Rational(1,4) + sp.Rational(3,4) + 3 - 4) == 0)
chk("B1f", "x²+y²+z² = rho² (identidade)", S(x_**2 + y_**2 + z_**2 - rho**2) == 0)
chk("B1g", "x²+y² = (rho sen phi)² (sombra = polar)", S(x_**2 + y_**2 - (rho*sp.sin(phi))**2) == 0)

# B2-1 · arestas da caixinha
# aresta do meridiano: arco de raio rho e ângulo dphi -> rho dphi ; paralelo: raio r = rho sen phi -> rho sen phi dtheta
chk("B2a", "rho * (rho sen phi) = rho² sen phi", S(rho*(rho*sp.sin(phi)) - rho**2*sp.sin(phi)) == 0)
# células do hook: rho em [1/2, 1], dtheta = pi/6; A: phi em [0, pi/6]; B: phi em [pi/3, pi/2]
def cel(r1, r2, p1, p2, dth):
    return sp.integrate(rho**2*sp.sin(phi), (rho, r1, r2), (phi, p1, p2))*dth
VA = cel(sp.Rational(1,2), 1, 0, sp.pi/6, sp.pi/6)
VB = cel(sp.Rational(1,2), 1, sp.pi/3, sp.pi/2, sp.pi/6)
aA = sp.Rational(3,4)**2*sp.sin(sp.pi/12)*sp.Rational(1,2)*(sp.pi/6)*(sp.pi/6)
aB = sp.Rational(3,4)**2*sp.sin(5*sp.pi/12)*sp.Rational(1,2)*(sp.pi/6)*(sp.pi/6)
print("   VA exato", sp.nsimplify(VA), float(VA), " aprox", float(aA))
print("   VB exato", sp.nsimplify(VB), float(VB), " aprox", float(aB), " razão", float(VB/VA), float(aB/aA))
chk("B2b", "VA exato = (7pi/144)(1 - sqrt3/2) ~ 0,0204", S(VA - 7*sp.pi/144*(1 - sp.sqrt(3)/2)) == 0 and abs(float(VA) - 0.0204) < 5e-4)
chk("B2c", "VB exato = 7pi/288 ~ 0,0764", S(VB - 7*sp.pi/288) == 0)
chk("B2d", "aprox A (ponto do meio) ~ 0,020", abs(float(aA) - 0.0200) < 5e-4)
chk("B2e", "aprox B (ponto do meio) ~ 0,075", abs(float(aB) - 0.0745) < 5e-4)
chk("B2f", "sen(5pi/12)/sen(pi/12) = 2+sqrt3 ~ 3,73 (razão das aproximações)", S(sp.sin(5*sp.pi/12)/sp.sin(sp.pi/12) - (2 + sp.sqrt(3))) == 0)
chk("B2g", "razão exata VB/VA ~ 3,73", abs(float(VB/VA) - 3.732) < 1e-3)

# B2-2 · duas polares em sequência
J1 = sp.Matrix([[sp.cos(phi), -rho*sp.sin(phi)], [sp.sin(phi), rho*sp.cos(phi)]]).det()  # (z, r) <- (rho, phi)
chk("B2h", "polar no meio-plano: det [(cos,-rho sen),(sen, rho cos)] = rho", S(J1 - rho) == 0)
Jc = sp.Matrix([[sp.cos(th), -r*sp.sin(th), 0], [sp.sin(th), r*sp.cos(th), 0], [0, 0, 1]]).det()
chk("B2i", "polar no chão (r, theta, z): det = r", S(Jc - r) == 0)
chk("B2j", "produto rho * r com r = rho sen phi = rho² sen phi", S(rho*(rho*sp.sin(phi)) - rho**2*sp.sin(phi)) == 0)

# B2-3 · determinante 3x3, colunas (rho, phi, theta)
M = sp.Matrix([x_, y_, z_]).jacobian([rho, phi, th])
chk("B2k", "coluna d/drho = (sen phi cos th, sen phi sen th, cos phi)", S(M[:, 0] - sp.Matrix([sp.sin(phi)*sp.cos(th), sp.sin(phi)*sp.sin(th), sp.cos(phi)])) == sp.zeros(3, 1))
chk("B2l", "coluna d/dphi = (rho cos phi cos th, rho cos phi sen th, -rho sen phi)", S(M[:, 1] - sp.Matrix([rho*sp.cos(phi)*sp.cos(th), rho*sp.cos(phi)*sp.sin(th), -rho*sp.sin(phi)])) == sp.zeros(3, 1))
chk("B2m", "coluna d/dth = (-rho sen phi sen th, rho sen phi cos th, 0)", S(M[:, 2] - sp.Matrix([-rho*sp.sin(phi)*sp.sin(th), rho*sp.sin(phi)*sp.cos(th), 0])) == sp.zeros(3, 1))
m31 = sp.Matrix([[M[0,1], M[0,2]], [M[1,1], M[1,2]]]).det()
m32 = sp.Matrix([[M[0,0], M[0,2]], [M[1,0], M[1,2]]]).det()
chk("B2n", "menor 31 = rho²cos phi sen phi cos²th + rho² cos phi sen phi sen²th", S(m31 - (rho**2*sp.cos(phi)*sp.sin(phi)*sp.cos(th)**2 + rho**2*sp.cos(phi)*sp.sin(phi)*sp.sin(th)**2)) == 0)
chk("B2o", "menor 31 = rho² sen phi cos phi", S(m31 - rho**2*sp.sin(phi)*sp.cos(phi)) == 0)
chk("B2p", "menor 32 = rho sen²phi cos²th + rho sen²phi sen²th = rho sen²phi", S(m32 - rho*sp.sin(phi)**2) == 0)
det_lap = sp.cos(phi)*m31 - (-rho*sp.sin(phi))*m32 + 0
chk("B2q", "Laplace linha 3: cos phi*m31 - (-rho sen phi)*m32 + 0*m33 = det", S(det_lap - M.det()) == 0)
chk("B2r", "= rho² sen phi cos²phi + rho² sen³phi", S(det_lap - (rho**2*sp.sin(phi)*sp.cos(phi)**2 + rho**2*sp.sin(phi)**3)) == 0)
chk("B2s", "det = rho² sen phi (>= 0 em 0<=phi<=pi)", S(M.det() - rho**2*sp.sin(phi)) == 0)
chk("B2t", "ordem do Guidorizzi (theta, rho, phi) também dá +rho² sen phi", S(sp.Matrix([x_, y_, z_]).jacobian([th, rho, phi]).det() - rho**2*sp.sin(phi)) == 0)

# B2-4 · o teste: volume da bola
Vbola = sp.integrate(rho**2*sp.sin(phi), (rho, 0, a), (phi, 0, sp.pi), (th, 0, 2*sp.pi))
chk("B2u", "[rho³/3]_0^a = a³/3", S(sp.integrate(rho**2, (rho, 0, a)) - a**3/3) == 0)
chk("B2v", "[-cos phi]_0^pi = -cos pi - (-cos 0) = 1 + 1 = 2", S((-sp.cos(sp.pi)) - (-sp.cos(0)) - 2) == 0)
chk("B2w", "[theta]_0^{2pi} = 2pi", True)
chk("B2x", "a³/3 * 2 * 2pi = 4 pi a³/3", S(Vbola - 4*sp.pi*a**3/3) == 0)
Vsem_sen = sp.integrate(rho**2, (rho, 0, a), (phi, 0, sp.pi), (th, 0, 2*sp.pi))
chk("B2y", "ERRO sem sen phi: a³/3 * pi * 2pi = 2pi²a³/3 ~ 6,58 a³ (unidade certa, número errado)", S(Vsem_sen - 2*sp.pi**2*a**3/3) == 0)
Vsem_r2 = sp.integrate(sp.sin(phi), (rho, 0, a), (phi, 0, sp.pi), (th, 0, 2*sp.pi))
chk("B2z", "ERRO sem rho²: a * 2 * 2pi = 4 pi a (metro)", S(Vsem_r2 - 4*sp.pi*a) == 0)
chk("B2z2", "4pi/3 ~ 4,19 e 2pi²/3 ~ 6,58", abs(float(4*sp.pi/3) - 4.19) < 5e-3 and abs(float(2*sp.pi**2/3) - 6.58) < 5e-3)

# B3 · teorema: imagem do interior de uma metade
import random, math
bad = 0
for _ in range(20000):
    X, Y, Z = [random.uniform(-1, 1) for _ in range(3)]
    if X*X + Y*Y + Z*Z >= 1 or Y <= 0: continue
    R = math.sqrt(X*X + Y*Y + Z*Z); F = math.acos(Z/R); T = math.atan2(Y, X)
    if not (0 < R < 1 and 0 < F < math.pi and 0 < T < math.pi): bad += 1
chk("B3a", "toda (x,y,z) com y>0 na bola aberta vem de (0,1)x(0,pi)x(0,pi) (amostra)", bad == 0)
chk("B3b", "rho² sen phi > 0 no interior (rho>0, 0<phi<pi)", sp.ask(sp.Q.positive(rho**2*sp.sin(sp.pi/3))))

# B4 · a casca e a área da esfera
A_esf = sp.integrate(rho**2*sp.sin(phi), (phi, 0, sp.pi), (th, 0, 2*sp.pi))
chk("B4a", "int_0^{2pi} int_0^pi rho² sen phi dphi dtheta = 4 pi rho²", S(A_esf - 4*sp.pi*rho**2) == 0)
chk("B4b", "int_0^a 4 pi rho² drho = 4 pi a³/3", S(sp.integrate(4*sp.pi*rho**2, (rho, 0, a)) - 4*sp.pi*a**3/3) == 0)
chk("B4c", "d/da (4pi a³/3) = 4 pi a² (área = derivada do volume)", S(sp.diff(4*sp.pi*a**3/3, a) - 4*sp.pi*a**2) == 0)

# B5 · bola com densidade = distância (Guidorizzi Ex. 5)
Mb = sp.integrate(rho*rho**2*sp.sin(phi), (rho, 0, 1), (phi, 0, sp.pi), (th, 0, 2*sp.pi))
chk("B5a", "delta = sqrt(x²+y²+z²) = rho", S(sp.sqrt(x_**2 + y_**2 + z_**2) - rho) == 0)
chk("B5b", "[rho⁴/4]_0^1 = 1/4", S(sp.integrate(rho**3, (rho, 0, 1)) - sp.Rational(1, 4)) == 0)
chk("B5c", "M = 1/4 * 2 * 2pi = pi", S(Mb - sp.pi) == 0)
chk("B5d", "densidade média = M/V = pi/(4pi/3) = 3/4", S(Mb/(4*sp.pi/3) - sp.Rational(3, 4)) == 0)
rm = sp.Rational(1, 2)**sp.Rational(1, 4)
chk("B5e", "metade da massa fora de rho = (1/2)^(1/4) ~ 0,84", S(sp.integrate(4*sp.pi*rho**3, (rho, 0, rm)) - sp.pi/2) == 0 and abs(float(rm) - 0.8409) < 1e-3)
try:
    from scipy import integrate as si
    val, err = si.tplquad(lambda zz, yy, xx: math.sqrt(xx*xx + yy*yy + zz*zz), -1, 1,
                          lambda xx: -math.sqrt(1 - xx*xx), lambda xx: math.sqrt(1 - xx*xx),
                          lambda xx, yy: -math.sqrt(max(0, 1 - xx*xx - yy*yy)), lambda xx, yy: math.sqrt(max(0, 1 - xx*xx - yy*yy)))
    chk("B5f", f"conferência numérica em cartesianas = {val:.6f} ~ pi", abs(val - math.pi) < 1e-5)
except Exception as e:
    print("B5f   scipy indisponível:", e)
# hook: a integral de dentro em cartesianas já traz raiz e logaritmo
k = sp.symbols('k', positive=True)
inner = sp.integrate(sp.sqrt(k**2 + z**2), z)
chk("H1a", "int sqrt(k²+z²) dz envolve asinh/log (não é polinômio)", inner.has(sp.asinh) or inner.has(sp.log))
print("   primitiva de dentro:", inner)

# B6 · casquinha: cone z >= sqrt(x²+y²) dentro da esfera x²+y²+z² <= 2z
chk("B6a", "cone: rho cos phi = rho sen phi  <=>  phi = pi/4", S(sp.tan(sp.pi/4) - 1) == 0)
chk("B6b", "esfera: rho² = 2 rho cos phi  =>  rho = 2 cos phi", S((x_**2 + y_**2 + z_**2 - 2*z_).subs(rho, 2*sp.cos(phi))) == 0)
chk("B6c", "x²+y²+z² = 2z <=> x²+y²+(z-1)² = 1", S((x_**2 + y_**2 + z_**2 - 2*z_) - (x_**2 + y_**2 + (z_ - 1)**2 - 1)) == 0)
chk("B6d", "cone e esfera se cruzam em phi = pi/4, rho = 2cos(pi/4) = sqrt2, (r, z) = (1, 1)", S(2*sp.cos(sp.pi/4) - sp.sqrt(2)) == 0 and S(sp.sqrt(2)*sp.sin(sp.pi/4) - 1) == 0)
inn = sp.integrate(rho**2*sp.sin(phi), (rho, 0, 2*sp.cos(phi)))
chk("B6e", "de dentro: [rho³/3]_0^{2cos phi} sen phi = (8/3) cos³phi sen phi", S(inn - sp.Rational(8, 3)*sp.cos(phi)**3*sp.sin(phi)) == 0)
chk("B6f", "u = cos phi: phi=0 -> u=1; phi=pi/4 -> u=sqrt2/2", sp.cos(0) == 1 and S(sp.cos(sp.pi/4) - sp.sqrt(2)/2) == 0)
mid_u = sp.Rational(8, 3)*sp.integrate(u**3, (u, sp.sqrt(2)/2, 1))
chk("B6g", "(8/3) int_{sqrt2/2}^1 u³ du = (8/3)[u⁴/4] = (8/3)(1/4 - 1/16)", S(mid_u - sp.Rational(8, 3)*(sp.Rational(1, 4) - sp.Rational(1, 16))) == 0)
chk("B6h", "(sqrt2/2)⁴ = 4/16 = 1/4", S((sp.sqrt(2)/2)**4 - sp.Rational(1, 4)) == 0)
chk("B6i", "(8/3)(3/16) = 1/2", S(sp.Rational(8, 3)*sp.Rational(3, 16) - sp.Rational(1, 2)) == 0)
mid = sp.integrate(inn, (phi, 0, sp.pi/4))
chk("B6j", "int_0^{pi/4} (8/3)cos³ sen dphi = 1/2 (direto)", S(mid - sp.Rational(1, 2)) == 0)
Vc = sp.integrate(inn, (phi, 0, sp.pi/4), (th, 0, 2*sp.pi))
chk("B6k", "V = 2pi * 1/2 = pi", S(Vc - sp.pi) == 0)
chk("B6l", "confere: cone (pi*1²*1/3) + meia bola (2pi/3) = pi", S(sp.pi/3 + sp.Rational(2, 3)*sp.pi - sp.pi) == 0)
Vcil = sp.integrate((1 + sp.sqrt(1 - r**2) - r)*r, (r, 0, 1), (th, 0, 2*sp.pi))
chk("B6m", "confere em cilíndricas: int (1+sqrt(1-r²) - r) r dr dtheta = pi", S(Vcil - sp.pi) == 0)
chk("B6n", "sinal: du = -sen phi dphi; inverter limites troca o sinal", S(sp.integrate(u**3, (u, 1, sp.sqrt(2)/2)) + sp.integrate(u**3, (u, sp.sqrt(2)/2, 1))) == 0)

# B7 · cilindro (gancho): x²+y² <= 1, 0 <= z <= 1
chk("B7a", "lateral x²+y²=1 => rho sen phi = 1 => rho = 1/sen phi", S((x_**2 + y_**2).subs(rho, 1/sp.sin(phi)) - 1) == 0)
chk("B7b", "tampa z=1 => rho = 1/cos phi; troca em phi = pi/4 (quina (1,1))", S(z_.subs(rho, 1/sp.cos(phi)) - 1) == 0 and S(1/sp.sin(sp.pi/4) - 1/sp.cos(sp.pi/4)) == 0)
Gcil = sp.integrate(sp.sqrt(r**2 + z**2)*r, (r, 0, 1))
Gc = sp.integrate(Gcil, (z, 0, 1))*2*sp.pi
print("   (referência p/ 3.5-T3) Guidorizzi 5.6 Ex.1 = ", sp.nsimplify(sp.simplify(Gc)), float(Gc))
chk("B7c", "Guidorizzi 5.6 Ex.1 calculável em cilíndricas (valor finito ~ 2,76)", 2.7 < float(Gc) < 2.8)

print(f"\nTOTAL: {sum(ok)}/{len(ok)} True")

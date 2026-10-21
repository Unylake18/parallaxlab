"""Estados físicos do 5.3 (unidades da cena: μ0 = 1). A animação lê estes valores; não desenha por tentativa.

Convenção de MUNDO usada nos desenhos (projeção W de base.py): o eixo do fio / solenoide / toroide é o eixo y do mundo
(vertical na tela); o plano transversal é xz. Nos rótulos esse eixo se chama z (cilíndricas s, φ, z).
"""
import math

import numpy as np

TAU = 2 * math.pi


def b_fio(p, I=1.0):
    """Fio infinito ao longo de +y (mundo): B = I/(2π s) φ̂, com φ̂ = ŷ × ŝ = (z, 0, −x)/s."""
    x, _, z = np.asarray(p, dtype=float)
    s2 = x * x + z * z
    return I / (TAU * s2) * np.array([z, 0.0, -x])


def b_cilindro(p, a, I=1.0):
    """Cilindro de raio a com J uniforme (I total) ao longo de +y: B ∝ s dentro, ∝ 1/s fora (μ0 = 1)."""
    x, _, z = np.asarray(p, dtype=float)
    s = math.hypot(x, z)
    if s < 1e-12:
        return np.zeros(3)
    bphi = I * s / (TAU * a * a) if s < a else I / (TAU * s)
    return bphi / s * np.array([z, 0.0, -x])


def bphi_cilindro(s, a, I=1.0):
    return I * s / (TAU * a * a) if s < a else I / (TAU * s)


def basis(n):
    """(u, v) ortonormais com u × v = n̂ (o sentido de percurso u→v segue a regra da mão direita em torno de n̂)."""
    n = np.asarray(n, dtype=float)
    n = n / np.linalg.norm(n)
    t = np.array([0.0, 1.0, 0.0]) if abs(n[1]) < 0.9 else np.array([1.0, 0.0, 0.0])
    u = np.cross(t, n)
    u /= np.linalg.norm(u)
    return u, np.cross(n, u)


def circulacao(field, c, rho, n, N=720):
    """∮ B·dℓ numérico num círculo (centro c, raio rho, normal n; sentido pela mão direita)."""
    u, v = basis(n)
    tot = 0.0
    for k in range(N):
        t = TAU * (k + 0.5) / N
        p = np.asarray(c, dtype=float) + rho * (math.cos(t) * u + math.sin(t) * v)
        dl = rho * (-math.sin(t) * u + math.cos(t) * v) * TAU / N
        tot += float(np.dot(field(p), dl))
    return tot


def enlace_fio(c, rho):
    """Círculo horizontal (plano xz, normal +y) de centro c e raio rho: enlaça o fio do eixo? → ∮B·dℓ/I (0 ou 1)."""
    return 1.0 if math.hypot(c[0], c[2]) < rho else 0.0


def rot_numerico(field, p, h=1e-4):
    p = np.asarray(p, dtype=float)
    J = np.zeros((3, 3))
    for j in range(3):
        d = np.zeros(3)
        d[j] = h
        J[:, j] = (field(p + d) - field(p - d)) / (2 * h)
    return np.array([J[2, 1] - J[1, 2], J[0, 2] - J[2, 0], J[1, 0] - J[0, 1]])


def div_numerico(field, p, h=1e-4):
    p = np.asarray(p, dtype=float)
    return sum((field(p + h * e)[j] - field(p - h * e)[j]) / (2 * h) for j, e in enumerate(np.eye(3)))


# região de corrente localizada (N06–N10), no "piso" do diagrama: elipse de centro BLOB_C e semi-eixos BLOB_A, BLOB_B
BLOB_C, BLOB_A, BLOB_B = np.array([-0.2, -0.2]), 1.65, 1.05
J0 = 0.9


def J_at(X, Y):
    """J = ∇×(ψ ẑ) com ψ = (dx/a)² + (dy/b)²: tangente às MESMAS elipses desenhadas (J·n̂ = 0 em toda elipse,
    inclusive a borda) e ∇'·J = 0 exatamente. Sentido anti-horário. Zero fora da região."""
    dx, dy = X - BLOB_C[0], Y - BLOB_C[1]
    if (dx / BLOB_A) ** 2 + (dy / BLOB_B) ** 2 > 1.0:
        return np.zeros(2)
    return J0 * np.array([-dy / BLOB_B ** 2, dx / BLOB_A ** 2])


def b_toroide(s, a, b, N=1.0, I=1.0):
    return N * I / (TAU * s) if a < s < b else 0.0


def b_espira(p, R, y0=0.0, I=1.0, n=400):
    """Biot–Savart numérico de uma espira de raio R no plano y = y0 (eixo y), corrente no sentido +φ em torno de +y."""
    p = np.asarray(p, dtype=float)
    B = np.zeros(3)
    for k in range(n):
        t = TAU * (k + 0.5) / n
        q = np.array([R * math.cos(t), y0, -R * math.sin(t)])     # sentido: x → −z (mão direita em torno de +y)
        dl = np.array([-R * math.sin(t), 0.0, -R * math.cos(t)]) * TAU / n
        r = p - q
        B += I / (2 * TAU) * np.cross(dl, r) / np.linalg.norm(r) ** 3   # μ0/4π = 1/(2·2π)
    return B

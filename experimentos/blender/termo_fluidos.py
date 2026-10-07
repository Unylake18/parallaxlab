"""Gás cinético num recipiente com êmbolo e tubo com estrangulamento (Termodinâmica 5.8-5.10 e Fluidos 5.7) — estudo 13.

Rodar: blender.exe -b -P experimentos/blender/termo_fluidos.py   (gera out/termo_fluidos_v1.png)

Moléculas e marcadores de fluido são NEUTROS (branco perto, azul-claro longe): não são cargas. Ambos têm loop sem
emenda (fase de 0 a 1; fase=1 reproduz a fase 0):
- gás: cada molécula ricocheteia com onda triangular de ciclos INTEIROS por loop em cada eixo (a velocidade é o
  número de ciclos: a temperatura multiplica os ciclos), dentro do volume que o êmbolo deixa;
- tubo: partículas igualmente espaçadas NO TEMPO, andando com v = v0 (R/r)²: ficam mais afastadas e mais rápidas no
  gargalo (equação da continuidade A v = const).
"""

import bisect
import math
import random
import sys
from pathlib import Path

import bpy

sys.path.insert(0, str(Path(__file__).resolve().parent))
import casca_oca as co  # noqa: E402
import cilindro_macico as cm  # noqa: E402
import gaussiana as ga  # noqa: E402
import revolucao as rv  # noqa: E402


def _tri(s):
    f = s % 1.0
    return 1.0 - abs(2.0 * f - 1.0)


def _marcador():
    return cm.material_carga(cor_perto="texto_neutro", cor_longe="fonte_contorno")


def _risco():
    return co._material("RiscoTF", {"cor": "fonte_contorno", "emissao": 1.0, "rugosidade": 0.4})


def _caixa(nome, escala, local):
    bpy.ops.mesh.primitive_cube_add(size=1, location=local)
    o = bpy.context.active_object
    o.name = nome
    o.scale = escala
    bpy.ops.object.transform_apply(scale=True)
    return o


def criar_caixa_gas(comprimento=4.0, largura=2.0, n_moleculas=40, temperatura=1.0, pistao=0.8, amplitude_pistao=0.0,
                    semente=7, fase=0.0, raio_molecula=0.07):
    """Recipiente (vidro, arestas azul-claro) com êmbolo (vidro mais opaco) e moléculas. `pistao` = fração do
    comprimento ocupada pelo gás; `amplitude_pistao` oscila o êmbolo (fração do comprimento) ao longo do loop.
    Devolve (recipiente, atualizar(fase))."""
    L, W = comprimento, largura
    x0 = -L / 2
    cont = _caixa("Recipiente", (L, W, W), (0, 0, 0))
    cm.material_vidro(cont, base=0.03, ganho=0.16, brilho_borda=0.7)
    mat_r = _risco()
    for a in (-1, 1):                                     # 12 arestas do recipiente
        for b in (-1, 1):
            for pts in (((x0, a * W / 2, b * W / 2), (-x0, a * W / 2, b * W / 2)),
                        ((a * L / 2, -W / 2, b * W / 2), (a * L / 2, W / 2, b * W / 2)),
                        ((a * L / 2, b * W / 2, -W / 2), (a * L / 2, b * W / 2, W / 2))):
                ga.criar_curva("ArestaRecipiente", [(list(pts), False)], mat_r, 0.012)
    esp = 0.12
    piston = _caixa("Embolo", (esp, W * 0.98, W * 0.98), (x0 + pistao * L, 0, 0))
    cm.material_vidro(piston, base=0.3, ganho=0.6, brilho_borda=2.2)

    rng = random.Random(semente)
    mol = []
    for _ in range(n_moleculas):
        ciclos = [max(1, round(rng.uniform(1.0, 4.0) * temperatura)) for _ in range(3)]
        mol.append((ciclos, [rng.random() for _ in range(3)]))
    objs = cm.criar_cargas([(0, 0, 0)] * n_moleculas, raio_molecula, material=_marcador())
    m = raio_molecula + 0.03

    def atualizar(fase):
        xp = x0 + L * (pistao + amplitude_pistao * math.cos(2 * math.pi * fase))   # posição da face do êmbolo
        piston.location = (xp + esp / 2, 0, 0)
        for o, (c, ph) in zip(objs, mol):
            ux, uy, uz = (_tri(c[k] * fase + ph[k]) for k in range(3))
            o.location = (x0 + m + (xp - x0 - 2 * m) * ux, -W / 2 + m + (W - 2 * m) * uy, -W / 2 + m + (W - 2 * m) * uz)

    atualizar(fase)
    return cont, atualizar


def _perfil_tubo(R, razao, L):
    """Raio do tubo ao longo de x: estrangula suavemente para `razao`*R no centro."""
    def sm(t):
        t = min(max(t, 0.0), 1.0)
        return t * t * (3 - 2 * t)
    return lambda x: R - (R - R * razao) * (1 - sm((abs(x) - 0.6) / 1.5))


def criar_tubo(comprimento=6.0, raio=1.0, razao=0.5, n_particulas=36, semente=7, fase=0.0, parede=0.05):
    """Tubo de vidro com estrangulamento e partículas fluindo em +X, com v ∝ 1/r² (continuidade).
    Devolve (tubo, atualizar(fase))."""
    L = comprimento
    r_x = _perfil_tubo(raio, razao, L)
    NP = 90
    xs = [-L / 2 + L * i / NP for i in range(NP + 1)]
    ext = [(x, r_x(x) + parede) for x in xs]
    inte = [(x, r_x(x)) for x in reversed(xs)]
    tubo = rv.malha_revolucao("Tubo", ext + inte, "X")
    cm.material_vidro(tubo)

    # tabela x(τ): dx/dτ = v0 (R/r)², τ em unidades arbitrárias (só a forma importa; o loop é 1 volta de T)
    N = 600
    X, T = [-L / 2], [0.0]
    for i in range(1, N + 1):
        x1 = -L / 2 + L * i / N
        xm = 0.5 * (X[-1] + x1)
        v = (raio / r_x(xm)) ** 2
        T.append(T[-1] + (x1 - X[-1]) / v)
        X.append(x1)
    TT = T[-1]

    def x_de(tau):
        i = max(1, min(N, bisect.bisect_left(T, tau)))
        f = (tau - T[i - 1]) / ((T[i] - T[i - 1]) or 1.0)
        return X[i - 1] + f * (X[i] - X[i - 1])

    rng = random.Random(semente)
    part = [(0.88 * math.sqrt(rng.random()), rng.uniform(0, 2 * math.pi)) for _ in range(n_particulas)]
    objs = cm.criar_cargas([(0, 0, 0)] * n_particulas, 0.06, material=_marcador())

    def atualizar(fase):
        for k, (o, (rho, th)) in enumerate(zip(objs, part)):
            tau = (((k / n_particulas) + fase) % 1.0) * TT
            x = x_de(tau)
            r = rho * r_x(x)
            o.location = (x, r * math.cos(th), r * math.sin(th))
            d = min(x + L / 2, L / 2 - x) / (0.18 * L)           # some suavemente nas pontas do tubo
            d = min(max(d, 0.0), 1.0)
            e = d * d * (3 - 2 * d)
            o.scale = (e, e, e)

    atualizar(fase)
    return tubo, atualizar


def cena_preview():
    co.limpar_cena()
    cont, _ = criar_caixa_gas()
    co.mundo()
    co.luzes()
    cam = co.camera_enquadrada(co.cantos([cont]), azimute=-35, elevacao=20, margem=0.1)
    cm.ajustar_profundidade(cam, cont)
    co.render(co.OUT / "termo_fluidos_v1.png")


if __name__ == "__main__":
    cena_preview()

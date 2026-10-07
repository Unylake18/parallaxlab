"""Massa-mola e pêndulo simples (MHS, Física II 5.1) — estudo 16 (sandbox).

Rodar: blender.exe -b -P experimentos/blender/oscilacoes.py   (gera out/oscilacoes_v1.png)

Corpo = vidro azul (massa-mola) ou esfera com degradê (pêndulo); mola = fio azul; marcas de equilíbrio e extremos =
construção violeta tracejada. fase de 0 a 1 = UM período (fase=1 repete a fase 0). Velocidade, aceleração, energia e
o gráfico x(t) são do Manim.
"""

import math
import sys
from pathlib import Path

import bpy

sys.path.insert(0, str(Path(__file__).resolve().parent))
import casca_oca as co  # noqa: E402
import cilindro_macico as cm  # noqa: E402
import gaussiana as ga  # noqa: E402
import vetores3d as v3  # noqa: E402

OS = co.ST["materiais"]["oscilacoes"]


def curva_viva(nome, n_pontos, mat, espessura):
    """Curva POLY de `n_pontos` cujos pontos são reescritos a cada quadro. Devolve (objeto, spline)."""
    cv = bpy.data.curves.new(nome, "CURVE")
    cv.dimensions = "3D"
    cv.bevel_depth = espessura
    cv.bevel_resolution = 3
    sp = cv.splines.new("POLY")
    sp.points.add(n_pontos - 1)
    o = bpy.data.objects.new(nome, cv)
    bpy.context.collection.objects.link(o)
    o.data.materials.append(mat)
    return o, sp


def pontos_curva(sp, pts):
    for p, c in zip(sp.points, pts):
        p.co = (c[0], c[1], c[2], 1.0)


def _caixa(nome, escala, local):
    bpy.ops.mesh.primitive_cube_add(size=1, location=local)
    o = bpy.context.active_object
    o.name = nome
    o.scale = escala
    bpy.ops.object.transform_apply(scale=True)
    return o


def _estrutura(obj):
    cm.material_vidro(obj, base=OS["estrutura_base"], ganho=OS["estrutura_ganho"], brilho_borda=OS["estrutura_brilho"])


def _marca(nome, p0, p1, mat):
    return ga.criar_curva(nome, v3.tracejado([p0, p1], False, 0.16, 0.6), mat, OS["marca_espessura"])


def criar_massa_mola(amplitude=1.0, equilibrio=0.5, parede=-3.0, lado=0.9, n_espiras=12, raio_mola=0.26, marcas=1, fase=0.0):
    """Bloco de vidro preso a uma mola helicoidal na parede, sobre um trilho. x(t) = x_eq + A cos(2π fase).
    Devolve (proxy, atualizar(fase))."""
    z0 = lado / 2
    comp_trilho = equilibrio + amplitude + lado / 2 + 0.6 - parede
    cx = parede + comp_trilho / 2
    trilho = _caixa("Trilho", (comp_trilho, 1.5, 0.1), (cx, 0, -0.05))
    _estrutura(trilho)
    muro = _caixa("Parede", (0.2, 1.5, 1.9), (parede - 0.1, 0, 0.9))
    _estrutura(muro)
    bloco = _caixa("Bloco", (lado, lado, lado), (equilibrio, 0, z0))
    cm.material_vidro(bloco)
    mat_mola = v3.material_cor("Mola", OS["mola_cor"], OS["mola_emissao"])
    NP = int(n_espiras * 26)
    _, sp = curva_viva("Mola", NP, mat_mola, OS["mola_fio"])
    if marcas:
        mat_t = co._material("TracoMHS", {"cor": "gaussiana", "emissao": 1.8, "rugosidade": 0.4})
        for x in (equilibrio - amplitude, equilibrio, equilibrio + amplitude):
            _marca("Marca", (x, 0, 0.02), (x, 0, 1.9), mat_t)
    proxy = _caixa("ProxyEnquadramento", (comp_trilho, 1.5, 2.0), (cx, 0, 0.95))
    proxy.hide_render = True

    def atualizar(fase):
        x = equilibrio + amplitude * math.cos(2 * math.pi * fase)
        bloco.location = (x, 0, z0)
        x_ini, x_fim = parede, x - lado / 2
        L = x_fim - x_ini
        pts = []
        for k in range(NP):
            t = k / (NP - 1)
            env = min(1.0, t / 0.04, (1 - t) / 0.04)                  # raio -> 0 nas pontas (fio reto entrando na mola)
            a = 2 * math.pi * n_espiras * t
            pts.append((x_ini + L * t, raio_mola * env * math.cos(a), z0 + raio_mola * env * math.sin(a)))
        pontos_curva(sp, pts)

    atualizar(fase)
    return proxy, atualizar


def criar_pendulo(comprimento=3.0, amplitude_graus=24.0, raio_corpo=0.24, arco=1, fase=0.0):
    """Pêndulo simples (pequenas oscilações): θ(t) = θ0 cos(2π fase), no plano XZ. Devolve (proxy, atualizar(fase))."""
    L, th0 = comprimento, math.radians(amplitude_graus)
    zp = L + 0.5                                                      # altura do pivô
    barra = _caixa("Suporte", (2.2, 0.5, 0.14), (0, 0, zp + 0.07))
    _estrutura(barra)
    mat_fio = v3.material_cor("FioPendulo", OS["fio_cor"], OS["fio_emissao"])
    _, sp = curva_viva("FioPendulo", 2, mat_fio, OS["fio_espessura"])
    mat_c = v3.material_degrade("Corpo", OS["corpo_cor"], OS["corpo_borda"], OS["corpo_emissao"], 0.7)
    bpy.ops.mesh.primitive_uv_sphere_add(radius=raio_corpo, segments=48, ring_count=24)
    corpo = bpy.context.active_object
    corpo.name = "Massa"
    bpy.ops.object.shade_smooth()
    corpo.data.materials.append(mat_c)
    mat_t = co._material("TracoPendulo", {"cor": "gaussiana", "emissao": 1.8, "rugosidade": 0.4})
    if arco:
        pts = [(L * math.sin(th0 * (2 * k / 60 - 1)), 0, zp - L * math.cos(th0 * (2 * k / 60 - 1))) for k in range(61)]
        ga.criar_curva("ArcoPendulo", v3.tracejado(pts, False, 0.26, 0.6), mat_t, OS["marca_espessura"])
        _marca("Vertical", (0, 0, zp), (0, 0, zp - L - 0.5), mat_t)
    proxy = _caixa("ProxyEnquadramento", (2 * L * math.sin(th0) + 1.2, 0.6, L + 1.0), (0, 0, zp - (L + 0.5) / 2 + 0.25))
    proxy.hide_render = True

    def atualizar(fase):
        th = th0 * math.cos(2 * math.pi * fase)
        p = (L * math.sin(th), 0.0, zp - L * math.cos(th))
        corpo.location = p
        pontos_curva(sp, [(0, 0, zp), p])

    atualizar(fase)
    return proxy, atualizar


def cena_preview():
    co.limpar_cena()
    proxy, _ = criar_massa_mola(fase=0.15)
    co.mundo()
    co.luzes()
    co.camera_enquadrada(co.cantos([proxy]), azimute=-30, elevacao=18, margem=0.08)
    co.render(co.OUT / "oscilacoes_v1.png")


if __name__ == "__main__":
    cena_preview()

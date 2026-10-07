"""Cálculo vetorial: campo de vetores, superfície parametrizada, Stokes e gradiente — estudo 15 (sandbox).

Rodar: blender.exe -b -P experimentos/blender/calc_vetorial.py   (gera out/calc_vetorial_v1.png)

Gramática (arsenal/estilo.json): campo vetorial = ciano (reservado ao campo); superfícies = vidro azul; curvas
coordenadas e de nível = azul-claro; construções matemáticas (remendo dS, contorno de Stokes, projeções) = violeta;
vetores tangentes = branco; normal n̂ = azul. fase de 0 a 1 = um ciclo (fase=1 repete a fase 0).
"""

import math
import sys
from pathlib import Path

import bpy
from mathutils import Vector

sys.path.insert(0, str(Path(__file__).resolve().parent))
import casca_oca as co  # noqa: E402
import cilindro_macico as cm  # noqa: E402
import gaussiana as ga  # noqa: E402
import vetores3d as v3  # noqa: E402

CV = co.ST["materiais"]["calculo_vetorial"]
VT = co.ST["materiais"]["vetor"]


def _mat_curva():
    return v3.material_cor("CurvaCV", CV["curva_cor"], CV["curva_emissao"])


def _mat_tang():
    return v3.material_cor("TangenteCV", CV["tangente_cor"], CV["tangente_emissao"])


def _mat_normal():
    return v3.material_cor("NormalCV", VT["normal_cor"], VT["normal_emissao"])


def _mat_campo():
    return v3.material_cor("CampoCV", VT["campo_cor"], VT["campo_emissao"])


def _vidro_violeta(obj, base=None):
    cm.material_vidro(obj, cor="gaussiana", base=CV["remendo_base"] if base is None else base, ganho=CV["remendo_ganho"],
                      brilho_borda=CV["remendo_brilho"])


CAMPOS = {
    "radial": lambda x, y, z: (x, y, z),
    "rotacional": lambda x, y, z: (-y, x, 0.0),
    "sela": lambda x, y, z: (x, -y, 0.0),
    "espiral": lambda x, y, z: (-y + 0.35 * x, x + 0.35 * y, 0.0),
}


def criar_campo(tipo="radial", dim=2, n=7, extensao=3.0, comprimento_max=0.85, altura=0.0):
    """Campo vetorial como setas ciano numa grade (plano z=altura se dim=2; cubo se dim=3). Devolve o proxy."""
    f = CAMPOS[tipo]
    mat = _mat_campo()
    pts = [(-extensao + 2 * extensao * i / (n - 1)) for i in range(n)]
    nz = 4 if dim == 3 else 1
    zs = [(-extensao * 0.6 + 1.2 * extensao * k / (nz - 1)) for k in range(nz)] if dim == 3 else [altura]
    mags = []
    amostras = []
    for x in pts:
        for y in pts:
            for z in zs:
                v = Vector(f(x, y, z))
                if v.length > 1e-6:
                    amostras.append(((x, y, z), v))
                    mags.append(v.length)
    mmax = max(mags)
    for (o, v) in amostras:
        comp = comprimento_max * (0.28 + 0.72 * v.length / mmax)
        v3.seta(o, v.normalized() * comp, mat, comp)
    bpy.ops.mesh.primitive_cube_add(size=1)
    proxy = bpy.context.active_object
    proxy.name = "ProxyEnquadramento"
    proxy.scale = (2 * extensao + 0.6, 2 * extensao + 0.6, 2 * extensao * 0.6 + 0.6 if dim == 3 else 0.3)
    bpy.ops.object.transform_apply(scale=True)
    proxy.location = (0, 0, altura)
    proxy.hide_render = True
    return proxy


SUPERFICIES = {
    "onda": (lambda u, v: (u, v, 0.45 * math.sin(1.1 * u) * math.cos(1.1 * v)), -2.4, 2.4, -2.4, 2.4),
    "sela": (lambda u, v: (u, v, (u * u - v * v) / 3.0), -1.9, 1.9, -1.9, 1.9),
    "esfera": (lambda u, v: (2.0 * math.sin(v) * math.cos(u), 2.0 * math.sin(v) * math.sin(u), 2.0 * math.cos(v)),
               0.0, 2 * math.pi, 0.05 * math.pi, 0.95 * math.pi),
}


def criar_superficie_param(tipo="onda", u0=0.5, v0=0.5, tamanho_remendo=1.0, vetores=1, linhas=1, movimento=0, fase=0.0,
                           n_linhas=9, comprimento_vetor=1.0):
    """Superfície parametrizada com curvas coordenadas, remendo dS (violeta) e vetores r_u, r_v (brancos) e n̂ (azul).
    (u0, v0) em fração [0, 1] do domínio. Devolve (corpo, atualizar(fase))."""
    F, ua, ub, va, vb = SUPERFICIES[tipo]
    corpo = v3.malha_param("Superficie", F, ua, ub, va, vb, 56, 56)
    if linhas:
        v3.curva("CurvasCoordenadas", v3.linhas_coordenadas(F, ua, ub, va, vb, n_linhas, n_linhas), _mat_curva(), CV["curva_espessura"])
    mat_dash = co._material("TracoRemendo", {"cor": "gaussiana", "emissao": 1.8, "rugosidade": 0.4})
    dinam = []

    def limpar():
        v3.remover(dinam)

    mat_t, mat_n = _mat_tang(), _mat_normal()

    def montar(fu, fv):
        limpar()
        u, v = ua + (ub - ua) * fu, va + (vb - va) * fv
        du, dv = tamanho_remendo * (ub - ua) / 9, tamanho_remendo * (vb - va) / 9
        P, ru, rv, n = v3.normal_superficie(F, u, v)
        cantos = [Vector(F(u + su * du, v + sv * dv)) + 0.05 * n for su, sv in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
        me = bpy.data.meshes.new("Remendo")
        me.from_pydata([tuple(c) for c in cantos], [], [(0, 1, 2, 3)])
        me.update()
        rem = bpy.data.objects.new("Remendo", me)
        bpy.context.collection.objects.link(rem)
        bpy.context.view_layer.objects.active = rem
        rem.select_set(True)
        sol = rem.modifiers.new("e", "SOLIDIFY")
        sol.thickness = 0.015
        _vidro_violeta(rem)
        dinam.append(rem)
        borda = [tuple(c) for c in cantos]
        dinam.append(v3.curva("BordaRemendo", [(v3.tracejado(borda, True, 0.16, 0.6)[i][0], False) for i in range(len(v3.tracejado(borda, True, 0.16, 0.6)))],
                              mat_dash, 0.014))
        if vetores:
            L = comprimento_vetor
            for vec, mat in ((ru, mat_t), (rv, mat_t), (n, mat_n)):
                s = v3.seta(P + 0.03 * n, vec.normalized() * L, mat, L)
                if s is not None:
                    dinam.append(s)

    def atualizar(fase):
        if movimento:
            a = 2 * math.pi * fase
            montar(u0 + 0.28 * math.cos(a), v0 + 0.28 * math.sin(a))
        else:
            montar(u0, v0)

    atualizar(fase)
    return corpo, atualizar


def criar_stokes(raio=1.8, com_campo=1, normais=1, contorno_continuo=1, movimento=0, fase=0.0):
    """Hemisfério (superfície S), contorno ∂S no plano z=0 (violeta), normais n̂ para fora (azul), setas do campo
    rotacional (ciano) e uma seta tangente (branca) percorrendo ∂S no sentido anti-horário. Devolve (corpo, atualizar)."""
    R = raio
    F = lambda u, v: (R * math.sin(v) * math.cos(u), R * math.sin(v) * math.sin(u), R * math.cos(v))
    corpo = v3.malha_param("Hemisferio", F, 0.0, 2 * math.pi, 0.0, 0.5 * math.pi, 64, 32)
    mat_dash = co._material("TracoStokes", {"cor": "gaussiana", "emissao": 1.8, "rugosidade": 0.4})
    n = 160
    pts = [(R * math.cos(2 * math.pi * k / n), R * math.sin(2 * math.pi * k / n), 0.0) for k in range(n)]
    v3.curva("Contorno", [(pts + [pts[0]], False)] if contorno_continuo else v3.tracejado(pts, True, 0.3, 0.6), mat_dash, 0.028)
    mat_n, mat_c, mat_t = _mat_normal(), _mat_campo(), _mat_tang()
    alvos_n = [(0.0, 0.0), (0.9, 0.55), (2.5, 0.55), (4.1, 0.55), (5.4, 0.55)]            # normais n̂
    alvos_c = [(0.0 + k * 1.0472, 1.05) for k in range(6)]                                    # campo, entre as normais
    if normais:
        for (u, v) in alvos_n:
            P = Vector(F(u, v))
            v3.seta(P, P.normalized() * 0.7, mat_n, 0.7)
    if com_campo:
        for (u, v) in alvos_c:
            P = Vector(F(u, v))
            c = Vector((-P.y, P.x, 0.0)).normalized() * 0.7
            v3.seta(P + 0.02 * P.normalized(), c, mat_c, 0.7)
    ponta = v3.seta((R, 0, 0), (0, 1, 0), mat_t, 0.8)

    def atualizar(fase):
        th = 2 * math.pi * fase
        ponta.location = (R * math.cos(th), R * math.sin(th), 0.0)
        ponta.rotation_quaternion = Vector((0, 0, 1)).rotation_difference(Vector((-math.sin(th), math.cos(th), 0.0)))

    atualizar(fase)
    return corpo, atualizar


def criar_gradiente(altura=2.0, abertura=1.0, extensao=3.0, n_niveis=5, raio_ponto=1.4, movimento=0, fase=0.0, th0=0.6):
    """Colina f(x, y) = h e^(−r²/2σ²) (vidro), curvas de nível (azul-claro) e um ponto P com o vetor gradiente (ciano)
    sobre a superfície e a projeção violeta no plano. Devolve (corpo, atualizar(fase))."""
    h, s = altura, abertura
    f = lambda x, y: h * math.exp(-(x * x + y * y) / (2 * s * s))
    F = lambda u, v: (u, v, f(u, v))
    E = extensao
    corpo = v3.malha_param("Colina", F, -E, E, -E, E, 72, 72)
    mat_c = _mat_curva()
    for k in range(1, n_niveis + 1):
        z = h * k / (n_niveis + 1)
        r = s * math.sqrt(-2 * math.log(z / h))
        v3.curva("Nivel", [([(r * math.cos(2 * math.pi * j / 160), r * math.sin(2 * math.pi * j / 160), z + 0.015) for j in range(161)], False)],
                 mat_c, CV["curva_espessura"])
    mat_dash = co._material("TracoGrad", {"cor": "gaussiana", "emissao": 1.8, "rugosidade": 0.4})
    mat_g = _mat_campo()
    mat_t = _mat_tang()
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.09, segments=24, ring_count=12)
    pt = bpy.context.active_object
    pt.name = "PontoP"
    bpy.ops.object.shade_smooth()
    pt.data.materials.append(mat_t)
    dinam = []

    def limpar():
        v3.remover(dinam)

    def atualizar(fase):
        limpar()
        th = th0 + (2 * math.pi * fase if movimento else 0.0)
        x, y = raio_ponto * math.cos(th), raio_ponto * math.sin(th)
        z = f(x, y)
        pt.location = (x, y, z + 0.04)
        gx, gy = -z * x / (s * s), -z * y / (s * s)
        comp = min(0.35 + 0.9 * math.hypot(gx, gy), 1.6)
        dinam.append(v3.seta((x, y, z + 0.06), (gx, gy, 0.0), mat_g, comp))
        dinam.append(v3.curva("Projecao", v3.tracejado([(x, y, z), (x, y, 0.0)], False, 0.16, 0.6), mat_dash, 0.014))
        dinam.append(v3.curva("Ponto0", [([(x, y, 0.0), (x + 1e-3, y, 0.0)], False)], mat_dash, 0.05))

    atualizar(fase)
    return corpo, atualizar


def cena_preview():
    co.limpar_cena()
    proxy = criar_campo("rotacional", 2, 7)
    co.mundo()
    co.luzes()
    co.camera_enquadrada(co.cantos([proxy]), azimute=-30, elevacao=40, margem=0.07)
    co.render(co.OUT / "calc_vetorial_v1.png")


if __name__ == "__main__":
    cena_preview()

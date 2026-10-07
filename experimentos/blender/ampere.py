"""Solenoide, toroide e fio infinito (fontes de Ampère) — estudo 8 (sandbox, não integrado a vídeo).

Rodar (sem abrir a interface), a partir da raiz do repositório:
    blender.exe -b -P experimentos/blender/ampere.py

Gera out/ampere_v1.png (solenoide, toroide e fio lado a lado). Fios e enrolamentos são FONTE FÍSICA (azul);
o campo B (ciano) e o sentido da corrente ficam para o 2D/Manim. Padrão visual: arsenal/estilo.json.

Convenção de eixos: o eixo do solenoide, do toroide e do fio é X (como os cilindros do arsenal).
"""

import bisect
import math
import sys
from pathlib import Path

import bpy

sys.path.insert(0, str(Path(__file__).resolve().parent))
import casca_oca as co  # noqa: E402
import cilindro_macico as cm  # noqa: E402
import distribuicoes as ds  # noqa: E402
import gaussiana as ga  # noqa: E402
import placa as pl  # noqa: E402

B = co.ST["materiais"]["bobina"]
F = co.ST["materiais"]["fio"]


def _fio_curva(nome, pts, ciclico, raio_fio):
    mat = co._material("Bobina", B)
    return ga.criar_curva(nome, [(pts, ciclico)], mat, espessura=raio_fio)


def caminho_solenoide(raio, comprimento, n_espiras, terminal):
    """Polilinha do fio do solenoide: terminal reto, hélice de passo constante, terminal reto (eixo X)."""
    n = int(n_espiras * B["pts_por_espira"])
    pts = []
    for k in range(n + 1):
        t = k / n
        a = 2 * math.pi * n_espiras * t
        pts.append((-comprimento / 2 + comprimento * t, raio * math.cos(a), raio * math.sin(a)))
    saida = comprimento / 2 + terminal
    return [(-saida, pts[0][1], pts[0][2])] + pts + [(saida, pts[-1][1], pts[-1][2])]


def criar_solenoide(raio=1.0, comprimento=4.0, n_espiras=16, raio_fio=B["raio_fio"], nucleo=0, eixo=0,
                    comprimento_eixo=6.0, terminal=0.9, offset=(0, 0, 0)):
    """Solenoide: hélice de fio azul ao longo de X (passo constante). `nucleo=1` põe um cilindro de vidro dentro."""
    pts = caminho_solenoide(raio, comprimento, n_espiras, terminal)
    obj = _fio_curva("Solenoide", pts, False, raio_fio)
    objs = [obj]
    if nucleo:
        corpo = cm.criar_corpo_macico(raio * 0.92, comprimento)
        corpo.name = "NucleoSolenoide"
        cm.material_vidro(corpo)
        objs.append(corpo)
    if eixo:
        objs.append(ds.eixo_simetria(comprimento_eixo))
    for o in objs:
        o.location = tuple(o.location[i] + offset[i] for i in range(3))
    return obj, objs


def cargas_no_caminho(pts, espaco=0.6, tamanho=0.07, fase=0.0, comprimento_fade=0.7, fechado=False):
    """Cargas espaçadas ao longo da polilinha `pts` (comprimento de arco); devolve (objs, atualizar).

    `atualizar(fase)` posiciona as cargas; fase=1 reproduz o quadro da fase 0 (loop perfeito).
    - Caminho aberto (fio, hélice): a rede de cargas anda de 0 a 1 espaçamento; as que saem do caminho somem por
      escala nas pontas (smoothstep em `comprimento_fade`), então entrada e saída não aparecem como saltos.
    - Caminho fechado (`fechado=True`, anel, toroide): `pts` não repete o primeiro ponto; o número de cargas é
      inteiro (o espaçamento é ajustado para fechar a volta) e elas circulam sem sumir.
    """
    caminho = list(pts) + ([pts[0]] if fechado else [])
    acum = [0.0]
    for a, b in zip(caminho, caminho[1:]):
        acum.append(acum[-1] + math.dist(a, b))
    total = acum[-1]
    if fechado:
        n_obj = max(1, round(total / espaco))
        espaco = total / n_obj
    else:
        n_obj = int(total / espaco) + 2
    objs = cm.criar_cargas([caminho[0]] * n_obj, tamanho)

    def posicao(s):
        i = max(1, min(len(acum) - 1, bisect.bisect_left(acum, s)))
        f = (s - acum[i - 1]) / ((acum[i] - acum[i - 1]) or 1.0)
        a, b = caminho[i - 1], caminho[i]
        return tuple(a[k] + f * (b[k] - a[k]) for k in range(3))

    def escala(s):
        d = min(s, total - s) / comprimento_fade
        d = min(max(d, 0.0), 1.0)
        return d * d * (3 - 2 * d)

    def atualizar(fase):
        for k, o in enumerate(objs):
            if fechado:
                o.location = posicao(((k + fase) * espaco) % total)
                o.scale = (1.0, 1.0, 1.0)
                continue
            s = (k - 1 + fase) * espaco             # k-1: um espaço antes da origem, p/ o loop cobrir a entrada
            if 0.0 <= s <= total:
                o.location = posicao(s)
                e = escala(s)
            else:
                e = 0.0
            o.scale = (e, e, e)

    atualizar(fase)
    return objs, atualizar


def caminho_circulo(raio, n=128):
    """Círculo no plano YZ (em torno do eixo X), sem repetir o primeiro ponto."""
    return [(0.0, raio * math.cos(2 * math.pi * k / n), raio * math.sin(2 * math.pi * k / n)) for k in range(n)]


def caminho_toroide(raio_maior, raio_menor, n_espiras):
    """Polilinha FECHADA do fio do toroide (a mesma que `criar_toroide` desenha)."""
    n = int(n_espiras * B["pts_por_espira"])
    pts = []
    for k in range(n):
        phi = 2 * math.pi * k / n
        th = n_espiras * phi
        r = raio_maior + raio_menor * math.cos(th)
        pts.append((raio_menor * math.sin(th), r * math.cos(phi), r * math.sin(phi)))
    return pts


def criar_toroide(raio_maior=1.6, raio_menor=0.5, n_espiras=40, raio_fio=B["raio_fio"], nucleo=0, eixo=0,
                  comprimento_eixo=4.5, offset=(0, 0, 0)):
    """Toroide: fio azul enrolado em torno de um toro cujo eixo é X. `nucleo=1` põe um toro de vidro dentro."""
    n = int(n_espiras * B["pts_por_espira"])
    pts = []
    for k in range(n):
        phi = 2 * math.pi * k / n               # em torno do eixo X (volta longa)
        th = n_espiras * phi                     # em torno da seção (cada espira)
        r = raio_maior + raio_menor * math.cos(th)
        pts.append((raio_menor * math.sin(th), r * math.cos(phi), r * math.sin(phi)))
    obj = _fio_curva("Toroide", pts, True, raio_fio)
    objs = [obj]
    if nucleo:
        bpy.ops.mesh.primitive_torus_add(major_radius=raio_maior, minor_radius=raio_menor * 0.92,
                                         major_segments=128, minor_segments=32)
        corpo = bpy.context.active_object
        corpo.name = "NucleoToroide"
        corpo.rotation_euler = (0, math.radians(90), 0)
        ds._aplicar_rotacao(corpo)
        bpy.ops.object.shade_smooth()
        cm.material_vidro(corpo)
        objs.append(corpo)
    if eixo:
        objs.append(ds.eixo_simetria(comprimento_eixo))
    for o in objs:
        o.location = tuple(o.location[i] + offset[i] for i in range(3))
    return obj, objs


def material_fio(obj, comprimento, alpha=None, emissao_base=None, emissao_borda=None):
    """Fio azul luminoso que se dissolve nas pontas (sugere comprimento infinito)."""
    cor = co.E.cor(F["cor"])
    mat = bpy.data.materials.new("FioInfinito")
    mat.use_nodes = True
    cm.configurar_transparencia(mat, "culling")
    nt = mat.node_tree
    bsdf = nt.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = co.hex_linear(cor)
    bsdf.inputs["Roughness"].default_value = 0.3
    bsdf.inputs["Emission Color"].default_value = co.hex_linear(cor)

    sep = nt.nodes.new("ShaderNodeSeparateXYZ")
    nt.links.new(nt.nodes.new("ShaderNodeTexCoord").outputs["Object"], sep.inputs[0])
    d = pl._op(nt, "DIVIDE", pl._op(nt, "ABSOLUTE", sep.outputs["X"]), comprimento / 2)
    fade = pl._faixa(nt, d, F["fade_inicio"], 1.0, 1.0, 0.0, suave=True)

    lw = nt.nodes.new("ShaderNodeLayerWeight")
    lw.inputs["Blend"].default_value = 0.35
    eb = F["emissao_borda"] if emissao_borda is None else emissao_borda
    e0 = F["emissao_base"] if emissao_base is None else emissao_base
    a = F["alpha"] if alpha is None else alpha
    brilho = pl._op(nt, "MULTIPLY_ADD", lw.outputs["Fresnel"], eb, e0)
    nt.links.new(pl._op(nt, "MULTIPLY", fade, a), bsdf.inputs["Alpha"])
    nt.links.new(pl._op(nt, "MULTIPLY", brilho, fade), bsdf.inputs["Emission Strength"])
    obj.data.materials.append(mat)


def criar_fio(comprimento=10.0, raio=F["raio"], eixo=0, comprimento_eixo=None, offset=(0, 0, 0)):
    """Fio retilíneo ao longo de X; a opacidade se dissolve nas pontas. Devolve (fio, objs, proxy de enquadramento)."""
    corpo = cm.criar_corpo_macico(raio, comprimento, lados=32)
    corpo.name = "FioInfinito"
    material_fio(corpo, comprimento)
    objs = [corpo]
    halo = cm.criar_corpo_macico(raio * F["halo_escala"], comprimento, lados=48)   # envoltório de vidro: dá volume
    halo.name = "FioHalo"
    material_fio(halo, comprimento, alpha=F["halo_alpha"], emissao_base=F["halo_emissao"], emissao_borda=F["halo_emissao"])
    objs.append(halo)
    if eixo:
        objs.append(ds.eixo_simetria(comprimento_eixo or comprimento * 0.6))
    for o in objs:
        o.location = tuple(o.location[i] + offset[i] for i in range(3))
    # Proxy invisível: região visível (sem as pontas dissolvidas) para enquadrar
    bpy.ops.mesh.primitive_cube_add(size=1)
    proxy = bpy.context.active_object
    proxy.name = "ProxyEnquadramento"
    proxy.scale = (comprimento * 0.8, raio * 2, raio * 2)
    bpy.ops.object.transform_apply(scale=True)
    proxy.location = offset
    proxy.hide_render = True
    return corpo, objs, proxy


def criar_amperiano_circular(raio=1.0, continua=0, faces=0, offset=(0, 0, 0)):
    """Contorno amperiano circular no plano YZ (em torno do eixo X): violeta, tracejado ou contínuo."""
    mat = ga.material_traco()
    c = tuple(offset)
    objs = [ga.criar_curva("AmperianoCircular", ga.circulo(c, (0, 1, 0), (0, 0, 1), raio, continua), mat)]
    if faces:
        bpy.ops.mesh.primitive_circle_add(vertices=96, radius=raio, fill_type="NGON", location=c,
                                          rotation=(0, math.radians(90), 0))
        disco = bpy.context.active_object
        disco.name = "AmperianoCircularFace"
        ga.vidro_gaussiana(disco)
        objs.append(disco)
    return objs


def criar_amperiano_retangular(comprimento=2.0, altura=1.6, continua=0, centro_y=0.0, faces=0, offset=(0, 0, 0)):
    """Contorno amperiano retangular no plano XY (contém o eixo X): lados `comprimento` (em X) e `altura` (em Y)."""
    mat = ga.material_traco()
    ox, oy, oz = offset
    hx, y0, y1 = comprimento / 2, centro_y - altura / 2, centro_y + altura / 2
    cantos = [(-hx, y0), (hx, y0), (hx, y1), (-hx, y1)]
    tracos = []
    for i in range(4):
        (xa, ya), (xb, yb) = cantos[i], cantos[(i + 1) % 4]
        tracos += ga.linha((ox + xa, oy + ya, oz), (ox + xb, oy + yb, oz), continua)
    objs = [ga.criar_curva("AmperianoRetangular", tracos, mat)]
    if faces:
        bpy.ops.mesh.primitive_plane_add(size=1, location=(ox, oy + centro_y, oz))
        pl_ = bpy.context.active_object
        pl_.name = "AmperianoRetangularFace"
        pl_.scale = (comprimento, altura, 1)
        pl_.rotation_euler = (0, 0, 0)
        bpy.ops.object.transform_apply(scale=True)
        ga.vidro_gaussiana(pl_)
        objs.append(pl_)
    return objs


def cena_trio():
    co.limpar_cena()
    az, el = -45, 20
    r = math.radians(az)
    dx, dy = -math.sin(r), math.cos(r)
    d = 4.2
    sol, _ = criar_solenoide(offset=(-d * dx, -d * dy, 0))
    tor, _ = criar_toroide(offset=(0, 0, 0))
    fio, _, proxy = criar_fio(offset=(d * dx, d * dy, 0))
    co.mundo()
    co.luzes()
    cam = co.camera_enquadrada(co.cantos([sol, tor, proxy]), azimute=az, elevacao=el, margem=0.07)
    co.render(co.OUT / "ampere_v1.png")


if __name__ == "__main__":
    cena_trio()

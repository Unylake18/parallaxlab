"""Esfera, cilindro e aro rolando sem deslizar (Mecânica) — estudo 9 (sandbox, não integrado a vídeo).

Rodar (sem abrir a interface), a partir da raiz do repositório:
    blender.exe -b -P experimentos/blender/rolamento.py

Gera out/rolamento_v1.png (os três lado a lado). A câmera acompanha o corpo: ele gira parado no centro e é o CHÃO
que corre (faixa de vidro com marcas espaçadas em 2πR/4), então uma volta completa reproduz o quadro inicial (loop
perfeito, fase de 0 a 1). Rolar sem deslizar: o chão anda R·θ enquanto o corpo gira θ.

Convenção de eixos: o corpo rola ao longo de +X, o eixo de rotação é Y, o chão está em z = -R. O corpo gira de +θ
em torno de +Y (o topo vai para +X). O eixo instantâneo de rotação (no ponto de contato) é a construção violeta
tracejada do padrão (arsenal/estilo.json); velocidades e energia ficam para o Manim.
"""

import math
import sys
from pathlib import Path

import bpy

sys.path.insert(0, str(Path(__file__).resolve().parent))
import casca_oca as co  # noqa: E402
import cilindro_macico as cm  # noqa: E402
import gaussiana as ga  # noqa: E402

RL = co.ST["materiais"]["rolamento"]
X, Y, Z = (1, 0, 0), (0, 1, 0), (0, 0, 1)


def _emissivo(nome, cor, emissao):
    return co._material(nome, {"cor": cor, "emissao": emissao, "rugosidade": 0.4})


def _bolinha(pos, raio, mat, pai):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=raio, segments=24, ring_count=12, location=pos)
    o = bpy.context.active_object
    o.name = "Marca"
    bpy.ops.object.shade_smooth()
    o.data.materials.append(mat)
    o.parent = pai
    return o


def _risco(nome, polilinhas, mat, pai, espessura=None):
    curva = ga.criar_curva(nome, polilinhas, mat, espessura if espessura is not None else RL["risco_espessura"])
    curva.parent = pai
    return curva


def _empty(nome):
    e = bpy.data.objects.new(nome, None)
    bpy.context.collection.objects.link(e)
    return e


def _chao(raio, largura):
    """Faixa de vidro em z = -raio (a superfície em que o corpo rola) e a lista das marcas transversais."""
    passo = 2 * math.pi * raio / RL["marcas_por_volta"]
    # comprimento = múltiplo exato do passo: a rede de marcas é uniforme módulo `comp` (sem marca duplicada na costura)
    comp = passo * round(RL["chao_comprimento"] / passo)
    bpy.ops.mesh.primitive_cube_add(size=1)
    faixa = bpy.context.active_object
    faixa.name = "Chao"
    faixa.scale = (comp, largura, 0.02)
    bpy.ops.object.transform_apply(scale=True)
    faixa.location = (0, 0, -raio - 0.01)
    cm.material_vidro(faixa, cor=RL["chao_cor"], base=RL["chao_vidro_base"], ganho=RL["chao_vidro_ganho"],
                      brilho_borda=RL["chao_vidro_brilho"])
    mat = _emissivo("MarcaChao", RL["chao_cor"], RL["marca_chao_emissao"])
    marcas = []
    for j in range(round(comp / passo)):
        bpy.ops.mesh.primitive_cube_add(size=1)
        m = bpy.context.active_object
        m.name = "MarcaChao"
        m.scale = (RL["marca_chao_espessura"], largura, 0.012)
        bpy.ops.object.transform_apply(scale=True)
        m.data.materials.append(mat)
        marcas.append(m)
    return faixa, marcas, passo, comp


def _eixo_instantaneo(raio, comprimento):
    """Eixo instantâneo de rotação: reta tracejada violeta ao longo de Y, no ponto de contato (construção, não objeto)."""
    mat = ga.material_traco()
    y = comprimento / 2 + 0.25
    ga.criar_curva("EixoInstantaneo", ga.linha((0, -y, -raio), (0, y, -raio), False), mat)


def criar_rolamento(tipo="esfera", raio=1.0, largura=2.0, voltas=1, eixo_instantaneo=1, marca_centro=1, fase=0.0):
    """Corpo rolando. tipo: 'esfera', 'cilindro' ou 'aro'. Devolve (proxy de enquadramento, atualizar(fase))."""
    corpo = _empty("Corpo")
    mat_marca = _emissivo("Marca", RL["marca_cor"], RL["marca_emissao"])
    mat_risco = _emissivo("Risco", RL["risco_cor"], RL["risco_emissao"])
    mr = RL["marca_raio"]
    W = largura if tipo != "esfera" else 2 * raio          # extensão do corpo ao longo de Y

    if tipo == "esfera":
        bpy.ops.mesh.primitive_uv_sphere_add(segments=96, ring_count=48, radius=raio)
        v = bpy.context.active_object
        bpy.ops.object.shade_smooth()
        cm.material_vidro(v)
        v.parent = corpo
        r = raio * 1.003
        for k in range(3):                                   # 3 meridianos (planos que contêm o eixo Y) + equador
            f = math.radians(60 * k)
            _risco("Meridiano", ga.circulo((0, 0, 0), Y, (math.cos(f), 0, math.sin(f)), r, True), mat_risco, corpo)
        _risco("Equador", ga.circulo((0, 0, 0), X, Z, r, True), mat_risco, corpo)
        _bolinha((0, 0, r), mr, mat_marca, corpo)             # marca: um ponto da superfície
    elif tipo == "cilindro":
        v = cm.criar_corpo_macico(raio, largura)
        v.rotation_euler = (0, 0, math.radians(90))          # eixo X -> Y
        bpy.context.view_layer.objects.active = v
        v.select_set(True)
        bpy.ops.object.transform_apply(rotation=True)
        cm.material_vidro(v)
        v.parent = corpo
        r = raio * 1.003
        for s in (-1, 1):                                    # bordas circulares e 4 geratrizes
            _risco("Borda", ga.circulo((0, s * largura / 2, 0), X, Z, r, True), mat_risco, corpo)
        for k in range(4):
            a = math.radians(90 * k)
            _risco("Geratriz", ga.linha((r * math.cos(a), -largura / 2, r * math.sin(a)),
                                        (r * math.cos(a), largura / 2, r * math.sin(a)), True), mat_risco, corpo)
        _bolinha((0, largura / 2, r), mr, mat_marca, corpo)
    elif tipo == "aro":
        raio_tubo = 0.07
        bpy.ops.mesh.primitive_torus_add(major_radius=raio, minor_radius=raio_tubo, major_segments=128, minor_segments=24)
        v = bpy.context.active_object
        v.rotation_euler = (math.radians(90), 0, 0)         # eixo Z -> Y
        bpy.ops.object.transform_apply(rotation=True)
        bpy.ops.object.shade_smooth()
        cm.material_vidro(v, base=0.3, ganho=0.6, brilho_borda=2.2)
        v.parent = corpo
        for k in range(3):                                   # 3 marcas a 120°: a rotação se lê sem rótulo
            a = math.radians(120 * k)
            _bolinha((raio * math.sin(a), 0, raio * math.cos(a)), mr * 1.3, mat_marca, corpo)
        W = 2 * raio_tubo + 0.3
    else:
        raise ValueError(f"tipo desconhecido: {tipo}")
    if marca_centro:
        _bolinha((0, 0, 0), mr * 0.9, mat_marca, corpo)       # centro de massa (fixo no quadro da câmera)

    faixa, marcas, passo, comp = _chao(raio, max(W, 1.0) + 0.8)
    if eixo_instantaneo:
        _eixo_instantaneo(raio, max(W, 1.0) + 0.8)

    # proxy invisível só para enquadrar: o corpo e um pedaço do chão
    bpy.ops.mesh.primitive_cube_add(size=1)
    proxy = bpy.context.active_object
    proxy.name = "ProxyEnquadramento"
    proxy.scale = (5.4 * raio, max(W, 1.0) + 0.8, 2.3 * raio)
    bpy.ops.object.transform_apply(scale=True)
    proxy.hide_render = True

    circ = 2 * math.pi * raio

    def atualizar(fase):
        corpo.rotation_euler = (0, 2 * math.pi * voltas * fase, 0)
        deslocamento = circ * voltas * fase
        for j, m in enumerate(marcas):
            x = ((j * passo - deslocamento + comp / 2) % comp) - comp / 2
            d = min(max((1 - abs(x) / (comp / 2)) / 0.3, 0.0), 1.0)    # some suavemente nas pontas do chão
            e = d * d * (3 - 2 * d)
            m.location = (x, 0, -raio - 0.01)
            m.scale = (1, 1, e)

    atualizar(fase)
    return proxy, atualizar


def cena_trio():
    co.limpar_cena()
    az = math.radians(-60)
    dx, dy = -math.sin(az), math.cos(az)
    d = 4.2
    cena = []
    for k, tipo in enumerate(("esfera", "cilindro", "aro")):
        # cada corpo tem a sua própria hierarquia; aqui só deslocamos o conjunto para a vista lado a lado
        antes = set(bpy.data.objects)
        proxy, atu = criar_rolamento(tipo, fase=0.35)
        novos = [o for o in bpy.data.objects if o not in antes and o.parent is None]
        off = (k - 1) * d
        for o in novos:
            o.location = (o.location[0] + off * dx, o.location[1] + off * dy, o.location[2])
        cena.append(proxy)
    co.mundo()
    co.luzes()
    co.camera_enquadrada(co.cantos(cena), azimute=-60, elevacao=14, margem=0.06)
    co.render(co.OUT / "rolamento_v1.png")


if __name__ == "__main__":
    cena_trio()

"""Placa infinita carregada — estudo 4 (sandbox, não integrado a vídeo).

Rodar (sem abrir a interface), a partir da raiz do repositório:
    blender.exe -b -P experimentos/blender/placa.py

Gera out/placa_v1.png. Um plano infinito não cabe no quadro: a placa é uma folha de vidro cuja
opacidade (e as cargas) se dissolvem com a distância ao centro, para sugerir que ela continua.
Mesmo padrão visual dos outros sólidos (arsenal/estilo.json).
"""

import math
import random
import sys
from pathlib import Path

import bpy

sys.path.insert(0, str(Path(__file__).resolve().parent))
import casca_oca as co  # noqa: E402
import cilindro_macico as cm  # noqa: E402


def criar_placa(largura=14.0, altura=6.5, espessura=0.05):
    """Caixa fina: espessura em X (a normal do plano é X), `largura` em Y e `altura` em Z. Coordenadas de objeto = reais."""
    bpy.ops.mesh.primitive_cube_add(size=1)
    obj = bpy.context.active_object
    obj.name = "PlacaInfinita"
    obj.scale = (espessura, largura, altura)
    bpy.ops.object.transform_apply(scale=True)
    return obj


def _op(nt, operacao, a, b=None, c=None):
    """Nó Math: operandos são sockets (ligados) ou números (valor padrão). Devolve o socket de saída."""
    n = nt.nodes.new("ShaderNodeMath")
    n.operation = operacao
    for i, v in enumerate((a, b, c)):
        if v is None:
            continue
        if isinstance(v, (int, float)):
            n.inputs[i].default_value = v
        else:
            nt.links.new(v, n.inputs[i])
    return n.outputs[0]


def _faixa(nt, valor, de_min, de_max, para_min, para_max, suave=False):
    n = nt.nodes.new("ShaderNodeMapRange")
    n.clamp = True
    if suave:
        n.interpolation_type = "SMOOTHSTEP"
    nt.links.new(valor, n.inputs["Value"])
    for nome, v in (("From Min", de_min), ("From Max", de_max), ("To Min", para_min), ("To Max", para_max)):
        n.inputs[nome].default_value = v
    return n.outputs["Result"]


def material_placa(obj, largura, altura, grade=1, **sobrescrever):
    """Vidro translúcido que se dissolve nas bordas, com grade sutil (a grade é opcional)."""
    v = {**co.ST["materiais"]["placa"], **sobrescrever}
    cor = co.E.cor(v["cor"])

    mat = bpy.data.materials.new("PlacaVidro")
    mat.use_nodes = True
    cm.configurar_transparencia(mat, v["modo"])
    nt = mat.node_tree
    bsdf = nt.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = co.hex_linear(cor)
    bsdf.inputs["Roughness"].default_value = v["rugosidade"]
    bsdf.inputs["Emission Color"].default_value = co.hex_linear(cor)

    sep = nt.nodes.new("ShaderNodeSeparateXYZ")
    nt.links.new(nt.nodes.new("ShaderNodeTexCoord").outputs["Object"], sep.inputs[0])
    y, z = sep.outputs["Y"], sep.outputs["Z"]

    # fade: 1 no centro, 0 na borda. d = distância normalizada ao centro (0..1 nas bordas, por eixo)
    d = _op(nt, "MAXIMUM", _op(nt, "DIVIDE", _op(nt, "ABSOLUTE", y), largura / 2),
            _op(nt, "DIVIDE", _op(nt, "ABSOLUTE", z), altura / 2))
    fade = _faixa(nt, d, v["fade_inicio"], 1.0, 1.0, 0.0, suave=True)

    lw = nt.nodes.new("ShaderNodeLayerWeight")
    lw.inputs["Blend"].default_value = v["blend"]
    fres = lw.outputs["Fresnel"]
    alfa = _op(nt, "MULTIPLY_ADD", fres, v["ganho"], v["base"])
    brilho = _op(nt, "MULTIPLY", fres, v["brilho_borda"])

    if grade:
        passo = v["grade_passo"]

        def linha(c):  # 1 sobre as linhas da grade, 0 fora
            frac = _op(nt, "FRACT", _op(nt, "DIVIDE", c, passo))
            dist = _op(nt, "ABSOLUTE", _op(nt, "SUBTRACT", frac, 0.5))
            return _faixa(nt, dist, 0.5 - v["grade_largura"], 0.5, 0.0, 1.0)

        g = _op(nt, "MAXIMUM", linha(y), linha(z))
        alfa = _op(nt, "ADD", alfa, _op(nt, "MULTIPLY", g, v["grade_alfa"]))
        brilho = _op(nt, "ADD", brilho, _op(nt, "MULTIPLY", g, v["grade_brilho"]))

    nt.links.new(_op(nt, "MULTIPLY", alfa, fade), bsdf.inputs["Alpha"])
    nt.links.new(_op(nt, "MULTIPLY", brilho, fade), bsdf.inputs["Emission Strength"])
    obj.data.materials.append(mat)


def pontos_no_plano(n, largura, altura, dist_min, margem=0.3, semente=7):
    """Pontos uniformes sobre o plano (x=0), com distância mínima entre eles."""
    rng = random.Random(semente)
    pts, tentativas = [], 0
    my, mz = largura / 2 - margem, altura / 2 - margem
    while len(pts) < n and tentativas < 20000:
        tentativas += 1
        p = (0.0, rng.uniform(-my, my), rng.uniform(-mz, mz))
        if all(math.dist(p, q) >= dist_min for q in pts):
            pts.append(p)
    return pts


def criar_placa_carregada(offset=(0, 0, 0), largura=14.0, altura=6.5, espessura=0.05, n_cargas=220,
                          dist_min=0.5, tamanho_carga=0.06, semente=7, grade=1, fade_inicio=None):
    """Placa de vidro com cargas pontuais sobre o plano; cargas encolhem para fora, como a placa se dissolve."""
    corpo = criar_placa(largura, altura, espessura)
    fi = co.ST["materiais"]["placa"]["fade_inicio"] if fade_inicio is None else fade_inicio
    material_placa(corpo, largura, altura, grade, fade_inicio=fi)
    cargas = cm.criar_cargas(pontos_no_plano(n_cargas, largura, altura, dist_min, semente=semente), tamanho_carga)
    for o in cargas:
        d = max(abs(o.location.y) / (largura / 2), abs(o.location.z) / (altura / 2))
        t = min(max((d - fi) / (1 - fi), 0.0), 1.0)
        s = 1.0 - t * t * (3 - 2 * t)          # smoothstep, igual ao fade do material
        o.scale = (s, s, s)
    for o in [corpo, *cargas]:
        o.location = (o.location[0] + offset[0], o.location[1] + offset[1], o.location[2] + offset[2])
    # Proxy invisível (só para enquadrar/medir profundidade): região visível, sem as bordas dissolvidas
    bpy.ops.mesh.primitive_cube_add(size=1)
    proxy = bpy.context.active_object
    proxy.name = "ProxyEnquadramento"
    proxy.scale = (espessura, largura * 0.85, altura * 0.85)
    bpy.ops.object.transform_apply(scale=True)
    proxy.location = offset
    proxy.hide_render = True
    return corpo, cargas, proxy


def cena_preview():
    co.limpar_cena()
    corpo, _, proxy = criar_placa_carregada()
    co.mundo()
    co.luzes()
    cam = co.camera_enquadrada(co.cantos([proxy]), azimute=-40, elevacao=16, margem=0.06)
    cm.ajustar_profundidade(cam, proxy)
    bpy.ops.wm.save_as_mainfile(filepath=str(co.AQUI / "placa_v1.blend"))
    co.render(co.OUT / "placa_v1.png")


if __name__ == "__main__":
    cena_preview()

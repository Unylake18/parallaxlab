"""Cilindro maciço isolante com cargas no volume — estudo 2 (sandbox, não integrado a vídeo).

Rodar (sem abrir a interface), a partir da raiz do repositório:
    blender.exe -b -P experimentos/blender/cilindro_macico.py

Gera, em out/: cilindro_macico_v3.png e comparacao_v3.png (casca à esquerda, maciço à direita).
Reaproveita mundo, luzes, câmera e render de casca_oca.py.
"""

import math
import random
import sys
from pathlib import Path

import bpy

sys.path.insert(0, str(Path(__file__).resolve().parent))
import casca_oca as co  # noqa: E402


def criar_corpo_macico(raio=1.0, comprimento=4.0, lados=96):
    """Cilindro com tampas (preenchido), eixo ao longo de X, como a casca."""
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=lados, radius=raio, depth=comprimento, end_fill_type="NGON"
    )
    obj = bpy.context.active_object
    obj.name = "CilindroMacico"
    obj.rotation_euler = (0, math.radians(90), 0)
    bpy.ops.object.transform_apply(rotation=True)
    bpy.ops.object.shade_smooth_by_angle(angle=math.radians(30))
    return obj


def configurar_transparencia(mat, modo):
    """Variantes para o artefato de ordenação das faces translúcidas do Eevee."""
    if modo == "dithered":
        mat.surface_render_method = "DITHERED"
        return
    mat.surface_render_method = "BLENDED"
    if modo in ("sem_sobreposicao", "culling_e_sem_sobreposicao"):
        mat.use_transparency_overlap = False
    if modo in ("culling", "culling_e_sem_sobreposicao"):
        mat.use_backface_culling = True


def material_vidro(obj, **sobrescrever):
    """Translúcido: centro quase transparente, borda (ângulo rasante) mais opaca e luminosa.

    modo="culling" descarta as faces de trás; sem isso o Eevee mistura as faces do próprio
    cilindro na ordem errada e surgem manchas escuras (testado: dithered não resolve).
    """
    v = {**co.ST["materiais"]["vidro"], **sobrescrever}
    cor, modo, base, ganho = co.E.cor(v["cor"]), v["modo"], v["base"], v["ganho"]
    brilho_borda, blend = v["brilho_borda"], v["blend"]
    mat = bpy.data.materials.new("VidroAzul")
    mat.use_nodes = True
    configurar_transparencia(mat, modo)
    nt = mat.node_tree
    bsdf = nt.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = co.hex_linear(cor)
    bsdf.inputs["Roughness"].default_value = v["rugosidade"]
    bsdf.inputs["Emission Color"].default_value = co.hex_linear(cor)

    lw = nt.nodes.new("ShaderNodeLayerWeight")
    lw.inputs["Blend"].default_value = blend

    alfa = nt.nodes.new("ShaderNodeMath")
    alfa.operation = "MULTIPLY_ADD"
    alfa.inputs[1].default_value = ganho   # ganho da borda
    alfa.inputs[2].default_value = base    # opacidade no centro

    brilho = nt.nodes.new("ShaderNodeMath")
    brilho.operation = "MULTIPLY"
    brilho.inputs[1].default_value = brilho_borda  # emissão máxima na borda

    nt.links.new(lw.outputs["Fresnel"], alfa.inputs[0])
    nt.links.new(alfa.outputs["Value"], bsdf.inputs["Alpha"])
    nt.links.new(lw.outputs["Fresnel"], brilho.inputs[0])
    nt.links.new(brilho.outputs["Value"], bsdf.inputs["Emission Strength"])
    obj.data.materials.append(mat)


def material_carga(cor_perto=None, cor_longe=None):
    """Carga com pista de profundidade: perto = azul-claro e brilhante, longe = azul e mais fraco.

    Cargas são FONTE FÍSICA (azul), nunca ciano: ciano é reservado ao campo elétrico (ver estilo.json).
    O fator vem da profundidade em relação à câmera (Camera Data > View Z Depth); os limites
    (zona de perto/longe) são ajustados depois do enquadramento por `ajustar_profundidade`.
    """
    c = co.ST["materiais"]["carga"]
    # cor_perto/cor_longe: nomes de cores do estilo.json (padrão: o das cargas); usados por marcadores neutros
    perto, longe = co.E.cor(cor_perto or c["cor_perto"]), co.E.cor(cor_longe or c["cor_longe"])
    mat = bpy.data.materials.new("Carga")
    mat.use_nodes = True
    nt = mat.node_tree
    bsdf = nt.nodes["Principled BSDF"]

    cam = nt.nodes.new("ShaderNodeCameraData")
    mapa = nt.nodes.new("ShaderNodeMapRange")
    mapa.name = "ProfundidadeMapa"
    mapa.clamp = True
    mapa.inputs["To Min"].default_value = 1.0   # perto -> fator 1
    mapa.inputs["To Max"].default_value = 0.0   # longe -> fator 0

    mistura = nt.nodes.new("ShaderNodeMix")
    mistura.data_type = "RGBA"
    mistura.inputs[6].default_value = co.hex_linear(longe)   # A (fator 0)
    mistura.inputs[7].default_value = co.hex_linear(perto)   # B (fator 1)

    forca = nt.nodes.new("ShaderNodeMath")
    forca.operation = "MULTIPLY_ADD"
    forca.inputs[1].default_value = c["brilho_ganho"]
    forca.inputs[2].default_value = c["brilho_min"]

    nt.links.new(cam.outputs["View Z Depth"], mapa.inputs["Value"])
    nt.links.new(mapa.outputs["Result"], mistura.inputs[0])
    nt.links.new(mapa.outputs["Result"], forca.inputs[0])
    nt.links.new(mistura.outputs[2], bsdf.inputs["Base Color"])
    nt.links.new(mistura.outputs[2], bsdf.inputs["Emission Color"])
    nt.links.new(forca.outputs["Value"], bsdf.inputs["Emission Strength"])
    return mat


def ajustar_profundidade(cam, corpo):
    """Zona de perto/longe = profundidades extremas do corpo, vistas da câmera.

    Ajusta todos os materiais de carga da cena (Carga, Carga.001...): uma cena com vários grupos de cargas
    cria um material por chamada de `criar_cargas`.
    """
    inv = cam.matrix_world.inverted()
    z = [-(inv @ p).z for p in co.cantos([corpo])]
    mats = [m for m in bpy.data.materials if m.name == "Carga" or m.name.startswith("Carga.")]
    if not mats:
        raise KeyError("Carga")
    for mat in mats:
        mapa = mat.node_tree.nodes["ProfundidadeMapa"]
        mapa.inputs["From Min"].default_value = min(z)
        mapa.inputs["From Max"].default_value = max(z)


def pontos_no_volume(n, raio, comprimento, dist_min, margem=0.12, semente=7):
    """Pontos uniformes no volume, com distância mínima (evita aglomerados). Eixo ao longo de X."""
    rng = random.Random(semente)
    pts, tentativas = [], 0
    rmax = raio - margem
    while len(pts) < n and tentativas < 20000:
        tentativas += 1
        r = rmax * math.sqrt(rng.random())
        a = rng.uniform(0, 2 * math.pi)
        p = (rng.uniform(-comprimento / 2 + margem, comprimento / 2 - margem),
             r * math.cos(a), r * math.sin(a))
        if all(math.dist(p, q) >= dist_min for q in pts):
            pts.append(p)
    return pts


def criar_cargas(pontos, tamanho=co.ST["materiais"]["carga"]["tamanho"], material=None):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=tamanho, segments=16, ring_count=8)
    base = bpy.context.active_object
    base.name = "Carga"
    base.data.materials.append(material if material is not None else material_carga())
    bpy.ops.object.shade_smooth()
    objs = [base]
    for i, p in enumerate(pontos[1:], start=1):
        o = bpy.data.objects.new(f"Carga.{i:03d}", base.data)  # dados compartilhados (leve)
        bpy.context.collection.objects.link(o)
        o.location = p
        objs.append(o)
    base.location = pontos[0]
    return objs


def criar_macico(offset=(0, 0, 0), n_cargas=110, raio=1.0, comprimento=4.0,
                 dist_min=0.26, tamanho_carga=co.ST["materiais"]["carga"]["tamanho"], semente=7, **vidro):
    corpo = criar_corpo_macico(raio, comprimento)
    material_vidro(corpo, **vidro)
    pts = pontos_no_volume(n_cargas, raio, comprimento, dist_min, semente=semente)
    cargas = criar_cargas(pts, tamanho_carga)
    for o in [corpo, *cargas]:
        o.location = (o.location[0] + offset[0], o.location[1] + offset[1], o.location[2] + offset[2])
    return corpo, cargas


def cena_macico():
    co.limpar_cena()
    corpo, _ = criar_macico()
    co.mundo()
    co.luzes()
    cam = co.camera_enquadrada(co.cantos([corpo]))
    ajustar_profundidade(cam, corpo)
    bpy.ops.wm.save_as_mainfile(filepath=str(co.AQUI / "cilindro_macico_v4.blend"))
    co.render(co.OUT / "cilindro_macico_v4.png")


def cena_comparacao():
    co.limpar_cena()
    casca = co.criar_casca_oca()
    co.material_casca(casca)
    casca.location = (0, -2.3, 0)
    corpo, _ = criar_macico(offset=(0, 2.3, 0))
    co.mundo()
    co.luzes()
    cam = co.camera_enquadrada(co.cantos([casca, corpo]), margem=0.07)
    ajustar_profundidade(cam, corpo)
    co.render(co.OUT / "comparacao_v4.png")


if __name__ == "__main__":
    cena_macico()
    cena_comparacao()

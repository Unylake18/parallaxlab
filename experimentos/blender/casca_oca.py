"""Casca cilíndrica oca — estudo 1, v2 (sandbox, não integrado a nenhum vídeo).

Rodar (sem abrir a interface):
    blender.exe -b -P experimentos/blender/casca_oca.py

Gera casca_oca_v2.blend e out/casca_oca_v2.png (960x540, Eevee).
"""

import math
import sys
from pathlib import Path

import bpy
from bpy_extras.object_utils import world_to_camera_view
from mathutils import Vector

AQUI = Path(__file__).resolve().parent
OUT = AQUI / "out"
OUT.mkdir(exist_ok=True)

# Padrão visual único: arsenal/estilo.json (cores, materiais, luzes, câmera, render)
sys.path.insert(0, str(AQUI / "arsenal"))
import estilo as E  # noqa: E402

ST = E.ESTILO
hex_linear = E.hex_linear


def limpar_cena():
    bpy.ops.wm.read_factory_settings(use_empty=True)


def criar_casca_oca(raio=1.0, comprimento=4.0, espessura=0.10, lados=96):
    """Tubo aberto nas pontas. Raio externo = `raio` (Solidify com offset -1 cresce para dentro)."""
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=lados, radius=raio, depth=comprimento, end_fill_type="NOTHING"
    )
    obj = bpy.context.active_object
    obj.name = "CascaOca"
    obj.rotation_euler = (0, math.radians(90), 0)  # eixo ao longo de X
    bpy.ops.object.transform_apply(rotation=True)

    sol = obj.modifiers.new("Espessura", "SOLIDIFY")
    sol.thickness = espessura
    sol.offset = -1
    sol.use_rim = True
    sol.material_offset = 1       # face interna -> slot 1 (escuro)
    sol.material_offset_rim = 2   # aro das pontas -> slot 2 (destaque)

    bpy.ops.object.shade_smooth_by_angle(angle=math.radians(30))
    return obj


def _material(nome, cfg):
    mat = bpy.data.materials.new(nome)
    mat.use_nodes = True
    cor = E.cor(cfg["cor"])
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = hex_linear(cor)
    bsdf.inputs["Metallic"].default_value = cfg.get("metalico", 0.0)
    bsdf.inputs["Roughness"].default_value = cfg["rugosidade"]
    bsdf.inputs["Emission Color"].default_value = hex_linear(cor)
    bsdf.inputs["Emission Strength"].default_value = cfg["emissao"]
    return mat


def material_casca(obj):
    """Slots: 0 exterior azul, 1 interior escuro (profundidade), 2 aro claro (espessura)."""
    for slot, chave in enumerate(("casca_exterior", "casca_interior", "casca_aro")):
        obj.data.materials.append(_material(chave, ST["materiais"][chave]))


def mundo():
    w = bpy.data.worlds.new("Fundo")
    bpy.context.scene.world = w
    w.use_nodes = True
    bg = w.node_tree.nodes["Background"]
    bg.inputs["Color"].default_value = hex_linear(E.cor("fundo"))
    bg.inputs["Strength"].default_value = 1.0


def luzes():
    def area(nome, loc, cor, energia, tamanho):
        d = bpy.data.lights.new(nome, "AREA")
        d.energy = energia
        d.color = hex_linear(cor)[:3]
        d.size = tamanho
        o = bpy.data.objects.new(nome, d)
        bpy.context.collection.objects.link(o)
        o.location = loc
        direcao = Vector((0, 0, 0)) - Vector(loc)
        o.rotation_euler = direcao.to_track_quat("-Z", "Y").to_euler()

    for nome, cfg in ST["iluminacao"].items():
        area(nome.capitalize(), cfg["loc"], E.cor(cfg["cor"]), cfg["energia"], cfg["tamanho"])


def camera(loc=(7.5, -3.2, 2.4), alvo=(0.3, 0, 0), lente=50):
    cam_d = bpy.data.cameras.new("Camera")
    cam_d.lens = lente
    cam = bpy.data.objects.new("Camera", cam_d)
    bpy.context.collection.objects.link(cam)
    cam.location = loc
    alvo = Vector(alvo)
    cam.rotation_euler = (alvo - Vector(cam.location)).to_track_quat("-Z", "Y").to_euler()
    bpy.context.scene.camera = cam


def cantos(objs):
    """Cantos (mundo) das caixas delimitadoras dos objetos: base para enquadrar."""
    bpy.context.view_layer.update()  # matrix_world fica velha após mudar location/rotation
    return [o.matrix_world @ Vector(c) for o in objs for c in o.bound_box]


def camera_enquadrada(pontos, azimute=ST["camera"]["azimute"], elevacao=ST["camera"]["elevacao"],
                      lente=ST["camera"]["lente"], margem=ST["camera"]["margem"],
                      largura=ST["render"]["preview"]["largura"], altura=ST["render"]["preview"]["altura"]):
    """Câmera que enquadra `pontos` com margem fixa (fração do quadro) em volta do conjunto.

    Direção dada por azimute/elevação (graus, a partir de +X). Ajusta distância e centragem
    projetando os pontos pela própria câmera, em vez de calcular na mão.
    """
    sc = bpy.context.scene
    sc.render.resolution_x, sc.render.resolution_y = largura, altura
    cam_d = bpy.data.cameras.new("Camera")
    cam_d.lens = lente
    cam = bpy.data.objects.new("Camera", cam_d)
    bpy.context.collection.objects.link(cam)
    sc.camera = cam

    az, el = math.radians(azimute), math.radians(elevacao)
    direcao = Vector((math.cos(el) * math.cos(az), math.cos(el) * math.sin(az), math.sin(el)))
    alvo = sum(pontos, Vector()) / len(pontos)
    dist = 10.0
    largura_vis = lambda d: d * cam_d.sensor_width / lente  # largura visível à distância d
    for _ in range(14):
        cam.location = alvo + direcao * dist
        quat = (alvo - cam.location).to_track_quat("-Z", "Y")
        cam.rotation_euler = quat.to_euler()
        bpy.context.view_layer.update()
        ndc = [world_to_camera_view(sc, cam, p) for p in pontos]
        xs, ys = [n.x for n in ndc], [n.y for n in ndc]
        cx, cy = (min(xs) + max(xs)) / 2 - 0.5, (min(ys) + max(ys)) / 2 - 0.5
        ocupa = max(max(xs) - min(xs), max(ys) - min(ys))
        dist *= ocupa / (1 - 2 * margem)
        wv = largura_vis(dist)
        alvo += quat @ Vector((1, 0, 0)) * cx * wv + quat @ Vector((0, 1, 0)) * cy * wv * altura / largura
    return cam


def render(caminho_png, largura=ST["render"]["preview"]["largura"], altura=ST["render"]["preview"]["altura"],
           amostras=ST["render"]["amostras"]):
    sc = bpy.context.scene
    # O nome do motor Eevee mudou entre versões do Blender; testar os candidatos.
    for nome in ("BLENDER_EEVEE", "BLENDER_EEVEE_NEXT"):
        try:
            sc.render.engine = nome
            break
        except TypeError:
            continue
    sc.render.resolution_x = largura
    sc.render.resolution_y = altura
    sc.render.resolution_percentage = 100
    sc.render.fps = ST["render"]["preview"]["fps"]
    sc.render.image_settings.file_format = "PNG"
    sc.view_settings.view_transform = ST["render"]["view_transform"]  # cores fiéis à paleta
    sc.eevee.taa_render_samples = amostras
    sc.render.filepath = str(caminho_png)
    bpy.ops.render.render(write_still=True)


def main():
    limpar_cena()
    obj = criar_casca_oca()
    material_casca(obj)
    mundo()
    luzes()
    camera()
    bpy.ops.wm.save_as_mainfile(filepath=str(AQUI / "casca_oca_v2.blend"))
    render(OUT / "casca_oca_v2.png")
    print("ENGINE:", bpy.context.scene.render.engine)


if __name__ == "__main__":
    main()

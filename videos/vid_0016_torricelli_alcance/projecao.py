"""Projeção dos pontos-chave do `tanque_torricelli` na câmera do arsenal, para alinhar os overlays Manim ao 3D.

Rodar a partir da raiz do repositório (usa o Blender só para ler a câmera; não renderiza nada e não altera o arsenal):
    blender.exe -b -P videos/vid_0016_torricelli_alcance/projecao.py

Grava `projecao.json`: para cada u = y/H (estados 0,2/0,35/0,8 e uma tabela fina de 0,05 a 0,95 para furo e pouso), as coordenadas normalizadas (0–1, origem embaixo à esquerda) de cada ponto na imagem
540×960 que `Solido3D` usa (mesmo enquadramento da ficha, `enquadramento_fixo=1`). A cena converte para unidades do Manim.
"""

import json
import sys
from pathlib import Path

import bpy
from bpy_extras.object_utils import world_to_camera_view
from mathutils import Vector

UNIDADE = Path(__file__).resolve().parent
ARSENAL = UNIDADE.parents[1] / "experimentos" / "blender" / "arsenal"
sys.path.insert(0, str(ARSENAL))
sys.path.insert(0, str(ARSENAL.parent))
import casca_oca as co  # noqa: E402
from construtores import CONSTRUTORES  # noqa: E402
import renderizar as R  # noqa: E402

ficha = json.loads((ARSENAL / "solidos" / "tanque_torricelli.json").read_text(encoding="utf-8"))
LARGURA, ALTURA = 540, 960
US = (0.2, 0.35, 0.8)
saida = {"res": [LARGURA, ALTURA], "u": {}}

for u in US:
    p = R.parametros(ficha, [])
    H, W = p["nivel"], p["largura"]
    p.update(altura_furo=u * H, enquadramento_fixo=1, setas=0, movimento=1)
    co.limpar_cena()
    res = CONSTRUTORES["tanque_torricelli"](p)
    co.mundo()
    co.luzes()
    e = ficha["enquadramento"]
    cam = co.camera_enquadrada(co.cantos(res["enquadrar"]), azimute=e["azimute"], elevacao=e["elevacao"], lente=e["lente"],
                               margem=e["margem"], largura=LARGURA, altura=ALTURA)
    cena = bpy.context.scene
    y, D, xf = u * H, 1.4, W / 2
    alcance = 2 * (y * (H - y)) ** 0.5

    def proj(x, yy, z):
        v = world_to_camera_view(cena, cam, Vector((x, yy, z)))
        return [round(v.x, 5), round(v.y, 5)]

    cx = xf + 0.25                                   # linha tracejada "Altura" desenhada pelo sólido (de H até y)
    saida["u"][str(u)] = {
        "y": y, "H": H, "W": W, "alcance": alcance,
        "furo": proj(xf, 0, y),
        "pouso": proj(xf + alcance, 0, 0),
        "chao_parede": proj(xf, 0, 0),
        "superficie_parede": proj(xf, 0, H),
        "esq_chao": proj(-W / 2, -D / 2, 0),
        "esq_superficie": proj(-W / 2, -D / 2, H),
        "esq_furo": proj(-W / 2, -D / 2, y),
        "cota_chao": proj(cx, 0, 0),
        "cota_furo": proj(cx, 0, y),
        "cota_superficie": proj(cx, 0, H),
        "chao_fim": proj(xf + 2.6, 0, 0),
    }

# Tabela fina u -> furo e pouso (para overlays que acompanham u continuamente: interpolação linear na cena)
tab = {"u": [], "furo": [], "pouso": []}
for k in range(5, 96):
    u = k / 100
    p = R.parametros(ficha, [])
    H, W = p["nivel"], p["largura"]
    p.update(altura_furo=u * H, enquadramento_fixo=1, setas=0, movimento=1, estilo_jato=1)
    co.limpar_cena()
    res = CONSTRUTORES["tanque_torricelli"](p)
    co.mundo()
    co.luzes()
    e = ficha["enquadramento"]
    cam = co.camera_enquadrada(co.cantos(res["enquadrar"]), azimute=e["azimute"], elevacao=e["elevacao"], lente=e["lente"],
                               margem=e["margem"], largura=LARGURA, altura=ALTURA)
    cena = bpy.context.scene
    y, xf = u * H, W / 2
    alc = 2 * (y * (H - y)) ** 0.5
    for chave, pt in (("furo", (xf, 0, y)), ("pouso", (xf + alc, 0, 0))):
        v = world_to_camera_view(cena, cam, Vector(pt))
        tab[chave].append([round(v.x, 5), round(v.y, 5)])
    tab["u"].append(u)
saida["tabela"] = tab
(UNIDADE / "projecao.json").write_text(json.dumps(saida, indent=1), encoding="utf-8")
print("PROJECAO ok:", UNIDADE / "projecao.json")

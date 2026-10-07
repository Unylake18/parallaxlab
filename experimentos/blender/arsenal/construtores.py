"""Registro de construtores do arsenal: id do JSON -> função que cria o sólido no Blender.

Cada construtor recebe o dict de parâmetros ({nome: valor}) e devolve
    {"enquadrar": [objetos que definem o enquadramento], "apos_camera": callable(cam) | None}
Só roda dentro do Blender (importa bpy). Reaproveita os estudos em experimentos/blender/.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import casca_oca as co  # noqa: E402
import cilindro_macico as cm  # noqa: E402
import esferas as es  # noqa: E402
import gaussiana as ga  # noqa: E402
import coaxial as cx  # noqa: E402
import distribuicoes as ds  # noqa: E402
import placa as pl  # noqa: E402


def casca_cilindrica_oca(p):
    obj = co.criar_casca_oca(p["raio"], p["comprimento"], p["espessura"], p["lados"])
    co.material_casca(obj)
    return {"enquadrar": [obj], "apos_camera": None}


def cilindro_macico_isolante(p):
    corpo, _ = cm.criar_macico(
        n_cargas=p["n_cargas"], raio=p["raio"], comprimento=p["comprimento"],
        dist_min=p["dist_min"], tamanho_carga=p["tamanho_carga"], semente=p["semente"],
    )
    return {"enquadrar": [corpo], "apos_camera": lambda cam: cm.ajustar_profundidade(cam, corpo)}


def casca_esferica_oca(p):
    obj = es.criar_casca_esferica(p["raio"], p["espessura"], p["segmentos"], p["aneis"], int(p["corte"]))
    co.material_casca(obj)
    return {"enquadrar": [obj], "apos_camera": None}


def esfera_macica_isolante(p):
    corpo, _ = es.criar_esfera_macica(
        raio=p["raio"], n_cargas=int(p["n_cargas"]), dist_min=p["dist_min"],
        tamanho_carga=p["tamanho_carga"], semente=int(p["semente"]),
    )
    return {"enquadrar": [corpo], "apos_camera": lambda cam: cm.ajustar_profundidade(cam, corpo)}


def placa_infinita_carregada(p):
    corpo, _, proxy = pl.criar_placa_carregada(
        largura=p["largura"], altura=p["altura"], espessura=p["espessura"], n_cargas=int(p["n_cargas"]),
        dist_min=p["dist_min"], tamanho_carga=p["tamanho_carga"], semente=int(p["semente"]),
        grade=int(p["grade"]), fade_inicio=p["fade_inicio"],
    )
    # Enquadra e mede profundidade pelo proxy (região visível), sem as bordas dissolvidas
    return {"enquadrar": [proxy], "apos_camera": lambda cam: cm.ajustar_profundidade(cam, proxy)}


def cilindro_coaxial(p):
    _, externo, _ = cx.criar_coaxial(
        raio_a=p["raio_a"], raio_b=p["raio_b"], comprimento=p["comprimento"], espessura=p["espessura"],
        n_cargas=int(p["n_cargas"]), dist_min=p["dist_min"], tamanho_carga=p["tamanho_carga"],
        semente=int(p["semente"]), corte=int(p["corte"]),
    )
    return {"enquadrar": [externo], "apos_camera": lambda cam: cm.ajustar_profundidade(cam, externo)}


def _com_fonte_depth(com_fonte, alvo):
    return (lambda cam: cm.ajustar_profundidade(cam, alvo)) if com_fonte else None


def gaussiana_esferica(p):
    objs = ga.criar_gaussiana_esferica(p["raio"], int(p["continua"]), int(p["faces"]))
    alvo = objs[-1]
    if int(p["com_fonte"]):
        es.criar_esfera_macica(raio=p["raio_fonte"], n_cargas=50, dist_min=0.34)
    return {"enquadrar": [alvo], "apos_camera": _com_fonte_depth(int(p["com_fonte"]), alvo)}


def gaussiana_cilindrica(p):
    objs = ga.criar_gaussiana_cilindrica(p["raio"], p["comprimento"], int(p["lateral_continua"]),
                                         int(p["tampas_continuas"]), int(p["n_linhas"]), int(p["faces"]))
    alvo = objs[-1]
    enquadrar = [alvo]
    if int(p["com_fonte"]):
        fonte, _ = cm.criar_macico(raio=p["raio_fonte"], comprimento=p["comprimento_fonte"], n_cargas=80)
        enquadrar = [fonte, alvo]
    return {"enquadrar": enquadrar, "apos_camera": _com_fonte_depth(int(p["com_fonte"]), enquadrar[0])}


def gaussiana_caixa(p):
    objs = ga.criar_gaussiana_caixa(p["lado"], p["altura"], int(p["continua"]), int(p["faces"]))
    alvo = objs[-1]
    enquadrar = [alvo]
    if int(p["com_fonte"]):
        _, _, proxy = pl.criar_placa_carregada(largura=8.0, altura=5.0, n_cargas=90, dist_min=0.55)
        enquadrar = [proxy]
    return {"enquadrar": enquadrar, "apos_camera": _com_fonte_depth(int(p["com_fonte"]), enquadrar[0])}


def _depth_se_cargas(com_cargas, alvo):
    return (lambda cam: cm.ajustar_profundidade(cam, alvo)) if com_cargas else None


def anel_carregado(p):
    corpo, _ = ds.criar_anel(p["raio"], p["raio_tubo"], int(p["n_cargas"]), int(p["com_cargas"]), int(p["eixo"]),
                             p["comprimento_eixo"], int(p["semente"]))
    return {"enquadrar": [corpo], "apos_camera": _depth_se_cargas(int(p["com_cargas"]), corpo)}


def disco_carregado(p):
    corpo, _ = ds.criar_disco(p["raio"], p["espessura"], int(p["n_cargas"]), p["dist_min"], int(p["com_cargas"]),
                              int(p["eixo"]), p["comprimento_eixo"], int(p["semente"]))
    return {"enquadrar": [corpo], "apos_camera": _depth_se_cargas(int(p["com_cargas"]), corpo)}


def haste_carregada(p):
    corpo, _ = ds.criar_haste(p["comprimento"], p["raio"], int(p["n_cargas"]), int(p["com_cargas"]), int(p["eixo"]),
                              p["comprimento_eixo"], int(p["semente"]))
    return {"enquadrar": [corpo], "apos_camera": _depth_se_cargas(int(p["com_cargas"]), corpo)}


CONSTRUTORES = {
    "casca_cilindrica_oca": casca_cilindrica_oca,
    "cilindro_macico_isolante": cilindro_macico_isolante,
    "casca_esferica_oca": casca_esferica_oca,
    "esfera_macica_isolante": esfera_macica_isolante,
    "placa_infinita_carregada": placa_infinita_carregada,
    "cilindro_coaxial": cilindro_coaxial,
    "gaussiana_esferica": gaussiana_esferica,
    "gaussiana_cilindrica": gaussiana_cilindrica,
    "gaussiana_caixa": gaussiana_caixa,
    "anel_carregado": anel_carregado,
    "disco_carregado": disco_carregado,
    "haste_carregada": haste_carregada,
}

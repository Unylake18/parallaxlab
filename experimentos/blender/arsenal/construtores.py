"""Registro de construtores do arsenal: id do JSON -> função que cria o sólido no Blender.

Cada construtor recebe o dict de parâmetros ({nome: valor}) e devolve
    {"enquadrar": [objetos que definem o enquadramento], "apos_camera": callable(cam) | None,
     "atualizar": callable(fase) | None}
`atualizar(fase)` só existe nos sólidos animáveis com `cargas_moveis=1`: fase em [0, 1) percorre um loop que
fecha sem emenda (fase=1 reproduz a fase 0); é o que `animar.py` e a ponte com o Manim usam.
Só roda dentro do Blender (importa bpy). Reaproveita os estudos em experimentos/blender/.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import casca_oca as co  # noqa: E402
import cilindro_macico as cm  # noqa: E402
import esferas as es  # noqa: E402
import gaussiana as ga  # noqa: E402
import ampere as am  # noqa: E402
import coaxial as cx  # noqa: E402
import distribuicoes as ds  # noqa: E402
import placa as pl  # noqa: E402
import capacitores as cp  # noqa: E402
import otica as ot  # noqa: E402
import revolucao as rv  # noqa: E402
import calc_vetorial as cv  # noqa: E402
import gravitacao as gr  # noqa: E402
import termo_fluidos as tf  # noqa: E402
import rolamento as rl  # noqa: E402


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
    movel = int(p["cargas_moveis"])
    corpo, _, proxy = pl.criar_placa_carregada(
        largura=p["largura"], altura=p["altura"], espessura=p["espessura"], n_cargas=int(p["n_cargas"]),
        dist_min=p["dist_min"], tamanho_carga=p["tamanho_carga"], semente=int(p["semente"]),
        grade=int(p["grade"]), fade_inicio=p["fade_inicio"], com_cargas=0 if movel else 1,
    )
    # Enquadra e mede profundidade pelo proxy (região visível), sem as bordas dissolvidas
    res = {"enquadrar": [proxy], "apos_camera": lambda cam: cm.ajustar_profundidade(cam, proxy)}
    if movel:
        _, res["atualizar"] = pl.cargas_deslizantes(
            p["largura"], p["altura"], int(p["n_cargas"]), p["dist_min"], p["tamanho_carga"], int(p["semente"]),
            p["fade_inicio"], int(p["periodos"]), p["fase"])
    return res


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
    movel = int(p["cargas_moveis"])
    corpo, _ = ds.criar_anel(p["raio"], p["raio_tubo"], int(p["n_cargas"]), 0 if movel else int(p["com_cargas"]),
                             int(p["eixo"]), p["comprimento_eixo"], int(p["semente"]))
    res = {"enquadrar": [corpo], "apos_camera": _depth_se_cargas(movel or int(p["com_cargas"]), corpo)}
    if movel:
        _, res["atualizar"] = am.cargas_no_caminho(am.caminho_circulo(p["raio"]), p["espaco_cargas"],
                                                   p["tamanho_carga_movel"], p["fase"], fechado=True)
    return res


def disco_carregado(p):
    movel = int(p["cargas_moveis"])
    corpo, objs = ds.criar_disco(p["raio"], p["espessura"], int(p["n_cargas"]), p["dist_min"],
                                 1 if movel else int(p["com_cargas"]), int(p["eixo"]), p["comprimento_eixo"],
                                 int(p["semente"]))
    res = {"enquadrar": [corpo], "apos_camera": _depth_se_cargas(movel or int(p["com_cargas"]), corpo)}
    if movel:
        cargas = [o for o in objs if o.name.startswith("Carga")]
        res["atualizar"] = ds.cargas_girando(cargas, int(p["voltas"]), p["fase"])
    return res


def haste_carregada(p):
    movel = int(p["cargas_moveis"])
    corpo, _ = ds.criar_haste(p["comprimento"], p["raio"], int(p["n_cargas"]), 0 if movel else int(p["com_cargas"]),
                              int(p["eixo"]), p["comprimento_eixo"], int(p["semente"]))
    res = {"enquadrar": [corpo], "apos_camera": _depth_se_cargas(movel or int(p["com_cargas"]), corpo)}
    if movel:
        m = p["comprimento"] / 2 - 0.15
        _, res["atualizar"] = am.cargas_no_caminho([(0.0, -m, 0.0), (0.0, m, 0.0)], p["espaco_cargas"],
                                                   p["tamanho_carga_movel"], p["fase"], 0.4)
    return res


def solenoide_corrente(p):
    corpo, _ = am.criar_solenoide(p["raio"], p["comprimento"], int(p["n_espiras"]), p["raio_fio"], int(p["nucleo"]),
                                  int(p["eixo"]), p["comprimento_eixo"], p["terminal"])
    res = {"enquadrar": [corpo], "apos_camera": None}
    if int(p["cargas_moveis"]):
        pts = am.caminho_solenoide(p["raio"], p["comprimento"], int(p["n_espiras"]), p["terminal"])
        cargas, atualizar = am.cargas_no_caminho(pts, p["espaco_cargas"], p["tamanho_carga_movel"], p["fase"])
        res["atualizar"] = atualizar
        res["apos_camera"] = lambda cam: cm.ajustar_profundidade(cam, corpo)
    return res


def toroide_corrente(p):
    corpo, _ = am.criar_toroide(p["raio_maior"], p["raio_menor"], int(p["n_espiras"]), p["raio_fio"], int(p["nucleo"]),
                                int(p["eixo"]), p["comprimento_eixo"])
    res = {"enquadrar": [corpo], "apos_camera": None}
    if int(p["cargas_moveis"]):
        pts = am.caminho_toroide(p["raio_maior"], p["raio_menor"], int(p["n_espiras"]))
        _, res["atualizar"] = am.cargas_no_caminho(pts, p["espaco_cargas"], p["tamanho_carga_movel"], p["fase"],
                                                   fechado=True)
        res["apos_camera"] = lambda cam: cm.ajustar_profundidade(cam, corpo)
    return res


def fio_infinito(p):
    _, _, proxy = am.criar_fio(p["comprimento"], p["raio"], int(p["eixo"]), p["comprimento_eixo"])
    res = {"enquadrar": [proxy], "apos_camera": None}
    if int(p["cargas_moveis"]):
        m = p["comprimento"] / 2
        cargas, atualizar = am.cargas_no_caminho([(-m, 0.0, 0.0), (m, 0.0, 0.0)], p["espaco_cargas"],
                                                 p["tamanho_carga_movel"], p["fase"], p["comprimento"] * 0.25)
        res["atualizar"] = atualizar
        res["apos_camera"] = lambda cam: cm.ajustar_profundidade(cam, proxy)
    return res


def amperiano_circular(p):
    objs = am.criar_amperiano_circular(p["raio"], int(p["continua"]), int(p["faces"]))
    if int(p["com_fonte"]):
        am.criar_fio(p["comprimento_fonte"], p["raio_fonte"])
    return {"enquadrar": [objs[0]], "apos_camera": None}


def amperiano_retangular(p):
    objs = am.criar_amperiano_retangular(p["comprimento"], p["altura"], int(p["continua"]), p["raio_fonte"],
                                         int(p["faces"]))
    alvo = objs[0]
    if int(p["com_fonte"]):
        alvo, _ = am.criar_solenoide(p["raio_fonte"], p["comprimento_fonte"], int(p["n_espiras_fonte"]))
    return {"enquadrar": [alvo], "apos_camera": None}


def _rolando(tipo, p):
    proxy, atualizar = rl.criar_rolamento(tipo, p["raio"], p.get("largura", 2.0), int(p["voltas"]),
                                          int(p["eixo_instantaneo"]), int(p["marca_centro"]), p["fase"])
    res = {"enquadrar": [proxy], "apos_camera": None}
    if int(p["movimento"]):
        res["atualizar"] = atualizar
    else:
        atualizar(0.0)
    return res


def esfera_rolando(p):
    return _rolando("esfera", p)


def cilindro_rolando(p):
    return _rolando("cilindro", p)


def aro_rolando(p):
    return _rolando("aro", p)


def _revolucao(metodo, p):
    corpo, atualizar = rv.criar_revolucao(
        metodo, p.get("perfil", "raiz"), p.get("comprimento", 4.0), p.get("raio_max", 1.6), p.get("raio_base", 2.0),
        p.get("altura", 3.0), int(p["fatia"]), p["posicao_fatia"], p["espessura_fatia"], int(p["perfil_visivel"]),
        int(p["eixo"]), int(p["movimento"]), p["fase"])
    res = {"enquadrar": [corpo], "apos_camera": None}
    if int(p["movimento"]):
        res["atualizar"] = atualizar
    return res


def solido_revolucao_disco(p):
    return _revolucao("disco", p)


def solido_revolucao_arruela(p):
    return _revolucao("arruela", p)


def solido_revolucao_cascas(p):
    return _revolucao("casca", p)


def capacitor_placas_paralelas(p):
    proxy = cp.criar_capacitor_placas(p["lado"], p["distancia"], p["espessura"], int(p["n_cargas"]), p["dist_min"],
                                      int(p["dieletrico"]), int(p["semente"]))
    return {"enquadrar": [proxy], "apos_camera": lambda cam: cm.ajustar_profundidade(cam, proxy)}


def capacitor_esferico(p):
    externa = cp.criar_capacitor_esferico(p["raio_a"], p["raio_b"], p["espessura"], int(p["n_cargas"]), corte=int(p["corte"]))
    return {"enquadrar": [externa], "apos_camera": lambda cam: cm.ajustar_profundidade(cam, externa)}


def lente_delgada(p):
    corpo = ot.criar_lente(p["forma"], p["diametro"], p["raio1"], p["raio2"], p["espessura_borda"], p["indice"],
                           int(p["focos"]), int(p["eixo"]))
    f = 1.0 / ((p["indice"] - 1) * (1 / p["raio1"] + 1 / p["raio2"]))
    proxy = cp._proxy((2 * (f + 0.7), p["diametro"] * 1.15, p["diametro"] * 1.15))
    return {"enquadrar": [proxy], "apos_camera": None}


def prisma_triangular(p):
    corpo = ot.criar_prisma(p["angulo_apice"], p["base"], p["comprimento"], int(p["eixo"]))
    return {"enquadrar": [corpo], "apos_camera": None}


def anteparo_fenda_dupla(p):
    ot.criar_fenda_dupla(p["largura"], p["altura"], p["espessura"], p["fenda"], p["separacao"])
    proxy = cp._proxy((p["espessura"] * 4, p["largura"], p["altura"]))
    return {"enquadrar": [proxy], "apos_camera": None}


def caixa_gas_cinetica(p):
    cont, atualizar = tf.criar_caixa_gas(p["comprimento"], p["largura"], int(p["n_moleculas"]), p["temperatura"],
                                         p["pistao"], p["amplitude_pistao"], int(p["semente"]), p["fase"])
    res = {"enquadrar": [cont], "apos_camera": lambda cam: cm.ajustar_profundidade(cam, cont)}
    if int(p["movimento"]):
        res["atualizar"] = atualizar
    return res


def tubo_escoamento(p):
    tubo, atualizar = tf.criar_tubo(p["comprimento"], p["raio"], p["razao"], int(p["n_particulas"]), int(p["semente"]), p["fase"])
    res = {"enquadrar": [tubo], "apos_camera": lambda cam: cm.ajustar_profundidade(cam, tubo)}
    if int(p["movimento"]):
        res["atualizar"] = atualizar
    return res


def _mov(res, atualizar, p):
    if int(p["movimento"]):
        res["atualizar"] = atualizar
    return res


def orbita_kepleriana(p):
    proxy, atu = gr.criar_orbita(p["semi_eixo"], p["excentricidade"], int(p["setores"]), p["fracao_setor"], 0.42, 0.17,
                                 int(p["vetor"]), p["fase"])
    return _mov({"enquadrar": [proxy], "apos_camera": None}, atu, p)


def poco_gravitacional(p):
    corpo, atu = gr.criar_poco(p["raio_max"], p["profundidade"], p["raio_nucleo"], int(p["bola"]), p["raio_bola"], p["fase"])
    return _mov({"enquadrar": [corpo], "apos_camera": None}, atu, p)


def campo_vetorial(p):
    proxy = cv.criar_campo(p["tipo"], int(p["dim"]), int(p["n"]), p["extensao"])
    return {"enquadrar": [proxy], "apos_camera": None}


def superficie_parametrizada(p):
    corpo, atu = cv.criar_superficie_param(p["tipo"], p["u0"], p["v0"], p["tamanho_remendo"], int(p["vetores"]),
                                           int(p["linhas"]), int(p["movimento"]), p["fase"])
    return _mov({"enquadrar": [corpo], "apos_camera": None}, atu, p)


def teorema_stokes(p):
    corpo, atu = cv.criar_stokes(p["raio"], int(p["com_campo"]), int(p["normais"]), int(p["contorno_continuo"]),
                                 int(p["movimento"]), p["fase"])
    return _mov({"enquadrar": [corpo], "apos_camera": None}, atu, p)


def gradiente_colina(p):
    corpo, atu = cv.criar_gradiente(p["altura"], p["abertura"], p["extensao"], int(p["n_niveis"]), p["raio_ponto"],
                                    int(p["movimento"]), p["fase"])
    return _mov({"enquadrar": [corpo], "apos_camera": None}, atu, p)


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
    "solenoide_corrente": solenoide_corrente,
    "toroide_corrente": toroide_corrente,
    "fio_infinito": fio_infinito,
    "amperiano_circular": amperiano_circular,
    "amperiano_retangular": amperiano_retangular,
    "esfera_rolando": esfera_rolando,
    "cilindro_rolando": cilindro_rolando,
    "aro_rolando": aro_rolando,
    "solido_revolucao_disco": solido_revolucao_disco,
    "solido_revolucao_arruela": solido_revolucao_arruela,
    "solido_revolucao_cascas": solido_revolucao_cascas,
    "capacitor_placas_paralelas": capacitor_placas_paralelas,
    "capacitor_esferico": capacitor_esferico,
    "lente_delgada": lente_delgada,
    "prisma_triangular": prisma_triangular,
    "anteparo_fenda_dupla": anteparo_fenda_dupla,
    "caixa_gas_cinetica": caixa_gas_cinetica,
    "tubo_escoamento": tubo_escoamento,
    "orbita_kepleriana": orbita_kepleriana,
    "poco_gravitacional": poco_gravitacional,
    "campo_vetorial": campo_vetorial,
    "superficie_parametrizada": superficie_parametrizada,
    "teorema_stokes": teorema_stokes,
    "gradiente_colina": gradiente_colina,
}

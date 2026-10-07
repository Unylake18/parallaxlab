"""Abre um sólido do arsenal na janela do Blender, já montado, enquadrado e (se tiver movimento) tocando em loop — sandbox.

Normalmente chamado pelos atalhos de `abrir/<id>.bat` (gerados por `gerar_atalhos.py`). À mão, a partir da raiz do repositório:
    blender.exe -P experimentos/blender/arsenal/abrir_no_blender.py -- <id> [--set nome=valor ...]

Sem `--set`, usa o mesmo estado ilustrativo do preview (`preview_set` da ficha). Os parâmetros ficam no código: troque-os com `--set`.
No Blender: a vista 3D abre pela câmera em modo Renderizado (Eevee); o loop toca sozinho (espaço pausa/retoma, setas ← → andam um quadro)
e a cena pode ser salva como .blend à vontade (os .blend não vão para o Git).
"""

import json
import sys
from pathlib import Path

import bpy

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
sys.path.insert(0, str(AQUI.parent))
import casca_oca as co  # noqa: E402
import renderizar as R  # noqa: E402
from construtores import CONSTRUTORES  # noqa: E402

ESTADO = {}


def _limpar_sem_recarregar():
    """`co.limpar_cena` recarrega o Blender de fábrica, o que derruba a interface aberta: aqui só se apaga o conteúdo."""
    for o in list(bpy.data.objects):
        bpy.data.objects.remove(o, do_unlink=True)
    for colecao in (bpy.data.meshes, bpy.data.curves, bpy.data.materials, bpy.data.lights, bpy.data.cameras, bpy.data.worlds, bpy.data.node_groups):
        for bloco in list(colecao):
            colecao.remove(bloco)


def _ao_mudar_quadro(cena, *_):
    atualizar, n, unico = ESTADO.get("atualizar"), ESTADO["n"], ESTADO["unico"]
    if atualizar:
        i = min(max(cena.frame_current - 1, 0), n - 1)
        atualizar(i / (n - 1) if unico else i / n)


def _preparar_janela():
    """Roda depois que a interface existe: câmera + Renderizado na vista 3D e começa a tocar."""
    for janela in bpy.context.window_manager.windows:
        for area in janela.screen.areas:
            if area.type != "VIEW_3D":
                continue
            espaco = area.spaces.active
            espaco.shading.type = "RENDERED"
            espaco.region_3d.view_perspective = "CAMERA"
            espaco.overlay.show_overlays = False
            if ESTADO.get("atualizar"):
                with bpy.context.temp_override(window=janela, area=area):
                    bpy.ops.screen.animation_play()
            return None
    return 0.5          # interface ainda não pronta: tenta de novo


def main():
    resto = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    if not resto:
        raise SystemExit("Uso: blender -P abrir_no_blender.py -- <id> [--set nome=valor ...]")
    solido, overrides = resto[0], [resto[i + 1] for i, x in enumerate(resto) if x == "--set" and i + 1 < len(resto)]
    ficha = json.loads((AQUI / "solidos" / f"{solido}.json").read_text(encoding="utf-8"))
    p = R.parametros(ficha, overrides or ficha.get("preview_set", []))

    (_limpar_sem_recarregar if not bpy.app.background else co.limpar_cena)()
    res = CONSTRUTORES[ficha["construtor"]](p)
    co.mundo()
    co.luzes()
    e = ficha["enquadramento"]
    cam = co.camera_enquadrada(co.cantos(res["enquadrar"]), azimute=e["azimute"], elevacao=e["elevacao"],
                               lente=e["lente"], margem=e["margem"], largura=1280, altura=720)
    if res["apos_camera"]:
        res["apos_camera"](cam)

    for o in bpy.data.objects:                      # caixas de enquadramento (hide_render) não somem sozinhas na vista Renderizada
        if o.hide_render:
            o.hide_viewport = True
    sc = bpy.context.scene
    for nome in ("BLENDER_EEVEE", "BLENDER_EEVEE_NEXT"):
        try:
            sc.render.engine = nome
            break
        except TypeError:
            continue
    sc.render.resolution_x, sc.render.resolution_y = 1280, 720
    sc.render.fps = co.ST["render"]["preview"]["fps"]
    sc.view_settings.view_transform = co.ST["render"]["view_transform"]

    anim = ficha.get("animacao")
    n = int(anim["frames_sugeridos"]) if anim else 1
    ESTADO.update(atualizar=res.get("atualizar"), n=max(n, 2), unico=bool(anim and anim.get("ciclo") == "unico"))
    sc.frame_start, sc.frame_end, sc.frame_current = 1, n, 1
    sc.render.use_lock_interface = True
    if ESTADO["atualizar"]:
        bpy.app.handlers.frame_change_post.append(_ao_mudar_quadro)
        _ao_mudar_quadro(sc)
    bpy.app.timers.register(_preparar_janela, first_interval=1.0)
    tipo = "ciclo único" if ESTADO["unico"] else ("loop" if anim else "estático")
    print(f"ARSENAL abrir: {solido} ({ficha['status']}, {tipo}) — {ficha['nome']}")


def _construir_na_janela():
    """Na interface o contexto (objeto ativo etc.) só existe dentro de uma janela/área: monta o sólido sob um override."""
    for janela in bpy.context.window_manager.windows:
        for area in janela.screen.areas:
            if area.type != "VIEW_3D":
                continue
            regiao = next(r for r in area.regions if r.type == "WINDOW")
            visao = bpy.context.preferences.view
            traduz = visao.use_translate_new_dataname
            visao.use_translate_new_dataname = False       # com a interface em português os nós nascem como "BSDF Principled"
            try:
                with bpy.context.temp_override(window=janela, screen=janela.screen, area=area, region=regiao,
                                               scene=janela.scene, view_layer=janela.view_layer):
                    main()
            finally:
                visao.use_translate_new_dataname = traduz
            return None
    return 0.5          # interface ainda não pronta: tenta de novo


if bpy.app.background:
    main()
else:
    bpy.app.timers.register(_construir_na_janela, first_interval=0.5)

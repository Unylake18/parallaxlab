"""Junta os MP4 dos casos (mesmo formato: 960x540, 30 fps) num único vídeo, na ordem do vídeo principal de Gauss. Sem áudio.
    uv run python experimentos/blender/preview_todos_limpo/juntar.py
"""
import shutil
from pathlib import Path

import av

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parents[2]
ORDEM = [("linha", "LinhaLimpo"), ("casca_cil", "CascaCilLimpo"), ("macico_cil", "MacicoCilLimpo"), ("coax", None), ("folha", "FolhaLimpo"),
         ("placa", "PlacaLimpo"), ("duas", "DuasLimpo"), ("face", "FaceLimpo"), ("casca_esf", "CascaEsfLimpo"), ("macico_esf", "MacicoEsfLimpo"),
         ("cap_esf", "CapEsfLimpo")]
saida = AQUI / "saida"
saida.mkdir(exist_ok=True)
fontes = []
for n, (cid, cls) in enumerate(ORDEM, 1):
    if cid == "coax":
        src = RAIZ / "experimentos/blender/preview_coaxial_3d_limpo/saida/CoaxialLimpo_540p30.mp4"
        cls = "CoaxialLimpo"
    else:
        src = RAIZ / f"media/preview_todos_limpo/{cid}/videos/cena_todos/540p30/{cls}.mp4"
    dst = saida / f"{n:02d}_{cid}_540p30.mp4"
    shutil.copy(src, dst)
    fontes.append(dst)
out = av.open(str(saida / "TODOS_limpo_540p30.mp4"), "w")
st = out.add_stream("libx264", rate=30)
st.width, st.height, st.pix_fmt = 960, 540, "yuv420p"
st.options = {"crf": "18", "preset": "medium"}
total = 0
for f in fontes:
    for fr in av.open(str(f)).decode(video=0):
        for pk in st.encode(av.VideoFrame.from_ndarray(fr.to_ndarray(format="rgb24"), format="rgb24")):
            out.mux(pk)
        total += 1
for pk in st.encode():
    out.mux(pk)
out.close()
print("quadros", total, "duração", round(total / 30, 1), "s")

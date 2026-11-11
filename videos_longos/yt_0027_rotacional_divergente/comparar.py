"""yt_0027 v2 (handoff v2 §6.1): os 24 lado a lado. Para cada quadro-alvo, acha o instante no lote (pelos logs do render: [ancora], [gatilho], [motor]),
renderiza o still a 1920×1080 (still1080.sh; no B6 o 3D é renderizado à parte a 1920×1080 com o estado do pedidos3d e composto por baixo do Manim) e monta
renders/v2/qa/lado_a_lado_NN_<nome>.png (render à esquerda, alvo à direita, 1920×1080 cada lado, reduzidos para 1920×540 no arquivo).
uso: python comparar.py [NN ...]  (sem argumentos: os 24)
v3 (handoff v3 §7.2): RODADA=v3 python comparar.py → os 11 alvos v3 (referencia_v3, números 101–111) e os alvos v2 que tocam as cenas corrigidas,
tudo em renders/v3/qa/."""
import json
import math
import os
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

U = Path(__file__).resolve().parent
RODADA = os.environ.get("RODADA", "v2")
ALVOS = U / "referencia_v2" / "yt_0027_quadros_alvo_v2"
ALVOS3 = U / "referencia_v3"
ALVOS4 = U / "referencia_v4"
OUT = U / "renders" / RODADA / "qa"
OUT.mkdir(parents=True, exist_ok=True)


def log(lote):
    return (U / f"log_{lote}.txt").read_text(encoding="utf-8", errors="replace")


def inicios(lote):
    return {m.group(1): float(m.group(2)) for m in re.finditer(r"\[ancora\] (\S+) ([0-9.]+)", log(lote))}


def gat(lote, anc, frase):
    for l in log(lote).splitlines():
        m = re.match(r"\[gatilho\] (\S+)\s+([0-9.]+)s .*?\) (.*)$", l)
        if m and m.group(1) == anc and frase in m.group(3):
            return inicios(lote)[anc] + float(m.group(2))
    raise KeyError((lote, anc, frase))


def total(lote):
    return float(re.search(r"\[tempo\] total ([0-9.]+)s", log(lote)).group(1))


def fim(lote, anc, prox=None, folga=0.4):
    i = inicios(lote)
    return round((i[prox] if prox else total(lote) - 0.9) - folga, 2)


def h2_t39():
    l = log("PHA")
    rt1 = float(re.search(r"\[motor\] H2: t de 0 a 2π em ([0-9.]+) s", l).group(1))
    return round(gat("PHA", "H2", "no primeiro") + 3.9 / (2 * math.pi) * rt1, 2)


ALVO = {
    1: ("01_H2_dois_redemoinhos", "PHA", h2_t39),
    2: ("02_H3_mesmas_setas", "PHA", lambda: fim("PHA", "H3", "A1", 0.7)),
    3: ("03_B1-3_tres_coisas", "PB1", lambda: fim("PB1", "B1-3")),
    4: ("04_B2-2_braco_horizontal", "PB2", lambda: fim("PB2", "B2-2", "B2-3")),
    5: ("05_B2-3_braco_vertical", "PB2", lambda: fim("PB2", "B2-3", "B2-4")),
    6: ("06_B2-4_tesoura_e_rodinha", "PB2", lambda: fim("PB2", "B2-4", "B2-5")),
    7: ("07_B2-5_rotacional", "PB2", lambda: fim("PB2", "B2-5", "B2-6")),
    8: ("08_B3-1-2_vortice_bracos", "PB3", lambda: fim("PB3", "B3-2", "B3-3")),
    9: ("09_B3-4_tornado", "PB3", lambda: fim("PB3", "B3-4", "B3-5")),
    10: ("10_B3-6_rio", "PB3", lambda: fim("PB3", "B3-6")),
    11: ("11_B4-2_divergente", "PB4", lambda: fim("PB4", "B4-2", "B4-3")),
    12: ("12_B4-4_caixa_saldo", "PB4", lambda: fim("PB4", "B4-4", "B4-5")),
    13: ("13_B4-5_caixa_encolhe", "PB4", lambda: fim("PB4", "B4-5", "B4-6")),
    14: ("14_B4-6_mapa_div", "PB4", lambda: fim("PB4", "B4-6")),
    15: ("15_B5-2_falsa_fonte_setor", "PB5", lambda: round(gat("PB5", "B5-2", "coloca uma caixa parada") - 0.3, 2)),
    16: ("16_B5-2_falsa_fonte_caixa", "PB5", lambda: fim("PB5", "B5-2", "B5-3")),
    17: ("17_B6-1_cubo", "PB6", lambda: fim("PB6", "B6-1", "B6-2", 1.0)),
    18: ("18_B6-2_rodinha_inclinada", "PB6", lambda: round(gat("PB6", "B6-2", "deita a rodinha de lado") + 3.0 * 5 / 45, 2)),
    19: ("19_B6-3_rot_no_espaco", "PB6", lambda: fim("PB6", "B6-3")),
    20: ("20_F1_fio_carregado", "PF", lambda: fim("PF", "F1", "F2", 0.7)),
    21: ("21_F2_fio_com_corrente", "PF", lambda: fim("PF", "F2")),
    22: ("22_B7-3_valor_media", "PB7", lambda: fim("PB7", "B7-3", "B7-4", 0.7)),
    23: ("23_B7-4_calor", "PB7", lambda: round((inicios("PB7")["B7-4"] + total("PB7")) / 2, 2)),
    24: ("24_S2_local_global", "PS", lambda: fim("PS", "S2", "S3")),
}


def still(lote, t):
    arq = OUT / f"still1080_{lote}_{t}.png"
    if not arq.exists():
        subprocess.run(["C:/Program Files/Git/bin/bash.exe", "still1080.sh", lote, str(t)], cwd=U, check=False, env=dict(os.environ, QA=f"renders/{RODADA}/qa"))
    if lote == "PB6":
        compoe_3d(lote, t, arq)
    return arq


def compoe_3d(lote, t, arq):
    """O still -s do Manim não cola o 3D: renderiza a cena 3D a 1920×1080 com o estado do quadro e põe por baixo da camada do Manim."""
    ped = json.loads((U / "threejs" / "pedidos3d" / f"{lote}.json").read_text(encoding="utf-8"))["cenas"]
    f = round(t * 15)
    cena, est = None, None
    for c, lista in ped.items():
        d = dict(lista)
        if f in d:
            cena, est = c, d[f]
    if cena is None:
        return
    png = OUT / f"_3d_{lote}_{t}.png"
    env = dict(os.environ, CHROMIUM_PATH="C:/Program Files/Google/Chrome/Application/chrome.exe",
               NODE_PATH=str((U.parent / "yt_0020_cinematica_angular" / "threejs" / "node_modules").resolve()))
    subprocess.run(["node", "r3d.js", "--w", "1920", "--h", "1080", "--sonda", cena, "--estado", json.dumps(est), "--png", str(png)], cwd=U / "threejs",
                   env=env, capture_output=True)
    m = np.asarray(Image.open(arq).convert("RGB"), float)
    bg = np.asarray(Image.open(U / "renders" / "fundo" / "fundo27_milimetrado_1920x1080.png").convert("RGB"), float)
    tr = np.asarray(Image.open(png).convert("RGBA"), float)
    a = tr[..., 3:] / 255
    base = bg * (1 - a) + tr[..., :3] * a
    cont = (np.abs(m - bg).max(2) > 10)[..., None]
    Image.fromarray(np.where(cont, m, base).astype(np.uint8)).save(arq)


MEIO = {1, 18}        # instantes no MEIO de uma animação longa: o still -s mostra o começo dela; usa o quadro do vídeo da seção (960×540)


def quadro_video(lote, t):
    import av
    c = av.open(str(U / f"media_{lote}" / "videos" / "cena" / "540p15" / f"{lote}.mp4"))
    alvo = round(t * 15)
    for i, fr in enumerate(c.decode(video=0)):
        if i == alvo:
            im = fr.to_image()
            c.close()
            return im
    c.close()


def lado(n):
    nome, lote, tf = ALVO[n]
    t = tf()
    if n in MEIO:
        r = quadro_video(lote, t).convert("RGB")
        r.save(OUT / f"quadro540_{lote}_{t}.png")
    else:
        r = Image.open(still(lote, t)).convert("RGB").resize((960, 540))
    a = Image.open((ALVOS4 if n > 200 else ALVOS3 if n > 100 else ALVOS) / f"{nome}.jpg").convert("RGB").resize((960, 540))
    p = Image.new("RGB", (1920, 540))
    p.paste(r, (0, 0))
    p.paste(a, (960, 0))
    d = ImageDraw.Draw(p)
    d.text((8, 6), f"RENDER {lote} t={t}s", fill="yellow")
    d.text((968, 6), f"ALVO {nome}", fill="yellow")
    p.save(OUT / f"lado_a_lado_{nome}.png")
    return n, lote, t


ALVO.update({
    101: ("01_B1-1_seta_velocidade", "PB1", lambda: fim("PB1", "B1-1", "B1-2")),
    102: ("02_B1-3_deforma_nomeado", "PB1", lambda: fim("PB1", "B1-3")),
    103: ("03_B2-4_rotulos_sem_sobrepor", "PB2", lambda: round(gat("PB2", "B2-4", "uma rodinha de pás não vira tesoura") - 0.4, 2)),
    104: ("04_B5-2_numeros_com_clareira", "PB5", lambda: fim("PB5", "B5-2", "B5-3")),
    105: ("05_B6-1_cubo_novo", "PB6", lambda: fim("PB6", "B6-1", "B6-2", 1.0)),
    106: ("06_F1_rotulo_com_clareira", "PF", lambda: fim("PF", "F1", "F2", 0.7)),
    107: ("07_B7-3_niveis_com_clareira", "PB7", lambda: fim("PB7", "B7-3", "B7-4", 0.7)),
    108: ("08_B7-4a_calor_vale", "PB7", lambda: round(gat("PB7", "B7-4", "vai se enchendo") - 0.3, 2)),
    109: ("09_B7-4b_calor_vale_enchendo", "PB7", lambda: fim("PB7", "B7-4")),
    110: ("10_S3_local_global", "PS", lambda: fim("PS", "S3", "S4")),
    111: ("11_S4_terceira_coisa_e_gancho", "PS", lambda: round(gat("PS", "S4", "no próximo vídeo") - 0.3, 2)),
})
ALVO.update({
    201: ("01_B1-1_seta_velocidade", "PB1", lambda: fim("PB1", "B1-1", "B1-2")),
    202: ("02_B1-3_deforma_nomeado", "PB1", lambda: fim("PB1", "B1-3")),
    205: ("05_B6-1_cubo_novo", "PB6", lambda: fim("PB6", "B6-1", "B6-2", 1.0)),
    207: ("07_B7-3_niveis_com_clareira", "PB7", lambda: fim("PB7", "B7-3", "B7-4", 0.7)),
    208: ("08_B7-4a_calor_vale", "PB7", lambda: round(gat("PB7", "B7-4", "vai se enchendo") - 0.3, 2)),
    211: ("11_S4_terceira_coisa_e_gancho", "PS", lambda: round(gat("PS", "S4", "no próximo vídeo") - 0.3, 2)),
    212: ("12_B4-1_pedacinho_com_malha", "PB4", lambda: fim("PB4", "B4-2", "B4-3")),
    213: ("13_B5-2_setor_com_malha", "PB5", lambda: round(gat("PB5", "B5-2", "as derivadas dizem o mesmo") - 0.3, 2)),
    214: ("14_B1-1a_definicao_P_Q", "PB1", lambda: fim("PB1", "B1-1a", "B1-1")),
    215: ("15_B2-6_P_Q_e_vorticidade", "PB2", lambda: fim("PB2", "B2-6")),
    216: ("16_B6-0_definicao_geral", "PB6", lambda: fim("PB6", "B6-0", "B6-1")),
    217: ("17_B6-3_rot_expandido", "PB6", lambda: fim("PB6", "B6-3")),
})
V2_TOCADOS = [4, 5, 7, 8, 9, 10, 11, 12, 13, 14, 15, 18, 19, 21, 24]      # alvos v2 das cenas corrigidas que não ganharam alvo v3

if __name__ == "__main__":
    ns = [int(a) for a in sys.argv[1:]] or (sorted(k for k in ALVO if k > 200) if RODADA == "v4" else
                                            sorted(k for k in ALVO if 100 < k < 200) + V2_TOCADOS if RODADA == "v3" else sorted(k for k in ALVO if k < 100))
    with ThreadPoolExecutor(6) as ex:
        for n, lote, t in ex.map(lado, ns):
            print(f"[lado] {n:02d} {ALVO[n][0]}: {lote} t = {t} s")

"""yt_0018 — monta a pasta final em entregas/Vídeos Longos/ (cópia; não move nem apaga origens). Modelo: entregar_yt0010.py.

Uso: uv run --no-sync python videos_longos/yt_0018_exercicios_centro_massa/entregar_yt0018.py
Gera: master (1920×1080 / 30 fps, H.264 CRF 14, voz AAC), legenda (.srt), capitulos (.txt), audio/, texto/ e manifesto (origem, tamanho, SHA-256, dados do vídeo).
Sem capa (não pedida).
"""
import hashlib
import json
import shutil
from pathlib import Path

import av

PASTA = Path(__file__).resolve().parent
ROOT = PASTA.parents[1]
N = "yt0018"
DEST = ROOT / "entregas" / "Vídeos Longos" / "Mecânica - Momento - Exercícios de centro de massa"
MASTER = PASTA / "renders" / "master_yt0018_1920x1080.mp4"
SRT = PASTA / "renders" / "legenda_yt0018.srt"
CAPITULOS = [  # (início em s, título) — os inícios vêm de renders/capitulos_final.txt (montar_final.py)
    ("0:00", "O gafanhoto na folha: onde ele precisa pular?"),
    ("0:39", "Abertura: seis problemas, três perguntas"),
    ("1:22", "Problema 1: o disco furado"),
    ("1:59", "Problema 2: a placa com furo"),
    ("3:14", "Problema 3: o fio no cubo"),
    ("4:43", "Problema 4: o gafanhoto e a folha"),
    ("8:28", "Problema 5: as naves"),
    ("10:05", "Problema 6: a balança"),
    ("12:23", "Epílogo: a luz também empurra"),
    ("12:58", "Resumo: as três perguntas"),
    ("13:34", "Encerramento"),
]


def sha(f):
    h = hashlib.sha256()
    with open(f, "rb") as fh:
        for b in iter(lambda: fh.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def main():
    (DEST / "audio").mkdir(parents=True, exist_ok=True)
    (DEST / "texto").mkdir(parents=True, exist_ok=True)
    cap = "\n".join(f"{t} {n}" for t, n in CAPITULOS) + "\n"
    (DEST / f"capitulos - {N}.txt").write_text(cap, encoding="utf-8")
    cop = [
        (MASTER, f"master - {N}.mp4"),
        (SRT, f"legenda - {N}.srt"),
        (PASTA / "audio" / "narracao_v7.wav", f"audio/narracao_v7 - {N}.wav"),
        (PASTA / "ficha.md", f"texto/ficha - {N}.md"),
        (PASTA / "narracao_tags_v1_4.md", f"texto/narracao_tags_v1_4 - {N}.md"),
    ]
    arquivos = []
    for o, d in cop:
        shutil.copy2(o, DEST / d)
        arquivos.append({"arquivo": d.replace("/", "\\"), "bytes": (DEST / d).stat().st_size, "sha256": sha(DEST / d)})
    arquivos.append({"arquivo": f"capitulos - {N}.txt", "bytes": (DEST / f"capitulos - {N}.txt").stat().st_size, "sha256": sha(DEST / f"capitulos - {N}.txt")})
    with av.open(str(DEST / f"master - {N}.mp4")) as c:
        v = c.streams.video[0]
        info = {"resolucao": f"{v.width}x{v.height}", "fps": float(v.average_rate), "duracao_s": round(float(c.duration) / 1e6, 2),
                "codec": "H.264 yuv420p CRF 14", "audio": "AAC 192 kb/s mono 44,1 kHz" if c.streams.audio else None}
    man = {"unidade": "yt_0018", "titulo": "Centro de massa: 6 problemas que parecem impossíveis",
           "rotulo_na_tela": "Mecânica · Centro de massa: problemas",
           "arquivos": sorted(arquivos, key=lambda a: a["arquivo"]), "video": info}
    (DEST / f"manifesto - {N}.json").write_text(json.dumps(man, ensure_ascii=False, indent=1), encoding="utf-8")
    print("entrega em", DEST)
    print(json.dumps(info, ensure_ascii=False))


if __name__ == "__main__":
    main()

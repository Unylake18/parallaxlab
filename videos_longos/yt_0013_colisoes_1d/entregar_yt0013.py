"""yt_0013 — monta a pasta final em entregas/Vídeos Longos/ (cópia; não move nem apaga origens).

Uso: uv run --no-sync python videos_longos/yt_0013_colisoes_1d/entregar_yt0013.py
Gera: master, legenda (.srt), capitulos (.txt), audio/, texto/ e manifesto (origem, tamanho, SHA-256, dados do vídeo).
Legenda e capítulos vêm de montar_sync.py (mesma base de tempo do master, com as pausas de ritmo).
"""
import hashlib
import json
import shutil
from pathlib import Path

import av

PASTA = Path(__file__).resolve().parent
ROOT = PASTA.parents[1]
N = "yt0013"
DEST = ROOT / "entregas" / "Vídeos Longos" / "Mecânica - Colisões - Colisões em 1D"


def sha(f):
    h = hashlib.sha256()
    with open(f, "rb") as fh:
        for b in iter(lambda: fh.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def main():
    (DEST / "audio").mkdir(parents=True, exist_ok=True)
    (DEST / "texto").mkdir(parents=True, exist_ok=True)
    F = PASTA / "final"
    cop = [
        (F / "master - 0013.mp4", f"master - {N}.mp4"),
        (F / "legenda - 0013.srt", f"legenda - {N}.srt"),
        (F / "capitulos - 0013.txt", f"capitulos - {N}.txt"),
        (PASTA / "audio" / "narracao_sync.wav", f"audio/narracao_sync - {N}.wav"),
        (PASTA / "audio" / "narracao_v4.wav", f"audio/narracao_v4 - {N}.wav"),
        (PASTA / "ficha.md", f"texto/ficha - {N}.md"),
        (PASTA / "direcao_v2.md", f"texto/direcao - {N}.md"),
        (PASTA / "narracao_sugestao.md", f"texto/narracao - {N}.md"),
        (PASTA / "narracao_tags.md", f"texto/narracao_tags - {N}.md"),
        (PASTA / "audio" / "texto_voz_v4.txt", f"texto/texto_narracao - {N}.txt"),
    ]
    arquivos = []
    for o, d in cop:
        shutil.copy2(o, DEST / d)
        arquivos.append({"arquivo": d.replace("/", "\\"), "origem": str(o), "bytes": (DEST / d).stat().st_size,
                         "sha256": sha(DEST / d)})
    with av.open(str(DEST / f"master - {N}.mp4")) as c:
        v = c.streams.video[0]
        info = {"resolucao": f"{v.width}x{v.height}", "fps": float(v.average_rate), "duracao_s": round(float(c.duration) / 1e6, 2),
                "codec": "H.264 yuv420p CRF 14", "audio": bool(c.streams.audio)}
    man = {"unidade": "yt_0013", "titulo": "Colisões em 1D", "pergunta": "Como saber o que acontece depois?",
           "rotulo_na_tela": "Mecânica · Colisões em 1D", "sincronia": "265 âncoras (ritmo.json), alinhamento forçado ElevenLabs",
           "arquivos": sorted(arquivos, key=lambda a: a["arquivo"]), "video": info}
    (DEST / f"manifesto - {N}.json").write_text(json.dumps(man, ensure_ascii=False, indent=1), encoding="utf-8")
    print("entrega em", DEST)
    print(json.dumps(info, ensure_ascii=False))


if __name__ == "__main__":
    main()

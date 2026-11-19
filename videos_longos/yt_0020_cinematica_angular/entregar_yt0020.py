"""yt_0020 — monta a pasta final em entregas/Vídeos Longos/Física I/ (cópia; não move nem apaga origens). Modelo: entregar_yt0018.py.

Uso: uv run --no-sync python videos_longos/yt_0020_momento_inercia/entregar_yt0020.py
Gera: master (1920×1080 / 30 fps, H.264 CRF 14, voz AAC), legenda (.srt), capitulos (.txt), audio/, texto/ e manifesto (origem, tamanho, SHA-256, dados do vídeo).
Sem capa (fluxo separado, ainda não feita). Sem série/EP (longo)."""
import hashlib
import json
import shutil
from pathlib import Path

import av

PASTA = Path(__file__).resolve().parent
ROOT = PASTA.parents[1]
N = "yt0020"
DEST = ROOT / "entregas" / "Vídeos Longos" / "Física I" / "Mecânica - Rotação - Cinemática angular"
MASTER = PASTA / "renders" / "master_yt0020_1920x1080.mp4"


def sha(f):
    h = hashlib.sha256()
    with open(f, "rb") as fh:
        for b in iter(lambda: fh.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def main():
    (DEST / "audio").mkdir(parents=True, exist_ok=True)
    (DEST / "texto").mkdir(parents=True, exist_ok=True)
    linhas = [l for l in (PASTA / "renders" / "capitulos_Fv1.txt").read_text(encoding="utf-8").splitlines() if l.strip()]
    (DEST / f"capitulos - {N}.txt").write_text(chr(10).join(linhas) + chr(10), encoding="utf-8")
    cop = [
        (MASTER, f"master - {N}.mp4"),
        (PASTA / "audio" / "narracao_v6.wav", f"audio/narracao_v6 - {N}.wav"),
        (PASTA / "ficha.md", f"texto/ficha - {N}.md"),
        (PASTA / "narracao_tags.md", f"texto/narracao_tags - {N}.md"),
    ]
    arquivos = []
    for o, d in cop:
        shutil.copy2(o, DEST / d)
        arquivos.append({"arquivo": d.replace("/", "\\"), "origem": str(o.relative_to(ROOT)), "bytes": (DEST / d).stat().st_size, "sha256": sha(DEST / d)})
    f = DEST / f"capitulos - {N}.txt"
    arquivos.append({"arquivo": f.name, "bytes": f.stat().st_size, "sha256": sha(f)})
    with av.open(str(DEST / f"master - {N}.mp4")) as c:
        v = c.streams.video[0]
        info = {"resolucao": f"{v.width}x{v.height}", "fps": float(v.average_rate), "duracao_s": round(float(c.duration) / 1e6, 2),
                "codec": "H.264 yuv420p CRF 14", "audio": "AAC 192 kb/s mono 44,1 kHz" if c.streams.audio else None}
    man = {"unidade": "yt_0020", "titulo": "Por que a ponta da hélice chega a quase 1.000 km/h? (cinemática angular)",
           "rotulo_na_tela": "Mecânica · Cinemática angular", "capa": "pendente (fluxo separado)", "legenda": "pendente (SRT não gerado)",
           "arquivos": sorted(arquivos, key=lambda a: a["arquivo"]), "video": info}
    (DEST / f"manifesto - {N}.json").write_text(json.dumps(man, ensure_ascii=False, indent=1), encoding="utf-8")
    print("entrega em", DEST)
    print(json.dumps(info, ensure_ascii=False))


if __name__ == "__main__":
    main()

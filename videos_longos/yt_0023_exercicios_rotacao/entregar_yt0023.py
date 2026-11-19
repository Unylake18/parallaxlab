"""yt_0023 — monta a pasta final em entregas/Vídeos Longos/Física I/ (cópia; não move nem apaga origens). Modelo: entregar_yt0018.py.

Uso: uv run --no-sync python videos_longos/yt_0023_momento_inercia/entregar_yt0023.py
Gera: master (1920×1080 / 30 fps, H.264 CRF 14, voz AAC), legenda (.srt), capitulos (.txt), audio/, texto/ e manifesto (origem, tamanho, SHA-256, dados do vídeo).
Sem capa (fluxo separado, ainda não feita). Sem série/EP (longo)."""
import hashlib
import json
import shutil
from pathlib import Path

import av

PASTA = Path(__file__).resolve().parent
ROOT = PASTA.parents[1]
N = "yt0023"
DEST = ROOT / "entregas" / "Vídeos Longos" / "Física I" / "Mecânica - Rotação - Exercícios de rotação"
MASTER = PASTA / "renders" / "yt_0023_master_1920x1080.mp4"
SRT = PASTA / "renders" / "legenda_yt0023.srt"
NOMES = ["Qual bloco desce?", "Caixa de ferramentas", "O desafio da régua", "Exercício 1: o volante", "Exercício 2: a haste e o eixo", "Exercício 3: o carretel",
         "Exercício 4: o pêndulo mais rápido", "Resumo", "Encerramento e desafio"]


def sha(f):
    h = hashlib.sha256()
    with open(f, "rb") as fh:
        for b in iter(lambda: fh.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def main():
    (DEST / "audio").mkdir(parents=True, exist_ok=True)
    (DEST / "texto").mkdir(parents=True, exist_ok=True)
    tempos = [l.split(" ", 1)[0] for l in (PASTA / "renders" / "capitulos_final.txt").read_text(encoding="utf-8").splitlines() if l.strip()]
    assert len(tempos) == len(NOMES), (len(tempos), len(NOMES))
    (DEST / f"capitulos - {N}.txt").write_text("\n".join(f"{t} {n}" for t, n in zip(tempos, NOMES)) + "\n", encoding="utf-8")
    cop = [
        (MASTER, f"master - {N}.mp4"),
        (SRT, f"legenda - {N}.srt"),
        (PASTA / "audio" / "narracao_v3.wav", f"audio/narracao_v3 - {N}.wav"),
        (PASTA / "ficha.md", f"texto/ficha - {N}.md"),
        (PASTA / "narracao_final_fonte.md", f"texto/narracao_final_fonte - {N}.md"),
        (PASTA / "renders" / "qa.txt", f"texto/qa - {N}.txt"),
        (PASTA / "narracao_tags_v3.md", f"texto/narracao_tags - {N}.md"),
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
    man = {"unidade": "yt_0023", "titulo": "Dinâmica da rotação: 4 problemas em que o momento de inércia decide tudo",
           "rotulo_na_tela": "Mecânica · Exercícios de rotação", "capa": "pendente (fluxo separado)",
           "arquivos": sorted(arquivos, key=lambda a: a["arquivo"]), "video": info}
    (DEST / f"manifesto - {N}.json").write_text(json.dumps(man, ensure_ascii=False, indent=1), encoding="utf-8")
    print("entrega em", DEST)
    print(json.dumps(info, ensure_ascii=False))


if __name__ == "__main__":
    main()

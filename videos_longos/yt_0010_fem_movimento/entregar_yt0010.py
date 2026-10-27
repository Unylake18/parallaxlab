"""yt_0010 — monta a pasta final em entregas/Vídeos Longos/ (cópia; não move nem apaga origens).

Uso: uv run --no-sync python videos_longos/yt_0010_fem_movimento/entregar_yt0010.py MASTER.mp4
Gera: master, legenda (.srt), capitulos (.txt), audio/, texto/ e manifesto (origem, tamanho, SHA-256, dados do vídeo).
"""
import hashlib
import json
import shutil
import sys
from pathlib import Path

import av

PASTA = Path(__file__).resolve().parent
ROOT = PASTA.parents[1]
N = "yt0010"
DEST = ROOT / "entregas" / "Vídeos Longos" / "Eletromagnetismo - Eletrodinâmica - FEM de movimento e regra do fluxo magnético"
CAPITULOS = [  # (unidade, título)
    (0, "Abertura: uma barra, um campo e uma pergunta"),
    (2, "As convenções do aparato"),
    (4, "A força de Lorentz sobre a carga de prova"),
    (5, "A força eletromotriz de movimento"),
    (6, "Corrente e potência dissipada no resistor"),
    (8, "Duas velocidades e o trabalho magnético nulo"),
    (11, "O arrasto sobre a barra e a força externa"),
    (13, "Quem paga a conta: potência externa = potência dissipada"),
    (14, "O fluxo magnético e o sinal"),
    (18, "A regra do fluxo: fem = menos a taxa de variação do fluxo"),
    (19, "Um contorno qualquer e a faixa varrida"),
    (24, "A prova pelo produto misto"),
    (26, "Soltando a barra: a equação do movimento"),
    (31, "Separando as variáveis e a constante de tempo"),
    (35, "Velocidade, corrente e potência no tempo"),
    (40, "A energia dissipada: integral e cancelamentos"),
    (45, "Balanço de energia e conclusão"),
    (49, "Encerramento e o próximo vídeo"),
]


def sha(f):
    h = hashlib.sha256()
    with open(f, "rb") as fh:
        for b in iter(lambda: fh.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def mmss(t):
    return f"{int(t) // 60:02d}:{int(t) % 60:02d}"


def main():
    master = Path(sys.argv[1])
    fr = json.load(open(PASTA / "frases.json", encoding="utf-8"))
    (DEST / "audio").mkdir(parents=True, exist_ok=True)
    (DEST / "texto").mkdir(parents=True, exist_ok=True)
    cap = "\n".join(f"{mmss(fr[f'N{n:02d}'][0]['t0'] if n else 0)} {t}" for n, t in CAPITULOS) + "\n"
    (DEST / f"capitulos - {N}.txt").write_text(cap, encoding="utf-8")
    cop = [
        (master, f"master - {N}.mp4"),
        (master.with_suffix(".srt"), f"legenda - {N}.srt"),
        (PASTA / "audio" / "narracao_v4.wav", f"audio/narracao_v4 - {N}.wav"),
        (PASTA / "ficha.md", f"texto/ficha - {N}.md"),
        (PASTA / "narracao_sugestao.md", f"texto/narracao_sugestao - {N}.md"),
        (PASTA / "narracao_tags.md", f"texto/narracao_tags - {N}.md"),
        (PASTA / "texto_narracao.txt", f"texto/texto_narracao - {N}.txt"),
    ]
    arquivos = []
    for o, d in cop:
        shutil.copy2(o, DEST / d)
        arquivos.append({"arquivo": d.replace("/", "\\"), "bytes": (DEST / d).stat().st_size, "sha256": sha(DEST / d)})
    arquivos.append({"arquivo": f"capitulos - {N}.txt", "bytes": (DEST / f"capitulos - {N}.txt").stat().st_size,
                     "sha256": sha(DEST / f"capitulos - {N}.txt")})
    with av.open(str(DEST / f"master - {N}.mp4")) as c:
        v = c.streams.video[0]
        info = {"resolucao": f"{v.width}x{v.height}", "fps": float(v.average_rate), "duracao_s": round(float(c.duration) / 1e6, 2),
                "codec": "H.264 yuv420p CRF 14", "audio": bool(c.streams.audio)}
    man = {"unidade": "yt_0010", "titulo": "FEM de movimento e regra do fluxo magnético",
           "rotulo_na_tela": "Eletromagnetismo · FEM de movimento e regra do fluxo magnético",
           "arquivos": sorted(arquivos, key=lambda a: a["arquivo"]), "video": info}
    (DEST / f"manifesto - {N}.json").write_text(json.dumps(man, ensure_ascii=False, indent=1), encoding="utf-8")
    print("entrega em", DEST)
    print(json.dumps(info, ensure_ascii=False))


if __name__ == "__main__":
    main()

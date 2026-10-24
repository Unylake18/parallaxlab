"""yt_0011 — monta a pasta final em entregas/Vídeos Longos/ (cópia; não move nem apaga origens).

Uso: uv run --no-sync python videos_longos/yt_0011_lei_faraday/entregar_yt0011.py MASTER.mp4 NARRACAO.wav
Gera: master, legenda (.srt), capitulos (.txt), audio/, texto/ e manifesto (origem, tamanho, SHA-256, dados do vídeo).
Capítulos: início da primeira palavra de cada célula em audio/alinhamento_forcado.json (mesma base de tempo do SRT).
"""
import hashlib
import json
import shutil
import sys
from pathlib import Path

import av

PASTA = Path(__file__).resolve().parent
ROOT = PASTA.parents[1]
N = "yt0011"
DEST = ROOT / "entregas" / "Vídeos Longos" / "Eletromagnetismo - Eletrodinâmica - Lei de Faraday e campo elétrico induzido"
CAPITULOS = [  # (célula, título)
    (1, "Abertura: corrente num circuito parado"),
    (4, "Por que a fem de movimento não explica"),
    (7, "A lei de Faraday já prevê o resultado"),
    (11, "Quanto não é o mesmo que mecanismo"),
    (12, "O campo elétrico induzido"),
    (16, "Circulação não é geometria"),
    (19, "Eletrostática × indução"),
    (21, "Solenoide ideal e simetria"),
    (25, "Dentro do solenoide: E proporcional a r"),
    (30, "Na borda: caminho, superfície e fluxo"),
    (32, "Fora do solenoide: E proporcional a 1/r"),
    (36, "O perfil do campo elétrico"),
    (39, "Campo elétrico onde o campo magnético é zero"),
    (41, "Da forma integral à diferencial: Stokes"),
    (45, "Local não é global"),
    (49, "O fio só revela o campo"),
    (51, "Síntese e próximo vídeo"),
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
    master, wav = Path(sys.argv[1]), Path(sys.argv[2])
    cel = {c["chave"]: c["palavras"][0][1]
           for c in json.loads((PASTA / "audio" / "alinhamento_forcado.json").read_text(encoding="utf-8"))["celulas"]}
    (DEST / "audio").mkdir(parents=True, exist_ok=True)
    (DEST / "texto").mkdir(parents=True, exist_ok=True)
    cap = "\n".join(f"{mmss(0 if n == 1 else cel[f'N{n:03d}'])} {t}" for n, t in CAPITULOS) + "\n"
    (DEST / f"capitulos - {N}.txt").write_text(cap, encoding="utf-8")
    cop = [
        (master, f"master - {N}.mp4"),
        (PASTA / "final" / "legenda - 0011.srt", f"legenda - {N}.srt"),
        (wav, f"audio/{wav.stem} - {N}.wav"),
        (PASTA / "ficha.md", f"texto/ficha - {N}.md"),
        (PASTA / "producao.md", f"texto/producao - {N}.md"),
        (PASTA / "storyboard.md", f"texto/storyboard - {N}.md"),
        (PASTA / "narracao.md", f"texto/narracao - {N}.md"),
        (PASTA / "narracao_sugestao_v3.md", f"texto/narracao_sugestao_v3 - {N}.md"),
        (PASTA / "narracao_tags.md", f"texto/narracao_tags - {N}.md"),
        (PASTA / "audio" / "celulas.txt", f"texto/texto_narracao - {N}.txt"),
    ]
    arquivos = []
    for o, d in cop:
        shutil.copy2(o, DEST / d)
        arquivos.append({"arquivo": d.replace("/", "\\"), "origem": str(o), "bytes": (DEST / d).stat().st_size,
                         "sha256": sha(DEST / d)})
    arquivos.append({"arquivo": f"capitulos - {N}.txt", "bytes": (DEST / f"capitulos - {N}.txt").stat().st_size,
                     "sha256": sha(DEST / f"capitulos - {N}.txt")})
    with av.open(str(DEST / f"master - {N}.mp4")) as c:
        v = c.streams.video[0]
        info = {"resolucao": f"{v.width}x{v.height}", "fps": float(v.average_rate), "duracao_s": round(float(c.duration) / 1e6, 2),
                "codec": "H.264 yuv420p CRF 14", "audio": bool(c.streams.audio)}
    man = {"unidade": "yt_0011", "titulo": "Lei de Faraday e campo elétrico induzido",
           "pergunta": "Como um campo magnético cria um campo elétrico?",
           "griffiths": "7.2.1 (lei de Faraday) e 7.2.2 (campo elétrico induzido)",
           "rotulo_na_tela": "Eletromagnetismo · Indução",
           "arquivos": sorted(arquivos, key=lambda a: a["arquivo"]), "video": info}
    (DEST / f"manifesto - {N}.json").write_text(json.dumps(man, ensure_ascii=False, indent=1), encoding="utf-8")
    print("entrega em", DEST)
    print(cap)
    print(json.dumps(info, ensure_ascii=False))


if __name__ == "__main__":
    main()

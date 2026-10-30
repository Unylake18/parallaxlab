"""yt_0016 — legenda (.srt), capítulos e pasta final em entregas/Vídeos Longos/ (cópia; não move nem apaga origens).

Uso: uv run --no-sync python entregar_yt0016.py
- final/legenda - yt0016.srt: tempos do alinhamento forçado da voz com respiro (alinhamento_palavras_v6.json) + PAD (ancoras.json): o tempo
  da voz é o tempo do master. Até 2 linhas de ≤ 42 caracteres (mesma regra do yt_0014/yt_0015).
- final/capitulos - yt0016.txt: início de cada bloco = início do lote (primeira âncora); o primeiro em 00:00.
- entregas/Vídeos Longos/<pasta>/: master, legenda, capítulos, audio/, texto/, zip para o GPT e manifesto (origem, tamanho, SHA-256).
O worktree não tem entregas/: o destino é a pasta entregas/ do checkout principal.
"""
import hashlib
import json
import shutil
import textwrap
from pathlib import Path

import av

U = Path(__file__).resolve().parent
ROOT = next(p for p in (U.parents[4], U.parents[1]) if (p / "entregas").is_dir())
N = "yt0016"
DEST = ROOT / "entregas" / "Vídeos Longos" / "Mecânica - Momento - Momento em sistemas"
F = U / "final"
ANC = json.loads((U / "ancoras.json").read_text(encoding="utf-8"))
PAD = ANC["pad"]
MASTER = U / "renders" / "master_yt0016_1920x1080_30fps.mp4"


def fmt(t):
    h, r = divmod(t, 3600)
    m, s = divmod(r, 60)
    ms = int(round((s - int(s)) * 1000))
    if ms == 1000:
        s, ms = s + 1, 0
    return f"{int(h):02d}:{int(m):02d}:{int(s):02d},{ms:03d}"


def legenda():
    pal = [(w["word"].strip(), w["start"] + PAD, w["end"] + PAD) for w in
           json.loads((U / "alinhamento_palavras_v6.json").read_text(encoding="utf-8")) if w["word"].strip()]
    blocos, cur = [], []
    for p in pal:
        cur.append(p)
        t = " ".join(q[0] for q in cur)
        if p[0][-1] in ".?!:" or (p[0][-1] in ",;" and len(t) > 45) or len(t) > 64:
            blocos.append(cur)
            cur = []
    if cur:
        blocos.append(cur)
    out = []
    for i, b in enumerate(blocos, 1):
        a, f = b[0][1], b[-1][2] + 0.25
        if i < len(blocos):
            f = min(f, blocos[i][0][1] - 0.02)
        out.append(f"{i}\n{fmt(a)} --> {fmt(f)}\n" + "\n".join(textwrap.wrap(" ".join(q[0] for q in b), 42)))
    (F / f"legenda - {N}.srt").write_text("\n\n".join(out) + "\n", encoding="utf-8")
    return len(blocos)


CAP = [("H1", "Abertura: o cavalo e a pedra"), ("T7-1", "Sistemas de partículas"), ("T8-1", "Força interna não move o sistema"),
       ("T9-1", "Escolher o sistema"), ("T10-1", "Como a energia se divide"), ("E6-1", "Exercício 6: agarrar ou rebater"),
       ("E7-1", "Exercício 7: o caçador no lago"), ("E8-1", "Exercício 8: os gases do rifle"), ("E9-1", "Exercício 9: Newton e a luz"),
       ("C-1", "A luz também tem momento"), ("S1", "Resumo e o próximo vídeo")]


def capitulos():
    linhas = []
    for aid, tit in CAP:
        t = 0.0 if aid == "H1" else ANC["ancoras"][aid]["t0"]
        linhas.append(f"{int(t) // 60:02d}:{int(t) % 60:02d} {tit}")
    (F / f"capitulos - {N}.txt").write_text("\n".join(linhas) + "\n", encoding="utf-8")
    return linhas


def sha(f):
    h = hashlib.sha256()
    with open(f, "rb") as fh:
        for b in iter(lambda: fh.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def main():
    F.mkdir(exist_ok=True)
    nleg, caps = legenda(), capitulos()
    (DEST / "audio").mkdir(parents=True, exist_ok=True)
    (DEST / "texto").mkdir(parents=True, exist_ok=True)
    cop = [
        (MASTER, f"master - {N}.mp4"),
        (F / f"legenda - {N}.srt", f"legenda - {N}.srt"),
        (F / f"capitulos - {N}.txt", f"capitulos - {N}.txt"),
        (U / "renders" / "final_para_gpt.zip", f"quadros_e_video_para_gpt - {N}.zip"),
        (U / "audio" / "narracao_v4_pausas.wav", f"audio/narracao - {N}.wav"),
        (U / "ficha.md", f"texto/ficha - {N}.md"),
        (U / "narracao_final_v4.md", f"texto/narracao - {N}.md"),
        (U / "narracao_tags.md", f"texto/narracao_tags - {N}.md"),
        (U / "handoff_v7.md", f"texto/handoff_v7 - {N}.md"),
    ]
    arquivos = []
    for o, d in cop:
        if not o.exists():
            print("faltando:", o)
            continue
        shutil.copy2(o, DEST / d)
        arquivos.append({"arquivo": d.replace("/", "\\"), "origem": str(o), "bytes": (DEST / d).stat().st_size, "sha256": sha(DEST / d)})
    with av.open(str(DEST / f"master - {N}.mp4")) as c:
        v = c.streams.video[0]
        info = {"resolucao": f"{v.width}x{v.height}", "fps": float(v.average_rate), "duracao_s": round(float(c.duration) / 1e6, 2),
                "codec": "H.264 yuv420p CRF 14", "audio": bool(c.streams.audio), "audio_codec": "AAC 192 kb/s (pico da voz −1,0 dBFS)"}
    man = {"unidade": "yt_0016", "titulo": "Momento em sistemas", "pergunta": "O que muda o momento de vários corpos?",
           "rotulo_na_tela": "Mecânica · Momento em sistemas", "parte": "2 de 2 do 4.9 (a parte 1 é o yt_0015)",
           "sincronia": f"{len(ANC['ordem'])} âncoras (ancoras.json), alinhamento forçado ElevenLabs, voz com respiro (pausas_v6.py)",
           "arquivos": sorted(arquivos, key=lambda a: a["arquivo"]), "video": info}
    (DEST / f"manifesto - {N}.json").write_text(json.dumps(man, ensure_ascii=False, indent=1), encoding="utf-8")
    print("entrega em", DEST)
    print(f"{nleg} legendas; {len(caps)} capítulos")
    print("\n".join(caps))
    print(json.dumps(info, ensure_ascii=False))


if __name__ == "__main__":
    main()

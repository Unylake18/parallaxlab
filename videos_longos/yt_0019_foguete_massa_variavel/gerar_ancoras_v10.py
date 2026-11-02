"""yt_0019 v10: grava ancoras.json a partir da VOZ CONTÍNUA (audio/voz10_tempos.json, do unir_voz.py).

Sem folga inventada e sem pausa colada: a janela de uma âncora vai do começo da sua primeira palavra MENOS 0,15 s (LEAD, padrão do yt_0010) até o
começo da primeira palavra da âncora seguinte menos 0,15 s. As pausas dentro da janela são as da própria voz. Os instantes são do WAV final
(o vídeo começa junto com o WAV) e ficam em múltiplos de 1/15 s, para a cena fechar cada âncora no mesmo quadro em que a voz abre a seguinte.
Por âncora: `ini` (s, absoluto), `dur` (janela), `t`/`e` (início e fim de cada palavra desde `ini`), `fala` (palavras minúsculas), `nominal` (janela do v5).
uso: python gerar_ancoras.py"""
import json
import re
from pathlib import Path

AQUI = Path(__file__).resolve().parent
LEAD, FPS, CAUDA = 0.15, 15, 5.5
nom = json.loads((AQUI / "ancoras_nominal_v10.json").read_text(encoding="utf-8"))
ordem = nom["ordem"]
V = json.loads((AQUI / "audio" / "voz10_tempos.json").read_text(encoding="utf-8"))
tempos = V["ancoras"]


def toks(s):
    return re.findall(r"\w+", s.lower())


q = lambda x: round(x * FPS) / FPS
ini = {}
for k, aid in enumerate(ordem):
    ini[aid] = 0.0 if k == 0 else q(max(0.0, tempos[aid][0]["t"] - LEAD))
fim_video = q(V["duracao"] + CAUDA - 0.3)
out = {}
for k, aid in enumerate(ordem):
    pal = tempos[aid]
    fim = ini[ordem[k + 1]] if k + 1 < len(ordem) else fim_video
    ws = [toks(p["w"])[0] if toks(p["w"]) else p["w"].lower() for p in pal]
    out[aid] = {"palavras": len(pal), "ini": round(ini[aid], 4), "fim": round(fim, 4), "dur": round(fim - ini[aid], 4), "fala": " ".join(ws),
                "t": [round(p["t"] - ini[aid], 3) for p in pal], "e": [round(p["e"] - ini[aid], 3) for p in pal], "nominal": nom["ancoras"][aid]["dur"]}
(AQUI / "ancoras.json").write_text(json.dumps({"ordem": ordem, "ancoras": out, "video_s": fim_video, "voz_s": V["duracao"]}, ensure_ascii=False, indent=1), encoding="utf-8")
tot = sum(v["dur"] for v in out.values())
print(f"{len(out)} âncoras; vídeo {tot / 60:.2f} min ({tot:.1f} s); voz {V['duracao']:.1f} s; nominal v5 {sum(v['nominal'] for v in out.values()) / 60:.2f} min")
for aid in ordem:
    v = out[aid]
    r = v["dur"] / v["nominal"]
    print(f"{aid:6s} ini {v['ini']:7.2f}  janela {v['dur']:6.2f} s (nominal {v['nominal']:6.2f}, x{r:.2f})  {v['palavras']:3d} pal")

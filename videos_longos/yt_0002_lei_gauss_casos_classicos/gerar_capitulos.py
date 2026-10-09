"""yt_0002 — capítulos do YouTube a partir de blocos.json (instantes de início de cada bloco no vídeo final).

    uv run --no-sync python videos_longos/yt_0002_lei_gauss_casos_classicos/gerar_capitulos.py   →   capitulos_youtube.txt
"""

import json
from pathlib import Path

PASTA = Path(__file__).resolve().parent
TITULOS = {
    1: "Três perfis, uma só Lei de Gauss",
    3: "O método: simetria, superfície, carga envolvida",
    4: "Linha infinita: a simetria do campo",
    7: "Casca cilíndrica",
    8: "Cilindro maciço: o campo cresce por dentro",
    10: "Cabo coaxial: campo preso no vão",
    12: "Folha infinita e o fator dois",
    13: "Placa com espessura (slab)",
    14: "Duas chapas: o capacitor plano",
    15: "Face de condutor",
    20: "Casca esférica",
    22: "Esfera maciça e comparação com o cilindro",
    23: "Capacitor esférico",
    24: "Três capacitores, uma lei",
    26: "Checklist: seis perguntas antes da integral",
    27: "Conclusão",
}


def ts(t):
    t = int(t)
    return f"{t // 60:02d}:{t % 60:02d}" if t < 3600 else f"{t // 3600:d}:{t % 3600 // 60:02d}:{t % 60:02d}"


def main():
    b = json.loads((PASTA / "blocos.json").read_text(encoding="utf-8"))
    linhas = [f"{ts(0 if k == 1 else b[str(k)])} {t}" for k, t in TITULOS.items()]
    (PASTA / "capitulos_youtube.txt").write_text("\n".join(linhas) + "\n", encoding="utf-8")
    print("\n".join(linhas))


if __name__ == "__main__":
    main()

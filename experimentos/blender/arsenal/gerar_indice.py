"""Gera indice_producao.md: índice enxuto do arsenal para quem escreve briefings (chat de Produção). Python puro.

    python experimentos/blender/arsenal/gerar_indice.py

Uma linha por sólido, na ordem curricular de `gerar_cobertura.CAPITULOS` (um sólido que serve a vários capítulos aparece
completo na primeira vez e só como remissão nas outras). O texto vem das fichas: rode de novo depois de criar ou editar sólidos.
"""

import json
import re
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
from gerar_cobertura import CAPITULOS, LACUNAS, ler_fichas  # noqa: E402


def primeira_frase(txt, limite):
    txt = re.sub(r"\s+", " ", txt).strip()
    m = re.match(r"(.+?[.:;])(\s|$)", txt)
    s = m.group(1) if m else txt
    s = s.rstrip(".:;")
    return s if len(s) <= limite else s[: limite - 1].rsplit(" ", 1)[0] + "…"


def movimento(f):
    a = f.get("animacao")
    return "—" if not a else ("único" if a.get("ciclo") == "unico" else "loop")


def main():
    fichas = ler_fichas()
    visto = set()
    linhas = []
    for cap, titulo, ids, nota in CAPITULOS:
        linhas += [f"### {cap} — {titulo}" + (f" ({nota})" if nota else ""), "", "| id | mostra | mov. | não usar quando |", "|---|---|---|---|"]
        for i in ids:
            f = fichas[i]
            if i in visto:
                linhas.append(f"| `{i}` | (ver acima) | {movimento(f)} | |")
                continue
            visto.add(i)
            nao = primeira_frase(f["nao_usar_quando"][0], 90) if f.get("nao_usar_quando") else ""
            linhas.append(f"| `{i}` | {primeira_frase(f['leitura_visual'], 150)} | {movimento(f)} | {nao} |")
        linhas.append("")
    manim = [l for l in LACUNAS if l[3] == "Manim"]
    texto = f"""# Arsenal 3D — índice enxuto para briefings

> Arquivo **gerado** por `gerar_indice.py` (não editar à mão). **{len(fichas)} sólidos**, todos `aprovado`
> ({sum(1 for f in fichas.values() if f['status'] != 'aprovado')} em outro status); versão completa em `catalogo.md`, cobertura em `cobertura.md`.

## Como usar num briefing

- Preencha `solido_3d:` com um `id` desta lista ou `nenhum` + motivo, e diga **o que o 3D deve mostrar e em que ponto do storyboard entra**.
- O 3D só dá a **geometria**: valores, fórmulas, rótulos, sinais e setas de sentido são do Manim. Gramática de cor fixa: campo elétrico = ciano,
  campo magnético = magenta, vetores físicos = branco, construções matemáticas = violeta tracejado, superfícies/corpos = vidro azul.
- Movimento: **loop** = fase 0–1 se repete sem emenda; **único** = ciclo que termina num estado diferente (congela no fim); **—** = estático.
- Cada sólido tem parâmetros (tamanho, quantidade, estado) na ficha `solidos/<id>.json`; quem implementa vê o sólido com `abrir/<id>.bat`.
- Um sólido só entra num vídeo com `solido_3d:` no briefing; quem implementa avalia o encaixe e devolve o relatório "Teste do arsenal" (`docs/formatos.md`).

## Sólidos por capítulo do mapa curricular

{chr(10).join(linhas)}
## Sem sólido 3D (melhor no Manim)

{chr(10).join(f"- **{l[0]}** {l[1]}: {l[4]}" for l in manim)}
"""
    (AQUI / "indice_producao.md").write_text(texto, encoding="utf-8", newline="\n")
    n = len((AQUI / "indice_producao.md").read_bytes())
    print(f"OK: indice_producao.md ({len(visto)} sólidos, {n/1024:.1f} KB)")


if __name__ == "__main__":
    main()

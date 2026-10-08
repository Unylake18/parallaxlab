# Preview padronizado dos casos de Gauss (Blender + Manim)

Experimento paralelo, fora do `yt_0002` (nada do vídeo principal foi alterado). Aplica o padrão do coaxial v2 aos casos de Gauss:
geometria no Blender, leitura física (região, Q_env, E, nota, gráfico, corte 2D) no Manim, tudo ligado ao mesmo parâmetro `p`.

**Vídeo:** `saida/PreviewGaussPadronizado_540p15.mp4` (90,5 s, 960×540, 15 fps; 11 casos + abertura e fecho).

## Como renderizar (a partir da raiz do repositório)

1. Validar só 3 estados por caso (poucos segundos): `blender.exe -b -P experimentos\blender\preview_gauss_padronizado\render_casos.py -- --caso todos --estados`
2. Sequências (11 casos, ~4,5 min no total, ~0,65 s/quadro, 208 MB em `renders/preview_gauss_padronizado/`, ignorado pelo Git):
   `blender.exe -b -P experimentos\blender\preview_gauss_padronizado\render_casos.py -- --caso todos`  (ou `--caso coax,folha`)
3. Preview: `uv run python -m manim -r 960,540 --fps 15 --media_dir media/preview_gauss_padronizado experimentos/blender/preview_gauss_padronizado/cena_preview.py PreviewGaussPadronizado`

Arquivos: `casos.py` (parâmetros por caso, lido pelos dois lados), `render_casos.py` (Blender), `cena_preview.py` (Manim). Dependem de
`../teste_gauss_coaxial/` (v1 e v2 do coaxial, intactos) e dos construtores do arsenal (importados, não alterados).

## Casos e reaproveitamento

| Caso | p varia | 3D |
|---|---|---|
| linha infinita | r da gaussiana | fio fino novo + gaussiana cilíndrica da v2 |
| casca cilíndrica | r | casca com corte da v2 (geometria nova), cargas na face externa |
| cilindro maciço | r | `criar_corpo_macico` + `material_vidro` + `pontos_no_volume` (arsenal) |
| cabo coaxial | r | v2 inteira (núcleo sólido, casca com corte, holofote) |
| folha infinita | x das tampas | `criar_placa_carregada` (arsenal) + pillbox novo |
| placa com espessura | x das tampas | bloco de vidro novo (`material_vidro`) + pillbox |
| duas folhas | tampa direita | duas `criar_placa_carregada` + pillbox |
| face de condutor | tampa de fora | bloco de metal (v2) + pillbox atravessando a superfície |
| casca esférica | r | `criar_casca_esferica` + `material_casca` (arsenal) |
| esfera maciça | r | `criar_esfera_macica` (arsenal) |
| capacitor esférico | r | `criar_capacitor_esferico` (arsenal), cargas reclassificadas |
| comparativo final | — | três quadros das sequências, montados no Manim |

## Melhorias do coaxial aplicadas

Câmera ortográfica fixa; carga + azul e − magenta (cor de apoio da paleta); cargas só na superfície ou no volume do material; gaussiana
"fantasma" (vidro violeta, tampas contínuas, arestas laterais tracejadas); carga envolvida em violeta claro; setas de E só onde o campo
existe, com comprimento coerente com o gráfico; corte 2D (radial ou lateral) e gráfico com marcador sincronizados; legenda de cores.

## Limitações

- Holofote por região (brilho/opacidade) só no coaxial; nos demais, o destaque é a carga envolvida e as setas.
- Linha e folha ficam pequenas no painel (a gaussiana máxima define o enquadramento); a folha/placa fina some nas bordas por design.
- Face de condutor e placa usam blocos finitos (a "infinitude" é só dita no texto); setas de campo são poucas e fixas por caso.
- Quadro comparativo final é simples (3 miniaturas); sem 1080p; sem áudio; não verificado em reprodução contínua.

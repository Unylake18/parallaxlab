# QA — preview silencioso do vid_0015

Concluído em 2026-10-06, exclusivamente na fase de preview.

## Arquivos e validação

- Implementação: `cena.py`, classe `LinhasCarga015`.
- Briefing aprovado registrado em `ficha.md`.
- Inspeção reproduzível: `inspecionar_preview.py`.
- Timestamps: `qa_estados.json`; medidas do MP4: `qa_tecnico.json`.
- Quadros: `frames_preview/`, 32 PNGs e quatro folhas de contato.
- Log do render concluído: `render_preview.log`.
- Preview: `media/videos/cena/960p15/vid_0015_preview_silencioso.mp4`.

Comandos executados no ambiente validado:

```powershell
uv run --no-sync python -m py_compile videos/vid_0015_linhas_carga_movimento/cena.py
uv run --no-sync python -m manim -r 540,960 --fps 15 --media_dir videos/vid_0015_linhas_carga_movimento/media -o vid_0015_preview_silencioso videos/vid_0015_linhas_carga_movimento/cena.py LinhasCarga015
uv run --no-sync python videos/vid_0015_linhas_carga_movimento/inspecionar_preview.py
```

Todos concluídos com código de saída 0 na versão entregue. O render foi executado
com redirecionamento de saída para `render_preview.log` nas iterações de correção.
O acesso ao runtime instalado exigiu execução fora do sandbox; nenhuma dependência
ou configuração global foi alterada.

## Resultado técnico

540×960, H.264, 15 fps nominal, **158,930 s** (2 min 38,93 s), **2.384 quadros**,
zero streams de áudio. O MP4 inteiro foi decodificado sem erro.

A média calculada pelo container é 15,000307 fps: os PTS dos trechos concatenados
pelo Manim têm arredondamento inferior a 1 ms nas fronteiras. A taxa nominal e a
taxa inferida pelo decoder são 15 fps; os intervalos entre quadros estão entre
0,066341 e 0,066667 s. `qa_tecnico.json` conserva as medidas exatas.

## Conferência visual e física

Os 32 estados marcados foram extraídos e inspecionados em folhas de contato.
Os estados mais densos e os trechos corrigidos também foram vistos em 540×960.

| Estado obrigatório | Quadros de referência |
| --- | --- |
| Enunciado com duas linhas, λ, d, v | 01, cerca de 4,4 s |
| Gauss e fluxo zero individual nas tampas | 07, cerca de 30,9 s |
| Corte do cilindro e transição para curva de Ampère | 11–12, cerca de 50,3–56,9 s |
| Regra da mão direita e campo entrando na tela | 13, cerca de 62,7 s |
| Produto vetorial e forças opostas | 16–18, cerca de 76,1–86,3 s |
| Condição \|I\|/\|λ\| = c, antes da relação com v | 22, cerca de 104,5 s |
| Retorno ao enunciado, \|I\| = \|λ\|v e v = c | 23–25, cerca de 112,1–122,9 s |
| Exploração ideal e razão final menor que 1 | 26–32, cerca de 130,3–156,0 s |

- E radial, apontando para fora na representação de cargas positivas.
- dA axial nas tampas superior e inferior, em sentidos opostos; E perpendicular
  a dA em ambas. Cada tampa tem fluxo zero, individualmente.
- Gauss identificado como superfície fechada; Ampère como curva fechada.
- A integral de B é identificada como circulação, sem “fluxo magnético”.
- I para cima na linha 1 produz B entrando na tela à direita (⊗).
- +ŷ × (−ẑ) = −x̂, com F_B sobre a linha 2 apontando para a linha 1.
- F_E aponta para a direita; F_B aponta para a esquerda. Na hipótese de igualdade,
  os comprimentos das duas setas também ficam iguais.
- Campos calculados a partir da linha 1 e forças avaliadas sobre a linha 2.
- Cancelamento explícito dos quatro termos comuns: dois 2π e dois d.
- Pausa em \|I\|/\|λ\| = c antes de apresentar \|I\| = \|λ\|v.
- v = c aparece somente após a volta visual às setas v do enunciado.
- O texto aprovado sobre a corrente produzida pela própria linha em movimento
  aparece no retorno ao enunciado.
- “MODELO IDEAL” permanece visível durante toda a exploração e o fechamento.
  A tela também explica que v/c é um parâmetro do modelo, sem acelerar elétrons
  de um fio real.
- Exploração em v/c = 0,200; 0,600; 0,850; 0,970; 0,995. A seta elétrica tem
  comprimento 2,2 e a magnética 2,2(v/c)²; a interpolação fica nesse intervalo.
  Portanto a magnética nunca alcança nem ultrapassa a elétrica para v < c.
- Limite de partículas massivas v < c e fechamento com F_B/F_E = v²/c² < 1
  e seta de repulsão líquida.

## Correções e pendências

Corrigidos durante o QA: compatibilidade com a API MathTex do Manim 0.21;
dois glifos ausentes na fonte dos textos; acento no modo matemático do rótulo
“líquida”; comprimentos das setas na hipótese de equilíbrio.

Nenhuma inconsistência no briefing nem pendência técnica identificada nos
estados inspecionados. Voz, SRT, master, legendado, capa e render final não fazem
parte desta rodada. Nenhum arquivo global ou de outro vídeo foi alterado.

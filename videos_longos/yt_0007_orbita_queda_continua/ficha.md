# Por que uma órbita é uma queda que nunca termina?

- id: `yt_0007`
- formato: `longo_horizontal`
- natureza: `teoria_visual`
- curso/eixo: Física I
- macroassunto: Mecânica
- módulo: Gravitação
- solido_3d: `nenhum` — volume e projeção espacial procedurais no próprio Manim, sincronizados ao estado SI; sem integração Blender ou sólido externo.
- fase: **preview de acabamento N01–N18 concluído para revisão editorial**, preservando a base visual e os previews anteriores. Sem voz, SRT, master, capa ou publicação.
- preview: 960×540, 15 fps, frame lógico 16×9.
- classe: `OrbitaQuedaContinua007`.

## Especificação de implementação

Briefing recebido em 18/10/2026. Sequência: N01 canhão → N02 queda contínua → N03 contrafactual → N04 rotação de v → N05 aceleração circular → N06 velocidade orbital → N07 queda local a 400 km → N08 interpretação → N09 microgravidade → N10 raio e velocidade → N11 período circular → N12 generalização elíptica → N13 parâmetro inicial → N14 impacto e continuação matemática → N15 Newton → N16 pedra/satélite/Lua → N17 baricentro → N18 fechamento.

Física em SI: `R_T=6.371e6 m`, `MU=3.986004418e14 m³/s²`; Terra esférica, sem atmosfera/rotação, massa de teste desprezível, gravitação newtoniana. Terra fixa em N01–N16, exceto a antecipação esquemática do ponto comum no sistema Terra–Lua em N16. N17 explicita o movimento de ambos.

Velocity-Verlet, passo padrão de 1 s; impacto refinado por bisseção do último passo. Cônicas analíticas na experiência paramétrica de N13 e continuação de N14. Energia ligada/aberta e colisão são propriedades independentes. Zoom gráfico não entra no modelo físico.

N07/N08: tempo físico de 1 s mostrado em câmera lenta; escalas horizontal/vertical diferentes, com os dois avisos obrigatórios em tela. N09 avisa a ampliação de altitude/separação na órbita de 400 km. N10 é comparação de uma família de órbitas circulares, não uma manobra física de transferência. N17: distâncias da visão geral em escala, marcador lunar ampliado com aviso, e ampliação local com a mesma escala para raio terrestre e distância ao baricentro.

## Execução

```powershell
uv run --no-sync python videos_longos/yt_0007_orbita_queda_continua/modelo_orbital.py
uv run --no-sync python -m manim -r 960,540 --fps 15 --media_dir videos_longos/yt_0007_orbita_queda_continua/media_acabamento videos_longos/yt_0007_orbita_queda_continua/cena.py OrbitaQuedaContinua007
```

`SO=7,8` no ambiente seleciona apenas esses blocos para depuração. Os JSONs de timing registram tempos reais do preview, sem pretensão de sincronização com voz.

## Teste do arsenal

Nenhum sólido Blender, conforme briefing explícito. Resolução de preview: 960×540/15 fps. Sem geração de sequências ou integração Blender. Nesta rodada, a esfera é amostrada no recorte visível à resolução da saída, com dois recortes RGBA em cache e contorno vetorial. O mesmo material e iluminação servem ao globo e ao horizonte; o detalhe geográfico é reduzido gradualmente. Teste curto também em 1920×1080/15 fps. Física e câmera permanecem independentes; custo medido em `validacao_acabamento.json`.

## Repaginação autorizada — 18/10/2026

Fonte: `proposta_repagina_aprovada.md`, copiada da revisão do Work, e confirmação explícita do usuário para reconstruir N01–N18 e renderizar outro preview silencioso. Decisões confirmadas: retirar NN/18; cabeçalho `GRAVITAÇÃO — ÓRBITAS`; marca no alto à direita, largura 1,92/opacidade 0,45/margem 0,30 como Gauss.

O modelo SI, constantes, impactos e sequência conceitual permanecem. `cena_v1.py` preserva a implementação anterior. A nova entrada `cena.py` usa `encenacao.py` e `geometria_visual.py`, somente nesta unidade. Câmera, relevo, esfera, trajetória, partículas e vetores compartilham a projeção; a superfície não gira fisicamente. N07/N08 aproximam e devolvem o mesmo detalhe com ampliação radial avisada. N10 compara duas condições circulares independentes num tempo comum; N13 ajusta e executa lançamentos, com reinício explícito entre condições. O fechamento reencontra a montanha.

`QUADROS=1` captura os marcos de composição sem renderizar intervalos de tempo. `SO=1,7,8` mantém as dependências anteriores em execução sem quadros e renderiza apenas os blocos selecionados. Saídas da reconstrução: `media_repagina/`, `qa_repagina_estatico/`, `timing_repagina*.json`; o vídeo e o ZIP anteriores continuam preservados.

## Acabamento implementado

Fonte: `reavaliacao_acabamento.md`, recebida após a avaliação do pacote anterior. Escopo: nitidez da Terra dentro do Manim, reconhecimento e chamadas do canhão/pedra, encadeamento de força/aceleração/condição circular, MF-Tools nos cancelamentos e no período, Lua e baricentro identificados em sequência, títulos ligados ao fenômeno e paleta central sem amarelo. Tempo/período usam magenta; distâncias usam violeta; `M` e Terra usam azul; gravidade usa ciano; massa de teste, velocidade, operadores e unidades usam branco.

Implementação local em `encenacao.py`, `geometria_visual.py`, `superficie.py`, `matematica_visual.py`, `cadeia_equacoes.py` e `sistema_lunar.py`. Modelo SI e casos de lançamento preservados. Cópias do código da rodada anterior: `encenacao_repagina_v2.py` e `geometria_repagina_v2.py`.

Preview atual: `media_acabamento/preview_acabamento_0007_960x540_15fps.mp4`, **488,1333 s (8min08,1s), 7.322 quadros**, 960×540/15 fps, H.264/yuv420p, CRF 23 de preview, sem áudio. Render completo e revisões locais montados sem recompressão; tempos em `timing_acabamento.json` e proveniência em `montagem_acabamento.json`.

Física, densidade de superfície, continuidade e validação técnica aprovadas. QA do MP4: 68 quadros de marcos/finais, 12 pranchas, 216 amostras temporais e 18 pranchas de movimento, inspecionadas. Auditoria dos 7.322 frames sem amarelo encontrado na amostragem espacial fora da marca. Prova curta de definição também em 1080p. Relatório: `qa_acabamento.md`; pacote: `avaliacao_acabamento_visual_0007.zip`. A unidade inteira permanece em preview 540p e aguarda revisão artística.

## Preview repaginado anterior — preservado

`media_repagina/preview_repagina_0007_960x540_15fps.mp4`: 433,7333 s (7min13,7s), 6.506 quadros, H.264/yuv420p, 15 fps, sem áudio, CRF 23 de preview 540p. Timestamps regularizados e relógios N10/N11 revisados sem recomprimir os demais blocos.

QA em `qa_repagina/`: 58 quadros de marcos/finais e 10 pranchas; `qa_repagina/movimento/`: 216 amostras e 18 pranchas temporais. Relatório em `qa_repagina.md`; pacote em `avaliacao_repagina_visual_0007.zip`. A aprovação artística permanece com o usuário.

## Arquivo da primeira versão — validação técnica e QA anteriores

Concluído em 18/10/2026, com identificação definitiva **yt_0007** solicitada pelo usuário durante esta rodada.

- Preview completo de referência: `media_preview/preview_completo_0007_960x540_15fps.mp4`.
- Duração: **386,6667 s (6min26,7s)**, 5.800 quadros, 960×540/15 fps, H.264/yuv420p, CRF 14, nenhuma faixa de áudio; 5.917.946 bytes.
- Física/asserts, `py_compile`, import e renders: aprovados. Também verificados 181 estados intermediários da experiência paramétrica.
- QA: 42 quadros extraídos do preview completo, incluindo finais dos 18 blocos e todos os marcos solicitados; pranchas e PNGs em `qa_preview/`.
- Valores e deriva numérica: `validacao_fisica.json`.
- Tempos do arquivo entregue: `timing_preview_revisado.json`. `timing_preview.json` registra o primeiro render completo e não deve ser usado para localizar os trechos no arquivo revisto.
- Relatório de implementação, verificações e limites: `qa_visual.md`.

Somente blocos afetados foram renderizados novamente. `revisar_preview.py` reuniu as revisões de N01/N03/N09/N13/N15/N17/N18 com os demais trechos do render completo, preservando os 18 blocos. As saídas de blocos revistos usam corte editorial para evitar reaparecer um quadro antigo durante o fade de saída.

Não há pendências dentro do escopo visual desta rodada. O ritmo é editorial e silencioso, sem sincronização com uma narração futura. Nenhuma etapa posterior de produção foi aberta.

# Entrega do preview visual — yt_0007

18/10/2026. **N01–N18 implementadas e conferidas.** Identificação definitiva: `yt_0007_orbita_queda_continua`; classe `OrbitaQuedaContinua007`. O ID 0007 estava livre. Todo trabalho desta rodada ficou nesta unidade; alterações preexistentes de outras unidades e dos documentos globais foram preservadas.

## Arquivos

- `cena.py`: sequência visual completa, projeção independente do SI, fontes/helpers horizontais existentes, seleção local por `SO` e marcos de timing.
- `modelo_orbital.py`: gravitação em SI, velocity-Verlet, impacto por bisseção, cônicas analíticas e asserts físicos.
- `ficha.md`: identificação, hipóteses, fase e registro da entrega.
- `quadros_estaticos.py`: depuração local de composições sem renderizar os intervalos de tempo.
- `verificar_preview.py`: inspeção técnica, extração de quadros e pranchas de QA.
- `revisar_preview.py`: substituição somente dos blocos revistos, mantendo os demais renders.
- `.gitignore`: saídas e caches locais, sem alteração do arquivo global.
- Relatórios gerados: `validacao_fisica.json`, `timing_preview.json`, `timing_preview_revisado.json`, `timing_parcial_*.json`, este relatório e `qa_preview/tecnico.json`.

## Verificações

`py_compile` dos cinco arquivos Python: aprovado. Import localizado, registro das fontes e `MathTex`: aprovados no ambiente existente. O registro de fontes falhou no sandbox; os renders foram executados fora dele com as fontes já existentes, sem instalar ou atualizar dependências.

| Verificação física | Resultado |
| --- | --- |
| Velocidade circular a 400 km | 7.672,598648 m/s |
| Gravidade a 400 km | 8,694250483 m/s² |
| Período a 400 km | 92,41425160 min |
| Queda local em 1 s | 4,347125241 m |
| Queda exata da circunferência | 4,347124776 m |
| Diferença entre aproximação e circunferência | 4,6536 × 10⁻⁷ m |
| Deriva relativa máxima de raio, uma volta | 6,4202 × 10⁻⁷ |
| Deriva relativa máxima de energia, uma volta | 4,0701 × 10⁻¹³ |
| Impactos de N01 | 13,099°; 26,705°; 162,773° após o lançamento |
| Estado circular de N01 | uma volta sem impacto |
| Impacto de N14 | primeiro cruzamento em R_T; erro numérico de localização < 10⁻⁵ m |
| Estados de N13 | energia ligada/aberta e colisão verificadas separadamente |
| 181 valores intermediários de N13 | curvas finitas, limitadas à janela gráfica, sem atravessamento físico da superfície |

Não há correção artificial de raio/energia. Passo padrão do integrador: 1 s; a queda local da pedra em N16 usa 0,01 s. N13 usa previsão analítica, como autorizado; N14 integra a trajetória física e separa a continuação analítica.

## Renders e QA visual

Render completo silencioso: `uv run --no-sync python -m manim -r 960,540 --fps 15 ...`. Revisões locais: `SO=3,9,13,18` (intermediário), `SO=1,3,9,13,15,18`, `SO=9` e `SO=17`, cada uma em sua saída local. Nenhum bloco não afetado foi renderizado novamente. O preview completo entregue usa o render inicial e as revisões mais recentes; sua proveniência por segmento está em `timing_preview_revisado.json`.

42 quadros foram extraídos do arquivo entregue e inspecionados, incluindo o final de cada bloco e os marcos abaixo. As pranchas têm cabeçalhos de QA externos ao vídeo; o produto não contém esses cabeçalhos, guias ou índices de desenvolvimento.

| Ponto solicitado | Conferência |
| --- | --- |
| N01 | lançamentos sequenciais, abertura da câmera, impactos na superfície, terceiro próximo do lado oposto, órbita circular; somente os traços anteriores são atenuados |
| N04 | vetores copiados à origem comum, Δv ≈ a Δt para intervalo finito, diferencial separado |
| N06 | transformação até a raiz, uma seta de gravidade e vetor de velocidade; papel centrípeto sem força adicional |
| N07 | mudança explícita para 400 km, avisos de aproximação e ampliação, 7,67 km/4,35 m e equação legíveis |
| N09 | acelerações quase iguais, queda conjunta, gravidade presente, comparação com normal; vetores ligados aos corpos e rótulos afastados do chão |
| N11 → N12 | encerramento do círculo, transição conceitual, nova elipse em foco, semieixo a e generalização sem derivação |
| N13 | mesmo ponto inicial, um parâmetro para vetor/curva/rótulo, estados ligados com e sem colisão, classificação aberta por energia |
| N14 | satélite para no impacto; continuação interna exclusivamente violeta tracejada e identificada |
| N17 | Lua visível e ampliação avisada; distâncias preservadas; ampliação terrestre mostra baricentro a 0,733 R_T, dentro da Terra |
| N18 | retomada de pedra/satélite/Lua, duas frases finais, remoção de overlays, Terra/satélite/trajetória no encerramento |
| Geral | área inferior reservada, matemática legível em 960×540, paleta semântica e branding existentes, nenhum debug ou índice de glyph |

## Artefato de referência

`media_preview/preview_completo_0007_960x540_15fps.mp4`

**386,6667 s · 5.800 quadros · 960×540 · 15 fps · H.264 · yuv420p · CRF 14,0 · sem áudio · 5.917.946 bytes.**

Checagem do vídeo e decodificação para extrair os 42 quadros: aprovadas. Cada segmento reconformado foi conferido por contagem de quadros. `qa_preview/tecnico.json` registra os metadados; `qa_preview/` contém PNGs em resolução nativa e sete pranchas. Os tempos corretos do preview entregue estão em `timing_preview_revisado.json`.

## Teste do arsenal e limites

Sólido usado: **nenhum**, conforme briefing justificado. Resolução: 960×540/15 fps. Custo/peso de 3D: zero. O modelo 2D permitiu sincronizar trajetória, vetores, parâmetros e projeção; nenhum ajuste ao arsenal foi necessário.

Sem pendências dentro desta rodada. O preview usa tempo comprimido nas órbitas e ampliações avisadas nas construções locais; não representa duração orbital em tempo real. O ritmo permanece editorial, sem sincronização com voz. Não foram criados voz, SRT, master, capa ou publicação; não houve commit, branch, PR ou push.

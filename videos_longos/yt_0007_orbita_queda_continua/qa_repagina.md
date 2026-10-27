# Longo 0007 — repaginação visual N01–N18

Preview silencioso reconstruído conforme `proposta_repagina_aprovada.md` e autorização explícita do usuário. A retirada do contador foi confirmada; o cabeçalho é **GRAVITAÇÃO — ÓRBITAS**, com marca oficial no alto à direita no tamanho/opacidade usados em Gauss.

## Entrega

- Vídeo completo: `media_repagina/preview_repagina_0007_960x540_15fps.mp4`.
- Duração: **433,7333 s (7min13,7s)**; **6.506 quadros**, 960×540, 15 fps exatos, H.264/yuv420p, sem áudio.
- CRF 23, conforme o padrão de preview 540p do repositório. A regularização dos timestamps e a substituição dos relógios copiam os pacotes H.264, sem recompressão.
- `qa_repagina/`: **58 PNGs de avaliação**, com todos os marcos e um estado próximo ao fim de cada bloco, e **10 pranchas**. Os marcos são capturados depois de a ação terminar, para registrar corretamente as classificações circular/aberta.
- `qa_repagina/movimento/`: **216 PNGs**, 12 instantes por bloco, e **18 pranchas temporais**.
- `timing_repagina.json`: tempos efetivos dos 18 blocos e seus marcos.
- `avaliacao_repagina_visual_0007.zip`: vídeo, todos os quadros de avaliação e amostras acima, pranchas, proposta, ficha, validação e relatório; manifesto SHA-256 e verificação de integridade ZIP.

Os PNGs são uma seleção para avaliação visual. Os 6.506 frames completos estão no MP4. A versão anterior, seus quadros e seu ZIP continuam preservados.

## Encenação implementada

N01 começa no relevo, plataforma, canhão e pedra. Os lançamentos abrem o plano de acordo com o alcance e terminam na vista orbital. A esfera tem iluminação fixa, relevo gráfico, grade superficial e oclusão; câmera e objetos usam a mesma projeção, separada do estado físico em SI.

N02–N06 conservam o corpo e a órbita entre força, contrafactual, rotação da velocidade, raio e dedução da velocidade circular. N06 explicita a fatoração e o cancelamento com `TransformByGlyphMap`; as demais transformações usam `TransformMatchingTex` quando a correspondência é adequada.

N07 amplia um trecho da própria órbita, avisa a ampliação radial e as escalas diferentes, mostra 1 s físico em câmera lenta e relaciona 7,67 km na tangente com 4,35 m de queda. N08 devolve o detalhe ao planeta. A curva local recebeu amostras densas dos dois lados do ponto inicial, eliminando uma corda espúria no zoom.

N09 acompanha a estação, aproxima o exterior e revela cabine, astronauta e objeto solto, antes da explicação da queda conjunta e da comparação com apoio. N10 executa dois casos circulares independentes num relógio comum; N11 acompanha uma volta e desenvolve o período. N12 apresenta uma nova órbita elíptica, foco e semieixo.

N13 alterna ajuste de um único parâmetro com cinco lançamentos físicos, incluindo impacto, órbita ligada sem impacto, circular, elíptica e aberta. Os reinícios são explícitos. N14 para no primeiro impacto e distingue a continuação matemática tracejada. N15 retorna ao diagrama de Newton. N16 muda explicitamente de escala e sistema entre pedra, satélite e Lua. N17 liga a visão oblíqua do sistema à ampliação perpendicular do baricentro, com `r_b/R_T ≈ 0,733`. N18 reencontra a montanha e executa o lançamento do fechamento.

## Verificações

- `py_compile`: código de encenação, geometria e utilitários compilados.
- `validar_repagina.py`: asserts físicos e de projeção aprovados; valores e resultados em `validacao_repagina.json`.
- Referências a 400 km: `v=7672,5986 m/s`, `g=8,6942505 m/s²`, `T=92,41425 min`; queda em 1 s `4,347125 m`. Diferença entre aproximação local e círculo exato inferior a `10⁻⁶ m`.
- Modelo `modelo_orbital.py` preservado nesta repaginação. Energia ligada e colisão são verificadas separadamente; o corpo para na superfície. As órbitas ligadas sem colisão de N13 percorrem seu período completo.
- Renders: inspeção estática dos marcos, teste N01/N07/N08, regressão curta de câmera, preview completo e revisão localizada dos relógios N10/N11. O render completo concluiu 315 animações.
- A revisão temporal detectou referências gráficas antigas durante a troca horizonte/esfera. A cena agora entrega as raízes atuais ao Cairo, evitando desenhar filhos já removidos. A correção foi conferida no teste curto e nas amostras do MP4 completo.
- Inspeção das 10 pranchas de marcos e das 18 pranchas temporais, com abertura adicional de quadros nativos para equações, zoom local, classificações e órbita elíptica completa. Esta revisão é por amostragem temporal, sem alegação de inspeção visual individual dos 6.506 frames.
- `verificar_preview.py`: resolução, fps, duração compatível com o timing, codec, formato de pixel e ausência de áudio aprovados. `tecnico.json` registra os resultados do arquivo entregue.

## Arquivos da unidade

Entrada `cena.py`; implementação em `encenacao.py` e `geometria_visual.py`; preservação da cena anterior em `cena_v1.py`. Ficha e cópia da proposta registram o escopo autorizado. Utilitários desta rodada: `validar_repagina.py`, `teste_camera.py`, `amostrar_movimento.py`, `regularizar_preview.py`, `substituir_relogios.py`, `empacotar_repagina.py`; `verificar_preview.py` recebeu a leitura do CRF e a captura do estado concluído. `.gitignore` mantém os intermediários de render/QA fora do versionamento.

Nenhum arquivo global, dependência ou outra unidade foi alterado por esta rodada. Sem commit, branch, PR ou publicação.

## Teste do arsenal e limites

Nenhum sólido Blender integrado, conforme briefing. A esfera usa imagem procedural RGBA de 512×512, até 24 orientações em cache (aproximadamente 24 MiB de pixels), e horizonte vetorial para os grandes aumentos. Não houve geração de sequências Blender. Funcionaram a iluminação, a oclusão e a projeção compartilhada; a geografia é esquemática e a aproximação extrema evidencia a resolução da textura no preview.

A entrega permanece em **preview visual para revisão editorial**. Ritmo e pausas são silenciosos; a sincronização com uma futura narração pertence à etapa seguinte. A aprovação artística permanece com o usuário. Voz, SRT, master final, capa e publicação não foram produzidos.

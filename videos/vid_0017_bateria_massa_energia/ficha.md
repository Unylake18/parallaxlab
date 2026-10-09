# Uma bateria carregada pesa mais?

- ID: `vid_0017_bateria_massa_energia`
- formato: `curto_vertical`
- Série pública: **ABSURDO CALCULÁVEL • EP.01**.
- Fase: sincronização, legendas e render final concluídos; entrega local em 1080×1920 / 30 fps.
- Classe sincronizada: `BateriaMassaEnergiaFinal` em `cena.py`.
- Classe silenciosa: `BateriaMassaEnergia`; rodadas anteriores preservadas.
- solido_3d: `nenhum` — unidades, energia, massa e ordens de grandeza; a geometria 3D não acrescenta compreensão.

## Especificação atual aprovada

Comparar a mesma bateria à mesma temperatura e sem ganho/perda de matéria.
A carcaça não muda de tamanho; a energia interna adicional corresponde a uma
massa total ligeiramente maior.

- Bateria fictícia: 3,8 V nominais e 4000 mAh = 4 Ah.
- Estimativa: 15,2 Wh = 54.720 J → 0,608842 ng; tela: **≈0,6 ng**.
- Para acrescentar 1 g: 8,98755×10¹³ J = 24,9654 GWh; tela: **≈25 GWh**.
- Quantidade: 1,64246×10⁹ baterias com a mesma capacidade energética; tela: **≈1,6 BILHÃO**.
- Hipótese separada: 250 Wh/kg → 99.861.686,5 kg; tela: **≈100 MILHÕES de kg**, como informação secundária.
- São Paulo: 26,91 TWh em 2023 / 8760 h = 3,071918 GWh/h;
  24,9654 GWh / 3,071918 GWh/h = 8,126982 h; tela: **≈8 HORAS do consumo elétrico médio do município de São Paulo**.
- Fechamento retorna à bateria original e ao acréscimo de ≈0,6 ng.
- CTA aprovado na voz e na imagem: **Siga o Parallax Lab.** / `@labparallax`.
- A montagem atual substitui os antigos casos de navio e +1 kg; não os inclui.

## Fonte da comparação com São Paulo

SEMIL — Anuário de Energéticos por Município 2024, ano-base 2023, p. 8.
Dado do **município**, não do estado: 26,91 TWh de eletricidade em 2023.

[Documento oficial](https://smastr16.blob.core.windows.net/home/2025/04/Anuario-de-Energeticos-por-Municipios-do-Estado-de-Sao-Paulo-2024-ano-base-2023.pdf)

A comparação representa o consumo elétrico médio anual. A nota de 2023 fica
visível na cena. Skyline procedural azul/ciano, com quatro grupos de janelas
que acendem durante a sequência 0 → 2 → 4 → 6 → 8 h; não é foto nem mapa exato.

## Narração e sincronização

- Texto final aprovado: `texto_narracao.txt` (275 palavras), transcrito integralmente do pedido do usuário.
- Fonte recebida: `K:/Downloads/ElevenLabs_Untitled_project (10).wav`.
- Cópia preservada, byte a byte: `audio/narracao_final.wav`, 110,48 s, PCM 16 bits, estéreo, 44,1 kHz.
- SHA-256: `72437a68a8eb7d5ce14784343d2b931824fc6d9157ca5e003d106e470c38c0e2`.
- A voz entra em 0,4 s; não foi acelerada, cortada ou regenerada.
- `gerar_sync.py`: frases ancoradas nas pausas medidas do WAV; palavras internas
  estimadas por pesos silábicos. Sem reconhecimento automático de fala.
- `palavras_tempos.json`: 27 limites de frase internos ancorados e estimativas por palavra.
- `sync.json`: 32 âncoras da fala e agenda de 131 operações, com duração alvo de 111,3 s.
- `native.json`: operações da rodada silenciosa 5, usadas como referência de duração.
- As entradas conservam duração curta; tempo extra vira permanência do estado pronto.
- O fechamento apresenta bateria/0,6 ng, depois a pergunta, e só então SIM / MAS QUASE NADA / CTA.
- CTA elevado para y = −4,15, reservando a faixa inferior para as legendas.
- `legenda.srt`: 45 cues, até duas linhas; frases curtas ficam em uma linha.
  Grafia numérica na rodada 7 (3,8; 4.000; 54.720; 0,6; 25; 1,6; 250;
  100 milhões; 8 horas), mantendo o conteúdo aprovado, incluindo **Siga**.

## Entrega atual — rodada 7 (08/10/2026)

- Cabeçalho: **ABSURDO CALCULÁVEL • EP.01**, Space Grotesk Medium, tamanho 20,
  opacidade 0,65 e margem 0,4, conforme o tamanho observado nos episódios anteriores.
- Logo oficial: original 2172×724; redução Lanczos para 216×72 no render 1080,
  conservando largura de 1,8 unidades, opacidade 0,35 e margem 0,28.
  Não houve troca do desenho nem aumento artificial do logo.
- Formato conferido contra os arquivos de postagem dos vídeos 0015 e 0016:
  **1080×1920, 9:16, 30 fps**, quadro lógico 9×16. Cabeçalho, marca e legendas
  mantêm o padrão de tamanho. O tamanho em MB depende da duração, do conteúdo
  e da compressão, não indica as dimensões da imagem.
- A entrega anterior era Full HD nativo, porém seu master usava CRF 23/4:2:0
  e o legendado CRF 18. A rodada atual foi renderizada novamente em resolução
  nativa com master H.264 4:4:4, QP 0; não há perdas de compressão nesse master.
  Configuração restrita à unidade, sem alterar Manim instalado ou template.
- Para uso normal: `renders/vid_0017_bateria_massa_energia_final_legendado_v2.mp4`,
  H.264 4:2:0, CRF 14, preset slow, **8.375.184 bytes**.
- Imagem legendada sem perdas de compressão:
  `renders/vid_0017_bateria_massa_energia_legendado_sem_perdas_v2.mp4`,
  H.264 4:4:4, QP 0, **16.483.031 bytes**.
- Master limpo: `renders/vid_0017_bateria_massa_energia_final_master_limpo_v2.mp4`,
  H.264 4:4:4, QP 0, **21.279.395 bytes**.
- Todos em 1080×1920 / 30 fps exatos, **3.339 quadros e 111,3 s**.
  Áudio AAC estéreo 48 kHz; os dois legendados copiam os mesmos pacotes AAC do
  master. A indicação sem perdas refere-se à compressão da imagem.
- `numeros_legenda.py` mapeia expressões faladas para algarismos, unindo cada
  número ao intervalo completo da expressão original. Artigos como «uma bateria»
  permanecem escritos. As 45 cues continuam com até duas linhas, Arial Bold
  de 58 px em 1080, mesma posição e estilo anteriores. Largura máxima 870 px,
  abaixo do limite seguro de 936 px.
- `gerar_sync.py` regenerou a legenda; comparadas as estruturas de `sync.json`
  antes/depois: agenda e âncoras integralmente idênticas. WAV aprovado inalterado.
- Verificações aprovadas: `py_compile` dos cinco helpers/cena; render Manim
  1080×1920; montagem dos dois legendados; QA completo com
  `verificar_montagem.py ... --legendado --alta-qualidade`.
- Decodificados todos os 3.339 quadros de cada legendado; verificadas dimensões,
  fps, grafia numérica, contas, 131 operações nos quadros exatos da agenda,
  início/fim da narração e identidade dos pacotes de áudio entre as entregas.
  Correlação da envoltória com o WAV: 0,994986; fala detectada em 0,47–110,60 s.
- Conferidos os parâmetros efetivos de codificação gravados nos MP4:
  QP 0 nos masters sem perdas de compressão e CRF 14 no arquivo para uso normal.
- Inspecionadas 69 amostras em nove painéis; conferidos também topo, fórmulas,
  contagem de baterias e CTA em quadros 1080 nativos. Sem cortes ou sobreposição
  de legendas com as informações da cena nas amostras conferidas.
- QA: `media_r7/qa_final/verificacao.json`; comparação com o padrão anterior:
  `media_r7/inspecao/comparacao_padrao.json` e `topos_comparados.png`.
- 19 frames atualizados: `media_r7/frames_final_19/` e
  `media_r7/frames_final_19.zip`; quantidade e CRC conferidos.
- Arquivos de produção alterados/criados: `cena.py`, `gerar_sync.py`,
  `numeros_legenda.py`, `montar_final.py`, `verificar_montagem.py`, `legenda.srt`
  e `ficha.md`. Arquivos anteriores de vídeo preservados.
- Limites reais: alinhamento interno por pausas/sílabas, sem ASR, como na rodada
  anterior; não houve teste em celular físico. O logo continua pequeno e com
  baixa opacidade conforme o padrão; uma reprodução reduzida perde detalhe.
- Teste do arsenal: nenhum sólido nesta revisão; animação 2D aprovada mantida,
  sem demanda geométrica nova. Nenhuma pendência de implementação desta rodada.
- Sem alteração global, dependências, voz, commit, push ou publicação.

## Verificação do preview sincronizado

- `py_compile`: aprovado para a cena e os helpers locais.
- Preview 540×960 / 15 fps nominal: 1.670 frames, 111,329753 s, AAC estéreo 48 kHz.
- Inspecionadas 69 amostras com legendas, cobrindo estados, âncoras e resultados principais.
- Contagem total dos frames conferida contra todos os segmentos do Manim.
- Envoltória da voz no MP4 correlaciona 0,994986 com a fonte, sem alteração de ritmo.
  Deslocamento medido de 0,42 s (0,4 s de entrada + priming do AAC, inferior a um quadro de 30 fps).
- Fala detectada no MP4: 0,47–110,60 s; final da fonte preservado.
- Números conferidos por `verify_physics()`. Limites de conteúdo conferidos pela cena.
- Legendas sem sobreposição com fórmulas, notas ou CTA nas amostras inspecionadas.
- Preview: `media_sync/videos/cena/960p15/BateriaMassaEnergiaFinal.mp4`.
- QA: `media_sync/qa_preview/`; metadados da prévia preservados em `media_sync/estados_preview_540.json`.

## Entrega final — rodada 6 (08/10/2026)

- Final legendado: `renders/vid_0017_bateria_massa_energia_final_legendado.mp4`.
- Master com áudio, sem legendas incorporadas: `renders/vid_0017_bateria_massa_energia_final_master_limpo.mp4`.
- Ambos: H.264, 1080×1920, 30 fps nominais; duração final **111,3 s (1min51,3s)**; 3.339 frames.
- Áudio AAC estéreo, 48 kHz. Fonte WAV aprovada preservada byte a byte.
- SRT separado: `legenda.srt`, 45 cues, no máximo duas linhas.
- 19 imagens finais com legendas, 1080×1920: `media_sync/frames_final_19/` e `media_sync/frames_final_19.zip`; contagem e CRC conferidos.
- QA completo: decodificados todos os 3.339 frames; 69 amostras de estados/âncoras inspecionadas em `media_sync/qa_final/`.
- As 131 operações começam exatamente nos quadros da agenda; corrigido localmente o truncamento de floats em pausas congeladas do Cairo (três quadros). Nenhuma dependência alterada.
- Verificados texto integral das legendas, CTA Siga, início/fim da voz, resolução, fps, áudio e contas. A correlação da envoltória da voz com a fonte é 0,994986.
- Conferência visual: sem cortes de fórmulas, unidades ou sobreposição com legendas nas amostras inspecionadas. CTA acima da faixa de legendas.
- Limites da verificação: palavras internas estimadas por pausas/sílabas; inspeção visual em quadros/miniaturas. Não houve teste em um celular físico.
- Matemática e física anteriores mantidas. Voz não acelerada; final urbano segue como consumo elétrico médio municipal, com base em 2023 visível.
- Arquivos de produção alterados/criados nesta rodada: `cena.py`, `ficha.md`, `texto_narracao.txt`, `audio/narracao_final.wav`, `gerar_sync.py`, `palavras_tempos.json`, `sync.json`, `native.json`, `legenda.srt`, `verificar_montagem.py`.
- Escopo restrito à unidade; sem alteração de template, dependências ou documentos globais. Sem commit, push ou publicação.

## Histórico de previews silenciosos

Rodada 5: fechamento com São Paulo; 108,597721 s; primeira parte preservada
contra a rodada 4 (13 imagens idênticas). Arquivos em `media_r5/`.
Os relatos abaixo registram fases antigas; não descrevem a montagem atual.

### Resultado da rodada 1 — 08/10/2026

- `py_compile`: aprovado.
- Render: concluído, 97 animações, 540×960 / 15 fps configurados, sem áudio.
- Duração provisória: aproximadamente 110 s; MP4 de 2.065.095 bytes.
- Preview: `media/videos/cena/960p15/BateriaMassaEnergia.mp4`.
- Inspeção visual: 23 estados extraídos do MP4 em `media/qa/` e reunidos em
  `painel_01.jpg`, `painel_02.jpg` e `painel_03.jpg`.
- Pergunta, 15,2 Wh (21,0 s), 54 720 J (29,4 s), 0,6 ng (53,5 s), rehook
  1 g (60,4 s), 25 GWh (76,3 s), 100 mil toneladas (94,5 s) e fechamento
  (107,5 s) conferidos. Sem cortes de fórmula ou sobreposições relevantes;
  faixa inferior preservada e payoffs destacados.
- Contas conferidas numericamente com c ≈ 3×10⁸ m/s; arredondamentos conforme
  briefing. A carcaça mantém tamanho ao carregar; multiplicação posterior
  identificada como quantidade simbólica, sem elétrons ou balança.
- Limitação operacional resolvida: o registro temporário da fonte pelo Pango
  falhou no sandbox; o render funcionou fora dele, sem alterar o ambiente.
- Decisão futura de Produção: avaliar ritmo/duração do piloto na etapa de voz;
  esta rodada não fixa duração final. Nenhuma inconsistência objetiva encontrada.

### Resultado da rodada 2 — 08/10/2026

- Alterados somente `cena.py` e esta ficha na unidade; preview da rodada 1
  preservado em `media/`. Sem mudança de conteúdo, ordem ou payoffs.
- `py_compile`: aprovado. Render refinado concluído: 104 animações,
  540×960 / 15 fps nominal, zero trilhas de áudio, aproximadamente 117,9 s.
- MP4: `media_r2/videos/cena/960p15/BateriaMassaEnergia.mp4` (2.279.512 bytes).
- Topo/marca conferidos com o padrão das unidades 0015/0016: tag à esquerda,
  watermark oficial à direita e título abaixo; sem novo logo ou asset.
- Paleta conferida: azul estrutural, violeta conceitual/intermediário, magenta
  pontual e ciano dominante nos números-payoff. Nenhuma fórmula cortada ou
  sobreposição persistente; faixa inferior preservada.
- Inspeção dos 24 estados principais em `media_r2/qa/estados_01…03.jpg`,
  incluindo cancelamento de Wh. Quadros de 14 transições e quatro janelas de
  movimento de produto, rearranjo, substituição e divisão final também
  inspecionados. Metadados de tempo são provisórios e orientam a inspeção.
- Refinados de fato: prefixo mAh → Ah; composição V × Ah e cálculo de Wh;
  c² atravessando a relação para o denominador; substituição por cópia das
  referências; preservação de Δm/≈ na avaliação; régua até ng e entrada do
  payoff; inversão dos rótulos massa/energia por arcos; cancelamento de Wh
  e passagem de kg ao resultado; continuidade de toneladas no fechamento.
- Valores diferentes usam saída/entrada em fases, evitando sobreposição de
  dígitos sem correspondência matemática. Mapas de glifos sem debug em tela.
- Limitação operacional resolvida localmente: o `key_map` entre grafias de Ah
  acionou erro no Manim; a grafia foi padronizada para matching direto, sem
  alterar dependências. Registro de fontes fora do sandbox como na rodada 1.
- Pendência: avaliação editorial do acabamento e do ritmo provisório pela
  Produção. Sem bloqueios técnicos; nenhuma etapa de voz/final foi iniciada.

### Resultado da rodada 3 — 08/10/2026

- Alterados somente `cena.py` e esta ficha; saídas da rodada em `media_r3/`,
  com os previews e as seleções anteriores preservados.
- `py_compile`: aprovado. Render concluído: 121 animações, 540×960 / 15 fps
  nominal, 1.835 frames, zero trilhas de áudio, aproximadamente 122,3 s.
- Preview: `media_r3/videos/cena/960p15/BateriaMassaEnergia.mp4`
  (2.580.689 bytes).
- Conferidos os 30 estados assentados capturados diretamente da câmera
  (`media_r3/qa/estados/`, painéis `estados_01…04.jpg`) e 57 quadros do MP4
  cobrindo 16 transições (`movimento_01…08.jpg`). Sem cortes de conteúdo,
  sobreposição persistente de números ou debug; faixa inferior preservada.
- Confirmados carga progressiva sem deformar a carcaça, especificações
  saindo da bateria, convergência V/Ah, Wh emergindo da conta, conversor
  Wh/J, etiqueta alimentando ΔE, rearranjo de c² e substituição por cópia.
- Confirmados régua construída durante o movimento do ponto, payoff de
  0,6 ng, recuo para o rehook, inversão real da seta, apoio transitório de
  1 g em kg, 25 GWh, divisão colorida com cancelamento de Wh e crescimento
  simbólico 1 → 4 → 16 → 48 integrado ao número de kg.
- Fechamento conserva toneladas e +1 g como eixos; primeira frase sai antes
  da segunda, sem acúmulo de parágrafos.
- Verificação numérica: 15,2 Wh = 54.720 J; diferença de massa 0,608 ng;
  1 g corresponde a 25 GWh com c ≈ 3×10⁸ m/s; a hipótese de 250 Wh/kg
  resulta em 100.000 toneladas. Arredondamentos do briefing preservados.
- Entrega para o limite de anexos: exatamente 19 PNGs de 540×960 em
  `media_r3/frames_envio_19/`, numerados em ordem narrativa, e o pacote
  `media_r3/frames_envio_19.zip`. São estados selecionados; o preview
  contém o movimento completo.
- Registro de fonte fora do sandbox como nas rodadas anteriores, sem
  mudanças de ambiente ou dependências. Sem bloqueios técnicos.
- Pendência editorial: avaliação do acabamento e do ritmo provisório pela
  Produção. Voz, SRT, capa, master final e publicação continuam fora da fase.

### Resultado da rodada 4 — 08/10/2026

- Alterados `cena.py` e esta ficha, somente na unidade. Preview e imagens
  das rodadas anteriores preservados. Sem commit ou push.
- Substituídos o bloco antigo de quantidade/toneladas e o fechamento
  comparativo. Novo percurso: contagem por 15,2 Wh → hipótese separada
  de massa → comparação com navio → ×1000 para 1 kg → bateria e CTA.
- A primeira parte até 0,6 ng foi preservada: comparação dos 13 PNGs de
  referência com a rodada 3 confirmou arquivos idênticos.
- Duração antiga: **122,3 s**; nova: **113,1 s**, redução de cerca de 9,2 s.
  Caso de +1 g, do rehook até o payoff do navio: **35,3 s** (63,6–98,9 s).
  Escalada de +1 kg: **8,2 s** (98,9–107,1 s). Conclusão/CTA: **6,0 s**.
  Tempos reais do primeiro render; refinamentos de fases mantiveram a
  duração do MP4 a menos de 1 ms. Metadados da Scene com cache são indicativos.
- Números públicos: 15,2 Wh, 54.720 J, 0,6 ng; para +1 g, ≈25 GWh,
  ≈1,6 bilhão de baterias, ≈100 milhões de kg a 250 Wh/kg e ordem de massa
  de 1 superporta-aviões; para +1 kg, ×1000 → ≈1,6 trilhão de baterias,
  ≈100 bilhões de kg e ordem de massa de 1000 superporta-aviões.
- Um navio: silhueta lateral procedural em ciano/azul, largura de 6,7
  unidades no quadro 9×16, com casco, convés, ilha, mastro e dois aviões
  mínimos. Sem foto, asset global ou Blender.
- Mil navios: 1 → fileira de 10 → grade de 100 miniaturas, explicitamente
  marcada como **este bloco ×10**, com resultado ≈1000. Cem miniaturas de
  cinco primitives cada; render concluído sem falha de performance.
- `py_compile`: aprovado. Preview concluído: 141 animações, 540×960 /
  15 fps nominal, 1.697 frames, nenhuma trilha de áudio.
- Preview final desta fase: `media_r4/videos/cena/960p15/BateriaMassaEnergia.mp4`
  (3.118.261 bytes). Render inicial e refinamento registrados em
  `media_r4/render_preview.log` e `media_r4/render_ajustes.log`.
- QA: 33 estados assentados, cinco painéis `media_r4/qa/estados_*.jpg`;
  56 quadros de 12 transições, incluindo inspeção específica das duas
  fases refinadas. Corrigidos cruzamento de toneladas com o navio e
  coincidência da equivalência kg/g com a legenda do bloco de baterias.
- Screenshots principais: `media_r4/qa/payoffs_principais.jpg` e PNGs
  individuais em `media_r4/qa/estados/`. Entrega de exatamente 19 PNGs
  540×960, numerados, em `media_r4/frames_envio_19/` e no ZIP homônimo;
  contagem, resolução e integridade do ZIP aprovadas.
- QA didático: quantidade distinguida de massa; hipótese de 250 Wh/kg
  separada; navios como comparação aproximada de massa total; acréscimos
  +1 g/+1 kg separados da massa do conjunto. Retorno à pergunta inicial,
  resposta SIM e 0,6 ng por carga completa do exemplo antes do CTA.
- Sem cortes, debug ou ambiguidade persistente identificada nos quadros
  inspecionados. Miniaturas representam escala simbólica, sem precisão
  geométrica naval; comparação usa ≈ e ordem de massa. Referência oficial
  e distinção long tons/toneladas métricas registradas acima.
- Pendência real: avaliação editorial do ritmo e da compreensão pelo público;
  o preview é silencioso e não valida encaixe de narração. Nenhuma etapa de
  voz, SRT, master final ou publicação foi iniciada.

## Teste do arsenal

- Sólido usado: nenhum, conforme briefing explícito.
- Resolução: preview Manim 540×960 / 15 fps; sem sequências 3D.
- Custo/peso 3D: zero.
- Adequação: bateria e régua 2D bastam para a investigação de energia/massa.
- Faltas do arsenal: não avaliadas; consulta fora do escopo desta rodada.

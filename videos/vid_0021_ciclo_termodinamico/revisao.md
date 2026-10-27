# VID21 — versão com partículas para avaliação

Data: 2026-10-12. Série: EXERCÍCIO RESOLVIDO · EP. 07.

Adicionadas 36 partículas em violeta claro dentro dos recipientes da abertura,
introdução, ferramentas e três processos. Quantidade fixa; rapidez proporcional
à raiz quadrada da temperatura. As partículas refletem nas paredes e abaixo da
face inferior do pistão, acompanhando o volume. Temperatura e energia interna
crescem juntas para essa quantidade fixa de gás; rapidez e concentração
representam qualitativamente o comportamento da pressão. O magenta continua
indicando o calor. Mantidos texto, voz, contas, gráfico, cabeçalho e CTA.

## Arquivos alterados

- `cena.py`: movimento molecular e saídas separadas para a nova variante.
- `montar_final.py`: opção `--particulas`, sem sobrescrever as fontes anteriores.
- `ficha.md` e `revisao.md`: estado e resultado desta rodada.
- `qa_particulas/verificar_modelo.py` e `verificar_audiovisual.py`: verificações e evidências.
- `revisao_sem_particulas.md`: relatório anterior preservado. Os masters e
  legendados anteriores continuam em `renders/vid_0021_master.mp4` e
  `renders/vid_0021_legendado.mp4`.

Não foram alterados áudio, SRT, texto da narração, dependências ou arquivos globais.

## Renders e verificações

Preview: 540×960, 15 fps, CRF 23, 2517 quadros/167,80 s de vídeo.
Final: 1080×1920, 30 fps, H.264/yuv420p, CRF 14, 5032 quadros/167,7333 s.
Voz AAC estéreo, 44,1 kHz, 167,76 s; final com diferença entre áudio e vídeo
menor que um quadro. O master copia o vídeo do Manim sem recompressão.
Legendado em CRF 14/preset medium.

Concluídos com sucesso:

- Sintaxe dos quatro scripts e `git diff --check`.
- Confinamento em 723 estados amostrados dos três processos, incluindo a face
  inferior do pistão; quantidade fixa de 36 partículas e rebotes detectados.
- Rapidez relativa 1:2:4 para temperaturas relativas 1:4:16.
- Renders e montagens completos nas duas resoluções.
- Decodificação integral dos quatro novos arquivos, PTS/CFR, resolução, fps,
  codecs, formato de pixel e CRF gravado no stream.
- Hash dos pacotes: áudio igual ao anterior e entre master/legendado; vídeo do
  master igual ao render do Manim.
- SRT integral, com as mesmas 64 legendas. Marcos visuais variaram no máximo
  66,67 ms no preview e 33,33 ms no final em relação à versão anterior.
- Inspeção visual de 24 quadros em cada resolução, cobrindo todos os blocos.
  Fórmulas, sinais, marca, legenda e CTA conferidos.

Evidências em `qa_particulas/modelo.json`, `audiovisual_960.json`,
`audiovisual_1920.json`, `contato_preview_*.jpg` e `contato_final_*.jpg`.
`movimento_estados.gif` compara detalhes de A, B e C em movimento.

## Artefatos

Preview legendado: `renders/vid_0021_particulas_preview_legendado.mp4`.
Master/legendado final: `renders/vid_0021_particulas_master.mp4` e
`renders/vid_0021_particulas_legendado.mp4`.

Entrega reunida com `uv run --no-sync python videos/entregar.py vid_0021` em:

`entregas/Exercício Resolvido - EP 07 - Ciclo termodinâmico - 0021/`

Contém master, legendado, SRT, áudio, textos e manifesto. Fontes anteriores
preservadas na unidade; a pasta de entrega passa a apontar para a nova variante.

## Limitações e pendências

Modelo molecular 2D qualitativo: posições relativas acompanham a mudança do
domínio; não há colisões entre partículas nem integração quantitativa do impacto
em parede móvel. A rapidez é determinada pela temperatura prescrita no ciclo.
O alinhamento original por pausas do WAV e interpolação silábica foi preservado.
Avaliação humana contínua do novo movimento junto à voz permanece pendente.

Teste do arsenal: mantido o 2D aprovado; nenhum sólido 3D integrado, sem custo
ou alteração de ponte. Capa, publicação, commit e push fora desta rodada.

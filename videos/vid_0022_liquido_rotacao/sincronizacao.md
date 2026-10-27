# VID22 · EP. 08 — sincronização com o texto confirmado

Texto da gravação fornecido pelo usuário: **458 palavras**, de “Quando um líquido começa a girar” até “Siga o Parallax Lab”. Substitui a referência R2 de 397 palavras usada na primeira tentativa. A montagem anterior foi preservada em `sync_anterior_r2/`.

## Entrega

- `preview_legendado.mp4`: legendas coloridas incorporadas, 6.469.679 bytes.
- `preview_sincronizado.mp4`: mesma montagem sem legendas incorporadas, 5.882.670 bytes.
- Ambos: 170,8 s, 540×960, 15 fps, 2.562 quadros, H.264/yuv420p, CRF 14.
- WAV completo: 166,8 s, estéreo, 44,1 kHz, sem mudança de velocidade. Cópia local idêntica ao original por SHA-256.
- `legenda.srt`: 65 blocos, até duas linhas, texto simples integral confirmado.
- `legenda_colorida.ass`: legenda editável com cores semânticas.

## O que mudou

Abertura retimada para que a superfície afunde e suba durante a descrição inicial; o paraboloide já está formado durante a pergunta. Álgebra, cancelamentos e integração seguem os tempos da nova fala.

A montagem agora segue a ordem narrada: seção → paraboloide/desnível → síntese causal → frase final → cartão da marca. Trechos existentes da V3.1 foram montados em quatro blocos, com cortes entre os blocos finais. A passagem redundante da conclusão pela relação inclinação→quadrado foi omitida na montagem, pois essa relação já aparece na síntese narrada. “Siga o Parallax Lab” aparece integralmente sobre a marca, a partir de 165,26 s. Logo permanece até 170,8 s, com 4 s silenciosos após o WAV.

Não houve edição da cena silenciosa, da física ou do asset. A faixa inferior reservada recebe as legendas sem reduzir a cena. Branco como base; pressão/gradiente em `#D77CFF`, coordenadas/inclinação/velocidade em `#35D9FF`, líquido/superfície/altura/geometria em `#75BDFF`.

## Verificações

- Compilação dos quatro helpers locais: aprovada.
- WAV original/cópia: SHA-256 idêntico.
- SRT igual ao texto confirmado: 458 palavras; ordem temporal, ausência de sobreposição, até duas linhas e largura segura ≤448 px aprovadas.
- Decodificação integral dos dois MP4: 2.562 quadros cada, relógio contínuo a 15 fps, áudio integral decodificado; duração, resolução, codecs e CRF 14 conferidos.
- Inspeção visual de 37 instantes distribuídos pelo vídeo; nova inspeção da abertura e dos blocos finais após antecipar a deformação. Relatório técnico e quadros da exportação entregue: `qa_sync_confirmado_final/`.
- Dois passes de montagem nesta correção; nenhum render novo de Manim ou Blender.

## Método e limite

Finais das frases ancorados nas pausas RMS do WAV por programação dinâmica; palavras internas estimadas por peso silábico. São 59 pontos em quatro blocos. O texto agora foi confirmado diretamente pelo usuário. Os tempos internos ainda são estimados, sem alinhamento fonético palavra a palavra.

## Arquivos alterados ou gerados

Na unidade: `texto_narracao.txt`, `gerar_sync.py`, `gerar_ancoras.py`, `sincronizar_preview.py`, `verificar_sync.py`, `alinhamento_palavras.json`, `sync.json`, `legenda.srt`, `legenda_colorida.ass`, `preview_sincronizado.mp4`, `preview_legendado.mp4`, `ficha.md`, este relatório e logs. Novas pastas: `sync_anterior_r2/`, `media_sync_confirmado/`, `qa_sync_confirmado/` (primeira inspeção) e `qa_sync_confirmado_final/` (exportação entregue).

Reprodução: executar `gerar_sync.py`, `gerar_ancoras.py`, `sincronizar_preview.py` e `verificar_sync.py`, nessa ordem, com `uv run --no-sync python videos/vid_0022_liquido_rotacao/<helper>.py`.

## Teste do arsenal

`liquido_rotacao`: caches aprovados e inserções da V3.1 reaproveitados a 540×960, sem tracers. Custo adicional de Blender: zero; cache preservado (~179 MiB). Setor e meridiana mantêm leitura limpa. Não houve alteração estrutural ou necessidade de novo sólido.

Esta entrega fecha a correção do preview sincronizado e das legendas. Master 1080p, capa, publicação e fechamento da unidade em `entregas/` continuam fora desta etapa. Sem commit ou push.

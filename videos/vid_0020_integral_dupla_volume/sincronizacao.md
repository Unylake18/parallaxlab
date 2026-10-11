# VID20 · EP.07 — sincronização da narração aprovada

- Áudio recebido: `ElevenLabs_Untitled_project (21).wav`, 171,36 s, preservado na duração e velocidade originais.
- Base visual: preview V6 existente. Sincronização por 43 marcos semânticos; fonte `cena.py` preservada, confirmada por SHA-256.
- Entrega: `preview_legendado.mp4`, 540×960, 15 fps, 2.577 quadros, 171,80 s de vídeo e 171,36 s de áudio. Encerramento de 0,44 s após o áudio.
- Alternativa: `preview_sincronizado.mp4`, mesma sincronização, sem legenda incorporada.
- `legenda.srt`: 72 blocos, até duas linhas, texto integral aprovado. As cores ficam incorporadas no MP4; SRT conserva texto simples.
- Cores: área/base em ciano; função/altura em magenta; volume/colunas em violeta; seções e integrações com cores correspondentes à cena.
- A versão legendada conserva cabeçalho/título e reduz uniformemente o corpo da cena para reservar a faixa inferior. Fórmulas e notas auxiliares ficam acima das legendas. Ajuste local na montagem.

## Arquivos criados nesta etapa

Na unidade: `audio/narracao_final.wav`, `texto_narracao.txt`, `gerar_sync.py`, `alinhamento_palavras.json`, `sync.json`, `legenda.srt`, `sincronizar_preview.py`, os dois MP4 acima e este relatório.

Em `media/vid_0020_sincronizado/`: cópia de preservação da cena V6, intermediários de montagem, mapa de sincronização, relatórios de validação, log do alinhamento, scripts de conferência e imagens de inspeção.

## Conferência executada

- Compilação dos dois scripts locais.
- WAV copiado idêntico ao original, verificado por SHA-256.
- Texto do SRT idêntico ao aprovado; ordem temporal, ausência de sobreposição, máximo de duas linhas e largura segura verificados.
- Decodificação integral dos dois MP4: 2.577 quadros cada, intervalos contínuos de 1/15 s, resolução e duração conferidas; áudio completo nos dois arquivos.
- Inspeção visual de 19 instantes distribuídos pela unidade, mais o encerramento extraído do MP4 entregue: coluna isolada, cores, faixa de legenda, refinamento, integrações, limites e resultado.

## Limite do alinhamento

As frases foram alinhadas às pausas medidas da gravação. Os tempos das palavras dentro de cada frase são estimados por peso silábico, seguindo o método local de produção; não constituem alinhamento fonético palavra a palavra. A legenda é apresentada em blocos.

Não houve alteração da matemática ou do template global. A inspeção foi dirigida à sincronização e à legenda desta entrega.

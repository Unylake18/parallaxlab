# VID22 · EP. 08 — preview sincronizado e legendas

Áudio recebido: `ElevenLabs_Untitled_project (20).wav`, 166,8 s, estéreo/44,1 kHz. Cópia idêntica em `audio/narracao_final.wav`, confirmada por SHA-256. Velocidade e conteúdo do WAV preservados.

Referência textual adotada: revisão R2 de 397 palavras. Foi enviada uma pergunta opcional para confirmar a versão do texto; a resposta não estava disponível no fechamento desta montagem. O WAV não foi transcrito por reconhecimento de fala. A igualdade conferida é entre SRT e roteiro de referência, não uma comparação independente com o conteúdo falado.

## Entrega desta etapa

- `preview_legendado.mp4`: legendas coloridas incorporadas.
- `preview_sincronizado.mp4`: mesma sincronização, sem legenda incorporada.
- Ambos: 540×960, 15 fps, H.264/yuv420p, CRF 14, 2.562 quadros, 170,8 s; áudio completo de 166,8 s. Encerramento visual silencioso de 4 s após o WAV.
- `legenda.srt`: 64 blocos, até duas linhas, texto simples.
- `legenda_colorida.ass`: versão editável com destaques semânticos.

A fonte visual é o preview silencioso V3.1 existente. Ajuste temporal por 50 âncoras locais, sem render Manim ou Blender. A cena V3.1 e seus caches permanecem preservados. As legendas ocupam a faixa inferior já reservada; não houve redução da cena. Texto branco, pressão/gradiente em `#D77CFF`, coordenadas/inclinação em `#35D9FF`, superfície/altura/geometria em `#75BDFF`.

## Método e limite

Finais de frases ancorados em pausas RMS do WAV por programação dinâmica. Ritmo silábico e limite de velocidade de fala impedem alguns encaixes extremos. Tempos internos das palavras interpolados por peso silábico. Isso constitui **sincronização estimada por frases**, não alinhamento fonético. Sem transcrição independente ou escuta humana de aprovação, não se pode garantir correspondência exata palavra a palavra nem excluir diferenças entre áudio e R2.

A primeira tentativa revelou ancoragens de vírgulas que esticavam palavras isoladas. A versão entregue usa finais de frases, corrigindo esse problema. O encerramento associa desnível à medição em 3D, inclinação→altura quadrática à seção e frase final ao paraboloide limpo.

## Verificações executadas

- Compilação dos quatro helpers locais: aprovada.
- SHA-256 original/cópia do WAV: idêntico.
- SRT igual ao texto de referência: aprovado; ordem temporal, sem sobreposição, até duas linhas e largura ≤448 px: aprovados.
- Decodificação integral dos dois MP4: 2.562 quadros por arquivo, relógio contínuo a 15 fps; áudio integral decodificado; resolução, duração, H.264/yuv420p e CRF 14 conferidos.
- Inspeção visual de 21 instantes extraídos do MP4 legendado entregue: cores, área segura, fórmulas, cancelamentos, regra da cadeia, integração, desnível e branding. Amostras e metadados em `qa_sync_v2/`.
- Dois passes de montagem/inspeção desta sincronização; nenhum novo render da cena.

## Arquivos desta etapa

`audio/narracao_final.wav`, `texto_narracao.txt`, `gerar_sync.py`, `gerar_ancoras.py`, `sincronizar_preview.py`, `verificar_sync.py`, `alinhamento_palavras.json`, `sync.json`, `legenda.srt`, `legenda_colorida.ass`, os dois previews MP4, logs, `media_sync/`, `qa_sync/` (primeira tentativa), `qa_sync_v2/` (entrega) e este relatório. `ficha.md` registra a fase atual.

Reprodução: `uv run --no-sync python videos/vid_0022_liquido_rotacao/gerar_sync.py`, depois `gerar_ancoras.py`, `sincronizar_preview.py` e `verificar_sync.py`, na mesma pasta. Não iniciar os dois primeiros sem a etapa seguinte, pois eles atualizam os tempos das legendas/âncoras.

## Teste do arsenal

`liquido_rotacao`: caches aprovados e inserções da V3.1 reaproveitados integralmente a 540×960. Custo adicional de Blender: zero; peso do cache preservado (~179 MiB). Setor de co-rotação e meridiana mantêm leitura limpa; nenhuma alteração estrutural do asset nesta etapa.

A entrega é um preview para revisão da sincronização e das legendas. Não houve geração de voz, master 1080p, capa, publicação, commit ou push, nem fechamento final da unidade em `entregas/`.

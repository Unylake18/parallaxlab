# Postagem V4 — vid_0022 · EP. 08

Fechamento autorizado em 12/10/2026 após aprovação do preview V4. Master e legendado em 1080×1920, 30 fps nativos, 170,8 s, H.264/yuv420p/CRF 14, preset medium e faststart. Mantidos os movimentos da V4, as legendas coloridas, a voz recebida e o `@labparallax` menor em degradê ciano→azul.

## Arquivos alterados e gerados

Novos auxiliares locais: `cena_v4_postagem.py`, `montar_v4_postagem.py` e `verificar_v4_postagem.py`. Ficha atualizada; este relatório acrescentado. Metadados: `operacoes_v4_postagem.json`, `marcos_v4_postagem.json`, `media_montagem_v4_postagem/montagem.json` e `qa_v4_postagem/validacao.json`. Nenhum arquivo global alterado; fontes, previews e renders anteriores preservados.

Render visual: `media_v4_postagem/videos/cena_v4_postagem/1920p30/fonte_v4_postagem.mp4`. Finais de origem: `renders/vid_0022_v4_postagem_master.mp4` e `renders/vid_0022_v4_postagem_legendado.mp4`.

## Execução e QA

- Compilação Python dos três auxiliares aprovada.
- Um render completo nativo Manim, com 149 animações executadas; 141 operações de origem e 12 mapas explícitos de glifos conferidos. Fonte de 175,0667 s antes da seleção e reordenação dos blocos aprovados.
- Comando: `uv run --no-sync python -m manim videos/vid_0022_liquido_rotacao/cena_v4_postagem.py LiquidoRotacao022V4Postagem -r 1080,1920 --fps 30 -o fonte_v4_postagem --disable_caching --progress_bar none`.
- Montagem: `uv run --no-sync python videos/vid_0022_liquido_rotacao/montar_v4_postagem.py`. Seleção dos quadros nativos, sem reamostragem temporal. Voz colada ao visual montado; índice MP4 movido para o início sem nova codificação.
- QA: `uv run --no-sync python videos/vid_0022_liquido_rotacao/verificar_v4_postagem.py`, aprovado. Ambos os finais têm 5.124 quadros integralmente decodificados, cadência constante de 30 fps, CRF 14, áudio AAC estéreo integral de 166,8 s e faststart confirmado.
- Legendas conferidas: 458 palavras do texto confirmado, 65 entradas, até duas linhas, sem sobreposição temporal e dentro da largura segura. Cores semânticas preservadas.
- Inspeção visual de 55 instantes em sete painéis, cobrindo abertura, elemento em órbita, álgebra, regra da cadeia, integração, paraboloide, desnível e encerramento. Quinze movimentos matemáticos verificados, com duração de até 1,4 s; maior sequência quase estática no interior dos movimentos: quatro quadros (0,133 s), excluindo pausas intencionais de leitura.
- Master: 16.019.133 bytes. Legendado: 17.453.368 bytes. Evidências nos logs `render_v4_postagem.log`, `montar_v4_postagem.log`, `verificar_v4_postagem.log` e em `qa_v4_postagem/`.

## Teste do arsenal

`liquido_rotacao`: reutilizados 397 PNGs em 1080×1920, 24 amostras, aproximadamente 657,1 MiB, preparados na etapa anterior. Custo Blender adicional nesta rodada: zero. Setor translúcido e geometria mantidos; sem tracers. A resolução nativa funcionou na abertura e no payoff; fórmulas, rótulos e vetores permanecem Manim 2D. Nenhuma alteração do asset foi necessária.

## Entrega e limites

Fluxo oficial: `uv run --no-sync python videos/entregar.py vid_0022`. Pasta: `entregas/Por Trás da Fórmula - EP 08 - Superfície de um líquido em rotação - 0022/`, com master, legendado, SRT, áudio, textos e manifesto. A V4 passa a ser a versão atual nessa pasta; as origens anteriores permanecem preservadas.

Sincronização da voz mantida conforme o preview aprovado, com alinhamento por pausas/frases, sem alinhamento fonético automático. Nenhuma pendência de render ou QA. Sem nova capa, publicação, commit ou push nesta rodada.

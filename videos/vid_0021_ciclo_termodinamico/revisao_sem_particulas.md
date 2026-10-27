# VID21 — entrega audiovisual para avaliação

Data: 2026-10-11. Série: EXERCÍCIO RESOLVIDO · EP. 07.

Cena ajustada à voz fornecida pelo usuário: 478 palavras em 167,76 s.
Preservados o gráfico, as contas, a direção didática e o visual 2D aprovado.
A expressão geral da área do triângulo aparece antes da substituição numérica.
Cabeçalho com série/episódio à esquerda e marca à direita; CTA somente
@labparallax, com degradê ciano → violeta → magenta.

## Arquivos alterados e gerados

- `cena.py`: entradas temporizadas pelo WAV e registro dos tempos reais.
- `ficha.md`, `narracao_sugestao.md` e `texto_narracao.txt`: documentação da voz em uso.
  Rascunhos anteriores preservados; `narracao_sugestao_v2.md` guarda a versão de 355 palavras.
- `audio/narracao_final.wav`: cópia idêntica da fonte, sem alterar velocidade ou duração.
- `gerar_sync.py`, `sync.json`, `alinhamento_palavras.json` e `legenda.srt`:
  marcos da voz e 64 legendas, com o texto integral e até duas linhas.
- `legenda_final.py` e `montar_final.py`: montagem da voz e legendas coloridas
  em faixa inferior, sem recortar ou redimensionar a cena.
- `qa_sincronia/`: verificação, relatório técnico e quadros de inspeção.

As alterações de identidade visual e refinamento do pistão já existentes foram
preservadas. Nenhuma dependência, template compartilhado ou vídeo anterior foi alterado.

## Renders e verificações

Preview: 540×960, 15 fps, CRF 23. Render de entrega: 1080×1920, 30 fps,
H.264/yuv420p, CRF 14. Master com vídeo copiado do Manim, sem recompressão;
legendado em CRF 14/preset medium. Voz AAC estéreo, 44,1 kHz, alvo 320 kb/s
(taxa medida 228,61 kb/s).

Master e legendado contêm 5032 quadros; vídeo de 167,7333 s e áudio de
167,76 s. Diferença final de 26,67 ms, menor que um quadro, sem cortar a fala.
Última legenda termina em 167,63 s.

Concluídos com sucesso:

- `py_compile` dos cinco scripts e `git diff --check`.
- Renders Manim preview e final; montagem de master e legendado nas duas resoluções.
- Decodificação integral dos quatro arquivos, conferência de PTS/CFR,
  resolução, fps, codec, formato de pixel e CRF gravado no stream.
- Hash dos pacotes: vídeo do master igual ao render; áudio do master igual ao legendado.
- SHA-256 do WAV igual à fonte:
  `ed910db013fe1dd85f9f6d9cc851f9479e2e4f9c12f66e2cac9cfe661fbf73ba`.
- Texto do SRT igual ao texto enviado; largura máxima 855,47 px em 1080p,
  dentro da faixa segura de 896 px. Fórmulas e resultados físicos conferidos.
- Entradas da cena verificadas em `timing_*.json`; atraso abaixo de 100 ms
  em relação aos marcos programados.
- Inspeção visual de 24 quadros por resolução, cobrindo todos os blocos,
  resultados, sinais, legendas, cabeçalho e CTA.

Evidências: `qa_sincronia/relatorio_tecnico.json`,
`qa_sincronia/verificacao_fontes.json`, `qa_sincronia/contato_final_*.jpg`,
`render_final.log` e `montagem_final.log`.

## Artefatos

Entrega reunida pelo comando `uv run python videos/entregar.py vid_0021` em:

`entregas/Exercício Resolvido - EP 07 - Ciclo termodinâmico - 0021/`

Contém master, legendado, SRT, áudio original, textos e manifesto com hashes.
Previews e intermediários permanecem na unidade em `renders/`,
`media_sincronizado/` e `media_final/`.

## Limitações e revisão pendente

Alinhamento obtido pelas pausas reais do WAV e interpolação silábica dos tempos
das palavras, sem ASR. As verificações de marcos medem a execução da cena;
não constituem confirmação auditiva independente de cada palavra.
Revisão humana contínua de voz, animação e legendas permanece pendente.

Teste do arsenal: não se aplica à integração nesta rodada. Mantido o 2D
explicitamente aprovado; nenhum sólido 3D foi integrado e não há custo de ponte.

Capa, publicação, commit e push não fazem parte desta entrega.

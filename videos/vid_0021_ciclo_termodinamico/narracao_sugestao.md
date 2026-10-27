# Narração em uso — VID21 · Exercício Resolvido · EP. 07

A voz e o texto atuais foram fornecidos pelo usuário na rodada de sincronização.
Substituem os rascunhos V1/V2: **478 palavras, WAV de 167,76 segundos**.
A média medida sobre o áudio inteiro é **170,96 palavras/minuto**, incluindo pausas;
não é uma medida da velocidade durante os trechos falados.

Texto efetivamente montado: `texto_narracao.txt`.
Áudio: `audio/narracao_final.wav`, cópia sem alteração do WAV fornecido.
Os rascunhos antigos permanecem em `narracao_sugestao_v1.md` e
`narracao_sugestao_v2.md`, para histórico; não são a transcrição do áudio atual.

## Sincronização

Foi reaproveitado o método local dos episódios recentes: pausas medidas por RMS,
limites de frase associados por programação dinâmica e palavras interpoladas
por peso silábico. Não foi executado reconhecimento de voz. Assim, os marcos de
frase têm suporte no WAV, enquanto os tempos internos de palavra são estimados.

- `alinhamento_palavras.json`: intervalos estimados das palavras.
- `sync.json`: entradas de bloco e resultados numéricos.
- `legenda.srt`: texto integral, dividido em 64 entradas de uma ou duas linhas.
- `timing_540x960.json` e `timing_1080x1920.json`: entradas medidas nos renders.
- `qa_sincronia/`: checagens, frames e relatório audiovisual.

A cena acompanha a nova fala com waits redistribuídos. O resultado físico e a
identidade aprovados permanecem: série/EP. 07 no topo esquerdo, marca no direito,
CTA somente com `@labparallax` em degradê. A fórmula da área é apresentada como
metade da base vezes a altura antes da substituição numérica.

A revisão humana da locução, das legendas e da sincronização segue pendente.
Não foi gerada nova voz, capa ou publicação.

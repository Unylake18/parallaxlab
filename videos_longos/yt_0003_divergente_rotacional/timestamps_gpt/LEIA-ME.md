# Como estes tempos foram gerados

- **Áudio:** 5 WAV do ElevenLabs (partes 1–5, 24:41 de fala), em `audio/partes/`; vídeo `preview_v3_1_com_voz.mp4` usa `audio/narracao_montagem.wav` (as 5 partes + 0,9 s entre elas + pausas extras de 1,43 s após G04, 0,48 s após P08 e 1,21 s após CTA02).
- **Não houve ASR.** Os tempos são ESTIMADOS: (1) mede-se no WAV os intervalos de silêncio (energia RMS < 0,03 por ≥ 0,12 s); (2) o fim de cada frase é ancorado numa dessas pausas por programação dinâmica que mantém o ritmo (sílabas/s) parecido entre frases; (3) vírgulas internas usam pausas quando existem; (4) as palavras de cada trecho são interpoladas por peso de sílabas.
- **O que é medido do áudio real:** `pausas_medidas_no_audio_s` (independente do texto). Os inícios/fim de frase vêm de combinar essas pausas com o texto; só são tão bons quanto o casamento pausa↔frase (verificação interna: 3 de 297 frases fora de ±30% do ritmo mediano; todos os 92 inícios de bloco caem após uma pausa).
- **O que é interpolado:** os instantes de cada palavra dentro de uma frase (erro típico de décimos de segundo).
- **Linha do tempo:** a do vídeo com voz (24:46). `evento_visual_s` = início da fala do bloco + 0,3 s, que é quando a cena dispara o primeiro evento do bloco (`self.ancora`).
- Arquivos: `frases_v3_1.srt/.vtt` (1 legenda por frase), `timestamps_v3_1.json` (pausas medidas, 92 âncoras, 4.120 palavras com bloco).
- Para confirmação independente seria preciso ASR/forced alignment (não disponível no ambiente do projeto).

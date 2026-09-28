# vid_0006 — Revisão e QA final

## Finais

| Arquivo | Vídeo | Frames | Duração | Áudio |
|---|---|---|---|---|
| `renders/vid_0006_cancelamento_ruido_final_master_limpo.mp4` (9.726.512 B) | H.264, 1080×1920, 30 fps | 3.166 | 105,53 s | AAC 44,1 kHz estéreo, 104,64 s |
| `renders/vid_0006_cancelamento_ruido_final_legendado.mp4` (9.111.798 B) | H.264, 1080×1920, 30 fps | 3.166 | 105,53 s | AAC 44,1 kHz estéreo, 104,64 s |

Reprodução, na raiz do repositório:

```powershell
uv run python -m manim -r 1080,1920 --fps 30 videos/vid_0006_cancelamento_ruido/cena.py CancelamentoRuido006
uv run python videos/montar_master.py media/videos/cena/1920p30/CancelamentoRuido006.mp4 videos/vid_0006_cancelamento_ruido/audio/narracao_final.wav renders/vid_0006_cancelamento_ruido_final_master_limpo.mp4
uv run python videos/montar_legendado.py renders/vid_0006_cancelamento_ruido_final_master_limpo.mp4 videos/vid_0006_cancelamento_ruido/legenda.srt renders/vid_0006_cancelamento_ruido_final_legendado.mp4 --color-module videos/vid_0006_cancelamento_ruido/cena.py
uv run python videos/vid_0006_cancelamento_ruido/gerar_capa.py
```

## Física

- Todas as curvas são calculadas pelas funções do modelo (`p_sum`, `noise`, `fone`,
  `residual`); a curva branca é sempre a soma, nunca desenhada à parte.
- Asserts no import de `cena.py`: pico da soma = 2A (φ = 0), √2 A (φ = π/2) e 0 (φ = π);
  colchete 2A|cos(φ/2)| igual ao pico da soma em nove valores de φ; residual 0,179A
  (g = 0,9, φ = 0,95π) e 0,105A (g = 0,95, φ = 0,97π).
- “= 0” só no modelo ideal (C6, com “CASO IDEAL”); a aplicação compara amplitudes
  (A_residual ≪ A_ruído) e o resíduo nunca chega a zero.
- No ar, as fileiras são deslocamento longitudinal (só movimento horizontal); p(t) só nos
  gráficos de pressão; a resultante espacial s₁ + s₂ é calculada.
- Arquitetura do fone apresentada como esquema conceitual.

## QA visual

Render 1080×1920/30 fps; margens verificadas pela própria cena (`check_safe_area`: nada
abaixo de y = −4,6 nem fora de |x| < 3,5) e pelo dry run da timeline. Folhas de frames
com a fala real sob cada frame (30 instantes) e amostra do legendado final em 1080p:
sem colisões, fórmulas legíveis, cores com significado fixo.

## QA de áudio

`audio/narracao_final.wav` intacta (sem corte, ganho ou normalização): fala de 0,05 a
104,45 s; pico −5,1 dBFS, sem clipping; nível estável (mediana −26,5 a −27,6 dB por
trecho de 16 s); maior pausa interna 0,34 s. Áudio presente e completo no master e no
legendado.

## QA de legenda

`legenda.srt`: 43 cues de 0,04 a 104,37 s, até duas linhas, linha mais larga 441 px
(limite 468 px do `montar_legendado.py`); quebras preferindo pontuação; tempos das
pausas medidas no áudio. Todas as 43 conferidas no legendado de prova 540p (frame no
meio de cada cue) e amostra no final 1080p; faixa da legenda abaixo do conteúdo.
Termos coloridos: ruído (ciano), onda magenta / outra contribuição (magenta),
processamento / mesmo atraso (violeta).

## Capa

`capa_instagram.png` (1080×1920), variante “a” do `gerar_capa.py`: “O SOM PODE /
CANCELAR O SOM?”; painel INTERFERÊNCIA → CANCELAMENTO DE RUÍDO com as mesmas funções
da cena (resíduo pequeno, não nulo). Conferida em tamanho cheio, médio e miniatura.

## Limitações reais

- Sincronia obtida por pausas do áudio, não por transcrição; conferida por amostras.
- Na miniatura muito reduzida (~180 px), rótulos do painel e linha da série da capa
  viram detalhe; headline, ondas e fone seguem legíveis.
- QA físico em celular, backup externo dos MP4s e URLs de publicação não registrados
  (publicado manualmente pelo usuário em 2026-09-28).

# vid_0005 — Revisão e QA final

## Finais

| Arquivo | Vídeo | Frames | Duração | Áudio |
|---|---|---|---|---|
| `renders/vid_0005_aceleracao_centripeta_final_master_limpo.mp4` (7.659.682 B) | H.264 High, 1080×1920, 30 fps, yuv420p | 3.840 | 128,0 s | AAC 44,1 kHz estéreo, 127,2 s |
| `renders/vid_0005_aceleracao_centripeta_final_legendado.mp4` (7.299.770 B) | H.264 High, 1080×1920, 30 fps, yuv420p | 3.840 | 128,0 s | AAC 44,1 kHz estéreo, 127,2 s |

Reprodução, na raiz do repositório:

```powershell
uv run python -m manim -r 1080,1920 --fps 30 videos/vid_0005_aceleracao_centripeta/cena.py AceleracaoCentripeta005
uv run python videos/montar_master.py media/videos/cena/1920p30/AceleracaoCentripeta005.mp4 videos/vid_0005_aceleracao_centripeta/audio/narracao_final.wav renders/vid_0005_aceleracao_centripeta_final_master_limpo.mp4
uv run python videos/montar_legendado.py renders/vid_0005_aceleracao_centripeta_final_master_limpo.mp4 videos/vid_0005_aceleracao_centripeta/legenda.srt renders/vid_0005_aceleracao_centripeta_final_legendado.mp4 --color-module videos/vid_0005_aceleracao_centripeta/cena.py
uv run python videos/vid_0005_aceleracao_centripeta/gerar_capa.py
```

## Matemática e física

- Instantes simétricos θ± = ±Δθ/2 (movimento anti-horário, instante central em θ = 0):
  v± = v(−sin θ±, cos θ±) ⇒ Δv = (−2v sin(Δθ/2), 0) = −|Δv| r̂(t): radial para dentro.
- |Δr| = 2R sin(Δθ/2) (corda, sem aproximação de arco) e |Δv| = 2v sin(Δθ/2):
  triângulos isósceles de mesmo Δθ, logo |Δv|/v = |Δr|/R para qualquer Δθ.
- Limite: |Δr|/Δt → |v| = v e |Δv|/Δt → a_c; logo a_c = (v/R)·v = v²/R.
- Na cena: |v| na tela fixo (`L_V`), v sempre tangente (calculado pelo ângulo da
  partícula), translação para a origem comum só por `shift`, Δθ do limite para em
  16° (nunca zero), fechamento com v ⊥ a_c e a_c apontando para O.
- Textos e fala nunca afirmam “velocidade constante”; usam “módulo da velocidade”.

## QA visual

Render 1080×1920/30 fps; margens verificadas pela própria cena (`check_safe_area`:
nada abaixo de y = −4,6 nem fora de |x| ≤ 3,5) e por varredura de todos os frames
do preview. Amostras em abertura, dois instantes, Δv, triângulos, limite,
fechamento e CTA: sem fórmula ou seta cortada, sem sobreposição relevante;
watermark discreto; texto em Space Grotesk Medium e matemática em MathTex.

## QA de áudio

`audio/narracao_final.wav` intacta (sem corte, ganho ou normalização): fala de
0,06 a 127,11 s; pico −3,6 dBFS, sem clipping; nível da fala estável
(mediana −23 a −25 dB por trecho de 16 s); maior pausa interna 0,71 s. Áudio
presente e completo no master e no legendado.

## QA de legenda

`legenda.srt`: 41 cues de 0,06 a 127,2 s, até duas linhas, todas dentro da
largura segura do `montar_legendado.py`; tempos das pausas medidas no áudio
(alinhamento por sílabas, sem ASR); faixa da legenda abaixo do conteúdo.

## Limitações reais

- Sincronia obtida por pausas do áudio, não por transcrição; conferida por
  amostras visuais.
- A narração gravada termina em “Se curtiu o conteúdo, siga o Parallax Lab”
  (duração do trecho compatível); a última cue do SRT diz “Se curtiu, siga o
  Parallax Lab.”. Mantido como publicado, por decisão do usuário.
- O @labparallax entra em 124,8 s, no início da frase do CTA.
- QA físico em celular, backup externo dos MP4s e URLs de publicação não registrados.

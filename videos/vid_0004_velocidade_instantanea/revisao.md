# Revisão — vid_0004

## Fechamento técnico — 2026-09-26

**Status técnico:** concluído. **Publicação:** manual, pelo usuário, em
2026-09-26 (Instagram, YouTube Shorts, TikTok e Facebook); URLs ainda não
registradas no repositório. Detalhes em `publicacao.md`.

**Matemática/física final verificada:**

- Modelo: x(t) = ½·a·t², com a = 2 m/s², x(0) = 0, v(0) = 0; instante t₀ = 2 s.
- x(2 s) = ½ · 2 · 2² = 4 m.
- Δx = a·t₀·Δt + ½·a·(Δt)², então v̄ = Δx/Δt = 4 m/s + (1 m/s²)·Δt, para Δt > 0.
- lim (Δt → 0) de Δx/Δt = dx/dt = v(t).
- v(t) = dx/dt = a·t, então v(2 s) = 4 m/s.

**Resumo:** 101,5 s; 1080×1920, 30 fps; áudio `audio/narracao_montagem.wav`
(99,93 s, derivado de `narracao_final.wav`); `legenda.srt` com 33 cues; capa
`capa_instagram.png`; finais listados abaixo.

**Finais locais** (`renders/`, fora do Git):

| Arquivo | Tamanho | Vídeo | Frames | Duração vídeo | Áudio |
| --- | ---: | --- | ---: | ---: | --- |
| `vid_0004_velocidade_instantanea_final_master_limpo.mp4` | 5.442.027 B | H.264 High, 1080×1920, 30 fps, yuv420p | 3.045 | 101,500 s | AAC 44,1 kHz estéreo, 99,93 s |
| `vid_0004_velocidade_instantanea_final_legendado.mp4` | 4.761.932 B | H.264 High, 1080×1920, 30 fps, yuv420p | 3.045 | 101,500 s | AAC 44,1 kHz estéreo, 99,93 s |

Comandos, na raiz:

```powershell
uv run python -m manim -r 1080,1920 --fps 30 videos/vid_0004_velocidade_instantanea/cena.py VelocidadeInstantanea004
uv run python videos/montar_master.py media/videos/cena/1920p30/VelocidadeInstantanea004.mp4 videos/vid_0004_velocidade_instantanea/audio/narracao_montagem.wav renders/vid_0004_velocidade_instantanea_final_master_limpo.mp4
uv run python videos/montar_legendado.py renders/vid_0004_velocidade_instantanea_final_master_limpo.mp4 videos/vid_0004_velocidade_instantanea/legenda.srt renders/vid_0004_velocidade_instantanea_final_legendado.mp4 --color-module videos/vid_0004_velocidade_instantanea/cena.py
```

**Fontes da unidade:**

- Áudio: fonte `audio/narracao_final.wav` (PCM 16 bits, 44,1 kHz, estéreo,
  101,68 s), intacta. Montagem `audio/narracao_montagem.wav` (99,93 s), gerada
  por `preparar_audio.py`: único tratamento é o corte na pausa da vírgula após
  “Segue o Parallax Lab”, com fade-out de 30 ms; “arroba labparallax” falado foi
  removido e o @ aparece só na tela. Sem aceleração, recorte interno ou ajuste
  de volume.
- Legenda: `legenda.srt`, 33 cues (0,10–100,11 s), até duas linhas, notação
  escrita (2 s, 4 m, 4 m/s); último cue “Segue o Parallax Lab.”. Cores por
  `SUBTITLE_TERM_COLORS` da cena (azul: média/secante; ciano: instantânea,
  tangente, derivada, 4 m/s; magenta: variação da posição; violeta: intervalo).
- Capa aprovada: `capa_instagram.png` (1080×1920), gerada por `gerar_capa.py`.
- Sincronia fala × tela: `roteiro.md`. Modelo e verificação: `ficha.md`.

**QA técnico:** os dois MP4s foram decodificados integralmente, sem erro:
3.045 frames e 4.407.296 amostras de áudio cada; pacotes de áudio idênticos
entre master e legendado. O áudio começa com a fala em 0,1 s, contém
“Segue o Parallax Lab” (~−20 dB entre 98,5 e 99,7 s) e termina em 99,94 s com
fade limpo (−72 dB); o vídeo segue 1,6 s no CTA. Vertical 1080×1920/30 fps.
As verificações de faixa segura da cena (`check_safe_area`, y > −4,6) passaram
no render final.

**QA visual** (frames em 6; 15; 31,5; 43,3; 51,5; 58; 64,5; 70,5; 76,5; 86;
92; 100,5 s): movimento inicial sincronizado com o gráfico; P = (2 s, 4 m);
secante com Q afastado, Δt violeta e Δx magenta no gráfico e na pista;
derivação de Δx; expressão de v̄; Q aproximando-se; secante quase tangente;
lim_{Δt→0} Δx/Δt = dx/dt; = v(t); v(2 s) = 4 m/s com seta ciano; síntese;
CTA “Segue o Parallax Lab / @labparallax”. Tangente ciano dominante; magenta
e violeta presentes. Legendas coloridas legíveis e abaixo de todo o conteúdo;
master sem legenda; watermark presente; capa não entra no vídeo. Recortes 1:1
sem serrilhado, clipping ou sobreposição.

**QA matemático/físico:** x(t) = ½at², a = 2 m/s²; x(2) = 4 m;
lim_{Δt→0} Δx/Δt = dx/dt = v(t); v(t) = at; v(2 s) = 4 m/s. Δt para em
`DT_MIN` = 0,02 s e `mean_velocity` rejeita Δt ≤ 0, então o quociente nunca é
avaliado em zero; a tangente exata (inclinação 4) substitui a secante.

**Limpeza de fechamento:** o preview legendado de 540×960 em `renders/` e os
renders/caches `VelocidadeInstantanea004` de `media/videos/cena/` (960p15 e
1920p30) foram removidos; regeneram-se pelos comandos acima.

**Pendências:** backup externo dos MP4s de `renders/` não confirmado; URLs
das publicações não registradas. Sincronia sem ASR: estimada pelas regiões de
fala medidas.

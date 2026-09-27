# vid_0004 — Velocidade em um instante

- Família interna: **Aplicação**. Série pública: **DA EQUAÇÃO AO FENÔMENO · EP. 01**.
- Tema: derivada como velocidade instantânea (secante → tangente enquanto Δt → 0).
- Cena: `cena.py`, classe `VelocidadeInstantanea004`.
- Formato: área lógica 9×16; preview 540×960/15 fps; final 1080×1920/30 fps.
- Narração: fonte `audio/narracao_final.wav` (101,68 s, intacta); montagem
  `audio/narracao_montagem.wav` (99,93 s), gerada por `preparar_audio.py`.
- Legenda: `legenda.srt` (33 cues), cores lidas de `SUBTITLE_TERM_COLORS` da cena.
- Capa: `capa_instagram.png`, gerada por `gerar_capa.py`.
- Roteiro e sincronia: `roteiro.md`. QA e finais: `revisao.md`. Publicação: `publicacao.md`.

## Modelo e verificação

x(t) = ½at², a = 2 m/s², x(0) = 0, v(0) = 0; instante t₀ = 2 s.

- x(2) = ½·2·2² = 4 m.
- Δx = x(t₀+Δt) − x(t₀) = ½a[(t₀+Δt)² − t₀²] = at₀Δt + ½a(Δt)².
- v̄ = Δx/Δt = at₀ + ½aΔt = 4 m/s + (1 m/s²)Δt, para Δt > 0.
  Referências: Δt = 2; 1; 0,5; 0,2; 0,02 s → 6; 5; 4,5; 4,2; 4,02 m/s.
- lim_{Δt→0} Δx/Δt = dx/dt = v(t) = at; v(2 s) = 4 m/s.
  Conferência independente: d/dt(t²) = 2t → 4 em t = 2 (eixos em s e m).

Na cena, Δt para em 0,02 s (`DT_MIN`) e `mean_velocity` rejeita Δt ≤ 0; a
tangente exata (inclinação 4) substitui a secante quase tangente.

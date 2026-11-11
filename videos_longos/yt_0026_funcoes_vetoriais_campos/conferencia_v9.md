# yt_0026 · conferência de tempo v9 (voz real × tela), 2026-11-10

- Voz: `audio/narracao_v4.wav`, 917.76 s contínuos (ElevenLabs v4, voz `qw7jgPZWOKrl10GsjQ82`, 4 blocos de API emendados sem silêncio inserido); alinhamento forçado palavra a palavra (`alinhamento_palavras.json`, perda média 0,61); transcrição de conferência (STT) sem tag lida e sem palavra pulada.
- `ancoras.json` regenerado pela voz (`gerar_ancoras.py`): âncora começa 0,15 s antes da 1ª palavra e termina no início da seguinte; CTA termina 1 s depois do fim do WAV.
- Render v9: 921.7 s com B7 (a cena do CTA segura 3 s de logo depois da última âncora). Deriva entre seções: 0,00 s em todos os lotes.
- Gatilhos: 140, maior atraso +0.19 s (portão ≤ 0,2 s). T5 e B6-5 conferidos.
- Nenhuma âncora com animação mais longa que a fala (nenhum `[estouro]`).
- "Tela parada > 3 s" = nenhum pixel muda (detector `qa_parado.py`, 960×540). Comparação: preview v8 aprovado tinha 91 trechos (534 s); v9 tem 68 trechos (374 s), porque a voz é mais rápida que o nominal. Esticado no v9: A1 (anéis do logo giram até o título; antes 12,5 s parados).

| âncora | voz (s) | nominal v8 (s) | render v9 (s) | gatilhos | maior atraso (s) | tela parada > 3 s |
|---|---:|---:|---:|---:|---:|---|
| T0 | 9.85 | 10.13 | 9.87 | 1 | -0.00 | 1× · 4.3 s |
| T1 | 7.80 | 9.39 | 7.80 | 2 | +0.00 | — |
| T2 | 7.40 | 9.76 | 7.40 | 1 | -0.03 | — |
| T3 | 5.98 | 7.17 | 5.93 | 0 | +0.00 | — |
| T4 | 16.98 | 20.87 | 17.00 | 6 | +0.02 | — |
| T5 | 7.70 | 8.28 | 7.73 | 3 | -0.01 | 1× · 3.9 s |
| A1 | 38.32 | 49.02 | 38.27 | 3 | +0.03 | 3× · 18.7 s |
| H1 | 17.86 | 23.46 | 17.87 | 2 | +0.02 | 1× · 10.8 s |
| H2 | 15.42 | 19.02 | 15.47 | 1 | -0.03 | 2× · 11.5 s |
| H3 | 16.46 | 20.87 | 16.47 | 2 | +0.15 | 1× · 7.6 s |
| B1-1 | 18.54 | 23.83 | 18.53 | 2 | -0.01 | 1× · 7.0 s |
| B1-2 | 42.22 | 50.13 | 42.20 | 4 | +0.02 | 3× · 25.7 s |
| B1-3 | 21.70 | 26.06 | 21.67 | 6 | +0.19 | 1× · 4.3 s |
| B1-4 | 16.70 | 20.87 | 16.73 | 3 | +0.03 | 2× · 8.7 s |
| B2-1 | 18.48 | 21.24 | 18.47 | 3 | +0.03 | 3× · 12.8 s |
| B2-2 | 22.86 | 27.54 | 22.87 | 3 | +0.03 | 2× · 8.1 s |
| B2-3 | 16.54 | 19.39 | 16.53 | 3 | +0.02 | 2× · 7.1 s |
| B2-4 | 22.08 | 28.28 | 22.07 | 4 | +0.02 | 1× · 5.5 s |
| B2-5 | 13.62 | 16.06 | 13.67 | 3 | +0.02 | — |
| B2-6 | 21.24 | 26.80 | 21.20 | 4 | +0.03 | 2× · 6.2 s |
| B2-7 | 23.88 | 28.28 | 23.87 | 3 | +0.01 | 2× · 16.3 s |
| B3-1 | 11.40 | 12.35 | 11.40 | 1 | +0.03 | 1× · 4.0 s |
| B3-2 | 23.76 | 25.31 | 23.80 | 4 | +0.02 | 1× · 7.7 s |
| B3-3 | 11.20 | 14.57 | 11.20 | 3 | +0.01 | 1× · 3.7 s |
| B3-4 | 24.22 | 26.80 | 24.20 | 4 | +0.02 | 2× · 11.0 s |
| B3-5 | 24.72 | 29.39 | 24.73 | 4 | +0.02 | 2× · 9.9 s |
| B3-6 | 28.00 | 33.09 | 28.00 | 5 | +0.01 | 3× · 11.7 s |
| B4-1 | 15.78 | 17.91 | 15.80 | 1 | +0.01 | 1× · 7.7 s |
| B4-2 | 12.54 | 15.69 | 12.53 | 3 | +0.01 | 1× · 5.7 s |
| B4-3 | 20.76 | 22.72 | 20.73 | 2 | +0.00 | 2× · 15.0 s |
| B5-1 | 30.72 | 37.91 | 30.73 | 4 | +0.03 | 3× · 15.1 s |
| B5-2 | 25.28 | 27.17 | 25.27 | 5 | -0.01 | 2× · 9.8 s |
| B5-3 | 35.64 | 34.94 | 35.67 | 7 | +0.03 | 3× · 13.2 s |
| B5-4 | 16.84 | 18.65 | 16.80 | 3 | +0.03 | 1× · 5.1 s |
| B6-1 | 18.54 | 22.35 | 18.53 | 3 | +0.03 | 1× · 6.8 s |
| B6-2 | 16.06 | 18.65 | 16.07 | 5 | +0.02 | 1× · 4.3 s |
| B6-3 | 17.10 | 19.76 | 17.13 | 2 | +0.03 | 2× · 7.2 s |
| B6-4 | 27.98 | 27.54 | 28.00 | 4 | +0.03 | 2× · 12.4 s |
| B6-5 | 24.30 | 28.28 | 24.27 | 3 | +0.02 | 2× · 6.5 s |
| B6-6 | 22.34 | 26.06 | 22.33 | 2 | +0.03 | 1× · 10.4 s |
| B6-7 | 20.64 | 26.43 | 20.67 | 4 | +0.03 | 1× · 5.0 s |
| B7-1 | 16.56 | 19.76 | 16.53 | 2 | +0.01 | — |
| B7-2 | 15.36 | 19.02 | 15.40 | 2 | +0.01 | — |
| S1 | 31.04 | 31.98 | 31.00 | 5 | +0.01 | 3× · 16.5 s |
| S2 | 21.60 | 24.20 | 21.60 | 2 | -0.01 | 3× · 18.0 s |
| CTA | 24.75 | 30.87 | 27.73 | 1 | +0.00 | 1× · 8.3 s |

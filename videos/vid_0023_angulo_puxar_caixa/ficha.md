# Qual o melhor ângulo para puxar uma caixa?

- id: vid_0023
- formato: curto_vertical
- Série pública: **EXERCÍCIO RESOLVIDO · EP. 7** (confirmado pelo usuário; aplicar a tag "EP. 7" no render final)
- fase: V5 (preview silencioso 540×960 / 15 fps, 154,5 s) — narração sugerida em `narracao_sugestao_v5.md`; falta voz, legenda, cartão final (@labparallax pequeno em degradê padrão + "siga o Parallax Lab") e render final
- implementação atual: `cena_v5.py` — `AnguloPuxarCaixa023V5` (V1–V4 preservadas)
- solido_3d: nenhum
- justificativa de solido_3d: forças, decomposição e gráfico são melhor explicados em 2D/Manim.

## Modelo

F(θ) = μ_s m g / (cos θ + μ_s sin θ); no limiar: N = mg − F sin θ, f_s,max = μ_s N, F cos θ = f_s,max.
Ótimo: tan θ_ideal = μ_s.

Exemplo: m = 20 kg, μ_s = 0,5, g = 9,8 m/s² → θ_ideal = 26,565°, F(0) = 98 N, F_min = 87,654 N (≈ 10,56 % menos).
Conferência: N = 156,8 N; f_s,max = 78,4 N = F_min cos θ_ideal.

Terminologia: nunca "o atrito diminui" em geral; inclinar reduz N e, portanto, o valor máximo do atrito estático no limiar.

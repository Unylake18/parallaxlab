# HANDOFF v1 — yt_0016 "Momento em sistemas" (preview silencioso v1, Parte 2 de 2 do 4.9)

Cópia de trabalho do handoff recebido em 2026-10-27 (o Anexo A, narração v1, está em `narracao_sugestao.md`).

## 0. Contexto e ordem de trabalho
- Passo 0: conferir que C09–C13 do yt_0015 (conservação em sistemas, gelo, caçador, gases do rifle, Newton e a luz, mais o tanque de água em Three.js)
  estão em `videos_longos/yt_0015_momento_impulso/_reservado_yt0016/` e fora do preview do yt_0015. Não mexer no yt_0015.
- Unidade nova: `videos_longos/yt_0016_sistemas_momento/` (irmã do yt_0015, mesmo worktree).
- Série do 4.9: yt_0015 uma partícula → yt_0016 sistemas (este) → yt_0017 centro de massa → yt_0018 foguete.
- Teoria (T7–T10) antes dos exercícios (E6–E9), selo DICA em cada bloco, nenhuma pessoa em linhas.

## 1. Rodada
Preview silencioso v1 960×540 / 15 fps, do hook ao CTA. Sem voz, SRT, master, entrega, commit ou push. Não alterar `template/`, `docs/`, `assets/`
nem `experimentos/threejs/`. Duração esperada ~19–20 min. Reaproveitar helpers, header, cores, DICA, selo de fonte, transições em fade, manequim
(ou plano B), blocos reservados de E6–E9 só como ponto de partida.

## 2. Ficha — ver `ficha.md`.

## 3. Física congelada (g = 9,8 m/s²; +x à direita, +y para cima)
- T7: dp⃗ᵢ/dt = Σⱼ F⃗ᵢ₍ⱼ₎ + F⃗ᵢ^ext → dP⃗/dt = ΣᵢΣⱼ F⃗ᵢ₍ⱼ₎ + F⃗^ext → dP⃗/dt = F⃗^ext. Binário. Por componente. Campo: só linha qualitativa.
- T8: cavalo 600 kg, pedra 800 kg, μ_c = 0,3: f_pedra = 2.352 N; f_c = 2.800 N (μ_e ≥ 0,48); a = 448/1.400 = 0,32 m/s²; T = 2.608 N; cavalo 192 N.
  Gelo sob as patas (μ_e ≈ 0,1): f_c,máx = 588 N. Cyrano: só forças internas.
- T9: bola 1 kg, 10 m, v = 14,0 m/s; Terra 2,3×10⁻²⁴ m/s. Blocos 1 kg e 2 kg, μ = 0,2: v₁ = −2, v₂ = +1 m/s; atrito +1,96 N e −3,92 N; resultante
  −1,96 N; P(t) = −1,96 t até t₂ = 0,510 s (P = −1,0); P(t) = −(2,0 − 1,96 t) até t₁ = 1,020 s (P = 0); leve 1,02 m, pesado 0,255 m; P_Terra = −P.
- T10: K₁/K₂ = m₂/m₁; K = 2 J e 1 J; fração 2/3 (67%); iguais 50%.
- E6 (Sears 8.20): 0,0850 m/s; 0,154 m/s; 30 J → 0,25 J (≈ 29,7 J calor); → ≈ 20,0 J (19,2 + 0,83).
- E7 (Sears 8.25): 0,0559 m/s; a 56°: 0,0313 m/s; K_bala 1.956 J; K_caçador 0,113 J; razão ≈ 17.262; ≈ 99,994% na bala.
- E8 (Sears 8.17): 599,15 m/s; p_bala 4,31; p_rifle −5,18; p_gases +0,866 kg·m/s.
- E9 (Moysés 9.2): impulso normal; θ₁′ = θ₁; v₁ sen θ₁ = v₂ sen θ₂; constante = v₂/v₁ no modelo de Newton (nunca "= n₁₂"); Foucault 1850.
  Ondulatória: sen θ₁/sen θ₂ = v₁/v₂. Referência: n = 1,33, 45° → 32,1°.
- Coda: p = E/c; Sol 1.361 W/m²: 4,5 μPa / 9,1 μPa; vela 100 m²: ≈ 0,9 mN; laser 1 W: 3,3 nN; preta F, espelho 2F.

## 4. Tela — capítulos (linha 2)
T7 SISTEMAS DE PARTÍCULAS · T8 FORÇA INTERNA NÃO MOVE O SISTEMA · T9 ESCOLHER O SISTEMA · T10 COMO A ENERGIA SE DIVIDE ·
E6 EXERCÍCIO 6 · AGARRAR OU REBATER · E7 EXERCÍCIO 7 · O CAÇADOR NO LAGO · E8 EXERCÍCIO 8 · OS GASES DO RIFLE · E9 EXERCÍCIO 9 · NEWTON E A LUZ ·
Coda A LUZ TAMBÉM TEM MOMENTO · Síntese RESUMO. Selos de fonte: MOYSÉS §8.1–8.3, SEARS · EX. 8.20, SEARS · EX. 8.25, SEARS · EX. 8.17,
MOYSÉS · PROB. 9.2, FEYNMAN §10-5 (~20, DIM, op. 0,6). DICA no fim de T7-5, T8-8, T9-7, T10-4, E6-4, E7-5, E8-4, E9-7. Fade ~0,4 s entre capítulos.

## 5. Direção por bloco — ver o handoff original (resumo): cavalo 2D preenchido com patas articuladas; matriz de pares 3×3; binário no disco;
fronteira tracejada sempre; gelo azulado só sob as patas; Cyrano leve; blocos com mola e gráficos P(t) e P_Terra(t); barras de momento e energia;
duas colunas AGARRA × REBATE; normal do gelo no tiro a 56° e barras log; rifle com referenciais rotulados e nuvem de gases; retrato estilizado,
espelho e ar→água com componentes; feixe em preto × espelho; síntese com o cavalo; CTA com granada.

## 6. Render mínimo e QA
Preview por lotes; stills 1920×1080: H1, T7-4, T8-5, T9-6, E7-5, E9-4. QA físico e de forma conforme o handoff (matriz, números do T8, P(t),
fronteira sempre, E7 normal, E8 referenciais, E9 sem "= n₁₂", DICA idênticas, sem sobreposição, sem stick figure).

## 7. O que não fazer
Sem voz/SRT/master/legendado/entrega; não alterar yt_0015, `template/`, `docs/`, `assets/`, `experimentos/threejs/`; sem commit/push; não
acrescentar nem cortar blocos; não repetir a derivação de dois corpos do yt_0015.

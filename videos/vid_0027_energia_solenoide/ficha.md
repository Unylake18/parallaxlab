# Energia de um solenoide

- ID: `vid_0027`
- Série pública: **EXERCÍCIO RESOLVIDO · EP. 10**
- formato: `curto_vertical`
- solido_3d: nenhum, porque o corte longitudinal, o disco de fluxo, a replicação das espiras e o volume aceso são mais didáticos em Manim 2D (decisão do briefing).
- Headline: “ONDE FICA A ENERGIA DE UM INDUTOR?”
- Fase: preview visual silencioso, 540×960 / 15 fps. Sem voz, SRT, master, legendado ou entrega.
- Física e storyboard: handoff de Produção (vid_0027, 10 beats C01–C10), física congelada pelo Kaio.
- Sem exemplo numérico no vídeo. End card silencioso: somente `@labparallax`.

## Física (congelada)

Solenoide muito longo, raio a, n espiras por metro, corrente I, núcleo de ar, trecho h longe das extremidades; A = πa², N = nh.

- Ampère: Bℓ = μ₀(nℓ)I ⇒ B = μ₀nI dentro; B fora ≈ 0.
- Fluxo: Φ = BA = μ₀nIπa²; NΦ = μ₀n²Iπa²h (fluxo concatenado).
- Indutância: L = NΦ/I = μ₀n²πa²h.
- Rota do circuito: U_B = ½LI² = ½μ₀n²πa²hI².
- Rota do campo: u_B = B²/(2μ₀), V = πa²h, U_B = u_B V = ½μ₀n²πa²hI².

Conferência (só QA): n = 1000/m, a = 1 cm, h = 1 m, I = 1 A ⇒ L ≈ 0,395 mH; U_B ≈ 1,97·10⁻⁴ J nas duas rotas.

## Cores

I verde `#3FE08B` · B, Φ, NΦ, U_B, u_B magenta `#EA63FF` · a, h, A, V, n GEO `#B8C4DA` · L, N, números brancos ·
espiras aço `#7A8696` · texto secundário `#8FA3C4`.

## Convenções

Eixo horizontal, B → +x dentro. Corte longitudinal (meia seção de trás): parede superior ⊙, inferior ⊗; na meia
volta de trás a corrente sobe (traços verdes). Laço amperiano anti-horário na tela: lado interno em +x, externo em −x.

## Preview

`uv run --no-sync python -m manim -ql -r 540,960 --fps 15 videos/vid_0027_energia_solenoide/cena.py EnergiaSolenoide027`
(`MEDIA_DIR` padrão: `videos/vid_0027_energia_solenoide/media`).

## Teste do arsenal

Não utilizado (decisão do briefing).

## Versões do preview

- v1 (`cena_v1.py`): solenoide deitado, 126 s; fórmulas já nasciam na forma particular.
- v2 (`cena_v2.py`): solenoide em pé, três estágios por grandeza, 222 s; recusada (poluída, longa).
- v3 (`cena.py`, atual): solenoide deitado e maior (9 espiras), três estágios com tela limpa (forma geral + passo atual +
  uma linha de nota), texto de tela em MAIÚSCULAS Space Grotesk e definições em MathTex minúsculo; 175,1 s.
  Preview: `renders/vid_0027_preview_v3_540x960.mp4`.

## Versão final (2026-10-26)

- Narração: `narracao_tags_v4.md` (revisão do GPT; sem bem-vindos, CTA "Se curtiu, siga o Parallax Lab."), voz
  `qw7jgPZWOKrl10GsjQ82`, modelo `eleven_v4`, com tags. Áudio `audio/narracao_v4.wav` = `audio/narracao_final.wav` (159,8 s).
- Sincronia: `alinhar_voz.py` (forced alignment) → `gerar_ancoras.py` (66 âncoras, uma por frase) → `MEDIR=1 --dry_run`
  (`nat.json`) → `plan_sync.py` (`sync.json`; LEAD 0,10 s, f ∈ [0,4; 1,8]) → render com `SYNC=sync.json`. A imagem chega
  0,07–0,11 s antes da voz em todas as âncoras; esperas "respiram" (sem tela parada).
- Master: `renders/vid_0027_postagem_master.mp4` (1080×1920, 30 fps, CRF 14, 161,5 s).
- Legenda: `legenda.srt` (73 blocos, `gerar_legenda.py 32`, linhas balanceadas) e legendado
  `renders/vid_0027_postagem_legendado.mp4` (`videos/montar_legendado.py` + `cores_legenda.py`, CRF 14).
- Entrega: `entregas/Exercício Resolvido - EP 10 - Energia de um solenoide - 0027/`.

---
name: projeto-teste-coaxial-blender
description: Experimento isolado "coaxial 3D" (Blender → PNG alpha → Manim) em experimentos/blender/teste_gauss_coaxial/, v1 e v2
metadata:
  type: project
---

Experimento paralelo (2026-10-07), fora do `yt_0002`: cabo coaxial montado no Blender (casca oca com cunha, núcleo sólido, cargas só nas superfícies, câmera ortográfica 3/4, gaussiana que cresce, setas ∝ 1/r no vão) com Manim só para texto, fórmulas, gráfico e corte 2D. v1 = `render_sequencia.py` + `cena_manim.py`; v2 = `*_v2.py` (mais legível). Sequências em `renders/teste_gauss_coaxial[_v2]/1120x784/` (ignoradas pelo Git); previews em `media/teste_blender_coaxial/` (pasta própria).

**Why:** o usuário quer testar Blender como cena 3D principal sem tocar no vídeo de 18 min; veredito v1 "encaixou com ajustes".

**How to apply:** validar primeiro `--estados` (3 quadros, ~2 s) antes da sequência de 90 quadros (~1 min, 0,65 s/quadro); `Text` do Manim não tem glifos gregos (λ só em MathTex); outra sessão apaga `media/videos/cena` (use `--media_dir` próprio); não alterar o arsenal nem o `cena.py` do yt_0002. Ver [[projeto-yt0002-gauss]].

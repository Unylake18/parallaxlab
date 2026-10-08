# Coaxial 3D + corte 2D ampliado, com setas que acompanham a gaussiana

Experimento paralelo (não altera yt_0002, arsenal, template nem os outros experimentos). Parte do `preview_coaxial_3d_limpo/` (a trajetória de r é a mesma).

**Vídeo:** `saida/Coaxial3D2D_540p30.mp4` (12,3 s, 960×540, 30 fps, sem áudio).

1. Quadros do Blender, nos instantes reais (148 imagens, ~65 s, em `renders/preview_coaxial_3d_2d/`, ignorado pelo Git): `blender.exe -b -P experimentos\blender\preview_coaxial_3d_2d\render_3d2d.py` (`-- --estados` valida)
2. Preview: `uv run python -m manim -r 960,540 --fps 30 --media_dir media/preview_coaxial_3d_2d experimentos/blender/preview_coaxial_3d_2d/cena_3d2d.py Coaxial3D2D`

O que mudou em relação ao coaxial limpo:
- **Campo avaliado no 3D (Blender):** com a gaussiana no vão, 4 anéis de setas radiais nascem na própria superfície gaussiana (planos x = ±0,35 e ±1,05, 4 setas por anel, só em ângulos visíveis pela janela do corte),
  com |E| ∝ 1/r (as setas se afastam do eixo e encurtam; comprimento limitado para não furar a casca). Fora do vão (E = 0) elas somem.
- **Campo existente:** as 4 setas discretas do vão ficam sempre; em destaque quando a gaussiana está fora do vão, mais discretas enquanto o anel de setas está visível.
- **Corte 2D ampliado (Manim):** núcleo, casca, sinais, a, b, r, gaussiana, 8 setas do campo existente e um anel de 12 setas na gaussiana (∝ 1/r), tudo do mesmo r(k) do Blender e do texto.
- **Recorte da casca:** 125° (a casca mantém ~65% da circunferência) para a janela mostrar mais setas.
Sem gráfico. Limitações: ver o relatório da rodada (setas encobertas pelas bordas da casca; 3D denso logo após r = a).


## Variante com coroas (`Coaxial3D2DCoroa`)

Mesmo corte 2D e mesma trajetória; no 3D os anéis de setas são trocados por duas coroas de setas planas (frente completa, fundo só por fora) e o campo existente do vão some enquanto a gaussiana está nele. A versão original acima permanece intacta.

```bash
blender.exe -b -P experimentos/blender/preview_coaxial_3d_2d/render_3d2d.py -- --coroa      # quadros em renders/preview_coaxial_3d_2d/1120x784_coroa
uv run python -m manim -r 960,540 --fps 30 --disable_caching --media_dir media/preview_coaxial_3d_2d_coroa experimentos/blender/preview_coaxial_3d_2d/cena_3d2d.py Coaxial3D2DCoroa
```
Saída: `saida/Coaxial3D2D_coroa_540p30.mp4`.

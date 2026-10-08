# Coaxial: apresentação 3D breve + corte 2D grande (teste de clareza)

Experimento paralelo (não altera yt_0002, arsenal, template nem os outros experimentos). Compara com `preview_gauss_refinado/`.

**Vídeo:** `saida/CoaxialCorte2D_540p30.mp4` (14,1 s, 960×540, 30 fps, sem áudio).

1. Quadro 3D (só ele vem do Blender, sem setas, halos nem gaussiana; ~2 s): `blender.exe -b -P experimentos\blender\preview_coaxial_corte2d\render_apresentacao.py` → `renders/preview_coaxial_corte2d/apresentacao.png`
2. Preview: `uv run python -m manim -r 960,540 --fps 30 --media_dir media/preview_coaxial_corte2d experimentos/blender/preview_coaxial_corte2d/cena_coaxial_corte2d.py CoaxialCorte2D`

Ordem da explicação: 3D (condutores e vão) → corte 2D com + azul e − magenta → 8 setas radiais iguais no vão (sempre visíveis) → gaussiana tracejada
animada por um ValueTracker (r<a, a<r<b, r>b) com região, Q_env e E(r) trocando de forma discreta em a e b. L fixo, perpendicular ao corte; sem gráfico.
Os sinais são marcadores esquemáticos, não uma contagem de cargas.

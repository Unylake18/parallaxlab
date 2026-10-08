# Coaxial 3D limpo (3D permanente + gaussiana animada no Blender)

Experimento paralelo (não altera yt_0002, arsenal, template nem os outros experimentos).

**Vídeo:** `saida/CoaxialLimpo_540p30.mp4` (12,3 s, 960×540, 30 fps, sem áudio).

1. Quadros do Blender, nos instantes reais da animação (148 imagens únicas, ~66 s, 104 MB em `renders/preview_coaxial_3d_limpo/`, ignorado pelo Git):
   `blender.exe -b -P experimentos\blender\preview_coaxial_3d_limpo\render_limpo.py`   (validação rápida: `-- --estados`)
2. Preview: `uv run python -m manim -r 960,540 --fps 30 --media_dir media/preview_coaxial_3d_limpo experimentos/blender/preview_coaxial_3d_limpo/cena_limpo.py CoaxialLimpo`

`trajetoria.py` define r(t) uma única vez (intro, pausas e duas passagens por a e b, 327 quadros); o Blender renderiza um quadro por instante em movimento
e um por pausa; o Manim escolhe a imagem pelo tempo da cena e a região/Q_env/E(r) a partir do mesmo r. Sem dissolução entre imagens.
Cargas: poucos símbolos + (azul, núcleo) e − (magenta, face interna da casca), esquemáticos. Campo: 4 setas radiais iguais num plano transversal do vão,
sempre visíveis. Casca externa ideal em b; recorte só ilustrativo.

# Todos os casos de Gauss no padrão do coaxial limpo (3D permanente + gaussiana no Blender)

Experimento paralelo (não altera yt_0002, arsenal, template nem os outros experimentos). Mesmo padrão do `preview_coaxial_3d_limpo/`, aplicado aos 10 casos
restantes do vídeo principal; o coaxial entra com o vídeo já aprovado.

**Vídeos** (`saida/`, 960×540, 30 fps, sem áudio): `TODOS_limpo_540p30.mp4` (136,1 s, os 11 casos em sequência) e um MP4 por caso (`01_linha` … `11_cap_esf`, ~12,3 s cada).
Ordem: linha, casca cilíndrica, cilindro maciço, coaxial, folha, placa, duas folhas, face de condutor, casca esférica, esfera maciça, capacitor esférico.

## Como renderizar (a partir da raiz do repositório)

1. Quadros do Blender, nos instantes reais (148 imagens por caso, ~1,1 GB no total em `renders/preview_todos_limpo/`, ignorado pelo Git):
   `blender.exe -b -P experimentos\blender\preview_todos_limpo\render_todos.py -- --caso todos`   (validar: `-- --caso todos --estados`; um caso: `--caso casca_esf`)
2. Manim, um caso por vez (pasta de mídia própria): `uv run python -m manim -r 960,540 --fps 30 --media_dir media/preview_todos_limpo/<caso> experimentos/blender/preview_todos_limpo/cena_todos.py <Classe>`
   (LinhaLimpo, CascaCilLimpo, MacicoCilLimpo, FolhaLimpo, PlacaLimpo, DuasLimpo, FaceLimpo, CascaEsfLimpo, MacicoEsfLimpo, CapEsfLimpo)
3. Juntar: `uv run python experimentos/blender/preview_todos_limpo/juntar.py`

Arquivos: `traj_gen.py` (trajetória e waypoints por caso, lida pelos dois lados), `render_todos.py` (Blender), `cena_todos.py` (Manim), `juntar.py`.

## O que cada caso tem (igual ao coaxial limpo)

3D permanente com câmera ortográfica fixa; poucos símbolos + (azul) e − (magenta) nas superfícies/volume certos; 4 a 6 setas de campo iguais num único plano (cilindros: plano
transversal; esferas: plano perpendicular à câmera; planos: grade perpendicular às folhas); gaussiana fantasma (cilindro, esfera ou pillbox) que varia só um parâmetro p, renderizada em
cada instante do vídeo (um quadro por instante em movimento, um por pausa, sem dissolução); Manim só com título, região, Q_env, E(r), uma nota curta e a legenda de R, r, a, b…

## Limitações

Setas fixas e poucas; nos planos (folha, placa, duas folhas, face) o painel finito é só ilustrativo; folha/placa/face ficam menores no quadro que as esferas; algumas setas se
sobrepõem a símbolos na projeção; a gaussiana planar (pillbox) tem tampa esquerda tracejada; conferido por quadros extraídos, não por reprodução contínua; sem 1080p, sem áudio.

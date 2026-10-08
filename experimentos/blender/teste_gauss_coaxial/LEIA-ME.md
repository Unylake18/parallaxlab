# Teste: cena 3D montada no Blender (coaxial + gaussiana) com texto em Manim

Sandbox, fora do `yt_0002` e sem alterar o arsenal (só importa seus construtores). Nada aqui entra em vídeo sem handoff.

1. Sequência 3D (Blender, ~1 min, `renders/` é ignorado pelo Git):
   `"C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" -b -P experimentos\blender\teste_gauss_coaxial\render_sequencia.py -- --frames 90 --res 1120x784`
2. Preview Manim (960x540, 15 fps, 23 s), em pasta própria para não colidir com `media/videos/cena`:
   `uv run python -m manim -r 960,540 --fps 15 --media_dir media/teste_blender_coaxial experimentos/blender/teste_gauss_coaxial/cena_manim.py TesteCoaxial3D`

O quadro 3D (raio da gaussiana), o texto da região, Q_env, E(r) e o marcador do gráfico seguem o mesmo `ValueTracker`.

## v2 (clareza física)

Casca externa oca com corte de 104° (~71% da circunferência, espessura e arestas visíveis), núcleo sólido, cargas só nas superfícies
(+λ no núcleo, −λ na face interna da casca), câmera ortográfica 3/4 fixa, gaussiana "fantasma" (vidro violeta, aros contínuos, duas guias
tracejadas), três setas de E no vão com comprimento ∝ 1/r (somem em r < a e r > b), holofote por região (brilho e opacidade do núcleo) e
um corte transversal 2D sincronizado no Manim.

1. Validar só os três estados (2 s): `blender.exe -b -P experimentos\blender\teste_gauss_coaxial\render_sequencia_v2.py -- --estados --saida renders\teste_gauss_coaxial_v2\_estados`
2. Sequência (90 quadros, ~1 min): `blender.exe -b -P experimentos\blender\teste_gauss_coaxial\render_sequencia_v2.py -- --frames 90 --res 1120x784`
3. Preview: `uv run python -m manim -r 960,540 --fps 15 --media_dir media/teste_blender_coaxial experimentos/blender/teste_gauss_coaxial/cena_manim_v2.py TesteCoaxial3Dv2`

`cena_manim_v2.py` importa helpers de `cena_manim.py` (v1), que fica intacto.

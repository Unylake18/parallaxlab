# Preview refinado: coaxial, duas folhas e esfera maciça (Blender + Manim)

Experimento paralelo, fora do `yt_0002` (nada do vídeo principal, de `preview_gauss_padronizado/`, de `teste_gauss_coaxial/` ou do arsenal
foi alterado; o que vem deles é só importado).

**Vídeo:** `saida/PreviewGaussRefinado_540p15.mp4` (38,9 s, 960×540, 15 fps, sem áudio).

## Como renderizar (a partir da raiz do repositório)

1. Validar 3 estados por caso (poucos segundos): `blender.exe -b -P experimentos\blender\preview_gauss_refinado\render_refinado.py -- --caso todos --estados`
2. Sequências (124 quadros, ~85 s, 83 MB em `renders/preview_gauss_refinado/`, ignorado pelo Git): `... render_refinado.py -- --caso todos`
3. Preview: `uv run python -m manim -r 960,540 --fps 15 --media_dir media/preview_gauss_refinado experimentos/blender/preview_gauss_refinado/cena_refinado.py PreviewGaussRefinado`

Arquivos: `casos_ref.py` (parâmetros), `render_refinado.py` (Blender), `cena_refinado.py` (Manim).

## Princípios aplicados (candidatos a padrão)

- **Sinal sempre legível:** + azul claro, − magenta. A carga em Q_env ganha um halo violeta pequeno e fica um pouco maior; a cor do sinal não muda.
- **Campo existente × avaliado:** o campo que existe fisicamente fica sempre visível e discreto (coaxial: setas no vão mesmo com r > b);
  quando a região avaliada é a dele, as setas sobem de brilho. Onde E = 0 na avaliação, nada é inventado.
- **Setas 3D comuns:** mesma malha e espessura, direções distribuídas de forma sistemática (6 ângulos por fatia; grade regular; fibonacci na esfera),
  comprimento = módulo (mesmo raio → mesmo comprimento) e oclusão preservada.
- **Gaussiana fantasma:** preenchimento quase invisível, contorno da frente contínuo, traseira e guias tracejadas.
- **Enquadramento por caso:** cada geometria define o próprio zoom (esfera com r_max = 1,5 R; coaxial e folhas com margem pequena).
- **Papéis:** Blender = sólido, cargas, gaussiana, setas de campo; Manim = fórmulas, regiões, Q_env, gráfico, cortes e esquemas 2D.

## Física conferida

Coaxial: E = 0 em r < a e r > b, E = λ/(2πε₀ r) no vão. Duas folhas: E₊ e E₋ somam entre elas (σ/ε₀) e se cancelam fora; o zero fora vem da
superposição, não de Q_env = 0. Esfera: E(0) = 0, Q_env ∝ r³ e E ∝ r dentro, E ∝ 1/r² fora, contínuo em R; o gráfico é E/E_R × r/R e parte da origem.

## Limitações

Setas do coaxial e das folhas são poucas e fixas; folhas/placas são retângulos finitos que se dissolvem nas bordas; o esquema 2D da esfera é pequeno;
carga envolvida na esfera é apenas um halo (sutil por escolha); sem 1080p, sem áudio; conferido por quadros extraídos, não por reprodução contínua.

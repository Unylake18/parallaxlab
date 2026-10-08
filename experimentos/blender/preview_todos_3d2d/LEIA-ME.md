# Todos os casos de Gauss no padrão 3D + corte 2D (preview experimental)

Replica, nos 10 casos restantes, o formato aprovado no cabo coaxial (`../preview_coaxial_3d_2d`):

- **3D permanente** (Blender, Eevee): sólido, símbolos de carga, gaussiana fantasma que cresce/anda no instante real de cada quadro (30 fps).
- **Setas do campo avaliado** que acompanham a superfície gaussiana (comprimento ∝ |E|); onde E = 0 elas somem.
  - **setas planas (2D) no 3D**: paralelas ao plano da imagem, com comprimento constante na tela (sem encurtamento de perspectiva) e direção = projeção do vetor; o campo existente usa o mesmo estilo.
  - cilindros (linha, casca, maciço) e coaxial: **duas coroas** de setas planas na gaussiana — frente completa (12) e fundo só por fora (8); o campo existente de dentro some enquanto elas estão ativas (3D e corte 2D). Estilos alternativos testados: `--estilo coroa|coroa3|coroa2|malha|atual`. Planos: grade nas tampas do pillbox; esferas: anel de borda (12) + anel interno intercalado (6).
  - nos limites da região (R, ±d, a, b) as setas crescem/encolhem numa rampa curta (`campo_aval.fator`) em vez de aparecer/sumir de uma vez; o campo existente escurece na mesma rampa.
  - o **campo existente** (setas fixas) fica discreto enquanto as avaliadas aparecem e em destaque quando elas somem.
- **Corte 2D ampliado** (Manim), com a mesma trajetória p(t) do 3D: gaussiana, setas na gaussiana, região, `Q_env`, `E`. Sem gráfico.
- Texto enxuto: título, região, `Q_env`, `E(r)` e uma nota curta (o mesmo texto do `preview_todos_limpo`).

Fora do escopo desta rodada (ficam para a integração no vídeo principal): vetores normais n̂ / dA e a indicação explícita de "E = 0 porque E ⟂ n̂".

## Arquivos

| arquivo | função |
|---|---|
| `campo_aval.py` | regras puras (Python): onde o campo existe e comprimento da seta avaliada (`ativo`, `comp`) — usadas pelo Blender e pelo Manim |
| `render_todos_3d2d.py` | Blender: reaproveita os construtores de `../preview_todos_limpo/render_todos.py` e acrescenta as setas avaliadas |
| `cena_todos_3d2d.py` | Manim: 10 cenas (`Linha3D2D`, `CascaCil3D2D`, `MacicoCil3D2D`, `Folha3D2D`, `Placa3D2D`, `Duas3D2D`, `Face3D2D`, `CascaEsf3D2D`, `MacicoEsf3D2D`, `CapEsf3D2D`) |
| `juntar.py` | junta os MP4 (inclui o coaxial 3D+2D com coroas, `Coaxial3D2D_coroa_540p30.mp4`) em `saida/TODOS_3d2d_540p30.mp4` |
| `saida/` | `NN_<caso>_540p30.mp4` (11 casos) e `TODOS_3d2d_540p30.mp4` (136,1 s) |

Quadros do Blender: `renders/preview_todos_3d2d/<caso>/1120x784/` (148 PNG com alfa por caso; git-ignorado).

## Como regerar

```bash
# 1) Blender (≈ 1,5–3 min por caso; 148 quadros únicos cada)
"C:/Program Files/Blender Foundation/Blender 5.2/blender.exe" -b -P experimentos/blender/preview_todos_3d2d/render_todos_3d2d.py -- --caso todos
# (ou --caso linha,duas ; --estados para validar só 6 estados)

# 2) Manim, um caso por vez, com media_dir próprio
uv run python -m manim -r 960,540 --fps 30 --disable_caching --media_dir media/preview_todos_3d2d/linha experimentos/blender/preview_todos_3d2d/cena_todos_3d2d.py Linha3D2D

# 3) junta tudo
uv run python experimentos/blender/preview_todos_3d2d/juntar.py
```

## Limitações

- Verificado por quadros (pranchas) e por contagem de quadros repetidos nos trechos de movimento (≤ 6 de 145 por caso, no máximo 3 seguidos nos pontos de inversão); não houve conferência em reprodução contínua.
- 960×540 / 30 fps, sem áudio, sem legenda. Não integrado ao `yt_0002`.
- No capacitor esférico o vão é estreito: as setas avaliadas são curtas e, no corte 2D, ampliadas (×1,8) para leitura.
- As setas avaliadas são esquemáticas (quantidade fixa), não uma contagem de linhas de campo; setas quase de frente para a câmera (projeção < 0,2) não são desenhadas.

# Reservado para o yt_0016 (momento de sistemas)

Movido do preview v1 do yt_0015 na rodada v2 (handoff_v2.md §0). Não faz parte do yt_0015; não apagar.

- `sec_d.py` — C09 (por que o momento se conserva), C10 (agarrar ou rebater / gelo), C11 (o caçador no lago), C12 (os gases do rifle), C13-1.
- `sec_e.py` — C13-6/7 (Newton e a luz, fim), síntese e CTA do v1 (granada → centro de massa).
- `sec_t_v1_camada13.py` — camada Manim do trecho 3D da luz na água (classe `Camada13`; a `Camada01` do mesmo arquivo virou o T2 do yt_0015).
- `threejs_cena3d/` — `c13.js`, `c13.html` (tanque de água, corpúsculos de luz) e `timeline_c13.json`. Para usar: copiar para
  `threejs/cena3d/` (e o json para `threejs/`) da unidade nova; dependem de `base3d.js`, `three.min.js` e `RoomEnvironment.js`.
- `gerar_timelines_v1.py` — gerador de tempos do v1 (inclui o T2/c13 a partir das âncoras C13-2..5 da narração v2).
- `renders_v1/` — renders do trecho 3D da luz na água no v1.
- As âncoras C09–C13 estão na narração v2 (`../narracao_sugestao_v2.md`); os tempos nominais, em `../ancoras_v1.json`.

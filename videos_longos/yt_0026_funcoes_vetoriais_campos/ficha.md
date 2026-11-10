# Funções a valores vetoriais e campos vetoriais

- **ID:** `yt_0026`
- **formato:** `longo_horizontal`
- **natureza:** `teoria_visual`
- **Série pública:** **CÁLCULO III · EP. 01**
- **disciplina:** `Cálculo III`
- **bloco:** `Funções de várias variáveis a valores vetoriais`
- **modulo:** `3.1-T1 Funções a valores vetoriais e campos vetoriais (no docs/mapa_curricular.md atual: 11.1 Campos escalares e vetoriais)`
- **referencia:** `Guidorizzi, Um Curso de Cálculo, vol. 3, 6ª ed., §1.1 (Ex. 1–3) e §1.2 (Ex. 1–2; Exerc. 1c)` — só na ficha e na descrição do YouTube; nunca na tela nem na fala.
- **pergunta narrativa (título):** Como a mesma fórmula pode girar o plano inteiro e, ao mesmo tempo, virar um redemoinho de setas?
- **pergunta_central:** como enxergar uma função que recebe um ponto e devolve um vetor, se o gráfico dela não cabe em lugar nenhum?
- **pre_requisitos:** curvas (funções de uma variável a valores em ℝⁿ); funções de várias variáveis a valores reais e seus gráficos; produto escalar
- **payoff_principal:** a mesma fórmula tem duas leituras, transformação (move pontos e se vê acompanhando conjuntos) e campo vetorial (pendura uma seta em cada ponto); desenhar um campo com três perguntas; as trajetórias de um campo saem da derivada
- **duracao_alvo:** sai da voz real. Estimativa nominal (2,7 palavras/s, `duracoes_estimadas.json`, com a abertura do handoff v4): ~16,3 min sem o B7, ~16,9 min com o B7. Preview v3 renderizado: 16,4 min sem o B7, 17,1 min com o B7. Se a voz passar de 15 min, o Kaio decide o corte; o B7 já foi mantido, então a ordem de corte que sobra é B3-6, depois a semirreta do B3-4.
- **3d_threejs:** `caixa` (T3), `colunas` (T5), `folha_paraboloide` (B4), `campo_espaco` (B7) — `threejs/cena3d/f26.js`, fundo `fundo_calculo_liso`
  - v3 (handoff v4 §2.3, sistema visual v3 da série de Cálculo): superfícies opacas com cor diferente em cada lado e borda de luz; luz chave com sombra, hemisférica, contraluz e preenchimento; linhas sobre superfícies em tubos; chão com sombra e o domínio projetado; setas com corpo e cor pela intensidade; colunas e caixa em três tons fixos com aresta clara. As cenas `fluxo_tigela` e `hemisferio` saíram com a abertura antiga.
- **solido_3d:** nenhum do arsenal Blender; geometria de `superficie_parametrizada` (malha que vira paraboloide), `campo_vetorial` (setas 3D) e `integral_dupla_colunas` (colunas) usada como referência e portada para Three.js
- **fundo:** milimetrado noturno parado (`assets/calculo/papel.py`, `usar_papel`); 3D sobre `fundo_calculo_liso`
- **canto:** a partir do bloco A (some durante o T). Linha 1 `CÁLCULO III · FUNÇÕES A VALORES VETORIAIS E CAMPOS VETORIAIS`; linha 2: `QUE FUNÇÃO É ESSA`, `TRANSFORMAÇÃO`, `A DOBRA`, `PARA O ESPAÇO`, `CAMPO VETORIAL`, `DE VOLTA AO REDEMOINHO`, `NO ESPAÇO`, `RESUMO`
- **abertura (T):** handoff v4 §3: três promessas (terreno medido pela cerca, redemoinho medido na borda, caixa fechada), GREEN · STOKES · GAUSS, mapa do caminho e o cartão `CÁLCULO III` / `UMA SETA EM CADA PONTO`
- **ordem:** T → A → H → B1 → B2 → B3 → B4 → B5 → B6 → B7 → S (B7 continua renderizado como seção separada, `PB7`)
- **B7:** fica no vídeo (decisão do Kaio no preview v1, 2026-11-09). Preview de referência: `renders/preview_yt0026_v1_com_b7_960x540.mp4` (16,9 min).
- **Status:** `preview silencioso v3 (960×540 @ 15 fps), sem voz` — `renders/preview_yt0026_v3_com_b7_960x540.mp4` (17,1 min); sistema visual v3 da série de Cálculo implementado só na unidade (`kit.py`, `threejs/cena3d/f26.js`), à espera de aprovação para ser promovido a `assets/calculo/`

## Arquivos
- `narracao.md` — Anexo A do handoff v2 (fonte do `ancoras.json`); `gerar_ancoras.py` → `ancoras.json`, `duracoes_estimadas.json`
- `kit.py` — paleta da Matemática, estilo v3 (contorno escuro, chapas, pontos com anel, placas, seta de voo, cor de seta por intensidade, auditoria `[estilo]`), base de cena (relógio por quadro, âncoras, canto), caneta, fundo 3D
- `sec_*.py` — um lote por seção; `cena.py` registra os lotes
- `render.sh` / `render3d.sh` / `render_todos.sh`, `montar_preview.py`, `prancha.py`

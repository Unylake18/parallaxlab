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
- **duracao_alvo:** voz real (v9): 15:17,8 de fala (917,8 s, ~3,1 palavras/s); vídeo final 15:21,8 (921,8 s, com B7 e 3 s de logo no CTA).
- **3d_threejs:** 4 cenas em `threejs/cena3d/c7.js` (render `threejs/r3d.js`), fundo transparente sobre o violeta liso da câmera: `c7_colunas` (T1), `c7_fluxo` (T3), `c7_paraboloide` (B4; também em B1 e S), `c7_campo` (B7). Final 1920×1080: alinhamento 3D × Manim ≤ 0,05 px (`qa3d_1080.py`, `threejs/timeline_1080.json`).
  - v3 (handoff v4 §2.3, sistema visual v3 da série de Cálculo): superfícies opacas com cor diferente em cada lado e borda de luz; luz chave com sombra, hemisférica, contraluz e preenchimento; linhas sobre superfícies em tubos; chão com sombra e o domínio projetado; setas com corpo e cor pela intensidade; colunas e caixa em três tons fixos com aresta clara. As cenas `fluxo_tigela` e `hemisferio` saíram com a abertura antiga.
- **solido_3d:** nenhum do arsenal Blender
- **fundo:** papel v2 (2026-11-11): violeta liso parado (`assets/calculo/papel.py`, `usar_papel`) + grade que nasce dos eixos de cada cena (`self.grade(...)` no `kit.py`, `papel(ax)`; um por painel; liso no 3D)
- **canto:** a partir do bloco A (some durante o T). Linha 1 `CÁLCULO III · FUNÇÕES A VALORES VETORIAIS E CAMPOS VETORIAIS`; linha 2: `QUE FUNÇÃO É ESSA`, `TRANSFORMAÇÃO`, `A DOBRA`, `PARA O ESPAÇO`, `CAMPO VETORIAL`, `DE VOLTA AO REDEMOINHO`, `NO ESPAÇO`, `RESUMO`
- **abertura (T):** handoff v4 §3: três promessas (terreno medido pela cerca, redemoinho medido na borda, caixa fechada), GREEN · STOKES · GAUSS, mapa do caminho e o cartão `CÁLCULO III` / `UMA SETA EM CADA PONTO`
- **ordem:** T → A → H → B1 → B2 → B3 → B4 → B5 → B6 → B7 → S (B7 continua renderizado como seção separada, `PB7`)
- **B7:** fica no vídeo (decisão do Kaio no preview v1, 2026-11-09). Preview de referência: `renders/preview_yt0026_v1_com_b7_960x540.mp4` (16,9 min).
- **Status:** `final v10 (2026-11-11)`: v9 com o papel v2 (fundo e grade; narração, sync, tempos, cores e layout iguais; áudio do master v9 copiado pacote a pacote, `montar_master_v2.py`; render `render1080_v2.sh`); voz ElevenLabs v4, master 1080p30 CRF 14 (`renders/yt_0026_master_final_1080p30.mp4`), `legenda.srt` separada, entregue em `entregas/Cálculo III - EP 01 - Funções a valores vetoriais e campos vetoriais - 0026/`. Conferência de tempo: `conferencia_v9.md`.

## Arquivos
- `narracao.md` — Anexo A do handoff v9 (fonte do `ancoras.json`); `narracao_tags.md` (texto corrido da voz) → `audio/narracao_v4.wav` = `audio/narracao_final.wav`; `alinhar_voz.py` → `alinhamento_palavras.json`; `gerar_ancoras.py` → `ancoras.json` (tempo real da voz); `gerar_srt.py` → `legenda.srt`; `render1080.sh` + `montar_final.py` → render final; `qa_parado.py`, `qa3d_1080.py`
- `kit.py` — paleta da Matemática, estilo v3 (contorno escuro, chapas, pontos com anel, placas, seta de voo, cor de seta por intensidade, auditoria `[estilo]`), base de cena (relógio por quadro, âncoras, canto), caneta, fundo 3D
- `sec_*.py` — um lote por seção; `cena.py` registra os lotes
- `render.sh` / `render3d.sh` / `render_todos.sh`, `montar_preview.py`, `prancha.py`

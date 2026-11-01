# vid_0025 — relatório da rodada r6 (voz v5, nova abertura, sincronização por âncoras)

Data: 25/10/2026. Fase: preview com voz. SRT, master final, capa e publicação continuam fechados. Sem commit/push.

## Resultado

- **Vídeo com voz:** `renders/vid_0025_preview_com_voz.mp4` — 540×960, 15 fps, H.264 + AAC, **150,996 s (2:31)**, 2.265 quadros. Limite pedido: 2:59 (folga de 28 s).
- **Visual sem áudio:** `media/videos/cena/960p15/ArcoIris025.mp4` (mesmo conteúdo).
- **Pranchas e zip para o GPT:** `renders/preview_r6_prancha_01..10.png`, `renders/anc_r6_01..06.png` (quadro de cada âncora, com a palavra falada), `renders/preview_r6_para_gpt.zip` (todos os quadros + MP4 com voz + cena.py; temporário).

## Voz

- ElevenLabs `eleven_v4`, voz `qw7jgPZWOKrl10GsjQ82`, texto `narracao_tags_v5.md` (2.652 caracteres, 1 bloco, 1 tomada) → `audio/narracao_v5.wav`, 146,2 s (≈ 3,1 palavras/s).
- A voz **não foi ouvida** por mim (sem ouvido). Alinhamento forçado das 459 palavras (sem transcrição) sem desvio de ordem: nenhuma tag foi lida em voz alta.
- Pausas: 9 silêncios, total 3,61 s, inseridos nos vãos entre frases onde a animação precisa de mais tempo que a fala (maiores: antes de "formam um cone", 0,66 s; antes de "quanto vale esse máximo", 0,51 s). Resultado: `audio/narracao_sync.wav`.

## Sincronização (meta: no máximo 0,2 s de atraso)

- 70 âncoras (início de cada frase/cláusula que dispara um evento visual) a partir do alinhamento palavra a palavra (`gerar_ancoras.py` → `ancoras.json`).
- Mede-se a duração natural de cada trecho visual (`MEDIR=1`, sem renderizar) → `plan_sync.py` calcula pausas e escalas → render usa relógio em quadros exato (`play` com `(q−0,5)/15`, `wait` com `(q+0,5)/15`).
- **Medido no render final:** atraso máximo **+0,016 s**, mínimo −0,132 s, média −0,097 s. Nenhuma âncora depois de 0,2 s; a imagem começa de 0,07 a 0,13 s antes da palavra. Relógio da cena = relógio do Manim = quadros do arquivo (2.265). Posição das palavras no áudio com pausas = alvo do plano com erro ≤ 0,016 s.
- Conferência visual: `anc_r6_*.png` mostra, para cada âncora, o quadro 0,25 s depois do início da palavra.

## O que mudou em relação ao r5

- **Nova abertura (C01):** o arco-íris tenta outros lugares do céu ("não aparece em qualquer lugar"), trava num ângulo ("fica preso a um ângulo") com o 42° ("cerca de quarenta e dois graus"), o 42° perde a referência e surge um "?" no centro ("de quê?"), e só então entram Sol, você, a sombra, a linha e a direção antissolar ("trace uma linha... essa é a direção antissolar... medimos o arco").
- **Cenas reescritas evento a evento** para acompanhar a fala (âncoras em todas as cenas, C02–C11).
- **Cortes de tela para caber na fala:** C02 não explica mais R e b/R (b/R aparece como guia na varredura de C06); C04 sem o aviso de triângulo isósceles em texto (ticks + R mantidos); C05 com 3 estados algébricos de θ em vez de 4; C07 sem o histograma de raios por grau (ficam o detalhe ×10, a janela de 1°, "5 DE 25 ≈ UM EM CADA CINCO" e o teto 42,1°); C08 sem o estado intermediário n²(1−sen²r)→(duas etapas fundidas); C09 com o zoom do gráfico em duas etapas (vermelho, depois violeta); C10 com varredura mais curta (8 passos).
- **Acabamentos:** rótulo HORIZONTE fora do caminho do arco; trocas de texto sem dois textos juntos; auditor de sobreposição sem avisos.

## Verificação

`py_compile` OK; auditor de sobreposição (texto×texto, texto×traço, quadro, faixa inferior) sem avisos nas pausas de leitura; asserções físicas do r5 mantidas (abertura do gancho = 42,078107°).

## Pendências reais

- Ouvir a tomada: pronúncia (números por extenso, "Snell", "antissolar"), entonação das tags e o "refração de quarenta..." (sem `[short pause]` na v5).
- Transições de 0,3–1 s (morfismos de equação, `TransformFromCopy`) mostram, por instantes, termos em movimento sobrepostos; é intencional (mostra de onde vem cada termo) e fora do alcance do auditor, que mede só estados parados.
- O arquivo de áudio tem pausas longas só em 2 pontos (≥ 0,6 s); se a pausa soar estranha, reduzir a escala mínima em `plan_sync.py --sfloor`.
- Falta SRT (texto sem tags + tempos do plano), master final e capa; fases fechadas.

Teste do arsenal: não se aplica (solido_3d: nenhum).

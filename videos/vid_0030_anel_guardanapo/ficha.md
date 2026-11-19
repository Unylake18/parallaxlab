# O anel de guardanapo: por que só a altura determina o volume?

Série pública: **ABSURDO CALCULÁVEL · EP. 03**

- id: vid_0030
- formato: curto_vertical
- final futuro: 1080×1920 / 30 fps · alvo com voz 150–170 s (< 3 min)
- status: preview com voz v5 (540×960 / 15 fps, 180 s; voz v2.1 178,6 s sincronizada palavra a palavra, ±0,2 s) — antes: preview visual silencioso (540×960 / 15 fps) — física, storyboard e decisões congelados pelo Kaio em 2026-10-27
- direção visual: pipeline Three.js (geometria 3D) + Manim/MF-Tools (matemática) + Remotion (experimento de orquestração)
- implementação: `cena3d/cena3d.js` (3D), `cena.py` → `CenaMat` (matemática) e `CenaUI` (interface), `timeline.json` (fonte única de tempo), `compor.py` (preview oficial), `remotion/` (experimento)
- solido_3d: nenhum
- justificativa de solido_3d: a esfera furada (anel de guardanapo) não existe no arsenal Blender; geometria nova feita em Three.js (zona esférica + parede cilíndrica, sem tampas).

## Pergunta e mensagem

- Hook (v4, 0–30 s): porta-guardanapo (etiqueta "ANEL DE GUARDANAPO") → esfera fantasma + furo (etiqueta "= ESFERA
  FURADA") → três esferas (R = 5, 7, 10) furadas viram o trio de h = 6 cm, "QUAL TEM MAIS VOLUME?" e "MESMA ALTURA: h = 6 cm".
  Narração de referência em `narracao_tags_v1.md` (Seki Kōwa só na fala, "estudava essa forma"; nada de história na tela).
- C06 (v4): antes da prova, corte das paredes no equador, R − a = 1,00 · 0,68 · 0,46 cm. C07 (v4): limites vistos no 3D
  (a = 0: o anel engrossa até a esfera; h → 0: afina até um fio), com contador de h e V.
- Mensagem: anéis com a **mesma altura h** têm o **mesmo volume**, qualquer que seja a esfera de origem.
- Proteção: "Não é qualquer furo que dá o mesmo volume. O que precisa ser igual é a altura h do anel que sobra." (só no C06, uma vez — v3: a tela não repete mensagens). Nunca "esferas maiores dão o mesmo volume".

## Matemática congelada

R² − a² = (h/2)²; fatia em z: A(z) = π[(R² − z²) − a²] = π[(h/2)² − z²] (R some) = área da fatia da esfera de raio h/2 →
Cavalieri: V = (4/3)π(h/2)³ = **πh³/6**. Integral só confirma. h = 6 cm ⇒ V = 36π cm³ ≈ 113,1 cm³ para qualquer R
(R = 5 ⇒ a = 4; R = 7 ⇒ a = √40; R = 10 ⇒ a = √91; R = 100 só em texto). a = 0 ⇒ esfera inteira; h → 0 ⇒ V → 0.

## Cores (pedido do Kaio em 2026-10-27: "pode usar cores, bem Parallax Lab")

h = ciano #35D9FF (protagonista) · R = magenta #EA63FF (some da conta) · a = violeta #9C8CFF (furo; no lugar do
azul-claro, pedido do Kaio) · z, eixos e construção = GEO #B8C4DA.

v2 (2026-10-27): anel azul #3D7BFF em todas as cenas, acetinado (nunca cinza-aço); trio do gancho na mesma família azul
(#5C93FF / #3D7BFF / #2C68EA, só a luminosidade muda) com rótulos "R = …" em magenta · esfera de Cavalieri e seu disco
em magenta translúcido (contorno #F7B8FF; ρ em #F7B8FF) — o Kaio pediu para tirar o âmbar/amarelo · esfera original
fantasma (momento em que o R sai) em magenta · material removido pelo furo vira violeta fantasma · coroa branca com
contorno #9CC8FF · equação ativa #F2F6FF a 100 %, usada a 85 % (v3; mínimo 75 %), fórmula-chave em caixa #0E2A52 / borda #7FB2FF.
v4 (2026-10-29): sólido com gradiente #2E5BD8 → #1B3FA6, rim light #8EC5FF, parede do furo mais escura e malha fina
(meridianos/paralelos, alfa 0,12); v4.1 (Kaio, 29/10): sem halo/contorno preto nem chip sobre o
sólido — traços e rótulos sólidos e opacos; sobre o sólido azul, R em branco e h, h/2 em magenta. v4.2 (Kaio, 29/10): **h é magenta #EA63FF em todo o vídeo** (álgebra,
3D, régua, títulos, contadores) e **R é branco**; ciano #35D9FF só como destaque que não é grandeza (setas, ✓, riscos de
cancelamento, "O MESMO VOLUME"). Isto substitui "h = ciano, R = magenta" acima. Exceção em aberto (decisão do Kaio): as grandezas seguem coloridas (R magenta, h ciano, a violeta) em vez de GEO.

## v5 (2026-10-29) · voz e sincronia
- Narração `narracao_tags_v2.md` (v2.1, cortes 1–3 aplicados: voz sem cortes 185,8 s → 178,6 s). Voz `audio/narracao_v2.wav`
  (normalizada a −1 dBFS em `audio/narracao_v2_norm.wav`), alinhamento forçado em `alinhamento_palavras.json`.
- A cena segue a voz (`timeline.json` "audio"): 64 pares fala ↔ tela conferidos em `qa/sincronia.py` (tolerância ±0,2 s).
- Mudanças de estrutura impostas pela voz: o C02 não refura a esfera (o hook já mostrou); no C04 a varredura do plano vem
  antes da caixa A_anel = A_esf (ordem da fala) e a câmera aproxima a esfera pequena com ρ, z e h/2 fora dela; no C05 a
  integral virou conferência curta (∫ → primitiva → πh³/6), porque a frase da integral saiu no corte 1.

## Master e legenda (2026-10-29)
- Master `renders/vid_0030_master_v1.mp4`: 1080×1920 / 30 fps, 180,0 s, H.264 yuv420p CRF 14, voz AAC 48 kHz (Remotion,
  composição `Vid0030Final`; 3D `frames3d_1080x1920`, âncoras `ancoras_30fps.json`, Manim `media_final/…/1920p30`).
- Legenda `legenda.srt` (86 blocos, ≤ 30 caracteres por linha, 2 linhas) gerada por `gerar_legenda.py` a partir do
  alinhamento da voz; cores das grandezas em `cores_legenda.py` (h magenta, raio do furo violeta, altura do corte GEO;
  expressão colorida nunca quebra entre linhas nem entre blocos). Legendado `renders/vid_0030_legendado_v1.mp4` (CRF 14).
- Voz final `audio/narracao_final.wav` = cópia de `narracao_v2_norm.wav` (a voz que entrou no master).
- **Entregue em 2026-10-29:** `entregas/Absurdo Calculável - EP 03 - O anel de guardanapo por que só a altura determina o
  volume - 0030/` (master, legendado, legenda, áudio, texto, manifesto). Sem capa.

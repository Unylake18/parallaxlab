# Por que um foguete é quase todo combustível?

- **ID:** yt_0019 · último vídeo do módulo 4.9 (momento): massa variável, empuxo, Tsiolkovsky, perda por gravidade e estágios.
- **formato:** longo_horizontal
- **natureza:** teoria_visual + exercicio_resolvido
- **disciplina:** Física I · **bloco:** Momento e colisões · **modulo:** 4.9 Momento linear e impulso (sistemas de massa variável)
- **referencia:** Sears 14ª ed. §8.6; Moysés vol. 1, sistemas de massa variável (só na ficha e na descrição, nunca na tela nem na fala)
- **pergunta_central:** Por que um foguete é quase todo combustível, e como ele acelera sem ter onde empurrar?
- **pre_requisitos:** ΣF⃗_ext = dP⃗/dt para sistema; conservação do momento; centro de massa de sistema isolado; integral de 1/x
- **payoff_principal:** escolhendo o sistema que inclui o que sai, sai o empuxo v_ex |dm/dt| e, integrando, Δv = v_ex ln(m₀/m_f); o logaritmo e o
  peso da estrutura obrigam a ~89% de propelente e a estágios
- **duracao_alvo:** ~21–22 min (sai da fala; narração v1.2: 3.397 palavras, 21,0 min a 2,7 palavras/s)
- **3d_threejs:** `threejs/cena3d/f19.js`, cenas `rampa` (hook H1–H3, T4-1/T4-2, S1: foguete de dois estágios na rampa, corte com os tanques,
  piso com grade ciano) e `esp` (T2-1, T2-6, T3-7/T3-8: foguete no espaço com o jato de partículas da simulação; E2-3: separação de estágios)
- **solido_3d:** nenhum do arsenal Blender; geometrias próprias em Three.js
- **Canto:** linha 1 `MECÂNICA · FOGUETE E MASSA VARIÁVEL`; linha 2 = bloco da vez
- **Status:** preview silencioso v1 960×540 / 15 fps do vídeo inteiro (handoff v1 de 2026-10-31) em `renders/preview_yt0019_v1_960x540.mp4`.
  Sem voz, SRT, master nem entrega.

## Estrutura e lotes
PH hook H1–H3 + abertura A1–A3 · PT1 carrinho de areia · PT2 empuxo · PT3 Tsiolkovsky · PT4 gravidade · PE1 decolagem · PE2 estágios ·
PE3 esteira de areia · PS síntese S1 + EN1–EN2. Render: `./render_v3.sh LOTE` (pedidos 3D → Three.js → render, com a auditoria em paralelo) ou
`./render_fila.sh L1 L2 …` (dois por vez); `montar_preview.py` emenda; `qa19.py` → `renders/qa.txt`; `prancha_humana.py` (G28).

## Arquivos
`narracao_sugestao.md` (narração v1.2 = Anexo A) → `gerar_ancoras.py` → `ancoras.json` · `kit.py`, `prob.py`, `prob2.py` (copiados do yt_0018;
muda o título, a tabela de cor por token e as zonas da Pilha) · `pecas19.py` (SimEsp: foguete + gás com massa e momento exatos; fundos 3D;
foguete 2D, carrinho, patinadores, manequim, barras; números de conferência) · `sec_*.py` (um por lote) · `threejs/` (r3d.js, b3d.js, f19.js).

## Números de conferência (g = 9,8 m/s²)
Iguais ao Anexo A do handoff v1 (conferidos por `qa19.py`, seção NÚMEROS): 300 kN; 196 kN; a₀ = 5,2; t_q = 133,3 s; 4.023,6; 1.306,7; 2.716,9;
a_f = 65,2; a_sentida = 75 (7,65 g); R = 11 → 7,194 km/s; e^1,5 = 4,4817; f₂ = 5,3414 P; m₀₂ = 6,8755 P; m₀₁ = 47,273 P; 89,0 / 8,9 / 2,1%;
30 N; 45 W; 22,5 W; desafio (não falado) 86,5%.

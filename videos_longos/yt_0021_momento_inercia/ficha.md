# Momento de inércia: por que o mesmo bastão exige o dobro de energia para girar?

- **ID:** yt_0021 · vídeo 2 de 7 do módulo Rotação de corpos rígidos (IDs provisórios yt_0020–yt_0026)
- **formato:** longo_horizontal
- **natureza:** teoria_visual + exercicio_resolvido
- **disciplina:** Física I · **bloco:** Rotação · **modulo:** 4.11 Rotação de corpos rígidos (energia de rotação e momento de inércia)
- **referencia:** Sears 14ª ed. §9.4–9.6; Moysés vol. 1, cap. 12; Feynman I, cap. 19 (só na ficha e na descrição, nunca na tela nem na fala)
- **pergunta_central:** se a massa é a mesma, por que girar o mesmo bastão até a mesma velocidade angular custa o dobro de energia só porque o eixo mudou de lugar?
- **pre_requisitos:** energia cinética e conservação da energia mecânica, velocidade de um ponto em rotação (v = ωr, r = distância ao eixo), centro de massa, integral simples
- **payoff_principal:** o momento de inércia não é propriedade do objeto: é propriedade da distribuição de massa **em relação a um eixo**; K = ½Iω², I = Σmr² = ∫r²dm, I = I_cm + Md², I_z = I_x + I_y (placas)
- **frase_guia:** na rotação não importa só quanta massa há, importa a que distância do eixo ela está, e a distância pesa ao quadrado
- **duracao_alvo:** 25–27 min (sai da fala); narração v1 nominal: 3.811 palavras, 24,0 min a 2,7 palavras/s
- **3d_threejs:** `threejs/cena3d/f21.js`, cenas `bastao` (H1–H3, T5-6, S2: bastões no plano horizontal, câmera de cima, pino vertical) e `esfera` (T4-4 esfera fatiada em 14 discos; T6-4 esfera com os três eixos)
- **solido_3d:** nenhum do arsenal Blender; geometrias próprias em Three.js
- **Canto:** linha 1 `MECÂNICA · MOMENTO DE INÉRCIA`; linha 2 = bloco da vez
- **Status:** preview silencioso v1 960×540 / 15 fps do vídeo inteiro (handoff v1 de 2026-11-02) em `renders/preview_yt0021_v1_960x540.mp4`. Sem voz, SRT, master nem entrega.

## Estrutura e lotes
PH hook · PA abertura · PT1 energia de um giro · PT2 de que depende I · PT3 massa contínua · PT4 aros, discos e esferas · PT5 eixos paralelos ·
PT6 eixos perpendiculares · PE1 carretel · PE2 haste · PE3 placa com recorte · PS síntese e encerramento.
Render: `./render.sh L` (2D), `./render3d.sh L` (pedidos 3D → Three.js → Manim), `./render_todos.sh L1 L2 …`; `./auditar.sh L` (portão);
`montar_preview.py v1` emenda e grava capítulos; `qa21.py` → `renders/qa.txt`; `conferencia.py v1` → quadros de conferência e pranchas por bloco.

## Arquivos
`narracao_sugestao.md` (narração v1 = Anexo A) → `gerar_ancoras.py` → `ancoras.json` · `kit.py`, `prob.py`, `prob2.py` (copiados do yt_0019; muda o
título, a paleta — massa e I em rosa `#FF7EB6`, velocidade `#9C8CFF` — e a cor por token: `tinge()` pinta as letras pela forma do glifo) ·
`pecas21.py` (números de conferência, corpos 2D, câmeras 3D, `Lote21`) · `sec_*.py` (um por lote) · `threejs/` (r3d.js, b3d.js, f21.js).

## Números de conferência (g = 9,8 m/s²)
Iguais à tabela do Anexo A (conferidos por `qa21.py`, seção NÚMEROS): I = 0,282 e 0,141 kg·m² (razão 2,000); K = 14,1 e 7,06 J; barra 0,212 e
0,053 kg·m²; haltere 1 e 2 kg·m²; E1 3,13 m/s, 31,3 rad/s, 4,9 + 4,9 J, 4,43 e 2,56 m/s; E2 5,42 rad/s, 5,42 / 4,43 / 4,70 m/s, 2L/3;
E3 0,090 / 0,0169 / 0,0731 / 0,0694 kg·m², −R/6, 4,48 rad/s, 0,22 e 1,34 m/s.

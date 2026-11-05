# Cinemática angular: por que a ponta da hélice chega a quase 1.000 km/h?

- **ID:** yt_0020 · vídeo 1 de 7 da Rotação (IDs provisórios yt_0020–yt_0026). Na página do mapa renumerada o módulo aparece como 1.12; o
  repositório ainda usa 4.11.
- **formato:** longo_horizontal
- **natureza:** teoria_visual + exercicio_resolvido
- **disciplina:** Física I · **bloco:** Rotação · **modulo:** 4.11 Rotação de corpos rígidos (cinemática angular)
- **referencia:** Sears 14ª ed. §9.1–9.3; Moysés vol. 1, cap. 11; Feynman I, cap. 18 e 20 (só na ficha e na descrição, nunca na tela nem na fala)
- **pergunta_central:** se a hélice inteira gira no mesmo ritmo, por que cada ponto tem uma velocidade diferente, e que número descreve o giro do
  corpo todo?
- **pre_requisitos:** movimento circular (a_c = v²/r), MUV em 1D, derivada e integral simples
- **payoff_principal:** um corpo rígido em eixo fixo tem um só θ, ω, α; cada ponto multiplica pela distância ao eixo (v = rω, a_t = rα, a_c = ω²r);
  como vetor, v⃗ = ω⃗ × r⃗
- **frase_guia:** o corpo inteiro compartilha o mesmo giro, mas cada ponto transforma esse giro em movimento de um jeito diferente
- **duracao_alvo:** ~26 min (sai da fala; narração v1.1: 4.247 palavras, 26,9 min a 2,7 palavras/s)
- **3d_threejs:** `threejs/cena3d/r20.js`, cenas `helice` (H1–H3, T4-2, S2), `livros` (T5-2 a T5-4: dois livros com eixos fixos no laboratório),
  `disco` (T5-1, T5-5 a T5-8: disco com ω⃗, α⃗, r⃗, r_⊥ e v⃗ = ω⃗ × r⃗ calculado no Three.js) e `terra` (E3: órbita vista de lado e de cima; Terra
  geocêntrica com São Paulo)
- **solido_3d:** nenhum do arsenal Blender; geometrias próprias em Three.js
- **Canto:** linha 1 `MECÂNICA · CINEMÁTICA ANGULAR`; linha 2 = bloco da vez
- **Status:** preview silencioso v1 960×540 / 15 fps do vídeo inteiro (handoff v1 de 2026-11-02). Sem voz, SRT, master nem entrega.

## Estrutura e lotes
PH hook H1–H3 + abertura A1–A3 · PT1 como medir um giro · PT2 quão rápido gira · PT3 quando o giro acelera · PT4 cada ponto do corpo · PT5 para onde
aponta um giro · PE1 ventilador · PE2 bicicleta · PE3 Terra · PS síntese S1–S2 + EN1–EN2. Render: `./render_v3.sh LOTE` (pedidos 3D → Three.js →
render, com a auditoria em paralelo) ou `./render_fila.sh L1 L2 …`; `montar_preview.py` emenda; `qa20.py` → `renders/qa.txt`; `prancha_humana.py` (G28).

## Arquivos
`narracao_sugestao.md` (narração v1.1 = Anexo A) → `gerar_ancoras.py` → `ancoras.json` (régua nominal: 2,7 palavras/s) · `kit.py`, `prob.py`,
`prob2.py` (copiados do yt_0019; mudam o título, a paleta por família, a tabela de cor por token e a junção segura das partes do TeX) · `pecas20.py`
(disco de referência, setas curvas, ventilador, engrenagens, números de conferência) · `sec_*.py` (um por lote) · `threejs/` (r3d.js, b3d.js, r20.js,
tex20.js gerado por `gerar_texturas.py`).

## Cores por família (handoff §2.1)
ângulo âmbar `#FFC24D` (θ, Δθ, arco, área sob ω(t), rad e graus) · velocidade violeta `#9C8CFF` (ω, ω⃗, v, f, rpm) · aceleração verde `#3FE08B`
(α, a_t, a_c, a, g) · geometria `GEO #B8C4DA` (r, r⃗, r_⊥, R, eixos, cotas) · tempo e números puros em branco · corpos em aço com luz B · caixas `PANEL`.

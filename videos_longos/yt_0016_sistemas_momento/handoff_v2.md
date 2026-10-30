# yt_0016 — HANDOFF v2 (cópia de trabalho, condensada) — 2026-10-28

Fonte: avaliação do preview v1 + HANDOFF v2 do chat de Produção (colado pelo Kaio). Especificação de conteúdo: `narracao_sugestao.md` (v2).
Física e números: iguais ao `handoff_v1.md` §3.

## Avaliação do v1 (resumo)
- Fica: matriz de pares; números do cavalo; P(t) + Terra espelhada + soma zero; barras log do E7; nuvem de gases do E8; componentes do E9; DICA no canto.
- Problemas: 35 trechos parados ≥ 6 s (285 s); telas só de álgebra/texto (1:12, 2:16–2:32, 2:56, 11:44–12:00, 13:04–13:20, 16:24, 16:56–17:20,
  17:28–17:40, 18:08–18:16); cavalo 2D reprovado; sobreposições (1:04 fórmula do impulso × painel; 4:16 texto fantasma; 11:36 QUASE O DOBRO × V;
  13:04 ENERGIA (ESCALA LOG) × eixo); referências de livro nos headers; abertura fraca; escala pequena (blocos do T9, esferas do T7, ícones).

## Regras de tela
1. Proibida tela só de álgebra/texto: PALCO vivo + CONTA. Frases de fechamento (E9-7, C-3, S2) com o PALCO trabalhando.
2. Variáveis saem do desenho (`TransformFromCopy`, mesma cor). Rearranjo: `TransformMatchingTex`; cancelamento/troca: `TransformByGlyphMap`.
3. Sempre algo acontecendo: ≤ ~4 s sem informação nova; medir quadros parados e reportar todo trecho > 6 s (meta: nenhum).
4. Exercícios: esquema fixo no PALCO do começo ao fim; dados/álgebra/resultado descendo na CONTA. Barras de E6/E7 na CONTA.
5. Sem referências de livro na tela. Selo de ligação (DIM, op. 0,85): E6 `SISTEMA: VOCÊ + A BOLA`, E7 `MOMENTO POR COMPONENTE`,
   E8 `QUEM ESTÁ NO SISTEMA?`, E9 `IMPULSO NORMAL`. A ficha mantém `referencia:`.
6. Fade ~0,4 s entre capítulos, sem tela vazia.

Grade (handoff em 14,22 × 8; o quadro da unidade é 16 × 9 → ×1,125): HEADER y > 3,1, x < 3,9 · LOGO canto sup. dir. · PALCO x ∈ [−7,4; 0,7], y ∈ [−3,4; 2,8]
· CONTA x ∈ [1,1; 7,4], y ∈ [−3,4; 2,8] · CENTRO largura ≤ 10 com PALCO recuado (op. ~0,35) e em movimento · LEGENDA y ∈ [−4,15; −3,5] · DICA canto inf. dir., largura ≤ 4,7.
Folga ≥ 0,25; faixa escura atrás do header sobre 3D (#050816, op. 0,55); objetos do PALCO ≥ 60% da altura útil.

## Correções pontuais
A3 grade + folga; 4:16 coluna sai inteira antes da próxima; E6 `QUASE O DOBRO` em linha própria; E7 rótulo do eixo log acima com folga;
T8 setas T/−T fora do corpo e da corda, presas às pontas, mesmo comprimento, `?` op. ~0,7; T9 blocos maiores na metade de cima, gráficos logo abaixo,
o ponto do gráfico anda junto com os blocos.

## 3D (Three.js)
Obrigatório: cavalo (H1–H3, A2, A5, T8, S1; T8 acelera 0,32 m/s² a partir de ~0,3 m/s, câmera acompanha; T8-6 gelo sob as patas, a ≈ −1,26 m/s²);
manequim (E6 agarra/rebate; E7 tiro horizontal e 56°, recuo; T8-8 andando). Setas/rótulos/fronteira no Manim, alinhados ≤ 2 px.
Recomendado: esferas com molas (T7-1..7), disco com binário (T7-8), tanque (E9), vela solar (coda). Opcional: Terra (T9-2).
Plano B: 2D preenchido com o mesmo movimento. `solido_3d: nenhum`; `3d_threejs:` lista na ficha.

## Render e QA
Por lote; 3D primeiro em quadros soltos. Stills 1920×1080: A5, T7-3, T7-6, T8-5, T9-6, E6-4, E7-5, C-2.
QA: quadros parados (> 6 s); cenas sem PALCO; sobreposição; nenhuma referência de livro; números do v1 §3; alinhamento ≤ 2 px; quadros iguais nas camadas;
capítulos iguais ao v1. Parar com o preview v2 completo; relatório; sem commit nem push.

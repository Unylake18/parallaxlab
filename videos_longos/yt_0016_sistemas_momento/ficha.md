# MOMENTO EM SISTEMAS — O QUE MUDA O MOMENTO DE VÁRIOS CORPOS

- **ID:** yt_0016 (provisório; Parte 2 de 2 do 4.9 — o yt_0015 é uma partícula). Série do 4.9: yt_0015 momento e impulso → **yt_0016 sistemas** →
  yt_0017 centro de massa → yt_0018 foguete (IDs provisórios).
- **formato:** longo_horizontal
- **natureza:** teoria_visual (com exercícios resolvidos)
- **disciplina:** Física I · **bloco:** Momento e colisões · **modulo:** 4.9 Momento linear e impulso
- **referencia:** Moysés 8.1–8.3 e 9.2 · Sears 8.2 (exercícios 8.17, 8.20, 8.25) · Feynman I, 10-5
- **duração esperada:** ~20 min com a voz (narração v2: 3.255 palavras; nominal 20,1 min a 2,7 palavras/s; v1 tinha 3.005)
- **solido_3d:** nenhum, porque o vídeo vive de diagramas de forças, matriz de pares e antes/depois em 2D; explosao/colisao_1d/colisao_2d não mostram
  forças externas nem escolha de sistema (explosao fica para o yt_0017).
- **3d_threejs:** cavalo (hook, abertura, T8, S1), manequim (E6, E7, T8-8), esferas com molas e disco (T7), vela solar (coda). Tanque do E9:
  plano B (diagrama 2D preenchido). Pipeline por estado: `threejs/r3d.js` + `render3d.sh` (os 3D são do Three.js, não do arsenal).
- **Status:** v4 preview silencioso 960×540 / 15 fps (último antes da narração; `handoff_v4.md`, narração v3 em `narracao_v3.md`, âncoras v4 em `ancoras.json` e o mapa no vídeo em `mapa_ancoras_v4.txt`) em `renders/preview_yt0016_v4_960x540.mp4`. v3, v2 e v1 em `renders/`; fontes do v3 em `_v3/`.
- **Tag do canto:** `MECÂNICA · MOMENTO EM SISTEMAS`
- **Pergunta narrativa:** "Se a corda puxa o cavalo para trás com a mesma força com que puxa a pedra, como ele anda?"
- **Pergunta central:** o que muda o momento total de um sistema, e como escolher o sistema para a conta fechar?
- **Pré-requisitos:** yt_0015 (p⃗, J⃗ = Δp⃗, F⃗ = dp⃗/dt, 3ª lei), vetores por componente.
- **Payoff:** só força externa muda P⃗ (por componente); "não conserva? aumente o sistema"; o momento se divide igual e a energia fica principalmente
  com o mais leve.
- **Fontes da especificação:** `handoff_v1.md` (física, §3 números), `handoff_v2.md` (regras de tela, grade, 3D), `handoff_v3.md`, `handoff_v4.md` (regras 1.1–1.6) e `narracao_v3.md`
  (narração v2; a v1 em `narracao_sugestao_v1.md`).

## Estrutura
hook H1–H3 (cavalo e pedra) · abertura A1–A6 (liga ao yt_0015: um corpo → dois corpos → sistema) · T7 sistemas de partículas · T8 força interna não move o sistema · T9 escolher o sistema ·
T10 como a energia se divide · E6 agarrar ou rebater · E7 o caçador no lago · E8 os gases do rifle · E9 Newton e a luz · coda: a luz também tem
momento · síntese S1–S2 · encerramento EN1–EN2 (granada → próximo vídeo: centro de massa).

## Cabeçalho e capítulos
Linha 1: `MECÂNICA · MOMENTO EM SISTEMAS` (17, DIM, op. 0,5). Linha 2 = capítulo (30, branco). Sem referência de livro na tela (v2): nos
exercícios, selo de ligação (20, DIM, op. 0,85): E6 `SISTEMA: VOCÊ + A BOLA` · E7 `MOMENTO POR COMPONENTE` · E8 `QUEM ESTÁ NO SISTEMA?` ·
E9 `IMPULSO NORMAL`. Capítulos: SISTEMAS DE PARTÍCULAS · FORÇA INTERNA NÃO MOVE O SISTEMA · ESCOLHER O SISTEMA · COMO A ENERGIA SE DIVIDE ·
EXERCÍCIO 6 · AGARRAR OU REBATER · EXERCÍCIO 7 · O CAÇADOR NO LAGO · EXERCÍCIO 8 · OS GASES DO RIFLE · EXERCÍCIO 9 · NEWTON E A LUZ ·
A LUZ TAMBÉM TEM MOMENTO · RESUMO. Selo DICA (cartão `#0E2A52`, borda `#7FB2FF`) em T7-7, T8-8, T9-7, T10-4, E6-4, E7-5, E8-4, E9-7.

## Semântica de cor
velocidade violeta `#9C8CFF` · momento p⃗, P⃗, Δp⃗ magenta `#EA63FF` · força `#5AA2FF` (força interna/tensão em cinza apagado) · impulso `#9CC7FF` ·
energia cinética ciano `#35D9FF` · calor/energia dissipada laranja `#FF7A3D` · corpos em aço `#7A8696`/`#B8C4DA` · Terra/chão como corpo: aço mais
escuro · ângulos em arco branco fino · assunto do próximo vídeo em ciano. Verde não aparece.

## Arquivos
`cena.py` (lotes PH hook+abertura · P7 T7 · P8 T8 · P9 T9 · P10 T10 · Q6 E6 · Q7 E7 · Q8 E8 · Q9 E9 · PC coda · PS síntese e fim) ·
`kit.py` (helpers, relógio por quadro, grade PALCO/CONTA, `Fundo3D`, cabeçalho, DICA, fronteira) · `sec_cavalo.py` (cavalo 3D) ·
`sec_manequim.py` (poses do manequim 3D) · `sec_*.py` (seções) · `threejs/` (cenas `cena3d/*.js`, `r3d.js`, pedidos e quadros) ·
`assets_unidade/` (cavalo CC0 e manequim, cópias do yt_0015) · `ancoras.json` (de `gerar_ancoras.py`) · `render.sh`, `render3d.sh`,
`auditar.sh`, `parados.py`, `montar_preview.py`, `stills.sh`, `prancha_v2.py`, `zip_gpt.py`. Fontes do v1 em `_v1/`.

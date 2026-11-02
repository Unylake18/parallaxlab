# yt_0018 v6 — preview com voz (960×540, 15 fps)

Vídeo: `renders/preview_yt0018_v6_960x540.mp4` — **14,93 min (896,1 s)**, vídeo H.264 e narração AAC mono 192 kb/s. Fala medida: 14,13 min (2.659 palavras, 3,14 palavras/s).
QA: `renders/qa.txt` — portão G28 v5 **aberto**; 68 gatilhos de fala com a voz real, **0 fora de ±0,3 s**; VAZIO 0; PAUSAS 0 trechos ≥ 4 s; voz sem silêncio ≥ 3 s.

## Voz
- ElevenLabs, voz `qw7jgPZWOKrl10GsjQ82`, modelo `eleven_v4`, endpoint `/with-timestamps` (o alinhamento por caractere dá o início de cada âncora e de cada palavra, sem ASR).
- 4 blocos cortados em fim de âncora (H1…X2-3, X2-3b…X3-8, X3-9…X5-6, X5-7…EN2).
- **Takes regerados:** A2, X1-4, X3-5, X3-7, X3-8 (os blocos 1 e 2 saíram da v1.1: o primeiro comando rodou em parte antes da v1.2 ficar pronta; só essas 5 âncoras mudaram, então regerei só elas) · H1, H3 e EN1 (v1.3: hook e CTA ampliados a pedido do Kaio).
- Texto: `narracao_tags_v1_2.md` (handoff v6, nove trechos) e `narracao_tags_v1_3.md` (v1.2 + H1, H3 e EN1 ampliados, sem promessa de data). Os quatro `[short pause]` estão no X3-5, X3-6, X4-4 e X5-6.
- **Eu não ouvi os takes.** A conferência de pronúncia (Parallax Lab, um doze avos, cinco sextos, zero vírgula um quatro sete, Einstein, mil novecentos e seis, catorze vírgula sete) e a de "fala calma depois do short pause" ficam para o ouvido do Kaio.

## Montagem
- Folga entre a última palavra de uma âncora e a primeira da seguinte: 0,75 s; 1,2 s antes da troca de problema, do A1, do epílogo e do resumo.
- Pausas protegidas dentro da fala: H2 2,0 s depois de "em câmera lenta"; X3-6 1,5 s depois de "dá duas faixas"; X3-7 1,2 s depois de "a ponta oposta da folha"; X5-2 1,2 s depois de "marcar cinco quilos"; X5-6 1,0 s depois de "como cinco quilos"; EP2 1,2 s depois de "o que foi para a direita".
- A voz manda: cada âncora ganhou a janela da voz real; as cenas aceleram só os plays (fator por âncora, 0,62–1,0) e as esperas por fração (`ate`) seguem o ponto do texto na voz. Âncoras mais rápidas que a janela nominal do v5: A3, X0-2, X0-3, X1-4, X3-1 e EP1 (fator < 0,85).

## Pendências do v5 e itens novos
- 1.1 ZOOM ×5: o cubo encolhe a 80% e vai para a esquerda em 0,6 s, o painel cai à direita sem cobrir aresta nem eixo (0 pontos de aresta sob o painel na busca de posição), o cubo volta em 0,6 s depois de o painel sair. 3D × TEXTO zerada; alinhamento Three.js × Manim 0,000 px.
- 1.2 Conferência visual: `renders/v6/conferencia_v6.png` (22 quadros, tirados do preview com voz). DICA do X1: maior trecho sem pixel novo 0,6 s (meta ≤ 1,5 s).
- 1.4 PESADA: os voos de v₂ e K₂ saem por baixo da linha; nos quadros de 64,0 a 66,1 s do PX4 o "1" não passa mais sobre o "=".
- 1.5 EN2: `COMO ACELERAR NO VÁCUO SEM SE APOIAR EM NADA?`.
- 1.6 X3-10: `NOS LIMITES: A PONTA OPOSTA` entra com a frase "nos dois ângulos-limite".
- CTA (EN1) em três cartões, um por ideia; hook com a etiqueta "FOLHA = 4 × A MASSA DO GAFANHOTO" na frase "quatro vezes a massa dele".

## Físicas que seguem na tela
4 m/s em relação à água e fator 1,25 pelo recuo da folha (X3); divisão 2 : 1 só no referencial do CM e 3.000 J como total (X4-5); mostrador = N/g em todo quadro (diferença máxima 0,046 kg); "m = E/c²" com PISTA, NÃO DEMONSTRAÇÃO.

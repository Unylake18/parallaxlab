# Ciclo termodinâmico

formato: curto_vertical

Série pública: **EXERCÍCIO RESOLVIDO · EP. 07**

solido_3d: nenhum — briefing e visual aprovado inteiramente em 2D.

Fase: versão com partículas renderizada em 1080×1920 para avaliação, mantendo
a voz, as legendas e a sincronia aprovadas.

- Cena: `cena.py`, classe `CicloTermodinamico021`.
- Voz fornecida pelo usuário: `audio/narracao_final.wav`, 167,76 s, 44,1 kHz,
  estéreo. Texto correspondente em `texto_narracao.txt` (478 palavras).
- Preview com partículas: 540×960, 15 fps, 167,80 s de vídeo.
- Render de entrega: 1080×1920, 30 fps, H.264/yuv420p, CRF 14;
  duração ajustada à voz. Master com AAC (alvo 320 kb/s) e legendado em CRF 14.
- Gás ideal monoatômico; A = (V₀, P₀), B = (4V₀, P₀), C = (4V₀, 4P₀).
- Ciclo A → B → C → A: isobárico, isocórico, compressão em reta no P×V.
- Convenção: trabalho do gás positivo; Q = ΔU + W; U = 3/2 PV.
- Pergunta: “Qual é o calor total absorvido pelo gás durante o ciclo?”
- Resultados: Q_AB = 15/2 P₀V₀; Q_BC = 18 P₀V₀; Q_CA < 0;
  Q_abs = 51/2 P₀V₀; W_ciclo = Q_líquido = −9/2 P₀V₀.
- Representação toda em 2D; pistão na introdução e compacto durante os três
  processos e nas ferramentas, com barras qualitativas de V/P/T em branco/cinza,
  tendências explícitas e setas de trabalho/calor. A abertura mostra o estado A.
- Em B→C, pistão fixo enquanto pressão, temperatura e intensidade visual do gás
  aumentam. Em C→A, P e V caem juntos ao longo da reta; T também diminui.
- Movimento molecular: 36 partículas em violeta claro, quantidade fixa em todos
  os estados; rapidez proporcional à raiz quadrada de T. Posições refletem nas
  paredes e no pistão e acompanham o volume. A energia interna cresce com T;
  rapidez e concentração representam qualitativamente o comportamento da pressão.
  Modelo 2D ilustrativo, sem colisões entre partículas ou integração quantitativa
  do impacto em uma parede móvel. A cor magenta continua reservada ao calor.
- Variante com partículas em `media_particulas_preview/` e `media_particulas_final/`;
  montagem com `montar_final.py --preview|--final --particulas`.
  Fontes e arquivos da versão anterior permanecem na unidade.
- Gramática cromática: estrutura azul elétrico, trabalho ciano, energia interna
  violeta, calor magenta, álgebra neutra branca. Gráfico preservado nas contas.
- Cabeçalho: série e episódio no canto superior esquerdo; marca oficial no
  canto superior direito, conforme `docs/identidade_visual.md`.
- CTA somente com `@labparallax`, em degradê ciano → violeta → magenta,
  após o resultado final.
- Legendas em Inter SemiBold, no máximo duas linhas, abaixo do conteúdo;
  trabalho ciano, energia interna violeta e calor magenta.
- Sincronização por pausas medidas no WAV e interpolação silábica, sem ASR.
  `sync.json` guarda os marcos; `timing_*.json` registra as entradas da cena.
- Capa e publicação não fazem parte desta rodada. Revisão humana do audiovisual
  permanece pendente.

Marcos da voz: construção até 24,38 s; ferramentas 24,38–47,28 s;
A→B 47,28–73,20 s; B→C 73,20–96,32 s; C→A 96,32–117,16 s;
calor absorvido 117,16–126,51 s; área e sentido 126,51–148,87 s;
fechamento 148,87–166,33 s; CTA 166,33–167,76 s.

Os títulos entram ligeiramente antes da fala para que a troca de bloco esteja
concluída no início da frase. A relação geral da área do triângulo aparece antes
da substituição dos valores da base e da altura.
